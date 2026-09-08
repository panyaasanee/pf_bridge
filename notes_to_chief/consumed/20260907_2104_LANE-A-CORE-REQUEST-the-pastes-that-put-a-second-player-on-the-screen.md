[จาก: LANE-A (WORLD) รอบ `q6a8oa` | 2026-09-07T21:04+07:00]
ADDRESSEE: chief (LANE-E)
cc: COO · Panya

# CORE-REQUEST — สาม paste ใน `runtime.py` ที่ทำให้ "ผู้เล่นคนที่สอง" โผล่บนจอ · รอบนี้ผมปิดคำถามค้างข้อเดียวของใบนี้แล้ว

## โทเคนว่าบล็อกมีจริง (รันได้เอง บนกิ่ง `claude/dreamy-archimedes-q6a8oa` sha `e84294f`)
```
$ grep -c "world_remote_player_actor" src/pirateforce_foundation/runtime.py
0
$ grep -c "lane_hooks.register_live_session(" src/pirateforce_foundation/runtime.py
1
$ grep -c "self.last_target_pos = (x, y, z, heading)" src/pirateforce_foundation/runtime.py
1
```
บรรทัดแรก = บล็อก: โมดูล `world_remote_player_actor` (`production_allowed = True` ไม่มีแฟล็ก ไม่มี scenario) **ไม่มีใครใน `runtime.py` เรียกเลยแม้แต่ครั้งเดียว**
สองบรรทัดหลัง = จุดเสียบที่ใบนี้ขอ **มีอยู่จริงในไฟล์วันนี้** (มีเทสปักไว้แล้วใน `tests/test_world_remote_player_actor.py`)

## ขออะไร
paste ตามตัวอักษรใน `world_remote_player_actor.PLAYER_PRESENCE_WIRING` (คงข้อความไว้ในโมดูล เพื่อไม่ให้จดหมายกับโค้ดเถียงกัน) สามจุด:
1. หลัง `lane_hooks.register_live_session(...)` ใน START_GAME_REQ → `register_presence_for_character(self.foundation.selected)`
2. ใน `_vital_walk_promote_target_pos` หลัง `self.last_target_pos = (x, y, z, heading)` → `register_presence_for_character(self.foundation.selected, position=(x, y, z))`
3. บนเส้นทาง arrival: ต่อท้าย actions ด้วยเฟรมจาก `compose_other_live_players_frame(legacy, scene_id, self.foundation.selected.id)` เมื่อ `actor_count` ไม่เป็นศูนย์
+ หนึ่งจุด disconnect → `clear_player_presence(scene_id, character_id)`

## สิ่งที่เปลี่ยนไปจากใบเดิมของสายผม (นี่คือเหตุผลที่ส่งใบนี้รอบนี้)
ข้อความ `PLAYER_PRESENCE_WIRING` เดิม **มีช่องว่างให้คนแปะต้องตัดสินใจเอง**: `<current hp>`, `<max hp>`, `<name>` และประโยคที่เขียนไว้เองว่า "การอ่าน HP pair ยังไม่มีที่มาที่เดียวชัด ๆ — เป็นคำถามเปิดข้อเดียวของใบนี้"
รอบนี้ผมปิดคำถามนั้นด้วยโค้ดของสายผมเอง ไม่ใช่ด้วยการเดา:
- `hp_pair_for_character()` อ่าน `hp_current`/`hp_max` ของแถวตัวละคร ถ้าล็อกอินของแถวนั้นส่งมา
- ถ้าแถวไม่มีทั้งคู่ (= สภาพปกติของแถวที่โหลดจาก DB) ใช้ `player_wire.PLAYER_LOGIN_HP_CURRENT/_HP_MAX` — **ค่าเดียวกับที่ไคลเอนต์ของตัวละครนั้นกำลังแสดงอยู่** ตามกฎ ALL-OR-NONE ของ `PANYA-DECISION 20260901_1059` ที่เขียนไว้ใน `model.Character` เอง
- ครึ่งคู่ (มีตัวเดียว) = ปฏิเสธโดยมีชื่อ ไม่เอาค่าคงที่มาเติมครึ่งที่ขาด
- **ศูนย์ = ปฏิเสธ** เพราะ `HP == 0` คือ death predicate ของไคลเอนต์ (Q1: 0x43BD7A/0x43BDAA) — ผู้เล่นคนที่สองที่ HP 0 คือคนตายในสมุดโลกที่ทุกเฟรมหลังจากนั้นอ่านต่อ
⇒ ตอนนี้ทั้งสาม paste **ไม่มีตัวแปรให้เติมเลยแม้แต่ตัวเดียว** และไม่มีจุดไหนที่ `runtime.py` ต้องอ่านฟิลด์ของแถวเอง

## nonclaim (เขียนไว้ก่อนถูกถาม)
- ยังไม่มีไคลเอนต์ตัวไหนเคยเห็น actor_type 2 ของโปรเจกต์นี้ — ใบนี้ไม่ได้อ้างว่า "ผู้เล่นคนที่สองจะเรนเดอร์แน่" อ้างแค่ว่าไบต์ถูกประกอบจากสมุดโลกจริงและถึงมือ session อีกคนไม่ได้เพราะไม่มีจุดเสียบ
- paste ข้อ 3 ส่งถึง **เฉพาะ session ที่เพิ่งเข้าฉาก** · การ broadcast ให้คนที่ยืนอยู่ก่อนต้องมีคิวข้ามเธรด ซึ่งใบนี้ **ไม่ได้ขอ** และไม่ได้ตัดสินใจแทนคุณ
- HP pair ที่ประตูนี้ตอบคือค่าที่ไคลเอนต์ของตัวละครนั้นถูกบอกตอนล็อกอิน ไม่ใช่ HP สดจากคอมแบต — สายที่เป็นเจ้าของ HP สด (B/DB) เขียนทับได้ผ่าน `register_player_presence` ตัวเดิมโดยไม่ต้องแก้ประตูนี้

-- LANE-A รอบ `q6a8oa`
