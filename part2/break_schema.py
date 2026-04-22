"""
╔══════════════════════════════════════════════╗
║  Part 2 — ทดลองพิเศษ: ส่งข้อมูลผิด Schema  ║
╚══════════════════════════════════════════════╝

เป้าหมาย: เห็นว่า Schema Registry ป้องกัน
          ข้อมูลผิดรูปแบบได้อย่างไร

รัน producer.py ปกติก่อน แล้วค่อยรัน file นี้
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
    "type": "record",
    "name": "Order",
    "namespace": "com.workshop",
    "fields": [
        {"name": "order_id",  "type": "int"},
        {"name": "item",      "type": "string"},
        {"name": "quantity",  "type": "int"},
        {"name": "price",     "type": "float"}
    ]
})

avro_serializer = AvroSerializer(sr_client, order_schema_str)
producer = Producer({
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
})

TOPIC = 'orders-avro'

# ══════════════════════════════════════════════════════════
# ทดลองที่ 1: ส่ง order_id เป็น string แทน int
# ══════════════════════════════════════════════════════════
print('🧪 ทดลองที่ 1: order_id เป็น string แทน int')
print('─' * 50)
wrong_order_1 = {
    "order_id": "abc",     # ❌ Schema บอกต้องเป็น int!
    "item": "pizza",
    "quantity": 2,
    "price": 250.0
}
try:
    avro_serializer(
        wrong_order_1,
        SerializationContext(TOPIC, MessageField.VALUE)
    )
    print('   ผ่าน (ไม่ควรเกิดขึ้น!)')
except Exception as e:
    print(f'   ❌ Error (คาดว่าจะเกิด): {type(e).__name__}')
    print(f'   📝 สาเหตุ: {e}')

print()

# ══════════════════════════════════════════════════════════
# ทดลองที่ 2: ลืมส่ง field 'price'
# ══════════════════════════════════════════════════════════
print('🧪 ทดลองที่ 2: ไม่มี field "price"')
print('─' * 50)
wrong_order_2 = {
    "order_id": 99,
    "item": "burger",
    "quantity": 1,
    # ❌ ลืม price!
}
try:
    avro_serializer(
        wrong_order_2,
        SerializationContext(TOPIC, MessageField.VALUE)
    )
    print('   ผ่าน (ไม่ควรเกิดขึ้น!)')
except Exception as e:
    print(f'   ❌ Error (คาดว่าจะเกิด): {type(e).__name__}')
    print(f'   📝 สาเหตุ: {e}')

print()

# ══════════════════════════════════════════════════════════
# ทดลองที่ 3: ส่ง field ที่ไม่มีใน Schema
# ══════════════════════════════════════════════════════════
print('🧪 ทดลองที่ 3: มี field "discount" ที่ไม่ได้อยู่ใน Schema')
print('─' * 50)
wrong_order_3 = {
    "order_id": 100,
    "item": "sushi",
    "quantity": 3,
    "price": 350.0,
    "discount": 10.0   # ❓ field นี้ไม่มีใน Schema จะเกิดอะไร?
}
try:
    serialized = avro_serializer(
        wrong_order_3,
        SerializationContext(TOPIC, MessageField.VALUE)
    )
    print('   ✅ ผ่าน! (Avro ยอมรับ field พิเศษ แต่จะถูก ignore ตอน deserialize)')
except Exception as e:
    print(f'   ❌ Error: {e}')

print()
print('─' * 50)
print('📚 สรุป: Schema Registry ช่วยป้องกัน type ผิดและ field ขาดหาย')
print('        แต่ field เกินจะถูก ignore โดยอัตโนมัติ')
