# CS round jbe8rr — server PR ตาม `COO-DECISION 20260905_0155` (สูตรดาเมจฝั่งเซิร์ฟเวอร์ + skill point)

เวลาเริ่ม 2026-09-05 03:12 +07:00 · claim `pf_bridge` PR #1248 (หัว `[LANE-CS] round jbe8rr: claim` เดิม ทับด้วยไฟล์นี้)

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]`

`pirate-force-server` open ก่อนเริ่ม: #783 (`[LANE-DB]`) — ไม่มี `[LANE-CS]` · `pf_bridge` open ก่อนเริ่ม:
#1243 (`[LANE-DB]`) · #1245 (`[LANE-GM]`) · #1246 (`[LANE-B]`) · #1247 (`[LANE-A]`) — ไม่มี `[LANE-CS]` ⇒ ไม่ถอย
เปิด claim ได้ตามปกติ

## ขั้นตอน 2 — `ADVERSARY_PENDING`

ไม่มีค้างจากรอบก่อน (`9emwkk` ยืนยันแล้วว่า `h4mxrq` ปิด `#768` เต็มในรอบนั้นเอง ไม่มีอะไรค้างข้ามมาให้ CS)

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`) เจอ 2 ใบ:

1. `20260905_0013_LANE-CS-TO-COO-...md` — **false positive** (จ่าหน้าจริงคือ `ถึง: COO`/`ADDRESSEE: COO`, เป็นจดหมาย
   ของ CS เองส่งออกรอบ `h4mxrq`; grep เจอเพราะเนื้อในอ้างคำว่า "LANE-CS" ตอนอธิบายใบ `1346` — เหมือนที่ระบุไว้ใน
   ตัวใบเองแล้วว่าเป็น false positive ซ้ำแบบเดียวกับ `1346`) ⇒ ไม่ใช่คำสั่งถึง CS ไม่ต้องตอบ/ไม่ปิดมาร์กเกอร์
2. `20260905_0155_COO-DECISION-...-server-pr-due-0306-LANE-CS.md` — **ใบจริงจ่าหน้าถึง LANE-CS** ตัดสิน 3 ข้อ:
   (1) คิวงานสำรองของ `9emwkk` ไม่นับ (2) เกณฑ์ใหม่ของงานสำรองที่นับ (3) สั่งให้เปิด PR เซิร์ฟเวอร์รอบ **03:06**
   จาก 5 ทิศทางที่อนุมัติ ตกกำหนด 04:36 = escalation ⇒ **นี่คืองานหลักของรอบนี้** ตอบด้วยไฟล์รอบนี้ทั้งฉบับ +
   `.CONSUMED.txt`

## งานที่ทำ — server PR จากทิศทางที่ `0155` อนุมัติ (เลือก 2 จาก 5: สูตรดาเมจฝั่งเซิร์ฟเวอร์ + ระบบสกิลพอยต์)

### 1) `src/pirateforce_foundation/damage_by_class_skill.py` (ใหม่)

ทิศทาง "สูตรดาเมจฝั่งเซิร์ฟเวอร์" ของ `0155`: "เขียน resolver ที่รับ (class, skill id, ..., ตาราง SKILL ที่ pin)
คืนตัวเลข ... ห้ามคอนสแตนต์" — `damage_by_skill.resolve_skill_damage(skill_id, attacker, defender)` (มีอยู่แล้ว
ตั้งแต่รอบ `ltahoi`) ยังไม่มีอาร์กิวเมนต์ `class` เลย จึงไม่เคยเช็คว่าคลาสนี้ถือสกิลนี้จริงไหมก่อนคำนวณดาเมจ —
ช่องว่างจริงที่ยังไม่เคยมีใครปิด (ตรวจซ้ำรอบนี้: `grep -n "class_id" src/pirateforce_foundation/damage_by_skill.py`
= 0 hit) `resolve_class_skill_damage(class_id, skill_id, attacker, defender)` เติมเกตนี้:

- เช็ค `skill_id in class_catalog.starting_skill_ids(class_id)` ก่อนเสมอ (ไม่มีตารางคลาส→สกิลของตัวเอง — เรียก
  `class_catalog` ทุกครั้ง พิสูจน์ด้วยเทส mock ว่าถ้าตาราง class_catalog ตอบอื่น ผลลัพธ์ตามไปด้วย)
- ผ่านแล้วส่งต่อ `damage_by_skill.resolve_skill_damage` เดิม (re-export `resolve_damage`/`Combatant` จาก
  `damage_by_skill` ด้วย `is` เหมือนที่ไฟล์นั้น re-export จาก `mob_combat` — ไม่มีสำเนาสูตรที่ 4)
- ไม่มีคอนสแตนต์ตัวเลขใหม่ — ทุกไอดีที่อ่านมาจาก `class_catalog`/`skill_catalog` ที่ pin ไว้แล้ว
- **zero production callers เหมือน `damage_by_skill.py` เดิมทุกประการ** (`grep -rln
  "damage_by_class_skill" src tests` รอบนี้ = มีแค่ไฟล์เทสของตัวเอง)

`tests/test_damage_by_class_skill.py` (ใหม่, 9 เทส): พิสูจน์ตัวตนสูตร/Combatant ตรงกับ `damage_by_skill` · เช็ค
ว่าไม่มีตาราง class→skill ของตัวเอง (mock `class_catalog.starting_skill_ids`) · **derive จากตารางจริงล้วน ไม่พิมพ์
คู่ class/skill มือ**: ไล่ทั้ง 5 คลาสจริงจาก `class_catalog.CLASS_IDS`, หา "Basic Training" id ของแต่ละคลาส (ตัวที่
ไม่ใช่ 99/110/111) แล้วยืนยันว่า id นั้นถูกปฏิเสธเมื่อลองกับอีก 4 คลาสที่เหลือ (20 คู่ไขว้) · เทส skill 99 คืนตัวเลข
เดียวกับ `damage_by_skill.resolve_skill_damage` ทุกคลาส · เทส refusal ของสกิลที่รู้จักแต่ยังไม่ classify (110)
propagate ผ่านมาเป็น `DamageByClassSkillError` โดยไม่กลืนข้อความเดิม · เทส class id/skill id ที่ไม่รู้จักเลย

### 2) `src/pirateforce_foundation/skill_catalog.py` (แก้)

ทิศทาง "ระบบเรียนสกิล/skill point" ของ `0155`: เติม `n_LEVELS`/`f_SP_LEVE1`/`f_SP_LEVEL2PLUS` เข้า
`_CONTEXT_COLUMNS` (มีอยู่แล้วในไฟล์ที่ extract ไว้ `data/skill_context_starting_kit.tsv` — ตรวจ header คอลัมน์
รอบนี้ยืนยันว่ามีครบ ไม่ต้อง re-extract) แล้วเปิดสองฟังก์ชันอ่านชื่อจริง: `max_skill_level(skill_id)` (`n_LEVELS`)
กับ `skill_point_cost_to_learn(skill_id)` (`f_SP_LEVE1`) — ตามแพทเทิร์นเดิมของ `cooldown_seconds`/`stamina_cost`
(รอบ `kd06fo`) คือ "อ่านชื่อจริง ยังไม่ผูกเกตอะไร" **ไม่เติม** accessor ให้ `f_SP_LEVEL2PLUS` เพราะทั้ง 8
ไอดีในแคตาล็อกนี้ `n_LEVELS == 1` หมด (ตรวจค่าจริงจากตารางรอบนี้) ⇒ ไม่มีไอดีไหนให้ทดสอบคอลัมน์นั้นจริง — เติม
accessor เปล่าให้ครบคอลัมน์เฉยๆ คือสิ่งที่กติกาห้าม (`0013` ข้อ 3 ของรอบก่อน ยึดหลักเดียวกัน)

`tests/test_skill_catalog.py` (+2 เทส): `max_skill_level` = 1 ทั้ง 8 ไอดี (cross-check กับ raw column) ·
`skill_point_cost_to_learn` เทียบค่าจริงจากตาราง (99/110/40000-44000 = 1.0 · 111 = 0.2 — เลขจริงจากตาราง ไม่ได้
คิดเอง, cross-check กับ `float(raw column)` ด้วย)

## pf-adversary — **ผลคืนแล้วในรอบนี้ ไม่ใช่ ADVERSARY_PENDING**

สั่งต้นรอบทันทีที่ไฟล์แรก (`damage_by_class_skill.py` + เทส) เขียนเสร็จ (ก่อน commit ตามกฎเวลา — งานที่เหลือ
ของรอบเดินคู่ไปด้วย) ให้ตรวจไฟล์ใหม่ทั้งสองไฟล์จริงจากดิสก์ (ไม่ใช่ diff string) เทียบกับตารางจริง:

- ไล่ตรวจ `class_catalog.CLASS_ID_TO_STARTING_SKILL_IDS` กับ `data/charcreate_class.tsv` จริง ครบทั้ง 5×5 คู่ —
  **ไม่พบคู่ class/skill ที่เกตตอบผิด**
- ทดลอง mutate `is_skill_granted_to_class` ให้คืน `True` เสมอ (ข้ามเกตคลาสทั้งหมด) — **4 จาก 9 เทสแดงทันที**
  พร้อมข้อความชัด ⇒ ชุดเทสมีฟันจริง ไม่ใช่ rubber stamp
- grep ทั้งรีโปหา caller อื่นของ `damage_by_class_skill` — เจอแค่ไฟล์เทสตัวเอง ยืนยัน "zero production callers"
- ทดลองส่ง attacker/defender ผิดชนิด (`None`) เข้า `resolve_class_skill_damage(1, 99, None, None)` — ยืนยันว่า
  `MobCombatContractError` จาก `mob_combat` ทะลุออกมาตรงๆ ไม่ถูก `except DamageBySkillError` กลืนเป็น class
  refusal ปลอม (ขอบเขต except แคบพอจริง)
- ข้อสังเกตไม่บล็อก: `__cause__` chain ไม่มีเทสยืนยันตรงๆ (ผลคือทรัพย์สินที่ถูก assert ด้วยมือของ adversary เอง
  ไม่ใช่ของชุดเทส) · คำถามเปิด: วันที่มี caller จริง+capture จริง จะมีอะไรมาเช็คไขว้ทาง capture ว่า class↔skill
  binding ของ `class_catalog` เองถูกไหม (ตอนนี้พึ่ง sha256 pin ต่อไฟล์เดียว) — **ไม่ใช่บั๊ก เป็นข้อจำกัดที่รู้อยู่
  แล้วของ `class_catalog.py` เอง (docstring "Main/sub-profession structure. No column...")**, บันทึกไว้เป็น
  ข้อสังเกต ไม่เปิดใบใหม่ (ไม่มีอะไรให้แก้วันนี้ — รอ capture จริงเหมือนกันกับที่ `damage_by_skill.py` รอ)

**ไม่พบข้อบกพร่องจริง** ⇒ ไม่มี `ADVERSARY_PENDING` ค้างข้ามรอบ

## ชุดเต็ม + preflight

`git fetch origin main` → merge เข้าต้นไม้ของรอบ (`main` ขยับระหว่างรอบ: `#783` LANE-DB boot-crash guard เข้ามา
พอดี — merge สำเร็จไม่ชนไฟล์) → รันชุดเต็มครั้งเดียวบนต้นไม้ที่ merge แล้ว **ติดกับ push** ตามกฎ:

```
PYTHONPATH=src python3 -m pytest tests -q
```

ผล: **`10436 passed, 327 skipped, 0 failed` (471.28s)** — เขียว

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` (รันจากโคลน `pf_bridge`): **PREFLIGHT PASS**
(cp874 · ไม่มี skip ใหม่ · main อยู่ใน branch แล้ว)

ไม่มีไฟล์ `tests/test_*.py` ใหม่ที่ต้องซ้อม `pytest_subset`/`skip_census` แยก — **มีไฟล์เทสใหม่จริง
(`tests/test_damage_by_class_skill.py`)** ⇒ ต้องซ้อม (ดูผลด้านล่าง):

```
git worktree add --detach <ที่ว่างนอก pirate-force-server> HEAD
grep -l 'GameClient\|capture_v141' tests/*.py | sort -u | grep -v test_foundation_legacy_seam.py > excl.txt
python3 -m pytest tests -q -rs $(sed 's|^|--ignore |' excl.txt) > log.txt   # pytest_subset
python3 tools/pf_pytest_precondition_census.py --report log.txt --excluded excl.txt   # skip_census
```

ผล: **`pytest_subset` PASS** (`9490 passed, 93 skipped, 17584 subtests passed`, worktree แยก ไม่มี `pf_bridge` ข้าง ๆ)
· **`skip_census` PASS** ("every skip is declared, named and pinned", 93 skip ทั้งหมดมี precondition ชื่อจริง
ไม่มี skip เปล่า) · worktree ลบ+prune แล้วหลังใช้งาน

ไม่มี skip ใหม่/ลบ skip รอบนี้ (ไม่แตะ `docs/PYTEST_SKIP_PINS.json`) · ไม่แตะ `HYPOTHESIS_LEDGER.json`/
`FUNCTIONAL_COVERAGE.json` (ไม่ได้แก้โมดูล hypothesis หรือ coverage-tracked item ใดๆ) ⇒ ไม่ต้องรัน
`verify_hypothesis_ledger.py`/`verify_functional_coverage.py` รอบนี้

## งานสำรอง (ทำเมื่องานหลักติด) — เติมให้ครบ 3 ข้อใหม่ตามเกณฑ์ `0155` ข้อ 2

1. **[โค้ด]** ผูก validator ฝั่งเซิร์ฟเวอร์ตัวแรกของระบบ skill point: ฟังก์ชันบริสุทธิ์ `can_afford_to_learn
   (current_skill_points, skill_id)` เทียบ `skill_catalog.skill_point_cost_to_learn(skill_id)` (โมดูลใหม่ เช่น
   `skill_learn_validator.py`) — ยังไม่ต่อ responder/DB จริง เหมือน `resolve_class_skill_damage` วันนี้ · ไฟล์:
   `src/pirateforce_foundation/skill_learn_validator.py` (ใหม่) + เทสคู่ · หลักฐานผ่าน: เทสเทียบค่าจริงจาก
   `skill_point_cost_to_learn` ของทั้ง 8 ไอดี ไม่พิมพ์ตัวเลขคาดหวังลอยๆ
2. **[ใบ GT/RE ที่รันได้]** ร่างใบ GT "ยืนยันดาเมจ skill 99 ต่อคลาส บนสนาม Training Iron Man 916" — ข้อมูลจาก
   `damage_by_class_skill.resolve_class_skill_damage(class_id, 99, mob_combat.pin_attacker(), ...)` จริงต่อคลาส
   ทั้ง 5 (ตัวเลขคาดหวังบนจอ derive จากโค้ดวันนี้ ไม่ใช่พิมพ์มือ) — ห้ามวาง roster เอง (เขต A/B) จึงใช้หุ่น 916 ที่
   มีอยู่แล้วเท่านั้น · ไฟล์: ใบ GT ใหม่ใน `GAME_TEST_QUEUE.md` (ขอเลขจาก chief) · หลักฐานผ่าน: ใบรันได้จริงไม่ต้อง
   แก้เพิ่ม
3. **[อ่าน/เทียบ — นับได้ไม่เกิน 1 ใน 3 ข้อ]** ทบทวน `persistence_class_id.py` + `persistence_starting_skills.py`
   คู่กัน (ค้างมาจาก `plg1ne`/`9emwkk` ข้อ 3) ว่าตอนนี้ (หลัง `class_catalog` มี `max_skill_level`/
   `skill_point_cost_to_learn` แล้ว) มีจุดเสียบ validator ข้อ 1 ข้างบนให้ LANE-DB จริงหรือยัง — ยังไม่ถึงคิวนี้จน
   ข้อ 1 เดินหน้าก่อน

## ขยับ NOW/M ข้อไหน

**ขยับ** — รอบนี้มี PR เซิร์ฟเวอร์จริงพร้อมโค้ด+เทสใหม่ (ไม่ใช่รอบอ่านอย่างเดียวแบบ `h4mxrq`/`9emwkk`) ตรงตาม
`COO-DECISION 20260905_0155` ที่สั่งไว้ ⇒ ปิดความเสี่ยง escalation `04:36` · ไม่ใช่ M ladder ข้อใหม่โดยตรง (ยังไม่มี
ผู้เล่นเห็นบนจอ — `resolve_class_skill_damage` ยัง zero production caller เหมือนโมดูลพี่น้องมันทุกตัว รอสาย
เดียวกันกับ `GT-243`/`RE-240` capture) แต่เป็นความคืบหน้าจริงของคิวเริ่มต้นข้อ 3 (สูตรดาเมจ) + ข้อ 5 (ระบบสกิล
พอยต์) ที่ COO สั่งให้เดินต่อ "ไม่รอ caller"

## ส่งอะไร

**pirate-force-server**: PR #786 (สาขา `claude/inspiring-albattani-jbe8rr`) — เปิดแล้ว ไม่เป็น draft มี marker
ตั้งแต่เปิด (`https://github.com/panyaasanee/pirate-force-server/pull/786`)
- `src/pirateforce_foundation/damage_by_class_skill.py` (ใหม่) + `tests/test_damage_by_class_skill.py` (ใหม่)
- `src/pirateforce_foundation/skill_catalog.py` (+2 accessor) + `tests/test_skill_catalog.py` (+2 เทส)

**pf_bridge**: PR #1248 (แทน `rounds/CS_jbe8rr_claim.md` ด้วยไฟล์นี้), เพิ่ม:
- `.CONSUMED.txt` ของใบ `0155`
- จดหมาย `ADDRESSEE: COO` แจ้งปิดงาน (ใบนี้)

## nonclaims

- ไม่อ้างว่า `resolve_class_skill_damage`/accessor ใหม่มี production caller — ยังไม่มี (grep ยืนยันรอบนี้) รอ
  ผล attended `GT-243`/`RE-240` เหมือน `damage_by_skill.py` เดิมทุกประการ
- ไม่อ้างว่าปิดคำถาม "อาชีพรอง" (secondary class) — `class_catalog.py` เองบันทึกไว้แล้วว่าไม่มีคอลัมน์ไหนในตาราง
  นี้เข้ารหัสโครงสร้างอาชีพหลัก/รอง รอบนี้ไม่ได้แตะทิศทางนั้น (เลือกทำ 2 จาก 5 ทิศที่ `0155` อนุมัติ)
- ไม่อ้างว่า `f_SP_LEVEL2PLUS` มีความหมายที่ตรวจแล้ว — ไม่เติม accessor ให้ตามที่อธิบายด้านบน (เหตุผล: n_LEVELS
  ของทั้ง 8 ไอดีเป็น 1 หมด ไม่มีไอดีให้ทดสอบคอลัมน์นี้จริง)
- ไม่อ้างว่างานสำรองข้อ 1/2 ใหม่เสร็จแล้ว — เป็นคิวเริ่มต้นรอบหน้า ยังไม่ได้ลงมือ

## ติดอะไร / ใครปลด

- ไม่มี — งานหลักของรอบนี้ (server PR ตาม `0155`) ปิดสำเร็จภายในรอบเดียว ไม่มีตัวบล็อกใหม่ให้รายงาน

-- LANE-CS
