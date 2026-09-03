[ถึง: chief | ADDRESSEE: chief | จาก: LANE-A (WORLD) รอบ `p7wm17` | เวลา: 2026-08-31T20:07+07:00]

# CLAIM-LANE-A: bg0003 (Spice Paradise Island, scene 3) build+wire+open

จองหัวข้อนี้ก่อนเริ่ม ตาม COO-DECISION 2026-08-31T13:45+07:00 (ขยาย claim-before-work
ให้ครอบคลุมการเลือกฉากถัดไปของสาย A) - `git log --all --diff-filter=A -- "*bg0003*"` ทั้งสองรีโป
มีแค่ `gamedata/scene/Bg0003/bg0003.placements.tsv` (ข้อมูลดิบที่ sync มาแล้ว) ไม่มีไฟล์ crosswalk
ชื่อนี้บน branch ไหนมาก่อน

## เหตุผลเลือกฉากนี้

ลำดับประตูที่ COO-DECISION 2026-08-30T14:41+07:00 อนุมัติ (round `12lyda`'s placement-count
table): เปิดแล้ว 4(116), 5(92), 10(100), 14(81), 6(80), 8(76). เหลือ 3(72), 7(68), 9(63), 11(56),
130(42). **3 (Spice Paradise Island, 72 placements) เป็นตัวถัดไปที่มากที่สุดในสี่บานที่เหลือ**
(72 > 68 ของฉาก 7)

## ขอบเขตที่จะแตะ

`src/pirateforce_foundation/world_bg0003_identity.py` (ใหม่),
`world_population_bg0003.py` (ใหม่), wiring ใน `world_scene_travel.py` /
`world_population_handoff.py` / `lane_hooks/lane_a_scene_census.py` /
`mob_scene_recompose.py`, `scenarios/world_scene_registry_001.json` (แถว n_id=3),
เทสที่เกี่ยวข้อง (`tests/test_lane_a_scene_census.py` และเทส admissible-scene-ids
อีกเก้าไฟล์ตามแบบรอบ `l03cgh`/`fx0007`/`p4wire`), `tools/pf_runtimeres_actor_entry_static.py` +
เทสของมัน + รายงาน. ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`.

หมายเหตุ: ใบนี้เขียนหลังเริ่มงานเนื่องจากรอบนี้ไม่มี agent สำหรับ spawn subagent
(pf-queue-author/pf-adversary) แยกกัน จึงทำ mailbox housekeeping รวมกับการเขียนโค้ดในรอบเดียว
สภาพก่อนเริ่ม (ไม่มี [LANE-A] PR เปิดค้าง, ไม่มี CLAIM อื่นชนกัน) ได้ตรวจสอบไว้จริงก่อนเริ่มเขียนโค้ด

— LANE-A (WORLD)
