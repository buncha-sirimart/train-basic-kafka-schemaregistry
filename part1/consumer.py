"""
╔══════════════════════════════════════════════╗
║  Workshop Part 1 — Step 2: consumer.py       ║
║  สร้าง Consumer อ่านข้อมูลออกจาก topic      ║
║  เติมโค้ดในส่วนที่มี TODO ให้ครบ            ║
╚══════════════════════════════════════════════╝
"""
import os
from confluent_kafka import Consumer

# ════════════════════════════════════════════════
# TODO 1: เติม 'group.id' และ 'auto.offset.reset'
#
#   group.id          = ชื่อกลุ่ม Consumer เช่น 'my-group'
#   auto.offset.reset = 'earliest' อ่านตั้งแต่ต้น
#                       'latest'   อ่านแค่ของใหม่
# ════════════════════════════════════════════════
config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092'),
    'group.id': ______,           # 👈 เติมที่นี่
    'auto.offset.reset': ______   # 👈 เติมที่นี่ (hint: 'earliest')
}
consumer = Consumer(config)


# ════════════════════════════════════════════════
# TODO 2: Subscribe topic ที่ต้องการอ่าน
#         ใส่เป็น list เช่น ['orders']
# ════════════════════════════════════════════════
consumer.subscribe([______])  # 👈 เติมที่นี่

print('⏳ รอรับข้อมูล... (กด Ctrl+C เพื่อหยุด)\n')

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print(f'❌ Error: {msg.error()}')
            continue

        # ════════════════════════════════════════════════
        # TODO 3: แสดงข้อมูลที่ได้รับ
        #   msg.value()     = ข้อมูลดิบ (bytes) → ต้อง .decode()
        #   msg.offset()    = ตำแหน่งใน partition
        #   msg.partition() = หมายเลข partition
        # ════════════════════════════════════════════════
        value = msg.value().______()  # 👈 เติม method แปลง bytes → string

        print(f'📨 ได้รับ: {value}')
        print(f'   offset={msg.______()} | partition={msg.______()}')
        # 👆 เติม method ชื่อ offset และ partition

except KeyboardInterrupt:
    print('\n🛑 หยุดรับข้อมูลแล้ว')
finally:
    consumer.close()
    print('✅ ปิด Consumer เรียบร้อย')


# ════════════════════════════════════════════════
# Step 3 — ทดลอง: สังเกต offset และ Consumer Group
# ════════════════════════════════════════════════
#
# 1. รัน producer.py → สังเกต offset ที่ได้
# 2. รัน consumer.py นี้ → เห็นข้อมูลไหม?
# 3. รัน producer.py อีกครั้ง → consumer รับได้ทันทีไหม?
#
# ❓ คำถามชวนคิด:
#    - เปิด Terminal ใหม่รัน consumer.py อีก 1 ตัว (group เดียวกัน)
#      → message ถูกแบ่งให้ consumer คนละตัวไหม?
#    - เปลี่ยน group.id เป็นชื่อใหม่ แล้วรันใหม่
#      → ได้รับข้อมูลเก่าตั้งแต่ต้นไหม?
