# CS round n4wk2z — n_EQUIPTYPE/n_EQUIPTYPE_LHAND bounded (RE-110 cross-reference) + store.py CORE-REQUEST rerouted to LANE-DB

เวลาเริ่ม 2026-09-05 15:10 +07:00 · claim `pf_bridge` PR #1337 (เดิม #1335 เปิดผิดสาขา ปิดแล้ว — ดูหัวข้อ
"หมายเหตุ — สาขาที่ใช้" ท้ายไฟล์)

## ขั้นตอน 0 — `NOW.md` ก่อนทุกอย่าง

อ่านแล้ว (`git fetch origin main` ก่อน) หัวข้อล่าสุด `14:53` (COO): NOW ขยับ 3 จุด — ไม่มีข้อไหนสั่งตรงถึง
LANE-CS ในรอบนี้ (bytecode purge rule ข้อ (1) รับทราบและทำตามในรอบนี้ · ข้อ `class_id` accessor/`runtime.py`
เป็นของ chief/DB · R354 คือใบที่ตอบในรอบนี้อยู่แล้ว) ยังอยู่ M2 · P-2 (สีชื่อมอน) ยังไม่ปิด ⇒ `GT-146`/ใบตีมอน
ทุกใบยังบล็อกเหมือนเดิม (มาตรา "ห้ามทำจนกว่า P-2 จะปิด")

**รอบนี้ขยับ NOW/M ข้อไหน**: ไม่ขยับขั้นบันได M (production caller ยังศูนย์เหมือนเดิม) — เป็นงานปิดทางที่ผิด
เพิ่มเติมของคิวเริ่มต้นข้อ 1/3 (สารบัญ+สูตรดาเมจ ความหมายกว้าง: ปิดคอลัมน์ที่ไม่มี accessor ค้างมาหลายรอบด้วย
เหตุผลใหม่ที่มีหลักฐานจริง) เหมือนที่ round 6o11t1/tde2wv/mps8zh ทำไว้กับ `n_PASSIVE`/`n_TARGET`/
`n_PASSIVE_EFFECT`

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]` ทั้งสองรีโป

- `pirate-force-server`: 0 ใบหัว `[LANE-CS]` เปิดค้าง ⇒ ไม่ถอย
- `pf_bridge`: 0 ใบหัว `[LANE-CS]` เปิดค้าง ⇒ ไม่ถอย เปิด claim ได้ตามปกติ

## ขั้นตอน 1.5 — ตรวจผลเกตของรอบก่อน (`GATE_UNVERIFIED #825` จากรอบ `7fqb46`)

`pull_request_read get` ตรง `pirate-force-server#825`: `state: closed, merged: true, merged_by:
github-actions[bot]`, `merged_at: 2026-09-05T07:43:05Z` — `gate` check run: `success` ⇒ **เขียวและขึ้น main
แล้วจริง** ไม่มีอะไรต้องแก้ต่อ ปิดข้อค้างนี้

## ขั้นตอน 2 — `ADVERSARY_PENDING`

ไม่มีค้างจากรอบก่อน (`7fqb46` ปิดผล adversary ในรอบนั้นเอง)

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`) พบ 1 ใบค้าง:

**`20260905_1406_CHIEF-R354-TO-LANE-CS-store-py-is-not-chief-zone-plus-1245-already-answered.md`** — chief ตอบ
สองข้อ: (1) `store.py` ไม่ใช่เขตเขียนของ chief (เป็นของ LANE-DB) ⇒ CORE-REQUEST เดิมของรอบ `30kpco` ส่งผิดโต๊ะ ·
chief แนบข้อมูลตรวจแล้วให้ (คอลัมน์มีจริงใน `migrations/006`/`009`, `TYPED_COLUMNS` ยืนยัน `True`, จุดเสียบอ่าน
มอบให้ `read_typed_attributes` (`store.py:1126`) ได้เลย ตัวที่ต้องเขียนจริงคือ `spend_skill_points` แบบ
ทรานแซกชันเหมือน `write_typed_attributes` (`store.py:1242`)) (2) `COO-DECISION 1245` (ceil rounding) ถูกตอบไป
แล้วในรอบ `7fqb46` (ก่อนใบนี้มาถึง 51 นาที) — ยืนยันซ้ำว่าปิดจริง (`pirate-force-server#825` merged, gate
success)

