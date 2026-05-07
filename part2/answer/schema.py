"""เฉลย Part 2 — schema.py"""
import os, json, requests

SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')
order_schema = {
    "type": "record", "name": "Order", "namespace": "com.workshop",
    "fields": [
        {"name": "order_id",  "type": "int"},
        {"name": "item",      "type": "string"},
        {"name": "quantity",  "type": "int"},
        {"name": "price",     "type": "float"},
    ]
}
subject = 'orders-avro-value'
print(f'📤 Register: {subject}')
r = requests.post(f'{SCHEMA_REGISTRY_URL}/subjects/{subject}/versions',
    headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'},
    json={"schema": json.dumps(order_schema)})
print(f'✅ Schema ID = {r.json()["id"]}' if r.status_code == 200 else f'❌ {r.text}')
