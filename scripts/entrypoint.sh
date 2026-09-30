#!/bin/sh
# ==============================================================================
# SecureVault Integration Test Entrypoint
# Waits for the reverse-proxy & ai-service to be healthy inside Docker,
# then runs both test suites sequentially.
# ==============================================================================

AI_URL="${AI_BASE_URL:-https://reverse-proxy/ai-api/health}"
NC_URL="${NC_URL:-https://reverse-proxy/status.php}"

echo ""
echo "============================================================="
echo "  SecureVault Docker-Native Integration Test Runner"
echo "  Connecting via securevault-net internal network"
echo "============================================================="
echo ""

# Wait for the reverse proxy to be ready (up to 90s)
echo "[*] Waiting for reverse-proxy (Nginx) to become ready..."
for i in $(seq 1 18); do
    STATUS=$(curl -sk -o /dev/null -w "%{http_code}" "$NC_URL" 2>/dev/null)
    if [ "$STATUS" = "200" ] || [ "$STATUS" = "302" ] || [ "$STATUS" = "301" ]; then
        echo "[OK] reverse-proxy is healthy (HTTP $STATUS)"
        break
    fi
    echo "    Attempt $i/18: HTTP $STATUS — retrying in 5s..."
    sleep 5
done

# Wait for the AI service to be ready (up to 60s)
echo "[*] Waiting for ai-service (FastAPI) to become ready..."
for i in $(seq 1 12); do
    STATUS=$(curl -sk -o /dev/null -w "%{http_code}" "$AI_URL" 2>/dev/null)
    if [ "$STATUS" = "200" ]; then
        echo "[OK] ai-service is healthy (HTTP $STATUS)"
        break
    fi
    echo "    Attempt $i/12: HTTP $STATUS — retrying in 5s..."
    sleep 5
done

echo ""
echo "============================================================="
echo "  PHASE 1: AI Document Intelligence Integration Tests"
echo "============================================================="
python test_ai_service.py
AI_EXIT=$?

echo ""
echo "============================================================="
echo "  PHASE 2: WAF & Perimeter Defense Security Tests"
echo "============================================================="
python attack_simulation.py
WAF_EXIT=$?

echo ""
echo "============================================================="
echo "  FINAL RESULT"
echo "============================================================="
if [ $AI_EXIT -eq 0 ] && [ $WAF_EXIT -eq 0 ]; then
    echo "  [ALL PASSED] All Docker-native integration tests succeeded."
    exit 0
else
    echo "  [FAILURES DETECTED] AI=$AI_EXIT  WAF=$WAF_EXIT"
    exit 1
fi