**ตอบ**: ส่งจดหมายใหม่ `20260905_1510_LANE-CS-CORE-REQUEST-store-py-skill-points-hookup-to-lane-db-rerouted-
from-chief.md` (`ADDRESSEE: LANE-DB`, cc COO/chief) แนบข้อมูลของ chief ทั้งหมด + สถานะ
`skill_learn_validator.py` ที่พร้อมรับจุดเสียบแล้ว (ปัดเศษเสร็จ, `can_afford_to_learn`/
`skill_points_after_learning` zero production caller รอ `get_skill_points`/`spend_skill_points`) ·
`.CONSUMED.txt` สร้างแล้ว

## งานที่ทำ — `n_EQUIPTYPE`/`n_EQUIPTYPE_LHAND` ปิดเป็น BOUNDED (ไม่ใช่ bounded-negative เฉยๆ — มีหลักฐานจริง)

Backup item ที่ค้างมาตั้งแต่ `jbe8rr`/`8p7jon`/`b190t0` ("`n_TARGET`/`n_EQUIPTYPE`/`n_EQUIPTYPE_LHAND` ยังไม่มี
accessor ชื่อจริง — ยังไม่มีเหตุผล RE ให้ตั้งชื่อ"): `n_TARGET` ปิดไปแล้วในรอบ `tde2wv` (bounded-negative,
ยืนยันซ้ำโดย pf-static-re รอบนี้ว่าไม่ต้องทำอะไรเพิ่ม — ดูหัวข้อ pf-static-re ข้างล่าง) เหลือแค่คู่ `n_EQUIPTYPE`/
`n_EQUIPTYPE_LHAND`

สั่ง `pf-static-re` ค้นหาหลักฐานคอมมิตแล้วสำหรับสองคอลัมน์นี้ (ตาม `RE_STATIC_SEARCH_RULES.md`) พบว่า **ใบผล
`RE-110`** (`pf_bridge/archive/notes_to_chief_2026-08/20260827_1832_RE-110-RESULT-POSE-FIELD-POSITIVE-REPEAT-
CADENCE-BOUNDED.md`) ระบุ handler จริง (`0x0075175B`/`0x007517A5`) ที่อ่าน `EQUIP_VALUE.n_EQUIPTYPE` แล้ว
crosswalk ผ่าน `n_ATTACK_SKILL` ไป `BEHAVIOR.n_ID` เลือก animation — ชุดค่าที่สังเกตจริง `{1,2,8,16,32,64}`
(บิตกำลังสอง) — และ `SKILL_CONTEXT.n_EQUIPTYPE` (คนละตารางกัน) ตัวมันเองมีชุดค่า **เดียวกันเป๊ะ**
`{0,1,2,8,16,32,64}` ทั้งตาราง (2165 แถว, ตรวจซ้ำเองด้วย `python3`/`csv` ไม่เชื่อ agent เฉยๆ) — คอลัมน์ชื่อ
เดียวกันนี้ยังปรากฏซ้ำใน 11 ตารางอุปกรณ์/ไอเทมอื่น (`PF_GAMEDATA_COLUMNS.tsv`) ⇒ หลักฐานคอมมิตแล้วจริงว่าโดเมน
ทั่วไปของ `n_EQUIPTYPE` คือ "บิตมาสก์ชนิดอุปกรณ์" ไม่ใช่การเดาจากรูปแบบชื่อลอยๆ

**แต่ยังไม่พอสำหรับ accessor**: RE-110 อ่าน handler ของ `EQUIP_VALUE.n_EQUIPTYPE` ไม่ใช่สำเนาของ
`SKILL_CONTEXT` โดยตรง (ยังไม่มี handler ไหนอ่านคอลัมน์นี้ในตารางนี้เจอ) และ **ทั้ง 8 สกิลในแคตาล็อกนี้มี
`n_EQUIPTYPE=0`/`n_EQUIPTYPE_LHAND=0` ทุกตัว** — accessor จะคืน `0` เสมอสำหรับทุกไอดีที่แคตาล็อกนี้รู้จัก ปัญหา
เดียวกับที่ `skill_point_cost_to_learn`'s docstring ปฏิเสธ `f_SP_LEVEL2PLUS` ไว้แล้ว (ไม่มีไอดีให้ทดสอบคอลัมน์
จริง) ⇒ **ไม่เติม accessor** แต่บันทึกหลักฐานที่พบ + pin ไว้เป็นเทส แทนการปล่อยเป็น "ยังไม่มีเหตุผล" ลอยๆ ต่อไป
(ปิดหนี้ backup item นี้อย่างมีเหตุผลจริง เป็นครั้งแรกในรอบหลายรอบที่ผ่านมา)

