# QUEUE_STATUS_SNAPSHOT — สแนปช็อตใบ READY + มี `ATTENDED:` + ยังไม่มี `RESULT`

🔴 **ไฟล์นี้ generate สดโดย LANE-K ทุกรอบ ห้ามอ่านเป็นประวัติ — เชื่อเฉพาะฉบับล่าสุด** (ka1-A ใช้ไฟล์นี้จัดรถบัส capture แทนการอ่าน `GAME_TEST_QUEUE.md` 2 MB เอง)
สร้างโดย: LANE-K รอบ `6rj6h1` · เวลา 2026-09-07T01:16+07:00 · แหล่ง: อ่านสดจาก `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` บน `origin/main` (เซสชันนี้มี `git clone`+push จริง) + `tools_bridge/pf_queue_status.py` (315 tickets total, **96 open** — ไม่เปลี่ยนจากรอบก่อน, ตอนนี้มี GT-288 เพิ่มแต่ยังไม่ READY จึงยังไม่กระทบตัวนับ open) — ดู `rounds/K_20260907_0109_6rj6h1_*.md`

🆕 **[K 6rj6h1 01:09] `RE-155` ตอบแล้วโดย LANE-B ภายในเส้นตาย 02:00** (`notes_to_chief/20260907_0021_LANE-B-TO-K-gt-body-RE-155-dummy-row-npc-and-916-sweep.md`, ADDRESSEE: LANE-K) — สปาวน์เนอร์ `name_colour_sweep.py` + ตารางผู้สมัคร (faction/actor_type/skin ทดสอบได้ · relation +0x98/rank ตั้งใจไม่ตัด) + บล็อก `ATTENDED:` (เขียนโดย B เอง) → ตั้งเลข **`GT-288`** NAME-COLOUR-SWEEP-DUMMY-ROW-001 (เนื้อเต็มที่ `tickets/GT-288.md`, สตับ+ATTENDED เต็มที่ `GAME_TEST_QUEUE.md`) · ประกาศในจดหมาย `notes_to_chief/20260907_0116_LANE-K-NUMBERED-GT-288.md` · อัปเดตหัวใบ `RE-155` ใน `CLIENT_RE_QUEUE.md` ให้ชี้มาที่ GT-288 แล้ว (ของเดิมขีดฆ่าเก็บไว้ ไม่ลบ) · consumed จดหมายต้นทางแล้ว
🔴 **`GT-288` ยัง `[PENDING]` ไม่ขึ้นรถบัส capture รอบนี้** — จดหมายต้นทาง (B) เขียนเองว่าสปาวน์เนอร์ยังไม่ต่อสายเข้า `runtime.py`/`app.py` ต้องมี CORE-REQUEST แยกต่อสาย env→dispatch ก่อนจึงบูตขึ้นจริง (เหมือน `pose_trial`/`speed_wire`) — K ไม่ตัดสินความพร้อม รอ B/COO ยืนยันแล้วสั่งพลิกเป็น READY รอบถัดไป (ดูหมวด ง. ด้านล่าง)
🔴 **ใบที่มี RESULT/ปิดแล้วไม่อยู่ในรายการนี้แล้ว**: GT-214 · GT-217 · GT-220 · GT-223 · GT-224 · GT-233 · GT-242 · GT-249 · GT-250 · GT-251 · GT-252 · GT-253 · GT-255 · GT-257 · GT-266 · GT-269 · GT-272 · GT-277 · GT-287 (PENDING, เจ้าของใบยังไม่เปลี่ยนเป็น READY) · GT-288 (PENDING, รอ wiring — ดูข้างบน) · RE-235 · RE-237 · RE-261 · RE-272 · RE-282 (รายละเอียดผล ⇒ หัวใบใน `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` หรือจดหมายรอบ)
**ยัง BLOCKED (ยืนยันแล้วว่าไม่มีจดหมายใหม่เปลี่ยนสถานะรอบนี้)**: `GT-284` WORLD-SCENE-STATE-SURVIVES-RELOGIN-001 ยัง BLOCKED ไม่เข้ารายการบูต · `RE-280`/`RE-283`/`RE-285`/`RE-286` เป็นใบ RE runner (static/client-image) ไม่ใช่ใบ attended-capture ของผู้เทสหน้าจอเกม — ไม่เข้าเกณฑ์สแนปช็อตนี้แม้ `RE-280` จะมีบล็อก `ATTENDED:` แล้วก็ตาม
🆕 **`GT-079` ยังคงสถานะเดิม (`BLOCKED-BY-PLACEHOLDER`) — K ห้ามแตะทั้งใบตาม `COO-DECISION k2217 (1/2)`** จนกว่า chief จะเติม placeholder แล้วส่ง `*-TO-K-*` มาเปลี่ยนสถานะเอง
**รายการ ก./ข./ค. ที่เหลือ (`GT-272`/`GT-274`/`GT-258`/`GT-262`/`GT-279`/`GT-193`/`GT-151`/`GT-178`/`GT-276`/`RE-273`) ตรวจสดผ่าน `pf_queue_status.py` รอบนี้แล้วว่ายัง READY/OPEN ไม่มี RESULT ใหม่ — เนื้อ ATTENDED ไม่เปลี่ยนจากฉบับรอบ `x91eo8r2`/`cm9v9y`/`ec26p6`/`43htls` (ไม่มีจดหมายใหม่แตะใบเหล่านี้รอบนี้ นอกจาก RE-155/GT-288 ข้างบน)

