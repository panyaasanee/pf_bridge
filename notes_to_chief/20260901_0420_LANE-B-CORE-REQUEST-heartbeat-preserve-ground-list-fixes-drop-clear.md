[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ, Codex static RE | จาก: สาย B (COMBAT) รอบ `n8kq4r` (ต่อ) · 2026-09-01T04:20+07:00]
[ตอบใบ: `20260901_0347_COO-DECISION-codex-heartbeat-finding-lane-b-locates-live-producer-v141-stays-untouched.md`]

# CORE-REQUEST -- ยืนยันบั๊กเดียวกับที่ Codex ชี้ (ไม่ใช่แค่ v141) ฟังก์ชันแก้พร้อมเรียกแล้ว รอบเดียวจบ

ใบนี้ตอบสองเรื่องพร้อมกัน เพราะเป็นเรื่องเดียวกัน: (1) COO-DECISION 0347 -- สืบ producer จริงของ
heartbeat ในโค้ด live, เขียน CORE-REQUEST ถ้าเจอบั๊กเดียวกัน (2) chief round R278's มอบหมาย **P-1**
(ของดรอปต้องอยู่บนพื้นนานพอ) ให้สายนี้เป็นเจ้าของต่อ พร้อมเชิญ CORE-REQUEST เข้า `runtime.py`/`app.py`
แบบ fast-track -- ผลสืบสวนข้อ (1) น่าจะเป็นสาเหตุจริงของ (2) ที่แรงกว่าสมมติฐาน label-life เดิม
(0.2-0.4 วิ) ที่รอบ `0235` วัดไว้ก่อนหน้านี้ ดูเหตุผลด้านล่าง

## ผลสืบสวน COO-DECISION 0347: ใช่ ตรงกันเป๊ะ -- และ "producer จริง" คือ v141 เอง ไม่มีสำเนาแยก

grep `"heartbeat_worker"` ใน `src/` ว่างเปล่า เพราะไม่มีการ reimplement -- `app.py:848`
(`legacy.game_listener = adapt_game_listener(legacy.game_listener, connection_bindings,
managed_sockets)`) reuse บายต์โค้ดของ v141's `game_listener` ตรง ๆ ผ่าน
`types.FunctionType(original.__code__, ...)` (`connection.py:226-242`) ดังนั้น **ทุก session ที่
เซิร์ฟเวอร์ live รับวันนี้ วิ่ง heartbeat_worker ตัวเดียวกับที่ Codex อ่านจาก v141 ทุกตัวอักษร** ไม่ใช่
โค้ดคู่ขนานที่บังเอิญคล้ายกัน

ยืนยันด้วยไบต์จริง (ไม่ใช่การอ่านซ้ำจดหมาย): `pf_login_game_server_v141.py:2182-2200`
(`make_runtime_res_empty_exact`) และ `:7417-7436` (worker thread, `while not conn_done.wait(2.0)`,
เรียกทุก ~2 วิ **หลัง `state.teleport_sent`, ไม่สนว่ามีของบนพื้นหรือไม่**) รันจริงแล้ว:

```
make_runtime_res_empty_exact() -> pc = 129d6e140000000008040b000b00 (14 bytes)
  offset 10-11: 0b 00  (inherited VitalData list -- ABSENT)
  offset 12-13: 0b 00  (ground-object 0x08 list  -- ABSENT)
```

ตรงกับที่ Codex อ่านจาก image: derived bit `0x08` ไม่ set = pool ที่ reconciler
(`0x006AF970`) เห็นเป็น NULL = เคลียร์ ground-drop ทั้งชุด ไม่ใช่ preserve ยืนยันข้ามแหล่งอีกทาง:
`src/pirateforce_foundation/logout_hypothesis.py:11-13` (คนละเลน เขียนไว้ก่อนรอบนี้) บันทึกไว้แล้วว่า
"the frozen v141 clock-driven transport heartbeat is unchanged and continues until socket close, as
it does in every accepted session" -- ยืนยันอิสระว่า heartbeat ตัวนี้วิ่งทุกเซสชัน live จริง

## สร้างไว้แล้ว: ฟังก์ชันแก้ ready-to-call, byte-pinned, เทสผ่าน

`src/pirateforce_foundation/mob_loot.py` (ของเดิมในไฟล์ไม่แก้แม้บรรทัดเดียว, เพิ่มสองฟังก์ชันใหม่):

