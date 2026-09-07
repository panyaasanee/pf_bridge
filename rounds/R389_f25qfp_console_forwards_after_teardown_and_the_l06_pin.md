# R389 (`f25qfp`) — มิเรอร์ที่ถอดแล้ว "ส่งต่อ" ไม่ใช่ "ทิ้ง" · และพิน L06 ที่ทำให้ `#1039` แดง

เริ่ม 2026-09-07T15:22+07:00 · เขียน 2026-09-07T15:44+07:00 · claim PR `pf_bridge#1735` · กิ่งเซิร์ฟเวอร์ `claude/eloquent-edison-f25qfp` HEAD `25669428`

## 0) รอบนี้ขยับ NOW/M ข้อไหน
**ขยับ**: `NOW.md` บรรทัด chief ข้อ (1) `_Mirror` encoding=คอนโซล (`1346`) + teardown forward + เตือนครั้งเดียว (`1441`) — จ่ายครบทั้งสองใบในคอมมิตเดียว
**ขยับ**: `NOW.md` "ฝั่ง pf_bridge: ยก §7 (`1441`)" — บล็อกขึ้น `AGENTS.md` §7 คำต่อคำแล้ว
**ขยับ**: `NOW.md` "GM-064: พิน L06 คอมมิตเดียวกัน" — พินขยับพร้อมโค้ดในคอมมิตเดียวกันตามสั่ง
**ไม่ขยับ**: ไมล์สโตน M2/M3/M4 — งานรอบนี้เป็นเส้นทางคอนโซลของผู้ควบคุม ไม่ใช่สิ่งที่ผู้เล่นเห็นบนจอ
**ไม่ได้ทำ**: CORE-REQUEST สามใบ PR เดียว (ลำดับ (2) ของใบ `1141`) — เลื่อนเป็นรอบที่สามแล้ว เหตุผลใน §7 ของไฟล์นี้

## 1) ชะตา PR รอบก่อน — `#1039` แดงและถูกปิด งานไม่หาย
`SYNC-NOTICE 20260907_1452` แจ้งว่า `pirate-force-server#1039` (LANE-E รอบ `axmac6`/R388) ถูก `merge-claude-pr.yml` ปิดเพราะ job `gate` = failure
กิ่ง `claude/adoring-turing-axmac6` ยังอยู่ครบ ⇒ รอบนี้ **cherry-pick `a9043b4` + `147d1e5`** ขึ้นกิ่งของรอบนี้ ไม่ทำใหม่จากศูนย์ ตามที่ตัวใบสั่ง

### สาเหตุแดง: จุดเดียวคุมสองแถวในตารางเกต [วัดแล้ว]
ตารางเกตของ run `34095113499`: `mpaudit exit=1` และ `pytest_subset exit=1` (ที่เหลือ GREEN ทุกแถว)
รากเดียวกัน: พิน `L06` ใน `tools/pf_multiplayer_readiness_audit.py` จับสตริง `sys\.stdout = build_console_mirror\(`
แต่ R388 ย้ายการเรียกโรงงานไปเป็น `self._installed_out = build_console_mirror(...)` แล้วค่อย `sys.stdout = self._installed_out`
⇒ พินจับได้ **0 ครั้ง** ⇒ `RESULT: 1 guard(s) drifted: assumption L06 ... found 0 at []`
และ `pytest_subset` แดงตามที่ `tests/test_multiplayer_readiness_audit.py::VerifierRunsCleanTests::test_the_verifier_exits_zero_as_a_subprocess`
ซึ่งรันตัวตรวจเป็น subprocess แล้วยืนยัน exit 0

🔴 **ทำไม R388 มองไม่เห็น**: เทสตัวนั้นมี precondition `audit_head_history` — **skip บนโคลนคลาวด์ที่ตื้น** และรันจริงเฉพาะบนเกต/สะพาน
รอบนี้ `git fetch --unshallow` ก่อน จึงรันของจริงได้บนคลาวด์เป็นครั้งแรก

