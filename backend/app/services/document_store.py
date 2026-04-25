import json
from pathlib import Path
from typing import Any


PROCESSED_DIR = Path("data/processed")


def save_extracted_text(file_id: str, text: str) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DIR / f"{file_id}.txt"
    output_path.write_text(text, encoding="utf-8")

    return output_path


def save_document_metadata(file_id: str, metadata: dict[str, Any]) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DIR / f"{file_id}.json"
    output_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    return output_path


def list_document_metadata() -> list[dict[str, Any]]:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    documents = []

    for metadata_path in PROCESSED_DIR.glob("*.json"):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        documents.append(metadata)

    return documents


def get_document_metadata(file_id: str) -> dict[str, Any]:
    metadata_path = PROCESSED_DIR / f"{file_id}.json"

    if not metadata_path.exists():
        raise FileNotFoundError(f"No metadata found for file_id: {file_id}")

    return json.loads(metadata_path.read_text(encoding="utf-8"))


def get_extracted_text(file_id: str) -> str:
    text_path = PROCESSED_DIR / f"{file_id}.txt"

    if not text_path.exists():
        raise FileNotFoundError(f"No extracted text found for file_id: {file_id}")

    return text_path.read_text(encoding="utf-8")
