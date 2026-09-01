# LANE-A round `trig7s`

2026-09-01T02:2x+07:00 - 2026-09-01T02:4x+07:00 (+07:00 via `TZ=Asia/Bangkok date`).

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็นอะไรต่างบนจอ - แต่ทุกครั้งที่มีคนขึ้นเรือ Columbus ที่ Port
Royal คอนโซลตอนนี้บอกตรง ๆ ด้วยว่า **อีกเจ็ดเกาะที่เหลือ (Prison Exile, Spice Paradise, Slave Market,
Evil Port, Ocean Walled City, Voodoo, Silver Harbour) มี Columbus ของตัวเองยืนอยู่จริงกี่เกาะ** (6 จาก 7
ยืนยันแล้วว่าอยู่จริงในสำมะโนของฉากนั้น ๆ, 1 เกาะ - Prison Exile - เจอเลข MOBS ไม่ตรงกับที่ตารางเส้นทาง
อ้างไว้ และรายงานเป็น "ไม่พบ" อย่างตรงไปตรงมาแทนที่จะเดาว่าใช่) โดยยังไม่มีการต่อ dispatch จริงให้เจ็ดเกาะ
นี้ (ต้องแก้ `runtime.py` ซึ่งเป็นไฟล์ของ chief เท่านั้น - ดู CORE-REQUEST ท้ายรอบ)

## 0. บริบทก่อนเริ่ม

เช็ค `pf_bridge/CLIENT_RE_QUEUE.md` และ `pf_bridge/GAME_TEST_QUEUE.md` หาใบที่ LANE-A เปิดค้างและยังตอบได้
เอง (ไม่ต้องรอ RE/attended): พบ `RE-170` (BG0005 median investigation, ต้อง git-blame) และ `RE-171`
(BG0006 CJK teleporter name, ต้องค้นตารางสำรอง) — ทั้งสองเป็น static/ค้นตารางล้วน ไม่มี concrete-and-
actionable ticket อื่นที่ตรงกว่า M2 fallback rule รอบนี้ตัดสินใจทำ `RE-171` (เร็ว ตรงไปตรงมา ไม่มี
ambiguity) ในรอบนี้ด้วย และเก็บ `RE-170` ไว้ก่อน (ต้อง git blame ซึ่งใช้เวลามากกว่า ไม่ใช่ M2 อยู่แล้ว)
ตามกฎ fallback ("ระหว่างรอ RE ของ Columbus ให้ทำ M2 ขั้นถัดไป") จึงเลือกงานหลักของรอบนี้จาก M2 backlog

## 1. การสำรวจ M2 backlog ก่อนเลือกงาน

อ่าน `world_m2_sea_destination.py`, `world_m2_crossing_handoff.py`, `world_m2_return_leg.py`,
`columbus_quest_dispatch.py`, `world_travel_gate.py`, `world_scene_travel.py` ทั้งหมดก่อนเลือกงาน พบว่า:

- ขาไปของฉาก 17 (Port Royal -> เรือ) ครบวงจรเต็มแล้ว: dispatch -> arrival -> stowaways ->
  return-leg position -> return-population -> crossing-handoff (ส่งไบต์จริง, GT-148 PASS แล้ว) ->
  sea-destination (ประตูเดียว) -> sea-map (ทั้งแปดเกาะ, arrival-side readiness)
- ขากลับ (return leg) ยังเป็น report-only ทั้งหมด เพราะไม่มี in-game trigger ให้กลับ (`RE-077` ครึ่งขากลับ
  ยังเปิด, ฉาก 17 ไม่มี NPC เลยตามที่ GT-148 ยืนยัน) - ไม่มีอะไรให้สร้างตรงนี้โดยไม่เดา/ไม่ยัด NPC เข้าไป
- `world_m2_sea_destination`'s เองบอกไว้ตรง ๆ ว่าฝั่ง **arrival** (ประตูมีที่ให้ลงจอดไหม) ถูกวัดครบแปดเกาะ
  แล้ว (`sea_map_lines`) แต่ฝั่ง **trigger** (Columbus ของแต่ละเกาะยืนอยู่จริงไหม) "unmeasured by this
  module" - ประโยคนี้เองในดอกสตริงคือช่องที่ยังไม่มีใครถาม
