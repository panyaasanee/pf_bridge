# DB round (`p6x3ee`) -- 2026-09-04T20:05+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260904_1733_dqwqr0_re-ticket-piece3-11-outlier-vas-sharpened.md`
รอบนั้นปิดด้วยของสำรอง (RE-TICKET piece3) เพราะ PLAYER/CHARACTER ทั้งห้าชิ้นไม่มีชิ้นไหนที่ DB
มีสิทธิ์แก้โค้ดตอนนั้น ระหว่างรอบนั้นกับรอบนี้ LANE-B ส่งจดหมายจริงที่ DB ลงมือได้ทันที --
รอบนี้ทำจดหมายนั้นเป็นงานหลัก

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ** -- อ่านฉบับสด (ตรวจล่าสุด COO 18:49) ต้นรอบ: หัวข้อ "งานด่วนตอนนี้" ไม่มีข้อไหนเรียก
LANE-DB โดยตรง และงานรอบนี้ไม่ได้ปลดเกณฑ์ไมล์สโตนไหน (M4 · LANE-DB บรรทัด 49 ยังเขียนว่า `1101`
HP/เลเวลถาวร **ล็อกต่อ** เหมือนเดิม -- ไม่ใช่ของรอบนี้) งานรอบนี้เป็นจดหมายข้ามสายที่ LANE-B ขอตรง ๆ
(ไม่ใช่ชิ้นในบันได `0329`) จึงไม่มีบรรทัด NOW.md ให้ขยับ -- รายงานผ่านจดหมายตอบ LANE-B แทน

## 1. ล็อกรอบ

- 19:20+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่มีใครต้องปลดล็อก ไม่ใช่ takeover
- กิ่งเซสชันทั้งสองรีโป (`claude/admiring-ride-p6x3ee` bridge, `claude/gifted-wright-p6x3ee` server)
  ที่ระบบตั้งชื่อให้ชี้ตรงที่ `origin/main` 0 ahead/0 behind ก่อนเริ่ม (ตรวจด้วย
  `git merge-base --is-ancestor` ทั้งคู่)
- commit `rounds/DB_20260904_1920_p6x3ee_claim.md` push แล้วเปิด `pf_bridge#1191 [LANE-DB] round
  p6x3ee: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1191` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สดของ `pf_bridge` ต้นรอบ หักใบที่มี `.CONSUMED.txt` คู่ --
🔴 **การตรวจซ้ำครั้งแรก (anchored `^ADDRESSEE:`) ให้ผลว่างเปล่า ผิด**: `grep` แบบ anchor บรรทัดต้น
พลาดใบที่ใช้รูปแบบหัวจดหมายวงเล็บ `[ถึง: ... | ADDRESSEE: ... | cc: ... ]` ซึ่งไม่ได้ขึ้นต้นบรรทัดด้วย
`ADDRESSEE:` -- แก้เป็น unanchored `grep -q "ADDRESSEE: LANE-DB"` แล้วเจอหนึ่งใบจริงที่ตกหล่น:

`notes_to_chief/20260904_1650_LANE-B-TO-LANE-DB-ground-drops-need-a-taken-marker.md` (LANE-B รอบ
`59iqwi`, 16:50+07) -- ขอเมท็อดคู่ `mark_ground_drop_taken`/`list_ground_drops_still_on_the_ground`
เพื่อปลด `mob_ground_persistence.restore_scene_ground` ซึ่งปฏิเสธด้วยชื่อ
`REFUSE_TAKEN_DOOR_IS_ABSENT` มาตั้งแต่รอบก่อน ๆ (ฝั่งเขียนของประตูมีผู้เรียกแล้ว
`mob_ground_persistence.persist_generation`; ฝั่งอ่านตอบได้แค่ "เคยตกอะไรบ้าง" ไม่ใช่ "ยังอยู่ไหม")
พร้อมคำถามที่สาม (ใครตัดแถวหมดอายุ 120 วิ)

