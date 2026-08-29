[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server session ipluns) | 2026-08-27T07:24+07:00]

ตอบ: `rounds/GM_20260827_0725_dispatch-authorization-gate-core-request-010.md` ส่วน "ค้าง (ตั้งใจ ไม่บล็อก)" ไม่ได้พูดถึงเรื่องนี้ตรง ๆ แต่ `docs/GM_LANE.md` (หัวข้อ "What is intentionally NOT built yet") ระบุไว้ชัดว่า `gm/commands.py`'s `warp` ยังไม่มีทาง execute เลยแม้แต่ทางเดียว — รอบนี้เปิดทางแรก (แคบมาก ตั้งใจให้แคบ)

# CORE-REQUEST-011 (เสนอ · รอ chief เขียนแถวลงทะเบียน `CHIEF_CONTINUATION.md`) — execute `warp` ในฉากเดียวกันผ่าน `ForcePos`

## เลขที่เสนอ
ทะเบียนล่าสุดที่พบ (`CHIEF_CONTINUATION.md` + git log ของ `pirate-force-server`) มีถึง **010** (สายนี้เอง: `CORE-REQUEST-010` inbound dispatch) — เลขถัดไปที่ว่างคือ **011**

## ① โมดูล
`src/pirateforce_foundation/gm/warp_executor.py` (ใหม่รอบนี้) ฟังก์ชัน `make_warp_force_pos_frame`

## ② ฟังก์ชันที่ต้องเรียก
```python
from pirateforce_foundation.gm.warp_executor import (
    WarpExecutorError,
    make_warp_force_pos_frame,
)

try:
    pc, frame = make_warp_force_pos_frame(
        legacy, vital_version, command, current_scene_id, z,
    )
except WarpExecutorError:
    ...  # refuse: cross-scene, scene-only form, or a malformed field -- no frame to send
```
- `command` คือ `GmCommand` (จาก `gm/commands.py.parse_gm_command`) ชนิด `warp` ที่ผ่านมาแล้วจากขั้นก่อนหน้า — โมดูลนี้ไม่ตัดสินใจว่า raw text มาจากไหน (0x51E9 wide-string decode ยังไม่พิสูจน์ ตามที่ `CORE-REQUEST-010` เขียนไว้)
- `current_scene_id` คือฉากจริงของ connection นั้น ๆ — chief เป็นคนรู้ค่านี้ (โมดูลนี้ไม่ track player state เลย) **ต้องเป็นค่าจริงจาก runtime state ไม่ใช่ค่าจากคำสั่งเอง**
- `z` คือความสูงปัจจุบันจริงของ connection นั้น (grammar ของ `warp` ไม่มี z เลย โมดูลนี้จึงไม่เดา ต้องให้ chief ส่งมา)
- `vital_version` ยังไม่พิสูจน์ (เหมือน `state_wire` เดิม) — ส่งเป็น 1 ได้ตามที่ `teleport_wire.py`/`state_wire.py` ใช้มาก่อน หรือค่าอื่นถ้า chief มีหลักฐานเพิ่ม

**ขอบเขตแคบมาก โดยตั้งใจ:** ฟังก์ชันนี้ทำได้แค่ "ย้ายตำแหน่งในฉากเดียวกัน" เท่านั้น — `ForcePos` (RE-090 PASS/DONE พิสูจน์ครบ ไม่มีฟิลด์ที่ยังไม่รู้ความหมายเลยสักตัว) ไม่มีช่อง scene id เลย ข้ามฉากไม่ได้จริง ๆ ไม่ใช่แค่เลือกไม่ทำ ถ้า `command.args[0]` (scene_id ที่ผู้ใช้พิมพ์) ไม่ตรงกับ `current_scene_id` หรือคำสั่งเป็นฟอร์ม `warp <scene_id>` (ไม่มี x y) ฟังก์ชันจะ raise `WarpExecutorError` ไม่ส่งอะไรเลย — ห้าม catch แล้วส่ง fallback เป็นการข้ามฉากเอง (จะกลายเป็นการเดา `TeleportVital` ที่ยังพิสูจน์ไม่ครบ)

## ③ ตรงไหนของ runtime
ยังไม่มีจุดเรียกอยู่เดิม (โมดูลนี้ใหม่ทั้งหมด ไม่มีอะไรให้ชนกัน) — จุดที่เหมาะคือหลัง `CORE-REQUEST-010`'s `handle_gm_run_command_vital` ตัดสินใจว่า payload มาจากบัญชี GM จริง **แต่** การ decode 0x51E9's wide-string fields ให้เป็น `GmCommand` จริงยังไม่พิสูจน์ (nonclaim เดิมของ `CORE-REQUEST-010`) — ดังนั้นรอบนี้ยังต่อสายเข้า runtime ไม่ได้จริง จนกว่าจะมีทางได้ `GmCommand` จาก client input จริง (RE เพิ่มเติมหรือ attended capture matrix) **หรือ** chief เห็นทางอื่นที่เหมาะกว่า (เช่น console/debug command สำหรับผู้เทส attended โดยตรง ไม่ผ่าน 0x51E9 เลย) — ข้อเสนอนี้ไม่ได้บังคับเส้นทางเดียว แค่ให้ฟังก์ชันพร้อมเรียกทันทีที่มีจุดเรียกจริง

