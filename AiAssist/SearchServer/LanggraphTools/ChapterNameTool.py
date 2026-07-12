from langchain_core.tools import tool
from ..MongoDb.FileMetadataConnection import MongoDB

@tool
async def chapter_name_tool(file_hash: str,query:str) -> str:

    """
    Use this tool when ever user ask a chapter name of the uploaded pdf.
    The input should be the user's question , about the chapter name , and
    the output is generated chapter name from mongo db
    """
    print("chapter name tool")
    mongodb = MongoDB()
    # print("file hash is :",file_hash)
    document = await mongodb.Aurix_collection.find_one(
        {"file_hash": file_hash}
    )

    if document:
        # print(document["chapter_name"])
        return document["chapter_name"]


    return "Chapter not found."