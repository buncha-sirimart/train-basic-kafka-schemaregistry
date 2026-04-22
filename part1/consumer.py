"""
╔══════════════════════════════════════════════╗
║  Part 1 — Workshop: Kafka Consumer           ║
║  เติมโค้ดในส่วนที่มี TODO ให้ครบ            ║
╚══════════════════════════════════════════════╝
"""
import os
from confluent_kafka import Consumer

# ════════════════════════════════════════════════
# TODO 1: เติม 'group.id' และ 'auto.offset.reset'
#
#   group.id          = ชื่อกลุ่มของ consumer เช่น 'my-group'
#   auto.offset.reset = ถ้าเป็น group ใหม่ให้เริ่มอ่านจากไหน
#                       'earliest' = ตั้งแต่ต้น
#                       'latest'   = แค่ข้อมูลใหม่เท่านั้น
# ════════════════════════════════════════════════
config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092'),
    'group.id': ______,           # 👈 เติมที่นี่
    'auto.offset.reset': ______   # 👈 เติมที่นี่ (hint: 'earliest')
}

consumer = Consumer(config)


# ════════════════════════════════════════════════
# TODO 2: Subscribe topic ที่ต้องการอ่าน
#         ใส่เป็น list ของชื่อ topic เช่น ['orders']
# ════════════════════════════════════════════════
consumer.subscribe([______])  # 👈 เติมที่นี่

print('⏳ รอรับข้อมูล... (กด Ctrl+C เพื่อหยุด)\n')

try:
    while True:
        # poll() = รอรับข้อมูล, timeout=1.0 วินาที
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue  # ยังไม่มีข้อมูลใหม่ รอต่อ

        if msg.error():
            print(f'❌ Error: {msg.error()}')
            continue

        # ════════════════════════════════════════════════
        # TODO 3: แสดงข้อมูลที่ได้รับ
        #   msg.value()  = ข้อมูลดิบ (bytes) ต้อง .decode() เป็น string
        #   msg.offset() = ตำแหน่งของ message ใน partition
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
