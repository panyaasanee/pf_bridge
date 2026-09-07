[จาก: COO รอบ `2342` | 2026-09-07T23:42+07:00 | ส่งต่อ PANYA-ORDER `20260907_2325` + ภาคผนวก `20260907_2350` คำต่อคำ]
ADDRESSEE: LANE-B
cc: LANE-K · LANE-GM · chief (LANE-E) · ka1-A · Panya

# คำสั่ง: งานแรกรอบถัดไป = ขยาย `pirate-force-server#1077` เป็นสวีป **ALL / ALL-NOID** (26 ป้าย · ลาน Iron Man · โลกว่าง · `n_ENEMY` 7 ค่า)

## ตัดสินอะไร — เจ้าของเคาะเอง COO ส่งต่อไม่ขยายไม่ตัด (คำเจ้าของอยู่ในใบ `2325`/`2350`)
1. **PR เดียว = `#1077` เดิม ขยาย** · env `PF_NAME_COLOUR_SWEEP=ALL` = ทุกแถว · `=ALL-NOID` = ทุกแถวยกเว้นกลุ่ม identity (B และ F) · ชุด 1/2/3 เดิมคงไว้
2. แถว (B ตรวจความเป็นไปได้เอง แถวไหนประกอบไม่ได้ = เขียนเหตุผลในใบ **ห้ามเงียบ**):
   ตัวควบคุม `N-BASE` `M-BASE` · A body 5 (`N-LVL N-HP N-SPD N-TPL N-PRE`) · B identity 3 (`N-ID0` `N-IDNEG` `M-IDNEG`) · C linked identity 2 (`N-LNKP` = identity ผู้ดู ประกอบตอน census · `N-LNKS` = ตัวเอง · ใช้ `mob_viewer_link` ที่มีอยู่) · D `n_ENEMY` 7 (`N-ENM0 N-ENM1 N-ENM2 N-ENM6 N-ENM12 N-ENMFF M-ENM1` — ถ้าเจอตารางบอกโดเมนจริงให้ใช้ค่าจริงแทน) · E ตาย 2 (`M-DEAD` `N-HP0`) · F ผสม 4 (`N-IDNEG-LNKP` `N-IDNEG-ENM1` `M-IDNEG-DEAD` `N-ID0-LNKP`) = 25 · **+ `M-T001` ของคุณ (ใบ `2245`) = 26** (COO เพิ่ม — ดู `COO-DECISION-b2245`) · ALL-NOID = 19
3. **ตำแหน่ง** (`2350` ข้อ 1): แนวหุ่น Training Iron Man `field_mob_tables.TOWN_TARGET_PLACEMENTS` (bg0001) · เริ่ม X `11800` +150/ป้าย · Y `9340` · Z จริงจากแถวหุ่นเดิม (≈`2200.46`) · แยกสองแถวได้ Y ห่าง 300 · `_spawn_anchor` ท่าเรือ**ไม่ใช้**กับ ALL · ป้าย ASCII ≤12 ตัว · พิมพ์พิกัดทุกป้ายใน `HEADLESS_PROOF:`
4. **โลกว่าง** (`2350` ข้อ 2): โหมด ALL/ALL-NOID census Port Royal 108 + Iron Man 4 **ไม่ส่ง** · โทเคน `NAME_COLOUR_SWEEP_ARMED actors=26 census_actors=0 wire=26` (ALL-NOID `actors=19 wire=19`) · env ว่าง = sha census เท่า main เหมือน `2117` · บันทึก nonclaim ว่าบูต ALL ไม่เทียบกับเมืองจริง (ตัวควบคุมในแถวทำหน้าที่แทน)
5. ตอบข้อ 4 ของ `2350` (identity บวกทุกค่าไม่ต้องสวีป — จุดแบ่งเดียวคือ ≤0) ไว้ในใบ gt-body ให้ K พับ
6. ส่ง `LANE-B-TO-K-gt-body-*` แบบใบ `2117`: `ATTENDED:` + `HEADLESS_PROOF:` + เกณฑ์อ่านผล (ป้ายไม่เขียว/ชมพู · ไม่วาด · client ล้ม = **ผลที่บันทึกได้** ไม่ใช่บูตล้ม · ล้มที่ ALL → ka1-A บูต ALL-NOID ต่อทันที) · **ห้ามรอ chief** · marker ใส่เองเมื่อ adversary คืน (§7 เดิม)

## เส้นตาย · โทเคนตรวจ
PR เขียวบน main **≤2 รอบของ B** (~03:00 8 ก.ย.) · โทเคน = `git log origin/main --grep 'name colour' ` เจอ `#1077` merge + ใบ `*LANE-B-TO-K-gt-body-*` หลัง `2342` · ระหว่างนี้ **นาฬิกา `GT-300` หยุด 1 รอบ B** (COO ลง NOW) · `name_tokens`/`GT-300` ต่อหลัง PR ALL ขึ้น main

## ไม่ได้เคาะ (อย่าขยาย)
`0159`/`HEADLESS_PROOF` คงเดิม · ไม่แก้เกตสีของ GM จนมีผลจอ · ไม่ตัดสินผู้สมัคร · ไม่แตะ census production · ไม่ตั้งเวลาเปิดเครื่อง

## ถ้าผิดต้องย้อน
ถอด env ALL/ALL-NOID = ชุด 1-3 ทำงานเหมือน `2117` · แถวเดี่ยวถอดได้ทีละแถวไม่กระทบแถวอื่น

-- COO รอบ `2342`
