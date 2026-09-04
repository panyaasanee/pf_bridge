# DB round (`qinqve`) -- 2026-09-05T02:35+07:00 -> 2026-09-05T02:58+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับขั้น M** -- นี่ไม่ใช่ milestone gate เป็นการแก้บั๊กบูตแตกที่ค้นพบระหว่างการเทส `GT-247` (ka1-A, ใบ
`0233`) ซึ่งไม่ใช่งานของบันได DB โดยตรง แต่เป็นบั๊กแตกที่กระทบ `main` ทั้งสาย (ทุกใบ attended ที่ใช้
`--scene-load-scenario` บูตไม่ได้) ที่อยู่บนพรมแดนเขตเขียนของสายนี้ (จุดเรียกเป็นของ chief ใน `app.py`
แต่จุดที่แก้ได้อยู่ในเมธอดของสายนี้เองใน `store.py`) -- ไม่มีข้อ NOW บรรทัดไหนพูดถึงเรื่องนี้ตรง ๆ ให้ขยับ

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended ตาม `2159` ไม่ใช่ DB)

## 1. ล็อกรอบ

- 02:35+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่มีใครต้องปลดล็อก ไม่ใช่ takeover
- กิ่งเซสชันทั้งสองรีโป (`claude/brave-goodall-qinqve` server, `claude/admiring-johnson-qinqve` bridge)
  ที่ระบบตั้งชื่อให้ -- **ทั้งสองกิ่งเดิมถูก merge หมดแล้วก่อนรอบนี้เริ่ม** (`claude/admiring-johnson-qinqve`
  = tip ของ `pf_bridge` main `30fb4fc2` เป๊ะ, `claude/brave-goodall-qinqve` = tip ของ
  `pirate-force-server` main `67ac2f0c` เป๊ะ) ⇒ รีเซ็ตทั้งสองกิ่งจาก `origin/main` สดก่อนเริ่ม (ไม่ใช่
  takeover, ไม่มีงานเก่าค้างอยู่บนกิ่งเดิมให้กู้)
- commit `rounds/DB_20260905_0235_qinqve_claim.md` push แล้วเปิด `pf_bridge#1243 [LANE-DB] round
  qinqve: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1243` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ

## 2. กล่องจดหมาย

`grep -q "ADDRESSEE: LANE-DB"` (unanchored) บน `origin/main` สดของ `pf_bridge` ต้นรอบ -- **ว่างเปล่า**
ไม่มีใบค้าง

ระหว่างรอบ (หลัง claim push) `pf_git_sync` [6b] ซิงก์ไฟล์ใหม่จากเครื่อง Panya เข้า `origin/main` หลายรอบ:
`20260905_0233_KA1A-R314-RESULTS-...boot-crash-class-id-backfill.md` (ADDRESSEE: chief, cc LANE-DB
ในหัวข้อ 3), `20260905_0234_SYNC-ALARM-...` (ไม่เกี่ยวกับสายนี้ -- สามใบของ LANE-GM/LANE-A/chief-to-A),
และชุด COO-DECISION `0247`-`0251` ซึ่งใบ `0250` (ADDRESSEE: chief, cc LANE-DB) ตัดสินเรื่องเดียวกับที่
ผมกำลังแก้อยู่พอดี -- ดู §3.2 ไม่มีใบไหนใน batch นี้จ่าหน้าตรงถึงสายนี้ (ADDRESSEE: LANE-DB) จึงไม่สร้าง stub
`.CONSUMED.txt` ให้ใบไหนเลย (สงวนไว้สำหรับใบที่จ่าหน้าตรงเท่านั้น) ตอบด้วยใบ `0254` (§3.1) และ `0258`
(§3.2)

## 3. ทำอะไร

### 3.1 แก้บั๊กบูตแตก `main` -- `sqlite3.OperationalError: no such column: class_id`

ka1-A รายงานสด (`GT-247` R314, ใบ `0233` หัวข้อ 3): `main` head บูต `--scene-load-scenario` ไม่ได้เลย
ตั้งแต่ `7717c747` (17:51Z) -- `app.py:802` เรียก
`persistence_class_id_backfill.backfill_missing_class_ids(store)` ไม่มีเงื่อนไขหลัง if/else ที่กิ่ง
`scene_load` (การออกแบบตั้งใจของ chief เอง, `migrations/006_character_typed_attribute_columns.sql`'s
commit message + `tests/test_startup_stale_lease_recovery.py::
test_the_scene_load_branch_is_the_one_deliberate_exception`) ไม่เรียก `store.migrate_with_backup()`
เลย ⇒ DB ก่อน migration 006 ไม่มีคอลัมน์ `class_id` บูตชนแตก

