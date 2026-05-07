"""
╔══════════════════════════════════════════════╗
║  Workshop Part 2 — Step 4: break_schema.py   ║
║  🔥 ทดลองส่งข้อมูลผิด Schema               ║
║     ดู error ที่ Schema Registry ป้องกัน    ║
╚══════════════════════════════════════════════╝
"""
import os
import json
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

sr_client = SchemaRegistryClient({
    'url': os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')
})
order_schema_str = json.dumps({
    "type": "record", "name": "Order", "namespace": "com.workshop",
    "fields": [
        {"name": "order_id",  "type": "int"},
        {"name": "item",      "type": "string"},
        {"name": "quantity",  "type": "int"},
        {"name": "price",     "type": "float"}
    ]
})
avro_serializer = AvroSerializer(sr_client, order_schema_str)
TOPIC = 'orders-avro'


def try_send(label, data):
    print(f'\n🧪 {label}')
    print(f'   ข้อมูล: {data}')
    print('   ' + '─' * 45)
    try:
        avro_serializer(data, SerializationContext(TOPIC, MessageField.VALUE))
        print('   ⚠️  ผ่าน (ไม่ควรเกิดขึ้น!)')
    except Exception as e:
        print(f'   ❌ Error: {type(e).__name__}')
        print(f'   📝 {e}')


# ── ทดลองที่ 1: ส่ง order_id เป็น string แทน int ────────────
try_send(
    'ทดลองที่ 1: order_id เป็น string แทน int',
    {"order_id": "abc", "item": "pizza", "quantity": 2, "price": 250.0}
)

# ── ทดลองที่ 2: ขาด field 'price' ────────────────────────────
try_send(
    'ทดลองที่ 2: ไม่มี field "price"',
    {"order_id": 1, "item": "burger", "quantity": 1}
)

# ── ทดลองที่ 3: มี field ที่ไม่อยู่ใน Schema ─────────────────
try_send(
    'ทดลองที่ 3: มี field "discount" เกิน Schema',
    {"order_id": 2, "item": "sushi", "quantity": 3, "price": 350.0, "discount": 10.0}
)

print('\n' + '═' * 50)
print('📚 สรุป:')
print('   ✅ Type ผิด        → Schema Registry ปฏิเสธทันที')
print('   ✅ Field ขาด       → Schema Registry ปฏิเสธทันที')
print('   ⚠️  Field เกิน     → Avro ignore อัตโนมัติ (ไม่ error)')
