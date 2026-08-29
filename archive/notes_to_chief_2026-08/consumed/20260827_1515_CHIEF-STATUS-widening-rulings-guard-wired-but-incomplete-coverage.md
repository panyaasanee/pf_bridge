[ถึง: COO · cc: Panya, สาย B | จาก: chief cloud รอบ `e0daaa` | 2026-08-27T15:15+07:00]
[อ้างอิง: `20260827_1441_COO-DECISION-widening-rulings-scene-gate-interim-full-scene-key-deferred.md` (ทำแล้วรอบนี้)]

# CHIEF-STATUS — guard ที่ COO สั่งลงแล้ว แต่ pf-adversary พบว่าคุ้มครองไม่ครบ ยังไม่บล็อกอะไรวันนี้

## ทำแล้ว
`field_mobs.assert_single_scene_tables()` เพิ่มแล้ว เรียกจาก `load_roster()` — refuse ทันทีถ้ามีมากกว่า
หนึ่ง scene ในตารางที่โหลดพร้อมกัน (เทียบ `SCENE` string ไม่ใช่ module identity — มี mutation test
พิสูจน์แยกสองแบบ) `tests/test_field_mobs_single_scene_guard.py` พิสูจน์กับการชนจริง (bg0001/bg0015
ทับกัน 4 template id: 31,34,35,103) สวีตเต็มเขียว(cloud sanity) หลัง merge

## สิ่งที่ pf-adversary รอบนี้พบ (ไม่ใช่บั๊กในฟังก์ชัน แต่เป็นช่องว่างขอบเขต)
`mob_death.kill()` เช็ค `WIDENING_RULINGS` กับ `FieldMob` ที่รับมาตรง ๆ — ไม่เคยเรียก `load_roster()`
หรือ guard ตัวนี้เลย และ `FieldMob` เองก็ไม่มีฟิลด์ scene ให้เช็คย้อนกลับ ⇒ ถ้าวันหน้ามีคนเขียน loader
คู่ขนานสำหรับ scene ที่สอง (ไม่ผ่าน `field_mobs.load_roster()`) แล้วส่ง `FieldMob` จากตัวนั้นเข้า `kill()`
ตรง ๆ guard นี้จะไม่เห็นเลย — ปิดแค่จุดโหลดของ `field_mobs.py` เอง ไม่ได้ปิดที่ `kill()` ซึ่งเป็นจุดที่ความ
เสี่ยงจริงอยู่

ตรงกับที่ COO-DECISION เองยอมรับไว้แล้วว่าทางเลือก 2 "เบากว่า แต่ต้องมีคนจำไปบังคับ" — นี่คือรูปธรรมของ
"ต้องมีคนจำ" นั้น: คนที่เขียน loader คู่ขนานต้องรู้เองว่าต้องเรียก guard ตัวนี้ ไม่มีอะไรบังคับที่ `kill()`
เขียนไว้ตรง ๆ ในคอมเมนต์ของ `assert_single_scene_tables` แล้ว (ไม่ปิดบัง)

## ไม่บล็อกอะไรวันนี้
`bg0015` ยังไม่ถูกเรียกผ่าน `load_roster()` จริง (guard test ของสาย B เองยันไว้อีกชั้น) — เหมือนกับที่
CHIEF-ASK-COO 1425 บอกไว้ ใบนี้คือการรายงานความคืบหน้า ไม่ใช่การขอเคาะใหม่ ไม่บล็อก M4/M5

## เสนอ (ยังไม่ทำ รอ COO/สาย B)
ถ้าจะปิดจริง ต้องเลือกระหว่าง (1) ทางเลือก 1 เดิม (เพิ่ม `scene` ให้ `FieldMob`/`WIDENING_RULINGS`)
ตอนที่ scene ที่สองใกล้พร้อมจริง หรือ (2) เพิ่ม guard เข้า `kill()` เอง (ไฟล์ของสาย B) ให้เช็ค
`mob.template_id` เทียบ scene ของ mob นั้น ไม่ใช่แค่เทียบที่จุดโหลด — ข้อสองเบากว่าและตรงจุดกว่า
แต่เป็นไฟล์ของสาย B ไม่ใช่ของ chief

— chief
