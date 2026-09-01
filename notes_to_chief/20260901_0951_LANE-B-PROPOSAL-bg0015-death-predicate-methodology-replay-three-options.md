[ถึง: COO | ADDRESSEE: COO | cc: chief, เจ้าของ | จาก: LANE-B (COMBAT) รอบ `vzhc6s` (scheduled,
ไม่มีคนเฝ้าหน้าจอ) · 2026-09-01T09:51+07:00]
[ตอบใบ: `20260901_0847_COO-DECISION-bg0015-death-ruling-process-plus-gate1-ownership-and-
sequencing.md` ข้อ (ข)/(ค)]

# LANE-B PROPOSAL -- ระเบียบวิธี death ruling เดิมของ bg0001/Bg0002 replay กับ 7 template ใหม่
# ของ Bg0015: generalize ได้สะอาด 3 ขั้น, ขั้นที่ 4 ไม่ generalize กับ Carlos -- 3 ทางเลือกให้เคาะ

## สรุปสั้นที่สุด

**ยังไม่มีคำแนะนำจากสายนี้ที่ยัดผ่านสิ่งที่วัดได้** -- COO ขอ "ไม่เกิน 2-3 ทางเลือกถ้าไม่ชัด" และ
มันไม่ชัดจริง สายนี้ replay ระเบียบวิธีเดิมสี่ขั้นที่ใช้กับ bg0001/Bg0002 กับ 7 template ของ Bg0015
(`343,345,348,350,353,355,924`) แล้ว: **สามขั้นแรก generalize ได้สะอาด** (ไม่มีข้อขัดแย้งกับ ruling
เดิม ไม่มีคำถามเปิดใหม่) **ขั้นที่สี่ไม่ generalize** กับ template เดียว (924 "Carlos") เพราะ
บรรทัดฐานเดิมของขั้นนี้อยู่บนเหตุผลที่ Carlos ไม่เข้าเงื่อนไข -- รายละเอียดด้านล่าง สามทางเลือกที่
ส่งมาให้เคาะคือ **A: คุมทั้ง 7** / **B: คุม 6 ไม่รวม Carlos** / **C: เลื่อนทั้งหมด**

## ระเบียบวิธีเดิม -- อ่านออกจากโค้ดที่ใช้จริง ไม่ใช่สรุปเอง

อ่าน `src/pirateforce_foundation/mob_death.py` (`WIDENING_RULINGS`, `WIDENING_RULING_SCENES`,
`ruling_for`, `rulings_covering`) พร้อมเทสที่ปักไว้ (`tests/test_mob_death.py`) ทั้งสอง ruling ที่
มีอยู่แล้ว (bg0001 `COO-RULING-20260827-1350`, Bg0002 `PANYA-DECISION 2026-08-27T20:10+07:00`)
ใช้ระเบียบวิธีเดียวกันสี่ขั้น:

1. **จดหมายเจ้าของ/COO ตั้งชื่อ** template id เจาะจง หรือ "ทั้งเทเบิล" -- ถ้าตั้งชื่อ "ทั้งเทเบิล"
   ตัวเลขใน `WIDENING_RULINGS` **re-derive จากตารางที่ mine ไว้จริงในเทส** ไม่เคย hand-copy
2. **การคัดกรองทางเทคนิคทำเสร็จแล้วโดยเครื่องมือ mine ก่อนจดหมายจะถูกขอด้วยซ้ำ**: rank>0 AND
   ai_combat!=0 (predicate ความเป็นศัตรู) บวก outfit ต้องเป็นสตริงเดี่ยว ไม่ใช่ variant list
   (";"-joined) -- แถวที่ตกกฎ outfit ไม่เคยเข้า `HOSTILE_PLACEMENTS` เลย คอมเมนต์ของ Bg0002 ruling
   เขียนตรง ๆ ว่า template 27/28/29/30/32/33 ถูกตัดด้วยเหตุผลนี้ ไม่ใช่มีใครอ่านแล้วตัดสินใจเอง
3. **ชื่อ ruling ผูกกับฉากเดียว** ใน `WIDENING_RULING_SCENES` กัน template id ที่ใช้ร่วมกันสองฉาก
   ไม่ให้ได้รับอนุญาตข้ามฉาก
4. **ตัวที่ตกกฎเทคนิคข้อ 2 ไปแล้ว แต่ถูกวางในฉากด้วยกระบวนการอื่น** (Mountain Deer/template 27 ของ
   Bg0002 มาจาก diagnostic object GT-114 ไม่ใช่ mined roster) ได้ ruling แยกของตัวเอง

## วัดกับ 7 template ของ Bg0015 -- ขั้น 1-3 สะอาด, ขั้น 4 ไม่ generalize

