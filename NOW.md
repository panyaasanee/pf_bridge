# NOW — งานที่ต้องมาก่อนทุกอย่าง (สถานะปัจจุบันเท่านั้น · ประวัติใน `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-06 18:46 +07:00 โดย COO (รอบ `1841`: ใบ `1846` ×4):
- 🔴 **เครื่อง Panya เปิดแล้ว 18:16 · สะพาน push ได้ แต่ pull เข้าเครื่องติด** (`SYNC_STUCK` 1816–1844): ชื่อไฟล์ COO ยาวเกิน Windows + cherry-pick ค้างบนเครื่อง ⇒ ใบ/จดหมายจาก cloud ไม่ถึงเครื่อง · แก้ได้ที่เครื่องเท่านั้น (`1846` ถึง ka1-A) · COO ชื่อไฟล์ ≤100 ตั้งแต่รอบนี้
- 🔴 **PANYA-ORDER `0156`: 23:00 คืนนี้เจ้าของเลื่อนเอง (`1645`/`1651`) ยังไม่มีเวลาใหม่**: แขน (ข) STUCK รอ `RE-280` บิต "สวม" + จุดเสียบ chief (`1452`) · **COO รายงานตามจริง 23:41**
- 🔴 **P-2 ชั้นแรก: โค้ดบน main แล้ว** (`#927` · A `1633`): faction ทุก login scene · เหลือยืนยันบนจอ = `GT-281` READY (K `1729`) · GT-220/223 BLOCKED จน `GT-281` ผ่าน
- 🔴 **เลขใบ/วางเนื้อใบ/พับผล/archive/snapshot = LANE-K** (PANYA `1259`) — chief ห้ามแตะไฟล์คิว (`1345`) · เนื้อใบใหม่ทุกสายส่ง `*-TO-K-gt-body-*`
- 🔴 **R364 ข้อ 2**: READY ไม่มี `ATTENDED:` = ไม่ขึ้นรถบัส — เติมใบตัวเอง**ก่อนงานใหม่** · ปิดใบใช้ `CANCELLED - covered by` (`0747`) · Scoreboard วัด 21:41

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
1. **สะพานฝั่งเครื่องคุณ pull ไม่ได้** — ใน clone `pf_bridge` บนเครื่อง: `git status` → `git cherry-pick --abort` → `git config core.longpaths true` · แล้ว sync รอบถัดไปจะ ff เอง (`1846` ถึง ka1-A)

## รอเครื่องคุณ (บูต attended หนึ่งครั้งเก็บทุกใบ `ATTENDED:` · คิวจริง = `QUEUE_STATUS_SNAPSHOT.md`)
1. **`GT-233` M2 provisioning trial — บูตได้ทันที** · env `PF_M2_SURVEY_TRIAL=1` · 🔴 นัดเดียวไม่มี BACKUP · อ่านผลตามบล็อก D1 ในใบ · **จดเลเวลตัวละครลงผล**
2. **`RE-280` (DB) ก่อน RE ใบอื่น** — บิต "สวม" · DB ส่ง `ATTENDED:` ≤5 บรรทัดให้ K (`1651`) · ตอบแล้ว → DB แขน (ข) → `GT-272` รอบสอง
3. `GT-281` faction READY · `GT-276` walk-lock CS · `GT-279` ปุ่ม GM · ที่เหลือตาม snapshot

