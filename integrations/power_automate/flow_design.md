# Power Automate Flow Design

## Flow Name

PDF Insight Extractor - Process Uploaded PDF

## Purpose

This Power Automate flow is the workflow automation layer of PDF Insight Extractor.

It detects when a PDF is uploaded to OneDrive for Business, reads the file content, and sends the PDF to the FastAPI backend for parsing and processing.

## Current Implementation Status

1. Power Automate detected a new PDF in OneDrive.
2. The flow retrieved the PDF file content.
3. The flow sent the PDF to the local FastAPI backend through a temporary VS Code public forwarded port.
4. The backend saved the uploaded PDF.
5. The backend extracted text with PyMuPDF.
6. The backend created a processed `.txt` text file.
7. The backend created a processed `.json` metadata file.

## OneDrive Folder

The flow watches this OneDrive for Business folder:

```text
/PDF Insight Extractor/Uploads
```

Only PDFs should be uploaded to this folder during testing.

## Trigger

Connector:

```text
OneDrive for Business
```

Trigger:

```text
When a file is created
```

Folder:

```text
/PDF Insight Extractor/Uploads
```

Purpose:

This trigger starts the flow whenever a new file is uploaded to the selected OneDrive folder.

## Action 1: Get File Content

Connector:

```text
OneDrive for Business
```

Action:

```text
Get file content
```

File input:

```text
Identifier
```

The `Identifier` value comes from the dynamic content produced by the `When a file is created` trigger.

Purpose:

This action reads the actual PDF content from OneDrive. The trigger tells the flow that a file exists, but the backend needs the file bytes in order to parse the PDF.

## Action 2: HTTP - Process PDF

Connector:

```text
HTTP
```

Method:

```text
POST
```

URI during local testing:

```text
https://YOUR-VSCODE-TUNNEL-URL/power-automate/process-pdf
```

URI after Azure deployment:

```text
https://YOUR-AZURE-APP-SERVICE-NAME.azurewebsites.net/power-automate/process-pdf
```

Headers:

```json
{
  "Content-Type": "application/json"
}
```

Body:

```json
{
  "filename": "@{triggerOutputs()?['headers']['x-ms-file-name']}",
  "file_content_base64": "@{base64(body('Get_file_content'))}"
}
```

Important note:

The internal action name may differ in Power Automate. If the flow rejects `Get_file_content`, use **Peek code** on the Get file content action and replace `Get_file_content` with the exact internal action name.

Example:

```json
{
  "filename": "@{triggerOutputs()?['headers']['x-ms-file-name']}",
  "file_content_base64": "@{base64(body('Get_file_content_using_path'))}"
}
```

## Base64

PDF files are binary files. The backend endpoint expects the PDF content to be sent as base64 inside JSON.

Valid base64 PDF content usually starts with:

```text
JVBERi0x
```

Raw PDF content usually starts with:

```text
%PDF-1.
```

If the backend receives raw PDF content instead of base64, it returns:

```text
file_content_base64 must be valid base64.
```

The fix is to wrap the file content expression with Power Automate's `base64(...)` function.

## Backend Endpoint

The flow calls this backend endpoint:

```text
POST /power-automate/process-pdf
```

Expected request body:

```json
{
  "filename": "example.pdf",
  "file_content_base64": "JVBERi0xLjQK..."
}
```

Expected successful response:

```json
{
  "file_id": "generated-file-id",
  "original_filename": "example.pdf",
  "saved_filename": "generated-file-id_example.pdf",
  "saved_path": "data/uploads/generated-file-id_example.pdf",
  "processed_text_path": "data/processed/generated-file-id.txt",
  "page_count": 1,
  "character_count": 1234,
  "processed_at": "2026-04-25T00:00:00+00:00",
  "metadata_path": "data/processed/generated-file-id.json",
  "text_preview": "Extracted document text preview...",
  "message": "PDF received from Power Automate, parsed, and stored successfully."
}
```

## Backend Files Created

For each processed PDF, the backend creates:

```text
backend/data/uploads/{file_id}_{original_filename}
backend/data/processed/{file_id}.txt
backend/data/processed/{file_id}.json
```

The `.txt` file stores the extracted text.

The `.json` file stores document metadata such as:

- file ID
- original filename
- saved filename
- uploaded PDF path
- processed text path
- page count
- character count
- processing timestamp

## Local Testing Setup

During local testing, the FastAPI backend runs on:

```text
http://127.0.0.1:8000
```

Because Power Automate runs in Microsoft's cloud, it cannot call `127.0.0.1` directly.

For the first integration test, VS Code Port Forwarding was used to expose the local backend through a temporary public HTTPS URL:

```text
https://YOUR-VSCODE-TUNNEL-URL
```

This is only a development shortcut. The planned deployment target is Azure App Service.

## Validation Checklist

Use this checklist to verify the flow:

1. Start the FastAPI backend locally.
2. Forward port `8000` in VS Code.
3. Set the forwarded port visibility to `Public`.
4. Confirm `/health` works through the public forwarded URL.
5. Upload a PDF to `/PDF Insight Extractor/Uploads` in OneDrive for Business.
6. Open the flow run history in Power Automate.
7. Confirm the trigger succeeded.
8. Confirm `Get file content` succeeded.
9. Confirm the HTTP action succeeded.
10. Confirm the backend returned a `file_id`.
11. Confirm a `.txt` file exists in `backend/data/processed`.
12. Confirm a `.json` file exists in `backend/data/processed`.

## Troubleshooting

### Flow will not save

Power Automate requires at least one trigger and one action.

Fix:

Add an action after the trigger, such as `Compose`, `Get file content`, or `HTTP`.

### HTTP action returns `file_content_base64 must be valid base64`

Cause:

Power Automate sent raw PDF content instead of base64.

Fix:

Use:

```text
@{base64(body('Get_file_content'))}
```

instead of passing the file content directly.

### HTTP action cannot reach the backend

Possible causes:

- The FastAPI server is not running.
- The VS Code forwarded port stopped.
- The forwarded port is private instead of public.
- The URI still points to `127.0.0.1`.

Fix:

Confirm the public tunnel URL works by opening:

```text
https://YOUR-VSCODE-TUNNEL-URL/health
```

### Backend returns `Only PDF filenames are supported`

Cause:

The filename sent by Power Automate does not end with `.pdf`.

Fix:

Confirm the uploaded file is a PDF and that the HTTP body sends the correct filename dynamic content.

## Security Notes

The current local testing endpoint does not yet require authentication.

Before deploying or sharing the API URL broadly, the project should add a simple API key or bearer token check so only trusted callers can submit PDFs.

Planned improvement:

```text
Power Automate HTTP header
  -> x-api-key
FastAPI backend
  -> validate x-api-key before processing PDFs
```

## Future Azure Deployment

The temporary VS Code public forwarded URL will eventually be replaced with Azure App Service.

After deployment, the HTTP action URI should be updated from:

```text
https://YOUR-VSCODE-TUNNEL-URL/power-automate/process-pdf
```

to:

```text
https://YOUR-AZURE-APP-SERVICE-NAME.azurewebsites.net/power-automate/process-pdf
```

This makes the workflow independent of the local development machine.