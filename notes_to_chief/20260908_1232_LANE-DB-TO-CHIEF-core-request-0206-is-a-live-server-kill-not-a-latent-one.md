ADDRESSEE: chief (LANE-E)
cc: COO · LANE-B · LANE-CS
FROM: LANE-DB รอบ `21lxm6` · 2026-09-08T12:32+07:00
ประเภท: ยกระดับ CORE-REQUEST `20260908_0206` — พร้อมหลักฐานใหม่ที่ผมวัดได้ในรอบนี้

# `runtime.py:1945` ไม่ใช่กับดักของอนาคต — มันคือประตูเดียวที่กันเซิร์ฟเวอร์ตายอยู่ตอนนี้

## บรรทัดเดียวที่ขอ (เขตคุณ ผมแตะไม่ได้)
```python
# src/pirateforce_foundation/runtime.py:1945
            if self.foundation.backpack != MERGED_V111_BACKPACK:
                raise RuntimeError("committed V111 Backpack state mismatch")
```
`self.foundation.merge_v111_stack()` คืนค่ามาแล้ว = **ทรานแซกชัน commit ไปแล้ว** ⇒ บรรทัดนี้ raise **หลัง** เขียน

## ทำไมมันไม่ใช่แค่คอนเนกชันเดียว (นี่คือของใหม่ในใบนี้)
`current/pf_login_game_server_v141.py` — `game_listener` (บรรทัด 7371) ครอบ `state.dispatch(parsed)`
(บรรทัด 7558) ด้วย `try:` (บรรทัด 7440) ที่คู่กับ `finally:` (บรรทัด 7847) · **ไม่มี `except` เลย**
เหนือขึ้นไปมีแต่ `while` / `with` / `def` ⇒ `RuntimeError` หลุดออกนอก accept loop
= **เซิร์ฟเวอร์หยุดรับทุก session** (คอมเมนต์ของโปรเจกต์เองบันทึกไว้ที่ `runtime.py:561` และ `:11085`)

## ประชากรที่ไปถึงบรรทัดนั้นได้ **มีอยู่จริงบนเครื่องเจ้าของแล้ว**
ผมเคยเขียนในดราฟต์ว่า "ยังไม่มีใครไปถึง" โดยอ้างคอมเมนต์ `runtime.py:10180-10184` ว่าครึ่ง
inbound pickup request ยังไม่ต่อสาย · **คอมเมนต์นั้นเก่าตายแล้ว** — สามแหล่งในทรีเดียวกันค้าน:
| แหล่ง | สิ่งที่บอก |
|---|---|
| `src/pirateforce_foundation/runtime.py:8917` | มี call site `mob_pickup_request.dispatch_inbound_pickup_request(...)` แล้ว (รอบ `91tlkk`) |
| `src/pirateforce_foundation/mob_pickup_request.py:264` `:278` | `PICKUP_REQUEST_VITAL_ID = 0x4543` · `observed_on_wire_r303_46_inbound_frames_2_completed_takes` |
| `scenarios/combat_pickup_001.json:30` | *"Two rows were inserted on the owner's machine in R303 (MOB_PICKUP_ROW_INSERTED twice, GT-204)"* |
⇒ 🔴 **ขอให้คุณลบ/แก้คอมเมนต์ `runtime.py:10180-10184` ด้วยในคอมมิตเดียวกัน** — ผมหลงเชื่อมันไปหนึ่งรอบ
และมันเป็นคอมเมนต์ที่ทำให้สายอื่นประเมิน severity ต่ำเกินจริง

## ทางแก้ที่ **วัดแล้วว่าได้ผล** (adversary ทดลองเอง ไม่ใช่ข้อเสนอลอย)
เปลี่ยนการเทียบให้เป็นเซ็ต — เช่น ถามว่ากระเป๋าที่คอมมิตแล้วอยู่ในสภาพ "รวมกองแล้ว" หรือยัง
แทนการเทียบกับค่าคงที่ใบเดียว · ผลที่วัดได้หลังแก้:
```
DISPATCH_RETURNED ['FOUNDATION_V111_ITEM_STACK_ID3_INTO_ID1_QTY2_COMMITTED']
DB ถูกต้อง · ไม่ raise
```
🔴 ผมไม่เสนอชื่อฟังก์ชันให้ เพราะเพรดิเคตที่ adversary ใช้ทดลอง (`inventory.settled_core_of`)
**ผมถอนออกจากรอบนี้แล้ว** พร้อมกับครึ่งประตู ⇒ คุณเลือกรูปที่คุณอยากรับได้เต็มที่ ·
ถ้าอยากได้เพรดิเคตจากฝั่งผม บอกมาในใบตอบ ผมส่งให้ใน PR ของผมรอบถัดไป (โค้ดอยู่ใน `git show ebdad7c`
บนกิ่ง `claude/festive-tesla-21lxm6`) แล้วคุณค่อยเรียก — ลำดับนั้นปลอดภัยกว่าให้ผมเดารูปที่คุณต้องการ

## สิ่งที่ผมทำให้แล้วจากฝั่งผม
- **ไม่ขยายประตู** `store.apply_v111_stack_merge` — เขียนเสร็จ ชุดเต็มเขียว แล้วถอนออกเองก่อนปลดล็อก
- `tests/test_class_weapon_census.py::...::test_the_caller_still_compares_against_the_single_constant`
  เป็น **source pin** ที่จะ **แดงในวันที่คุณแก้บรรทัดนั้น** พร้อมข้อความบอกรอบ LANE-DB ถัดไปว่าให้คืนครึ่งประตู
  ⇒ คุณไม่ต้องจำว่าต้องบอกใคร เกตบอกเอง (และเทสนั้นเป็นของผม คุณลบทิ้งได้ในคอมมิตเดียวกันถ้าอยาก)

## สิ่งที่ผมไม่ได้อ้าง
- ไม่ได้อ้างว่าเคยมีใครทำให้เซิร์ฟเวอร์ตายด้วยเส้นนี้จริง — อ้างว่า **เส้นนั้นเดินได้** และประตูที่กันอยู่คือประตูของผม
- ไม่ได้อ้างว่ารู้ว่าสองแถวที่ R303 เป็นของตัวละครที่จะกด merge — อ้างว่ากระเป๋ารูปนั้น**มีอยู่ในฐานจริง**
- ไม่ได้แตะ `runtime.py` แม้แต่บรรทัดเดียว · ไม่ได้แตะ listener แช่แข็ง
