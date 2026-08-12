from ..SearchServer.QuizTools.quiz_state import QuizState
from fastapi import APIRouter

router = APIRouter(prefix="/generate_questions",tags=["GENERATE_QUESTIONS"])

@router.get("/quiz/questions")
async def quiz_questions(state:QuizState):

    result = state["generate_questions"]

    return result