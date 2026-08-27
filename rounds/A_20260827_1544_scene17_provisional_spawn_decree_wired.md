# รอบ `A_0z3kjx` - สาย A - WORLD (`pf-builder`)

**เวลา:** 2026-08-27T15:44+07:00
**สาย:** A (WORLD)
**รอบ:** `0z3kjx`

---

## ① ประโยคบังคับของสาย: ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

> **ไม่มีอะไรเปลี่ยนบนจอเกม** — Columbus (MOBS 156) ยังคุยได้เหมือนเดิม เควส 3021 ยัง refuse เหมือนเดิมทุก
> ครั้ง ไม่มีใครถูกส่งลงทะเล ไม่มีเรือ ไม่มี M2 เหตุผลตรงไปตรงมา: `dispatch_columbus_quest3021` เป็น compound
> action ที่ "ไม่ apply บางส่วน" ตามที่ออกแบบไว้เดิม (ไม่ให้ผู้เล่นลอยอยู่กลางทะเลแบบไม่มีเรือ) และช่องว่างที่สอง
> (vehicle-bind payload, `RE-096`) ยังปิดแบบ bounded-negative เหมือนเดิม — เพดาน static ถึงที่สุดแล้วจริง ไม่มี
> ทางลัด
>
> **สิ่งที่เปลี่ยนคือคอนโซล/เอกสาร ไม่ใช่จอเกม**: `dispatch_columbus_quest3021` เคย refuse ด้วย **สอง** เหตุผล
> (พิกัดขาเข้าฉาก 17 ไม่มี + vehicle-bind ไม่มี) ตอนนี้ refuse ด้วยเหตุผลเดียว (vehicle-bind เท่านั้น) เพราะ
> เจ้าของประกาศพิกัดชั่วคราว (0,0,0) เองแล้ว (`notes_to_chief/20260827_1445_PANYA-DECISION-scene17-*`) และ
> รอบนี้เพิ่งเอาค่านั้นมาต่อสายเข้า `scenarios/world_scene_registry_001.json` จริง — คนอ่านคอนโซล (bridge-side,
> ไม่ใช่ผู้เล่น) จะเห็นบรรทัดใหม่สองบรรทัดตอน dispatch ถูกเรียก: `WORLD_SCENE scene_id=17 ...` และ
> `SCENE_ENTRY scene=17 xyz=0,0,0 source=PROVISIONAL-OWNER-DECREE-20260827-1445`

---

## ② ตรวจ mailbox/คิวก่อนเริ่ม (ตามที่มอบหมาย)

อ่าน `CLIENT_RE_QUEUE.md` เต็มไฟล์ (575 บรรทัด ณ ตอนเริ่ม) — `RE-085`-`RE-098` archived/closed ทั้งหมด,
`RE-100`/`RE-102` closed bounded-negative (สาย A เอง, ยืนยันซ้ำแล้วรอบก่อน), `RE-096` closed bounded-negative
(ไม่มี VEHICLE row/semantic ผูกฉากทะเลได้ - เพดาน static ถึงที่สุด), `RE-103` **หัวใบยังเปิดอยู่จริง** (chief
cloud รอบ `4txjyg` เป็นเจ้าของ, ผล DONE/BOUNDED-NEGATIVE มาแล้วตั้งแต่ `20260827_1321` แต่หัวใบยังไม่ถูกปิด -
ไม่แตะตามกฎห้ามแก้หัวใบข้ามสาย), `RE-104` ยังเปิด (สาย GM). `GT-102` ยัง PENDING (attended capture ของบทสนทนา
Columbus - ไม่เกี่ยวกับพิกัดขาเข้า)

อ่านจดหมายล่าสุด 40 ฉบับใน `notes_to_chief/` (จนถึง `20260827_1936`) เพื่อหางานที่ยังไม่มีใครทำ พบสองอย่างสำคัญ:

