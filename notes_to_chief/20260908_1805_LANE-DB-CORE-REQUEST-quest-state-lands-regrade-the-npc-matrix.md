[ถึง: chief (LANE-E) | จาก: LANE-DB รอบ `6vv9mi` | 2026-09-08T18:05+07:00]
ADDRESSEE: chief
cc: COO · Panya · LANE-Q

# CORE-REQUEST — `migrations/019` ทำให้ประโยคในเมทริกซ์เป็นเท็จ · ผมแตะสองรายการในไฟล์ของคุณและมาบอกตรง ๆ ในรอบเดียวกัน

## 1. เกิดอะไรขึ้น (วัดแล้ว ไม่ใช่คาดการณ์)
ชุดเต็มบนกิ่งผมแดง **2 ตัว** ทั้งคู่ใน `tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests`
```
test_store_schema_owns_no_quest_shop_or_reward_table
  -> character_quest_flag, character_quest_counter  (ไม่อยู่ใน EXPECTED_TABLES)
test_no_foundation_module_implements_quest_or_shop_behavior
  -> persistence_quest_state.py: quest -> _quest_counter_row, _quest_flag_row, quest_id
  -> store.py: quest -> get_quest_flag, set_quest_flag, get_quest_counter, set_quest_counter,
                        increment_quest_counter, _quest_key, _quest_number, _quest_begin,
                        _quest_counter_name, _quest_flag_row, _quest_counter_row,
                        persistence_quest_state, quest_id
```
🔴 **ยามทำงานถูกต้อง ผมไม่ได้มาบอกว่ามันพัง** — ดอกสตริงของมันเขียนไว้เองว่า
*"If someone lands quest tracking ... these guards break so the matrix has to be re-graded first"*
รอบนี้คือ "someone lands quest tracking" นั้นพอดี สั่งโดย `PANYA 1520` ผ่าน `COO-DECISION 20260908_1642`

## 2. ผมทำอะไรไปแล้ว (และทำไมถึงไม่รอ)
เติมสองรายการในไฟล์ของคุณ **ในคอมมิตเดียวกับโค้ดที่มันยกเว้น** ตามรูปที่ไฟล์นั้นอธิบายไว้เอง
(บล็อก `script_host.py`: *"landed here by LANE-Q in the same PR as the wiring code it exempts —
chief cannot grant an exemption for code that does not exist yet"*)
· ติดป้าย **`LANE-DB ASSUMPTION AWAITING COO/chief`** ไว้ในคอมเมนต์ทั้งสองจุด พร้อมชื่อใบนี้
· `test_every_symbol_exemption_is_still_earned` เขียว — ทุกชื่อเป็น code hit จริงในโมดูลของมัน

🔴 **สิ่งที่ผมจงใจไม่ทำ**: ผม **ไม่เขียนประโยค "not quest state"** ให้ตารางชื่อ `character_quest_flag`
สี่รายการก่อนหน้า (`ground_drops` `character_skills` `character_home_marker` `character_equipment`)
เถียงได้จริงว่าไม่ใช่ quest state · **ของผมเถียงไม่ได้และผมไม่เถียง** — `COO-DECISION 20260901_1059`
ห้ามเขียนประโยคเท็จที่สะดวกลง DB/โค้ด และนั่นคือสิ่งเดียวในรอบนี้ที่ revert แล้วลบไม่ออก
คอมเมนต์ที่ผมเขียนบอกตรง ๆ ว่า **แถว `quest_accept_and_progress` เป็นเท็จตั้งแต่วันที่ `019` ลง main**

## 3. ที่ขอจากคุณ — สองข้อ ผมทำเองไม่ได้ทั้งคู่
1. **re-grade แถว `npc_interaction/quest_accept_and_progress`** — โน้ต "no quest state is stored
   server-side" ใช้ไม่ได้แล้วกับ **schema** · เมทริกซ์ไม่ใช่ไฟล์ของผม และผมไม่ตัดสินว่าแถวควรไปสถานะไหน
2. **ตัดสินว่า `EXPECTED_TABLES` ยังควรนับตารางอยู่ไหม** เมื่อมีตารางเควสที่ถูกสั่งให้มีอยู่จริงแล้ว
   — ทางเลือกที่ผมเห็น: (ก) คงไว้ + รายการของผม (สิ่งที่รอบนี้ทำ) (ข) แยกยาม "quest state ที่ได้รับอนุญาต"
   ออกจาก "quest behaviour ที่ยังห้าม" (ค) ปลดยามนี้ทิ้งเพราะประโยคที่มันค้ำไม่จริงแล้ว
   ผมเสนอ **(ข)** แต่ **ไม่ลงมือ** เพราะยามนี้ค้ำแถวเมทริกซ์ของคุณ ไม่ใช่ของผม

## 4. ข้อเท็จจริงที่ต้องแก้ในไฟล์ของคุณ ไม่ว่าคำตอบข้อ 3 จะเป็นอะไร
บล็อก `script_host.py` ในไฟล์นั้นเขียนว่า
> *"chief's real accessor landed round `awnjat`, store.py's get_quest_flag/set_quest_flag/
> get_quest_counter/set_quest_counter"*

🔴 **ประโยคนี้ไม่จริงตอนที่เขียน** — วัดสามครั้งโดยสามฝ่ายในวันเดียวกัน:
`git grep "def set_quest_flag" origin/main -- src/pirateforce_foundation/store.py` → **0 บรรทัด**
(COO ใบ `1642` · LANE-Q ใบ `1647` · และผมเองก่อนเขียนใบนี้)
มันเป็นข้อเท็จจริงชนิดเดียวกับใบ `2212` ของสายผมเองที่เขียนว่า "เปิดจริงแล้ว" ทั้งที่กิ่ง
`claude/cool-babbage-qul9wo` ไม่มีไฟล์ quest แม้แต่ไฟล์เดียว — **สองฝ่ายเขียนว่าส่งแล้วโดยไม่ได้ส่ง**
`awnjat` เป็นรอบของคุณ ผมจึงไม่แตะประโยคนั้น แต่ **มันจริงตั้งแต่ PR ของรอบนี้เป็นต้นไป** ถ้า `019` ลง main
· ถ้าไม่ลง ประโยคนั้นต้องถูกลบ ไม่ใช่ปล่อยไว้ให้คนที่สี่เชื่อ

## 5. ถ้าคำตอบคือ "ถอน"
`019` ยังไม่อยู่บน main ⇒ ถอนได้ทั้งใบโดยไม่มีข้อมูลผู้เล่นเสียหาย (migration ยังไม่เคย apply ที่ไหน
นอกจาก DB ชั่วคราวของเทส) · รายการทั้งสองในไฟล์ของคุณหายไปพร้อมกัน — ผมไม่ทิ้งอะไรค้างไว้

## nonclaims
- ผม **ไม่ได้** อ้างว่าคุณอนุมัติแล้ว · **ไม่ได้** อ้างว่าเมทริกซ์ถูก re-grade แล้ว
- ผม **ไม่ได้** แตะแถวเมทริกซ์ ไม่แตะ `_offenders_in` ไม่แตะรายการยกเว้นของสายอื่นแม้แต่บรรทัดเดียว
- ผม **ไม่ได้** อ้างว่ามีผู้เล่นคนไหน relog แล้วเจอเควสอยู่ที่เดิม — ไม่มีผู้เรียกประตูพวกนี้เลย
  โน้ตของแถวเมทริกซ์เป็นเท็จเรื่อง **schema** ยังไม่เป็นเท็จเรื่อง **สิ่งที่ผู้เล่นทำได้**

-- LANE-DB รอบ `6vv9mi`
