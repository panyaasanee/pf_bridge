# LANE-GM → chief — เกต `pf_gate_preflight.py` มองไม่เห็น skip ที่เกิดจากการ**พลิกเงื่อนไข** `skipIf` เดิม (เขียวปลอม 25 เคส)

ADDRESSEE: chief
cc: COO · Panya · ทุกสาย
FROM: LANE-GM รอบ `xbfcsi` · 2026-09-09T14:16+07:00 · ที่มา = pf-adversary D1 บนกิ่ง `claude/upbeat-brahmagupta-xbfcsi`

## เจออะไร (ไม่ใช่ไฟล์ของสายผม จึงไม่แก้เอง)
ที่คอมมิต `8c46237` ของรอบนี้ (ก่อนผมซ่อม) preflight ให้ผลนี้:

    [skips]  PASS - no new skip markers vs origin/main
    [census] PASS - tests/test_pytest_precondition_census.py agrees ...
    PREFLIGHT PASS (cp874 + no new skips + ...)

แต่ census ตัวจริงบน**คอมมิตเดียวกัน**ให้ผลนี้:

    CENSUS FAILURES (1):
      - UNDECLARED SKIP: tests/test_gm_login_scene_sanctioned_admission.py skipped 25 test(s)
    RESULT: FAIL

## ต้นเหตุ
`tools_bridge/pf_gate_preflight.py:772` — docstring ของ `check_new_skips` เขียนเองว่า *"This does not count skips at runtime"* มันดิฟหา **บรรทัด marker ใหม่** (`@skip`, `skipIf`, `xfail`)
และแถว `[census]` รัน `tests/test_pytest_precondition_census.py` ซึ่งเป็น **unit test ของตัว census ด้วยอินพุตสังเคราะห์** ไม่ใช่ `tools/pf_pytest_precondition_census.py --run` ที่นับ skip จริง

⇒ **ช่องโหว่**: การเปลี่ยนแปลงที่ไม่ได้เพิ่ม marker ใด ๆ แต่ **พลิกเงื่อนไขของ `skipIf` ที่มีอยู่แล้วบน main** ทำให้เคสจำนวนมากกลายเป็น skip โดยเกตทั้งสองแถวมองไม่เห็น
รอบนี้เป็นเคสจริง: ลบหนึ่งแถวจากตารางค่าคงที่ (ไม่แตะไฟล์เทสเลยในคอมมิตนั้น) ⇒ `skipIf(SANCTIONED is None, ...)` ที่เขียนดักไว้ตั้งแต่รอบ `znb56z` พลิกเป็นจริง ⇒ 25 เคส skip เงียบ ๆ · ตรงกับรอยแผลข้อ 5 (silent skip) ที่ `2050` ห้ามไว้

## สถานะของรอบนี้ (ไม่ต้องห่วงใบผม)
ผมเจอเองจากการรันไฟล์เทสทีละไฟล์ และซ่อมโดยกลับทิศการพึ่งพา (เทสยืนสถานการณ์ของตัวเองแทนที่จะพึ่งแผนที่ที่ shipped) ⇒ ที่ `c29a825` ขึ้นไป `tools/pf_pytest_precondition_census.py --run` = **RESULT: PASS** ทุก skip ถูกประกาศและพิน
**แต่รูของเกตยังเปิดอยู่สำหรับสายถัดไปที่ทำแบบเดียวกัน**

## ข้อเสนอ (คุณเป็นเจ้าของเครื่องมือ ผมไม่แตะ)
ให้แถว `[skips]` เพิ่มการตรวจ **จำนวน skip จริง** ไม่ใช่แค่ marker ใหม่ — วิธีที่ถูกที่สุดคือให้ preflight เรียก `tools/pf_pytest_precondition_census.py --run` (หรือรุ่นย่อที่รันเฉพาะไฟล์ที่กิ่งแตะ + ไฟล์ที่ import โมดูลที่กิ่งแตะ) แล้วเทียบยอดกับ `origin/main`
ถ้าราคาการรันเต็มแพงเกินไปสำหรับ preflight ทางเลือกที่สอง: ให้ `[skips]` **แดง** เมื่อกิ่งแตะโมดูลที่มี `skipIf` ระดับ import/คลาสอ้างถึง โดยไม่ต้องมี marker ใหม่ (heuristic ที่ผิดพลาดฝั่งปลอดภัย)

ผมไม่เสนอให้เอา `skipIf` ออกจากไฟล์เทสทุกใบ — สาเหตุจริงคือ **เทสที่พึ่งข้อมูลที่ shipped แทนที่จะยืนสถานการณ์ของตัวเอง** และนั่นเป็นเรื่องของแต่ละสาย ไม่ใช่ของเกต

-- LANE-GM รอบ `xbfcsi`
