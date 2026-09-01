# R288 (round `liq4ri`) — LANE-E (PLATFORM)

เวลา: 2026-09-01T~14:2x+07:00 (TZ=Asia/Bangkok)

## บริบทต้นรอบ

1. `pf_bridge/NOW.md`: ไมล์สโตนทั้งหมดยังพักไว้ (`PANYA-ORDER 20260901_0215`) งานด่วนตอนนี้คือ P-1/P-2/P-3
   ยังไม่ขยับข้อไหน (ไม่ใช่ของ chief รอบนี้) — คิวต่อ GM-A/UI-A/GM-B/UI-B/census latch มีของให้ทำ
   (ดูข้อ COO-DECISION 1341 ด้านล่าง) · หัวข้อ "รอ Panya ติ๊ก" ว่าง
2. การ์ดกันรอบซ้อน: ไม่มี PR `[LANE-E]`/WIP round claim ค้างในทั้งสองรีโป ก่อนเริ่ม (มีแต่ `[LANE-A]`
   `pf_bridge#712`/server`#474` และ `[LANE-B]` server`#475` — ไม่ใช่ล็อกของ chief ไม่แตะ) — จับล็อกด้วย
   `pf_bridge#715` / `pirate-force-server#476` (draft, marker `PF-AUTOMERGE: v4`)
3. ตรวจชะตา PR รอบก่อนของ LANE-E (`5jswxi`, R287): `pf_bridge#707` `merged:true`,
   `pirate-force-server#470` `merged:true` (ทั้งคู่ยืนยันด้วย `pull_request_read get`) — งานรอบก่อนอยู่
   บน main แล้ว ไม่มีอะไรต้องกู้
4. `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง — โครงพี่น้องปกติ
5. ทั้งสองสาขาที่ระบบมอบหมายให้เซสชันนี้ (`claude/happy-dirac-liq4ri`, `claude/focused-turing-liq4ri`)
   เป็น branch ที่ PR ก่อนหน้า merge ไปแล้ว — สร้างใหม่จาก `origin/main` ล่าสุดตามกติกา "merged branch
   ต้องเริ่มสด"

## CORE-REQUEST ที่ต่อสายรอบนี้ (ก่อนงานอื่นทุกอย่างตามกฎ)

มี CORE-REQUEST ค้างสองใบที่ถึง chief ในกล่องจดหมายวันนี้ (ทั้งคู่ต้องแก้ `app.py`/`runtime.py` ซึ่งเป็น
เขตของ chief):

### 1. CORE-REQUEST-DB-001 (LANE-DB, ใบ `20260901_1201_LANE-DB-REQUEST-*.md`)

ขอสองบรรทัดใน `app.py:784`/`:787`: `store.migrate()` -> `store.migrate_with_backup()`
(`migrate_with_backup` มีอยู่แล้วใน `store.py` จากรอบก่อนของ LANE-DB, PR `#472` merged) ทำตามที่ขอเป๊ะ
ทั้งสองจุด `migrate()` เดิมไม่ถูกแตะแม้ไบต์เดียว

seam test `tests/test_startup_stale_lease_recovery.py::test_every_recovery_call_follows_a_migration_in_its_own_block`
เช็คชื่อ attribute `"migrate"` แบบตรงตัว (ผ่าน AST) เลยแดงทันทีที่ชื่อ method เปลี่ยน — แก้ให้เช็คทั้ง
`"migrate"` และ `"migrate_with_backup"` โดยคง invariant เดิมไว้ครบ (migration call ต้องมาก่อน
`expire_open_sessions` ใน block เดียวกัน) พิสูจน์ด้วย pf-adversary (สร้าง scratch reachability ในสาขา
disposable worktree) ว่าไม่มีทางทำให้เทสผ่านทั้งที่ invariant พัง

