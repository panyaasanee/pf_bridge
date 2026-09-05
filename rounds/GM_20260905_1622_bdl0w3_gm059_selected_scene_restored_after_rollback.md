# LANE-GM รอบ `bdl0w3` — `CORE-REQUEST-GM-059` ปิด: ป้ายฉากใน `selected` กลับมาหลัง rollback

- เริ่ม 2026-09-05T16:12+07:00 · เขียน 2026-09-05T16:2x+07:00 (+07:00 ทุกบรรทัด)
- ล็อกรอบ: `[LANE-GM]` open = **ไม่มี** ทั้ง `pirate-force-server` และ `pf_bridge` ตอนต้นรอบ
  ⇒ ตัดกิ่ง claim เอง (ไม่ใช่ takeover) · claim PR = `pf_bridge#1344`
- อ่าน `NOW.md` เป็นไฟล์แรก **ก่อน** อ่านกล่องจดหมายและก่อนแตะโค้ด

## รอบนี้ขยับ NOW ข้อไหน
**ขยับ 1 ข้อ · ไม่ขยับ 1 ข้อ (มีเหตุผลวัดได้)**

1. ✅ **ขยับ: `NOW` บล็อก 14:53 ข้อ (3) — "GM-059 ... งานแรก 14:51 PR จุดคืน `selected` ตก 16:21"**
   ปิดในรอบนี้ · chief คืนเขตให้สายนี้ (`1522`) และสายนี้ลงบรรทัดเองใน `gm/warp_send_watch.py`
   ไม่แตะ `runtime.py` เลย · PR เซิร์ฟเวอร์ = ดูท้ายไฟล์
2. ❌ **ไม่ขยับ: `NOW` "GM-A `/warp <เลขแมพ>`" ข้อ `1347` (เทสปักวาป 126 สด · ตก 17:11)**
   **เพราะ precondition ของใบยังไม่เกิด และวัดแล้ว ไม่ใช่เดา**: `1347` ข้อ 2 เขียนว่า
   "รอบแรกของ GM **หลัง PR นั้นบน main**" -- PR ของ LANE-A (ใบ `1346`) **ยังไม่ขึ้น main
   และยังไม่มี PR เปิดด้วยซ้ำ**
   - วัดบน `origin/main` `77b9fc3` รอบนี้:
     `warp_no_coords_live_target(126)` = `None` · `world_scene_travel.destination(126).
     has_authored_entry` = `False` (`spawn` = `(3050.0, 232.0, 90.0)` มีอยู่แล้ว แต่เกตอยู่ที่
     marker ไม่ใช่ spawn) ⇒ `/warp 126` ยัง **stage** ตามกฎเดิม
   - `list_pull_requests(state=open)` ของ `pirate-force-server` = `#833` (LANE-E) และ `#794`
     (LANE-E) เท่านั้น · ไม่มีใบของ LANE-A
   - 🔴 **ไม่แตะเกตของ `1347` ข้อ 3 ล่วงหน้า** (`chat_command_action.py:167` ชุด 126 ·
     preflight) เพราะ `1347` ผูกไว้ว่า "แก้ใน**รอบเดียวกัน**" กับเทสปัก และเทสปักยังเขียนไม่ได้
     · แก้ตอนนี้ = แก้ตามสมมติฐานว่า A จะลงมาหน้าตาแบบไหน และเสี่ยงพลิกเทสที่ปัก `GT-141` ไว้
     (`ProductionCallShapeTests::test_the_default_argument_call_stages_where_gt141_says_it_does`)
- **ว่างเพราะรอ**: `LANE-A` ใบ `20260905_1346_*` (registry ให้ `warp_no_coords_live_target(126)`
  คืนเป้า) · ตกของ A = 15:51 · ตอนวัด 16:2x ยังไม่มา ⇒ ตกของ GM (17:11) ยังไม่เริ่มนับ

NO_FEATURE_WAITING: RE-263 bounded-negative -- second P-2 route dead, blocker unchanged
(บรรทัดตามแบบที่ `COO 1452` สั่งเติม · ย้อนอ้างรอบ `0dlc07` ที่เขียนเป็นร้อยแก้วแทน · `PANYA 1130`)

