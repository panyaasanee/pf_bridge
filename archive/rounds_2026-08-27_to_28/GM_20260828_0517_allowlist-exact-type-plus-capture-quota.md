# LANE-GM round `i76is0` — 2026-08-28T05:17+07:00

## บริบท
รอบก่อน (`4djeqi`) ปิด `RE-118` แล้วไม่มีโค้ดใน `gm/` ให้แก้ (client-side UI precondition ล้วน)
`CORE-REQUEST-011`/`012` ยังบล็อกเหมือนเดิม, `GT-103`/`GT-110` ยังรอ attended runner รอบนี้ไม่มีของใหม่จาก
RE queue หรือกล่องจดหมาย เลยรัน `pf-adversary` sweep เต็มกับทั้งแพ็กเกจ `gm/` แทน (rule F ข้อ ง — technical
debt ที่ pf-adversary อาจชี้ได้) sweep เต็มครั้งก่อนคือรอบ `w8t8vi`; `ccc9wj` ตรวจแค่โมดูลที่ตัวเองแตะ

## ขั้น A (addendum v2) — ตรวจชะตา PR รอบก่อน
`pull_request_read` (method `get`) บน `pf_bridge#269` และ `pirate-force-server#171` (รอบ `4djeqi`) ยืนยัน
`merged: true` ทั้งคู่, `merged_by: github-actions[bot]` — อยู่บน `main` จริง ไม่ต้อง cherry-pick
(`list_pull_requests` ยังโชว์ `merged:false` ผิดเหมือนที่เคยพบมาแล้ว — ยึด `pull_request_read get` เท่านั้น)

## ขั้น B — กล่องจดหมาย
grep `ADDRESSEE: LANE-GM` ใน `notes_to_chief/*.md` ที่ยังไม่มี `.CONSUMED.txt` คู่กัน: 2 hit แต่ทั้งคู่เป็น
ใบ `LANE-GM-STATUS` ที่สายนี้เขียนเอง (ข้อความ "ADDRESSEE: LANE-GM" ที่แมตช์เป็นแค่คำอธิบายผลการ grep ภายใน
เนื้อหา ไม่ใช่หัวใบจริง) — ไม่ใช่จดหมายเข้าใหม่ ไม่ต้อง consume ตรวจ mailbox ล่าสุด (เรียง `20260828_04xx`
ถึง `0452`) ไม่พบใบใหม่ถึง `LANE-GM` เลยตั้งแต่ใบสถานะปิดรอบ `4djeqi` (`0418`)

## งานที่ทำ (pirate-force-server)

### `gm/accounts.py`, `gm/login_scene_override.py`, `gm/dispatch.py` — exact-type fix บน allowlist gate
`pf-adversary` (subagent) พบว่าทั้งสามจุดเช็ก `isinstance(account_name, str)` ก่อนใช้ค่าเป็น
dict/frozenset key — เป็นบั๊กชนิดเดียวกับที่แพ็กเกจนี้เคยแก้ให้ `GmCommand.args` มาแล้วห้ารอบ
(`type(args) is not tuple` ไม่ใช้ `isinstance`) แต่บทเรียนนั้นไม่เคยมาถึงจุดเดียวที่ทั้งแพ็กเกจพึ่งเป็น
security invariant จริง `str` subclass ที่ override `__eq__`/`__hash__` ให้ตรงกับบัญชี GM จริงเสมอ ผ่าน
`isinstance` เดิมได้ แล้วทำให้ `frozenset.__contains__`/`dict.get` รายงานว่าตรงกับบัญชีที่ไม่เคยอยู่ในลิสต์
เลย — reproduce จริงทั้งสามจุด แก้เป็น `type(account_name) is not str` ทั้งหมด ยังไม่พิสูจน์ว่าช่องโหว่นี้ไปถึง
จากไบต์บนสายจริงได้ (`lane_hooks/lane_gm_run_command.py` ส่ง `session.token` ซึ่งเป็น `str` ธรรมดาจาก login
deserializer) แต่เป็นการละเมิด "regardless of source" ที่โมดูลนี้ประกาศไว้เองจริง สำหรับผู้เรียกภายในโปรเซส
ใด ๆ ในอนาคต

