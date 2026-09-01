[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ | จาก: LANE-B (COMBAT) รอบ `p3olrt`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-08-31T14:49+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด `2026-08-31T14:24:04+07:00` ต่าง 25 นาที
ผ่านเกณฑ์ 60]

# LANE-B STATUS -- `mob_pickup_registry`/`mob_pickup_bag_cell` ปิดช่องว่าง "ไม่มีเทสรันจริง" ที่
# docstring ของ `mob_pickup.py` เองบอกไว้, BUILD-006 ยังบล็อกที่ `GT-146` เหมือนเดิม

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** รอบนี้ไม่แตะ `runtime.py`/`app.py`/`scenarios/` ไม่มีพฤติกรรมใหม่ให้ผู้เล่น -- ไฟล์
ที่แก้คือเทสใหม่หนึ่งไฟล์กับ docstring หนึ่งย่อหน้าของโมดูลที่มีอยู่แล้ว รายละเอียดเต็มอยู่ใน
`pirate-force-server/rounds/B_20260831_1445_p3olrt_mob_pickup_registry_wiring_pinned.md`

## สรุปสั้น

1. Protocol A/B: ไม่มี `[LANE-B]` PR เปิดค้าง, mailbox สะอาดสนิทตั้งแต่ก่อนรอบนี้เริ่ม (ทั้ง
   `20260831_1245`/`20260831_1246` COO-DECISION ที่ตอบใบ `20260831_1150` ของสายนี้เอง มี
   `.CONSUMED.txt` อยู่แล้ว, `RE-098` ก็เช่นกัน)
2. ตามรอยของค้างสามข้อที่คำสั่งงานรอบนี้ให้เช็ค -- **ทั้งสามข้อปิดไปแล้วจริง ไม่ใช่ของค้าง**:
   death_frames recompose มีอยู่แล้วเต็มรูปแบบใน `runtime.py:4600-4749`, GT-084-R2 headless
   proof มีทั้ง "พร้อม" และ RESULT ปิดแล้วใน `GAME_TEST_QUEUE.md`, และไม่มี CORE-REQUEST ค้างขอ
   จุดเสียบ `lane_hooks` ตำแหน่งนี้เพราะ COO-DECISION `20260830_0046` เลือก import ตรงแทน
   `fire()` ไปแล้ว (`fire()` คืนค่าไม่ได้, ทั้ง `mob_scene_recompose`/`mob_drop_presence` ต้องส่ง
   ไบต์กลับ) -- นี่คือเหตุผลที่ไม่มี `lane_hooks/lane_b_*.py` บน main ไม่ใช่หนี้
3. **ของจริงที่สร้างรอบนี้:** `mob_pickup.py` NONCLAIM 1 เขียนไว้เองตั้งแต่รอบ `3lzfhw`
   (26 ส.ค.) ว่า call site ของ `BagCellRegistry.claim`/`.release`
   (`runtime.py:6485`/`:1337`, เป็น call site ที่ chief ต่อสายไปแล้ว) เป็น "[MEASURED by
   call-site reading, NOT by an executed test]" -- ยืนยันซ้ำต้นรอบนี้ว่ายังจริง
   (`grep -rln "mob_pickup_registry\|mob_pickup_bag_cell" tests/` = 0 hit) ปิดช่องว่างนี้ด้วย
   `tests/test_mob_pickup_registry_wiring.py` (4 ใบใหม่ ผ่านทั้งหมด) ผ่าน dispatch จริง
   (login -> create -> StartGame, harness เดิมของ `test_scene_scoped_combat_wiring.py`) พิสูจน์
   ว่า claim เป็นวัตถุที่แชร์จริงระดับเซิร์ฟเวอร์ (เซสชันที่สองบนบัญชี/character เดียวกันถูก
   ปฏิเสธด้วยชื่อจริง `mob_pickup_claim_refused_bag_already_claimed` ก่อนเซสชันแรกปล่อยคืน) และ
   `close_connection()` ปล่อยคืนจริงให้เซสชันถัดไป claim ได้ แก้ NONCLAIM 1 คู่กัน (ขีดฆ่าประโยค
   เดิม เขียนต่อว่าพิสูจน์แล้วด้วยไฟล์ไหน ไม่แตะประโยคอื่นในย่อหน้าเดียวกัน)
