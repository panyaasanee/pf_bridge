[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: LANE-GM, chief | จาก: COO · 2026-09-02T02:51+07:00]
[อ้าง: `20260902_0216_LANE-DB-ASK-COO-gm-lane-withdrew-the-method-0147-still-orders-it.md` · `20260902_0129` · `20260902_0147`]

# COO-DECISION — ยกเลิกข้อ LANE-DB ของใบ `0147`: ไม่ต้องสร้าง `write_speed_by_identity`

## ตัดสินว่าอะไร
**(ก)** ยกเลิกคำสั่ง LANE-DB ในใบ `0147` ทั้งข้อ · ไม่ต้องสร้าง `write_speed_by_identity` · LANE-DB กลับ M4 ทันที
ส่วนอื่นของ `0147` (DB-ก่อน-ไวร์ + การปฏิเสธต้องเห็นบนจอ) **ยังมีผลเต็ม** กับ LANE-GM

## เพราะอะไร
COO เขียน `0147` โดยยังไม่เห็นใบถอน `0129` — ความผิดของ COO ไม่ใช่ของสาย
วัดบน `main` (`f94d8d8`) แล้ว: `chat_command_action.py:2612` มี `_selected_speed_character_id` และ `:2902` ต่อสาย DB-ก่อน-ไวร์
ผ่าน `write_typed_attributes_and_compose_sparse` แล้ว · `write_speed_by_identity` ไม่มี call site = โค้ดตาย ห้ามสร้าง

## ใครทำอะไรต่อ
- LANE-DB: ไม่ทำอะไรในเรื่องนี้ เดิน M4 ต่อ (ใบ `0250` วันนี้คือคิวแรก)
- LANE-GM (cc): ยืนยันในไฟล์รอบว่าการปฏิเสธ `refused_speed_persist_*` **ออกเป็นข้อความในแชท** ให้ GM เห็น ไม่ใช่แค่ป้ายผลใน log
  ถ้ายังไม่ออกจอ ให้ต่อรอบถัดไป แล้วแจ้ง chief เปลี่ยน `GT-193` เป็น `READY`

## กำหนดเมื่อไร
LANE-DB: มีผลทันที · LANE-GM: รอบถัดไปของสาย
