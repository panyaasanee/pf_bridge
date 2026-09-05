# NOW — งานที่ต้องมาก่อนทุกอย่าง (สถานะปัจจุบันเท่านั้น · เพดาน 12 KB / 60 บรรทัด · ประวัติอยู่ในจดหมาย `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-05 23:56 +07:00 โดย COO (รอบกล่องจดหมาย · 7 ใบตัดสิน · รายละเอียด `2356`) — รอบนี้ขยับ:
- ✅ **`#857` SAILING_RESULT key บน main 23:18** ⇒ ตัวบล็อกโค้ด M2 = 0 · GT-233 v3 ยังห้ามบูตจน A ลง D1 lazy-load + ผู้สมัครแยกคอลัมน์ (`2349`)
- 🔴 **เกตปิด 2 ใบ**: `#859` lupa ของ chief (shim `py.cmd` ตัด `=` · `2351`) · `#858` DB `'learned'` (หมุด migration 13→14 · `2354`) — ทั้งคู่ re-land งานแรกรอบหน้า
- 🔴 **COO ค้างส่ง 09:41**: PANYA `1130` ประเมินกำลัง 8 สายพร้อมตัวเลข (ตก 21:41 · ทวง `2225`) — ≤15 บรรทัด ต่อสาย = ค้าง/โค้ด 24 ชม./คอขวด · พอไหม · สายที่ 9?
- สะพานเดิน `23:40` · claim เฝ้า: pf_bridge `#1377` UI yield เปิด 21:18 (ผีเมื่อ 00:18) · escalation 0 · PR เปิด server: `#860` UI `#861` B `#862` Q · `#794` รอ Panya · Scoreboard: DONE 0/8

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ว่าง = ไม่มีอะไรค้างคุณ · ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
1. **ปิด `pirate-force-server#794` ด้วยมือ** (กิ่งไม่ใช่ `claude/*` workflow ไม่แตะ · เนื้องานบน main ตั้งแต่ `#806` · ย้ายมา 17:55 `1751`)
2. **ปิด `pf_bridge#1336` (courier) ด้วยมือ** — ค้างตั้งแต่ 15:22 · ไฟล์ `1518_KA1A-NOTICE` บน main แล้ว (`2152`)

## รอเครื่องคุณ (ไม่นับเป็นงานค้างของสายไหน · บูต attended หนึ่งครั้งเก็บทุกใบที่มี `ATTENDED:`)
1. **`GT-233` M2 provisioning trial** — 🔴 **ห้ามบูตจนกว่า PR D1+ผู้สมัคร (ข) ของ A ขึ้น main** (`2349`) · `#857` บน main แล้ว (RE-265: `+0x14` = key ตาราง `SAILING_RESULT` → `Common_Confirm` → ผู้เล่นกด → client ยิง `EnterInstanceVital` เอง · **คอลัมน์ key ยังไม่รู้**) · chief พลิกหัว v3 หลัง PR ถัดไปของ A merge · ใบ GT ต้องมีประโยค "เงียบทั้งสองนัด ≠ ทฤษฎีผิด" · R318 NEGATIVE ไม่มี BACKUP
2. **`GT-266`** `/warp 126` วาปสด + relog ยังอยู่ Rising Sun Sea (`#838`+`#844` บน main) · GM เติม `ATTENDED:` (`2051`) · **`GT-NNN` cast 304** (`1953` รอ chief ตั้งเลข · `#847` ปิดไม่ merge ⇒ A re-land หลัง D1 `2349`)
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
- ⏳ **M2 "ออกจากเมืองได้" — โปรเจกต์อยู่ตรงนี้ · ตัวบล็อกโค้ด 0**: key `SAILING_RESULT` ที่ record `+0x14` (RE-265) = **`#857` บน main 23:18** ⇒ เหลือ A: D1 lazy-load + ผู้สมัครแยกคอลัมน์ (`2349`) → chief พลิกหัว GT-233 v3 → เครื่องคุณ · เกณฑ์ผ่าน: ใกล้เกาะ → "รายงานกัปตัน" → ผู้เล่นกด → วาปเข้า **เกาะ 2 และ 3 บนจอ** · ห้ามเซิร์ฟเวอร์ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวลฝั่งเซิร์ฟเวอร์ · ชั้นถัดไป = Trigger.* ของ Q · งานสำรอง A: cast 305
- **M3 "สนามมีมอนสเตอร์" = P-2** · **M4 "ตีได้ตายได้"** สี่ข้อ: มอนตีกลับ HP ลดจริง · ตายถูกต้อง · ศพไม่ค้าง · เกิดใหม่ (LANE-B · `GT-224`) · **M5** เก็บได้+รอด relog · **M final** ครบวงจร · ตาราง CHARTER-02 ใน `CHIEF_CONTINUATION.md`
- 🔴 **PLAYER/CHARACTER = LANE-DB มาก่อนทุกอย่างในคิว DB** (`0328`): ชิ้น 1 class_id ✅ (เหลือบรรทัด chief `runtime.py:5159`) · ชิ้น 2 **รอ RE `s_SCORE`** DEFAULT 100 · ชิ้น 3 `0x309A` typed · ชิ้น 4 นามแฝง+รหัสรอง (RE ก่อน) · ชิ้น 5 ✅ · **ตอนนี้: `select_character_honoring_home_marker` บน main (`#851`) ⇒ chief สลับจุดเรียก · ประตูเควส/flag สำหรับ Q สร้างแล้วแต่ชน guard ⇒ chief whitelist (`2353`) · `'learned'` = `#858` ปิดโดยเกต ⇒ DB re-land (`2354`)**
- **ทีม 8 สาย**: chief(E) · A · B · DB · GM · CS (:06/:36) · UI (:16/:46) · **Q SCRIPT/QUEST** (`prompts/LANE-Q.md` · Lua host 616 สคริปต์ · 0/160 API · คิว: Trigger.* 17 (ปลด M2) → Quest.* 25 → Player.* 73)

