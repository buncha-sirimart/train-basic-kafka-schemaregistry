# 🚀 Kafka & Schema Registry Workshop

## วิธีเริ่มต้น

### 1. เปิด Workshop Environment
กด **"Open in Codespaces"** ที่ปุ่มด้านบนของ Repository
> รอประมาณ 1-2 นาที ให้ Kafka และ Schema Registry พร้อมทำงาน

### 2. ตรวจสอบว่าระบบพร้อมใช้งาน
เปิด Terminal แล้วรันคำสั่ง:
```bash
bash check.sh
```
ถ้าเห็น `✅ Kafka ready!` และ `✅ Schema Registry ready!` แปลว่าพร้อมแล้วครับ

---

## โครงสร้างไฟล์

```
kafka-workshop/
├── workshop/
│   ├── part1/
│   │   ├── producer.py        ← Part 1: เติมโค้ด Producer
│   │   └── consumer.py        ← Part 1: เติมโค้ด Consumer
│   └── part2/
│       ├── schema.py          ← Part 2: เติมโค้ด Schema Registry
│       ├── producer.py        ← Part 2: เติมโค้ด Avro Producer
│       ├── consumer.py        ← Part 2: เติมโค้ด Avro Consumer
│       └── break_schema.py    ← Part 2: ทดลองส่งข้อมูลผิด Schema
└── answers/
    ├── part1/                 ← เฉลย Part 1
    └── part2/                 ← เฉลย Part 2
```

---

## Part 1 — Basic Produce & Consume (30 นาที)

```bash
# รัน Producer
python workshop/part1/producer.py

# รัน Consumer (เปิด Terminal ใหม่)
python workshop/part1/consumer.py
```

## Part 2 — Schema Registry (30 นาที)

```bash
# ขั้นตอนที่ 1: Register Schema
python workshop/part2/schema.py

# ขั้นตอนที่ 2: รัน Avro Producer
python workshop/part2/producer.py

# ขั้นตอนที่ 3: รัน Avro Consumer (เปิด Terminal ใหม่)
python workshop/part2/consumer.py

# ขั้นตอนที่ 4: ทดลองส่งข้อมูลผิด Schema
python workshop/part2/break_schema.py
```

---

## Kafka UI (ดูข้อมูลใน Topic แบบ Visual)
เปิด Browser ไปที่ port **8080** เพื่อดู Kafka UI
