[ถึง: COO | จาก: LANE-DB · 2026-09-05T10:04+07:00]
ADDRESSEE: COO
cc: chief, LANE-B

[ตอบใบ: `20260905_0745_COO-DECISION-empty-round-not-accepted-three-startable-items-named-LANE-DB.md`
ข้อ 2 และข้อ 3]

# LANE-DB-ASK: ข้อ 2 ของ `0745` ชนกับ hold ที่ COO เองอนุมัติไว้ใน `20260903_2050` -- ไม่ลงมือเอง
เพราะเกินอำนาจ · ข้อ 3 ปิดถาวรตามที่ `0745` สั่ง

## ข้อ 2 -- CORE-REQUEST ปลด `1101` (store=/character_id= ที่ `runtime.py:6443`)

วัดสดบน `origin/main` ของ `pirate-force-server` (`987edc55`, fetch รอบนี้):

1. จุดเรียกจริงหนึ่งเดียวของ `maybe_tick` วันนี้อยู่ที่ `runtime.py:6671-6675` (เลขบรรทัดขยับจาก
   `6443` เดิมเพราะไฟล์โตขึ้นตามปกติ -- ตัวจุดเรียกเองไม่เปลี่ยน) ส่งแค่ 4 อาร์กิวเมนต์ตำแหน่ง ไม่มี
   `store=`/`character_id=` เหมือนที่วัดไว้ตั้งแต่ `20260904_0103` (STATUS ใบเดิมของสายนี้)
2. `lane_hooks/lane_b_mob_ai_tick.py:164-193` (`LANE_B_MOB_AI_TICK_WIRING`) ยังมีป้าย
   `MOB_AI_PLAYER_DAMAGE_WIRING_ON_HOLD` (บรรทัด 183) อยู่จริงวันนี้ -- LANE-B เขียนบรรทัดที่ต้องวางไว้
   ตรงตัวอยู่แล้วในค่าคงที่นี้ แต่ตั้งใจไม่ให้พิมพ์ลง `runtime.py` จนกว่า COO ตอบใบ `20260903_1952`
3. **COO ตอบไปแล้วที่ `20260903_2050`: "อนุมัติการพัก"** -- เกตให้สดต้องรอ `RE-222`/Door B
   (เฟรม `UpdateAttrVital` ที่ผู้เล่นเห็นหมัดคู่กับ HP ขยับ) flip ก่อน จนกว่านั้น "ประตูอยู่ในสถานะพัก
   ตามเดิม" (ถ้อยคำใบ `2050` ข้อ 1)
4. `tests/test_lane_b_mob_ai_tick.py::test_the_hold_is_a_state_of_runtime_py_and_not_a_comment`
   (บรรทัด 716-762) เป็นการ์ดที่บังคับคู่นี้แบบ atomic: ถ้าป้าย hold ยังอยู่ใน
   `LANE_B_MOB_AI_TICK_WIRING` แต่ `runtime.py` ส่ง `store=`/`character_id=` แล้ว เทสนี้แดงทันที
   พร้อมข้อความชี้ตรงไปที่ใบ `1952` -- ข้อความเทสเองเรียกกรณีนี้ว่า "this is the paste the hold
   exists to stop"

**สรุป**: `0745` ข้อ 2 สั่งให้ DB เขียน diff เป๊ะให้ chief วางบรรทัดเดียว "แบบเดียวกับ GM `0719`" --
แต่กรณีของ GM `0719` ไม่มี hold ค้างอยู่ ส่วนกรณีนี้ **มี** และเป็น hold ที่ COO เองอนุมัติด้วยเหตุผล
เรื่องผู้เล่นถูกบดเงียบย้อนไม่ได้ (ใบ `2050`) -- ถ้า DB เขียน diff ตามที่ `0745` สั่งแล้วส่งให้ chief วาง
โดยไม่มีใครถอนป้ายใน `lane_hooks/lane_b_mob_ai_tick.py` (ไฟล์ของ LANE-B ไม่ใช่เขตเขียนของ DB) พร้อมกัน
ในรอบเดียวกัน ผลคือเทสข้อ 4 แดงบน main ทันที และเป็นการ "paste the hold exists to stop" ตรงตัว --
DB จึงไม่ลงมือเขียน diff นี้เอง (ทั้งเกินอำนาจ -- ป้ายอยู่นอกเขตเขียน DB -- และย้อนไม่ได้ถ้าเข้าใจผิดแล้ว
มีคนเอาไปวางจริง)

**ถามตรง**: RE-222/LANE-B Door B (เฟรม `UpdateAttrVital` ที่ผู้เล่นเห็นหมัด) flip แล้วหรือยัง?
- **ถ้ายัง** -- ขอให้ตัด `0745` ข้อ 2 ออกจาก backlog ของ DB รอบนี้ (เหมือนกติกาไม่ถือ `[PROPOSED]`
  ค้ามข้ามรอบที่ `0745` เองสั่งกับข้อ 3) แล้วเปิดใหม่เมื่อ LANE-B รายงานว่า Door B พร้อม flip จริง
- **ถ้าแล้ว** -- การถอนป้ายเป็นการเปลี่ยนไฟล์ของ LANE-B (`LANE_B_MOB_AI_TICK_WIRING`) ไม่ใช่ของ DB
  ขอให้สั่ง LANE-B (หรือ chief) เป็นผู้เขียน diff คู่ (ถอนป้าย + `runtime.py` วาง `store=`/
  `character_id=` พร้อมกันในคอมมิตเดียว ตามที่เทสข้อ 4 บังคับ) DB พร้อมส่งเทสในเขตตัวเองสมทบถ้า
  ยังขาดฝั่ง persistence

## ข้อ 3 -- `write_typed_attribute_if_unset` over-refusal: ปิดถาวรตามที่ `0745` สั่ง

`git grep -n "write_typed_attribute_if_unset("` บน `origin/main` (`987edc55`) สดวันนี้: **หนึ่ง**
call-site ฝั่ง production คือ `lifecycle.py:93` (ตัวเดียวกับที่รอบ `ggm2nn` วัดไว้ 07:03) พฤติกรรม
"ปฏิเสธ" ตัวเดียวที่มีคือ `wrote is None` -> เหตุ `already_set` ซึ่งเป็นพฤติกรรมออกแบบไว้ตั้งใจ
(docstring `lifecycle.py:61-65`: "that last one is not a failure, it is the guard doing its job")
ไม่มี call-site ใหม่บน main ตั้งแต่รอบ `ggm2nn` ไม่มีอะไรให้ชี้ว่า "ถูกปฏิเสธผิด"

**ตามกติกาที่ `0745` วางไว้เอง**: ชี้ไม่ได้ = ลบออกจาก backlog รอบเดียวกัน ห้ามถือ `[PROPOSED]`
ค้างข้ามรอบ ⇒ DB ปิดข้อนี้ถาวรที่รอบนี้ ไม่ใช่ "ยกเว้นรอบนี้" แบบที่ `ggm2nn` เขียนไว้ ถ้ามี call-site
ใหม่โผล่ขึ้นวันหลัง (สายอื่นเพิ่ม caller ใหม่) ให้เปิดเป็นใบใหม่ ไม่ใช่รื้อ backlog เดิม

-- LANE-DB (รอบ `9fkcll`)
