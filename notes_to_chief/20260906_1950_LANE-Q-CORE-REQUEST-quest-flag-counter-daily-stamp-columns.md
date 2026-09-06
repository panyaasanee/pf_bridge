[จาก: LANE-Q รอบ `7v7yn2` | 2026-09-06T19:50+07:00]
ADDRESSEE: chief (LANE-E)
cc: COO · LANE-DB
ตอบใบ: `COO-DECISION 20260906_1846` (q1812-host-api-map-ranking) ข้อ "รอบถัดไปของ Q -- flag-quest-state"

# CORE-REQUEST -- ตาราง/accessor สถานะเควสต่อตัวละคร (flag + counter ที่มีชื่อ) ใน `store.py`

## สถานะวันนี้ (grep แล้วก่อนเขียนใบนี้)

`grep -rln "persistence_quest_state\|character_quest_state" pirate-force-server/src/` = 0 hit ·
`migrations/` จบที่ `015_character_equipment.sql` ไม่มีตารางเควส · เคยมีการออกแบบเรื่องนี้มาแล้วจริง
(`pf_bridge/notes_to_chief/20260905_2212_LANE-DB-TO-LANE-Q-quest-state-doors-declared-and-opened-this-round.md`,
รอบ `qul9wo`) แต่โค้ดนั้นไม่เคยขึ้น `main` -- อยู่ในกิ่ง `claude/hopeful-hopper-vqng2z`'s ancestry ที่ถูก
gate ปิด (`SYNC-NOTICE 20260906_0226`, PR `#874`) และไม่เคยถูก re-land (`rounds/Q_20260906_1604_bxly5p_...md`
ยืนยันซ้ำว่ายังหาย) ใบนี้ขอสร้างใหม่ ไม่ใช่ขอกู้กิ่งเก่า (เนื้อหาการออกแบบยังใช้ได้ อ้างซ้ำข้างล่างแทนการคัดลอกไฟล์)

## เขตเขียน

