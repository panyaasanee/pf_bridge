# QUEUE_STATUS_SNAPSHOT — สแนปช็อตใบ READY + มี `ATTENDED:` + ยังไม่มี `RESULT`

🔴 **ไฟล์นี้ generate สดโดย LANE-K ทุกรอบ ห้ามอ่านเป็นประวัติ — เชื่อเฉพาะฉบับล่าสุด** (ka1-A ใช้ไฟล์นี้จัดรถบัส capture แทนการอ่าน `GAME_TEST_QUEUE.md` 2 MB เอง)
สร้างโดย: LANE-K รอบ `cu7c2r` · เวลา 2026-09-06T20:11+07:00 · แหล่ง: อ่านสดจาก `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` บน `origin/main` ผ่าน git clone จริง (ไม่ใช่ MCP ทีละไฟล์ — ทาง (ค) ตาม `COO-DECISION 20260906_1955` ข้อ 2) + `tools_bridge/pf_queue_status.py` (95 open หลังพับ `GT-233`) — ดู `rounds/K_20260906_2011_cu7c2r_*.md`

🆕 **[K cu7c2r 20:11] เครื่องมือกลับมาใช้ได้แล้ว**: รอบนี้มี git clone จริงทั้งสองรีโป (`COO-DECISION 20260906_1955` ข้อ 2 ยืนยัน "ทาง (ค)" — session ที่ไม่มี clone ให้จบรอบว่างแทน ไม่ใช่อ้อมด้วย MCP) แก้บล็อกเครื่องมือของรอบ `n27xtq` ได้เต็มที่
🆕 **[K cu7c2r 20:11] `GT-233` พับปิดแล้ว = CLOSED · NEGATIVE-MEASURED-v3** (R322A, `OBSERVER_CONFIRMED 2026-09-06T18:57+07:00`, จดหมาย `notes_to_chief/20260906_1909_KA1A-R322A-RESULTS-*.md`, `.LANEK-FOLDED.txt` วางแล้ว) — เงียบทั้งเกาะ 2/3 แม้ `confirmed=126` และ key ชี้แถวจริงทั้งสองคอลัมน์ · ปิดถาวรตาม `PANYA-ORDER 20260906_1910` ข้อ 2.1 (**ห้ามบูต v4 ซ้ำ ห้ามตั้งใบ trial `AddSurveyData` ใหม่**) · ย้ายเนื้อเต็มไป `tickets/GT-233.md` (>8,192 B) รอบนี้ด้วย · **ถอดออกจากรายการ ก. ด้านล่างแล้ว — ห้ามจัดให้ผู้เทสบูตใบนี้อีก**
🆕 **[K cu7c2r 20:11] `GT-281` ชั้น wire = PASS พับแล้ว** (จดหมายเดียวกับข้างบน) — `PLAYER_FACTION basic_faction=1` ที่ login ทะเล 126 ผ่าน return ticket · ชั้นจอยังไม่วัด (เจ้าของหยุดเครื่องหลังบูต 2) ⇒ **ยัง READY** เหลือแค่ `/warp 2` ดูสีชื่อมอน (รายการ ก.2 ด้านล่าง)

🔴 **ใบที่มี RESULT/ปิดแล้วไม่อยู่ในรายการนี้แล้ว**: GT-214 · GT-217 · GT-220 · GT-223 · GT-224 · GT-233 (🆕 CLOSED รอบนี้) · GT-242 · GT-249 · GT-250 · GT-251 · GT-252 · GT-253 · GT-255 · GT-257 · GT-266 · GT-269 · GT-272 · GT-277 · RE-235 · RE-237 · RE-261 · RE-272 (รายละเอียดผล ⇒ หัวใบใน `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` หรือจดหมายรอบ)
**ยัง BLOCKED (ตรวจสดครั้งล่าสุดรอบ `cm9v9y` 17:10 — รอบนี้ไม่มีเครื่องมือแตะ `pirate-force-server` จึงไม่ตรวจ precondition ซ้ำ แต่ยืนยันแล้วว่าไม่มีจดหมายใหม่เปลี่ยนสถานะสองใบนี้)**: `GT-284` WORLD-SCENE-STATE-SURVIVES-RELOGIN-001 ยัง BLOCKED ไม่เข้ารายการบูต · `RE-280`/`RE-282`/`RE-283`/`RE-285` เป็นใบ RE runner (static/client-image, ต้อง debugger/memory-watch คนละแบบกับบูตปกติ) ไม่ใช่ใบ attended-capture ของผู้เทสหน้าจอเกม — ไม่เข้าเกณฑ์สแนปช็อตนี้แม้ `RE-280` จะมีบล็อก `ATTENDED:` แล้วก็ตาม
**รายการ ก./ข./ค. ที่เหลือ (`GT-272`/`GT-274`/`GT-258`/`GT-262`/`GT-279`/`GT-193`/`GT-151`/`GT-178`/`GT-276`/`RE-273`/`RE-155`) ตรวจสดผ่าน `pf_queue_status.py` รอบนี้แล้วว่ายัง READY/OPEN ไม่มี RESULT ใหม่ — เนื้อ ATTENDED ไม่เปลี่ยนจากฉบับรอบ `x91eo8r2`/`cm9v9y`**

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

## ง. ใบ NEEDS-ATTENDED-CAPTURE ที่ตกรถ (ไม่มีบล็อก `ATTENDED:` — chief ไม่จัดคิวได้จนกว่าเจ้าของใบจะเติม)
- `RE-155` ACTOR-NAME-COLOR-NPC-VS-HOSTILE-MOB-ONE-FIELD-CROSSWALK-001 — ไม่พบบล็อก `ATTENDED:` ในใบ ณ ตอน generate สแนปช็อตนี้

## จ. nonclaims ของสแนปช็อตนี้
- ไม่ได้ไล่ทุกบรรทัดของ `CLIENT_RE_QUEUE.md` แบบ RE ล้วน (สแกนเฉพาะแท็ก `NEEDS-ATTENDED-CAPTURE`) — RE เฉพาะที่ไม่มีแท็กนี้ไม่ถูกนับ (ปกติไม่ต้อง capture)
- ไม่ได้ตัดสินว่าใบไหน "ควรบูต" ก่อน — ลำดับ (ก)/(ข)/(ค) และเลขในวงเล็บเป็นการเรียงตามกติกา ไม่ใช่คำสั่งบูต
- ใบที่มีบล็อก `ATTENDED:` มากกว่าหนึ่งก้อนในตัวเอง (เช่นใบ multi-step) แสดงเฉพาะก้อนแรกที่เจอ — อ่านเนื้อใบเต็มก่อนบูตเสมอ
- `GT-274` ไม่ได้ตรวจกาน "ก่อนบูต (gate)" ให้ล่วงหน้าจากรอบนี้ (ไม่มีเครื่องมือรัน git ต่อ pirate-force-server ในเซสชันนี้) — ผู้บูตต้องรันเองก่อนเสมอตามที่หัวใบสั่ง
- รายการ ก./ข./ค. ที่เหลือ (นอกจาก GT-233/GT-281 ที่ตรวจสดรอบนี้) ยังยกมาจากฉบับรอบ `x91eo8r2`/`cm9v9y` โดยยืนยันผ่าน `pf_queue_status.py` ว่าสถานะเปิด/READY ไม่เปลี่ยน — ไม่ได้เปิดอ่านเนื้อ ATTENDED ทีละใบซ้ำทั้งหมดรอบนี้ (ไม่มีจดหมายใหม่แตะใบเหล่านี้)
