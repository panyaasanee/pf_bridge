# A_20260827_1052 - Columbus M2 identity correction: quest 3021/scene 17, not 3023/19

เวลา: 2026-08-27 ~10:35-10:52 +07:00 = ~03:35-03:52 UTC
สาย: A (WORLD)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ยังไม่มีอะไรเปลี่ยนบนหน้าจอผู้เล่นรอบนี้ - นี่เป็นรอบแก้ข้อมูล (crosswalk) ที่ป้อนแผนต่อสายให้ chief
เขียน CORE-REQUEST ในรอบถัดไป ไม่ใช่รอบที่แตะ runtime.py เอง

## สรุปหนึ่งย่อหน้า

จดหมาย `20260827_1830_CHIEF-REPLY-PANYA-CHASE-...` (ข้อ ①) เขียนว่า Columbus quest id = 3023 และ
placement index 1 ราวกับเป็นข้อเท็จจริงเดียวกัน - ผิด สอง fact นี้เป็นคนละ NPC: MOBS n_ID 156 (Columbus
ของ Port Royal จริง, ยืนที่ bg0001 census index 1, ยืนยันสองรอบโดยเจ้าของใน `20260827_0925_PANYA-DECISION`
และ `20260827_0950_PANYA-DECISION`) มี `s_QUEST_BEGIN` มีเลข **3021** ไม่ใช่ 3023 - เลข 3023 เป็นเควสต์จริง
แต่เป็นของ MOBS n_ID 36 (Columbus คนละตัว ของ Spice Paradise, level 35) เควสต์ 3021 เป็น `Q_TELEPORT1`,
`n_VARI_2=17` -> ปลายทางฉาก 17 (`Bg1001`, `n_SCENE_TYPE=4`, ฉากทะเล) ตรงกับแผน M2 (คุย Columbus -> เทเลพอร์ต
ไปแมพทะเล -> กลายเป็นเรือ) ส่วนเควสต์ 3023 เอง `n_VARI_2=19` - ปลายทางของ Spice-Paradise-Columbus ไม่ใช่ของ
Port Royal ทุก fact ตรวจซ้ำเองจากตาราง sha256-pinned จริง (ไม่ใช่แค่ก็อปจากใบสั่งงาน) แล้วตรงกับที่สั่งมา 100%

## สิ่งที่ตรวจ/re-derive เอง (ไม่ใช่แค่เชื่อใบสั่งงาน)

1. `pf_bridge/gamedata/tables/CONSTDATA_TH__MOBS.tsv` sha256
   `3c0d33d68f832eefda56c845495008338dcef56f4277584b9ca479b7e1b3916b` - ตรงกับที่ให้มา ✓ - แถว
   `n_ID=156`: `s_ROLE_GRAPHIC=COLUMBUS_0`, `s_QUEST_BEGIN=111;998;3021;3205;7062;7063` (**มี 3021 ไม่มี
   3023**) - แถว `n_ID=36`: level 35, `s_QUEST_BEGIN=121;3023;3207` (**มี 3023**)
2. `pf_bridge/gamedata/tables/QUESTDATA_TH__QUEST.tsv` sha256
   `cc9927286def2bda166c320a2dddd16f5457eb4579ce5207a3d76758707527bd` - ตรง ✓ - แถว `n_ID=3021`:
   `n_TYPE=20`, `s_LUASCRIPT=Q_TELEPORT1`, `n_VARI_2=17` - แถว `n_ID=3023`: `n_VARI_2=19`
3. `pf_bridge/gamedata/tables/CONSTDATA_TH__SCENE_NAME.tsv` sha256
   `e38114a802576266ce37b2abcf8ebce3f105d7d5abaf4bc5ca066e7848c5d60b` - ตรง ✓ - แถว `n_ID=17`:
   `s_MODLE_ID=Bg1001`, `n_SCENE_TYPE=4`, `n_SCENE_WEATHER=5`, `n_SCENE_DAYANDNIGHT=2`,
   `n_CLINE_TYPE=4294967295`, `n_CANGLIDE=0`, `n_CANRIDE=0`, `n_LIMIT_HEIGHT=0`, `n_SAVE=0`,
   `n_MARKER=0`, `n_CAMERA_TYPE=1`, `n_COLLECT_MAP=0`, `n_SCENE_LV=0`