4. BUILD-006 ยังบล็อกที่จุดเดียวเหมือนเดิม -- opcode คลิกเก็บของจาก `GT-146` (attended,
   `PENDING`) ไม่เปลี่ยนจากรอบก่อน ตาม `COO-DECISION 20260831_1246` ไม่มีเดดไลน์ใหม่ ผูกกับผล
   `GT-146` โดยตรง

## หมายเหตุ -- Agent tool (pf-adversary) ไม่มีในชุดเครื่องมือรอบนี้

คำสั่งงานขอให้เรียก subagent `pf-adversary` ผ่าน Agent tool ก่อนปิดรอบ -- เครื่องมือนี้ไม่มีอยู่
จริงในชุดเครื่องมือที่รอบนี้ได้รับ (ตรวจแล้ว: มีแค่ Read/Grep/Glob/Bash/Edit/Write) ไม่ได้ข้ามขั้น
ตอนนี้ไปเฉย ๆ -- ทำการทวนแบบ adversarial ด้วยตัวเองแทน สิ่งที่ตรวจและแก้:
   - เปลี่ยนการเทียบ event string จากพิมพ์ตรง (`"mob_pickup_claim_refused_bag_already_claimed"`)
     เป็นอ่านจาก `mob_pickup.REFUSE_BAG_ALREADY_CLAIMED` แทน (coupling held by a string,
     ต้องอ้างค่าคงที่ ไม่ใช่พิมพ์สำเนา -- ธรรมเนียมที่ไฟล์เทสอื่นในสายนี้ใช้อยู่แล้ว)
   - ตรวจว่าแก้ NONCLAIM 1 แล้วไม่ได้เผลอเปลี่ยนถ้อยคำอื่นในย่อหน้าเดียวกันที่ยังจริงอยู่ (พบว่า
     ฉบับร่างแรกเผลอเปลี่ยน "pending RE-082's vital id" เป็น "pending GT-146's vital id" ทั้งที่
     ไม่ได้ตั้งใจแก้ประโยคนั้น -- ย้อนกลับเป็นถ้อยคำเดิม เพราะไม่มีหลักฐานในรอบนี้ว่า RE-082 ผิด
     และไม่ใช่ขอบเขตของรอบนี้ที่จะตัดสิน)
   - ยืนยันว่าไฟล์ทั้งสองที่แก้เป็น cp874-encodable (แม้จะเป็น ASCII ล้วนอยู่แล้ว) และสวีตเทส
     `tests/test_tree_is_cp874_safe.py` ผ่านเป็นส่วนหนึ่งของสวีตเต็ม

## ตัวเลขที่วัดได้

```
pirate-force-server ไฟล์ที่แตะ: 2
  - tests/test_mob_pickup_registry_wiring.py (ใหม่, 4 เทส)
  - src/pirateforce_foundation/mob_pickup.py (docstring เท่านั้น, NONCLAIM 1)
pf_bridge ไฟล์ที่แตะ: 2 (round record นี้, จดหมายนี้)
สวีตเต็ม pirate-force-server ครั้งแรก (ก่อนแก้ NONCLAIM ครั้งที่สอง): 5740 passed, 323 skipped,
  10606 subtests passed, 0 failed (143.29s)
สวีตเต็มครั้งที่สอง (หลังแก้ NONCLAIM + เปลี่ยน event assertion เป็นค่าคงที่): 5740 passed,
  323 skipped, 10606 subtests passed, 0 failed (139.98s) -- ตัวเลขเท่าครั้งแรกเป๊ะ (การแก้รอบ
  ที่สองเป็นแค่ผ่อนความแม่นของ 1 assertion ไม่เปลี่ยนพฤติกรรมที่วัดผ่าน/ตก) ผลย่อยที่รันก่อนหน้า
  (tests/test_mob_pickup_registry_wiring.py, tests/test_tree_is_cp874_safe.py,
  tests/test_mob_pickup.py, tests/test_mob_pickup_persist.py,
  tests/test_scene_scoped_combat_wiring.py, tests/test_foundation.py): 151 passed,
  548 subtests passed, 0 failed
git diff --check: silent
```

## ยังไม่ได้พิสูจน์

BUILD-006 การ wire สุดท้าย รอ `GT-146` (attended, ต้องมีคนหน้าเครื่องเกม) -- ไม่เปลี่ยน

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `p3olrt`
