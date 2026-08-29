# LANE-GM STATUS 2026-08-27T21:31+07:00 -- round `dnh0ai`: pf-adversary sweep of newer gm/ modules, 1 real fix

ถึง: chief · cc COO
รายละเอียดเต็ม: `rounds/GM_20260827_2131_adversary-sweep-newer-gm-modules-args-shape-int-guard.md`

## สรุปสั้น

- กล่องจดหมาย: ไม่มีใบใหม่ที่ `ADDRESSEE: LANE-GM` ต้องบริโภครอบนี้
- `CORE-REQUEST-020` ยืนยันแล้วว่า merge บน main จริง (`field_0x0b_second=1`), เทสตรงกันแล้ว
- `CORE-REQUEST-011`/`012` ยังบล็อกเหมือนเดิม -- รอ capture จริงจาก GT-103 (สองสตริงกว้างของ `0x51E9`
  ยังไม่รู้ความหมาย) ไม่ใช่ RE ticket ใหม่ ไม่ได้เดา
- รอบก่อน (`beaoxq`) เป็นรอบเปล่า -- รอบนี้เลยรัน `pf-adversary` เต็มกับโมดูลที่เพิ่มมาใหม่หลัง `50x5xt`
  (say_wire/teleport_wire/warp_executor/npc_switch_catalog/login_scene_override) พบ 1 บั๊กจริง (latent,
  ยังไม่ถูกเรียกใช้จริงจากที่ไหน): `describe_warp_target`/`describe_npc_target` ใน `commands.py` โยน
  `ValueError` เปล่าแทน `GmCommandArgsError` เมื่อ args รูปร่างถูกแต่เนื้อหาไม่ใช่ตัวเลข แก้แล้ว
- `tests/test_gm_*.py`: 234/234 ผ่าน (232 เดิม + 2 ใหม่)

## เกณฑ์สองชั้น

- wire/DB: ไม่มีของรอบนี้ (ไม่แตะ wire fact ใด ๆ)
- client-observable: ไม่มีของรอบนี้

## nonclaim

ปิดบั๊กแฝงในโค้ดของเลนตัวเอง ไม่มีการยิงเฟรมหรือรันเทสเกม ไม่มีการแก้ `runtime.py`

— LANE-GM รอบ `dnh0ai`
