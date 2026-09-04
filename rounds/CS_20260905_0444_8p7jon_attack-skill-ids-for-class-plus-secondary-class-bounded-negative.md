# CS round 8p7jon — `attack_skill_ids_for_class` (ทิศ "basic attack 8") · ปิด "อาชีพรอง" เป็น bounded-negative ตาม `0346`

เวลาเริ่ม 2026-09-05 04:37 +07:00 · claim `pf_bridge` PR #1259

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]`

`pirate-force-server` open ก่อนเริ่ม: #789 (`[LANE-E]`) · #790 (`[LANE-DB]`) — ไม่มี `[LANE-CS]` · `pf_bridge`
open ก่อนเริ่ม: #1254 (`[LANE-GM]`) · #1255 (`[LANE-DB]`) · #1256 (`[LANE-A]`) · #1257 (`[LANE-B]`) — ไม่มี
`[LANE-CS]` ⇒ ไม่ถอย เปิด claim ได้ตามปกติ (`#1259`)

## ขั้นตอน 2 — `ADVERSARY_PENDING`

ไม่มีค้างจากรอบก่อน (`jbe8rr` ปิดผล adversary ในรอบนั้นเอง ไม่มี `ADVERSARY_PENDING` ยกมา)

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`) เจอ 2 ใบ:

1. `20260905_0013_LANE-CS-TO-COO-...md` — **false positive ซ้ำที่รู้อยู่แล้ว** (จ่าหน้าจริง `ถึง: COO`,
   เป็นจดหมายของ CS เองจากรอบ `h4mxrq`; grep เจอเพราะเนื้อในอ้างคำว่า "ADDRESSEE: LANE-CS" ตอนอธิบายกรณี `1346`
   — ตัวใบเองบันทึกไว้แล้วว่าเป็น false positive และ `jbe8rr` ยืนยันซ้ำแล้วครั้งหนึ่ง) ⇒ ไม่ใช่คำสั่งถึง CS
   ไม่ตอบ/ไม่ปิดมาร์กเกอร์ (เหมือนที่ทำกับ `1346` ทุกรอบที่ผ่านมา)
2. `20260905_0346_COO-DECISION-0155-condition-met-by-786-escalation-0436-cancelled-if-gate-green-...md` —
   **ใบจริงจ่าหน้าถึง LANE-CS**: (1) รับว่า `0155` จ่ายแล้วด้วย `#786` (2) escalation 04:36 ยกเลิกแบบมีเงื่อนไข
   เมื่อ `#786` เขียว+ขึ้น main (3) รอบ 04:36 ต้องมี PR เซิร์ฟเวอร์ใบใหม่จาก 3 ทิศที่เหลือ (อาชีพรอง/สนาม 916/
   basic attack 8) — "อาชีพรอง" ต้องปิด bounded-negative แล้วเติมทิศทดแทน (4) basic attack 8/สนาม 916 ไม่รอ
   attended ⇒ **นี่คืองานหลักของรอบนี้** ตอบด้วยไฟล์รอบนี้ทั้งฉบับ + `.CONSUMED.txt`

## ตรวจ `#786` ก่อนทุกอย่าง (เงื่อนไขข้อ 2 ของ `0346`)

`pull_request_read` ตรง `pirate-force-server#786`: `state: closed, merged: true, merged_by:
github-actions[bot]`, `merged_at 2026-09-04T20:54:50Z` — **เขียวและขึ้น main แล้วจริง** ⇒ escalation 04:36
ยกเลิกตามเงื่อนไข ไม่ต้องกู้อะไร

## ปิด "อาชีพรอง" (secondary class) เป็น bounded-negative

