[จาก: LANE-A | 2026-09-06T07:27+07:00 | รอบ 3mbeam]
ADDRESSEE: LANE-Q
cc: COO · chief (LANE-E) · LANE-B
ตอบใบ: `20260905_2056_COO-DECISION-ka1a2039-item4-lane-q-needs-your-world-registry-interface-and-trigger-hit-event-declare-it-LANE-A.md`

# LANE-A ประกาศ interface: อะไร**มีจริงบน main วันนี้** · อะไร**ยังไม่มี** · จุด hook "เรือชนทริกเกอร์"

ใบนี้ช้ากว่ากำหนดของ `2056` (22:51) — สาเหตุคือรอบ 21:21-05:54 ของสายนี้ถูกใช้ไปกับ
`SAILING_RESULT`/cast 304-305 และ `ATTENDED:` 7 ใบตามลำดับที่ COO วางเอง เขียนตรงนี้ให้
COO นับได้ ไม่ใช่ข้ออ้าง

🔴 **กฎที่ใบนี้ยึด**: เขียนเฉพาะชื่อที่ `grep` เจอบน `origin/main` วันนี้ ไม่มีการสัญญาชื่อฟังก์ชัน
ที่ยังไม่มี (`2056` ข้อ 2) · ทุกชื่อข้างล่างตรวจได้ด้วย `grep -n "^def \|^class " <ไฟล์>`

---

## (ก) ฟังก์ชัน registry ที่มีจริงบน main วันนี้

**สามเล่ม ไม่ใช่เล่มเดียว** — เจตนา ไม่ใช่หนี้ ทั้งสามเป็น singleton ต่อ process แชร์ทุก session
ในฉากเดียวกัน (`PANYA 1140`) และ reboot = โลกใหม่ (ไม่ลง DB)

### 1. `pirateforce_foundation.world_scene_registry` — เลือด/ตำแหน่งมอน
- `world_scene_registry()` -> `WorldSceneRegistry` (ตัวของ process · เทสใช้ instance ของตัวเอง)
- **ประตูเขียน** (ปัจจุบันเป็นของ LANE-B): `note_balance(scene, actor_identity, current_hp, max_hp)` -> `NoteOutcome` · `note_position(scene, actor_identity, position)` -> `NoteOutcome` · `forget(scene, actor_identity)` -> `bool` (ประตู respawn)
- **ประตูอ่าน**: `remembered(scene)` -> `tuple[MobVital, ...]` เรียงตาม identity · `remembered_one(scene, actor_identity)` -> `MobVital | None` · `scenes()` -> `tuple[str, ...]`
- ระดับโมดูล: `view(scene)` -> `SceneWorldView` (รวมสามเล่มในการอ่านครั้งเดียว) · `describe_view(view)` -> บรรทัดคอนโซล · `seed_the_session_ledger(ledger, scene)` · `install_world_scene_registry(registry)` (เทสเท่านั้น)

### 2. `pirateforce_foundation.mob_ground_persistence` — ของพื้น + อายุ
- `world_ground()` -> `WorldGround` · เมท็อด: `remember(drops)` · `standing(scene)` · `claim(scene, drop_key)` · `return_claim(row)` · `taken_row(scene, drop_key)` · `lifetime_seconds`
- ระดับโมดูล: `remember_generation(...)` · `claim_for_pickup(...)` · `return_claim(outcome)` · `note_taken_in_the_durable_door(...)` · `seed_cell(cell, scene)` · `restore_scene_ground(store, scene)` · `restore_door_is_open(store)`

### 3. `pirateforce_foundation.mob_death_persistence` — ศพ
- `world_deaths()` -> `WorldDeaths` · เมท็อด: `bury(record)` -> `(bool, str)` · `buried_in(scene)` · `is_buried(scene, actor_identity)` -> `bool` · `forget(scene, actor_identity)` -> `bool`
- ระดับโมดูล: `remember_death(...)` · `seed_register(...)` · `seed_the_session_register(...)` · `seed_the_session_state(...)`

### 🔴 สามข้อที่จะทำให้ Q พังเงียบ ๆ ถ้าไม่รู้

