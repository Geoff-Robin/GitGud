from langchain_groq import ChatGroq
from langgraph.graph import Graph
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph_reflection import create_reflection_graph
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchResults
import requests
from Agent.models import ExtractPythonCode, NoCode
from Agent.tools import get_problem_description
from dotenv import load_dotenv
import os

SYSTEM_PROMPT=[]


def try_running(state: dict) -> dict | None:
    """Attempt to run and analyze the extracted Python code using the code_runner api.

    Args:
        state: The current conversation state

    Returns:
        dict | None: Updated state with compiler or interpreter results from code_runner api.
    """
    load_dotenv()
    LLM_API_KEY = os.getenv("GROQ_API_KEY")
    model = ChatGroq(model="qwen-2.5-coder-32b", temperature=1, api_key=LLM_API_KEY)
    extraction = model.bind_tools([ExtractPythonCode, NoCode])
    er = extraction.invoke(
        [{"role": "system", "content": SYSTEM_PROMPT}] + state["messages"]
    )
    if len(er.tool_calls) == 0:
        return None
    tc = er.tool_calls[0]
    if tc["name"] != "ExtractPythonCode":
        return None
    api_url = "http://localhost:3000/execute"
    response = requests.post(api_url, json={"language": "python", "code": tc["args"]["python_code"]})
    result = response.json()

    if not result["output"]:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": f"The code execution resulted in an error: {result}\n\n"
                    "Please try to fix it. Ensure you provide the entire code snippet. "
                    "If you're unsure what's wrong, or think there's a mistake, "
                    "you can ask me a question rather than generating code.",
                }
            ]
        }
    return None

def create_graph() -> Graph | None:
    load_dotenv()
    LLM_API_KEY = os.getenv("GROQ_API_KEY")
    model = ChatGroq(model="qwen-2.5-coder-32b", temperature=1, api_key=LLM_API_KEY)
    duckduckgo = DuckDuckGoSearchResults(max_results=10)
    coder_graph = create_react_agent(model,tools=[duckduckgo])
    judge_graph = (
        StateGraph(MessagesState)
        .add_node(try_running)
        .add_edge(START, "try_running")
        .add_edge("try_running", END)
        .compile()
    )
    return create_reflection_graph(judge_graph, coder_graph).compile()
    