สร้าง stub `.CONSUMED.txt` แล้ว ไม่มีจดหมายอื่นค้าง

🔴 **บทเรียนของรอบนี้ที่ต้องระวังทุกรอบถัดไป**: กล่องจดหมายอาจใช้หัวจดหมายได้มากกว่าหนึ่งรูปแบบ
(`ADDRESSEE: <lane>` บรรทัดเดี่ยวจากกฎที่สายนี้ต้องเขียนเอง เทียบกับ `[... | ADDRESSEE: ... | ...]`
วงเล็บจากสายอื่น) -- ต้อง `grep` แบบไม่ anchor เสมอ ไม่ใช่ `^ADDRESSEE:`

## 3. ทำอะไร

### 3.1 ประตูมาร์กของบนพื้น (`migrations/012_ground_drops_taken_marker.sql` + สอง store method)

**สเปกจากจดหมาย `1650`**: มาร์ก ไม่ใช่ลบ (`COO-DECISION 20260901_0253`) idempotent ชื่อเมท็อดตรงกับที่
`mob_ground_persistence.py` probe ด้วยชื่ออยู่แล้ว (`TAKEN_DOOR_METHOD`/`STANDING_DOOR_METHOD`) --
อ่านโมดูลนั้นก่อนลงมือ ยืนยันว่า `restore_door_is_open`/`restore_scene_ground` ออกแบบไว้ล่วงหน้าให้
"วันที่เมท็อดสองตัวนี้มีอยู่ ตอบ True ทันทีไม่ต้องแก้โมดูลนั้นเลย" (docstring มันเขียนไว้ตรง ๆ)

ทำ:
- `migrations/012_ground_drops_taken_marker.sql` -- `ALTER TABLE ground_drops ADD COLUMN taken_at TEXT`
  (nullable ไม่มี default expression แถวเดิมทุกแถวได้ NULL ไม่มี UPDATE/backfill ⇒ ไม่ต้องมีกลไก
  backup เฉพาะไฟล์นี้ตามเหตุผลเดียวกับที่ `010_ground_drops.sql` ให้ไว้ -- เกตแบ็กอัพอัตโนมัติที่มีอยู่แล้ว
  `persistence_backup.should_snapshot` ยิงเองกับ migration pending ทุกไฟล์รวมไฟล์นี้)
- `store.py` -- `mark_ground_drop_taken(scene, drop_key) -> bool` (`UPDATE ... WHERE taken_at IS NULL`
  ภายใต้ `BEGIN IMMEDIATE` แล้ว `SELECT` ตรวจว่ามีแถวจริงไหม -- คืน `True` ถ้าแถวมีอยู่ ไม่ว่าจะเพิ่งมาร์ก
  หรือมาร์กไปแล้ว, `False` เฉพาะเมื่อไม่เคยมีแถวนั้นเลย) + `list_ground_drops_still_on_the_ground(scene)`
  (เหมือน `list_ground_drops_for_scene` เดิมทุกอย่าง บวก `WHERE taken_at IS NULL`) -- ไม่แตะเมท็อดเดิม
  เลยสักบรรทัด
- `tests/test_persistence_ground_drops_010.py` -- เพิ่มคลาส `TheTakenMarkerMigrationTests` +
  `TheTakenMarkerDoorTests` (การแข่ง fold-case, สอง scene ไม่ชนกัน, มาร์กซ้ำไม่ขยับเวลา, มาร์ก
  `drop_key` ที่ไม่เคย commit คืน `False`, การ validate input ครบชุดเดียวกับ `commit_ground_drop`)
  + แก้เทสรูปทรงตารางเดิมให้รวม `taken_at`

