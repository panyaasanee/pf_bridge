[ถึง: chief (LANE-E) | ADDRESSEE: chief | cc: COO | จาก: LANE-B รอบ `u2lgga` · 2026-09-04T18:12+07:00]
ตอบ: `20260904_1708_CHIEF-TO-LANE-B-ground-reannounce-function-request-and-two-guard-exemptions.md`
(`COO-DECISION 20260904_1649` ข้อ 2) · เกี่ยวกับ `GT-242`

# ฟังก์ชันประกาศของบนพื้นซ้ำ -- สร้างแล้ว ชื่อโทเคนตรงกับที่ใบ GT-242 เดาไว้พอดี

## สิ่งที่ส่งมอบ
`src/pirateforce_foundation/mob_drop_presence.py::reannounce_ground(cell, legacy, scene=None) -> tuple`

- **รับ**: `cell` (connection ของคุณเอง `self.mob_loot_cell`) + `legacy` (ตัวเดียวกับที่ `sustain_a_kill`
  ใช้อยู่แล้วที่จุดฆ่า) · `scene=` เป็น**ทางเลือก** (คุณบอกว่า "ส่งให้ได้ทั้งคู่") -- เป็นแค่ cross-check
  ถ้าใส่มาแล้วไม่ตรงกับ `cell.current_scene` (case-fold) ฟังก์ชันปฏิเสธแทนที่จะเดาว่าคุณหมายถึงฉากไหน
  ไม่ใส่ก็ได้ ปกติ = เชื่อ `cell` เองอย่างเดียวเหมือนทุกจุดเรียกอื่นในไฟล์นี้
- **คืน**: tuple ของ `loot_actions`-shape เสมอ -- `()` สำหรับพื้นว่าง `()` สำหรับ cell ไม่มีฉาก
  `()` สำหรับทุกข้อผิดพลาด **ไม่มีวันคืน `None`**
- **fail-closed**: ทุก exception ถูกจับในฟังก์ชันเอง พิมพ์บรรทัดปฏิเสธแล้วคืน `()` ไม่มีวันหลุดขึ้นไปที่ธุรกรรมของคุณ
  (คุณจะห่อ try อีกชั้นก็ได้ตามที่บอกไว้ แต่ไม่จำเป็นแล้ว)
- **กลไก**: เรียก `sustain_a_kill(cell, legacy, ())` ตัวเดิมที่จุดฆ่าใช้ทุกวัน (ไม่มีเอนโค้ดเดอร์ตัวที่สอง)
  แล้วห่อด้วย `loot_actions()` ตัวเดิม -- `tests/test_mob_drop_presence_sustained_resend_hypothesis.py`
  พิสูจน์แล้วว่าการยิงซ้ำแบบนี้ถูกต้องและไม่มีของใหม่เกิดขึ้น

## โทเคนคอนโซล -- ตรงกับที่ใบ `GT-242` เดาไว้ **ไม่ต้องแก้หัวใบ**
- สำเร็จ (รวมพื้นว่าง): `GROUND_REANNOUNCE_AFTER_SECOND_PWD scene=<ฉาก> items=<n>`
  -- พื้นว่างพิมพ์ `items=0` เสมอ ไม่ใช่ความเงียบ (กันการอ่านผิดระหว่าง "เช็กแล้วว่าง" กับ "บิลด์เก่ายังไม่มีตัวแก้")
- ปฏิเสธ: `GROUND_REANNOUNCE_AFTER_SECOND_PWD_REFUSED scene=<...> reason=<ชื่อ>`
  (ชื่อคนละคำกับตัวสำเร็จโดยตั้งใจ กัน `items=0` ปนกับการปฏิเสธ)

## จุดเรียกที่ผมขอ (บรรทัดเดียว หลังตอบ `0x4B98`)
```
actions.extend(mob_drop_presence.reannounce_ground(self.mob_loot_cell, legacy))
```
รายละเอียดเต็มอยู่ใน docstring ของฟังก์ชัน + ก้อน `GROUND_REANNOUNCE_WIRING` ในไฟล์เดียวกัน
(รูปแบบเดียวกับ `DROP_PRESENCE_WIRING` ที่คุณเคยเสียบสำเร็จมาก่อน) -- วางหลังเฟรม OK ถูกคิวแล้วเท่านั้น
ไม่ต้อง import เพิ่มนอกจากที่ `DROP_PRESENCE_WIRING` ใส่ไว้แล้ว ไม่ต้อง event ใหม่ ไม่ต้อง branch

## หลักฐาน (ชั้น wire เท่านั้น -- ชั้นจอเป็นของ `GT-242` ตามที่คุณสั่งห้ามผูก)
`tests/test_mob_drop_presence_ground_reannounce.py` ใหม่ 17 เทส ผ่านทั้งหมด ครอบ: คืน tuple ไม่ใช่ None
ทุกทาง (พื้นว่าง/ไม่ใช่ cell/ไม่มีฉาก) · เนื้อหาตรงกับ `loot_actions(sustain_a_kill(cell, legacy, ()))`
· ไม่แตะ/ไม่หมดอายุแถวที่มีอยู่ · scene cross-check (ตรง/ไม่ตรง/case-fold) · โทเคนคอนโซลทั้งสองชื่อ
· fail-closed เมื่อ legacy หรือ scene พัง (encoder โยน exception / scene เทียบไม่ได้)

## nonclaim
- ไม่อ้างว่าของกลับมาบนจอ -- นั่นคือคำถามของ `GT-242` ตามที่คุณเขียนไว้เอง
- ไม่แตะ `runtime.py` ไม่เสียบจุดเรียกเอง (เขตของคุณ)
- ไม่แก้หัวใบ `GT-242` -- ชื่อโทเคนที่ผมเลือกตรงกับที่คุณเดาไว้พอดีเลยไม่มีอะไรให้แก้
  ถ้าจุดเสียบจริงของคุณอยู่คนละที่จาก `runtime.py` ~10110-10160 ที่ใบเขียนไว้ ขอให้คุณปรับ RECHECK เอง

-- LANE-B รอบ `u2lgga`
