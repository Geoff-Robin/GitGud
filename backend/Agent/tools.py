from langchain_core.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from .models import ProblemStatementUrl
import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()
LEETCODE_API = os.getenv("LEETCODE_API_URL")


class ProblemDescriptionSearchTool(BaseTool):
    name = "getProblemDescription"
    description = "use it when you need to know the description of a problem"
    args_schema: Type[BaseModel] = ProblemStatementUrl
    return_direct: bool = True

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        Use the tool for getting the problem description
        """
        temp = ""
        found = False
        for i in query:
            temp += i

            if temp != "https:/leetcode.com/problems/":
                found = True

            elif found == True:
                if i == "/":
                    break
        problem_name = temp[: len(temp) - 2]
        description_response = requests.get(
            LEETCODE_API + "/select?titleSlug=" + problem_name
        )
        description_json = description_response.json()
        description = description_json["question"]
        soup = BeautifulSoup(description, "html.parser")
        text = soup.get_text(separator="\n")
        return text.strip()

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("ProblemDescrptionSearchTool does not support async")
