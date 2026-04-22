"""
╔══════════════════════════════════════════════╗
║  Part 2 — เฉลย: Avro Consumer                ║
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

# ✅ เฉลย TODO 1
avro_deserializer = AvroDeserializer(sr_client)

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

        # ✅ เฉลย TODO 2
        order = avro_deserializer(
            msg.value(),
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
