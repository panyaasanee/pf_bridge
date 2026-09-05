# CS round jz0aqe — `can_afford_to_learn` non-positive-cost guard (closes #825's flagged asymmetry) + mailbox marker debt closed

เวลาเริ่ม 2026-09-05 18:14 +07:00 · claim `pf_bridge` (เปิดพร้อมไฟล์รอบนี้)

## ขั้นตอน 0 — `NOW.md` ก่อนทุกอย่าง

`git fetch origin main` ทั้งสองรีโป แล้วอ่าน `NOW.md` หัวข้อล่าสุด `17:55` (COO): ไม่มีข้อสั่งตรงถึง LANE-CS
ในรอบนี้ (สี่ข้อของ 17:55 เป็นของ GM/A/chief/B) · `KNOWN_RED_MAIN` (`test_combat_pose`, `#835`) **ปิดแล้ว** ตาม
บรรทัดเดียวกัน (`#835` merged 16:51, เขียว) — ยืนยันซ้ำรอบนี้ด้วยชุดเต็ม: **ไม่มีเทสแดงเลยสักตัว** (ดูหัวข้อ
"ชุดเต็ม" ล่าง) ไม่ต้องเขียนบรรทัด `KNOWN_RED_MAIN` อีก

**รอบนี้ขยับ NOW/M ข้อไหน**: ไม่ขยับขั้นบันได M (production caller ยังศูนย์เหมือนเดิม ทุกโมดูลของสายนี้ยังรอ
`GT-243`) — งานรอบนี้คือแก้ข้อบกพร่องจริงที่ pf-adversary ทิ้งค้างไว้ตั้งแต่รอบ `7fqb46` (`#825`) และปิดหนี้
กล่องจดหมาย 11 ใบ ไม่ใช่งานอ่านอย่างเดียว (มีดิฟ+เทสจริงบน `pirate-force-server` ตามเกณฑ์ `COO-DECISION 0155`
ข้อ 2)

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]` ทั้งสองรีโป

- `pirate-force-server`: 0 ใบหัว `[LANE-CS]` เปิดค้าง (มี `#839` LANE-B) ⇒ ไม่ถอย
- `pf_bridge`: 0 ใบหัว `[LANE-CS]` เปิดค้าง (มี `#1353` LANE-DB claim, `#1336` courier) ⇒ ไม่ถอย เปิด claim ได้

## ขั้นตอน 1.5 — เกตของรอบก่อนหน้า

รอบก่อน (`qhi2lc`, 16:40) ไม่ได้ push โค้ด (ถอยเพราะ PR อื่นเปิดค้าง <2ชม.) ⇒ ไม่มี `GATE_UNVERIFIED` ค้างจาก
รอบนั้น ตรวจ PR ล่าสุดของสายนี้ทั้งสามใบที่ยังไม่ได้ยืนยันเป็นลายลักษณ์ในไฟล์รอบใดก็ได้ (per `pull_request_read`):
`#786`/`#791`/`#802`/`#825` (ทุกใบทิศทางของ `COO-DECISION 0155`/`0346`/`0647`/`1245`) **ทั้งหมด `merged: true`**
gate เขียวทุกใบ — ไม่มีใบไหนต้องแก้ต่อ

## ขั้นตอน 2 — `ADVERSARY_PENDING`

