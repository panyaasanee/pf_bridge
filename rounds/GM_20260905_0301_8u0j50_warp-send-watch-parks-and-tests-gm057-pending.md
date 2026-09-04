รหัสรอบ: 8u0j50
เวลาเริ่ม: 2026-09-05T03:01+07:00
เวลาจบ: 2026-09-05T03:12+07:00

## NOW ข้อไหนขยับ

**ไม่ขยับ**. `pf_bridge/NOW.md` (ตรวจล่าสุด COO 02:52) ไม่มีข้อ "รอเครื่องคุณ" หรือหัวข้อ "งานด่วน
ตอนนี้" ข้อไหนเป็นของ LANE-GM รอบนี้ — ตัวบล็อกที่เหลือทั้งหมดเป็นของ chief (`--scene-load-scenario`
บูตไม่ได้บน main head), LANE-A (`MEASURED_SCENE_IDS`), LANE-B (`GT-247` echo ต่อ hit) และ
`GT-146`/`GT-242` (attended, เครื่อง Panya) รายการบันไดไมล์สโตน CHARTER-02 (§13 ของ prompt นี้)
ก็ไม่ขยับ: M2 ยังค้างเกณฑ์เดียวเดิม (ชนเกาะ 2/3 แล้วเห็นหน้ารายงานกัปตันจริงบนจอ) ซึ่งรอ chief
เสียบจุดเรียกที่ `runtime.py:706` (`CORE-REQUEST-GM-056`) ไม่ใช่ของรอบนี้

## ต้นรอบ — ตรวจตามลำดับที่ prompt บังคับ

1. `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **มีจริง** (ยืนยันแล้ว)
2. ล็อกรอบ: `list_pull_requests` state=open ทั้งสองรีโป กรอง `[LANE-GM]` — **ไม่พบใบเปิดค้าง**
   ทั้ง `pirate-force-server` และ `pf_bridge` ⇒ ไม่มีรอบทำงานอยู่ ไม่มีใบผี ไม่ต้อง takeover
3. ตรวจชะตา PR รอบก่อนของตัวเองทั้งสอง repo (ADDENDUM หัวข้อ A): PR ล่าสุดของ `[LANE-GM]`
   - `pirate-force-server#779` — `merged=true` (`67ac2f0c`) ✅ อยู่บน main แล้ว
   - `pf_bridge#1235` — `merged=true` (`20c34af`) ✅ อยู่บน main แล้ว
   ⇒ ไม่มีงานรอบก่อน "หายจาก main" ไม่ต้อง cherry-pick อะไร
4. กล่องจดหมาย: grep `ADDRESSEE: LANE-GM` ที่ไม่มี `.CONSUMED.txt` คู่กัน — **ค้นแล้ว: ไม่เจอ**
   (ศูนย์ใบ ยืนยันสองครั้ง ครั้งแรกต้นรอบ ครั้งที่สองหลัง fetch ล่าสุด 02:56 ก่อนเริ่มเขียน)
5. `notes_to_chief/*CLAIM*` อายุ < 90 นาที ที่แตะหัวข้อเดียวกับที่จะหยิบ — **ค้นแล้ว: ไม่เจอ** (งานนี้
   เป็นใบที่ระบุผู้ทำสายเดียวจาก backlog รอบก่อนของตัวเอง ไม่เข้าเกณฑ์ "มากกว่าหนึ่งสาย" ไม่ต้องจอง)

## หาอันดับงานตาม "งานตามลำดับ (แหล่งจริงอยู่ในไฟล์)"

1. จดหมายจ่าหน้า `ADDRESSEE: LANE-GM` ไม่มี `.CONSUMED.txt` — **ว่าง**
2. CORE-REQUEST / คำตอบ chief อ้างเลข GM-0xx — **`CORE-REQUEST-GM-057`** (ส่งรอบ `hv8ets` 01:21)
   ยังไม่มีคำตอบจาก chief ⇒ ไม่มีผลใหม่ให้บริโภค
3. ใบ GT ในคิวที่ระบุว่าเป็นของสาย GM — ตรวจ `CLIENT_RE_QUEUE.md`: `RE-238`/`RE-222` ยัง
   `[STATIC-ON-BRIDGE]` (ต้องดิสแอสเซมบลีอิมเมจ ทำบนคลาวด์ไม่ได้) `RE-241` ปิดและบริโภคแล้ว
   (`2056`) — ไม่มีของใหม่
4. ไฟล์รอบล่าสุดของตัวเอง `rounds/GM_20260905_0113_hv8ets_...md` หัวข้อ backlog — **มีของ**:
   บรรทัดแรกของ backlog เขียนไว้ตรง ๆ ว่า `gm/warp_send_watch.py` "ติดที่ตัวเอง ยังไม่เริ่ม เขียนได้
   ครบโดยไม่ต้องรอ chief = งานแรกที่ควรหยิบรอบถัดไป" ⇒ **หยิบข้อนี้**