TWO_SESSIONS_SAME_SCENE: ~~ไม่เกี่ยว -- รอบนี้ไม่แตะสถานะโลกต่อฉากเลย ป้ายที่คืนคือ
`foundation.selected.position.scene_id` ของ **เซสชันเดียว** (ตำแหน่งตัวละคร = ของบัญชี ลง DB ตาม
`PANYA 1057/1140` ไม่ใช่ roster/มอน/ศพ/ของพื้น) · ไม่มีเฟรมออกจากเซิร์ฟเวอร์เพิ่มแม้แต่ไบต์เดียว~~
🔴 **ขีดฆ่า -- ประโยคนี้ผิด และ `pf-adversary` D5 วัดหักล้างได้** (ห้ามลบประวัติ)
ตัวป้ายยังเป็นของเซสชันเดียวจริง และรอบนี้ยังไม่เขียน roster/มอน/ศพ/ของพื้นจริง **แต่ประโยค
"ไม่มีเฟรมออกเพิ่มแม้แต่ไบต์เดียว" เท็จ**: dispatch ถัดไปหลัง send ล้ม วัดได้ว่า
- **มีตัวแก้**: `WORLD_CENSUS_INITIAL_108` + `REAPPLY_108` (roster ฉาก 1 · 108 ตัว)
- **ไม่มีตัวแก้ (control)**: `WORLD_CENSUS_BG0002_INITIAL_97` + `REAPPLY_97` (roster ฉาก 2 · 97 ตัว)
⇒ ป้ายที่รอบนี้คืน **เป็นตัวตัดสินว่าฉากไหนถูกประกาศ roster ใหม่ทั้งฉาก** = สถานะโลกต่อฉาก และเป็นไบต์จริง
🔴 **การประกาศซ้ำทั้งฉากเองเป็นของเดิม ไม่ใช่ของรอบนี้** — `world_census_sent = False` ถูกตั้งโดย
`_gm_warp_resync_selected_scene` (`runtime.py` · `CORE-REQUEST-GM-045`) ไม่ใช่โดยโค้ดของรอบนี้
สิ่งที่รอบนี้ตัดสินคือ **ฉากไหน** ไม่ใช่ **ประกาศซ้ำหรือไม่** · แต่กติกา delta (`PROCESS_GATES §25(ก)`)
แตะเรื่องนี้ ⇒ **บันทึกเป็นหนี้ที่เปิดเผย ไม่ใช่ "ไม่เกี่ยว"** และเข้า backlog ข้อ 1 ของรอบถัดไป
🔴 **และรอยต่อที่ยังเปิด (D5 ครึ่งที่สอง · วัดว่ามีจริง ผลกระทบยัง PROPOSED)**: `mob_loot_cell.
current_scene` ยังเป็น `Bg0002` ขณะที่ป้ายถูกคืนแล้ว ⇒ ถ้ามีการฆ่ามอนหลังจุดนั้น เฟรมจะประกอบด้วย
scene key คนละตัว · **สายนี้ยังไม่ได้ขับเส้นทางฆ่าจริง** จึงไม่อ้างว่าพัง แต่ไม่ปิดปากเรื่องนี้เช่นกัน

BYTECODE_PURGED: ทั้งรอบรันด้วย `PYTHONDONTWRITEBYTECODE=1` + `python3 -B` · และหลังคืนค่ามิวแทนต์
รัน `find . -name __pycache__ -type d -prune -exec rm -rf {} +` ก่อนชุดเต็ม (`COO 1446`)

## กล่องจดหมาย (ขั้นที่สองของรอบ)
`ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt` ตอนต้นรอบ = **3 ใบ**
- ✅ `1452` COO (RE-263 ตรวจคู่) — **บริโภคแล้ว** · เติมบรรทัด `NO_FEATURE_WAITING:` ข้างบน · stub วางแล้ว
- ✅ `1522` chief (GM-059 คืนเขต) — **บริโภคแล้ว** · ลงมือทั้งใบในรอบนี้ · stub วางแล้ว
- 🔶 `1347` COO (`/warp 126` สด) — **อ่านแล้ว วัด precondition แล้ว แต่ตั้งใจไม่วาง stub**
  งานยังค้างจริง ๆ · ปล่อยใบเปิดไว้เพื่อให้รอบถัดไปเห็นเป็นงานแรก (กติกากล่องจดหมาย ข้อ B)
  ไม่ใช่การมองข้าม -- เหตุผลอยู่ในหัวข้อ "ไม่ขยับ" ข้างบน และในจดหมายรายงาน `16xx`

