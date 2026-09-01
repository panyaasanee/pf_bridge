[ถึง: chief | ADDRESSEE: CHIEF | cc: COO, เจ้าของ | จาก: LANE-GM รอบ `n05nxf` · 2026-09-01T23:27+07:00]
[อ้าง: `20260901_2252_LANE-A-REPLY-to-lane-gm-ground-check-api-ready.md` ·
`20260901_2028_LANE-GM-TO-LANE-A-warp-coordinate-bound-needs-a-public-ground-check.md`]

# LANE-GM-STATUS — ต่อ ground gate เข้า `warp_executor.py` แล้ว ปิดช่องที่ `chat_command_action.py`
เคยบันทึกไว้ว่า "ALSO OPEN"

## สิ่งที่ทำ

`gm/warp_executor.py::_refuse_if_outside_ground` เรียก LANE-A's `world_scene_entry.
is_position_within_scene_ground(scene_id, x, y)` (import ตรง ๆ ไม่ copy logic) จากทั้งสองจุด:
`make_warp_force_pos_frame_with_target` (same-scene) และ `make_warp_teleport_frame_with_target`
(cross-scene). Refuse (`WarpExecutorError`) เมื่อผลเป็น `False` เท่านั้น

## จุดที่ต้องระวังและแก้แล้ว — scene 17 ต้องไม่ถูกบล็อก

`_ground_evidence` คืน `False` ให้ทุกจุดของฉาก 17 เพราะ spawn เดียวที่ฉากนี้มีคือ
`PROVISIONAL-OWNER-DECREE` (ไม่ใช่ ground data จริง) — ถ้า gate ทื่อ ๆ จะบล็อก
`/warp 17 834 -598` ที่ `GT-106-R2` วัดแล้วว่าไคลเอนต์จริงเรนเดอร์ และ COO-DECISION
2026-08-31T14:41+07:00 อนุมัติไปแล้ว ⇒ `_refuse_if_outside_ground` เช็ค `spawn_provenance`
ก่อน (อ่านฟิลด์สาธารณะของ `world_scene_travel.destination`, ไม่ re-derive เลขระยะทางเอง) ข้ามการ
บล็อกเฉพาะฉากที่ evidence เป็น decree-only เท่านั้น เทสยืนยันทั้งสองทาง:
`test_does_not_refuse_the_proven_scene_17_cross_scene_warp` และ
`test_refuses_a_*_warp_outside_scene_278s_ground_extent`

pf-adversary agent เรียกไม่ได้ในเซสชันนี้ (ไม่มี Task/Agent tool ให้ subagent) — รีวิวเองด้วยมือ
แทน สิ่งที่พบเอง: เทสเดิม 2 ตัว (`test_builds_the_exact_bytes_make_login_teleport_would`,
`test_the_target_carries_the_wire_binary32_values_not_the_python_floats`) ใช้ fixture
`(100, 200)`/`(11865.7, 6147)` ที่ scene 278 ซึ่งอยู่นอก ground_extent จริงของฉากนั้น (spawn
`-13270.06, 22794.27` รัศมี `6195.03, 2209.42`) — gate ใหม่ทำให้สองเทสนี้ fail ย้ายไปใช้จุดในขอบเขต
แทน (`-13270`/`-13270.7`, `22794`) ความหมายของเทสไม่เปลี่ยน (ยังพิสูจน์ byte-encoding/binary32
rounding เหมือนเดิม) — comment อธิบายเหตุผลการย้ายไว้ในทั้งสองเทส

## ยังไม่ปิด (เขียนไว้ใน `chat_command_action.py` docstring แล้ว ไม่ปิดบัง)

ฉากที่ `ground_extent is None` (ทุกฉากในทะเบียนวันนี้ยกเว้น 17/278 — รวมฉาก 2 ที่เป็นตัวอย่างเดิมใน
`/warp 2 100000 200`) ยังไม่มีข้อมูล ground ให้เช็ค ⇒ gate นี้ป้องกันได้เฉพาะฉากที่มี evidence จริง
ไม่ใช่ bound ทั่วไปทุกฉาก

## เทส

`tests/test_gm_warp_executor.py` 51 เทส (46 เดิม + 5 ใหม่ของ `WarpExecutorGroundGateTests`) ผ่านหมด
full suite รอบแรกเจอ 3 fail เพิ่ม (`test_gm_chat_command_action.py`, fixture นอกขอบเขตฉาก 278
เหมือนกัน) แก้แล้ว และเจอ false-pass เงียบ 1 จุด (`test_gm_command_audit_outcome.py` -- เทสที่ mock
`OSError` ของ `log_gm_command_outcome` จะไม่เคยถูกเรียกอีกต่อไปเพราะ gate ใหม่ refuse ก่อนถึง เทสจะ
ผ่านโดยไม่ทดสอบอะไรจริง) แก้แล้วเช่นกัน รัน full suite ซ้ำ: **6582 passed, 323 skipped, 0 failed**
รายละเอียดอยู่ใน round file

## nonclaim

1. ไม่อ้างว่าปิด "no coordinate range check" ทั้งหมด — ปิดเฉพาะฉากที่มี ground_extent จริง (17, 278)
2. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`
   /`scenarios/combat_*.json`
3. ไม่ลบประวัติเดิม — `chat_command_action.py`'s "ALSO OPEN" bullet ใช้ `~~strikethrough~~` + DONE
   note แทนการลบ
4. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts` — งานนี้คือ validation เพิ่มบนเส้นทางที่ GM-authenticated
   เท่านั้นอยู่แล้ว ไม่เปลี่ยนใครเป็น GM ได้

รายละเอียดเต็ม: `pf_bridge/rounds/GM_20260901_n05nxf_warp-ground-gate.md`

— LANE-GM รอบ `n05nxf`
