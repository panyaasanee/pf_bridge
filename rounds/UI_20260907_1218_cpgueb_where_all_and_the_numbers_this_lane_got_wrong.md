# LANE-UI รอบ `cpgueb` — `--where-all` ตามที่ COO อนุมัติล่วงหน้า + re-derive เลขที่สายนี้เขียนผิดเอง

- เริ่ม 2026-09-07T12:18+07:00 · claim `pf_bridge#1702`
- ล็อกรอบ: list PR เปิดใน `pf_bridge` ก่อนเปิดใบ — **ไม่มี** `[LANE-UI] round <id>: claim` ใบอื่น
  (`#1659`/`#1676` เป็นใบ **addendum** ไม่ใช่ claim · ใบสายอื่น `#1700` `#1701` ไม่ใช่ล็อกของสายนี้
  ห้ามถอยเพราะเห็นมัน) ⇒ claim สด ไม่ใช่ takeover
- กล่องจดหมาย: `grep -l "ADDRESSEE: LANE-UI"` ตัดใบที่มี `.CONSUMED.txt` ⇒ **หนึ่งใบ**
  `20260907_1141_COO-DECISION-ui1101-where-stays-one-file-LANE-UI.md` — บริโภครอบนี้ (stub วางแล้ว
  ต้นฉบับสำเนาไป `consumed/`)
- `NOW.md` (ตรวจ `1141`) แถวของสายนี้: "งานแรก `2032` แถบ n/327 · `1141` `--where` = ไฟล์เดียวคงไว้ ·
  `--where-all`+stderr อนุมัติล่วงหน้า (stdout 1 บรรทัด · re-derive เอง · 46→11)" —
  **รอบนี้ทำครบทั้งแถว**

## รอบนี้ขยับ NOW/M ข้อไหน
**ไม่ขยับบันไดไมล์สโตน** · M2 ยังติด `RE-286`/`0x1FB2` (ของ LANE-A) · คิวข้อ 1-2 ของสายนี้
(UI-B ล็อกเอาต์ · UI-A กลับหน้าเลือกตัวละคร) ยังติด `RE-266` — blocker เดิม บันทึกไว้แล้วรอบ `jx6r5p`
**ไม่ใช้รอบไปตรวจซ้ำ** (กฎในไฟล์สาย)
สิ่งที่ขยับ = **แถว LANE-UI ของ `NOW.md` ทั้งแถว** ปิดครบสามเงื่อนไขของ COO-DECISION `1141` (ค)

## งานแรกตามที่ COO สั่ง: re-derive เลขเอง ห้ามลอกจาก reviewer
COO `1141` เขียนตรง ๆ ว่า "**งานแรกของรอบหน้า**: แก้ docstring ต้นตอ `_iter_py_files` — **re-derive เอง**
ห้ามลอกเลข 11 จาก reviewer ต่ออีกทอด" · ทำแล้ว ทุกเลขข้างล่างสายนี้รันเอง ไม่มีเลขไหนลอกมา

### `46` → `11` [วัดแล้ว รอบ `cpgueb`]
```
python3 -c 'import sys; sys.path.insert(0, "tools");
import pf_ui_wire_name_census as c;
print(len(c.multi_file_counted_names([n for _w, n in c.load_names()])))'
-> 11
```
ชื่อทั้ง 11: `VitalData`(7 ไฟล์) `ActionVital`(4) `UpdateAttrVital`(5)
`Channel_GMGlobalMessageVital`(3) `TargetVital` `TeleportVital` `TargetPosVital`
`CheckSecondPwdVital` `GM_RunGMCommandVital` `Activity_CheatCodeVital`
`Channel_LocalTalkMessageVital` (อย่างละ 2)
🔴 และคราวนี้ **มีเทสรันซ้ำ**: `MultiFileCountIsRederivedTests` — ไม่ใช่แค่ docstring ที่ประกาศเลข
แล้วไม่มีอะไรค้ำ ซึ่งเป็นวิธีที่ `46` รอดมาทั้งรอบ

