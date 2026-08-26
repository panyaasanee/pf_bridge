# GM round 2026-08-26 ~17:1x-17:4x (+07:00) — LANE-GM first round

🎯 เปิด LANE-GM ตามคำสั่งเจ้าของ (`PANYA-ORDER` 16:1x, จดหมาย `20260826_1630`) — ยึดล็อกด้วย draft PR ทั้งสอง repo ก่อนเริ่ม (`pf_bridge#123`, `pirate-force-server#66`) แล้วสร้าง GM-001/002/003/004 ตามลำดับที่สั่งไว้

## สร้างแล้ว (`pirate-force-server`, เขตเขียนของสายนี้ทั้งหมด)
- `src/pirateforce_foundation/gm/__init__.py`, `accounts.py`, `state_wire.py`, `command_capture.py`, `scene_catalog.py`, `commands.py`, `data/gm_scene_name_tip.tsv`
- `docs/GM_LANE.md`
- `tests/test_gm_accounts.py` (9) · `test_gm_state_wire.py` (8) · `test_gm_command_capture.py` (6) · `test_gm_scene_catalog.py` (8) · `test_gm_commands.py` (19) — 50 เทสใหม่ ผ่านทั้งหมด
- `pf-adversary` รันก่อน commit ตามกฎ (ดูผลข้อล่าง)

## ผลตรวจ
- สวีตเต็ม (`python3 -m unittest discover -s tests -p "test_*.py"`): 3264 เทส, 18 error เดิม (`ModuleNotFoundError: capstone`/`pefile`/`pytest` — cloud container ไม่มีแพ็กเกจพวกนี้ ไม่เกี่ยวกับรอบนี้, มีมาก่อนรอบนี้), 212 skip เดิม — **ไม่มี regression จากรอบนี้** เขียว(cloud sanity)
- `pf-adversary` ตรวจ 5 โมดูล + เทสใหม่ก่อน commit ตามกฎบังคับ

## ยังไม่ทำ (ตั้งใจ ไม่ใช่ลืม — เหตุผลเต็มใน `docs/GM_LANE.md`)
- ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` — ขอผ่าน `CORE-REQUEST-006` (เสนอเลข รอ chief ยืนยัน) แทน
- `gm/commands.py` v1 = parse+log เท่านั้น ไม่ execute คำสั่งไหนเลย (บล็อกด้วย layout ที่ยังไม่รู้ของ `TeleportVital`/`GM_RunGMCommandResultVital` + wiring ที่ยังไม่มี)
- ยังไม่มี attended probe ที่ทำได้จริง — รอ `CORE-REQUEST-006` ต่อสายและ merge เข้า `main` ก่อน

## จดหมายที่ส่งรอบนี้
- `notes_to_chief/20260826_1731_LANE-GM-CORE-REQUEST-006-gm-state-after-login.md`
- `notes_to_chief/20260826_1732_LANE-GM-STATUS-round-one-gm001-002-003-004.md` (รวม "ค้นแล้ว: เจอ" ทั้งสองแหล่ง + แจ้งสาย A ว่า `gm/scene_catalog.py` ใช้ต่อได้)

## nonclaim
โค้ดรอบนี้ทั้งหมดยังไม่ผ่านการต่อสาย runtime และยังไม่มีการเทสในเกมจริงแม้แต่นาทีเดียว — ทุกผลข้างต้นเป็นเทสหน่วยฝั่งเซิร์ฟเวอร์ (`unittest`, ในโปรเซส, ไม่มี client) เท่านั้น

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
ยังไม่มี — รอบนี้เป็น scaffolding ล้วน (allowlist, wire builder, catalog, parser) ยังไม่ต่อเข้า runtime จริง ผู้เทสยังทำอะไรในเกมไม่ได้เพิ่มจนกว่า `CORE-REQUEST-006` จะถูก merge เข้า `main`

## ค้าง
- `CORE-REQUEST-006` รอ chief ต่อสาย + ยืนยันเลขทะเบียน
- RE-open ทั้งสามข้อจากใบ 1630 (ยังไม่มีใครทำ, ไม่ใช่ของใหม่รอบนี้)
- GM-002 ต้องการรอบ attended จริง (พิมพ์ในแชทหลายแบบ) เพื่อได้ capture มาอ่าน layout — ยังไม่มีให้จับเพราะยังไม่ต่อสาย
