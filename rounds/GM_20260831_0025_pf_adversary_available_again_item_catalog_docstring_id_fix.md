# รอบ `aejgap` (สาย GM) -- 2026-08-31T00:25+07:00

## 1. round-lock (ADDENDUM v2 ข้อ A + กฎรอบเดิม)

- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11388 ไบต์ · ยืนยันขั้นแรก)
- ต้นรอบไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo (`search_pull_requests(is:open, in:title [LANE-GM])`:
  ทั้งสอง repo ว่างเปล่า) ⇒ ยึดล็อกด้วย draft: pf_bridge **#544** · pirate-force-server **#345**
- ชะตารอบก่อน (`xq4vrn`) วัดด้วย `pull_request_read(method="get")` ตรง ไม่เชื่อจดหมาย:
  - pf_bridge `#541`: `merged: true`, `merged_at: 2026-08-30T16:45:43Z`
  - pirate-force-server `#342`: `merged: true`, `merged_at: 2026-08-30T16:54:00Z`
  ⇒ อยู่บน `main` ทั้งคู่ ไม่มีอะไรต้องกู้
- heartbeat: `_BRIDGE_HEARTBEAT.txt` ล่าสุด `00:02:03+07:00` · ต้นรอบตรวจ `00:16` ⇒ ห่าง ~14 นาที ผ่านเกณฑ์ 60

## 2. กล่องจดหมาย (ADDENDUM v2 ข้อ B)

grep `ADDRESSEE: LANE-GM` (รูปแบบ `ADDRESSEE:` ตรง ๆ และรูปแบบหัวจดหมาย `[ถึง: สาย GM | ADDRESSEE: ...]`)
บนไฟล์ที่ยังไม่มี `.CONSUMED.txt` คู่กัน (ทั้งที่ค้างอยู่และในนามสกุลที่ `consumed/`): **ศูนย์ใบ**

สามใบที่ cc สายนี้คืนนี้ (`20260830_1823_KA1A-CORRECTION-...`, `20260830_2151_KA1A-RECHECK-...`,
`20260830_2356_PANYA-DECISION-one-addressee-per-letter-plus-claim-before-you-start.md`) และใบธุรการ
`20260831_0011_KA1A-ADDENDUM-...` ล้วนจ่าหน้าถึง chief/COO เป็นหลัก ไม่มีข้อไหนสั่งสายนี้โดยตรง (อ่านครบ
ทุกใบแล้ว) กติกาใหม่ที่เกี่ยวข้อง (CLAIM-before-work, ADDRESSEE เดียวต่อใบ) บันทึกรับทราบไว้ที่นี่: รอบนี้
ไม่มีใบเปิดกว้างเกินหนึ่งสายให้ต้องจองในเขตสายนี้ ไม่ต้องทำอะไรเพิ่ม

## 3. backlog ในเขต `gm/` -- ยังบล็อกบน chief/COO เหมือนรอบก่อน

- `CORE-REQUEST-GM-042` เต็ม (state store + จุดเขียน + ตัวกรอง roster): chief ตอบ (`20260830_2100`) ว่ายัง
  ไม่ทำ เพราะต้องอ่าน `mob_ledger_admission.py`/`require_ledger_for_recompose` ให้ครบก่อน -- เป็นเขตของ
  chief (`runtime.py`/`mob_scene_recompose.py`) ไม่ใช่เขต `gm/`
- `GT-128` (chat-warp วัดบนจอ): ยัง `STILL BLOCKED` บน "COO-held gate" ตาม chief R243 -- ไม่ใช่ของที่แก้ใน
  เขต `gm/` ได้เอง
- `GT-127` ปิดแล้ว (`CLOSED PASS`, รอบ `noixtz`) -- ไม่มีอะไรเหลือ

## 4. ตัวเลือกกฎข้อ F ที่ตรวจก่อนตัดสินใจ

(ก) backlog pre-approved ในเขตตัวเอง -- ไม่มี ทั้งสามจุดบล็อกบน chief/COO
(ข) ใบ RE/STATIC ที่ตอบได้จากซอร์ส -- ไม่มีใบ RE เปิดที่เป็นของเขต GM
(ค) เขียน/ปรับใบเทสในคิว -- `GAME_TEST_QUEUE.md` ไม่อยู่ในเขตเขียนของสายนี้
(ง) technical debt ที่ `pf-adversary` เคยชี้ -- **ตัวเลือกนี้ใช้ได้จริงรอบนี้**: `pf-adversary` subagent
  เรียกได้เป็นครั้งแรกในห้ารอบติดต่อกัน (`opr2xd`/`dao2gd`/`xq4vrn` ก่อนหน้าไม่มีให้เรียก) ⇒ ให้ตรวจ `gm/`
  ทั้งโมดูลหาหนี้สินทางเทคนิคที่ค้างจากการไม่มีมันมาสี่รอบ

## 5. สิ่งที่ `pf-adversary` พบ + สิ่งที่แก้

