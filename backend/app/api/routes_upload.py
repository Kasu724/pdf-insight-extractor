from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.document_store import save_document_metadata, save_extracted_text
from app.services.pdf_parser import extract_text_from_pdf

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = Path("data/uploads")


@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_id = str(uuid4())
    original_filename = file.filename or "uploaded.pdf"
    saved_filename = f"{file_id}_{original_filename}"
    saved_path = UPLOAD_DIR / saved_filename

    file_bytes = await file.read()
    saved_path.write_bytes(file_bytes)

    try:
        extracted = extract_text_from_pdf(saved_path)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    processed_text_path = save_extracted_text(
        file_id=file_id,
        text=extracted["full_text"],
    )

    metadata = {
        "file_id": file_id,
        "original_filename": original_filename,
        "saved_filename": saved_filename,
        "saved_path": str(saved_path),
        "processed_text_path": str(processed_text_path),
        "page_count": extracted["page_count"],
        "character_count": extracted["character_count"],
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }

    metadata_path = save_document_metadata(
        file_id=file_id,
        metadata=metadata,
    )

    return {
        **metadata,
        "metadata_path": str(metadata_path),
        "text_preview": extracted["text_preview"],
        "message": "PDF uploaded, parsed, and stored successfully.",
    }
