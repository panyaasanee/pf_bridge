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
- R239(5m7hpk) 2026-08-30T~11:5x+07:00 ไม่แก้ src รอบนี้: บริโภค COO-DECISION 1145 (รับข้อเสนอ (ก) ของ R238 -- จุดเสียบที่ 3 ผูกกับ GT-124/RE-125 ใบเดียว ไม่เปิด CORE-REQUEST แยก ไม่มีงานให้ทำจนกว่า GT-146 ปลด RE-125) · CORE-REQUEST audit ซ้ำ: ไม่มีใบค้างจริง · พบหนี้ใหม่ AGENTS.md วัดสด 46,597B (เพดาน 30,720B) และ EVIDENCE_GATES.md วัดสด 39,028B (เพดาน 15,360B เกิน 2.5x ไม่เคยถูกวัดซ้ำตั้งแต่แยกไฟล์ R216) -- ไม่ตัดกฎเองตามที่ AGENTS.md สั่งไว้ (ต้อง pf-adversary + ปลายทางที่ COO เคาะ) → เปิด CHIEF-ASK-COO 1156 เสนอปลายทาง UNATTENDED_RULES.md (วัดขนาดแล้ว 8,587B) · push แล้ว รอ merge PR pf_bridge#484 / server#305 -> rounds/R239_5m7hpk_third-insertion-point-folds-into-gt124-plus-agents-md-evidence-gates-cap-drift-reported.md
- R240(qq97gx) 2026-08-30T~13:0x+07:00 ไม่แก้ src รอบนี้: COO-DECISION 1249 อนุมัติ (ก) UNATTENDED_RULES.md, ปฏิเสธยกเพดาน (ข) EVIDENCE_GATES.md สั่งเสนอแยกไฟล์แทน → chief ทำ AGENTS.md split: ย้าย §9 (unattended, 8587B) ไป UNATTENDED_RULES.md ใหม่ คำต่อคำ + ย้ายเหตุผลกฎ restore-DB/pf-adversary-worktree ไป archive/AGENTS_HISTORY_20260828.md §11 (เดิม §7 ชนกับหัวข้อที่มีอยู่ -- pf-adversary จับได้ แก้เป็น §11) · แก้ EVIDENCE_GATES.md cross-ref §9 x4 จุด + GAME_TEST_QUEUE.md 6 จุด ให้ชี้ UNATTENDED_RULES.md แทน (pf-adversary จับจุดนี้ได้เช่นกัน ไม่งั้นค้างเป็น dead link ในไฟล์ใช้งานจริง) · AGENTS.md 46,597->38,024B (ยังเกินเพดาน ~7,300B รายงานตรง) · แก้เกณฑ์ ndjson ของ GT-128 (LANE-GM ชี้ผิดว่าเป็น GT-127 แต่ตัวจริงอยู่บล็อก GT-128 -- GT-127 มี P1 ของตัวเองแข็งแรงอยู่แล้ว) เป็นรูปนับ record_id ไม่ซ้ำ ครอบคลุมแถวที่สามจาก GM-040 · ยืนยัน GM-040 ปิดครบสองครึ่ง · CORE-REQUEST audit ซ้ำ: ไม่มีใบค้างจริง · EVIDENCE_GATES.md split proposal (COO 1249 ข้อ (ข)) ยังไม่เสนอ -- ต้องเสนอรอบหน้า ไม่งั้น COO ESCALATION · stub 4 ใบ · push แล้ว รอ merge PR pf_bridge#488 -> rounds/R240_qq97gx_agents-md-split-unattended-rules-plus-gt128-ndjson-criterion-fix.md
- R241(8i0lto) 2026-08-30T~13:5x+07:00 ไม่แก้ src ทั้งสอง repo รอบนี้: CORE-REQUEST audit ซ้ำรอบที่ 4 ติด (ไม่มีใบค้างจริง) · stub ย้อนหลัง 2 ใบ COO-DECISION ที่ถึง chief ไม่เคยมีไฟล์ (1145 ใช้จริงแล้วตั้งแต่ R238/239 · 2255 ตรวจ 8 รายการยังไม่ครบ บันทึกตรง) + stub LANE-B-STATUS 1336 (กู้ PR #476/#490/#300) · 🎯 EVIDENCE_GATES.md split proposal ตาม COO 1249 ข้อ (ข) กำหนดครบสองรอบพอดี: วัด B จริงทีละหัวข้อ เสนอ 3 ไฟล์ (EVIDENCE_GATES.md แก่นเดิม 18,890B ยังเกินเพดาน เสนอ COO ตัดสินเพดานใหม่ + PROCESS_GATES.md ใหม่ 11,211B + V141_FREEZE.md ใหม่ 7,416B) รอ COO อนุมัติก่อนตัดจริง -> notes_to_chief/20260830_1356_CHIEF-ASK-COO-evidence-gates-md-split-proposal-three-files.md · push แล้ว รอ merge PR pf_bridge#492 / server#310 -> rounds/R241_8i0lto_evidence-gates-md-split-proposal-plus-mailbox-stub-backlog.md
- R242(6yjio0) 2026-08-30T~14:5x-15:0x+07:00 ไม่แก้ src ทั้งสอง repo รอบนี้: CORE-REQUEST audit ซ้ำรอบที่ 5 ติด (ไม่มีใบค้างจริง) · 🎯 **`EVIDENCE_GATES.md` split ตัดจริง** ตาม `COO-DECISION 1441` (ไฟล์ดริฟท์ 39,517B->43,020B ระหว่างใบขอกับใบอนุมัติเพราะ §12 ใหม่ลง main กลางทาง — พับเข้าไฟล์หลักเป็น §5 ใหม่ เปิดเผยเป็นการเบี่ยงจากโครงที่อนุมัติเป๊ะ ๆ ในคำนำ) เป็น `EVIDENCE_GATES.md` (คำนำ+§1-4+§5ใหม่ 24,803B ใต้เพดาน 25,600B) + `PROCESS_GATES.md` ใหม่ (เดิม §5-7,9-11 = 13,339B) + `V141_FREEZE.md` ใหม่ (เดิม §8 = 8,610B) ย้ายคำต่อคำ · แก้ cross-ref 6 จุดใน `AGENTS.md` · pf-adversary รีวิวก่อน commit: ยืนยัน byte-identical ทุกก้อน เจอ 3 จุดสถานะเก่า (เพดาน 15KB ค้างที่ AGENTS.md:11, ป้าย "(เดิม §12)" หาย, รอยต่อเลขหัวข้อ 7->9 ไม่มีหมายเหตุ) แก้ครบในคอมมิตตาม · เปิด CHIEF-ASK-COO 1504 ถามกระบวนการ (ไฟล์นี้ดริฟท์ระหว่างขอ/อนุมัติเป็นรอบที่สองในสามรอบ ไม่บล็อกงานอื่น) · stub 8 ใบ · push แล้ว รอ merge PR pf_bridge#499 / server#315 -> rounds/R242_6yjio0_evidence-gates-three-file-split-executed-plus-adversary-fixes.md
- R243(3ru85y) 2026-08-30T~16:0x-16:2x+07:00 ต่อสาย COO-DECISION 1541 (กำหนด 21:00): 🎯 `GT-127` HOLD ปลด (ป้ายค้าง ไม่ใช่โค้ดค้าง -- `CORE-REQUEST-GM-032` ข้อ 1-3 ครบบน main มาตั้งแต่ก่อนรอบนี้ ยืนยันซ้ำด้วยเทสสด `QueuedRowLandsEndToEndTests`) + 🎯 `GT-128` โทเคน `GM_WARP_POSITION_TARGET_MATCH`/`_MISMATCH` ลงจริงตาม `CORE-REQUEST-GM-030`/`-031` (เพิ่มจากโทเคนเดิม ไม่แทนที่ · เทสใหม่ 5 ใบรวม stale-target regression · สวีต 5480 passed เขียว(cloud sanity)) · 🔴 pf-adversary พบ: กิ่ง `unknown_character_mismatch` เป็น dead code จริง (การ์ดเดิมดักก่อนเสมอ) เขียน nonclaim ลงคอมเมนต์ + ถามลำดับการ์ดกลับ LANE-GM/COO · พบบั๊กเดิมแยกต่างหาก (rearm ตัวละครอื่นก่อน TargetPos ทำให้โทเคนทั้งชุดเงียบ) รายงานไม่แก้ · 🔴🔴 `GT-128` ทั้งใบยังบูตไม่ได้: `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED` ยัง `None` (ล็อกแยกโดย COO 2130 คนละขั้นจาก "พิมพ์โทเคน") ส่งคำถามปลดล็อกกลับ COO · มายด์บ็อกซ์: revert การเข้าใจผิดของตัวเอง (9 ใบที่มี stub อยู่แล้วจริง แค่ไม่มีสำเนาใน consumed/ -- ไม่ใช่เกณฑ์ "ยังไม่บริโภค") + stub ใหม่ 2 ใบถึง chief จริง (1541 x2) · CHIEF_CONTINUATION.md 30,525B->22,235B (ย้าย R224-R230 ไป archive) · push แล้ว รอ merge PR pf_bridge# / server# -> rounds/R243_3ru85y_gt127-hold-lifted-plus-gt128-tokens-wired-and-adversary-findings.md
- R244(7ohcx5) 2026-08-30T~16:5x-17:1x+07:00 สองงานที่ COO/LANE-B มอบให้รอบนี้ ทั้งคู่สอบแล้วไม่ทำ: 🔴 `FORCE_POS_VITAL_VERSION_CONFIRMED` unlock (COO-DECISION 1645) แก้ค่าคงที่+สองไฟล์เทสที่ล็อกไว้ตามสั่งจริง แต่เจอ **11 เทสแดงใหม่ใน 5 ไฟล์ที่ใบสั่งไม่ได้ระบุ** (เทสที่อ่านค่าคงที่ shipped ตรง ๆ แทนที่จะ mock.patch เพราะ shipped-None เคยเท่ากับ withheld มาตลอด) -- revert กลับที่เดิมทั้งหมด `git status` สะอาด ไม่ unlock รอบนี้ · 🔴 LANE-B's CORE-REQUEST (ย้าย `loot_actions` มาก่อน `MOB_DEATH_DYING`/`DEAD`) ขัดตรงกับ invariant ของ `CORE-REQUEST-007` เดิมที่ยืนอยู่จุดเดียวกัน ("AFTER the whole death schedule ... never between") -- ไม่ทำ ส่งคำถามกลับ COO/LANE-B ว่า invariant นี้ยังยืนไหม · ✅ สิ่งที่ทำสำเร็จ: แก้คอมเมนต์ล้าสมัยใน `runtime.py` (สาย A ชี้), ปิดหัวใบ `RE-156` ใน `CLIENT_RE_QUEUE.md` ตามที่สาย A ขอ, consume mailbox 13 ใบถึง chief พร้อม stub, เขียน CHIEF-REPLY รวมทุกข้อค้นพบ · ตรวจ `lane_hooks/` (สร้างไว้แล้วรอบก่อน) ยังทำงานปกติ ไม่ต้องสร้างใหม่ · ledger PASS 47 · สวีตเต็ม 5509 passed เขียว(cloud sanity) · round B: R243 ทั้งสอง repo merged=true ยืนยันด้วย `pull_request_read get` ไม่มีของหาย · push แล้ว รอ merge PR pf_bridge#510 / server#320 -> rounds/R244_7ohcx5_force-pos-unlock-and-loot-reorder-both-blocked-comment-fix-mailbox.md
- R245(nnlka4) 2026-08-30T~17:5x-18:0x+07:00 ไม่แก้ src ฝั่ง server รอบนี้: 🎯 **`pf_bridge/.github/workflows/merge-claude-pr.yml` แก้บั๊กจริง** ตาม KA1A-FINDING (`#507` ค้าง draft ~1ชม. ทำให้ LANE-A เห็น PR ของตัวเองแล้วจบรอบทันทีถูกต้องตามกติกา แต่ reap เก่า `PF_STALE_HOURS=2` (2 ชม.) ช้ากว่าคาบรายชั่วโมงของเลนเอง ⇒ อาจอดตายได้ถึงสองรอบ) เปลี่ยนเป็น `PF_STALE_MINUTES=45` (สั้นกว่าคาบ 1 ชม. แต่พอสำหรับรอบปกติ) แก้ `LIMIT`/ข้อความครบทุกจุด ผ่าน dup-key check + `bash -n` + ASCII scan ตามกฎหัวข้อ 7 · server ฝั่ง `merge-claude-pr.yml` ไม่แตะ (คนละสถาปัตยกรรม `decide`/`reap` ผูกกับเกต ต้องอ่านแยก) · 🎯 `GT-145` แก้ sha256 ฝังตายในหัวใบเป็นอ้าง `CANON_SHA.txt` ตามที่ RESULT letter ขอ (ค่าเก่าจะทำให้บูตครั้งหน้า ABORT ผิด) + ปิดสถานะ PENDING->DONE (ครบ 5 เกณฑ์ wire/DB, N/A client-observable ตามใบเอง) · 🎯 ตอบคำถามสาย GM เรื่อง `spawn` (pf-static-re สืบรอบสอง อิสระจากที่สาย GM grep เอง): **bounded-negative ยืนยัน** ไม่มี factory สร้างมอนกลางเซสชันที่ไหนใน `src/`/`gm/` เลย เจอใกล้เคียงที่สุดคือ diagnostic scaffold ตอนบูต (ไม่ใช่ precedent) · เลื่อน `FORCE_POS` unlock (กำหนดใหม่ COO 08-31 09:00, ต้องอ่านเทส 11 ตัวทีละตัวรอบที่มีเวลาพอ) + `gate-windows.yml` cp874 policy vs `runtime_console.py` utf-8 constant (ตัดสินใจของ chief ตาม GT-145 nonclaim ต้องคิดรอบหน้า ไม่รีบแก้ไฟล์ที่ทุกรอบ unattended ต้องบูตผ่าน) · stub 8 ใบ (KA1A-FINDING, 4 COO-DECISION, GT-145-RESULT, LANE-GM-REPLY, LANE-GM-STATUS เก่าที่ล้าสมัยแล้ว) · ledger PASS 47 · สวีตเต็ม server ไม่เปลี่ยน (baseline sanity) 5509 passed เขียว(cloud sanity) · round B: R244 ทั้งสอง repo merged=true ยืนยันด้วย `pull_request_read get` ไม่มีของหาย · push แล้ว รอ merge PR pf_bridge#513 / server#322 -> rounds/R245_nnlka4_merge-workflow-stale-draft-fix-gt145-canon-sha-plus-spawn-factory-bounded-negative.md
- R246(bunu7v) 2026-08-30T~19:0x-19:2x+07:00 แพตช์บั๊กจริงทั้งสอง repo: draft PR ที่ token เอเจนต์ปลดไม่ได้ (403 บน `#507`) จะเคยติดถาวร/หายเป็นรอบตาย ⇒ ให้ `reap` ลอง `gh pr ready` ด้วย token ของ workflow เองก่อน (ยังไม่เคยเห็นสำเร็จจริง — pf-adversary จับได้ว่าผมเขียนมั่นใจเกินจริงตอนแรก แก้เป็น `[PROPOSED, UNTESTED]` แล้วทั้งคู่ + เพิ่มบริบทลง close-comment ของ server) · แก้ `cloud_round_lock.json` คำรับประกันเท็จ + เขียน `PR_STATE.txt` (COO 1841 x2) · ต่อจุดเสียบ `CORE-REQUEST-GM-041` (`gm_npc_toggle_recompose.py` — คำตอบวันนี้คือ False ทุก mob_id, ไม่มี state store ให้อ่าน, pf-adversary จับ overclaim ในดอกสตริงแก้ก่อน commit) · `RE-162` เปิดและปิดในรอบเดียวตาม PANYA-ORDER — ผล MIXED ไม่ใช่ bounded-negative ที่คาด: กลไกเปลี่ยนแมพกลางเซสชันมีจริงและ merged แล้ว (`_dispatch_columbus_quest3021`) แต่ยังไม่มีใครยืนยันจอจริง (`GT-106` PENDING ตรงคำถามพอดี) `/warp` ไม่ใช้กลไกนี้เพราะนโยบายไม่ใช่ช่องว่างหลักฐาน — ทำตามสัญญาผู้บริโภคครบ (CHIEF-REPLY + GT-106 update + แจ้งเจ้าของตรง) · `RE-157` ปิด (analysis) สองการ์ดที่ต้องสร้าง (TradeCmd active-session stamp, mob-combat announced-membership) ยังไม่ได้สร้างจริง เป็นงานรอบหน้า · CORE-REQUEST-007 ยืนตามเดิม (COO 1841) · consume 11 ใบ stub ครบ · เก็บกวาด CHIEF_CONTINUATION R231-R238 → archive · สวีตเต็ม 5524 passed 0 failed เขียว(cloud sanity) ledger PASS 47 · push แล้ว รอ merge PR pf_bridge#518 / server#326 -> rounds/R246_bunu7v_workflow-draft-lock-fix-both-repos-plus-gm-041-wired-and-re-162-opened.md
