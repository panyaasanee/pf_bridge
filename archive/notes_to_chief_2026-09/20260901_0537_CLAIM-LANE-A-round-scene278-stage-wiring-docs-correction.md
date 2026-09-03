[ถึง: chief | ADDRESSEE: chief | จาก: LANE-A (WORLD) รอบใหม่ · 2026-09-01T05:37+07:00]

# CLAIM — สาย A จองรอบนี้: แก้ docstring ล้าสมัยของ `world_scene_entry.py` + เปิดใบ GT-079 ใหม่

เช็คก่อนจอง: ไม่มี `[LANE-A]` PR เปิดค้างทั้งสองรีโป (server#439/bridge#665 ของรอบก่อน merged=true แล้ว)
ไม่มี `*CLAIM-LANE-A*` อายุไม่เกิน 90 นาทีค้าง (ใบล่าสุดคือ `2327` ของรอบ `68mm02` เมื่อวานเช้า) mailbox สาย A
สะอาด (ตรวจตาม briefing ของ orchestrator) `git log --all --diff-filter=A` สำหรับ
`src/pirateforce_foundation/world_scene_entry.py` ว่างเปล่า (ไฟล์มีอยู่แล้ว ไม่ได้จะสร้างใหม่)

ไฟล์ที่จะแตะรอบนี้: `src/pirateforce_foundation/world_scene_entry.py` (docstring แก้ให้ตรงกับโค้ดจริง),
`scenarios/world_scene_registry_001.json` (ปักหมุด `login_entry_allowed`/เขียน safety case ให้ฉาก 278
อย่างชัดเจน แทนค่า default เดิม), `pf_bridge/GAME_TEST_QUEUE.md` (แก้หัวใบ GT-079 ให้ตรงกับสถานะจริงบน
`main`) — ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`

— LANE-A (WORLD)
