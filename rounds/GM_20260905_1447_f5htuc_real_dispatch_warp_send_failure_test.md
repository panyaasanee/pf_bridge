# LANE-GM round `f5htuc`

Started 2026-09-05T14:47+07:00. Claim PR: `pf_bridge#1330`. PR เซิร์ฟเวอร์: (เปิดตอนจบรอบ).

`TWO_SESSIONS_SAME_SCENE:` **ไม่เกี่ยว** -- รอบนี้แตะเฉพาะไฟล์เทส (`tests/test_gm_warp_send_watch.py`)
ไม่มีโค้ด production ไม่มีคีย์ต่อ session ไม่มีเส้นทางวาดโลกใหม่ทั้งฉาก

## รอบนี้ขยับ NOW ข้อไหน / ถ้าไม่ขยับ เพราะอะไร
**ไม่ขยับ** งานหลักของรอบนี้ตามใบ `1347` (`/warp 126` วาปสด + persist) **ยังทำไม่ได้**: precondition
ของ COO-DECISION `1347` ข้อ 1-2 คือ "รอบแรกของ GM **หลัง** PR ของ LANE-A (ใบ `1346`, ทำให้
`warp_no_coords_live_target(126)` คืนเป้า) ขึ้น main" -- ตรวจแล้วสามครั้งในรอบนี้ (ต้นรอบ, กลางรอบ,
ก่อน push) `scenarios/world_scene_registry_001.json` แถว `n_id=126` ยัง `from_marker: false`,
`evidence_tier: decreed_provisional`, `table_row.n_MARKER: 0` เหมือนเดิมทุกครั้ง -- ไม่มี PR
`[LANE-A]` เรื่อง marker/126 ทั้งเปิดและ merge ในช่วงรอบนี้ (LANE-A รอบ `tz2rgc` เปิด/merge `#829`
จริง แต่เป็นคนละเรื่อง -- world registry ของ mob HP ไม่ใช่ scene 126 marker) ⇒ **ว่างเพราะรอ LANE-A
ใบ `1346`** (เห็นจาก mailbox ว่า LANE-A ยังไม่ส่งจดหมายว่าใบนั้นเสร็จ) รอบถัดไปของสายนี้เปิดด้วยการ
เช็คซ้ำก่อนสิ่งอื่น

ข้อ 3 ของใบ `1347` (RE-263 consumption) **ขยับไปแล้วก่อนรอบนี้** -- รอบ `0dlc07` (13:12, ก่อนใบ
`1347` เขียนเสียอีกที่ 13:47) ปิด `RE-263` เป็น `CLOSED BOUNDED-NEGATIVE` ครบทุกขั้นแล้ว (ดู
`rounds/GM_20260905_1312_0dlc07_*.md` งาน ②) -- ไม่มีอะไรให้ทำเพิ่มในข้อนี้

## ต้นรอบ (ตามลำดับที่บังคับ)
1. `NOW.md` อ่านเป็นไฟล์แรก -- ไม่มีบล็อกใหม่เฉพาะสายนี้นอกจาก `1347` (blocked, ดูข้างบน) และ P-2/P-3
   ที่ยังค้างเหมือนเดิม (ทั้งคู่รอ RE runner บนสะพาน)
2. **ล็อก**: list open ทั้งสองรีโป ต้นรอบ `[LANE-GM]` = **0 ใบ** (`pf_bridge` มี `#1327` LANE-DB,
   `#1319` LANE-A -- ไม่ใช่ของสายนี้ · `pirate-force-server` มี `#794` LANE-E เก่า) ⇒ ถือล็อกได้
   เปิด claim `pf_bridge#1330` (ไม่ draft ไม่มี marker) แล้ว list ซ้ำ: ไม่มี `[LANE-GM]` ใบอื่น ⇒ ถือต่อ
3. **ชะตารอบก่อน (ข้อ A)**: `pirate-force-server#824` (รอบ `0dlc07`) `merged=true` ·
   `pf_bridge#1318` (claim ของรอบเดียวกัน) `merged=true` ⇒ ไม่ต้องกู้อะไร
4. **กล่องจดหมาย**: `ADDRESSEE: LANE-GM` ที่ไม่มี `.CONSUMED.txt` = ใบเดียว (`1347`) -- อ่านแล้ว
   บริโภคเท่าที่ทำได้ตามข้างบน (ข้อ 3 ปิดไปแล้วก่อนรอบนี้, ข้อ 1-2 blocked) ยังไม่วาง `.CONSUMED.txt`
   เพราะยังไม่ได้ทำงานหลักของใบ -- จะวางเมื่อ LANE-A ลง main แล้วสายนี้ทำรอบยืนยันจริง