1. **`20260827_1445_PANYA-DECISION-scene17-provisional-arrival-xyz-0-0-0-owner-decree-ka1-B.md`** — เจ้าของ
   ประกาศพิกัดขาเข้าชั่วคราวของฉาก 17 = (0,0,0) ภายใต้ป้าย `PROVISIONAL-OWNER-DECREE-20260827-1445` เพื่อ
   "ปลดบล็อก dispatch ข้อ 1 ของ M2" - **ยังไม่มีใครต่อสายค่านี้เข้าโค้ดจริง** ตรวจแล้ว: จดหมายรอบ `kqrlhr`
   (14:48, สามนาทีหลัง decree) consume ผล RE 6 ใบ (รวม RE-103) แต่ **เลือกไม่ต่อสาย** ตัวพิกัด - เติมแค่ `ground`
   block แล้วปล่อย `spawn: null` ไว้เหมือนเดิม (round file `A_20260827_1448_*` บรรทัด ① พูดตรงว่า "ไม่มีทางลัด
   static เหลือให้สาย A สร้างต่อโดยไม่เดาค่าที่ตารางไม่มี" - **ไม่ได้พูดถึงคำสั่งเจ้าของที่อนุญาตให้ใช้ค่านั้น
   เป็นข้อยกเว้นได้แล้ว** ดูเหมือนจะพลาดจดหมาย 1445 ไปในรอบนั้น หรือเจตนาทิ้งให้รอบถัดไป) `git log`/ไฟล์ยืนยัน
   ว่าไม่มี `.CONSUMED.txt` คู่กับจดหมายนี้เลย
2. **`20260827_1830_CHIEF-REPLY-PANYA-CHASE-0915-*`** — chief เสนอเองว่าให้สาย A "เขียนแผนต่อสายเป็นขั้น" ในรอบ
   ถัดไปของตัวเอง เพราะข้อมูลพร้อมหมดแล้ว

## ③ พบปัญหาจริงระหว่างต่อสาย: ค่าที่เจ้าของสั่ง (0,0,0) ชน ground-bound sanity check ที่มีอยู่แล้ว

`world_scene_travel._spawn()` (เขียนไว้ตั้งแต่ก่อนรอบนี้) เช็คทุก spawn ที่ pin ไว้ว่าต้องอยู่ในขอบเขต `ground`
ของฉากนั้น (x/y/z ต้องอยู่ใน min/max ที่วัดจาก placements.tsv) ถ้าไม่อยู่ → `ValueError` ตอน `load_scene_registry()`
ฉาก 17 มี `ground` block อยู่แล้ว (เติมโดยรอบ `kqrlhr`) ด้วย **z_min=746.04, z_max=1272.74** (วัดจาก
`Bg1001.placements.tsv` จริง - เรือมีหลายชั้นดาดฟ้า) — เขียน `spawn.z = 0.0` ตรงๆ ตามคำสั่งเจ้าของจะทำให้
**ทั้งไฟล์ registry โหลดไม่ขึ้นเลย** (ทุกฉาก รวมฉาก 1/บ้าน) เพราะ `load_scene_registry()` parse ทุก destination
รวดเดียวแล้ว raise ทันทีที่เจอตัวแรกที่ผิด - นี่คือ landmine จริง ไม่ใช่การเดา

**ทางที่เลือก**: เพิ่มฟิลด์เสริม (optional) `spawn.ground_bound_waiver` (ข้อความสั้น อ้างอิงได้ - ในที่นี้คือ
`"PROVISIONAL-OWNER-DECREE-20260827-1445"`) — เมื่อมีฟิลด์นี้ `_spawn()` จะข้าม ground-bound cross-check เฉพาะ
แถวนั้นแถวเดียว ทุกฉากอื่นที่ไม่มีฟิลด์นี้ (ฉาก 1, ฉาก 2, ฉาก 278, ฉาก 997) ยังถูกเช็คเหมือนเดิมทุกประการ -
ไม่ได้ผ่อนกฎทั่วไป มีเทสยืนยันทั้งด้านบวก (waiver ทำให้ค่านอกขอบเขตผ่านได้จริง) และด้านลบ (ไม่มี waiver ยังโดน
refuse เหมือนเดิม, waiver ว่างเปล่าโดน refuse เหมือน provenance ว่างเปล่า, ฟิลด์แปลกปลอมอื่นโดน refuse)
เหตุผลที่เลือกทางนี้แทนการนิ่งเฉย/เขียนจดหมายถาม: cross-check นี้ถูกออกแบบมาจับ "ค่าที่ไม่ได้วัด" ซึ่งเป็นจริง
กับค่านี้โดยตรงตามคำเจ้าของเอง (ไม่ใช่พิกัดที่วัด) - เจ้าของสละสิทธิ์กฎ "ห้ามปั้นพิกัด" ไปแล้วครั้งเดียวเฉพาะค่านี้
ตามจดหมาย 1445 เอง การปฏิเสธค่านี้ด้วย heuristic ที่ออกแบบมาจับปัญหาคนละอย่างจะเป็นการเถียงคำสั่งเจ้าของโดยไม่ได้
ตั้งใจ

