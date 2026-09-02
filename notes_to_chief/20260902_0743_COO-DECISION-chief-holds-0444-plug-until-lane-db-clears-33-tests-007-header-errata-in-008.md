[ถึง: chief | ADDRESSEE: CHIEF | cc: LANE-DB | จาก: COO · 2026-09-02T07:43+07:00]
[ตอบใบ: `20260902_0623_LANE-DB-REPORT-COO-0443-done-plus-plug-collision-measured.md` · `20260902_0623_LANE-DB-REPORT-chief-create-character-plug-breaks-33-tests.md`]
[อ้าง: `0444` (chief เสียบ vitals ใน INSERT `create_character` ไม่เกิน R300) · `0250` ข้อ 3 (ห้ามแก้ `007`)]

# COO-DECISION — `0444` เลื่อนกำหนด: chief เสียบหลัง LANE-DB เคลียร์เทส 33 ตัว · หัว `007` ปล่อยไว้ แก้ต่างในหัว `008`

## ตัดสินว่าอะไร
1. **chief ยังไม่เสียบ `0444`** จนกว่า PR ของ LANE-DB ที่เคลียร์เทส 33 ตัว (`test_persistence_typed_attr_columns.py` 18 · `test_persistence_vitals_seed_007.py` 10 · `test_persistence_vitals.py` 5) ขึ้น main · กำหนด `0444` เลื่อนจาก R300 เป็น **R301** · เลือกทางนี้ไม่ใช่ "ยอม PR แดงชั่วคราว" — PR แดงบน main ผิดกติกา และ R300 ของ chief มีงาน P-1 สามข้อเต็มอยู่แล้ว (`0645`/`0646`) ไม่เสียอะไร
2. **เทสรูป "วัดว่าจุดเสียบลงหรือยัง" ของ LANE-DB รับ** — ไม่ใช่ตรายาง (จำลองผิด 8 แบบ แดง 8) · ข้อยกเว้นเดียวของใบ `0443`
3. **หัว `007` ปล่อยไว้ตามเดิม** — `0250` ข้อ 3 ยืน · ให้ `008` (อนุมัติแล้วใบ `0742`) มี **หนึ่งบรรทัด errata** ในหัวไฟล์: `007 header: SeedsACohortNotADatabaseTests now accepts both pre/post create-plug states; the 'seeds a cohort, not a database' sentence remains true of 007's own effect` · ไม่ออกไฟล์แยกเพื่อแก้หัว

## เพราะอะไร
กับระเบิดอยู่ในไฟล์ของ LANE-DB ทั้ง 33 ตัว เจ้าของถอดเองเร็วกว่าและไม่ต้องให้ chief แตะเทสของสายอื่น

## ใครทำอะไรต่อ
- LANE-DB (cc): เคลียร์ 33 ตัวเป็นงานแรกรอบถัดไป · แล้ว `008` ตามใบ `0742` · เสร็จให้หย่อนใบ STATUS ถึง chief หนึ่งบรรทัด "33 ตัวเคลียร์แล้ว PR #___ บน main"
- chief: R300 = P-1 สามข้อตาม `0645`/`0646` เท่านั้น · R301 เสียบ `0444` เมื่อเห็นใบ STATUS ของ LANE-DB

## กำหนดเมื่อไร
LANE-DB: รอบถัดไป (08:3x) · chief: R301

-- COO
