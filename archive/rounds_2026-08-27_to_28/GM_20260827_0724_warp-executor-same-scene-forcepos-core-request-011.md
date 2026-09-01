# GM round 2026-08-27 ~07:1x-08:0x (+07:00) — same-scene `warp` execution via `ForcePos` (CORE-REQUEST-011)

ยึดล็อกด้วย draft PR ทั้งสอง repo ก่อนเริ่ม (`pf_bridge#171`, `pirate-force-server#97`) — ตรวจ GitHub API ก่อนยึดล็อก: ไม่มี PR หัวข้อขึ้นต้น `[LANE-GM]` เปิดค้างในทั้งสอง repo (pf_bridge มีแค่ `[LANE-E]` #170, pirate-force-server มี `[LANE-E]` #96 และ `[LANE-A]` #91 — ไม่ใช่ล็อกของสายนี้ ไม่แตะ)

## ตรวจสถานะก่อนเริ่มงานจริง

ยืนยัน `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (ขั้นแรกบังคับของทุกรอบ) · อ่านจดหมาย order 1630 ซ้ำ · อ่าน `docs/GM_LANE.md` เต็มไฟล์ + จดหมายสถานะรอบก่อน (`20260827_0725`, CORE-REQUEST-010) เต็มฉบับ: `CORE-REQUEST-010` ยังไม่ถูก chief ต่อสายเข้า `runtime.py` (grep `0x51E9`/`handle_gm_run_command_vital` ใน `runtime.py`/`app.py` = ศูนย์ผลลัพธ์ ยืนยันแล้ว) และ `GM_RunGMCommandVital`'s wide-string decode ยังไม่พิสูจน์ — ยังไม่มี RE ใหม่หรือ CHIEF-REPLY เจาะจงสายนี้เข้ามาตั้งแต่รอบก่อน

**ค้นแล้ว: เจอ** — `pf_bridge/external/00_SEARCH_HERE_FIRST.md`/`gamedata/00_SEARCH_HERE_FIRST.md`: `ForcePos`/`CWarpResult`/`TeleportVital` อยู่ใน `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv` แล้ว (RE-090 ปิดแล้วตั้งแต่รอบก่อนหน้า) ไม่มีอะไรใหม่ให้ถอดเพิ่มสำหรับรอบนี้

เนื่องจากยังไม่มี RE ใหม่และ CORE-REQUEST-010 ยังไม่ถูกต่อสาย รอบนี้เลือกทำสิ่งที่สร้างได้โดยไม่ต้องรอทั้งสองอย่าง: `gm/commands.py` เก็บ `GmCommand` ที่ parse แล้วไว้เฉย ๆ (ไม่ผูกกับ 0x51E9 ตามที่โมดูลนั้นเลือกไว้เอง) แต่ยังไม่มีใครเอาไปสร้างเฟรมจริงเลยสักตัว — และ `gm/teleport_wire.py`'s `ForcePos` (RE-090 พิสูจน์ครบ ไม่มีฟิลด์ค้าง) เป็นจุดที่ปลอดภัยที่สุดที่จะเริ่ม เพราะไม่ต้องเดาอะไรเลยสักตัว ต่างจาก `TeleportVital` ที่ยังมีฟิลด์ไม่รู้ความหมายอยู่หลายตัว

## สร้าง (`pirate-force-server`, เขตเขียนของสายนี้ทั้งหมด)

- **ใหม่** `gm/warp_executor.py` — `make_warp_force_pos_frame(legacy, vital_version, command, current_scene_id, z)` เชื่อม `GmCommand` ชนิด `warp` (จาก `gm/commands.py`) เข้ากับเฟรม `ForcePos` จริง **เฉพาะกรณีย้ายตำแหน่งในฉากเดียวกันเท่านั้น** — `ForcePos` ไม่มีช่อง scene id เลย ข้ามฉากไม่ได้จริง ๆ ถ้า `scene_id` ที่คำสั่งขอไม่ตรงกับ `current_scene_id` ที่ caller ส่งมา หรือคำสั่งเป็นฟอร์ม `warp <scene_id>` ไม่มี x y ฟังก์ชัน raise `WarpExecutorError` ไม่ส่งอะไรเลย ไม่เดาแทน — ข้ามฉากจริงต้องรอ `TeleportVital` ที่ยังมีฟิลด์ไม่รู้ความหมายอยู่ (`field_0x10`/`field_0x11`/`field_0x18`/`field_0x20`/`field_0x22` และ `TeleportAux` เกือบทุกฟิลด์)
- **ใหม่** `tests/test_gm_warp_executor.py` (10 เทส หลังแก้ตาม adversary)
- **แก้** `gm/commands.py` — docstring เขียนไว้เก่าว่า execute `warp` "ยังไม่พิสูจน์" ทั้งที่ `ForcePos` พิสูจน์ครบแล้วตั้งแต่ RE-090 แก้ให้ตรงสถานะจริง (ยังไม่ execute เพราะยังไม่มีจุด send จริง ไม่ใช่เพราะ layout ไม่รู้)
- **แก้** `docs/GM_LANE.md` — เพิ่มหัวข้อ "Modules delivered (warp-executor round)" + แก้บรรทัด "no command execution path" ให้ตรงสถานะใหม่

## `pf-adversary` (บังคับก่อน commit)

รอบเดียว พบ 3 ข้อจริง (2 HIGH, 1 MEDIUM) ในดราฟต์แรก:

1. **HIGH** — `z` เป็นพารามิเตอร์ที่ `warp` grammar ไม่มีเลย จึงไม่เคยผ่านการเช็ค `math.isfinite` ของ `commands.py`'s `_require_number` แม้แต่ทางเดียว — ทดสอบจริงยืนยัน: คำสั่ง `warp 1 100 200` ที่ parse ถูกต้องสมบูรณ์ ยังส่ง `z=nan` เข้าไปสร้างเฟรมได้เงียบ ๆ (45 ไบต์ มี NaN อยู่ในไบต์จริง) — ตรงกับที่ `commands.py`'s own comment เตือนไว้ว่าเป็น "landmine for whoever wires real warp execution" เป๊ะ เพียงแต่หลุดผ่านแกน z ที่ comment เดิมไม่ครอบ แก้ด้วยการเช็ค finite เองในโมดูลนี้ทุกฟิลด์
2. **HIGH** — `docs/GM_LANE.md` เขียนพันธะไว้ตรง ๆ ว่าโมดูลนี้ต้องรับ `GmCommand` "regardless of source" (เหมือน `commands.py` เอง) แปลว่า x/y ก็อาจไม่เคยผ่าน `parse_gm_command` เลยเช่นกัน — ทดสอบจริงยืนยัน: `GmCommand("warp", ("1","nan","inf"), ...)` ที่สร้างตรง ๆ ไม่ผ่าน parser เลย ยังสร้างเฟรมได้เงียบ ๆ เหมือนกัน แก้ด้วยการเช็ค finite/type เองทุกฟิลด์ตัวเลข ไม่พึ่งพาว่า caller ผ่าน parser มาหรือไม่
3. **MEDIUM** — ฟิลด์ที่แปลงพัง (เช่น scene_id ไม่ใช่ตัวเลข) เดิม raise `ValueError` เปล่า ไม่ใช่ `WarpExecutorError` ตามที่ docstring/เทสสัญญาไว้ ("refuses... rather than silently mis-executing") — caller ที่เขียนมาจับเฉพาะ `WarpExecutorError` จะพังแทนที่จะ refuse อย่างสุภาพ แก้ให้ raise `WarpExecutorError` ทุกกรณี

ตรวจแล้วไม่พบช่องโหว่จริงอีก: ลำดับ x/y (ไม่สลับ — เทสเดิมใช้ค่าที่แยกแยะได้ 100.5 vs 200.25 round-trip ผ่าน decode จับได้อยู่แล้ว), การสร้างซองเฟรม (ใช้ `make_force_pos_frame`/`legacy.make_runtime_vital` เดิมที่พิสูจน์แล้วตรง ๆ ไม่มีจุดใหม่ให้พัง), การเช็ค scene mismatch เอง (ลองพลิกชนิดข้อมูล str/int แล้ว ไม่มีทางบายพาสเจอ) · หมายเหตุที่ยังไม่ปิด: `scene_id`/`current_scene_id` ที่เป็นค่าติดลบหรือ 0 ยังไม่ถูกปฏิเสธ (เช็คแค่ equality ไม่เช็ค sanity) — ไม่ยืนยันว่าเป็นช่องโหว่จริงเพราะไม่รู้ว่า `current_scene_id` จะเป็น sentinel แบบนั้นได้จริงหรือไม่ (นอกขอบเขตที่ตรวจได้จากสองไฟล์นี้อย่างเดียว) บันทึกไว้เป็นข้อสังเกต ไม่บล็อกรอบนี้

เพิ่ม 4 เทสยืนยันสามข้อที่แก้ push ก่อนปิดรอบ

## เทส

`test_gm_warp_executor.py` 10 เทสใหม่ผ่านหมด (6 เดิมของดราฟต์แรก + 4 ใหม่จาก adversary) · `test_gm_*.py` ทั้งชุด 150 เทสผ่านหมด (140 เดิม + 10 ใหม่) · สวีตเต็มโปรเจกต์ (ติดตั้ง `capstone`/`pefile`/`pytest` สดในคอนเทนเนอร์นี้ก่อนรัน — หายไปจาก python3 ของ session นี้เหมือนรอบก่อน ๆ): **3322 passed, 327 skipped, 4986 subtests passed, 0 failed** เขียว(cloud sanity)

## push

`pirate-force-server` บน `claude/youthful-johnson-ipluns` (PR #97)

## จดหมาย

`notes_to_chief/20260827_0724_LANE-GM-CORE-REQUEST-011-same-scene-warp-via-forcepos.md` — ขอเลข CORE-REQUEST-011 (เลขถัดจาก 010 ของสายนี้เอง)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ยังไม่มี — รอบนี้เป็นโค้ด/เอกสารฝั่งเซิร์ฟเวอร์ล้วน ฟังก์ชันที่สร้างยังไม่ถูกเรียกจากที่ไหนเลย (ไม่มีจุดต่อสายเข้า `runtime.py` — รอ chief พิจารณาตาม CORE-REQUEST-011 ข้อ ③ ซึ่งยังไม่มีเส้นทางที่ชัดเจนจนกว่า 0x51E9 decode จะพิสูจน์ หรือ chief เลือกเส้นทางอื่น เช่น debug console สำหรับ attended) ไม่มีอะไรให้ client เห็นต่างไปจากเดิม

## nonclaim

ไม่มีการอ้างว่าคำสั่ง `warp` (หรือคำสั่งอื่นใด) ทำงานได้จริงหลังรอบนี้ — สิ่งเดียวที่สร้างคือฟังก์ชันที่แปลง `GmCommand` เป็นเฟรมจริงสำหรับกรณีแคบมาก (ย้ายในฉากเดียวกัน) พร้อมให้ chief เรียกเมื่อมีจุดเรียกจริง ยังไม่มี effect ในเกมเลยสักอย่าง ข้ามฉาก / npc / item / lv / spawn ยังไม่มีทาง execute เลยสักทางเหมือนเดิม

## ค้าง (ตั้งใจ ไม่บล็อก)

- CORE-REQUEST-010 (0x51E9 inbound dispatch) รอ chief ต่อสายจริง — ค้างจากรอบก่อน ไม่ใช่ของใหม่รอบนี้
- CORE-REQUEST-011 (this round) รอ chief พิจารณาว่ามีจุดเรียกจริงหรือยัง (ขึ้นกับ CORE-REQUEST-010 หรือเส้นทาง debug console อื่น)
- `scene_id`/`current_scene_id` ที่เป็นค่าติดลบหรือ 0 ยังไม่ถูกปฏิเสธ (pf-adversary หมายเหตุ LOW ที่ยังไม่ยืนยันว่าเป็นช่องโหว่จริง)
- การ decode สองฟิลด์ wide-string ของ `GM_RunGMCommandVital` เป็นชื่อคำสั่ง/argument จริง ยังต้องรอ RE หรือ attended capture matrix — ค้างจากหลายรอบก่อน ไม่ใช่ของใหม่
- `TeleportTarget` field-order ยังไม่เทียบกับ 132 candidate frame ที่ `A2_STATIC_OPEN` — ค้างจากหลายรอบก่อน ไม่ใช่ของใหม่
