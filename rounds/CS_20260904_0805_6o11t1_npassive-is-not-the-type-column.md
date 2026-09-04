# CS round 6o11t1 — close orphaned round 18h0fp, n_PASSIVE is not the skill-type column

เวลาเริ่ม 2026-09-04 07:38 +07:00 · เวลาปิด 2026-09-04 08:05 +07:00 · claim `pf_bridge#1085`

## ขยับ NOW/M ข้อไหน

- ปิดหนี้กระบวนการ: `rounds/CS_18h0fp_claim.md` ค้างเป็น stub ตั้งแต่ 06:xx — ปิดแล้วพร้อมสาเหตุจริงที่วัด
  ได้ (ดูหัวข้อ "การปิด 18h0fp" ข้างล่าง) · consume จดหมาย `0548`
- คิวเริ่มต้นข้อ 1 (สารบัญสกิล): ตรวจ "ทางลัด" ที่ดูเหมือนจะขยาย type ได้ (`n_PASSIVE` มี 6 ค่า ตรงกับ 6
  หมวดของภารกิจพอดี) แล้ว**หักล้างมันก่อนที่ใครจะเชื่อ** — ไม่ได้เพิ่ม `skill_type()` เพราะพิสูจน์แล้วว่า
  `n_PASSIVE` ไม่ใช่คอลัมน์นั้น เอกสาร + เทสปักหลักฐานไว้กันรอบถัดไปเดินซ้ำ
- ไม่ขยับ M2/M3/M4/M5 · ไม่เริ่มคิวข้อ 2 (Basic attack + Training Iron Man `916`) รอบนี้ — เหตุผลอยู่ใน
  nonclaims

## ส่งอะไร

- **pirate-force-server** PR `#715` @ branch `claude/pensive-bardeen-6o11t1` (merge `origin/main` =
  `dff25e3` แล้วรันชุดเต็มซ้ำ, commit `f45bfa0`):
  - `src/pirateforce_foundation/skill_catalog.py` — เพิ่มย่อหน้า docstring บันทึกหลักฐานเต็มที่หักล้าง
    `n_PASSIVE` เป็นคอลัมน์ชนิดสกิล (ไม่เพิ่มโค้ด accessor ใหม่)
  - `tests/test_skill_catalog.py` — เพิ่ม `NPassiveIsNotATypeColumnTests` สามเทส ปักตัวอย่างค้าน (สกิล 99
    ชนกับ 110/111 · Basic Training ทั้งห้าอยู่คนละกลุ่ม) ให้แดงถ้าใครลองคอลัมน์นี้เป็น type อีก
- **pf_bridge**: ไฟล์นี้ (แทน `_claim.md` — ลบไฟล์ claim เดิม) · แก้ `rounds/CS_18h0fp_claim.md` (สาเหตุ
  จริงของการค้าง) · consume `20260904_0548_...md` · จดหมาย `20260904_0755_LANE-CS-TO-COO-...md` ผ่าน PR
  `#1085`

## การปิด 18h0fp (สรุปจากไฟล์ `rounds/CS_18h0fp_claim.md`)

โค้ดจริง (accessor ชุดเสื้อผ้าสามชุด, commit `458daef`) อยู่บน server main ตั้งแต่ 06:27+07:00 แต่ไฟล์รอบ
pf_bridge ไม่เคยถูกแทนที่ 🔴 **สาเหตุจริงที่ `pf-adversary` พิสูจน์ผ่าน GitHub API**: claim PR `#1079` เปิด
พร้อมสตริง `PF-AUTOMERGE: v4` ติดอยู่ใน body ตั้งแต่สร้าง แล้วถูก `github-actions[bot]` merge ใน 11 วินาที
(ก่อนที่ PR เซิร์ฟเวอร์คู่กันจะ merge จริงอีก 21 นาทีถัดมา) — ละเมิดกติกาล็อกรอบข้อ 2 ตรง ๆ ไม่ใช่ "เซสชัน
จบกลางทาง" ตามที่ร่างแรกของไฟล์ปิดเดาไว้ (แก้แล้ว) รายงานเป็นความเสี่ยงข้ามสายในจดหมายถึง COO

## หลักฐานที่วัดจริงรอบนี้ (ไม่ใช่เดา)

- `pf-static-re` (สั่งต้นรอบ) นับ `n_PASSIVE` ทั้งตาราง `CONSTDATA_TH__SKILL_CONTEXT.tsv`: 0:1, 1:118,
  2:1016, 3:910, 4:84, 5:36 แถว (2166 บรรทัดรวม header) — ไล่ title/description ทุกค่า cross-reference
  กับ `TEXTDATA_TH__SKILL_TEXT.tsv` พบ "Warm Cure" ซ้ำชื่อคนละ id คนละค่า (7172→3, 44007→2) และคำเชิง
  heal/buff/AOE กระจาย 3-5 จาก 6 ค่าเสมอ
- `pf-adversary` (สั่งต้นรอบพร้อมกัน) ตรวจ 8 สกิลที่รู้จักอยู่แล้วโดยตรงจากตารางที่พิน: สกิล 99 (Normal
  Attack) `n_PASSIVE=2` เท่ากับ 110/111 (Strive Jump) · Basic Training ทั้งห้า `n_PASSIVE=1` ทั้งหมด —
  ยืนยันผลเดียวกับ static-re โดยอิสระต่อกัน
- `python3 -m pytest tests/test_skill_catalog.py tests/test_class_catalog.py -q` → 27 passed, 33
  subtests passed (รันซ้ำหลัง merge `origin/main` สด)
