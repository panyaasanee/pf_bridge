# CS round mps8zh — n_PASSIVE_EFFECT bounded-negative finding, pinned

เวลาเริ่ม 2026-09-05 10:44 +07:00 · เวลาจบ 2026-09-05 11:11 +07:00

## ขั้นตอน 0 — `NOW.md` ก่อนทุกอย่าง

อ่านแล้ว (`git fetch` ก่อน) หัวข้อล่าสุด `09:48` (COO): **NOW ไม่ขยับข้อไหน** — โปรเจกต์อยู่ที่ M2 ขั้นคงเดิม
รอ `RE-256` บนเครื่อง Panya · หมายเหตุใน `09:48` ว่า "CS ล่าสุด 07:56 (`#1282`/`#802`) รอบ 09:06 ยังไม่เห็น PR —
ดูรอบหน้า" — รอบ 09:06 ของสายนี้ไม่ยิง (ไม่ทราบสาเหตุ ไม่มีข้อมูลให้สอบสวนจากฝั่งนี้) รอบนี้คือรอบถัดไปจริง
(นาฬิกา 10:44 ตอนเริ่ม)

**รอบนี้ขยับ NOW/M ข้อไหน**: ไม่ขยับขั้นบันได M (production caller ยังศูนย์เหมือนเดิม) — ไม่ขยับความคืบหน้า
คิวเริ่มต้นข้อ 4 ตรง ๆ ด้วย (งานหลักของรอบนี้คือปิดทางที่ผิดของสูตรจำแนกสกิล ไม่ใช่เปิดสกิลใหม่) แต่เป็นงานสำคัญของ
คิวเริ่มต้นข้อ 3 ("หาและดูแลเรื่องสูตรคำนวนดาเมจ") ในความหมายกว้าง: กันไม่ให้ future round สร้าง accessor
`is_pure_passive_effect()`-ทรงนี้บนคอลัมน์ที่พิสูจน์แล้วว่าไม่แยกพาสซีฟ/แอ็กทีฟจริง — ทำงานเดียวกับที่ round
6o11t1 ทำไว้กับ `n_PASSIVE`

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]` ทั้งสองรีโป

`list_pull_requests` `state:open`:
- `pirate-force-server`: 0 ใบหัว `[LANE-CS]` (มี `#810` LANE-A, `#794` LANE-E — ไม่เกี่ยว) ⇒ ไม่ถอย
- `pf_bridge`: 0 ใบหัว `[LANE-CS]` (มี `#1297` LANE-B claim, `#1295` LANE-GM claim — ไม่เกี่ยว) ⇒ ไม่ถอย · claim
  เปิดที่นี่ (`#1298`, ดูข้อ "ส่งอะไร")

## ขั้นตอน 2 — `ADVERSARY_PENDING` จากรอบก่อน

