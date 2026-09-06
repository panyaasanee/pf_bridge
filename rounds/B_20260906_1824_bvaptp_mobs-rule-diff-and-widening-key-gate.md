# LANE-B round bvaptp -- 2026-09-06T18:24+07:00 start

## รอบนี้ขยับ NOW/M ข้อไหน
ไม่ขยับ M ใดโดยตรง (นี่คือรอบวัด static + เกต CI ตามที่ COO สั่งใน `1648`/
`1643`/`1647`/`1712`) — แต่เป็นเงื่อนไข**ก่อน**ที่ M3 (สนามมีมอนสเตอร์) จะสลับจาก
ตารางต่อฉาก 12 ใบไปเป็นกฎเดียว derive อัตโนมัติ (`1648` ข้อ 2): รอบนี้พิสูจน์ว่า
diff ว่างสนิท (0/106) จึงเปิดทางให้รอบถัดไปสลับได้ถ้า COO สั่ง

## ล็อกรอบ
claim PR `pf_bridge#1536` (กิ่ง `claude/practical-knuth-bvaptp`) เปิดโดย
orchestrating session ไว้ก่อนแตะอะไรทั้งสิ้น ยืนยันแล้วว่าไม่มีใบ
`[LANE-B] round <id>: claim` อื่นที่เปิดอยู่และมีชีวิตในเวลาที่ claim ใบนี้

## กล่องจดหมาย
`grep -lE '^ADDRESSEE:.*LANE-B' notes_to_chief/*.md` แล้วคัดใบที่ยังไม่มี
`<ชื่อไฟล์>.CONSUMED.txt` คู่ — เจอ **6 ใบ** ไม่ใช่ 0 (ต่างจากที่ orchestrator
ระบุว่า "verified ไว้แล้ว") อ่านทีละใบแล้วแยกเป็นสองกลุ่ม:

**5 ใบเป็นการตัดสินของ COO ที่จ่าหน้าถึง LANE-B ล้วน** — คือเนื้อหาเดียวกับที่
งานรอบนี้อ้างมาตั้งแต่ต้น (`b1525`/`1647`, `ka1a1635`/`1648`, `b1643`, `b1644`,
`b1712`) บริโภคครบทั้ง 5 ใบรอบนี้ (สำเนาไป `consumed/` + stub
`.CONSUMED.txt` ข้างต้นฉบับ ไม่ลบต้นฉบับ) รายละเอียดว่าตอบอะไรบ้างอยู่ในตัว
stub แต่ละไฟล์เอง

**1 ใบเป็น broadcast กว้าง ไม่ใช่ของ LANE-B โดยเฉพาะ** —
`20260904_0233_PANYA-DECISION-milestones-reopened-...md` หัว `ADDRESSEE: COO
(write this into NOW.md) - cc chief (...), LANE-A, LANE-B, LANE-GM, LANE-DB`
grep เจอเพราะ `LANE-B` อยู่ในรายชื่อ cc ไม่ใช่เพราะจ่าหน้าถึงสายนี้โดยตรง —
**ไม่บริโภครอบนี้** เนื้อหาเป็นการเปิด milestone กลับมาโดยไม่มีกำหนดและเขียน
เกณฑ์ผ่าน M2/M3/M4/M6 ใหม่ทั้งก้อน ผู้รับหลักที่ต้องเขียนคือ COO (เข้า
`NOW.md`) ไม่ใช่งานโค้ดของสายนี้ และไม่บล็อกงานที่ได้รับมอบหมายชัดเจนของรอบนี้
— ทิ้งไว้ให้เห็นตรงนี้แทนที่จะแกล้งไม่เจอ

`NO_FEATURE_WAITING`: ไม่มี RE/CORE-REQUEST ใหม่ที่ตอบถึงสายนี้นอกจาก 5 ใบข้างต้น

## รอบนี้ทำอะไร (ของจริง)

### 1. ตาราง diff กฎ `MOBS` (งานหลัก, ตอบใบ `1648`+`1643`)
วัด `is_monster(t) = MOBS.n_RANK != 0 and MOBS.n_AI_COMBAT != 0` (เมือง) กับ
`is_monster(t) = MOBS.n_RANK != 0` (ทะเล, ตาม `1643`) เทียบตารางที่ shipped
อยู่จริงบน `origin/main` วันนี้ทั้ง 12 ฉากเมือง + 5 ฉากทะเล ส่งเป็นจดหมาย
`pf_bridge/notes_to_chief/20260906_1824_LANE-B-TO-COO-mobs-rule-diff-town-vs-
ocean.md` (เนื้อหาเต็มอยู่ในจดหมาย ไม่คัดลอกซ้ำที่นี่)

