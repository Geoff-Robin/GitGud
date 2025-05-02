"""
This module defines the ChatBot class, which handles the logic for the competitive programming assistant.

It includes methods for summarizing conversations, interacting with models, and executing code.
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Literal, Union
from langgraph.graph import StateGraph, START, END
from langgraph_reflection import create_reflection_graph
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from Agent.models import *
from httpx import AsyncClient
from pydantic_ai import Agent
from Agent.prompts import *


class ChatBot:
    """
    A chatbot for assisting with competitive programming problems.

    Attributes:
        messages (List[Dict[str, str]]): The conversation history.
        problem (str): The problem description.
        summary (str): A summary of the conversation.
        level (int): The assistance level (0, 1, or 2).
    """

    def __init__(
        self,
        messages: List[Dict[str, str]],
        problem: str,
        summary: str = "",
        level: int = 0,
    ):
        load_dotenv()
        self._messages = messages
        self._problem = problem.strip()
        self._summary = summary
        self._level = level
        self._API_KEY = os.getenv("GROQ_API_KEY")
        self._EXECUTE_URL = os.getenv("CODE_RUNNER_API_URL")
        assert self._API_KEY, "Missing GROQ_API_KEY in .env"
        assert self._EXECUTE_URL, "Missing CODE_RUNNER_API_URL in .env"

        self._chat_model: Agent[None, Union[str, ChatbotCodeOutput]]
        self._deps = AgentDeps(api_key=self._API_KEY, http_client=AsyncClient)
        self._chat_settings = {"temperature": 1}
        self._judge_settings = {"temperature": 0.3}
        self._summarizer_settings = {"temperature": 0.4}
        self._search_tool = duckduckgo_search_tool()

    def should_run(self, state: Dict[str, Any]) -> Literal["summarize", "call_model"]:
        return "summarize" if len(state["messages"]) > 10 else "call_model"

    async def summarize(self, state: Dict[str, Any]) -> Dict[str, Any]:
        self._chat_model = Agent(
            model="groq:meta-llama/llama-4-maverick-17b-128e-instruct",
            system_prompt=SUMMARIZER_PROMPT,
            model_settings=self._summarizer_settings,
            deps_type=AgentDeps,
        )
        # Making chat history into strings
        chat_history = ""
        for m in state["messages"]:
            if m["role"] == "user":
                chat_history += "User: " + m.content + "\n"
            else:
                chat_history += "Assistant: " + m.content + "\n"
        result = await self._chat_model.run(
            "Summarize the following:\n" + chat_history, deps=self._deps
        )
        self._summary = "Summary of earlier conversation" + result.output
        return state

    async def call_model(self, state: Dict[str, Any]) -> Dict[str, Any]:
        chat_history = None

        if self._summary == "":
            chat_history = "The below is earlier conversation:\n"
            for m in state["messages"]:
                if m["role"] == "user":
                    chat_history += "User: " + m.content + "\n"
                else:
                    chat_history += "Assistant: " + m.content + "\n"
        FINAL_SYSTEM_PROMPT = (
            SYSTEM_PROMPT[self._level]
            + "\n\nProblem:\n"
            + self._problem
            + self._summary
            if self._summary == ""
            else chat_history
        )

        self._chat_model = Agent(
            model="groq:meta-llama/llama-4-maverick-17b-128e-instruct",
            system_prompt=(
                SYSTEM_PROMPT[self._level]
                + "\n\nProblem:\n"
                + self._problem
                + self._summary
                if self._summary == ""
                else chat_history
            ),
            model_settings=self._chat_settings,
            deps_type=AgentDeps,
            output_type=Union[ChatbotCodeOutput, str],
            tools=[self._search_tool],
        )

        result = await self._chat_model.run(
            state["messages"][-1].content, deps=self._deps
        )

        state["messages"].append(
            {
                "role": "assistant",
                "content": result.output.extra_bot_response_beginning
                + "\n\n\n"
                + result.output.extracted_code
                + "\n\n\n"
                + result.output.code_explanation
                + "\n"
                + result.output.extra_bot_response_end,
            }
        )

        state["extracted_code"] = ExtractCode(
            code=result.output.extracted_code + "\n" + result.output.validation_code,
            language=result.output.extracted_code_language,
        )

        return state

    async def try_running(self, state: Dict[str, Any]) -> Dict[str, Any]:
        resp = requests.post(
            self._EXECUTE_URL,
            json={
                "code": state["extract_code"].code,
                "language": state["extract_code"].language,
            },
        )
        result = resp.json()
        output = result.get("output")
        self._chat_model = Agent(
            model="groq:meta-llama/llama-4-maverick-17b-128e-instruct",
            system_prompt=JUDGE_SYSTEM_PROMPT,
            output_type=JudgeOutput,
            model_settings=self._judge_settings,
            deps_type=AgentDeps,
        )
        result = await self._chat_model.run(
            user_prompt="Code:\n" + state["extract_code"].code + "\nOutput" + output,
            deps=self._deps,
        )
        if result.output.passed == "False":
            state["messages"].append(
                {
                    "role": "user",
                    "content": f"This solution code is incorrect, as i get the incorrect output: "+output,
                }
            )
        return state

    def create_reflection(self):
        agent_graph = (
            StateGraph(State)
            .add_node(self.summarize, "summarize")
            .add_node(self.call_model, "call_model")
            .add_conditional_edges(START, self.should_run)
            .add_edge("summarize", "call_model")
            .add_edge("call_model", END)
            .compile()
        )
        judge_graph = (
            StateGraph(State)
            .add_node(self.try_running, "try_running")
            .add_edge(START, "try_running")
            .add_edge("try_running", END)
            .compile()
        )
        return create_reflection_graph(agent_graph, judge_graph).compile()

    def create_agent(self):
        agent_graph = (
            StateGraph(State)
            .add_node(self.summarize, "summarize")
            .add_node(self.call_model, "call_model")
            .add_conditional_edges(START, self.should_run)
            .add_edge("summarize", "call_model")
            .add_edge("call_model", END)
            .compile()
        )
        return agent_graph

    def chat(self, message: str) -> Dict[str, Any]:
        result = None
        self._messages.append({"role": "user", "content": message})
        if self._level == 2:
            graph = self.create_reflection()
            state = {
                "messages": self._messages,
            }
            result = graph.invoke(state)
            return {
                "response": result["messages"][-2].content,
                "summary": self._summary,
            }
        else:
            graph = self.create_agent()
            state = {
                "messages": self._messages,
            }
            result = graph.invoke(state)
            return {
                "response": result["messages"][-1].content,
                "summary": self._summary,
            }
