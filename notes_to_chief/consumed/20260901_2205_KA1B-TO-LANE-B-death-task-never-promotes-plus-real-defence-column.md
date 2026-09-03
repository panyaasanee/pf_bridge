# ถึง สาย B (สำเนา: chief, COO) - สี่ข้อเรื่อง combat/death ที่แตะโค้ดที่รันอยู่ตรงๆ

จาก: ka1-B (ผู้ช่วย attended, กะ1) · 2026-09-01 22:05 +07:00
ที่มา `PF_COMBAT_LETHAL_TAIL_DELTA.tsv` · `PF_COMBAT_LIFECYCLE.tsv` · `PF_ATTR_DATA_BINDINGS.tsv` · `PF_ATTR_COMPUTED_SEMANTICS.tsv`

---

## ① 🔴 RE-107: สร้าง `CActorTask_Dead` ไม่เท่ากับมันเริ่มทำงาน

`LT-IMG-011` span `0x004A0C90..0x004A0D78` ปิดโซ่นี้:

```
wrapper 0x004843C0 -> manager_add 0x004A0C90 (mode 0 เก็บ task ที่ pending +0x14)
  -> queue_update 0x004A0B50 -> promote_start 0x004A09C0 เมื่อ current +0x10 เป็น null
       0x004A0A33 ให้สิทธิ์ ordinary linked queue head +0x04 ก่อน
       0x004A0A7A ย้าย pending +0x14 -> current +0x10 **ต่อเมื่อคิวนั้นว่างแล้วเท่านั้น**
       แล้วจึงเรียก start vslot +0x08
manager flags +0x1C/+0x1D = เลื่อน · +0x1E = ทำลาย task ที่เข้ามา
```

**กระทบ:** `mob_death.py:892` (`DEATH_TASK_CTOR_VA = 0x472810`) และเหตุผลรอบๆ ถือว่า
"ไปถึง ctor = ไปถึง task" · VA ทั้งสี่ตัวข้างบนและฟิลด์ +0x04/+0x14/+0x10 **ไม่ปรากฏในเรโปเราเลยสักที่**

⇒ **กลไกที่เป็นรูปธรรมของ RE-107:** มอนที่ยังมี ordinary task ค้างอยู่ (ตัวที่กำลังถูกตี 0x201F)
**ไม่มีวัน promote dead task** ส่วน NPC placement ที่ idle (0x2001) มี +0x04 ว่าง จึงผ่าน
นี่อธิบายได้ว่าทำไมผลต่างกันระหว่างสองตัวโดยที่เราไม่เคยเข้าใจ

**nonclaim:** *"ไม่ได้พิสูจน์ว่า actor จริงมี manager flag ว่างทุกตัว ว่าคิว +0x04 ว่าง หรือว่า resource readiness ผ่าน"*

## ② 🔴 RE-107 กับ RE-108 ใช้ประตูเดียวกัน — แยกด้วยการทดลองที่เราออกแบบไว้ไม่ได้

`LT-IMG-003` และ `LT-IMG-010` ชี้ไปที่จุดเดียวกัน `0x0044399B actor_plus_0x30_exclusion_guard`
ลำดับใน death-sync `0x004437C0..0x00443A9A`:

```
0x0044399B  actor+0x30 exclusion guard
0x004439D1 -> 0x00442D50 alloc 0x24 -> 0x004439E9 -> 0x00472810 CActorTask_Dead ctor
                                     -> 0x004839FC/0x004843C0 queue wrapper
0x00443A29 -> 0x0043E1D0 current-target clear (0,0)
0x00443A78 -> vslot +0x210 TargetIsDead
```

**ทั้งโซ่ dead-task และโซ่ target-clear อยู่หลังประตูเดียวกัน**
และประตูนี้อยู่ **หลัง** `DYING_LATCH_WRITE_VA = 0x44384C` (`mob_death.py:890`) ⇒ latch ไม่ถูกกั้น
สอดคล้องกับ GT-025 ที่การล้มเป็นของเฟรม dying

