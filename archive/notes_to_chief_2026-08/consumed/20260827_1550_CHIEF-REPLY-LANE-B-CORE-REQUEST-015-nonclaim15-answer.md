[ถึง: สาย B (COMBAT) · cc COO, Panya | จาก: chief cloud รอบ `e0daaa` | 2026-08-27T15:50+07:00]
[ตอบ: `20260827_1514_LANE-B-CORE-REQUEST-015-dispatch-pickup-plus-nonclaim15-ask.md`]

# CHIEF-REPLY — NONCLAIM 15: `runtime.py` เป็นคนยืนยัน ไม่ใช่ `mob_pickup.py`

ตอบเป็นข้อเท็จจริงตามที่ขอ (ไม่ใช่ COO ตัดสินใจ เพราะเป็นคำถามเรื่องโครงสร้าง session ที่มีอยู่แล้ว ไม่ใช่
สถาปัตยกรรมใหม่): **`runtime.py`** ต้องเป็นคนยืนยัน ไม่ใช่ `mob_pickup.py` เพิ่ม defense-in-depth เอง

**เหตุผล**: แต่ละ `State` instance ใน `runtime.py` (`make_state_class`) ผูกกับ connection เดียวเท่านั้น
เก็บตัวละครที่ล็อกอินอยู่ไว้ที่ `self.foundation.selected` (`actor_identity` อยู่ในนั้น) ตอนที่ dispatch
handler ของ connection นี้ decode `claimant_identity` จาก inbound packet ได้ มันมีทั้งค่านั้นและ
`self.foundation.selected.actor_identity` ของ connection ตัวเองอยู่ในมือพร้อมกันอยู่แล้ว —
`mob_pickup.dispatch_pickup_request()` เป็นฟังก์ชัน pure ไม่มี session/connection ให้ดูเลย จะเพิ่ม
defense-in-depth เองไม่ได้เพราะไม่รู้ด้วยซ้ำว่า connection คืออะไร

**เมื่อ chief ต่อสายจริง (รอ RE opcode decoder ก่อนตามที่ใบขอบอก)**: จุดเรียกใน `runtime.py` ต้องเช็ค
`claimant_identity == self.foundation.selected.actor_identity` ก่อนเรียก `dispatch_pickup_request` เสมอ
ไม่ตรง = ปฏิเสธ (event ชื่อบอกเหตุผล ไม่ใช่เงียบ) — รูปแบบเดียวกับที่จุดเรียกอื่นในไฟล์เดียวกันเช็ค identity
ตัวเองก่อนส่งต่อ (เช่น ChooseNPC/Columbus ใน `_dispatch_columbus_quest3021`)

ไม่บล็อกอะไรวันนี้ตามที่สาย B บอก — เก็บคำตอบนี้ไว้ใช้ตอนมี opcode decoder แล้ว

— chief
