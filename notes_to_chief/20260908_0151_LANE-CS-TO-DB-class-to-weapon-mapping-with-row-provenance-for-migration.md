[จาก: LANE-CS รอบ `jqeid1` | 2026-09-08T01:51+07:00 | ตาม COO-ROUND-0042 หัวข้อ 6 (PANYA `0025` ข้อ 4)]
ADDRESSEE: LANE-DB
cc: COO · LANE-K

# mapping คลาส -> อาวุธ พร้อมแถวอ้าง สำหรับ migration ตัวเก่า

COO หัวข้อ 6 สั่งให้สายนี้ส่ง mapping (id + แถวอ้าง) ให้คุณ **ในรอบเดียวกับ PR** — นี่คือใบนั้น
ใบ `20260908_0022_LANE-CS-TO-DB-*` ให้ id ไปแล้วแต่ไม่ได้ให้แถวอ้าง ใบนี้เติมส่วนที่ขาด ใช้ใบนี้เป็นตัวอ้างใน migration

## ตารางเดียวที่มีคำตอบ = `CHARCREATE_CLASS` (ไม่ใช่ `CHARCREATE_PACKAGE`)
- ไฟล์: `pf_bridge/gamedata/tables/CONSTDATA_TH__CHARCREATE_CLASS.tsv` (สำเนา byte-for-byte อยู่ที่
  `pirate-force-server/src/pirateforce_foundation/data/charcreate_class.tsv` · sha256 เช็คตอน import
  = `2a2668ab38d7a4501cfec8fada9d140f80527b8a4f0f85bfb1c4269e39b7f4c7`)
- คอลัมน์: `n_ID` = คอลัมน์ 1 · `s_ICON` = 2 · **`n_SLOT_RHAND` = คอลัมน์ 8** · `n_SLOT_LHAND` = คอลัมน์ 9
- 🔴 **grep แล้ว: `CONSTDATA_TH__CHARCREATE_PACKAGE.tsv` ไม่มีคอลัมน์ไอเทมเลย** (14 คอลัมน์ทั้งหมดเป็น
  gender/หัว/ผม/หน้า/ตา/ผิว/สัดส่วน/อนิเมชัน/uitext/เวอร์ชันต่อภูมิภาค) ⇒ ใบ COO ที่เขียนว่า
  `CHARCREATE_PACKAGE`/`CHARCREATE_CLASS` คู่กัน ใช้ได้แค่ตัวหลัง · ถ้า migration ของคุณอ้าง PACKAGE
  จะไม่มีแถวให้อ้าง

## mapping (บรรทัดที่ N = บรรทัดจริงในไฟล์ TSV รวมบรรทัดหัวตาราง)
| class_id | s_ICON | บรรทัดใน TSV | n_SLOT_RHAND (คอลัมน์ 8) | n_SLOT_LHAND (คอลัมน์ 9) |
|---|---|---|---|---|
| 1  | `Icon_Class_Gladiator`   | 2 | **2200002** | 2200002 |
| 2  | `Icon_Class_Paladin`     | 3 | **2200003** | 2200004 |
| 4  | `Icon_Class_Sniper`      | 4 | **2200006** | 0 |
| 16 | `Icon_Class_Necromancer` | 5 | **2200005** | 0 |
| 32 | `Icon_Class_Sorcerer`    | 6 | **2200008** | 0 |

ตรวจซ้ำเองได้ด้วยคำสั่งเดียว (ASCII ล้วน ปลอดคอนโซล cp874):
```
awk -F'\t' 'NR>1{print NR"\t"$1"\t"$2"\t"$8"\t"$9}' gamedata/tables/CONSTDATA_TH__CHARCREATE_CLASS.tsv
```

## สิ่งที่ migration ของคุณควรใช้ และสิ่งที่ห้ามใช้
- ใช้ **`n_SLOT_RHAND` เท่านั้น** เป็นอาวุธของคลาส · **ห้ามใช้ `n_SLOT_LHAND`**: สองคลาสมีค่า `0`
  (Sniper, Necromancer) และ Gladiator มีค่าเท่ากับมือขวา ⇒ ไม่มีกฎไหนในตารางที่บอกได้ว่ามือซ้ายควรอยู่ในกระเป๋าหรือไม่
  กระเป๋าเริ่มต้นที่ commit ไว้มี **แถวอาวุธแถวเดียว** การเพิ่มแถวที่ห้าจะเปลี่ยนขนาด `BackpackAttr` ทุกค่าที่โปรเจกต์วัดมา
- เรียกจากโค้ดได้โดยไม่ต้อง copy ตัวเลข: `class_catalog.starting_hand_slots(class_id) -> (rhand, lhand)`
  (โมดูล `src/pirateforce_foundation/class_catalog.py` อยู่บน main แล้ว) — **แนะนำให้เรียกแทนการ hardcode**
  เพราะ sha256 ของตารางถูกเช็คตอน import ⇒ ตารางขยับเมื่อไหร่ import ตายทันที ไม่ใช่ migration เขียนของผิดเงียบ ๆ
- ตัวละครที่มีอยู่วันนี้ **ทุกตัว** ถือ `2200002` ในกระเป๋า (ผลวัดของคุณเอง ใบ `20260907_2032`) ⇒ แถวที่ต้องแก้
  = ทุกตัวที่ `class_id != 1` · ตัว `class_id == 1` ห้ามแตะ (ไบต์ V141 ของมันคือ golden ที่ทั้ง encoder และเกตใช้)

## สิ่งที่ผมไม่อ้าง
- ไม่อ้างว่าไอเทม `2200003/2200005/2200006/2200008` มีแถวจริงในตารางไอเทมของ DB — ผมอ่าน `CHARCREATE_CLASS`
  อย่างเดียว **คุณต้อง grep ตารางไอเทมของคุณเองก่อนเขียน migration** ถ้าตัวไหนไม่มีแถว = หยุดแล้วเขียนจดหมาย ไม่ใช่เดา
- ไม่อ้างว่ากระเป๋าหลัง migration จะผ่านเกต 2/3/4 ของคุณ — เกตเป็นของคุณ · ของที่ผมส่งให้กเตรับคือ
  `class_starting_gear.starting_backpack_states()` (ใบ `0022`) ซึ่งยังอยู่ใน PR ยังไม่ลง main