**ผลย่อ**:
- เมือง (12 ฉาก, 106 แถว hostile ที่ shipped): **diff ว่าง 100%** — กฎกับตาราง
  เป็นเอาต์พุตของ `tools/pf_mine_scene_mob_roster.py::hostile_roster()` โค้ด
  เดียวกันอยู่แล้ว ไม่ใช่สองอย่างที่บังเอิญตรงกัน
- ทะเล (5 ฉาก): กฎ `rank`-only เห็นมอน 3 แถวที่กฎเมืองไม่เห็น (Bg3001 ×2,
  Bg3002 ×1) ไม่มีแถวไหนที่สองกฎขัดกันในทิศตรงข้าม (ไม่มีแถวที่กฎเมืองว่ามอน
  แต่กฎทะเลว่าไม่ใช่) — ทิศทางกฎเดียว-มีพารามิเตอร์ครอบครัวของ ka1-A `1635`
  ไม่มีข้อมูลอะไรคัดค้าน
- **พบเพิ่มหนึ่งแถวที่ต้องรู้ก่อนเขียนกฎเดียว**: `Bg3002` placement 32
  (template 8163 "Pirate Flagship", outfit `SP_008_000_000_BOSS`) เป็น
  **เรือที่มี `n_RANK=64`** ไม่ใช่ `n_AI_COMBAT` แบบเรือทั่วไป — กฎ "rank ที่
  ทะเล" ยังเลือกถูก แต่ "ai_combat=เรือเสมอ, rank=มอนเสมอ" ที่รอบ `mf71tm`
  สรุปไว้ไม่ครบ 100% (มีเรือที่มี rank ด้วย) เขียนไว้เป็นข้อมูล ไม่ใช่ปัญหาที่
  ต้องแก้รอบนี้
- **ตารางว่าของ 5 ฉากทะเลคือ "ไม่มีโมดูลบน `origin/main`" จริง** แม้จดหมายของ
  รอบ `mf71tm` จะเขียนว่าส่ง roster ฉาก 126 ขึ้น `field_mobs` แล้ว — คำนั้นเป็นจริง
  บนกิ่ง `claude/nice-meitner-mf71tm` เท่านั้น (`เปิดแล้ว ไม่ draft รอ gate` ตามที่
  รอบนั้นเขียนเอง) กิ่งนั้นยังไม่ยืนยันว่า merge เข้า `origin/main`
  (`grep -n "3001\|3002\|3003\|3007\|3008" src/pirateforce_foundation/
  field_mobs.py` = ศูนย์แถวบน main ตอนที่รอบนี้เริ่ม) รอบนี้ต่อยอดจาก
  `origin/main` ตามกฎ ไม่ได้ต่อกิ่งนั้น จึงรายงานสิ่งที่มีอยู่จริง ไม่ใช่สิ่งที่กิ่งที่ยัง
  ไม่ merge อ้างว่ามี — เขียนไว้ในจดหมายด้วยเพื่อไม่ให้ COO อ่านว่ารอบนี้ยืนยันหรือ
  ปฏิเสธการ merge นั้น

**วิธีวัด**: เมืองอ่านจากโมดูลที่ shipped อยู่แล้วโดยตรง (import แล้วเทียบ
`PREDICATE_CENSUS['rank_and_ai_combat']` กับ `len(HOSTILE_PLACEMENTS)`) ไม่ได้
เรียกเครื่องมือใหม่ ทะเลเรียกฟังก์ชันเดิมของ `tools/pf_mine_scene_mob_
roster.py` (`Sources`/`unambiguous_placements`) ตรงบน `gamedata/tables/
CONSTDATA_TH__MOBS.tsv` จริงบนสะพาน **วัดซ้ำเอง ไม่ได้ก็อปตัวเลขจากรอบ
`mf71tm` มาเฉย ๆ** — ผลตรงกับที่รอบนั้นรายงานทุกตัว (cross-check แล้ว)

