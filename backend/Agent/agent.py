"""
This module defines the ChatBot class, which handles the logic for the competitive programming assistant.

It includes methods for summarizing conversations, interacting with models, and executing code.
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Literal, Union
from langgraph.graph import StateGraph, START, END
from Agent.reflection_agent import create_reflection_graph
from Agent.models import *
from langchain_core.messages import AIMessage, HumanMessage
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

        self._chat_model: Agent[None, ChatbotCodeOutput]
        self._judge_model: Agent[None, JudgeOutput]
        self._deps = AgentDeps(api_key=self._API_KEY, http_client=AsyncClient)
        self._chat_settings = {"temperature": 1}
        self._judge_settings = {"temperature": 0.3}
        self._summarizer_settings = {"temperature": 0.4}

    async def should_run(
        self, state: Dict[str, Any]
    ) -> Literal["summarize", "call_model"]:
        return "summarize" if len(state["messages"]) > 10 else "call_model"

    async def summarize(self, state: Dict[str, Any]) -> Dict[str, Any]:
        self._chat_model = Agent(
            model="groq:gemma2-9b-it",
            system_prompt=SUMMARIZER_PROMPT,
            model_settings=self._summarizer_settings,
            deps_type=AgentDeps,
        )
        # Making chat history into strings
        chat_history = ""
        for m in state["messages"]:
            if type(m) == HumanMessage:
                chat_history += "User: " + m.text() + "\n"
            elif type(m) == AIMessage:
                chat_history += "Assistant: " + m.text() + "\n"
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
                if type(m) == HumanMessage:
                    chat_history += "User: " + m.text() + "\n"
                elif type(m) == AIMessage:
                    chat_history += "Assistant: " + m.text() + "\n"
        
        
        FINAL_SYSTEM_PROMPT = (
            SYSTEM_PROMPT[self._level]
            + "\n\nProblem:\n"
            + self._problem
            + self._summary
            if self._summary == ""
            else chat_history
        )
        
        
        self._chat_model = Agent(
            model="groq:qwen-qwq-32b",
            system_prompt=FINAL_SYSTEM_PROMPT,
            model_settings=self._chat_settings,
            deps_type=AgentDeps,
            output_type=ChatbotCodeOutput,
        )


        result = await self._chat_model.run(
            state["messages"][-1].content, deps=self._deps
        )
        
        
        if type(result.output) == ChatbotCodeOutput:
            state["messages"].append(
                {
                    "role": "assistant",
                    "content": result.output.extracted_code
                    + "\n\n\n"
                    + result.output.code_explanation,
                }
            )
            
            
        elif type(result.output) == str:
            state["messages"].append({"role": "assistant", "content": result.output})


        if type(result.output) == ChatbotCodeOutput:
            state["extract_code"] = ExtractCode(
                code=(
                    result.output.extracted_code
                    + "\n\n\n"
                    + result.output.validation_code
                ),
                language=result.output.extracted_code_language,
            )

        return state

    async def try_running(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if state["extract_code"]:
            
            resp = requests.post(
                self._EXECUTE_URL,
                json={
                    "code": state["extract_code"]["code"],
                    "language": state["extract_code"]["language"],
                },
            )
            
            result = resp.json()
            print(result)
            
            
            if resp.status_code == 200:
                output = result.get("output")
            else:
                output = result
                
            
            self._judge_model = Agent(
                model="groq:gemma2-9b-it",
                system_prompt=JUDGE_SYSTEM_PROMPT,
                output_type=JudgeOutput,
                model_settings=self._judge_settings,
                deps_type=AgentDeps,
            )
            judge_result = await self._judge_model.run(
                user_prompt="Code:\n"
                + state["extract_code"]["code"]
                + "\nOutput"
                + (output or "Error"),
                deps=self._deps,
            )
            print(judge_result.output)
            if not judge_result.output["passed"]:
                state["messages"].append(
                    {
                        "role": "user",
                        "content": f"This solution code is incorrect, as i get the incorrect output: "
                        + output
                        + "\nHere's my advice on correcting it: \n"
                        + judge_result.output["advice"],
                    }
                )
            state["extract_code"] = None

        return state

    async def create_reflection(self):
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

    async def create_agent(self):
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

    async def chat(self, message: str | None = None) -> Dict[str, str]:
        result = None
        if message:
            self._messages.append({"role": "user", "content": message})
        if self._level == 2:
            graph = await self.create_reflection()
            state = State(messages=self._messages, extract_code=None)
            result = await graph.ainvoke(state)
            return {
                "response": result["messages"][-2].content,
                "summary": self._summary,
            }
        else:
            graph = await self.create_agent()
            state = {
                "messages": self._messages,
            }
            result = await graph.ainvoke(state)
            return {
                "response": result["messages"][-1].content,
                "summary": self._summary,
            }
