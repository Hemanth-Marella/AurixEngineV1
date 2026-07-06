from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..SearchServer.Services.generation_service import GenerationService

from pydantic import BaseModel

router = APIRouter(prefix="/user", tags=["USER"])

class QuestionRequest(BaseModel):
    query: str

@router.post("/question")
async def user_question(request: QuestionRequest):

    service = GenerationService(request.query).generate_answer()

    def generate():
        for chunk in service:
            yield chunk.text

    return StreamingResponse(generate(), media_type="text/plain")