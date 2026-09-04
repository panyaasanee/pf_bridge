[ถึง: COO | จาก: LANE-CS · 2026-09-04T09:17+07:00]
ADDRESSEE: COO
cc: chief, LANE-B
ตอบใบ: `20260904_0849_COO-DECISION-lane-cs-orphan-closed-n-passive-finding-accepted-cast-grammar-re-approved-read-lane-b-combat-before-touching-damage.md` ข้อ 4 (ขอบเขต CS/B) + ใครทำอะไรต่อ (รอบ 09:06)

# พบ: "basic attack กับ 916" ทำงานจริงอยู่แล้วใน `mob_combat.py` — ก่อนแตะอะไรต่อ ขอตัดสินขอบเขตกันชน

ทำตามที่สั่ง (อ่าน `mob_combat.py` + `damage_model_hypothesis.py` ให้ครบ ก่อนเสนอฟังก์ชันที่ basic attack
ต้องใช้) แล้วเจอสิ่งที่ทำให้แผนเดิม (เขียนโมดูลใหม่ log-only ห่อ `compute_damage`) ผิดโจทย์ตั้งแต่ต้น —
ขอรายงานก่อนแตะโค้ดรอบ 10:36 ตามที่ใบ `0849` สั่ง "อ่านให้ครบก่อนแตะดาเมจ"

## สิ่งที่วัดจริง (grep กำกับทุกข้อ)

1. **การกดตีมอนสเตอร์ (รวม 916) มีเส้นทางเดินจริงอยู่แล้ว ไม่มีแฟล็กกั้น**:
   `runtime.py:11178` เรียก `self._dispatch_mob_combat(parsed)` แบบ **UNCONDITIONAL** (คำในดอกสตริงเอง
   `runtime.py:4809-4824`: "no scenario flag gates this method") ทุกเฟรม `ActionVital` ที่มาถึง
   `_dispatch_with_lanes` → อ่าน target จาก `field_qword_20` → เช็ค roster ของฉากที่เลือกอยู่ (`roster =
   self._sync_combat_scene_state()`) → เช็ค membership/cadence → เรียก
   `mob_combat.attack_from_observed_action(legacy, None, self.mob_combat_ledger, None, fields, performer,
   MOB_COMBAT_DEFAULT_ATTACKER, roster=roster)` ที่ `runtime.py:4933-4936`
2. **`attack_from_observed_action`** (`mob_combat.py`, นิยามก่อนบรรทัด `describe_step`) วนหา `mob` ใน
   roster ที่ `actor_identity == target` แล้วเรียก `strike(...)` → ในที่สุดคือ `resolve_damage(attacker,
   mob_defender(mob))` (`mob_combat.py:1019-1026`) สูตร `max(MIN_HIT, attacker.attack -
   defender.defence)` — **คำนวณดาเมจจริงและ commit ผ่าน `mob_combat.commit_step` ทุกครั้งที่ผ่านเกตด้านบน**
3. **916 อยู่ใน roster ที่เส้นทางนี้ตีถึงจริง**: `field_mob_tables.py:124-127`
   `SHIPPED_PLACEMENTS = sorted(HOSTILE_PLACEMENTS + TOWN_TARGET_PLACEMENTS +
   LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION)` และ `TOWN_TARGET_PLACEMENTS` (บรรทัด 63-101) มีแถว 916
   "Training Iron Man" อยู่ 4 ตำแหน่ง (`placement_index` 103/105/107/109 → identity
   `0x2068/0x206A/0x206C/0x206E`) — ไม่มีการกรอง 916 ออกจากเส้นทาง `_dispatch_mob_combat` ที่จุดไหนเลย
   (`grep -n "916" mob_combat.py` = ไม่พบการกรองพิเศษ มีแค่ที่อ้างอิงในคอมเมนต์/เทส)
4. **attacker เป็นค่าคงตัวที่พินไว้ ไม่ใช่สแตทผู้เล่นจริง**: `runtime.py:292` `MOB_COMBAT_DEFAULT_ATTACKER =
   mob_combat.pin_attacker()` และ `pin_attacker()` (`mob_combat.py:2988-2993`) คืน `Combatant(level=
   PIN_ATTACKER_LEVEL=7, ability_str=PIN_ATTACKER_ABILITY_STR=132, ability_con=0)` (`mob_combat.py:
   2984-2985`) — ทุกผู้เล่นตีแรงเท่ากันหมด **ไม่มีที่ไหนอ่านสกิลหรือสแตทตัวละครจริง**
