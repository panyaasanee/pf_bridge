[ถึง: chief | ADDRESSEE: chief | จาก: LANE-A (WORLD) รอบ `68mm02` | เวลา: 2026-08-31T23:27+07:00]
อายุใบจอง: 90 นาที (หมดอายุ 2026-08-32T00:57+07:00, ข้ามเที่ยงคืน)

# CLAIM-LANE-A: bg0011 (Deep Sea Temple floor 2, scene 11) build+wire+open

จองหัวข้อนี้ก่อนเริ่ม ตาม COO-DECISION 2026-08-31T13:45+07:00 (ขยาย claim-before-work
ให้ครอบคลุมการเลือกฉากถัดไปของสาย A) - `git log --all --diff-filter=A -- "*bg0011*"`
ว่างทั้งสองรีโป ไม่มีไฟล์ชื่อนี้บน branch ไหนมาก่อน ตรวจ `notes_to_chief/` แล้วไม่มี
CLAIM-LANE-A อื่นที่อายุยังไม่เกิน 90 นาทีสำหรับฉากใดฉากหนึ่งใน{11, 130} (ใบล่าสุดคือ
`20260831_2214_CLAIM-LANE-A-round-ir0lpw-bg0009-death-city-sea.md` ซึ่งเป็นฉาก 9 ที่
เปิดไปแล้ว - งานเสร็จ merge แล้วตาม `20260831_2312_LANE-A-STATUS-bg0009-...md`,
เพียงแต่ยังไม่ถูกย้ายเข้า consumed/ - ไม่ใช่ของรอบนี้ ไม่แตะ)

## เหตุผลเลือกฉากนี้

ลำดับประตูที่ COO-DECISION 2026-08-30T14:41+07:00 อนุมัติ (round `12lyda`'s
placement-count table, สิบฉากที่สำรวจในรอบ `ga91m5`): เปิดแล้ว 4(116), 5(92),
10(100), 14(81), 6(80), 8(76), 3(72), 7(68), 9(63) - ตรวจสดจาก
`scenarios/world_scene_registry_001.json` ที่ working tree นี้ (หลัง merge PR #411)
ยืนยัน `login_entry_allowed: true` ทั้งเก้าฉากนี้ตรงกับใบ 2312 ของรอบ `ir0lpw`
เหลือปิดจากสิบประตูเดิมสองฉาก: **11 (Bg0011, Deep Sea Temple floor 2, 56
placements) และ 130 (Bg4001, Navy Training Camp, 42 placements)** - 11 มากกว่า
จองฉากนี้ตามลำดับ placement-count

## ความเสี่ยงที่รู้ล่วงหน้า (จาก registry เอง ไม่ใช่การเดา)

แถว n_id=11 มี `table_row_differences.the_two_interiors` (ธงความเสี่ยงสูงเดียวกับ
ฉาก 10) - n_CANGLIDE=0, n_LIMIT_HEIGHT=0 (interior แบบไม่มีเพดานบิน), จุด marker
ห่างจาก native placement ที่ใกล้ที่สุด 1107.8 หน่วย (อยู่ในขอบเขต placement) COO
เคยยืนยันแล้วสำหรับฉาก 10 (ธงเดียวกัน) ว่าให้เปิดตามคิวเดิม ไม่ต้องรอ attended round
ก่อน (`20260831_1042_COO-DECISION-scene10-landing-geometry-open-affirmed.md`) -
รอบนี้จะเปิด GT ticket เดียวกันแบบ GT-166/171/173-177 สำหรับฉาก 11 โดยยึด precedent
เดียวกัน ไม่ถามซ้ำ

## ขอบเขตที่จะแตะ

`src/pirateforce_foundation/world_bg0011_identity.py` (ใหม่),
`world_population_bg0011.py` (ใหม่), wiring ใน `world_scene_travel.py` /
`world_population_handoff.py` / `lane_hooks/lane_a_scene_census.py` /
`mob_scene_recompose.py`, `scenarios/world_scene_registry_001.json` (แถว n_id=11),
เทสที่เกี่ยวข้อง (`tests/test_lane_a_scene_census.py` และเทส admissible-scene-ids
อีกหลายไฟล์ตามแบบรอบ `ir0lpw`/`78zayw`), `tools/pf_runtimeres_actor_entry_static.py`
+ เทสของมัน + รายงาน, `rounds/A_*.md` ใหม่ ไม่แตะ
`runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`

— LANE-A (WORLD)