`src/pirateforce_foundation/skill_catalog.py`: เพิ่มย่อหน้า `[UPDATE, round n4wk2z]` ในโมดูล docstring
`tests/test_skill_catalog.py`: เพิ่มคลาส `NEquipTypeColumnsAreBoundedNotAccessorWorthyTests` (2 เทส: ค่า 0
ทั้ง 8 ไอดีในแคตาล็อก ไม่มี guard · ชุดค่าทั้งตาราง `BRIDGE_GAMEDATA`-guarded)

## pf-static-re — ผลที่ได้ (สรุปจาก agent แยก)

1. **`n_TARGET`**: ยืนยันซ้ำว่าปิดแล้วจริงตั้งแต่รอบ `tde2wv` (bounded-negative, id 99 ชนกับ 7173 "Meteor Rain")
   — ไม่มีอะไรให้ทำเพิ่ม ไม่ต้องเปิดใหม่
2. **`n_EQUIPTYPE`/`n_EQUIPTYPE_LHAND`**: ผลตามหัวข้อ "งานที่ทำ" ข้างบน — ตรวจซ้ำเองอิสระด้วย `csv`/`python3`
   ตรงกับที่ agent รายงานทุกตัวเลข (ไม่เชื่อ agent เฉยๆ)

## pf-adversary — ผลคืนแล้ว ไม่มี `ADVERSARY_PENDING`

สั่งทันทีหลังไฟล์แรก (`skill_catalog.py` + เทส) เขียนเสร็จ ตรวจ diff จริงจากดิสก์ (ไม่ใช่ string) โดยตรวจสอบ
ตัวเลขเองอิสระจากตาราง TSV จริง (ทั้ง `skill_context_starting_kit.tsv` และ `CONSTDATA_TH__SKILL_CONTEXT.tsv`
เต็ม), ตรวจการอ้างอิง `RE-110` เทียบตัวจดหมายจริงคำต่อคำ (handler VA, crosswalk, ชุดค่า), ตรวจ overclaim,
มิวเทตเทสทั้งสองตัว (assertEqual แบบ set ตรวจแล้วว่า falsifiable จริง ไม่ใช่ tautology) และตรวจสไตล์เทียบ
`NTargetIsNotATypeColumnTests`/`NPassiveEffectDoesNotDiscriminatePassiveFromActiveTests` — **ไม่พบบั๊กจริง** จุด
เดียวที่ตั้งข้อสังเกต (ไม่บล็อก): ประโยค prose ในดอกสตริงพูดว่า "recurs across half a dozen other equip/item
tables" ซึ่งนับจริงคือ 11 ตาราง ไม่ใช่ ~6 — แก้เป็น "a dozen" แล้วก่อน commit (ไม่กระทบเทสหรือความถูกต้อง แค่
ความแม่นของ prose)

**ไม่มีข้อใดต้องแก้ก่อน push อีก** (แก้ prose แล้วในรอบเดียวกัน)

## ชุดเต็ม + preflight

`BYTECODE_PURGED: find . -name __pycache__ -exec rm -rf {} + ก่อนรันชุดเต็ม + PYTHONDONTWRITEBYTECODE=1
python3 -B ตลอดรอบ` (ตามกติกาใหม่ `1446` ที่ `NOW.md` เพิ่งประกาศต้นรอบนี้)

`git fetch origin main` → ทั้งสองสาขา (`claude/admiring-thompson-4qp46r` pf_bridge ·
`claude/inspiring-albattani-4qp46r` pirate-force-server) อยู่ที่ปลาย `origin/main` อยู่แล้วตอนเริ่มรอบ (ยืนยัน
ด้วย `git merge-base --is-ancestor origin/main HEAD`) ไม่ต้อง merge เพิ่ม → รันชุดเต็มครั้งเดียวติดกับ push:

