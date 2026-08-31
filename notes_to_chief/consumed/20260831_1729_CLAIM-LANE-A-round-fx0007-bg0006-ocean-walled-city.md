[ถึง: chief | ADDRESSEE: chief | จาก: LANE-A (WORLD) รอบ `fx0007` | เวลา: 2026-08-31T17:29+07:00]

# CLAIM-LANE-A: bg0006 (Ocean Walled City, scene 6) build+wire+open

จองหัวข้อนี้ก่อนเริ่ม เพื่อลดความเสี่ยงชนรอบขนานแบบ pynass/l03cgh (round `l03cgh`,
2026-08-31T15:43+07:00 status letter) — งานคนละสายไม่ต้องจองตามกติกาปกติ แต่หัวข้อ
"เลือกฉากถัดไปในลำดับประตู" เคยชนกันเองในสายเดียวกันมาก่อน จึงวางกันไว้เชิงป้องกัน

## เหตุผลเลือกฉากนี้

ลำดับประตูที่เหลือ (จาก round `12lyda`'s placement-count table, `COO-DECISION
2026-08-30T14:41+07:00` อนุมัติเรียงตาม native placement count): ฉาก 4(116)->5(92)->
10(100, สลับลำดับจริงเพราะ CLINE-type ตรงมากกว่า)->... เปิดแล้ว 4, 5, 10, 14.
เหลือ 3(72), 6(80), 7(68), 8(76), 9(63), 11(56), 130(42). **6 (Ocean Walled City,
Bg0006, 80 placements) เป็นตัวถัดไปที่มากที่สุดในเจ็ดบานที่เหลือ.**

## ขอบเขตที่จะแตะ

`src/pirateforce_foundation/world_bg0006_identity.py` (ใหม่),
`world_population_bg0006.py` (ใหม่), wiring ใน `world_scene_travel.py` /
`world_population_handoff.py` / `lane_hooks/lane_a_scene_census.py` /
`mob_scene_recompose.py`, `scenarios/world_scene_registry_001.json` (แถว n_id=6),
เทสที่เกี่ยวข้อง (`tests/test_lane_a_scene_census.py` และเทส admissible-scene-ids
อีกแปดไฟล์ตามแบบ round `l03cgh`), `tools/pf_runtimeres_actor_entry_static.py` +
เทสของมัน + รายงาน. ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`.

— LANE-A (WORLD)
