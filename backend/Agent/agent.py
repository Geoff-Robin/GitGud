"""
This module defines the ChatBot class, which handles the logic for the competitive programming assistant.

It includes methods for summarizing conversations, interacting with models, and executing code.
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Literal, TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph_reflection import create_reflection_graph
from langchain_community.tools import DuckDuckGoSearchResults
from Agent.models import NoCode, ExtractCode, State
from Agent.prompts import SYSTEM_PROMPT, JUDGE_SYSTEM_PROMPT,SUMMARIZER_PROMPT


class ChatBot:
    """
    A chatbot for assisting with competitive programming problems.

    Attributes:
        messages (List[Dict[str, str]]): The conversation history.
        problem (str): The problem description.
        summary (str): A summary of the conversation.
        level (int): The assistance level (0, 1, or 2).
    """
    def __init__(self, messages: List[Dict[str, str]], problem: str, summary: str = "",level: int = 0):
        load_dotenv()
        self._messages = messages
        self._problem = problem.strip()
        self._summary = summary
        self._level = level
        self._API_KEY = os.getenv("GROQ_API_KEY")
        self._EXECUTE_URL = os.getenv("CODE_RUNNER_API_URL")
        print(level)
        assert self._API_KEY, "Missing GROQ_API_KEY in .env"
        assert self._EXECUTE_URL, "Missing CODE_RUNNER_API_URL in .env"

        self._cold_model = ChatGroq(
            model="qwen-qwq-32b", temperature=0.3, api_key=self._API_KEY
        )
        self._hot_model = ChatGroq(
            model="qwen-qwq-32b", temperature=0.5, api_key=self._API_KEY
        )
        self._summarizer = ChatGroq(
            model="qwen-qwq-32b", temperature=0.5, api_key=self._API_KEY
        )
        self._search_tool = DuckDuckGoSearchResults(max_results=5)

    def should_run(self, state: Dict[str, Any]) -> Literal["summarize", "call_model"]:
        return "summarize" if len(state["messages"]) > 5 else "call_model"

    def summarize(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = SUMMARIZER_PROMPT
        sys_msg = {"role": "system", "content": prompt}
        response = self._summarizer.invoke([sys_msg] + state["messages"])
        state["summary"] = response.content
        state["messages"] = state["messages"][-3:]
        return state

    def call_model(self, state: Dict[str, Any]) -> Dict[str, Any]:
        sys_msg = {
            "role": "system",
            "content": SYSTEM_PROMPT[self._level] + "\n\nProblem:\n" + self._problem+ "Summarized conversation given by Summary Bot: " + state["summary"]
        }
        msgs = [sys_msg] + state["messages"]
        model = self._hot_model.bind_tools([self._search_tool])
        ai_msg = model.invoke(msgs)
        state["messages"].append({"role": "assistant", "content": ai_msg.content})
        return state

    def try_running(self, state: Dict[str, Any]) -> Dict[str, Any]:
        judge_msg = {"role": "system", "content": JUDGE_SYSTEM_PROMPT}
        msgs = [judge_msg] + state["messages"]
        extractor = self._cold_model.bind_tools([ExtractCode, NoCode])
        er = extractor.invoke(msgs)
        if not getattr(er, "tool_calls", []):
            return state
        tc = er.tool_calls[0]
        if tc["name"] != "ExtractCode":
            return state
        code = tc["args"]["code"]
        resp = requests.post(
            self._EXECUTE_URL, json={"code": code, "language": tc["args"]["language"]}
        )
        result = resp.json()
        if result.get("output") == "False":
            state["messages"].append(
                {
                    "role": "user",
                    "content": f"Execution failed: {result.get('error','unknown')}. Try running the correct code.",
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
        judge_graph= (
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
        self._messages.append({
                "role" : "user",
                "content" : message
            })
        if self._level == 2:
            graph = self.create_reflection()
            state = {
                "messages": self._messages,
                "summary": self._summary,
            }
            result = graph.invoke(state)
            print(result)
            return {
                "response": result["messages"][-1].content,
                "summary": result["summary"],
            }
        else:
            graph = self.create_agent()
            graph = self.create_reflection()
            state = {
                "messages": self._messages,
                "summary": self._summary,
            }
            result = graph.invoke(state)
            print(result)
            return {
                "response": result["messages"][-1].content,
                "summary": result["summary"],
            }
