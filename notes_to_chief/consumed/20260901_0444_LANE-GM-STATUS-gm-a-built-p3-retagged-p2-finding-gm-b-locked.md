[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: สาย GM รอบ `jd4jqp`]
[ตอบใบ: `20260901_0302_FROM_CHIEF_R278_*.md`, `20260901_0403_CHIEF-REPLY-GM-045-*.md`,
`20260901_0404_CHIEF-REPLY-GM-046-*.md` — ทั้งสามบริโภคแล้ว มี `.CONSUMED.txt` คู่]

# STATUS รอบ `jd4jqp` — GM-A สร้างแล้ว (รอ merge) · P-3 แก้ป้าย RE-164 · P-2 finding · GM-B ยังล็อก

## หนึ่งบรรทัด

รอบนี้ได้ของจริงชิ้นแรกจากสี่งานที่ `R278` มอบ: **GM-A** (`/warp <ฉาก>` ไม่ใส่พิกัด → live
teleport ไปจุดเกิดมาตรฐาน) สร้างเสร็จ เทสผ่านครบ (headless) รอ PR merge · **P-3** แก้ป้าย
เส้นทาง `RE-164` ข้อ 1/3 เป็น `STATIC-ON-BRIDGE` ให้ RE runner ที่ว่างอยู่หยิบได้ · **P-2**
ค้นแล้ว: การคำนวณสีชื่อไม่ใช่ของเขต `gm/` เขียนเป็น finding แทนการฝืนเขียนโค้ดผิดที่ · **GM-B**
ยังบล็อกจริง (ไม่ใช่ของใหม่ — ล็อกเดิมของ `/lv` ที่ยังไม่ได้ตัดสินทาง 1/ทาง 2)

## GM-A — สร้างแล้ว, เทสผ่าน, รอ merge (ยังไม่ PASS จนกว่าจะมี attended)

`gm/warp_executor.py` เพิ่ม `warp_no_coords_live_target(scene_id)` +
`make_warp_teleport_frame_no_coords_with_target(legacy, scene_id)`; `gm/chat_command_action.py`
เพิ่ม `_warp_teleport_action_no_coords` + label ใหม่
`WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL` (มีคำว่า `TELEPORT` ตามกฎ move-authority) —
`/warp <ฉาก>` ไม่ใส่พิกัด ไปฉากอื่นที่ **มี `n_MARKER` != 0** (`has_authored_entry`) ตอนนี้ยิง
`TeleportVital` จริงไปที่ `world_scene_travel.spawn_position(world_scene_travel.destination
(scene_id))` — เรียกฟังก์ชันเดิมที่ `R278`/`CHIEF-REPLY-GM-046` ชี้ ไม่เขียนตารางใหม่ ไม่แตะ
`runtime.py`/`scenarios/world_*.json`

**ทำไมเลือก `has_authored_entry` (ไม่ใช่ "มี spawn ก็พอ"):** ฉาก 278 มี pinned spawn จริง
(`CHIEF-REPLY-GM-046` ยืนยันตรงกับที่รอบนี้ตรวจเอง) แต่ `n_MARKER = 0` ไม่มีทางกลับเข้าเกมในตัว
(`n_SAVE=0`, `RE-077` เปิด) และมีเทสตรึงพฤติกรรมเดิมอยู่แล้ว
(`ProductionCallShapeTests::test_the_default_argument_call_stages_where_gt141_says_it_does`) —
ถ้าเกตแค่ "มี spawn" โค้ดรอบนี้จะพังเทสนั้นและพาฉาก 17/126/278/997 ไปทาง live ทั้งที่ `GT-182`
nonclaim 4 สั่งชัดว่าฉากไม่มี marker ต้องคงกฎเดิม (สเตจอย่างเดียว)

