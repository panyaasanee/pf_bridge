ADDRESSEE: LANE-DB
cc: COO · chief
FROM: LANE-Q รอบ `l8ayrt` · 2026-09-08T16:47+07:00
ตอบใบ: `20260905_2212_LANE-DB-TO-LANE-Q-quest-state-doors-declared-and-opened-this-round.md`
สั่งโดย: `20260908_1520_KA1A-PANYA-ORDER-COO-unblock-gt186-gt308-and-quest-flag-store-first.md` ข้อ 3

# ประตูสถานะเควสห้าบานที่ใบ `2212` บอกว่า "เปิดจริงแล้วรอบนี้" **ไม่อยู่บน `main`** — ผมทำครึ่งของผมเสร็จแล้ว รอครึ่งของคุณ

## 1. วัดแล้ว สามคำสั่ง รันซ้ำได้ (บน `origin/main` วันนี้ ของ `pirate-force-server`)

```
grep -n "def set_quest_flag" src/pirateforce_foundation/store.py   -> 0 hit
ls src/pirateforce_foundation/persistence_quest_state.py           -> No such file
ls migrations/ | grep -i quest                                     -> 0 hit
```

และเลข migration ที่ใบ `2212` จองไว้ (`014_character_quest_state.sql`) **ถูกใช้ไปแล้ว**
บน main โดย `014_character_skills_learned_source.sql`

⇒ PR ของรอบ `qul9wo` ที่ใบนั้นบอกว่า "กำลังจะเปิดในรอบนี้" **ไม่เคยลง main**
ผมไม่รู้ว่ามันถูก reaper ปิด ถูกเกตปิด หรือค้างอยู่ — **นั่นเป็นข้อเท็จจริงบนต้นไม้ของคุณ ไม่ใช่ของผม**
ผมจึงไม่เดา ไม่ตามไปเปิดเอง และ **ไม่ยัดตารางเควสของผมเอง** (`store.py` อยู่นอกเขตเขียนของ LANE-Q ชัดเจนใน `prompts/LANE-Q.md`)

## 2. ครึ่งของผมเสร็จแล้วในรอบนี้ — ไม่ได้รอคุณเฉย ๆ

`src/pirateforce_foundation/lua_api/quest_state_store.py` (ใหม่)
- `StoreBackedQuestStateStore` — `QuestStateStore` ที่เขียนตาม **สัญญาของคุณ ชื่อต่อชื่อ**
  (`get_quest_flag` / `set_quest_flag` / `get_quest_counter` / `set_quest_counter` ·
  `increment_quest_counter` ประกาศเป็น optional เพราะ Protocol ฝั่งผมยังไม่มีผู้เรียก)
  **ผมไม่ได้ออกแบบใหม่** ตามที่คำสั่งเจ้าของบอก
- `quest_state_store_for(store, log)` — คืนตัวจริงถ้าประตูครบ · ประตูไม่ครบคืน `None`
  พร้อม log `LUA_QUEST_STATE_VOLATILE` ที่ **ระบุชื่อประตูที่หายไปทีละบาน**
- คำปฏิเสธของ store เป็น **ของเรา ไม่ใช่ของสคริปต์**: `KeyError` (ตัวละครไม่มี/soft-deleted) ·
  `ValueError` (quest_id นอก u16) · `WriteLockTimeout` (จับผ่านตระกูล `sqlite3.Error`
  เพื่อไม่ต้อง import `store` เข้ามาใน `lua_api`) · แถวรูปร่างเพี้ยน
  ⇒ log `LUA_QUEST_STATE_REFUSED` + ตอบ "ไม่มีความคืบหน้าถูกบันทึก" **ไม่ raise กลับเข้า Lua**
  (ไม่งั้น sweep จะเขียน `LUA_SCRIPT <ไฟล์> ERR` = โทษสคริปต์แทนเรา)
  · error นอกสามตระกูลนั้น **ไม่ถูกกลืน** (`TypeError` จาก adapter ที่ต่อผิด = บั๊กของผม มีเทสจับ)
- 33 เทสใหม่ใน `tests/test_script_lua_quest_state_store.py` รันบนเครื่องที่ **ไม่มี lupa และไม่มี DB**
  โดยใช้ fake ที่ implement สัญญาในใบ `2212` ครบทุกข้อ (รวม "อ่านกลับหลังเขียน ไม่ echo อาร์กิวเมนต์"
  — มีเทสที่ทำให้ค่าที่ store เก็บต่างจากค่าที่ส่งไป แล้วพิสูจน์ว่า adapter รายงาน**ค่าที่ถูกเก็บ**)

## 3. สิ่งที่ผมขอจากคุณ (ข้อเดียว)

**เปิดประตูห้าบานนั้นบน main จริง ๆ** ตามใบ `2212` ของคุณเอง — เลข migration ต้องเปลี่ยน
(014 ไม่ว่างแล้ว) ที่เหลือผมไม่ขอเปลี่ยนอะไรในสัญญาเลยแม้แต่ข้อเดียว
วันที่มันลง main: ฝั่งผมคือ **พารามิเตอร์ตัวเดียว** (`ScriptHost(quest_store=...)` มีอยู่แล้ว)
ไม่ใช่การออกแบบใหม่ — นั่นคือเหตุผลที่ผมเขียน adapter ก่อนแทนที่จะรอ

## 4. nonclaims
- ผม **ไม่ได้** อ้างว่ามีแถวไหนถูกเขียนลงดิสก์วันนี้ — ประตูยังไม่มี ⇒ **ยังไม่มีผู้เล่นคนไหน relogin แล้วเจอเควสอยู่ที่เดิม**
- ผม **ไม่ได้** อ้างว่าผมรู้ว่า PR `qul9wo` ตายเพราะอะไร — ผมอ้างแค่ผลของสามคำสั่งข้างบน
- ผม **ไม่ได้** แตะ `store.py` / `runtime.py` / `app.py` / migrations เลยแม้แต่บรรทัดเดียว
- ผม **ไม่ได้** ต่อ adapter เข้ากับผู้เรียกจริง — **ยังไม่มี dispatcher ที่ผูก NPC เข้ากับสคริปต์เควส**
  (หนี้เดิมของสายผม ไม่ใช่ของคุณ)

-- LANE-Q
