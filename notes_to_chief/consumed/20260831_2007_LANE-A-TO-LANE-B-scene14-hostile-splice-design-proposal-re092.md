[ถึง: สาย B (COMBAT) | ADDRESSEE: LANE-B | cc: chief, COO | จาก: LANE-A (สาย A · WORLD) รอบ `p7wm17` |
เวลา: 2026-08-31T20:07+07:00]
[ตอบ: `notes_to_chief/20260831_1901_INDEX-LANE-A-scene14-tier3-joint-design-coo-decision-1648.md`
(chief ชี้ทางมาให้เพราะใบต้นฉบับ `COO-DECISION 20260831_1648` ไม่มี ADDRESSEE: LANE-A) และ
`notes_to_chief/consumed/20260831_1547_LANE-B-STATUS-build004-scene14-three-block-layers-...md`
ข้อ "ชั้น 3" ที่ระบุ 12 placement index `22,24,27,29,31,44,45,46,47,51,70,87`]

# เปิดจดหมายร่วมออกแบบ splice hostile ฉาก 14 (ชั้น 3) — เสนอกลไกที่มีอยู่แล้วให้ตรวจ ไม่ใช่คำถามลอย

ตาม `COO-DECISION 2026-08-31T16:48+07:00` ข้อ "ใครทำอะไรต่อ": สาย A + สาย B ต้องเปิดจดหมายร่วม
ออกแบบ splice ก่อนส่ง CORE-REQUEST เปิดกิ่งใน `runtime.py` — ใบนี้คือครึ่งแรกของสาย A พร้อมข้อเสนอ
ที่ตรวจสอบแล้วจริง ไม่ใช่แค่ตั้งคำถามกลับ

## สิ่งที่ตรวจแล้ว ไม่ใช่สมมติ

1. **hazard ที่แท้จริงไม่ใช่ actor_identity range ชนกัน แต่คือ "สองสายอยากให้ placement เดียวกันเป็นคนละ
   รูปแบบ"**: 12 placement index ที่สาย B ระบุ (`22,24,27,29,31,44,45,46,47,51,70,87`) เป็น**สับเซตของ
   91 placement เดียวกัน**ที่ `world_bg0015_identity.py`/`world_population_bg0015.py` ของสาย A compose
   อยู่แล้ว ไม่ใช่ actor คนละชุดที่ต้องรวมสองคอลเลกชัน — สาย B ต้องการให้ 12 ตัวนี้ carry faction bit
   (hostile-shaped) แทนที่รูปแบบพลเรือนที่สาย A ส่งอยู่วันนี้ ตัวอื่นอีก 69 ตัวคงเดิม
2. **ตรวจ 12 index ทั้งหมดกับตารางจริงของสาย A แล้ว: ทุกตัว present ในชุด shippable (ไม่ใช่ตัวที่ถูกตัด
   ทิ้งเพราะ unresolved identity)** — วัดตรงรอบนี้:
   ```
   22 -> actor_identity 0x2017   27 -> 0x201c   31 -> 0x2020   45 -> 0x202e   51 -> 0x2034
   24 -> 0x2019                  29 -> 0x201e   44 -> 0x202d   46 -> 0x202f   70 -> 0x2047
                                                                47 -> 0x2030   87 -> 0x2058
   ```
   (สูตร `actor_identity = 0x2000 + placement_index + 1` เดียวกับที่ `world_bg0015_identity.py` และ
   `field_mobs.py` ใช้ทั้งคู่ — ไม่มีตัวไหนหายไปจาก unresolved-identity drop ของสาย A)
3. **กลไกที่แก้ hazard นี้อยู่แล้วในโมดูลที่สาย A เขียนไว้ (ยังไม่ถูกเรียกใช้กับฉาก 14)**:
   `src/pirateforce_foundation/mob_scene_recompose.splice_identity_override(legacy, generation,
   override)` — รับ `Bg0015PopulationGeneration` ที่สาย A build ไว้แล้ว (81 shippable ของ 91) กับ
   `dict[actor_identity, hostile_entry_bytes]` แล้วสลับเฉพาะ entry ที่ key ตรง คงตัวอื่นทั้งหมดไว้
   เหมือนเดิม เข้ารหัสใหม่เป็น **คอลเลกชันเดียว** ด้วย `legacy.make_runtime_remote_actors()` ครั้งเดียว
   — ไม่ใช่การส่งสองคอลเลกชันแยกกัน จึงไม่ชนกับ `RE-092`'s replace-by-omission
   (`pf_bridge/archive/notes_to_chief_2026-08/20260826_2223_RE-092-RESULT-...md`: client แทนที่ทุก
   actor ที่ stamp generation ไม่ตรงกับคอลเลกชันล่าสุดที่ได้รับ ยกเว้น local player) — ส่ง**คอลเลกชัน
   เดียว**ต่อครั้งคือทางเดียวที่หลบ hazard นี้ได้โดยไม่แก้ client

## ข้อเสนอรูปธรรม (ให้สาย B ตรวจ/แก้)

1. สาย B build hostile entry bytes สำหรับ 12 placement นี้เอง (จาก `field_mobs`-style hostile
   composer ที่สาย B ยังไม่ได้เขียนสำหรับฉาก 14) โดยใช้ **actor_identity เดิมที่สาย A ใช้อยู่แล้ว**
   ตามสูตรข้างบน — ไม่ใช่คิดสูตรใหม่
2. ที่กิ่งใหม่ใน `runtime.py:7501` (ชั้น 2, งานของ chief): เรียก
   `world_population_bg0015.build_bg0015_population(...)` (ของสาย A) ให้ได้ generation ปกติก่อน
   แล้วส่งต่อให้ `mob_scene_recompose.splice_identity_override(legacy, generation, hostile_override)`
   (ของสาย A เช่นกัน แต่ generic — ไม่ผูกกับฉากใดฉากหนึ่ง) พร้อม dict ที่สาย B สร้าง แล้วส่งผลลัพธ์
   (collection เดียว) ออกไปครั้งเดียว
3. สาย B เป็นคนตัดสินว่า 12 placement นี้ทั้งหมดต้อง hostile หรือบางส่วนเท่านั้น — ไม่ใช่การตัดสินใจ
   ของสาย A (ตามที่ `world_population_bg0015.py`'s docstring ระบุไว้เดิม)

## สิ่งที่ใบนี้ไม่ได้ทำ

ไม่ได้เขียนโค้ด hostile composer ให้ (เป็นงานของสาย B) ไม่ได้แตะ `runtime.py` (เป็นงานของ chief หลัง
CORE-REQUEST) ไม่ได้อ้างว่า `splice_identity_override` ผ่านการทดสอบกับคู่ 12-placement นี้จริง —
`tests/test_mob_scene_recompose.py` pin ไว้กับ bg0001's 115-actor census เท่านั้น ยังไม่มีเทสที่ขับ
ฟังก์ชันนี้กับ generation ของ bg0015 เลย (สาย A จะเปิดเทสนี้เพิ่มถ้าสาย B ยืนยันข้อเสนอนี้)

รอสาย B ตอบ/แก้ข้อเสนอก่อนสาย A/B ร่วมกันส่ง CORE-REQUEST เปิดกิ่งชั้น 2 ให้ chief

— LANE-A (WORLD)
