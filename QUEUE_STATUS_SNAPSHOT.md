# QUEUE_STATUS_SNAPSHOT — สแนปช็อตใบ READY + มี `ATTENDED:` + ยังไม่มี `RESULT`

🔴 **ไฟล์นี้ generate สดโดย LANE-K ทุกรอบ ห้ามอ่านเป็นประวัติ — เชื่อเฉพาะฉบับล่าสุด** (ka1-A ใช้ไฟล์นี้จัดรถบัส capture แทนการอ่าน `GAME_TEST_QUEUE.md` 2 MB เอง)
สร้างโดย: LANE-K รอบ `slug54r2` · เวลา 2026-09-06T13:40+07:00 · แหล่ง: `GAME_TEST_QUEUE.md` + `CLIENT_RE_QUEUE.md` บน `origin/main` หลังแก้ผล pf-adversary ของรอบ `slug54` — ดู `rounds/K_20260906_1340_slug54r2_*.md`
ลำดับ: (1) PANYA-ORDER (2) ไมล์สโตนใน `NOW.md` (3) อายุใบ (เก่าสุดก่อน) · แยกตามชนิดบูต

🔴 **ใบที่มี RESULT แล้วไม่อยู่ในรายการนี้แล้ว** (พับแล้วรอบ `slug54`/`slug54r2`): GT-214 · GT-217 · GT-220 · GT-223 · GT-224 · GT-242 · GT-249 · GT-250 · GT-251 · GT-252 · GT-253 · GT-255 · GT-257 · GT-266 · GT-269 · GT-272 · RE-235 · RE-237 · RE-261 · RE-272 (รายละเอียดผล ⇒ หัวใบใน `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` หรือจดหมายรอบ) · 🔴 **`GT-223`/`GT-224`/`GT-249` แก้เข้าใหม่รอบ `slug54r2`** — รอบ `slug54` เคยพลาด (GT-223 เขียนผิดว่า "ไม่มีผล" ทั้งที่มี FAIL จริงจาก R309 · GT-249 ไม่ถูกแตะเลยทั้งที่มี PASS-PARTIAL ค้างเกรด >30 ชม. จาก R312) เพราะจดหมายเหล่านั้นมี `.CONSUMED.txt` จากสายอื่นเพื่อจุดประสงค์อื่นอยู่ก่อนแล้ว — pf-adversary จับได้ ดู `notes_to_chief/20260906_1350_LANE-K-ASK-COO-consumed-marker-collision.md`

---

## ก. ไร้ธง / env (บูตมาตรฐานหรือ env variable — ไม่ใช่ `--*-scenario`)

1. **`GT-233` M2-PROVISIONING-TRIAL-001** — env `PF_M2_SURVEY_TRIAL=1` (ไม่มีธง scenario) · **PANYA-ORDER 0155/0156 + M2 milestone ตัวบล็อกโค้ด 0** (NOW.md: "M2 ... GT-233 อยู่บนเครื่องคุณ") · warp 126 → logout/login → แล่นเข้าใกล้เกาะ 2 (dock 153) และเกาะ 3 (dock 154) เกาะละ ~3 นัด · **นัดเดียวไม่มี BACKUP** (NOW.md) · `RE-270` ขนานได้
2. **`GT-258` WARP-SEND-FAILURE-ROLLS-THE-SCENE-BACK-001** — ไร้ธง scenario · GM account · อัดวิดีโอต่อเนื่องตลอด `LOCK_GAME` · precondition: `git grep install_send_outcome_observers -- src/pirateforce_foundation/runtime.py` ต้องเจอบนคอมมิตที่บูต (ไม่เจอ = BLOCKED ข้ามใบ) · เจ้าของใบ/ผู้บริโภคผล = LANE-GM · ต่อท้ายคิว ไม่บล็อกสายใด
3. **`GT-262` STALL-AND-GUILD-STORAGE-ATTENDED-CAPTURE-001** — ไร้ธง (สร้างตัวละครใหม่ปกติ) · หาทางเข้า "แผงขายเอง" (เพดาน 15 นาที/20 คลิก) + "คลังกิลด์" (เพดาน 10 นาที/15 คลิก) · คู่กับ `RE-261` (RE-261 มี CAPTURED บางส่วนแล้วจาก R320 — ปุ่มแถวบนกระเป๋า 7 ปุ่ม NOT REACHED ทั้ง 4 ฟีเจอร์ยัง — ใบนี้ยังต้องหาทางเข้าเอง) · เจ้าของใบ/ผู้บริโภคผล = LANE-UI · ต่อท้ายคิว
4. **`GT-193` SPEED-COMMAND-SPARSE-X7-001 (เฉพาะขั้น 9-10)** — ไร้ธง scenario + `-SecondPasswordMode bypass` · run-copy DB เฉพาะรอบ · **ห้ามตั้ง `PF_SPEED_TRIAL`** (คนละใบกับ `GT-218`) · ขั้น 4-7 ยัง PENDING interface ห้ามเกรด · ก่อนบูตต้องรัน RECHECK ข้อ 6 สดสี่คำสั่งให้ผ่านก่อน
5. **`GT-151` PORT-ROYAL-SEVEN-HOLES-EYES-001 (ค้าง 1/7 จุด)** — ไร้ธง (`/warp 10` หรือ GM staged login) · ใบเก่า (30 ส.ค.) 6 จุดที่เหลือยังไม่ได้เดินตรวจ · ไม่บล็อกใคร
6. **`GT-178` BG0015-HOSTILE-TWELVE-AGGRO-001** — สรุป ATTENDED ในใบสั้นเกินตัดสินชนิดบูตจากตรงนี้ (อ่านเนื้อใบเต็มก่อนบูต) · ใบเก่า

7. **`GT-276` LEARN-SKILL-RESULT-WALKLOCK-ISOLATE-001** (ใหม่ ตั้งเลขรอบนี้) — ไร้ธง `--*-scenario` (ส่งเฟรมทีละอันผ่านเครื่องมือ dev) · หาว่าเฟรมไหนใน sweep 6 ขั้นของ `GT-249` ทำให้เดินไม่ได้ · เจ้าของใบ/ผู้บริโภคผล = LANE-CS

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