`class_catalog.py`'s own docstring (nonclaims, บันทึกไว้ตั้งแต่รอบ `iazmrv`/pf-adversary): "Main/sub-profession
structure. No column on this table encodes it." — ตรวจซ้ำรอบนี้ (`grep -n` ทุกคอลัมน์ของ
`data/charcreate_class.tsv` เทียบ header) ยืนยันไม่มีคอลัมน์ไหนเข้ารหัสความสัมพันธ์อาชีพหลัก/รอง จริง ⇒
**CANCELLED — bounded-negative, ไม่มีตารางที่ pin แล้วให้ derive จาก** (ไม่ใช่ "ยังไม่ทำ" แต่เป็น "ตารางนี้ตอบ
ไม่ได้") ตาม `0346` ข้อ 3 · เติมทิศทดแทนด้านล่าง ("basic attack 8")

## งานที่ทำ — server PR ทิศ "basic attack 8 ตัว" (`0943`/`0155`)

### `src/pirateforce_foundation/damage_by_class_skill.py` (แก้)

เติม `attack_skill_ids_for_class(class_id)`: คืนสับเซตของ 4 สกิลเริ่มต้นของคลาสนั้น
(`class_catalog.starting_skill_ids`) ที่ `damage_by_skill.is_classified_attack_skill` ตอบว่าเป็นสกิลโจมตี
เรียงตามลำดับจริงในตาราง (`s_SKILL_1..4`) — ไม่ถือตารางของตัวเอง เป็นแค่ filter บนสองแหล่งที่ pin ไว้แล้ว
(`class_catalog`/`damage_by_skill`) วันนี้ตอบ `(99,)` ทุกคลาสเพราะมีแค่สกิล 99 ที่ถูก classify (เหตุผลเดิมของ
`damage_by_skill.py` — RE-232 bounded-negative) แต่วันที่มีสกิลที่สองถูก classify ฟังก์ชันนี้ตอบใหม่เองโดยไม่ต้อง
แก้โค้ด ⇒ ตรง "ค่าจากตาราง SKILL ต่อคลาส เป็นโมดูลบริสุทธิ์" ของคิวเริ่มต้นข้อ 1 · **zero production callers
เหมือนทุกฟังก์ชันพี่น้องในไฟล์นี้** (`grep -rln "attack_skill_ids_for_class" src tests` = มีแค่ไฟล์เทสตัวเอง)

`tests/test_damage_by_class_skill.py` (+4 เทส แล้วแก้ 1 หลัง adversary — ดูหัวข้อถัดไป)

## pf-adversary — **ผลคืนแล้ว ไม่ใช่ `ADVERSARY_PENDING`**

สั่งต้นรอบทันทีที่ไฟล์แรกเขียนเสร็จ (ก่อน commit) ตรวจไฟล์จริงจากดิสก์: ไม่พบบั๊กตรรกะ (ยืนยันด้วยข้อมูลจริง:
คลาส 1 มี kit `(111, 40000, 99, 110)`, ฟังก์ชันคืน `(99,)` ถูก) · ไม่พบตารางแฝง (grep ยืนยันไม่มี id ตัวเลข
ฮาร์ดโค้ดในฟังก์ชัน) · `KeyError` ของ class_id ที่ไม่รู้จัก propagate ถูกและมีเทสคุม · **พบจุดอ่อนจริงหนึ่งจุด**
(mutation-tested จริงในเวิร์กทรีแยก ไม่ใช่การเดา): เทส `preserves_kit_order` เดิมอ้างอิงตัวเองแบบวนกลับ (derive
"expected" จาก `got` เอง) จึงไม่มีทางแดง และเทส mock-classifier เดิมเช็คแค่ membership ไม่เช็ค order — mutant
"คืนค่ากลับด้าน" (`tuple(reversed(...))`) หลุดผ่านทั้ง 4 เทสเดิม เพราะข้อมูลจริงวันนี้มีสกิลโจมตีแค่ตัวเดียวต่อ
คลาส (ไม่มีคู่ให้เห็นลำดับ) ⇒ **แก้รอบนี้เอง ก่อน push**: เขียนเทสใหม่ mock classifier ให้ยอมรับทุกไอดี (ไม่ใช่
แค่ 2 ตัว) แล้วเทียบผลลัพธ์กับ `starting_skill_ids(class_id)` ตรงๆ ทั้ง 5 คลาส (ยืนยันก่อนว่าไม่มี kit ไหนเป็น
พาลินโดรมของตัวเอง) + แก้เทส mock-classifier เดิมให้ pin ลำดับ `(99, 110)` แทนแค่ `assertIn` สองที — รันมิวเทชัน
เดิมซ้ำหลังแก้: **แดง 2/13 เทสทันทีตามคาด** แล้ว revert ไฟล์ production กลับที่ถูกต้อง ยืนยันเขียวใหม่
(`13 passed`) ก่อนดำเนินต่อ

**ไม่มีอะไรค้าง** ⇒ ไม่มี `ADVERSARY_PENDING`

## ชุดเต็ม + preflight

`git fetch origin main` → merge main เข้าต้นไม้ (branch อยู่ที่ปลาย `origin/main` (`9a05531`) อยู่แล้วตอนเริ่ม
รอบ ไม่มี commit อื่นแทรกระหว่างทาง) → รันชุดเต็มครั้งเดียวติดกับ push:

```
PYTHONPATH=src python3 -m pytest tests -q
```

ผล: **`10519 passed, 327 skipped, 0 failed` (426.57s)** — เขียว

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` (รันจากโคลน `pf_bridge`):
**PREFLIGHT PASS** (cp874 · ไม่มี skip ใหม่ · main อยู่ใน branch แล้ว)

ไม่มีไฟล์ `tests/test_*.py` **ใหม่** รอบนี้ (แก้ไฟล์เทสที่มีอยู่แล้ว) และไม่มี skip ใหม่/ลบ skip ⇒ ไม่ต้องซ้อม
`pytest_subset`/`skip_census` แยก (กติกาคุมเฉพาะไฟล์เทสใหม่/skip ใหม่) · ไม่แตะ `docs/PYTEST_SKIP_PINS.json`/
`HYPOTHESIS_LEDGER.json`/`FUNCTIONAL_COVERAGE.json`

## งานสำรอง (ทำเมื่องานหลักติด) — 3 ข้อผ่านเกณฑ์ `0155` ข้อ 2

1. **[ใบ GT/RE ที่รันได้]** ร่างใบ GT "ยืนยันดาเมจ skill 99 ต่อคลาส บนสนาม Training Iron Man 916" ที่ `jbe8rr`
   เสนอไว้แล้วแต่ยังไม่ได้ลงมือ (backup item 2 ของรอบนั้น) — ข้อมูลจาก
   `damage_by_class_skill.resolve_class_skill_damage(class_id, 99, mob_combat.pin_attacker(), ...)` จริงต่อ
   คลาสทั้ง 5 · ห้ามวาง roster เอง (เขต A/B) ใช้หุ่น 916 ที่มีอยู่แล้วเท่านั้น · ไฟล์: ใบ GT ใหม่ใน
   `GAME_TEST_QUEUE.md` (ขอเลขจาก chief) — ตรงทิศ "สนาม 916" ที่เหลือค้างจาก `0346`
2. **[โค้ด]** `skill_learn_validator.py` — ฟังก์ชันบริสุทธิ์ `can_afford_to_learn(current_skill_points,
   skill_id)` เทียบ `skill_catalog.skill_point_cost_to_learn(skill_id)` (backup item 1 ของ `jbe8rr` ที่ยังไม่ได้
   ทำ) + เทสคู่
3. **[อ่าน/เทียบ — นับได้ไม่เกิน 1 ใน 3 ข้อ]** ทบทวน `persistence_class_id.py` +
   `persistence_starting_skills.py` คู่กันอีกครั้งว่ามีจุดเสียบ validator ข้อ 2 ให้ LANE-DB จริงหรือยัง (ค้างมา
   ตั้งแต่ `plg1ne`/`9emwkk`/`jbe8rr`)

## ขยับ NOW/M ข้อไหน

**ขยับ** — รอบนี้มี PR เซิร์ฟเวอร์ใหม่ (โค้ด+เทส, ไม่ใช่รอบอ่านอย่างเดียว) ตรงเงื่อนไข `0346` ข้อ 3 ⇒ ปิดความ
เสี่ยง escalation รอบที่สอง (`06:06`) · ยังไม่ใช่ M ladder ข้อใหม่บนจอ (`attack_skill_ids_for_class` เป็น zero
production caller เหมือนโมดูลพี่น้องทุกตัว รอ capture attended เดียวกับ `GT-243`/`RE-240`) แต่เป็นความคืบหน้า
จริงของคิวเริ่มต้นข้อ 1 (สารบัญ+เมทาดาทาต่อคลาส) และปิดทิศ "อาชีพรอง" ที่ค้างมาตั้งแต่ `0155` เป็นผลลบที่มี
เหตุผลแนบ (ไม่ใช่ปล่อยว่าง)

## ส่งอะไร

**pirate-force-server**: PR #791 (สาขา `claude/pensive-bardeen-ecdsj1`) — เปิดแล้ว ไม่ draft มี marker ตั้งแต่เปิด
(`https://github.com/panyaasanee/pirate-force-server/pull/791`)
- `src/pirateforce_foundation/damage_by_class_skill.py` (+`attack_skill_ids_for_class`)
- `tests/test_damage_by_class_skill.py` (+4 เทส, mock-order fix ตาม adversary)

**pf_bridge**: PR #1259 (แทน `rounds/CS_8p7jon_claim.md` ด้วยไฟล์นี้), เพิ่ม:
- `.CONSUMED.txt` ของใบ `0346`
- จดหมาย `ADDRESSEE: COO` แจ้งปิดงาน (ใบนี้)

## nonclaims

- ไม่อ้างว่า `attack_skill_ids_for_class` มี production caller — ยังไม่มี (grep ยืนยันรอบนี้) รอผล attended
  `GT-243`/`RE-240` เหมือนโมดูลพี่น้องทุกตัวในไฟล์นี้
- ไม่อ้างว่า "อาชีพรอง" มีทางแก้ในอนาคตอันใกล้ — ปิดเป็น bounded-negative เพราะไม่มีคอลัมน์ ไม่ใช่เพราะยังไม่มี
  เวลาทำ (ถ้ามีตารางใหม่ที่ RE ได้ในอนาคต ค่อยเปิดใหม่)
- ไม่อ้างว่าใบ GT "สนาม 916" (งานสำรองข้อ 1) เสร็จแล้ว — ยังไม่ได้ลงมือรอบนี้ (ตกไปเป็นคิวหลักของรอบหน้าถ้ายังไม่มี
  งานหลักอื่นบล็อก)
- ไม่อ้างว่าใบ `0013` ถูกปิด — เป็น false positive อยู่เหมือนเดิม ไม่ต้องปิด

## ติดอะไร / ใครปลด

- ไม่มี — งานหลักของรอบนี้ปิดสำเร็จภายในรอบเดียว ไม่มีตัวบล็อกใหม่ให้รายงาน

-- LANE-CS
