# LANE-CS round ovkikh — 2026-09-09T15:13+07:00 ถึง 2026-09-09T15:5x+07:00

## ล็อกรอบ
`pf_bridge#1990` `[LANE-CS] round ovkikh: claim` เปิดไว้แล้วก่อนแตะโค้ด (list ซ้ำตอนเปิด: ไม่มี
ใบ `[LANE-CS]` อื่นเปิดแข่ง) รอบนี้เป็นการต่อรอบเดิมข้ามเทิร์น — เทิร์นก่อนหน้าเขียนโค้ดและ
เปิดเทสเสร็จแล้ว จบเทิร์นกลางทางระหว่างรอ `pytest tests/` ชุดเต็มที่รันเบื้องหลัง ยังไม่ได้ push/
เปิด PR เซิร์ฟเวอร์/ปลดล็อก เทิร์นนี้ปิดขั้นที่เหลือทั้งหมด

## รอบนี้สืบทอดจากรอบ cg3nrb
รอบก่อน (`cg3nrb`) ปิดสองงาน (`2220`/`2150`) ขึ้น `pirate-force-server#1186` (merge แล้ว) แต่
รันชุดเต็มไม่จบ (kill ที่ ~52%) — carryover ข้อ 2 ของรอบนั้นคือ "รันชุดเต็มให้จบรอบเดียว" ซึ่งรอบ
`ovkikh` นี้ทำสำเร็จ (ดูหัวข้อ เทสและเกต)

## จดหมายที่บริโภครอบนี้
`20260908_2141_COO-DECISION-re316-is-a-bounded-negative-the-number-stays-yours-LANE-CS.md`
(`.CONSUMED.txt` แล้ว, commit `8223d06`) — คำสั่งเจ้าของตรง: ชื่อ provenance ของ
`BIRTH_SKILL_POINTS_PROVENANCE` ต้องอ้าง RE-316 (บอกว่าทำไมไม่ใช่ตัวเลขที่วัดได้) ไม่ใช่แค่ label
`ASSUMPTION` เฉย ๆ

## งานที่ทำ (`pirate-force-server`, `pirate-force-server#1194`)

### 1) D1 ของ pf-adversary รอบ `mfgv4m` — `skill_learn_roundtrip.main()` ไม่เคยถูกเรียกจริง
- `src/pirateforce_foundation/skill_learn_roundtrip.py`: เพิ่ม `store.migrate()` ก่อนใช้ store ใน
  `main()` — ไม่งั้น `--db` พาธที่ยังไม่มีไฟล์ถูกส่งให้ sqlite3 เงียบ ๆ (สร้างไฟล์เปล่า ไม่มีตาราง)
  ทุกการอ่านหลังจากนั้น raise ถูกกลืนแล้วออกมาเป็นคำปฏิเสธเฉพาะเจาะจง
  `REFUSE_BALANCE_UNMEASURED` ทั้งที่จริงคือฐานข้อมูลไม่เคย migrate · `migrate()` เป็น call
  เดียวกับที่ fixture ของเทสเรียกอยู่แล้ว และเป็น no-op กับฐานข้อมูลจริงของเซิร์ฟเวอร์ (`app.py`
  migrate ตอนบูตอยู่แล้ว)
- `tests/test_skill_learn_roundtrip.py`: เพิ่มคลาส `TheConsoleEntryPointIsActuallyCalledTests`
  สามเทสที่เรียก `main()` จริงกับไฟล์ sqlite จริงบนดิสก์ (ทางเรียน exit 0/`RESULT=TOLD`, ทางปฏิเสธ
  exit 1/`RESULT=NOT_TOLD`, และรูปที่ adversary วัด — `--db` พาธที่ยังไม่มีไฟล์ ต้องถูก migrate
  ไม่ใช่โกหก) · เทสเดิมในไฟล์นี้ตรวจแค่ `callable(main)` — [วัดแล้ว] แทน body ทั้งก้อนด้วย
  `return 0` เดิมให้ 22 passed ไม่มีเทสไหนแดง หลังแก้ให้มิวแทนต์เดียวกันแดง 4 เทสในไฟล์นี้

### 2) COO-DECISION `20260908_2141` — RE-316 provenance
- `src/pirateforce_foundation/skill_point_curve.py`: คอมเมนต์เหนือ
  `BIRTH_SKILL_POINTS_PROVENANCE` เพิ่มย่อหน้าอ้าง RE-316 (คำขอ CharCreate ของไคลเอนต์เองไม่มี
  `ActorAttr` เลย ⇒ วัดค่าตั้งต้นจากไคลเอนต์นี้ไม่ได้ = bounded negative ไม่ใช่หลักฐานว่า 0 คือค่าที่
  วัดได้) · label ยังเป็น `ASSUMPTION` ค่ายังเป็น `0` เหมือนเดิม (`PANYA-DECISION 20260908_1218`
  ข้อ 3) — ไม่มีอะไรเปลี่ยนพฤติกรรม
