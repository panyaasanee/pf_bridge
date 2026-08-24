# R149 (zip9tr) — บริโภคผล 4 ใบ + เปิดเลนโค้ด `CSkillAttr` sender (ผลบวกจาก RE-061)

- เวลาเริ่ม: 2026-08-24 ~22:0x (+07:00) · เซสชัน: zip9tr
- ล็อก: PR #50 (draft) `pf_bridge` เปิดเป็นอย่างแรกก่อนงานทั้งหมด (ลำดับ v5 ข้อ 3)
- probe: GitHub API ใช้ได้ (list/create PR สำเร็จ) · ทาง D มีชีวิต (`git ls-tree origin/ci-status ci/` exit 0)
- โครงพี่น้อง: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง ✅
- PR #20 (whole-world fix ของ pf-static-re จาก R148) **merge เข้า `main` แล้ว** (`50aa32d`) — งานค้าง R148 ข้อนี้ปิด

## จดหมายที่บริโภค (4 ใบ · สำเนาเข้า `consumed/` + stub ครบ)

1. `20260824_1413_RE-059-RESULT-EXTRACTED-5-OF-5` — ✅ ถอดครบ 5/5 เฟรม `ItemOperateVitalRes 0x4C13` ver 2
   ทุกเฟรม `bag_present_flag=1` (ตรงคำทำนาย) · `affected_identity_count=0` · nested `ItemBagAttr` โครงลงตัวทุกเฟรม
   ⇒ **เลนลูท (monster_spawn_and_loot) ได้วัตถุดิบสำคัญ: hex เต็มของเฟรมจริงที่ client เคยรับ** — ใช้เป็น golden
   สำหรับ acquire-path (D2 ของ R147: ต้องพิสูจน์ว่า body แบบไหนทำให้ id-131 บรรทัดเขียวยิง)
2. `20260824_1422_RE-060-RESULT-PINNED-5-CODES` — ✅ pin `22/24/25/26/35` → ตาราง CONSTDATA ห้าตาราง
   กลไก `full_id/100000 → table · %100000 → n_ID` ยืนยันจาก image · crosswalk ชื่อ = join `n_ID` ไม่ใช่ row order
3. `20260824_1437_RE-061-RESULT-SKILLATTR-GATE-PINNED` — ✅ **ผลบวก** (เงื่อนไข R146):
   `CSkillModule` serializer ว่างจริง (ไม่มี wire) · `CSkillAttr` ขี่ `UpdateAttrVital 0x309A` เป็น attr block
   `class_id 0x1661` · inbound apply มีจริง · **gate หน้าต่าง Skill พิสูจน์แล้ว**: controller init `0x761ED0`
   คืน false ถ้า `[actor+0x3E8]` (CSkillAttr) ไม่พร้อม ⇒ ตามแผน R146: **chief เปิดเลนโค้ด sender ในรอบนี้**
4. `20260824_1443_GT-047-RESULT-GUARD-PASS` — ✅ ปิด GT-047 = `DONE / GUARD-GAP FIXED / METHOD-RUN COMPLETE`
   การ์ด 8/8 ผ่าน · mutation แดงจริง · **claim F2 คง OPEN** (`A2_STATIC_OPEN 50,820/50,820`)

## ✅ cross-check ฟรีจาก RE-059 (chief ตรวจเองบน cloud รอบนี้)

เทียบ hex เฟรม #1 ของ RE-059 (`ItemBagAttr` 43 ไบต์) กับ `inventory.py::make_item_move_delta_response`:
`0B FF · 32 id=0 · 0F count=1 · (32 id=1 · 14 template=2600001 · 0F qty=2 · 0F slot=2 · 08 00 · 08 FF · 0B 0) · 0F removal=0`
⇒ **ตรงโครงของ encoder เราแบบ field-ต่อ-field** รวมค่าคงที่ `BACKPACK_BASE_MASK=0xFF` และ `BACKPACK_BASE_IDENTITY=0`
(inventory.py:15-16) · เฟรม #2 = ทรง merge (removal 1 ตัว) · เฟรม #3/#4 = ทรง 2 updates
⇒ เฟรมจริงที่ client เคยรับ = โครงเดียวกับ codec ที่เรามีอยู่แล้ว — D1 ของ R147 แน่นขึ้นอีกชั้น
(หมายเหตุ: นี่คือการเทียบโครง ไม่ใช่ byte-equality ทั้งเฟรม — template `2600001` = Adventure Key ตาม RE-060)

