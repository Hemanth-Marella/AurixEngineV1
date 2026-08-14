from ..SearchServer.QuizTools.quiz_state import QuizState
from fastapi import APIRouter
from ..SearchServer.MongoDb import MongoDB

router = APIRouter(prefix="/generate_questions",tags=["GENERATE_QUESTIONS"])

@router.get("/quiz/questions")
async def quiz_questions(state:QuizState):

    mongodb = MongoDB()

    document = await mongodb.question_generator.find_one({"file_hash":state['file_hash']})


    if document:
        result = state["generate_questions"]
    return result