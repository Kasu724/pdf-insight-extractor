from fastapi import APIRouter, HTTPException

from app.services.document_store import get_document_metadata, list_document_metadata

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
