# NOW — งานที่ต้องมาก่อนทุกอย่าง (สถานะปัจจุบันเท่านั้น · เพดาน 12 KB / 60 บรรทัด · ประวัติอยู่ในจดหมาย `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-05 21:52 +07:00 โดย COO (รอบผู้บริหาร = `2152`) — รอบนี้ขยับ:
- 🔴 **PANYA-ORDER `2038`/`2039` มีผล**: ตัววัดหลัก = Scoreboard (tsv ยังไม่มี · chief รอบ 22:21) · ไฟล์รอบจบด้วย `SCOREBOARD:` · ใบที่ต้องการเครื่อง Panya มี `ATTENDED:` ≤5 บรรทัด · **LANE-Q ตั้งแล้ว** (`2055` · รอบแรก 21:12)
- **M2 ไม่ขยับ**: `#852` SAILING_RESULT key (A) รอเกต = ตัวบล็อกตัวเดียว · **`#847` cast 304 ปิดไม่ merge ⇒ A re-land (`2151`)** · บน main: `#846` `#848` `#849` `#850` `#851`
- ตัดสิน 5 ใบ: `2147` `2148` (B) · `2149` (chief: 3 เฟรมก่อน · GM-060 กลืน D3/D4 · `DEATH_SEED_WIRING` ถัดไป) · `2150` (GM) · `2151` (A)
- สะพานเดิน `21:32` · claim ผี 0 · escalation 0 · PR เปิด server: `#852` A · `#853` B · `#854` CS · `#794` รอ Panya

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ว่าง = ไม่มีอะไรค้างคุณ · ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
1. **ปิด `pirate-force-server#794` ด้วยมือ** (กิ่งไม่ใช่ `claude/*` workflow ไม่แตะ · เนื้องานบน main ตั้งแต่ `#806` · ย้ายมา 17:55 `1751`)
2. **ปิด `pf_bridge#1336` (courier) ด้วยมือ** — ค้างตั้งแต่ 15:22 · ไฟล์ `1518_KA1A-NOTICE` บน main แล้ว (`2152`)

## รอเครื่องคุณ (ไม่นับเป็นงานค้างของสายไหน · บูต attended หนึ่งครั้งเก็บทุกใบที่มี `ATTENDED:`)
1. **`GT-233` M2 provisioning trial** — 🔴 **ห้ามบูตจนกว่า PR `SAILING_RESULT` ของ A ขึ้น main** (RE-265 `1932`: record `+0x14` ชี้แถว `SAILING_RESULT` n_AREA=126 จริง → `Common_Confirm` → ผู้เล่นกด → client ยิง `EnterInstanceVital` เอง) · PR = `#852` รอเกต · chief พลิกหัว v3 หลัง merge (`2130`) · R318 NEGATIVE ไม่มี BACKUP
2. **`GT-266`** `/warp 126` วาปสด + relog ยังอยู่ Rising Sun Sea (`#838`+`#844` บน main) · GM เติม `ATTENDED:` (`2051`) · **`GT-NNN` cast 304** (`1953` รอ chief ตั้งเลข · A เติม `ATTENDED:` `2052` · **`#847` ปิดไม่ merge ⇒ re-land `2151`**)
3. **`GT-230`** ร้านค้า NPC hex (UI) · **`GT-243`** skill 99 hotbar+Z (CS) · RE-235/237/261 (UI · ต้องมี `ATTENDED:` `2054`) · GT-255/257 — รันหลังใบ M2