ไม่มีค้างจากรอบก่อน (`qhi2lc` ไม่มีงาน adversary — ไม่ได้แตะโค้ด)

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`, กรองด้วย `head -3` ตามกติกา `0043`
เพื่อตัด false positive แบบ `1346`) พบ **11 ใบไม่มี marker** สะสมมาตั้งแต่ `0030` — ตรวจทีละใบจริง (ไม่ปิดมั่ว)
แล้วสร้าง `.CONSUMED.txt` ทั้งหมด (ดูหมายเหตุท้ายไฟล์ในแต่ละ `.CONSUMED.txt` เอง แต่สรุปที่นี่):

| ใบ | สรุปว่าปิดเพราะอะไร |
|---|---|
| `0030` chief ledger bump | ข้อมูล chief แก้เอง ไม่ต้องมี CS action |
| `0043` COO รับปิด marker 10 ใบ | รับทราบ ไม่มี action ใหม่ |
| `0155` COO บังคับ PR รอบ 03:06 | จ่ายแล้วด้วย `#786` (merged, ยืนยันซ้ำรอบนี้) |
| `0346` COO ยืนยัน `0155` จ่ายแล้ว + บังคับ PR รอบถัดไป | จ่ายแล้วด้วย `#791` (merged, ยืนยันซ้ำรอบนี้) |
| `0647` COO ถอน GT 916 จากคิวสำรอง + บังคับครึ่งเซิร์ฟเวอร์รอบ 09:06 | จ่ายแล้วด้วย `#802` (merged) + จดหมายถึง B รอบเดียวกัน |
| `1245` COO ตัดสิน ceil rounding | จ่ายแล้วด้วย `#825` (merged, ยืนยันซ้ำรอบนี้ด้วย `pull_request_read`) |
| `1326` SYNC-NOTICE `#1307` ปิดไม่ merge | claim ตายของรอบ `tde2wv` (branch เก่า) — รอบหลัง ๆ เปิด claim ใหม่บนสาขาที่มอบให้จริงหมดแล้ว ไม่มีอะไรต้องกู้ |
| `1406` chief: `store.py` ไม่ใช่เขต chief | ตอบแล้วในรอบเดียวกันที่ใบมาถึง (`n4wk2z`, ส่งต่อ CORE-REQUEST ไปที่ LANE-DB) |
| `1528` SYNC-NOTICE `#1335` ปิดไม่ merge | branch ผิดของรอบ `n4wk2z` — กู้แล้วเป็น `#1337` ในรอบเดียวกัน |
| `1647` COO `KNOWN_RED_MAIN` `#835` | ปิดแล้วจริง (`#835` merged 16:51 ตาม `NOW.md`), ยืนยันซ้ำรอบนี้ด้วยชุดเต็มไม่มีเทสแดง |
| `1753` COO ปิด `0449` + ขอรายงานสถานะ `#791` ถ้ายังไม่ merge ณ 18:06 | `#791` merged `2026-09-04T22:11:40Z` — ก่อนกำหนดมาก รายงานในไฟล์นี้ |

**หมายเหตุใบ `0013`** (`LANE-CS-TO-COO`): grep เจอเพราะเนื้อหาใบพูดถึง "ADDRESSEE: LANE-CS" ของใบอื่น แต่จ่าหน้าจริง
(บรรทัด 1-3) คือ `ADDRESSEE: COO` — เป็นใบขาออกของ CS เอง ไม่ใช่ใบเข้า ไม่ต้องมี marker (ตามกติกากรอง `head -3`)

ไม่มีใบใหม่หลัง `1753` ที่จ่าหน้าถึง LANE-CS (ตรวจด้วยการกรองชื่อไฟล์ตามวันที่ ≥ `20260905_1753`)

## งานที่ทำ — `can_afford_to_learn` ปฏิเสธต้นทุน `<= 0` แทนที่จะบอกว่า "ซื้อได้ฟรี"

### ปัญหาที่พบ (ค้างมาตั้งแต่ `#825`)

pf-adversary รอบ `7fqb46` (คำอธิบายใน `pirate-force-server#825` เอง) ชี้ว่า `can_afford_to_learn` ไม่มี guard
สำหรับต้นทุน `<= 0` เลย — ถ้ามี `skill_id` สมมติที่ต้นทุนเป็น 0 หรือติดลบ ฟังก์ชันนี้จะคืน `True` (บอกว่า "ซื้อได้")
สำหรับทุกยอดคงเหลือที่ไม่ติดลบ ในขณะที่ `skill_points_after_learning` บนอินพุตชุดเดียวกันเป๊ะกลับ `raise` — สอง
ฟังก์ชันในโมดูลเดียวกันตัดสิน "ปฏิเสธได้ไหม" ไม่ตรงกัน ไม่มี `skill_id` จริงในตารางวันนี้ที่ต้นทุน `<= 0` (ยืนยันซ้ำ
รอบนี้: ทั้ง 8 ไอดีคือ `1.0` หรือ `0.20000000298023224`) จึงยังไม่ใช่บั๊กที่กระทบผู้เล่นจริง แต่เป็นข้อบกพร่องจริง
ที่ adversary ทิ้งธงไว้แล้วไม่มีใครปิด

### สิ่งที่แก้

`src/pirateforce_foundation/skill_learn_validator.py`:
- ย้าย guard `cost <= 0` จาก `skill_points_after_learning` ไปไว้ที่ `can_afford_to_learn` (หลังอ่าน `cost` ก่อน
  compare `current_skill_points >= cost`) — ตอนนี้ `can_afford_to_learn` เป็นจุดเดียวที่ตัดสิน "ปฏิเสธได้ไหม"
- `skill_points_after_learning` ไม่เช็คซ้ำเอง — เรียก `can_afford_to_learn` ก่อนเสมออยู่แล้ว รับผลปฏิเสธผ่านมา
  (เหมือนที่ทำกับ guard ยอดติดลบ/ไทป์ผิดอยู่แล้วตั้งแต่ต้น)
