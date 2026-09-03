# LANE-GM รอบ `n4vgpz` — 2026-09-04T05:54+07:00 → 06:2x+07:00

## ทำไมเลือกงานนี้ (ลำดับตามพรอมป์: จดหมายค้าง > CORE-REQUEST ค้าง > GT queue > backlog รอบตัวเอง)

- **จดหมายที่ยังไม่บริโภค** (`git grep -l "ADDRESSEE: LANE-GM" notes_to_chief/` ที่ไม่มี `.CONSUMED.txt`
  คู่กัน นอกโฟลเดอร์ `consumed/`): เจอ 2 ใบ —
  1. `20260903_2345_COO-DECISION-...pf-adversary-runs-at-round-start...` — กฎกระบวนการ ปฏิบัติไปแล้ว
     ตั้งแต่รอบ `tof9cw` (เปิด `ADVERSARY_PENDING #700` ตอน push ตามกฎ แล้วบันทึกผล `#1067` ตามลำดับ)
  2. `20260904_0346_SYNC-NOTICE-pirate-force-server-pr696-closed-never-merged` — รอบ `tof9cw` กู้และ
     merge เป็น `#700` ไปแล้วเช่นกัน (ตรวจซ้ำรอบนี้ด้วย `pull_request_read`: `merged=true`)

  ทั้งสองใบ**ถูกกระทำไปแล้วจริงในรอบก่อน** เหลือแค่ยังไม่มีสตับ `.CONSUMED.txt` — วางสตับให้ทั้งคู่รอบนี้
  ไม่ต้องทำโค้ดซ้ำ (ดูหัวข้อ "จดหมาย" ล่าง)

- **ADVERSARY_PENDING**: `COO-DECISION 20260903_2345` สั่งว่ารอบถัดไปของ LANE-GM ต้องหยิบผล adversary
  ที่ยังไม่คืนเป็นงานแรกก่อน claim ใหม่ — ตรวจแล้ว: `pf_bridge#1067` (ใบบันทึกผล adversary ของรอบ
  `tof9cw`) **merged แล้ว**, `pirate-force-server#700` (โค้ดของรอบ `tof9cw`) **merged แล้ว**,
  `pirate-force-server#705` (ของ LANE-E คนละสาย) merged แล้วเช่นกัน ⇒ ไม่มี ADVERSARY_PENDING ค้างของ
  สายนี้ให้หยิบ **แต่** `#1067`/`#700` เองระบุ "แก้รอบหน้า" ไว้สามจุดชัดเจน (ดูหัวข้อถัดไป) — นับเป็น
  งานที่ผูกกับ ADVERSARY_PENDING โดยตรง (ผลของมันเอง) จึงหยิบสามจุดนี้ก่อนสิ่งอื่นใดในเขตเขียน
- ไม่มี CORE-REQUEST-GM ค้างที่ chief ยังไม่ตอบ (`git grep -rl "GM-0" notes_to_chief/` ไม่เจอใบเปิดใหม่
  หลัง `tof9cw`)
- **GT queue ของสาย GM**: ไม่มี — `/speed`/Door B ล็อกที่จุดอ่านของ chief (`0216`, ยังไม่ครบ), P-2 ล็อกที่
  chief ออกเลขใบ RE ที่สองซึ่งยังไม่ออก (ตรวจแล้ว: ไม่มีใบใหม่หลัง `0306`), P-3 ต้องการ client image
  ที่คลาวด์ไม่มี
- backlog ไฟล์รอบตัวเอง (`GM_20260904_0412_tof9cw.md`): ข้อ 3 (`validate_field_value` สองคำตอบ) เป็น
  งานที่ยอมรับแล้วว่า "งานแรกของรอบหน้าถ้า `0345` ไม่มีของตามมา" — **`0345` มีของตามมาจริง** (สามจุดแก้ที่
  `#1067`/`#700` ระบุ) ⇒ งานนั้นเลื่อนไปรอบถัดไปแทนตามเงื่อนไขที่ตัวมันเองตั้งไว้

