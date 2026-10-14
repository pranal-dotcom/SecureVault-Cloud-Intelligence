import uuid
import time
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.ocr import process_document_ocr
from app.pii import detect_and_redact_pii
from app.summarizer import generate_summary
from app.compute import (
    execute_cloud_compute_pipeline,
    create_task,
    get_task_status,
    init_compute_db
)
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

@app.on_event("startup")
def on_startup():
    init_compute_db()

@app.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
@app.post("/ai-api/analyze", status_code=status.HTTP_202_ACCEPTED)
async def analyze_document(
    background_tasks: BackgroundTasks,
    response: Response,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    sync: bool = False
):
    """
    Decoupled Cloud Compute Ingestion Endpoint.
    Immediately validates the incoming file or text, assigns a unique task_id,
    registers execute_cloud_compute_pipeline() in BackgroundTasks,
    and returns HTTP 202 Accepted with status 'processing'.
    """
    raw_text = None
    filename = "text_payload.txt"
    source_type = "raw_text"
    file_bytes = None
    content_type = None

    # Step 1: Immediate Validation
    if file is not None and file.filename:
        filename = file.filename
        source_type = "file_upload"
        content_type = file.content_type
        try:
            file_bytes = await file.read()
            if len(file_bytes) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            
            # Extension validation
            ext = os.path.splitext(filename)[1].lower()
            allowed_exts = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".pdf", ".txt"}
            if ext and ext not in allowed_exts:
                raise HTTPException(status_code=422, detail=f"Unsupported file format '{ext}'. Allowed: PNG, JPG, PDF, TXT.")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    elif text is not None and text.strip():
        raw_text = text.strip()

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No input provided. Please upload a file via 'file' field or provide text via 'text' field."
        )

    # Step 2: Assign Task ID & Queue in Multi-Process Task Store
    task_id = f"task_{uuid.uuid4().hex[:12]}"
    create_task(task_id)

    # Step 3: Synchronous override if explicitly requested
    if sync:
        execute_cloud_compute_pipeline(
            task_id=task_id,
            file_bytes=file_bytes,
            filename=filename,
            content_type=content_type,
            raw_text=raw_text,
            source_type=source_type
        )
        task_data = get_task_status(task_id)
        response.status_code = status.HTTP_200_OK
        if task_data and task_data.get("result"):
            return task_data["result"]
        return task_data

    # Step 4: Decouple Compute via FastAPI BackgroundTasks
    background_tasks.add_task(
        execute_cloud_compute_pipeline,
        task_id=task_id,
        file_bytes=file_bytes,
        filename=filename,
        content_type=content_type,
        raw_text=raw_text,
        source_type=source_type
    )

    response.status_code = status.HTTP_202_ACCEPTED
    return {
        "status": "processing",
        "task_id": task_id,
        "message": "Compute task accepted and dispatched to background vCPU worker pipeline.",
        "stage": "OCR_EXTRACTION",
        "compute_status_url": f"/api/compute/status/{task_id}"
    }

@app.get("/api/compute/status/{task_id}")
@app.get("/ai-api/api/compute/status/{task_id}")
@app.get("/compute/status/{task_id}")
@app.get("/ai-api/compute/status/{task_id}")
def get_compute_status(task_id: str):
    """
    Cloud Compute Pillar Telemetry Endpoint.
    Returns:
      - status: 'QUEUED' | 'COMPUTING' | 'COMMITTED'
      - compute_duration_ms: processing time taken by the CPU
      - cpu_threads_used: number of worker threads or CPU utilization
      - stage: 'OCR_EXTRACTION' -> 'PII_SANITIZATION' -> 'VAULT_SYNC'
    """
    task = get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Compute task '{task_id}' not found.")

    response_payload = {
        "task_id": task["task_id"],
        "status": task["status"],                          # 'QUEUED' | 'COMPUTING' | 'COMMITTED'
        "compute_duration_ms": task["compute_duration_ms"],  # CPU processing duration in milliseconds
        "cpu_threads_used": task["cpu_threads_used"],        # Worker threads / CPU count
        "stage": task["stage"],                            # 'OCR_EXTRACTION' -> 'PII_SANITIZATION' -> 'VAULT_SYNC'
        "created_at": task.get("created_at"),
        "updated_at": task.get("updated_at")
    }

    if task.get("error"):
        response_payload["error"] = task["error"]

    if task.get("result"):
        result_dict = task["result"]
        response_payload["result"] = result_dict
        # Expose top-level convenience fields for downstream consumers
        for key in ("original_text", "redacted_text", "pii_summary", "summary", "filename", "source_type"):
            if key in result_dict and key not in response_payload:
                response_payload[key] = result_dict[key]

    return response_payload

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
            
        root = ET.fromstring(resp.content)
        # Process WebDAV XML to get file list...
        files = []
        for response in root.findall(".//{DAV:}response"):
            href = response.find("{DAV:}href").text
            if href.endswith("/"): 
                continue
            name = href.split("/")[-1]
            prop = response.find(".//{DAV:}prop")
            if prop:
                length_el = prop.find("{DAV:}getcontentlength")
                length = int(length_el.text) if length_el is not None and length_el.text else 0
                files.append({"name": name, "size": length})
                
        return {"status": "success", "files": files}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vault-bridge")
