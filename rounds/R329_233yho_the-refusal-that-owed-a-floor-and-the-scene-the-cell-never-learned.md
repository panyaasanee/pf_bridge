# R329 (LANE-E, session 233yho) — 2026-09-04 00:22 - 00:51 +07:00

## บริบท
`NOW.md` งานด่วน "ต่อคิวทันทีหลังสองข้อบน" / COO-DECISION `20260903_2346` และ `20260903_2347`
สั่ง chief สองข้อ กำหนด 02:21: (1) ลง CORE-REQUEST ของ LANE-B (`20260903_2249`) ใน `runtime.py`
+ วัด D9 ว่า `#675` ปิดหรือไม่ (2) ลงกฎเวลาของ `pf-adversary` ใน `AGENTS.md` §7 ตาม `20260903_2347`
(ห้ามรวม PR กับข้อ 1)

## ข้อ 1: CORE-REQUEST `2249` — ลงแล้ว
`src/pirateforce_foundation/runtime.py`: กิ่ง `if outcome.delta is None:` ของ
`dispatch_inbound_pickup_request` แยกเป็นสองทาง — `ground_after` ว่าง คืน `[]` เหมือนเดิม ·
ไม่ว่าง คืน `list(self._mob_loot_boundary_flush()) + [("MOB_PICKUP_GROUND_AFTER", ...) ...]`
รูปเดียวกับกิ่งคลิกสำเร็จด้านล่าง (ตามรูปที่ใบ `2249` เสนอ)

`src/pirateforce_foundation/mob_pickup_request.py`: `EXPIRY_PUBLICATION_CALL_SITE_STATUS`
`"composed_not_sent"` -> `"sent"` (ผูกกับ AST ของ `runtime.py` โดย
`tests/test_mob_pickup_ground_expiry.py::TheConstantAndTheRuntimeAgree` — เขียวแล้ว)

## ข้อ D9 — วัดแล้ว: `#675` ไม่ปิด
`pirate-force-server#675` (merged) body ของมันเองบอกตรง ๆ ว่า "ground rows are not touched
(the withdrawn `reconcile_scene_transition` stays out)" — มันแก้แค่ `mob_ai_register`/
`mob_combat_ledger`/scene folder ตอนฆ่า/วาป GM ⇒ `DropLedgerCell` ยังไม่เรียนรู้ฉากตอน
**เดิน** ข้ามขอบ ตามคำเตือน `!!` ข้อสองของใบ `2249` เอง

ตาม `2346` ข้อ 3 (ไม่ใช่ ⇒ ห้ามแก้ใน PR นี้): **ไม่แก้** เปิดเป็นหนี้ของ chief เอง ต่อคิวหลัง
`GT-215` — จดหมาย `notes_to_chief/20260904_0027_CHIEF-REPORT-COO-2249-landed-and-D9-does-not-close.md`

## ข้อ 2 (2347): `AGENTS.md` §7 — ลงแล้ว (คนละไฟล์ คนละ PR จากข้อ 1)
สองข้อเดิมที่บังคับ "เรียก pf-adversary ก่อน commit เสมอ" / "ต้องมีผลก่อน push เสมอ" ถูกแทนด้วย
สามข้อของ `2345`/`2347`: สั่งต้นรอบ · push ได้แม้ผลยังไม่คืน (`ADVERSARY_PENDING`, รอบถัดไปหยิบก่อน
claim ใหม่) · ห้ามเขียน "ผ่าน" ก่อนผลคืน

## pf-adversary — คืนผลก่อน push (ไม่ใช่ ADVERSARY_PENDING)
สั่งต้นรอบ (agent `pf-adversary`) ตรวจ diff ของ `runtime.py`/`mob_pickup_request.py` ผลคืนก่อน push จริง
พบข้อบกพร่องจริงหนึ่งข้อ: **กิ่งใหม่ของ refusal ไม่มีเทสรันจริงเลยแม้แต่ตัวเดียว** — เทสเดิม
`TheConstantAndTheRuntimeAgree` เช็คแค่รูป AST ไม่ได้รัน · `test_mob_pickup_ground_expiry.py` เรียก
`dispatch_inbound_pickup_request` ตรง ไม่ผ่าน `runtime.py`/`_mob_loot_boundary_flush()` เลย
พิสูจน์ด้วยมิวแทนต์สองตัว (ลบเงื่อนไข `not outcome.ground_after`, สลับลำดับ boundary-flush กับ
`ground_after`) ทั้งคู่รอดชุดเต็มโดยไม่มีเทสไหนจับได้

**แก้แล้วในรอบเดียวกัน**: เพิ่มสองเทสใน `test_mob_loot_scene_boundary_wiring.py` ที่เดินผ่าน
`state.dispatch()` จริง (`test_an_unrelated_refusal_still_leaves_a_committed_boundary_owed`,
`test_a_refused_expired_click_flushes_the_held_boundary_first`) — ทั้งสองมิวแทนต์ตายแล้ว
(ยืนยันด้วยมือ: ใส่มิวแทนต์กลับ เทสแดง แล้ว revert)

## เทส
`test_mob_pickup_ground_expiry.py` (24/24) · `test_mob_loot_scene_boundary_wiring.py` +
`test_mob_pickup_request.py` + `test_mob_loot.py` (313 passed + 831 subtests) ·
`test_mob_pickup.py` `test_mob_stat_fabrication_guard.py` `test_pickup_transaction_console_discipline.py`
`test_vital_walk.py` (154/154 + 91 subtests) · `tools/verify_hypothesis_ledger.py` +
`tools/verify_functional_coverage.py` PASS ไม่มี drift
ชุดเต็มบนต้นไม้ merge main รันสองครั้ง (ก่อนแก้ช่องโหว่เทสของ adversary และหลัง):
9169 passed / 9171 passed, 323 skipped, 17659 subtests, 0 failed ทั้งสองครั้ง

## ยังไม่พิสูจน์
- D9 (ข้างบน) — หนี้ต่อคิว
- client-observable — เกณฑ์สองชั้นเป็นของ LANE-B เขียนต่อ (COO `2344`) chief ยังไม่เปิดใบใหม่

## PR
`pirate-force-server#689` (open, marker ยืนยันด้วย GET แล้ว, รอเกต)
