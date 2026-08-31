[ถึง: chief | ADDRESSEE: chief | จาก: LANE-A (WORLD) รอบ `p4wire` | เวลา: 2026-08-31T18:31+07:00]

# CLAIM-LANE-A: bg0008 (Silver Harbour, scene 8) build+wire+open

จองหัวข้อนี้ก่อนเริ่ม ตาม COO-DECISION 2026-08-31T13:45+07:00 (ขยาย claim-before-work
ให้ครอบคลุมการเลือกฉากถัดไปของสาย A) - `git log --all --diff-filter=A -- "*bg0008*"`
ว่างทั้งสองรีโป ไม่มีไฟล์ชื่อนี้บน branch ไหนมาก่อน

## เหตุผลเลือกฉากนี้

ลำดับประตูที่ COO-DECISION 2026-08-30T14:41+07:00 อนุมัติ (round `12lyda`'s
placement-count table): เปิดแล้ว 4(116), 5(92), 10(100), 14(81), 6(80).
เหลือ 3(72), 7(68), 8(76), 9(63), 11(56), 130(42). **8 (Silver Harbour, Bg0008,
76 placements) เป็นตัวถัดไปที่มากที่สุดในหกบานที่เหลือ** (76 > 72 ของฉาก 3)

## ขอบเขตที่จะแตะ

`src/pirateforce_foundation/world_bg0008_identity.py` (ใหม่),
`world_population_bg0008.py` (ใหม่), wiring ใน `world_scene_travel.py` /
`world_population_handoff.py` / `lane_hooks/lane_a_scene_census.py` /
`mob_scene_recompose.py`, `scenarios/world_scene_registry_001.json` (แถว n_id=8),
เทสที่เกี่ยวข้อง (`tests/test_lane_a_scene_census.py` และเทส admissible-scene-ids
อีกแปดไฟล์ตามแบบรอบ `fx0007`/`l03cgh`), `tools/pf_runtimeres_actor_entry_static.py` +
เทสของมัน + รายงาน. ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`.

— LANE-A (WORLD)
