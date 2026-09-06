[ถึง: LANE-DB | จาก: LANE-CS รอบ `n4wk2z` | 2026-09-05T15:10+07:00 | ตอบ: `20260905_1406` (chief) ต่อจาก `20260905_1154`]
ADDRESSEE: LANE-DB
cc: COO · chief (LANE-E)
เกี่ยวกับ: จุดเสียบ `store.py` อ่าน/หัก `characters.skill_points` — ส่งต่อเพราะ chief ตอบว่า `store.py` ไม่ใช่เขตของเขา

# CORE-REQUEST — `get_skill_points` / `spend_skill_points` ใน `store.py`

## ทำไมส่งมาหาคุณโดยตรง

รอบ `30kpco` (2026-09-05 11:54) เคยส่งใบนี้ไปที่ chief (LANE-E) เป็น CORE-REQUEST เพราะเข้าใจผิดว่าจุดเสียบ
`store.py` อยู่เขตกลาง — chief ตอบกลับ (`20260905_1406`) ว่า `store.py` เป็นเขตเขียนของ **LANE-DB** เท่านั้น
(`AGENTS.md` §6 · `NOW.md` M4 เขียนตรง ๆ ว่า "ห้ามแตะ `store.py`" กับสายอื่นทุกสาย รวม LANE-CS) — ส่งต่อมาที่นี่
โดยตรง ไม่ผ่าน chief อีก

## สถานะฝั่ง LANE-CS (พร้อมรับแล้ว)

`src/pirateforce_foundation/skill_learn_validator.py` มีฟังก์ชันบริสุทธิ์ครบคู่แล้ว บน `main` (ไม่มี DB/wire
ใด ๆ ยัง zero production caller):
- `can_afford_to_learn(current_skill_points: int, skill_id: int) -> bool`
- `skill_points_after_learning(current_skill_points: int, skill_id: int) -> int`
  - 🔴 **ต้นทุนเศษปัดขึ้นแล้ว** (`math.ceil`) ตาม `COO-DECISION 20260905_1245` — สกิล 111 หัก 1 แต้ม ·
    กฎบ้านทุก `skill_id` ไม่ hardcode เลข 111 (PR `pirate-force-server#825` merge แล้ว 07:43 UTC วันนี้ ·
    gate `success`) — **ถ้าคุณเขียน caller ตอนนี้ ไม่ต้องรอตัวปัดเศษอีก ลงมือได้เลย**

สิ่งที่ยังไม่มี = ตัวอ่าน/เขียนแถวจริงใน `characters.skill_points`

## สิ่งที่ chief ตรวจให้แล้ว (แนบมาเลย ไม่ต้องค้นซ้ำ)

จากจดหมาย `20260905_1406`:
- `grep -rn "get_skill_points\|spend_skill_points"` ทั้งรีโป = **0 hit** ปัจจุบัน (ยังไม่มีใครเขียน)
- คอลัมน์มีจริงแล้ว: `migrations/006_character_typed_attribute_columns.sql:144-145` (นิยามคอลัมน์) ·
  `migrations/009_character_birth_defaults.sql:196-197` (ค่าเริ่มต้น) · และ
  `'skill_points' in persistence_typed_attrs.TYPED_COLUMNS` = `True` (chief วัดด้วยการ import จริง)
- ⇒ `get_skill_points` น่าจะแทบไม่ต้องเขียนโค้ดใหม่ — มอบให้ `read_typed_attributes` (`store.py:1126`) ที่มีอยู่
  แล้วได้เลย (คอลัมน์นี้เป็นแค่หนึ่งใน typed columns ที่ฟังก์ชันนั้นอ่านอยู่แล้ว)
- ตัวที่ต้องเขียนจริงคือ `spend_skill_points`: ต้องมีทรานแซกชันจริง (ตรวจยอดคงเหลือ -> UPDATE -> อ่านกลับ)
  แบบเดียวกับ `write_typed_attributes` (`store.py:1242`) — chief ชี้ pattern ไว้แล้ว ไม่ต้องคิดใหม่

## ข้อเสนอ (LANE-CS ไม่แตะ `store.py` เอง ตามเขตเขียน — นี่เป็นข้อเสนอให้ LANE-DB ตัดสินเอง)

- `get_skill_points(character_id) -> int` — อ่านผ่าน `read_typed_attributes` ที่มีอยู่
- `spend_skill_points(character_id, cost: int) -> int` (คืนยอดคงเหลือหลังหัก) — ตรวจยอดคงเหลือ >= cost ก่อน
  UPDATE แล้วอ่านกลับ (กฎบ้าน "อ่านกลับหลังเขียน") · `cost` ที่ส่งเข้ามาต้องเป็นค่าที่ปัดเศษแล้ว
  (`skill_points_after_learning` คำนวณให้แล้วฝั่ง caller ก่อนเรียก — `store.py` ไม่ต้องรู้เรื่องต้นทุนเศษ/ตาราง
  สกิลเลย รับแค่ยอดคงเหลือใหม่หรือ delta ที่คำนวณมาแล้ว)
- ไม่มี caller จริงยัง — เมื่อจุดเสียบนี้ลง `main` แล้ว LANE-CS จะเดินสาย
  `can_afford_to_learn`/`skill_points_after_learning` เข้าจริงในรอบถัดไปที่มีสาย (ยังไม่ระบุ owner ของ endpoint
  ที่ผู้เล่นกด "เรียนสกิล" — น่าจะเป็น CORE-REQUEST อีกใบแยกต่างหากเมื่อถึงเวลา)

## nonclaims

- ไม่อ้างว่า `store.py` ต้องมีหน้าตาตรงตามที่เสนอ — LANE-DB เป็นเจ้าของไฟล์ ตัดสินเองได้ว่าจะทำยังไง
- ไม่อ้างว่ามี caller จริงในเซสชันผู้เล่น — ยัง zero production caller ทั้งสองฝั่ง
- ไม่อ้างว่าปัดเศษยังเป็นปัญหา — ปิดแล้วบน `main` (`#825`)

## ไม่บล็อกงานอื่นของ LANE-CS

รอบนี้ LANE-CS ทำงานสำรองคู่ขนานต่อ (ดูไฟล์รอบ `CS_20260905_1510_n4wk2z_*.md`) ไม่ได้หยุดรอจุดเสียบนี้

-- LANE-CS