ไม่มีค้าง (รอบ `b190t0` ปิดผล adversary ในรอบนั้นเอง ไม่มี pending ยกมา)

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`, ยืนยันด้วย `git ls-tree` ตรงกับ
working tree) — **ทุกใบมี `.CONSUMED.txt` แล้วจากรอบก่อน ไม่มีใบใหม่รอบนี้**

## งานที่ทำ — บันได M ข้อ 3 (สูตรดาเมจ): ปิดทางลัดที่สองของการจำแนกชนิดสกิล

หลัง round 6o11t1 พิสูจน์ว่า `n_PASSIVE` ไม่ใช่คอลัมน์ชนิดสกิล ทางเดาถัดไปที่เป็นธรรมชาติคือคู่ (`s_CAST_CONDITION`
ว่าง, `n_PASSIVE_EFFECT` ไม่เป็นศูนย์) — 5 สกิล Basic Training ที่รู้จักอยู่แล้วเข้ารูปนี้พอดี สั่ง `pf-static-re`
ตรวจข้ามตาราง `CONSTDATA_TH__SKILL_CONTEXT.tsv` เต็ม (2165 แถว ไม่ใช่แค่ 8 ไอดีในแคตาล็อกของสายนี้) แล้วยืนยันมือ
อีกชั้นด้วย awk ตรงไฟล์จริงก่อนเชื่อ (ตัวเลขทุกตัวตรงกัน) — ผล **BOUNDED-NEGATIVE**:

- `s_CAST_CONDITION` ว่างมีเป๊ะ 25 แถวทั้งตาราง: เทียร์ 4 แถวต่ออาชีพ (40000/40013/40022/40025 · 41000/41007/
  41010/41025 · 42000/42004/42016/42025 · 43000/43023/43024/43025 · 44000/44023/44024/44025) บวกอาชีพที่ 6
  ที่ `own_class_bit()` เคยตั้งชื่อบิต (8) และไอดีเดียว (45000) ไว้แล้ว — รอบนี้ยืนยันเป็นเทียร์เต็ม 4 แถว
  (45000/45023/45024/45025) ยังไม่เลือกได้และไม่ถูกบรรจุในแคตาล็อกเหมือนเดิม — บวกอีกหนึ่งแถวที่ไม่ใช่ Basic
  Training เลย (id 2954) ซึ่ง `n_PASSIVE_EFFECT = 0` — ข้ออ้างแคบ ("ว่างแปลว่าไม่เป็นศูนย์") มีข้อโต้แย้งตั้งแต่ยัง
  ไม่ออกจากถังของตัวเอง
- ทิศตรงข้ามพังหนักกว่า: 146 จาก 2140 แถวที่แอ็กทีฟจริง (cast condition ไม่ว่าง) มี `n_PASSIVE_EFFECT` ไม่เป็นศูนย์
  ด้วย (6.8% ไม่ใช่หางปัดเศษ) — รวมถึง id 8200 (สกิลโจมตีเดี่ยวที่แอ็กทีฟจริงตามข้อความบรรยาย) ที่
  `n_PASSIVE_EFFECT = 40002` ชี้ไปไอดีอื่น ไม่ใช่ตัวเอง — หักล้างสองข้ออ้างพร้อมกัน (ไม่เป็นศูนย์ ≠ พาสซีฟ/ว่าง,
  และไม่เป็นศูนย์ ≠ self-reference แบบ `n_ISCLASS` เสมอไป)
- id 3546/3547 (ชื่อสกิลอ่านเป็น buff/heal พอดีกับที่โปรเจกต์กำลังหา) แอ็กทีฟจริง (`GO(0)`) แต่
  `n_PASSIVE_EFFECT = 0` — มุมตรงข้ามกับที่สมมติฐานทำนาย

บันทึกใน docstring ของ `skill_catalog.py` (หัวข้อ "ROUND mps8zh") + ปักด้วยคลาสเทสใหม่
`NPassiveEffectDoesNotDiscriminatePassiveFromActiveTests` ใน `tests/test_skill_catalog.py` (5 เทส,
`BRIDGE_GAMEDATA`-guarded เพราะแถวที่หักล้างอยู่นอกแคตาล็อก 8 ไอดีของสายนี้) + อัปเดต `docs/PYTEST_SKIP_PINS.json`
ให้ตรงกับ 5 เทสใหม่ **ไม่มีโค้ด production เปลี่ยนแม้แต่บรรทัดเดียว** — `skill_catalog.py`'s accessors ทั้งหมดคง
เดิม

## pf-adversary — ผลคืนแล้ว ไม่มี `ADVERSARY_PENDING`

สั่งกลางรอบ (ไม่ทันต้นรอบ เพราะงานเริ่มด้วยการสั่ง `pf-static-re` ก่อน — บันทึกไว้ตรง ๆ) บนเวิร์กทรีแยกของตัวเอง
เอง: ตรวจตัวเลขทุกตัวซ้ำอิสระตรงกับไฟล์จริง (25 แถว, ไอดีตรงเป๊ะ, 146/2140, ฯลฯ) · มิวเทตค่า pin สองจุด (146→147,
2954→2955) ทั้งคู่ทำให้เทสแดง (ไม่ vacuous) · ยืนยัน skip-guard ทำงานถูกทั้งมี/ไม่มี `pf_bridge` sibling และ
census รายงานเป็น declared skip · **ไม่พบข้อบกพร่อง** — ข้อสังเกตหนึ่งข้อ (ชื่อคลาสเทสอาจถูกอ่านกว้างเกินไปว่า
"ไม่มีคอลัมน์ไหนแยกพาสซีฟได้เลย") ถูกพับเข้า docstring ของคลาสเทสเองเป็นประโยค "SCOPED CLAIM" แล้ว (ไม่ใช่บั๊ก
เป็นความชัดเจนของถ้อยคำ)

## ชุดเต็ม + preflight

`git fetch origin main` → main ขยับจาก `987edc5` เป็น `b49a4e4` (LANE-A: RE-256/scene 17 roster, ไม่ทับไฟล์กัน) →
`git merge origin/main` เข้ากิ่งของรอบ (merge สะอาด ไม่มี conflict) → รันชุดเต็มครั้งเดียวติดกับ push บนต้นไม้ที่
merge แล้ว:

```
python3 -m pytest tests -q -rs
```

ผล: **`10783 passed, 327 skipped, 19916 subtests passed` (502.64s)** — เขียว

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS**

**ไฟล์เทสใหม่**: ไม่มีไฟล์ `.py` ใหม่ (แก้ไฟล์เดิม `tests/test_skill_catalog.py` เพิ่มคลาส) แต่ **เพิ่ม skip ใหม่**
(5 เทสถูก `BRIDGE_GAMEDATA`-guard) ⇒ ซ้อมทั้งสองช่องในเวิร์กทรีแยกที่ไม่มี `pf_bridge` ข้าง ๆ (นอกโฟลเดอร์แม่):

```
python3 -m pytest tests -q -rs --ignore ... (48 ไฟล์ excl.txt)  → 9783 passed, 98 skipped, 17771 subtests (exit 0)
python3 tools/pf_pytest_precondition_census.py --report log.txt --excluded excl.txt → RESULT: PASS (exit 0)
```

`bridge_gamedata tests/test_skill_catalog.py x6` ตรงกับ `count: 6` ที่เติมใน `docs/PYTEST_SKIP_PINS.json`
พอดี (1 เทสเดิม + 5 เทสใหม่)

## งานสำรอง (ทำเมื่องานหลักติด) — ยังไม่ได้ลงมือรอบนี้ งานหลักไม่ติด

1. **[โค้ด]** จุดเสียบ `can_afford_to_learn` ให้ LANE-DB จริง — ตรวจซ้ำรอบนี้: `grep -rn skill_points
   src/pirateforce_foundation/persistence_*.py src/pirateforce_foundation/store.py` ยังไม่มีคอลัมน์ต่อตัวละคร
   จริง (มีแค่ `attr_wire.py`/`stats_progression_hypothesis.py` ที่นิยาม wire field) — ยังบล็อกจริง ยกมาอีกรอบ
2. **[อ่าน/เทียบ — นับได้ไม่เกิน 1 ใน 3 ข้อ]** ทวนสารบัญคิวเริ่มต้นข้อ 1: `n_TARGET`/`n_EQUIPTYPE`/
   `n_EQUIPTYPE_LHAND` ใน `skill_catalog.py` ยังไม่มี accessor ชื่อจริง — ยังไม่มีเหตุผล RE ให้ตั้งชื่อ ยกมาอีกรอบ
3. **[ใบ GT/RE ที่รันได้]** เมื่อ `GT-243` capture ได้ผล (ยังไม่ถึง — ต้องเครื่อง Panya) เตรียม caller จริงของ
   `resolve_skill_damage`/`resolve_class_skill_damage` ตามฟิลด์ที่ผลชี้ทันที — ระบุไว้กันลืม ไม่ใช่ backup item
   จริงจนกว่าผลมา (ตามที่ `0013` เคยระบุ)

## ขยับ NOW/M ข้อไหน

**ไม่ขยับขั้นบันได M** — ยัง zero production caller เหมือนเดิม งานรอบนี้เป็นงานปิดทางผิดของ "หาและดูแลเรื่องสูตร
คำนวนดาเมจ" (คิวเริ่มต้นข้อ 3 ในความหมายกว้าง: การจำแนกชนิดสกิลเป็นส่วนหนึ่งของการดูแลสูตร) ไม่ใช่การเปิดสกิลใหม่
หรือเดินสายเข้า production — เทียบเท่ากับที่ round 6o11t1 ทำไว้กับ `n_PASSIVE` (ก็ไม่ได้ขยับ NOW/M ตอนนั้นเช่นกัน
แต่กันงานซ้ำ/ผิดพลาดของรอบหลัง)

## ส่งอะไร

**pirate-force-server**: PR #811 (สาขา `claude/pensive-bardeen-mps8zh`) —
`https://github.com/panyaasanee/pirate-force-server/pull/811`
- `src/pirateforce_foundation/skill_catalog.py` (docstring +45 บรรทัด)
- `tests/test_skill_catalog.py` (+98 บรรทัด, คลาสเทสใหม่ 5 เทส)
- `docs/PYTEST_SKIP_PINS.json` (+8/-3, อัปเดตพิน bridge_gamedata ของไฟล์นี้)

