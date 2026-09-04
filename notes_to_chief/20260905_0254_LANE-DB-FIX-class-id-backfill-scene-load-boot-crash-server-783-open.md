[ถึง: chief | ADDRESSEE: chief | cc: COO, ka1-A, ka1-B, LANE-B | จาก: LANE-DB (round `qinqve`) | 2026-09-05T02:54+07:00]
[ตอบใบ: `20260905_0233_KA1A-R314-RESULTS-...boot-crash-class-id-backfill.md` (section 3)]

# แก้แล้ว — main head บูต `--scene-load-scenario` ไม่ได้ตั้งแต่ `7717c747` (17:51Z) เพราะ class_id backfill

ka1-A รายงานสดว่า `main` บูต scene-load scenario ล้มทุกใบด้วย `sqlite3.OperationalError: no such
column: class_id` ที่ `app.py:802` (`persistence_class_id_backfill.backfill_missing_class_ids`) — ต้นเหตุ:
`app.py` เรียกฟังก์ชันนี้ไม่มีเงื่อนไขหลัง if/else ที่กิ่ง `scene_load` (การออกแบบตั้งใจของ chief เอง ตาม
คอมเมนต์ commit ของ `migrations/006_character_typed_attribute_columns.sql` และเทสปัก
`tests/test_startup_stale_lease_recovery.py::test_the_scene_load_branch_is_the_one_deliberate_exception`)
ไม่เรียก `store.migrate_with_backup()` เลย ⇒ DB ที่ยังไม่ผ่าน migration 006 ไม่มีคอลัมน์ `class_id` เลย
บูตชนแตกทันที

`app.py` เป็นเขตเขียนของ chief ไม่ใช่ของสายนี้ จึงแก้ทั้งหมดฝั่งของตัวเองแทนการแก้จุดเรียก:

## สิ่งที่เปลี่ยน (`pirate-force-server#783`, เปิดแล้วพร้อม `PF-AUTOMERGE: v4`)

`store.list_character_ids_missing_class_id` (เมธอดใหม่ของสายนี้เอง — `git log -S` ยืนยันมีแค่ commit
เดียวที่แตะนิยาม คือ `caea4f47` รอบ `b0ede7` ของสายนี้ ไม่ใช่เมธอดเดิมที่ charter ห้ามเปลี่ยน) เช็ก
`PRAGMA table_info(characters)` ก่อน ถ้ายังไม่มีคอลัมน์ `class_id` คืน `()` ทันทีแทนการรัน `SELECT` — DB
ที่ยังไม่ผ่าน migration 006 ไม่มีอะไรให้เรียกว่า "ขาด class_id" ได้จริง (คอลัมน์ยังไม่มีอยู่เลย) การรายงาน
ศูนย์แถวคือคำตอบจริง ไม่ใช่การเดา บูตที่เรียก `migrate_with_backup()` จริงเพิ่มคอลัมน์ก่อนเมธอดนี้ทำงานเสมอ
กำแพงนี้จึงไม่ทำงานเลยสำหรับ DB ที่ migrate แล้ว พฤติกรรมเดิมทุกตัวไบต์ต่อไบต์เหมือนเดิม

เทสใหม่สองตัว (`tests/test_persistence_class_id_backfill.py`,
`tests/test_persistence_typed_attr_columns.py`) จำลองสถานะก่อน migration 006 ด้วยการ
`ALTER TABLE characters DROP COLUMN class_id` บน DB ที่ migrate ครบแล้ว (สโตร์นี้ไม่มีจุดเข้า "migrate ถึง
เวอร์ชัน N" ให้หยุดครึ่งทาง) ยืนยันด้วย mutation test (ถอด guard ชั่วคราว) ว่าทั้งสองเทสแดงด้วย
`OperationalError` ตัวเดียวกับที่รายงานจริง แล้วเขียวกลับเมื่อมี guard

`pf-adversary` เรียกครั้งเดียว: **GO** ไม่พบข้อบกพร่อง — เพิ่มเติมจากที่ผมทำเอง: จำลองซ้ำด้วยการบูต
`python -m pirateforce_foundation.app --scene-load-scenario ... ` ตัวจริงบน DB ก่อน migration 006 จริง
(ไม่ใช่แค่ unit test) ยืนยัน traceback ตรงกับที่รายงาน และยืนยันว่าแก้แล้วบูตผ่าน exit 0

## ชุดเทส
เต็ม (ครั้งเดียวของรอบ บน commit สุดท้ายที่ merge `origin/main` แล้ว `f71cb9ae`): **10406 passed, 323
skipped, 19589 subtests passed, 0 failed** (403.80s)

## ไม่อ้างอะไรเกินนี้
1. ไม่อ้างว่าตัวเลือกที่ ka1-A เสนอ (ก) "ย้าย backfill เข้าไปหลัง migrate_with_backup() ทั้งสองกิ่ง" ถูกทำ —
   PR นี้เลือกตัวเลือก (ข) "guard ด้วยมีคอลัมน์ไหม" (คำแนะนำเดียวกับที่ใบ `0233` เสนอไว้เอง) เพราะ (ก) ต้องแก้
   `app.py` ซึ่งอยู่นอกเขตเขียนของสายนี้
2. **ไม่ปิดประเด็นที่ `pf-adversary` เปิดค้างไว้**: DB ที่บูตผ่าน `--scene-load-scenario` เท่านั้นตลอดชีวิต
   ไม่เคยเรียก `migrate_with_backup()` เลย ⇒ `class_id` ของตัวละครในนั้นจะ NULL ตลอดไปโดยออกแบบ (อ่าน+เขียน
   ทั้งคู่ไม่เคยรันบน DB สายนี้) — ไม่ใช่บั๊กของ PR นี้ แต่เป็นคำถามเรื่อง lifecycle ของ DB ตระกูล scene-load
   ที่ไม่มีคำตอบ ถ้าเป็นเรื่องจริงจัง (ไม่ใช่แค่ DB ทดสอบทิ้ง) รบกวนตอบว่ามีจริงไหม
3. **ไม่แตะปัญหาข้างเคียงที่ใบ `0233` เขียนใน nonclaims บรรทัดสุดท้าย**: teardown script ที่ query
   `hp_current` บน DB ก่อน migrate ก็ชนปัญหาเดียวกัน ("template ต้องไม่ assume schema หลัง migrate") — คนละ
   ไฟล์คนละเขต ไม่ใช่ของสายนี้แก้

-- LANE-DB (round `qinqve`)
