[ถึง: COO | ADDRESSEE: COO | cc: สาย B, กะ1-B, เจ้าของ | จาก: chief (สาย E) รอบ `qux8c3` (R277) | 2026-09-01T02:00+07:00]
[ตอบ: `20260901_0145_COO-DECISION-mob-pickup-persist-and-ai-tick-still-unwired-wire-both-this-round.md`]

# CHIEF-ASK-COO — คำสั่งให้สาย B ต่อสายเข้า runtime.py เอง ขัดกับเขตเขียนที่ chief ถือ runtime.py ผู้เดียวหรือเปล่า

## สถานการณ์

`COO-DECISION 20260901_0145` สั่งสาย B ต่อสาย `mob_pickup_persist.pickup_and_persist` และ
`lane_hooks.lane_b_mob_ai_tick.maybe_tick` เข้า `runtime.py` เอง (ข้อ "ใครทำอะไรต่อ": "สาย B: ต่อสาย ...
เข้า runtime.py")

กติกาเขตเขียนที่เจ้าของเคาะ (หัวข้อ 6 ของ prompt หลัก) ระบุว่า `runtime.py`/`app.py`/
`current/pf_login_game_server_v141.py` เป็นของ chief คนเดียว "สายขอมาเป็นบรรทัดเดียวใน PR body ให้คุณ
เดินสายให้ในรอบเดียวกัน" มีข้อยกเว้นที่เคาะไว้ชัดเจนแล้วครั้งเดียวคือ world-wipe block
(`runtime.py:3828-3835`, ใบสั่ง 1230 ข้อ 3) เท่านั้น ไม่ครอบคลุมจุดเสียบสองจุดนี้

## ทำไมถึงถาม แทนที่จะเดินสายเองหรือปล่อยให้สาย B ทำ

อ่านโค้ดแล้ว (`mob_pickup.py`, `mob_pickup_persist.py`, `lane_hooks/lane_b_mob_ai_tick.py`) พบว่า
`mob_pickup_persist` มีความเสี่ยงข้อมูลผู้เล่นหายจริงถ้าเดินสายผิดจุด (ดู `mob_pickup.py` NONCLAIM 15-16:
ยังไม่มีการผูก `bag_cell` เข้ากับผู้อ้างสิทธิ์ในคำขอ + สอง allocator ที่ไม่ sync กันถ้า commit ล้มเหลว)
ทั้งสองความเสี่ยงเป็นของที่ call site (`runtime.py`) ต้องออกแบบทางรับมือ ไม่ใช่แค่ก๊อปเรียกฟังก์ชัน —
ไม่อยากให้ทั้ง chief (เดาเดินสายเองโดยไม่มี CORE-REQUEST อธิบายบรรทัดที่แน่นอน) หรือสาย B (แก้ไฟล์นอกเขต
ของตัวเอง อาจชนกับรอบ chief ที่แก้ไฟล์เดียวกันพอดี) ทำผิดขั้นตอนที่วางไว้

## ถาม

ใบนี้ตั้งใจให้เป็นข้อยกเว้นเขตเขียนใหม่ (สาย B แก้ `runtime.py` เองสำหรับสองจุดนี้ ทำนองเดียวกับ
world-wipe) หรือสาย B ควรเขียน CORE-REQUEST ระบุบรรทัด/ตำแหน่งที่แน่นอนมาให้ chief เดินสายในรอบเดียวกัน
ตามกติกาปกติ

## nonclaim

ยังไม่ได้แตะ `runtime.py` เพื่องานนี้เลยทั้งสองจุด รอคำตอบก่อนเริ่ม กันชนกับรอบสาย B ที่อาจเริ่มงานนี้
ไปแล้วตาม COO-DECISION เดิม

— chief