## งานของรอบ — `CORE-REQUEST-GM-059` (ครึ่งเซิร์ฟเวอร์)

### ข้อบกพร่องที่ปิด (D-2 · วัดแล้ว ไม่ใช่ทฤษฎี)
`/warp <n>` ข้ามฉาก → `persist_warp_scene` เขียนแถวถาวรเป็นฉากปลายทางแล้วคืน `selected` ให้สะอาด →
`runtime.py` `_gm_warp_resync_selected_scene` **relabel** `selected.position.scene_id` เป็นฉากปลายทาง
(ตั้งใจ · `CORE-REQUEST-GM-045` · census ต้องอ่านฉากใหม่) → **send ล้ม** →
`rollback_warp_scene` คืน**แถวถาวร**ถูกต้อง `OUTCOME_ROLLED_BACK` → **ไม่มีใครคืนป้ายใน `selected`**
→ เฟรมเดินถัดไป (`runtime.py:4164`) เขียน `candidate` ที่เอา `scene_id` จาก `selected` แต่เอา x/y/z
จากรายงานไคลเอนต์ ⇒ **แถวถาวรกลับไปเป็นฉากปลายทางที่ไคลเอนต์ไม่เคยไปถึง พร้อมพิกัดจริงของฉากที่ยืนอยู่**
= undo ที่สำเร็จถูกลบล้างเงียบ ๆ ด้วยก้าวเดินหนึ่งก้าว

### สิ่งที่ลง (2 ไฟล์ · เขต `gm/` + เทสของสายนี้เท่านั้น · **ไม่แตะ `runtime.py`**)
- `src/pirateforce_foundation/gm/warp_send_watch.py`
  - `_restore_selected_scene(session, previous)` — คืน **`scene_id` อย่างเดียว** x/y/z/heading ไม่แตะ
    (อินเวิร์สของ relabel เป๊ะ ๆ ไม่มากกว่านั้น) · `dataclasses.replace` สองชั้นแบบเดียวกับที่
    `runtime.py` ใช้ในทิศตรงข้าม · **อ่านกลับหลังเขียน** (setattr ที่กลืนค่าเงียบ ๆ ไม่ raise)
  - เรียก **เฉพาะ** เมื่อ `outcome == OUTCOME_ROLLED_BACK` และ**เฉพาะกิ่ง `usable`** ที่มี
    `record.previous_position` ที่ park ไว้ · กิ่ง fallback
    (`rollback_warp_scene_on_send_failure`) ไม่เรียก เพราะตัวนั้น derive แถวจาก `selected` เอง
    การคืนป้ายจากแถวที่มันเพิ่งเขียนคือวงกลม
  - คำตอบสี่คำเข้า `session.events` ทุกครั้ง: `selected_scene_restored` /
    `_already_there` / `_unreadable` / `_not_restored` — เพราะ rollback สองแบบทิ้งแถวถาวร
    **หน้าตาเหมือนกัน** ต่างกันแค่ในเทรล · `_not_restored` เท่านั้นที่พิมพ์คอนโซล
    `GM_WARP_SELECTED_SCENE_RESTORE_FAILED scene=<n>` (กฎ "ห้ามเงียบ")
  - **NEVER RAISES** ทุกกิ่ง — มันรันอยู่ในเฟรม send ที่ล้มแล้ว ใต้ `send_lock` ตัวเดียวกับ
    `heartbeat_worker` (R348) · คอนโซลตายไม่คิดค่าคำตอบ (`_note` `console_lost_*` แทน)
- `tests/test_gm_warp_send_watch.py`
  - `RestoreSelectedSceneUnitTests` (7 ตัว) — คืนสำเร็จ+พิกัดไม่ขยับ · ป้ายตรงอยู่แล้ว =
    คำตอบคนละคำและวัตถุเดิม (identity) · session ที่อ่านแล้ว raise · `Position` ปลอม ·
    write ที่ถูกกลืนเงียบ (จับได้ด้วย read-back) · `replace` ที่ raise · คอนโซลตาย
  - เขียน **สองบรรทัดที่รอบ `0dlc07` ปักไว้ให้พลิก** เป็นค่าที่ถูก (ไม่ใช่ปล่อยแดง ไม่ใช่ผ่อนเป็น
    `assertIn`) ตามที่ docstring ของคลาสนั้นสั่งไว้เอง + ขีดฆ่าย่อหน้าที่ตอนนี้เท็จ (ห้ามลบประวัติ)

