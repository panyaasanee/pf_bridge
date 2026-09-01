[ถึง: chief, COO | ADDRESSEE: chief | จาก: LANE-B (COMBAT) รอบ scheduled `i7cwdh`, 2026-09-01T21:50+07:00]

# LANE-B-STATUS -- ปิดหนี้เทคนิค: inventory.py ไม่มี tests/test_inventory.py เอง (แก้แล้ว), P-1/P-2/P-3 ยังไม่ขยับ

## ต้นรอบ

- `NOW.md` (ตรวจล่าสุด 21:54): P-1/P-2/P-3 ยังไม่ขยับ, GT-146/ใบเทสตีมอนทุกใบยังห้ามทำ ตามเดิม
- ไมล์สโตน BUILD-004/5/6 ยังพัก (PANYA-ORDER 20260901_0215) -- รอบนี้ไม่เพิ่มพื้นผิว build ใหม่
- 🔴 รอบก่อนหน้า (`unkjpn`, 19:41) เป็นรอบเปล่า (ไม่แตะ source) และไฟล์ `rounds/B_*_unkjpn_*.md` ฝั่ง
  `pirate-force-server` ไม่เคย push ขึ้น origin เลย (หายทั้งรอบตามกฎบ้าน) -- รอบนี้จึงหางานจริงมาทำ
  ตามที่ `unkjpn` ทิ้งท้ายไว้ว่าจะทำ

## สิ่งที่พบและปิด

`src/pirateforce_foundation/inventory.py` (549 บรรทัด, ตัวโมเดล Backpack หลักของ BUILD-006/M5) ไม่มี
`tests/test_inventory.py` ของตัวเองมาตั้งแต่แรก ทั้งที่ 13 ไฟล์เทสอื่นอิมพอร์ต symbol จากมันโดยอ้อม
(ผ่านเลนส์ของฟีเจอร์ตัวเองเท่านั้น) และสองฟังก์ชันที่ `runtime.py` เรียกจริงบนทุก inbound ItemOperate
request (`parse_merge_candidate` ที่ `:6999`, `is_exact_merge_request` ที่ `:1459`) ไม่มีเทสไฟล์ไหน
อ้างชื่อเลยแม้แต่บรรทัดเดียวก่อนรอบนี้ (ยืนยันด้วย grep ก่อนเขียน)

สร้าง `tests/test_inventory.py` ใหม่ -- 47 เทสตรง ครอบทุกฟังก์ชัน public (ทั้งสอง gate, ทั้งสามการ
กลายพันธุ์ที่ควบคุม, ทั้งสามตัวประกอบไวร์ ItemOperate, ตัวเข้ารหัส Backpack, และคู่ parse/exact-request)
รวมเทสที่พาร์สไบต์จริงของ `V111_MERGE_REQUEST_PC` ผ่าน `legacy.parse_outer()` ตัวจริงแล้ว mutate ทีละ
ไบต์เพื่อพิสูจน์ว่าสองฟังก์ชันที่ไม่เคยมีเทสมาก่อนแยกกรณีถูกจริง ไม่ใช่คืนค่าคงที่ (รายละเอียด byte-offset
คำนวณด้วยมือและยืนยันซ้ำก่อนวางเทส -- ดูใบ round แนบ)

**ไม่แก้ `src/` แม้แต่บรรทัดเดียว** -- ไฟล์เดียว ใหม่ทั้งไฟล์ ผลกระทบพฤติกรรม runtime = ไม่มี

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** รอบนี้เป็นการปิดหนี้เทคนิคด้านเทสล้วน ไม่แก้โค้ดที่รัน

## จดหมายที่พบแต่ตัดสินใจไม่สร้างโค้ดจากรอบนี้

`20260901_2015_KA1B-TO-LANE-B-drop-model-selector-field-is-not-on-our-wire.md` (ยังไม่มี
`.CONSUMED.txt`) -- Codex ปิด static ว่า client's ground-drop model selector (`n_DROPMODEL_TYPE`)
อ่านจากช่องที่ `mob_loot.py`'s element mask `0x12` ไม่เคยส่งเลย (`0x04`/`0x08`/`0x20`) พร้อมวิธีพิสูจน์
ผิดราคาถูก (เพิ่มทีละ bit, สาม mask candidate) -- **ข้อสรุปเป็น [สมมติฐาน] ที่ผู้เขียนใบเองประกาศชัดว่ายัง
ไม่มีใครพิสูจน์บนจอ** สายนี้ตัดสินใจไม่สร้างโค้ดจากมันรอบนี้ เพราะ (1) ต่อ `ground_loot_hypothesis.py`
(HYP-PF-032) ด้วย mask ใหม่ยังเป็นการเพิ่มพื้นผิว probe อีกชุด ไม่ใช่ default-runtime path และ
(2) ไม่มีไคลเอนต์จริงในเซสชันนี้ให้พิสูจน์ผิด/ถูกได้ -- ฝากให้ COO/chief ตัดสินว่าจะเปิด GT attended
experiment ให้ Panya รันสามขั้นตามที่ใบเสนอหรือไม่ (ไม่เปิดใบสาย C ใหม่ เพราะฝั่ง static RE Codex ปิดแล้ว
สิ่งที่เหลือคือรอบ attended ไม่ใช่ RE เพิ่ม)

## ตัวเลขที่วัดได้

```
tests/test_inventory.py (ใหม่): 47 passed
11 ไฟล์เทสที่แตะ inventory.py โดยตรง/อ้อม: 291 passed, 1017 subtests passed
git diff --stat: 1 file changed (untracked, ใหม่ทั้งไฟล์), ไม่มีไฟล์ src/ ถูกแก้
สวีตเต็ม: 6545 passed, 327 skipped, 13766 subtests passed, 0 failed (176.17s)
```

## ยังไม่ได้พิสูจน์

- P-1 (`GT-188`), P-2 (P0-3 quest mark), P-3 -- ยังไม่ขยับ, ไม่ใช่พื้นผิวของสายนี้รอบนี้
- ใบ `20260901_1838_LANE-B-REPLY-re157-job2-scope-gap-option-c-spec.md` (สเปกสองจุดใน `runtime.py`
  ที่ยังรอ chief หยิบ) ยังไม่มี `.CONSUMED.txt`

## CORE-REQUEST

ไม่มี (รอบนี้ไม่แตะ `runtime.py`/`app.py`)

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT)
