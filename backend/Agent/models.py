from typing import TypedDict, Annotated, Any
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from langgraph.graph.message import add_messages


class ExtractCode(TypedDict):
    """Type class for extracting Python code."""

    code: str = Field(..., description="Enter code if there is any code in the message")
    language: str | None = Field(
        ..., description="Enter the programming language of the code"
    )


class NoCode(TypedDict):
    """Type class for indicating no code was found."""

    no_code: bool


class JudgeOutput(TypedDict):
    """Type class for judge output."""

    passed: bool = Field(
        ...,
        description="'True' if solution code passes all test cases and 'False' if it doesn't",
    )
    advice: str =Field(
        ...,
        description="Give advice on correcting the solution"
    )


class State(TypedDict):
    """State class containing messages and extracted code."""

    messages: Annotated[
        list, add_messages
    ]  
    extract_code: ExtractCode | None = None


class ChatMessage(BaseModel):
    """Model for a chat message."""

    message: str

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "message": "Hello, how are you?",
                },
            ]
        }


class ChatbotCodeOutput(BaseModel):
    """Output model for the chatbot."""

    extracted_code_language: str = Field(
        ...,
        description="The programming language used for the solution (e.g., 'Python', 'Java').",
    )
    extracted_code: str = Field(
        ...,
        description="Only the clean solution code (e.g., the Solution class or main function) without any test cases.",
    )
    validation_code: str = Field(
        ...,
        description="Validation Code should print/give an output ''True'' if it passes all test cases",
        examples=["""python code:
    print(longest_palindrome("babad")=="bab")  # Output: "bab"
    print(longest_palindrome("cbbd")=="cbbd")"""],
    )
    code_explanation: str = Field(
        ...,
        description="A detailed explanation of the logic, approach, and time/space complexity of the extracted solution.",
    )

@dataclass
class AgentDeps:
    """Dependencies for the agent."""

    api_key: str
    http_client: Any

    class Config:
        arbitrary_types_allowed = True