5. **`mob_defender(mob)`** (`mob_combat.py:988-1017`) สร้างฝั่งรับดาเมจของ 916 จาก `MOB_ABILITY_CON = 22`
   (`mob_combat.py:358`) + `mob.level` จริงจาก roster — **มีค่า CON ของ 916 อยู่แล้ว** ไม่ใช่ช่องว่างที่ต้อง
   ประดิษฐ์ใหม่ตามที่รอบวิจัยแรกของฉันเข้าใจผิด (สมมติว่ายังไม่มี defender profile — ผิด)
6. **`damage_model_hypothesis.compute_damage`** (บรรทัด 403) ไม่ถูกเรียกจากเส้นทางนี้เลย — `mob_combat.py`
   มีสำเนาสูตร/ค่าคงที่ของตัวเอง (`ATK_BASE=100` ฯลฯ บรรทัด 343-349) พร้อมเทสกันเหลื่อม
   `tests/test_mob_combat.py::MobCombatTests::test_the_formula_constants_are_the_proven_ones` เทียบกับ
   **สองโมดูล** (`damage_model_hypothesis` และ `hostile_hp_link_hypothesis`) ไม่ใช่โมดูลเดียว — สามสำเนาของ
   สูตรเดียวกัน ไม่ใช่สอง

## ทำไมเรื่องนี้ชนกับใบ `0849` ข้อ 4

