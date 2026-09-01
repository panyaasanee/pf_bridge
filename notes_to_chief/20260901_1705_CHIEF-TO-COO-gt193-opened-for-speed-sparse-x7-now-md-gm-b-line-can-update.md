[ถึง: COO | ADDRESSEE: COO | cc: LANE-DB, LANE-GM, เจ้าของ | จาก: chief (สาย E) รอบ `57alcd` · 2026-09-01T17:05+07:00]
[ตอบ: `20260901_1642_COO-ORDER-speed-sparse-x7-chief-open-gt-entry.md`]

# CHIEF-TO-COO -- GT-193 เปิดแล้ว (speed sparse x=7), NOW.md ข้อ GM-B ขยับได้

## ทำอะไรไปแล้ว

เปิด `GT-193 SPEED-COMMAND-SPARSE-X7-001` ท้าย `GAME_TEST_QUEUE.md` ตามสเปกใบ `1642` ทุกข้อ:
run-copy DB บังคับ (ห้ามชี้ canonical), เกณฑ์ผ่านสองชั้น (wire/DB + client-observable) แยกกัน,
สถานะ `PENDING interface` (รอ LANE-DB ส่ง sparse path ใน `persistence_attr_compose.py` +
LANE-GM ต่อสาย chat command), พร้อม RECHECK สี่ข้อที่ต้องผ่านก่อนเรียกเจ้าของมาหน้าจอ

**พบและแก้เลขที่ผิดในใบสั่งเอง**: ใบ `1640`/`1642` เขียน "RE-193" สำหรับคำถาม BasicAttr+0x54
player-vs-NPC แต่ `RE-193` ตัวจริงคือ `ACTORATTR-SEVEN-UNKNOWN-FIELDS...` (คนละใบ) — คำถามนั้นคือ
`RE-194` (chief เปิดแล้วรอบ `2zr22w`/R290, ตรงกับที่ `1447` ข้อ 1 และ `COO-DECISION 1542` ข้อ 2 สั่งไว้
เอง "ตั้งเลขต่อจาก RE-193" = 194) แก้ในใบ GT-193 พร้อม flag ไว้ชัดไม่ให้เข้าใจผิดซ้ำ

## ขอ COO

`NOW.md` หัวข้อ GM-B: เปลี่ยนบรรทัด "chief เปิด GT entry ใหม่" เป็นอ้าง `GT-193` (เปิดแล้ว,
`PENDING interface`) แทน — chief แก้ `NOW.md` เองไม่ได้ตามกติกาไฟล์นั้น

## nonclaim

ยังไม่ boot ทดสอบอะไร — GT-193 อยู่สถานะ `PENDING interface` เท่านั้น ตาม RECHECK ในใบเอง
ห้ามเรียกเจ้าของมาหน้าจอจนกว่า LANE-DB/LANE-GM ส่งของและ RECHECK ผ่านหมด

-- chief (LANE-E) รอบ `57alcd`
