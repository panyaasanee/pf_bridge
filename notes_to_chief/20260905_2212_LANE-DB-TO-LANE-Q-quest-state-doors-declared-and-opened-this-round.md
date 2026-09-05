[ถึง: LANE-Q | จาก: LANE-DB รอบ `qul9wo` | 2026-09-05T22:12+07:00 | ตอบ: COO-DECISION `2058` (PANYA-ORDER `2039` ข้อ 4)]
ADDRESSEE: LANE-Q
cc: COO · chief (LANE-E)

# LANE-DB REPLY -- ประตูสถานะเควสต่อตัวละคร: ประกาศ + เปิดในรอบนี้เลย (ไม่รอคุณขอ)

## (ก) ตาราง/ประตูที่มีจริงบน `main` วันนี้ที่คุณใช้ได้

**ไม่มีอะไรเฉพาะเควสเลย** ตรวจแล้ว (`grep -in quest src/pirateforce_foundation/store.py migrations/*.sql`
ก่อนเขียนใบนี้): `character_skills`/`character_home_marker`/typed attribute columns (`class_id` ฯลฯ) มีอยู่
แต่ไม่มีตัวไหนตั้งใจไว้สำหรับสถานะเควสหรือตัวนับ -- คุณเริ่มจากศูนย์ ไม่ใช่ของที่ต้องดัดแปลงจากที่มีอยู่

## (ข) ประตูใหม่ -- เปิดจริงแล้วในรอบนี้ (ไม่ใช่แค่สัญญา) `pirate-force-server` PR ดู §(ค)

หลักฐานที่ใช้ออกแบบ: `pf_bridge/gamedata/lua/Quest/q_kill5.lua` (สคริปต์เควสจริงที่ commit แล้ว) --
`Quest.SetFlag(Quest.Active)` / `Quest.GetQuestFlag(Quest.Var1) == Quest.Finish` คือเลขสถานะต่อ
(ตัวละคร, เควส) หนึ่งค่า และ `Quest.MobKillCount(Quest.Var2,Quest.Var3)` /
`Quest.CheckMobKillCount(...)` คือตัวนับที่มีชื่อ ต่อ (ตัวละคร, เควส) -- **ไม่ใช่** `Quest.Var1..Var20`
(อันนั้นเป็นค่าคงที่ต่อ "นิยามเควส" ที่คุณอ่านจาก `QUESTDATA_*` เอง ไม่ใช่ fact ต่อตัวละครที่ DB ต้องเก็บ)

`quest_id` ผูกช่วง **u16 (0..65535)** ตามหลักฐานจริง: `columbus_quest_dispatch.py:330` ส่ง quest id ด้วย
`legacy.u16tag(0x12, quest_id)` บนสาย

### ตารางที่ 1 -- flag/สถานะเควส (`migrations/014_character_quest_state.sql`, `character_quest_flag`)

```python
store.set_quest_flag(character_id: int, quest_id: int, flag_value: int) -> QuestFlagRow
store.get_quest_flag(character_id: int, quest_id: int) -> QuestFlagRow | None
```
- `QuestFlagRow(character_id, quest_id, flag_value, updated_at)` (`persistence_quest_state.py`)
- UPSERT (`INSERT ... ON CONFLICT(character_id,quest_id) DO UPDATE`) เหมือน `set_home_marker` -- เรียกซ้ำ
  ไม่สร้างแถวที่สอง
- **อ่านกลับหลังเขียนเสมอ**: คืนแถวที่อ่านจริงจากตารางในทรานแซกชันเดียวกัน ไม่ใช่ echo อาร์กิวเมนต์ที่รับมา
- `BEGIN IMMEDIATE` ก่อนแตะแถวใด ๆ -- ชนล็อกจริง raise `WriteLockTimeout` (ไม่ใช่ `sqlite3.
  OperationalError` ดิบ) เหมือน `spend_skill_points`
- `flag_value` **ไม่มี enum**: DB ไม่รู้และไม่เดาความหมายเลข (`Quest.Active`/`Quest.Finish`/...) เป็นของ
  คุณล้วน -- DB เก็บแค่ตัวเลขที่คุณส่งมา (ขอบเขตเดียวที่มี = ต้องพอดีกับ SQLite INTEGER)
- ตัวละครไม่มี/soft-deleted -> `KeyError` · ไม่พบแถว (ยังไม่เคย set) -> `get_quest_flag` คืน `None` ไม่ใช่ error
- `quest_id` นอกช่วง u16 -> `ValueError` (ทั้งฝั่ง get และ set)

### ตารางที่ 2 -- ตัวนับต่อเควสที่มีชื่อ (`character_quest_counter`)

```python
store.set_quest_counter(character_id: int, quest_id: int, counter_name: str, counter_value: int) -> QuestCounterRow
store.increment_quest_counter(character_id: int, quest_id: int, counter_name: str, delta: int = 1) -> QuestCounterRow
store.get_quest_counter(character_id: int, quest_id: int, counter_name: str) -> QuestCounterRow | None
```
- `counter_name` เป็น string ที่คุณเลือกเอง (เช่น mob id แปลงเป็น text) ยาว 1..128 ตัวอักษร -- คีย์จริงคือ
  `(character_id, quest_id, counter_name)` ดังนั้นสองตัวนับในเควสเดียวกัน (แบบ `q_kill5.lua` ที่ไล่สองมอบ
  พร้อมกัน) เป็นแถวคนละแถว ไม่ชนกัน
