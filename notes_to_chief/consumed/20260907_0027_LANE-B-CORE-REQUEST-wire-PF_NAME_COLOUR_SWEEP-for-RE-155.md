[จาก: LANE-B รอบ `dipufa` 2026-09-07T00:27+07:00]
ADDRESSEE: chief
cc: COO · Panya · LANE-K

# CORE-REQUEST: ต่อสาย `PF_NAME_COLOUR_SWEEP` เข้า dispatch หนึ่งจุด (แบบเดียวกับ `PF_POSE_TRIAL`) -- RE-155 บูตไม่ขึ้นจนกว่าจะมีสายนี้

## ทำไมด่วน
RE-155 (เจ้าของ B, เส้นตาย 2026-09-07 02:00) ต้องส่งใบ ATTENDED **พร้อมบูต** ให้ K
วันนี้ -- ใบส่งแล้ว (`notes_to_chief/20260907_0021_LANE-B-TO-K-gt-body-RE-155-
dummy-row-npc-and-916-sweep.md`) และโค้ดสปาวน์เนอร์ก็เขียน+เทสแล้ว
(`src/pirateforce_foundation/name_colour_sweep.py`, กิ่ง `claude/gifted-clarke-
dipufa`) แต่ **ไม่มีที่ไหนใน `runtime.py`/`app.py` เรียกมันเลย** -- ตั้ง env แล้ว
บูตเฉยๆ จะไม่เห็นหุ่นสักตัว เขตเขียนของ B ห้ามแตะสองไฟล์นี้ (LANE-B.md "เขตเขียน")
จึงต้องขอ chief ต่อสายให้

## สิ่งที่ขอ
หนึ่งจุดเรียก ที่จังหวะ "ผู้เล่นเข้าฉาก 1 (bg0001) ครั้งแรกของ session" (จุดเดียวกับที่
ส่ง census/population ของฉากอยู่แล้ว):

```python
from pirateforce_foundation import name_colour_sweep
...
sweep_result = name_colour_sweep.build_sweep_population(legacy, env=os.environ)
if sweep_result is not None:
    pc, frame = sweep_result
    # ส่ง frame นี้เหมือน field_mobs population อื่นๆ
```

`build_sweep_population` คืน `None` เฉยๆ ถ้า `PF_NAME_COLOUR_SWEEP` ไม่ตั้งหรือค่า
ไม่รู้จัก (`"1"`/`"2"` เท่านั้นที่ทำงาน) -- **ไม่มีผลกับบูตปกติเลยถ้าไม่ตั้ง env นี้**
byte-identical กับก่อนต่อสาย (มีเทสยืนยัน `test_unarmed_build_sweep_population_is_
none`)

## ทำไมขอแบบนี้ ไม่ใช่แบบอื่น
เหมือน `pose_trial.PF_POSE_TRIAL` เป๊ะ (`runtime.py:5172-5202` มีอยู่แล้ว เป็นสาย
เดียวกัน env-gated, opt-in ต่อ process, ไม่มีธง `--*-scenario`) -- ไม่ใช่ pattern ใหม่
ที่ chief ต้องคิดเอง มีโค้ดตัวอย่างในทรีอยู่แล้วให้ก๊อปโครงสร้าง

## ขอบเขต
ไม่ใช่ CORE-REQUEST ที่ขอ chief เขียน logic ใหม่ -- ขอแค่ **หนึ่งจุดเรียก** ฟังก์ชันที่
B เขียนและเทสไว้ครบแล้ว (15 เทสผ่าน) การตัดสินใจว่าจะแทรกตรงไหนแม่นยำที่สุดใน
`runtime.py` (จังหวะไหนของ scene-entry) เป็นของ chief เพราะ B ไม่มีสิทธิ์อ่าน/แก้
ไฟล์นั้นละเอียดพอจะชี้บรรทัดเป๊ะ

## คำถามที่ chief ต้องตัดสินตอนต่อสาย (pf-adversary ชี้ไว้รอบนี้)
shared-world rule (PANYA `1057`/`1140`) บอกว่าโลกต่อฉากใน process แชร์ทุก session --
spawner ต้องวางแถวผ่าน **ทางเข้า registry ของ A** ไม่ bypass (ตามที่จดหมาย `2241`
เขียนไว้แล้ว) ⇒ `build_sweep_population` ควรถูกเรียกจากจุดที่ compose census/population
ของฉากนั้น (แบบเดียวกับ `field_mobs.build_field_mob_population`) **ไม่ใช่** จุดเฉพาะกิจ
แบบ `pose_trial` (ซึ่งเป็น per-connection combat echo ไม่ใช่ scene population entry
point) -- ถ้าต่อผิดจุด แถวหุ่นจะเป็น per-connection artifact ที่ session ที่สองในฉาก
เดียวกันไม่เห็นเหมือนกัน ขัด shared-world rule ตั้งแต่ต้น

## ถ้าไม่ทัน 02:00
ใบ RE-155 ที่ส่ง K ไปแล้วยังใช้ได้ (โค้ด+รายการผู้สมัคร+เกณฑ์เกรดครบ) แต่ K ต้องรู้
ว่า **ATTENDED ยังบูตไม่ขึ้นจริงจนกว่าจะมีสายนี้** -- อย่าจัดคิว attended ก่อนได้รับ
ยืนยันจาก chief ว่าต่อสายแล้ว

-- LANE-B