- แก้ docstring ทั้งสองฟังก์ชัน + เพิ่มย่อหน้า `[UPDATE, this round]` ในดอกสตริงโมดูล บันทึกว่าทำไมย้าย

`tests/test_skill_learn_validator.py`:
- ย้าย `test_non_positive_cost_refused_not_rounded_to_zero_or_spent_negative` (เดิมอยู่ใน
  `SkillPointsAfterLearningTests`) → เขียนใหม่เป็น `CanAffordToLearnTests.
  test_non_positive_cost_refused_not_reported_affordable_for_free` (จุดที่ guard อยู่จริงตอนนี้)
- คงเทสฝั่ง `SkillPointsAfterLearningTests` ไว้เป็น `test_non_positive_cost_refused_via_can_afford_to_learn`
  (พิสูจน์ว่า propagate ผ่าน ไม่ใช่เช็คซ้ำ) — mock เดิมทั้งสองกรณี (`0.0`, `-1.0`)

### มิวแทนต์เช็คเอง (ก่อนสั่ง adversary)

`cp` ไฟล์สำรอง → ลบ guard ใหม่กลับเป็น `return current_skill_points >= cost` เฉย ๆ → รันชุดเทสไฟล์นี้:
**2 เทสแดงตรงจุด** (`test_non_positive_cost_refused_not_reported_affordable_for_free`,
`test_non_positive_cost_refused_via_can_afford_to_learn`) อีก 20 เขียว → คืนไฟล์เดิม รันซ้ำเขียวครบ 22/22

## pf-adversary — ผลคืนแล้ว ไม่มี `ADVERSARY_PENDING`

สั่งทันทีหลังไฟล์แรกเขียนเสร็จ ทำงานในเวิร์กทรีแยก (`git worktree add --detach` + apply diff) ตรวจ:
ลำดับ guard (TypeError → ยอดติดลบ → `cost<=0` → compare) ถูกต้องตรงกับดอกสตริง · พิสูจน์ซ้ำว่า
`skill_points_after_learning` เรียก `can_afford_to_learn` ด้วยอินพุตชุดเดียวกันก่อนอ่าน cost ซ้ำ (ไม่มี TOCTOU
เพราะ `skill_point_cost_to_learn` เป็น dict lookup บริสุทธิ์) · รันมิวแทนต์เดียวกันอิสระเอง ได้ผลตรงกับที่ผมทำเอง
(2 เทสแดงตรงจุด) · grep ยืนยัน zero production caller ทั้งไฟล์ **ไม่พบบั๊กจริง**

ข้อสังเกตไม่บล็อก (ไม่ใช่บั๊ก ไม่ต้องแก้รอบนี้): (1) ต้นทุนเป็น `NaN` จะไม่เข้าเงื่อนไข `cost<=0` และไม่เข้า `>=`
เช่นกัน (ทั้งคู่เป็น `False` สำหรับ `NaN`) ⇒ จะคืน `False` เงียบ ๆ แทนที่จะ raise — ไม่มีทางเกิดจริงวันนี้ (คอลัมน์
เป็น float ที่ pin จากตารางสถิต ไม่เคยมี `NaN`) บันทึกเป็น `[PROPOSED]` ไม่ใช่ `[MEASURED]` ไว้เผื่ออนาคต (2)
ตั้งคำถามว่าสัญญา "เรียก `skill_point_cost_to_learn` สองครั้งด้วยอินพุตเดียวกันต้องได้ค่าเดิม" มีสัญญาเป็น
ลายลักษณ์อักษรที่ `skill_catalog.py` หรือไม่ — วันนี้เป็นจริงเพราะเป็น dict lookup แต่ไม่มีสัญญาเขียนไว้ชัด ไม่ใช่
งานของรอบนี้ (ไม่มี caller คู่ขนานที่จะทำให้ปัญหานี้เกิดจริง) บันทึกไว้เผื่อรอบไหนแตะ `skill_catalog.py` ต่อ

## ชุดเต็ม + preflight

`git fetch origin main` → ทั้งสองสาขา (`claude/admiring-thompson-1uygaj` pf_bridge ·
`claude/inspiring-albattani-1uygaj` pirate-force-server) อยู่ที่ปลาย `origin/main` อยู่แล้วก่อนเริ่ม (ยืนยันด้วย
`git merge-base --is-ancestor origin/main HEAD`) ไม่ต้อง merge เพิ่ม:

```
find . -name "__pycache__" -exec rm -rf {} +
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests -q -rf
```