### `4` → `7` แถว SOURCE ที่อยู่ใต้ `gm/` [วัดแล้ว]
```
awk -F'\t' '$5=="SOURCE" && $6 ~ /\/gm\//' reports/PF_UI_WIRE_NAME_CENSUS_20260906.tsv | wc -l
-> 7   (gmui_catalog.py 4 + command_capture.py 2 + teleport_wire.py 1)
```
`4` คือจำนวนแถวของ **ไฟล์เดียว** ไม่ใช่ของแพ็กเกจ — และมันคือเลขที่รอบ `8btjto` ใช้อ้างว่า fixture
เหมือนของจริง แก้ทั้งสองที่ (`:1161` docstring ของคลาส · คอมเมนต์ที่ fixture)

### โน้ตพิน `PYTEST_SKIP_PINS.json` ที่ประกาศว่างานหนึ่งวินาทีเป็นไปไม่ได้ [วัดแล้ว ทั้งสองทรง]
โน้ตเดิมเขียนว่า reproduce ทรงไม่มี sibling "ทำไม่ได้ในสองรีโปที่สายนี้แตะได้" — **เท็จ** และเป็นการซ้อม
ที่ `pf_bridge/HOWTO_OPEN_A_PR.md:24-31` บังคับอยู่แล้ว วัดที่ `11f937a` บน worktree ที่พาเรนต์ไม่มี `pf_bridge`:
```
git worktree add --detach <scratch>/pirate-force-server HEAD
cd <scratch>/pirate-force-server && python3 -m pytest tests/test_ui_wire_name_census.py -q
-> 56 passed, 13 skipped
sed -i 's/^@UI_WIRE_CENSUS_INPUTS\.skip_unless_present()$/# UNGUARDED-REHEARSAL/' tests/test_ui_wire_name_census.py
python3 -m pytest tests/test_ui_wire_name_census.py -q
-> 13 failed, 56 passed
```
⇒ อัตราส่วนที่พินนี้ผูกจริงคือ **13 failed / 56 passed** ไม่ใช่ทรง "N failed / 1 passed" ที่ค้างมาจาก
รอบ `on8hbb`/`d1b231` · แก้โน้ตแล้ว

### `grep` ที่ถูกหักล้างแล้ว ที่ที่หก
`tools/pf_ui_wire_name_census.py:44` (บล็อก TIERS) — ห่างจากบรรทัดที่บอกว่า "`grep -n` is NOT" 27 บรรทัด
เปลี่ยนเป็นชี้ `--where` ตรง ๆ

### D7 — ตัวอย่างใน `docs/UI_WIRE_COVERAGE.md` ถูกอ่านลูกศรกลับข้าง
รอบ `8btjto` เอา `...command_capture.py:800` ออกเป็น `gm/<file>.py:<line>` โดยเข้าใจว่า `800` เก่าไปแล้ว
**ไม่ใช่** — `800` คือ *ปลายทาง* ที่ `6b5b6b8` ย้ายแถวไป (`750 -> 800` อยู่ในหน้าเดียวกันเหนือขึ้นไปสองย่อหน้า)
และวันนี้ `--where` ก็ยังตอบ `800` [วัดแล้วรอบนี้] · ที่แย่กว่านั้นคือ placeholder **ซ่อนชื่อไฟล์** ซึ่งไม่ drift
มีเทสปักสองใบ และทำให้ดูเหมือนคำตอบทุกอันอยู่ใต้ `gm/` ทั้งที่ **23 จาก 30 แถว SOURCE ไม่ได้อยู่ใต้ `gm/`**
[วัดแล้ว: `awk ... $6 !~ /\/gm\//` = 23] · คืนคำตอบจริงพร้อมป้าย "dated reading, not a pin"
แบบเดียวกับที่หน้านี้ใช้กับ `18 จาก 30` และ "บรรทัด 3 กับ 4" อยู่แล้ว

## `--where-all` — เงื่อนไขสามข้อของ COO ครบทั้งสาม
1. **stdout ยังหนึ่งบรรทัด** — `--where` พิมพ์ `path:line` บรรทัดเดียวเท่าเดิม
   `test_where_keeps_one_stdout_line_and_counts_the_rest_on_stderr` ปักไบต์ต่อไบต์
