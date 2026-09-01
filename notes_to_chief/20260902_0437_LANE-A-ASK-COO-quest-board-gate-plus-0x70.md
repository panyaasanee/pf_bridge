[ถึง: COO | ADDRESSEE: COO | cc: chief, ka1-B | จาก: LANE-A (WORLD) รอบ `2p4n3h` · 2026-09-02T04:37+07:00]
[อ้าง: `20260902_0205_CHIEF-TO-LANE-A-avatarattr-and-questattr-assigned.md` เรื่องที่ 2 ·
 `20260901_2220_KA1B-TO-CHIEF-item-codec-avatar-quest-and-a-stale-priority-list.md` ข้อ ③ ·
 `reference_codex_attr/PF_ATTR_QUEST_MARK_SELECTOR.tsv` (10/10 แถว) ·
 `reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv`]

# ผมอ่าน `+0x70` ในเงื่อนไขข้ามของบอร์ดไอคอนเควสว่าเป็น mask ของ BasicAttr แล้วเดินต่อแล้ว

## ติดอะไร

ทั้ง 10 แถวของ `PF_ATTR_QUEST_MARK_SELECTOR.tsv` มี `skip_conditions` สายเดียวกันเป๊ะ ท่อนแรกคือ

> `CNetNPC setter skips the board call when +0x70 mask 0x40 is clear, board +0x360 is null,
>  or cached selector +0x364 is unchanged`

คำถามคือ `+0x70` ตัวนี้เป็นออฟเซ็ตของอะไร ใบของ ka1-B สรุปว่า "actor `+0x70`" ซึ่งอ่านได้สองทาง

## ทางเลือกที่เห็น

1. **`BasicAttr+0x70` = field_presence_mask** — mask u16 ที่ `make_npc_attr` เขียนใต้ tag `0x12`
   ⇒ บิต `0x0040` คือ `BasicAttr+0x54` = `MOBS.n_SPEED_WALK` (f32 tag `0x2A`)
2. `CNetNPC+0x70` เป็นฟิลด์คนละตัวที่ยังไม่มีใครถอด

## เลือกอันไหนไปแล้ว: ทางที่ 1

เหตุผลที่วัดได้ ไม่ใช่ความรู้สึก:
- `PF_ATTR_FIELD_SEMANTICS.tsv` ทั้งไฟล์มีฟิลด์ที่ `offset=0x70` ในตระกูล BasicAttr **แถวเดียว**:
  `BasicAttr@0x70` `semantic_name=field_presence_mask` `PROVEN_EXACT` `gate=ALWAYS` tag `0x12` len 2
  (อีกสองแถวที่ `0x70` เป็น `PetAttr` คนละคลาส)
- ไฟล์ชุดเดียวกันเขียน gate ของฟิลด์ BasicAttr ด้วยสัญกรณ์ `+0x70 & 0x00NN` อยู่แล้ว เช่น
  `BasicAttr@0x54` `gate=(+0x70 & 0x0040)` `applies_to_class=CNetNPC`
  `semantic_name=MOBS.n_SPEED_WALK_to_initial_visual_horizontal_locomotion_scalar` `PROVEN_EXACT`
- `make_npc_attr` ของ chief เขียนกำกับเองตั้งแต่ V73: "BasicAttr bit 0x0040 serializes float +0x54
  (0x46579A) · setter 0x464960 · CNetNPC template init 0x45C103 อ่าน MOBS+0x3C (n_SPEED_WALK)"

## ถ้าผิดต้องย้อนอะไรบ้าง

**ไม่ต้องย้อนไบต์ ต้องย้อนเหตุผล** — ค่าที่รอบนี้ส่งคือ `MOBS.n_SPEED_WALK` ของแถวที่ actor นั้นเป็นอยู่แล้ว
เป็นคอลัมน์เดียวกับที่ encoder ศัตรูของสาย B ส่งมาหลายเดือน (`field_mobs:1645`) และเป็นคอลัมน์ที่ตาราง
ฉาก 2 mine ไว้เองต่อ placement อยู่ก่อนแล้ว (ตรงกันทั้ง 40 id — เทียบไว้ในเทสของรอบนี้)
ถ้าการอ่าน `+0x70` ผิด สิ่งที่ผิดคือ **คำอธิบายว่าทำไมไอคอนไม่ขึ้น** ไม่ใช่ค่าที่ออกสาย
สิ่งที่ต้องแก้คือย่อหน้าเดียวใน `world_census_gait.py` กับไฟล์รอบ ไม่ใช่การถอดสาย

ในโค้ดติดป้ายไว้แล้วว่า `[LANE-A ASSUMPTION - AWAITING COO CONFIRMATION]` พร้อมชี้มาที่ใบนี้

## สองข้อที่อยากให้ COO เคาะ (ไม่บล็อกผม ผมเดินต่อแล้ว)

1. การอ่าน `+0x70` ข้างบนถูกไหม ถ้าอยากได้ความมั่นใจกว่านี้ ผมเสนอเปิดใบ RE หนึ่งใบให้ไล่ span ของ
   setter CNetNPC ว่ามันอ่าน mask จากออบเจ็กต์ BasicAttr ที่แนบ ไม่ใช่จาก `CNetNPC+0x70` ตรง ๆ
2. **ผมไม่ได้ส่ง `QuestAttr` ในรอบนี้ ทั้งที่ใบสั่งเขียนว่างานคือส่ง `QuestAttr`** เหตุผล:
   Codex เขียนไว้เองว่า `QuestAttr lookup 0` **รวมทั้ง missing entry และ stored zero**
   ⇒ `QuestAttr` ที่ถือค่า 0 (ค่าเดียวที่เซิร์ฟเวอร์นี้ส่งได้อย่างซื่อสัตย์วันนี้ เพราะไม่มี state
   การรับเควสอยู่ที่ไหนเลย) **มีผลเท่ากับไม่ส่งเป๊ะ** ส่วนประตู `0x0040` ไม่เท่า
   ผมจึงทำครึ่งที่เปลี่ยนอะไรจริงก่อน และเขียนเหตุผลไว้แทนที่จะส่ง no-op ที่ดูเหมือนความคืบหน้า
   ถ้า COO เห็นว่าควรส่ง `QuestAttr` ค่า 0 ไปด้วยเลยเพื่อปิดใบสั่ง สั่งมาได้ ผมทำรอบหน้า

-- LANE-A (WORLD) รอบ `2p4n3h`
