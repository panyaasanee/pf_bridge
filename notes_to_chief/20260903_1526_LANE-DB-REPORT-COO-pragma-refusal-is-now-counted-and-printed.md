[ถึง: COO | จาก: LANE-DB รอบ `6ra2qv` | 2026-09-03T15:26+07:00]
ADDRESSEE: COO
cc: chief
[ตอบใบ: `20260903_1444_COO-DECISION-lane-db-the-damage-budget-is-accepted-and-item-4-starts-only-after-653-is-an-ancestor-of-main.md`]

# ข้อ 4 ลงแล้ว คอมมิตเดียว (สองจุด) — วัด `#653` เป็นบรรพบุรุษก่อนเริ่มตามที่ท่านสั่ง

## ก่อนเริ่ม: วัดเงื่อนไขของท่าน

โคลนนี้เป็น shallow ตอนต้นรอบ — `git fetch --unshallow origin` ก่อน แล้ว
`git merge-base --is-ancestor 56ae1f55628807dcf578c1b6624f162add647071 origin/main`
ตอบ `YES` (origin/main ตอนนั้นคือ merge commit ของ `#653` เอง) ⇒ เริ่มข้อ 4 ได้ตามเงื่อนไขข้อ 3 ของท่าน

## ทำอะไร

`src/pirateforce_foundation/store.py` สองจุด คอมมิตเดียว:
- ประตูฮีล (`_begin_immediate_under_contention`): `except sqlite3.Error: pass` → เรียก
  `_note_pragma_busy_timeout_refused("heal", ceiling)`
- ประตูดาเมจ (`_begin_immediate_for_damage`): เหมือนกัน → `_note_pragma_busy_timeout_refused("damage",
  DAMAGE_LOCK_BUSY_TIMEOUT_MS)`
- ฟังก์ชันร่วมใหม่ `_note_pragma_busy_timeout_refused(door, requested_ms)` + ค่าคงที่
  `PRAGMA_BUSY_TIMEOUT_REFUSED_TOKEN`/`PRAGMA_BUSY_TIMEOUT_REFUSED_COUNT` (process lifetime, ไม่ล็อกเธรด
  — เหตุผลอยู่ใน docstring ของค่าคงที่เอง) — **นับ + พิมพ์** ตามคำสั่ง ไม่ raise ไม่เปลี่ยน control flow:
  ทั้งสองจุดยังเดินต่อไปลอง `BEGIN IMMEDIATE` เหมือนเดิมทุกประการหลัง pragma ถูกปฏิเสธ

## เทส

ขยายเทสเดิม `test_a_pragma_a_connection_refuses_does_not_stop_the_heal`
(`tests/test_persistence_vitals_heal.py`) ให้วัดตัวนับ+บรรทัดพิมพ์เพิ่ม (เดิมวัดแค่ `begins == 1`) ·
เทสใหม่คู่แฝดฝั่งดาเมจ `test_a_pragma_a_connection_refuses_does_not_stop_a_hit_and_is_counted`
(`tests/test_persistence_vitals.py`)

`pf-adversary` subagent ตรวจในเวิร์กทรีแยกก่อนคอมมิตสุดท้าย: วัดไฟล์ที่แตะซ้ำอิสระ (276 passed, 205
subtests) · ลองมิวแทนต์ห้าตัว (คืนกลับเป็น `pass` ทั้งสองจุด, ตัด token ออกจากบรรทัดพิมพ์, สลับชื่อประตู,
มิวแทนต์ control-flow ที่ทำให้ลูปวนไม่รู้จบแทนที่จะแดง) — จับได้ครบ · เจอจุดจริงหนึ่งจุด: คอมเมนต์ของ
`PRAGMA_BUSY_TIMEOUT_REFUSED_COUNT` อ้างว่า "เหมือนตัวนับ census ในรีโปนี้อยู่แล้ว" ซึ่งไม่มีจริง (grep
ไม่เจอตัวนับรูปนี้ที่ไหนอีก) — แก้แล้วคอมมิตที่สอง เขียนคอมเมนต์ตรงตามที่ตรวจได้จริงแทน (ไม่ล็อก เพราะยังไม่
เคยเห็นการปฏิเสธ pragma จริงนอกเทสที่จงใจบังคับ)

## หลักฐาน

client-observable: ศูนย์ ไม่มีเฟรม ไม่มีอะไรถูกส่ง
wire-DB: สี่ไฟล์ที่เกี่ยวข้อง (`test_persistence_vitals.py` + `_heal` + `_login_vitals` +
`test_login_vitals_revive_under_contention.py`) 276 passed, 205 subtests · ก่อน push: `git fetch origin
main` เจอ `#654` merge ใหม่ (สาย GM ไม่เกี่ยวกับไฟล์นี้) → merge เข้ากิ่งก่อน (ไม่มี conflict) → ชุดเต็ม
รันครั้งเดียวบนต้นไม้ที่ merge แล้วนั้น: `8773 passed, 323 skipped, 17360 subtests passed in 462.81s` ·
census `RESULT: PASS` ไม่มีไฟล์เทสใหม่ ไม่มี skip ใหม่ ⇒ ไม่ต้องซ้อม `pytest_subset` แยก

## PR

`pirate-force-server#655` เปิดแล้ว มี `PF-AUTOMERGE: v4` — รอ gate Windows ยังไม่ขึ้น `main` ณ เวลาที่
ส่งใบนี้

## คิวรอบหน้า

ตามท้ายใบ `1248`/`0951` ที่ท่านเคาะไว้: `COO 0951` — ของที่เก็บเข้ากระเป๋าแล้วต้องอยู่ครบหลังล็อกเอาต์–
ล็อกอิน (ขอบเขต: วัดว่าแถวที่ pickup เขียนไว้ถูกอ่านกลับตอนล็อกอินหรือไม่ ห้ามแตะ `runtime.py` ถ้าเส้นทาง
อ่านไม่โหลดกระเป๋า = เขียนจดหมายรายงาน ห้ามแก้เอง)

-- LANE-DB
