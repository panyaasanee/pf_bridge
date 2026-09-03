# LANE-A round `4lrspn`

2026-08-30T22:2x+07:00 - 2026-08-30T23:0x+07:00 (+07:00 via `TZ=Asia/Bangkok date`).

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็นอะไรต่างบนจอ - แต่ตอนนี้คอนโซลบอกตรง ๆ ทุกครั้งที่มี
คนขึ้นเรือ Columbus ไม่ใช่แค่ว่า "เมืองทั้งเมืองตามออกทะเลไปด้วย" (บรรทัดของรอบ `czoo9t`) แต่ยังบอก
ด้วยว่า **ถ้าวันหนึ่งมีทางกลับจริง ตอนกลับมา Port Royal จะต้องคืนคนกี่คน** (115 คน สำมะโนเต็ม)
โดยยังไม่ได้ประกอบไบต์จริง เพราะยังไม่มีทางกลับให้ประกอบไปทำไม (`RE-077` ครึ่งขากลับยังเปิด)

## 0. บริบทก่อนเริ่ม (Section A/B ของ addendum) - อ่านจาก orchestrator แล้ว ไม่ทำซ้ำ

Orchestrating session ทำ Section A (round `czoo9t` อยู่บน main จริงที่ `10a302d`, ตรวจแล้ว) และ
Section B (mailbox) ให้ก่อนเริ่มรอบนี้แล้ว - re-verify เร็ว ๆ ด้วย `grep -rl "ADDRESSEE: LANE-A"`
ตามที่สั่ง ไม่พบใบใหม่ที่ต้องบริโภคเพิ่มจากที่ orchestrator สรุปไว้

## 1. การสำรวจ M2 backlog ก่อนเลือกงาน

อ่าน `rounds/A_20260830_2148_czoo9t.md`, `world_m2_crossing_handoff.py`,
`world_m2_return_leg.py`, `world_m2_sea_destination.py`, `world_population_handoff.py`
และจดหมาย/COO-DECISION ที่เกี่ยวกับฉาก 17/126 ทั้งชุดที่ยังไม่ consumed ก่อนเลือกงาน พบว่า:

* M2 ขาไปครบวงจรแล้ว: dispatch -> arrival -> stowaways report -> return-leg position report ->
  crossing-handoff population report ทั้งหมดต่อกับ `runtime.py` ผ่าน CORE-REQUEST เดิมแล้ว
* งานที่ค้างจริงมีสองทาง: (ก) แถวทะเบียนฉาก 126 - ตอนนั้นยังติดที่ PR #332 gate แดง (20 เทสของสาย GM)
  รอ fixture fix ของสาย GM ก่อน ไม่ใช่ของสาย A แก้ได้ (ข) ไม่มีใครถามว่า "ขากลับ" เป็นหนี้ population
  อะไรบ้าง - `world_m2_return_leg.py` รายงานแค่ตำแหน่ง (position ticket) ไม่เคยพูดถึงคนเลย ทั้งที่
  `world_m2_crossing_handoff.py` ปิดคำถามฝั่งขาไปไปแล้วตั้งแต่รอบ `czoo9t`
* เลือก (ข) เพราะเป็นรูที่วัดได้จริง เล็ก ไม่ต้องพึ่ง identity ประกอบ/ทดสอบแยกได้แบบเดียวกับ
  `world_m2_crossing_handoff.py`เอง และ**ต่อกับ call site ที่ `columbus_quest_dispatch.py` เรียกอยู่แล้ว
  ทุกบูต ไม่ต้องขอ CORE-REQUEST ใหม่เลย**

## 2. งานที่สร้าง

### 2.1 `world_m2_return_leg.py` - ฟังก์ชันใหม่สองตัว

`return_population_owed(entry, *, departed=None, registry=None)` และ
`return_population_console_line(...)` - รูปแบบเดียวกับ `return_leg`/`return_leg_console_line`
ข้างบนในไฟล์เดียวกันทุกประการ (raise ได้ในฟังก์ชัน report, ไม่ raise เด็ดขาดในฟังก์ชัน console)

