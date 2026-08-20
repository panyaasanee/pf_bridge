# PROPOSAL R107 — ปลูกแดงจงใจ (planted red) บน branch `gate-redtest`

**สถานะก่อนหน้า:** run #1 แดงเพราะ plumbing (false red) · run #2 แดงเพราะหมุดค้างยุค · run #3 แดงเพราะ 4 เทสล้ม · **run #4 เขียวหมด**
**กฎที่ chief เขียนเอง:** แดงที่ "บังเอิญเกิด" ไม่นับ — ต้อง **ปลูก** ถึงจะนับว่า gate ถูกพิสูจน์
**ข้อบังคับของ Panya:** ปลูกลง branch `gate-redtest` · เห็นแดงแล้วลบ branch · **`main` ห้ามถูกแตะแม้แต่ commit เดียว**

เอกสารนี้เป็น **ข้อเสนอ** ล้วน ๆ — ไม่มีการ commit / push / แก้ไฟล์ใน repo `Pirate Force ServerProject` เกิดขึ้นระหว่างเขียน ทุกตัวเลขในนี้อ่านมาจากไฟล์จริงที่ HEAD `9045978` (รอบ 106)

---

## 0. สรุปหนึ่งย่อหน้า

แนะนำให้ปลูก **อักขระ U+1F534 หนึ่งตัวต่อท้าย `tools/pf_move_cadence001_headless_replay.py`** — จะถูกจับที่ step 7 จาก 9 ชื่อ **`cp874 static tripwire`** ด้วยข้อความ `RED tools/pf_move_cadence001_headless_replay.py got=1 pinned=0` ภายในราว 90 วินาที เป็นบั๊กคลาสเดียวกับที่ทำให้ workflow นี้เกิดขึ้น (รอบ 142) หมุดชั้นเดียว ไม่มีช่องแดงอื่นปนบน CI และกู้คืนด้วยการลบ branch อย่างเดียว ตัวเลือกรองคือขยับหมุด skip 2→1 ซึ่งจะจุด `skip_census` — check ที่ **ยังไม่เคยเห็นแดงบน runner เลย** — แต่ช้ากว่า (~6 นาที) และพิสูจน์คนละชนิด

---

## 1. แผนที่ gate: ทุก step พร้อมกลไกที่ทำให้แดง

### 1.1 ตาราง A — 9 named steps ของ job (ไฟล์ `.github/workflows/gate-windows.yml`)