## ทำอะไร

`src/pirateforce_foundation/gm/warp_send_watch.py` (ไฟล์ใหม่, ASCII ล้วน, นับไบต์ >127 = 0) —
cell ต่อคอนเนกชันที่ park เฟรมของ `/warp` ที่เพิ่งเขียนแถวถาวรสำเร็จ (`_persist_warp_scene` คืน
`persisted`) ระหว่างรอยืนยันว่าเฟรมนั้นถึงสายจริง:

- `on_game_frame_sent(session, frame_bytes)` — เคลียร์ **เฉพาะเมื่อไบต์ตรงกับที่ park เป๊ะ**
  (send loop เรียก observer หลังทุกเฟรม ไม่ใช่แค่ของ warp — เทียบไบต์กันไม่ให้เฟรมอื่นที่ส่งสำเร็จ
  ก่อนไปเคลียร์ park ที่ยังไม่ได้รับการยืนยัน)
- `on_game_frame_send_failed(session, frame_bytes, error)` — เรียก
  `rollback_warp_scene_on_send_failure` **โดยไม่ต้องเทียบไบต์เลย** ถ้า cell ยังไม่ว่าง — ตรงตาม
  ประโยคของ `CORE-REQUEST-GM-057` เอง: v141 `break` ทิ้งลิสต์ action ทั้งก้อนตั้งแต่เฟรมแรกที่พัง
  ⇒ ถ้าเฟรมที่พังเป็นเฟรมอื่นที่เข้าคิวก่อน warp เอง เฟรม warp จะไม่มีวันถูกส่งเลย และไบต์ของมันจะ
  ไม่มีทางมาถึงฟังก์ชันนี้ — ข้อเท็จจริงเดียวที่พอใช้ได้คือ "cell ยังไม่ว่างตอนส่งพัง"

