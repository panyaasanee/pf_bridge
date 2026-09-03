# LANE-CS round 18h0fp: class_catalog exposes all three starting dress sets

ตอบใบ: `notes_to_chief/20260904_0548_COO-DECISION-lane-cs-catalog-accepted-expose-all-three-dress-sets-so-class-presets-derive-from-your-table.md` (ตอบด้วยจดหมาย .CONSUMED.txt แล้ว)

## ขยับ NOW/M ข้อไหน
- `PANYA-DECISION 0328` ข้อ 5 (LANE-CS · COO-DECISION `0548` ข้อ 2): เปิด accessor สามชุดเสื้อผ้าเริ่มต้นต่อคลาส ให้ LANE-DB derive `CLASS_PRESETS` จากตารางที่พิน — **ส่งแล้ว**
- ไม่ขยับ M2/M3/M4 (ไม่ใช่เขตของรอบนี้)

## ส่งอะไร
- **pirate-force-server** PR #708 (`claude/inspiring-albattani-18h0fp` @ `458daef`, merged with `origin/main` @ `59b1fb0`):
  - `src/pirateforce_foundation/class_catalog.py`: `CLASS_ID_TO_STARTING_DRESS_SETS` + `starting_dress_sets(class_id)` — คืน 3 ทริปเปิล `(hat, chest, leggings)` ต่อคลาส จากคอลัมน์ `n_DRESS_CHEST`/`n_DRESS_LEGGINGS` + `_2` + `_3` (พิน sha256 เดิม ไม่แก้ตาราง)
  - `tests/test_class_catalog.py`: เทสค่าจริงครบ 5 คลาส x 3 ชุด · เทส distinctness ข้ามชุด · เทสอ่าน header ดิบแทนเทส tautological เดิม (ราย ละเอียดในหัวข้อ adversary)
  - เกต: `pytest tests/test_class_catalog.py` 14 passed · full suite บนต้นไม้ merge main แล้ว 9441 passed/328 skipped/0 failed · `pf_gate_preflight.py` PASS

## ADVERSARY (ผลคืนก่อน push — ไม่ใช่ ADVERSARY_PENDING)
`pf-adversary` สั่งต้นรอบ ผลคืนก่อน push จริง สองข้อ แก้แล้วทั้งคู่ก่อนส่ง:
1. docstring อ้าง "หนึ่งทริปเปิลคอลัมน์ต่อหนึ่งชุดที่ผู้เล่นเห็นบนจอ" เป็นข้อเท็จจริงที่วัดแล้ว ทั้งที่ต้นตอ (chief `0535` ข้อ D5) เขียนกำกับไว้ว่า `[เสนอ] กลไกยังไม่วัด` และ `GT-226` ที่จะวัดยังไม่รัน ⇒ แก้ docstring ให้ระบุชัดว่าเป็นข้อเท็จจริงระดับตารางเท่านั้น ยังไม่ใช่พฤติกรรมไคลเอนต์ที่วัดแล้ว
2. เทส "hat ใช้ค่าเดียวกันทั้งสามชุด" ตัวแรก tautological — โค้ด loader คำนวณ `_hat` ครั้งเดียวแล้ว reuse เอง เทสจึงพิสูจน์ตัวเองวนไป ไม่มีวันจับตารางต้นทางเปลี่ยนได้ (adversary จำลองเพิ่มคอลัมน์ `n_DRESS_HAT_2/_3` ปลอมแล้วเทสเดิมยังเขียวหมด) ⇒ แทนที่ด้วยเทสอ่าน header ดิบจากไฟล์ TSV ตรง ๆ

## nonclaims
- ไม่แตะ `persistence_class_id.py`/`CLASS_PRESETS` (LANE-DB ไปต่อในใบ `0551`)
- ไม่แตะ `s_SCORE`/`STANDARD_STATUS`/`lifecycle.py`
- ไม่ยืนยันว่า `GT-226` วัดแล้วว่าไคลเอนต์ส่งชุดที่ 2/3 ตรงกับที่ผู้เล่นเลือกจริงบนจอ — ยังเป็นคำถามเปิดตามที่ docstring ระบุ
- ไม่ใช่งานสารบัญสกิลทุกตัว (คิวข้อ 1 เดิม) — เขตนี้ตอบเฉพาะจดหมาย `0548` ข้อ 2

## ADVERSARY_PENDING
ไม่มี — ผลคืนแล้วก่อน push

## ต่อไป
รอบถัดไป (:06/:36) กลับไปคิวข้อ 2: basic attack ทำงานจริงกับ Training Iron Man `916`
