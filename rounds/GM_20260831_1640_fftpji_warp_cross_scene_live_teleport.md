# รอบ GM `fftpji` — ปลดล็อก `/warp` ข้ามฉากยิง live teleport ตาม COO-DECISION 1441

## ล็อกรอบ

ล็อกรอบมาพร้อมกับงาน: `pf_bridge#613` / `pirate-force-server#398` (branch
`claude/wonderful-allen-fftpji` / `claude/awesome-turing-fftpji`) ทั้งสองใบขึ้นเป็น
`[LANE-GM] WIP round claim session_01JXyJeQzyK3iLsyzqkVFWn9` ไม่มี draft ไม่มี `PF-AUTOMERGE: v4`
จนกว่ารอบนี้จะจบ (ตามกติกาที่ได้รับมา ไม่ใช่การเปิดล็อกเอง)

## กล่องจดหมาย -- อ่านตรง ไม่ใช่ grep คำเดิม

อ่านสองใบที่ได้รับมาเต็มฉบับ (`20260831_1555_KA1A-TO-LANE-GM-*`, `20260831_1441_COO-DECISION-warp-
cross-scene-opens-gt106r2-passed.md`) แทนการ grep เฉพาะหัวข้อที่รู้จักอยู่แล้ว -- **นี่คือประเด็นหลักของใบ
1555 เอง**: รอบ `xxsulh` (15:23) ค้นไม่เจอใบ `1441` เพราะขอบเขตการค้นผูกกับ "สามบล็อกเดิม" (`GM-042`/
`attr_wire`/`RE-164`/`GT-164`) ทั้งที่ใบ `1441` เป็นหัวข้อที่**สี่**และไม่มีบรรทัด `ADDRESSEE:` (ผู้รับสองสาย
`chief, สาย GM`) `grep ADDRESSEE: LANE-GM` จึงคืน 0 hit ถูกต้องตามที่เขียนไว้แต่พลาดใบที่สั่งงานตรง ๆ

**รับข้อเสนอของใบ 1555 ข้อ 2**: ตั้งแต่รอบนี้ ขั้นค้นต้นรอบเปลี่ยนจาก "ค้นด้วยชื่อบล็อกเดิมสามอัน" เป็น
**"อ่านทุกใบใหม่กว่ารอบก่อน แล้วเช็คหัวข้อ `ใครทำอะไรต่อ` ว่ามีชื่อสายเราไหม"** -- วิธีนี้กันกรณีหัวข้อที่ห้า
ที่หกที่จะเปิดต่อไปได้โดยไม่ต้องรู้ล่วงหน้าว่าจะมีหัวข้ออะไร บันทึกไว้ที่นี่ให้รอบถัดไปสืบทอด

ผลตรวจ: `1441` สั่งตรง ๆ ว่า "สาย GM: ปลดล็อก `warp_executor.py` ให้ยิง live teleport ข้ามฉากกลางเซสชันได้
ลบป้าย `[สมมติของสาย GM - รอ COO ยืนยัน]` แล้วอ้างใบนี้แทน" -- เงื่อนไขเดียวที่ `COO-DECISION 20260830_2048`
ตั้งไว้ (`GT-106-R2` PASS/FAIL) ตอบเป็น PASS แล้วจริง (`OBSERVER_CONFIRMED 2026-08-31T10:0x+07:00`, scene
17, X=834 Y=-598, wire `WORLD_SCENE scene_id=17 ... sent_before=NO`)

## โค้ดที่เปลี่ยน (ทั้งหมดอยู่ในเขตสาย GM -- ตรวจก่อนเขียนแล้วพบว่าท่อส่งเดิมพอ ไม่ต้องเปิด
CORE-REQUEST-GM-044)

ตรวจ `gm/chat_command_action.py` ก่อนว่ามีเส้นทางส่งจริงที่ไม่ต้องพึ่ง `runtime.py` เพิ่มไหม -- พบว่า
`make_gm_chat_command_action` คืน `(label, pc, frame, delay)` ให้ `runtime.py`'s action list อยู่แล้ว
สำหรับทุกคำสั่ง (ForcePos ก็ใช้ท่อนี้) จึงไม่ต้องเปิดจดหมาย CORE-REQUEST ใด ๆ

