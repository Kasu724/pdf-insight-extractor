from pathlib import Path

import fitz


def extract_text_from_pdf(pdf_path: Path) -> dict:
    pages = []

    with fitz.open(pdf_path) as document:
        if document.needs_pass:
            raise ValueError("Password-protected PDFs are not supported yet.")

        for page_number, page in enumerate(document, start=1):
            text = page.get_text()
            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )

    full_text = "\n\n".join(page["text"] for page in pages)

    return {
        "page_count": len(pages),
        "character_count": len(full_text),
        "full_text": full_text,
        "text_preview": full_text[:1000],
        "pages": pages,
    }
