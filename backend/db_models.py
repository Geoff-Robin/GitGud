from typing import Optional
from fastapi import Body
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Optional[str] = Field(default=None, description="MongoDB document ObjectID", alias="_id")
    username: str
    email: str
    password: str