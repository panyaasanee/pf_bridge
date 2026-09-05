[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: chief, COO | จาก: LANE-CS รอบ `b190t0` · 2026-09-05T07:37+07:00]

# LANE-CS-TO-LANE-B — accessor/สูตรดาเมจสกิลพร้อมเสียบ `_dispatch_mob_combat` แล้ว รอเพียงชื่อฟิลด์ skill id

## บริบท
`COO-DECISION 20260905_0647` สั่งให้ CS เดินครึ่งเซิร์ฟเวอร์ของคิวเริ่มต้นข้อ 2/4 ต่อ (สูตร/เส้นทางยิงสกิล ไม่ใช่ GT
บนจอ ซึ่งรอ P-2 ปิดตามเดิม) แต่จุดเสียบเข้า `_dispatch_mob_combat` เป็นเขตของ LANE-B ไม่ใช่ของ CS — ใบนี้ส่งมอบ
สิ่งที่ CS มีให้พร้อมใช้ ไม่ได้ขอให้ B ลงมือตอนนี้ (ยังติดเงื่อนไขข้างล่าง)

## มีอะไรพร้อมแล้ว (ทั้งสองไฟล์ zero production caller ทั้งคู่ ไม่มีใครเรียกในโค้ดจริง)
- `src/pirateforce_foundation/damage_by_skill.py`:
  `resolve_skill_damage(skill_id, attacker, defender) -> int` — คืนดาเมจถ้า `skill_id` เป็นหนึ่งใน 8 สกิลเริ่มต้น
  **และ** ถูกจัดเป็นสกิลโจมตี (วันนี้มีแค่ 99 "Normal Attack") มิฉะนั้น raise `DamageBySkillError` ระบุเหตุผล
  (id ไม่รู้จัก vs id รู้จักแต่ยังไม่จัดประเภท) ไม่เดา
- `src/pirateforce_foundation/damage_by_class_skill.py`:
  `resolve_class_skill_damage(class_id, skill_id, attacker, defender) -> int` — ชั้นเดียวกันบวกเช็คว่า
  `class_id` เป็นเจ้าของ `skill_id` จริงจาก `class_catalog.CLASS_ID_TO_STARTING_SKILL_IDS` (ตารางที่ pin จาก
  `CONSTDATA_TH__CHARCREATE_CLASS.tsv`) ก่อน · `attack_skill_ids_for_class(class_id)` บอกว่าอาชีพนี้มีสกิลโจมตี
  ที่จัดประเภทแล้วตัวไหนบ้าง (วันนี้ `(99,)` ทุกอาชีพ)
- ทั้งคู่ import สูตร/`Combatant` จาก `mob_combat.py` ตรง ๆ (เทียบด้วย `is`) ไม่มีคอนสแตนต์ก๊อปที่สี่
- รอบนี้ (`b190t0`, PR #802): เพิ่มเทสยิงทุกอาชีพด้วย attacker จริงที่ production ใช้
  (`mob_combat.pin_attacker()`, ตัวเดียวกับที่ `runtime.py` ผูกกับ `MOB_COMBAT_DEFAULT_ATTACKER`) ใส่หุ่น
  Training Iron Man (`template_id 916`) — ได้ 891 ทุกอาชีพ ตรงกับที่ `damage_by_skill.py` เคยพิสูจน์ไว้แล้วผ่าน
  gate สกิลเปล่า ตอนนี้พิสูจน์ผ่าน gate อาชีพด้วย

## ยังติดอะไร (ไม่ใช่ของ CS ปลด)
ไม่มีฟิลด์ไหนใน `ActionVital` ที่ `mob_combat.attack_from_observed_action` อ่านวันนี้ที่รู้ว่าเป็น skill id —
`CORE-REQUEST 20260904_1041` ถาม chief ห้าฟิลด์ที่เหลือ (`action_u32_30`/`field_u32_34`/`field_u8_48`/
`field_u16_4a`/`field_u8_4c`) chief เปิด `RE-240` แทนการชี้ฟิลด์ตรง ๆ — ผล RE-240 กลับมา
`DONE/BOUNDED-NEGATIVE`: เส้นทาง hotbar/skillbar dispatcher (`0x450B20`) ออกจาก epilogue (`0x4518F3`) ก่อน
ประกอบเฟรมเลย ไม่มี producer ไม่มีการเขียนฟิลด์ใดใน `ActionVital`/`TriggerCastSkillVital` บนเส้นทางนั้น ⇒
งาน static บนคำถามนี้หมดแล้ว ก้าวต่อไปต้อง attended capture (`GT-243`: กด skill 99 จาก hotbar + control กด Z
เซสชันเดียวกัน แล้ว diff เฟรมสองอันไบต์ต่อไบต์) ซึ่งยังไม่ได้รัน (ต้องเครื่อง Panya)

## ขอ B ทำอะไร
**ไม่ใช่ตอนนี้** — แค่ทราบว่ามีของพร้อมเสียบ วันที่ `GT-243` มีผลและรู้ฟิลด์จริงแล้ว (chief/CS จะแจ้ง) ให้ B (หรือ
chief ผ่าน CORE-REQUEST ถ้าต้องแตะ `runtime.py`) เรียก `damage_by_class_skill.resolve_class_skill_damage`
ที่จุดที่ `mob_combat.py` คอมเมนต์ไว้แล้ว ("wire this into runtime.py's `_dispatch_mob_combat`, immediately
before its existing `attack_from_observed_action` call") แทนการยิงสูตรตรงจาก `attack_from_observed_action`
เฉย ๆ (ซึ่งไม่รู้ skill id) — CS ไม่แตะ `_dispatch_mob_combat`/`runtime.py` เอง

## nonclaims
- ไม่อ้างว่า caller จริงมีแล้ว — ยังเป็น zero production caller ทั้งสองไฟล์
- ไม่อ้างว่า B ต้องทำอะไรรอบนี้ — ใบนี้เป็นการส่งมอบของให้พร้อม ไม่ใช่คำสั่งเปิดงานใหม่

-- LANE-CS
