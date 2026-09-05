# CS round 30kpco (resumed session) — `skill_points_after_learning` + store.py CORE-REQUEST + COO ask on id 111

เวลาเริ่ม 2026-09-05 ~11:30 +07:00 (คอนเทนเนอร์รีสตาร์ตกลางงานของรอบก่อนหน้าคนละเซสชัน ไม่ใช่ของรอบนี้ — ดู
หัวข้อ "หมายเหตุ" ท้ายไฟล์) · เวลาจบ 2026-09-05 11:54 +07:00

## ขั้นตอน 0 — `NOW.md` ก่อนทุกอย่าง

อ่านแล้ว (`git fetch` ก่อน) หัวข้อล่าสุด `10:45` (COO): NOW ขยับ 3 จุด (RE-256 DONE → GT-233 layout gate ปลด ·
GT-247 PASS R315 → ท่าโจมตี production หลังฉาก 4 · GT-245 ครึ่งแรก PASS) — ไม่มีข้อไหนเป็นตัวบล็อก/งานของ CS
โดยตรง · ยังอยู่ M2 · P-2 (สีชื่อมอน) ยังไม่ปิด ⇒ `GT-146`/ใบตีมอนทุกใบยังบล็อกเหมือนเดิม (มาตรา "ห้ามทำจนกว่า
P-2 จะปิด")

**รอบนี้ขยับ NOW/M ข้อไหน**: ไม่ขยับขั้นบันได M (ยัง zero production caller) — ต่อยอดคิวเริ่มต้นข้อ 5 (ระบบ
เรียนสกิล/skill point) ที่รอบ `6r13k5` เปิดไว้

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]` ทั้งสองรีโป

- `pirate-force-server`: `#811` "[LANE-CS] round mps8zh" เปิดค้างตอนเริ่มตรวจ (อายุ ~1 ชม. 20 นาที ตอนเริ่ม) —
  **ไม่ใช่ของ NOW.md ใหม่ เป็นรอบก่อนหน้าคนละเซสชัน (`session_01VFmw4BzcM6md69GUbAS9ou`) ที่ทิ้ง
  `GATE_UNVERIFIED #811` ไว้ให้รอบถัดไปตรวจ** — ตรวจแล้ว: เกต `pull_request` ของ `#811` (`THE GATE` step)
  ยังรันจริงอยู่ (ไม่ใช่ค้าง — sibling run `push` event เดียวกันปิดสำเร็จใน ~25 นาทีพอดี ตัวเลขใกล้เคียงกัน) รอ
  จนจบ: **merge สำเร็จ 04:41 UTC (11:41+07)** ⇒ ปิดข้อค้างนี้ ไม่ต้องเขียน `GATE_UNVERIFIED` ต่อ
- `pf_bridge`: 0 ใบหัว `[LANE-CS]` เปิดค้าง (มี `#1303` LANE-DB claim — ไม่เกี่ยว) ⇒ ไม่ถอย เปิด claim ที่นี่
  ได้ตามปกติ

## ขั้นตอน 2 — `ADVERSARY_PENDING`

ไม่มีค้างจากรอบก่อน (`mps8zh` ปิดผล adversary ในรอบนั้นเอง) · รอบนี้เองก็ปิดผล adversary ในรอบเดียวกัน (ดูล่าง)
ไม่ทิ้ง pending ต่อ

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`) — **ทุกใบมี `.CONSUMED.txt` แล้ว**
รวมถึง `20260905_0030_CHIEF-TO-LANE-CS-hypothesis-ledger-bump-answer-v002.md` (คำตอบเรื่อง governance gate ของ
`docs/HYPOTHESIS_LEDGER.json` ที่ค้างมาตั้งแต่รอบ `30kpco` เดิม — chief ตอบและแก้ไฟล์เองแล้วตั้งแต่ 00:30 วันนี้
ยืนยันซ้ำว่าปิดจริง ไม่ใช่แค่เห็นว่ามี `.CONSUMED.txt`: อ่านเนื้อใบตอบครบแล้ว ตรงตามที่ pf-adversary รอบ `h4mxrq`
ถามไว้) ไม่มีใบใหม่รอบนี้

## งานที่ทำ — `skill_points_after_learning` (คิวเริ่มต้นข้อ 5 ต่อจาก `6r13k5`)

`can_afford_to_learn`'s docstring เองระบุไว้ว่า "deducting the cost... is a caller's job" — รอบนี้สร้างครึ่ง
นั้น: `skill_points_after_learning(current_skill_points: int, skill_id: int) -> int` ฟังก์ชันบริสุทธิ์ ไม่แตะ
DB/wire เหมือนเดิม

**สิ่งที่เจอระหว่างทำ**: `skill_catalog.skill_point_cost_to_learn(111)` ("VIP Strive Jump") = `0.2000...`
(เศษ) ในขณะที่คอลัมน์จริง `characters.skill_points` เป็น `INTEGER` (CHECK บังคับ) — ไม่มีกติกาบ้านตัดสินไว้ว่า
ต้นทุนเศษหักกับยอด INTEGER ยังไง ⇒ ฟังก์ชันนี้ **ปฏิเสธ** (`SkillLearnValidatorError`) แทนการเดากติกาปัดเศษเอง
(อีก 7 ตัวต้นทุน `1.0` พอดี หักปกติ)

`tests/test_skill_learn_validator.py` เพิ่มคลาส `SkillPointsAfterLearningTests` (10 เทสใหม่)

## pf-adversary — ผลคืนแล้ว ไม่มี `ADVERSARY_PENDING`

สั่งบนเวิร์กทรีแยกทันทีหลังไฟล์แรกเขียนเสร็จ: อ่าน TSV ดิบเองยืนยันตัวเลข 7×1.0 + 1×0.2 ตรง (ไม่เชื่อ docstring
เฉย ๆ) · ยืนยันไม่มี state ผันแปรระหว่างสองครั้งที่เรียก `skill_point_cost_to_learn` · มิวเทตการ์ดทั้งสี่ตัว
(affordability pre-check, fractional-cost refusal, `int()` cast, type/negative guard) — ทุกตัวถูกจับ **ยกเว้น
จุดเดียว**: เทส `test_negative_balance_refused_before_any_spend_is_computed` ชื่อ/คอมเมนต์อ้างว่าแยกการ์ด
ยอดติดลบของฟังก์ชันนี้เอง แต่จริง ๆ ผ่านเพราะการ์ด affordability (ทุกต้นทุนในแคตาล็อกเป็นบวก ยอดติดลบเลย "ซื้อ
ไม่ไหว" อยู่แล้วก่อนถึงจุดเช็คเศษ) ไม่ใช่บั๊ก production (test suite รวม `CanAffordToLearnTests` เดิมจับ
มิวเทชันนี้ได้อยู่ดี) แต่เป็น overclaim ของถ้อยคำเทส — **แก้แล้ว**: เปลี่ยนชื่อเป็น
`test_negative_balance_refused_same_as_can_afford_to_learn` + คอมเมนต์อธิบายตรง ๆ ตามที่ adversary พบ

## ชุดเต็ม + preflight

`git fetch origin main` → main ขยับจาก `b49a4e4`→`2f7a7ae` (LANE-GM `#812`) → `git checkout -B` สาขาที่ระบบ
ให้จาก `origin/main` สด (สาขาเดิม `claude/pensive-bardeen-30kpco` merge ไปแล้วรอบก่อน — รีสตาร์ตสาขาจาก main
ล่าสุดตามกติกา "PR ที่ merge แล้วต้องรีสตาร์ตสาขาเดิมจาก main ไม่ต่อยอดของเก่า") → รันชุดเต็มครั้งเดียวติดกับ
push:

```
python3 -m pytest tests -q -rs
```

ผล: **`10819 passed, 323 skipped, 19938 subtests passed` (454.96s)** — เขียว

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS** (ต้องแก้ก่อน
ผ่าน: สาขา pf_bridge ยังค้างที่ `main` ตอนแรก — สลับไป `claude/vigilant-ramanujan-30kpco` จาก origin/main สด
ก่อน ถึงผ่าน `[branch]` check ทั้งคู่)

**ไม่มีไฟล์เทสใหม่/skip ใหม่** (แก้ไฟล์เดิมเพิ่มคลาส) ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census`

## ส่งอะไร

**pirate-force-server**: PR **#815** (`claude/pensive-bardeen-30kpco`) —
`https://github.com/panyaasanee/pirate-force-server/pull/815`
- `src/pirateforce_foundation/skill_learn_validator.py` (+`skill_points_after_learning` + docstring update)
- `tests/test_skill_learn_validator.py` (+`SkillPointsAfterLearningTests`, 10 เทส + แก้ชื่อเทสเดิม 1 ตัว)

**pf_bridge**: PR (สาขา `claude/vigilant-ramanujan-30kpco`) — ไฟล์นี้แทน claim
- `notes_to_chief/20260905_1154_LANE-CS-CORE-REQUEST-store-py-skill-points-hookup-plus-ask-COO-fractional-cost-id-111-ruling.md`
  (CORE-REQUEST ถึง chief: จุดเสียบ `store.py` อ่าน/หัก `skill_points` จริง + ถาม COO เรื่องต้นทุนเศษของสกิล 111)

## nonclaims

- ไม่อ้างว่าเรียนสกิลได้จริงในเซสชันผู้เล่น — ยัง zero production caller เหมือนทุกโมดูลพี่น้อง
- ไม่อ้างว่าตัดสินกติกาปัดเศษของสกิล 111 เอง — ส่งเป็นคำถามให้ COO ตัดสิน (ข้อ 2 ในจดหมาย) ไม่เดา
- ไม่แตะ `store.py`/`characters` table เอง — ขอ chief เป็น CORE-REQUEST ตามเขตเขียน
- ไม่อ้างว่า `#811` (รอบ `mps8zh` คนละเซสชัน) เป็นงานของรอบนี้ — แค่ตรวจผลเกตตามกติกา "รอบถัดไปเปิดด้วยการตรวจ
  ก่อน" แล้วรายงานว่าปิดแล้ว (merge สำเร็จ ไม่ใช่ปัญหา)

## ติดอะไร / ใครปลด

- **จุดเสียบ `store.py`** — รอ chief (CORE-REQUEST ข้อ 1 ในจดหมาย)
- **กติกาปัดเศษของสกิล 111** — รอ COO/Panya (ข้อ 2 ในจดหมาย) ไม่บล็อกงานอื่นของ CS
- ตัวบล็อกเดิมคงอยู่: `GT-243` ต้องเครื่อง Panya · P-2 ยังไม่ปิด (บล็อกใบตีมอนทุกใบ)

## หมายเหตุ — คอนเทนเนอร์รีสตาร์ต

เซสชันนี้ถูกรีสตาร์ตกลางคัน (งาน background หนึ่งชิ้น — pytest wait-loop ของรอบ `mps8zh` คนละเซสชัน — หายไป
ตอนรีสตาร์ต ไม่ใช่งานของเซสชันนี้เอง ไม่มีอะไรต้องกู้คืนฝั่งนี้: ตรวจแล้วทั้งสอง working tree สะอาด ไม่มี diff
ค้าง) รอบนี้จึงเริ่มด้วยการตรวจสถานะสดใหม่ทั้งหมดตาม §7 ปกติ ไม่ได้ข้ามขั้นตอนใด

-- LANE-CS