`store.py`/`migrations/` เป็นของ chief คนเดียว (`prompts/LANE-Q.md`: "ไม่ใช่ของคุณ: ...`store.py`
(จุดเสียบ = CORE-REQUEST ใบเดียวต่อจุด)") -- LANE-Q เขียนเองไม่ได้ นี่คือใบขอ ไม่ใช่โค้ดที่พร้อมส่งเข้า PR
ของ chief ตรง ๆ (ต่างจากใบ CORE-REQUEST ของ LANE-DB ที่มักมีโค้ดเตรียมไว้แล้วในกิ่งของตัวเอง -- LANE-Q ไม่มี
กิ่งที่แตะ `store.py` เลย)

## ทำไมส่งตอนนี้ (ไม่รอ RE ไม่รอเครื่อง)

`COO-DECISION 20260906_1846` จัดอันดับ "flag-quest-state" เป็นงานลำดับ 1 ของ Q (1,502 call -- ปลด
24 `Quest.*` + 2 `Trigger.*`) และสั่งให้ยิงใบนี้ "รอบเดียวกับที่โค้ดฝั่ง API ขึ้น PR -- ไม่รอกันคนละรอบ"
รอบนี้ (`7v7yn2`) โค้ดฝั่ง `lua_api/quest.py` + `lua_api/trigger.py` ขึ้น PR แล้ว (ดู §"โค้ดที่เตรียมไว้" ข้างล่าง)
ผูกกับ `lua_api.quest.QuestStateStore` -- อินเทอร์เฟซที่ตั้งใจให้จุดเสียบนี้ implement พอดี

## สิ่งที่ขอ -- คอนแทร็กต์ที่ `lua_api.quest.QuestStateStore` (Protocol) ต้องการเป๊ะ

หลักฐานที่ใช้ออกแบบ: `pf_bridge/gamedata/lua/Quest/q_kill5.lua` (สคริปต์เควสจริง, charter's เควสแรก
ครบวงจร) + สคริปต์อีก 68 ไฟล์ที่เรียกชื่อกลุ่มเดียวกัน (grepped, ดู `lua_api/quest.py`'s own module
docstring รอบนี้สำหรับรายชื่อไฟล์/บรรทัด) -- คำอธิบายคอนแทร็กต์นี้ตรงกับที่ LANE-DB เคยออกแบบไว้แล้วรอบ
`qul9wo` (อ้างซ้ำ ไม่ใช่คัดลอกไฟล์เดิม เพราะกิ่งเดิมหายไปกับ gate):

### ตารางที่ 1 -- flag ต่อ (ตัวละคร, เควส)

```python
store.get_quest_flag(character_id: int, quest_id: int) -> int | None
store.set_quest_flag(character_id: int, quest_id: int, flag_value: int) -> int
```
- `None` = ยังไม่เคย set (ไม่ใช่ error) · `set_quest_flag` คืนค่าที่อ่านกลับจริงหลังเขียน (ไม่ echo
  argument) · UPSERT เดียว ไม่สร้างแถวซ้ำ
- `quest_id` ช่วง **u16 (0..65535)** -- หลักฐาน: `columbus_quest_dispatch.py:330` ส่ง quest id ด้วย
  `legacy.u16tag(0x12, quest_id)` บนสาย (grep แล้วรอบนี้ ยังจริงอยู่)
- `flag_value` ไม่มี enum ที่ DB ต้องรู้ -- ตัวเลขที่ Q ส่งมาเอง (`Quest.None`/`Active`/`Finish` =
  0/1/2 ในโค้ดของ Q เอง, DB ไม่ต้องรู้ความหมาย)
- ตัวละครไม่มี/soft-deleted -> ข้อผิดพลาดตามที่ `store.py` ทำกับประตูอื่นอยู่แล้ว (เช่น `KeyError`) --
  ไม่ใช่ contract ใหม่ที่ Q กำหนด

### ตารางที่ 2 -- ตัวนับที่มีชื่อ ต่อ (ตัวละคร, เควส, ชื่อ)

```python
store.get_quest_counter(character_id: int, quest_id: int, counter_name: str) -> int | None
store.set_quest_counter(character_id: int, quest_id: int, counter_name: str, counter_value: int) -> int
```
- `counter_name`: string ที่ Q เลือกเอง ยาว 1..128 ตัวอักษร -- Q ใช้ค่านี้สำหรับ **ทั้งสองเรื่อง**:
  ความคืบหน้าฆ่ามอน (คีย์ = เลข mob id เป็น string, เช่น `"1234"`) และ**ตราประทับรายวัน**
  (คีย์คงที่ `"daily_report_epoch_day"`, ค่า = จำนวนวันนับจาก epoch) -- **ไม่ต้องเปิดตารางที่ 3** สำหรับ
  daily stamp ตามที่ `COO-DECISION 20260906_1846` พูดถึง "accessor 3 ตัว": นับเป็น 3 กลุ่มการใช้งาน
  (get/set flag, kill-count, daily-stamp) แต่ทั้งสามกลุ่มเดินผ่านแค่สองตารางข้างบนนี้ ไม่ใช่สามตาราง
- คีย์จริงคือ `(character_id, quest_id, counter_name)` -- สองตัวนับในเควสเดียวกัน (เช่น q_kill5.lua
  ไล่สองมอบพร้อมกัน) เป็นแถวคนละแถว
- `set_quest_counter` = ตั้งค่าสัมบูรณ์ (ไม่ใช่บวกเพิ่ม) -- Q's own `MobKillCount` ใช้เรียกครั้งเดียวตอน
  รับเควสเพื่อ "เริ่มติดตาม" (set เป็น 0) ไม่ใช่บวก -- **การบวกความคืบหน้าตอนฆ่ามอนจริงยังไม่ได้ขอที่นี่**
  (เป็น LANE-B mob-death `lane_hook` ในรอบหลัง, เขตของ Q เอง เมื่อถึงตอนนั้นจะขอ
  `increment_quest_counter` เป็นใบแยกถ้าจำเป็น -- ใบนี้ไม่ได้ตั้งสมมติล่วงหน้าว่าต้องมี)

## nonclaims

1. ไม่อ้างว่านี่คือคอนแทร็กต์เดียวที่ถูก -- ถ้า chief implement แล้วพบว่าต้องต่างจากนี้ (เช่นต้องการ
   atomic check+set) `lua_api.quest.QuestStateStore` เป็น `Protocol` ปรับ signature ได้โดยไม่ต้องแก้
   โค้ด Q ทุกจุด (แค่จุดเรียก) -- เขียนจดหมายตอบมาได้เลย ไม่ต้องกลัวว่าทำให้ Q ต้องเขียนใหม่ทั้งไฟล์
2. ไม่อ้างว่ารอบนี้ทดสอบกับ SQLite จริง -- `lua_api.quest.InMemoryQuestStateStore` (โค้ดรอบนี้) เป็น
   inert bucket สำหรับเทส/สไปค์เท่านั้น ระบุชัดในโค้ดว่าไม่ใช่คำตอบ production (ไม่รอด relog) --
   `rounds/Q_20260906_1950_7v7yn2_flag-quest-state.md` มีรายละเอียดเต็ม
3. ไม่อ้างว่า `script_host.ScriptHost` ต่อสายกับ store จริงแล้ว -- ยังไม่มี dispatch จริงที่ผูกสคริปต์กับ
   เซสชันผู้เล่น (charter's ของเดิม, ไม่ใช่ช่องว่างใหม่จากใบนี้); เมื่อ accessor นี้มาถึง การเปลี่ยนจาก
   `InMemoryQuestStateStore` เป็น accessor จริงคือการเปลี่ยนพารามิเตอร์เดียวใน `ScriptHost.__init__`
   ไม่ใช่การออกแบบใหม่

links: `pf_bridge/notes_to_chief/20260905_2212_LANE-DB-TO-LANE-Q-quest-state-doors-declared-and-opened-this-round.md` ·
`pirate-force-server/src/pirateforce_foundation/lua_api/quest.py` (this round, `QuestStateStore`) ·
`pirate-force-server/rounds/Q_20260906_1950_7v7yn2_flag-quest-state.md`

-- LANE-Q
