# R176 (session modest-newton-r95s49 / sweet-franklin-r95s49) — ต่อสาย CORE-REQUEST-003/004 เข้า runtime.py, ปิด pf-adversary สองข้อ, อัปเดต GT-078 + REAL_SERVER_DIVERGENCE, เคลียร์กล่องจดหมาย 6 ใบ

เวลา: 2026-08-26 ~14:5x-16:0x (+07:00) = ~07:5x-09:0x UTC
สาย: E (PLATFORM) · chief cloud

## สรุปหนึ่งย่อหน้า

ไม่มี PR `[LANE-E]`/WIP round claim เปิดค้างทั้งสอง repo (PR ที่เปิดอยู่ `pf_bridge#113` และ
`pirate-force-server#59` เป็น `[LANE-B]` ไม่ใช่ล็อกของสายผม) ⇒ จับล็อกด้วย empty commit + draft PR
`pf_bridge#115` / `pirate-force-server#60` (`PF-AUTOMERGE: v4` ตรงเป๊ะ ทั้งคู่ยืนยันแล้วว่า `draft:true`
จริง). งานหลักของรอบนี้คือ **`CORE-REQUEST-003`/`004`** ที่สาย A ค้างมาสามรอบติด (`hfcnmk` → `jcczgc`
→ `irgnc3`) เพราะเป็นจุดเรียกใน `runtime.py`/`app.py` ซึ่งเป็นเขตของ chief คนเดียว — ต่อสายครบทั้งสามจุด
ของ `004` (`world_travel_gate.preload()` + `scenario_stand_down(active_lanes)` ตอนบูต ·
`TravelGateSet.from_preloaded()` ใน `__init__` · `observe()`/`confirmed_fields()` สองเฟสในเส้นทาง
`TargetPos` ดีฟอลต์) และจุดเดียวของ `003` (`world_scene_entry.resolve_entry()` แทนที่การอ่านพินแยกจาก
แถวเดิม พร้อม handler เฉพาะสำหรับ `SceneEntryRefused`) **ก่อน commit ส่งให้ `pf-adversary` รีวิวหนึ่งรอบ
ตามกฎบังคับ — เจอสองข้อจริง แก้ครบก่อน push:**

1. 🔴 **(สูง) ข้อผูกพันการเซสชันค้างถาวร** — โค้ดร่างแรกตั้ง `start_game_reply_sent = True` และคอมโพส
   `actions` ของ `START_GAME_RES` **ก่อน** เรียก `resolve_entry()` ลึกเข้าไปในบล็อกย่อย ⇒ ถ้า `resolve_entry`
   ปฏิเสธ (`SceneEntryRefused`) โค้ดคืน `[]` ทิ้ง action ที่คอมโพสไว้แล้ว **แต่ latch ยังติดอยู่** ⇒ ไคลเอนต์
   ไม่ได้รับ reply อะไรเลย และ retry `START_GAME_REQ` ใบต่อไปถูกการ์ดที่หัวฟังก์ชันบล็อกเงียบตลอดไป —
   pf-adversary reproduce จริงผ่าน dispatcher จริง ไม่ใช่แค่อ่านโค้ด ⇒ **แก้โดยย้าย `resolve_entry()` ให้รัน
   ก่อนสิ่งที่ commit ใด ๆ (inventory sync, latch, การคอมโพส action)** เหมือนแพทเทิร์นเดิมของ
   `except (KeyError, PermissionError)` รอบ `select_and_start` — รีโปรดิวส์ซ้ำเองแล้วยืนยันว่า retry
   สำเร็จหลังการแก้ (`start_game_reply_sent` ยังเป็น `False` หลังปฏิเสธ, retry ครั้งถัดไปสำเร็จจริง)
2. 🟡 (กลาง) `tools/pf_damage_model_headless_replay.py` ปิด `stdout_guard` แบบไม่ exception-safe
   (ไม่มี `try/finally` ต่างจากไฟล์พี่น้อง `pf_ground_loot_nameprop_headless_replay.py` ที่แก้พร้อมกัน) —
   ปฏิบัติจริงตอนนี้ไม่พังเพราะทั้งสองเครื่องมือถูกเรียกผ่าน subprocess เท่านั้น (process exit คืน stdout ให้
   เองอยู่แล้ว) แต่เป็นบั๊กจริงถ้าถูกเรียกในโปรเซสเดียวกันในอนาคต ⇒ **แก้ด้วยการห่อ body ทั้งก้อนด้วย
   `try/finally` ให้เหมือนไฟล์พี่น้อง** รีโปรดิวส์เองแล้วยืนยันว่า `sys.stdout` กลับมาเป็นของจริงแม้ `main()`
   raise กลางทาง