**pf_bridge**: PR #1298 (สาขา `claude/vigilant-ramanujan-mps8zh`) — ไฟล์รอบนี้แทน `_claim.md`

## nonclaims

- ไม่อ้างว่าคอลัมน์ไหนในตารางนี้แยกพาสซีฟ/แอ็กทีฟได้ — เฉพาะคู่ (`s_CAST_CONDITION`, `n_PASSIVE_EFFECT`) เท่านั้น
  ที่ถูกพิสูจน์ว่าไม่แยก (จุดที่ pf-adversary เตือน ปักไว้ใน docstring คลาสเทสแล้ว)
- ไม่อ้างว่า production caller มีแล้ว — ยัง zero production caller ทั้ง `damage_by_skill`/`damage_by_class_skill`
- ไม่อ้างว่ารู้ฟิลด์ skill id จริงจาก `GT-243` — ยังรอ attended capture บนเครื่อง Panya
- ไม่อ้างว่า LANE-B ต้องลงมืออะไรจากรอบนี้ — จดหมายส่งมอบสูตร (รอบ `b190t0`) ยังไม่มีคำตอบ ไม่ใช่ตัวบล็อกของรอบนี้

## ติดอะไร / ใครปลด

- ไม่มีตัวบล็อกใหม่ต่อ CS เอง — งานหลักปิดสำเร็จภายในรอบเดียว
- ตัวบล็อกเดิมคงอยู่: `GT-243` ต้องเครื่อง Panya (ผู้ปลด = Panya/chief ตามคิว attended) · จุดเสียบ
  `_dispatch_mob_combat` เขต LANE-B (ผู้ปลด = LANE-B/chief เมื่อ `GT-243` มีผล) · `can_afford_to_learn` รอ
  คอลัมน์ `skill_points` จริงจาก LANE-DB

-- LANE-CS