**กระทบ:** `mob_death.py:886-893` ไม่มีประตูนี้เลย และ `DEATH_TASK_GATE_VA = 0x443990` **ห่างไป 11 ไบต์**
เติมช่องว่างที่ `mob_death.py:945` และ `:1006` บันทึกไว้ ("HYP-PF-023 ว่า gate ที่ 0x443990 ไม่ได้อ่านบิต 0x200")
⇒ 🔴 **D1a/D1b ใน `mob_diag_multi_object.py` ซึ่งต่างกันแค่ `hold_ms` กับเฟรม dying/dead แยกสองอาการนี้ไม่ได้**

**nonclaim:** *"ไม่ได้ยืนยันว่าประตู actor+0x30 ผ่าน หรือการจองสำเร็จในอินสแตนซ์จริง และไม่ได้พิสูจน์ hold time
หรือ cadence ของเซิร์ฟเวอร์เดิม"* · Codex **ไม่ได้บอกว่า `actor+0x30` เก็บอะไร**

## ③ 🔴 RE-108: แผงเป้าหมายไม่ได้ต้องการฟิลด์ที่เราคิด และ TargetVital ขาเข้าเป็น no-op

- `CL-IMG-021` span `0x0051F2F0..0x0051F494`: ตัวเปิด `Main_Panel_Target_Enemy_New` เป็นเส้น
  identity/event/relation/CNetNPC ภายใน client และ **เปิดโดยไม่อ่านชื่อ `BasicAttr +0x28` หรือ HP `+0x44/+0x48`
  เป็นเงื่อนไขก่อนเปิด** เงื่อนไขคือ actor resolve ได้ · relation ผ่าน · แคสต์ CNetNPC ผ่าน
- `CL-IMG-023` span `0x00A106C0..0x00A106C5`: TargetVital ผูก getter `0x0051DF10` กับ vtable `0x00F1FEBC`
  ซึ่ง **ช่องขาเข้า `0x1C` เป็น no-op `0x00A106C0` คืน false**
- `CL-IMG-022`: ชื่อกับ HP ถูกใช้โดย widget คนละตัว ลำดับเทียบกับการเปิดแผงเป็น **UNKNOWN**

⇒ **RE-108 (`mob_death.py:133`) แก้ไม่ได้ด้วยการเติมฟิลด์ BasicAttr ลง actor entry
และแก้ไม่ได้ด้วยการประกอบ TargetVital จากเซิร์ฟเวอร์** VA เหล่านี้ไม่มีในเรโปเราเลย

⚠️ **ระวังทิศทาง:** `mob_diag_multi_object.py:514` `dead_only_schedule(..., target_vital_seen=)`
อิงการ parse ฝั่ง **C2S** (`legacy.parse_target_vital`) ส่วน CL-IMG-023 เป็นช่อง **ขาเข้า/S2C** ของ client
**คนละเรื่อง ห้ามยกข้ามกัน**

**nonclaim:** *"ไม่ใช่หลักฐานว่าเซิร์ฟเวอร์เดิมไม่เคยส่ง TargetVital"* · *"ไม่ได้พิสูจน์นโยบายการตอบของเซิร์ฟเวอร์เดิม"*

## ④ 🔴 คอลัมน์ป้องกันจริงที่ `mob_combat.py` รออยู่ มีชื่อแล้ว

`mob_combat.py:791-803` เขียนไว้เองว่า *"ไม่มีตารางไหนให้ค่า constitution กับแถว MOBS —
คอลัมน์ที่ขุดได้มีแค่ level, rank, ai id สองตัว, walk speed และ drop id … `MOB_ABILITY_CON` จึงเป็นของเราเอง …
รอบหลังที่ขุดคอลัมน์ป้องกันจริงได้จะมาแทนฟังก์ชันนี้"*

