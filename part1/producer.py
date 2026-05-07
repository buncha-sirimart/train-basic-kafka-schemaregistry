"""
╔══════════════════════════════════════════════╗
║  Workshop Part 1 — Step 1: producer.py       ║
║  สร้าง Producer ส่ง message เข้า topic      ║
║  เติมโค้ดในส่วนที่มี TODO ให้ครบ            ║
╚══════════════════════════════════════════════╝
"""
import os
from confluent_kafka import Producer

# ─── เชื่อมต่อ Kafka ─────────────────────────────────────────
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


# ════════════════════════════════════════════════
# TODO 1: กำหนดชื่อ Topic
#         ใส่ชื่อ topic เป็น string
#         ตัวอย่าง: 'orders'
# ════════════════════════════════════════════════
TOPIC = ______  # 👈 เติมที่นี่


# ════════════════════════════════════════════════
# TODO 2: กำหนดรายการ message ที่จะส่ง
#         แต่ละ message เป็น string รูปแบบ JSON
#         ตัวอย่าง: '{"order_id": 1, "item": "pizza"}'
# ════════════════════════════════════════════════
messages = [
    ______,  # 👈 เติม message ที่ 1
    ______,  # 👈 เติม message ที่ 2
    ______,  # 👈 เติม message ที่ 3
]


# ─── ส่งข้อมูลทุกชิ้น ────────────────────────────────────────
for msg in messages:
    # ════════════════════════════════════════════════
    # TODO 3: เติม argument ใน produce()
    #   topic    = ชื่อ topic (ตัวแปร TOPIC)
    #   value    = ข้อมูล แปลงเป็น bytes ด้วย .encode()
    #   callback = ฟังก์ชัน on_delivery
    # ════════════════════════════════════════════════
    producer.produce(
        topic=______,           # 👈 เติมที่นี่
        value=______.encode(),  # 👈 เติมที่นี่ (hint: ตัวแปร msg)
        callback=______         # 👈 เติมที่นี่
    )

producer.flush()
print('\n🎉 ส่งข้อมูลครบแล้ว!')
