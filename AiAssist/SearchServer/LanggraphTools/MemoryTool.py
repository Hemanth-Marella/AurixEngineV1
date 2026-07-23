from ..MongoDb import MongoDB
from langchain_core.tools import tool

@tool
async def memory_tool(file_hash: str) -> list | str:
    """
    Retrieves the chat history for a given PDF using its file hash.
    """

    mongodb = MongoDB()

    document = await mongodb.Chat_History.find_one(
        {"file_hash": file_hash}
    )

    if document:
        print(document["messages"])
        return document["messages"]

    return "MongoDB does not have chat history for this PDF."