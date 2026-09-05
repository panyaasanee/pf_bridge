round: R355 (cool-johnson-oiysl5)
lane: LANE-E (chief)
time: 2026-09-05T15:22+07:00 start

## หัวข้อ 2 ข้อ 7 -- ชะตา PR ของรอบก่อน
pf_bridge: ไม่มี [LANE-E] PR ค้าง -- รอบก่อนปลดล็อกเรียบร้อย
pirate-force-server: server#794 (LANE-E round `5e00uw`/R348, grant LANE-UI's CORE-REQUEST trace-path
observer) ยังเปิดอยู่หลังผ่านมา 10+ ชั่วโมง, `mergeable_state=dirty` (conflict กับ main), 0 CI runs
(สถานะ pending). server#795 ของรอบเดียวกัน merge ไปแล้ว -- นี่คือครึ่งที่ตกค้าง

แก้: fetch `lane-e-5e00uw-corereq-ui`, merge origin/main เข้าไป, conflict เดียวใน
`src/pirateforce_foundation/ui_tracepath_wire.py` (module docstring, ทั้งสองฝั่งเขียนย่อหน้า
เดียวกันคนละเวอร์ชัน -- ฝั่ง main ใหม่กว่าและครอบเนื้อหาฝั่ง HEAD ทั้งหมดรวมส่วนที่ปิด RE-236(b)
ที่ HEAD ยังไม่รู้ -- resolve โดยรับฝั่ง main) push กลับไปที่ branch เดิม (ไม่เปลี่ยน PR number)
เทสแคบที่เกี่ยวข้อง (`test_ui_tracepath_wire.py` + `test_trace_path_wiring.py` + `test_lane_hooks.py`
+ `test_ui_lane_hooks_wire_log.py`) 84 passed หลัง merge · `mergeable_state` เปลี่ยนเป็น `unstable`
(ไม่มี conflict แล้ว รอเกตตัดสิน) -- ไม่รอ merge ในรอบนี้ ปล่อยให้ workflow ตัดสิน

## RE-259 / RE-260 header close-out
ตามคำขอ LANE-DB (`notes_to_chief/20260905_1425_...`) -- ตรวจว่าไฟล์ผลทั้งสองมีจริงและถูก consume
แล้ว จากนั้นแก้หัวใบ `CLIENT_RE_QUEUE.md:5497`/`:5553` ตามที่ขอเป๊ะ · stub จดหมายต้นทาง

## CORE-REQUEST-0542 (LANE-DB, starting-skill door) -- wired เป็น PR แยก
`pf_bridge/notes_to_chief/20260904_0542_...` ขอจุดเสียบเดียว: หลัง `class_id` ถูก resolve ที่
`CharacterLifecycle.create`, เรียก `persistence_starting_skills.resolve_starting_skill_ids` แล้ว
`store.grant_starting_skills`

ทำ: `lifecycle.grant_starting_skills_for_class(store, character, class_id)` เรียกที่จุดเดียวกับ
`persist_class_id_from_starting_gear` ใน `create()` · เทสจบ-ถึง-จบสี่ตัวใหม่ + เทส fault-injection
สี่ตัวใหม่ใน `tests/test_class_id_login_wiring.py`

pf-adversary (สั่งก่อน push ตามกฎบังคับ) พบข้อบกพร่องจริงหนึ่งข้อ: ฉบับแรก gate การเรียกด้วย
`resolved_class_id is not None` (คืนค่าจาก `persist_class_id_from_starting_gear`) -- ค่านั้นเป็น
`None` ทุกครั้งที่ resend ของตัวละครที่ class_id ลงแล้ว (ตามออกแบบ, เป็น NULL-only guard) ⇒ ถ้า
`store.grant_starting_skills` ล้มแบบชั่วคราวในรอบที่ชนะ (database locked ฯลฯ ที่ `try/except`
ของฟังก์ชันนี้เขียนไว้ให้จับอยู่แล้ว) ตัวละครจะติด class_id แต่ไม่มีสกิลตลอดไป ไม่มี backfill
ปิดช่องนี้เหมือนที่ LANE-DB ทำให้ class_id เอง -- มิวแทนต์ยืนยันแล้วว่า 36/36 เทสเดิมผ่านแม้ลบ
gate ทิ้งไปเลย (เพราะ `resolve_starting_skill_ids(None)` เองก็ raise TypeError ที่ถูกจับไว้
บังเอิญให้ผลภายนอกเหมือนกัน)

แก้: เพิ่ม `_class_id_for_a_retried_skill_grant(store, character_id)` -- อ่านค่า `class_id` จริง
บนแถวเมื่อ resend เจอคอลัมน์ที่ set แล้ว **และ** `list_character_skills` ยังว่างเปล่าเท่านั้น (แยก
"grant ครั้งแรกล้มชั่วคราว ต้อง retry" ออกจาก "อีกคนแก้ class_id ทีหลัง สกิลมีอยู่แล้ว ห้ามยุ่ง" --
สองกรณีนี้คืนค่า `None` เหมือนกันจาก `persist_class_id_from_starting_gear` แต่ต้องการคำตอบตรงข้าม
กัน) · เพิ่มเทส regression จำลอง flaky grant ครั้งแรกแล้ว resend ครั้งที่สองต้องได้สกิลครบ · เพิ่ม
เทสยืนยันว่าตัวละคร classless ไม่มีบรรทัดคอนโซล `CHARACTER_STARTING_SKILLS` เลย (ปิดช่องมิวแทนต์
ที่ adversary จับได้)

มิวแทนต์ที่ adversary รายงานถูกวัดซ้ำด้วยมือหลังแก้: ลบ gate `if class_id_for_skills is not None:`
ทิ้ง -> เทส `test_gear_matching_no_preset_grants_no_skills` แดงทันที (ก่อนแก้: ผ่านทั้งชุด)

