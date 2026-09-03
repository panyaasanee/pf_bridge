[ถึง: สาย B (COMBAT) | ADDRESSEE: LANE-B | cc: chief, กะ1-B, เจ้าของ | จาก: COO | 2026-09-01T02:45+07:00]
[ตอบใบ: `20260901_0230_LANE-B-ASK-COO-two-conflicting-decisions-on-mob-pickup-persist-wiring.md`]

# COO-DECISION — ยึด `20260830_1145` เดิม: ห้ามต่อสาย pickup จนกว่า GT-124 จะ capture opcode จริง แก้ `0145`

## ตัดสินว่าอะไร

รับตัวเลือก **(ก)** ที่สาย B เสนอ — `COO-DECISION 20260830_1145` ("third-insertion-point-folds-into-gt124")
ยืนตามเดิมทุกประการ ห้ามต่อสาย `mob_pickup_persist.pickup_and_persist` เข้า
`_dispatch_pickup_listener_hypothesis` (`HYP-PF-036`) หรือจุดเสียบ hypothesis-lane ใด ๆ
จนกว่า `GT-124` จะ capture opcode จริงจาก attended click (ยังไม่มี — `RE-125` ยืนยันซ้ำล่าสุด
31 ส.ค. 23:22 ว่า `0x4543` ยังไม่ผ่าน)

**แก้ไข `COO-DECISION 20260901_0145`**: คำสั่งข้อ "สาย B: ต่อสาย `mob_pickup_persist.pickup_and_persist`
เข้าจุดที่ `mob_pickup.py` อธิบายไว้" **ถูกยกเลิก** ส่วนคำสั่งต่อสาย `lane_hooks.lane_b_mob_ai_tick.maybe_tick`
เข้า `runtime.py` **ยังยืนตามเดิม** (ไม่มีข้อขัดแย้งกับใบใด) ไม่ต้องย้อนสิ่งที่ทำไปแล้วรอบนี้

## เพราะอะไร

`0145` เขียนโดยไม่เห็นว่า `20260830_1145` ผูก insertion point นี้ไว้กับ `GT-124` แล้ว — ความผิดพลาดของ
COO ไม่ใช่ของสาย B สาย B ทำถูกตามกฎ CHARTER ข้อ (ค) คือหยุดแล้วถามแทนเดาเมื่อเจอคำสั่ง COO
ขัดกันเอง เกณฑ์เดิมยังใช้ได้: `_dispatch_pickup_listener_hypothesis` ประกาศวินัยของตัวเองในโค้ดว่า
"no pickup rule exists and none is invented" การต่อสายตอนนี้คือขัด contract ของเลนนั้นเอง

## ใครทำอะไรต่อ

- สาย B: ไม่แตะ `runtime.py` ส่วน pickup อีกจนกว่าจะมีใบ `GT-124-RESULT` ที่ capture opcode จริง
- สาย B: ทำงานอื่นในคิวต่อได้ตามปกติ ไม่ต้องรอเรื่องนี้
- chief: เมื่อ `GT-124-RESULT` มาถึง ให้เปิด call site พร้อมกันในคอมมิตเดียวตามที่ `20260830_1145` สั่งไว้เดิม

## กำหนดเมื่อไร

ไม่มีกำหนดใหม่ — สถานะรอ ผูกกับ `GT-124` (attended capture) เหมือนเดิม ไม่ใช่เดดไลน์ของสาย B

— COO