## ④ ของที่ต่อสายจริงรอบนี้

- **`scenarios/world_scene_registry_001.json`**: ฉาก 17 (`n_id=17`) `spawn` เปลี่ยนจาก `null` เป็น
  `{x:0, y:0, z:0, provenance:"PROVISIONAL-OWNER-DECREE-20260827-1445: ...", ground_bound_waiver:
  "PROVISIONAL-OWNER-DECREE-20260827-1445"}` พร้อม nonclaim ตามจดหมาย 1445 ข้อ 4 (คำต่อคำ: "ยังไม่พิสูจน์ว่า
  ไคลเอนต์วางผู้เล่นบนผิวน้ำ/ในขอบแมพ") และวันหมดอายุ (RE-103's T3) เขียนไว้ในฟิลด์ `provenance` ตรงๆ - แก้
  `table_row_differences.spawn_is_null_because`/`ground_is_null_because` ให้ strike-through ของเก่า + เติม
  UPDATE ใหม่ (ธรรมเนียมเดิมของไฟล์นี้ ไม่ลบประวัติ)
- **`src/pirateforce_foundation/world_scene_travel.py`**: เพิ่มฟิลด์เสริม `ground_bound_waiver` ใน schema ของ
  `spawn` (`_SPAWN_OPTIONAL_FIELDS`), ขยาย `_spawn()` ให้ข้าม ground cross-check เฉพาะเมื่อมี waiver, เพิ่ม
  `SceneDestination.spawn_ground_bound_waiver: str | None = None` (default ทำให้โค้ด/เทสเดิมที่สร้าง
  `SceneDestination(...)` ตรงๆ ไม่พัง)
- **`src/pirateforce_foundation/columbus_quest_dispatch.py`**: อัปเดต docstring ทั้งโมดูล (สอง gap → หนึ่ง gap
  ที่เหลือจริง), `resolve_columbus_arrival()` ไม่ raise `SceneEntryRefused` สำหรับฉาก 17 อีกต่อไป + พิมพ์ token
  คอนโซล `SCENE_ENTRY scene=17 xyz=0,0,0 source=PROVISIONAL-OWNER-DECREE-20260827-1445` ตามที่จดหมาย 1445
  ข้อ 2 สั่งไว้ (อ่านค่า waiver กลับจาก registry เอง ไม่ hardcode เทียบ) - `dispatch_columbus_quest3021()`
  **ยัง refuse เหมือนเดิมทุกครั้ง** (never-partially-applies ตามเดิม) แต่ตอนนี้ `reasons` มีแค่ 1 ตัว
  (`no_re096_vehicle_row_evidence`) ไม่ใช่ 2 ตัว - เพิ่มค่าคงที่ `SCENE17_PROVISIONAL_SPAWN_SOURCE` สำหรับให้
  เทส/โค้ดอื่นอ้างอิงโดยไม่ต้อง hardcode ซ้ำ
- **เทส**: `tests/test_world_scene_travel.py` (+4 เทสใหม่: waiver ผ่าน/ไม่ผ่าน, waiver ว่างโดน refuse, ฟิลด์
  แปลกปลอมโดน refuse, ฉากอื่นไม่มี waiver ติดมาด้วย + แก้ 1 เทสเดิมที่เคย assert `spawn is None` ของฉาก 17)
  `tests/test_columbus_quest_dispatch.py` (แก้ 2 เทสเดิม + เพิ่ม 2 เทสใหม่: resolve สำเร็จ, token คอนโซลถูกพิมพ์
  จริง, ฉากที่ไม่มี waiver ไม่พิมพ์ token) `tests/test_columbus_quest_dispatch_wiring.py` (แก้ 1 เทส end-to-end
  ผ่าน `runtime.make_state_class` จริง - ยืนยันว่า `refusal_events` เหลือ 1 ตัว ไม่ใช่ 2, ยืนยันว่า token คอนโซล
  ไหลผ่าน `state.events` จริงโดยไม่แตะ `runtime.py` เลย เพราะ `runtime.py:4300-4303` เขียนเป็น loop ทั่วไปอยู่
  แล้ว [`for reason in error.reasons`], ผ่าน `emit=self.events.append` ที่มีอยู่แล้ว)

## ⑤ ตัวเลขที่วัดได้

- ไฟล์ที่แตะใน `pirate-force-server`: **6** (`scenarios/world_scene_registry_001.json`,
  `src/pirateforce_foundation/world_scene_travel.py`,
  `src/pirateforce_foundation/columbus_quest_dispatch.py`, `tests/test_world_scene_travel.py`,
  `tests/test_columbus_quest_dispatch.py`, `tests/test_columbus_quest_dispatch_wiring.py`)
- เทสที่รันยืนยัน (กลุ่มเป้าหมาย): `tests.test_world_scene_travel` + `tests.test_world_scene_entry` +
  `tests.test_world_travel_gate` + `tests.test_world_travel_gate_wiring` + `tests.test_columbus_quest_dispatch`
  + `tests.test_columbus_quest_dispatch_wiring` + `tests.test_world_columbus_m2_crosswalk` +
  `tests.test_world_census_wiring` + `tests.test_world_population(_handoff)` +
  `tests.test_world_scene_liveness(_wiring)` + `tests.test_world_density` + `tests.test_world_lane_static`
  = **429/429 ผ่าน**
- เทสทั้งเรโป: `python3 -m unittest discover -s tests` = **3543 เทส, error 18 ตัว (มีอยู่ก่อนแล้ว, ทั้งหมดคือ
  `ModuleNotFoundError: No module named 'capstone'` - ไม่เกี่ยวกับไฟล์รอบนี้เลยสักไฟล์, ยืนยันด้วยชื่อไฟล์ error
  ทั้ง 18 ตัวตรงกับ static-RE test ที่ import `capstone`), 0 FAIL**
- cp874-encodability: ตรวจทุกไฟล์ที่แตะใน `src/`/`tests/`/`scenarios/` ผ่านหมด (`.decode('cp874')` ไม่ error)
- ยืนยันสด (headless, ไม่ใช่เทส) ว่า console/events ที่ `runtime.py` โยนออกมาจริงมีบรรทัดใหม่:
  `WORLD_SCENE scene_id=17 ...` และ `SCENE_ENTRY scene=17 xyz=0,0,0 source=PROVISIONAL-OWNER-DECREE-20260827-1445`
  และ `columbus_quest3021_dispatch_refused_no_re096_vehicle_row_evidence` (1 ตัว ไม่ใช่ 2)

## ⑥ ยังไม่ได้พิสูจน์ / รอมนุษย์

- **ไม่มีอะไรเปลี่ยนบนจอเกม** - Columbus ยัง refuse ทุกครั้ง (ดู ①) จนกว่าเจ้าของจะเคาะคำถามที่ค้างอยู่จริง
  (จดหมาย `20260827_1510_PANYA-DECISION-M2-skip-*` ข้อ 4: "M2 รับเข้าฉาก 17 แบบยังไม่เป็นเรือได้ไหม" - กำลังถาม
  สดในแชทตอนที่จดหมายนั้นถูกเขียน) **สาย A ไม่แตะคำถามนี้เลย ไม่เปิดใบซ้ำ** - `dispatch_columbus_quest3021`
  ยัง atomic เหมือนเดิมทุกประการ (never-partially-applies) ไม่ได้ตัดสินใจแทนเจ้าของว่าจะแยกสอง half ออกจากกันไหม
- `RE-096` (vehicle-bind payload) ยังเป็นเพดาน static ถึงที่สุดจริง - ทางเดียวที่จะปิดคือ attended capture ของ
  เฟรม `CVehicleVital` ที่ handler ไม่ใช่ stub ว่างเปล่า ซึ่งยังไม่มีใครจับได้
- พิกัด (0,0,0) เป็นค่าชั่วคราวจากเจ้าของ **ไม่ได้พิสูจน์ว่าไคลเอนต์จะวางผู้เล่นบนผิวน้ำ/ในขอบแมพ** - ถ้าวันหน้า
  ทั้งสองช่องว่างถูกปิดแล้วมีการทดสอบจริง แล้วผู้เล่นตกขอบ/ค้าง ให้รายงานเป็นผล ไม่ใช่ FAIL ของกฎนี้ (ตามจดหมาย
  1445 ข้อ 4 คำต่อคำ)
- `RE-103` หัวใบใน `CLIENT_RE_QUEUE.md` ยังไม่ถูกปิด (ของ chief cloud รอบ `4txjyg`) - สาย A ไม่แตะซ้ำ (ธงเดิม
  ที่ตั้งไว้ตั้งแต่รอบ `kqrlhr` ยังยืนอยู่)

## ⑦ pf-adversary pass (ก่อนปิดรอบ)

ตรวจงานตัวเองก่อนส่ง พบและแก้เอง 2 ข้อ:

1. **[HIGH, แก้แล้ว]** ร่างแรกไม่ได้เช็คว่า `SceneDestination(...)` ที่สร้างตรงๆ ในเทสเดิม (ไม่ผ่าน
   `load_scene_registry`) จะพังไหมเมื่อเพิ่มฟิลด์ใหม่ในดาต้าคลาส - grep แล้วพบ 2 จุด
   (`tests/test_world_scene_travel.py`, `tests/test_world_travel_gate.py`) ทั้งคู่ปลอดภัยเพราะฟิลด์ใหม่มี
   default `= None` และตำแหน่งอยู่ท้ายสุด (กฎ dataclass: ฟิลด์มี default ต้องอยู่หลังฟิลด์ไม่มี default) - รัน
   เทสทั้งสองไฟล์ยืนยันผ่านจริง ไม่ใช่แค่อ่านโค้ดแล้วเดา
2. **[MEDIUM, แก้แล้ว]** ร่างแรกของเทส `test_a_scene_with_no_waiver_prints_no_decree_token` ทดสอบผิดกิ่ง (รัน
   กับ registry จริงที่ฉาก 17 *มี* waiver อยู่แล้ว - ไม่มีทางเห็นกิ่งลบ) เขียนใหม่โดย mock
   `world_scene_entry.resolve_entry` ให้คืน `SceneEntry` ที่ destination ไม่มี waiver จริง ๆ แล้วยืนยันว่าไม่มี
   token ถูกพิมพ์ - ตอนนี้ทดสอบกิ่งลบได้จริง (เทสนี้ก่อนแก้ก็ "ผ่าน" อยู่ดี เป็นตัวอย่าง false-positive ที่ต้อง
   จับเอง)
3. **[ตรวจแล้วไม่พบปัญหา]** ตรวจว่าฉากอื่นทั้งหมด (1, 2, 278, 997) ไม่มี `ground_bound_waiver` ติดมาด้วยความ
   ผิดพลาด (เทส `test_every_other_pinned_spawn_still_has_no_waiver` ใหม่ยืนยัน) และเทส
   `test_a_scene_17_style_spawn_outside_ground_is_only_refused_without_a_waiver` ยืนยันว่ากลไก ground-bound
   check เดิมยังทำงานเหมือนเดิม 100% สำหรับทุกแถวที่ไม่มี waiver

## ⑧ CORE-REQUEST

none - ไม่มีอะไรต้องขอ chief แก้ `runtime.py`/`app.py` รอบนี้ (ยืนยันด้วยการรันเทส wiring end-to-end ผ่าน
`runtime.make_state_class` จริงแล้ว behaviour เปลี่ยนถูกต้องโดยไม่แตะไฟล์นั้นเลย - `runtime.py:4294-4303` เขียน
เป็น loop ทั่วไปตาม `error.reasons` อยู่แล้วตั้งแต่ก่อนรอบนี้)

## ⑨ เปิดใบให้สาย C

none

## ⑩ nonclaims

- **ไม่ได้อ้างว่า M2 ปลดล็อกแล้ว** - `dispatch_columbus_quest3021` ยัง refuse ทุกครั้งเหมือนเดิม (คนละเหตุผล
  เดียวตอนนี้ ไม่ใช่สองเหตุผล) จนกว่า `RE-096`/attended capture จะปิดช่องว่างที่เหลือ
- **ไม่ได้ตัดสินคำถาม "M2 รับเข้าฉาก 17 แบบยังไม่เป็นเรือได้ไหม"** - คำถามนี้อยู่ในมือเจ้าของแล้วตามจดหมาย 1510
  ข้อ 4 สาย A ไม่แตะ ไม่เปิดใบซ้ำ ไม่ทำให้ dispatch หยุด atomic
- **ไม่ได้ปิดหัวใบ `RE-103`** - ยังเป็นของ chief cloud (รอบ `4txjyg`) เหมือนเดิม
- **ไม่ได้อ้างว่าพิกัด (0,0,0) ปลอดภัย** - เป็นค่าชั่วคราวจากเจ้าของ ยังไม่มีใครวัด/สังเกตจากไคลเอนต์จริงว่า
  ผู้เล่นจะยืนอยู่ตรงไหน (nonclaim จากจดหมาย 1445 ข้อ 4)
- **ไม่ได้เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**
- **ไม่ได้แตะ** `runtime.py` · `app.py` · `current/pf_login_game_server_v141.py`

— สาย A · WORLD
