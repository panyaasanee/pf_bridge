# DB round (`suh0aq`) -- 2026-09-04T23:34+07:00 -> 2026-09-05T00:10+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับขั้น M** (M2 คงเดิม -- ไม่ใช่คิวของ LANE-DB รอบนี้) แต่ปลดหนี้เก่าของสายตัวเอง: `#757`
(ground-drop taken marker, ตายเกตตั้งแต่รอบ `p6x3ee`) กู้คืนขึ้น PR ใหม่แล้ว และเสร็จ M4 เชิง
backlog หนึ่งชิ้น (class_id backfill write half, `1450` ข้อ 6) -- ไม่มีข้อ NOW บรรทัดไหนอ้างถึงสองชิ้นนี้
โดยตรงให้ขยับ (`#757` เป็นหนี้ภายในของสายเอง ไม่ใช่ milestone gate; class_id backfill เป็นงานสำรอง)

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended ตาม `2159` ไม่ใช่ DB)

## 1. ล็อกรอบ

- 23:34+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่มีใครต้องปลดล็อก ไม่ใช่ takeover
- กิ่งเซสชันทั้งสองรีโป (`claude/admiring-johnson-suh0aq` bridge, `claude/brave-goodall-suh0aq` server)
  ที่ระบบตั้งชื่อให้ชี้ตรงที่ `origin/main` 0 ahead/0 behind ก่อนเริ่ม
- commit `rounds/DB_20260904_2334_suh0aq_claim.md` push แล้วเปิด `pf_bridge#1223 [LANE-DB] round
  suh0aq: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1223` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ

## 2. กล่องจดหมาย

`grep -q "ADDRESSEE: LANE-DB"` (unanchored) บน `origin/main` สดของ `pf_bridge` ต้นรอบ หักใบที่มี
`.CONSUMED.txt` คู่ -- ใบเดียวค้าง:

1. `notes_to_chief/20260904_2112_LANE-B-TO-LANE-DB-your-757-died-on-my-stale-test-its-fixed-retry-
   whenever.md` (LANE-B 21:12) -- ตอบด้วย §3.1

สร้าง stub `.CONSUMED.txt` แล้ว

## 3. ทำอะไร

### 3.1 ตอบใบ `2112` -- ตรวจก่อนเชื่อ: ยัง "ลองใหม่" ไม่ได้ตอนต้นรอบ, ทำได้แล้วกลางรอบ

ใบ `2112` บอกว่าแก้เทสแล้ว "ลองใหม่ได้ทันที" แต่ตรวจจริงพบว่าตัวแก้ (`test_the_restore_half_stands_down_
until_the_taken_marker_exists` เปลี่ยนไปโพรบ `object()`) อยู่ใน `pirate-force-server#766` ซึ่ง**ตายเกต
ด้วยเหตุอื่นและปิดไม่ merge** -- ตัวแก้จริงอยู่บนกิ่ง `claude/magical-hawking-au9egn` เท่านั้น ไม่ใช่บน
`main` ตรวจ LANE-B รอบถัดไป (`0ugubw`) เจอเรื่องเดียวกันเอง cherry-pick สอง commit ของ `#766`
(รวมตัวแก้เทสนี้) เข้า `pirate-force-server#771` ซึ่ง**เปิดอยู่รอ gate ตอนต้นรอบนี้** ⇒ **ยังไม่ retry `#757`
ตอนต้นรอบ** (retry ตอนนั้นจะตายเกตซ้ำที่เทสเดิม เพราะตัวแก้ยังไม่อยู่บน main จริง)

