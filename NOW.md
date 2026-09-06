# NOW — งานที่ต้องมาก่อนทุกอย่าง (สถานะปัจจุบัน · ประวัติใน `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-06 21:41 +07:00 โดย COO (รอบผู้บริหาร `2141`: ใบ ×8 · M2 ไม่ขยับ · 12 ชม. DONE 0 แถว):
- 🔴 **PANYA-DECISION `2032` เคาะ 2 งาน · COO จัดคิว `2047`**: B ตัวแปลกฎ AI_COMBAT+wander · UI แถบ "เฟรมที่ server รู้จัก n/327"
- 🔴 **PANYA-ORDER `1910`: M2 ไปทาง (ก)** — เซิร์ฟตอบ `TriggerVital 0x1FB2` trigger 2/3 เอง · GT-233 ปิด ห้าม trial `AddSurveyData` · **ห้ามขอเครื่องเจ้าของสำหรับ M2 จนมีเฟรมผู้สมัครอ้าง binary ได้**
- 🔴 **ชื่อไฟล์ใหม่ทุกไฟล์ใน pf_bridge ≤100 ตัวอักษรรวม `.md`** (PANYA `1910`) · chief ตั้งเกต · ไฟล์เก่าห้าม rename
- เครื่อง Panya ปิด 19:0x · heartbeat หยุดตามเครื่อง ไม่ใช่สะพานตาย
- 🔴 **PANYA-ORDER `0156` เจ้าของเลื่อนเอง ยังไม่มีเวลาใหม่**
- 🔴 **เลขใบ/เนื้อใบ/พับผล/archive/snapshot = LANE-K** (PANYA `1259`) — chief ห้ามแตะไฟล์คิว · เนื้อใบใหม่ส่ง `*-TO-K-gt-body-*`
- 🔴 READY ไม่มี `ATTENDED:` = ไม่ขึ้นรถบัส (R364) · ปิดใบใช้ `CANCELLED - covered by`

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
- ว่าง — ไม่มีอะไรรอคุณตอนนี้

## รอเครื่องคุณ (บูตครั้งเดียวเก็บทุกใบ `ATTENDED:` · คิวจริง = `QUEUE_STATUS_SNAPSHOT.md`)
1. **`RE-280` (DB) ก่อน RE ใบอื่น** — บิต "สวม" · DB ส่ง `ATTENDED:` ให้ K แล้ว (`1737`) · ตอบแล้ว → DB แขน (ข) → `GT-272` รอบสอง
2. `GT-281` ชั้นจอ (สีชื่อมอน · GT-220/223 BLOCKED จนผ่าน) · `GT-276` walk-lock CS · `GT-279` ปุ่ม GM · ที่เหลือตาม snapshot
3. **M2: ไม่มีใบให้บูต** จนกว่า UI/A มีเฟรมผู้สมัคร

