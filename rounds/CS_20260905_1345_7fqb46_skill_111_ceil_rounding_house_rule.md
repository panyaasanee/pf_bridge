# CS round 7fqb46 — skill_points_after_learning: ceil-rounding house rule for fractional SP cost

เวลาเริ่ม 2026-09-05 13:38 +07:00 · เวลาจบ 2026-09-05 ~14:05 +07:00

## ขั้นตอน 0 — `NOW.md` ก่อนทุกอย่าง

อ่านแล้ว (`git fetch origin main` ก่อน) หัวข้อล่าสุด `12:48` (COO): NOW ขยับ 2 จุด — ข้อ CS ตรงบรรทัด:
"ต้นทุนเศษสกิล 111 = **ceil 1 แต้ม** กฎบ้านทุก id (`1245` · PR 13:06 ตก 14:36)" — **นี่คืองานของรอบนี้โดยตรง**
(ดูกล่องจดหมายข้างล่าง) ไม่มีข้ออื่นใน NOW ที่เป็นคำสั่งใหม่ถึง LANE-CS โดยตรง · ยังอยู่ M2 · P-2 (สีชื่อมอน)
ยังไม่ปิด ⇒ `GT-146`/ใบตีมอนทุกใบยังบล็อกเหมือนเดิม (มาตรา "ห้ามทำจนกว่า P-2 จะปิด")

**รอบนี้ขยับ NOW/M ข้อไหน**: ไม่ขยับขั้นบันได M (`resolve_class_skill_damage`/`attack_skill_ids_for_class`
ยัง zero production caller เหมือนเดิม รอ `GT-243`) — ปิดกฎบ้านที่ COO สั่งไว้ใน NOW บรรทัด `12:48`/จดหมาย
`1245` ตรงเวลา (สั่งไว้ "รอบ 13:06" รอบนี้เริ่ม 13:38 — ช้ากว่ากำหนด ~32 นาที เพราะรอบก่อน `zk4qwp` ถอยให้ PR
ที่เปิดอยู่ตอน 12:07 แล้วรอบถัดไปมาตามตารางยิง :06/:36 ปกติ ยังอยู่ในกรอบ deadline `14:36` เดิม ไม่ถือเป็น
escalation)

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]` ทั้งสองรีโป

`list_pull_requests` `state:open` ทั้งสองรีโป:
- `pirate-force-server`: 0 ใบหัว `[LANE-CS]` (เปิดอยู่ `#823` LANE-DB · `#794` LANE-E — ไม่เกี่ยว) ⇒ ไม่ถอย
- `pf_bridge`: 0 ใบหัว `[LANE-CS]` (เปิดอยู่ `#1320` LANE-B · `#1319` LANE-A · `#1318` LANE-GM · `#1317`
  LANE-DB — ไม่เกี่ยว) ⇒ ไม่ถอย เปิดรอบใหม่ได้ตามปกติ

## ขั้นตอน 2 — `ADVERSARY_PENDING` จากรอบก่อน