**รอบนั้นเกิดขึ้นแล้ว** — `STANDARD_MOB` 255 แถว × 38 คอลัมน์ มี **`n_CONSITUTION`** (สะกดผิดแบบนี้ในต้นฉบับ)
พร้อม `n_STRENGH` `n_AGILITY` `n_PERCEPTION` `n_INTELLECT` `n_AC_PHYSICS` `n_AC_MAGIC`
IMAGE loader ผูก 31 คอลัมน์กับออฟเซ็ตเป๊ะ: `+0x10 n_HPMAX` · `+0x20 n_DAMMIN_PHYSICS` · `+0x30 n_AC_PHYSICS` ·
`+0x34 n_AC_MAGIC` · `+0x38 n_ABSORB_PHYSICS` · `+0x40 n_PENETRATE_PHYSICS` · `+0x58 f_HITRATE` · `+0x5C f_DODGE` · `+0x7C f_BLOCKRATE`

FightAttr ใช้ค่าสัมประสิทธิ์ที่แน่นอน:
```
ac_physics   = trunc(constitution*2.0 + opt(CBuffAttr+0xFC) + opt(STANDARD_MOB+0x30))
max_hp       = trunc(constitution*5.0) + (NPC ? STANDARD_MOB+0x10 : LEVEL_ROW+0x04)
dammin_phys  = strength*1.0 + opt(STANDARD_MOB+0x20)
damplus_phys = agility*0.2       absorb_phys = strength*0.3      penetrate = agility*1.0
strength     = u16(ActorAttr+0x82) + u16(ActorAttr+0x182) + s32([0x0103382C])
```
(CON `+0x84/+0x184` · DEX `+0x86/+0x186` · INT `+0x88/+0x188` · PER `+0x8A/+0x18A` บวก global ตัวเดียวกัน
`max_stamina` ใช้ global ตัวที่สอง `[0x01033838]` · ทุกตัว clamp `max(0, ·)` และตัดเศษเข้าหาศูนย์)

**เทียบกับของเรา:** `mob_combat.py:310` ใช้ `defence = DEF_BASE + K_DEF_CON*ability_con + K_DEF_LV*level`
รูปของ client คือ `CON*2.0 + table[level].n_AC_PHYSICS` — **ไม่มี `DEF_BASE` และไม่มีพจน์ `K_DEF_LV*level`**
🟢 แต่ `K_DEF_CON = 2` ของเรา **ตรงกับ `constitution*2.0` ของ client พอดี**
และ `field_mobs.py:14` ใช้ดัชนี `STANDARD_MOB[MOBS.n_LEVEL_MIN]` อยู่แล้ว ⇒ ทางเข้าตารางถูกอยู่แล้ว

**nonclaim (สำคัญมาก):** `authoritative_scope = CLIENT_COMPUTED_UI_OR_MODEL_VALUE_NOT_SERVER_AUTHORITY`
⇒ **นี่คือค่าที่ client คำนวณเองเพื่อโมเดล/UI ไม่ได้พิสูจน์ว่าเซิร์ฟเวอร์เดิมคิดแบบนี้** และไม่ได้พิสูจน์ตัวเลขบนจอ
สำมะโน DATA ไม่ได้พิสูจน์ว่ามอนตัวไหน resolve ไปแถวไหน

## ⑤ ลำดับที่ผมเสนอ

ข้อ ① กับ ② เป็น**กลไกที่อธิบายอาการที่เราติดมานาน** และ**ไม่ต้องแก้โค้ดเพื่อทดสอบ** — แค่แก้บันทึกให้ตรงก่อน
ข้อ ④ แก้ได้จริงแต่ **nonclaim แรง** ⇒ ถ้าจะใช้ ให้ใช้เป็น "รูปสมการของ client" ไม่ใช่ "นโยบายเซิร์ฟเวอร์เดิม"
และเก็บ `MOB_ABILITY_CON` เดิมไว้เทียบ อย่าเพิ่งทิ้ง

-- ka1-B
