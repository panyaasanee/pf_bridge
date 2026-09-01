[ถึง: chief | ADDRESSEE: chief | จาก: LANE-DB รอบ `ovwiwo` · 2026-09-01T20:50+07:00]

# LANE-DB STATUS -- sparse compose **ยังไม่อยู่บน `main`** PR #503 ถูกปิดที่ช่อง `skip_census`

## ทำไมใบนี้เร่งด่วนกว่าที่ดูเหมือน

`FROM_CHIEF R292` ข้อ 3 บอกว่า `CORE-REQUEST-GM-049` รอ COO เคาะ
`attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED` อย่างเดียว แล้ว "chief ต่อสายให้ทันที"

🔴 **ถ้า COO เคาะแล้ว chief ต่อสายทันทีตอนนี้ จะต่อไม่ติด** เพราะฟังก์ชันที่ใบ `1716` บอกให้เรียก
**ยังไม่มีอยู่บน `main`** ทั้งสองตัว:

- `store.write_typed_attributes_and_compose_sparse`
- `persistence_attr_compose.compose_sparse_block`

ยืนยันได้ตรง ๆ ก่อนเชื่อใบนี้:

```
git show origin/main:src/pirateforce_foundation/persistence_attr_compose.py | grep -c sparse   # 0
git show origin/main:src/pirateforce_foundation/store.py | grep -c compose_sparse              # 0
```

ใบ `1716` ของสายนี้บอกให้ LANE-GM รอจนกว่าจะขึ้น `main` -- คำนั้นยังใช้ได้อยู่ ยังไม่ถึงเวลา

## สถานะจริง

| PR | ผล | ช่องที่แดง |
| --- | --- | --- |
| #495 (รอบ `9zvic2`) | closed unmerged | `pytest_subset` -- handle รั่วบน Windows |
| #503 (รอบ `u2wgzc`) | closed unmerged | `skip_census` -- `skipTest` ที่ไม่ได้ประกาศ |
| รอบนี้ `ovwiwo` | PR เปิดใหม่ | -- |

รอบ `u2wgzc` **แก้เหตุของ #495 ได้จริง** เกตรัน `pytest_subset exit=0 GREEN`
`5515 passed, 65 skipped, 11862 subtests passed` บน Windows จริง (run `33505566615`)
แล้วตายที่ช่องถัดไปด้วยเหตุใหม่

รอบนี้: โค้ดโมดูลกับไฟล์เทสอีกสองไฟล์ **byte-identical** กับรอบนั้น (ตรวจด้วย `sha256sum` ทั้งสาม)
ที่แก้คือไฟล์เทสไฟล์เดียว 54 บรรทัด: เอา `skipTest` ออก แล้วให้เทสยืนยันสัญญาคนละข้อบนสองแพลตฟอร์ม
`tools/pf_pytest_precondition_census.py --run` บนเครื่องนี้ ⇒ `RESULT: PASS`
และโมดูลของสายนี้ไม่ปรากฏในสำมะโนอีกเลย

## ที่ chief ต้องทำ (สองข้อ ทั้งคู่เล็ก)

1. **`GT-193` ยังเป็น `PENDING interface` ต่อไป** ตอบคำถามข้อ 1 ของใบ `1750` ซ้ำอีกรอบ -- คำตอบยัง
   เหมือนเดิมเพราะเหตุผลเดิมยังจริง ไม่ต้องเปลี่ยนอะไร ผมจะแจ้งเมื่อ merge จริง ไม่แจ้งก่อน
2. **ถ้า COO เคาะ `GM-049` ก่อน PR รอบนี้ merge** ⇒ อย่าเพิ่งต่อสาย รอ merge ก่อน มิฉะนั้น
   runtime.py จะอ้างชื่อที่ยังไม่มี ผมจะเขียนใบแจ้งทันทีที่ยืนยันบน `main` ได้ด้วย `git show` สองบรรทัดบน

## nonclaims

- **ไม่อ้างว่าเกตรอบนี้จะเขียว** อ้างได้แค่ว่าเหตุของรอบก่อนถูกวัดแล้วว่าหายไป และไม่มี skip
  ตัวใหม่ในโมดูลของสายนี้เลยทั้งบน Linux และใต้เงื่อนไข "ไม่มี `/proc`" ที่จำลอง
  เกตทำอย่างอื่นอีก 21 อย่างบน Windows จริงที่เครื่องนี้รันแทนไม่ได้
- **ไม่อ้างว่า `/speed` ทำงาน** ไม่มีใครนอกเทสเรียกโค้ดนี้ · `UPDATE_ATTR_VITAL_VERSION_CONFIRMED`
  ยังเป็น `None` · ครึ่งของ LANE-GM ยังไม่ต่อ
- **ไม่อ้างว่า client ปล่อยฟิลด์ที่ไม่ได้ส่งไว้เฉย ๆ** นั่นคือสิ่งที่ `GT-193` วัด ไม่ใช่สิ่งที่ PR นี้ตอบ
- **ไม่มี migration ไม่มี backfill ไม่มีค่า seed** คอลัมน์ typed ทุกตัวยังอ่านได้ `NULL`
  ⇒ `COO-DECISION 20260901_1447` ข้อ 2 (ห้าม seed ก่อน RE ตัดสิน 150.0 vs 400.0) ไม่ถูกแตะ
- `speed_walk` ยังเข้ารหัสการระบุ `BasicAttr+0x54` ของ player object ที่ยังไม่พิสูจน์ (RE-193 เดินขนานไป)
