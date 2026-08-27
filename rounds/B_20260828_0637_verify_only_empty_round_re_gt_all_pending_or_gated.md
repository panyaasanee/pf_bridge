# round `B_20260828_0637` (`8wya7k`) - lane B - COMBAT -- verify-only, empty round

**opened:** 2026-08-28 06:33 (+07:00) - **closed:** 2026-08-28 06:37 (+07:00)
**branches:** `claude/admiring-galileo-8wya7k` (pirate-force-server) -
`claude/friendly-ride-8wya7k` (pf_bridge)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ไม่มีอะไรต่างเลยรอบนี้ -- ไม่มีการแก้โค้ดใน `src/` ของทั้งสองรีโป
รอบนี้เป็นรอบตรวจสอบล้วน (verify-only) ตามกฎข้อ F เพราะไม่พบงานจริงที่ยัง self-decidable และไม่ถูกบล็อก

## 1 ล็อกต้นรอบ (ตามที่ orchestrator เช็คสดมาให้แล้ว, ไม่ขุดซ้ำ)

PR #276 (pf_bridge) และ #178 (pirate-force-server) รอบก่อน `db07x9` merged=true ทั้งคู่ -- งานอยู่บน main
แล้ว ไม่มี PR `[LANE-B]` เปิดค้าง (มีแค่ `[LANE-A] round grl1o1: WIP` ของสายอื่น) จดหมายสถานะรอบก่อน
(`notes_to_chief/20260828_0452_...`) ยืนยัน addendum v2 ข้อ A/B/G ทั้งหมดจัดการแล้ว จดหมายล่าสุดของ chief
(`FROM_CHIEF_R207_...`) บอกไม่มีอะไรให้เทสรอบนี้เพราะ CORE-REQUEST-021/026 (seed ตัวละครเข้า scene_id=2)
ยังเป็นงานค้างของ chief เอง ไม่ใช่ของสาย B

## 2 สำรวจโจทย์จริง (`rounds/` ล่าสุด, `CLIENT_RE_QUEUE.md`, `GAME_TEST_QUEUE.md`, `CHIEF_CONTINUATION.md`)

- `rounds/B_*` 20 ไฟล์ล่าสุด: รอบก่อนสุด (`db07x9`, 2026-08-28 05:52) ปิด RE-116 (heading provenance,
  bounded-negative, ไม่ต้องแก้ค่า) รอบก่อนหน้านั้น (`2pnu4l`, 04:52) ปิด RE-117 (NPC level wire) -- ทั้งคู่
  บริโภคแล้ว ไม่มีของค้าง
- `CLIENT_RE_QUEUE.md`: ทุกใบ `RE-085`-`RE-119` ปิดหมด (`CLOSED PASS/DONE` หรือ `BOUNDED-NEGATIVE`) ใบเดียว
  ที่ยัง `🟡 OPEN` คือ `RE-115` (MAPWINDOW-SCENE-NPC-LIST-SOURCE-001) -- ตรวจแล้วนี่**ไม่ใช่ของสาย B**:
  หัวข้อคือ client Map Window UI (ปุ่ม M, รายการค้นหาตัวละครในฉาก) ถามว่ามันอ่านจาก census packet ของ
  `world_population.py` (เขตสาย A) หรือตารางฝั่งไคลเอนต์เอง -- ไม่ใช่ combat/mob/loot mechanic และเป็นใบ
  `[STATIC-ON-BRIDGE]` (งานของ RE runner ที่มีอิมเมจไคลเอนต์ ไม่ใช่งาน pf-builder) รอบ GM ก่อนหน้า
  (`42p0wl`) ก็สรุปแบบเดียวกันไว้แล้ว ("ซึ่งเป็นของสาย A")
- `GAME_TEST_QUEUE.md`: ใบที่แตะ combat/mob/loot ทั้งหมดอยู่ในสถานะ `PENDING` รอ attended session
  (`GT-104` widen-death-scope -- ต่อสายครบแล้วตั้งแต่ R193, ไม่บล็อก M4, "งานเสริมหลัง ruling ผ่าน COO"
  หมายถึงรอทดสอบ ไม่ใช่รอโค้ด; `GT-114` diag-multi-object -- ต่อสายครบ R202, nonclaim (12) เขียนไว้ชัดว่า
  D1b ตั้งใจไม่ต่อ ต้องมี CORE-REQUEST ใหม่ (per-session TargetVital-seen tracking ใน `runtime.py`) ถึงจะ
  ต่อได้ -- เป็นเขตของ chief ไม่ใช่ของ `src/` ธรรมดา) ไม่มีใบ combat/mob ใดที่ status เป็น buildable วันนี้
- `CHIEF_CONTINUATION.md` แถว 005-026: CORE-REQUEST ทุกอันของสาย B (005, 007, 010, 015(บล็อก, ไม่เร่ง),
  022, 024) ต่อสายและ merge แล้วหรือ push รอ merge แล้ว แถว 015 (`mob_pickup.dispatch_pickup_request`)
  ยังบล็อกจริงตามเดิม (รอ RE ถอด opcode inbound pickup request เต็ม, RE-082 ปิดไปแล้วแต่ไม่ครบ) ไม่มี RE
  ใหม่มาปลดล็อก

## 3 ตรวจ `src/pirateforce_foundation/` เขตสาย B หา technical debt/TODO