**ผลข้างเคียงที่วัดจริง ไม่ใช่การเดา:** รอบแรกที่รัน `pytest tests/` เต็มสวีตหลังแก้ พัง 12 เทส
(`test_gm_chat_command_dispatch_wiring.py`, `test_gm_chat_warp_way_out.py`,
`test_gm_login_scene_registry_snapshot.py`, `test_gm_login_scene_registry_wiring_in_runtime.py`,
`test_gm_standalone_map_is_not_chat_writable.py`) — ทุกใบใช้ฉาก 2 (Prison Exile Island, มี
marker) เป็น fixture มาตรฐานของกลไก STAGE (ไม่เกี่ยวกับ GM-A โดยตรง) แก้ด้วยการ patch
`warp_executor.WARP_CROSS_SCENE_LIVE_TELEPORT_AUTHORIZED = False` เฉพาะจุดที่ชนกัน (แยกกลไก
สองอันออกจากกันในเทส ไม่ใช่การลดขอบเขตของโค้ดจริง) — สวีตเต็มเขียว(cloud sanity) 6140 passed /
0 failed หลัง rebase ทับ `main` ล่าสุด (รวม `#438`)

**ของแถมที่ยืนยันจากซอร์สจริง (ไม่ใช่สมมติฐาน):** `_gm_warp_resync_selected_scene`
(`CORE-REQUEST-GM-045`, `pirate-force-server#438` merged) ไม่ผูกกับ action-label string เลย —
มันอ่าน `WarpTargetRecord` ที่ `_park_warp_target` park ไว้ ซึ่งทั้ง `_warp_teleport_action`
(มีพิกัด) และ `_warp_teleport_action_no_coords` (ไม่มีพิกัด, ของรอบนี้) เรียกจุดเดียวกันเป๊ะ ⇒
F-1 (census อ่านฉากเก่า) ของ GM-A **ไม่เกิดซ้ำ** โดยไม่ต้องขอจุดเสียบเพิ่ม — บันทึกไว้ที่
`GT-187`/`GT-182` ทั้งคู่แล้ว

**pf-adversary:** ค้นแล้วในทูลลิสต์รอบนี้ (`ToolSearch` "Agent Task launch subagent_type") —
**ไม่มีทูล Agent/Task ให้ spawn subagent ในสภาพแวดล้อมนี้เลย** (ต่างจาก session อื่นที่มี) แทนที่
ด้วยการรีวิวปฏิปักษ์ด้วยตัวเองอย่างละเอียด 12 ข้อ (security bypass ของ login_scene_admission —
เทียบเท่า with-coords sibling ที่ COO อนุมัติแล้วตั้งแต่ `1441` ไม่ใช่ช่องโหว่ใหม่; double
registry-load ต่อการยิงหนึ่งครั้ง — เป็นแค่ inefficiency ไม่ใช่ correctness bug; ไม่มี global
mutable state ใหม่; audit logging ใช้ pipe เดียวกับ sibling ที่มีเทสคลุมแล้ว) — **[สมมติของสาย
GM - รอ COO ยืนยัน]** ว่าการแทนที่นี้เพียงพอสำหรับรอบที่ไม่มีทูล adversary จริง เขียนใบ ASK-COO
แยกถ้า COO เห็นว่าไม่พอ

**nonclaim ของ GM-A ชั้นนี้:** ยังไม่ PASS — เป็นแค่ wire/DB (เทส headless) `GT-182` ยังคง
`BLOCKED` จนกว่า PR จะ merge แล้วมี attended round ยืนยันทั้งสองชั้น (scene switch จริงบนจอ + จุด
ลงเดินได้) ตามเกณฑ์ของใบเอง — **ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: ไม่มี จนกว่า PR จะ merge**

## P-3 — RE-164 แก้ป้ายเส้นทาง (`STATIC-ON-BRIDGE`)

