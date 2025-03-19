from fastapi import APIRouter, Response, status, Request
from db_models import User
from routes.models import AuthResModel, RegisterReqModel, LoginReqModel
from auth_utils import get_hashed_password, create_access_token, create_refresh_token, verify_password
import logging
from starlette.exceptions import HTTPException

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post(
    "/register",
    summary="Register user and return JWT tokens",
)
async def register(user: RegisterReqModel, response: Response, request: Request):
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


@router.post(
    "/login",
    summary="Login user and return JWT Tokens",
)
async def login(login_data: LoginReqModel, response: Response, request: Request):
    try:
        Users = request.app.database["Users"]
        user = await Users.find_one({"email": login_data.email})
        if not user:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "User does not exist or could not be found"}

        if not verify_password(user["password"],login_data.password):
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
