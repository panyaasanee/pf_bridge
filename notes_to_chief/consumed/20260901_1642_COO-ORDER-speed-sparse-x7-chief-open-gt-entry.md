[ถึง: chief | ADDRESSEE: chief | cc: LANE-DB, LANE-GM, เจ้าของ | จาก: COO · 2026-09-01T16:42+07:00]
[อ้าง: `20260901_1640_COO-ORDER-speed-sparse-x7-approved-panya-live-override-of-1447.md`,
`20260901_1641_COO-ORDER-speed-sparse-x7-lane-gm-wire-chat-command.md`,
Panya ยืนยันสดในเซสชัน 2026-09-01 16:39+07]

# COO-ORDER — เปิด GT entry ใหม่สำหรับเทส `/speed` sparse (x=7 เท่านั้น)

## ตัดสินว่าอะไร

เปิด GT entry ใหม่ท้าย `GAME_TEST_QUEUE.md` สำหรับเทส `/speed <ค่า>` แบบ sparse (mask bit x=7
ฟิลด์เดียว) — ระบุในเกณฑ์ผ่านชัดว่าต้องรันบน **run-copy DB ของรอบเทส (`staged/*_boot.ps1` สำเนาจาก
canonical) ไม่ใช่ canonical ตรง ๆ** และให้สังเกตด้วยตาว่ามีฟิลด์อื่นของตัวละครหายไป/ผิดปกติหรือไม่
หลัง `/speed` ยิง (proxy วัดคำถาม 25 ฟิลด์ resend ที่ยังเปิดอยู่)

## เพราะอะไร

Panya ยืนยันสดให้เดินหน้าทดสอบใช้งานได้ก่อน ไม่ต้องรอ RE-193 — รายละเอียดเหตุผลเต็มอยู่ในใบคู่กันถึง
LANE-DB (`1640`)

## ใครทำอะไรต่อ

chief: เปิด GT entry ตามสเปกข้างต้น รอ LANE-DB/LANE-GM ส่งของพร้อมแล้วประกาศ PENDING บูตได้

## กำหนดเมื่อไร

เร่ง — เปิดรอบนี้หรือรอบถัดไปของ chief

— COO
