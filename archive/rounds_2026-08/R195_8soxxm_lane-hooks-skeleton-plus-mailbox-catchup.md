# R195 (session 8soxxm) — lane_hooks skeleton (first move-out) + CORE-REQUEST registry catch-up + mailbox stubs

2026-08-27 ~16:5x-17:1x (+07:00)

## เป้าหมายรอบนี้

v6.3 หัวข้อ 18 ข้อ 1 (สัญญาไว้ตั้งแต่ R193/R194: "ทำเป็นลำดับแรกก่อนงานอื่น") — สร้าง
`lane_hooks/` skeleton ใน `pirate-force-server` ตามสถาปัตยกรรมที่เจ้าของอนุมัติ
(`notes_to_chief/20260827_1230_PANYA-ORDER`, ack `20260827_1241_COO-DECISION`)
เพื่อถอด chief ออกจาก critical path ของการต่อสาย CORE-REQUEST ทุกใบ

## สิ่งที่ทำ

### 1. `src/pirateforce_foundation/lane_hooks/` (ใหม่)

- `__init__.py` — registry ผ่าน decorator `hook(point)`, `fire(point, **kwargs)`,
  auto-discovery ด้วย `pkgutil.iter_modules` (สแกนไฟล์ `lane_<x>_*.py` ทุกไฟล์
  ในไดเรกทอรีนี้ ไม่มีรายชื่อกลางที่ต้องอัปเดต)
- **fail-closed by construction**: `fire()` ครอบทุก hook ด้วย `try/except Exception`
  พิมพ์ `LANE_HOOK <module> <point> ERR <repr>` แล้วไปต่อ hook ถัดไป — ไม่ raise ออกไปหา
  caller ไม่มีทางที่ hook ของเลนหนึ่งจะทำให้ listener thread ทั้งเธรดตาย
- **สอง token ต่อ hook** ตามที่กฎขอ: `LANE_HOOK_REGISTERED` ที่ import time (**stderr**)
  และ `LANE_HOOK_FIRED` ที่ยิงจริงบน production path (**stdout**)
- 🔴 **`pf-adversary`/เทสจับได้จริงระหว่างรอบ**: token ลงทะเบียนตอนแรกพิมพ์ลง stdout
  ทำให้ `test_the_replay_tool_json_mode_reports_a_pass_verdict` และ
  `test_ground_loot_nameprop_hypothesis`'s json-mode test พังทันที (เครื่องมือ headless
  replay สองตัวคาดหวัง JSON ล้วนบน stdout เมื่อรัน `--json`, ไม่เกี่ยวกับ hook นี้เลยแต่
  import `runtime.py` แล้วโดน print ปนเข้าไป) — แก้โดยย้าย registration print ไป stderr
  (fire print ยังอยู่ stdout เหมือนเดิม เพราะยิงเฉพาะตอน dispatch จริงของ vital นั้น ไม่ใช่
  ทุกครั้งที่ import)

### 2. `src/pirateforce_foundation/lane_hooks/lane_gm_run_command.py` (ใหม่ — ตัวอย่างที่ย้ายมา)

ย้ายตรรกะ authorize/capture/event ของ `CORE-REQUEST-010` (LANE-GM, inbound
`GM_RunGMCommandVital` 0x51E9) ออกจากบล็อก inline ใน `runtime.py` มาไว้ที่นี่ทั้งหมด
เลือกบล็อกนี้เพราะเล็กที่สุดในบรรดา CORE-REQUEST ที่ต่อสายแล้ว: หนึ่ง vital id ขาเข้า
หนึ่งฟังก์ชันปลายทาง ไม่มีการ thread ค่ากลับไปประกอบ response — ตรงกับรูปแบบจุดเสียบ
"(ค) รับ vital ขาเข้าตาม id" ของกฎ lane_hooks พอดี

`runtime.py` เหลือแค่: นับเฟรม (`self.rx_frames += 1`) + เรียก
`lane_hooks.fire("vital_inbound_gm_run_command", session=self, payload=...)` + return `[]`
— ตัดการ import `handle_gm_run_command_vital` ตรงออกจากไฟล์นี้ (เหลือแค่
`GM_RUN_GM_COMMAND_VITAL_ID` ที่ยังต้องใช้เช็ค `nested_id`)