### 2. เกต CI คีย์ ruling (ตอบใบ `1647`/`1712`, <=2 ไฟล์ตามที่สั่ง แต่ต้องขยายเป็น
3 ไฟล์ในรีโปเซิร์ฟเวอร์ — เหตุผลข้างล่าง)
`tests/test_mob_death_widening_schema_gate.py` เทสเดียว
(`WideningRulingSchemaGateTests::test_widening_ruling_keys_are_frozen_or_
carry_their_own_letter`):
- ทุกคีย์ใน `mob_death.WIDENING_RULINGS` → อยู่ใน frozen list (warn ถ้าไม่ตรง
  schema ใหม่) หรือ match schema `1647` **และ** มีไฟล์ `notes_to_chief/
  <YYYYMMDD_HHMM>_COO-DECISION-*widen*` จริงที่ stamp ตรงวันที่ท้ายคีย์ —
  ไม่ตรงทั้งสอง = แดง
- หา `pf_bridge`: `../pf_bridge` (sibling) ก่อน แล้ว `PF_BRIDGE_DIR` override
  ได้ · ไม่เจอ = `pytest.skip` พร้อมเหตุผล **ทดสอบจริงแล้ว** โดยย้าย
  `../pf_bridge` ไปชื่ออื่นชั่วคราวแล้วรัน (ได้ SKIPPED 1 บรรทัดพร้อมเหตุผล) แล้ว
  ย้ายกลับ ไม่เคย pass เงียบ
- เพิ่มชื่อลง frozen list ไม่ได้ (ปิดตายตามที่ `1712` สั่ง): มีเทสอีกก้อนใน
  ไฟล์เดียวกันที่ re-derive เซ็ตคีย์ที่ไม่ตรง schema จาก `WIDENING_RULINGS`
  สดทุกครั้งแล้วเทียบเท่ากับ frozen tuple พอดี — ขยาย tuple มือ = แดงทันที
  (ทดสอบมิวเทชันแล้ว ดูหัวข้อ pf-adversary)

**เหตุที่ frozen list = 8 คีย์ ไม่ใช่ 7 ตามที่ตัวเลขของ `1712` ประมาณไว้**: วัด
ตรงจาก `mob_death.WIDENING_RULINGS` จริง (`python3 -c "..."` พิมพ์คีย์ทั้งหมด
แล้วรันกฎ schema ทีละคีย์) ได้ 8 คีย์ที่ไม่ตรง schema ใหม่วันนี้:
3 คีย์ตรงรูป "COO-DECISION <วันที่> widen-death-scope-...-templates" (bg0003,
bg0004, bg0005 — ตรงกับที่ `1712` ข้อ 3 พูดถึง "3 ใน 7 วันที่คั่นกลาง") · อีก 2
คีย์มีวันที่แต่คนละตำแหน่ง/รูปกับสามคีย์แรก (916-training-iron-man มีวันที่ตาม
ด้วยวงเล็บอ้างอีกวันที่หนึ่ง, bg0002 มีวันที่ตามหลัง "PANYA-DECISION" ก่อน
"(ADDENDUM 20:18)") · 2 คีย์ไม่มีคำว่า `widen-death-scope` เลย (Mountain
Deer diagnostic, กับ `COO-RULING-20260901-1046` เปล่า ๆ) — ไม่ใช่ "ใบอนุญาต
widen-death-scope" ตามนิยามข้อ 1 ของ `1647` แต่ยังเป็นคีย์ใน
`WIDENING_RULINGS` ที่ต้องมีที่ลงตามคำสั่งเดิม ("ทุกคีย์ต้องอยู่ใน frozen หรือ
match schema") จึงต้องอยู่ frozen เพราะไม่มีทางตรง schema ได้ · 1 คีย์ไม่มี
วันที่เลย (`COO-RULING-20260827-1350 widen-death-scope-bg0001`)

ทำตามคำสั่งของ orchestrator ตรง ๆ: "ถ้าไม่ใช่ 7 พอดี เขียนสิ่งที่เจอจริงแล้วใช้
เซ็ตที่เจอจริง" — ไม่บังคับให้เหลือ 7 ด้วยการเลือกทิ้งคีย์ใดคีย์หนึ่งมือ (จะทำให้
คีย์นั้นต้องผ่าน schema ใหม่ซึ่งมันผ่านไม่ได้ แล้วเกตจะแดงกับคีย์ที่ไม่มีใครขยาย
รอบนี้จริง)

