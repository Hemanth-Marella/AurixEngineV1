from langchain_core.tools import tool
from ..MongoDb.FileMetadataConnection import MongoDB
from langgraph.types import interrupt
import time

@tool
async def chapter_name_tool(file_hash: str,query:str) -> str:

    """
    Use this tool when ever user ask a chapter name of the uploaded pdf.
    The input should be the user's question , about the chapter name , and
    the output is generated chapter name from mongo db
    """

    start_time = time.perf_counter()

    mongodb = MongoDB()

    document = await mongodb.Aurix_collection.find_one(
        {"file_hash": file_hash}
    )

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    if document:

        return document["chapter_name"]

    return "Chapter not found."














## WITH INTERRUPT TOOL

# from langchain_core.tools import tool
# from ..MongoDb.FileMetadataConnection import MongoDB
# from langgraph.types import interrupt
# import time

# @tool
# async def chapter_name_tool(file_hash: str,query:str) -> str:

#     """
#     Use this tool when ever user ask a chapter name of the uploaded pdf.
#     The input should be the user's question , about the chapter name , and
#     the output is generated chapter name from mongo db
#     """

#     print("before interrupt")
#     chapter_name = interrupt({
#         "type": "chapter_name",
#         "message": "Which chapter do you want?"
#     })
    
#     print("after interrupt")
#     start_time = time.perf_counter()

#     mongodb = MongoDB()

#     document = await mongodb.Aurix_collection.find_one(
#         {"file_hash": file_hash}
#     )

#     end_time = time.perf_counter()
#     execution_time = end_time - start_time

#     if document:
#         mongodb_chapter =  document["chapter_name"]

#         if chapter_name.lower() == mongodb_chapter.lower():
#             print("chapter name is found")
#             return mongodb_chapter

#     return "Chapter not found."