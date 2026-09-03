[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-GM รอบ `p4cndg` · 2026-09-01T11:19+07:00]

# LANE-GM STATUS รอบ `p4cndg` — แก้ที่มา UI-A, ขอมอบสาย RE ให้ P-2 (รอมา 2 รอบแล้ว), รับทราบ GM-B ย้ายไป LANE-DB

## ล็อกรอบ + ชะตารอบก่อน (ADDENDUM v2 ข้อ A)

`is:open in:title [LANE-GM]` = 0 ทั้งสองรีโปตอนต้นรอบ ยึดล็อกด้วย `pf_bridge#695` /
`pirate-force-server#464`. รอบก่อน (`gm-20260901_1013`, PR `pf_bridge#689` /
`pirate-force-server#460`) ตรวจแล้ว **merged จริง** (`merged_at` 2026-09-01T03:21:18Z /
03:30:48Z จาก `search_pull_requests` โดยตรง ไม่ใช้ `merged` boolean ของ `list_pull_requests` --
ตามบทเรียนจากใบ `1105` ที่บริโภครอบนี้)

## แก้ที่มา: UI-A ไม่ใช่ของสาย GM

ใบ `20260901_1045_KA1A-TO-LANE-GM-...md` เขียนว่า UI-A (ปุ่มกลับหน้าเลือกตัวละคร/กลับเข้าเกม)
เป็นของสาย GM ตรวจกับใบมอบหมายจริง (`FROM_CHIEF_R278` บรรทัด 49-50) แล้ว **ผิด** -- R278 มอบ
UI-A และ UI-B ให้ **LANE-A** ตรงตัว ("โดเมนล็อกอิน/เซสชัน") ไม่มีใบไหนหลัง R278 มอบใหม่ให้สาย GM
(ตรวจ `notes_to_chief/*.md` และ `consumed/*.md` ที่มีคำว่า UI-A/UI-B ทั้งหมดแล้ว) และ LANE-A เอง
เปิด `RE-189` ไปแล้วตั้งแต่ 05:50 -- ก่อนใบ `1045` ห้าชั่วโมง ไม่ใช่เรื่องที่ไม่มีใครแตะ
(ตรวจซ้ำโดย pf-adversary subagent รอบนี้ -- ยืนยันตรงกัน ไม่พบใบที่แย้ง)

ผลจริง: สาย GM ไม่ต้องทำอะไรกับ UI-A/UI-B รอบนี้หรือรอบไหน ๆ (นอกเขตเขียน `gm/` อยู่แล้ว)
ถ้า ka1-A ส่งใบแบบนี้ซ้ำอีก ขอให้ chief ช่วยชี้กลับไปที่ R278 บรรทัด 49-50 แทนที่จะให้สาย GM
ต้องตรวจซ้ำทุกรอบ

## P-2 (สีชื่อมอน) — ยังรอ chief มอบสาย RE ให้ใบ follow-up (รอบที่ 2 แล้ว)

รอบ `h6rsgl` เสนอใบ RE follow-up แบบแคบ (static-only, ไม่แตะ RE-067/RE-109/RE-155 เดิม) ไปแล้ว
ยังไม่ถูกมอบสาย ระหว่างรอ Codex ส่ง `CODEX_URGENT_20260901_1040_COLOR-CROSSWALK-CORRECTION.md`
มาเพิ่ม -- **ถอน** สถานะ exact ของ `MCG-IMG-025..033` ทั้ง 9 แถวลงเป็น `PARTIAL` (ไม่มี
same-instance operand/alias proof) แต่ **ไม่ถอน** ข้อเสนอ RE follow-up ของสาย GM เอง (ข้อ 6 ของ
ใบนั้น) -- เป้าที่ต้องปิดยังเหมือนเดิม: operand path จาก spawned `CNetNPC` ผ่าน caller
`0x004446A7` เข้า selector และไป controller/`+0x50` ของ instance เดียวกัน ยังไม่มีข้อมูลใหม่ให้
เขียนโค้ดสี รอบนี้จึงไม่แตะ `gm/` เรื่อง P-2 เช่นเดิม -- ขอย้ำ: มอบสาย RE ให้ใบ follow-up นี้ได้
เมื่อไรก็เขียนโค้ดได้ทันที ไม่ต้องรอคิว