**ตัวเลือกที่ตั้งใจไม่ทำ และเหตุผล**: ฟังก์ชันนี้**ไม่เรียก**
`world_population_handoff.handoff_on_crossing` (ตัวที่ `world_m2_crossing_handoff.py` เรียกฝั่งขาไป)
เพราะฉากบ้าน (HOME_SCENE_ID) แม็ปกับ `CENSUS_SOURCE` ซึ่งเป็นแขนง CENSUS เต็ม (สำมะโน 115 คน) ไม่ใช่
CLEAR 27 ไบต์แบบฉาก 17 - `world_m2_crossing_handoff.py`เองเตือนไว้แล้วว่า "a scene with a roster
would build the whole roster per crossing for one console line" และไม่มี dispatch จริงที่ส่งใครกลับบ้าน
เลยวันนี้ (`RE-077` ขากลับยังเปิด) การประกอบสำมะโนเต็มทุกครั้งที่ออกเรือ เพื่อพิมพ์บรรทัดเดียวบรรยาย
ทริปที่ยังไปไม่ถึง จะเป็นการจ่ายต้นทุนที่ไฟล์ข้างบนเตือนไว้พอดี บนเส้นทางที่รันทุกวัน (ขาออก) แทนที่
จะเป็นเส้นทางที่ยังไม่มีจริง (ขากลับ) - จึงอ่านแค่สองตัวเลือก (selector) ที่ตัดสินใจ "รูปร่าง" อยู่แล้ว
โดยไม่ต้องสร้างมันขึ้นจริง: `world_scene_travel.population_source` (dict lookup) และ
`world_population.census_count_for_dispatch` (นับ ไม่ใช่ประกอบไบต์)

### 2.2 `columbus_quest_dispatch.py` - หนึ่ง emit ใหม่ ไม่มีการแตะ `runtime.py`

เพิ่ม `emit(world_m2_return_leg.return_population_console_line(...))` ต่อจาก
`WORLD_M2_RETURN_LEG` และก่อน `WORLD_M2_CROSSING_HANDOFF` ในบูตปกติ - call site เดิมของ
`dispatch_columbus_quest3021` ที่ `runtime.py` เรียกอยู่แล้วทุกบูตไม่มีแฟล็ก **ไม่ต้องแก้ไฟล์ chief เลย
เพราะใช้ jack เดิม**

บรรทัดจริงที่เห็นวันนี้ (ไม่มี legacy/held_indices ส่งมาจาก call ตรง ๆ ในเทส แต่ที่ `runtime.py`
ส่งมาจริง):

```
WORLD_M2_RETURN_POPULATION owed=YES source=bg0001_census kind=census count=115 count_source=full_census composed=NO
```

### 2.3 สองจุดแก้เอกสารเก่าที่ตรวจพบระหว่างอ่านไฟล์เดิม (ไม่ใช่งานหลัก แต่แก้ตรงจุด)

พบสอง comment ในไฟล์เดียวกันที่ยังอ้าง (present tense) ว่า "call site ยังไม่ส่ง legacy/held_indices/
departed_from" ทั้งที่ `runtime.py:4985-5021` ส่งมาตั้งแต่รอบ `R229/qb70g2` แล้ว (จุดหนึ่งอยู่ใน
`_emit_arrival_stowaways`'s `if legacy is None:` branch, อีกจุดอยู่ที่ comment ก่อน emit ของ
`return_leg_console_line`) แก้ด้วยการขีดฆ่า/แก้ข้อความ ไม่ลบ ตามธรรมเนียมไฟล์

**หมายเหตุสำคัญ**: จุดที่สาม (ย่อหน้า docstring ใหญ่เรื่อง "this round's CORE-REQUEST to chief")
รอบนี้แก้ไปเหมือนกันโดยอิสระ - แต่พอ rebase กับ main ใหม่ (ดูข้อ 4) พบว่ารอบ `oprday` (ซึ่งเพิ่งถูกกู้
กลับมา merge จริงระหว่างที่รอบนี้กำลังทำงาน) **แก้ประโยคเดียวกันไปแล้วก่อนหน้า** ด้วยถ้อยคำที่ต่างกัน
เล็กน้อยแต่ความหมายเดียวกันทุกประการ - เก็บของ `oprday` ไว้ (เพราะ merge แล้วจริงบน main ก่อน) ไม่ทับ
ด้วยของรอบนี้ ไดฟ์เดียวกันไม่ควรพูดความจริงเดียวกันสองแบบ

## 3. Gate (วัดหลัง rebase กับ main ใหม่แล้ว - ดูข้อ 4)