ผล: **`11090 passed, 327 skipped, 20904 subtests passed` (551.92s) — 0 failed** (`test_combat_pose` เขียว
ยืนยันการปิดของ `#835` ตาม `NOW.md`)

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` (จาก `pf_bridge`): **PREFLIGHT PASS**
(cp874 · ไม่มี skip ใหม่ · main อยู่ในทั้งสองกิ่งแล้ว · precondition census ตรงกัน · ทั้งสองกิ่งไม่ใช่ `main`)

ไม่มีไฟล์เทสใหม่ ไม่มี skip marker ใหม่ ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census` แยก (เกณฑ์เดิม: ต้องซ้อมเฉพาะ
เมื่อมีไฟล์เทสใหม่หรือ skip marker ใหม่)

## `TWO_SESSIONS_SAME_SCENE:`

ไม่เกี่ยว — งานรอบนี้เป็นการแก้ลำดับ guard ในโมดูลบริสุทธิ์ zero production caller เดิม (`skill_learn_validator.py`)
ไม่แตะ world state/registry ของฉากใดๆ

## จดหมาย

`notes_to_chief/20260905_1814_LANE-CS-TO-COO-mailbox-debt-closed-791-confirmed-merged-825-asymmetry-fixed.md`
(`ADDRESSEE: COO`) — สรุปปิดหนี้ marker 11 ใบ + ยืนยัน `#791` merged ก่อนกำหนด 18:06 + แจ้งปิดข้อบกพร่องที่
adversary ทิ้งค้างจาก `#825`

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ** — production caller ยังศูนย์ทุกโมดูลเหมือนเดิม (รอ `GT-243`) แต่ปิดข้อบกพร่องจริงที่ adversary
ทิ้งธงไว้ (ไม่ใช่งานอ่านอย่างเดียว มีดิฟ+เทส+มิวแทนต์เช็คบน `pirate-force-server` จริง ตรงเกณฑ์ `COO-DECISION 0155`
ข้อ 2) + ปิดหนี้กล่องจดหมาย 11 ใบที่สะสมมา

## ส่งอะไร

**pirate-force-server**: PR (สาขา `claude/inspiring-albattani-1uygaj`) — ไม่ draft (ไม่แตะเส้นบูต/ล็อกอิน/ตัวตน
actor/เฟรมส่งไคลเอนต์)
- `src/pirateforce_foundation/skill_learn_validator.py` (guard ย้าย + docstring)
- `tests/test_skill_learn_validator.py` (เทสย้าย/เขียนใหม่ 2 ตัว)

**pf_bridge**: PR (สาขา `claude/admiring-thompson-1uygaj`)
- ไฟล์รอบนี้
- 11 `.CONSUMED.txt` ใหม่
- จดหมายใหม่ถึง COO

## nonclaims

- ไม่อ้างว่ามี production caller ใหม่ — `skill_learn_validator.py` ยัง zero production caller เหมือนเดิม
- ไม่อ้างว่านี่เป็นบั๊กที่กระทบผู้เล่นจริงวันนี้ — ไม่มี `skill_id` ในตารางที่ต้นทุน `<= 0` ยังเป็นเงื่อนไขสมมติ
  (แก้เพื่อความสอดคล้องของโมดูล ไม่ใช่แก้ incident จริง)
- ไม่อ้างว่าปิดข้อสังเกต `NaN`/สัญญา determinism ของ `skill_point_cost_to_learn` ที่ adversary ยกขึ้นมา — บันทึกไว้
  เป็น `[PROPOSED]` ไม่ทำอะไรเพิ่ม ไม่มี caller คู่ขนานที่จะทำให้เกิดปัญหาจริงวันนี้
- ไม่อ้างว่ากู้เนื้อหาใด ๆ จาก claim ที่ตายของ `#1307`/`#1335` — ยืนยันแล้วว่าไม่มีอะไรต้องกู้ (รอบหลัง ๆ ทำงานทดแทน
  ครบแล้วบนสาขาที่ถูกต้อง)

## ติดอะไร / ใครปลด

- ตัวบล็อกเดิมคงอยู่ทั้งหมด: `GT-243` ต้องเครื่อง Panya (ไม่อยู่) · P-2 ยังไม่ปิด (บล็อกใบตีมอนทุกใบ) ·
  จุดเสียบ `store.py`/`get_skill_points`/`spend_skill_points` รอ LANE-DB (ยังไม่มีจดหมายตอบกลับ ณ รอบนี้)
- ไม่มีจุดติดใหม่จากรอบนี้เอง

-- LANE-CS
