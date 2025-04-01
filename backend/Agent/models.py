from typing import TypedDict,Literal
from fastapi import Body
from pydantic.v1 import BaseModel, Field
from datetime import datetime
from langgraph.prebuilt import Agent

class ProblemStatementUrl(BaseModel):
    query: str = Field(
        description="should be a url of the format https:/leetcode.com/problems/problem_name/description"
    )

class ExtractCode(TypedDict):
    """Type class for extracting Python code. The python_code field is the code to be extracted."""
    code: str
    language: str | None

class NoCode(TypedDict):
    """Type class for indicating no code was found."""
    no_code: bool
    
class ArgsSchema(BaseModel):
    current_timestamp: datetime = Field(
        ..., description="The timestamp of the current user message in ISO 8601 format."
    )

class TimeStampDifferenceInput(BaseModel):
    first_timestamp: str = Field(..., description="The first timestamp in ISO 8601 format.")
    second_timestamp: str = Field(..., description="The second timestamp in ISO 8601 format.")
