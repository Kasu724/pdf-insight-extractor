from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.document_processor import process_pdf_bytes

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    file_bytes = await file.read()
    original_filename = file.filename or "uploaded.pdf"

    try:
        processed_document = process_pdf_bytes(
            file_bytes=file_bytes,
            original_filename=original_filename,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {
        **processed_document,
        "message": "PDF uploaded, parsed, and stored successfully.",
    }
