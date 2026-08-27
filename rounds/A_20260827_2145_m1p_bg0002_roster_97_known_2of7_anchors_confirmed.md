# รอบ `A_20260827_2145` - สาย A - WORLD (`pf-builder`)

**เวลา:** 2026-08-27T21:45+07:00
**สาย:** A (WORLD)
**คำสั่งที่ทำงานตาม:** PANYA-DECISION 2026-08-27 20:10 (`notes_to_chief/20260827_2010_PANYA-DECISION-pause-M2-M1-identity-first-Prison-Exile-Bg0002-MOBSET-equals-nID.md`) - M2 พัก, M1-P (เกาะคุก) เป็นลำดับหนึ่ง

---

## ① ประโยคบังคับของสาย: ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

> **ยังไม่มีอะไรต่างในเกม** - โมดูลรอบนี้ยังไม่ถูกเรียกจากเส้นทางบูตจริง (`runtime.py` เป็นไฟล์ของ chief)
> ของที่สร้างคือ "ตัวประกอบสำมะโนเกาะคุก" ที่พร้อมต่อสาย ไม่ใช่การต่อสายเอง - ดู CORE-REQUEST ข้อ ⑧

## ② BUILD-001/BUILD-002 เดิม: สถานะจริงก่อนเปลี่ยนคำสั่ง

ตรวจก่อนได้รับคำสั่งใหม่ (PANYA-DECISION 20:10) พบว่า:

- **BUILD-001 (M1 เมืองมีชีวิต) เสร็จแล้วจริง ไม่ต้องทำซ้ำ** - `src/pirateforce_foundation/world_population.py`
  มี `production_allowed = True`, `DEFAULT_ACTOR_COUNT = CENSUS_COUNT` (115) และ `runtime.py:930-932`
  (`world_census_enabled = not active_lanes and second_password_mode == "required"`) ต่อสายเข้า
  `build_world_population`/`census_console_line` แล้วแบบ **ไม่มีแฟล็ก** (ปิดเฉพาะตอนมี opt-in lane อื่นทำงานอยู่ -
  เป็นการกันชนไม่ใช่สวิตช์ฟีเจอร์) `dispatch_report()`/`census_console_line()` พิมพ์
  `assembled=N/115` ทุกบูตตามที่ CHARTER-02 สั่งแล้ว
- **BUILD-002 (M2 ออกจากเมือง) ยังบล็อกเหมือนที่รายงานไว้รอบก่อน** ไม่มีอะไรให้ทำเพิ่มก่อนคำสั่งใหม่มาถึง
- ไม่ได้แก้อะไรในสองงานนี้รอบนี้ (ไม่มีของเก่าที่ต้องทิ้ง เพราะยังไม่ได้เขียนไฟล์ใดๆ ก่อนได้รับ PANYA-DECISION 20:10)

## ③ คำสั่งใหม่ที่ทำตามรอบนี้: M1-P (roster_bg0002)

PANYA-DECISION 20:10 สั่งพัก M2 (ยกเว้นบั๊ก persistence ที่ทำไปแล้วรอบก่อน) และให้สาย A ทำ
**item 1 (roster_bg0002)**: จอยน์ placement ทุกจุดของ Bg0002 (เกาะคุก) เข้ากับ `MOBS.n_ID` ผ่านชื่อ
`MOBSET_NN MM`, ดึงชื่อ/ตำแหน่งจาก `MOBS_TIP`, body/preset/level จาก `MOBS`, ตรวจ anchor 7 จุด,
ติดป้าย UNKNOWN ให้ชุด 101-104 ไม่วาง แล้วเขียน `WORLD_CENSUS` ของฉาก 2 ผ่าน production path (encoder เดิม)

**หมายเหตุขอบเขต**: `tools/` ไม่อยู่ในเขตเขียนของสาย A รอบนี้ (ตามบรีฟ) - จึงไม่สร้าง
`tools/pf_mine_scene2_prison_exile_roster.py` เอง ทำ join ด้วยมือแทน (สคริปต์ที่ใช้จริง +
บันทึกการ cross-check ทุกแถวอยู่นอก repo ใน scratchpad ของรอบนี้) แล้วบันทึกทุกขั้นตอนไว้ในเอกสารของ
โมดูลที่ได้ ให้คนละรอบสร้าง `tools/pf_mine_scene2_prison_exile_roster.py` ให้ mechanise ทีหลังได้ตรงตามที่เขียนไว้

## ④ ตัวเลขที่วัดได้จากการ join

จาก `Bg0002.placements.tsv` (106 แถว) ผ่าน `CONSTDATA_TH__MOBS` / `CONSTDATA_TH__STANDARD_MOB` /
`TEXTDATA_TH__MOBS_TIP` (digest ตรงกับที่ `field_mob_tables.py` ปักไว้แล้วสำหรับ bg0001):

