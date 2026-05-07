"""เฉลย Part 1 — producer.py"""
import os
from confluent_kafka import Producer

config = {'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')}
producer = Producer(config)

def on_delivery(err, msg):
    if err:  print(f'❌ {err}')
    else:    print(f'✅ topic={msg.topic()}, partition={msg.partition()}, offset={msg.offset()}')

TOPIC = 'orders'
messages = [
    '{"order_id": 1, "item": "pizza",  "quantity": 2}',
    '{"order_id": 2, "item": "burger", "quantity": 1}',
    '{"order_id": 3, "item": "sushi",  "quantity": 3}',
]

for msg in messages:
    producer.produce(topic=TOPIC, value=msg.encode(), callback=on_delivery)

producer.flush()
print('\n🎉 ส่งข้อมูลครบแล้ว!')
