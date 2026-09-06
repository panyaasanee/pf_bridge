# NOW — งานที่ต้องมาก่อนทุกอย่าง (สถานะปัจจุบัน · ประวัติใน `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-07 01:48 +07:00 โดย COO (รอบ `0148` ใบ ×3):
- ✅ **main เขียว** (`#968`) → เปิด PR ได้ fetch main ซ้ำก่อน · PR ที่ reaper ปิด กู้ด้วย cherry-pick **บนฐาน main ปัจจุบัน หนึ่ง PR ต่อรอบ**
- 🔴 **RE-155 = `GT-288`** (K ตั้ง 01:16) สถานะ `[PENDING]` จน **chief ต่อสาย CORE-REQUEST B `0027`** → B แจ้ง K พลิก READY · `#966` (B) ปิดที่ `skip_census` → กู้พร้อม**กลับ pin skip ในใบเดียว**
- 🔴 **PANYA `1910`: M2 ทาง (ก)** (ดูบันได) · GT-233 ปิด ห้าม trial `AddSurveyData` · **ห้ามขอเครื่องเจ้าของสำหรับ M2 จนมีเฟรมผู้สมัครอ้าง binary**
- 🔴 **ชื่อไฟล์ใหม่ ≤100 รวม `.md`** (PANYA `1910`) · ไฟล์เก่าห้าม rename · เครื่อง Panya เปิด (heartbeat 01:26) · `0156` เลื่อน
- 🔴 **เลขใบ/เนื้อใบ/พับผล/archive/snapshot = LANE-K** (PANYA `1259`) · chief ห้ามแตะไฟล์คิว · เนื้อใบส่ง `*-TO-K-gt-body-*`

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
- **routine K ต้องได้ environment มี git ทุกรอบ** — รอบ `camatf` มีแต่ MCP เขียนไฟล์คิวไม่ได้ (K `2217`)

## รอเครื่องคุณ (บูตเดียวเก็บทุกใบ · คิวจริง = `QUEUE_STATUS_SNAPSHOT.md`)
1. **`GT-288` (B) ใบแรก** — รอ chief ต่อสาย `0027` ก่อน · จอเห็น Fish ชมพู/Eagle เขียว (R322B)
2. `RE-280` **ตอบแล้ว `2258`** → DB แขน (ข) → `GT-272` รอบสอง
3. **GT-281 ✅ (R322B)** → `GT-220`/`GT-223` ปลดล็อก · `GT-279` client ✅ `0x51E9` ×3 **server hook ไม่เขียนไฟล์** → GM · `GT-276` walk-lock CS
4. **M2: ไม่มีใบให้บูต** จนกว่า UI/A มีเฟรมผู้สมัคร

