#!/bin/bash
# ╔══════════════════════════════════════════════════════╗
# ║  check.sh — ตรวจสอบ environment ก่อนเริ่ม Workshop  ║
# ╚══════════════════════════════════════════════════════╝

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

PASS=0
FAIL=0

ok()   { echo -e "  ${GREEN}✅ $1${NC}"; ((PASS++)); }
fail() { echo -e "  ${RED}❌ $1${NC}"; ((FAIL++)); }
warn() { echo -e "  ${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "  ${CYAN}ℹ️  $1${NC}"; }

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Kafka Workshop — Environment Check         ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""

# ── 1. Python ──────────────────────────────────────────────
echo -e "${BOLD}1. Python${NC}"
if command -v python3 &>/dev/null; then
  PY_VER=$(python3 --version 2>&1)
  ok "Python พร้อมใช้: $PY_VER"
else
  fail "ไม่พบ python3 — กรุณาติดตั้งก่อน"
fi

# ── 2. pip packages ────────────────────────────────────────
echo ""
echo -e "${BOLD}2. Python Packages${NC}"
for pkg in "confluent_kafka" "confluent_kafka.schema_registry" "requests"; do
  if python3 -c "import $pkg" 2>/dev/null; then
    ok "$pkg"
  else
    fail "$pkg ยังไม่ได้ติดตั้ง → รัน: pip install -r requirements.txt"
  fi
done

# ── 3. Kafka connectivity ──────────────────────────────────
echo ""
echo -e "${BOLD}3. Kafka Broker${NC}"
KAFKA_HOST="${KAFKA_BOOTSTRAP_SERVERS:-kafka:29092}"
HOST=$(echo $KAFKA_HOST | cut -d: -f1)
PORT=$(echo $KAFKA_HOST | cut -d: -f2)

if timeout 3 bash -c "echo > /dev/tcp/$HOST/$PORT" 2>/dev/null; then
  ok "Kafka เชื่อมต่อได้ที่ $KAFKA_HOST"
else
  fail "ไม่สามารถเชื่อมต่อ Kafka ที่ $KAFKA_HOST"
  info "ลอง: docker-compose up -d && bash check.sh"
fi

# ── 4. Schema Registry connectivity ───────────────────────
echo ""
echo -e "${BOLD}4. Schema Registry${NC}"
SR_URL="${SCHEMA_REGISTRY_URL:-http://schema-registry:8081}"
if curl -sf "$SR_URL/subjects" -o /dev/null 2>/dev/null; then
  ok "Schema Registry เชื่อมต่อได้ที่ $SR_URL"
  SUBJECTS=$(curl -sf "$SR_URL/subjects" 2>/dev/null || echo "[]")
  info "Subjects ที่มีอยู่: $SUBJECTS"
else
  fail "ไม่สามารถเชื่อมต่อ Schema Registry ที่ $SR_URL"
  info "ลอง: docker-compose up -d && bash check.sh"
fi

# ── 5. Docker services ────────────────────────────────────
echo ""
echo -e "${BOLD}5. Docker Services${NC}"
if command -v docker &>/dev/null; then
  for svc in "kafka" "schema-registry" "zookeeper"; do
    if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "$svc"; then
      ok "container '$svc' กำลังรัน"
    else
      warn "container '$svc' ไม่พบ หรือยังไม่ได้รัน"
    fi
  done
else
  warn "ไม่พบ docker — ข้ามการตรวจสอบ containers"
fi

# ── 6. Workshop files ─────────────────────────────────────
echo ""
echo -e "${BOLD}6. Workshop Files${NC}"
files=(
  "part1/producer.py"
  "part1/consumer.py"
  "part2/schema.py"
  "part2/producer.py"
  "part2/consumer.py"
  "part2/break_schema.py"
)
for f in "${files[@]}"; do
  if [ -f "$f" ]; then
    ok "$f"
  else
    fail "$f ไม่พบ"
  fi
done

# ── Summary ───────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════╗${NC}"
if [ "$FAIL" -eq 0 ]; then
  echo -e "${BOLD}${GREEN}║   ✅ พร้อมเริ่ม Workshop! ($PASS/$((PASS+FAIL)) ผ่าน)          ║${NC}"
else
  echo -e "${BOLD}${RED}║   ❌ ยังไม่พร้อม ($FAIL ข้อที่ต้องแก้ไข)         ║${NC}"
fi
echo -e "${BOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo -e "${YELLOW}แก้ไขปัญหาด้วยคำสั่งเหล่านี้:${NC}"
  echo "  docker-compose up -d        # เริ่ม Kafka + Schema Registry"
  echo "  pip install -r requirements.txt  # ติดตั้ง Python packages"
  echo "  bash check.sh               # ตรวจสอบอีกครั้ง"
  echo ""
  exit 1
fi

exit 0
