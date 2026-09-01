# ROUND A_5irwkp 2026-08-27T22:44+07:00 -- LANE-A (WORLD)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
**ไม่มีอะไรบนจอ** -- เหมือนรอบก่อน (85vaq0, status only) เมืองยังคือ Port Royal 115
actor เท่าเดิม, Prison Exile Island (Bg0002) ยังส่งไม่ถึงไคลเอนต์บูตไหนเลยวันนี้ (ไม่มี
seed path ให้ character row เป็น scene_id=2 -- นั่นคืองานของ chief ตาม M1-P ข้อ 2 ที่ยัง
ไม่เสร็จ, สาย A ไม่มีสิทธิ์แก้ run DB/runtime.py) รอบนี้แก้ "หลักฐาน" ที่มนุษย์จะใช้ยืนยัน
ชื่อ/ตำแหน่งในรอบ attended M1-P ครั้งถัดไป ไม่ใช่สิ่งที่ผู้เล่นเห็น

## บริบทต้นรอบ
ตรวจ PR ล่าสุดของสาย A ทั้งสอง repo (protocol A): `pirate-force-server` #150 และ
`pf_bridge` #241 ยืนยัน `merged_at != null` ทั้งคู่ (query PR รายตัว ไม่ใช้ list endpoint) --
งานอยู่บน main แล้วจริง ไม่ต้อง cherry-pick กู้อะไร

กล่องจดหมาย (protocol B): RE-095/096/097/100/102/103 ทั้งหมด **บริโภคไปแล้วจริง** โดยรอบ
`kqrlhr` ก่อนหน้า (`1cc8e53`, เป็น ancestor ของ main ยืนยันด้วย `git merge-base
--is-ancestor`) -- มี `.CONSUMED.txt` ครบทุกใบ, หัวใบ `CLIENT_RE_QUEUE.md` ปิดแล้ว
(096/100/102 = CLOSED, 103 = ยังเปิดแต่เป็นของ chief cloud รอบ `4txjyg` ไม่ใช่ของสาย A --
กฎ header-ownership ห้ามแตะ). ไม่มีอะไรให้บริโภคใหม่ในรอบนี้

## สิ่งที่พบและแก้ (`pirate-force-server`, branch `claude/sleepy-ride-5irwkp`)

M1-P letter (`20260827_2010_PANYA-DECISION-...`) บอกไว้ว่า anchor 3 ใน 7 (Navy
Transfer-at-gate, Sebastian+Goliaon, Pike) เป็น "photographs this lane did not open" --
รอบนี้เปิดทั้งสามไฟล์จริง (`pf_bridge/evidence_screens/REF_ORIGINAL_SERVER_
PrisonExile_*.jpg`, ของเดิมที่ commit ไว้แล้ว ไม่ใช่ capture ใหม่):

1. **แก้บั๊กจริงที่พบระหว่างเปิดภาพ**: Veronica anchor เดิมเขียนไว้ว่า transform คือ
   "negate X, keep Y" (`hud_from_placement`) และ `VERONICA_HUD_X = 3825.0` (บวก) ซูมภาพ
   `REF_ORIGINAL_SERVER_PrisonExile_Veronica_ApprenticeWitch_20260827.jpg` ที่ 15-18x
   (หลายรอบ ยืนยันซ้ำด้วย crop คนละมุม) เห็นชัดว่า minimap พิมพ์ `X:-3,825` (มีเครื่องหมาย
   ลบ) ไม่ใช่ `X:3,825` -- ระยะทางที่ match ยังเท่าเดิม (248.76 หน่วย, sign flip แบบเดิม
   หักล้างตัวเองพอดีสำหรับ anchor นี้ตัวเดียว เพราะทั้ง HUD X และ placement X ติดลบทั้งคู่ --
   นี่คือเหตุที่บั๊กไม่มีใครจับได้) แต่ transform ที่ถูกต้องคือ **identity ไม่มี sign flip**
   (`HUD_x = placement_x`) -- สำคัญเพราะถ้าเอา transform ผิดไปทำนายพิกัดของ anchor อื่น
   (เช่น Sebastian placement x เป็นบวก 23184) transform เดิมจะทำนาย HUD X ติดลบผิดทิศ
2. **เพิ่มหลักฐานใหม่ (name/title match)**: Sebastian (NN 2) กับ Pike (NN 5) -- nameplate
   ในภาพตรงกับ `display_name`/`title` ในตาราง **ตัวสะกดตรงเป๊ะ** ("Warden"/"Sebastian",
   "Unemployed Sailor"/"Pike") ตรวจแบบ programmatic (`PHOTO_NAME_TITLE_EVIDENCE` เทียบกับ
   `KNOWN_PLACEMENTS` ใน `anchor_report()`) ไม่ใช่ hardcode ไว้เฉย ๆ -- ภาพ Pike ยังเห็นรั้ว
   ไม้+คบไฟ ตรงกับ "Pike ในคอกไม้" ที่จดหมายบอก **ไม่มีตัวเลข HUD ที่อ่านได้จากทั้งสองภาพ**
   (บีบอัด JPEG หนักกว่าภาพ Veronica มาก ลองซูม 10-16x หลายแบบแล้วอ่านตัวเลขไม่ได้ด้วยความ
   มั่นใจ -- ไม่เดา ไม่ปั้นตัวเลข)