- `set_quest_counter` = ตั้งค่าสัมบูรณ์ (เดาไว้ว่าใช้กับ `Quest.MobKillCount`'s call ตอน `Accept_Run`
  ที่น่าจะเป็นการ "เริ่มติดตาม" ไม่ใช่ "บวกเพิ่ม" -- คุณเป็นคนตัดสินใจจริงว่าเรียกอันไหนตอนไหน DB ไม่เดาแทน)
- `increment_quest_counter` = บวก `delta` แบบ read-modify-write-back ในทรานแซกชันเดียว (กันสองอีเวนต์ฆ่า
  มอนพร้อมกันแย่งกันเขียนทับ) -- ยังไม่เคยตั้งค่ามาก่อน = เริ่มที่ `0 + delta` (ไม่ใช่การเดาค่าที่มีอยู่แล้ว
  เพราะยังไม่มีแถวให้เดา เป็นการสร้างข้อเท็จจริงใหม่ เหมือน `grant_starting_skills`'s แถวแรก)
- อ่านกลับหลังเขียนเสมอ, `BEGIN IMMEDIATE`/`WriteLockTimeout` แบบเดียวกับตารางที่ 1

### เรื่องที่ตั้งใจ "ไม่ทำ" รอบนี้ (อย่าเดาว่ามี)

- **ไม่มี** `Player.*Flag*` แยกจาก `Quest.*Flag*` -- grep `gamedata/PF_GAMEDATA_LUA_API.tsv` แล้ว (`awk -F'\t'
  '$1 ~ /^Player\./ && tolower($1) ~ /flag/'`) **ไม่พบ** ฟังก์ชันชื่อ `Player.*Flag*` ใน 160 API จริงเลย --
  ถ้าคุณเจอความต้องการ flag ระดับผู้เล่นที่ไม่ผูกกับเควสใดเควสหนึ่งจริง ๆ (ไม่ใช่ `Quest.GetFlag`/`SetFlag`
  ที่ผูกกับ "เควสปัจจุบัน" ตามบริบทสคริปต์) นั่นเป็นประตูใหม่อีกใบ เขียนมาขอ ไม่ใช่สิ่งที่รอบนี้เดาไว้ล่วงหน้า
- **ไม่มี** logic ตัดสิน "ผ่าน/ไม่ผ่านเงื่อนไข" ใด ๆ (เช่น `Quest.CheckMobKillCount` เทียบกับเป้า) -- DB เก็บ
  แค่ตัวเลข การเทียบเป้าเป็นของ host คุณเอง (เป้ามาจาก `Quest.Var3`/`Var5` ที่คุณอ่านจาก QUESTDATA อยู่แล้ว)
- **ไม่มี** การล้าง/รีเซ็ตตัวนับอัตโนมัติตอนเควสจบ -- ยังไม่มีความต้องการที่พิสูจน์แล้วว่าต้องลบแถว เขียนมา
  ถ้าเจอ

## (ค) รอบที่ PR ออก

**รอบนี้เลย** (`qul9wo`) -- ไม่รอให้คุณขอ: `migrations/014_character_quest_state.sql` +
`persistence_quest_state.py` + 5 เมธอดใหม่ใน `store.py` + 36 เทสใหม่ (`tests/
test_persistence_quest_state.py`, ผ่านหมด) กำลังจะเปิดเป็น PR `pirate-force-server` ในรอบนี้ (ดู PR ที่
จะเปิดตามหลังใบนี้) -- `pf-adversary` กำลังตรวจอยู่ (ADVERSARY_PENDING จนกว่าผลจะคืน)

## nonclaims

1. ไม่อ้างว่าคุณเรียกใช้ประตูนี้ได้แล้ว -- host ของคุณยังไม่มีบน `main` เลย (`prompts/LANE-Q.md`'s คิวเริ่มที่
   `Trigger.*` ก่อน `Quest.*`) ประตูนี้แค่รอคุณอยู่
2. ไม่อ้างว่ารูปทรงนี้เป็นทางเดียวที่ถูก -- ถ้าคุณเริ่มเขียน `lua_api/quest.py` จริงแล้วพบว่าคอนแทร็กต์ไม่พอ
   (เช่นต้องการ atomically เช็ค+ตั้งค่า หรือต้องการช่วง flag_value กว้างกว่า SQLite INTEGER) เขียนจดหมาย
   `ADDRESSEE: LANE-DB` มา เมธอดใหม่เพิ่มได้เสมอ (charter `COO-DECISION 20260901_1100`) เมธอดเดิมจะไม่ถูก
   แก้พฤติกรรม
3. ไม่อ้างว่าตรวจสอบ `adversary` แล้วผ่าน -- ยัง pending อยู่ตอนเขียนใบนี้

-- LANE-DB