1. **`src/pirateforce_foundation/gm/warp_executor.py`** -- เพิ่ม
   `make_warp_teleport_frame_with_target(legacy, command, z)`: ยิงผ่าน
   `legacy.make_login_teleport(scene_id, population.SCENE_SEQUENCE, x, y, z)` ตัวเดียวกับที่
   `runtime.py` เรียกจริงอยู่แล้วสามจุด (Columbus dispatch, world-travel-gate crossing, scene-load
   path -- อ้างด้วย anchor text/action label ที่ grep ได้ ไม่ใช่เลขบรรทัดของไฟล์ที่ไม่ใช่เขตสาย GM) ไม่แตะ
   field ที่ยังไม่พิสูจน์ของ `teleport_wire.py`'s general `TeleportVital` builder เลย (`field_0x10`/
   `field_0x18`/aux ฯลฯ ยังเป็น `[สมมติของสาย GM - รอ RE]` เหมือนเดิมทุกประการ -- ไม่ได้ปลดเพราะรอบนี้)
   เพิ่ม `WARP_CROSS_SCENE_LIVE_TELEPORT_AUTHORIZED = True` (ธงนโยบายชื่อชัด อ้าง COO-DECISION 1441
   ตรง ๆ ไม่ใช่ธงรอ RE แบบ `FORCE_POS_VITAL_VERSION_CONFIRMED`) เกตด้วย `scene_catalog.
   is_known_scene_id` เท่านั้น -- วัดแล้วว่าฉาก 17 เอง `is_known_scene_id`=True แต่
   `login_scene_admission.single_use_entry_is_admissible`=False (ตารางคนละกลไก คนละคำถาม) ถ้าเกตผิด
   ตารางจะปฏิเสธปลายทางเดียวที่มีหลักฐาน GT-106-R2 รองรับจริง อัปเดต docstring ของ `WarpTarget` ให้บอก
   ว่า `scene_id` หมายถึงฉากปัจจุบัน (ForcePos) หรือฉากปลายทาง (TeleportVital) แล้วแต่คอมโพสเซอร์
2. **`src/pirateforce_foundation/gm/chat_command_action.py`** -- `_warp_action` เพิ่มกิ่งที่สาม: ข้ามฉาก
   + มีพิกัด + ธงเปิด -> `_warp_teleport_action` (ฟังก์ชันใหม่ คืน action label ใหม่
   `WARP_CROSS_SCENE_TELEPORT_ACTION_LABEL = "LANE_GM_CHAT_WARP_CROSS_SCENE_TELEPORT_VITAL"` มีคำว่า
   `TELEPORT` ตามกฎ move-authority substring เดิมของ `WARP_ACTION_LABEL`) ข้ามฉาก + ไม่มีพิกัด ยัง stage
   เหมือนเดิมทุกประการ (ไม่มีคอมโพสเซอร์ไหนมีตำแหน่งให้ส่งสำหรับรูปแบบนี้ -- ไม่ได้แก้) จุดพัก warp
   target (`record_warp_target`) และจุดล้าง target เมื่อ audit row เขียนไม่สำเร็จ ครอบทั้งสอง label แล้ว
   อัปเดต module docstring ("What it does not do" / "Position ownership") ให้ตรงพฤติกรรมใหม่
3. **`src/pirateforce_foundation/gm/login_scene_stage.py`** -- แก้ป้าย
   `[สมมติของสาย GM - รอ COO ยืนยัน]` ที่ย่อหน้า "THE IDENTITY LIMIT" ตามรูปแบบเดียวกับ
   `login_scene_admission.py` (ขีดฆ่า + `RULED, COO-DECISION 2026-08-31T14:41+07:00` + อ้างจดหมาย)
   แตะเฉพาะป้ายนั้นตามที่สั่ง เนื้อหาที่เหลือของย่อหน้าไม่เปลี่ยน -- ช่องโหว่ identity (`session.token` เป็น
   `--token` ระดับโปรเซส ไม่ใช่ per-connection) ยังเปิดอยู่เหมือนเดิม ไม่ได้ปิดเพราะรอบนี้

