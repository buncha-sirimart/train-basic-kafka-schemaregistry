"""
╔══════════════════════════════════════════════╗
║  Part 1 — เฉลย: Kafka Consumer               ║
╚══════════════════════════════════════════════╝
"""
import os
from confluent_kafka import Consumer

# ✅ เฉลย TODO 1
config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092'),
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)

# ✅ เฉลย TODO 2
consumer.subscribe(['orders'])

print('⏳ รอรับข้อมูล... (กด Ctrl+C เพื่อหยุด)\n')

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            print(f'❌ Error: {msg.error()}')
            continue

        # ✅ เฉลย TODO 3
        value = msg.value().decode()

        print(f'📨 ได้รับ: {value}')
        print(f'   offset={msg.offset()} | partition={msg.partition()}')

except KeyboardInterrupt:
    print('\n🛑 หยุดรับข้อมูลแล้ว')

finally:
    consumer.close()
    print('✅ ปิด Consumer เรียบร้อย')