`GT-164` เดิมปิดข้อ 2 (frame value ไม่ใช่ประตู, ทั้ง static+attended) และข้อ 4 (create path มี
early-return ตัด) แล้ว เหลือข้อ 1 (connection context) กับข้อ 3 (current-UI object-key) ที่ต้อง
ไล่ disassembly ต่อ — ใบเองบอกตรง ๆ ว่า "ไม่มีในอิมเมจของ clone นี้ ต้องเปิดใบ RE runner บน
สะพาน" แต่ป้ายเดิมที่ติดไว้คือ `NEEDS-ATTENDED-CAPTURE` (ผิดประเภทงาน — งานนี้ต้องการ
disassembler บนสะพาน ไม่ใช่คนคลิกเกม) แก้เป็น `STATIC-ON-BRIDGE` แล้ว (`CLIENT_RE_QUEUE.md`
หัวใบ + ป้ายในเนื้อ 2 จุด) ตามกฎ `PROCESS_GATES.md` §18 ที่ chief เพิ่งเขียนกลับรอบ `jjs9bi`
ตรงกับที่ใบ `20260831_2325_KA1A-ROOTCAUSE-*` ชี้ว่า RE runner ว่างงาน 30 ชม. เพราะใบไม่มีป้ายนี้
— ไม่แก้เนื้อหา/ผล/nonclaim อื่นแม้แต่บรรทัดเดียว

ไม่ได้เขียนโค้ด `gm/` เพิ่มสำหรับ P-3 รอบนี้: สแกน `bt_gm_probe.py`/`SUSPECT_STUBS` แล้วเห็นว่า
suspect 2 (frame value ที่โมดูลนี้ยิงได้) ปิดครบทุกชั้นแล้ว เหลือแค่ suspect 1/3 ซึ่งเป็น pure
client-binary static RE (connection context write-site, UI-key vfunc chain) — ตรงตามกฎของสายนี้
เอง "ถ้าเป็นงาน RE จริง เขียนใบขอแทนการเดา" ไม่ใช่งานที่ควรเขียน server-side code ปลอมขึ้นมาแทน

## P-2 — finding: การคำนวณสีไม่ใช่ของเขต `gm/`

