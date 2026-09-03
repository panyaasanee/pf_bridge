# CS round iazmrv — class registry + starting-skill-kit catalog

เวลาเริ่ม 2026-09-04 03:54 +07:00 · เวลาปิด 2026-09-04 04:53 +07:00 · claim `pf_bridge#1054`

## ขยับ NOW/M ข้อไหน

- คิวเริ่มต้นของ LANE-CS ข้อ 1 ("สารบัญอาชีพและสกิลจากตารางจริง") — **ขยับบางส่วน**: ส่งสารบัญ 5
  อาชีพหลักที่เลือกได้จริง (`CHARCREATE_CLASS`) และสารบัญสกิลชุดเริ่มต้น (starting kit) 8 ตัวที่ทั้ง 5
  อาชีพอ้างถึง (`SKILL_CONTEXT` + `SKILL_TEXT`) — **ไม่ใช่** "สกิลทุกตัวต่ออาชีพ" ตามที่คิวเดิมเขียนไว้
  เต็มรูปแบบ เหตุผลอยู่ในหัวข้อ nonclaims ข้างล่าง (พบจริงระหว่างรอบ ไม่ใช่ทราบล่วงหน้า)
- ไม่ขยับ M2/M3/M4/M5 (ไม่ใช่เขตของสายนี้)

## ส่งอะไร

- **pirate-force-server** branch `claude/inspiring-albattani-o1t4t6` @ `f02fbc3` (merge main `2315364`
  แล้วรันชุดเต็มซ้ำ, ไม่มีคอนฟลิกต์) — ไฟล์ใหม่:
  - `src/pirateforce_foundation/class_catalog.py` — 5 อาชีพ (`CLASS_ID_TO_NAME`,
    `CLASS_ID_TO_STARTING_SKILL_IDS`) จาก `data/charcreate_class.tsv` (สำเนาไบต์ต่อไบต์ของ
    `CONSTDATA_TH__CHARCREATE_CLASS.tsv`)
  - `src/pirateforce_foundation/skill_catalog.py` — สกิลชุดเริ่มต้น 8 ตัว (99/110/111 ร่วมทุกอาชีพ +
    ตัว "Basic Training" เฉพาะอาชีพ) จาก `data/skill_context_starting_kit.tsv` +
    `data/skill_text_starting_kit.tsv`
  - `tools/pf_class_skill_starting_kit_extract.py` — ตัวสร้าง/ตัวเช็ค (`--check`) ทั้งสามไฟล์ tsv ข้างต้น
    จาก `../pf_bridge/gamedata` ตรง — เปิดตัวเองเข้า `.gitignore` allowlist ด้วย (บรรทัดใหม่)
  - `tests/test_class_catalog.py`, `tests/test_skill_catalog.py` — 24 เทส/31 subtest, สอง
    เทสในนั้นการ์ดด้วย `BRIDGE_GAMEDATA.skip_unless_present()` รัน `--check` จริงกับ `../pf_bridge`
    สด (ไม่ใช่แค่ self-hash) — ปักไว้ `docs/PYTEST_SKIP_PINS.json` ใต้ `preconditions` แล้ว
  - ทั้งหมด **sha256-pinned** กับสำเนาที่คอมมิต + คอมโพสจริงกับ `../pf_bridge/gamedata` ตรงในรอบนี้
    (ไม่ใช่ค่าที่พิมพ์มือ)
- **pf_bridge**: PR `#1054` (claim → final รอบนี้), จดหมายถึง COO ไฟล์เดียวกับรอบนี้ (`≤12,000` อักขระ,
  วัดจริงก่อนส่ง)

## หลักฐานที่วัดจริงรอบนี้ (ไม่ใช่เดา)

- `python3 tools/pf_class_skill_starting_kit_extract.py --gamedata ../pf_bridge/gamedata --check` →
  `CHECK OK` (รันจริงกับ pf_bridge สดในเซสชันนี้)
