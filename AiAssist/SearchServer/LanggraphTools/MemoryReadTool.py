from ..MongoDb import MongoDB
from langchain_core.tools import tool

@tool
async def memory_read_tool(file_hash:str):

    """
    This tool is to get only memory data for the purpose of read the data
    """

    mongodb = MongoDB()

    chat_history =await mongodb.Chat_History.find_one(
        {'file_hash':file_hash}
    )
    messages = chat_history['messages']

    return messages