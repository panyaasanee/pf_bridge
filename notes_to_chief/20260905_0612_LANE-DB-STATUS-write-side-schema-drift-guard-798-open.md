[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-DB รอบ `d3h7zk` · 2026-09-05T06:12+07:00]
[อ้าง: `pirate-force-server#790` (round `1hwg61`, merged) -- `pf-adversary` finding 2 บนรอบนั้น]

# LANE-DB-STATUS -- guard ฝั่งเขียนปิดหนี้ที่ `#790` เปิดไว้ · `#798` เปิดรอเกต

## ทำอะไร

`#790` (round `1hwg61`) แก้ช่องโหว่ pre-006 schema-drift เฉพาะฝั่งอ่าน (`read_typed_attributes`/
`read_typed_attributes_and_name`) `pf-adversary` รอบนั้นยืนยันด้วยการรัน
`ALTER TABLE ... DROP COLUMN` ตรง ๆ ว่าฝั่งเขียน (`write_typed_attributes`/
`write_typed_attribute_if_unset`) มีช่องโหว่เดียวกันจริง แต่ scope ออกจาก PR นั้นเพราะ unreachable
วันนี้ (`ReadOnlyFoundationSession` ไม่มีทางเขียน) -- รอบนี้ปิดหนี้นั้น

แก้: ทั้งสองเมธอดเรียก `persistence_vitals.verify_schema(db)` หลัง `BEGIN IMMEDIATE` (guard เดียวกับ
ที่ `create_character`/`apply_hp_damage`/ฯลฯ ในไฟล์เดียวกันเรียกอยู่แล้ว) ⇒ พัง `SchemaDriftError`
แบบมีป้ายแทน `sqlite3.OperationalError` ดิบ ๆ ไม่ใช่ปฏิเสธเงียบ ๆ (เพราะฝั่งเขียนตัดคอลัมน์ทิ้งไม่ได้
โดยไม่ผิดกฎ "ห้ามเงียบหาย" ของเจ้าของ `1059`)

`pf-adversary` เรียกครั้งเดียว: **GO** พร้อมสามข้อบันทึก (รายละเอียดเต็มใน PR body และไฟล์รอบ)
ไม่มีข้อไหนบล็อกรอบนี้ -- ที่น่าสนใจที่สุด: `write_typed_attribute_if_unset` เขียนคอลัมน์เดียวแต่ guard
เช็คทั้ง schema เหมือน `create_character` เป๊ะ (ไม่ใช่ asymmetry ใหม่) บันทึกเป็น `[PROPOSED]` งาน
ปรับปรุงในอนาคต

## สถานะ PR

`pirate-force-server#798` เปิดแล้วพร้อม `PF-AUTOMERGE: v4` -- 🔴 **GATE_UNVERIFIED**: push ที่
~22:59Z, job `gate` ยังเป็น `in_progress` ที่ตรวจครั้งสุดท้าย (23:12Z, เกิน 10 นาทีตาม
`PANYA-DECISION 1158`) ⇒ เขียนไว้ตรงนี้แทนรอต่อ รอบหน้าของสายนี้เปิดด้วยการตรวจ PR นี้ก่อนอย่างอื่น

ชุดเต็มครั้งเดียวของรอบ (บน commit สุดท้าย merge `origin/main` `3e29682f`):
**10595 passed, 323 skipped, 19737 subtests passed, 0 failed** (390.42s)

## ไม่ได้ขอ/ไม่ได้ตัดสินอะไรเพิ่ม

ใบนี้เป็นใบแจ้งสถานะ (STATUS) ไม่ใช่ ASK -- ไม่ต้องการคำตอบเว้นแต่ `#798` แดงจริงแล้วต้องการทิศทาง

— LANE-DB
