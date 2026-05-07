# 🚀 Kafka & Schema Registry Workshop

## วิธีเริ่มต้น

```bash
# ตรวจสอบว่าระบบพร้อม
bash check.sh
```

---

## Workshop Part 1 — Basic Produce & Consume

```
workshop/part1/
├── producer.py   ← Step 1: เติมโค้ดส่ง message
└── consumer.py   ← Step 2 + 3: เติมโค้ดรับ + ทดลอง Consumer Group
```

```bash
# Step 1: รัน Producer
python workshop/part1/producer.py

# Step 2: รัน Consumer (เปิด Terminal ใหม่)
python workshop/part1/consumer.py

# Step 3: ทดลอง
# - รัน producer.py อีกครั้ง ดูว่า consumer รับได้ทันทีไหม
# - เปิด consumer.py อีกหน้าต่าง (group เดียวกัน) → message แบ่งกันไหม?
# - เปลี่ยน group.id ใหม่ → ได้ข้อมูลเก่าตั้งแต่ต้นไหม?
```

---

## Workshop Part 2 — Schema Registry with Avro

```
workshop/part2/
├── schema.py         ← Step 1: Register Avro Schema
├── producer.py       ← Step 2: ส่งข้อมูล Avro
├── consumer.py       ← Step 3: รับและ Deserialize
└── break_schema.py   ← Step 4: ทดลองส่งผิด Schema
```

```bash
# Step 1: Register Schema (ทำก่อนเสมอ)
python workshop/part2/schema.py

# Step 2: Avro Producer
python workshop/part2/producer.py

# Step 3: Avro Consumer (เปิด Terminal ใหม่)
python workshop/part2/consumer.py

# Step 4: ทดลองส่งผิด Schema
python workshop/part2/break_schema.py
```

---

## เฉลย

```
workshop/answers/part1/producer.py
workshop/answers/part1/consumer.py
workshop/answers/part2/schema.py
workshop/answers/part2/producer.py
workshop/answers/part2/consumer.py
```