| check | result |
|---|---|
| `python3 -m pytest tests -q` | **5586 passed, 327 skipped, 0 failed**, 9729 subtests (183s) |
| `python3 tools/verify_hypothesis_ledger.py` | `HYPOTHESIS_LEDGER PASS entries=47` |
| `python3 tools/verify_functional_coverage.py` | rc=0, 8 open domains (ไม่เปลี่ยนจากรอบก่อน) |
| `git diff -- current/pf_login_game_server_v141.py src/pirateforce_foundation/runtime.py src/pirateforce_foundation/app.py` | ว่างเปล่า - ไฟล์ต้องห้ามไม่ถูกแตะเลย |
| `git diff --check` | เงียบ |
| `git check-ignore` ทั้งห้าไฟล์ที่แตะ | ไม่ถูก ignore สักไฟล์ |
| cp874/ASCII scan ทั้งห้าไฟล์ | ผ่านหมด (`.decode("ascii")` และ `.decode("cp874")`) |

## 4. เหตุการณ์กลางรอบ: main ขยับจริงระหว่างทำงาน - rebase แล้วแก้ conflict หนึ่งจุด

`git fetch origin main` กลางรอบพบว่า origin/main ขยับจาก `10a302d` (จุดเริ่มรอบ) ไปเป็น `c2d67ac`
จริง - ที่สำคัญที่สุดคือ **PR #332 (แถวทะเบียนฉาก 126 ของรอบ `oprday`) ถูกกู้คืนและ merge จริงแล้ว**
ผ่าน chief round R249 (`v1 declared plus PR332 gate-red-repair`) และ GM round `2f9xji`
(fixture-dedup fix ตามที่รอบ `oprday`/ใบ blocker เตือนไว้ว่าต้องแก้ fixture ไม่ใช่แก้ค่าคาดหวัง - แก้
ถูกจุดจริงตามที่เตือน) **ยืนยันจาก `notes_to_chief/consumed/20260830_2112_LANE-A-BLOCKER-...md` และ
`.../20260830_2114_LANE-A-STATUS-pr332-closed-...md` ที่ตอนนี้มี `.CONSUMED.txt` แล้วทั้งคู่**

ขั้นตอนที่ทำ (บันทึกไว้เพราะเป็นการตัดสินใจ ไม่ใช่ auto-merge เงียบ ๆ):

1. `git stash push -u` เก็บ diff ที่ยังไม่ commit ของรอบนี้ (5 ไฟล์)
2. `git merge --ff-only origin/main` ให้ branch ขยับไป `c2d67ac` สะอาด (fast-forward จริง ไม่มี merge commit)
3. `git stash pop` - ชน conflict **หนึ่งจุดเดียว** ใน `columbus_quest_dispatch.py`: ย่อหน้าเดียวกันทั้ง
   รอบนี้และรอบ `oprday` (ที่เพิ่งกู้กลับมา) แก้ประโยค "this round's CORE-REQUEST to chief" ที่ล้าสมัย
   ไปพร้อมกันโดยไม่รู้ตัว (สองรอบทำงานคาบเกี่ยวกันจริง - อาจเป็นเคสที่ COO-DECISION
   `claim-before-work` รอบใหม่ (2244) พูดถึง แม้จะไม่ตรงเป๊ะ เพราะนี่ไม่ใช่ใบเปิดกว้างหลายสาย
   แค่สองรอบของสาย A เดียวกันอ่านโค้ดจุดเดียวกันคนละเวลา) แก้โดย**เก็บของ `oprday` ที่ merge อยู่บน
   main แล้วไว้** ไม่ทับด้วยของรอบนี้ (มีเหตุผลเดียวกันแค่คำต่างกัน การมีสองคำอธิบายความจริงเดียวกัน
   ไม่มีประโยชน์) - อีกสี่ไฟล์ merge สะอาดไม่มี conflict
4. รันชุดเทสเต็มใหม่ทั้งหมดอีกครั้งบน main ใหม่ (ผลอยู่ข้อ 3 ข้างบน) - ไม่ได้เชื่อผลรอบก่อน rebase
5. `git stash drop` หลัง verify ว่า conflict แก้ครบและเทสผ่านหมดแล้ว

**ผลคือโค้ดของรอบนี้ทดสอบจริงกับ main ล่าสุดที่มีฉาก 126 อยู่แล้ว ไม่ใช่ main เก่าที่ orchestrator
ให้จุดเริ่มไว้** ตัวเลข gate ในข้อ 3 คือตัวเลขหลัง rebase เท่านั้น (ก่อน rebase ก็เขียวเหมือนกัน
5583/5585 passed แล้วแต่จังหวะที่วัด แต่ตัวเลขนั้นวัดกับ main ที่ตอนนี้ล้าสมัยไปแล้ว ไม่รายงานซ้ำ)

