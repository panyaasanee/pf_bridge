[ถึง: chief | จาก: LANE-CS รอบ `30kpco` (สายเดิม รอบ `mps8zh` เพิ่งปิด) | 2026-09-05T11:54+07:00]
ADDRESSEE: chief
cc: COO
เกี่ยวกับ: `pirate-force-server#815` (แนบมากับจดหมายนี้)

# CORE-REQUEST — จุดเสียบ `store.py` อ่าน/หัก `characters.skill_points` จริง + ถาม COO เรื่องสกิล 111 ต้นทุนเป็นเศษ

## ข้อ 1 — CORE-REQUEST ถึง chief: จุดเสียบ `store.py`

### ทำไม

`skill_learn_validator.py` (LANE-CS, รอบ `6r13k5`/`30kpco`) มีฟังก์ชันบริสุทธิ์ครบคู่แล้ว:
- `can_afford_to_learn(current_skill_points: int, skill_id: int) -> bool`
- `skill_points_after_learning(current_skill_points: int, skill_id: int) -> int` (ใหม่รอบนี้ — `#815`)

ทั้งคู่ไม่แตะ DB/wire/socket เลยตามเขตเขียนของ LANE-CS — `store.py`/`characters` table เป็นเขตของ chief/LANE-DB
ตามกติกาบ้าน ("จุดเสียบ = ขอ chief เป็น CORE-REQUEST ใบเดียวต่อจุด") ผมเลยยังต่อสายเข้า DB เองไม่ได้

### สิ่งที่ต้องมี (ข้อเท็จจริงที่วัดแล้ว รอบนี้)

- คอลัมน์ `characters.skill_points` **มีอยู่แล้ว** (`migrations/006_character_typed_attribute_columns.sql:144-145`
  ADD COLUMN + CHECK `typeof='integer'` · เติมค่าเริ่มต้นต่อใน `migrations/009_character_birth_defaults.sql`)
  แต่ `grep -n skill_points src/pirateforce_foundation/store.py` = **0 hit** — ยังไม่มี reader/writer ตั้งชื่อ
  ในไฟล์นี้เลย (แค่คอลัมน์ระดับ schema ยังไม่มีฟังก์ชันอ่าน/เขียน)

### ขอ chief ทำอะไร (จุดเสียบเดียว ไม่ใช่งานใหญ่)

เพิ่มคู่ฟังก์ชันใน `store.py` (ชื่อแนะนำ ไม่ยึดติด): `get_skill_points(character_id) -> int` (อ่านคอลัมน์
ตรง ๆ) และ `spend_skill_points(character_id, skill_id) -> int` (เรียก `skill_learn_validator.
can_afford_to_learn` ก่อน แล้ว `skill_learn_validator.skill_points_after_learning` เพื่อคำนวณค่าใหม่ แล้ว
`UPDATE` คอลัมน์ + อ่านกลับยืนยันตามกฎบ้าน "อ่านกลับหลังเขียน") — LANE-CS ไม่ขอเขียน `store.py` เอง เขียน
ฟังก์ชันบริสุทธิ์ทั้งสองไว้ให้พร้อมแล้วที่ `skill_learn_validator.py`

**ยังไม่มีผู้เรียก production ใด ๆ เรียกจุดเสียบนี้** (เหมือนทุกจุดใน `damage_by_skill.py`/
`damage_by_class_skill.py`) — คำขอนี้แค่เปิดทางให้อนาคตต่อสายได้ ไม่ใช่คำขอให้ทำงานเรียนสกิลจริงในเซสชันผู้เล่น
รอบนี้ (นั่นเป็นก้าวถัดไปหลังมีจุดเสียบ)

## ข้อ 2 — ขอ COO ตัดสิน (ไม่ใช่ของ chief คนเดียว เพราะกระทบดีไซน์เกม): ต้นทุนเศษของสกิล 111 ทำยังไง

### สิ่งที่พบ

`skill_catalog.skill_point_cost_to_learn(111)` ("VIP Strive Jump") = `0.20000000298023224` — **เป็นเศษ**
ในขณะที่อีก 7 ตัว (99, 110, 40000-44000) = `1.0` พอดี คอลัมน์ `characters.skill_points` เป็น `INTEGER`
(CHECK บังคับ) — **ไม่มีใครในโปรเจกต์นี้เคยตัดสินว่าต้นทุนเศษหักกับยอด INTEGER ยังไง** (ปัดลง/ปัดขึ้น/ปฏิเสธ
สกิลนี้ไปเลย/คอลัมน์ผิดชนิดตั้งแต่แรก) — `skill_points_after_learning` (`#815`) จึง **ปฏิเสธ** (raise
`SkillLearnValidatorError`) แทนการเดากติกาปัดเศษเอง ตาม `COO-DECISION 20260901_1059` (ห้ามเดาดีกว่าปฏิเสธ)

### ทำไมต้องถาม COO ไม่ใช่แค่ chief ตัดสินเอง

นี่ไม่ใช่คำถามทางเทคนิคล้วน (เช่น "bump เลขเวอร์ชันไหนของ ledger") แต่กระทบว่า "VIP Strive Jump" เรียนได้จริง
ไหมในระบบสุดท้าย (ถ้าเลือกปฏิเสธถาวร = สกิลนี้เรียนไม่ได้เลยจนกว่าจะมีคนแก้อีกที) หรือกลายเป็นได้ฟรี/เกือบฟรี
(ถ้าปัดลงเป็น 0) — เป็นทางเลือกดีไซน์เกม ไม่ใช่แค่การ implement

### ทางเลือกที่มองเห็น (ไม่ชี้นำ แค่แจกแจง)
1. ปัดขึ้น (`math.ceil` = 1 แต้ม) — เสียแพงกว่าค่าจริงเล็กน้อย แต่ปลอดภัย (ไม่มีทางติดลบ/ให้ฟรี)
2. ปัดลง (`math.floor` = 0 แต้ม) — เรียนได้ฟรี ขัดกับที่ตาราง client ตั้งใจให้มีต้นทุน
3. เปลี่ยนคอลัมน์ `skill_points` เป็น REAL/FLOAT — กระทบ migration + ทุกจุดอ่าน `skill_points` อื่นที่มีอยู่
   แล้ว (`persistence_attr_compose.py:394`, ฝั่ง wire `attr_wire.py` "SP" offset `0x7C` เป็น u32)
4. ปฏิเสธสกิล 111 ถาวรจนกว่าจะมีคนตัดสิน (สถานะปัจจุบันของ `#815`)

รอคำตอบ COO/Panya ก่อน LANE-CS จะเปลี่ยนพฤติกรรมของ `skill_points_after_learning` — ไม่ใช่ตัวบล็อกงานอื่นของ CS
(ยัง zero production caller เหมือนเดิม)

-- LANE-CS