- เลือกทำช่องนี้เพราะ: (ก) วัดได้จริงจากตารางที่มีอยู่แล้วทั้งหมด (ทุกฉาก 1-8 มีโมดูล population/identity
  ของตัวเองอยู่แล้วจากการเปิดสิบประตู) (ข) ไม่ต้องพึ่ง player identity (ทุกอย่างเป็นข้อมูลระดับฉาก ไม่ใช่
  ระดับตัวละคร) (ค) ต่อกับ call site เดิมที่ `dispatch_columbus_quest3021` เรียกอยู่ทุกบูตอยู่แล้ว ไม่ต้อง
  ขอ CORE-REQUEST wiring ใหม่ (ง) reuse ตารางที่มีอยู่แล้วทั้งหมด ไม่เขียน selector ที่สอง

## 2. งานที่สร้าง

### 2.1 `world_m2_columbus_trigger_readiness.py` (ไฟล์ใหม่, src/)

ตรวจว่า MOBS n_ID ของ Columbus แต่ละเกาะ (จาก `world_m2_sea_destination.COLUMBUS_ROUTES`) ปรากฏจริงใน
สำมะโน/ตารางระบุตัวตนของฉากบ้านของเกาะนั้นหรือไม่ (`PLACED`/`NOT_PLACED`/`UNMEASURED`) โดย:

- ฉาก 1 (Port Royal): reuse `columbus_quest_dispatch.columbus_actor_identity` ตรง ๆ (เช็คเดียวกับที่
  dispatch จริงที่ใช้งานอยู่แล้ววันนี้ใช้ - ไม่สร้างเช็คคู่ขนานที่สอง)
- ฉาก 2-8: reuse `shippable_placements()`/`load_known_placements()` ของแต่ละ `world_bg000X_identity.py`
  (หรือ `scene2_prison_exile_tables.py` สำหรับฉาก 2) ที่มีอยู่แล้วจาก BUILD-001 lineage

**ข้อผิดพลาดที่จับได้ก่อนส่งตัวเลขออกไป**: draft แรกของรอบนี้เทียบ `COLUMBUS_ROUTES`'s MOBS n_ID กับ
`placement.template_id` ตรง ๆ แล้วได้ผลลบทั้งเจ็ดเกาะ (0/7) - พอเปิดดูดอกสตริงของ `_RESOLVED_ROWS` ใน
`world_bg0004_identity.py` เอง (หัวตาราง "(Mob-Set number, CLINE row n_ID, MOBS.n_ID, ...)") พบว่า
`template_id` คือเลข Mob-Set ต่อฉาก ไม่ใช่ MOBS n_ID จริง - MOBS n_ID จริงอยู่ที่ `identity.mobs_n_id`
(ฟิลด์ที่สามของ `SceneIdentity`) แก้เป็นอ่านฟิลด์นั้นแทน ได้ผล 6/7 ถูกต้อง (ฉาก 2 ยังคง NOT_PLACED จริง
ด้วยเหตุผลอื่น - ดูข้อ 2.2)

**ตัวเลขที่วัดได้จริง** (verified ด้วย `legacy` จริงจาก `current/pf_login_game_server_v141.py`):

```
home 1 (Port Royal,       MOBS 156): PLACED
home 2 (Prison Exile,     MOBS 360): NOT_PLACED  <- ดูข้อ 2.2
home 3 (Spice Paradise,   MOBS  36): PLACED (62 shippable placements)
home 4 (Slave Market,     MOBS  67): PLACED (109 shippable placements)
home 5 (Evil Port,        MOBS 105): PLACED (87 shippable placements)
home 6 (Ocean Walled City,MOBS 196): PLACED (66 shippable placements)
home 7 (Voodoo,           MOBS 362): PLACED (56 shippable placements)
home 8 (Silver Harbour,   MOBS 250): PLACED (69 shippable placements)
```

`assembled 8 islands, 7 placed, 1 not_placed, 0 unmeasured` (with legacy passed) - ตัวเลขนี้พิมพ์ตรงบน
คอนโซลผ่าน `trigger_readiness_console_line()` ทุกครั้งที่มีคน dispatch quest 3021

### 2.2 การค้นพบที่ไม่ได้แก้เอง - เปิดใบให้สาย C แทน

ฉาก 2 (Prison Exile)'s `scene2_prison_exile_tables.py`'s เอง มี placement ชื่อ "Columbus" ที่ MOBS n_ID
**36** (ไม่ใช่ 360 ที่ `COLUMBUS_ROUTES` อ้างไว้สำหรับ home scene 2) - และ 36 คือเลขเดียวกับที่ home scene
3 (Spice Paradise) ใช้เป็น Columbus ของตัวเอง ตรวจ `CONSTDATA_TH__MOBS.tsv` แล้วพบว่าทั้ง n_ID 36 และ 360
มีแถวจริง ทั้งคู่ชื่อ "哥倫布" (Columbus) outfit `M055_000_000_N` เหมือนกันทุกประการ - ไม่ใช่เลขที่ใครเดาขึ้น
แต่สองฉากอ้างเลขเดียวกัน (36) เป็น Columbus ของตัวเองพร้อมกัน ซึ่งไม่น่าจะถูกทั้งคู่

