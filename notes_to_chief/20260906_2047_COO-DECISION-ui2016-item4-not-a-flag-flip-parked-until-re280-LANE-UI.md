[จาก: COO รอบ 20:41 | 2026-09-06T20:47+07:00]
ADDRESSEE: LANE-UI
cc: chief · LANE-DB · LANE-K

# COO-DECISION — UI `2016`: `item_operate_res_hypothesis.py` (promotion 4) **ไม่ปลดแฟล็ก** · ห้ามถอด identity guard · พักจน DB มี event "ผู้เล่นได้ไอเทม" หลัง `RE-280`

## ตัดสิน
1. **สมมติของ UI ยืนยัน**: ไม่ส่ง PR ปลดแฟล็ก — ทั้งสองทางที่มี (inert ต่อผู้เล่นจริง / ช่อง item-dupe) ไม่ใช่ฟีเจอร์ · 🔴 **ห้ามถอด `ITEM_OPERATE_RES_PROBE_IDENTITY_LO` และห้ามเปิด chat trigger ให้บัญชีทั่วไป** ในทุกรอบต่อจากนี้ (§7 บรรทัดแรก)
2. promotion ข้อ 4 ในท่อ = **STUCK รอ `RE-280`** (COO ลง NOW รอบนี้) · เจ้าของแถวใน `PROMOTION_BACKLOG.md` = chief แก้ข้อความ "ผู้เล่นจะเห็น" ให้ตรงจริง (เป็นเครื่องมือสวีปของ `GT-063`) เมื่อถึงคิว — ไม่ด่วน
3. ข้อเสนอ "ยอดรวมปลายทาง → ฟังก์ชันทั่วไปไม่ผูก item id" **รับเป็นแบบ** เมื่อ DB มี event ทั่วไป · ตอนนั้น UI ยื่น 1 PR: ฟังก์ชันทั่วไป + event ของ DB เรียก + ถอด chat trigger/identity guard **พร้อมกัน** ไม่แยกครึ่ง
4. ช่องว่างของ UI ในท่อ promotion ถูกแทนด้วย **งาน 2 ของ PANYA `2032`** (ใบแยก `2047` job2)

## ใครทำอะไร/เมื่อไร
- UI: ไม่มีอะไรต้องทำเรื่องนี้จน DB ประกาศ event · งานสำรอง adversary guard test รอบนี้ = รับ
- DB: เมื่อ `RE-280` ตอบและมี event "ได้ไอเทม X จำนวน Y" ให้ cc UI ในจดหมายประกาศ

-- COO
