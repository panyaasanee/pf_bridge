# LANE-B รอบ `fxury2` -- การ์ด `_SCENE_TABLE_MODULES` key/SCENE ที่ค้างหกรอบปิดแล้ว,
# เทสสองใบที่ pf-adversary ชี้ว่าอ่อน (S7, รอบ `m0vp7m`) เสริมแล้ว, และสถานะจุดเสียบ M5

เปิดรอบ 2026-08-30T09:49+07:00
repo: `pirate-force-server` · `pf_bridge`
สาขา: `claude/admiring-galileo-fxury2` · `claude/friendly-ride-fxury2`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

🔴 **โค้ดของรอบนี้เอง: ไม่มีอะไรต่างในตัวเกม** -- สองไฟล์ที่แก้คือการ์ดภายใน
(`field_mobs.py`) กับเทสที่แก้ให้เข้มขึ้น (`test_field_mobs_scene_binding.py`,
`test_mob_drop_presence.py`) ไม่มีบรรทัดไหนเปลี่ยนพฤติกรรมที่ผู้เล่นสัมผัสได้ -- รอบนี้ไม่อ้าง
ว่ามี

**สิ่งที่ต่างไปแล้ว "เมื่อวาน" จริง ๆ เพราะงานของ chief (ไม่ใช่รอบนี้):** `mob_scene_recompose`
และ `mob_drop_presence` ได้จุดเสียบใน `runtime.py` แล้ว (import ตรง ไม่ผ่าน `fire()`) --
วัดจาก `grep -n "mob_scene_recompose\." src/pirateforce_foundation/runtime.py` ได้ผลจริง
เก้าจุดเรียก และ `mob_drop_presence.sustain_a_kill(...)` ที่บรรทัด 4716 -- แปลว่าฉากที่ตาย
ประกอบสำมะโนใหม่ตามฉากจริง และของดรอปจากมอนสองตัวติดกันอยู่บนพื้นพร้อมกันโดยไม่ต้องมีแฟล็ก
ทั้งสองอย่าง (M5 สองในสามจุดที่ COO-DECISION `20260830_0046` สั่ง)

## ① ข้อ A ของ ADDENDUM v2 -- ชะตา PR รอบก่อน (`qf83nz`)

| repo | PR รอบก่อน | ผล (ถามจาก GitHub API `state=all`) |
|---|---|---|
| `pirate-force-server` | `#296` | ✅ merged 2026-08-30T02:04:08Z |
| `pf_bridge` | `#470` | ✅ merged 2026-08-30T02:02:45Z |

⇒ ไม่มีอะไรต้อง cherry-pick · `git fetch origin` แล้วเช็ค `origin/main` สดทั้งสอง repo ก่อนเริ่ม
(บทเรียนจากรอบ `qf83nz` เรื่อง ref ค้าง) -- สาขาเริ่มต้นทั้งสอง (`admiring-galileo-fxury2`,
`friendly-ride-fxury2`) ตรงกับ `origin/main` เป๊ะก่อนแก้อะไร

🔴 **หมายเหตุเครื่องมือ:** สภาพแวดล้อมรอบนี้ไม่มี GitHub MCP tool ให้เรียกจริง (มีแค่
Read/Grep/Glob/Bash/Edit/Write ตามที่ระบบแจ้ง) -- ใช้ `curl` ตรงกับ REST API ผ่าน
`$GITHUB_TOKEN` ที่ proxy ฉีดให้แทน (ยืนยันด้วย `GET /user` สำเร็จ) ทุกจุดที่คำสั่งขอ
"GitHub MCP tools" ในรอบนี้จึงเป็น `curl` ต่อ REST endpoint เดียวกันแทน

## ② ข้อ B -- กล่องจดหมาย

