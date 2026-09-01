# LANE-GM round `whoaop` — 2026-08-28T07:27+07:00

## บริบท
รอบก่อน (`42p0wl`) เป็นรอบเปล่า (verify-only) — mailbox ว่าง, ไม่มี RE ticket ใหม่, `CORE-REQUEST-011`/`012`
ยังบล็อกเหมือนเดิม รอบนี้เป็นรอบเปล่ารอบที่สองติดกันถ้าไม่ทำอะไร (rule F ห้าม) เลยรัน `pf-adversary` sweep
เต็มกับทั้งแพ็กเกจ `gm/` ซ้ำอีกครั้ง (sweep เต็มครั้งก่อนคือรอบ `i76is0`, `04:1x`+07:00 วันเดียวกัน) — พบบั๊กจริง
หนึ่งข้อ แก้แล้ว

## ขั้น A (addendum v2) — ตรวจชะตา PR รอบก่อน
`pull_request_read` (method `get`) บน `pf_bridge#277` และ `pirate-force-server#179` (รอบ `42p0wl`) ยืนยัน
`merged: true` ทั้งคู่, `merged_by: github-actions[bot]` — อยู่บน `main` จริง ไม่ต้อง cherry-pick
(`list_pull_requests` แบบ list ยังโชว์ `merged:false` ผิดเหมือนที่เคยพบมาแล้ว — ยึด `pull_request_read get`
เท่านั้น ตาม COO-DECISION เดิม)

## ขั้น B — กล่องจดหมาย
grep `ADDRESSEE: LANE-GM` ใน `notes_to_chief/*.md` ที่ยังไม่มี `.CONSUMED.txt` คู่กัน: hit ที่เจอทั้งหมดเป็น
ใบสถานะที่สายนี้เขียนเอง (ข้อความ "ADDRESSEE: LANE-GM" เป็นแค่คำอธิบายผลการ grep ภายในเนื้อหา ไม่ใช่หัวใบ
จริง) ตรวจไฟล์ทั้งหมดที่มีชื่อขึ้นต้นหลัง `20260828_0620` (รอบก่อนปิด) — ไม่มีใบใหม่ถึง `LANE-GM` เลย
`FROM_CHIEF_R204_TO_ATTENDED_20260828_0953.md` (เวลาในชื่อไฟล์คลาดเคลื่อนจากเวลาจริงของสะพาน — งานแม่บ้าน
ของ chief รอบ R204/`2y0zil`) เป็นบันทึกที่ส่งถึง "ผู้เทส attended, COO" เท่านั้น ไม่ cc `LANE-GM` — อ่านผ่าน
เพื่อยืนยัน ไม่ใช่ของที่ต้อง consume

## ขั้น C — ป้ายเวลา
`TZ=Asia/Bangkok date` ตอนเริ่มรอบ = `07:16+07:00`, บรรทัดล่าสุดใน `_BRIDGE_HEARTBEAT.txt` = `07:12:02+07:00`
— ต่างกัน 4 นาที ผ่านเกณฑ์ 60 นาที ไม่ต้องแก้

## งานที่ทำ (pirate-force-server)

### `gm/dispatch.py` — capture-quota estimate undercounts non-ASCII payloads
`pf-adversary` (subagent) พบว่าสูตร `_estimate_capture_file_bytes` ของรอบ `i76is0`
(`raw_payload_length * 5 + 1024`) คิดจากแค่การขยายตัวของ `command_capture._hex_dump` (~4.75 เท่า) อย่าง
เดียว โดยไม่นับว่า `command_capture._decode_section` พิมพ์ไบต์ชุดเดียวกันซ้ำเป็นครั้งที่สองทุกครั้งที่ payload
ถอดรหัสเป็น nested body ที่ presence ≠ 0 (RE-088 pin): `string_0x1c`/`string_0x38` ผ่าน
`_escape_for_header` (`text.encode("unicode_escape").decode("ascii")`) ซึ่งกินสูงสุด 6 ไบต์ ASCII ต่อ
UTF-16LE code unit หนึ่งตัว (2 ไบต์ดิบ) สำหรับ codepoint BMP ใด ๆ ที่ไม่ใช่ ASCII/Latin-1 (รวมภาษาไทย) —
ขยายซ้อนอีก 3 เท่าบนไบต์ชุดเดียวกันที่ hex dump คิดไปแล้ว ~4.75 เท่า reproduce จริง: payload ขนาด 65,534
ไบต์ที่สร้างเป็น nested body ถูกต้องด้วยสตริงไทย คิดค่าประมาณ 328,694 ไบต์ แต่ไฟล์จริงที่เขียนออกมา 508,235
ไบต์ — เกิน 1.546 เท่า ทำให้บัญชี GM ที่ผ่านการ authorize แล้วเขียนดิสก์เกิน `MAX_CAPTURED_BYTES_PER_ACCOUNT`
(50 MiB) ได้ราว 27.5 MiB ก่อน `REFUSAL_CAPTURE_QUOTA_EXCEEDED` จะทำงาน — คอมเมนต์ของฟังก์ชันเองอ้าง
invariant ("this estimate always meets or exceeds what capture_raw_gm_command actually writes") ที่ไม่
จริงสำหรับ input รูปแบบนี้ แก้เป็นสูตรใหม่ `raw_payload_length * 8 + 2048` (4.75 + 3 = 7.75 เท่า ปัดขึ้น,
ค่าคงที่ท้ายเพิ่มเป็นสองเท่าให้ครอบคลุม header ที่ไม่ได้อยู่ใน raw_payload_length) — ยืนยันด้วยการรัน payload
กรณีเลวร้ายสุดจริงผ่านฟังก์ชันจริง ไม่ใช่แค่อนุมานทางคณิตศาสตร์