4. `pf_bridge/gamedata/scene/Bg1001/Bg1001.placements.tsv` sha256
   `5e4de48707a87061d9a95471a1c3c25c56f0469fe2ece7ef0709a9c79f40fec7` - ตรง ✓ - 8 แถว ทุกแถวเป็น
   `Mob_set_*` (index 0-7) **ไม่มีจุด player-arrival spawn เลย** - ติดป้าย unknown ไม่ปั้นพิกัด
   `pf_bridge/gamedata/PF_GAMEDATA_SCENE_INDEX.tsv` sha256
   `c4016cf685671d4c7bbb1909bb300146afd802dd6b53f2d5e7b928249f26652d` - ตรง ✓ - แถว `Bg1001`:
   `definition_count=6`, `src_sha256=da5c560af6c483490a041f0605a1b0cfe047a7ee00e515de07567d0c1247e821`
5. `current/pf_login_game_server_v141.py:1323-1456` (frozen, อ่านอย่างเดียว ไม่แก้) -
   `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` index 1: `x=-8013.458984375, y=-2780.045166015625,
   z=223.29209899902344` ตรงกับที่สั่งมา - raw census field ที่ index นี้เขียน template_id=2,
   display_name="Sebastian" (**ไม่ใช่หลักฐานตัวตน** ตามกฎโครงการที่ยืนยันซ้ำในจดหมาย 0950: identity มาจาก
   คำตัดสินของเจ้าของ + พิกัด ไม่มาจาก ordinal/template/display_name ดิบ)
6. คำนวณ nearest-other-census-member จาก index 1 เอง (Python, 115 แถวเต็มจากไฟล์แข็ง): index 65
   ("Columbus" ในป้ายดิบ) อยู่ห่าง 1074.59 units - ตรงกับเลข 1074.6 ที่ไฟล์เก่าเคยปักไว้ (สมมาตร, sanity
   check ผ่าน) - ยืนยันว่า index 65 = Loie (MOBS 802) ตาม `20260827_0950_PANYA-DECISION`, ไม่ใช่ Columbus

## ของที่สร้าง

1. `pirate-force-server/scenarios/world_travel_gates_001.json` - แก้ gate
   `port_royal_columbus_departure`: **ไม่เปลี่ยนตัวเลข** operative ของ `centre`/`to_scene_id` (275 lines
   ของ `tests/test_world_travel_gate.py` ปักตัวเลข index-65 กับ `gate.centre` ไว้แน่นแล้ว - ไฟล์นั้นอยู่
   นอกโซนเขียนของรอบนี้) - เพิ่ม/แก้ข้อความ provenance + คีย์ optional ใหม่
   `why_an_authored_placement_and_not_a_bare_coordinate` (คีย์นี้มีอยู่แล้วใน schema `_CENTRE_FIELDS`
   ของ `world_travel_gate.py`) บันทึกการแก้ไข identity เต็ม พร้อม strike-through (`~~...~~`) ของข้อความ
   เก่าที่ผิด ตาม convention เดิมของไฟล์ (`COO_RULING_..._SUPERSEDES_THE_PARAGRAPH_ABOVE`) - ระบุชัดว่า
   walk-in gate นี้ (ของ BUILD-002, ไปฉาก 278) เป็นกลไก debug-only คนละเรื่องกับเส้นทาง M2 จริง
   (NPC conversation -> quest 3021 -> scene 17) ตามที่ COO_RULING ในไฟล์เดียวกันเคยตัดสินไว้แล้ว
