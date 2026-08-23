from fastapi import APIRouter
from ..SearchServer.QuizNodes.AskQuestionNode import ask_question_node

router = APIRouter(prefix="/one_question",tags=["ONE_QUESTION"])

@router.get("single/quiz")
async def single_question():
    return