# LANE-A round `qw9tz4`

2026-09-01T14:41+07:00 - (กำลังดำเนินอยู่, +07:00 via `TZ=Asia/Bangkok date`).

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ไม่มีอะไรเลยบนหน้าจอ -- รอบนี้เป็นบัญชี/verify-only บริโภคจดหมาย
สองใบที่ค้างถึงสาย A แล้วเปิด CORE-REQUEST ใหม่หนึ่งใบ ไม่แตะโค้ดเกม

## 0. ต้นรอบ: ตรวจชะตา PR รอบก่อน (ADDENDUM v2 ข้อ A)

รีเซ็ต branch ทั้งสอง repo จาก `origin/main` สด (พบว่า branch ที่ตั้งชื่อไว้ `claude/epic-turing-sgo1pn` /
`claude/dazzling-volta-sgo1pn` ไม่เคยมีอยู่บน remote มาก่อน -- เริ่มจากศูนย์ตามกฎ "ถ้า merged แล้ว
restart จาก main") ตรวจ PR ล่าสุดของสาย A ทั้งสอง repo:

- `pf_bridge#712` / `pirate-force-server#474` (round `x4qlc7`) -- **merged=true จริง** (ยืนยันด้วย
  `pull_request_read` โดยตรง ไม่ใช่แค่เชื่อ `rounds/`) -- ตอนแรก list ทั่วไปแสดง `merged=false` เพราะ
  ดึงข้อมูลก่อน reaper ทำงาน แล้ว reaper merge ให้จริงระหว่างที่รอบนี้กำลังตรวจอยู่ (สังเกตได้จาก
  `merged_at` เทียบกับเวลาที่ดึงข้อมูล) -- ไม่มีอะไรต้อง cherry-pick กู้
- `pirate-force-server#476` (round `liq4ri`, LANE-E ไม่ใช่สาย A แต่ต่อสาย CORE-REQUEST ของสาย A) ก็
  merged=true แล้วเช่นกัน (`4ff782b`) -- ยืนยันด้วยการ grep โค้ดจริงบน HEAD ไม่ใช่แค่เชื่อ broadcast letter

## 1. บริโภคกล่องจดหมาย (ADDENDUM v2 ข้อ B)

จดหมายที่ค้างถึงสาย A ไม่มี `.CONSUMED.txt`:

1. `FROM_CHIEF_R288_TO_ALL_20260901_1420.md` ข้อ 1 (ถึง LANE-A) -- อ่านแล้ว: CORE-REQUEST ของสาย A
   (GT-184/GT-186 dialog-open) ต่อสายเข้า `runtime.py` แล้วจริง (ตรวจเองบน HEAD `4ff782b`: import,
   counter init, routing branch, constant ใหม่ครบตามที่ grep เจอ) แต่ยังบูตไม่ได้เพราะ allowlist ของ
   `require_logout_hypothesis_scenario` ไม่มี profile ที่หก -- เปิด CORE-REQUEST ใหม่ (ข้อ 3 ด้านล่าง)
   ตามที่จดหมายเชิญไว้ ("เขียนเป็น CORE-REQUEST ใหม่มาได้ถ้าต้องการให้ chief ต่อให้อีกรอบ")
2. `20260901_1435_KA1A-TO-LANE-A-*.md` (แก้ตัวเลข SLA ของ reaper: 55/45 **นาที** ไม่ใช่ 2/6 **ชั่วโมง**,
   ค่าจริงจาก `PF_STALE_MINUTES` ใน `merge-claude-pr.yml` แยกออกจาก `PF_STALE_HOURS`/
   `PF_STALE_CLOSE_HOURS` (เกณฑ์ปิดทิ้ง) ตั้งแต่ `PANYA-DECISION 20260901_0920`) -- รับแก้ จะอ่านค่าจาก
   `merge-claude-pr.yml` บน main จริงก่อนอ้างเวลาให้เจ้าของทุกครั้งต่อจากนี้ ไม่ใช้ค่าจากความจำ

ทั้งสองใบมี `.CONSUMED.txt` แล้วในรอบนี้ (เนื้อหาสรุปการกระทำอยู่ในสตับ)

## 2. สืบสวน CORE-REQUEST เก่าให้ครบก่อนเปิดใบใหม่

ก่อนเชื่อ broadcast letter ว่า "ต่อสายแล้ว" ตรวจโค้ดจริงเอง (`grep` บน `runtime.py`,
`logout_hypothesis.py`, `logout_dialog_open_hypothesis.py` บน HEAD `4ff782b`):

- ยืนยัน: import + counter init + routing branch (`nested_id`-keyed, ทาง (a)) มีจริงตามที่อ้าง
- ยืนยัน: `LOGOUT_RESPONSE_POLICY_WORLDINFO_DIALOG_OPEN_PUSH` มีจริงใน `logout_hypothesis.py:176`
- **พบเอง (ไม่ใช่แค่เชื่อ broadcast):** ไม่มี `_PROFILE_*` ตัวไหนใช้ค่านี้เป็น `response_policy` เลย และ
  `require_logout_hypothesis_scenario()`'s allowlist tuple ยังมีแค่ 5 ตัวเดิม -- ตรงกับที่
  `docs/HYPOTHESIS_LEDGER.json`'s `HYP-PF-040` entry (`accepted_ceiling`) บันทึกไว้เองพอดี ยืนยันสอง
  แหล่งตรงกัน
- **อ่าน `stop_rule` ของ `HYP-PF-040` เจอข้อห้ามชัดเจน**: ห้ามพลิก
  `logout_dialog_open_hypothesis.production_allowed` ก่อนมีรอบ attended ของ `GT-184`/`GT-186` ผ่านจริง
  **และ** pf-adversary อ่าน wiring ใหม่อีกครั้ง -- สายนี้จะไม่พลิกแฟล็กแม้ตอนนี้จะมี Agent tool ให้เรียก
  pf-adversary จริงในเซสชันก็ตาม (ดูข้อ 3)

## 3. pf-adversary รอบนี้ -- fresh read ตามที่ stop_rule ของ HYP-PF-040 ต้องการ

**มี Agent tool ให้เรียก pf-adversary จริงในเซสชันนี้** (ต่างจากรอบก่อน ๆ ที่ KA1A รายงานซ้ำว่าสาย A
เสีย GitHub MCP/pf-adversary -- บันทึกไว้เป็นข้อมูลอีกจุดสำหรับการสืบสวนของ ka1-A เรื่อง tool list ที่
`20260901_1355_KA1A-OBSERVATION-*.md`) เรียกให้ตรวจ wiring ของรอบ `liq4ri` อีกครั้งบนโค้ดจริงที่ merge
แล้ว (ไม่ใช่ diff ของ PR) โฟกัส: double-count ของ `rx_frames`, one-shot latch, และยืนยันอิสระว่า branch
ยังไม่มีทาง reachable จากบูตจริงใด ๆ

**ผล (agent จริงกลับมาแล้ว):** verdict = **SAFE-TO-FLIP** วันนี้ -- ตรวจสามทาง (อ่านซอร์ส, ลอง
สร้าง scenario ปลอมแล้วป้อนเข้า `require_logout_hypothesis_scenario` ใน worktree แยก จนได้
`ValueError`, และขับ branch จริงผ่าน `make_state_class`/`_dispatch_with_lanes` ด้วย monkeypatch
allowlist ชั่วคราว) ยืนยันตรงกันทั้งสามทาง: **ไม่มี** `_PROFILE_*` ใดพา
`LOGOUT_RESPONSE_POLICY_WORLDINFO_DIALOG_OPEN_PUSH` ได้เลยวันนี้, **ไม่มี** double-count ของ
`rx_frames` (สอง branch คนละค่าคงที่บนฟิลด์เดียวกัน แยกกันเชิงโครงสร้าง ไม่ใช่แค่ธรรมเนียม),
one-shot latch ทำงานถูกต้องจริง (ครั้งที่สองถูกปฏิเสธ, ตัวนับไม่ขยับ)

**พบบั๊กจริง 2 จุด (ไม่ใช่ severity สูง แต่แก้แล้วรอบนี้):**
1. `tests/test_logout_dialog_open_hypothesis.py`'s module docstring เขียนว่า "UNWIRED on main" ซึ่ง
   **เท็จแล้ว** ตั้งแต่ PR #476 merge -- แก้แล้ว (ขีดฆ่า ไม่ลบ ต่อด้วยคำแก้พร้อม citation ตามธรรมเนียม
   เดิม) เพราะข้อความเท็จนี้จะบังหมอกอีกจุดที่ยังจริงอยู่ (ข้อ 2 ด้านล่าง) ถ้าไม่แก้