พบ off-by-one จริงใน docstring ของ `item_catalog.py`: ย่อหน้า "IMPORTANT finding" อ้าง "id 6 is 'Earth
Element' (misc) but 'Fruit Wine Jar' (consumable)" -- ยืนยันซ้ำเองตรงกับ `gm/data/*.tsv` ด้วย `awk`:
id 6 **ไม่มีอยู่ในตาราง misc เลย** (มีแค่ consumable="Fruit Wine Jar" / quest="Lucky Canine" -- ชนกัน
consumable/quest ไม่ใช่ misc/consumable) ส่วน "Earth Element" ตัวจริงคือ **id 7** ของ misc ซึ่งชนกับ
consumable id 7 = "Fruit Wine Jar" พอดี (สามทางจริง ๆ ชนกับ quest id 7 = "Princess Sick Leave" ด้วย) --
สรุปคือพิมพ์เลข id ผิดหนึ่งตัว ไม่ใช่ชื่อไอเทมผิด (ตัวอย่าง id 1 ในย่อหน้าเดียวกันตรวจแล้วถูกต้องอยู่แล้ว)

ผลกระทบ: ไม่มีโค้ด production อ่าน docstring เป็นข้อมูล แต่ย่อหน้านี้เป็นจุดเดียวที่เตือนคนต่อไปที่จะ wire
`item <id> <n>` ให้แจกไอเทมจริงเรื่อง id ชนข้ามตาราง -- ตัวอย่างผิดตรงนี้จะชักนำให้คนถัดไปเดาหมวด/ชื่อผิด
ตอนตัดสินใจจริง ตรงกับสิ่งที่ย่อหน้านี้เขียนมาเพื่อป้องกันพอดี

แก้: (1) `item_catalog.py` เปลี่ยน `id 6` → `id 7` หนึ่งจุด (2) เพิ่ม
`tests/test_gm_item_catalog.py::test_module_docstrings_misc_consumable_example_id_matches_the_data` pin
ตัวอย่างของ docstring กับข้อมูลจริง ตอบคำถามที่ `pf-adversary` ทิ้งไว้ (มีกลไกผูก docstring กับข้อมูลจริง
ไหม) -- มีแล้วหนึ่งเทส ถ้า data refresh รอบหน้าย้ายชื่อออกจาก id 7 เทสนี้แดงทันที mutation-kill ยืนยันด้วย
มือ: เปลี่ยนชื่อฟังก์ชัน `item_category` ชั่วคราวให้เรียกไม่ได้ เห็นเทสนี้ (และอีก 6 เทสในไฟล์เดียวกัน) แดง
จริง คืนของเดิม รันเขียวก่อนคอมมิต

`pytest tests/test_gm_item_catalog.py -q`: 14 passed (+1), 12 subtests
`pytest tests/test_gm_*.py -q`: 1054 passed (+1), 469 subtests, 0 failed
`pytest tests/ -q` เต็ม: **5596 passed** (+1), 327 skipped, 9729 subtests passed, 0 failed (cloud sanity,
`origin/main` ต้นรอบ)

จุดอื่นที่ `pf-adversary` ตรวจแล้วไม่พบข้อบกพร่องจริง (บันทึกกันขุดซ้ำ): call-site ordering/shape guard ของ
`_note_item_catalog_diagnostic`, `scene_catalog.py` blank-row handling, `dispatch.py` rate-limiter/
capture-quota locking, `accounts.py`, `npc_switch_catalog.py`, `login_scene_override.py`,
`warp_executor.py`/`teleport_wire.py`/`warp_target_record.py` round-trip encode/decode -- ข้อสังเกตอ่อน
หนึ่งจุด (`chat_command.py`'s `_command_log_quota_allows` ไม่มี lock รอบ stat-then-append) ผลกระทบเล็ก
มาก ไม่ยืนยันเป็นบั๊กจริง บันทึกไว้ให้รอบหน้าอาจดูซ้ำ

รายละเอียดเต็มของบันทึกรอบ: `pirate-force-server` `docs/GM_LANE.md` หัวข้อ "รอบ `aejgap`"

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- แก้ docstring + เทสเท่านั้น ไม่มีบรรทัดใดของคำสั่ง GM เปลี่ยนพฤติกรรมที่ผู้เทสหน้าจอเห็น

## nonclaim

grep/read ซอร์สที่ commit แล้ว, `pytest` headless เต็มชุด (5596 passed, 0 failed), `pf-adversary` subagent
(อ่าน `gm/` ทั้งโมดูลในเวิร์กทรีแยก ไม่แตะ checkout จริง), และ GitHub API เป็นหลักฐานเดียวของรอบนี้ ไม่มีการ
เปิด client ไม่มีการใช้ GM ข้ามขั้นทดสอบใด ๆ ไม่มีการให้สถานะ GM กับใคร ไม่มีการแตะเขตสาย A/สาย B/
canonical DB ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`

— สาย GM รอบ `aejgap`
