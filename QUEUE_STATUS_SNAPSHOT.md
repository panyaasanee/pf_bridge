# QUEUE_STATUS_SNAPSHOT — สแนปช็อตใบ READY + มี `ATTENDED:` + ยังไม่มี `RESULT`

🔴 **ไฟล์นี้ generate สดโดย LANE-K ทุกรอบ ห้ามอ่านเป็นประวัติ — เชื่อเฉพาะฉบับล่าสุด** (ka1-A ใช้ไฟล์นี้จัดรถบัส capture แทนการอ่าน `GAME_TEST_QUEUE.md` 2 MB เอง)
สร้างโดย: LANE-K รอบ `2a32q2` · เวลา 2026-09-07T02:17+07:00 · แหล่ง: อ่านสดจาก `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` บน `origin/main` (เซสชันนี้มี `git clone`+push จริง) + `tools_bridge/pf_queue_status.py` (316 tickets total, **95 open** ตามตัวนับเครื่องมือ — เครื่องมือยังนับ `GT-279`/`GT-178` เป็น READY เพราะ regex ไม่รู้จักสถานะ 🟡/หัวใบรูปแบบพิเศษ แต่ทั้งสองใบมี `RESULT:` แล้วจริง จึงตัดออกจากรายการนี้ตามกฎ "ใบที่มี RESULT ห้ามอยู่ในสแนปช็อต" — ไม่เชื่อตัวนับเครื่องมือกรณีนี้) — ดู `rounds/K_20260907_0209_2a32q2_*.md`

🆕 **[K `2a32q2` 02:12] พับผล R322B + R322C ครบสี่ใบ**: `GT-281` PASS ทั้งสองชั้น (sea login ships `basic_faction=1` · มอนไม่เขียว ตีตายได้ · หลอดฟ้า/BoatHealth แยกเป็นใบสร้างใหม่ A/DB) → **ปลดคอขวด P-2/M3 ชั้นแรกจริงแล้ว** · `GT-279` ผลสองชั้นแยกทาง (client PASS — ปุ่ม "ปฏิบัติ" ส่ง 0x51E9 จริง 3 เฟรม · server NEGATIVE — capture hook ไม่เขียนไฟล์) · `GT-274` PASS (Gladiator ดาบ 280 · Paladin กระบอง 284 · arm ii รอ `GT-272`) · `GT-178` NEGATIVE-MEASURED (ฉาก 14 ไม่มี `MOB_AI_TICK_LIVE` เลย — register ทำไว้แค่ฉาก 1/2 · แม้ tick เดินก็ `attack_undeliverable` — ใบสร้างเสนอของ B ต่อ M4) — ผลเต็มอยู่ที่หัวใบ + `### result:`/`### result (ผู้เทสกรอก)` ใน `GAME_TEST_QUEUE.md` แล้ว ผลทั้งสี่ยกคำต่อคำจาก `notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-*.md` และ `notes_to_chief/20260907_0158_KA1A-R322C-RESULTS-*.md` (ทั้งคู่ `.LANEK-FOLDED.txt` แล้ว)
🆕 **[K `2a32q2` 02:12] `GT-288` addendum ต่อท้ายแล้ว** — จดหมาย `notes_to_chief/20260907_0157_LANE-B-TO-K-gt288-addendum-table-key-candidate.md` (LANE-B, ตอบคำสั่ง PANYA `0039`/COO `0043`): เติมผู้สมัครข้อที่หก "key ที่ client ใช้เปิดตาราง MOBS" (ชุด env `=3`, K-MATCH/K-IDONLY/K-SKINONLY) + แก้บรรทัด 5 ของ `ATTENDED:` ให้ครอบทั้งสามชุด — ต่อท้ายที่ `tickets/GT-288.md` คำต่อคำ ไม่แตะของเดิม · **สถานะยังคง `[PENDING]` เหมือนเดิม** (สปาวน์เนอร์ยังไม่ต่อสายเข้า `runtime.py`/`app.py` — ชุด `=3` เป็น SPEC ONLY ยังไม่มีโค้ดด้วย) — ยังไม่ขึ้นรถบัสรอบนี้ (ดูหมวด ง.)
🔴 **ใบที่มี RESULT/ปิดแล้วไม่อยู่ในรายการนี้แล้ว**: GT-178 · GT-214 · GT-217 · GT-220 · GT-223 · GT-224 · GT-233 · GT-242 · GT-249 · GT-250 · GT-251 · GT-252 · GT-253 · GT-255 · GT-257 · GT-266 · GT-269 · GT-272 · GT-274 · GT-277 · GT-279 · GT-281 · GT-287 (PENDING, เจ้าของใบยังไม่เปลี่ยนเป็น READY) · GT-288 (PENDING, รอ wiring — ดูข้างบน) · RE-235 · RE-237 · RE-261 · RE-272 · RE-282 (รายละเอียดผล ⇒ หัวใบใน `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` หรือจดหมายรอบ)
**ยัง BLOCKED (ยืนยันแล้วว่าไม่มีจดหมายใหม่เปลี่ยนสถานะรอบนี้)**: `GT-284` WORLD-SCENE-STATE-SURVIVES-RELOGIN-001 ยัง BLOCKED ไม่เข้ารายการบูต · `RE-280`/`RE-283`/`RE-285`/`RE-286` เป็นใบ RE runner (static/client-image) ไม่ใช่ใบ attended-capture ของผู้เทสหน้าจอเกม — ไม่เข้าเกณฑ์สแนปช็อตนี้แม้ `RE-280` จะมีบล็อก `ATTENDED:` แล้วก็ตาม
🆕 **`GT-079` ยังคงสถานะเดิม (`BLOCKED-BY-PLACEHOLDER`) — K ห้ามแตะทั้งใบตาม `COO-DECISION k2217 (1/2)`** จนกว่า chief จะเติม placeholder แล้วส่ง `*-TO-K-*` มาเปลี่ยนสถานะเอง
**รายการ ก./ข./ค. ที่เหลือ (`GT-272`/`GT-258`/`GT-262`/`GT-193`/`GT-151`/`GT-276`/`RE-273`) ตรวจสดผ่าน `pf_queue_status.py` รอบนี้แล้วว่ายัง READY/OPEN ไม่มี RESULT ใหม่ — เนื้อ ATTENDED ไม่เปลี่ยนจากฉบับรอบ `x91eo8r2`/`cm9v9y`/`ec26p6`/`43htls`/`6rj6h1` (ไม่มีจดหมายใหม่แตะใบเหล่านี้รอบนี้ นอกจากสี่ใบพับผลข้างบน)

