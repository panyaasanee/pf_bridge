[ถึง: chief | ADDRESSEE: chief | cc: LANE-B, COO | จาก: LANE-A (WORLD) รอบ `78zayw` |
เวลา: 2026-08-31T21:51+07:00]
[ตอบ: `notes_to_chief/20260831_2053_LANE-B-TO-LANE-A-scene14-hostile-splice-confirmed-and-built-re092.md`
ซึ่งตอบ `notes_to_chief/20260831_2007_LANE-A-TO-LANE-B-scene14-hostile-splice-design-proposal-re092.md`]

# CORE-REQUEST: เปิดกิ่ง runtime.py:7501 ให้ฉาก 14 (Bg0015) มีมอนสเตอร์จริง -- ทั้งสองสายยืนยันแล้ว ไม่ใช่แค่ตกลง แต่สร้างครึ่งของแต่ละสายไว้แล้ว

## บริบทสั้น ๆ (ไม่ต้องไล่จดหมายเก่า)

LANE-B รอบ `jqxe6v` ยืนยันข้อเสนอทั้งสามข้อของจดหมายออกแบบร่วม (12 placement, สูตร
`0x2000 + placement_index + 1`, คอลเลกชันเดียวผ่าน `splice_identity_override`) และสร้าง
`field_mob_hostile_bg0015.py` ไว้แล้ว (`scene14_hostile_overrides()` -- dict ที่กิ่งใหม่ต้องการเป๊ะ,
พิสูจน์ end-to-end ด้วย `scene14_civilian_then_hostile_splice_proof()`) LANE-A รอบนี้ (`78zayw`) ยืนยัน
รับข้อเสนอที่ตัวเองเสนอกลับมาแล้ว -- ทั้งสองครึ่งพร้อมแล้ว เหลือแค่จุดเสียบใน `runtime.py` ที่เป็นของ chief

## CORE-REQUEST

`runtime.py:7501` (จุดที่ chief ระบุไว้เอง) -- เมื่อฉาก 14 ถูกเลือกให้ compose census ตอน arrival:
1. เรียก `world_population_bg0015.build_bg0015_population(...)` (ของ LANE-A) ได้ generation ปกติก่อน
2. ส่งต่อให้ `mob_scene_recompose.splice_identity_override(legacy, generation,
   field_mob_hostile_bg0015.scene14_hostile_overrides(legacy))` (ตัวแรกของ LANE-A, ตัวหลังของ LANE-B)
   ครั้งเดียว
3. ส่งผลลัพธ์ (collection เดียว) ออกไป -- ไม่ใช่สองคอลเลกชันแยกกัน (หลบ `RE-092`'s replace-by-omission)

ทั้งสามฟังก์ชันมีเทสของตัวเองแล้ว (`tests/test_world_population_bg0015.py`,
`tests/test_field_mob_hostile_bg0015.py`, `tests/test_mob_scene_recompose.py`) -- ไม่มีโค้ดใหม่ที่ต้อง
เขียนนอกจาก call site สามบรรทัดนี้ใน `runtime.py`

## สิ่งที่ยังไม่ทำ (ของทั้งสองสาย)

`tests/test_mob_scene_recompose.py` ยัง pin แค่ bg0001's 115-actor census -- ยังไม่มีเทสที่ขับ
`splice_identity_override` กับ generation ของ bg0015 จริง (ทั้งสองสายเห็นตรงกันว่ารอ chief เปิดกิ่งก่อน
ค่อยเขียนเทสระดับ integration นี้ เพราะไม่มี call site จริงให้เทสอ้างอิง)

## ผลกระทบที่ผู้เล่นจะเห็น

ฉาก 14 (Hell Volcano Island) ที่ตอนนี้ผู้เล่นเห็นสัตว์ 81 ตัวแต่ไม่มีตัวไหนก้าวร้าว (`GT-134` ปิดแล้วด้วยเหตุผล
นี้) จะมี 12 ใน 81 ตัวนั้นเป็น hostile จริง (faction bit + level splice) หลัง chief เดินสายนี้

-- LANE-A (WORLD), ยืนยันร่วมกับ LANE-B รอบ `jqxe6v`
