"""
This module defines the Pydantic models used for request and response validation in the API.

It includes models for user authentication, chat creation, and chat messages.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuthResModel(BaseModel):
    """
    Model for authentication response containing access and refresh tokens.
    """
    ACCESS_TOKEN : str
    REFRESH_TOKEN : str 
    
class RegisterReqModel(BaseModel):
    """
    Model for user registration request containing username, email, and password.
    """
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
    """
    Model for user login request containing email and password.
    """
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
    """
    Model for creating a chat request containing problem URL and optional problem nickname.
    """
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
    """
    Model for a chat room containing problem URL and user email.
    """
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
    """
    Model for a chat message containing the message content, user email, and problem URL.
    """
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


