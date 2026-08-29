[ถึง: สาย B (COMBAT) · chief · cc Panya | จาก: COO | 2026-08-27T13:50+07:00]
[ตอบ: `20260827_1500_LANE-B-ASK-COO-widen-death-scope-to-real-mob-roster.md`]

# COO-DECISION — ขั้นสองอนุมัติ: widen mob_death.kill() ครอบคลุมมอนจริง 13 ตัวจากตาราง MOBS ใน bg0001

**ตัดสินว่าอะไร**: อนุมัติขั้นสอง เปิดทางให้ `kill()` รับเป้าหมายมอนจริงจากตาราง MOBS ใน `bg0001` (13 ตัว) ไม่ใช่แค่ `0x201F`

**เพราะอะไร**: เงื่อนไข "รอ roster จริงจากสาย A" ที่ตั้งไว้ในคำตัดสิน 0954/0955 ปิดแล้ว (evidence 1020: MOBS 1-35 = Prison-Exile roster, Port Royal 35 placements แรกยืนยันแล้ว) stage 1 บน `0x201F` นิ่งมาหลายรอบ ไม่มี fail ใหม่ (3444 เทสเขียว) และ `kill()` มีเทสยืนยันกับ roster จริงแล้วไม่ใช่ identity สมมติ การเปลี่ยนแปลงคือ string เดียวที่ `runtime.py:3925` ย้อนกลับได้ทันที ไม่ขัดกับ PANYA-RULINGS-FOUR ข้อ 3 (สองขั้นตอนแยกรอบกันจริง)

**ใครทำอะไรต่อ**: chief แก้ `runtime.py:3925` เป็น `mob_death.kill(legacy, mob, step.outcome, self.mob_death_register, widened="COO-RULING-20260827-1350 widen-death-scope-bg0001")` ไม่ต้องแตะไฟล์ของสาย B

**กำหนดเมื่อไร**: รอบถัดไปของ chief ที่ถือ LOCK ไม่บล็อก M4 (29 ส.ค. 23:59)
