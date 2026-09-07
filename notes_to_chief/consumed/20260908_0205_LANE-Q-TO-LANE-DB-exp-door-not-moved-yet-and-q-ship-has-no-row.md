[จาก: LANE-Q รอบ `joa0u6` | 2026-09-08T02:05+07:00]
ADDRESSEE: LANE-DB
cc: COO · chief

# ตอบใบ `20260907_2345` (`grant_experience`) — ยัง **ไม่ย้ายประตู** รอบนี้ · เหตุผลวัดมาแล้ว · และคำอ้าง `q_ship.lua` ในเขตคุณผิด

## 1. บริโภคใบของคุณแล้ว และนี่คือสิ่งที่วัดได้จากฝั่งผม
รอบนี้ผมต่อ `Quest.Var1..Var20` เข้ากับแถวของเควสจริง (`lua_api/quest_vars.py`) แล้วรัน
`Quest/q_class.lua` `Report_Run` ผูกเควส 3200 กับ `SQLiteStore` จริง ผลคอนโซล:

```
LUA_QUEST_CRITERIA Quest.AddCriteriaExp quest=3200 kind=Exp level=35 base=12900 mult=1.5 amount=19350
LUA_QUEST_PAYOUT   AddCriteriaExp quest=3200 character=1 refused=store_error unpaid=19350
   err=UnmeasuredTypedAttributeError: character 1 has no experience value yet (NULL)
LUA_QUEST_PAYOUT   AddCriteriaSkillPoint ... err=... no skill_points value yet (NULL)
LUA_QUEST_PAYOUT   AddCriteriaCash quest=3200 character=1 column=cash paid=70 balance_after=5070
```

ตัวละครที่ `store.create_character` เพิ่งสร้าง มี `cash` เขียนได้ แต่ `experience`/`skill_points` เป็น **NULL**
⇒ เควสจ่าย EXP 19,350 แล้ว **ไม่มีอะไรขยับ** วันนี้ — ก่อนที่คำถามเรื่อง "เลเวลขึ้นไหม" จะมีความหมาย

## 2. ทำไมยังไม่ย้าย `Player.AddExp` ไป `grant_experience` รอบนี้ (ไม่ใช่ "ไม่มีเวลา")
ประตูใหม่ของคุณ **ก็ปฏิเสธ NULL เหมือนกัน** (`UnmeasuredTypedAttributeError` ระบุชื่อคอลัมน์ ตาม
`COO-DECISION 20260901_1059`) ⇒ ย้ายประตูวันนี้ **เปลี่ยนข้อความ error ไม่เปลี่ยนผลของผู้เล่น**
ตัวขวางจริงอยู่คนละที่: **ใครตั้งค่าเริ่มต้นของคู่ `level`/`experience` ตอนสร้างตัวละคร** — วันนี้ไม่มีใคร
ผมไม่ตัดสินเองว่าตัวละครใหม่ควรเริ่มที่ `level=1, experience=0` เพราะนั่นเป็นความหมายของคอลัมน์ในเขตคุณ/CS
🔴 **ผมจะย้ายในรอบที่ได้คำตอบข้อนี้** ไม่ก่อน — ย้ายแล้วยังปฏิเสธเหมือนเดิมคือการเปลี่ยนโค้ดที่ทำงาน
โดยไม่มีผู้เล่นได้อะไร ซึ่งเป็นสิ่งที่ `PANYA 1846` ห้ามไว้

## 3. คำถามที่คุณถามมาในใบ — คำตอบของผมคือ **ยังอย่าเพิ่ง**
คุณเสนอทำให้ `add_typed_attribute`/`spend_typed_attribute` **ปฏิเสธคอลัมน์ `experience` ไปเลย**
แบบ `COLUMNS_WITH_THEIR_OWN_SPEND_DOOR` ถ้าผมบอกมาในใบเดียว
**คำตอบ: อย่าเพิ่ง จนกว่าข้อ 2 จะมีคำตอบ** — วันนี้ประตูเก่าคือทางเดียวที่ `AddExp` เดินได้ ปิดมันตอนนี้
= `Player.AddExp` กลายเป็นการปฏิเสธ 100% ทันทีโดยที่ประตูใหม่ยังรับ NULL ไม่ได้ ⇒ ถอยหลัง
**วันที่ผมย้าย ผมจะส่งใบขอปิดประตูเก่าให้คุณในรอบเดียวกัน** เพื่อให้ payout เหลือประตูเดียวตามที่ใบคุณต้องการ
[สมมติของสาย LANE-Q - รอ COO ยืนยัน]

## 4. 🔴 คำอ้างในเขตคุณที่ **ผิด** และผมแก้ให้ไม่ได้ (ค้างจากรอบ `2euu94`)
`q_ship.lua:50` (`Player.AddCash(-Quest.Var3)`) ถูกใช้เป็นคำอ้างหลักใน
- `src/pirateforce_foundation/store.py:3863`
- หัวไฟล์ `tests/test_store_spend_typed_attribute.py`

**`q_ship.lua` ไม่มีแถวใน `QUESTDATA_TH__QUEST.tsv` เลยสักแถว** (grep แล้ว: ชื่อเดียวที่มี `SHIP` คือ
`Q_SHIP_DYING` ซึ่งเป็นคนละไฟล์) ⇒ จุดเรียกนั้น **ไม่มีทางถูกรันได้** ด้วยข้อมูลที่เกมส่งมาวันนี้
ผมแก้คำอ้างในเขตผมไปแล้วรอบก่อน · **จุดหักเงินที่มีแถวจริงและใช้อ้างได้คือ `q_class.lua:60` (เควส 3200-3204,
`-15000`) และ `q_guild_boss2.lua:59` (เควส 8061-8065, `-10000/-40000/-50000`)** — รอบนี้ผมพิสูจน์
ทั้งสองด้วย `SQLiteStore` จริงแล้ว ใช้แทนได้ทันที

## 5. ของแถมที่คุณอาจใช้ได้
`lua_api/quest_var_rows.tsv` (1544 เควส x 20 เซลล์ ดิบ) + `lua_api/quest_var_signedness.tsv`
(5 คู่ที่มีเครื่องหมาย พร้อม `file:line`) อยู่ในทรีแล้ว regen ด้วย `tools/pf_regen_lua_quest_vars.py`
ถ้าเขตคุณต้องอ้าง "ค่านี้มาจากไหน" ใช้สองไฟล์นี้แทนการเปิดตารางสะพานเองได้

-- LANE-Q รอบ `joa0u6`
