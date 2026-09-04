# DB round (`1cajqi`) -- 2026-09-04T10:03+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260904_0840_b0ede7_class_id_backfill_hookup_and_piece3_scope_ask.md`
รอบนั้นปิด `class_id` backfill list method (`pirate-force-server#718`, merge แล้ว) และส่งจดหมายถาม COO
ว่า `0745` ข้อ 4 ("DEFAULT 100 ก็ได้") หมายถึงคอลัมน์ที่มี DEFAULT อยู่แล้วเท่านั้นหรือสั่งให้เขียน
migration ใหม่ -- `COO-DECISION 20260904_0942` ตอบมาก่อนต้นรอบนี้: (ก) DEFAULT ที่มีอยู่แล้วเท่านั้น
(`1607` ยืน) ห้าม migration และวางขอบเขตชิ้น 3 ใหม่ชัดเจน: "ชุด mask ล็อกอิน (b'') ตัดกับแถวที่มีค่าจริง"
รายงานเป็นรายชื่อในไฟล์รอบ ไม่ใช่เติมศูนย์

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ** -- ไม่มีสิทธิ์แก้ไฟล์นั้นเอง อ่านฉบับสดต้นรอบ (ตรวจล่าสุด COO 09:45) ทั้ง "งานด่วนตอนนี้"
และ "บันไดไมล์สโตน" บรรทัด PLAYER/CHARACTER ข้อ (3) ("บล็อก `0x309A` เต็มจากแถว typed = แหล่งค่าของ DB")
เป็นข้อที่ COO ตัดสินไว้แล้วในใบ `0745`/`0942` ไม่ใช่บรรทัดที่รอบนี้ทำให้ล้าสมัย

## 1. ล็อกรอบ

- 10:03+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่มีใครต้องปลดล็อก ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`1378a131`) commit `rounds/DB_20260904_1003_1cajqi_claim.md`
  push แล้วเปิด `pf_bridge#1104 [LANE-DB] round 1cajqi: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1104` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- ก่อนเปิด PR ฝั่งเซิร์ฟเวอร์: `git fetch origin main` (ขยับจาก `b3d3fd9c` เป็น `531dc9d0` ระหว่างรอบ
  -- `#722` ของ LANE-E/LANE-B ไม่แตะไฟล์ในเขตเขียนของ LANE-DB เลย, `git log --stat` ตรวจแล้ว) fast-forward
  merge เข้ากิ่งของตัวเอง แล้วรัน targeted tests ซ้ำ (เขียว) ก่อนรันชุดเต็ม
- ก่อนสร้างไฟล์ migration ใหม่: **ไม่มี** -- รอบนี้ไม่แตะ `migrations/` เลย (ตาม `0942` ข้อ 2 ห้าม migration)
  จึงไม่มีเลขให้ชน ไม่ต้องเช็ค
- ก่อนเปิด PR: `git fetch origin main` ซ้ำ -- ยังอยู่ที่ `531dc9d0` ไม่ขยับ ⇒ push ตรง เปิด PR
  `pirate-force-server#723` มี `PF-AUTOMERGE: v4` ในตัว
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pirate-force-server` มีใบเดียวคือ `#723` ของผมเอง ⇒ ไม่ชนใคร

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สดของ `pf_bridge` ต้นรอบ หักใบที่มี `.CONSUMED.txt` คู่ ⇒
สี่ใบใหม่ อ่านครบทั้งสี่ก่อนแตะโค้ด:

1. `20260904_0328_PANYA-DECISION-...` -- คำสั่งเจ้าของตั้งเลนใหม่ (LANE-CS/LANE-UI) + ยืนยัน LANE-DB
   ถือ PLAYER/CHARACTER ก่อนอย่างอื่น รับทราบ ไม่มีอะไรให้ทำเพิ่มจากใบนี้เอง (ใบ `0329` ที่ตามมาคือใบสั่งงาน
   จริง ซึ่งบริโภคไปแล้วตั้งแต่รอบก่อน ๆ)
2. `20260904_0905_CHIEF-TO-LANE-DB-CORRECTION-...` -- chief แก้ใบตัวเองเรื่อง `RE-122`/`RE-229` ถามว่า
   ชิ้น 2 เดินได้เลยไหมด้วยหลักฐานที่พินแล้วของ `RE-122` -- ตอบแล้ว: **เดินไม่ได้** เพราะ crosswalk หกแกน
   → ห้า wire field ที่ชิ้น 2 ต้องใช้ยังเป็นช่องว่างจริงตามที่ `RE-122` เขียนไว้เอง
   (`docs/FUNCTIONAL_COVERAGE.json`: `AGILITY<->DEX` เป็น inference ไม่ใช่ผลผูก) ส่งจดหมายตอบแล้ว
   (`20260904_1012_LANE-DB-REPLY-piece2-cannot-proceed-without-re-229-crosswalk.md`)
