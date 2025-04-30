from typing import TypedDict,Annotated
from pydantic import BaseModel, Field
from datetime import datetime
from langgraph.graph.message import MessagesState
from typing import Annotated
from langgraph.graph.message import add_messages


class ExtractCode(TypedDict):
    """Type class for extracting Python code. The python_code field is the code to be extracted."""
    code: str = Field(...,description="Enter code if there is any code in the message")
    language: str  | None = Field(...,description="Enter the programming language of the code")

class NoCode(TypedDict):
    """Type class for indicating no code was found."""
    no_code: bool
    

class State(TypedDict):
    messages: Annotated[list,add_messages]
    summary: str = Field(..., description="The summary of the conversation.")
    problem: str = Field(..., description="The leetcode problem for the conversation.")
    level : int = Field(..., description="The level of the conversation.")
    
class ChatMessage(BaseModel):
    """
    Model for a chat message containing the message content, user email, and problem URL.
    """
    message: str
    model_config={
        "json_schema_extra":{
            "examples" : [
                    {
                        "message": "Hello, how are you?",
                    },
                ]
            }
        }