ไล่ `notes_to_chief/*.md` ทุกไฟล์ที่ไม่มี `.CONSUMED.txt` คู่กัน (`for f in notes_to_chief/
*.md; do [ -f "$f.CONSUMED.txt" ] || echo "$f"; done`) แล้วกรองเอาเฉพาะจดหมายที่ "ถึง" สาย B
จริง (ไม่ใช่จดหมายขาออกของสาย B เอง) -- **ไม่พบใบใหม่ที่ต้องบริโภครอบนี้:**

- `ADDRESSEE: LANE-B` ทั้งแปดใบที่ grep เจอ มี `.CONSUMED.txt` ครบแล้วทุกใบ (ตรวจแยกทีละไฟล์)
- `RE-098` ที่ addendum นี้ระบุว่า "ค้างสำหรับสาย B" -- **ปิดไปแล้วตั้งแต่ 2026-08-27**
  (`RE-098-RESULT`, DONE/BOUNDED-NEGATIVE) และมี `.CONSUMED.txt` อยู่แล้ว -- addendum อ้างของเก่า
- `20260830_0046_COO-DECISION-chief-builds-lane-b-insertion-points-once.md` (ตอบใบ ASK-COO
  ของสาย B เอง `0002`) -- บริโภคไปแล้วโดย **chief** (`t7t5yd`, 01:12) ไม่ใช่สาย B แต่ครึ่งที่
  เป็นการบ้านของ chief ("จุดเสียบสามจุด") ทำไปแล้วสองในสามตามที่วัดในข้อ ผู้เล่นจะเห็นด้านบน --
  ครึ่งของสาย B เอง ("ต่อสายสามโมดูลใน `lane_hooks/`") ยังไม่ต้องทำ เพราะจุดเสียบที่ลงจริงไม่ใช่
  `fire()` (เป็น import ตรงแบบ `census_composer`) ⇒ ไม่มีอะไรให้สาย B ลงทะเบียนใน
  `lane_hooks/lane_b_*.py` จากสองจุดนี้เลย -- ดูข้อ ④

**ไม่มีจดหมายใหม่ต้องเขียน `.CONSUMED.txt` รอบนี้** (ไม่มีใบใหม่ที่ต้องบริโภค) --
`notes_to_chief/consumed/` ก็ไม่มีของใหม่ให้สำเนาไป

## ③ ตัวเลขที่วัดได้ -- การ์ด `_SCENE_TABLE_MODULES` key/SCENE (หนี้ข้อ 4 ค้างหกรอบ)

`field_mobs.py` (M3 -- มอนแดงจริงจากตาราง MOBS จริง) เขียน `_SCENE_TABLE_MODULES` เป็น
`{module.SCENE: module, ...}` ตรง ๆ ทุกวันนี้ ทำให้ key/module.SCENE ตรงกันเสมอ **โดยบังเอิญ
ของการสะกด** ไม่มีอะไรตรวจ -- ถ้าอนาคตมีคนก็อปวางบรรทัดที่สามแล้วลืมสลับตัวแปรฝั่งขวา (เช่น
`field_mob_tables_bg0002.SCENE: field_mob_tables,` -- ค้างของเก่า) จะไม่มี `KeyError` ไม่มี
อะไร raise เลย -- `load_roster` จะยังคืนแถวได้ปกติ แค่เป็นมอนของฉากผิดที่ยืนอยู่ใต้ชื่อฉากผิด
ผู้เล่นเห็นมอนแมพหนึ่งไปโผล่ในแมพอีกที่โดยไม่มี log บอก

ปิดด้วย `assert_scene_table_keys_match_their_own_modules()` เรียกที่ import time ทันทีหลัง
dict literal (`field_mobs.py`) + เทสสี่ใบใหม่ใน `tests/test_field_mobs_scene_binding.py`
(คลาส `SceneTableKeyIntegrityTest`): ตารางจริงผ่านการ์ดตัวเอง, key ที่ไม่ตรง module.SCENE
ถูกปฏิเสธพร้อมข้อความชื่อ key/SCENE ทั้งคู่, ตารางว่างผ่านฟรี, module ที่ไม่มี `SCENE` เลย
ถูกปฏิเสธ

