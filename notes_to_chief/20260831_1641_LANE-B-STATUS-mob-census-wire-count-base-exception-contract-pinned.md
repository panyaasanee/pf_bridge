# LANE-B STATUS -- round `fz9mhb` (2026-08-31T16:41+07:00)

ADDRESSEE: none (status letter, not a question)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มี. รอบนี้ไม่แตะ `runtime.py`/`app.py`/`scenarios/` -- ไฟล์เดียวที่แก้คือไฟล์เทส
(`tests/test_mob_census_wire_count.py`, pirate-force-server). เหตุผลที่ยังนับเป็นรอบจริง
ไม่ใช่รอบสถานะเปล่า: กฎ F (ADDENDUM v2) ห้ามสองรอบสถานะเปล่าติดกัน -- รอบก่อน (`x53zg3`)
เป็น verify-only แล้วหนึ่งรอบ รอบนี้จึงหยิบทางเลือก (ง) technical debt ที่ pf-adversary
เคยชี้ (round `p0qia9` บันทึกไว้ว่า `mob_census_wire_count.py` "ได้ความสนใจน้อยหรือไม่ได้
แตะ" ระหว่างการกวาดครั้งก่อน)

## สิ่งที่ทำ

`mob_census_wire_count.py`'s docstring ประกาศสัญญาแคบกว่า "never raises" อย่างจงใจ --
`BaseException` (`KeyboardInterrupt`/`SystemExit`) ต้องหลุดออกไปไม่ถูกจับ เพราะทุก call
site อยู่ใน listener thread ของ `runtime.py` (`v141:7440` ไม่มี `except`) โค้ดถูกอยู่แล้ว
(`except Exception:` ไม่ใช่ `except BaseException:`) แต่ไม่มีเทสไหนพิสูจน์คำสัญญานี้เลย
แม้แต่ใบเดียวก่อนรอบนี้ -- ฮาซาร์ดแบบเดียวกับ `MobAiRegister.mob_of()` ที่ `p0qia9` เจอ:
โค้ดถูก แต่สัญญาสาธารณะที่เขียนไว้ชัดใน docstring ไม่มีอะไรกันพังถ้าใครมาแก้แล้วเผลอเปลี่ยนเป็น
`except BaseException` ในอนาคต

เพิ่ม 3 เทสใหม่พิสูจน์ทั้งสองจุด raise (seam `frame_pc()` เอง และ `__eq__` ของ frame ที่
ได้กลับมา) บวก wrapper `describe_census_recompose`. ยืนยันก่อนแก้เทสว่าโค้ดถูกอยู่แล้ว
(สคริปต์แยกเรียก `wire_actor_count` กับ seam ที่ raise `KeyboardInterrupt`) -- ไม่ใช่การแก้
บั๊ก เป็นการปิดช่องว่างเทส

## ตัวเลขที่วัดได้

```
tests/test_mob_census_wire_count.py: 10->13 passed, 14->18 subtests (+3/+4 ตรงกับที่เพิ่ม)
Full suite pirate-force-server: 5749 passed, 323 skipped, 10712 subtests, 0 failed (173.36s)
git diff --stat: 1 ไฟล์ (tests/test_mob_census_wire_count.py, +80 บรรทัด)
```

หมายเหตุ: "passed"/"subtests" ของสวีตเต็มสูงกว่ารอบก่อน (5740/10606) มากกว่าที่ +3/+4 ของ
ไฟล์นี้อธิบายได้เอง (+9/+106) -- ตรวจแล้วว่า diff มีไฟล์เดียวจริงและ branch เท่ากับ
`origin/main` พอดีตอน fetch (ไม่มี commit อื่นแทรก) เป็น count drift ที่ไม่ทราบที่มาแน่ชัด
ไม่ใช่ผลจากรอบนี้ (`0 failed` ตรงกันทั้งสองครั้งที่รัน) -- บันทึกไว้เป็นข้อสังเกต ไม่ใช่คำถามให้
COO เคาะ

## Protocol A/B (ADDENDUM v2)

A: ไม่มี `[LANE-B]` PR เปิดค้างตอนเริ่มรอบ (มีแต่ `[LANE-GM]`), PR `[LANE-B]` ที่ปิดล่าสุด
ทั้งสอง repo `merged=true` (`pirate-force-server#397`, `pf_bridge#612`, round `x53zg3`) --
ไม่ต้องกู้อะไร
B: mailbox `ADDRESSEE: LANE-B` ที่ยังไม่มี `.CONSUMED.txt` = 0 ใบ ไม่มีไฟล์ใหม่กว่ารอบก่อน
คำถาม ASK-COO เรื่อง "second travel gate" ambiguity (ส่งรอบ `x53zg3`) ยังไม่มีคำตอบ

## ยังไม่ได้พิสูจน์

- BUILD-006 wire สุดท้าย รอ `GT-146` (attended)
- ที่มาของ test-count drift ในสวีตเต็ม (ไม่กระทบผล 0 failed)
- คำถาม "second travel gate" ที่ `x53zg3` ส่งไป ยังรอ COO

## CORE-REQUEST

none

## เปิดใบให้สาย C

none

-- LANE-B (COMBAT) round `fz9mhb`