## กติกาของไฟล์นี้ (ห้ามลบสี่บรรทัดนี้)
- ผู้เขียน: **Panya และ COO เท่านั้น** · คนอื่นเสนอผ่านจดหมายจ่าหน้า `ADDRESSEE: COO`
- **"เสร็จ" ติ๊กได้โดย Panya คนเดียว** — สถานะสูงสุดที่ COO ไปถึงได้คือ `รอเจ้าของยืนยัน` (โค้ดขึ้น main ไม่ใช่ "เสร็จ" · `production_allowed = False` ยังไม่นับว่าขยับ)
- **COO มีหน้าที่เตือน** — ย้ายข้อที่คิดว่าเสร็จขึ้น `รอ Panya ติ๊ก` ทันทีในรอบที่ตัดสิน · ค้างเกิน 6 ชม. = ทวงเธอผ่านช่องทางที่เธอเห็นจริง
- เพดาน **12 KB / 60 บรรทัด** (PANYA `2039` · เกต preflight) · ข้อที่ปิดแล้ว **ลบทิ้ง** · กฎบ้านอยู่ `AGENTS.md §7` + `prompts/COMMON_LANE_ROUND.md` — NOW ไม่เก็บกฎซ้ำ ยกเว้นที่ยังไม่ลง §7
- 🔴 ยังไม่ลง §7: **`GameMaster.dll` ติดถาวร ห้ามสั่ง rollback** (PANYA `1259` ข้อ 3) · **reaper ปิดเอง**: claim ผี >3 ชม. / `SUPERSEDED-BY:` `DUPLICATE-OF:` (PANYA `1315`) · **ห้าม `rm -r`** (PANYA `1546`) · `ATTENDED:`/`SCOREBOARD:` บังคับ (READY ไม่มี = ไม่ขึ้นรถบัส) · `prompts/` ห้ามสายแก้ · grep ที่ห้า `reference_codex_attr/` (`0256`) · `.LANEK-FOLDED.txt` = พับแล้ว · fetch main ซ้ำก่อน PR (`1456`) · **pin ของสายอื่นแดงตาม docstring = กลับ pin ในใบเดียวกัน** (`2241`) · grep กลไกไม่ใช่การสะกด (`1454`) · เพดานต่อใบ 8,192 B (PANYA `1448`)
- 🔴 **ตัววัด (PANYA `1259` ข้อ 2)**: `*RESULTS*`/`OBSERVER_CONFIRMED` ไม่มี `.LANEK-FOLDED.txt` >6 ชม. = escalation K
- 🔴 **shared world** (PANYA `1057`/`1140`): โลกต่อฉากใน process แชร์ทุก session · A = registry · B เขียน combat state ลง registry ของ A · DB ไม่รับงานโลก · ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:`
- 🔴 **PANYA `0039` (ka1-A) หลักถาวร: โลกใบเดียว + ฟิลเตอร์มองเห็น NPC ต่อผู้เล่น** · `Player.MobAppear` = **ธงต่อผู้เล่น ไม่ใช่ spawn** · **rank 0 = ธง · rank>0 = ลงโลกร่วม** · ส่งให้คนนี้ = (ไม่ผูกเควส ∧ `n_MOB_APPEAR=1`) ∨ เควสเข้า `s_QUEST_BEGIN/END` ∨ ธง true · **ออกแบบฟิลเตอร์ก่อนแตะ MobAppear** (A) · แถวขัดสคริปต์ → ถาม COO
- 🔴 RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING:` (PANYA `1130`) · `KNOWN_RED_MAIN:` **1 แถว** = `skip_census PIN DRIFT bridge_lua_scripts 1→0` (Q `#891` · `#967` ผ่านแล้ว → chief ลบ) · ห้ามปิด PR สายอื่นด้วยแถวนี้ · **สิทธิ์ฆ่า: ใบเซ็น > derive > ตาราง** ฉากใหม่ต้องมีใบเซ็นหรือ census (`2345`)

## บันไดไมล์สโตน (PANYA `20260904_0233` · ไม่มีกำหนดวัน ห้ามรายงาน "เลยกำหนด" · ผ่าน M(n) ก่อนประกาศ v(n))
- ✅ **M1/v1** ประกาศแล้ว (R249)
- ⏳ **M2 "ออกจากเมืองได้" ← อยู่ตรงนี้ · ทาง (ก) PANYA `1910`**: ตัวบล็อก = เฟรมตอบ `0x1FB2` trigger 2/3 · UI RE `2124` → **A** ต่อสาย (1 รอบ) → ใบ attended · เกณฑ์ผ่าน: ใกล้เกาะ → "รายงานกัปตัน" → ผู้เล่นกด → วาปเข้า **เกาะ 2 และ 3 บนจอ** · ห้าม server ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวล
- **M3 "สนามมีมอนสเตอร์" = P-2** (ชั้นแรก+จอ ✅ GT-281 · ชั้นสอง สี = `GT-288` รอ `0027`) · **M4 "ตีได้ตายได้"**: มอนตีกลับ HP ลด · ตาย · ศพไม่ค้าง · เกิดใหม่ (B `GT-224`) · **M5** เก็บได้+รอด relog · **M final** ครบวงจร
- 🔴 **LANE-DB**: (1) กู้ `skill_points_null_audit` cherry-pick `f51b94e`+`849bf2a` บนฐานปัจจุบัน (COO `0148`) → (2) แขน (ข) seam `1452` (`RE-280` ตอบ `2258`) · `0328` ชิ้น 1 ✅ · 2 = `RE-282` ตอบ `2322` · 3 `0x309A` RE-blocked (`1455`) · `#896`/`#902` รอ `0156` · ใบสร้าง A/DB (R322B): ออก 126 คืน HP ตัวละคร · BoatHealth ≠ -1
- **Q SCRIPT/QUEST** ลำดับระบบ (COO `1846`): 1 flag-quest-state (`1950`/`1951` → chief) → 2 inventory ฝั่งอ่าน → 3 `Player.MobAppear` = **A หลัง P-2** → 4 message-wire → 5 exp-level · `RE-285` ตอบ `2303` · `CastSkill*` encoder = CS ทำเมื่อ Q ขอ (`2345`)
- **LANE-K**: พับ R322B `0123` · GT-220/223 ปลดล็อก · ticket ใหญ่→`tickets/` ≤400 KB/PR

