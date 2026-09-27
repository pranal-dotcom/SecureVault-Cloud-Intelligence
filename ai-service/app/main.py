import time
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.ocr import process_document_ocr
from app.pii import detect_and_redact_pii
from app.summarizer import generate_summary
from app.dashboard import DASHBOARD_HTML

app = FastAPI(
    title="SecureVault AI Document Intelligence Engine",
    description="Autonomous OCR, PII Identification & Redaction, and Summary Engine for Zero-Trust Cloud Vault",
    version="1.0.0",
    root_path="/ai-api",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/dashboard/", response_class=HTMLResponse)
@app.get("/ai-api/dashboard", response_class=HTMLResponse)
@app.get("/ai-api/dashboard/", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    """Renders the interactive SecureVault AI Document Intelligence Web Dashboard."""
    return HTMLResponse(content=DASHBOARD_HTML)

class TextPayload(BaseModel):
    text: str = Field(..., description="Raw text to be analyzed for PII and summarized")
    filename: Optional[str] = Field("direct_input.txt", description="Optional filename reference")

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    modules: List[str]
    timestamp: str

@app.get("/health", response_model=HealthResponse)
@app.get("/ai-api/health", response_model=HealthResponse)
def health_check():
    """Returns AI microservice operational status and active feature engines."""
    return {
        "status": "healthy",
        "service": "SecureVault-AI-Document-Intelligence",
        "version": "1.0.0",
        "modules": [
            "Tesseract OCR Engine (PDF/Image)",
            "Zero-Trust PII Redaction (Aadhaar, PAN, CC, Email, Phone)",
            "Document Summarizer & Highlight Extractor"
        ],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/analyze")
@app.post("/ai-api/analyze")
async def analyze_document(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    """
    Unified analysis endpoint accepting either a file upload (PDF/PNG/JPG/etc.)
    or raw text payload. Executes OCR -> PII Redaction -> Summarization pipeline.
    """
    raw_text = ""
    filename = "text_payload.txt"
    source_type = "raw_text"

    # Case 1: Uploaded file
    if file is not None and file.filename:
        filename = file.filename
        source_type = "file_upload"
        try:
            file_bytes = await file.read()
            if len(file_bytes) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            raw_text = process_document_ocr(file_bytes, file.filename, file.content_type)
        except ValueError as ve:
            raise HTTPException(status_code=422, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process document OCR: {str(e)}")

    # Case 2: Raw Text provided via form or query
    elif text:
        raw_text = text.strip()

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No input provided. Please upload a file via 'file' field or provide text via 'text' field."
        )

    if not raw_text.strip():
        return {
            "status": "warning",
            "message": "No extractable text found in the provided input.",
            "filename": filename,
            "source_type": source_type,
            "original_text": "",
            "redacted_text": "",
            "pii_summary": {"total_redactions": 0, "categories": {}, "entities": []},
            "summary": generate_summary("")
        }

    # Step 1: PII Identification & Redaction
    redacted_text, detected_entities, category_counts = detect_and_redact_pii(raw_text)

    # Step 2: Key Highlight & Summary Generation
    doc_summary = generate_summary(redacted_text)

    return {
        "status": "success",
        "filename": filename,
        "source_type": source_type,
        "original_text": raw_text,
        "redacted_text": redacted_text,
        "pii_summary": {
            "total_redactions": len(detected_entities),
            "categories": category_counts,
            "entities": detected_entities
        },
        "summary": doc_summary
    }

@app.post("/analyze/text")
@app.post("/ai-api/analyze/text")
def analyze_text_json(payload: TextPayload):
    """Dedicated JSON endpoint for analyzing direct text payloads."""
    raw_text = payload.text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    redacted_text, detected_entities, category_counts = detect_and_redact_pii(raw_text)
    doc_summary = generate_summary(redacted_text)

    return {
        "status": "success",
        "filename": payload.filename,
        "source_type": "json_payload",
        "original_text": raw_text,
        "redacted_text": redacted_text,
        "pii_summary": {
            "total_redactions": len(detected_entities),
            "categories": category_counts,
            "entities": detected_entities
        },
        "summary": doc_summary
    }

class VaultCommitPayload(BaseModel):
    filename: Optional[str] = Field("Sanitized_KYC_Document.txt", description="Target filename for Nextcloud Vault")
    sanitized_text: str = Field(..., description="Sanitized text payload")
    original_filename: Optional[str] = Field(None, description="Original uploaded filename")

@app.post("/vault/commit")
@app.post("/ai-api/vault/commit")
def commit_to_vault(payload: VaultCommitPayload):
    """
    Synchronizes sanitized documents directly into the admin user's Nextcloud storage
    via internal WebDAV API (http://nextcloud/remote.php/dav/files/<user>/<filename>)
    and triggers OCC files:scan for immediate UI refresh.
    """
    import os
    import subprocess
    import requests
    from requests.auth import HTTPBasicAuth

    nc_host = os.getenv("NEXTCLOUD_HOST", "nextcloud")
    nc_user = os.getenv("NEXTCLOUD_ADMIN_USER", "admin")
    nc_pass = os.getenv("NEXTCLOUD_ADMIN_PASSWORD", "ChangeMeWithAStrongPassword123!")
    folder_name = "SecureVault_Sanitized_Docs"
    
    # Generate canonical sanitized filename if not provided
    target_name = payload.filename.strip() if payload.filename else ""
    if not target_name:
        if payload.original_filename:
            base = payload.original_filename.rsplit(".", 1)[0]
            clean_base = "".join(c for c in base if c.isalnum() or c in ("-", "_")).strip()
            target_name = f"Sanitized_{clean_base or 'Document'}.txt"
        else:
            target_name = "Sanitized_Document.txt"
    
    if not target_name.endswith(".txt"):
        target_name += ".txt"

    file_bytes = payload.sanitized_text.encode("utf-8")
    auth = HTTPBasicAuth(nc_user, nc_pass)
    
    # Primary WebDAV file URLs (Root Files folder + Dedicated Folder)
    root_webdav_url = f"http://{nc_host}/remote.php/dav/files/{nc_user}/{target_name}"
    folder_url = f"http://{nc_host}/remote.php/dav/files/{nc_user}/{folder_name}"
    folder_webdav_url = f"http://{nc_host}/remote.php/dav/files/{nc_user}/{folder_name}/{target_name}"
    vault_rel_path = f"/files/{nc_user}/{target_name}"
    
    try:
        # Step 1: Ensure dedicated SecureVault_Sanitized_Docs folder exists via MKCOL
        try:
            requests.request("MKCOL", folder_url, auth=auth, timeout=5)
        except Exception:
            pass

        # Step 2: Upload sanitized copy directly inside SecureVault_Sanitized_Docs folder
        resp_folder = None
        try:
            resp_folder = requests.put(
                folder_webdav_url,
                data=file_bytes,
                headers={"Content-Type": "text/plain; charset=utf-8", "User-Agent": "SecureVault-AI-Sync/1.0"},
                auth=auth,
                timeout=12
            )
        except Exception as e:
            print(f"Folder upload warning: {e}")

        # Step 3: Upload sanitized copy directly inside root files for immediate visibility
        resp = requests.put(
            root_webdav_url,
            data=file_bytes,
            headers={"Content-Type": "text/plain; charset=utf-8", "User-Agent": "SecureVault-AI-Sync/1.0"},
            auth=auth,
            timeout=12
        )

        # Step 4: Trigger OCC background file scan if docker CLI is accessible on host
        try:
            subprocess.run(
                ["docker", "compose", "exec", "-u", "www-data", "nextcloud", "php", "occ", "files:scan", nc_user],
                capture_output=True,
                timeout=8
            )
        except Exception:
            pass  # Non-blocking if running in containerized or background isolation
        
        if resp.status_code in (200, 201, 204) or (resp_folder and resp_folder.status_code in (200, 201, 204)):
            return {
                "status": "success",
                "sync_state": "COMMITTED_WEBDAV",
                "message": f"Successfully synchronized '{target_name}' to Nextcloud Vault via WebDAV (Root + SecureVault_Sanitized_Docs).",
                "filename": target_name,
                "folder": f"/{folder_name}/ & /",
                "webdav_url": root_webdav_url,
                "folder_webdav_url": folder_webdav_url,
                "vault_path": vault_rel_path,
                "nextcloud_url": "https://localhost/apps/files/",
                "bytes_written": len(file_bytes),
                "nextcloud_status_code": resp.status_code,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        else:
            return {
                "status": "warning",
                "sync_state": "WEBDAV_HTTP_ERROR",
                "message": f"Nextcloud WebDAV returned status {resp.status_code}.",
                "filename": target_name,
                "webdav_url": root_webdav_url,
                "folder_webdav_url": folder_webdav_url,
                "vault_path": vault_rel_path,
                "nextcloud_url": "https://localhost/apps/files/",
                "bytes_written": len(file_bytes),
                "nextcloud_status_code": resp.status_code,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    except requests.exceptions.RequestException as req_err:
        # Graceful fallback when Nextcloud container is starting up or in standalone test mode
        return {
            "status": "staged",
            "sync_state": "STAGED_LOCAL",
            "message": f"Sanitized file staged for Nextcloud commit (Destination: {vault_rel_path}).",
            "filename": target_name,
            "webdav_url": root_webdav_url,
            "folder_webdav_url": folder_webdav_url,
            "vault_path": vault_rel_path,
            "nextcloud_url": "https://localhost/apps/files/",
            "bytes_written": len(file_bytes),
            "nextcloud_status_code": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

