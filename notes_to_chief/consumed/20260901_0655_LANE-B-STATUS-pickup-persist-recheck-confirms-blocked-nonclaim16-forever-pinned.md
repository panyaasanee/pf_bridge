[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: กะ1-B, เจ้าของ | จาก: LANE-B (COMBAT) รอบ `1yj0j0`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-09-01T06:55+07:00]
[ตอบใบ: `20260901_0245_COO-DECISION-pickup-wiring-stays-blocked-0145-corrected.md` (ไม่มีคำถามใหม่ --
ใบนี้รายงานผลการตรวจซ้ำที่ใบนั้นสั่งโดยนัย)]

# LANE-B STATUS -- ตรวจซ้ำ `mob_pickup_persist` ตามที่มอบหมาย: ยังบล็อกจริงทุกประการ
# ไม่มี src/-ต่อสายใหม่รอบนี้ ปักช่องโหว่ "forever" ของ NONCLAIM 16 เป็นเทสแทน (กฎ F)

## สรุปสั้น

ตรวจ `mob_pickup_persist.pickup_and_persist` ซ้ำที่ HEAD วันนี้ตามที่ได้รับมอบหมาย: **ยังไม่มี call
site ใน `runtime.py`** และควรเป็นอย่างนั้นต่อไป -- `COO-DECISION 20260901_0245` แก้ `0145` แล้วและ
ยึด `20260830_1145` เดิม (ห้ามต่อสายจนกว่า `GT-124` capture opcode จริง) ไม่มีจดหมายใหม่หลังจากนั้น
เปลี่ยนสถานะนี้อีก (ตรวจทุกไฟล์ที่ mtime ใหม่กว่ารอบ `h40iwu` ของสาย B เองแล้ว) จึงไม่มีอะไรต้องถาม
COO ซ้ำ -- ใบนี้เป็นการยืนยัน ไม่ใช่คำถาม

## รายละเอียดที่ตรวจ

1. `grep -rn mob_pickup_persist src/pirateforce_foundation/*.py` ที่ HEAD ของ
   `pirate-force-server` -- ไม่มี caller ใหม่, `GAME_TEST_QUEUE.md`'s `GT-124`
   ยัง `BLOCKED-ON-WIRING`, `GT-146` ยัง `PENDING`, `RE-125` ยังปิดแบบ bounded-negative
2. เส้นทางอื่นที่เคยเปิดใน `h40iwu` (Bg0015 gate 1-4, `mob_aggro.ATTACK_INTENT_DELIVERABLE`) --
   ตรวจซ้ำทุกข้อ ยังปิดเหมือนเดิมทั้งหมด ไม่มีอะไรขยับ

## งานที่ทำแทน (กฎ F -- ไม่มีรอบว่างเปล่า)

`mob_pickup.py` NONCLAIM 16 อ้างมานานว่าถ้าผู้เรียกข้าม precheck ของ `mob_pickup_persist` (สูตรสอง
ขั้นเดิมที่ `MOB_PICKUP_WIRING` เก็บไว้เป็นบันทึกเหตุผลเท่านั้น) แล้วเขียน DB ล้มเหลวครั้งหนึ่ง
"ทุกการเก็บของถัดไปในเซสชันจะถูกปฏิเสธด้วยเหตุผล identity **ตลอดไป**" -- ตรวจแล้วไม่มีเทสไหนพิสูจน์
คำว่า "ตลอดไป" จริง (เทสเดิมพิสูจน์แค่ครั้งเดียว จากสถานการณ์ drift ที่ปิดตัวเองได้พอดีหลังครั้งแรก --
ลองสร้างเทสตามสูตรนั้นก่อนจริง ๆ แล้วพบว่าครั้งที่สองผ่าน ไม่ตรงคำอ้าง จึงเปลี่ยนสถานการณ์เป็น mock
เขียนล้มเหลวทุกครั้งแทน ซึ่งพิสูจน์ "ตลอดไป" ได้จริง)

เพิ่มเทส `test_without_the_precheck_every_later_pickup_keeps_failing_the_same_way` ใน
`tests/test_mob_pickup_persist.py` (สาย B, ไฟล์เดียว, +55 บรรทัด, ไม่แก้เทสเดิม) พิสูจน์ 3 รอบติดว่า:
ของหายทุกรอบ, เหตุผลการปฏิเสธเดิมทุกรอบ, identity ที่ mint คนละค่ากันทุกรอบ (เครื่องหมายในหน่วยความ
จำเดินหน้าเรื่อย ๆ ไม่มีวันหยุด), ไม่มีแถวไหนถึงตารางจริง

**mutation-proof**: ลบ `self._issued_through = item.identity` ใน `BagCell.commit_pickup` ชั่วคราว ->
เทสแดงด้วยคนละ exception เลย (`identity_high_water_below_the_bag`) -> revert เป๊ะ (`git diff` ว่าง
ก่อน commit)

## ตัวเลขที่วัดได้

```
ไฟล์ที่แตะ (pirate-force-server) รวม 2: tests/test_mob_pickup_persist.py,
  rounds/B_20260901_0647_1yj0j0_pickup-persist-status-recheck-nonclaim16-forever-pinned.md
เทสใหม่: 1 ใบ
เฉพาะไฟล์ที่แก้: 116 passed, 133 subtests passed (ก่อนแก้ 115 passed)
สวีตเต็มหลังแก้: 6155 passed, 323 skipped, 13141 subtests passed, 0 failed (157.64s)
(diff เป็น pure-addition ตรวจแล้ว -> เดลต้า +1 passed เป๊ะ ไม่รัน baseline แยกเพราะสวีตเต็มใช้เวลา
~2.5 นาที/ครั้งและ diff พิสูจน์แล้วว่าไม่แตะเทสเดิมสักบรรทัด)
```

`runtime.py`/`app.py`: ไม่แตะ · `field_mobs._SCENE_TABLE_MODULES`: ไม่แตะ · `mob_pickup.py`/
`mob_pickup_persist.py` โค้ดทำงานจริง: ไม่แตะ (มิวเทตชั่วคราวเพื่อพิสูจน์เทสแล้ว revert หมด)

## ยังไม่ได้พิสูจน์

- `mob_pickup_persist` ยังบล็อกเหมือนเดิมทุกประการ -- รอ `GT-146`/`GT-124` เท่านั้น
- gate 1-4 ของ Bg0015, `mob_aggro.ATTACK_INTENT_DELIVERABLE` -- ไม่มีอะไรเปลี่ยนจากรอบ `h40iwu`

## CORE-REQUEST

ไม่มี

## ตัวเลือก

ไม่มี -- ใบนี้ยืนยันสถานะ ไม่ใช่คำถามที่ต้องเลือก

-- LANE-B (COMBAT) รอบ `1yj0j0`
