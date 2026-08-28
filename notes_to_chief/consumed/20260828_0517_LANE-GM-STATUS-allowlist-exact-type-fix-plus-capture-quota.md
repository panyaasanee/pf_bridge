# LANE-GM STATUS 2026-08-28T05:17+07:00 -- round `i76is0`: allowlist exact-type fix, capture-volume quota

ถึง: chief · cc COO
รายละเอียดเต็ม: `rounds/GM_20260828_0517_allowlist-exact-type-plus-capture-quota.md`

## สรุปสั้น
- ขั้น A (addendum v2): `pf_bridge#269`/`pirate-force-server#171` (รอบ `4djeqi`) ยืนยัน `merged: true`
  ทั้งคู่ผ่าน `pull_request_read get` -- อยู่บน `main` จริง ไม่ต้อง cherry-pick
- กล่องจดหมาย: ไม่มีใบใหม่ถึง `LANE-GM` ตั้งแต่ปิดรอบ `4djeqi`
- `CORE-REQUEST-011`/`012` ยังบล็อกเหมือนเดิม -- ไม่มีอะไรใหม่จาก chief ฝั่งนั้น
- รอบนี้ไม่มี RE queue ใหม่ให้ทำ เลยรัน `pf-adversary` full sweep ของ `gm/` ทั้งแพ็กเกจ (sweep เต็มครั้งก่อน
  คือรอบ `w8t8vi`) พบ 2 ข้อจริงระดับสูง แก้ครบทั้งคู่:
  1. `gm/accounts.py`, `gm/login_scene_override.py`, `gm/dispatch.py` เช็ก `isinstance(account_name, str)`
     ก่อนใช้เป็น dict/frozenset key -- `str` subclass ที่โกหกผ่าน `__eq__`/`__hash__` ผ่านการเช็กเดิมได้แล้ว
     ทำให้บัญชีที่ไม่เคยอยู่ใน allowlist ดูเหมือนตรงกับบัญชี GM จริง แก้เป็น `type(account_name) is not str`
     ทั้งสามจุด (ยังไม่พิสูจน์ว่าไปถึงจากไบต์บนสายจริงได้ -- `session.token` เป็น `str` ธรรมดาเสมอ -- แต่เป็น
     ช่องโหว่จริงสำหรับผู้เรียกภายในโปรเซสใด ๆ)
  2. `gm/dispatch.py` ไม่มีเพดานปริมาณสะสมของการเขียน capture file ต่อบัญชี -- บัญชี GM ที่ถูกจองไว้ส่ง
     payload ขนาดสูงสุดที่อัตราถูกกฎหมาย (ไม่โดน rate limit) เขียนดิสก์ได้ไม่จำกัดตลอดเวลา เพิ่ม
     `MAX_CAPTURED_BYTES_PER_ACCOUNT` (50 MiB/บัญชี/อายุโปรเซส) ปิดช่องนี้
  3. (เอกสารเท่านั้น ไม่ใช่บั๊ก) `docs/GM_LANE.md` อ้าง call site เก่าของ `CORE-REQUEST-010` ผิด -- จริง ๆ
     ย้ายไป `lane_hooks/lane_gm_run_command.py` แล้ว wiring ยังถูกต้อง แก้แค่คำอธิบาย
- `tests/test_gm_*.py`: 259/259 (up from 250, 9 ใหม่). Repo-wide `unittest discover`: 3846 tests, 18
  pre-existing `capstone`-import errors เท่านั้น (baseline เดิม) ไม่มี failure ใหม่

## เกณฑ์สองชั้น
- wire/DB: ไม่มีของรอบนี้
- client-observable: ไม่มีของรอบนี้ (headless robustness round ล้วน)

## nonclaim
รอบนี้ headless ล้วน ไม่มีการยิงเฟรม ไม่รันเกมจริง ไม่แก้ `runtime.py` (แก้แค่คำอธิบายในเอกสารของสายตัวเอง)
ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: ไม่มีความสามารถใหม่บนจอ -- ปิดช่องโหว่ allowlist-subclass และปิดเพดาน
ปริมาณ capture สะสมที่ไม่เคยมีมาก่อน

— LANE-GM รอบ `i76is0`
