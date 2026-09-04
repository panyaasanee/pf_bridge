# CS round 6r13k5 — `skill_learn_validator.can_afford_to_learn`

เวลาเริ่ม 2026-09-05 ~05:20 +07:00 · claim `pf_bridge` PR #1269

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]`

`pirate-force-server`: `search_pull_requests repo:panyaasanee/pirate-force-server is:pr is:open [LANE-CS] in:title`
→ 0 ใบ · `pf_bridge`: เดียวกัน → 0 ใบ ⇒ ไม่มี `[LANE-CS]` เปิดค้าง ไม่ถอย เปิด claim ได้ตามปกติ (`#1269`)

## ขั้นตอน 2 — `ADVERSARY_PENDING`

ไม่มีค้างจากรอบก่อน (`8p7jon` ปิดผล adversary ในรอบนั้นเอง ไม่มี `ADVERSARY_PENDING` ยกมา)

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`) เจอ 1 ใบ:

`20260905_0013_LANE-CS-TO-COO-mailbox-marker-gap-closed-plus-skill-attr-backup-item-2-3-negative.md`
— **false positive ที่รู้อยู่แล้ว** (จ่าหน้าจริง `ถึง: COO`, เนื้อในอ้างคำว่า "ADDRESSEE: LANE-CS" ตอนอธิบาย
กรณี `1346` เท่านั้น — ยืนยันซ้ำแล้วโดย `h4mxrq`/`9emwkk`/`jbe8rr`/`8p7jon`) ⇒ ไม่ใช่คำสั่งถึง CS ไม่ตอบ/ไม่ปิด
มาร์กเกอร์ (เหมือนทุกรอบที่ผ่านมา) · ไม่มีใบใหม่จ่าหน้า LANE-CS รอบนี้

## อ่าน NOW.md ก่อนทุกอย่าง — ทิศหลักของ CS ถูกบล็อกบางส่วน

`NOW.md` §"ห้ามทำจนกว่า P-2 จะปิด": **GT-146 และใบเทสตีมอนทุกใบ** บล็อกจนกว่า P-2 (สีชื่อมอน) ปิด ยกเว้น
`ATTACK-POSE-ONE-FIELD-AB-001` ใบเดียว (LANE-B) · `NOW.md` §01:45 เดิมเคยแยกไว้ชัดกว่านั้น: "หมวด ข. RE-155
เลื่อนจน P-2 ปิด" — `RE-155` **คือ** สนามเทส Training Iron Man `916` ที่มอบหมายให้สายนี้เป็นสนามมาตรฐาน ⇒
คิวเริ่มต้นข้อ 2 ("Basic attack ทำงานจริงกับ Training Iron Man" บนจอ) และข้อ 4 (สกิลโจมตีตัวแรกของแต่ละอาชีพ
ยิงจริงใส่หุ่น) **ทั้งคู่ต้องการ attended GT ตีหุ่น ⇒ อยู่ในข่ายบล็อกเดียวกัน** จนกว่า P-2 ปิด ไม่ใช่ตัวบล็อกของ
CS เอง (เจ้าของ P-2 = LANE-GM+LANE-B) ⇒ รอบนี้เลือกทิศที่ไม่ต้องรอ attended: **คิวเริ่มต้นข้อ 5 (ระบบเรียน
สกิล/skill point)** ซึ่งเป็น backup item 2 ที่ `8p7jon` เสนอไว้แล้วแต่ยังไม่ได้ลงมือ

## งานที่ทำ — `skill_learn_validator.can_afford_to_learn` (คิวเริ่มต้นข้อ 5)

### `src/pirateforce_foundation/skill_learn_validator.py` (ใหม่)

ฟังก์ชันบริสุทธิ์ `can_afford_to_learn(current_skill_points: int, skill_id: int) -> bool` เทียบยอดคงเหลือ
skill point (int) กับ `skill_catalog.skill_point_cost_to_learn(skill_id)` (คอลัมน์ `f_SP_LEVE1` ที่ pin ไว้แล้ว)
— ไม่อ่าน DB ไม่เขียนอะไร ไม่หักแต้ม (โพสเจอร์เดียวกับ accessor พี่น้องทุกตัวใน `skill_catalog.py`/
`persistence_starting_skills.py`): `TypeError` ถ้า `current_skill_points` ไม่ใช่ `int` แท้ (รวม `bool`) ·
`SkillLearnValidatorError` ถ้าติดลบ · `KeyError` ไหลผ่านถ้า `skill_id` ไม่รู้จัก (ห้ามกลืนแล้วตอบ `False` เพราะ
"แพงเกินจ่าย" กับ "ไม่รู้จักสกิล" เป็นคนละความล้มเหลว)

`tests/test_skill_learn_validator.py` (ใหม่ · 8 เทส)

## pf-adversary — **ผลคืนแล้ว ไม่ใช่ `ADVERSARY_PENDING`**

สั่งทันทีที่ไฟล์แรกเขียนเสร็จ (ก่อน commit) ตรวจไฟล์จริงจากดิสก์ในเวิร์กทรีแยก
(`git worktree add --detach`) — **ระหว่างรอผล ผมรันเทสของตัวเองก่อนแล้วเจอบั๊กเอง**: สองเทส
(`test_exact_balance_affords_every_starting_kit_skill`/`test_one_short_never_affords` ตามที่เขียนไว้ตอนแรก)
ยัด `cost` (float เช่น `1.0` หรือ `0.20000000298023224` ของสกิล 111) เข้าพารามิเตอร์ `current_skill_points`
ที่รับเฉพาะ `int` โดยตรง ⇒ `TypeError` ทุกครั้งก่อนถึงบรรทัดเปรียบเทียบจริง (16/24 subtests แดง) — **แก้ก่อน
adversary ตอบกลับ**: เปลี่ยนไปเทียบกับ `math.ceil(cost)` (ยอด int ที่น้อยที่สุดที่จ่ายพอสำหรับต้นทุนเป็นเศษส่วน
อย่างสกิล 111) แล้วรันซ้ำเขียวทั้ง 8 เทส

ผล adversary (คืนหลังแก้แล้ว) **ยืนยันบั๊กเดียวกันที่พบเอง** (พบไฟล์เทสฉบับก่อนแก้แดง 16/24 ตอนเริ่มอ่าน) +
มิวเทชันจริงกับไฟล์ production ฉบับแก้แล้ว (`>=`→`>`, `>=`→`<=`, การ์ดติดลบ off-by-one, ตัด bool-guard, กลืน
`KeyError` เป็น `False`, ฮาร์ดโค้ด skill 99, `return True` เสมอ) — **ทุกมิวแทนต์ถูกจับ ไม่มีตัวรอด** · ข้อสังเกต
รอง (ไม่ใช่บั๊ก): `skill_id` เองไม่ตรวจชนิด (เหมือน accessor พี่น้องในไฟล์เดียวกัน) · SHA256 pin ของ
`skill_catalog.py` ยังตรง

**ไม่มีอะไรค้างหลังแก้** ⇒ ไม่มี `ADVERSARY_PENDING`

## ชุดเต็ม + preflight

`git fetch origin main` → merge เข้าต้นไม้ (fast-forward `7b164ac`→`68138b0`, PR #798 LANE-DB แทรกเข้ามาระหว่าง
รอบ) → รันชุดเต็มครั้งเดียวติดกับ push บนต้นไม้ที่ merge แล้ว:

```
PYTHONPATH=src python3 -m pytest tests -q
```

ผล: **`10621 passed, 327 skipped, 0 failed` (402.90s)** — เขียว

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS** (cp874 · ไม่มี skip
ใหม่ · main อยู่ใน branch แล้ว)

**ไฟล์เทสใหม่รอบนี้** (`tests/test_skill_learn_validator.py`) ⇒ ซ้อม `pytest_subset` + `skip_census` ใน
`git worktree` แยกที่ไม่มี `pf_bridge` เป็นพี่น้อง: `pytest_subset` **`9669 passed, 93 skipped` exit 0** ·
`skip_census` **"every skip is declared, named and pinned" RESULT: PASS exit 0** — ทั้งสองช่องผ่าน

## งานสำรอง (ทำเมื่องานหลักติด) — ยังไม่ได้ลงมือรอบนี้ งานหลักไม่ติด

1. **[ใบ GT/RE ที่รันได้]** ใบ GT "ยืนยันดาเมจ skill 99 ต่อคลาส บนสนาม Training Iron Man 916" ที่ `jbe8rr`/
   `8p7jon` เสนอค้างสองรอบ — **ยังบล็อกจริงตาม NOW.md จนกว่า P-2 ปิด** (ดูหัวข้อ "อ่าน NOW.md" ข้างบน) ⇒ ถอด
   ออกจากรายการงานสำรองของ CS จนกว่า P-2 ปิด แทนที่ด้วยข้อ 3 ใหม่ด้านล่าง
2. **[โค้ด]** จุดเสียบ `can_afford_to_learn` ให้ LANE-DB จริง (ต้องมีคอลัมน์ `skill_points` ต่อตัวละครก่อน — ยัง
   ไม่มี ตรวจซ้ำรอบหน้า) หรือฟังก์ชันคู่ `skill_points_after_learning` (หักแต้มบริสุทธิ์ ไม่เขียน DB)
3. **[อ่าน/เทียบ — นับได้ไม่เกิน 1 ใน 3 ข้อ]** ทวนสารบัญคิวเริ่มต้นข้อ 1 (อาชีพ/สกิล) ว่ามีคอลัมน์ MP/CD/ระยะ
   ตัวไหนยังไม่มี accessor ชื่อจริง (จาก `skill_catalog.py` ปัจจุบัน: `n_TARGET`/`n_EQUIPTYPE`/
   `n_EQUIPTYPE_LHAND` ยังไม่มีเหตุผล RE ให้ตั้งชื่อ — ตรวจว่ายังจริงอยู่ไหม)

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ NOW/M ขั้นบันได** — `can_afford_to_learn` เป็น zero-production-caller เหมือนโมดูลพี่น้องทุกตัว
(`attack_skill_ids_for_class` ของ `8p7jon` เอง, accessor ทุกตัวใน `skill_catalog.py`) รอ hookup ที่ต้องมีคอลัมน์
`skill_points` ต่อตัวละครจาก LANE-DB ก่อน (ยังไม่มี) แต่เป็นความคืบหน้าจริงของ**คิวเริ่มต้นข้อ 5**
("ระบบเรียนสกิล/skill point") ที่ `0155` สั่งไว้และยังไม่มีใครในสายนี้ลงมือมาก่อนรอบนี้ · ไม่ใช่รอบอ่านอย่าง
เดียว (โค้ด+เทสจริงขึ้น PR) ⇒ ไม่นับ "ไม่ส่งงาน" ตามเกณฑ์ (ก)-(ง) ของ `0156`

## ส่งอะไร

**pirate-force-server**: PR #800 (สาขา `claude/inspiring-albattani-6r13k5`) — เปิดแล้ว ไม่ draft มี marker
ตั้งแต่เปิด (`https://github.com/panyaasanee/pirate-force-server/pull/800`)
- `src/pirateforce_foundation/skill_learn_validator.py` (ใหม่)
- `tests/test_skill_learn_validator.py` (ใหม่, +8 เทส)

