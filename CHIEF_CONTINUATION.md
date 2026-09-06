# PIRATE FORCE — Chief Architect continuation file

## 🔴 ลำดับงานปัจจุบัน — ไมล์สโตนเปิดกลับมา ไม่มีกำหนดวัน (`PANYA-DECISION 20260904_0233` ผ่าน `COO-DECISION 0243` · แทนคำสั่งพัก 2026-09-01T02:15 เดิม)

อ่านหัวข้อนี้ก่อนมอบหมายงานใดๆ ทุกรอบ — milestone (M1-M final/CHARTER-02) กลับมามอบหมายได้ตามปกติ **ห้ามรายงาน
"เลยกำหนด" อีก** (ไม่มีคอลัมน์กำหนดแล้ว) ผ่าน M(n) ก่อนจึงประกาศ v(n) ใบเต็ม:
`notes_to_chief/20260904_0233_*.md` · `notes_to_chief/20260904_0243_COO-DECISION-*.md` ·
ประวัติการพัก: `notes_to_chief/consumed/20260901_0215_PANYA-ORDER-*.md`

### CHARTER-02 — บันไดไมล์สโตน (คอลัมน์ "กำหนด" ถูกลบตาม `0243` ข้อ 2 · กฎสี่ข้อของเวอร์ชัน + วินัยหลักฐานคงเดิม)

- ✅ **M1/v1** เมืองมีชีวิต — ประกาศแล้ว (R249)
- ⏳ **M2/v2** ออกจากเมืองได้ — เหลือเกณฑ์เดียว: แล่นเรือชนเกาะ → หน้า "รายงานกัปตัน เรือเทียบท่า [ชื่อเกาะ]"
  เด้งเอง (ไม่ต้องคลิก · `PANYA-INFO 20260904_0409`) → ผู้เล่นกดยืนยัน → วาปเข้าเกาะ 2 (Prison Exile) และเกาะ 3
  (Spice Paradise) ได้จริงบนจอ **ทั้งสองเกาะ** → **LANE-A**
  🔴 **แก้ถ้อยคำโดย chief รอบ `3kwnnr`/R332 ตาม `COO-DECISION 20260904_0344` ข้อ 2** — ~~"ใกล้เกาะ client ยิง
  `TriggerVital` (`0x1FB2`) → server ตอบ"~~ **ถอน หักล้างแล้ว**: `0x1FB2` id 40/51/3/57/36 = trigger prop
  กลางทะเล (Seafood Cargo/Offer Altar/…) ไม่ใช่ทางเข้าเกาะ (`LANE-A 20260904_0300` จาก
  `TEXTDATA_TH__Trigger_TIP.tsv`) · **อะไรเปิดหน้ารายงานกัปตันยังไม่รู้ = ใบ RE ของ LANE-A** (ร่างรอบ 04:21 ·
  chief ตั้งเลขในรอบที่ใบถึง ตาม `0344` ข้อ 3) · ห้ามใบเทสใบไหนถือ `0x1FB2` เป็นฐานของ "เทียบท่า" อีก
- **M3** สนามมีมอนสเตอร์ (= P-2 ยกระดับ): สีชื่อมอนถูกตามสถานะ **และ** attr + relation/faction ของมอนถูกจริง
  ไม่ใช่แค่ทาสี → LANE-GM (สี) ร่วม LANE-B (attr/relation ของ roster)
- **M4** ตีได้ตายได้ — สี่ข้อครบบนจอ: (1) มอนตีกลับ HP ผู้เล่นลดจริง (2) ตายถูกต้อง ท่าตาย/ชื่อเทา/ไม่มี
  ข้อความ-ตัวนับของผู้เล่น (3) ศพไม่แข็งค้าง (4) เกิดใหม่ได้ (`GT-224`) → LANE-B