### หลักฐาน
- **มิวแทนต์ รันจริงและฆ่าได้**: ลบการเรียก `_restore_selected_scene` ทิ้งทั้งก้อน →
  `RealDispatchSendFailureTests` แดง **2 ตัว**
  (`test_a_walk_reported_after_the_rollback_does_not_raise_through_dispatch` ที่ `row.scene_id`
  = `2 != 1` · และ `test_a_real_send_failure_after_the_relabel_still_rolls_back_the_row`
  ทั้งทูเพิลในหน่วยความจำและคำในเทรล) · คืนค่าแล้วล้าง `__pycache__` แล้วรันใหม่ = เขียว
  🔴 เส้นทางที่มิวแทนต์นี้เดินคือ **`runtime.dispatch` จริง + SQLite จริง + `/warp` ที่ compose จริง
  + ซ็อกเก็ตที่ `sendall` โยน `ConnectionResetError` จริง** ไม่ใช่การเรียก action ตรง ๆ
  (นั่นคือหนี้ที่รอบ `0dlc07` บันทึกไว้ว่าสายนี้ไม่มีเทสเดินเส้นนี้เลย -- จ่ายไปแล้วรอบ `f5htuc`
  ตอนสร้าง `RealDispatchSendFailureTests` และรอบนี้ใช้มันเป็นที่วัด)
- แคบ: `tests/test_gm_warp_send_watch.py` + `tests/test_gm_source_is_cp874_safe.py`
  = **121 passed, 80 subtests**
- 🔴 **ชุดเต็มรันสองครั้งในรอบนี้ และนี่คือเหตุผล** (กติกาบังคับให้เขียน): ครั้งแรกรันบน commit
  `ae0d5a5` ที่เปิด `#836` · จากนั้น `pf-adversary` คืนผล **NOT APPROVED** พร้อม D1/D2/D3 ระดับ
  ship-blocking ⇒ โค้ดเปลี่ยน ⇒ **ห้าม push สภาพที่ไม่เคยถูกรันเต็ม** จึงต้องรันใหม่ทั้งชุด
  ครั้งที่สองคือชุดที่นับ และเป็น commit สุดท้ายจริง
- **ชุดเต็ม ครั้งที่ 1** (commit `ae0d5a5` · ก่อนผล adversary) บนต้นไม้ที่ merge `77b9fc3` แล้ว
  = **1 failed, 11038 passed, 327 skipped, 20343 subtests passed** (782.60s)
  🔴 **ตัวที่แดงเป็นของเดิม ไม่ใช่ของรอบนี้ และวัดแล้วสามทาง**:
  `tests/test_combat_pose.py::SourcePinTests::test_the_generator_reproduces_the_shipped_tables_
  when_it_can_run` ล้มเพราะ `tools/pf_equip_attack_behavior_extract.py` ไม่มีในโคลน
  · `git check-ignore -v` = `.gitignore:119:/tools/*` ⇒ ไฟล์ไม่เคยถูก ship
  · `git diff --stat origin/main...HEAD` = 2 ไฟล์ ไม่มี `tools/` และไม่มี `combat_pose.py`
  · รายงานไปแล้วโดยสายอื่นสองใบ: LANE-DB `20260905_1450_*SYNC-NOTICE-combat-pose-source-pin-*`
    และ claim ของ LANE-B `pf_bridge#1342` · chief เองก็บันทึกตัวเดียวกันใน body ของ `#833`
- ไบต์ > 127 ในบรรทัดที่ **เพิ่ม**: encode `cp874` ได้ทั้งหมด (0 บรรทัดที่ encode ไม่ได้)
- 🔴 **ADVERSARY_PENDING** — ดูหัวข้อ "adversary" ท้ายไฟล์

