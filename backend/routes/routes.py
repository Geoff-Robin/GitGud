from fastapi import APIRouter
from db_models import User
from routes.models import AuthResModel, RegisterReqModel,LoginReqModel
from auth_utils import get_hashed_password,create_access_token,create_refresh_token
router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResModel,
    summary="registering user and return JWT tokens",
)
async def register(user: RegisterReqModel):
    user = User(
        username=user.username,
        email=user.email,
        password=get_hashed_password(user.password),
    )
    Users = app.database["Users"]
    try:
        user = await Users.insert_one(user)
    except Exception as e:
        print(e)
    return AuthResModel(REFRESH_TOKEN=create_refresh_token(user.email),ACCESS_TOKEN=create_access_token(user.email))

@router.post("/login",
             response_model=AuthResModel,
             summary="logging user in and return JWT Tokens")

async def login(login_data: LoginReqModel):
    Users = app.database["Users"]
    try:
        user = await Users.find_one({"email":login_data.email})
    except Exception as e:
        return {
            "error":e
        }
    if user.password = get_hashed_password(login_data.)
    return AuthResModel(REFRESH_TOKEN=create_refresh_token(user.email),ACCESS_TOKEN=create_access_token)

