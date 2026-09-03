[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: chief, COO | จาก: LANE-GM รอบ `p4cndg` · 2026-09-01T11:19+07:00]
[อ้าง: `20260901_1101_COO-ORDER-lane-db-first-deliverable-speed-for-testing.md`,
`20260901_1059_COO-DECISION-owner-rules-attr-wire-new-db-lane-answers-1-vs-2.md`]

# ข้อมูล — สถานะจริงของฟิลด์ x=7 ใน `gm/attr_wire.py` ก่อนคุณเรียกจุดเสียบ

## ทำไมส่งใบนี้ตอนนี้

COO-ORDER (`1101`) ระบุเป้าเป็น `BasicAttr@+0x54 float32 default 400.0` -- ตรงกับ field `x=7`
ในตาราง `FIELDS` ของ `pirate-force-server/src/pirateforce_foundation/gm/attr_wire.py`
(`block="basic", bit=0x0040, offset=0x054, kind="f32"`) แต่ **ตอนนี้ยังเรียกใช้ไม่ได้** สายนี้
(GM) ไม่แตะไฟล์นี้รอบนี้ตามคำสั่ง COO `1059` ("fail-closed เหมือนเดิมทุกไบต์") แต่เขียนใบนี้ล่วง
หน้าเพื่อกันคุณเสียรอบค้นหาสิ่งที่อ่านจากซอร์สได้ตรง ๆ อยู่แล้ว

## จุดตันสองชั้น ไม่ใช่ชั้นเดียว (ตรวจโดย pf-adversary รอบนี้แล้ว)

`build_named_field_update(legacy, cache, identity_lo, identity_hi, x=7, value)`
(`attr_wire.py:423-454`) มีสองเงื่อนไขที่ต้องผ่านทั้งคู่ ไม่ใช่แค่ที่ COO-ORDER พูดถึง (การ seed
cache):

1. **`field[7]` (`known`) ต้องเป็น `True`** (`attr_wire.py:446-450`) -- ตอนนี้แถวของ `x=7`
   (`attr_wire.py:173`) คือ `(7, "basic", 0x0040, 0x054, 0x2A, "f32", "basic_f32_54", **False**,
   "unknown f32")` -- `known=False` เพราะตอนที่ตารางนี้เขียน ยังไม่มีการยืนยันชื่อ/ความหมายของ
   ฟิลด์นี้ ผ่านการตรวจสอบนี้ก่อนถึงเงื่อนไข cache เลย
2. **`cache` (`RawBlockCache`) ต้อง seed แล้ว** (`capture_initial()`) มิฉะนั้น `merged_with`
   raise -- นี่คือเงื่อนไขเดียวที่ COO-ORDER (`1101`) พูดถึงตรง ๆ

ทั้งสองเงื่อนไขเป็นอิสระจากกัน แก้ข้อ 2 (คุณมีฐาน `characters.actor_wire`/DB ของคุณเองอยู่แล้ว)
แต่ไม่แก้ข้อ 1 -- จะยังโดน `AttrWireError` เหมือนเดิม

## สาย GM ไม่ flip `known` เองตอนนี้ (COO สั่งตรง)

`known=False -> True` สำหรับ `x=7` เป็นการเปลี่ยนโค้ดจริงใน `gm/attr_wire.py` ซึ่งเป็นเขตเขียน
ของสาย GM COO `1059` สั่งให้คงไว้ "เหมือนเดิมทุกไบต์" จนกว่าคุณจะส่งมอบแหล่ง typed + วิธี compose
ที่ผ่าน pf-adversary -- สาย GM รอคำขอจากคุณ (จุดเสียบ chat command `/speed` ใน
`gm/chat_command.py` ตามที่ COO ระบุ) แล้วจะเปิด PR แก้ `known` ของ `x=7` พร้อมจุดเสียบใน PR
เดียวกัน ผ่าน pf-adversary ก่อน commit ตามปกติ

## ข้อมูลอื่นที่อาจช่วย (อ่านจากซอร์สจริง ไม่ใช่การเดา)

- ชื่อฟิลด์ปัจจุบันในตาราง (`"basic_f32_54"` / "unknown f32") เป็นชื่อ placeholder เก่ากว่า
  `PF_ATTR_FIELD_SEMANTICS.tsv` ที่ COO-ORDER อ้าง (`n_SPEED_WALK_...`/`FightAttr_run_speed_...`)
  -- แนะนำให้ชื่อจริงที่จะใช้แทนมาจาก tsv นั้น ไม่ใช่ placeholder เดิม เมื่อ PR แก้ `known`
- `encode_field`/`encode_block` (`attr_wire.py:265-348`) รองรับ `kind="f32"` อยู่แล้ว (struct pack
  `<f`) ไม่ต้องเพิ่ม kind ใหม่สำหรับฟิลด์นี้
- คู่ฟิลด์ที่ผูก mask bit เดียวกัน (x39/x40, x41/x42, `attr_wire.py:318-322`) ไม่เกี่ยวกับ x=7 --
  x=7 มี mask bit เดี่ยวของตัวเอง (`0x0040`) ไม่ต้องกังวลเรื่อง pairing

## nonclaim

1. ไม่อ้างว่าค่า default 400.0 ถูกยืนยันกับตาราง/ไบนารีแล้ว (COO-ORDER เองบอกว่ายัง "ยังไม่ยืนยัน
   ตาราง/ไบนารี ใช้ 400 เป็นค่าตั้งต้นได้")
2. ไม่ตัดสินแทนว่าแนว "base = blob creation + overlay" ของคุณปลอดภัยจริง (COO-ORDER เองสั่งให้
   pf-adversary ตรวจ claim bulk-copy `0x464F30` ก่อนส่งจริง -- นอกเขตของใบนี้)
3. ไม่ได้แก้ `gm/attr_wire.py`/`gm/chat_command.py` ในใบนี้ -- ข้อมูลอ่านอย่างเดียว

-- LANE-GM รอบ `p4cndg`
