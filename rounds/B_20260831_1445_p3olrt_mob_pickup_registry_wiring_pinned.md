# LANE-B รอบ `p3olrt` -- ปิดช่องว่างเดียวที่เอกสารของ `mob_pickup.py` ยอมรับเองว่ายังไม่ถูก
# พิสูจน์ด้วยเทสที่รันจริง: `mob_pickup_registry`/`mob_pickup_bag_cell`

เปิดรอบ 2026-08-31T14:45+07:00
repo: `pirate-force-server` · `pf_bridge`
สาขา: `claude/tender-goldberg-p3olrt` · `claude/wizardly-gauss-p3olrt`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

🔴 **ไม่มี.** รอบนี้ไม่เพิ่มพฤติกรรมใหม่ให้ผู้เล่น -- ไม่แตะ `runtime.py`/`app.py` ไม่แตะ
`scenarios/`, ไฟล์ที่แก้ทั้งสองเป็นเทสใหม่ + docstring ของโมดูลที่มีอยู่แล้ว บอกตรง ๆ ตามกฎ
lane C ว่าไม่ใช่รอบเกมเพลย์ ก่อนจะเข้ารายละเอียดว่าทำไมรอบนี้ยังนับเป็น "งานจริง" ไม่ใช่รอบ
สถานะเปล่า (กฎห้ามสองรอบสถานะเปล่าติดกัน, ตามที่ผู้สั่งงานเน้นย้ำตอนเปิดรอบ)

## Protocol A -- round-lock recovery check

`list_pull_requests(state=open)` ทั้งสอง repo ตอนเริ่มรอบ: ไม่มี `[LANE-B]` PR เปิดค้าง
(มีแต่ `[LANE-A]`) -- ไม่มีอะไรต้องกู้คืนจาก main

## Protocol B -- mailbox triage

`grep "ADDRESSEE: LANE-B"` + ไล่ทุกไฟล์ `FROM_CHIEF_R*_TO_LANE-B_*.md` ที่ไม่มี
`.CONSUMED.txt`: **ไม่มี** -- ใบล่าสุด (`FROM_CHIEF_R256_TO_LANE-B`) consumed แล้วตั้งแต่รอบก่อน
`RE-098` (ที่คำสั่งงานเก่าเตือนว่าอาจยังค้าง) ก็มี `.CONSUMED.txt` อยู่แล้วใน
`notes_to_chief/consumed/` -- ไม่ต้องทำอะไรซ้ำ ใบ `20260831_1150_LANE-B-ASK-COO` (round-lock
livelock + BUILD-006 deadline) ที่รอบก่อนเขียนไว้ว่า "รอ COO" ตอนนี้มีคำตอบครบทั้งสองข้อแล้ว
(`20260831_1245_COO-DECISION-round-lock-livelock-fix...` และ
`20260831_1246_COO-DECISION-build006-m5-deadline-extended-pending-gt146...`) ทั้งคู่มี
`.CONSUMED.txt` อยู่แล้วเช่นกัน -- mailbox สะอาดสนิทตั้งแต่ก่อนรอบนี้เริ่ม

## ตามรอยของค้างสามข้อที่คำสั่งงานให้เช็ค

1. **death_frames counterpart ของ world-wipe fix** -- อ่าน `runtime.py:4600-4749` (block
   `MOB_DEATH_DYING`/`MOB_DEATH_DEAD`) แล้วพบว่า **มีอยู่แล้วเต็มรูปแบบ**: `recompose_dying`/
   `recompose_dead` เรียก `mob_scene_recompose.recompose_frames` ทั้งคู่, มีบรรทัดคอนโซล
   `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING`/`..._RECOMPOSE` พิมพ์นอก `if`/`try` (เหตุผลเดียว
   กับที่ `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` พิมพ์นอก scope), และ fallback สองทางมี event ชื่อ
   ปลอดภัย (`mob_death_frames_census_compose_skipped_no_population_anchor` /
   `..._refused_<reason>`) -- นี่คือของที่ `CORE-REQUEST-008` (LANE-B) ขอไว้แล้วและ chief ต่อสาย
   ไปแล้วในรอบก่อน ๆ ไม่ใช่หนี้ที่ยังค้าง ไม่มีอะไรต้องทำ
2. **GT-084-R2 headless proof / "พร้อมสำหรับ GT-084-R2"** -- `GAME_TEST_QUEUE.md` มีทั้งบรรทัด
   "พร้อมสำหรับ GT-084-R2" (เขียนไปแล้วตั้งแต่รอบเก่า) และผล RESULT ของทั้ง `GT-084`/`GT-084-R2`
   เอง (attended, ปิดแล้ว ทั้งสองใบมี RESULT tag ที่หัวบรรทัด) -- นี่คืองานที่จบไปหลายวันแล้ว
   (27 ส.ค.) คำสั่งงานที่เปิดรอบนี้อ้างข้อมูลเก่ากว่าที่มันควรจะเป็น เหมือนที่รอบ `o9ei0n`/`p0qia9`
   เคยบันทึกไว้แล้วสำหรับ RE-098/RE-067 -- **ไม่ใช่งานค้างจริง**
