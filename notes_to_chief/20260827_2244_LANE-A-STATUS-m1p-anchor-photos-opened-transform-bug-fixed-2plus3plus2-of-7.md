[ถึง: chief cloud - cc: COO, Panya, RE runner | จาก: สาย A (WORLD) รอบ `5irwkp` - 2026-08-27T22:44+07:00]
[ตอบ: `20260827_2010_PANYA-DECISION-pause-M2-M1-identity-first-Prison-Exile-Bg0002-MOBSET-equals-nID.md` (M1-P anchor evidence, ต่อจากรอบ `85vaq0`/`cyp4zt`)]

# LANE-A-STATUS-5irwkp - เปิดภาพ evidence 3 ใบที่ยังไม่เคยเปิด, พบและแก้บั๊ก transform, anchor เพิ่มจาก 2/7

## สรุปสั้น
รอบก่อน (`85vaq0`) เป็น status-only เพราะไม่มีอะไรใหม่ให้ทำ - anchor ยังค้างที่ 2/7 numeric,
3 ใบ evidence (Navy-Transfer-at-gate, Sebastian+Goliaon, Pike) ยังเป็น "photograph this
lane did not open" ตามคำของจดหมาย 20:10 เอง รอบนี้เปิดทั้งสามไฟล์จริง
(`pf_bridge/evidence_screens/REF_ORIGINAL_SERVER_PrisonExile_*.jpg`, ของเดิม ไม่ใช่
capture ใหม่) และพบบั๊กจริงระหว่างทาง: Veronica anchor's HUD X ที่เคยอ่านว่า `+3825` จริง
ๆ แล้วภาพพิมพ์ `-3825` (มีเครื่องหมายลบ) ทำให้ transform ที่เคยเขียนไว้ ("negate X, keep Y")
ผิด แก้เป็น identity transform แล้ว - ระยะ match ของ Veronica เองไม่เปลี่ยน (หักล้างกันพอดี
สำหรับ anchor นี้ตัวเดียว) แต่ transform ที่ถูกจะสำคัญกับ anchor ตัวอื่นในอนาคต

## ผลของรอบนี้ (ดูรายละเอียดเต็มใน `rounds/A_20260827_2244_5irwkp_*.md`)
- Veronica, Legend-Jack-cluster: **CONFIRMED numeric เท่าเดิม (2)** - ตัวเลข match ไม่
  เปลี่ยน, sign/transform ที่ใช้คำนวณถูกแก้
- Navy-Transfer near Sebastian (ภาพเดียวกันเห็นทั้งคู่ที่ประตูเกาะคุก, ห่างกัน 3079.9
  หน่วย): **SUPPORTIVE ใหม่** (2 -> 3)
- Sebastian, Pike: nameplate ในภาพตรงกับ `display_name`/`title` ในตารางตัวสะกดเป๊ะ, ตรวจ
  แบบ programmatic ไม่ hardcode: **NAME/TITLE MATCH ใหม่** (0 -> 2, หมวดใหม่ อ่อนกว่า
  numeric)
- **ยังไม่มีตัวเลข HUD ที่อ่านได้จากภาพ Sebastian/Pike เลย** - บีบอัดหนักกว่าภาพ Veronica
  มาก ลองซูม/filter หลายแบบแล้วอ่านไม่ได้ด้วยความมั่นใจ ไม่เดา ไม่ปั้นตัวเลข (self-check เจอ
  ตัวเองอ้างผิดว่า "ไม่มีเครื่องหมายลบ" ทั้งที่ภาพเบลอเกินยืนยัน แก้เป็น "อ่านไม่ได้เลยทั้ง
  สองทาง" ก่อน commit)
- `anchor_report()["all_seven_confirmed"]` ยังเป็น `False` - **ยังไม่ประกาศ "NN =
  MOBS.n_ID" เป็น fact** ตามกฎเดิมของจดหมาย 20:10 การเปิดภาพไม่ใช่การยืนยันจากมนุษย์

## สิ่งที่ยังไม่เปลี่ยน
CORE-REQUEST-021 ยังรอ chief ทำ M1-P ข้อ 2 (seed run DB ให้ Arena01 อยู่ scene_id=2 +
login wiring) เหมือนที่ `20260827_2200_CHIEF-REPLY-*` บอกไว้ - รอบนี้ไม่กระทบจุดต่อสายที่มี
อยู่เลย (โมดูลสำมะโน `world_population_bg0002.py` ไม่เรียก `hud_from_placement`/
`VERONICA_HUD_X` เลย เป็นคนละชั้นกัน) ผู้เล่นยังไม่เห็นอะไรต่างจากเมื่อวาน - Prison Exile
Island ยังส่งไม่ถึงบูตไหนเลยวันนี้

## เทส
`test_scene2_prison_exile_tables.py` 17/17 (15 เดิม + 2 ใหม่), `test_world_population_bg0002.py`
+ `test_bg0002_census_wiring.py` 17/17 ไม่กระทบ, สวีตเต็ม `3637 passed, 323 skipped,
5035 subtests, 0 FAIL`

## ไฟล์ที่แตะ (`pirate-force-server`, branch `claude/sleepy-ride-5irwkp`)
`src/pirateforce_foundation/scene2_prison_exile_tables.py`,
`tests/test_scene2_prison_exile_tables.py` - 2 ไฟล์

## CORE-REQUEST
ไม่มีใบใหม่

## เปิดใบให้สาย C
ไม่มี

-- สาย A - WORLD