5. **ป้ายเวลา**: `TZ=Asia/Bangkok date` = 14:47 · `_BRIDGE_HEARTBEAT.txt` ล่าสุด (ตอนตรวจ) 14:36 ⇒
   ห่าง 11 นาที ผ่าน (เช็คซ้ำก่อน push ที่ 15:24 heartbeat, ห่าง 10 นาที ผ่านเช่นกัน)
6. `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` -- มีจริงที่ราก `pf_bridge/`

## งานสำรอง (Panya `1450`/`0155`): เทสที่เดินผ่าน `runtime.dispatch` จริงสำหรับ `/warp` + send ล้ม + เดินหนึ่งก้าว
รายการนี้เป็นข้อ 1 ของ backlog "งานสำรอง" ที่รอบ `0dlc07` ทิ้งไว้เอง (บรรทัดสุดท้ายของไฟล์รอบนั้น):
"สายนี้ไม่มีเทสที่เดินผ่าน `runtime.dispatch` เลย -- เทสทุกตัวใน `test_gm_warp_send_watch.py` เรียก
action ตรง ๆ จึงไม่เคยเห็น relabel" เริ่มได้ทันทีไม่รอใคร ออกเป็นเทสบนเซิร์ฟเวอร์จริง เข้าเกณฑ์ทั้งสี่ข้อ
ของ `0155`

### สิ่งที่พบ (ไม่รู้มาก่อนต้นรอบ ยืนยันด้วยการรันจริง ไม่ใช่อ่านโค้ดเดา)
เพิ่มคลาส `RealDispatchSendFailureTests` ใน `tests/test_gm_warp_send_watch.py` -- คลาสแรกในไฟล์นี้
ที่ส่ง `/warp <scene>` เป็นข้อความแชทจริงผ่าน `state.dispatch(...)` (แทนที่จะเรียก
`chat_command_action._warp_teleport_action_no_coords` ตรง ๆ แบบทุกคลาสก่อนหน้า) สามเทส:

1. `/warp 2` ผ่าน dispatch จริง ทำให้ `_gm_warp_resync_selected_scene` (`runtime.py`,
   CORE-REQUEST-GM-045) รันจริงเป็นครั้งแรกในไฟล์นี้ -- `foundation.selected.position.scene_id`
   เปลี่ยนเป็น 2 ทันที (relabel) ส่วน x/y/z ยังเป็นค่าฉากต้นทาง (ตามดีไซน์ของ resync เอง)
2. ส่ง send failure จริงหลัง relabel (`wrapped.sendall` ที่โยน `ConnectionResetError`,
   construction แบบเดียวกับ `HookupWiringPinTests`): **แถวในดาต้าเบสย้อนกลับถูกต้อง** (อ่าน
   `previous_position` ที่บันทึกไว้ตอน compose ก่อน relabel จะรันด้วยซ้ำ) แต่ **`foundation.selected`
   ในหน่วยความจำยังค้างที่ scene_id=ปลายทาง + x/y/z=ต้นทาง** เพราะ `rollback_warp_scene`'s
   `_restore_selected` คืนค่ากลับเป็นสิ่งที่ `foundation.selected` เป็นอยู่ ณ ตอนเริ่ม rollback (คือ
   ตัวที่ relabel ไปแล้ว) ไม่ใช่ค่าที่ตรงกับแถวที่เพิ่งเขียนกลับ -- pin ไว้เป็นพฤติกรรมปัจจุบัน ไม่อ้างว่าถูก
3. ส่งเฟรม `TargetPos` (เดินหนึ่งก้าว) จริงหลัง rollback: ไม่ throw (ผ่านเกณฑ์ 5b ขั้นต้น) **แต่แถวที่เขียน
   ลงดาต้าเบสจริงคือ (scene_id=ปลายทาง, x/y/z=จากรายงานเดิน)** -- คือสภาพพังตัวเดียวกับที่ adversary
   ของรอบ `0dlc07` ชี้ไว้ใน `GT-258` D2 ("(ฉากปลายทาง, พิกัดใหม่) ไม่ใช่ (ฉากปลายทาง, พิกัดก่อนวาป)")
   ตอนนั้นเป็นข้อสังเกตจาก reasoning รอบนี้คือ**วัดซ้ำผ่านโค้ดจริงเป็นครั้งแรก**และ pin เป็นเทสถาวร

ทั้งสามข้อไม่ใช่การออกแบบของรอบนี้ -- วัดจากต้นไม้จริงก่อนเขียน assertion (ยืนยันด้วยมิวแทนต์สองทิศทาง
ดูหัวข้อ ADVERSARY) `CORE-REQUEST-GM-059` (ใบของสายนี้เอง ส่งไปแล้วรอบก่อน ยังไม่มีคำตอบ) ถามเรื่อง
"คืน `selected` หลัง rollback" ตรงนี้พอดี -- รอบนี้ไม่แก้ `runtime.py`/`gm/warp_scene_persist.py`
(นอกเขตเขียน + คำถามยังไม่มีคำตอบจาก chief) แค่วัดและ pin ห่วงโซ่ที่คำตอบนั้นจะเปลี่ยน

