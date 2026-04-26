import base64

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.config import PDF_INSIGHT_API_KEY
from app.services.document_processor import process_pdf_bytes


class PowerAutomatePdfUpload(BaseModel):
    filename: str = Field(..., examples=["sample.pdf"])
    file_content_base64: str = Field(..., examples=["JVBERi0xLjQK..."])


router = APIRouter(prefix="/power-automate", tags=["power-automate"])


def verify_api_key(x_api_key: str | None) -> None:
    if not PDF_INSIGHT_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="PDF_INSIGHT_API_KEY is not configured on the backend.",
        )

    if x_api_key != PDF_INSIGHT_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key.",
        )


@router.post("/process-pdf")
def process_pdf_from_power_automate(
    payload: PowerAutomatePdfUpload,
    x_api_key: str | None = Header(default=None),
):
    verify_api_key(x_api_key)

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
