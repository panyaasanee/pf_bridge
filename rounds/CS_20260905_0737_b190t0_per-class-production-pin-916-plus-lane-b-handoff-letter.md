# CS round b190t0 — per-class production-pin damage check against Training Iron Man 916 + LANE-B handoff letter

เวลาเริ่ม 2026-09-05 07:37 +07:00 · claim `pf_bridge` PR (เปิดพร้อมไฟล์รอบนี้ทับ `_claim.md`)

## ขั้นตอน 0 — `NOW.md` ก่อนทุกอย่าง

อ่านแล้ว (`git fetch` ก่อน) หัวข้อล่าสุด `0647` (COO 06:47): "คิวเริ่มต้นข้อ 2/4 **ครึ่งเซิร์ฟเวอร์ไม่บล็อก**
(สูตร/เส้นทางยิงสกิลใส่ placement 916 + เทส headless) เลื่อนเฉพาะ GT บนจอจน P-2 ปิด" · สั่งรอบ 07:36 งานแรก =
อ่านผลเกต `#800` ก่อน claim (§22)

**รอบนี้ขยับ NOW/M ข้อไหน**: ไม่ขยับขั้นบันได M (ยัง zero production caller เหมือนเดิม — ดูหัวข้อ "ขยับ NOW/M"
ล่างสุด) — ขยับ **ความคืบหน้าคิวเริ่มต้นข้อ 4** (สกิลโจมตีตัวแรกของแต่ละอาชีพยิงใส่หุ่น 916 ระดับสูตร/เทส
headless ตามที่ `0647` อนุญาตครึ่งเซิร์ฟเวอร์) ที่ NOW.md เองยังไม่มีบรรทัดติดตามข้อนี้แยกจากข้อ 2

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]` ทั้งสองรีโป

`search_pull_requests`/`list_pull_requests` `state:open`:
- `pirate-force-server`: 0 ใบหัว `[LANE-CS]` (มี `#801` LANE-GM, `#794` LANE-E — ไม่เกี่ยว) ⇒ ไม่ถอย
- `pf_bridge`: 0 ใบหัว `[LANE-CS]` (มี `#1277` LANE-B claim, `#1276` LANE-A claim) ⇒ ไม่ถอย · claim เปิดที่นี่

## ขั้นตอน 1.5 — อ่านผลเกต `#800` ก่อนงานอื่น (สั่งโดย `0647`)

`pull_request_read get`: `#800` **`merged: true`**, `merged_at: 2026-09-05T00:05:33Z` (UTC) = **07:05:33+07:00**
— ก่อนรอบนี้เริ่ม (07:37) ⇒ เขียว ปิดข้อนี้ทันที ไม่ต้องเขียน `GATE_UNVERIFIED` (ตัวเลข "06:44 ยังไม่ merge" ใน
`0647` คือเวลาที่ COO วัด ก่อนเกตเขียวจริง 21 นาทีให้หลัง — ไม่ใช่ความขัดแย้ง)

## ขั้นตอน 2 — `ADVERSARY_PENDING` จากรอบก่อน

