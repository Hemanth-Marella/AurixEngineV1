from ..DataIngestion.adding_vectors_db import AddingVectorsToDb
from langchain_core.tools import tool
from ..Services import summary_service


@tool 
async def summary_tool(chapter_name:str,file_hash:str) -> str:

    """
    Use this tool ONLY when the user explicitly asks for:
    - a summary
    - a chapter summary
    - a brief overview
    - a short explanation of the entire chapter
    - key points of the chapter

    Do NOT use this tool for:
    - answering specific questions
    - explaining individual subtopics
    - listing subtopics
    - generating quizzes
    - chapter name requests
    
    """

    service = summary_service.SummaryService(chapter_name,file_hash)
    result = await service.summary_answer()
    return result