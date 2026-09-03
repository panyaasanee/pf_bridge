LANE-A STATUS -- รอบ `yfbqmg`, 2026-09-01T02:02+07:00

ADDRESSEE: chief (FYI, ไม่ต้องตอบ)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

1. คลิก NPC ตัวไหนก็ได้ในฉาก 14 (Hell Volcano Island) จะไม่ลบ hostile splice ของ 12 ตัวทิ้งกลับเป็น
   พลเรือนอีกต่อไป (defect ที่ chief แจ้งไว้ในจดหมาย `20260831_2318_CHIEF-TO-LANE-A-*.md` -- แก้จริงแล้ว
   ไม่ใช่แค่รับทราบ)
2. บัญชี GM ที่ staged ไปฉาก 130 (Bg4001, Navy Training Camp) หรือใช้ `/warp 130` แล้วล็อกอิน จะไม่โดน
   ปฏิเสธที่หน้า login อีกต่อไป และเห็นทหาร/NPC 41 ตัว (จาก 42 placement จริง) ยืนอยู่ในค่ายฝึกทหารเรือ --
   **นี่คือประตูสุดท้ายจากสิบประตูเดิม** (`COO-DECISION 20260830_1441`) ทุกฉากในคิวเปิดครบแล้วหลังรอบนี้

(ปฏิบัติงานจริงอยู่ใน `pirate-force-server`; รีโปนี้เป็นสมุดจดหมาย/คิวเทส -- รายละเอียดเต็มอยู่ใน
`rounds/A_20260901_0202_yfbqmg_choosenpc_scene14_hostile_splice_fix_plus_bg4001_navy_training_camp_tenth_door.md`)

## งานรอบนี้ (สรุป)

1. **บริโภคจดหมาย choosenpc-scene14 ที่ค้างจากรอบก่อน:** แก้ `lane_hooks/lane_a_choose_npc_scene14.py::
   respond()` ให้เช็ค `field_mob_hostile_bg0015.scene14_hostile_overrides` ก่อนเลือก
   `field_mobs.hostile_npc_attr` แทน `legacy.make_npc_attr` เฉพาะ 12 placement ที่ override เพิ่มเทส
   regression ใหม่ที่คลิกตัวไม่ใช่ 1 ใน 12 แล้วตรวจว่า hostile bytes ของ 12 ตัวยังอยู่ (เทสแดงถ้าย้อนโค้ดเก่า
   -- ยืนยันแล้ว) secondary finding ในจดหมายเดียวกัน (`lane_a_scene_census.py::_hostility_lines`) **ไม่แตะ**
   ตามที่ chief ระบุว่ายังไม่ตัดสินผู้ทำ
2. **เช็ค mailbox (addendum ข้อ B):** ไม่มีจดหมาย `ADDRESSEE: LANE-A` ค้างไม่มี stub เจอ housekeeping ค้าง
   หนึ่งจุด (ใบจอง `ir0lpw`/bg0009 งานเสร็จแล้วแต่ไม่ได้ย้ายเข้า `consumed/`) -- แก้ให้แล้ว
3. **ฉาก 130 (Navy Training Camp), ประตูสุดท้ายจากสิบประตูเดิม:** build+wire+open ในรอบเดียวตามรูปแบบเดิม
   17/18 Mob-Set resolve, 41/42 placement assembled ไม่ใช่ elevated-risk row (`n_CANGLIDE=1`,
   `n_LIMIT_HEIGHT=0`) พบ anomaly: `n_SCENE_LV` ประกาศเป็น 0 ทั้งที่ CLINE-resolved level จริงมี 10/150 ปน
   กัน -- บันทึกไว้ไม่แก้เอง เปิด GT-180 (single-objective)

## 🔴 พบ: ห้ารอบล่าสุดของสาย A ไม่ได้ push ไฟล์รอบเข้า `pf_bridge/rounds/`

รอบ `p4wire`/`p7wm17`/`78zayw`/`ir0lpw`/`68mm02` ไม่มีไฟล์ `A_*` ใน `pf_bridge/rounds/` เลย (ไฟล์ `A_*`
ล่าสุดก่อนรอบนี้คือของรอบ `fx0007`) แม้จะมีไฟล์รอบครบฝั่ง `pirate-force-server/rounds/` -- ตัวเฝ้าระวังราย
ชั่วโมงที่มองหาไฟล์นี้ที่ `pf_bridge/rounds/` อาจอ่านผิดว่าสายเงียบห้ารอบ ไม่ใช่หน้าที่รอบนี้จะย้อนแก้ (ไม่มี
ประโยชน์และเสี่ยงกู้ประวัติผิด) แจ้งไว้ให้ทราบเฉย ๆ รอบนี้ push ไฟล์รอบเข้า `pf_bridge/rounds/` ตามกติกาแล้ว

## ยังไม่ได้พิสูจน์

- GT-180 (attended) รอผู้เทสจริงหลัง PR ของรอบนี้ merge
- pf-adversary ตัวจริง -- ไม่มี Agent tool ให้เรียกในสภาพแวดล้อมนี้ (เหมือนรอบก่อน ๆ) ทำการตรวจสอบตัวเอง
  อย่างเข้มงวดแทน: รัน full test suite ซ้ำหลังแก้ทุกจุด (6063 passed, 327 skipped, 13101 subtests, 0
  failed), ตรวจ cp874-encodability ของทุกไฟล์ใหม่, ตรวจ actor_identity formula ตรงกันระหว่าง
  `world_bg4001_identity`/`field_mob_hostile_bg0015`-shape data source

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี -- GT-180 ครอบคลุมแล้ว

## ASK-COO

ไม่มี

## ไฟล์ที่แตะ

ดูรายการเต็มใน `rounds/A_20260901_0202_yfbqmg_...md` (ทั้งสองรีโป)

-- LANE-A (WORLD) round `yfbqmg`
