[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: chief, เจ้าของ | จาก: COO · 2026-09-01T21:48+07:00]
[อ้าง: `CODEX_URGENT_20260901_2040_P05-CORPSE-DROP-STATE-SCOPE.md`]

# COO-DECISION — สองบั๊กที่ Codex ยืนยันแล้ว ให้ LANE-B แก้แบบ bounded รอบหน้า

## ตัดสินว่าอะไร
อนุมัติทั้งสองข้อเสนอ bounded ของ Codex ให้ **LANE-B** ลงมือ (โค้ดอยู่ในเขต mob_death.py /
mob_scene_recompose.py / mob_loot.py / mob_drop_presence.py ซึ่งเป็นคอมแบต):
1. ทำ corpse timer เป็น per-identity/per-record — ศพเก่าต้องไม่ถูก re-arm เป็น positive timer
   ตอนมีศพใหม่ตายในเซนซัสเดียวกัน
2. ผูก drop ownership กับ scene/generation — drop ฉาก A ต้องไม่หลุดไปประกอบ publication ของฉาก B

ข้อ 3 (pickup/removal ของชิ้นสุดท้าย) **ยังเปิดไว้ตามเดิม** — ห้ามใช้ resend หรือ guessed
count-zero clear ตามที่ Codex ระบุ ไม่อยู่ในสโคปรอบนี้

## เพราะอะไร
Codex ยืนยันสองข้อนี้เป็น self-contradiction ของโค้ดปัจจุบันเอง (ไม่ใช่แค่สมมติฐานเรื่อง original
server) มีขอบเขตชัด มีข้อเสนอ regression test มาให้แล้ว และเกี่ยวตรงกับ **P-1** (ของดรอปต้องค้างพอ
ให้เห็นและเก็บได้) ใน NOW.md — ยิ่งปล่อยไว้ยิ่งกวนผลเทส P-1/P-2 ที่จะตามมา

## ใครทำอะไรต่อ
LANE-B: แก้สองข้อ + เพิ่ม regression ตามที่ Codex เสนอ (A ตาย→B ตาย→เช็ค A ไม่กลับ positive timer;
scene A มี drop→ไป B→kill B→publication B ต้องไม่มี key/position จาก A) ไม่ต้องรอ P-1/P-2 ปิดก่อน
เพราะนี่คือการแก้บั๊กใต้ฝากระโปรง ไม่ใช่ GT-146/ใบเทสตีมอนที่ NOW.md ห้ามไว้

## กำหนดเมื่อไร
รอบถัดไปของ LANE-B ที่มีที่ว่างหลังงานด่วน NOW.md ปัจจุบัน (P-1/P-2/P-3 ไม่ผูกกับเรื่องนี้)
