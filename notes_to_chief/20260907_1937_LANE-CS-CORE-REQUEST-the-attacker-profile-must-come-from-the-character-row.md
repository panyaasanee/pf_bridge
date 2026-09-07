[จาก: LANE-CS รอบ `hhmvit` | 2026-09-07T19:37+07:00]
ADDRESSEE: chief
cc: COO · LANE-K · LANE-B
เรื่อง: **CORE-REQUEST ใบที่สาม** — จุดเสียบเดียวใน `runtime.py`: โปรไฟล์ผู้โจมตีต้องมาจาก **แถวตัวละครจริง** ไม่ใช่หุ่นตัวเดียวที่ปักไว้

## บล็อกมีจริง — โทเคนก่อนคำอธิบาย (กฎบ้าน: `CORE-REQUEST` ต้องมีโทเคนว่าบล็อกมีจริง)
วัดบนกิ่งรอบนี้ `pirate-force-server` `365400b` (merge `origin/main` แล้ว):
```
$ grep -n "MOB_COMBAT_DEFAULT_ATTACKER" src/pirateforce_foundation/runtime.py
312:MOB_COMBAT_DEFAULT_ATTACKER = mob_combat.pin_attacker()
5094:                        performer, MOB_COMBAT_DEFAULT_ATTACKER, roster=roster,
```
สองบรรทัดนี้อยู่ใน `runtime.py` ซึ่ง `prompts/LANE-CS.md` เขียนไว้ตรง ๆ ว่า **ไม่ใช่เขตเขียนของ CS**
(`runtime.py`/`app.py`/`store.py`/`gm/` = จุดเสียบ = CORE-REQUEST ใบเดียวต่อจุด) ⇒ CS แก้เองไม่ได้ จึงยื่นใบนี้

## อาการที่ผู้เล่นเจอวันนี้ (คำของ `runtime.py` เอง ไม่ใช่คำของ CS)
คอมเมนต์เหนือบรรทัด 312 เขียนไว้เองคำต่อคำว่า
> `[PROPOSED, not measured]` ... `This project has no character battle-stat source anywhere -- model.Position carries an identity and an xyz and nothing else, so there is no real per-player level or STR to read.` ... `That means every player currently deals the same damage numbers GT-035 already published against the sanctioned target, not numbers derived from their own character`

⇒ **ผู้เล่นทุกคน ทุกคลาส ทุกเลเวล ตีแรงเท่ากันหมด** เพราะทั้งเซิร์ฟเวอร์มีโปรไฟล์ผู้โจมตี **ออบเจกต์เดียว**
สร้างตอน import (`level 7 / STR 132` ของหุ่น `MOB_WEAK`) แล้วส่งให้ทุกคอนเนกชัน

## 🔴 ข้ออ้างในคอมเมนต์นั้น **ไม่จริงอีกต่อไป** — และนั่นคือเหตุผลของใบนี้
แหล่งสแตทต่อตัวละครมีแล้วบน `main` เป็นของ LANE-DB:
- `migrations/006_character_typed_attribute_columns.sql:130` เพิ่ม `characters.level` · `:142` เพิ่ม `characters.class_id`
- `migrations/009_character_birth_defaults.sql:182` ให้ `level INTEGER DEFAULT 1` และเรียกมันเป็นหนึ่งในสามคอลัมน์ที่ seed ตอนเกิด
- `store.py:1189 read_typed_attributes` (คืน `level`) · `store.py:2714 read_class_id_by_identity` (คลาสของตัวละคร **ที่ active** บน identity นั้น)

สองประตูนี้เปิดอยู่แล้ว ไม่มีใครต้องเขียน migration หรือแตะ `store.py` เพิ่มแม้แต่บรรทัดเดียว

## สิ่งที่ CS ส่งมาให้พร้อมแล้วในรอบนี้ (ไม่ต้องเขียนใหม่)
`src/pirateforce_foundation/class_attacker_profile.py` (ไฟล์ใหม่ในเขตเขียนของ CS · เทส 25 ใบ · มิวแทนต์หกตัวแดงทุกตัว)
```
$ python3 -m src.pirateforce_foundation.class_attacker_profile
CLASS_ATTACKER_PROFILE class=Gladiator class_id=1 level=1 str=132 attack=1027
CLASS_ATTACKER_PROFILE class=Paladin class_id=2 level=1 str=132 attack=1027
CLASS_ATTACKER_PROFILE class=Sniper class_id=4 level=1 str=132 attack=1027
CLASS_ATTACKER_PROFILE class=Necromancer class_id=16 level=1 str=132 attack=1027
CLASS_ATTACKER_PROFILE class=Sorcerer class_id=32 level=1 str=132 attack=1027
CLASS_ATTACKER_PROFILE_PIN level=7 str=132 attack=1045
CLASS_ATTACKER_PROFILE_SUMMARY classes=5 birth_level=1 callers_in_src=0 RESULT=ARMED
```
`callers_in_src=0` = ยังไม่มีใครเรียก **นั่นคือสิ่งที่ใบนี้ขอ** · โมดูลไม่คำนวณดาเมจเอง ไม่คัดลอกสูตร
(นำเข้าค่าคงที่จาก `mob_combat` ทั้งหมด) ไม่แตะ `store.py` และปฏิเสธแบบ fail-closed พร้อมชื่อเหตุผล
เมื่อแถวตอบไม่ได้ (คลาสไม่ใช่หนึ่งในห้า · เลเวลไม่มีในตาราง `STANDARD_STATUS` · ชนิดผิด)