3. `20260904_0938_CHIEF-TO-LANE-DB-...` -- chief รับ CORE-REQUEST boot-time backfill loop ไว้ทำเองรอบถัดไป
   ไม่ต้องรอ ไม่มีอะไรให้ LANE-DB ทำเพิ่ม รับทราบ
4. `20260904_0942_COO-DECISION-...` -- คำตอบขอบเขตชิ้น 3 (ดูหัวข้อบนของไฟล์นี้) -- นี่คือใบที่รอบนี้ทำตาม

สร้าง stub `.CONSUMED.txt` ให้ทั้งสี่ใบแล้ว ส่งจดหมายออกหนึ่งใบ (ข้อ 2 ข้างบน)

## 3. ทำอะไร

### 3.1 อ่านขอบเขตชิ้น 3 ตาม `0942` ให้ครบก่อนเขียนโค้ด

`0942` ข้อ 3: ขอบเขตชิ้น 3 = ชุด mask ล็อกอิน (b'') ตัดกับแถวที่มีค่าจริง แถวที่ล็อกอินส่งแต่ DB ไม่มีค่า
= `server_owned_value_not_supplied` รายงานในไฟล์รอบเป็นรายชื่อ ไม่ใช่เติมศูนย์ -- 55 แถวของ
`compose_full_block` ไม่ใช่เกณฑ์ (ยืนยันสิ่งที่วัดไว้ในรอบก่อน)

**ตัวที่ตั้งใจไม่ทำ, และทำไม**: การหาชุด mask ล็อกอิน (b'') จริง ๆ มีอยู่แล้วในโค้ด --
`gm/login_mask.login_field_x(legacy)` -- แต่ทุก caller ที่มีอยู่ (`tests/test_gm_login_mask.py`) เรียก
`legacy_bridge.load_legacy(ROOT / "current/pf_login_game_server_v141.py")` เพื่อได้ `legacy` object
มา ป้อนให้ฟังก์ชันนั้น ⇒ การเรียก `login_field_x` เองในโมดูล/เทสของ LANE-DB จะพา v141 เข้ามาเป็น
dependency ของสายนี้โดยตรง ซึ่งเป็นข้อห้ามตลอดกาลของกฎบัตร ("ห้ามแตะ v141 ... ห้ามใช้เป็นเกณฑ์")
รอบนี้จึงเลือกรายงาน `SERVER_OWNED_FIELDS` (22 fields) ที่ "supplied/not-supplied" เต็มชุด แทนที่จะกรอง
ด้วย (b'') เอง แล้วให้ผู้อ่านไฟล์รอบตัด (intersect) เองด้วยชุดที่วัดไว้แล้วใน docstring ของ
`gm/login_mask.py` เอง (ล็อกอินปกติผูก `{1,2,3,4,7,9,10,13,24}`, กิ่ง faction เพิ่ม `{11}`) แทนที่จะ
พิมพ์ชุดนั้นซ้ำเป็นสำเนาที่ดริฟต์ได้ในไฟล์ของ LANE-DB เอง -- `pf-adversary` ยืนยันจุดนี้ไม่ใช่บั๊ก
เป็น trap ที่ต้องระวังตอนอ่านผลลัพธ์ (ดูข้อ 3.2)

### 3.2 โค้ดที่เพิ่ม

- `persistence_attr_compose.live_typed_values_for(store, character_id)` และ
  `.live_unlock_report(store, character_id)` -- เวอร์ชัน "จริง" ของ `unlock_report()` เดิม
  (ซึ่งวัดกับ `{}` เสมอ) ใช้ค่าจริงจากแถวตัวละครหนึ่งตัว คืนรายชื่อ x ที่ "supplied" กับ "not_supplied"
  ของ `SERVER_OWNED_FIELDS` ทั้ง 22 ตัว -- ไม่เดา ไม่เติมศูนย์ ใช้ `block_gaps`/`typed_values_for_compose`
  เดิมทั้งหมด ไม่ตัดสินอะไรใหม่
- `store.SQLiteStore.read_typed_attributes_and_name(character_id)` -- method ใหม่ อ่าน typed columns
  กับ name จาก connection เดียว row เดียว (ดูข้อ 3.3 -- เหตุที่ต้องเพิ่ม) ไม่แตะ method เดิม

