# GAME TEST QUEUE -- ARCHIVE 20260905 (closed tickets moved verbatim from `GAME_TEST_QUEUE.md` per PANYA-ORDER 20260905_2038 item 1; each has a one-line stub left in place; nothing here is deleted)

## GT-078 M1-V1-ACCEPTANCE-PORT-ROYAL-POPULATION-115-001 [attended, in-game]: บูตเซิร์ฟเวอร์ **โดยไม่มีแฟล็ก scenario แม้แต่ตัวเดียว** แล้วเจ้าของเดินทั่ว Port Royal — **เมืองมีคนอยู่จริงหรือไม่ และของเดิมทั้งหมดยังเล่นได้อยู่ไหม** (ใบตรวจรับ `v1` ของ `M1`)  [✅ **CLOSED — `v1` ประกาศแล้ว 2026-08-30 โดย chief R249 ตาม `COO-DECISION 20260830_2142`** ปิดช่องว่าง identity ด้วยหลักฐานคนละใบ (`GT-131` `OBSERVER_CONFIRMED: 2026-08-30T00:2x+07:00` โดย Panya คำต่อคำ "ตำแหน่ง npc ถูก ตัวถูกต้อง ฉันให้เทสนี้ผ่าน") แทนที่จะรัน `GT-078` ซ้ำ — ดูบล็อก v1 เต็มที่ `pirate-force-server/SERVER_VERSIONS.md` · **`GT-078` เองยังคง OWNER-REJECTED ตามที่รันจริงเมื่อ 2026-08-26 ห้ามเขียนว่า "PASS"** ใบนี้ปิดเพราะเกณฑ์ M1/v1 ครบด้วยหลักฐานทดแทนแล้ว ไม่ใช่เพราะใบนี้เองผ่าน — **ประวัติเต็มย้ายไปที่ `archive/GT-078_history_20260901.md` (กฎ v6.3 §11)**]

### pass criteria — **สองชั้น แยกกันเด็ดขาด 🔴 ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

**ชั้น (1) wire/DB — ทำ headless ได้ ไม่ต้องมีคนหน้าจอ**
1. **`BOOT_COMMIT`** + ผลเช็คลิสต์ปลดบล็อกข้อ 3 ทั้งสี่บรรทัด (แปะสิ่งที่คอนโซลพิมพ์)
2. 🎯 **หลักฐานกฎข้อ 1:** `CommandLine` ของโปรเซสเซิร์ฟเวอร์ **ทั้งบรรทัด** · **ต้องไม่มีสตริง `-scenario` เลย** · console ไม่มี label เลนหัววัดแม้แต่บรรทัดเดียว
3. **`composed`** = เลขที่ log พิมพ์ก่อนส่ง · วัดไม่ได้เขียน **`composed = unmeasured`**
4. **`sent`** = นับจาก `GAME_LIVE.txt` · **census: นับ *ทุก* บรรทัด `[G>]` ทั้งไฟล์แล้วรายงานยอดรวม ไม่กรองอะไรออก**
5. **session ต่อเนื่อง ≥ 10 นาที:** ไม่มี reconnect · ไม่มี GAME connection ที่สอง · เวลาเข้า-ออกเป็นตัวเลข
6. ไม่มี traceback · stderr 0 B · **ไม่มี `ErrorData=28317`** (มี = จดว่าโผล่หลังอะไร เก็บคอนโซลทั้งไฟล์)
7. DB สำเนา: `PRAGMA integrity_check` = `ok` · row-diff ต่างเฉพาะ `sessions` **+1 ต่อการเข้าเกมหนึ่งครั้ง** (`count(*) WHERE selected_character_id IS NOT NULL`) · `max(lease_generation)` **ไม่ถอยหลัง** · **sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`** · **canonical ไม่ถูกเปิดตลอดรอบ**
8. **ความครบของวิดีโอ:** `ffprobe` → เฟรมจริงเทียบ `duration x fps` · **รายงานเฟรมที่หายเป็นตัวเลข** 🔴 บอกว่าไฟล์ครบแค่ไหน ไม่ได้บอกว่าในเฟรมมีอะไร
9. 🔴🔴 **ชั้นนี้ตอบไม่ได้:** **`composed = 115` และ `sent = 115` ไม่ใช่หลักฐานว่ามีอะไรขึ้นจอแม้แต่ตัวเดียว** · **`M1` ปิดด้วยชั้นนี้ไม่ได้เด็ดขาด**

**ชั้น (2) client-observable — ต้องมีคนหน้าจอ · 🔴 ตัวปิดใบและตัวปิด `M1` อยู่ชั้นนี้ชั้นเดียว**
1. **หลักฐานบังคับ:** วิดีโอต่อเนื่องครอบคลุม ≥ 10 นาทีในแมพ · ภาพนิ่ง full-res ≥ 3 ใบ · **sha256 ทุกไฟล์** · **ทุกเฟรมที่อ้างมีบรรทัด `FRAME:`** + **`UNMEASURED_DIST:`**
2. 🎯 **เลขหลักของใบ — ตอบเป็นตัวเลขจริง ห้ามตอบเป็นคำ:**
   - **`seen_max_frame`** = จำนวน NPC มากที่สุดที่นับได้ **ในเฟรมเดียว** + ชื่อไฟล์เฟรมนั้น + บรรทัด `FRAME:`
   - **`seen_tour_total`** = จำนวนตัวที่นับได้ตลอดทัวร์ **แบบไม่นับซ้ำ** + **วิธีตัดตัวซ้ำ เขียนเป็นภาษาคน**
   - **ตารางต่อจุด `S0..S5`:** HUD `X/Y` · `t` ที่ถึงจุด · จำนวนที่นับได้ · ไฟล์ภาพ
   - 🔴 **`seen` น้อยกว่า `sent` ไม่ใช่ FAIL** — เป็นค่าที่วัดได้ · 🔴 **ห้ามอนุมานสาเหตุ**
3. **กฎข้อ 2 (สะสม) — ตอบทีละบรรทัด ห้ามยุบรวม:** ล็อกอิน **ผ่าน/ไม่ผ่าน** · หน้าเลือกตัวละคร **ผ่าน/ไม่ผ่าน** · เดิน `W/A/S/D` **ผ่าน/ไม่ผ่าน** · **อยู่ครบ 10 นาทีโดยไม่หลุด ผ่าน/ไม่ผ่าน** (พร้อมเวลาจริงสองค่า)
4. **ประโยคของเจ้าของ (กฎข้อ 4) — คัดคำต่อคำ ห้ามเรียบเรียงใหม่:** *"ผู้เล่นทำอะไรได้ ที่เวอร์ชันก่อนทำไม่ได้"* + *"เมืองมีชีวิตหรือยัง"*
   - 🔴 **ผู้ช่วยห้ามเขียนประโยคนี้แทนเจ้าของ** — ถ้าเธอไม่ได้พูด ให้เขียนว่า **"เจ้าของยังไม่ได้ให้ประโยคนี้"**
5. **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ full-res** (PLAYBOOK ข้อ 13)
6. **NO-CRASH / CRASH verdict** (ตัดสินด้วยคลิกขวาลากเท่านั้น)
7. 🔴 **ชั้นนี้ตอบไม่ได้:** เซิร์ฟเวอร์ประกอบ/ส่งไปกี่ตัว · บูตมีแฟล็กหรือไม่ · ทำไม `seen` ไม่เท่า `sent`

🔴 **ชั้น (1) ไม่ผ่านข้อ 2 (พบแฟล็ก scenario) ⇒ NO-RESULT ทางเทคนิคทันที — ห้ามอ่านจอเป็นผลใด ๆ แม้เห็นเมืองแน่นไปหมด**

---

**ลิงก์:**
- ประวัติเต็ม (protocol/ถ้อยคำเดิม/ผลลัพธ์ V1-V7/nonclaims): `archive/GT-078_history_20260901.md`
- ผลรอบที่รันจริง 2026-08-26: `notes_to_chief/consumed/20260826_1430_GT078-RESULT-*.md` + addendum `20260826_1440_GT078-ADDENDUM-*.md`
- หลักฐานทดแทนที่ปิด `M1`/`v1`: `GT-131` (`OBSERVER_CONFIRMED: 2026-08-30T00:2x+07:00`)
- คำตัดสิน: `COO-DECISION 20260830_2142` (chief R249) · บล็อก `v1`: `pirate-force-server/SERVER_VERSIONS.md`
- divergence identity/name/title: `REAL_SERVER_DIVERGENCE.tsv`

---

## GT-106-R2 COO-DECISION-20260830-2048 IN-SESSION-TELEPORT-RENDER-001: เมื่อ TeleportVital ข้ามฉากมาถึงกลางเซสชัน (ผ่าน _dispatch_columbus_quest3021 หลังคลิกเควส 3021 ของ Columbus ไม่ใช่ตอน login) ไคลเอนต์เรนเดอร์ฉากปลายทางจริงไหม หรือเฟรมถูกรับแต่จอไม่เปลี่ยนอะไรเลย  [~~PENDING -- ด่าน 0 ยังไม่ยืนยันว่าเดินบทสนทนาถึงจุดคลิกได้จริงในบูตเดียว~~ 🟢 **PASS — chief รอบ `893xv4` 2026-08-31T~14:5x+07:00 ปิดหัวใบ (ค้างล้าสมัยเป็นใบที่ 7 ตามที่กะ1-A ชี้ใน `20260831_1435_KA1A-NOTE-*`) ตามผล `notes_to_chief/20260831_1036_GT106R2-RESULT-PASS-client-renders-the-destination-scene-mid-session-plus-two-new-findings.md`: `OBSERVER_CONFIRMED: 2026-08-31T10:0x+07:00` เจ้าของขับ UI เอง เดินบทสนทนา Columbus ถึงจุดคลิกเควส 3021 จริง (ด่าน 0 ผ่านครั้งแรก) แล้วถูกวาร์ปไปฉาก 17 (`Bg1001` "Ship in the Sea") จอเปลี่ยนจริง พิกัดเปลี่ยนเป็น X=834 Y=-598 -- ไม่ใช่ "เฟรมถูกรับแต่จอไม่เปลี่ยน" ตามสมมติฐานทางเลือกของใบ. wire: `WORLD_SCENE scene_id=17 model=Bg1001 name=a_ship_at_sea sent_before=NO`. `COO-DECISION 20260831_1441` ยืนยันเงื่อนไขของ `COO-DECISION 20260830_2048` หมดแล้ว เปิดทางเลือก 1 ให้ GM `/warp` ข้ามฉากยิง live teleport กลางเซสชัน (เขตของสาย GM เอง ต่อสายเองรอบถัดไป). รับข้อเสนอ mailbox-triage ของกะ1-A เป็นกฎมาตรฐานตาม `COO-DECISION 1441`: ทุกใบผล CONSUMED ที่ chief consume ต้อง grep หัวใบ GT/RE ที่มันอ้างถึงแล้วปิดเองถ้าสถานะไม่ตรงกับผล**]

> เลขใบ: ตัวนับร่วมกับ CLIENT_RE_QUEUE.md. grep ยืนยัน 2026-08-30: ไม่มี heading `## GT-106-R2` จริงในทั้งสอง
> ไฟล์ (รวม archive/) -- มีแค่การพาดพิงชื่อนี้ในข้อความปรับปรุงของ `GT-106` เอง (บรรทัด 4951/4956/4958/4963/
> 4965 ไฟล์นี้) ซึ่งหมายถึง "รันซ้ำ GT-106" คนละความหมายกับใบนี้ ใบนี้เป็นคำถามใหม่แยกกัน ตามที่
> `COO-DECISION 20260830_2048` สั่งเปิดตรง ๆ เปิดโดย chief รอบ `67ga0v` (ร่างโดย pf-queue-author)

### ที่มา
`COO-DECISION 20260830_2048` (`notes_to_chief/20260830_2048_COO-DECISION-warp-cross-scene-waits-for-gt106-r2.md`)
สั่งตรง: "ยืนยันว่าไคลเอนต์เรนเดอร์ฉากปลายทางจริงหรือไม่ เมื่อ `TeleportVital` มาถึงกลางเซสชัน (ไม่ใช่ตอน
login)" อ้างอิง `RE-162` (`notes_to_chief/20260830_1909_RE-162-RESULT-IN-SESSION-SCENE-CHANGE-WIRE-EXISTS-
CLIENT-OBSERVABLE-UNPROVEN.md`) ซึ่งวัด headless ว่า `_dispatch_columbus_quest3021` (`runtime.py:4826-5044`,
dispatch ที่ `runtime.py:8045`) ส่ง `TeleportVital` ข้ามฉากจริงขณะออนไลน์ (ไม่ใช่แค่ login) ด้วย encoder
เดียวกับ login (`legacy.make_login_teleport`) -- กลไก live mid-session teleport ตัวเดียวที่มีจริงวันนี้
`/warp` เจตนา**ไม่ใช้**กลไกนี้ (stage รอ login หน้าแทน ตาม `COO-DECISION 20260828_2130`) และยังคงเดิมจนกว่า
ใบนี้จะมีผล

### เกตก่อนบูต (สืบทอดจาก GT-106 ตรง -- trigger เดียวกัน, ห้ามสมมติว่าเปิดแล้ว)
ใบนี้ขี่ trigger เดียวกับ `GT-106` (บทสนทนา Columbus -> เลือกเควส 3021 -> `_dispatch_columbus_quest3021`)
อ่าน update ล่าสุดของ `GT-106` เอง (chief รอบ `bunu7v`/R246, 2026-08-30, บรรทัด 4960-4966 ไฟล์นี้) ก่อนบูต
ทุกครั้ง: 3 จุดของ `COO-DECISION 1746` ต่อสายครบฝั่ง server-side wiring แล้ว (`CORE-REQUEST-018`/`019`) และ
`RE-162` ยืนยันซ้ำว่า dispatch ยังส่งเฟรมจริง -- **แต่ไม่มีใครยืนยันว่าเดินบทสนทนาถึงจุดคลิกเควส 3021 ได้จริง
ในบูตเดียวสักครั้ง** (`GT-106` เองก็ยังไม่มีผลใน `result:`) ก่อนบูตต้อง grep ซ้ำสามคำสั่งจาก addendum ของ
`GT-106` (บรรทัด 4896-4900 ไฟล์นี้) บน `<SHA>` จริง และเดินเกต 7 ข้อของ `RE-162` Job 3(B) ("Columbus
quest-3021 in-session teleport") เดินถึงจุดคลิกไม่ได้ = ทั้งใบคง **PENDING -- รอด่าน 0 เดินถึงจริง** (ไม่ใช่
BLOCKED ไม่ใช่ NO-RESULT) ห้ามยิง `TeleportVital` มือเปล่า ห้ามแก้ `src/`

### สองชั้นหลักฐาน
- **wire/DB (พิสูจน์ headless แล้วโดย RE-162, ไม่ใช่ของใหม่ใบนี้)**: `_dispatch_columbus_quest3021`
  ประกอบ/ส่ง `TeleportVital` จริงไปฉาก 17 ผ่าน `legacy.make_login_teleport` ขณะ character ออนไลน์อยู่แล้ว
  (`runtime.py:5035-5044`) ใบนี้แค่ยืนยันซ้ำบนบูตจริง + เช็ค persistence: `character_positions` ต้องเขียน
  `scene_id=17` ตรงกับ XYZ ฉาก 17 (ไม่ถอยกลับไปเป็นบั๊ก `scene_id=1` ที่ `GT-106` R197 เคยเจอ)
- **client-observable (ใบนี้มีไว้ตอบเรื่องนี้โดยเฉพาะ)**: วินาทีที่เฟรมมาถึงหลังคลิก จอเปลี่ยนจากฉาก Port
  Royal ไปฉากปลายทางจริงไหม เทียบกับนิ่งอยู่ฉากเดิมไม่มีอะไรเกิดขึ้นเลย (เฟรมถูกรับแต่ FSM ฝั่งไคลเอนต์ไม่อยู่
  state `StateRunTime`/`StateNavigation` ตอนเฟรมมาถึง จึงถูกปัดทิ้งเงียบ -- `RE-077` T3 / `RE-162`
  nonclaim 2)

### objective (claim เดียว)
เมื่อเฟรม `TeleportVital` ข้ามฉากมาถึงไคลเอนต์ที่ออนไลน์อยู่แล้ว (กลางเซสชัน ไม่ใช่ login) ไคลเอนต์เรนเดอร์
การเปลี่ยนฉากบนจอจริงหรือไม่ -- ตอบแค่ "เห็นการเปลี่ยนฉาก" vs "ไม่เห็นอะไรเลย/ค้าง" **ไม่ตัดสิน**คุณภาพจุดลง
(claim ของ `GT-106` เอง แยกกันคนละใบ)

### nonclaim บังคับ
1. ไม่ตัดสินว่า `/warp` ควรใช้กลไกนี้หรือไม่ -- เป็นของ COO ล้วน ตาม `COO-DECISION 20260830_2048`:
   "เมื่อ `GT-106-R2` มีผล (PASS/FAIL) ให้สาย GM ส่งจดหมายขอเคาะใหม่พร้อมผลนั้นทันที" (ตามด้วยอีกหนึ่งประโยค
   ก่อนลงชื่อ ไม่ใช่บรรทัดสุดท้ายจริงของใบ -- แก้คำบรรยายตำแหน่งตามที่ pf-adversary รอบ `67ga0v` จับได้)
   ใบนี้แค่ผลิตผลนั้น
2. ไม่ทดสอบซ้ำคำถามจุดลงฉาก 17 ของ `GT-106` (ยืนบนผิวน้ำ/จม/หลุดขอบ) -- claim เดิมของ `GT-106` เปิดแยกอยู่
   แม้ trigger จะเป็นตัวเดียวกัน
3. ไม่ปิดช่องว่างสำมะโน/actor ที่ `RE-162` Job 4 พบ (Columbus dispatch ไม่ส่งสำมะโนตามฉากปลายทาง) -- ความ
   เสี่ยงจริงที่บันทึกไว้ ยังไม่มีเจ้าของรับผิดชอบ ถ้าฉากเปลี่ยนแต่ actor/NPC อื่นหายหมด บันทึกเป็นข้อสังเกตแยก
   ไม่กระทบ PASS/FAIL ของ claim นี้ (claim นี้วัดแค่ "ฉากเปลี่ยนไหม")
4. ผลลบ (จอไม่เปลี่ยน/ค้าง/เฟรมถูกปัดทิ้งเงียบ) มีค่าเท่ากับผลบวก -- คือคำตอบ ไม่ใช่ความล้มเหลวของใบเทส
   ทิศทางถัดไปถ้าเป็นผลลบ: ต้องมีคนวัด state FSM จริงตอนคลิกเควส (`0x005F14B0`/`RE-077` T3) -- งานของใบ RE
   คนละใบ ไม่ใช่ใบนี้
5. คลิกขวาลากกล้อง = หมุนกล้องอย่างเดียว ไม่ยิงอะไรออกสาย ใช้เป็น NO-CRASH check ได้ทุกจุด ห้ามใช้ `Q`/`E`
   เป็น NO-CRASH check -- `Q`/`E` หันตัวละครจริงและยิง `TargetPosVital`

### db (สำเนาเสมอ ห้ามเปิด canonical)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-106-R2_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt106r2.sqlite3
```
เทียบ sha256 canonical กับ `CANON_SHA.txt` ก่อน/หลัง ต้องตรงทั้งสองครั้ง

### server args
ขึ้นกับเส้นทางที่ด่าน 0 หาเจอจริง (เส้นทางเดียวกับที่ `GT-106` ใช้เดินถึง Columbus ได้) **เขียนบรรทัดคำสั่งจริง
เป๊ะ ๆ ลงผลก่อนบูต** ห้ามคัดลอกจากใบอื่นเดา ห้ามพ่วง `--*-scenario` ตัวอื่นเข้าบูตเดียวกัน

### steps (คลิกต่อคลิก)
1. LOCK_GAME, ผ่านเกตด่าน 0 จริง (grep สามคำสั่ง + เดินถึงจุดคลิกเควส 3021 ได้จริง), จด BOOT_COMMIT + คำสั่ง
   บูตจริง
2. ล็อกอินปกติ เดินเล่นในฉากเดิม (Port Royal) อย่างน้อย 60 วินาที ก่อนเข้าใกล้ Columbus -- ยืนยันว่าเป็น
   mid-session จริง ไม่ใช่เฟรมที่ติดมาจากขั้นตอน login
3. NO-CRASH ก่อน trigger: คลิกขวาลากกวาดกล้อง 360 องศา, ถ่ายภาพนิ่ง full-res ของฉากเดิมไว้เทียบก่อน/หลัง
4. เดินเข้าไปคุย Columbus, เลือกบทสนทนาจนถึงตัวเลือกเควส 3021, คลิกยืนยัน
5. จับตาจอทันทีหลังคลิก บันทึกใน 5 วินาทีแรก: จอโหลด/เปลี่ยนฉากจริง, หรือนิ่งอยู่ฉากเดิมไม่มีอะไรเกิดขึ้นเลย,
   หรือค้าง/error/disconnect
6. ถ้าฉากเปลี่ยน: ยืนยัน console/log พิมพ์ token เดินทางเข้าฉากปลายทาง (รูปแบบเดียวกับที่ `GT-106` ใช้,
   `SCENE_ENTRY scene=17 ...`) ถ่ายภาพนิ่ง full-res ของฉากใหม่ + ป้ายชื่อทุกป้ายในเฟรม
7. ถ้าฉากไม่เปลี่ยน: รออีก 30 วินาที (กันโหลดช้า) แล้วบันทึกผลลบตามจริง **ห้ามคลิกเควสซ้ำ**
   (`columbus_quest3021_dispatch_attempted` ล็อกครั้งเดียวต่อ connection คลิกซ้ำจะเงียบสนิทไม่มี event)
   จบ NO-CRASH check แล้วไป teardown แทน
8. NO-CRASH ซ้ำ (คลิกขวาลากกล้องเท่านั้น) -> teardown -> เทียบ sha canonical -> query
   `character_positions` แถวล่าสุดของตัวละครนี้ ยืนยัน `scene_id` ตรงฉากปลายทางจริง

### pass criteria (สองชั้น แยกกันเสมอ)
wire/DB: log/console พิมพ์ token เดินทางเข้าฉากปลายทางจริงระหว่างบูต (ยืนยันซ้ำกลไกที่ `RE-162` วัด headless
ไว้) + แถวล่าสุดของ `character_positions` มี `scene_id` ตรงฉากปลายทาง ไม่ใช่ฉากเดิม (regression check ต่อ
บั๊กที่ `GT-106` R197 เจอ) + `sessions`/`max(lease_generation)` ไม่ถอยหลัง + sha256 canonical ตรงก่อน/หลัง +
`PRAGMA integrity_check`=ok
client-observable: อย่างใดอย่างหนึ่งที่เห็นจริง (ไม่เดา) -- (ก) จอเปลี่ยนฉากจริง ผู้เล่นอยู่ในสภาพเล่นต่อได้ =
PASS สำหรับ claim นี้ (ไม่ตัดสินคุณภาพจุดลง) หรือ (ข) จอนิ่งอยู่ฉากเดิม/ค้าง/error/disconnect = ผลลบ มีค่า
เท่ากับผลบวก ตาม nonclaim ข้อ 4 + สีป้ายชื่อทุกป้ายในทุกภาพ full-res (บรรทัดเดียวต่อป้าย, "none" เขียนออกมา
ถ้าไม่มี, อ่านจาก full-res เท่านั้น ห้ามอ่านจาก contact sheet/ภาพย่อ/วิดีโอ, ห้ามชี้สาเหตุ -- `RE-067` เปิดอยู่)
ส่วนต่างจากภาพของ real server เดิม (ถ้ามีของเทียบ) บันทึกลง `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่ง

### result (ผู้เทสกรอก)
```

```

---

## GT-116 CORE-REQUEST-022 CLASS-LEVEL-LOGIN-SKILLWINDOW-UNBLOCK-001: after CORE-REQUEST-022 wires class_id=1 (Gladiator) + level=1 into every login's ActorAttr/BasicAttr frames, does a real client's skill window (K / `Bt_main_Skill`) finally open, and does the wire actually carry those two fields byte-exact -- the one field GT-058/GT-059/GT-064 (all CLOSED, archived) could never get past because class was always 0  [✅ PASS -- ปิดโดย chief round 28jd9c (2026-08-28T09:56+07:00) จากผล attended กะ1-A `20260828_0925_GT116-121-120-RESULT-*.md` · OBSERVER_CONFIRMED: 2026-08-28T09:2x+07:00 (BOOT_COMMIT `98307ae` = main HEAD) · claim เดียว (หน้าต่างสกิลเปิดได้) เท่านั้น: จอเจ้าของ "หน้าต่างสกิลเปิดได้ แต่ยังไม่มีรายการใด ๆ" -- level 1 มี 0 สกิลเป็นเรื่องปกติ ตรงเกณฑ์ P1/P2 เป๊ะ · [ไม่อ้าง] ว่ารายการสกิลของ Gladiator ถูก -- ยังไม่วัด (คนละเรื่อง)]

> NUMBERING NOTE: grep confirmed before reserving -- `GT-116`/`RE-116` = 0 hits in `GAME_TEST_QUEUE.md`,
> `CLIENT_RE_QUEUE.md`, and both `archive/*_closed.md` files (checked this round). Highest number in use
> is `115` (`RE-115` MAPWINDOW-SCENE-NPC-LIST-SOURCE-001, OPEN, unrelated topic -- claimed same round by a
> different lane) => this entry is `116`. Entries `GT-101`-`GT-114`, `GT-107-R3`, and `RE-085`-`RE-115` stay
> exactly where they are, unchanged -- this is a new entry, not a replacement for any of them. `GT-058`
> (CLOSED BOUNDED-NEGATIVE), `GT-059` (CLOSED P2/FALSIFIED), and `GT-064` (CLOSED) are archived, not
> reopened -- per the queue's own archival rule, only PENDING/READY/BLOCKED/RUNNING entries stay live, and
> all three are genuinely closed. This entry supersedes their open question with a new claim, on a new number.

### source (links only -- see cited files for full detail, not re-derived here)
- `notes_to_chief/20260828_0231_CHIEF-REPLY-CORE-REQUEST-022-class-level-wired-name-field-not-touched.md`
  (chief round `9do841`/R203): "class_id = 1 (Gladiator) -- `ActorAttr +0x8C`, mask bit `0x00000001`
  (เดิมไม่เคยส่งเลย, class=0 เสมอ ⇒ หน้าต่างสกิลเปิดไม่ได้ ตรงกับ GT learn-skill ที่ค้าง)" and "level = 1 --
  `BasicAttr +0x5E`, mask bit `0x0002` (เดิมไม่เคยส่งเลย)". Both wired into the flagless production login
  path AND the faction=1 recompose path in the same commit (a runtime length-delta check would otherwise
  fail-closed if only one path got the fields). New functions named in that letter: `player_wire.py`'s
  `make_actor_attr_with_name_and_class` / `make_actor_attr_with_name_class_and_faction`, wired into
  `legacy_bridge.py`'s `LegacyProjector.start_game`. Old functions (`make_actor_attr_with_name`,
  `make_actor_attr_with_basic_faction`) left untouched. Cites `3546 passed, 0 failed` full suite +
  pf-adversary review -- headless evidence, cited not reproduced by this entry.
- `notes_to_chief/20260828_0146_COO-DECISION-boot-character-actorattr-core-request-022-to-chief.md`: opens
  CORE-REQUEST-022, names class+level (+ name-slot fix, see below) as the minimum "สมประกอบ" boot character.
- `notes_to_chief/20260828_0125_PANYA-DECISION-boot-character-must-be-complete-...-ka1-B.md`: **owner's own
  testimony**, from a separate ad-hoc probe fork (never merged, canonical never touched): "GT ที่เทส
  learn skill ก็ติด block มาแล้วเพราะว่าเปิดหน้าต่างสกิลกันไม่ได้ จนตอนนี้เรามารู้แล้วว่าต้องใส่ค่า class
  ก่อนถึงจะเปิดหน้าต่างสกิลได้" -- this is the direct antecedent this entry tests. Same letter's table (③)
  independently pins `x13 = Actor b0 +0x8C u32 class id` and `x2 = Basic +0x5E u16 level`, matching the
  chief-reply's offsets.
- `GT-058` (CLOSED BOUNDED-NEGATIVE), `GT-059` SKILL-ATTR-WINDOW-GATE-001 (CLOSED P2/FALSIFIED: wire-exact
  `CSkillAttr` x3 triggers, window never opened either session), `GT-064`
  SKILL-ATTR-WINDOW-KPRESS-IN-GAP-001 (CLOSED) -- all archived in
  `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`. None of the three could ever isolate "was it timing,
  was it the wrong trigger, or was the client simply never told it had a class" -- class was 0 in every one
  of those sessions. This entry is the first attended shot with class != 0.
- ✅ **Verified chief round 2y0zil (2026-08-28T09:53+07:00):** branch `claude/awesome-darwin-9do841` /
  commit `8017c71` confirmed on `pirate-force-server` -- `pirate-force-server#162` shows `merged: true`,
  `merged_at: 2026-08-27T19:48:29Z` via the GitHub API, and `git log origin/main` on this round's fresh
  clone shows `8017c71` as an ancestor of HEAD (`08e9f4f Merge pull request #162 ...` -> `8017c71
  CORE-REQUEST-022: send class+level at login...`). No longer unverified; ด่าน 0/1/2 below can boot against
  current `origin/main` directly.

### objective (claim เดียว)
On a completely ordinary, flagless login (no `--*-scenario`), does the client now (a) receive
`class_id=1`/`level=1` byte-exact in its login ActorAttr/BasicAttr frames, and (b) as a direct consequence,
does pressing **K** / clicking `Bt_main_Skill` open an actual skill window for the first time in this
project's history -- instead of the total silence GT-058/059/064 measured every time before. Both layers
are the same claim (wire cause -> client effect), not two claims.

### predictions (a wrong prediction is a finding, not a failure)
- P1 [proposed, the heart of the entry] K / `Bt_main_Skill` after a normal flagless login opens the skill
  window -- something GT-058/059/064 never once observed.
- P2 [proposed, corollary] the window, once open, is not an empty/garbled error panel -- it shows
  Gladiator-plausible content (zero learned skills at level 1 is a perfectly fine result; a broken/garbled
  panel is not).
- P3 [falsifier] K / `Bt_main_Skill` still produces nothing even with class_id=1 + level=1 confirmed on the
  wire -- a real negative, not a failure: it means these two fields are necessary but not sufficient, and
  redirects to the next untested field in the owner's own probe table (③) -- likely `x16`/`x17` (SP /
  remaining status points) or `x18`-`x22` (STR/CON/DEX/INT/PER) -- open a new RE/GT entry naming the next
  candidate rather than re-running this one.

### ก่อนบูต -- ด่าน 0 (สถานะ merge, ยังไม่ merge ณ ตอนเขียนใบ -- ห้ามข้าม), ด่าน 1 (green boot), ด่าน 2 (grep ยืนยันสาย)

**ด่าน 0 -- สถานะ merge:** CORE-REQUEST-022 is reported (chief round `9do841`/R203, `notes_to_chief/
20260828_0231_CHIEF-REPLY-*`) as landed on a branch of `pirate-force-server`, **PR pending, not yet merged
into `main`** at time of writing. `pf_resolve_green_boot.py` follows `origin/main` only -- if the PR has not
merged when the tester runs ด่าน 1, the resolver will not return a commit containing this code (`exit 3`, or
a commit missing `player_wire.py`'s new functions). **The entry stays unbootable** -- record the result as
"รอ merge" and move to another ticket. **Never checkout the branch directly to skip the resolver**, even
with a sha in hand (same rule as every other entry in this queue) -- and never trust the `8017c71` string
above without ด่าน 2 confirming it live, per the source-section warning.

**ด่าน 1 -- resolve commit เขียว:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
Run from the `pf_bridge` folder. Only `exit 0` + a printed `BOOT_COMMIT: <sha>` means bootable (detached
HEAD checkout of `<sha>`). Do not eyeball-compare commit numbers -- the resolver returns whatever gated
branch head is current, not necessarily a merge commit.

**ด่าน 2 -- ยืนยันสายจริงของ `<SHA>` (ห้ามเชื่อเลขบรรทัด/ชื่อฟังก์ชันในเอกสาร ต้อง grep ของจริง):**
```
git grep -n "make_actor_attr_with_name_and_class" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "make_actor_attr_with_name_class_and_faction" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "make_actor_attr_with_name_and_class\|make_actor_attr_with_name_class_and_faction" <SHA> -- src/pirateforce_foundation/legacy_bridge.py
git grep -n "class_id" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "def start_game" <SHA> -- src/pirateforce_foundation/legacy_bridge.py
```
Need at least 1 line from every command. Missing any one = **BLOCKED** -- the commit that would boot does
not actually carry CORE-REQUEST-022 -- do not boot, do not hunt for a different commit yourself, go do
another ticket and come back later.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-116_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt116.sqlite3
```
- Compare canonical sha256 against `CANON_SHA.txt` both before start and after finish -- must match both
  times.
- Fresh copy every boot => character position resets to spawn every time (same spawn other entries use:
  X -8553.9473, Y -2579.6890, Z 186.0, scene 1 Port Royal), regardless of anything saved from a previous
  session.

### server args (เป๊ะ -- ไม่มี --*-scenario เพราะ CORE-REQUEST-022 ทำงานเสมอ flagless production, ไม่มีสวิตช์)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt116.sqlite3
```
No `--*-scenario` flag of any kind, no other entry piggybacked onto this boot. Capture proof of the bare
command line immediately after the server comes up, paste the full line into the result:
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```

### steps (click by click -- record continuous video for the whole LOCK_GAME window)
Before start: hold `LOCK_GAME`, note boot stamp (+07:00, must be under 420 min old when teardown runs),
compare canonical sha, copy both DBs per the db block, stage `TEMPLATE_teardown_generic.ps1`. Confirm ด่าน
0-2 all cleared (record the resolved SHA).

1. Start the server first always (`Get-NetTCPConnection -State Established` on ports 10188/10189 must be 0
   before opening the client). A client opened with no server dies on its own in ~3.5 minutes. If the client
   has to be killed mid-session, restart the server before opening the next client -- the server keeps the
   old session, and the next client hangs on "connecting" forever otherwise.
2. Open client -> select server -> PVP dialog left button -> character select -> first slot -> the middle
   of the 5 bottom buttons = enter game (never the leftmost -- that deletes the character). Start continuous
   recording before pressing enter-game.
3. T0 -- HP bar / minimap / map name all visible. Record HUD X/Y. Photograph full-res, name-label colours
   from this still (self, "none" if no other label visible).
4. NO-CRASH check: right-click-drag to sweep the camera 360 degrees once. This is the only liveness check
   this entry accepts -- camera-only, character facing never moves, nothing goes out on the wire, safe at
   any point. **Never use Q/E or W/A/S/D for this check** -- those turn the character and emit
   `TargetPosVital`.
5. Press **K** (or click `Bt_main_Skill` if K does nothing) -- photograph full-res immediately before and
   immediately after. Record every new server console line that appears in the same window.
6. If a window opened: photograph its full content full-res, read/record what it shows character-for-
   character from the still (not from memory). Do not compare it against any expected skill list -- this
   entry does not test content correctness (see nonclaims).
7. Secondary positive control (same move GT-059 used): press **C** to open the `CHARACTER` window,
   photograph, close. This has opened successfully in every prior session even when K didn't -- if C fails
   too, that's a much bigger finding than this entry's own claim, write it up prominently.
8. NO-CRASH check again (right-click-drag).
9. Log out -> teardown via `TEMPLATE_teardown_generic.ps1` (boot stamp must still be under 420 min) ->
   recheck canonical sha256 -> sha256 every capture.

Colour rule (Panya's order, 2026-08-25): one line per label per image, write "none" not blank, full-res
stills only (never a contact sheet or video), never infer a cause -- `RE-067` is open and is the only place
that question lives.

### pass criteria (two layers, never mixed)

wire/DB (read from raw captured frame bytes / server console+log only, never from what's on screen):
- The login/StartGame response's ActorAttr block, at byte offset **+0x8C** relative to that block's start,
  decodes as u32 little-endian **`0x00000001`** (class_id=1), and the frame's own change-mask has bit
  **`0x00000001`** set for that block (previously this field was never sent at all, not merely zero --
  record which of "absent" vs "present-but-zero" the pre-fix baseline actually was if a comparison capture
  exists, otherwise just record what this session shows).
- The same response's BasicAttr block, at offset **+0x5E**, decodes as u16 little-endian **`0x0001`**
  (level=1), with change-mask bit **`0x0002`** set.
- Byte layout reference for locating these offsets inside the captured frame:
  `drafts/CHUNK2_Q1_ACTORATTR_MASK_FINDINGS.md` (pinned 55-field ActorAttr/BasicAttr map).
- `sessions`: +1 row with `selected_character_id` set for this login; `max(lease_generation)` does not go
  backward; `PRAGMA integrity_check` = `ok` on the working copy both times; canonical sha256 matches
  `CANON_SHA.txt` before and after.
- Raw GAME log + console out/err kept whole, not trimmed, both before and after.
- Negative result with equal standing: if class_id/level are still absent or still zero on the wire despite
  ด่าน 0-2 clearing -- write that up in full, it means the merged commit did not do what the letter claims,
  which is itself the finding.

client-observable (a human at the screen only, never inferred from the console):
- Whether the skill window (K / `Bt_main_Skill`) opens at all is the primary reading -- opens (even
  showing zero learned skills) vs. still nothing, both are complete, valid results; write whichever one
  actually happened, do not treat "still nothing" as this entry failing (see P3).
- If it opens: full-res photograph, content transcribed character-for-character from the still.
- `C` / `CHARACTER` window control check per step 7.
- Both NO-CRASH checks pass.
- Name-label colours recorded per the colour rule above, one line per label per full-res still, "none"
  written out where there is none.

### nonclaims
- 🔴 **Does not prove the character-name-slot bug is fixed.** The chief's own reply
  (`...0231_CHIEF-REPLY-...-name-field-not-touched.md`) states the `x37`(`+0x164`, guild-name slot) ->
  `x1`(`+0x28`, real name slot) move was deliberately **not** done this round, pending a second source of RE
  confirmation. **UPDATE 2026-08-28 ~09:xx +07:00, chief round `03d46t`:** CORE-REQUEST-027 now wires this
  move (headless-proven, PR pending merge) -- see `GT-122` for the dedicated attended entry. If GT-116 runs
  before CORE-REQUEST-027 merges, expect the old guild-slot placement per this nonclaim; if it runs after,
  the name should already be correct and GT-122 is the entry that claims/tests it, not this one -- do not
  read either outcome here as this entry's own finding.
- Does not prove "probe base 1" full completeness (movement speed `x7`, HP/MP per `STANDARD_STATUS`, stat
  points `x18`-`x22`, etc. from the owner's own table in `...0125_PANYA-DECISION-...`) -- only `class_id`
  (`x13`) and `level` (`x2`) were wired this round, per the chief reply.
- Does not test or reopen `GT-058`/`GT-059`/`GT-064` -- those stay CLOSED/archived exactly as written. This
  entry answers a related but distinct question (does an ordinary flagless login with class!=0 unblock the
  window) rather than repeating their scenario-driven `CSkillAttr` trigger tests.
- Does not test skill-window **content** correctness (whether the skills shown, if any, actually match a
  level-1 Gladiator's real kit) -- only whether the window opens.
- Does not test the faction=1 / HYP-PF-027 recompose path's client-visible behaviour -- the chief reply
  states headless coverage exists for both paths sharing one length-delta check, cited here, not reproduced.
- Single account, single login, single session -- no reconnect/relogin, no second character, no second
  player observing.
- Does not decide the cause of any name-label colour observed (`RE-067` stays open, no cause inferred).
- If ด่าน 0/1/2 don't clear (PR not merged / functions not found at the resolved SHA) -> the entire entry is
  **BLOCKED**, not NO-RESULT/FAIL -- record it as "รอ merge" and stop.

### result (ผู้เทสกรอก)
```

```

---

## GT-122 CORE-REQUEST-027 NAME-FIELD-GUILD-SLOT-FIX-001: after CORE-REQUEST-027 moves the character's own name off ActorAttr's guild-name slot (`+0x164`, mask bit `0x01000000`, `LABEL_GUILD`) and onto BasicAttr's real name slot (`+0x28`, mask bit `0x0001`, `LABEL_NAME`) -- the guild-slot bug GT-116's own nonclaims section named and CORE-REQUEST-022/023 deliberately left untouched -- does a real client's own nameplate and `CHARACTER` window now show the character's name as a name, with no guild artifact on a freshly-created guildless character [**PASS ทั้งสองชั้น** -- เกรดโดย chief รอบ `wi1m62` 2026-08-29T01:0x+07:00 จากผล `notes_to_chief/20260829_0018_KA3A-GT122-PASS-GT102-PARTIAL-GT104-BLOCKED-mobs-answer-as-npc.md` ข้อ ① · `OBSERVER_CONFIRMED: 2026-08-29T00:17+07:00` · บูต flagless commit `3baf65de` · wire: `BasicAttr` mask `0x10010001` (บิต `0x0001` SET) + wstring `Arena01` · `ActorAttr` mask `0x0000000000000801` เป๊ะ · ลาย `0x01000000` = **0 hit** ใน u64 mask ทั้ง 13 ตัวของเฟรม · client-observable: ป้ายชื่อ `Arena01` ขาวล้วน ไม่มี artifact กิลด์ และหน้าต่าง CHARACTER **ไม่มีช่องกิลด์ทั้งหน้าต่าง** · หมายเหตุ ด่าน 2: grep ที่เขียนไว้เดิมในใบนี้ stale ณ เวลาเทส เจ้าของเคาะสดให้ใช้ 2 greps ที่แน่นกว่า (`make_actor_attr_with_name_and_class` ใน `legacy_bridge.py` · `return _make_...` ใน `player_wire.py`) -- ไม่แก้ถ้อยคำย้อนหลังเพราะใบปิดแล้ว บันทึกไว้ให้ใบถัดไปลอกรูปที่ถูก · ประวัติเดิม: PENDING -- merge confirmed chief round 28jd9c (2026-08-28T09:56+07:00, entry was stale until now -- pf-adversary caught it): `pirate-force-server#187` merged=true via `pull_request_read` method=get (merged_at 2026-08-28T02:28:54Z), commit `5e24e0b` verified an ancestor of `origin/main` HEAD (`9024844`) via `git merge-base --is-ancestor` on this round's fresh fetch. Ready for an attended session. Same handling as GT-116: do not boot until ด่าน 0 clears.]

> NUMBERING NOTE: grep confirmed before reserving -- `GT-122` = 0 hits in `GAME_TEST_QUEUE.md` at time of
> reservation. `RE-122` (`CLIENT_RE_QUEUE.md`) is already in use, filed under the `RE-` prefix for an
> unrelated topic (`PLAYER-STANDARD-STATUS-AND-CHARCREATE-SCORE-VALUES-001`, the still-open MP/STR/CON/DEX/
> INT/PER static probe) -- not this entry, not renamed, not touched here; `GT-` and `RE-` are separate
> counters in separate files, same as `GT-116`/`RE-116` before it. `RE-123`'s own NUMBERING NOTE (round
> `of27sx`, 2026-08-28 ~08:3x+07:00) already lists `GT-101`-`GT-122` alongside `RE-085`-`RE-122` as
> protected/unchanged -- this number was already anticipated before this entry was filed, this is that
> anticipated entry, not a fresh collision. `GT-101`-`GT-121` and `RE-085`-`RE-123` stay exactly where they
> are, unchanged -- this is a new entry, not a replacement for any of them.

### source (links only -- see cited files for full detail, not re-derived here)
- `notes_to_chief/20260828_0125_PANYA-DECISION-boot-character-must-be-complete-min-probe-base-1-plus-name-x1-share-actorattr-probe-to-all-lanes-fix-name-in-guild-slot-ka1-B.md`:
  owner's own live-client probe (row ② item 2, row ③ x1/x37) -- "ชื่อตัวละครที่ปัจจุบันส่งลง
  x37 (+0x164 = LABEL_GUILD ชื่อกิลด์) ต้องย้ายไป x1 -- x37 ต้องว่างสำหรับตัวละครใหม่ (ไม่มีกิลด์)". Table
  row 1 pins `x1 = Basic 0x0001 +0x28 wstring` -> ป้ายล่างสีขาว + หน้าต่าง `CHARACTER`; row 37 pins
  `x37 = ActorAttr b24 +0x164 wstring` -> ชื่อกิลด์ (ควรว่าง) + row 38 (`+0x180` guild-flag byte) -> สีป้าย
  ม่วง(มีกิลด์)/ส้ม(ไม่มี) -- the *flag* byte, not the name field, is what this project's own table says
  drives the purple/orange split; CORE-REQUEST-027 does not touch `+0x180`.
- `notes_to_chief/20260828_0231_CHIEF-REPLY-CORE-REQUEST-022-class-level-wired-name-field-not-touched.md`:
  chief's prior round (`9do841`) deliberately declined to move x1/x37, pending a second independent source
  before touching a field with a prior live-client PASS on it. CORE-REQUEST-027 is the follow-up that answers
  that ask.
- `notes_to_chief/20260828_0912_CHIEF-REPLY-CORE-REQUEST-027-actor-name-slot-wired.md` (chief round `03d46t`,
  this round): `player_wire.py`'s `_make_actor_attr_with_name_and_class` (the real-login-path composer wired
  via `legacy_bridge.py`'s `LegacyProjector.start_game` -- NOT the frozen `make_actor_attr_with_name`/
  `make_actor_attr_with_basic_faction` baseline, left untouched) now writes the name wstring to
  `BasicAttr +0x28` (bit `0x0001`) instead of `ActorAttr +0x164`, and the `ActorAttr` mask literal changed
  `0x01000801` -> `0x00000801` (bit `0x01000000` no longer set at all). Net frame length unchanged. Cited
  headless evidence: full suite `3750 passed, 327 skipped, 0 failed` (skips pre-declared/pinned via
  `tools/pf_pytest_precondition_census.py`), `tools/verify_hypothesis_ledger.py` clean, `pf-adversary` review
  pass before PR. Two golden-hash files re-baselined (`tests/golden/foundation_v1.json`,
  `tests/golden/item_lifecycle_v1.json`) -- only `start_pc`/`start_frame`/`merged_start_pc`/
  `merged_start_frame` keys changed, frozen V141 template path untouched -- cited as blast-radius evidence,
  not reproduced by this entry.
- GT-116's own nonclaims section (see its UPDATE block, this round) already forward-references this entry.

### objective (single claim)
On a completely ordinary, flagless login (no `--*-scenario`), does the character's own name now render in the
correct name slot -- the white nameplate above the character and the `CHARACTER` (`C`) window -- instead of
the guild-name slot, and does the character show no guild artifact (matching a freshly-created character that
has no guild)? Wire cause and client effect are the same claim here, not two entries.

### predictions (a wrong prediction is a finding, not a failure)
- P1 [proposed, the heart of the entry] the nameplate above the character and the `CHARACTER` window both show
  the character's actual own name, transcribed verbatim off a full-res still -- not blank, not garbled, not
  standing in for something else.
- P2 [proposed, corollary] no guild tag/label is visible anywhere on screen for this character, and if the
  `CHARACTER` window has a guild field at all, it reads empty/none -- consistent with a freshly-created
  guildless character.
- P3 [falsifier] the name is missing entirely, garbled, or visibly rendered as if it were a guild
  tag/slot -- a real negative, not a failure: it would mean the fix is wrong or incomplete, and redirects to a
  new RE ticket comparing this session's raw frame bytes against the queue's own pinned ActorAttr/BasicAttr
  mask findings field-by-field rather than re-running this entry. A name-label rendering in guild-styled
  colour (purple, per the owner's own table row 38) is also a P3 finding worth recording, but per the colour
  rule below the tester records the colour only and does not infer that the name-field move caused it -- the
  actual driver per this project's own table is the separate `+0x180` guild-flag byte, untouched by
  CORE-REQUEST-027, and `RE-067` (name-label colour cause) stays open regardless of what this entry sees.

### ก่อนบูต -- ด่าน 0 (สถานะ merge, ยังไม่ merge ณ ตอนเขียนใบ -- ห้ามข้าม), ด่าน 1 (green boot), ด่าน 2 (grep ยืนยันสาย)

**ด่าน 0 -- สถานะ merge:** CORE-REQUEST-027 is reported (chief round `03d46t`) as landed on branch
`claude/jolly-mccarthy-03d46t` of `pirate-force-server`, **PR pending, not yet merged into `main`** at time of
writing. `pf_resolve_green_boot.py` follows `origin/main` only -- if the PR has not merged when the tester
runs ด่าน 1, the resolver will not return a commit containing this code (`exit 3`, or a commit missing
`_make_actor_attr_with_name_and_class`). **The entry stays unbootable** -- record the result as "รอ merge" and
move to another ticket. **Never checkout the branch directly to skip the resolver**, even with a sha in hand,
and never trust any sha string above without ด่าน 2 confirming it live.

**ด่าน 1 -- resolve commit เขียว:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
Run from the `pf_bridge` folder. Only `exit 0` + a printed `BOOT_COMMIT: <sha>` means bootable (detached HEAD
checkout of `<sha>`). Do not eyeball-compare commit numbers.

**ด่าน 2 -- ยืนยันสายจริงของ `<SHA>` (need at least 1 line from every command; missing any one = BLOCKED, do
not boot, do not hunt for a different commit, go do another ticket and come back later):**
```
git grep -n "_make_actor_attr_with_name_and_class" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "0x00000801" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "_make_actor_attr_with_name_and_class" <SHA> -- src/pirateforce_foundation/legacy_bridge.py
git grep -n "def make_actor_attr_with_name\b" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "def start_game" <SHA> -- src/pirateforce_foundation/legacy_bridge.py
```
The fourth command confirms the OLD frozen baseline (`make_actor_attr_with_name`) is still present and
untouched -- if it is gone, more changed than this ticket's description covers, treat as BLOCKED too.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-122_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt122.sqlite3
```
Compare canonical sha256 against `CANON_SHA.txt` both before start and after finish -- must match both times.
Fresh copy every boot => character position resets to spawn every time (X -8553.9473, Y -2579.6890, Z 186.0,
scene 1 Port Royal), regardless of anything saved from a previous session.

### server args (เป๊ะ -- ไม่มี --*-scenario, production flagless path only)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt122.sqlite3
```
No `--*-scenario` flag of any kind, no other entry piggybacked onto this boot. Capture proof of the bare
command line immediately after the server comes up:
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```

### steps (click by click -- record continuous video for the whole LOCK_GAME window)
Before start: hold `LOCK_GAME`, note boot stamp (+07:00, must be under 420 min old when teardown runs), compare
canonical sha, copy both DBs per the db block, stage `TEMPLATE_teardown_generic.ps1`. Confirm ด่าน 0-2 all
cleared (record the resolved SHA).

1. Start the server first always (`Get-NetTCPConnection -State Established` on ports 10188/10189 must be 0
   before opening the client). A client opened with no server dies on its own in ~3.5 minutes. If the client
   has to be killed mid-session, restart the server before opening the next client.
2. Open client -> select server -> PVP dialog left button -> character select -> first slot -> the middle of
   the 5 bottom buttons = enter game (never the leftmost -- that deletes the character). Start continuous
   recording before pressing enter-game.
3. T0 -- HP bar / minimap / map name all visible. Photograph full-res immediately.
4. NO-CRASH check: right-click-drag to sweep the camera 360 degrees once. Camera-only, character facing never
   moves, nothing goes out on the wire, safe at any point. **Never use Q/E or W/A/S/D for this check.**
5. Photograph the nameplate above the character full-res, close enough to read it clearly; transcribe the
   text verbatim from the still -- this is the P1 reading.
6. Press **C** to open the `CHARACTER` window; photograph full-res; transcribe the name field shown verbatim,
   and note whether any guild tag/field/label appears anywhere in that window ("none" if none).
7. NO-CRASH check again (right-click-drag).
8. Log out -> teardown via `TEMPLATE_teardown_generic.ps1` (boot stamp must still be under 420 min) -> recheck
   canonical sha256 -> sha256 every capture.

Colour rule (Panya's order, 2026-08-25): one line per label per image, write "none" not blank, full-res stills
only (never a contact sheet or video), never infer a cause -- `RE-067` is open and is the only place that
question lives. Divergences from the original server's screenshots go into `REAL_SERVER_DIVERGENCE.tsv`.

### pass criteria (two layers, never mixed)

wire/DB (read from raw captured frame bytes / server console+log only, never from what's on screen):
- The login/StartGame response's `BasicAttr` block has change-mask bit **`0x0001`** set, with a wstring field
  immediately following the mask field among `BasicAttr`'s emitted fields (ascending mask-bit order -- `0x0001`
  is the lowest bit, so it is emitted first) that decodes to the character's actual stored name.
- The same response's `ActorAttr` block does **NOT** have change-mask bit **`0x01000000`** set at all (absent,
  not merely present-and-zero -- record which the captured frame actually shows).
- Net frame length: record byte length of the `BasicAttr`/`ActorAttr` blocks and the whole StartGame response;
  compare against a pre-fix capture if the tester has one, otherwise record this session's bytes as a fresh
  baseline, not a comparison.
- `sessions`: +1 row with `selected_character_id` set for this login; `max(lease_generation)` does not go
  backward; `PRAGMA integrity_check` = `ok` on the working copy both times; canonical sha256 matches
  `CANON_SHA.txt` before and after. Raw GAME log + console out/err kept whole, both before and after.
- Negative result with equal standing: if `0x01000000` is still set, or the `0x0001` name field does not
  decode to the character's name, despite ด่าน 0-2 clearing -- write that up in full; it means the merged
  commit did not do what this ticket's source description claims, which is itself the finding.

client-observable (a human at the screen only, never inferred from the console):
- Nameplate text (step 5) transcribed verbatim from a full-res still -- PASS reading = matches the character's
  actual own name; anything else (blank/garbled/wrong text) is recorded plainly, not read as this entry's own
  failure (see P3).
- `CHARACTER` window name field (step 6) transcribed verbatim; presence/absence of any guild
  tag/field/label anywhere in that window recorded plainly ("none" if none).
- Both NO-CRASH checks pass.
- Name-label colours recorded per the colour rule above, one line per label per full-res still, "none" written
  out where there is none.

### nonclaims
- Does not test class/level or the skill window (`K` / `Bt_main_Skill`) -- that is `GT-116`'s claim, a
  separate entry on a separate number; do not read either entry's result as evidence for the other.
- Does not test movement speed / HP-MP completeness / STR-CON-DEX-INT-PER stat points -- the remainder of the
  owner's own "probe base 1" table is still open at `RE-122` (`CLIENT_RE_QUEUE.md`), unrelated to this fix.
- Does not test guild membership mechanics (joining, leaving, guild chat, etc.) -- only that a freshly-created
  guildless character shows no guild artifact on login.
- Does not decide the cause of any name-label colour observed -- `RE-067` stays open, no cause inferred, even
  if a guild-styled colour appears (see P3's caveat re the separate `+0x180` guild-flag byte).
- Single account, single login, single session -- no reconnect/relogin, no second character, no second player
  observing, no guild ever actually created or joined.
- Headless full-suite (`3750 passed, 327 skipped, 0 failed`), ledger-verify, and `pf-adversary` review are
  cited evidence from this round's build, not reproduced or re-run by this entry.
- The two golden-hash re-baselines (`tests/golden/foundation_v1.json`, `tests/golden/item_lifecycle_v1.json`)
  are cited as blast-radius evidence only -- this entry does not independently re-verify their diff.
- If ด่าน 0/1/2 don't clear (PR not merged / functions not found at the resolved SHA) -> the entire entry is
  **BLOCKED**, not NO-RESULT/FAIL -- record it as "รอ merge" and stop.

### result (ผู้เทสกรอก)
```

```

---

## GT-120 CORE-REQUEST-025 TRACEPATH-GO-BUTTON-STALL-CLEAR-001: after CORE-REQUEST-025 wires an empty-vector `CTracePathVital` (0x2F92) reply to every `CTracePathReqVital` (0x4391), does a real client's map-window GO! button actually stop the client stuck showing "กำลังค้นหาเส้นทาง..." forever -- the orange stall KA1A found this round -- and does NOT this entry test whether the character walks anywhere (no waypoint/auto-walk logic exists yet)  [✅ PASS -- ปิดโดย chief round 28jd9c (2026-08-28T09:56+07:00) จากผล attended กะ1-A `20260828_0925_GT116-121-120-RESULT-*.md` · OBSERVER_CONFIRMED: 2026-08-28T09:2x+07:00 (BOOT_COMMIT `98307ae` = main HEAD) · claim เดียว (ข้อความไม่ค้างตลอดไป) เท่านั้น: กด GO! ที่ Warden Sebastian แล้ว "กำลังค้นหาเป้าหมาย.." หายใน 1 วินาที (เดิมค้างตลอดไป) จากนั้นแชทแจ้ง "เป้าหมายปัจจุบันไม่มีอยู่..." ตรงกับพฤติกรรม empty-vector fallback ที่ตั้งใจ · [ไม่อ้าง] ว่า GO! พาเดินไปหา NPC ได้จริง -- ยังไม่มี auto-walk/path จริง เป็นงานถัดไป]

> NUMBERING NOTE: grep confirmed before reserving (2026-08-28, round R206) -- `GT-120`/`RE-120` = 0 hits in
> `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`, and `archive/`. Highest number in use anywhere in the shared
> counter is `119` (`RE-119` TRACEPATH-GO-BUTTON-REQREPLY-LAYOUT-001, CLOSED PASS/DONE) -- `GT-116` is the
> highest bare GT number but is lower than 119 -- => this entry is `120`. Entries `GT-101`-`GT-116`,
> `GT-107-R3`, and `RE-085`-`RE-119` stay exactly where they are, unchanged -- this is a new entry, not a
> replacement for any of them.

### source (links only -- see cited files for full detail, not re-derived here)
- `notes_to_chief/consumed/20260828_0235_KA1A-FOUND-GO-button-sends-CTracePathReqVital-0x4391-server-must-answer-0x2F92.md`:
  attended finding, exact repro path `เปิดแผนที่ (M) -> เลือก NPC -> กด GO!` -- nothing happens on the wire
  reply side, orange center-screen text "กำลังค้นหาเส้นทาง..." stays up forever (screenshot
  `M1P_ingame_20260828_prison_exile_pike_deer_*.png`). Server never sent `0x2F92` at all.
- `notes_to_chief/20260828_0424_RE-119-RESULT-DISCRIMINATED-PATH-RECORDS-AND-UI-ACTIONS.md` (STATIC-ON-BRIDGE,
  PASS/DONE): proves the client's own response handler `[0x006EA9E0,0x006EACD3)`, on an empty response vector
  (`u16` count = 0, no records), dispatches UI action `EndFindPath` at object `Main_FindPath` -- a clean stall-
  clear signal, static evidence only, never fired at a real client before this entry.
- `notes_to_chief/20260828_0427_LANE-A-CORE-REQUEST-025-wire-tracepath-empty-response-fallback.md`: opens the
  build request, scoped explicitly to "empty-vector fallback only, do not guess a real path."
- `archive/rounds_2026-08-27_to_28/R206_confident-ride-l5xxkh_core-request-025-tracepath-empty-vector-plus-024-shadow-numbering-flag.md`:
  chief wired it same round. New `src/pirateforce_foundation/trace_path.py` (`TRACE_PATH_REQ_VITAL_ID`=0x4391,
  `TRACE_PATH_VITAL_ID`=0x2F92, `make_trace_path_empty_response`); `runtime.py` dispatch branch is
  unconditional (no `--*-scenario` flag -- production path), fail-closed if no character selected. New
  `tests/test_trace_path_wiring.py` (4 tests, driven through the real dispatcher): no reply pre-select;
  byte-identical to calling the builder directly; reply re-parses to exactly one `u16` tag `0x12`=0 field and
  nothing else; repeated requests each independent. Full suite `3568 passed, 0 failed` cited, not reproduced
  here.
- `notes_to_chief/consumed/20260828_0200_PANYA-DECISION-new-direction-attr-completeness-use-client-data-map-window-GO-probe.md`
  ADDENDUM 02:35: the owner's own attended GO! probe was stood down "until the payload is understood" --
  RE-119 (closed) + CORE-REQUEST-025 (wired) together lift that pause; this is the first attended shot since.

### objective (single claim -- wire/DB layer is a separate, already-closed claim)
On an ordinary flagless login, after selecting a destination in the in-game map window and clicking GO!, does
the client stop showing the orange "กำลังค้นหาเส้นทาง..." text stuck forever, instead clearing it the way
KA1A's pre-fix capture never once saw. The wire/DB layer of this same fix (does the server actually reply with
a structurally-empty `CTracePathVital`) is already proven headless this round in
`tests/test_trace_path_wiring.py` (pirate-force-server repo) -- cited above, NOT re-proven by this entry. This
entry is the client-observable layer only: the first human eyes on this specific fix.

### predictions (a wrong prediction is a finding, not a failure)
- P1 [primary, proposed]: clicking GO! causes the orange text to either not persist at all, or to appear and
  then clear on its own within a short window -- either way, NOT stuck forever the way KA1A captured it.
- P2 [expected non-event, explicitly NOT a requirement]: the character does not walk/move anywhere. If motion
  is observed, write it up as a surprising bonus finding, separate from this entry's own pass/fail -- CORE-
  REQUEST-025 deliberately implements no waypoint/auto-walk logic (RE-119 T4, request field `u16@+0x14`
  bounded negative, never touched this round).
- P3 [falsifier]: the orange text still appears and never clears within the observation window below -- a real
  negative, not a failure. It would mean either this client build never received the fix, this exact click
  path does not reach the new dispatch branch, or `EndFindPath` needs more than an empty vector in practice
  (RE-119's handler proof was static, never fired at a real client before this entry) -- redirect to a new
  RE/GT entry naming which of those three, do not re-run this one guessing.

### ก่อนบูต -- ด่าน 0 (merge status, MUST clear first), ด่าน 1 (green boot), ด่าน 2 (grep confirms the branch)
**ด่าน 0 -- merge status:** commit `pirate-force-server@4ddfd54` is confirmed merged into `origin/main` as of
round `qynsyw` (`git merge-base --is-ancestor 4ddfd54 origin/main` => ancestor, via `pirate-force-server#173`,
itself an ancestor of the current `origin/main` HEAD `29a3a92`/PR `#180`) -- this replaces the earlier
"not yet confirmed" note, which is now stale. This does NOT mean the tester can skip verification: run
`pf_resolve_green_boot.py` yourself at boot time regardless (more commits may have landed on `origin/main`
between this note and your session) -- if it still returns non-zero or a commit missing `trace_path.py`,
the entry stays unbootable, record "รอ merge" and move to another ticket. Never checkout the branch directly
to skip the resolver, and never trust the `4ddfd54` string above without ด่าน 2 confirming it live.

**ด่าน 1:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
Only `exit 0` + printed `BOOT_COMMIT: <sha>` means bootable.

**ด่าน 2 (need at least 1 line from every command; missing any one = BLOCKED, do not boot):**
```
git grep -n "TRACE_PATH_REQ_VITAL_ID" <SHA> -- src/pirateforce_foundation/trace_path.py
git grep -n "TRACE_PATH_VITAL_ID" <SHA> -- src/pirateforce_foundation/trace_path.py
git grep -n "make_trace_path_empty_response" <SHA> -- src/pirateforce_foundation/trace_path.py
git grep -n "0x4391\|TRACE_PATH_REQ_VITAL_ID" <SHA> -- src/pirateforce_foundation/runtime.py
```

### db
default_state\pirateforce.sqlite3 -- copy only, canonical never opened. Copy to
`pf_bridge\backup\pirateforce_before_GT-120_<yyyyMMdd_HHmmss>.sqlite3`, then `state\run_gt120.sqlite3`. sha256
vs `CANON_SHA.txt` before/after; `PRAGMA integrity_check=ok` on the working copy both times.

### server args (flagless -- the dispatch branch is unconditional/production, no `--*-scenario` of any kind)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt120.sqlite3
```
No scenario flag, no other entry piggybacked onto this boot. Any ordinary character/login works -- default
spawn (Port Royal, scene 1) is enough; the map window's own NPC list is populated by the world census, not by
this fix.

### steps (click by click -- record continuous video for the whole LOCK_GAME window)
Before start: hold `LOCK_GAME`, note boot stamp (+07:00, must be under 420 min old at teardown), compare
canonical sha, copy both DBs per the db block, stage `TEMPLATE_teardown_generic.ps1`, confirm ด่าน 0-2 all
cleared (record the resolved SHA).
1. Start the server first (`Get-NetTCPConnection -State Established` on ports 10188/10189 must be 0 before
   opening the client -- a client opened with no server dies on its own in ~3.5 minutes). If a client has to
   be killed mid-session, restart the server before the next client -- the server keeps the old session, the
   next client hangs on "connecting" forever otherwise.
2. Open client, log in normally to a character, enter the map. Start continuous recording before entering.
3. T0: HP bar / minimap / map name visible. Record HUD X/Y. Photograph full-res, name-label colours from this
   still (self, "none" if no other label visible).
4. NO-CRASH check: right-click-drag to sweep the camera 360 degrees once. Camera-only, character facing never
   moves, nothing goes out on the wire. Never use Q/E or W/A/S/D for this check -- those turn the character
   and emit `TargetPosVital`.
5. Press M to open the map window. Photograph full-res.
6. Select any one destination/NPC entry in the map window's list (KA1A's own path: open map -> select NPC).
   Photograph the selection, before clicking GO!.
7. Click GO!. Immediately watch screen-center.
8. Photograph full-res at: immediately after click, +2s, +5s, +10s, +30s, or until the orange text clears,
   whichever comes first. Record whether it appeared at all, and if so the exact timestamp it appeared and the
   exact timestamp it cleared (or "still present at +30s" if it never clears).
9. Record HUD X/Y again -- expected unchanged (P2); if changed, note prominently as a bonus/surprise finding,
   not a requirement of this entry.
10. Supplementary only, not required for a pass: if the server console is visible, copy verbatim any line
    carrying `CTracePathReqVital`/`0x4391` at the moment of the click and any reply line carrying
    `CTracePathVital`/`0x2F92` -- a missing console line does not fail this entry (see wire/DB pass criteria).
11. NO-CRASH check again (right-click-drag).
12. Log out, teardown via `TEMPLATE_teardown_generic.ps1` (stamp still under 420 min), recheck canonical
    sha256, sha256 every capture.

Colour rule (Panya's order, 2026-08-25): one line per label per image, write "none" not blank, full-res stills
only (never a contact sheet or video), never infer a cause -- RE-067 is open and is the only place that
question lives.

### pass criteria (two layers, never mixed)

wire/DB: the actual claim this layer answers -- "does the server structurally reply with an empty
`CTracePathVital`" -- is already CLOSED headless this round by `tests/test_trace_path_wiring.py` (4/4 green,
cited above, not reproduced by this entry). This entry's own wire/DB obligations are only: canonical sha256
matches `CANON_SHA.txt` before/after; `PRAGMA integrity_check` = `ok` on the working copy both times;
`sessions`/`lease_generation` behave normally for one ordinary login. Any console lines captured per step 10
are recorded as supplementary corroboration only, never as a substitute for the client-observable answer below
and never required for this entry to close.

client-observable (a human at the screen only, never inferred from the console):
- Primary reading: does "กำลังค้นหาเส้นทาง..." ever get stuck forever, or does it clear (including "never even
  appeared because the reply was fast") -- P1 vs P3, both are complete, valid answers; write whichever
  actually happened.
- Secondary: did the character's position change -- expected no (P2); record either way, do not fail this
  entry if it did move.
- Both NO-CRASH checks pass.
- Name-label colours recorded per the colour rule above, one line per label per full-res still.

### nonclaims
- Does not prove any waypoint/auto-walk behavior of any kind. CORE-REQUEST-025 wires only an empty-vector
  reply; RE-119 T4 leaves the request's own discriminator field (`u16@+0x14`) bounded negative -- quest id vs.
  NPC id vs. list index is still unresolved, and no record-carrying reply exists to test.
- Does not test the map window's destination-selection semantics or which NPC/quest a given click corresponds
  to on the wire -- out of scope, RE-119 T4's own open question.
- Does not decide the cause of any name-label colour observed (`RE-067` stays open, no cause inferred).
- Does not reproduce or re-run `tests/test_trace_path_wiring.py` -- that headless proof is cited as already
  closed, this entry supplies only the client-observable half.
- Single account, single login, single session -- no reconnect/relogin, no second character.
- If ด่าน 0/1/2 don't clear (PR not merged / functions not found at the resolved SHA) -> the entire entry is
  **BLOCKED**, not NO-RESULT/FAIL -- record it as "รอ merge" and stop.
- Does not reopen or supersede any other GT/RE entry; PANYA-DECISION 0200's ADDENDUM 02:35 stood the GO! probe
  down only pending payload understanding -- RE-119 (closed) + CORE-REQUEST-025 (wired) lift that pause, this
  is the first attended shot since, on a fresh number.

### result (ผู้เทสกรอก)
```

```

---

## GT-127 GM-003 CHAT-COMMAND-DOOR-001: GM พิมพ์คำสั่งลง**กล่องแชทธรรมดา**ของเกม (ไม่ใช่หน้าต่าง `BT_GM`/`GMUI_BASIC` ที่คลิกแล้วเงียบ) แล้วเซิร์ฟเวอร์อ่านคำสั่งนั้นได้จริงไหม -- ตัดสินที่ ndjson audit log ไม่ใช่ผลบนจอ  [🟢 **CLOSED PASS (wire/DB layer, ตามเกณฑ์เดิมของใบเอง — ndjson audit ไม่ใช่ผลบนจอ)** — ปิดหัวใบโดย LANE-GM (เจ้าของใบ) รอบ `noixtz` 2026-08-30T17:4x+07:00 หลังเดินด่าน 2 เต็ม + P1-P4 จบโดย attended กะ1-A (เจ้าของขับ UI เอง) · `OBSERVER_CONFIRMED: 2026-08-30T17:1x+07:00` · `BOOT_COMMIT 57490434` = main HEAD ไร้แฟล็ก · consumed stub: `notes_to_chief/20260830_1731_*.CONSUMED.txt` · **ประวัติเต็ม (HOLD→READY→ทุกรอบอัปเดตของ chief/LANE-GM/P1-P4/ด่าน 0-2) ย้ายไปที่ `archive/GT-127_history_20260901.md` (กฎ v6.3 §11)**]

### objective (claim เดียว)
บนบูตไร้แฟล็ก บัญชีที่อยู่ใน GM allowlist พิมพ์คำสั่งที่ขึ้นต้นด้วย `/` ลงกล่องแชทธรรมดา -- เซิร์ฟเวอร์
**อ่านและ parse คำสั่งนั้นได้จริง** (มีเรคคอร์ดใน `capture/gm_command_log.ndjson`) และบัญชีที่ไม่อยู่ใน
allowlist พิมพ์คำสั่งเดียวกันแล้ว **ไม่ได้อะไรเลย** ใช่หรือไม่.

### ผลจริง (สรุปหนึ่งบรรทัด)
`capture/gm_command_log.ndjson` = 8 แถว (4 คำสั่งที่รู้จัก `/lv` `/warp 2` `/say` `/warp 14` × 2 แถว parse+outcome, ทุกแถว `executed:false`) · ประโยคธรรมดา/คำสั่งผิด = 0 แถวตามคาด · จอไม่เปลี่ยนอะไรเลยตรงคำทำนาย · **wire/DB: PASS** · **client-observable: ยังไม่มีใครวัดเต็มรูปแบบ** (บัญชีคู่ควบคุมทำได้แค่ 2/3 ข้อ — เจ้าของไม่มีบัญชีที่สอง) · รายละเอียดเต็มทุกรอบอัปเดต: ดูอาร์ไคฟ์

### pass criteria (สองชั้น แยกกันเสมอ ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)

**wire/DB (อ่านจากคอนโซล/ล็อก/ไฟล์บนดิสก์เท่านั้น):**
- คอนโซล: `LANE_GM_CHAT_ACTION <cmd> route=action` (stderr) + ชุด `gm_chat_action_*`:
  `gm_chat_action_accepted_lv` · `gm_chat_action_warp_withheld_no_confirmed_force_pos_vital_version_re129_open`
  (`/warp` **ไม่ใช่** `accepted_` และนั่นคือผลที่ถูกต้อง) ·
  `gm_chat_action_refused_not_a_command` · `gm_chat_action_refused_command_parse_error_*` ·
  `gm_chat_action_refused_not_gm_account` (บัญชีคู่ควบคุมได้ `stdout='' stderr=''` โดยตั้งใจ)
- `capture/gm_command_log.ndjson`: จำนวนแถวขึ้นกับ `BOOT_COMMIT` (0 hit ของ `AUDIT_RECORD_OUTCOME` = 1 แถวต่อคำสั่ง ·
  มี hit = 2 แถวต่อคำสั่ง คือ `issued` + `outcome`) · ที่ไม่เปลี่ยน: ทุกแถวมีชื่อบัญชี GM และ `"executed": false` ·
  **ไม่มี**เรคคอร์ดของบัญชีนอก allowlist และ**ไม่มี**เรคคอร์ดของประโยคธรรมดา
- `sessions`: +1 แถวต่อหนึ่งการล็อกอิน · `max(lease_generation)` ไม่ถอยหลัง · `PRAGMA integrity_check` = `ok`
  ก่อน/หลัง · sha256 canonical ตรง `CANON_SHA.txt` ก่อน/หลัง
- **ผลลบมีค่าเท่ากับผลบวก:** คอนโซลเงียบทั้งหมด/ndjson ไม่ถูกสร้าง ทั้งที่ด่าน 2 ผ่าน = ผลของใบนี้เช่นกัน

**client-observable (คนหน้าจอเท่านั้น ห้ามอนุมานจากคอนโซล):**
- **สิ่งที่คาดหมายคือ "ไม่มีอะไรเปลี่ยน"** -- บรรทัดแชทต้องแสดงผลเหมือนเดิมทุกประการ เลนนี้ต้องมองไม่เห็น
- คำถามที่ต้องตอบตรง ๆ: `/warp 2` ที่พิมพ์ไปปรากฏในหน้าต่างแชทเป็นข้อความธรรมดา หรือหายไป (ไคลเอนต์กลืนบรรทัด `/`)?
- ไม่มี warp ไม่มีเลเวลเปลี่ยน (GM-003 v1 ไม่มี execution) · บัญชีคู่ควบคุม: จอไม่มีอะไรเกิดขึ้นเช่นกัน
- NO-CRASH ผ่านทั้งสองครั้ง · ตารางสีป้ายชื่อครบตามกฎสี

🔴 **หมายเหตุจากใบเดิม:** เกณฑ์ที่ตัดสินจริงคือ P1/P2/P4 (เต็มในอาร์ไคฟ์) — บล็อกข้างบนเป็นสำเนาย่อ ถ้าขัดกัน P1 ชนะ

### nonclaims (ติดไปกับผลทุกกรณี)
- ไม่อ้างว่าคำสั่งใดมีผลต่อเกม -- v1 ทำแค่ parse + log (`"executed": false`)
- ไม่อ้างว่าใบนี้พิสูจน์อะไรเกี่ยวกับ `BT_GM`/`GMUI_BASIC`/`0x51E9` -- คนละประตู (`GT-103`, `RE-126`)
- ไม่อ้างว่าข้อความไม่ใช่ ASCII ผ่านเส้นทางนี้ได้ · **GM nonclaim:** ใบนี้ใช้สถานะ GM เพื่อไปให้ถึงสถานะที่ทดสอบ
  ไม่ใช่หลักฐานว่าฟีเจอร์ทำงานสำหรับผู้เล่นทั่วไป · ไม่ทดสอบไวยากรณ์ที่เหลือ (`npc`/`item`/`spawn`/`say`) หรือ `rate_limited`

---

**ลิงก์:**
- ประวัติเต็ม (ทุกเวอร์ชันของหัวใบ, ที่มา, P1-P4, ด่าน 0-2/grep, db/server args/ขั้นตอน, หลักฐานที่ต้องเก็บ, teardown): `archive/GT-127_history_20260901.md`
- ผลปิดใบ: `notes_to_chief/20260830_1731_GT127-GT134-RESULT-both-PASS-chat-door-open-and-first-eyes-on-hell-volcano.md`

## GT-131 NPC-IDENTITY-CLINE-RESOLVED-001 [attended, in-game]: NPC ของ Port Royal แสดง **ตัวจริง** แล้วหรือยัง -- ใบตรวจรับหลัง `GT-078` ถูกเจ้าของปฏิเสธ  [~~PENDING~~ ✅ **PASS · ปิดโดยเจ้าของใบ LANE-A รอบ `n4wj7k` 2026-08-30T08:30+07:00 — `OBSERVER_CONFIRMED` โดย Panya:** กะ3-A ใบ `notes_to_chief/20260830_0030_KA3A-GT131-PASS-owner-confirmed-gt151-partial-plus-four-polish-gaps-and-mob-vs-npc-question.md` บันทึกคำต่อคำ "ตำแหน่ง npc ถูก ตัวถูกต้อง ฉันให้เทสนี้ผ่าน" (2026-08-30T00:2x+07:00) · ชั้น client-observable: ท่าเรือ Marine Transport Station/Columbus + Royal Navy/Loie ตรงตำแหน่งครบทั้งสองสมอ, ลานดอกไม้ 3 ชื่อ + Training Iron Man, ย่านร้าน 3 ชื่อ, ท่าเรือฝั่งเรือเหลือง 2 ชื่อ — ไม่พบชื่อเก่านอกกลุ่ม 13 placement · ชั้น wire บูตเดียวกัน `WORLD_CENSUS_INITIAL_108`/`WORLD_CENSUS_REAPPLY_108`, `undressable=7`, `ceiling=108/115` ตรงคำทำนาย · วิดีโอ `1352_b131151_FULLROUND_20260830_000047.mkv` + ภาพนิ่ง 4 ใบ เก็บไว้ ห้ามลบ · 🔴 การปิดใบนี้ไม่เปลี่ยนเลข 115: เพดานข้อมูลยังเป็น 108/115 ตาม `COO-DECISION 20260829_1941` — GT-131 ยืนยันเฉพาะ**ตัวตน**ของ 108 ที่ส่งจริง เจ็ดรูชั้นสายตายังเป็นเรื่องของ `GT-151` แยกกัน (ดูหัวใบนั้น)]
[ประวัติเดิม ก่อนปิดใบ ไม่ลบ: 🆕 **บันทึกโดยเจ้าของใบ LANE-A รอบ `80x5ba` 2026-08-29T20:4x+07:00 — สถานะของใบไม่เปลี่ยน ยัง PENDING:** `COO-DECISION 2026-08-29T19:41+07:00` (`notes_to_chief/20260829_1941_COO-DECISION-build001-closes-at-108-data-ceiling.md`) **ปิดชั้น wire/DB ของ BUILD-001 ที่ 108/115** โดยประกาศ 108 เป็น**เพดานของข้อมูลที่ไคลเอนต์ชิป ไม่ใช่งานที่ทำไม่ถึง** (`RE-149` BOUNDED-NEGATIVE verifier PASS 51/51 · 5 ไม่มีแถว `MOBS` + 2 เป็น leader 0 = 7 ครบทุกแถวมีเหตุผลชื่อจริง) · 🔴 **คำสั่งของ COO ในใบนั้นระบุตรง ๆ ว่า `GT-131` คง PENDING เป็นงานค้างของ BUILD-001 ชั้นสายตา และ "ห้ามเคลมปิดทั้งใบจนกว่า GT-131 ผ่าน"** ⇒ ใบนี้ยังต้องรัน · 🔴 **เลข 115 ยังเป็นเป้าที่พิมพ์บนคอนโซลทั้งสองจุด** (`assembled=108/115`, `ceiling=108/115`) ไม่มีที่ไหนเขียนว่าเป้าคือ 108 — ผู้เทสที่เห็น 108 บนจอ **อย่าอ่านว่าเป้าถูกลด** · ใบชั้นสายตาของ 7 รูคือ `GT-151` (คนละใบ ปิดแทนกันไม่ได้)]

> **LANE-A รอบ `pqx4fj`** (2026-08-28) จอง `GT-131` (ตัวนับร่วมกับ `CLIENT_RE_QUEUE.md` · grep ก่อนจอง = 0 hit ·
> สูงสุดก่อนหน้า `GT-129`/`RE-130`) · ไม่แทนที่ใบใด ใบเก่าอยู่ที่เดิม

### ที่มา
bg0001 ส่ง placement 115 ตัวโดยใส่ **เลข Mob-Set ของไฟล์ฉาก (1..113)** ลงช่องที่ไคลเอนต์อ่านเป็น `MOBS.n_ID`
⇒ `GT-078` = "ตำแหน่งถูกทุกตัว NPC ผิดทุกตัว" · `RE-128` เจอตารางแปลงของไคลเอนต์เอง `CONSTDATA_TH__CLINE`
คีย์ (`n_CLINE_TYPE=1` ผ่าน `SCENE_NAME`, `n_CREATURE_TYPE`=เลข Mob-Set) -> `n_LEADER_BK1` = `MOBS.n_ID` ตัวจริง ·
รอบนี้ต่อสายแล้ว **ไม่มีแฟล็ก ทุกบูต**: actor ถือ n_ID ที่ resolve + `s_OUTFIT` ของแถวนั้น + ชื่อจาก `MOBS_TIP`
🔴 **7 placement ว่างโดยตั้งใจ** (index `0,75,86,87,145,147,148`) -- resolve ได้ id ที่ไม่มีแถวใน MOBS
(`155,819,9107,937,942`) หรือได้ `0` ⇒ เลนนี้ไม่เดา · index 0 = จุดบนท่าเรือข้าง Columbus ·
**ว่างคือของถูก ห้ามรายงานเป็น regression**

### objective
บนบูตไร้แฟล็ก ชื่อที่ไคลเอนต์แสดงให้ NPC ของ bg0001 = แถว `MOBS` ที่ resolve ผ่าน CLINE ใช่หรือไม่

### คำทำนาย (ผิด = ผล ไม่ใช่ความล้มเหลว) · P1/P2 คือสมอของเจ้าของเอง (`PANYA-DECISION 2026-08-27 09:50`)

| # | placement | เคยเห็น | ต้องเห็นรอบนี้ (n_ID) | ที่สังเกต |
|---|---|---|---|---|
| P1 | 1 | `Sebastian` | `Columbus / Marine Transport Station` (156) | ท่าเรือ ข้างเรือลำใหญ่ |
| P2 | 65 | `Columbus` | `Loie / Royal Navy Engineer` (802) | ข้างปืนใหญ่ฐานแดง |
| P3 | 4 | -- | `Hields / Guild Administrator` (159) | ลานดอกไม้+ม้านั่ง 2 ตัว · **คู่ของเขา (placement 59) ยังเป็น `Toxic Vine` ดูแถบแดงข้างล่าง** |
| P4 | 3 / 90 | -- | `Dorothy` (158) **ไม่มีบรรทัดตำแหน่ง** / `Melody / Grocer` (903) | -- |
| P5 | 91 | -- | `Chalais / Illustrations Appraisers` (904) | คู่ของเขาคือ placement 30 ซึ่ง **ยังเป็น `Tornado Eagle`** (แถบแดงข้างล่าง) |

🔴 **13 placement ที่ยัง "ชื่อผิด" อยู่ และนั่นคือของถูกในรอบนี้ ห้ามรายงานเป็น FAIL:**
`12, 30, 33, 58, 59, 60, 63, 95, 103, 105, 107, 109, 132` — `runtime.py` splice โรสเตอร์ศัตรูของ
สาย B (`field_mob_tables.py` ซึ่งยัง generate ด้วยกฎเก่า) ทับ census หลังจากสาย A ประกอบเสร็จ
⇒ **95 จาก 108 ตัวได้ชื่อใหม่ · 13 ตัวยังเป็นของเดิม** · ยกให้สาย B แล้วในจดหมาย
`20260828_2305_LANE-A-STATUS-runtime-splice-*` · **ถ้าผู้เทสเห็น 13 จุดนี้เป็นชื่อเก่า = ตรงตามคาด**
ถ้าเห็น **จุดอื่นนอก 13 นี้** เป็นชื่อเก่า = **นั่นคือของจริงที่ต้องรายงาน**

- **P6 [สัญญาณเดี่ยวที่แรงที่สุด]** หน้าต่างแผนที่ (`M`) ลิสต์ "find character in scene" ต้องเรียงตาม n_ID
  `156,157,158,...` แบบในวิดีโอเจ้าของ -- ด้วย id ชุดเก่า ลิสต์นี้ถูกไม่ได้เลย · กด `GO!` หนึ่งแถวแล้วจดผลที่เห็น
- **P7** 7 จุดข้างบน **ว่าง** ยืนยันด้วยตา (จุดไหนเดินไม่ถึง เขียนว่าไม่ได้ตรวจ ห้ามเดา)
- **P8** `n_ID 917` ไม่มีแถว `MOBS_TIP` ⇒ actor หนึ่งตัวไม่มีบรรทัดชื่อโดยชอบธรรม -- จด ไม่ใช่ข้อบกพร่อง
- **P9 [ตัวหักล้าง ค่าเท่ากับ PASS]** ชื่อยังเป็นชุดเดิม/ยังเห็นชื่อมอนที่ 30 ทั้งที่คอนโซลขึ้น `identity=CLINE:108 shipped`
  ⇒ ไคลเอนต์ไม่ได้ใช้ id ที่เราส่งตัดสินชื่อ ⇒ redirect กลับ `RE-128` (static) **ไม่ใช่เปิดใบเทสใหม่**

### server args (เป๊ะ -- "ไม่มีแฟล็ก" คือส่วนหนึ่งของสิ่งที่ทดสอบ)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt131.sqlite3
```
client `-SecondPasswordMode bypass` · 🔴 ห้ามมี `--*-scenario` / `--world-census-actors` / `--export-events` แม้ตัวเดียว
ก่อนบูต: `pf_resolve_green_boot.py --fetch` (เอาเฉพาะ exit 0 + `BOOT_COMMIT`) แล้ว
`git grep -n "identity_resolved" <SHA> -- src/pirateforce_foundation/` · 0 hit = `<SHA>` เก่ากว่างานรอบนี้ ⇒ fetch ใหม่

### ขั้นตอน (~25-35 นาที · อัดวิดีโอต่อเนื่องทั้งช่วง `LOCK_GAME`)
1. ของมาตรฐานทั้งหมดตาม `ATTENDED_SESSION_RUNBOOK.md` (LOCK · สำเนา DB · `CANON_SHA` ก่อน-หลัง ·
   เซิร์ฟเวอร์ก่อนไคลเอนต์ · teardown ภายใน 420 นาที · กฎสีป้ายชื่อ · หลักฐานครบทุกข้อ)
2. เข้าเกม -> T0 ภาพนิ่ง full-res + HUD X/Y -> NO-CRASH ด้วย **right-click-drag** (🔴 ห้าม `Q`/`E`)
3. 🔴 **ห้ามพิมพ์ตัวอักษรใด ๆ** ยกเว้นกด `M` ในข้อ 5
4. เดินทัวร์ `W/A/S/D` ตามลำดับ ถ่ายภาพนิ่ง full-res + HUD X/Y ทุกจุด: ท่าเรือ (1 และจุดว่าง 0) ·
   ลานดอกไม้ (4, 59) · (3, 90) · (30, 91 ให้อยู่เฟรมเดียวกันอย่างน้อยหนึ่งภาพ) · ปืนใหญ่ฐานแดง (65)
   · ทุกจุดจด **ชื่อ/บรรทัดตำแหน่งที่อ่านได้จริง ตัวอักษรเป๊ะ** (ไม่มี = เขียน "none")
5. กด `M` -> ถ่ายลิสต์ให้อ่านออกทั้งลิสต์ -> จด 10 แถวแรก -> กด `GO!` หนึ่งแถว -> ถ่าย/จดผล
6. NO-CRASH ซ้ำ -> ออกจากเกม -> 🔴 restart เซิร์ฟเวอร์ก่อนบูตถัดไป -> teardown
เฉพาะใบนี้: เก็บ `state\run_gt131.sqlite3` ไว้ให้ chief re-derive · บรรทัด `WORLD_CENSUS` ให้ **คัดลอกตัวอักษร ไม่ใช่ถ่ายรูป**

### pass criteria (สองชั้น แยกกัน ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
**wire/DB** -- grep stdout+stderr รวมกัน (`2>&1`) ด้วย `WORLD_CENSUS` ต้องได้บรรทัดที่มีครบ:
`assembled=108/115` · `wire=108` (ไม่ใช่ `MISMATCH`) · `bodies=ok` · `source=identity_resolved` ·
`shortfall=identity_resolved=108` · ลงท้าย `identity=CLINE:108 shipped,7 unresolvable`
🔴 เห็น `115` ตรงไหนบนบรรทัดนั้น = การเปลี่ยน identity ไม่ทำงานในบูตนั้น ⇒ จดทั้งบรรทัด ·
`sessions` +1 · `max(lease_generation)` ไม่ถอย · `integrity_check`=`ok` · sha canonical ตรงก่อน-หลัง
**client-observable** -- P1 **และ** P2 ถูกทั้งคู่บนภาพนิ่ง (แกนของการตรวจรับ) · P3/P4/P5 ตรงตาราง
รวม Dorothy ที่ไม่มีบรรทัดตำแหน่ง · P6 ลิสต์ `M` เรียงตาม n_ID · P7 จุดว่างว่างจริง · NO-CRASH ผ่านสองครั้ง

### nonclaims (ติดไปกับผลทุกกรณี)
1. 🔴 ไม่อ้างว่าไคลเอนต์อ่าน CLINE เอง (nonclaim ที่ยังเปิดของ `RE-128`) -- ใบนี้ตอบชั้น client-observable:
   ชื่อบนจอถูก = id ที่เราส่งถูก ไม่ว่าไคลเอนต์อ่านจากตารางไหน
2. 🔴 ไม่อ้างว่าร่าง/โมเดลถูก เกินกว่า "ใช้ `s_OUTFIT` ของ id ที่ resolve ได้" -- **ร่างผิดแต่ชื่อถูก = จด ไม่ใช่ FAIL**
3. `n_ID 910` (Saben) มี `s_OUTFIT` เป็น **รายการหลายตัวคั่นด้วย `;`** สาย A ส่ง **ตัวแรก** เพราะส่งทั้งสตริง
   = ชื่อไฟล์ที่ไม่มีจริง ⇒ ไม่มีร่าง · **ถ้า Saben หน้าตาไม่เหมือนของเดิม = จด ไม่ใช่ FAIL** [สมมติของสาย A - รอ COO ยืนยัน]
4. ไม่อ้างอะไรเรื่อง hp / aggro / เควสต์ / แหล่งแพ็กเก็ตของลิสต์ในหน้าต่างแผนที่
5. ไม่ปิด `GT-078` แทนเจ้าของ ไม่ประกาศ milestone ใด ไม่ใช้สถานะ GM
6. ไม่ชี้สาเหตุของสีป้ายชื่อ (`RE-067` เปิดอยู่) · ผู้เทสคนเดียว บูตเดียว

**ผู้เปิดใบ: LANE-A (รอบ `pqx4fj`)** -- ผลกลับมาที่สาย A บริโภค

### result (ผู้เทสกรอก)
```

```
---

## GT-134 BG0015-FIRST-EYES-001 [attended, in-game]: เกาะภูเขาไฟนรก `Bg0015` (scene 14) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  ~~[BLOCKED]~~ ~~[READY]~~ **[PASS]**

> 🆕 **ปิดหัวใบ R260(sm51i5) 2026-08-31 (chief แทนสาย A ที่เป็นเจ้าของใบ):** เทสจริงผ่านแล้วตั้งแต่ 2026-08-30T17:1x+07:00
> ผล `notes_to_chief/20260830_1731_GT127-GT134-RESULT-both-PASS-chat-door-open-and-first-eyes-on-hell-volcano.md`
> (`OBSERVER_CONFIRMED` · `BOOT_COMMIT 57490434` = main HEAD ไร้แฟล็ก) — พบว่าหัวใบยังค้าง `[READY]` โดยไม่มีใครปิด
> จาก `notes_to_chief/20260831_0909_KA1A-NOTE-*.md` (กะ1-A, ใบที่หกของปัญหานี้ในสัปดาห์นี้) แก้เฉพาะหัวใบ ไม่แตะเนื้อใบ/เกณฑ์เดิม
> `RECHECK:` ใบนี้ปิดแล้ว ไม่ต้องบูตซ้ำ — ถ้าจะยืนยันซ้ำให้ค้นหา `OBSERVER_CONFIRMED` ในผลข้างต้นแทนการบูตใหม่

> 🟢🟢 **B2 ปิดแล้ว · ใบนี้ `[READY]` · 2026-08-30T00:4x+07:00 (LANE-A รอบ `vvy6q7`)**
> `COO-DECISION 20260829_2342` (ตอบใบ `ASK-COO 20260829_2240` ของสายนี้) **เคาะว่า "เปิดได้"**
> ⇒ รอบนี้พลิก `login_entry_allowed` ของฉาก 14 เป็น `true` ใน `scenarios/world_scene_registry_001.json`
> **และปิด `D3` ในคอมมิตเดียวกัน** (ไม่ได้ปล่อยให้เปิดค้างอย่างที่ใบ COO ยอมให้ทำได้)
> 🔴 **ห้ามบูตจนกว่าจะเห็น merge sha ของ `pirate-force-server#290` บน main** — ก่อนหน้านั้นประตูยังปิดจริง
> **สองบรรทัดที่ใบ COO บังคับให้มีก่อนใบรันได้ อยู่ในหัวข้อ `เกณฑ์` ข้างล่างแล้วทั้งคู่**

> 🔴🔴 **บรรทัดที่ผู้เทสต้องอ่านก่อนตัดสิน PASS/FAIL — เงื่อนไขข้อ 1 ของ `COO-DECISION 20260829_2342`:**
> **"มอนไม่ก้าวร้าว / ไม่อ่านว่าเป็นศัตรู = อาการของ `D3` ที่คาดไว้แล้ว ไม่ใช่ `FAIL` ของใบนี้"**
> คำถามของใบนี้คือ ***มีสิ่งมีชีวิตขึ้นจอไหม*** ไม่ใช่ ***มันตีเราไหม***
> 🔴 และ **แม้รอบนี้จะปิด `D3` ไปแล้ว บรรทัดนี้ยังยืน ไม่ถอน**: สิ่งที่รอบนี้ทำคือ**ส่งไบต์ faction ออกไป**
> — **ไม่มีใครเคยเห็นว่าไคลเอนต์เรนเดอร์คู่ faction ในฉากนี้ออกมาเป็นอะไร** เพราะไม่เคยมีใครยืนในฉาก 14
> ⇒ ถ้ามอนขึ้นจอแต่ไม่ก้าวร้าว = **ยังเป็น PASS ของใบนี้** และเป็นข้อมูลชิ้นใหม่ให้ใบถัดไป

> 🔴 **`D3` ปิดในรอบเดียวกัน — แต่ผู้เทส "ตรวจไม่ได้ด้วยบรรทัดเดียว" อ่านสองย่อหน้านี้ให้ครบ**
> ตัวคุมคือ `src/pirateforce_foundation/world_faction_admission.py`: ฉากที่ registry ประกาศเปิด **และ** `n_SAVE = 1`
> วันนี้ = `{1, 2, 14}` · ฉาก 278/997 ไม่เข้าเพราะ `n_SAVE = 0`
>
> 🔴🔴 **แก้คำแนะนำของตัวเองก่อนออกจาก draft (`pf-adversary` D3 + D4) — ฉบับแรกของบล็อกนี้ผิดสองที่:**
> **(ก)** ผมเขียนให้ผู้เทส grep หาบรรทัด `WORLD_FACTION_ADMISSION scenes=1,2,14`
> **บรรทัดนั้นไม่มีวันขึ้น** — `console_line()` ของโมดูลผม **ไม่มีใครเรียก** (จุดเรียกต้องอยู่ใน `runtime.py` ของ chief)
> ⇒ **ลบข้อแนะนำนั้นทิ้ง อย่าไปหา ไม่เห็นไม่ใช่ความผิดของใคร**
> **(ข)** บรรทัด `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` **ไม่มีเลขฉากอยู่ในนั้น**
> ⇒ มัน**ขึ้นเหมือนกันเป๊ะตอนล็อกอิน Port Royal ปกติ** และขึ้นแม้ในบูตที่ผิดแฟล็ก
> ⇒ **ห้ามใช้บรรทัดนี้บรรทัดเดียวสรุปว่า "ฉาก 14 ได้ faction แล้ว"** มันแยกไม่ออกจากการยืนอยู่ที่ท่าเรือ
>
> **สิ่งที่ผู้เทสทำได้จริง:** ตัวยืนยันว่า "อยู่ฉาก 14 จริง" คือ `WORLD_CENSUS_BG0015 assembled=81/91`
> (มีเลขฉากในตัว) ⇒ **ถ้าเห็นบรรทัดนั้น *และ* เห็น `PLAYER_FACTION` ในบูตเดียวกัน = `D3` ทำงาน**
> เห็น `PLAYER_FACTION` แต่**ไม่**เห็น `WORLD_CENSUS_BG0015` = **บูตผิด** กลับไปอ่าน precondition
> 🔴 **ไม่เห็นบรรทัด `PLAYER_FACTION` = ให้จดไว้และรายงาน แต่ไม่ใช่ FAIL ของใบนี้** (เกณฑ์ PASS ยังเป็นตาเห็น)

> **LANE-A รอบ `w0pu2i`** (2026-08-28 · milestone M3 · สั่งโดย `COO-DECISION 2026-08-28T22:50+07:00`
> "M2 stays paused, M3 walks without that door")
> NUMBERING: จอง `GT-132` ตอนต้นรอบ (grep = 0 hit ทั้งสองไฟล์ · สูงสุดตอนนั้น `GT-131`/`RE-130`)
> แต่ระหว่างรอบ **สาย B merge `GT-132` และสาย GM merge `GT-133`/`RE-132` เข้า main ก่อน**
> ⇒ ตามกฎ "ชนแล้วห้ามทับ" ใบเหล่านั้นอยู่ที่เดิม ใบนี้ขยับเป็น **`GT-134`** · ไม่แทนที่ใบใด
> 🔴 **BLOCKED โดยตั้งใจ ห้ามบูตจนกว่าจะเคลียร์ทั้งสองข้อในหัวข้อ blockers** -- บูตก่อนนั้นได้ FAIL ปลอม

> 🔴 **แก้ข้อเท็จจริง 2026-08-29T02:3x+07:00 (LANE-A รอบ `02k3w5` · เจ้าของใบแก้หัวใบตัวเอง):**
> ประโยค "รอบนี้ลงสองไฟล์ของสาย A" ข้างล่าง **เป็นจริงในระดับ commit เท่านั้น ไม่ใช่ระดับ main**
> PR `pirate-force-server#217` ของรอบ `w0pu2i` ถูก `merge-claude-pr.yml` ปิดทิ้งเพราะ job `gate` แดง
> (cp874 tripwire · `tools/pf_runtimeres_actor_entry_static.py:911` · `U+00B7` ที่รอบนั้นเขียนเอง)
> ⇒ ทั้ง `world_bg0015_identity.py` และ `world_population_bg0015.py` **ไม่เคยขึ้น main**
> รอบ `02k3w5` กู้กลับมาแล้ว (PR **#220**) แก้ต้นเหตุ เทสเต็มเขียว 4096 passed / 328 skipped / 0 failed
> ⇒ **ก่อนบูตใบนี้ ต้องเห็น merge sha ของ #220 บน main ก่อนเสมอ**

> ✅ **merge sha ที่ว่านั้น มาแล้ว 2026-08-29T03:34+07:00 (LANE-A รอบ `uajlve` · เจ้าของใบยืนยันเอง):**
> `#220` merged เป็น **`14e99bbd0e091a966a9988e3f430ea1cdb854281`** (commit งานจริง `77640cc`)
> `git fetch origin main` รอบนี้เห็นไฟล์ทั้งสองบน main จริง ⇒ **เงื่อนไข "ต้องเห็น merge sha" ข้างบนเคลียร์แล้ว**
> 🔴 แต่ **B1 ยังไม่เคลียร์** -- กิ่ง census ของ scene 14 ใน `runtime.py` ยังไม่มี
> chief ตอบใบ `CORE-REQUEST` แล้ว (`notes_to_chief/20260829_0103_CHIEF-REPLY-LANE-A-bg0015-*`)
> ว่าติดอยู่ที่ "โมดูลยังไม่อยู่บน main" ข้อเดียว และจะวางกิ่งให้ **ในรอบถัดไปของ chief เลย**
> สาย A ส่ง sha กลับไปแล้วรอบนี้ (`notes_to_chief/20260829_0334_LANE-A-REPLY-CHIEF-bg0015-*`)
> ⇒ ใบนี้ยัง `[BLOCKED]` จนกว่ากิ่งจะลง main · **ห้ามบูตเพราะเห็นบรรทัดนี้**

> ~~✅ **B2 ปิดแล้ว 2026-08-29T04:4x+07:00 (LANE-A รอบ `vyi2ud`)**~~ **ปิดครึ่งเดียว — แก้ 05:2x
> ในรอบเดียวกัน ก่อน PR ออกจาก draft (ขีดฆ่าไม่ลบ)** · ฉาก 14 **เข้าทะเบียนแล้วจริง**
> (สเปกฉาก · จุดเกิดจาก `MARKER[14]` ของไคลเอนต์เอง · native digest) แต่ **ประตูล็อกอินถูกปิดกลับ**
> (`login_entry_allowed: false`) หลัง `pf-adversary` วัดได้สามอาการของการเปิดมัน — ดู blockers ข้างล่าง
> 🔴 **B1 และ B2 ยังเปิดทั้งคู่ ⇒ ใบนี้ยัง `[BLOCKED]`** — ยังห้ามบูต

> 🔴 **ใบนี้รับภาระเพิ่มอีกหนึ่งข้อ 2026-08-29T07:39+07:00 (LANE-A รอบ `8ubiku` · เจ้าของใบเติมเอง)
> — สั่งโดย `COO-DECISION 20260829_0542` ข้อ 3 และ §ใครทำอะไรต่อ:**
> ใบนี้คือ **การพิสูจน์ชั้นแรกของกฎจุดเกิดจากตาราง `MARKER`** ที่เพิ่งเป็นกฎถาวรของโปรเจกต์
> จุดเกิดฉาก 14 `(-17513, 18989, 1894)` มาจาก `MARKER[14]` ⇒ ชั้นหลักฐาน **`authored` เท่านั้น**
> "นักออกแบบแมพเขียนพิกัดนี้ไว้" ไม่ใช่ "มีใครเคยยืนตรงนี้" — ยังไม่เคยมีไคลเอนต์ยืนบนจุดนี้เลย
> ⇒ **เกณฑ์ที่ผู้เทสต้องดูเพิ่ม หนึ่งบรรทัด:** ตอนโผล่เข้าฉาก **ยืนอยู่บนพื้นที่ยืนได้หรือไม่**
> 🔴 **ถ้าผู้เทสโผล่ในหิน ในลาวา ใต้พื้น หรือตกทะลุแมพ = กฎ marker ตกทันที** (คำของ COO เอง)
> ไม่ใช่แค่ใบนี้ FAIL แต่สาย A ต้องย้อนกฎตามข้อ ④ ของใบ `20260829_0447` โดยไม่ต้องถาม COO ซ้ำ
> ⇒ ถ้าเกิดกรณีนี้ **ถ่ายภาพหน้าจอ + จดพิกัดที่ UI แสดง** เป็นหลักฐานชั้น client-observable
> ✅ ถ้ายืนบนพื้นได้ปกติ = จุด marker จุดแรกที่ถูกยืนยันด้วยตา และเป็นทางเดียวที่จะเลื่อนชั้น
> จาก `authored` เป็น `confirmed` ได้ (`COO-DECISION 20260828_2250` ยังบังคับ ใบ 0542 ไม่ได้ยกเลิก)
> **หมายเหตุ:** เกณฑ์นี้ **ไม่** ทำให้ใบนี้บูตได้เร็วขึ้น — B1/B2 ยังเปิด ยังห้ามบูต

> 🟢 **B1 ปิดแล้ว 2026-08-29T22:4x+07:00 (LANE-A รอบ `ga91m5-r2` · เจ้าของใบปิดเอง · ขับ dispatcher จริง)**
> B1 เคยอ่านว่า "กิ่ง census ของ scene 14 ใน `runtime.py` ยังไม่มี" — **ไม่ต้องมีแล้ว และจะไม่มีวันมี**:
> chief สร้าง **จุดเสียบสำมะโนต่อฉาก** ในรอบ `73fhoc` (`lane_hooks.census_composer(scene_id)`
> + call site เดียวใน `runtime.py`) แทนการเพิ่ม `elif` รายฉาก ⇒ สาย A ลงทะเบียนเองได้โดยไม่ต้องมีรอบ chief คั่น
> รอบนี้ลง `src/pirateforce_foundation/lane_hooks/lane_a_scene_census.py` แล้ว **ฉาก 14 มีสำมะโนของตัวเอง**
> วัดจริงด้วยการเปิดคีย์ประตูใน registry **ฉบับชั่วคราว** (ไม่ commit) แล้วขับ dispatcher จริง:
> ```
> LANE_HOOK_FIRED ... scene_census_composer:14
> WORLD_POP_HANDOFF scene=14 kind=census actors=81 wire=81 pc=14866B frame=14879B
> WORLD_CENSUS_BG0015 assembled=81/91 shippable=81 wire=81 bodies=ok source=bg0015_full_roster
> actions: WORLD_CENSUS_LANE_SCENE14_INITIAL_81 / _REAPPLY_81   (คอนโซล 93 บรรทัด)
> ```
> 🔴 **B2 (ประตู) ยังเปิด ⇒ ใบนี้ยัง `[BLOCKED]` ยังห้ามบูต** — เหลือคำเคาะเรื่อง **D3** ข้อเดียว:
> บน registry จริง ล็อกอินฉาก 14 ยังถูกปฏิเสธ `WORLD_SCENE_ENTRY_REFUSED [scene_not_allowed_at_login]`
> `teleport_sent=False` ⇒ สาขาสำมะโนไม่ถูกแตะเลย (วัดแล้ว มีเทสพิน)
> เหตุที่ประตูยังปิดคือ **D3 เท่านั้น**: `player_wire` ปฏิเสธ faction-1 ทุกฉากนอก `(1, 2)`
> ⇒ ฉาก 14 ไม่มีเฟรม `PLAYER_FACTION` ⇒ มอน 81 ตัวอาจ **ขึ้นจอแต่ไม่อ่านว่าเป็นศัตรู**
> ⇒ คำถามนี้ส่ง COO แล้ว (ตอบแล้ว, archived R259): `archive/notes_to_chief_2026-08-28_29_lane-a-backlog5-closed/20260829_2240_LANE-A-ASK-COO-scene-14-door-has-one-blocker-left.md`
> 🔴 **แก้คำอ้างของตัวเองในรอบเดียวกัน (pf-adversary วัดให้ดู):** ฉบับแรกของบล็อกนี้เขียนว่า
> "เหลือกุญแจดอกเดียว" — **ผิด** · `resolve_entry` ปฏิเสธฉาก 14 เฉพาะทาง `via_login=True`
> เรียกด้วย `via_login=False` มัน resolve ได้ตั้งแต่วันนี้ และ `CORE-REQUEST-GM-038` ของสาย GM
> กำลังขอ chief สร้างจุดเรียกแบบนั้นพอดี ⇒ **เคยมีสองกุญแจ และดอกที่สองอยู่ในใบของสายอื่น**
> แก้แล้วด้วยโครงสร้าง: composer ของสาย A มี **ด่านรับเข้า** ถาม registry ทุกครั้งว่าฉากเปิดหรือยัง
> ⇒ ทุกเส้นทางได้ `None` เหมือนกันหมด ⇒ boolean ใน registry กลับมาเป็นกุญแจดอกเดียวจริง ๆ
> **ถ้า COO เคาะว่าเปิดได้ทั้งที่ D3 เปิด** ⇒ สาย A พลิก boolean เดียวและใบนี้บูตได้ทันที
> และผู้เทสต้องอ่านเพิ่มหนึ่งบรรทัด: **"มอนไม่ก้าวร้าว/ไม่อ่านว่าเป็นศัตรู = อาการของ D3 ที่คาดไว้แล้ว
> ไม่ใช่ FAIL ของใบนี้"** — คำถามของใบนี้คือ *มีสิ่งมีชีวิตขึ้นจอไหม* ไม่ใช่ *มันตีเราไหม*


> 🟢 **PANYA-ORDER ข้อ ④ (จุดเกิดต้องใกล้ object) ใบนี้ผ่านอยู่แล้ว โดยไม่ต้องย้ายจุดเกิด
> — วัดใหม่ 2026-08-29T10:5x+07:00 (LANE-A รอบ `i8timv` · เจ้าของใบวัดเอง):**
> คำสั่งเจ้าของ `20260829_0930_PANYA-ORDER-*` ข้อ ④ บังคับทุกโหมด: ใบที่เกี่ยวกับ world object/NPC/monster
> ตัวละครต้องเกิด "ใกล้ ในระยะ หันหน้า และยืนเยื้อง object เล็กน้อย" · **ใบนี้ชนกับข้อ ④ ตรงหน้า**
> เพราะจุดเกิดของใบนี้ถูกบังคับให้เป็น `MARKER[14]` เป๊ะ ๆ (มันคือ object ที่ใบนี้กำลังทดสอบเอง)
> จะ seed ไปข้าง ๆ มอนแทนไม่ได้ — ย้ายเมื่อไรก็เลิกพิสูจน์กฎ marker ทันที
> **แต่วัดแล้วไม่ต้องเลือก:** จาก `MARKER[14]` `(-17513, 18989, 1894)` ไปหา 81 placement ที่ส่งจริง
> (`world_bg0015_identity.shippable_placements()` — ผ่าน API ของโมดูล ไม่ใช่อ่าน tuple ดิบ)
> - **ใกล้ที่สุด: `placement_index 2` = `Siren` เลเวล 110 ที่ `(-17206.6, 19632.4, 1952.3)`
>   ห่าง 712.6 หน่วยในแนว XY · 715.0 หน่วยสามมิติ · สูงกว่าจุดเกิด 58.3 หน่วย**
> - รองลงมา `placement_index 5` `Walking undead` 2339.7 · `placement_index 1` `Columbus` 2852.2
> - **มี 3 ตัวที่ส่งจริงอยู่ในรัศมี 3000 หน่วย XY** จาก 81 ตัว
> ⇒ ผู้เทสที่โผล่ที่ `MARKER[14]` มีสิ่งมีชีวิตตัวหนึ่งอยู่ห่าง ~713 หน่วย **โดยไม่ต้องเดินหา**
> เทียบมาตราส่วนที่โปรเจกต์นี้มีอยู่: ระยะบ้านฉาก 1 ถึง `MARKER[1]` = 2340 หน่วย ซึ่งเอกสารเดิมเรียกว่า "ไกล"
> 🔴 **สิ่งที่ยังไม่รู้และห้ามเขียนว่ารู้:** 713 หน่วยอยู่ในกล้องหรือไม่ **ยังไม่มีใครวัด** — ไม่มีรอบไหน
> ในประวัติโปรเจกต์เคยยืนในฉากนี้ ⇒ ใบนี้คือรอบแรกที่จะตอบ **ให้ผู้เทสจดว่าเห็นหรือไม่เห็น**
> ถ้าหันกล้องรอบตัวแล้วไม่เห็นอะไรเลย = ข้อมูลชิ้นใหม่เรื่องระยะกล้อง ไม่ใช่ FAIL ของกฎ marker
> **ไม่เปลี่ยนสถานะใบ** — `[BLOCKED]` ตามเดิม B1 ยังเปิด (กิ่ง census ฉาก 14 ใน `runtime.py` เป็นของ chief)

> 🔴🔴 **ข้อห้ามที่วัดแล้ว ไม่ใช่ข้อควรระวัง — เพิ่มโดย LANE-A รอบ `ucaybn` 2026-08-29T23:3x+07:00
> (`pf-adversary` ข้อ D8) · เซิร์ฟเวอร์ห้ามรันด้วย `--second-password-mode bypass`
> และห้ามมีแฟล็ก `--*-scenario` ใด ๆ:**
> `runtime.py:944` `world_census_enabled = (not active_lanes and second_password_mode == "required")`
> เป็นทั้งเงื่อนไขแรกของกิ่งสำมะโนต่อสาย **และ** ตัวปลดอาวุธ dispatcher เดิม `v141:4292`
> ⇒ บูตแบบ opt-in จะ **ไม่เรียกสำมะโนฉาก 14 เลย** แล้วส่ง `V134_P0_P30_P91_ISOLATED`
> = placement bg0001 สามตัว พิกัด Port Royal `population_indices=(0, 30, 91)` เข้าไปในฉาก 14 แทน
> ⇒ ผู้เทสจะเห็น **3 ร่าง โดยไม่มีบรรทัด `WORLD_CENSUS_BG0015` เลย** แล้วรายงาน FAIL ปลอม
> ขับจริงแล้วทั้งสองทาง (บูตไร้แฟล็ก = `WORLD_CENSUS_LANE_SCENE14_INITIAL_81` · บูต bypass = สามตัว)
> 🔴 `-SecondPasswordMode bypass` ของ **ไคลเอนต์** ยังใช้ตามเดิม — คนละตัวกับแฟล็กเซิร์ฟเวอร์
> args เซิร์ฟเวอร์ที่ระบุไว้ในใบนี้ถูกอยู่แล้ว บรรทัดนี้กันไม่ให้ใครเติมแฟล็กเข้าไปเอง

> 🔴 **บันทึกการชนกันของสองรอบ (LANE-A `ucaybn` · 23:3x):** สองเซสชันของสาย A เดินรอบพร้อมกัน
> โดยไม่เห็นกัน — `ga91m5-r2` (บล็อกข้างบน) กับ `ucaybn` · ต้นรอบ `ucaybn` ตรวจแล้วไม่มี PR
> หัวข้อ `[LANE-A]` เปิดค้างเลย จึงยึดล็อกและทำงาน · `ga91m5-r2` merge ก่อน
> ⇒ ตามกฎ **"ชนแล้วห้ามทับ"** ฉบับที่อยู่บน main คือของ `ga91m5-r2` และ **`ucaybn` ไม่ทับ ไม่แทนที่**
> ~~บล็อก B1 ของรอบ `ucaybn` ที่เคยอยู่ตรงนี้ พร้อมเงื่อนไข "merge sha ของ PR รอบ ucaybn"~~
> **ถอนแล้ว** — B1 ปิดโดย `ga91m5-r2` ซึ่ง merge ไปแล้วจริง เงื่อนไขของ `ucaybn` ไม่มีความหมาย
> สิ่งที่เหลือจากรอบ `ucaybn` บนใบนี้คือข้อห้ามแฟล็กข้างบน ซึ่งเป็นของใหม่และวัดแล้ว

### ที่มา
`Bg0015` = `SCENE_NAME.n_ID 14`, `s_MODLE_ID Bg0015`, 91 native placements, `n_SCENE_LV=100`
🔴 **ไม่เคยมีใครในโปรเจกต์นี้เข้าฉากนี้** -- ทุกบูตในประวัติศาสตร์ `scene_id` = 1 เสมอ
⇒ ฉากนี้ยัง **ไม่มีหลักฐานชั้น client-observable ใด ๆ เลย** และนั่นคือเหตุผลเดียวที่ใบนี้มีอยู่
รอบนี้ลงสองไฟล์ของสาย A: `world_bg0015_identity.py` + `world_population_bg0015.py`
ฉากนี้มี selector **ตรง** (`n_CLINE_TYPE = 14` ไม่ใช่ `0xFFFFFFFF` แบบที่ ~~240~~ **252** ใน 271 ฉากถือ
— นับใหม่จาก `CONSTDATA_TH__SCENE_NAME.tsv` 2026-08-29 โดยสาย A รอบ `02k3w5`: 271 แถว · 252 ถือ `0xFFFFFFFF`
· **19 ถือ selector ตรง** ซึ่งตรงกับเลข 19 ที่ `world_bg0015_identity` อ้างอยู่แล้ว · เลข 240 เดิมขัดกับเลข 19
ในประโยคเดียวกันมาตลอด ขีดฆ่าไม่ลบ) ⇒ ตามผลที่สอง
ของ `RE-128` (23:14 · PASS/DONE) crosswalk คือ `CLINE[(14, เลข Mob-Set)].n_LEADER_BK1` -> `MOBS.n_ID`
-> `s_OUTFIT` + ชื่อจาก `MOBS_TIP` · 41 จาก 51 ชุด resolve ได้ · **81 จาก 91 placement ลงสาย**

### objective
บูตเดียว หนึ่งข้ออ้าง: **ในฉาก 14 ผู้เล่นมองเห็น actor ที่มีชื่อตามสำมะโน ยืนอยู่ตามพิกัดที่ส่งไป จริงหรือไม่**

### 🔴 nonclaim ที่ต้องอ่านก่อนตัดสิน PASS/FAIL (เพิ่ม 2026-08-29T03:34+07:00 รอบ `uajlve`)
ใบนี้ยืนยันได้อย่างเดียวว่า **"มีร่างยืนอยู่จริงและอ่านชื่อได้"** -- **ไม่ยืนยันว่าโต้ตอบกับร่างพวกนั้นได้**
ที่มา: `notes_to_chief/20260829_0103_CHIEF-REPLY-LANE-A-*` และผล attended `20260829_0018_KA3A-*`
วัดไว้แล้วบน `bg0001` ว่า **คลิกซ้ายบน hostile placement ถูกเซิร์ฟเวอร์ตอบด้วยเลนคุย NPC**
(`V98_NPC_CONVERSATION_DEFAULT_*`) ⇒ ได้หน้าต่างบทสนทนาเปล่า ไม่เข้าโหมดโจมตี
⇒ ถ้าผู้เทสคลิกแล้ว "ไม่มีอะไรเกิดขึ้น" **นั่นไม่ใช่ FAIL ของใบนี้** เป็นบั๊กคนละใบที่มีอยู่ก่อนแล้วบน bg0001
เกณฑ์ PASS ของใบนี้อยู่ที่ **ตาเห็น + ชื่อบนป้าย + พิกัด** เท่านั้น · การคลิกไม่อยู่ในเกณฑ์

### 🔴 blockers (ต้องเคลียร์ครบก่อนเปลี่ยนสถานะเป็น READY)
- **B1 -- `runtime.py` ยังไม่มีกิ่ง census ของ scene 14** · dispatch เป็น if/elif บนเลขฉาก: `bg0002` ->
  "ฉากอื่นใด: ไม่ส่งอะไรเลย" (event `world_census_skipped_scene_<id>_not_home`) -> `bg0001`
  `runtime.py` เป็นไฟล์ของ chief · `CORE-REQUEST` ออกไปแล้วรอบนี้:
  `notes_to_chief/20260828_2348_LANE-A-CORE-REQUEST-bg0015-census-branch.md`
  ⇒ ถ้ายังไม่ merge ผู้เล่นที่วาร์ปเข้า `Bg0015` จะเห็น **เกาะร้าง** และใบนี้จะรายงาน FAIL ปลอม
- ~~**B2 -- วันนี้ยัง "ไปไม่ถึง" ฉาก 14** · registry ของ `world_scene_travel` ไม่มีปลายทางที่ pin ไว้
  (ต้องใช้ native `.npc` digest ซึ่งไม่มีใน cloud clone) · `COO-DECISION 22:50` มอบหมายเลน GM
  เตรียมวาร์ป ⇒ ทางเข้า = **GM warp หรือ set scene ตรง** เท่านั้น~~
  ✅ **B2 ปิดแล้ว 2026-08-29T04:4x+07:00 (LANE-A รอบ `vyi2ud` · เจ้าของใบปิดใบตัวเอง)**
  🔴 **และวงเล็บในบรรทัดที่ขีดฆ่าเป็นเท็จมาตลอด (G1)**: native digest ของ `Bg0015` อยู่ในเรโปสะพานนี้เอง
  ที่คอลัมน์ `src_sha256` ของ `gamedata/PF_GAMEDATA_SCENE_INDEX.tsv` (91 placement · 51 definition ·
  `5d98e830…`) ⇒ ตัวปิด B2 อยู่ในมือตั้งแต่ต้น ไม่มีใครเปิดอ่าน
  🔴 **แก้ข้อเท็จจริงที่ใหญ่กว่านั้น: เมื่อวานนี้ผลของการวาร์ปเข้าฉาก 14 ไม่ใช่ "เกาะร้าง" แต่คือ "ล็อกอินตาย"**
  ฉาก 14 ไม่อยู่ในทะเบียน ⇒ `world_scene_entry.resolve_entry` โยน `SceneEntryRefused` ⇒ `runtime.py`
  พิมพ์ `WORLD_SCENE_ENTRY_REFUSED` แล้ว `return []` **ไม่ตอบเฟรมใดกลับ** ⇒ ไคลเอนต์ค้างหน้าเชื่อมต่อ
  ⇒ ถ้าบูตใบนี้ก่อนรอบ `vyi2ud` จะได้ FAIL ที่อ่านผิดเรื่องทั้งใบ
  **ตอนนี้**: ฉาก 14 เข้าทะเบียนแล้ว จุดเกิด = `MARKER[14]` `(-17513, 18989, 1894)` (จุดที่คนทำแมพเขียนไว้เอง
  · `src/pirateforce_foundation/world_scene_marker.py`) · `login_entry_allowed=true` ·
  `persist_position_allowed=false` (แถว Port Royal ของผู้เทสไม่ถูกแตะ ถอด override = กลับที่เดิมเป๊ะ)
  ⇒ ทางเข้าที่ใช้จริง: **override ฉากล็อกอินรายบัญชี → ล็อกเอาต์ → ล็อกอินใหม่**
  🔴 วันนี้ตัวเขียน override คือ **แก้ `config/gm_login_scene.json` หนึ่งบรรทัด** ให้บัญชี GM ที่ใช้เทส
  (`{"<ชื่อบัญชี>": 14}` · `gm/login_scene_override.py` อ่านใหม่ทุกล็อกอิน ไม่ต้องรีสตาร์ต)
  · คำสั่ง `/warp 14` ของสาย GM ที่เขียนไฟล์นี้ให้อัตโนมัติอยู่ใน `pirate-force-server#224` ซึ่ง
  **ยังไม่ merge ณ 04:4x** — ถ้ารอบเทสเกิดหลังมัน merge ใช้ `/warp 14` แทนได้ ผลเหมือนกัน
  บรรทัดที่ต้องเห็นบนคอนโซลก่อนอย่างอื่นทั้งหมด (ไม่เห็น = หยุด รายงานว่าไม่เห็น):
  `WORLD_SCENE scene_id=14 ... spawn=(-17513.000,18989.000,1894.000) ... population=bg0015_roster`
  และ `WORLD_SCENE_RELOCATED scene_id=14 reason=no_pinned_ground_for_scene`
  🔴 บรรทัด `RELOCATED` **เป็นของถูก ไม่ใช่บั๊ก**: ฉากนี้ตั้งใจไม่ปัก ground ⇒ ทุกการมาถึงลงที่ marker เสมอ
  🔴🔴 **แก้ 2026-08-29T05:2x+07:00 (รอบเดียวกัน หลัง `pf-adversary`) — ประตูถูกปิดกลับ B2 ยังเปิด**
  `pf-adversary` ขับล็อกอินเข้าฉาก 14 จริง (บูตไร้แฟล็ก) ตอนที่ `login_entry_allowed` ยังเป็น true
  แล้ววัดได้สามอย่าง ซึ่ง**ทั้งสามทำให้ใบนี้อ่านผลไม่ได้ ไม่ใช่แค่ไม่สวย**:
  1. **ส่ง NPC ท่าเรือ Port Royal 108 ตัวเข้าไปในฉาก 14** (`WORLD_CENSUS assembled=108/115`)
     ⇒ ผู้เทสจะเห็น "สิ่งมีชีวิตขึ้นจอ" **แล้วตัดสิน PASS ทั้งที่มันคือคนละเกาะ**
     🔴 คำทำนายเดิมของ B1 ที่ว่า "ถ้ากิ่งยังไม่ merge จะเห็นเกาะร้าง" **ผิด**
  2. **แถว `character_positions` ถูกเขียนเป็น `(scene_id 1, พิกัดภูเขาไฟ)`** ⇒ ล็อกอินครั้งถัดไป
     ตัวละครยืนอยู่ที่พิกัดภูเขาไฟกลาง Port Royal **เงียบ ๆ ไม่มีบรรทัดเตือน** = เหตุการณ์ `GT-106` ซ้ำ
  3. **ไม่มีบรรทัด `PLAYER_FACTION`** เลย (ตัวประกอบ faction-1 ปฏิเสธทุกฉากที่ไม่ใช่ 2 กับ Port Royal)
     ⇒ ป้าย/สีของศัตรูอาจเรนเดอร์ไม่เหมือนที่ใบนี้คาด
  เหตุร่วมของทั้งสาม: `runtime.py` อ่าน **แถวใน DB** ไม่ใช่ฉากที่ `resolve_entry` คืนมา และทางเข้าเดียว
  ที่มี (override ฉากล็อกอิน) ไม่เคยเขียนแถวนั้น ⇒ สลักทุกตัวในทะเบียนถูกเดินผ่าน
  ใบเต็ม + CORE-REQUEST: `notes_to_chief/20260829_0520_LANE-A-FINDING-stored-row-vs-resolved-scene.md`
  🔴 **สิ่งที่ต้องเคลียร์ก่อนใบนี้จะ READY ตอนนี้มีสามข้อ ไม่ใช่ข้อเดียว**: B1 (กิ่ง census ของ chief) ·
  B2' (คำตอบของใบ `0520` แล้วจึงเปิด `login_entry_allowed` กลับ) · และ D3 (faction byte)
  🔴 **ห้ามบูตใบนี้จนกว่าจะครบ** — เข้าเกาะได้ ไม่เท่ากับเห็นสิ่งมีชีวิต และตอนนี้ "เห็นสิ่งมีชีวิต"
  อาจแปลว่าเห็นของผิดเกาะ
  🆕 **อัปเดต chief R223 (`ngwnnj`) 2026-08-29T06:0x+07:00 — B2' ครึ่งของ chief push แล้ว รอ merge ยังไม่อยู่บน main:**
  ทาง A ตาม `CHIEF-DECISION 20260829_0520` ต่อสายแล้วใน `runtime.py` (ล็อกอินที่ override ฉากสำเร็จ เขียน
  `foundation.selected.position = entry.position` หลัง `world_scene_liveness.decide`) พร้อมเปลี่ยนตัวอ่านเป็น
  `consume_login_scene_override` (ใช้ครั้งเดียวตาม `COO-DECISION 0441` ข้อ 2)
  ⇒ ข้อ 1 (สำมะโนผิดเกาะ) และข้อ 2 (แถว `character_positions` ติดป้าย `scene_id 1`) **มีเทสขับผ่าน dispatcher จริงแล้วทั้งคู่**
  (`tests/test_gm_login_scene_override_position_resync.py`) · 🔴 **เป็นผลของ PR ที่ยัง "รอ merge"** — ผู้เทสห้ามถือว่าแก้แล้ว
  จนกว่าจะเห็น merge sha บน `main` · ~~ข้อ 3 (faction byte / D3) **ไม่ได้แตะรอบนี้ ยังบล็อกใบนี้อยู่**~~

  🟢🟢 **ทั้งสามข้อปิดครบแล้ว · B1 · B2 · B2' · D3 — LANE-A รอบ `vvy6q7` 2026-08-30T00:4x+07:00**
  | ข้อ | ปิดโดย | ตรวจได้ที่ |
  |---|---|---|
  | **B1** สำมะโนฉาก 14 | รอบ `ga91m5-r2` — `lane_hooks/lane_a_scene_census.py` (ไม่ต้องมี `elif` ใน `runtime.py` อีกแล้ว) | `WORLD_CENSUS_BG0015 assembled=81/91` |
  | **ข้อ 1** สำมะโนผิดเกาะ | `CHIEF-DECISION 0520` ทาง A + ฉาก 14 มีสำมะโน**ของตัวเอง** | `tests/test_lane_a_scene_census.py` ขับ dispatcher จริงบน registry จริง |
  | **ข้อ 2** แถว `character_positions` | กิ่ง `login_scene_override_visit` ไม่เขียนแถวถาวร · **และ `persist_position_allowed` ของฉาก 14 ยังเป็น `false`** (รอบนี้พลิก boolean เดียว ไม่ใช่สอง) | `tests/test_world_scene_marker.py` |
  | **ข้อ 3 / D3** faction byte | **รอบนี้** — `src/pirateforce_foundation/world_faction_admission.py` + แก้เกตเดียวใน `player_wire.py` | `PLAYER_FACTION basic_faction=1` · `tests/test_world_faction_admission.py` |
  | **B2** ประตูล็อกอิน | **รอบนี้** — `login_entry_allowed: true` ตาม `COO-DECISION 20260829_2342` | `WORLD_SCENE scene_id=14 ...` (ไม่ใช่ `WORLD_SCENE_ENTRY_REFUSED`) |
  🔴 **เงื่อนไขเดียวที่เหลือก่อนบูต: เห็น merge sha ของ `pirate-force-server#290` บน main**
  🔴 **`persist_position_allowed` ยังเป็น `false` โดยตั้งใจ** ⇒ ถอน override แล้วตัวละครกลับ Port Royal เป๊ะ
  แถวเดิมของผู้เทสไม่ถูกแตะ — ถ้าผู้เทสเห็นตัวเองโผล่ที่พิกัดภูเขาไฟกลาง Port Royal ในล็อกอินถัดไป
  **นั่นคือ `GT-106` ซ้ำ = รายงานทันที เป็นบั๊กจริง ไม่ใช่ผลที่คาดไว้**

### server args (เป๊ะ) — 🔴 **PRECONDITION แข็ง ไม่ใช่ข้อควรระวัง**
`py -3 -u -m pirateforce_foundation.app --db state\run_gt132.sqlite3` · db = สำเนา **ห้ามเปิด canonical**
· client `-SecondPasswordMode bypass` · 🔴 ห้ามมีแฟล็ก `--*-scenario` / `--world-census-actors` / `--export-events`

> 🔴🔴 **ยกเป็น PRECONDITION แข็ง ตามเงื่อนไขข้อ 1 ของ `COO-DECISION 20260829_2342`
> (LANE-A รอบ `vvy6q7` · 2026-08-30T00:4x+07:00) — บูตผิดข้อนี้ = ใบนี้เป็นโมฆะ ห้ามกรอกผล**
> **ถ้าคำสั่งบูตมีแฟล็ก `--*-scenario` ใด ๆ หรือ `--second-password-mode bypass` (ฝั่ง *เซิร์ฟเวอร์*)
> ⇒ หยุด ปิดเซิร์ฟเวอร์ บูตใหม่ให้ถูก แล้วเริ่มใบใหม่ตั้งแต่ต้น**
> เหตุผลที่วัดแล้ว (`pf-adversary` รอบ `ucaybn` ข้อ D8): `runtime.py:944`
> `world_census_enabled = (not active_lanes and second_password_mode == "required")`
> เป็นทั้งเงื่อนไขของกิ่งสำมะโนต่อสาย **และ** ตัวปลดอาวุธ dispatcher เดิม `v141:4292`
> ⇒ บูต opt-in **ไม่เรียกสำมะโนฉาก 14 เลย** แล้วส่ง `V134_P0_P30_P91_ISOLATED` = bg0001 สามตัว
> พิกัด Port Royal เข้าฉาก 14 แทน ⇒ ผู้เทสเห็น **3 ร่าง ไม่มีบรรทัด `WORLD_CENSUS_BG0015`** = **FAIL ปลอม**
> 🔴 **ตัวยืนยันหนึ่งบรรทัด ก่อนทำอย่างอื่นทั้งหมด:** ต้องเห็น `WORLD_CENSUS_BG0015 assembled=81/91`
> **ไม่เห็น = หยุด ห้ามเดินต่อ ห้ามเดา** · เห็น `V134_P0_P30_P91` = บูตผิด กลับไปข้อบน
> 🔴 `-SecondPasswordMode bypass` ของ **ไคลเอนต์** ยังใช้ตามเดิม — คนละตัวกับแฟล็กเซิร์ฟเวอร์

### ขั้นตอน (~30-40 นาที · อัดวิดีโอต่อเนื่องทั้งช่วง `LOCK_GAME`)
1. ของมาตรฐานทุกข้อตาม `ATTENDED_SESSION_RUNBOOK.md` (LOCK · สำเนา DB · `CANON_SHA` ก่อน-หลัง ·
   เซิร์ฟเวอร์ขึ้นก่อนไคลเอนต์ · T0 ภาพนิ่ง + HUD · NO-CRASH ด้วย **right-click-drag** ไม่ใช่ `Q`/`E` ·
   🔴 ห้ามพิมพ์ตัวอักษรใด ๆ ตลอดรอบ · กฎสีป้ายชื่อ · teardown ภายใน 420 นาที)
2. ให้ GM วาร์ป/ตั้งฉากเข้า `Bg0015` -> **คัดลอกตัวอักษร** (ไม่ใช่ถ่ายรูป) บรรทัด `WORLD_CENSUS_BG0015`
   ทั้งบรรทัด + บรรทัด per-actor ทั้งหมด + ทุกบรรทัด `BG0015_UNSHIPPED`
3. เดินไปยืนที่ **placement 32 (Hell King Kong) ที่ `(10607.72, 2047.01, 4600.40)`** ด้วย `W/A/S/D`
   -- จุดนี้คือจุดเดียวบนเกาะที่คุ้ม: ภายในรัศมี 2,500 หน่วยมี actor ที่ลงสายอีก 5 ตัว
   (Hell King Kong ตัวที่สอง 1367 · Carlos 2142 · Sea Phantom 2399 · Earth Flame Dragon 2496)
   และ Val'kyr ที่ 2734 ⇒ **6 ร่าง 5 ชื่อไม่ซ้ำ ในพื้นที่ประมาณหนึ่งจอ**
   ที่อื่นบนเกาะห่างกันมาก (median ระหว่าง actor สองตัวใด ๆ = 21,776 หน่วย) -- ไม่ต้องไปตามหา
4. ถ่ายภาพนิ่ง full-res อย่างน้อย 3 ภาพให้เห็นกลุ่มนี้ + HUD X/Y ทุกภาพ · จด **ชื่อที่อ่านได้จริง ตัวอักษรเป๊ะ**
   ทุกป้าย (อ่านไม่ออก = เขียน "unreadable" · ไม่มีป้าย = เขียน "none" · **ห้ามเว้นว่าง**)
5. 🔴 **บันทึกสีของทุกป้ายชื่อในเฟรม** (คำสั่งเจ้าของ 2026-08-25) · อ่านจากภาพนิ่ง full-res เท่านั้น ·
   จดสีอย่างเดียว **ห้ามเดาสาเหตุ**
6. NO-CRASH ซ้ำ -> ออกจากเกม -> 🔴 **restart เซิร์ฟเวอร์ก่อนบูตถัดไปเสมอ** -> teardown

### คำทำนาย (ผิด = ผล ไม่ใช่ความล้มเหลว)
คาดว่าเห็นสัตว์/ปีศาจ **level 105-115** (ฉากประกาศ `n_SCENE_LV=100`) 32 ชื่อ ตัวที่ซ้ำมากสุดคือ
Hell Ghoul 11 ตัว · Glaucoma 6 · Blood red eagle 5 · Phosphor powder Banshee 5 · Earth Flame Dragon 4
🔴 **รายชื่อเต็มไม่ต้องจำ** -- บรรทัด per-actor บนคอนโซลของบูตนั้นเองคือรายชื่อที่ต้องเทียบ

🔴 **หนึ่งตัวที่ดูผิดที่ผิดทาง แต่เป็นของถูกตามตารางวันนี้ -- ห้ามรายงานเป็นบั๊กของรอบนี้:**
placement `84` จะได้ `n_ID=923 Big Sword lv1 hp106` `s_OUTFIT` = `MAP009_000_000` = **ของประดับแมพ
ไม่ใช่สิ่งมีชีวิต** ยืนปนอยู่กับมอนเลเวล 105 · `pf-adversary` เป็นคนจับได้ ไม่ใช่ตัวคุมของสาย A เอง ·
สาย A **เลือกไม่ตั้งกฎตัดทิ้งใหม่ในรอบนี้** เพราะกฎที่ไม่มีตัวคุมรองรับคือสิ่งที่รอบนี้เพิ่งโดนตีตก ·
Port Royal ก็ส่ง `MAP001_000_000` (Mirage reel) แบบเดียวกันอยู่แล้ว
⇒ **จดว่าเห็นอะไรตรงนั้น** (ร่างจริง? กล่องเปล่า? ไม่มีอะไรเลย?) คำตอบนี้มีค่าเพราะมันตัดสินว่า
`MAP*` เกิดเป็น actor ได้หรือไม่ ซึ่งยังไม่มีใครรู้

🔴 **10 placement ว่างโดยตั้งใจ -- ว่างคือของถูก ห้ามรายงานเป็น regression:**
- placement `0` (Mob-Set 1 -> leader n_ID 321) -- ไม่มีแถวใน CONSTDATA `MOBS`
- placement `76`-`83` (Mob-Set 101-108 -> leader 10063-10070) -- มีแถว `MOBS` แต่ **ไม่มี `s_OUTFIT`**
  ชื่อใน `MOBS_TIP` เป็นสตริงจีนที่ตั้งชื่อ **ตัวช่วย path-finding ไม่ใช่สิ่งมีชีวิต**
- placement `90` (Mob-Set 115 -> leader 944) -- ไม่มีแถว `MOBS`

**[ตัวหักล้าง ค่าเท่ากับ PASS]** ถ้าคอนโซลขึ้น `wire=81` ครบแต่บนจอ **ไม่มีร่างใดเลย** ⇒ ผลนี้ redirect
กลับไปที่ `RE-128` (สาย static) **ไม่ใช่การเปิดใบ attended ใหม่** -- จดแล้วปิดรอบ

### pass criteria (สองชั้น แยกกัน 🔴 ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
**wire/DB** (headless พิสูจน์ได้ ไม่ต้องมีคนดูจอ) -- grep stdout+stderr รวมกัน (`2>&1`):
- มีบรรทัด `WORLD_CENSUS_BG0015` ที่อ่านได้ครบ: `assembled=81/91` · `shippable=81` · `wire=81`
  (ไม่ใช่ `MISMATCH`) · `bodies=ok`
- **token ที่พิสูจน์ว่าอยู่ในฉาก 14 จริง**: การมีบรรทัดนั้น **อยู่เลย** คือหลักฐาน (dispatch เป็น if/elif
  บนเลขฉาก) 🔴 ถ้าเจอ `world_census_skipped_scene_<id>_not_home` แทน = ยังไม่ได้เข้าฉาก
  ⇒ **หยุด อย่าให้คะแนน** จดเลขฉากที่มันบอกแล้วรายงาน
- บรรทัด per-actor `n_ID=<id> <name> lv<level> hp<hp> @(x,y,z)` ต้องมีชื่อครบตามตารางคาดข้างบน
- มี `BG0015_UNSHIPPED` **10 บรรทัด** ตรงกับ placement `0`, `76`-`83`, `90`
- `sessions` +1 · `max(lease_generation)` ไม่ถอย · `integrity_check` = `ok` · sha canonical ตรงก่อน-หลัง

**client-observable** (ต้องมีคนอยู่หน้าจอเท่านั้น จะอนุมานจากคอนโซลไม่ได้เด็ดขาด):
- ที่ **placement 32** เห็น **6 ร่าง ที่มีป้ายชื่อ 5 ชื่อไม่ซ้ำ** พร้อมกันบนภาพนิ่ง full-res
- ชื่อบนป้ายตรงกับชื่อในบรรทัด per-actor และร่างยืนอยู่ตำแหน่งเดียวกับพิกัดที่ส่ง (เทียบกับ HUD X/Y)
- 10 จุดว่างที่เดินถึงได้ = ว่างจริง (จุดที่เดินไม่ถึง **เขียนว่าไม่ได้ตรวจ ห้ามเดา**)
- สีป้ายชื่อครบทุกป้ายทุกภาพตามข้อ 7 · NO-CRASH ผ่านสองครั้ง
- ❗ **negative มีค่าเท่ากับ positive**: "เกาะร้าง ทั้งที่ `wire=81`" หรือ "ชื่อไม่ตรงสำมะโน" คือผลที่ต้อง
  บันทึกให้ละเอียดเท่ากับผลบวก และ redirect ไปสาย static ตามข้อหักล้างข้างบน

### nonclaims (ติดไปกับผลทุกกรณี)
1. **ไม่ทดสอบความเป็นศัตรู/การต่อสู้** -- ทุก actor ในสำมะโนนี้เป็น NEUTRAL ไม่ถือ faction bit เลย
   นั่นเป็น splice ของสาย B และ **จงใจไม่อยู่ในรอบนี้** 🔴 **มอนสเตอร์ที่ไม่เข้าตี = ผลที่คาดไว้ ไม่ใช่ FAIL**
2. **ไม่ทดสอบสีป้ายชื่อ** -- อะไรกำหนดสียังไม่รู้ (`RE-067` ปิดแบบ bounded-negative) ผู้เทสจดสีอย่างเดียว
3. **ไม่อ้างว่า NPC ที่ไคลเอนต์สร้างเองในฉาก กับ census ของเซิร์ฟเวอร์ เป็น registry เดียวกัน**
   (nonclaim ที่ยังเปิดของ `RE-128`) 🔴 **ถ้าผู้เทสเห็น actor ซ้อน (Hell Ghoul สองตัวยืนทับกันจุดเดียว)
   นั่นคือคำตอบของคำถามที่ยังเปิดข้อนั้น และเป็นสิ่งที่มีค่าที่สุดที่ใบนี้จะส่งกลับมาได้** -- ถ่าย/จดให้ละเอียดที่สุด
4. `s_OUTFIT` แบบหลายตัวคั่น `;` มี 10 รายการ สาย A ส่ง **ตัวแรก** -- กระทบ 45 จาก 81 placement
   ⇒ **ถ้าครึ่งเกาะดูเหมือนใส่ skin ผิด = สมมติข้อนี้ จด ไม่ใช่ FAIL** [LANE-A ASSUMPTION] (ติดแท็กไว้ในโมดูลแล้ว)
5. **ไม่เลื่อนสถานะ identity ของ `Bg0015` เป็นข้อเท็จจริงด้วยตัวเอง** -- `world_scene_numbering` ยังคืน
   `verdict=refused` สำหรับ `Bg0015` และจะคืนแบบนั้นต่อไปจนกว่าตาเจ้าของจะบอกเป็นอย่างอื่น
   (`COO-DECISION 2026-08-28T22:50` ว่าด้วยผู้มีสิทธิ promote ฉาก)
6. ผู้เทสคนเดียว บูตเดียว ฉากเดียว · ไม่ปิดใบใด ไม่ประกาศ milestone ใด ไม่ใช้สถานะ GM
7. 🔴 **ตัวคุมของสาย A พิสูจน์แค่ว่าคาสต์มาจากบล็อก CLINE type 14 ไม่ได้พิสูจน์ว่าตัวไหนอยู่จุดไหน**
   (`pf-adversary` รอบ `w0pu2i` เอาตารางที่สลับคู่แบบสุ่มยัดผ่านตัวคุมทั้งสี่ได้หมด) ⇒ **ใบนี้คือ
   ตัวเดียวที่ตัดสินการจับคู่รายจุดได้** ถ้าผู้เทสเห็นชื่อไม่ตรงตำแหน่ง นั่นไม่ใช่ความประหลาดใจ
   มันคือสิ่งที่ใบนี้มีไว้ตรวจ

**ผู้เปิดใบ: LANE-A (รอบ `w0pu2i`)** -- ผลกลับมาที่สาย A บริโภค

### result (ผู้เทสกรอก)
```

```

## GT-145 CONSOLE-ENCODING-MEASURE-001 [STATIC-ON-BRIDGE -- วัดบนสะพานตอนเซิร์ฟเวอร์รันจริง · ไม่บูตไคลเอนต์ ไม่ล็อกอิน ไม่มีตัวละคร · ~15 นาที]: คอนโซลของเครื่องเจ้าของเป็น encoding อะไร -- พิมพ์สี่ค่าครั้งเดียว คัดลอกกลับมาดิบ ๆ  [DONE (wire/DB, N/A client-observable by design) -- ผล: `20260830_1738_GT145-RESULT-four-values-measured-PYTHONIOENCODING-is-None-locale-cp874-streams-utf8.md`, วัดครบสี่ค่าตรงคำทำนายทั้งสี่ข้อ, OBSERVER_CONFIRMED N/A ตามใบ]

**ตอบใบ `CORE-REQUEST-GM-035`** · เข้าคิวตามจดหมาย chief `20260829_1221` ข้อ ⑤ · เขียนใบโดย `pf-queue-author`

> NUMBERING: grep ก่อนจอง -- `GT-145` / `RE-145` = 0 hit ทั้ง `GAME_TEST_QUEUE.md` และ `CLIENT_RE_QUEUE.md` · สูงสุดก่อนหน้า = `GT-144` · ตัวนับเดียวร่วมกับ `CLIENT_RE_QUEUE.md`

**ทำไมต้องวัด:** สามที่ใน repo พูดไม่ตรงกัน และ **ไม่มีที่ไหนวัดอะไรเลย** -- `runtime_console.py:26` (`_Mirror.encoding` รายงาน `utf-8`) · `gate-windows.yml:53` (บังคับ `PYTHONIOENCODING: 'cp874:strict'` เป็นนโยบาย) · เอกสารสาย GM + กติกาบ้าน ("คอนโซลสะพานเป็น cp874" มาหลายรอบ) · 🔴 และมี**ที่สี่**ที่จดหมาย GM-035 ไม่ได้ลิสต์: `runtime_console.py:122,126-133` เปิดคอนโซลด้วย `SetConsoleOutputCP(65001)` แล้ว `open("CONOUT$", "w", encoding="utf-8", errors="replace")` · ผลไม่ใช่เรื่องความเรียบร้อย: คอนโซลที่เข้ารหัสอักขระไม่ได้ทำให้ `print` โยน `UnicodeEncodeError` และเพราะ `_Mirror.write` เขียนคอนโซล (`:45`) **ก่อน** ไฟล์ mirror (`:46`) บรรทัดนั้นจะไม่ถูกบันทึกที่ไหนเลย

- objective: บนสะพาน ตอนเซิร์ฟเวอร์รันอยู่จริง สี่ค่านี้คือค่าอะไร -- `sys.stderr.encoding` · `sys.stdout.encoding` · `os.environ.get("PYTHONIOENCODING")` · `locale.getpreferredencoding(False)` · หนึ่งข้อเท็จจริงของเครื่อง วัดครั้งเดียว **ไม่ได้พิสูจน์ว่าไฟล์ไหนถูกหรือผิด**
- db: สำเนา `state\run_gt145.sqlite3` · 🔴 ห้ามเปิด canonical `state\pirateforce.sqlite3` · sha256 ก่อน-หลังต้องตรงกับ `CANON_SHA.txt` ทั้งสองครั้ง (🔴 ห้ามฝังค่าตาย -- ใบนี้เคยฮาร์ดโค้ด `673f4bfb1c35...` ซึ่งเป็นค่าเก่าและทำให้ GT-145 abort ทั้งที่ DB ไม่ได้ผิดอะไร วัดแล้ว R245 จาก GT-145 RESULT)
- server args: `py -3 -u -m pirateforce_foundation.app --db state\run_gt145.sqlite3` · 🔴 ห้ามมีแฟล็ก `--*-scenario` / `--world-census-actors` / `--export-events` · ไม่บูตไคลเอนต์
- steps:
    0. `LOCK.txt` ต้องเป็น `RELEASED` แล้วเขียนตัวเองเป็น holder · `py -3 -V` ตอบได้ (ไม่ตอบ = เลื่อนใบ ไม่ใช่ FAIL)
    1. copy DB · จด sha256 ของ canonical
    2. บูตเซิร์ฟเวอร์ในหน้าต่างของมันเอง ปล่อยรันไว้ **ห้ามแตะ** · จด boot stamp
    3. `netstat -ano | findstr "10188 10189"` -> ต้องเห็น LISTENING ทั้งสองพอร์ต · คัดลอกทุกบรรทัด
    4. เปิดหน้าต่าง PowerShell **ใหม่** ด้วยวิธีเดียวกับหน้าต่างที่บูตเซิร์ฟเวอร์ (shortcut/profile เดียวกัน) แล้ว `cd` รากรีโป · **จดว่าเป็นหน้าต่างใหม่หรือหน้าต่างเดียวกับเซิร์ฟเวอร์** (จดอย่างเดียว ไม่ต้องตีความ)
    5. รันบรรทัดนี้ **ตามตัวอักษร**:
       `py -3 -c "import sys,os,locale;print('PF_ENC stderr=%r stdout=%r PYTHONIOENCODING=%r locale=%r' % (sys.stderr.encoding, sys.stdout.encoding, os.environ.get('PYTHONIOENCODING'), locale.getpreferredencoding(False)))"`
       ทั้งบรรทัดเป็น ASCII ล้วนโดยตั้งใจ -- ถ้าคอนโซลเป็น cp874 strict จริง โพรบที่มีอักขระนอก ASCII จะฆ่าการวัดของตัวเอง
       🔴 **ห้าม redirect ห้าม pipe** (`>` `|` `Out-File` `Tee-Object` `Out-Host` `Select-String`) -- pipe เปลี่ยนค่า `sys.stdout.encoding` จริง ๆ ⇒ ผลที่ผ่าน pipe ใช้ไม่ได้ · แล้ว `echo $LASTEXITCODE` ต้องได้ `0`
    6. รันต่อ คัดลอกผลด้วย: `chcp` และ `py -3 -V`
    7. **คัดลอกตัวอักษร** จากคอนโซล (mark & copy) ไม่ใช่ถ่ายรูป ไม่ใช่พิมพ์ตาม -> วางลงช่อง result ดิบ ๆ
    8. `netstat` ซ้ำข้อ 3
    9. Ctrl+C ปิดเซิร์ฟเวอร์ · จด sha256 canonical ซ้ำ · **teardown ภายใน 60 นาทีนับจาก boot stamp** (`PANYA-ORDER 2026-08-29T09:30+07:00` ข้อ ① ลดเพดานจาก 180 เหลือ 60 สำหรับรอบ unattended · ใบนี้กินเวลา ~15 นาทีจึงอยู่ในเพดานสบาย ๆ) · ปลด LOCK เป็น `RELEASED` · 🔴 ห้าม commit เอง
- pass criteria: 🔴 สองชั้นแยกกัน ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น
    wire/DB (headless ล้วน ไม่ต้องมีคนหน้าจอ):
      (ก) `netstat` ทั้งก่อนและหลังโพรบ เห็น LISTENING ทั้ง `10188` และ `10189` ⇒ วัดตอนเซิร์ฟเวอร์รันจริง
      (ข) บรรทัด `PF_ENC` ออก **ครั้งเดียว** และ `$LASTEXITCODE` = `0`
      (ค) สี่ค่าอยู่ในช่อง result แบบคัดลอกดิบ ครบสี่คีย์ **ไม่มีคีย์ไหนเว้นว่าง** · ค่าที่ไม่ได้ตั้งต้องเป็นตัวอักษร `None` เขียนออกมาเต็ม ๆ
      (ง) `chcp` · `py -3 -V` · คำตอบข้อ 4 (หน้าต่างไหน) บันทึกครบ -- ใบปิดที่สี่ค่า สามอย่างนี้คือบริบทที่กันการต้องรันซ้ำอีกรอบ
      (จ) sha256 canonical เท่าเดิมก่อน-หลัง · `SELECT max(lease_generation) FROM sessions;` บน**สำเนา** เท่าเดิมก่อน-หลัง (ใบนี้ไม่ส่งเฟรมใด ๆ ไม่มีแถวที่ `selected_character_id IS NOT NULL`)
    client-observable: 🔴 **ใบนี้ไม่มีชั้นนี้ -- N/A และนี่คือเหตุผล** ไม่มีไคลเอนต์ถูกบูต ไม่มีล็อกอิน ไม่มีตัวละคร ไม่มีอะไรถึงจอผู้เล่นแม้แต่พิกเซลเดียว · สิ่งเดียวที่อยู่บนจอคือหน้าต่างคอนโซล ซึ่งเป็นข้อเท็จจริงของเครื่องที่อ่านได้แบบ headless **ไม่ใช่หลักฐานชั้น client-observable** ⇒ **ไม่ต้องมี `OBSERVER_CONFIRMED` และห้ามรอมัน** · กฎบันทึกสีป้ายชื่อทุกป้ายในเฟรม (คำสั่งเจ้าของ 2026-08-25, R163) **ไม่ใช้กับใบนี้ เพราะไม่มีเฟรมและไม่มีป้ายชื่อเลย** -- ไม่ใช่การขอยกเว้น · 🔴 ห้ามใช้ผลใบนี้อ้างว่าอะไรปรากฏหรือไม่ปรากฏบนจอ
- nonclaims:
    1. ไม่อ้างค่าของ `sys.stderr` **ภายในโปรเซสเซิร์ฟเวอร์หลัง `install_runtime_console` ทำงานแล้ว** -- ตรงนั้น `sys.stderr` เป็น `_Mirror` (`runtime_console.py:84-85`) เป็นคำถามคนละใบ ⇒ อยากได้ต้องเปิดใบใหม่ ห้ามยัดเข้าใบนี้
    2. ไม่อ้างอะไรกับ stdout ที่ถูก redirect/pipe (ใบนี้วัดกรณีคอนโซลล้วน) และไม่อ้างว่าค่านี้เท่ากับค่าบน CI -- `gate-windows.yml` **บังคับ** ค่า ไม่ได้วัด (`:160-165` ยืนยันตัวเองบน runner ไม่ใช่บนสะพาน)
    3. ผู้เทส **ไม่ต้องตีความ และไม่แก้ไฟล์ใด ๆ** รายงานสี่ค่าดิบอย่างเดียว การตัดสินว่าไฟล์ไหนผิดเป็นของ chief
    4. **ผลลบมีค่าเท่าผลบวก** -- ค่าที่ออกมาไม่ตรงคำทำนายสักข้อคือคำตอบของ `GM-035` ไม่ใช่ความล้มเหลว · โพรบรันไม่ได้ / exit != 0 = **เลื่อนใบ ไม่ใช่ FAIL**
    5. ไม่บล็อกสาย GM -- `console_safe(text, stream)` ถามสตรีมเองอยู่แล้ว เดินต่อได้ทุกคำตอบ

**คำทำนาย (เป็นคำทำนาย ผิด = ผล ไม่ใช่ความล้มเหลว):** `PYTHONIOENCODING` = `None` · `locale.getpreferredencoding(False)` = `cp874` · `sys.stdout.encoding` = `sys.stderr.encoding` = `utf-8` เมื่อสตรีมต่อกับคอนโซลจริง (Windows ข้าม code page เว้นแต่ตั้ง `PYTHONLEGACYWINDOWSSTDIO=1` ซึ่ง `gate-windows.yml:54` ตั้ง แต่สะพานอาจไม่ตั้ง)

**คำตอบแต่ละแบบแปลว่าอะไร (สำหรับคนอ่านผล ไม่ใช่งานของผู้เทส):**
- **ไม่ใช่ `cp874`** ⇒ `gate-windows.yml:53` กำลังทดสอบเงื่อนไขที่ไม่มีอยู่บนสะพาน · ไฟล์นั้นเป็นเขต chief ตัดสินเองว่าแก้หรือคงไว้เป็นการเผื่อ
- **เป็น `cp874`** ⇒ `runtime_console.py:26` ที่คืนค่าคงที่ `utf-8` คือคำรายงานเท็จที่รอคนเชื่อ · คนที่ถามสตรีมจะพับน้อยเกินไป -> `print` โยน -> บรรทัดหายทั้งคอนโซลและ mirror (`:45` ก่อน `:46`)
- **`PYTHONIOENCODING` = `None`** ⇒ `cp874` ในรีโปมีที่มาเดียวคือไฟล์ CI · ประโยค "คอนโซลสะพานเป็น cp874" ไม่เคยมีการวัดรองรับ
- **stdout != stderr** ⇒ ผลที่ไม่มีที่ไหนในสี่ที่พูดถึง ⇒ เปิดใบใหม่ ห้ามยัดเข้าใบนี้

**ลิงก์ (ผู้เทสไม่ต้องอ่านเพื่อรันใบ):** `notes_to_chief/20260829_1105_LANE-GM-CORE-REQUEST-GM-035-what-encoding-is-the-console.md` · `notes_to_chief/20260829_1221_CHIEF-REPLY-LANE-GM-034-answered-differently-and-035-queued.md` ข้อ ⑤ · `src/pirateforce_foundation/runtime_console.py:26,45-46,84-85,122,126-133` · `.github/workflows/gate-windows.yml:53,160-165` · `docs/GM_LANE.md:3522` · `src/pirateforce_foundation/gm/login_scene_override.py:71`

**ผู้เปิดใบ: chief (สาย E) ตามจดหมาย `20260829_1221` ข้อ ⑤** -- ผลกลับมาที่ chief และสาย GM บริโภค

### result (ผู้เทสกรอก)
```

```

---

## GT-148 SCENE17-STOWAWAY-ACTORS-FIRST-EYES-001 [attended, in-game]: ออกทะเลกับ Columbus แล้ว **ไคลเอนต์ยังโชว์ actor ของ Port Royal ที่ถูกส่งไปตอนล็อกอินอยู่หรือไม่**  [~~PENDING · เปิดโดย LANE-A (WORLD) รอบ `2pdf6j`~~ 🟢 **PASS ทั้งสองชั้น — LANE-A รอบ `qoj8ei` 2026-08-31T11:4x+07:00 ปิดหัวใบ ตามผล `notes_to_chief/20260831_1037_GT148-and-GT165-RESULT-stowaways-cleared-and-slave-market-island-has-life.md`: เจ้าของออกทะเลกับ Columbus ไปฉาก 17 รายงานตรง ๆ ว่า "ในแมพนั้นไม่มี npc อะไรอยู่" — ไม่มี actor ของ Port Royal ค้างข้ามมาแม้แต่ตัวเดียว; wire ยืนยันครบสี่บรรทัด รวม `WORLD_M2_CROSSING_HANDOFF kind=clear dispatched=YES slot=before_teleport`. หมายเหตุ: พบของใหม่คนละชั้น (หน้าต่างบทสนทนา Columbus ค้างบนจอ) ยกเป็น `RE-168` แยก ไม่นับเป็น FAIL ของใบนี้**]

> 🔴 อัปเดตโดย chief รอบ `65etwo` 2026-08-30T~23:1x+07:00: LANE-A เปิด CORE-REQUEST
> (`notes_to_chief/20260830_2148_LANE-A-CORE-REQUEST-columbus-crossing-owes-a-population-handoff.md`)
> ให้ต่อสาย `world_m2_crossing_handoff.crossing_handoff()` เข้าสาขาสำเร็จของ Columbus ใน `runtime.py`
> รอบนี้ต่อแล้ว — **ไม่เปิดใบใหม่ซ้ำ** (ใบนี้ถามคำถาม client-observable เดียวกันเป๊ะกับที่ CORE-REQUEST
> นี้ตอบชั้น wire/DB แล้ว: "จอยังโชว์ Port Royal อยู่ไหมหลังออกทะเล") ปรับ **wire/DB criteria ข้อ (ค)**
> ด้านล่างให้ตรงของจริงที่ลงแล้วแทน: บรรทัดที่คัดลอกตอนนี้คือ `WORLD_M2_CROSSING_HANDOFF scene=17
> kind=clear held=108 composed=YES dispatched=YES pc=17B frame=27B slot=before_teleport reason=...`
> (ยืนยันด้วย probe สดผ่าน harness เดียวกับ `tests/test_columbus_quest_dispatch_wiring.py` รอบนี้ ไม่ใช่
> การอ่านซอร์สเฉย ๆ) มาก่อนบรรทัด teleport เสมอ (`slot=before_teleport`) ตามด้วย `WORLD_POP_STOWAWAYS`
> เดิมที่ยังพิมพ์อยู่เหมือนเคย — คัดลอกทั้งสองบรรทัดลง result ไม่ใช่เลือกอันเดียว สวีตเต็มเขียว(cloud
> sanity) 5578 passed 0 failed หลังต่อสาย · รอ merge/gate จริงบนสะพานก่อนบูตใบนี้ (ดู `PR_STATE.txt`)
> P1/P2 เดิมข้างล่างยังใช้ได้ทั้งคู่: ตอนนี้เฟรม clear ถูกคิวจริงแล้ว ถ้าผู้เทสยังเห็น actor เดิม (P1)
> แปลว่าไคลเอนต์รับเฟรมแล้วไม่ทำตาม (ไม่ใช่ว่าเซิร์ฟเวอร์ยังไม่ส่ง) — ข้อค้นพบคนละความหมายจากตอนใบนี้เปิด
> ครั้งแรก เขียนไว้ในผลให้ชัดว่าทดสอบตอนที่เฟรมถูกส่งแล้ว

> NUMBERING: ใบนี้เปิดเป็นเลข 147 (grep ตอน 14:2x: เลขสูงสุดที่ใช้ไป = 146) แล้ว **ขยับเป็น `GT-148` ด้วยตัวเอง** ตามกฎออกเลขข้อ 3 ที่หัวไฟล์ — ชนกันจริง = คนที่ push ทีหลังขยับเลขของตัวเอง แล้วเขียนเหตุผลไว้ในใบ: ใบ COUNTER-RESYNC-RECOVERY-TOOL-001 ลง main ก่อนใบนี้ ⇒ ใบนั้นถือเลข 147 ไว้ทั้งใบ ไม่ถูกแตะแม้แต่ตัวอักษรเดียว
> ที่มา (วัดรอบนี้จากตารางแช่แข็ง ผ่าน `world_population_handoff` + `tests/test_world_population_handoff.py::ArrivalStowawayTests`): census ส่ง actor `bg0001` **108 ตัวจาก 115 แถวในตาราง ครั้งเดียวบนเส้นทางล็อกอิน** และ **ไม่มีอะไร recompose ระหว่างเซสชัน** ⇒ ตอนข้ามไปทะเลเซิร์ฟเวอร์ไม่ได้ส่งคอลเลกชันใหม่เลย · สี่ตัวยืนห่างจุดขาเข้าทะเล `(0,0,0)` ไม่ถึง 2000 หน่วย: `Legend Jack` 1226.6u · `Plato` 1646.7u · `Qina` 1915.8u · `Betula` 1935.9u (รัศมี 5000u: **census ที่ส่งจริง 10 ตัว** · ตารางดิบ 11 — แถว `Filet` ที่ 2530u ไม่เคยถูกส่ง) 🔴 **เลข 4 เป็นของจุด `(0,0,0)` ซึ่งเป็น decree ไม่ใช่ค่าที่วัด** — ถ้าลงในแถบพื้นของฉากเอง (z 746.04-1272.74) จะเป็น **5 ตัว** (`Kaim` เข้ามา) และระยะสูงต่ำยุบจาก ~930 เหลือไม่เกิน ~341

### objective (claim เดียว)
เมื่อผู้เล่นออกจาก Port Royal ด้วยเรือของ Columbus (เส้นทางที่มีอยู่จริงวันนี้ ไม่ต้องใช้แฟล็ก: คลิก Columbus ที่ท่า → ตัวเลือก 1 → เควส 3021 → ฉาก 17 "เรือกลางทะเล" ซึ่ง `GT-106` พิสูจน์แล้วว่าเดินได้) **จอยังแสดง actor ของ Port Royal ที่ถูกส่งไปตอนล็อกอินอยู่หรือไม่** — ใบนี้ตอบแค่ "เห็น" vs "ไม่เห็น" เท่านั้น

### db / server args (เป๊ะ)
สำเนา `state\run_gt148.sqlite3` (+ backup) · 🔴 **ห้ามเปิด canonical** · sha256 เทียบ `CANON_SHA.txt` ก่อน-หลัง ต้องตรงทั้งสองครั้ง
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt148.sqlite3
```
🔴 **ห้ามมีแฟล็กฝั่งเซิร์ฟเวอร์ใด ๆ** (`--*-scenario`, `--world-census-actors`, `--export-events`) — แฟล็กทำให้กิ่ง v141 เก่ายิง actor ฉาก 1 เข้ามาเอง ⇒ ผลอ่านไม่ได้ทั้งรอบ · client `-SecondPasswordMode bypass` ตามปกติ · 🔴 **restart เซิร์ฟเวอร์ก่อนบูตไคลเอนต์ทุกครั้ง** (session ค้าง ⇒ ไคลเอนต์ถัดไปค้าง "connecting")

### ขั้นตอน
0. มาตรฐานบ้าน: `LOCK` · boot stamp (+07:00) · sha canonical · copy DB · resolve commit เขียว
1. **server ก่อน client เสมอ** · **อัดวิดีโอต่อเนื่องตั้งแต่ก่อนแมพโหลด**
2. 🔴 **ห้ามพิมพ์ตัวอักษรใด ๆ ตลอดรอบ** — ตัวอักษรตอนช่องแชตไม่โฟกัสกลายเป็น hotkey
3. ที่ท่าเรือ Port Royal: **S0** ภาพนิ่ง full-res ก่อนคลิก ให้เห็น NPC ท่าเรือในเฟรม
4. คลิก NPC index 1 ที่ปืนใหญ่ (`GT-106`: ป้ายยังเขียน `Warden / Sebastian`) → หน้าต่าง QUEST → กด **ตัวเลือกที่ 1** ("มุ่งหน้าไป Atlantic Ocean: Rising Sun Sea") **ครั้งเดียว** · ยิงได้ครั้งเดียวต่อ connection — พลาดแล้วให้ relog **ห้ามคลิกซ้ำแล้วรอ**
5. **S1** ทันทีที่ภาพฉากทะเลขึ้น โดย**ยังไม่ขยับอะไรเลย**
6. กวาดกล้องรอบตัว 360 องศาด้วย **คลิกขวาค้างลากเท่านั้น** (หมุนกล้องอย่างเดียว ไม่มีไบต์ออกสาย · 🔴 ห้าม `Q`/`E`/`W`/`A`/`S`/`D` ซึ่งหัน**ตัวละคร**จริงและยิง `TargetPosVital`) → **S2**
7. **เงยกล้องขึ้นให้สุด** ด้วยคลิกขวาค้างลาก แล้วกวาดรอบอีกหนึ่งรอบ → **S3** · 🔴 ถ้าไม่ได้เงย ให้เขียนลงผลว่า **"ไม่ได้เงย"** ห้ามรายงานว่าทะเลว่าง
8. NO-CRASH ด้วยคลิกขวาค้างลาก · ออกเกมด้วย X มุมขวาบน
9. **คัดลอกตัวอักษร** (mark & copy ไม่ใช่ถ่ายรูป ไม่ใช่พิมพ์ตาม) บรรทัดคอนโซลช่วงข้ามฉากลงช่อง result **ดิบ ๆ ห้ามแก้**
10. ปิด server · เก็บ capture + console `.out`/`.err` + sha256 ทุกไฟล์ · `PRAGMA integrity_check` บน**สำเนา** · **teardown เสมอ ภายใน 420 นาทีจาก boot stamp** (`TEMPLATE_teardown_generic.ps1:135`) · sha canonical ซ้ำ · 🔴 **ห้าม commit เอง**

### pass criteria (สองชั้น 🔴 ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
**wire/DB (headless ล้วน):** คัดลอกครบสี่บรรทัดดิบ — `WORLD_SCENE scene_id=17` · `SCENE_ENTRY scene=17 xyz=0.000,0.000,0.000 source=PROVISIONAL-OWNER-DECREE-20260827-1445` · `COLUMBUS_QUEST3021_NO_VEHICLE_DISPATCH scene=17` · และบรรทัดที่รอบนี้เพิ่ม `WORLD_POP_STOWAWAYS ...` — บนเซิร์ฟเวอร์วันนี้อ่านว่า `WORLD_POP_STOWAWAYS unmeasured reason=call_site_passed_no_legacy anchor=(0.000,0.000,0.000)` (call site ใน `runtime.py` ยังไม่ส่งโมดูลแช่แข็ง/สมาชิกเข้าไป · CORE-REQUEST หนึ่งโทเคนถึง chief เปิดอยู่) ถ้าของ chief ลงแล้วจะอ่านว่า `WORLD_POP_STOWAWAYS anchor=(0.000,0.000,0.000) held=108 radius=2000.0 within=4 nearest=Legend_Jack@1226.6 names=...` — **ทั้งสองแบบใช้เป็นหลักฐานว่าการข้ามฉากเกิดขึ้นจริงได้เท่ากัน คัดลอกอันที่เห็น ห้ามแก้** · + `integrity_check`=ok · `sessions` +1 ต่อการเข้าเกม · `max(lease_generation)` ไม่ถอยหลัง · sha canonical ตรงก่อน-หลัง
🔴 ชั้นนี้ **ตอบไม่ได้ว่ามีอะไรอยู่บนจอ**
**client-observable (ต้องมีคนหน้าจอ):** วิดีโอต่อเนื่อง + `S0`..`S3` **full-res** พร้อม sha256 · ตอบเป็นภาษาคน: เห็นตัวละครอื่นในฉากทะเลไหม กี่ตัว · **ชื่อที่อ่านได้** · อยู่ **เหนือหัว/บนฟ้า** หรือ **ระดับดาดฟ้า** · มีตัวแต่ไม่มีป้าย / มีป้ายแต่ไม่มีตัว · **จดสีป้ายชื่อทุกป้ายทุกภาพ** บรรทัดละป้าย รวมป้ายตัวเอง ไม่มีป้ายเขียน `none` · อ่านสีจาก **full-res เท่านั้น** · 🔴 **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (`RE-067`) · ต่างจากภาพเซิร์ฟเวอร์จริง → `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งข้อ · NO-CRASH/CRASH · `OBSERVER_CONFIRMED: <เวลา +07:00>`
🔴 ชั้นนี้ **ตอบไม่ได้ว่าเฟรมใดออกจากเซิร์ฟเวอร์**

### คำทำนาย (เป็นคำทำนาย ผิด = ผล ไม่ใช่ความล้มเหลว)
**P1** เห็นหนึ่งตัวขึ้นไปในสี่ตัวนั้น (ป้ายอ่านได้ หรือเป็นร่างลอยบนฟ้าเหนือทะเล) ⇒ ไคลเอนต์ **เก็บ** remote actor ข้ามฉาก ⇒ เฟรม clear ของ `world_population_handoff` เป็นของจำเป็นจริงและการต่อสายเป็นเรื่องด่วน
**P2** ทะเลว่างไม่มีตัวละครเลย ⇒ ไคลเอนต์ **เคลียร์เอง** ⇒ `[INFERENCE]` กลางของโมดูลเดียวกันปลดระวาง และเฟรม clear ไม่จำเป็นสำหรับการข้ามนี้ — **มีค่าเท่ากับ P1 ทุกประการ**
**P3** อย่างอื่นทั้งหมด (ร่างไม่มีป้าย / ป้ายไม่มีร่าง / อยู่บนดาดฟ้าแทนที่จะลอย) ⇒ **จดตามที่เห็นเป๊ะ ๆ ไม่ต้องตัดสินอะไร**

### กฎจุดเกิด
รอบนี้ก๊อป DB ⇒ ตัวละครกลับจุดเกิดทุกบูต · จุดขาเข้าฉาก 17 = `(0,0,0)` เป็น**คำสั่งเจ้าของ ไม่ใช่ค่าที่วัด** · z ของสี่ตัวนั้นราว **930-971** ส่วนพิกัดที่เซิร์ฟเวอร์ส่งให้ผู้เล่นลงคือ **z=0** ⇒ ถ้ายังถืออยู่ **และไคลเอนต์วางผู้เล่นที่ z=0 จริง** ควรอยู่ **สูงเหนือผู้เล่นราว 930 หน่วย** คือบนฟ้า/เหนือผืนน้ำ ไม่ใช่บนดาดฟ้า — **คำคาดหมาย ไม่ใช่เกณฑ์ผ่าน**: ไม่มีใครวัดว่าไคลเอนต์ re-base พิกัดต่อฉากไหม และระยะเรนเดอร์เท่าไร

### nonclaims
1. ไม่เทส vehicle/ship transform (เจ้าของเลื่อนไว้เอง `M2-NO-VEHICLE-OWNER-20260827-1525`)
2. **ไม่เทสทางกลับจากทะเล — วันนี้ไม่มีทางกลับ ทางออกเดียวคือ relog** เขียนไว้ตรง ๆ เพื่อไม่ให้ผู้เทสติดค้างและไม่ให้เข้าใจผิดว่าเจอบั๊ก
3. ไม่ตัดสินว่าฉาก 17 หรือการอ่านแบบ `MarkerID` ของ `n_VARI_2` ถูก (CONTESTED · `ASK-COO 20260829_1410` เปิดอยู่)
4. **ทะเลที่ว่างเปล่าไม่ได้พิสูจน์ว่าเฟรม clear ทำงาน** — ไม่มีใครส่งมันเลย · มันพิสูจน์แค่ว่าไคลเอนต์ไม่ต้องใช้มันตรงนี้
5. **ไม่นับเป็นเวอร์ชัน** — รอบที่เปิดใบนี้ ship ศูนย์บรรทัดของ gameplay: เพิ่มบรรทัดรายงานคอนโซลหนึ่งบรรทัด ไม่มีเฟรมใหม่

### links
`GT-106` (รอบ attended ที่พิสูจน์ว่าฉาก 17 เดินได้) · `notes_to_chief/20260827_1710_GT106-RESULT-M2-Columbus-3021-enters-scene17-walkable-*.md` · `src/pirateforce_foundation/world_population_handoff.py` + `tests/test_world_population_handoff.py::ArrivalStowawayTests` · `notes_to_chief/20260826_0120_RE-077-RESULT-SCENE-TRANSITION-SEQUENCE-PINNED.md` (T5 ปิดแบบ BOUNDED NEGATIVE — ปฏิเสธทั้งสองการอ่าน จึงต้องใช้ตาคน) · `rounds/A_20260829_1422_2pdf6j_who-is-still-on-your-client-when-the-boat-lands.md`

**ผู้เปิดใบ: LANE-A (WORLD) รอบ `2pdf6j`** — ผลกลับมาที่สาย A บริโภค

### result (ผู้เทสกรอก)
```
P1 / P2 / P3        :
บรรทัดคอนโซลสี่บรรทัด (คัดดิบ) :
เห็นตัวละครอื่นไหม / กี่ตัว / ชื่อ / สูงหรือระดับดาดฟ้า :
เงยกล้องหรือไม่     :
สีป้ายชื่อทุกป้าย S0..S3 (บรรทัดละป้าย, ไม่มี = none) :
path + sha256 ของวิดีโอ/ภาพ/console/DB :
CANON_SHA ก่อน/หลัง · integrity_check · NO-CRASH/CRASH :
OBSERVER_CONFIRMED  :
```

## 🆕 GT-165 SLAVE-MARKET-ISLAND-FIRST-EYES-001 [attended, in-game]: เกาะตลาดทาส `Bg0004` (ฉาก 4) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  [~~READY~~ 🟢 **PASS ทั้งสองชั้น — LANE-A รอบ `qoj8ei` 2026-08-31T11:4x+07:00 ปิดหัวใบ ตามผล `notes_to_chief/20260831_1037_GT148-and-GT165-RESULT-stowaways-cleared-and-slave-market-island-has-life.md`: เจ้าของเข้าฉาก 4 จริง เดินสำรวจแล้วรายงาน "มีสิ่งมีชีวิตหลายตัว ทุกตัวดูเหมือนจะเป็นสิ่งมีชีวิตของที่นี่จริง ๆ"; wire ตรงเกณฑ์เป๊ะ `WORLD_CENSUS_BG0004 assembled=109/116` ทั้ง 7 ตัวที่ไม่ส่งมีเหตุผลระบุครบ**]

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `bq4mst`, 2026-08-31T06:4x+07:00 · `login_entry_allowed` ของฉาก 4 พลิกเป็น
> `true` รอบนี้ (`COO-DECISION 20260830_1441`, composer `world_population_bg0004.py`/`world_bg0004_identity.py`
> ที่สร้างรอบ `6p22bu` และผูกรอบ `2jdde8` ถูกตัดสินว่าพร้อมแล้ว) -- แยกออกจาก `GT-144` (สิบฉาก) เพราะฉากนี้เปิด
> เพียงฉากเดียวและมีเกณฑ์ของตัวเอง (ไม่มี faction bit เลย ต่างจากที่ `GT-144` เขียนไว้สำหรับกลุ่มรวม)

### objective (claim เดียว)
ล็อกอินเข้าฉาก 4 จริงแล้ว **เห็นตัวละคร/มอนสเตอร์ยืนอยู่บนเกาะ** (ไม่ใช่เกาะว่างเปล่า) ใช่หรือไม่ -- คำถามคือ
"มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม": composer ของฉากนี้**ตั้งใจไม่ส่ง faction bit เลย** (ดู
`world_population_bg0004.py` docstring -- เป็นคำตัดสินของสาย B ที่ยังไม่ทำ) จึงไม่มีความเสี่ยงแบบ `GT-134`
ที่มอนไม่ก้าวร้าว -- นั่นเป็นพฤติกรรมที่คาดไว้ ไม่ใช่ FAIL ของใบนี้

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 4 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=4) หรือ GM `/warp 4`

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
จุดเกิด `MARKER[4]` ยังเป็นชั้นหลักฐาน `authored` เท่านั้น -- ไม่เคยมีไคลเอนต์ยืนจริง, ห่างจาก placement
ที่ใกล้ที่สุด 777.5 หน่วย (`table_row_differences.marker_geometry_measured_not_enforced`) -- ถ้าตกในหิน/หลุด
พื้น ให้บันทึกเป็นข้อมูลแยก ไม่ใช่ FAIL ของใบนี้ (คำถามของใบนี้คือมี actor ไหม ไม่ใช่พื้นดีไหม)

### pass criteria — สองชั้น
**wire/DB (ปิดแล้วโดยเทส):** console line `WORLD_CENSUS_BG0004 assembled=109/116 ...` ปรากฏหลังล็อกอินเข้าฉาก 4
-- pin ไว้แล้ว `tests/test_lane_a_scene_census.py::OnTheRealDispatcherTests::
test_with_the_real_registry_the_slave_market_census_ships_109`
**client-observable (ยังไม่มีใครยืนดู -- นี่คือสิ่งที่ใบนี้ต้องการ):** ผู้เทสเข้าฉาก 4 จริงแล้วรายงานว่าเห็น
actor ขึ้นจอหรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 109)

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตา

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 4` (`login_entry_allowed_because`) ·
`src/pirateforce_foundation/world_population_bg0004.py`, `world_bg0004_identity.py` ·
`notes_to_chief/20260830_1441_COO-DECISION-scene4-slave-market-first-door.md` ·
`notes_to_chief/20260831_0643_LANE-A-STATUS-scene4-slave-market-island-opens.md` · `GT-144` (the other nine,
still shut) · `GT-134` (the sibling ticket for scene 14, same shape)

## GT-172 GM-003 CHAT-WARP-CROSS-SCENE-LIVE-TELEPORT-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากอื่น> x y` ในกล่องแชท -- จอเปลี่ยนไปฉากปลายทางจริงกลางเซสชันไหม (ไม่ต้อง relog)  [✅ **PASS ทั้งสองชั้น** -- ปิดโดย LANE-GM รอบ `k0w291` 2026-09-01T03:18+07:00 จากผล `notes_to_chief/20260901_0225_GT172-RESULT-PASS-*.md` (`OBSERVER_CONFIRMED 2026-09-01T01:2x+07:00`, เจ้าของขับเอง, วิดีโอ `evidence_video/1400_gt172_FULLROUND_20260901_011801.mkv`): `/warp 278 100 200` เปลี่ยนฉาก/พิกัดจริงบนจอ ไม่ relog, wire ยืนยัน `LANE_GM_CHAT_WARP_CROSS_SCENE_TELEPORT_VITAL` -> `TeleportVital` ยิงสำเร็จ 4/4 ครั้ง -- สามข้อสังเกตใหม่ระหว่างเทส (สำมะโนทะเบียนเก่า / ไม่มีจุดเกิดปลอดภัย / live warp ไม่ sync กับ stage) แยกไปเป็น `CORE-REQUEST-GM-045`, `CORE-REQUEST-GM-046`, และ FINDING ต่างหาก ไม่ใช่ FAIL ของใบนี้]

> เปิดโดย LANE-GM รอบ `fftpji`, 2026-08-31T16:40+07:00 · `COO-DECISION 2026-08-31T14:41+07:00`
> (`notes_to_chief/20260831_1441_COO-DECISION-warp-cross-scene-opens-gt106r2-passed.md`) เปิดทางให้
> `/warp <scene_id> x y` ข้ามฉาก**ที่มีพิกัด**ยิง `legacy.make_login_teleport` จริงกลางเซสชันแทนการ
> stage-รอ-login-หน้าเดิม (`gm/warp_executor.py::make_warp_teleport_frame_with_target`,
> `gm/chat_command_action.py::_warp_teleport_action`) · โค้ดอยู่บนรอบนี้ (`pirate-force-server`
> branch `claude/awesome-turing-fftpji`, PR `#398`) ยังไม่อยู่บน `main` จนกว่า PR จะ merge ·
> `GT-106-R2` (`OBSERVER_CONFIRMED 2026-08-31T10:0x+07:00`) พิสูจน์แล้วว่ากลไกเดียวกันนี้
> (`legacy.make_login_teleport` กลางเซสชัน) เคลื่อนจอจริงที่ฉาก 17 -- แต่ผ่าน call site อื่น
> (`_dispatch_columbus_quest3021`, พิกัดคงที่ X=834 Y=-598) ไม่ใช่ผ่านคำสั่ง `/warp` ของสาย GM เอง ·
> ใบนี้ถามคำถามที่ยังไม่มีใครตอบ: `/warp` เองที่ GM พิมพ์ ยิงแล้วจอเปลี่ยนจริงไหม ที่ปลายทางที่ GM เลือกเอง

### objective (claim เดียว)
GM login ด้วยบัญชีใน `gm_accounts.json` ยืนอยู่ฉากใดก็ได้ (ฉาก A) พิมพ์ `/warp 278 100 200` ลงกล่องแชทธรรมดา
(278 = "Beach Soccer Field" ตาม `gm/scene_catalog.py` -- ฉากที่ catalog รู้จักจริง ไม่ใช่ฉากพิเศษแบบ 17 ที่มี
call site อื่นเตรียมทางไว้แล้ว, และไม่ใช่ฉากที่ GM ยืนอยู่) -- **จอเปลี่ยนไปฉาก Beach Soccer Field ทันที
กลางเซสชันหรือไม่ (ไม่ต้อง logout/login)**  ถ้าจะเลือกฉากอื่นแทน 278 ก็ได้ ขอเพียงเป็นฉากที่
`scene_catalog.is_known_scene_id` คืน True และไม่ใช่ฉากปัจจุบันของ GM

### ทางเข้า
`/warp <scene_id> x y` เป็นบรรทัดแชทของ GM ทันที ไม่ต้องเตรียมไฟล์ config ใด ๆ ก่อน (ต่างจาก `GT-141` ที่
เทสรูปแบบ stage+relog) -- **ต้องระบุ x y เสมอ** เช่น `/warp 278 100 200`: รูปแบบไม่มีพิกัด (`/warp 278`
เฉย ๆ) ยัง stage-รอ-login-หน้าเหมือนเดิมทุกประการและไม่ใช่กลไกที่ใบนี้เทส (ไม่มีตำแหน่งให้ทั้งสอง
composer ส่ง เจตนา ไม่ใช่บั๊ก)

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
1. **census/actor ของฉากปลายทางไม่ตามไป** -- ช่องว่างเดียวกับที่ `RE-162` พบใน Columbus dispatch เอง
   (แม้แต่กลไกที่ chief เขียนเองก็ไม่ปิดช่องนี้) ฉาก Beach Soccer Field อาจดูโล่งแม้ catalog จะมีชื่อ NPC
   จริงก็ตาม -- **ไม่ใช่ FAIL ของใบนี้** (ใบนี้ถามแค่ "จอเปลี่ยนฉากไหม" ไม่ใช่ "ประชากรตามไปไหม")
2. **จุดลง (x,y,z) ที่ GM พิมพ์เองอาจตกในหิน/นอกแมพ** เพราะยังไม่มี range/ground-extent check (ช่องโหว่เดิม
   ที่บันทึกไว้ใน `gm/chat_command_action.py` ก่อนรอบนี้แล้ว ไม่ใช่ของใหม่รอบนี้) -- แนะนำเริ่มด้วยพิกัดใกล้
   จุดกำเนิด (`0 0`) ก่อน ถ้าตกพื้นแปลกให้บันทึกแยกเป็นข้อมูล ไม่ใช่ FAIL ของกลไกเปลี่ยนฉาก
3. **UI ค้างข้ามฉาก** -- `GT-106-R2` พบเพิ่มเติมว่าหน้าต่างบทสนทนา Columbus ค้างจอข้ามฉากแม้ actor จะถูกล้าง
   แล้ว (ยกเป็น `RE-168` แยก) อาจเกิดซ้ำกับใบนี้เพราะกลไกส่งเฟรมเดียวกัน -- บันทึกแยกถ้าเจอ ไม่ใช่ FAIL
   ของ "จอเปลี่ยนฉากไหม"
4. z ที่ส่งคือ z ปัจจุบันของ GM ณ ฉาก A (ไม่ใช่ z ที่เหมาะกับฉาก Beach Soccer Field) -- ถ้าตกใต้/เหนือพื้น
   ให้บันทึกแยก ไม่ใช่ FAIL

### pass criteria — สองชั้น
**wire/DB (ปิดแล้วโดยเทสเฮดเลส, ไม่ใช่ผลของใบนี้):**
`tests/test_gm_warp_executor.py::WarpTeleportCrossSceneTests` +
`tests/test_gm_chat_command_action.py::WarpActionTests` พิสูจน์ว่า `/warp <scene_id> x y` ข้ามฉากคืนไบต์
เดียวกับ `legacy.make_login_teleport(scene_id, 0, x, y, z)` เป๊ะไบต์ต่อไบต์ ภายใต้ action label
`LANE_GM_CHAT_WARP_CROSS_SCENE_TELEPORT_VITAL` -- นี่เป็น proof เชิงเฟรมเท่านั้น (bytes ออกไปถูกรูปถูกท่อ)
**ไม่ใช่หลักฐานว่าจอไคลเอนต์เปลี่ยน**

**client-observable (ใบนี้ถาม -- ยังไม่มีใครตอบ):** ผู้เทสพิมพ์ `/warp` เองแล้วรายงานตรง ๆ ว่าจอเปลี่ยนไปฉาก
ปลายทางจริงหรือไม่ (ชื่อฉาก/ภาพพื้นหลัง/มินิแมพเปลี่ยนตามที่ `gm/scene_catalog.py` ระบุ) เก็บ log คอนโซล
grep โทเคน `LANE_GM_CHAT_WARP_CROSS_SCENE_TELEPORT_VITAL` เทียบเวลากับสิ่งที่เห็นบนจอ

### ข้อห้าม
ห้ามประกาศ PASS ให้ปลายทางอื่นที่ไม่ได้เทสจริงในบูตเดียวกันโดยอิงผลของใบนี้ (กฎ G-OBS สาย GM เอง: ทุก
ปลายทางใหม่ต้องมีหลักฐาน client-observable ของตัวเอง, ระบุไว้ตรง ๆ ใน `COO-DECISION 1441` เช่นกัน) -- ใบนี้
ปิดได้แค่ปลายทางที่เทสจริงในบูตนั้น

### สัญญาผู้บริโภค
เปิดโดย LANE-GM -- LANE-GM บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตา (G-OBS)

### links
`notes_to_chief/20260831_1441_COO-DECISION-warp-cross-scene-opens-gt106r2-passed.md` ·
`notes_to_chief/20260831_1036_GT106R2-RESULT-PASS-client-renders-the-destination-scene-mid-session-plus-two-new-findings.md`
· `src/pirateforce_foundation/gm/warp_executor.py::make_warp_teleport_frame_with_target` ·
`src/pirateforce_foundation/gm/chat_command_action.py::_warp_teleport_action` ·
`docs/GM_LANE.md` รอบ `fftpji` · `GT-141` (สายเดิม stage-รอ-login-หน้า ยังใช้ได้สำหรับ `/warp` ไม่มีพิกัด)

**หมายเหตุผู้เขียนใบนี้:** ควรเขียนผ่านเอเจนต์ `pf-queue-author` ตามกติกาของโปรเจกต์ แต่ในสภาพแวดล้อมคลาวด์
รอบนี้ไม่มีเครื่องมือสำหรับ spawn subagent ชนิดนั้นเลย (ตรวจด้วย `ToolSearch`/`ListAgents` หลายคำค้นแล้วไม่พบ)
จึงเขียนเองตามรูปแบบของใบ `GT-171`/`GT-141` ให้ใกล้เคียงที่สุด -- ถ้ารูปแบบผิดจากมาตรฐานให้แก้ได้ตามที่
`pf-queue-author` เห็นสมควรในรอบถัดไป

## GT-182 GM-A-WARP-NO-COORD-LIVE-SPAWN-001  [PASS -- OBSERVER_CONFIRMED 2026-09-01T10:40+07:00, chief round 8zf80f]

> ✅ **PASS (chief round `8zf80f`), OBSERVER_CONFIRMED 2026-09-01T10:40+07:00:** attended session,
> Panya drove every keystroke herself (`notes_to_chief/consumed/20260901_1040_GT182-RESULT-*.md`).
> `/warp 3` typed with no coordinates, mid-session, no relog. Screen changed to Spice Paradise
> Island; landed X:-21,215 Y:16,907, standing on ground, walkable immediately -- F-2 from
> `GT-172` (float/stuck geometry from a carried-over z) does NOT reproduce on this no-coords
> form, confirming the `world_scene_travel.spawn_position()` anchor this entry's own background
> section asked for. Creatures were on screen before she moved. Wire:
> `LANE_GM_CHAT_WARP_CROSS_SCENE_NO_COORDS_TELEPORT_VITAL` (73 B) then
> `WORLD_POP_HANDOFF scene=3 kind=census actors=62` anchored on the destination's pinned spawn,
> not the departure coordinates -- F-1 from `GT-172` closed for this path (GM-045 + GM-047).
> Both (a) and (b) of this entry's single claim hold. Not covered by this PASS: whether a
> SECOND warp later in the same session would also get a census (the once-per-connection latch
> this same round's `runtime.py` fix addresses, see `rounds/` this round) -- out of scope for
> this entry's own claim, which is about the first warp only.

> ✅ **UNBLOCKED (chief round `69r41m`, R283):** the `20260901_0741_COO-DECISION-gm047-position-corruption-p0-block-gt182-until-fixed.md`
> warning is lifted. `CORE-REQUEST-GM-047` (registry row 028) landed on `main` in both repos this
> round -- `pull_request_read get` confirms `pf_bridge#680` and `pirate-force-server#452` both
> `merged: true` (`merged_at 2026-09-01T01:19:23Z` / `01:27:10Z`), and `runtime.py:5304` on
> `origin/main` was read directly this round and shows the three-label `_GM_WARP_LABELS` fix in
> place, not the old single-label check. The position-corruption risk this warning existed for no
> longer applies -- normal queue status resumes. Registry row 028 marked wired below.

> 🆕 **STATUS round `jd4jqp`:** the no-coordinate live-teleport branch this entry asks for is
> BUILT and TESTED (`gm/warp_executor.py::warp_no_coords_live_target`/
> `make_warp_teleport_frame_no_coords_with_target`, `gm/chat_command_action.py::
> _warp_teleport_action_no_coords`, new label `WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL`) --
> uses exactly `world_scene_travel.spawn_position(world_scene_travel.destination(scene_id))` as
> R278 asked, gated on `has_authored_entry` (n_MARKER != 0) so markerless scenes (17/126/278/997)
> keep the old stage-only rule per this entry's own nonclaim 4 (scene 278 specifically is a pinned
> regression test: `tests/test_gm_chat_command_action.py::ProductionCallShapeTests::
> test_the_default_argument_call_stages_where_gt141_says_it_does`). Full suite green headless
> (เขียว(cloud sanity), 6128 passed / 0 failed after rebase onto `main` post-`#438`). PR merged
> `2026-09-01T01:19:23Z`/`01:27:10Z` (confirmed round `69r41m`/R283, see UPDATE note below) -- was
> BLOCKED, now READY. Also see `GT-187`'s
> own status note this round: `_gm_warp_resync_selected_scene` (CORE-REQUEST-GM-045, merged
> `pirate-force-server#438`) covers this branch too for free, verified from source -- both
> `_warp_teleport_action` and this entry's `_warp_teleport_action_no_coords` call the same
> `_park_warp_target`, which is the only thing that mechanism keys on.
>
> 🆕 **UPDATE round `69r41m` (R283):** `CORE-REQUEST-GM-047` merged both repos
> (`pf_bridge#680`, `pirate-force-server#452`), confirmed via `pull_request_read get` and a direct
> read of `runtime.py:5304` on `origin/main` (now keys on all three `_GM_WARP_LABELS`). Registry
> row 028 marked wired. This entry is safe to run per the standard playbook now.
>
> Opened by chief this round, directly per Panya's order (not through pf-queue-author --
> no subagent-spawn tool available in this environment; written by hand in the shape of
> GT-181/GT-172/GT-141, per those entries' own stated fallback). Source: PANYA-ORDER
> `notes_to_chief/20260901_0215_PANYA-ORDER-drop-milestones-all-hands-on-three-things-plus-new-gm-and-ui-work.md`
> section 3 (GM-A), routed per PROCESS_GATES.md rule #18 (route tag required, additive to
> an OPEN/assigned tag, not a replacement). Build-owner lane: **LANE-GM** per chief's
> broadcast letter this round (`notes_to_chief/20260901_0302_FROM_CHIEF_R278_priority-reorg-panya-order-P1-P2-P3-plus-new-builds.md`).

- objective: single claim -- while already in a live session (any current scene), a GM
  account types `/warp <mapnum>` in the chat box with NO coordinate arguments, and the
  client (a) lands the character at that destination map's standard spawn point (the
  `MARKER` table entry resolved via `SCENE_NAME[n].n_MARKER`, per
  `COO-DECISION 20260829_0542_COO-DECISION-marker-table-is-the-default-spawn-source-with-an-evidence-label.md`
  -- NOT (0,0,0), NOT an arbitrary hand-typed coordinate, and NOT the GM's own carried-over
  z from the scene they warped from) AND (b) the scene switch happens immediately, mid
  session, with no logout/relogin. Today there are two behaviors and neither does both:
  `/warp <mapnum> x y` (with coordinates) already does a live, immediate, same-session
  scene switch (`GT-106-R2` PASS via a different call site; `GT-172` PASS -- confirmed
  2026-09-01, see below) but forces the GM to type exact coordinates by hand and the
  server sends whatever z the GM was already standing at in the OLD scene, which `GT-172`
  itself measured as finding F-2: the owner lands stuck in geometry / floating, unable to
  fall to the floor, because the wrong z is carried over. `/warp <mapnum>` with no
  coordinates only calls the stage path (`GT-141` PASS: writes
  `config/gm_login_scene.json` for the NEXT relog: it does not touch the live session at
  all). This entry is what proves the NEW, combined behavior the owner asked for.
- background (read before touching anything):
  - `notes_to_chief/consumed/20260829_0542_COO-DECISION-marker-table-is-the-default-spawn-source-with-an-evidence-label.md`:
    marker-derived spawn points are an `authored` evidence tier, not `client-observed` --
    most scenes have never had a client actually stand on their marker. If the GM lands in
    rock/underground/off-map at the destination, record that as separate data, it is not a
    FAIL of this entry's own claim (which is "did the scene switch happen and did the
    server target the marker coordinate", not "is the marker geometry good").
  - `GT-172` RESULT (PASS, `OBSERVER_CONFIRMED 2026-09-01T01:2x+07:00`): confirms the live
    cross-scene teleport plumbing (`gm/warp_executor.py`, `gm/chat_command_action.py`)
    already sends a real `TeleportVital` that moves the client mid-session with no relog.
    It also found F-1 (wrong-scene census follows the player to the destination, using the
    OLD scene's registry with the NEW scene's anchor coordinate) and F-2 (z carried over
    from the old scene, character floats/sticks). **The implementing lane for this ticket
    should build the no-coordinate branch using `world_scene_travel.spawn_position()` as
    the anchor (the same call already used by the bg0002 eager-census arrival path, see
    `runtime.py` ~7420-7452) instead of accepting a caller-supplied z** -- this sidesteps
    F-2 by construction for THIS branch, though it does not fix F-2 for the with-coordinates
    branch, and F-1 (census timing/registry mismatch) is a separate, still-open bug this
    entry does not close either.
  - GT-141's PASS already proves the STAGE half of this in isolation (no coords -> next
    relog lands correctly); this entry does not repeat that, it only tests the NEW
    combination (no coords + live + immediate).
- db: fresh copy of `state\pirateforce.sqlite3` for this boot (never the canonical file) --
  record the copy's filename and sha256 before/after; verify the canonical file's own
  sha256 is unchanged before and after this round.
- server args: standard boot, `-SecondPasswordMode bypass`, using a GM account already
  present in `config/gm_accounts.json` (or a test copy pointed to by
  `PF_GM_ACCOUNTS_CONFIG` if the real allowlist should not be touched). Requires whatever
  PR lands the new no-coordinate live-spawn branch to be merged to `main` first -- this
  entry cannot be run meaningfully before that (see RECHECK below).
- steps:
  1. Boot server + client per standard playbook. Confirm server has been running under 3.5
     minutes before the client connects and that this is a fresh server start (not a
     server left over from a previous, already-killed client).
  2. Log in with the GM account. Note starting scene (scene A) and starting X/Y/Z from the
     HUD.
  3. Right-click-drag the camera only (never Q/E, never WASD) to get a clean baseline view
     of the character. Screenshot, full resolution, labelled BASELINE. Record: scene
     name/background shown, HUD X/Y/Z, and the colour of every name label visible in
     frame (one line per label, write "none" if nothing else is in view).
  4. Click into the chat input box and confirm focus. Type exactly `/warp <mapnum>` for a
     destination map that is NOT scene A and IS known to `gm/scene_catalog.py`
     (`is_known_scene_id` True) and DOES have a nonzero `n_MARKER` per the registry (pick
     one already opened by LANE-A, e.g. scene 4/5/6/8/10). Press Enter.
  5. Wait ~2 seconds. Screenshot, full resolution, labelled STEP-A. Record: did the scene
     visibly change (background/scene name/minimap) with NO relog/loading-screen-to-login
     step, HUD X/Y/Z (compare against the destination scene's `MARKER[n_MARKER]`
     coordinate, not against scene A's coordinate), dead/stuck-in-geometry state if any,
     and every name label's colour again.
  6. If the scene did not change within ~10 seconds, stop -- this is the negative result
     this entry is built to catch (see pass criteria).
- pass criteria (two layers, kept separate):
    wire/DB: the server console/capture log for this boot shows a single `/warp <mapnum>`
      chat line (no coordinate arguments) producing a `TeleportVital`/`make_login_teleport`
      frame (whatever action label the implementing lane uses for this new branch) whose
      target X/Y/Z decode to the exact `MARKER[n_MARKER]` row for the destination scene,
      not (0,0,0) and not the GM's prior X/Y/Z. This is headless-provable and needs no
      human at the screen; it proves the bytes sent were correct, not that the client did
      anything with them.
    client-observable: what the human at the screen reports for STEP-A per step 5 above --
      did the scene actually change on screen (background/minimap/scene name), did it
      happen without any relog/login-screen step, and did the character appear to land on
      walkable ground rather than visibly stuck in geometry. The three-part prediction
      this entry falsifies: (i) scene changes without relog, (ii) landing coordinate
      matches the marker (not the GM's old z), (iii) character is not visibly stuck. Any
      one of these being false is a valid, useful negative result -- write up which part
      failed, do not describe the whole entry as a blanket FAIL without saying which
      sub-claim broke.
- nonclaims:
  1. Does not confirm the destination scene's marker geometry is good (per the
     `authored`-not-`confirmed` caveat) -- a landing inside rock is recorded as data about
     that scene's marker, not as a FAIL of "did warp switch scenes with no coordinates".
  2. Does not test census/actor population of the destination scene following the switch
     (F-1 from `GT-172` is a separate, still-open bug).
  3. Does not test `/warp <mapnum> x y` (with coordinates) again -- that is `GT-172`,
     already PASSed/separately tracked (its own F-1/F-2 findings remain open elsewhere).
  4. Does not test warping to a scene with `n_MARKER == 0` (no marker) -- per the
     COO-DECISION, those scenes keep the OLD rule (client evidence / owner ruling /
     refusal) and are out of scope for "standard spawn point" as this entry defines it.
  5. Does not claim any UI dialog (e.g. a stale NPC conversation box, per `RE-168`) is
     fixed by this change -- if one appears, log it separately, it is not this entry's FAIL.
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="GM-A" --grep="warp.*no.coord" --grep="GT-182" | head -5`
  (non-empty as of round `69r41m`/R283 -- the no-coordinate live-spawn branch AND its
  CORE-REQUEST-GM-047 position-resync fix are both on `main`; this entry is READY, not BLOCKED).
- links: `notes_to_chief/20260901_0215_PANYA-ORDER-drop-milestones-all-hands-on-three-things-plus-new-gm-and-ui-work.md`
  (section 3, GM-A) -- `notes_to_chief/consumed/20260829_0542_COO-DECISION-marker-table-is-the-default-spawn-source-with-an-evidence-label.md`
  -- `rounds/GM_20260831_1640_fftpji_warp_cross_scene_live_teleport.md` -- `GT-106-R2`,
  `GT-172` (with-coordinates live warp, PASS with F-1/F-2 open findings), `GT-141`
  (no-coordinates stage-only warp) -- `PROCESS_GATES.md` rule #18.
- numbering: this batch (GT-182 through GT-186) was opened after re-running the shared
  counter's own search command against `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`, and
  `archive/*QUEUE*ARCHIVE*.md`; highest confirmed prior number was `GT-181`. This entry is
  `182`.
- result: (tester/build lane fills in: PASS/FAIL/BLOCKED, evidence, timestamp,
  OBSERVER_CONFIRMED line per G-OBS once client-observable evidence exists)

## GT-187 GM-045-CENSUS-SCENE-RESYNC-CLIENT-CONFIRM-001  [❌ **CANCELLED - no longer needs proving because ทางเข้าของใบนี้ไม่มีอยู่บน `main` วันนี้** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2) — R307 วัดแล้วว่ารูป cross-scene ที่มีพิกัดถูก `WarpExecutorError` ปฏิเสธบน main (`notes_to_chief/20260903_1901_*` หัวข้อ `GT-187 -> [NO-RESULT]`) และ `COO-DECISION 20260903_1744` ข้อ 3 สั่งให้ LANE-GM ปฏิเสธรูปนั้นพร้อมบรรทัดคอนโซล ไม่มีไบต์ออก ⇒ ใบนี้เทสสิ่งที่เซิร์ฟเวอร์ตั้งใจไม่ทำ · 🔴 **census resync หลังวาปยังต้องพิสูจน์อยู่** แต่พิสูจน์ผ่านรูปที่ไม่มีพิกัด ซึ่งเป็นของ `GT-192` · เปิดใบใหม่เมื่อ LANE-GM ลงรูปเฟรมใหม่ · สถานะเดิม: READY -- `pirate-force-server#438` merged, verify below]

> เปิดโดย pf-queue-author ตามคำขอของ chief รอบ `lperai` หลังต่อสาย `_gm_warp_resync_selected_scene`
> แก้ `CORE-REQUEST-GM-045` (F-1 ของ `GT-172`: WORLD-CENSUS-001 อ่านทะเบียนฉากต้นทางแทนฉากปลายทาง
> หลัง live warp ของสาย GM) -- โค้ดอยู่บน branch `claude/trusting-mendel-lperai`, PR `#438`, ยังไม่
> merge เข้า `main` ตอนเปิดใบนี้ (ดู `notes_to_chief/20260901_0403_CHIEF-REPLY-CORE-REQUEST-GM-045-scene-resync-wired.md`
> ข้อสุดท้าย) ใบนี้เป็นครึ่งที่ chief เขียนขอเองในจดหมายฉบับนั้น: "ไม่พิสูจน์ว่าไคลเอนต์จริงเห็น
> สำมะโนถูกฉากหลังแก้ ... ต้องมีรอบ attended ยืนยันซ้ำ (เสนอ GT ใหม่ในคิว แยกใบ)"
>
> 🆕 **สถานะแก้ รอบ `jd4jqp`:** `pirate-force-server#438` `merged=true`
> `2026-08-31T21:25:15Z` (ยืนยันด้วย `pull_request_read(method=get)`, ไม่ใช่แค่อ่านใบ) -- เงื่อนไข
> BLOCKED เดิม ("รอ merge") หมดแล้ว ใบนี้พร้อมให้ผู้เทส attended หยิบทำได้ทันที (แก้เฉพาะป้ายสถานะ
> ไม่แตะ objective/steps/pass-criteria/nonclaims ข้างล่าง) ⇒ ตอบ nonclaim 3 เดิมด้วย (ไม่ใช่การเดา
> ไล่จาก diff จริง `git show ff04ee5`): **ใช่ โค้ดร่วมกันบางส่วนจริง** --
> `_gm_warp_resync_selected_scene` ไม่ได้ผูกกับ action-label string ใด ๆ เลย มันอ่าน
> `WarpTargetRecord` ที่ `gm/chat_command_action.py::_park_warp_target` park ไว้บน session attribute
> เดียวกันทุกกิ่งของ `/warp` ที่ข้ามฉากแบบ live -- ทั้ง `_warp_teleport_action` (มีพิกัด, ใบนี้ทดสอบ)
> และ `_warp_teleport_action_no_coords` (ไม่มีพิกัด, `GT-182`'s GM-A, สร้างรอบ `jd4jqp`) เรียก
> `_park_warp_target` ตัวเดียวกันเป๊ะ ⇒ `_gm_warp_resync_selected_scene` ครอบคลุม GM-A ให้ฟรีโดยไม่ต้อง
> ต่อสายเพิ่ม -- ยังไม่มีรอบ attended ยืนยันทั้งคู่ (ทั้งใบนี้และ `GT-182`) แค่ยืนยันว่า wire/DB
> mechanism เดียวกันจริงจากการอ่านซอร์ส ไม่ใช่การเดา

- objective: claim เดียว -- หลังคำสั่งแชท `/warp <ฉาก> x y` ข้ามฉากแบบ live ของสาย GM (คำสั่งเดียวกับที่
  `GT-172` PASS ไว้แล้ว) การ dispatch `WORLD-CENSUS-001` รอบถัดไป **อ่าน scene_id ของฉากปลายทาง ไม่ใช่
  ฉากต้นทาง** ทั้งสองชั้น: (ก) บรรทัดคอนโซล/log ฝั่งเซิร์ฟเวอร์ และ (ข) สิ่งที่มนุษย์เห็นบนจอจริง --
  actor ที่ปรากฏใกล้ตำแหน่งจริงของตัวละครบนจอ ไม่ใช่ทะเบียนของฉากต้นทางที่ลากพิกัดปลายทางมาใช้
  (อาการที่ `GT-172` วัดได้ 4/4 ครั้งก่อนแก้) ใบนี้เป็นการยืนยัน attended ของสิ่งที่ chief แก้ไว้แล้วบน
  wire/DB (`tests/test_gm_warp_position_confirmed.py::GmWarpSelectedSceneResyncTests`) เท่านั้น --
  ไม่ทดสอบ F-2 (z ค้างจากฉากเก่า, `CORE-REQUEST-GM-046`) หรือ F-3 (live warp ไม่ sync กับค่า stage)
- db: สำเนาสดของ `state\pirateforce.sqlite3` สำหรับบูตนี้เท่านั้น (ห้ามเปิด canonical) -- จดชื่อไฟล์
  สำเนา + sha256 ก่อน/หลัง และยืนยัน sha256 ของไฟล์ canonical ไม่เปลี่ยนก่อน/หลังรอบนี้
- server args: บูตมาตรฐาน, `-SecondPasswordMode bypass`, บัญชี GM จาก `config/gm_accounts.json`
  (หรือสำเนาทดสอบผ่าน `PF_GM_ACCOUNTS_CONFIG` ถ้าไม่อยากแตะ allowlist จริง) ต้องรอ
  `pirate-force-server#438` merge เข้า `main` ก่อน -- ดู RECHECK
- steps:
  1. บูตเซิร์ฟเวอร์+ไคลเอนต์ตาม playbook มาตรฐาน -- ยืนยันเซิร์ฟเวอร์ขึ้นก่อนไคลเอนต์ต่อ และอายุยังไม่ถึง
     3.5 นาที -- ยืนยันเป็นเซิร์ฟเวอร์ใหม่ (ไม่ใช่ตัวที่เหลือจากไคลเอนต์ที่ถูกฆ่าไปก่อนหน้า)
  2. ล็อกอินด้วยบัญชี GM หมุนกล้องด้วย right-click-drag เท่านั้น (ห้าม Q/E ห้าม WASD ตอนนี้ -- ยังไม่ถึง
     ตัวยิง) เพื่อดูมุมสะอาด ถ่ายภาพความละเอียดเต็ม ป้าย BASELINE บันทึกชื่อฉาก, X/Y/Z จาก HUD, และสี
     ของป้ายชื่อทุกป้ายในเฟรม (บรรทัดละหนึ่งป้าย เขียน "none" ถ้าไม่มี)
  3. คลิกเข้ากล่องแชท ยืนยันโฟกัสแล้วพิมพ์ให้ตรงเป๊ะ `/warp 278 100 200` (หรือฉากปลายทางอื่นที่
     `gm/scene_catalog.py::is_known_scene_id` คืน True และไม่ใช่ฉากปัจจุบัน -- `GT-172` ใช้ 278
     "Beach Soccer Field"; ถ้าจะเทียบกับ baseline วิดีโอเดิมของ `GT-172` ให้ใช้ฉากเดียวกัน) กด Enter
  4. รอ ~2 วินาที (จาก `GT-172` การสลับฉากเกิดสด ไม่ต้อง relog) ถ่ายภาพ STEP-A ความละเอียดเต็ม บันทึก:
     ฉากเปลี่ยนจริงไหม (พื้นหลัง/มินิแมป/ชื่อฉาก), X/Y/Z จาก HUD, และสีป้ายชื่อทุกป้ายอีกครั้ง
  5. ยืนรอ/เดินสั้น ๆ ต่ออีก ~5 วินาที (ขยับ WASD ได้ตรงนี้ -- อยู่หลังตัวยิงแล้ว ไม่ใช่ก่อน) ให้ผ่านรอบ
     dispatch `RuntimeReq`/สำมะโนถัดไปอย่างน้อยหนึ่งรอบ ถ่ายภาพ STEP-B บันทึกสีป้ายชื่อทุกป้ายอีกครั้ง และ
     ว่ามี actor ปรากฏใกล้ตำแหน่งจริงของตัวละครบนจอหรือไม่
  6. จดเวลานาฬิกาแขวนของทุกขั้นตอน เพื่อเทียบกับ console/capture log ของเซิร์ฟเวอร์ภายหลังรอบ
- pass criteria (สองชั้น แยกกัน):
    wire/DB: console/capture log ของบูตนี้ สำหรับ `RuntimeReq` dispatch ที่ตามหลังบรรทัดแชท
      `/warp 278 100 200` ต้องพิมพ์ `WORLD_CENSUS ... scene=278` (ฉากปลายทาง ไม่ใช่ `scene=bg0001`
      หรือฉากต้นทางอื่นที่ GM ยืนอยู่ก่อนวาร์ป) พร้อม actor อย่างน้อยหนึ่งตัวจากทะเบียนของฉาก 278 เอง
      (ไม่ใช่ทะเบียนฉากต้นทางที่ลาก anchor ปลายทางมาใช้ -- อาการที่ `GT-172` F-1 วัดได้ 4/4 ครั้งก่อนแก้)
      ชั้นนี้พิสูจน์ได้แบบ headless ไม่ต้องมีคนหน้าจอ พิสูจน์แค่ว่าไบต์/log ที่เซิร์ฟเวอร์ผลิตถูกต้อง
      ไม่ได้พิสูจน์ว่าไคลเอนต์วาดอะไรออกมา
    client-observable: สิ่งที่มนุษย์หน้าจอรายงานจาก STEP-A/STEP-B ตามข้อ 4-5 -- ฉากเปลี่ยนจริงบนจอไหม
      โดยไม่มี relog และ actor ที่ปรากฏใกล้ตำแหน่งจริงของตัวละคร (จากภาพถ่าย) ดูสมเหตุสมผลว่าเป็นของฉาก
      ปลายทาง ไม่ใช่เศษที่เหลือจากฉากต้นทางที่จำได้ (เช่นถ้าเห็น actor/ป้ายชื่อใดยืนอยู่ที่พิกัด anchor
      ของฉากเก่าราวกับหลุดมาจากมุมมองใหม่ ให้บันทึกแยกเป็นข้อสังเกต) ผลลบ (ไม่เห็น actor เลยทั้งสองแบบ
      หรือ actor ที่ดูเหมือนซ้ำกับประชากรของฉากต้นทาง) เป็น finding ที่มีค่าเท่าผลบวก -- เขียนว่า sub-claim
      ไหนพัง อย่าสรุปเป็น FAIL รวมทั้งใบ
- nonclaims:
  1. ไม่ทดสอบหรือยืนยัน F-2 (z ค้างจากฉากเก่า / ลอย-ติดโครงสร้างตอนลง) -- นั่นคือ `CORE-REQUEST-GM-046`
     ติดตามแยกต่างหาก
  2. ไม่ทดสอบ F-3 (live warp ไม่ sync กับค่า stage ที่ใช้ตอน relog ถัดไป) -- FINDING แยก ไม่ใช่ claim
     ของใบนี้
  3. ไม่ทดสอบ `/warp <mapnum>` แบบไม่ใส่พิกัด -- นั่นคือ `GT-182` คนละเส้นทางโค้ด (`_gm_warp_resync_selected_scene`
     อาจเป็นโค้ดร่วมกันบางส่วน -- ถ้าใช่ ให้เขียนไว้ในผลของใบนี้พร้อมอ้างอิงไขว้ แต่ยังต้องเกรดใบนี้ด้วย
     claim ของตัวเอง)
  4. ไม่อ้างว่าทะเบียน actor ของฉากปลายทางถูกต้อง/ครบถ้วนโดยรวม -- อ้างแค่ว่า census dispatch อ่าน
     scene_id ถูกต้อง และมนุษย์เห็น actor ที่ดูสมเหตุสมผลว่าเป็นของฉากนั้น ไม่ใช่เศษของฉากต้นทาง
  5. ผล wire/DB ของใบนี้ไม่ใช่หลักฐานแทนผล client-observable และในทางกลับกันก็ไม่ใช่ -- จดหมายของ chief
     เองระบุว่าตัวแก้พิสูจน์แค่ wire/DB (`tests/test_gm_warp_position_confirmed.py::GmWarpSelectedSceneResyncTests`,
     สวีตเต็ม 6127 passed / 0 failed) ไม่มีไคลเอนต์เกี่ยวข้องเลย -- ใบนี้คือครึ่งที่ปิดฝั่ง
     client-observable
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="GM-045" --grep="_gm_warp_resync_selected_scene" --grep="GT-187" | head -5`
  (แก้รอบ `jd4jqp`: ตอนนี้มีผลจริง -- `ff04ee5 Wire CORE-REQUEST-GM-045: resync selected scene after
  live GM warp` อยู่บน `main` แล้ว ผ่าน PR `#438` -- เดิมข้อความนี้บอก "ไม่มีผลลัพธ์ = ยังไม่ merge",
  ตอนนี้ล้าสมัยไปแล้ว สถานะ READY ด้านบนคือของจริง)
- links: `notes_to_chief/consumed/20260901_0318_LANE-GM-CORE-REQUEST-GM-045-census-uses-stale-scene-after-live-chat-warp.md`
  (ใบขอต้นเรื่อง F-1) -- `notes_to_chief/20260901_0403_CHIEF-REPLY-CORE-REQUEST-GM-045-scene-resync-wired.md`
  (คำตอบ+ตัวแก้ของ chief, PR #438, ผลเทส wire/DB) -- `GT-172` (PASS, live cross-scene warp ที่ใบนี้
  ขับซ้ำ, เปิด F-1/F-2/F-3) -- `GT-182` (ใบพี่น้อง ไม่ใส่พิกัด, คนละเส้นทางโค้ด) -- `PROCESS_GATES.md`
  rule #18
- numbering: ตามคำสั่งค้นหาของตัวนับร่วม (กฎ ② หัวไฟล์) เลขสูงสุดที่ยืนยันได้ก่อนหน้าใบนี้ข้าม
  `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`, และ `archive/*QUEUE*ARCHIVE*.md` คือ `GT-186` ใบนี้คือ `187`
- result: (ผู้เทสกรอก: PASS/FAIL/BLOCKED, หลักฐาน, เวลา, บรรทัด OBSERVER_CONFIRMED ตาม G-OBS เมื่อมี
  หลักฐาน client-observable แล้ว)

## GT-192 GM-A-WARP-MULTI-MAP-CENSUS-CHAIN-001  [✅ **PASS สองชั้น · OBSERVER_CONFIRMED 2026-09-03T18:5x+07:00** (chief รอบ `pk14rf`/R326 เกรดตาม `COO-DECISION 20260903_1743` ข้อ 2 — ห้ามปั๊ม PASS จากชั้นเดียว จึงระบุทั้งสองชั้นและข้อที่ไม่ครบ) — **ชั้นจอ (R307 เจ้าของเอง):** `/warp 3,4,5,6,7,8,9,10,11,14,130` แล้ว `/warp 1` · NPC/HP/LV ดูปกติทุกแมพ ไม่มีแมพว่าง · **ชั้น wire:** census ตอนถึงตรงกับตัวเลขที่ใบทำนายทุกแมพ (3=62 · 4=109 · 5=87 · 6=66 · 7=56 · 8=69 · 9=57 · 10=94 · 11=51 · 14=81 · 130=41) และ `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED` = 0 · จดหมายผล `notes_to_chief/20260903_1901_KA1A-R307-RESULTS-*.md` · 🔴 **ข้อที่ไม่ครบ ระบุตามคำสั่ง:** (ก) ข้อ "เก็บฟรี" ของ `1743` ข้อ 1 (กลับมาแมพแรกแล้วป้ายเขียวของตัวที่เคยเห็นยังอยู่ไหม) **ไม่ถูกถ่าย/ไม่ถูกถอดความ** — ไม่ใช่เกณฑ์ FAIL ของใบนี้ตามคำสั่งเดียวกัน เจ้าของอาการเมื่อเกิดซ้ำ = LANE-A หลัง P-2 · (ข) `MOB_CENSUS_HOSTILITY roster=0` ทุกฉากที่วาปไป = คนละใบ (M4 · แก้ชั้นที่หนึ่งแล้วรอบ `pk14rf`) · (ค) แชทฉาก 130 ขึ้นบรรทัดเหลือง "เป้าหมายไม่มีอยู่/ไปไม่ถึง" หกครั้ง = บันทึกไว้ ไม่อ้างสาเหตุ · สถานะเดิม: 🟢 READY (R306, 2026-09-02T17:2x+07:00) -- ของอยู่บน `main` ครบแล้ว ตัวบล็อกเดียวคือคนบูต · หนี้หัวใบตาม `COO-DECISION 20260902_0544` (รายการปิด + ฉาก 1 เดินหนึ่งก้าว) **ปิดในรอบนี้** หลัง LANE-GM ทวงในใบ `20260902_1526` — R299/R305 เคยบันทึกว่าทำแล้ว ซึ่งไม่จริง]

> Opened by chief (round `liq4ri`, cloud) per `COO-DECISION 20260901_1341_COO-DECISION-census-latch-verified-on-main-open-gt-entry-for-multimap-warp-plus-queue-summary-fix.md`
> item 1, itself answering `notes_to_chief/20260901_1256_KA1A-TO-COO-census-latch-fix-landed-on-main-NOW-md-needs-updating-and-GM-A-is-testable-again.md`.
> `notes_to_chief/reference` for this entry's spec: `20260901_1035_KA1A-ROOTCAUSE-one-census-per-login-world_census_sent-is-a-connection-latch.md`
> (the bug and fix items 1-3) and `20260901_1120_KA1A-AMENDMENT-my-1035-fix-spec-item-4-is-unsafe-as-written-lane-A-already-measured-why.md`
> (item 4, scene-1 eager census, deliberately NOT part of this fix or this entry -- see nonclaim 4).
> Build-owner lane for this ticket's underlying fix: the census-latch clear already landed on
> `main` (verified this round by COO directly from source, `pirate-force-server@81952ce`,
> `runtime.py:5459-5470`) -- this entry exists to get the one thing nobody has yet: an attended
> human confirming the client actually renders a SECOND (and third, fourth...) census inside one
> TCP connection, not just the first one `GT-182` already proved.
>
> numbering: `grep -ohE '\b(GT|RE)-[0-9]{3}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md
> archive/*QUEUE*ARCHIVE*.md | grep -oE '[0-9]{3}$' | sort -n | tail -1` returned `191`
> (`RE-191`) at the time this entry was opened -- this entry is `192`.

- objective: single claim -- starting from an already-logged-in live session (any starting
  scene), a GM account types `/warp <mapnum>` down the **closed list in step 3** (12 marker-backed
  scenes, then scene 1 last), and at each of the TWELVE marker-backed destinations the client renders
  a normal NPC population, not an empty map.
  🔴 **ฉาก 1 ถูกตัดสินด้วยกฎของขั้น 4 ไม่ใช่ด้วยประโยคนี้** (ว่างตอนมาถึงโดยตั้งใจ · nonclaim 1 ข้างล่าง
  ไม่ใช่ nonclaim 4 -- การอ้าง "nonclaim 4" ในประโยคเดิมผิดมาตั้งแต่ก่อนรอบ R306 และแก้ตรงนี้)
  `GT-182` already
  proved the FIRST warp of a session gets a census; this entry is the one thing that PASS did
  not cover, stated explicitly in its own PASS note: "whether a SECOND warp later in the same
  session would also get a census... out of scope for this entry's own claim, which is about
  the first warp only."
- background: ย้ายทั้งบล็อกไปที่ `archive/GT192_BACKGROUND_verbatim_20260902.md` (chief รอบ `xkmzxr`/R306 ·
  เหตุ: เพดานใบ 12,000 อักขระ · ไม่มีการลบ ไม่มีขั้นตอนความปลอดภัยถูกตัด) — อ่านก่อนแตะอะไรถ้าต้องการที่มาของบั๊ก
- db: fresh copy of `state\pirateforce.sqlite3` for this boot (never the canonical file) --
  record the copy's filename and sha256 before/after; verify the canonical file's own
  sha256 is unchanged before and after this round.
- server args: standard boot, `-SecondPasswordMode bypass`, using a GM account already
  present in `config/gm_accounts.json`. Requires `pirate-force-server@main` at or after
  `81952ce` (the commit COO read `runtime.py:5459-5470` from this round) -- see RECHECK below.
  🔴 **เซิร์ฟเวอร์ห้ามรันด้วย `--second-password-mode` ที่ไม่ใช่ `required` · ห้ามมี `--*-scenario` แม้ตัวเดียว
  · และห้าม `--world-census-actors`** (สองข้อแรกปิดสำมะโนทั้งหมด ⇒ ทั้ง 13 แมพขึ้นจอว่าง และนั่นคือ**การบูต ไม่ใช่บั๊ก**
  ⇒ ใบนี้จะอ่านเป็น FAIL ผิด ๆ · ข้อสามไม่ได้ปิดสำมะโนแต่ย้ายจำนวน actor ⇒ ตารางในขั้น 3 ใช้เทียบไม่ได้)
  ยืนยันด้วยชื่อ ไม่ใช่ด้วยเลขบรรทัด (ไฟล์โต เลขเลื่อน):
  `git grep -n "world_census_enabled = " -- src/pirateforce_foundation/runtime.py`
  ต้องได้ `world_census_enabled = (not active_lanes and second_password_mode == "required")`
  (`active_lanes` ประกอบจากแฟล็ก `--*-scenario` ทั้ง 27 ตัวใน `app.py` · chief วัดเองรอบ `xkmzxr`)
  `-SecondPasswordMode bypass` ที่เขียนไว้บรรทัดบนเป็นแฟล็กของ **ไคลเอนต์** (ขีดเดียว) คนละตัวกับแฟล็กเซิร์ฟเวอร์ (สองขีด)
  ตัดสินโดย chief รอบ `xkmzxr` (R306) ตามที่ LANE-GM เสนอในใบ `20260902_1604` — ใบนี้ chief เป็นผู้เปิดเอง
- preflight (ไม่บังคับ · **ทำก่อนบูต** ถ้าจะทำ · ทำไม่ได้ก็ข้ามได้ ใบนี้ไม่ผูกกับมัน):
  ให้จ็อบฝั่งสะพานรัน แล้วเก็บลงไฟล์ (คอนโซลของผู้เทสเป็น PowerShell/cp874 — บรรทัด bash ใช้ไม่ได้):
  ```
  cd <repo>\pirate-force-server
  $env:PYTHONPATH = "src"
  py -3 -m pirateforce_foundation.gm.warp_chain_preflight *> preflight_gt192.txt
  ```
  แนบไฟล์นั้นมากับผล · output จริง ~44 บรรทัด (stdout 16 + stderr ~28) ทั้งหมด ASCII
  🔴 มันทำนาย**สิ่งที่เซิร์ฟเวอร์ประกอบ** ไม่ใช่สิ่งที่ไคลเอนต์วาด — จอไม่ตรงตารางคือของที่ใบนี้ตามหา
  🔴 **บรรทัด `LANE_A_CENSUS_SKIPPED scene=2 ... reason=reserved_by_a_runtime_branch` ใน output ของมันไม่ใช่คำเตือน**
  ฉาก 2 ส่งสำมะโนของตัวเองจากแขนอื่นของ `runtime.py` (97 ตัว) ⇒ **ฉาก 2 ว่างบนจอ = ผลลบที่มีค่า ไม่ใช่ "by design"**
- steps:
  1. Boot server + client per standard playbook. Confirm a fresh server start (not reused
     from a previous client).
  2. Log in with the GM account into any scene. Let the FIRST census for this session land
     and confirm NPCs are visible (this is `GT-182`'s own claim, not re-tested here in
     detail -- just confirm the session is past its first census before warping).
  3. 🔴 **รายการปิด ไม่ใช่ "เลือกเอง"** (`COO-DECISION 20260902_0544` · LANE-GM วัดประตู production
     `warp_executor.warp_no_coords_live_target` ครบ 330 ฉากแล้วได้ 13 ฉากนี้พอดี ฉากนอกชุดถูกปฏิเสธด้วยชื่อ
     · chief วัดซ้ำเองในรอบ `xkmzxr` ได้ชุดเดียวกันเป๊ะ):
     พิมพ์ `/warp <เลข>` ทีละฉาก **เรียงตามนี้** ในล็อกอินเดียวไม่ตัดการเชื่อมต่อ
     `2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 130` แล้ว**ปิดท้ายด้วย `1`**
     ทุกฉาก: Enter → รอ ~3 วินาที → **สกรีนช็อตก่อนคลิกอะไรทั้งสิ้น** ตั้งชื่อ `MAP-<เลขฉาก>` →
     จด ชื่อฉาก/ฉากหลัง · HUD X/Y/Z · **ประมาณจำนวน NPC ที่เห็น** (ไม่ต้องจดชื่อครบทุกตัว 41-109 ตัวต่อแมพ)
     🔴 แมพไหนที่ดู **ว่างหรือน้อยผิดปกติ** ค่อยจดชื่อ NPC ทุกตัวพร้อมสีให้ครบ — นั่นคือแมพที่ใบนี้ตามหา
     จำนวน actor ที่เซิร์ฟเวอร์จะประกอบตอนมาถึง (จาก `warp_chain_preflight` ของ LANE-GM รอบ `0aij4z`
     · chief วัดซ้ำรอบ `xkmzxr` ตรงทุกตัว · **ใช้เทียบ ไม่ใช่เกณฑ์ผ่าน**):
     `2`=97 · `3`=62 · `4`=109 · `5`=87 · `6`=66 · `7`=56 · `8`=69 · `9`=57 · `10`=94 · `11`=51 · `14`=81 · `130`=41
     🔴 **เดินหนึ่งก้าว (W/S) ก่อนคลิก NPC เสมอ** — วาปข้ามฉากล้าง `last_target_pos` เป็น `None`
     คลิกก่อนเดิน = เงียบ และนั่นคือความผิดของขั้นตอน ไม่ใช่ผลวัด
     🔴 **ขอบเขต: คลิกเพื่อเลือกเท่านั้น ห้ามตีมอน ห้ามใช้สกิล** (ใบตีมอนถูกกันไว้จนกว่า P-1/P-2 จะปิด)
  4. 🔴 **ฉาก 1 (Port Royal) ว่างตอนมาถึงโดยตั้งใจ — เดินหนึ่งก้าวก่อนตัดสิน**
     ที่มาของกฎ: `KA1A-AMENDMENT 20260901_1120` (ห้ามส่งสำมะโนก่อนผู้เล่นเดิน) ·
     ตัวเลข 0 ตอนมาถึง / 108 หลังเดินหนึ่งก้าว มาจาก `warp_chain_preflight` และ chief วัดซ้ำรอบ `xkmzxr`
     (**ไม่ได้อยู่ในใบ `1120`** — อย่าไปหาในนั้น) · กลไก: `runtime.py` เกตสำมะโนด้วย
     `last_target_pos is not None or scene_id != 1` ⇒ ฉาก 1 ตอนมาถึงยังไม่มีสำมะโน
     ⇒ ว่างทันทีที่วาปเข้า **ไม่ใช่ FAIL** · "เดินหนึ่งก้าวแล้วยังว่าง" = ผลลบที่มีค่า ให้จดแล้วเทียบกับชั้น wire
     ตามเกณฑ์สองชั้นข้างล่าง (ห้ามตัดสิน FAIL จากจอชั้นเดียว)
  5. 🔴 **ใบนี้วัดการ "เห็น" NPC เป็นหลัก** — คลิก NPC ได้ (หลังเดินหนึ่งก้าว) แต่ไม่ใช่เกณฑ์ผ่านของใบนี้
     🔴 ตอนบูต **ต้องไม่มี** บรรทัด `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED` แม้แต่บรรทัดเดียว —
     มีบรรทัดใด = **บิลด์ผิด หยุด ไม่ต้องวาป** ทั้งใบเป็น NO-RESULT (กฎเดียวกับ `GT-212` ข้อ 3)
     กฎการข้าม roster สิบฉากถูก **ถอนแล้ว** ใน `server#583` (merge 2026-09-02 09:29Z) ⇒ วันนี้ทุกฉากลงทะเบียนตอบคลิก
     (ร่างแรกของขั้นนี้ในรอบ `xkmzxr` เขียนตรงข้าม โดยลอกจากจดหมายที่เขียนก่อน `#583` — ถอนแล้ว)
  6. หมดแรง/หมดเวลากลางทางได้ — **เขียนว่าหยุดที่ฉากไหน** ผลบางส่วนของสายที่เรียงตามข้อ 3 ยังใช้ตัดสินได้
     🔴 **แต่ต้องรัน teardown ตาม `ATTENDED_SESSION_RUNBOOK.md` เสมอ แม้เลิกกลางคัน** พร้อม sha256 ของสำเนา DB
     หลังจบ และปล่อยล็อก — เลิกกลางคันโดยไม่ teardown = หลักฐานชั้น wire ของทั้งรอบหายถาวร
     ถ้ายังไหว: วาปกลับไป **ฉาก 2** (ฉากแรกของรายการ) อีกครั้ง แล้วยืนยันว่า NPC ยังอยู่
     (ทดสอบว่าการปลดแลตช์ไม่พังฉากที่กลับมาซ้ำ)
- pass criteria (two layers, kept separate):
    wire/DB: the server console/capture log for this boot shows, for EACH of the TWELVE
      marker-backed destinations in step 3, a fresh `world_census_sent = False` ->
      `WORLD_POP_HANDOFF`/`WORLD_CENSUS_BG*` assembled line pair for that destination scene
      (not just the first one) -- i.e. the wire-level count of census dispatches equals the
      number of distinct marker-backed scenes warped into this session, not one.
      🔴 **นับได้สูงสุด 12 จาก 13 และนั่นถูกแล้ว**: การวาปเข้าฉาก 1 ล้าง `last_target_pos` เป็น `None`
      และเกตสำมะโนคือ `last_target_pos is not None or scene_id != 1` ⇒ ฉาก 1 **ไม่ส่งอะไรตอนมาถึง**
      โดยตั้งใจ · มันจะส่งหลังผู้เล่นเดินหนึ่งก้าวตามขั้น 4 · เกณฑ์เดิมที่เขียนว่า "เท่ากับจำนวนฉากทั้งหมด"
      เป็นเลขที่ทำให้ผ่านไม่ได้ ถอนแล้วในรอบ `xkmzxr` (`COO-DECISION 20260902_0544` เองก็เขียนไว้ว่า 12/13)
      This is headless-provable from the console log alone and needs no human at the screen; it
      proves the server SENT the bytes, not that the client rendered anything from them.
    client-observable: what the human at the screen reports for each `MAP-<scene>` of the
      closed list in step 3 (scene 1 judged by step 4's rule, not by its arrival frame)
      -- did each destination map show a normal NPC population (not empty), matching
      what a fresh login into that same scene would show. Any ONE destination coming up
      empty while the wire/DB layer shows a census WAS sent for it is a valid, useful
      negative result (points at a client-side replace/render bug per RE-189 Job 1's own
      "the field every profile is trying to flip" territory, or at a stale
      `population_indices` mismatch this round's fix did not fully address) -- write up
      which specific map failed, do not describe the whole entry as a blanket FAIL.
- nonclaims:
  1. Does not test the SCENE-1 eager-census case (item 4 of `1035`, blocked by `1120`'s
     amendment as unsafe without either `lane_hooks.lane_a_choose_npc_scene1.production_allowed`
     or a deferred `population_indices` install) -- this entry only exercises the cross-scene
     GM-warp latch-clear path (`1035` items 1-3), which carries none of that hazard because a
     warp only ever fires after login is already complete.
     🔴 ฉาก 1 ที่เพิ่มเข้าท้ายรายการปิดในขั้น 3 (R306) **ไม่ขัดกับ nonclaim ข้อนี้**: ใบนี้ยัง**ไม่**เรียกร้อง
     ให้ฉาก 1 มีสำมะโนตอนมาถึง — ขั้น 4 ตัดสินมันหลังเดินหนึ่งก้าวเท่านั้น ซึ่งคือพฤติกรรมที่ `1120` กันไว้ตั้งใจ
  2. Does not re-test the FIRST warp of a session in detail -- that is `GT-182`, already PASS.
  3. Does not test whether the destination scenes' marker geometry is walkable/good (per the
     `authored`-not-`confirmed` caveat `GT-182` already carries) -- a bad landing spot is
     scene data, not a FAIL of the census-chain claim this entry tests.
  4. Does not claim this proves the census-latch fix is complete for every code path --
     `1035`'s own nonclaim that nobody measured whether `world_census_refused` (vs
     `world_census_sent`) had latched in the original bug capture is still open; this entry's
     PASS/FAIL is about client-observed NPC presence across warps, not about which of the two
     latch fields was responsible for the original symptom.
  5. Does not test relog/reconnect behavior -- this is a single, unbroken TCP session across
     all warps, per the entry's own objective.
- RECHECK: `cd pirate-force-server && git log --oneline -1 -- src/pirateforce_foundation/runtime.py | head -1`
  then confirm that commit is an ancestor of (or equal to) the boot commit used for this run,
  and `grep -n -B5 "world_census_sent = False" src/pirateforce_foundation/runtime.py` shows a
  hit inside `_gm_warp_resync_selected_scene` (at `main@81952ce` this is line 5459 -- do not
  trust that exact number on a later commit, the file grows; confirm by function name, not by
  line number) before trusting this entry's premise that the latch-clear fix is present on the
  commit being tested.
- links: `notes_to_chief/consumed/20260901_1035_KA1A-ROOTCAUSE-one-census-per-login-world_census_sent-is-a-connection-latch.md` ·
  `notes_to_chief/consumed/20260901_1120_KA1A-AMENDMENT-my-1035-fix-spec-item-4-is-unsafe-as-written-lane-A-already-measured-why.md` ·
  `notes_to_chief/20260901_1256_KA1A-TO-COO-census-latch-fix-landed-on-main-NOW-md-needs-updating-and-GM-A-is-testable-again.md` ·
  `notes_to_chief/20260901_1341_COO-DECISION-census-latch-verified-on-main-open-gt-entry-for-multimap-warp-plus-queue-summary-fix.md` ·
  `GT-182` (first-warp-of-session PASS, this entry's direct precondition) · `runtime.py:5459-5470`
  · `notes_to_chief/20260902_1526_LANE-GM-TO-CHIEF-gt192-header-debt-and-a-preflight-for-the-13-scene-chain.md`
  · `notes_to_chief/20260902_1604_LANE-GM-TO-CHIEF-gt192-server-args-line-would-disable-the-census.md`
- teardown: `ATTENDED_SESSION_RUNBOOK.md` — **ต้องรันเสมอ** แม้รอบจบเพราะเลิกกลางคันหรือเจ้าของเลิกเล่นเฉย ๆ
- result: (ผู้เทสกรอก: หยุดที่ฉากไหน · แมพที่ว่าง/น้อยผิดปกติ · ชั้น wire นับได้กี่สำมะโน · เวลา · ไฟล์สกรีนช็อต)

**ผู้เปิดใบ: chief รอบ `liq4ri` 2026-09-01 (cloud)** · แก้ครั้งล่าสุด: chief รอบ `xkmzxr`/R306 (จ่ายหนี้ `COO 0544`)

## GT-198 GROUND-DROP-MODEL-TYPE-FIELD-RENDER-CHECK-001  [❌ **CANCELLED - covered by GT-216** (🟢 PASS สองชั้น · `OBSERVER_CONFIRMED 2026-09-03T16:51+07:00`) **+ ผลรอบ attended R309** `notes_to_chief/20260904_1430_KA1A-R309-RESULTS-*` — ปิดโดย chief รอบ `oi2r2n`/R340 ตาม `COO-DECISION 20260904_1648` ข้อ 3 + `PANYA-DECISION 20260903_1934` ตามข้อเสนอ ka1-A ใน `1430`]

> **คำถามของใบนี้คำต่อคำ**: "ไคลเอนต์วาดโมเดล/เรขาคณิตที่ไม่ใช่ข้อความใต้ป้ายชื่อของที่ตกไหม สำหรับ item id ที่การฆ่าจริงสุ่มออกมา" — ตอบไปแล้ว **ทางบวก ทั้งสองชั้น** โดยที่ไม่มีใครบูตใบนี้:
> **ชั้น wire** — ทุกดรอปในรอบ R309 เป็น `frame_bytes=57` = `DROP_FRAME_SIZE_WITH_MODEL_TYPE` ⇒ ฟิลด์ `n_DROPMODEL_TYPE` (mask `0x04` · tag `0x0F` · u16 · `+0x18`) อยู่บนสายจริงทุกเฟรม ผ่านทางเดินโปรดักชัน ไม่มีแฟล็ก
> **ชั้นจอ** — เจ้าของยืนยันเองว่าเห็นโมเดลสามมิติ ในรอบ attended สามรอบ (R306 = `GT-216` PASS · R307 · R309) และมีภาพจากรอบล่าสุด (`140947.png` คริสตัล)
> 🔴 **สิ่งที่การปิดใบนี้ไม่ได้อ้าง**: ไม่มีใบไหนเคยเกรด "เห็นเรขาคณิต" เป็นเกณฑ์ของตัวเอง — หลักฐานชั้นจอมาจากคำยืนยันของเจ้าของในรอบ attended บวกภาพ ซึ่งเป็นชั้นเดียวกับที่ใบนี้จะวัด ไม่ใช่ชั้นที่ต่ำกว่า · และ **ไม่**อ้างว่า `n_DROPMODEL_TYPE` คือฟิลด์ที่ตัวเลือกโมเดลของไคลเอนต์อ่าน (สมมติฐานของ ka1-B ยังไม่ถูกพิสูจน์ · `GT-045` วัดแล้วว่าค่า `1` อย่างเดียวไม่พอ)
> 🔴 **เหตุผลข้อที่สองที่ปิด ไม่ใช่แค่ "ตอบแล้ว"**: ใบนี้เขียนขั้นตอนไว้บนมอนที่เจ้าของ**สั่งห้ามใช้ตั้งแต่ 27 ส.ค.** (Tornado Eagle) ⇒ บูตตามตัวอักษรของใบไม่ได้อีกต่อไป การคงไว้คือการถือใบที่รันไม่ได้และตอบแล้ว
> สถานะเดิม (ยกมาคำต่อคำ ไม่ได้ลบ): PENDING -- ready to boot on `origin/main`. ~~not yet merged to `main`; do not boot until RECHECK below shows the wide-mask code on `origin/main`~~ IS STRUCK: pirate-force-server PR #513 (branch `claude/zen-einstein-8efcx1`, commits `74cee95a`/`4d2b5105`/`d6e7a56a`, pf-adversary-reviewed x3) MERGED 2026-09-01T15:22Z; both RECHECK contents verified present on `origin/main` by LANE-B round `78zy6l` (2026-09-02T01:4x+07:00) -- see the RECHECK note below, its second command had a false-negative window and was corrected in the same round]

- objective: one claim only -- after wiring wire dirty-mask bit `0x04` (tag `0x0F`, u16, element offset `+0x18`, `n_DROPMODEL_TYPE`) into the ground-drop element (the wide `mask 0x16` element -- position + item-id + model-type -- now `mob_loot.py`'s own default for every real monster kill via `mob_loot.DROP_MODEL_TYPE_FIELD_ENABLED = True`, no CLI flag, reached by the real production dispatch chain `runtime.py:4921-4922` -> `mob_drop_presence.sustain_a_kill` -> `mob_loot.refresh_frames` -> `mob_loot.drop_frames_with_model_type`), does a real client render a non-text 3D model/geometry under the drop's floating name label, for whatever item id a real kill actually rolls? This is the client-observable test of ka1-B's letter (`notes_to_chief/consumed/20260901_2015_KA1B-TO-LANE-B-drop-model-selector-field-is-not-on-our-wire.md`, **[HYPOTHESIS, unproven]**): that this exact field is what the client's model selector reads. `GT-045` (CLOSED-ANSWERED) already measured `n_DROPMODEL_TYPE = 1` alone is NOT sufficient -- both of GT-045's client-confirmed ids (`2200423`/`2200003`) carried `1` and neither drew a model -- so a positive here is genuinely new evidence (this is the first time the field itself has ever been on the wire), not a re-confirmation.
- db: default `state\pirateforce.sqlite3` -- always a fresh copy for this boot only, never the canonical file:
  ```
  copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-198_<yyyyMMdd_HHmmss>.sqlite3
  copy state\pirateforce.sqlite3 state\run_gt198.sqlite3
  ```
  Record the run-copy's filename and sha256 before/after this round, and separately confirm the canonical file's own sha256 is byte-identical before and after (it is never opened for this test).
- server args: standard no-flag boot, on a `pirate-force-server` checkout that actually carries this round's three commits (branch `claude/zen-einstein-8efcx1` today; `origin/main` once merged -- confirm with RECHECK before booting either way):
  ```
  $env:PYTHONPATH = Join-Path (Get-Location) 'src'
  py -3 -u -m pirateforce_foundation.app --db state\run_gt198.sqlite3
  ```
  No `--*-scenario` flag of any kind -- the point of this ticket is that this is now the unflagged production path. Fresh server start only (age < 3.5 min); boot the client only after the server is up; never boot a client against a server left over from a previously killed client (the server keeps the session and the new client hangs on "connecting" forever).
- steps:
  1. Confirm RECHECK below passes. Boot server + client per the args above. Right-click-drag only (camera rotation, does not change facing, emits nothing) to a clean baseline view -- no `Q`/`E`, no `W`/`A`/`S`/`D` yet. Full-res photo BASELINE: (a) non-text item model/geometry visible on the ground y/n (expect none), (b) name-label visible y/n plus the colour of every name label in frame (one line per label, "none" if none).
  2. Walk to identity `0x201F` ("Tornado Eagle", bg0001, `(1747.5244, -7837.6978, 931.0413)`) -- the one field-mob `mob_death.kill()` authorises with no `widened=` argument, and the same real, no-flag combat path GT-035/GT-084/GT-084-R2 already proved reaches `mob_combat`/`mob_death` end to end. Double-click to select+attack (SCENE-006, `docs/COMMAND_HANDOFF.md`, cited at GT-084) until it dies -- 5 real `ActionVital` hits at -964 HP each is the established count (GT-035/GT-084).
  3. As soon as the kill's drop appears (after the dead frame + `DEATH_TASK_HOLD_MS`), name/track exactly ONE dropped item by icon/appearance and rough ground position, in writing -- if the kill emits more than one drop event, this project has previously observed a single kill emit two `MOB_LOOT_DROP` events (GT-084's own result line); pick one and track only that one. Immediately, full-res photo STEP-A: (a) non-text item model/geometry visible y/n -- distinct from any label text, dust, or shadow, and distinct from the killed mob's own corpse/body mesh (GT-084-R2, OBSERVER_CONFIRMED 2026-08-27T15:52-15:55+07:00, measured identity `0x201F`'s own corpse freezes in a floating pose after death rather than falling flat -- describe the tracked item's shape/position as distinct from that frozen corpse, not merely "something is there"; neither corpse nor dust/shadow ever counts as a model sighting), and (b) name-label visible y/n plus every label's colour.
  4. Record wall-clock time for every step, to cross-check against the server console/capture log afterward.
  5. Optional, non-blocking, not part of pass/fail: if a model is visible at STEP-A, the tester may click it and note whether a pickup opcode appears to fire. Colour only -- does not stand in for `GT-146`'s own claim and must not be written as gating it.
- pass criteria (two layers, kept separate):
    wire/DB: the server console/capture log for this boot shows the tracked kill's drop frame is **57 bytes** (`DROP_FRAME_SIZE_WITH_MODEL_TYPE`, element mask `0x16`), not **54 bytes** (`DROP_FRAME_SIZE`, mask `0x12`) -- headless-checkable from the capture log alone, and by itself proves only that the server sent the wide element, nothing about what the client drew. Also record the actual `n_DROPMODEL_TYPE` value the roll produced (0..12) from that same line -- do not assume it is `1` (GT-045's own two ids both were, and neither rendered).
    client-observable: what the human reports for STEP-A against BASELINE, per the two fields above. **POSITIVE** (a non-text model/geometry distinct from label/corpse/dust appears) is new evidence -- record it with the wire-layer's `n_DROPMODEL_TYPE` value; do not read it as confirming GT-045 (GT-045 measured the opposite). **NEGATIVE** (label + dust only, same as GT-045, regardless of the shipped value) is a finding worth exactly as much as a PASS -- it falsifies ka1-B's hypothesis for this field/offset and redirects to ka1-B's own un-eliminated alternative (letter section 3: nobody confirmed `TerrainThingPool*` at `+0x20` of `0x6E9D` is the same pool this lane's derived-bit-`0x08` list feeds). Neither outcome is a failure of this ticket to run.
- nonclaims:
  1. Does not verify the client's asset-decode/texture-upload path completes even if the selector byte is read -- Codex's own IMAGE-layer read of the reconciler names "concrete file open, callback state, reader selection, decode return, texture upload/bind, visible pixels" as its own still-open questions; this ticket only observes the end result and does not use or depend on any Codex IMAGE-layer finding beyond the token table already cited above.
  2. Does not test or claim anything about the two candidate offsets this round deliberately did NOT wire -- mask `0x08` (`+0x1B`) and `0x20` (`+0x1A`) -- already pinned by `mob_loot.py`'s own NONCLAIM 16 / `RE-067` as the client's text-label-COLOR property, P-2 territory reserved to the RE line.
  3. Does not test drop persistence or the heartbeat-preserve fix -- that is `GT-188`'s own separate claim; this ticket's pass/fail is decided entirely by the single photo taken immediately after the drop appears (STEP-A), the same timing GT-045 itself used.
  4. Does not accept the killed mob's own corpse/body mesh as evidence of the dropped item's model -- see step 3's citation of GT-084-R2's corpse-freeze measurement for `0x201F` specifically.
  5. Does not attribute a cause to any label's colour -- record colours only, per `RE-067`.
  6. Does not guarantee the kill produces any drop at all. The roll is probabilistic (`field_drop_tables` percentage rates; template 31 "Tornado Eagle" has real drop-table rows -- `2701001`, `2802234`, `5400001` -- but none is certain on any single roll). A zero-drop kill is NO-RESULT (wrong roll), not FAIL; `mob_death.py` limits `0x201F` to one kill per connection, so a retry needs a fresh DB copy and a full reboot (new RNG stream), not a relog.
  7. Does not test any mob other than `0x201F` Tornado Eagle in bg0001. A result here does not generalize to Bg0002 or any other scene/roster without its own entry.
  8. Does not claim the PR named in this ticket's header is merged -- see RECHECK; this ticket stays `BLOCKED`/`PENDING` until it passes.
- RECHECK: content-based, not commit-hash-based, per the lesson GT-045 itself learned (never compare a resolved commit to a number by eye -- judge by content):
  ```
  cd pirate-force-server && git fetch origin && \
  git show origin/main:src/pirateforce_foundation/mob_loot.py | grep -n "DROP_MODEL_TYPE_FIELD_ENABLED = True" && \
  git show origin/main:src/pirateforce_foundation/mob_loot.py | sed -n '/^def refresh_frames/,/^def /p' | grep -n "return drop_frames_with_model_type"
  ```
  RECHECK RUN 2026-09-02T01:4x+07:00 (LANE-B round `78zy6l`): command 1 hits (`mob_loot.py:604`); command 2 as first written (`grep -n -A3 "def refresh_frames"`) returned EMPTY on merged code, because `refresh_frames`'s docstring is ~55 lines long and a 3-line window never reaches the body -- a FALSE NEGATIVE that would have kept this ticket unbootable forever. The command above is the corrected one and hits (`return drop_frames_with_model_type(legacy, ledger.drops)`, body of `refresh_frames`, `origin/main`). Nothing about the ticket's claim changed; only the way it is verified.

  Both greps must hit on `origin/main` before booting; empty/failing output means the PR has not merged -- stays `BLOCKED`/`PENDING`, do not boot, report back instead. (If testing the pre-merge branch directly, swap `origin/main` for `origin/claude/zen-einstein-8efcx1` in both commands and note which was used in the result.)
- links: `pirate-force-server#513` (branch `claude/zen-einstein-8efcx1`, commits `74cee95a`/`4d2b5105`/`d6e7a56a`, pf-adversary x3, one HIGH finding fixed in commit 3) -- `notes_to_chief/consumed/20260901_2015_KA1B-TO-LANE-B-drop-model-selector-field-is-not-on-our-wire.md` (the hypothesis this ticket tests) -- `mob_loot.py` NONCLAIM 16 / `RE-067` (`CLIENT_RE_QUEUE.md`, withheld offsets) -- GT-045 closing letters (`archive/notes_to_chief_2026-08-19_to_26/20260825_1340_GT045-ANSWERED-*.md`, `.../20260825_1615_GT045-EVIDENCE-COMMITTED-*.md`) -- `GT-084`/`GT-084-R2` (real no-flag combat path on `0x201F`, corpse-freeze measurement) -- `GT-188` (heartbeat-preserve, separate claim, do not conflate) -- `rounds/B_20260901_2036_8efcx1_*.md` (this round's own account, same branch).
- numbering: per the shared-counter search command (rule ② at the top of this file), re-run at rebase time against `origin/main`: highest `GT` on `main` is now `GT-194` (LANE-A, opened same day, merged ahead of this branch during a rebase conflict); highest `RE` in `CLIENT_RE_QUEUE.md` is `RE-197`. This entry is `198`.
- result: (tester fills in: PASS/FAIL/BLOCKED/NO-RESULT, evidence, timestamp, `OBSERVER_CONFIRMED` line per G-OBS once client-observable evidence exists)

## GT-204 MOB-DROP-LEFT-CLICK-PICKUP-INTO-BACKPACK-001  [❌ **CANCELLED - covered by GT-216** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2) — `GT-216` PASS บนจอเจ้าของ R306 16:51 (คลิก 10 ครั้ง เข้ากระเป๋า 9 · 8 ใน 9 ติดคลิกแรก · กระเป๋า 3→12 ตรงกับ DB) และ `GT-220` ยืนยันซ้ำอีกครั้งใน R307 ⇒ คำถามของใบนี้ ("คลิกซ้ายของที่มอนดรอปแล้วเข้ากระเป๋าไหม") ถูกตอบบนจอไปแล้วสองรอบ · 🔴 **สิ่งที่ยัง "ไม่" ถูกตอบและห้ามผูกกับใบนี้อีก** (`COO-DECISION 20260903_1942` ข้อ 4): เกณฑ์ "ป้ายชื่อของไม่กะพริบตอนตีตัวถัดไป" (`RE-208`) — LANE-B เขียนเป็นหนึ่งขั้นใน **`GT-223`** ซึ่งเป็นใบของบนพื้นที่ chief ยังเปิดอยู่ · สถานะเดิม: READY -- run RECHECK first; line 2 is still the real gate]

### 🔴 โทเคนที่ห้ามอ่านว่าเสีย (`COO-DECISION 20260903_0953` ข้อ 2 -- เขียนลงทุกใบที่มีคลิกเก็บของ)
  **`cell_has_no_scene` ก่อนการฆ่ามอนตัวแรก *ของเซสชันล็อกอินนั้น* = พฤติกรรมที่ถูก ไม่ใช่ความเสีย ห้ามรายงาน FAIL**
  เซสชันที่เพิ่งล็อกอินถือ ground cell ที่ยัง `current_scene is None` (LANE-B วัดเองรอบ `gewbnj`) และซอร์สเขียนไว้ตรง ๆ ว่าตั้งใจ:
  `mob_pickup.py:1454-1460` -- "the cell does not know its scene -> `cell_has_no_scene` ... reachable mainly before the first kill of a boot -- where refusing is right" (chief re-derive เองรอบ R317 ไม่ได้เชื่อจดหมายแหล่งเดียว)
  🔴 **หน่วยคือ "เซสชัน" ไม่ใช่ "บูตของเซิร์ฟเวอร์"** — chief วัดเองรอบ R317: `DropLedgerCell()` ถูกสร้างใหม่ต่อหนึ่งเซสชัน (`runtime.py:1328`)
  และ `_scene` ถูกตั้งได้แค่สามทาง: ctor (`mob_loot.py:2772`) · การฆ่า (`:3005`) · `enter_scene` ที่ขอบฉาก (`:3261`)
  ⇒ **รีล็อกอินระหว่างบูตเดียวกัน = cell ใหม่ = ตัวนับเริ่มใหม่** เห็นโทเคนนี้อีกครั้งหลังรีล็อกอินก่อนฆ่าอะไร **ยังเป็นปกติ**
  ⇒ **เห็นบนพื้นว่างก่อนฆ่าอะไรในเซสชันนั้น = ปกติ เดินต่อได้** · เห็น**หลัง**ฆ่ามอนในเซสชัน*เดียวกัน*แล้วและของตกจริงแล้ว = **finding** หยุดและรายงาน
  🔴 **รีล็อกอินกลางใบ = ตัวนับรีเซ็ต** ⇒ ถ้าต้องรีล็อกอิน ให้ **ฆ่ามอนหนึ่งตัวก่อน** แล้วค่อยตัดสินโทเคนนี้ อย่าตัดสินจากการฆ่าครั้งก่อนรีล็อกอิน
  🔴 **คัด *ข้อความ* ไม่ใช่แค่โทเคน** — ชื่อเดียวกันถูกใช้สองความหมาย (`mob_pickup.py:1477-1483` แปลง `MobLootContractError` ทุกตัวเป็นชื่อนี้):
  ข้อความ `does not know which scene it is in` = **กรณีปกติข้างบน** · ข้อความ `could not answer which scene it is in (<เหตุผลข้างใน>)` = **finding เสมอ** ไม่ว่าจะฆ่าอะไรมาแล้วหรือยัง
  (ทางที่สองยังไม่เคยถูกรัน — ซอร์สติด `# pragma: no cover` ⇒ เจอเมื่อไหร่คือของใหม่ ต้องรายงาน)

> 🔴 **NUMBERING — เลขใบนี้ถูกขยับจาก `203` เป็น `204` กลางรอบ และต้องเขียนไว้:**
> ตอน chief จองครั้งแรก (2026-09-02T07:1x+07:00) `GT-203`/`RE-203` = **0 hit** จริงทั้งสองคิว
> แต่ระหว่างรอบเดียวกันนี้ LANE-A merge `GT-203 AVATARATTR-NAMED-FIELDS-MATCH-THE-CREATION-SCREEN-001`
> ขึ้น `main` ก่อน ⇒ chief **ขยับใบตัวเองไปเลขถัดไป ไม่ทับของใคร** (เลขชนกัน ห้ามทับ ให้ +1 แล้วบันทึกเหตุ)
> ตรวจซ้ำบน main ล่าสุด (`53018b00`): `GT-204`/`RE-204` = **0 hit** ทุกที่ที่กติกาสั่งให้ดู --
> `GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `notes_to_chief/` · `rounds/` · `archive/`
> ⇒ ใบนี้ = **204** · ใบ `GT-001`-`GT-203` และ `RE-085`-`RE-202` อยู่ที่เดิมทั้งใบ ไม่ลบ ไม่ย้าย

> ✅ **ประตูที่หนึ่ง เปิดแล้ว:** `pirate-force-server PR #549` (chief, R300) **อยู่บน `main`** --
> call site `3e8541e` · การถอน fallback ตำแหน่ง `815ebce` · ปลดสถานะเป็น `READY` ตาม
> `COO-DECISION 20260902_0945` ข้อ 1 และ 3
> 🔴 **ประตูที่สอง ยังไม่เปิด และมันคือประตูจริง:** ของต้องค้างบนพื้นนานพอให้ตาคนเห็นและเล็งคลิกได้
> ⇒ **`GT-188` checkpoint 2 ต้องได้ผลก่อน** · ฝั่ง ledger เซิร์ฟเวอร์รอด 120 วิ แล้วจริง
> (`mob_drop_presence.sustain_a_kill` บน `main`) แต่ **การวาดป้าย/โมเดลซ้ำบนจอยังไม่มีใครวัด**
> ทาง `preserve_ground_in_runtime_res_vitals` แบบครอบ **ถูกถอนแล้ว** โดย `COO-DECISION 20260902_0646`
> (วัดได้ว่าฆ่าเธรด `game_listener` 3 ทาง) · ตัวแทนแบบ opt-in ทีละจุด: `announce_frames` **ขึ้น main แล้ว**
> (`#554`/`#557`) แต่ `action_ack` **ขึ้นแล้วก็ยังไม่พอ** ⇒ **ห้ามอ้างว่า PRESERVE ครบแล้ว — มันยังไม่ครบ**
>
> 🔴 **แก้คำของ chief เอง 2026-09-02T11:3x+07:00 (R302 `ogq686`) — ร่างแรกของบล็อกนี้ทำนายผลไว้ล่วงหน้า
> และคำทำนายนั้นไม่มีหลักฐานรองรับ ถอนแล้วทั้งย่อหน้า**
> ร่างแรกเขียนว่า "ของถูกล้างภายใน 0.0 วินาที ⇒ ผลที่คาดคือ P5 NO-RESULT" โดยยกตารางของสาย B
> (`20260902_1030`) มาเป็น `วัดแล้ว` · pf-adversary หักล้างสองชั้น และถูกทั้งสองชั้น:
> **(ก) ตารางนั้นรวมสองเบิร์สต์ที่ไม่เคยเกิดพร้อมกัน** — `MOB_COMBAT_BAR` มีเฉพาะตอน **ตีไม่ตาย**
> ส่วน `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` มีเฉพาะตอน **ฆ่า** · ใบนี้เป็นใบ "ฆ่าหนึ่งตัว คลิกหนึ่งครั้ง"
> ⇒ เบิร์สต์ของใบนี้ **ไม่มี `MOB_COMBAT_BAR` อยู่เลย**
> **(ข) เฟรมสุดท้ายของเบิร์สต์การฆ่าคือ `MOB_LOOT_DROP` ไม่ใช่ `MOB_DEATH_DEAD`** —
> `runtime.py:4963-5036` ต่อ `mob_drop_presence.loot_actions` ไว้ **หลัง** ตารางเวลาการตายทั้งชุด
> และมันพก ledger ทั้งฉาก (`whole_live_ledger_per_kill`) ⇒ ภายใต้ `RE-130` (generation ที่ไม่ว่าง
> **ใบสุดท้าย** คือใบที่อยู่) ของอาจอยู่รอดบนจอ และ **ไม่มีใครวัดว่ามันอยู่หรือไม่อยู่**
> สาย B เองปิดใบ `1030` ด้วยคำถามข้อนี้ตรง ๆ ว่ายังไม่มีคำตอบ และ `COO-DECISION 1044` ข้อ 5
> สั่งให้สาย B ตอบเป็นงานแรกก่อนเขียนโค้ด
>
> ⇒ **ใบนี้จึงไม่ทำนายอะไรทั้งสิ้น** เจอของบนพื้น = เดินไปคลิกตามขั้น · ไม่เจอ = กรอก **P5 NO-RESULT**
> (ไม่ใช่ FAIL) ตามคำทำนาย P5 ที่มีอยู่แล้ว · **ทั้งสองทางคือผลการวัดที่ใบนี้ต้องการ**
> 🔴 **ห้ามเอาผลชั้น wire/DB ไปตอบชั้น client-observable** (G5)

- objective: (ข้ออ้างเดียว) ผู้เล่นฆ่ามอน -> ของตกลงพื้น -> เดินเข้าไปแล้ว **คลิกซ้ายที่ของชิ้นนั้นหนึ่งครั้ง** --
  เส้นทาง production ใหม่ใน `runtime.py` ที่เรียก `mob_pickup_request.dispatch_inbound_pickup_request(...)`
  โดยคีย์ที่ **NESTED vital id** `mob_pickup_request.PICKUP_REQUEST_VITAL_ID` (= `0x4543`)
  **หยิบของออกจากพื้นเข้ากระเป๋าได้จริงหรือไม่**
- db: `default_state\pirateforce.sqlite3` -- **สำเนาเท่านั้น ห้ามเปิด canonical** · คัดไป
  `backup\pirateforce_before_GT-204_<yyyyMMdd_HHmmss>.sqlite3` แล้ว `state\run_gt204.sqlite3` ·
  จด sha256 ของสำเนาก่อน/หลัง · เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` **ก่อนและหลัง ต้องเท่ากัน** ·
  `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง
- server args: บูตปกติตาม playbook บน `main` **ไม่มีแฟล็ก `--*-scenario` ใด ๆ** (สาขานี้เป็น production ไม่มี flag):
  `py -3 -u -m pirateforce_foundation.app --db state\run_gt204.sqlite3`
  🔴 **ตัวละครบูตต้อง "สมประกอบ" ตาม `PANYA-DECISION 20260828_0125`** ก่อนเริ่มจับเวลา: level 1 · class 1 ·
  stats จาก `CHARCREATE_CLASS s_SCORE` · HP/MP จาก `STANDARD_STATUS` · speed `ActorAttr` x7 = 400 ·
  **ชื่อตัวละครอยู่ใน `BasicAttr` x1 (`+0x28`) และห้ามอยู่ใน x37** · x39/x41/x42 = **0** ทั้งสามช่อง
- steps: (playbook: `ATTENDED_SESSION_RUNBOOK.md` · อัดวิดีโอต่อเนื่องตลอดหน้าต่าง `LOCK_GAME`)
    0. LOCK_GAME · boot stamp · sha canonical · copy DB · รัน RECHECK ข้างล่างให้ผ่านทั้งสองบรรทัดก่อน ไม่ผ่าน = ไม่บูต
    1. **server ก่อน client เสมอ** · เข้าเกม ยืนยันบล็อก "สมประกอบ" จากคอนโซล/HUD แล้วจด scene + X/Y/Z
    2. จัดมุมกล้องด้วย **คลิกขวาค้างลาก** เท่านั้น · ยังห้าม `Q`/`E` และ `W/A/S/D` จนกว่าจะถึงขั้นที่สั่งให้เดิน
       (ทั้งสองชุดเปลี่ยน facing และยิง `TargetPosVital`) · **ห้ามพิมพ์ตัวอักษรตลอดรอบ**
    2b. 🔴 **ขั้นใหม่ ก่อนขั้นเก็บของ -- ตีมอนหนึ่งครั้ง แล้วดูสองอย่าง** (`COO-DECISION 20260902_1248` ข้อ 2 ·
       ถ้อยคำจากใบ LANE-B `20260902_1144` ข้อ 4) · เลือกมอนที่จะฆ่าในขั้นที่ 3 นั่นแหละ **ตีหนึ่งครั้ง
       ให้ยังไม่ตาย** แล้วบันทึกทันที ห้ามตีซ้ำก่อนจด:
       (ก) **มอนยังยืนอยู่บนจอ และหลอดเลือดของมันขยับ** => ไคลเอนต์รับ mask `0x0A` ของเฟรม bar
           ⇒ เดินขั้นที่ 3 ต่อได้ตามปกติ · ถ่าย **S0a** ตอนหลอดขยับ (full-res เห็นตัวมอนกับหลอด)
       (ข) **มอนหายไปจากจอ** หรือคอนโซลเซิร์ฟเวอร์ขึ้น `GROUND_ACTORS_PRESERVE_REFUSED` (ASCII ตรงตัว)
           => ตัว fall back ทำงาน ⇒ 🔴 **หยุดใบนี้เดี๋ยวนั้น ไม่ต้องเดินขั้นเก็บของ** คัดบรรทัดคอนโซลดิบ
           ทั้งบล็อก + `S0a` แล้วรายงานว่าใบหยุดที่ขั้น 2b เพราะข้อ (ข)
       เหตุผลที่ขั้นนี้อยู่ตรงนี้: ผลของมันคือกุญแจของรั้ว census ทั้งใบ (`COO 1044` ข้อ 4) และเป็นครั้งแรก
       ที่ P-1 จะถูกมองเห็นบนจอ · **ขั้นนี้ไม่ใช่ใบตีมอนใบใหม่** (`NOW.md` ยังห้ามเปิดใบตีมอน) มันคือหนึ่งขั้น
       ในใบนี้ที่บูตอยู่แล้ว
    3. ฆ่ามอน **หนึ่งตัวที่ดรอปของ** · ทันทีที่ของโผล่ ถ่าย full-res **S0** · เลือก **ของหนึ่งชิ้น** แล้วเขียนชื่อ/รูปร่าง/
       ตำแหน่งของชิ้นนั้นลง result เดี๋ยวนั้น แล้วตามชิ้นเดิมตลอดใบ · ซากมอน (corpse) **ไม่นับ** เป็นตัวของ
    4. เดินเข้าไปหาของด้วย `W/A/S/D` จนอยู่ติดชิ้นที่ตามอยู่ · ถ่าย **S1** · **จดสภาพกระเป๋าก่อนคลิก**:
       เปิดกระเป๋า นับช่องที่มีของ ถ่าย **S2** แล้วปิด
    4b. 🔴 **ต้องเดินมาถึงของด้วยเท้าจริง ๆ ห้ามคลิกจากตำแหน่งที่ไม่เคยขยับ** --
       `COO-DECISION 20260902_0945` ข้อ 1 · **เหตุผล วัดแล้วจากคอมมิตเอง:**
       `815ebce` ("withdraw the position fallback") ถอนการถอยไปใช้ `selected.position` ออกโดยเจตนา
       ⇒ เซิร์ฟเวอร์ตัดสินระยะ 450 หน่วยจาก `last_target_pos` เท่านั้น ซึ่งไคลเอนต์รายงานเมื่อผู้เล่นเดิน
       ⇒ ถ้าตัวละคร **ไม่เคยขยับเลยตั้งแต่ล็อกอิน** `last_target_pos` เป็น `None` และคลิกถูกปฏิเสธ
       **โดยระบุชื่อ `reason=position_not_finite`** (เซิร์ฟเวอร์ไม่ได้ "เชื่อว่าอยู่จุดเกิด" -- มันไม่เชื่ออะไรเลย
       ดู nonclaim 7 และคำทำนาย P2 ของใบนี้ ซึ่งเขียนถูกอยู่แล้ว) · 🔴 **นั่นคือ fail-closed ที่ถูกต้อง ไม่ใช่บั๊ก**
       🔴 **แก้คำของ chief เอง 11:3x+07:00 (pf-adversary N2):** ร่างแรกของขั้นนี้สั่งให้ "เดินเพิ่มอีกหนึ่งก้าว
       ก่อนคลิก" ซึ่ง **ถอนแล้ว** สองเหตุผล (ก) ขั้นที่ 4 สั่งให้เดินด้วย `W/A/S/D` มาถึงของอยู่แล้ว
       การเดินนั่นเองคือสิ่งที่ตั้ง `last_target_pos` ⇒ เงื่อนไข "ยืนนิ่งมาตลอด" เกิดไม่ได้ถ้าทำตามขั้นที่ 4
       (ข) ก้าวเกินมาอีกหนึ่งก้าวเสี่ยงยืนทับของ ⇒ คลิกไปโดนตัวละคร/พื้น ไม่ออกเฟรม pickup
       ⇒ ได้ผล (c)/**P4 ปลอม** ที่ขั้นตอนสร้างขึ้นเอง แล้วส่งงานผิดไปที่ใบ static
       ⇒ **ทำตามขั้นที่ 4 พอ** ข้อนี้เหลือไว้เป็นคำเตือนว่าอย่าลัดขั้นที่ 4 ด้วยการวาป/ยืนเฉย ๆ แล้วคลิก
    5. **คลิกซ้ายที่ของชิ้นนั้นหนึ่งครั้ง** · จดเวลานาฬิกา (+07:00) และ `t` ในวิดีโอ · ถ่าย **S3** ทันที ·
       คัดคอนโซลเซิร์ฟเวอร์ **ดิบ ห้ามตีความ** ตั้งแต่วินาทีที่คลิกไปอีก 3 วินาที
    6. เปิดกระเป๋าอีกครั้ง ถ่าย **S4** (ช่องเดิม + ช่องที่เพิ่ม) · **ห้ามลากของในกระเป๋า** (ยิง item-move คนละเลน)
    7. NO-CRASH ด้วย **คลิกขวาค้างลาก** (🔴 ห้ามใช้ `Q`/`E` เป็นตัวเช็ค) · **S5** · ออกเกมด้วย X มุมขวาบน
    8. ปิดเซิร์ฟเวอร์ (**ฆ่าไคลเอนต์แล้วต้อง restart เซิร์ฟเวอร์ก่อนบูตหน้าเสมอ**) · เก็บ console `.out`/`.err`
       + `capture_v141\GAME_LIVE.txt` + `capture_v141\GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ ·
       `PRAGMA integrity_check` · **teardown เสมอ** · sha canonical ซ้ำ · ห้าม commit เอง
    9. คัดผลจากคอนโซล/แคปเจอร์ (ดิบ): `findstr /N /C:"MOB_PICKUP_REQUEST_DECODED" /C:"MOB_PICKUP_REQUEST_REFUSED"
       /C:"MOB_PICKUP_ROW_INSERTED" server_console_live.*.txt` · `findstr /N /C:"UNKNOWN_0x"
       capture_v141\GAME_EVENTS_LIVE.txt` · `findstr /N /C:"[G< #" server_console_live.*.out`

- 🔴 **สามผลลัพธ์ที่เป็นไปได้ และวิธีแยกจากคอนโซลอย่างเดียว** (`0x4543` เป็นเลข **DERIVED** จากการอ่านอิมเมจแบบ
  static และ **ไม่เคยถูกเห็นบนไวร์ใด ๆ เลย** -- `RE-125` CLOSED BOUNDED-NEGATIVE):
    (a) คอนโซลมี `MOB_PICKUP_REQUEST_DECODED ...` => **เลขถูก และสาขายิงแล้ว**
        (ดูต่อว่าตามด้วย `MOB_PICKUP_ROW_INSERTED ...` หรือ `MOB_PICKUP_REQUEST_REFUSED reason=<ชื่อ>`)
    (b) **ไม่มี** สองโทเคนนั้น แต่มีบรรทัด vital ที่ไม่รู้จักของ **id อื่น** ในหน้าต่าง +-2 วิรอบคลิก --
        `[G< #<n>] <len> bytes IDs=[...]` และ/หรือ `EVENT seq=... name=UNKNOWN_0x<ID>` ใน
        `GAME_EVENTS_LIVE.txt` => **เลข `0x4543` ผิด แต่รอบนี้จับ opcode จริงมาได้** ซึ่งคือสิ่งที่ `GT-146`
        ต้องการพอดี · **คัด id + บรรทัดเต็ม + hexdump ห้าม decode เอง**
    (c) คอนโซล **เงียบสนิท** ตอนคลิก => **ไคลเอนต์ไม่ส่งเฟรม pickup** · เป็นผลที่วัดแล้ว ไม่ใช่รอบเสีย
  🔴 ต้องเทียบกับ **baseline ก่อนคลิก** เสมอ ไม่งั้นแยก (b) กับ (c) ไม่ออก

- pass criteria: (สองชั้น 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**)
    wire/DB          : (1) `character_backpack_items` ในสำเนา DB มี **แถวใหม่หนึ่งแถวของตัวละครที่เลือกไว้**
      (จำนวนแถวก่อน/หลังต่างกัน 1 · จด `item_identity`/`template_id`/`quantity`/`slot` ทุกค่า) **และ**
      (2) คอนโซลมีบรรทัด `MOB_PICKUP_REQUEST_DECODED` ของคลิกครั้งนั้น · ประกอบ: `MOB_PICKUP_ROW_INSERTED
      table=character_backpack_items ...` ที่ค่าตรงกับแถวจริง · `integrity_check` = `ok` ·
      sha256 canonical ตรง `CANON_SHA.txt` ก่อน/หลัง · ไม่มี traceback ที่ไม่ถูกจับ
      ชั้นนี้ตอบไม่ได้: บนจอเห็นอะไร ป้ายหายจริงไหม กระเป๋าวาดของขึ้นไหม
    client-observable: **ต้องมีคนอยู่หน้าจอเท่านั้น ห้ามอนุมานจากคอนโซล** -- (1) **ป้ายชื่อลอยของชิ้นที่ตามอยู่
      หายไปจากพื้น** เทียบ `S1` กับ `S3` **และ** (2) **ช่องกระเป๋าได้ของเพิ่มขึ้นจริงบนจอ** เทียบ `S2` กับ `S4` ·
      มีข้อความระบบขึ้นไหม (คัดเป๊ะ + สี) · NO-CRASH/CRASH ·
      🔴 **จดสีป้ายชื่อทุกป้ายทุกภาพ หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** อ่านจาก **full-res เท่านั้น** ·
      ไม่มีป้ายให้เขียนคำว่า `none` ห้ามเว้นว่าง · **จดสีอย่างเดียว ห้ามเดาสาเหตุของสี** (`RE-067` เป็นเจ้าของ)
      ชั้นนี้ตอบไม่ได้: มีแถวลง DB จริงไหม เฟรมที่ยิงคือ id อะไร

- คำทำนาย (**เป็นคำทำนาย** · ทำนายผิด = ผลการวัด ไม่ใช่ความล้มเหลว):
    P1 (a) + แถวใหม่ + ป้ายหาย + ช่องกระเป๋าเพิ่ม => ผ่านทั้งสองชั้น
    P2 (a) แล้วตามด้วย `MOB_PICKUP_REQUEST_REFUSED reason=<ชื่อจากทะเบียน>` => สาขายิงแล้วและถูกกั้นถูกจุด
       **แต่ไม่มีแถวใหม่** => wire/DB = FAIL ของข้ออ้างนี้ แต่ชี้ไปที่ชื่อ reason นั้นตรง ๆ
       🔴 `reason=position_not_finite` โดยเฉพาะ = ตำแหน่งผู้เล่นอ่านไม่ได้ทั้งสองทาง (ดู nonclaim 7)
    P3 (b) => `0x4543` ผิด · **ผลลบนี้มีค่าเท่าผลบวก** redirect ไป `GT-146`/`RE-125` ไม่ใช่ rerun ใบนี้แบบเดา
    P4 (c) => ไคลเอนต์ไม่ส่งเฟรม · redirect ไปใบ static ว่าใคร populate ลิสต์ของ `DropThingModule_Client`
    P5 ของหายจากพื้นก่อนคลิกทัน / ไม่มีของให้คลิก => **NO-RESULT (ประตู `GT-188` ยังไม่เปิดจริง)** ไม่ใช่ FAIL

- nonclaims:
  1. ไม่พิสูจน์ว่าของ **รอดข้าม relog** -- นั่นคือ `GT-142` ทั้งใบ
  2. ไม่พิสูจน์ว่า `0x4543` เป็น opcode จริงของไคลเอนต์ ถ้าผลออกมาเป็น (b) หรือ (c) · และผล (a) พิสูจน์แค่ว่า
     **เฟรมที่ไคลเอนต์ส่งตรงกับเลขนี้ในรอบนี้** ไม่ได้ทำให้ `RE-125` เปลี่ยนสถานะโดยอัตโนมัติ
  3. ไม่พิสูจน์อายุของ/ป้ายบนพื้น และไม่พิสูจน์ว่า PRESERVE ทำงาน -- `GT-188` เป็นเจ้าของคำถามนั้น
  4. ไม่ตัดสินสาเหตุของสีป้ายใด ๆ (`RE-067`) · จดสีอย่างเดียว
  5. ไม่ใช่เทส stack / กระเป๋าเต็ม / สองผู้เล่นแย่งของ / race -- หนึ่งบัญชี หนึ่งเซสชัน หนึ่งการฆ่า หนึ่งคลิก
  6. ไม่พิสูจน์อะไรเกี่ยวกับหุ่นซ้อมใน Port Royal -- `n_ID 916` มี `n_DROPS_*` = 0 ทั้งสามคอลัมน์ => ฆ่าที่นั่น
     ได้ **NO-RESULT (ฉากผิด)** ไม่ใช่ FAIL
  7. 🔴 ระยะ pickup ของเซิร์ฟเวอร์คือ **450 หน่วย 3 มิติ** จากตำแหน่งที่เซิร์ฟเวอร์ "เชื่อว่า" ผู้เล่นอยู่ ซึ่งเป็น
     ตำแหน่งที่ **ไคลเอนต์รายงานมาเอง** (ไม่ใช่ server-authoritative) · ใบนี้ไม่พิสูจน์ว่าไคลเอนต์โกหกตำแหน่งไม่ได้

- 🔴 **ห้ามบูตเพื่อใบนี้ใบเดียว** (`COO-DECISION 20260902_1146` ข้อ 2): ถ้า RECHECK ข้อ 3 ไม่ผ่าน (0 hit)
  ให้วัดชั้น wire/DB ของใบนี้ **เฉพาะเมื่อเครื่องบูตอยู่แล้วเพื่อใบอื่นในรอบเดียวกัน** เท่านั้น
  ลำดับบูตของรอบนี้: `GT-207` -> `GT-193` -> `GT-205` -> **`GT-204` ท้ายสุด**
  เหตุผล: รอบ attended ของเจ้าของแพงกว่าผลที่ใบนี้จะได้ ถ้าประตูยังไม่เปิด

- RECHECK: (รันก่อนเชื่อหัวใบเสมอ · ต้องผ่าน **ทั้งสองบรรทัด** ไม่งั้นยัง BLOCKED ห้ามบูต)
  1. `cd pirate-force-server && git grep -n "dispatch_inbound_pickup_request(" origin/main -- src/pirateforce_foundation/runtime.py`
     -- ต้องได้ **>= 1 hit** (0 hit = `PR #549` ยังไม่ merge) · และต้องเห็นคอมเมนต์ที่มีคำว่า
     "now observed on the wire (R303" ภายในสิบบรรทัดจาก call site (เงื่อนไขของ `COO-DECISION 20260902_0541`)
     🔴 **แก้สตริงโดย chief รอบ `rz1fxh`/R358**: ถ้อยคำเดิม `"never been observed on any wire"` ถูกพลิกทั้งซอร์สและเทสตาม
     `COO-DECISION 20260905_0249` ข้อ 2 (R303 = 46 เฟรมขาเข้า 2 เทคจบ) ⇒ grep เดิมคืน 0 hit ตลอดกาล และ RECHECK นี้จะไม่มีวันผ่าน
     (กฎ "PR ที่ลบสตริงที่ใบเทส grep อยู่ ต้องแก้ในรอบเดียวกัน") · ใบนี้ CANCELLED covered by `GT-216` อยู่แล้ว ไม่มีใครบูตค้าง
  4. 🔴 **บรรทัดถอนของ ลงแล้วรอ merge (chief R304 · `pirate-force-server#581`)** -- ก่อนบูตใบนี้ให้ตรวจว่า
     merge แล้วจริง: `cd pirate-force-server && git fetch origin && git grep -n "MOB_PICKUP_GROUND_AFTER" origin/main -- src/pirateforce_foundation/runtime.py`
     ต้องได้ **>= 1 hit** · 0 hit = ยังไม่ merge ⇒ ชั้น client-observable ข้อ (1) (ป้ายหายจากพื้น) **วัดไม่ได้**
     ให้บันทึกเป็น NO-RESULT ของข้อนั้น ไม่ใช่ FAIL
     🔴 **และซองของ delta เปลี่ยนไปจริงในคอมมิตเดียวกัน** (วัดแล้ว 74 ไบต์ แทน 71 ไบต์เดิม):
     ตั้งแต่ merge ทุกการเก็บของที่ยังมีของเหลือบนพื้นจะตอบด้วย delta ตัว **PRESERVE ของสาย B**
     แทน mask เปล่าของ v141 · **ยังไม่มีจอไหนยืนยันว่าไคลเอนต์รับ tail นี้** ⇒ ถ้าผลออกมาว่า
     "คลิกแล้วไม่มีอะไรเกิดขึ้น / ของไม่เข้ากระเป๋า" ให้สงสัย **ซอง** ก่อนสงสัยสาขา
     และคัดบรรทัด `MOB_PICKUP_DELTA_GROUND_KEPT` / `MOB_PICKUP_GROUND_REMOVAL_PUBLISHED` มาด้วยทุกครั้ง
     (สองบรรทัดนี้แยก "ส่งไปแล้ว" ออกจาก "ประกอบแล้วทิ้ง" ได้ที่เดียว)
  5. 🔴 **เก็บ "ชิ้นสุดท้ายของฉาก" ได้แล้ว รอ merge (chief R307 · ใบ `COO 1746` / `LANE-B 1650`)** --
     ก่อนใช้ชิ้นสุดท้ายเป็นขั้นตัดสิน ให้ตรวจว่าลง main จริง:
     `cd pirate-force-server && git fetch origin && git grep -nE "MOB_LOOT_BOUNDARY_STASH_CLEARED|boundary_stash_cleared_console_line" origin/main -- src/pirateforce_foundation/runtime.py`
     🔴 **คำสั่งนี้ถูกแก้รอบ `xcmfr6` (chief R321) และเหตุผลสำคัญกว่าตัวคำสั่ง**: ตั้งแต่ PR ของรอบนั้น
     `runtime.py` **ไม่ได้สะกดสตริง `MOB_LOOT_BOUNDARY_STASH_CLEARED` เองอีกแล้ว** — มันเรียก
     `mob_loot.boundary_stash_cleared_console_line()` ให้ประกอบบรรทัดแทน (คำสั่งรวมคำศัพท์ให้เหลือชุดเดียว
     `COO-DECISION 20260903_0054` ข้อ 2) ⇒ คำสั่งเดิมที่ปักคำเดียวจะตอบ **0 hit** ทั้งที่ของอยู่บน main
     และผู้เทสจะอ่านว่า "ยังไม่ merge" ผิด ๆ · **บรรทัดบนคอนโซลไม่เปลี่ยนสักตัวอักษร** สี่ฟิลด์เดิม ลำดับเดิม
     ต้องได้ **>= 1 hit** · 0 hit = ยังไม่ merge ⇒ **เลี่ยงการเก็บชิ้นสุดท้ายของฉากเป็นขั้นตัดสิน**
     (บั๊กเดิม: หยิบชิ้นสุดท้ายหลังวาปเข้าฉาก แล้ว poll ถัดไปประกาศใบ **ก่อนหยิบ** ⇒ ของกลับขึ้นพื้น
     คลิกซ้ำโดนปฏิเสธ ทั้งที่ของอยู่ในกระเป๋าและลง DB แล้ว = อ่านผลผิดทั้งรอบ)
     เมื่อ merge แล้ว ให้คัดบรรทัดนี้จากคอนโซลมาด้วยทุกครั้งที่เก็บของหลังวาป:
     บรรทัดมีสามแบบ อ่านที่ `reason=` และดู `rows_left=` ประกอบเสมอ:
     · `reason=superseded_by_pickup` = มีใบพื้นใหม่ทับให้แล้วในคลิกเดียวกัน (ปกติที่สุด)
     · `reason=last_object_pickup rows_left=0` = เก็บชิ้นสุดท้ายจริง ฉากว่าง ไคลเอนต์ **ไม่ถูกวาดใหม่** (ปกติ ไม่ใช่ FAIL)
     · `reason=publication_refused rows_left=-1` = 🔴 **ของยังอยู่บนพื้นอีกหลายชิ้น แต่เซิร์ฟเวอร์ประกาศพื้นไม่สำเร็จ**
       ⇒ ถ่ายภาพพื้นไว้ แล้วจดเป็นข้อสังเกตในรายงาน (ของที่เห็นบนจออาจไม่ตรงกับของที่คลิกได้จริง) ไม่ใช่ FAIL ของขั้นเก็บของ
     ไม่มีบรรทัดนี้เลย = ไม่มีสแตชค้างในคลิกนั้น (ก็ปกติ) · **ห้ามอ่านโทเคนนี้เป็นความล้มเหลวของการเก็บของ**
     · หมายเหตุรอบ `xcmfr6`: เดิมค่าที่อ่านไม่ออกทำให้ **ทั้งบรรทัดหาย** (ประกอบด้วย `%d` ในบล็อก `try`)
       ตอนนี้ตัวประกอบพิมพ์ `rows_left=-1` แล้วปล่อยบรรทัดออกเสมอ ⇒ เห็นแบบที่สามบ่อยขึ้นได้ **ไม่ใช่อาการใหม่ของเกม**
  2. `GT-188` checkpoint 2 ต้องมีผลบันทึกแล้วในใบของมันเอง และของต้องยังอยู่บนพื้นตอนที่ผู้เล่นเดินไปถึง --
     ไม่มีผล = **ชั้น client-observable ยัง BLOCKED** (ชั้น wire/DB บูตต่อได้ ผลที่คาดคือ P5 = NO-RESULT) ·
     🔴 ห้ามอ้าง `grep install_ground_vitals_preserve src/pirateforce_foundation/app.py`
     เป็นหลักฐานว่าผ่าน: บรรทัดนั้น **ต้องไม่มี** บน main วันนี้ (ถูกถอนโดย `COO-DECISION 20260902_0646`)
  3. ✅ **ผ่านแล้ว 2026-09-02T13:0x+07:00 (chief, R303) ตาม `COO-DECISION 20260902_1248` ข้อ 1** --
     composer ของ carrier `make_runtime_remote_actors` **อยู่บน main แล้ว** (PR #564 merge)
     ตรวจด้วย `git fetch origin` แล้วเปิดไฟล์บน `origin/main` `96503ff9` ตรง ๆ (ไม่ได้เชื่อหัวใบ):
     `mob_loot.preserve_ground_in_runtime_res_remote_actors` = `src/pirateforce_foundation/mob_loot.py:4090`
     และผู้เรียกบนสายฆ่า/ตี = `src/pirateforce_foundation/mob_combat.py:1429`
     ⇒ ข้อนี้ **ไม่กั้นการบูตอีกต่อไป** · ผลจริงของมันวัดที่ **ขั้น 2b** ของใบนี้ ไม่ใช่ที่ grep
     ~~ข้อความเดิมของข้อนี้ (เกต `"MOB_COMBAT_BAR": False`)~~ **ขีดฆ่าทั้งข้อ 2026-09-02T11:3x+07:00
     โดย chief ผู้เขียนมันเอง — มันเป็นเกตที่กั้นผิดเบิร์สต์** (pf-adversary D1)
     ข้อนี้เคยสั่งให้ grep หมุด `"MOB_COMBAT_BAR": False` ใน `tests/test_mob_combat_dispatch.py`
     แต่หมุดใบนั้นมาจาก `test_what_the_burst_says_about_the_ground_pool_frame_by_frame` ซึ่งเรียก `_attack`
     **โดยไม่ลด HP** ⇒ เป็นเบิร์สต์ของการ **ตีไม่ตาย** (`[MOB_COMBAT_ANNOUNCE, MOB_COMBAT_BAR]`)
     ส่วนเบิร์สต์ของใบนี้คือการ **ฆ่า** (`[MOB_COMBAT_ANNOUNCE, MOB_DEATH_DYING, MOB_DEATH_DEAD, MOB_LOOT_DROP...]`
     -- `tests/test_mob_combat_dispatch.py:695`) ซึ่ง **ไม่มี `MOB_COMBAT_BAR` อยู่เลย**
     ⇒ วันที่สาย B ลง composer ของ bar เป็นตัวแรก (ตามลำดับ bar → dying → dead ที่ `COO 1044` สั่ง)
     หมุดจะพลิกเป็น `True` เกตจะเขียว **ทั้งที่ dying/dead ซึ่งเป็นเฟรมของใบนี้ยังไม่ถูกแตะเลย**
     ⇒ ไม่มีเกตแทนที่ และ **ไม่ต้องมี**: ใบนี้เลิกทำนายผลแล้ว (ดูบล็อกหัวใบ) เห็นของ = คลิก
     ไม่เห็น = `P5 NO-RESULT` · คำถาม "เฟรมสุดท้ายหลังของตกคือเฟรมไหน และพกบิต `0x08` ไหม"
     เป็นของ **สาย B** ตอบก่อนเขียนโค้ด (`COO-DECISION 20260902_1044` ข้อ 5) ไม่ใช่ของผู้เทสใบนี้

- links: `COO-DECISION 20260902_0542` ข้อ 3 (ใบนี้) · `COO-DECISION 20260902_0541` (ปลด HELD ของ call site) ·
  `COO-DECISION 20260902_0646` (ถอน wrap · opt-in ทีละจุดเริ่มที่ `action_ack` ยังไม่ขึ้น main) ·
  `GT-188` (ประตู) · `GT-146` (ใบ capture opcode -- ผล (b)/(c) ของใบนี้ป้อนใบนั้น) · `GT-124` · `GT-142` ·
  `RE-125` (`CLIENT_RE_QUEUE.md:1761`, CLOSED BOUNDED-NEGATIVE) · `RE-067` (สีป้าย) ·
  `PANYA-DECISION 20260828_0125` (ตัวละครสมประกอบ) ·
  `pirate-force-server/src/pirateforce_foundation/mob_pickup_request.py:192,289,587` ·
  `pirate-force-server/src/pirateforce_foundation/mob_pickup_persist.py:213-238` (`MOB_PICKUP_ROW_INSERTED`) ·
  `pirate-force-server/migrations/003_character_inventory.sql:9` (`character_backpack_items`)

- result: (ผู้เทสกรอก) ผล (a)/(b)/(c) + P1-P5 · เวลาคลิก (+07:00 และ `t` วิดีโอ) · path + sha256 ของ
  console/`GAME_LIVE.txt`/`GAME_EVENTS_LIVE.txt`/ภาพ/วิดีโอ · จำนวนแถว `character_backpack_items` ก่อน/หลัง +
  ค่าทุกคอลัมน์ของแถวใหม่ · บรรทัดคอนโซลเต็มทุกโทเคน · สามช่องบนจอ (ป้ายหาย/กระเป๋าเพิ่ม/ข้อความระบบ) ·
  **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ** · NO-CRASH/CRASH · sha canonical ก่อน/หลัง · `integrity_check`
  🔴 **G-OBS:** จดหมายผลของใบนี้ **ต้องมีบรรทัด** `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ·
  ตราบใดที่ยังไม่มีบรรทัดนี้ สถานะใบคือ **`AWAITING-OBSERVER` ไม่ใช่ `PASS`** และห้ามยกผลใบนี้ไปเป็นฐานของใบอื่น

**ผู้เปิดใบ: chief (LANE-E) รอบ `ls5m3c` / R300 ตาม `COO-DECISION 20260902_0542` ข้อ 3**

## GT-207 GM-PLUGIN-THREE-CELL-BUTTON-001  [**PASS** on build 1 -- ka1-A/เจ้าของ 2026-09-02T18:54+07:00 · `OBSERVER_CONFIRMED` มีในใบผล · ผล: `notes_to_chief/20260902_1915_KA1A-GT-207-PASS-the-gm-button-opens-the-gmui-window-on-build-1-and-p3-is-unblocked.md` · ปิดหัวใบโดย LANE-GM (เจ้าของใบ) รอบ `selrsl` · ~~[READY]~~]

> 🔴 **DEVIATION ที่ผู้เทสประกาศเอง และ LANE-GM รับ ไม่ถือว่าเป็น INCONCLUSIVE**: build 1 ออกมาไม่มี manifest ฝัง (= `verdict=manifest_missing` ตามใบ ⇒ ต้องหยุด) แต่เครื่องมี `mt.exe` และเจ้าของเลือกให้ฝังเอง (`mt.exe -manifest GameMaster.dll.manifest -outputresource:GameMaster.dll;#2`) แล้วขั้น 0 จึงผ่านเป็น `image_ok` · เหตุที่รับ: จุดประสงค์ของ STOP คือ "ห้ามบูต DLL ที่โหลดไม่ได้" การฝัง manifest คือสิ่งที่ทำให้มันโหลดได้ และไม่มีไฟล์ใน `patches/gm_plugin/` ถูกแก้ระหว่างรอบนั้นเลย · ขั้น `mt.exe` เข้าสคริปต์แล้วใน `#887` (revision 5) ⇒ รอบถัดไปไม่ต้อง deviate อีก
> 🔴 **`PASS` ของใบนี้ไม่ย้าย `NOW.md` P-3 ไป "รอ Panya ติ๊ก"** (`COO-DECISION 20260902_2147` ข้อ 3): สคริปต์ทั้งสาม (`find_mt.bat` / `build_vs2008.bat` rev.5 / `install.bat`) **ยังไม่เคยถูกรันเลย** ใบนี้ตอบว่า "ปุ่มเปิดหน้าต่างได้เมื่อมี DLL ที่โหลดได้" ไม่ได้ตอบว่า "สคริปต์ในรีโปผลิต DLL ที่โหลดได้เอง"
> ของแถมที่ใบนี้ตอบแล้ว: `RE-164` = **ไม่มี** `GameMaster.dll` ข้าง exe มาก่อน (สามชั้นจาก `GameClient\`)

> 🔴 **NUMBERING — ใบนี้คือ `GT-207` และถูกขยับสองครั้ง เขียนไว้ให้ครบ:**
> ใบที่ `COO 0846`/`LANE-GM 0731` เรียกว่า `GT-P3`/`GT-203` **คือใบนี้** · `203` เป็นของ LANE-A
> และ `204` เป็นใบ P-1 ของ chief ไปแล้ว ⇒ ขยับเป็น `205` ตอนลงคิว
> จากนั้น **LANE-A merge `GT-205 UI-A-BACK-BUTTON-VISIBLE-NOTICE-001` ขึ้น `main` ก่อน** ระหว่างรอบเดียวกัน
> ⇒ กฎ ③ (คนที่ push ทีหลังขยับเลขของตัวเอง) · `206` ถูกใบ `RE-206` ของรอบนี้ใช้ไปแล้ว ⇒ **ใบนี้ = `207`**
> ไม่มีใบของใครถูกลบ ย้าย หรือทับ · `GT-205` ที่ถูกต้องคือใบของ LANE-A ข้างบนนี้
> 🔴 `NOW.md` P-3 ยังเขียนว่า "ใบ `GT-203`" — **ชี้ผิดใบ** (`GT-203` คือใบ AvatarAttr ของ LANE-A) ·
> chief แก้ `NOW.md` เองไม่ได้ (ผู้เขียนคือ Panya กับ COO) ⇒ ขอไว้ในใบ `CHIEF-TO-COO 20260902_0920`

- objective: ข้อเดียว — ปุ่ม GM ที่กดแล้วเงียบมาตั้งแต่ `RE-104` (27 ส.ค.) เปิดหน้าต่างได้หรือไม่
  เมื่อมี `GameMaster.dll` ที่เราสร้างเองอยู่ข้าง client (สถานะ GM ยังตัดสินที่ `gm_accounts` ฝั่งเซิร์ฟเวอร์เท่านั้น)

- ของที่ใช้: `patches/gm_plugin/` **revision 4** sha `780d41dd` [วัดแล้ว: เป็น ancestor ของ `main`, 07:58+07:00]
  ไม่ใช่ revision 3 (ไม่เคย commit) · **คำห้าม build ถอนแล้ว** (`COO 0845`)
  install/rollback ตาม `patches/gm_plugin/README.md` (`install.bat "<client folder>"` ห้าม copy เอง)

- 🔴 **เปิด DebugView ค้างไว้ก่อนบูตทุกครั้ง** — ทั้งใบตัดสินด้วยบรรทัด `[GM_PLUGIN]` ไม่มีตัวจับ = อ่านผลไม่ได้เลย

### ลำดับต่อหนึ่ง build (ห้ามสลับ — ขั้น 0 อยู่ **หลัง** install)
`build` → `install.bat` → **ขั้น 0** → บูต → ล็อกอินบัญชีใน `gm_accounts` → **กดปุ่ม GM หนึ่งครั้ง** → ปิดเกม → **rollback**

- **ขั้น 0** (จาก checkout ของ `pirate-force-server` · `set PYTHONPATH=src`) — 🔴 ใส่เครื่องหมายคำพูด **ทั้งสองพาธ**
  (พาธของเจ้าของมีช่องว่าง ไม่ใส่ = argparse ตัดครึ่งแล้วรายงานผิดใบ):
  `py -3 -m pirateforce_foundation.gm.plugin_image_check --dll "<build>\GameMaster.dll" --client-dir "<client>"`
  · ค่าที่ต้องได้คือ `verdict=image_ok` (แปลว่า ไฟล์ที่ติดตั้ง = ไฟล์ที่เพิ่ง build)
  · 🔴 **รันก่อน install จะได้ `verdict=missing` exit 1 เสมอ** — นั่นไม่ใช่ของเสีย แค่รันผิดลำดับ
  · 🔴 `verdict=manifest_missing` = **หยุด build นี้ บันทึก แล้วรายงาน LANE-GM** — เป็นช่องโหว่ของ build chain
    (`build_vs2008.bat` ไม่มีขั้น `mt.exe` และ VS2008 ไม่มี `/MANIFEST:EMBED`) **ไม่ใช่ความผิดของผู้เทส**
    และ **ห้ามบูตทั้งที่เห็นค่านี้** [เสนอ โดย pf-adversary รอบ `smrum3` — ยังไม่มีใครสร้างจริงบน MSVC]
  · exit code อื่นที่ไม่เป็น 0 = หยุด ห้ามบูต แก้ตามที่มันบอกก่อน
- 🔴 `install.bat` ปฏิเสธเพราะเจอ `GameMaster.dll` เดิม → **ก่อนรายงานว่าเจอของเก่า ให้เทียบ sha256 ของไฟล์นั้น
  กับ sha256 ที่ขั้น 0 ของ build ก่อนหน้าบันทึกไว้เสมอ** · ตรงกัน = **ของเราเองที่ลืม rollback** ให้ลบแล้วเดินต่อ ·
  ไม่ตรง = **หยุดทั้งใบ** เก็บ sha256 แล้วรายงานทันที (นั่นคือของที่ตามหามาตั้งแต่ 27 ส.ค. `RE-164`)
- **rollback ทุกครั้งที่จบ build ไม่ว่าผลจะเป็นอะไร**: ลบ `GameMaster.dll` ที่ติดตั้งออกจากข้าง client
  (ไม่มี patch ไบต์ ไม่มี registry ไม่แตะ DB) · ลืมข้อนี้ = รอบหน้าจะอ่านของเราเองเป็นหลักฐาน `RE-164` ผิด ๆ

### ขั้น 0N — negative control ของ `check 0/4` **หนึ่งครั้งเดียวทั้งใบ** (`COO-DECISION 20260902_2148` ใบที่ 2)
ทำ **ก่อน** build แรก · **ไม่กินโควตา build** · ไม่บูตเกม ไม่แตะ client ไม่แตะ DB · ใช้เวลาไม่ถึงหนึ่งนาที

**เหตุผลที่ต้องทำ** — LANE-GM เขียนไว้เองในใบ `20260902_2038` nonclaim 3ก: `check 0/4`
(`mt.exe -inputresource:...;#2 -validate_manifest`) เขาเขียน **จากเอกสารของ Microsoft ไม่ได้วัดเอง**
⇒ วันนี้ไม่มีใครรู้ว่ามันกันอะไรได้จริงหรือเปล่า และมันคือเกตที่ยืนขวางไม่ให้ DLL ที่โหลดไม่ได้เข้าโฟลเดอร์ client

**ทำอะไร** ชี้เกตไปที่ DLL ที่ **รู้ว่าเสีย** — ตัวที่ ka1-A วัดเองแล้วว่า `LoadLibraryW` ปฏิเสธ
(**13,824 ไบต์ · sha256 `67501F7E...F496`** · ตัวที่ *ไม่มี* เซกชัน `.rsrc` · ใบ `20260902_1920_KA1A-TO-LANE-GM-*`)
ถ้ายังมีไฟล์นั้นอยู่ ใช้ตัวนั้น · ถ้าลบไปแล้ว สร้างขึ้นใหม่ได้ด้วย `build_vs2008.bat` **ที่ข้ามขั้น `mt.exe`**
(หรือคัดสำเนา DLL ที่บิลด์เสร็จแล้วมาลบ `.rsrc` ออก) — เกณฑ์คือ **DLL ที่ไม่มี manifest ฝัง** ไม่ใช่ sha ตัวนั้นเป๊ะ ๆ

`py -3 -m pirateforce_foundation.gm.plugin_image_check --dll "<DLL ที่ไม่มี manifest>" --client-dir "<client>"`
(หรือรัน `check 0/4` ของ `install.bat` ตรง ๆ ถ้าเรียกแยกได้ · จดคำสั่งที่ใช้จริงลงผลด้วย)

**อ่านผลยังไง — ทั้งสองผลคือข้อมูลที่วันนี้เราไม่มี ไม่มีผลไหน "เสียรอบ"**
- **แดง** (`verdict=manifest_missing` หรือ exit ไม่เป็น 0) = เกตทำงานจริง ⇒ จดว่าแดง แล้วเดินต่อไป BUILD ตามปกติ
- **เขียว** (`image_ok` / exit 0) = 🔴 **เกตนี้ไม่เคยกันอะไรได้เลย** ⇒ จดไว้ให้ชัด **แล้วยังเดินต่อไป BUILD ได้**
  แต่ตั้งแต่จุดนั้น `check 0/4` ในผลของใบนี้ **ห้ามถูกอ้างเป็นหลักฐานว่า DLL ครบ** ต้องพึ่งเกต `.rsrc` (`dumpbin`) แทน
- **รันไม่ได้** (ไม่มี `mt.exe` / เรียกแยกไม่ได้) = จด `NO-RESULT` ของขั้นนี้บรรทัดเดียวแล้วเดินต่อ **ห้ามหยุดทั้งใบเพราะขั้นนี้**

nonclaim ของขั้นนี้: ไม่พิสูจน์ว่า DLL ของ build ไหนดีหรือเสีย · พิสูจน์แค่ว่า **เครื่องมือวัดตัวนั้นขยับหรือไม่ขยับ**
เมื่อชี้ไปที่ของที่รู้ว่าเสีย · ไม่แตะข้อสรุปของ `RE-164` และไม่เปลี่ยนเกณฑ์ผ่าน/ไม่ผ่านของใบนี้แม้แต่ข้อเดียว

#### ขั้น 0N-b — ลองฝัง manifest ที่ `;#1` **ขั้นสุดท้ายที่ไม่ให้คะแนน** (`COO-DECISION 20260902_2343`)
🔴 **ขั้นนี้ไม่มีน้ำหนักต่อ PASS/FAIL ของใบเลย ข้ามได้ทุกเมื่อ** — ไม่มี `mt.exe` หรือเวลาหมด = จด `NO-RESULT`
บรรทัดเดียวแล้วเดินต่อ ใบยังตัดสินได้ตามปกติ · 🔴 **ห้ามเอาสำเนานี้ไปวางในโฟลเดอร์ไคลเอนต์** ทดลองนอกโฟลเดอร์เกมเท่านั้น

1. คัดสำเนา DLL ที่ build เสร็จแล้วหนึ่งตัวไว้ **นอกโฟลเดอร์ client** แล้วฝัง manifest ใบเดียวกันที่ `;#1`
   `mt.exe -manifest GameMaster.dll.manifest -outputresource:<สำเนา>;#1`
2. `LoadLibraryW` สำเนานั้น **จดผลดิบ**: สำเร็จ หรือ error code (คาดว่า `14001`) · จดคำสั่งที่ใช้จริงลงผลด้วย

**เหตุผล** — กฎ "manifest ต้องอยู่ที่ id 2" ที่ `COO 20260902_2147` สั่งไว้ **ไม่เคยมีใครวัด** LANE-GM รายงานตรง ๆ เอง
(ใบ `20260902_2252` ข้อ 2 · COO นับเป็นความดี) · **โหลดสำเร็จ = กฎนั้นผิด** ⇒ ลดกิ่ง `RT_MANIFEST id 2` เป็น advisory ทันที
· **โหลดไม่สำเร็จ = กฎถูก** และเรามีหลักฐานแทนคำสั่ง · แต่รอบของเจ้าของแพงเกินกว่าจะให้คำถามเชิงวิชาการมีสิทธิ์ทำใบหลักตก

nonclaim: ไม่พิสูจน์อะไรเกี่ยวกับ DLL ที่ใบนี้กำลังทดสอบ · พิสูจน์แค่ว่า **loader ยอมรับ manifest ที่ id 1 หรือไม่**
· ไม่เปลี่ยนเกณฑ์ผ่าน/ไม่ผ่านของใบนี้ และไม่ใช่เหตุให้ rebuild

### BUILD (นับเป็น **build** ไม่ใช่ "ช่อง" — เพดาน **สาม build** ทั้งใบ รวมกิ่งแครช)
| build | `PF_GM_KEY` | `PLUS4` | คำสั่ง | build เมื่อ |
|---|---|---|---|---|
| 1 | `GMUI_1` | 0 | `build_vs2008.bat` เปล่า ๆ | เสมอ |
| 2 | `GMUI_BASIC` | 0 | `set EXTRA_DEFS=/D PF_GM_KEY=L\"GMUI_BASIC\"` | build 1 มี `loaded` + `client CRT:` แต่คลิกไม่เปิด |
| 3 | `GMUI_1` | 1 | `set EXTRA_DEFS=/D PF_GM_SLOT0_TOUCH_PLUS4=1` | build 2 ยังไม่เปิด |

🔴 **`set` เขียนทับ ไม่ได้บวกกัน** — build 3 จึงกลับไปเป็น `key=GMUI_1` **โดยตั้งใจ** (ตรงกับตาราง README)
เห็น `key=GMUI_1` ใน build 3 = **ถูกแล้ว ห้าม rebuild** · ห้าม build `GMUI_BASIC` + `PLUS4=1` (ช่องที่สี่) ทุกกรณี

🔴 **STOP ก่อนเปลืองรอบ — ถ้า build 1 ขึ้น `loaded` แต่คลิกแล้ว *ไม่มี* บรรทัด `client CRT:`**
= client ยังไม่เคยเรียก `CreateGameMaster` ⇒ `PF_GM_KEY` และ `PLUS4` **ยังไม่ถูกอ่านเลย**
⇒ build 2 กับ build 3 เป็นการทดลองที่เหมือน build 1 ทุกประการ **หยุดทั้งใบตรงนี้ รายงาน** อย่า build ต่อ
(นี่คือผลลัพธ์ที่มีค่า ไม่ใช่รอบเสีย: มันชี้ไป `GM-IMG-005`/`RE-164` โดยตรง)

🔴 **กิ่งแครช (`COO 0845` ข้อ 2)** — แครช **ตอนคลิก**:
- แครชใน **build 1** → build ถัดไป = `PLUS4=1` คง key เดิม (`GMUI_1`+`PLUS4=1`) = แถว 3 ของตาราง **ทำได้**
  build นี้กินโควตาไปหนึ่ง ⇒ เหลืออีกหนึ่ง build เท่านั้นทั้งใบ
- แครชใน **build 2** (`GMUI_BASIC`) → 🔴 **หยุดทั้งใบ รายงาน ห้าม build ต่อ** — เพราะ "คง key เดิม + `PLUS4=1`"
  จะกลายเป็น `GMUI_BASIC`+`PLUS4=1` = **ช่องที่สี่ที่ README ห้ามไว้** · `COO 0845` กับตาราง README ขัดกันตรงนี้
  และยังไม่มีใครตัดสิน ⇒ แครชใน build 2 เป็น **ผลที่ต้องรายงาน** ไม่ใช่เหตุให้ build ต่อ
- 🔴 **ห้ามใช้ "sha256 เปลี่ยน" เป็นหลักฐานว่าแฟล็กถึง compiler** — DLL ฝัง `__DATE__`/`__TIME__` ทุก rebuild
  จึงเปลี่ยน sha เสมอแม้ลืม `set` · ตัวควบคุมจริงคือบรรทัด `EXTRA_DEFS=` ที่สคริปต์พิมพ์ กับ `key=`/`slot +0x00 +4 init:`

### RECHECK (ตามลำดับ ข้อ 1 ทำให้ข้ออื่นมีความหมาย · ทุกบรรทัดมีอยู่จริงในซอร์ส revision 4 [วัดแล้ว])
1. `[GM_PLUGIN] loaded build=<วันเวลา>` **ตอนบูต** — บรรทัดแรกสุดที่ `DllMain` พิมพ์ ก่อนโค้ดที่ fault ได้
   ⇒ **ไม่มี = DLL ไม่เคยถูกโหลด** (ข้ออื่นไม่ต้องอ่าน) · 🔴 บรรทัดนี้บอก **เวลา build ไม่ได้บอก revision**
2. **บรรทัดผลของการคลิก — ข้อที่ตัดสินว่ารอบนี้ได้ข้อมูลจริงหรือไม่** คัดมาทั้งบรรทัด ห้ามสรุปเอง
   หนึ่งในห้าบรรทัดนี้ต้องขึ้นตอนคลิกครั้งแรก:
   · `alive, returning interface` ← **ปลั๊กอินทำงานครบและส่งของให้ client จริง**
   · `FAIL alloc: client CRT operator new unavailable; returning NULL`
   · `FAIL: msvcp90 wstring ctor unresolved and PF_GM_SLOT0_TOUCH_PLUS4=1; returning NULL` (เจอได้เฉพาะ build 3)
   · `FAIL exception in CreateGameMaster; returning NULL`
   · **ไม่มีสักบรรทัด** = client ไม่เคยเรียก `CreateGameMaster` (ดู STOP ข้างบน)
3. `client CRT: ...` / `msvcp90 wstring ctor: ...` / `self-pin: ...` ขึ้น **ตอนคลิกครั้งแรก ไม่ใช่ตอนบูต**
   [วัดแล้ว ในซอร์ส: `ResolveOnce()` ถูกเรียกจาก `CreateGameMaster` ที่เดียว · `DllMain` เขียนเองว่า deferred]
   [เสนอ: ว่า **การคลิก** คือสิ่งที่ไปถึง `CreateGameMaster` — นั่นคือคำถามของทั้งใบ ยังไม่มีใครวัด]
   · `client CRT:` เขียน `REFUSING` **หรือ** `NOT FOUND` ให้คัดพาธ/ข้อความที่ตามมาด้วยทั้งหมด
4. `key=` และ `slot +0x00 +4 init:` ตรงกับตาราง BUILD ข้างบนของ build ที่กำลังเทส
   🔴 สองบรรทัดนี้ขึ้น **สองรอบต่อเซสชัน** (ตอนบูตจาก `DllMain` และตอนคลิกครั้งแรกจาก `ResolveOnce`) — อ่าน**ของตอนบูต**
5. **คลิกแล้วหน้าต่าง `GMUI_1` เปิด ถึง tab `GMUI_BASIC` หรือไม่** ← ข้อที่ตัดสินทั้งใบ
6. ปิดเกมแล้วไม่แครช (มีความหมายเมื่อข้อ 1 ผ่าน) · แครชตอนปิด ให้ดู `self-pin:` ก่อนเสมอ
7. 🔴 `slot +0x08 called with no MSVCP90 ctor` = **หลักฐานใหม่ ต้องรายงาน ห้ามแก้เอง**
   🔴 **ไม่เห็นบรรทัดนี้ = `NO-RESULT` ของข้อ 7 เท่านั้น** ห้ามบันทึกว่า "ไม่มีใครเรียก slot 8" --
   บรรทัดนี้มีประตูสองชั้น (slot 8 ถูกเรียก **และ** `msvcp90` ctor resolve ไม่ได้ · สาขา
   `if (g_wstringCtor == NULL)` ใน `MakeEmptyString`) ⇒ บน build ที่ ctor resolve **ได้**
   การเรียก slot 8 จะ default-construct แล้วคืนค่า **เงียบสนิทโดยการออกแบบ**
   ⇒ ห้ามเอาผลลบของข้อ 7 ไปปิดหรือยืนยัน blocker `NO_PINNED_CALL_ROUTE_FOR_SLOT8` ของ `GM-IMG-014`
   🔴 **เกณฑ์อ่านว่า ctor resolve ได้หรือไม่ ต้องดูคำว่า `NOT RESOLVED` ห้ามดูคำว่า `resolved`**
   (แก้คำของ chief เอง 11:3x -- pf-adversary N1 · วัดจาก `patches/gm_plugin/GameMaster.cpp` โดยตรง):
   สาขาที่ **สำเร็จ** มีสองสาขา บรรทัด `:667` ขึ้นว่า `msvcp90 wstring ctor: resolved from the client's own ...`
   แต่บรรทัด `:671` ขึ้นว่า `msvcp90 wstring ctor: the client does not import it, but the msvcp90.dll
   instance it is bound to exports it` -- **ไม่มีคำว่า `resolved` เลย**
   ⇒ ถ้าเกรปหาคำว่า `resolved` แล้วไม่เจอบนเครื่องที่เข้าสาขา `:671` จะสรุปผิดว่า "ctor พัง"
   แล้วเอาผลลบของข้อ 7 ไปปิด blocker ผิด ซึ่งคือความผิดพลาดที่ข้อนี้ถูกเพิ่มมาเพื่อกัน
   **อ่านแบบนี้แทน:** ขึ้น `NOT RESOLVED` (`:662` หรือ `:674`) หรือ `degraded: no MSVCP90 wstring ctor` (`:750`)
   = ctor พังจริง ⇒ ข้อ 7 ใช้ได้ตามปกติ · **ไม่ขึ้นคำเหล่านั้น = ctor ใช้ได้ ⇒ ข้อ 7 เป็น NO-RESULT เสมอ**
   (ที่มา: LANE-GM `notes_to_chief/20260902_1005_LANE-GM-TO-CHIEF-gt207-recheck7-needs-its-second-gate.md`
   อ่านไบต์จริงของ revision 4 `780d41dd` · chief รับคำนี้ทั้งประโยคใน R302)
   (`GM-IMG-014` blocker `NO_PINNED_CALL_ROUTE_FOR_SLOT8`)

### หลักฐานสองชั้น
- **client-observable** = ภาพหน้าจอตอนคลิก (เปิด/ไม่เปิด) + ข้อความ debug ทั้งชุดของแต่ละ build
- **wire/DB** = ใบนี้ **ไม่มีชั้นนี้และไม่ต้องมี** ปลั๊กอินเป็น client ล้วน ไม่แตะ vital ไม่แตะ DB ไม่เปิด canonical
  (`gm_accounts` เป็นไฟล์ JSON allowlist ไม่ใช่ DB) · ใครอ้างว่าใบนี้พิสูจน์อะไรฝั่งเซิร์ฟเวอร์ = อ้างผิด

### เกณฑ์ปิดใบ
- **PASS** = build ใด build หนึ่งเปิดหน้าต่างได้ → บันทึกว่า build ไหน แล้วปิด P-3
- **bounded negative** = 🔴 **ใช้ได้ต่อเมื่อทุก build ขึ้นบรรทัด `alive, returning interface`** (RECHECK 2)
  แล้วยังไม่เปิดสักอัน → "ปลั๊กอินทำงานครบแล้ว แต่ประตูไม่ได้อยู่ที่ตัวปลั๊กอิน" → กลับไป `RE-164` ผู้ต้องสงสัยข้อ 1
  (`GM-IMG-005` gate `GMModule_Client+0x19`) **ห้ามอ่านว่า "ปลั๊กอินใช้ไม่ได้"**
  🔴 เห็น `FAIL ...` หรือไม่เห็นบรรทัดไหนเลย = **ไม่ใช่ bounded negative** เป็น `INCONCLUSIVE-PLUGIN-NEVER-RAN`
  ⇒ ห้ามใช้ปิดหรือเบนงานของ `RE-164` เด็ดขาด (ปลั๊กอินไม่เคยได้ลอง key ที่ใบนี้ตั้งใจจะเทส)
  ⚠️ ระวัง: `GM-IMG-005` เขียนเองว่าไบต์นั้นคุม **ทั้ง show และ click gate** แต่ปุ่ม **มองเห็นได้** (`RE-104`)
  ⇒ ถ้าจะสรุปไปทางนั้น ต้องอธิบายความตึงข้อนี้ก่อน [เสนอ ยังไม่มีใครไล่ disassembly]
- **BLOCKED** = ไม่มี `loaded` เลย → ผลของ `plugin_image_check` คือคำตอบ ไม่ใช่การเดา
  ⚠️ `image_ok` แต่ไม่มี `loaded` **และเกมเปิดไม่ขึ้นด้วย** = คนละอาการ (ตายใต้ loader lock)
  ⇒ ลบไฟล์ออก ยืนยันว่าเกมกลับมาเปิดได้ บันทึกแล้วรายงาน — อย่าวนไป build ถัดไป

### ของแถม / result / links
- ของแถม (`RE-164` · NOW.md P-3): มี `GameMaster.dll` อยู่ข้าง exe **ก่อน** ติดตั้งของเราไหม — ตอบ มี/ไม่มี หนึ่งบรรทัด
  (ถามก่อนแตะอะไร เพราะหลัง build แรกจะแยกไม่ออกจากของเราเอง)
- ก่อนเริ่ม: ยืนยันหนึ่งบรรทัดว่าบัญชีที่จะล็อกอิน **อยู่ใน** `config/gm_accounts.json` จริง —
  ไม่งั้น "คลิกเงียบ" แยกไม่ออกระหว่าง "ไม่มีสถานะ GM" กับ "ปลั๊กอินเงียบ"
- links: `COO 20260902_0846` `0845` `0648` · `LANE-GM 0731` `0801` `0856` · `RE-164` · `RE-104` ·
  `patches/gm_plugin/README.md` (ตารางช่อง + install/rollback) · `PF_GM_PLUGIN_GATE.tsv` (`GM-IMG-001..017`)
- RECHECK: `git -C <pf_bridge> merge-base --is-ancestor 780d41dd HEAD`
  -- exit 0 = **checkout ที่จะ build อยู่จริงที่ revision 4** (ใช้ `HEAD` ไม่ใช่ `origin/main`: fetch แล้วแต่ยังไม่ merge
  จะทำให้ `origin/main` ผ่านทั้งที่ working tree ยังเป็น revision 2 ที่ถูกห้าม) · คำสั่งเดียว ไม่มี `&&` (PS 5.1 ไม่รับ)
- result: (ผู้เทสกรอก) จำนวน build ที่ทำจริง + บรรทัด `EXTRA_DEFS=` ของแต่ละอัน · `verdict` + sha256 คู่จากขั้น 0 ทุก build ·
  บรรทัด `[GM_PLUGIN]` ทั้งชุดต่อ build (**แยกตอนบูต / ตอนคลิก**) · บรรทัดผลของ RECHECK 2 ทั้งบรรทัด ·
  ภาพหน้าจอตอนคลิก · เปิด/ไม่เปิด · แครชหรือไม่ (ตอนคลิก / ตอนปิด) · rollback ทำแล้วทุก build หรือไม่ ·
  คำตอบหนึ่งบรรทัดของ `RE-164`
  🔴 **G-OBS:** จดหมายผลต้องมีบรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ·
  ไม่มี = **`AWAITING-OBSERVER` ไม่ใช่ `PASS`** ห้ามยกผลใบนี้ไปเป็นฐานของใบอื่น
- nonclaim: (1) หน้าต่างเปิด **ไม่ใช่** ข้อพิสูจน์ว่าคำสั่ง GM ใดทำงาน และไม่ใช่ไมล์สโตน
  (2) ไม่อ้างว่า revision 4 คอมไพล์ผ่าน MSVC — ไม่มี toolchain บนคลาวด์ (`COMPILE-UNVERIFIED` อยู่หัวไฟล์)
  (3) ไม่อ้างว่าปลั๊กอินคือสาเหตุของ P-3 — กำจัดผู้ต้องสงสัยหนึ่งตัวเท่านั้น
  (4) ใบนี้ไม่ให้สถานะ GM กับใครเลย เป็นเครื่องมือไปถึงสภาพที่จะเทส

**ผู้เปิดใบ: LANE-GM รอบ `q6p0pb` (ร่าง `0731`) · chief (LANE-E) รอบ `smrum3`/R301 ลงคิวตาม `COO-DECISION 20260902_0846`**
**แก้ตาม pf-adversary รอบเดียวกัน 16 ข้อ** (ลำดับขั้น 0 · `manifest_missing` · กิ่งแครช build 2 ขัดตาราง README ·
`alive, returning interface` เป็นเงื่อนไขของ bounded negative · STOP เมื่อไม่มี `client CRT:` · rollback ทุก build ·
sha256 discriminator ของ `RE-164` · RECHECK ที่รันได้บน PS 5.1 · quote พาธ · ค่าคาดหวังต่อ build)

## GT-210 CHOOSE-NPC-SCENE3-CLICK-ANSWER-001  [✅ **PASS · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — R306 บนจอเจ้าของ (`notes_to_chief/20260903_1657_*`) · 🔴 เกณฑ์ (ก)/(ง2) ของใบนี้ **วัดไม่ได้ในรอบนั้น** เพราะโทเคนตอน boot พิมพ์ก่อน `.err.txt` เปิด (`1743` ข้อ 3 ข้อย่อย 5 · เป็นหนี้เครื่องมือของ chief ไม่ใช่ FAIL ของใบ) · สถานะเดิม: 🟢 READY -- RECHECK ผ่าน **วัดเองโดย LANE-A (เจ้าของใบ) รอบ `mcf4qp` 2026-09-03T08:3x+07:00** บน `origin/main` (สะพาน `d1c7eed` · เซิร์ฟเวอร์ `f240ab4`) · ~~[BLOCKED -- โค้ดยังไม่ขึ้น `main`: branch `claude/dazzling-volta-326kf4`]~~ กิ่งนั้น merge ไปแล้ว
🔴 **ใบนี้ถูกเขียนใหม่หลายจุดในรอบ `mcf4qp` เพราะโลกเดินไปแล้ว ห้ามอ่านฉบับเก่าจาก git history แล้วเดินตาม:** เก้าเกาะที่ใบนี้เคยใช้เป็น "ตัวควบคุมเชิงลบ" **ตอบคลิกแล้วตั้งแต่รอบ `gwwpmr`** และฉาก 2 ก็ตอบแล้ว ⇒ ฉบับเก่าจะสั่งให้ผู้เทส **หยุดทั้งใบและรายงานว่าเสีย** ทั้งที่บิลด์ถูกต้อง และขั้นบูตข้อ 2 ของมันเป็นไปไม่ได้อีกแล้ว (`NO-RESULT` แน่นอน) ⇒ **บูตหนึ่งครั้งของเจ้าของจะสูญฟรี** · จุดที่แก้: ขั้น 2 · **ขั้น 9 ถูกลบทั้งข้อ** · เกณฑ์ (ก)/(ง)/(ง2)/(ซ) · FAIL branch · RECHECK (เขียนใหม่ให้รันได้บน PS 5.1)
🟢 **บูตเดียวรวมกับ `GT-212` ได้และควรทำ** -- ใบนี้ (`/warp 3`) ก่อน แล้วค่อยเดินตาม `GT-212` (`/warp 4` ...)]

> เปิดโดย LANE-A (WORLD) รอบ `326kf4` 2026-09-02T12:2x+07:00 · **LANE-A บริโภคผลเอง**
> numbering: คำสั่งค้นหาตามกฎ ② คืน `209` (`RE-209`) ⇒ ใบนี้ `210`
> บูต/DB/teardown ตาม `ATTENDED_SESSION_RUNBOOK.md` (teardown ปฏิเสธ boot stamp เก่ากว่า 420 นาที)
> 🔴 **ใบนี้เคยร่างไว้ครอบสิบฉาก แล้วหดเหลือฉากเดียวก่อนลงคิว** — pf-adversary วัดบน dispatcher จริงว่า
> อีกเก้าฉากจะเปิดเควสต์ Columbus ของพอร์ตรอยัลผิดเกาะไปด้วย ⇒ สายกันเก้าฉากนั้นไว้เอง (ดู background ข้อ 3)
> 🔴 **ประวัติ ไม่ใช่สภาพวันนี้ (รอบ `mcf4qp`): เก้าฉากนั้นเปิดไปแล้วตั้งแต่รอบ `gwwpmr` หลัง scene guard ลง `runtime.py`**

- objective: ข้อพิสูจน์เดียว -- **คลิกซ้ายหนึ่งครั้งบน NPC ในฉาก 3 (Spice Paradise) แล้วไคลเอนต์
  วาดคำตอบบนจอจริง** ที่เมื่อวานคลิกแล้วเซิร์ฟเวอร์เงียบสนิท (62 actor) · ตัวควบคุมอยู่ในข้อพิสูจน์
  เดียวกัน ไม่ใช่ข้อที่สอง: คำตอบส่ง roster **ทั้งชุด** ใหม่ ⇒ actor ตัวอื่นต้องไม่เปลี่ยนหน้าตา ไม่หายเลเวล
- background:
  1. ของใหม่: `src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_roster_scenes.py`
     `production_allowed = True` · ~~ลงทะเบียน ChooseNPC responder **ให้ฉาก 3 ฉากเดียว**~~
     **แก้รอบ `mcf4qp`: วันนี้โมดูลเดียวกันลงทะเบียนสิบเอ็ดฉาก** (3,4,5,6,7,8,9,10,11,126,130) ·
     **ใบนี้ยังตัดสินฉาก 3 ฉากเดียวเหมือนเดิม** ฉากอื่นเป็นของ `GT-212`/`GT-217`
  2. การลงทะเบียน responder คือสิ่งเดียวกับที่ **arm census membership**
     (`lane_a_scene_census._membership_if_answerable`) ⇒ ฉาก 3 เพิ่งมี `population_indices` จริง
  3. ~~🔴 **ฉาก 4,5,6,7,8,9,10,11,130 ถูกกันไว้โดยตั้งใจ** (`LANE_A_CHOOSE_NPC_ROSTER_SKIPPED
     ... reason=columbus_placement_index_collision_needs_runtime_scene_guard`) ... **คลิกบนเก้าฉากนั้นต้องยังเงียบ**
     และนั่นคือตัวควบคุมเชิงลบที่ดีที่สุดของใบนี้ (ขั้น 9)~~
     🔴 **ล้าสมัยตั้งแต่รอบ `gwwpmr` -- แก้รอบ `mcf4qp` (วัดบน `origin/main` แล้ว):** scene guard ของ
     สาขา Columbus ลง `runtime.py` แล้ว ⇒ เก้าฉากนั้น **ลงทะเบียนและตอบคลิกแล้ว**
     (`scenes_this_lane_answers_for()` = `(3, 4, 5, 6, 7, 8, 9, 10, 11, 126, 130)` · `skipped_scenes()` = `()`)
     ⇒ **ห้ามใช้เก้าฉากนั้นเป็นตัวควบคุมเชิงลบอีก** และการตอบของมันเป็นเรื่องของ `GT-212` ไม่ใช่ใบนี้ ·
     ความปลอดภัยของเก้าฉาก **ยืมมาจาก conjunct เดียวใน `runtime.py`** ไม่ใช่การแก้ index space (ดู `GT-212` nonclaims 4)
  4. 🔴 **สิ่งที่จะทำให้เสียรอบถ้าไม่รู้:** วาปข้ามฉากล้าง `last_target_pos = None` และ responder
     ปฏิเสธเมื่อค่านี้เป็น `None` ⇒ **หลังวาปถึง ต้องเดินหนึ่งก้าว (`W`/`S`) ก่อนคลิก** ·
     คลิกก่อนเดิน = เงียบ และนั่นคือ **ความผิดของขั้นตอน ไม่ใช่ผลวัด** ให้เดินแล้วคลิกใหม่
- db: สำเนาใหม่ของ `state\pirateforce.sqlite3` (ห้ามเปิดไฟล์ canonical) · จด sha256 ของสำเนาก่อน/หลัง
  และยืนยัน sha256 ของ canonical ไม่เปลี่ยนทั้งก่อนและหลังรอบ
- server args: บูตปกติ **ไม่มีแฟล็ก scenario** · `-SecondPasswordMode bypass` · บัญชี GM ใน
  `config/gm_accounts.json` · เก็บคอนโซลรวม stdout+stderr (`2>&1`) -- โทเคนของเลนออกทาง stderr
- เส้นทาง: **ใช้เส้นทางวาปของ `GT-192` ห้ามคิดเส้นทางใหม่** (`/warp <scene_id>` เปล่า ไม่ใส่พิกัด)
  🟢 **รันบูตเดียวกับ `GT-192` ได้และควรทำ** (รวม `GT-200` ถ้าหยิบพร้อมกัน) กติกาลำดับข้อเดียว:
  ที่แต่ละฉาก **ถ่ายภาพของใบเหล่านั้นให้เสร็จก่อนคลิกใคร** เพราะคำตอบของใบนี้ส่ง roster ทับของเดิม ·
  🔴 ใบนี้ **ห้ามแก้ `GT-192`/`GT-200`** ไม่ว่าผลจะออกอย่างไร
- steps:
  1. RECHECK ผ่านก่อน · บูตเซิร์ฟเวอร์ใหม่สด (ห้ามใช้ตัวที่เพิ่งมีไคลเอนต์ถูกฆ่าค้าง -- เซสชันจะค้าง
     และไคลเอนต์ตัวถัดไปจะ "connecting" ตลอดกาล) แล้วบูตไคลเอนต์ · ล็อกอิน GM
  2. ~~ตอนบูต ต้องเห็น **หนึ่งบรรทัด** `LANE_HOOK_REGISTERED ...choose_npc_responder:3`
     และ **เก้าบรรทัด** `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED` (ฉาก 4,5,6,7,8,9,10,11,130)~~
     **แก้รอบ `mcf4qp` (ฉบับเก่าเป็นไปไม่ได้แล้ว = `NO-RESULT` แน่นอน):** ตอนบูตต้องเห็น
     `LANE_HOOK_REGISTERED ...lane_a_choose_npc_roster_scenes choose_npc_responder:3`
     **บรรทัดนี้บรรทัดเดียวคือเงื่อนไขหยุดของขั้นนี้** -- ไม่เห็น = บิลด์ผิด **หยุด ไม่ต้องคลิก** ทั้งใบ `NO-RESULT`
     🔴 **สามอย่างนี้ปกติ ห้ามอ่านว่าบิลด์ผิด และห้ามหยุดใบเพราะมัน** (วัดเองรอบ `mcf4qp`):
     (i) โมดูลเดียวกันพิมพ์ `choose_npc_responder:<n>` **หลายบรรทัด** (วันนี้สิบเอ็ด: 3,4,5,6,7,8,9,10,11,126,130)
         จำนวนจะมากขึ้นหรือน้อยลงในอนาคตก็ได้ **ตราบใดที่ฉาก 3 อยู่** -- ใบนี้ตัดสินฉาก 3 ฉากเดียว
     (ii) `LANE_A_CENSUS_SKIPPED scene=1/scene=2 ... reason=reserved_by_a_runtime_branch` -- **คนละโทเคน**
     (iii) `LANE_HOOK_REGISTERED ...lane_a_choose_npc_scene1 choose_npc_responder:1` ตามด้วย
         `LANE_HOOK_DISCOVERY ...lane_a_choose_npc_scene1 SKIPPED_NOT_PRODUCTION_ALLOWED` -- decorator พิมพ์ก่อน
         แล้วถูกถอนทีหลัง ⇒ **ไม่ใช่เกตรั่ว**
     🔴 `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED` **ของฉากอื่นที่ไม่ใช่ 3** (กฎ `no_census_sources_row` / `spliced_source_*`
     ยังมีชีวิต) ⇒ **จดบรรทัดนั้นไว้แล้วเดินต่อ ไม่ใช่เหตุให้หยุด** · เจอบรรทัดที่ `scene=3` เมื่อไหร่ **นั่น**
     คือบิลด์ผิดของใบนี้ ⇒ หยุด `NO-RESULT` (คัดลอก `reason=` มาด้วย)
  3. คลิกช่องแชท **ยืนยัน focus จริง** (พิมพ์ตอนไม่ focus = ฮอตคีย์) · `/warp 3` · Enter · รอ ~3 วิ
     (`/warp` เป็นคำสั่ง GM **ไม่ใช่** ตัวยิงแชท 12 ตัวอักษร -- ห้ามเติมตัวอักษรให้ครบ 12)
  4. **เดินหนึ่งก้าว** `W` หรือ `S` (ก้าวนี้จำเป็น ดู background ข้อ 4)
  5. ภาพนิ่ง **เต็มความละเอียด** ชื่อ `S03-BEFORE` -- ยังไม่คลิกใคร
  6. **คลิกซ้ายหนึ่งครั้ง** บน NPC หนึ่งตัว โดยให้มีตัวอื่นอยู่ในเฟรมอย่างน้อยสองตัว · ภาพนิ่ง
     เต็มความละเอียดชื่อ `S03-AFTER` ภายใน ~3 วินาที
  7. บันทึก: ตัวที่คลิกหันมาหาเราไหม · แผงเป้าหมายเปิดไหมและเขียนว่าอะไร (คัดลอกตรง ๆ **รวมกรณี
     ช่องชื่อว่าง**) · 🔴 **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** เขียน "none"
     ถ้าไม่มี · อ่านสีจากภาพเต็มเท่านั้น (ห้าม contact sheet/ภาพย่อ/วิดีโอ) · **จดสีอย่างเดียว
     ห้ามอนุมานสาเหตุ** (`RE-067`)
  8. ทำซ้ำข้อ 4-7 อีกสองครั้งกับ NPC คนละตัวในฉาก 3 (รวมสามคลิก) เพื่อดูว่าคลิกที่สองและสามยังตอบ
  9. ~~**ตัวควบคุมเชิงลบสองชั้น (ทำทั้งคู่):** (ก) ฉาก 2 -- คลิก NPC หนึ่งครั้ง คาดว่า **เงียบ** ·
     (ข) ฉาก 4 -- `/warp 4` เดินหนึ่งก้าว แล้วคลิก NPC หนึ่งครั้ง คาดว่า **เงียบ** ·
     🔴 ถ้า (ข) ตอบ หรือมีบทสนทนา/เควสต์ใด ๆ โผล่ที่ฉาก 4 = **หยุดทั้งใบทันที รายงานทันที**~~
     🔴 **ตัวควบคุมสองข้อนี้ตายแล้วทั้งคู่ -- วัดบน `origin/main` รอบ `mcf4qp`:** ฉาก 2 มี responder ของตัวเอง
     (`lane_a_choose_npc_scene2` · `production_allowed = True` · ใบของมันคือ `GT-214`) และฉาก 4 อยู่ในสิบเอ็ดฉาก
     ที่ตอบแล้ว (`GT-212`) ⇒ **ทั้งสองฉากตอบคือพฤติกรรมที่ถูกต้องของวันนี้ ไม่ใช่ FAIL และไม่ใช่เหตุให้หยุดใบ**
     🔴 **ใบนี้ไม่มีตัวควบคุมเชิงลบระดับ attended และไม่ต้องมี -- ขั้น 9 ถูกลบทั้งข้อ (รอบ `mcf4qp`)**
     ร่างแรกของรอบนี้ใส่ตัวควบคุมใหม่ไว้ (ไป `/warp 1` พอร์ตรอยัลแล้วดูว่าเงียบ) · **pf-adversary วัดแล้วว่ามันแย่กว่าไม่มี**
     สามเหตุผล ทุกข้อวัดจากซอร์ส ไม่ใช่ความเห็น:
     1. **มันผ่านฟรี** -- `production_allowed = False` ทำให้ `_withdraw()` ลบฉาก 1 ออกจากรีจิสทรี ⇒ จุดเรียกได้ `None`
        ⇒ ทั้ง `LANE_HOOK_FIRED ...scene1` และ `LANE_A_CHOOSE_NPC_SCENE1_ANSWERED` **พิมพ์ไม่ได้ในทุกกรณี**
        และ RECHECK ก่อนบูตก็ยืนยันค่าเดียวกันนี้ไปแล้วจากซอร์สชุดเดียวกับที่เซิร์ฟเวอร์บูต ⇒ ไม่ได้ข้อมูลใหม่แม้แต่บิตเดียว
     2. **ไม่มีอะไรพิสูจน์ว่าคลิกไปถึงสาขา** -- คลิกโดนพื้น/ช่องแชทยังโฟกัส/`chosen_identities` ว่าง ก็เงียบเหมือนกัน
        ⇒ ผู้เทสจด "เงียบ = ผ่าน" ได้ทั้งที่ไม่เคยคลิกถึงอะไรเลย
     3. 🔴 **มันจะฆ่าเกณฑ์ความปลอดภัยของ `GT-212` ในบูตรวมที่ใบนี้เองแนะนำ** -- คลิกโดนโคลัมบัสตัวจริงที่พอร์ตรอยัล
        ทำให้แลตช์ `columbus_quest3021_conversation_sent` ติดทั้งเซสชัน ⇒ เกณฑ์ (ง) ของ `GT-212` และโทเคน (B) ของ
        `GT-213` **ผ่านโดยอัตโนมัติ ต่อให้ scene guard ถูกลบทิ้งไปแล้ว** (กฎเดียวกันนี้เขียนอยู่ในกล่องแดงของ `GT-213`)
     ⇒ **สิ่งที่เกตฉาก 1 ต้องการ พิสูจน์แบบ headless เสร็จแล้ว**: RECHECK ข้อ 3 (`production_allowed` = `False`)
     บวกบรรทัดบูต `LANE_HOOK_DISCOVERY ...lane_a_choose_npc_scene1 SKIPPED_NOT_PRODUCTION_ALLOWED`
     **ไม่ต้องใช้ตาคน ไม่ต้องเสียเวลาผู้เทสสองนาที และไม่ต้องเสี่ยงแลตช์โคลัมบัส**
  10. ตัวเช็ค NO-CRASH: **คลิกขวาลากหมุนกล้อง** เท่านั้น · ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้
  🔴 **ขอบเขต:** คลิกเพื่อ **เลือก** เท่านั้น -- **ห้ามตีมอนสเตอร์ ห้ามใช้สกิล ห้ามคลิกโจมตี** ทุกฉาก
  (`NOW.md`: ใบตีมอนทุกใบรอ P-1 และ P-2 ปิดก่อน) · ถ้าเผลอตี ให้บันทึกไว้ในผล
- pass criteria (สองชั้น แยกเด็ดขาด · ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น):
    wire/DB (headless พิสูจน์ได้ ไม่ต้องมีตาคน · grep คอนโซลรวม `2>&1`):
      (ก) ตอนบูต: บรรทัด `LANE_HOOK_REGISTERED
          pirateforce_foundation.lane_hooks.lane_a_choose_npc_roster_scenes
          choose_npc_responder:3` ~~และเก้าบรรทัด `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED`~~
          **แก้รอบ `mcf4qp`: และ `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED` ต้องไม่มีบรรทัดที่ `scene=3`**
          (วันนี้วัดได้ศูนย์บรรทัดทุกฉาก · บรรทัดของฉากอื่นให้จดแล้วเดินต่อ ดูขั้น 2) ·
          (บรรทัด `LANE_A_CENSUS_SKIPPED` ของฉาก 1/2 เป็นคนละโทเคน ปกติ)
      (ข) ทุกคลิกในฉาก 3: `LANE_HOOK_FIRED ...lane_a_choose_npc_roster_scenes
          scene_choose_npc_responder`
      (ค) ทุกคลิกในฉาก 3: `LANE_A_CHOOSE_NPC_SCENE3_ANSWERED placement=<n> visible=<n> omitted=0`
          **[คำทำนาย ไม่ใช่ผลวัด]** `omitted=0` ทุกครั้ง · `visible` = จำนวน actor ที่สำมะโนขาเข้าส่ง
      (ง) ~~ที่ฉาก 4: **ไม่มี** `LANE_A_CHOOSE_NPC_SCENE4_ANSWERED`~~ **แก้รอบ `mcf4qp`:** ฉาก 4 ตอบแล้ว
          เป็นเรื่องของ `GT-212` ⇒ ข้อนี้เหลือสองท่อนที่ยังจริง: **ตลอดเวลาที่ยืนอยู่ฉาก 3 ต้องไม่มี**
          `core_request_014_columbus_npc_conversation_sent_once` และ **ไม่มี** label
          `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE`
      (ง2) เกตฉาก 1 (แทนตัวควบคุมที่ถูกลบในขั้น 9): ตอนบูตต้องเห็น
          `LANE_HOOK_DISCOVERY ...lane_a_choose_npc_scene1 SKIPPED_NOT_PRODUCTION_ALLOWED`
          🔴 **บรรทัด `LANE_HOOK_REGISTERED ...lane_a_choose_npc_scene1 choose_npc_responder:1` มีอยู่จริง
          และปกติ** -- decorator พิมพ์ตอนลงทะเบียน แล้ว `_withdraw()` ถอนทีหลัง ⇒ **เห็นบรรทัดนี้ไม่ใช่เกตรั่ว
          และไม่ใช่เหตุให้หยุดใบ** (วัดรอบ `mcf4qp`) · ข้อนี้พิสูจน์แบบ headless ล้วน ไม่ต้องคลิกอะไรเลย
          (ชื่อข้อเป็น `ง2` เพราะ `(จ)` ถูกใช้แล้วในชั้น client-observable ข้างล่าง)
      ชั้นนี้พิสูจน์แค่ว่า **เซิร์ฟเวอร์ประกอบและส่งไบต์** ไม่พิสูจน์อะไรที่ผู้เล่นเห็นเลย
    client-observable (ต้องมีคนนั่งหน้าจอ · **ชั้นนี้เท่านั้นที่ตัดสินใบ**):
      (จ) ตัวที่ถูกคลิก **หันมาหาตัวละครเรา** เทียบ `AFTER` กับ `BEFORE`
      (ฉ) แผงชื่อ/HP เปิดขึ้น -- บันทึกสิ่งที่แสดงตรง ๆ · **ช่องชื่อว่างเป็นการบันทึก ไม่ใช่ FAIL อัตโนมัติ**
          (`GT-030-R3` เคยวัดได้แบบนั้นกับ actor type 4)
      (ช) actor ตัวอื่นในเฟรมเหมือนเดิมทุกตัว: อยู่ครบ · หน้าตาเดิม · ป้าย `LV` ไม่หายและไม่กลายเป็น `1` ·
          ไม่มีใครกลายเป็นคนอื่น
      ~~(ซ) ที่ฉาก 4 ไม่มีอะไรเกิดขึ้นบนจอเลยตอนคลิก~~ **ตายไปกับตัวควบคุมเก่า (รอบ `mcf4qp`) และไม่มีข้อแทน**
          -- ใบนี้ไม่มีตัวควบคุมเชิงลบระดับ attended อีกแล้ว (เหตุผลสามข้อในขั้น 9) · ชั้นนี้ตัดสินฉาก 3 อย่างเดียว
      **ผลลบมีค่าเท่าผลบวก** -- ดู FAIL branch
- FAIL branch:
  - พิมพ์ `..._ANSWERED` ครบแต่ **จอไม่ขยับเลย** ⇒ คำตอบที่ใบนี้มีไว้ตัดสิน: **เซิร์ฟเวอร์ตอบแล้ว
    ไคลเอนต์ไม่วาด** ⇒ ไม่ใช่ความผิดของ lane hook และ **ห้ามถอน `production_allowed` ด้วยเหตุนี้** ·
    ให้เปิดใบ `RE-` ใหม่เรื่องเส้นทางเรนเดอร์คำตอบ ChooseNPC พร้อมภาพและเลข `visible=`
  - มี `LANE_HOOK_FIRED` แต่ไม่มี `..._ANSWERED` ⇒ responder ปฏิเสธ · เช็คก่อนว่าเดินหนึ่งก้าวจริง
    (ข้อ 4) · ถ้าเดินแล้วยังไม่มี = finding จริงเรื่อง membership/identity
  - ไม่มี `LANE_HOOK_FIRED` ตอนคลิก ⇒ คลิกไม่ถึงสาขานี้ = `NO-RESULT`
  - ~~ฉาก 4 ตอบ หรือมีเควสต์โผล่ ⇒ **หยุดทั้งใบ** รายงานทันที (ดู steps ข้อ 9ข)~~
    🔴 **ยกเลิกในรอบ `mcf4qp`: ฉาก 4 ตอบคือของถูกต้องวันนี้** (`GT-212`) · เหตุให้หยุดใบเหลือข้อเดียว:
    **เควสต์/บทสนทนาโผล่ขณะยืนอยู่ฉาก 3** (หรือรู้ตัวว่าอยู่คนละแมพหลังคลิกที่ฉาก 3)
- nonclaims:
  1. ไม่พิสูจน์ว่าสำมะโนขาเข้าถูก/ครบ -- `GT-192` (ห้ามแก้) · ไม่พิสูจน์กลไก `/warp` เอง
  2. ไม่พิสูจน์ว่าเลข `LV` ถูก -- `GT-200` (ห้ามแก้) · ใบนี้ดูแค่ว่า **ป้ายไม่หาย** หลังคลิก
  3. ไม่พูดเรื่องความหมายของสีป้าย -- `RE-067`/P-2 ยังเปิด · จดสีอย่างเดียว
  4. ~~ไม่พิสูจน์อะไรของฉาก 2 หรือฉาก 4 นอกจากความเงียบ (ตัวควบคุม)~~ **แก้รอบ `mcf4qp`:** ไม่ตัดสินฉาก 2
     (`GT-214`) ฉาก 4 และอีกแปดเกาะ (`GT-212`) ฉาก 14 (`GT-134`) หรือฉาก 126 (`GT-217`) ·
     ที่ฉาก 1 ตัดสินอย่างเดียวคือ **เกต `production_allowed` ยังกันจริงที่ชั้นคอนโซล** ไม่ตัดสินสิ่งที่จอวาด
  5. ~~**ผลของใบนี้ไม่ใช่ใบอนุญาตให้เปิดเก้าฉากที่ถูกกัน** -- ประตูนั้นเปิดได้ก็ต่อเมื่อ `runtime.py`
     มี scene guard บนสาขา Columbus แล้วเท่านั้น (CORE-REQUEST ของรอบ `326kf4` ถึง chief)~~
     **เกิดขึ้นแล้วในรอบ `gwwpmr`: scene guard ลง `runtime.py` และเก้าฉากเปิดไปแล้ว** ⇒ ข้อนี้เป็นประวัติ
     ไม่ใช่เงื่อนไขที่ยังบังคับ · สิ่งที่ยังจริง: ใบนี้ไม่ได้พิสูจน์ว่า index space เป็น scene-aware แล้ว **ไม่ใช่**
  6. ไม่พิสูจน์คอมแบต/aggro/HP ใด ๆ · ไม่พิสูจน์ว่าพื้นที่ยืนของ placement ดี
  7. ไม่พิสูจน์ว่าอะไรรอดข้าม relog · ความต่างจากเซิร์ฟเวอร์จริงลง `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
- RECHECK ~~(ต้องได้ hit จริงทั้งสองบรรทัด · `grep -n "_columbus_collision_scenes"`)~~
  **เขียนใหม่รอบ `mcf4qp`** (ตัดสินด้วยเนื้อโค้ด ห้ามเทียบเลข commit · ข้อเก่าข้อที่สองปักฟังก์ชันที่
  **ยังอยู่แต่กฎ skip ของมันถูกขีดฆ่าไปแล้ว** ⇒ hit ของมันไม่ได้แปลว่าอะไรอีก) -- ต้องผ่านครบสามข้อ:
  🔴 **หนึ่งบรรทัด = หนึ่งคำสั่ง · ไม่มี `&&` และไม่มีวงเล็บ (PS 5.1 ไม่รับ `&&` และ `( )` ไม่ใช่ subshell บน Windows)**
  · รันจากโฟลเดอร์แม่ที่มี `pirate-force-server` อยู่ข้างใน · พาธมีช่องว่างให้ครอบด้วยเครื่องหมายคำพูด
  ```
  git -C pirate-force-server fetch origin
  git -C pirate-force-server show origin/main:src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_roster_scenes.py | findstr /C:"production_allowed = True"
  py -3 -c "import sys; sys.path.insert(0, r'pirate-force-server\src'); from pirateforce_foundation.lane_hooks import lane_a_choose_npc_roster_scenes as m; print(m.scenes_this_lane_answers_for()); print(m.skipped_scenes())"
  py -3 -c "import sys; sys.path.insert(0, r'pirate-force-server\src'); from pirateforce_foundation.lane_hooks import lane_a_choose_npc_scene1 as m; print('scene1 production_allowed =', m.production_allowed)"
  ```
  ข้อ 1 ต้องเจอจริง · ข้อ 2 ต้องมี **ฉาก 3** อยู่ในรายการ และ `skipped_scenes()` = `()` (วัดรอบ `mcf4qp`:
  `(3, 4, 5, 6, 7, 8, 9, 10, 11, 126, 130)`) · ข้อ 3 ต้องพิมพ์ **`False`**
  (อ่าน **บรรทัดสุดท้าย** -- ก่อนหน้ามีบรรทัด `LANE_HOOK_REGISTERED`/`LANE_A_CENSUS_SKIPPED` ของ import ตามปกติ)
  -- ถ้าเป็น `True` แปลว่ามีคนพลิกเกตฉาก 1
  ⇒ **มีคนพลิกเกตฉาก 1 โดยไม่ได้บอก** ⇒ เขียนลงผลหนึ่งบรรทัดแล้วเดินต่อ (เกณฑ์ (ง2) เป็นการบันทึก ไม่ใช่เงื่อนไขหยุดของใบนี้)
  🔴 คำสั่งที่ไม่เจอ **ไม่พิมพ์ `0`** มันไม่พิมพ์อะไรเลย ⇒ "ไม่มีบรรทัดออกมา" = ไม่ผ่าน
- links: `lane_hooks/lane_a_choose_npc_roster_scenes.py` · `lane_hooks/lane_a_scene_census.py`
  (`_membership_if_answerable`) · `lane_hooks/lane_a_choose_npc_scene14.py` · `GT-192` (เส้นทางวาป) ·
  `GT-200` (ป้าย LV) · `GT-134` (ฉาก 14) · `RE-067` (สีป้าย)
- result: (ผู้เทสกรอก: PASS/FAIL/NO-RESULT · ภาพ `S03-BEFORE`/`S03-AFTER` (สามคลิก) ·
  บรรทัดสีป้ายครบ · บรรทัดคอนโซลสี่ชนิด · ~~ผลตัวควบคุมฉาก 2 และฉาก 4~~ **(ตัวควบคุมถูกลบรอบ `mcf4qp`
  -- แทนด้วยบรรทัดบูตของเกณฑ์ (ง2) ซึ่งคัดลอกมาแปะได้เลย)** · timestamp +07:00 ·
  `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: LANE-A (WORLD) รอบ `326kf4` 2026-09-02T12:2x+07:00 -- LANE-A บริโภคผลใบนี้เอง**

## GT-211 UI-B-EXIT-BUTTON-VISIBLE-NOTICE-001  [✅ **PASS สองชั้น · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — R306: `EXIT REFUSED` ขึ้นวินาทีเดียวกับคลิก เฟรม 66 ไบต์ ⇒ **ชั้นตอบผู้เล่นเสร็จ** · 🔴 **ปุ่มยังไม่ล็อกเอาต์จริง** ใบนี้ไม่เคยอ้างข้อนั้น (`NOW.md` UI-B ยังค้าง) · ป้าย `BACK_REFUSED`→`EXIT` ที่ `COO 20260903_1746` ข้อ 2 สั่ง: เปลี่ยนแล้วต้องแก้สตริงในเกณฑ์ใบนี้รอบเดียวกัน · สถานะเดิม: 🟢 READY -- RECHECK ผ่านครบสองข้อ วัดเองบน `origin/main` `106b4df` โดย LANE-A รอบ `4uztfj` 2026-09-02T19:35+07:00: `world_logout_button_notice.py` บน main มี `EXIT REFUSED` 7 จุด (บรรทัด 62/123/229/265/311/320/325) · `pytest tests/test_world_logout_button_notice.py tests/test_world_logout_button_notice_wiring.py` = **53 passed, 19 subtests** · ป้ายเดิมอ้าง branch `claude/dazzling-volta-1d6rta` ซึ่ง merge ไปแล้วที่ `#577` — ~~[BLOCKED -- โค้ดยังไม่ขึ้น main]~~ ตาม COO-DECISION 20260902_1850]

> เปิดโดย LANE-A (WORLD) รอบ `1d6rta` 2026-09-02T13:4x+07:00 · **LANE-A บริโภคผลเอง**
> numbering: shared counter กับ `CLIENT_RE_QUEUE.md` (กฎ ② หัวไฟล์) -- **ให้รันคำสั่งค้นหาซ้ำตอน rebase**
> ณ วันเปิดใบ: highest `GT` บน `main` = `GT-210`; highest `RE` = `RE-210` (เปิดรอบเดียวกัน) ⇒ ใบนี้ `211`
> บูต/DB/teardown ตาม `ATTENDED_SESSION_RUNBOOK.md` (teardown ปฏิเสธ boot stamp เก่ากว่า 420 นาที
> -- ต้องรัน teardown เสมอ แม้รอบจบเพราะเจ้าของเลิกเล่นเฉย ๆ)

- objective: ข้อพิสูจน์เดียว ตัดสินด้วยตาคนเท่านั้น -- ตัวละครยืนอยู่ในแมพจริงบนบูต **ปกติ ไม่มีแฟล็ก
  scenario ใด ๆ ทั้งสิ้น และโดยเฉพาะไม่ใช่ logout scenario** · ผู้เล่นเปิดเมนู HOME แล้วคลิกปุ่ม
  "ออกจากเกม" (exit game) แล้วบรรทัดเดียว `EXIT REFUSED` -- ตัวอักษร ASCII พิมพ์ได้ **12 ตัวพอดี** --
  **ขึ้นบนจอ** ในพื้นที่แชท/ช่องพูดฝั่งเรา ไม่ว่าจะระหว่างที่ dialog logout ยังค้างอยู่ หรือหลังมันปิดไป
- background (อ่านครั้งเดียวแล้วทำตาม steps):
  1. รอบ `od1xso` สร้าง `src/pirateforce_foundation/world_logout_button_notice.py` ซึ่งตอบ **เฉพาะ**
     ปุ่ม UI-A ("กลับหน้าเลือกตัวละคร", subcode 3) ด้วย `BACK REFUSED` -- นั่นคือ `GT-205`
     **ยังมีชีวิตอยู่และใบนี้ไม่แตะ**
  2. รอบ `1d6rta` (รอบนี้) ต่อยอดโมดูลเดิมให้ตอบปุ่ม UI-B ("ออกจากเกม", `LogoutVital 0x1B40`
     subcode 1, เฟรมจับสดของเจ้าของเอง 119 ไบต์ ห่อ vital มาสี่ตัว) ด้วยประโยค 12 ตัวอักษรของตัวเอง
     `EXIT REFUSED` ประกอบผ่าน `gm/say_wire.make_local_talk_notice_frame` -- **byte-equal** กับ composer
     ที่พิสูจน์แล้ว ไม่มีความรู้เรื่องสายเป็นของตัวเอง
  3. **ไม่ต้อง wire อะไรใหม่** -- call site `0x1B40` เดิมใน `runtime.py` (รอบ `od1xso` บรรทัดของ chief)
     ส่งสิ่งที่ `observe_parsed` คืนมา ไม่ว่าจะปุ่มไหน
  4. คำว่า `EXIT REFUSED` เป็น **[ข้อสมมติของเลน A -- รอ COO ยืนยัน]** จดหมาย
     `notes_to_chief/20260902_1341_LANE-A-ASK-COO-uib-notice-wording.md` ⇒ ผู้เทสที่อ่านสะกดคำอื่นบนจอ
     ให้ **จดตามที่เห็นเป๊ะ ๆ** อย่าเพิ่งตัดสินว่าเป็นข้อบกพร่อง
  5. ~~🔴 **ไม่เคยมีใครเห็นบรรทัดที่เซิร์ฟเวอร์ประกอบเองบนช่องนี้ขึ้นจอบนบูตปกติมาก่อนเลย**
     (`gm/say_wire.py` เขียนไว้เป็นตัวใหญ่)~~ **หมดอายุแล้ว — แก้โดย LANE-A (เจ้าของใบ) รอบ `kozzu1`
     2026-09-03T11:5x+07:00**: `GT-205` รันไปแล้ว R303 2026-09-02 และ **บรรทัด `BACK REFUSED` ขึ้นจอจริง**
     บนบูตที่พิสูจน์ได้ว่า**ไม่มี scenario ล็อกเอาต์** (เกตของ `runtime.py` ยอมประกอบเฉพาะตอน
     `logout_hypothesis_scenario is None`) · 🔴 **แต่ไม่ได้แปลว่าใบนี้ตอบไปแล้ว**: `GT-205` เป็น **subcode 3**
     ปุ่มคนละปุ่มกับใบนี้ (**subcode 1**) และ argv ของบูตนั้นไม่มีใครบันทึก ⇒ "บูตไร้แฟล็ก" **ยังไม่ถูกวัด**
     ของที่ขึ้นจอใน `GT-006`/`GT-009` คือข้อความที่ไคลเอนต์
     **สะท้อนของตัวเอง** หลังแฟล็ก scenario และตอน dialog logout ปิดอยู่ ⇒ **ผลลบของใบนี้มีค่าเท่าผลบวก**
     (ประโยคนี้ **ไม่ถูกขีดฆ่า** และสำคัญขึ้นหลัง `GT-205` ไม่ใช่น้อยลง)
     🔴 **ผลลบของใบนี้ตอนนี้เป็น finding เรื่อง subcode 1 / dialog ออกจากเกม ไม่ใช่เรื่องช่องแชตอีกแล้ว**
     เพราะช่องนี้พิสูจน์แล้วว่าเรนเดอร์ได้ · ไม่ใช่หลักฐานว่า composer ผิด
     🔴 **ห้ามจดผล `EXIT REFUSED` ว่าเป็น "บรรทัดแรกในประวัติโปรเจกต์"** — บรรทัดแรกคือ `GT-205` เมื่อ 2 ก.ย.
  6. ความยาว 12 ตัวอักษรคือความยาวเดียวที่เคยเห็นเรนเดอร์ (`GT-006`/`GT-009`: `PFCHATPROBE1`) ·
     body ห้าตัวอักษร **วัดแล้วว่าเงียบ**
- PRECONDITION / RECHECK (ใบนี้เริ่มที่ `BLOCKED` · **RECHECK ผ่านเท่านั้นจึงเลื่อนเป็น `READY`**) --
  คำสั่งล็อก cwd ในตัวเอง ไม่พึ่ง cwd ผู้รัน:
  ```
  (cd pirate-force-server && git fetch origin && git show origin/main:src/pirateforce_foundation/world_logout_button_notice.py | grep -n "EXIT REFUSED")
  (cd pirate-force-server && python3 -m pytest tests/test_world_logout_button_notice.py tests/test_world_logout_button_notice_wiring.py -q)
  ```
  ข้อ 1 ต้อง **เจอจริง** · ข้อ 2 ต้อง **เขียวทั้งชุด** บน clone เดียวกันนั้น ·
  **ผลว่างจากข้อ 1 = ยังไม่ merge ⇒ ไม่บูต ไม่เสียเวลาผู้เทสแม้แต่นาทีเดียว** คงสถานะ `BLOCKED`
  ทดสอบบน branch ก่อน merge ได้ ถ้าเปลี่ยน `origin/main` เป็น `origin/claude/dazzling-volta-1d6rta`
  แล้ว **เขียนในผลว่าใช้ตัวไหน และ commit ไหน**
- db: `state\pirateforce.sqlite3` -- **สำเนาเท่านั้น ห้ามเปิดไฟล์ canonical** · คัดลอกเป็น
  `state\run_gt211_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา · จด sha256 ของสำเนา ก่อน/หลัง ·
  จด sha256 ของ canonical ก่อน/หลัง และยืนยันว่า **ไม่เปลี่ยน** · `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง
  (รอบคัดลอก DB ⇒ ตำแหน่งตัวละครกลับไป spawn ทุกบูต เป็นเรื่องปกติ ไม่ใช่ผลวัด)
- server args: บูตมาตรฐานตาม `BRIDGE_BOOT_PROCEDURE.md` · `-SecondPasswordMode bypass` ·
  🔴 **ไม่มีแฟล็ก scenario ใด ๆ และห้ามเป็น logout scenario เด็ดขาด** · เก็บคอนโซลรวม stdout+stderr (`2>&1`)
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt211_<stamp>.sqlite3
  ```
- steps: (ราว 10 นาทีหน้าจอ · เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ)
  1. RECHECK ผ่านก่อน · LOCK_GAME · จด boot stamp · sha canonical · คัดลอก DB
  2. บูตเซิร์ฟเวอร์ **ใหม่สด** แล้วค่อยบูตไคลเอนต์ (เคยมีไคลเอนต์ถูกฆ่า = เซิร์ฟเวอร์ยังถือเซสชันไว้
     ไคลเอนต์ตัวถัดไปจะ "connecting" ค้างตลอดกาล ⇒ **รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ**) ·
     ห้ามบูตไคลเอนต์ทิ้งไว้โดยไม่มีเซิร์ฟเวอร์ (ตายใน ~3.5 นาที)
  3. **ล็อกอินเข้าฉากจริงให้เสร็จก่อนทุกอย่าง** (มีเกต fail-closed เมื่อยังไม่ได้เลือกตัวละคร)
  4. จัดมุมภาพด้วย **คลิกขวาลาก** เท่านั้น (กล้องอย่างเดียว facing ไม่ขยับ ไม่มีไบต์ออกสาย) ·
     🔴 **ห้ามเปลี่ยน facing ของตัวละคร**: ห้าม `Q`/`E` ห้าม `W/A/S/D` (ทั้งคู่ยิง TargetPosVital) ·
     **ห้ามพิมพ์ตัวอักษรใด ๆ** ตอนช่องแชทไม่ focus (ทุกปุ่มกลายเป็นฮอตคีย์)
  5. ภาพนิ่ง `S0-BASELINE` **เต็มความละเอียด** เห็นพื้นที่แชท/ช่องพูด · จดเวลานาฬิกา (+07:00) และ `t` ของวิดีโอ
  6. เปิดเมนู HOME · ภาพนิ่ง `S1` (เมนูเปิด)
  7. คลิก "ออกจากเกม" **หนึ่งครั้ง** · จดเวลานาฬิกาและ `t` ของคลิกนั้น **ก่อนทำอย่างอื่น**
  8. **จ้องจออย่างน้อย 30 วินาที** · `S2` ที่ ~+2s · `S3` ที่ +10s · `S4` ที่ +30s (เต็มความละเอียดทุกใบ
     เห็นพื้นที่แชท) · ห้ามคลิกอะไร ห้ามปิด dialog เอง ระหว่าง 30 วินาทีนั้น เว้นแต่ไคลเอนต์ปิดเอง
  9. บันทึกในผล: เห็น 12 ตัวอักษรไหม yes/no · **ตรงไหนบนจอ** (แผง/บรรทัดใด) · ห่างจากคลิกกี่วินาที ·
     อยู่นานเท่าไร · และตอนนั้น **dialog logout ยังเปิดอยู่หรือปิดไปแล้ว**
  10. ทำซ้ำได้อีกครั้งเดียว **เฉพาะเมื่อครั้งแรกไม่เห็นอะไร**: relog แล้วทำข้อ 6-9 ใหม่โดย
      **เปิดหน้าต่าง/แท็บแชทค้างไว้ให้เห็นประวัติก่อนคลิก** · ตั้งชื่อ `S0b..S4b` และ
      **บันทึกสองครั้งแยกกัน ห้ามรวม**
  11. ตัวเช็ค NO-CRASH: **คลิกขวาลากหมุนกล้อง** เท่านั้น (ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้) · `S5` · ปิดด้วยปุ่ม X
  12. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err`, `capture_v141\GAME_LIVE.txt`,
      `capture_v141\GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · เช็ค sha canonical ซ้ำ ·
      **รัน teardown เสมอ**
- pass criteria (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**):
    wire/DB (อ่านจากคอนโซล/แคปเจอร์อย่างเดียว ไม่ต้องมีตาคน): คลิกนั้นต้องพิมพ์ **บรรทัดเดียว**
      `LANE_A_UIA_NOTICE_COMPOSED button=EXIT_GAME subcode=1 vitals=4 trailing=85 text=EXIT REFUSED pc=56 frame=66`
      (`pc=`/`frame=` คือความยาวไบต์ที่ประกอบได้ ⇒ โทเคนนี้ปรากฏไม่ได้ถ้าไม่มีไบต์จริง ·
      ชื่อโทเคนขึ้นต้น `UIA` ตามโมดูลเดิม **ไม่ใช่ความผิดพลาด** ให้ดูที่ `button=`) ·
      🔴 **บรรทัดนี้คือที่เดียวในแคปเจอร์ที่แยกสองปุ่มออกจากกันได้ — อย่าใช้บรรทัด `SENT` แทน**
      (pf-adversary D1 วัดแล้ว): ตัวส่งของ v141 เขียน **label** ลง ~~`GAME_LIVE.txt` / `[G>]` / ไฟล์
      events~~ **แก้ตามที่วัดใหม่ รอบ `omhpqj`: `GAME_LIVE.txt` (`SENT label=`) · คอนโซล `[G>]` · และ log ดิบ
      ต่อเซสชัน — ไม่ใช่ `GAME_EVENTS_LIVE.txt`** (ไฟล์นั้นเขียนโดย `event()` `v141:7378` เท่านั้น ซึ่งมีแต่
      `SESSION_START` กับ `MILESTONE` ⇒ 🔴 **ห้าม grep หา label หรือชื่อ event ใน `GAME_EVENTS_LIVE.txt` จะได้ศูนย์เสมอ
      และไม่ใช่ FAIL**) และ ~~label ของทั้งสองปุ่มยังเป็น `LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE` เหมือนกัน~~
      **แก้ครึ่งเดียว รอบ `omhpqj` 2026-09-03T18:5x+07:00 (LANE-A · COO-DECISION `20260903_1746` ข้อ 2)**:
      ตอนนี้ label มีได้ **สองค่า** ให้ผู้เทส **คัดลอกค่าที่เห็นจริง ห้ามแก้ให้ตรงใบ** และทั้งสองค่าถูกต้องทั้งคู่ —
      `LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE` (ค่าเดิม แปลว่าบรรทัดหนึ่งบรรทัดใน `runtime.py` ของ chief
      ยังไม่ถูกสลับ) หรือ `LANE_A_UIB_EXIT_REFUSED_LOCAL_TALK_NOTICE` (แปลว่าสลับแล้ว ⇒ ตั้งแต่บูตนั้นเป็นต้นไป
      บรรทัด `SENT` แยกสองปุ่มออกจากกันได้เอง) ·
      🔴🆕 **อัปเดตรอบ `oi2r2n`/R340 (chief) — โลกที่สองมาถึงแล้ว อ่านก่อนบันทึกผล**: chief สลับบรรทัดนั้นแล้ว
      (`uia_notice.action_label` แทนสตริงตายตัว · `CORE-REQUEST 20260904_1524`) และ **PR เซิร์ฟเวอร์ของรอบ `oi2r2n`
      ยังรอเกต/ยังไม่ merge ตอนเขียนบรรทัดนี้** ⇒ ผู้เทสต้องตัดสินจาก commit ที่บูตจริง ไม่ใช่จากบรรทัดนี้:
      🔴 **บูตบน commit ที่มีการสลับแล้ว: คลิกปุ่ม "ออกจากเกม" ต้องได้ `LANE_A_UIB_EXIT_REFUSED_LOCAL_TALK_NOTICE`**
      — ได้ค่าเดิมแทน = **finding ต้องรายงาน ไม่ใช่ "chief ยังไม่สลับ"** ·
      🔴 **ป้ายของปุ่ม UI-A ยังเป็น `LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE` ตลอดไปทั้งสองโลก** (มันคือค่าของแถว
      `UIA_ACTION_LABEL` เอง) ⇒ **การเห็นสตริงนั้นจากคลิกปุ่ม "กลับ" ไม่ได้แปลว่ายังไม่สลับ** —
      ประโยคก่อนหน้าอ่านผิดได้ตรงนี้ (pf-adversary รอบ `oi2r2n` D5 วัดว่าจะทำให้ผู้เทสบันทึก false negative
      ถ้าคลิกสองปุ่มในเซสชันเดียวตาม nonclaim ② ของใบนี้) · ตัวชี้ขาดคือ **ปุ่มออกจากเกม** ปุ่มเดียว · ป้ายของปุ่ม UI-A **ไม่เปลี่ยนทั้งสองโลก** เพราะคำสั่งของ COO
      ระบุปุ่มเดียว (ไม่ใช่เพราะ `GT-205` grep ค่านั้น — **วัดแล้วว่าใบ `GT-205` ไม่มีสตริงนี้เลยสักที่**
      สิ่งที่ใบนั้น grep คือ `LANE_A_UIA_NOTICE_COMPOSED` กับ `BACK REFUSED` ซึ่งรอบนี้ไม่แตะ) ·
      ตาราง `ACTION_LABEL_BY_BUTTON` อยู่ใน
      `src/pirateforce_foundation/world_logout_button_notice.py` · คำขอสลับ = `CORE-REQUEST 20260903_1832`
      🔴 **ตราบใดที่ยังเห็นค่าเดิม ข้อความข้างล่างนี้ยังยืน**: ประโยคทั้งสองยาว 12 ตัวเท่ากัน ⇒
      `SENT ... frame_bytes=66` ของสองคลิก **เหมือนกันทุกไบต์**
      (`runtime.py` เป็นไฟล์ของ chief · คำขอเปลี่ยนชื่อใบแรกอยู่ในจดหมาย `20260902_1341_LANE-A-TO-CHIEF-*`
      · ไบต์ที่ผู้เล่นได้ถูกต้องทั้งสองปุ่มอยู่แล้ว ไม่ใช่บั๊กของไบต์) ·
      **ผู้เทสคัดลอกบรรทัดดิบ ๆ ห้ามตีความ** · เลข `vitals=`/`trailing=` บอกสิ่งที่ไคลเอนต์ห่อมารอบคลิก
      และ **ต่างจาก 4/85 ได้โดยชอบธรรมในเซสชันอื่น -- ให้คัดลอกเลขที่เห็นจริง ห้ามนับความต่างเป็น FAIL** ·
      สิ่งที่ตัดเกรดมีแค่ โทเคน · `button=EXIT_GAME` · `subcode=1` · และช่อง `text=`
      โทเคนอื่นที่อาจขึ้นแทน และความหมายของแต่ละตัว:
      `LANE_A_UIA_STOOD_DOWN` (เลนนี้ไม่มีประโยคให้ปุ่มนั้น -- **รายงานทันที** เพราะกับ subcode 1
      ตอนนี้ไม่ควรเป็นไปได้แล้ว) · `LANE_A_UIA_WITHDRAWN` (โมดูลถูกปิดสวิตช์) ·
      `LANE_A_UIA_NOTICE_FAILED` (composer ปฏิเสธ -- เป็นบั๊กให้รายงาน ไม่ใช่ความผิดผู้เทส) ·
      `LANE_A_LOGOUT_FRAME_UNCLASSIFIED verdict=<word>` (เฟรมถึงเลนแล้วถูกปฏิเสธ · คำนั้นคือคำตัดสิน
      ของ classifier ตัวจริง) · `LANE_A_UIA_NOTICE_NOT_THIS_BOOT` (โหลด logout scenario มา = **บูตผิดใบ**
      ให้รีบูตแบบไม่มีแฟล็ก) · และ `integrity_check` = `ok` · sha canonical ไม่เปลี่ยน · ไม่มี traceback หลุด
      **ชั้นนี้ตอบไม่ได้เลยว่ามีอะไรถูกวาดบนจอ**
    client-observable (ต้องมีคนนั่งหน้าจอ · **ห้ามอนุมานจากคอนโซล**): ภายใน 30 วินาทีหลังคลิก มนุษย์
      **เห็น** บรรทัด `EXIT REFUSED` -- 12 ตัวอักษร ASCII สะกดตามนั้น -- ในพื้นที่แชท/ช่องพูดฝั่งเรา ·
      เทียบ `S0` กับ `S2`/`S3`/`S4` ตามแบบของบ้านนี้ ·
      🔴 บันทึก **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** สำหรับ `S0`-`S5`
      (และ `S0b`-`S4b` ถ้าทำรอบสอง) เขียนคำว่า `none` ออกมาแทนการเว้นว่าง ·
      อ่านสีจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น** ห้าม contact sheet / ภาพย่อ / วิดีโอ ·
      **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (สิ่งที่ตัดสินสีป้ายยังไม่มีใครรู้ = ตัว `RE-067` ทั้งใบ) ·
      ความต่างจากภาพเซิร์ฟเวอร์จริงลง `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      **ชั้นนี้ตอบไม่ได้เลยว่าประกอบไบต์อะไร หรือ subcode ไหนมาถึง**
- prediction (**นี่คือคำทำนาย ไม่ใช่ผลวัด** · ทำนายผิด = finding ไม่ใช่ความล้มเหลว):
    P1 มีโทเคน **และ** เห็น `EXIT REFUSED` ใน ~2 วิ ⇒ ผ่านทั้งสองชั้น
    P2 มีโทเคน แต่ 30 วินาทีแล้วไม่เห็นอะไร ⇒ ช่องนี้ไม่เรนเดอร์ขณะ dialog logout ถือ input/render state อยู่
       -- เป็น finding จริงเรื่อง dialog **ไม่ใช่หลักฐานว่า composer ผิด** ⇒ เปิดใบ `RE-` เรื่อง render state
       ของ dialog **ห้ามรันซ้ำมั่ว ๆ**
    P3 ไม่มีโทเคนเลย ⇒ คลิกไม่ถึง call site นี้ · รัน RECHECK ใหม่และรายงานว่าบูต commit ไหน ⇒
       ชั้นจอเป็น `NO-RESULT` ไม่ใช่ FAIL
- nonclaims:
  1. **ใบนี้ไม่ทำให้ผู้เล่นออกจากเกม** · `NOW.md` ข้อ UI-B ขอปุ่ม logout ที่ออกได้จริง (ไม่ใช่ปิดหน้าต่างด้วย X)
     ใบนี้ตัดสิน **เฉพาะว่าบรรทัดปฏิเสธขึ้นจอไหม** เท่านั้น · `GT-033` วัดรูปแบบคำตอบทั้งสองแบบที่โปรเจกต์นี้มี
     แล้วไคลเอนต์จริงยังอยู่แมพเดิม 50-77 วิ ตลอดสามรอบที่มีคนนั่งดู · `RE-189` พบว่าฟิลด์ที่เกต transition
     ของไคลเอนต์ต้องใช้ ถูกเขียนโดย local UI binding เท่านั้น
  2. ไม่ทดสอบปุ่ม UI-A (นั่นคือ `GT-205`) -- แต่ถ้าเธอกดทั้งสองปุ่มในเซสชันเดียว **ต้องขึ้นทั้งสองบรรทัด
     และต้องคัดลอกทั้งสองบรรทัด**
  3. ไม่แตะ `GT-194`: ใบนั้นบูต logout scenario ซึ่งใบนี้ **ประกอบอะไรไม่ได้เลยโดยโครงสร้าง**
     (ตรึงไว้ด้วย `tests/test_world_logout_button_notice_wiring.py::...test_a_scenario_boot_composes_nothing_for_the_uib_click`)
     ⇒ 🔴 **บูตใบนี้ด้วย logout scenario คือวิธีเดียวที่ทำให้ทั้งสองใบไร้ความหมายพร้อมกัน**
  4. ไม่อ้างว่า 12 ตัวอักษรนั้นเรนเดอร์ **ขณะ dialog logout เปิดอยู่** -- นั่นคือสิ่งที่ยังไม่รู้ และเป็นเหตุผล
     ที่ต้องจดว่าตอนเห็น dialog เปิดหรือปิด
- links: `NOW.md` queue item UI-B · `COO-DECISION 20260902_1145` ·
  `notes_to_chief/20260902_1341_LANE-A-ASK-COO-uib-notice-wording.md` · `GT-205` · `GT-194` · `GT-033` ·
  `RE-189` · `RE-210` (เปิดรอบเดียวกัน: vital `0x1EB4` คืออะไร) ·
  `FINDINGS_A_1d6rta_UI_B_LOGOUT_BUTTON_FRAME_EVIDENCE.md` (ไบต์จับสด 119 ไบต์ เทียบกับ pin) ·
  `notes_to_chief/consumed/20260901_1930_KA1A-CAPTURE-*.md` (ที่มาของไบต์) ·
  `rounds/A_20260902_1341_1d6rta_uib-exit-button-answers-on-screen.md` ·
  `src/pirateforce_foundation/world_logout_button_notice.py` · `src/pirateforce_foundation/gm/say_wire.py`
- result: (ผู้เทสกรอกตาม G-OBS: PASS/FAIL/BLOCKED/NO-RESULT · ภาพ `S0`-`S5` (+ `S0b`-`S4b` ถ้ามีรอบสอง) ·
  บรรทัดคอนโซลดิบทุกบรรทัด · บรรทัดสีป้ายครบทุกป้ายทุกภาพ · dialog เปิด/ปิดตอนเห็น · sha256 ทั้งสี่ค่า ·
  branch/commit ที่บูต · timestamp +07:00 · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: LANE-A (WORLD) รอบ `1d6rta` 2026-09-02T13:4x+07:00 -- LANE-A บริโภคผลใบนี้เอง**

## GT-212 CHOOSE-NPC-NINE-ROSTER-ISLANDS-CLICK-ANSWER-001  [✅ **PASS · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — R306 บนจอเจ้าของ (`notes_to_chief/20260903_1657_*`) · 🔴 เกณฑ์ (ก)/(ง2) วัดไม่ได้ด้วยเหตุเดียวกับ `GT-210` (`1743` ข้อ 3 ข้อย่อย 5) · สถานะเดิม: 🟢 READY -- RECHECK ผ่านครบสามข้อ **วัดเองโดย LANE-A (เจ้าของใบ) รอบ `mcf4qp` 2026-09-03T08:3x+07:00** บน `origin/main` (สะพาน `d1c7eed` · เซิร์ฟเวอร์ `f240ab4`): ข้อ 1 `production_allowed = True` เจอจริง (บรรทัด 329) · ข้อ 2 พิมพ์ `(3, 4, 5, 6, 7, 8, 9, 10, 11, 126, 130)` + `skipped = ()` · ข้อ 3 `97 passed, 258 subtests` · ~~[BLOCKED -- โค้ดยังไม่ขึ้น `main`: อยู่บน branch `claude/laughing-archimedes-gwwpmr` เท่านั้น]~~ กิ่งนั้น merge ไปแล้ว · 🔴 **ผู้เทสยังต้องรัน RECHECK เองก่อนบูตทุกครั้ง** · 🟢 **บูตเดียวรวมกับ `GT-210` ได้และควรทำ** (`/warp 3` ของ `GT-210` ก่อน แล้วค่อย `/warp 4`)]

> เปิดโดย LANE-A (WORLD) รอบ `gwwpmr` 2026-09-02T15:55+07:00 · **LANE-A บริโภคผลเอง**
> numbering: shared counter กับ `CLIENT_RE_QUEUE.md` -- ณ วันเปิด highest `GT` = 211, highest `RE` = 210
> ⇒ ใบนี้ `212` (รันคำสั่งค้นหาซ้ำตอน rebase) · บูต/DB/teardown ตาม `ATTENDED_SESSION_RUNBOOK.md`
> (teardown ปฏิเสธ boot stamp เก่ากว่า 420 นาที · รอบที่จบเพราะเลิกเล่นเฉย ๆ ก็ต้องรัน teardown)

- objective: ข้อพิสูจน์เดียว -- **เก้าเกาะ roster (ฉาก 4,5,6,7,8,9,10,11,130 · 630 actor) ตอบคลิก NPC
  บนไคลเอนต์จริงแล้ว และคลิกนั้นไม่พาผู้เล่นไปไหน** · ครึ่งความปลอดภัยอยู่ในข้อพิสูจน์เดียวกัน ไม่แยกใบ:
  คลิก actor ที่ **placement index 1** (actor identity `0x2002`) ต้อง **ไม่เปิดบทสนทนา Columbus ของ
  พอร์ตรอยัล และไม่ย้ายผู้เล่นไปแมพอื่น** (ปลายทางที่กลัวคือฉาก 17 ซึ่ง registry เขียน
  `login_entry_allowed: false`) · ฉาก 3 (Spice Paradise) เป็นของ `GT-210` **ไม่ใช่ใบนี้**
- PRECONDITION / RECHECK (ต้องผ่านครบสามข้อจึงเลื่อนเป็น `READY` · ตัดสินด้วยเนื้อโค้ด ห้ามเทียบเลข commit):
  🔴 **แก้รอบ `mcf4qp`: หนึ่งบรรทัด = หนึ่งคำสั่ง ไม่มี `&&` ไม่มีวงเล็บ** (PS 5.1 ไม่รับ `&&` · `( )` ไม่ใช่ subshell
  บน Windows ⇒ ฉบับเดิมพังทั้งสามบรรทัดและผู้เทสจะอ่านว่า "ยังไม่ merge" ทั้งที่ merge แล้ว) ·
  สองบรรทัดแรกรันจากโฟลเดอร์แม่ · บรรทัด `pytest` รันจากในรีโปเซิร์ฟเวอร์
  ```
  git -C pirate-force-server fetch origin
  git -C pirate-force-server show origin/main:src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_roster_scenes.py | findstr /C:"production_allowed = True"
  py -3 -c "import sys; sys.path.insert(0, r'pirate-force-server\src'); from pirateforce_foundation.lane_hooks import lane_a_choose_npc_roster_scenes as m; print(m.scenes_this_lane_answers_for()); print(m.skipped_scenes())"
  cd pirate-force-server
  py -3 -m pytest tests/test_lane_a_choose_npc_roster_scenes.py tests/test_columbus_quest_dispatch_wiring.py -q
  ```
  ข้อ 1 ต้องเจอจริง · ข้อ 2 ~~ต้องพิมพ์ **ครบสิบฉาก** `(3, 4, 5, 6, 7, 8, 9, 10, 11, 130)`~~ **แก้รอบ `mcf4qp`:
  ต้องพิมพ์ `(3, 4, 5, 6, 7, 8, 9, 10, 11, 126, 130)` พอดี และ `skipped` = `()`** -- ฉาก **126** (Bg3001 Atlantis)
  เข้ามาทีหลังใบนี้ (รอบ `gx7xtp`) และ **ไม่ใช่ขอบเขตของใบนี้** (ของมันคือ `GT-217`) ⇒ เห็น 126 **ไม่ใช่บิลด์ผิด**
  🔴 **เป็นเซตเป๊ะโดยตั้งใจ (pf-adversary D7):** ถ้าเกณฑ์เขียนว่า "ขอแค่เก้าฉากของใบอยู่ครบ" วันที่มีเลนเพิ่มฉากใหม่
  ที่มี placement index 1 เข้ามาโดย conjunct ใน `runtime.py` ยังไม่ครอบ ผู้เทสจะอ่านว่าผ่านแล้วบูตไปคลิกโดยไม่มีใครตรวจฉากนั้นเลย
  ⇒ **เจอ id ที่ไม่อยู่ในเซตนี้ = หยุดก่อนบูต รายงานให้เจ้าของใบตรวจก่อน ไม่ใช่ FAIL และไม่ใช่ผ่าน** ·
  เก้าฉากของใบนี้คือ 4,5,6,7,8,9,10,11,130 ต้องอยู่ครบเสมอ ·
  ข้อ 3 ต้อง **เขียวทั้งชุด** (ในนั้นมี `TheNineAreSafeOnlyBecauseTheRuntimeGuardStandsTests` และ
  `ColumbusSceneGuardTests` -- สองตัวนี้คือของที่พิสูจน์ scene guard แบบ headless ไปแล้ว) ·
  ว่าง/แดง/ขาดฉาก = ยังไม่ merge ⇒ คง `[BLOCKED]` **ห้ามบูต ห้ามเสียเวลาผู้เทสแม้แต่นาทีเดียว** ·
  ทดสอบก่อน merge ได้ถ้าเปลี่ยน `origin/main` เป็น `origin/claude/laughing-archimedes-gwwpmr`
  แล้ว **เขียนในผลว่าใช้ branch ไหนและ commit ไหน**
- db: `state\pirateforce.sqlite3` -- **สำเนาเท่านั้น ห้ามเปิดไฟล์ canonical** · คัดลอกเป็น
  `state\run_gt212_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา · จด sha256 ของสำเนาก่อน/หลัง ·
  จด sha256 ของ canonical ก่อน/หลัง และยืนยันว่า **ไม่เปลี่ยน** · `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง
  (รอบคัดลอก DB ⇒ ตำแหน่งตัวละครกลับไป spawn ทุกบูต เป็นเรื่องปกติ ไม่ใช่ผลวัด)
- server args: บูตปกติตาม `BRIDGE_BOOT_PROCEDURE.md` · 🔴 **ไม่มีแฟล็ก scenario ใด ๆ** ·
  `-SecondPasswordMode bypass` · บัญชี GM ใน `config/gm_accounts.json` · เก็บคอนโซลรวม stdout+stderr (`2>&1`)
  -- โทเคนของเลนออกทาง **stderr**
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt212_<stamp>.sqlite3
  ```
- เส้นทาง: **ใช้เส้นทางวาปของ `GT-192` ห้ามคิดเส้นทางใหม่** -- `/warp <scene n_id>` เปล่า **ไม่ใส่พิกัด**
- ตัวไหนคือ placement index 1 (ผู้เทสต้องทำได้จริง):
  ฉาก 4 index 1 = body ชื่อ **`Columbus`** (Mob-Set 2 · `n_ID=67` · outfit `M055_000_000_N` · lv50 hp23976)
  -- ชื่อพ้องกับ NPC พอร์ตรอยัลแต่คนละตัว และนั่นคือประเด็นทั้งหมดของใบนี้ ·
  🔴 **บนจออาจไม่มีอะไรบอกว่าตัวไหนคือ index 1** (ป้ายชื่ออาจว่าง -- `GT-030-R3` วัดได้แบบนั้นกับ actor type 4)
  ⇒ ถ้าหาจากจอไม่ได้ ให้ **คลิกหลายตัว รวมตัวแรกที่สำมะโนพิมพ์ในคอนโซล** แล้วอ่าน `placement=` ย้อนจาก
  บรรทัด `..._ANSWERED` · **ใบนี้ยังไม่ครบจนกว่าจะมีอย่างน้อยหนึ่งคลิกที่พิมพ์ `placement=1`**
- steps: (เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ)
  1. RECHECK ผ่านก่อน · LOCK_GAME · จด boot stamp · sha canonical · คัดลอก DB
  2. บูตเซิร์ฟเวอร์ **ใหม่สด** แล้วค่อยบูตไคลเอนต์ (เคยมีไคลเอนต์ถูกฆ่า = เซิร์ฟเวอร์ยังถือเซสชันไว้
     ตัวถัดไปจะค้าง "connecting" ตลอดกาล ⇒ **รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ**) · ห้ามบูตไคลเอนต์ทิ้งไว้
     โดยไม่มีเซิร์ฟเวอร์ (ตายใน ~3.5 นาที) · ล็อกอิน GM เข้าฉากจริงให้เสร็จก่อน
  3. ตอนบูต: ต้อง **ไม่มี** `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED` แม้แต่บรรทัดเดียว · มีบรรทัดใด = บิลด์ผิด
     **หยุด ไม่ต้องคลิก** ทั้งใบ `NO-RESULT` (คัดลอก `scene=`/`reason=` มาด้วย)
     🔴 **เพิ่มรอบ `mcf4qp` (วัดแล้ว):** ตอน import จะมีบรรทัด **คนละโทเคน** โผล่มาด้วยเสมอ --
     `LANE_A_CENSUS_SKIPPED scene=1 source=bg0001_census reason=reserved_by_a_runtime_branch`
     และ `... scene=2 source=bg0002_roster ...` · **สองบรรทัดนี้ปกติ ไม่เกี่ยวกับใบนี้ และไม่ใช่บิลด์ผิด**
     ⇒ เกรปด้วยสตริงเต็ม `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED` เท่านั้น **ห้ามเกรปคำว่า `SKIPPED` ลอย ๆ**
  4. คลิกช่องแชท **ยืนยัน focus จริง** (พิมพ์ตอนไม่ focus = ฮอตคีย์) · `/warp 4` · Enter · รอ ~3 วิ
     (`/warp` คือคำสั่ง GM **ไม่ใช่** ตัวยิงแชท 12 ตัวอักษร -- ห้ามเติมตัวอักษรให้ครบ 12)
  5. 🔴 **เดินหนึ่งก้าว** (`W` หรือ `S`) ก่อนคลิกเสมอ · วาปข้ามฉากล้าง `last_target_pos = None` และ
     responder ปฏิเสธเมื่อค่านี้เป็น `None` ⇒ **คลิกก่อนเดิน = เงียบ และนั่นคือความผิดของขั้นตอน ไม่ใช่ผลวัด**
  6. ภาพนิ่ง **เต็มความละเอียด** `S04-BEFORE` -- ยังไม่คลิกใคร · จัดมุมด้วย **คลิกขวาลาก** เท่านั้น
  7. **คลิกซ้ายหนึ่งครั้ง** บน NPC หนึ่งตัว โดยมีตัวอื่นในเฟรมอย่างน้อยสองตัว · `S04-AFTER` ภายใน ~3 วิ ·
     จดบรรทัด `..._ANSWERED` ดิบ ๆ ทุกครั้ง
  8. ทำซ้ำข้อ 5-7 จนได้คลิกที่ `placement=1` (อย่างน้อยสามคลิกต่างตัว) · หลังคลิกนั้น **จ้องจอ 30 วินาที**
     ไม่คลิกอะไรเลย · `S04-P1+2s` `S04-P1+30s`
  9. ทำซ้ำข้อ 4-8 กับอีกหนึ่งเกาะที่เลือกเอง (`/warp 5` หรือ `/warp 130`) ตั้งชื่อภาพตามฉากนั้น
  10. ตัวเช็ค NO-CRASH: **คลิกขวาลากหมุนกล้อง** เท่านั้น · ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้ ·
      🔴 **ห้ามเปลี่ยน facing ของตัวละครนอกจากก้าวเดินในข้อ 5**
  11. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err`, `capture_v141\GAME_LIVE.txt`, `GAME_EVENTS_LIVE.txt` + sha256 ·
      `integrity_check` · เช็ค sha canonical ซ้ำ · **รัน teardown เสมอ**
  🔴 **ขอบเขต:** คลิกเพื่อ **เลือก** เท่านั้น -- ห้ามตีมอน ห้ามใช้สกิล ห้ามคลิกโจมตี ทุกฉาก · เผลอตี = จดไว้ในผล
  🔴 **STOP:** ถ้ามีหน้าต่างบทสนทนา/เควสต์โผล่ หรือรู้ตัวว่าอยู่คนละแมพหลังคลิก ⇒ **หยุดทั้งใบทันที
  ปิดไคลเอนต์ รายงานทันที = FAIL** และเก้าเกาะต้องกลับไปอยู่หลัง skip rule เดิมของเลน
- pass criteria (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**):
    wire/DB (headless พิสูจน์ได้ ไม่ต้องมีตาคน · grep คอนโซลรวม `2>&1`):
      (ก) ตอนบูต **ไม่มี** `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED scene=<n> reason=<reason>` สำหรับเก้าฉากเลย
      (ข) ทุกคลิกที่ได้คำตอบ: `LANE_A_CHOOSE_NPC_SCENE<n>_ANSWERED placement=<idx> visible=<count>
          omitted=<count>` และ label ที่ส่ง `LANE_A_CHOOSE_NPC_SCENE<n>_FACE_P<idx>` ·
          **[คำทำนาย ไม่ใช่ผลวัด]** `omitted=0` ทุกครั้ง และ `visible` = จำนวน actor ที่สำมะโนขาเข้าส่ง
      (ค) มีอย่างน้อยหนึ่งบรรทัดที่ `placement=1`
      (ง) 🔴 ตลอดเวลาที่ยืนอยู่บนเก้าฉาก: **ไม่มี** event `core_request_014_columbus_npc_conversation_sent_once`
          และ **ไม่มี** label `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` -- นี่คือครึ่งสายของ
          เกณฑ์ความปลอดภัย · (จ) `integrity_check` = `ok` · sha canonical ไม่เปลี่ยน · ไม่มี traceback หลุด
      **ชั้นนี้ตอบไม่ได้เลยว่ามีอะไรถูกวาดบนจอ หรือผู้เล่นยืนอยู่ที่ไหน**
    client-observable (ต้องมีคนนั่งหน้าจอ · **ชั้นนี้เท่านั้นที่ตัดสินใบ**):
      (ฉ) หลัง `/warp 4` **เห็นชาวเกาะยืนอยู่จริง** ในเฟรมก่อนคลิก (`S04-BEFORE`)
      (ช) ตัวที่ถูกคลิก **หันมาหาตัวละครเรา** และมี **ชื่อและ/หรือแถบ HP** ขึ้น -- บันทึกสิ่งที่แสดงตรง ๆ
          **ช่องชื่อว่างเป็นการบันทึก ไม่ใช่ FAIL อัตโนมัติ** · เทียบ `AFTER` กับ `BEFORE`
      (ซ) 🔴 หลังคลิกตัวที่ `placement=1` ครบ 30 วินาที: **ไม่มีหน้าต่างบทสนทนา/เควสต์ใด ๆ** และ
          **ผู้เล่นยังอยู่เกาะเดิม** (พื้นหลังเดิม ชาวเกาะชุดเดิม กล้องไม่ถูกย้าย)
      (ฌ) actor ตัวอื่นในเฟรมเหมือนเดิมทุกตัว: อยู่ครบ · หน้าตาเดิม · ป้าย `LV` ไม่หายและไม่กลายเป็น `1`
      (ญ) 🔴 **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** ทุกภาพ · เขียนคำว่า `none`
          ออกมาแทนการเว้นว่าง · อ่านสีจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น** (ห้าม contact sheet/ภาพย่อ/วิดีโอ)
          · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067`) · ความต่างจากเซิร์ฟเวอร์จริงลง
          `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      **ผลลบมีค่าเท่าผลบวก:** มี `..._ANSWERED` ครบแต่จอไม่ขยับ ⇒ คำตอบคือ **เซิร์ฟเวอร์ตอบแล้ว ไคลเอนต์
      ไม่วาด** ⇒ ไม่ใช่ความผิดของ lane hook · **ห้ามถอน `production_allowed` ด้วยเหตุนี้** ให้เปิดใบ `RE-` ·
      มี `LANE_HOOK_FIRED` แต่ไม่มี `..._ANSWERED` ⇒ เช็คก่อนว่าเดินหนึ่งก้าวจริง (ข้อ 5) ·
      ไม่มี `LANE_HOOK_FIRED` เลย ⇒ คลิกไม่ถึงสาขานี้ = `NO-RESULT`
- nonclaims:
  1. ไม่พิสูจน์ว่าสำมะโนขาเข้าถูก/ครบ (`GT-192` ห้ามแก้) · ไม่พิสูจน์เลข `LV` (`GT-200` ห้ามแก้) ·
     ไม่พิสูจน์กลไก `/warp` เอง
  2. ไม่ตัดสินฉาก 3 (`GT-210`) ฉาก 14 (`GT-134`) ฉาก 1 หรือฉาก 2
  3. ไม่พูดเรื่องความหมายของสีป้าย -- `RE-067` ยังเปิด · จดสีอย่างเดียว
  4. ไม่พิสูจน์ว่า index space เป็น scene-aware แล้ว -- **ไม่ใช่** · ความปลอดภัยยังยืมมาจาก conjunct เดียว
     ใน `runtime.py` · ใบนี้พิสูจน์แค่ว่า **ผู้เล่นจริงกดแล้วไม่ถูกพาไปไหน** ไม่ใช่ว่าการชนกันหายไป
  5. ไม่พิสูจน์คอมแบต/aggro/HP · ไม่พิสูจน์ว่าอะไรรอดข้าม relog · ไม่พิสูจน์ melee/skill targeting
     บนฉากที่ responder อ้างสิทธิ์ (ภาระที่ยังไม่ปลด -- `runtime.py:7520-7533`)
- links: `lane_hooks/lane_a_choose_npc_roster_scenes.py` · `lane_hooks/lane_a_scene_census.py`
  (`_membership_if_answerable`) · `runtime.py` scene guard (PR #570) · `world_bg0004_identity.py` ·
  `tests/test_lane_a_choose_npc_roster_scenes.py` · `GT-210` (ฉาก 3) · `GT-192` (เส้นทางวาป) ·
  `GT-200` (ป้าย LV) · `GT-134` · `RE-067` (สีป้าย) ·
  `notes_to_chief/20260902_1207_LANE-A-CORE-REQUEST-columbus-branch-needs-a-scene-guard.md`
- result: (ผู้เทสกรอก: PASS/FAIL/NO-RESULT · branch/commit ที่บูต · ภาพ `S04-BEFORE`/`S04-AFTER`/
  `S04-P1+2s`/`S04-P1+30s` + ของเกาะที่สอง · บรรทัดคอนโซลดิบทุกบรรทัด (`..._ANSWERED` ทุกคลิก) ·
  บรรทัดสีป้ายครบทุกป้ายทุกภาพ · sha256 ทั้งสี่ค่า · timestamp +07:00 ·
  `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: LANE-A (WORLD) รอบ `gwwpmr` 2026-09-02T15:55+07:00 -- LANE-A บริโภคผลใบนี้เอง**

## GT-216 MULTI-VITAL-WALKER-MAKES-GROUND-PICKUP-PLAYABLE-001  [✅ **PASS สองชั้น · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — จอเจ้าของ R306: คลิกเก็บ 10 ครั้ง เข้ากระเป๋า 9 · 8 ใน 9 ติดคลิกแรก · กระเป๋า 3→12 ตรงกับ DB · `vital_count_not_one` = 0 (เดิม 42/46) · จดหมายผล `notes_to_chief/20260903_1657_KA1A-R306-RESULTS-*.md` · **ห้ามบูตซ้ำเพื่อวัดสิ่งที่วัดแล้ว** · 🔴 ที่ยัง **ไม่** อ้าง: ของหายชั่วคราวตอนตีตัวถัดไปแล้วโผล่กลับ = `RE-208` ของ LANE-B (ขั้นปิดอยู่ใน `GT-223` ตาม `COO 20260903_1942` ข้อ 4) · ✅ RECHECK เดิมที่ grep ชื่อโมดูลในตัวเอง (`1743` ข้อ 3 ข้อย่อย 6) **แก้ถ้อยคำแล้วรอบนี้** ถามโทเคนกับชื่อจุดเสียบแทน]

### 🔴 โทเคนที่ห้ามอ่านว่าเสีย (`COO-DECISION 20260903_0953` ข้อ 2 -- เขียนลงทุกใบที่มีคลิกเก็บของ)
  **`cell_has_no_scene` ก่อนการฆ่ามอนตัวแรก *ของเซสชันล็อกอินนั้น* = พฤติกรรมที่ถูก ไม่ใช่ความเสีย ห้ามรายงาน FAIL**
  เซสชันที่เพิ่งล็อกอินถือ ground cell ที่ยัง `current_scene is None` (LANE-B วัดเองรอบ `gewbnj`) และซอร์สเขียนไว้ตรง ๆ ว่าตั้งใจ:
  `mob_pickup.py:1454-1460` -- "the cell does not know its scene -> `cell_has_no_scene` ... reachable mainly before the first kill of a boot -- where refusing is right" (chief re-derive เองรอบ R317 ไม่ได้เชื่อจดหมายแหล่งเดียว)
  🔴 **หน่วยคือ "เซสชัน" ไม่ใช่ "บูตของเซิร์ฟเวอร์"** — chief วัดเองรอบ R317: `DropLedgerCell()` ถูกสร้างใหม่ต่อหนึ่งเซสชัน (`runtime.py:1328`)
  และ `_scene` ถูกตั้งได้แค่สามทาง: ctor (`mob_loot.py:2772`) · การฆ่า (`:3005`) · `enter_scene` ที่ขอบฉาก (`:3261`)
  ⇒ **รีล็อกอินระหว่างบูตเดียวกัน = cell ใหม่ = ตัวนับเริ่มใหม่** เห็นโทเคนนี้อีกครั้งหลังรีล็อกอินก่อนฆ่าอะไร **ยังเป็นปกติ**
  ⇒ **เห็นบนพื้นว่างก่อนฆ่าอะไรในเซสชันนั้น = ปกติ เดินต่อได้** · เห็น**หลัง**ฆ่ามอนในเซสชัน*เดียวกัน*แล้วและของตกจริงแล้ว = **finding** หยุดและรายงาน
  🔴 **รีล็อกอินกลางใบ = ตัวนับรีเซ็ต** ⇒ ถ้าต้องรีล็อกอิน ให้ **ฆ่ามอนหนึ่งตัวก่อน** แล้วค่อยตัดสินโทเคนนี้ อย่าตัดสินจากการฆ่าครั้งก่อนรีล็อกอิน
  🔴 **คัด *ข้อความ* ไม่ใช่แค่โทเคน** — ชื่อเดียวกันถูกใช้สองความหมาย (`mob_pickup.py:1477-1483` แปลง `MobLootContractError` ทุกตัวเป็นชื่อนี้):
  ข้อความ `does not know which scene it is in` = **กรณีปกติข้างบน** · ข้อความ `could not answer which scene it is in (<เหตุผลข้างใน>)` = **finding เสมอ** ไม่ว่าจะฆ่าอะไรมาแล้วหรือยัง
  (ทางที่สองยังไม่เคยถูกรัน — ซอร์สติด `# pragma: no cover` ⇒ เจอเมื่อไหร่คือของใหม่ ต้องรายงาน)

### 📎 เก็บฟรี -- ไม่ใช่เกณฑ์ของใบนี้ และไม่มีทางทำให้ใบนี้ FAIL (เพิ่มโดย chief R322)
  ระหว่างรอบนี้ **ถ้า** มีล็อกอินใดถูกปฏิเสธ (คอนโซลขึ้น `WORLD_SCENE_ENTRY_REFUSED`) ให้คัด **ทั้งบรรทัด** ใส่จดหมายผล
  🔴 **แล้วเทียบค่าด้วยตา อย่าดูแค่ว่ามีคำนี้อยู่**: `refused_character_id=<เลข>` ต้องเป็น**เลขเดียวกับตัวละครที่คุณล็อกอินจริง**
  และ `refused_name=` ต้องเป็น**ชื่อตัวละครนั้น** · เห็น `refused_character_id=none` หรือเลขคนละตัว = **finding** รายงานทันที
  (เหตุผล: `pf-adversary` R322 พิสูจน์ว่าการสลับอาร์กิวเมนต์สองตัวทำให้ทุกช่องพิมพ์ `none` โดยที่คำว่า `refused_character_id=`
  ยัง grep เจอครบ ⇒ **การ grep หาคำอย่างเดียวปิดใบนี้ไม่ได้** ต้องเทียบ**ค่า**)
  🔴 **ไม่มีล็อกอินถูกปฏิเสธในรอบนี้ = ไม่ต้องทำอะไร ไม่ใช่ FAIL ไม่ใช่ finding** -- ปกติล็อกอินจะไม่ถูกปฏิเสธ
  ประโยชน์: `CORE-REQUEST 20260903_1505` ปิดได้เมื่อเห็นเลขที่**ตรงกับตัวละครจริง**บนคอนโซลหนึ่งครั้ง (เทสยูนิตปิดใบนั้นไม่ได้)

RECHECK: `git -C pirate-force-server fetch && git -C pirate-force-server grep -c "VITAL_WALK_PROMOTED_TOKEN" origin/main -- src/pirateforce_foundation/vital_walk.py && git -C pirate-force-server grep -c "_vital_walk_promote_target_pos" origin/main -- src/pirateforce_foundation/runtime.py`
  🔴 **แก้ถ้อยคำโดย chief รอบ `pk14rf`/R326 ตาม `COO-DECISION 20260903_1743` ข้อ 3 ข้อย่อย 6** — บรรทัดเดิม grep คำว่า `vital_walk` ใน `vital_walk.py` ซึ่งเป็น **ชื่อโมดูลในตัวมันเอง** = จริงเกือบตลอดโดยไม่ได้พิสูจน์ว่าโค้ดที่ใบนี้พึ่งมีอยู่ · บรรทัดใหม่ถามสองอย่างที่ **หายได้จริง**: โทเคนที่โมดูลประกาศ และ **ชื่อจุดเสียบใน `runtime.py`** (ไม่ใช่บรรทัด import)
  ต้องได้ **สองค่าที่ไม่ใช่ศูนย์** = โมดูลอยู่บน main และ `runtime.py` เสียบมันจริง ⇒ ใบนี้ `READY`
  ได้บรรทัดเดียวหรือศูนย์ = โค้ดหาย ให้ตีกลับเป็น `BLOCKED` แล้วเขียนถึง chief
  🔴 **บรรทัด RECHECK เดิมของใบนี้ผิด และ chief เป็นคนเขียนผิดเอง** (R309) มันสั่ง grep หาสตริง
  `VITAL_WALK_PROMOTED` ใน **ทั้งสอง** ไฟล์ แต่โทเคนนั้นเป็นค่าคงที่ที่ประกาศใน `vital_walk.py:162`
  ไฟล์เดียว ส่วน `runtime.py` เป็นฝ่าย **เรียก** ตัวพิมพ์ ⇒ เกณฑ์เดิมเป็นเท็จตลอดกาล และจะขัง
  ใบนี้ไว้แม้โค้ดขึ้น main ครบแล้ว · วัดจริงรอบ R310: `origin/main` มี `vital_walk.py`
  (`VITAL_WALK_PROMOTED_TOKEN` บรรทัด 162 · จุดพิมพ์บรรทัด 420) และ `runtime.py:26` `import vital_walk`
  พร้อมจุดเสียบ `_vital_walk_promote_target_pos` (6428) และ `walk_nested_vitals` (6473)
  ⇒ ตัวบล็อกเดียวที่หัวใบเดิมอ้าง (`PR #600 ยังไม่ขึ้น main`) **หมดไปแล้ว วัดจาก main ไม่ใช่จากบันทึกรอบก่อน**
  สถานะกลางหลังรันจบแต่ยังไม่มีลายเซ็นตาคน = **`AWAITING-OBSERVER`** (ไม่ใช่ PASS ไม่ใช่ FAIL)
  ใบนี้มีชั้น client-observable ⇒ **G-OBS บังคับ**: จดหมายผลต้องมีบรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ไม่มี = chief ไม่ปิดใบ

- objective: (ข้ออ้างเดียว) ตัวเดิน nested vital ตัวใหม่ (`src/pirateforce_foundation/vital_walk.py` + call site สองจุดใน `runtime.py`)
  ทำให้ **การคลิกซ้ายเก็บของบนพื้นสำเร็จตั้งแต่คลิกแรก แทนที่จะรอด 2 จาก 46 อย่างที่วัดได้ใน `GT-204`/R303**
  `GT-204` PASS แล้วว่า "เก็บได้อย่างน้อยหนึ่งครั้ง" · ใบนี้ถามคนละคำถาม: **มันเล่นได้จริงหรือยัง**
- db: `default_state\pirateforce.sqlite3` -- **สำเนาเท่านั้น ห้ามเปิด canonical** · คัดไป
  `backup\pirateforce_before_GT-216_<yyyyMMdd_HHmmss>.sqlite3` แล้ว `state\run_gt216.sqlite3` ·
  จด sha256 สำเนาก่อน/หลัง · sha256 canonical เทียบ `CANON_SHA.txt` **ก่อนและหลัง ต้องเท่ากัน** · `PRAGMA integrity_check` = `ok` สองครั้ง
- server args: บูตปกติบน `main` **ไม่มีแฟล็ก `--*-scenario` ใด ๆ** (production branch):
  `py -3 -u -m pirateforce_foundation.app --db state\run_gt216.sqlite3`
- steps: (playbook: `ATTENDED_SESSION_RUNBOOK.md` · อัดวิดีโอต่อเนื่องตลอด `LOCK_GAME`)
    0. LOCK_GAME · boot stamp (teardown ปฏิเสธ stamp เก่ากว่า 420 นาที) · sha canonical · copy DB · รัน `RECHECK` ไม่ผ่าน = ไม่บูต
    1. **server ก่อน client เสมอ** · เข้าเกม จด scene + X/Y/Z · ยืนยันบล็อก "สมประกอบ" จากคอนโซล
    2. จัดกล้องด้วย **คลิกขวาค้างลาก** เท่านั้น (ไม่เปลี่ยน facing ไม่มีไบต์ขึ้นไวร์) · `Q`/`E` และ `W/A/S/D` เปลี่ยน **facing ของตัวละคร** และยิง `TargetPosVital` ⇒ ใช้ได้เฉพาะขั้นที่สั่งให้เดิน · **ห้ามพิมพ์ตัวอักษรตลอดรอบ** (ตัวอักษรตอนช่องแชทไม่โฟกัส = ฮอตคีย์)
    3. ไปฉาก 2 · ฆ่ามอนจนได้ของบนพื้น **อย่างน้อย 10 ชิ้น** (ฆ่าหลายตัวได้) · ถ่าย full-res **S0** ตอนของกองอยู่
    4. เปิดกระเป๋า นับช่องที่มีของ ถ่าย **S1** แล้วปิด
    5. เดินด้วย `W/A/S/D` เข้าไปติดของ **แล้วคลิกซ้ายที่ของชิ้นนั้น "หนึ่งครั้ง"** · รอ 2 วินาที · ถ้าไม่หาย ให้คลิกซ้ำได้ **แต่ต้องนับจำนวนคลิกของชิ้นนั้นลง result ทุกครั้ง** (ตัวเลขนี้คือตัวหารของชั้น client-observable)
    6. ทำซ้ำขั้นที่ 5 ให้ครบทุกชิ้น (>= 10 ชิ้น) · **ห้ามลากของในกระเป๋า** (item-move คนละเลน)
    7. เปิดกระเป๋าอีกครั้ง ถ่าย **S2** · NO-CRASH ด้วย **คลิกขวาค้างลาก** (🔴 ห้ามใช้ `Q`/`E` เป็นตัวเช็ค) · **S3** · ออกเกมด้วย X มุมขวาบน
    8. ปิดเซิร์ฟเวอร์ (**ฆ่าไคลเอนต์แล้วต้อง restart เซิร์ฟเวอร์ก่อนบูตหน้า ไม่งั้นค้าง "connecting" ตลอดกาล**) · เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `capture_v141\GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · **teardown เสมอ** · sha canonical ซ้ำ · ห้าม commit เอง
    9. คัดดิบ ห้ามตีความ:
       `findstr /N /C:"MOB_PICKUP_REQUEST_DECODED" /C:"MOB_PICKUP_REQUEST_REFUSED" /C:"MOB_PICKUP_ROW_INSERTED" /C:"VITAL_WALK_PROMOTED" /C:"VITAL_WALK_REFUSED" server_console_live.*.txt`
       `findstr /N /C:"vital_walk_" capture_v141\GAME_EVENTS_LIVE.txt`

- ตัวเลขที่ต้องคำนวณ (เขียนสูตรไว้เพื่อไม่ให้ตีความต่างกัน):
    `N_click` = จำนวนคลิกซ้ายที่ของ นับจากวิดีโอ (ขั้น 5-6)
    `N_dec`   = จำนวน `MOB_PICKUP_REQUEST_DECODED`
    `N_vc1`   = จำนวน `MOB_PICKUP_REQUEST_REFUSED reason=vital_count_not_one` (**R303 = 42 จาก 46**)
    `N_silent` = `N_click - N_dec - (refused ทุก reason)` = คลิกที่หายเงียบ

- pass criteria: (สองชั้น 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด** -- G5)
    wire/DB          : (1) `N_click >= 10` · (2) **`N_vc1 = 0`** · (3) `N_dec >= 0.90 * N_click` ·
      (4) `VITAL_WALK_PROMOTED vital=0x4543 vital_count=<n>` ปรากฏอย่างน้อยหนึ่งบรรทัด (= มีคลิกที่ถูกกู้จริง) ·
      (5) `VITAL_WALK_PROMOTED vital=0x2A90 vital_count=<n>` ปรากฏ **หนึ่งบรรทัดต่อหนึ่ง connection** (มากกว่านั้น = การกันสแปมพัง รายงานเป็นข้อสังเกต) ·
      (6) จำนวนแถวใหม่ใน `character_backpack_items` = จำนวน `MOB_PICKUP_ROW_INSERTED` (จด `item_identity`/`template_id`/`quantity`/`slot` ทุกแถว) ·
      (7) `integrity_check` = `ok` · sha canonical ตรง `CANON_SHA.txt` ก่อน/หลัง · ไม่มี traceback ที่ไม่ถูกจับ
      ชั้นนี้ตอบไม่ได้: บนจอของหายไหม กระเป๋าขยับไหม ต้องคลิกกี่ทีถึงติด
    client-observable: **ต้องมีคนอยู่หน้าจอเท่านั้น ห้ามอนุมานจากคอนโซล** --
      (1) **ของ >= 9 ชิ้นจาก 10 ชิ้นหายจากพื้นด้วยคลิกเดียว** (จดจำนวนคลิกต่อชิ้นครบทุกชิ้น) ·
      (2) **ตัวเลข/ช่องกระเป๋าบนจอขยับขึ้นตามจำนวนชิ้นที่เก็บ** เทียบ `S1` กับ `S2` ·
      (3) NO-CRASH/CRASH · มีข้อความระบบขึ้นไหม (คัดเป๊ะ + สี) ·
      🔴 **จดสีป้ายชื่อทุกป้ายทุกภาพ หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** อ่านจาก **full-res เท่านั้น** · ไม่มีป้ายให้เขียน `none` ห้ามเว้นว่าง · **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (`RE-067` เป็นเจ้าของ)
      ชั้นนี้ตอบไม่ได้: `N_vc1` เป็นเท่าไร มีแถวลง DB จริงไหม

- คำทำนาย (**เป็นคำทำนาย** · ทำนายผิด = ผลการวัด ไม่ใช่ความล้มเหลว):
    P1 `N_vc1 = 0` · `N_dec ~= N_click` · ของหายคลิกเดียว => ผ่านทั้งสองชั้น
    P2 `N_vc1 = 0` แต่โผล่ `reason=` ชื่ออื่น (เช่น `claimant_out_of_range`) => ตัวเดินทำงาน แต่เหลือประตูอื่น ⇒ **ผลลบนี้มีค่าเท่าผลบวก** redirect ไปที่ชื่อ reason นั้น
    P3 เจอ `VITAL_WALK_REFUSED reason=unknown_vital_id` => ไคลเอนต์ยัด vital ที่ตารางไม่รู้จัก ⇒ redirect ไปขยายตารางความยาว (คัด hexdump ห้าม decode เอง)
       🔴 บรรทัดนี้พิมพ์ **ครั้งเดียวต่อหนึ่งเหตุผลต่อหนึ่ง connection** · จำนวนครั้งจริงอ่านจาก event `vital_walk_refused_*`
    P4 ไม่มีของให้คลิก / ของหายก่อนเดินถึง => **NO-RESULT (ประตู `GT-188`)** ไม่ใช่ FAIL

- nonclaims:
  1. ตารางความยาวของตัวเดินครอบ **สี่ vital id เท่านั้น** (จาก 49 ชื่อที่ v141 รู้จัก) · id อื่นทำให้ **ทั้งเฟรมถูกปฏิเสธ** และคงพฤติกรรมของ `main` วันนี้เป๊ะ
  2. 🔴 **ใบนี้ไม่ตัดสินว่าใครถูกระหว่างสองหลักฐานที่ขัดกัน** -- ka1-A เขียนว่า "the request usually arrives as vital 2..5" แต่โทเคน `vital_count_not_one` 42 ครั้ง **เกิดได้เฉพาะตอน pickup vital เป็นตัวแรก** ⇒ ขัดกันตรง ๆ · ตัวเดินรองรับทั้งสองแบบ
  3. `vital=0x2A90` พิมพ์ **ครั้งเดียวต่อ connection โดยเจตนา** ⇒ **จำนวนบรรทัดนั้นไม่ใช่จำนวน TargetPos ที่ถูกกู้** ห้ามเอาไปเป็นตัววัด
  4. 🔴 **ความยาว body ของ `TARGET_POS` = 24 มีแหล่งเดียว ไม่ใช่สอง** -- ทั้งสองแหล่งวาง vital นี้ไว้ท้ายเฟรม ซึ่งแยก "body 24" กับ "body 22 + trailer 2" ไม่ออก
     ⇒ ถ้าอ่านผิด เฟรมที่ `TargetPos` ไม่ได้อยู่ท้ายจะพัง **และจะโผล่เป็น `VITAL_WALK_REFUSED`** ไม่ใช่เงียบ (ดู P3)
  5. ไม่พิสูจน์ว่าของอยู่บนพื้นนานเท่าไร และไม่พิสูจน์ว่า PRESERVE ทำงาน -- `GT-188` เป็นเจ้าของ
  6. ไม่พิสูจน์ว่าของ **รอดข้าม relog** -- `GT-142`
  7. ไม่พิสูจน์ว่า consumer อื่นที่เคยเสียหางเฟรมถูกซ่อมด้วย · ใบนี้ครอบแค่ pickup + `last_target_pos`
  8. ไม่ตัดสินสาเหตุของสีป้ายใด ๆ (`RE-067`) · ไม่ใช่เทส stack / กระเป๋าเต็ม / สองผู้เล่นแย่งของ
- result: (ผู้เทสกรอก · ตัวเลข `N_click`/`N_dec`/`N_vc1`/`N_silent` + จำนวนคลิกต่อชิ้นครบทุกชิ้น + ตารางสีป้าย · ผลเต็มไปที่ round file และจดหมายผล ไม่ใช่ในใบนี้)

## GT-254 ISLAND-155-CONTACT-TRIGGER-FRAME-CAPTURE-001  [⛔ **CLOSED = `CANCELLED - refuted by KA1A-R318 §3 (Slave Market Island/แถว 155 อยู่ฉาก 304 Dark Fog Sea ไม่ใช่ 126)`** -- ปิดโดย chief (LANE-E) รอบ `r045nx`/R354 ตาม `COO-DECISION 20260905_1349` ข้อ 2
> ⛔ **อย่าเดินขั้นใดของใบนี้** · ใบนี้ตั้งอยู่บนสมมติฐานว่าเกาะ 155 (Slave Market Island) อยู่ในฉาก 126 -- **ผิด**: แผนที่โลกของไคลเอนต์ (Panya เปิดแผนที่ M ตอน 12:47 ใน R318) แสดงว่าฉาก 126 "Atlantic Ocean: Rising Sun Sea" มีเฉพาะ Prison Exile Island · Port Royal · Spice Paradise Island ส่วน Slave Market Island + Evil Port อยู่ "Atlantic Ocean: Dark Fog Sea" = **ฉาก 304** (`gm_scene_name_tip.tsv`)
> **ใบแทน**: ออกใบใหม่ในฉาก 304 ได้เมื่อกลไก **"ข้ามขอบทะเล"** (แล่นเรือชนขอบแมพด้านตะวันตก → 304 · ด้านใต้ → 305) ผ่านบนจอแล้ว (`COO-DECISION 20260905_1348` ข้อ 6 · R318 §4 วัด id ขอบ: ตะวันตก `7` ที่ X≈-8090 ยิงซ้ำ 2/2 · ใต้ `69` ที่ Y≈-8384 · เหนือ `48` · ตะวันออกเงียบ) -- เลขใบใหม่จะถูกตั้งเมื่อร่างมาถึง ห้ามใช้เลข `GT-254` ซ้ำ
> **ไม่ใช่ความผิดของ `GT-233`** (เกรดแยกใบตามกติกาของใบนี้เอง) · P-A ของ R318 ผ่านครบ ขั้น 1-6 ไม่ได้ทำ = `NO-RESULT` ก่อนถูกยกเลิก
> เดิม: 🟡 PENDING -- แนบท้ายบูตของ `GT-233` · เจ้าของใบ/ผู้บริโภคผล = **LANE-A** · ผู้รัน = attended (Panya) · ~10-12 นาทีบนจอ **ต่อท้าย** GT-233 · ร่างโดย LANE-A รอบ `qqqtqp` 2026-09-05T01:35+07:00]

> ✅ **เลขตั้งแล้ว = `GT-254`** โดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:4x+07:00 (ใบนี้กับใบ `GT-250`-`GT-253` ของ chief ต่อท้ายไฟล์เดียวกันในรอบเดียวกัน ⇒ ชนกันตอน rebase · เก็บทั้งสองฝั่งครบ ไม่มีใบไหนถูกทิ้ง · ตัวนับร่วมสองคิว + `archive/` คืนสูงสุด `249` ก่อนรอบนี้ ⇒ ชุดนี้กิน `250`-`254`) · `GT-254`/`RE-254` = 0 hit ทั้งสามที่ก่อนวาง
> ~~**เลขใบเป็นของ chief** -- ปล่อยไว้เป็น `GT-254`~~ ผู้เทสและ LANE-A ห้ามตั้งเลขเอง (ตัวนับร่วมสองคิว + archive) · หัวใบใน index ข้างบนให้ chief เป็นคนวางพร้อมเลข
> ใบนี้เป็นน้องของ `GT-228` (PASS R308) ทุกประการ: **ใบ "เก็บ hex" ไม่ใช่ใบตัดสินการเทียบท่า** และไม่ใช่ใบเข้าเกาะ
> 🔴 **PIGGYBACK -- ห้ามบูตรอบใหม่เพื่อใบนี้**: เดินบน **บูตเดียวกับ `GT-233`** (เจ้าของเครื่องจะบูตเพื่อ `GT-233` อยู่แล้ว บูตซ้ำ = เสียเปล่า) · **ทำ `GT-233` ให้จบทุกขั้นและจดผลของมันครบก่อน** แล้วจึงเริ่มขั้น 1 ของใบนี้
> 🔴 **เกรดแยกใบเด็ดขาด**: ผลลบของใบนี้ **ไม่ใช่** ความล้มเหลวของ `GT-233` และผล `GT-233` ไม่ตัดสินใบนี้ · เขียนผลสองใบแยกจดหมาย/แยกหัวข้อ

- objective: ข้อพิสูจน์เดียว -- **เรามี hex ดิบของทุกเฟรมที่ไคลเอนต์ส่งออกในหน้าต่าง +/-5 วินาที รอบจังหวะที่เรือ "ชน/เข้าเขต" เกาะ Slave Market Island (แถว dock `155`) ในฉาก 126 อย่างน้อยสองครั้ง**
  🔴 ใบนี้ต้องการแค่ **สองอย่าง** จาก hex ก้อนนั้น: (ก) **คู่พิกัด HUD `X Y` ณ วินาทีสัมผัส** และ (ข) **trigger id ที่ `TriggerVital 0x1FB2` ถืออยู่ ณ จังหวะสัมผัส** · **ไม่ต้องการการเข้าเกาะ ไม่ต้องการหน้าต่างรายงานกัปตัน**
  ที่มา: `GT-228` วัดสองอย่างนี้ให้เกาะ 153/154 และนั่นคือเหตุผลเดียวที่ `world_m2_survey_plan.MEASURED_XYZ` ไม่ว่าง และเป็นเหตุผลเดียวที่ `GT-233` ออกเรคอร์ดได้ · จะขยาย M2 พ้นสองเกาะแรกต้องได้ **สองอย่างเดียวกัน** ของแถวถัดไปคือ `155 Slave Market Island · scene 4 · BG0004 · min_level 45 · wire=CANDIDATE`
  (z ตัวที่สามไม่ต้องอ่านจาก HUD -- `GT-228` ถอดจากสาม float ของ tag `2A` ในเฟรมเอง ได้ 186.0 ทุกครั้ง · ผู้เทสส่ง **HUD pair + hex ดิบ** เท่านั้น LANE-A ถอดเอง)

- prediction (🔴 **คำทำนาย ไม่ใช่ผลวัด · ทำนายผิด = finding ไม่ใช่ใบตก**):
  P1. ชนเกาะ ⇒ ไคลเอนต์ยิง `0x1FB2` โดย tag `0x0F` = **`4`** (= `scene_name_tip_id` ของแถว 155) เทียบเคียงจาก R308 (153→id 2 · 154→id 3) · **หลักฐานเป็นการอนุมานจากสองแถว ไม่ใช่กฎ**
  P2. **ไม่มีหน้ารายงานกัปตันที่เกาะ 155** -- บิลด์นี้ provision เฉพาะ 153/154 (`PLANNED_TRIGGER_IDS = M2_TARGET_TRIGGER_IDS` · `provisionable_count() = 2`) ⇒ **ไม่มีหน้าต่าง = ผลที่คาดไว้** ไม่ใช่รอบล่ม และไม่หักล้างอะไร
  P3. เจอ **ข้อความปฏิเสธเรื่องเลเวล** มากกว่าเจอหน้าต่างใด ๆ (ตารางไคลเอนต์เอง แถว 155: `[เข้าได้เมื่อ: Lv.45]`)

- 🔴 PRECONDITION (เช็คจริง ไม่ใช่หมายเหตุ):
  P-A. `GT-233` เดินจบและจดผลแล้ว · **ยังอยู่ในฉาก 126 · ไคลเอนต์ยังไม่ตาย · ตัวจับแพ็กเก็ตยังเขียนไฟล์อยู่** · ถ้า `GT-233` จบด้วย STOP (ไคลเอนต์ปิด) หรือจบด้วยการ **เปลี่ยนฉากเข้าเกาะ** ⇒ ใบนี้ **`NO-RESULT: ไม่ได้อยู่ในฉาก 126`** ยกไปบูตหน้า **ห้ามบูตใหม่วันนี้เพื่อใบนี้**
  P-B. จุดยิง hook มีจริงในโคลนที่บูต: หาโทเคนใน **stderr** `LANE_HOOK_REGISTERED pirateforce_foundation.lane_hooks.lane_a_island_trigger_log vital_inbound_trigger_vital` (ไม่เจอ = เขียนว่า "ไม่มี" แล้ว **เดินใบต่อ ห้ามรายงาน FAIL ห้ามแก้โค้ดเอง** -- ครึ่งจับแพ็กเก็ตคือครึ่งที่ตัดสินใบ)
  P-C. **min_level 45 · ตัวละครเทสแทบแน่นอนว่าไม่ถึง** ⇒ **การถูกปฏิเสธคือ RESULT ไม่ใช่ FAIL** และมันแปลว่า **การตรวจการชนเกิดขึ้นแล้ว** ซึ่งคือสิ่งที่ใบนี้อยากได้
  P-D. **ห้ามพิมพ์ลงแชทตลอดช่วงนี้** (ตัวอักษรตอนแชทไม่ focus = ฮอตคีย์) · ไม่ต้องใช้ `/warp`
  P-E. เซิร์ฟเวอร์ก่อนไคลเอนต์เสมอ · ฆ่าไคลเอนต์แล้ว **ต้องรีสตาร์ตเซิร์ฟเวอร์ก่อน** เปิดตัวใหม่

- db: **สำเนาเดียวกับ `GT-233`** -- 🔴 **ห้ามคัดลอก DB ใหม่กลางรอบ ห้ามเปิด canonical `state\pirateforce.sqlite3`** · sha256 canonical ก่อน/หลัง ต้องไม่เปลี่ยน · `PRAGMA integrity_check` = `ok` (ใช้ค่าชุดเดียวกับ teardown ของ `GT-233`)
- server args: **เหมือน `GT-233` ทุกตัวอักษร ไม่มีแฟล็กเพิ่มของใบนี้เลย** (`PF_M2_SURVEY_TRIAL=1` · ไม่มี `--*-scenario`) · เก็บคอนโซลรวม `2>&1` ต่อเนื่อง · `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` เปิดค้างตลอด
  หมายเหตุที่ทำให้ใบนี้ปนกับ `GT-233` ไม่ได้: trial provision เฉพาะ 153/154 ⇒ **ไม่มีเรคอร์ดใดของเกาะ 155 ถูกส่ง**

- steps: (จดเวลานาฬิกา `HH:MM:SS+07:00` ทุกครั้งที่เขียนว่า "จดเวลา" -- ไม่จด = ตัดหน้าต่าง hex ไม่ออก)
  1. จด **`T_START` = เวลาที่เริ่มขั้นนี้** (เส้นแบ่งระหว่าง `GT-233` กับใบนี้) · ภาพนิ่ง `S155-START` เต็มความละเอียด · ยืนยันว่ายังเป็นเรือ + HUD เข็มทิศ
  2. หาเกาะด้วย **คลิกขวาลาก (หมุนกล้องล้วน -- ไม่มีไบต์ออกสาย)** · ภาพ `S155-LOOK1..3` · **ยืนยันตัวเกาะจากป้ายชื่อบนจอ คัดตามตัวอักษร** · หาไม่เจอภายใน ~8 นาที ⇒ **`NO-RESULT: ไม่พบเกาะ`** พร้อมรายชื่อเกาะที่เห็นจริง **ห้ามเดาว่าก้อนไหนคือ 155**
  3. แล่นเข้าชนด้วย `W/A/S/D` และ `Q`/`E` -- 🔴 ใบนี้ **ต้องการ** ให้ตัวละครขยับและหันจริง · 🔴 **ห้ามคลิกซ้ายใส่เกาะ** (คนละเส้นทาง) · ภาพ `S155-APPROACH` · **จดเวลาวินาทีที่แตะ** · ภาพ `S155-CONTACT` ภายใน ~2 วิ · ค้างนิ่ง ~10 วิ · ภาพ `S155-AFTER` · **อ่านและจด HUD `X Y` จากภาพ `S155-CONTACT` ตามตัวอักษร**
  4. ถอยออก ~5 วิ แล้วชนซ้ำครั้งที่สอง: **จดเวลาใหม่** · ภาพ `S155-CONTACT-B` · **จด HUD `X Y` ซ้ำจากภาพนี้**
  5. NO-CRASH ตอนจบ: **คลิกขวาลากหมุนกล้องเท่านั้น** · ออกด้วยปุ่ม X
  6. ปิดเซิร์ฟเวอร์ · เก็บคอนโซลรวม + `GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ**
  🔴 **STOP-1 (เข้าเกาะ):** ฉากเปลี่ยนเข้าเกาะจริง หรือมีหน้าต่างยืนยันโผล่แล้วเผลอกด ⇒ หยุดทั้งใบ ปิดไคลเอนต์ รายงานทันที · **ใบนี้ไม่มีสิทธิ์กดยืนยัน**
  🔴 **STOP-2 (ไม่มี TriggerVital เลยที่เกาะ 155):** หลังชนสองครั้งแล้วเงียบ ⇒ **ชนได้อีกครั้งเดียว โดยเข้าจากอีกด้านของเกาะ** (จดเวลา · ภาพ `S155-CONTACT-C`) แล้ว **หยุด** · ห้ามชนซ้ำต่อ ห้ามไปลองเกาะอื่น ห้ามแก้บิลด์
  (คอนโซลเงียบอย่างเดียวไม่ใช่ข้อสรุป: `parse_outer` อ่าน nested vital **ตัวแรกตัวเดียว** ถ้า TriggerVital มาเป็นตัวที่สอง คอนโซลจะเงียบทั้งที่เฟรมมีจริง -- ตัดสินจาก hex เท่านั้น)

- pass criteria (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**):
    wire/DB:
      (ก) 🔴 **เกณฑ์ผ่านของใบ**: ตัด hex ดิบจาก `GAME_LIVE.txt` **หน้าต่าง +/-5 วินาที รอบทุกเวลาสัมผัสที่จดไว้** · **คัดทุกเฟรม ทุก opcode ไม่กรองอะไรทิ้ง** พร้อม index เฟรม + จำนวนไบต์ต่อเฟรม · `TargetPosVital` รัว ๆ ต้องอยู่ในนั้นด้วย · **ครบสองจังหวะสัมผัส = ผ่านชั้นนี้**
      (ข) ตัวช่วยค้น (**ไม่ใช่ตัวตัดสิน**): รูปเฟรม `12 B2 1F 0B 01 0F <u16> 00 0B 04 2A x 2A y 2A z` · id `4` ⇒ ค้น `0F 04 00 0B 04` · id `155` = `9B 00` ⇒ ค้น `0F 9B 00 0B 04` · **ไม่เจอ ไม่ได้แปลว่าใบตก** แปลว่าคำทำนายผิด = finding
      (ค) บรรทัดคอนโซล `LANE_A_TRIGGER_VITAL ...` **หลัง `T_START`** ทุกบรรทัด คัดดิบ ๆ · 🔴 **ถ้า id = 4 บรรทัดจะพิมพ์ `... PROP no_responder bytes_out=0`** เพราะ hook override เฉพาะ id 2/3 -- **คำว่า `PROP` เป็นสิ่งที่คาดไว้ ไม่ใช่การหักล้าง** สิ่งที่เป็นผลคือ **ตัวเลข `id=`**
      (ง) **หลัง `T_START` ต้องไม่มีบรรทัด `LANE_A_ENTER_INSTANCE ...`** · มี = finding ชิ้นใหญ่ คัดมาดิบ ๆ
      (จ) `integrity_check` = `ok` · sha256 canonical ไม่เปลี่ยน · ไม่มี traceback หลุด
      🔴 **ชั้นนี้ตอบไม่ได้เลยว่ามีอะไรขึ้นบนจอ**
    client-observable (🔴 **ต้องมีคนนั่งหน้าจอ**):
      (ฉ) **ตอนชนแต่ละครั้ง จอเป็นอย่างไร** -- หนึ่งในสี่คำต่อหนึ่งครั้ง: `หน้าต่างรายงานกัปตัน` / `ข้อความปฏิเสธ (คัดตามตัวอักษร)` / `ข้อความอื่น (คัด)` / `ไม่มีอะไรเลย` · แนบภาพนิ่ง
      (ช) เรือ **หยุด/เด้ง/ทะลุผ่าน** เกาะหรือไม่ -- บรรยายตามที่เห็น **ห้ามเดาสาเหตุ**
      (ซ) **ป้ายชื่อเกาะบนจอ คัดตามตัวอักษร** จากภาพเต็มความละเอียด -- สิ่งเดียวที่ยืนยันว่าก้อนที่ชนคือ Slave Market Island
      (ฌ) 🔴 **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** · เขียน `none` แทนการเว้นว่าง · อ่านจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น** · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067` เป็นเจ้าของคำถามนั้น)
      🔴 **ชั้นนี้ตอบไม่ได้ว่าไบต์ใดออกจากไคลเอนต์**
    🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` เท่านั้น (G-OBS) · หลักฐานครบแต่ไม่มีลายเซ็นคน = `AWAITING-OBSERVER`

- 🔴 **กฎ NEGATIVE vs FAIL (ผู้เทสแค่เลือกกล่องแล้วรายงาน)**:
  A. **เฟรมตอนชนถือ id `4`** ⇒ **PASS** · P1 ถูก · redirect: LANE-A พิจารณาเติมแถว 155 ลง `MEASURED_XYZ`
  B. **มีเฟรมตอนชน แต่ id เป็นเลขอื่น** ⇒ **ยัง PASS** เพราะเกณฑ์คือ hex ไม่ใช่ id · เขียนเลขที่เห็นตรง ๆ · redirect: กฎ "id = เลขฉากปลายทาง" ไม่ขยายถึงแถว 155 ⇒ **ห้ามขยาย `MEASURED_XYZ` จนกว่าจะรู้กฎใหม่**
  C. **ไม่มีเฟรมของ `0x1FB2` เลยทุกจังหวะ แต่หน้าต่างมี opcode อื่นอยู่จริง** ⇒ **PASS พร้อมคำตัดสิน `NO-FRAME`** -- **ผลลบนี้มีค่าเท่าผลบวก** แนบหน้าต่าง hex ที่ไม่มี `12 B2 1F` เป็นหลักฐาน · redirect: การขยาย M2 ต้องไปทาง static RE (สาย `RE-234`) ไม่ใช่ใบ attended ใบที่สาม
  D. **เจอข้อความปฏิเสธเรื่องเลเวล** ⇒ **RESULT ไม่ใช่ FAIL** (P-C · P3) · คัดข้อความตามตัวอักษร + ภาพ + เวลา แล้วเดินใบต่อจนจบ · มีเฟรมมาด้วย = เช็คอยู่ฝั่งสาย · ปฏิเสธแต่ไม่มีไบต์ออกเลย = เช็คอยู่ในไคลเอนต์ล้วน
  E. **หน้าต่างว่างเปล่าจากทุก opcode / หาเกาะไม่เจอ / ไคลเอนต์ตาย / capture ไม่เขียนไฟล์** ⇒ **`NO-RESULT`** พร้อมเหตุผลหนึ่งบรรทัด (capture ตายไม่ใช่ `NO-FRAME`) · **ห้ามเดาแทนไบต์ที่ไม่มี**
  🔴 ทุกกล่องข้างบน **ไม่กระทบสถานะของ `GT-233`** แม้แต่กล่องเดียว

- ที่รู้อยู่แล้วและ **ไม่ใช่ FAIL**: เรือขึ้น **HP -1/1** และไหม้ไฟตลอด · ฉากนี้ไม่มีเฟรม `PLAYER_FACTION` · วัตถุนิ่ง "หันหน้าเข้าหาเรา" เมื่อถูกคลิก · ตำแหน่งกลับจุดเกิดทุกบูต · ไม่มีหน้ารายงานกัปตันที่เกาะ 155 (P2)

- nonclaims:
  1. **ไม่ใช่ใบตัดสินว่าเทียบท่าเกาะ 155 ได้** และ **ไม่ใช่ใบเข้าเกาะ**
  2. **ไม่พิสูจน์ว่า wire scene id ของแถว 155 คือ `4`** -- `wire_scene_id_status` ของแถวนี้ยังเป็น `CANDIDATE` · การชนสำเร็จ **ห้าม** ใช้อัปเกรดฟิลด์นั้น
  3. ไม่พิสูจน์เฟรม **ขาเข้า** ไม่พิสูจน์ปุ่มยืนยัน ไม่พิสูจน์เส้นทางเปลี่ยนฉาก
  4. ไม่ใช่การทดสอบเกตเลเวล และไม่ตัดสินว่าเกตอยู่ฝั่งไหน
  5. **ไม่เกรด `GT-233`**
  6. ไม่ตัดสินความหมายของสีป้ายชื่อ (`RE-067`) · ไม่แตะ HP/vitals ของเรือ (`GT-109`)
  7. ไม่พิสูจน์อะไรที่ต้องรอดข้าม relog (บูตบนสำเนา DB)

- links: `GT-228` (PASS R308 -- ใบพี่ · แหล่ง XYZ/id ของ 153/154) · `GT-233` (บูตที่ใบนี้แนบไปด้วย) · `RE-227` (กลไก provisioning · รัศมี 500) · `RE-234` (ทางสำรองของกล่อง C) · `RE-067` (สีป้าย) · `world_island_dock_table.py` แถว 155 · `world_m2_survey_plan.py` (`MEASURED_XYZ` / `MEASURED_XYZ_BACKUP`) · `lane_hooks/lane_a_island_trigger_log.py` · `BRIDGE_BOOT_PROCEDURE.md` + `ATTENDED_SESSION_RUNBOOK.md`
- result: (ผู้เทสกรอก **แยกสองชั้น · ชั้นไหนไม่ได้วัดเขียน `NOT MEASURED`**: PASS / PASS+`NO-FRAME` / NO-RESULT + กล่อง A-E · branch+commit ที่บูต · `T_START` · เวลาสัมผัสทุกครั้ง · hex ดิบของหน้าต่าง +/-5 วิ · บรรทัด `LANE_A_TRIGGER_VITAL` ทุกบรรทัดหลัง `T_START` (หรือ "ไม่มี") · มี/ไม่มี `LANE_HOOK_REGISTERED` · **HUD `X Y` ทั้งสองครั้ง** · ป้ายชื่อเกาะคัดตามตัวอักษร · สิ่งที่เห็นบนจอตอนชนทีละครั้ง · **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** · ภาพ `S155-*` · sha256 ทุกไฟล์ + canonical ก่อน/หลัง · `integrity_check` · NO-CRASH/CRASH · teardown รันแล้ว · `OBSERVER_CONFIRMED`)

**ผู้เปิดใบ: LANE-A รอบ `qqqtqp` -- ผู้บริโภคผล: LANE-A**
---
