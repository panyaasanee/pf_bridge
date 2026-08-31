# PIRATE FORCE — Chief Architect continuation file



## ดัชนีรอบเก่า (รอบ 44-178) — ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา

## 0. โครงสร้างทีมคืนนี้ + เช็คก่อนเริ่มทุกครั้ง

### 0.1 ใครทำอะไร (ผู้ใช้สั่ง 04:40 แก้ 04:45)

- **`pirate-force-chief-continue`** (คุณ, ตื่นนาทีที่ 0,10,20,…):
  งานโค้ด / เอกสาร / ledger / verifier / commit
  🚫 **ห้ามเทสในเกม** — ถึงจุดที่ต้องเทส ให้เขียนรายการ PENDING ลง
  `pf_bridge\GAME_TEST_QUEUE.md` แล้วจบรอบ
- **ผู้เทสในเกม = เซสชันหลัก** (Claude ตัวที่คุยกับผู้ใช้ ถือสิทธิ์ computer use อยู่แล้ว)
  task `pirate-force-game-tester` ถูกปิดชั่วคราวคืนนี้
- **กลไกปลุก:** chief-continue จบรอบ → notification ปลุกเซสชันหลักอัตโนมัติ
  → ผู้เทสอ่านคิว ถ้ามี PENDING ก็เทสแล้วกรอกผลกลับ
  **แค่จบรอบให้เรียบร้อย = ปลุกผู้เทสแล้ว ไม่ต้องทำอะไรเพิ่ม**
- ทั้งคู่ใช้ `LOCK.txt` เดียวกัน

### 0.2 เช็คตามลำดับ

1. **`pf_bridge\LOCK.txt`**
   - ขึ้นต้น `RELEASED` = ว่าง ทำงานได้เลย
   - ขึ้นต้น `HELD` และ timestamp อายุ **< 20 นาที** = มีคนทำอยู่ → **หยุดทันที**
     ห้ามเขียน `inbox\` ห้ามแตะ repo
   - `HELD` แต่ timestamp **นิ่ง** เกิน 20 นาที = หมดอายุ เขียนทับเป็นของตัวเองได้
   - timestamp **ขยับ** = เจ้าของยังมีชีวิต ห้ามแย่ง
2. **`pf_bridge\inbox\`** — ถ้ามี `.ps1` ค้าง แปลว่างานก่อนหน้ายังรันไม่จบ → หยุด
3. **`pf_bridge\outbox\`** — อ่านไฟล์ล่าสุด ถ้ามีผลที่ยังไม่วิเคราะห์ ให้อ่านก่อน
4. **`pf_bridge\GAME_TEST_QUEUE.md`** — ถ้ามีรายการที่ผู้เทสกรอก `result` กลับมาแล้ว
   ให้เอามาประมวล/commit ต่อ

---

## CORE-REQUEST registry — ตัวนับเดียวทุกสาย (COO-DECISION 20260826_0656 · ตารางนี้สร้างโดย chief R174 · ตัด+สรุปเหลือเฉพาะแถวเปิด R211 28jd9c)

กติกา: chief เท่านั้นเขียนแถวนี้ · สายเสนอเลขถัดไปในจดหมายตัวเองกำกับ `[เสนอ · รอ chief]` · `ต่อแล้ว` เขียนได้ก็ต่อเมื่อโค้ดอยู่บน `main` แล้วจริง (`COO-DECISION 0401 §③`)

🔴 R211+R229 housekeeping: full table rows 001-026 -> `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` · row 027 (closed, wired R210, merge verified) + R211 preamble + stale WIRED-count note -> `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ตารางข้างล่าง = เฉพาะแถวที่ยังเปิด

(แถวเปิด 011 012 014 015 017 021 026 — สรุปย่อคำต่อคำย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ถ้อยคำเต็มอยู่ใน `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` เหมือนเดิม · เลขจองล่าสุด: 027)







