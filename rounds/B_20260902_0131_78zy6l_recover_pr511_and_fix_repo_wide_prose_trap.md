# Round B_20260902_0131 (branch 78zy6l) — LANE-B (COMBAT), scheduled round

เริ่ม 2026-09-02T01:31+07:00 · เขียนไฟล์นี้ 2026-09-02T01:4x+07:00
(เวลาจากคำสั่ง `TZ=Asia/Bangkok date` ทุกจุด ไม่คำนวณเอง · heartbeat ล่าสุด
`_BRIDGE_HEARTBEAT.txt` = 2026-09-02T01:26:02+07:00 ห่าง ~15 นาที ผ่านเกณฑ์ 60 นาที)

## รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ P-1/P-2/P-3 โดยตรง** — และบอกตรง ๆ ว่าทำไม:

- **P-1 (ของดรอปค้างบนพื้น)** ฝั่งโค้ดของสายนี้ทำเสร็จไปแล้วสองรอบก่อน
  (`reconcile_scene_transition` + corpse re-arm fix, server#516 merged) สิ่งเดียวที่ยังกั้น P-1
  ไม่ให้ขยับคือ **จุดเรียกใน `runtime.py` ซึ่งเป็นไฟล์ของ chief** (CORE-REQUEST จากรอบ `4ztr6t`
  ยังไม่ถูกต่อสาย) สายนี้ทำแทนไม่ได้ตามเขตเขียน
- **P-2/P-3** เป็นของสาย GM/RE — ไม่แตะ

**แต่รอบนี้ขยับของจริงสองอย่างที่เกี่ยวกับ P-1 โดยอ้อม:**

1. **กู้รอบที่หายไปทั้งรอบ** (ADDENDUM v2 ข้อ A) — `tests/test_inventory.py` (458 บรรทัด, โมเดล
   Backpack ของ BUILD-006/M5) ถูกปิดทิ้งพร้อม PR server#511 เพราะ gate แดง งานยังอยู่บน branch
   `claude/zen-einstein-i7cwdh` เท่านั้น ไม่เคยขึ้น `main`
2. **ปิดกับดักที่ทำให้รอบนั้นหาย และจะทำให้รอบอื่นหายอีก** — หาสาเหตุที่ gate แดงจริง แล้วแก้ที่ต้นเหตุ

## ต้นรอบ (ตามลำดับที่พรอมป์กำหนด)

1. อ่าน `NOW.md` เป็นไฟล์แรก
2. ล็อกรอบ: ไม่มี PR `[LANE-B]` เปิดค้างในทั้งสองรีโป (เปิดค้างมีแต่ `[LANE-A]` #778/#524 กับ
   `[LANE-GM]` #777/#523 — ไม่ใช่ล็อกของสายนี้ ไม่แตะ) → เปิด draft ยึดล็อกก่อนทำงาน:
   **pf_bridge#779**, **pirate-force-server#525**
3. ชะตา PR รอบก่อน (ADDENDUM v2 ข้อ A): `[LANE-B]` ใบล่าสุดของทั้งสองรีโป **merged=true**
   (server#516 16:37Z, bridge#768 16:25Z) → งานรอบก่อนอยู่บน `main` แล้ว
   แต่ไล่ย้อนขึ้นไปอีกใบพบ **server#511 closed merged=false** และ `tests/test_inventory.py`
   ไม่มีอยู่บน `main` จริง → งานหายจริง หนึ่งรอบเต็ม
4. กล่องจดหมาย: บริโภค 4 ใบที่ยังไม่มี stub (รายละเอียดท้ายไฟล์)
5. ไม่มี `*CLAIM*` ของสายอื่นที่ยังไม่หมดอายุทับหัวข้อนี้ · งานรอบนี้เป็นการกู้งานของสายตัวเอง
   ไม่ใช่ใบที่ระบุผู้ทำได้หลายสาย จึงไม่ต้องวางใบจอง

## สาเหตุที่ gate แดงจริง (วัดจาก log ไม่ใช่เดา)

Run `33522539202`, job `gate` (windows-latest), ตารางสรุป: ทุกช่องเขียวหมด **ยกเว้น**
`pytest_subset exit=1`. เทสที่ล้มมีใบเดียว:

```
tests/test_gate2_bag_admission_wiring.py
  OnlyTheCharacterSelectPathAsksThisPredicate
    ::test_nothing_outside_the_package_calls_it_either
```

เทสใบนั้นรัน `git grep -l bag_admission -- .` **ทั้งรีโปที่ track ไว้** แล้วบังคับว่าทุกไฟล์ที่โผล่มา
ต้องอยู่ใน allowlist ที่ hardcode ไว้ในตัวเทส ไฟล์ใหม่ `tests/test_inventory.py` **เอ่ยชื่อไฟล์พี่น้อง
สองใบใน docstring ของตัวเอง** (`test_bag_admission.py`, `test_gate2_bag_admission_wiring.py`)
สตริงนั้นจึงติด grep → เทสแดง → gate แดง → reaper ปิด PR ทั้งใบ **ทั้งที่ไฟล์นั้นไม่ได้ import,
ไม่ได้เรียก และไม่ได้แตะ predicate นั้นเลยแม้แต่บรรทัดเดียว**

🔴 **นี่ไม่ใช่อุบัติเหตุครั้งแรก** — ในตัวเทสเองมีแผลเป็นเขียนไว้สองรอย (รอบ `uq2lxw`, และ entry ของ
chief รอบ `4gqnwm`) ว่าเคยเสียรอบไปกับกลไกเดียวกัน วิธีแก้ที่ผ่านมาคือ "เติมชื่อไฟล์เข้า allowlist
ทีละใบหลังเกิดเหตุ" ซึ่งไม่ปิดกับดัก แค่เลื่อนมันไปครั้งหน้า และที่แย่กว่านั้น: **ไฟล์รอบ
(`rounds/*.md`) ที่เอ่ยชื่อโมดูลนี้ในภาษาไทยธรรมดาก็ทำ gate แดงได้เหมือนกัน** — ไฟล์รอบของรอบ
`i7cwdh` เองก็มีสตริงนั้นอยู่สองบรรทัด

## ที่สร้างจริง (pirate-force-server, branch `claude/laughing-pasteur-78zy6l`)

### 1. กู้ `tests/test_inventory.py` กลับมา (verbatim)

ดึงจาก `origin/claude/zen-einstein-i7cwdh` ตรง ๆ ไม่แก้เนื้อหาแม้แต่บรรทัดเดียว — 47 เทสตรงของ
`inventory.py` รวมเทสของ `parse_merge_candidate` / `is_exact_merge_request` สองฟังก์ชันที่
`runtime.py` เรียกจริงบนทุก ItemOperate request แต่ไม่เคยมีเทสไหนอ้างชื่อมาก่อน
**ไม่แก้ `src/` แม้แต่บรรทัดเดียว**

### 2. แก้ที่ต้นเหตุ: `tests/test_gate2_bag_admission_wiring.py`

ถามให้ตรงกับชื่อเทสของมันเอง — "มีอะไร**เรียก**มันจากนอกแพ็กเกจไหม" ไม่ใช่ "มีอะไร**เอ่ยชื่อ**มันไหม":

- `PROSE_SUFFIXES = {".md", ".txt"}` — ผ่านโดยกฎ (markdown ในรีโปนี้ไม่ถูกรันโดยอะไรเลย
  ตรวจแล้วว่าไม่มี doctest runner ก่อนเขียนบรรทัดนี้) → **ไฟล์รอบและจดหมายเอ่ยชื่อโมดูลได้แล้ว
  โดยไม่ทำ gate แดง**
- ฟังก์ชันใหม่ `_names_bag_admission_as_code(path)` — คืน "เหตุผล" ถ้าไฟล์ `.py` เข้าถึง predicate
  จริง คืน `None` ถ้าทุกจุดที่เอ่ยเป็นแค่ docstring/คอมเมนต์ กฎที่ใช้ต่อยอดจากกฎเดิมที่ไฟล์นี้ใช้กับ
  ตัวแพ็กเกจอยู่แล้ว: (ก) โผล่ใน AST เป็น identifier (ข) **สตริงที่มีชื่อโมดูลอยู่ในตำแหน่งที่ไม่ใช่
  docstring** (ค) import ตรง ๆ (ง) parse ไม่ผ่าน = ไม่ผ่าน ไม่ปล่อยเงียบ
  🔴 ข้อ (ข) ร่างแรกเขียนเป็น "สตริงที่ไหลเข้า `Call`/`Subscript`" ซึ่งปิด `import_module("...")` /
  `getattr(m, "...")` / `sys.modules["..."]` ได้ แต่ **หลุด** `MODULE = "...bag_admission"` ที่ผูก
  ชื่อไว้ก่อนแล้วค่อยเอาไป import ทีหลัง — รัดกฎเป็น "ไม่ใช่ docstring" ก่อน commit และเพิ่มเทสปักไว้
- allowlist เดิม **ไม่ถูกลบ** — ยังเป็นทะเบียนของไฟล์ที่เรียก predicate จริง ๆ ต่อไป
- คลาสเทสใหม่ `ProseIsNotACallerButEveryDynamicRouteStillIs` — 10 เทส ปักกฎนี้ด้วยไฟล์จริง
  (เขียนไฟล์ `.py` ชั่วคราวแล้วถามฟังก์ชัน ไม่ใช่ assert ลอย ๆ): docstring+comment = ไม่ใช่ผู้เรียก ·
  import / attribute hop / `import_module` ด้วยสตริง / `sys.modules[...]` / `getattr` ด้วยสตริง /
  ไฟล์ parse ไม่ผ่าน = **ยังเป็นผู้เรียกทุกเส้นทาง** · และเทสสุดท้ายถามฟังก์ชันนี้กับไฟล์จริงที่รอบนี้
  กู้กลับมา (`tests/test_inventory.py`) ถ้าวันหลังมันกลายเป็นผู้เรียกจริง เทสนี้จะแดงและรอบนั้นต้องไป
  เขียน allowlist พร้อมเหตุผล

## ที่แก้ในคิว (หัวใบที่สายนี้เปิดเอง เท่านั้น)

`GAME_TEST_QUEUE.md` — **GT-198** หัวใบเขียนว่า "PR #513 ยังไม่ merge ห้ามบูต" ซึ่งไม่จริงแล้ว
(#513 merged 2026-09-01T15:22Z) รันคำสั่ง RECHECK ของใบเองกับ `origin/main`:

- คำสั่งที่ 1 hit (`mob_loot.py:604 DROP_MODEL_TYPE_FIELD_ENABLED = True`)
- คำสั่งที่ 2 **ว่างเปล่า** ทั้งที่โค้ดอยู่บน main จริง — เพราะเขียนเป็น `grep -n -A3
  "def refresh_frames"` แต่ docstring ของ `refresh_frames` ยาว ~55 บรรทัด หน้าต่าง 3 บรรทัด
  จึงไปไม่ถึงตัวบอดี้ **false negative ที่จะกันใบนี้ไม่ให้บูตได้ตลอดกาล**

แก้สองจุด: หัวใบเป็น `PENDING -- ready to boot on origin/main` (ขีดฆ่าข้อความเดิม ไม่ลบ) และแก้คำสั่ง
RECHECK ที่ 2 เป็น `sed -n '/^def refresh_frames/,/^def /p' | grep -n "return
drop_frames_with_model_type"` ซึ่ง hit จริง พร้อมบันทึกว่าเคยเป็น false negative เพราะอะไร
**ข้อกล่าวอ้างของใบไม่เปลี่ยนแม้แต่คำเดียว เปลี่ยนแค่วิธีตรวจ**

## ตัวเลขที่วัดได้

```
tests/test_gate2_bag_admission_wiring.py + tests/test_inventory.py : 82 passed, 2 subtests
สวีตเต็ม (pirate-force-server, ทั้งรีโป)  : 6673 passed, 327 skipped, 13778 subtests, 0 failed (182.96s)
git grep -l bag_admission -- .            : 13 ไฟล์ (รวม tests/test_inventory.py ที่ stage แล้ว) เทสผ่าน
```

🔴 **stage ก่อนวัด** — `git add` ทั้งสองไฟล์ก่อนรันสวีต ตามแผลเป็นที่เขียนไว้ในตัวเทสเอง
(`git grep` อ่าน INDEX ไฟล์ที่ยัง untracked จะมองไม่เห็นและสวีตจะเขียวหลอก)

## pf-adversary

**เรียกจริง** (เซสชันนี้มี Agent tool จริง ตาม `AGENTS.md` ข้อ 107) — สั่ง `pf-adversary` ตรวจ
staged diff ก่อน commit พร้อมรายการเส้นทางหลบเลี่ยงที่ต้องลองพังให้หมด (dynamic import ที่ประกอบ
สตริงเป็นชิ้น, `exec`, ไฟล์ `.cfg/.json/.ps1/.bat/.yml`, `__getattr__`, star-import, alias,
`.pyw/.pyi`, `conftest.py`, path ที่ git grep quote, case ของนามสกุล, ปัญหาเฉพาะ Windows)

**ผลกลับมาแล้วก่อน push** (ใช้เวลา ~17 นาที) — เจอของจริง **9 ข้อ ระดับ HIGH สามข้อ** และ
**แก้ทั้งเก้าข้อก่อน commit** ทุกข้อวัดจริงในเวิร์กทรีแยกพร้อม control กับโค้ดก่อนแก้:

### HIGH ที่ต้องแก้ทันที

- **D1 — ร่างที่สองยังหลุดผู้เรียกจริง** ทำ **module docstring ให้เป็น path ของโมดูลเอง** แล้ว
  `importlib.import_module(__doc__)` — โทเคนไม่โผล่เป็น identifier และไม่โผล่นอก docstring เลย
  แต่เข้าถึง gate ได้จริง (adversary เรียก `may_enter_world` ผ่านไฟล์นั้นสำเร็จ) วัดแล้วว่า guard เขียว
  **แก้:** docstring เป็น "prose" ได้เฉพาะในไฟล์ที่ **ไม่มีเครื่องมือแปลงสตริงเป็นโมดูล** เลย
  (`DYNAMIC_LOOKUP_NAMES`: `__doc__` `import_module` `importlib` `__import__` `exec` `eval`
  `getattr` `modules` `load_module` `spec_from_file_location`) มีอย่างใดอย่างหนึ่ง = สตริงที่มีชื่อ
  โมดูลกลายเป็นผู้เรียกทันที · เพิ่มเทสด้วยเพย์โหลดของ adversary เองสามแบบ (module/class docstring +
  `exec(__doc__)`)
- **D2 — คลาสของบั๊ก #511 ยังไม่ปิดจริง** ร่างที่สองอนุญาตเฉพาะ docstring ดังนั้น **ข้อความ
  assertion / ลิสต์ชื่อไฟล์ / `help=` ที่เอ่ยชื่อไฟล์พี่น้อง ยังทำ gate แดงเหมือนเดิม** คือย้ายกับดัก
  ไปหนึ่งบรรทัด ไม่ได้ปิด **แก้:** กฎใหม่ข้างบนปิดทั้งสองด้าน — ไฟล์ที่ไม่มีเครื่องมือ dynamic
  เอ่ยชื่อได้ทุกตำแหน่ง (เทสใหม่ `test_prose_outside_a_docstring_is_still_prose`)
- **D3 — สองบรรทัดที่ "ทำงานจริง" ของสแกนไม่เคยถูกรันเลย** coverage ชี้บรรทัด 650-652 ·
  adversary ปลูก mutant สามตัว (ปล่อยผ่านทุกไฟล์ `.py` · ใส่ทุกนามสกุลเป็น prose · เปลี่ยน
  pattern เป็นโทเคนที่ไม่มีอยู่จริง) **ทั้งสามตัวเทสยังเขียว** — เทสที่เขียนไว้เทสแค่ฟังก์ชันช่วย
  ไม่ได้เทสตัวสแกน **แก้:** แยกตัวสแกนเป็น `_classify_repo_wide_hits()` / `_repo_wide_hits()` แล้ว
  เขียนคลาสเทสใหม่ `TheRepoWideScanItselfActsOnWhatItFinds` ที่ปลูกไฟล์จริงแล้วขับตัวสแกน
  **วัดซ้ำแล้ว: mutant ทั้งสามตัวตายหมด** (B: 4 failed · A: 3 failed · C: 2 failed)

### ที่เหลืออีกหกข้อ แก้ในรอบเดียวกัน

- **D4** ไม่เคยเช็ค `git grep` returncode — นอกรีโป exit 128 + stdout ว่าง = "ไม่มีใครเรียก"
  วัดแล้วว่าเขียวทั้งที่มีผู้เรียกฉาว ๆ · แก้: เช็ค returncode + ปัก lower bound `>= 8` hits
- **D5** BOM (Windows PowerShell/Notepad) ทำให้ไฟล์ prose กลายเป็น `"unparseable python"` = gate แดง
  ทั้งที่ python เองอิมพอร์ตไฟล์นั้นได้ · แก้: อ่านด้วย `utf-8-sig` (ทั้งฟังก์ชันใหม่และ
  `_imports_bag_admission` เดิม)
- **D6** `core.quotePath` ทำให้ path ที่มีอักขระนอก ASCII ถูก quote → นามสกุลเพี้ยน → ผู้เรียกจริง
  ถูกรายงานว่าเป็น "ไฟล์ข้อมูล" · แก้: `-c core.quotePath=false` + `-z`
- **D7** `.pyw`/`.pyi` (entry point จริงบน Windows) ตกช่อง "ไม่ใช่ python" และเทียบนามสกุลแบบ
  case-sensitive · แก้: `PYTHON_SUFFIXES` + `.suffix.lower()` ทั้งสองด้าน
- **D8** เทสใหม่ผูกกับ prose ของ `test_inventory.py` (ตกแต่ง docstring ไฟล์อื่น = gate แดง) และ
  ข้อความ fail ทิ้งไฟล์ 458 บรรทัดลงคอนโซล cp874 · แก้: ตัด `assertIn` ทิ้ง เหลือคำถามเดียวคือคำตัดสิน
- **D9** `.txt` ถูกใส่ในชุด prose โดยไม่มีใครเถียงให้ — และในรีโปนี้ `.txt` ไม่ใช่ prose เฉย ๆ
  (`docs/.round_claim_*.txt` คือ **ล็อกรอบ**) · แก้: เอา `.txt` ออก เหลือ `.md` อย่างเดียว
- **D10** (exposure ไม่ใช่ defect) ไฟล์รอบมี `U+1F534` ที่ไม่มีใน cp874 — adversary หาโปรแกรมที่
  อ่าน `rounds/` ไม่เจอเลย จึงไม่ยิง ไม่แก้ แต่บันทึกไว้

### คำถามออกแบบที่ adversary ทิ้งไว้ (ยังไม่ตอบ ไม่แกล้งตอบ)

"ทำไมเทสนี้ต้องนับผู้เรียกด้วยการ grep ข้อความ แทนที่จะ import แพ็กเกจแล้วยืนยันสมบัติตรง ๆ ว่า
`may_enter_world` ถูกอ้างโดยโมดูลเดียวคือ `session`" — เป็นคำถามที่ถูก แต่ครึ่งที่สแกนนี้ดูแลคือ
**นอกแพ็กเกจ** (`tools/`, entry point, สคริปต์) ซึ่ง import เข้ามาเดินไม่ได้ปลอดภัย รอบนี้จึงไม่
เปลี่ยนสถาปัตยกรรม บันทึกไว้ในจดหมายถึง chief เป็นข้อเสนอ ไม่ตัดสินเอง

**สิ่งที่ตรวจเองก่อนส่งให้ adversary** (ทำตามขั้นตอนด้วยมือ):

1. **หาเส้นทางหลบเลี่ยงเอง แล้วเจอจริงหนึ่งจุด ก่อนที่ใครจะบอก** — ร่างแรกของ
   `_names_bag_admission_as_code` เช็คเฉพาะสตริงที่ไหลเข้า `Call`/`Subscript` ซึ่ง **หลุด**
   `MODULE = "pirateforce_foundation.bag_admission"` ที่ผูกชื่อไว้ก่อนแล้วค่อยส่งให้
   `import_module` ทีหลัง → รัดกฎใหม่เป็น "สตริงที่ไม่ได้อยู่ในตำแหน่ง docstring = ผู้เรียก"
   และเพิ่มเทส `test_a_name_bound_for_a_later_dynamic_import_is_a_caller` ปักไว้
2. **fail-closed ทุกทางออก** — นามสกุลที่ไม่ใช่ `.md/.txt/.py` (เช่น `.json/.ps1/.pyw/.pyi`),
   path ที่ `git grep` ใส่เครื่องหมายคำพูด, ไฟล์ที่อ่านไม่ได้, ไฟล์ที่ `ast.parse` ไม่ผ่าน — ทุกกรณี
   **ตกไปทางถูกแจ้ง** ไม่ใช่ผ่านเงียบ (เทส `test_an_unparseable_file_is_not_cleared_as_prose` ปักข้อสุดท้าย)
3. **alias/รูปแบบ import ทุกแบบ** — `_imports_bag_admission` เดิมจับทั้ง
   `from ... import bag_admission [as x]` และ `from ...bag_admission import ...` (อ่านโค้ดของมัน
   ไม่ใช่เชื่อชื่อฟังก์ชัน) + เทส `test_an_import_is_a_caller`
4. **เทสไม่ผ่านแบบว่าง ๆ** — ทุกเทสในคลาสใหม่เขียนไฟล์ `.py` จริงลงดิสก์แล้วถามฟังก์ชัน และเทสที่
   คาด `IsNotNone` ทุกใบใช้ซอร์สที่ `ast.parse` ผ่านจริง (ไม่ได้ผ่านเพราะ "unparseable")
   ยกเว้นใบที่ตั้งใจทดสอบ unparseable ซึ่ง assert ข้อความเหตุผลตรงตัว
5. **หลักฐาน end-to-end ไม่ใช่แค่ยูนิต** — `git add` ไฟล์รอบ `.md` ที่มีสตริงนั้นจริงเข้า INDEX
   แล้วรันเทสซ้ำ: `git grep` เห็นไฟล์นั้นจริง และ guard ยังเขียว (ก่อนแก้ ไฟล์นี้จะทำ gate แดง)
6. **สวีตเต็มทั้งรีโปสองรอบ** (ก่อนและหลังรัดกฎข้อ 1) 0 failed ทั้งสองรอบ
7. **ไม่ใช้ `git add -A`** — stage ทีละไฟล์ และอ่าน `git diff --cached` ทั้งก้อนก่อน commit
   (`AGENTS.md` ข้อ 104)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่มีอะไรต่างบนจอ** — รอบนี้เป็นการกู้เทสที่หายกับปิดกับดักของ gate ไม่มีบรรทัดใน `src/` ถูกแก้
สิ่งที่ผู้เล่นจะได้จริงคือทางอ้อม: **ใบเทส GT-198 (ของตกพื้นมีโมเดล 3D ไหม) บูตได้แล้ว** จากเดิมที่
หัวใบสั่งห้ามบูตด้วยข้อมูลที่ล้าสมัยและคำสั่งตรวจที่ให้ผลลบเสมอ — นั่นคือใบที่จะตอบคำถามของ P-1
ครึ่งหนึ่งว่าของที่ตกลงพื้น "เห็นเป็นของ" จริงหรือยัง

## จดหมาย/CLAIM ที่บริโภค/เปิดรอบนี้

บริโภค 4 ใบ (เขียน `.CONSUMED.txt` + สำเนาเข้า `consumed/` ครบ ไม่ลบต้นฉบับ):

- `20260901_2322_CHIEF-REPLY-re157-job2-spec-c-wired.md` — สเปก (ค) ต่อสายครบทั้งสองจุดแล้ว
  ไม่มีอะไรให้สายนี้สร้างต่อ · ช่องหลักฐานฝั่ง M2 ยัง `[เสนอ]` แต่ใบเองบอกว่าไม่บล็อก ไม่เปิดใบใหม่
- `20260901_2323_CHIEF-TO-LANE-B-codex-p05-corpse-rearm-and-drop-leak-assigned.md` — สองข้อที่
  มอบหมาย **ทำเสร็จและ merge แล้ว** ตั้งแต่รอบ `4ztr6t` (server#516) สิ่งที่ยังค้างคือจุดเรียกใน
  `runtime.py` ของ chief เท่านั้น
- `20260901_2346_COO-DECISION-concurrent-lane-b-race-accept-add-refetch-before-finalize.md` —
  **ทำตามจริงในรอบนี้**: fetch + rebase ทับ `origin/main` อีกครั้งก่อนแก้ title/body และก่อนปลด draft
- `20260901_1741_LANE-B-STATUS-field-mobs-wiring-doc-drift-fixed-p1-not-a-blocker.md` — ใบของสายเอง

ไม่เปิดใบ RE/GT ใหม่รอบนี้ · ไม่วาง CLAIM (ไม่ใช่หัวข้อที่หลายสายหยิบได้)

## CORE-REQUEST ถึง chief

**ย้ำใบเดิมจากรอบ `4ztr6t` ไม่ใช่ใบใหม่** — ตราบใดที่ `runtime.py` ยังไม่เรียกสองจุดนี้ P-1 ขยับไม่ได้เลย
ไม่ว่าสายนี้จะเขียนอะไรเพิ่มอีกกี่รอบ:

1. `hostile_census_frames(..., transitioning=(scene, actor_identity))` ที่ `runtime.py:4743-4760`
2. `cell.reconcile_scene_transition()` ตรงจุด scene-sync (`runtime.py:4111-4191`)

## จบรอบ

- pirate-force-server: push แล้ว → PR **#525**
- pf_bridge: push แล้ว → PR **#779**
- ลำดับท้ายรอบตามพรอมป์ข้อ 1→2→3→4 (marker `PF-AUTOMERGE: v4` ลง body **ก่อน** ปลด draft เสมอ
  แล้ว GET กลับมายืนยัน · wake gate commit เปล่าเฉพาะรีโปเซิร์ฟเวอร์)

## หมายเหตุไฟล์รอบ

`rounds/B_20260902_0131_78zy6l_WIP.md` ที่ commit ไว้ตอนยึดล็อกถูกลบในรอบเดียวกัน — เป็นไฟล์
placeholder ที่ประกาศตัวเองว่าเป็น WIP ไม่ใช่หลักฐานหรือประวัติ และกติกาคือหนึ่งไฟล์ต่อรอบ
เนื้อหาจริงทั้งหมดอยู่ในไฟล์นี้ (ตัว placeholder ยังอยู่ในประวัติ git ของ branch นี้)