- โทเคนตรวจ: `git grep -n "RE-316" src/` = อย่างน้อย 1 บรรทัด (พอใจเงื่อนไขที่ระบุใน
  `.CONSUMED.txt`)

## pf-adversary
`ADVERSARY_UNAVAILABLE` (เหมือนรอบ `cg3nrb`) — ค้นด้วย ToolSearch ("pf-adversary agent subagent",
"Task launch subagent adversary review") ไม่พบ tool Agent/Task ตัวไหนในเซสชันนี้ → self-review
แทน: อ่านทุก hunk ก่อน commit ทุกครั้ง (3 commit + merge) · ทั้งสาม commit ไม่แตะเส้นบูต/ล็อกอิน/
ตัวตนของ actor/เฟรมที่ส่งไคลเอนต์ (เฉพาะ CLI entry point `skill_learn_roundtrip.py`, เทสของมัน,
คอมเมนต์ล้วนใน `skill_point_curve.py`) → เปิด PR แบบไม่ draft ได้ตาม `HOWTO_OPEN_A_PR.md` · **สอง
รอบติดกันแล้วที่ไม่มี adversary ให้เรียก — รอบหน้าของสาย CS ต้องสั่งจริงเป็นงานแรกถ้ามี tool**

## เทสและเกต
- ระหว่างรอผลชุดเต็มรอบแรก `main` ของ `pirate-force-server` ขยับ (`pirate-force-server#1189`
  merge เข้า `main` — ไฟล์ LANE-UI ล้วน `Community_SendMailVital`/friend-request arming/wstring
  fuzz pin ไม่ทับไฟล์ของรอบนี้เลย) จึง `git merge origin/main` เข้ากิ่งอีกครั้ง (`6665c143`, ort
  strategy, ไม่มี conflict) **หลัง**ชุดเต็มรอบแรกรันจบ — ผิดลำดับที่ถูกต้องของกฎ "ชุดเต็มต้องรันบน
  ต้นไม้ที่ merge main แล้วเป็น commit สุดท้ายจริง ติดกับ push" (`COO-DECISION 20260904_1428` ข้อ
  4/`20260903_0053`) จึง**รันชุดเต็มซ้ำอีกครั้งบนต้นไม้ที่ merge แล้วจริง** (`6665c143`) ก่อนเปิด PR
  — บันทึกเป็นความผิดพลาดของรอบนี้ ไม่ปิดบัง
- ชุดเต็มรอบแรก (บน `f842cbd4`, ก่อน merge): `pytest tests/` (PYTHONPATH=src) =
  **15713 passed, 447 skipped, 0 failed, 43461 subtests passed** (1043.42s / 0:17:23)
- ชุดเต็มรอบสอง (บน `6665c143`, หลัง merge origin/main จริง — ต้นไม้เดียวกับที่ push/PR ใช้จริง):
  **15741 passed, 446 skipped, 0 failed, 43470 subtests passed** (1041.43s / 0:17:21) — ตัวเลข
  ต่างจากรอบแรกเล็กน้อย (skip นับต่าง 1, passed มากกว่า 28) เพราะ `#1189` (LANE-UI) มาพร้อมเทส
  ใหม่ของตัวเอง ไม่ใช่ของรอบนี้
- `python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server` (รันซ้ำบนต้นไม้หลัง
  merge ด้วย) = PASS ทุกช่อง (cp874/skips/mainmerge/census/branch/bridgesize/queuegrowth/
  filenamelen/scoreboard-manual/claudecfg/consumedstub/modebits) — `filenamelen` มีชื่อ 101
  ตัวอักษรของ `.CONSUMED.txt` stub ที่สืบทอดความยาวจากใบต้นทางบน `main` อยู่แล้ว (SKIPPED-open
  ตามกติกา ไม่ใช่ของใหม่ที่รอบนี้เลือกตั้งชื่อ)
- `python3 tools_bridge/pf_gate_preflight.py --pr-body <ไฟล์> --pr-stage final` = `[prbody] PASS`
  (มี `PF-AUTOMERGE: v4` บรรทัดเดียว) ก่อนเปิด PR เซิร์ฟเวอร์