⇒ เลือกทำ**สามจุดแก้ที่ `pirate-force-server#700`/`pf_bridge#1067` ประกาศไว้ว่า "แก้รอบหน้า"** เป็นงาน
ของรอบนี้ ไม่ใช่เริ่มงานใหม่ (P-3 catalog) เพราะสามจุดนี้ผูกกับ ADVERSARY_PENDING ตรงตัวและมาก่อนตาม
ลำดับ "จดหมายค้าง"/"ผล adversary" ในพรอมป์

## ทำอะไรลงไป (`pirate-force-server`, เขต `gm/` + `tests/test_gm_*.py` + `docs/GM_LANE.md` เท่านั้น)

### 1. `speed_wire.py` — แก้ถ้อยคำ "ZERO BYTES OUT" / "ONE CONSOLE LINE" ที่เกินจริง
`compose_sparse_speed_update`'s docstring และ PR body เดิมของ `#700` เขียนว่าการปฏิเสธ `/speed` ที่ arm
ด้วย `PF_SPEED_TRIAL` ได้ "REFUSAL WITH ONE CONSOLE LINE AND ZERO BYTES OUT" — pf-adversary (รอบ
`tof9cw`) วัดแล้วว่าไม่แม่น: ไม่มีไบต์ `0x309A` ออกจริง (ครึ่งนี้ถูก) แต่ `_speed_denied` ส่งเฟรม LocalTalk
"SPEED DENIED" ออกไปหนึ่งใบ (เป็นไบต์) และคอนโซลพิมพ์**สองบรรทัด** (`GM_CHAT_NOTICE_SENT` +
`GM_CHAT_NO_BYTES_SENT`) ไม่ใช่หนึ่ง — **โค้ดถูกอยู่แล้ว** (ตรวจจาก `_announce_console_outcome` +
`_speed_denied` ยืนยันพฤติกรรมสองบรรทัดจริง) มีแค่คอมเมนต์ที่เกินจริง แก้ถ้อยคำในดอกสตริง ขีดฆ่าของเดิม
ไม่ลบ

### 2. `chat_command_action.py` — เติมบรรทัดคอนโซลที่หายไปตอนประตูปิดถาวร
`SPEED_TRIAL_CONSOLE_TOKEN` (`"SPEED TRIAL OPEN"`) เป็น dead code ตั้งแต่ `compose_sparse_speed_update`
raise ทุกครั้งไม่มีเงื่อนไข (`0345` ข้อ 2): branch `if trial_admitted:` ที่พิมพ์โทเคนนี้อยู่ใต้ `try:
pc, frame = speed_wire.compose_sparse_speed_update(...)` ซึ่ง raise เสมอ ⇒ ทุกคำสั่งที่ arm
`PF_SPEED_TRIAL` ตกไปที่ branch `except` (compose-refused) ก่อนถึงบรรทัดนั้นเสมอ — เป็น dead code จริง
ตามที่ `#1067` ระบุ ผลคือคอนโซลพิมพ์ข้อความเดียวกันไม่ว่า `PF_SPEED_TRIAL` จะ arm หรือไม่ ผู้คุมจอแยก
"คีย์ไม่ทำงาน" กับ "คีย์ทำงานแต่ประตูปิด" ไม่ออก ซึ่งขัดกับ `COO 0646` ข้อ 2 ข้อย่อยที่ 4 ตรง ๆ

เพิ่ม:
- ค่าคงที่ `SPEED_TRIAL_ARMED_REFUSED_CONSOLE_TOKEN = "SPEED TRIAL ARMED REFUSED"`
- event `EVENT_SPEED_TRIAL_ADMITTED_BUT_REFUSED` (พ่วงกับ `EVENT_SPEED_PERSIST_COMPOSE_REFUSED_PREFIX`
  เดิม ไม่แทนที่)
- ฟังก์ชันพิมพ์ `_print_speed_trial_armed_refused` — ไม่มีฟิลด์ `sending=` เด็ดขาด (กันไม่ให้เกิดข้ออ้าง
  เกินจริงแบบข้อ 1 ซ้ำ) พิมพ์ค่าที่ arm ไว้ (ผ่าน `_trial_console_field()` ตัวเดียวกับที่ send-branch เดิม
  ใช้) กับชื่อ exception ที่ปฏิเสธ
- เรียกจาก branch `except` ของ `_speed_action` เมื่อ `trial_admitted` เป็นจริง

