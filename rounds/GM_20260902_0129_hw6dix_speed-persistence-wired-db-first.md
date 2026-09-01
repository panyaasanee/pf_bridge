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

`python3 -m pytest tests/ -q` = **6622 passed · 327 skipped · 13796 subtests** เขียว(cloud sanity)
เฉพาะสาย GM `tests/test_gm_*.py` = **1307 passed · 590 subtests** เขียว(cloud sanity)

## 6. pf-adversary

**เรียกจริงรอบนี้** ผ่าน `Agent(subagent_type: pf-adversary)` -- สั่งให้ลองพังหกทาง:
(1) มี session shape ไหนที่พา **การเขียน** ไปลง canonical DB ได้ไหม และ `_speed_store` กับ
`_speed_db_filename` ชี้คนละอ็อบเจกต์ได้ไหม (2) เฟรมพาเลขที่แถวไม่ได้ถืออกไปได้ไหม
(3) `SPEED_TYPED_COLUMN` resolve ตอน import ปลอดภัยไหมถ้า x=7 เสียคอลัมน์
(4) **mutation test**: ลบ/บิดพฤติกรรมทีละอย่างแล้วรัน `tests/test_gm_speed_action.py`
เทสใหม่ตัวไหน "เขียวเพราะผิดเหตุผล" (5) ด่านสองด่านยังยิงก่อนการเขียนจริงไหม
(6) fd/temp-dir รั่วในเทส integration ใหม่ (เกต Windows `WinError 32`) หรือเปล่า

🔴 **สถานะตอน push: subagent ยังรันอยู่ (เกิน 13 นาที) ยังไม่คืนผล** -- บันทึกตามจริง ไม่เดาผลแทนมัน
สิ่งที่ทำแทนเพื่อไม่ให้รอบหาย และเพื่อไม่ให้ข้ามกฎ:
- **PR ยังเป็น draft** จนกว่าผลจะกลับมา งานยังไม่มีทางเข้า `main` ระหว่างนี้
- ตรวจ working tree ก่อน commit ว่าไม่มี mutation ของ subagent ค้างอยู่:
  `git diff --stat` = `202 / 13 / 323` (+ `docs/GM_LANE.md` 97) ตรงกับที่สายนี้เขียนเองทุกบรรทัด
- ผู้เขียนรอบนี้อ่าน diff ย้อนกลับเองหนึ่งรอบ (adversarial self-read) ก่อน commit -- สามข้อที่ตั้งใจ
  ปิดตั้งแต่เขียน: จุดอ่าน store จุดเดียว (ด่านกับการเขียนหมายถึงอ็อบเจกต์เดียวกันเสมอ) ·
  ด่านทั้งสองยิงก่อนการเขียน มีเทส assert `store.calls == []` เป็น control จริง ·
  เฟรมประกอบจาก read-back และเทส assert **ทั้ง** "เท่ากับ 9.5" **และ** "ไม่เท่ากับ 5.0"
  (ถ้าลบพฤติกรรม read-back ออก ข้อหลังจะแดง -- นี่คือ control ที่ตั้งใจใส่กันเทสเขียวลอย ๆ)
- **ถ้า subagent คืนผลแล้วเจอข้อบกพร่อง: แก้ในคอมมิตถัดไปบน branch เดียวกันก่อนปลด draft**
  ถ้าจบรอบก่อนมันคืนผล จะเขียนไว้ในไฟล์รอบนี้ว่า "ยังไม่ได้ผล" และยกเป็นข้อแรกของ backlog รอบหน้า

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

## ไฟล์ที่แตะ

`pirate-force-server` (เขต `gm/` + `tests/test_gm_*` + `docs/GM_LANE.md` เท่านั้น):
`src/pirateforce_foundation/gm/chat_command_action.py` · `tests/test_gm_speed_action.py` ·
`tests/test_gm_chat_command_action.py` · `docs/GM_LANE.md`
`pf_bridge`: จดหมายใหม่ 2 ใบ + stub 1 + สำเนา `consumed/` 1 + ไฟล์รอบนี้

## PR

`pf_bridge` #777 · `pirate-force-server` #523
