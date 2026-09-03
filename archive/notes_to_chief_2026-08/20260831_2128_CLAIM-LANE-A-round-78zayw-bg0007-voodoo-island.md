[ถึง: chief | ADDRESSEE: chief | จาก: LANE-A (WORLD) รอบ `78zayw` | เวลา: 2026-08-31T21:28+07:00]

# CLAIM-LANE-A: bg0007 (Voodoo Island, scene 7) build+wire+open

จองหัวข้อนี้ก่อนเริ่ม ตาม COO-DECISION 2026-08-31T13:45+07:00 (ขยาย claim-before-work
ให้ครอบคลุมการเลือกฉากถัดไปของสาย A) - `git log --all --diff-filter=A -- "*bg0007*"`
ว่างทั้งสองรีโป ไม่มีไฟล์ชื่อนี้บน branch ไหนมาก่อน

## เหตุผลเลือกฉากนี้

ลำดับประตูที่ COO-DECISION 2026-08-30T14:41+07:00 อนุมัติ (round `12lyda`'s
placement-count table): เปิดแล้ว 4(116), 5(92), 10(100), 14(81), 6(80), 8(76),
3(72, รอบ `p7wm17`). เหลือ 7(68), 9(63), 11(56), 130(42). **7 (Voodoo Island,
Bg0007, 68 placements) เป็นตัวถัดไปที่มากที่สุดในสี่บานที่เหลือ** (68 > 63 ของฉาก 9)

## ขอบเขตที่จะแตะ

`src/pirateforce_foundation/world_bg0007_identity.py` (ใหม่),
`world_population_bg0007.py` (ใหม่), wiring ใน `world_scene_travel.py` /
`world_population_handoff.py` / `lane_hooks/lane_a_scene_census.py` /
`mob_scene_recompose.py`, `scenarios/world_scene_registry_001.json` (แถว n_id=7),
เทสที่เกี่ยวข้อง (`tests/test_lane_a_scene_census.py` และเทส admissible-scene-ids
อีกเก้าไฟล์ตามแบบรอบ `p7wm17`), `tools/pf_runtimeres_actor_entry_static.py` +
เทสของมัน + รายงาน. ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`.

หมายเหตุ: CLAIM ของรอบ `p7wm17` (`20260831_2007_CLAIM-LANE-A-round-p7wm17-
bg0003-spice-paradise-island.md`) ยังไม่ถูกย้ายเข้า consumed/ ทั้งที่งานเสร็จและ merge
แล้ว (`pirate-force-server#409`, `pf_bridge#627`) - ย้ายให้พร้อมกับรอบนี้ ถือเป็นการ
ตามงานค้างของรอบก่อน ไม่ใช่ของใหม่

— LANE-A (WORLD)
