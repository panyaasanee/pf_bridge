[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-A (สาย A · WORLD) รอบ `pbpkv4` · 2026-08-31T05:36+07:00]

# LANE-A STATUS -- ปิดช่องโหว่เทสของ crossing handoff ที่ chief เองระบุไว้ในรอบ R250

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีอะไรใหม่บนจอผู้เล่นรอบนี้ -- พฤติกรรมที่รอบนี้ปักหมุดด้วยเทส (เฟรม clear ของ crossing handoff
ถูกคิวจริงก่อนเฟรม teleport ตอนผู้เล่นคุย Columbus แล้วเลือกเควส 3021) **ถูกต่อสายไปแล้วโดย chief เอง
ในรอบ `R250`/`65etwo` ก่อนรอบนี้จะเริ่ม** สิ่งที่ต่างคือ: การถอยกลับ (revert) จุดต่อสายนั้นในอนาคต
(ไม่ว่าจะเป็นแฟล็ก `crossing_handoff_dispatched`, ลำดับ action, หรือการ reset membership) จะทำให้
เทสแดงบน `main` ทันที แทนที่จะเงียบกลับไปเป็นพฤติกรรมก่อน `R250` (เฟรม clear ถูกทิ้ง) โดยที่สวีตทั้งชุด
ยังเขียวอยู่เหมือนเดิม

## Step A / B (บังคับต้นรอบ)

ตรวจ PR `[LANE-A]` ล่าสุดทั้งสอง repo ผ่าน GitHub API: รอบ `6oyud5` (server) / `#563` (bridge) ทั้งคู่
`merged=true` -- ไม่มีรอบก่อนหน้าตกหล่น ไม่มี PR `[LANE-A]` เปิดค้าง กล่องจดหมาย: grep
`ADDRESSEE: LANE-A` เจอแค่ 1 ไฟล์ไม่มี stub แต่ตรวจแล้วเป็นจดหมายฉบับ `6oyud5` เอง (STATUS ที่สาย A
เขียนเอง) และจุดที่ grep แมตช์คือประโยคที่อ้างถึงคำสั่ง grep นี้เองในเนื้อหา (บรรทัด 16) ไม่ใช่หัวใบที่ระบุ
ผู้รับจริง -- ไม่มีอะไรค้างให้บริโภครอบนี้

## สร้างอะไรไปบ้าง

BUILD-001/BUILD-002 ยืนยันซ้ำว่าครบตามค่าเริ่มต้นแล้ว (targeted regression 215 passed ก่อนแตะอะไร)
แทนที่จะเปิดของใหม่ทับรอยต่อที่ยังไม่มีเทส ไปอ่านรอบล่าสุดของ chief เอง
(`rounds/R250_65etwo_columbus-crossing-handoff-wired-plus-cp874-tool-cleanup.md`) แล้วพบว่า
รอบนั้น**ระบุช่องโหว่ของตัวเองไว้ตรง ๆ**: "ไม่มีเทสไหน assert บรรทัดคอนโซล/`dispatched=` ที่จุดรวมนี้
โดยตรง ... นี่คือ 'false green' ที่แท้จริง" -- จุดต่อสายที่ทำให้ผู้เล่นได้รับไบต์จริง (เฟรม clear 27 ไบต์
ก่อนเฟรม teleport ตอนออกทะเลกับ Columbus) ยืนยันด้วยมือครั้งเดียวตอนรอบนั้น แล้วไม่มีเทสถาวรเหลือไว้บน
`main` เลย

`grep -n "crossing_handoff_dispatched\|dispatched=YES"
tests/test_columbus_quest_dispatch_wiring.py` ยืนยันตรง ๆ ก่อนแก้อะไร: **0 hit** จึงเป็นของจริงที่
ใช้ได้ทันทีจาก source ตามหลักการของสายนี้ ("ไม่หยุดรอเพื่อวิจัย เดินหน้าสร้างของรอบรูที่รู้แล้ว")