### สิ่งที่ **ไม่** ทำตามคำสั่ง หนึ่งจุด (มีจดหมายแย้ง เดินต่อแล้ว ไม่รอ)
`COO 1150` ข้อ 1 / `chief 1522` สั่งลบเทส (หรือคอมเมนต์) `KNOWN_DEFECT` ในคอมมิตเดียวกัน
**ไม่ลบทั้งคู่** เพราะ `test_a_busy_database_leaves_the_row_wrong_and_says_nothing` ปัก
ข้อบกพร่อง **busy-database** ซึ่ง PR นี้ไม่ได้แก้แม้แต่บรรทัดเดียว -- พิสูจน์ได้จากตัวมันเอง:
มัน **ยังเขียว** หลังตัวแก้ลง · ลบตอนนี้ = ลบการวัดของข้อบกพร่องที่ยังมีชีวิตบน main
แก้คอมเมนต์แทน (บอกว่า GM-059 ลงแล้วและไม่ใช่ PR ที่ปลดเทสนี้) ·
จดหมาย `20260905_1622_LANE-GM-ASK-COO-known-defect-test-pins-a-defect-this-pr-does-not-fix.md`
[สมมติของสาย GM - รอ COO ยืนยัน] · COO ยืนตามตัวอักษร = สายนี้ลบให้รอบถัดไปทันที

### `GT-258` (ใบเทสที่ผูกกับงานนี้)
แก้เนื้อใบ: ขีดฆ่าประโยค "จุดแก้อยู่ใน `runtime.py` = เขตของ chief" (เท็จแล้ว) + บันทึกว่าครึ่ง
เซิร์ฟเวอร์ลงแล้ว · 🔴 **เกณฑ์ W6 ไม่แก้แม้แต่ตัวเดียว และใบยังต้องรัน** -- ครึ่งเซิร์ฟเวอร์เป็น
headless ไม่ใช่หลักฐานบนจอ · ถ้าขั้น 5b เกิดแล้ว W6 ยังอ่านฉากปลายทาง = ตัวแก้ไปไม่ถึงเส้นทางจริง

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
เดินต่อหนึ่งก้าวหลัง `/warp` ที่ส่งไม่สำเร็จ แล้วอ่าน `character_positions` ได้ **ฉากก่อนวาป**
แทนที่จะเป็นฉากปลายทางที่ตัวละครไม่เคยไปถึง -- คือขั้น 5b ของ `GT-258` มีโอกาสอ่านว่าผ่านได้จริง
เป็นครั้งแรก (ก่อนหน้านี้ถ้าขั้น 5b เกิด มันต้อง FAIL เสมอโดยโครงสร้าง)

## nonclaim (บังคับทุกรอบของสายนี้)
- **ไม่มีอะไรผ่านจอ** ทั้งรอบไม่มีการบูตไคลเอนต์ ไม่มี capture ไม่มีภาพ
- **ไม่ประกาศว่าไมล์สโตนใดขยับ** M2/M3/M4 ไม่ขยับจากรอบนี้ · GM คือเครื่องมือไปถึงสภาพที่จะเทส
  ไม่ใช่หลักฐานว่าฟีเจอร์ทำงาน
- **ใช้ GM ข้ามขั้นไหน**: รอบนี้ไม่ได้ใช้สถานะ GM ข้ามขั้นใดเลย เพราะไม่มีการรันเกม · เส้นทาง
  `/warp` ที่เทสเดินผ่านใช้การอนุญาต GM จริงทุกครั้ง (`gm_accounts` ไฟล์จริงใน temp dir ของเทสเอง)
  ไม่เคยข้าม · ไม่มีบัญชีใดได้หรือเสียสถานะ GM · ไม่มี `production_allowed` ในเส้นทางนี้
- ครึ่งเซิร์ฟเวอร์ = wire/DB layer เท่านั้น · ชั้น client-observable ยังเป็นของ `GT-258` ที่ยังไม่รัน

## งานสำรอง (3 ข้อ · เริ่มได้ทันทีไม่รอใคร · จากคิวของสายเอง · `PANYA 0904_14:4x` / `COO 0155`)
1. **`scene_label_is_server_guess` ค้าง `True` หลัง rollback** — หลังรอบนี้ ป้ายฉากกลับมาถูกแล้ว
   แต่ธงที่ `_gm_warp_resync_selected_scene` ตั้งไว้ไม่มีใครล้าง ⇒ `client_confirmed_scene`
   ไม่มีวันขยับอีกทั้งเซสชัน · ออกเป็น **ใบวัด headless + CORE-REQUEST ถึง chief** (ธงอยู่ใน
   `runtime.py`) · เริ่มได้ทันที ไม่รอใคร
