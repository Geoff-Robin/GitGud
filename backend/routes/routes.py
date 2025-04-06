from fastapi import APIRouter, Response, status, Request, Depends
from routes.models import (
    AuthResModel,
    RegisterReqModel,
    LoginReqModel,
    CreateChatReqModel,
    ChatRoom,
    ChatMessage,
)
from pymongo import DESCENDING,ASCENDING
from auth_utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    get_current_user,
    get_current_user_refresh,
)
import datetime as dt
from datetime import datetime, timezone
from Agent.agent import ChatBot
from routes.utils import scraper
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


@router.get("/refresh", summary="Refresh JWT tokens")
async def refresh_token(response: Response, user=Depends(get_current_user_refresh)):
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


@router.post("/create_chat", summary="Create a new chat room for a leetcode problem")
async def create_chat(
    chat: CreateChatReqModel,
    request: Request,
    response: Response,
    user=Depends(get_current_user),
):
    try:
        problem_url = chat.problem_url
        problem_nickname = chat.problem_nickname
        problem_statement = scraper(problem_url)
        if not problem_statement:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Invalid problem URL"}
        if problem_nickname:
            request.app.database["Chat List"].insert_one(
                {
                    "problem": problem_nickname,
                    "email": user["email"],
                    "problem_statement": problem_statement,
                    "summary": "",
                }
            )
        else:
            request.app.database["Chat List"].insert_one(
                {
                    "problem": problem_url,
                    "email": user["email"],
                    "problem_statement": problem_statement,
                    "summary": "",
                }
            )
        return {"message": "Chat created successfully"}
    except Exception as e:
        logger.error(f"Error creating chat: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get_chat", summary="Get chat history for a leetcode problem")
async def get_chat(
    chat: ChatRoom, request: Request, response: Response, user=Depends(get_current_user)
):
    try:
        chat_history = await request.app.database["Chat List"].find_one(
            {
                "problem": chat.problem,
                "email": user["email"],
            }
        )
        if not chat_history:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "Chat not found"}
        return chat_history
    except Exception as e:
        logger.error(f"Error retrieving chat: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat_message", summary="Send a message in a chat room")
async def chat_message(
    chat_message: ChatMessage,
    request: Request,
    response: Response,
    user=Depends(get_current_user),
):
    try:
        # Insert user's message into DB with timestamp
        await request.app.database["Messages"].insert_one(
            {
                "problem": chat_message.problem,
                "email": user["email"],
                "role": "user",
                "message": chat_message.message,
                "timestamp": dt.datetime.now(timezone.utc),
            }
        )

        # Fetch chat metadata
        chat = await request.app.database["Chat List"].find_one(
            {
                "problem": chat_message.problem,
                "email": user["email"],
            }
        )
        if not chat:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "Chat not found"}

        # Fetch all chat history sorted by timestamp DESCENDING
        chat_history = await request.app.database["Messages"].find(
            {
                "problem": chat_message.problem,
                "email": user["email"],
            }
        ).sort("timestamp", DESCENDING).to_list(length=None)

        if not chat_history:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "Chat History not found"}

        # 🕒 Get time difference in minutes from earliest message
        earliest_message = await request.app.database["Messages"].find_one(
            {
                "problem": chat_message.problem,
                "email": user["email"],
            },
            sort=[("timestamp", ASCENDING)]
        )

        time_difference_minutes = None
        if earliest_message and "timestamp" in earliest_message:
            earliest_time = earliest_message["timestamp"]
            if earliest_time.tzinfo is None:
                earliest_time = earliest_time.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            diff = now - earliest_time
            time_difference_minutes = diff.total_seconds() / 60
            print(f"⏳ Time since first message: {time_difference_minutes:.2f} minutes")

        # Format history for ChatBot
        formatted_history = [
            {"role": m["role"], "content": m["message"]}
            for m in chat_history if m["role"] != "system"
        ]

        summary = chat.get("summary", "")
        problem = chat.get("problem_statement", "")

        chatbot = ChatBot(messages=formatted_history, summary=summary, problem=problem)
        result = chatbot.chat()

        # Update summary
        await request.app.database["Chat List"].update_one(
            {"problem": chat_message.problem, "email": user["email"]},
            {"$set": {"summary": result["summary"]}},
        )

        # Insert bot response
        await request.app.database["Messages"].insert_one(
            {
                "problem": chat_message.problem,
                "email": user["email"],
                "role": "assistant",
                "message": result["response"],
                "timestamp": dt.datetime.now(timezone.utc),
            }
        )

        return {
            "message": result["response"],
            "minutes_since_first_message": time_difference_minutes
        }

    except Exception as e:
        logger.error(f"Error sending message: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(e))