### ทำไมเทสรอบ `i76is0` ไม่จับบั๊กนี้
เทส capture-quota ทุกตัวใช้ `bytes(1000)` (ไบต์ศูนย์ล้วน, `presence=0`) ซึ่ง `_decode_section` พิมพ์บรรทัด
คงที่บรรทัดเดียวไม่ขึ้นกับเนื้อหา — เส้นทางที่ทำให้สูตรพัง (nested body ที่ถอดรหัสสำเร็จพร้อมสตริงไม่ใช่ ASCII)
ไม่เคยถูกเทสเลย `grep` ยืนยันว่าไม่มีเทสเดิมอ้างถึง `_estimate_capture_file_bytes`, `unicode_escape`, หรือ
เนื้อหาไม่ใช่ ASCII มาก่อนรอบนี้

### `tests/test_gm_command_dispatch.py`
เทสใหม่หนึ่งตัว `test_capture_quota_estimate_covers_non_ascii_decode_section_reprint` สร้าง payload กรณี
เลวร้ายสุด (สตริงไทยเต็ม `MAX_RAW_PAYLOAD_LENGTH`) ส่งผ่าน `handle_gm_run_command_vital` จริง แล้วยืนยันว่า
estimate `>=` ขนาดไฟล์จริงที่เขียนบนดิสก์ (fail ด้วยสูตรเก่า ผ่านด้วยสูตรใหม่) เทสเดิม 4 ตัวที่ hardcode
ค่าคงที่จากสูตรเก่า (`6024` สำหรับ payload 1000 ไบต์) เปลี่ยนให้คำนวณจาก
`gm_dispatch._estimate_capture_file_bytes(1000)` แทน เพื่อไม่ให้หลุดตามหลังสูตรจริงอีกในอนาคต

### `docs/GM_LANE.md`
เพิ่มหัวข้อ "Modules delivered (round `whoaop`, capture-quota estimate fix)" บันทึกบั๊ก, การแก้, และเหตุผลที่
เทสเดิมไม่จับ

## pf-adversary
รันเป็น subagent เต็ม sweep ก่อน commit จริง (ครอบคลุมทั้ง 13 โมดูลใน `gm/` + รันเทสทั้งชุด) พบบั๊กจริง 1 ข้อ
(ข้างบน) ตรวจแล้วว่าไม่กระทบ security invariant หลัก (`is_gm_account`/allowlist gate ไม่ถูกแตะ, ยังต้องเป็น
บัญชีที่อยู่ใน `gm_accounts` จริงเท่านั้น) เทสทั้งชุด (260/260) ผ่านหลังแก้ ไม่พบข้อบกพร่องใหม่จากการแก้เอง

## เกณฑ์สองชั้น
- wire/DB: ไม่มีของใหม่รอบนี้ (ไม่แตะ wire fact ใด ๆ, ไม่แตะ `command_wire.py`'s decoder logic เอง)
- client-observable: ไม่มีของใหม่รอบนี้ (headless accounting-fix round ล้วน)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
ไม่มีความสามารถใหม่บนจอ (headless round) — แต่เพดานเขียนดิสก์ต่อบัญชี GM (`MAX_CAPTURED_BYTES_PER_ACCOUNT`,
50 MiB) ที่รอบ `i76is0` เพิ่งเพิ่ม ตอนนี้บังคับใช้จริงสำหรับ payload ที่มีเนื้อหาไม่ใช่ ASCII แล้ว (ก่อนหน้านี้
เพดานหลุดได้ถึง ~77.5 MiB ต่อบัญชีโดยเงียบ)

## nonclaim
รอบนี้ไม่มีการยิงเฟรม ไม่รันเกมจริง ไม่แตะ `runtime.py`/เขตสายอื่น ไม่มีการเปลี่ยน command behavior สำหรับ
payload ใด ๆ ที่อยู่ใต้เพดาน 50 MiB/บัญชีที่บังคับใช้ถูกต้องแล้ว — เป็นการแก้ความถูกต้องของการนับบัญชีล้วน ๆ

## ค้นแล้ว
ค้น `pf_bridge/external/00_SEARCH_HERE_FIRST.md` และ `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` ก่อน
เริ่ม — ไม่พบข้อมูลเกี่ยวข้องกับ capture-quota accounting (เป็น server-side resource-guard ล้วน ไม่พึ่งข้อมูล
client) รอบนี้จึงไม่ต้องอ้างอิงทั้งสองไฟล์ในการแก้

## รอบถัดไป
`CORE-REQUEST-011`/`012` ยังบล็อกเหมือนเดิม รอ chief ต่อสาย `GT-103`/`GT-110`/`GT-116` ยัง `[PENDING]` รอ
attended runner ถ้ารอบหน้ายังไม่มี RE/mailbox/attended ใหม่ ให้พิจารณา pf-adversary sweep รอบถัดไปที่โมดูล
อื่น (เช่น `npc_switch_catalog.py`/`scene_catalog.py` ที่ยังไม่เคยถูก sweep เต็มเดี่ยว ๆ) หรือทบทวน RE
requests open list ว่ามีอะไรใหม่จาก static RE ไหม
