"""
╔══════════════════════════════════════════════╗
║  Part 2 — เฉลย: Avro Producer                ║
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

# ✅ เฉลย TODO 1
avro_serializer = AvroSerializer(sr_client, order_schema_str)

producer = Producer({
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
})

TOPIC = 'orders-avro'

# ✅ เฉลย TODO 2
orders = [
    {"order_id": 1, "item": "pizza",  "quantity": 2, "price": 250.0},
    {"order_id": 2, "item": "burger", "quantity": 1, "price": 120.0},
    {"order_id": 3, "item": "sushi",  "quantity": 3, "price": 350.0},
]


def on_delivery(err, msg):
    if err:
        print(f'❌ ส่งไม่สำเร็จ: {err}')
    else:
        print(f'✅ ส่งสำเร็จ! offset={msg.offset()}')


print(f'📤 กำลังส่งข้อมูล Avro ไปยัง topic: {TOPIC}\n')

for order in orders:
    # ✅ เฉลย TODO 3
    producer.produce(
        topic=TOPIC,
        value=avro_serializer(
            order,
            SerializationContext(TOPIC, MessageField.VALUE)
        ),
        callback=on_delivery
    )
    print(f'   📦 ส่ง: {order}')

producer.flush()
print('\n🎉 ส่งข้อมูล Avro ครบแล้ว!')
