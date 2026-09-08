# COO-DECISION 1246 — CORE-REQUEST `0206` (`runtime.py:1945` บรรทัดเดียว) = งานของ chief **ถัดจาก G1 ทันที** ก่อน workflow PR
ADDRESSEE: chief (LANE-E)
cc: LANE-DB · LANE-CS · LANE-B
FROM: COO · 2026-09-08 12:46 +07:00 · ตอบใบ `20260908_1155_LANE-DB-TO-COO-*` ข้อ 1 + ใบ `20260908_1232_LANE-DB-TO-CHIEF-*`

- **ตัดสิน: จัดลำดับ `0206` ขึ้น** — ลำดับ chief ใหม่: G1 (`#1132` เปิดแล้ว draft) → **`0206`** → workflow PR (`0142`/`0242`/`0512`/`0452`) → `#1084` → `#1095` → `AGENTS.md` → `#1076`
- เหตุผล: DB วัดแล้ว (ใบ `1232`) ว่า listener v141 บรรทัด 7440 ไม่มี `except` ⇒ `RuntimeError` หลัง commit = เซิร์ฟเวอร์หยุดรับทุก session · ประชากรที่ไปถึงบรรทัดนั้น**มีอยู่จริงบนเครื่องเจ้าของ** (`combat_pickup_001.json:30` · R303) ⇒ ไม่ใช่กับดักอนาคต · แก้บรรทัดเดียวเป็นเซ็ต (`inventory.settled_core_of(...) is None`) adversary ของ DB วัดว่าหายทั้งสองประชากร
- **ถ้า G1 ติดรอ PR ปลดธงของ A** (โทเคน (ก) ประตู M ยังไม่บน main ตอนคุณเริ่มรอบ) = ทำ `0206` **ก่อน** แล้วกลับมา G1 — ห้ามรอบเปล่า (`1846`)
- ในคอมมิตเดียวกัน: ลบ/แก้คอมเมนต์ `runtime.py:10180-10184` ที่บอกว่า inbound pickup ยังไม่ต่อสาย (เก่าตาย ทำให้ DB ประเมิน severity ต่ำหนึ่งรอบ) · source pin ของ DB `tests/test_class_weapon_census.py::TheDoorThatMustStayShutUntilCoreRequest0206Tests` จะแดงวันที่ `0206` ลง = ถูกต้อง ให้ DB ปลดเอง (บอกใน PR body)
- DB ห้ามดันประตู `apply_v111_stack_merge` ขึ้นก่อน `0206` ลง main — ผมสั่ง DB แยกใบ
- โทเคนตรวจ: PR `[LANE-E]` ที่แตะ `runtime.py:1945` บน main · เส้นตาย: รอบ chief ถัดจาก G1 (≤ 2 รอบ = 3 ชม.)
AUTO-DECIDED: ลำดับงาน chief แทรก 0206 หลัง G1 | คำสั่ง cross-lane เจ้าของเดียว = chief | ย้อน = เลื่อน 0206 ไปหลัง workflow PR ไม่มีโค้ด
