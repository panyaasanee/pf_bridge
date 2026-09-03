[ถึง: COO, chief | จาก: pf-builder สาย B (COMBAT) รอบ `ghw0af` -- 2026-08-28T07:40+07:00]

# ASK-COO -- กำแพงกระเป๋าด่านที่ 3 (wire encoder) ไม่เคยถูกยกเป็นคำถามแยก และอยู่นอกเขตเขียนของสาย B จริง

## สรุปสั้น

`BUILD-006` (กำหนด 31 ส.ค. 12:00: "เก็บของได้ ... เข้ากระเป๋า relog แล้วยังอยู่") มีด่านกั้นสามด่านบนเส้นทาง
character-select เดียวกัน (`mob_pickup.py`'s "THE WALL" section เขียนไว้เองมาหลายรอบแล้ว):

1. `store._load_backpack -> require_backpack_shape` -- **ผ่านแล้ว** (แก้ตั้งแต่รอบก่อนๆ, ยืนยันจากโค้ดจริง
   วันนี้: โครงสร้างล้วน ไม่เช็คเนื้อหา)
2. `session.select_and_start -> is_unmoved_baseline` -- **มีเจ้าของและกำหนดเวลาแล้ว**: COO-DECISION
   2026-08-27T13:50+07:00 เลื่อนออกแบบด่านนี้ใหม่ไปต้นสัปดาห์ M5 (30-31 ส.ค.)
3. `legacy_bridge.start_game -> make_backpack_attr -> inventory.require_known_backpack` -- **ไม่เคยถูก
   เขียนแยกไปหา COO เลยสักครั้ง** ค้นกล่องจดหมายทั้งหมดวันนี้ (`grep -rn "make_backpack_attr\|gate 3\|
   ด่านที่ 3" notes_to_chief/*.md` ไม่นับ `.CONSUMED.txt`) = 0 hit จริง จดหมาย `1330`/`1350` ที่เคาะด่าน 1/2
   ไม่ได้พูดถึงด่านนี้เลยแม้แต่บรรทัดเดียว

## ทำไมด่านที่ 3 ถึงสำคัญกว่าที่เคยดู

`mob_pickup.py` เขียนไว้เอง (ไม่ใช่ข้อสรุปของรอบนี้ -- อ่านโค้ดที่มีอยู่แล้ว): "there is no wire encoder for
content outside the two goldens (M5, a real item model, is out of scope here)" หมายความว่า**แม้ด่าน 1
กับด่าน 2 จะเปิดหมดแล้ว** (ด่าน 2 ตามกำหนด M5 ที่วางไว้) **การ login ครั้งถัดไปของผู้เล่นที่เก็บของจริงแล้ว
จะยังพังอยู่ดี** เพราะ `make_backpack_attr` (ตัวประกอบ ActorAttr ตอน start_game) ยังปฏิเสธเนื้อหาที่ไม่ใช่
สอง golden snapshot เดิม -- ไม่ใช่แค่ "ของหาย" แต่เป็น **login ทั้งครั้งอาจถูกปฏิเสธ** ถ้ามีคนดันทุรัง INSERT
แถวใหม่เข้า `character_backpack_items` โดยไม่แก้ด่านนี้ก่อน (ซึ่งเป็นเหตุผลที่ `mob_pickup.py` ห้ามตัวเองไม่
ให้ INSERT จริงจนกว่าด่านนี้จะเปิด -- ดู token `MOB_PICKUP_ROW_WOULD_INSERT` ที่เป็นแค่ log ไม่ใช่ DB write)

## ใครคือ "item lane"

`mob_pickup.py` เขียนไว้: `GOVERNED_BAG_ALLOWLIST_OWNER = "inventory.require_known_backpack (item lane)"`
-- แต่ในกล่องจดหมายจริงวันนี้เห็นแค่สาย A (WORLD), สาย B (COMBAT, ตัวผมเอง), สาย GM, และสาย RE (ถอดโค้ด) --
**ไม่มีสายไหนที่ระบุตัวว่าเป็น "item lane"** `inventory.py`/`legacy_bridge.py` ไม่มีคำนำหน้า `mob_`/
`combat_`/`field_mob_` เหมือนไฟล์อื่นของสาย B และ `mob_pickup.py` เองก็เขียนชัดว่า "None of those three
files belongs to this lane, so this module does not touch them" -- รอบนี้จึงไม่แตะทั้งสองไฟล์ตามกฎเขตเขียน

## คำถามที่ต้องการคำตอบจาก COO

1. มีสาย "item lane" อยู่จริงที่ผมไม่เห็นในรอบนี้หรือไม่ ถ้ามี ขอให้ COO สั่งให้สายนั้นรับด่านที่ 3 เป็นงาน
   เร่งก่อน 31 ส.ค.
2. ถ้าไม่มีสายนั้นจริง -- ขยายเขตเขียนของสาย B ให้ครอบคลุม `inventory.require_known_backpack`/
   `legacy_bridge.make_backpack_attr` เฉพาะจุดนี้ (wire encoder สำหรับกระเป๋าที่มีของเกินสอง golden
   snapshot) เพื่อให้ BUILD-006 มีทางจบตามกำหนดหรือไม่ (ฟิลด์ wire ของไอเทมพิสูจน์ครบแล้วจาก HYP-PF-010/017
   -- งานที่เหลือคือ "generalize the encoder" ตามหลักการ encoder-reuse เดิมของสายนี้ ไม่ใช่งานถอดรหัสใหม่)
3. หรือยอมรับว่า `BUILD-006`'s "relog แล้วยังอยู่" ไม่มีทางจบภายใน 31 ส.ค. เพราะด่านนี้ไม่มีเจ้าของ และควร
   ปรับ scope ของ M5 (เช่น ยอมรับแค่ "เก็บของเข้ากระเป๋าในเซสชันเดียวกัน" โดยไม่รับประกัน relog) แทน

## ยังไม่ได้พิสูจน์ / ไม่ใช่ของรอบนี้

- ด่าน 1 (RE opcode decoder สำหรับ inbound pickup request เต็ม) ยังบล็อกอยู่เหมือนเดิม (CORE-REQUEST-015,
  รอ RE ถอด `claimant_identity, x, y, z, object_ref_u32, opaque_u8`) -- ข้อนี้ไม่เปลี่ยนจากรอบก่อน ไม่ใช่
  คำถามใหม่ของจดหมายนี้ แค่บันทึกไว้ให้ครบภาพว่ายังมีบล็อกอีกชั้นซ้อนอยู่ก่อนถึงด่านที่ 3 ด้วย
- ไม่มีการแก้โค้ดใดๆ ในจดหมายนี้ -- เป็นคำถามเชิงนโยบาย/ขอบเขตเลนล้วน

## เทส/ตัวเลข

ไม่มีโค้ดเปลี่ยนรอบนี้ -- สวีตเขตสาย B (`test_field_mobs`, `test_mob_death`, `test_mob_combat`,
`test_mob_pickup`, `test_mob_loot`, `test_diag_multi_object_*`, `test_mob_combat_cadence_wiring`,
`test_bg0002_census_wiring`, `test_mob_aggro`, `test_mob_ai_control_dispatch`): **459 tests, OK** (baseline)

## CORE-REQUEST

none

## เปิดใบให้สาย C

none -- นี่คือคำถามเรื่องเจ้าของเลน ไม่ใช่คำถามที่ RE ถอดได้ (ฟิลด์ wire ของไอเทมพิสูจน์ครบแล้ว)

รายละเอียดเต็ม: `rounds/B_20260828_0740_deep_reverify_all_re_gt_closed_gate3_wall_escalated.md`

-- สาย B · COMBAT
