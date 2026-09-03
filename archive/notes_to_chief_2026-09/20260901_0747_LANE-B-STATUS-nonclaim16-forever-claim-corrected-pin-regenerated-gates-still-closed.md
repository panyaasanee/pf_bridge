[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: กะ1-B, เจ้าของ | จาก: LANE-B (COMBAT) รอบ `0t89ae`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-09-01T07:47+07:00]

# LANE-B STATUS -- Bg0015 gate 1-4 ยังปิดเหมือนเดิมทุกข้อ (ตรวจสด) แก้ NONCLAIM 16 prose ให้ตรง
# กับสิ่งที่เทสจริงพิสูจน์ (กฎ F) ไม่มีอะไรให้ผู้เล่นเห็นเปลี่ยนไปรอบนี้

## สรุปสั้น

1. **มือจดหมาย**: grep `notes_to_chief/*.md` ที่ขาด `.CONSUMED.txt` แล้วกรองด้วย
   `ADDRESSEE.*LANE-B` / `CHIEF-TO-LANE-B` / `LANE-A-TO-LANE-B` -- พบแค่จดหมาย STATUS ขาออกของ
   สาย B เอง 3 ใบ (`0235`, `0550`, `0655`) ไม่ต้อง consume ไม่มีใบใหม่ที่ต้องตอบ
2. **ตรวจ Bg0015 gate 1-4 ที่ HEAD สด** (git grep จริง ไม่เชื่อ prose เก่า): ทั้งสี่ยังปิดเหมือนเดิม
   - gate 1 (`field_mobs._SCENE_TABLE_MODULES`): ยังมีแค่ bg0001/bg0002 สองคีย์
   - gate 2 (`mob_aggro.ATTACK_INTENT_DELIVERABLE`): ยัง `False`
   - gate `mob_pickup_persist`: ยังไม่มี caller ใน `runtime.py` -- ยึด `COO-DECISION 20260901_0245`
   - hostility-override dispatch / scene-14 composer จริง (ของ chief): ไม่มี commit ใหม่ที่แตะ
     `mob_ai_control.py`/`mob_ai_scheduler.py` dispatch ตั้งแต่รอบ `h40iwu`
3. ไม่มี gate ไหนเปิดใหม่ -> ทำตามกฎ F (ห้ามรอบว่างติดกัน)

## งานที่ทำ -- แก้คำกล่าวอ้าง "ตลอดไป" ของ NONCLAIM 16 ให้ตรงกับสิ่งที่เทสจริงพิสูจน์

รอบก่อน (`1yj0j0`) เขียนไว้ตรง ๆ ในจดหมายของตัวเองว่า ตอนพยายามพิสูจน์คำว่า "ตลอดไป" จากสถานการณ์
drift ครั้งเดียวก่อน **ความพยายามครั้งที่สองผ่านจริง** (ไม่ตรงคำอ้าง) จึงเปลี่ยนไปพิสูจน์ด้วย mock
เขียนล้มเหลวทุกครั้งแทน ซึ่งพิสูจน์ "ตลอดไป" ได้จริงสำหรับกรณีนั้นเท่านั้น **แต่ไม่ได้กลับไปแก้ prose
ของ NONCLAIM 16 เองใน `mob_pickup.py`** ซึ่งยังพูดแบบไม่มีเงื่อนไขว่า "cell mints one above the
column forever, so EVERY later pickup in that session is refused" -- กว้างเกินกว่าที่พิสูจน์จริง (ครอบ
ทั้งกรณี store แค่ตามหลังชั่วคราว ซึ่งพิสูจน์แล้วว่า**ไม่**เป็นแบบนั้น)

