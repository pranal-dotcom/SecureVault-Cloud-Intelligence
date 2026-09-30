#!/usr/bin/env python3
"""
SecureVault: Automated Penetration & Attack Simulation Suite
Phase 3: Perimeter Defense & WAF Simulation Verification

Tests the Nginx Reverse Proxy WAF rules, Rate Limiting, and Security Headers
against OWASP attack patterns.
"""

import sys
import time
import urllib3
import requests

# Suppress InsecureRequestWarning for self-signed development certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ANSI Color Codes for Terminal Output
class Colors:
    HEADER    = '\033[95m'
    BLUE      = '\033[94m'
    CYAN      = '\033[96m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET     = '\033[0m'

import os
TARGET_BASE = f"https://{os.environ.get('SECUREVAULT_HOST', 'localhost')}"

def print_header(title: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 75}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN} {title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 75}{Colors.RESET}")

def log_test_result(test_name: str, passed: bool, status_code: int, expected: str, detail: str = ""):
    status_color = Colors.GREEN if passed else Colors.RED
    status_text = "[ PASSED ]" if passed else "[ FAILED ]"
    print(f"{Colors.BOLD}{status_color}{status_text}{Colors.RESET} {Colors.BOLD}{test_name}{Colors.RESET}")
    print(f"         Status Code : {status_color}{status_code}{Colors.RESET} (Expected: {expected})")
    if detail:
        print(f"         Details     : {detail}")
    print(f"         {'-' * 70}")

