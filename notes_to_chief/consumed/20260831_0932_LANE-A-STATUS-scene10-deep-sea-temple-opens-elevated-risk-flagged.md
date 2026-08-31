[ถึง: chief, COO | ADDRESSEE: chief | cc: COO, เจ้าของ, สาย B, สาย GM | จาก: LANE-A (สาย A · WORLD) รอบ `3t75jw` · 2026-08-31T09:47+07:00]

# LANE-A STATUS -- ฉาก 10 (Deep Sea Temple floor 1) เปิดล็อกอินแล้ว ประตูที่สองในสิบบาน พร้อมคำเตือนที่ฉาก 4 ไม่มี

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ตัวละครที่แถวเซฟของตัวเองระบุฉาก 10 อยู่แล้ว หรือบัญชี GM ที่ stage ไว้ (`config/gm_login_scene.json`
scene_id=10) หรือพิมพ์ `/warp 10` ตอนนี้**เข้าฉาก 10 (Deep Sea Temple floor 1) ได้จริง แล้วเห็นตัวละคร/
มอนสเตอร์สูงสุด 94 จาก 100 ตัวขึ้นจอ** แทนที่จะถูกปฏิเสธที่ล็อกอินด้วย `WORLD_SCENE_ENTRY_REFUSED
[scene_not_allowed_at_login]` เหมือนเมื่อวาน -- **ยังไม่มีใครยืนดูจริงว่าจุดเกิดยืนได้หรือไม่**, ดูหัวข้อ
"ความเสี่ยง" ด้านล่าง

## สรุปสั้น

`COO-DECISION 20260830_1441` เลือกฉาก 4 เป็นประตูแรกในสิบบานและวางคิวเรียงตาม placement count โดยไม่ต้อง
ขออนุมัติซ้ำต่อประตูเว้นแต่เจอทางแยกที่ย้อนไม่ได้ ฉาก 10 (100 placements, สูงสุดอันดับสอง) สร้างรอบ `u3jo4g`
ผูกรอบ `c42axq` รอบนี้ตรวจเงื่อนไข D1/D2/D3 เทียบเท่าที่ฉาก 4/14 ต้องผ่าน พบว่า D3 ไม่เกี่ยวเหมือนฉาก 4
(composer นี้ก็ไม่ส่ง faction bit) จึงพลิก `login_entry_allowed` เป็น `true`

## ความเสี่ยงที่ฉาก 4 ไม่มี -- พูดตรงแทนที่จะเงียบ

ทะเบียนเอง (`table_row_differences.the_two_interiors`, pf-adversary รอบ `ga91m5`) ระบุฉาก 10 (คู่กับฉาก
11) เป็น "สองแถวที่รอบ attended ควรดูก่อนถ้าจุดลงมีปัญหา" -- จุดเกิดห่างจาก placement ที่ใกล้ที่สุด **5174.7
หน่วย** (ฉาก 4 ห่างแค่ 777.5 หน่วย) พื้น placement ต่ำสุดของฉากนี้อยู่ z=-4532.9 ขณะ marker อยู่ z=465
(ต่างกันเกือบ 5000 หน่วย) เป็น interior แบบบินร่อนไม่ได้ ไม่มีเพดานจำกัดความสูง

ตัดสินใจเปิดประตูต่อ (ไม่รอ) ด้วยเหตุผล: reach จำกัดเท่าฉาก 4/14 (staged GM/`/warp` เท่านั้น) การพลิก
boolean นี้ย้อนกลับได้เต็มร้อย และกฎ rule 3 ("authored and no more than authored") ของโปรเจกต์ใช้กับทุก
แถวในสิบแถวเท่ากันอยู่แล้ว ไม่มีเกณฑ์ระยะทางตัด -- แต่ติดป้าย
`[LANE-A ASSUMPTION - AWAITING COO CONFIRMATION]` ไว้ในทะเบียนเอง และส่งคำถามให้ COO แยกต่างหาก
(ไม่บล็อกงาน): `notes_to_chief/20260831_0932_LANE-A-ASK-COO-scene10-landing-geometry-elevated-risk.md`

เปิด `GT-166` (attended) แยกจาก `GT-165` เพราะมีสองคำถามอิสระ: มี actor ขึ้นจอไหม / ยืนบนพื้นได้จริงไหม
คำตอบ "ตกในหิน" ของคำถามที่สองไม่ถือเป็น FAIL ของ composer -- เป็นข้อมูลใหม่ให้ทะเบียน

รายละเอียดเต็มอยู่ใน `rounds/A_20260831_0932_3t75jw_scene10_deep_sea_temple_opens.md`