3. **หลักฐานสนับสนุนใหม่ (proximity)**: ภาพ `NavyTransfer_at_dock_gate` เฟรมเดียวเห็น Navy
   Transfer และ Warden Sebastian/Goliaon อยู่ด้วยกันที่ประตูทางเข้า "Prison Exile Island"
   -- placement ห่างกัน 3079.9 หน่วย (order เดียวกับคู่ Columbus-Navy Transfer ที่ยอมรับแล้ว
   ว่า SUPPORTIVE)

## สถานะ anchor หลังรอบนี้ (`anchor_report()`)
- CONFIRMED (numeric): Veronica, Legend-Jack/Men/Deer cluster -- **2 เท่าเดิม** (ตัวเลขไม่
  เปลี่ยน แค่ transform/sign ที่ใช้คำนวณถูกแก้)
- SUPPORTIVE (numeric, ไม่แน่น): Columbus-near-NavyTransfer, NavyTransfer-near-spawn,
  **ใหม่: NavyTransfer-near-Sebastian** -- 2 -> 3
- NAME/TITLE MATCH (ใหม่ทั้งคู่, ไม่มีพิกัด): Sebastian, Pike -- 0 -> 2
- ไม่เปิดเลย: 0 (จาก 3 เดิม)
- `all_seven_confirmed` ยังเป็น `False` เหมือนเดิม -- **ไม่ประกาศ "NN = MOBS.n_ID" เป็น
  fact** ยังต้องรอมนุษย์ยืนยันในรอบ attended M1-P ตามกฎเดิมของจดหมาย 20:10 (การเปิดภาพ
  ไม่ใช่การยืนยัน แค่เพิ่มหลักฐานอีกชั้น)

## ตัวเลขที่วัดได้
- ไฟล์ที่แตะ: `pirate-force-server/src/pirateforce_foundation/scene2_prison_exile_tables.py`
  (docstring + 3 ค่าคงที่ + 1 dict ใหม่ + `hud_from_placement()` + `anchor_report()`
  ขยาย), `pirate-force-server/tests/test_scene2_prison_exile_tables.py` (แก้ 3 เทสเดิม +
  เพิ่ม 2 เทสใหม่) = 2 ไฟล์
- เทส: `test_scene2_prison_exile_tables.py` 17/17 ผ่าน (15 เดิม + 2 ใหม่),
  `test_world_population_bg0002.py` + `test_bg0002_census_wiring.py` 17/17 ผ่าน (ไม่กระทบ
  -- โมดูลสำมะโนไม่เรียก `hud_from_placement`/`VERONICA_HUD_X` เลย) สวีตเต็มทั้งโปรเจกต์
  `3637 passed, 323 skipped, 5035 subtests, 0 FAIL` (ติดตั้ง `capstone`/`pefile` เพิ่มเอง
  ในเครื่องทดสอบ -- ของเดิมรายงาน error เพราะไม่มีสองแพ็กเกจนี้ ไม่ใช่บั๊กจริง)
- cp874/ASCII: ทั้งสองไฟล์ที่แก้ผ่าน `.encode('cp874')` และ `.encode('ascii')` (โค้ด src/
  เป็น ASCII pure ตามกฎ)

## nonclaims
- ไม่ได้แตะ `runtime.py`/`app.py`/run DB/canonical DB เลย
- ไม่ได้เปิดเกม ไม่มี headless boot ใหม่รอบนี้ (ไม่จำเป็น -- งานเป็นการอ่านภาพ evidence ที่
  commit ไว้แล้ว ไม่ใช่ capture ใหม่)
- ยังไม่ยืนยัน anchor ครบ 7 -- 2 ตัวใหม่เป็น name/title match เท่านั้น ไม่ใช่ numeric
- self-check เจอ overclaim ของตัวเองระหว่างรอบ (อ้างว่าภาพ Sebastian "ไม่มีเครื่องหมายลบ" ทั้ง
  ที่ภาพเบลอเกินจะยืนยัน) แก้ทันทีก่อน commit เป็น "อ่านเครื่องหมายไม่ได้เลย ทั้งสองทาง"

## CORE-REQUEST
ไม่มีใบใหม่ -- การแก้รอบนี้อยู่ในชั้น diagnostic/evidence เท่านั้น ไม่กระทบจุดต่อสายที่มีอยู่
(`CORE-REQUEST-021` ยังรอ chief ทำ M1-P ข้อ 2 (seed run DB + login wiring) ตามเดิม ไม่มี
อะไรเปลี่ยนจากรอบ `f9pzed`)

## เปิดใบให้สาย C
ไม่มี -- ไม่เจอคำถามใหม่ที่ต้องให้ RE ตอบรอบนี้ (คำถามเดิม "ปลายทางฉาก 126 vs 17" ยังพักอยู่
กับ M2 ตามคำสั่ง 20:10, ไม่ใช่ของ M1-P)

-- สาย A · WORLD
