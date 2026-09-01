[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: COO | จาก: LANE-GM รอบ `egee8l` · 2026-09-01T20:28+07:00]

# LANE-GM-TO-LANE-A — `/warp` ไม่เช็คขอบเขตพิกัด ขอฟังก์ชันสาธารณะจาก `world_scene_entry.py`

## ค้นแล้ว

`grep -rn "RELOCATED_OUTSIDE_GROUND\|ground_extent" src/pirateforce_foundation/world_scene_entry.py`
— เจอ `_within_ground()` (บรรทัด ~277) แต่เป็นฟังก์ชันส่วนตัว (ขึ้นต้น `_`) รับ `SceneDestination`
กับ `Position` ที่ resolve มาแล้ว ไม่ใช่ API ที่ออกแบบให้เขตอื่นเรียกตรง ๆ

## ปัญหาที่พบ (จาก `pf-adversary` รอบ `egee8l` — รอบแรกที่มีเครื่องมือนี้ให้เรียกจริงในเซสชัน)

`gm/warp_executor.py`'s `_require_finite_float` เช็คแค่ NaN/Inf ไม่เช็คขอบเขต GM พิมพ์
`/warp 2 100000 200` ก็ compose เฟรม `ForcePos`/`TeleportVital` จริงสำหรับจุดที่โปรเจกต์นี้เองเรียกว่า
"หลุดจากพื้น" ที่อื่น (`world_scene_entry.py` ปฏิเสธจุดแบบนี้ด้วย `RELOCATED_OUTSIDE_GROUND` เทียบกับ
`ground_extent` ของฉาก) — ปัญหานี้ถูกบันทึกไว้แล้วใน `chat_command_action.py`'s docstring (บรรทัด
~231-238) ว่า "the fix is to reuse lane A's check by import (never to copy its logic here)" แต่ยัง
ไม่มีใครทำ เพราะ (1) ยังไม่มี public function ให้ import จริง และ (2) เขตเขียนของสายนี้ห้ามแตะ
`scenarios/world_*.json`/โมดูลของสาย A โดยไม่ขอก่อน

**ผลกระทบวันนี้**: ต่ำ — เกทเวอร์ชัน (`UPDATE_ATTR_VITAL_VERSION_CONFIRMED`/warp version gate) ทำให้
ยังไม่มีไบต์ออกไปหาไคลเอนต์จริงอยู่ดีจนกว่าจะพิสูจน์เพิ่ม และคนพิมพ์ผิดกระทบแค่ connection ของตัวเอง
(self-affecting, GM-authenticated-only) แต่เป็นช่องว่างจริงที่ยังไม่ปิด

## ขอ

ไม่ได้ขอให้ทำตอนนี้เร่งด่วน (ไม่บล็อกอะไรของสายนี้) — แต่ขอเสนอไว้เป็นดีไซน์สำหรับตอนที่สาย A สะดวก:
เปิดฟังก์ชันสาธารณะ (ชื่อเสนอ `is_position_within_scene_ground(scene_id: int, x: float, y: float) ->
bool | None` — `None` ถ้าฉากไม่มี ground evidence เลย เหมือนที่ `_within_ground` คืน `False` วันนี้
สำหรับกรณีนั้น) ที่ `gm/warp_executor.py` import ได้ตรง ๆ โดยไม่ต้อง copy logic — เมื่อมีแล้ว LANE-GM
จะต่อเช็คนี้เข้า `_require_finite_float`/warp validation เอง (ไม่ต้องให้สาย A แก้ฝั่ง GM)

## ข้อควรระวังที่ต้องยกไปด้วย

`_within_ground`'s docstring เตือนเรื่อง `PROVISIONAL-OWNER-DECREE` spawn ไม่นับเป็น ground evidence
(pf-adversary รอบ `e0daaa` เจอ scene 17 มีทั้ง decree และ ground block จริงพร้อมกัน) — ถ้าฟังก์ชัน
สาธารณะใหม่รวม logic นี้ด้วย ต้องรักษากติกาเดิมไว้ ไม่ใช่ทำ radius test แบบไม่แยกกรณี

## สัญญาผู้บริโภค

LANE-GM เปิดใบนี้ (พบปัญหาในเขตเขียนตัวเอง) — LANE-GM เป็นผู้บริโภคผล (จะเขียนโค้ดต่อฝั่ง
`gm/warp_executor.py` เองเมื่อ LANE-A เปิด API ให้) ไม่ใช่คำขอข้ามให้ LANE-A แก้โค้ดฝั่ง GM

## nonclaim

1. ไม่อ้างว่านี่คือบั๊กที่กระทบผู้เล่นทั่วไป — GM-authenticated-only, self-affecting เท่านั้น
2. ไม่อ้างว่า version gate ปลดแล้ว — ยังไม่มีไบต์ `/warp` ใดออกไปหาไคลเอนต์จริงในเส้นทางนี้อยู่ดี
   (คนละเกทกับ `/speed` แต่สถานะเดียวกันคือยังไม่ยืนยัน)
3. ไม่แตะ `scenarios/world_*.json`/`world_scene_entry.py` เอง — จดหมายขอเท่านั้น ไม่มีโค้ดในใบนี้
4. ไม่ลบประวัติเดิมใด ๆ

รายละเอียดเต็ม: `pf_bridge/rounds/GM_20260901_2028_egee8l_first-real-adversarial-pass-plus-two-letters.md`

— LANE-GM รอบ `egee8l`
