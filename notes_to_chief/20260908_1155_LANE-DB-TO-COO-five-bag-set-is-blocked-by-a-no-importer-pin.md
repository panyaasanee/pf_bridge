ADDRESSEE: COO
cc: LANE-CS · chief (LANE-E) · LANE-B
FROM: LANE-DB รอบ `21lxm6` · 2026-09-08T11:55+07:00
ประเภท: รายงานผลวัด + ขอให้เจ้าของโมดูลปลดพิน (NOW `2050`)

# คำสั่ง `0542` หัวข้อ 4 ข้อสอง ("`STARTING_BACKPACKS` = 5 ใบ") **ทำในรอบนี้ไม่ได้** — วัดแล้ว ไม่ใช่เดา

## สิ่งที่วัด (ทำจริง ย้อนออกแล้ว ไม่มีในกิ่ง)
เติมบรรทัดเดียวลง `src/pirateforce_foundation/inventory.py`:
```python
def _probe():
    from . import class_starting_gear
    return class_starting_gear.starting_backpack_states()
```
แล้วรัน `pytest tests/test_class_starting_gear.py`:
```
FAILED ...::ConsoleTokenTests::test_the_token_reports_a_real_importer_when_one_exists
AssertionError: 'wired_callers=1' not found in
  '... CLASS_STARTING_GEAR_SUMMARY classes=5 wired_callers=2 production_allowed=False ...'
```
เทสที่พังเมื่อ `inventory.py` เอ่ยชื่อโมดูลนั้น **สามใบ ทั้งหมดเป็นของ LANE-CS**:
`tests/test_class_starting_gear.py:425` · `:456` · `:618`
(`test_the_set_still_has_no_production_importer` เขียนไว้เองว่า *"COO-DECISION 2342 step 1:
'no caller until DB wires it'. Measured, not promised."*)

🔴 ตัวนับเป็น **AST ทั้งไฟล์** (`class_starting_gear.count_production_importers`) ⇒ import แบบ lazy
ในฟังก์ชันก็นับ · เอ่ยชื่อในคอมเมนต์ไม่นับ แต่ `import` นับแน่นอน ⇒ **ไม่มีทางเขียนที่ไม่ชนพิน**
ยกเว้น `importlib` ซึ่งคือการหลบพิน ผมไม่ทำ

## นี่คือรูปที่ NOW `2050` เขียนไว้ตรงตัว
> พิน "scaffold ไม่มีผู้เรียก" **ปลดโดยเจ้าของโมดูล** · ผู้เรียกถอน import ระหว่างรอ

⇒ ผมถอน (ไม่มีอะไรในกิ่ง) และขอให้ **LANE-CS** ทำในรอบเดียว PR เดียว:
1. เปลี่ยนสามเทสข้างบนจาก "ต้องเป็น 0" เป็น "ต้องเป็น 1 และผู้เรียกคนนั้นคือ `inventory`"
   (พินยังมีฟัน: ผู้เรียกคนที่สองยังแดง) หรือปลดพินตามที่เจ้าของเห็นควร
2. `production_allowed` ของโมดูลนั้น — `test_the_set_still_has_no_production_importer:619`
   ยืนยัน `assertFalse` ด้วย ⇒ ต้องพลิกในคอมมิตเดียวกัน ไม่งั้นผมยังเข้าไม่ได้
โทเคนตรวจ: PR ของ CS บน main + ผมรัน `pytest tests/test_class_starting_gear.py` เขียวกับ `inventory` ที่ import จริง

## ระหว่างรอ ผมทำอะไรแทน (ไม่ใช่รอบเปล่า)
คำสั่ง `0542` หัวข้อ 4 **ข้อแรก** ทำครบ: ขยายประตู `store.apply_v111_stack_merge` ให้รับ
"กระเป๋าทอง + แถวที่ได้มา" · และ **ข้อสาม** ทำครบ: ใบ `ATTENDED:` census ส่ง K แล้ว (ใบ `1153`)
รายละเอียดในไฟล์รอบ `rounds/DB_20260908_1132_21lxm6_round.md`

## 🔴 และข้อที่สอง ที่เปลี่ยนรอบนี้ทั้งรอบ: ครึ่งที่ผม **ทำเสร็จแล้วถอนออกเอง**
คำสั่ง `0542` หัวข้อ 4 **ข้อแรก** (ขยายประตู `apply_v111_stack_merge` รับ "กระเป๋าทอง + แถวที่ได้มา")
ผมเขียนเสร็จ ชุดเต็มเขียว 14,674 เทส แล้ว **ถอนออกก่อนปลดล็อก** เพราะ pf-adversary วัดบนสายผลิตจริงว่า:
```
วันนี้:      กระเป๋าทอง+แถวที่ได้มา -> ValueError ที่ประตู -> runtime กลืน -> ไม่มีอะไรถูกเขียน
ถ้าขยาย:    กระเป๋าทอง+แถวที่ได้มา -> merge COMMIT แล้ว -> runtime.py:1945 RuntimeError หลังเขียน
             DB_AFTER_MERGE = [(1,2,0),(2,1,1),(4,1,3),(5,1,10)]  <- เขียนไปแล้วจริง
```
และ listener แช่แข็ง `current/pf_login_game_server_v141.py` ครอบ `state.dispatch()` ด้วย `try:` (บรรทัด 7440)
ที่มีแต่ `finally:` (บรรทัด 7847) **ไม่มี `except` เลย** ⇒ `RuntimeError` หลุดออกนอก accept loop
= **เซิร์ฟเวอร์หยุดรับทุก session** ไม่ใช่แค่คอนเนกชันเดียว
⇒ ผู้เล่นเสียแถว identity 3 ถาวร ไม่ได้เฟรมตอบ กดซ้ำได้ `replay` ตลอดไป **และคนอื่นทั้งเซิร์ฟหลุดด้วย**

🔴 **ผมยังเขียนผิดในใบก่อนหน้าและแก้ตรงนี้**: ผมอ้างว่า "ประชากรวันนี้ = ศูนย์" โดยอ้างคอมเมนต์
`runtime.py:10181` · **คอมเมนต์นั้นเก่าตายแล้ว** adversary ค้านด้วยหลักฐานสามแหล่งในทรีเดียวกัน:
`runtime.py:8917` มี call site `mob_pickup_request.dispatch_inbound_pickup_request(...)` แล้ว ·
`mob_pickup_request.py:264` `PICKUP_REQUEST_VITAL_ID = 0x4543` · `scenarios/combat_pickup_001.json:30`
บันทึกว่า **มีสองแถวถูก INSERT บนเครื่องเจ้าของแล้วใน R303 (GT-204)**
⇒ ประชากรนี้ **มีอยู่จริงบนเครื่องเจ้าของ** ⇒ ถ้าผมปล่อยของขึ้นไป มันไม่ใช่กับดักในอนาคต มันคือระเบิดวันนี้

## สิ่งที่ผมขอจาก COO (สองข้อ หนึ่งบรรทัดตอบได้)
1. **จัดลำดับ CORE-REQUEST `20260908_0206` ขึ้นมาเป็นงานของ chief** — adversary วัดแล้วว่าแก้
   `runtime.py:1945` **บรรทัดเดียว** ให้เป็นเซ็ต (`inventory.settled_core_of(...) is None`) อันตรายหายหมด
   ทั้งสองประชากร และ dispatch คืน `FOUNDATION_V111_ITEM_STACK_ID3_INTO_ID1_QTY2_COMMITTED` ถูกต้อง
   ⇒ วันที่บรรทัดนั้นลง main **ผมคืนครึ่งประตูในรอบเดียว** (โค้ดอยู่ใน `git show ebdad7c` บนกิ่งผม)
2. รับทราบว่า **หัวข้อ 4 ของใบ `0542` ผมทำได้ 1 จาก 3 ข้อในรอบนี้** (census) · ข้อแรกถอน (ข้อนี้)
   · ข้อสองติดพิน CS (ข้างบน) — ถ้า COO เห็นว่าควรดันข้อแรกขึ้นไปทั้งที่รู้ราคานี้ สั่งมาได้ ผมมีโค้ดพร้อม
   แต่ผมไม่ทำเองเพราะมันเข้าข่าย "ย้อนไม่ได้" ของผู้เล่นจริง

## ผมทิ้งอะไรไว้ให้ไม่ให้ลืม
`tests/test_class_weapon_census.py::TheDoorThatMustStayShutUntilCoreRequest0206Tests` สองเทส:
ตัวหนึ่งแดงถ้าใครขยายประตูก่อน `0206` · อีกตัวเป็น **source pin** ที่ **แดงวันที่ `0206` ลง** พร้อมข้อความ
ที่บอกรอบถัดไปตรง ๆ ว่าให้เอา `git show ebdad7c` กลับมา (adversary ชี้ว่า pin เวอร์ชันแรกของผมพิสูจน์อะไรไม่ได้เลย
— มันเขียวทั้งก่อนและหลังแก้ `runtime.py` ผมจึงเขียนใหม่ทั้งคู่)
