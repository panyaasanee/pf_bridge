# NOW — งานที่ต้องมาก่อนทุกอย่าง (สถานะปัจจุบันเท่านั้น · เพดาน 12 KB / 60 บรรทัด · ประวัติอยู่ในจดหมาย `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-06 11:52 +07:00 โดย COO (รอบ `1141`: ใบ `1145`-`1150` · chief archive ก่อน `1146` · ใบฆ่า 4 ฉาก `1150`):
- 🔴 **PANYA-ORDER `0155`/`0156` เส้นตาย 14:00**: **GM `/lv <n>` บน main** (`#885` · เพดาน 254 · ใบ GT รอ archive `1145`) · **DB สวมอาวุธ** แขน (ก) `#883` ✅ · แขน (ข) `RE-272`/`GT-272` วางแล้ว **รอ capture บนเครื่องคุณ (ค้าง 7 ชม.)** ⇒ DB โค้ด op 5 · ปิดเฉพาะ**บนจอ + คงหลัง relog** · **COO รายงาน 14:41**
- **GT-233 บูตได้** (`0252` · ผู้สมัคร (1,126)) · census `#906` บน main ✅ · 🔴 **เลข GT ที่ค้างทุกใบวางไม่ได้จน chief archive ไฟล์คิว = งาน (0) ก่อน 14:00 (`1146`)**
- 🔴 **R364 ข้อ 2**: READY ไม่มี `ATTENDED:` = ไม่ขึ้นรถบัส — เติมใบตัวเอง**ก่อนงานใหม่** (เหลือ ~11: GM 3 · E 3 · UI 2 · CS/DB 1 · A/B ครบ) · `bridgesize` แดงจากบล็อกนี้ = known-red (`0745`) · ปิดใบใช้ `CANCELLED - covered by` (`0747`)
- สะพานเดิน `11:40` · Scoreboard 40 แถว **DONE 1** (server merge 43/12 ชม. · CS COMING 0 ⇒ `1044`) · PR เปิด server `#908` GM ปกติ

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
1. **เคาะสายที่ 9** ใบ `1042`: (ก) LANE-K เสมียนคิว (COO แนะนำ) / (ข) DB ถือชั่วคราว / (ค) ไม่ทำ
2. **ปิดมือ 3 ใบ**: `pf_bridge#1440` claim ผี · `server#894` ถูกแทนด้วย `#906` · `server#886` duplicate `#885`

## รอเครื่องคุณ (บูต attended หนึ่งครั้งเก็บทุกใบที่มี `ATTENDED:`)
1. **`GT-233` M2 provisioning trial — บูตได้ทันที** · env `PF_M2_SURVEY_TRIAL=1` ใบแรกของรถบัส · 🔴 นัดเดียวไม่มี BACKUP · อ่านผลตามบล็อก D1 ในใบ (เงียบ ≠ ทฤษฎีผิด) · **จดเลเวลตัวละครลงผล** · `RE-270` ขนาน
2. **`GT-272`** สวมอาวุธ op 5 (DB · `0156` แขน ข) — capture `RE-272` ก่อน แล้วโค้ด DB ขึ้น main · **`GT-269`** GMUI + `GT-268` พ่วงท้ายได้
3. GT-266/257/255/230/243 · RE-235/237/261 รันแล้ว (R320) ผล `0155` รอ chief ปิด/แยกใบ

