"""
╔══════════════════════════════════════════════╗
║  Workshop Part 2 — Step 3: consumer.py       ║
║  รับข้อมูล Avro และ Deserialize กลับเป็น    ║
║  Python dict                                 ║
║                                              ║
║  ⚠️  รัน producer.py ก่อน                   ║
╚══════════════════════════════════════════════╝
"""
import os
from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

sr_client = SchemaRegistryClient({
    'url': os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')
})


# ════════════════════════════════════════════════
# TODO 1: สร้าง AvroDeserializer
#         ต้องการ 1 argument: sr_client
#         (ดึง Schema จาก Registry อัตโนมัติ)
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
        #   avro_deserializer(raw_bytes, SerializationContext(...))
        #   raw_bytes ดึงจาก msg.value()
        # ════════════════════════════════════════════════
        order = avro_deserializer(
            ______,  # 👈 เติมที่นี่ (hint: msg.value())
            SerializationContext(msg.topic(), MessageField.VALUE)
        )

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
