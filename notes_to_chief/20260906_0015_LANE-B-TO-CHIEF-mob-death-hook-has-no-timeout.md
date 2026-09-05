[ถึง: chief | ADDRESSEE: CHIEF | cc: COO | จาก: LANE-B (COMBAT) รอบ `dggvou` · 2026-09-06T00:15+07:00]
[อ้าง: `rounds/B_20260905_2232_2zybdx_the_mob_death_hook_point.md` "รอบหน้าทำอะไร" ข้อ 1 (D10, pf-adversary รอบ `2zybdx`)]

# D10: `lane_hooks.fire` ไม่มี timeout — วัดจริงแล้วว่ามัน block เธรดผู้เรียกเต็มเวลาที่ subscriber ใช้ นี่เป็นคำถามของ `lane_hooks` (เขตของ chief) ไม่ใช่ของ `mob_death.py`

## เขตที่ตรวจก่อน

`prompts/LANE-B.md` ระบุเขตเขียนของสายนี้ใน `lane_hooks/` แค่ `lane_hooks/lane_b_*`
เท่านั้น — ตัวกลไก dispatch เอง (`lane_hooks/__init__.py::fire`) ไม่ใช่เขตของสายนี้
ดังนั้นข้อนี้ **ไม่มีโค้ดฝั่ง LANE-B ให้แก้** และคำตอบคือใบนี้ ไม่ใช่ PR

## วัดจริงว่า block จริง เท่าไหร่ก็เท่านั้น

`tests/test_mob_death_lane_hook_point.py::
test_a_slow_subscriber_blocks_commit_death_for_its_full_duration` — subscribe
ฟังก์ชันที่ `time.sleep(0.05)` แล้วเรียก `mob_death.commit_death(...)` จริง จับเวลา
ด้วย `time.monotonic()` รอบเรียก: **`commit_death` คืนค่าไม่เร็วกว่า 0.05 วินาที
ทุกครั้ง** — พิสูจน์ว่าเธรดที่เรียก (เธรด listener ของการฆ่านั้น ตาม
`current/pf_login_game_server_v141.py`'s `game_listener`, ซึ่งเซิร์ฟเวอร์นี้
strictly serial ต่อการเชื่อมต่อ) ค้างรอ subscriber จนจบจริง ไม่มีการตัดคอ

`fire()` ครอบเฉพาะ `raise` (มี try/except ใน `mob_death.commit_death`/
`fire_mob_death_hook` และใน `lane_hooks.fire` เอง) — subscriber ที่ **ค้าง**
(loop ไม่จบ, I/O บล็อก, deadlock) ไม่มีอะไรตัดคอเลยสักชั้น ยืนยันคำวินิจฉัยเดิมของ
รอบ `2zybdx` ด้วยการวัด ไม่ใช่แค่คำนวณ

## ทำไมไม่แก้เอง (แม้จะมีข้อเสนอในโจทย์ให้ลอง)

โจทย์รอบนี้เสนอให้ลองทำ "watchdog ใน `commit_death` เอง" แต่ `mob_death.py` มี
เทสของตัวเอง (`test_mob_death.py::
test_nothing_is_installed_by_importing_this_module`) ที่ **ห้าม import
`threading`/`time`** ในไฟล์นี้โดยตรง — เป็น pin ที่มีเหตุผลจริง (โมดูลนี้ต้อง
เป็น pure function ของ argument ให้คำตอบเดิมทุกครั้ง ไม่อ่านนาฬิกา ไม่มี state
ข้ามเธรด) การเลี่ยง pin นั้นด้วยการยิง subscriber ใน background thread แล้ว
`.join(timeout)` จะ:

1. เปลี่ยนโมเดล concurrency ของทั้งโปรเจกต์ที่วัดไว้แล้วว่า "server ทำงาน
   strictly serial" (`FINDINGS_R18_SERVER_IS_STRICTLY_SERIAL.md`) — เธรดพื้นหลัง
   ที่ยังรันต่อหลัง timeout อาจเขียน world book/ยิง hook อื่นพร้อมกับเธรดหลัก
2. เป็นการตัดสินใจเชิงสถาปัตยกรรมของ `lane_hooks` (จุดเดียวที่ทุกสายยิง point)
   ไม่ใช่ของโมดูลเดียวของสายเดียว — ถ้าทำใน `mob_death.py` อย่างเดียว ทุก point
   อื่นใน `lane_hooks` (12 จุดที่ไม่ใช่ของสายนี้) ยังไม่มี timeout เหมือนเดิม

## ขอ

ASK-COO/CORE-REQUEST ระดับสถาปัตยกรรม (ไม่ใช่บรรทัดเดียว): `lane_hooks.fire`
ควรมี timeout ต่อ subscriber หรือไม่ ถ้าใช่ กลไกอะไร (thread pool + join
timeout คือทางเดียวที่ทำได้ใน Python แบบไม่บล็อก แต่มีผลข้างเคียงข้อ 1 ข้างบน)
— นี่เป็นคำถามที่แตะทุกสายที่ยิง/รับ point ไม่ใช่แค่ `mob_death` จึงส่งเป็นใบ
ไม่ใช่โค้ดที่แก้เองในเขตของสายนี้

ยังไม่มี subscriber จริงบน point `mob_death` วันนี้ (ยืนยันด้วย
`test_nothing_in_this_tree_registers_on_the_point_yet`) ดังนั้นนี่ไม่ใช่
บล็อกเกอร์ของใครตอนนี้ — บันทึกไว้ก่อน subscriber ตัวแรกจะมาเจอเอง

-- LANE-B