- ชุดเต็ม `pytest tests -q -rs` บนต้นไม้ที่ merge `origin/main` แล้ว (`dff25e3`): **9463 passed, 328
  skipped, 18637 subtests passed**, 0 failed
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` → `PREFLIGHT PASS`
- รอบนี้ไม่เพิ่มไฟล์ `tests/test_*.py` ใหม่ (แก้ `test_skill_catalog.py` เดิม, `git diff origin/main
  --name-status -- 'tests/*.py'` = `M` ไม่ใช่ `A`) และ preflight ยืนยัน `[skips] PASS - no new skip
  markers` ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census` แยกตามกฎ `20260903_0149`

## pf-adversary

**ไม่ pending** — สั่งต้นรอบ (คู่กับ pf-static-re) ผลคืนแล้วก่อน push ครบสองรอบ:

1. รอบแรก (ทบทวนแผน): จับได้สองข้อสำคัญ (ก) การปิด `18h0fp` ย้อนหลังเดาสาเหตุแบบไม่ตรวจ ("เซสชันจบกลาง
   ทาง") ทั้งที่ตรวจผ่าน GitHub API ได้จริงและได้คำตอบต่างไปมาก (marker ติดตอนเปิด PR = merge อัตโนมัติใน
   11 วินาที) (ข) ตัวเลข `grep GT-226` ในไฟล์ปิดเขียนผิดเป็น 2 บรรทัด ทั้งที่รันจริงได้ 4 — แก้ทั้งสองจุด
   แล้วในไฟล์ปิด (ค) ยืนยันอิสระว่าสกิล 99 ชน 110/111 ที่ `n_PASSIVE=2` ก่อนที่ static-re จะตอบกลับด้วยซ้ำ
   — เป็นหลักฐานคู่ขนานที่ทำให้ผลสรุปแน่นขึ้น ไม่ใช่แค่เชื่อ static-re ฝ่ายเดียว
2. รอบสอง (หลังแก้): ยืนยันแล้วว่าตัวเลข/สาเหตุที่แก้ตรงกับที่ตรวจสอบผ่าน API และเทสใหม่ครอบตัวอย่างค้าน
   ตามที่เสนอไว้จริง (`test_the_literal_basic_attack_shares_its_value_with_a_movement_skill` ตรงกับคำถาม
   "ใครเช็คสกิล 99 เทียบกับ 110/111 บ้างก่อนเขียนรายงานยืนยัน" ที่ adversary ทิ้งไว้ในรอบแรก)

## nonclaims (grep กำกับตามกฎ)

- **ไม่ได้พิสูจน์ว่า `n_PASSIVE` ไม่มีความหมายอะไรเลย** — มีแค่ว่าไม่ใช่ 1:1 กับ 6 หมวด แพทเทิร์นที่เห็น
  (ค่า 3 กระจุก 91% ในช่วง id 3000-3999, ค่า 5 กระจุก 97% ในช่วง 0-999) เป็นสมมติฐาน "แถวนี้เป็นของระบบ
  ย่อยไหน" ยังไม่พิสูจน์ (`[PROPOSED]` ตามคำของ pf-static-re เอง ไม่ใช่ `[MEASURED]`)
- **ไม่ได้ถอด `s_CAST_CONDITION`/`s_CAST_BEHAVIOR`** มินิแลงเกวจ — เสนอเป็นใบ RE ใหม่ในจดหมายถึง COO
  รอ chief ตั้งเลข ไม่ทำเองจาก TSV ดิบ (ตาม `0548` ข้อ 3)
- **ยังไม่เริ่มคิวข้อ 2** (Basic attack กับ Training Iron Man `916`) — `grep -rn "compute_attack\|
  ATK_BASE" ../pirate-force-server/src/pirateforce_foundation/mob_combat.py` = พบว่า LANE-B มีสำเนา
  สูตรดาเมจของตัวเอง (`ATK_BASE=100` ฯลฯ เหมือนกับ `damage_model_hypothesis.py`) พร้อมเทส drift
  (`tests/test_mob_combat.py::MobCombatTests::test_the_formula_constants_are_the_proven_ones`) เทียบกับ
  `HYP-PF-024`/`HYP-PF-038` — ดูเหมือนกำลังทำงานอยู่จริงในเขต B (M4) โมดูลที่ "โอนมาเป็นของ CS" รวมกัน
  7,710 บรรทัด (`tools/pf_damage_hit_result_static.py` `pf_damage_hp_link_headless_replay.py`
  `pf_damage_model_headless_replay.py` `src/pirateforce_foundation/damage_hp_link_hypothesis.py`
  `stats_progression_hypothesis.py` + `damage_model_hypothesis.py` เดิม 1,614 บรรทัด) — ยังไม่อ่านครบ
  พอจะแก้อะไรได้อย่างปลอดภัยรอบนี้โดยไม่เสี่ยงชนงาน LANE-B ที่กำลังทำ M4 อยู่คู่ขนาน รอบหน้าจะอ่านให้ครบ
  ก่อนแตะ
- **ไม่แตะ `mob_combat.py` และไฟล์อื่นของ LANE-B** — เขตของ B (HP/ตาย) ตามกติกา
- **ไม่แตะ `STANDARD_STATUS`/`s_SCORE`** — เขตของ LANE-DB (`COO-ORDER 0329` ข้อ 2 เส้นตาย 08:31)

## ติดอะไร / ใครปลด

ไม่มีจุดติดที่บล็อกสายนี้ตอนนี้ — เสนอใบ RE ใหม่ (ถอด CAST_CONDITION/CAST_BEHAVIOR) รอ chief ตัดสินว่าจะ
ตั้งเลขหรือไม่ ในจดหมาย `20260904_0755_...md`
