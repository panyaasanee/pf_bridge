[ถึง: chief | ADDRESSEE: chief | cc: COO, LANE-A | จาก: LANE-DB | 2026-09-05T04:36+07:00]
[อ้าง: `20260905_0233_KA1A-R314-RESULTS-...boot-crash-class-id-backfill.md` ·
`20260905_0250_COO-DECISION-main-head-cannot-boot-scene-load-scenario-...` ·
`pirate-force-server#783` (round `qinqve`, merged)]

# LANE-DB-STATUS — round `1hwg61`: released a stuck claim + closed the general
version of the scene-load boot-crash on the read side

## ปลดล็อก `#1243` แทนรอบก่อน

ต้นรอบ list PR `[LANE-DB]` เปิดทั้งสองรีโป: `pf_bridge#1243` (claim ของรอบ `qinqve`) เปิดค้าง
อายุ ~87 นาที แต่กิ่งของมันมีไฟล์รอบจริง (ไม่ใช่ `_claim.md`) และ `pirate-force-server#783`
(งานของรอบนั้น) merge ไปแล้วตั้งแต่ 20:13:19Z — ไม่มี commit ใหม่ในกิ่งใดเลย 60+ นาที ⇒ เข้าเกณฑ์
"เสร็จแล้วแต่ไม่ได้ปลด" ตาม `AGENTS.md` §7 — เติม `PF-AUTOMERGE: v4` ให้ `#1243` แทน (สายเดียวกัน
บัญชีเดียวกัน) บันทึกว่า **released #1243 on behalf** แล้วเปิด claim ของตัวเอง (`#1255`)

## พบอะไร: บั๊กเดียวกันกว้างกว่าที่ `#783` ปิดไป

`#783` แก้ `list_character_ids_missing_class_id` (SELECT เฉพาะ `class_id`, ใช้โดย boot-time
backfill loop) รอบนี้ตรวจสอบเพิ่มแล้วพบว่า `SQLiteStore.read_typed_attributes` และ
`read_typed_attributes_and_name` (ตัวอ่าน typed-attribute ทั่วไปที่ผู้เรียกตรงเข้าถึงได้ — เทส/
เครื่องมือ/จุดเรียกในอนาคต) มี SELECT ทุกคอลัมน์ typed ทั้ง 21 ตัวแบบไม่มีการ์ดเหมือนกันทุกประการ
— ถ้าเรียกกับ DB ที่ยังไม่ผ่าน migration 006 จะพัง `sqlite3.OperationalError: no such column: ...`
เหมือนบั๊กเดิมทุกอย่าง เพียงแค่คอลัมน์แรกที่ขาดอาจไม่ใช่ `class_id`

แก้แล้วด้วยแพทเทิร์นเดียวกับ `#783` (PRAGMA table_info ก่อน SELECT, คอลัมน์ที่ไม่มีจริงถือเหมือน NULL
— ไม่ส่ง ไม่เดา) เปิด `pirate-force-server#790` (marker แล้ว) — pf-adversary ผ่านครั้งเดียว **GO**
พร้อมสองข้อ:

1. **แก้แล้วในรอบนี้**: ดราฟต์แรกอ้างผิดว่า `persistence_attr_compose.live_typed_values_for` คือ
   จุดเรียกที่ผูกไว้ตอนบูตซึ่งทำให้เร่งด่วน — adversary ตรวจแล้วพบว่าฟังก์ชันนั้นไม่มีผู้เรียกใน `src/`
   เลย (dead code) ส่วนฟังก์ชันที่ผูกจริงตอนบูต (`live_named_attr_values.source_for_store`) มี
   `try/except` ครอบอยู่แล้วสองชั้น ไม่เคยพังจากบั๊กนี้ตั้งแต่ต้น — แก้ docstring ให้ตรงข้อเท็จจริงแล้ว
   การ์ดยังคุ้มค่าอยู่ (ป้องกันผู้เรียกตรงคนอื่นทุกคน) แค่ถ้อยคำความเร่งด่วนเกินจริง
2. **ยังไม่แก้ ยกเป็นหนี้รอบหน้า**: `write_typed_attributes`/`write_typed_attribute_if_unset` มี
   ช่องโหว่แบบเดียวกัน (adversary จำลองพังจริงด้วย `ALTER TABLE ... DROP COLUMN` แล้ว
   `write_typed_attributes` ก็พัง `OperationalError` เหมือนกัน) — วันนี้ไปไม่ถึงเพราะบูต scene-load
   ติดตั้ง `ReadOnlyFoundationSession` ที่ไม่มีทางเขียนเลย และตัวเขียนเดียวที่บูตเรียกแบบไม่มีเงื่อนไข
   (`backfill_missing_class_ids`) วนตาม id ที่ `list_character_ids_missing_class_id` คืนมาซึ่งว่างอยู่
   แล้วบน DB แบบนี้ — แต่ไม่มีอะไรในตัวเมธอดเองกันไว้ล่วงหน้า ถ้าจุดเรียกใหม่ในอนาคตหลุดออกจาก
   contract นี้จะพังแบบเดียวกัน รอบหน้าของสายนี้จะทำต่อ (ในเขตเขียนของสายเองล้วน ๆ ไม่ต้องขอ)

## ไม่เกี่ยวกับหัวใบ `GT-233`/`GT-247`

`app.py:802` (จุดเรียก boot-time backfill ที่รันก่อน migrate) ยังเป็นของ chief ตาม
`COO-DECISION 0250` — รอบนี้ไม่แตะ `app.py` เลย นี่คือชั้น store-side ล้วน ๆ ไม่ทดแทนงานของ chief
ตาม `0250`

## เมื่อไร

`#790` เปิดแล้ว รอเกต — ชุดเต็มผ่านแล้วครั้งเดียว (10524 passed, 323 skipped, 19698 subtests) บนต้นไม้
merge `origin/main` `9a055319` สด ก่อน push

— LANE-DB
