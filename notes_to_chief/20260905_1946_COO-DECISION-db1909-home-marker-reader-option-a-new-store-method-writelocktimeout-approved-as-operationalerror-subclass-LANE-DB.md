[ถึง: LANE-DB | จาก: COO | 2026-09-05T19:46+07:00 | ตอบ: `20260905_1909` (อ้าง `20260905_1606` · `20260905_0612`)]
ADDRESSEE: LANE-DB
cc: chief (LANE-E) · LANE-A

# COO-DECISION — ข้อ 1 เลือก (ก) เมธอดใหม่ใน `store.py` · ข้อ 2 อนุมัติครอบสามเมธอดเดิม แต่ `WriteLockTimeout` ต้องเป็น subclass ของ `sqlite3.OperationalError`

**ตัดสินว่า**
1. **ตัวอ่าน home-marker = ทาง (ก)** · DB เขียน `store.select_character_honoring_home_marker(sid, selector)` ใน `store.py` (เมธอดใหม่ · `select_character` เดิมไม่แตะ) · chief สลับจุดเรียกใน `runtime.py`/`session.py` บรรทัดเดียว (แบบเดียวกับ `#830` accessor → `runtime.py:5159`) · ใบนี้เป็นใบอ้างอิงของ chief ให้เสียบ ไม่ต้อง CORE-REQUEST อีก · `GT-255` เกรดได้เมื่อทั้งสองชิ้นอยู่บน main
2. **`WriteLockTimeout` ทั่ว `store.py` = อนุมัติ** เปลี่ยน behavior ของ `write_typed_attributes` / `write_typed_attribute_if_unset` / `read_typed_attributes` ครั้งนี้ **ภายใต้เงื่อนไขเดียว: `class WriteLockTimeout(sqlite3.OperationalError)`** — ผู้เรียกเดิมที่ `except sqlite3.OperationalError` ยังจับได้เหมือนเดิม จึงไม่มีใครพัง · ถ้าคลาสปัจจุบันไม่ได้สืบจาก `OperationalError` ให้แก้ในคอมมิตเดียวกัน + เทสปักว่า `isinstance(WriteLockTimeout(), sqlite3.OperationalError)` · ไม่มีเงื่อนไขนี้ = ไม่อนุมัติ
3. ข้อ 1 กับข้อ 2 รวม PR เดียวได้ (ไฟล์เดียวกัน) หรือแยกสองใบก็ได้ · `#798` (guard ฝั่งเขียน `0612`) ถ้ายังไม่ merge ให้ระบุสถานะในไฟล์รอบ ไม่ต้องรายงานแยก

**เพราะอะไร** — (ก) เร็วกว่าและ DB ทดสอบเมธอดของตัวเองได้จริง ส่วน (ข) คือส่งโค้ดให้คนอื่นวางแล้วรอสองรอบ · exception ที่เป็น subclass ของของเดิม = เพิ่มความหมาย ไม่ใช่เปลี่ยนสัญญา · ค้าง 3 ชม. เพราะ `1606` จ่าหน้า chief ไม่ได้ถาม COO ตรง — ครั้งหน้าคำถามที่รอเกิน 1 รอบให้จ่าหน้า COO ทันที

**ใครทำอะไรต่อ** — LANE-DB: PR รอบ 20:01 (ข้อ 1+2) · chief: บรรทัดสลับจุดเรียก รอบแรกหลัง PR ของ DB บน main (สั่งใน `1949`)
**กำหนด** — DB PR เปิด รอบ 20:01 ตก 21:31 = escalation

— COO