- ชุดเต็ม `pytest tests -q -rs` บนต้นไม้ที่ merge `origin/main` แล้ว: **9267 passed, 327 skipped, 17807
  subtests passed**, 0 failed (`git fetch origin main` ก่อนแล้ว merge เข้ากิ่งตามกฎ)
- ซ้อมเกตแบบ "ไม่มี `pf_bridge` ข้าง ๆ" ใน `git worktree --detach` แยกโฟลเดอร์: `pytest_subset` exit 0
  (8326 passed, 87 skipped — สองเทสใหม่ของรอบนี้ skip แบบ declared ตาม `bridge_gamedata`) ·
  `skip_census` exit 0 `RESULT: PASS` (ปักลง `docs/PYTEST_SKIP_PINS.json` ในคอมมิตเดียวกันแล้ว)
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` → `PREFLIGHT PASS`
- `pf-adversary` (สั่งต้นรอบ) จับได้ว่าคำว่า "quest" ในดอกสตริงของร่างแรก `skill_catalog.py` ชน
  containment test ของเลนอื่น (`tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests`) —
  แก้คำ (ไม่แตะไฟล์เทสของเลนอื่น) แล้วรันชุดเต็มซ้ำจนเขียว — รายละเอียดเต็มอยู่หัวข้อ adversary ข้างล่าง

## pf-adversary

**ไม่ pending** — สั่งต้นรอบ (ก่อนเริ่มเขียนโค้ด, ตามกฎ `20260903_2345`) ผลคืนแล้วก่อน push:

1. อ่านตารางจริงก่อนเขียนโค้ดตามผล `pf-static-re` (สั่งพร้อมกัน) — จับได้ 5 จุดสำคัญ ทุกจุดสะท้อนในโค้ด/
   ดอกสตริง/nonclaims ของรอบนี้แล้ว: (ก) อ่าน `gamedata` ตรงจาก `pf_bridge` ที่ runtime = ห้าม → แก้เป็น
   สำเนาไบต์ต่อไบต์ + ตัวสร้างแยก แบบเดียวกับ `gm/scene_catalog.py`/`gm/item_catalog.py` (ข)
   self-hash เดี่ยวจับได้แค่แก้มือ ไม่จับตารางต้นทางเปลี่ยน → เพิ่มเทสการ์ด `BRIDGE_GAMEDATA` ที่รัน
   `--check` จริง แบบเดียวกับ `tools/pf_mine_scene_drop_tables.py`/`test_mob_loot.py` (ค) มีหลายตาราง
   สกิล (SAILOR_SKILL คนละโดเมน, CURRICULUM คนละรหัสอาชีพ, เควสสคริปต์ให้สกิลนอกตาราง) → ตัดขอบเขต
   เหลือ "สกิลชุดเริ่มต้น 8 ตัว" เท่านั้น ไม่อ้าง "ทุกสกิล" (ง) ไม่มีคอลัมน์ type/MP ในตาราง → ไม่ประดิษฐ์
   ฟิลด์ type ใหม่ ให้ค่าดิบตามชื่อคอลัมน์จริง (จ) `s_SCORE`/`STANDARD_STATUS` เป็นเขตของ LANE-DB
   (`COO-ORDER 0329` ข้อ 2 ที่กำลังทำพร้อมกันรอบนี้เป๊ะ) → ไม่แตะเลย
2. คำว่า "quest" ในดอกสตริง `skill_catalog.py` ชน containment test ของเลนอื่นจริง (จับได้จากการรันชุดเต็ม
   ไม่ใช่จาก adversary โดยตรง แต่เป็นสิ่งที่ adversary เตือนเรื่อง "evidence-layer laundering"
   ทางอ้อม) — แก้คำแล้ว ไม่แตะไฟล์เทสของเลนอื่น (`tools/pf_class_skill_starting_kit_extract.py`
   ยังพูดคำว่า "quest" ได้เพราะการ์ดนั้นสแกนแค่ `src/pirateforce_foundation/*.py` ไม่รวม `tools/`)

## nonclaims (grep กำกับตามกฎ)

- **ไม่ใช่ "สกิลทุกตัวต่ออาชีพ"** อย่างที่คิวเดิมเขียน — ไม่มีตารางที่คอมมิตไว้ตารางเดียวตอบคำถามนั้นได้:
  `grep -c "" gamedata/tables/CONSTDATA_TH__SKILL_CONTEXT.tsv` = 2166 บรรทัด (2165 แถว) แต่
  `n_ISCLASS` เป็น bitmask ที่ self-referential เฉพาะ 6 แถว "Basic Training" เอง (แถว 40000 มี
  `n_ISCLASS=1` ตรงกับบิตของตัวเอง ไม่ใช่ foreign key ทั่วไป) · `CONSTDATA_TH__SAILOR_SKILL.tsv`
  ใช้ id ช่วงเดียวกันแต่เป็นสกิลเรือ คนละโดเมน · `CONSTDATA_TH__CURRICULUM.tsv` ใช้รหัสอาชีพคนละตัว
  (`n_PPCLASS`) · เควสสคริปต์ให้สกิลนอกตารางทั้งหมด — ทั้งสี่จุดนี้ pf-static-re วัดจริงจากไฟล์ที่คอมมิต
  แล้ว ไม่ใช่เดา
- **ไม่แตะค่าสถานะ/ความสามารถ** (STR/CON/AGI/INT/PER, HP/MP): `s_SCORE` (คอลัมน์ใน
  `CHARCREATE_CLASS` เอง) ไม่เคยถูก RE ความหมายในโปรเจกต์นี้ (`grep -c "s_SCORE"
  reports/PF_JOB001_CHARCREATE_CLASS_STATIC_BOUNDARY_20260816.md` = นับรวมอยู่ใน "37 other columns"
  เท่านั้น ไม่มีการถอดรหัส) · `CONSTDATA_TH__STANDARD_STATUS.tsv` เป็นเขต LANE-DB ตาม
  `COO-ORDER 20260904_0329` ข้อ 2 (เส้นตาย 08:31 รอบเดียวกับรอบนี้) · `CONSTDATA_TH__POTENTIAL.tsv`
  มีแค่ header ไม่มีแถวข้อมูลจริง (`wc -l gamedata/tables/CONSTDATA_TH__POTENTIAL.tsv` = 1 บรรทัด)
- **ไม่มีอาชีพที่ 6**: `CONSTDATA_TH__CHARCREATE_CLASS.tsv` มี 5 แถวข้อมูลเท่านั้น (`n_ID`
  1/2/4/16/32) — สกิล `45000` (ไอคอน `ICON_Class_Voodooist_s`) เป็นเบาะแสสำหรับ RE รอบถัดไป ไม่ใช่
  อาชีพที่เลือกได้ตอนสร้างตัวละครในข้อมูลชุดนี้
- **ไม่ใช่การเปลี่ยนชื่อ `FACTPACK_L2_CLASSCENSUS001`** ของ pf_bridge (สำมะโน RTTI C++ engine
  ~1327 คลาส) — คนละความหมายของคำว่า "class" กันคนละเรื่อง
- ไม่มี basic/attack/AOE/buff/heal/passive ในโค้ดรอบนี้ — ตาราง `SKILL_CONTEXT` ไม่มีคอลัมน์ enum
  แบบนั้น (`grep -c "n_PASSIVE\b"` เจอคอลัมน์เดียวคือ raw flag ค่าที่พบ = 1 หรือ 2 ไม่ใช่ 0/1) การจัด
  หมวดต้องถอด `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` (mini-language เช่น `GO(0)`, `CHASE(n)`) ก่อน —
  ยังไม่ทำรอบนี้
- ยังไม่แตะสูตรดาเมจ (`damage_model_hypothesis.py` ฯลฯ) และยังไม่ทำ Basic attack กับ Training Iron
  Man จริงบนจอ — คิวข้อ 2/3 ของ LANE-CS ยังไม่เริ่ม

## ติดอะไร / ใครปลด

ไม่มีจุดติดของสายนี้ในรอบนี้ ไม่มี CORE-REQUEST ใหม่ (ยังไม่แตะ `runtime.py`/`app.py`)