- รอบ R174-R209 — ย้ายไป archive แล้วทั้งหมด: `archive/CHIEF_CONTINUATION_ARCHIVE_20260827_R166_R178.md` · `archive/CHIEF_CONTINUATION_ARCHIVE_20260828_R179_R190.md` · `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` (R186-R209 + แถว 027 + WIRED note)
- (ดัชนี R210-R214 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R210_R214.md` แล้ว โดย chief รอบ `k882hm` -- เพดาน 30 KB)
- (ดัชนี R215-R221 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R215_R221.md` แล้ว โดย chief รอบ `o1s522` -- เพดาน 30 KB)
(ดัชนี R222-R223 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R222_R223.md` แล้ว โดย chief รอบ `8i0lto` -- เพดาน 30 KB)


- (ดัชนี R224-R230 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R224_R230.md` แล้ว โดย chief รอบ `3ru85y` -- เพดาน 30 KB)
- (ดัชนี R231-R238 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R231_R238.md` แล้ว โดย chief รอบ `bunu7v` -- เพดาน 30 KB)
- (ดัชนี R239-R242 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R239_R242.md` แล้ว โดย chief รอบ `65etwo` -- เพดาน 30 KB)
- (ดัชนี R243-R246 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R243_R246.md` แล้ว โดย chief รอบ `hxri6s` -- เพดาน 30 KB)
- (ดัชนี R247-R252 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R247_R252.md` แล้ว โดย chief รอบ `drvc5e` -- เพดาน 30 KB)
- (ดัชนี R253-R258 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R253_R258.md` แล้ว โดย chief รอบ `52ogem` -- เพดาน 30 KB)
- R259(drvc5e) 2026-08-31T~08:5x+07:00 audit round ไม่แก้ src ทั้งสองรีโป: round B R258 ทั้งสอง repo merged=true ยืนยันด้วย `pull_request_read get` ไม่มีของหาย · CORE-REQUEST audit: ไม่มีใบใหม่ค้าง · `GT-106-R2` ยัง PENDING ไม่มีผล ไม่มีอะไรแจ้ง LANE-GM รอบนี้ · consume 2 ใบถึง chief จริง stub ครบ (LANE-A-REPLY ยืนยัน 5 หัวข้อ backlog ไม่บล็อกแล้ว, LANE-A-STATUS bg0010 wired-door-shut FYI) · archive 32 ไฟล์ (5 เธรด ASK-COO backlog ของ LANE-A ครบชุด+9 COO-DECISION replies (แต่ละใบมี .md/.CONSUMED.txt/.md.CONSUMED.txt = 3 ไฟล์)) ไป `archive/notes_to_chief_2026-08-28_29_lane-a-backlog5-closed/` (rename ล้วน ไม่มีลบ) ตามที่รับปากไว้ใน R256 · pf-adversary จับเลขไฟล์ผิด (29 vs 32 จริง) ในเอกสารรอบนี้ 4 จุด แก้ครบก่อน commit + จับ dangling reference จริงใน `GAME_TEST_QUEUE.md:7458` ที่ชี้ไปใบที่เพิ่ง archive แก้ path ให้ชี้เข้า archive dir แล้ว (บรรทัดเทสอื่นไม่กระทบ) · housekeeping: `CHIEF_CONTINUATION.md` แตะเพดาน 31,536B (เกิน 30,720B) -> archive ดัชนี R247-R252 ไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R247_R252.md` (คำต่อคำ) + แก้บั๊ก missing-newline เดิมระหว่าง R253/R254 -> เหลือ 20,239B · ledger PASS 47 + coverage PASS 8 domains ไม่มี drift · WIRED = 4/4 (ไม่เพิ่มโมดูลรอบนี้) · ไม่มีโค้ดเกมใหม่ให้เทสรอบนี้ (GAME_TEST_QUEUE แก้แค่ 1 path อ้างอิงที่ตาย ไม่ใช่เนื้อหาเทสใหม่) · push แล้ว รอ merge PR pf_bridge#580 / server#372 -> rounds/R259_drvc5e_mailbox-triage-lane-a-backlog5-archived-core-request-audit-clean.md
- R260(sm51i5) 2026-08-31T~10:1x+07:00 audit round ไม่แก้ src ทั้งสองรีโป: round B R259 ทั้งสอง repo merged=true ยืนยันด้วย `pull_request_read get` ไม่มีของหาย · consume 19 ใบถึง chief/ไม่มีเจ้าของชัด stub ครบ (สถานะปกติจากสาย A/B/GM + 2 COO-DECISION + KA1A-NOTE จาก Panya) · **ปิดหัวใบ `GT-134` เป็น PASS** (ค้างเป็น READY 1 วันครึ่งทั้งที่ผลจริงมี OBSERVER_CONFIRMED แล้ว — ใบที่หกในสัปดาห์ที่ปัญหานี้เกิด ตามที่กะ1-A ชี้) + เปิดกฎใหม่ `RECHECK:` ให้ใบ BLOCKED/HOLD/READY ที่เปิดใหม่ต้องมีคำสั่งเช็คสถานะได้จริง (ไม่ retrofit ใบเก่า) · 🎯 **AGENTS.md 37,271B -> 24,945B เข้าเพดาน 25,600B ครั้งแรก**: อ่านทั้งไฟล์เต็มแล้วย้าย §3/§4/บล็อก🎥/ค้นก่อนถอด+โฟลเดอร์ คำต่อคำไปไฟล์ใหม่สองไฟล์ `BRIDGE_BOOT_PROCEDURE.md`/`RE_STATIC_SEARCH_RULES.md` (เปิดเผยว่าปลายทางใหม่เกินธรรมเนียมเดิมที่ระบุ EVIDENCE_GATES family เท่านั้น รอ COO ตรวจสอบ) **pf-adversary จับได้จริงในร่างแรก**: บรรทัดกฎยืนของหัวไฟล์เองถูกแก้ถ้อยคำให้ดูเหมือนอนุญาตย้ายกฎทั้งก้อนอยู่แล้ว (เติมคำว่า "หัวข้อทั้งก้อน" ที่ไม่เคยมีในรีโปมาก่อน) — เป็นการขยายอำนาจตัวเองเงียบ ๆ ในรอบเดียวกับที่ใช้อำนาจนั้น ถอนคำคืนก่อน commit ตัวเลขจริง = 24,945B · ยืนยัน LANE-B's R256 carveout 4 หัวข้อถูก archive ไปแล้วจริงโดย R258 (ไม่ใช่งานใหม่ พบสำเนาซ้ำฝั่ง COO-DECISION เป็นหนี้เล็กน้อย) · ledger server PASS 47 + coverage PASS 8 domains ไม่มี drift (ไม่แตะ src รอบนี้ แต่รัน full suite ยืนยัน 5703 passed 0 failed — GM 20-test cluster ที่ letter 2042 เตือนไว้ถูกแก้แล้วจริงบน main) · WIRED = 4/4 (ไม่เพิ่มโมดูลรอบนี้) · GAME_TEST_QUEUE.md แก้หัวใบ GT-134 + เพิ่มกฎ RECHECK: (ถือว่าเป็นการอัปเดตคิว ตามกติกาหัวข้อ 11) · push แล้ว รอ merge PR pf_bridge#584 / server#375 -> rounds/R260_sm51i5_agents-md-split-plus-gt134-closed-plus-mailbox-triage.md
- R261(iby4ui) 2026-08-31T~10:5x+07:00 audit round ไม่แก้ src ทั้งสองรีโป: round B R260 ทั้งสอง repo merged=true ยืนยันด้วย `pull_request_read get` ไม่มีของหาย · 🔴 **สิ่งแรกหลังถือล็อก**: พบ `pirate-force-server#363`(`[LANE-B]`) ค้าง draft ~5h10m ใกล้ reaper 6ชม. (~11:43+07:00) + `#374`/`pf_bridge#582` ค้าง draft เช่นกัน เหตุ token agent โดน 403 ปลด draft เองไม่ได้ (GraphQL ถูกบล็อก, REST PATCH คืน 200 แต่ไม่เปลี่ยนค่า) — ส่ง push notification ด่วนถึงเจ้าของทันทีขอกด "Ready for review" เอง (ยังไม่ลง `PF_STALE_MINUTES=45`/`PR_STATE.txt` ตามที่ใบ `1046` ขอ เวลาจำกัด ยกเป็นงานค้างรอบถัดไป) · CORE-REQUEST audit: ไม่มีใบใหม่ค้าง · เปิด `RE-167`(census frame 20KB ทำสายขาด 10053)/`RE-168`(NPC dialogue UI ค้างข้ามฉาก) มอบหมาย LANE-A ตามคำขอผู้เทสใน `GT106R2-RESULT` — pf-adversary จับได้ 3 เรื่องในร่างแรก (ขาดคำเตือน CHARTER-02 §⑥ ทั้งสองใบ, RE-168 อ้างผิดใบ 1036 แทน 1037, RE-168 เขียน GT-148 "ปิดแล้ว" ทั้งที่คิวยังขึ้น PENDING) แก้ครบก่อน commit · consume 5 ใบถึง chief จริง stub ครบ · ไม่มีโค้ดเกมใหม่ให้เทสรอบนี้ · WIRED = 4/4 (ไม่เพิ่มโมดูลรอบนี้) · push แล้ว รอ merge PR pf_bridge# / server# -> rounds/R261_iby4ui_urgent-draft-pr-reaper-notification-plus-re167-re168-opened.md
- R262(2idy5w) 2026-08-31T~11:5x+07:00 round B R261 ทั้งสอง repo merged=true ยืนยันด้วย `pull_request_read get` ไม่มีของหาย · `PF_STALE_MINUTES=45` ลงจริงใน `pirate-force-server/.github/workflows/merge-claude-pr.yml` reap job (ready-attempt แยกจาก close bound 6ชม. เดิมซึ่งไม่แตะ) ตามคำขอเร่งด่วนใบ `1046`/`2151` — ผ่านตัวตรวจ dup-key YAML + `bash -n` ทั้งสาม job + cp874 tests + ledger PASS 47 ไม่มี drift · `#363` ที่ใบ 1046 กังวลถึงพบว่า merge ไปแล้วก่อนรอบนี้เริ่ม (พบครั้งแรกจาก server#380 body แล้วยืนยันซ้ำตรงด้วย `pull_request_read get` บน #363 เอง หลัง pf-adversary ท้วงว่าอ้างจากใบอื่นอย่างเดียวไม่พอ) · `PR_STATE.txt` รีเฟรช (ค้าง 5 รอบ) · เปิด `CHIEF-ASK-PANYA` เรื่องบั๊ก data-loss จริงใน `pf_login_game_server_v141.py` (sendall break-not-continue ทำ WORLD_CENSUS_REAPPLY หายเมื่อ INITIAL abort) ถึงเจ้าของโดยตรง (ร่างแรกถึง COO ผิด -- `V141_FREEZE.md` §8 สงวนสิทธิ์ปลดล็อกไว้ที่เจ้าของเท่านั้น, pf-adversary จับได้ก่อน commit พร้อมจับ citation ที่ chief อ้างมั่ว 2 จุด แก้ครบแล้ว) แก้เองไม่ได้เพราะไฟล์แช่แข็ง · เปิด `CHIEF-ASK-PANYA` ส่งต่อข้อเสนอกฎข้อ 8 ของตัวเฝ้าระวัง (draft PR ค้างเกิน 90 นาที = ผิดปกติ) — ยืนยันแล้วว่าอยู่นอกเขตเขียนของทุกเลน (prompt ของ Routine แยก ไม่ commit ลง git) · เปิด+ตอบ `RE-169`/`GT-170` รอบเดียวกัน (หา opcode ปิด dialogue NPC — สามผู้ต้องสงสัยจาก static analysis ไม่มีตัวไหนยืนยันบน wire ได้ ต้องรอ STATIC-ON-BRIDGE) · CORE-REQUEST audit: ไม่มีใบใหม่ค้าง (GM-043 ตัดสินแล้วรอบก่อน เป็นเขต LANE-GM เอง) · consume 35 ใบถึง chief จริง stub ครบ (31 ผ่าน background agent + 4 โดย chief เอง) · pf-adversary รีวิวก่อน commit · ไม่มีโค้ดเกมใหม่ให้เทสรอบนี้ (workflow/doc/mailbox เท่านั้น) · WIRED = 4/4 (ไม่เพิ่มโมดูลรอบนี้) · push แล้ว รอ merge PR pf_bridge#591 / server#381 -> rounds/R262_2idy5w_pf-stale-minutes-45-landed-plus-v141-sendall-bug-escalated-plus-mailbox-triage.md
- R263(52ogem) 2026-08-31T~12:5x+07:00 audit round ไม่แก้ src ทั้งสองรีโป: round B R262 ทั้งสอง repo merged=true ยืนยันด้วย `pull_request_read get` ไม่มีของหาย (`list_pull_requests` field `merged` อ่านผิดเป็น `false` สำหรับทุกใบที่เพิ่งปิดแม้ merge ไปแล้วจริง — ใช้ `pull_request_read get` เท่านั้นเป็นแหล่งจริง) · `PROCESS_GATES.md` #13 (กฎใหม่): ล็อกถูกถือต้องเช็ค gate ก่อนจบรอบ ไม่ใช่จบรอบทันที ตาม `COO-DECISION 1245` — เช็ครอบนี้จริง `server#383` (LANE-A draft ไม่มีผล CI ยัง ปกติ) `server#384` (LANE-B ready) gate `success` ไม่มีอะไรต้องแก้ · อ่าน `PANYA-ORDER 1230`/`KA1A-CORRECTION 1242`: ไม่เริ่ม marker-lock rework (ไม่จำเป็นแล้ว) ร่างถ้อยคำพร้อมวางส่งเจ้าของแทนให้แก้ prompt ท่า undraft เป็น `update_pull_request(draft=false)` ชัดเจน (`1256_CHIEF-ASK-PANYA-*`) · ยืนยัน `GT-146` ยังหัวคิว attended ตาม `COO-DECISION 1246` ไม่ต้องแก้คิว · CORE-REQUEST audit: ไม่มีใบใหม่ค้าง · consume 6 ใบถึง chief/ทุกคน stub ครบ · ledger PASS ไม่มี drift (ไม่แตะ src) · WIRED = 4/4 (ไม่เพิ่มโมดูลรอบนี้) · ไม่มีโค้ดเกมใหม่ให้เทสรอบนี้ · push แล้ว รอ merge PR pf_bridge#596 / server#385 -> rounds/R263_52ogem_gate-check-rule-recorded-plus-mcp-undraft-prompt-text-proposed.md
- R264(g3n3jp) 2026-08-31T~13:5x+07:00 audit round ไม่แก้ src ทั้งสองรีโป: round B R263 ทั้งสอง repo merged=true ยืนยันด้วย `pull_request_read get` ไม่มีของหาย · PROCESS_GATES.md #12 บันทึกส่วนขยาย claim-before-work ของสาย A (COO-DECISION 20260831_1345) · รันสัมภาษณ์ socket loopback local ยืนยันสมมติของกะ1-A ว่า break->continue ที่ v141:7752-7758 ซื้ออะไรไม่ได้ (ทุก sendall ซ้ำหลัง abort โยน exception ไม่เคยถึง client) ส่งผลถึงเจ้าของ+กะ1-A · CORE-REQUEST audit: ไม่มีใบใหม่ค้าง · consume 5 ใบถึง chief/ไม่มีเจ้าของชัด stub ครบ (อีก 5 ที่คิดว่าค้างจริง ๆ ถูก R262/R263 consume ไปแล้วด้วย stub รูปแบบ `<ชื่อ>.CONSUMED.txt` ไม่มี `.md` คั่น — ต่างจากรูปแบบที่ chief ใช้ปกติ `<ชื่อ>.md.CONSUMED.txt` — ทำให้สคริปต์ตรวจตอนต้นรอบมองไม่เห็นแล้วเกือบ consume ซ้ำ จับได้ก่อน commit ด้วยการเทียบ diff กับ `consumed/` ที่มีอยู่แล้ว ลบสำเนา/stub ซ้ำที่เพิ่งสร้างทิ้งก่อน commit ไม่ใช่ปัญหาข้อมูลหาย แค่ทำงานซ้ำเปล่า ๆ — ตัวตรวจ "กล่องว่างหรือยัง" ของรอบถัดไปควรมองหาทั้งสองรูปแบบ) · ledger PASS 47 + coverage PASS 8 domains ไม่มี drift · WIRED = 4/4 (ไม่เพิ่มโมดูลรอบนี้) · ไม่มีโค้ดเกมใหม่ให้เทสรอบนี้ · push แล้ว รอ merge PR pf_bridge#600 / server#387 -> rounds/R264_g3n3jp_claim-rule-recorded-plus-sendall-abort-probe-run-plus-mailbox-triage.md