2. **`/speed` (b'') — บันทึก mask ล็อกอินจริง** (`COO 0545` นิยามใหม่ · `NOW` "ต่อคิวทันที")
   PR ในเขต `gm/attr_wire.py` + CORE-REQUEST หนึ่งใบ · ตัวบล็อกไม่ใช่จุดอ่านของ chief อีกแล้ว
3. **P-3 สารบัญปุ่ม GMUI ทั้ง 3 หน้า** (`COO 0245`) — ทำได้เท่าที่ไม่ต้องเปิด client image:
   ไล่จากสตริง/ตารางที่ commit แล้วใน `pf_bridge/gamedata/` + `external/` แล้วเปิดใบ RE แคบ
   สำหรับปุ่มที่ต้องการ image · ออกเป็นใบ ไม่ใช่รายงานวิจัย

## backlog (อะไรบล็อกอยู่ที่ใคร)
- 🔴 **หนี้ที่ `pf-adversary` เปิดในรอบนี้ = งานของสายนี้เอง รอบถัดไป** (ไม่ใช่ของใครอื่น)
  1. **park ไม่ผูกกับ character id** — `on_game_frame_send_failed` ไม่เทียบ `selected.id` กับตัวละคร
     ที่ park ไว้ · ถ้าเปลี่ยนตัวละครได้บนคอนเนกชันเดียว rollback จะเขียนแถว A ทับ B
     **ยังไม่ได้วัด** (ฮาร์เนสไปไม่ถึง) ⇒ งานแรกคือ **วัดว่าเข้าถึงได้ไหม** ไม่ใช่แก้ทันที
  2. **census ประกาศซ้ำทั้งฉาก** หลัง rollback (D5) — ตัวตั้งอยู่ใน `runtime.py` ของ chief
     สายนี้ตัดสินแค่ "ฉากไหน" ⇒ ใบวัด headless ก่อน แล้วค่อยตัดสินว่าเป็น CORE-REQUEST หรือไม่
  3. **`mob_loot_cell.current_scene` ไม่ตรงกับป้ายหลัง rollback** — วัดว่ามีจริงแล้ว
     ผลกระทบต่อเฟรมตอนฆ่ายัง PROPOSED · ต้องขับเส้นทางฆ่าจริงก่อนจึงจะเรียกว่าข้อบกพร่องได้
- **`1347` `/warp 126` สด** → บล็อกที่ **LANE-A** ใบ `1346` (registry 126 · ตก 15:51 ยังไม่มา)
  · รอบถัดไปของ GM: ตรวจ `warp_no_coords_live_target(126)` บน main เป็นข้อแรก ก่อนอย่างอื่น
- **P-2 สีชื่อมอน** → บล็อกที่ **chief** ยังไม่ตั้งเลข RE ใบที่สอง (สายนี้ร่างส่งตั้งแต่ `0306`
  = 13 ชม. · `SYNC-ALARM 1554` · `COO 1650` ตั้งให้ตก 18:21 = escalation) · ตัวบล็อกเดียวที่เหลือ
  คือ `faction_is_a_fallback_operand_only` (`RE-263` ปิดทางที่สองไปแล้ว)
- **P-3 ปุ่ม GM** → บล็อกที่ **RE runner บนสะพาน** (คลาวด์ไม่มี client image) · ไม่บล็อกรอบ
- **`KNOWN_DEFECT` / rollback เทียบปลายทาง** → รอ COO ตอบใบ `1622` (เดินต่อแล้ว ไม่รอ)

## adversary (`COO 0903_2345` · `Panya 0904_14:1x` / `COO 1428`)
~~🔴 `ADVERSARY_PENDING` — ผลยังไม่คืนตอน push~~ **ผลคืนแล้วเวลา ~17:0x และเป็น NOT APPROVED**
(ครั้งที่ 1 จากโควตา 2 · สั่ง ~16:24 · คืน ~17:0x · ขีดฆ่าไว้เพราะบรรทัดบนคือสภาพจริงตอน push รอบแรก)
🔴 **ตัวแก้ทั้งหมดข้างล่างถูก push ทับ `#836` ใบเดิมก่อนเกตเขียว** (ยังไม่ merge ⇒ ไม่ต้องเปิด PR ใหม่)

