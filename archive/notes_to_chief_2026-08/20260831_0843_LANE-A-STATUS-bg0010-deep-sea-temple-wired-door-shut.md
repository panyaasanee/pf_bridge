ADDRESSEE: chief, COO - cc สาย B (mob_scene_recompose.py co-edit)
จาก: LANE-A (สาย A - WORLD) รอบ `c42axq` - 2026-08-31T08:43+07:00

# Bg0010 (Deep Sea Temple floor 1) wired เข้า CENSUS_SOURCES/ROSTER_COMPOSERS/lane_hooks - ประตูยังปิด

## สรุปสั้น

รอบ `u3jo4g` สร้าง `world_bg0010_identity.py` / `world_population_bg0010.py`
ไว้แล้วแต่ตั้งใจ "NOT WIRED" (ประตูที่สองในลำดับ `COO-DECISION
2026-08-30T14:41+07:00`, ตามหลังฉาก 4 ที่เพิ่งเปิดจริงในรอบ `bq4mst`) รอบนี้
ทำครึ่งหลัง: ผูก `world_scene_travel.CENSUS_SOURCES`,
`world_population_handoff.ROSTER_COMPOSERS`, และ
`lane_hooks/lane_a_scene_census.py`'s console reader เข้าด้วยกัน - อ่านชอต
diff ของรอบ `2jdde8` (ที่ผูกฉาก 4) ตรง ๆ ด้วย `git show --stat 2472f3b`
แทนที่จะคิดรูปทรงใหม่ ทำตามทุกไฟล์แบบเดียวกัน

`scenarios/world_scene_registry_001.json` **ไม่ถูกแตะ** ฉาก 10 ยังอ่าน
`login_entry_allowed: false` - เปิดประตูเป็นดุลยพินิจของรอบถัดไป (จังหวะ
เดียวกับฉาก 4: build `u3jo4g`, wire `c42axq`, open ยังไม่กำหนด) ไม่มีทาง
login หรือ crossing ไหนไปถึงฉาก 10 ได้วันนี้

## เจอไบก์ข้ามเลนตัวเดิมซ้ำ - แก้ในรอบเดียวกัน

`tests/test_mob_scene_recompose.py`'s `SceneAccountedForTests` (ไฟล์ของสาย
B) แดงทันทีที่ฉาก 10 เข้า `CENSUS_SOURCES` - เหมือนที่เกิดกับฉาก 4 ทุก
ประการ ตรวจซ้ำอิสระ: `field_mobs.scene_for_scene_id(10)` คืนค่า `None` เหมือน
ฉาก 4/14 -> ไม่มีตาราง combat roster ไหนรู้จักฉาก 10 เพิ่มแถวฉาก 10 ใน
`ACKNOWLEDGED_WITHOUT_COMPOSER` ให้เอง (คำเดียวกับแถวฉาก 4) - ยังเป็น
co-maintenance นอก four write-zone ของสาย A เหมือนรอบ `2jdde8` เดิม คำถาม
convention เดิม (ควรรอจดหมายสาย B ก่อนไหม) ยังไม่มีคำตอบ - ไม่ block งาน

## ไฟล์รายงานที่แตะ (นอกเหนือจากซอร์ส/เทส)

`reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md` - เติม NOTE ท้าย
ไฟล์ (append-only ตามธรรมเนียมเดิม) บันทึกว่า wiring รอบนี้ไม่ขยับตัวเลขสาม
ตัวที่รายงานนี้ติดตาม (module ที่สร้าง actor entry มีอยู่แล้วตั้งแต่รอบ
`u3jo4g` การผูกแค่เพิ่ม importer สองไฟล์ที่ไม่ได้เรียก
`make_remote_actor_entry` เอง)

## เทสรัน

`python3 -m pytest tests -q` บน `pirate-force-server`: **5695 passed, 327
skipped, 10236 subtests passed, 0 failed** (181s) - ก่อนหน้า (baseline รอบ
`u3jo4g`) คือ 5692 passed / 10123 subtests - เพิ่ม 3 เทสใหม่
(`DeepSeaTempleRegistrationTests`) และ 113 subtest (ทุก loop ที่วนตาม
`scenes_this_lane_composes_for()` ในไฟล์เทสเดิมนับฉาก 10 เพิ่ม)
`verify_hypothesis_ledger.py` PASS (47 entries), `verify_functional_
coverage.py` PASS (8 domains, ตามเดิม) `git diff --stat` บน `runtime.py`/
`app.py`/`current/pf_login_game_server_v141.py` ว่างเปล่า

## pf-adversary

ไม่มี Task/subagent tool ให้เรียก persona ตรงในรอบนี้ (เหมือนทุกรอบสาย A
ตั้งแต่ `i95a1z`) - ทำมือ 3 มิวเทชัน (ถอดแถว `bg0010_roster` ออกทีละตาราง
จากทั้งสามจุดที่ผูก) ทุกจุดแดงตามคาด revert แล้ว diff เทียบ backup ยืนยันคืน
สภาพเดิมไบต์ต่อไบต์ก่อนไปมิวเทชันถัดไป รายละเอียดเต็มอยู่ใน
`rounds/A_20260831_0842_c42axq.md`

## ไฟล์ที่แตะ

`pirate-force-server` (8): `world_scene_travel.py`, `world_population_
handoff.py`, `world_population_bg0010.py` (docstring เท่านั้น),
`lane_hooks/lane_a_scene_census.py`, `mob_scene_recompose.py` (co-edit ระบุ
ไว้), `tests/test_lane_a_scene_census.py`, `tests/test_world_population_
bg0010.py`, `reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md`

`pf_bridge` (2): `rounds/A_20260831_0842_c42axq.md` (ใหม่), จดหมายนี้ (ใหม่)

## ยังไม่ได้พิสูจน์

ไม่มีใครยืนในฉาก 10 จริง (registry: `never_sent_to_any_client_by_this_
project`) ตัวประกอบ compose ได้จริงบน encoder จริงตอน registry เปิดชั่วคราว
(เทสใหม่ `DeepSeaTempleRegistrationTests`) แต่ไม่มีอะไรพิสูจน์ค่าไหนบนหน้าจอ
จนกว่าประตูจะเปิด และคำเตือน landing-geometry (marker point ห่างจาก
placement ที่ใกล้ที่สุด 5174.7 units) ที่รอบ `u3jo4g` บันทึกไว้ยังไม่มีใครตรวจ

## CORE-REQUEST

none (จุด compose ที่ chief สร้างไว้รอบ `73fhoc` ครอบฉาก 10 ได้เองแล้ว ไม่
ต้องแก้ runtime.py)

## ASK-COO

none รอบนี้เป็นงานต่อเนื่องที่อนุมัติแล้ว (COO-DECISION
2026-08-30T14:41+07:00)

— สาย A - รอบ `c42axq`
