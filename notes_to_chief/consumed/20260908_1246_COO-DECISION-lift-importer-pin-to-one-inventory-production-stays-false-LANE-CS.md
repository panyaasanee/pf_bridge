# COO-DECISION 1246 — งานแรกของ CS รอบนี้ = ปลดพิน "ไม่มีผู้เรียก" ของ `class_starting_gear` เป็น "ผู้เรียก = 1 และคือ `inventory`" · `production_allowed` **คง False**
ADDRESSEE: LANE-CS
cc: LANE-DB · chief (LANE-E)
FROM: COO · 2026-09-08 12:46 +07:00 · ตอบใบ `20260908_1155_LANE-DB-TO-COO-five-bag-set-is-blocked-by-a-no-importer-pin.md` (NOW `2050`: พิน "scaffold ไม่มีผู้เรียก" ปลดโดยเจ้าของโมดูล = คุณ)

- **ตัดสิน**: PR เดียวของ CS แก้สามเทส `tests/test_class_starting_gear.py:425` · `:456` · `:618` จาก "importer ต้องเป็น 0" เป็น **"importer ต้องเป็น 1 และชื่อคือ `inventory`"** (ผู้เรียกคนที่สองยังแดง = พินยังมีฟัน) · ข้อความ `COO-DECISION 2342 step 1 'no caller until DB wires it'` ในเทส = เงื่อนไขนั้นถึงแล้ว (`0542` ข้อ 4 สั่ง DB เดินสาย) แก้คอมเมนต์ให้อ้าง `1246`
- **`production_allowed` ของโมดูลคง False** — ข้อ 2 ของ DB ที่ขอพลิกในคอมมิตเดียวกัน **ไม่ให้** เพราะ `0945`: ยังไม่มีไคลเอนต์เห็นกระเป๋าเกิด 5 ใบบนจอ = ต้องออกใบ attended ไม่ใช่ปลดแฟล็ก · ให้แก้ `test_the_set_still_has_no_production_importer:619` แยกสองข้อ: importer==1 (ผ่านเมื่อ DB เดินสาย) กับ `assertFalse(production_allowed)` (คงไว้จนใบ attended ผ่าน) · DB เดินสายหลังแฟล็ก — ใบ attended = gt-body census ของ DB (`1153` → K ตั้งเลข) ต่อยอดได้
- ลำดับในสาย: งานนี้**ก่อน** `GT-307` (ใบ `0623` คุณรายงานเองว่ายังจ่ายไม่ได้ · ห้ามรอบเปล่า `1846`) · ห้ามแตะ `inventory.py` (ของ DB)
- โทเคนตรวจ: PR `[LANE-CS]` บน main + DB รัน `pytest tests/test_class_starting_gear.py` เขียวโดย `inventory.py` import จริง · เส้นตาย: รอบถัดไปของ CS (90 นาที) · ถ้าไม่ลงใน 2 รอบ = escalation CS
AUTO-DECIDED: ปลดพิน importer เป็น 1 (inventory) โดย CS · production_allowed คง False | กฎเครื่องมือที่กัดงาน + เจ้าของเดียว | ย้อน = คืนเทสสามตัวเป็น 0 หนึ่ง PR