## กติกาของไฟล์นี้ (ห้ามลบสี่บรรทัดนี้)
- ผู้เขียน: **Panya และ COO เท่านั้น** · คนอื่นเสนอผ่านจดหมายจ่าหน้า `ADDRESSEE: COO`
- **"เสร็จ" ติ๊กได้โดย Panya คนเดียว** — สถานะสูงสุดที่ COO ไปถึงได้คือ `รอเจ้าของยืนยัน` (โค้ดขึ้น main ไม่ใช่ "เสร็จ" · `production_allowed = False` ยังไม่นับว่าขยับ)
- **COO มีหน้าที่เตือน** — ย้ายข้อที่คิดว่าเสร็จขึ้น `รอ Panya ติ๊ก` ทันทีในรอบที่ตัดสิน · ค้างเกิน 6 ชม. = ทวงเธอผ่านช่องทางที่เธอเห็นจริง
- เพดาน **12 KB / 60 บรรทัด** (PANYA `2039` ข้อ 1 · เกต preflight ของ chief) · ข้อที่ปิดแล้ว **ลบทิ้ง** · กฎบ้านอยู่ `AGENTS.md §7` + `prompts/COMMON_LANE_ROUND.md` — NOW ไม่เก็บกฎซ้ำ ยกเว้นที่ยังไม่ลง §7
- 🔴 ยังไม่ลง §7 (chief `2038` ข้อ 1/7): **ห้ามแฟล็ก `-r` ของ rm ทุกการสะกด** ใช้ `mktemp -d` (PANYA `1546`) · `ATTENDED:` บังคับ · `SCOREBOARD:` บังคับ · `prompts/` ของ Panya ห้ามสายแก้ · เพดานไฟล์ (GT 300 KB · RE 200 KB · AGENTS/CHIEF_CONTINUATION 30 KB · NOW 12 KB)
- 🔴 **shared world** (PANYA `1057`/`1140`): สถานะโลกต่อฉากอยู่ใน process แชร์ทุก session · reboot = โลกใหม่ · A = world registry · B เขียน combat state ลง registry ของ A · DB ไม่รับงานโลก · ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:` · `#827` companion ยัง session-scoped ❌ · ผู้อ่านสมุดโลกใน `runtime.py` ยังไม่มี (`2149`)
- 🔴 RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING:` (PANYA `1130` · ผู้ตรวจคู่ = COO) · `KNOWN_RED_MAIN:` ตอนนี้ **ไม่มี**

## บันไดไมล์สโตน (PANYA `20260904_0233` · ไม่มีกำหนดวัน ห้ามรายงาน "เลยกำหนด" · ผ่าน M(n) ก่อนจึงประกาศ v(n) · `SERVER_VERSIONS.md` ของ chief)
- ✅ **M1/v1** ประกาศแล้ว (R249 · `SERVER_VERSIONS.md` v1)
- ⏳ **M2 "ออกจากเมืองได้" — โปรเจกต์อยู่ตรงนี้ · ตัวบล็อกโค้ด 1 ตัว**: key `SAILING_RESULT` ที่ record `+0x14` (RE-265 `1932`) ⇒ **PR `#852` เปิดแล้ว รอเกต · GT-233 v3 `ATTENDED:` ตก 22:51** (`1947`/`2130`) · เกณฑ์ผ่าน: ใกล้เกาะ → "รายงานกัปตัน" → ผู้เล่นกด → วาปเข้า **เกาะ 2 และ 3 บนจอ** · ห้ามเซิร์ฟเวอร์ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวลฝั่งเซิร์ฟเวอร์ · ชั้นถัดไป = Trigger.* ของ Q · งานสำรอง A: cast 305
- **M3 "สนามมีมอนสเตอร์" = P-2** · **M4 "ตีได้ตายได้"** สี่ข้อ: มอนตีกลับ HP ลดจริง · ตายถูกต้อง · ศพไม่ค้าง · เกิดใหม่ (LANE-B · `GT-224`) · **M5** เก็บได้+รอด relog · **M final** ครบวงจร · ตาราง CHARTER-02 ใน `CHIEF_CONTINUATION.md`
- 🔴 **PLAYER/CHARACTER = LANE-DB มาก่อนทุกอย่างในคิว DB** (`0328`): ชิ้น 1 class_id ✅ (เหลือบรรทัด chief `runtime.py:5159`) · ชิ้น 2 **รอ RE `s_SCORE`** DEFAULT 100 · ชิ้น 3 `0x309A` typed · ชิ้น 4 นามแฝง+รหัสรอง (RE ก่อน) · ชิ้น 5 ✅ · **ตอนนี้: `select_character_honoring_home_marker` บน main (`#851`) ⇒ chief สลับจุดเรียก · ประตูเควส/flag สำหรับ Q (`2058`) · `grant_learned_skill` + source `'learned'` จาก CS (`2119`)**
- **ทีม 8 สาย**: chief(E) · A · B · DB · GM · CS (:06/:36) · UI (:16/:46) · **Q SCRIPT/QUEST** (`prompts/LANE-Q.md` · Lua host 616 สคริปต์ · 0/160 API · คิว: Trigger.* 17 (ปลด M2) → Quest.* 25 → Player.* 73)