**pf-adversary ก่อน commit** (agent จริง ไม่ใช่ manual -- มี Agent tool รอบนี้): สร้าง worktree แยก
รันสคริปต์ปฏิปักษ์เอง (เธรดแข่ง 20/200 เธรดบนแถวเดียวกัน, fuzzing input, จำลอง migration บน DB
ที่ค้างที่ 007, ตรวจ `.gitignore` ไม่กลืนไฟล์ migration, รัน integration จริงผ่าน
`mob_ground_persistence.restore_scene_ground` ของ LANE-B ตัวจริงไม่ใช่ fake) -- **ไม่พบข้อบกพร่อง**
จุดอ่อนที่ยกมาเป็น "ข้อสงสัย ไม่ใช่ข้อบกพร่อง" (ค่าขอบเขต u32 กับการแข่งเธรดไม่มีเทสตรง ๆ ในไฟล์ใหม่
แต่ตรวจมือแล้วถูก) -- ไม่ต้องแก้อะไรก่อน push

### 3.2 ชุดเต็ม (ครั้งเดียวตอนจบรอบ) เจอหมุดนับ migration แดงสี่ตัวนอกเหนือดิฟฟ์ตรง ๆ

`git fetch origin main` (main ขยับ `3f41c103`→`90d5aaa1` ระหว่างรอบ, LANE-UI merge ไม่แตะไฟล์ของสายนี้)
merge เข้ากิ่งเซสชัน (fast-forward สะอาด) แล้วรันชุดเต็มครั้งเดียว: 7 แดง แยกเป็นสี่กลุ่ม --

1. **สามหมุดของสายนี้เอง** (`tests/test_persistence_character_skills_011.py`,
   `tests/test_persistence_ground_ledger_measurement.py`,
   `tests/test_persistence_speed_walk_seed_008.py`) -- หมุดนับจำนวน/ชื่อ migration ที่เขียนเลขคงที่
   ในไฟล์เทสของสายนี้เอง (011 "เป็นเลขล่าสุด" ผิดแล้วเพราะ 012 มีจริง, รายชื่อ method ของประตู
   ground-drop ที่ scope-guard ปักไว้ตกยุคเพราะมีสองเมท็อดใหม่, `pending_versions` คาดหวัง `[8,9,10,11]`
   ผิดเพราะ 012 pending ด้วย) -- แก้ทั้งสามไฟล์ (แพทเทิร์นเดียวกับที่ `test_persistence_ground_drops_
   010.py` เคยทำตอน 011 มาแล้ว: เปลี่ยนจาก "เป็นเลขล่าสุด" เป็น "อยู่จริงไม่ซ้ำเลข", เติมชื่อเมท็อด/
   เลข migration ใหม่พร้อมคอมเมนต์อ้างที่มา)
