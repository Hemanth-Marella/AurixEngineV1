from langchain.tools import tool
from ..MongoDb import MongoDB
import json

@tool
async def get_answer_tool(file_hash: str, current_answer: str):

    if current_answer:
        return current_answer