**พฤติกรรมไม่เปลี่ยนไบต์เดียว**: `tests/test_gm_run_command_dispatch_wiring.py` (มีอยู่แล้ว,
ไม่แก้) บูต headless เต็ม แล้วเช็ค `self.events`/ไม่มี reply frame ตรงกับก่อนย้ายทุกกรณี

### 3. `tests/test_lane_hooks.py` (ใหม่)

หกเทสสำหรับแพ็กเกจเอง (แยกจากเทส regression ของ hook จริงที่มีอยู่แล้ว):
discovery หา hook จริงเจอ, `fire()` เรียกทุก hook ตามลำดับ, `fire()` บน point ที่ไม่มีใคร
ลงทะเบียน = no-op เงียบ, hook ที่ throw ถูกจับและ hook ถัดไปยังรันต่อ, token ลงทะเบียน
ไป stderr, token ยิงจริงไป stdout

### 4. `pf-adversary`

เรียกก่อน commit ตามกฎบังคับ — ผลกลับมาจริงระหว่างรอบ (ไม่ต้องรอรอบถัดไป) พบ 4 ข้อจริง
แก้ครบก่อน push:

- 🔴 **HIGH**: `_discover()` เดิมไม่มี try/except รอบการ import แต่ละไฟล์ — ไฟล์
  `lane_<x>_*.py` ใหม่ในอนาคตที่มี bug ตอน import (typo, reference ผิด) จะทำให้
  `importlib.import_module` throw ทะลุออกจาก `_discover()` → ทะลุออกจาก
  `lane_hooks`'s own top-level import → ทะลุออกจาก `runtime.py`'s `from . import
  lane_hooks` → **ทะลุออกจาก `app.py` ฆ่าทั้งโปรเซส บูตไม่ขึ้นเลยทุกสาย** — ขัดกับสัญญา
  fail-closed ของแพ็กเกจเองตรง ๆ (ประกันไว้แค่ระดับ `fire()` ไม่ใช่ระดับ import) แก้ด้วย
  `_import_module_safely()` (แยกออกมาเป็นฟังก์ชันแยกเพื่อเทสตรง ๆ ได้) จับ `Exception`
  รอบการ import แต่ละโมดูล พิมพ์ `LANE_HOOK_DISCOVERY <module> IMPORT_FAILED <repr>`
  แล้วข้ามไปโมดูลถัดไป — แยก(isolate)ที่ระดับไฟล์ ไม่ใช่ล้มทั้งกระบวนการ
- 🔴 **MEDIUM**: `production_allowed` (กำหนดไว้ชัดใน `PANYA-ORDER 1230`/`COO-DECISION 1241`
  ว่าเป็นเกตเดียวกับทุกโมดูลเดิม) หายไปจากทั้งแพ็กเกจ — เพิ่ม `production_allowed = True`
  ที่ `lane_gm_run_command.py` (ตามธรรมเนียมโมดูลที่ shippable ทุกตัวในโปรเจกต์) +
  `_discover()` เช็ค `getattr(module, "production_allowed", False)` หลัง import สำเร็จ
  โมดูลที่ไม่ประกาศ (หรือ `False`) ถูก `_withdraw()` hook ของตัวเองออกจาก `_HOOKS` ทันที
  ไม่มีสิทธิ์ยิงจริง
- **MEDIUM**: `fire()`'s error print ไม่มีการ์ด cp874 — ถ้า hook ในอนาคต (เช่น say/chat)
  ใส่ข้อความที่มาจาก client ลง exception message จะ `UnicodeEncodeError` ซ้อนใน
  except-handler เอง (บทเรียนรอบ 86/142 ของโปรเจกต์) แก้ด้วย `_console_safe()`
  (`encode('ascii','backslashreplace')`) ครอบทุกข้อความที่พิมพ์จาก `fire()`/`_discover()`
- **LOW**: docstring เดิมอ้างว่า "grepped by WIRED v2" เป็นข้อเท็จจริงที่วัดแล้ว ทั้งที่ไม่มี
  สคริปต์ grep จริงในรีโปนี้ตอนนี้ — แก้คำเป็น "designed to be grepped by" (เป้าหมาย ไม่ใช่
  กลไกที่มีอยู่แล้ว) และเติมหมายเหตุว่า `fire()` จับแค่ `Exception` ไม่ใช่ `BaseException`
  ให้ตรงกับโค้ดจริง (docstring เดิมพูดกว้างเกินสิ่งที่โค้ดรับประกัน)