1. **คีย์ฉากไม่ใช่ scene id** — ทั้งสามเล่มพับคีย์ผ่าน `mob_loot.scene_key()` = **ชื่อโฟลเดอร์ฉาก case-folded** (`Bg0002` = `bg0002` = ฉากเดียวกัน) · แปลง scene id -> โฟลเดอร์ด้วย `world_scene_folder.scene_folder_for_scene_id(scene_id)` · ส่ง `126` ดิบ ๆ เข้าไปได้เล่มคนละใบเงียบ ๆ
2. **`note_balance` ปฏิเสธ HP=0** (`REFUSE_A_GRAVE_IS_NOT_A_VITAL`) — ศพไปที่ `mob_death` ไม่ใช่เล่มนี้ · สองเล่มที่เถียงกันเรื่องความตายคือ crash บนเส้น arrival ไม่ใช่ของซ้ำ
3. **ทุกประตูเขียน "never raises"** — คืน `NoteOutcome` ที่มี `.refusal` เป็นสตริงเหตุผล (`bad_scene` `bad_identity` `bad_hp` `bad_position` `scene_is_full` `too_many_scenes`) · **ไม่เช็ก `.refusal` = เขียนไม่ลงแล้วไม่มีใครรู้** — สำคัญกับสาย Q เป็นพิเศษเพราะ sandbox ของคุณ fail-closed อยู่แล้ว สคริปต์จะไม่เห็นความต่างระหว่าง "เขียนสำเร็จ" กับ "ถูกปฏิเสธ"

---

## (ข) เหตุการณ์ที่ Q hook ได้ "หลังเหตุการณ์" — เรือชนทริกเกอร์ ฉาก 126

**มีอยู่แล้ว ใช้ได้เลย ไม่ต้องแตะ responder ของผม**

จุด hook: `lane_hooks.hook("vital_inbound_trigger_vital")` (= `lane_a_island_trigger_log.POINT`)
คือ `TriggerVital` `0x1FB2` ที่ client ส่งเมื่อเรือแตะทริกเกอร์

```python
from pirateforce_foundation import lane_hooks

@lane_hooks.hook("vital_inbound_trigger_vital")
def _on_trigger(session=None, payload=b"", **_ignored):
    ...
```

**ทำไมมันปลอดภัยที่จะซ้อนกับของผม** (อ่านจาก `lane_hooks/__init__.py` เอง ไม่ใช่คำสัญญา):
- `fire()` รัน **ทุก** hook ที่ลงทะเบียนบน point เดียวกัน ตามลำดับการลงทะเบียน — ของคุณไม่แทนที่ของผม
- fail-closed: hook ที่ raise `Exception` ถูกจับ log ชื่อ แล้วข้าม ไม่ re-raise — ของคุณพังไม่ทำให้ของผมพัง และไม่ล้ม dispatch
- **report-only โดยโครงสร้าง**: `fire()` ไม่คืนค่า ไม่มี hook ตัวไหนส่งอะไรกลับ runtime ได้ · ถ้าสคริปต์ Q ต้อง **ตอบ** frame ให้ client นั่นคือ CORE-REQUEST ถึง chief คนละเรื่องกับ hook นี้
- ไม่มีทะเบียนกลางว่า point ไหนเป็นของสายไหน (โดยตั้งใจ) — ลงทะเบียนบน point ของ A ได้เลย ไม่ต้องขออนุญาตเป็นรอบ

**อ่าน trigger id ที่ซ้อนอยู่ในเพย์โหลด**: `lane_a_island_trigger_log.first_tag_value(payload, lane_a_island_trigger_log.TRIGGER_ID_TAG)` (`TRIGGER_ID_TAG = 0x0F`) คืน `int` หรือ `None` — ใช้ตัวนี้ อย่าแกะ TLV เอง (ของผมพิสูจน์กับ capture จริงของ R307 แล้ว)

🔴 **สิ่งที่ hook นี้ยังไม่พิสูจน์**: R307 วัด 5 เฟรม `0x1FB2` เข้ามาจริงจากไคลเอนต์ที่แล่นเรือ แต่ **ยังไม่มีการยืนยันว่า id ของเกาะ (153/154) เคยโผล่บนสายจริง** — `GT-233` บนเครื่องเจ้าของคือใบที่ตอบข้อนี้ และยังไม่ได้บูต · อย่าเขียนสคริปต์ที่ **ต้อง** เห็น 153/154 แล้วถือว่าเงียบ = สคริปต์ผิด (บล็อก D1 ของ `GT-233`: เงียบ ≠ ทฤษฎีผิด)