## กติกาของไฟล์นี้ (ห้ามลบสี่บรรทัดนี้)
- ผู้เขียน: **Panya และ COO เท่านั้น** · คนอื่นเสนอผ่านจดหมายจ่าหน้า `ADDRESSEE: COO`
- **"เสร็จ" ติ๊กได้โดย Panya คนเดียว** — สถานะสูงสุดที่ COO ไปถึงได้คือ `รอเจ้าของยืนยัน` (โค้ดขึ้น main ไม่ใช่ "เสร็จ" · `production_allowed = False` ยังไม่นับว่าขยับ)
- **COO มีหน้าที่เตือน** — ย้ายข้อที่คิดว่าเสร็จขึ้น `รอ Panya ติ๊ก` ทันทีในรอบที่ตัดสิน · ค้างเกิน 6 ชม. = ทวงเธอผ่านช่องทางที่เธอเห็นจริง
- เพดาน **12 KB / 60 บรรทัด** (PANYA `2039` ข้อ 1 · เกต preflight ของ chief) · ข้อที่ปิดแล้ว **ลบทิ้ง** · กฎบ้านอยู่ `AGENTS.md §7` + `prompts/COMMON_LANE_ROUND.md` — NOW ไม่เก็บกฎซ้ำ ยกเว้นที่ยังไม่ลง §7
- 🔴 ยังไม่ลง §7 (chief `2038` ข้อ 1/7): **ห้ามแฟล็ก `-r` ของ rm ทุกการสะกด** ใช้ `mktemp -d` (PANYA `1546`) · `ATTENDED:`/`SCOREBOARD:` บังคับ · `prompts/` ห้ามสายแก้ · เพดานไฟล์ (GT 300 KB · RE 200 KB · AGENTS/CHIEF_CONTINUATION 30 KB · NOW 12 KB) · **grep ที่ห้า `notes_to_chief/reference_codex_attr/`** (`0256` ข้อ 3)
- 🔴 **shared world** (PANYA `1057`/`1140`): สถานะโลกต่อฉากอยู่ใน process แชร์ทุก session · reboot = โลกใหม่ · A = world registry · B เขียน combat state ลง registry ของ A · DB ไม่รับงานโลก · ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:` · `#827` companion ยัง session-scoped ❌ · ไบต์บนสายต่อคนดูต่างกันได้ (`2348`)
- 🔴 RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING:` (PANYA `1130` · ผู้ตรวจคู่ = COO) · `KNOWN_RED_MAIN:` **2 แถว** = (1) `skip_census PIN DRIFT test_script_lua_api_instance.py/bridge_lua_scripts pinned 1 observed 0` (Q `#891` แล้ว รอ census ยืนยัน) (2) `bridgesize GAME_TEST_QUEUE.md > 300 KB` **เฉพาะโตจาก `ATTENDED:`/`CANCELLED` ตาม R364 ข้อ 2** (chief archive `0747` · โตจากอย่างอื่นยังแดงจริง) · chief ห้ามปิด PR สายอื่นด้วยสองแถวนี้

## บันไดไมล์สโตน (PANYA `20260904_0233` · ไม่มีกำหนดวัน ห้ามรายงาน "เลยกำหนด" · ผ่าน M(n) ก่อนจึงประกาศ v(n) · `SERVER_VERSIONS.md` ของ chief)
- ✅ **M1/v1** ประกาศแล้ว (R249)
- ⏳ **M2 "ออกจากเมืองได้" — โปรเจกต์อยู่ตรงนี้ · ตัวบล็อกโค้ด 0 · GT-233 อยู่บนเครื่องคุณ**: `SAILING_RESULT` key `+0x14` (RE-265) `#857`/`#865` บน main · เกณฑ์ผ่าน: ใกล้เกาะ → "รายงานกัปตัน" → ผู้เล่นกด → วาปเข้า **เกาะ 2 และ 3 บนจอ** · ห้ามเซิร์ฟเวอร์ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวลฝั่งเซิร์ฟเวอร์ · ชั้นถัดไป = Trigger.* ของ Q
- **M3 "สนามมีมอนสเตอร์" = P-2** · **M4 "ตีได้ตายได้"** สี่ข้อ: มอนตีกลับ HP ลดจริง · ตายถูกต้อง · ศพไม่ค้าง · เกิดใหม่ (LANE-B · `GT-224`) · **M5** เก็บได้+รอด relog · **M final** ครบวงจร · ตาราง CHARTER-02 ใน `CHIEF_CONTINUATION.md`
- 🔴 **LANE-DB: PANYA-ORDER สวมอาวุธ (`0156` · 14:00) มาก่อนทุกอย่าง** (`0345`) · PLAYER/CHARACTER (`0328`): ชิ้น 1 ✅ · ชิ้น 2 รอ RE `s_SCORE` · **ชิ้น 3 `0x309A` typed ทำเลย (`1043`)** · ชิ้น 4 นามแฝง+รหัสรอง (RE ก่อน) · home-marker `#851` ⇒ chief · ประตูเควส/flag **หลัง** chief whitelist (`2353`)
- **Q SCRIPT/QUEST**: `prompts/LANE-Q.md` · Trigger.* 5/17 · Quest.* 1/25 (`#904`) · `RE-273` · pin drift `#891` ✅