## ④ เทสที่พิสูจน์
- `tests/test_gm_warp_executor.py` (10 เทสใหม่) — เฟรมตรงกับ codec ที่พิสูจน์แล้วไบต์ต่อไบต์ · ปฏิเสธคำสั่งที่ไม่ใช่ warp · ปฏิเสธฟอร์ม scene-only (ไม่มี x y) · ปฏิเสธเมื่อ scene_id ต่างจาก current_scene_id (ยืนยันด้วยว่าไม่ silently ส่งเฟรมในฉากเดิมแทน) · **หลัง pf-adversary รอบนี้:** ปฏิเสธ z ที่ไม่ finite (nan/inf) แม้คำสั่งอื่นถูกต้องครบ, ปฏิเสธ x/y ที่ไม่ finite จาก `GmCommand` ที่ไม่ได้ผ่าน `parse_gm_command` มา, ปฏิเสธ scene_id/x ที่ไม่ใช่ตัวเลขด้วย `WarpExecutorError` ไม่ใช่ `ValueError` เปล่า
- `tests/test_gm_*.py` ทั้งชุด: 150 เทสผ่านหมด (140 เดิม + 10 ใหม่)
- สวีตเต็มโปรเจกต์: 3322 passed, 327 skipped, 4986 subtests passed, 0 failed เขียว(cloud sanity) (ติดตั้ง `capstone`/`pefile`/`pytest` สดในคอนเทนเนอร์นี้ก่อนรัน — หายไปจาก python3 ของ session นี้เหมือนรอบก่อน ๆ)

## ⑤ ค้นแล้ว
ค้น `pf_bridge/external/00_SEARCH_HERE_FIRST.md` และ `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` แล้ว: เจอ — ยืนยัน `ForcePos`/`CWarpResult`/`TeleportVital` อยู่ใน `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv` ตามที่ `gm/teleport_wire.py` อ้างอิงอยู่แล้ว ไม่มีอะไรใหม่ให้ถอดเพิ่มสำหรับรอบนี้ (RE-090 ปิดแล้ว) · อ่าน `docs/GM_LANE.md` เต็มไฟล์ก่อนเริ่ม ยืนยันว่า "no command execution path" คือช่องว่างจริงที่ยังไม่มีใครทำ · grep `warp_executor`/`make_warp_force_pos_frame` ใน `runtime.py`/`app.py` แล้ว: **ไม่เจอ** ยืนยันว่าไม่มีจุดต่อสายเดิมให้ชนกัน

## ⑥ pf-adversary
รันก่อน commit — พบ 3 ข้อจริง (2 HIGH, 1 MEDIUM) ในดราฟต์แรก แก้ครบก่อน push:
1. **HIGH** `z` ไม่เคยผ่านการเช็ค finite เลยแม้แต่ทางเดียว (grammar ของ `warp` ไม่มี z ฟิลด์นี้จึงหลุดจาก `commands.py`'s `_require_number` เสมอ) — แก้ด้วยการเช็ค `math.isfinite` เองในโมดูลนี้
2. **HIGH** `docs/GM_LANE.md` เขียนไว้ตรง ๆ ว่าโมดูลนี้ต้องรับ `GmCommand` "regardless of source" — แปลว่า x/y อาจไม่เคยผ่าน `parse_gm_command` เลยเช่นกัน โมดูลเดิม trust `int()`/`float()` ตรง ๆ ไม่เช็คซ้ำ — แก้ด้วยการเช็ค finite/type เองทุกฟิลด์ตัวเลข ไม่พึ่งพา caller
3. **MEDIUM** field ที่แปลงพัง (เช่น scene_id ไม่ใช่ตัวเลข) เดิม raise `ValueError` เปล่า ไม่ใช่ `WarpExecutorError` ตามที่ docstring/เทสสัญญาไว้ ("refuses... rather than silently mis-executing") — แก้ให้ raise `WarpExecutorError` ทุกกรณี
เพิ่ม 4 เทสยืนยันทั้งสามข้อ push ก่อนปิดรอบ

## ⑦ nonclaim
ใบนี้ไม่ได้อ้างว่า `warp` ทำงานได้จริงหลังรอบนี้ — ฟังก์ชันที่สร้างยังไม่ถูกเรียกจากที่ไหนเลย (ไม่มีจุดต่อสายจริงใน runtime.py) แม้ chief ต่อสายตามข้อ ③ ก็ยังครอบคลุมแค่ "ย้ายตำแหน่งในฉากเดียวกัน" เท่านั้น — ข้ามฉาก / npc / item / lv / spawn ยังไม่มีทาง execute เลยสักทาง ไม่มี GM shortcut ใดที่ใบนี้อ้างว่าข้ามขั้นการทดสอบปกติได้จริง เพราะยังไม่มีอะไรให้ผู้เทสลองเลย
