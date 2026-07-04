from langchain_core.tools import tool
from ..Services import generation_service

@tool
def generation_tool(query: str) -> str:
    """
    Answer questions using the indexed PDF documents.

    Use this tool whenever a user asks a question that requires information
    from the uploaded PDF content. The input should be the user's question,
    and the output is the generated answer based on the relevant document
    context.
    """
    service = generation_service.GenerationService(query)
    return service.generate_answer()