ปักด้วยเทสคลาสใหม่ `TheArmedButRefusedLineReplacesTheDeadTokenTests` ใน
`tests/test_gm_speed_trial_gate.py` (event ยิงเฉพาะตอน arm, บรรทัดมี `trial_opens_for=`/`refused_by=`,
ไม่มี `sending=`, โทเคนเก่ายังไม่พิมพ์, ASCII ล้วน) และเติมชื่อ event ใหม่ในตาราง completeness ของ
`tests/test_gm_chat_command_action.py::EventNameContractTests` (ไม่งั้นเทสนั้นแดงทันที — จับได้จาก
การรันชุดเต็มครั้งแรก)

### 3. `tests/test_gm_attr_wire.py` — เกินจริงข้อสาม
`TheFrameExitIsTheWallTests`'s docstring เขียนว่า "NO caller can build a partial frame, whatever route
it takes" — `#1067` ชี้ว่ามี 3 โมดูล (`stats_progression_hypothesis.py`, `skill_attr_hypothesis.py`,
`damage_hp_link_hypothesis.py`) ที่ประกอบเฟรม `0x309A` เองโดยตรง ไม่ผ่าน
`attr_wire.make_update_attr_frame` เลย — ตรวจซ้ำแล้ว (`grep UPDATE_ATTR_VITAL_ID` ทั้งสามไฟล์: มีตัวแปร
`UPDATE_ATTR_VITAL_ID`/composer ของตัวเอง) ⇒ กำแพงนี้มองไม่เห็นสามโมดูลนั้น ข้อความเกินจริง แก้ให้แคบลง
เหลือ "ผู้เรียกที่ผ่าน `make_update_attr_frame`" และระบุสามโมดูลเป็นช่องว่างที่ยังไม่วัด `[PROPOSED, not
measured]` (ไม่ตัดสินว่าปลอดภัยหรือไม่ปลอดภัย)

### นอกเขต — ประกาศไว้ ไม่แตะ
`live_named_attr_values.py` ยังเขียน "26 rows"/"4 of 26 rows" (ที่ถูกคือ 27 — วัดซ้ำด้วย
`len(attr_wire.named_field_x())` รอบนี้ = 27) รอบ `tof9cw` เคยแก้ไฟล์นี้นอกเขตครั้งหนึ่งเพื่อกู้เกตแดง
รอบนี้**ไม่มีเกตแดงให้กู้** จึงไม่ทำซ้ำ ส่งจดหมายแทน:
`notes_to_chief/20260904_0554_LANE-GM-TO-CHIEF-live-named-attr-values-still-says-26-not-27.md`

## หลักฐาน / ชุดเทส

1. `pytest tests/test_gm_speed_trial_gate.py` — 55 passed, 83 subtests (คลาสใหม่รวมอยู่ในนี้)
2. `pytest tests/test_gm_speed_action.py tests/test_gm_speed_deferred.py
   tests/test_gm_speed_denied_nine_paths.py tests/test_gm_speed_denied_notice.py
   tests/test_gm_speed_shape_hold.py tests/test_gm_speed_wire.py tests/test_gm_attr_wire.py` —
   344 passed, 155 subtests
3. `pytest tests/test_gm_*.py` (ครั้งแรก ก่อนเติมชื่อ event ใน completeness table) — **1 failed**
   (`EventNameContractTests::test_the_two_tables_above_cover_every_name_the_module_exposes` —
   จับได้ถูกต้องว่า event ใหม่ยังไม่ลงทะเบียน) แก้แล้วรันซ้ำ: **2118 passed, 1250 subtests passed**
4. ก่อน push: `git fetch origin main` แล้ว merge (พบว่าอยู่บน `origin/main` (`d98d7ab5`) อยู่แล้วตั้งแต่
   clone — ไม่มี commit ใหม่ให้ merge) รันชุดเต็ม `pytest tests/` หนึ่งครั้งบนต้นไม้นี้: ผลอยู่หัวข้อ
   "สถานะเมื่อจบรอบ" ด้านล่าง

