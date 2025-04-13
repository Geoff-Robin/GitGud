from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class AuthResModel(BaseModel):
    ACCESS_TOKEN : str
    REFRESH_TOKEN : str 
    
class RegisterReqModel(BaseModel):
    username :str
    email :str
    password:str
    model_config = {
        "json_schema_extra":{
            "examples" : [
                {
                    "username": "John Doe",
                    "email": "johndoe@example.com",
                    "password": "password123"
                }
            ]
        }
    }
    
    
class LoginReqModel(BaseModel):
    email :str
    password:str
    model_config = {
        "json_schema_extra":{
            "examples" : [
                {
                    "email": "johndoe@example.com",
                    "password": "password123"
                }
            ]
        }
    }
    
class CreateChatReqModel(BaseModel):
    problem_url : str
    problem_nickname : Optional[str] = None
    model_config = {
        "json_schema_extra":{
            "examples" : [
                {
                    "problem_url": "https://example.com/problem1",
                    "problem_nickname": "Problem 1"
                },
            ]
        }
    }
    
class ChatRoom(BaseModel):
    problem: str
    email: str
    model_config={
        "json_schema_extra":{
            "examples" : [
                    {
                        "problem": "https://example.com/problem1",
                        "email": "johndoe@example.com",
                    },
                ]
            }
        }
    
class ChatMessage(BaseModel):
    message: str
    email: str
    problem: str
    model_config={
        "json_schema_extra":{
            "examples" : [
                    {
                        "message": "Hello, how are you?",
                        "email": "johndoe@example.com",
                        "problem": "https://example.com/problem1",
                    },
                ]
            }
        }
    
    
