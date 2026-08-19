from ..MongoDb import MongoDB
from langchain_core.tools import tool
from ..Services.chatHistoryService import ChatHistoryService

@tool
async def memory_tool(file_hash: str,query:str,result) -> list | str:
    """
    Retrieves the chat history for a given PDF using its file hash.
    """

    chat_history_service = ChatHistoryService(file_hash,query,result)

    # update chat history
    update_current_message = chat_history_service.chat_history()
    if update_current_message:

        return result