คำสั่งที่รันซ้ำได้ (ทั้งสองทาง · [วัดแล้ว] บนโคลนรอบนี้ · CPython 3.14 ผ่าน `uv`):
```
git fetch --unshallow origin
# พินเก่า:
uv run --python 3.14 --with pytest --with pytest-subtests python -m pytest \
  tests/test_multiplayer_readiness_audit.py -q -k verifier_exits_zero
#   => 1 failed  (AssertionError: verifier drifted: ... assumption L06 ... found 0 at [])
# พินใหม่ (บนกิ่งนี้):
uv run --python 3.14 --with pytest --with pytest-subtests python -m pytest \
  tests/test_multiplayer_readiness_audit.py -q
#   => 29 passed, 1 skipped, 25 subtests passed
```

🔴 **แก้คำที่ R388 เขียนเองในรายงาน**: R388 เขียนว่า "the L06 pin matches on the factory call, which did not move" — **ผิด** และเป็นสาเหตุแดงตรง ๆ
ประโยคนั้นไม่เคยถูกวัดบนกิ่ง (รันตัวตรวจก่อนเปลี่ยนชื่อ ไม่ได้รันหลัง) ⇒ รอบนี้เขียนคำแก้ลงในรายงานเอง ไม่กลบ

พินใหม่ตามหลังสิ่งที่ L06 ยืนยันจริง = **การสลับ stdout ทั้ง process** (`sys\.stdout = self\._installed_out`)
ส่วนข้ออ้างว่า "มิเรอร์สร้างผ่านโรงงาน" ปักไว้ที่เทสของมันเอง (`test_runtime_console_installs_what_the_factory_returns`) ซึ่งเป็นที่ที่ควรอยู่

## 2) จ่ายใบ `1346` — มิเรอร์รายงาน encoding ของคอนโซล ไม่ประกาศของตัวเอง
- `_Mirror.encoding`/`errors` อ่านผ่าน `_reported_text_attr(self._console, ...)` (getattr ห่อ try/except กว้าง)
- ค่าตั้งต้น: `encoding` → `"utf-8"` · **`errors` → `"replace"` ไม่ใช่ `"strict"`** (ข้อที่ใบย้ำว่าอย่าพลาด)
- **พลิกพินในคอมมิตเดียวกัน ไม่มี skip/xfail/allowlist**: `test_factory_writes_both_ends_and_declares_the_module_encoding`
  → `..._reports_the_console_encoding` · บรรทัด `errors == "strict"` → `"replace"`
- **docstring ของ `build_console_mirror` ที่ `#1022` ยกค่าคงที่ขึ้นเป็นสัญญา เขียนใหม่แล้ว** ตามข้อ 4 ของใบ
- เทสคู่ที่ใบสั่ง: มิเรอร์ห่อสตรีมที่ประกาศ `cp874` ⇒ `mirror.encoding == "cp874"` · property ที่ยกข้อยกเว้น ⇒ ตกมาที่ `"utf-8"`

## 3) จ่ายใบ `1441` — forward + เตือนหนึ่งครั้งต่อมิเรอร์
- `write()`/`flush()` ของมิเรอร์ที่ถอดแล้วส่งต่อไป `_live_stream(self._fallback)` (ข้อ 2 ของใบ)
- คำเตือน: **ธง bool ต่ออินสแตนซ์** เขียนตรงลง fallback ใน `try/except Exception` · **ไม่ใช้ `warnings.warn` ไม่ใช้ `logging`** ตามที่ห้าม
- ข้อ 4 (หลักฐานแตกสองที่) เขียนเป็น docstring ของ `_Mirror`: บรรทัดหลังปิดอยู่บนจอ **ไม่อยู่ในไฟล์ retained ของรอบนั้น**
- ข้อ 5 เทสสามตัวในคอมมิตเดียวกัน ครบ: exit 0 หลัง `close()` (subprocess จริงสองคอนโซลซ้อน) · บรรทัดหลังปิดไปถึง fallback · คำเตือนออกครั้งเดียวแม้เขียนสิบบรรทัด

### สองอย่างที่ผมเพิ่มเองเพราะรูปที่ใบสั่งเปิดช่องไว้ (ไม่ได้อยู่ในใบ)
1. **รั้วกันวนซ้ำต่อเธรด** (`_active_forwards()` = `threading.local` เก็บ id ของมิเรอร์ที่กำลัง forward)
   เพราะ fallback ของสองมิเรอร์ชี้หากันได้: `a→b→a→b…` · `_live_stream` มี `seen` แต่คุมได้แค่ **การเดินของตัวเอง** ไม่คุมการเรียกซ้อนข้ามอ็อบเจกต์
   [วัดแล้ว] ถอดรั้วออก = 1,915 hop · ใส่รั้ว = 5 hop
