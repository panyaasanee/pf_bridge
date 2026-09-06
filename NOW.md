# NOW — งานที่ต้องมาก่อนทุกอย่าง (สถานะปัจจุบัน · ประวัติใน `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-06 22:41 +07:00 โดย COO (รอบ `2241`: ใบ ×5 · 7 จดหมาย):
- 🔴 **main server แดง** (pin ของ A หลัง `0137`) → reaper ปิด PR ทุกสาย · **ตัวแก้ = A `#957`** · ทุกสาย: ทำงานบนกิ่ง **ไม่เปิด PR เซิร์ฟเวอร์จน main เขียว** (fetch ซ้ำ + รันเทสแถว 2 ก่อนเปิด) · ไม่นับแดงสองรอบ
- 🔴 **PANYA `2142`+`2150`: `RE-155` สีชื่อ NPC+มอน = แถวหุ่นทดลองบูตเดียว · เจ้าของ = B** · ATTENDED+ผู้สมัคร → K **ก่อน 07 ก.ย. 02:00** · B หยุดสร้างโครงสีจนได้ค่า · ตารางสี `2150` = เกณฑ์ทุกใบสี · ห้าม hardcode
- 🔴 **PANYA `1910`: M2 ทาง (ก)** — เซิร์ฟตอบ `TriggerVital 0x1FB2` trigger 2/3 เอง · GT-233 ปิด ห้าม trial `AddSurveyData` · **ห้ามขอเครื่องเจ้าของสำหรับ M2 จนมีเฟรมผู้สมัครอ้าง binary ได้** · `2032` เคาะ 2 งาน (B parser AI_COMBAT+wander · UI แถบ n/327)
- 🔴 **ชื่อไฟล์ใหม่ ≤100 ตัวอักษรรวม `.md`** (PANYA `1910`) · chief ตั้งเกต · ไฟล์เก่าห้าม rename · เครื่อง Panya ปิด 19:0x (heartbeat หยุดตาม) · **`0156` เจ้าของเลื่อนเอง ยังไม่มีเวลาใหม่**
- 🔴 **เลขใบ/เนื้อใบ/พับผล/archive/snapshot = LANE-K** (PANYA `1259`) · chief ห้ามแตะไฟล์คิว · เนื้อใบส่ง `*-TO-K-gt-body-*`

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
- ว่าง — ไม่มีอะไรรอคุณตอนนี้

## รอเครื่องคุณ (บูตเดียวเก็บทุกใบ · คิวจริง = `QUEUE_STATUS_SNAPSHOT.md`)
1. **`RE-155` (B) ใบแรก** (PANYA `2142` ข้อ 4) — แถวหุ่น NPC+916 · รอบล็อก `ATTENDED:` จาก B · ~15 นาที/ชุด ≤3 ชุด
2. **`RE-280` (DB)** — บิต "สวม" · DB ส่ง `ATTENDED:` ให้ K แล้ว (`1737`) · ตอบแล้ว → DB แขน (ข) → `GT-272` รอบสอง
3. `GT-281` ชั้นจอ (หลัง RE-155 · GT-220/223 BLOCKED) · `GT-276` walk-lock CS · `GT-279` ปุ่ม GM · ที่เหลือตาม snapshot
4. **M2: ไม่มีใบให้บูต** จนกว่า UI/A มีเฟรมผู้สมัคร

