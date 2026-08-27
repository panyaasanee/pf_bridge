# รอบ `dnh0ai` -- LANE-GM: pf-adversary กวาดโมดูลใหม่ของ `gm/` ปิดช่องจริง 1 ข้อ (2026-08-27 21:2x +07:00)

## บริบท

รอบก่อน (`beaoxq`) เป็นรอบสถานะล้วน ไม่มีโค้ดเปลี่ยน (บล็อกอยู่ที่ `CORE-REQUEST-011/012/020`) ตามกฎ
ADDENDUM ข้อ F ห้ามรอบสถานะเปล่าติดกันเกิน 1 รอบ รอบนี้จึงต้องหยิบงานจริงแม้ `CORE-REQUEST-011`/`012`
ยังบล็อกอยู่เหมือนเดิม (ดูด้านล่าง)

## ต้นรอบ: ตรวจล็อกตาม ADDENDUM v2

ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo ตอนต้นรอบ -- เปิด draft PR ยึดล็อก (`pf_bridge#237`,
`pirate-force-server#148`)

ตรวจ PR ปิดล่าสุดของสายนี้ทั้งสอง repo ด้วย `pull_request_read`: `pf_bridge#231` และ
`pirate-force-server#141` ทั้งคู่ `merged: true` -- งานรอบก่อนอยู่บน `main` แล้ว ไม่ต้องกู้อะไร

กล่องจดหมาย: grep `ADDRESSEE: LANE-GM` -- ไม่มีใบใหม่ที่ต้องบริโภครอบนี้ (ใบล่าสุด, `CHIEF-REPLY-CORE-
REQUEST-020-bt-gm-field-wired` ที่ 20:14 ถูกบริโภคไปแล้วก่อนรอบ `beaoxq` ปิด) ตรวจซ้ำอีกครั้งกลางรอบ (หลัง
merge branch เข้า main) ก็ไม่มีใบใหม่

ตรวจ `runtime.py` (อ่านอย่างเดียว) ยืนยัน `field_0x0b_second` เป็น `0, 1, 0` แล้วจริง (`CORE-REQUEST-020`
ต่อสายและ merge บน main แล้ว) และ `tests/test_gm_login_state_guard.py` ตรงกับค่านี้แล้ว -- ปิดข้อนี้จริง
ไม่ต้องทำอะไรต่อ `CORE-REQUEST-011`/`012` ยังไม่มีจดหมายตอบ -- ยังบล็อกด้วยช่องว่างความหมายเดียวกับที่
`docs/GM_LANE.md` "RE requests open" บันทึกไว้แล้ว (สองสตริงกว้างของ `0x51E9` ยังไม่รู้ความหมาย ต้องรอ
capture จริงจาก GT-103 ไม่ใช่ RE ticket ใหม่) -- ไม่เดา ไม่เปิดใบซ้ำ

## สิ่งที่ทำ (pirate-force-server, `pirate-force-server#148`)

ไม่มีงาน wire ใหม่ให้ทำ (บล็อกตามข้างบน) จึงหยิบ "technical debt ที่ pf-adversary เคยชี้" ตามกฎข้อ F(ง):
รัน `pf-adversary` (subagent) กับโมดูลใหม่ทั้งหมดที่เพิ่มเข้ามาหลังรอบกวาดเต็มแพ็กเกจล่าสุด (`50x5xt`) --
`say_wire.py`, `teleport_wire.py`, `warp_executor.py`, `npc_switch_catalog.py`,
`login_scene_override.py` -- บวกตรวจซ้ำทั้งแพ็กเกจอีกครั้ง

**พบ 1 ข้อจริง:**