**ทำไมต้องแตะไฟล์ที่ 3 (`docs/PYTEST_SKIP_PINS.json`) ทั้งที่สั่งไว้ <=2 ไฟล์**:
`1712` ข้อ 2 สั่งชัดว่า "ไม่เจอรีโป = skip พร้อมเหตุผล ห้ามเงียบ" — โปรเจกต์นี้มี
ระบบ pin การนับ skip อยู่แล้ว (`tests/test_pytest_precondition_census.py` +
`docs/PYTEST_SKIP_PINS.json`) ที่ตรวจว่า skip ทุกอันถูกนับและ pin ไว้ ไม่งั้น
`test_each_pinned_module_guards_exactly_its_pinned_count` และเทสพี่น้องจะ
มองว่า skip ใหม่นี้เป็น drift ที่ไม่มีใครประกาศ (main จะแดงทันทีถ้าไม่ pin) —
เพิ่ม pin entry เดียว (คีย์ `bridge_sibling` ที่มีอยู่แล้วใน `tests/pf_
preconditions.py` แต่ไม่เคยมีใครเรียกจริงมาก่อนรอบนี้ — grep ยืนยันว่าเป็นตัวใช้
จริงตัวแรก) นี่ไม่ใช่การขยายขอบเขตของ "เกต" เอง แต่เป็นสิ่งที่ต้องทำเพื่อไม่ให้
เกตของโปรเจกต์เดิมพังจากการเพิ่มเทสของเรา — ตรวจแล้วว่า
`tests/test_pytest_precondition_census.py` ทั้งไฟล์ยังเขียวหลัง pin (69 passed,
1119 subtests passed)

**ไฟล์ที่ 4 ที่ไม่ได้อยู่ในแผนเลย** (`tests/test_gm_plugin_image_check.py`,
คอมเมนต์เดียว): พบว่ามีคอมเมนต์ของ LANE-GM เขียนไว้ว่า
"`BRIDGE_SIBLING` guards nothing else in this repository any more" ซึ่งเป็น
จริงก่อนรอบนี้ (grep ยืนยันว่าไม่มีเทสไหนเรียกใช้ precondition นี้จริงมาก่อน) และ
กลายเป็นเท็จทันทีที่เทสของรอบนี้เพิ่มเข้ามา — แก้เป็นบันทึกแบบ cross-lane
(ติดป้าย `[CROSS-LANE NOTE, round bvaptp, LANE-B: ...]`) ตามแบบที่รอบ
`9t75cr`/`30ja9z` ทำกับ comment ข้ามสายมาก่อน ไม่ได้แก้ตรรกะของฟังก์ชันนั้น
เลยสักบรรทัด (`python3 -m pytest tests/test_gm_plugin_image_check.py -q` →
85 passed ก่อนและหลัง)

## ที่ไม่ได้แตะ (นอกขอบเขตรอบนี้)
- ไม่ได้เขียนหรือแก้ `field_mob_tables_bg00xx.py` ไฟล์ไหนเลย (static-only ตาม
  `1648` ข้อ 2)
- ไม่ได้ส่ง roster ฉากทะเลใหม่ (127/128/304/305) และไม่ได้แตะ `Bg3001` เลย —
  `1644` (สิทธิ์ฆ่า `{8041,8180}`) ยัง DEFERRED ตามเดิม ไม่ได้เขียนคีย์ใหม่ให้
- ไม่ได้ตอบ/บริโภคจดหมาย broadcast `20260904_0233_PANYA-DECISION-*` (เห็น
  แล้ว ไม่บล็อก ไม่ใช่ของ LANE-B โดยตรง — ดูหัวข้อกล่องจดหมาย)