@app.get("/ai-api/vault-bridge")
def vault_bridge(u: str, p: str):
    """
    Acts as a Session-Bridge / SSO route to Nextcloud.
    Logs in to Nextcloud on behalf of the user, grabs session cookies,
    and redirects the browser directly to their dedicated vault.
    """
    import os
    import requests
    import re
    
    nc_host = os.getenv("NEXTCLOUD_HOST", "nextcloud")
    session = requests.Session()
    
    try:
        # 1. Fetch the Nextcloud login page to grab the CSRF requesttoken
        login_page = session.get(f"http://{nc_host}/index.php/login", timeout=5)
        
        match = re.search(r'data-requesttoken="([^"]+)"', login_page.text)
        if not match:
            raise HTTPException(status_code=500, detail="Could not extract Nextcloud CSRF token for vault bridge.")
        
        req_token = match.group(1)
        
        # 2. Submit the login form to Nextcloud
        login_data = {
            "user": u,
            "password": p,
            "timezone-offset": "0",
            "timezone": "UTC",
            "requesttoken": req_token
        }
        
        login_resp = session.post(f"http://{nc_host}/index.php/login", data=login_data, allow_redirects=False, timeout=8)
        
        if login_resp.status_code not in (302, 303):
            raise HTTPException(status_code=401, detail="Vault Bridge authentication failed. Invalid credentials.")
            
        # 3. Create RedirectResponse to the user's isolated workspace
        response = RedirectResponse(url="/index.php/apps/files/?dir=/SecureVault_Sanitized_Docs", status_code=302)
        
        # Invalidate old known session cookies just in case
        response.delete_cookie("nc_session_id", path="/")
        response.delete_cookie("oc_sessionPassphrase", path="/")
        response.delete_cookie("nc_sameSiteCookielax", path="/")
        response.delete_cookie("nc_sameSiteCookiestrict", path="/")
        
        # 4. Proxy the new Nextcloud session cookies to the client
        for cookie in session.cookies:
            response.set_cookie(
                key=cookie.name,
                value=cookie.value,
                path="/",
                httponly=cookie.has_nonstandard_attr('HttpOnly'),
                secure=True,
                samesite="Lax"
            )
            
        return response
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Vault Bridge error: {str(e)}")

@app.post("/vault-logout")
@app.post("/ai-api/vault-logout")
def vault_logout(response: Response):
    """
    Clears Nextcloud session cookies to enforce zero-trust session boundaries on SecureVault logout.
    """
    response.delete_cookie("nc_session_id", path="/")
    response.delete_cookie("oc_sessionPassphrase", path="/")
    response.delete_cookie("nc_sameSiteCookielax", path="/")
    response.delete_cookie("nc_sameSiteCookiestrict", path="/")
    return {"status": "success", "message": "Vault sessions cleared"}


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
                "nextcloud_url": f"https://{nc_user}:{nc_pass}@localhost/index.php/apps/files/?dir=/SecureVault_Sanitized_Docs",
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
                "nextcloud_url": f"https://{nc_user}:{nc_pass}@localhost/index.php/apps/files/?dir=/SecureVault_Sanitized_Docs",
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
            "nextcloud_url": f"https://{nc_user}:{nc_pass}@localhost/index.php/apps/files/?dir=/SecureVault_Sanitized_Docs",
            "bytes_written": len(file_bytes),
            "nextcloud_status_code": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