## 5. Adversarial self-review (ทำเอง - ไม่มี pf-adversary subagent ในสภาพแวดล้อมนี้)

* **มิวเทชันที่ทดสอบจับได้**: สลับ `!=` เป็น `==` ที่ branch `source != world_scene_travel.CENSUS_SOURCE`
  ใน `return_population_owed` -> `test_the_sea_crossing_owes_the_home_census_by_name` จะแดงทันที
  (count จะกลายเป็น None ทั้งที่ควรเป็น 115)
* **coverage gap ที่แก้แล้ว**: แขนง `source is None` -> `SOURCE_NOT_NAMED` และแขนง "source อื่นที่ไม่ใช่
  census" ไม่มีทางเกิดจริงจากทะเบียนที่ shipped วันนี้ (ฉากบ้านมีแค่ค่าเดียว) - เพิ่มเทสสองตัวที่
  `unittest.mock.patch.object(world_scene_travel, "population_source", ...)` บังคับให้แขนงทำงานจริง
  แทนที่จะเช็คแค่ค่าคงที่เฉย ๆ
* **false-positive ที่จับได้เอง**: เทสแรกที่เขียน (`test_this_function_never_builds_the_actual_roster`)
  เช็คคำเปล่า `"world_population_handoff"` ในซอร์ส - ชนกับ docstring ของตัวเองที่อธิบายว่าทำไมถึงไม่เรียก
  มัน (ชื่อโมดูลปรากฏในร้อยแก้วเอง) แก้เป็นเช็ค call syntax จริง (`.handoff_on_crossing(` /
  `.handoff_for_arrival(`) ตามแบบที่เทสอื่นในไฟล์เดียวกันทำไว้แล้ว ("Call syntax, not bare words")
* **บรรทัดยาวเกิน 79 ตัวอักษร**: `awk` เช็คทั้งไฟล์ที่แตะเทียบกับ baseline (ไฟล์เดิมมี 0 บรรทัดเกิน
  79 - โปรเจกต์ยึด 79 จริง ไม่ใช่ 99/119) พบ 4 บรรทัดที่รอบนี้เพิ่มเกิน - ตัดให้สั้นลงทั้งหมด
* **การอ้างรอบ**: เขียนคอมเมนต์อ้าง "round `pf-builder/M2-return-population`" ก่อน - ไม่ตรงธรรมเนียม
  โปรเจกต์ (อ้างด้วย token 6 ตัวอักษรจาก branch เสมอ) แก้เป็น "round 4lrspn" ทั้งหมดก่อน commit
  (ยืนยันชื่อรอบ `R229/qb70g2` ที่อ้างถึงจริงด้วย `grep -rl qb70g2 pf_bridge/rounds` ก่อนเขียน ไม่ได้
  เดา)
* **ความเสี่ยงที่ยังไม่ตัดออก**: ฟังก์ชันใหม่ยัง raise ได้ (ผ่าน `return_leg`) เมื่อ `departed`
  เป็นแถวผิดฉาก - นี่คือ contract เดียวกับ `return_leg` เอง (raise ในชั้น report, ไม่ raise ในชั้น
  console) มีเทสยืนยันทั้งสองชั้นแล้ว (`test_owed_is_shared_with_return_leg_not_re_derived` +
  `test_nothing_a_caller_can_hand_this_makes_it_raise`)

## 5b. pf-adversary จริง (orchestrating session เรียกได้ นอกสภาพแวดล้อมที่แยกไป)

Orchestrating session เรียก pf-adversary subagent จริงตรวจ diff นี้แยกต่างหาก (worktree ของตัวเอง
ไม่แตะ checkout จริง) ผล: ยืนยัน 77/77 เทสผ่าน, `runtime.py`/`app.py`/`pf_login_game_server_v141.py`
ไม่ถูกแตะ, ทำ mutation test ซ้ำ 5 จุด (สลับ `!=`/`==`, สลับ field ใน dict ที่คืน, พลิก `if not
ticket["owed"]`, พลิก `if report["count"] is None`, ลบ emit ใหม่) ไม่มีมิวเทชันไหนรอด - **สรุปว่าเป็น
เทสที่ต้านมิวเทชันจริง ไม่ใช่แค่ท่องพฤติกรรมซ้ำ**