**สิ่งที่ pf-adversary เจอและยังไม่แก้ (เปิดเป็นคำถามให้ LANE-DB/COO ไม่ใช่ของ chief แก้เอง):**
`migrate_with_backup()` ทำให้ boot path ปกติมีทางแดงใหม่ที่ `migrate()` เดิมไม่มี —
`persistence_backup.BackupError` (พื้นที่ดิสก์ไม่พอ/verify ล้ม) จะ raise ออกจาก `app.main()` ตรง ๆ
เพราะ `app.py` ไม่มี `try`/`except` จุดไหนเลย ไม่มีเทสไหนพิสูจน์ end-to-end ผ่าน `app.main()` จริง (มีแต่
เทสที่เรียก `migrate_with_backup()`/`persistence_backup` โดยตรง กับเทสที่เช็ค AST) — น่าจะเป็นพฤติกรรม
ที่ตั้งใจ (fail-closed ตาม charter ของ LANE-DB) แต่ยังไม่มีใครตัดสินใจว่า unhandled traceback คือ UX ที่
ยอมรับได้หรือควรมี `except BackupError` จับแล้ว log ให้ชัดแทน — นอกเขตของ CORE-REQUEST สองบรรทัดนี้
ไม่ตัดสินใจแทน แก้ docstring ที่ล้าสมัยของ `tests/test_persistence_premigration_backup.py` (เคยเขียนว่า
"no boot path calls migrate_with_backup yet" ซึ่งเท็จแล้วหลังรอบนี้) ให้ตรงกับความจริงใหม่แทน

### 2. LANE-A CORE-REQUEST (ใบ `20260901_1254_LANE-A-CORE-REQUEST-*.md`, GT-184/GT-186)

ต่อสายโมดูล `logout_dialog_open_hypothesis.py` (มี้อยู่แล้วบน main, merged, unit test 12 ตัวผ่านครบ)
เข้า `runtime.py` ตามที่ใบขอทุกจุด:
1. `self.logout_dialog_open_push_count = 0` ข้าง `logout_chat_push_count` (HYP-PF-031)
2. import `dispatch_logout_dialog_open_hypothesis` + module `logout_dialog_open_hypothesis`
3. เพิ่ม constant `LOGOUT_RESPONSE_POLICY_WORLDINFO_DIALOG_OPEN_PUSH` ใน `logout_hypothesis.py`
   (นอกเขตของ LANE-A ตามที่ใบระบุเอง — เป็นงานของ chief)
4. routing branch ใหม่ทาง **(a)** เท่านั้นตามที่ใบสั่งชัด (top-level branch คีย์ด้วย `response_policy`
   ใหม่ ไม่ nest เข้า `_dispatch_worldinfo_observation`) — pf-adversary ของ LANE-A เองในรอบก่อนตัดทาง
   (b) ทิ้งแล้วเพราะจะนับ `rx_frames` ซ้ำสอง เพิ่ม defensive gate อีกชั้น:
   `logout_dialog_open_hypothesis.production_allowed` (ยังเป็น `False`)
5. ลงทะเบียน **HYP-PF-040** ใน `docs/HYPOTHESIS_LEDGER.json` + `tools/verify_hypothesis_ledger.py`
   (`EXPECTED_META`/`EXPECTED_IDS`/hash pin) — `HYPOTHESIS_LEDGER PASS entries=48`

**ยังไม่ทำ (นอกเขตรอบนี้ตามที่ใบระบุ):** ไม่มี CLI/scenario construction path ให้เลือก policy ใหม่นี้ได้
จริงบน boot ใด ๆ — สาขานี้จึงยัง unreachable บน production path ทุกทาง `production_allowed` ยังเป็น
`False` `GT-184`/`GT-185`/`GT-186` ยังต้องรอ path นั้นก่อนถึงจะรัน attended ได้จริง

**pf-adversary (mandatory, isolated subagent, สร้าง disposable worktree แยกทั้งสองครั้ง):**
รันโมดูล/routing branch ผ่าน dispatcher จริงด้วย fixture จริง (268-byte full-form GetWorldInfoVital) —
ยืนยัน `rx_frames` เพิ่มครั้งเดียว ไม่ซ้ำสอง, one-shot latch ปฏิเสธเฟรมที่สองถูกต้อง,
`worldinfo_last_payload`/`worldinfo_stored_count` ไม่ถูกแตะตามที่ scope ระบุ (branch ใหม่ไม่เรียก
`_dispatch_worldinfo_observation`) — ยืนยันด้วยว่าสาขานี้ยังถูกกันอีกชั้นโดย
`require_logout_hypothesis_scenario`'s hardcoded 5-item allowlist (ยังไม่รวม policy ใหม่) — เพิ่ม
ย่อหน้าอธิบายจุดนี้ลง ledger's `accepted_ceiling` (AMENDED ไม่ใช่ replace) พร้อมปรับ hash pin ตาม
ไม่พบ defect จริงในโค้ดที่ commit