## งานที่ทำ

- `CLIENT_RE_QUEUE.md`: RE-059/060/061 → DONE พร้อมสรุปผล + บล็อกสถานะ R149 (ไม่มีใบ RE เปิดค้างแล้ว)
- `GAME_TEST_QUEUE.md`: GT-047 → DONE (F2 คง OPEN) · [รอเติม: ใบเทสใหม่เลน skill-attr]
- `pirate-force-server`: ✅ ลูกมือ implement เลนใหม่เสร็จ — **HYP-PF-035 · checkpoint SKILL-ATTR-001**
  - โมดูลใหม่ `src/pirateforce_foundation/skill_attr_hypothesis.py`: encoder/decoder `CSkillAttr` (fail-closed ·
    decoder-inverse-checked) · payload wrap ตรวจ drift กับ frozen module · compose ผ่าน `legacy.make_runtime_vitals`
    พร้อม structural re-checks · พิน sha256+size ของ body/payload/pc/frame · VA citations จาก RE-061 ครบ
  - scenario opt-in `skill_attr_hypothesis_attr_sweep` (flag `--skill-attr-hypothesis-scenario` · `production_allowed=false`
    · ต้องระบุ `--db` ที่มีอยู่จริง · mutually exclusive กับโหมดอื่น) · trigger แบบ chat-input เลียน learn-skill lane
    · สองสเต็ป: `HYP_PF_035_SKILL_ATTR_COUNT0_EMPTY` (record 0 ตัว) · `HYP_PF_035_SKILL_ATTR_COUNT1_KEY1`
    (1 record key=1 opaque=0/0 — ค่า probe ตามอำเภอใจ ประกาศชัดว่าไม่รู้ความหมาย)
  - เทสใหม่ `tests/test_skill_attr_hypothesis.py` 68 เทส (golden hex สองเฟรม · round-trip · refusal ครบตระกูล ·
    off-by-default containment) · ledger → 43 entries (`verify_hypothesis_ledger.py` PASS) · GRADE_SUBSET_SHA256
    ขยับพร้อมพินในคอมมิตเดียว (บทเรียน R147) · census twins ได้ exception triple
  - **สวีตเต็ม: 2103 passed / 324 skipped / 0 failed — เขียว(cloud sanity)** · ASCII ล้วนทุกไฟล์ใหม่
  - หมายเหตุ: ลูกมือรอบแรกตายกลางทางด้วย API 529 (overload ชั่วคราว) — resume ต่อสำเร็จ ไม่เสียงาน
