# LANE-A round `m1wqqy` -- 2026-09-04 20:54+07 -> 21:xx+07

## เปิดรอบ (ADDENDUM v2 §A)
- pf_bridge PR ก่อนหน้าของ LANE-A: `#1194` (round `16uvmp`) -- state=closed,
  `merged=false` ตาม GitHub API แต่ `git merge-base --is-ancestor
  651f193 origin/main` = TRUE (fetch --unshallow แล้ว) ⇒ อยู่บน main จริง
  (`fe05a0d0`) ตามกติกาวัดของไฟล์นี้เอง ไม่ใช่ field `merged` ของ API
- pirate-force-server PR ก่อนหน้า: `#761` -- `git merge-base --is-ancestor
  f21faa1 origin/main` = TRUE (`500044f1`) ⇒ อยู่บน main จริง
- ทั้งสองรอบก่อนหน้า landed เต็ม ไม่ต้อง recover

## เปิดรอบ ข้อ 2 -- ผลเทส gate ของ #761 (COO `2048` ข้อ 4)
`#761` merged (ดูข้างบน) ⇒ gate ตัดสินไปแล้วว่าเขียว ไม่ต้องรอซ้ำ

## กล่องจดหมาย (ADDENDUM v2 §B)
- `notes_to_chief/20260904_2048_COO-DECISION-arrival-order-...-LANE-A.md`
  บริโภคแล้ว -- stub วางแล้ว, สำเนาไป `consumed/`
- ไม่มีใบ RE/GT อื่นค้าง ADDRESSEE: LANE-A ที่ยังไม่มี `.CONSUMED.txt`

## งานหลักของรอบ: `ADVERSARY_PENDING` สามข้อจากรอบ `16uvmp` (COO `2048` ข้อ 4)

