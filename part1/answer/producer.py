"""
╔══════════════════════════════════════════════╗
║  Part 1 — เฉลย: Kafka Producer               ║
╚══════════════════════════════════════════════╝
"""
import os
from confluent_kafka import Producer

config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
}

producer = Producer(config)


def on_delivery(err, msg):
    if err:
        print(f'❌ ส่งไม่สำเร็จ: {err}')
    else:
        print(f'✅ ส่งสำเร็จ! '
              f'topic={msg.topic()}, '
              f'partition={msg.partition()}, '
              f'offset={msg.offset()}')


# ✅ เฉลย TODO 1
TOPIC = 'orders'

# ✅ เฉลย TODO 2
messages = [
    '{"order_id": 1, "item": "pizza", "quantity": 2}',
    '{"order_id": 2, "item": "burger", "quantity": 1}',
    '{"order_id": 3, "item": "sushi", "quantity": 3}',
]

for msg in messages:
    # ✅ เฉลย TODO 3
    producer.produce(
        topic=TOPIC,
        value=msg.encode(),
        callback=on_delivery
    )

producer.flush()
print('\n🎉 ส่งข้อมูลครบแล้ว!')