**pf_bridge**: PR #1269 (แทน `rounds/CS_6r13k5_claim.md` ด้วยไฟล์นี้)

## nonclaims

- ไม่อ้างว่า `can_afford_to_learn` มี production caller — ยังไม่มี (grep ยืนยันรอบนี้) รอคอลัมน์
  `skill_points` ต่อตัวละครจาก LANE-DB + hookup ที่ chief ต้องอนุมัติ เหมือนโมดูลพี่น้องทุกตัวในไฟล์เดียวกัน
- ไม่อ้างว่าใบ GT "สนาม 916" พร้อมรัน — ยืนยันรอบนี้ว่า **บล็อกจริงตาม NOW.md จนกว่า P-2 ปิด** ไม่ใช่แค่ "ยังไม่
  ได้ลงมือ" เหมือนที่ `8p7jon` บันทึกไว้ก่อนหน้า (แก้ไข nonclaim เดิม)
- ไม่อ้างว่ารองรับต้นทุนหลายแรงค์ (`f_SP_LEVEL2PLUS`) — สกิลทั้ง 8 ตัวในคาตาล็อกมี `n_LEVELS == 1` ทุกตัว
  (`skill_catalog.max_skill_level`) จึงยังไม่มีไอดีให้ตรวจ ขอบเขตเดียวกับที่ `skill_catalog.py` เองยังไม่ตั้งชื่อ
  accessor ให้คอลัมน์นั้น

