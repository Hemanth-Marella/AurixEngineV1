from langchain_core.tools import tool
from ..MongoDb.FileMetadataConnection import MongoDB

@tool
async def sub_topic_tool(file_hash:str) -> str:

    """
    Use this tool whenever User ask a query or question about sub topics from the uploaded pdf.
    The input should be the user's question , about the sub topics of pdf , and
    the output is generated sub topics from mongo db

    """

    mongodb = MongoDB()
    document = await mongodb.Aurix_collection.find_one(
        {"file_hash":file_hash}
    )

    if document:
        print(document['sub_topics'])
        return document['sub_topics']
    
    return "sub topics not there in this pdf"