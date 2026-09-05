# NOW — งานที่ต้องมาก่อนทุกอย่าง (สถานะปัจจุบันเท่านั้น · เพดาน 12 KB / 60 บรรทัด · ประวัติอยู่ในจดหมาย `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-05 21:00 +07:00 โดย COO — รอบนี้ขยับ:
- 🔴 **PANYA-ORDER `2038`/`2039` (20:3x) มีผลทันที**: NOW ย่อจาก 68 KB (สำเนาเต็ม = `2100`) · ตัววัดหลัก = Scoreboard · ทุกไฟล์รอบจบด้วย `SCOREBOARD:` · ใบที่ต้องการเครื่อง Panya ต้องมีบล็อก `ATTENDED:` ≤5 บรรทัด · งานสำรองข้อแรกทุกสาย = ปลดแฟล็ก 1 ตัว · **LANE-Q ตั้งแล้ว** (`2055` · A/B/DB ประกาศ interface `2056`-`2058`) · ลำดับ chief คืนนี้ = `2059`
- แขนที่สามของ A (cast 304/305) **ยืนยัน** (`2052`) · warp rollback = คืนทั้ง 13 ฟิลด์ inverse ของ chief PR เดียว D3+D4 ตก 23:51 (`2050`/`2051`) · `#844` GM + `#845` CS บน main ⇒ escalation CS ถอน (`2053`) · UI `#846` draft ⇒ `ADVERSARY_UNAVAILABLE` + undraft รอบ 21:16 (`2054`)
- ตรวจคู่ RE 19:44→20:40 = 0 · สะพานเดิน heartbeat `20:28` · claim ผี = 0 · PR เปิด: server `#846`/`#847`/`#848`/`#849` · `#794` รอ Panya

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ว่าง = ไม่มีอะไรค้างคุณ · ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
1. **ปิด `pirate-force-server#794` ด้วยมือ** (กิ่ง `lane-e-5e00uw-corereq-ui` ไม่ใช่ `claude/*` workflow ไม่แตะ · เนื้องานบน main แล้วตั้งแต่ `#806` · ย้ายมา 2026-09-05 17:55 COO `1751`)

## รอเครื่องคุณ (ไม่นับเป็นงานค้างของสายไหน · บูต attended หนึ่งครั้งเก็บทุกใบที่มี `ATTENDED:`)
1. **`GT-233` M2 provisioning trial** — 🔴 **ห้ามบูตจนกว่า PR `SAILING_RESULT` ของ A ขึ้น main** (RE-265 `1932`: record `+0x14` ต้องชี้แถว `SAILING_RESULT` n_AREA=126 ที่มีจริง → `Common_Confirm` → ผู้เล่นกด → client ยิง `EnterInstanceVital` เอง) · chief พลิกหัว READY-v2 หลัง merge (`1949`) · R318 = NEGATIVE-MEASURED ไม่มี BACKUP
2. **`GT-266`** `/warp 126` วาปสด + relog ยังอยู่ Rising Sun Sea (`#838`+`#844` บน main) · GM เติม `ATTENDED:` (`2051`) · **`GT-NNN` cast ฉาก 304** (`1953` รอ chief ตั้งเลข · A เติม `ATTENDED:` `2052` · BLOCKED-ON-MERGE `#847`)
3. **`GT-230`** ร้านค้า NPC hex (UI) · **`GT-243`** skill 99 hotbar+Z (CS) · RE-235/237/261 (UI · ต้องมี `ATTENDED:` `2054`) · GT-255/257 — ไม่บล็อกใคร รันหลังใบ M2

