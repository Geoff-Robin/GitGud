import os
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from langchain.tools import tool
from dotenv import load_dotenv
from datetime import datetime
from Agent.models import ProblemStatementUrl, TimeStampDifferenceInput


load_dotenv()
LEETCODE_API = os.getenv("LEETCODE_API_URL")



@tool("get_problem_description", args_schema=ProblemStatementUrl)
def get_problem_description(url: str) -> str:
    """
    Retrieve the description of a LeetCode problem given its URL.

    Args:
        url (str): The URL of the LeetCode problem statement.

    Returns:
        str: The plain text description of the problem.
    """
    # Extract the problem slug from the URL
    prefix = "https://leetcode.com/problems/"
    if not url.startswith(prefix):
        raise ValueError("Invalid LeetCode problem URL.")
    problem_slug = url[len(prefix) :].split("/")[0]

    # Fetch the problem description from the LeetCode API
    response = requests.get(f"{LEETCODE_API}/select?titleSlug={problem_slug}")
    response.raise_for_status()
    description_html = response.json().get("question", "")

    # Parse the HTML description to plain text
    soup = BeautifulSoup(description_html, "html.parser")
    description_text = soup.get_text(separator="\n").strip()
    return description_text


# Define input schema for the timestamp difference tool


@tool("get_message_timestamp_difference", args_schema=TimeStampDifferenceInput)
def get_message_timestamp_difference(
    first_timestamp: str, second_timestamp: str
) -> str:
    """
    Calculate the difference between two message timestamps.

    Args:
        first_timestamp (str): The first timestamp in ISO 8601 format.
        second_timestamp (str): The second timestamp in ISO 8601 format.

    Returns:
        str: The difference between the two timestamps.
    """
    fmt = "%Y-%m-%dT%H:%M:%S"
