from langchain_core.tools import tool
from ..Services import generation_service

@tool
async def generation_tool(query: str,file_hash:str) -> str:

    
    """
    Answer questions using the indexed PDF documents.

    Use this tool whenever a user asks a question that requires information
    from the uploaded PDF content. The input should be the user's question,
    and the output is the generated answer based on the relevant document
    context.
    """

    print("janu")
    service = generation_service.GenerationService(query)

    result = await service.generate_answer()
    
    return result