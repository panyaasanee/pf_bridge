# DB round (`64da3x`) -- 2026-09-05T17:39+07:00 -> 2026-09-05T19:05+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

อ่าน `NOW.md` ล่าสุดก่อนอื่น (ตรวจล่าสุด 16:52 โดย COO). **รอบนี้ไม่ขยับข้อไหนใน NOW.md
โดยตรง** -- งานหลักของรอบนี้ (สอง store door ของ `skill_points`) เป็นคิวปกติของ
`COO-ORDER 20260904_0329` (piece 5 ต่อเนื่อง) ที่มาทาง CORE-REQUEST ของ LANE-CS
(`20260905_1510`) ไม่ใช่หัวข้อที่ NOW.md ระบุชื่อไว้ตรง ๆ -- `1101` (M4 หลัก, HP/เลเวล
ที่ `runtime.py:6443`) **ไม่ขยับ**: ยังล็อกรอ LANE-B รายงาน "Door B พร้อม flip"
ตาม `COO-DECISION 20260905_1044` ข้อ 1 เหมือนเดิม รอบนี้ไม่แตะเรื่องนั้น (ไม่ใช่ของ DB
จนกว่า LANE-B ส่งสัญญาณ)

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended)

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยวข้อง -- รอบนี้ไม่แตะโลก/ฉากเลย เป็นคอลัมน์ของตัวละคร
(`characters.skill_points`) ที่มีอยู่แล้วตั้งแต่ migration 006 -- ตรงกับ `COO-DECISION
20260905_1154` ข้อ 1 ("ของพื้น/ศพ/เลือดมอน/ตำแหน่งมอน = A/B, DB ไม่แตะ" -- เรื่องนี้ไม่ใช่
สถานะโลก เป็นสถานะของตัวละครเจ้าของบัญชี)

## 1. ล็อกรอบ

- ต้นรอบ list `[LANE-DB]` open ทั้งสองรีโป (ก่อนอ่านกล่องจดหมาย/แตะโค้ด): **ว่างเปล่าทั้งคู่**
- ตัดกิ่งจาก `origin/main` สดของทั้งสองรีโป: `pf_bridge` = `claude/admiring-johnson-64da3x`
  (จาก `ed28d4fa`), `pirate-force-server` = `claude/brave-goodall-64da3x` (จาก `e5d3b119`,
  ไม่มี commit ใหม่ระหว่างรอฟีเจอร์นี้)
- commit `rounds/DB_20260905_1739_64da3x_claim.md` (สามบรรทัด) push แล้วเปิด
  `pf_bridge#1353 [LANE-DB] round 64da3x: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1353` ของผมเอง ⇒
  ไม่แพ้ ทำงานต่อ

## 2. กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-DB" notes_to_chief/*.md` แล้วกรองที่ยังไม่มี `.CONSUMED.txt` คู่:
สามใบ

1. `20260905_1510_LANE-CS-CORE-REQUEST-store-py-skill-points-hookup-to-lane-db-rerouted-from-chief.md`
   -- CORE-REQUEST ขอ `get_skill_points`/`spend_skill_points` ใน `store.py` (งานหลักของรอบนี้ --
   ดู §3.1)
2. `20260905_1610_LANE-B-CORRECTION-1353-was-founded-on-a-false-claim-db-built-it-anyway.md`
   -- LANE-B แก้ไขข้ออ้างเท็จของตัวเองเรื่องใบ `1353` (คนละใบเลขซ้ำกับ claim PR ของรอบนี้โดยบังเอิญ
   -- นี่คือจดหมาย ไม่ใช่ PR) -- ยกให้ COO ตัดสินไปแล้ว
3. `20260905_1651_COO-DECISION-b1610-keep-read-class-id-by-identity-lost-round-counted-to-b-db-class-id-item-closed-LANE-DB.md`
   -- COO ตัดสินเก็บ `read_class_id_by_identity` ไว้ · **"LANE-DB: ไม่มีงานจากใบนี้"** ตามที่
   ใบเขียนตรง ๆ · consume ด้วย stub เฉย ๆ ไม่มีอะไรต้องทำ