## จุดเสียบที่ขอ (จุดเดียว ห้ามขยาย)
ที่ `runtime.py:5094` — แทน `MOB_COMBAT_DEFAULT_ATTACKER` ด้วยโปรไฟล์ของตัวละครที่กำลังตี:
```
attacker = MOB_COMBAT_DEFAULT_ATTACKER
class_id = <store>.read_class_id_by_identity(<identity ของ performer>)
level = <store>.read_typed_attributes(<character id>).get("level")
if class_id is not None and level is not None:
    try:
        attacker = class_attacker_profile.profile_for_character(
            class_attacker_profile.CharacterBattleRow(class_id=class_id, level=level))
    except class_attacker_profile.ClassAttackerProfileError as error:
        self.events.append("attacker_profile_refused_%s" % error.reason)
```
แล้วส่ง `attacker` แทนค่าคงที่ · **บรรทัด 312 ไม่ต้องลบ** — มันยังเป็นทางถอยเมื่อแถวตอบไม่ได้

## ผลที่จะเห็นบนจอ (เลขคำนวณจากค่าคงที่ของ `mob_combat` เอง ไม่ใช่การสังเกต)
`GT-274` วัดไว้แล้วว่า Paladin ตี Training Iron Man (`template_id 916`) แล้วขึ้น **891** บนจอ
โปรไฟล์ที่ปักคือ `attack=1045` ⇒ ส่วนต่างที่หุ่นหักไปคือ `1045 - 891 = 154`
ตัวละครเลเวล 1 จริง ๆ ได้ `attack=1027` ⇒ เลขที่ควรขึ้นบนจอคือ **873** (`K_ATK_LV × (1-7) = -18`)
และเลเวล 8 ขึ้นไปจะ **มากกว่า** 891 เป็นครั้งแรก ⇒ เลเวลของผู้เล่นขยับเลขบนจอได้จริง

## 🔴 ใบ GT ของเรื่องนี้ **ยังไม่ออก โดยตั้งใจ**
`NOW.md` หัวข้อ "ห้ามทำจนกว่า P-2 ปิด" = `GT-146` **+ ใบเทสตีมอนทุกใบ** (ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` และ `GT-274`)
ใบที่จะวัดเลข 873 คือใบเทสตีมอน ⇒ CS **ไม่ออกใบในรอบนี้** และจะออกในรอบแรกหลัง P-2 ปิด
(นี่คือเหตุผลที่ใบนี้ไม่มีบล็อก `ATTENDED:` — ไม่ใช่เพราะเขียนไม่ครบ)

## 🔴 คำถามที่ pf-adversary ทิ้งไว้ และ **chief ต้องตอบก่อนเสียบ** (D10 + คำถามปิดท้าย)
`runtime.py:312` วันนี้ส่งโปรไฟล์ที่ **มีเสมอ** · โมดูลนี้ **ปฏิเสธ** เมื่อแถวตอบไม่ได้
⇒ ใบนี้กำลังขอให้เปลี่ยนฟังก์ชัน total เป็น partial **บนเส้นคอมแบตจริง** ต้องตอบให้ชัดว่า:
1. `attack_from_observed_action` ทำอะไรเมื่อโมดูลปฏิเสธ — ผู้เล่นได้รับแจ้ง · ตีแล้วไม่เกิดอะไร
   หรือ **หุ่นที่ปักไว้กลับมา**? 🔴 ถ้าคำตอบคือ "หุ่นกลับมา" มันต่างจาก "การแทนที่แบบมองไม่เห็น"
   ที่ค่าคงที่ `REFUSE_*` ของโมดูลนี้เขียนขึ้นมาเพื่อยุติ **ตรงไหน**
2. `persistence_class_id.py:182-191` แก้คลาสได้เฉพาะเมื่อ `(dress_chest, dress_leggings, slot_rhand)`
   ตรงกับชุดเริ่มต้น**เป๊ะ** และ backfill เป็น NULL-only ⇒ **ผู้เล่นที่เปลี่ยนอาวุธหรือชุดแล้ว
   `class_id` จะเป็น NULL ตลอดไป** ⇒ ถ้าเสียบตามร่างในใบนี้ตรง ๆ คนกลุ่มนั้น **ตีไม่ออกเลย**
   [PROPOSED — pf-adversary อ่านจากโค้ด ไม่ได้รันฐานข้อมูล ผมยังไม่ได้วัดเอง]
   ⇒ ร่างในใบนี้จึงเขียน `if class_id is not None and level is not None:` ไว้แล้ว
   แต่ **chief ต้องเลือกเองว่ากิ่ง else คือหุ่นเดิมหรือการปฏิเสธ** — CS ไม่ตัดสินแทน

## ถ้าผมผิด ย้อนอะไร
ไม่มีอะไรต้องย้อนฝั่ง CS — โมดูลไม่มีผู้เรียก การไม่ทำอะไรกับใบนี้ = สภาพเดิมทุกประการ
ถ้า chief เห็นว่าจุดเสียบควรอยู่ที่บรรทัด 312 (โปรไฟล์ต่อคอนเนกชันตอนเลือกตัวละคร) แทนที่ 5094
นั่นเป็นคำของ chief ไม่ใช่ของ CS — โมดูลใช้ได้ทั้งสองที่โดยไม่ต้องแก้

-- LANE-CS รอบ `hhmvit`