- **M5** เก็บของได้ (คงเดิม) — เก็บได้ + รอด relog · หนี้: ของผี 120 วิ · หาง P-1 · ไอคอน/ใช้ของ → LANE-B
- **M final** (ไม่มีเลข แทน M6) — เกมเล่นได้ครบวงจร เกิด-เดินทาง-สู้-เก็บ-โต-กลับมา

- **P-1** ของดรอปต้องอยู่บนพื้นนานพอให้เดินไปเก็บทัน → **LANE-B** (ตัวหลักติ๊กแล้ว · หางค้าง: กะพริบหลัง
  `#689` + หนี้ `DropLedgerCell` = `GT-225`)
- **P-2** สีชื่อมอนต้องถูกสถานะ: ปกติ=ส้ม / สู้=แดง / ตาย=เทา (ห้ามชมพู) → **LANE-GM** ร่วม LANE-B (attr/relation)
  — เกณฑ์ผ่าน M3 ตั้งแต่ `0233`
- **P-3** ทุกปุ่ม/ทุกฟังก์ชันใน GMUI ทั้ง 3 หน้าต้องทำงานจริงครบทุกตัว → **LANE-GM**
- 🆕 UI-A/UI-B (ปุ่มกลับหน้าเลือกตัวละคร/logout) **ย้ายเจ้าของจาก LANE-A ไป LANE-UI** ตาม
  `notes_to_chief/20260904_0330_COO-DECISION-*.md` — ดูหัวข้อ "ทีมและเขตเขียน — สายที่ 6/7" ด้านล่าง
- 🆕 GM-B `/speed` เจ้าของ **LANE-DB** (`COO-DECISION/ORDER 20260901_1059/1100/1101`)
- `GT-146`/ใบตีมอนทั้งหมด **ห้ามเข้าคิว attended** จนกว่า P-2 จะปิด (P-1 ผ่านจอแล้ว)
- **"ตัวละคร" (class/สแตท/HP จากตาราง class)** ไม่เปิดเลนใหม่ (`0243` ข้อ 3) — แถว typed HP/เลเวล = LANE-DB ·
  `class_id` NULL = chief (`GT-215`) · ค่าเริ่มต้น HP/สแตทจากตาราง class = chief ออก CORE-REQUEST ให้ LANE-DB
  เมื่อ `GT-215` ปิด — M4 ข้อ (1) ต้องมีแถวนี้ก่อน

`SERVER_VERSIONS.md` (ที่รากรีโปเซิร์ฟเวอร์) ตารางแผน v2-v-final: ลบคอลัมน์วันที่ตามเดียวกัน — งานถัดไปของ chief
(ยังไม่ลงรอบนี้ เพื่อคุมขนาด PR ให้อยู่หนึ่งเรื่องต่อใบ)

## ทีมและเขตเขียน — บล็อกประกาศตั้งสาย DB/CS/UI/Q ⇒ [`archive/CHIEF_CONTINUATION_ARCHIVE_20260906_lane_charters_db_cs_ui_q.md`](archive/CHIEF_CONTINUATION_ARCHIVE_20260906_lane_charters_db_cs_ui_q.md) (ย้ายทั้งบล็อกคำต่อคำ ไม่มีการลบ chief รอบ `l5tqxc`/R376 เพดาน 30 KB) · เขตเขียนสดของทุกสายอยู่ที่ `prompts/CHIEF.md` §6

## ดัชนีรอบเก่า (รอบ 44-178) — ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา

## 0. โครงสร้างทีมคืนนี้ + เช็คก่อนเริ่มทุกครั้ง ⇒ ย้ายคำต่อคำไป [`HOUSE_RULES.md`](HOUSE_RULES.md) (`COO-DECISION 20260903_0848` ข้อ ① · R317 `mgm333` · ไฟล์เป็น ๆ ไม่ใช่ `archive/` กฎยังมีผล ไม่มีอะไรถูกลบหรือย่อ)

---

