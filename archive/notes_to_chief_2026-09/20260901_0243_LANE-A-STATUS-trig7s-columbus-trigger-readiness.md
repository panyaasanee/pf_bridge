[ถึง: chief | ADDRESSEE: chief | จาก: สาย A (WORLD) รอบ `trig7s` | 2026-09-01T02:43+07:00]

# สถานะรอบ `trig7s` - Columbus trigger readiness (ฝั่ง "ยืนอยู่จริงไหม" ของอีกเจ็ดเกาะ)

## สรุปสั้น

ตรวจคิว (`CLIENT_RE_QUEUE.md`, `GAME_TEST_QUEUE.md`) ก่อนเริ่ม - ไม่มีของใหม่ที่ตอบได้ทันทีตรงกว่า M2
fallback ตามกฎเดิม ("ระหว่างรอ RE ของ Columbus ให้ทำ M2 ขั้นถัดไป") จึงอ่าน M2 backlog ทั้งชุดแล้วพบว่า
`world_m2_sea_destination.py`'s เองบอกไว้ตรง ๆ ว่าฝั่ง **arrival** ของอีกเจ็ดเกาะถูกวัดครบแล้ว
(`sea_map_lines`) แต่ฝั่ง **trigger** (Columbus ของแต่ละเกาะยืนอยู่จริงในสำมะโนหรือไม่) "unmeasured by
this module" - รอบนี้วัดช่องนั้น

## งานที่สร้าง

โมดูลใหม่ `world_m2_columbus_trigger_readiness.py` วัดว่า Columbus แต่ละเกาะ (จาก `COLUMBUS_ROUTES`
8 แถว) ปรากฏจริงในตาราง identity/population ของฉากบ้านตัวเองหรือไม่ โดย reuse ตารางที่มีอยู่แล้วทั้งหมด
(ไม่เขียน selector ใหม่) ต่อกับ call site เดิมของ `dispatch_columbus_quest3021` ที่ `runtime.py` เรียกอยู่
แล้วทุกบูต - **ไม่ต้องแตะ `runtime.py` เลยรอบนี้**

ผลวัด: 7 จาก 8 เกาะ PLACED (Port Royal + หกเกาะที่เหลือยกเว้น Prison Exile) 1 เกาะ (Prison Exile) พบ MOBS
n_ID ไม่ตรงกับที่ตารางเส้นทางอ้างไว้ (36 ที่มีจริง vs 360 ที่ควรมี) - ไม่ได้เดาแก้ เปิดใบ `RE-173` ให้สาย C
หา crosswalk จริงแทน (รายละเอียดเต็มในใบ)

งานเสริม: ปิด `RE-171` (BG0006 CJK name) เป็น bounded-negative (ค้นครบต้นไม้ ไม่พบตารางสำรอง) ไม่มีการ
แก้โค้ด และ consume จดหมาย COO เรื่อง door-reader-precedence (self-close ตามที่จดหมายสั่งเอง)

## เทส

ทั้งชุด `tests/`: 6089 passed, 327 skipped, 13115 subtests passed, 0 failed (227s) เทสใหม่/แก้ที่
เกี่ยวข้องโดยตรง: 161 passed, 11 subtests passed

## CORE-REQUEST

ไม่มีรอบนี้ - งานทั้งหมดต่อกับ call site เดิม ถ้าอนาคตต้องการให้เจ็ดเกาะ dispatch ได้จริง (ไม่ใช่แค่
รายงาน) นั่นคือ CORE-REQUEST ใหม่ที่ยังไม่ได้ขอ เพราะปลายทางทั้งเจ็ดยังไม่มี arrival spawn ที่เจ้าของ
decree ไว้ (ดูรายละเอียดในไฟล์ round)

## ไม่มี ASK-COO รอบนี้

ไม่มีเงื่อนไขบล็อกจริงสามข้อ (เปลี่ยนทิศทางโปรเจกต์ / undo ไม่ได้ / ขัดคำตัดสินเดิม) - เป็นสถานะรายงาน
ปกติ

— สาย A (WORLD)
