#!/usr/bin/env python3
"""
SecureVault: Autonomous AI Document Intelligence Engine Verification Suite
Phase 4: OCR, PII Identification & Redaction, and Summarization Testing

Verifies:
1. AI Service Health Endpoint (/ai-api/health)
2. Direct Text Payload Analysis with Indian KYC & Financial PII Redaction
3. Document Upload with OCR (Image/PDF) -> PII Redaction -> Summarization
"""

import io
import sys
import json
import urllib3
import requests
from PIL import Image, ImageDraw, ImageFont

# Suppress InsecureRequestWarning for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ANSI Colors
class Colors:
    HEADER    = '\033[95m'
    BLUE      = '\033[94m'
    CYAN      = '\033[96m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    BOLD      = '\033[1m'
    RESET     = '\033[0m'

AI_BASE_URL = "https://localhost/ai-api"

def print_header(title: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 75}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN} {title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 75}{Colors.RESET}")

def log_result(test_name: str, passed: bool, status_code: int, expected: str, details: str = ""):
    status_color = Colors.GREEN if passed else Colors.RED
    status_text = "[ PASSED ]" if passed else "[ FAILED ]"
    print(f"{Colors.BOLD}{status_color}{status_text}{Colors.RESET} {Colors.BOLD}{test_name}{Colors.RESET}")
    print(f"         Status Code : {status_color}{status_code}{Colors.RESET} (Expected: {expected})")
    if details:
        print(f"         Details     : {details}")
    print(f"         {'-' * 70}")