| # | ชื่อ step (ตรงตามไฟล์) | บรรทัด | กลไกที่ทำให้แดง | เป็น tripwire ที่ตั้งใจให้จับของ? |
|---|---|---|---|---|
| 1 | `Checkout (FULL history - not optional)` | 68 | action ล้มเอง · `fetch-depth: 0` จำเป็นเพราะ `mpaudit` เรียก `git ls-tree 5cc0eda` | ไม่ (plumbing) แต่เป็น precondition ของ `mpaudit` |
| 2 | `Pin the interpreter to the bridge's series` | 77 | setup-python หา 3.14 ไม่เจอ | ไม่ (plumbing) |
| 3 | `Make ``py -3`` mean the pinned interpreter` | 85 | เขียน shim ไม่สำเร็จ (`$ErrorActionPreference='Stop'`) | ✅ กัน "py -3 กลายเป็น Python ของ image" — divergence ชนิดที่ workflow นี้เกิดมาเพื่อกัน |
| 4 | `Install the packages the suite imports` | 114 | `throw 'pip self-upgrade failed'` / `throw 'dependency install failed'` | ไม่ (plumbing) — และเป็น step เดียวที่ปิด cp874 ชั่วคราว |
| 5 | `Assert the environment is the one we think it is` | 136 | `throw "CONSOLE CODE PAGE IS '$cp'..."` · `throw "INTERPRETER IS $ver..."` · `throw "STDOUT IS '$enc', EXPECTED 'cp874 strict' - the cp874 tripwire would be disarmed"` | ✅✅ **tripwire ชั้นที่ 1 ของ cp874** — พิสูจน์ว่าสภาพแวดล้อมคือของจริง |
| 6 | `SELF-CHECK - prove both tripwires are armed before trusting them` | 158 | `throw "SELF-CHECK FAILED: native exit did not propagate..."` · `throw 'SELF-CHECK FAILED: U+1F534 printed cleanly - the cp874 tripwire is DISARMED'` | ✅✅ **tripwire ชั้นที่ 2** — จับ *ตัวเอง* ก่อนจะเชื่อตัวเอง (นี่คือ step ที่ทำ run #1 false red) |
| 7 | `cp874 static tripwire (tools/, src/, current/)` | 197 | สคริปต์ฝังใน YAML สแกน `.py` ที่ tracked ใต้ `tools/ src/ current/` เทียบกับ dict `ALLOWED` (บรรทัด 228-232) · พิมพ์ `RED <path> got=N pinned=M` (บรรทัด 259) + `line N: codepoint 0xXXXX` (263) · `sys.exit(1)` (271) → PowerShell `throw 'cp874 static tripwire is RED'` (277) | ✅✅✅ **tripwire ชั้นที่ 3 — หมุด/pin** แดงได้ **สองทิศ**: `got > pinned` (ต้นไม้สกปรก) และ `got < pinned` (หมุดค้างยุค — ทิศที่ run #2 เจอ) |
| 8 | `Declare what this runner CANNOT check, and why` | 280 | แทบไม่มีทางแดง (พิมพ์ literal ลง log + job summary) | ไม่ใช่ tripwire — เป็น **skip census ชั้นประกาศ**: "a skipped check is not a passed check" |
| 9 | `THE GATE` | 326 | รวบทุกอย่างลง `$results` แล้วตัดสินครั้งเดียวที่ท้าย: `if (-not $allGreen) { ... exit 1 }` (549-551) พร้อม `::error::Windows gate RED` | ✅ ตัวรวม — ดูตาราง B |

> **การอ่าน step:** GitHub Actions หยุด job ทันทีที่ step ใดล้ม → **ถ้า step 7 แดง step 8-9 จะไม่รันเลย** (ดูข้อค้นพบ 2.1)

### 1.2 ตาราง B — 23 แถวของ `GATE SUMMARY` (ภายใน step 9)

| แถว | คำสั่ง / กลไก | expect | แดงเมื่อ | ชนิด tripwire |
|---|---|---|---|---|
| `pycompile_v141` | `py_compile current\pf_login_game_server_v141.py` | 0 | snapshot ที่แช่แข็งคอมไพล์ไม่ผ่าน | regression จริง |
| `compileall` | `compileall -q src tests tools` | 0 | syntax error ที่ไหนก็ได้ | regression จริง |
| `v141_selftest` | `... --self-test-only` | 0 | self-test ของ snapshot ล้ม | regression จริง |
| `ledger` | `verify_hypothesis_ledger.py` | 0 | `LedgerError` — inventory drift, `CANONICAL_CONTENT_SHA256` (บรรทัด 284) ไม่ตรง, annotation ใน `src/**/*.py` ไม่ถูกประกาศ | ✅ หมุด/pin (แฮชเนื้อ ledger JSON) |
| `replay3` | `pf_runtimeres_death_headless_replay.py` | 0 | guard ใด guard หนึ่งพัง | regression จริง |
| `replay2` | `... --profile dying_latch_only` | 0 | เหมือนบน | regression จริง |
| **`replayx`** | `... --profile nonsense` | **2** | **exit 0 = validator รับอะไรก็ได้** (บรรทัด 354-357 ของ tool) | ✅ **negative check** — เขียวคือ 2 |
| `dmenc` | `verify_damage_model_encoder.py` | 0 | guard พัง | regression จริง |
| `dmreplay` | `pf_damage_model_headless_replay.py` | 0 | guard พัง | regression จริง |
| `hpenc` | `verify_hp_death_encoder.py` | 0 | guard พัง **หรือ `UnicodeEncodeError` จาก print()** | regression จริง + ช่อง runtime ของ cp874 |
| `hlhold` | `pf_hp_death002_headless_replay.py --profile dying_hold` | 0 | guard พัง | regression จริง |
| `mpaudit` | `pf_multiplayer_readiness_audit.py` | 0 | ไม่มี git history → exit 1 | regression จริง + ต้องพึ่ง `fetch-depth: 0` |
| `seam` | `pytest tests\test_foundation_legacy_seam.py` | 0 | seam ขยับ · `GRADE_SUBSET_SHA256` ไม่ตรง · manifest debt โต | ✅ หมุดหลายชั้น |
| `pytest_subset` | `pytest tests -q -rs` + `--ignore` 43 โมดูล | 0 | เทสล้ม (run #3 แดงตรงนี้) | regression จริง |
| **`skip_census`** | `pf_pytest_precondition_census.py --report ... --excluded ...` | 0 | `PIN DRIFT` (บรรทัด 203/220) · `UNDECLARED SKIP` (214) · `UNPINNED` (198) · unknown key | ✅✅ **skip census — ยังไม่เคยเห็นแดงบน runner** |
| `coverage_debt` | สคริปต์ฝังใน YAML นับ `evidence_refs` ที่ไม่ tracked เทียบ `COVERAGE_EVIDENCE_DEBT_PIN='0'` (บรรทัด 59) | 0 | `COVERAGE EVIDENCE DEBT MOVED.` + `sys.exit(1)` (448) — แดงทั้งขึ้นและลง | ✅✅ หมุด/pin |
| `coverage` | `verify_functional_coverage.py` | 0 | exit 2 ที่ ref แรกที่หาไม่เจอ — **blocking แล้ว** เพราะ pin=0 (เงื่อนไขบรรทัด 460) | regression จริง |
| `git_lsfiles` | `git ls-files` | 0 | git พัง | plumbing |
| `forbidden_paths` | regex กัน prefix/นามสกุลต้องห้าม | 0 | มีไฟล์ `.bin/.zip/.sqlite3/...` หรือ `backups/ evidence/ ...` ถูก track | ✅ hygiene |
| `ignoreGuard` | `git check-ignore -q --no-index` กับ 4 probe | 0 | `.gitignore` เลิกกันไฟล์ไบนารี | ✅ hygiene |
| `diffcheck` | `git diff --check` | 0 | whitespace error | vacuous บน CI |
| `v141Guard` | `git status --short -- current/pf_login_game_server_v141.py` | 0 | ไฟล์แช่แข็งสกปรก | **vacuous บน CI** |
| `release_determinism` | build 2 ครั้งเทียบ sha256 | 0 | สอง build ของ tree เดียวกันไม่เท่ากัน | ✅ determinism |

**เก้า check ที่ถูก SKIP โดยประกาศชื่อ** (step 8): `latchver` `runtimeres` `damage` `hpstatic` `census` `stats` (ต้องการ `..\GameClient\GameClient.local.bin` 14,759,424 bytes) · `corpus` (ต้องการ `backups/**/capture_v131`) · `canonGuard` (ต้องการ canonical DB + `pf_bridge/CANON_SHA.txt`) — **ไม่ใช่ผ่าน**

---

## 2. ข้อค้นพบที่ต้องรู้ *ก่อน* เลือกวิธีปลูก

### 2.1 🔴 Actions หยุด job ที่ step แรกที่ล้ม → README recipe 2 ทำนายผิด

`README_GATE_CI.md` recipe 2 เขียนว่า "Expected: **two** red channels from one cause ... static tripwire fires, **และ** `hpenc` in THE GATE exits non-zero with `UnicodeEncodeError`"

**เป็นไปไม่ได้บน GitHub Actions ด้วย workflow ปัจจุบัน:** `cp874 static tripwire` คือ step 7 ส่วน `THE GATE` คือ step 9 — พอ step 7 `throw` job จบทันที step 8-9 ไม่ถูกรัน จึงเห็นได้แค่ **ช่องเดียว** เสมอ (ยกเว้นเติม `if: always()` ซึ่งไม่มี)

**ผลต่อการเลือก:** การปลูก cp874 ที่ไหนก็ตามใน `tools/ src/ current/` จะให้ช่องแดงช่องเดียวเสมอ = **อ่านง่าย** แต่ **ไม่พิสูจน์ `THE GATE`** (ซึ่ง run #3 และ run #4 พิสูจน์ไปแล้วว่ารันครบ)

### 2.2 แผนที่ "หมุดหลายชั้น" — ไฟล์ไหนแตะแล้วผลอ่านยาก

| ไฟล์ที่จะปลูก | ช่องที่จะแดงบน CI | อ่านง่าย? |
|---|---|---|
| `tools/pf_move_cadence001_headless_replay.py` | **1** — static tripwire เท่านั้น | ✅ ดีที่สุด |
| `src/pirateforce_foundation/__init__.py` | **1** — static tripwire (ตรวจแล้ว: `ANNOTATION_RE` ของ ledger ไม่จับคอมเมนต์ธรรมดา, `GRADE_SUBSET_SHA256` แฮชเฉพาะ ledger JSON ไม่ใช่ src, seam อ่านแค่ `app.py`/`runtime.py`) | ✅ ดี แต่แตะ source ที่เซิร์ฟเวอร์ import จริง |
| `docs/PYTEST_SKIP_PINS.json` (ขยับ count) | **1** — `skip_census` เท่านั้น (ตรวจแล้ว: ไม่มีเทสไหนเทียบ `len(tests)` กับ `count`, และ `fresh_clone_transcript()` สร้าง transcript จากหมุดเอง จึงสอดคล้องกับตัวเองเสมอ) | ✅ ดี |
| `tests/test_damage_hp_link_dispatch.py` (ลบ decorator) | **2** — `pytest_subset` + `skip_census` | ⚠️ ข้อความ pytest คือ `AssertionError: 2 != 0` ซึ่งเป็นกับดักที่รอบ 106 บันทึกไว้เองว่าอ่านผิดง่าย |
| `tools/pf_runtimeres_death_headless_replay.py` (`return 2`→`0`) | **2** — `replayx exit=0 expect=2` + `pytest_subset` (`test_the_replay_tool_refuses_a_profile_it_does_not_ship` ที่ `tests/test_runtimeres_death_dispatch.py:514` และโมดูลนี้ **ไม่** ถูก `--ignore`) | ⚠️ สองช่องแต่พูดเรื่องเดียวกัน |
| `docs/FUNCTIONAL_COVERAGE.json` (recipe 4) | **4-6** — `coverage_debt` + `coverage` + `seam` + `pytest_subset` (+ `test_presentation_ownership.py`, `test_single_session_limitation.py`, `test_hp_death_respawn_static.py` อ่านไฟล์นี้ด้วย) | ❌ **ตัดทิ้ง** — ตรงกับข้อห้าม "หมุดหลายชั้นจนอ่านผลยาก" |

### 2.3 ตะแกรง cp874 ชั้น pytest **ไม่ทำงานบน runner**

`tests/test_names_fold003_thunk_census.py` มีคลาส `Cp874ConsoleGateTests` (บทเรียนรอบ 86/92) ที่สแกน **ทั้ง tree `tools/` และ `tests/`** หาอักขระที่จะเข้า `print()` — แต่โมดูลนี้ **ติดตัวกรอง `GameClient|capture_v141`** จึงถูก `--ignore` ออกจาก `pytest_subset` บน CI

**ผลสองอย่าง:** (ก) บน CI การปลูก cp874 ใน `tools/` จะถูกจับโดย static tripwire **ช่องเดียว** (ข) บนบริดจ์จะถูกจับ **สองชั้น** (pytest + tripwire) → ปลอดภัยยิ่งขึ้นถ้าเผลอ merge

### 2.4 เกร็ดที่ต้องแก้ในเอกสาร (ไม่ได้แก้ในรอบนี้ — นอก scope)

- recipe ทั้ง 4 ใน `README_GATE_CI.md` เขียน `git checkout master` แต่ **branch จริงของ repo คือ `main`** (ไม่มี `master`) — คำสั่งในเอกสารนี้ใช้ `main`
- README บอก "84 files" ที่ static tripwire สแกน — วัดที่ HEAD ตอนนี้ได้ **97** (ตัวเลขนี้ *พิมพ์* ออกมาเฉย ๆ ไม่ได้ถูกปัก จึงไม่ทำให้แดง)
- README บอก exclusion list "42 modules" — grep ที่ HEAD ได้ 44 แมตช์ ลบ `test_foundation_legacy_seam.py` ที่ workflow ดึงกลับ = **43** (พิมพ์เต็มรายการทุกครั้ง ไม่ได้ปัก)
- run #3 บันทึกว่า "21 of 22 steps" แต่ตาราง `GATE SUMMARY` ที่ pin=0 มี **23 แถว** — ควรเทียบกับ log ของ run #4 ก่อนอ้างตัวเลข "22"

---

## 3. ตัวเลือกการปลูก 5 แบบ

### ตัวเลือก A — ปลูกอักขระนอก cp874 ในเครื่องมือที่หมุดเป็น 0 ⭐ **แนะนำ**

| หัวข้อ | รายละเอียด |
|---|---|
| **ปลูกอะไร** | ต่อท้าย `tools/pf_move_cadence001_headless_replay.py` (ปัจจุบัน 164 บรรทัด ลงท้ายด้วย newline) → เนื้อหาใหม่ไปอยู่ **บรรทัด 165** |
| **patch ที่แน่นอน** | บรรทัดใหม่: `# PLANTED RED R107 <U+1F534>` โดย `<U+1F534>` คืออักขระจริง — สร้างด้วยคำสั่งในหัวข้อ 5 (ห้ามพิมพ์มือ) |
| **step ไหนจับ** | **step 7 จาก 9** — `cp874 static tripwire (tools/, src/, current/)` |
| **ข้อความ error ที่คาด** | `RED tools/pf_move_cadence001_headless_replay.py           got=1 pinned=0` (จาก `gate-windows.yml:259`) ตามด้วย `        line 165: codepoint 0x1f534` (บรรทัด 263) แล้ว `CP874 TRIPWIRE RED. ...` (266-270) `sys.exit(1)` (271) และ PowerShell `cp874 static tripwire is RED` (277) — หมุด `0` มาจาก `ALLOWED` บรรทัด **229** |
| **แดงเร็วแค่ไหน** | ~**60-90 วินาที** (checkout ~6s + setup-python + pip ~11s + assert + self-check + tripwire) — step 7/9, `THE GATE` ไม่ถูกรัน |
| **ช่องแดง** | **1 ช่องเดียว** (ยืนยันแล้ว: tool นี้ไม่ถูกเรียกใน `THE GATE` เลย และเทสที่เฝ้ามัน — `test_names_fold003_thunk_census.py` — ถูก `--ignore` บน CI) |
| **ความเสี่ยงตกค้าง** | ถ้าลืมลบ branch: มี branch ค้างที่แดงถาวร ไม่กระทบ `main` · ถ้าเผลอ merge: อักขระอยู่ในคอมเมนต์ท้ายไฟล์ ไม่มีทางถึง `print()` → **ไม่พังตอนรัน** แต่ gate จะแดงถาวรจนกว่าจะลบ และบนบริดจ์ `pytest` จะแดงเพิ่มอีกช่อง (ตะแกรงรอบ 86) → **สังเกตเห็นทันที** · กู้คืน: `git revert` 1 บรรทัด หรือลบ branch |
| **พิสูจน์ tripwire ชนิดไหน** | **จับ regression จริง** — คลาสบั๊กรอบ 142 (U+1F534 → `UnicodeEncodeError` → เครื่องมือตายกลางรายงาน) และปิดทิศที่ยังไม่เคยเห็น: run #2 พิสูจน์ทิศ `got < pinned` (หมุดค้าง) ส่วนนี่คือทิศ `got > pinned` (**ต้นไม้สกปรก — ทิศที่ tripwire เกิดมาเพื่อจับ**) |

### ตัวเลือก B — ขยับหมุด skip จาก 2 เป็น 1 (SKIP-CENSUS-001)

| หัวข้อ | รายละเอียด |
|---|---|
| **ปลูกอะไร** | `docs/PYTEST_SKIP_PINS.json` **บรรทัด 31** |
| **patch ที่แน่นอน** | `      "count": 2,` → `      "count": 1,` (บล็อก `"key": "canonical_db"` บรรทัด 29, `"module": "tests/test_damage_hp_link_dispatch.py"` บรรทัด 30) |
| **step ไหนจับ** | **step 9 จาก 9** — `THE GATE` แถว `skip_census` |
| **ข้อความ error ที่คาด** | พิมพ์เต็มก่อนตัดสิน (`gate-windows.yml:408-409`) แล้ว: `CENSUS FAILURES (1):` / `  - PIN DRIFT: tests/test_damage_hp_link_dispatch.py / precondition 'canonical_db' (artifact absent): pinned 1, observed 2` (สร้างที่ `tools/pf_pytest_precondition_census.py:202-206`) / `RESULT: FAIL` (313) `return 1` (314) → แถวสรุป `skip_census exit=1 expect=0 RED` → `ALL GREEN (partial gate) = False` → `::error::Windows gate RED` (550) |
| **แดงเร็วแค่ไหน** | ~**5-6 นาที** — ต้องรอ `pytest_subset` (~217s ตาม run #3) จบก่อน แล้ว census จึงอ่าน transcript |
| **ช่องแดง** | **1 ช่องเดียว** — ยืนยันโดยอ่าน `tests/test_pytest_precondition_census.py` ครบ: `test_every_pinned_count_is_a_positive_integer` (1 ยังบวก ✓) · `test_the_pinned_test_names_exist_in_their_modules` (ไล่ชื่อในลิสต์ ไม่เทียบกับ count ✓) · `fresh_clone_transcript()` สร้างจากหมุดเอง → `test_a_fresh_clone_is_green_...`, `test_one_extra_skip_is_red`, `test_one_missing_skip_is_red_too` ยังเขียว ✓ → **`pytest_subset` ไม่แดง** |
| **ความเสี่ยงตกค้าง** | ถ้าเผลอ merge: census จะนับต่ำกว่าความจริง 1 → เทสจริงหลุดออกจากชุดที่ถูกเฝ้าได้เงียบ ๆ **1 ตัว** = ทำลายจุดประสงค์ของรอบ 106 พอดี ⚠️ · กู้คืน: แก้ตัวเลขเดียว |
| **พิสูจน์ tripwire ชนิดไหน** | **จับ pin drift** — คลาสเดียวกับ run #2 (หมุดกับความจริงไม่ตรงกัน) *ไม่ใช่* คลาส "เทสหลุดออกจากชุดที่ถูกเฝ้า" ซึ่งเป็นสิ่งที่ census เกิดมาเพื่อจับ (นั่นคือตัวเลือก B') · **ข้อดีเฉพาะตัว: `skip_census` เป็น check ที่ยังไม่เคยแดงบน runner เลย** และ job จะรันครบทุก step ให้เห็นตาราง `GATE SUMMARY` เต็มพร้อมแถวแดงแถวเดียว |

### ตัวเลือก B' — ลบ decorator ที่กันเทส (recipe 6 ของ README, รูปแบบที่ "จริง" กว่า)

| หัวข้อ | รายละเอียด |
|---|---|
| **ปลูกอะไร** | ลบ `tests/test_damage_hp_link_dispatch.py` **บรรทัด 941** |
| **patch ที่แน่นอน** | ลบบรรทัด `    @CANONICAL_DB_PRECONDITION.skip_unless_present()` ที่อยู่เหนือ `def test_the_replay_tools_output_is_pure_ascii(self):` (บรรทัด 942) — **อย่าลบบรรทัด 928** เพราะเป็นของอีกเทส |
| **step ไหนจับ** | **step 9** — แดง **2 แถว**: `pytest_subset` และ `skip_census` |
| **ข้อความ error ที่คาด** | `pytest_subset`: `AssertionError: 2 != 0` (assert แรกคือ `assertEqual(completed.returncode, 0)` ที่บรรทัด 944 ของเทส — tool คืน 2 เพราะไม่มี DB) · `skip_census`: `PIN DRIFT: tests/test_damage_hp_link_dispatch.py / precondition 'canonical_db' (artifact absent): pinned 2, observed 1` |
| **แดงเร็วแค่ไหน** | ~5-6 นาที (step 9) |
| **ความเสี่ยงตกค้าง** | ถ้าเผลอ merge: เทสจะล้ม (ไม่ใช่หลุดเงียบ) บนทุกเครื่องที่ไม่มี DB — เห็นชัด · กู้คืนง่าย |
| **พิสูจน์ tripwire ชนิดไหน** | **จับ regression จริง** ชนิดที่ README ระบุเองว่า "**THAT** is the failure mode the pin exists for" — แต่ ⚠️ ข้อความ `AssertionError: 2 != 0` คือกับดักการอ่านที่รอบ 106 บันทึกไว้เอง ("2 คือ return code ไม่ใช่จำนวนไบต์") ทำให้ผลอ่านยากกว่า B |

### ตัวเลือก C — ทำลาย negative check `replayx`

| หัวข้อ | รายละเอียด |
|---|---|
| **ปลูกอะไร** | `tools/pf_runtimeres_death_headless_replay.py` **บรรทัด 357** |
| **patch ที่แน่นอน** | `        return 2` → `        return 0` (อยู่ในบล็อก `if profile_name not in SCENARIO_BY_PROFILE:` บรรทัด 354) |
| **step ไหนจับ** | **step 9** — แดง **2 แถว**: `replayx` (โผล่เร็ว ~30 วิแรกของ `THE GATE`) และ `pytest_subset` (~250 วิ) |
| **ข้อความ error ที่คาด** | `  replayx exit=0` แล้วในตารางสรุป `replayx  exit=0  expect=2  RED` (จาก `Step 'replayx' {...} 2` บรรทัด 366 + ตัวเทียบบรรทัด 534-538) · `pytest_subset`: `test_the_replay_tool_refuses_a_profile_it_does_not_ship` → `AssertionError: 0 != 2` (`tests/test_runtimeres_death_dispatch.py:514`) |
| **แดงเร็วแค่ไหน** | ~2 นาที ถึงบรรทัด `replayx` ใน log แต่ job จบที่ ~6 นาที |
| **ความเสี่ยงตกค้าง** | ⚠️ **สูงสุดในลิสต์นี้** — ถ้าเผลอ merge validator จะรับ profile อะไรก็ได้แล้วเงียบ ๆ ตกไปใช้ค่า default (`spawn_then_kill`) = ทำ replay ผิด profile โดยไม่มีใครรู้ · กู้คืน: แก้อักขระเดียว แต่ **ความเสียหายถ้าไม่ถูกจับคือของจริง** |
| **พิสูจน์ tripwire ชนิดไหน** | **จับ regression จริง** + พิสูจน์กลไก **expect ที่ไม่ใช่ 0** (`replayx=2`) ซึ่งเป็นสิ่งที่ไม่มีที่ไหนพิสูจน์ — แต่ run #3 ได้เห็น `replayx exit=2 expect=2` เขียวไปแล้ว |

### ตัวเลือก D — coverage evidence debt (recipe 4 ของ README) ❌ **ตัดทิ้ง**

| หัวข้อ | รายละเอียด |
|---|---|
| **ปลูกอะไร** | เพิ่ม `"reports/NOT_A_REAL_REPORT.md"` เข้า `evidence_refs` ตัวใดตัวหนึ่งใน `docs/FUNCTIONAL_COVERAGE.json` |
| **step ไหนจับ** | step 9 — แต่แดง **4-6 แถวพร้อมกัน** |
| **ข้อความ error ที่คาด** | `NOT in a fresh clone : 1  (pinned at 0)` + `COVERAGE EVIDENCE DEBT MOVED.` (`gate-windows.yml:443-448`) · `coverage` exit 2 `does not exist: reports/NOT_A_REAL_REPORT.md` (blocking แล้วเพราะ pin=0) · `seam` แดงเพราะ `GRADE_SUBSET_SHA256` แฮชครอบ `evidence_refs` (`tests/test_foundation_legacy_seam.py:65-69`) · `pytest_subset` แดงซ้ำเพราะ workflow ดึง seam กลับเข้า pytest ด้วย (`Where-Object { $_ -ne 'tests/test_foundation_legacy_seam.py' }`) |
| **เหตุผลที่ตัด** | ผิดเกณฑ์ "ไม่แตะไฟล์ที่มีหมุดหลายชั้นจนอ่านผลยาก" ตรง ๆ — และถ้ามีอะไรพลาด จะแยกไม่ออกว่าแดงเพราะอะไร ทำให้ผลการทดลอง **inconclusive** ทั้งที่ทุกอย่างทำงานถูก |

### ตัวเลือก E — ช่อง runtime ของ cp874 (รอบ 142 แบบคำต่อคำ) — สองไฟล์

| หัวข้อ | รายละเอียด |
|---|---|
| **ปลูกอะไร** | (1) แทรก `print('<U+1F534>')` เป็นบรรทัดแรกของ `tools/verify_hp_death_encoder.py` **และ** (2) เพิ่ม `"tools/verify_hp_death_encoder.py": 1,` เข้า dict `ALLOWED` ใน `.github/workflows/gate-windows.yml` (หลังบรรทัด 231) |
| **ทำไมต้องแก้สองไฟล์** | ถ้าไม่ยกหมุด static tripwire (step 7) จะแดงก่อน job หยุด → **ไม่มีทางเห็นช่อง runtime เลย** (ดูข้อ 2.1) การยกหมุดคือช่องทางที่ workflow ออกแบบไว้เอง ("raise the pin in the same commit and say why") |
| **step ไหนจับ** | **step 9** — แถว `hpenc` |
| **ข้อความ error ที่คาด** | `  hpenc> UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f534' in position 0: character maps to <undefined>` (Step helper โชว์ 6 บรรทัดท้าย, `gate-windows.yml:335`) แล้ว `hpenc exit=1 expect=0 RED` — ยืนยันว่าไม่มีเทสไหนใน `tests/` อ้างถึง `verify_hp_death_encoder` เลย → ช่องเดียว |
| **แดงเร็วแค่ไหน** | ~2-3 นาที (step 9, `hpenc` เป็น check ที่ 10) |
| **ความเสี่ยงตกค้าง** | ⚠️ **สูง** — ถ้าเผลอ merge จะได้ทั้งเครื่องมือที่ตายบนคอนโซลบริดจ์ **และ** หมุดที่ถูกยกไว้ให้มันผ่าน = ปิดตา tripwire ถาวร กู้คืนต้องแก้ 2 ไฟล์ |
| **พิสูจน์ tripwire ชนิดไหน** | **จับ regression จริง ชั้น runtime** — เป็นตัวเลือกเดียวที่พิสูจน์ว่า `UnicodeEncodeError` ตอนรันจริงทำ gate แดง (ไม่ใช่แค่ static scan) แต่ต้องแตะ workflow เอง จึงกึ่ง ๆ "จับ pipeline ตัวเอง" |

### ตารางเทียบรวบ

| | A (cp874 static) | B (หมุด skip 2→1) | B' (ลบ decorator) | C (replayx) | E (runtime cp874) |
|---|---|---|---|---|---|
| จับได้แน่นอน | ✅ 100% deterministic | ✅ | ✅ | ✅ | ✅ (ถ้ายกหมุดถูก) |
| step ที่จับ | 7/9 | 9/9 | 9/9 | 9/9 | 9/9 |
| เวลาถึงแดง | **~90 วิ** | ~6 นาที | ~6 นาที | ~6 นาที | ~3 นาที |
| จำนวนช่องแดง | **1** | **1** | 2 | 2 | 1 |
| ไฟล์ที่แตะ | 1 | 1 | 1 | 1 | **2 (รวม workflow)** |
| ชนิดที่พิสูจน์ | regression จริง (cp874) | pin drift | regression จริง (skip drift) | regression จริง (negative check) | regression จริง (runtime cp874) |
| check นี้เคยแดงบน runner? | เคย (run #2 คนละทิศ) | **ไม่เคย** | ไม่เคย | ไม่เคย | ไม่เคย |
| อันตรายถ้าเผลอ merge | ต่ำ | กลาง | ต่ำ | **สูง** | **สูง** |
| กู้คืน | ลบ branch | ลบ branch | ลบ branch | ลบ branch | ลบ branch (2 ไฟล์) |

---

## 4. ตัวแนะนำ: **ตัวเลือก A**

**เหตุผลตามเกณฑ์ทั้งสี่ของ Panya:**

1. **จับได้แน่นอน** — เป็น static scan ล้วน ไม่ขึ้นกับ pytest, เวลา, เครือข่าย, หรือสภาพ runner และ README บันทึกไว้เองว่า *"the rehearsal ... produced exactly that output"* เมื่อซ้อมออฟไลน์กับชุดไฟล์จริง (รูปแบบ `src/` แต่กลไกเดียวกัน)
2. **เป็นความบกพร่องชนิดที่โปรเจกต์กลัวจริง** — U+1F534 ในเครื่องมือคือเหตุการณ์รอบ 142 ตัวจริง ที่ทำให้ workflow ทั้งไฟล์นี้เกิดขึ้น comment หัวไฟล์ `gate-windows.yml:1-16` พูดถึงมันโดยตรง และ `pf_move_cadence001_headless_replay.py` คือ **ไฟล์ที่เคยมีกับดักนั้นจริง ๆ** (U+00D7 / U+00B1 ก่อนรอบ 92-93) การเอากลับไปใส่คือการถามว่า "ถ้ามันกลับมา gate จับไหม"
3. **แก้คืนด้วยการลบ branch อย่างเดียว** — ✅ เป็นการ *ต่อท้าย* หนึ่งบรรทัด ไม่แก้บรรทัดเดิม ไม่ย้ายเลขบรรทัดใคร
4. **ไม่แตะไฟล์ที่มีหมุดหลายชั้น** — ✅ ตรวจครบแล้ว: เครื่องมือนี้ **ไม่ถูกเรียกใน `THE GATE`** · **ไม่อยู่ใน `src/`** (จึงไม่โดน ledger annotation scan และ release builder) · เทสเดียวที่เฝ้ามัน (`test_names_fold003_thunk_census.py`) ถูก `--ignore` บน CI → **ช่องแดงช่องเดียว หมุดชั้นเดียว**

**เหตุผลเพิ่ม (ที่สำคัญที่สุด):** run #2 ทำให้ step นี้แดงในทิศ `got=0 pinned=6` = **หมุดค้างยุค** ตัวเลือก A ทำให้แดงในทิศ `got=1 pinned=0` = **ต้นไม้สกปรก** — ทิศเดียวกับที่บทเรียนรอบ 86/142 กลัว และเป็นทิศที่ **ยังไม่เคยเกิดบน runner** ผลลัพธ์คือคู่ A/B ที่สะอาด: step เดียวกัน ไฟล์เดียวกัน สองทิศ ครบ

**และเวลา 90 วินาทีคือคุณสมบัติ ไม่ใช่ข้อด้อย** — รอบทดลองสั้นที่สุด = โอกาสลืมลบ branch น้อยที่สุด ซึ่งเป็นความเสี่ยงเดียวที่เอกสารนี้ควบคุมไม่ได้

### 🔴 เทียบตรง ๆ: cp874 (A) กับ ขยับหมุด skip (B) ตามที่ Panya เอ่ยชื่อมา

| ประเด็น | A — cp874 (บทเรียนรอบ 86/142) | B — SKIP-CENSUS-001 (บทเรียนรอบ 106) |
|---|---|---|
| **ข้อดี** | เป็นเหตุผลการมีอยู่ของทั้ง workflow · แดงใน 90 วิ · ไม่แตะ logic ใด ๆ (คอมเมนต์ล้วน) · ปลอดภัยสุดถ้าเผลอ merge · บนบริดจ์จะถูกจับซ้ำอีกชั้น | จุด `skip_census` ซึ่ง **ยังไม่เคยเห็นแดงบน runner เลย** · job รันครบทุก step ให้เห็น `GATE SUMMARY` เต็มตารางกับแถวแดงแถวเดียว = ภาพหลักฐานที่สวยที่สุด · แก้ไฟล์ข้อมูล ไม่ใช่โค้ด |
| **ข้อเสีย** | step 7 แดงแล้ว job หยุด → **ไม่ได้รัน `THE GATE`** (แต่ run #3/#4 พิสูจน์ไปแล้ว) · `cp874 static tripwire` เคยเห็นแดงมาแล้วครั้งหนึ่ง (run #2) แม้จะคนละทิศ | รอ ~6 นาที · **พิสูจน์ผิดชนิด**: ขยับ *หมุด* จำลอง "หมุดค้างยุค" (run #2) ไม่ใช่ "เทสหลุดออกจากชุดที่ถูกเฝ้า" ที่ census เกิดมาเพื่อจับ — ถ้าอยากพิสูจน์ชนิดหลังต้องใช้ B' ซึ่งแดง 2 ช่องและมีข้อความหลอกตา `2 != 0` · ถ้าเผลอ merge จะปิดตา census ไป 1 ตัวเงียบ ๆ |
| **คำตัดสิน** | ⭐ **เลือกอันนี้เป็นนัดแรก** | เก็บเป็น **นัดที่สอง** (ดูหัวข้อ 5.B) — คุ้มมาก เพราะเป็น check เดียวในตารางที่ยังไม่เคยแดง |

---

## 5. ขั้นตอนที่ Panya ทำเองได้ (ก๊อปวาง PowerShell)

> ทุกบล็อกด้านล่างเป็น ASCII ล้วน · รันจากหน้าต่าง PowerShell ปกติ · **ห้ามรันขณะ `main` สกปรก**

### 5.0 พรีเช็ก + จดสถานะ `main` ไว้เทียบทีหลัง

```powershell
$repo = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
Set-Location -LiteralPath $repo

# 1. must be on main, and clean
git --no-optional-locks rev-parse --abbrev-ref HEAD
git --no-optional-locks status --porcelain

# 2. BASELINE - copy this output somewhere before you touch anything
$mainBefore = (git --no-optional-locks rev-parse main)
$originBefore = (git --no-optional-locks rev-parse origin/main)
Write-Host "main       BEFORE = $mainBefore"
Write-Host "origin/main BEFORE = $originBefore"
git --no-optional-locks log main --oneline -1
```

หยุดทันทีถ้า `git status --porcelain` ไม่ว่าง หรือ branch ปัจจุบันไม่ใช่ `main`

### 5.1 สร้าง branch แล้วปลูก (ตัวเลือก A)

```powershell
git switch -c gate-redtest

# plant one U+1F534 as the LAST line.  newline='' keeps it LF, matching
# .gitattributes '*.py text eol=lf'.  The character is produced by an escape
# so nothing outside cp874 is ever typed into this console.
py -3 -c "open('tools/pf_move_cadence001_headless_replay.py','a',encoding='utf-8',newline='').write('# PLANTED RED R107 \U0001F534\n')"

# local dry run of the EXACT scan the workflow does - expect: got=1 pinned=0
py -3 -c "
import pathlib
p = pathlib.Path('tools/pf_move_cadence001_headless_replay.py')
hits = []
for n, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
    for ch in line:
        try:
            ch.encode('cp874')
        except UnicodeEncodeError:
            hits.append((n, hex(ord(ch))))
print('got=%d pinned=0  hits=%s' % (len(hits), hits))
"

# expect exactly:  got=1 pinned=0  hits=[(165, '0x1f534')]
git --no-optional-locks status --short
git --no-optional-locks diff --stat
```

### 5.2 commit และ push (แตะเฉพาะ branch)

```powershell
git add tools/pf_move_cadence001_headless_replay.py
git commit -m "PLANTED RED R107: one U+1F534 in the cadence tool, to prove the cp874 static tripwire fires on a dirty tree. THROWAWAY BRANCH - delete after the run. Do not merge."

# confirm main did NOT move
git --no-optional-locks rev-parse main
Write-Host "main BEFORE was $mainBefore"

git push -u origin gate-redtest
```

### 5.3 ดูผล

```powershell
# with the GitHub CLI
gh run list --branch gate-redtest --limit 3
gh run watch

# without gh, open this URL in a browser
Write-Host 'https://github.com/panyaasanee/pirate-force-server/actions?query=branch%3Agate-redtest'
```

สิ่งที่ต้องเห็นใน log ของ step **`cp874 static tripwire (tools/, src/, current/)`**

```text
scanned 97 tracked .py files under tools/, src/, current/
  RED tools/pf_move_cadence001_headless_replay.py            got=1 pinned=0
        line 165: codepoint 0x1f534
  ok  tools/pf_vital_name_thunk_static.py                    got=1 pinned=1
  ok  tools/pf_vital_thunk_census_static.py                  got=3 pinned=3

CP874 TRIPWIRE RED.  A character with no code page 874 mapping does not
degrade into '?' on the bridge console - it raises UnicodeEncodeError
inside print() and kills the tool mid-report.  Remove the character or,
if it is provably unreachable from any print(), raise the pin in
.github/workflows/gate-windows.yml in the same commit and say why.
```

และบรรทัดสุดท้ายของ step: `cp874 static tripwire is RED`
และ step 1-6 ต้อง **เขียวทั้งหมด** · step 8-9 ต้องเป็น **skipped** (ไม่ใช่ failed)

### 5.4 ลบ branch ทั้ง local และ remote + ยืนยัน `main` ไม่ถูกแตะ

```powershell
git switch main
git --no-optional-locks status --porcelain      # must be empty

git branch -D gate-redtest
git push origin --delete gate-redtest

# AFTER - must equal the BEFORE values from step 5.0
$mainAfter = (git --no-optional-locks rev-parse main)
$originAfter = (git --no-optional-locks rev-parse origin/main)
Write-Host "main       BEFORE=$mainBefore AFTER=$mainAfter  SAME=$($mainBefore -eq $mainAfter)"
Write-Host "origin/main BEFORE=$originBefore AFTER=$originAfter  SAME=$($originBefore -eq $originAfter)"
git --no-optional-locks log main --oneline -1

# no stray branch, local or remote
git --no-optional-locks branch -a
git --no-optional-locks fetch --prune origin
git --no-optional-locks ls-remote --heads origin
```

ต้องเห็น `SAME=True` ทั้งสองบรรทัด และ `gate-redtest` หายจากทั้ง `branch -a` และ `ls-remote --heads origin`

### 5.B (ทางเลือก) นัดที่สอง — จุด `skip_census` ในการทดลองเดียวกัน

ถ้าอยากได้ทั้งสองช่องในเซสชันเดียว ให้ push **คอมมิตที่สอง** บน branch เดิม โดยคอมมิตที่สองต้อง **ถอน** การปลูกแรกออกก่อน (ไม่งั้น step 7 แดงซ้ำแล้ว job หยุดก่อนถึง `THE GATE`)

```powershell
# run this AFTER 5.3 and BEFORE 5.4
git revert --no-edit HEAD          # undo the cp874 plant

# plant #2: move the canonical_db skip pin from 2 to 1
$pins = 'docs/PYTEST_SKIP_PINS.json'
$text = Get-Content -LiteralPath $pins -Raw
$text = $text -replace '(?m)^(\s*)"count": 2,$', '$1"count": 1,'
Set-Content -LiteralPath $pins -Value $text -NoNewline -Encoding utf8

git --no-optional-locks diff -- $pins      # must show exactly one line changed, 2 -> 1
git add $pins
git commit -m "PLANTED RED R107 second shot: move the canonical_db skip pin from 2 to 1 so skip_census must refuse it. THROWAWAY BRANCH - delete after the run. Do not merge."
git push
```

สิ่งที่ต้องเห็นใน step **`THE GATE`**

```text
--- skip census (every skip named, with its reason) ---
  PYTEST SKIP CENSUS - 4 skip(s) on this machine
  ...
  CENSUS FAILURES (1):
    - PIN DRIFT: tests/test_damage_hp_link_dispatch.py / precondition 'canonical_db' (artifact absent): pinned 1, observed 2

  RESULT: FAIL
  skip_census exit=1
```

และในตารางท้าย: `| skip_census | 1 | 0 | RED |` โดย **ทุกแถวอื่นเป็น GREEN** รวมทั้ง `pytest_subset` แล้วปิดท้ายด้วย `ALL GREEN (partial gate) = False` และ `::error::Windows gate RED`

จากนั้นกลับไปทำ **5.4** ตามเดิม

---

## 6. เกณฑ์ว่าการทดลองนี้สำเร็จ

### ✅ สำเร็จ (gate ถูกพิสูจน์แล้ว) — ต้องเห็น **ครบทุกข้อ**

1. Actions run บน branch `gate-redtest` **แดง**
2. แดงที่ step **`cp874 static tripwire (tools/, src/, current/)`** — **ไม่ใช่ step อื่น**
3. log มีบรรทัด `RED tools/pf_move_cadence001_headless_replay.py` พร้อม `got=1 pinned=0` และ `line 165: codepoint 0x1f534` — คือ gate **ชี้ไฟล์ บรรทัด และ codepoint ที่เราปลูกได้ถูกต้อง**
4. step 1-6 **เขียวทั้งหมด** โดยเฉพาะ `SELF-CHECK` ต้องเขียว (แปลว่าตะแกรงติดอาวุธจริงตอนที่จับได้ ไม่ใช่บังเอิญ)
5. step 8-9 แสดงเป็น **skipped** (ยืนยันพฤติกรรม fail-fast ตามข้อ 2.1)
6. `main` ที่ `rev-parse` ก่อน/หลัง **เท่ากันเป๊ะ** และ `origin/main` เท่าเดิม
7. `gate-redtest` หายทั้ง local และ remote หลังจบ
8. (ถ้าทำ 5.B) run ที่สองแดงที่แถว `skip_census` เท่านั้น โดย `pytest_subset` เขียว

### ❌ ล้มเหลว — เห็นแล้วต้องหยุดและสอบสวน

| อาการ | แปลว่า |
|---|---|
| **เขียวหมด** ทั้งที่ปลูกแล้ว | 🔴 **ร้ายแรงที่สุด** — tripwire ไม่ทำงาน ให้ตรวจว่า push ขึ้นไปจริงไหม (`git ls-remote --heads origin`) และไฟล์ที่ปลูกถูก commit จริงไหม (`git show --stat HEAD`) ถ้าปลูกจริงแล้วยังเขียว = gate โกหก ต้องเปิด FINDINGS |
| แดงที่ `SELF-CHECK` | ตะแกรง cp874 **ถูกปลดอาวุธ** (`U+1F534 printed cleanly`) หรือ exit code ไม่ propagate — ผลการทดลอง **ไม่นับ** เพราะ tripwire ไม่ติดอาวุธ |
| แดงที่ `Assert the environment...` | runner เปลี่ยนพฤติกรรม (chcp/encoding/interpreter) — **inconclusive** ต้องซ่อม plumbing ก่อนแล้วทดลองใหม่ |
| แดงที่ `Install the packages...` | pip/เครือข่ายล้ม — **false red** ไม่นับ ให้ re-run |
| แดงที่ step ที่ถูกต้อง แต่ log ชี้ **ไฟล์อื่น / บรรทัดอื่น / codepoint อื่น** | tripwire จับของ **แต่จับผิดตัว** — ต้องหาว่ามีอะไรอื่นสกปรกอยู่ ผลการทดลองยังไม่ปิด |
| แดงหลายแถวใน `GATE SUMMARY` (กรณี 5.B) | แปลว่าประเมิน blast radius ผิด — บันทึกไว้เป็น finding แล้วอ่านผลด้วยความระวัง |
| `main` ขยับ (rev-parse ไม่เท่าเดิม) | 🔴 **ละเมิดข้อบังคับ** — หยุดทุกอย่าง แจ้ง chief ก่อนทำอะไรต่อ |
| `gate-redtest` ยังอยู่บน remote หลังจบ | การทดลองยังไม่ปิด — gate จะแดงค้างในหน้า Actions ทำให้ครั้งหน้าอ่านผลผิด |

### ⚠️ inconclusive — ต้องทำซ้ำ

- แดงที่ step ถูกต้อง แต่ **run นั้นถูก cancel / timeout** ก่อนจบ
- แดงเพราะ runner image เปลี่ยนกลางคัน (เทียบ `py -3 -> 3.14.x` ใน log กับ run #4)
- ปลูกแล้วแต่ commit ว่าง (`git show --stat` ไม่มีไฟล์) — push ไม่มีผล

---

## 7. สิ่งที่ **ไม่ได้** ทำ / ข้อจำกัดของเอกสารนี้

- ไม่ได้ commit, push, checkout, branch, pull อะไรทั้งสิ้น — อ่านด้วย `git --no-optional-locks` อย่างเดียว
- **ไม่ได้แก้ไฟล์ใด ๆ ใน repo `Pirate Force ServerProject`** ไฟล์เดียวที่เขียนคือเอกสารนี้ใน `pf_bridge/`
- ไม่ได้แตะ canonical DB, ไม่ได้เปิด UI, ไม่ได้แตะ `LOCK_*.txt` / `GAME_TEST_QUEUE.md` / `CHIEF_CONTINUATION.md`
- ไม่ได้รัน pytest ชุดเต็ม — การทำนายผลทั้งหมดมาจาก **การอ่านโค้ดและอ้างเลขบรรทัด** บวกกับ log ที่ `README_GATE_CI.md` บันทึกไว้จาก run #1-#3
- เวลาที่ประมาณ (90 วินาที / 6 นาที) มาจากตัวเลขที่ README บันทึก (checkout 6s, pip 11s, `THE GATE` 3m50s, `pytest_subset` 217s) ไม่ได้วัดใหม่
- ข้อ 2.1 (fail-fast) เป็นการอนุมานจากพฤติกรรมมาตรฐานของ GitHub Actions บวกกับการที่ workflow ไม่มี `if: always()` ที่ไหนเลย — **run แรกของการทดลองนี้จะพิสูจน์หรือหักล้างมันเอง** ซึ่งเป็นของแถมที่มีค่า