2. **สแนปช็อตใต้ล็อกแล้วทำ I/O นอกล็อก** — forward เขียนเข้าไปในล็อกของมิเรอร์อีกตัว การถือล็อกตัวเองข้ามไปคือ lock-order inversion ระหว่างสาย stdout กับ stderr

### `[สมมติของสาย LANE-E - รอ COO ยืนยัน]`
ข้อ 3 บรรทัดสุดท้าย "`write`/`flush` ห้ามยกข้อยกเว้นออกไปหาผู้เรียกไม่ว่ากรณีใด" ผมตีความว่า **ครอบคลุมเส้นทางหลังถอด**
เส้นทางปกติยังปล่อยข้อยกเว้นของ sink ทะลุตามเดิม (การกลืนเงียบบนเส้นทางปกติคือความเสียหายรูปเดียวกับ (ก) drop ที่ใบนี้เพิ่งปฏิเสธ)
ส่งถาม COO แล้ว: `notes_to_chief/20260907_1600_FROM-CHIEF-TO-COO-write-never-raises-scope.md` — **เขียนคำถามแล้วเดินต่อ ไม่ได้รอ**

## 4) ฝั่ง pf_bridge — ยกบล็อก §7 ลง `AGENTS.md`
ใบ `20260907_1441_COO-TO-CHIEF-section7-block` สั่งยกทั้งบล็อกคำต่อคำ + สองข้อเพิ่ม (`NEGATIVE-MEASURED` ของ `1349` พร้อมที่มา `GT-178` · เกต 3.14 / คลาวด์ 3.11)
ไม่ตัดข้อ ไม่เรียบเรียงใหม่ · เปลี่ยนเฉพาะป้าย "ยังไม่ลง §7" (ซึ่งเป็นเท็จทันทีที่มันลง §7) เป็นที่มาของบล็อก · **ไม่แตะ `NOW.md`** ตามที่ใบสั่ง

🔴 **ข้อจำกัดที่เจอ และวิธีที่ผมแก้โดยไม่ทิ้งกฎข้อไหน**
`AGENTS.md` = 44,206 B อยู่ **เหนือเพดานเกต 30,720 B อยู่แล้ว** และ `check_bridge_file_sizes` แดงเมื่อไฟล์ **"เกินเพดาน และ โตขึ้นเทียบ origin/main"**
⇒ เติมบล็อกเฉย ๆ = preflight แดง = push ไม่ได้ · หั่น §7 ให้เหลือ 30 KB ในรอบเดียว = เสี่ยงทำกฎหล่นหาย ซึ่งแพงกว่าหนี้ขนาดไฟล์
ทางที่เลือก: **ย้าย §10 (Codex spot-check) ออกไป `CODEX_SPOT_CHECK.md` คำต่อคำ** แล้วเหลือบรรทัดชี้ทางใน `AGENTS.md`
— ท่าเดียวกับ §3/§4/§5 ที่ชี้ไป `BRIDGE_BOOT_PROCEDURE.md`/`EVIDENCE_GATES.md` · **กฎยังมีผลเต็ม ไม่ใช่การส่งไป archive**
ผล: 44,206 → 44,142 B ⇒ **ไม่โตขึ้น** ⇒ `[bridgesize] PASS` · หนี้ 13 KB ที่เหลือยังอยู่ ไม่ได้แสร้งว่าจ่ายแล้ว

## 5) CORE-REQUEST (§17.3) — ต่อสายค้าง เขียนตามจริง
`WIRED = 15 / 10` — วัดซ้ำรอบนี้ด้วยคำสั่งเดียวกับ R388 ไม่เปลี่ยน (`lane_hooks` auto-discover 19 หัก `registered_but_not_fired` 4 · `grep -rliE '"production_allowed"[[:space:]]*:[[:space:]]*true' scenarios/*.json` ⇒ 10 ไฟล์)
🔴 **สามใบแดงใน PR เดียว (GM-062 · GM-063 · DB op5) เลื่อนเป็นรอบที่สาม** — เหตุผลตามจริง ไม่ใช่ข้ออ้าง:
ใบ `1141` วาง (1) ก่อน (2) และ NOW เขียนว่า chief ทำ **หนึ่งงานต่อรอบ** · รอบนี้ (1) ไม่ใช่งานเดี่ยว มันมาพร้อมการกู้ `#1039` และการหาสาเหตุแดง
ยัดสามใบ CORE-REQUEST เข้าไปอีกจะละเมิด v6.3 (หนึ่งเรื่องต่อใบ ≤~6 ไฟล์) ⇒ **รอบหน้าเป็นงานแรก ห้ามเลื่อนอีก**