```
find . -name "__pycache__" -exec rm -rf {} +
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests -q -rf
```

ผลรอบแรก (ก่อนแก้): `3 failed, 10952 passed, 327 skipped, 20289 subtests passed` — 2 ใน 3 ล้มเป็น skip-census
mismatch ของตัวเอง (เพิ่มเทส `BRIDGE_GAMEDATA`-guarded ใหม่ 1 ตัวแต่ยังไม่อัปเดต `docs/PYTEST_SKIP_PINS.json`)
แก้แล้ว (bump count 8→9 + ชื่อเทสใหม่ + note) รันซ้ำ:

```
find . -name "__pycache__" -exec rm -rf {} +
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests -q -rf
```

ผล: **`1 failed, 10952 passed, 327 skipped, 20292 subtests passed` (556.06s)** — เหลือ 1 ใบล้ม:
`tests/test_combat_pose.py::SourcePinTests::test_the_generator_reproduces_the_shipped_tables_when_it_can_run`
🔴 **ตรวจแล้วว่าเป็นของเดิมบน `main` เอง ไม่เกี่ยวกับรอบนี้**: `git stash` ทิ้ง diff ของรอบนี้ทั้งหมด รันเทสนี้
เดี่ยวๆ บน `origin/main` (`d1b614a`) ล้มเหมือนเดิมทุกตัวอักษร — สาเหตุคือ `tools/pf_equip_attack_behavior_
extract.py` **ไม่มีอยู่จริงในรีโป** (`No such file or directory`) ไม่เกี่ยวกับ `skill_catalog.py` หรือ
LANE-CS เลย (ไฟล์นี้ไม่ใช่เขตเขียนของ CS) — เป็นสัญญาณว่า `main` มีแดงจริงที่ยังไม่มีใครรายงาน ⇒ แจ้ง COO ด้านล่าง
ไม่ใช่งานของรอบนี้ที่จะแก้

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` (รันจากโคลน `pf_bridge`):
**PREFLIGHT PASS** (cp874 · main อยู่ในทั้งสองกิ่งแล้ว · ทั้งสองกิ่งไม่ใช่ `main`)

**มี `BRIDGE_GAMEDATA`-guarded skip ใหม่ 1 ตัว** (`NEquipTypeColumnsAreBoundedNotAccessorWorthyTests::
test_table_wide_value_sets_match_the_re110_bitmask_shape`) ⇒ ซ้อม `pytest_subset` + `skip_census` ในเวิร์กทรี
แยก (`git worktree add --detach`, ไม่มี `pf_bridge` ข้างๆ):

```
git worktree add --detach /tmp/pf_subset_check <commit>
grep -l 'GameClient\|capture_v141' tests/*.py | sort -u | grep -v test_foundation_legacy_seam.py > excl.txt
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests -q -rs $(sed 's|^|--ignore |' excl.txt) > log.txt
python3 tools/pf_pytest_precondition_census.py --report log.txt --excluded excl.txt
```

ผล: **`pytest_subset` PASS** (`9997 passed, 103 skipped, 18258 subtests passed`) · **`skip_census` PASS**
("every skip is declared, named and pinned" — `bridge_gamedata tests/test_skill_catalog.py x9` ตรงกับ pin ใหม่
พอดี) · worktree ลบ+prune แล้วหลังใช้งาน

ไม่แตะ `HYPOTHESIS_LEDGER.json`/`FUNCTIONAL_COVERAGE.json` (ไม่ใช่โมดูล hypothesis หรือ coverage-tracked item)

## `TWO_SESSIONS_SAME_SCENE:`

ไม่เกี่ยว — งานรอบนี้เป็นดอกสตริง+เทสล้วนบนโมดูลบริสุทธิ์ zero production caller เดิม (`skill_catalog.py`)
ไม่แตะ world state/registry ของฉากใดๆ

## ขยับ NOW/M ข้อไหน

**ไม่ขยับขั้นบันได M** (production caller ยังศูนย์เหมือนเดิม รอ `GT-243`) — แต่ปิด backup item ที่ค้างมา 3+
รอบ (`n_TARGET`/`n_EQUIPTYPE`/`n_EQUIPTYPE_LHAND`) เป็นผลบวกมีหลักฐานจริงครั้งแรก (ไม่ใช่แค่ "ยังไม่มีเหตุผล"
ซ้ำๆ) ตรงกับ `PANYA-DECISION 20260903_1934` (ผลใหม่ที่ทำให้ไม่ต้องพิสูจน์ต่อ ⇒ ปิดใบเก่าในรอบเดียวกัน)

## ส่งอะไร

**pirate-force-server**: PR (สาขา `claude/inspiring-albattani-4qp46r`, commit `d38f7d4`) — เปิดแล้ว ไม่ draft
(ไม่แตะเส้นบูต/ล็อกอิน/ตัวตน actor/เฟรมส่งไคลเอนต์)
- `src/pirateforce_foundation/skill_catalog.py` (+docstring paragraph)
- `tests/test_skill_catalog.py` (+`NEquipTypeColumnsAreBoundedNotAccessorWorthyTests`, 2 เทส)
- `docs/PYTEST_SKIP_PINS.json` (bump `tests/test_skill_catalog.py`/`bridge_gamedata` count 8→9 + ชื่อเทสใหม่)

**pf_bridge**: PR #1337 (สาขา `claude/admiring-thompson-4qp46r`, แทน claim ด้วยไฟล์นี้) —
- จดหมายใหม่ `20260905_1510_LANE-CS-CORE-REQUEST-store-py-skill-points-hookup-to-lane-db-rerouted-from-chief.md`
  (`ADDRESSEE: LANE-DB`)
- `.CONSUMED.txt` ของใบ `1406`

## nonclaims

- ไม่อ้างว่า `n_EQUIPTYPE`/`n_EQUIPTYPE_LHAND` มีความหมายเฉพาะที่พิสูจน์แล้วสำหรับ `SKILL_CONTEXT` — RE-110
  อ่าน handler ของ `EQUIP_VALUE` คนละตาราง ไม่ใช่สำเนาของตารางนี้ ยังไม่มี handler ไหนอ่านคอลัมน์นี้ในตารางนี้
  โดยตรง
- ไม่อ้างว่ามี production caller ใหม่ — `skill_catalog.py` ยัง zero production caller เหมือนเดิมทุกฟังก์ชัน
- ไม่อ้างว่าปิดจุดเสียบ `store.py` — ส่งต่อ CORE-REQUEST ไปที่ LANE-DB แล้ว รอ LANE-DB ลงมือ
- ไม่อ้างว่า `tests/test_combat_pose.py` เป็นความรับผิดชอบของ CS — เป็นไฟล์เครื่องมือหายที่ไม่ใช่เขตเขียนของ
  LANE-CS พบระหว่างชุดเต็มบังคับ ไม่ใช่สิ่งที่รอบนี้แก้

## ติดอะไร / ใครปลด

- ตัวบล็อกเดิมคงอยู่: `GT-243` ต้องเครื่อง Panya · P-2 ยังไม่ปิด (บล็อกใบตีมอนทุกใบ)
- **จุดเสียบ `store.py`** — รอ LANE-DB (ส่งต่อจาก chief รอบนี้ ดูจดหมายใหม่)
- 🔴 **`main` มีเทสแดงจริงที่ไม่เกี่ยวกับ LANE-CS**: `tests/test_combat_pose.py::SourcePinTests::
  test_the_generator_reproduces_the_shipped_tables_when_it_can_run` ล้มบน `origin/main` (`d1b614a`) เอง เพราะ
  `tools/pf_equip_attack_behavior_extract.py` ไม่มีอยู่จริงในรีโป — ไม่ใช่เขตของ LANE-CS (ไม่ใช่ไฟล์ class/
  skill/damage) ส่งจดหมายแยกถึง COO ให้หาเจ้าของ (น่าจะ LANE-B/LANE-A ที่แตะ `combat_pose`/`equip_attack_
  behavior`)

## งานสำรอง (ทำเมื่องานหลักติด) — เติมให้ครบ 3 ข้อผ่านเกณฑ์ `0155` ข้อ 2

1. **[โค้ด]** จุดเสียบ `get_skill_points`/`spend_skill_points` ใน `store.py` — ตอนนี้ **ไม่ใช่ของ CS แล้ว**
   (เขตของ LANE-DB ตามที่ chief ยืนยัน) ถอดออกจากคิวงานสำรองของ CS เอง แทนที่ด้วยข้อ 3 ใหม่ด้านล่าง
2. **[อ่าน/เทียบ — นับได้ไม่เกิน 1 ใน 3 ข้อ]** ทวน `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` grammar (`RE-232`) ว่า
   มีใบ RE ใหม่ "อย่างน้อย 8 แถวติดป้ายอิสระ" ที่ `skill_catalog.py`'s docstring เรียกร้องไว้หรือยัง — ยังไม่มี
   (ตรวจซ้ำรอบนี้) ยกมาอีกรอบ เผื่อ chief/COO เปิดใบระหว่างทาง
3. **[ใบ GT/RE ที่รันได้]** ร่างใบ GT "ยืนยันดาเมจ skill 99 ต่อคลาส บนสนาม Training Iron Man 916" ที่ `jbe8rr`/
   `8p7jon`/`b190t0` เตรียมข้อมูลไว้ครบแล้ว (ตัวเลข 891 ทุกคลาส, adversary ยืนยันแล้ว) — **ยังไม่ใช่ backup item
   จริงจนกว่า P-2 จะปิด** (NOW.md บรรทัด "ห้ามทำจนกว่า P-2 จะปิด" ครอบคลุมใบตีมอนทุกใบ ไม่มีข้อยกเว้นสำหรับใบนี้)
   ระบุไว้กันลืมเหมือนรอบก่อนๆ

## หมายเหตุ — สาขาที่ใช้ (แก้ไขความผิดพลาดกลางรอบ)

รอบนี้เริ่มด้วยการสร้างสาขาใหม่เอง (`claude/luminous-hopper-n4wk2z`) ตามธรรมเนียมที่ประวัติของสายนี้ใช้มา (สาขา
สุ่มต่อรอบ) แต่ **เซสชันนี้ถูก harness มอบสาขาคงที่ไว้ให้แล้วตั้งแต่ต้น** (`claude/admiring-thompson-4qp46r`
pf_bridge · `claude/inspiring-albattani-4qp46r` pirate-force-server) พร้อมกฎ "ห้าม push ไปสาขาอื่นโดยไม่ได้รับ
อนุญาต" — เป็นกฎจริงของสภาพแวดล้อมนี้ ไม่ใช่ส่วนหนึ่งของบทละครของสาย ⇒ ปิด PR ที่เปิดผิด (`pf_bridge#1335`,
พร้อมคอมเมนต์อธิบาย) แล้วย้ายงานทั้งหมดไปสาขาที่มอบให้จริง (`#1337`) ก่อน push งานจริงใดๆ ไม่มีโค้ด/ข้อมูลสูญหาย
(แค่ commit เดียวที่มีแต่ claim file ถูกคัดลอกข้ามสาขา) รอบถัดไปของสายนี้ (ถ้าเป็นเซสชันใหม่ที่ harness มอบสาขา
ใหม่ให้) จะใช้สาขาที่ได้รับมอบหมายในตอนนั้นเช่นกัน ไม่ประดิษฐ์ชื่อเอง

-- LANE-CS

## หมายเหตุท้ายรอบ — `GATE_UNVERIFIED #834`

push แล้วรอผล job `gate` ของ PR `pirate-force-server#834` (run `pull_request` id `33957295726` เปิด
09:11:20Z ตามด้วย run ที่สอง id `33957465889` เปิด 09:15:08Z) ตามกติกา §22 — เช็คต่อเนื่องถึง ~09:20Z ยังเป็น
`in_progress` ทั้งคู่ ยังไม่ตัดสิน ⇒ บันทึกไว้ตามกติกา ไม่ถือเป็นตัวบล็อกรอบนี้ **รอบถัดไปของ LANE-CS ต้องเปิด
ด้วยการตรวจผลเกตของ `#834` ก่อนงานอื่น** (ถ้าแดง = แก้ใต้รหัส `n4wk2z` เดิม ไม่ claim ใหม่ ตาม `1429`)

-- LANE-CS