สวีตเต็มเขียว(cloud sanity) **`3089 passed, 327 skipped, 4986 subtests passed, 0 failed`** ทั้งก่อนและ
หลังการแก้สองข้อของ pf-adversary และหลัง merge `origin/main` (Lane B PR#59 เข้ามาระหว่างรอบ ไม่ชนไฟล์
ที่แตะเลย) · push `pirate-force-server` commit เดียว (`67ff98d`) 4 ไฟล์: `runtime.py`,
สองเครื่องมือ headless replay, และ re-pin `checkpoint_calls_at_try_depth_zero: 3 -> 4` ใน
`reports/PF_MULTIPLAYER_READINESS_AUDIT001_*.md` (ตัวเลขที่ตรวจสอบสดจริงด้วยตัวเอง ไม่ใช่การเดา — audit
tool re-derive ด้วย AST walk ของมันเอง).

## สิ่งที่ทำ

1. **การ์ดกันรอบซ้อน** — `git fetch --all` ทั้งสอง repo ตรวจ PR เปิดค้างด้วย `list_pull_requests`:
   พบ `pf_bridge#113` และ `pirate-force-server#59` แต่หัวข้อขึ้นต้น `[LANE-B]` ⇒ ไม่ใช่ล็อกของผม ไม่แตะ
   ไม่จบรอบ ⇒ จับล็อกเอง (empty commit + draft PR) `pf_bridge#115` / `pirate-force-server#60` ยืนยัน
   `draft:true` จริงทั้งคู่ผ่าน `pull_request_read`
   - 🔴 ระหว่างจับล็อก เผลอรัน `git commit --allow-empty` ผิด repo หนึ่งครั้ง (เขียนข้อความของ
     `pirate-force-server` ลง `pf_bridge` เพราะ cwd เพี้ยนข้าม tool call) — จับได้ก่อน push ด้วย
     `git status`/`git log` แล้วแก้ด้วย commit ชี้แจงต่อท้าย (ไม่ใช้ reset ตามกฎ) ก่อนจับล็อกที่ถูกต้องจริง
2. **เคลียร์กล่องจดหมาย** — 6 ใบที่ยังไม่บริโภค (ทั้งหมดของช่วง 12:50-14:42): สามใบ `LANE-A-STATUS`
   (ยืนยันซ้ำว่ายังบล็อกที่ `CORE-REQUEST-003/004`), `GT-078-RESULT` + `GT-078-ADDENDUM` (ผลเทส M1/v1
   attended — เจ้าของปฏิเสธ identity ของ NPC ทุกตัวแม้ตำแหน่งถูก), `COO-DECISION-GT078` (สั่งเก็บใบเปิด
   ห้ามเขียน v1) — อ่านครบ ตัดสินใจ ทำ copy+stub เข้า `consumed/` ครบทั้ง 6 (ไม่มีการลบต้นฉบับ)
3. **`CORE-REQUEST-003`/`004`** — งานหลักของรอบ รายละเอียดเต็มอยู่ใน commit message ของ
   `pirate-force-server@67ff98d` แล้ว ไม่ทวนซ้ำที่นี่ สรุปสั้น: ต่อสายครบตามสเปกของสาย A
   (`notes_to_chief/consumed/20260826_0645_LANE-A-CORE-REQUEST-004-v2-*.md` +
   `20260826_0245_LANE-A-GT-079-*.md`) และเงื่อนไขของ COO
   (`20260826_0655_COO-DECISION-CORE-REQUEST-004-*.md`) ครบทั้งสองข้อ (ไม่สร้าง `TravelGateSet` บนเส้นทาง
   ล็อกอิน · guard เป็นเพรดิเคตจาก `active_lanes` ไม่ใช่รายชื่อมือ) · ผ่าน `pf-adversary` หนึ่งรอบตามกฎ
   บังคับก่อน commit สิ่งที่ไม่ใช่การแก้คำผิด พบสองข้อ (ดูสรุปย่อหน้าบน) แก้ครบก่อน push
   - **สาย A ยังไม่ทดสอบเห็นฉาก 278 ขึ้นจอ** — ใบนี้ยังไม่ปิด รอ `GT-081` เป็นผู้ตัดสิน
   - **ไม่แตะ `session.py`** เพื่อส่ง `entry.position` เข้า `projector.start_game()` (แก้ปัญหา
     ActorAttr/MovementAttr ยังถือพิกัดท่าเรือแม้ teleport ถือจุดพินแล้ว — สาย A ยกเป็นคำถามเปิดให้ chief
     ตัดสินร่วมรอบเดียวกัน) **เลื่อนออกไปตั้งใจ**: ต้องหาตำแหน่งดึงแถวดิบก่อนเรียก `select_and_start` ซึ่ง
     `FoundationSession.select_and_start` ยังไม่มีจุดให้แทรก และการแก้ตรงนั้นเสี่ยงกระทบทุกคอลของ
     `start_game` (รวมบ้าน) โดยไม่มีเทสของสาย A คลุมกรณีนี้ ⇒ **เขียนไว้เป็นช่องว่างที่รู้** ไม่ใช่รีบแก้ใต้
     ความกดดันเดดไลน์ — บันทึกไว้ให้รอบถัดไปหรือ COO ตัดสินว่าจะทำเมื่อไหร่