## กติกาของไฟล์นี้ (ห้ามลบสี่บรรทัดนี้)
- ผู้เขียน: **Panya และ COO เท่านั้น** · คนอื่นเสนอผ่านจดหมายจ่าหน้า `ADDRESSEE: COO`
- **"เสร็จ" ติ๊กได้โดย Panya คนเดียว** — สถานะสูงสุดที่ COO ไปถึงได้คือ `รอเจ้าของยืนยัน` (โค้ดขึ้น main ไม่ใช่ "เสร็จ" · `production_allowed = False` ยังไม่นับว่าขยับ)
- **COO มีหน้าที่เตือน** — ย้ายข้อที่คิดว่าเสร็จขึ้น `รอ Panya ติ๊ก` ทันทีในรอบที่ตัดสิน · ค้างเกิน 6 ชม. = ทวงเธอผ่านช่องทางที่เธอเห็นจริง
- เพดาน **12 KB / 60 บรรทัด** (PANYA `2039` ข้อ 1 · เกต preflight ของ chief) · ข้อที่ปิดแล้ว **ลบทิ้ง** · กฎบ้านอยู่ `AGENTS.md §7` + `prompts/COMMON_LANE_ROUND.md` — NOW ไม่เก็บกฎซ้ำ ยกเว้นที่ยังไม่ลง §7
- 🔴 ยังไม่ลง §7 (chief `1457` ข้อ 5): **`GameMaster.dll` ติดถาวร ห้ามสั่ง rollback** (PANYA `1259` ข้อ 3) · **reaper ปิดเอง 2 ประเภท** claim ผี >3 ชม. / `SUPERSEDED-BY:` `DUPLICATE-OF:` (PANYA `1315`) · **ห้าม `rm -r`** ใช้ `mktemp -d` (PANYA `1546`) · `ATTENDED:`/`SCOREBOARD:` บังคับ · `prompts/` ห้ามสายแก้ · grep ที่ห้า `notes_to_chief/reference_codex_attr/` (`0256`) · **`.LANEK-FOLDED.txt` = พับแล้ว / `.CONSUMED.txt` สายอื่นขึ้น `NOT-FOLDED:`** (`1451`) · fetch main ซ้ำก่อนเขียนโค้ด (`1456`) · grep กลไกไม่ใช่การสะกด (`1454`) · เพดานต่อใบ 8,192 B (PANYA `1448`)
- 🔴 **ตัววัดใหม่ (PANYA `1259` ข้อ 2)**: จดหมายผล `*RESULTS*`/`OBSERVER_CONFIRMED` ไม่มี `.LANEK-FOLDED.txt` ค้าง >6 ชม. = escalation สาย K · ขนาดไฟล์รายงานเป็น**ไบต์**
- 🔴 **shared world** (PANYA `1057`/`1140`): โลกต่อฉากอยู่ใน process แชร์ทุก session · A = world registry · B เขียน combat state ลง registry ของ A · DB ไม่รับงานโลก · ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:`
- 🔴 RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING:` (PANYA `1130`) · `KNOWN_RED_MAIN:` **1 แถว** = `skip_census PIN DRIFT test_script_lua_api_instance.py/bridge_lua_scripts pinned 1 observed 0` (Q `#891` รอ census) · ห้ามปิด PR สายอื่นด้วยแถวนี้

## บันไดไมล์สโตน (PANYA `20260904_0233` · ไม่มีกำหนดวัน ห้ามรายงาน "เลยกำหนด" · ผ่าน M(n) ก่อนจึงประกาศ v(n) · `SERVER_VERSIONS.md` ของ chief)
- ✅ **M1/v1** ประกาศแล้ว (R249)
- ⏳ **M2 "ออกจากเมืองได้" — โปรเจกต์อยู่ตรงนี้ · ตัวบล็อกโค้ด 0 · GT-233 อยู่บนเครื่องคุณ**: `#857`/`#865` บน main · `RE-270` ✅ · เกณฑ์ผ่าน: ใกล้เกาะ → "รายงานกัปตัน" → ผู้เล่นกด → วาปเข้า **เกาะ 2 และ 3 บนจอ** · ห้าม server ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวล server · ชั้นถัดไป = Trigger.* ของ Q
- **M3 "สนามมีมอนสเตอร์" = P-2** (ชั้นแรก faction → A `1347` · ชั้นสอง สี/attr → B) · **M4 "ตีได้ตายได้"** สี่ข้อ: มอนตีกลับ HP ลดจริง · ตายถูกต้อง · ศพไม่ค้าง · เกิดใหม่ (LANE-B · `GT-224`) · **M5** เก็บได้+รอด relog · **M final** ครบวงจร
- 🔴 **LANE-DB: แขน (ข) STUCK รอ `RE-280` + seam `1452` (`1549`/`1603`)** · PLAYER/CHARACTER (`0328`): ชิ้น 1 ✅ · ชิ้น 2 = `RE-282` · ชิ้น 3 `0x309A` RE-blocked (`1455`) · `#896`/`#902` ไม่รันบน DB จริงก่อน `0156` ปิด (`0749`)
- **Q SCRIPT/QUEST**: `LUA_HOST_API_MAP` บน main (`#938`) ✅ · **ลำดับระบบ (COO `1846`)**: 1 flag-quest-state (Q รอบถัดไป + CORE-REQUEST ตาราง) → 2 inventory ฝั่งอ่าน (ฝั่งเขียนรอ `RE-280`) → 3 `Player.MobAppear` = **LANE-A หลัง P-2** → 4 message-wire → 5 exp-level · Trigger.* 5/17 · Quest.* 1/25
- **LANE-K เสมียนคิว**: หนี้ folded 0 · ต่อ: ข้อ ข ใบยาว→`tickets/` ยาวสุดก่อน ≤400 KB/PR · archive ใต้เพดาน · GT 72% · RE 74%

