"""เฉลย Part 2 — consumer.py"""
import os
from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

sr_client = SchemaRegistryClient({'url': os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')})
avro_deserializer = AvroDeserializer(sr_client)
consumer = Consumer({'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092'),
                     'group.id': 'avro-consumer-group', 'auto.offset.reset': 'earliest'})
consumer.subscribe(['orders-avro'])
print('⏳ รอรับข้อมูล Avro...\n')
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        if msg.error(): print(f'❌ {msg.error()}'); continue
        order = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
        print(f'📦 {order} | offset={msg.offset()}')
except KeyboardInterrupt:
    print('\n🛑 หยุดแล้ว')
finally:
    consumer.close()
