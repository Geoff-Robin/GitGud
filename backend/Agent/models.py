from typing import TypedDict,Annotated
from pydantic.v1 import BaseModel, Field
from datetime import datetime
from langgraph.graph.message import MessagesState
from typing import Annotated
from langgraph.graph.message import add_messages


class ExtractCode(TypedDict):
    """Type class for extracting Python code. The python_code field is the code to be extracted."""
    code: str
    language: str | None

class NoCode(TypedDict):
    """Type class for indicating no code was found."""
    no_code: bool
    

class State(TypedDict):
    messages: Annotated[list,add_messages]
    summary: str = Field(..., description="The summary of the conversation.")
    problem: str = Field(..., description="The leetcode problem for the conversation.")
    level : int = Field(..., description="The level of the conversation.")