เดินสายในเขตตัวเองสองจุด (`src/pirateforce_foundation/gm/chat_command_action.py`, ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py`):

1. `_warp_teleport_action_no_coords` — เรียก `park_warp_send` ทันทีหลัง `_persist_warp_scene`
   คืน `OUTCOME_PERSISTED`
2. `_make_action`'s withhold branch — เคลียร์ park ของ label เดียวกันเมื่อ `verdict.undo` ย้อนแถว
   ไปแล้ว synchronously (audit row เขียนไม่ได้) เพราะเฟรมที่จะยืนยัน/ทำให้ล้มเหลวจะไม่ถูกคิวเลยแล้ว
   (`action = None` บรรทัดเดียวกัน) — กันไม่ให้ send ที่พังภายหลังของคำสั่งอื่นบนคอนเนกชันเดียวกัน
   ไป rollback แถวที่ย้อนไปแล้วซ้ำอีกที · เพิ่ม event สองตัว
   (`EVENT_WARP_SEND_WATCH_NOT_PARKED`, `EVENT_WARP_SEND_WATCH_STALE_PARK_NOT_CLEARED`) และ
   pin เข้าตาราง `EventNameContractTests` ที่มีอยู่แล้วใน `tests/test_gm_chat_command_action.py`

`docs/GM_LANE.md` — เพิ่มหัวข้อรอบ `8u0j50` (ท้ายไฟล์) พร้อมผล ADVERSARY_MANUAL เต็ม

## ค้นแล้ว: เจอ/ไม่เจอ

- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (โค้ดฝั่งเซิร์ฟเวอร์ล้วน
  ไม่พึ่งข้อมูล client ใหม่)
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เหตุผลเดียวกัน)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ** (ยืนยันขั้นแรกของรอบแล้ว)
- `notes_to_chief/*CLAIM*` อายุ < 90 นาที — **ค้นแล้ว: ไม่เจอ**

## pf-adversary — ADVERSARY_MANUAL (ไม่มี Agent tool ในสภาพแวดล้อมนี้)

ใช้เช็คลิสต์ `.claude/agents/pf-adversary.md` ตรวจมือ (รูปเดียวกับ `741zlx`/R342):

- **ข้อ 12 MANDATORY (โทเคนยิงตาม drift)**: `OUTCOME_CLEARED_OWN_FRAME` ยิงเมื่อไบต์ตรงกับที่
  park เป๊ะเท่านั้น ไม่ใช่ "มีอะไรส่งสำเร็จ" ⇒ ผ่าน · ฝั่งล้มเหลวจงใจไม่เทียบไบต์ ไม่ใช่ช่องโหว่ชนิด
  เดียวกันเพราะ "cell ไม่ว่าง" คือข้อเท็จจริงเกี่ยวกับเป้าหมายจริง (มีแถวที่ยังไม่ยืนยัน)
- **ข้อ 2 (เขียวเพราะยังไปไม่ถึง)**: `test_an_earlier_unrelated_frames_failure_still_rolls_back_
  the_parked_warp` ยิงผ่านแถว SQLite จริงและอ่านกลับ ไม่ใช่แค่เช็ค return value
- **ข้อ 7 (cp874/print)**: ไฟล์ใหม่ไม่มี `print`/console call เลย (มอบให้
  `rollback_warp_scene_on_send_failure` ที่มี guard ของมันเองอยู่แล้ว)
- **ข้อ 4 (ไฟล์มีบนเครื่องแต่ git ไม่เห็น)**: จับได้จริงระหว่างพัฒนา — `test_gm_tests_collect_
  without_posix.py::test_every_lane_gm_test_file_is_tracked_by_git` แดงก่อน `git add`
  แก้แล้วก่อนรันชุดเต็ม
- คำถามที่ยังไม่ตอบ: `/warp` สองครั้งรัวติดกันไปฉากเดียวกันก่อนคำสั่งแรกยืนยัน/ล้มเหลว — park
  ตัวที่สองแทนที่ตัวแรก (เจตนา ตามเหตุผลเดียวกับ `record_warp_target`) แต่ยังไม่มีเทสยิงตรง ๆ

## ชุดเทส

- ระหว่างทาง (เฉพาะไฟล์ที่แตะ): `pytest tests/test_gm_warp_send_watch.py` — 24 passed ·
  `pytest tests/test_gm_chat_command_action.py tests/test_gm_warp_scene_rollback.py
  tests/test_gm_warp_scene_persist.py tests/test_gm_warp_target_record.py
  tests/test_gm_chat_warp_way_out.py tests/test_gm_source_is_cp874_safe.py
  tests/test_gm_name_color_gate.py tests/test_gm_p2_color_call_site_tripwire.py
  tests/test_gm_say_gate_lock.py tests/test_gm_force_pos_version_lock.py
  tests/test_gm_command_audit_outcome.py tests/test_gm_queued_confirm_arming.py
  tests/test_gm_login_scene_consume_cause.py` — ทั้งหมดเขียว รวม `pytest tests/test_gm_*.py`
  เต็มกลุ่ม GM — 2419 passed, 1333 subtests passed (ก่อนรวมเข้าชุดเต็ม)
- `git fetch origin main` แล้ว fast-forward กิ่งรอบนี้เข้ากับ main (`f71cb9ae`, สอง PR ใหม่
  `#780` LANE-A / `#781` LANE-E) ก่อนรันชุดเต็ม ตามกติกา
- ชุดเต็ม (`pytest tests/`) รันครั้งเดียวบน commit สุดท้ายจริง หลัง fast-forward เข้า main:
  **10428 passed, 323 skipped, 19597 subtests passed, 0 failed** (447.37s, python 3.11 คลาวด์)
  — ไม่มีการแก้ไขใด ๆ หลังจากนี้ก่อน push
- ไม่มีเหตุต้องรันเต็มเกินหนึ่งครั้งรอบนี้ (ไม่มีผล pf-adversary แบบ agent ที่ต้องรอ เพราะทำ
  ADVERSARY_MANUAL แทน)

## backlog: อะไรบล็อกอยู่ที่ใคร

- **`CORE-REQUEST-GM-057`** (จุดเสียบ `connection.py` หนึ่งบรรทัด) — ติดที่ **chief** (ส่งรอบ
  `hv8ets` 01:21 ยังไม่ตอบ) — เมื่อลง main แล้ว `on_game_frame_sent`/`on_game_frame_send_failed`
  จะถูกเรียกจริงจากซ็อกเก็ตเป็นครั้งแรก ก่อนหน้านั้นสองฟังก์ชันนี้ยังไม่มีคนเรียกนอกไฟล์เทส
- **เทส wiring `runtime.py` ของ GM-056** — ติดที่ **chief** (บรรทัดเดียวที่ `runtime.py:706`)
- **D3/D6 (process-global รั่วข้ามเทส, ติดตั้งซ้ำเงียบ)** จาก adversary รอบ `hv8ets` — ติดที่
  **chief** ต้องเคาะทางเลือกก่อน (ไม่ใช่ของรอบนี้)
- **`lifecycle.py:121` การอ่านทะเบียนครั้งที่สาม** — ยังไม่มีเจ้าของใบ ไม่ด่วน
- **P-2 สีชื่อมอน** — ติดที่ **chief** (RE ใบที่สองรอเลขตั้งแต่ `0306` เกิน 24 ชม.แล้ว — SYNC-ALARM
  `1554` ยังไม่เห็นเลขใหม่ใน NOW ล่าสุด)
- **P-3 ปุ่ม GMUI** — ติดที่ **RE runner บนสะพาน** (ใบ `1328`) คลาวด์เปิด client image ไม่ได้
- **`/warp` สองครั้งรัวติดกัน** (คำถามที่ ADVERSARY_MANUAL ทิ้งไว้ข้างบน) — ติดที่ตัวเอง ยังไม่เริ่ม
  ไม่ด่วน (ความเสี่ยงต่ำตามที่ให้เหตุผลไว้)

**ว่างเพราะรอใคร**: รอบนี้ **ไม่ว่าง** — หยิบงานที่บันทึกไว้แล้วจากรอบก่อนของตัวเอง

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ยังไม่มีอะไรเปลี่ยนบนจอรอบนี้ และจะไม่มีจนกว่า chief จะเสียบบรรทัดที่ `connection.py`
(`CORE-REQUEST-GM-057`) — รอบนี้สร้าง**ครึ่งที่สองของประตูความปลอดภัย**สำหรับ `/warp` ให้เสร็จสมบูรณ์
ฝั่งนี้ ไม่ได้ต่อสาย สิ่งที่ผู้เทสจะได้เมื่อสายต่อครบ (ทั้ง GM-056 และ GM-057) คือ: วาร์ปข้ามฉากที่เขียน
แถวถาวรสำเร็จแล้วแต่ซ็อกเก็ตหลุดก่อนเฟรมจะออกจริง (สายหลุดกลางคัน, socket reset) จะไม่ทิ้งตัวละคร
ไว้ในฉากที่ไคลเอนต์ไม่เคยถูกส่งไป — แถวจะถูกย้อนกลับไปที่เดิมโดยอัตโนมัติแทนที่จะต้องรอ login รอบหน้า
มาแก้ (ก่อนรอบ `741zlx`/`hv8ets`/`8u0j50` ไม่มีกลไกนี้เลยแม้แต่ครึ่งเดียว)

## nonclaim

- **ไม่มีอะไรในรอบนี้ผ่านจอ** · ไม่มีบัญชีใดได้/เสียสถานะ GM · ไม่มีขั้นตอนใดถูกข้ามด้วย GM
- ไม่ได้แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py` / canonical DB /
  เขตสาย A (`scenarios/world_*.json`) / เขตสาย B (`scenarios/combat_*.json`)
- **`on_game_frame_sent`/`on_game_frame_send_failed` ยังไม่ถูกเรียกจากที่ไหนจริงนอกไฟล์เทสกับจุด
  park ของ `chat_command_action.py` เอง** — รอ `CORE-REQUEST-GM-057` ลง main ก่อน
- หน้าต่าง D8 ข้อ 2 (rollback ตอนส่งพัง) ยังเปิดอยู่จนกว่าบรรทัดของ chief จะลง main
- ไม่ได้อ้างว่า P-2/P-3 ขยับ

## จบรอบ

1. **push ครบทั้งสองรีโปแล้ว**
   - `pirate-force-server` กิ่ง `claude/beautiful-sagan-8u0j50` — `gm/warp_send_watch.py` ·
     `tests/test_gm_warp_send_watch.py` · แก้ `gm/chat_command_action.py` ·
     `tests/test_gm_chat_command_action.py` (ตารางชื่ออีเวนต์) · `docs/GM_LANE.md`
     (ทั้งหมดอยู่ในเขตสายนี้)
   - `pf_bridge` กิ่ง `claude/serene-bell-8u0j50` — ไฟล์รอบนี้ + จดหมายหนึ่งใบ (ไฟล์ `_claim.md`
     ถูกลบบนกิ่งแล้ว ไฟล์รอบนี้แทนที่)
2. **`pirate-force-server#784`** — เปิดไม่ draft · `PF-AUTOMERGE: v4` ใส่ตั้งแต่เปิด แล้ว GET
   ยืนยันว่า marker อยู่จริง (`https://github.com/panyaasanee/pirate-force-server/pull/784`)
3. **`pf_bridge#1245`** (claim PR ของรอบนี้) — เติม `PF-AUTOMERGE: v4` เป็นขั้นสุดท้าย = **ปลดล็อก**
   แล้ว GET ยืนยัน (ทำหลังไฟล์นี้ push)
4. **ชุดเต็ม ครั้งเดียว = ผลที่นับ** บน commit สุดท้ายจริงหลัง fast-forward เข้า main:
   **10428 passed, 323 skipped, 19597 subtests passed, 0 failed** (447.37s)
5. **push แล้ว รอ merge PR #784** · สถานะ: **เปิดแล้ว รอ gate** (`mergeable_state: unstable` ตอน
   เปิด = เช็คยังไม่จบ) — ไม่รอ gate ไม่รอ merge ตามกติกาจบรอบ (`COO 1229`)

-- LANE-GM รอบ `8u0j50`
