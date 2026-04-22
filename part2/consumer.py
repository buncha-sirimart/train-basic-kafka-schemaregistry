"""
╔══════════════════════════════════════════════╗
║  Part 2 — Workshop: Avro Consumer            ║
║  เติมโค้ดในส่วนที่มี TODO ให้ครบ            ║
╚══════════════════════════════════════════════╝

⚠️  รัน producer.py ก่อน เพื่อให้มีข้อมูลใน Topic
"""
import os
from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

# ─── เชื่อมต่อ Schema Registry ───────────────────────────────
sr_client = SchemaRegistryClient({
    'url': os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')
})


# ════════════════════════════════════════════════
# TODO 1: สร้าง AvroDeserializer
#         ต้องการ 1 argument: sr_client
#         (จะดึง schema จาก Registry อัตโนมัติ)
# ════════════════════════════════════════════════
avro_deserializer = AvroDeserializer(______)  # 👈 เติมที่นี่


consumer = Consumer({
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092'),
    'group.id': 'avro-consumer-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['orders-avro'])

print('⏳ รอรับข้อมูล Avro... (กด Ctrl+C เพื่อหยุด)\n')

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f'❌ Error: {msg.error()}')
            continue

        # ════════════════════════════════════════════════
        # TODO 2: Deserialize ข้อมูล Avro → Python dict
        #         avro_deserializer รับ 2 arguments:
        #           1. raw bytes จาก message (hint: msg.value())
        #           2. SerializationContext(msg.topic(), MessageField.VALUE)
        # ════════════════════════════════════════════════
        order = avro_deserializer(
            ______,  # 👈 เติมที่นี่
            SerializationContext(msg.topic(), MessageField.VALUE)
        )

        # แสดงข้อมูลที่ได้รับ (order คือ Python dict)
        print(f'📦 Order ที่ได้รับ:')
        print(f'   order_id : {order["order_id"]}')
        print(f'   item     : {order["item"]}')
        print(f'   quantity : {order["quantity"]}')
        print(f'   price    : {order["price"]} บาท')
        print(f'   offset   : {msg.offset()}\n')

except KeyboardInterrupt:
    print('\n🛑 หยุดรับข้อมูลแล้ว')

finally:
    consumer.close()
    print('✅ ปิด Consumer เรียบร้อย')