## งานด่วนตอนนี้ (P-1/P-2/P-3 ซ้อนกับบันไดข้างบน)
- **หาง P-1** (PANYA `0125`): `#689` บน main · ปิดด้วย `GT-223` บนจอ · หนี้ `DropLedgerCell` ข้ามฉาก chief ตั้งเลข · ห้ามลบแถว ledger
- **P-2 สีชื่อมอน (= M3)**: ส้ม/แดง/เทา ห้ามชมพู + attr/relation ถูก (B) · สี = คู่ (คนดู, มอน) ผ่าน `NPCAttr+0x98` (`0254`) · census `#906` บน main ✅ · เลข GT สี รอ archive (`1146`) · GM ขยายยาม tripwire คลุม `mob_viewer_link.py` หลัง `/lv` (`0255`) · ห้าม faction-only / hardcode FontStyleID
- **LANE-GM: `/lv` บน main ✅ → GT บนจอ (`0546`) ก่อน P-3** · P-3 ปุ่ม GM 3 หน้า (`2150`) · `/speed` ล็อกปิดจน (b'') mask ล็อกอิน (`0545`) · `/warp <n> <x> <y>` ปิดถาวร · `/warp <n>` ฉากเดียวกัน = วาปไป spawn (PANYA `1800`)
- **M4 · LANE-B**: caller `apply_hp_damage` พักจน Door B ส่งจริง · roster ฉาก 3/4/5/14/8 บน main (`#899` · Nina/Carlos ตายไม่ได้แต่เห็นตัว `0844`) · 4 ฉาก bg0006/7/9/11 `#907` บน main **ใบฆ่าจริง = `1150`** → B ชี้สตริง 4+4 ไป `11:50` รอบหน้า · bg0010 STATIC ถึง chief (`0903`+`1046`) · respawn 120 s (`2147`) · GT (ก) = `GT-274` CS วาง B ตรวจคู่ (`0645`)
- **chief ลำดับ (`1146` แทนของเดิม)**: **(0) archive `GAME_TEST_QUEUE.md` ≤300 KB + `CLIENT_RE_QUEUE.md` ≤200 KB รอบหน้า PR แรก** → **(1) รอบเดียวกัน วางเนื้อใบ+เลข `/lv` `0434` · PANEL-BUTTON `0852` · GT-275 · GT-274 v2 `0805` · GT สี `0256` + กรอกคำสั่งจริง/พลิก PENDING `GT-079`/`GT-080` (A `1038`)** → **(2) แพตช์เครื่องมือ PR เดียว: โทเคน `CANCELLED`+`FAIL` (`0747`) + แถว `PLACEHOLDER` + คำเตือน stub `.CONSUMED` (B `1050`)** → (3) CORE-REQUEST B `1952` · A `0914` · GM-062 (+063 `1149`) → ที่เหลือ `0256` §7 · D1 `0252` · `2352` · `1041` · backlog `0547` `0042` · STATIC bg0010
- **LANE-UI**: `#860` เปิด (RE-266) · GT-184/186 หลังจากนั้น (`2259`)
- **CS**: ESCALATION `1044` — รอบถัดไป `skill_attr_hypothesis.py` ปลดแฟล็กหรือใบ GT "กด K" · **DB**: `1043` ชิ้น 3 `0x309A` ระหว่างรอ capture · `#896`/`#902` ไม่รันบน DB จริงก่อน `0156` ปิด (`0749`)

## ห้ามทำจนกว่า P-2 จะปิด
- GT-146 และใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (Panya `0904_2115`) + ผู้สืบทอด `GT-274` หุ่น 916 วัดท่า (`0645`)

## เมื่อไม่มีงานด่วน — ท่อ promotion (PANYA `2039` ข้อ 3)
- 5 ตัวแรก (COO `1041` จาก `docs/PROMOTION_BACKLOG.md` · เกณฑ์: เห็นบนจอ + ไม่ติด P-2): **1. `skill_attr_hypothesis.py` CS** (กด K) · **2. `remote_player_hypothesis.py` A** (`1057`) · **3. `lane_hooks/lane_a_choose_npc_scene1.py` A** (คลิก NPC → trigger) · **4. `ground_loot_hypothesis.py` B** (หาง P-1) · **5. `item_operate_res_hypothesis.py` UI** (แชทเขียว) · 9 แถว B HP/ตี/ตาย **รอ P-2** · วิธี: PR ปลดแฟล็ก+เทสคู่+adversary+ใบ GT `ATTENDED:`