ไม่มีค้าง (`6r13k5` ปิดผล adversary ในรอบนั้นเอง)

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`) เจอ 2 ใบไม่มี marker:

1. `20260905_0013_...md` — **false positive ที่รู้อยู่แล้ว** (จ่าหน้าจริง `ถึง: COO`, ยืนยันซ้ำโดย `h4mxrq`/
   `9emwkk`/`jbe8rr`/`8p7jon`/`6r13k5` ทุกรอบ) — เติม `.CONSUMED.txt` รอบนี้เพื่อปิดหนี้ marker เดียวกับที่ใบนี้
   เองรายงานไว้กับอีก 10 ใบ (จะได้ไม่ต้องอธิบายซ้ำทุกรอบอีก)
2. `20260905_0647_COO-DECISION-...md` — **จดหมายคำสั่งของรอบนี้เอง** ตอบด้วยไฟล์รอบนี้ + จดหมายถึง LANE-B
   ด้านล่าง ⇒ เติม `.CONSUMED.txt`

## งานที่ทำ — server ครึ่งของคิวเริ่มต้นข้อ 2/4

### `pirate-force-server` PR #802

`tests/test_damage_by_class_skill.py`: เพิ่มคลาสเทส `PerClassProductionPinAgainst916Tests` — ยิงทุกสกิลที่
`attack_skill_ids_for_class(class_id)` จัดว่าเป็นสกิลโจมตี (วันนี้ `(99,)` ทุกอาชีพ) ด้วย attacker จริงที่
production ใช้ (`mob_combat.pin_attacker()`) ใส่หุ่น Training Iron Man (`template_id 916`) ครบทั้ง 5 อาชีพ —
ได้ 891 ตรงกับที่ `damage_by_skill.py` เคยพิสูจน์ผ่าน gate สกิลเปล่าแล้ว ตอนนี้พิสูจน์ผ่าน gate อาชีพด้วย
(เดิมมีแต่เทสด้วย attacker สมมติ `Combatant(level=27, ...)` ซึ่งพิสูจน์แค่ว่า gate ส่ง attacker ผ่านไม่เปลี่ยนรูป
ไม่ใช่ตัวเลขที่ caller จริงจะได้)

`src/pirateforce_foundation/damage_by_class_skill.py`: อัปเดต docstring บันทึกการเพิ่มนี้ (ไม่มีโค้ด
production เปลี่ยน — โมดูลยัง zero production caller เหมือนเดิม)

**ไม่แตะ** `mob_combat.py`/`runtime.py`/`_dispatch_mob_combat` (เขต LANE-B) — จุดเสียบยังรอชื่อฟิลด์ skill id
จาก attended capture `GT-243`

### จดหมายถึง LANE-B

`notes_to_chief/20260905_0737_LANE-CS-TO-LANE-B-damage-formula-ready-to-wire-once-skill-id-field-is-known.md`
— ส่งมอบ `resolve_skill_damage`/`resolve_class_skill_damage`/`attack_skill_ids_for_class` พร้อมเสียบ อธิบาย
สถานะ `RE-240`/`GT-243` และจุดเสียบที่ `mob_combat.py` คอมเมนต์ไว้แล้ว — ไม่ได้ขอให้ B ลงมือตอนนี้ (ยังไม่รู้
ฟิลด์จริง)

## pf-adversary — ผลคืนแล้ว ไม่มี `ADVERSARY_PENDING`

สั่งทันทีหลังไฟล์แรกเขียนเสร็จ ตรวจในเวิร์กทรีแยก (`git worktree add --detach`) มิวเทชัน:
- `class_catalog.CLASS_IDS` → `()` และ `attack_skill_ids_for_class` → คืน `()` เสมอ — ทั้งคู่ทำให้เทสแดงทันที
  (`checked_a_class`/`assertTrue(attack_ids, ...)` จับได้) ⇒ **ไม่ผ่านแบบ vacuous**
- `mob_combat.resolve_damage` → `+1` — เทสแดงที่บรรทัดแรก (`892 != 891`) ⇒ **891 คำนวณสดจากสูตรจริง ไม่ใช่ก๊อป
  ตัวเลขจากไฟล์พี่น้องโดยไม่ตรวจ**
- ไม่มี mock ในคลาสเทสใหม่เลย · `Combatant` เป็น frozen dataclass property ล้วน ไม่มีผลข้างเคียงข้ามอาชีพในลูป ·
  รูปแบบ API ตรงกับที่ไฟล์เดียวกันใช้อยู่แล้วทุกจุด

**ไม่พบบั๊ก** — ไม่มีอะไรค้าง ⇒ ไม่มี `ADVERSARY_PENDING`

## ชุดเต็ม + preflight

`git fetch origin main` → ต้นไม้ตรงกับ `origin/main` (`ce97e1f`) อยู่แล้วก่อนคอมมิต → รันชุดเต็มครั้งเดียวติดกับ
push บนต้นไม้ที่ merge แล้ว:

```
python3 -m pytest -q
```

ผล: **`10636 passed, 327 skipped, 19765 subtests passed` (354.50s)** — เขียว

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS** (cp874 · ไม่มี
skip ใหม่ · main อยู่ใน branch แล้ว)

**ไม่มีไฟล์เทสใหม่รอบนี้** (แก้ไฟล์เทสเดิม `test_damage_by_class_skill.py` เพิ่มคลาส ไม่ใช่ไฟล์ใหม่) และไม่มี
skip ใหม่ ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census` แยกตามกฎ (เงื่อนไขคือ "เพิ่มไฟล์เทสใหม่ หรือเพิ่ม skip
ใหม่" เท่านั้น)

## งานสำรอง (ทำเมื่องานหลักติด) — ยังไม่ได้ลงมือรอบนี้ งานหลักไม่ติด

1. **[โค้ด]** จุดเสียบ `can_afford_to_learn` ให้ LANE-DB จริง — ตรวจซ้ำรอบนี้: `grep -rn skill_points
   src/pirateforce_foundation/persistence_*.py src/pirateforce_foundation/store.py` ยังไม่มีคอลัมน์ต่อตัวละคร
   จริง (มีแค่ชื่อในลิสต์ `persistence_attr_compose.py:394` ซึ่งเป็นคนละเรื่อง) — ยังบล็อกจริง ยกมาอีกรอบ
2. **[อ่าน/เทียบ — นับได้ไม่เกิน 1 ใน 3 ข้อ]** ทวนสารบัญคิวเริ่มต้นข้อ 1: `n_TARGET`/`n_EQUIPTYPE`/
   `n_EQUIPTYPE_LHAND` ใน `skill_catalog.py` ยังไม่มี accessor ชื่อจริง (ตรวจซ้ำจาก `6r13k5`) — ยังไม่มีเหตุผล
   RE ให้ตั้งชื่อ ยกมาอีกรอบ
3. **[ใบ GT/RE ที่รันได้]** เมื่อ `GT-243` capture ได้ผล (ยังไม่ถึง — ต้องเครื่อง Panya) เตรียม caller จริงของ
   `resolve_skill_damage`/`resolve_class_skill_damage` ตามฟิลด์ที่ผลชี้ทันที — ไม่ใช่ backup item จริงจนกว่าผล
   มา (ตามที่ `0013` ระบุไว้) แต่ระบุไว้กันลืม

## ขยับ NOW/M ข้อไหน

**ไม่ขยับขั้นบันได M** — `resolve_class_skill_damage`/`attack_skill_ids_for_class` ยัง zero production caller
เหมือนเดิม (grep ยืนยันรอบนี้: ไม่มีจุดเรียกใน `mob_combat.py`/`runtime.py`) รอ (ก) `GT-243` ชี้ฟิลด์ skill id
และ (ข) LANE-B/chief เขียนจุดเรียกใน `_dispatch_mob_combat` — **แต่เป็นความคืบหน้าจริงของคิวเริ่มต้นข้อ 4**
("สกิลโจมตีตัวแรกของแต่ละอาชีพ") ที่ `0647` สั่งให้เดินครึ่งเซิร์ฟเวอร์ต่อโดยเฉพาะ: พิสูจน์แล้วว่าทุกอาชีพยิงสกิล
โจมตีของตัวเองใส่สนามมาตรฐาน 916 ได้ตัวเลขถูกต้องตรงกับ production attacker จริง เหลือแค่จุดเสียบเฟรม (เขต B)
ไม่ใช่รอบว่างตาม `1450`/`0156` (โค้ด+เทสจริงขึ้น PR ไม่ใช่แค่อ่าน)

## ส่งอะไร

**pirate-force-server**: PR #802 (สาขา `claude/pensive-bardeen-gpxc2v`) —
`https://github.com/panyaasanee/pirate-force-server/pull/802`
- `tests/test_damage_by_class_skill.py` (+57 บรรทัด, คลาสเทสใหม่)
- `src/pirateforce_foundation/damage_by_class_skill.py` (docstring update)

**pf_bridge**: PR claim (แทนที่ด้วยไฟล์รอบนี้)
- จดหมายถึง LANE-B: `20260905_0737_LANE-CS-TO-LANE-B-damage-formula-ready-to-wire-once-skill-id-field-is-known.md`
- ปิด marker ใบ `0013`/`0647`

## nonclaims

- ไม่อ้างว่ามี production caller — ยัง zero production caller ทั้ง `damage_by_skill`/`damage_by_class_skill`
- ไม่อ้างว่า GT บนจอสนาม 916 พร้อมรัน — ยังบล็อกตาม NOW.md จนกว่า P-2 ปิด (เจ้าของ = LANE-GM/LANE-B)
- ไม่อ้างว่า LANE-B ต้องลงมือทันที — จดหมายเป็นการส่งมอบของพร้อมใช้ ไม่ใช่คำสั่งเปิดงานใหม่ให้ B
- ไม่อ้างว่ารู้ฟิลด์ skill id จริง — ยังรอ `GT-243` attended capture

## ติดอะไร / ใครปลด

- ไม่มีตัวบล็อกใหม่ต่อ CS เอง — งานหลักปิดสำเร็จภายในรอบเดียว ตามกำหนด `0647` (PR ≤09:06)
- ตัวบล็อกเดิมคงอยู่: `GT-243` ต้องเครื่อง Panya (ผู้ปลด = Panya/chief ตามคิว attended) · จุดเสียบ
  `_dispatch_mob_combat` เขต LANE-B (ผู้ปลด = LANE-B/chief เมื่อ `GT-243` มีผล)

-- LANE-CS
