from ..SearchServer.Services.pdf_processing_service import PdfProcessingService
from fastapi import APIRouter, UploadFile, File
import os
import shutil

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    
    # read the uploaded file into memory
    pdf_bytes = await file.read()

    # pass bytes and filename to the service
    service = PdfProcessingService(
        pdf_bytes=pdf_bytes,
        filename=file.filename
    )

    result = await service.upload_document()

    return result
