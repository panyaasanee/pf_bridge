# R138 (bcc9z5) — เปิดเลนโค้ด LEARN-SKILL-RESULT-001: encoder `CLearnSkillResultVital 0x673C`

- **เซสชัน:** branch `claude/exciting-goldberg-bcc9z5` (pf_bridge) · `claude/amazing-goodall-bcc9z5` (server)
- **เวลา:** 2026-08-24 ~03:1x–04:4x +07:00 (2026-08-23 20:1x–21:4x UTC) — timestamp ในไฟล์นี้เป็น +07:00 เว้นแต่กำกับ
- **ล็อกรอบ:** draft PR #39 (pf_bridge) เปิดเป็น draft ตั้งแต่ก่อนเริ่มงานตามกติกา v5 · ไม่มี PR ค้างตอนเช็ค (ทั้งสอง repo ว่าง)

## Probe ต้นรอบ
- GitHub API/tool: ✅ อ่านรายการ PR ได้ทั้งสอง repo (ใช้เป็นทางหลัก)
- ทาง D (`ci-status`): ✅ มีชีวิต — `git ls-tree origin/ci-status ci/` คืน 6 ไฟล์ · d_exit=0
- โครงพี่น้อง: ✅ `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง

## กล่องจดหมาย
- ไม่มีจดหมายผู้เทสใบใหม่ (ทุกใบมีคู่ `.CONSUMED.txt` แล้ว — ที่ไม่มีคู่เป็น `FROM_CHIEF_*`/README ของฝั่งเราเอง)
- จดหมายล่าสุดที่บริโภคไปแล้วคือชุด 0033–0159 (R135–R137)

## งานรอบนี้ — ทำไมเลือกเลนนี้
- เลน attended: ⏸ พักตามคำสั่ง Panya 16:56 — ไม่แตะ
- `RE-056` / `RE-057` / `GT-055`: งานหน้าสะพานล้วน (ต้องใช้อิมเมจ/capture) — รอสะพาน
- `PF_VITAL_NAMES` 3 id: ติดรอคำตอบ Panya เรื่อง provenance ชั้น 4 (คำถามค้างจาก R134/R135)
- ⇒ milestone สำรองที่ปลดล็อกแล้วและยังไม่มีใครหยิบ: **เลน headless สกิลฝั่ง learn-result**
  (R135 บันทึกว่า GT-050 ปิด codec `CLearnSkillResultVital` แล้ว "มี wire shape พิสูจน์แล้วให้เขียนโค้ดได้")
  เข้าเกณฑ์ pre-approved ข้อ 3 (ฟังก์ชัน gameplay ใหม่ใต้ pattern มาตรฐาน) + ข้อ 2 (headless = เส้นทางหลัก)

## สิ่งที่ทำ

### 1) LEARN-SKILL-RESULT-001 / HYP-PF-033 — encoder + opt-in scenario (repo โค้ด)
- ไฟล์ใหม่ 3: `src/pirateforce_foundation/learn_skill_result_hypothesis.py` (encoder+strict decoder ของ body `0x673C`
  ตาม GT-050: `count u16/0x12` + records 12 ไบต์ `(u32 0x14 · u16 0x12 · u32 0x14)` + trailing `u8 0x0B @+0x2C` ·
  envelope ใช้ helper v141 เดิม ไม่เขียนซ้ำ) · `scenarios/learn_skill_result_hypothesis_learn_sweep.json`
  (sweep 5 สเต็ป COUNT0/1/1/3/3 × TRAIL0/1 · pin sha256 ต่อสเต็ปครบ payload/pc/frame) ·
  `tests/test_learn_skill_result_hypothesis.py` (59 เทส + 3 subtests — golden bytes เขียนมือ ไม่ self-certify:
  mutation test ของ adversary เปลี่ยน tag 0x12→0x13 แล้วล้ม 24/59)
- wiring: `runtime.py` + `app.py` (flag `--learn-skill-result-hypothesis-scenario` · opt-in · `--db` บังคับ ·
  mutually exclusive · `production_allowed=false` · fail closed) · ledger HYP-PF-033 (entry 41) + coverage `skill_use`
- nonclaims หลัก: semantics ของ record fields (u32/u16/u32) ยัง opaque · inbound `CLearnSkillVital 0x36AA` ไม่ทำ ·
  version byte 0 = ดีไซน์เรา ยัง unpinned · ไม่มี client เคยเห็นเฟรมนี้ · ไม่ใช่พฤติกรรมเซิร์ฟเวอร์ต้นฉบับ (กู้ไม่ได้ตลอดกาล)
- เทสก่อนแก้ defect: ชุดเต็ม **1976 passed / 324 skipped / 0 failed** เขียว(cloud sanity) · skip census PASS · verifiers PASS

### 2) adversary ตรวจก่อน commit — 5 defect (แก้ครบก่อน commit · ดูรายละเอียดท้ายรอบ)
- D1 (HIGH): guard ฝาแฝดใน `tools/pf_stats_progression_static.py` ไม่ถูก amend พร้อมเทส 24 — บน cloud มองไม่เห็น
  เพราะ tool ตายก่อนถึงจุดสแกน (ไม่มีอิมเมจ) แต่จะ **exit 1 จริงบนสะพาน** ⇒ amend twin + ผูก exception list สองฝั่งเข้าด้วยกัน
- D2: ประโยค stale ใน coverage `stats_and_progression` ("five verbs still zero") — false ที่ HEAD ⇒ แก้ระบุข้อยกเว้น
- D3: allowlist เทส 24 กว้างเกิน (membership ไม่นับ occurrence) — inbound 0x36AA ในไฟล์เดียวกันจะรอดตาข่าย ⇒ pin occurrence count
- D4: prose ใน module/runtime บรรยาย step plan ผิด (COUNT0 มีแค่ TRAIL0) ⇒ แก้สองจุด
- D5: คอมเมนต์นับเลน "eight above" ผิด (จริง 11) ⇒ เอาตัวเลขออก
- ข้อที่ adversary ยกเป็นคำถามดีไซน์ค้าง: **ใครเป็นเจ้าของ guard ฝาแฝด tools/tests** — cloud แก้ครึ่งที่ตัวเองรันได้
  แล้วครึ่งสะพานแดงเงียบ ๆ ทุกครั้งที่มี "encoder ตัวแรกของ X" ⇒ จดลงจดหมายรอบนี้ให้ Panya เห็น

## คิวเทสเกม
- ✅ เพิ่มใบ **GT-058** (client-observable ครึ่งหลังของเลนนี้) ลง `GAME_TEST_QUEUE.md` ผ่าน pf-queue-author —
  ติดสองบล็อกชัดเจนในหัวใบ: 🔴 รอ gate เขียว + merge ก่อน · ⏸ รอ Panya ปลดพัก attended (คำสั่ง 16:56) ·
  pass criteria สองชั้นแยกกัน (wire/DB · client-observable) · ห้ามฝัง sha เดา — อ่าน pin จาก scenario ตอน merge

## ผลแก้ defect + สถานะ commit/PR (ปิดรอบ)
- แก้ครบทั้ง 5: D1 amend tool twin + ผูก exception list `(file, verb, occurrence_count)` ผ่าน ast re-read
  (test อ่านค่าคงที่จาก tool แล้ว assert เท่ากันสามทาง: tool == test == live scan — แก้ฝั่งเดียวเมื่อไหร่เทสแดงทุกเครื่อง) ·
  D2 แก้ประโยค stale ใน coverage (notes นอก GRADE_SUBSET — digest ไม่ขยับ ยืนยันแล้ว) · D3 pin occurrence count +
  บังคับ mention อยู่ใน docstring เท่านั้น (โค้ด executable ห้ามเอ่ยชื่อ verb) · D4/D5 แก้ prose สองไฟล์
- หลังแก้: ชุดเต็ม **1976/324/0** เขียว(cloud sanity) · census PASS · verifiers PASS (entries=41 · domains=8) ·
  ASCII scan สะอาด (non-ASCII ที่เหลือ = ไทยเดิมใน verify_hypothesis_ledger ไบต์ตรง HEAD เป๊ะ)
- commit server: `e34d91f` (11 ไฟล์ตามประกาศ · staged=11 · deletion=0) · **PR #14** เปิดพร้อม marker — gate ตัดสิน
- pf_bridge: ใบ GT-058 + ไฟล์รอบนี้ + ดัชนี continuation + จดหมาย R138 — commit/push แล้ว PR (draft #39) ปลดท้ายรอบ
- 🔴 note ถึงสะพาน: guard section 20 ของ tool twin ตรวจด้วย standalone simulation ที่นี่ (tool เต็มต้องมีอิมเมจ) —
  รอบสะพานหน้าให้รัน `tools/pf_stats_progression_static.py` เต็มหนึ่งครั้งยืนยัน exit 0 ที่ HEAD ใหม่

## คำถามค้าง (ยกยอดเดิม + ใหม่หนึ่งข้อ)
- 🆕 **ดีไซน์ guard ฝาแฝด tools/tests (จาก adversary R138):** milestone "encoder ตัวแรกของ X" ทุกอันจะเจอปัญหาเดิม —
  cloud แก้ครึ่ง tests/ ที่ตัวเองรันได้ แต่ครึ่ง tools/ รันเต็มได้เฉพาะสะพาน ⇒ R138 ผูกคู่ด้วย ast-binding เฉพาะคู่นี้แล้ว
  แต่ยังไม่มีกติกากลางว่า "ฝั่งไหน canonical + cloud พิสูจน์ยังไงว่าไม่พัง guard ที่ตัวเองรันไม่ได้" — เสนอ Panya เคาะ
- provenance ชั้น 4 ให้ `PF_VITAL_NAMES.json` ปิด 0x16A0/0x1661/0x16F7 (จาก R134)
- นัดจังหวะ rename `external\` → `clientbin\` (จาก R135)