- **pf-adversary (บังคับก่อน commit — ผ่านแล้ว):** parse golden frame สองตัวด้วย parser อิสระ (ไม่ import โมดูล)
  **ตรงสเปค RE-061 ทุกฟิลด์** รวม trailing `0B00` (= RuntimeRes-v4 derived-class change mask ของ v141:706-710
  ไม่ใช่ไบต์หลง) · identity qword = สูตร lifecycle `0x10010001` ถูกต้อง · gating เจาะไม่เข้า (23-mode mutual
  exclusion · exact-allowlist scenario · ไม่มี normal-boot path) · GRADE pin ขยับพร้อม change (พ้น scar R147)
  - **D1 (แก้แล้ว):** refusal ตำแหน่ง opaque_u16 ติดป้ายผิดเป็น `wrong_record_key_tag` → แก้เป็น
    `wrong_record_opaque_u16_tag` + ลงทะเบียน + แก้เทส
  - **D2 (แก้แล้ว):** โน้ต invariant เก่าใน `remote_player_hypothesis.py` ("src/ ไม่มี token คลาสนี้") ค้าง
    → เขียน amendment ลงวันที่ (เลี่ยงการสะกด token/ชื่อโมดูล — census + containment test บังคับ)
  - **D3 (ส่งต่อสะพาน — ไม่แก้บน cloud):** `external/PF_SERIALIZER_FIELDS.tsv` แถว `CSkillAttr` W/R ยังเขียน
    `EMPTY` (อ่านจาก slot `+0x18`) — RE-061 พบ serializer จริงของตระกูล Attr อยู่ `+0x34` ⇒ กติกา "ดูแถว TSV
    ต้องไม่ EMPTY" ใช้กับตระกูล Attr ไม่ได้ · TSV เป็นไฟล์ derive จาก image (ห้าม hand-edit บน cloud) —
    แจ้งในจดหมายรอบนี้ให้ฝั่งสะพานพิจารณา regenerate extractor ให้รู้จัก `+0x34` หรือหมายเหตุแถว
  - **คำถามเปิด (เปิดเป็น RE-062):** inbound `0x1661` **สร้าง** container ที่ `[actor+0x3E8]` ได้ไหมตอน null
    หรือได้แค่อัปเดต — ตัดสินว่า sweep นี้พลิก gate ได้เชิงโครงสร้างหรือไม่ · เป็นกุญแจอ่านผลลบ GT-059
  - หลังแก้ D1/D2: **สวีตเต็ม 2103/324/0 เขียว(cloud sanity) อีกครั้ง**
- **commit/push/PR:** repo โค้ด commit `01b8b9e` (12 ไฟล์: 3 ใหม่ 9 แก้ · declared ตรง staged · ไม่มี deletion)
  → push `claude/amazing-goodall-zip9tr` → **PR #21** (marker ครบ) — **รอ gate · workflow merge เอง**
- **ใบเทสใหม่:** `GAME_TEST_QUEUE.md` เพิ่ม **GT-059 SKILL-ATTR-WINDOW-GATE-001** (pf-queue-author เขียน ·
  chief วาง): baseline replicate GT-058 ก่อน → sweep → K/ปุ่ม tri-state → relog variant (P3) · สองชั้นแยกเด็ดขาด ·
  "ผลลบมีค่าเท่าผลบวก" + redirect ไป RE-062 · กำกับ "รอ merge PR #21 ก่อน" ครบสามเงื่อนไข
- `CLIENT_RE_QUEUE.md`: เปิด **RE-062 SKILLATTR-BIND-NULL-BRANCH-001** (ใบเปิดค้างเหลือใบเดียว)

## เรื่องที่ไม่ได้พิสูจน์ (nonclaims ของรอบ)

- ไม่พิสูจน์ว่า client เปิดหน้าต่างสกิลเมื่อรับเฟรม (นั่นคือหน้าที่ GT-059 · NONCLAIM ของ RE-061 ยังยืน)
- ไม่พิสูจน์ว่า inbound สร้าง container ได้ตอน slot null (RE-062 เปิดไว้)
- version byte 0 ของ vital เป็นดีไซน์เรา ยัง unpinned
- เขียวทั้งหมดในรอบนี้คือ **เขียว(cloud sanity)** — gate จริงคือ Actions/สะพาน (PR #21 ยังรอ)

## สรุปเวลา/กลไก

- ลูกมือที่ใช้: general-purpose (implement) · pf-adversary (บังคับ) · pf-queue-author (ใบ GT-059) — ครบตามกติกา ④
- อุบัติเหตุ: ลูกมือ implement ตายหนึ่งครั้งด้วย API 529 (overload ฝั่ง Anthropic ชั่วคราว) — resume สำเร็จ งานไม่หาย
- จบรอบ: push pf_bridge → ปลด draft PR #50 → แก้หัวข้อ/บอดี้ (ลำดับ ①②③ ตาม v5)