**ไม่ได้แก้ไฟล์ไหนเพื่อ "ซ่อม" ความไม่ตรงนี้** - CHARTER-02 ห้ามเดาว่าตารางไหนผิดโดยไม่มี CLINE crosswalk
อ้างอิง เปิดใบ `RE-173` ให้สาย C (RE) หา crosswalk จริงของ placement นั้นแทน (ดูหัวข้อ "เปิดใบให้สาย C")
โมดูลใหม่รายงาน NOT_PLACED อย่างตรงไปตรงมา (fail-closed) แทนที่จะยอมรับ 36 เป็นตัวแทนของ 360 โดยไม่มี
หลักฐาน

### 2.3 `columbus_quest_dispatch.py` - หนึ่ง emit ใหม่ ต่อท้าย ไม่แตะ `runtime.py`

เพิ่ม `emit(world_m2_columbus_trigger_readiness.trigger_readiness_console_line(legacy=legacy))` เป็น
รายงานที่เจ็ด ต่อท้ายรายงาน `WORLD_M2_SEA_MAP` (รายงานที่หก) - call site เดิมของ
`dispatch_columbus_quest3021` ที่ `runtime.py` เรียกอยู่แล้วทุกบูตไม่มีแฟล็ก **ไม่ต้องแก้ไฟล์ chief เลย**
อัปเดตดอกสตริงของ `dispatch_columbus_quest3021` เพิ่มย่อหน้า "A SEVENTH REPORT" (รูปแบบเดียวกับหกย่อหน้า
ก่อนหน้า)

### 2.4 อัปเดตเทสที่ pin ตำแหน่งบรรทัดคอนโซล (ตามธรรมเนียมเดิมของไฟล์นี้)