```
full_roster_template_ids()             = (343, 345, 348, 350, 353, 355, 924)
  ตรงกับ templates_without_a_death_ruling() เป๊ะ (cross-check ในเทส ไม่ใช่ hand-copy)
overlaps_with_registered_rulings()     = frozenset()   -- ไม่ชนกับ ruling ที่มีอยู่แล้วเลยสักตัว
  (bg0001 ruling คุม {916}, Bg0002 ruling คุม {31,34,35,103})
```

ขั้น 4 ไม่ generalize กับ **template 924 "Carlos" (placement 87)**: Carlos **ไม่ได้ตกกฎเทคนิคข้อ
2 เลย** -- `outfit = P_MALE_033_000_CARLOS` เป็นสตริงเดี่ยว ไม่ใช่ variant list เครื่องมือ mine จึง
เลือกมันเข้า `HOSTILE_PLACEMENTS` ด้วย predicate เดียวกับอีก 6 ตัวเป๊ะ สิ่งที่ทำให้ Carlos ต่างคือ
สิ่งที่เครื่องมือ mine มองไม่เห็นเลย: มี `MOBS_TIP` title และบทพูด NPC -- ค้างเป็นคำถามเปิดจากสอง
จดหมายก่อนหน้านี้แล้ว (`notes_to_chief/20260829_0739_LANE-A-STATUS-lane-B-edit-confirmed-and-
carlos-is-your-call.md` ข้อ ④: "Carlos ควรเป็นมอนหรือ NPC... ยังไม่มีอะไรเสียหายวันนี้"; และ
`src/pirateforce_foundation/scene_identity_rule.py` ของสายนี้เอง จุดที่ 8: "อาจเป็นบอสจริงก็ได้
ยังไม่มีใครดู") **การถอด Mountain Deer ออกจาก ruling ของ Bg0002 จึงไม่ใช่บรรทัดฐานสำหรับถอด
Carlos ด้วยเหตุผลเดียวกัน** -- มันเป็นบรรทัดฐานสำหรับถอดตัวที่ตกกฎเทคนิค ซึ่ง Carlos ไม่ได้ตก
Replay ระเบียบวิธีเดิมแบบกลไกล้วน**ไม่สามารถตอบเองได้**ว่า Carlos ควรได้รับการปฏิบัติแบบเดียวกัน
หรือไม่ -- นี่คือคำถามเนื้อหาใหม่ ไม่ใช่การนำระเบียบวิธีเดิมมาใช้ซ้ำ

ข้อเท็จจริงเชิงกลไกอย่างเดียวที่วัดได้ภายในเทเบิลของ Bg0015 เอง: 6 ใน 7 template มี outfit prefix
`M0` (โมเดลมอนสเตอร์) มีแค่ Carlos ตัวเดียวที่ prefix `P_` (โมเดลผู้เล่น) 🔴 **ไม่ใช่กฎทั่วไป** --
โปรเจกต์นี้ ship ทหารเรือ `P_MALE_002_000_SP1` ที่ตีตายได้อยู่แล้วในที่อื่น
(`scene2_prison_exile_tables.py`) เป็นแค่ข้อเท็จจริงเฉพาะเทเบิลนี้ที่บังเอิญตรงกับตัวเดียวที่มี
คำถามค้างพอดี ไม่ได้เสนอเป็นกฎที่ใช้ตัดสินเนื้อหาได้

## สามทางเลือก

**ทางเลือก A -- คุมทั้ง 7 (รวม Carlos)**: ruling เดียวคุมทุก template ที่ predicate ของ Bg0015
เลือกไว้แล้ว มิเรอร์ bg0001 ("ทั้ง 13 ตัวจริงของ bg0001") และ Bg0002 ("ทั้งเทเบิลของตัวเอง") เป๊ะ
ไม่มีข้อยกเว้นใหม่ นี่คือการ replay ระเบียบวิธีเดิมแบบกลไกล้วน ไม่มีการตัดสินใจเนื้อหาใหม่เลย

**ทางเลือก B -- คุม 6 ไม่รวม Carlos**: คุม `343,345,348,350,353,355` ก่อน แยก Carlos ไว้รอคำตอบ
เรื่องบทบาท รูปร่างเดียวกับที่ Mountain Deer เคยถูกแยก แต่**เหตุผลต่างกัน** ตามที่อธิบายข้างบน --
เสนอเพราะสองจดหมายก่อนหน้านี้ตั้งคำถามเรื่อง Carlos ไว้แล้ว ไม่ใช่เพราะ replay ระเบียบวิธีเดิมได้
คำตอบนี้เอง

**ทางเลือก C -- เลื่อนทั้งหมด**: ยังไม่เคาะสักตัว `[สมมติของสาย B - รอ COO ยืนยัน]` สายนี้เห็นว่า
เป็นทางที่อ่อนที่สุดในสามทาง เพราะ 6 ใน 7 ตัวไม่มีคำถามค้างเลย การเลื่อนทั้งหมดจะดึง 6 ตัวที่ตอบได้
แล้วไปรอด้วยตัวที่ยังตอบไม่ได้เฉยๆ -- แต่เสนอไว้เพราะจดหมายขอ "ทางเลือก" ไม่ใช่คำแนะนำเดียว

## ของที่สร้างไว้ให้แล้ว (ไม่ลงทะเบียน ไม่แก้ `WIDENING_RULINGS`)

`src/pirateforce_foundation/mob_death_bg0015_ruling_proposal.py` (โมดูลใหม่, pure derivation)
มีฟังก์ชัน `full_roster_template_ids()`, `player_body_template_ids()`,
`overlaps_with_registered_rulings()`, `option_a_full_roster()`,
`option_b_roster_minus_carlos()`, `option_c_defer_the_whole_roster()` -- ทั้งหมดอ่านจากตารางที่
mine ไว้จริง ไม่มี hand-typed literal ยกเว้นค่าคงที่ `CARLOS_TEMPLATE_ID = 924` ที่ตั้งชื่อไว้ให้
อ่านง่าย ไม่ import อะไรที่จะแก้ `mob_death.WIDENING_RULINGS` ได้เลย (มีเทสยืนยันว่า dict ไม่
เปลี่ยนหลังเรียกทุกฟังก์ชันในโมดูล) `tests/test_mob_death_bg0015_ruling_proposal.py` (17 เทส
ผ่านหมด) รวม acceptance criterion: stub การเช็คความขัดแย้งของ outfit ให้ข้าม แล้วเทสแดงก่อนแก้กลับ
เขียว ยืนยันว่าจับของจริง

เมื่อ COO เคาะแล้วว่าเลือกทางไหน ขั้นตอนต่อไปคือจดหมายเจ้าของ/COO ที่ตั้งชื่อ ruling จริง (ชื่อที่
ต้อง quote เป๊ะใน `WIDENING_RULINGS`) -- สายนี้ยังไม่ตั้งชื่อ ruling เองในโมดูลนี้ เพราะ
`WIDENING_RULINGS`'s ดอกสตริงเองบอกไว้ว่า "ไม่มี leniency fallback สำหรับ ruling ที่ยังไม่ได้ขึ้น
ทะเบียน" -- โมดูลนี้จึงมีไว้เตรียมข้อมูลให้ตัดสินใจ ไม่ใช่ตัดสินใจแทน

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** จดหมายและโมดูลนี้เป็นข้อเสนอ+ข้อมูล ไม่ใช่การลงทะเบียน ไม่ใช่การ wire อะไรเข้า
`runtime.py`/`app.py` gate 1 (`field_mobs._SCENE_TABLE_MODULES`) ยังปิดเหมือนเดิมตามคำสั่ง (ค)
ที่ห้ามลงทะเบียนรอบนี้โดยเด็ดขาด

## ตัวเลขที่วัดได้

```
full_roster_template_ids()          : (343, 345, 348, 350, 353, 355, 924)  -- 7 ตัว
player_body_template_ids()          : (924,)  -- 1 ตัว (Carlos)
overlaps_with_registered_rulings()  : frozenset()  -- ชนกับ ruling ที่มีอยู่แล้ว 0 ตัว
option_a (full)  : 7 template  |  option_b (minus Carlos) : 6 template  |  option_c : 0
เทสใหม่: 17 passed  |  เทสที่เกี่ยวข้อง (cross-check gates.py/mob_death.py): รวม 119 passed
สวีตเต็ม pirate-force-server (หลังแก้ pinned-inventory 2 เทสที่โมดูลใหม่ทำให้ล้าสมัย):
  6173 passed, 327 skipped, 13141 subtests passed, 0 failed (144.33s)
```

รายละเอียดเต็ม: `rounds/B_20260901_0939_vzhc6s_bg0015-death-predicate-proposal.md` (repo
pirate-force-server, branch `claude/determined-brown-vzhc6s`)

## ยังไม่ได้พิสูจน์

- COO ยังไม่ได้เคาะว่าจะเลือก A/B/C หรือทางอื่น -- ใบนี้ส่งข้อเสนอ ไม่ใช่คำตอบสุดท้าย
- ถ้าเลือก A หรือ B, ข้อความ ruling ตัวจริง (ชื่อจดหมายที่ต้อง quote เป๊ะใน `WIDENING_RULINGS`)
  ยังไม่มี -- ต้องมาจากจดหมายเจ้าของ/COO เอง
- gate 1 ยังล็อกเหมือนเดิม รอคำตอบข้อนี้ก่อนตามที่ COO-DECISION 08:47 (ค) สั่งไว้

## CORE-REQUEST

ไม่มี (รอบนี้ไม่แตะ `runtime.py`/`app.py`)

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `vzhc6s`
