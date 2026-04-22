"""
╔══════════════════════════════════════════════╗
║  Part 1 — Workshop: Kafka Producer           ║
║  เติมโค้ดในส่วนที่มี TODO ให้ครบ            ║
╚══════════════════════════════════════════════╝
"""
import os
from confluent_kafka import Producer

# ─── การตั้งค่าเชื่อมต่อ Kafka ───────────────────────────────
config = {
    # ดึงค่า KAFKA_BOOTSTRAP_SERVERS จาก environment variable
    # ถ้าไม่มีให้ใช้ค่า default: 'kafka:29092'
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
}

producer = Producer(config)


# ─── ฟังก์ชันแจ้งผลการส่ง ────────────────────────────────────
def on_delivery(err, msg):
    if err:
        print(f'❌ ส่งไม่สำเร็จ: {err}')
    else:
        print(f'✅ ส่งสำเร็จ! '
              f'topic={msg.topic()}, '
              f'partition={msg.partition()}, '
              f'offset={msg.offset()}')


# ════════════════════════════════════════════════
# TODO 1: กำหนดชื่อ Topic ที่ต้องการส่งข้อมูล
#         ใส่เป็น string เช่น 'orders'
# ════════════════════════════════════════════════
TOPIC = ______  # 👈 เติมที่นี่


# ════════════════════════════════════════════════
# TODO 2: กำหนดรายการข้อมูลที่จะส่ง
#         แต่ละ message เป็น string รูปแบบ JSON
#         ตัวอย่าง: '{"order_id": 1, "item": "pizza"}'
# ════════════════════════════════════════════════
messages = [
    ______,  # 👈 เติม message ที่ 1
    ______,  # 👈 เติม message ที่ 2
    ______,  # 👈 เติม message ที่ 3
]


# ─── ส่งข้อมูลทุกชิ้นเข้า Kafka ─────────────────────────────
for msg in messages:
    # ════════════════════════════════════════════════
    # TODO 3: เติม argument ใน produce() ให้ครบ
    #   topic    = ชื่อ topic (ใช้ตัวแปร TOPIC)
    #   value    = ข้อมูลที่จะส่ง แปลงเป็น bytes ด้วย .encode()
    #   callback = ฟังก์ชัน on_delivery
    # ════════════════════════════════════════════════
    producer.produce(
        topic=______,           # 👈 เติมที่นี่
        value=______.encode(),  # 👈 เติมที่นี่ (hint: ตัวแปร msg)
        callback=______         # 👈 เติมที่นี่
    )

# flush() รอให้ส่งครบก่อน exit
producer.flush()
print('\n🎉 ส่งข้อมูลครบแล้ว!')