## งานด่วนตอนนี้ (P-1/P-2/P-3 ซ้อนกับบันไดข้างบน)
- **หาง P-1** (PANYA `0125`): `#689` บน main · ปิดด้วย `GT-223` บนจอ (BLOCKED จน faction ขึ้น main) · หนี้ `DropLedgerCell` ข้ามฉาก · ห้ามลบแถว ledger
- **P-2 สีชื่อมอน (= M3)**: ส้ม/แดง/เทา ห้ามชมพู + attr/relation ถูก (B) · สี = คู่ (คนดู, มอน) ผ่าน `NPCAttr+0x98` (`0254`) · GT สี = chief แต่ง ส่ง K · GM tripwire คลุม `mob_viewer_link.py` (`0255`) · ห้าม faction-only / hardcode FontStyleID
- **LANE-GM: `/lv` = GT-277 ✅ → P-3** ปุ่ม GM 3 หน้า = `GT-279` (K ตั้งแล้ว) · GM-063 ถอน (`1454`) · `/speed` ปิดจน (b'') mask ล็อกอิน (`0545`) · `/warp <n> <x> <y>` ปิดถาวร · `/warp <n>` ฉากเดียวกัน = spawn (PANYA `1800`)
- **M4 · LANE-B**: **งานแรก = ตาราง diff กฎ `MOBS` vs ต่อฉาก (`1648`) รวมทะเล rank-only (`1643` ยืนยัน) + เกต CI คีย์ทาง 2 (`1712`)** · Bg3001 ฆ่า = DEFERRED จนตารางมา (`1644`) · caller `apply_hp_damage` พักจน Door B ส่งจริง · ฆ่าได้ bg0006/7/9/11 `#907` + Bg0010 ×6 · respawn 120 s · เทสตีมอนรอ `GT-281`
- **chief ลำดับ (`1745` แทน `1546`)**: (0) เหลือ = เช็ค `.CONSUMED` stub + เกตโต ≤50,000 B/PR (D11) → (1) **A `0137` คู่ `latches_spent` ทั้งคู่หรือไม่เอาเลย (`1633`)** · DB `1452` รอ `RE-280` ไม่นับ escalation → (2) reaper + concurrency เท็จ + ตอบ D2 ของ B (`1712`) → (3) §7 → (4) เนื้อใบ → K: GT สี `0256` · `GT-079`/`080` → (5) D1 `0252` · STATIC bg0010 · `CHIEF_CONTINUATION.md` ใต้เพดานก่อน 21:41 · 🔴 ไม่แตะไฟล์คิว
- **LANE-UI**: **รอบถัดไป = PR เดียว migrate wstring 0x48 ใน mail/party/trade (`1713`) · express/community ยังห้ามต่อสาย (`1649`)** · promotion ข้อ 4 รอบถัดจากนั้น · `#860` เปิด (RE-266) → GT-184/186 · **CS**: walk-lock = `GT-276` attended · `GT-274` คู่ B · ไม่มี startable = ปิดใน 10 นาที (`1456`) · ห้ามปลดแฟล็กชุด 6 เฟรม

## ห้ามทำจนกว่า P-2 จะปิด
- GT-146 และใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (Panya `0904_2115`) + `GT-274` (`0645`)

## เมื่อไม่มีงานด่วน — ท่อ promotion (PANYA `2039` ข้อ 3)
- 4 ตัวแรก (`skill_attr` ออก `1348`): **1. `remote_player_hypothesis.py` A** (`#1476` ขึ้นแล้ว รอ GT) · **2. `lane_a_choose_npc_scene1.py` A** · **3. `ground_loot_hypothesis.py` B** · **4. `item_operate_res_hypothesis.py` UI** · 9 แถว B HP/ตี/ตาย **รอ P-2** · ใบ GT `ATTENDED:` ส่ง K
