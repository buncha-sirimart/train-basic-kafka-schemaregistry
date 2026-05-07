"""เฉลย Part 2 — producer.py"""
import os, json
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

sr_client = SchemaRegistryClient({'url': os.getenv('SCHEMA_REGISTRY_URL', 'http://schema-registry:8081')})
schema_str = json.dumps({"type":"record","name":"Order","namespace":"com.workshop","fields":[
    {"name":"order_id","type":"int"},{"name":"item","type":"string"},
    {"name":"quantity","type":"int"},{"name":"price","type":"float"}]})

avro_serializer = AvroSerializer(sr_client, schema_str)
producer = Producer({'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')})
TOPIC = 'orders-avro'

orders = [
    {"order_id": 1, "item": "pizza",  "quantity": 2, "price": 250.0},
    {"order_id": 2, "item": "burger", "quantity": 1, "price": 120.0},
    {"order_id": 3, "item": "sushi",  "quantity": 3, "price": 350.0},
]

for order in orders:
    producer.produce(topic=TOPIC,
        value=avro_serializer(order, SerializationContext(TOPIC, MessageField.VALUE)),
        callback=lambda e,m: print(f'✅ offset={m.offset()}' if not e else f'❌ {e}'))
    print(f'📦 ส่ง: {order}')

producer.flush()
print('\n🎉 เสร็จ!')