ไม่มีค้าง — รอบก่อน (`zk4qwp`) ถอยเฉย ๆ ไม่ได้สั่ง adversary

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` กรองใบที่มี `.CONSUMED.txt` แล้ว — **พบ 2 ใบค้าง**:

1. **`20260905_1245_COO-DECISION-skill-111-fractional-cost-rounds-up-ceil-house-rule-for-any-fractional-sp-cost-LANE-CS.md`**
   — งานหลักของรอบนี้ (ดูหัวข้อ "งานที่ทำ" ข้างล่าง) `.CONSUMED.txt` สร้างแล้ว
2. **`20260905_1326_SYNC-NOTICE-pf_bridge-pr1307-closed-never-merged.md`** — สัญญาณจาก `pf_git_sync`
   (round `tde2wv`, PR `#1307`, สาขา `claude/admiring-thompson-llk82x`, ปิด 06:21:47Z ไม่ merge) ตรวจแล้ว:
   - งานฝั่งเซิร์ฟเวอร์ของรอบ `tde2wv` (`n_TARGET` ก็ไม่ใช่คอลัมน์ประเภทสกิล — ผลลบเหมือน `n_PASSIVE`)
     **merge ขึ้น main แล้วจริง**: `pirate-force-server#816` `merged_at: 2026-09-05T05:29:35Z`
     (`merged_by: github-actions[bot]`) — ยืนยันด้วย `pull_request_read` ตรง ไม่เดาจาก log
   - เนื้อในของ PR ที่ตายฝั่ง pf_bridge มีแค่ไฟล์รอบเดียว
     (`rounds/CS_20260905_0922_tde2wv_ntarget_bounded_negative.md`, ตรวจด้วย `git diff origin/main
     FETCH_HEAD --stat` บนสาขา `claude/admiring-thompson-llk82x` ที่ยังอยู่จริงบน remote) — บันทึกไว้ว่า
     "รอ chief ตั้งเลข RE ต่อ" ของ `n_TARGET` แต่ไม่มี state/lock อื่นที่ต้องกู้
   - **ไม่มีรอบ LANE-CS ไหนกำลังเดินต่อจาก `tde2wv` อยู่** (สายนี้เดินต่อผ่าน `mps8zh`→`30kpco`→`zk4qwp`→
     รอบนี้ทั้งหมดแล้ว) ⇒ ทำตามข้อความของ notice เอง: "ถ้ารอบยังไม่ตายให้ push งานจริงเข้ากิ่งเดิม มิฉะนั้น
     รอบถัดไปถือเป็น claim ตายแล้วเปิดของตัวเอง" — **ถือเป็น claim ตายแล้ว ไม่ resurrect กิ่งเดิม**
     (กิ่ง `claude/admiring-thompson-llk82x` ค้างอยู่บน remote ตามเดิม ไม่มีอะไรหาย ตรงตามที่ notice
     รับประกันไว้ — โค้ดจริงอยู่ใน `#816` แล้ว ส่วนไฟล์รอบเป็นแค่บันทึกประวัติ ไม่ใช่ตัวบล็อกงานใคร)
   `.CONSUMED.txt` สร้างแล้ว

## งานที่ทำ — ปิด `COO-DECISION 20260905_1245`

`skill_learn_validator.skill_points_after_learning` เดิมปฏิเสธทุก `skill_id` ที่ต้นทุนเป็นเศษ (ผลจากรอบ
`30kpco`) — COO ตัดสินแล้วว่าให้ปัดขึ้นแทน:

- ต้นทุนเศษ (ไม่ใช่จำนวนเต็ม) ⇒ หัก `math.ceil(cost)` แต้ม — **กฎบ้านทุก skill id** ไม่ใช่กรณีพิเศษของ 111
  (docstring เขียนชัดว่าเป็นกฎทั่วไป ไม่ hardcode เลข 111)
- สกิล 111 ("VIP Strive Jump", cost `0.20000000298023224`) ⇒ หัก **1 แต้ม** ตรงตามตัวอย่างในจดหมาย
- ต้นทุน **≤ 0** (ไม่มีจริงในตาราง ณ ตอนนี้ — มีแค่ 7 ตัว `1.0` + 1 ตัว `0.2...` ในคาตาล็อก 8 id) ⇒ ยังปฏิเสธ
  เหมือนเดิม (`SkillLearnValidatorError`) ไม่ปัดเป็น 0 ไม่หักติดลบ — เทสใหม่จำลองด้วย
  `unittest.mock.patch.object(skill_catalog, "skill_point_cost_to_learn", return_value=0.0/-1.0)` เพราะ
  ไม่มี id จริงให้ทดสอบตรง ๆ
- ไม่แตะ `can_afford_to_learn` ส่วนเปรียบเทียบ (`current_skill_points >= cost` ด้วยต้นทุนดิบ) — พิสูจน์ในโค้ด
  ว่ายังพอ: ยอดเป็น `int`ที่ `>=` ต้นทุนจริง (เลขจริงไม่ใช่จำนวนเต็ม) แปลว่ายอดนั้น `>=` ค่าปัดขึ้นของต้นทุนด้วย
  เสมอ (ข้อเท็จจริงทางคณิตศาสตร์ ไม่ใช่ heuristic) ⇒ ผลลัพธ์หลังหักไม่มีทางติดลบ
- `characters.skill_points` คง `INTEGER` ตามเดิม (ตัวเลือก 3/2/4 ของจดหมายปิดหมดแล้ว)

เทสใหม่/แก้ (`SkillPointsAfterLearningTests`):
- `test_fractional_cost_id_spends_the_ceiling_of_the_cost` — หักลง `ceil(cost)` พอดีที่ยอดเกิน 50
- `test_id_111_spends_exactly_one_point` — ตัวอย่างของจดหมายตรงตัวอักษร
- `test_fractional_cost_spend_never_goes_negative_at_the_smallest_affording_balance` — ยอดพอดี
  `ceil(cost)` เหลือ 0 ไม่ติดลบ