แก้ที่ `src/pirateforce_foundation/mob_pickup.py`:
- ป้ายกำกับ NONCLAIM 16 จาก "MEASURED BY READING BOTH CALL PATHS, NOT BY RUNNING THEM" เป็น
  "MEASURED BY EXECUTION (round `1yj0j0`, `tests/test_mob_pickup_persist.py::
  test_without_the_precheck_every_later_pickup_keeps_failing_the_same_way`)" -- ป้ายเดิมพูดเท็จแล้ว
- ขีดฆ่าประโยค "mints one above the column forever ... EVERY later pickup ... is refused" ด้วย
  สัญกรณ์ `~~...~~ IS STRUCK` ที่ไฟล์นี้ใช้เป็นมาตรฐานอยู่แล้ว (เหมือน NONCLAIM 9/11/14) แล้วเขียน
  แทนว่า: store แค่ตามหลัง (drift ครั้งเดียว) ปิดช่องว่างได้เองหลังพยายามอีกครั้งเดียว; เทสที่รันจริง
  พิสูจน์เฉพาะกรณี store ไม่ฟื้นเลย (mock ล้มเหลวทุกครั้ง 3 รอบติด -- ปฏิเสธเหตุผลเดิมทุกรอบ, identity
  คนละค่ากันทุกรอบ, ช่องว่างกว้างขึ้นเรื่อย ๆ) -- รูปที่ถูกคือ "ปฏิเสธไปอีกเท่าจำนวนรอบที่ store ไม่ฟื้น"
  ไม่ใช่ "ตลอดไปแบบไม่มีเงื่อนไข"

**ต่อสายพัง / ซ่อม**: `MOB_PICKUP_NONCLAIMS` เป็นส่วนหนึ่งของ `pin_document()` ที่
`scenarios/combat_pickup_001.json` ยึดไว้ (`tests/test_mob_pickup.py::
test_the_shipped_pin_file_is_what_the_code_computes`) -- แก้ prose แล้วเทสนี้แดงทันทีตามคาด สร้าง
ไฟล์ pin ใหม่จาก `pin_document()` เองแทนการแก้ JSON ด้วยมือ; `git diff` ของไฟล์นั้นมีแค่ 1 บรรทัด
เปลี่ยน (บรรทัด NONCLAIM 16 เท่านั้น)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มี -- นี่คือการแก้ความถูกต้องของเอกสารภายในโค้ด ไม่ใช่การเปลี่ยนพฤติกรรม ไม่มีบรรทัดตรรกะไหนแตะ

## ตัวเลขที่วัดได้

```
ไฟล์ที่แตะ (pirate-force-server) รวม 3:
  src/pirateforce_foundation/mob_pickup.py  [prose NONCLAIM 16 เท่านั้น]
  scenarios/combat_pickup_001.json          [regenerate จาก pin_document(), 1 บรรทัดเปลี่ยน]
  rounds/B_20260901_0747_0t89ae_*.md
ไฟล์ที่แตะ (pf_bridge) รวม 2:
  rounds/B_20260901_0747_0t89ae_*.md
  notes_to_chief/20260901_0747_LANE-B-STATUS-*.md [ใบนี้]
เฉพาะไฟล์ที่แก้ (targeted): tests/test_mob_pickup.py tests/test_mob_pickup_persist.py
  -> 116 passed, 133 subtests passed -- เท่าเดิมเป๊ะก่อน/หลัง (prose+pin เท่านั้น ไม่แก้ตรรกะ)
สวีตเต็มหลังแก้: 6153 passed, 327 skipped, 13141 subtests passed, 0 failed (173.84s)
  (รอบก่อนรายงาน 6155/323 -- ต่างกัน 4 -- ตรวจแล้วด้วย -rs ว่าทุก skip ที่ต่างเป็น
  `[precondition:client_image]` ล้วน คือ environment-dependent ไม่เกี่ยวกับ diff 2 ไฟล์ของรอบนี้)
```

## หมายเหตุกระบวนการ -- pf-adversary

session นี้ไม่มีเครื่องมือ/agent สำหรับเรียก pf-adversary แยกต่างหาก ทำสิ่งที่ปกติมันตรวจเอง: (ก) grep
หาทุกจุดที่ quote ข้อความ NONCLAIM 16 แบบเป๊ะก่อนแก้ (ไม่มีที่ไหนอ้างอิงคำต่อคำที่จะพัง) (ข) ยืนยัน
pin-file guard ทำงานจริงโดยเห็นมันแดงก่อนแก้ ไม่ใช่แค่มีไฟล์ (ค) ระหว่างพยายามวัด baseline สวีตเต็มแยก
คำสั่ง `git stash && timeout ...` ถูก timeout กลางทางหลัง `git stash` สำเร็จแต่ก่อน `git stash pop` --
ตรวจพบทันทีด้วย `git stash list`, กู้คืนด้วย `git stash pop`, ยืนยันด้วย `git diff --stat` ว่าไฟล์กลับมา
ครบ 2 ไฟล์ ไม่มีอะไรหาย

## ยังไม่ได้พิสูจน์

- gate 1-4 ของ Bg0015 ทั้งสี่ยังปิดเหมือนเดิม -- ต้องรอ chief ต่อสาย (hostility-override dispatch /
  scene-14 composer) หรือรอ scene table registration ก่อนจึงจะมีอะไรให้ผู้เล่นเห็น
- `mob_pickup_persist` ยังบล็อกด้วย `GT-124`/`GT-146` เหมือนเดิมทุกประการ
- prose fix รอบนี้ไม่เปลี่ยนพฤติกรรมเลยสักบิต -- ประโยชน์คือคนต่อสาย (chief) ในอนาคตจะอ่าน NONCLAIM 16
  แล้วไม่เข้าใจผิดว่า "ตลอดไป" หมายถึงทุกกรณีของ store refuse

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `0t89ae`
