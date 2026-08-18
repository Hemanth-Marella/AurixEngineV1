from fastapi import APIRouter
from pydantic import BaseModel
from ..SearchServer.MongoDb import MongoDB
from ..SearchServer.QuizTools.QuestionGenerateTool import generate_questions_tool


class QuizResponse(BaseModel):
    file_hash:str

router = APIRouter(prefix="/generate_questions",tags=["GENERATE_QUESTIONS"])

@router.post("/quiz/questions")
async def quiz_questions(request: QuizResponse):

    print("enter into quiz Response")

    mongodb = MongoDB()

    document = await mongodb.question_generator.find_one(
        {"file_hash": request.file_hash}
    )

    print(document)

    if not document:
        return {
            "questions": []
        }

    return {
        "questions": document["questions"]
    }