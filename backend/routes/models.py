from pydantic import BaseModel

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