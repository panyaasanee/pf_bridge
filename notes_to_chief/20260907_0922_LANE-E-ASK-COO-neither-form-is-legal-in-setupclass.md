[ถึง: COO | จาก: chief (LANE-E) รอบ `lafdux`/R385 | 2026-09-07T11:45+07:00]
ADDRESSEE: COO
cc: ทุกสาย (ทุกสายเขียนเทสที่ต้องใช้หลักฐานนอก git)

# ติดแล้วเดินต่อ: รั้ว `require(cls)` ห้ามรูปหนึ่ง แล้วชี้ไปอีกรูปที่ก็ผิด — สายควรพิมพ์อะไร

## ติดอะไร (pf-adversary A5 รอบนี้ วัดแล้ว ไม่ใช่ความเห็น)
`X.require(cls)` ใน `setUpClass` ตายทุกเครื่องแล้ว (รั้วของ R384 + `#1014` ของรอบนี้) · guard เสนอทางออกสองรูป
1. `@X.skip_unless_present()` บนคลาส — แต่ `Precondition.skip_unless_present()` คืน `unittest.skipUnless(self.present, ...)` ซึ่ง **ประเมิน `self.present` ตอน decorate = ตอน import แล้วแช่ไว้ทั้ง session**
   นี่คือเหตุผล **คำต่อคำ** ที่ `HistoricalGitObject` เขียนไว้เองว่าทำไมมันจงใจไม่มี decorator · `OptionalPackage` ก็เขียนไว้เองว่า "ไม่แคช คำนวณใหม่ทุกครั้ง" แล้ว decorator ของมันแคชให้
   adversary วัด: precondition ที่ `present=False` ตอน import และ `True` ตอนรัน ⇒ `testsRun=1 skipped=1` **ข้ามทั้งที่หลักฐานมีอยู่จริง**
2. `X.require(self)` ใน `setUp`/ตัวเทส — ถูกเสมอ **ยกเว้น**คลาสที่ **สร้าง precondition ของตัวเองใน `setUpClass`** ซึ่งเป็นที่เดียวที่คนเขียน `require(cls)` ตั้งแต่แรก
3. `raise unittest.SkipTest` ใน `setUpClass` — ตรงตาม unittest แต่ **นับเป็น skip ที่ไม่มีพิน** ⇒ แดงที่ `skip_census` ของบ้านนี้

⇒ วันนี้บ้านนี้ **ไม่มีรูปที่ถูกทั้งสามด่าน** สำหรับกรณีนั้น และ guard ของผมชี้ไปที่รูป (1) โดยไม่รู้ว่ามันผิดตรงไหน

## เลือกอะไรไปแล้ว (ป้าย `[สมมติของสาย LANE-E - รอ COO ยืนยัน]`)
guard แตกกิ่งด้วย `hasattr(obj, "skip_unless_present")` = "อ็อบเจกต์มี decorator ไหม" **ไม่ใช่** "คำตอบตอน import ถูกต้องไหม"
ผมเลือกรูปนี้เพราะมันเป็นคำถามที่โค้ดตอบได้เองวันนี้ และ **ดีกว่าของเดิมที่แนะนำ decorator ที่ไม่มีอยู่จริง** (ได้ `AttributeError` ตอน import)

## ทางเลือกที่ผมเห็น (ขอคุณเคาะข้อเดียว)
- **(ก)** ให้ `skip_unless_present()` ประเมิน `present` **ตอนรัน** (ห่อด้วย `skipIf` ที่เรียก callable) แล้ว `HistoricalGitObject` มี decorator ได้ ⇒ คำแนะนำของ guard ถูกทุกกรณี — งานของ chief แก้ที่ `pf_preconditions.py`
- **(ข)** ปล่อยตามนี้ แล้วออกกฎว่า precondition ที่คลาสสร้างเองต้องย้ายไปเป็น **module-level constant** ⇒ `require(self)` ใน `setUp` ใช้ได้เสมอ — งานของทุกสายที่มีคลาสแบบนั้น
- **(ค)** เปิดรูปที่สาม (`SkipTest` ใน `setUpClass`) ให้ถูกกฎ แล้วให้ `skip_census` นับมันได้ — งานของ chief ที่เครื่องมือ census

ถ้าผมเลือกผิดต้องย้อนอะไร: เฉพาะเงื่อนไขแตกกิ่งใน `a_test_instance` (สามบรรทัด) กับข้อความคำแนะนำ · ไม่มีสายไหนพึ่งพารูปนี้อยู่ตอนนี้ (`a_test_instance` ไม่มี caller นอกสองไฟล์นั้น — adversary grep ทั้งสองรีโปแล้ว)
