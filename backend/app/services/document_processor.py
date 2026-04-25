from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.services.document_store import save_document_metadata, save_extracted_text
from app.services.pdf_parser import extract_text_from_pdf


UPLOAD_DIR = Path("data/uploads")


def process_pdf_bytes(file_bytes: bytes, original_filename: str) -> dict:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_id = str(uuid4())
    safe_original_filename = Path(original_filename or "uploaded.pdf").name
    saved_filename = f"{file_id}_{safe_original_filename}"
    saved_path = UPLOAD_DIR / saved_filename

    saved_path.write_bytes(file_bytes)

    extracted = extract_text_from_pdf(saved_path)

    processed_text_path = save_extracted_text(
        file_id=file_id,
        text=extracted["full_text"],
    )

    metadata = {
        "file_id": file_id,
        "original_filename": safe_original_filename,
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
    }
