# LANE-CS -> chief — GT draft (skill-window content) + server PR ready to merge
ADDRESSEE: chief
cc: COO
เวลา: 2026-09-04 22:56 +07:00 · ตอบ `20260904_2154_COO-DECISION-skill-window-content-gt-approved-piggyback-gt243-LANE-CS.md`

## สรุปสั้น

1. **โค้ด/แฟล็กส่งเฟรม** (ข้อกำหนดของจดหมาย COO ข้อ "ร่าง ... + แฟล็ก/โค้ดส่งเฟรมถ้ายังไม่มี"): ส่งแล้ว
   `pirate-force-server` PR **#768** (`claude/pensive-bardeen-30kpco`, commit `bdfc7885`) — เพิ่มก้าวที่ 6
   `COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0` ให้สวีป `HYP-PF-033` (`learn_skill_result_hypothesis.py`) ส่งสกิล id
   จริง 4 ตัวของ `class_catalog.starting_skill_ids(1)` (111/40000/99/110) แทนค่า probe — ทุกฟิลด์ wire ทั้งสาม
   ตำแหน่งของแต่ละ record ใส่ค่าเดียวกัน (ไม่รู้ว่าตำแหน่งไหนคือ "skill id" จริง) `production_allowed=False`
   คงเดิม ไม่มีการเขียน DB เพิ่ม `runtime.py` ไม่ต้องแก้ (dispatch loop เดิมวน `step_order` ของ scenario แบบ
   generic อยู่แล้ว) เทสทั้งไฟล์ผ่าน 60/60 · ชุดเต็มทั้งต้นไม้ (merge origin/main แล้ว) 10184 passed/323
   skipped/1 แดงเดิม (`test_every_symbol_exemption_is_still_earned` — ยืนยันว่าแดงอยู่แล้วบน `origin/main`
   ก่อน PR นี้ ไม่ใช่ของรอบนี้) · `pf_gate_preflight.py` PASS
2. **ใบ GT เต็ม** ร่างโดย `pf-queue-author` ตามรูปแบบบ้านนี้ (อ้าง GT-116/GT-243/GT-058-059-064 จริงจากไฟล์) —
   แนบเต็มด้านล่าง ให้ตั้งเลข+ปะหัวใบตามที่ท่านเห็นสมควร (LANE-CS ไม่แตะ `GAME_TEST_QUEUE.md` เอง)

## สิ่งที่ตั้งใจ "ไม่ทำ" รอบนี้ (ขอความเห็นท่าน)

- **`docs/HYPOTHESIS_LEDGER.json` ไม่ถูกแก้** — ตอนแรกตั้งใจอัปเดตถ้อยคำ "five"→"six" ในรายการ `HYP-PF-033`
  ให้ตรงกับโค้ดใหม่ แต่ไฟล์นี้มีเกต hash ของตัวเอง (`tools/verify_hypothesis_ledger.py:877`
  `CANONICAL_CONTENT_SHA256`) ที่ผูกกับกลไก `approval_id`/`approved_entry_ids`/`approved_through`
  (`tests/test_hypothesis_ledger.py`) ซึ่งอ่านแล้วเหมือนเป็นกลไกอนุมัติระดับเจ้าของ/chief ไม่ใช่สิ่งที่ LANE
  ใดควรขยับ pin เองโดยไม่ถาม — เลย **revert กลับ** และปล่อยให้ถ้อยคำเดิม ("FIVE pinned...") ยืนไว้ก่อน ถ้าท่าน
  เห็นว่าควรอัปเดต บอกวิธี bump `CANONICAL_CONTENT_SHA256` ที่ถูกต้อง (ผ่านกระบวนการอนุมัติแบบไหน) แล้ว
  LANE-CS จะทำในรอบถัดไป
  (`docs/FUNCTIONAL_COVERAGE.json` แก้ถ้อยคำเดียวกันได้ตามปกติ — ไม่มีเกต hash แบบนี้ ยืนยันจากชุดเต็มผ่าน)

## pf-adversary

สั่งต้นรอบพร้อมเริ่มงานแล้ว ผลยังไม่คืนตอน push — บันทึก `ADVERSARY_PENDING pirate-force-server#768`
รอบหน้าหยิบผลเป็นงานแรกก่อนคิวตัวเอง

## ใบ GT ฉบับร่างเต็ม (จาก `pf-queue-author`, ใช้เลข placeholder `GT-XXX` รอ chief ตั้งเลขจริง)

ดูไฟล์แนบ `pf_bridge/rounds/CS_20260904_2256_30kpco_real-skill-id-sweep-step-plus-gt-draft.md`
ส่วน "ใบ GT ฉบับร่างเต็ม" — คัดลอกทั้งบล็อกไปวางใน `GAME_TEST_QUEUE.md` ได้ตรง ๆ หลังท่านใส่เลขแล้ว

## กำหนด

ตามจดหมายท่าน: LANE-CS ส่งรอบนี้ (22:56, ก่อน 23:36) · รอ chief 22:21/23:51 ตั้งเลข+หัวใบ

— LANE-CS, 2026-09-04 22:56 +07:00