## กติกาของไฟล์นี้ (ห้ามลบสี่บรรทัดนี้)
- ผู้เขียน: **Panya และ COO เท่านั้น** · คนอื่นเสนอผ่านจดหมายจ่าหน้า `ADDRESSEE: COO`
- **"เสร็จ" ติ๊กได้โดย Panya คนเดียว** — สถานะสูงสุดที่ COO ไปถึงได้คือ `รอเจ้าของยืนยัน` (โค้ดขึ้น main ไม่ใช่ "เสร็จ" · `production_allowed = False` ยังไม่นับว่าขยับ)
- **COO มีหน้าที่เตือน** — ย้ายข้อที่คิดว่าเสร็จขึ้น `รอ Panya ติ๊ก` ทันทีในรอบที่ตัดสิน · ค้างเกิน 6 ชม. = ทวงเธอผ่านช่องทางที่เธอเห็นจริง
- เพดาน **12 KB / 60 บรรทัด** (PANYA `2039` ข้อ 1 · เกต preflight ของ chief) · ข้อที่ปิดแล้ว **ลบทิ้ง** · กฎบ้านอยู่ `AGENTS.md §7` + `prompts/COMMON_LANE_ROUND.md` — NOW ไม่เก็บกฎซ้ำ ยกเว้นที่ยังไม่ลง §7
- 🔴 ยังไม่ลง §7: **`GameMaster.dll` ติดถาวร ห้ามสั่ง rollback** (PANYA `1259` ข้อ 3) · **reaper ปิดเอง**: claim ผี >3 ชม. / `SUPERSEDED-BY:` `DUPLICATE-OF:` (PANYA `1315`) · **ห้าม `rm -r`** (PANYA `1546`) · `ATTENDED:`/`SCOREBOARD:` บังคับ (READY ไม่มี = ไม่ขึ้นรถบัส · ปิดใบ `CANCELLED - covered by`) · `prompts/` ห้ามสายแก้ · grep ที่ห้า `reference_codex_attr/` (`0256`) · `.LANEK-FOLDED.txt` = พับแล้ว (`1451`) · fetch main ซ้ำก่อนเขียนโค้ด**และก่อนเปิด PR** (`1456`/`2241`) · **pin ของสายอื่นแดงตาม docstring = กลับ pin ในใบเดียวกัน** (`2241`) · grep กลไกไม่ใช่การสะกด (`1454`) · เพดานต่อใบ 8,192 B (PANYA `1448`) · **ชื่อไฟล์ ≤100** (PANYA `1910`)
- 🔴 **ตัววัด (PANYA `1259` ข้อ 2)**: `*RESULTS*`/`OBSERVER_CONFIRMED` ไม่มี `.LANEK-FOLDED.txt` >6 ชม. = escalation K
- 🔴 **shared world** (PANYA `1057`/`1140`): โลกต่อฉากใน process แชร์ทุก session · A = registry · B เขียน combat state ลง registry ของ A · DB ไม่รับงานโลก · ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:`
- 🔴 RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING:` (PANYA `1130`) · `KNOWN_RED_MAIN:` **2 แถว** = `skip_census PIN DRIFT test_script_lua_api_instance.py/bridge_lua_scripts pinned 1 observed 0` (Q `#891`) · `test_lane_a_choose_npc_scene1.py …still_missing_at_real_dispatch_today` (A `#957` · COO ลบเมื่อ merge) · ห้ามปิด PR สายอื่นด้วยแถวนี้

## บันไดไมล์สโตน (PANYA `20260904_0233` · ไม่มีกำหนดวัน ห้ามรายงาน "เลยกำหนด" · ผ่าน M(n) ก่อนประกาศ v(n))
- ✅ **M1/v1** ประกาศแล้ว (R249)
- ⏳ **M2 "ออกจากเมืองได้" ← อยู่ตรงนี้ · ทาง (ก) PANYA `1910`**: ตัวบล็อก = เฟรมตอบ `0x1FB2` trigger 2/3 · UI RE `2124` → **A** ต่อสาย (1 รอบ) → ใบ attended · เกณฑ์ผ่าน: ใกล้เกาะ → "รายงานกัปตัน" → ผู้เล่นกด → วาปเข้า **เกาะ 2 และ 3 บนจอ** · ห้าม server ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวล
- **M3 "สนามมีมอนสเตอร์" = P-2** (ชั้นแรก ✅ จอรอ `GT-281` · ชั้นสอง สี = `RE-155` B) · **M4 "ตีได้ตายได้"**: มอนตีกลับ HP ลด · ตาย · ศพไม่ค้าง · เกิดใหม่ (B `GT-224`) · **M5** เก็บได้+รอด relog · **M final** ครบวงจร
- 🔴 **LANE-DB: แขน (ข) STUCK รอ `RE-280` + seam `1452`** · `0328` ชิ้น 1 ✅ · 2 = `RE-282` · 3 `0x309A` RE-blocked (`1455`) · `#896`/`#902` รอ `0156`
- **Q SCRIPT/QUEST** ลำดับระบบ (COO `1846`): 1 flag-quest-state (`1950`/`1951` → chief) → 2 inventory ฝั่งอ่าน (เขียนรอ `RE-280`) → 3 `Player.MobAppear` = **A หลัง P-2** → 4 message-wire → 5 exp-level · Trigger.* 5/17 · Quest.* 1/25
- **LANE-K**: RE-155 body จาก B → ใบแรก (`2241`) · กวาดสารบัญ 34 แถวชี้ใบปิด (`1346` 5ก) + ticket ใหญ่→`tickets/` ≤400 KB/PR · ตั้งเลข RE body `2124`

