from fastapi import APIRouter
from ..SearchServer.Services.summary_service import SummaryService

from pydantic import BaseModel

class SummaryRequest(BaseModel):
    chapter_name: str

router = APIRouter(prefix="/summary",tags=["Summary"])

@router.post("/summaryApi")
async def summary(request :SummaryRequest):

    service = SummaryService(request.chapter_name)

    result = await service.summary_answer()

    return {
        'summary':result
    }