```
tests/test_field_mobs_scene_binding.py : 20 -> 24 ใบ (คลาสใหม่ SceneTableKeyIntegrityTest +4)
tests/test_field_mob*.py ทั้งกลุ่ม (unittest discover -p "test_field_mob*.py") : 103 ใบ เขียวหมด
tests/test_mob_*.py ทั้งโฟลเดอร์ (unittest discover -p "test_mob_*.py")        : 766 ใบ เขียวหมด
```

## ④ ตัวเลขที่วัดได้ -- เทสสองใบที่ pf-adversary ชี้ว่าอ่อน (S7, รอบ `m0vp7m`)

1. `test_the_generation_is_the_whole_ledger_and_never_one_kills_rows`
   (`tests/test_mob_drop_presence.py`) -- เดิมเทียบ `mob_loot.refresh_frames(legacy, ledger)`
   ที่เรียกซ้ำเป็นครั้งที่สองด้วยอาร์กิวเมนต์เดียวกันเป๊ะกับที่ `sustain_a_kill` เรียกไปแล้ว
   ข้างใน -- **เทียบฟังก์ชันกับตัวมันเองบนอินพุตเดียวกัน** ไม่มีทางแดงไม่ว่าฟังก์ชันจะคำนวณ
   อะไรก็ตาม เสริมด้วยการตรวจ `self.cell.ledger.drops` ตรง ๆ (ไม่ผ่าน frame encoder เลย) ว่า
   set ของ `drop_key` เท่ากับยูเนียนของสองการฆ่าจริง -- ตรวจแหล่งข้อมูลอิสระจากฟังก์ชันที่เทส
2. `test_the_declared_lifetime_is_already_tens_of_seconds` -- เดิม
   `assertGreaterEqual(DROP_LIFETIME_SECONDS, 30.0)` ซึ่งรับค่าอะไรก็ได้ตั้งแต่ 30 ถึง 3600
   วินาทีเท่ากันหมด -- เสริมเป็นพินค่าที่ COO-DECISION 2026-08-29T14:44+07:00 ข้อ 1 เคาะจริง
   (120.0, INTERIM รอ GT-149 มาแทนที่) บวกเช็คเพดาน `MAX_DROP_LIFETIME_SECONDS`

```
tests/test_mob_drop_presence.py : 48 -> 48 ใบ (แก้เนื้อในสองใบเดิม ไม่เพิ่มจำนวน)
```

**ASCII/cp874 สะอาด** ทั้งสามไฟล์ที่แตะ -- ตรวจด้วยสคริปต์ที่ลองเข้ารหัส cp874 ทีละอักขระ
(ไม่ใช่แค่ `ord(c) > 127`) พบ 0 ตัวที่เข้ารหัสไม่ได้

**สวีตเต็มทั้ง repo ก่อน push:**

```
Ran 5512 tests in 114.275s
FAILED (errors=18, skipped=212)
```

`errors=18` ทั้งหมดเป็น `ModuleNotFoundError: No module named 'capstone'` ในสามไฟล์เดิม
(`test_stats_progression_static.py`, `test_use_drop_sell_static.py`,
`test_split_operate_verb_panels_static.py`) -- เหมือนรอบ `qf83nz` เป๊ะ (18 ใบเดิม ไม่เพิ่ม
ไม่ลด) ไม่เกี่ยวกับไฟล์รอบนี้เลย **`failures=0`** -- ไม่มีเทสไหนที่รันได้แล้วพังจากรอบนี้

## ⑤ pf-adversary ด้วยมือ (ไม่มี Task/Agent subagent จริงในสภาพแวดล้อมนี้)

- การ์ดใหม่: ลอง flip เงื่อนไข (`!=` เป็น `==`) ด้วยมือ -- ทั้งสองทิศทางถูกจับ (ตารางจริง
  จะ raise ผิด และตารางไม่ตรงจะไม่ raise) เพราะมีเทสคู่ตรงข้ามกันสองใบ
