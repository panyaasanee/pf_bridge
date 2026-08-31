[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, เจ้าของ, สาย B, สาย GM | จาก: สาย A (WORLD) รอบ `h1utu5` · 2026-08-31T12:46+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 2026-08-30T14:58 (ไฟล์ไม่ได้อัปเดตตั้งแต่รอบ R242 ไม่ใช่นาฬิการอบนี้ผิด)]
[ตอบใบ: `20260830_1441_COO-DECISION-scene4-slave-market-first-door.md`]

# LANE-A STATUS — ฉาก 4 (Slave Market Island) มี crosswalk แล้ว 84/116 ยังไม่ต่อสาย

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มีเลย.** รอบนี้สร้างสองโมดูลใหม่ (`world_bg0004_identity.py`,
`world_population_bg0004.py`) ตามแบบ `world_bg0015_identity.py`/`world_population_bg0015.py`
ทุกประการ แต่ **ไม่มีอะไรใน `src/` เรียกใช้สองโมดูลนี้เลย** (เทสของสายนี้เองยืนยันด้วย AST-walk ว่า
importer = ว่างเปล่า) และ `login_entry_allowed` ของฉาก 4 ยังเป็น `false` ตาม
`COO-DECISION 2026-08-30T14:41+07:00` เอง ("ยังไม่แก้จนกว่าตัวประกอบจะพร้อมจริง") ผู้เล่นล็อกอินวันนี้
เห็นเหมือนเมื่อวานทุกประการ

## สิ่งที่สร้าง

- **ตัวตน (`world_bg0004_identity.py`):** crosswalk CLINE→MOBS ตรงแบบ BUILD-001 — `BG0004` อ่าน
  `n_CLINE_TYPE=4` ตรงจากตาราง (ไม่ต้องเดา เพราะเป็นหนึ่งใน 19 ฉากที่มี direct selector ตามที่
  `world_bg0015_identity` เคยนับไว้แล้ว) 47 จาก 61 แถว CLINE type 4 resolve ได้จริง จาก 116
  placement จริงของฉาก มี **84 ตัวประกอบได้** (32 ตัวไม่มีตัวตนที่ส่งได้ — Mob-Set 107 ตัวเดียวกิน 25
  ใน 32 เพราะ leader ไม่มีชื่อใน `MOBS_TIP`)
- **สำมะโน (`world_population_bg0004.py`):** ใช้ encoder เดิมทั้งชุด (`make_npc_attr` /
  `make_remote_movement_attr` / `make_remote_actor_entry` / `make_runtime_remote_actors`) ไม่มีบิต
  faction/hostile บนตัวไหน พิมพ์ `WORLD_CENSUS_BG0004 assembled=84/116` ทุกครั้งที่เรียก

พบสองความผิดปกติในข้อมูลจริง บันทึกไว้ไม่แก้เงียบ ๆ: (1) placement index 82/83 คอลัมน์ `name` เขียนว่า
"Mob_Set_34" แต่คอลัมน์ `template_ids` (ที่ถือเป็นค่าจริง) บอก 45/46 — ใช้ `template_ids` (2) ชื่อ
"Orc Chief " มีช่องว่างต่อท้ายจริงในข้อมูล `MOBS_TIP` — ส่งตามนั้น ไม่ตัดออก

## ตัวเลขที่วัดได้

เทสใหม่ 27/27 ผ่าน (`test_world_bg0004_identity.py` 14 + `test_world_population_bg0004.py` 13) ·
ทั้ง suite 5485 passed / 327 skipped / 0 failed (baseline ก่อนรอบนี้ 5483/327/0) · cp874 ผ่านทั้งสี่
ไฟล์ใหม่

## Re-pin กติกาโครงการ (แก้ตามที่ `test_static_verifier_pins_cloud.py` สั่งไว้เอง)

เพิ่ม call site หนึ่งจุดของ `make_remote_actor_entry`/`make_runtime_remote_actors` ทำให้ตัวเลขที่
ปักหมุดไว้สามชุดขยับ: `src_actor_entry_call_sites` 17→18, `src_actor_stream_call_sites` 26→27,
`src_modules_building_actor_entries` 16→17 แก้ครบสามที่ตามที่ไฟล์เทสสั่งไว้เอง
(`tools/pf_runtimeres_actor_entry_static.py`, รายงาน
`reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md`,
`tests/test_runtimeres_actor_entry_static.py`) — สามไฟล์นี้อยู่นอกเขตเขียนปกติของสายนี้
(`src/`/`scenarios/`/`rounds/`/เทสของโมดูลตัวเอง) แต่แตะเพราะไม่แตะแล้ว suite จะแดงจากการแก้ของรอบนี้
เอง และไฟล์เหล่านั้นเขียนกติกาการ re-pin ไว้เองว่าเป็นงานที่ทุกสายต้องทำเมื่อเพิ่ม call site แจ้งไว้ตรงนี้
ไม่ทำเงียบ ๆ

## ยังไม่ได้พิสูจน์

ทุกอย่างในชั้น client-observable — ไม่มีใครยืนในฉาก 4 มาก่อนในประวัติโปรเจกต์ `GT-160`
(SCENE4-SLAVE-MARKET-FIRST-EYES-001) เปิดไว้ล่วงหน้าใน `GAME_TEST_QUEUE.md` สถานะ
`BLOCKED-ON-WIRING` รอรอบต่อสายก่อน

## งานถัดไปที่เห็น (ไม่ใช่คำขอ CORE-REQUEST — เป็นงานหลายบรรทัดของ src/ ไม่ใช่บรรทัดเดียวของ
`runtime.py`)

ต่อสายฉาก 4 เข้าจุด per-scene census dispatch แบบเดียวกับที่ `lane_a_scene_census.py` ทำให้ฉาก 2/14
แล้ว (ไม่ใช่ `runtime.py` โดยตรง) — เป็นงานของสายนี้เอง ไม่ต้องรอ chief เดินสายเพิ่ม แค่รอรอบหน้าที่มี
เวลาสร้างและทดสอบให้ครบก่อนขอเปิดประตูจริง

## ไฟล์ที่แตะ (pirate-force-server)

- `src/pirateforce_foundation/world_bg0004_identity.py` (ใหม่)
- `src/pirateforce_foundation/world_population_bg0004.py` (ใหม่)
- `tests/test_world_bg0004_identity.py` (ใหม่)
- `tests/test_world_population_bg0004.py` (ใหม่)
- `tools/pf_runtimeres_actor_entry_static.py` (re-pin, นอกเขตปกติ)
- `reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md` (re-pin, นอกเขตปกติ)
- `tests/test_runtimeres_actor_entry_static.py` (re-pin, นอกเขตปกติ)
- `rounds/A_20260831_1246_h1utu5_bg0004-crosswalk.md` (ใหม่)

## ไฟล์ที่แตะ (pf_bridge)

- `GAME_TEST_QUEUE.md` (เปิด `GT-160`)
- `notes_to_chief/20260831_1246_LANE-A-STATUS-bg0004-crosswalk-built-84-of-116-door-still-shut.md` (ใบนี้)

CORE-REQUEST: none
เปิดใบให้สาย C: none
เปิดใบให้ผู้เทส: `GT-160` (BLOCKED-ON-WIRING, ยังไม่ต้องบูต)

— สาย A (WORLD) รอบ `h1utu5`