## ติดอะไร / ใครปลด

- ไม่มีตัวบล็อกใหม่ — งานหลักของรอบนี้ปิดสำเร็จภายในรอบเดียว
- **แจ้ง COO** (จดหมายแนบ): ทิศ "Training Iron Man 916" ของ CS ถูกบล็อกโดย P-2 (เจ้าของ = LANE-GM/LANE-B ไม่ใช่
  CS) — สายนี้จะเดินคิวเริ่มต้นข้อ 1/3/5 ต่อจนกว่า P-2 ปิด แล้วค่อยกลับไปข้อ 2/4

## GATE_UNVERIFIED #800 (`PANYA-DECISION 20260904_1158` §22)

push server PR #800 เวลา ~06:32 +07:00 · gate check-run (`gate`, run `pull_request`) ยัง `in_progress` ต่อเนื่อง
ตรวจซ้ำทุก 30 วิ นาน 13 ครั้ง (≈06:32→06:41 = 9-10 นาที ผ่าน `commits/<sha>/check-runs` ของ GitHub API) ยังไม่
`completed` ⇒ ตาม §22 ไม่รอเกินนี้ ห้ามจบรอบด้วย "waiting on gate — routine" **บันทึกไว้เป็น GATE_UNVERIFIED
แทน**: **รอบถัดไปของ LANE-CS ต้องเปิดด้วยการตรวจผล `pull_request_read get_check_runs` ของ #800 ก่อนงานอื่น** —
เขียว = ปิดข้อนี้ในไฟล์รอบถัดไป · แดง = แก้ในรอบถัดไปทันที (ห้ามถือว่าเป็นรอบใหม่ที่ไม่เกี่ยวข้อง)

-- LANE-CS
