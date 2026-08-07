from .quiz_state import QuizState
from langchain.tools import tool

@tool
async def ask_question_tool(state:QuizState):
    return