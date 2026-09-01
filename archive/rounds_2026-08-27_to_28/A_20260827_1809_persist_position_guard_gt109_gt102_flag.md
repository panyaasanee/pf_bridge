# รอบ `A_jafskv` - สาย A - WORLD (`pf-builder`)

**เวลา:** 2026-08-27T18:09+07:00
**สาย:** A (WORLD)
**รอบ:** `jafskv`

---

## ① ประโยคบังคับของสาย: ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

> **ยังไม่มีอะไรเปลี่ยนบนจอเกม** — รอบนี้เพิ่มฟิลด์/ฟังก์ชันฝั่งเซิร์ฟเวอร์ (`persist_position_allowed`) ที่
> ป้องกันบั๊กจริงที่ `GT-106` พบ (ตำแหน่งตัวละครถูกบันทึกผิดหลังเดินทางเข้าฉาก 17) **แต่ยังไม่มีใครเรียกใช้ที่จุด
> เขียนจริง** — ต้องรอ chief ต่อสายใน `runtime.py`/`app.py` ก่อน (`CORE-REQUEST-018`) ถึงจะเห็นผลจริง: ตอนนั้น
> ผู้เล่นที่เดินทางผ่าน Columbus เข้าฉาก 17 จะไม่ถูกบันทึกตำแหน่งผิดๆ อีกต่อไป (แถวเดิมจะถูกเก็บไว้แทนการเขียน
> ทับด้วยค่าผิด) ไม่มีโค้ด `pirate-force-server` อื่นถูกแตะ ไม่มี PR ฝั่ง `pf_bridge` ที่เปลี่ยนโค้ดเลย
> (เอกสาร/คิวเท่านั้น)

## ② ต้นรอบ: ตรวจชะตา PR รอบก่อน (ADDENDUM v2 หัวข้อ A)

`pull_request_read(method=get)` (ไม่ใช้ field `merged` ของ `list_pull_requests` ตาม `COO-DECISION
20260827_1646`) ยืนยัน PR ล่าสุดของสาย A ทั้งสอง repo:

- **`pirate-force-server` #131** (`lf7p3z`): `merged=false`, `mergeable_state=dirty`, ไม่มี `merged_at`/
  `merged_by` — ปิดจริงโดยไม่ merge ตามตัวอักษร **แต่ตรวจโค้ดจริงบน `origin/main` (HEAD `4f0140e`) พบว่า
  เนื้อหาที่ PR #131 พยายามกู้คืน (`login_entry_allowed`/`via_login` fail-closed fix) มีอยู่แล้วครบ** — PR
  #130 (รอบ `0z3kjx` เดิม, คนละ PR, base ใหม่กว่า) merge สำเร็จไปก่อนแล้ว (`pull_request_read` ยืนยัน
  `merged=true`, `merged_by=github-actions[bot]`) **ไม่มีอะไรต้อง cherry-pick จริง**
- **`pf_bridge` #215** (`lf7p3z`): `merged=false`, dirty เช่นกัน — เนื้อหาคือ round file/status letter ของ
  รอบ `lf7p3z` เอง (ไม่ใช่โค้ด) หายจริงแต่มีค่าต่ำ (เอกสารของรอบที่งานจริงกลายเป็น redundant) ไม่ cherry-pick