2. `pirate-force-server/scenarios/world_scene_registry_001.json` - เพิ่ม destination ใหม่ `n_id: 17`
   (`Bg1001`) ตาม pattern เดียวกับ scene 1/2/278/997 ที่มีอยู่แล้ว: `table_row` เต็มจากตารางจริง,
   `native_placement_count=8`, `native_definition_count=6`, `native_sha256` จาก
   `PF_GAMEDATA_SCENE_INDEX.tsv`, `spawn: null` (ติดป้าย unknown ใน `table_row_differences`,
   ไม่ปั้นพิกัด), `ground: null` (มีตัวเลขจริงที่คำนวณแล้วบันทึกไว้ใน text แต่ตั้งใจไม่ประกอบเป็น
   `ground` block เต็มรอบนี้ เพื่อไม่ต้องรีบตีความ undecoded fields - เป็นทางเลือกขอบเขต ไม่ใช่ refusal)
   - `table_row_differences` มี crosswalk เต็ม + citation sha256 ครบ + strike-through ของ claim 3023 เดิม
3. `pirate-force-server/tests/test_world_columbus_m2_crosswalk.py` (ใหม่) - pin 7 เทส: MOBS 156 มี 3021,
   MOBS 156 ไม่ต้องมี 3023 (และ MOBS 36 มี 3023 จริง - regression guard กันย้อนกลับไปผิดจุดเดิม), เควสต์
   3021 -> scene 17, เควสต์ 3023 -> scene 19 (ไม่ใช่ 17), scene 17 = Bg1001/type 4, Bg1001 placements
   ไม่มี player spawn (8 แถว, ทุกแถว `Mob_set_*`), และ sha256 provenance ของทั้ง 4 ตาราง ใช้ pattern
   `pf_preconditions.BRIDGE_GAMEDATA` + `ROOT.parent/pf_bridge/gamedata` เดียวกับ
   `test_pf_scan_field_scene_candidates.py`/`pf_mine_scene_mob_roster.py` (ไม่ hardcode path เฉพาะ
   session นี้) - รัน `pytest tests/test_world_columbus_m2_crosswalk.py -v` = **7 passed**

## เทสที่รันแล้ว (นอกเหนือจากไฟล์ใหม่)

- `pytest tests/test_world_travel_gate.py` = 83 passed (ก่อนแก้ครั้งแรกเคยพัง 76/83 เพราะเผลอเปลี่ยน
  `centre` x/y/z จริง - ย้อนกลับตัวเลขแล้วใส่แก้เฉพาะ text ตามที่เขียนไว้ข้างบน, รันซ้ำแล้วเขียวหมด)
- `pytest tests/test_world_scene_liveness.py tests/test_world_scene_liveness_wiring.py
  tests/test_world_travel_gate_wiring.py` = 97 passed
- `pytest tests/` (ทั้งชุด, ข้าม 22 ไฟล์ที่ collection error เพราะขาด `capstone`/`tools` module ใน
  sandbox นี้ - ไม่เกี่ยวกับรอบนี้) = **3190 passed, 194 skipped, 2 failed**

## regression ที่พบ นอกโซนเขียนของรอบนี้ (รายงานตามกฎ ไม่แก้เอง)

`tests/test_world_scene_travel.py` มี 2 เทสพังเพราะ destination ตัวที่ 5 (`n_id=17`) ที่เพิ่มเข้าไป:
- `SceneRegistryTests::test_the_registry_pins_exactly_the_scenes_that_have_evidence` (บรรทัด ~75)
  ปัก tuple `(1, 2, TEST_STAGE_SCENE_ID, 997)` ตรง ๆ - docstring ของเทสเองเขียนไว้ว่า "A fifth id
  appearing here without a decision behind it is what this test is for" ⇒ ตั้งใจให้ปรับเมื่อมี
  "decision" มารองรับ ซึ่งรอบนี้มี (crosswalk ที่ verify สองรอบจากตาราง sha256-pinned) แนะนำ 1 บรรทัด:
  เปลี่ยนเป็น `(1, 2, 17, TEST_STAGE_SCENE_ID, 997)`
