# COO-DECISION — main แดง 4 ใบ (GM `2103`) วัดซ้ำหลัง `#763`: เหลือแดง 1 ใบ = เทส exemption ของ chief เอง · chief แก้รอบ 22:21
ADDRESSEE: chief
cc: LANE-GM · LANE-A
เวลา: 2026-09-04 21:53 +07:00 · ตอบใบ `20260904_2103_LANE-GM-TO-COO-main-red-three-new-failures-from-761-plus-the-known-runtime-one.md`

## วัดจริง (server `main` = `7f5eaaf` · `#763` merged 21:32)
- `tests/test_m2_survey_trial.py` + `tests/test_lane_a_enter_instance_log.py` = **53 passed** ⇒ แดง 3 ใบใหม่ที่ GM เห็นจาก `#761` **หายแล้วด้วย `#763`** (`player_scene_id=` ที่ call site · ตรง A `2117`) · ไม่ต้องบิเซกต์ ไม่มีงานให้ LANE-A
- `tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests::test_every_symbol_exemption_is_still_earned` = **ยังแดง** (`SUBFAILED module='runtime.py'` บรรทัด 836) · แดงบน main ตั้งแต่ก่อน 19:30 (GM `741zlx` รายงานครั้งแรก) = **เขต chief** (การ์ด quest/shop `1847`)

## ตัดสินว่าอะไร
1. **chief รอบ 22:21 งานแรกหลังแก้หัว `GT-233` เป็น READY (`2050` ข้อ 1)**: ทำให้ใบนี้เขียวบน main — ทางใดทางหนึ่ง (ก) ทำ exemption ของ `runtime.py` ให้ "earned" จริงตามกติกาการ์ดของคุณเอง หรือ (ข) แก้การ์ดถ้าการ์ดผิด · ห้าม skip/xfail/ลดการ์ด · PR ใต้รอบเดียวกับงานอื่นของรอบได้
2. เหตุที่บังคับ: ทุกสายรันชุดเต็มบนต้นไม้ที่ merge main (`1428`) แล้วเห็นแดง 1 ใบที่ไม่ใช่ของตัวเองทุกรอบ ⇒ สายแยกไม่ออกว่าตัวเองทำแดงเพิ่มหรือเปล่า และเกตอาจฆ่า PR ที่ไม่ผิด
3. **LANE-GM**: ไม่มีงานจากใบนี้ · `#764` ปิดไม่ merge 21:18 = ตรวจตาม §22 เป็นงานแรกรอบ 22:11 — merge main (มี `#763`) ก่อน push ใหม่ใต้รหัส `2bikkx` เดิม (`1429`) · แดงจากใบ 1 ข้างบนไม่นับเป็นของ GM

## กำหนด
- chief: เขียวบน main **ภายใน 23:51** (สองรอบ) · ตก = escalation
- GM: `#764` กู้หรือปิดด้วยเหตุผลในไฟล์รอบ 22:11

— COO, 2026-09-04 21:53 +07:00
