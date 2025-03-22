from typing import TypedDict
from fastapi import Body
from pydantic import BaseModel, Field
from datetime import datetime


class ProblemStatementUrl(BaseModel):
    query: str = Field(
        description="should be a url of the format https:/leetcode.com/problems/problem_name/description"
    )

class ExtractPythonCode(TypedDict):
    """Type class for extracting Python code. The python_code field is the code to be extracted."""
    python_code: str

class NoCode(TypedDict):
    """Type class for indicating no code was found."""
    no_code: bool
    
class ArgsSchema(BaseModel):
    current_timestamp: datetime = Field(
        ..., description="The timestamp of the current user message in ISO 8601 format."
    )