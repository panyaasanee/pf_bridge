# GM รอบ `hw6dix` -- 2026-09-02T01:29+07:00

## NOW.md -- อ่านเป็นไฟล์แรก (ตรวจสดรอบนี้)

แก้ไขล่าสุด 2026-09-01 21:54+07 โดย COO · "รอ Panya ติ๊ก" = **ว่าง** · "งานด่วนตอนนี้" ยังมี 3 ข้อ

| ข้อ | เขตสายนี้ไหม | รอบนี้ |
|---|---|---|
| P-1 ของดรอปค้างพื้น | ไม่ (สาย A/B) | ไม่แตะ |
| P-2 สีชื่อมอนสเตอร์ | ไม่ | ไม่แตะ |
| P-3 ปุ่ม GM กดแล้วใช้ได้จริง | **ใช่** | ไม่ขยับ -- ดูเหตุผลด้านล่าง |
| GM-A `/warp` ข้ามแมพ | ใช่ | โค้ดจบแล้ว รอ Panya รัน `GT-192` (กฎ NOW.md บรรทัด 19-21: ไม่ใช่ตัวบล็อก) |
| GM-B `/speed` | **ใช่** | **ขยับรอบนี้ -- งานหลัก ดูหัวข้อ 4** |
| UI-A / UI-B / census latch | ไม่ | ไม่แตะ |

