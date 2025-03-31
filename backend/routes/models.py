from pydantic import BaseModel
from typing import Optional

class AuthResModel(BaseModel):
    ACCESS_TOKEN : str
    REFRESH_TOKEN : str 
    
class RegisterReqModel(BaseModel):
    username :str
    email :str
    password:str
    
class LoginReqModel(BaseModel):
    email :str
    password:str
    
class CreateChatReqModel(BaseModel):
    problem_url : str
    problem_nickname : Optional[str] = None