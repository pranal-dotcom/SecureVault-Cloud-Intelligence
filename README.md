# SecureVault - Production Nextcloud Cloud Intelligence Stack

A production-grade, highly secure, and performance-tuned Nextcloud deployment orchestrated with Docker Compose, MariaDB 10.6, Redis caching/locking, and an Nginx reverse proxy with SSL termination.

---

## 📁 Directory Structure

```text
SecureVault-Cloud-Intelligence/
├── .env.example                # Environment variable template
├── .env                        # Active environment secrets & configurations
├── docker-compose.yml          # Production multi-container orchestration
├── nginx/
│   ├── nginx.conf              # High-performance Nginx main configuration
│   ├── conf.d/
│   │   └── nextcloud.conf      # Virtual host, SSL parameters, proxy & WebDAV headers
│   ├── ssl/                    # SSL/TLS certificates (fullchain.pem, privkey.pem)
│   │   ├── fullchain.pem
│   │   └── privkey.pem
│   └── certbot/                # Webroot path for ACME / Let's Encrypt challenges
└── README.md                   # Operational & deployment documentation
```

---

## 🚀 Quick Start Deployment

### 1. Configure Environment Variables
Copy `.env.example` to `.env` (if not already done) and set your secure passwords and domain:
```bash
cp .env.example .env
```
Ensure you update:
- `DOMAIN_NAME` and `OVERWRITEHOST`
- `MYSQL_ROOT_PASSWORD` and `MYSQL_PASSWORD`
- `REDIS_HOST_PASSWORD`
- `NEXTCLOUD_ADMIN_PASSWORD`

---

### 2. Generate or Install SSL Certificates

#### Option A: Quick Self-Signed Certificate (for local development / testing)
**Linux / macOS / Git Bash:**
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/privkey.pem \
  -out nginx/ssl/fullchain.pem \
  -subj "/CN=localhost"
```

**Windows PowerShell:**
```powershell
New-SelfSignedCertificate -DnsName "localhost", "vault.example.com" -CertStoreLocation "cert:\LocalMachine\My"
# Or copy existing fullchain.pem and privkey.pem to .\nginx\ssl\
```

#### Option B: Let's Encrypt (Production)
Place your certificate and private key in `./nginx/ssl/fullchain.pem` and `./nginx/ssl/privkey.pem`.

---

### 3. Start the Stack
Launch all services in detached mode:
```bash
docker compose up -d
```

Check the status of all services:
```bash
docker compose ps
```

Monitor logs in real-time:
```bash
docker compose logs -f
```

---

## 🔒 Architecture & Security Highlights

| Service | Image | Purpose & Hardening |
| :--- | :--- | :--- |
| **`nextcloud`** | `nextcloud:apache` | Nextcloud application server with persistent HTML, config, apps, and data volumes. Pre-configured with Redis caching, transactional file locking, and memory limits. |
| **`db`** | `mariadb:10.6` | MariaDB configured with `utf8mb4_unicode_ci` 4-byte charset, `READ-COMMITTED` transaction isolation, and row-based binary logging. |
| **`redis`** | `redis:alpine` | Redis memory cache configured with LRU memory eviction policy and password authentication. |
| **`reverse-proxy`** | `nginx:alpine` | Nginx reverse proxy with HTTP→HTTPS redirect, TLS 1.2/1.3, HSTS, CalDAV/CardDAV redirection, and 10GB body upload limits with WebDAV streaming. |
| **`securevault-net`** | `bridge` | Isolated internal container network preventing external access to the database and Redis instances. |

---

## 🛠 Useful Maintenance Commands

- **Run Nextcloud OCC CLI:**
  ```bash
  docker compose exec --user www-data nextcloud php occ status
  ```

- **Perform Nextcloud Database Migration / Maintenance:**
  ```bash
  docker compose exec --user www-data nextcloud php occ db:add-missing-indices
  ```

- **Restart Services:**
  ```bash
  docker compose restart
  ```

- **Graceful Shutdown:**
  ```bash
  docker compose down
  ```