## กติกาของไฟล์นี้ (ห้ามลบสี่บรรทัดนี้)
- ผู้เขียน: **Panya และ COO เท่านั้น** · คนอื่นเสนอผ่านจดหมายจ่าหน้า `ADDRESSEE: COO`
- **"เสร็จ" ติ๊กได้โดย Panya คนเดียว** — สถานะสูงสุดที่ COO ไปถึงได้คือ `รอเจ้าของยืนยัน` (โค้ดขึ้น main ไม่ใช่ "เสร็จ" · `production_allowed = False` ยังไม่นับว่าขยับ)
- **COO มีหน้าที่เตือน** — ย้ายข้อที่คิดว่าเสร็จขึ้น `รอ Panya ติ๊ก` ทันทีในรอบที่ตัดสิน · ค้างเกิน 6 ชม. = ทวงเธอผ่านช่องทางที่เธอเห็นจริง
- เพดาน **12 KB / 60 บรรทัด** (PANYA `2039` ข้อ 1 · เกต preflight ของ chief) · ข้อที่ปิดแล้ว **ลบทิ้ง** · กฎบ้านอยู่ `AGENTS.md §7` + `prompts/COMMON_LANE_ROUND.md` — NOW ไม่เก็บกฎซ้ำ ยกเว้นที่ยังไม่ลง §7
- 🔴 ยังไม่ลง §7: **`GameMaster.dll` ติดถาวร ห้ามสั่ง rollback** (PANYA `1259` ข้อ 3) · **reaper ปิดเอง**: claim ผี >3 ชม. / `SUPERSEDED-BY:` `DUPLICATE-OF:` (PANYA `1315`) · **ห้าม `rm -r`** ใช้ `mktemp -d` (PANYA `1546`) · `ATTENDED:`/`SCOREBOARD:` บังคับ · `prompts/` ห้ามสายแก้ · grep ที่ห้า `notes_to_chief/reference_codex_attr/` (`0256`) · **`.LANEK-FOLDED.txt` = พับแล้ว / `.CONSUMED.txt` สายอื่นขึ้น `NOT-FOLDED:`** (`1451`) · fetch main ซ้ำก่อนเขียนโค้ด (`1456`) · grep กลไกไม่ใช่การสะกด (`1454`) · เพดานต่อใบ 8,192 B (PANYA `1448`) · **ชื่อไฟล์ ≤100** (PANYA `1910`)
- 🔴 **ตัววัดใหม่ (PANYA `1259` ข้อ 2)**: จดหมายผล `*RESULTS*`/`OBSERVER_CONFIRMED` ไม่มี `.LANEK-FOLDED.txt` ค้าง >6 ชม. = escalation สาย K
- 🔴 **shared world** (PANYA `1057`/`1140`): โลกต่อฉากอยู่ใน process แชร์ทุก session · A = world registry · B เขียน combat state ลง registry ของ A · DB ไม่รับงานโลก · ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:`
- 🔴 RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING:` (PANYA `1130`) · `KNOWN_RED_MAIN:` **2 แถว** = `skip_census PIN DRIFT test_script_lua_api_instance.py/bridge_lua_scripts pinned 1 observed 0` (Q `#891` รอ census) · `test_lane_a_choose_npc_scene1.py …still_missing_at_real_dispatch_today` (A กลับ assertion `2141` · ลบเมื่อ merge) · ห้ามปิด PR สายอื่นด้วยแถวนี้

## บันไดไมล์สโตน (PANYA `20260904_0233` · ไม่มีกำหนดวัน ห้ามรายงาน "เลยกำหนด" · ผ่าน M(n) ก่อนประกาศ v(n))
- ✅ **M1/v1** ประกาศแล้ว (R249)
- ⏳ **M2 "ออกจากเมืองได้" ← อยู่ตรงนี้ · ทาง (ก) PANYA `1910`**: ตัวบล็อก = เฟรมตอบ `0x1FB2` trigger 2/3 · UI ส่ง RE เฟรมผู้สมัครแล้ว (`2124`) → **A** ต่อสาย (1 รอบ) → ใบ attended ใหม่ · เกณฑ์ผ่าน: ใกล้เกาะ → "รายงานกัปตัน" → ผู้เล่นกด → วาปเข้า **เกาะ 2 และ 3 บนจอ** · ห้าม server ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวล
- **M3 "สนามมีมอนสเตอร์" = P-2** (ชั้นแรก faction wire ✅ จอรอ `GT-281` · ชั้นสอง สี/attr → B) · **M4 "ตีได้ตายได้"**: มอนตีกลับ HP ลดจริง · ตายถูกต้อง · ศพไม่ค้าง · เกิดใหม่ (B · `GT-224`) · **M5** เก็บได้+รอด relog · **M final** ครบวงจร
- 🔴 **LANE-DB: แขน (ข) STUCK รอ `RE-280` + seam `1452`** · `0328` ชิ้น 1 ✅ · 2 = `RE-282` · 3 `0x309A` RE-blocked (`1455`) · `#896`/`#902` รอ `0156`
- **Q SCRIPT/QUEST**: **ลำดับระบบ (COO `1846`)**: 1 flag-quest-state (CORE-REQUEST `1950`/`1951` → chief) → 2 inventory ฝั่งอ่าน (เขียนรอ `RE-280`) → 3 `Player.MobAppear` = **A หลัง P-2** → 4 message-wire → 5 exp-level · Trigger.* 5/17 · Quest.* 1/25
- **LANE-K**: GT-233/GT-074 → `tickets/` แล้ว · รอบถัดไป = กวาดสารบัญ 34 แถวชี้ใบปิด (`1346` 5ก) + ticket ใหญ่ถัดไป→`tickets/` ≤400 KB/PR · ตั้งเลข RE body `2124`

