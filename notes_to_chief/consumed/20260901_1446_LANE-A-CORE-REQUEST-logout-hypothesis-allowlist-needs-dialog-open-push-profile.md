[ถึง: chief | ADDRESSEE: chief | จาก: LANE-A (WORLD) รอบ `qw9tz4` · 2026-09-01T14:46+07:00]

# CORE-REQUEST: `logout_hypothesis.py`'s allowlist needs a sixth profile before GT-184/185/186 can ever boot

## บริบท

รอบ `liq4ri` (R288, ยืนยันจริงบน `main` HEAD `4ff782b`, PR `pirate-force-server#476`) ต่อสาย
`logout_dialog_open_hypothesis.py` เข้า `runtime.py` ครบตามที่ CORE-REQUEST ก่อนหน้าของสาย A ขอ
(counter init, import, routing branch ทาง (a)) และเพิ่ม `LOGOUT_RESPONSE_POLICY_WORLDINFO_DIALOG_OPEN_PUSH`
ใน `logout_hypothesis.py` (บรรทัด 176) แล้ว -- ตรวจสอบเองบน main จริง ไม่ได้เชื่อแค่ broadcast letter

**แต่ยังไม่มีทางสร้าง `logout_hypothesis_scenario` object ที่มี `response_policy` เท่ากับค่านี้ได้เลย**
`require_logout_hypothesis_scenario()` (`logout_hypothesis.py`, ท้ายไฟล์) เช็ค allowlist แบบ hardcode
5 ตัว (`_PROFILE_ECHO`, `_PROFILE_ACK_CLOSE`, `_PROFILE_WORLDINFO_FIRST`, `_PROFILE_RETURN_SELECT`,
`_PROFILE_CHAT_PUSH`) -- ไม่มีตัวที่หกสำหรับ `worldinfo_dialog_open_push` -- และ `app.py`'s
`--logout-hypothesis-scenario` flag (ผ่าน `load_logout_hypothesis_scenario`) ก็เช็ค `id` กับ
`_EXPECTED_BY_ID` เดียวกันนี้ ดังนั้น**แม้ `logout_dialog_open_hypothesis.production_allowed` จะเป็น
`True` วันนี้ กิ่งใหม่ก็ยังบูตไม่ได้จากทางใดเลย** -- ยืนยันด้วย `docs/HYPOTHESIS_LEDGER.json`'s
`HYP-PF-040` entry เอง (`accepted_ceiling` ระบุเหตุผลเดียวกันนี้ตรงตัว)

`logout_hypothesis.py` เป็นไฟล์ที่หลายสายพึ่ง (`hostile_hp_link_hypothesis`, `chat_input_hypothesis`,
`channel_message_hypothesis`, `delete_actor_hypothesis`, `population_scenario` ทั้งหมดใช้ pattern
`require_*_hypothesis_scenario` แบบเดียวกันในไฟล์เดียวกันนี้) ไม่ใช่ "โมดูลใหม่ของสาย A" ตามเขตเขียนของ
สายนี้ -- ขอให้ chief แก้เอง หรือระบุว่าสายไหนเป็นเจ้าของไฟล์นี้จริง ๆ ถ้าไม่ใช่ chief

## สิ่งที่ขอให้ต่อสาย (สเปกละเอียด)

ใน `logout_hypothesis.py`, ตามรูปแบบ `_PROFILE_CHAT_PUSH`/`_EXPECTED_CHAT_PUSH` เป๊ะ (บรรทัด ~728-770):

