ADDRESSEE: chief
FROM: LANE-B
TIME: 2026-09-01T14:36+07:00
ROUND: fbql13

## สรุปสั้น

P-1/P-2/P-3 ไม่มีพื้นผิวใหม่ให้สาย B รอบนี้ (เหมือนรอบ `ruigb0` ก่อนหน้า) และ `GT-146`/ใบเทสตีมอน
ทุกใบยังล็อกตาม NOW.md เข้ากฎ F ข้อ ง (technical debt): แก้ docstring ค้างของ `bar_frames()` ใน
`pirate-force-server/src/pirateforce_foundation/mob_combat.py` -- ยังชี้ว่า `runtime.py` เรียก
`mob_death.hostile_census_frames` ตรง ๆ ทั้งที่เปลี่ยนไปเรียก `mob_scene_recompose.recompose_frames`
ตั้งแต่รอบ `y9s0xo` (29 ส.ค.) แล้ว

ต่อท้ายด้วย `[UPDATE, round fbql13]` (ไม่ลบของเดิม) -- เรียก pf-adversary จริงได้รอบนี้ (มี subagent
ให้เรียก) จับได้ว่าร่างแรกอ้างผิดสองจุด (ตำแหน่งคอมเมนต์ผิดไฟล์ + สรุปเกินจริงว่า
`mob_death.hostile_census_frames` เป็นแค่ประวัติศาสตร์ ทั้งที่ `diag_multi_object_wiring.
hostile_census_frames` ส่งต่อไปเรียกมันตรง ๆ ทุกครั้งที่ไม่มี diagnostic object ทำงาน ซึ่งเป็นค่า
default ของทุกแอคเคาต์) แก้ทั้งสองจุดแล้วยืนยันด้วยการอ่านโค้ดเอง (`runtime.py:1206`,
`diag_multi_object_wiring.py:606-610`) ก่อน push

docstring-only ไม่มี behavior/wire change ใหม่ เทสผ่านครบ (119 passed, 24 subtests, 0 failed)

รายละเอียดเต็มอยู่ใน `pirate-force-server/rounds/B_20260901_1436_fbql13_mob-combat-bar-frames-caller-doc-drift.md`

## ไม่ได้ทำ

- ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`/canonical DB
- ไม่เปิด/เดิน `GT-146` หรือใบเทสตีมอนใด ๆ (ล็อกตาม NOW.md)
- ไม่แตะ P-2 (สีชื่อ) หรือ P-3 (ปุ่ม GM) -- ไม่ใช่ของสายนี้

PF-AUTOMERGE: v4
