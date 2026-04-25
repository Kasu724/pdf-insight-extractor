from fastapi import APIRouter, HTTPException

from app.services.document_store import (
    get_document_metadata,
    get_extracted_text,
    list_document_metadata,
)
from app.services.insight_extractor import generate_document_insights

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/")
def list_documents():
    return {
        "documents": list_document_metadata()
    }


@router.get("/{file_id}")
def get_document(file_id: str):
    try:
        return get_document_metadata(file_id)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/{file_id}/text")
def get_document_text(file_id: str):
    try:
        text = get_extracted_text(file_id)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    return {
        "file_id": file_id,
        "character_count": len(text),
        "text": text,
    }


@router.get("/{file_id}/insights")
def get_document_insights(file_id: str):
    try:
        text = get_extracted_text(file_id)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    insights = generate_document_insights(text)

    return {
        "file_id": file_id,
        **insights,
    }
