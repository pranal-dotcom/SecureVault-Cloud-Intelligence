# SecureVault: Zero-Trust Cloud Document Intelligence & PII Redaction Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker Multi-Container](https://img.shields.io/badge/Docker-Multi--Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Nextcloud WebDAV](https://img.shields.io/badge/Nextcloud-WebDAV_Vault-0082C9?style=for-the-badge&logo=nextcloud&logoColor=white)](https://nextcloud.com/)
[![Tesseract OCR](https://img.shields.io/badge/Tesseract_OCR-v5.x_Engine-5C8DBC?style=for-the-badge&logo=google&logoColor=white)](https://github.com/tesseract-ocr/tesseract)
[![Nginx WAF](https://img.shields.io/badge/Nginx-WAF_Perimeter-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)

---

### 🛡️ Core Value Proposition
**SecureVault** is an enterprise-grade, Zero-Trust document intelligence, privacy compliance, and cloud preservation platform. Built for strict regulatory and high-throughput environments (such as KYC intake, banking, and healthcare), SecureVault eliminates the risk of sensitive data exposure by decoupling document intake from an asynchronous, multi-threaded vCPU background compute engine. 

Incoming identity files and confidential payloads undergo sub-second optical character recognition (OCR), automated regulatory PII scrubbing, side-by-side privacy audits, and direct WebDAV cryptographic persistence into encrypted, tenant-isolated cloud storage vaults.

---

## 🏛️ The Three Cloud Architecture Pillars

SecureVault is engineered around three decoupled architectural pillars, guaranteeing high performance, complete tenant isolation, and defense-in-depth perimeter protection:

| Architecture Pillar | Core Technologies | Implementation & Engineering Responsibility |
| :--- | :--- | :--- |
| **Compute** | **FastAPI & Tesseract OCR Worker (`compute.py`)** | Asynchronous, decoupled background compute engine utilizing dynamic multi-thread vCPU scheduling (`os.cpu_count()`). Orchestrates sub-second rasterization, optical character extraction, high-precision regex token masking, and executive summary synthesis without blocking ingestion threads. |
| **Storage** | **Nextcloud (WebDAV) & MariaDB 10.6** | Tenant-isolated cloud vaults backed by ACID-compliant MariaDB metadata stores and Redis in-memory cache/file locking. Enforces enterprise storage assurance with AWS S3 Server-Side Encryption (SSE-KMS), immutable audit logs, and instant WebDAV synchronization. |
| **Networking** | **Nginx Reverse Proxy & WAF Perimeter** | High-performance reverse proxy enforcing TLSv1.2/TLSv1.3 cryptographic termination, OWASP regex-based inspection against SQLi, XSS, and directory traversal, aggressive auth-endpoint rate limiting, and zero-trust internal bridge network isolation (`securevault-net`). |

---

## 🔄 4-Stage Zero-Trust Pipeline Workflow

The SecureVault pipeline enforces strict Zero-Trust boundaries: documents are validated upon intake, processed entirely in decoupled container memory, sanitized before persistent storage, and verified with cryptographic integrity checks.

```text
┌────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│ 1. INTAKE      │ ──> │ 2. OCR EXTRACTION    │ ──> │ 3. PII SANITIZATION  │ ──> │ 4. VAULT COMMIT     │
│                │     │    & TELEMETRY       │     │    & INTELLIGENCE    │     │    & ASSURANCE      │
├────────────────┤     ├──────────────────────┤     ├──────────────────────┤     ├─────────────────────┤
│ • Strict MIME  │     │ • Tesseract v5 OCR   │     │ • Regex Token Mask   │     │ • WebDAV HTTP 201   │
│ • Task ID Gen  │     │ • Multi-Thread vCPU  │     │ • Dual Stream Audit  │     │ • SHA-256 Checksum  │
│ • HTTP 202     │     │ • Hardware Telemetry │     │ • Executive Summary  │     │ • SSE-KMS Encrypted │
└────────────────┘     └──────────────────────┘     └──────────────────────┘     └─────────────────────┘
```

### Detailed Pipeline Stages

* **Step 1: Upload Intake & Validation**
  * Ingests identity records, scans, and documents across supported formats (`PNG`, `JPG`, `PDF`, `TXT`).
  * Enforces MIME-type whitelisting, file integrity checks, and size thresholds.
  * Dispatches work to an asynchronous multi-process task store with SQLite WAL journaling and returns `HTTP 202 Accepted` with a deterministic `task_id`.

* **Step 2: OCR Text Extraction & Classification**
  * Tesseract OCR v5 engine dynamically allocates vCPU processing threads (`os.cpu_count()`) for high-speed rasterization and optical parsing.
  * Captures real-time execution telemetry including execution latency (in milliseconds), vCPU thread utilization, total word counts, and character densities.

* **Step 3: PII Redaction & AI Executive Intelligence**
  * High-precision tokenization engine identifies and scrubs sensitive regulatory identifiers, including Indian KYC entities:
    * **Indian Aadhaar**: 12-digit UIDAI format (`[REDACTED_AADHAAR]`)
    * **Permanent Account Number (PAN)**: 10-character alphanumeric tax ID (`[REDACTED_PAN]`)
    * **Payment Cards**: Visa, MasterCard, Amex, Discover (`[REDACTED_CREDIT_CARD]`)
    * **Email Addresses**: RFC compliant mail addresses (`[REDACTED_EMAIL]`)
    * **Phone Numbers**: Indian 10-digit mobile (+91) and international numbers (`[REDACTED_PHONE]`)
  * Generates an automated executive summary and renders a dual-panel, side-by-side stream comparison in the dashboard for compliance sign-off.

* **Step 4: Encrypted Vault Commit & Storage Assurance**
  * Directly synchronizes sanitized documents into the user's isolated Nextcloud storage via authenticated WebDAV API (`MKCOL` / `PUT`) at `/SecureVault_Sanitized_Docs/`.
  * Verifies server responses (`HTTP 201 Created` / `HTTP 204 No Content`) and triggers Nextcloud OCC background indexing.
  * Validates cryptographic SHA-256 integrity checksums and confirms AWS S3 SSE-KMS hardware encryption assurance.

---

## 📁 Repository Directory Structure

```text
SecureVault-Cloud-Intelligence/
├── .env.example                     # Production environment variable template
├── .env                             # Active environment secrets & KMS configurations
├── .gitignore                       # Git ignore rules for keys, certs, and volumes
├── Dockerfile.integration           # Container definition for automated test runner
├── docker-compose.yml               # Multi-container orchestration specification
├── README.md                        # Industry-grade architecture & deployment documentation
├── ai-service/                      # Autonomous AI Document Intelligence Microservice
│   ├── Dockerfile                   # Python 3.11-slim + Tesseract v5 OCR base image
│   ├── requirements.txt             # Service dependencies (FastAPI, PyTesseract, Pillow)
│   └── app/
│       ├── compute.py               # Asynchronous vCPU task engine & SQLite WAL store
│       ├── dashboard.py             # Interactive Dual-Panel UI & Telemetry Dashboard
│       ├── landing.py               # SaaS product landing page
│       ├── main.py                  # FastAPI application routes, WebDAV bridge, and API
│       ├── ocr.py                   # Tesseract optical character recognition worker
│       ├── pii.py                   # High-precision regulatory regex sanitization rules
│       ├── summarizer.py            # AI executive document summarizer
│       └── static/                  # Static assets and UI stylesheets
├── config/
│   └── s3.config.php                # Nextcloud Primary Storage S3 & SSE-KMS connector
├── nginx/                           # Perimeter Security & Reverse Proxy WAF
│   ├── nginx.conf                   # Main Nginx daemon configuration
│   ├── certbot/                     # Webroot directory for Let's Encrypt challenges
│   ├── certs/                       # Trusted local CA certificates (mkcert / dev)
│   ├── ssl/                         # Production SSL/TLS certificates (fullchain & privkey)
│   ├── html/                        # Custom branded WAF error templates (403 Forbidden)
│   └── conf.d/
│       └── nextcloud.conf           # VirtualHost, OWASP WAF rules, WebDAV and API routing
└── scripts/                         # Operational, Security & Test Automation Suites
    ├── attack_simulation.py         # Automated WAF validation (SQLi, XSS, Path Traversal)
    ├── entrypoint.sh                # Container initialization & wait-for-health script
    ├── setup_aws_s3_kms.ps1         # PowerShell deployment script for AWS S3 & KMS
    ├── setup_aws_s3_kms.sh          # Bash deployment script for AWS S3 & KMS
    └── test_ai_service.py           # Verification suite for OCR, PII masking, and WebDAV
```

---

## 🔒 Container Architecture & Security Matrix

SecureVault enforces defense-in-depth across every container boundary. Services run on an isolated bridge network with no direct host port exposure for databases or backend APIs.

| Service | Base Image | Security Hardening & Implementation |
| :--- | :--- | :--- |
| **`ai-service`** | `python:3.11-slim` | Isolated FastAPI microservice executing asynchronous vCPU tasks. Protected by an internal SQLite WAL task queue, strict MIME-type whitelisting, read-only application code mounting (`./ai-service/app:/app/app:ro`), and zero host port publication (traffic accessible solely via internal reverse proxy). |
| **`nextcloud`** | `nextcloud:apache` | Enterprise cloud storage server configured with tenant isolation, brute-force IP throttling, strict Content Security Policy (CSP), secure cookie flags (`HttpOnly`, `SameSite=Lax`, `Secure`), S3 SSE-KMS hardware encryption assurance, and transactional locking via Redis. |
| **`db`** | `mariadb:10.6` | Relational database restricted exclusively to the internal container bridge (`securevault-net`). Hardened with `READ-COMMITTED` transaction isolation, `utf8mb4_unicode_ci` collation, row-based binary logging, and isolated named volume storage (`db_data`). |
| **`redis`** | `redis:alpine` | High-throughput in-memory cache and transactional file lock manager. Hardened with mandatory authentication (`--requirepass`), LRU eviction policy (`--maxmemory-policy allkeys-lru`), and strictly bound to internal container network traffic. |
| **`reverse-proxy`** | `nginx:alpine` | Perimeter WAF and TLS termination gateway. Enforces TLSv1.2/1.3 cipher suites, OWASP-aligned regex filtering against SQLi, XSS, and directory traversal, aggressive login route rate-limiting (`burst=3 nodelay`), HSTS preloading, and custom 403 error masking. |
| **`securevault-net`** | `bridge` (driver) | Dedicated user-defined Docker bridge network isolating backend communication. Prevents untrusted ingress into internal microservices, enforcing all external interactions to traverse the Nginx reverse proxy. |

---

## 🚀 Quick Start Deployment Guide

### Prerequisites
* **Docker Desktop** (v24.0+ with Docker Compose v2)
* **Git** (v2.30+)
* **OpenSSL** or **PowerShell 5.1+** (for SSL/TLS certificate generation)

---

### Step 1: Clone the Repository & Configure Environment

Clone the repository and initialize the production environment file:

```bash
git clone https://github.com/pranal-dotcom/SecureVault-Cloud-Intelligence.git
cd SecureVault-Cloud-Intelligence
cp .env.example .env
```

Edit `.env` to configure your passwords and domain preferences:
```ini
DOMAIN_NAME=localhost
OVERWRITEHOST=localhost
OVERWRITEPROTOCOL=https

# MariaDB Credentials
MYSQL_ROOT_PASSWORD=YourStrongRootPasswordHere123!
MYSQL_PASSWORD=YourStrongDatabasePasswordHere123!

# Redis Cache Security
REDIS_HOST_PASSWORD=YourStrongRedisPasswordHere123!

# Nextcloud Admin Account
NEXTCLOUD_ADMIN_USER=admin
NEXTCLOUD_ADMIN_PASSWORD=YourStrongAdminPasswordHere123!
```

---

### Step 2: Generate Local SSL/TLS Certificates

SecureVault requires HTTPS. Generate trusted local certificates before starting the stack:

#### Option A: Windows PowerShell (Self-Signed)
```powershell
# Create certificates directory if not present
New-Item -ItemType Directory -Force -Path "nginx\ssl"

# Generate self-signed certificate and export
$cert = New-SelfSignedCertificate -DnsName "localhost", "127.0.0.1" -CertStoreLocation "Cert:\CurrentUser\My" -NotAfter (Get-Date).AddYears(1)
Export-Certificate -Cert $cert -FilePath "nginx\ssl\fullchain.pem"
```

#### Option B: OpenSSL / Linux / macOS
```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/privkey.pem \
  -out nginx/ssl/fullchain.pem \
  -subj "/CN=localhost"
```

---

### Step 3: Build & Launch Microservices

Build container images and start all services in detached mode:

```bash
docker compose up -d --build
```

Verify that all containers are running and healthy:

```bash
docker compose ps
```

---

### Step 4: Access Platform Endpoints

Once the health checks pass, access the SecureVault services:

| Service / Interface | URL Endpoint | Description |
| :--- | :--- | :--- |
| **SaaS Landing Page** | [https://localhost/](https://localhost/) | Public architectural overview and platform features |
| **Intelligence Dashboard** | [https://localhost/dashboard](https://localhost/dashboard) | Interactive dual-panel document scanner, OCR & PII audit interface |
| **FastAPI Swagger Docs** | [https://localhost/ai-api/docs](https://localhost/ai-api/docs) | Interactive OpenAPI documentation for compute and ingestion APIs |
| **Nextcloud Cloud Vault** | [https://localhost/index.php/login](https://localhost/index.php/login) | Tenant-isolated encrypted cloud storage repository |

---

## 🛠️ Operational Maintenance Commands

### 1. Rebuilding the AI Service Microservice
After making changes to Python source code in `ai-service/`:
```bash
docker compose build ai-service
docker compose up -d ai-service
```

### 2. Monitoring Real-Time Worker Logs
Stream container logs with timestamps:
```bash
# Monitor AI worker & compute tasks
docker compose logs -f ai-service

# Monitor Reverse Proxy & WAF events
docker compose logs -f reverse-proxy

# Monitor Nextcloud application server
docker compose logs -f nextcloud
```

### 3. Nextcloud OCC CLI Management
Execute administrative commands inside the Nextcloud container:
```bash
# Check Nextcloud installation status
docker compose exec -u www-data nextcloud php occ status

# Trigger an index scan across all user directories
docker compose exec -u www-data nextcloud php occ files:scan --all

# Add missing database indices for optimal performance
docker compose exec -u www-data nextcloud php occ db:add-missing-indices
```

### 4. Running the Verification & Attack Test Suite
Validate API functionality, OCR ingestion, PII redaction, and WAF security filters:
```bash
# Run standalone Python test verification suite
python scripts/test_ai_service.py

# Run containerized integration tests on securevault-net
docker compose --profile test run --rm integration-tests
```

### 5. Graceful Stack Shutdown & Maintenance
```bash
# Stop containers while preserving all data volumes
docker compose stop

# Tear down containers and internal networks
docker compose down

# Full wipe including persistent volumes (CAUTION: wipes database and vaults)
docker compose down -v
```

---

## 🔮 Future Roadmap & Enhancements

* **Phase 2: Interactive Zero-Trust Document Intelligence Chatbot**
  * Local, privacy-preserving Retrieval-Augmented Generation (RAG) powered by **Ollama / Llama 3**.
  * Embedded vector search utilizing **pgvector** or **ChromaDB** to enable natural-language Q&A across sanitized vault documents.
  * Strict in-memory execution guardrails ensuring confidential context never leaves the perimeter.
* **Multi-Modal Redaction Pipeline**
  * **Audio Redaction Engine**: Automatic PII identification in customer service calls and dictations using **Whisper ASR**, featuring acoustic tone-bleeping for sensitive credentials.
  * **Video PII Masking**: Real-time bounding-box blurring for biometric faces, government identity cards, and screens detected across video KYC sessions.
* **Enterprise Identity Federation & Custom Compliance**
  * Full SAML 2.0 / OpenID Connect (OIDC) single sign-on integration for Okta, Azure Active Directory, and PingFederate.
  * User-definable compliance regex rules supporting HIPAA (medical records), GDPR (EU privacy identifiers), and India's Digital Personal Data Protection (DPDP) Act 2023.

---

## 🔗 Repository & Community

* **GitHub Repository**: [pranal-dotcom/SecureVault-Cloud-Intelligence](https://github.com/pranal-dotcom/SecureVault-Cloud-Intelligence)
* **License**: Proprietary / Open-Source Cloud Security Reference Implementation
* **Maintainer**: SecureVault Engineering Team