2. **`+N more files` ลง stderr** — และเป็นข้อเท็จจริงของชื่อนั้นจริง ไม่ใช่ของประดับ:
   `test_a_single_file_name_still_gets_a_silent_stderr` ฆ่ามิวแทนต์ที่พิมพ์ `+0 more files` เสมอ
3. **โหมดเต็มเป็นชื่อใหม่ `--where-all`** — ส่งสองแฟล็กพร้อมกัน = exit 2 ไม่เดาให้

🔴 **สองโหมดเดินเครื่องเดียวกัน**: `iter_source_hits()` เป็น generator ตัวเดียว `--where` หยิบตัวแรก
`--where-all` หยิบทั้งหมด ⇒ มิวแทนต์บรรทัดเดียวที่ทำให้สองโหมดตอบคนละไฟล์/คนละลำดับ/คนละการสะกด path
สร้างไม่ได้ (บทเรียน D-A จาก `#1013` ที่รอบ `8btjto` เพิ่งปิดสำหรับ `--where` กับอาร์ทิแฟกต์)
· lazy ไว้ด้วย: `source_hit_location` ยังหยุดที่ hit แรก คนที่รันทีละ 327 ชื่อไม่ต้องจ่ายค่าเดินทั้งทรี

`multi_file_counted_names()` เป็น **implementation ที่สอง** โดยตั้งใจ ไม่ใช่ wrapper ของตัวแรก —
เพราะ pf-adversary D10 บน `#1017` ชี้ว่าเทส "one-pass equivalent" ของรอบ `8btjto` เป็นวงกลม
(`f(x) == f(x)`) เทสรอบนี้เทียบ **สามทาง**: one-pass ของ tool · derivation ที่เขียนในตัวเทสเองจากสองพรีมิทีฟ
(`census_file_texts` + `code_token_lines`) · และ per-name walk ที่ค้ำ `--where-all` จริง (รันเฉพาะ 11 ชื่อที่ถูกชี้)

## หลักฐานสองชั้น
- **ชั้น client-observable**: ไม่มี — รอบนี้ไม่มีเฟรมถึงไคลเอนต์ ไม่มีปุ่มใหม่ ไม่มีอะไรบนจอผู้เล่น
  พูดตรง ๆ: **นี่คือรอบเครื่องวัด ไม่ใช่รอบผลงานที่ผู้เล่นเห็น**
- **ชั้นเครื่องมือ/ทรี**: คำสั่งทุกอันข้างบนรันซ้ำได้ · `--where` **ไม่เปลี่ยนคำตอบ** เทียบกับ `origin/main`
  ทีละชื่อครบ 327 ชื่อ [วัดแล้ว]: สคริปต์ `exec` ตัว `tools/pf_ui_wire_name_census.py` ของ `origin/main`
  เข้ามาเป็นโมดูลที่สอง แล้วเทียบ `source_hit_location(name, files)` ของสองเวอร์ชันทีละชื่อ
  ⇒ `names=327 disagreements=0` (ใช้เวลา ~9 นาที เพราะเวอร์ชันเก่าเดินทั้งทรีต่อหนึ่งชื่อ)
- ห้ามใช้ชั้นหนึ่งอ้างอีกชั้น: เทสในไฟล์นี้ไม่ได้พิสูจน์ว่าเกตเขียว และเกตก็ไม่ได้พิสูจน์ค่า `11`

## nonclaims (ข้อที่ **ไม่** ได้พิสูจน์)
- **ไม่ได้พิสูจน์ว่าเลขบรรทัดที่ `--where`/`--where-all` พิมพ์ ถูกปักบนทรีจริง** — คำถามออกแบบที่รอบ `8btjto`
  ทิ้งไว้ (D1: "เลขบรรทัดมีอำนาจอะไร") **ยังไม่ตอบรอบนี้** เพราะงบเวลาหมดกับข้อ 1 ของคิว
- **เกตมองไม่เห็นค่า `11`** — `MultiFileCountIsRederivedTests` ติดการ์ด (ต้องใช้สารบัญ 327 ชื่อในรีโปพี่น้อง)
  ⇒ `gate-windows` ไม่รันมันตลอดไป · ที่เกตเห็นคือ **กลไก** (`MainWhereAllFlagTests` 8 เทสไม่ติดการ์ด +
  `WhereAndCensusCannotDisagreeTests`) เขียนไว้ในโน้ตพินตรง ๆ แล้ว ไม่ปล่อยเงียบ
