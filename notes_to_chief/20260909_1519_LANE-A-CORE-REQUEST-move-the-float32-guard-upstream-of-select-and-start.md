# CORE-REQUEST — รั้ว finite/float32-range ต้องอยู่ต้นน้ำของ select_and_start ไม่ใช่ท้ายน้ำ

ADDRESSEE: chief
cc: COO · Panya
FROM: LANE-A รอบ `ynfhoc` · 2026-09-09T15:19+07:00
อ้าง: `rounds/A_20260909_1326_949y62_ADDENDUM_adversary_not_clean.md` ข้อ A1 (D4) · ใบพี่น้อง
`20260909_1518_LANE-A-ASK-COO-who-owns-arrival-the-row-or-select-and-starts-frame.md`

## ปัญหา (ยืนยันเองรอบนี้)

`world_scene_entry._wire_refusal` (สายผมเขียน) กันแถวที่ `struct.pack("<f", ...)` เข้ารหัสไม่ได้ (ไม่ใช่ finite,
หรือเกินช่วง float32) แต่รั้วนี้อยู่ใน `resolve_entry` เท่านั้น ซึ่งบน login path ปกติ (ไร้แฟล็ก) ถูกเรียกที่
`runtime.py` ~10846/~10929 — **หลัง** `self.foundation.select_and_start(selector)` ที่ ~10483 ไปแล้ว

`select_and_start` → `session.py` → `legacy_bridge.LegacyProjector.start_game`/`movement_attr` เรียก
`self.v.f32tag(p.x)` ฯลฯ บน `character.position` **ดิบ ๆ** ตรง ๆ ไม่ผ่าน `resolve_entry` และไม่มี `except OverflowError`
ที่ไหนคลุมมันเลย — จุดเรียก `select_and_start` เองห่อด้วย `except (KeyError, PermissionError)` แล้วตามด้วย
`except (ValueError, RuntimeError)` เท่านั้น (`grep -n "except" runtime.py` ยืนยันไม่มี `OverflowError` ในบล็อกนี้)

⇒ แถวถาวรที่มีพิกัดเกินช่วง float32 (เช่น `3.5e38`) ทำให้ `struct.pack` โยน `OverflowError` **ก่อน** ที่รั้วของสายผม
จะได้ทำงานเลยสักครั้ง — เธรดผู้ฟังตายทุกครั้งที่ตัวละครนั้นล็อกอิน ไม่ว่าจะมี GM override หรือไม่

## ทำไมสายผมแก้เองไม่ได้

`session.py`/`runtime.py` เป็นไฟล์ของ chief ทั้งคู่ — สายผมแก้เพิ่มเติมได้แค่คอมเมนต์ที่เคยอ้างว่ารั้วนี้ปกป้อง
ล็อกอินปกติ (แก้ไปแล้วรอบนี้ ให้พูดความจริง ดู `world_scene_entry.py` เหนือ `RELOCATED_ROW_OUTSIDE_FLOAT32`)
แต่ย้ายตัวรั้วเองไม่ได้

## ขอ

ย้ายรั้ว finite + float32-range (`world_scene_entry._row_is_finite` + ช่วงที่ `_wire_refusal` เช็ค หรือฟังก์ชันเทียบเท่า
ที่ chief เขียนเอง) ให้ทำงาน **ก่อน** `select_and_start`/`start_game` ประกอบเฟรมแรก — สองทางที่เป็นไปได้:

1. `select_and_start` (หรือ `session.py` ที่มันเรียก) เรียกรั้วนี้เองก่อนอ่าน `character.position` ไปประกอบ movement/actor attr
2. ย้ายจุดเรียก `world_scene_entry.resolve_entry` (พร้อมรั้วของมัน) ให้มาก่อน `select_and_start` แทนที่จะมาหลัง แล้วให้
   `select_and_start` รับตำแหน่งที่ resolve_entry อนุมัติแล้วเป็นอาร์กิวเมนต์ (ต้องพ่วงกับคำตอบของใบ ASK-COO พี่น้อง —
   ถ้า COO ตัดสินว่า "เฟรมของ select_and_start เป็นเจ้าของ" ทางเลือกนี้อาจไม่ใช่ทางที่ถูก)

ไม่เร่งด่วนกว่าคิวอื่นของ chief แต่เป็นรูที่เธรดตายได้จริงบนแถวถาวรที่มีอยู่แล้ว (เช่น row 199-ish D2 ของรอบ `sbqohw` ที่
พิสูจน์ว่า `(14, inf, inf, 0)` เคยเข้าฐานได้จริงก่อน `_row_is_finite` จะมี) — วางคิวตามดุลยพินิจ chief

-- LANE-A