3. **CORE-REQUEST สำหรับจุดเสียบ `lane_hooks/lane_b_*.py` ที่ตำแหน่งนี้** -- ไม่มีอยู่ และไม่ควรมี:
   COO-DECISION `20260830_0046` เลือกให้ chief ต่อสาย `mob_scene_recompose`/`mob_drop_presence`
   เป็น **import ตรงใน `runtime.py`** ไม่ใช่ผ่าน `lane_hooks.fire()` เพราะทั้งสองโมดูลต้องส่งไบต์
   กลับ และ `fire()` คืนค่าไม่ได้ (ข้อจำกัดที่ระบุไว้ในเอกสารของแพ็กเกจเอง) -- ยืนยันด้วย
   `grep -n "mob_scene_recompose\." src/pirateforce_foundation/runtime.py` = 9 จุดเรียกตรง
   ไม่มีจุดไหนผ่าน `lane_hooks` เลย **นี่คือเหตุผลที่ไม่มีไฟล์ `lane_hooks/lane_b_*.py` บน main
   ไม่ใช่ของค้าง** -- โมดูลของสาย B ที่ยังไม่มีจุดเสียบ (`mob_pickup_persist.py`,
   `mob_combat_membership.py`) ก็ไม่ใช่ทรง `lane_hooks` เช่นกัน (อย่างแรกรอ opcode จาก `GT-146`,
   อย่างหลังเป็น predicate ธรรมดาที่มี CORE-REQUEST ฝังในตัวมันเองรอ chief แล้ว) -- ปิดคำถามนี้
   อย่างชัดเจน ไม่ใช่แค่ยืนยันซ้ำว่า "ยังไม่มี"

## BUILD-004/5/6 -- reverified, ยังบล็อกเหมือนเดิม

เหมือนสองรอบก่อน: BUILD-004/005 ยังอยู่ ไม่ drift (ผ่านสวีตเทสเต็ม) **BUILD-006 ยังบล็อกจริง**
ที่จุดเดียว -- opcode คลิกเก็บของจาก `GT-146` (attended, `PENDING` หัวคิว) เส้นทางเขียน
(`mob_pickup_persist.py`) และฝั่งอ่านคืนตอน relog (`store.get_backpack`, เรียกจริงใน
`select_and_start`, ยืนยันด้วยการอ่านโค้ด `runtime.py:6452-6453`) ทำและเทสแล้วทั้งคู่ -- ตาม
`COO-DECISION 20260831_1246` ไม่มีเดดไลน์ตายตัวใหม่ ผูกกับผล `GT-146` โดยตรง ไม่เดา opcode เอง

## ของจริงที่สร้างรอบนี้ -- ปิดช่องว่างที่ docstring ของ `mob_pickup.py` เองยอมรับว่ายังไม่พิสูจน์

`mob_pickup.py` NONCLAIM 1 เขียนไว้เองตั้งแต่รอบ `3lzfhw` (26 ส.ค.) ว่า call site ของ
`BagCellRegistry.claim`/`.release` (`runtime.py:6485`/`:1337`) เป็น **"[MEASURED by call-site
reading, NOT by an executed test -- no test in `tests/` references
`mob_pickup_registry`/`mob_pickup_bag_cell`]"** -- ยืนยันซ้ำต้นรอบนี้ด้วย
`grep -rln "mob_pickup_registry\|mob_pickup_bag_cell" tests/` = **0 hit** แม้ call site เอง
จะขึ้น main มาแล้วห้าวัน (`mob_pickup.py` 2018 บรรทัด และ `runtime.py` โดยรวม เป็นสองไฟล์ที่รอบ
`p0qia9` เพิ่งบันทึกไว้ว่า "ได้ความสนใจน้อยหรือไม่ได้แตะ")

ไฟล์ใหม่ `tests/test_mob_pickup_registry_wiring.py` ใช้ harness เดิม (`make_state_class`,
รูปแบบเดียวกับ `_login_and_create`/`_start_game` ของ `test_scene_scoped_combat_wiring.py`) พิสูจน์
ด้วยการ dispatch จริง (login -> create -> StartGame) สี่ข้อ:

1. StartGame claim ทะเบียนให้ character ที่เลือก (`mob_pickup_bag_cell` ไม่ใช่ `None`,
   `mob_pickup_character_id` ตรงกับ character จริง)
2. เซสชันที่สองบน**บัญชีเดียวกัน เลือก character เดียวกัน** ก่อนเซสชันแรกปล่อยคืน (สถานการณ์
   "reconnect ที่ session เก่าไม่ถึง close_connection" ที่ docstring ของ registry เองพูดถึง)
   ถูกปฏิเสธด้วยชื่อจริง (`mob_pickup_claim_refused_bag_already_claimed`, อ่านค่าคงที่จาก
   `mob_pickup.REFUSE_BAG_ALREADY_CLAIMED` ไม่ใช่พิมพ์สตริงเอง) และ `mob_pickup_bag_cell` ของ
   มันเองยังเป็น `None` -- นี่คือข้อเท็จจริงที่การอ่านโค้ดพิสูจน์ไม่ได้แต่เทสรันจริงพิสูจน์ได้: ทะเบียน
   เป็นวัตถุเดียวที่แชร์กันจริงระดับเซิร์ฟเวอร์ ไม่ใช่ภาพลวงตาต่อเซสชัน
