# PDF Insight Extractor

PDF Insight Extractor is a project for learning workflow automation, AI document processing, Databricks-based data processing, and agent-style chat interfaces.

The project demonstrates how a PDF can move through an automated workflow:

1. A user uploads a PDF.
2. Power Automate detects or triggers the workflow.
3. A Python API receives and parses the PDF.
4. Extracted document text and metadata are prepared for Databricks.
5. Databricks stores, processes, and enriches the document data.
6. Copilot Studio provides a chat interface for asking questions about processed PDFs.

## Project Goals

- Learn Power Automate workflow design.
- Learn PDF parsing and document-processing basics in Python.
- Learn how Databricks can support AI and data workflows.
- Learn how Copilot Studio can provide an agent/chat interface.

## Technology Stack

| Area | Tool |
| --- | --- |
| Workflow automation | Power Automate |
| Backend API | Python, FastAPI |
| PDF parsing | PyMuPDF |
| Data processing | Databricks Free Edition |
| Chat interface | Copilot Studio |
| Local storage | Filesystem, SQLite |
| Demo UI | Streamlit |

## Enterprise Mapping

| Project Component | Enterprise Concept |
| --- | --- |
| Power Automate flow | Automated business workflow |
| Python FastAPI backend | Custom processing service |
| PDF parser | Document ingestion and extraction layer |
| Databricks notebooks | AI/data processing backend |
| Databricks storage | Structured document repository |
| Copilot Studio agent | Business-facing conversational assistant |
| Streamlit demo UI | Lightweight prototype interface |

## Initial MVP Scope

1. Create a Python backend.
2. Upload a PDF locally.
3. Extract text from the PDF.
4. Store the extracted result.
5. Return a simple summary and metadata.
6. Connect the workflow to Power Automate.
7. Add Databricks processing.
8. Add Copilot Studio chat.

## Repository Structure

```text
pdf-insight-extractor/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  ├─ services/
│  │  └─ models/
│  ├─ data/
│  │  ├─ uploads/
│  │  └─ processed/
│  └─ tests/
├─ frontend/
├─ integrations/
│  ├─ power_automate/
│  ├─ databricks/
│  │  └─ notebooks/
│  └─ copilot_studio/
├─ sample_pdfs/
├─ docs/
├─ .gitignore
└─ README.md