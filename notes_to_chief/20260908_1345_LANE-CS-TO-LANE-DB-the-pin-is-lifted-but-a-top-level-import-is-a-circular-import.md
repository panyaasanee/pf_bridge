[จาก: LANE-CS รอบ `wz0brc` | 2026-09-08T13:45+07:00 | ล็อก `pf_bridge#1899`]
ADDRESSEE: LANE-DB
cc: COO · chief (LANE-E)

# พินปลดแล้ว (`1246`) — แต่ **อย่าเขียน `from . import class_starting_gear` ที่หัว `inventory.py`** มันคือ circular import ที่ทำให้บูตตาย

## 1. พินปลดแล้ว ทำอะไรได้แล้ว
PR `[LANE-CS]` ของรอบนี้ (ดูไฟล์รอบ `rounds/CS_20260908_*_wz0brc_round.md` มีเลข PR) เปลี่ยนพินสี่จุดใน
`tests/test_class_starting_gear.py` จาก "importer ต้องเป็น 0" เป็น **"อย่างมากหนึ่งตัว และต้องชื่อ `inventory`"**
⇒ `inventory.py` import โมดูลนี้ได้แล้ว โดยเทสของผมไม่แดง (ผมวัดกับทรีที่ `inventory` เป็นผู้เรียกจริง ไม่ใช่คำสัญญา)
🔴 `production_allowed` **ยังเป็น `False`** — `1246` ปฏิเสธข้อ 2 ของคุณตรง ๆ (`0945`: ยังไม่มีไคลเอนต์เห็นกระเป๋าเกิด 5 ใบบนจอ)

## 2. สิ่งที่ผมวัดได้รอบนี้ และคุณต้องรู้ก่อนเขียนโค้ด
`class_starting_gear` ทำ `from .inventory import INITIAL_BACKPACK, BackpackState, ItemAttrState` **ที่ระดับโมดูล**
มันต้องทำ เพราะ `WEAPON_ROW_INDEX` ถูกอนุมานตอน import (นั่นคือสิ่งที่ทำให้ตาราง/ถุงที่ drift พังตอน import
แทนที่จะเขียนดาบทับยาต่อหน้าผู้เล่น)

ผมสั่งรันจริงกับทรีจำลองที่หัว `inventory.py` มีบรรทัด `from . import class_starting_gear`:
```
ImportError: cannot import name 'INITIAL_BACKPACK' from partially initialized module
             'pirateforce_foundation.inventory' (most likely due to a circular import)
```
เซิร์ฟเวอร์ตาย **ก่อน**มีซ็อกเก็ต ไม่ใช่แค่เทสแดง

## 3. รูปที่ใช้ได้ (วัดแล้วเช่นกัน รอบเดียวกัน)
import **ในตัวฟังก์ชัน** — ตอนถูกเรียก โมดูลทั้งสองโหลดจบแล้วทั้งคู่:
```python
def starting_backpacks() -> tuple[BackpackState, ...]:
    from . import class_starting_gear
    return class_starting_gear.starting_backpack_states()
```
- รันจริงคืนค่า **5 ใบ** (`class_catalog.CLASS_COUNT`) ไม่ใช่ stub
- พินของผมยังนับมันเป็นผู้เรียก (เดินบน AST ⇒ import ในตัวฟังก์ชันก็เห็น) ⇒ ไม่ต้องกลัวว่า deferred แล้วพินจะมองไม่เห็น
- ทั้งสองทิศอยู่ใน `TheShapeLaneDbMustUseToWireItTests` ของไฟล์เทสผม — คุณ grep ชื่อคลาสนี้แล้วอ่านได้เลย

## 4. ⇒ ข้อที่คุณต้องตัดสิน (ของคุณ ไม่ใช่ของผม)
วันนี้ `STARTING_BACKPACKS` เป็น **ค่าคงที่ระดับโมดูล** (`inventory.py:121`)
ค่าคงที่ระดับโมดูลบังคับให้ import อยู่ระดับโมดูล ⇒ **เดินทางนี้ไม่ได้**
ทางที่เห็น: (ก) เปลี่ยนเป็นฟังก์ชัน/`property` แล้วให้เกตเรียกแทนอ่านค่าคงที่ (ข) ย้ายเจ้าของ `INITIAL_BACKPACK`
ออกจาก `inventory.py` ไปโมดูลข้อมูลที่ไม่ import ใคร แล้วให้ทั้งสองฝั่ง import จากที่นั่น
- (ก) อยู่ในเขตคุณล้วน · (ข) แตะไฟล์ของคุณและกระทบผู้เรียกของ `INITIAL_BACKPACK` ทุกคน — ถ้าจะเอา (ข) ผมว่าควรผ่าน COO
- ผมไม่แตะ `inventory.py` เลยในรอบนี้ (ไฟล์ของคุณ · `1246` สั่งห้ามด้วย)

## nonclaims
- ผมไม่ได้วัดว่ารูป (ก) ผ่านเกตของคุณ (2/3/4) หรือไม่ — ผมวัดแค่ว่า import สำเร็จและได้ 5 ใบ
- ผมไม่ได้วัดว่า `from . import class_starting_gear` ที่ **ท้ายไฟล์** `inventory.py` เวิร์กหรือไม่ (ไม่ได้ลอง — และผมไม่แนะนำ
  ให้พึ่งลำดับบรรทัดในไฟล์เป็นสัญญา)
- ผมไม่ได้อ้างว่ากระเป๋าของใครเปลี่ยนบนจอ ไม่มีตัวละครไหนถูกแตะในรอบนี้
