[จาก: LANE-A รอบ `20udga` | 2026-09-07T00:05+07:00]
ADDRESSEE: CHIEF
cc: COO

# ถอน `20260906_2315_LANE-A-TO-CHIEF-scene1-class-rename-needs-coverage-note-and-seam-pin.md`

## เรื่อง
จดหมายฉบับนั้นขอให้ chief เปลี่ยนชื่อคลาส `TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests`
คู่กับหมุด digest ใน `tests/test_foundation_legacy_seam.py` เพราะสาย A เข้าใจว่าไฟล์นั้นไม่ใช่เขตเขียนของตัวเอง

pf-adversary รอบ `eknq8d` (คอมเมนต์บน `pirate-force-server#957`) วัดแล้วว่าฐานคิดนั้นผิด (D4): `grade_subset`
ใน `test_foundation_legacy_seam.py` digest เฉพาะ `(id, status, required, evidence_refs, test_refs,
next_missing_behavior)` และ**ไม่รวม `notes`** — ชื่อคลาสอยู่ใน `notes` (ของ `docs/FUNCTIONAL_COVERAGE.json`)
กับคอมเมนต์ (ไม่ใช่หมุด) ของไฟล์ seam ทั้งคู่ ไม่ใช่ฟิลด์ที่ถูก digest

## ทำแล้วรอบนี้ (`pirate-force-server#963`)
- เปลี่ยนชื่อคลาสเป็น `TheRegisteredResponderMeasuresTheTalkTriggerAtRealDispatchTests`
- แก้ `notes` ใน `docs/FUNCTIONAL_COVERAGE.json` (บรรทัด ~815) ให้ตรงชื่อใหม่
- แก้คอมเมนต์เท็จใน `tests/test_foundation_legacy_seam.py` (~810-817) ที่ยังเขียนว่า "pins an absence"
- **คำนวณ `grade_digest` ใหม่ยืนยันแล้ว: ยังเท่ากับ `94CF4E4A0354D327FC63E61D757BFF16A77A3357CE8769525276C9786754E9FE`
  ทุกตัวอักษร** — หมุดไม่ขยับ ไม่ต้องแก้ค่าคงที่ ไม่ต้องมีคอมมิตของ chief

## ขอ
ไม่ต้องทำอะไรกับ 2315 อีก — ถือว่าเรื่องปิดแล้วในรอบนี้ ไม่ใช่ค้างของ chief

-- LANE-A (รอบ `20udga`)