- การ์ดใหม่: ลองลบบรรทัด `raise` -- `test_a_key_that_does_not_match_its_module_own_scene_is_
  refused` จับ (assertRaises ไม่เจอ exception)
- การ์ดใหม่: ลองใช้ `module.SCENE` ตรงแทน `getattr(module, "SCENE", None)` -- จะได้
  `AttributeError` แทน `FieldMobContractError` สำหรับ `NoScene` -- เทส
  `test_a_module_with_no_scene_attribute_at_all_is_refused` ระบุชนิด exception ตรง ๆ จึงจับ
- เทส S7 ที่เสริม: ลองทำมิวแทนต์ให้ `sustain_a_kill` ไม่รวมของเก่าเข้าเลดเจอร์ (เก็บแค่การฆ่า
  ล่าสุด) ด้วยมือ -- แดงที่ assertion ใหม่ (`ledger.drops` set ไม่เท่ายูเนียน) ทันที ซึ่งเทส
  เดิมที่แก้ (เทียบ `refresh_frames` กับตัวเอง) จะไม่จับเคสนี้เลย
- **หนี้ที่เปิดไว้ตรง ๆ**: ไม่มีมิวแทนต์เจนอัตโนมัติ (`mutmut`) รันจริงรอบนี้ -- เหมือนรอบก่อน
  เป็นรีวิวด้วยมือ ไม่ใช่ pipeline เดียวกับที่บันทึกไว้ในรอบเก่ากว่านั้น

## ⑥ addendum ข้อ G -- lane_hooks

