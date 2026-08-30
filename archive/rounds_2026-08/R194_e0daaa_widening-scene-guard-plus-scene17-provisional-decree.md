# R194 (session e0daaa) 2026-08-27 ~15:0x-16:0x (+07:00)

**หัวข้อจริงของรอบนี้ขยายจากที่ตั้งใจไว้แรก**: เริ่มจาก widening-rulings guard + scene17 decree แล้วจดหมาย
ใหม่ที่มาถึงกลางรอบ (`PANYA-DECISION 1510`/`1525`, `LANE-GM CORE-REQUEST-016`) ทำให้ M2 deadline (20:00)
กลายเป็นงานหลักของรอบ ดูหัวข้อ "ทำเพิ่มกลางรอบ" ด้านล่างสำหรับส่วนที่ทำหลังบันทึกแรก

## การ์ดกันรอบซ้อน
`git fetch --all` ทั้งสอง repo — ไม่มี PR `[LANE-E]`/WIP round claim เปิดค้างของ chief เอง (มีแต่ PR ของ
`[LANE-A]`/`[LANE-B]`/`[LANE-GM]` — ไม่ใช่ล็อกของ chief, ไม่แตะ) จับล็อกด้วย empty commit `round claim:
e0daaa` ทั้งสอง repo, เปิด draft PR ทั้งคู่ (`pf_bridge#208`, `pirate-force-server#124`) ตรวจชะตา PR รอบก่อน
(R193): `pf_bridge#203`/`pirate-force-server#121` ทั้งคู่ `merged=true` จริง (ยืนยันด้วย `pull_request_read
(get)` ตาม ADDENDUM v6.2 item G ของ R193 เอง ไม่เชื่อ `list_pull_requests`'s `merged` field) — งาน R193 อยู่บน
main แล้ว ไปต่อได้

`CORE-REQUEST` check: ไม่มีใบใหม่ค้างที่ chief ต่อได้วันนี้ (011/012 บล็อกที่การ decode `GmCommand` จาก
0x51E9 ยังไม่มี, 013 ยังไม่มี call site และไม่ได้ดูละเอียดรอบนี้ — ดู "ค้าง" ด้านล่าง, 014 ครึ่งสองยังบล็อก
RE-096) `WIRED v2` ไม่เปลี่ยน = 9/10 (ไม่มีเลนใหม่ต่อสายรอบนี้ ปรับ scope ของเลนที่ wire แล้วสองเลน)

## ทำ
🎯 **COO-DECISION 2026-08-27T14:41+07:00 (widening-rulings scene gate)**: เพิ่ม
`field_mobs.assert_single_scene_tables()` เรียกจาก `load_roster()` — refuse ทันทีถ้ามีมากกว่าหนึ่ง scene
ในตารางที่โหลดพร้อมกัน (เทียบ `SCENE` string ไม่ใช่ module identity) `tests/
test_field_mobs_single_scene_guard.py` (7 เทส) พิสูจน์กับการชนจริง (bg0001/bg0015 ทับกัน template id
31/34/35/103) `pf-adversary` พบ 5 ข้อ ข้อสำคัญ 2 ข้อ (guard ไม่ครอบ `mob_death.kill()`'s
`WIDENING_RULINGS` check เอง เพราะ `FieldMob` ไม่มีฟิลด์ scene, และ mutation gap ในเทสที่แยก identity
เทียบ string ไม่ได้) — แก้ mutation gap ด้วยเทสใหม่ 1 ตัว, เขียนข้อจำกัดที่เหลือลง docstring ตรง ๆ (ไม่ปิดบัง)
+ ส่ง `CHIEF-STATUS` แจ้ง COO/สาย B ว่า guard ยังไม่ครอบ `kill()` เอง เสนอสองทางเลือกให้เคาะต่อ ไม่บล็อกอะไร
วันนี้ (`bg0015` ยังไม่ถูกเรียกผ่าน `load_roster()` จริง)

🎯🔴 **PANYA-DECISION 2026-08-27T14:45+07:00 (scene17 provisional arrival, M2 deadline วันนี้ 20:00)**:
`scenarios/world_scene_registry_001.json` scene 17 (Bg1001) ใส่ spawn ชั่วคราว `(0,0,0)` ป้าย
`PROVISIONAL-OWNER-DECREE-20260827-1445` (append-only ต่อท้าย `spawn_is_null_because` เดิม ไม่ลบของเก่า)
`world_scene_entry.py`'s `resolve_entry` พิมพ์ token `SCENE_ENTRY scene=<n> xyz=... source=...` ทุกครั้งที่
ใช้พิกัด provisional จริง (ตรวจจากคำนำหน้า provenance ไม่ hardcode เลข scene) ผลตรง: `columbus_quest_
dispatch.resolve_columbus_arrival()` **สำเร็จแล้ว** (เดิม refuse เสมอ) `dispatch_columbus_quest3021`
ยังปฏิเสธเหมือนเดิมแต่เหลือเหตุผลเดียว (`RE-096` vehicle-bind ที่ยังเปิด) — ไม่ใช่การปิด `CORE-REQUEST-014`
เต็ม อัปเดตเทส 3 ไฟล์ให้ตรงพฤติกรรมใหม่ (`test_columbus_quest_dispatch.py`,
`test_columbus_quest_dispatch_wiring.py`) + docstring แก้แบบ append-only ทั้งสองจุดที่เคยบอกว่า refuse
เสมอ พบเอง 1 จุดที่ตัวเองเขียนอ้าง `GT-104` ผิด (เลขซ้ำกับใบ MOB-DEATH) แก้เป็น `GT-106` ก่อน commit
เปิด `GT-106` ใหม่ในคิว (รูปแบบสั้น ≤8KB ตาม PANYA-ORDER 1345 ข้อ 3) ครอบเฉพาะคำถาม client-observable ของ
การวางตำแหน่งที่ scene 17 พร้อม nonclaim บังคับตามคำเจ้าของ `pf-queue-author` ตรวจซ้ำแล้วพบจริงว่าใบแรกที่
เขียนขาดฟิลด์บังคับ (db/server args/steps) **และที่สำคัญกว่า: ยังไม่มีทางเข้าฉาก 17 จริงในบูตเดียวเลย**
(`dispatch_columbus_quest3021` refuse เสมอเพราะ RE-096, `--scene-load-scenario` ไม่มีฉาก 17,
`gm_login_scene` ที่เสนอไว้ยังไม่เขียน) แก้ด้วย addendum เติมด่าน 0 พิเศษ + ฟิลด์ที่ขาดในใบเดียวกัน
(ไม่เปิดใบซ้ำ) เปลี่ยนสถานะจาก "เทสได้เลย" เป็น "PENDING — รอ wiring ทางเข้าจริง" ตรง ๆ

สวีตเต็มหลังทุกแก้ `3419 passed, 327 skipped, 5001 subtests, 0 failed` (17 capstone-import collection
error เดิม ไม่เกี่ยว) เขียว(cloud sanity) `tools/verify_hypothesis_ledger.py`/`verify_functional_coverage.py`
รันแล้วก่อน commit ตามกฎ v6.3 §7 ไม่มี diff (ไม่ได้แตะไฟล์ ledger/pin รอบนี้ แต่ยืนยันตามกฎ)

## ledger drift root cause (v6.3 §18 ข้อ 2)
สืบแล้ว: `HYPOTHESIS_LEDGER.json`/`FUNCTIONAL_COVERAGE.json` pin ด้วย hand-computed SHA ไม่มี generator
CLI (`CANONICAL_CONTENT_SHA256`/`GRADE_SUBSET_SHA256` ต้องรันสคริปต์ในหัวแล้วพิมพ์ hex เอง) — สอง PR แก้
พร้อมกันจึง merge ทับกันได้จริง เขียนคำสั่งตรวจ (`python3 tools/verify_hypothesis_ledger.py` /
`verify_functional_coverage.py`, cloud-sandboxable เต็มที่) เพิ่มลง `AGENTS.md` (pf_bridge) แบบ append-only
ต่อท้ายกฎเดิมของ R193 ยังไม่เขียน generator CLI จริง (งานแยก ยังไม่ทำรอบนี้)

## บริโภคกล่องจดหมาย
stub ย้อนหลัง RE-085/086/087/092/093/094 (PANYA-ORDER 1405 ข้อ 17 — ปิดหัวใบไปแล้วก่อนหน้านี้โดยไม่ stub) +
stub 2 ใบที่บริโภครอบนี้ (`1445_PANYA-DECISION-scene17`, `1441_COO-DECISION-widening-rulings`) รวม 8 ใบ

## ทำเพิ่มกลางรอบ (M2 deadline 20:00)

🎯🔴 **merge conflict จริงที่พบตอน push ครั้งแรก**: `scenarios/world_scene_registry_001.json` — Lane A
(round `kqrlhr`) เติม `ground` block ของ scene 17 (จาก placements.tsv จริง) เข้า main พร้อมกับที่ chief เติม
`spawn` decree ในรอบนี้เอง สองบล็อกนี้ conflict กันตรง ๆ ทาง git (คนละ hunk เดียวกัน) เก็บทั้งสองไว้ (ไม่ทิ้ง
ฝั่งไหน) แต่พบว่ารวมกันตรงๆ ทำให้ **โหลด registry ไม่ขึ้นเลย** (`_spawn()`'s bound-check ปฏิเสธ z=0.0 เพราะ
นอกช่วง ground z ที่วัดจริง [746.04, 1272.74]) แก้ด้วย `PROVISIONAL_SPAWN_PROVENANCE_PREFIX` carve-out ใน
`world_scene_travel._spawn()` (ยกเว้น bound-check เฉพาะ spawn ที่ป้าย decree เท่านั้น) — `pf-adversary` รอบ
สองยังจับได้อีกว่า `_within_ground()` ที่ใช้ตัวชี้วัด "ใกล้ spawn point" กลายเป็นเท็จเมื่อ spawn เป็น decree
ไม่ใช่ค่าที่วัด (แถวที่ห่างจาก ground จริงแต่ใกล้ (0,0,0) จะถูกนับว่า "อยู่บน ground ที่มีหลักฐาน" ทั้งที่ไม่ใช่)
แก้ให้ `_within_ground` คืน False เสมอสำหรับ scene ที่มี decree spawn (บังคับ relocate ไปจุด decree เป๊ะทุกครั้ง)
เทสใหม่ 5 ตัวพิสูจน์ทั้งสองจุด (`test_world_scene_travel.py`, `test_world_scene_entry.py::ProvisionalDecreeTests`)

🎯🔴 **PANYA-DECISION 2026-08-27T15:25+07:00 (M2-NO-VEHICLE)**: `dispatch_columbus_quest3021` ไม่ต้องรอ
vehicle bind อีกต่อไป (`RE-096` ปิดลบไปแล้ว เจ้าของรับสภาพ "เข้าฉาก 17 แบบตัวคนเดิน") — ฟังก์ชันสำเร็จจริงแล้ว
คืน `SceneEntry` แทนที่จะ raise เสมอ `runtime.py`'s `_dispatch_columbus_quest3021` ต่อสาย `legacy.
make_login_teleport(*entry.teleport_fields)` จริง ส่ง `TeleportVital` จริงเป็นครั้งแรกของโปรเจกต์สำหรับ
ตัวละครที่ live อยู่แล้ว (ไม่ใช่แค่ตอน login) headless proof ผ่าน dispatcher จริงเขียว

🔴 **CORE-REQUEST-016 (LANE-GM, เร่งด่วน)**: `runtime.py:4746` (เดิม) ส่ง `GM_UpdateGMStateVital` เวอร์ชัน
`1` แบบไม่มีเงื่อนไข — `GT-101` (attended, OBSERVER_CONFIRMED) วัดจริงว่าเวอร์ชันนี้ **ฆ่าเซสชันเจ้าของไปแล้ว
หนึ่งครั้งจริง** (client ปฏิเสธเฟรมด้วย modal error แล้วปิด socket เอง) เพิ่ม `gm.state_wire.GM_UPDATE_
STATE_VITAL_VERSION_CONFIRMED = None` + gate จุดเรียกใน `runtime.py` ให้ไม่ส่งจนกว่า `RE-105` จะปิด เทสใหม่
พิสูจน์ทั้งสถานะปิด (ไม่ส่ง) และสถานะเปิด (monkeypatch ค่าแล้วต้องส่งจริง) — `gm_accounts.json` ไม่มีบัญชี
commit จริงตอนนี้จึงไม่มีอันตรายทันที แต่บัญชีถัดไปที่เพิ่มก่อน `RE-105` ปิดจะชนบั๊กเดิมทันที ป้องกันไว้แล้ว

🔴 **pf-adversary รอบสอง (M2 no-vehicle) พบ 5 ข้อ แก้ 2 เปิดเผย 3**:
- แก้: token คอนโซลไม่เคยขึ้นจริง (`emit=self.events.append` ไม่ใช่ `print`) — แก้เป็นพิมพ์+บันทึกพร้อมกัน
  ตามแบบ `PLAYER_FACTION` เดิม มีเทส capture stdout จริงยืนยัน
- แก้: comment เก่าใน `runtime.py` ที่บอกว่า dispatch ปฏิเสธเสมอ (ล้าสมัยแล้ว)
- เปิดเผย (ยังไม่แก้ ต้องรอ attended ลองจริง): ① `RE-077` T3 เคยพินว่าไคลเอนต์ต้องอยู่ state `StateRunTime`/
  `StateNavigation` ถึงจะรับ `TeleportVital` — จุดใหม่นี้ยิงทันทีหลังเลือกบทสนทนา ไม่มีใครวัดว่า state ตอนนั้น
  คืออะไร ② ยิงได้แค่ครั้งเดียวต่อ connection ไม่มี retry ถ้าพลาด (เงียบสนิท ไม่มี event) ③ quest-gate-skip
  (ดูข้างล่าง) อาจทำให้ทุกอย่างข้างบนไม่ถูกใช้จริงเลยคืนนี้ ส่ง `CHIEF-STATUS 1600` แจ้งครบ

🔴 **quest-gate-skip (PANYA-DECISION 1510 ①) ทำไม่ได้วันนี้**: ตรวจ static ก่อนเขียนโค้ดพบว่าฟังก์ชันเดียวที่
ไคลเอนต์ใช้เขียน quest flag (`Quest.SetFlag`/`SetQuestFlag`) เป็น **STUB_NOOP บนไคลเอนต์เอง** (พิสูจน์จาก
`PF_GAMEDATA_LUA_API.tsv`) — เขียนโค้ดตอนนี้เท่ากับปั้น wire field ที่ไม่มีหลักฐาน เปิด `RE-106`
(STATIC-ON-BRIDGE) แทน เสนอให้ attended ลองคลิกจริงดูว่าไคลเอนต์ปฏิเสธตัวเลือกเควสเงียบๆหรือปล่อยผ่าน
(`CHIEF-STATUS 1545`) — ทั้งสองผลมีค่า ไม่ใช่ FAIL

**ตัวเลขชนกันที่พบเอง**: `GT-105` ของ chief ชนกับ `RE-105` ที่ LANE-GM เปิดพร้อมกัน (ทั้งคู่กันคนละไฟล์แต่
ใช้เลขเดียวกันเพราะไม่เห็น commit ของกันและกัน) renumber เป็น `GT-106` ก่อน push (แก้ทุกจุดอ้างอิงในทั้งสอง
repo) เช่นเดียวกับที่ Lane B/Lane GM ก็ชนกันเองที่ "CORE-REQUEST-015" (คนละทะเบียน คนละไฟล์ ไม่กระทบไฟล์
เดียวกัน ไม่ต้อง renumber แต่บันทึกไว้ให้ chief เขียน registry รอบหน้าเลือกเลขจบไม่ชน)

**CORE-REQUEST-015 (LANE-GM, login-scene-override) ยังไม่ต่อสายรอบนี้** — อ่านครบแล้ว ตัดสินใจเลื่อนเพราะ
รอบนี้เต็มไปด้วยงาน M2 deadline-critical + งานเร่งด่วน CORE-REQUEST-016 อยู่แล้ว การรวม logic ข้ามสาย A/B
สำหรับจุดต่อที่สอง (census) ต้องคิดรอบคอบ ไม่ใช่บรรทัดเดียว — เลื่อนไปรอบหน้า (ลำดับความสำคัญสูงสุดรองจาก
`lane_hooks`) ระหว่างรอ Lane GM เดินหน้าสร้างโมดูลเองเสร็จแล้ว (`gm/login_scene_override.py`, merge เข้ามา
กลางรอบผ่าน PR#126 ของเขาเอง ไม่ชนกับไฟล์ที่ chief แตะ)

สวีตเต็มหลังทุกแก้ (รวม merge ทั้งสองรอบ) `3448 passed, 327 skipped, 5001 subtests, 0 failed` เขียว
(cloud sanity)

## ค้าง (ตรง ๆ ไม่ปิดบัง)
- 🔴 **`lane_hooks/` skeleton (v6.3 §18 ข้อ 1, สัญญาไว้ตั้งแต่ R193 ว่า "ทำเป็นลำดับแรกก่อนงานอื่น") ยังไม่ทำ
  เป็นรอบที่สองติดต่อกัน** — เหตุผล: M2 deadline วันนี้ 20:00 (`PANYA-CHASE 0915 ①.5`: "priority หนึ่งเหนือ
  ทุกอย่าง") บวก COO-DECISION 1441 ที่กำหนดเส้นตายชัดว่า "รอบถัดไปของ chief ที่ถือ LOCK" (คือรอบนี้) ทำให้
  งานสองเรื่องนี้ต้องมาก่อน ตัดสินใจเดินหน้าอันนี้ก่อนแทนที่จะรีบทำ `lane_hooks` แบบเร่งรัด (สถาปัตยกรรมใหม่
  ต้องผ่าน pf-adversary และคิดเรื่อง auto-discovery ให้รอบคอบ ไม่ใช่บรรทัดเดียว) **สัญญารอบหน้า: ทำเป็น
  ลำดับแรกจริง ๆ ไม่เลื่อนอีก เว้นแต่มีเส้นตายเจ้าของแทรกอีกเหมือนรอบนี้**
- `CORE-REQUEST-013` (world_population_handoff) ยังไม่ได้ดูละเอียดรอบนี้ — ยังเปิดค้าง ไม่แน่ใจว่า RE ที่
  เคยบล็อกยังบล็อกจริงไหม (RE-085/094 ปิดแล้ว, RE-091 ปิดแล้วแต่เป็นคนละเรื่อง) ต้องอ่านใบต้นทางใหม่ก่อน
  ตัดสินใจ ไม่รีบทำแบบไม่แน่ใจ
- `CHIEF_CONTINUATION.md`/`AGENTS.md` ยังไม่ย่อขนาด (v6.3 §17 ข้อ 9 ง/จ) — `AGENTS.md` (pf_bridge) 87KB+
  ยังเกิน 25KB เดิม (R193 ก็เลื่อนไว้เหมือนกัน เหตุผลเดิม: เสี่ยงทำข้อมูลหายถ้าเร่งทำพร้อมงานโค้ดจริง)
- `GT-084`/`GT-084-R2` ยังไม่มีรอบ attended ยืนยัน (เหมือนเดิม)

-> ดูรายละเอียดโค้ดที่ `pirate-force-server` PR ของรอบนี้