อ่านสามใบก่อตั้งสาย (`20260901_1059`/`1100`/`1101`/`1112`) ครบตามกติกา "รอบแรกของเซสชัน"
(เซสชันนี้ไม่มีความจำข้ามรอบ)

อ่านไฟล์รอบล่าสุด `DB_20260905_1606_rdpgoz_home_marker_value_reply_and_class_id_pr_verify.md`
-- ข้อ 7 ชี้ไปที่: รอคำตอบเรื่องตัวอ่าน home-marker ตัวที่สอง (ยังไม่มีคำตอบ ณ ตอนอ่านกล่องจดหมาย
รอบนี้ -- ไม่ใช่ 2 รอบ/3 ชม.ยัง) และกลับไปคิว `COO-ORDER 0329` ชิ้น 3/4/5 ถ้าไม่มีใบใหม่ -- **มีใบใหม่**
(`1510`) เลยไม่ต้องกลับไปคิวเดิม

## 3. ทำอะไร

### 3.1 CORE-REQUEST `1510` -- `get_skill_points`/`spend_skill_points` ใน `store.py`

ตรวจก่อนเขียนโค้ด (ไม่เดา):

- `'skill_points' in persistence_typed_attrs.TYPED_COLUMNS` ยืนยันจริง (`True`, x=16, u32,
  0..4294967295) -- ตรงกับที่ chief ตรวจไว้ในใบ `1406` ที่ CS แนบมา
- `migrations/006_character_typed_attribute_columns.sql:144-145` มีคอลัมน์จริง;
  `migrations/009_character_birth_defaults.sql` **ไม่ให้ default** สี่คอลัมน์เดียวที่ได้ default
  คือ `level`/`hp_current`/`hp_max`/`speed_walk` -- `skill_points` ยังเป็น NULL ที่เกิดเสมอ
  จนกว่าจะมีคนเขียน
- `grep -rn "get_skill_points\|spend_skill_points"` ทั้งรีโปก่อนเขียน = 0 hit (ยืนยันซ้ำตามที่
  chief วัดไว้ในใบ `1406`)

สร้างใน `src/pirateforce_foundation/store.py` (เมธอดใหม่ทั้งคู่ ไม่แตะเมธอดเดิม
-- charter `COO-DECISION 20260901_1100`):

- `get_skill_points(character_id) -> int | None` -- wrapper บาง ๆ บน `read_typed_attributes`
  ที่มีอยู่แล้ว คืน `None` (ไม่ใช่ `0`) เมื่อคอลัมน์ยัง NULL -- กติกา "ห้ามเดาศูนย์"
  (`COO-DECISION 20260901_1059`) เพราะ `0` เป็นค่าที่การหักจริงก็ทิ้งไว้ได้เหมือนกัน
  ใช้แทนกันไม่ได้กับ "ยังไม่มีใครวัด"
- `spend_skill_points(character_id, cost) -> int` -- ธุรกรรมเดียว (`BEGIN IMMEDIATE` +
  `vitals.verify_schema` guard เดียวกับทุกเมธอดเขียน typed attribute ในไฟล์นี้):
  อ่านยอด -> NULL ปฏิเสธด้วย `UnmeasuredSkillPointsError` ใหม่ (ไม่เดาว่าเป็น 0 หรือไม่จำกัด)
  -> ยอดไม่พอปฏิเสธด้วย `InsufficientSkillPointsError` ใหม่ (ไม่หักบางส่วน) -> UPDATE
  แล้วอ่านกลับในธุรกรรมเดียวกัน (แบบเดียวกับ `write_typed_attribute_if_unset`) คืนยอดหลังหัก
- สองข้อยกเว้นใหม่ (`InsufficientSkillPointsError`, `UnmeasuredSkillPointsError`) ประกาศเป็น
  `RuntimeError` ระดับโมดูล ต่อจาก `WriteLockTimeout` ตามรูปแบบเดิมของไฟล์
