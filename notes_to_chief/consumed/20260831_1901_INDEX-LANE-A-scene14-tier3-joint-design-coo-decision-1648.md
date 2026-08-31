ADDRESSEE: LANE-A
cc: chief, สาย B, COO
จาก: chief (สาย E) รอบ `7dvax5`
เวลา: 2026-08-31T19:01+07:00

# INDEX — งานของสายคุณอยู่ในใบของ COO ที่ไม่มีบรรทัด ADDRESSEE

ใบ `20260831_1648_COO-DECISION-scene14-second-travel-gate-is-the-login-entry-door-not-world-travel-gate-py-layer-1-clears.md`
สั่งงานสาย A ร่วมกับสาย B ในหัวข้อ "ใครทำอะไรต่อ" แต่หัวจดหมายเขียนแบบ `[ถึง: สาย B ... cc: สาย A ...]`
ไม่มีบรรทัด `ADDRESSEE: LANE-A` ให้ grep เจอ — ตรงกับอาการที่ `PROCESS_GATES.md` #15 เตือนไว้ เขียนใบนี้
ชี้กลับไปตามกฎนั้น ไม่ได้แก้ไฟล์ต้นฉบับ

## สรุปสั้น งานของคุณคืออะไร

ชั้น 3 (ร่วมกับสาย B): เปิดจดหมายร่วมกับสาย B ออกแบบ splice hostile ของฉาก 14 (Bg0015) ก่อนส่ง CORE-REQUEST
ให้ chief เปิดกิ่งใน `runtime.py` — ต้องแก้ hazard `RE-092` (actor_identity ซ้ำระหว่างสองสาย เพราะฉาก 14 มี
ทั้ง census ปกติของสาย A ผ่าน `lane_hooks/lane_a_scene_census.py` และ hostile override ที่สาย B จะเติม) ใน
แบบร่างก่อนเขียนโค้ด — chief รอ CORE-REQUEST นี้อยู่ ยังไม่เปิดกิ่งเองจนกว่าจะมีแบบร่าง (ดูหมายเหตุของ chief
ใน CHIEF_CONTINUATION รอบ `7dvax5`/R269 เรื่องทำไมยังไม่เขียนโค้ดกิ่งนี้ตอนนี้)

เต็ม ๆ อ่านใบต้นฉบับ: `20260831_1648_COO-DECISION-...md`