- **assembled 97 / 106** - ตัวที่สร้าง actor entry ได้จริง (ชื่อ+ preset + HP ครบ)
- **unresolved 9 / 106** - **ไม่ใช่ 5 ตามจดหมาย** เป็นความคลาดเคลื่อนที่พบและรายงานตรงๆ ไม่ปิดทับ:
  - 8 แถวอยู่ในบล็อก n_ID 101-104 ที่เจ้าของสั่งห้ามเดา (ไม่ใช่ 5)
  - **1 แถวใหม่ที่จดหมายไม่ได้พูดถึง**: n_ID 37 "Port transportation" มีชื่อใน `MOBS_TIP` แต่**ไม่มีแถวใน
    `MOBS` เลย** (ไม่มี outfit/level ให้สร้าง body) - ไม่วาง ไม่เดา บันทึกเหตุผลไว้
- **53 / 97 แถวมี outfit กำกวม** (`s_OUTFIT` เป็นลิสต์คั่น `;`) - เลือก outfit ตัวแรกเป็นค่าเริ่มต้น
  ทำเครื่องหมาย `ambiguous_outfit=True` ไว้ทุกแถว ไม่ใช่การวัด เป็นการเลือกที่ต้องรู้ไว้

## ⑤ ผล anchor 7 จุด (ตามกฎ "ห้ามอ้าง NN = n_ID เป็นข้อเท็จจริงจนกว่าครบ 7")

**ยืนยันด้วยตัวเลขจริง 2 จุด:**
- **Veronica (n_ID 14)**: HUD (3825,12447) เทียบตำแหน่ง (-3598.77,12550.46) ผ่าน transform sign-flip แกน X
  (HUD_x = -placement_x, HUD_y = placement_y คงเดิม - สูตรนี้ re-derive จาก anchor นี้เอง ไม่พบ helper
  สำเร็จรูปในซอร์สจริง แม้บรีฟจะบอกว่ามี) ผลต่าง 226.2/103.5 หน่วย - ตรงกับที่จดหมายรายงานไว้ (227/103) พอดี
- **Legend Jack(6) + Men(7 ×2) + Mountain Deer(27 instance 2)**: ระยะคู่ 601-1647 หน่วย ยืนกลุ่มเดียวกันจริง

**สนับสนุนแต่ไม่แน่น 2 จุด:**
- Columbus(36) ห่าง Navy Transfer(1) 3935 หน่วย - อยู่โซนท่าเรือเดียวกัน ไม่ใกล้ชิดขนาดนั้น
- Navy Transfer(1) ห่างจุด spawn ฉาก 2 ที่ปักไว้แล้วใน `world_scene_registry_001.json` (26905,21185) 1147 หน่วย

**ยังไม่มีหลักฐานเชิงตัวเลข 3 จุด** (มีแต่ภาพในจดหมายที่สายนี้ไม่ได้เปิดดู): Navy Transfer ที่ประตูท่า,
Sebastian+Goliaon (Goliaon ไม่มีแถวใน MOBS เลย - อ่านว่าเป็น prop ของฉาก ไม่ใช่ NPC), Pike ในคอกไม้

**⇒ ไม่ประกาศว่า "NN = MOBS.n_ID" เป็นข้อเท็จจริง** โมดูลที่สร้างพิมพ์สถานะนี้ตรงๆ (`anchor_report()`
คืน `all_seven_confirmed: False` เสมอ) - ยัง[สมมติฐานแข็ง]ตามกฎของจดหมาย ต้องให้เจ้าของยืนยันเองในรอบ attended

## ⑥ ของที่สร้าง/แก้รอบนี้ (`pirate-force-server`)

1. **`src/pirateforce_foundation/scene2_prison_exile_tables.py`** (ใหม่) - ตารางที่ join มือ (97 known +
   9 unresolved), dataclass + loader ตรวจชนิด/ช่วงค่า, `anchor_report()` คำนวณจากตารางจริงทุกครั้ง (ไม่ hardcode
   ผลลัพธ์), digest ของ 4 ไฟล์ต้นทางปักไว้ในตัว
2. **`src/pirateforce_foundation/world_population_bg0002.py`** (ใหม่) - ตัวประกอบสำมะโนฉาก 2 คู่แฝดของ
   `world_population.py`: ใช้ encoder เดิมทุกตัว (`legacy.make_npc_attr` ฯลฯ) และค่าคงที่ header ของ wire
   (`WIRE_HEADER_BYTES` ฯลฯ) **import มาจาก `world_population.py` ไม่ประกาศซ้ำ** ปฏิเสธทุกฉากยกเว้น 2
   (เหมือนที่ `world_population.py` ปฏิเสธทุกฉากยกเว้น 1) ไม่ใส่ faction bit ให้มอน 27-35 (ของสาย B ตาม
   PANYA-DECISION ข้อ 3) พิมพ์ `WORLD_CENSUS assembled=97/97 ... unresolved=9` + `n_ID name title @xyz`
   ทีละบรรทัดตามที่จดหมายสั่ง
3. **`src/pirateforce_foundation/world_scene_travel.py`** (แก้) - `population_source()` เปลี่ยนจากตอบ
   เฉพาะฉาก 1 เป็นอ่านจากตาราง `CENSUS_SOURCES` ใหม่ (`{1: "bg0001_census", 2: "bg0002_roster"}`)
   `CENSUS_SCENE_ID`/`CENSUS_SOURCE` เดิมไม่แตะ (ค่าเท่าเดิม) กันของเก่าพัง