---

## ก. ไร้ธง / env (บูตมาตรฐานหรือ env variable — ไม่ใช่ `--*-scenario`)

1. **`GT-272` (รอบสอง หลัง DB แขน (ข) ขึ้น main ตาม `NOW.md` "รอเครื่องคุณ" ข้อ 2)** — เปิดกระเป๋า → สวม → ช่องอุปกรณ์แสดง → relog → ยังสวม · **ยังไม่ถึงเวลาบูตจนกว่า DB แขน (ข) ขึ้น main** (เส้นตาย `PANYA-ORDER 0156` 23:00)
2. **`GT-281` BASIC-FACTION-EVERY-LOGIN-SCENE-SEA-126-001 (🟢 READY — ชั้น wire PASS R322A พับแล้ว)** — ไร้ธง ไร้ env (FLAGLESS) · ต้องมีบัญชี GM ในตั๋ว relog 126 · `/warp 126` → ปิด client → เปิดใหม่ login → `/warp 2` → ดูชื่อมอน Fighting Fish (เขียว=FAIL) + หลอดสถานะเหนือหัว (มี=FAIL) · **ปลดคอขวด P-2/M3 milestone ชั้นแรก** (`NOW.md` "P-2 ชั้นแรกเจอต้นเหตุ") — เจ้าของใบ/ผู้บริโภคผล = LANE-A · เหลือแค่ชั้นจอ (ชั้น wire ปิดแล้ว)
3. **`GT-274` PRODUCTION-ATTACK-POSE-BY-CLASS-CONFIRMED-001 (ใหม่รอบนี้)** — ไร้ธง แต่ **บังคับผ่านกาน "ก่อนบูต (gate)" ก่อนเสมอ**: `git merge-base --is-ancestor d52cae3 <commit ที่จะบูต>` ต้อง exit 0 + `git grep -n "class_id=selected.class_id" <commit นั้น> -- src/pirateforce_foundation/runtime.py` ต้องเจอ 1 บรรทัด (ใช้ `tools/pf_resolve_green_boot.py` หา `BOOT_COMMIT` ห้ามเดา SHA) · ตี Gladiator แล้วสร้างตัว Paladin ใหม่ตี ถ่ายภาพท่าตี + คัดคอนโซล `POSE_*` สองชุด · เจ้าของใบ/ผู้บริโภคผล = LANE-CS
4. **`GT-258` WARP-SEND-FAILURE-ROLLS-THE-SCENE-BACK-001** — ไร้ธง scenario · GM account · อัดวิดีโอต่อเนื่องตลอด `LOCK_GAME` · precondition: `git grep install_send_outcome_observers -- src/pirateforce_foundation/runtime.py` ต้องเจอบนคอมมิตที่บูต (ไม่เจอ = BLOCKED ข้ามใบ) · เจ้าของใบ/ผู้บริโภคผล = LANE-GM · ต่อท้ายคิว ไม่บล็อกสายใด
5. **`GT-262` STALL-AND-GUILD-STORAGE-ATTENDED-CAPTURE-001** — ไร้ธง (สร้างตัวละครใหม่ปกติ) · หาทางเข้า "แผงขายเอง" (เพดาน 15 นาที/20 คลิก) + "คลังกิลด์" (เพดาน 10 นาที/15 คลิก) · คู่กับ `RE-261` (RE-261 มี CAPTURED บางส่วนแล้วจาก R320 — ปุ่มแถวบนกระเป๋า 7 ปุ่ม NOT REACHED ทั้ง 4 ฟีเจอร์ยัง — ใบนี้ยังต้องหาทางเข้าเอง) · เจ้าของใบ/ผู้บริโภคผล = LANE-UI · ต่อท้ายคิว
6. **`GT-279` GM-PANEL-BUTTON-CAPTURE-001** — ไร้ธง ไม่แตะเซิร์ฟเวอร์ · **ขึ้นรถบัส capture คันเดียวกับ `GT-266`/`GT-269` ได้ (~2 นาทีท้ายรถบัส — `GT-233` เดิมเคยขึ้นรถคันนี้ด้วย ปิดใบแล้วรอบ `cu7c2r` ตัดออก)** · คลิกทีละปุ่ม GMUI ทั้ง 3 หน้า (7/5/5) เว้น 2 วิ/ปุ่ม แล้วเปิด `capture/gm_command_capture/` นับไฟล์ mtime ตรงช่วง · เจ้าของใบ/ผู้บริโภคผล = LANE-GM
7. **`GT-193` SPEED-COMMAND-SPARSE-X7-001 (เฉพาะขั้น 9-10)** — ไร้ธง scenario + `-SecondPasswordMode bypass` · run-copy DB เฉพาะรอบ · **ห้ามตั้ง `PF_SPEED_TRIAL`** (คนละใบกับ `GT-218`) · ขั้น 4-7 ยัง PENDING interface ห้ามเกรด · ก่อนบูตต้องรัน RECHECK ข้อ 6 สดสี่คำสั่งให้ผ่านก่อน
8. **`GT-151` PORT-ROYAL-SEVEN-HOLES-EYES-001 (ค้าง 1/7 จุด)** — ไร้ธง (`/warp 10` หรือ GM staged login) · ใบเก่า (30 ส.ค.) 6 จุดที่เหลือยังไม่ได้เดินตรวจ · ไม่บล็อกใคร
9. **`GT-178` BG0015-HOSTILE-TWELVE-AGGRO-001** — สรุป ATTENDED ในใบสั้นเกินตัดสินชนิดบูตจากตรงนี้ (อ่านเนื้อใบเต็มก่อนบูต) · ใบเก่า
10. **`GT-276` LEARN-SKILL-RESULT-WALKLOCK-ISOLATE-001** — ไร้ธง `--*-scenario` (ส่งเฟรมทีละอันผ่านเครื่องมือ dev) · หาว่าเฟรมไหนใน sweep 6 ขั้นของ `GT-249` ทำให้เดินไม่ได้ · เจ้าของใบ/ผู้บริโภคผล = LANE-CS

