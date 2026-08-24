from fastapi import APIRouter
from ..SearchServer.QuizNodes.AskQuestionNode import ask_question_node
from ..SearchServer.QuizTools.quiz_state import QuizState

router = APIRouter(prefix="/one_question",tags=["ONE_QUESTION"])

@router.get("single/quiz")
async def single_question(state:QuizState):

    quiz_question = await ask_question_node(state)

    return quiz_question