4. **`src/pirateforce_foundation/world_population_handoff.py`** (แก้ - บั๊กที่พบและปิดในรอบเดียวกัน) -
   `handoff_for_arrival()` เดิมเช็ค `population_source(scene) is None` แล้วสาขาที่เหลือ hardcode
   `scene_id=CENSUS_SCENE_ID` (1) เข้า `build_world_population` เสมอ - เดิมปลอดภัยเพราะ `population_source`
   ตอบ non-None แค่ฉากเดียว พอข้อ 3 เปลี่ยน ฉาก 2 จะตอบ non-None ด้วย โค้ดเดิมจะเอาสำมะโน**bg0001**ไปส่งตอน
   ผู้เล่นข้ามฉากเข้าเกาะคุกแบบ live - **คือบั๊กที่โมดูลนี้เขียนมาเพื่อกันเป๊ะๆ** แก้เป็นเช็ค
   `population_source(scene) != CENSUS_SOURCE` แทน (ตรวจตรงว่าใช่แหล่งของ bg0001 หรือไม่ ไม่ใช่แค่ "ไม่ใช่ None")
   ผลคือฉาก 2 ยัง CLEAR เหมือนเดิมทุกไบต์ตอนข้าม-ฉากสด (ยังไม่ต่อสาย crossing-handoff ให้ Bg0002 - งานแบบ M2
   ที่พักไว้) มีเทสต์เดิม `test_the_dock_census_can_never_be_the_answer_for_another_scene` เป็นคนจับบั๊กนี้ให้เอง

## ⑦ เทสต์

- ใหม่: `tests/test_scene2_prison_exile_tables.py` (15 เทสต์), `tests/test_world_population_bg0002.py` (9 เทสต์)
- แก้: `tests/test_world_scene_travel.py` (1 assertion), `tests/test_world_scene_entry.py` (แยกเทสต์เดิม 1
  ตัวเป็น 2 - ฉาก 278 ยัง None, ฉาก 2 ตอบ `bg0002_roster` แล้ว)
- รันทั้ง repo: `pytest tests -q --continue-on-collection-errors`
  → **3371 passed, 234 skipped, 23 errors (pre-existing, ไม่เกี่ยวกับรอบนี้ - ขาด `capstone`/`tools` บน
  sys.path ในเครื่องนี้ ตรวจแล้วว่ามีก่อนเริ่มรอบด้วย)**, **0 failed**
- cp874-encodable ตรวจแล้วทุกไฟล์ที่แตะ (`.encode("cp874")` ผ่านหมด)

## ⑧ CORE-REQUEST

**CORE-REQUEST-BG0002-LOGIN**: ต่อสาย login path (`runtime.py`) ให้ทำตาม M1-P ข้อ 2 ของ PANYA-DECISION 20:10:
เมื่อ `world_scene_liveness.decide(...)` ให้ผล honour สำหรับแถวที่ `scene_id=2` (หลังรัน DB seed ตามที่ chief
วางแผนไว้) ให้ใช้ `world_scene_travel.login_teleport_fields(world_scene_travel.destination(2))` แทน
`legacy.make_login_teleport(1, 0)` ที่ hardcode อยู่ที่ `runtime.py:3675` แล้วเรียก
`world_population_bg0002.scene_and_census_console_lines(legacy, anchor)` (พิมพ์ `WORLD_SCENE` +
`WORLD_CENSUS` + บรรทัดต่อ actor ให้ headless-proof gate ของจดหมาย) จากนั้นค่อยส่งเฟรมของ
`world_population_bg0002.build_bg0002_population(...)` แทนสำมะโน bg0001 - **ยังไม่ทำเอง เพราะ `runtime.py`
เป็นไฟล์ของ chief**

## ⑨ ยังไม่ได้พิสูจน์ / ต้องคนจริงยืนยัน

- anchor 3 จุด (Navy Transfer ที่ประตูท่า, Sebastian+Goliaon, Pike ในคอกไม้) - ต้องเปิดภาพ
  `evidence_screens/REF_ORIGINAL_SERVER_PrisonExile_*.jpg` เทียบเอง หรือให้เจ้าของยืนยันในรอบ attended
- ตัวเลขความคลาดเคลื่อน 8 vs 5 ของบล็อก 101-104 - รายงานตรงๆ แล้ว รอเจ้าของ/COO กระทบยอด
- ทุกแถวที่ `ambiguous_outfit=True` (53/97) - ตัวแปรใน MM ที่แท้จริงต่อ outfit ยังไม่รู้ ใช้ตัวแรกเป็นค่าเริ่มต้น
- headless boot จริงยังไม่ได้รัน (โมดูลยังไม่ต่อสายเข้า `runtime.py`) - ต้องรอ CORE-REQUEST ข้อ ⑧

## ⑩ เปิดใบให้สาย C

ไม่มี

— สาย A · WORLD
