from fastapi import FastAPI

from app.api.routes_documents import router as documents_router
from app.api.routes_upload import router as upload_router

app = FastAPI(
    title="PDF Insight Extractor API",
    version="0.1.0",
)

app.include_router(upload_router)
app.include_router(documents_router)


@app.get("/")
def read_root():
    return {
        "message": "PDF Insight Extractor API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