3. `close_connection()` ปล่อยคืน -- เซสชันที่สามบนบัญชีเดียวกัน claim character เดิมได้สำเร็จ
4. `close_connection()` ของเซสชันที่ไม่เคย claim สำเร็จ (login อย่างเดียว) ไม่ raise และไม่
   release ซ้ำ (การ์ด `if self.mob_pickup_bag_cell is not None` ที่ `runtime.py:1336`)

แก้ `mob_pickup.py` NONCLAIM 1 คู่กัน: ขีดฆ่าประโยค "NOT by an executed test" เดิม แล้วเขียน
ต่อว่าตอนนี้พิสูจน์แล้วด้วยไฟล์ไหน ไม่ลบ ไม่ย้ายถ้อยคำอื่นในย่อหน้าเดียวกัน (`resolve_claim`/
`place_in_bag`/`BagCell.commit_pickup` ยังไม่มีจุดเรียกจริง -- ยังจริงอยู่ ไม่แตะประโยคนั้น)

**ทำไมถึงนับเป็นงานจริงแม้ผู้เล่นไม่เห็นอะไรเปลี่ยน:** นี่คือ call site เดียวที่ M5 มีอยู่แล้วบน
main วันนี้ (claim ที่ character select, release ที่ teardown) -- ถ้าวันที่ `GT-146` ให้ opcode
มาแล้วมีคนแก้ `BagCellRegistry`/`close_connection` โดยไม่ตั้งใจ ก่อนหน้านี้สวีตเทสทั้งหมด (5704+
ใบ) จะยังเขียวสนิทเพราะไม่มีเทสไหนแตะเส้นทางนี้เลย -- ตอนนี้มี

## ตัวเลขที่วัดได้

```
tests/test_mob_pickup_registry_wiring.py : ใหม่ 4 ใบ ผ่านทั้งหมด
สวีตเต็ม pirate-force-server (pytest tests -q), รันสองครั้ง:
  ครั้งแรก (ก่อนแก้ NONCLAIM ครั้งที่สอง + เปลี่ยน event assertion เป็นค่าคงที่):
    5740 passed, 323 skipped, 10606 subtests passed, 0 failed (143.29s)
  ครั้งที่สอง (หลังแก้): 5740 passed, 323 skipped, 10606 subtests passed,
    0 failed (139.98s) -- ตัวเลขเท่ากันเป๊ะ
git diff --check: silent
```

`current/pf_login_game_server_v141.py`: ไม่แตะเลย (อ่านอย่างเดียว ผ่าน `load_legacy`,
ใช้ harness เดิม -- ไม่มีการเขียนไฟล์นี้ ไม่ต้องเช็ค hash) ไม่แตะ canonical DB, ไม่แตะ capture
corpus

## ยังไม่ได้พิสูจน์

- BUILD-006 การ wire สุดท้าย (`mob_pickup.dispatch_pickup_request` call site) ยังรอ `GT-146`
  (attended, human-at-client เท่านั้น) -- ไม่เปลี่ยนจากรอบก่อน
- `mob_combat_membership.admits()` (RE-157 job 2) ยังไม่มีจุดเรียกใน `runtime.py` -- CORE-REQUEST
  ฝังอยู่ใน docstring ของโมดูลเองแล้ว (รอบ `le2dox`) รอ chief หยิบ ไม่ใช่ของค้างใหม่รอบนี้

## CORE-REQUEST

ไม่มี (ไม่มีอะไรใหม่ให้ chief -- ของเดิมสองข้อข้างบนอยู่ในบันทึกแล้ว)

## เปิดใบให้สาย C

ไม่มี -- รอบนี้ไม่ชนคำถามที่ไม่รู้คำตอบ เป็นการปิดช่องว่างที่รู้คำตอบอยู่แล้ว (สร้างเทสให้ของที่มี
อยู่แล้ว)

## nonclaim

ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`/`scenarios/world_*.json`
ไม่อ้าง milestone เกมเพลย์ใหม่ การแก้ `mob_pickup.py` รอบนี้เป็น **docstring เท่านั้น** (ไม่มี
บรรทัดโค้ดที่ execute เปลี่ยน) ยืนยันด้วย `git diff` -- ทุกบรรทัดที่เปลี่ยนอยู่ใน comment/docstring
block ของ NONCLAIM 1

## pf-adversary

Agent tool (subagent_type `pf-adversary`) ไม่มีอยู่ในชุดเครื่องมือของรอบนี้ -- ไม่สามารถเรียกได้
จริง ทำการทวนแบบ adversarial ด้วยตัวเองแทน (บันทึกในจดหมายถึง chief คู่กับรอบนี้) แทนที่จะข้าม
ขั้นตอนนี้ไปเฉย ๆ

-- LANE-B (COMBAT) รอบ `p3olrt`
