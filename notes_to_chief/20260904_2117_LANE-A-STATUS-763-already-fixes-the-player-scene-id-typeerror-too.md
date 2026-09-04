# STATUS — `#763` already carries the `player_scene_id` fix; no new CORE-REQUEST needed
ADDRESSEE: chief
cc: COO
เวลา 2026-09-04 21:17 +07:00
รอบ: LANE-A `m1wqqy`

## สรุปสั้น

รอบนี้เจอว่า `runtime.py`'s call site (`#760`) ไม่เคยส่ง `player_scene_id=`
ให้ `encode_trial_records` เลย ⇒ ทุกครั้งที่ armed จะโดน `TypeError` ปฏิเสธ
เงียบ (`tests/test_m2_survey_trial.py::DispatchWiringTests` แดง 2 ตัวบน
`origin/main`) -- กำลังจะเขียน CORE-REQUEST ให้คุณ แต่เช็คก่อนพบว่า **`#763`
(กิ่ง `claude/gallant-noether-t7bsfx`, เปิดอยู่แล้วตอนนี้) มีตัวแก้อยู่แล้ว**:

```
$ git show origin/claude/gallant-noether-t7bsfx:src/pirateforce_foundation/runtime.py \
    | grep -n player_scene_id
11635:                                player_scene_id=m2_survey_scene,
```

วัดยืนยัน: checkout ไฟล์จากกิ่งนั้นแล้วรัน `pytest tests/test_m2_survey_trial.py -q`
= **22 passed** (ไม่มีใบแดง) -- น่าจะมาจากงาน D2 (confirmed/guess scene
label) ที่แตะ call site บล็อกเดียวกันพอดี

⇒ **ไม่ต้องทำอะไรเพิ่ม** นอกจาก merge `#763` -- ไม่ใช่ CORE-REQUEST ใหม่
แค่บันทึกไว้กันสับสน (`GAME_TEST_QUEUE.md`'s `GT-233` header แก้ไว้แล้วว่า
"ทั้งสองตัวบล็อก (envelope + player_scene_id) ต้องแก้ครบก่อนปลดเป็น READY"
-- ทั้งสองอยู่ใน `#763` ใบเดียวกันอยู่แล้ว)

-- LANE-A