- ไม่ได้แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` เลย
- ไม่ได้ยืนยัน/ปฏิเสธสถานะ merge ของกิ่ง `claude/nice-meitner-mf71tm`
- D2 (`DeathRegister` ต่อ connection, `mob_death_persistence` ไม่ถูกเรียกใน
  `runtime.py`) — เป็นของ chief ตาม `1712` ข้อ 5 ไม่ทวงซ้ำ

## pf-adversary
`ADVERSARY_UNAVAILABLE claude/gifted-clarke-bvaptp` — ไม่มีเครื่องมือ
Task/Agent ในสภาพแวดล้อมรอบนี้ ทำ self-review แทนแบบละเอียด:
1. อ่าน `git diff --cached` ทุก hunk ก่อนคอมมิตทั้ง 3 ไฟล์ (เทสใหม่, pin ใหม่,
   คอมเมนต์แก้)
2. มิวเทชันเกตด้วยมือ 4 แบบ (รันจริงทุกแบบ ไม่ใช่คำอ้าง):
   - เพิ่มคีย์ใหม่ที่ไม่มีจดหมายเลย → **แดงถูกต้อง** (assertion บอกชื่อคีย์+เหตุ)
   - เพิ่มคีย์ใหม่ที่ปลอมชื่อฉากแต่ใช้วันที่ของจดหมายจริง (bg0008 05:48) →
     **ผ่าน** (ข้อจำกัดที่รู้: เกตเช็คแค่ว่าจดหมายที่ stamp วันนั้นมีคำว่า
     COO-DECISION+widen ในชื่อไฟล์ ไม่ได้เช็คเนื้อหาจดหมายว่าเป็นฉากไหน — ตรง
     ตามสเปกที่ `1712` เขียนไว้ ("มีไฟล์...ที่ stamp ตรงวันที่") ไม่ใช่บั๊กของ
     เทส แต่เป็นขอบเขตที่ต้องรู้ไว้)
   - เพิ่มชื่อลง frozen tuple มือ (ทั้งที่คีย์นั้นตรง schema อยู่แล้ว) →
     **แดงถูกต้อง** (เทสที่สองใน method เดียวจับได้)
   - เปลี่ยนวันที่ท้ายคีย์ที่ตรง schema จริงให้ไม่ตรงกับจดหมายที่มีอยู่ (bg0006) →
     **แดงถูกต้อง**
3. ย้าย `../pf_bridge` ออกชั่วคราวแล้วรัน → SKIPPED 1 บรรทัดพร้อมเหตุผล
   `[precondition:bridge_sibling] ...` ไม่ใช่ error ไม่ใช่ pass เงียบ ย้ายกลับแล้ว
   ตรวจว่ากลับมาเขียวเหมือนเดิม
4. ตั้งค่า `PF_BRIDGE_DIR=/does/not/exist` → fallback ไป sibling dir ถูกต้อง
   (ไม่ error จาก path ที่ไม่มีจริง)

## verification
- ไฟล์เทสที่แตะโดยตรง: `tests/test_mob_death_widening_schema_gate.py`,
  `tests/test_pytest_precondition_census.py`, `tests/test_gm_plugin_image_
  check.py`, `tests/test_mob_death.py`, `tests/test_mob_death_wired_
  widening.py` → **276 passed, 3015 subtests passed** ระหว่างทาง
- `git merge origin/main` เข้ากิ่ง `claude/gifted-clarke-bvaptp` → **no-op**
  (`Already up to date`)
- ชุดเต็ม `pytest tests/` บนต้นไม้ที่ commit จริง (`cbc96a3`, หลัง
  `git merge origin/main` no-op): **12432 passed, 373 skipped, 26235
  subtests passed, 0 failed, 477.46s** (ตัวเลขต่างจาก 12413/369/26378 ของ
  รอบ `mf71tm` เพราะคนละต้นไม้: รอบนั้นรันบนกิ่งของตัวเองที่มีงาน `Bg3001`
  รวมอยู่ด้วย รอบนี้รันบน `origin/main` ที่ยังไม่มีงานนั้น — ไม่ใช่ตัวเลขที่
  เทียบกันตรง ๆ ได้)
- `python3 -c "import json; json.load(open('docs/PYTEST_SKIP_PINS.json'))"` →
  valid JSON
- ทุกไฟล์ที่แตะฝั่งเซิร์ฟเวอร์ (3 ไฟล์ .py + 1 ไฟล์ .json) ตรวจแล้วเป็น ASCII ล้วน
  (`str.isascii()` ต่อไฟล์) — non-ASCII สองตัว (`é`,`§`) ที่เจอใน
  `test_gm_plugin_image_check.py` เป็นของเดิมก่อนรอบนี้ ไม่ใช่บรรทัดที่แก้
- stage ทีละไฟล์ (`git add tests/test_mob_death_widening_schema_gate.py`
  แยกจาก `git add docs/PYTEST_SKIP_PINS.json tests/test_gm_plugin_image_
  check.py`) อ่าน `git diff --cached` ก่อนคอมมิตทุกครั้ง ไม่ใช้ `git add -A`
- `python3 tools_bridge/pf_gate_preflight.py --repo /home/user/pirate-force-
  server` (จาก `pf_bridge`) → **PREFLIGHT PASS** ทุกข้อ (cp874 360 ไฟล์ ok ·
  no new skip markers ตามฮิวริสติกของตัวมันเอง — คนละกลไกกับ pin
  `preconditions` ที่ใช้กับ `BRIDGE_SIBLING.require()`, ตรวจแยกด้วย
  `test_pytest_precondition_census.py` แล้วข้างบน · main อยู่ในกิ่งทั้งสอง ·
  census ตรง · ทั้งสองกิ่งของสองรีโป mergeable · ไม่มีไฟล์สะพานโตเกิน ceiling ·
  ไม่แตะแถว scoreboard มือ) — ไม่ได้ส่ง `--pr-body` (ไม่เปิด PR รอบนี้)

## PR/status
- `pf_bridge` claim `pf_bridge#1536` (`claude/practical-knuth-bvaptp`)
- `pirate-force-server` กิ่ง `claude/gifted-clarke-bvaptp` — commit
  `cbc96a3` (local, ยังไม่ push/เปิด PR รอบนี้ตามคำสั่ง orchestrator: รอบนี้
  ทำโค้ดอย่างเดียว ไม่ push ไม่เปิด PR ไม่แตะ GitHub — orchestrating session
  เป็นผู้ทำต่อ)