### ADVERSARY (โควตา 2 ครั้ง ใช้ 1 ครั้ง)
`pf-adversary` ตรวจในเวิร์กทรีแยก (`git worktree`) -- รันเทสใหม่เดี่ยว ๆ, ทั้งไฟล์สองทิศทางลำดับ,
คลัสเตอร์ gm/warp/connection 828 ตัวสองทิศทาง, **และชุดเต็มทั้งหมด (10867 passed)** ไม่พบข้อบกพร่อง
MAJOR/MODERATE ตรวจ mutation สองทิศทาง: (1) ปิด `_gm_warp_resync_selected_scene` เป็น no-op ⇒
3 เทสใหม่แดง 7 เทสเดิมเขียว (ยืนยันว่าไม่ใช่ proxy) (2) จำลองคำตอบของ `CORE-REQUEST-GM-059`
(แก้ `rollback_warp_scene` ให้คืน scene_id ต้นทางจริง) ⇒ เทส 2/3 แดงตามที่ดีไซน์ไว้ (ยืนยันว่า pin
พฤติกรรมปัจจุบัน ไม่ใช่ผลลัพธ์ที่ถูกโดยบังเอิญ) ตรวจ citation ทุกอันในจดหมาย/GT-258/CORE-REQUEST-GM-059
กับสำเนา `pf_bridge` จริง -- ตรงตามที่อ้างทั้งหมด
พบ 1 MINOR (ถ้อยคำ "house rule" ที่ไม่มีจริงใน `AGENTS.md`) + 1 คำถามเปิด (อะไรบังคับให้แก้ assertion
พร้อมกับ `CORE-REQUEST-GM-059` แทนที่จะปล่อยแดงหรือคลายทิ้ง) -- **แก้ทั้งคู่ในรอบเดียวกัน**: เปลี่ยนถ้อยคำ
เป็น "established practice" (ยืนยันด้วย `git grep`), เพิ่ม checklist ในเฮดเดอร์คลาส + marker
`CORE-REQUEST-GM-059` บนทั้งสอง assertion message ให้ grep เจอทั้งคู่เวลาคำตอบมา

## เทส
- ระหว่างทำงาน: `tests/test_gm_warp_send_watch.py` (111 passed) +
  `tests/test_gm_chat_command_dispatch_wiring.py` + `tests/test_gm_warp_position_confirmed.py` +
  `tests/test_gm_source_is_cp874_safe.py` = 269 passed, 80 subtests
- **ชุดเต็ม รันสองครั้งรอบนี้ (เหตุผลตามกฎ)**: ครั้งแรกก่อน merge `origin/main` รอบสอง (LANE-A `#828`/
  `#829` เข้า main ระหว่างรอบ) -- ผลนั้นถูกทิ้ง ไม่ใช้เป็นหลักฐานของสิ่งที่ push เพราะต้นไม้เปลี่ยนหลังรัน
  ครั้งที่สอง**บนคอมมิตสุดท้ายจริง หลัง merge `origin/main` ครั้งล่าสุดแล้ว**:
  **1 failed, 11002 passed, 327 skipped, 20333 subtests passed (515 วิ)**
- 🔴 **1 failed ไม่ใช่ของรอบนี้**: `tests/test_combat_pose.py::SourcePinTests::
  test_the_generator_reproduces_the_shipped_tables_when_it_can_run` --
  `FileNotFoundError: tools/pf_equip_attack_behavior_extract.py` ไฟล์ไม่เคย commit (ยืนยันด้วย
  `git log --all` = 0 commit + `.gitignore` ไม่มีบรรทัด allowlist ให้ไฟล์นี้) แดงเหมือนกันบน
  `origin/main` เปล่า (ตรวจก่อนแตะโค้ดใด ๆ) ไม่ใช่เขตเขียนของสายนี้ (`tools/`/`test_combat_pose.py`
  เป็นของ LANE-B) -- ส่งใบพบไปแล้ว (ดูจดหมาย `1534`) ไม่แก้เอง = เขียว(cloud sanity) ยกเว้นตัวนี้
  ที่พิสูจน์แล้วว่าไม่เกี่ยวกับ diff
- ไม่ได้เพิ่มไฟล์เทสใหม่ (แก้ไฟล์เดิม `tests/test_gm_warp_send_watch.py`) ⇒ ไม่เข้าเงื่อนไขซ้อม
  `pytest_subset`/`skip_census`