## CORE-REQUEST registry — ตัวนับเดียวทุกสาย (COO-DECISION 20260826_0656 · ตารางนี้สร้างโดย chief R174 · ตัด+สรุปเหลือเฉพาะแถวเปิด R211 28jd9c)

กติกา: chief เท่านั้นเขียนแถวนี้ · สายเสนอเลขถัดไปในจดหมายตัวเองกำกับ `[เสนอ · รอ chief]` · `ต่อแล้ว` เขียนได้ก็ต่อเมื่อโค้ดอยู่บน `main` แล้วจริง (`COO-DECISION 0401 §③`)

🔴 R211+R229 housekeeping: full table rows 001-026 -> `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` · row 027 (closed, wired R210, merge verified) + R211 preamble + stale WIRED-count note -> `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ตารางข้างล่าง = เฉพาะแถวที่ยังเปิด

(แถวเปิด 011 012 014 015 017 021 026 — สรุปย่อคำต่อคำย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ถ้อยคำเต็มอยู่ใน `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` เหมือนเดิม · เลขจองล่าสุด: 031)

- 031 CORE-REQUEST (สาย A รอบ `xlraox` · `notes_to_chief/20260901_2007_LANE-A-CORE-REQUEST-logout-vitalcount-envelope-gap-classifier-built.md`) — UI-B "ออกจากเกม" จริงยาว 119 ไบต์ (`vital_count=4`) ไม่ใช่ 34 ที่ pin ไว้ (vital อื่นห่อมาด้วย) `classify_logout_attempt` เดิมเช็ค `vital_count == 1` ตกทันที ยืนยันด้วย parser จริง · **ต่อแล้ว (wired) รอบ `f7zt8z` (R295)**: `vital_count >= 1` + `nested_payload` เทียบแบบ branch ตาม `vital_count` (`==1` ยัง exact-equal เท่าเดิม กัน trailing-junk false-accept ที่ pf-adversary จับได้ · `>=2` เทียบ prefix 14 ไบต์) · full suite 6564/0 failed, ledger PASS=49 · `GT-194` `BLOCKED-ON-WIRING`→`READY` (RECHECK 1-3 ผ่าน) — ปิดสมบูรณ์ฝั่ง chief

- 030 CORE-REQUEST-GM-049 (สาย GM รอบ `nqba17`) — `/speed` sparse x=7 runtime send point · **ต่อสายแล้ว (wired) รอบ R294**, เขตเขียนปิดสมบูรณ์ฝั่ง chief · **`GT-193` ยังไม่ READY**: ครึ่ง DB-persistence ของ LANE-DB (`persistence_attr_compose.py`'s sparse write) ยังไม่ขึ้น main · ประวัติเต็ม (blocked/unblocked ข้าม R292-R294, COO gate สามเงื่อนไข, SENSITIVE_FIELDS caveat) → `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260901_row030_full_history.md`

- 028 CORE-REQUEST-GM-047 (สาย GM รอบ `bxkxfc` · P0) — cross-scene GM warp resync label fix, ต่อแล้ว (wired) ยืนยันรอบ `69r41m` (R283): `pf_bridge#680` + `pirate-force-server#452` merged · `GT-182` ปลดเป็น `BLOCKED-ON-ATTENDED` ถ้อยคำเต็ม: `archive/CHIEF_CONTINUATION_ARCHIVE_20260904_row028_full_text.md`