## งานด่วนตอนนี้ (P-1/P-2/P-3 ซ้อนกับบันไดข้างบน)
- **หาง P-1** (PANYA `0125`): `#689` บน main · ปิดด้วย `GT-223` (BLOCKED จน `GT-281` จอ) · หนี้ `DropLedgerCell` ข้ามฉาก · ห้ามลบแถว ledger
- **P-2 สีชื่อมอน (= M3)**: ส้ม/แดง/เทา ห้ามชมพู + attr/relation ถูก (B) · สี = คู่ (คนดู, มอน) ผ่าน `NPCAttr+0x98` (`0254`) · GT สี = chief แต่ง ส่ง K · GM tripwire คลุม `mob_viewer_link.py` · ห้าม faction-only / hardcode FontStyleID
- **LANE-GM: `/lv` ✅ → P-3** ปุ่ม GM 3 หน้า = `GT-279` · หลังเกต Windows เขียว = `_best_effort_unlink` retry 3 + doc (`2047`) · `/speed` ปิดจน (b'') mask ล็อกอิน (`0545`) · `/warp <n> <x> <y>` ปิดถาวร · `/warp <n>` ฉากเดียวกัน = spawn (PANYA `1800`)
- **M4 · LANE-B**: `#946` derive ต่อฉาก ✅ D1 ✅ (`2047`) · **รอบถัดไป = adversary `0wef26` → PR `1955`: ครอบครัวจาก registry A + ตาราง `1824` เป็น test + กู้ #936** → เทส bg0002 แดงตามลำดับรัน (`2141`) → P-2 ชั้นสอง · นาฬิกา respawn → สมุดโลก (`2141` หลังคิว) → รอจอ = งาน 1 `2032` (parser ก่อน ห้ามแตะ wire) · Bg3001 DEFERRED จน key gate · `apply_hp_damage` พักจน Door B ส่งจริง · ฆ่าได้ bg0006/7/9/11 `#907` + Bg0010 · respawn 120 s
- **chief ลำดับ (`2141`)**: (1) เกต ≤100 + ยกเว้น (ก) basename บน base + workflow เรียก `pf_gate_preflight.py` จริง → (1b) #948 seed (ข) + ตาราง 18 เทส conftest → (2) `gate-windows.yml` พิมพ์ `FAILED/ERROR` ท้าย job (`1921`) → (3) reaper + concurrency เท็จ + D2 ของ B (`1712`) · reaper ปิด `#886` (DUP #885 23 ชม.) `#894` draft `pf_bridge#1493` → (4) §7 ≤30 KB → (5) GT สี `0256` · `GT-079`/`080` → K · D1 `0252` · 🔴 ไม่แตะไฟล์คิว/`prompts/`
- **LANE-A**: `#951` ตาราง 0x1FB2 เปิดแล้ว · **รอบถัดไป = กลับ assertion เทส scene1 ที่แดงบน main (`2141` · `0137` ลงแล้ว)** → promotion 2 → 1 · **ห้ามส่งเฟรมเดา** (`1955`)
- **LANE-UI**: RE "รายงานกัปตัน" ส่ง A/K แล้ว (`2124`) → **wstring 0x48 PR (`1713`) → งาน 2 `2032` แถบ n/327 (`2047`)** · express/community ยังห้าม (`1649`) · `#860` → GT-184/186 · **CS**: curriculum 137 = ขอบล่าง ✅ `#952` → ขอบบนจาก quest Lua → ต่อ `grant_learned_skill` ใต้แฟล็ก · ถัง 1024 ไม่ประกาศความหมาย ห้ามเปิด RE (`2141`) · `GT-276` · `GT-274` คู่ B · ห้ามปลดแฟล็กชุด 6 เฟรม

## ห้ามทำจนกว่า P-2 จะปิด
- GT-146 และใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (`0904_2115`) + `GT-274` (`0645`)

## เมื่อไม่มีงานด่วน — ท่อ promotion (PANYA `2039` ข้อ 3)
- 5 ตัวแรก (`2141` จาก `docs/PROMOTION_BACKLOG.md` 18 แถว): **1. `remote_player_hypothesis.py` A** (`#1476` รอ GT) · **2. `lane_a_choose_npc_scene1.py` A** · **3. `ground_loot_hypothesis.py` B** · **4. `logout_dialog_open_hypothesis.py` UI** · **5. `skill_attr_hypothesis.py` CS** · `item_operate_res` UI พักรอ `RE-280` (ห้ามถอด identity guard) · 9 แถว B HP/ตี/ตาย **รอ P-2**
