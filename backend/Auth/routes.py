from fastapi import APIRouter, Response, status, Request, Depends
from Auth.models import *
from Auth import *
from starlette.exceptions import HTTPException
from fastapi import APIRouter, Response, status, Request, Depends
from Auth.models import *
from Auth import *
from starlette.exceptions import HTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_router = APIRouter()

@auth_router.post(
    "/register",
    summary="Register user and return JWT tokens",
)
async def register(user: RegisterReqModel, response: Response, request: Request):
    """
    Register a new user and generate JWT tokens.

    Args:
        user (RegisterReqModel): The user registration data.
        response (Response): The HTTP response object.
        request (Request): The HTTP request object.

    Returns:
        AuthResModel: The access and refresh tokens for the user.
    """
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": await get_hashed_password(user.password),
    }
    Users = request.app.database["Users"]
    user_db = await Users.find_one({"email": user.email})
    if user_db:
        return {"message": "User already exists"}
    try:
        await Users.insert_one(user_data)
    except Exception as e:
        logger.error(f"Error inserting user: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Error inserting user"}

    return AuthResModel(
        REFRESH_TOKEN=await create_refresh_token(user.email),
        ACCESS_TOKEN=await create_access_token(user.email),
    )


@auth_router.post(
    "/login",
    summary="Login user and return JWT Tokens",
)
async def login(login_data: LoginReqModel, response: Response, request: Request):
    """
    Authenticate a user and generate JWT tokens.

    Args:
        login_data (LoginReqModel): The user login data.
        response (Response): The HTTP response object.
        request (Request): The HTTP request object.

    Returns:
        AuthResModel: The access and refresh tokens for the user.
    """
    try:
        Users = request.app.database["Users"]
        user = await Users.find_one({"email": login_data.email})
        if not user:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "User does not exist or could not be found"}

        if not verify_password(user["password"], login_data.password):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"error": "Invalid password"}

        return AuthResModel(
            REFRESH_TOKEN=await create_refresh_token(user["email"]),
            ACCESS_TOKEN=await create_access_token(user["email"]),
        )
    except Exception as e:
        logger.error(f"Error during login: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.get("/refresh", summary="Refresh JWT tokens")
async def refresh_token(response: Response, user=Depends(get_current_user_refresh)):
    """
    Refresh the JWT access token using a refresh token.

    Args:
        response (Response): The HTTP response object.
        user: The current user obtained from the refresh token.

    Returns:
        dict: The new access token.
    """
    try:
        user_email = user["email"]
        if not user_email:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"error": "Invalid refresh token"}
        return {
            "ACCESS_TOKEN": await create_access_token(user_email),
        }
    except Exception as e:
        logger.error(f"Error during token refresh: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(e))

auth_router = APIRouter()

@auth_router.post(
    "/register",
    summary="Register user and return JWT tokens",
)
async def register(user: RegisterReqModel, response: Response, request: Request):
    """
    Register a new user and generate JWT tokens.

    Args:
        user (RegisterReqModel): The user registration data.
        response (Response): The HTTP response object.
        request (Request): The HTTP request object.

    Returns:
        AuthResModel: The access and refresh tokens for the user.
    """
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": await get_hashed_password(user.password),
    }
    Users = request.app.database["Users"]
    user_db = await Users.find_one({"email": user.email})
    if user_db:
        return {"message": "User already exists"}
    try:
        await Users.insert_one(user_data)
    except Exception as e:
        logger.error(f"Error inserting user: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Error inserting user"}

    return AuthResModel(
        REFRESH_TOKEN=await create_refresh_token(user.email),
        ACCESS_TOKEN=await create_access_token(user.email),
    )


@auth_router.post(
    "/login",
    summary="Login user and return JWT Tokens",
)
async def login(login_data: LoginReqModel, response: Response, request: Request):
    """
    Authenticate a user and generate JWT tokens.

    Args:
        login_data (LoginReqModel): The user login data.
        response (Response): The HTTP response object.
        request (Request): The HTTP request object.

    Returns:
        AuthResModel: The access and refresh tokens for the user.
    """
    try:
        Users = request.app.database["Users"]
        user = await Users.find_one({"email": login_data.email})
        if not user:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "User does not exist or could not be found"}

        if not verify_password(user["password"], login_data.password):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"error": "Invalid password"}

        return AuthResModel(
            REFRESH_TOKEN=await create_refresh_token(user["email"]),
            ACCESS_TOKEN=await create_access_token(user["email"]),
        )
    except Exception as e:
        logger.error(f"Error during login: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.get("/refresh", summary="Refresh JWT tokens")
async def refresh_token(response: Response, user=Depends(get_current_user_refresh)):
    """
    Refresh the JWT access token using a refresh token.

    Args:
        response (Response): The HTTP response object.
        user: The current user obtained from the refresh token.

    Returns:
        dict: The new access token.
    """
    try:
        user_email = user["email"]
        if not user_email:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"error": "Invalid refresh token"}
        return {
            "ACCESS_TOKEN": await create_access_token(user_email),
        }
    except Exception as e:
        logger.error(f"Error during token refresh: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(e))