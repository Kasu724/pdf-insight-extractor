from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

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

    return {
        "file_id": file_id,
        "original_filename": original_filename,
        "saved_filename": saved_filename,
        "saved_path": str(saved_path),
        "message": "PDF uploaded successfully.",
    }