## ข. ธง scenario

(ว่างรอบนี้ — `GT-249` ที่เคยอยู่หมวดนี้มี RESULT แล้ว ดูรายการที่หลุดด้านบน)

## ค. STATIC-ON-BRIDGE (ไม่ต้อง `LOCK_GAME` — attended เป็นทางสำรอง)

1. **`RE-273` TRIGGER-ID-TO-LUA-SCRIPT-FILE-MAPPING-001** — ทางแรก static บนสะพาน (ไม่ต้องบูตเกม) · มีบล็อก `ATTENDED:` (5 บรรทัดพอดี) เป็นทางสำรองถ้า static ไม่พอ · เจ้าของใบ = LANE-Q

---

## ง. ใบ NEEDS-ATTENDED-CAPTURE ที่ตกรถ
- `RE-155`/`GT-288` NAME-COLOUR-SWEEP-DUMMY-ROW-001 — **มีบล็อก `ATTENDED:` แล้ว** (เขียนโดยเจ้าของใบ B เอง, ครบ 5 บรรทัด) แต่ตกรถเพราะ **สปาวน์เนอร์ยังไม่ต่อสายเข้า `runtime.py`/`app.py`** (จดหมายต้นทางเขียนเอง) — รอ CORE-REQUEST ต่อสาย env→dispatch จาก B แล้วบูตขึ้นจึงจะขึ้นรถบัส capture ได้จริง

## จ. nonclaims ของสแนปช็อตนี้
- ไม่ได้ไล่ทุกบรรทัดของ `CLIENT_RE_QUEUE.md` แบบ RE ล้วน (สแกนเฉพาะแท็ก `NEEDS-ATTENDED-CAPTURE`) — RE เฉพาะที่ไม่มีแท็กนี้ไม่ถูกนับ (ปกติไม่ต้อง capture)
- ไม่ได้ตัดสินว่าใบไหน "ควรบูต" ก่อน — ลำดับ (ก)/(ข)/(ค) และเลขในวงเล็บเป็นการเรียงตามกติกา ไม่ใช่คำสั่งบูต
- ใบที่มีบล็อก `ATTENDED:` มากกว่าหนึ่งก้อนในตัวเอง (เช่นใบ multi-step) แสดงเฉพาะก้อนแรกที่เจอ — อ่านเนื้อใบเต็มก่อนบูตเสมอ
- `GT-274` ไม่ได้ตรวจกาน "ก่อนบูต (gate)" ให้ล่วงหน้าจากรอบนี้ (ไม่มีเครื่องมือรัน git ต่อ pirate-force-server ในเซสชันนี้) — ผู้บูตต้องรันเองก่อนเสมอตามที่หัวใบสั่ง
- รายการ ก./ข./ค. ที่เหลือ (นอกจาก GT-233/GT-281 ที่ตรวจสดรอบนี้) ยังยกมาจากฉบับรอบ `x91eo8r2`/`cm9v9y` โดยยืนยันผ่าน `pf_queue_status.py` ว่าสถานะเปิด/READY ไม่เปลี่ยน — ไม่ได้เปิดอ่านเนื้อ ATTENDED ทีละใบซ้ำทั้งหมดรอบนี้ (ไม่มีจดหมายใหม่แตะใบเหล่านี้)
