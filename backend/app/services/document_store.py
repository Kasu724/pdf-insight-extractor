from pathlib import Path


PROCESSED_DIR = Path("data/processed")


def save_extracted_text(file_id: str, text: str) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DIR / f"{file_id}.txt"
    output_path.write_text(text, encoding="utf-8")

    return output_path