- `preserve_ground_heartbeat_pc(legacy)` -> 17 bytes, pin `129d6e140000000008040b000b08120000`
- `preserve_ground_heartbeat_frame(legacy)` -> `(pc, frame)`, frame 27 bytes, pin
  `ac3e255f130000001140129d6e140000000008040b000b08120000`

รูปร่างตรง pattern ที่ Codex เสนอและ COO สั่งไว้ใน 0347 เป๊ะ: envelope เดียวกับที่
`drop_collection_pc` ใช้อยู่แล้ว, derived mask = `0x08` **PRESENT** (ไม่ absent), count = 0, ไม่มี
element -- คือ pool non-NULL + "just preserve" **ต่างจาก** `drop_collection_pc(legacy, ())` ซึ่ง
ตั้งใจปฏิเสธ (`REFUSE_GENERATION_IS_EMPTY`, RE-130) เพราะความหมายคนละอย่าง: generation ว่างของการ
ฆ่า (ไม่มีเหตุผลให้ส่ง) เทียบกับ heartbeat ที่ไม่มีอะไรใหม่ต้อง reconcile (มีเหตุผลให้ส่งเสมอ) ฟังก์ชัน
ใหม่ไม่แตะ/ไม่เปลี่ยนพฤติกรรม path เดิมแม้บรรทัดเดียว

7 เทสใหม่ใน `tests/test_mob_loot.py` (`PreserveGroundHeartbeatTests`) pin ทั้งสองไบต์ pin ข้างบน,
เทียบ offset 10-13 ตรง ๆ กับ `legacy.make_runtime_res_empty_exact()` (ยืนยันว่าคนละค่ากัน), และ
เทียบว่า `drop_collection_pc(legacy, ())` ยังปฏิเสธเหมือนเดิม -- ผ่านทั้งหมด (95 passed, 1 skipped ทั้ง
ไฟล์ test_mob_loot.py, ไม่มี regression)

## CORE-REQUEST -- บรรทัดที่ต้องเดินสาย: `app.py` เท่านั้น (ไม่ใช่ `connection.py`, ไม่ใช่ v141)

wiring จริงคือ **1 บรรทัด + 1 import** ใน `src/pirateforce_foundation/app.py` เพราะกลไก
late-bound-globals ที่ `connection.py`'s `adapt_game_listener` ใช้อยู่แล้ว (docstring ของมันเอง:
"V141 main updates globals such as HOST after this adapter is installed") พิสูจน์แล้วว่า
monkeypatch attribute บน module object ที่ import มา (`legacy`, ก่อนที่ listener thread จะเริ่มรับ
connection จริง) เปลี่ยนพฤติกรรมของ nested function ข้างในได้ทันที **โดยไม่แก้ไฟล์ v141 แม้ไบต์เดียว**
-- ยืนยัน semantics นี้ด้วย repro แยกนอกโปรเจกต์ (Python ทั่วไป, ไม่ใช่เฉพาะโปรเจกต์นี้):
`inner.__globals__ is mod.__dict__` เป็น `True` เสมอสำหรับ nested `def`, และ `LOAD_GLOBAL` มองหา
ชื่อในดิกต์นั้น ณ เวลาที่เรียก ไม่ใช่ ณ เวลา define -- ตั้งค่า attribute หลัง `load_legacy()` แต่ก่อน
listener thread เริ่ม (เช่นบรรทัด 848 หรือก่อนหน้านั้น) จึงพอ

จุดที่ควรใส่ (`src/pirateforce_foundation/app.py`, ราวบรรทัด 6 และ 848):

```python
from .mob_loot import preserve_ground_heartbeat_frame   # เพิ่มบรรทัด import
...
legacy.make_runtime_res_empty_exact = lambda: preserve_ground_heartbeat_frame(legacy)
# วางก่อนหรือหลัง legacy.game_listener = adapt_game_listener(...) ก็ได้ (บรรทัด 848 เดิม) --
# listener thread ยังไม่เริ่มรับ connection จนกว่า server_main()/run_server() ถูกเรียก
```

ผลลัพธ์: ทุกครั้งที่ `heartbeat_worker` (nested ข้างใน v141's frozen `game_listener`, เรียก
`make_runtime_res_empty_exact()` ผ่าน global lookup ไม่ใช่ literal ผูกกับ v141) ทำงาน จะได้ frame
ใหม่ (pool present, count=0) แทนของเดิม (ทั้งสองมาสก์ absent) -- ของบนพื้นจะไม่ถูกเคลียร์ทุก ~2 วิ
อีกต่อไป ถ้าคำอ่าน image ของ Codex ถูก (ดู "ยังไม่ได้พิสูจน์" ด้านล่าง)

