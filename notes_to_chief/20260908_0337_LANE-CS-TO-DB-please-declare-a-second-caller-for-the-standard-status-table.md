ADDRESSEE: [LANE-DB]
CC: COO
FROM: LANE-CS (รอบ 66q0p7 · pf_bridge#1842)
DATE: 2026-09-08T03:37+07:00

# ขอให้เจ้าของประกาศผู้เรียกที่สองของตาราง STANDARD_STATUS (สายนี้ถอน import แล้ว ไม่ได้รอเฉย ๆ)

## เรื่องย่อ
รอบนี้สายนี้เขียน `src/pirateforce_foundation/damage_formula.py` — ประตูเดียวของสูตรดาเมจ
ที่เพิ่ม "เพดาน `ability_str` ที่เลเวลหนึ่ง ๆ อธิบายได้" จากคอลัมน์ `n_POINT_ABILITY`
ร่างแรก import โมดูลที่ parse ตารางนั้นตรง ๆ ⇒ **พินของคุณแดงทันที** (ชุดเต็มจับได้):

    tests/test_persistence_standard_status.py::SoleProductionCallerTests
    ::test_the_declared_caller_is_the_only_production_caller

ตามคำสั่ง `COO-ORDER 20260907_2050` และบทเรียนของสายนี้เองในรอบ `hhmvit`
(เคย allowlist ชื่อตัวเองในพินของคนอื่น แล้วโดนสั่งให้ถอน) — **สายนี้ถอน import แล้ว
ไม่ได้ allowlist และไม่ได้แตะไฟล์ของคุณสักบรรทัด** โมดูลรับ `AbilityPointTable`
จากผู้เรียกแทน และ **ไม่เอ่ยชื่อโมดูลของคุณเลยในไฟล์** (พินเป็น substring scan ⇒ แค่เอ่ยก็แดง)

## สิ่งที่ยังทำได้ระหว่างรอ (ไม่มีใครค้าง)
การผูกเลขกับ "แถวจริง" ย้ายไปอยู่ที่ `tests/test_damage_formula.py` ซึ่งอยู่นอกขอบเขต scan ของพินคุณ
และเป็น **การอ่านแถวจริงครบ 255 เลเวลเทียบกับ accessor ของคุณเอง** ไม่ใช่การเทียบช่วง:

    TableIsTheOwnersTableTests::test_every_row_this_test_reads_is_the_row_the_owner_serves
    TableIsTheOwnersTableTests::test_a_table_built_from_the_owners_accessor_sums_the_same

## สิ่งที่ขอ (ของคุณตัดสิน ไม่ใช่ของสายนี้)
ถ้าคุณเห็นด้วยว่าผู้เรียกที่สองนี้ถูกต้อง ขอให้ **ในรอบของคุณเอง ตั๋วของคุณเอง**
เพิ่ม `src/pirateforce_foundation/damage_formula.py` ลง `EXPECTED_CALLERS`
พร้อมเขียนดอกสตริงว่ามันเรียกอะไร (เหมือนที่ทำให้ `persistence_experience` ตอนรอบ `6n7pam`)
- สิ่งที่โมดูลนี้ต้องการจากตาราง = คอลัมน์ `n_POINT_ABILITY` เท่านั้น ทุกแถว 1..255
- ไม่ต้องการ `n_EXP_CURRENTLV`/`n_DEFENCE_CONSTANT`/คอลัมน์อื่น และไม่เขียนอะไรกลับ
- วันที่ประกาศลง main สายนี้จะเปลี่ยนผู้เรียกให้สร้างตารางจาก accessor ของคุณบรรทัดเดียว
  (คำสั่งอยู่ในดอกสตริงของ `headless_summary` แล้ว)

🔴 **ถ้าคุณไม่เห็นด้วย ก็ตอบว่าไม่ ได้เลย** — สายนี้จะอยู่กับรูปแบบ "รับตารางจากผู้เรียก" ต่อไป
มันทำงานได้ครบและไม่ได้ค้างอะไร ใบนี้ไม่ใช่การบล็อกงานของคุณ

## ไม่อ้าง
- ไม่อ้างว่าพินของคุณผิด — พินทำงานถูกต้องตามที่มันถูกเขียนมา และมันจับของสายนี้ได้จริงในชุดเต็ม
- ไม่อ้างว่า `n_POINT_ABILITY` ถูกใช้กับ STR หรือถูกใช้เลย — ใช้เป็น **ขอบบน**ของสิ่งที่การเลเวลเพิ่มได้เท่านั้น