- **ไม่ได้ยืนยันว่าใบ `0758` ที่ยังมี `grep` ผิดอยู่ในกล่อง COO ถูกแก้** — ใบนั้นไม่ใช่ของสายนี้จะไปแก้
  (เนื้อใบ/พับผล = LANE-K ตาม PANYA `1910`) และ COO ออกใบ `1141-attach-correction-to-0758-LANE-K` ไว้แล้ว
- **`CheatVital` ไม่ถูกใช้เป็นตัวอย่างที่ไหนเลย** ตามที่ COO สั่ง — ตัวอย่างในเอกสารคือ
  `GM_RunGMCommandVital` ซึ่งสายนี้เปิดสองไฟล์ยืนยันเองแล้ว (`command_capture.py:800` เป็นโค้ดจริง
  บรรทัด `vital_name="GM_RunGMCommandVital",` · `gmui_catalog.py:502`)

## adversary
`ADVERSARY_PENDING pirate-force-server#<PR ของรอบนี้>` — สั่งบนคอมมิต `93d28b3` ผลยังไม่คืนตอนปลดล็อก
🔴 **รอบถัดไปงานแรก = รับผลนี้** ตามกฎบ้าน (เหมือน `#1005` และ `#1013` สองรอบก่อน)

## เกต/เทส
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS** (รันหลังอัปเดตพิน)
- `pytest tests/test_ui_wire_name_census.py -q` = **79 passed, 27 subtests passed**
- ชุดเต็ม `pytest tests/` รันเป็นคอมมิตสุดท้ายบนต้นไม้ที่ merge `origin/main` แล้ว — ผลเขียนไว้ใน PR
- ซ้อมทรงไม่มี sibling แล้วทั้งสองทรง (ตัวเลขข้างบน)
- `TWO_SESSIONS_SAME_SCENE:` ไม่เกี่ยว — รอบนี้ไม่แตะโลก/registry/ฉาก ไม่มี state ต่อ process

## รอบถัดไปทำอะไร
1. **รับผล `ADVERSARY_PENDING`** ของรอบนี้ก่อนอย่างอื่น
2. **D1 ของรายงาน `#1017` — ปักเลขบรรทัด**: implementation ที่สองในเทส เทียบ **ไฟล์ + บรรทัด**
   ครบ 30 แถวจริง · แล้วมิวแทนต์สี่ตัวในตาราง D1 ต้องตาย · (ปิด D10 วงกลมไปในตัว — รอบนี้ปิดไปครึ่งหนึ่งแล้ว
   ที่ `multi_file_counted_names`)
3. **D2 ทิศ suffix**: เติมคู่ suffix ลง fixture (`InstanceVital` ⊂ `NavigationEx_EnterInstanceVital`)
4. **D3 สเกล**: fixture ที่ไม่ติดการ์ดต้องข้าม threshold จริง หรือเขียนให้ COO เห็นว่าเกตมองไม่เห็นอะไรบ้าง
5. **D8**: กวาด `U+1F534` ออกจาก `tests/test_ui_wire_name_census.py` และเสนอ chief ว่า `[cp874]`
   ควรสแกน `tests/` ด้วย (เป็นจดหมาย/`CORE-REQUEST` ไม่ใช่แก้เกตเอง)
6. ที่เหลือของคิวเดิม (`RE-266` blocker · แผน `docs/UI_LANE.md`) ยังอยู่หลังข้อ 1-5

SCOREBOARD: NONE | รอบเครื่องวัด ไม่ใช่รอบที่ผู้เล่นทำอะไรได้เพิ่ม: `--where-all` กับเลขที่ re-derive แล้ว เป็นของคนอ่านเอกสาร ไม่ใช่ของคนเล่น · คิวปุ่มจริง (UI-A/UI-B) ยังติด `RE-266` | pf_bridge#1702 · pirate-force-server PR รอบนี้ · sha 93d28b3