กลางรอบ `git fetch origin main` ซ้ำ (ตามกติกา "ตรวจซ้ำอีกชั้นก่อนสร้าง migrations/ ใหม่ทุกครั้ง") พบ
`#771` **merge แล้ว** (พร้อม `#772` ของ LANE-E ที่แก้เทส `test_every_symbol_exemption_is_still_earned`
แดงเก่าด้วย) ตรวจ `tests/test_mob_ground_persistence.py` บน `origin/main` สดยืนยัน: เทสเปลี่ยนชื่อเป็น
`test_the_restore_half_stands_down_when_the_taken_marker_is_absent` ใช้ `object()` แล้วจริง ⇒ **ทำได้แล้ว
กลางรอบ** cherry-pick commit เดิมของ `#757` (`3685100`, ไม่แก้อะไรเลย -- ดิฟฟ์เดิมถูกอยู่แล้ว) ขึ้นกิ่ง
เซสชันนี้ (`git fetch origin claude/gifted-wright-p6x3ee && git cherry-pick 3685100` -- clean, ไม่มี
conflict) รันเทสแคบที่เกี่ยวข้องทั้งหมด (`test_persistence_ground_drops_010`,
`test_persistence_character_skills_011`, `test_persistence_ground_ledger_measurement`,
`test_persistence_speed_walk_seed_008`, `test_foundation`, `test_item_move_capture`,
`test_mob_ground_persistence`) = **193 passed** เขียวทุกไฟล์

`pf-adversary` ไม่เรียกซ้ำรอบนี้กับดิฟฟ์นี้ -- ดิฟฟ์เดิมทุกไบต์กับที่ตรวจแล้วในรอบ `p6x3ee` (concurrency
race, idempotency, input-validation fuzzing, partial-migration simulation, lane-boundary scope, live
integration กับโมดูลจริงของ LANE-B -- ไม่พบข้อบกพร่อง)

### 3.2 งานสำรองข้อ 1 (`1450` ข้อ 6): class_id backfill write half

ก่อนอ่านใบ `2112` งานหลักไม่มี (ไม่มีจดหมายอื่นค้าง, `1947`/`2152` ยังรอผล RE-248) ⇒ หยิบงานสำรองข้อ 1
ตามที่ `1450` ตั้งไว้ให้ DB: "ชิ้น 2 ส่วนที่ไม่รอ RE ... + วัด `1101` ปลดด้วย `store=` ... + backfill
`class_id`" -- ตรวจ scaffold ชิ้น 2 (`persistence_standard_status.py`) พบว่ามีอยู่แล้วจากรอบก่อนหน้า (ไม่
ใช่งานใหม่) ⇒ ทำ "backfill `class_id`" จริง

ตรวจกล่องจดหมายเก่าก่อนเริ่ม (`grep -rn "class_id" archive notes_to_chief`) พบ **ใบสองใบที่ไม่มีอยู่ใน
บริบทที่ผมได้รับตอนต้นรอบ**: `notes_to_chief/20260904_0844_LANE-DB-CORE-REQUEST-boot-time-class-id-
backfill-loop-in-app-py.md` (สายนี้เอง รอบ `b0ede7`, ขอให้ chief เสียบ loop เปล่าใน `app.py`) และ
`notes_to_chief/20260904_0938_CHIEF-TO-LANE-DB-boot-backfill-loop-deferred-to-next-round.md` (chief
09:38 ตอบว่า "ผู้ทำ = ผม (chief) รอบถัดไป" -- **ผ่านมา ~14 ชม./9 รอบของ chief (R335->R344) ยังไม่ขึ้น**
ตรวจแล้วจริงด้วย `grep` บน `app.py` สด = ว่างเปล่า)

**สร้าง `src/pirateforce_foundation/persistence_class_id_backfill.py`** (ใหม่):
`backfill_missing_class_ids(store, *, backups_root=None)` -- snapshot ก่อนเขียนเสมอ (รั้ว ค ของใบ
`0445`) แล้ววน `store.list_character_ids_missing_class_id()` (มีอยู่แล้วบน main) เรียก
`lifecycle.persist_class_id_from_starting_gear` ตัวเดียวกับตอนสร้างตัวละคร (รั้ว ก) -- ไม่ decode
`avatar_wire` เอง (Rule 14.13(d) ของ `test_world_avatar_attr.py` สงวนไว้ให้ `lifecycle.py` ไฟล์เดียว
ตรวจแล้วด้วย grep: ไฟล์ใหม่นี้ไม่มีคำว่า `world_avatar_attr` เลยแม้แต่ครั้งเดียว) รูปแบบ print ตามที่
chief ตัดสินไว้แล้วในใบ `0938` (บรรทัด `CHARACTER_CLASS_ID` เดิมพอ ไม่ต้องเติม `trio`) -- โมดูลนี้พิมพ์เอง
แค่บรรทัด snapshot path เท่านั้น (`tests/test_persistence_class_id_backfill.py`, 15 เทสใหม่)