## งานด่วนตอนนี้
- **หาง P-1** (PANYA `0125`): `#689` บน main · ปิดด้วย `GT-223` (BLOCKED จน `GT-281` จอ) · หนี้ `DropLedgerCell` ข้ามฉาก · ห้ามลบแถว ledger
- **P-2 สีชื่อ (= M3)**: ค่าจริงจาก `RE-155` เท่านั้น · สี = คู่ (คนดู, มอน) `NPCAttr+0x98` (`0254`) · GT สี = chief แต่ง → K ตรวจ NPC+มอนบูตเดียว (`2150`) · ห้าม faction-only/hardcode FontStyleID
- **LANE-GM: `/lv` ✅ → P-3** `GT-279` · `#956` (unlink retry 3 + O_BINARY) ปล่อยไว้ ถูกปิด = cherry-pick (`2241`) · `/speed` ปิดจน (b'') mask (`0545`) · `/warp <n> <x> <y>` ปิดถาวร · `/warp <n>` = spawn (PANYA `1800`)
- **M4 · LANE-B** (ลำดับ `2241`): **0 `RE-155` spawner+ผู้สมัคร+ATTENDED → K** → 1 กู้กิ่ง `0wef26` เมื่อ main เขียว **PR เดียว**: D1 เทสต่อฉาก + D3 **deny-list withheld** (`Bg3001` DEFERRED `1745` · ห้าม merge `mf71tm` ก่อน) + 924/529 ยกเว้นตก + กู้ #936 + bg0002 ลำดับรัน → 2 งาน 1 `2032` parser (ห้ามแตะ wire) → respawn → สมุดโลก · `apply_hp_damage` พักจน Door B · ฆ่าได้ bg0006/7/9/11 `#907`+Bg0010 · respawn 120 s
- **chief ลำดับ (`2241`)**: (1) เกต ≤100 + ยกเว้น (ก) + workflow เรียก preflight จริง → **(2) `gate-windows.yml` พิมพ์ `FAILED/ERROR` ท้าย job (`1921`)** → (3) §7 ≤30 KB + กฎใหม่ 2 ข้อ (`2241`) + reaper ปิด `#886` `#894` `pf_bridge#1493` + D2 ของ B (`1712`) → (4) #948 seed (ข) + ตาราง 18 เทส conftest → (5) GT สี `0256` ตาม `2150` · 🔴 ไม่แตะไฟล์คิว/`prompts/` · เกตห้ามอ่านข้อยกเว้นจาก NOW
- **LANE-A**: **`#957` = ตัวแก้ main แดง ไล่จน merge เล็กที่สุด ถูกปิด = เปิดใหม่ทันที** → `#951` 0x1FB2 → ต่อสายเฟรม `2124` 1 รอบ → ใบ attended → K · promotion 2→1 · **ห้ามส่งเฟรมเดา** (`1955`)
- **LANE-UI**: RE "รายงานกัปตัน" ส่ง A/K แล้ว (`2124`) → **wstring 0x48 PR (`1713`) → งาน 2 `2032` แถบ n/327** · express/community ยังห้าม (`1649`) · **CS**: curriculum 137 = ขอบล่าง ✅ `#952` → ขอบบนจาก quest Lua → `grant_learned_skill` ใต้แฟล็ก · ถัง 1024 ห้ามเปิด RE (`2141`) · `GT-276`/`GT-274` · ห้ามปลดแฟล็กชุด 6 เฟรม

## ห้ามทำจนกว่า P-2 จะปิด
- GT-146 และใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (`0904_2115`) + `GT-274` (`0645`)

## เมื่อไม่มีงานด่วน — ท่อ promotion (PANYA `2039` ข้อ 3)
- 5 ตัวแรก (`docs/PROMOTION_BACKLOG.md`): **1. `remote_player_hypothesis.py` A** · **2. `lane_a_choose_npc_scene1.py` A** · **3. `ground_loot_hypothesis.py` B** · **4. `logout_dialog_open_hypothesis.py` UI** · **5. `skill_attr_hypothesis.py` CS** · `item_operate_res` UI พักรอ `RE-280` · 9 แถว B HP/ตี/ตาย **รอ P-2**
