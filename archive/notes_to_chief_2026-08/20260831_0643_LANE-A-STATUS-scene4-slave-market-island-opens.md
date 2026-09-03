[ถึง: chief, COO | ADDRESSEE: chief | cc: COO, เจ้าของ, สาย B, สาย GM | จาก: LANE-A (สาย A · WORLD) รอบ `bq4mst` · 2026-08-31T06:43+07:00]
[ตอบใบ: `20260830_1441_COO-DECISION-scene4-slave-market-first-door.md`]

# LANE-A STATUS — ฉาก 4 (Slave Market Island) เปิดล็อกอินแล้ว ประตูแรกในสิบบานที่ COO เลือก

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ตัวละครที่แถวเซฟของตัวเองระบุฉาก 4 อยู่แล้ว หรือบัญชี GM ที่ stage ไว้ (`config/gm_login_scene.json`
scene_id=4) หรือพิมพ์ `/warp 4` ตอนนี้**เข้าฉาก 4 (เกาะตลาดทาส) ได้จริง แล้วเห็นตัวละคร/มอนสเตอร์สูงสุด 109
จาก 116 ตัวขึ้นจอ** แทนที่จะถูกปฏิเสธที่ล็อกอินด้วย `WORLD_SCENE_ENTRY_REFUSED [scene_not_allowed_at_login]`
เหมือนเมื่อวาน — เมื่อวานเกาะนี้ไม่มีใครเข้าไปได้เลยแม้แต่ทางลัด GM

## สรุปสั้น

`COO-DECISION 20260830_1441` เลือกฉาก 4 เป็นประตูแรกในสิบบาน สั่งให้สร้าง crosswalk ก่อน แล้ว **"ห้ามพลิก
`login_entry_allowed` จนกว่าตัวประกอบจะพร้อมจริง"** รอบ `6p22bu` สร้างตัวประกอบ รอบ `2jdde8` ผูกเข้าสามจุด
(`CENSUS_SOURCES`/`ROSTER_COMPOSERS`/`lane_hooks`) แต่เจตนาปิดประตูไว้ รอบนี้ตรวจเงื่อนไขทั้งสาม (D1/D2/D3
เทียบเท่าที่ฉาก 14 เคยต้องปิดก่อนเปิด) พบว่าฉาก 4 **ปลอดภัยกว่าฉาก 14** ด้วยซ้ำ เพราะ composer ของฉากนี้ไม่ส่ง
faction bit เลย (เป็นคำตัดสินของสาย B ที่ยังไม่ทำ ไม่ใช่บั๊ก) จึงพลิก `login_entry_allowed` เป็น `true`

รายละเอียดเต็มอยู่ใน `rounds/A_20260831_0643_bq4mst_scene4_slave_market_opens.md`

## ตัวเลขที่วัดได้

- targeted (11 ไฟล์ที่เกี่ยว): ผ่านหมดหลังแก้ (ดูรอบละเอียด)
- full suite: **5664 passed, 327 skipped, 9759 subtests passed, 0 failed** (รอบก่อน `pbpkv4`: 5661/327/9758)
- `tools/verify_hypothesis_ledger.py`: PASS entries=47 (ไม่เปลี่ยน)
- `git diff --stat` บน `src/`: ว่างเปล่า (ไม่แตะโค้ด Python เลยรอบนี้)
- `git diff --stat` บน `scenarios/`: 1 ไฟล์ 9 บรรทัด
- `git diff --stat` บน `tests/`: 9 ไฟล์ 225 insertions(+) 46 deletions(-)
- `git diff --stat` บน `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`: ว่างเปล่า (ไม่แตะ ไม่ต้องแตะ)

## เจอไบก์ข้ามไฟล์ 6 จุดจากการรัน full suite (ไม่ใช่แค่ targeted)

การพลิก boolean เดียวทำให้เทสที่ตรึง `admitted_scene_ids()`/`stageable_scene_ids()`/
`ADMISSIBLE_TODAY` เป็น literal ในไฟล์อื่นแดง 6 ไฟล์ (คนละสายเขียนไว้ตอนที่ฉาก 14 เปิด แล้วตรึงเป็นเลขตายตัว
ตามธรรมเนียมโปรเจกต์นี้) แก้ครบทุกไฟล์โดยเติมฉาก 4 เข้าไปในเซตพร้อมคอมเมนต์อ้างรอบนี้ ไม่แตะตรรกะอื่นของแต่ละ
ไฟล์: `test_world_faction_admission.py`, `test_gm_login_scene_admission.py`,
`test_gm_login_scene_stage.py` (ใบ `GT-141` เอง!), `test_gm_login_scene_sanctioned_barred.py`,
`test_gm_login_scene_registry_snapshot.py`, `test_gm_login_scene_override_position_resync.py`

## ไฟล์ที่แตะ (รวม `pirate-force-server` 10 ไฟล์ + `pf_bridge` 5 ไฟล์)

`pirate-force-server`: `scenarios/world_scene_registry_001.json`,
`tests/test_lane_a_scene_census.py`, `tests/test_world_scene_registry_rule_1_scenes.py`,
`tests/test_world_faction_admission.py`, `tests/test_world_scene_marker.py`,
`tests/test_gm_login_scene_admission.py`, `tests/test_gm_login_scene_stage.py`,
`tests/test_gm_login_scene_sanctioned_barred.py`, `tests/test_gm_login_scene_registry_snapshot.py`,
`tests/test_gm_login_scene_override_position_resync.py`

`pf_bridge`: `GAME_TEST_QUEUE.md` (เพิ่ม `GT-165` ใบใหม่ + อัปเดตหัวใบ `GT-144` ของตัวเองย้ายฉาก 4 ออกจาก
ขอบเขต), `rounds/A_20260831_0643_bq4mst_scene4_slave_market_opens.md` (ใหม่), จดหมายนี้,
`20260831_0643_LANE-A-REPLY-backlog-5-letters-none-blocking-archive-them.md` (ใหม่),
`FROM_CHIEF_R256_TO_LANE-A_20260831_0556.md.CONSUMED.txt` (ใหม่)

## ยังไม่ได้พิสูจน์

ยังไม่มีใครยืนดูฉาก 4 จริงบนไคลเอนต์ — เปิดใบ `GT-165` (attended) ให้ผู้เทสเดินเข้าไปดู `MARKER[4]` ยังเป็น
ชั้นหลักฐาน `authored` เท่านั้น (ไม่เคยมีไคลเอนต์ยืนจริง ห่างจาก placement ใกล้สุด 777.5 หน่วย บันทึกไว้ล่วงหน้า)
อีกเก้าฉากในสิบบาน (3,5,6,7,8,9,10,11,130) **ยังปิดเหมือนเดิมทุกตัวอักษร** ไม่มีตัวประกอบ ไม่ใช่แค่ประตูปิด

## CORE-REQUEST

ไม่มี — ประตูนี้เปิดได้โดยไม่ต้องแตะ `runtime.py`/`app.py` เลย (เกต/การอนุมาน faction เป็นของเดิมที่ทั่วไป
อยู่แล้ว ตรวจโค้ดจริงยืนยันแล้วในรอบนี้ ไม่ใช่แค่เชื่อ docstring)

## เปิดใบให้สาย C

ไม่มี — รอบนี้ไม่มีคำถามใหม่ที่ต้องส่ง RE

-- LANE-A (WORLD) รอบ `bq4mst`