**รอบนี้ขยับ NOW ข้อไหน: GM-B** (`/speed`) -- เงื่อนไข (b) ของ `GT-193` ปิด
**ข้อที่ไม่ขยับและเพราะอะไร:**
- **P-3** -- ตรวจสดรอบนี้ ไม่ copy จากรอบก่อน: `grep` `GAME_TEST_QUEUE.md` หา
  `GameMaster.dll`/`BT_GM`/`GMUI`/`P-3` = เจอเฉพาะใบเก่า (GT-107-R3, GT-164) ไม่มีใบใหม่ ·
  `grep notes_to_chief/` หา `CHIEF-REPLY`/`ADDRESSEE: LANE-GM` ใหม่เรื่องนี้ = ไม่มี
  ⇒ **ว่างเพราะรอ chief มอบสาย RE ต่อจาก `RE-104`** (ซอร์ส `GameMaster.dll` สายนี้ส่งครบแล้ว
  รอบ `ku3jz6`/r2, PR #760 merge แล้ว) สายนี้ไม่มีของทำต่อกับ P-3 จนกว่าจะมีใบ
- **P-1/P-2/UI-A/UI-B/census latch** -- ไม่ใช่เขตเขียนของสายนี้

## 1. ล็อกรอบ

`list_pull_requests(state=open)` ทั้งสอง repo = **ว่างทั้งคู่** (ไม่มี PR เปิดค้างของสายไหนเลย)
⇒ ยึดล็อก: empty commit `round claim: hw6dix` + draft PR ตั้งแต่วินาทีแรก
`pf_bridge` **#777** · `pirate-force-server` **#523** (หัวข้อ `[LANE-GM] WIP round claim hw6dix`)

## 2. ชะตา PR รอบก่อน (ADDENDUM v2 ข้อ A)

รอบก่อน = `3avy0t` (`pf_bridge#775` / `pirate-force-server#521`)
`list_pull_requests` คืน `merged:false` ให้ทุกใบ -- **ค่านี้ไม่น่าเชื่อถือ** (บันทึกไว้แล้วในใบ
`20260901_1105_KA1A-DISPROVEN-*`) ตรวจจากประวัติ `main` ตรง ๆ แทน:
`git log --oneline` เจอ `9c8563e Merge pull request #775` และ `35b8abb Merge pull request #521`
⇒ **merged จริงทั้งคู่** งานรอบก่อนอยู่บน `main` ไม่มีอะไรต้อง cherry-pick

## 3. กล่องจดหมาย (ADDENDUM v2 ข้อ B)

`grep -rl "ADDRESSEE: LANE-GM" notes_to_chief/*.md` แล้วเช็ค stub **ทั้งสองรูปแบบ**
(`<ชื่อเต็ม>.md.CONSUMED.txt` และ `<ชื่อไม่มี .md>.CONSUMED.txt` -- ตาม
`CHIEF-DECISION 20260901_2357`) ⇒ **ไม่มีใบใหม่ที่ยังไม่บริโภค** ทุกใบมี stub ครบ

ใบที่ "สายนี้เปิดเอง" และยังไม่มีคำตอบ -- จัดการรอบนี้:
| ใบ | สถานะรอบนี้ |
|---|---|
| `20260902_0017_LANE-GM-TO-LANE-DB-request-speed-persistence-method.md` | **ถอน** (วาง stub + สำเนาเข้า `consumed/` + ใบแทน `0129`) -- คำขอนี้ไม่จำเป็นเลย ดูหัวข้อ 4 |
| `20260902_0017_LANE-GM-ASK-COO-speed-db-first-ordering-change.md` | **ยังเปิด** COO ยังไม่ตอบ (รอบ :41 ผ่านไปแล้วหนึ่งรอบ) -- ไม่วาง stub |

## 4. งานหลัก: `/speed` เขียนแถวจริงแล้ว (DB ก่อน ไวร์ทีหลัง)

### สิ่งที่เจอตอนต้นรอบ -- คำขอของตัวเองรอบก่อนตั้งอยู่บนพื้นฐานที่ผิด
รอบก่อนสายนี้ขอ overload ที่รับ `identity_lo/hi` จาก LANE-DB เพราะคิดว่า `gm/` ไม่มีทางรู้
`character_id` **ผิด** -- `model.Character` (`model.py:13-22`) มี `id` เป็นฟิลด์แรกมาตลอด และ
`session.foundation.selected` **คือ** `Character` ตัวนั้น (จุดอ่านเดียวกับที่
`_selected_speed_identity` ใช้อยู่แล้ว) ⇒ การแปลมีบรรทัดเดียว อยู่ในเขตสายนี้ ไม่ต้องรอใคร
**ถ้าไม่เจอข้อนี้ รอบนี้จะเป็นรอบเปล่ารอบที่สองติดกัน (ผิดกฎ F)**

### สิ่งที่เปลี่ยน (`src/pirateforce_foundation/gm/chat_command_action.py`)
`_speed_action` เดิม: parse -> compose เฟรม -> ส่ง (ไม่แตะ DB เลย ตาม docstring ของมันเอง)
`_speed_action` ใหม่ ตามลำดับ ทุกด่านเป็น **no-frame** ทั้งหมด:
1. ด่าน run-copy DB (`_speed_db_is_canonical`) -- เดิมกันแค่ "การส่ง" **ตอนนี้กัน "การเขียน" ด้วย**
2. อ่าน `identity_lo/hi` (เดิม)
3. ด่าน vital_version (เดิม) -- withheld = ไม่มีทั้งเฟรม **และไม่มีแถว**
4. parse ค่า
5. **ใหม่** `store.write_typed_attributes_and_compose_sparse(character_id, {speed_walk: value})`
6. **ใหม่** compose เฟรมจาก **ค่าที่อ่านกลับมาจากแถว** ไม่ใช่จากตัวอักษรที่ GM พิมพ์

จุดอ่านใหม่/ค่าคงที่ใหม่:
- `_speed_store(session)` -- **จุดอ่าน store จุดเดียว** ที่ทั้งด่าน filename และการเขียนใช้ร่วมกัน
  (ก่อนหน้านี้ด่านอ่านเอง; ถ้าปล่อยไว้ ด่านกับการเขียนอาจหมายถึงคนละอ็อบเจกต์ = ด่านแต่ในชื่อ)
- `_selected_speed_character_id(session)` -- `int` บวกเท่านั้น (`bool` ตกไปด้วย `type(...) is not int`,
  `0`/`-1` ปฏิเสธ เพราะ rowid เริ่มที่ 1 ค่าพวกนั้นคือ sentinel ที่รั่วมา)
- `SPEED_TYPED_COLUMN = persistence_typed_attrs.column_for(7)` -- resolve ตอน import
  ไม่ hardcode `"speed_walk"` ⇒ ถ้าตารางของ LANE-DB ย้าย x=7 ที่นี่พังตอนบูตเสียงดัง
- EVENT/OUTCOME ใหม่สี่ตัว: `no_store` · `no_character_id` · `persist_refused_<ExcType>` ·
  `persist_readback_unusable` (ชื่อชนิดอย่างเดียวเสมอ ข้อความ exception อาจฝังตัวอักษรที่ GM พิมพ์)

### ทำไมสำคัญกับ `GT-193`
หัวใบ `GT-193` (ของ chief) เขียน `PENDING interface` = รอสองครึ่ง (a) write path ของ LANE-DB
บน `main` (b) `/speed` ที่ **เรียกฟังก์ชันนั้นจริง** · (a) ปิดตั้งแต่ `20260901_2213`
· **(b) ปิดรอบนี้** ก่อนหน้านี้ขั้นที่ 6 ของใบ ("Re-query the persisted attribute row ... Diff
field-by-field") จะได้ diff **ว่างทุกครั้ง** และใบวัดได้แค่ "เฟรมถูก" ไม่ใช่ "จำได้"
ไม่แตะหัวใบเอง (ใบของ chief) -- ขอ chief พลิกเป็น `READY` ในใบ `0129`

### เทส (`tests/test_gm_speed_action.py` +323 บรรทัด)
สองคลาสใหม่:
- `SpeedPersistenceTests` (fake store) -- ลำดับ (แถวก่อนเฟรม) · เขียนคอลัมน์เดียวเสมอ ·
  เฟรมมาจาก read-back ไม่ใช่ตัวอักษรที่พิมพ์ (double บอก 9.5 ขณะ GM พิมพ์ 5.0 -- assert ทั้งว่า
  เท่ากับ 9.5 **และ** ไม่เท่ากับ 5.0) · store raise = ไม่มีเฟรม + ป้ายชนิดอย่างเดียว ·
  ข้อความ exception ไม่รั่วเข้าแถว audit · read-back ที่เป็น `str`/`True`/หายไป = ไม่มีเฟรม ·
  **ด่าน canonical DB ยิงก่อนการเขียน** (`store.calls == []`) · **version gate ปิด = ไม่เขียนเช่นกัน**
- `PersistenceIntegrationTests` (**SQLiteStore จริงบนไฟล์ temp จริง**) -- ค่าอยู่รอดถึง store
  ตัวที่สองที่เปิดไฟล์เดิม (ใกล้ที่สุดที่เทส headless จะเป็น "พรุ่งนี้ล็อกอินใหม่") · `400.1` ปัด f32
  แล้วเฟรมกับคอลัมน์เป็นเลขเดียวกัน · `1e40` ถูกคอลัมน์ปฏิเสธ แถวเดิมไม่ถูกแตะ
  พร้อม guard fd/temp-dir (เหตุที่ PR #495 ตายที่เกต Windows `WinError 32`)
- `tests/test_gm_chat_command_action.py` -- ตรึงชื่อ EVENT ใหม่สี่ตัวในตาราง contract
  (ตารางนั้นบังคับความครบ ไม่ใช่แค่ความถูก)

## 5. เขียว

หลังแก้ทั้งหกข้อของ pf-adversary: `python3 -m pytest tests/ -q` =
**6638 passed · 327 skipped · 13805 subtests** เขียว(cloud sanity)
(ก่อนแก้คือ 6622/327/13796 -- ส่วนต่างคือเทสใหม่ของรอบนี้เอง ไม่ใช่เทสที่เคยแดง)
🔴 หมายเหตุความไม่ตรงกัน: pf-adversary วัดใน worktree ของมันได้ `6562 passed · 387 skipped`
ยอดรวมเท่ากัน มี 60 ใบย้าย passed -> skipped (น่าจะเป็นโมดูลที่ต้องมี client image/capture corpus)
**ไม่มีใบไหนแดง** -- ตัวเลขในไฟล์นี้คือของ clone นี้ ไม่ใช่ค่าที่ re-derive ได้ทุกเครื่อง

## 6. pf-adversary -- **เรียกจริง คืนผลแล้ว ไม่ approve เจอ 6 ข้อ แก้ครบทั้ง 6**

subagent รัน 20 นาที ทำ mutation test จริงใน worktree แยก (sha256 เทียบกับ blob ที่ commit แล้ว
ยืนยันว่าตรวจโค้ดที่ push จริง) แล้วลบ worktree ทิ้ง live tree สะอาด **สรุปคำตัดสิน: Not approved**
ทั้งหกข้อแก้ในคอมมิตถัดมาบน branch เดียวกัน **ก่อน**ปลด draft -- ไม่มีข้อไหนเลื่อนไปรอบหน้า

| # | สิ่งที่มันวัดได้ | แก้อย่างไร | control ที่พิสูจน์ว่าแก้จริง (mutation) |
|---|---|---|---|
| D1 | `/speed` เป็น handler ตัวที่สองที่มี durable state แต่ **ไม่มี `undo`** -- ทำให้ตอน audit row เขียนไม่ลง คอลัมน์ค้างที่ 777.0 ขณะคอนโซลพิมพ์ว่า "anything it had in hand was dropped with it" (**เท็จ**) | `_speed_undo(store, character_id)` อ่านค่าเดิม **ก่อน** เขียน แล้วคืนค่าผ่าน `write_typed_attributes` (ไม่ใช่ตัว compose -- undo ที่ถูก wire gate ปฏิเสธไม่ใช่ undo) แนบไปกับ **ทุก verdict** ตั้งแต่จุดเขียนลงไป | ถอด `undo` ออก -> **4 เทสแดง** (รวมเทส integration บน SQLiteStore จริง) |
| D2 | `refused_speed_<ExcType>` หมายถึง **สองสถานะตรงข้ามกัน** (parse ล้ม = ไม่มีแถว / compose ล้มหลัง commit = แถวเปลี่ยนแล้ว) และคอนโซลพิมพ์ `no blocker recorded` ให้ทางที่อันตรายกว่า | ป้ายใหม่ `refused_speed_persist_compose_<ExcType>` + `COMMITTED_ROW_BLOCKER_PREFIXES` ให้ printer หาประโยคด้วย prefix (suffix เป็นชื่อ exception จึงเป็น fixed key ไม่ได้) ประโยคบอกตรง ๆ ว่า "แถว commit แล้ว" | เทสเก่าสองใบที่ความหมายเปลี่ยนใต้เท้า **ขีดฆ่าและเขียนใหม่** ให้ assert ทั้งป้ายใหม่และสถานะแถว + เทสใหม่ของฝั่ง pre-write |
| D3 | 🔴 **ด่าน canonical DB เทียบสตริงแบบ case-sensitive** -- `--db state\PirateForce.sqlite3` (หรือ trailing space/dot, `::$DATA`, ชื่อสั้น 8.3) **อนุญาตให้เขียนทับไฟล์ canonical** และ `app.py:660` เก็บสตริงของผู้ใช้ดิบ ๆ ไม่ normalize | normalize (ตัด stream suffix, ตัด `. ` ท้าย, casefold) + ชื่อที่มี `~` = ปฏิเสธทันที (8.3 resolve จากสตริงไม่ได้) + **`os.path.samefile` กับไฟล์ canonical ในไดเรกทอรีเดียวกัน** ซึ่งเห็นทะลุ case/8.3/hard link/junction · fail-closed ทุก error | ย้อนกลับเป็น `==` เดิม -> **7 เทสแดง** · ถอด samefile ออกอีก -> **8 เทสแดง** (hard link จริงบนไฟล์จริง) |
| D4 | `test_the_row_is_written_before_any_frame_exists` **มองลำดับไม่เห็นเลย** -- แทรก compose ไว้เหนือการเขียน ก็ยังเขียว 134 เทส | เทสใหม่ `test_no_frame_is_composed_before_the_row_is_written` ห่อ composer แล้วบันทึกว่าตอนมันถูกเรียก store เขียนไปกี่แถวแล้ว (compose ก่อนเขียน = เห็นเลข `0`) | ใส่ mutation ตัวเดิมของ adversary (M11b) กลับเข้าไป -> **แดงแล้ว** |
| D5 | `SPEED_TYPED_COLUMN` เปลี่ยนเป็น literal `"speed_walk"` แล้ว **ยังเขียวหมด** (เทสเดิมเทียบค่าคงที่กับตัวเอง = tautology) และ `FakeStore` ก็ copy literal ที่ตัวเองห้าม · docstring ยังอ้างว่า import-time error เป็น "boot failure ในสายนี้" ทั้งที่ `runtime.py:40` import ระดับโมดูล = **ทั้งเซิร์ฟเวอร์ไม่บูต** | **AST guard** อ่านซอร์สจริง ยืนยันว่า `SPEED_TYPED_COLUMN` ผูกกับ `ast.Call` ชื่อ `column_for` ไม่ใช่ `ast.Constant` · `FakeStore` เปลี่ยนมาใช้ค่าคงที่ · แก้ docstring ให้บอกขอบเขตจริงว่าเป็น trade ที่ตั้งใจ | เปลี่ยนเป็น literal -> **แดง** (การเทียบค่าเฉย ๆ ยังเขียว จึงต้องเป็น AST) |
| D6 | class docstring อ้างว่าเทสจริงคุมทุกอย่าง แต่ refusal 3 ใน 4 ตัว **โปรดักชันเอื้อมไม่ถึงเลย** | เขียนลง docstring ตรง ๆ ว่าตัวไหนโปรดักชันถึง (`persist_refused_TypedAttrError`) ตัวไหนเป็น defence-in-depth ต่อ session shape ที่โปรดักชันยังไม่ผลิต (`no_store` / `no_character_id` / `readback_unusable`) และทำไมยังเก็บไว้ | -- (ข้อนี้เป็นการแก้คำอ้าง ไม่ใช่พฤติกรรม) |

**ข้อที่ adversary ลองแล้วพังไม่ได้** (บันทึกไว้เพราะเป็นส่วนหนึ่งของผล ไม่ใช่แค่ข้อเสีย):
`_speed_store` กับ `_speed_db_filename` แยกกันไม่ได้จริง (attribute ธรรมดา ไม่ใช่ property) ·
ลำดับด่านถูกต้อง (M2 ลบด่าน -> 7 แดง · M3 fail-open -> 1 แดง) · เฟรมพาเลขที่แถวไม่ได้ถือออกไปไม่ได้
(M1/M10/M12 โดนจับหมด) · เขียนสองคอลัมน์ไม่ได้ (M8 -> 5 แดง) · guard ของ `character_id` มีชีวิตทุกตัว
(M4/M5/M6/M9) · **fd guard เป็น control จริง** (ฉีด connect ค้างเข้าไป -> 3 แดง ข้อความ WinError 32) ·
cp874 ไม่มีอักขระ unmappable · GM authorization ไม่ถูกแตะ

**ของแถมสองข้อที่มันแจ้งโดยไม่นับเป็น defect -- จัดการแล้วทั้งคู่:**
1. `python3 tests/test_gm_speed_action.py` รันแค่ 29/59 เทส เพราะ `unittest.main()` อยู่กลางไฟล์
   เหนือคลาสใหม่สามคลาส (เกตใช้ pytest จึงไม่เคยถูกหลอก แต่เขียวที่ไม่ได้รันอะไรเลยแย่กว่าไม่มีเขียว)
   -> **ย้าย block ไปท้ายไฟล์แล้ว** ตอนนี้ `python3 tests/...` = 59 เทส
2. ตัวเลข "เขียว" ของ `docs/GM_LANE.md` (`6622/327`) ไม่ตรงกับที่มันวัดใน worktree (`6562/387`)
   -- ยอดรวมเท่ากัน (6949) มี 60 เทสย้ายจาก passed ไป skipped **ไม่ใช่เทสแดง**
   น่าจะเป็นโมดูลที่ต้องมี client image/capture corpus ซึ่ง sandbox ของ subagent ไม่มี
   -> บันทึกความต่างไว้ตรงนี้ตามจริง ยังไม่ได้ระบุ 60 ใบนั้นทีละใบ (ยกเป็น backlog รอบหน้า)

## ค้นแล้ว (กฎ "ค้นก่อนถอด")

- `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` -- **ค้นแล้ว: เจอ** (root ของ `pf_bridge`)
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` -- **ค้นแล้ว: เจอ**
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` -- **ค้นแล้ว: เจอ**
- `GAME_TEST_QUEUE.md` หา `GT-193` -- **ค้นแล้ว: เจอ** (~บรรทัด 9686, หัวใบ `PENDING interface`)
- `GAME_TEST_QUEUE.md` หา `GameMaster.dll`/`BT_GM`/`GMUI`/`P-3` -- **ค้นแล้ว: เจอเฉพาะใบเก่า** ไม่มีใบใหม่
- `notes_to_chief/*CLAIM*` (กฎใบสองสาย) -- **ค้นแล้ว: ไม่เจอใบจองที่ยังไม่หมดอายุ** และงานรอบนี้
  ระบุผู้ทำสายเดียวอยู่แล้ว (`COO-ORDER 20260901_1641` = LANE-GM) จึงไม่ต้องจอง
- รอบนี้ **ไม่ได้อ้างข้อเท็จจริงใหม่จาก client เลย** -- เป็นการต่อสายภายในเซิร์ฟเวอร์ล้วน

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

พิมพ์ `/speed 800` แล้ว **ขั้นที่ 6 ของ `GT-193` มีอะไรให้ diff จริง** -- คอลัมน์ `speed_walk`
ของตัวละครใน run-copy DB เปลี่ยน และเลขที่ client เห็นเป็นเลขเดียวกับที่แถวถือ (f32 ปัดที่เดียว)
เมื่อวานคำสั่งเดียวกันสร้างเฟรมแล้วลืมทันที ขั้นนั้น diff ว่างเสมอ

## คำถามเดียวที่ adversary บอกว่าดีไซน์ยังไม่ตอบ -- ตอบในรอบนี้

**"แถวอยู่บนดิสก์แล้วแต่เฟรมไม่ได้ออก ใครเป็นเจ้าของความไม่ตรงกันนั้น"**
สายนี้เคยตอบแค่ทางเดียว (ห้ามให้ client เห็นค่าที่ DB ไม่รับ) ไม่เคยตอบทางกลับ คำตอบของรอบนี้
แยกเป็นสองกรณี ไม่ใช่กรณีเดียว:

1. **audit row เขียนไม่ลง** = ทางนี้ **ย้อนกลับ** ตามกฎบ้าน ("ไม่เก็บผลที่สายนี้บันทึกไม่ได้")
   `undo` จริงตาม D1 · ถ้าย้อนไม่ได้ (คอลัมน์เคยเป็น NULL) จะได้ `..._stage_not_reverted` **ไม่โกหก**
2. **compose ล้มหลัง commit / store ปฏิเสธหลัง commit** = **เก็บแถวไว้** DB คือความจริงที่ทนทาน
   ค่าที่เก็บคือ speed ของตัวละครจริง client จะเห็นตอนล็อกอินครั้งหน้า · แต่ต้อง **แยกออกจากกันได้ในร่องรอย**
   จึงมีป้ายของตัวเองและประโยคคอนโซลที่บอกตรง ๆ ว่า "the row IS committed ... the row is the truth"

**ผู้เทสที่เกรด `GT-193` ขั้นที่ 6 ต้องอ่านยังไง:** เจอแถวเปลี่ยนแต่จอไม่เปลี่ยน ให้ grep ป้ายในคอนโซล
`refused_speed_persist_compose_*` หรือ `refused_speed_persist_*` = **ไม่ใช่ FAIL ของใบ** เป็นสภาพที่
ระบบตั้งใจ (แถวคือความจริง เฟรมประกอบไม่สำเร็จ) ให้บันทึกเป็นข้อสังเกตแยก · ถ้า **ไม่เจอ** ป้ายพวกนั้น
แล้วแถวยังเปลี่ยนโดยจอไม่เปลี่ยน อันนั้นเป็นของใหม่ที่ยังไม่มีใครวัด ให้เปิดใบใหม่
[สมมติของสาย GM - รอ COO ยืนยัน] เฉพาะข้อ 2 (การเก็บแถวไว้) -- ข้อ 1 เป็นกฎบ้านที่มีอยู่แล้ว

## nonclaim

1. **ไม่อ้างว่า `GT-193` ผ่าน** -- ไม่มี client อยู่ในหลักฐานรอบนี้เลย ปิดแค่เงื่อนไขเปิดประตูของใบ
2. **ไม่อ้างว่า GM-B ปิด** -- ปิดเมื่อ Panya ติ๊กหลังรัน `GT-193` เท่านั้น (กฎ NOW.md: โค้ดขึ้น main ไม่ใช่ "เสร็จ")
3. ลำดับ **DB-ก่อน-ไวร์ ยังเป็น [สมมติของสาย GM - รอ COO ยืนยัน]** -- ใบ `20260902_0017_LANE-GM-ASK-COO-*`
   ยังไม่มีคำตอบ ต่างจากรอบก่อนตรงที่ตอนนี้เป็นโค้ดจริงแล้ว ถ้า COO เคาะทางตรงข้าม
   จุดแก้คือ `_speed_action` จุดเดียวและ `SpeedPersistenceTests` จะแดงให้เห็น
4. ไม่อ้างว่าด่าน run-copy DB เป็นหลักประกันเชิงเข้ารหัส -- **เป็น heuristic จากชื่อไฟล์** เท่านั้น
   (docstring ของมันเองพูดไว้) สิ่งที่รอบนี้เพิ่มคือมันกันการ **เขียน** แล้วด้วย ไม่ใช่ว่ามันแม่นขึ้น
5. ไม่อ้างว่า x=7 คือ speed ที่พิสูจน์บนจอแล้ว -- `RE-194` (BasicAttr+0x54 player-vs-NPC) ยังเปิด
   และเดินขนานไป ไม่ใช่เงื่อนไขเปิดประตูของใบนี้
6. ไม่แตะ `runtime.py` / `app.py` / `current/pf_login_game_server_v141.py` / canonical DB /
   `scenarios/world_*.json` / `scenarios/combat_*.json` / ไฟล์ใด ๆ ของ LANE-DB
   (เรียก `store.write_typed_attributes_and_compose_sparse` เฉย ๆ ไม่แก้แม้บรรทัดเดียว)
7. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json` · client ยกระดับตัวเองไม่ได้ · ไม่ประกาศ milestone
8. **GM ข้ามขั้นไหน:** `/speed` เป็นคำสั่ง GM -- ค่า speed ที่ได้จากมันไม่ใช่หลักฐานว่าระบบ
   movement/attribute ของผู้เล่นปกติทำงาน เป็นทางลัดไปถึงสภาพที่จะเทสเท่านั้น
9. ไม่ลบประวัติเดิม -- docstring เดิมที่กลายเป็นเท็จ (`"writes no DB row"`) **ขีดฆ่า ไม่ลบ**
   และเทสสองใบที่ความหมายเปลี่ยนใต้เท้าหลังต่อสาย ก็ขีดฆ่าพร้อมเหตุผล ไม่ลบเงียบ ๆ
10. **ไม่อ้างว่าด่าน canonical DB ปิดสนิทแล้วหลังแก้ D3** -- `samefile` เห็นเฉพาะไฟล์ที่อยู่
   **ไดเรกทอรีเดียวกัน** สำเนา canonical ที่วางไว้คนละโฟลเดอร์คนละชื่อ ยังเล็ดลอดได้เหมือนเดิม
   (ข้อจำกัดเดิม ไม่ได้แย่ลง แต่ก็ไม่ได้ปิด)
11. ไม่อ้างว่าตัวเลขเขียวของรอบนี้ re-derive ได้ทุกเครื่อง -- ดูหมายเหตุ 60 ใบ passed->skipped ข้างบน

## ไฟล์ที่แตะ

`pirate-force-server` (เขต `gm/` + `tests/test_gm_*` + `docs/GM_LANE.md` เท่านั้น):
`src/pirateforce_foundation/gm/chat_command_action.py` · `tests/test_gm_speed_action.py` ·
`tests/test_gm_chat_command_action.py` · `docs/GM_LANE.md`
`pf_bridge`: จดหมายใหม่ 2 ใบ + stub 1 + สำเนา `consumed/` 1 + ไฟล์รอบนี้

## PR

`pf_bridge` #777 · `pirate-force-server` #523