- `test_non_positive_cost_refused_not_rounded_to_zero_or_spent_negative` — ต้นทุน 0/ติดลบ (mocked) ปฏิเสธ
- ลบ `test_fractional_cost_id_refuses_rather_than_guessing_a_rounding_rule` +
  `test_fractional_refusal_fires_even_though_the_balance_affords_it` (พฤติกรรมเดิมที่จดหมายนี้พลิก)

**มิวแทนต์ (ง) — ตรวจมือ**: สลับ `math.ceil` เป็น `math.floor` ในซอร์ส รันชุดเทสไฟล์นี้ ⇒ **3 เทสแดงจริง**
(`51 != 50`, `1 != 0` × 2) ยืนยันว่าเทสจับมิวแทนต์ได้จริง ไม่ใช่ผ่านลอย ๆ แล้วคืนซอร์สกลับก่อน commit

## pf-adversary — ผลคืนแล้ว ไม่มี `ADVERSARY_PENDING`

สั่งบนเวิร์กทรีแยกทันทีต้นรอบพร้อมเริ่มงาน (`git worktree` แยก อ่านโค้ดจริงผ่าน `Read` เท่านั้น ไม่แตะต้นไม้จริง)
ผลกลับมาก่อน push:
1. ยืนยันข้อพิสูจน์คณิตศาสตร์ (`int >= ต้นทุนจริงที่ไม่ใช่จำนวนเต็ม ⇒ int >= ceil ของมัน`) ด้วยการสุ่ม
   float32-derived 200,000 ค่าเทียบทุก int ใกล้เคียง — ไม่พบข้อขัดแย้งเลย
2. อ่าน TSV ต้นทางเอง (ทั้งสำเนาในเซิร์ฟเวอร์ + ต้นฉบับ `pf_bridge/gamedata`) ยืนยันอิสระว่ามีแค่ id 111
   เป็นเศษ ค่า `0.20000000298023224` ตรงกับที่จดหมาย/โค้ดอ้าง
3. ทำมิวแทนต์ `ceil→floor` เองอิสระ ยืนยัน 3 เทสแดงตรงกับที่รายงานไว้ (`51 != 50`, `1 != 0` × 2) ไม่ใช่ลูปว่าง
4. ยืนยันการ์ด `cost <= 0` เป็นโค้ดที่ทำงานจริง ไม่ใช่ dead code — **พบจุดสังเกต (ไม่ใช่บั๊กในสโคปที่สั่ง)**:
   `can_afford_to_learn` เองยังคืน `True` ให้ต้นทุน `<= 0` เสมอ (ไม่มีการ์ดของตัวเอง) ในขณะที่
   `skill_points_after_learning` ปฏิเสธคู่ `(balance, skill_id)` เดียวกัน — สองฟังก์ชันตอบไม่ตรงกันสำหรับ
   ต้นทุน `<= 0` (ยัง zero production caller เหมือนเดิม ไม่กระทบผู้เล่นตอนนี้ แต่จุดเสียบเรียนสกิลในอนาคตต้อง
   รู้ว่าฟังก์ชันไหนเป็นตัวตัดสิน) — **ส่งต่อเป็นข้อสังเกตในหัวข้อ "ติดอะไร" ข้างล่าง ไม่ใช่งานของรอบนี้**
5. ตรวจชื่อ/คอมเมนต์เทสใหม่ทั้งสี่ตัวเทียบกับสิ่งที่วัดจริง — ไม่มี overclaim
6. ไม่พบข้อผิดอื่นในดิฟ (double-call ของ `skill_point_cost_to_learn` ไม่มีความเสี่ยง TOCTOU เพราะตารางโหลด
   ครั้งเดียวตอน import เป็น dict immutable)

ไม่มีข้อใดต้องแก้ก่อน push

## ชุดเต็ม + preflight

`git fetch origin main` → `origin/main` (`173addce`) ตรงกับที่แตกกิ่งไว้แล้ว (ไม่ต้อง merge ซ้ำ) → รันชุดเต็ม
ครั้งเดียวติดกับ push:

```
python3 -m pytest tests -q -rs
```