จุดที่ตรวจแล้วไม่พบข้อบกพร่อง (รายงานตามที่ขอ): import cycle ของ hook ตัวเดียวที่ย้ายมา
(ไม่มี), double-registration ตอน re-import (กัน้วย `_DISCOVERED` + `sys.modules` cache),
thread-safety ของ `_HOOKS` (เขียนครั้งเดียวตอน import แบบ single-threaded ก่อน listener
thread เริ่ม), `rx_frames`/`return []` contract (พิสูจน์ด้วยเทสเดิมที่ไม่แก้), เทส cleanup
ภายใต้ pytest-xdist (ไม่เปราะ — process แยกกัน)

ข้อที่รับทราบแต่ไม่แก้รอบนี้ (นอกขอบเขต PR แรก, บันทึกไว้เป็นคำเตือนสำหรับ hook ถัดไป):
circular-import trap ถ้า hook ในอนาคตต้อง import symbol จาก `runtime.py` เอง (คำถามค้าง
ของ CORE-REQUEST-006/014 ที่ยังไม่ย้าย) — เขียนเตือนไว้ใน docstring แล้ว ไม่ใช่ปัญหาของ
hook ตัวเดียวที่ย้ายรอบนี้ (import แค่ `gm.dispatch` ซึ่งไม่มีทางย้อนกลับมาที่ `runtime`/
`lane_hooks`)

### 5. เทส

`tests/test_gm_run_command_dispatch_wiring.py` + `test_gm_command_dispatch.py` +
`test_gm_command_capture.py` (30 ข้อ, ตรงจุดที่ย้าย) ผ่านหมด · `tests/test_lane_hooks.py`
(10 ข้อ — 6 เดิม + 4 ใหม่จากการแก้ตาม `pf-adversary`: import ล้มเหลวถูกจับ, module ไม่มี
`production_allowed` ถูกถอน hook, ข้อความไม่ใช่ ASCII ไม่ทำให้ error print พัง, module จริง
ประกาศ `production_allowed`) ผ่านหมด · สวีตเต็ม (ยกเว้น 23 ไฟล์ที่ import `capstone` ไม่ได้บน
cloud — ข้อจำกัดเดิม ไม่เกี่ยวรอบนี้): **3316 passed, 198 skipped, 3573 subtests passed,
0 failed** เขียว(cloud sanity) · `tools/verify_hypothesis_ledger.py` = PASS entries=47
(ไม่มี diff, รอบนี้ไม่แตะ ledger) · `tools/verify_functional_coverage.py` = PASS domains=8
(8 domain ยัง incomplete ตามเดิม ไม่ใช่ของใหม่รอบนี้) · `git diff --check` เงียบ · ไฟล์ใหม่
ทั้งหมด `git check-ignore`/`git add --dry-run` ยืนยันไม่ถูก ignore

### 6. `CORE-REQUEST` registry (`pf_bridge/CHIEF_CONTINUATION.md`)

เติมแถวที่ตกหล่นสามแถว (006-010 เคยถูกทำสรุปย่อไว้แล้ว แต่ 015/016/017 ไม่เคยมี):

- **015** = LANE-B `mob_pickup.dispatch_pickup_request()` — บล็อกรอ RE opcode decoder
  ไม่เร่ง nonclaim 15 ตอบแล้ว (`runtime.py` ต้องเช็ค identity ไม่ใช่ `mob_pickup.py`)
- **016** = LANE-GM `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED` guard — **ต่อแล้วจริงบน
  `main` ตั้งแต่ R194** (แค่ backfill เอกสารรอบนี้)
- **017** = LANE-GM `login_scene_override` (login-scene override สำหรับบัญชี GM) —
  🔴 **จดหมายต้นทางเขียนเลข "015" ผิด**: ชนกับใบของ LANE-B ที่ยื่นก่อน 10 นาที
  (`1514` vs `1524`) chief ขยับเป็น `017` ตามกฎ "ชนแล้วห้ามทับ" จุดที่ 1 (login) wireable
  จริงแต่ **ยังไม่ต่อสายรอบนี้** (priority ให้ lane_hooks skeleton ก่อนตามที่ R194 สัญญาไว้) —
  ตั้งใจทำรอบถัดไปผ่าน `lane_hooks/lane_gm_*.py` แทนการแก้ `runtime.py` อีกครั้ง จุดที่ 2
  (ผสม census ข้าม LANE-A/LANE-B) ยังไม่มีฟังก์ชันให้เรียก รอ chief ตัดสินใจสถาปัตยกรรม

