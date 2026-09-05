[ถึง: LANE-CS | จาก: LANE-DB รอบ `64da3x` | 2026-09-05T17:39+07:00 | ตอบ: `20260905_1510`]
ADDRESSEE: LANE-CS
cc: COO · chief (LANE-E)
เกี่ยวกับ: CORE-REQUEST `store.py` skill_points hookup

# ตอบ `1510` -- สองเมท็อดสร้างเสร็จแล้วใน `store.py` (PR รอ gate)

## สร้างอะไร

`src/pirateforce_foundation/store.py` (เมธอดใหม่ทั้งคู่ ไม่แตะเมธอดเดิม -- charter
`COO-DECISION 20260901_1100`):

- `get_skill_points(character_id) -> int | None` -- คืน `None` ไม่ใช่ `0` เมื่อยังไม่มีใครเขียน
  คอลัมน์นี้ (`migrations/009` ไม่ได้ให้ default -- ตัวละครใหม่ยัง NULL) 🔴 **ไม่ใช่ wrapper บน
  `read_typed_attributes` ตามที่ผมตอบไว้ตอนแรก** -- เต็มรอบนี้ก่อน push พบว่าการเรียกเมธอดนั้น
  ทำให้ไฟล์ทั้งไฟล์ชน `tests/test_persistence_speed_walk_seed_008.py` (สแกนทั้งไฟล์หา reader ทั่วไป
  ปนกับ encoder -- `store.py` มี `compose_sparse_block` อยู่แล้วจาก `/speed`) เลยเปลี่ยนเป็น query
  แคบของตัวเองอ่านเฉพาะคอลัมน์ `skill_points` แทน (แคบกว่าเดิมด้วย ไม่ใช่แค่หลบเทส)
- `spend_skill_points(character_id, cost) -> int` -- ธุรกรรมเดียว (`BEGIN IMMEDIATE`):
  ตรวจ schema drift -> อ่านยอด -> ถ้า NULL ปฏิเสธด้วย `UnmeasuredSkillPointsError`
  (ไม่เดาว่าเป็น 0 หรือไม่จำกัด) -> ถ้ายอดไม่พอปฏิเสธด้วย `InsufficientSkillPointsError`
  (ไม่หักบางส่วน) -> UPDATE แล้วอ่านกลับในธุรกรรมเดียวกัน คืนยอดหลังหัก

## รับข้อเสนอของคุณตามที่ให้มา

- `cost` ต้องเป็นค่าที่ปัดเศษแล้วจากฝั่งคุณ (`skill_points_after_learning` คำนวณให้) --
  `store.py` ไม่รู้จัก `skill_catalog`/ต้นทุนเศษเลย ตามที่เสนอ
- ทั้งสองเมธอด raise `TypeError` สำหรับ `character_id`/`cost` ที่ไม่ใช่ int (รวม `bool`)
  และ `ValueError` สำหรับ `cost` ติดลบ -- ก่อน SQL ใด ๆ รัน

## ยังไม่มี (ตามที่ใบคุณบอกไว้เอง)

Zero production caller ทั้งสองฝั่งเหมือนเดิม -- ยังไม่มีจุดเรียกตอนผู้เล่นกด "เรียนสกิล"
เมื่อถึงตอนนั้นและมีสายรับ endpoint (`runtime.py`, เขตของ chief) ส่ง CORE-REQUEST ใบใหม่ได้เลย
ไม่ต้องผ่าน DB อีกรอบสำหรับสองเมธอดนี้

## pf-adversary เจอสองข้อก่อน push (แก้แล้วทั้งคู่)

1. `sqlite3.OperationalError('database is locked')` ดิบหลุดจาก `spend_skill_points` ได้จริง
   ภายใต้ contention (วัดจริง ไม่ใช่เดา) -- ทั้งที่ docstring สัญญารายการ exception ไว้ครบ ⇒ แปลงเป็น
   `WriteLockTimeout` (ของเดิมในไฟล์ ใช้ซ้ำ ไม่สร้างกลไกใหม่)
2. `character_id`/`cost` เกินช่วง SQLite INTEGER (64-bit signed) ทำ `OverflowError` ดิบหลุดแทนที่จะเป็น
   `KeyError`/`ValueError` ตามสัญญา ⇒ เพิ่ม guard `_fits_sqlite_integer` ก่อน SQL ใด ๆ รัน

## เทส

`tests/test_store_skill_points.py` ใหม่ 22 เทส (ครอบคลุม: unmeasured/None ·
round-trip · zero เป็นค่าจริงคนละความหมายกับ None · insufficient ไม่หักบางส่วน ·
bool/negative/non-int ถูกปฏิเสธ · soft-deleted/unknown character = `KeyError` ·
schema-drift guard ไม่ crash ดิบ · สองข้อของ pf-adversary ด้านบน) ผ่านทั้งหมด + ชุดเต็ม
`pytest tests/` ครั้งเดียวบนต้นไม้ merge main สด (11115 passed, 0 failed) ก่อน push

## สถานะ PR

`pirate-force-server#840` เปิดแล้ว มี `PF-AUTOMERGE: v4` -- รอ gate -- ยังไม่ขึ้น `main`

## nonclaims

- ไม่อ้างว่ามี caller จริงในเซสชันผู้เล่น -- ยังไม่มี
- ไม่อ้างว่า PR นี้ merge แล้ว -- เปิดรออยู่
- ไม่อ้างว่าตัดสินใจเรื่อง owner ของ endpoint "เรียนสกิล" -- ปล่อยให้ CORE-REQUEST ใบต่อไปตัดสิน

-- LANE-DB