### `gm/dispatch.py` — capture-volume quota ต่อบัญชี (ช่องโหว่ resource-exhaustion ใหม่)
`pf-adversary` วัดจริง: `MAX_RAW_PAYLOAD_LENGTH` (ต่อครั้ง) กับ `RATE_LIMIT_MAX_CALLS_PER_WINDOW`/
`RATE_LIMIT_WINDOW_SECONDS` (ต่อ burst) ไม่มีตัวไหนจำกัด "ปริมาณสะสม" บัญชี GM ที่ถูกจองไว้แล้วส่ง payload
ขนาดสูงสุดที่อัตราถูกกฎหมาย (ไม่โดน rate limit เลย) เขียนไฟล์ได้ราว 4 ไฟล์/วินาที ไฟล์ละหลายร้อย KB
(hex dump ขยาย ~4.75 เท่าของ raw) ไม่มีเพดาน ไม่มีวันหยุด อยู่ในช่วงที่ rate limiter ตั้งใจปล่อยผ่านอยู่แล้ว
(round `kzwdle`: "flood guard ไม่ใช่ throttle") เพิ่ม `MAX_CAPTURED_BYTES_PER_ACCOUNT` (50 MiB ต่อบัญชี
ต่ออายุโปรเซส เหมือน scope เดิมของ rate limiter) คิดจากค่าประมาณขนาดไฟล์จริง (`_estimate_capture_file_bytes`
= raw x5 + 1KiB, มากกว่าอัตราขยายจริงเสมอ) refusal reason ใหม่ `REFUSAL_CAPTURE_QUOTA_EXCEEDED` รูปแบบ
เดียวกับ refusal อื่นทุกตัว (`authorized=True` ยังคงจริง แค่ไม่เขียนไฟล์รอบนี้)

### `docs/GM_LANE.md` — แก้อ้างอิงที่ล้าสมัย (ไม่ใช่บั๊กจริง)
เอกสารยังอ้างว่า `CORE-REQUEST-010` คือ branch inline ใน `runtime.py` เรียก `gm/dispatch.py` ตรง ๆ — จริง ๆ
ย้ายไป `lane_hooks/lane_gm_run_command.py` ตั้งแต่ `lane_hooks` ลง main แล้ว ตรวจแล้วว่า wiring ยังถูกต้อง
(argument เดิม, fail-closed ผ่าน `lane_hooks.fire`'s broad except) ไม่ใช่บั๊กที่ต้องแก้โค้ด แค่บันทึกแก้ไข
ในเอกสารตามกฎ "re-derive ก่อนอ้างอิงซ้ำ"

## pf-adversary
รันเป็น subagent เต็ม sweep ก่อน commit จริง พบ 2 ข้อสูง (allowlist exact-type, capture quota) + 1 ข้อ
เอกสารล้าสมัย ตามรายละเอียดข้างบน แก้ครบทั้งสาม เทสยืนยันทุกจุด ไม่พบข้อบกพร่องใหม่ในโค้ดที่แก้แล้ว (ตรวจซ้ำ
ด้วยการรันเทสทั้งชุดหลังแก้)

## เกณฑ์สองชั้น
- wire/DB: ไม่มีของใหม่รอบนี้ (ไม่แตะ wire fact ใด ๆ)
- client-observable: ไม่มีของใหม่รอบนี้ (headless robustness round ล้วน)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
ไม่มีความสามารถใหม่บนจอ (headless round) — แต่ allowlist gate ที่สถานะ GM ทั้งหมดพึ่งอยู่ตอนนี้ปิดช่องโหว่
ประเภท "subclass โกหก" ที่แพ็กเกจนี้เคยแก้ให้ args มาแล้ว และการเขียนไฟล์ capture ของบัญชี GM หนึ่งบัญชีมีเพดาน
รวมแล้ว (ก่อนหน้านี้ไม่มี แม้จะอยู่ในเรตที่กฎหมายอนุญาต)

## nonclaim
รอบนี้ headless ล้วน ไม่มีการยิงเฟรมใส่ไคลเอนต์จริง ไม่รันเกมจริง ไม่แตะ `runtime.py` (แก้แค่เอกสารอ้างอิง
ไฟล์ที่ถูกต้อง ไม่แก้ตรรกะ) ไม่เปลี่ยนพฤติกรรม happy-path ของบัญชี GM จริงใด ๆ ที่ใช้ `str` ธรรมดา (ไม่ใช่
subclass) และไม่เกิน 50 MiB ต่อบัญชี ไม่พิสูจน์ว่าช่องโหว่ subclass เข้าถึงได้จากไบต์บนสายจริง (ดูรายละเอียด
ข้างบน) — เป็นการปิดช่องว่างตาม threat model ที่แพ็กเกจประกาศเองเท่านั้น ไม่ใช่การพิสูจน์ exploit จากภายนอก