- `SceneRegistryRefusalTests::test_a_half_written_ground_block_is_refused_by_contract` (บรรทัด ~245)
  ใช้ `data["destinations"][2]["ground"]` โดยสมมติว่า index 2 = ฉาก 278 (มี ground จริง) - ตอนนี้ index 2
  = ฉาก 17 (`ground: null`) ⇒ `TypeError` แทน `ValueError` แนะนำ: index ด้วย `n_id==278` แทน positional
  index 2, หรือเปลี่ยนเป็น index 3
ไม่แก้ไฟล์นี้เอง เพราะอยู่นอกโซนเขียนที่ได้รับมอบหมายรอบนี้ (`tests/` เฉพาะไฟล์ใหม่ของโมดูลตัวเอง) -
รายงานไว้ให้ chief/คนต่อรอบตัดสินใจว่าจะขยับ pin นี้หรือไม่

**อัปเดตหลัง pf-adversary pass (ผู้ประสาน รอบเดียวกัน):** แก้ทั้งสองเทสแล้วด้วยบรรทัดที่แนะนำไว้ข้างบน
(assertion tuple 5 ตัว + docstring อัปเดต, และเปลี่ยน `data["destinations"][2]` เป็น n_id-lookup แทน
positional index ในสี่จุดของ `SceneRegistryRefusalTests` เพื่อไม่ให้พังซ้ำถ้ามี destination ตัวที่ 6 ในอนาคต)
รันซ้ำ: `3299 passed, 208 skipped, 17 errors (capstone/tools ขาดใน sandbox, ไม่เกี่ยวรอบนี้), 0 failed`
pf-adversary ยังเจออีก 2 ข้อ (unpinned skip ในไฟล์เทสใหม่ของรอบนี้เอง + ข้อความ "ยืนยันสองรอบ"/"Spice
Paradise's Columbus" ที่ overclaim) ดูรายละเอียดและการแก้ทั้งหมดในจดหมายคู่กัน หัวข้อ "pf-adversary pass"

## nonclaims

- ไม่ได้อ้างว่าเควสต์ 3021 ผ่านการยืนยันระดับ wire แล้ว - ยังเป็น [STATIC] เท่านั้น (เปิดใบให้สาย C
  ด้านล่าง)
- ไม่ได้อ้างว่า scene 17 เคยถูกส่งให้ client จริงสักครั้ง
- ไม่ได้อ้างว่ารู้จุด player-arrival spawn ของ scene 17 - ไม่รู้ และไม่ปั้น
- ไม่ได้แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` เลยในรอบนี้
- ไม่ได้ทำ BUILD-002 (scene_id=278 default) ตามคำสั่งอัตโนมัติของรอบ - งานนั้นถูกบล็อกไว้แล้วโดย
  `20260826_2147_COO-DECISION-BUILD-002-scene278-stays-blocked.md` และ
  `20260827_0245_COO-DECISION-BUILD-002-scene278-stays-off-1600-1645-affirmed.md` รอบนี้ทำงาน M2 จริงที่
  เจ้าของอนุมัติแล้วแทน (Columbus -> quest 3021 -> scene 17)

## CORE-REQUEST / เปิดใบให้สาย C

ดูจดหมายคู่กัน `notes_to_chief/20260827_1052_LANE-A-CORRECTION-columbus-m2-quest3021-not-3023-scene17-not-19.md`

## PR

`pirate-force-server` - branch ปัจจุบัน, ไฟล์ที่แก้/เพิ่ม: `scenarios/world_travel_gates_001.json`,
`scenarios/world_scene_registry_001.json`, `tests/test_world_columbus_m2_crosswalk.py` (ใหม่)
`pf_bridge` - branch ปัจจุบัน, ไฟล์นี้ + จดหมายถึง chief คู่กัน

— **สาย A · WORLD**
