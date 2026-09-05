# DB round (`j9wwc4`) -- 2026-09-05T13:10+07:00 -> 2026-09-05T13:33+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ** -- อ่าน `NOW.md` ล่าสุดก่อนอื่น (ตรวจล่าสุด 12:48 โดย COO). งานรอบนี้คือคิว DB
หลัง `1044` ตามที่ `COO-DECISION 20260905_1154` ข้อ 3 สั่งไว้ตรง ๆ (ไม่มีบรรทัด M ไหนที่ผมมี
เขตเขียนขยับได้ตรง ๆ รอบนี้ -- M4 หลักยังล็อกที่ `runtime.py:6443`/Door B ของ LANE-B เหมือนเดิม)

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended ตาม `2159` ไม่ใช่ DB)

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยวข้อง -- รอบนี้ไม่แตะโลก/ฉากเลย (persistence เฉพาะของ
ตัวละคร, ไม่มี world registry)

## 1. ล็อกรอบ

- ต้นรอบ list PR หัวข้อ `[LANE-DB]` open ทั้งสองรีโป (ก่อนแตะโค้ด/จดหมายใด ๆ): **ว่างเปล่าทั้งคู่**
  (ตรวจผ่าน `search_pull_requests` ทั้ง `pirate-force-server` และ `pf_bridge`) ไม่มีใบค้าง
  ไม่ต้อง takeover
- ตัดกิ่งจาก `origin/main` สดของทั้งสองรีโป -- กิ่งของเซสชันนี้เอง (`claude/gifted-wright-j9wwc4`
  ของ `pirate-force-server`, `claude/admiring-ride-j9wwc4` ของ `pf_bridge`) เป็นกิ่งที่ระบบให้
  ตอนสร้างเซสชัน อยู่ตรง `origin/main` พอดีตั้งแต่ต้น (ตรวจด้วย `git log origin/main..<branch>`
  = ว่างเปล่าทั้งคู่ ก่อนเริ่ม)
- commit `rounds/DB_20260905_1310_j9wwc4_claim.md` (สามบรรทัด) push แล้วเปิด
  `pf_bridge#1317 [LANE-DB] round j9wwc4: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1317` ของผมเอง ⇒ ไม่แพ้
  ทำงานต่อ

## 2. กล่องจดหมาย

`grep` แบบไม่ยึดตำแหน่งหา `ADDRESSEE: LANE-DB` บนไฟล์ที่ยังไม่มี `.CONSUMED.txt` คู่ ใน
`notes_to_chief/`: เจอ**สองใบ**:

1. `20260905_1154_COO-DECISION-db-takes-no-world-work-home-marker-persistence-row-queued-
   after-1044-LANE-DB.md` -- คำสั่งงานหลักของรอบนี้ (consumed รอบนี้)
2. `20260905_1244_SYNC-NOTICE-pirate-force-server-pr819-closed-never-merged.md` -- เขียนโดย
   `pf_git_sync.ps1` [5d] ไม่ใช่ `ADDRESSEE: LANE-DB` ตามรูปแบบเดิม แต่จ่าหน้าถึงสายนี้โดยตรง
   ในบรรทัดแรกของเนื้อหา (`ADDRESSEE: LANE-DB`) -- นับเป็นกล่องจดหมายจริง (consumed รอบนี้)

อ่านสามใบก่อตั้งสาย (`20260901_1059`/`1100`/`1101`/`1112`) ครบตามกติกา "รอบแรกของเซสชัน"
(เซสชันนี้ไม่มีความจำข้ามรอบ -- เจอในอาร์ไคฟ์ `archive/notes_to_chief_2026-09/`)

อ่านไฟล์รอบล่าสุด `DB_20260905_1153_uhfve8_gt221_fixture_and_gt255_ticket.md` -- ทำต่อจากที่
รอบนั้นทิ้งไว้: `server#819` (GT-221 fixture) เปิดไว้รอเกต, `GT-255` เนื้อใบส่งเป็นจดหมายรอ
chief วาง, `RE-259`/`RE-260` ยืนยันสถานะเดิม -- ทั้งสามตัวมีความคืบหน้าจริงรอบนี้ (ดูข้อ 3)

## 3. ทำอะไร

### 3.1 `server#819` ถูกปิดที่เกต Windows -- กู้ตามใบแจ้ง ไม่เริ่มใหม่

ใบ `1244` (`pf_git_sync.ps1` [5d]) รายงานว่า `server#819` (รอบก่อน `uhfve8`) ถูก**ปิด**เพราะ
`job gate = failure` บน commit `994e72bf` ของกิ่ง `claude/brave-goodall-uhfve8` -- ตรวจ log
งาน `gate` จริง (`run 33946765934`, job id `101254167605`) พบสาเหตุตรงตัว:

```
1 failed, 9895 passed, 95 skipped, 18114 subtests passed in 1453.40s
FAILED ListRosterWritesNothingButTheAccountTests::test_listing_an_existing_account_changes_nothing
PermissionError: [WinError 32] The process cannot access the file because it is being
used by another process: '...\\Temp\\tmps6cqi4q7\\run_gt221_20260905_000000.sqlite3'
```

สาเหตุจริง: เทสตัวนั้นเปิด `sqlite3.connect(str(self.path)).execute(...)` สองครั้งแบบ ad-hoc
ไม่เคย `.close()` เลย -- ไม่มีพิษบน Linux (แซนด์บ็อกซ์รอบก่อนรันผ่านจริง 10848/0 failed) แต่
Windows ล็อกไฟล์ค้างจนกว่า connection จะถูกปิด ทำให้ `TemporaryDirectory.cleanup()` unlink
ไม่ได้ -- เป็นบั๊ก platform-specific ที่ sandbox บนคลาวด์นี้พิสูจน์ไม่ได้ล่วงหน้า (ไม่มี Windows)

**ทำตามที่ใบแจ้งสั่งตรงตัว: ไม่เริ่มรอบใหม่** -- ดึงเนื้อไฟล์ทั้งสอง
(`persistence_gt221_fixture.py`, `test_persistence_gt221_fixture.py`) จาก
`origin/claude/brave-goodall-uhfve8` (commit `994e72bf`) แบบ verbatim ขึ้นกิ่งของรอบนี้เอง
(เซสชันนี้ push เข้ากิ่งของเซสชันก่อนไม่ได้ -- ระบบให้กิ่งใหม่ทุกเซสชัน) แล้วแก้จุดเดียว: เพิ่ม
helper `_raw_vitals(path, character_id)` ที่ปิด connection ใน `finally` (รูปแบบเดียวกับที่
`tests/test_persistence_ground_drops_010.py`'s `_raw_rows` ใช้อยู่แล้วทั้งไฟล์) แทนที่สอง
inline connect เดิม -- ไม่เปลี่ยนว่าเทสพิสูจน์อะไร (query เดิมทุกตัวอักษร) รันไฟล์นี้เดี่ยว ๆ
20/20 ผ่าน

### 3.2 งานหลักของรอบ (`COO-DECISION 20260905_1154` ข้อ 3(ข)): ประตู persistence ของ home marker

R317 (`notes_to_chief/20260905_1125_KA1A-R317-RESULTS-*.md`) วัดจริงบนจอ: เลือกตัวเลือก 2
ที่ Columbus (quest 3205, Q_BORNAGAIN) เซิร์ฟพิมพ์
`COLUMBUS_QUEST3205_BORNAGAIN_REFUSED reason=no_home_marker_persistence_row_evidence` ทุกครั้ง
-- ตรวจ `src/pirateforce_foundation/columbus_quest_dispatch.py` (ไฟล์ของ LANE-A) ตรงกับที่
คิดไว้: `dispatch_columbus_quest3205` refuse **ไม่มีเงื่อนไข** ด้วยเหตุผลตรงตัวจาก docstring
ของมันเอง -- "no persisted column anywhere in this project's schema for a player-chosen
respawn scene" -- และบอกไว้แล้วว่า "Wiring ... is NOT done here -- that file is the chief's".

ไฟล์ใหม่ทั้งคู่ + method ใหม่ใน `store.py` (เขตเขียนของสาย ไม่แตะ `runtime.py`/
`columbus_quest_dispatch.py`):

- `migrations/013_character_home_marker.sql` -- ตารางใหม่หนึ่งตาราง
  `character_home_marker(character_id PK REFERENCES characters(id) ON DELETE CASCADE,
  home_scene_id INTEGER NOT NULL, updated_at TEXT NOT NULL)` -- ไม่มี backfill ไม่มี default
  ทุกตัวละครมี 0 แถวจนกว่าจะมีคนเรียก `set_home_marker` (ไม่เดาฉากไหนทั้งนั้น ตามคำสั่งเจ้าของ
  ใบ 1059) -- ตรวจเลขชนก่อนสร้าง: `git fetch origin` แล้ว `ls migrations/` บน `origin/main` สด
  = ล่าสุดคือ `012` ไม่มี PR `[LANE-DB]` เปิดค้างในเลข `013` (ไม่มีใบ `[LANE-DB]` เปิดเลย) และ
  `rounds/DB_*.md` ล่าสุดไม่มีใครอ้างว่าทำ `013` ไปแล้ว ⇒ ปลอดภัย
- `src/pirateforce_foundation/persistence_home_marker.py` -- `HomeMarkerRow` (dataclass เดียว
  กับที่ `persistence_ground_drops.GroundDropRow` วางแบบไว้)
- `store.py`: `set_home_marker(character_id, home_scene_id)` -- upsert
  (`INSERT ... ON CONFLICT(character_id) DO UPDATE`) เพราะ quest 3205 กดซ้ำได้ ตรวจตัวละครมีจริง/
  ไม่ soft-deleted ในธุรกรรมเดียวกับการเขียน (`BEGIN IMMEDIATE`) raise `KeyError` ถ้าไม่มี ตรวจ
  `home_scene_id` เป็น int ในช่วง `0..0xFFFF` (ช่วงเดียวกับ `character_positions.scene_id` ที่
  `save_position` ใช้อยู่แล้ว) อ่านกลับหลังเขียนในธุรกรรมเดียวกัน ·
  `get_home_marker(character_id)` -- อ่านอย่างเดียว คืน `None` ถ้ายังไม่เคยตั้ง (ไม่เดาเป็น
  ศูนย์หรือฉากไหน)
- `tests/test_persistence_home_marker.py` -- 26 เคส (shape ของ migration, upsert-in-place ไม่
  สร้างแถวซ้ำ, สองตัวละครแยกกันจริง, รอดการเปิดไฟล์เดิมใหม่ (ครึ่งหนึ่งของ "รอด relog" ที่ระดับ
  storage), validation ครบ)

**`pf-adversary` (เรียกพร้อมเริ่มงาน 3.2 ตามกติกาใหม่ `COO 0903_2345`/`1428`)**: ตรวจทั้งสอง
ชิ้น (home marker ใหม่ + การกู้ `#819`) -- **ไม่พบข้อบกพร่องจริง** หลังพิสูจน์จริงสามข้อ ไม่ใช่
สมมุติ: (1) แข่ง 200 รอบระหว่าง thread จริงสองตัว (`set_home_marker` ปะทะ
`soft_delete_character` ตัวละครเดียวกัน) = ศูนย์ความผิดปกติ เพราะทั้งคู่ล็อกด้วย `BEGIN
IMMEDIATE` บน connection ใหม่จาก `self.connect()` แต่ละครั้ง (2) `ON CONFLICT` syntax ถูกต้อง
ทดสอบจริงสองครั้งติดกัน แถวเดียว `updated_at` ขยับ (3) FK CASCADE ยิงจริงเมื่อ hard-delete แถว
`characters` ผ่าน `store.connect()` (ทางเดียวที่โค้ด production ใช้) -- ข้อสังเกตเดียวที่ยกมา
(ไม่ใช่บั๊ก): ถ้าวันหน้ามีทาง hard-delete ที่ข้าม `PRAGMA foreign_keys=ON` แถว marker จะลอย
กำพร้าเงียบ ๆ -- ไม่มีทางแบบนั้นอยู่จริงวันนี้ (grep ทุก `sqlite3.connect(` ใน `src/` แล้ว)
ไม่ใช้ `ADVERSARY_PENDING` เพราะผลคืนก่อน push จริง

### 3.3 CORE-REQUEST ถึงจุดเสียบเดียว (chief/LANE-A, ไฟล์ของพวกเขาไม่ใช่ของผม)

ประตูฝั่งผมพร้อมแล้ว แต่ยังไม่มีใครเรียก -- `runtime.py`/`columbus_quest_dispatch.py` เป็นไฟล์
ของ LANE-A/chief ตามเขตเขียนของสายนี้ (`COO-DECISION 20260901_1100`) ส่ง CORE-REQUEST ระบุ
จุดแก้ตรงเดียว (`dispatch_columbus_quest3205` เพิ่ม `character_id`/`store` แล้วเรียก
`store.set_home_marker(character_id, 1)` แทนการ refuse ไม่มีเงื่อนไข -- `1` = Port Royal ตาม
`/warp 1` ที่ `GT-245` ยืนยันแล้ว R317) ระบุชัดว่า**ไม่ครอบคลุม**ส่วน wire-ack ที่ docstring
เดิมพูดถึง (คนละช่องว่าง คนละใบ RE) -- เนื้อใบ GT ("กดตัวเลือก 2 ที่ Columbus แล้วฐานทัพ = Port
Royal รอด relog") **เลื่อนส่ง**จนกว่าจุดเสียบขึ้น main (รันไม่ได้ก่อนหน้านั้น ไม่มีประโยชน์ตั้ง
เนื้อใบก่อน -- อธิบายเหตุผลไว้ในจดหมายเอง)

### 3.4 พ่วง: สี่ pin ที่ขยับตามไฟล์ migration ใหม่ (ตามกติกาที่มีอยู่แล้ว)

ชุดเต็มรอบแรก (ก่อนแก้) พบ **4 แดง** ทั้งหมดเป็น pin ที่ผูกกับจำนวน/รายชื่อไฟล์ migration ตรง ๆ
(ไม่ใช่ regression ของโมดูลอื่น -- ทุกอันมีคอมเมนต์ของตัวเองบอกไว้ล่วงหน้าว่า "pin นี้ขยับตาม
ไฟล์ migration ใหม่ทุกไฟล์" อ้างใบ `20260901_1416`/`20260901_1459` ที่ให้สายนี้ bump ได้บรรทัด
เดียว):

1. `test_foundation.py::test_upgrade_from_original_foundation_schema` -- ลิสต์เวอร์ชัน
   `[1..12]` → `[1..13]`
2. `test_item_move_capture.py::test_modes_and_explicit_existing_database_are_fail_closed` --
   `COUNT(*) FROM schema_migrations` คงที่ `12` → `13`
3. `test_npc_interaction_wire.py::test_store_schema_owns_no_quest_shop_or_reward_table` --
   `EXPECTED_TABLES` เพิ่ม `"character_home_marker"` (คอมเมนต์อธิบายเหตุผลเดียวกับที่
   `ground_drops`/`character_skills` มีอยู่แล้ว)
4. `test_persistence_speed_walk_seed_008.py::test_a_snapshot_is_due_while_008_is_the_pending_file`
   -- `pending_versions` คงที่ `[8,9,10,11,12]` → `[8,9,10,11,12,13]` (คอมเมนต์เดิมของไฟล์นี้
   เขียนไว้ตรง ๆ ว่า "a thirteenth file nobody looked at" -- คือรอบนี้เอง)

แก้ทั้งสี่ รันแยกไฟล์ยืนยัน 4/4 ผ่าน ก่อนรันชุดเต็มรอบสอง (ดู §4)

### 3.5 จดหมายที่ส่ง (รอบเดียว)

1. `20260905_1311_LANE-DB-CORE-REQUEST-home-marker-door-now-exists-wire-quest3205.md`
   (ADDRESSEE: chief, cc COO/LANE-A/Panya)
2. stub `.CONSUMED.txt` ของใบ `1154`
3. stub `.CONSUMED.txt` ของใบ `1244` (sync-notice)

## 4. ชุดเทสของรอบ

ระหว่างทำ: `pytest tests/test_persistence_home_marker.py tests/test_persistence_gt221_fixture.py
tests/test_persistence_login_vitals.py -q` หลายครั้งระหว่างแก้ (ไฟล์สุดท้าย 38/38 ผ่าน + seam-scan
ของสายอื่นไม่แดง) ไม่รันชุดเต็มระหว่างทาง

ชุดเต็ม **สองครั้งในรอบนี้ (เกินหนึ่งครั้ง -- เหตุผลตามกติกา)**: ครั้งแรกบนต้นไม้ที่ merge
`origin/main` แล้ว (หลังผล adversary กลับมาว่าไม่พบข้อบกพร่อง) = **4 failed, 10898 passed, 323
skipped** -- ทั้งสี่คือ pin ไฟล์ migration ที่อธิบายไว้ใน §3.4 ไม่ใช่ regression ของโมดูลอื่น
(อ่าน traceback ยืนยันทีละตัวก่อนตัดสินใจแก้) แก้ครบ + `git fetch origin main` ซ้ำ (พบ main ขยับ
อีกสองครั้งระหว่างรอบ: `#821`, `#822` -- ตรวจ `git diff --stat` กับทุกไฟล์ที่รอบนี้แตะ = ไม่ชนกัน
ทั้งสองครั้ง merge fast-forward สะอาด) ครั้งที่สองบน commit สุดท้ายจริงที่ push:
**10913 passed, 0 failed, 323 skipped, 20212 subtests passed (523.56s)**

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
**ศูนย์** -- รอบนี้เป็นประตูฝั่งเซิร์ฟเวอร์ (migration + store methods) ไม่มีจุดเรียกจริงจนกว่า
CORE-REQUEST ข้อ 3.3 จะขึ้น main ไม่มีอะไรถึงจอผู้เล่นเองในรอบนี้

### 5.2 wire-DB
`pirate-force-server#823` (`claude/gifted-wright-j9wwc4`) -- **เปิดแล้ว 13:3x+07 พร้อม
`PF-AUTOMERGE: v4` รอเกต Windows** (สถานะ ณ ตอนเขียนไฟล์นี้ ยังไม่เห็นผล `merged: true`) หนึ่ง
คอมมิต ผ่านชุดเต็มตาม §4 ทั้งสองครั้ง (ครั้งที่สองคือ commit ที่ push จริง) · `pf_bridge#1317`
claim -- เติม marker ทันทีหลังไฟล์นี้ + จดหมาย + stub ขึ้นกิ่งเดียวกัน (ข้อ 7)

## 6. nonclaims

1. **ไม่อ้างว่า `pirate-force-server#823` ขึ้น main แล้ว** -- เปิดรอเกต ตามกฎ §22 (`1158`) ต้อง
   อ่านผล job `gate` ของรอบ `pull_request` เอง แต่รอบนี้จบก่อนเกตรันเสร็จ (เขียนตามจริง ไม่รอ)
2. **ไม่อ้างว่า quest 3205 หยุด refuse แล้ว** -- ประตู persistence พร้อม แต่ยังไม่มีจุดเรียก
   (CORE-REQUEST รอ chief/LANE-A) ไม่มีอะไรในรอบนี้พิสูจน์ว่า
   `COLUMBUS_QUEST3205_BORNAGAIN_REFUSED` จะหยุดพิมพ์ -- pf-adversary ชี้ประเด็นเดียวกันตรง ๆ
3. **ไม่อ้างว่า `GT-221`/`GT-255` PASS แล้ว** -- `GT-221` ยังเป็นใบ attended ที่ยังไม่รัน
   (READY เมื่อ `#823` merge) `GT-255` ยังรอ chief วางเนื้อใบ ไม่ใช่งานรอบนี้
4. **ไม่อ้างว่าการกู้ `#819` เท่ากับ `#819` เอง** -- เป็น PR ใหม่ (`#823`) จากกิ่งใหม่ ของ
   session นี้ ตามที่ sync notice สั่ง ("recover them from that branch by hand") ไม่ใช่การเปิด
   `#819` ซ้ำ
5. **ไม่แตะ `store.py` ของเดิม (เฉพาะเพิ่ม method ใหม่), `runtime.py`,
   `columbus_quest_dispatch.py`, `app.py`, `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`,
   `current/pf_login_game_server_v141.py`** -- ไฟล์ที่แก้จริงคือของใหม่สองไฟล์ + `store.py`
   (เพิ่ม method) + สี่ pin ใน tests/ ที่มีอยู่แล้ว
6. **ไม่อ้างว่า `1101` (M4 หลัก) ปลดล็อกแล้ว** -- ยังล็อกที่ `runtime.py:6443`/Door B ของ
   LANE-B เหมือนเดิม ไม่มีสัญญาณใหม่รอบนี้ (คนละเรื่องกับ home marker แม้จะมีเลขบรรทัดใกล้กัน)

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจผลเกตของ `pirate-force-server#823` ก่อนอื่น -- ถ้าแดง แก้ในรอบนั้นทันที (โดยเฉพาะเช็ค
   ว่าไม่มี ad-hoc `sqlite3.connect` ไม่ปิดตัวอื่นหลงเหลืออยู่ที่ sandbox Linux มองไม่เห็น)
3. ตรวจว่า chief/LANE-A รับ CORE-REQUEST ข้อ 3.3 หรือยัง (ไม่บล็อกใคร ไม่ต้องทวงจนกว่าจะเกิน
   deadline ปกติของสาย)
4. ถ้าจุดเสียบขึ้น main แล้ว: ส่งเนื้อใบ GT ("กดตัวเลือก 2 ที่ Columbus แล้วฐานทัพ = Port Royal
   รอด relog") ตามที่ `1154` ข้อ 3(ข) สั่ง
5. ไม่มีใบใหม่ถึง LANE-DB รอบหน้า: กลับไปหาใบ chief/COO ที่ cc ถึง LANE-DB ย้อน 12 ชม. ก่อน
   ประกาศ "ไม่มีงาน" หรือหยิบคิว "COO-ORDER 0329" ชิ้น 3/4/5 ที่ยังไม่ปิด
6. มาร์กกล่องจดหมายด้วย unanchored grep เสมอ (รอบนี้พบว่า sync-notice จาก `pf_git_sync.ps1`
   ก็นับเป็นกล่องจดหมายจริงแม้ไม่ผ่าน pattern `ADDRESSEE:` ตรงหัวไฟล์ตามชื่อไฟล์ -- มันอยู่ใน
   บรรทัดแรกของเนื้อหาแทน ตรวจให้ครบทั้งสองแบบ)
