# LANE-A round `tmizmk`

2026-09-01T15:58+07:00 (+07:00 via `TZ=Asia/Bangkok date`).

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ไม่มีอะไรเลยบนหน้าจอในบูตปกติวันนี้ -- `production_allowed`
ของ `logout_dialog_open_hypothesis` ยังเป็น `False` ตาม stop_rule เดิม สิ่งที่เปลี่ยนคือกลไกภายใน
ตอนนี้ "สร้างได้จริง" ผ่านแฟล็ก CLI ที่มีอยู่แล้ว ซึ่งเป็นตัวปลดล็อกสุดท้ายที่ `GT-184`/`GT-185`/
`GT-186` ต้องการก่อนจะทดสอบแบบ attended ได้ในรอบถัดไป

## 0. ต้นรอบ: ตรวจชะตา PR รอบก่อน (ADDENDUM v2 ข้อ A)

ตรวจ `pull_request_read` ตรงบน PR รอบก่อนของสาย A ทั้งสอง repo:

- `pirate-force-server#481` (round `qw9tz4`) -- `merged: true` จริง (`merged_at` 2026-09-01T08:16:01Z)
- `pf_bridge#720` (round `qw9tz4`) -- `merged: true` จริง (`merged_at` 2026-09-01T08:03:17Z)

ไม่มีอะไรต้อง cherry-pick กู้ งานรอบก่อนอยู่บน main แล้วจริง

## 1. ตรวจล็อก + กล่องจดหมาย

ไม่มี PR `[LANE-A]` ค้างเปิดในทั้งสองรีโปตอนต้นรอบ (มี `[LANE-GM]` ค้างเปิดหนึ่งใบ ไม่ใช่ล็อกของสาย
นี้ ไม่แตะ) -- เปิด draft PR ยึดล็อก: `pirate-force-server#484`, `pf_bridge#724`

กล่องจดหมายที่ค้างถึงสาย A ตั้งแต่รอบ `qw9tz4`: ไม่พบใบใหม่ (grep `ADDRESSEE: LANE-A` ทุกใบที่ยังไม่มี
`.CONSUMED.txt` -- ใบเดียวที่ตรงคือ CORE-REQUEST ของสาย A เอง ซึ่งเป็นใบที่เปิดเอง ไม่ใช่ใบที่ต้อง
บริโภค) จดหมายใหม่ที่เข้ามาระหว่างนั้น (sync จาก Windows bridge) เป็นของ chief/COO/LANE-DB/Codex
ทั้งหมด ไม่มีใบไหน `ADDRESSEE: LANE-A`

อ่าน `NOW.md`: P-1/P-2/P-3 ไม่มีของให้สาย A ทำ (P-1 = LANE-B แล้ว, P-2 = LANE-GM static research,
P-3 = native-DLL นอกเขตทั้งสอง repo) GM-A บล็อกแค่รอ Panya รันเทส attended (กฎใหม่: ไม่ใช่ตัวบล็อก
สาย) UI-A/UI-B (`GT-184`/`185`/`186`) เป็นของสาย A และเป็นงานเดียวที่มีพื้นผิวจริงให้ทำต่อรอบนี้

## 2. สิ่งที่ทำ: ปิด allowlist blocker ของ `logout_hypothesis.py` เอง แทนที่จะรอ chief

รอบก่อน (`qw9tz4`) เปิด CORE-REQUEST ถามว่าใครควรแก้ `logout_hypothesis.py`'s allowlist (5 ตัว
เดิม ไม่มีที่ 6 สำหรับ `LOGOUT_RESPONSE_POLICY_WORLDINFO_DIALOG_OPEN_PUSH`) เพราะเห็นว่าไฟล์นี้
"หลายสายพึ่ง" และไม่แน่ใจว่าอยู่ในเขตเขียนของสาย A หรือไม่ ใบนั้นยังไม่มีคำตอบตอนรอบนี้เริ่ม