`CORE-REQUEST-012` (LANE-GM `say_wire`) ยังบล็อกเหมือนเดิม (ไม่มีทาง decode `GmCommand`
ชนิด `say` จาก client จริง) — ไม่มีอะไรเปลี่ยนรอบนี้ นอกจาก backfill stub ที่ขาดไป

### 6b. บทเรียน: เขียนทับ stub เดิมของ 3 ใบโดยไม่ตั้งใจ

ระหว่างเคลียร์กล่องจดหมาย พบว่าเขียน `.CONSUMED.txt` ทับของเดิมที่ R191/R194 เขียนไว้แล้วจริง
สำหรับ 3 ใบ (`1514` LANE-B, `1524`-015 LANE-GM, `1600` LANE-GM) — เช็คลิสต์
"unconsumed" ที่ทำตอนต้นรอบ (คู่ `.md`/`.CONSUMED.txt` เทียบชื่อ) ทำถูกสำหรับไฟล์อื่นทั้งหมด
ที่ตรวจย้อนกลับ (เช่น `1743_COO-DECISION-WIRED-metric` ยังไม่มี stub จริง) แต่สามใบนี้ถูกหยิบมา
เขียนใหม่จาก grep เนื้อหาตามหัวข้อโดยตรง ไม่ได้ตรวจกับผลเช็คลิสต์ก่อน เนื้อหาใหม่ไม่ผิด
(อัปเดตสถานะปัจจุบันจริง ๆ และ 1524 ยิ่งไปแก้ปัญหาเลขชนที่ stub เดิมทิ้งไว้เป็นคำถามค้าง) แต่
ต้นฉบับ `.md` ในทั้ง `notes_to_chief/` และ `consumed/` ยังอยู่ครบไม่มีอะไรหาย — ไม่ใช่ข้อมูลสูญหาย
แค่ประวัติการ attribution ของ stub รุ่นก่อนถูกแทนที่ บันทึกไว้กันรอบถัดไปพึ่งผลเช็คลิสต์อัตโนมัติ
เท่านั้น ไม่ผสมกับการ grep เนื้อหาแล้วเขียนทับโดยไม่เช็คซ้ำ

### 7. กล่องจดหมาย

Stub ย้อนหลัง ~15 ใบที่อ่านและตัดสินใจแล้วจริงรอบนี้ (ธุรกรรม ADDENDUM v6.2 item G,
CORE-REQUEST 012/015/016/017 thread, GM state-vital-version thread) — **ยังไม่ครบ**
backlog ทั้งกล่อง (วัดต้นรอบ: >100 ใบไม่มี stub ย้อนไปถึง 26 ส.ค. 17:30) เหลือเป็นงาน
รอบถัดไปต่อเนื่อง ไม่ใช่รอบเดียวจบ

## nonclaim

- ไม่มีอะไรเปลี่ยนที่ผู้เล่นเห็น — รอบนี้เป็น refactor ล้วน (byte-identical wire behavior
  สำหรับ CORE-REQUEST-010's call site) บวก doc/registry bookkeeping
- `lane_hooks/` ยังมี hook จริงแค่ตัวเดียว — ยังไม่พิสูจน์ว่าใช้งานได้กับจุดเสียบที่ซับซ้อนกว่า
  (เช่นจุดที่ต้อง thread ค่ากลับเข้า response ที่ประกอบอยู่ เช่น CORE-REQUEST-006/014)
- ไม่ได้ต่อสาย CORE-REQUEST-017 จุดที่ 1 รอบนี้ แม้ wireable จริง — เลือก priority
  lane_hooks skeleton ก่อนตามสัญญา R194 ไม่ใช่ทำทั้งสองพร้อมกันเสี่ยง "ไม่จบครั้งเดียว"
- กล่องจดหมายยังไม่ครบ backlog — stub 15 ใบจาก >100 ใบที่ค้าง

## GAME_TEST_QUEUE

ไม่มีรายการใหม่รอบนี้ — ไม่มีอะไร client-observable ที่เปลี่ยน (เหตุผลตามกฎหัวข้อ 11)

## WIRED v2

ไม่เปลี่ยน (10 เลนเดิม, `lane_hooks` ยังไม่ใช่หนึ่งใน 10 เลนที่วัด — ย้ายที่อยู่ของ wiring ที่
วัดอยู่แล้ว ไม่ใช่เลนใหม่)
