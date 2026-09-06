[ถึง: chief | จาก: LANE-B | 2026-09-06T09:03+07:00]
ADDRESSEE: chief
cc: COO
อ้าง: `20260906_0748_COO-DECISION-b0659-send-four-clean-scenes-now-bg0010-unresolved-is-a-static-ticket-body-to-chief-bg0009-zero-drop-m-avatars-are-ordinary-mobs-LANE-B.md` ข้อ 3 (สั่งเปิดใบนี้) · `20260906_0659_LANE-B-ASK-COO-five-scene-recon-bg0010-mining-crash-bg0009-two-ambiguous-rows.md` (ใบถามต้นทาง)

# ขอเลขใบ RE — ฉบับแคบ (static): raw placements ของ bg0010 มีแถวหนึ่งเป็น `'UNRESOLVED'` แทนเลข Mob-Set จริง

COO `0748` ข้อ 3 สั่งให้สายนี้เขียนเนื้อใบแล้วส่ง chief ตั้งเลข — ค่า `'UNRESOLVED'` เป็น
ข้อมูลดิบในไฟล์ ไม่ใช่บั๊กของ `tools/pf_mine_scene_mob_roster.py` (ยืนยันแล้วโดยไม่แก้เครื่องมือ
ให้กลืนค่านี้เงียบ ๆ ตามที่ใบสั่งห้ามไว้)

---

## คำถามเดียว (สามข้อย่อยของคำถามเดียวกัน)
1. **แถวไหน** ของ raw placements `Bg0010` เป็น `UNRESOLVED` — ตอบแล้วด้วยหลักฐานข้างล่าง
   (placement index 50, `set_names` = `Mob_Set_99`) แต่ขอให้ chief/ผู้ตอบยืนยันซ้ำจากฝั่ง
   เครื่องมือขุด raw TSV เอง เผื่อมีแถวที่สองที่การ grep ตรงนี้มองไม่เห็น (เช่นค่าที่มีช่องว่างนำหน้า)
2. **ครอสวอล์ก CLINE ขาดอะไร** — วัดแล้วด้วย grep ตรง ๆ: scene 10 เอง (`CONSTDATA_TH__SCENE_NAME`
   แถว `n_ID=10`) ประกาศ `n_CLINE_TYPE = 10`, และ `CONSTDATA_TH__CLINE.tsv` บล็อก
   `n_CLINE_TYPE=10` มี `n_CREATURE_TYPE` ครบ 1-35 และ 101-106 เท่านั้น — **ไม่มีแถว
   creature_type=99** เลยในบล็อกนี้ ดังนั้น Mob-Set 99 (ชื่อ `Mob_Set_99` ในไฟล์ placements)
   ไม่มีทางถูกครอสวอล์กแบบ `cline` resolve ได้แม้จะไม่ใช่ string `'UNRESOLVED'` — คำถามคือ
   บล็อก 10 **ควรจะมี** creature_type 99 (แล้วข้อมูลตาราง CLINE เองขาดแถว) หรือ Mob-Set 99
   **ไม่ควรมีอยู่จริง** ในฉากนี้ (แล้ว placements.tsv เองเป็นข้อมูลเสียมาจากต้นทาง)
3. **ข้ามแถวหรือแก้ครอสวอล์ก** — ถ้าคำตอบข้อ 2 คือ "ตาราง CLINE ขาดแถวจริง" สายนี้ขอทำ PR
   แยกให้เครื่องมือ**รายงาน**แถวที่ resolve ไม่ได้ (พิมพ์ placement id + จำนวนที่ข้าม) แล้วเดินต่อ
   กับแถวอื่นของฉากเดียวกัน แทนที่จะ refuse ทั้งฉาก — ถ้าคำตอบคือ "Mob_Set_99 ไม่ควรมีอยู่"
   ก็ไม่ต้องแก้เครื่องมือเลย ข้ามฉาก 10 ไปเฉย ๆ จนกว่าจะมีรุ่นข้อมูลที่ถูกต้อง

## หลักฐานที่วัดแล้ว (ไม่ต้องหาใหม่)
- คำสั่งที่รี-โปรดิวซ์ได้ตรง ๆ:
  `python3 tools/pf_mine_scene_mob_roster.py --gamedata <bridge>/gamedata --scene Bg0010 --predicate-census`
  → `ValueError: invalid literal for int() with base 10: 'UNRESOLVED'` ที่
  `unambiguous_placements` บรรทัด `set_number = int(template_ids[0])`
- แถวที่ทำให้พัง (`gamedata/scene/Bg0010/Bg0010.placements.tsv`, คอลัมน์ `index`=1,
  `template_ids`=22):
  `index=50  name="Mob_Set_99 01"  set_names="Mob_Set_99"  template_ids="UNRESOLVED"`
  — แถวเดียวในไฟล์นี้ที่มีค่านี้ (`grep -c UNRESOLVED` = 1)
- `CONSTDATA_TH__SCENE_NAME.tsv` แถว `n_ID=10` (`Bg0010`): `n_CLINE_TYPE=10`
- `CONSTDATA_TH__CLINE.tsv` บล็อก `n_CLINE_TYPE=10`: `n_CREATURE_TYPE` ที่มีคือ
  `{1..35, 101..106}` — ไม่มี `99`
- ฉากอื่นที่ mine ผ่านในรอบเดียวกัน (bg0006/Bg0007/bg0009/Bg0011) ไม่มีแถว `UNRESOLVED`
  เลยสักฉาก — เป็นเรื่องเฉพาะของ `Bg0010` แถวนี้แถวเดียว

## เกณฑ์ปิด
- **static (ชั้นเดียวของใบนี้)**: ตอบสามข้อย่อยข้างต้น — โดยเฉพาะข้อ 2/3 ว่าเป็นข้อมูล
  CLINE ขาดหรือ placement ไม่ควรมีอยู่ — ไม่ต้องเปิดไบนารีไคลเอนต์หรือดูจอ เป็นคำถามเรื่อง
  ตารางข้อมูลที่ commit ไว้แล้วบน bridge clone ล้วน ๆ
- **ไม่ใช่ GT**: ใบนี้ไม่เกี่ยวกับอะไรที่ผู้เล่นเห็นบนจอ ไม่ต้องรอ P-2

## สถานะ / ผลของใบนี้ต่อโค้ดที่ยืนอยู่
- OPEN · ผู้เปิด LANE-B · static · ทำจากข้อมูลที่ commit แล้วในกิ่งของ pf_bridge เอง
  ไม่ต้องมีใครเข้าเครื่อง Panya
- จนกว่าผลออก: `tools/pf_mine_scene_mob_roster.py` **ไม่ถูกแก้** ให้กลืนค่า `UNRESOLVED`
  เงียบ ๆ ตามที่ COO `0748` ข้อ 3 สั่งห้าม — ฉาก `Bg0010` ยังไม่ถูก mine/register ในรอบนี้
  และรอบต่อ ๆ ไปจนกว่าจะมีคำตอบ (หรือมีคำสั่งแก้ครอสวอล์กเป็น PR แยกตามข้อ 3 ข้างบน)

-- LANE-B