### D1 (HIGH · รับ · แก้แล้ว) — ตัวแก้รอบแรก **ใช้ค่าผิดตัว**
`record.previous_position` คือ **แถวถาวรใน DB** (`row_before_warp` อ่าน store) แต่สิ่งที่ resync
เขียนทับคือ **ป้ายในหน่วยความจำ** `foundation.selected.position.scene_id` — คนละค่า และ**แยกจากกันได้จริง**:
`lifecycle.py:311` เขียนแถวถาวรเฉพาะเมื่อ `is_position_persist_allowed(scene_id)` จริง แต่
`FoundationSession.checkpoint` (`session.py:446`) อัปเดต `selected` **ทุกครั้งไม่มีเงื่อนไข**
⇒ ตัวละครที่ยืนในฉาก **17** (`persist_position_allowed=False` ใน registry · GT-106) มีป้าย = 17
แต่แถวถาวร = 1 · ตัวแก้รอบแรกจะคืนเป็น **1 = ฉากที่เซสชันไม่เคยอยู่** แล้วเทรลบอกว่า `restored`
**ตัวแก้**: `ParkedWarpSend` พกฟิลด์ที่สอง `previous_selected_scene_id` อ่านที่ compose time
(จังหวะสุดท้ายที่ป้ายจริงยังอ่านได้ — `persist_warp_scene` คืน `selected` แล้ว และ resync ยังไม่รัน)
· `_restore_selected_scene` รับ **ป้าย** ไม่ใช่แถว · park ที่ไม่มีป้าย = `selected_scene_unknown`
**เขียนอะไรไม่ได้เลย ห้ามเดาจากแถวถาวร** (และปฏิเสธ `bool` ด้วย เพราะ `True == 1`)
**เทสที่ปิด**: `test_the_label_restored_is_the_in_memory_one_not_the_durable_rows` — เดินฉาก 17
ผ่านประตูจริง (`foundation.checkpoint`) แล้ว `/warp 2` ให้ send ล้ม · ยืนยัน
`is_position_persist_allowed(17)` เป็นเท็จในเทสเอง ไม่ใช่สมมติ

### D2 (HIGH · รับ · แก้แล้ว) — คำว่า `already_there` เคย**โกหก**
วัดได้: `/warp 1` จากเซสชันที่ป้าย = 17 → resync relabel 17→1 → ตอบ `selected_scene_already_there`
ซึ่ง docstring ของมันเองแปลว่า "ไม่มีการ relabel" ทั้งที่ `gm_warp_selected_scene_resynced_1`
อยู่ในเทรลเดียวกันสองบรรทัดก่อนหน้า · หายเองเมื่อเทียบกับ **ป้าย** แทนแถว (D1) · เทสคู่:
`test_a_same_scene_warp_from_a_divergent_label_is_not_called_restored`

### D3 (HIGH · test defect · รับ · แก้แล้ว) — เกต `OUTCOME_ROLLED_BACK` ไม่มีอะไรยึด
มิวแทนต์ `if outcome == OUTCOME_ROLLED_BACK:` → `if True:` **รอดทั้งไฟล์ (118 passed)** และไม่ equivalent:
บน rollback ที่ถูกปฏิเสธ มันทิ้งแถวถาวรไว้ที่ฉากปลายทางแต่ดึงป้ายกลับ = สร้างความไม่ตรงกันขึ้นมาเอง
**เทสที่ปิด**: `test_a_refused_rollback_leaves_the_label_where_the_resync_put_it`

### D4 (MEDIUM-HIGH · test defect · รับ · แก้แล้ว) — "asserted, not incidental" ไม่ได้ assert อะไรเลย
fixture เดิมสร้างด้วย `replace(PREVIOUS, scene_id=...)` ⇒ x/y/z ของ treatment กับ control เท่ากัน
การ assert พิกัดจึงเป็น tautology · แก้เป็นพิกัด `WALKED` ที่**เข้าถึงไม่ได้จากอาร์กิวเมนต์**

### D5 (MEDIUM · รับ) — ดูหัวข้อ `TWO_SESSIONS_SAME_SCENE` ข้างบน (ขีดฆ่าและเขียนใหม่แล้ว)

### D6 (LOW · รับ · แก้แล้ว) — `NEVER RAISES` มีบรรทัดที่ไม่มี `try`
`current.scene_id == previous.scene_id` อยู่นอก `try` ทุกก้อน · ห่อแล้ว + เทส `_RaisingSceneId`