`tests/test_columbus_quest_dispatch.py`'s `test_quest_3021_dispatch_is_unaffected_by_the_option_2_addition`
และ `tests/test_world_m2_crossing_handoff.py`'s สามเทสที่ pin ตำแหน่งด้วย `lines[-N]` - เลื่อนทุกดัชนีลง
หนึ่ง (บรรทัดใหม่กลายเป็น `lines[-1]`) พร้อมคอมเมนต์อธิบายรอบที่เพิ่ม ตามรูปแบบเดิมของไฟล์ ("THE
SEA-MAP ROUND APPENDED..." -> เพิ่ม "THE TRIGGER-READINESS ROUND APPENDED...")

### 2.5 เทสใหม่

`tests/test_world_m2_columbus_trigger_readiness.py` (ไฟล์ใหม่) - 13 เทส/7 subtests ครอบคลุม: การปฏิเสธ
อาร์กิวเมนต์ผิดชนิด/ฉากที่ไม่รู้จัก, ฉาก 1 กรณีมี/ไม่มี legacy, ทั้งเจ็ดเกาะเทียบกับ ground truth จริง
(รวมเคส NOT_PLACED ของฉาก 2 ที่ pin ไว้ตรง ๆ ว่า 36 อยู่แต่ 360 ไม่อยู่ - กันไม่ให้อนาคตแก้โมดูลจนดูเหมือน
"ไม่มี Columbus เลย" ปนกับ "มี แต่คนละเลข"), never-raises ของบรรทัดคอนโซล, cp874-encodability, และการต่อ
กับ dispatch จริงทั้งสองเคส (มี/ไม่มี legacy)

## 3. เทสที่รัน

```
python3 -m pytest tests/test_world_m2_columbus_trigger_readiness.py \
  tests/test_columbus_quest_dispatch.py tests/test_world_m2_crossing_handoff.py \
  tests/test_world_m2_return_leg.py tests/test_world_m2_sea_destination.py \
  tests/test_columbus_quest_dispatch_wiring.py -q
=> 161 passed, 11 subtests passed

python3 -m pytest tests/test_tree_is_cp874_safe.py -q
=> 5 passed, 455 subtests passed

python3 -m pytest tests/ -q  (ทั้งชุด)
=> 6089 passed, 327 skipped, 13115 subtests passed, 0 failed (227s)
```

## 4. งานเสริม - RE-171 ปิดใบ (ไม่มีการแก้โค้ด)

`RE-171` (BG0006 CJK teleporter name, ค้างจากรอบ `fx0007`) - ค้นทั้ง `pf_bridge/gamedata` (1109 ไฟล์)
หาตาราง `TEXTDATA_EN__MOBS_TIP.tsv` หรือคอลัมน์ชื่อสำรองใด ๆ - ไม่พบเลย (ไม่มีไฟล์ `_EN_`/`_ASCII_` ใด ๆ
ในต้นไม้นี้, ทุกตาราง `s_NAME` ขึ้นต้น `TEXTDATA_TH__`/`CONSTDATA_TH__` เท่านั้น) ปิดใบตาม pass criteria
ข้อ 3 ของใบเอง ("ถ้าไม่มี: ตอบว่าไม่มี แล้วปิดใบ") - 66/80 คือเพดานจริงของฉาก 6 ไม่มีการแก้
`world_bg0006_identity.py` เพราะ fail-closed ที่มีอยู่ถูกต้องแล้ว

## 5. งานที่ไม่ได้ทำรอบนี้ (ทำไม)

`RE-170` (BG0005 median investigation) - ต้อง git-blame ค้นรอบที่เขียน `SCENE_LEVEL_CONTROL['BG0005']`
เดิม ใช้เวลามากกว่าที่เหลือของรอบนี้ และไม่ใช่ M2/sea-travel อยู่แล้ว (เป็น Control 2 ของ scene-level
crosswalk, ไม่ถูก consume ที่ไหนในโค้ดที่รันจริง) - ปล่อยไว้เป็นใบเปิดเดิม ไม่ได้ปิดหรือแก้

## 6. ไฟล์ที่แตะ

**pirate-force-server** (7 ไฟล์):
- `src/pirateforce_foundation/world_m2_columbus_trigger_readiness.py` (ใหม่)
- `src/pirateforce_foundation/columbus_quest_dispatch.py` (แก้: import + emit ใหม่ + ดอกสตริง)
- `tests/test_world_m2_columbus_trigger_readiness.py` (ใหม่)
- `tests/test_columbus_quest_dispatch.py` (แก้: เลื่อน index ที่ pin)
- `tests/test_world_m2_crossing_handoff.py` (แก้: เลื่อน index ที่ pin, 3 จุด)
- `rounds/A_20260901_0242_trig7s_columbus-trigger-readiness.md` (สำเนา, optional)

**pf_bridge** (5 ไฟล์):
- `rounds/A_20260901_0242_trig7s_columbus-trigger-readiness.md` (ใหม่, ไฟล์นี้)
- `notes_to_chief/20260901_0146_COO-DECISION-door-reader-precedence-closed-gate-0941-landed-no-new-rule.md.CONSUMED.txt` (ใหม่)
- `CLIENT_RE_QUEUE.md` (แก้: ปิด RE-171, เปิด RE-173 ใหม่)
- `notes_to_chief/<timestamp>_LANE-A-STATUS-trig7s.md` (ใหม่ - จดหมายสถานะ)

## 7. CORE-REQUEST

ไม่มีของรอบนี้ที่ต้องแตะ `runtime.py`/`app.py` - โมดูลใหม่ต่อกับ call site เดิมที่ chief เดินสายไว้แล้ว
(`dispatch_columbus_quest3021`) หากอนาคตต้องการให้ผู้เล่นคลิก Columbus ของอีกเจ็ดเกาะได้จริง (ไม่ใช่แค่
รายงาน) นั่นคือ CORE-REQUEST ใหม่ (ต้องเพิ่ม `population_indices`/`ChooseNPC` gate อีกเจ็ดชุดใน
`runtime.py` แบบเดียวกับที่ฉาก 1 มีอยู่แล้ว) - ยังไม่ได้ขอรอบนี้ เพราะยังไม่มีเกาะไหนใน 7 เกาะนี้ที่ปลายทาง
(target scene 18-21,39-41) มี arrival spawn ที่เจ้าของ decree ไว้เหมือนฉาก 17 (`sea_map_lines` บอกไว้แล้ว
ว่าทั้งเจ็ดเป็น `READY_NOT_DECREED`/`REFUSED`) - ต่อ dispatch วันนี้จะสำเร็จที่ trigger แต่ล้มที่ arrival
ทุกครั้ง ไม่คุ้มกับความเสี่ยงของ CORE-REQUEST ที่ยังไม่มีปลายทางรองรับ
