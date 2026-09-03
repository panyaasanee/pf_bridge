ADDRESSEE: COO

LANE-CS round `iazmrv` (สายนี้เกิดจริงรอบนี้เป็นรอบแรก) — ส่งอะไร / ขยับ NOW-M ข้อไหน / ติดอะไร /
nonclaims ตามรูปแบบมาตรฐาน รายละเอียดเต็มอยู่ `rounds/CS_20260904_0453_iazmrv_class-and-starting-skill-catalog.md`

## ส่งอะไร

`pirate-force-server` branch `claude/inspiring-albattani-o1t4t6` @ `f02fbc3` (merge `main` แล้ว
รันชุดเต็มซ้ำเขียว, PR กำลังเปิดรอบนี้) — สารบัญอาชีพ 5 อาชีพที่เลือกได้จริงจาก `CHARCREATE_CLASS`
(`class_catalog.py`) และสารบัญสกิลชุดเริ่มต้น 8 ตัวที่ทั้ง 5 อาชีพอ้างถึงจาก `SKILL_CONTEXT`+`SKILL_TEXT`
(`skill_catalog.py`) ทั้งคู่เป็นสำเนาไบต์ต่อไบต์ของตารางที่คอมมิตใน `pf_bridge/gamedata/tables/` (ไม่ใช่
เลขที่พิมพ์มือ) ผ่านตัวสร้างใหม่ `tools/pf_class_skill_starting_kit_extract.py` ที่รันได้จริง
`--check` กับ `../pf_bridge` สด — เทสใหม่สองไฟล์ (24 เทส/31 subtest) มีเทสการ์ดที่รัน `--check` จริงเพื่อ
จับตารางต้นทางเปลี่ยน ไม่ใช่แค่เทียบ self-hash เดิม ปักไว้ `docs/PYTEST_SKIP_PINS.json` แล้ว

หลักฐานที่วัดจริง: ชุดเต็ม 9267 passed/0 failed, ซ้อมเกตไม่มี `pf_bridge` ข้าง ๆ ผ่านทั้ง
`pytest_subset`+`skip_census` (exit 0 ทั้งคู่), `pf_gate_preflight.py --repo` PASS, `--check` ของ
ตัวสร้างคืน `CHECK OK` จริงกับ `pf_bridge` สด

## ขยับ NOW/M ข้อไหน

คิวเริ่มต้น LANE-CS ข้อ 1 ("สารบัญอาชีพและสกิลจากตารางจริง") — ขยับบางส่วน ไม่ใช่ทั้งข้อ ดูหัวข้อ
nonclaims ว่าทำไมไม่ใช่ "สกิลทุกตัวต่ออาชีพ" เต็มรูปแบบตามที่คิวเขียนไว้ ไม่ขยับไมล์สโตนอื่น (ไม่ใช่เขต
ของสายนี้)

## ติดอะไร / ใครปลด

ไม่มีจุดติด ไม่มี CORE-REQUEST ใหม่รอบนี้ (ยังไม่แตะ `runtime.py`/`app.py`/`gm/`)

## nonclaims (สำคัญ ขอให้อ่านก่อนอ้างว่า "LANE-CS ส่งสารบัญสกิลครบแล้ว")

1. **ไม่ใช่ "สกิลทุกตัวต่ออาชีพ"** — pf-adversary (สั่งต้นรอบ) วัดจริงว่าไม่มีตารางคอมมิตตารางเดียวตอบ
   คำถามนั้นได้: `SKILL_CONTEXT.n_ISCLASS` เป็น bitmask self-referential เฉพาะ 6 แถว "Basic Training"
   เอง (แถว `40000` มี `n_ISCLASS=1` ตรงกับบิตของตัวเองเท่านั้น ไม่ใช่ foreign key ทั่วไปที่ผูกสกิลอื่น
   เข้ากับอาชีพ) · `CONSTDATA_TH__SAILOR_SKILL.tsv` ใช้ id ช่วงเดียวกันแต่เป็นสกิลเรือ คนละโดเมน ·
   `CONSTDATA_TH__CURRICULUM.tsv` ใช้รหัสอาชีพคนละตัว (`n_PPCLASS` ไม่ใช่ `CHARCREATE_CLASS.n_ID`) ·
   เควสสคริปต์ของไคลเอนต์ให้สกิลนอกตารางทั้งหมด (`gamedata/lua/Quest/q_add_skill*.lua`) รอบนี้จึงส่ง
   เฉพาะ **สกิลชุดเริ่มต้น 8 ตัว** ที่มาจาก `CHARCREATE_CLASS.s_SKILL_1..4` เท่านั้น (99/110/111 ร่วม
   ทุกอาชีพ + Basic Training เฉพาะอาชีพ) — ขยาย "สกิลครบทุกตัว" เป็นงาน RE รอบถัดไป
2. **ไม่แตะค่าสถานะ/ความสามารถ** — `s_SCORE` (คอลัมน์ใน `CHARCREATE_CLASS` เอง) ไม่เคยถูก RE
   ความหมายในโปรเจกต์นี้ และ `STANDARD_STATUS`/`STANDARD_BUFF` เป็นเขต LANE-DB ตาม
   `COO-ORDER 20260904_0329` ข้อ 2 (กำลังทำพร้อมกันรอบนี้) — จงใจไม่แตะเพื่อไม่ให้สองสายส่งตัวเลข
   ขัดแย้งกันสำหรับตารางเดียวกัน (`CONSTDATA_TH__POTENTIAL.tsv` ที่ `FUNCTIONAL_COVERAGE.json` อ้าง
   ว่าเป็นตัวเลือกจริงสำหรับค่าความสามารถ มีแต่ header ไม่มีแถวข้อมูล)
3. **ไม่มีอาชีพที่ 6** — `CHARCREATE_CLASS` มี 5 แถวข้อมูลเท่านั้น สกิล `45000`
   (`ICON_Class_Voodooist_s`) เป็นเบาะแสสำหรับ RE รอบถัดไป ไม่ใช่อาชีพที่เลือกได้จริงในข้อมูลชุดนี้
4. **ไม่มี type enum ที่ประดิษฐ์เอง** — `SKILL_CONTEXT` ไม่มีคอลัมน์ basic/attack/AOE/buff/heal/passive
   หรือคอลัมน์ MP จริง (`n_STAMINA_COST` เป็นชื่อคอลัมน์จริง ไม่ใช่ MP) โมดูลรอบนี้ให้ค่าดิบตามชื่อ
   คอลัมน์ของตารางเท่านั้น การจัดหมวดต้องถอด `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` ก่อน ยังไม่ทำ
5. ยังไม่แตะสูตรดาเมจ และยังไม่ทำ Basic attack กับ Training Iron Man จริงบนจอ — คิวข้อ 2/3 ของ
   LANE-CS ยังไม่เริ่ม (โมดูล hypothesis ที่รับโอนมายังไม่ถูกแก้/ยกระดับรอบนี้)

— LANE-CS
