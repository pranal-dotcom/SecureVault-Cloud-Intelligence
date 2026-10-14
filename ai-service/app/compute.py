import os
import time
import json
import sqlite3
import multiprocessing
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from app.ocr import process_document_ocr
from app.pii import detect_and_redact_pii
from app.summarizer import generate_summary

DB_PATH = os.environ.get("COMPUTE_DB_PATH", "/tmp/securevault_compute_tasks.db")

def _get_db():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn

def init_compute_db():
    """Initializes the multi-process SQLite task store for decoupled cloud compute telemetry."""
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    except Exception:
        pass
    with _get_db() as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS compute_tasks (
                task_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                stage TEXT NOT NULL,
                compute_duration_ms REAL NOT NULL,
                cpu_threads_used INTEGER NOT NULL,
                error TEXT,
                result TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        conn.commit()

def create_task(task_id: str) -> Dict[str, Any]:
    """Registers a new cloud compute task in QUEUED status."""
    init_compute_db()
    now = datetime.now(timezone.utc).isoformat()
    cpu_threads = os.cpu_count() or multiprocessing.cpu_count() or 2
    task = {
        "task_id": task_id,
        "status": "QUEUED",
        "stage": "OCR_EXTRACTION",
        "compute_duration_ms": 0.0,
        "cpu_threads_used": cpu_threads,
        "error": None,
        "result": None,
        "created_at": now,
        "updated_at": now
    }
    with _get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO compute_tasks 
            (task_id, status, stage, compute_duration_ms, cpu_threads_used, error, result, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_id,
            task["status"],
            task["stage"],
            task["compute_duration_ms"],
            task["cpu_threads_used"],
            None,
            None,
            now,
            now
        ))
        conn.commit()
    return task

def update_task_progress(
    task_id: str,
    status: str,
    stage: str,
    compute_duration_ms: float,
    error: Optional[str] = None,
    result: Optional[Dict[str, Any]] = None
):
    """Updates telemetry metrics and state for an active compute task."""
    now = datetime.now(timezone.utc).isoformat()
    result_json = json.dumps(result) if result is not None else None
    with _get_db() as conn:
        conn.execute("""
            UPDATE compute_tasks
            SET status = ?, stage = ?, compute_duration_ms = ?, error = ?, result = COALESCE(?, result), updated_at = ?
            WHERE task_id = ?
        """, (status, stage, compute_duration_ms, error, result_json, now, task_id))
        conn.commit()

def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves live telemetry metrics for a given compute task."""
    init_compute_db()
    with _get_db() as conn:
        row = conn.execute("SELECT * FROM compute_tasks WHERE task_id = ?", (task_id,)).fetchone()
        if not row:
            return None
        data = dict(row)
        if data.get("result"):
            try:
                data["result"] = json.loads(data["result"])
            except Exception:
                pass
        return data

def execute_cloud_compute_pipeline(
    task_id: str,
    file_bytes: Optional[bytes] = None,
    filename: str = "document.txt",
    content_type: Optional[str] = None,
    raw_text: Optional[str] = None,
    source_type: str = "file_upload"
):
    """
    Dedicated background worker function executing the cloud compute pipeline:
    1. Stage 'OCR_EXTRACTION' (Tesseract OCR on vCPU)
    2. Stage 'PII_SANITIZATION' (Zero-Trust Regex Masking & Summarization)
    3. Stage 'VAULT_SYNC' (Packaging for WebDAV Nextcloud commit)
    Status Transitions: QUEUED -> COMPUTING -> COMMITTED
    """
    t_start = time.perf_counter()
    cpu_threads = os.cpu_count() or multiprocessing.cpu_count() or 2

    try:
        # Step 1: Transition to COMPUTING (Stage: OCR_EXTRACTION)
        update_task_progress(
            task_id=task_id,
            status="COMPUTING",
            stage="OCR_EXTRACTION",
            compute_duration_ms=0.0
        )

        extracted_text = ""
        if file_bytes and len(file_bytes) > 0:
            extracted_text = process_document_ocr(file_bytes, filename, content_type)
        elif raw_text:
            extracted_text = raw_text.strip()

        t_ocr = time.perf_counter()
        ocr_duration_ms = round((t_ocr - t_start) * 1000, 2)

        # Step 2: Transition to Stage PII_SANITIZATION
        update_task_progress(
            task_id=task_id,
            status="COMPUTING",
            stage="PII_SANITIZATION",
            compute_duration_ms=ocr_duration_ms
        )

        if not extracted_text.strip():
            redacted_text = ""
            detected_entities = []
            category_counts = {}
            doc_summary = generate_summary("")
        else:
            redacted_text, detected_entities, category_counts = detect_and_redact_pii(extracted_text)
            doc_summary = generate_summary(redacted_text)

        t_pii = time.perf_counter()
        pii_duration_ms = round((t_pii - t_start) * 1000, 2)

        # Step 3: Transition to Stage VAULT_SYNC
        update_task_progress(
            task_id=task_id,
            status="COMPUTING",
            stage="VAULT_SYNC",
            compute_duration_ms=pii_duration_ms
        )

        t_end = time.perf_counter()
        total_duration_ms = round((t_end - t_start) * 1000, 2)

        result_payload = {
            "status": "success",
            "task_id": task_id,
            "filename": filename,
            "source_type": source_type,
            "original_text": extracted_text,
            "redacted_text": redacted_text,
            "pii_summary": {
                "total_redactions": len(detected_entities),
                "categories": category_counts,
                "entities": detected_entities
            },
            "summary": doc_summary,
            "compute_telemetry": {
                "task_id": task_id,
                "status": "COMMITTED",
                "stage": "VAULT_SYNC",
                "compute_duration_ms": total_duration_ms,
                "cpu_threads_used": cpu_threads,
                "completed_at": datetime.now(timezone.utc).isoformat()
            }
        }

        # Step 4: Final State COMMITTED
        update_task_progress(
            task_id=task_id,
            status="COMMITTED",
            stage="VAULT_SYNC",
            compute_duration_ms=total_duration_ms,
            result=result_payload
        )

    except Exception as e:
        elapsed_ms = round((time.perf_counter() - t_start) * 1000, 2)
        update_task_progress(
            task_id=task_id,
            status="FAILED",
            stage="FAILED",
            compute_duration_ms=elapsed_ms,
            error=str(e)
        )
