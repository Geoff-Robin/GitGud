import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import Union, Any, Annotated
from jose import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import datetime
from jwt.exceptions import InvalidTokenError

load_dotenv()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    email: str | None = None


async def get_user(db, email: str):
    user = await db.Users.find_one({"email": email})
    return user


async def create_access_token(
    subject: Union[str, Any], expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expires_delta = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def create_refresh_token(
    subject: Union[str, Any], expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expires_delta = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


async def get_current_user_refresh(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        body = await request.json()
        token = body.get("refresh_token")
        if not token:
            raise credentials_exception
        
        payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)
    except (InvalidTokenError, ValueError):
        raise credentials_exception
    
    user = await get_user(request.app.database, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], request: Request
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        print("decoded payload", payload)
        email = payload.get("sub")
        print("email: ", email)
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(request.app.database, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user