- `cost` ต้องเป็นค่าที่ปัดเศษแล้วจากฝั่งผู้เรียก (ตามข้อเสนอของ `1510` -- `store.py` ไม่รู้จัก
  `skill_catalog`/ต้นทุนเศษ) -- validate เป็น `int` ไม่ใช่ `bool`, ไม่ติดลบ, ก่อน SQL ใด ๆ รัน
  เหมือนทุกเมธอดเขียนอื่นในไฟล์

จดหมายตอบ: `20260905_1739_LANE-DB-REPLY-skill-points-store-doors-built-get-and-spend.md`
(ADDRESSEE: LANE-CS, cc COO/chief) -- แก้เนื้อหาอีกครั้งหลัง §3.3 ก่อน push

### 3.2 กล่องจดหมายอีกสองใบ (`1610`, `1651`)

ทั้งคู่เป็นข้อมูล ไม่มีงานให้ DB ทำ -- `1651` เขียนตรงว่า "LANE-DB: ไม่มีงานจากใบนี้ ·
กลับคิว DB ตาม NOW" ซึ่งตรงกับที่รอบนี้ทำอยู่แล้ว (§3.1) -- consume ด้วย stub เฉย ๆ

### 3.3 pf-adversary + ผลชุดเต็มครั้งแรก -- สามข้อที่ต้องแก้ก่อน push

เรียก `pf-adversary` ต้นรอบพร้อม §3.1 (ตามกติกา -- ไม่ใช่ก่อน commit) ผลคืนพร้อมสองข้อจริง วัดสด
ไม่ใช่แค่อ่านโค้ด:

1. **`sqlite3.OperationalError('database is locked')` ดิบหลุดจาก `spend_skill_points` ได้จริง
   ภายใต้ contention** -- pf-adversary ยึดล็อกเขียนจากคอนเนกชันที่สองค้างไว้ 6 วิ (จำลองตัวเขียนอื่น
   ที่ช้า เช่น `write_typed_attributes`) แล้วเรียก `spend_skill_points` พร้อมกัน ได้ error ดิบหลุดจริง
   หลัง 5.0 วิ (`connect()`'s `busy_timeout=5000`) -- docstring ของเมธอดสัญญารายการ exception ไว้ครบ
   (`TypeError`/`ValueError`/`KeyError`/`UnmeasuredSkillPointsError`/`InsufficientSkillPointsError`)
   แต่ไม่มีตัวนี้ -- ตรงกับเหตุผลที่ `WriteLockTimeout` ถูกสร้างไว้แล้วในไฟล์นี้ตั้งแต่
   `COO-DECISION 20260903_1248` (สำหรับ `apply_hp_damage`/heal) หนี้เดิมที่ใช้ pattern เดียวกัน
   (`write_typed_attributes`, `write_typed_attribute_if_unset`) มีช่องเดียวกันด้วย แต่ไม่ใช่ของรอบนี้
   จะไปแก้ (charter ห้ามเปลี่ยน behavior เมธอดเดิม) -- แก้เฉพาะเมธอดใหม่ของรอบนี้: ครอบ
   `db.execute("BEGIN IMMEDIATE")` แปลง `database is locked` เป็น `WriteLockTimeout` (ใช้ของเดิม
   ไม่สร้างกลไก retry/budget ใหม่ -- ไม่ต้องมี COO ตัดสินชื่อ token ใหม่)
2. **`character_id`/`cost` เกินช่วง SQLite `INTEGER` (signed 64-bit) ทำ `OverflowError` ดิบหลุด
   แทนที่จะเป็น `KeyError`/`ValueError`** -- pf-adversary วัดสดด้วย `2**63` ⇒ เพิ่ม
   `_fits_sqlite_integer` (helper ใหม่ระดับโมดูล) เช็คก่อน SQL ใด ๆ รันทั้งสองเมธอด: `character_id`
   เกินช่วง = `KeyError` (id ขนาดนี้ไม่มีทางเป็นแถวจริง), `cost` เกินช่วง = `ValueError`
   (`read_typed_attributes` เองก็มีช่องเดียวกัน เป็นหนี้เดิม ไม่แตะเพราะไม่ใช่เมธอดของรอบนี้)
3. **ชุดเต็มครั้งแรก (§4) เจอ 2 เทสแดงจริง ที่ pf-adversary ไม่เจอ** (ไม่ใช่เพราะ pf-adversary
   พลาด -- เป็นเทสที่รันเฉพาะตอนชุดเต็มสแกนทั้งรีโป ไม่ใช่ unit test ของโมดูลเดียว):
   `tests/test_persistence_speed_walk_seed_008.py::NothingSendsItTests` สอง testcase สแกนทั้งไฟล์
   `store.py` หา method reader ทั่วไป (`read_typed_attributes`) ปนกับ attribute encoder
   (`compose_sparse_block`, มีอยู่แล้วจาก `/speed`) ในไฟล์เดียวกัน -- `get_skill_points` เดิมเรียก
   `self.read_typed_attributes(...)` เข้าเงื่อนไขพอดี ทั้งที่ไม่เกี่ยวกับ `speed_walk` เลย
   (`COO-DECISION 20260902_0742` ข้อ 4 ห้ามไฟล์ที่อ่านได้ทุกคอลัมน์ + เข้ารหัสบล็อกได้ในไฟล์เดียวกัน
   -- ป้องกันการรีแฟคเตอร์ที่ส่ง `speed_walk` แบบไม่มีใครอนุมัติ) **ไม่แก้ด้วยการอ่อนเทสนั้น** (เทสมีไว้
   ป้องกันความเสี่ยงจริงในไฟล์นี้) -- แก้ที่ `get_skill_points` แทน: เขียน query แคบของตัวเองอ่านแค่
   `skill_points` (ไม่เรียก `read_typed_attributes` เลย) พร้อม guard `PRAGMA table_info` มือ
   (แบบเดียวกับ `list_character_ids_missing_class_id`) แคบกว่าเดิมจริง ไม่ใช่แค่หลบเทส -- แก้
   docstring ด้วย (คำอธิบายเดิมมีคำว่า "speed_walk" ปนกับ "select"/"from" จนชนเทสฝั่ง raw-SQL-string
   scan ของไฟล์เดียวกันซ้ำ -- เขียนใหม่หลีกเลี่ยงคำตรงตัวโดยไม่เปลี่ยนความหมาย)

ทั้งสามข้อแก้ก่อน push (สองข้อแรกจาก pf-adversary, ข้อสามจากชุดเต็มครั้งแรก) เพิ่มเทสให้ครบ
(22 เทสรวม ดู §4) แล้วรันชุดเต็มซ้ำ (ครั้งที่สอง -- เหตุผลที่ต้องรันเกินหนึ่งครั้ง: พบเทสแดงจริงจาก
ชุดเต็มครั้งแรกที่ต้องแก้ก่อน push ตามกติกา "ห้าม push สภาพที่ไม่เคยถูกรันเต็ม") เขียวหมด (§4)

## 4. ชุดเทสของรอบ

ระหว่างทำงาน (เฉพาะไฟล์ที่เกี่ยว): `pytest tests/test_store_skill_points.py
tests/test_persistence_typed_attr_columns.py tests/test_persistence_character_skills_011.py
tests/test_class_id_login_wiring.py tests/test_skill_learn_validator.py
tests/test_persistence_vitals.py tests/test_persistence_vitals_heal.py` -- 18 เทสใหม่ผ่าน
(ภายหลังเป็น 22 -- ดู §3.3) + 391 เทสเดิม (483 subtests) ผ่านหมด ไม่มีแดง

pf-adversary สั่งต้นรอบพร้อมเริ่มงาน ผลคืนก่อน push (ดู §3.3) -- ไม่ใช่ `ADVERSARY_PENDING`

**ชุดเต็ม (`pytest tests/`) รันครั้งเดียวจริง** บนต้นไม้ที่ `git fetch origin main` +
`git merge origin/main` สดที่สุดแล้ว (`46d7f59f`, หลัง PR #837/#838 ของสายอื่น merge เข้ามา
ระหว่างรอบ) เป็น **commit สุดท้ายจริง** ก่อน push (`215f3be1` ต่อจาก `4a55e2f0`, หลังแก้ผล §3.3
เรียบร้อย): **11115 passed, 323 skipped, 20904 subtests passed, 0 failed** (571.58s แรกเจอแดง
2 ตัวจาก §3.3, 572.85s รอบสุดท้ายเขียวหมด) -- ไม่มีการแก้อะไรหลังชุดเต็มรอบสุดท้ายผ่าน ก่อน push

BYTECODE_PURGED: `find . -name "*.pyc" -type f -delete` (ลบทีละไฟล์ ไม่ใช้ `-r`/`rm -rf` ตาม
กติกาใหม่ `PANYA-DECISION 20260905_1546`) ก่อนชุดเต็มทั้งสองครั้ง + `python3 -B` /
`PYTHONDONTWRITEBYTECODE=1` ทุกคำสั่ง pytest ตลอดรอบ

KNOWN_RED_MAIN: ไม่มี -- `test_combat_pose` SourcePin (LANE-B `#835`, เคยรู้ว่าแดงจากรอบก่อน)
ผ่านแล้วในชุดเต็มของรอบนี้ (แก้ไปแล้วก่อนรอบนี้เริ่ม เห็นได้จาก 0 failed)

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable

**ศูนย์** -- สองเมธอดใหม่นี้ zero production caller ทั้งคู่ (เหมือนที่ใบ `1510` บอกไว้ตรง ๆ)
ไม่มี call site ใน `runtime.py`/`session.py` ที่เรียกใช้ ผู้เล่นยังกด "เรียนสกิล" ไม่ได้จากงาน
รอบนี้ -- endpoint ยังไม่มีเจ้าของ (ตามที่ `1510` ระบุว่าจะเป็น CORE-REQUEST แยกเมื่อถึงเวลา)

### 5.2 wire-DB

**สองเมธอดใหม่ทำงานถูกตามที่เทสวัด** (ดู §4): บันทึก/อ่านยอดจริงในตาราง `characters`
คอลัมน์ `skill_points` ที่มีอยู่แล้ว, อ่านกลับหลังเขียนในธุรกรรมเดียวกัน, ปฏิเสธ NULL/ยอดไม่พอ
โดยไม่เขียนอะไรเลย (วัดจาก `get_skill_points` หลัง exception ยังคงค่าก่อนหน้า), แปลง lock-timeout
และ out-of-range เป็น exception ที่ตั้งชื่อไว้แล้ว (จำลองสด ไม่ใช่แค่อ่านโค้ด -- §3.3) -- PR
`pirate-force-server#840` เปิดแล้ว มี `PF-AUTOMERGE: v4` รอ gate

## 6. nonclaims

1. **ไม่อ้างว่ามี caller จริงในเซสชันผู้เล่น** -- zero production caller ทั้งสองฝั่งเหมือนเดิม
   ตามที่ใบ `1510` บอกไว้เอง
2. **ไม่อ้างว่า `1101` (M4 หลัก, HP/เลเวล) ขยับ** -- ยังล็อกรอ LANE-B รายงาน Door B พร้อม flip
   ตาม `COO-DECISION 20260905_1044` เหมือนเดิม รอบนี้ไม่แตะ
3. **ไม่อ้างว่า `COO-ORDER 0329` piece 3 (`0x309A` full block) ปิด** -- ยังบล็อกด้วยเหตุผลเดิม
   (RE-259/RE-260 เป็น bounded negative ไม่ปลดล็อก, x=26/27 ยังพิสูจน์ owner ไม่ได้) รอบนี้ไม่แตะ
4. **ไม่อ้างว่า home-marker reader gap (ใบ `1606`) ปิดแล้ว** -- ยังไม่มีคำตอบจาก chief/COO ว่าเลือก
   ทาง (ก)/(ข) รอบนี้ตรวจกล่องจดหมายแล้วไม่มีใบใหม่เรื่องนี้ ยังไม่ถึงเกณฑ์ 2 รอบ/3 ชม. ที่จะยกระดับ
5. **ไม่อ้างว่า PR นี้ขึ้น `main` แล้ว** -- ณ ตอน push สถานะคือ "เปิดแล้ว รอ gate" เท่านั้น
6. **ไม่แตะไฟล์ใดนอกเขต** -- `src/pirateforce_foundation/store.py` (เมธอดใหม่) +
   `tests/test_store_skill_points.py` (ไฟล์เทสใหม่) เท่านั้นในฝั่ง `pirate-force-server`
7. **ไม่อ้างว่าหนี้ lock-timeout/out-of-range เดิมใน `write_typed_attributes`/
   `write_typed_attribute_if_unset`/`read_typed_attributes` ถูกแก้ด้วยรอบนี้** -- pf-adversary
   ระบุตรงว่าทั้งสามมีช่องเดียวกัน (มาก่อนรอบนี้) แต่ charter ห้ามเปลี่ยน behavior เมธอดเดิม แก้ได้
   เฉพาะเมธอดใหม่ของรอบนี้เอง -- ยังไม่มีใบถาม COO ว่าควรแก้หนี้เดิมด้วยรอบแยกหรือไม่ (ดูคำถามท้าย
   ผล pf-adversary -- เสนอเป็นใบถ้ารอบหน้ายังไม่มีใครหยิบ)

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจ gate ของ PR `pirate-force-server` รอบนี้ (`GATE_UNVERIFIED` ถ้ายังไม่ทราบผลตอนจบรอบ)
3. ตรวจว่า chief/COO เลือกทาง (ก)/(ข) ของตัวอ่าน home-marker ที่สอง (ใบ `1606`) หรือยัง
4. ตรวจว่า LANE-CS ส่ง CORE-REQUEST ใบใหม่สำหรับ endpoint "เรียนสกิล" หรือยัง (ไม่บล็อกใคร)
5. ถ้าไม่มีใบใหม่: กลับไปหา `COO-ORDER 0329` piece 3/4 ที่ยังไม่ปิด ตรวจสถานะจริงก่อนอ้างว่ายังเปิด
6. มาร์กกล่องจดหมายด้วย unanchored grep เสมอทั้งสองแบบ (`ADDRESSEE:` หัวไฟล์ และจ่าหน้าในบรรทัดแรก
   ของเนื้อหาแบบ sync-notice)
7. คำถามเปิดจาก pf-adversary รอบนี้ (nonclaims ข้อ 7): ควรให้ทุกเมธอดที่ `BEGIN IMMEDIATE` ใน
   `store.py` (ไม่ใช่แค่ heal/damage) ผ่าน `WriteLockTimeout` เสมอไหม หรือ skill-point spend
   ถือว่า contention ต่ำพอไม่ต้องมี -- ยังไม่มีคำตอบ พิจารณาเขียนใบถึง COO ถ้ารอบหน้ายังไม่มีใครหยิบ

## งานสำรอง (ถ้างานหลักติดเครื่องรอบหน้า)

1. RE ticket แคบสำหรับ VA ที่เหลือของ piece 3 (`x=26`/`x=27` owner ยังพิสูจน์ไม่ได้) --
   เริ่มได้ทันที แต่เป็น audit/RE ไม่ใช่ diff+เทส (นับได้ไม่เกิน 1 ใน 3 ตามกติกา `0155`)
2. ขยาย `typed_column_null_audit` ให้รายงาน `skill_points`/`unspent_points` แยกกลุ่ม
   (คอลัมน์ที่มี CORE-REQUEST เขียนใช้แล้ว vs ยังไม่มีใครแตะ) -- เริ่มได้ทันที เป็น diff+เทส
3. ตรวจ `write_typed_attribute_if_unset` over-refusal (`COO-DECISION 20260905_0745` ข้อ 3
   -- ปิดถาวรแล้วครั้งก่อน แต่ call-site ใหม่วันหลังนับเป็นใบใหม่ได้ถ้าพบจริง) -- grep call site
   ใหม่ก่อนตัดสินว่ามีอะไรให้ทำ
