"""
╔══════════════════════════════════════════════╗
║  Part 2 — Workshop: Register Avro Schema     ║
║  เติมโค้ดในส่วนที่มี TODO ให้ครบ            ║
╚══════════════════════════════════════════════╝

Avro Schema คือ "สัญญา" ที่บอกว่าข้อมูลใน Topic
ต้องมีหน้าตาเป็นแบบนี้เท่านั้น

ชนิดข้อมูลที่ใช้บ่อยใน Avro:
  "string"  → ข้อความ
  "int"     → จำนวนเต็ม
  "float"   → จำนวนทศนิยม
  "boolean" → true / false
"""
import os
import json
import requests

SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')


# ════════════════════════════════════════════════
# TODO 1: เติม type ของแต่ละ field ให้ถูกต้อง
#
#   order_id  → จำนวนเต็ม (เช่น 1, 2, 3)
#   item      → ข้อความ (เช่น "pizza")
#   quantity  → จำนวนเต็ม (เช่น 2)
#   price     → ทศนิยม (เช่น 250.0)
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
#         เช่น ถ้า topic ชื่อ 'orders-avro' → subject คือ 'orders-avro-value'
# ════════════════════════════════════════════════
subject = ______  # 👈 เติมที่นี่


# ─── Register Schema เข้า Schema Registry ────────────────────
print(f'📤 กำลัง Register Schema สำหรับ subject: {subject}')

response = requests.post(
    f'{SCHEMA_REGISTRY_URL}/subjects/{subject}/versions',
    headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'},
    json={"schema": json.dumps(order_schema)}
)

if response.status_code == 200:
    schema_id = response.json()['id']
    print(f'✅ Register สำเร็จ! Schema ID = {schema_id}')
else:
    print(f'❌ Register ล้มเหลว: {response.text}')


# ─── ดู Schema ที่ Register ไว้ทั้งหมด ───────────────────────
print('\n📋 Schema ที่มีใน Registry ทั้งหมด:')
all_subjects = requests.get(f'{SCHEMA_REGISTRY_URL}/subjects').json()
for s in all_subjects:
    print(f'   • {s}')
