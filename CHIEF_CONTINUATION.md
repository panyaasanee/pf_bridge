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

## ทีมและเขตเขียนของสาย DB / CS / UI / Q ⇒ ย้ายคำต่อคำไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R368_lane_charters.md` (chief R368 · งานแม่บ้าน §17 ข้อ 9 เพื่อให้ไฟล์กลับใต้เพดาน 30,720 B — ไม่มีอะไรถูกลบหรือย่อ)
- เขตเขียนที่**มีผลจริง**อ่านจาก `prompts/<สาย>.md` และ `CHIEF.md` §6 เสมอ ไม่ใช่จากไฟล์นี้
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
- R361(siynev) 2026-09-06T00:22-01:1x+07:00 [เติมย้อนหลังโดยรอบ R362 -- รอบ R361 ไม่ได้เขียนบรรทัดดัชนีของตัวเอง] `#859` lupa (`python -m pip`) + `#858` หมุด migration แบบ dynamic วินิจฉัยจบและ re-land -> merge เป็น `#870` บน main 01:11 · ไม่ได้ขยับ PROMOTION_BACKLOG/whitelist/DEATH_SEED_WIRING (เหตุผลรายข้ออยู่ในไฟล์รอบ) -> rounds/R361_siynev_lupa_shim_equals_split_dynamic_migration_pin.md
- R362(6z131u) 2026-09-06T01:51-02:1x+07:00 GT-233 v3 พลิกเป็น "บูตได้ทันที" หลังวัดเอง (#857/#865 ancestor จริง · D1 lazy · dock153 key=1 dock154 key=126 · len(pc)=62) + เติมบล็อก ATTENDED ที่ใบไม่เคยมีตั้งแต่ R358 · RE-270 ตั้งเลขให้ LANE-A (ข้าม 268/269 ที่ประกาศเป็นของ A/GM ไปแล้ว) · GT-269 ลงคิว READY · archive 20 ใบปิด (GT 2.33->2.22 MB · RE 467->352 KB) เปิดหัวคิวให้ใบใหม่ · ADVERSARY_PENDING -> rounds/R362_6z131u_gt233_v3_bootable_re270_numbered_gt269_filed_queue_archival_pass.md
- R363(ss9u08) 2026-09-06T03:49-04:2x+07:00 PANYA-ORDER 0156 ทาง (ก): CORE-REQUEST 2242 รับ (class_id=selected.class_id ต่อ runtime.py:5159) ปลดเส้นทาง production pose ที่ตายมาตลอด, pf-adversary จับ blast radius จริง 21 แดง/7 ไฟล์เทสที่ไม่ได้แตะ แก้ครบ (ชุดเต็ม 11603 passed/0 failed) -> pirate-force-server#883 (draft, adversary รอบสองรอผล) · COO-DECISION 0042: scoreboard date column + MALFORMED สำหรับแถว manual + เกต pf_gate_preflight.py ปฏิเสธ PR ที่แตะแถว manual + AGENTS.md หนึ่งบรรทัด (ทำให้ AGENTS.md 44161->44628 ไบต์ RED เฉพาะกิ่งนี้ บันทึกไว้ตรง ๆ ไม่ใช่ CI บังคับจริง) -> rounds/R363_ss9u08_panya_order_0156_class_id_wired_scoreboard_manual_row_gate.md
- R364(xcbnbn) 2026-09-06T04:52-05:2x+07:00 pf_bridge only, no server PR (เหตุผลอยู่ในไฟล์รอบข้อ 2: งาน server ข้อเดียวตามลำดับ COO คือยกเว้น guard ให้ Q ซึ่งวัดแล้วว่าลง main ก่อนโค้ด = แดง จึงไม่ใช่ commit ของ chief): 🔴 **เกต reaper ที่ปิดรอบจริงทิ้ง** แก้แล้วทั้งสอง job — การ์ด #1079 ใช้ `changed_files <= 1` แทน 'ไม่มีงานมา' แต่ COMMON สั่งลบ `_claim.md` บนกิ่ง ⇒ รอบที่โค้ดไปฝั่ง server ทั้งหมดตกที่ 1 ไฟล์พอดี (ยืนยันเอง: #1414 = 1 ไฟล์ +273 บรรทัด mergeable_state=clean ปิดไม่ merge ไฟล์เดียวนั้นคือไฟล์รอบ GM ที่ถือ PANYA-ORDER /lv 14:00) ⇒ เปลี่ยนเป็น `PF_ROUND_FILE_FILTER` สองสัญญาณ OR กัน (ชื่อไม่ใช่ placeholder เทียบไม่สนตัวพิมพ์ + ขนาด ≥20 บรรทัด) ตัด status=removed · **pf-adversary คืนผลทันในรอบและหักล้าง chief ได้จริง D1-D4 จ่ายครบ** (D1 chief สร้าง unbounded skip ที่ไฟล์นี้เคยแก้ไปแล้ว R335 -> bound ด้วย PF_STALE_CLOSE_HOURS · D2 `|| true` ครอบทั้งไปป์ ⇒ jq ตายบน rc=0 อ่านเป็น 'ไม่มีงาน' ⇒ ปิด PR -> แยก parse ออกจาก verdict · **D3 การ์ดอ่อนลงจริง คำอ้าง 'ไม่อ่อนลง' ของ chief เป็นเท็จ**: 26 placeholder บน main สะกด `_CLAIM.md`/`_claim_<id>.md` ผ่านการ์ดหมด -> เทียบไม่สนตัวพิมพ์ + สัญญาณขนาดกันไฟล์รอบจริงที่ slug มีคำว่า claim · D4 deletion นับเป็นงาน -> select(status != removed)) ตรวจซ้ำหลังแก้ 8/8 เคสผ่าน · LANE-Q CORE-REQUEST 0209 **อนุมัติยกเว้นครบสามชื่อ แต่วัดสองทิศทางแล้วว่าลง main ก่อนโค้ด = แดง** (test_every_symbol_exemption_is_still_earned) / บนกิ่ง #874 = เขียว 31 passed ⇒ อนุญาต LANE-Q แตะ ALLOWED_SYMBOLS ครั้งเดียวใน #874 พร้อมบล็อกคำต่อคำ · RE-273 trigger-id -> .lua ตั้งเลขวางคิวให้ LANE-Q (เติมผล grep ที่ห้าที่ใบเดิมไม่มี รันเอง 0 hit) · **QUEUE_TRIAGE ครบกำหนด 05:02 จ่ายแล้ว กวาดครบ 302 ใบ — ผลหลัก: READY 19/22 ใบไม่มีบล็อก ATTENDED: = ตกรถบัส capture** ตีกลับ 8 สายทางจดหมาย · ไม่ได้ทำ: viewer_identity+GT สี (โควตา adversary หมดกับเกต reaper) · §7 grep ที่ห้า (AGENTS.md 44,628 ไบต์เกินเพดานอยู่แล้ว แต่กฎถูกใช้จริงใน RE-273) · 0323/0332/0435/GT-233 D1 (ชนงบ 75 นาที) -> rounds/R364_xcbnbn_reaper_unripe_guard_fixed_q_guard_grant_re273_queue_triage.md
- R365(d5igq0) 2026-09-05T23:22-2026-09-06T00:09+07:00 mailbox triage (AGENTS.md §7 grep ที่ห้า `reference_codex_attr/` · GT-233 D1 สี่กรณี+ช่วงเลเวล · GT-266 ปิด PASS ขอบเขต live-warp/no-relog แยก GT-274 · LANE-Q ALLOWED_SYMBOLS ยกเว้นครั้งเดียวอนุมัติแบบมีเงื่อนไข) · `docs/PROMOTION_BACKLOG.md` ใหม่ (18 แถว) + เสียบ `viewer_identity` เข้า scene-arrival override (CORE-REQUEST-GM-061) -> `pirate-force-server#894` **แต่ pf-adversary รอบเดียวกันพบว่าเสียบไม่ครบ** (recompose_frames/hostile_census_frames ทุกการตี/ตายยังไม่มี) ⇒ #894 ค้าง draft, GT-275 ถูกตั้งเลขแต่พลิกกลับ BLOCKED-ON-WIRING · claim `pf_bridge#1440` ไม่ปลด (ไม่มี marker) รอรอบหน้าปิดช่องว่างต่อ -> rounds/E_20260906_0621_d5igq0 (ไม่มีไฟล์รอบจริง — งานอยู่ที่คอมมิตบนกิ่ง `claude/adoring-fermat-d5igq0` และ PR #1440/#894 เอง เก็บย้อนหลังโดยรอบ `ald09i`/R367)
- R366(19wyif) 2026-09-06T07:51+07:00 ถอยให้ `#1440` (อายุ 91 นาที ตอนนั้นยังไม่ถึงเกณฑ์ 120 นาทีของข้อ 2 · เช็คข้อ 3 ก่อนแล้วไม่เข้าเพราะ `#894` ยัง draft) — ไม่ขยับ NOW/M ข้อไหน ถอยตามกฎล็อกรอบล้วน ๆ -> rounds/R366_19wyif_yield.md
- R367(ald09i) 2026-09-06T09:22+07:00 takeover of `#1440`/R365 (อายุเกิน 3 ชม.แล้วตอนตรวจ): ปิดช่องว่างที่ R365 เปิดค้าง — เสียบ `viewer_identity` ผ่าน `mob_death.hostile_census_frames`/`diag_multi_object_wiring.hostile_census_frames`/`mob_scene_recompose.recompose_frames` ครบสามจุดที่เหลือ + ต่อเข้า `runtime.py` ทั้งสามจุดเรียกจริง (บาร์ตอนตี, dying/dead ตอนตาย) · ต่อสาย LANE-B D11 (`commit_death_and_prepare_hook`+เขียนกลับก่อนยิง hook) · **pf-adversary พบข้อบกพร่องจริง**: เทสสองไฟล์ที่พลาดตอนแรกทำให้ 5 เคสแดงบน commit ที่ push ไปแล้วก่อนชุดเต็มรันเสร็จจริง — แก้ในรอบเดียวกัน (`ff71c44`) ยืนยันชุดเต็มเขียว 12031 passed/365 skipped/0 failed บนต้นไม้ merge origin/main สองรอบ (`#902`,`#903`) · TWO_SESSIONS_SAME_SCENE ตอบแล้วด้วยการอ่านโค้ด `dispatch()` จริง (per-connection instance, ไม่มีทางถึง session อื่น) · GT-275 ร่างเนื้อใบเต็มแล้วแต่ถอนจาก `GAME_TEST_QUEUE.md` รอบนี้เพราะเกต bridgesize แดงจริง (ไม่เข้าข้อยกเว้นแคบของ R364) — เก็บไว้ในไฟล์รอบ รอ archive pass รอบหน้า · archive ดัชนีรอบเก่า R350-R357 ไปไฟล์แยกเพื่อดันไฟล์นี้กลับลงมาใกล้เพดาน (57236->~4x KB) · CORE-REQUEST ใหม่จาก LANE-A (`0914`, world-ground เข้า ground-companion recompose) มาถึงกลางรอบ ยังไม่ทำ ยกเป็นงานที่สองของรอบหน้า -> rounds/R367_ald09i_viewer_identity_combat_recompose_plus_d11_hook_ordering.md

- R368(u2o8d7) 2026-09-06T10:51-12:5x+07:00 takeover of `#1440` (ครั้งที่สอง อายุ 4:29) · โทเคน CANCELLED/FAIL ลง pf_queue_status.py (เปิด 107->102 ห้าใบ ไม่มีใบกลับเป็นเปิด) · ตั้งเลข+วางเนื้อใบจริง GT-274/275/276/277/278 + RE-275 + บล็อก ATTENDED ของ GT-255 · รอบ archive **ถอนฉบับ regex แล้วทำใหม่แบบ allowlist มือ** หลัง pf-adversary พบว่า regex ตัดเนื้อใบเปิด GT-178/GT-133 ขาดและย้ายใบที่ยังไม่ปิด 6 ใบ (D1/D2) · GT queue 2,235,655->2,155,007 · RE queue 362,594->356,520 · เพดานยังไม่ถึงและวัดแล้วว่าถึงไม่ได้ (ใบ ASK-COO 1155) -> rounds/R368_u2o8d7_queue_archive_cancelled_fail_tokens_five_gt_numbers_landed.md