4. **`GT-078`** — อัปเดตหัวใบใน `GAME_TEST_QUEUE.md` จาก "BLOCKED — รอ merge" (สถานะก่อนรัน) เป็น
   "RAN · wire PASS · OWNER-REJECTED (identity) — ห้ามปิดเป็น PASS" ตามผลจริงและคำตัดสินของ COO · เก็บ
   ถ้อยคำเดิมทั้งก้อนไว้เป็น strikethrough ประวัติ ไม่ลบ
5. **`REAL_SERVER_DIVERGENCE.tsv`** — เติม 4 แถวตามที่ใบ `GT-078-RESULT` ขอชัดเจน ("chief เติมเอง ห้าม
   ผมแก้ไฟล์"): โครงป้ายชื่อ (บรรทัดเดียว vs สองบรรทัด) + identity ที่ตำแหน่ง Hields/Sase/Columbus ×3 —
   ตรวจ sha256 ของภาพอ้างอิงที่ commit แล้วเองก่อนอ้าง (`REF_ORIGINAL_SERVER_*.jpg` =
   `61fb15f5...`, `GT078_S1_FULLRES_*.png` = `af1b58d4...` ตรงกับที่จดหมายอ้างทั้งคู่) · แถวที่ยังไม่มีภาพ
   ของเราเอง sync เข้าคลาวด์ (เช่น `GT078_CENTER_FULLRES`, in-game screenshot) ทำเครื่องหมาย
   `evidence_in_repo=partial` และเขียนตรง ๆ ว่าไฟล์ไหนยังไม่ sync แทนที่จะอ้างว่ามี
6. **`AGENTS.md`** — เพิ่มกฎไฟล์แฟล็ก (`Read-Flag`/`Write-Flag`/ASCII-only สำหรับ `LOCK_*.txt` +
   `PANYA_PRESENT.txt`) ตาม `COO-DECISION LOCK_GAME-was-920MB` ที่ยังไม่เคยถูกเขียนลงเอกสารตรง ๆ มา
   ก่อน (มีแต่กฎ ABORT/try-finally ที่แยกกันคนละเรื่อง ซึ่ง R175 เขียนไปแล้ว) — พร้อมรายชื่อจ็อบที่ยังค้าง
   (`1097 1100 1103 1143 1153 1154 1170`) ระบุชัดว่างานแก้จ็อบเหล่านี้เป็นของฝั่งสะพาน chief คลาวด์ทำเอง
   ไม่ได้เพราะไฟล์เหล่านั้นไม่ sync เข้า clone คลาวด์

## สิ่งที่ตรวจแล้วว่า "ทำไปแล้วก่อนหน้า" — ไม่ต้องทำซ้ำ (v6 prompt §18 มีสี่ในห้าข้อที่ทำไปแล้ว)

v6 prompt (2026-08-26) §18 มีงานค้างห้าข้อ ตรวจสถานะจริงในรีโปก่อนลงมือทุกข้อ:

- **ข้อ 2 (กฎ ABORT เชิงโครงสร้าง)** — R175 เขียนลง `AGENTS.md` + `staged/TEMPLATE_teardown_generic.ps1`
  บล็อก 7 ไปแล้ว (มีวันที่ "chief R175 · 2026-08-26" อยู่ในคอมเมนต์จริง) — ไม่ต้องทำซ้ำ
- **ข้อ 3 (พิน 48 พร้อมชื่อ)** — R172 ทำไปแล้ว (`docs/PYTEST_SKIP_PINS.json` +
  `tests/test_pytest_precondition_census.py` มี `test_the_modules_the_gate_hides_are_pinned_by_name`
  อยู่แล้ว) — ไม่ต้องทำซ้ำ
- **ข้อ 4 (`GT-033` → ANSWERED)** — R166 ปิดไปแล้ว (`GAME_TEST_QUEUE.md` แสดง "✅ ANSWERED — ปิดโดย
  chief R166" อยู่แล้ว) — ไม่ต้องทำซ้ำ
- **ข้อ 5 (heartbeat)** — R175 เดินสายไปแล้วใน `pf_git_sync.ps1` (`[2c] bridge heartbeat` ทุก ≥15 นาที)
  + `notes_to_chief/_BRIDGE_HEARTBEAT.txt` มีบรรทัดจริงจากรอบ 14:42 — ไม่ต้องทำซ้ำ
- **ข้อ 1 (`GT-001` samePos "แก้แล้วรันผ่านจริง")** — 🔴 **นี่คือข้อความเท็จเดียวกับที่ R175 ตรวจแล้วว่า
  สืบไม่ถึงเอกสารใดในรีโป และเขียนคืนสถานะ HOLD ไปแล้ว** (`GAME_TEST_QUEUE.md` หัวใบ `GT-001` มีบล็อก
  "R175 correction" อธิบายไว้ครบ) — v6 prompt ที่ผมได้รับยังคงมี bullet เดียวกันนี้ค้างอยู่ (แหล่งที่มาคือ
  `HANDOVER-CHIEF-PROMPT-v6-full` ซึ่ง R175 เองก็ระบุว่าเป็นต้นทางของข้อความเท็จนี้) ⇒ **ไม่ทำตาม ไม่แตะ
  `GT-001`** ยึดผลตรวจของ R175 เป็นความจริง ไม่ใช่ prompt ที่ยังไม่ได้อัปเดตให้ตรงกับที่ R175 แก้แล้ว —
  บันทึกไว้ให้ COO/Panya ทราบว่า prompt v6 มีข้อความค้างที่ผิดอยู่ 1 จุด (§18 ข้อ 1) ควรลบทิ้งในเวอร์ชันถัดไป

## ผลตรวจ

สวีตเต็มเขียว(cloud sanity) `3089 passed, 327 skipped, 4986 subtests passed, 0 failed` — รันสี่ครั้งตลอด
รอบ (ก่อนแก้/หลังแก้/หลัง merge main/ครั้งสุดท้ายก่อน push) เขียวทุกครั้ง ผ่าน `pf-adversary` หนึ่งรอบตามกฎ
บังคับ พบสองข้อ แก้ครบและ verify ด้วยการรีโปรดิวส์เองอีกครั้งก่อน commit

## ที่ยังค้าง / ส่งต่อ

- `GT-081` (สาย A) ยังต้องรอ attended test ยืนยันว่าฉาก 278 ขึ้นจอจริงหรือไม่ — ตอนนี้ต่อสายแล้วแต่ยังไม่มี
  ใครเห็นด้วยตา
- `session.py` position-injection สำหรับ `ActorAttr`/`MovementAttr` — ช่องว่างที่รู้ ยังไม่แก้ (ดูข้อ 3 ด้านบน)
- `GT-078` เปิดค้าง รอตาราง placement→identity จากสาย A + RE (Hields/Sase/Columbus อย่างน้อยสามตัวอย่าง)
  แล้ว `pf-queue-author` จะร่างใบ retest
- v6 prompt §18 ข้อ 1 มีข้อความเท็จค้างอยู่ — เสนอ COO/Panya ให้ตัดออกในเวอร์ชันถัดไปของ prompt
- `checkpoint_calls_at_try_depth_zero` re-pin (3→4) เป็นผลข้างเคียงที่ถูกต้องของการต่อสาย ไม่ใช่ drift
- ไม่ได้แตะ `CHIEF_CONTINUATION.md` เกิน ~110KB แล้ว (เกินเกณฑ์ ~100KB ที่แนะนำ housekeeping) — รอบหน้าที่
  มีที่ว่างควรย้ายรอบเก่าไป archive/