---

## ก. ไร้ธง / env (บูตมาตรฐานหรือ env variable — ไม่ใช่ `--*-scenario`)

1. **`GT-272` (รอบสอง หลัง DB แขน (ข) ขึ้น main ตาม `NOW.md` "รอเครื่องคุณ" ข้อ 2)** — เปิดกระเป๋า → สวม → ช่องอุปกรณ์แสดง → relog → ยังสวม · **ยังไม่ถึงเวลาบูตจนกว่า DB แขน (ข) ขึ้น main** (เส้นตาย `PANYA-ORDER 0156` 23:00)
2. **`GT-258` WARP-SEND-FAILURE-ROLLS-THE-SCENE-BACK-001** — ไร้ธง scenario · GM account · อัดวิดีโอต่อเนื่องตลอด `LOCK_GAME` · precondition: `git grep install_send_outcome_observers -- src/pirateforce_foundation/runtime.py` ต้องเจอบนคอมมิตที่บูต (ไม่เจอ = BLOCKED ข้ามใบ) · เจ้าของใบ/ผู้บริโภคผล = LANE-GM · ต่อท้ายคิว ไม่บล็อกสายใด
3. **`GT-262` STALL-AND-GUILD-STORAGE-ATTENDED-CAPTURE-001** — ไร้ธง (สร้างตัวละครใหม่ปกติ) · หาทางเข้า "แผงขายเอง" (เพดาน 15 นาที/20 คลิก) + "คลังกิลด์" (เพดาน 10 นาที/15 คลิก) · คู่กับ `RE-261` (RE-261 มี CAPTURED บางส่วนแล้วจาก R320 — ปุ่มแถวบนกระเป๋า 7 ปุ่ม NOT REACHED ทั้ง 4 ฟีเจอร์ยัง — ใบนี้ยังต้องหาทางเข้าเอง) · เจ้าของใบ/ผู้บริโภคผล = LANE-UI · ต่อท้ายคิว
4. **`GT-193` SPEED-COMMAND-SPARSE-X7-001 (เฉพาะขั้น 9-10)** — ไร้ธง scenario + `-SecondPasswordMode bypass` · run-copy DB เฉพาะรอบ · **ห้ามตั้ง `PF_SPEED_TRIAL`** (คนละใบกับ `GT-218`) · ขั้น 4-7 ยัง PENDING interface ห้ามเกรด · ก่อนบูตต้องรัน RECHECK ข้อ 6 สดสี่คำสั่งให้ผ่านก่อน
5. **`GT-151` PORT-ROYAL-SEVEN-HOLES-EYES-001 (ค้าง 1/7 จุด)** — ไร้ธง (`/warp 10` หรือ GM staged login) · ใบเก่า (30 ส.ค.) 6 จุดที่เหลือยังไม่ได้เดินตรวจ · ไม่บล็อกใคร
6. **`GT-276` LEARN-SKILL-RESULT-WALKLOCK-ISOLATE-001** — ไร้ธง `--*-scenario` (ส่งเฟรมทีละอันผ่านเครื่องมือ dev) · หาว่าเฟรมไหนใน sweep 6 ขั้นของ `GT-249` ทำให้เดินไม่ได้ · เจ้าของใบ/ผู้บริโภคผล = LANE-CS