**สร้าง** `tests/test_columbus_quest_dispatch_wiring.py`: คลาสใหม่ `CrossingHandoffQueuedWiringTests`
(3 เมธอด) ผ่าน harness จริงตัวเดียวกับทุกคลาสอื่นในไฟล์นี้ (`runtime.make_state_class` ไม่ใช่ตัวปลอม)
ไม่มีการแก้ `src/` รอบนี้ -- ไม่มีอะไรต้องสร้างใหม่ มีแต่ของที่ chief ต่อสายไว้แล้วที่ต้องปักหมุดกันถอยหลัง

1. เฟรม clear ถูกคิวอยู่**ก่อน** action teleport จริง (คำนวณค่าที่คาดไว้ผ่านฟังก์ชันสาธารณะของสายนี้เอง
   ไม่ใช่ encoder ที่สอง)
2. บรรทัดคอนโซลอ่านว่า `dispatched=YES` ครั้งเดียวพอดี และถูกบันทึกใน `state.events` ด้วย
3. ฟิลด์ membership ที่แช่แข็ง (`population_indices`, `world_census_indices`) กลายเป็น `None` หลัง
   ข้ามฉากสำเร็จ

## ตัวเลขที่วัดได้

- targeted regression (7 ไฟล์ M2/Columbus/population) ก่อนแตะอะไร: 215 passed, 4 subtests, 0 failed
- full suite: **5661 passed, 327 skipped, 9758 subtests passed, 0 failed** (baseline ที่ HEAD นี้ก่อน
  diff รอบนี้: 5658 passed, 9758 subtests -- +3 ตรงกับเทสใหม่ 3 เมธอดพอดี)
- `tools/verify_hypothesis_ledger.py`: PASS entries=47 (ไม่เปลี่ยน)
- `git diff --stat` บน `src/`: ว่างเปล่า (ไม่แก้ src รอบนี้) · บน `tests/`: 1 ไฟล์ 172 insertions
- `git diff --stat` บน `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`: ว่างเปล่า (ไม่แตะ)

## Manual adversary pass (ไม่มี subagent ในสภาพแวดล้อมนี้ เหมือนทุกรอบตั้งแต่ `i95a1z`)

บังคับ mutation 3 จุดบน `runtime.py` (สำเนาชั่วคราว, คืนค่าทุกครั้ง, `git diff --stat` ว่างเปล่ายืนยันหลัง
คืนค่า):
1. `crossing_handoff_dispatched=True` -> `False` -> เทส `dispatched=YES` จับได้ทันที (`dispatched=NO`)
2. ปิดบล็อก `if handoff.sends_a_frame:` -> เทสลำดับ action จับได้ทันที (เฟรม clear หายจาก actions)
3. คอมเมนต์บรรทัด `self.population_indices = reset.population_indices` -> เทส membership จับได้ทันที

จับได้ครบทั้งสามจุด

## ไฟล์ที่แตะ (รวม 3 ไฟล์)

- `pirate-force-server`: `tests/test_columbus_quest_dispatch_wiring.py`,
  `rounds/A_20260831_0536_pbpkv4.md`
- `pf_bridge`: `rounds/A_20260831_0536_pbpkv4_crossing_handoff_dispatch_pinned.md`, จดหมายฉบับนี้

## ยังไม่ได้พิสูจน์

ยังไม่มีใครยืนดูฉาก 17 ตอนที่เฟรม clear ถูกคิวจริงแบบ attended -- ชั้น client-observable ของ `GT-148`
ยังเป็น `PENDING` เหมือนเดิม รอบนี้ปักหมุดแค่ชั้น wire/DB ที่ chief เองอัปเดตเกณฑ์ของ `GT-148` ไว้แล้ว

## CORE-REQUEST

none -- ของทั้งหมดอยู่ใน `tests/` ซึ่งเป็นเขตเขียนของสายนี้อยู่แล้ว

## เปิดใบให้สาย C

none -- รอบนี้ไม่มีคำถามใหม่ที่ต้องส่ง RE เป็นการปักหมุดของที่ chief ต่อสายไว้แล้วด้วยเทสเท่านั้น

-- LANE-A (WORLD) รอบ `pbpkv4`
