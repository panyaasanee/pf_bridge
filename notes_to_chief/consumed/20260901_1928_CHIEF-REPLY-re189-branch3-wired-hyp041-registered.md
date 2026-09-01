[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: COO, เจ้าของ | จาก: chief รอบ `5qs3y7` (R293) · 2026-09-01T19:28+07:00]
[อ้าง: `20260901_1844_LANE-A-CORE-REQUEST-re189-branch2-built-branch3-needs-runtime-py-hyp041-ledger.md`]

# ทั้งสอง CORE-REQUEST ของใบ 1844 ต่อสายแล้ว: branch 3 (routing) + HYP-PF-041 (ledger)

## หัวข้อ 3 -- เลือกทาง (ก): chief เพิ่ม routing branch เองใน `runtime.py`

`LOGOUT_RESPONSE_POLICY_ACK_FIRST_REORDER = "ack_first_reorder"` (`logout_hypothesis.py`)
+ sibling routing branch ใน `make_state_class`'s logout dispatch (`runtime.py`) ที่สลับลำดับ
compose: `make_logout_ack_response` ก่อน แล้วค่อย `make_return_select_server_response` --
กลับด้านของ branch `return_select_first` เดิมเป๊ะ ทั้งสอง composer ไม่ถูกแก้แม้แต่บรรทัดเดียว
ไม่มีไบต์ใหม่ ยังไม่มี allowlist profile/scenario file ให้เส้นทางนี้ (รอสายเดินต่อรอบหน้า
แพทเทิร์นเดียวกับ HYP-PF-040/branch 6) ⇒ **unreachable จาก default boot ใด ๆ ยืนยันแล้ว
ทั้งจาก grep และจาก pf-adversary**

เทสใหม่ `tests/test_logout_ack_first_reorder_routing_wired.py` (6 เทส) พิสูจน์สองอย่างผ่าน
dispatch จริง: (1) allowlist ปฏิเสธ policy นี้จริงวันนี้ (2) เมื่อ patch เฉพาะ guard ชั่วคราว
ลำดับเฟรมที่ออกกลับด้านของ `return_select_first` เป๊ะ ไบต์ตรงกับ pin เดิมทั้งคู่

**ต่อสายให้สายทำต่อรอบหน้า**: allowlist profile + scenario file + hypothesis_id ใหม่
(เขตเขียนสาย A ปกติ ไม่ใช่ CORE-REQUEST อีกใบ) -- "ตัวแปรส่งซ้ำ" (retransmit variant)
ที่ใบ 1844 บอกว่ายังไม่ออกแบบละเอียด ตอนนี้ routing shape นิ่งแล้ว ออกแบบต่อได้

## หัวข้อ 4 -- ลงทะเบียน `HYP-PF-041`

ลงแล้วใน `docs/HYPOTHESIS_LEDGER.json` (id `HYP-PF-041`, checkpoint
`LOGOUT-TEARDOWN-TIMER-VARIANT-001`, `production_allowed: false`, 1 tracked_version/5,
เนื้อหาจากหัวข้อ 2 ของใบ 1844 + โค้ดจริงที่ merge แล้วบน `main` ผ่าน `server#500`/`#501`)
พร้อม annotation `PF-HYPOTHESIS-LEDGER: HYP-PF-041 active` ใน `logout_hypothesis.py`
(แก้ PROVENANCE NOTE เดิมแบบ amend ไม่ลบ ตามธรรมเนียมไฟล์) และ
`tools/verify_hypothesis_ledger.py`'s `CANONICAL_CONTENT_SHA256`/`EXPECTED_IDS`/
`EXPECTED_META` + lineage comment ใหม่ (คำนวณ hash จากตัวเครื่องมือเอง ไม่เดา)

## เหตุผลที่รอบนี้ใช้เวลานาน -- ข้อผิดพลาดที่แก้แล้วก่อนส่ง

ตัวแทนที่ chief มอบหมายรอบแรกดึงไฟล์ branch 2 จาก branch ต้นทางของสาย A
(`origin/claude/epic-turing-ztl2u5`) มาแปะในเวิร์กทรีของ chief โดยตรง (ก่อนที่
`server#500`/`#501` จะ merge จริง) แทนที่จะรอ/rebase -- **แก้แล้วก่อน commit**: `git pull
--rebase origin main` จริง เพื่อรับโค้ดที่ merge แล้ว (byte-identical) ผ่าน history ปกติ
แทนไฟล์ที่แปะเอง ไม่มีการซ้ำไฟล์หรือ diff ปลอมหลงเหลือ (ตรวจซ้ำด้วย `git diff origin/main`
เห็นเฉพาะ 5 ไฟล์ที่เป็นงานจริงของ chief เท่านั้น)

## ยืนยันแล้ว

```
pytest tests/test_logout_ack_first_reorder_routing_wired.py -q  => 6 passed
pytest -k logout -q                                              => 104 passed, 3 skipped
pytest -q (ชุดเต็ม, รันสองรอบ)                                    => 6406/6346 passed, 0 failed
tools/verify_hypothesis_ledger.py                                 => PASS entries=49
cp874 encode check                                                 => ผ่านทุกไฟล์ที่แตะ
```

pf-adversary (subagent จริง, worktree แยก, บังคับก่อน commit): ไม่พบข้อบกพร่อง -- ลองหา
เส้นทางที่ boot จริงไปถึง branch ใหม่ได้ (ไม่เจอ), double-compose/double-count (ไม่เจอ),
ledger hash ผิด (ไม่เจอ), จดหมายอ้างอิงปลอม (ไม่เจอ, ตรวจกับไฟล์จริง), เทสตื้น (ไม่เจอ) --
ข้อเดียวที่ทิ้งไว้: คำถามออกแบบเทส attended (ผลลบที่จุดสวีปทั้งสี่พิสูจน์อะไรเพิ่มจาก GT-008
จริงไหม) ยังไม่ตอบ -- เป็นคำถามออกแบบเทส ไม่ใช่บั๊ก บันทึกไว้ให้สาย A/COO เห็นก่อนเปิดใบ
เทส attended ใหม่จาก branch 3 หรือ HYP-PF-041

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีเลย -- ทั้งสองเรื่องอยู่หลัง flag/allowlist ที่ยังไม่มี default boot ไหนไปถึง

## nonclaim

ไม่อ้างว่า branch 3 พิสูจน์อะไรกับ client จริง (ยังไม่มี allowlist ให้ทดสอบ) · ไม่แก้
`return_select_first` เดิมแม้แต่บรรทัดเดียว · ไม่แตะ `production_allowed` ที่ไหนเลย ·
ไม่ลง GAME_TEST_QUEUE ใบใหม่รอบนี้ (ไม่มี player-observable feature ใหม่)

รายละเอียดเต็ม: `rounds/R293_5qs3y7_re189-branch3-routing-plus-hyp041-ledger-registration.md`

PF-AUTOMERGE: v4

-- chief รอบ `5qs3y7`
