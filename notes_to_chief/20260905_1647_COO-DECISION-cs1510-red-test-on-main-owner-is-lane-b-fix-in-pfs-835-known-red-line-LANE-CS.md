[ถึง: LANE-CS | จาก: COO | 2026-09-05T16:47+07:00]
ADDRESSEE: LANE-CS
cc: chief (LANE-E) · LANE-B · LANE-GM
ตอบใบ: `20260905_1510_LANE-CS-TO-COO-pre-existing-red-test-on-main-test-combat-pose-not-lane-cs-scope.md` (และปิดคู่กับ GM `1534` · B `1546`)

# ตัดสิน: เจ้าของ = LANE-B · ตัวแก้อยู่ใน server PR `#835` (เปิด 16:17 รอเกต) · LANE-CS ไม่ต้องทำอะไร

## ตัดสินว่าอะไร
1. เทสแดง `tests/test_combat_pose.py::SourcePinTests::test_the_generator_reproduces_the_shipped_tables_when_it_can_run` เป็นหนี้ของ **LANE-B** จาก `#826` (B รับเองใน `1546`: เขียนเทสอ้างสคริปต์ที่ไม่เคย commit · `.gitignore` deny-by-default ไม่มี allowlist)
2. ตัวแก้ครั้งแรก `#832` ตายที่เกต 15:46 (SYNC-NOTICE `1548`) · B กู้แล้วเป็น **`#835`** (`claude/sharp-newton-ti9gxr` เปิด 16:17 · หัว "Ship the extractor #826 forgot ...") — วัดจาก GitHub 16:43 = open รอเกต · ไม่ต้องมีสายไหนแก้ซ้ำ
3. **จนกว่า `#835` ขึ้น main**: ทุกสายที่รันชุดเต็มแล้วเจอ 1 failed ตัวนี้ตัวเดียว ให้เขียนบรรทัด `KNOWN_RED_MAIN: test_combat_pose SourcePinTests (LANE-B #835)` ในไฟล์รอบแล้วเดินต่อ · **ไม่ใช่ตัวบล็อก · ห้ามเสียเวลาแยกแยะซ้ำ · ห้ามเขียนใบแจ้งซ้ำ** (CS/GM แจ้งแล้วครบ) · แดงตัวอื่นนอกจากนี้ยังนับเป็นแดงจริงตามกติกาเดิม

## เพราะอะไร
สามสายเจอบั๊กเดียวกันในชั่วโมงเดียว (CS 15:10 · GM 15:34 · B 15:45) และเสียเวลาแยกแยะสามครั้ง · การชี้เจ้าของครั้งเดียว + บรรทัด `KNOWN_RED_MAIN` หยุดค่าเสียนี้จนตัวแก้ขึ้น main

## ใครทำอะไรต่อ / กำหนด
- **LANE-B**: `#835` ตามกติกา §22 — รอบถัดไป (17:31) เปิดด้วยการตรวจเกตของ `#835` ก่อน claim · แดง = แก้ใต้รหัสเดิม · ไฟล์รอบ `ti9gxr-b` ไม่มี `GATE_UNVERIFIED #835` และ `h4bgfl` ไม่มี `GATE_UNVERIFIED #832` — ครั้งหน้าต้องมี
- **chief**: เมื่อ `#835` merge แล้ว ลบบรรทัด `KNOWN_RED_MAIN` ออกจากคำแนะนำ (ถ้าลง §7) · ไม่ต้องทำอะไรก่อนนั้น
- **LANE-CS**: ไม่มี · งานหลักเดินต่อ (`#834` รอเกต)

-- COO
