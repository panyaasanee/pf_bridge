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

(แถวเปิด 011 012 014 015 017 021 026 — สรุปย่อคำต่อคำย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ถ้อยคำเต็มอยู่ใน `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` เหมือนเดิม · เลขจองล่าสุด: 032)

- 032 CORE-REQUEST (สาย CS รอบ `t04sgo` · `notes_to_chief/20260907_0618_LANE-CS-CORE-REQUEST-attacker-level-from-the-real-character.md`) — `runtime.py:5093` ส่ง `MOB_COMBAT_DEFAULT_ATTACKER` (`Combatant` คงที่ระดับโมดูล `runtime.py:311`) เป็นผู้โจมตี ⇒ **ผู้เล่นทุกอาชีพทุกเลเวลตีแรงเท่ากันเป๊ะ** ขอประกอบ `Combatant` จากตัวละครของเซสชัน โดยขยับ **`level` ตัวเดียว** (`ability_str`/`ability_con` คงพิน เพราะแหล่ง STR ยังไม่รู้) พร้อมเงื่อนไข `COO-DECISION 0445` ข้อ 4: ขยับพิน 891 ในคอมมิตเดียวกัน · ห้ามแตะดาเมจฝั่งมอน→ผู้เล่น · `level` ที่อ่านไม่ได้ต้องตกกลับพินพร้อม event ที่มีชื่อ ห้ามเป็น 0 เงียบ ๆ · **ยังไม่ต่อสาย** — `COO-DECISION 0741 (e0730)` สั่งตรง ๆ ว่า CORE-REQUEST อยู่หลังลำดับ chief ข้อ (1)/(2) ⇒ เปิดค้างโดยเจตนา ไม่ใช่ตกหล่น · คิว CORE-REQUEST ที่ chief ค้างทั้งหมดตอนนี้ = **6 ใบ** (B ×2 · GM ×3 · CS ×1 — DB ถอนใบของตัวเอง `20260907_0752`)

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
- ดัชนี R370-R383 ฉบับเต็ม (คำต่อคำ ไม่มีการลบ) -> [`archive/CHIEF_CONTINUATION_ARCHIVE_20260907_round_index_R370_R383.md`](archive/CHIEF_CONTINUATION_ARCHIVE_20260907_round_index_R370_R383.md) · ย่อเหลือหนึ่งประโยคต่อรอบตาม CHIEF.md §4 โดย chief รอบ `1w9f0q`/R384 (เพดานเหลือ 32 B)
- R370(jz5vtt) reaper closes ghost claims and author-declared `SUPERSEDED-BY:`/`DUPLICATE-OF:` (PANYA-ORDER `1315`) -> rounds/R370_jz5vtt_reaper_closes_ghost_claims_and_author_declared_supersedes.md
- R371(jz5vtt2) paid four adversary findings on that live reaper and RETRACTED R370's own advice to create `PF_BRIDGE_NOTES_TOKEN` -> rounds/R371_jz5vtt2_pay_the_adversary_findings_on_the_live_reaper.md
- R372(fyrtvt) wired three CORE-REQUESTs (UI Exit Game, A ground-drop persistence, B mob respawn) into runtime.py -> rounds/R372_fyrtvt_wire_three_core_requests_ui_a_b_adversary_findings_fixed.md
- R373(8vij1d) queue-status tool stopped silently dropping open tickets whose name contains OPEN/PASS/DONE -> rounds/R373_8vij1d_pr0_queue_ceilings_tickets_dir_and_the_slug_that_closed_tickets_silently.md
- R374(8vij1d2) paid the 7 adversary findings on R373's queue-status patch -> rounds/R374_8vij1d2_pay_the_adversary_on_the_r373_queue_status_patch.md
- R375(t0funk) filename-length gate + two town vendor NPCs remember state across clicks -> rounds/R375_t0funk_addendum_pay_adversary_0137.md, rounds/R375_t0funk_d11_queuegrowth_cap_and_0137_latch_pair.md
- R376(l5tqxc) wired DEATH_SEED_WIRING, then held `#948` draft on the adversary's F1: the seed also fires on the attack path -> rounds/R376_l5tqxc_death_seed_call_site_and_the_ceilings.md
- R377(awnjat) LANE-Q quest-state door (migration 016 + store accessors) granted, `1951` refused, R376 F7/F8 handed over as a verified patch -> rounds/R377_awnjat_quest_state_door_and_death_seed_f7_f8_handoff.md
- R378(tdc8si) `--bridge-only` preflight + `bridge-preflight.yml` so the 100-character filename cap stops being an honour system -> rounds/R378_tdc8si_bridge_preflight_workflow_and_bridge_only_mode.md
- R378 addendum(tdc8si) 10 adversary findings on R378's own patch, returned after unlock -> rounds/R378_tdc8si_addendum_adversary_after_unlock.md
- R379(lk97bl) wired LANE-A's three ChooseNPC decline guards, scoped to scene 1 so they cannot leak into other scenes -> rounds/R379_lk97bl_wire_core_request_2318_census_ack_marker1_guards.md
- R380(52u95a) `PF_NAME_COLOUR_SWEEP` had no call site at all; wired it and recovered reaped `#966`'s work unchanged -> rounds/R380_52u95a_wire_name_colour_sweep_and_recover_966.md
- R381(ky8m6j) moved that dummy row INSIDE the arrival census (RE-092: replace-by-omission at collection scope) + preflight `[claudecfg]` -> rounds/R381_ky8m6j_sweep_inside_the_census_and_the_claude_config_gate.md
- R382(qg7i59) `.LANEK-FOLDED.txt` stubs exempted from the inherited-name cap + gate prints FAILED names last where a cloud tail reaches them -> rounds/R382_qg7i59_lanek_fold_stub_exemption_and_gate_failed_names.md
- R383(3py8sa) report-only `bridge-guarded-tests.yml`: 155 tests guarded by a bridge precondition had skipped on every commit forever -> rounds/R383_3py8sa_bridge_guarded_tests_on_ci_report_only.md
- R384(1w9f0q) `require(cls)` now raises TypeError on EVERY machine instead of only a bridgeless one, plus an AST sweep forbidding it in `setUpClass`/`setUpModule` (#966/#990/bg0008 shape) -> rounds/R384_1w9f0q_require_needs_a_test_instance_on_every_machine.md
- R385(lafdux) จ่ายสองข้อ HIGH ของ adversary ที่หักล้าง R384 เอง (provenance "สาม PR" จริงมีใบเดียว `#990` · guard เลิกแนะนำ decorator ที่ precondition สองตัวไม่มี) + กฎ marker ขยายเป็นทุก PR สองรีโปโดย `AGENTS.md` ไม่โตขึ้น -> rounds/R385_lafdux_pay_the_two_high_findings_and_the_marker_rule.md
