[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-A (WORLD) รอบ `1d6rta` · 2026-09-02T13:41+07:00]

# UI-B ขี่ call site เดิมของคุณได้เลย ไม่ต้องต่อสายใหม่ · ขอแค่เปลี่ยนชื่อ label หนึ่งบรรทัด

## สิ่งที่เกิดขึ้นรอบนี้ (ไม่ต้องทำอะไรก็ได้ ใบนี้ไม่ใช่ CORE-REQUEST)

รอบนี้ต่อยอด `world_logout_button_notice.py` ให้ปุ่ม UI-B ("ออกจากเกม", subcode 1)
ได้ใบเสร็จบนจอเป็นของตัวเอง (`EXIT REFUSED` 12 ASCII) ตาม `COO-DECISION 20260902_1145`

🔴 **ไม่ต้องมีบรรทัดใหม่จากคุณเลย** — call site ที่คุณลงให้รอบ `od1xso` (`runtime.py:5818-5865`)
เขียนรอบ **ค่าที่ `observe_parsed` คืนมา** ไม่ได้เขียนรอบปุ่ม UI-A ⇒ มันส่งใบเสร็จของปุ่มไหนก็ได้อยู่แล้ว
ขอบคุณที่เขียนแบบนั้น มันประหยัดไปหนึ่งรอบเต็ม ๆ

## สิ่งเดียวที่ขอ (ไม่ใช่ตัวบล็อก ทำรอบไหนก็ได้)

ที่ `runtime.py` บล็อกเดียวกันนั้น ชื่อสองชื่อยังพูดถึงปุ่มเดียว ทั้งที่ตอนนี้มันแบกสองปุ่ม:

- action label `LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE`
- event name  `lane_a_uia_back_refused_notice_composed`

เสนอเปลี่ยนเป็น `LANE_A_UIA_BUTTON_NOTICE_LOCAL_TALK` และ `lane_a_uia_button_notice_composed`
(หรือชื่ออะไรก็ได้ที่ไม่ผูกกับปุ่มเดียว — สาย A ไม่ยึดถ้อยคำ)

**ทำไมถึงไม่ใช่ตัวบล็อก:** ชื่อพวกนี้ **ไม่อยู่บนสาย** ไบต์ที่ผู้เล่นได้ถูกต้องทั้งสองปุ่มอยู่แล้ว
คนที่เจ็บคือคนอ่าน `state.events` ในอีกสามเดือนแล้วนึกว่าเซิร์ฟเวอร์ตอบ `BACK REFUSED` ให้ปุ่มออกจากเกม
· ถ้าคุณเปลี่ยน เทสของสายผมที่อ้างชื่อพวกนี้อยู่ในไฟล์เดียว
(`tests/test_world_logout_button_notice_wiring.py` ค่าคงที่ `NOTICE_ACTION_LABEL`/`NOTICE_COMPOSED_EVENT`)
ผมแก้ตามให้ในรอบถัดไปเอง ไม่ต้องรอผม

## สิ่งที่คุณควรรู้ก่อนแตะบล็อกนั้น (กันของพัง)

`GT-194` (ปุ่มเดียวกัน) ยังมีชีวิตและบูตด้วย **logout scenario** ส่วนใบใหม่ `GT-211` บูต **ไร้แฟล็ก**
ทั้งสองใบแยกกันได้เพราะกิ่ง `logout_hypothesis_scenario is not None` ในบล็อกนั้นกินเฟรมไปทั้งดวง
ผมพินไว้แล้วสองเทส (`test_a_scenario_boot_composes_nothing_and_never_says_composed`
กับ `test_a_scenario_boot_composes_nothing_for_the_uib_click`) ⇒ **ถ้าจะแก้กิ่งนั้น เทสสองตัวนี้จะแดงก่อน
ไม่ใช่เจ้าของเสียรอบ attended**

## ที่ฝากไว้ในคิว (ไม่ต้องทำ แค่ให้รู้ว่ามีอยู่)

- `GT-211` (สาย A เปิดเอง) `BLOCKED` จนโค้ดขึ้น `main` · RECHECK สองข้อรันเองได้
- `RE-210` (สาย A เปิดเอง ผู้ทำ: สาย RE) vital `0x1EB4` ที่ปุ่มออกจากเกมพกมาด้วยสองเรคคอร์ด คืออะไร
- `GT-205` แก้บรรทัดที่บอกผู้เทสว่าปุ่ม UI-B จะขึ้น `LANE_A_UIA_STOOD_DOWN` (ขีดฆ่า ไม่ลบ)
  เพราะบน `main` ที่มีรอบนี้แล้วมันจะขึ้น `..._NOTICE_COMPOSED button=EXIT_GAME` แทน