- ไบต์ >127 ที่รอบนี้เพิ่ม: มีภาษาไทยในคอมเมนต์ที่อ้างข้อความ GT-258/NOW.md ตรง ๆ (cp874-safe,
  `tests/test_gm_source_is_cp874_safe.py` ผ่าน) ไม่มี emoji/อักขระนอก cp874

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
ไม่มีอะไรบนจอ (headless, server-side) -- แต่ chief/COO ตอนนี้มีเทสอัตโนมัติที่วัดพฤติกรรมจริงของห่วงโซ่
"`/warp` ผ่าน dispatch จริง -> send ล้ม -> rollback -> เดินหนึ่งก้าว" แทนการอนุมานจากการอ่านโค้ด และ
เมื่อ `CORE-REQUEST-GM-059` มีคำตอบ จะรู้ทันทีว่าคำตอบนั้นแก้ปัญหาจริงหรือไม่ (สองเทสจะแดงถ้าคำตอบยังไม่
ครอบคลุมเคสนี้ เขียวถ้าครอบคลุม)

## backlog: อะไรบล็อกอยู่ที่ใคร (วัดจาก main รอบนี้)
- **`/warp 126` วาปสด (ใบ `1347`)** -- ยังบล็อกที่ **LANE-A** (ใบ `1346` ยังไม่ขึ้น main -- ตรวจซ้ำ
  สามครั้งในรอบนี้ ยืนยันจากไฟล์ registry ตรง ไม่ใช่จากการเดา) รอบถัดไปเช็คก่อนสิ่งอื่น
- **`CORE-REQUEST-GM-059`** -- ยังไม่มีคำตอบจาก chief (ส่งรอบ `0dlc07`)
- **P-3 ตารางปุ่ม/หน้า/opcode ของ GMUI** -- ติดที่ RE runner บนสะพาน (ใบ `1328`) เหมือนเดิม
- **`tools/pf_equip_attack_behavior_extract.py` gitignored** -- ติดที่ **chief** (ใบ `1534` รอบนี้)
  ไม่บล็อกสายนี้ แต่บล็อกความน่าเชื่อถือของชุดเต็มทุกรอบ

## nonclaim
- **ไม่มีอะไรผ่านจอรอบนี้** ไม่บูตไคลเอนต์เลย · ไม่ประกาศว่าไมล์สโตนใดขยับ · **ไม่มีขั้นตอนใดถูกข้ามด้วย GM**
  (การใช้ `/warp` ในเทสใหม่เป็นเส้นทาง GM auth จริงผ่าน `gm_accounts.json` env override เดียวกับที่
  ทุกคลาสอื่นในไฟล์ใช้ ไม่ใช่ทางลัด) · ไม่มีบัญชีใดได้หรือเสียสถานะ GM
- **บั๊กที่พบ (ข้อ 2-3 ของ "สิ่งที่พบ") ไม่ได้แก้รอบนี้** -- `runtime.py`/`gm/warp_scene_persist.py`
  เป็นไฟล์ของ chief ตามเขตเขียน (`AGENTS.md` §7) และ `CORE-REQUEST-GM-059` ที่ถามเรื่องนี้ยังไม่มี
  คำตอบ -- รอบนี้แค่วัดและ pin ไม่ใช่ตัดสินว่าควรแก้อย่างไร
- ไม่แตะ `runtime.py` / `app.py` / `connection.py` / v141 / canonical DB / เขตสาย A
  (`scenarios/world_*.json`) / เขตสาย B (`scenarios/combat_*.json`) / `.gitignore` / `tools/`

## จบรอบ (ตามลำดับที่บังคับ)
1. push ครบทั้งสองรีโป
2. PR เซิร์ฟเวอร์: ไม่ draft · หัวข้อขึ้นต้น `[LANE-GM]` · `PF-AUTOMERGE: v4` ใน body ตั้งแต่เปิด
   แล้ว GET กลับมายืนยันว่า marker อยู่จริง
3. `pf_bridge`: ไฟล์รอบนี้ + จดหมาย `1534` ลงกิ่ง claim (ลบ `_claim.md`) push
   แล้วแก้ body ของ claim PR `#1330` เติม `PF-AUTOMERGE: v4` = ปลดล็อก แล้ว GET ยืนยันว่า marker อยู่จริง
4. ไม่รอเกต Windows ไม่รอ PR เซิร์ฟเวอร์ merge (ใบ COO `1229`)

**สถานะจริงท้ายรอบ**: **push แล้ว รอ merge PR #831** -- PR เซิร์ฟเวอร์ `pirate-force-server#831`
**เปิดแล้ว รอ gate** (`mergeable_state: unstable` ตอนเปิด · marker `PF-AUTOMERGE: v4` GET กลับมา
ยืนยันแล้วว่าอยู่ใน body จริง) ไฟล์รอบนี้และจดหมายอยู่บนกิ่ง claim `pf_bridge#1330` รอ reaper merge
**ไม่มีอะไรในรอบนี้อยู่บน `main` ตอนเขียนบรรทัดนี้**
