from typing import Annotated
from fastapi import Body
from pydantic import BaseModel, Field


class ProblemStatementUrl(BaseModel):
    query: str = Field(
        description="should be a url of the format https:/leetcode.com/problems/problem_name/description"
    )
