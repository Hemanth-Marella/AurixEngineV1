from fastapi import APIRouter
from ..SearchServer.Services.summary_service import SummaryService
from ..SearchServer.LanggraphTools.LanggraphState import LanggraphState

from pydantic import BaseModel

class SummaryRequest(BaseModel):
    chapter_name: str
    file_hash : str

router = APIRouter(prefix="/summary",tags=["Summary"])

@router.post("/summaryApi")
async def summary(request :SummaryRequest):

    service = SummaryService(request.chapter_name,request.file_hash)

    result = await service.summary_answer()

    return {
        'summary':result
    }