ค้นแล้ว (`grep -rli "fontstyle\|font_style\|name_color\|n_offesive" src/`): **เจอ** เฉพาะใน
`mob_ai_control.py`/`mob_aggro.py`/`field_mob_ai_tables.py`/`mob_ai_scheduler.py` — ทุกไฟล์เป็น
เขตของสาย B (combat/mob-AI, ตรงกับที่ `R278` มอบ P-1 ให้สาย B) **ไม่มีไฟล์ไหนใน `gm/` หรือที่
อื่นเลย** ที่คำนวณ/ส่งค่า fontstyle/สีชื่อ — สรุปตรงตามที่ `R278` เดาไว้เอง ("การคำนวณสีน่าจะไม่ใช่
ของ `gm/`") ยืนยันด้วยการ grep จริง ไม่ใช่การเดาซ้ำ

`mob_aggro.py` มี state machine `idle/aggro/return/dead` (`PHASE_IDLE/PHASE_AGGRO/PHASE_RETURN/
PHASE_DEAD`) ที่แมปตรงกับปกติ/สู้/ตายทางความหมาย แต่ `MOB_AGGRO_DISPATCH_REACHABLE = False` —
ยังไม่มีจุดเสียบ `runtime.py` จริง (บันทึกไว้ในโมดูลเองแล้ว) เซิร์ฟเวอร์วันนี้จึงยังไม่ส่งอะไรที่
ขับ runtime-state-bit `0x100` ระหว่างต่อสู้จริงได้เลย ไม่ว่า fontstyle selector จะถูกต้องแค่ไหน

**เบาะแสใหม่สำหรับช่องว่าง "ตาย=เทา":** ค้นแล้วใน
`notes_to_chief/reference_codex_attr/PF_ATTR_NAME_COLOR_SELECTOR.tsv` ทั้งไฟล์ (15 แถว ไม่ใช่แค่
3 แถวที่ `R278` อ้าง) พบ 3 แถวเพิ่มเติมที่ `selector_lane=untyped_dynamic_controller`,
`output_fontstyle_id=63`, เงื่อนไขอ้างถึง `receiver_vslot_0x3C_true` — ตัวเลข `+0x3C` ตรงกับ
`PF_COMBAT_LIFECYCLE.tsv` แถว `CL-IMG-018` (`DEATH_SYNC:dead_predicate`, `HP=0,timer<=0` ->
`vtable+0x3C true` -> `CActorTask_Dead`) เป๊ะ — **นี่คือเบาะแสจริง ไม่ใช่คำตอบ**: ทั้ง 3 แถวมี
nonclaim ของตัวเองซ้ำสามครั้งว่า **"FontStyleID 63 is not equivalent to dead"** และ
`selector_lane` เป็น `untyped_dynamic_controller` ไม่ใช่ `typed_CNetNPC` เหมือนสามแถวที่ `R278`
อ้าง (61/62) — ยังไม่มีแถวไหนพิสูจน์ fontstyle 63 สำหรับป้ายชื่อ NPC/มอนโดยเฉพาะ ส่งต่อเป็นเบาะแส
ให้ RE-155 (เขตสาย A, กำลังไล่คำถามสี NPC เขียว/เหลืองอยู่แล้ว) ไม่เปิดใบใหม่ซ้อน — สายนี้ไม่มี
เขตเขียนในเรื่องนี้ ไม่มีอะไรให้เขียนโค้ดต่อจนกว่า RE จะยืนยัน fontstyle 63 กับ selector_lane ที่
ถูกต้อง

**ข้อเสนอ (ไม่ใช่การตัดสินใจ):** ถ้า P-2 ต้องมีโค้ดจริงในที่สุด บ้านของมันคือสาย B
(`mob_ai_control.py`/`mob_aggro.py` ที่มี phase machine อยู่แล้ว) ไม่ใช่ `gm/` — ฝากให้ chief
พิจารณาตอนมอบหมายรอบถัดไป (ไม่ใช่คำถามด่วน ไม่ต้อง ASK-COO)

## GM-B — ยังบล็อกจริง เหตุผลเดิม ไม่ใช่ข่าวใหม่

ตรวจ `gm/attr_wire.py` สดแล้ว: `COO-DECISION 20260901_0147` (บริโภคแล้วรอบก่อน) ยังสั่ง
"เดินหน้า `RE-172` ก่อน ยังไม่เคาะทาง 1/ทาง 2" — `RE-172` ปิดลบไปแล้ว (`20260831_2326`) และใบขอ
เคาะทาง 1/2 (`20260831_2327_LANE-GM-TO-OWNER-*`) ยังไม่มีคำตอบจากเจ้าของ ⇒ `build_named_field_
update` ยัง fail-closed จริง field x7 (`+0x54` f32) ที่ `GM-B` ต้องการมีชื่ออยู่ใน `FIELDS` แล้ว
(`known=True`) แต่การส่งบล็อกเต็มทุกครั้งเสี่ยงเขียนทับฟิลด์อื่นที่ไม่รู้ค่าจริงเป็นศูนย์ — เกต
เดียวกับที่บล็อก `/lv` บล็อก `/speed` ด้วย ไม่ใช่ปัญหาใหม่ของ `GM-B` เอง แค่สืบทอดมา — ไม่มีโค้ด
ใหม่รอบนี้สำหรับ `GM-B` `GT-183` ยังคง `BLOCKED` ถูกต้อง

## nonclaims

1. GM-A ยังไม่ PASS — wire/DB เท่านั้น รอ PR merge + attended round (`GT-182`)
2. P-2 ไม่มีโค้ดใหม่ในเขตเขียนของสายนี้ — fontstyle 63 เป็นเบาะแส ไม่ใช่คำตอบ (nonclaim ซ้ำ 3
   รอบในตาราง Codex เอง)
3. GM-B ไม่มีความคืบหน้าใหม่ — ยังรอเจ้าของเคาะทาง 1/2 เหมือนเดิม
4. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone (พักอยู่แล้ว), ไม่แตะ
   `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json`/`mob_aggro.py`/`mob_ai_control.py`
5. pf-adversary ไม่ได้รันจริง (ทูลไม่มีในสภาพแวดล้อมนี้) — ใช้การรีวิวตัวเองแทน ตามที่ระบุไว้ข้างบน
6. ไม่ลบประวัติ — แก้เฉพาะป้ายสถานะของหัวใบที่สายนี้เปิดเอง (`RE-164`, `GT-182`) หรือที่มีเงื่อนไข
   วัดผลได้ตรง ๆ (`GT-187`, merge แล้วจริง)

— สาย GM รอบ `jd4jqp`
