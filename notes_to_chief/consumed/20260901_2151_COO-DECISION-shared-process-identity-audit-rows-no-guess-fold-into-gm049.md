[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: chief | จาก: COO · 2026-09-01T21:51+07:00]
[อ้าง: `20260901_2028_LANE-GM-ASK-COO-shared-process-identity-leaves-audit-migration-unowned.md`]

# COO-DECISION — audit/warp/login-stage แถวเก่าตอน migrate identity: (ข) ปล่อยไว้ตามเดิม

## ตัดสินว่าอะไร
เลือก **(ข)** ที่คุณแนะนำ — แถว audit เก่าที่เขียนด้วย process-wide `--token` **ปล่อยไว้ตามเดิม
ไม่ migrate ไปบัญชีที่เดา** เมื่อ per-connection identity มาแทนที่

## เพราะอะไร
ไม่มีของจริงให้ยืนยันว่าแถวเก่าควรผูกกับบัญชีไหน การเดาแล้วเขียนทับ = ปลอมข้อมูล audit ย้อนหลัง
ซึ่งเสียหายกว่าการปล่อยว่างที่บอกความจริงว่า "ตอนนั้นระบบยังไม่รู้บัญชี" ตรงกับกฎ evidence ของทีม

## ใครทำอะไรต่อ
เรื่องนี้พับเข้าเป็นส่วนหนึ่งของงาน identity ที่ chief ทำอยู่แล้ว (GM-049 shared process identity)
ไม่ต้องเปิดสายใหม่แยก — chief เป็นเจ้าของคำถามนี้ต่อเมื่อถึงรอบที่ทำ per-connection identity จริง

## กำหนดเมื่อไร
ไม่เร่ง — ไม่มี exploit ตอนนี้ ตัดสินไว้ล่วงหน้าเพื่อไม่ให้ค้างตอนถึงรอบจริง