## 6) ชุดเทสและเกต — เขียนตามจริง ห้ามอ่านว่าเขียว
- `pytest tests/test_runtime_console.py` ⇒ **17 passed, 2 subtests** (เดิม 11) — เขียว(cloud sanity) บน 3.11 และ 3.14
- **มิวแทนต์เก้าตัว ตายทั้งเก้า** (แต่ตัวที่สามรอดในการวัดครั้งแรก และผมแก้เทส ไม่ใช่แก้ตัวเลข):
  M1 เตือนทุกบรรทัด · M2 ถอดแล้วทิ้งแทนส่งต่อ · M3 ถอดรั้วกันวนซ้ำ · M4 encoding กลับเป็นค่าคงที่ · M5 errors กลับเป็น strict · M6 forward ปล่อยข้อยกเว้นทะลุ · M7 property ปล่อยข้อยกเว้นทะลุ · M8 `flush()` เลิก forward · M9 หลังถอดยังตอบแทนคอนโซลที่ตายแล้ว
  🔴 **M3 รอดรอบแรก**: เทส cycle เดิมยืนยันแค่ "`write()` คืนค่าปกติ" ซึ่ง **ไม่พอ** เพราะ `RecursionError` เป็นลูกของ `Exception` แล้วโดน `except Exception` ของตัวเองกลืน
  ⇒ เปลี่ยนเทสไปนับ hop ของ `_live_stream` แทน (มีรั้ว 5 · ไม่มีรั้ว 1,915) แล้ว M3 จึงตาย
- `pf_gate_preflight.py --repo <server>` ⇒ **PREFLIGHT PASS** (cp874 · skips · mainmerge · census · bridgesize · queuegrowth · filenamelen · scoreboard · claudecfg · consumedstub)
  🔴 `cp874` จับผมเองระหว่างทาง: อักขระ 🔴 สองตัวที่ผมพิมพ์ลง docstring ของ `runtime_console.py` — ถอดเป็น ASCII แล้ว
- `git merge origin/main` เข้ากิ่งก่อนรันชุดสุดท้าย ⇒ `[mainmerge] PASS`
- **ชุดกว้างบน CPython 3.14 (ซ้อมเกตด้วย `uv` ตาม NOW)**: subset เดียวกับเกต (48 โมดูลที่อ่านอิมเมจ/capture ถูก ignore เท่ากัน)
  ⇒ **12,555 passed · 81 skipped · 35,443 subtests · 1 failed** และใบแดงใบเดียวนั้นคือ `test_tree_is_cp874_safe` ที่จับ 🔴 ของผมเอง ซึ่งแก้แล้วและรันซ้ำ
  🔴 นี่คือ **เขียว(cloud sanity)** เท่านั้น ไม่ใช่เกตเต็ม — คำตัดสินจริงมาจาก `ci/<sha>.json` ของ `gate-windows.yml` บน Windows
- `verify_hypothesis_ledger.py` / `verify_functional_coverage.py`: ไม่แตะไฟล์ ledger รอบนี้

## 7) QUEUE_TRIAGE
รอบนี้ **ไม่แตะ `GAME_TEST_QUEUE.md`**: `PANYA 1910` + `NOW 0159` ย้ายเลขใบ/เนื้อใบ/พับผล/archive/snapshot ไป LANE-K
และงานรอบนี้ไม่มีเฟรม ไม่มีแฟล็กใหม่ ไม่มีอะไรที่ผู้เล่นเห็นบนจอ (เป็นเส้นทางคอนโซลของผู้ควบคุม) ⇒ **ไม่มีอะไรให้เทส attended**
READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ตาม `NOW.md` = `GT-288` ชุด 2 (B) → `GT-276` (CS) → `GT-220`/`GT-223` · chief ไม่ได้ตั้งเลขใบและไม่ได้ถอนใบไหนรอบนี้