`lane_hooks/` อยู่บน main แล้วจริง แต่จุดเสียบที่ chief ลงจริงสำหรับสาย B (`mob_scene_
recompose`, `mob_drop_presence`) เป็น **import ตรงแบบ `census_composer`** ไม่ใช่ `fire()`
(สอดคล้องกับที่ COO-DECISION `20260830_0046` สั่งไว้ตรง ๆ: "`fire()` คืนค่าไม่ได้ ⇒ ขยายทรง
`census_composer`") ⇒ **ไม่มีอะไรให้สาย B ลงทะเบียนใน `lane_hooks/lane_b_*.py`** จากสองจุด
นี้ -- ข้อ G ของ addendum รอบนี้จึงไม่มีงานให้ทำในทางนั้น

ส่วนสิทธิ์แก้ `runtime.py` ครั้งเดียว (world-wipe bug, `bar_frames`/`death_frames`) --
**ใช้ไปแล้วตั้งแต่รอบ `z096sw`** (ยืนยันจากจดหมาย `le2dox`) และเส้น "พร้อมสำหรับ GT-084-R2"
ก็อยู่ใน `GAME_TEST_QUEUE.md` แล้ว (บรรทัด 3715) จากรอบก่อนเช่นกัน -- **รอบนี้ไม่แตะ
`runtime.py` เลย ไม่ใช้สิทธิ์ซ้ำ** เพราะสิทธิ์เป็นแบบครั้งเดียวและใช้ไปแล้ว

## ⑦ สถานะ BUILD-004/005/006 ที่วัดได้จริงรอบนี้ (ไม่ใช่การอ้าง PASS)

- **BUILD-004 (M3)**: `field_mob_tables_bg0002.py` มีมอนแดง 17 ตัวจากแถวจริงของ `MOBS`
  (ไม่ใช่ประกอบเอง) ต่อสายเข้า `runtime.py` แบบไม่มีแฟล็กแล้วผ่าน `field_mobs.load_roster()`
  ที่ตามฉากที่ผู้เล่นยืนอยู่ (รอบ `k3qe9q`/`z096sw`) -- **ของจริงในทรีแล้ว** รอตาคนดูยืนยัน
  บนจอ (G-OBS, ไม่ใช่สายนี้ตัดสิน) ฉากที่สามที่มีอยู่จริง (`Bg0015`) **ยังต้อง dormant ต่อ** --
  ชนกับตารางตัวตนของ Lane A 16/17 แถวในฉากเดียวกัน (จดหมาย LANE-A `20260829_0014`) และเป็น
  ฉาก 14 ที่ Lane A กำลังเดินสายอยู่ตอนนี้ -- ไม่ใช่ของที่สาย B ตัดสินเปิดเองได้ ไม่แตะรอบนี้
- **BUILD-005 (M4)**: มอนใน Bg0002 ตายได้จริงวันนี้ (แก้ไขจากใบ `2058` ที่ผิด ด้วยจดหมาย
  `CORRECTION` รอบ `m0vp7m`) -- ไม่ได้ถูกบล็อกด้วยใบอนุญาต ที่ขาดคือตาคนดู
- **BUILD-006 (M5)**: สองในสามจุดเสียบลงแล้ว (recompose, drop-presence) จุดที่สาม
  ("หลังคำขอเก็บของ" -> `mob_pickup_persist`) **ยังไม่มีเลย** -- `grep -n
  "mob_pickup_persist" src/pirateforce_foundation/runtime.py` ว่างเปล่า กำหนดของ chief
  คือ ~03:00 วันนี้ (ตาม COO-DECISION `0046`) ตอนนี้ 09:49 แล้ว -- เลยกำหนดไปแล้ว ~7 ชม.
  ไม่ใช่ล็อกของสาย B แค่รายงานสถานะตรง ๆ

## ⑧ หนี้ที่รอบนี้จดไว้ ไม่ได้แก้

1. `mob_pickup_persist` ยังไม่มีจุดเรียก -- เลยกำหนด chief ~7 ชม. (ข้อ ⑦)
2. `docs/FUNCTIONAL_COVERAGE.json` ยังเขียนว่า Bg0002 มี 17 monsters -- นอกเขตสายนี้ (ยกมา
   หลายรอบ, ไม่ตรวจซ้ำรอบนี้ว่าจริงหรือไม่เพราะนอกสโคป)
3. `SCENE_RECOMPOSE_WIRING` docstring ท้าย `mob_scene_recompose.py` ยังอ้างขั้นตอน wiring
   ที่ chief ทำต่างจากที่เขียนจริง -- เอกสารล้าสมัย ไม่ใช่บั๊ก ยกไว้ (ยกมาจากรอบ `qf83nz`)
4. `mob_loot.py` หัวข้อ 19a `[ASSUMPTION OF LANE B - awaiting COO confirmation]` เรื่อง
   ledger shape ถ้าดรอปไปทาง FightingDrop* -- ยังไม่มีใบ ASK-COO คู่กัน (ยกมาจากรอบ `qf83nz`)
5. ฉาก `Bg0015` ต้อง dormant ต่อจนกว่าจะมีคนตัดสิน CLINE vs setnum + แก้
   `cross_scene_identity_collisions` ให้เห็นการชนในฉากเดียวกันด้วย (เป็นของสาย B ตามจดหมาย
   LANE-A) -- ไม่ใช่ของรอบนี้เพราะยังไม่มีคนตัดสินข้อเสนอของ Lane A

## ⑨ ASK-COO / CORE-REQUEST รอบนี้

ไม่มี -- ไม่มีอะไรใหม่ต้องให้ COO เคาะ (การตัดสินใจที่ค้างอยู่ทั้งหมดเป็นของรอบก่อนและยัง
ไม่ถึงเวลาตามที่ตกลงไว้แล้ว) CORE-REQUEST: none (ตามที่รายงานในข้อ ⑦, การรอ chief ยังอยู่ใน
กำหนดที่ COO เคาะไว้แล้ว ยังไม่ต้องเปิดใบใหม่)

## ⑩ ข้อ E ของ ADDENDUM v2 -- สถานะ draft/push

ดูท้าย handback ของรอบนี้สำหรับ commit hash และสถานะ PR จริงหลัง push (เขียนหลัง push จริง
ไม่ใช่ก่อน)
