"""
╔══════════════════════════════════════════════╗
║  Part 2 — Workshop: Avro Producer            ║
║  เติมโค้ดในส่วนที่มี TODO ให้ครบ            ║
╚══════════════════════════════════════════════╝

⚠️  รัน schema.py ก่อน เพื่อ Register Schema ไว้ก่อน
"""
import os
import json
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

# ─── เชื่อมต่อ Schema Registry ───────────────────────────────
sr_client = SchemaRegistryClient({
    'url': os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')
})

# ─── กำหนด Avro Schema (ต้องตรงกับที่ Register ไว้ใน schema.py) ─
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


# ════════════════════════════════════════════════
# TODO 1: สร้าง AvroSerializer
#         ต้องการ 2 arguments: sr_client และ order_schema_str
# ════════════════════════════════════════════════
avro_serializer = AvroSerializer(______, ______)  # 👈 เติมที่นี่


producer = Producer({
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
})

TOPIC = 'orders-avro'


# ════════════════════════════════════════════════
# TODO 2: เติมข้อมูล order ให้ครบทุก field
#         order_id  → int    เช่น 1
#         item      → string เช่น "pizza"
#         quantity  → int    เช่น 2
#         price     → float  เช่น 250.0
#
# ⚠️  ชื่อ key ต้องตรงกับ Schema ทุกตัว!
# ════════════════════════════════════════════════
orders = [
    {"order_id": ______, "item": ______, "quantity": ______, "price": ______},  # 👈 เติม
    {"order_id": ______, "item": ______, "quantity": ______, "price": ______},  # 👈 เติม
    {"order_id": ______, "item": ______, "quantity": ______, "price": ______},  # 👈 เติม
]


# ─── ส่งข้อมูลผ่าน Avro Serializer ──────────────────────────
def on_delivery(err, msg):
    if err:
        print(f'❌ ส่งไม่สำเร็จ: {err}')
    else:
        print(f'✅ ส่งสำเร็จ! offset={msg.offset()}')


print(f'📤 กำลังส่งข้อมูล Avro ไปยัง topic: {TOPIC}\n')

for order in orders:
    # ════════════════════════════════════════════════
    # TODO 3: เติม value= โดยผ่าน avro_serializer
    #         avro_serializer รับ 2 arguments:
    #           1. ข้อมูล (dict) ที่ต้องการส่ง
    #           2. SerializationContext(TOPIC, MessageField.VALUE)
    # ════════════════════════════════════════════════
    producer.produce(
        topic=TOPIC,
        value=avro_serializer(
            ______,  # 👈 เติม: ตัวแปร order
            SerializationContext(TOPIC, MessageField.VALUE)
        ),
        callback=on_delivery
    )
    print(f'   📦 ส่ง: {order}')

producer.flush()
print('\n🎉 ส่งข้อมูล Avro ครบแล้ว!')
