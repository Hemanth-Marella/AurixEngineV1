from ..DataIngestion.adding_vectors_db import AddingVectorsToDb
from langchain_core.tools import tool



@tool 
async def summary_tool(file_hash:str,chapter_name:str,query:str) -> str:

    """
    
    """ 

    service = AddingVectorsToDb()