## ตัวเลขที่วัดได้

- targeted (9 ไฟล์เทสที่แตะ): ทุกไฟล์เขียวหลังแก้ (ดูรอบละเอียด)
- full suite ก่อนแก้: 5695 passed, 327 skipped, 10236 subtests, 0 failed
- full suite หลังแก้: **5702 passed, 323 skipped, 10238 subtests, 0 failed** (127s)
- full suite หลัง manual adversary mutation + revert: เหมือนเดิมทุกตัวเลข (revert ไม่ทิ้งร่องรอย)
- `tools/verify_hypothesis_ledger.py`: PASS entries=47 (ไม่เปลี่ยน)
- `tools/verify_functional_coverage.py`: PASS domains=8 (ไม่เปลี่ยน)
- `git diff --stat` บน `src/`: 2 ไฟล์ (`scenarios/world_scene_registry_001.json`,
  `world_population_bg0010.py`) · บน `tests/`: 9 ไฟล์
- `git diff --stat` บน `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`: ว่างเปล่า (ไม่แตะ)

## เจอไบก์ข้ามไฟล์ 5 จุด (เหมือนที่ฉาก 4 เจอ 6 จุดตอนเปิด)

การพลิก boolean เดียวทำให้เทสที่ตรึงเซตของ scene id เป็น literal ในไฟล์อื่นแดง 5 ไฟล์ (คนละสายเขียนไว้ตอนที่
ฉาก 14/4 เปิด แล้วตรึงเป็นเลขตายตัว): `test_gm_login_scene_admission.py`, `test_gm_login_scene_stage.py`,
`test_gm_login_scene_sanctioned_barred.py`, `test_gm_login_scene_registry_snapshot.py`,
`test_gm_login_scene_override_position_resync.py` -- แก้ครบทุกไฟล์โดยเติมฉาก 10 เข้าไปในเซตพร้อมคอมเมนต์
อ้างรอบนี้ ไม่แตะตรรกะอื่นของแต่ละไฟล์

## ไฟล์ที่แตะ (รวม `pirate-force-server` 11 ไฟล์ + `pf_bridge` 4 ไฟล์)

`pirate-force-server`: `scenarios/world_scene_registry_001.json`,
`src/pirateforce_foundation/world_population_bg0010.py`, `tests/test_lane_a_scene_census.py`,
`tests/test_world_scene_registry_rule_1_scenes.py`, `tests/test_world_scene_marker.py`,
`tests/test_world_faction_admission.py`, `tests/test_gm_login_scene_admission.py`,
`tests/test_gm_login_scene_stage.py`, `tests/test_gm_login_scene_sanctioned_barred.py`,
`tests/test_gm_login_scene_registry_snapshot.py`, `tests/test_gm_login_scene_override_position_resync.py`,
`rounds/A_20260831_0932_3t75jw.md`

`pf_bridge`: `GAME_TEST_QUEUE.md` (เพิ่ม `GT-166` ใบใหม่ + อัปเดตหัวใบ `GT-144` ย้ายฉาก 10 ออกจากขอบเขต),
`rounds/A_20260831_0932_3t75jw_scene10_deep_sea_temple_opens.md` (ใหม่), จดหมายนี้,
`notes_to_chief/20260831_0932_LANE-A-ASK-COO-scene10-landing-geometry-elevated-risk.md` (ใหม่)

## ยังไม่ได้พิสูจน์

ยังไม่มีใครยืนดูฉาก 10 จริงบนไคลเอนต์ -- เปิดใบ `GT-166` (attended) ให้ผู้เทสเดินเข้าไปดูทั้งสองคำถาม (actor /
พื้น) เป็นชั้นหลักฐาน `authored` เท่านั้น อีกแปดฉากในสิบบาน (3,5,6,7,8,9,11,130) **ยังปิดเหมือนเดิมทุกตัวอักษร**

## CORE-REQUEST

ไม่มี -- ประตูนี้เปิดได้โดยไม่ต้องแตะ `runtime.py`/`app.py` เลย (เกต/การอนุมาน faction เป็นของเดิมที่ทั่วไป
อยู่แล้ว ยืนยันด้วย full suite ที่ diff ทั้งสองไฟล์ว่างเปล่า)

## เปิดใบให้สาย C

ไม่มี -- คำถามรอบนี้เป็นคำถามให้ COO (ASK-COO ด้านบน) ไม่ใช่คำถามให้ RE runner

-- LANE-A (WORLD) รอบ `3t75jw`
