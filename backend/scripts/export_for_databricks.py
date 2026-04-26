import json
from pathlib import Path


PROCESSED_DIR = Path("data/processed")
EXPORT_DIR = Path("data/exports")
EXPORT_PATH = EXPORT_DIR / "documents_for_databricks.jsonl"


def load_processed_documents() -> list[dict]:
    documents = []

    for metadata_path in PROCESSED_DIR.glob("*.json"):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

        file_id = metadata["file_id"]
        text_path = PROCESSED_DIR / f"{file_id}.txt"

        if not text_path.exists():
            continue

        text = text_path.read_text(encoding="utf-8")

        documents.append(
            {
                "file_id": file_id,
                "original_filename": metadata["original_filename"],
                "page_count": metadata["page_count"],
                "character_count": metadata["character_count"],
                "processed_at": metadata["processed_at"],
                "text": text,
            }
        )

    return documents


def export_documents() -> Path:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    documents = load_processed_documents()

    with EXPORT_PATH.open("w", encoding="utf-8") as export_file:
        for document in documents:
            export_file.write(json.dumps(document) + "\n")

    return EXPORT_PATH


if __name__ == "__main__":
    output_path = export_documents()
    print(f"Exported processed documents to: {output_path}")
