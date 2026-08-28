from langgraph.types import Command
from fastapi import APIRouter
from pydantic import BaseModel
from ..SearchServer.Agent.QuizGraph import quiz_graph

router = APIRouter(prefix="/quiz",tags=["QUIZANSWER"])

class QuizAnswerRequest(BaseModel):
    thread_id:str
    answer : str

@router.post("/answer")
async def quiz_answer(request: QuizAnswerRequest):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = await quiz_graph.ainvoke(
        Command(resume=request.answer),
        config=config
    )

    return result