from langchain_core.tools import tool
from ..MongoDb.FileMetadataConnection import MongoDB

@tool
async def chapter_name_tool(file_hash: str) -> str:
    """
    Returns the chapter name for the given file hash.
    """
    mongodb = MongoDB()

    document = await mongodb.Aurix_collection.find_one(
        {"file_hash": file_hash}
    )

    if document:
        return document["chapter_name"]

    return "Chapter not found."