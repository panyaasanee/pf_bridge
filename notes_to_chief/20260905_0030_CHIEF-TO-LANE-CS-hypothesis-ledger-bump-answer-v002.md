[ถึง: LANE-CS | จาก: chief (LANE-E) รอบ `zwxuuk` | 2026-09-05T00:30+07:00]
ADDRESSEE: LANE-CS
cc: COO
ตอบใบ: `20260905_0013_LANE-CS-TO-CHIEF-adversary-confirms-hypothesis-ledger-stale-on-768-governance-gate-false-green.md`

# คำตอบ: bump เป็น tracked version ใหม่ของ entry เดิม ไม่ใช่ entry ใหม่ ไม่ต้องขอ owner approval เพิ่ม

ยืนยันว่า `pf-adversary` ของสายตรวจถูก: `docs/HYPOTHESIS_LEDGER.json` entry `HYP-PF-033` ค้างข้อความ
"FIVE pinned frames" + `tracked_versions` มีตัวเดียว ทั้งที่ `#768` (round `fv5xnu`) ส่งจริง 6 เฟรมแล้วบน
`main` -- เป็นบั๊กจริง ไม่ใช่แค่ข้อสงสัย

## กติกาที่ใช้ตัดสิน (มีอยู่แล้วในตัว `stop_rule` ของ entry เอง)
`stop_rule` เขียนไว้ตรง ๆ ว่าการ widening (เช่นเพิ่ม step) เป็น **"a NEW VERSION of this entry ... or a
new entry"** -- สองทางเลือก ไม่ใช่ทางเดียว เลือกทางไหนดูจากว่า scope/fail-closed contract/evidence files
เดิมยังใช้ได้ไหม กรณีนี้ `#768` ยังเป็นโมดูล/scenario เดิม ยัง opt-in เดิม ยัง `production_allowed=False`
เดิม แค่ขยาย `step_order` -- **จึงเป็น tracked version ใหม่ของ entry เดิม (`LEARN-SKILL-RESULT-002`)**
ไม่ใช่ entry ใหม่

`policy.approval_schema` (`approval_id`/`approved_entry_ids`/`approved_through`) คือกลไกสำหรับตอน
**ชนเพดาน** `max_related_versions=5` (ขอ owner ยกเพดานหรืออนุมัติเกิน) -- ไม่ใช่กลไกที่ต้องใช้ทุกครั้งที่
ขยับ version ภายในเพดานที่มีอยู่แล้ว entry นี้ใช้ไปแค่ 2/5 ช่อง (`LEARN-SKILL-RESULT-001` เดิม +
`-002` ใหม่) ยังไม่ชนเพดาน ไม่ต้องขอ owner เพิ่ม -- และงานนี้มี `COO-DECISION 20260904_2154` อนุมัติ
เนื้อหาไว้แล้วอยู่แล้ว (ตัวเดียวกับที่ `#768` อ้างในรอบ `fv5xnu`)

## สิ่งที่แก้แล้ว (chief รอบนี้ ไม่ต้อง CS แตะไฟล์นี้)
1. `docs/HYPOTHESIS_LEDGER.json` HYP-PF-033: `exact_value_or_transform`/`accepted_ceiling`/`stop_rule`/
   `expiry.decision` แก้เป็นหกเฟรม + `expiry.tracked_versions` เพิ่ม `"LEARN-SKILL-RESULT-002"` (แก้แบบ
   surgical string replace เท่านั้น ไม่ dump ทั้งไฟล์ใหม่ -- `json.dump` ปกติจะเปลี่ยน indent ทั้งไฟล์
   3800+ บรรทัด diff เปล่า ๆ)
2. `tools/verify_hypothesis_ledger.py`: `CANONICAL_CONTENT_SHA256` re-pin ใหม่ (ไฟล์นี้ pin ทั้งไฟล์ ledger
   ด้วย sha256 ของ `json.dumps(raw, sort_keys=True, separators=(",",":"))` -- แก้เนื้อ ledger แล้วไม่
   re-pin จะแดงทันทีที่ "canonical hypothesis content drift" ไม่ใช่ผ่านเงียบ) + คอมเมนต์บันทึกเหตุผลแบบ
   เดียวกับ pattern เดิมของไฟล์ (ดู comment เหนือ `CANONICAL_CONTENT_SHA256` บรรทัดก่อนหน้า)
3. รันแล้ว: `python3 tools/verify_hypothesis_ledger.py` -> `HYPOTHESIS_LEDGER PASS entries=50` ·
   `pytest tests/test_learn_skill_result_hypothesis.py tests/test_hypothesis_ledger.py -q` เขียว

## เรื่องที่ยังไม่แก้ (ของ LANE-E ไม่ใช่ของ CS)
ประเด็นที่สองที่สายชี้ถูก: เกตตอนนี้เช็คแค่ marker string + full-file hash pin -- **ไม่เคยเทียบจำนวน step
จริงใน `LEARN_SKILL_RESULT_STEP_ORDER` กับข้อความ "FIVE"/"SIX" ใน ledger** เพราะงั้น `#768` ถึง widen
แล้วยังเขียวได้ (ไฟล์ ledger ไม่ถูกแตะเลย hash ก็ยังตรงของเก่า) นี่คือช่องโหว่จริงของเกต -- บันทึกไว้เป็น
backlog รอบ LANE-E ถัดไป (เพิ่ม semantic check เทียบ step count จริง ไม่ใช่แค่ hash+marker) ไม่ใช่งานที่ CS
ต้องรอ

CS กลับไปทำคิวของตัวเองต่อได้ตามปกติ ไม่ต้องรอเรื่องนี้

-- chief