def run_tests():
    print_header("SecureVault Phase 3: Perimeter Defense & WAF Simulation Suite")
    print(f"Target URL: {Colors.BOLD}{TARGET_BASE}{Colors.RESET}\n")

    session = requests.Session()
    session.verify = False  # Ignore self-signed cert validation for local tests

    results = []

    # --------------------------------------------------------------------------
    # Test 1: Normal Legitimate Traffic
    # --------------------------------------------------------------------------
    test_1_name = "Test 1: Normal Legitimate Request (/status.php)"
    try:
        r1 = session.get(f"{TARGET_BASE}/status.php", timeout=5)
        passed_1 = (r1.status_code in (200, 301, 302))
        log_test_result(
            test_1_name,
            passed_1,
            r1.status_code,
            "200 OK or 301/302 Redirect",
            f"Headers returned: Content-Type='{r1.headers.get('Content-Type', '')}', HSTS='{r1.headers.get('Strict-Transport-Security', 'N/A')}'"
        )
        results.append((test_1_name, passed_1))
    except Exception as e:
        log_test_result(test_1_name, False, 0, "200/301/302", f"Connection Error: {e}")
        results.append((test_1_name, False))

    # --------------------------------------------------------------------------
    # Test 2: SQL Injection (SQLi) Attempt in Query Parameters
    # --------------------------------------------------------------------------
    test_2_name = "Test 2: SQL Injection Attack Detection (UNION SELECT / OR 1=1 / SLEEP)"
    sqli_payloads = [
        "id=1%20UNION%20SELECT%201,2,3,user(),password()",
        "search=admin'%20OR%201=1%20--",
        "category=books'%20AND%20SLEEP(5)%20--"
    ]
    passed_2 = True
    sub_results_2 = []
    for payload in sqli_payloads:
        try:
            r2 = session.get(f"{TARGET_BASE}/?{payload}", timeout=5)
            is_blocked = (r2.status_code == 403)
            sub_results_2.append(f"Payload '?{payload[:30]}...' -> HTTP {r2.status_code}")
            if not is_blocked:
                passed_2 = False
        except Exception as e:
            sub_results_2.append(f"Payload error: {e}")
            passed_2 = False

    log_test_result(
        test_2_name,
        passed_2,
        403 if passed_2 else 200,
        "403 Forbidden",
        "; ".join(sub_results_2)
    )
    results.append((test_2_name, passed_2))

    # --------------------------------------------------------------------------
    # Test 3: Cross-Site Scripting (XSS) Vector Payload
    # --------------------------------------------------------------------------
    test_3_name = "Test 3: Cross-Site Scripting (XSS) Vector Detection (<script> / onerror / js:)"
    xss_payloads = [
        "q=%3Cscript%3Ealert('XSS')%3C/script%3E",
        "redirect=javascript:alert(document.cookie)",
        "avatar=test.jpg%22%20onerror=%22alert(1)"
    ]
    passed_3 = True
    sub_results_3 = []
    for payload in xss_payloads:
        try:
            r3 = session.get(f"{TARGET_BASE}/?{payload}", timeout=5)
            is_blocked = (r3.status_code == 403)
            sub_results_3.append(f"Payload '?{payload[:30]}...' -> HTTP {r3.status_code}")
            if not is_blocked:
                passed_3 = False
        except Exception as e:
            sub_results_3.append(f"Payload error: {e}")
            passed_3 = False

    log_test_result(
        test_3_name,
        passed_3,
        403 if passed_3 else 200,
        "403 Forbidden",
        "; ".join(sub_results_3)
    )
    results.append((test_3_name, passed_3))

    # --------------------------------------------------------------------------
    # Test 4: Path Traversal & Sensitive File Probing
    # --------------------------------------------------------------------------
    test_4_name = "Test 4: Path Traversal & Sensitive File Access Interception"
    traversal_targets = [
        "/.env",
        "/etc/passwd",
        "/.git/config",
        "/index.php?file=../../../../etc/passwd"
    ]
    passed_4 = True
    sub_results_4 = []
    for target in traversal_targets:
        try:
            r4 = session.get(f"{TARGET_BASE}{target}", timeout=5)
            is_blocked = (r4.status_code == 403)
            sub_results_4.append(f"Target '{target}' -> HTTP {r4.status_code}")
            if not is_blocked:
                passed_4 = False
        except Exception as e:
            sub_results_4.append(f"Target error: {e}")
            passed_4 = False

    log_test_result(
        test_4_name,
        passed_4,
        403 if passed_4 else 200,
        "403 Forbidden",
        "; ".join(sub_results_4)
    )
    results.append((test_4_name, passed_4))

    # --------------------------------------------------------------------------
    # Test 5: Rapid Request Burst / Rate Limiting (DDoS / Brute Force Mitigation)
    # --------------------------------------------------------------------------
    test_5_name = "Test 5: Rate Limiting Enforcement (Burst Mitigation on /login)"
    burst_count = 25
    rate_limited_detected = False
    status_counts = {}

    print(f"{Colors.BOLD}{Colors.YELLOW}[*] Sending burst of {burst_count} rapid requests to '/login'...{Colors.RESET}")
    for i in range(burst_count):
        try:
            rb = session.get(f"{TARGET_BASE}/login", timeout=3)
            code = rb.status_code
            status_counts[code] = status_counts.get(code, 0) + 1
            if code in (429, 503):
                rate_limited_detected = True
        except Exception as e:
            status_counts['error'] = status_counts.get('error', 0) + 1

    log_test_result(
        test_5_name,
        rate_limited_detected,
        429 if rate_limited_detected else 200,
        "429 Too Many Requests (or 503)",
        f"Distribution across {burst_count} requests: {status_counts}"
    )
    results.append((test_5_name, rate_limited_detected))

    # --------------------------------------------------------------------------
    # Summary Report
    # --------------------------------------------------------------------------
    print_header("Perimeter Defense & WAF Simulation Summary")
    total_tests = len(results)
    passed_count = sum(1 for _, p in results if p)

    for name, p in results:
        mark = f"{Colors.GREEN}[PASS]{Colors.RESET}" if p else f"{Colors.RED}[FAIL]{Colors.RESET}"
        print(f"  {mark} - {name}")

    print(f"\n{Colors.BOLD}Final Result: {passed_count}/{total_tests} Security Tests Passed.{Colors.RESET}")
    if passed_count == total_tests:
        print(f"{Colors.BOLD}{Colors.GREEN}>> Zero-Trust Perimeter Defense & WAF rules are FULLY OPERATIONAL. <<{Colors.RESET}\n")
        return 0
    else:
        print(f"{Colors.BOLD}{Colors.RED}>> One or more WAF security tests failed! Check proxy logs. <<{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
