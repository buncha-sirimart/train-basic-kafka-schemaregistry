"""เฉลย Part 1 — consumer.py"""
import os
from confluent_kafka import Consumer

config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092'),
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(config)
consumer.subscribe(['orders'])
print('⏳ รอรับข้อมูล... (Ctrl+C เพื่อหยุด)\n')
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None: continue
        if msg.error():
            print(f'❌ {msg.error()}'); continue
        value = msg.value().decode()
        print(f'📨 {value} | offset={msg.offset()} | partition={msg.partition()}')
except KeyboardInterrupt:
    print('\n🛑 หยุดแล้ว')
finally:
    consumer.close()