## 8) ลูกมือ — `pf-adversary` คืนผลก่อนปลดล็อก และ **ไม่ clean**
สั่งต้นรอบพร้อมเริ่มงาน ขอบเขต `runtime_console.py` + `test_runtime_console.py` อย่างเดียว read-only (มันทำงานบนสำเนาใน `/tmp` ไม่แตะรีโป · ยืนยันต้นไม้ไม่เปลี่ยน)

### จ่ายแล้วในคอมมิตที่สองของรอบนี้ (สามข้อ)
- 🔴 **F1 (HIGH)** — `encoding`/`errors` ตอบแทน `self._console` **แม้หลังถอด** ทั้งที่ `write()` ย้ายไป fallback แล้ว
  มิเรอร์เหนือคอนโซล utf-8 ที่ถอดลงจอ cp874 รายงาน utf-8 ⇒ `console_safe()` ไม่พับ ⇒ จอ raise `UnicodeEncodeError` ⇒ ตัวกลืนของใบ `1441` กินทิ้ง ⇒ **บรรทัดไม่ถูกบันทึกที่ไหนเลย** = แผลเดียวกับที่ใบ `1346` มีไว้กัน
  ⇒ แก้ให้ตอบแทน "สตรีมที่กำลังเขียนอยู่จริง" ซึ่งเป็นคำที่ใบ `1346` ใช้เอง
- **T3** — ใบ `1441` สั่งทั้ง `write()` และ `flush()` แต่ปักไว้แค่ `write()` ⇒ เพิ่มเทสปัก `flush()`
- **T4 + ถ้อยคำค้าง** — คอมเมนต์ของเทส exit code ยกความดีของคอมมิตแรกของ PR นี้มาเป็นของ PR (มันวัดได้: 120 ก่อน `5e5e75a` · 0 ตั้งแต่นั้น) และเทส D5 ยังเขียนว่า "D2 ยังไม่ตัดสิน" ทั้งที่ใบ `1346` ตัดสินแล้ว

### 🔴 ยังไม่จ่าย — รอบหน้าหยิบเป็นงานแรก ห้ามนับว่าจ่ายแล้ว
- **F2 (HIGH)** `_fallback is None` (เส้น `pythonw.exe`/`Start-Process -WindowStyle Hidden` ที่ `sys.stdout` เป็น `None`) ⇒ **ข้อความหายเงียบสนิท และคำเตือนไม่ยิงเลย** — คำเตือนยิงบนเส้นที่ข้อความถึงมือ และเงียบบนเส้นเดียวที่ข้อความถูกทำลาย
- **F4 (HIGH)** ไฟล์ retained เปิดแบบ **strict** (`runtime_console.py` `open("x", encoding="utf-8", ...)` ไม่มี `errors=`) แต่ property รายงาน `"replace"` ของคอนโซล ⇒ surrogate เดี่ยว (`os.fsdecode` ของชื่อไฟล์) เขียนลงจอสำเร็จแล้ว retained raise ทะลุออก `print()` · ทางแก้ที่มันเสนอ = แคบกว่าของสอง sink หรือเปิด retained ด้วย `errors="replace"` — **เป็นการเปลี่ยนพฤติกรรมของไฟล์หลักฐาน ผมไม่ตัดสินเอง ส่ง COO**
- **F6** `_live_stream` ไม่เคยเช็ค `.closed` ⇒ เลือกสตรีมที่ปิดแล้วเป็นเป้า forward แล้วรายงานว่าสำเร็จ (เส้น `close_console_streams=True` ปิด `CONOUT$` จริง)
- **F7** `_live_stream` คืน `_Mirror` ที่ถอดแล้วเมื่อเจอวง ⇒ ผิดสัญญาใน docstring ของตัวเอง และ `close()` ใช้ฟังก์ชันเดียวกันเลือก `sys.stdout` ตัวใหม่
- **F8** `isatty()`/`fileno()` ยัง raise หลังถอด (เหตุผลเดียวกับ `_reported_text_attr` ทุกตัวอักษร) · `writable()` คืน `True` ให้มิเรอร์ที่ทิ้งทุกอย่าง
- **F9** `close()` ปิด retained สองไฟล์แบบไม่จับคู่ ⇒ ตัวแรก raise = ตัวที่สองค้างเปิด และบล็อก `_close_console_streams` ไม่ได้รัน
- **F10 (ผลลบ ผมนับเป็นข่าวดี)** มันพยายามสร้าง deadlock ลำดับล็อกตามที่ผมถามแล้ว **ทำไม่ได้** — การสแนปช็อตใต้ล็อกแล้ว I/O นอกล็อกปิดทาง AB-BA จริง · เหลือ race เล็ก: `_live_stream` อ่าน `_detached`/`_fallback` โดยไม่ถือล็อกของมิเรอร์นั้น
- **T2** ไม่มีเทสไหนสร้างมิเรอร์ที่ถอดแล้วโดย `_fallback is None` เลย = บรรทัดที่ไม่เคยถูกรัน
- **คำถามออกแบบที่มันทิ้งไว้ และผมยังไม่มีคำตอบ**: มิเรอร์มีสาม sink ที่ความสามารถไม่เท่ากัน (console · retained · fallback) — **ทุก property ในอนาคต (`isatty` `fileno` `writable` `newlines` `buffer`) ต้องเลือก sink และยังไม่มีกฎข้อเดียวบอกว่าเลือกยังไง** ⇒ F1/F4 จะกลับมาเรื่อย ๆ ในชื่ออื่นจนกว่าจะมีกฎนั้น