## งานด่วนตอนนี้ (P-1/P-2/P-3 ซ้อนกับบันไดข้างบน)
- **หาง P-1**: ของหายชั่วคราวแล้วโผล่กลับ (PANYA `0125`) · `#689` บน main · ปิดด้วย `GT-223` บนจอ · หนี้ `DropLedgerCell` ข้ามฉาก chief ตั้งเลขใบ · ห้ามลบแถว ledger
- **P-2 สีชื่อมอน (= M3)**: ส้ม/แดง/เทา ห้ามชมพู + attr/relation ถูก (B) · มอนเรามาทาง census ไม่ใช่ `CNetNPC` (RE-222) ⇒ RE-259/260/263 ตอบแล้ว ผู้บริโภค **LANE-GM ยังไม่มี PR สี = STUCK นานสุด** · ห้าม faction-only fix / hardcode FontStyleID
- **P-3 ปุ่ม GM ทั้ง 3 หน้าทำงานจริง** (LANE-GM · งานสำรองข้อแรกของ GM `2150`) · GMUI เปิดแล้ว เหลือไล่ทีละปุ่ม · `/speed` ล็อกปิดจน (b'') mask ล็อกอิน (`0545`) · `/warp <n> <x> <y>` ปิดถาวร · `/warp <n>` ในฉากเดียวกัน = วาปไป spawn ทันที (PANYA `1800`)
- **M4 · LANE-B**: caller `apply_hp_damage` พักจน Door B ส่งจริง · roster ฉาก 3/4/5/14 บน main · **งานแรก: สัญญาต่อฉาก generic + ปิดรูฉาก 3 (`1246` ค)** · `#848` บน main · respawn 120 s (`2147`) · ผู้อ่าน `DEATH_SEED_WIRING` = chief (`2149`) · CORE-REQUEST `1352`+flag ใบเดียว (`2148`)
- **M4 · chief**: คืนนี้ตาม `2059`+`2149` (1+7 → Scoreboard tsv + D3/D4 กลืน GM-060 → PROMOTION_BACKLOG + `DEATH_SEED_WIRING` + เขต Q) · 3 เฟรมตก 22:51 · คิวเดิม: `runtime.py:5159` class_id · สลับจุดเรียก home-marker · attr+x=9 · coerce `actor_identities` · ปลดบล็อก `GT-223`
- **UI-B/UI-A (LANE-UI)**: PANYA `1911`: UI-B ล็อกเอาต์จริง headless = `#846` **บน main 21:37** ✅ ⇒ ถัดไป: `docs/UI_LANE.md` ใน `pirate-force-server/docs/` (`2149`) + `ATTENDED:` RE-235/237/261 (`2054`) · GT-184/186 BLOCKED-ON-RE-266
- **GM-A `/warp 126`**: ✅ `#838`+`#844` บน main ⇒ `GT-266` รอเครื่องคุณ · ประตูล็อกอิน 126 ปิด (`1444`)
- **CS**: `#845` บน main · `#854` grant สกิล (Protocol) เปิดรอเกต · CORE-REQUEST `2119` ถึง DB

## ห้ามทำจนกว่า P-2 จะปิด
- GT-146 และใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (Panya 0904_21:15)

## เมื่อไม่มีงานด่วน — ท่อ promotion (PANYA `2039` ข้อ 3)
- 5 ตัวแรกที่ควรปลดแฟล็ก + เจ้าของ: **รอ `docs/PROMOTION_BACKLOG.md` จาก chief (รอบ 23:51)** ⇒ COO จัดอันดับ 09:41 · จนกว่านั้นทุกสายหยิบ scenario ในเขตตัวเองที่พิสูจน์แล้ว (`production_allowed=true` 10/60) มาปลด 1 ตัว = งานสำรองข้อแรก · โค้ดก่อน กระดาษทีหลัง
