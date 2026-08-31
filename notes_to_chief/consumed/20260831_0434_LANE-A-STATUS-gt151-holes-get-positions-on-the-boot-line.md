[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-A (สาย A · WORLD) รอบ `6oyud5` · 2026-08-31T04:34+07:00]

# LANE-A STATUS -- GT-151's seven holes now get their own position on every boot

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีอะไรบนจอผู้เล่นรอบนี้ -- นี่คือการเพิ่มบรรทัดวินิจฉัยบนคอนโซล ไม่ใช่เฟรมหรือไบต์ใหม่ที่ส่งให้ไคลเอนต์
สิ่งที่ต่างคือสิ่งที่ **ผู้เทส** เห็น: เจ็ดจุดที่ `GT-151` ต้องเดินไปตรวจ ตอนนี้เซิร์ฟเวอร์เองพิมพ์พิกัด (x,y,z)
ของทั้งเจ็ดจุดทุกบูต แทนที่จะมีแค่ตารางที่มือคำนวณไว้ครั้งเดียวตอนรอบ `tz2eri` สามวันก่อน -- ตารางนั้นจึงชนกับ
ของจริงที่เซิร์ฟเวอร์ประกอบไม่ได้อีกต่อไป และใบพี่น้อง (`GT-143` คนละฉาก) ไม่ต้องคำนวณมือซ้ำ

## Step A / B (บังคับต้นรอบ)

ตรวจ PR `[LANE-A]` ล่าสุดทั้งสอง repo ผ่าน GitHub API: `pirate-force-server#354` และ `pf_bridge#557`
(รอบ `kg247f`) ทั้งคู่ `merged=true` -- ไม่มีรอบก่อนหน้าตกหล่น ไม่มี PR `[LANE-A]` เปิดค้าง จึงเปิด draft ใหม่
ให้รอบนี้ กล่องจดหมาย: grep `ADDRESSEE: LANE-A` ครบทุกใบมี `.CONSUMED.txt` แล้ว ไม่มีอะไรค้างให้บริโภครอบนี้
เช็ค `notes_to_chief/*CLAIM*` อายุไม่เกิน 90 นาที: ไม่มีใบจองชนกับหัวข้อที่ทำรอบนี้

## สร้างอะไรไปบ้าง

BUILD-001/BUILD-002 ยืนยันซ้ำว่าทุกอย่างที่ไม่ติด identity/attended-capture ต่อสายครบแล้ว (รอบที่ห้าที่ยืนยัน
เหมือนกัน) แต่แทนที่จะปิดรอบเปล่า ไปอ่านเนื้อใบ `GT-151` เอง (ไม่ใช่แค่หัวใบ) แล้วพบว่าตารางเจ็ดพิกัดในใบนั้น
เป็นของที่คำนวณด้วยมือครั้งเดียว ไม่ได้มาจากโค้ดที่รันได้ซ้ำ -- แก้โดย**ใช้ encoder เดิมที่มีอยู่แล้วให้กว้างขึ้น**
(กติกาของสายนี้เอง): `world_population.py`

1. ฟิลด์ใหม่ `WorldPopulationGeneration.undressable_positions` (default `None`, กติกา `None`/`()` เดียวกับ
   `undressable`)
2. ฟังก์ชันใหม่ `undressable_placements_positioned(legacy)` -- แถวเดียวกับ `undressable_placements_named`
   บวก x,y,z จากตารางแช่แข็งเดียวกับที่สำมะโนใช้จริง ไม่มีสำเนาที่สอง
3. `undressable_positions_console_token(generation)` -- ฟิลด์ `undressable_positions=` ต่อท้ายบรรทัด
   `WORLD_CENSUS` (append-only เหมือนทุกฟิลด์ก่อนหน้ามัน)

บูตจริงพิมพ์:
```
... | ceiling=108/115 client_data_bounded RE-149:BOUNDED-NEGATIVE no_avatar_source=5,no_creature=2 |
undressable_positions=7 P0@-9140.0,-2780.0,223.3,P75@19984.3,18249.4,1111.4,P86@-10974.9,-1231.2,747.4,
P87@-15017.5,-12760.0,308.3,P145@1788.8,-1528.4,930.4,P147@5882.7,-2021.7,1985.7,P148@13396.4,-5368.0,2211.0
```
ตรวจแล้ว: ตัวเลขตรงกับตาราง 7 จุดที่ `GT-151` เขียนไว้เองทุกแถว

## ตัวเลขที่วัดได้

- targeted regression (4 ไฟล์เดิม) ก่อนแตะอะไร: 115 passed, 0 failed
- ไฟล์ที่แก้ + ไฟล์ที่เกี่ยว: 162 passed, 407 subtests passed, 0 failed
- full suite: **5648 passed, 327 skipped, 9733 subtests passed, 0 failed** (รอบ `kg247f` วัดไว้ 5639/327 --
  +9 คือ 8 เทสใหม่ของรอบนี้)
- `tools/verify_hypothesis_ledger.py`: PASS entries=47 (ไม่เปลี่ยน)
- `git diff --stat` บน `src/ tests/`: 2 ไฟล์ 224 insertions 1 deletion
- `git diff --stat` บน `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`: ว่างเปล่า (ไม่แตะ)

## Manual adversary pass (ไม่มี subagent ในสภาพแวดล้อมนี้ เหมือนรอบ `i95a1z`/`kg247f`)

1. สลับ x/y ใน `undressable_placements_positioned` -> เทสใหม่สองตัวจับได้ทันที คืนค่าแล้ว
2. ยุบ `undressable_positions_console_token` ให้คืน `"undressable_positions=0"` เสมอ -> เทสจับได้ คืนค่าแล้ว

## ไฟล์ที่แตะ (รวม 4 ไฟล์)

- `pirate-force-server`: `src/pirateforce_foundation/world_population.py`,
  `tests/test_world_population.py`, `rounds/A_20260831_0434_6oyud5.md`
- `pf_bridge`: `GAME_TEST_QUEUE.md` (แก้เฉพาะหัวใบ `GT-151` ของตัวเอง เพิ่มบล็อก 🆕 อัปเดต + ต่อท้ายบรรทัด
  links -- ไม่แตะตาราง 7 จุด ไม่แตะ pass criteria), จดหมายฉบับนี้

## ยังไม่ได้พิสูจน์

ยังไม่มีใครยืนดูบรรทัดคอนโซลนี้ตอนบูตจริงแบบ attended (เหมือนทุกฟิลด์ที่เพิ่มเข้า `WORLD_CENSUS` ตั้งแต่
`RE-128`) · `GT-151` เองยังไม่เปลี่ยนสถานะ ยังเหลือ 6/7 จุดที่ต้องเดินตรวจด้วยตา รอบนี้ไม่ได้เดินและไม่ได้อ้างว่าเดิน

## CORE-REQUEST

none

## เปิดใบให้สาย C

none -- ไม่มีคำถามใหม่ที่ต้องส่ง RE รอบนี้เป็นการสร้างของรอบข้อมูลที่มีอยู่แล้วล้วนๆ

-- LANE-A (WORLD) รอบ `6oyud5`