**registry CORE-REQUEST:** ไม่มีแถวใหม่ต้องเปิด — ทั้งสองใบเป็นคำขอตรงถึง chief ไม่ใช่ผ่าน
CORE-REQUEST registry table (แถวเปิดเดียวที่มี, 028, ยัง wired เหมือนเดิม ไม่แตะรอบนี้)

full suite ทั้งสองครั้งก่อน/หลัง amendment: 6265 passed / 327 skipped (cloud sanity) 0 failed

## งานอื่นที่ทำ (pf_bridge, doc-only)

### GT-192 (ตอบ `COO-DECISION 20260901_1341` ข้อ 1)

เปิด `GT-192 GM-A-WARP-MULTI-MAP-CENSUS-CHAIN-001` ท้าย `GAME_TEST_QUEUE.md` (เลข 192 จาก grep คำสั่ง
บังคับ) — วาปข้ามอย่างน้อยสามแมพติดกัน (ไม่ใช่ใบแรกของ login, `GT-182` พิสูจน์ใบแรกแล้ว) แล้วเช็ค NPC
ปกติทุกแมพ พิสูจน์ census latch fix ที่แก้แล้วบน `main` (`runtime.py:5459-5470` ที่ commit `81952ce`)
ตามสเปกใบ `1035`+`1120` ผู้ทำ **LANE-GM**

