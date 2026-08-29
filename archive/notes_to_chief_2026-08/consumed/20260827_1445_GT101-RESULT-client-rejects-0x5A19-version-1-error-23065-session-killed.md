# GT-101 RESULT 2026-08-27 14:45 +07:00 — ผลบวกที่ไม่มีใครคาด: client ปฏิเสธ GM_UpdateGMStateVital เวอร์ชัน 1 ด้วย error 23065 แล้วเซสชันตาย

ถึง: สาย GM (เจ้าของใบ) · RE runner · chief · cc COO · ADDRESSEE: LANE-GM
จาก: attended session "กะ1" (Panya ขับ UI เอง) · OBSERVER_CONFIRMED: 2026-08-27T14:39+07:00 (เจ้าของเห็นเองและส่งภาพ 2 ใบ)

## สถานะที่ควรเป็น
**GT-101 = RESULT (ไม่ใช่ PASS ไม่ใช่ NO-RESULT ไม่ใช่ BLOCKED)** — ใบเขียนไว้ว่ามีสองผลที่ยอมรับ (ไม่เปลี่ยน / เปลี่ยน) ผลจริงเป็นแบบที่สาม: **client โยน error แล้วเซสชันตาย**

## บูต
- BOOT_COMMIT 2217fa47 = main HEAD (merge #119) มีคำตัดสิน gate ของตัวเอง (workflow_dispatch run 33048706673 success) — post-merge dispatch ใช้ได้จริง resolver ไม่ถอยแล้ว
- ไร้แฟล็กทุกตัว · `PF_GM_ACCOUNTS_CONFIG=pf_bridge\backup\gm_accounts_GT-101_20260827_142820.json` เนื้อหา `{"gm_accounts": ["localtest"]}` — ใช้ชื่อบัญชีจริงที่ client ส่ง (ตาราง accounts: `localtest` ตัวละคร Arena01) **ไม่ใช่ `attended_test`** ที่ CHIEF-REPLY 1200 ระบุ (ชื่อนั้นเป็น fixture ใน tests ไม่มี client ตัวไหนส่งชื่อนี้ ถ้าใช้ตามนั้น is_gm_account จะคืน False ตลอด) — ทาง B ตามที่อนุมัติ ไม่แตะ config/gm_accounts.json
- ด่าน 2 ห้า grep + PF_GM_ACCOUNTS_CONFIG ผ่านครบที่ 2217fa47 (outbox/1287_gt101_hold_and_resolve.utf8.txt) · code delta vs main = 0
- รอบแรก 14:28 ถูก teardown ที่ผู้ช่วยต่อคิวเร็วเกินไปปิดทิ้งก่อน login (ความผิดผู้ช่วย ไม่มีข้อมูล) · รอบจริง 14:34 boot job 1291, teardown 1292, release 1290

## ชั้น wire/DB (จากคอนโซลเซิร์ฟเวอร์ GameClient\capture_gt101_20260827_143419\server_console_live.out.txt)
- login ปกติ: LOGIN_VERIFY_ACK → CHARACTER_LIST → StartGameReq → `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` (R190 ต่อสายแล้วจริง) → FOUNDATION_SELECTED_START_GAME 423B → V113 teleport 73B
- **`[G>] GM_UPDATE_STATE_AFTER_LOGIN (39 bytes; late=4.3 ms)`** พิมพ์ 1 ครั้ง · ไม่มี `gm_account_lookup_failed_*` ⇒ is_gm_account("localtest") = True เฟรมถูกคิวและส่งจริง
- ไบต์บนสาย (คัดจากคอนโซล):
  `12 9D 6E 14 00 00 00 00 08 04 0B 02 12 01 00 12 19 5A 0B 01 0B 00 0B 00 14 00 00 00 00`
  เทียบเฟรมอื่นบน connection เดียวกัน: START_GAME `… 08 00 0B 02 12 01 00 12 9F 1E 0B 03 …` · TeleportVital `… 12 A2 25 0B 04 …`
  ข้อสังเกตเชิงไบต์ (ไม่ใช่ semantic): (ก) ไบต์หลัง vital id ของเรา = `0B 01` (vital_version=1 ที่ซอร์สติดป้าย [ASSUMED - awaiting RE]) ขณะที่เฟรมอื่นเป็น `0B 03` / `0B 04` (ข) ไบต์ที่ offset 8-9 ของเราเป็น `08 04` ขณะที่เฟรมอื่นทุกเฟรมเป็น `08 00`
- หลังเฟรมนี้: heartbeat ว่างต่อไปอีก 35 ใบ (~35 วินาที) โดย client ไม่ส่งอะไรกลับ แล้ว `[G!] game socket closed/reset: ConnectionResetError(10054)` — client ปิด socket เอง
- DB สำเนา run_gt101_20260827_143419: sessions-with-char 11→12, open 0, integrity ok · canonical sha 4FF37060… ไม่เปลี่ยน · teardown สะอาด (listeners 0, traceback 0, stopped ×1)

## ชั้น client-observable (ตาเจ้าของ + ภาพ 2 ใบ)
- ทันทีที่หน้าโหลด "WANTED" จบและเข้าแมพ: **หน้าต่าง Error กลางจอ** ข้อความจีนตัวเต็ม `網路 VitalData 版本不對 --- ErrorData=23065, 請洽程式設計人員` (= "เครือข่าย: เวอร์ชันของ VitalData ไม่ตรง — ErrorData=23065 กรุณาติดต่อโปรแกรมเมอร์") **23065 ฐานสิบ = 0x5A19 = GM_UpdateGMStateVital** ⇒ client ระบุชัดว่าเฟรมไหนผิด
- ด้านหลัง dialog แมพ Port Royal ขึ้นครบ (HP 100/100 Lv.1, minimap, HUD X -8,553 Y -2,579 = จุดเกิดเดิม, ตัวละครยืน) แต่มีข้อความเหลืองกลางบนจอ "เลยเวลา 24/25/26 วินาที ยังไม่สามารถรับข้อมูล Server ได้ กรุณาออกจากระบบ…" นับขึ้นเรื่อย ๆ = client หยุดประมวลผลสายหลังเจอ error
- เจ้าของกด OK → เกมปิดตัวเอง
- **ไม่มีทางสังเกต "จอเปลี่ยนไหม" ตามที่ใบตั้งไว้** เพราะ client ไม่เคยไปถึงสถานะปกติ — ใบยังไม่ได้ตอบคำถามเดิม (UI ของ GM) แต่ตอบคำถามที่ใหญ่กว่า: **เวอร์ชันที่ client ต้องการของ 0x5A19 ไม่ใช่ 1**

## สิ่งที่ผลนี้บอก / ไม่บอก (nonclaims)
- [วัดแล้ว] client ตรวจ vital_version ของ 0x5A19 และปฏิเสธค่า 1 ด้วย error path ที่ไม่ใช่การ drop เงียบ ๆ — เป็น modal + หยุดรับข้อมูล + ปิด socket
- [วัดแล้ว] ผลของ RE-089 ("ไม่พบ UI consumer") ยังไม่ได้ถูกทดสอบ เพราะ payload ไม่เคยถูกประมวลผล
- [ไม่อ้าง] ว่าเวอร์ชันที่ถูกคือ 3 หรือ 4 (เป็นค่าที่เฟรมอื่นใช้ ไม่ใช่หลักฐานของ vital นี้) · [ไม่อ้าง] ว่า `08 04` เป็นสาเหตุร่วม — ต้องให้ RE อ่าน handler
- [ไม่อ้าง] ว่า error path นี้เกิดกับ vital อื่นแบบเดียวกัน (วัดแค่ 0x5A19)

## ตอนนี้ต้องทำอะไรต่อ (ตามลำดับ)
1. **RE runner (ใบใหม่ ต่อยอด RE-089)**: อ่าน handler 0x5A19 (`0x00729F00` ที่ RE-089 พิน) หาจุดเทียบ vital_version → ค่าที่รับได้ · และหา error path ที่ผลิตข้อความ 版本不對 + ErrorData=<vital id> (ตัวนี้ใช้ได้กับทุก vital ในอนาคต: client "บอก" เราเองว่าเวอร์ชันผิดพร้อม id)
2. **สาย GM**: แก้ `make_gm_update_state_frame(legacy, 1, 0, 0, 0)` ที่ runtime.py:4746 ให้ใช้เวอร์ชันที่ RE พิน (ห้ามเดา 3/4 แล้วยิงใส่เจ้าของอีก) และตรวจว่า header `08 04` มาจากไหน · จนกว่าจะพิน **ห้ามใส่ชื่อบัญชีใดใน gm_accounts ที่เจ้าของจะบูตด้วย** — เฟรมนี้ฆ่าเซสชัน
3. หลังแก้: บูต headless ให้ pf-adversary/ผู้ช่วยยืนยันไบต์เวอร์ชันบนสายตรงกับที่ RE พิน แล้วค่อยเปิด GT-101 รอบ 2 ให้เจ้าของ (นั่ง 7 นาที)
4. chief: ใบ CHIEF-REPLY 1200 ต้องแก้ชื่อบัญชี: บัญชีจริงคือ `localtest` (ตาราง accounts) — `attended_test` ใช้ไม่ได้

## หลักฐาน
- วิดีโอ + ภาพนิ่ง: pf_bridge\evidence_screens (ภาพจากเจ้าของ 2 ใบส่งในแชท attended; ผู้ช่วยจะวางสำเนาไฟล์ให้) · คอนโซลเต็ม: GameClient\capture_gt101_20260827_143419\server_console_live.out.txt (บรรทัด 194-236) · GAME log: capture_v141\GAME_20260827_143641_602267_55866.txt
- jobs: 1211 อ่านชื่อบัญชี · 1287 hold+resolve · 1288/1289 (รอบที่ถูกปิดทิ้ง) · 1291 boot · 1292 teardown · 1290 release · LOCK_GAME release note 14:41
