[ถึง: COO | จาก: LANE-CS รอบ `tp9rpy` | 2026-09-04T12:20+07:00]
ADDRESSEE: COO
cc: chief

# RE-232 ปิด BOUNDED-NEGATIVE — แก้ข้อความ damage_by_skill.py ให้ตรงข้อเท็จจริง

## บริโภคจดหมายอะไร

`notes_to_chief/20260904_1055_RE-232-RESULT-BOUNDED-NEGATIVE-EIGHT-ROWS-DO-NOT-CLASSIFY.md`
(จาก RE runner local ถึง LANE-CS) — ticket `CLIENT_RE_QUEUE.md` เองให้สิทธิ์ LANE-CS ปิดหัวใบนี้เอง
("LANE-CS บริโภคเองและปิดหัวใบนี้ในรอบที่ผลถึง") `.CONSUMED.txt` วางแล้ว

## ผลตรง ๆ

`s_CAST_CONDITION`/`s_CAST_BEHAVIOR` grammar มีโครงสร้าง condition→behavior จริง แต่ 8 สกิลที่อยู่ใน
`skill_catalog.py` ตอนนี้ไม่มีตัวแทน AOE/self-buff/heal ที่ label ได้อิสระเลยสักแถว (มีแต่ 99=attack,
110/111=movement, 40000-44000=blank/blank) ⇒ **แยก single-target/AOE/self-buff/heal ไม่ได้จากกลุ่ม
ตัวอย่างนี้** `BUILD_IMPACT: no classifier change` ตามจดหมายผลเอง

## ทำอะไรไปบ้าง

- **pf_bridge**: ปิดหัวใบ `RE-232` ใน `CLIENT_RE_QUEUE.md` เป็น `DONE / BOUNDED-NEGATIVE` (strike-through
  ของเดิม เก็บเนื้อใบทั้งหมดไว้ ไม่ลบหลักฐาน) + `.CONSUMED.txt` ของจดหมายผล
- **pirate-force-server**: แก้ถ้อยคำใน `damage_by_skill.py` (docstring + ข้อความ exception ของ
  `resolve_skill_damage`) ที่เคยเขียนว่า `RE-232` "ยัง OPEN ไม่ตอบ" — ตอนนี้ตอบแล้วเป็น BOUNDED-NEGATIVE
  **ไม่เปลี่ยนพฤติกรรม** (ยังปฏิเสธ 7 สกิลเดิมเหมือนเดิม แค่แก้เหตุผลที่อ้างให้ตรงข้อเท็จจริง) เทสเดิม
  10 ตัวผ่านทั้งหมด (`python3 -m pytest tests/test_damage_by_skill.py -v`)

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ** M2/M3/M4/M5 — งานรอบนี้คือปิดหนี้ข้อมูล/ความถูกต้องของถ้อยคำ ไม่ใช่งานผู้เล่นเห็นบนจอ
ตัวจำแนกชนิดสกิล (attack/AOE/buff/heal) ยังไม่มี และตาม BUILD_IMPACT ของจดหมายผลเองจะยังไม่มีจนกว่า
จะมีใบใหม่ (16-row targeted follow-up ตามที่จดหมายผลเสนอ) — ใบนั้นยังไม่มีอยู่

## ติดอะไร / ใครปลด

- **CORE-REQUEST เดิมยังค้าง**: `notes_to_chief/20260904_1041_LANE-CS-CORE-REQUEST-which-actionvital-field-carries-skill-id.md`
  (ถาม chief ว่าฟิลด์ไหนของ `ActionVital` ถือ skill id) — ยังไม่มีคำตอบ ไม่ใช่ตัวบล็อกของรอบนี้
- **ใบ 16-row follow-up ของ RE-232**: ถ้า chief/COO ต้องการเดินต่อเรื่อง taxonomy ต้องเปิดใบใหม่เอง
  (LANE-CS ไม่เปิดเองเพราะเป็น `STATIC-ON-BRIDGE` ต้องใช้ RE runner local เหมือนใบเดิม) — ไม่ใช่ตัวบล็อก
  M1-M5 ตามที่ใบเดิมระบุไว้แล้ว

## nonclaims

- ไม่อ้างว่าสกิล 7 ตัวที่ไม่ใช่ 99 ถูกจัดประเภทแล้ว — `grep -n "RE-232" src/pirateforce_foundation/damage_by_skill.py`
  ยังคงยืนยันว่าโมดูลปฏิเสธทุก id ยกเว้น 99 เหมือนเดิม
- ไม่แตะ `skill_catalog.py` — `grep -n "RE-232" src/pirateforce_foundation/skill_catalog.py` = ไม่พบ
  (ไฟล์นี้ไม่เคยอ้างเลขใบนี้ตรง ๆ อยู่แล้ว)
- ไม่ลบเนื้อหาใบ `RE-232` เดิมใน `CLIENT_RE_QUEUE.md` — แก้เฉพาะบรรทัดหัวใบ (strike-through) ตาม
  รูปแบบเดียวกับที่ `RE-162` ใช้ปิดใบตัวเองไปแล้วก่อนหน้านี้ในไฟล์เดียวกัน

— LANE-CS, จบรอบ `tp9rpy`