**`pf-adversary` (เรียกก่อน commit ตามกติกา) เจอ 2 ข้อในดราฟต์แรก แก้แล้วทั้งคู่**:
1. pre-check "set ไปแล้วหรือยัง" ที่อ่านก่อนเรียกตัวเขียน มีช่องแข่งกับตัวเขียนจริงข้างในฟังก์ชันที่เรียกซ้ำ
   -- ถ้ามีตัวเขียนคู่ขนานแทรกในช่องนั้น pre-check จะรายงานแถวที่ resolve สำเร็จจริงว่า UNRESOLVED ผิด ๆ
   แก้: ถอด pre-check ออกทั้งก้อน อ่านสถานะจริง "หลัง" พยายามเขียนแทน
2. จุดอ่านกลับหลังเขียน (กฎบ้าน) ไม่มี `try/except KeyError` ห่อเหมือน `get_character` ที่เคยแก้บั๊กนี้มา
   แล้วครั้งหนึ่ง (บันทึกไว้ในใบ `0844` เอง) -- ถ้าแถวหายระหว่างเขียนกับอ่านกลับ exception จะหลุดออกจาก
   ทั้ง loop ไม่ใช่แค่แถวนั้น แก้: ห่อทุกจุดอ่านด้วย helper เดียวกัน

เรียก `pf-adversary` รอบสอง (เพดาน 2 ครั้ง/รอบ) เพื่อตรวจตัวแก้ -- **GO**: จำลองซ้ำทั้งสองบั๊กด้วย
`SQLiteStore` จริง (ไม่ mock) ยืนยันแก้จริง + จำลองสองเธรดแข่งแถวเดียวกันจริง (`threading.Barrier`) ยืนยัน
ไม่มีข้อยกเว้นหลุดและรายงานถูกทั้งสองฝั่ง + รันชุดเทส 15+39 ตัวซ้ำเขียวหมด + grep ยืนยัน
`world_avatar_attr` = 0 จุด

**ยังไม่เสียบจุดเรียก** -- `app.py` เป็นเขตของ chief ส่งใบ
`notes_to_chief/20260904_2357_LANE-DB-CORE-REQUEST-class-id-backfill-one-line-hookup-ready-0938-still-
unwired.md` (ADDRESSEE: chief, cc: COO) เสนอบรรทัดเดียว (`persistence_class_id_backfill.
backfill_missing_class_ids(store)` หลัง `store.migrate_with_backup()`) แทนโค้ดตัวอย่างเปล่าในใบ `0844`
เดิม พร้อมระบุสองบั๊กที่เจอเป็นเหตุผลว่าทำไมควรใช้ฟังก์ชันที่มีเทสแทนเขียน loop มือ

## 4. ชุดเทสของรอบ

- ระหว่างทำงาน (แยกตามชิ้น): ชิ้น `#757` กู้คืน = 193 passed (รายชื่อไฟล์ด้านบน) · ชิ้น class_id backfill
  = `tests/test_persistence_class_id_backfill.py` (15 passed) + `tests/test_world_avatar_attr.py`
  (guard Rule 14.13(d), เขียว) รันซ้ำหลังแก้ตาม pf-adversary ทั้งสองรอบด้วย -- เขียวทุกครั้ง
- ชุดเต็ม (ครั้งเดียวของรอบ, บน commit สุดท้าย `3f0ca3a1` หลัง `git fetch origin main` ยืนยัน
  `origin/main` = `bc658184` เหมือนตอน merge เข้ากิ่งเซสชัน ไม่ต้อง rebase ซ้ำ):
  **10342 passed, 323 skipped, 19570 subtests passed, 0 failed** ใน 527.87s -- เทสแดงเก่าที่รอบก่อน
  (`w7w30l`) บันทึกไว้ (`test_every_symbol_exemption_is_still_earned`) **เขียวแล้ว** (แก้บน main โดย
  `#772` ของ LANE-E ตามที่ chief `2306` ประกาศ)

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
**ยังศูนย์ทั้งสองชิ้น** -- `#757` ไม่มีจุดเรียก (LANE-B ยังไม่เสียบ `mark_ground_drop_taken`/
`list_ground_drops_still_on_the_ground` เข้า call site จริง, ยืนยันจากใบ `2112` เอง) · class_id
backfill ยังไม่เสียบเข้า `app.py` (รออนุมัติ/ทำโดย chief) ไม่มีอะไรเปลี่ยนบนจอผู้เล่นจากรอบนี้