**สรุป**: ไม่มีงานจริงหายจาก `main` ไม่มี PR `[LANE-A]` เปิดค้างทั้งสอง repo (ตรวจซ้ำด้วย `pull_request_read`
เพราะ `list_pull_requests`'s `state` field เคย stale ระหว่างรอบที่แล้ว) → เปิด PR ใหม่ยึดล็อก

## ③ กล่องจดหมาย (ADDENDUM v2 หัวข้อ B)

- `grep "ADDRESSEE: LANE-A"` — ใบเดียว (`20260827_1450_ATTENDED-REPLY-LANE-GM-1936-*`) consume แล้วก่อนรอบนี้
  (มี `.CONSUMED.txt` คู่กันทั้งใน `notes_to_chief/` และ `consumed/`) — ไม่มีอะไรต้องทำเพิ่ม
- **`20260827_1710_GT106-RESULT-M2-Columbus-3021-*.md`** (cc สาย A, ถามตรงถึง "chief/สาย A" ในข้อ ④.3) —
  **พบระหว่างตรวจ backlog รอบนี้ ไม่มีใน grep ADDRESSEE เพราะใช้ฟอร์แมต "cc" ไม่ใช่ "ADDRESSEE:"** — บริโภคแล้ว
  รอบนี้ (ดู ④ ด้านล่าง) วาง `.CONSUMED.txt` คู่กันแล้ว (ต้นฉบับอยู่ที่เดิม + สำเนาไป `consumed/`)

## ④ ของที่สร้างจริงรอบนี้ (`pirate-force-server` — ทั้งรอบมีแค่นี้)

**บั๊กที่แก้**: `GT-106`'s ผล ④.3 — ตัวละครเดินทางผ่าน Columbus เข้าฉาก 17 สำเร็จ (`M2-NO-VEHICLE-OWNER-
20260827-1525` ทำให้ `dispatch_columbus_quest3021` ไม่ refuse ด้วย vehicle-bind อีกต่อไป — ตรวจโค้ดยืนยันเอง:
ค่าคงที่ `VEHICLE_BIND_REFUSED_NO_VEHICLE_ROW` ยังอยู่ในไฟล์แต่ไม่มีจุดเรียกใช้เหลือเลย) แต่หลัง teardown แถว
`character_positions` ถูกเขียนเป็น `scene_id=1` (ผิด) พร้อม XYZ ของฉาก 17 (`x=-149.0, y=-1250.3, z=745.0` —
ผิดที่สำหรับฉาก 1 ด้วย) จดหมายผลถามตรงว่าควร (ก) บันทึกฉาก 17 ตามจริง หรือ (ข) ไม่บันทึกเลย

**สาย A เลือก (ข)** — เหตุผล: ฉาก 17 ถูกตั้ง `login_entry_allowed: false` ไว้แล้วตั้งแต่รอบ `0z3kjx` เพราะ
เหตุผลเดียวกันเป๊ะ (แถวที่ persist `scene_id=17` จะโดน refuse ที่ login ครั้งถัดไป เพราะฉาก 17 ไม่มีทางกลับวัด
ได้จริง — `n_MARKER=0`, `RE-077` เปิดอยู่, `return_ticket=REQUIRED`) เลือก (ก) จะเดินตรงเข้ากับดักที่
`login_entry_allowed=false` ถูกสร้างมากันไว้เอง — ตัวละครจะ **ล็อกตัวเองออกจากเกม** ที่ login ครั้งหน้า แย่กว่า
บั๊กปัจจุบันอีก (ตัดสินเองตามกฎ "เขียนคำถาม แล้วเดินต่อ" — ไม่ใช่กรณี (ก)/(ข)/(ค) ที่ต้องหยุดรอ COO จริง)

**ไฟล์ที่แตะ (3 ไฟล์, ทำตามแพทเทิร์นเดียวกับ `login_entry_allowed`/`ground_bound_waiver` ที่มีอยู่แล้ว)**:

- `scenarios/world_scene_registry_001.json`: ฉาก 17 เพิ่ม `"persist_position_allowed": false` +
  `table_row_differences.persist_position_allowed_because` อ้างอิงจดหมาย `GT-106` ตรงๆ (ไม่ลบของเก่า)
- `src/pirateforce_foundation/world_scene_travel.py`: `SceneDestination.persist_position_allowed: bool =
  True` (ทุกฉากเดิม 1/2/278/997 ไม่เปลี่ยนพฤติกรรม), `DEFAULT_PERSIST_POSITION_ALLOWED = True`, ฟังก์ชันใหม่
  `is_position_persist_allowed(n_id, registry=None) -> bool` — **fail-open เฉพาะฉากที่ไม่อยู่ใน registry
  เลย** (คนละ default จาก `login_entry_allowed`/`spawn_position` โดยตั้งใจ: unknown-scene ที่นี่ไม่ใช่
  untrusted-scene เพราะบั๊กนี้เกิดเฉพาะฉากที่ pin ไว้แล้วเท่านั้น — เหตุผลเต็มอยู่ใน docstring)
- `tests/test_world_scene_travel.py`: เทสใหม่ 5 ตัว (ฉาก 17 คืน False, ฉากอื่นทุกตัวคืน True เมื่อไม่มี field,
  ฉากไม่รู้จักคืน True แบบ fail-open, `n_id` ผิด range ยัง raise, ค่า `persist_position_allowed` ที่ไม่ใช่
  bool โดน refuse)

**ห้ามแตะ `runtime.py`/`app.py` — ตามกฎ** ยังไม่มีใครเรียก `is_position_persist_allowed` ที่จุดเขียนจริง งาน
รอบนี้จบแค่ "ฟังก์ชัน/ฟิลด์พร้อมใช้ + เทสผ่าน" → เปิด `CORE-REQUEST-018` ให้ chief ต่อสาย (ดู ⑥)

**เทส**: `test_world_scene_travel.py` 42/42, `test_world_scene_entry.py`+`test_world_travel_gate.py`
(ไฟล์ที่อ้าง `SceneDestination` โดยตรง) 145/145, full suite `unittest discover` = 3592 เทส, 0 FAIL, 18 error
เดิม (`capstone` import, ไม่เกี่ยวรอบนี้), 212 skipped · cp874-encodability ผ่านทั้ง 3 ไฟล์

## ⑤ ของที่สร้างจริงรอบนี้ (`pf_bridge` — เอกสาร/คิวเท่านั้น)

- **`GAME_TEST_QUEUE.md`**: เปิดใบใหม่ `GT-109 VEHICLE-BIND-WIRE-CAPTURE-001` ต่อท้าย `GT-107` (เลขว่างยืนยัน
  ด้วย grep ทั้งสองไฟล์ + `archive/`, ตรวจซ้ำโดย `pf-adversary` ด้วย `\bGT-109\b|\bRE-109\b` ทั้งเรโป) —
  objective: capture เฟรม `CVehicleVital` จริงทั้งสองทิศทาง เพื่อให้ RE follow-up ต่อได้หลัง `RE-096` ปิด
  bounded-negative เกตด่าน 0 เขียนตรงว่ายังไม่มีทางเข้าใดยิงเฟรมนี้ได้เลยตอนนี้ — `PENDING` ไม่บล็อก M2
  (`pf-adversary` ยืนยันว่าใบนี้ไม่มีข้อผิดพลาดข้อเท็จจริง, เกตด่าน 0 grep ใช้ได้จริง — เติม cross-ref ไปหา
  ผล `GT-106` ตามข้อเสนอ)
- **`CLIENT_RE_QUEUE.md`**: `RE-096` (ใบที่สาย A เปิด+ปิดเอง รอบ `kqrlhr`) — ขีดฆ่าบรรทัด BUILD_IMPACT ที่
  ล้าสมัย (อ้างว่า `VEHICLE_BIND_REFUSED_NO_VEHICLE_ROW` ยังคง refuse) + เติม addendum อ้างอิง
  `M2-NO-VEHICLE-OWNER-20260827-1525` (ผลหลักของใบ T0/T1/T2 ไม่เปลี่ยน)

## ⑥ จดหมายที่เขียนรอบนี้

1. `20260827_1809_LANE-A-CORE-REQUEST-018-wire-persist-position-allowed-gt106-fix.md` — ขอ chief ต่อสาย
   `is_position_persist_allowed()` เข้าจุดเขียน `character_positions` (ดู ④)
2. `20260827_1809_LANE-A-STATUS-functional-coverage-stale-gt102-stale-flags.md` — แจ้ง `docs/
   FUNCTIONAL_COVERAGE.json` (HIGH, นอกเขตเขียนของสาย A) และ `GT-102` (ไม่ใช่ใบของสาย A) ล้าสมัยหลัง
   `M2-NO-VEHICLE-OWNER-20260827-1525` — `pf-adversary` พบว่า `GT-102`'s ขั้น 6 อันตรายกว่าที่คิด (บอกผู้เทสว่า
   กดตอบรับโดยไม่ตั้งใจ "ไม่กระทบใบนี้" ทั้งที่ตอนนี้จะทริกเกอร์ M2 state mutation จริงที่มีบั๊กติดอยู่)
3. `20260827_1710_GT106-RESULT-*.CONSUMED.txt` — บริโภคจดหมายผล `GT-106` (ดู ③)

## ⑦ pf-adversary pass (ก่อนปิดรอบ)

รันสอง agent แยกกัน: (1) ตรวจ `GT-109` + claim เรื่อง `GT-102`/`dispatch_columbus_quest3021` ก่อนเขียนจดหมาย
(2) — ไม่ได้รันรอบสองแยกสำหรับ diff ของ `persist_position_allowed` (ตรวจเองด้วยการอ่าน diff เต็ม + เทียบกับ
แพทเทิร์น `login_entry_allowed` ที่เคยผ่าน `pf-adversary` มาแล้วในรอบก่อน โครงสร้าง/เหตุผล fail-open vs
fail-closed สมเหตุสมผล ไม่มีจุดที่น่าสงสัย)

ผลรอบ (1): `GT-109` ไม่มีข้อผิดพลาดข้อเท็จจริง (ตรวจ 3 grep เกตด่าน 0 ซ้ำเอง, ตรวจเลขใบซ้ำเอง, ตรวจกับผล
`RE-096`/`RE-085` แล้วตรงกัน) — จุดเดียวที่พลาดคือไม่ได้อ้างอิงผล `GT-106` ที่มีอยู่แล้ว (แก้แล้ว) claim เรื่อง
`GT-102` ถูกต้อง (ยืนยันด้วยการอ่านโค้ดเอง) และพบเพิ่มอีก 3 จุดที่ล้าสมัยเหมือนกัน:
1. `docs/FUNCTIONAL_COVERAGE.json` [HIGH] — แจ้งแล้ว (⑥.2)
2. `GT-102`'s ขั้น 6 (ไม่ใช่แค่ P4) [HIGH] — แจ้งแล้ว (⑥.2), รุนแรงกว่าที่ประเมินไว้แรก
3. `CLIENT_RE_QUEUE.md:270` (`RE-096` BUILD_IMPACT) [MEDIUM] — แก้เองแล้ว (⑤)
4. จดหมาย `20260827_1544_LANE-A-STATUS-*` เอง [LOW, self-correcting เพราะเป็นจดหมายสถานะเก่า ไม่ใช่เอกสาร
   อ้างอิง] — ไม่แก้ ปล่อยไว้เป็นบันทึกประวัติศาสตร์ตามธรรมเนียมห้ามลบ

## ⑧ CORE-REQUEST

`CORE-REQUEST-018` (ดู ⑥.1) — ต่อสาย `is_position_persist_allowed()` เข้า `runtime.py`/`app.py`'s จุดเขียน
`character_positions`

## ⑨ เปิดใบให้สาย C

none — `GT-109` เปิดให้ผู้เทส attended ผ่าน `pf-queue-author`, ไม่ใช่ CORE-REQUEST

## ⑩ nonclaims

- **ไม่ได้อ้างว่าบั๊ก `GT-106` ④.3 ถูกซ่อมแล้ว** — ฟังก์ชัน/ฟิลด์พร้อมใช้เท่านั้น ยังไม่มีจุดเรียกจริง (รอ
  `CORE-REQUEST-018`)
- **ไม่ได้ตัดสินคำถามอื่นของ `GT-106` ④** (ปลายทางฉาก 126 vs 17, ตัวเลือกเควส 3205, roster index 1 ยังชื่อ
  Sebastian) — เรื่องคนละเรื่อง ปล่อยให้ chief/COO/สาย GM เคาะแยก
- **ไม่ได้แก้ `GT-102`/`docs/FUNCTIONAL_COVERAGE.json` เอง** — นอกเขต/ไม่ใช่ใบของสาย A แจ้งแทน
- **ไม่ได้อ้างว่า M2/vehicle-bind ปลดล็อกแล้ว** — `GT-109` แค่เปิดคิวรอทางเข้า
- **ไม่ได้เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**
- **ไม่ได้แตะ** `runtime.py` · `app.py` · `current/pf_login_game_server_v141.py` · `columbus_quest_dispatch.py`
  (ไม่เกี่ยวกับบั๊กนี้) ทั้งรอบ

— สาย A · WORLD
