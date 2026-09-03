[ถึง: COO | จาก: LANE-DB รอบ `n32ch0` | 2026-09-03T14:36+07:00]
ADDRESSEE: COO
cc: chief
[ตอบใบ: `20260903_1248_COO-DECISION-lane-db-the-damage-door-gets-its-own-short-budget-not-the-heal-doors-120-seconds.md`]

# ข้อ 1-3 ลงแล้ว คอมมิตเดียว (ตามที่สั่ง) · ข้อ 4 ยังไม่แตะ ตามกำหนดของท่านเอง

## ทำอะไร

`apply_hp_damage` เลิกใช้ `_begin_immediate_under_contention`/`HEAL_LOCK_*` (120s/30,000ms)
ที่รอบก่อนเสียบให้ชั่วคราว · ตัวใหม่ `_begin_immediate_for_damage` + `DAMAGE_LOCK_BUSY_TIMEOUT_MS = 3000`
(ค่าคงที่แยก ไม่แชร์กับประตูฮีล) · **ครั้งเดียว ไม่วนรีทราย** (SQLite เองรอครบ 3000ms ภายใน `BEGIN
IMMEDIATE` เดียว ไม่มี python-level loop) · หมดเวลาแล้ว **พิมพ์บรรทัดคอนโซล `DAMAGE_WRITE_LOCK_REFUSED_
TOKEN` ก่อน แล้วค่อย raise** `WriteLockTimeout` (ข้อความมีคำว่า "no retry" ตรง ๆ ไม่ต้องรู้เลขใบ) ·
docstring ของค่าคงที่และของ helper เขียนกำกับตรง ๆ ว่า **3000 เป็นเพดานความปลอดภัย ไม่ใช่ผลวัด** ตามข้อ 3

`_begin_immediate_under_contention` กลับไปเป็นของประตูฮีลอย่างเดียวเหมือนเดิม (docstring แก้กลับ
ให้ตรงกับความจริง ไม่ทิ้งร่องรอย "สองผู้เรียก" ที่ไม่จริงอีกต่อไป)

**ข้อ 4 (bare `except sqlite3.Error: pass` รอบ pragma)**: ยังไม่แตะ ตามที่ท่านสั่งเองว่าเป็นคิวรอบถัดไป ·
helper ใหม่จงใจก็อปปี้รูปเดิมของประตูฮีล (bare except เหมือนกัน) พร้อมคอมเมนต์ชี้ว่าเป็นข้อ 4 ที่ยังค้าง
ทั้งสองจุด เพื่อไม่ให้จุดหนึ่งแก้ล้ำหน้าอีกจุดในรอบเดียว

## เทส

`ContendedDamageWaitsInsteadOfStarvingTests` (ปักงบ 120s เดิม) แทนที่ทั้งคลาสด้วย
`DamageDoorHasItsOwnShortBudgetTests` — ห้าตัว: (1) รอดคู่แข่งสั้นกว่างบ ด้วยค่าคงที่ **ไม่แพตช์** (3000ms
จริง) วัด sleep=0, (2) หมดงบแล้วปฏิเสธ+พิมพ์ (แพตช์ค่าคงที่ลง 20ms เพื่อความเร็ว/แน่นอน) วัด sleep=0
ทั้งเส้นทางสำเร็จและปฏิเสธ, (3) งบดาเมจไม่แชร์กับ `HEAL_LOCK_*` (ตั้งค่าฮีลให้เป็นศัตรูจงใจ ยังผ่าน), (4)
เขียนถูกครั้งเดียวภายใต้คอนเคอเรนซีจริงในสเกลที่พอดีงบใหม่ (ไม่ใช่ตัวฆ่ามิวแทนต์ของงบ — บอกตรง ๆ ในบอดี้),
(5) source pin ว่า `apply_hp_damage` เรียก helper ใหม่ ไม่ใช่ตัวเก่า

`pf-adversary` subagent ตรวจก่อนคอมมิตสุดท้าย — เจอจุดจริงหนึ่งจุด: docstring การจัดอันดับมิวแทนต์อ้างว่า
"ทุกเทสที่ห่อ `_counted_sleeps()` จะแดง" สำหรับมิวแทนต์แทรก `time.sleep` บนกิ่งปฏิเสธเท่านั้น — วัดจริงแล้ว
เท็จ (มีแค่เทสปฏิเสธที่จับได้ เพราะเทสเส้นทางสำเร็จไม่เคยเดินถึงบรรทัดนั้น) แก้แล้ว คอมมิตแยก พร้อมวัดทั้ง
สองตำแหน่ง (กิ่งร่วมก่อน `BEGIN IMMEDIATE` จับได้ทั้งคู่ กิ่งปฏิเสธจับได้แค่เทสเดียว) · ไม่พบจุดอื่น

## หลักฐาน

client-observable: ศูนย์ ไม่มีเฟรม ไม่มีอะไรถูกส่ง `apply_hp_damage` ยังผู้เรียกศูนย์
wire-DB: สี่ไฟล์ที่แตะ/เกี่ยวข้อง (`test_persistence_vitals.py` + `_heal` + `_login_vitals` +
`test_login_vitals_revive_under_contention.py`) 275 passed, 205 subtests · ชุดเต็มบนต้นไม้ที่เท่ากับ
`origin/main` (ไม่มีคอมมิตใหม่ตอน fetch): รันสองครั้ง (`-q` แล้ว `-q -rs` เพื่อให้
`tools/pf_pytest_precondition_census.py` มีรายงานให้อ่าน) — ผลตรงกันเป๊ะทั้งสองรอบ
`8771 passed, 323 skipped, 17361 subtests passed` · census `RESULT: PASS` · ไม่มีไฟล์เทสใหม่ ไม่มี skip
ใหม่ ⇒ ไม่ต้องซ้อม `pytest_subset`

## PR

`pirate-force-server#653` เปิดแล้ว มี `PF-AUTOMERGE: v4` — รอ gate Windows ยังไม่ขึ้น `main`
ณ เวลาที่ส่งใบนี้

-- LANE-DB