**รอบนี้ตัดสินเอง (ไม่รอ) ว่าจะแก้ตรง ๆ** เหตุผล: กฎเขตเขียนที่เขียนไว้จริงห้ามแก้เฉพาะ `runtime.py`
กับ `app.py` สองไฟล์ชื่อจริงเท่านั้น ไม่ได้ครอบคลุม "ไฟล์ที่หลายสายพึ่ง" ทั้งหมด และการแก้เป็น pure
addition ล้วน ย้อนกลับได้สะอาดถ้าผิด (`git revert 07e5f57`) **ป้ายกำกับ: [สมมติของสาย A -- รอ
COO/chief ยืนยัน]** รายละเอียดเต็ม+เหตุผล+revert path อยู่ในจดหมาย
`20260901_1558_LANE-A-STATUS-allowlist-fixed-in-zone-not-waited-for-chief-decision.md` (ใบใหม่)
และใบ CORE-REQUEST เดิมถูกขีดฆ่า+ต่อท้ายว่า SUPERSEDED (ไม่ลบของเดิม)

### รายละเอียดทางเทคนิค

เพิ่ม `_PROFILE_DIALOG_OPEN`/`_EXPECTED_DIALOG_OPEN` เป็น profile ที่หกใน
`src/pirateforce_foundation/logout_hypothesis.py` ตามรูปแบบ `_PROFILE_CHAT_PUSH`/`_EXPECTED_CHAT_PUSH`
เป๊ะ (ฟิลด์ `request_pc_sha256_*`/`ack_pc_sha256_*`/`ack_frame_sha256_*` ใช้ pinned constants ซ้ำจาก
chat-push เพราะกิ่งนี้ไม่ตอบ `LogoutVital` เช่นกัน) ลงทะเบียนเข้า `_EXPECTED_BY_ID` และเข้า tuple
allowlist ของ `require_logout_hypothesis_scenario()` **ไม่แตะ 5 profile เดิมแม้แต่บรรทัดเดียว**
(พิสูจน์: เทสของ 5 profile เดิมทั้งหมดผ่านไม่เปลี่ยนแปลง)

ไฟล์ใหม่ `scenarios/logout_hypothesis_dialog_open_push.json` -- generate จาก `_EXPECTED_DIALOG_OPEN`
โปรแกรมเมติกเพื่อกันไม่ให้ pin กับ source drift กัน

เทสใหม่ `tests/test_logout_dialog_open_scenario_wired.py` (7 เทส) -- ขับ branch นี้ผ่าน
`make_state_class`/`_dispatch_with_lanes` จริงเป็นครั้งแรก (ก่อนหน้านี้เทสของโมดูลนี้เรียกฟังก์ชัน
dispatch ตรง ๆ ด้วย fake connection เท่านั้น เพราะไม่มี allowlist profile ให้สร้าง state instance
จริงได้ -- ตรงกับที่ CORE-REQUEST เดิมของรอบ `qw9tz4` ขอไว้เป็น follow-up)

แก้ docstring ที่ค้าง (append `[STALE][MEASURED]`, ไม่ลบของเดิม) ใน
`logout_dialog_open_hypothesis.py` และ `test_logout_dialog_open_hypothesis.py` ให้ตรงกับสถานะจริง
(wired ตั้งแต่ PR #476, allowlist ที่หกมีแล้ว) และปรับ `docs/HYPOTHESIS_LEDGER.json`'s `HYP-PF-040`
เป็น tracked version `LOGOUT-DIALOG-OPEN-002` (amend ไม่ replace ฟิลด์เดิม) กับ
`tools/verify_hypothesis_ledger.py`'s pinned lineage/sha คู่กัน

**ไม่พลิก `production_allowed`** -- ยังเป็น `False` ตาม `HYP-PF-040`'s stop_rule ทุกประการ (ต้องรอ
attended `GT-184`/`GT-186` pass ก่อน)

## 3. ตรวจซ้ำเอง (ไม่ใช่แค่เชื่อ subagent ที่สร้างงาน)

ผมสั่งงานส่วนโค้ดให้ pf-builder subagent ทำจริง (เพราะ investigation+implementation ลึก) แล้วตรวจ
ซ้ำเองก่อนถือว่าจบ:

1. **base ล้าสมัย** -- branch ถูกสร้างจาก `origin/main` ที่ `13e229c` แต่ main เดินหน้าไปแล้วถึง
   `6d7db16` (LANE-DB's PR #480 merge, migration 006) ระหว่างที่ subagent ทำงาน -- `git diff main`
   ตอนแรกแสดง 253 ไฟล์เปลี่ยนซึ่งผิดปกติมาก ตรวจแล้วเป็นเพราะ base เก่าไม่ใช่งานจริงของรอบนี้ **merge
   `origin/main` เข้ามาสด** (clean merge, ไม่มี conflict) แล้ว diff เหลือ 7 ไฟล์ตรงกับที่ subagent
   รายงานเป๊ะ
2. รันเทสทั้งชุดเองอีกครั้งหลัง merge: `6348 passed, 327 skipped, 0 failed` (192.08s)
3. รัน `tools/verify_hypothesis_ledger.py` เอง: `PASS entries=48`
4. ตรวจ pf-adversary-equivalent ที่ subagent ทำเอง (ไม่มี Agent tool ให้เรียกในเซสชันย่อยรอบนี้ --
   ทำ manual review แทน): พบว่า subagent จับบั๊กจริงในร่างแรกของตัวเอง 2 จุดก่อนส่งงาน (เทสสมมติ
   fallback ผิด, marker annotation ซ้ำ) แก้แล้วก่อนส่ง -- อ่านซ้ำเองว่า diff เป็น pure-addition
   จริงตามที่อ้าง (ยืนยันด้วย `git diff origin/main` ด้านบน)

## 4. ไฟล์ที่แตะ

**pirate-force-server** (7 ไฟล์, PR `#484`):
- `src/pirateforce_foundation/logout_hypothesis.py` -- profile/allowlist ที่หก (เพิ่มเท่านั้น)
- `scenarios/logout_hypothesis_dialog_open_push.json` -- ใหม่
- `tests/test_logout_dialog_open_scenario_wired.py` -- ใหม่ (7 เทส)
- `src/pirateforce_foundation/logout_dialog_open_hypothesis.py` -- docstring correction (append)
- `tests/test_logout_dialog_open_hypothesis.py` -- docstring correction (append)
- `docs/HYPOTHESIS_LEDGER.json` -- HYP-PF-040 amend (append)
- `tools/verify_hypothesis_ledger.py` -- pinned lineage/sha update

**pf_bridge** (5 ไฟล์, PR `#724`):
- `GAME_TEST_QUEUE.md` -- GT-184/185/186 header + TOC บรรทัดอัปเดต (append, ไม่ลบของเดิม)
- `notes_to_chief/20260901_1446_LANE-A-CORE-REQUEST-*.md` -- ขีดฆ่า+ SUPERSEDED note (append)
- `notes_to_chief/20260901_1558_LANE-A-STATUS-allowlist-fixed-in-zone-not-waited-for-chief-decision.md` -- ใหม่
- `rounds/A_20260901_1558_tmizmk_logout_hypothesis_allowlist_sixth_profile.md` -- ไฟล์นี้เอง

## เทสที่รัน

```
targeted (7 files, subagent's run): 83 passed, 0 failed
python3 -m pytest tests/ -q  (ทั้งชุด, รันเองหลัง merge main สด)
=> 6348 passed, 327 skipped, 13717 subtests passed, 0 failed (192.08s)
python3 tools/verify_hypothesis_ledger.py
=> HYPOTHESIS_LEDGER PASS entries=48
```

## ยังไม่ได้พิสูจน์

- ว่า push `ReturnSelectServerVital 0x709E` ตอน GetWorldInfoVital-full-form (dialog-open) จริง ๆ
  พาไปหน้าเลือกตัวละครหรือไม่ -- นี่คือสิ่งที่ `GT-184`/`GT-186` มีไว้เพื่อวัด ยังไม่มีใครรัน attended
- ว่าการตัดสินใจแก้ `logout_hypothesis.py` เองแทนที่จะรอ chief เป็นการตัดสินใจที่ถูกต้องตามเขตเขียน
  จริง -- แจ้งเป็น[สมมติของสาย A]รอยืนยัน ไม่ใช่ข้อสรุปปิดเรื่อง

## 5. ASK-COO / chief

ดูจดหมาย `20260901_1558_LANE-A-STATUS-allowlist-fixed-in-zone-not-waited-for-chief-decision.md`
-- ไม่ใช่คำถามที่บล็อกงาน (ทำไปแล้ว) แต่ขอการยืนยันย้อนหลังว่าเขตเขียนตีความถูกต้อง

-- LANE-A (WORLD) round `tmizmk`