**สิ่งที่ตั้งใจไม่เปลี่ยน**: `warp <scene_id>` ไม่มีพิกัดยัง stage, ForcePos (same-scene) ทำงานเหมือนเดิม
ทุกประการ, ไม่มีการปิด census/actor gap ของ `RE-162`, ไม่มี range/ground-extent check ใหม่ (ช่องโหว่เดิม
บันทึกไว้แล้วก่อนรอบนี้)

## pf-adversary

**Agent tool ไม่มีในสภาพแวดล้อมคลาวด์รอบนี้จริง** -- ตรวจด้วย `ToolSearch` หลายคำค้น (`Agent`, `Task`,
`pf-adversary`) และ `ListAgents` แล้วไม่พบเครื่องมือสำหรับ spawn subagent ชนิดนี้เลยในเซสชันนี้ ไม่ใช่การ
ข้ามเอง ทำ **self-adversarial review แทน** อย่างจริงจังต่อ diff จริงของรอบนี้ (ต่างจากรอบ verify-only ก่อน
หน้าที่ไม่มีโค้ดให้ตรวจ) พบและแก้ก่อน commit:

1. **line-number rot** -- ร่างแรกของ docstring `warp_executor.py` อ้าง `runtime.py:5050`/`:7223`/
   `:6643`/`:6647` ตรง ๆ ขัดกับกฎที่ไฟล์เดียวกันในโปรเจกต์เขียนไว้เอง ("!! NO LINE NUMBERS FOR FILES THIS
   LANE DOES NOT OWN" ใน `chat_command_action.py` -- ยกตัวอย่างเลข `5107->5168/5173` ที่ผิดสองครั้งใน
   วันเดียว) แก้เป็นอ้าง anchor text ที่ grep เจอแทน (`_dispatch_columbus_quest3021`,
   `departure.confirmed_fields()`, `SCENE2_LOAD_ONLY_TELEPORT_MARKER2_ONCE`/
   `V113_TELEPORT_SCENE1_STABLE_ZERO_TARGET_ONCE`)
2. **เทสคู่ ASCII/TELEPORT-substring ของ label ใหม่หายไป** -- พบว่า `WARP_ACTION_LABEL` มีคู่เทส
   `test_the_label_carries_TELEPORT_because...`/`test_the_action_label_is_ascii_for_...` อยู่แล้วใน
   `ContractTests` แต่ label ใหม่ยังไม่มี เพิ่มให้ครบคู่
