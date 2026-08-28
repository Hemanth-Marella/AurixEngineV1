from langchain.tools import tool
from ..MongoDb import MongoDB
import json

@tool
async def get_answer_tool(file_hash: str, query: str):

    """
    Get the user's answer for the current quiz question.
    """

    if query:
        return query