`app.py` เป็นเขตเขียนของ chief -- แก้ทั้งหมดฝั่งของสายนี้แทน:

- `src/pirateforce_foundation/store.py`: `list_character_ids_missing_class_id` (เมธอดใหม่ของสายนี้เอง,
  `git log -S"def list_character_ids_missing_class_id"` ยืนยันมีแค่ commit เดียวที่แตะนิยาม คือ
  `caea4f47` รอบ `b0ede7` ของสายนี้ -- ไม่ใช่เมธอดเดิมที่ charter ห้ามเปลี่ยน) เช็ก
  `PRAGMA table_info(characters)` ก่อน คืน `()` ทันทีถ้ายังไม่มีคอลัมน์ `class_id` แทนการรัน `SELECT` ที่จะ
  ชน DB ที่ migrate แล้วไม่ถูกแตะเลย (คอลัมน์มีอยู่แล้วเสมอ กำแพงไม่ทำงาน) พฤติกรรมเดิมไบต์ต่อไบต์เหมือนเดิม
- `tests/test_persistence_class_id_backfill.py`:
  `test_a_database_that_predates_migration_006_does_not_crash_the_boot` (จำลองด้วย
  `ALTER TABLE characters DROP COLUMN class_id` บน DB migrate ครบแล้ว -- สโตร์นี้ไม่มีจุดเข้า "migrate ถึง
  เวอร์ชัน N" ให้หยุดครึ่งทาง)
- `tests/test_persistence_typed_attr_columns.py`:
  `test_a_database_missing_the_class_id_column_reports_empty_not_a_crash` (เทสระดับเมธอดของ `store.py`
  ตรง ๆ)

**mutation test เอง (ก่อนเรียก adversary)**: ถอด guard ชั่วคราว (`git stash`) รันสองเทสใหม่ -- ทั้งคู่แดงด้วย
`sqlite3.OperationalError: no such column: class_id` ตัวเดียวกับที่รายงานจริงเป๊ะ (ไม่ใช่เทสผ่านลอย ๆ)
ใส่ guard กลับเขียวทั้งคู่

**`pf-adversary` เรียกครั้งเดียว**: **GO** ไม่พบข้อบกพร่อง -- เพิ่มเติมจากที่ผมทำเอง: จำลองซ้ำด้วยการบูต
`python -m pirateforce_foundation.app --scene-load-scenario ...` ตัวจริงบน DB ก่อน migration 006 จริง
(ไม่ใช่แค่ unit test) ยืนยัน traceback ตรงกับรายงานเป๊ะทั้งไฟล์:บรรทัด, ยืนยันด้วย `git log -S` ว่าเมธอดที่
แก้เป็นของสายนี้เองจริง, grep ยืนยันไม่มีผู้เรียกอื่นของเมธอดนี้ที่จะแปลกใจกับพฤติกรรมใหม่, ให้เหตุผล PRAGMA/
SELECT race แล้วสรุปว่าไปไม่ถึงในโปรดักชัน (ไม่มีโค้ดไหนรัน `DROP COLUMN` เลย ทิศทางเดียวที่เป็นไปได้คือ
ไม่มี→มี ซึ่งไม่เป็นอันตราย) เปิดประเด็นค้างสองข้อ (ดู §6 nonclaims)

ตอบกลับ chief/COO/ka1-A/ka1-B/LANE-B ด้วยใบ
`notes_to_chief/20260905_0254_LANE-DB-FIX-class-id-backfill-scene-load-boot-crash-server-783-open.md`
(push+PR เปิดเวลา **02:54:04+07**)

### 3.2 🔴 ชนกับคำตัดสินของ COO ที่ออกก่อนหน้า 4 นาที -- ถืออัตโนมัติ merge ไว้ก่อน ถามแทนตัดสินเอง

`git merge origin/main` เข้ากิ่ง `pf_bridge` (หลัง push `#783` ไปแล้ว) ดึงใบ
`20260905_0250_COO-DECISION-...class-id-backfill-before-migrate-fix-first-chief.md` เข้ามาด้วย --
เวลา **02:50+07** (ก่อนผม push `#783` 4 นาที ค้นพบบั๊กเดียวกันจากใบต้นทางเดียวกันพร้อมกันโดยไม่รู้ตัว)
COO ตัดสินว่า **เจ้าของ = chief** (`app.py`) เป็นงานแรกของ chief รอบ 02:51 เดดไลน์ escalation 04:21 และ
เขียนชัดว่า **"โมดูล backfill ของ DB ไม่ต้องแตะ"**

ตัวแก้ของผมไม่ใช่บั๊ก (adversary GO) และอยู่ในเขตเขียนของสายนี้ล้วน ๆ แต่ COO ตัดสินเรื่องเจ้าของงานนี้ไปแล้ว
สด ๆ ก่อนหน้าไม่กี่นาที -- การปล่อยให้ `#783` automerge เอง หรือถอนเองเงียบ ๆ ทั้งสองทางเป็นการตัดสินใจแทน
COO ในเรื่องที่ COO เพิ่งเคาะไป จึงหยุดแล้วถามแทนเดา (วินัย "ติดอะไรเกินอำนาจ...เขียนใบถึง COO ทันที
อย่าตัดสินเอง อย่ารอข้ามรอบ"):

- **ถอด `PF-AUTOMERGE: v4` ออกจาก body ของ `pirate-force-server#783`** ทันที (ระบบจะไม่ merge เองแล้ว)
- เขียนใบ `notes_to_chief/20260905_0258_LANE-DB-ASK-COO-independent-fix-already-pushed-before-seeing-0250-keep-or-withdraw.md`
  ถาม COO ว่าจะเก็บ `#783` ไว้คู่กับตัวแก้ของ chief (defense-in-depth คนละไฟล์คนละกลไก) หรือถอน
- **claim PR `#1243` ของรอบนี้ก็ยังไม่เติม marker เช่นกัน** (รอบล็อกยังไม่ปลด -- ดู §7)

## 4. ชุดเทสของรอบ

- ระหว่างทำงาน: `tests/test_persistence_typed_attr_columns.py tests/test_persistence_class_id_backfill.py`
  (100 passed, 340 subtests) เขียวทุกครั้งที่รัน (รวมก่อน/หลัง merge `origin/main` เข้ากิ่ง)
- ชุดเต็ม (ครั้งเดียวของรอบ, บน commit สุดท้าย `d5e6035f` -- merge `origin/main` `f71cb9ae` เข้ากิ่งแล้ว
  ก่อนรัน): **10406 passed, 323 skipped, 19589 subtests passed, 0 failed** ใน 403.80s -- ไม่มีเทสแดงเก่า
  ค้างจากรอบก่อน

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
**ยังศูนย์สำหรับสายนี้โดยตรง** -- ผลที่จอผู้เล่นเห็นได้ (บูต `--scene-load-scenario` ผ่านแล้วรัน GT ต่อได้)
เป็นของ ka1-A รอบทดสอบถัดไป ไม่ใช่ของรอบนี้ **แต่หลักฐานที่ pf-adversary เก็บเป็นชั้น process-observable**
(exit code 0 ของ `python -m pirateforce_foundation.app --scene-load-scenario ...` ตัวจริงบน DB ก่อน
migration 006 จริง เทียบกับ exit ล้มก่อนแก้) ใกล้เคียง client-observable กว่า unit test เฉย ๆ

### 5.2 wire-DB
`pirate-force-server#783` เปิดแล้ว (`claude/brave-goodall-qinqve` @ `d5e6035f`) **ไม่มี `PF-AUTOMERGE: v4`
ตั้งใจ** -- ถืออัตโนมัติ merge ไว้ก่อนจนกว่า COO จะตอบใบ `0258` (ดู §3.2) 🔴 **GATE_UNVERIFIED `#783`**
เพิ่มเติม -- push แล้วยังไม่ตรวจผล `gate` job ที่ตอนเขียนไฟล์รอบนี้ (รอบถัดไปเปิดด้วยการตรวจ PR นี้ก่อน
อย่างอื่นตาม `PANYA-DECISION 1158` แม้จะไม่มี marker ก็ตาม -- แดงต้องแก้เหมือนกัน)

## 6. nonclaims

1. **ไม่อ้างว่าเลือกทางแก้ (ก) ที่ ka1-A เสนอ** ("ย้าย backfill เข้าไปหลัง migrate_with_backup() ทั้งสองกิ่ง")
   -- เลือกทาง (ข) "guard ด้วยมีคอลัมน์ไหม" เพราะ (ก) ต้องแก้ `app.py` นอกเขตเขียนของสายนี้
2. **ไม่ปิดประเด็นที่ pf-adversary เปิดค้าง**: DB ที่บูตผ่าน `--scene-load-scenario` ตลอดชีวิตไม่เคยเรียก
   `migrate_with_backup()` เลย ⇒ `class_id` ของตัวละครในนั้น NULL ตลอดไปโดยออกแบบ -- ถามไปในใบ `0254` แล้ว
   ยังไม่มีคำตอบ
3. **ไม่แตะปัญหาข้างเคียง**: teardown script ที่ query `hp_current` บน DB ก่อน migrate (nonclaims บรรทัด
   สุดท้ายของใบ `0233`) เป็นปัญหาเดียวกันแต่คนละไฟล์คนละเขต ไม่ใช่ของรอบนี้แก้
4. **ไม่แตะ `app.py`, `runtime.py`, `current/pf_login_game_server_v141.py`, `lifecycle.py`** ตามข้อห้ามเดิม
5. **ไม่ทำงานคิว M4/`1101`/piece 2/piece 3 ตามลำดับปกติของสาย** -- รอบนี้ทั้งหมดไปกับบั๊กบูตแตกข้างต้นเพราะ
   กระทบ `main` ทั้งสาย (ทุกใบ attended ตระกูล `--scene-load-scenario`) ถือเป็นลำดับความสำคัญเหนือคิวปกติ
   ไม่ใช่ "หาเรื่องทำนอกเขต" (อยู่ในเขตเขียนของสายนี้ทั้งหมด, ตอบจดหมายที่ cc มาให้)
6. **ไม่อ้างว่า `#783` merge แล้ว** -- เปิดอยู่ รอ gate + รอคำตอบ COO (ดู §5.2/§3.2)
7. **ไม่อ้างว่ารอบนี้ปลดล็อก `#1243`** -- claim PR ยังไม่เติม `PF-AUTOMERGE: v4` ตั้งใจ (§3.2) -- รอบนี้จบ
   แบบ "เสร็จแล้วแต่ไม่ได้ปลด" ของจริง ไม่ใช่ลืม

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. **ตรวจใบ `20260905_0258` (ASK COO) ก่อนอย่างอื่น** -- ถ้า COO ตอบแล้ว:
   - "เก็บไว้" ⇒ เติม `PF-AUTOMERGE: v4` กลับเข้า body ของ `pirate-force-server#783` แล้วเติม marker ให้
     claim PR `#1243` ของรอบนี้ (ปลดล็อก) ตามลำดับ
   - "ถอน" ⇒ ตามคำสั่ง COO ว่าใครปิด `#783` (สายนี้ห้ามปิด PR เอง) แล้วเติม marker ให้ `#1243` ปลดล็อก
   - ยังไม่ตอบ ⇒ ตรวจ `#783` ว่า gate เขียว/แดงยังไง (แก้ถ้าแดง) แล้วรอต่อ ไม่ปลด `#1243`
3. ตรวจว่า chief ตอบใบ `0254` แล้วหรือยัง (โดยเฉพาะคำถามค้าง: DB ตระกูล scene-load-only ไม่เคย backfill
   class_id เลยโดยออกแบบ เป็นปัญหาจริงไหม)
4. ตรวจว่า chief ตอบใบ `2357` แล้วหรือยัง (class_id backfill one-line hookup ค้างจากรอบ `suh0aq` --
   ยังไม่มีเลยตอนต้นรอบนี้ `grep` บน `app.py` สดว่างเปล่า) -- หมายเหตุ: ถ้า chief เดินตาม `0250` แล้ว
   hookup นี้อาจถูกแก้ไปพร้อมกันในทีเดียว ตรวจ `app.py` สดก่อนเขียนซ้ำ
5. ถ้ายังไม่มีอะไรใหม่ -- DB กลับไปคิว M4 ปกติ (NOW.md บรรทัด 49: `1101` ล็อกต่อรอ chief แก้ `store=` ที่
   `runtime.py` -- วัดซ้ำรอบนี้แล้วไม่เปลี่ยน (`0 store=` sites ใน `runtime.py` สดของรอบนี้), เป็น hold
   ที่ COO อนุมัติเองแล้ว (ใบ `0103`) ไม่ใช่บั๊ก -- ไม่ต้องวัดซ้ำอีกจนกว่ามีสัญญาณใหม่จาก LANE-B/Door B)
6. มาร์กกล่องจดหมายด้วย unanchored grep เสมอ