## งานด่วนตอนนี้ (P-1/P-2/P-3 ซ้อนกับบันไดข้างบน)
- **หาง P-1**: ของหายชั่วคราวแล้วโผล่กลับ (PANYA `0125`) · `#689` บน main · ปิดด้วย `GT-223` บนจอ · หนี้ `DropLedgerCell` ข้ามฉาก chief ตั้งเลขใบ · ห้ามลบแถว ledger
- **P-2 สีชื่อมอน (= M3)**: ส้ม/แดง/เทา ห้ามชมพู + attr/relation ถูก (B) · มอนเรามาทาง census ไม่ใช่ `CNetNPC` (RE-222 · RE-263 = ใบสีที่ตอบแล้ว · RE-259/260 ไม่ใช่เรื่องสี) ⇒ **COO เคาะ `2348`: สี = คู่ (คนดู, มอน) ผ่าน `NPCAttr+0x98` · จุด compose ต่อคนดู = chief runtime · GM ยื่น CORE-REQUEST ถึง LANE-E + ใบ GT รอบหน้า** · ห้าม faction-only / hardcode FontStyleID
- **P-3 ปุ่ม GM ทั้ง 3 หน้าทำงานจริง** (LANE-GM · งานสำรองข้อแรกของ GM `2150`) · GMUI เปิดแล้ว เหลือไล่ทีละปุ่ม · `/speed` ล็อกปิดจน (b'') mask ล็อกอิน (`0545`) · `/warp <n> <x> <y>` ปิดถาวร · `/warp <n>` ในฉากเดียวกัน = วาปไป spawn ทันที (PANYA `1800`)
- **M4 · LANE-B**: caller `apply_hp_damage` พักจน Door B ส่งจริง · roster ฉาก 3/4/5/14 บน main · **งานแรก: สัญญาต่อฉาก generic + ปิดรูฉาก 3 (`1246` ค)** · `#848` บน main · respawn 120 s (`2147`) · ผู้อ่าน `DEATH_SEED_WIRING` = chief (`2149`) · CORE-REQUEST `1352`+flag ใบเดียว (`2148`)
- **M4 · chief**: ลำดับ `2351`: re-land lupa (+PR pf_bridge preflight ทาง ก `2350`) → PROMOTION_BACKLOG (+หัว AGENTS หน่วยไบต์ `2352`) → whitelist ประตูเควส `2353` → `DEATH_SEED_WIRING` · คิวเดิม: `runtime.py:5159` class_id · สลับจุดเรียก home-marker · attr+x=9 · coerce `actor_identities` · ปลดบล็อก `GT-223`
- **LANE-UI**: UI-B `#846` บน main ✅ · `#860` เปิด (UI_LANE.md + RE-266) · `ATTENDED:` RE-235/237/261 (`2054`) · GT-184/186 หลัง RE-266 (`2259`)
- **CS**: `#845` `#854` บน main · รอ DB `'learned'` re-land (`2354`)

## ห้ามทำจนกว่า P-2 จะปิด
- GT-146 และใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (Panya 0904_21:15)

## เมื่อไม่มีงานด่วน — ท่อ promotion (PANYA `2039` ข้อ 3)
- 5 ตัวแรกที่ควรปลดแฟล็ก + เจ้าของ: **รอ `docs/PROMOTION_BACKLOG.md` จาก chief (ใบที่ 2 ใน `2351`)** ⇒ COO จัดอันดับ 09:41 · จนกว่านั้นทุกสายปลด scenario ในเขตตัวเองที่พิสูจน์แล้ว 1 ตัว (`production_allowed=true` 10/60) = งานสำรองข้อแรก