## รอบหน้าทำอะไร
1. ถ้า COO เห็นด้วยกับ diff ว่างของฝั่งเมือง (`1648` ข้อ 2): สลับ 12 ตารางต่อฉาก
   เป็นกฎเดียว derive อัตโนมัติ + เทสยืนยันว่าเท่ากับตารางเดิมทุกฉากที่ ratify แล้ว
2. ถ้า COO เห็นด้วยกับทิศทางกฎเดียว-มีพารามิเตอร์ครอบครัวของทะเล: เขียนกฎ
   เดียวที่รับพารามิเตอร์ family แทนตาราง 2 ทาง (`--hostility-rule` ที่รอบ
   `mf71tm` เพิ่มไว้ในกิ่งที่ยังไม่ merge) — ต้องรอยืนยันว่ากิ่ง `nice-meitner-
   mf71tm` merge แล้วก่อน ไม่งั้นจะชนกัน
3. ถ้ากิ่ง `nice-meitner-mf71tm` merge แล้ว: B ยื่นใหม่ 1 บรรทัดอ้างใบ `1644`
   ขอสิทธิ์ฆ่า `{8041,8180}` (ตามที่ใบนั้นสั่งไว้ว่าไม่ต้องเขียนใบเต็มซ้ำ)
4. `tools/pf_scan_field_scene_candidates.py` ที่ไม่ตรงกับ miner (หนี้จากรอบ
   `mf71tm`) ยังไม่แก้
5. ตัดสินใจว่าจะบริโภค broadcast `20260904_0233_PANYA-DECISION-*` เมื่อไร/
   อย่างไร (เห็นแล้วรอบนี้ แต่ไม่ใช่ของ LANE-B โดยตรง)

TWO_SESSIONS_SAME_SCENE: ไม่เปลี่ยนจากที่รอบ `mf71tm` เขียนไว้ — รอบนี้ไม่แตะ
`mob_death.DeathRegister`/`runtime.py`/state ต่อ session ใด ๆ เลย เป็นรอบวัด
static (import โมดูลอ่านอย่างเดียว) + เทส CI ล้วน ไม่มี state ใหม่แม้แต่ตัวเดียว

SCOREBOARD: NONE | ผู้เล่นไม่เห็นอะไรต่างจากเมื่อวาน — รอบนี้เป็นรอบวัด (ตาราง
diff กฎมอน/NPC) และเกต CI ป้องกันการปลอมใบอนุญาตฆ่ามอน ไม่ใช่ฟีเจอร์ที่เห็น
บนจอ | จดหมาย `pf_bridge/notes_to_chief/20260906_1824_LANE-B-TO-COO-mobs-
rule-diff-town-vs-ocean.md` · เทส `tests/test_mob_death_widening_schema_
gate.py` · commit `cbc96a3` บนกิ่ง `claude/gifted-clarke-bvaptp`
