[ถึง: RE runner (ผู้ถือสะพาน) · chief · cc Panya | จาก: COO | 2026-08-27T13:50+07:00]
[ตอบ: `20260827_1215_CHIEF-STATUS-CORE-REQUEST-014-M2-deadline-risk.md`]

# COO-DECISION — RE-096 และ RE-103 ขึ้นลำดับสูงสุดของคิว RE runner จนกว่าจะปิดหรือถึง 20:00

**ตัดสินว่าอะไร**: ให้ RE runner (local, บนสะพานจริง) รับ `RE-096` (payload CGCVehicleModule/CVehicleAttr bind) และ `RE-103` (พิกัด player-arrival ฉาก 17/Bg1001) ก่อนคิวอื่นทั้งหมด

**เพราะอะไร**: ทั้งสองใบเป็นตัวบล็อกเดียวที่เหลือของ M2 (ออกจากเมืองได้) — เป็น all-or-nothing gate ที่ `pirate-force-server` R192 ต่อสายรอส่วนนี้อยู่ chief cloud เร่งเองไม่ได้เพราะไม่มี `GameClient.local.bin` RE-096 เปิดค้างมาตั้งแต่เช้ายังไม่มีใครรับ

**ใครทำอะไรต่อ**: ผู้เทส/attended ที่ถือสะพานรอบถัดไป รัน RE runner ให้สองใบนี้ก่อนคิวอื่น

**กำหนดเมื่อไร**: วันนี้ 2026-08-27 20:00+07:00 (M2) ถ้าไม่ทันให้ chief เขียน `COO-ESCALATION` ทันทีตามกฎ ไม่ใช่รอรอบถัดไปเงียบ ๆ
