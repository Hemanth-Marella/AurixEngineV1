from ..SearchServer.Services.pdf_processing_service import PdfProcessingService
from fastapi import APIRouter, UploadFile, File
import os
import shutil

router = APIRouter(prefix="/pdf", tags=["PDF"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    service = PdfProcessingService(file_path)

    result = await service.upload_document()

    return result