### D7 (LOW · รับ · แก้แล้ว) — หมุดบรรทัดค้าง `runtime.py:6827` → **`6887`** (วัดใหม่: `def` อยู่ 6887)

### D8 (LOW · **ไม่รับ · ข้อสรุปของ adversary ผิด ตัวเลขถูก**)
adversary รันในกิ่ง `/tmp` ที่**ไม่มี `pf_bridge` วางข้าง ๆ** จึงได้ `0 failed / 421 skipped` แล้วสรุปว่า
"ไฟล์ที่หายทำให้แดงไม่ได้ ต้องเป็นอย่างอื่น" · **หลักฐานที่หักล้าง**: เทสนั้นมีเดคอเรเตอร์
`@BRIDGE_GAMEDATA.skip_unless_present()` และ `tests/pf_preconditions.py:397-399` นิยาม
`BRIDGE_GAMEDATA` = `SIBLING / "pf_bridge" / "gamedata" / "tables"` ⇒ **มีสะพานข้าง ๆ = รัน · ไม่มี = skip**
โคลนของรอบนี้มี `/home/user/pf_bridge/gamedata` จริง ⇒ เทสรัน แล้วแดงเพราะเครื่องมือที่ถูก gitignore หาย
นี่คือหัวข้อของใบ LANE-DB เป๊ะ ๆ: `*SYNC-NOTICE-combat-pose-source-pin-test-fails-with-pf-bridge-alongside*`
ส่วนต่าง 93/94 ก็คือชุดเทสที่ประตูสะพานบานเดียวกันเปิด/ปิด · **ข้อวินิจฉัยของรอบนี้ยืน**

### ที่ adversary ลองแล้วไม่แตก (บันทึกไว้)
same-scene · `DoubleWarpTests` วาปซ้อน · กิ่ง fallback · ต้นทุนต่อ listener thread (ไม่มี I/O ไม่มีล็อก)
· มิวแทนต์ที่ตายอยู่แล้ว 6 ตัว (read-back · type gate · คำสี่คำ) · ชุดเต็มไม่มี regression

### ที่ยังเปิดอยู่ ไม่ปิดปาก
- **ตัวละครถูกเลือกใหม่ระหว่างวาปกับ send ล้ม** — `on_game_frame_send_failed` ไม่เคยเทียบ `selected.id`
  กับตัวละครที่ park ไว้ และ `park_warp_send` ไม่บันทึก character id · adversary **ไปไม่ถึง** ในฮาร์เนส
  (`_V25_REAL_CREATE_PC` ใช้ id 1 ซ้ำ) ⇒ **ข้อสงสัย ยังไม่ได้วัด** · ถ้าเข้าถึงได้จริง
  `rollback_warp_scene` เขียนแถวตัวละคร A ทับ B อยู่ก่อนแล้ว ตัวแก้นี้แค่ขยายไปถึงป้าย
  **= หนี้ของสายนี้ เข้า backlog รอบถัดไป ไม่ใช่ของรอบนี้ที่จะปิด**
- โควตา adversary: ใช้ไป **1 จาก 2** · ตัวแก้ชุดนี้ยังไม่ผ่าน adversary รอบสอง
  🔴 **ห้ามอ่านไฟล์นี้ว่า "ผ่าน adversary"** — ผ่านคือรอบที่ adversary คืนว่าไม่เจอ ซึ่งยังไม่เกิด

## สถานะ push
- `pf_bridge` claim PR `#1344` — marker เติม **หลัง** push ครบทั้งสองรีโปเท่านั้น (`COO 1229`/`1849`)
- PR เซิร์ฟเวอร์ = **`pirate-force-server#836`** · **push แล้ว รอ merge PR #836** (เปิดแล้ว รอ gate)
  ห้ามอ่านว่าเสร็จ/อยู่บน main · marker `PF-AUTOMERGE: v4` ยืนยันด้วย GET กลับมาแล้วว่าอยู่จริงใน body
  · sha ที่เปิด PR = `ae0d5a5` · `mergeable_state` ตอนเปิด = `unstable` (เกตยังไม่รัน)
- เกต (`PANYA 1158` §22): อ่านผล job `gate` ของ run `pull_request` ≤10 นาทีหลังเปิด
  อ่านไม่ทัน/ยังไม่ตัดสิน = `GATE_UNVERIFIED #836` และรอบถัดไปเปิดด้วยการตรวจ PR นั้นก่อน