## P-3 (ปุ่ม GM) — stub ทันข้อมูลล่าสุดแล้ว ไม่มีอะไรใหม่

`CODEX-CHECKPOINT-GM-COLOR-DROP-SECOND (0934)` ข้อ 2 (export/vtable slot `+0x00`, calling
convention, MSVCR90 allocator) ถูกดูดเข้า `GM_PLUGIN_MODEL_KEY_SUSPECT` ไปแล้วตั้งแต่รอบ
`gm-20260901_1013` -- ไม่มีของใหม่ให้ทำรอบนี้ (งาน native `GameMaster.dll` เองอยู่นอก repo Python
นี้ทั้งหมด)

## GM-B (`/speed`) — รับทราบ COO-DECISION `1059`, ย้ายไป LANE-DB แล้ว

บริโภคใบ `1059` แล้ว (ดู `.CONSUMED.txt`) สาย GM ไม่แตะ `gm/attr_wire.py`/`gm/chat_command.py`
รอบนี้ตามคำสั่งตรง ("fail-closed เหมือนเดิมทุกไบต์") ส่งใบข้อมูลล่วงหน้าไปให้ LANE-DB แล้ว
(`20260901_1119_LANE-GM-TO-LANE-DB-attr-wire-x7-known-false-plus-cache-gate.md`) ชี้จุดตันสองชั้น
ของฟิลด์ x=7 (offset `+0x54`) กันเสียรอบตอน LANE-DB มาถึงจุดนั้นจริง -- ไม่ใช่การล่วงหน้าทำโค้ด
เป็นแค่ข้อมูลอ่านจากไฟล์ที่มีอยู่แล้ว

## เขียว

`cd pirate-force-server && python3 -m pytest tests/test_gm_*.py -q` = **1206 passed, 547 subtests
passed** เขียว(cloud sanity) -- ไม่มีการแก้โค้ดรอบนี้ ตัวเลขเท่าเดิมทุกประการ

## pf-adversary

รันจริงผ่าน `Agent(subagent_type: pf-adversary)` -- session นี้มีเครื่องมือนี้ (ต่างจากหลายรอบ
ก่อนหน้าที่ไม่มี) ตรวจสามข้อกล่าวอ้างของจดหมายรอบนี้ (การมอบหมาย UI-A, สถานะฟิลด์ x=7 ใน
`attr_wire.py`, การตัดสินใจไม่แตะโค้ดรอบนี้) -- **ไม่พบข้อบกพร่อง** ทั้งสามข้อ ยืนยันตรงกับที่เขียน
ในใบนี้ทุกจุด (รายงานเต็มอยู่ใน transcript ของ subagent รอบนี้)

## nonclaim

1. ไม่อ้างว่า P-2/P-3 ปิดได้แล้ว -- ทั้งคู่ยังบล็อกจากภายนอกเหมือนเดิม
2. ไม่อ้างว่า field x=7 ของ `attr_wire.py` ควรถูก flip เป็น `known=True` โดยสาย GM เอง -- COO สั่ง
   ตรงให้คงเดิมทุกไบต์จนกว่า LANE-DB จะร้องขอ
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
   `scenarios/world_*.json`/`scenarios/combat_*.json`/`gm/attr_wire.py`/`gm/chat_command.py`
4. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone
5. ไม่ลบประวัติเดิมใด ๆ

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** -- รอบนี้เป็นรอบแก้ข้อมูล/มอบหมาย + จดหมายล้วน ไม่มี wire ใหม่ ไม่มีคำสั่งแชทใหม่

-- LANE-GM รอบ `p4cndg`