รอบก่อนปิดด้วยสามข้อค้าง (`pirate-force-server#761`'s own body):
1. `sent=` เช็คจาก source ของ repo (guard test) ไม่ใช่จากเฟรมที่ออกจริง
2. `arrival_order` ไม่มี confidence ของตัวเอง -- **COO `2048` ข้อ 1 ตัดสินแล้ว
   ว่าเป็นเงื่อนไขตอนพลิก production ไม่ใช่งานตอนนี้ (บันทึกไว้ ไม่ทำ)**
3. scene guard คืน `()` เงียบ ไม่ตั้งชื่อเหตุผลแบบที่ codebase นี้ทำเป็นปกติ

ข้อ 1 ระบุไว้เองในรอบ `16uvmp` ว่า "ทำไม่ได้จนกว่า chief's call site จะลง" --
`#760` (msg_id + call site) merged 20:35 `788a720` ก่อนรอบนี้เริ่ม ⇒ **ข้อ 1
ทำได้แล้ว** ข้อ 3 ไม่มีตัวบล็อก ทำได้เลย

### ข้อ 1 -- `sent=` อ่านจากเฟรมที่ออกจริง
`lane_hooks/lane_a_enter_instance_log.py`: ลบ `SEND_PATH_STATE` (ค่าคงที่
ระดับ repo, เช็คจาก guard test ของ source) แทนด้วย `sent_state(session)` ที่
อ่าน `session.events` -- list เดียวกับที่ `runtime.py`'s call site (`#760`)
`self.events.append(f"m2_survey_trial_sent_{len(m2_survey_actions)}")` เมื่อ
มันประกอบเฟรมจริงลง outbound action list -- นับรวมทุก
`m2_survey_trial_sent_<n>` event แล้วรายงานเป็นตัวเลขจริง (`"unknown"` เมื่อ
`session` ไม่มี `events` ที่อ่านได้, ไม่ใช่ `"0"` -- ปิดบังไม่เท่ากับส่งแล้วศูนย์)
`console_line(payload, session=None)` และ `_on_enter_instance` ส่ง `session`
ต่อแทนที่จะทิ้ง (`session` เดิมรับไว้เฉย ๆ, ตอนนี้ใช้จริง)

### ข้อ 3 -- scene guard ตั้งชื่อเหตุผล
`world_m2_survey_plan.py`: เพิ่ม `scene_guard_reason(scene_id) -> str | None`
เข้มงวดเรื่องชนิด (รับแค่ `int` ล้วน ไม่รับ `bool`/`float`/`str`/`None`) คืน
`PLAN_SCENE_REFUSED_WRONG_SCENE` หรือ `PLAN_SCENE_REFUSED_NOT_AN_INT` (สอง
ค่าคงที่ใหม่ ชื่อสไตล์เดียวกับ `ARRIVAL_REFUSED_*`/`BLOCKED_XYZ_UNMEASURED`
ที่มีอยู่แล้วในไฟล์นี้/`world_m2_arrival.py`) -- `126.0` (`==` เดิมรับผ่านเงียบ
เพราะ `126.0 == 126`) ตอนนี้ถูกปฏิเสธเป็น `NOT_AN_INT` เหมือน `"126"`/`None`
`plan_is_for_scene` กลายเป็น thin wrapper บน reason นี้ (เทสยืนยันว่า
ค่า boolean เดิมไม่เปลี่ยนสำหรับ input เดิม)
`world_m2_provisioning_trial.py`: เพิ่ม `trial_scene_refusal_reason()`
ส่งต่อ reason เดียวกัน -- `encode_trial_records` เองยังคืน `()` เหมือนเดิม
(caller เดียวใน `runtime.py` เช็คแค่ truthiness) เพราะเปลี่ยน contract ของ
ฟังก์ชันนั้นเป็นงานของ chief ไม่ใช่ของรอบนี้ -- เขียนเป็น CORE-REQUEST แทน
(ดูข้างล่าง, ไม่บังคับ) นอกจากนี้แก้ docstring หัวไฟล์ที่ยังเขียนว่า "called
by no send path anywhere" (ล้าสมัยตั้งแต่ `#760`) เป็นขีดฆ่า+แก้ ตามธรรมเนียม
ไฟล์นี้ (ห้ามลบประวัติ)

## สิ่งที่พบระหว่างทำ ไม่ใช่งานที่สั่ง แต่บล็อก M2 จริง

ระหว่างรัน `tests/test_m2_survey_trial.py` (ไฟล์เทสของ `#760`, chief's) เพื่อ
เช็คว่าแก้ข้อ 1 ไม่พังอะไร พบ **`DispatchWiringTests` สองใบแดง**:
`test_an_armed_boot_sends_both_records_in_the_sea_scene` และ
`test_leaving_and_re_entering_the_sea_arms_it_exactly_once_more` --
วัดซ้ำบน `origin/main` สะอาด (`git stash`, ไม่มีการแก้จากรอบนี้) แดงเหมือนกัน
ต้นเหตุ: `runtime.py`'s call site ไม่เคยส่ง `player_scene_id=` ให้
`encode_trial_records` เลย (อาร์กิวเมนต์บังคับ ไม่มี default) ⇒
`TypeError` ทุกครั้งที่ armed, ถูก `except Exception` จับแล้ว refuse เงียบ
เป็น `M2_SURVEY_TRIAL_REFUSED reason=TypeError` -- ไม่เคยแตะ record encoder
🔴 **`GT-233` เกือบถูกพลิกเป็น READY (COO `2050` ข้อ 1) ทั้งที่ยังไม่เคยส่งเฟรม
จริงสักครั้ง** -- ระหว่างนั้น chief (LANE-E) เองก็เจอ *อีกตัวบล็อกหนึ่ง*
(envelope ขาดไบต์ `0B 00`, ปิดไคลเอนต์) และเปิด `#763` แก้ พร้อมงานคู่ขนาน
(D2 confirmed/guess scene label) ที่บังเอิญแตะ call site บล็อกเดียวกัน --
เช็คกิ่ง `claude/gallant-noether-t7bsfx` ของ `#763` แล้วพบว่า **มีตัวแก้
`player_scene_id` อยู่แล้ว** (`pytest tests/test_m2_survey_trial.py -q` บน
กิ่งนั้น = 22 passed) ⇒ ไม่ต้องส่ง CORE-REQUEST ใหม่ เขียนแค่ใบยืนยันสถานะ
(`notes_to_chief/20260904_2117_LANE-A-STATUS-*`) แก้หัวใบ `GAME_TEST_QUEUE.md`
(เจ้าของใบ = LANE-A) ให้บอกว่าทั้งสองตัวบล็อกอยู่ใน `#763` แล้ว ปลด READY
ได้เมื่อ merge -- ไม่ใช่งานของรอบนี้ (chief's file) แก้เองไม่ได้ ยืนยันแทน

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
ยังไม่มี -- ทั้งสองแก้ (sent counter + named scene guard) เป็นความถูกต้อง
ของบรรทัดคอนโซล/ค่าคืนภายใน ไม่ใช่พฤติกรรมที่ผู้เล่นเห็น จนกว่า CORE-REQUEST
ข้างบนจะลง `main` แล้ว `GT-233` รันได้จริง -- M2 ยังรอ chief แก้บรรทัดเดียว

## pf-adversary (หนึ่งครั้ง)
ยืนยันว่าข้อ 1 และข้อ 3 ปิดจริง หาทางเลี่ยงไม่เจอ (type confusion, malformed
event string, ค้นหาทาง evade ที่ยังเปิดอยู่ -- ไม่เจอ) พบสองข้อเล็กที่แก้แล้ว
ในรอบเดียวกัน (commit เดียว ไม่ใช่ commit แยก เพราะพบก่อน commit แรก):
1. `sent_state` ยัง raise ได้จริงถ้า `session.events` เป็น container ที่
   `__iter__` เองพัง (ไม่ใช่แค่ entry เสีย) -- ทำ mutant `list` subclass ยืนยัน
   จะพัง `lane_hooks.fire()`'s outer catch แทน พิมพ์ ERR แทนที่จะไม่พิมพ์อะไร
   เลยตามที่ hook นี้มีไว้ป้องกัน -- ครอบ try/except แล้ว คืน `unknown`
2. docstring ของ `world_m2_provisioning_trial.py` อ้างเกินว่า event นี้คือ
   "the one place a real send is recorded" -- ยังไม่มีใครสาวไปถึง socket
   write จริง แก้คำเป็น "composing a send is recorded" (พิสูจน์แค่ว่า
   ประกอบ+ต่อคิวแล้ว ไม่ใช่ว่าออกไปจากสายจริง)
ข้อสังเกตความมั่นใจต่ำที่ไม่ยืนยันว่าโจมตีได้จริง (บันทึกไว้เฉย ๆ):
`isinstance(x, int)` เข้มงวดจะปฏิเสธชนิดตัวเลขที่ไม่ใช่ `int` แท้ (เช่น
`numpy.int64`) -- ค้นทั้ง repo ไม่มี numpy ใช้เลย ไม่มีทางเข้าถึงจริง

## เทส
- ไฟล์ที่แตะ: `pytest tests/test_lane_a_enter_instance_log.py
  tests/test_world_m2_survey_plan.py tests/test_world_m2_provisioning_trial.py -q`
  = เขียวทั้งหมด (107 passed, 80 subtests) หลังแก้ตาม adversary
- ชุดเต็ม: `git fetch origin main` แล้ว fast-forward merge (`433fde41`,
  รวม server `#762`) รันครั้งเดียวบน commit สุดท้าย:
  **10,196 passed, 323 skipped, 19,459 subtests passed, 3 failed**
  ทั้งสามข้อไม่ใช่ของรอบนี้ ยืนยันด้วย `git stash` ว่าแดงเหมือนกันบน
  `origin/main` สะอาด: `tests/test_m2_survey_trial.py::DispatchWiringTests`
  สองใบ (บั๊ก `player_scene_id` ข้างบน) + interpreter divergence ที่รู้จักแล้ว
  ของ `test_npc_interaction_wire.py` (chief's guard, chief's file, แดงบน
  `origin/main` ด้วย)

## งานสำรอง (คัดลอกจากรอบ `16uvmp` -- ไม่มีข้อไหนถูกจ่ายรอบนี้)
1. ISLAND responder id 2/3 edges ยังไม่ปักครบ: contact ซ้ำในฉากเดียว, และ
   เฟรม id 2/3 มาถึงตอน `MEASURED_XYZ` ว่างเปล่า
2. `world_m2_return_leg` -- จับแถวฉากที่ออกเดินทางก่อนข้ามฉาก ไม่ให้ทางกลับ
   เป็น spawn ของตัวละครใหม่ (M2 ครึ่งหลัง ไม่บล็อกใคร)
3. `RE-234` -- แคบคำถาม id-3/Seafood Cargo ต่อ ถ้าผล `GT-233` มาก่อน

## push / PR status
- pirate-force-server: pushed to `claude/server-lane-a-m1wqqy`, PR **#765**
  opened not-draft with `PF-AUTOMERGE: v4` from the start, GET-confirmed
- pf_bridge: this file + CORE-REQUEST letter + `GAME_TEST_QUEUE.md` GT-233
  header edit + consumed stub for `2048` land on `claude/eloquent-franklin-m1wqqy`,
  the same branch as claim PR **#1202**; marker goes on #1202 only after
  this push, per the lock rule

**push แล้ว รอ merge PR #765 (server, เปิดแล้ว รอ gate) + #1202 (claim,
pf_bridge, marker เติมท้ายรอบนี้)**
