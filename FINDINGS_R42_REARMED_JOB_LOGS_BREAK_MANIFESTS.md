# FINDINGS R42 — job ที่ re-arm เขียนทับ log ใน outbox ที่ manifest เก่า pin ไว้ → seam test แดงเงียบ ๆ

วันที่: 2026-08-18 (chief scheduled รอบ 52) · สถานะ: แก้เฉพาะหน้าแล้ว + วางกติกาถาวร

## อาการ

manifest ของ `PF_GT001_POST_HYP012_..._20260817` (เขียนหลังรอบ 19:2x) pin
`pf_bridge\outbox\072_gt001_boot.*` + `073_gt001_teardown.*` — คืนนี้ GT-001
re-run (02:07) ด้วย staged jobs ชื่อเดิม → ไฟล์ทั้ง 4 ถูกเขียนทับ →
seam test (re-hash ทุกบรรทัด manifest) **แดงบน tree ปัจจุบันตั้งแต่ 02:07
โดยไม่มีใครเห็น** เพราะ gate 096 รันไปก่อน (01:25) และยังไม่มี gate ใหม่

## Root cause

staged jobs ที่ออกแบบให้ใช้ซ้ำ (072/073/087/088/090/091/097/098) เขียน log
ชื่อตายตัวใน outbox — ของดีสำหรับ workflow ผู้เทส แต่ขัดกับ manifest ที่
ต้องการ immutability ตลอดกาล

## การแก้

1. **เฉพาะหน้า**: ถอด 4 บรรทัด stale ออกจาก manifest เก่า (หลักฐานแท้ =
   capture dir timestamped ยังอยู่ครบ) + จด addendum ใน report เก่า ·
   สำเนา log คืนนี้ทั้ง 14 ไฟล์ snapshot ไว้ที่
   `pf_bridge/archive/biground2_outbox_20260818/` แล้ว manifest ใหม่
   (BIGROUND2) pin ที่สำเนานั้นแทน
2. **กติกาถาวร (ทุกคนที่เขียน manifest)**: ห้าม pin path ใน `outbox/` ของ
   job ที่ re-arm ได้ — pin ได้เฉพาะ (a) ไฟล์ timestamped ที่ไม่ถูกใช้ซ้ำ
   (เช่น `073_console_tail_<stamp>.txt`, capture dirs) หรือ (b) สำเนาใน
   `pf_bridge/archive/` · ทางเลือกอนาคตถ้าผู้เทสสะดวก: ให้ teardown .ps1
   ใส่ stamp ในชื่อ log หลักด้วย — แล้วปัญหานี้หายทั้ง class