## งานด่วนตอนนี้
- **หาง P-1** (PANYA `0125`): ปิดด้วย `GT-223` (ปลดล็อกแล้ว) · หนี้ `DropLedgerCell` ข้ามฉาก · ห้ามลบแถว ledger
- **P-2 สีชื่อ (= M3)**: ค่าจริงจาก `RE-155`/`GT-288` เท่านั้น · สี = คู่ (คนดู, มอน) `NPCAttr+0x98` (`0254`) · GT สี = chief แต่ง → K (`2150`) · ห้าม faction-only/hardcode FontStyleID
- **LANE-GM**: `#970` (กู้ `#962`) รอ merge → P-3 `GT-279`: **ปุ่ม "ปฏิบัติ" ส่ง `0x51E9` จริง แต่ `capture_raw_gm_command` ไม่เขียนไฟล์** → หาทางเฟรม · `RE-278` `BasicAttr` บิต `0x0002` **ส่ง mask ทั้งก้อน** · `/speed` ปิดจน (b'') mask (`0545`) · `/warp <n>` = spawn เท่านั้น (PANYA `1800`)
- **M4 · LANE-B** (`2345`+`0148`): **0 กู้ `#966` + pin skip ในใบเดียว** → 1 **PR เดียว**: D1(ก) bg0001 อ้าง `0041` + D2 derive ปฏิเสธข้ามฉาก + tripwire ฉากที่ 13 + D3 deny-list (`1745`) + 924/529 + bg0002 ลำดับรัน → **1b R322B: `bg0002.HOSTILE_PLACEMENTS` 17 แถว vs roster rank-1 12 ตัว → regenerate จากกฎบน roster จริง** → 2 `2032` parser (ห้ามแตะ wire) → respawn 120 s → `1648` → สมุดโลก · `apply_hp_damage` พักจน Door B
- **chief ลำดับ (`0148`)**: **(0) CORE-REQUEST B `0027` ต่อสาย `PF_NAME_COLOUR_SWEEP` (บล็อก M3)** → (1) `bridge-preflight` บล็อกจริง (R378) → (1b) `2345`: `pytest` bg0002 → B · `GT-079` → K · ตอบ GM `0724`/`1029` → **(2) `gate-windows.yml`: failure-detail R350 ไม่พิมพ์ (run `34045847454`) + `FAILED/ERROR` ท้าย job (`1921`)** → (3) §7 ≤30 KB + กฎ `2241`+`2345`+`0039` + reaper ปิด `#886` `#894` `pf_bridge#1493` → (4) #948 seed (ข) + conftest → (5) GT สี `0256` · **ตอบ GM `1215` GM-063**
- **LANE-A**: `#969` รอ merge → ต่อสายเฟรม `2124` 1 รอบ → ใบ attended → K · promotion 2→1 · **ห้ามส่งเฟรมเดา** (`1955`)
- **LANE-UI**: `#967` ✅ → **กู้ `#961` ครั้งเดียวบนฐานปัจจุบัน + census ไม่ผูก path/newline** → งาน 2 `2032` แถบ n/327 · express/community ยังห้าม (`1649`) · **CS**: `#964` ✅ → `grant_learned_skill` ใต้แฟล็ก รอ DB caller · `GT-276`/`GT-274` · ห้ามปลดแฟล็กชุด 6 เฟรม

## ห้ามทำจนกว่า P-2 จะปิด
- GT-146 และใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (`0904_2115`) + `GT-274` (`0645`)

## เมื่อไม่มีงานด่วน — ท่อ promotion (PANYA `2039` ข้อ 3)
- 5 ตัวแรก (`docs/PROMOTION_BACKLOG.md`): **1. `remote_player_hypothesis.py` A** · **2. `lane_a_choose_npc_scene1.py` A** · **3. `ground_loot_hypothesis.py` B** · **4. `logout_dialog_open_hypothesis.py` UI** · **5. `skill_attr_hypothesis.py` CS** · `item_operate_res` UI ปลดได้ · 9 แถว B HP/ตี/ตาย **รอ P-2**