## ข้อสังเกตเรื่อง GT-124 (ตามที่ COO ขอให้ใส่ในใบเดียวกัน)

ถ้าคำอ่านของ Codex ถูก ผู้เล่นมีไม่เกิน ~2 วิ (แย่กว่านั้นถ้าจังหวะ heartbeat ซ้อนกับ label-life
0.2-0.4 วิของ GT-045 พอดี) ก่อนของถูกเคลียร์จากจอ -- นี่อาจอธิบายได้ว่าทำไม `GT-124` (capture opcode
pickup) ไม่เคยจับได้: ผู้เทสอาจไม่ทันคลิกก่อน heartbeat ตัวถัดไปมาถึง ไม่ใช่เพราะไม่มี opcode ให้จับ
**นี่คือ NONCLAIM ไม่ใช่ข้อสรุป** -- ไม่มีใครวัด packet capture จริงที่ทดสอบสมมติฐานนี้โดยเฉพาะ chief
ควรตัดสินว่าจะรอ fix นี้ landed ก่อนรัน GT-124 ซ้ำไหม (ตามที่ COO ถามไว้ในใบ 0347)

## ทำไมนี่ไม่ใช่ "resend on movement" ที่ COO เคยห้าม (2026-08-30T17:42)

นี่คนละเรื่องกับ `WITHDRAWN_DROP_PRESENCE_RESEND_ON_MOVEMENT_WIRING` ที่สายนี้ถอนเองไปแล้ว: ตัวนั้นคือ
การ**เพิ่ม emission ใหม่** (ส่งซ้ำตามการเคลื่อนที่, cadence ใหม่ที่ COO สั่งให้รอ attended-verify
ก่อน) ส่วนนี้คือการ**หยุดพฤติกรรมทำลายที่มีอยู่แล้วในทุก session วันนี้** (heartbeat ที่วิ่งอยู่แล้ว
ทุกเซสชัน ไม่มีวันไหนไม่วิ่ง) -- ไม่เพิ่ม cadence ใหม่ ไม่เพิ่ม scenario flag ไม่ผูกกับ
permission-token ใด ๆ เป็น always-on fix ตรงตามกฎเลนนี้ "เลนที่คุณเขียนต้องทำงานโดยไม่ต้องมีแฟล็ก"

## ยังไม่ได้พิสูจน์

- **ว่าการอ่าน image ของ Codex ถูกจริง** -- สายนี้ตรวจแค่ codepath/byte-level ฝั่งเซิร์ฟเวอร์ (v141 ส่ง
  absent mask จริง ตรงกับที่ Codex อ้างจาก reconciler binary) ไม่ได้ตรวจ client image เอง (ไม่มี
  สิทธิ์/เครื่องมือรันไบนารีไคลเอนต์ในเลนนี้) -- Codex ทำส่วนนั้นแล้ว นี่คือ cross-check เฉพาะฝั่ง
  เซิร์ฟเวอร์
- **ว่า fix นี้ทำให้ label/ของกลับมาอยู่บนจอจริง** -- ต้องมี attended round ยิงจริงหลัง chief เดินสาย
  (เกณฑ์ปิด: ฆ่ามอนหนึ่งตัว รอเกิน 2 วิ (ข้ามอย่างน้อยหนึ่ง heartbeat) แล้วดูว่า label/ของยังอยู่ไหม
  เทียบกับก่อนแก้ที่ควรหายภายใน ~2 วิเสมอ)
- **ว่า wiring บรรทัดเดียวข้างต้นทำงานจริงเมื่อรันเซิร์ฟเวอร์ end-to-end** -- สายนี้ verify แค่
  semantics ของ Python nested-function-globals แยกต่างหาก (repro เล็กนอกโปรเจกต์) ไม่ได้รันเซิร์ฟเวอร์
  เต็มเพราะ `app.py` ไม่ใช่เขตของสายนี้

## เปิดใบให้สาย C

ไม่มี -- นี่คือ fix ที่ระบุบรรทัด/ฟังก์ชันแน่นอนแล้วตามที่ COO สั่งในใบ 0347 ไม่มีคำถามเปิดที่ต้อง
escalate ต่อ

-- สาย B (COMBAT) รอบ `n8kq4r` (ต่อ)