### 3.3 `pf-adversary` (สั่งต้นรอบ ผลคืนก่อน push)

พบสองข้อจริง แก้ทั้งคู่ก่อน push:

1. **AST guard (`test_the_module_uses_no_defaulting_call_anywhere`) มีจุดบอด** -- `producers` set ใน
   เทสไม่รวมฟังก์ชันใหม่สองตัว ยืนยันด้วยการ mutate จริง: เปลี่ยน
   `values[1] = character.name` (ตอนนั้นยังเป็น draft) เป็น `values[1] = character.name or "Unknown"`
   (ค่าเดาแบบตรงข้อห้ามของเจ้าของเป๊ะ ๆ) แล้วรันชุดเทสของไฟล์นี้ทั้งไฟล์ -- ผ่านหมดไม่มีอะไรจับ
   แก้โดยเพิ่ม `"live_typed_values_for", "live_unlock_report"` เข้า `producers` set
2. **TOCTOU จริงระหว่าง `read_typed_attributes` กับ `get_character`** -- draft แรกอ่านสองครั้งคนละ
   connection ยืนยันด้วยการ monkeypatch ให้มีการเขียน `class_id` แทรกกลางสองคอล -- รายงานอ่านค่าเก่า
   (ไม่ครบ) และแทรก soft-delete กลางสองคอล -- ครึ่งหนึ่ง raise `KeyError` อีกครึ่งไม่ (ไม่ตรงกัน)
   ไม่ได้ทำให้เกิดค่าเดาซึ่งเป็นกฎหลักของไฟล์นี้ แต่ผลลัพธ์ไม่ใช่ snapshot เดียวกันจริง แก้โดยเพิ่ม
   `store.read_typed_attributes_and_name` (connection เดียว) แล้วให้ `live_typed_values_for` เรียกอันนี้
   แทนสองเมธอดเดิม
3. (informational, ไม่ใช่บั๊ก) จุด trap ของการอ้าง `server_owned_fields_not_supplied` เป็น "สิ่งที่บล็อก
   ล็อกอิน" ตรง ๆ โดยไม่ตัด (intersect) กับชุด (b'') ก่อน -- x=9/10/11 อยู่ในล็อกอินจริงแต่ไม่อยู่ใน
   `SERVER_OWNED_FIELDS` เลย (เป็น `CLIENT_DEFAULT`) จึงไม่โผล่ในลิสต์ไหนของฟังก์ชันนี้ทั้งคู่ -- เพิ่ม
   comment เตือนเรื่องนี้ตรง ๆ ในโค้ด (ดูข้อ 5.3 การอ่านผลลัพธ์ด้านล่าง)

หลังแก้ทั้งสองข้อ ไม่ได้เรียก `pf-adversary` ซ้ำรอบสอง (ตามแบบแผนรอบก่อน `b0ede7`: แก้ตามผลที่ได้
แล้วรันชุดเต็มเป็น commit สุดท้ายจริง ไม่ใช่เรียกซ้ำเพื่อยืนยันการแก้เล็กที่ตรงเป้า)

### 3.4 ตัวอย่างค่าจริง (วัดจากเทสของรอบนี้)

ตัวละครใหม่ที่สร้างผ่าน `store.create_character` เปล่า ๆ (ไม่ผ่าน `lifecycle.create` -- ยังไม่ได้ผ่าน
`persist_class_id_from_starting_gear`) วันนี้:

- **supplied** (5 จาก 22): x=1 name, x=2 level, x=3 hp_current, x=4 hp_max, x=7 speed_walk --
  ทั้งหมดมาจาก DEFAULT ของ `migrations/009` ไม่มีค่าไหนที่ LANE-DB เขียนเองในรอบนี้
- **not_supplied** (17 จาก 22): x=5,6 (mp), x=13 class_id (backfill loop ยังไม่ลง -- chief รอบหน้า),
  x=16,17 (skill/unspent points), x=18-22 (stat_*), x=23 experience, x=24 cash, x=31-35 (bonus_*) --
  ตรงกับ 17 คอลัมน์ที่ `COO-DECISION 20260902_1607` ค้าง NULL ไว้เป๊ะ

ตัวละครที่ผ่าน `lifecycle.create` จริง (chief รอบหน้าจะเปิด boot-backfill loop) จะมี x=13 เพิ่มเข้า
supplied -- โค้ดของรอบนี้วัดตรงนั้นสดทุกครั้งที่เรียก ไม่ใช่ค่าคงที่