pf-adversary (worktree แยก) จับได้ว่า RECHECK bullet เดิมอ้าง `runtime.py:5468` ซึ่งเป็นเลขบรรทัดจาก
working tree ที่ยังไม่ commit ของ chief เอง (หลัง wire LANE-A's CORE-REQUEST เข้าไปแล้วบรรทัดขยับ) ไม่ใช่
เลขที่ commit `81952ce` ซึ่งเป็น precondition จริงของใบนี้เอง (ที่นั่นคือ 5459 ตรงกับที่เนื้อใบเขียนไว้เอง
สองย่อหน้าก่อนหน้า) — แก้ RECHECK ให้ยึดชื่อฟังก์ชันแทนเลขบรรทัด และระบุชัดว่า 5459 คือเลขที่ `81952ce`
เท่านั้น ไฟล์จะขยับต่อไปเรื่อย ๆ

### GT-182 TOC (ข้อ 2 ของใบเดียวกัน)

แก้บรรทัดสารบัญที่ยังเขียน `BLOCKED-ON-ATTENDED [NEEDS-ATTENDED-CAPTURE]` ให้ตรงกับผลจริงที่บรรทัดใบเต็ม
(`PASS -- OBSERVER_CONFIRMED 2026-09-01T10:40+07:00, chief round 8zf80f`) พร้อมชี้ไปที่ `GT-192`

### RE-193 (ตอบ `COO-DECISION 20260901_1325` ข้อ 2)

เปิด `RE-193 ACTORATTR-SEVEN-UNKNOWN-FIELDS-CLIENT-DEFAULT-VALUES-001 [STATIC-ON-BRIDGE]` ท้าย
`CLIENT_RE_QUEUE.md` (เลขคำนวณใหม่ = 193 เพราะ grep รันหลัง `GT-192` ลงไฟล์แล้ว หลีกเลี่ยงชนกัน) — หา
ค่า default ของ 7 ฟิลด์ `ActorAttr` ที่ LANE-DB ระบุว่าไม่มีทั้ง typed-column source และแถว codex
`default_writer_va` (`x=14`/`25`/`36`/`41`/`42`/`43`/`54`) ผู้ทำ **LANE-DB** ไม่เร่งด่วน (LANE-DB แก้เอง
แล้วว่า `/speed` เดินได้โดยไม่ต้องรอ)

ข้อ 1 ของใบเดียวกัน (ตัด item 4 ของใบ `1210` ออกจาก charter) **ตรวจแล้วไม่มีอะไรต้องทำ** — grep
`CHIEF_CONTINUATION.md`/`AGENTS.md` หา "1210"/"ห้ามเปิด canonical"/"state/pirateforce.sqlite3" ไม่เจอ
สักที่ แปลว่า item 4 ไม่เคยถูกลงทะเบียนไว้จริง (บล็อก charter ที่มีอยู่สะท้อนแค่ `COO-DECISION 1112`
อยู่แล้ว) — แจ้ง COO ในจดหมายผลว่าความกังวลไม่ตรงกับไฟล์จริง

pf-adversary (worktree แยกสามครั้งรวมของรอบนี้) ตรวจเลขคิว/G5/lane assignment/consumed-stub ทุกจุด —
ไม่พบ defect อื่นนอกจาก RECHECK ข้างบน (แก้แล้ว) และตั้งข้อสังเกต (ไม่ใช่ defect) ว่า grep กฎเลขใบไม่ครอบ
ไฟล์ archive บางประเภท (`archive/*_history_*.md`, `archive/CHIEF_CONTINUATION_ARCHIVE_*.md`) — ตรวจ
manual แล้วเลขสูงสุดในนั้นคือ 188 ไม่ชนกับ 192/193 รอบนี้ แต่เป็นช่องโหว่เชิงกลไกที่ยังไม่ได้แก้

## งานแม่บ้าน

- `git rm --cached` สองไฟล์ marker sync ตามใบ `1340` (ka1-A พิสูจน์แก้ `pf_git_sync.ps1` แล้วจริงบนสะพาน
  รอบสด 13:38 — เหลือแค่คำสั่งนี้ให้ chief) ไฟล์ยังอยู่บนดิสก์ แค่ untrack ตาม `.gitignore` ที่มี pattern
  อยู่แล้ว
- mailbox triage: stub 6 ใบที่ถึง chief วันนี้ (1254, 1201, 1341, 1325, 1340, 1230) — ใบ 1230 ข้อ 2
  พบว่าแก้แล้วจริงในใบ 1340 (ไม่ต้องทำซ้ำ) ข้อ 1/3 ไม่ใช่เขตของ chief (พรอมป์ของเจ้าของ /
  evidence_screens ของผู้เทส local)

## WIRED

`WIRED=5/5 unchanged` — รอบนี้ไม่แตะ `lane_hooks/` เลย โมดูลใหม่ที่ต่อสาย
(`logout_dialog_open_hypothesis`) ไม่ใช่ lane_hook (auto-discover) เป็น hypothesis module ที่ยัง
unreachable จาก production path จริง (ไม่มี CLI/scenario ให้เลือก + ยังติด allowlist ของ
`require_logout_hypothesis_scenario` อีกชั้น) จึงไม่นับเข้า WIRED v2

## ไม่ได้พิสูจน์ / ยังค้าง

1. `migrate_with_backup()` unhandled `BackupError` บน default boot path — เปิดคำถามให้ LANE-DB/COO
   ตัดสินใจ ไม่ใช่ chief ตัดสินใจแทน (ดูรายละเอียดข้างบน)
2. LANE-A's CORE-REQUEST ยังไม่ปิดสมบูรณ์ — ต้องมีรอบถัดไปที่เพิ่ม CLI/scenario construction path +
   เพิ่ม policy ใหม่เข้า `require_logout_hypothesis_scenario`'s allowlist ก่อน GT-184/185/186 จะรัน
   attended ได้จริง (ไม่ใช่ของรอบนี้ ใบไม่ได้ขอ)
2. ช่องโหว่ grep กฎเลขใบไม่ครอบไฟล์ archive บางประเภท — ไม่ชนรอบนี้ แต่ยังไม่แก้กลไก

## push แล้ว รอ merge PR

`pirate-force-server` PR (branch `claude/focused-turing-liq4ri`, commit `579a6bb`) และ `pf_bridge` PR
(branch `claude/happy-dirac-liq4ri`) — ยังไม่ merge จนกว่ารอบถัดไปยืนยัน `merged: true`
