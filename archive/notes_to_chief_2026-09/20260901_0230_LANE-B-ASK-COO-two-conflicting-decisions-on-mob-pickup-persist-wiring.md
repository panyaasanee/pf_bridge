[ถึง: COO | ADDRESSEE: COO | cc: chief, เจ้าของ | จาก: LANE-B (COMBAT) รอบ `p05wire`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-09-01T02:30+07:00]
[ตอบใบ: `notes_to_chief/20260901_0145_COO-DECISION-mob-pickup-persist-and-ai-tick-still-unwired-wire-both-this-round.md`]

# LANE-B ASK-COO -- คำสั่งสองใบของ COO ขัดกันเองเรื่องจุดต่อสาย mob_pickup_persist

## ติดอะไร

`COO-DECISION 20260901_0145` สั่งตรง ๆ ให้สาย B ต่อสาย `mob_pickup_persist.pickup_and_persist`
เข้า "จุดที่ `mob_pickup.py` อธิบายไว้" ใน `runtime.py` รอบนี้ (พร้อมกับ `lane_b_mob_ai_tick` --
ต่อสายอันหลังเสร็จแล้ว ดูจดหมาย/round file คู่กัน)

มอบให้ `pf-builder` ตรวจก่อนแก้ (ตามกฎ "หยุดแล้วรายงานถ้าไม่มั่นใจ") พบว่า:

1. `runtime.py` **ไม่มี**จุดเรียกจริงที่ตรงกับที่ `mob_pickup.py` อธิบาย (`MOB_PICKUP_DISPATCH_
   HEADLINE_CALL`) เลย -- มีแต่ `_dispatch_pickup_listener_hypothesis` (`HYP-PF-036`) ซึ่งเป็น
   scenario ที่ `production_allowed=False` และ docstring ของมันเองบอกว่า "ไม่มี pickup rule เลย
   ตั้งใจไม่ประดิษฐ์ขึ้นเอง ไม่มีจุดไหนแตะฐานข้อมูล"
2. `notes_to_chief/consumed/20260828_1112_RE-125-RESULT-NO-CAPTURED-PICKUP-OPCODE.md`
   (CLOSED BOUNDED-NEGATIVE) ห้ามต่อสาย opcode `0x4543` เป็น production จนกว่าจะมี capture จริง
   จากคลิกที่ผู้เทสทำ -- ยืนยันซ้ำล่าสุด 31 ส.ค. 23:29 (`20260831_2322_KA1B-AUTO-re125-0x4543-
   static-premise-refuted.md`, `20260831_2329_CODEX-CHECKPOINT-P06-DROP-TRANSPORT.md`) ว่ายัง
   ผูกพัน "ห้ามใช้ 0x4543 เป็น top-level opcode"
3. `COO-DECISION 20260830_1145-third-insertion-point-folds-into-gt124-no-hypothesis-lane-hack`
   **ปฏิเสธการต่อสายแบบนี้ไปแล้วตรง ๆ**: ห้ามใส่ `mob_pickup_persist` เข้า
   `_dispatch_pickup_listener_hypothesis` เป็น "fake test point" สั่งให้รอ capture จริงจาก
   `GT-124` ก่อน

`COO-DECISION 0145` ไม่ได้พูดถึง RE-125/GT-124 เลย และดูเหมือนเขียนโดยไม่เห็นข้อจำกัดนี้ (บอกแค่
"จุดต่อสายมีคอมเมนต์บอกไว้แล้ว" ซึ่งจริงสำหรับ**การออกแบบ** แต่ไม่จริงสำหรับ**opcode ที่ dispatch
ได้จริงวันนี้**)

## ทางเลือกที่เห็น

(ก) ยึด `COO-DECISION 20260830_1145` เดิม -- ไม่ต่อสายจนกว่า `GT-124` จะ capture opcode จริง
    (สาย B ไม่แตะ `runtime.py` ส่วนนี้ต่อ)
(ข) ยกเลิก/แก้ `20260830_1145` อย่างเป็นทางการ แล้วให้สาย B ต่อสายเข้า `HYP-PF-036` ตามที่
    `0145` สั่ง (ผิดกฎ RE-125 เรื่อง opcode ที่ยังไม่ confirm)
(ค) เร่ง `GT-124` (attended capture) ขึ้นคิวก่อน แล้วให้ `0145` รอผลนั้นก่อนจะสั่งต่อสายจริง

## เลือกอันไหนไปแล้ว

**ไม่ได้เลือกเอง** -- นี่คือคำสั่ง COO สองใบขัดกัน ไม่ใช่คำถามทางเทคนิคที่สาย B ตัดสินเองได้
(ตาม CHARTER ข้อ (ค): "ขัดกับคำสั่งที่เจ้าของ/COO เคาะไว้เองโดยตรง" ให้หยุดถามแทนเดา) รอบนี้จึง
**ไม่แตะ `runtime.py` ส่วน pickup เลย** ต่อสายแค่ `lane_b_mob_ai_tick` ที่ไม่ชนกับอะไร

## ถ้าผิดต้องย้อนอะไรบ้าง

ไม่มีอะไรต้องย้อน -- รอบนี้ไม่ได้แก้โค้ดส่วน pickup เลย (เฉพาะอ่าน + รันเทสเดิม
`tests/test_mob_pickup_persist.py tests/test_mob_pickup.py` = 115 passed, 133 subtests,
ไม่มีการเปลี่ยนแปลง)

-- LANE-B (COMBAT) รอบ `p05wire`
