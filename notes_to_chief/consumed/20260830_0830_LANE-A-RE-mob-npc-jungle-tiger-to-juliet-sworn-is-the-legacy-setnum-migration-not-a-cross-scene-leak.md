[ถึง: กะ attended (คำถามข้อ ④ ใบ 20260830_0030) · chief | ADDRESSEE: LANE-A | cc: COO, สาย B, สาย GM, เจ้าของ | จาก: สาย A (WORLD) รอบ `n4wj7k` · 2026-08-30T08:30+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 08:18]
[ตอบใบ: `20260830_0030_KA3A-GT131-PASS-owner-confirmed-gt151-partial-plus-four-polish-gaps-and-mob-vs-npc-question.md` ข้อ ④]

# LANE-A ตอบคำถามเจ้าของ — mob→npc ที่ท่าเรือฝั่งเรือเหลือง: ใช่ CLINE resolve จริง แต่กลไกไม่ใช่ตามสมมติฐาน

## สรุปคำตอบ

**ยืนยันครึ่งแรกของสมมติฐาน (การสลับมาจาก CLINE resolve) แต่หักล้างกลไกที่เสนอ (การรั่วของ roster
บล็อก 36-66 จาก Spice Paradise)** จากตารางที่ commit ไว้แล้วในเรโป ไม่ต้องเปิดไคลเอนต์เพิ่ม:

`src/pirateforce_foundation/world_port_royal_identity.py` แถว `WITHDRAWN_UNDER_THIS_RULE`
(บรรทัด `(58, 60, 'Jungle Big Tiger', 741, 'Juliet')`) บันทึกไว้ตรง ๆ ว่า placement ที่กติกา
**เก่า** (`LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION` ในไฟล์เดียวกัน) เคยให้ template_id `60`
ชื่อ **"Jungle Big Tiger"** — ตัวเดียวกับที่กะ3-A เห็นรอบก่อน — ส่วนกติกา**ปัจจุบัน** (CLINE crosswalk)
ให้ template_id `741` ชื่อ **"Juliet"** role **"Sworn"** ที่ placement เดียวกัน ตรงกับสิ่งที่กะ3-A
เห็นวันนี้ทุกตัวอักษร (`(60, 741, 'P_FEMALE_012_002_FRIEND', 'Juliet', 'Sworn')` ใน
`SHIPPED_PLACEMENTS` ของไฟล์เดียวกัน)

คอมเมนต์เหนือ `LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION` (ตอนนี้ว่างเปล่า) เขียนไว้ตรง ๆ ว่า
เก้าแถวนี้ **"ถูกส่งอีกหนึ่งรอบเท่านั้นภายใต้ `COO-DECISION 2026-08-29T00:41+07:00`"** แล้วย้ายเข้า
`WITHDRAWN_UNDER_THIS_RULE` ครบทุกแถว — นี่คือกลไกจริง: **หน้าต่างโยกย้ายที่กำหนดไว้ล่วงหน้าของฉาก
เดียวกัน (bg0001) ไม่ใช่ roster ของฉากอื่นรั่วเข้ามา**

## ทำไมกลไกที่กะ3-A เสนอ (บล็อก 36-66 / Spice Paradise) จึงไม่ใช่

สมมติฐานอ้าง "Mob-Set ของไฟล์ฉากลงช่อง MOBS n_ID ⇒ ได้ identity จากบล็อก 36-66 = roster Spice
Paradise" — ไม่พบโค้ดหรือตารางใดใน `src/` ที่ผูก placement นี้กับบล็อก Spice Paradise โดยตรง
กลไกที่วัดได้จริงง่ายกว่านั้น: เป็นการอ่าน Mob-Set number แบบเก่า (ก่อน crosswalk ไป CLINE) เทียบ
กับกติกาใหม่ที่อ่านผ่าน `CLINE[n_CLINE_TYPE == <ประเภทฉาก> and n_CREATURE_TYPE == <Mob-Set>]`
(ตามที่ `world_m2_sea_destination.py` บันทึกไว้สำหรับฉากอื่น — หลักการเดียวกันใช้กับ bg0001)
ไม่มีการข้ามฉาก ไม่มี block 36-66 เข้ามาเกี่ยวข้องเท่าที่ตารางที่ commit แล้วแสดง

## หลักฐาน

- `src/pirateforce_foundation/world_port_royal_identity.py`:
  - `WITHDRAWN_UNDER_THIS_RULE` รายการ `(58, 60, 'Jungle Big Tiger', 741, 'Juliet')`
  - `SHIPPED_PLACEMENTS` / ตารางดิบ รายการ `(60, 741, 'P_FEMALE_012_002_FRIEND', 'Juliet', 'Sworn')`
  - `LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION = []` พร้อมคอมเมนต์อ้าง
    `COO-DECISION 2026-08-29T00:41+07:00` ("nine rows get one round only")
- 🔴 **ป้ายกำกับ ยังไม่ยืนยัน**: เลข placement_index ในสองตาราง (`58` ใน `WITHDRAWN_UNDER_THIS_RULE`
  กับ `60` ใน `SHIPPED_PLACEMENTS`) **ไม่ตรงกันเป็นตัวเลข** แม้ `template_id`/ชื่อจะตรงกันทุกตัวอักษร
  ผมยังไม่ตามรอยว่าสองตารางนี้นับ index คนละฐานหรือเป็นความคลาดเคลื่อนจริง — ไม่ฟันธงว่า placement 58
  ในสายตากะ3-A คืออันเดียวกับแถว SHIPPED index 60 เป๊ะ จนกว่าจะมีคนไล่ index สองตารางนี้เทียบกัน
  (งานนี้เล็ก ยกให้รอบสาย A ถัดไปหรือใบ `RE-` ถ้าจำเป็น)

## สิ่งที่ไม่ได้ทำ

ไม่ได้ปิดใบ `20260830_0030` เอง (ใบนั้นเป็นของกะ attended เปิด ไม่ใช่ของสายนี้เปิด — เขียนตอบแล้ว
วางไว้ให้กะ attended/chief เห็น) · ไม่ได้แตะไฟล์ `world_port_royal_identity.py` เอง (คำถามเป็นเรื่อง
อ่านหลักฐาน ไม่ใช่เรื่องต้องแก้โค้ด) · ไม่ได้ปิดข้อ 🔴 เรื่อง index ไม่ตรงกัน เพราะยังไม่มีหลักฐานพอ

— สาย A (WORLD) รอบ `n4wj7k`
