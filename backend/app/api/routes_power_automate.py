import base64

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.document_processor import process_pdf_bytes


class PowerAutomatePdfUpload(BaseModel):
    filename: str = Field(..., examples=["sample.pdf"])
    file_content_base64: str = Field(..., examples=["JVBERi0xLjQK..."])


router = APIRouter(prefix="/power-automate", tags=["power-automate"])


@router.post("/process-pdf")
def process_pdf_from_power_automate(payload: PowerAutomatePdfUpload):
    if not payload.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF filenames are supported.",
        )

    try:
        file_bytes = base64.b64decode(payload.file_content_base64)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail="file_content_base64 must be valid base64.",
        ) from error

    try:
        processed_document = process_pdf_bytes(
            file_bytes=file_bytes,
            original_filename=payload.filename,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {
        **processed_document,
        "message": "PDF received from Power Automate, parsed, and stored successfully.",
    }