## 4. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงาน: `pytest tests/test_persistence_attr_compose.py tests/test_persistence_typed_attr_columns.py
  tests/test_persistence_class_id.py tests/test_class_id_login_wiring.py tests/test_foundation_legacy_seam.py`
  ซ้ำหลายครั้งระหว่างแก้ -- เขียวตลอด (221 passed / 818 subtests ครั้งสุดท้ายก่อนรันเต็ม)
- ชุดเต็มรอบนี้รันสองครั้ง (เกินหนึ่งครั้ง -- เหตุผลตามกติกา): ครั้งแรกหลัง `git fetch origin main` +
  merge (`531dc9d0`) และหลังแก้ตาม `pf-adversary` เรียบร้อย จับได้ว่า `tests/test_tree_is_cp874_safe.py`
  แดง -- โค้ดของรอบนี้เอง (comment ใน `persistence_attr_compose.py`) มีอักขระ `∩` (U+2229) ที่ไม่มี
  mapping ใน cp874 หนึ่งตัว ไม่ใช่ flaky ไม่ใช่ของสายอื่น แก้เป็น "INTERSECTED with" (ASCII) แล้วรันชุด
  เต็มซ้ำเป็น commit สุดท้ายจริง: **9578 passed, 323 skipped, 18733 subtests passed (467.28s)**
  บน `531dc9d0` (ไม่ขยับจากตอน fetch จนถึง push จริง)
- `pirate-force-server#723 [LANE-DB] round 1cajqi: live per-character server-owned attribute gap report
  (piece 3)` -- เปิดแล้ว มี `PF-AUTOMERGE: v4` ในตัว รอ gate Windows (ยังไม่ merge -- ไม่ได้เขียนว่าขึ้น
  main แล้ว)
- `pf_bridge#1104` (claim PR ของรอบนี้) -- เติม `PF-AUTOMERGE: v4` ทันทีหลัง push ไฟล์รอบนี้ เพราะ PR
  ฝั่งเซิร์ฟเวอร์ของรอบ (มีใบเดียว) เปิดแล้วพร้อม marker ครบตามเงื่อนไขปลดล็อก

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** -- รอบนี้เพิ่มฟังก์ชันอ่านอย่างเดียวในโมดูลของ LANE-DB (`persistence_attr_compose.py`)
กับ method อ่านอย่างเดียวใหม่ใน `store.py` ไม่มีจุดเสียบไปยัง boot/runtime/encoder ใด ๆ ตรวจแล้ว:
`grep` เจอแค่ไฟล์ตัวเองกับเทสของตัวเอง ไม่มีอะไรใหม่บนจอผู้เล่นจากรอบนี้ ไม่เข้าคิว GT รอบนี้

### 5.2 wire-DB

- `src/pirateforce_foundation/persistence_attr_compose.py` (แก้) -- เพิ่ม `live_typed_values_for`,
  `live_unlock_report` (78 บรรทัดใหม่) ไม่แตะฟังก์ชันเดิม
- `src/pirateforce_foundation/store.py` (แก้) -- เพิ่ม `read_typed_attributes_and_name` ไม่แตะ method เดิม
- `tests/test_persistence_attr_compose.py` (แก้) -- เพิ่มคลาส `LiveUnlockReportTests` (7 เทส) + แก้
  `producers` set ในเทส AST guard ที่มีอยู่แล้ว (2 ชื่อฟังก์ชันเพิ่ม)
- `tests/test_persistence_typed_attr_columns.py` (แก้) -- เพิ่มคลาส `ReadTypedAttributesAndNameTests`
  (5 เทส)
- ไม่มีไฟล์ migration ใหม่ (ตาม `0942` ข้อ 2 ห้าม)
- ไม่มีการเขียนแถวจากรอบนี้ (ทุกฟังก์ชัน/method ใหม่เป็น read-only ล้วน)
- `pirate-force-server#723`, `pf_bridge#1104` -- ลิงก์ PR ของรอบ

### 5.3 วิธีอ่านผลลัพธ์รอบหน้า (คำเตือนที่ฝังไว้ในโค้ดด้วย)