2. **ยังไม่มีเทสไหนขับ branch นี้ผ่าน `runtime.py`'s wired path จริง** (`test_logout_worldinfo_first.py`
   มีแบบนั้นให้ policy พี่น้องของมัน แต่ไฟล์เทสของโมดูลนี้ยังเรียกฟังก์ชัน dispatch ตรง ๆ ด้วย fake
   connection เท่านั้น) -- ช่องว่างนี้ยังจริง เพราะไม่มี allowlist profile ให้สร้าง state instance จริง
   ได้ (ดูข้อ 4) ทิ้งไว้เป็น follow-up หลัง allowlist profile ลง ไม่ปิดช่องว่างเองตอนนี้เพราะต้อง
   monkeypatch allowlist ชั่วคราวซึ่งไม่ควร ship เป็นเทสถาวร

**การตัดสินใจเรื่องแฟล็ก:** แม้ verdict คือ SAFE-TO-FLIP ทางเทคนิค **สายนี้ไม่พลิก
`production_allowed`** เพราะ `HYP-PF-040`'s `stop_rule` เขียนเงื่อนไขไว้เป็น "และ" (ต้องมีรอบ
attended `GT-184`/`GT-186` ผ่านจริง **ด้วย**) ไม่ใช่แค่ "หรือ" -- นี่คือกฎที่ chief/pf-adversary
ตัดสินใจร่วมกันไว้แล้วในรอบ `liq4ri` (โปรเจกต์เคาะไว้เอง ไม่ใช่สายนี้ตีความเพิ่ม) ตรงกับ "(ค) ขัดกับ
คำสั่งที่เจ้าของ/โปรเจกต์เคาะไว้เองโดยตรง" ในกฎ "ติดแล้วต้องให้ COO เคาะ" -- แจ้งเรื่องนี้ชัดในจดหมาย
CORE-REQUEST เพื่อกันไม่ให้รอบถัดไปพลิกเร็วไปเพราะเห็นแค่ผล SAFE-TO-FLIP โดยไม่อ่าน stop_rule เต็ม

