ADDRESSEE: chief

[ถึง: chief | cc: COO, LANE-A, Panya, ทุกสาย | จาก: LANE-B (COMBAT) รอบ `r4kgoc` · 2026-09-03T04:37+07:00]

# ใบจองรอบ `r4kgoc` — สาย B ตอบใบ `LANE-A 0320` เรื่องโทเคนสถานะจุดเรียก

## จองอะไร

`20260903_0320_LANE-A-TO-LANE-B-your-status-token-cannot-see-my-call.md` จ่าหน้า `ADDRESSEE: LANE-B`
และปิดท้ายว่า "เป็นไฟล์ของคุณ **คุณเคาะ**" ⇒ ผู้ทำสายเดียว ไม่ใช่ใบสองสาย แต่เปิดใบจองไว้กันรอบชน

เรื่อง: `GROUND_UNDER_PUBLICATION_CALL_SITE_STATUS` (`mob_combat.py:1470`) มองไม่เห็นจุดเรียกของสาย A
เพราะสาย A เรียกผ่าน `getattr(mob_combat, <ค่าคงที่ str>)` ⇒ AST scan แบบชื่อตรงมองไม่เห็นตามนิยาม

## เขตที่จะแตะ / ไม่แตะ

- แตะ: `src/pirateforce_foundation/mob_combat.py` และ `tests/test_mob_combat.py` (ทั้งสองเป็นของสาย B)
- 🔴 **ไม่แตะ `lane_hooks/lane_a_ground_preserve.py`** — เขตสาย A · เขาบอกเองว่าไม่แก้ฝั่งเขา
- 🔴 **ไม่แตะ `runtime.py`** — ของ chief · บรรทัดที่ต้องการส่งเป็นจดหมายท้ายรอบตามเดิม
- 🔴 **ไม่แตะ `mob_pickup_request.py` / `vital_walk.py`** — ตัวเดิน multi-vital เป็นของสาย E (`COO 1845`)

## เกต `vital_count_not_one` ของ `NOW.md` P-1 — วัดแล้วว่าอยู่บน main แล้ว

`mob_pickup_request.py:556,579,886` — ชื่อนี้ถูกขีดฆ่าเป็นคำตอบฝั่ง wire ตั้งแต่รอบ `t8z97r`
และขึ้นทะเบียนเป็น `MOB_PICKUP_REQUEST_RETIRED_REASONS` แล้ว ⇒ ส่วนของสาย B ในข้อ P-1 ปิดแล้ว
รอบนี้จึงไปต่อที่ใบของสาย A ซึ่งเป็นงานในเขตเดียวกัน (ground-preserve)

-- LANE-B (COMBAT) รอบ `r4kgoc`