`grep -rn "TODO\|FIXME\|XXX"` บน `mob_*.py`/`field_mobs.py`/`loot_roll.py`/`diag_multi_object*.py`/
`ground_loot*.py` -- **0 hit** ทุกจุดที่เคยเป็น pf-adversary finding ถูกแก้และบันทึกไว้ในคอมเมนต์แล้ว
(ตรวจแล้วว่าเป็นบันทึกประวัติ ไม่ใช่ debt ค้าง) จุดเดียวที่ดูเหมือนงานค้างจริง (`field_mobs.py:332`,
"bg0015's already-committed, still-unwired table") ตรวจแล้วเป็น **การบล็อกเชิงนโยบายที่ตั้งใจ**:
`COO-DECISION 2026-08-26T12:46+07:00` สั่งห้าม import โมดูล `field_mob_tables_bg0015` ที่ไหนใน package
นี้จนกว่า lane A's second travel gate + geometry/reachability check จะผ่าน -- วันนี้ `world_travel_gates`
ยังปิดโดยนโยบาย (`WORLD_TRAVEL_INERT`, ยืนยันจาก log จริงตอนรันเทสรอบนี้: `reason=
walkin_travel_gate_disabled_by_default_owner_20260826`) มี guard test บังคับอยู่แล้ว
(`tests/test_field_mob_tables_bg0015.py`'s AST + literal-string sweep) -- ไม่ใช่ของที่สาย B ต่อได้เองวันนี้

## 4 สรุปตามกฎข้อ F (รอบเปล่า) -- ตรวจครบสี่ทางเลือกก่อนประกาศว่าง

1. **backlog pre-approved**: ไม่มี -- ทุก CORE-REQUEST ของสาย B ต่อสายและ push/merge แล้ว (ดูข้อ 2)
2. **ใบ RE/STATIC ที่ตอบได้จากซอร์สเกี่ยวกับ combat/mob**: ไม่มี -- `RE-115` เปิดอยู่ใบเดียวแต่ไม่ใช่
   เขต/บทบาทของ pf-builder สาย B (ดูข้อ 2)
3. **เขียน/ปรับใบเทสในคิว**: อ่าน `GT-104`/`GT-114` ซ้ำ -- procedure ครบ พร้อมรัน ไม่มีอะไรต้องแก้ ทั้งคู่
   รอ attended runner เท่านั้น
4. **technical debt ที่ pf-adversary เคยชี้**: ไม่มีรายการค้าง (ดูข้อ 3) -- ทุกจุดที่เคยพบถูกแก้และบันทึกแล้ว
   จุดเดียวที่ยังไม่ต่อ (bg0015) เป็นการบล็อกเชิงนโยบายที่มีเอกสาร+guard test ครบอยู่แล้ว ไม่ใช่สิ่งที่รอบนี้
   ควร override

ไม่มีทางไหนมีของจริงให้ทำ -- **ว่างเพราะรอ (a) chief seed ตัวละครเข้า `scene_id=2` (CORE-REQUEST-021/026)
เพื่อให้ `GT-104`/`GT-114`/`GT-106` มีทางเทสจริง, (b) attended session ปิดผล `GT-104`/`GT-114`, (c) RE
ใหม่ถอด opcode inbound pickup request เต็ม (ปลดบล็อกแถว 015), (d) lane A's travel gate + COO ปลดล็อก
`bg0015`**

## 5 ยืนยันสภาพ (verify, ไม่มีโค้ดเปลี่ยน)

`python3 -m unittest tests.test_field_mobs tests.test_mob_death tests.test_mob_combat
tests.test_mob_pickup tests.test_mob_loot tests.test_diag_multi_object_wiring
tests.test_diag_multi_object_config tests.test_diag_multi_object_runtime_wiring
tests.test_mob_combat_cadence_wiring tests.test_bg0002_census_wiring` (`pirate-force-server`, ทุกโมดูล
เขตสาย B): **395 tests, OK** ไม่มี regression (ไม่มีโค้ดเปลี่ยนรอบนี้ ตัวเลขนี้คือ baseline)

## เกณฑ์สองชั้น

wire/DB: ไม่มีของรอบนี้ -- ไม่มีเฟรมใหม่ ไม่มี wire เปลี่ยน
client-observable: ไม่มีของรอบนี้ -- จอผู้เล่นเหมือนเดิมทุกอย่าง

## nonclaim

รอบนี้ verify-only -- ไม่รันเกมจริง ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`/
`scenarios/world_*.json`/`world_population*.py` ไม่มีโค้ดเปลี่ยนในทั้งสองรีโป จึงไม่เรียก `pf-adversary`
(ไม่มี diff ให้รีวิว)

## 6 write zone

`pf_bridge`: `rounds/B_20260828_0637_...md` (ไฟล์นี้), `notes_to_chief/20260828_0637_LANE-B-STATUS-...md`
ไม่แตะไฟล์อื่นเลย `pirate-force-server`: ไม่แตะไฟล์ใดเลยรอบนี้

## CORE-REQUEST

none (บันทึกในข้อ 2/4: D1b ของ `GT-114` ต้องการ per-session TargetVital-seen tracking ใน `runtime.py`
ถ้า chief มีเวลาว่างและอยากปลดบล็อกก่อน RE ใหม่มาถึง แต่นี่ไม่ใช่คำขอเร่งด่วนของรอบนี้ เป็นแค่การชี้ตำแหน่ง
ที่มีอยู่แล้วในคอมเมนต์ `diag_multi_object_wiring.D1B_UNWIRED_REASON`)

## เปิดใบให้สาย C

none -- ไม่พบเบาะแสใหม่ที่ควรเปิดใบ RE ใหม่รอบนี้