## 4. CORE-REQUEST ใหม่

`20260901_1446_LANE-A-CORE-REQUEST-logout-hypothesis-allowlist-needs-dialog-open-push-profile.md`
-- ขอให้ chief (หรือมอบสาย A ทำถ้า chief เห็นว่าปลอดภัย) เพิ่ม `_PROFILE_DIALOG_OPEN_PUSH` +
`_EXPECTED_DIALOG_OPEN_PUSH` เข้า allowlist ของ `logout_hypothesis.py` ตามรูปแบบ `_PROFILE_CHAT_PUSH`
เป๊ะ เพื่อให้ `--logout-hypothesis-scenario` (flag ที่มีอยู่แล้ว ไม่ต้องแก้ `app.py`) เลือก policy ใหม่นี้
ได้จริงเป็นครั้งแรก -- ปลดบล็อกทางสร้าง attended run ของ `GT-184`/`GT-185`/`GT-186` (แจ้งชัดในใบว่า
**ไม่ใช่การขอพลิก `production_allowed`** -- อันนั้นยังห้ามตาม stop_rule จนกว่าจะมีรอบ attended ผ่านก่อน)

## 5. ไฟล์ที่แตะ

**pf_bridge:**
- `notes_to_chief/FROM_CHIEF_R288_TO_ALL_20260901_1420.md.CONSUMED.txt` -- ใหม่
- `notes_to_chief/20260901_1435_KA1A-TO-LANE-A-*.md.CONSUMED.txt` -- ใหม่
- `notes_to_chief/20260901_1446_LANE-A-CORE-REQUEST-logout-hypothesis-allowlist-needs-dialog-open-push-profile.md` -- ใหม่
- `rounds/A_20260901_1446_qw9tz4_mailbox_triage_corerequest_dialog_open_allowlist.md` -- ไฟล์นี้เอง

**pirate-force-server** (1 ไฟล์):
- `tests/test_logout_dialog_open_hypothesis.py` (module docstring แก้ -- ขีดฆ่าประโยค "UNWIRED on
  main" ที่ล้าสมัยตั้งแต่ PR #476 merge + เขียนคำแก้พร้อม citation ไม่แตะ test logic ใด ๆ)

## เทสที่รัน

```
python3 -m pytest tests/test_logout_dialog_open_hypothesis.py tests/test_logout_worldinfo_first.py \
  tests/test_tree_is_cp874_safe.py -q
=> 33 passed, 467 subtests passed (7.69s)

python3 -m pytest tests/ -q  (ทั้งชุด)
=> 6298 passed, 327 skipped, 13373 subtests passed, 0 failed (194.60s)
```

จำนวนเทสไม่เปลี่ยน (docstring-only fix ไม่แตะ logic ใด ๆ) 0 failed ทั้งชุด

## 6. ASK-COO

ไม่มี -- ทุกการตัดสินใจอิงกับกฎที่มีอยู่แล้ว (allowlist แก้ไม่ได้เพราะนอกเขตเขียน, ห้ามพลิกแฟล็กเพราะ
stop_rule เขียนไว้ตรงตัว)

-- LANE-A (WORLD) round `qw9tz4`
