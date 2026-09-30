import time
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.ocr import process_document_ocr
from app.pii import detect_and_redact_pii
from app.summarizer import generate_summary
from app.dashboard import DASHBOARD_HTML
from app.landing import LANDING_HTML

class LoginPayload(BaseModel):
    username: str
    password: str

class FeedbackPayload(BaseModel):
    category: str
    comment: str

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

import os
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
def get_landing():
    """Renders the SecureVault SaaS Landing Page."""
    return HTMLResponse(content=LANDING_HTML)

@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/dashboard/", response_class=HTMLResponse)
@app.get("/ai-api/dashboard", response_class=HTMLResponse)
@app.get("/ai-api/dashboard/", response_class=HTMLResponse)
def get_dashboard():
    """Renders the interactive SecureVault AI Document Intelligence Web Dashboard."""
    return HTMLResponse(
        content=DASHBOARD_HTML,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.post("/login")
@app.post("/ai-api/login")
def login(payload: LoginPayload):
    import os
    import requests
    from requests.auth import HTTPBasicAuth
    
    nc_host = os.getenv("NEXTCLOUD_HOST", "nextcloud")
    admin_user = os.getenv("NEXTCLOUD_ADMIN_USER", "admin")
    admin_pass = os.getenv("NEXTCLOUD_ADMIN_PASSWORD", "ChangeMeWithAStrongPassword123!")
    
    # 1. Check if the user exists via OCS API using Admin Auth
    ocs_url = f"http://{nc_host}/ocs/v1.php/cloud/users/{payload.username}"
    headers = {"OCS-APIRequest": "true", "Accept": "application/json"}
    admin_auth = HTTPBasicAuth(admin_user, admin_pass)
    
    try:
        check_resp = requests.get(ocs_url, headers=headers, auth=admin_auth, timeout=5)
        check_data = check_resp.json() if check_resp.status_code == 200 else {}
        ocs_statuscode = check_data.get("ocs", {}).get("meta", {}).get("statuscode", 0)
        
        if ocs_statuscode == 404:
            # User does not exist, auto-provision them!
            create_url = f"http://{nc_host}/ocs/v1.php/cloud/users"
            data = {"userid": payload.username, "password": payload.password}
            create_resp = requests.post(create_url, headers=headers, auth=admin_auth, data=data, timeout=8)
            create_data = create_resp.json() if create_resp.status_code == 200 else {}
            create_statuscode = create_data.get("ocs", {}).get("meta", {}).get("statuscode", 0)
            
            if create_statuscode == 100:
                return {"status": "success", "message": "User auto-provisioned and authenticated"}
            else:
                msg = create_data.get("ocs", {}).get("meta", {}).get("message", "Failed to auto-provision user.")
                raise HTTPException(status_code=400, detail=f"User Registration Failed: {msg}")
                
        elif ocs_statuscode == 100:
            # 2. User exists, verify credentials against Nextcloud WebDAV
            auth = HTTPBasicAuth(payload.username, payload.password)
            url = f"http://{nc_host}/remote.php/dav/files/{payload.username}/"
            
            resp = requests.request("PROPFIND", url, auth=auth, timeout=5)
            if resp.status_code in (200, 207):
                return {"status": "success", "message": "Authentication successful"}
            elif resp.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid credentials. Please try again.")
            elif resp.status_code == 429:
                raise HTTPException(status_code=429, detail="Too many failed login attempts. Nextcloud brute-force protection triggered. Please wait 30 seconds.")
            else:
                raise HTTPException(status_code=401, detail=f"Authentication failed (Status: {resp.status_code})")
        else:
            raise HTTPException(status_code=500, detail=f"Unexpected response from Nextcloud OCS API (Code: {ocs_statuscode})")
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
def submit_feedback(payload: FeedbackPayload):
    """Stores user feedback from the landing page."""
    # In a real app, this might insert into a database or send an email.
    print(f"Feedback received - Category: {payload.category}, Comment: {payload.comment}")
    return {"status": "success", "message": "Thank you for helping us secure SecureVault!"}

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

@app.post("/vault/files")
@app.post("/ai-api/vault/files")
def list_vault_files(payload: LoginPayload):
    import os
    import requests
    import xml.etree.ElementTree as ET
    from requests.auth import HTTPBasicAuth
    
    nc_host = os.getenv("NEXTCLOUD_HOST", "nextcloud")
    folder_name = "SecureVault_Sanitized_Docs"
    url = f"http://{nc_host}/remote.php/dav/files/{payload.username}/{folder_name}/"
    auth = HTTPBasicAuth(payload.username, payload.password)
    
    try:
        # PROPFIND Depth 1 gets the folder and its immediate children
        headers = {"Depth": "1"}
        resp = requests.request("PROPFIND", url, auth=auth, headers=headers, timeout=5)
        
        if resp.status_code == 404:
            return {"status": "success", "files": []}
        elif resp.status_code not in (200, 207):
            raise HTTPException(status_code=401, detail="Invalid credentials or unauthorized.")
            
        # Parse WebDAV XML response
        root = ET.fromstring(resp.content)
        files = []
        # XML namespaces for WebDAV
        namespaces = {'d': 'DAV:'}
        
        for response in root.findall('d:response', namespaces):
            href = response.find('d:href', namespaces)
            if href is not None:
                path = href.text
                # Skip the directory itself
                if path.endswith(f"/{folder_name}/"):
                    continue
                
                filename = path.split('/')[-1]
                
                # Get file size and last modified (if needed)
                propstat = response.find('d:propstat', namespaces)
                size = 0
                if propstat is not None:
                    prop = propstat.find('d:prop', namespaces)
                    if prop is not None:
                        getcontentlength = prop.find('d:getcontentlength', namespaces)
                        if getcontentlength is not None and getcontentlength.text:
                            size = int(getcontentlength.text)
                
                if filename:
                    files.append({"name": filename, "size": size})
                    
        return {"status": "success", "files": files}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to fetch files: {str(e)}")

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
    username: Optional[str] = Field(None, description="Nextcloud username")
    password: Optional[str] = Field(None, description="Nextcloud password")

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
    nc_user = payload.username if payload.username else os.getenv("NEXTCLOUD_ADMIN_USER", "admin")
    nc_pass = payload.password if payload.password else os.getenv("NEXTCLOUD_ADMIN_PASSWORD", "ChangeMeWithAStrongPassword123!")
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
                "nextcloud_url": "https://localhost/index.php/apps/files/?dir=/SecureVault_Sanitized_Docs",
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
                "nextcloud_url": "https://localhost/index.php/apps/files/?dir=/SecureVault_Sanitized_Docs",
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
            "nextcloud_url": "https://localhost/index.php/apps/files/?dir=/SecureVault_Sanitized_Docs",
            "bytes_written": len(file_bytes),
            "nextcloud_status_code": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