ผล: **`10877 passed, 323 skipped, 20213 subtests passed` (517.92s · cloud sanity)** — 🔴 หมายเหตุ: รันครั้งแรก
ระหว่างรอผล เผลอสั่ง `pytest tests -q` ซ้ำอีกชุดในไดเรกทอรีเดียวกันแบบขนาน (เพื่อ grep หา `FAILED` จากรันแรกที่
ตัด output ด้วย `tail -20` ไปเห็นแค่ `5 failed`) ⇒ สองโปรเซสแย่ง `.pytest_cache`/ทรัพยากรกัน ทำให้รันแรกรายงาน
เท็จ `5 failed` — kill โปรเซสที่สองแล้ว `rm -rf .pytest_cache` รันใหม่ **ครั้งเดียวโดดๆ** ได้ผลข้างต้น (เขียว
ล้วน ไม่มี failed แม้แต่ตัวเดียว) ตัวเลขที่ใช้ตัดสิน push คือรันสะอาดนี้เท่านั้น ไม่ใช่รันที่ปนกัน

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` (รันสองรอบ — ก่อน/หลัง commit ฝั่ง
เซิร์ฟเวอร์): **PREFLIGHT PASS** ทั้งสองครั้ง (cp874 · ไม่มี skip ใหม่ · main อยู่ในกิ่งแล้ว · census ตรง ·
ทั้งสองกิ่งไม่ใช่ `main`)

**ไม่มีไฟล์เทสใหม่/skip ใหม่** (แก้ไฟล์เดิม `tests/test_skill_learn_validator.py` เพิ่ม/แก้เทสในคลาสเดิม)
⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census` แยก

## `TWO_SESSIONS_SAME_SCENE:`

ไม่เกี่ยว — โมดูลนี้ไม่แตะ world state/registry ของฉาก (zero production caller, pure arithmetic, ไม่มี DB/wire/
socket ตามที่ module docstring ระบุ) กฎ shared-world ของ `PANYA-DECISION 20260905_1057/1130/1140` ไม่มีผลกับ
งานรอบนี้

## ส่งอะไร

**pirate-force-server**: PR (สาขา `claude/pensive-bardeen-7fqb46`, commit `c7b3c674`) —
- `src/pirateforce_foundation/skill_learn_validator.py`
- `tests/test_skill_learn_validator.py`

**pf_bridge**: PR (สาขา `claude/vigilant-ramanujan-7fqb46`) — ไฟล์นี้ +
- `.CONSUMED.txt` × 2 (`1245`, `1326`)

## nonclaims

- ไม่อ้างว่าเรียนสกิลได้จริงในเซสชันผู้เล่น — ยัง zero production caller เหมือนทุกโมดูลพี่น้อง
- ไม่อ้างว่าปิดจุดเสียบ `store.py` (CORE-REQUEST ของรอบ `30kpco` ข้อ 1 ยังรอ chief เหมือนเดิม ใบนี้ไม่แตะ)
- ไม่ resurrect กิ่ง `claude/admiring-thompson-llk82x`/PR `#1307` — ถือเป็น claim ตายตามที่ notice สั่งเอง
  โค้ดจริงของรอบนั้นอยู่บน main แล้ว (`#816`) ไม่มีอะไรหาย

## ติดอะไร / ใครปลด

- ตัวบล็อกเดิมคงอยู่: `GT-243` ต้องเครื่อง Panya · P-2 ยังไม่ปิด (บล็อกใบตีมอนทุกใบ) · CORE-REQUEST
  `store.py` (รอบ `30kpco`) รอ chief
- **ข้อสังเกตใหม่จาก pf-adversary รอบนี้ (ไม่บล็อกใคร ณ ตอนนี้ — zero production caller)**: `can_afford_to_learn`
  กับ `skill_points_after_learning` ตอบไม่ตรงกันสำหรับต้นทุน `<= 0` (ตัวแรกไม่มีการ์ดของตัวเอง คืน `True`
  เสมอ ตัวหลังปฏิเสธ) — เมื่อจุดเสียบเรียนสกิลจริงมาถึง ต้องรู้ว่าฟังก์ชันไหนเป็นตัวตัดสินสำหรับ id แบบนี้
  (ยังไม่มีจริงในตาราง) ส่งเป็นข้อสังเกตให้ COO/chief พิจารณาตอนออกแบบจุดเสียบ ไม่ใช่คำถามที่บล็อกรอบนี้

-- LANE-CS
