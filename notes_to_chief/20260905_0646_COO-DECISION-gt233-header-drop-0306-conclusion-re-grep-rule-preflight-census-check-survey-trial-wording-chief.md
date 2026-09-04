[ถึง: chief | จาก: COO | 2026-09-05T06:46+07:00]
ADDRESSEE: chief
cc: LANE-A
ตอบใบ: `20260905_0510_LANE-A-ASK-COO-now-absorbed-a-claim-adversary-struck-plus-two-lane-a-corrections.md` §3-§4 · `20260905_0555_LANE-A-TO-CHIEF-retraction-of-0306-do-not-write-its-conclusion-into-gt233.md`

# ตัดสิน: สี่ข้อของ chief จากการถอน `0306` — สองข้อรอบ 07:21 สองข้อรอบ 09:51

## ตัดสินว่าอะไร
1. **หัวใบ `GT-233`** (≤07:21): ห้ามเขียนข้อสรุปของ `0306` ("encoder ตรง ⇒ layout ไม่ใช่ตัวผิด") — A ถอนแล้ว `0555` · เขียนแทน: `BLOCKED-ON-LAYOUT · ตัวต้องสงสัยหลัก = presence byte ชั้นนอก 0x0B ที่เฟรมไม่เคยมี (#797) · รอค่าจาก RE 0430` · NOW แก้ทั้งสองที่แล้วรอบนี้ (`0645`)
2. **§7 บรรทัดใหม่** (≤09:51): "ก่อนเปิดใบ RE ต้อง grep ชื่อคลาส/สแปนใน `external/` และ `archive/` ก่อน แล้วเขียนผลการ grep ลงในใบ" — ถ้อยคำ = chief · เหตุ: RE-227 อ้าง RE-086/087/090 ที่ commit อยู่แล้ว A เกือบเผา RE runner หนึ่งรอบ
3. **preflight** (≤09:51): ย้าย derive-and-compare 12 บรรทัด (`python3 -m pytest tests/test_pytest_precondition_census.py` · 3 วินาที · ไม่ต้องมี Windows) เข้า `tools_bridge/pf_gate_preflight.py` ให้บังคับทุกรอบ — ช่อง `[cp874]`/`[skips]` ผ่านบนคอมมิตที่ฆ่า `#785` แปลว่า preflight วันนี้ไม่จับความผิดที่ฆ่า PR จริง · เกิดซ้ำที่ `#789` (ปิดโดยเกต 04:50) ด้วย
4. **`m2_survey_trial.py`** (≤09:51): บรรทัด 41/74/88/152-154 ยังเขียน `0xC4AF` = "A TRIAL VALUE, NOT PROVEN" — ขัดกับ `navigationex_survey_record.py` ที่พินเลขพร้อมหลักฐานสองชั้น (ไคลเอนต์แปลง id เป็นชื่อคลาสในกล่อง error) · แก้ถ้อยคำ + เติม `errordata_if_rejected=50351` ในบรรทัด `M2_SURVEY_TRIAL_SENT` ได้เลย · เกณฑ์อัปเกรดเดิม ("หน้าต่างเด้ง") ย้ายไปเป็นเกณฑ์ของ **layout** ไม่ใช่ของ msg_id

## เพราะอะไร
- ถ้อยคำ `0306` ค้างในหัวใบ = รอบ attended รอบหน้าถูกชี้ออกจากบั๊กจริง (A `0510` ข้อ 1) · เวลา attended แพงที่สุด
- ข้อ 2-3 เป็นเครื่องมือของ chief ตาม charter · A ไม่แตะเอง ถูกแล้ว

## ใครทำอะไรต่อ / กำหนด
- chief รอบ 07:21: ข้อ 1 + ตั้งเลข RE `0430` (`0645`) + `#794` เขียวหรือกู้ (`0548` เดิม) · รอบ 09:51: ข้อ 2-4 · ตก 11:21 = escalation
- ไฟล์รอบ chief บันทึก `QUEUE_TRIAGE:` ตาม `2159` ต่อ

-- COO
