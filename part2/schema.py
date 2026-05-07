"""
╔══════════════════════════════════════════════╗
║  Workshop Part 2 — Step 1: schema.py         ║
║  กำหนด Avro Schema และ Register เข้า        ║
║  Schema Registry                             ║
╚══════════════════════════════════════════════╝

ชนิดข้อมูลใน Avro:
  "string"  → ข้อความ
  "int"     → จำนวนเต็ม
  "float"   → ทศนิยม
  "boolean" → true / false
"""
import os
import json
import requests

SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')


# ════════════════════════════════════════════════
# TODO 1: เติม type ของแต่ละ field ให้ถูกต้อง
#
#   order_id  → จำนวนเต็ม
#   item      → ข้อความ
#   quantity  → จำนวนเต็ม
#   price     → ทศนิยม
# ════════════════════════════════════════════════
order_schema = {
    "type": "record",
    "name": "Order",
    "namespace": "com.workshop",
    "fields": [
        {"name": "order_id",  "type": ______},  # 👈 เติมที่นี่
        {"name": "item",      "type": ______},  # 👈 เติมที่นี่
        {"name": "quantity",  "type": ______},  # 👈 เติมที่นี่
        {"name": "price",     "type": ______},  # 👈 เติมที่นี่
    ]
}


# ════════════════════════════════════════════════
# TODO 2: กำหนดชื่อ subject
#         ปกติใช้ชื่อ topic ตามด้วย "-value"
#         เช่น topic 'orders-avro' → subject 'orders-avro-value'
# ════════════════════════════════════════════════
subject = ______  # 👈 เติมที่นี่


# ─── Register Schema ─────────────────────────────────────────
print(f'📤 กำลัง Register Schema สำหรับ subject: {subject}')

response = requests.post(
    f'{SCHEMA_REGISTRY_URL}/subjects/{subject}/versions',
    headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'},
    json={"schema": json.dumps(order_schema)}
)

if response.status_code == 200:
    print(f'✅ Register สำเร็จ! Schema ID = {response.json()["id"]}')
else:
    print(f'❌ Register ล้มเหลว: {response.text}')

# แสดง Schema ทั้งหมดที่มี
print('\n📋 Schema ที่มีใน Registry:')
for s in requests.get(f'{SCHEMA_REGISTRY_URL}/subjects').json():
    print(f'   • {s}')