## กติกาของไฟล์นี้ (ห้ามลบสี่บรรทัดนี้)
- ผู้เขียน: **Panya และ COO เท่านั้น** · คนอื่นเสนอผ่านจดหมายจ่าหน้า `ADDRESSEE: COO`
- **"เสร็จ" ติ๊กได้โดย Panya คนเดียว** — สถานะสูงสุดที่ COO ไปถึงได้คือ `รอเจ้าของยืนยัน` (โค้ดขึ้น main ไม่ใช่ "เสร็จ" · `production_allowed = False` ยังไม่นับว่าขยับ)
- **COO มีหน้าที่เตือน** — ย้ายข้อที่คิดว่าเสร็จขึ้น `รอ Panya ติ๊ก` ทันทีในรอบที่ตัดสิน · ค้างเกิน 6 ชม. = ทวงเธอผ่านช่องทางที่เธอเห็นจริง
- เพดาน **12 KB / 60 บรรทัด** (PANYA `2039` ข้อ 1 · เกต preflight ของ chief) · ข้อที่ปิดแล้ว **ลบทิ้ง** ไม่ archive · กฎบ้านทั้งหมดอยู่ `AGENTS.md §7` + `prompts/COMMON_LANE_ROUND.md` — NOW ไม่เก็บกฎซ้ำ ยกเว้นที่ยังไม่ลง §7 ข้างล่าง
- 🔴 ยังไม่ลง §7 (chief `2038` ข้อ 1/7 รอบ 20:51): **ห้ามแฟล็ก `-r` ของ rm ทุกการสะกด** ใช้ `mktemp -d` (PANYA `1546`) · `ATTENDED:` บังคับ · `SCOREBOARD:` บังคับ · `prompts/` เจ้าของ Panya ห้ามทุกสายแก้ · เพดานไฟล์กลาง (GT 300 KB · RE 200 KB · AGENTS/CHIEF_CONTINUATION 30 KB · NOW 12 KB)
- 🔴 **shared world** (PANYA `1057`/`1140`): สถานะโลกต่อฉากอยู่ใน process แชร์ทุก session · reboot = โลกใหม่ · A = world registry · B เขียน combat state ลง registry ของ A · DB ไม่รับงานโลก · ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:` · `#827` companion ยัง session-scoped ❌ แก้ทางเดียว = registry ของ A
- 🔴 RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING:` (PANYA `1130` · ผู้ตรวจคู่ = COO) · `KNOWN_RED_MAIN:` ตอนนี้ **ไม่มี**

## บันไดไมล์สโตน (PANYA `20260904_0233` · ไม่มีกำหนดวัน ห้ามรายงาน "เลยกำหนด" · ผ่าน M(n) ก่อนจึงประกาศ v(n) · `SERVER_VERSIONS.md` ของ chief)
- ✅ **M1/v1** ประกาศแล้ว (R249)
- ⏳ **M2 "ออกจากเมืองได้" — โปรเจกต์อยู่ตรงนี้ · ตัวบล็อกโค้ด 1 ตัว มีชื่อแล้ว**: key `SAILING_RESULT` ที่ record `+0x14` (RE-265 `1932`) ⇒ **LANE-A PR + GT พร้อม `ATTENDED:` รอบ 21:21 ตก 22:51** (`1947`/`2052`) · เกณฑ์ผ่าน: ใกล้เกาะ → หน้า "รายงานกัปตัน" → ผู้เล่นกด → วาปเข้า **เกาะ 2 และ 3 ทั้งสองบนจอ** · ห้ามเซิร์ฟเวอร์ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวลฝั่งเซิร์ฟเวอร์ · ชั้นถัดไป = Trigger.* ของ LANE-Q · งานสำรอง A: cast ฉาก 305 (`2052`)
- **M3 "สนามมีมอนสเตอร์" = P-2** · **M4 "ตีได้ตายได้"** สี่ข้อ: มอนตีกลับ HP ลดจริง · ตายถูกต้อง · ศพไม่ค้าง · เกิดใหม่ (LANE-B · `GT-224`) · **M5** เก็บได้+รอด relog · **M final** เล่นได้ครบวงจร · ตาราง CHARTER-02 ใน `CHIEF_CONTINUATION.md`
- 🔴 **PLAYER/CHARACTER = LANE-DB มาก่อนทุกอย่างในคิว DB** (`0328`): ชิ้น 1 class_id ✅ (เหลือบรรทัด chief `runtime.py:5159`) · ชิ้น 2 ค่าเกิดจากตาราง **รอ RE `s_SCORE`** DEFAULT 100 คงไว้ · ชิ้น 3 บล็อก `0x309A` typed · ชิ้น 4 นามแฝง+รหัสรอง (RE ก่อน) · ชิ้น 5 ✅ · **ตอนนี้: `select_character_honoring_home_marker` PR ตก 21:31 (`1946`) · ประตูเควส/flag สำหรับ Q (`2058`)**
- **ทีม 8 สาย**: chief(E) · A WORLD · B COMBAT · DB · GM · CS (:06/:36) · UI (:16/:46) · **Q SCRIPT/QUEST** (`prompts/LANE-Q.md` · Lua host 616 สคริปต์ · 0/160 API · คิว: spike → Trigger.* 17 (ปลด M2) → Quest.* 25 → Player.* 73)

## งานด่วนตอนนี้ (P-1/P-2/P-3 ซ้อนกับบันไดข้างบน)
- **หาง P-1**: ของหายชั่วคราวแล้วโผล่กลับ = ต้องแก้ (PANYA `0125`) · โค้ด `#689` บน main · ปิดด้วย `GT-223` บนจอ · หนี้ `DropLedgerCell` ข้ามฉาก chief ตั้งเลขใบ · ห้ามลบแถว ledger
- **P-2 สีชื่อมอน (= M3)**: ส้ม/แดง/เทา ห้ามชมพู + attr/relation ถูก (B) · ติด: มอนเรามาทาง census ไม่ใช่ `CNetNPC` (RE-222) ⇒ RE-259/260/263 ตอบแล้ว ผู้บริโภค **LANE-GM** · ห้าม faction-only fix / hardcode FontStyleID
- **P-3 ปุ่ม GM ทั้ง 3 หน้าทำงานจริงทุกปุ่ม** (LANE-GM) · GMUI เปิดแล้ว (`GT-207`/`GT-219` PASS) เหลือไล่ทีละปุ่ม · `/speed` ล็อกปิดจน (b'') mask ล็อกอิน (`0545`) · `/warp <n> <x> <y>` ปิดถาวร · `/warp <n>` ในฉากเดียวกัน = วาปไป spawn ทันที (PANYA `1800`)
- **M4 · LANE-B**: caller `apply_hp_damage` พักจน Door B ส่งจริง ((b'') + `MOB_HIT_FRAME_CONFIRMED`) · roster ฉาก 3/4/5/14 บน main · **งานแรก: สัญญาต่อฉาก generic + ปิดรูฉาก 3 (`1246` ค)** · `#848` respawn door รอ merge · hook เหตุการณ์ให้ Q (`2057`)
- **M4 · chief**: คืนนี้ตาม `2059` (`2038` ข้อ 1+7 → Scoreboard + D3/D4 PR → PROMOTION_BACKLOG + เขต Q) · คิวเดิมยืน: `runtime.py:5159` class_id · จุดอ่าน attr+x=9 · coerce `actor_identities` · ปลดบล็อก `GT-223`
- **UI-B/UI-A (LANE-UI)**: 🔴 PANYA `1911`: UI-B ล็อกเอาต์จริง headless ก่อนใบ RE ใหม่ = `#846` draft ⇒ undraft รอบ 21:16 (`2054`) ไม่มี = escalation 21:41 · GT-184/186 BLOCKED-ON-RE (0x709E)
- **GM-A `/warp 126`**: ✅ `#838`+`#844` บน main ⇒ `GT-266` รอเครื่องคุณ · ประตูล็อกอิน 126 ยังปิด (`1444`)
- **CS**: `#845` บน main · ถัดไป `2053` (ตรวจ `1335` → ปลดแฟล็ก/grant สกิล)

## ห้ามทำจนกว่า P-2 จะปิด
- GT-146 และใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (Panya 0904_21:15)

## เมื่อไม่มีงานด่วน — ท่อ promotion (PANYA `2039` ข้อ 3)
- 5 ตัวแรกที่ควรปลดแฟล็ก + สายเจ้าของ: **รอ `docs/PROMOTION_BACKLOG.md` จาก chief (รอบ 23:51 `2059`)** · จนกว่านั้นทุกสายหยิบ scenario ในเขตตัวเองที่พิสูจน์แล้ว (`production_allowed=false` · 50/60) มาปลด 1 ตัว = งานสำรองข้อแรก (COMMON) · โค้ดก่อน กระดาษทีหลัง
