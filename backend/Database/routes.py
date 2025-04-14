from fastapi import APIRouter, Response, status, Request, Depends
import logging
from Database.models import *
from Auth import *
from utils import scraper

db_router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@db_router.post("/create_chat", summary="Create a new chat room for a leetcode problem")
async def create_chat(
    chat: CreateChatReqModel,
    request: Request,
    response: Response,
    user=Depends(get_current_user),
):
    """
    Create a new chat room for a given LeetCode problem.

    Args:
        chat (CreateChatReqModel): The chat creation data.
        request (Request): The HTTP request object.
        response (Response): The HTTP response object.
        user: The current user obtained from the access token.

    Returns:
        dict: A message indicating the success of the chat creation.
    """
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


@db_router.post("/get_chat", summary="Get chat history for a leetcode problem")
async def get_chat(
    chat: ChatRoom, request: Request, response: Response, user=Depends(get_current_user)
):
    """
    Retrieve the chat history for a given LeetCode problem.

    Args:
        chat (ChatRoom): The chat room data.
        request (Request): The HTTP request object.
        response (Response): The HTTP response object.
        user: The current user obtained from the access token.

    Returns:
        dict: The chat history for the specified problem.
    """
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