1. เพิ่ม `_PROFILE_DIALOG_OPEN_PUSH = LogoutHypothesisScenario(scenario_id="logout_hypothesis_dialog_open_push", hypothesis_id="HYP-PF-040", ...)` -- ฟิลด์ที่เหลือ (`request_pc_sha256_*`, `ack_pc_sha256_*`, `ack_frame_sha256_*`) เดาว่าเหมือน `_PROFILE_CHAT_PUSH` (ใช้ pinned constants เดิมซ้ำ เพราะกิ่งนี้ไม่ตอบ `LogoutVital` เลย เหมือน chat-push) แต่ **สายนี้ไม่มีสิทธิ์ยืนยันฟิลด์พวกนี้เอง** -- ผู้ที่ต่อสาย `runtime.py` รอบ `liq4ri` (pf-adversary + chief) ควรเป็นคนเคาะค่าที่ถูกต้อง ไม่ใช่สาย A เดา
2. เพิ่ม `_EXPECTED_DIALOG_OPEN_PUSH` dict คู่กัน (schema เดียวกับ `_EXPECTED_CHAT_PUSH`, `production_allowed: false`, `hypothesis_id: "HYP-PF-040"`)
3. เพิ่มทั้งคู่เข้า `_EXPECTED_BY_ID` และเข้า tuple allowlist ใน `require_logout_hypothesis_scenario()` (บรรทัดที่เช็ค `value not in (...)`)
4. ผลที่ได้: `--logout-hypothesis-scenario <path-to-json>` (flag ที่มีอยู่แล้วใน `app.py:144`, generic, ไม่ต้องแก้ `app.py`/`runtime.py` เพิ่มอีก) จะเลือก policy นี้ได้จริงเป็นครั้งแรก -- นี่คือ construction path ที่ `GT-184`/`GT-185`/`GT-186` ต้องการ เพื่อให้ทดสอบ attended ได้เลย

## ทำไมสายนี้ไม่ทำเอง

`logout_hypothesis.py` ไม่ใช่โมดูลใหม่ของสาย A และไม่ใช่ `runtime.py`/`app.py` -- อยู่กึ่งกลางระหว่างสอง
กฎเขตเขียน ขอให้ chief ตัดสินว่าใครแก้ (chief เอง หรือมอบให้สาย A แก้ในเขตนี้ครั้งเดียวก็ได้ ถ้า chief
เห็นว่าปลอดภัยเพราะเป็นการเติมแถวใหม่ไม่แตะของเดิมเลย)

## 🔴 ห้ามพลิก `production_allowed` แม้ต่อสายนี้เสร็จ

`docs/HYPOTHESIS_LEDGER.json`'s `HYP-PF-040` `stop_rule` เขียนไว้ตรงตัว: *"Do not flip
`logout_dialog_open_hypothesis.production_allowed` to True before an attended GT-184/GT-186 pass
and a fresh pf-adversary read of the wired runtime.py branch."* -- สายนี้เห็นแล้ว จะไม่พลิกแฟล็ก
จนกว่าจะมีรอบ attended จริงผ่านก่อน แจ้งไว้กันสายอื่น/รอบถัดไปพลิกเร็วไปด้วย

## pf-adversary รอบนี้

เรียก pf-adversary agent จริงในเซสชันนี้ (มี tool ให้เรียก รอบนี้ผิดปกติจากที่ KA1A เคยรายงานว่าสาย A
เสีย GitHub MCP/pf-adversary ซ้ำ ๆ) ให้ตรวจ wiring ของรอบ `liq4ri` อีกครั้ง (fresh read ตามที่
stop_rule ต้องการก่อนวันที่จะพลิกแฟล็กได้จริง) ผลอยู่ในไฟล์รอบ -- verdict **SAFE-TO-FLIP** ทางเทคนิค
วันนี้ (unreachable, ไม่ double-count, one-shot latch ถูกต้อง) **แต่สายนี้ไม่พลิกแฟล็ก** เพราะ
stop_rule ต้องการรอบ attended ผ่านจริงด้วย ไม่ใช่แค่ pf-adversary read เพียงอย่างเดียว

**พบเพิ่ม (จะเป็นประโยชน์กับผู้ต่อสาย allowlist):** ยังไม่มีเทสไหนขับ branch นี้ผ่าน wired
`runtime.py` path จริง (`tests/test_logout_dialog_open_hypothesis.py` เรียกฟังก์ชัน dispatch ตรง ๆ
เท่านั้น) เพราะไม่มี allowlist profile ให้สร้าง state instance จริงได้ -- เมื่อเพิ่ม profile ที่หกแล้ว
ขอให้รอบนั้นเพิ่มเทสแบบ `test_logout_worldinfo_first.py` (ขับผ่าน `make_state_class`/
`_dispatch_with_lanes` จริง) ให้ branch นี้ด้วย ไม่ใช่แค่เพิ่ม profile เฉย ๆ

-- LANE-A (WORLD) round `qw9tz4`
