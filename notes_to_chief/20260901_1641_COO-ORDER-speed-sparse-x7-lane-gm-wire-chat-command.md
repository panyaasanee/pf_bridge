[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: chief, LANE-DB, เจ้าของ | จาก: COO · 2026-09-01T16:41+07:00]
[อ้าง: `20260901_1640_COO-ORDER-speed-sparse-x7-approved-panya-live-override-of-1447.md` (คำสั่งคู่กันถึง LANE-DB),
Panya ยืนยันสดในเซสชัน 2026-09-01 16:39+07: "ส่ง /speed ให้รอบเทสพอใช้งานได้ก่อน แล้วค่อยรอผล RE ไปด้วย"]

# COO-ORDER — ต่อสาย `/speed` chat command เข้ากับ sparse path ของ LANE-DB (x=7 เท่านั้น)

## ตัดสินว่าอะไร

อนุมัติเปิดจุดส่งของ `/speed <ค่า>` ใน `runtime.py`/`UPDATE_ATTR_VITAL_VERSION_CONFIRMED` ให้เรียก
เส้นทาง sparse ของ LANE-DB (ตั้งเฉพาะ mask bit x=7 ฟิลด์เดียว) **ห้ามส่งบล็อกเต็ม 55 ฟิลด์** จนกว่า COO
จะสั่งเปิดแยกต่างหาก ไม่ต้องรอผล RE-193 — เดินหน้าได้ทันทีที่ LANE-DB ส่ง interface มา

## เพราะอะไร

ดูใบคู่กันถึง LANE-DB รอบนี้ (`1640`) — ความเสี่ยงจำกัดอยู่ที่ run-copy DB ของรอบเทส attended เท่านั้น
ไม่ใช่ของถาวร เจ้าของยืนยันสดให้เดินหน้าไม่ต้องรอ RE

## ใครทำอะไรต่อ

LANE-GM: ต่อสาย chat command → sparse path (ประสานรับ interface จาก LANE-DB) ทดสอบเฉพาะบน
run-copy DB ของ GT test เท่านั้น ห้ามชี้ canonical

## กำหนดเมื่อไร

เร่ง — พร้อมทันทีที่ LANE-DB ส่ง interface มา ไม่ผูกกับ RE-193

— COO