เขต client-observable: ไม่มี -- ยังไม่มีเฟรม/หน้าต่างสกิลส่งไปที่ client (letter ต้นทางระบุไว้ว่า
ขอบเขตคือ DB ก่อน หน้าต่างเป็นคิวถัดไป) ⇒ ไม่เปิด GT ใบใหม่รอบนี้ (G5, สองชั้นห้ามปน)

ชุดเทสเต็ม: กำลังรันบน `lane-e-cool-johnson-oiysl5-starting-skill-hookup` (แยกกิ่งจาก `#794` เพราะ
คนละเรื่อง -- กฎขนาด PR หนึ่งเรื่องต่อใบ) -- ผลจะอยู่ในไฟล์รอบต่อท้าย/PR body

## GM-059 -- ตัดสินเขต ไม่ใช่โค้ด
LANE-GM เสนอ CORE-REQUEST-GM-059 (คืน `foundation.selected.position.scene_id` หลัง warp rollback)
แต่ตัวจดหมายเองแสดงว่าบรรทัดจริงต้องอยู่ที่ `gm/warp_send_watch.py:547-553` -- เขตเขียนของ LANE-GM
เอง ไม่ใช่ `runtime.py` (ที่ COO 1150 ข้อ 2 มอบให้ chief เพราะเข้าใจผิดว่า `selected` กระจายอยู่ใน
runtime.py หลายจุด) ⇒ เขียนจดหมายคืนเขตให้ LANE-GM ทำเอง (มีเทสมิวแทนต์พร้อมอยู่แล้วในจดหมายต้นทาง)
ไม่แตะโค้ด -- นี่คือคำตัดสินของ chief ไม่ต้องรอ Panya (หัวข้อ 0: ติดแล้วต้องการคำตัดสิน)

## CORE-REQUEST backlog -- ยังไม่ต่อ
- `0844` (LANE-DB class_id backfill boot loop ใน app.py) -- ค้างมาตั้งแต่ R341 หลายรอบ, ยังไม่ตรวจ
  รอบนี้ (ของบวมเกิน scope)
- `1652` (LANE-B ground-seed เมื่อ session รู้ฉาก, สองบรรทัดใน runtime.py) -- เช่นกัน
- `1352` (LANE-B ส่ง class_id ของ performer เข้า pose composer, บรรทัดเดียวใน runtime.py) --
  **ปลดบล็อกแล้ว**: `1353` (LANE-DB store reader) merge แล้วใน server#830 -- นี่คืองานแรกที่ควร
  ทำต่อรอบหน้า ไม่ใช่ของยาก แค่ไม่มีเวลาในรอบนี้หลังพบ defect ของ starting-skill hookup

## WIRED v2
ไม่ได้วัดรอบนี้ -- รอบเน้นกู้ PR ค้างและปิดหนี้เดิม ไม่ใช่รอบสาย lane_hooks

## เก็บกวาด
stub จดหมาย 5 ใบ (RE-259/260 close-out, GM-053 เก่าที่ตอบแล้วแต่ไม่เคย stub, LANE-A 1339
confirm-to-arrival ที่ landed แล้วแต่ไม่เคย stub, GM-059) -- ไม่มีเวลาไล่ housekeeping เต็มรูปแบบ
(CHIEF_CONTINUATION 45KB เกินเพดาน 30KB ที่ยังไม่แก้, AGENTS.md ไม่ได้ตรวจขนาดรอบนี้)

## 🔴 เกือบพลาดกฎ AGENTS.md:103 (ห้ามตั้งชื่อสาขาเอง)
ระหว่างเตรียม branch สำหรับ starting-skill hookup, ครั้งแรกตั้งชื่อเอง
(`lane-e-cool-johnson-oiysl5-starting-skill-hookup`) ก่อน push แล้วจับได้เอง (กฎ 103 อยู่ใน AGENTS.md
อยู่แล้วจากบทเรียน server#794 ตัวเดียวกับที่รอบนี้กำลังกู้) -- แก้ทันก่อนเปิด PR โดยย้ายคอมมิตไปที่
`claude/friendly-darwin-oiysl5` (สาขาที่ระบบกำหนดให้เซสชันนี้จริง) branch ผิดชื่อยังค้างอยู่บน remote
เฉยๆ (ลบไม่ได้ 403 จาก proxy) แต่ไม่มี PR ผูกอยู่ -- ไม่มีผลอะไรต่อ

## สถานะ PR ท้ายรอบ (ตามหัวข้อ 3 ข้อ 4 -- ห้ามเขียนว่าเสร็จ)
- **pf_bridge**: push แล้วขึ้น `claude/cool-johnson-oiysl5` (commit `c9e85e7b`) · claim PR #1338
  รอเติม marker ปลดล็อกตอนจบรอบ
- **pirate-force-server server#794** (รอบก่อน, กู้ conflict แล้ว): push แล้ว, `mergeable_state=unstable`
  (ไม่ conflict แล้ว รอเกตตัดสิน) -- ยังไม่ merge ณ เวลาที่เขียนบรรทัดนี้
- **pirate-force-server server#833** (ใบใหม่รอบนี้, starting-skill hookup): เปิดแล้วบน
  `claude/friendly-darwin-oiysl5` (commit `412303c9`), marker อยู่, `mergeable_state=unstable`
  (รอเกต) -- ยังไม่ merge ณ เวลาที่เขียนบรรทัดนี้
- ห้ามเชื่อว่างานอยู่บน main จนกว่ารอบถัดไปเห็น `merged=true` ทั้งสองใบ (หัวข้อ 2 ข้อ 7)
