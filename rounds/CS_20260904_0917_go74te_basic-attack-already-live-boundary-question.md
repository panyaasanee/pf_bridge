# CS round go74te — basic attack vs. 916 is already live in mob_combat.py; boundary question sent to COO

เวลาเริ่ม 2026-09-04 09:14 +07:00 · เวลาปิด 2026-09-04 09:17 +07:00 · claim `pf_bridge#1093`

## ขยับ NOW/M ข้อไหน

- คิวเริ่มต้นข้อ 2 (Basic attack + Training Iron Man `916`) — **รอบนี้เป็นรอบอ่าน+รายงานตามที่ใบ
  `0849` สั่งไว้เอง** (ใครทำอะไรต่อ รอบ 09:06: "อ่าน `mob_combat.py` + `damage_model_hypothesis.py` ให้ครบ
  ... ส่งไฟล์รอบระบุว่า basic attack ที่ Training Iron Man `916` ต้องใช้ฟังก์ชันไหน") — ทำครบตามสั่ง แต่
  คำตอบที่ได้ไม่ใช่ "ใช้ฟังก์ชัน X" อย่างเดียว เพราะพบว่าเส้นทางนั้นมีอยู่แล้วในเขตของ LANE-B (ดูล่าง) จึง
  **ไม่ขยับ M ใด ๆ รอบนี้ — ส่งจดหมายขอตัดสินขอบเขตแทนก่อนเปิด PR รอบ 10:36 ตามแผนเดิม**
- ไม่ขยับ M2/M3/M4/M5 · ไม่แตะ RE `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` (รอ chief ตั้งเลขตามใบ `0849` ข้อ 3)

## ส่งอะไร

- **pf_bridge**: ไฟล์นี้ (แทน `rounds/CS_go74te_claim.md` — ลบไฟล์ claim เดิม) · จดหมายใหม่
  `notes_to_chief/20260904_0917_LANE-CS-TO-COO-basic-attack-vs-916-already-live-in-mob-combat-boundary-question.md`
  (`ADDRESSEE: COO`) · consume `20260904_0849_...md` (`.CONSUMED.txt` วางแล้ว)
- **pirate-force-server**: ไม่มี — รอบนี้ไม่แก้ไฟล์ใด ๆ ในรีโปนั้น (`git status --short` = ว่าง อ่านอย่างเดียว
  ทั้งรอบ)

## สิ่งที่ทำจริงรอบนี้

1. อ่าน `damage_model_hypothesis.py` (1613 บรรทัด), `mob_combat.py` (3070 บรรทัด) และห้าโมดูล hypothesis ที่
   โอนมา (`tools/pf_damage_hit_result_static.py`, `damage_hp_link_hypothesis.py`,
   `pf_damage_hp_link_headless_replay.py`, `pf_damage_model_headless_replay.py`,
   `stats_progression_hypothesis.py`) ผ่าน agent วิจัยรอบแรก แล้วตรวจซ้ำเองด้วย `grep`/`sed -n` ตรง ๆ
2. สั่ง `pf-adversary` ต้นรอบคู่กับงานวิจัย (รีวิวข้อสรุปของรอบวิจัยแรก) — **ผลคืนแล้วก่อนเขียนไฟล์นี้ ไม่
   pending** — จับได้ว่าข้อสรุป "compute_damage ไม่ถูกเรียกจาก runtime.py เลย" ผิด (เรียกอ้อมผ่าน
   `_dispatch_damage_model_hypothesis`, `runtime.py:3156`, แต่มีแฟล็กกั้น) และชี้ว่า `mob_combat.py` มี
   เส้นทางคำนวณ+ใช้ดาเมจจริงกับผู้เล่นตี 916 อยู่แล้ว ไม่มีแฟล็กกั้น — เป็นจุดที่พลิกแผนทั้งรอบ
3. ตรวจซ้ำด้วยตัวเอง (ไม่เชื่อ adversary อย่างเดียว) ว่าข้อค้นพบนั้นจริง — ดูหัวข้อถัดไป

## ข้อค้นพบหลัก (grep กำกับ วัดเองซ้ำ ไม่ใช่แค่เชื่อ agent)

- `runtime.py:11178` เรียก `self._dispatch_mob_combat(parsed)` **UNCONDITIONAL** ทุกเฟรม `ActionVital`
  (ดอกสตริง `runtime.py:4809-4824`: "no scenario flag gates this method")
- เส้นทางนั้นจบที่ `mob_combat.attack_from_observed_action(...)` (`runtime.py:4933-4936`) → `strike(...)` →
  `resolve_damage(attacker, mob_defender(mob))` (`mob_combat.py:1019-1026`, สูตร `max(MIN_HIT,
  attacker.attack - defender.defence)`) → commit ผ่าน `mob_combat.commit_step`
- Training Iron Man `916` อยู่ใน roster ที่เส้นทางนี้ตีถึง: `field_mob_tables.py:124-127`
  `SHIPPED_PLACEMENTS = sorted(HOSTILE_PLACEMENTS + TOWN_TARGET_PLACEMENTS + ...)` มี 916 สี่ตำแหน่ง
  (`placement_index` 103/105/107/109 → identity `0x2068/0x206A/0x206C/0x206E`) ไม่มีจุดกรอง 916 ออก
- attacker เป็นค่าพินคงตัว ไม่ใช่สแตทผู้เล่นจริง: `runtime.py:292` `MOB_COMBAT_DEFAULT_ATTACKER =
  mob_combat.pin_attacker()` → `pin_attacker()` (`mob_combat.py:2988-2993`) คืน `level=
  PIN_ATTACKER_LEVEL=7, ability_str=PIN_ATTACKER_ABILITY_STR=132` (`mob_combat.py:2984-2985`) — ไม่มีที่
  ไหนอ่านสกิลหรือสแตทตัวละครจริงเลย
- `mob_defender(mob)` (`mob_combat.py:988-1017`) มี CON ของ 916 อยู่แล้วจาก `MOB_ABILITY_CON = 22`
  (`mob_combat.py:358`) — **ไม่ใช่ช่องว่างที่ต้องประดิษฐ์ใหม่** (รอบวิจัยแรกเข้าใจผิดว่ายังไม่มี defender
  profile — แก้ตรงนี้แล้ว)
- `damage_model_hypothesis.compute_damage` (บรรทัด 403) เป็นสูตรที่**สาม**ที่แยกกัน ไม่ถูกเรียกจากเส้นทาง
  ด้านบนเลย — `mob_combat.py` มีสำเนาค่าคงที่ของตัวเอง (`ATK_BASE=100` ฯลฯ บรรทัด 343-349) พร้อมเทสกัน
  เหลื่อม `tests/test_mob_combat.py::MobCombatTests::test_the_formula_constants_are_the_proven_ones` เทียบ
  กับ**สองโมดูล** (`damage_model_hypothesis` + `hostile_hp_link_hypothesis`) — สามสำเนาของสูตรเดียวกัน

## ทำไมถึงหยุดแล้วเขียนจดหมายแทนเปิด PR

ใบ `0849` ข้อ 4 ขีดขอบว่า "basic attack ที่ผู้เล่นกด" = LANE-CS และ "ห้ามแตะ `mob_combat.py`" (เขตของ B)
พร้อมกัน — แต่สิ่งที่วัดได้คือ "ผู้เล่นกดตี → มอนใน roster (รวม 916) เสียเลือดจริง" เดินอยู่แล้ววันนี้**ผ่าน
`mob_combat.py` เอง** ถ้าเขียนโมดูลใหม่ log-only ห่อ `compute_damage` ตามแผนเดิมของรอบวิจัยแรก จะกลาย
เป็น**สูตรที่สี่**ของพฤติกรรมเดียวกัน ไม่มีเทสกันเหลื่อมกับอีกสาม (ขัด `COO-DECISION 20260903_1143`:
"ข้อเท็จจริงหนึ่งอยู่กี่ที่ ต้อง derive ตัวเลขนั้น") และผู้เล่นจะไม่เห็นความต่างบนจอเลยเพราะเส้นทางจริงไม่
เรียกโมดูลของฉัน — ขัดกฎสี่ข้อของเวอร์ชันตั้งแต่ต้น ("ผลงานคือพฤติกรรมที่ผู้เล่นเห็นบนจอ") จึงหยุดก่อนเปิด PR
รอบ 10:36 แล้วส่งจดหมายขอตัดสินขอบเขตแทน (เนื้อหาเต็ม →
`notes_to_chief/20260904_0917_LANE-CS-TO-COO-...md`)

พื้นที่ที่ยังเป็นของ LANE-CS จริง ไม่ชนกับข้างบน (เสนอไว้ในจดหมายเดียวกัน รอ COO ยืนยัน): **สกิลแปดตัวที่มี
ชื่อ** — `attack_from_observed_action` อ่านแค่ `field_qword_20` (target identity) จาก `ActionVital` ไม่มี
ที่ไหนอ่าน skill id หรือแยกพฤติกรรมตามสกิล (`grep -n "skill_id\|SkillVital" mob_combat.py` = ไม่พบ) และ
AOE/buff/heal/passive ก็ว่างเหมือนกัน

## pf-adversary

**ไม่ pending** — สั่งต้นรอบ ผลคืนแล้วก่อนเขียนไฟล์นี้ (ดูหัวข้อ "สิ่งที่ทำจริงรอบนี้" ข้อ 2) รายละเอียดเต็ม
อยู่ในจดหมายถึง COO

## nonclaims (grep กำกับตามกฎ)

- **ไม่ได้เขียนโค้ดใหม่รอบนี้** — `git status --short` บน `pirate-force-server` (ที่ `HEAD` =
  `ecfeec554948fc68c1ae8a5708e4f2b8bbb13451`, `git fetch origin main` แล้ว) = ว่าง ไม่มีการแก้ไฟล์ `src/`
  ใด ๆ
- **ไม่ได้พิสูจน์ว่า `attack_from_observed_action` ทำงานถูกต้องบนจอจริง** — `grep -n "916\|Training Iron
  Man" GAME_TEST_QUEUE.md` (รันจริงรอบนี้) เจอหลายที่แต่ไม่มีใบไหนปิด PASS เรื่อง "ตี 916 แล้ว HP ลดบนจอ"
  โดยตรง ที่ใกล้ที่สุดคือ `GT-129` (DEAD-เฟรมเดียว) ยัง **BLOCKED** (ต้องมี call site ใน `runtime.py` ของ
  chief) — โค้ดเส้นทางนี้ "มีอยู่" แต่ยังไม่มีใบ GT ยืนยันผลบนจอ ห้ามอ่านว่า M4-vs-916 เสร็จแล้ว
- **ไม่แตะ `mob_combat.py`/`runtime.py`/`app.py`/`store.py`/`gm/`** — อ่านอย่างเดียวทั้งรอบ
- **ไม่ได้ถอด `s_CAST_CONDITION`/`s_CAST_BEHAVIOR`** — รอ chief ตั้งเลขตามใบ `0849` ข้อ 3

## ติดอะไร / ใครปลด

**ติดจุดเสียบ/ข้ามเขต** — ขอบเขต "basic attack" ของ LANE-CS ทับซ้อนกับเส้นทางที่มีอยู่แล้วใน `mob_combat.py`
(เขต LANE-B) ส่งจดหมายขอตัดสินสามข้อถึง COO แล้ว (`20260904_0917_LANE-CS-TO-COO-...md`) — รอคำตอบก่อนเปิด
PR รอบ 10:36 ตามแผนที่ใบ `0849` วางไว้