- **`gm/commands.py`**: `describe_warp_target`/`describe_npc_target` เช็ค*รูปร่าง*ของ `command.args`
  ผ่าน `_require_args_tuple` (ของแก้จากรอบ `50x5xt`) แล้ว แต่จากนั้นเรียก `int(args[0])`/`int(args[1])`
  ตรง ๆ ไม่มี `try`/`except` เลย -- tuple ที่รูปร่างถูกต้องแต่เนื้อหาไม่ใช่ตัวเลข
  (`GmCommand("warp", ("abc",), "warp abc")`) จะโยน `ValueError` เปล่า ๆ หลุดออกมาแทนที่จะเป็น
  `GmCommandArgsError` ของโมดูลเอง ขัดกับ docstring ของ `GmCommandArgsError` เองที่บอกว่าโมดูลนี้รับ
  `GmCommand` "regardless of source" เหมือน `warp_executor.py`/`say_wire.py`
- **reachability**: `grep -rn "describe_warp_target|describe_npc_target" src/` -- ยังไม่มีจุดเรียกจริงจาก
  `runtime.py`/`lane_hooks/` เลย (เรียกจากเทสของตัวเองเท่านั้น) จึงเป็นบั๊กแฝง (latent) ยังไม่ครัชอะไรวันนี้
  แต่จะเป็นบั๊กตัวแรกที่โดนทันทีที่รอบไหนต่ออนาคตเชื่อมสองสตริงกว้างของ `0x51E9` (ที่ยังไม่รู้ความหมาย,
  ดูข้างบน) เข้ามาเป็น `GmCommand` แบบข้าม `parse_gm_command`
- **ไม่พบอื่น**: rate limiter, filename-collision loop, wire codec round-trip (`command_wire.py`,
  `teleport_wire.py`), fail-closed authorization (`accounts.py`/`dispatch.py`/
  `login_scene_override.py`), SHA pin ของสองตาราง data ที่ commit ไว้ -- ลองหักทุกจุดแล้วไม่หลุด

**แก้จริง**: เพิ่ม `_require_arg_int(value, label)` ใน `commands.py` (โยน `GmCommandArgsError` ไม่ใช่
`GmCommandParseError` -- อยู่ตระกูล args-shape เพราะเป็น "regardless of source" path ไม่ใช่ path parse
จาก text) ใช้แทน `int()` ตรง ๆ ทั้งสองจุด

## เทส

`tests/test_gm_commands.py`: 2 เทสใหม่ใน `ArgsShapeGuardTests` (tuple รูปร่างถูก เนื้อหาไม่ใช่เลข ต้องโยน
`GmCommandArgsError` ทั้ง warp/npc) · `tests/test_gm_*.py` ทั้งชุด: 234/234 (232 เดิม + 2 ใหม่) ·
repo-wide `pytest tests/ --continue-on-collection-errors`: 3536 passed, 212 skipped, 17 error เดิม
(`ModuleNotFoundError: capstone`, ยืนยันแล้วไม่เกี่ยวกับ `gm/`, baseline เดิมทุกรอบ) ไม่มี failure ใหม่

## ค้นแล้ว: ไม่เจอ (ไม่เกี่ยวข้องรอบนี้)

รอบนี้ไม่พึ่งข้อมูลจาก client เลย -- แก้ความทนทานของโค้ดบนโครง wire ที่พิสูจน์แล้วทั้งหมด กฎ "ค้นก่อนถอด"
ไม่มีผลกับรอบนี้

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- ไม่มีจุดเรียกจริงจาก `runtime.py`/`lane_hooks/` ที่เปลี่ยน (`describe_warp_target`/
`describe_npc_target` ยังไม่ถูกเรียกจากที่ไหนนอกเทสของตัวเอง) เป็นการปิดบั๊กแฝงก่อนมันครัช ไม่ใช่ฟีเจอร์
ใหม่ที่ผู้เทสจะเห็น

nonclaim: ไม่มีการอ้างว่าคำสั่ง `warp`/`npc` ทำงานจริงหรือถูกส่งออกไปจริง -- ยังไม่มีจุดส่งข้อมูลไปยัง socket
ในรอบนี้ ไม่มีการเปลี่ยนพฤติกรรมบน happy path (args ที่เป็นตัวเลขถูกต้องให้ผลเหมือนเดิมทุกไบต์) ไม่มีการแก้
`runtime.py` ไม่มีการยิงเฟรมหรือรันเทสเกมใด ๆ