`live_unlock_report(...)["server_owned_fields_not_supplied"]` **ไม่ใช่** "สิ่งที่บล็อกล็อกอิน" ตรง ๆ
มันเป็น superset ของช่องว่างจริงของ (b'') -- ผู้อ่าน (รวมถึง LANE-DB รอบหน้า) ต้องตัด (intersect) กับ
ชุดที่วัดไว้ใน `gm/login_mask.py` docstring (`{1,2,3,4,7,9,10,13,24}` ∪ `{11}` กิ่ง faction) เองก่อน
จึงจะได้ช่องว่างจริงของชิ้น 3 -- x=9/10/11 ไม่โผล่ในลิสต์ไหนของฟังก์ชันนี้เลย (เป็น `CLIENT_DEFAULT`
ไม่ใช่ `SERVER_OWNED`) แม้จะอยู่ในล็อกอินจริงก็ตาม `pf-adversary` ชี้จุดนี้ไว้ ไม่ใช่บั๊กที่ต้องแก้
แต่เป็นกับดักตอนอ่าน

## 6. nonclaims

1. **ไม่อ้างว่าชิ้น 3 (บล็อก `0x309A` เต็ม) เสร็จ** -- `compose_full_block` ยังบล็อกอยู่เหมือนเดิม
   (`RESEND_ADJUDICATED` ว่างเปล่าโดยตั้งใจ, เหตุผลเดิมทุกประการ) รอบนี้ให้แค่ "รายชื่อที่ตรวจได้" ตามที่
   `0942` สั่ง ไม่ใช่การปลดบล็อก
2. **ไม่ได้เรียกหรือ derive ชุด mask ล็อกอิน (b'') เอง** -- ตั้งใจ เพราะทางเดียวที่มีอยู่ต้องพึ่ง
   `legacy_bridge.load_legacy` ชี้ไปที่ v141 (ดูข้อ 3.1) `server_owned_fields_not_supplied` จึงเป็น
   superset ไม่ใช่ตัวเลขสุดท้าย (ดูข้อ 5.3)
3. **ไม่ได้แตะ 17 คอลัมน์ที่ `1607` ค้าง NULL** (ชิ้น 2) -- ยืนยันด้วยจดหมายตอบ chief ว่ายังเดินไม่ได้
   จนกว่า `RE-229` จะตอบ
4. **ไม่ได้ปิด `class_id` backfill สำหรับตัวละครเก่า** -- chief รับไปทำเองรอบหน้าตามใบ `0938`
5. **ไม่ได้แตะ `gm/`, `app.py`, `lifecycle.py`, `migrations/`** -- นอกเขตเขียนของ LANE-DB ทั้งหมด
6. **`1101` (HP/เลเวลถาวร) ยังล็อกอยู่เหมือนเดิม** -- รอบนี้ไม่ได้วัดซ้ำ Door B (นอกคิวรอบนี้ตาม `0329`
   ข้อ 1: PLAYER/CHARACTER มาก่อน)
7. **ไม่ได้เปิด image/canonical DB/capture corpus** -- ทุกอาร์ติแฟกต์ commit แล้วในสองรีโป

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจว่า `pirate-force-server#723` gate ผ่าน + merge เข้า main หรือยัง
3. ตรวจว่า chief เปิด PR boot-time class_id backfill loop (ใบ `0938`) หรือยัง -- merge แล้วให้วัดซ้ำว่า
   `live_unlock_report` รายงาน x=13 เป็น supplied สำหรับตัวละครเก่าจริงไหม (ตัวอย่าง end-to-end แรกของ
   ฟังก์ชันนี้)
4. ตรวจว่า chief ตอบใบ `20260904_1012_LANE-DB-REPLY-piece2-...md` (ยืนยัน "เดินไม่ได้") หรือมีข้อโต้แย้ง
5. ตรวจสถานะ `RE-229` (`CLIENT_RE_QUEUE.md`) -- ยัง OPEN ณ ต้นรอบนี้ -- ถ้าผลถึงแล้วให้อ่าน ใช้ แล้วปิด
   หัวใบเองพร้อม stub
6. piece 4 (นามแฝง + รหัสผ่านรอง MD5) ยังต้องส่ง RE ก่อนตาม `0329` ข้อ 4 -- ตรวจว่าส่งไปหรือยัง ถ้ายัง
   ให้ส่งรอบหน้า
7. ถ้า COO/chief ต้องการช่อง (b'') ที่ตัด intersect แล้วจริง ๆ (ไม่ใช่ superset) ให้เขียนใบขอ chief
   เปิดจุดเสียบที่ไม่ต้องพึ่ง v141 (เช่น chief บันทึกชุด mask ที่ login คำนวณจริงไว้ให้ LANE-DB อ่าน --
   ใกล้เคียงกับที่ `CORE-REQUEST-GM-053` ขอไว้แล้วสำหรับ per-connection mask) แทนที่จะให้ LANE-DB derive
   เอง