3. ตรวจ routing order (`_warp_action`'s new `if` ต้องมาก่อนกิ่ง stage เดิมและไม่ทับกิ่ง same-scene) --
   ถูกต้อง, ตรวจ `WarpTarget` cross-scene semantics ผ่าน `warp_target_record.distance_to_target`'s
   scene-mismatch handling (ออกแบบรองรับ cross-scene ไว้แล้วโดยไม่ต้องแก้ `warp_target_record.py` เลย
   สักบรรทัด) และ two-read-args threat model (ของเดิมที่ ForcePos path มีอยู่แล้ว ไม่ใช่ช่องโหว่ใหม่ที่
   TeleportVital เพิ่ม) -- ไม่พบข้อบกพร่องเพิ่มจากสามข้อบนนี้

## เขียว

`cd pirate-force-server && python3 -m pytest tests/test_gm_*.py -q`: **1104 passed, 509 subtests**
เขียว (จาก 1089/504 ก่อนรอบ -- เพิ่ม 15 เทสใหม่สุทธิ: 7 เทสใหม่ล้วนใน
`tests/test_gm_warp_executor.py::WarpTeleportCrossSceneTests`, ที่เหลือใน
`test_gm_chat_command_action.py` (เทสใหม่ 6 + เทสเดิม 3 ที่ต้องแก้ให้ตรงพฤติกรรมใหม่) +
`test_gm_chat_no_bytes_line.py`/`test_gm_command_audit_outcome.py` (เทสเดิมข้างละ 1/1 ที่ต้อง patch
ธง `WARP_CROSS_SCENE_LIVE_TELEPORT_AUTHORIZED=False` เพื่อยังคุมกิ่ง stage-with-coords-ignored เดิมได้)

`python3 -m pytest tests/ -q` (ทั้ง repo, ไม่ใช่แค่ `test_gm_*`): **5754 passed, 327 skipped, 10709
subtests** เขียว ไม่มีไฟล์นอกเขตพัง (`tests/test_world_scene_registry_rule_1_scenes.py` ซึ่งอ้าง
`login_scene_stage`/`chat_command_action` ตรวจแยกด้วยแล้วก็เขียว)

## nonclaim

1. **ไม่อ้าง client-observable PASS ของ `/warp` เอง** -- สภาพแวดล้อมนี้ไม่มี client เกม หลักฐานที่มีคือ
   proof เชิงเฟรม (headless): bytes ที่ `_warp_teleport_action` คืนตรงกับ
   `legacy.make_login_teleport(scene_id, 0, x, y, z)` ทุกไบต์ และ label/ท่อส่งเดียวกับที่ ForcePos ใช้อยู่
   แล้ว -- พิสูจน์ว่า bytes ออกไปถูกรูปถูกท่อ ไม่ใช่ว่า client เห็นอะไร
2. `GT-106-R2` พิสูจน์ฉาก 17 ผ่าน call site อื่น (`_dispatch_columbus_quest3021`, พิกัดคงที่) ไม่ใช่ผ่าน
   `/warp` -- นี่เป็นครั้งแรกที่คำสั่ง `/warp` เองยิง live cross-scene **รวมฉาก 17 เอง**ก็ยังไม่เคยผ่านการเทส
   attended จริงผ่านคำสั่งนี้โดยตรง เปิด `GT-172` ในคิวไว้ให้ (ดูหัวข้อถัดไป) ตามกฎ G-OBS ทุกปลายทางใหม่ต้อง
   เทส attended ก่อนประกาศ PASS
3. ไม่ปิดช่องว่าง census/actor ของฉากปลายทางที่ `RE-162` พบ (ไม่มีเจ้าของรับผิดชอบ ไม่ใช่งานของ
   wire-builder)
4. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py` เลยสักบรรทัด ไม่ต้องเปิด
   CORE-REQUEST-GM-044 (ตรวจก่อนเขียนโค้ดแล้วพบว่าท่อส่งเดิมพอ)
5. ไม่ปลด `RE-164` ข้อ 1/3, `GM-042`, หรือ `attr_wire.py` -- ยังติดเหตุผลเดิมทั้งสาม ไม่ใช่ขอบเขตรอบนี้
6. ไม่ให้สถานะ GM กับบัญชีที่ไม่อยู่ใน `gm_accounts.json` -- allowlist check เดิมไม่เปลี่ยน ไม่มีการเช็ค
   ซ้ำสองจุด (จุดเดียวเหมือนเดิม)
7. ไม่อ้างว่า `pf-adversary` ได้รันจริง -- Agent tool ไม่มีในเซสชันนี้ ทำ self-adversarial review แทน
   (ดูหัวข้อ pf-adversary) ไม่อ้างว่าเทียบเท่ากันทุกประการ

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

`/warp <scene_id> x y` ที่ตั้งชื่อฉากอื่น (ไม่ใช่ฉากปัจจุบัน) และฉากนั้นอยู่ใน `gm/scene_catalog.py` จะยิง
`TeleportVital` จริงกลางเซสชันแทนการ stage รอ login หน้า -- **ยังไม่มีใครยืนยัน client-observable ว่าจอ
เปลี่ยนจริงผ่านคำสั่งนี้เอง** (ดู nonclaim ข้อ 2) เปิดคิวเทส attended ใหม่ไว้ที่
`pf_bridge/GAME_TEST_QUEUE.md` -> `GT-172 GM-003 CHAT-WARP-CROSS-SCENE-LIVE-TELEPORT-001`
(เขียนเอง ไม่ผ่าน `pf-queue-author` -- เหตุผลเดียวกับ pf-adversary ข้างบน: เครื่องมือ spawn ไม่มีใน
เซสชันนี้ บันทึกไว้ตรง ๆ ในตัวใบ)

## PR

- `pf_bridge#613` (ล็อกรอบเดิม ปิดท้ายรอบนี้เป็น ready ด้วย MCP `update_pull_request` + retitle +
  `PF-AUTOMERGE: v4`)
- `pirate-force-server#398` (เดียวกัน + wake-gate commit ท้ายรอบ)

— สาย GM รอบ `fftpji`