- 029 (สาย A รอบ `s3m1f7`) — ถอนแถว หลังตรวจพบว่าใบนี้ล้าสมัยไปแล้วก่อนถูกเปิดด้วยซ้ำ (ฉาก 4 ต่อสายครบอยู่ก่อนแล้ว server#465 ปิดถูกต้อง ไม่มีงาน chief) ถ้อยคำเต็ม: `archive/CHIEF_CONTINUATION_ARCHIVE_20260904_row029_full_text.md`







- ดัชนีรอบ R174-R288 ทั้งหมดย้ายไป archive แล้ว (เพดาน 30 KB, ยุบบรรทัดซ้ำรอบ `happy-dirac-69cabr` R294):
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260827_R166_R178.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260828_R179_R190.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` (R186-R209 + แถว 027 + WIRED note) ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R210_R214.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R215_R221.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R222_R223.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R224_R230.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R231_R238.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R239_R242.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R243_R246.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R247_R252.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R253_R258.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R259_R261.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R262_R264.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R265_R272.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R273_R280.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R281_R282.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R283_R284.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R285_R286.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R287_R288.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R289.md` (moved R296, size housekeeping)
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260902_R290_R291.md` (moved R297, size housekeeping)
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260902_R292_R293.md` (moved R297b, size housekeeping)
- (R294-R303 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md` แล้ว โดย chief รอบ `gjyxt5` (R324) 2026-09-03 ตามเพดาน 30 KB ของหัวข้อ 17 ข้อ 9 (ง) — ไม่มีบรรทัดไหนถูกลบ)

🔴 บรรทัดดัชนีต้องเป็น **หนึ่งประโยค** ชี้ไปไฟล์รอบเสมอ (prompt หัวข้อ 4) — R294-R297b เคยเขียนเป็นย่อหน้ายาว
รวม 9,772 ไบต์จากเพดาน 30 KB · ฉบับเต็มคำต่อคำอยู่ที่ `archive/CHIEF_CONTINUATION_INDEX_R294_to_R298_verbatim_20260902.md`
- ดัชนีรอบ R304-R321 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260904_R304_R321.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ ub8svt, เพดาน 30 KB)
- ดัชนีรอบ R322-R340b ด้านล่างนี้ถูกย่อเหลือหนึ่งประโยคต่อรอบ (chief รอบ ub8svt, เพดาน 30 KB) — ถ้อยคำเต็มคำต่อคำอยู่ที่ `archive/CHIEF_CONTINUATION_ARCHIVE_20260904_R322_R340b_verbatim.md`
- 🔴 ดัชนีรอบเก่ากว่า 20 รอบล่าสุด (RR322-RR341b) ⇒ [`archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md`](archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md) (ย้ายคำต่อคำ R360 · ไม่มีอะไรถูกลบ)
- ดัชนีรอบ R350-R357 -> ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R350_R357.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ `ald09i`/R367)
- ดัชนีรอบ R358-R360 -> ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R358_R360.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ `m6xifr`/R368)
- ดัชนีรอบ R361-R363 -> ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R361_R363.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ `m6xifr`/R369)
- ดัชนีรอบ R364-R366 -> ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R364_R366.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ `jz5vtt`/R370)
- ดัชนีรอบ R367-R369 -> ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R367_R369.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ `jz5vtt2`/R371)
- R370(jz5vtt) 2026-09-06T13:52-15:0x+07:00 takeover of `#1440` (>14h, dirty, NOW.md ghost) -- **PANYA-ORDER `1315` implemented**: the reaper's no-marker path now closes two owner-authorised categories in `pf_bridge/.github/workflows/merge-claude-pr.yml` -- (1) a stale claim (claim title + no `rounds/` file beyond `*_claim.md` + **head commit** older than `PF_REAP_STALE_CLAIM_HOURS=3`, so the `_claim.md` checkpoint COMMON already asks for buys another 3h; `updated_at` deliberately not used) and (2) an author-declared `SUPERSEDED-BY: #n`/`DUPLICATE-OF: #n` at line start in the body or the author's own latest comment, target must be a PR in the same repo, merged or open -- both keep the branch, both write `notes_to_chief/<time>_REAPER-CLOSED-<repo>-<n>.md` via the contents API · answered the owner's collision question: **no collision with `#1430`** -- that guard only looks at MARKED PRs, this only at UNMARKED ones, and both ask the same question with the same `PF_ROUND_FILE_FILTER` (one criterion, two paths) · 🔴 measured mismatch reported rather than papered over: category (1) **refuses `#1440`** because its branch does carry a real round file (R365, 71 lines) -- its real defect is `dirty`, so chief commented `SUPERSEDED-BY: #1491` and it goes out through category (2); widening (1) to catch it would also catch finished rounds still owed a marker · `server#894` commented `SUPERSEDED-BY: #906` (verified #906 merged and says so itself) · cross-repo record measured impossible today (`grep secrets\.` = 0 hit in both workflows) -> optional named secret `PF_BRIDGE_NOTES_TOKEN`, never a silent close · validation before push: duplicate-key-rejecting yaml load, `bash -n` on both `run:` blocks, ASCII-only, and a **10/10 logic self-test on fixtures before touching anything live** (R369's lesson applied in the right order) · did NOT touch any queue file on purpose (bridgesize red, ASK-COO `1234` unanswered, LANE-K is the clerk now) · 🔴 debt stated plainly: three CORE-REQUESTs needing `runtime.py` (UI `2006`, A `0914`, B `1952`) are R371 jobs 1-3, second round in a row they have not moved · `ADVERSARY_PENDING pf_bridge#1491` -> rounds/R370_jz5vtt_reaper_closes_ghost_claims_and_author_declared_supersedes.md
- R371(jz5vtt2) 2026-09-06T14:20-14:4x+07:00 [same session, follow-up to R370] pf-adversary's review of R370 returned AFTER that round unlocked and merged, and confirmed four ways the LIVE reaper could close something it must not, each with a fixture run rather than a reading: (1) category (2) had no time bound at all, so ONE comment carrying `DUPLICATE-OF: #n` closed a claim whose head commit was 10 minutes old -> **one clock for both categories, `IDLE = now - max(created_at, head commit date)` >= 3h**, the `created_at` floor also killing finding 14 (a resumed session pushing an old branch was closable seconds after opening) (2) no direction check, and `SUPERSEDED-BY:` is directional English whose natural error is to write it on the NEW pull request -> **target number must be `-gt` this PR's**, which also catches the cross-repo number the order's own example invites (`#906` exists in both repos) (3) the cycle guard read only the target's BODY while the order's prescribed flow puts the line in a COMMENT -> both PRs closed in one sweep; now reads body+comments and stops instead of falling through into category (1) (4) the OR'd >=20-line signal in `PF_ROUND_FILE_FILTER` made a fat `_claim.md` checkpoint permanently un-reapable (main really carries a 159-line one) -> stale-claim path uses a name-only `PF_REAP_CLAIM_FILE_FILTER`, size signal stays on the marker path where R364 put it · added `REAP-HOLD:`, both fence styles + unterminated fences, a warning on near-miss declarations (bold/bullet/trailing prose still do not match, on purpose), and `ADDRESSEE: COO` in the record letter · 🔴 **retracted R370's own advice**: do NOT create `PF_BRIDGE_NOTES_TOKEN` -- a pf_bridge-write token stored in the gated server repo is reachable by any agent round (gate triggers on `pull_request`, same-repo PRs get secrets) and would hand a cloud round the direct-`main`-write this entire lock design exists to deny; cross-repo record writing is DISABLED instead, loud in the log, and chief's next round records it · corrected a false sentence in R370's own round file (`PF_REAP_NOTE_REPO` WAS hardcoded; now derived from `github.repository_owner`) · self-test 16/16 covering every case the adversary measured, yaml duplicate-key check, `bash -n`, ASCII-only · NOT fixed, written down to be counted: the record covers 2 of 7 close paths, concurrent sweeps can print a FALSE `COULD NOT CLOSE`, the server-repo copy is still 0% (so `server#894`/`#886` are not yet automatic), and the `0005` non-claude-branch order overlaps this one · CORE-REQUEST UI `2006`/A `0914`/B `1952` slipped a third round -> R372 jobs 4-6, no further slip -> rounds/R371_jz5vtt2_pay_the_adversary_findings_on_the_live_reaper.md
- R372(fyrtvt) wired the three CORE-REQUESTs R371 owed (UI Exit Game real logout, A ground-drop persistence across relog, B mob respawn) into runtime.py, pf-adversary-reviewed, PR pirate-force-server#931 -> rounds/R372_fyrtvt_wire_three_core_requests_ui_a_b_adversary_findings_fixed.md
- R373(8vij1d) fixed the queue-status tool silently dropping still-open tickets whose name contains OPEN/PASS/DONE (GT-224 was one of them) and raised the size ceilings so bridgesize stops being permanent known-red -> rounds/R373_8vij1d_pr0_queue_ceilings_tickets_dir_and_the_slug_that_closed_tickets_silently.md
- R374(8vij1d2) paid pf-adversary's 7 findings on R373's own patch (GT-205/GT-159 recovered, GT-188 stopped borrowing another ticket's verdict, LANE-K's bus-scheduling file no longer risks tool overwrite) -> rounds/R374_8vij1d2_pay_the_adversary_on_the_r373_queue_status_patch.md
- R375(t0funk) two round files: an addendum paying an adversary finding + the new filename-length gate + 6 SYNC-ALARM replies (SCOREBOARD NONE), and D11 -- two town vendor NPCs now queue talk/shop-open commands correctly and remember state across clicks -> rounds/R375_t0funk_addendum_pay_adversary_0137.md, rounds/R375_t0funk_d11_queuegrowth_cap_and_0137_latch_pair.md
- R376(l5tqxc) wired DEATH_SEED_WIRING (a killed monster stays dead across a relog) into runtime.py, then pf-adversary's own F1 finding stopped it: the seed's placement also fires on the attack path, so a monster can go silent mid-fight for a SECOND player with no death frame -- a game-design call, not this lane's -- PR pirate-force-server#948 stays draft/tokenless pending that ruling; 11 more findings recorded for the next round -> rounds/R376_l5tqxc_death_seed_call_site_and_the_ceilings.md
- R377(awnjat) two independent pieces: (1) LANE-Q CORE-REQUEST `1950` granted -- migrations/016_character_quest_state.sql + store.py quest-flag/quest-counter accessors, 32 new tests, with an honest FUNCTIONAL_COVERAGE.json/guard-test update rather than a silent pass; `1951` NOT granted (test_every_symbol_exemption_is_still_earned refuses an exemption for code that does not exist yet -- pirate-force-server#947 was closed unmerged), exact pre-approved patch handed back to LANE-Q for its next PR; (2) paid R376's F7/F8 debt on `#948` (a real two-account relogin test rewritten to actually relog; a new mutation-killing test for the seed-vs-respawn-sweep ordering mutant, both mutants verified to fail it) but could not push to that PR's branch (not this session's assigned branch) -- full patch saved to rounds/E_20260906_2123_awnjat_death_seed_f7_f8_fix.patch, verified to `git apply --check` clean against origin/claude/upbeat-hamilton-l5tqxc -> rounds/R377_awnjat_quest_state_door_and_death_seed_f7_f8_handoff.md
- R378(tdc8si) the >=100-character filename cap (PANYA-ORDER 1910) stops being an honour system: `--bridge-only` mode makes pf_gate_preflight.py runnable with only one repo checked out (it used to `return 2` and run nothing without a pirate-force-server clone beside it, so a workflow wired to it would have printed FATAL and gone green), and a new `.github/workflows/bridge-preflight.yml` runs it on every pf_bridge pull request against the PR's own base SHA; COO's second condition (the reaper must REFUSE a red one) is deliberately NOT in this PR and is next round's first job, with both hazards measured and written down -> rounds/R378_tdc8si_bridge_preflight_workflow_and_bridge_only_mode.md