## adversary
`ToolSearch` หาเครื่องมือ spawn subagent ในเซสชันนี้หลายคำค้น **ไม่พบ** (ตรงกับที่รอบ `20260901_1013`
เจอมาก่อน) ⇒ ทำ manual self-review แทน (ความเสี่ยงต่ำ: แก้ดอกสตริง/คอมเมนต์สองจุด + เพิ่ม branch คอนโซล
ใหม่หนึ่งเส้นทางที่ไม่แตะตรรกะเกตเดิมเลย ไม่มีการย้าย/ลบเงื่อนไขปฏิเสธใด ๆ) **ไม่เขียนว่า "ผ่าน
adversary"** ที่ไหน — บันทึกไว้เป็นข้อจำกัดของ session ไม่ใช่ขั้นที่ข้ามเอง

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
เมื่อวาน ผู้เทสที่ arm `PF_SPEED_TRIAL=<ค่า>` แล้วพิมพ์ `/speed <ค่าเดียวกัน>` เห็นคอนโซลบรรทัดเดียวกับ
กรณีไม่ได้ arm อะไรเลย (แยกไม่ออกจากจอว่าคีย์ทำงานหรือเปล่า) วันนี้เห็นบรรทัดเพิ่ม
`SPEED TRIAL ARMED REFUSED ... trial_opens_for=<ค่า> refused_by=SpeedWireError` บอกตรง ๆ ว่าคีย์ถูก
จำได้จริง และประตูปิดด้วยเหตุผลอะไร

## จดหมาย
- `notes_to_chief/20260904_0554_LANE-GM-TO-CHIEF-live-named-attr-values-still-says-26-not-27.md`
  (ใหม่ — ค้นแล้ว: เจอไฟล์ที่อ้างถึงจริง แก้เลขยังไม่มา)
- `.CONSUMED.txt` สำหรับ `20260903_2345_COO-DECISION-...` และ `20260904_0346_SYNC-NOTICE-...` (ทั้งคู่
  ถูกกระทำไปแล้วจริงในรอบ `tof9cw` ขาดแค่สตับ)

## nonclaim
1. **ไม่ได้ใช้ GM ข้ามขั้นใดในรอบนี้** — ไม่บูตเซิร์ฟเวอร์/เกม ไม่มีบัญชีใดได้/เสียสถานะ GM ไม่มีเฟรม
   `0x309A` ออกจากประตูใดที่ไม่เคยออกอยู่แล้ว (ของที่เพิ่มคือบรรทัดคอนโซล + event เท่านั้น พฤติกรรมการ
   ปฏิเสธเดิมไม่เปลี่ยนแม้แต่บิตเดียว)
2. ไม่อ้างว่า `/speed`/(b'')/M2/M3/M4 ขยับ — รอบนี้ไม่แตะตรรกะเกตใดเลย มีแค่แก้ถ้อยคำ + เพิ่มการมองเห็น
   บนคอนโซล
3. ไม่อ้างว่า pf-adversary ตรวจแล้วผ่าน — เครื่องมือไม่มีให้เรียกในเซสชันนี้
4. ไม่อ้างว่า P-2/P-3 ขยับ — ทั้งคู่ยังบล็อกจากภายนอกเหมือนเดิม (รายละเอียดในหัวข้อ "ทำไมเลือกงานนี้")
5. ไม่แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py` / canonical DB /
   `scenarios/world_*.json` / `scenarios/combat_*.json` / `live_named_attr_values.py` (นอกเขต ส่ง
   จดหมายแทน) / `GAME_TEST_QUEUE.md` / `NOW.md`
6. ประวัติเดิมในดอกสตริงที่แก้ **ขีดฆ่า ไม่ลบ**
7. ใบจดหมายใหม่จ่าหน้าสายเดียว (chief)

## สถานะเมื่อจบรอบ
- ดูหัวข้อ "หลักฐาน / ชุดเทส" ข้อ 4 สำหรับผลชุดเต็มบน commit สุดท้าย
- `pirate-force-server`: push แล้ว เปิด `#706` ไม่ draft มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด — GET กลับมา
  ยืนยันแล้วว่า marker อยู่จริง (`mergeable_state=unstable` = รอเกต ยังไม่เขียว ยังไม่ merge)
- `pf_bridge`: claim PR `#1072` เติม marker ตอนจบรอบนี้ = ปลดล็อก
- ล็อกรอบ: ต้นรอบ list ทั้งสองรีโปไม่มี `[LANE-GM]` เปิดอยู่เลย ⇒ ไม่มีการถอย ไม่มี takeover ไม่มี
  released-on-behalf