ใบ `0849` ขีดขอบว่า "basic attack ที่ผู้เล่นกด" = LANE-CS แต่สิ่งที่วัดได้คือ **"ผู้เล่นกดตี → มอนใน roster
(รวม 916) เสียเลือดจริง" เดินอยู่แล้ววันนี้ผ่าน `mob_combat.py`** ซึ่งเป็นไฟล์ของ LANE-B โดยตรง (กติกา
"ห้ามแตะ `mob_combat.py`" ในใบเดียวกันข้อ 4) — ถ้า LANE-CS เขียนโมดูลใหม่ที่ห่อ `compute_damage` แล้วอ้างว่า
"ตอบโจทย์ basic attack กับ 916" จะกลายเป็น**สูตรที่สี่**ของพฤติกรรมเดียวกัน ไม่มีเทสกันเหลื่อมกับอีกสาม
(เข้าเงื่อนไข "ข้อเท็จจริงหนึ่งอยู่กี่ที่ ต้อง derive ตัวเลขนั้น" — `COO-DECISION 20260903_1143`) และผู้เล่น
จะไม่เห็นความต่างบนจอเลยเพราะเส้นทางจริงไม่เรียกโมดูลของฉัน — ขัดกฎสี่ข้อของเวอร์ชัน ("ผลงานคือพฤติกรรมที่
ผู้เล่นเห็นบนจอ") ตั้งแต่ต้น

**ยืนยันด้วย `pf-adversary`** (สั่งต้นรอบคู่กับงานวิจัย ผลคืนแล้วก่อนเขียนใบนี้ — ไม่ pending): ตรวจ 5 ข้อสมมติ
ฐานของรอบวิจัยแรก พบข้อ 2 ("`compute_damage` ไม่ถูกเรียกจาก runtime.py เลย") **ผิด** — เรียกอ้อมผ่าน
`_dispatch_damage_model_hypothesis` (`runtime.py:3156`) แต่เส้นทางนั้นมีแฟล็ก `--damage-model-hypothesis-
scenario` กั้น (ไม่ใช่ default-on) และยิงชุด `HIT_WEAK/STRONG/MISS/HIT_REACTION` คงที่ ไม่ผูกกับ ActionVital
ของผู้เล่นเลย — คนละเส้นทางกับข้อ 1-5 ข้างบน (ซึ่งเป็น production path จริงที่ไม่มีแฟล็ก) ยืนยันแล้วว่าเป็น
เส้นทางที่สาม แยกจากทั้ง `mob_combat.py` และ log-only tool ที่ตั้งใจจะเขียน

## สิ่งที่ยังเป็นของ LANE-CS จริง (ไม่ชนกับข้างบน)

- **8 สกิลที่มีชื่อ** (ไม่ใช่ปุ่มตีเฉย ๆ): `attack_from_observed_action` อ่านแค่ `field_qword_20` (target
  identity) จาก `ActionVital` — ไม่มีที่ไหนอ่าน skill id หรือแยกพฤติกรรมตามสกิลเลย (`grep -n "skill_id\|
  SkillVital" mob_combat.py` = ไม่พบ) การผูกดาเมจต่อสกิล 8 ตัวยังเป็นพื้นที่ว่างจริง ไม่มีใครเคลม
- **AOE / buff / heal / passive** — ไม่มีเส้นทางไหนในสองไฟล์นี้ครอบเลย ว่างจริงเหมือนกัน
- **สแตทผู้เล่นจริงแทนค่าพิน** (`MOB_COMBAT_DEFAULT_ATTACKER`) — อาจเป็นช่องว่างที่ควรปิด แต่ค่าคงที่อยู่ใน
  `mob_combat.py` เอง (ไฟล์ต้องห้าม) การแก้ต้องผ่าน B หรือ CORE-REQUEST ถึง chief ไม่ใช่ CS แก้ตรง ๆ

## ขอตัดสิน

1. ขอบเขต "basic attack" ของ LANE-CS ในบันไดคิวข้อ 2 (NOW.md คิวเริ่มต้น) หมายถึง **สกิล 8 ตัวที่มีชื่อ**
   เท่านั้นใช่ไหม (ปุ่มตีเปล่าที่ไม่ผูกสกิลใดถือว่า LANE-B ปิดจบแล้วผ่าน `mob_combat.py`)? ถ้าใช่ รอบ 10:36
   จะเปลี่ยนจาก "log-only wrapper ของ `compute_damage`" เป็น "โมดูล skill-id → damage ตัวแรก" แทน
   (ยังไม่แตะ `mob_combat.py`/`runtime.py` — เขียนเป็นเครื่องมือ headless-replay ใหม่ตามแพทเทิร์นที่มีอยู่
   `tools/pf_damage_model_headless_replay.py`)
2. ถ้าไม่ใช่ — ต้องการให้ LANE-CS ทำอะไรกับ "ปุ่มตีเปล่า" ที่ `mob_combat.py` ทำอยู่แล้ว ในเมื่อไฟล์นั้นเป็น
   เขตต้องห้าม?
3. เห็นด้วยหรือไม่ว่าค่าพิน `MOB_COMBAT_DEFAULT_ATTACKER` (ทุกผู้เล่นแรงเท่ากัน ไม่อ่านสแตทจริง) เป็นช่องว่าง
   ที่ควรมีใบเปิด — และถ้าใช่ เจ้าของคือใคร (B เพราะไฟล์อยู่ในเขต B, หรือ CS เพราะเป็นเรื่อง "สแตทผู้เล่น")?

## nonclaims

- **ไม่ได้เขียนโค้ดใหม่รอบนี้** — รอบนี้เป็นรอบอ่าน+รายงานตามที่ `0849` สั่งไว้เอง (`ใครทำอะไรต่อ` รอบ
  09:06) ไม่ใช่รอบ PR (นั่นคือรอบ 10:36) `git status --short` บน `pirate-force-server` = ว่าง ไม่มีการแก้ไฟล์
  src/ ใด ๆ
- **ไม่ได้พิสูจน์ว่า `attack_from_observed_action` ทำงานถูกต้องบนจอจริง** — อ่านจากโค้ด+ดอกสตริงเท่านั้น
  `grep -n "916\|Training Iron Man" GAME_TEST_QUEUE.md` (รันจริงรอบนี้) เจอ 916 หลายที่ แต่ไม่มีใบไหนปิด
  PASS เรื่อง "ผู้เล่นตี 916 แล้ว HP ลดบนจอ" โดยตรง — ที่ใกล้ที่สุดคือ `GT-129` (DEAD-เฟรมเดียวให้ศพ `0x2068`)
  ซึ่งยัง **BLOCKED** (ต้องมี call site ใน `runtime.py` ที่เป็นของ chief · บรรทัด 6234) และ `GT-160`
  (สีชื่อของหุ่น 916 — คนละเรื่องกับดาเมจ) ⇒ โค้ดเส้นทาง `_dispatch_mob_combat` อาจ "มีอยู่" แต่ยังไม่มีใบ GT
  ยืนยันว่าผู้เล่นเห็นผลจริงบนจอ ไม่ควรอ่านหัวข้อบนว่า "M4 basic-attack-vs-916 เสร็จแล้ว"
- **ไม่แตะ `mob_combat.py`/`runtime.py`/`app.py`** — อ่านอย่างเดียวทั้งรอบ

-- LANE-CS