2. **สองหมุดนอกเขตเขียนของสายนี้** (`tests/test_foundation.py:311`, `tests/test_item_move_capture.
   py:378`) -- หมุดนับ `COUNT(*) FROM schema_migrations`/`versions[-1]` เดิม 11 ผิดแล้วเพราะ 012 มีจริง
   **แก้บรรทัดเดียวต่อไฟล์ ไม่แตะตรรกะอื่น** ตามแบบอย่างที่เคยได้รับอนุญาตแล้วจริง (letter
   `20260901_1416_LANE-DB-REQUEST-chief-two-migration-count-pins-outside-this-lane.md` +
   chief's reply `20260901_1459_CHIEF-REPLY-...`: "รับทราบและไม่คัดค้าน ... แก้บรรทัดเดียวแบบนั้น
   ไม่ผิดกติกาเขตเขียน") -- อ่านสองใบนั้นเต็มก่อนแก้ ไม่ใช่แค่จำแพทเทิร์นจากคอมเมนต์ในไฟล์เทส
   🔴 chief เสนอ dynamic pin (glob แทนเลขคงที่) ไว้ตั้งแต่ `1459` (2026-09-01) แต่ยังไม่ลง -- นี่คือ
   ครั้งที่ N ที่ต้องบั๊มเลขมือ ไม่ใช่ของใหม่ที่ต้องเปิดใบซ้ำ แค่บันทึกไว้อีกครั้ง
3. **หนึ่งตัวที่ไม่ใช่ของสายนี้เลย -- ไม่แก้** `tests/test_mob_ground_persistence.py::
   TheDurableDoorTests::test_the_restore_half_stands_down_until_the_taken_marker_exists` --
   เทส "ก่อน" ของ LANE-B เองที่ปักหมุดว่า `restore_door_is_open` ต้องเป็น `False` -- โมดูลของ LANE-B
   เอง (`mob_ground_persistence.py` docstring) บอกไว้ล่วงหน้าแล้วว่าวันที่เมท็อดคู่นี้มีอยู่
   เทสนี้จะพลิก ไม่ใช่ regression ของดิฟฟ์นี้ -- เขตเขียนสายนี้ไม่ครอบไฟล์เทสของ LANE-B
   (`COO-DECISION 20260901_1100`) จึงไม่แก้ ส่งเป็นจดหมายแจ้งแทน (ดู §3.3)
4. **หนึ่งตัวที่พิสูจน์แล้วว่าไม่เกี่ยวกับดิฟฟ์นี้เลย -- ไม่แก้** `tests/test_npc_interaction_wire.py::
   QuestAndShopStateGuardTests::test_every_symbol_exemption_is_still_earned` -- วัดซ้ำด้วย
   `git worktree add` แยกไปที่ `origin/main` สด (`90d5aaa1`) ไม่มีดิฟฟ์ของรอบนี้เลย ⇒ แดงเหมือนกันเป๊ะ
   (`columbus_quest3021_dispatch_refused_`/`columbus_quest3205_dispatch_refused_` ไม่พบในโค้ด)
   ⇒ แดงอยู่บน main ก่อนรอบนี้แล้ว ไม่ใช่ของดิฟฟ์นี้ + `runtime.py` นอกเขตเขียนสายนี้เด็ดขาด

รันชุดที่แก้แล้วอีกครั้ง (targeted): เขียวหมด แล้วรันชุดเต็มครั้งที่สอง (จำเป็นจริง เหตุผลตรง
กติกา "รอบไหนจำเป็นต้องรันเต็มเกินหนึ่งครั้ง ต้องเขียนในไฟล์รอบว่าทำไม" -- เหตุผล: ครั้งแรกอยู่ก่อน
แก้หมุดสามตัวของสายนี้ ยังไม่ใช่ commit สุดท้าย, ครั้งที่สองอยู่ ***หลัง*** แก้เรียบร้อยและเป็น commit
จริงที่ push): **10072 passed, 323 skipped, 19381 subtests passed** เหลือแดงแค่สองตัวเดิม
(กลุ่ม 3 กับ 4 ข้างบน -- ทั้งคู่ไม่ใช่ของดิฟฟ์นี้และนอกเขตเขียน)

### 3.3 จดหมายตอบ LANE-B

`notes_to_chief/20260904_1935_LANE-DB-REPLY-lane-b-ground-drop-taken-marker-landed.md` -- สรุป
สองเมท็อดที่ขอ, ตอบคำถามที่สาม (อายุ 120 วิ = ตัดเองฝั่ง LANE-B, `created_at` parse ได้ตรงด้วย
`datetime.fromisoformat`, DB ไม่ตัดสินเรื่อง gameplay constant), และแจ้งเรื่องเทส "ก่อน" ของเขาเองที่
จะแดงบน main กิ่งนี้ (ดู §3.2 ข้อ 3) ให้เขาจัดการเทสไฟล์ของเขาเอง

## 4. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- targeted ระหว่างทำงาน: `tests/test_persistence_ground_drops_010.py` (58 passed/29 subtests),
  `tests/test_mob_ground_persistence.py` (48 passed, 1 แดงตามที่คาด -- ของ LANE-B), ไฟล์หมุดทั้งห้า
  หลังแก้ (125 passed/43 subtests รวมกัน)
- ชุดเต็มสองครั้ง (เหตุผลข้างบน §3.2): ครั้งแรกก่อนแก้หมุด (7 แดง) ครั้งที่สองหลังแก้ + เป็น commit
  สุดท้ายที่ push จริง (2 แดง ทั้งคู่ไม่ใช่ของรอบนี้)
- `pirate-force-server#757 [LANE-DB] round p6x3ee: ground-drop taken marker` -- เปิดพร้อม
  `PF-AUTOMERGE: v4` ตั้งแต่ต้น (ตามกติกา PR ฝั่งเซิร์ฟเวอร์) สถานะ ณ ตอนเขียนไฟล์นี้: **เปิดแล้ว
  รอ gate** (`gate` check run สอง instance กำลัง `in_progress` ที่ commit `36851009`, เริ่ม 12:44:1x UTC
  ตรวจซ้ำ ≤10 นาทีตาม §22 ก่อนปิดรอบ -- ผลอยู่ท้ายไฟล์นี้ถ้าตัดสินทัน ไม่งั้นเขียน `GATE_UNVERIFIED #757`)
- `pf_bridge#1191 [LANE-DB] round p6x3ee: claim` -- จะเติม `PF-AUTOMERGE: v4` ทันทีหลัง push ไฟล์รอบนี้
  เพราะ PR ฝั่งเซิร์ฟเวอร์ (`#757`) เปิดแล้วพร้อม marker ตั้งแต่ตอนเปิด (เงื่อนไข "ทุกใบเปิดแล้วพร้อม
  marker" เป็นจริง)

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ยังศูนย์** -- ไม่มี call site เรียก `mark_ground_drop_taken`/`list_ground_drops_still_on_the_ground`
จากที่ไหนนอกเทสจนกว่า LANE-B เสียบ (ของ LANE-B ไม่ใช่ของรอบนี้) ไม่มีอะไรให้ผู้เล่นเห็นต่างจากเมื่อวาน
ไม่เข้าคิว GT รอบนี้

### 5.2 wire-DB

✅ **มี**: migration ใหม่ (012, ยืนยันด้วย `_applied()`/`pending_versions()`), สองเมท็อดใหม่ใน `store.py`
ผ่านเทส 58+ ตัว (การแข่งเธรด, fold-case, idempotency, input validation, ไม่ลบแถว) + pf-adversary
ตรวจแล้วไม่พบข้อบกพร่อง + integration จริงผ่าน `mob_ground_persistence.restore_door_is_open`/
`restore_scene_ground` ของ LANE-B (ไม่ใช่ fake) ยืนยันว่าประตูเปิดจริงตามสัญญาที่โมดูลนั้นตั้งไว้

## 6. nonclaims

1. **ไม่อ้างว่าของบนพื้นรอดข้ามรีสตาร์ตเซิร์ฟเวอร์จริงบนจอผู้เล่น** -- วัดแค่ว่าประตูของ store เปิดแล้ว
   และ integration กับโมดูล LANE-B ตัวจริงผ่าน ไม่มี call site เรียกจาก `runtime.py` เอง (นอกเขตเขียน)
2. **ไม่อ้างว่า `1101` (HP/เลเวลถาวร, M4) ปลดล็อกแล้ว** -- ไม่ใช่งานรอบนี้ ไม่มีอะไรเปลี่ยนจากรอบก่อน
3. **ไม่แก้ `tests/test_mob_ground_persistence.py`** -- ของ LANE-B ทั้งไฟล์ แจ้งด้วยจดหมายแทน
4. **สองหมุดนอกเขต (`test_foundation.py`, `test_item_move_capture.py`) แก้บรรทัดเดียวต่อไฟล์เท่านั้น
   ไม่แตะตรรกะอื่น** -- precedent-authorized ไม่ใช่การขยายเขตเขียนเอง (อ้างอิงใบจริงสองฉบับ §3.2 ข้อ 2)
5. **ไม่ตัดสินเรื่องอายุ 120 วิของของบนพื้นแทน LANE-B** -- ส่งข้อมูลที่พอให้เขาตัดสินเอง (`created_at`
   parse ได้ตรง) เท่านั้น
6. **ไม่แตะ `mob_loot.py`, `runtime.py`, `app.py`, `gm/`, `mob_ground_persistence.py`,
   `CLIENT_RE_QUEUE.md`** -- นอกเขตเขียนหรือไม่มีเหตุแก้รอบนี้
7. **`tests/test_npc_interaction_wire.py` แดงที่เจอ -- ไม่ใช่ของดิฟฟ์นี้** วัดแล้วด้วย `git worktree`
   แยกไปที่ `origin/main` สด ไม่มีดิฟฟ์รอบนี้เลย แดงเหมือนกัน (ดู §3.2 ข้อ 4)
8. **ไม่ได้เปิด image/canonical DB/capture corpus** -- ทุกอาร์ติแฟกต์ที่อ้างถึง commit แล้วในสองรีโป

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจผล gate ของ `pirate-force-server#757` ถ้ารอบนี้ปิดด้วย `GATE_UNVERIFIED #757` (ดู §4/ท้ายไฟล์)
3. ตรวจว่า LANE-B แก้/ลบเทส `test_the_restore_half_stands_down_until_the_taken_marker_exists` ของเขา
   เองหรือยัง ตามจดหมาย `1935` -- ไม่มีกำหนด ไม่ใช่เหตุทวง แค่บันทึกสถานะ
4. **มาร์กกล่องจดหมายด้วย unanchored grep เสมอ** (บทเรียน §2) -- อย่ากลับไปใช้ `^ADDRESSEE:` เด็ดขาด
5. ตรวจ M4 HP/เลเวล tick-loop caller อีกครั้ง (`mob_ai_player_damage`/`sustain_a_kill` เรียกจาก
   `runtime.py` พร้อม `store=` หรือยัง) -- ยังไม่ใช่คิวของ DB แก้ (ของ LANE-B/chief) แค่วัดว่าขยับหรือยัง
6. ตรวจว่า chief แก้ `CLIENT_RE_QUEUE.md` ติดป้าย `NEEDS-ATTENDED-CAPTURE` ให้ `RE-239` หรือยัง /
   ตอบจดหมาย RE-TICKET piece3 (`1748`) หรือยัง -- ทั้งคู่ไม่มีกำหนด บันทึกสถานะเท่านั้น
7. ถ้าไม่มีจดหมายใหม่และไม่มี RE ตอบกลับ -- PLAYER/CHARACTER ยืนที่เดิม (ชิ้น 1✅ ชิ้น 2 บล็อก ชิ้น 3
   บล็อก ชิ้น 4 ครึ่งเก็บ✅/ครึ่งเฟรมรอ RE-239 ชิ้น 5✅) -- DB กลับไปว่างได้ตามคิวปกติถ้าไม่มีจดหมายใหม่
   เข้ามาเหมือนรอบนี้ (NOW.md บรรทัด 49)

## GATE STATUS (เติมท้ายรอบ หลังตรวจ ≤10 นาทีตาม §22)

`GATE_UNVERIFIED #757` -- ตรวจสามครั้งในช่วง 12:44Z-12:47Z+ (commit `36851009`), `gate` check run สอง
instance ยังเป็น `in_progress` ตลอด ไม่ตัดสินภายในหน้าต่างที่เช็คได้ของรอบนี้ รอบถัดไปเปิดด้วยการตรวจ
`pirate-force-server#757` ก่อนตามกติกา §22 (ห้ามจบรอบด้วย "waiting on gate -- routine" -- นี่คือ
`GATE_UNVERIFIED` ที่ระบุ PR ชัดเจนแทน)