พบหนึ่งจุด severity ต่ำที่รอบนี้ (ก่อน adversary ตรวจ) ไม่เคย pin ไว้: `return_population_owed`
(`world_m2_return_leg.py:272-273`) อ่าน `home.scene_id` (ปลายทาง) ไม่ใช่ `departed.scene_id`
(ต้นทาง) - สลับสองตัวนี้แล้วรันสวีตทั้ง 77 เทสผ่านหมด (ไม่มีเทสไหนแยกสองตัวนี้ออกจากกัน) ตรวจแล้วว่า
**ไม่ใช่บั๊กที่เกิดจริงวันนี้**: `remember_departure`/`world_scene_entry.return_ticket` บังคับให้แถว
`departed` ที่ไม่ใช่ `None` ต้องเท่ากับ `HOME_SCENE_ID` อยู่แล้วเหมือนกับ `home` เอง สองค่านี้จึงเท่ากัน
เสมอภายใต้ทะเบียนที่ shipped วันนี้ - เป็นช่องว่างของเทส (coverage gap) ไม่ใช่พฤติกรรมผิดที่ใช้งานได้จริง
และเป็นประเภทเดียวกับที่ `SOURCE_NOT_NAMED` (บรรทัด 240-245) ประกาศไว้แล้วว่า "not reachable today"

**แก้แล้วก่อน commit**: เพิ่มคอมเมนต์ที่บรรทัดนั้นระบุเจตนาชัดเจน (อ่าน scene ปลายทางที่ผู้เล่นจะไปถึง
ไม่ใช่ scene ที่จากมา) พร้อมเงื่อนไขที่ต้องเพิ่มเทสจริงถ้าวันหนึ่งมีปลายทางขากลับที่สอง - รูปแบบเดียวกับ
`SOURCE_NOT_NAMED` เอง รันเทสทั้งสามไฟล์ซ้ำหลังแก้: ยังผ่าน 77/77 เหมือนเดิม ไม่มีพฤติกรรมเปลี่ยน

## 6. ไฟล์ที่แตะ (5, ทั้งหมดใน `pirate-force-server`)

* `src/pirateforce_foundation/world_m2_return_leg.py` - +128 บรรทัด (สองฟังก์ชันใหม่ + docstring)
* `src/pirateforce_foundation/columbus_quest_dispatch.py` - +1 emit, 3 จุดแก้ comment, 1 จุดรวมกับ
  การแก้ของรอบ `oprday` ที่เพิ่งกู้กลับมา (ดูข้อ 4)
* `tests/test_world_m2_return_leg.py` - +11 เทสใหม่ (2 คลาสใหม่: `ReturnPopulationOwedTests`,
  `ReturnPopulationConsoleTests`) + ปรับ pin รายการ import ที่ทดสอบไว้
* `tests/test_columbus_quest_dispatch.py` - ปรับ index ของบรรทัดที่ pin ไว้ (`lines[-N]`) จาก 3 บรรทัด
  รายงานเป็น 4 บรรทัด
* `tests/test_columbus_quest_dispatch_wiring.py` - +1 เทส end-to-end ผ่าน `runtime.make_state_class`
  จริง (ไม่ใช่แค่เรียก `columbus_quest_dispatch` ตรง ๆ)

`runtime.py`, `app.py`, `current/pf_login_game_server_v141.py`: **ไม่ถูกแตะเลย** (ตรวจด้วย
`git diff` เปล่าตามข้อ 3)

## 7. ยังไม่ได้พิสูจน์

ทุกอย่างเป็นบรรทัดคอนโซล ไม่มีอะไรถึงไคลเอนต์ - ไม่มีมนุษย์คนไหนเห็นบรรทัดนี้บนจอจริง เพราะไม่มีทางกลับ
จากฉาก 17 ให้เดินถึงเลยวันนี้ (`RE-077` ขากลับเปิดอยู่) บรรทัดนี้จึงเป็นการเตรียมของไว้ล่วงหน้า ไม่ใช่
สิ่งที่พิสูจน์ว่าใช้งานได้จริงกับไคลเอนต์ - รอวันที่มีทาง dispatch ขากลับจริงก่อน

รอบนี้ไม่ตั้งสถานะให้ใคร ไม่เขียน PASS ไม่ประกาศว่า M2 ถึงหมุดไหน

CORE-REQUEST: none (ต่อกับ call site เดิมที่มีอยู่แล้ว ไม่ต้องแก้ `runtime.py`)
เปิดใบให้สาย C: none

— LANE-A (WORLD) รอบ `4lrspn`

---
_Generated by [Claude Code](https://claude.ai/code)_
