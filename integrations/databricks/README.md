# Databricks Integration

This folder contains the Databricks portion of PDF Insight Extractor.

Databricks is used as the AI/data backend layer of the project. The local FastAPI backend extracts text and metadata from PDFs, then exports processed document records into a JSON Lines file that can be loaded into Databricks.

## Current Status

Completed:

- Local backend exports processed PDF records to JSONL
- Databricks notebook loads the JSONL export
- Notebook creates a Spark DataFrame
- Notebook saves the records as the `pdf_insight_documents` table
- Validation SQL queries confirm the table contents

Planned next:

- Add document chunking for retrieval
- Add a simple search/query notebook
- Prepare the data layer for Copilot Studio integration
- Later, explore Databricks AI/agent capabilities

## Files

```text
integrations/databricks/
|-- README.md
`-- notebooks/
    `-- 01_load_documents.py
```

## Local Export File
The backend creates this file:
```text
backend/data/exports/documents_for_databricks.jsonl
```
The export script is:
```text
backend/scripts/export_for_databricks.py
```
Run it from the backend folder:
```powershell
cd backend
python scripts\export_for_databricks.py
```

Each line in the export file is one processed document record.
Example shape:
```json
{
  "file_id": "generated-file-id",
  "original_filename": "example.pdf",
  "page_count": 1,
  "character_count": 1234,
  "processed_at": "2026-04-25T00:00:00+00:00",
  "text": "Extracted PDF text..."
}
```

## Notebook
Notebook source file:
```text
integrations/databricks/notebooks/01_load_documents.py
```

Purpose:
1. Load `documents_for_databricks.jsonl`
2. Parse document records
3. Create a Spark DataFrame
4. Display the document data
5. Save the table as pdf_insight_documents
6. Run validation queries

## Databricks Setup
In Databricks Free Edition:
1. Create a workspace folder: `PDF Insight Extractor`
2. Upload or import the notebook: `integrations/databricks/notebooks/01_load_documents.py`
3. Upload the generated export file: `backend/data/exports/documents_for_databricks.jsonl`
4. Open the notebook
5. Run the notebook cells in order.

Expected result:
```text
Saved table: pdf_insight_documents
```