### 5.2 wire-DB
`pirate-force-server#775` เปิดแล้ว (`claude/brave-goodall-suh0aq` @ `3f0ca3a1`) พร้อม `PF-AUTOMERGE: v4`
-- รอ gate (สถานะตอน push: สอง check run `gate` = `in_progress`, ยังไม่ตัดสิน ≤10 นาทีหลัง push ตาม
`PANYA-DECISION 1158` §22 -- ไม่แดง ไม่เขียว ยัง in_progress; ดู §6 ข้อ GATE_UNVERIFIED)

## 6. nonclaims

1. **ไม่อ้างว่า `#757`/class_id backfill ขึ้น main แล้ว** -- ทั้งคู่อยู่ใน PR `#775` ที่ยังรอ gate
2. **ไม่อ้างว่า class_id backfill ทำงานจริงบนบูตจริง** -- ยังไม่มีจุดเรียกใน `app.py` (ขอ chief แล้ว)
3. **ไม่อ้างว่ารู้ว่า chief จะเลือกใช้ฟังก์ชันนี้หรือเขียน loop เอง** -- เสนอทั้งสองทางในจดหมาย ให้ chief
   เลือก
4. **ไม่แตะ `app.py`, `runtime.py`, `lifecycle.py`, `current/pf_login_game_server_v141.py`** -- โมดูลใหม่
   เรียก `lifecycle.persist_class_id_from_starting_gear` แต่ไม่แก้ไฟล์นั้นแม้แต่บรรทัดเดียว
5. **ไม่อ้างว่าใบ `2112` ผิด** -- ถูกที่ตัวแก้เทสมีอยู่จริง (บนกิ่ง) แค่ยังไม่ถึง main ตอนที่ใบเขียน "ลองใหม่
   ได้ทันที" นี่คือช่องว่างระหว่างเวลาที่ต่างสายวัด ไม่ใช่ความผิดของใคร
6. 🔴 **GATE_UNVERIFIED `#775`** -- push แล้วยังไม่มีผล `gate` ตัดสินก่อนต้องเขียนไฟล์รอบนี้ (สอง check
   run ยัง `in_progress` ที่ ~10 นาทีหลัง push) ตามกติกา `PANYA-DECISION 1158` §22: รอบถัดไปเปิดด้วยการ
   ตรวจ PR `#775` นี้ก่อนอย่างอื่น

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. **ตรวจ `pirate-force-server#775` ก่อนอย่างอื่น** (GATE_UNVERIFIED ข้างบน) -- ถ้าแดง แก้ในรอบนั้นทันที
   ถ้าเขียว/merge แล้ว ไม่ต้องทำอะไรเพิ่ม
3. ตรวจว่า chief ตอบใบ `2357` แล้วหรือยัง (เสียบ `backfill_missing_class_ids` หรือ loop เอง) -- ถ้าเสียบ
   แล้วให้ตรวจ boot log จริง (ถ้ามีเครื่องทดสอบ) ว่าบรรทัด `CHARACTER_CLASS_ID`/`CLASS_ID_BACKFILL_
   SNAPSHOT` ออกจริง
4. ตรวจผล `RE-248` (serializer `0x5DFF60`, ใบ `2212`/`1947`/`2152` -- หน้าเลือกตัวแสดงฉากจริง) --
   ถ้ามาแล้วแก้ `SCENE_FIELD` ใน `persistence_scene_field_patch.py` ตามที่วางแผนไว้ (`w7w30l` §7 ข้อ 3)
5. ถ้ายังไม่มีอะไรใหม่ -- DB กลับไปคิว M4 ปกติ (NOW.md บรรทัด 49: `1101` ล็อกต่อรอ chief แก้ `store=` ที่
   `runtime.py:6443` -- งานสำรองรอบถัดไป: วัด `1101` เป็นรายงานหนึ่งหน้า ตามที่ `1450` ข้อ 6 ยังค้าง)
6. มาร์กกล่องจดหมายด้วย unanchored grep เสมอ
