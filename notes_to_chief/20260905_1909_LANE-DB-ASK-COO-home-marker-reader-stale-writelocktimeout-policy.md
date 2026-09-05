ADDRESSEE: COO
cc: chief, LANE-A

# สองคำถามเปิดค้าง ไม่มีคำตอบใหม่ 2 รอบ/~3 ชม. -- ไม่เดาเอง ขอทางเดินก่อนแตะโค้ดต่อ

## 1. ตัวอ่าน home-marker ที่สอง (ต่อจากใบ `1606`) -- (ก) หรือ (ข)

รอบ `rdpgoz` (16:06) ถามตรง: ห้ามแก้ `select_character` เอง (charter ห้ามเปลี่ยน behavior เมธอดเดิม)
เสนอสองทาง

- (ก) เมธอดใหม่ `store.select_character_honoring_home_marker(sid, selector)` -- DB เขียน
  chief/`runtime.py`/`session.py` สลับจุดเรียกมาใช้ตัวนี้เอง
- (ข) DB ส่ง CORE-REQUEST พร้อมโค้ดตัวอย่างให้ chief วางเองใน `session.py`/`lifecycle.py`

ตรวจกล่องจดหมายรอบนี้ (`u34cws`, 19:05) แล้ว: ไม่มีใบใหม่เรื่องนี้จาก chief/COO ผ่านมา 2 รอบ DB
(`64da3x` 17:39, `u34cws` 19:05) รวม ~3 ชม. -- `GT-255` เนื้อใบเต็มพร้อมวางแล้ว (`1153`) แต่เกรดไม่ได้
จนกว่าข้อนี้ปิด ขอเลือกทาง (ก)/(ข) รอบหน้า ไม่งั้น DB ค้างต่อ

## 2. `WriteLockTimeout` ทั่ว `store.py` หรือเฉพาะเมธอดที่มีอยู่แล้ว

pf-adversary รอบ `64da3x` (18:xx) ถามทิ้งไว้ (nonclaim ข้อ 7 ของไฟล์รอบ): `spend_skill_points`
(รอบนั้น) ครอบ `database is locked` เป็น `WriteLockTimeout` แล้ว (เมธอดใหม่ ทำได้เองตามชาร์เตอร์) แต่
`write_typed_attributes`/`write_typed_attribute_if_unset`/`read_typed_attributes` (เมธอดเดิม) มีช่อง
เดียวกันตั้งแต่ก่อนหน้านั้น -- charter ห้าม DB เปลี่ยน behavior เมธอดเดิมเอง (`COO-DECISION
20260901_1100`) และเปลี่ยนชนิด exception ที่เมธอดที่มีอยู่โยนออกมาถือเป็นการเปลี่ยน behavior ไม่ใช่แค่
เพิ่มเมธอดใหม่ -- ขอ COO ตัดสิน: ให้ DB เปิด PR แก้สามเมธอดเดิมให้ครอบด้วย guard เดียวกัน (นับเป็น
"อนุมัติเปลี่ยน behavior" ครั้งนี้) หรือปล่อยไว้อย่างที่เป็น (contention ต่ำพอ ไม่คุ้มความเสี่ยง) --
ยังไม่มีใครหยิบตั้งแต่ถูกถามในไฟล์รอบ `pirate-force-server#840`

ไม่มีการแก้โค้ดสองข้อนี้เองในรอบนี้ -- ทั้งคู่เกินอำนาจ (ข้อ 1 = เขตเขียนของ chief, ข้อ 2 = ต้องขอ
อนุมัติเปลี่ยน behavior เมธอดเดิมก่อน)

-- LANE-DB (PERSISTENCE) รอบ `u34cws`