## PR
- Server: `pirate-force-server#1194` — เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` จริง (GET ยืนยัน
  แล้วตอนเปิด — สถานะ "เปิดแล้ว รอเกต" ไม่ใช่ "อยู่บน main")
- Bridge claim: `pf_bridge#1990` — เติม marker ท้ายรอบนี้เพื่อปลดล็อก (GET ยืนยันหลังแก้)
- `#1595`/`#1629` (addenda ค้างของรอบ `l85fts`/`li5jc1`) — ไม่ใช่ของรอบนี้ จัดการไปแล้วในเทิร์น
  ก่อนหน้าของรอบ `ovkikh` เอง (เติม marker ให้ทั้งคู่, GET ยืนยันตอนนั้นแล้ว) `#1595` merge ไปแล้ว
  · `#1629` ยังเปิดรอเกต (มี marker) — ไม่มีอะไรต้อง push เพิ่มรอบนี้กับสองใบนี้

## รอบหน้าทำอะไร
1. **สั่ง pf-adversary จริงบน `pirate-force-server#1194` เป็นงานแรก** ถ้ามี tool ให้เรียกในรอบนั้น
   (เซสชันนี้ไม่มี — สามรอบติดกันแล้ว `cg3nrb`/`ovkikh`)
2. หนี้เก่าของ `skill_learn_roundtrip.py` จาก `CS_20260908_2109_mfgv4m_ADVERSARY-RESULT.md` ที่
   ยังไม่จ่าย: **D2** (double-spend บนสกิลเดียวกันพร้อมกัน คำนวณ points ผิด), **D3** (preflight
   ตัดสินได้ก่อนหักแต้มแต่ไม่ตัดสิน ⇒ ล็อกอินครั้งถัดไปพัง), **D4** (แต้มหายรายงานเป็น
   `refused`), **D5** (พิน AST หลบผ่าน absolute import ได้), **D6** (โทเคนหลักฐานไม่เทียบกับเป้า
   จริง), **D7/D8** (LOW — เอกสารเกิน/ล้างชั้นหลักฐานข้ามไฟล์)
3. คิว `NOW.md` สาย CS ข้อถัดไปหลัง `2220`/`2150` (จ่ายแล้วรอบ `cg3nrb`): CORE-REQUEST
   `learn_skill_spend` — ใบ `20260908_2109_LANE-CS-CORE-REQUEST-learn-skill-spend-seam.md` และ
   `20260908_2002_LANE-CS-CORE-REQUEST-learn-and-grant-need-one-transaction.md` ยังไม่มี
   `.CONSUMED.txt` → ยังรอ chief เสียบ ไม่ใช่ของรอบนี้ที่จะสร้างซ้ำ

## งานสำรอง (ทำเมื่องานหลักติด)
1. จ่ายหนี้ D5 (พิน AST `top_level` เทียบ absolute import ใน
   `tests/test_skill_learn_roundtrip.py`) — ไฟล์เดียวกับที่รอบนี้แตะแล้ว หลักฐานผ่านคือชุดเต็ม
   ยังเขียวและมิวแทนต์ absolute-import ของ D5 แดง
2. จ่ายหนี้ D4 (`spent=False` เมื่อ `points_after is None` ไม่มีเทสคลุมสาขา) —
   `src/pirateforce_foundation/skill_learn_roundtrip.py` หลักฐานผ่านคือเทสใหม่จำลอง
   `database is locked` แล้วยืนยันข้อความคำตอบไม่ทับกับ "แต้มหาย" อีกทาง
3. gold byte pin ของ opcode `0x673C` ที่ยังไม่มี (หนี้เก่าจาก `mfgv4m` ข้อสังเกต) —
   `tests/test_skill_learn_roundtrip.py` หลักฐานผ่านคือพินไบต์จับคู่กับ decoder จริงหนึ่งจุด

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-CS (เป็นของ chief ต่อ `GAME_TEST_QUEUE.md`) — ไม่ได้แตะคิว attended รอบนี้

SCOREBOARD: COMING | ปฏิบัติการที่เรียนสกิลผ่านเครื่องมือคอนโซล `skill_learn_roundtrip` จะไม่ได้รับคำตอบเท็จ "ยังไม่วัด" อีกต่อไปเมื่อไฟล์ฐานข้อมูลเพิ่งถูกสร้าง (ยังไม่กระทบผู้เล่นจริงในเกม เพราะเส้นทางนี้ยังเป็นเครื่องมือฝั่งเซิร์ฟเวอร์ ไม่ใช่โค้ดที่ล็อกอินจริงเรียก) และคอมเมนต์แหล่งที่มาของแต้มเกิด (ยังเป็น 0 เท่าเดิม) อ้างอิงหลักฐาน RE-316 ชัดเจนแทนป้าย ASSUMPTION เปล่า | pirate-force-server#1194 (4 commits รวม merge, preflight PASS, pytest 15741 passed/0 failed บนต้นไม้ merge origin/main แล้วจริง sha 6665c143)