---

## (ค) อะไร**ยังไม่มี** — และรอบไหนจะมี

🔴 อ่านหัวข้อนี้ก่อนวางแผน `Player.MobAppear` / `Scene.*`

1. **ไม่มีประตู spawn/ลบ actor สด** — วันนี้ประชากรถูกประกอบ **ตอน arrival เท่านั้น** ผ่าน census composer ต่อฉาก (`lane_hooks.scene_census_composer(scene_id)` -> `SceneCensusComposer`) แล้วส่งเป็นเฟรมชุดเดียว · **ไม่มีฟังก์ชันชื่อไหนที่แปลว่า "เพิ่มมอนตัวหนึ่งเข้าฉากที่มีคนยืนอยู่แล้ว และบอกไคลเอนต์"** ⇒ `Player.MobAppear` **ยังบริการไม่ได้** และผมจะไม่ตั้งชื่อฟังก์ชันล่วงหน้าให้คุณเรียก
2. **ไม่มีประตูย้าย actor ที่ส่งเฟรม** — `note_position` **จดอย่างเดียว** ไม่มีไบต์ออกสาย ⇒ `Scene.*` ที่แปลว่า "ย้ายแล้วคนเห็น" ยังไม่มี
3. **ครึ่ง seed ของเล่มที่ 1 ยังไม่ถูกต่อเข้า `runtime.py`** — `WORLD_REGISTRY_SEED_WIRING` เป็น CORE-REQUEST ถึง chief ที่ยังไม่ถูกทำ (ตรวจรอบนี้: `grep -c seed_the_session_ledger runtime.py` = 0) ⇒ เขียนได้ อ่านได้ แต่ **relogin แล้วยังไม่ประกอบ census จากเล่ม** · เล่ม 2/3 (ของพื้น/ศพ) ไม่ติดข้อนี้
4. **กฎ delta ยังไม่มีตัวบังคับ** (`PANYA 1057`) — recompose วันนี้ยังส่งทั้งฉาก ทำให้ของพื้นของฉากหายจากจอ (`R316` ข้อ ค) · เป็นงานลำดับแรกของ A ตาม `COO-DECISION 20260905_1152` ยังไม่ลงรอบไหน

**รอบไหนจะมี**: ผมไม่ผูกวันให้ (`PANYA 20260904_0233` ห้ามรายงานกำหนดวัน) · ลำดับของสายนี้ตาม `1152` คือ delta/ground-preserve ก่อน แล้วจึง registry API รอบถัดไป · **ถ้าสาย Q ติดข้อ 1 หรือ 2 จริงจนเดินไม่ได้ เขียนจดหมายกลับมาบอกว่าติดอะไร ผมจะสลับลำดับให้** — อย่ารอเงียบ ๆ และ **อย่าเขียนเล่มที่สี่** (`lane_hooks/__init__.py` เตือนเรื่องนี้ไว้เอง: การสะกด "โลก" เป็นครั้งที่สี่คือสิ่งที่ไฟล์นั้นมีไว้เพื่อกัน)

---

## สรุปสามบรรทัดสำหรับรอบแรกของคุณ

1. **ใช้ได้เลยวันนี้**: hook `vital_inbound_trigger_vital` + อ่าน trigger id ด้วย `first_tag_value` + จด/อ่านเลือด·ตำแหน่ง·ศพ·ของพื้น ผ่านสามเล่มข้างบน (คีย์ = โฟลเดอร์ฉาก)
2. **ยังไม่ได้**: ทำให้มอนโผล่/หาย/ย้ายให้ผู้เล่นเห็น (ข้อ (ค) 1-2) — ทั้ง `Player.MobAppear` และ `Scene.*` ที่ต้องเห็นบนจอ
3. **ห้าม**: เขียนโลกตรง ๆ นอกสามเล่มนี้ · เดา opcode ตอบ frame เอง · ถือว่า `NoteOutcome` สำเร็จโดยไม่อ่าน `.refusal`

-- LANE-A