def generate_sample_kyc_image() -> bytes:
    """Generates an in-memory test image containing sample text for OCR verification."""
    img = Image.new("RGB", (800, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    lines = [
        "SECUREVAULT CONFIDENTIAL KYC VERIFICATION REPORT",
        "Customer Name: Priya Sharma",
        "Aadhaar Number: 4589 7812 3456",
        "PAN Card: ABCDE9876Z",
        "Contact Email: priya.sharma@cloudvault.internal",
        "Mobile Number: +91 9876543210",
        "Account Status: Fully Verified and Encrypted with KMS."
    ]

    y_pos = 40
    for line in lines:
        draw.text((40, y_pos), line, fill=(0, 0, 0))
        y_pos += 45

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def run_ai_tests():
    print_header("SecureVault Phase 4: AI Document Intelligence Engine Test Suite")
    print(f"Target Base URL: {Colors.BOLD}{AI_BASE_URL}{Colors.RESET}\n")

    session = requests.Session()
    session.verify = False

    results = []

    # --------------------------------------------------------------------------
    # Test 1: Microservice Health Check
    # --------------------------------------------------------------------------
    t1_name = "Test 1: AI Service Health Check (/ai-api/health)"
    try:
        r1 = session.get(f"{AI_BASE_URL}/health", timeout=10)
        data1 = r1.json() if r1.status_code == 200 else {}
        passed1 = (r1.status_code == 200 and data1.get("status") == "healthy")
        log_result(
            t1_name,
            passed1,
            r1.status_code,
            "200 OK (status: healthy)",
            f"Service: '{data1.get('service')}', Modules: {data1.get('modules')}"
        )
        results.append((t1_name, passed1))
    except Exception as e:
        log_result(t1_name, False, 0, "200 OK", f"Error: {e}")
        results.append((t1_name, False))

    # --------------------------------------------------------------------------
    # Test 2: PII Redaction & Summarization on Indian KYC & Financial Record
    # --------------------------------------------------------------------------
    t2_name = "Test 2: Zero-Trust PII Redaction (Aadhaar, PAN, CC, Email, Phone)"
    sample_text = (
        "CONFIDENTIAL AUDIT REPORT: SecureVault Client Onboarding.\n"
        "Applicant Rajesh Kumar provided Aadhaar card number 5489 1234 5678 and PAN ABCDE1234F for verification. "
        "Official communication was sent to rajesh.sharma@example.com and mobile +91 9876543210. "
        "The primary billing payment was charged to corporate Visa credit card 4532-1234-5678-9012. "
        "All transactions have been secured via AWS KMS and validated by the compliance team."
    )

    try:
        r2 = session.post(
            f"{AI_BASE_URL}/analyze",
            data={"text": sample_text},
            timeout=15
        )
        data2 = r2.json() if r2.status_code == 200 else {}
        pii_sum = data2.get("pii_summary", {})
        categories = pii_sum.get("categories", {})
        redacted = data2.get("redacted_text", "")

        # Verify all 5 PII types detected and redacted
        has_aadhaar = "[REDACTED_AADHAAR]" in redacted and categories.get("AADHAAR", 0) >= 1
        has_pan = "[REDACTED_PAN]" in redacted and categories.get("PAN", 0) >= 1
        has_email = "[REDACTED_EMAIL]" in redacted and categories.get("EMAIL", 0) >= 1
        has_phone = "[REDACTED_PHONE]" in redacted and categories.get("PHONE", 0) >= 1
        has_cc = "[REDACTED_CREDIT_CARD]" in redacted and categories.get("CREDIT_CARD", 0) >= 1

        all_pii_passed = has_aadhaar and has_pan and has_email and has_phone and has_cc
        passed2 = (r2.status_code == 200 and all_pii_passed)

        detail_msg = (
            f"Detected PII Categories: {categories}\n"
            f"         Redacted Text Snippet: {redacted[:140]}...\n"
            f"         Executive Summary: {data2.get('summary', {}).get('executive_summary', '')}"
        )
        log_result(t2_name, passed2, r2.status_code, "200 OK (All 5 PII entities redacted)", detail_msg)
        results.append((t2_name, passed2))
    except Exception as e:
        log_result(t2_name, False, 0, "200 OK", f"Error: {e}")
        results.append((t2_name, False))

    # --------------------------------------------------------------------------
    # Test 3: Document Upload with OCR -> PII -> Summary Pipeline
    # --------------------------------------------------------------------------
    t3_name = "Test 3: File Upload & Tesseract OCR Pipeline (/ai-api/analyze)"
    try:
        test_img_bytes = generate_sample_kyc_image()
        files = {
            "file": ("sample_kyc_document.png", test_img_bytes, "image/png")
        }

        r3 = session.post(
            f"{AI_BASE_URL}/analyze",
            files=files,
            timeout=25
        )
        data3 = r3.json() if r3.status_code == 200 else {}
        extracted_text = data3.get("original_text", "")
        ocr_redacted = data3.get("redacted_text", "")
        summary3 = data3.get("summary", {})

        passed3 = (
            r3.status_code == 200
            and len(extracted_text) > 30
            and data3.get("status") == "success"
            and len(summary3.get("key_highlights", [])) > 0
        )

        detail_msg = (
            f"OCR Extracted Characters: {len(extracted_text)}\n"
            f"         Document Classification : {summary3.get('document_type')}\n"
            f"         Key Highlights Found    : {len(summary3.get('key_highlights', []))}\n"
            f"         OCR Redacted Preview    : {ocr_redacted.replace(chr(10), ' ')[:120]}..."
        )
        log_result(t3_name, passed3, r3.status_code, "200 OK with OCR extracted text", detail_msg)
        results.append((t3_name, passed3))
    except Exception as e:
        log_result(t3_name, False, 0, "200 OK", f"Error: {e}")
        results.append((t3_name, False))

    # --------------------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------------------
    print_header("AI Document Intelligence Test Suite Summary")
    total = len(results)
    passed_count = sum(1 for _, p in results if p)

    for name, p in results:
        mark = f"{Colors.GREEN}[PASS]{Colors.RESET}" if p else f"{Colors.RED}[FAIL]{Colors.RESET}"
        print(f"  {mark} - {name}")

    print(f"\n{Colors.BOLD}Final Result: {passed_count}/{total} AI Intelligence Tests Passed.{Colors.RESET}")
    if passed_count == total:
        print(f"{Colors.BOLD}{Colors.GREEN}>> Autonomous AI Document Intelligence Engine is FULLY OPERATIONAL. <<{Colors.RESET}\n")
        return 0
    else:
        print(f"{Colors.BOLD}{Colors.RED}>> One or more AI service tests failed! <<{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_ai_tests())
