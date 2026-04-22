"""
╔══════════════════════════════════════════════╗
║  Part 2 — เฉลย: Register Avro Schema         ║
╚══════════════════════════════════════════════╝
"""
import os
import json
import requests

SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')

# ✅ เฉลย TODO 1
order_schema = {
    "type": "record",
    "name": "Order",
    "namespace": "com.workshop",
    "fields": [
        {"name": "order_id",  "type": "int"},
        {"name": "item",      "type": "string"},
        {"name": "quantity",  "type": "int"},
        {"name": "price",     "type": "float"},
    ]
}

# ✅ เฉลย TODO 2
subject = 'orders-avro-value'

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

print('\n📋 Schema ที่มีใน Registry ทั้งหมด:')
all_subjects = requests.get(f'{SCHEMA_REGISTRY_URL}/subjects').json()
for s in all_subjects:
    print(f'   • {s}')