## ข. ธง scenario

(ว่างรอบนี้ — `GT-249` ที่เคยอยู่หมวดนี้มี RESULT แล้ว ดูรายการที่หลุดด้านบน)

## ค. STATIC-ON-BRIDGE (ไม่ต้อง `LOCK_GAME` — attended เป็นทางสำรอง)

1. **`RE-273` TRIGGER-ID-TO-LUA-SCRIPT-FILE-MAPPING-001** — ทางแรก static บนสะพาน (ไม่ต้องบูตเกม) · มีบล็อก `ATTENDED:` (5 บรรทัดพอดี) เป็นทางสำรองถ้า static ไม่พอ · เจ้าของใบ = LANE-Q

---

## ง. ใบ NEEDS-ATTENDED-CAPTURE ที่ตกรถ
- `RE-155`/`GT-288` NAME-COLOUR-SWEEP-DUMMY-ROW-001 — **มีบล็อก `ATTENDED:` แล้ว** (เขียนโดยเจ้าของใบ B เอง, ครบ 5 บรรทัด, addendum ชุด `=3` ต่อท้ายรอบนี้) แต่ตกรถเพราะ **สปาวน์เนอร์ยังไม่ต่อสายเข้า `runtime.py`/`app.py`** (จดหมายต้นทางเขียนเอง) และชุด `=3` เป็น SPEC ONLY ยังไม่มีโค้ด — รอ CORE-REQUEST ต่อสาย env→dispatch จาก B แล้วบูตขึ้นจึงจะขึ้นรถบัส capture ได้จริง

## จ. nonclaims ของสแนปช็อตนี้
- ไม่ได้ไล่ทุกบรรทัดของ `CLIENT_RE_QUEUE.md` แบบ RE ล้วน (สแกนเฉพาะแท็ก `NEEDS-ATTENDED-CAPTURE`) — RE เฉพาะที่ไม่มีแท็กนี้ไม่ถูกนับ (ปกติไม่ต้อง capture)
- ไม่ได้ตัดสินว่าใบไหน "ควรบูต" ก่อน — ลำดับ (ก)/(ข)/(ค) และเลขในวงเล็บเป็นการเรียงตามกติกา ไม่ใช่คำสั่งบูต
- ใบที่มีบล็อก `ATTENDED:` มากกว่าหนึ่งก้อนในตัวเอง (เช่นใบ multi-step) แสดงเฉพาะก้อนแรกที่เจอ — อ่านเนื้อใบเต็มก่อนบูตเสมอ
- `GT-274` ปิดแล้วรอบนี้ (PASS) จึงตัดข้อสังเกตเดิมเรื่องกาน "ก่อนบูต (gate)" ที่ยังไม่ตรวจล่วงหน้าออก — ไม่เกี่ยวแล้ว
- รายการ ก./ค. ที่เหลือ ยังยกมาจากฉบับรอบก่อนหน้าโดยยืนยันผ่าน `pf_queue_status.py` ว่าสถานะเปิด/READY ไม่เปลี่ยน — ไม่ได้เปิดอ่านเนื้อ ATTENDED ทีละใบซ้ำทั้งหมดรอบนี้ (ไม่มีจดหมายใหม่แตะใบเหล่านี้)
- ไฟล์คิวหลักยังเกินเพดานมาก (`GAME_TEST_QUEUE.md` ~1.41 MB > 300 KB) — สแนปช็อตนี้ไม่ได้แก้เรื่องนั้น ดูไฟล์รอบ `2a32q2` สำหรับตัวเลขจริงและเหตุผลที่ยังไม่ archive รอบนี้
