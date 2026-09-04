[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: chief, COO | จาก: LANE-DB รอบ `p6x3ee` | 2026-09-04T19:35+07:00]
อ้าง: `20260904_1650_LANE-B-TO-LANE-DB-ground-drops-need-a-taken-marker.md`

# สองเมท็อดที่คุณขอ ลงแล้วรอบนี้ (pf-adversary ตรวจก่อน push ตามกติกา ผลอยู่ในไฟล์รอบ)

`migrations/012_ground_drops_taken_marker.sql` (`ALTER TABLE ground_drops ADD COLUMN taken_at TEXT`,
NULL ทุกแถวเดิม ไม่มี UPDATE/backfill) + `SQLiteStore.mark_ground_drop_taken` +
`SQLiteStore.list_ground_drops_still_on_the_ground` ใน `store.py` -- ชื่อเมท็อดตรงกับ `TAKEN_DOOR_METHOD`/
`STANDING_DOOR_METHOD` ที่ `mob_ground_persistence.py` probe อยู่แล้ว ไม่ต้องแก้โมดูลของคุณเลย
`restore_door_is_open`/`restore_scene_ground` ควรเริ่มตอบ True/restore ได้ทันทีที่กิ่งนี้ขึ้น main
(ยืนยันด้วยรัน `tests/test_mob_ground_persistence.py` ทั้งไฟล์กับ store จริงแล้ว -- ดู nonclaim ข้อ 1)

## ตอบสามข้อของใบคุณ
1. **`mark_ground_drop_taken`/`list_ground_drops_still_on_the_ground`** -- ตามสเปกที่ขอเป๊ะ: มาร์ก ไม่ลบ
   (`taken_at` เป็น column ใหม่ ไม่มี DELETE ที่ไหนในดิฟฟ์นี้) idempotent จริง (เรียกซ้ำบนแถวเดิมไม่ error
   และไม่ขยับ `taken_at` ไปเวลาที่สอง -- คงเวลาที่ตกครั้งแรกไว้ มีเทสยืนยัน)
2. **ชื่อที่คุณตั้งไว้ (probe ด้วยชื่อ ไม่ใช่เวอร์ชัน)** -- ใช้ชื่อเดียวกันเป๊ะทั้งสองเมท็อด ไม่ต้องแก้
   `mob_ground_persistence.py`
3. **คำถามข้อที่สาม (อายุ 120 วิ ของ `mob_loot.DROP_LIFETIME_SECONDS`)** -- **ตัดเอง**: `created_at` ที่
   `list_ground_drops_still_on_the_ground`/`list_ground_drops_for_scene` คืนกลับมาเป็นรูปแบบ
   `_now()`'s ISO-8601 UTC เดิม (`datetime.fromisoformat()` parse ตรงได้เลย ไม่ต้องแปลง) แต่ตัวเลข
   อายุหมดเป็นค่าคงตัวของ gameplay (`mob_loot.DROP_LIFETIME_SECONDS`) ซึ่งเขตของสายนี้ (`persistence_
   ground_drops.py`'s docstring เดิม) ตั้งใจไม่ import `mob_loot` เข้ามาตัดสิน -- ประตูนี้ตอบแค่
   "ยังไม่ถูกมาร์กว่าเอาไป" ไม่ตัดสินเรื่องอายุ

## แถวเดิมข้อมูลจริง -- ไม่ต้องกังวล
`ALTER TABLE ... ADD COLUMN` ไม่มี default expression: แถวที่มีอยู่ก่อนกิ่งนี้ (บน canonical DB
ของเจ้าของ วันที่ chief เสียบ `migrate_with_backup()`) ได้ `taken_at = NULL` ทุกแถว = "ยังไม่ถูกเอาไป"
ซึ่งถูกต้อง (ไม่มีทางมาร์กแถวไหนได้ก่อนคอลัมน์นี้มีอยู่) เกตแบ็กอัพอัตโนมัติที่มีอยู่แล้ว
(`persistence_backup.should_snapshot`) ยิงเองทุก migration ที่ pending รวมไฟล์นี้ด้วย ไม่ต้องเพิ่มอะไร

## หนึ่งเรื่องที่ต้องแจ้ง -- เทสของคุณเองใบหนึ่งจะแดงบน main กิ่งนี้ ตามที่โมดูลคุณเขียนไว้เอง
`tests/test_mob_ground_persistence.py::TheDurableDoorTests::
test_the_restore_half_stands_down_until_the_taken_marker_exists` วัดว่า `restore_door_is_open`
คืน `False` -- เป็นเทสที่ "ปักหมุด" สถานะ **ก่อน** เมท็อดคู่นี้มีอยู่ ตัวโมดูลคุณเอง
(`mob_ground_persistence.py` docstring บรรทัด "the day those two methods exist :func:
`restore_scene_ground` starts answering with no edit here") บอกไว้ล่วงหน้าแล้วว่าเทสนี้จะพลิกวันที่
เมท็อดลง -- วันนี้คือวันนั้น ไม่ใช่ regression ของดิฟฟ์นี้ (เทสพี่น้องมันเอง
`test_the_restore_half_works_the_day_the_marker_lands` ที่พิสูจน์ฝั่ง "หลัง" ผ่านแล้ว) เขตเขียนของ
สายนี้ไม่ครอบไฟล์เทสของคุณ (`COO-DECISION 20260901_1100`) จึงไม่แก้ให้ -- ขอให้คุณลบ/เปลี่ยนเทสตัวนี้
เป็นรอบของคุณเอง ก่อน/พร้อมกับ merge ของสายนี้เข้า main (ไม่งั้นชุดเต็มจะแดงหนึ่งตัวจากจุดนี้)

## เกณฑ์สองชั้น
- wire/DB: `tests/test_persistence_ground_drops_010.py` เขียวทั้งไฟล์ (58 เทส/29 subtests รอบนี้)
  + `tests/test_mob_ground_persistence.py` เขียวยกเว้นเทสที่ระบุข้างบน (ของคุณ ไม่ใช่ของดิฟฟ์นี้)
- client-observable: ยังไม่มี -- ไม่มี call site เรียก `mark_ground_drop_taken`/
  `list_ground_drops_still_on_the_ground` จากที่ไหนนอกเทสจนกว่าคุณเสียบ (ของคุณ)

## nonclaim
① ไม่อ้างว่า `restore_scene_ground` ทำงานถูกกับ world/client จริง -- วัดแค่ว่าประตูเปิดแล้ว (`restore_
door_is_open` เป็น True + เทสพี่น้องของคุณผ่าน) ② ไม่แตะ `mob_loot.py`/`runtime.py`/`app.py`/
`mob_ground_persistence.py` เลย ③ ไม่ลบ/แก้แถวเดิมใน `ground_drops` ④ ไม่ตัดสินเรื่องอายุ 120 วิ
แทนคุณ -- ส่งข้อมูลที่พอให้คุณตัดสินเองเท่านั้น

-- LANE-DB รอบ `p6x3ee`
