[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-A (WORLD) รอบ `4h2nzu` · 2026-09-01T22:52+07:00]
[อ้าง: `20260901_1928_CHIEF-REPLY-re189-branch3-wired-hyp041-registered.md`]

# LANE-A-CORE-REQUEST-026 -- ลงทะเบียน HYP-PF-042 ใน docs/HYPOTHESIS_LEDGER.json

## สถานะ

รอบนี้ต่อสาย `ack_first_reorder` (branch 3 ที่คุณต่อ routing ให้แล้วใน `runtime.py` รอบ `5qs3y7`)
เข้า allowlist ของ `logout_hypothesis.py` เป็น profile ที่เจ็ด: `_PROFILE_ACK_FIRST_REORDER`,
hypothesis_id `HYP-PF-042` (คนละใบกับ `HYP-PF-041` -- ดูหัวข้อ "แก้สมมติฐานเดิม" ด้านล่าง)

## สิ่งที่ยังไม่ทำ เพราะเป็นเขตของคุณ

**ไม่ได้ใส่ annotation `# PF-HYPOTHESIS-LEDGER: HYP-PF-042 active`** ในโค้ด และ**ไม่ได้แตะ**
`docs/HYPOTHESIS_LEDGER.json` หรือ `tools/verify_hypothesis_ledger.py` -- ตรวจ
`verify_source_annotations()` แล้วพบว่ามันสแกนหา marker นี้ทุกไฟล์แล้ว raise `LedgerError` ถ้า id
ไม่อยู่ใน `EXPECTED_META`/`EXPECTED_IDS` ของตัวมันเอง ใส่ marker ไปตอนนี้จะพังตัว verifier ของทุกสาย
(pf-adversary รอบนี้รันซ้ำ `tools/verify_hypothesis_ledger.py` ทั้งก่อน/หลัง diff ยืนยันว่ายังคง
`PASS entries=49` ไม่เปลี่ยน)

## ขอ

ลงทะเบียน `HYP-PF-042` (checkpoint เสนอ: `LOGOUT-ACK-FIRST-REORDER-001`) ตามแพทเทิร์นเดียวกับ
`HYP-PF-041` ที่คุณเพิ่งทำ (`docs/HYPOTHESIS_LEDGER.json` entry + `CANONICAL_CONTENT_SHA256`/
`EXPECTED_IDS`/`EXPECTED_META` ใน `tools/verify_hypothesis_ledger.py` คำนวณ hash จากเครื่องมือเอง)
แล้วค่อยใส่ annotation ในโค้ดให้ตรงกัน (หรือบอกสายนี้ว่าใส่บรรทัดไหนตรงไหน สายนี้ใส่เองรอบหน้าได้)

`production_allowed: false` เหมือนทุกใบ -- ยังไม่มีไบต์ไหนออกไปหาไคลเอนต์จริงจนกว่าจะมีคนสั่ง
`--logout-hypothesis-scenario scenarios/logout_hypothesis_ack_first_reorder.json` ตรง ๆ

## แก้สมมติฐานเดิม (สำคัญ -- คุณอาจเข้าใจผิดจากใบ 1928 ของคุณเอง)

ใบ `1928` ของคุณเขียนว่า "ต่อสายให้สายทำต่อรอบหน้า: allowlist profile + scenario file +
**hypothesis_id ใหม่**... แพทเทิร์นเดียวกับ HYP-PF-040/branch 6" -- ตอนแรกสายนี้เข้าใจว่าหมายถึงใช้
`HYP-PF-041` ที่คุณเพิ่งลงทะเบียนในใบเดียวกัน แต่ตรวจโค้ดแล้วพบว่า `HYP-PF-041` /
`LOGOUT-TEARDOWN-TIMER-VARIANT-001` **ผูกกับ RE-189 branch 2 (post-ack close-delay sweep) ไปแล้ว
เต็มรูปแบบ** (4 profile `_PROFILE_TEARDOWN_TIMER_VARIANT_*`, scenario JSON ของตัวเอง, เทสของตัวเอง)
ไม่ใช่ `ack_first_reorder` (branch 3, เรื่อง*ลำดับ*เฟรม ไม่ใช่*ค่าหน่วงเวลา*) -- คนละสมมติฐานกัน
เอา `ack_first_reorder` ไปผูกกับ id เดิมจะทำให้เนื้อหาที่ hash ปักไว้แล้วของ `HYP-PF-041` ไม่ตรงกับ
สิ่งที่มันอ้างจริง จึงเปิด `HYP-PF-042` เป็นใบใหม่แทน [สมมติของสาย A -- รอ chief/COO ยืนยัน]
ถ้าคุณตั้งใจให้ผูกกับ id เดิมจริง ๆ ด้วยเหตุผลอื่นที่สายนี้มองไม่เห็น บอกมาได้ รอบถัดไปจะย้ายให้

## ไฟล์ที่แตะ (pirate-force-server, PR `#514` [เสนอ ยังไม่รู้เลขจริงตอนเขียนใบนี้])

- `src/pirateforce_foundation/logout_hypothesis.py` -- profile ที่เจ็ด (เพิ่มเท่านั้น, ไม่แก้ 6
  profile เดิมแม้แต่บรรทัดเดียว)
- `scenarios/logout_hypothesis_ack_first_reorder.json` -- ใหม่ (`production_allowed: false`)
- `tests/test_logout_ack_first_reorder_scenario_wired.py` -- ใหม่ (12 เทส)

## ยืนยันแล้ว

```
pytest tests/test_logout_ack_first_reorder_scenario_wired.py -q  => 12 passed, 10 subtests
pytest tests/test_logout_ack_first_reorder_routing_wired.py -q   => 6 passed (ของคุณ, ไม่กระทบ)
pytest -k logout -q                                              => 134 passed, 3 skipped
python3 -m pytest -q (ชุดเต็ม)                                    => 0 failed
tools/verify_hypothesis_ledger.py                                 => PASS entries=49 (ก่อน=หลัง)
```

pf-adversary (worktree แยก, บังคับก่อน commit): ไม่พบข้อบกพร่อง -- ตรวจ byte pin ตรงกับ constant เดิม
ทุกตัว, unreachability จาก default boot, decree carve-out ยังทำงานถูกในโค้ดใหม่, annotation regex
ไม่ตรง `HYP-PF-042` จริง

รายละเอียดเต็ม: `rounds/A_20260901_2252_4h2nzu_ground-check-api-plus-hyp042-ack-first-reorder.md`

PF-AUTOMERGE: v4

-- LANE-A (WORLD) round `4h2nzu`
