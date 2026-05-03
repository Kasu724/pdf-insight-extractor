# PDF Insight Extractor

PDF Insight Extractor is a portfolio project for learning workflow automation, AI document processing, Databricks-based data processing, and agent-style chat interfaces.

The project demonstrates a document-processing workflow where a PDF is uploaded, detected by Power Automate, sent to a Python API, parsed into text and metadata, and prepared for later Databricks and Copilot Studio integration.

## Project Goals

- Learn Power Automate workflow design using a real file-ingestion flow
- Learn PDF parsing and document-processing basics in Python
- Learn how Databricks can support AI and data workflows
- Learn how Copilot Studio can provide a business-facing agent/chat interface
- Build a clean, explainable project that can be deployed and demoed

## Current Status

Completed:

- FastAPI backend created
- PDF upload endpoint created
- PDF text extraction added with PyMuPDF
- Extracted text stored locally as `.txt`
- Processed document metadata stored locally as `.json`
- API endpoints added to list documents, retrieve metadata, retrieve extracted text, and generate basic insights
- Power Automate flow connected to the backend through a temporary VS Code public forwarded port
- Power Automate successfully processed a PDF uploaded to OneDrive for Business
- Databricks export script creates a JSONL file from processed documents.
- Databricks notebook loads exported document records into a table.
- Databricks document chunking and basic keyword search

Planned next:

- Add Databricks ingestion for processed document data
- Add Copilot Studio chat integration
- Deploy the API to Azure App Service for a stable demo URL

## Technology Stack

| Area | Tool |
| --- | --- |
| Workflow automation | Power Automate |
| Backend API | Python, FastAPI |
| PDF parsing | PyMuPDF |
| Data processing | Databricks Free Edition |
| Chat interface | Copilot Studio |
| Local storage | Filesystem, SQLite later if needed |
| Deployment target | Azure App Service |
| Local development | VS Code on Windows 11 |

## Workflow Overview

```text
OneDrive for Business upload folder
  -> Power Automate trigger
  -> Get file content
  -> HTTP POST to FastAPI
  -> Save uploaded PDF locally
  -> Extract PDF text with PyMuPDF
  -> Save processed .txt and .json files
  -> Expose results through API endpoints
  -> Export processed documents to Databricks
  -> Chunk documents for search
  -> Run baseline document search
```

## Power Automate Integration

The current Power Automate flow watches this OneDrive for Business folder:

```text
/PDF Insight Extractor/Uploads
```

When a PDF is uploaded, the flow:

1. Detects the new file
2. Gets the file content
3. Encodes the file content as base64
4. Sends the filename and encoded content to the FastAPI backend

The flow calls:

```text
POST /power-automate/process-pdf
```

See:

```text
integrations/power_automate/flow_design.md
```

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Basic API message |
| `GET` | `/health` | Health check |
| `POST` | `/upload/pdf` | Manual PDF upload through FastAPI docs |
| `POST` | `/power-automate/process-pdf` | Power Automate-friendly PDF processing endpoint |
| `GET` | `/documents/` | List processed document metadata |
| `GET` | `/documents/{file_id}` | Get metadata for one processed document |
| `GET` | `/documents/{file_id}/text` | Get extracted text for one processed document |
| `GET` | `/documents/{file_id}/insights` | Get basic local summary and keywords |

## Local Development

Create and activate the Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend\requirements.txt
```

Run the backend:

```powershell
cd backend
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Local Data

During local development, uploaded and processed files are stored under:

```text
backend/data/uploads/
backend/data/processed/
```

Generated local files are intentionally ignored by Git.

## Repository Structure

```text
pdf-insight-extractor/
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |-- services/
|   |   `-- models/
|   |-- data/
|   |   |-- uploads/
|   |   `-- processed/
|   |-- tests/
|   `-- requirements.txt
|-- frontend/
|-- integrations/
|   |-- power_automate/
|   |   `-- flow_design.md
|   |-- databricks/
|   |   `-- notebooks/
|   `-- copilot_studio/
|-- sample_pdfs/
|-- docs/
|-- .gitignore
`-- README.md
```