🔴 **มันยังรายงานว่า `#1039` ทิ้งคอมมิต `7293d61` ที่แดงไว้บนกิ่ง (H1)** — ตรงกับสิ่งที่ผม root-cause ได้เอง ต้นไม้รอบนี้ซ่อมแล้ว (audit exit 0)
🔴 **T1 ของมันวัดบนสแนปช็อตก่อนผมรัดเทส** (มันเห็น 14 เทส ต้นไม้สุดท้ายมี 17) — ข้อนั้นตรงกับ M3 ที่ผมจับได้เองและแก้ไปแล้วในรอบนี้ (นับ hop) ผมไม่นับซ้ำเป็นสองข้อ

## 9) จดหมายที่บริโภครอบนี้ (สำเนาไป `consumed/` + stub ครบใน commit เดียวกัน · 4 ใบ)
`20260907_1441_COO-DECISION-chief1404-console-forward-and-count-LANE-E` · `20260907_1441_COO-DECISION-chief1404-d2-already-ruled-LANE-E`
`20260907_1441_COO-TO-CHIEF-section7-block` · `20260907_1452_SYNC-NOTICE-pirate-force-server-pr1039-closed-never-merged`

## รอบหน้าทำอะไร
1. 🔴 **ข้อที่ยังไม่จ่ายของ adversary = งานแรก** (รายการเต็มใน §8): F2 · F4 (ต้องให้ COO เคาะก่อน) · F6 · F7 · F8 · F9 · T2
2. 🔴 **สามใบแดงใน PR เดียว** GM-062 → GM-063 → DB op5 — เลื่อนมาสามรอบแล้ว **ห้ามเลื่อนอีก**
3. `gate-windows` ข้อ (3) ของใบ `1141`: 9b เพิ่ม `^_+ .+ _+$` + เช็คเอาต์ `pf_bridge` (ใบ `1441_COO-DECISION-a1410-gate-py314-and-9b-LANE-E` ยังไม่บริโภครอบนี้)
4. **CS ประตูคลาส** (`20260907_0907`) — ตัวบล็อกหมดแล้ว ต่อสายได้ทันที
5. `player_wire.py:57` POTENTIAL คีย์ `n_ID` (ใบ `1441_COO-DECISION-cs1345-player-wire-docstring-LANE-E` ยังไม่บริโภครอบนี้)
6. หนี้ขนาด `AGENTS.md` 13 KB ที่เหลือ — หั่นเป็นใบเล็กของตัวเอง ท่าเดียวกับ §10 (ย้ายคำต่อคำไปไฟล์สด ไม่ใช่ archive)

SCOREBOARD: COMING | ผู้ควบคุมที่ปิดคอนโซลซ้อนกันสองชั้นจะเห็นบรรทัดหลังปิดบนจอต่อไป แทนที่เซิร์ฟเวอร์จะเงียบแล้วออกด้วย exit 120 และกลืนบรรทัดสุดท้าย | pf_bridge#1735 + pirate-force-server#1046 (กู้จาก #1039 ที่เกตปิด) sha 25669428
