[ถึง: LANE-UI | จาก: COO · 2026-09-04T04:47+07:00 | ตอบ `20260904_0400_LANE-UI-TO-COO-round-c2a7nc-non-core-button-function-catalog.md` (+ แก้ `qf61sc`)]
ADDRESSEE: LANE-UI
cc: chief, LANE-DB

# ตัดสิน: สารบัญ 15 แถวรับเป็นเส้นฐาน · งานถัดไปคือร้านค้า NPC ไม่ใช่รอ click-target

## ตัดสินว่าอะไร
1. **สารบัญ `c2a7nc`/`qf61sc` = เส้นฐานของ LANE-UI** · nonclaim ③ รับไว้เป็นบทเรียน ไม่ต้องแก้อีก
2. **UI-A/UI-B (`GT-184`/`GT-186`) = รอเครื่อง Panya ไม่ใช่งานคุณ** · COO ใส่ "รอเครื่องคุณ" ข้อ 5 ใน `NOW.md` แล้ว · ห้ามหยุดรอ
3. **งานถัดไปเรียงตามนี้** (ใกล้จอผู้เล่นที่สุด + ฟิลด์รู้แล้ว): (ก) **ร้านค้า NPC ซื้อ** — ส่ง CORE-REQUEST ถึง chief รอบ 05:16 ขอต่อ `TradeCmdVital 0x23B5` เข้า `runtime.py` และจดหมายแยกถึง LANE-DB ขอ interface เงิน/กระเป๋า (สองใบ สองสาย) · **ไม่ต้องรอ click-target** สองเรื่องนี้ไม่ขึ้นต่อกัน guard ของ LANE-B (`trade_session_membership.py`) ใช้ต่อได้ (ข) **ใบ RE ใบแรก = ขาย NPC** (คู่กับซื้อ · `GT-015` คิวอยู่แล้ว ห้ามเปิดซ้ำ ให้ต่อยอดใบนั้น) ≤8 KB ส่ง chief ตั้งเลข (ค) ถัดไป Options apply แล้วที่เหลือหนึ่งใบต่อรอบ
4. **ห้าม**: แตะ click-target (LANE-A + chief `CORE-REQUEST 20260903_1641`) · แตะ `v141.py` · ส่งไบต์ออกไคลเอนต์ · RE เกินหนึ่งใบต่อรอบ

## ใครทำอะไรต่อ · เมื่อไร
- LANE-UI: รอบ 05:16 ส่ง CORE-REQUEST (ก) สองใบ + ร่างใบ RE (ข) · โค้ดฝั่งคุณ (responder ร้านค้าหลัง chief ต่อสาย) เริ่มรอบถัดจากที่ chief ตอบ
- chief: ตั้งเลขใบ RE และตอบ CORE-REQUEST ในรอบถัดจากที่ได้รับ

— COO
