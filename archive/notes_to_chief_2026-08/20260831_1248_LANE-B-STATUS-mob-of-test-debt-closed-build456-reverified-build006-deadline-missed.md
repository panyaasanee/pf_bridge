[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ | จาก: LANE-B (COMBAT) รอบ `p0qia9`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-08-31T12:48+07:00]

# LANE-B STATUS -- pf-adversary technical-debt item closed, BUILD-004/5/6 reverified no drift, BUILD-006 deadline now missed

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** รอบนี้ไม่ใช่รอบเกมเพลย์ -- ปิดหนี้เทคนิคที่ `pf-adversary` ชี้ รายละเอียดเต็มอยู่ใน
`pirate-force-server/rounds/B_20260831_1239_p0qia9.md`, `pirate-force-server#384`.

## สรุปสั้น

1. Protocol A: PR #380 ของสาย B (`pirate-force-server`) ปิดแบบ `merged=false` แต่เนื้องานจริง
   push ตรงเข้าไปที่ branch ที่ถือล็อกของ PR #363 ซึ่ง merge แล้วที่ 04:45:20Z (ยืนยันด้วย
   `pull_request_read get`) -- ไม่มีอะไรต้อง cherry-pick กู้คืน
2. Protocol B: ไม่มีใบใหม่จ่าหน้า `ADDRESSEE: LANE-B` ที่ยังไม่ consumed ตั้งแต่ R256 -- ใบ
   `20260831_1150_LANE-B-ASK-COO` (round-lock livelock + BUILD-006 deadline) ยังรอ COO ตอบ
3. Lock: ไม่มี `[LANE-B]` PR เปิดค้างในทั้งสอง repo ตอนเริ่มรอบ (มีแต่ `[LANE-A]` #383/#593) --
   เปิด draft PR ใหม่ยึดล็อก: `pirate-force-server#384`, `pf_bridge#594`
4. BUILD-004/005: ยืนยันซ้ำว่ายังอยู่ ไม่ drift จากรอบก่อน (ผ่านสวีตเทสเต็ม)
5. **BUILD-006 (M5, กำหนด 31 ส.ค. 12:00) พลาดกำหนดแล้ว** -- เส้นทางเขียน + store insert
   ทำและเทสแล้ว เหลือจุดเดียวคือ wire call site ใน `runtime.py` (ของ chief) ซึ่งต้องรู้ opcode
   ที่ต้องมาจาก `GT-146` (attended, ยัง `PENDING` หัวคิว) รอบ unattended ปลดเองไม่ได้ -- แจ้งซ้ำจาก
   รอบ `3oo982`/`#380`, สถานะไม่เปลี่ยน
6. หนี้เทคนิคที่ปิดรอบนี้: `pf-adversary` สแกนโมดูล combat/mob/loot ของสาย B ทั้งหมด (grep
   ครอบคลุม combat/mob/loot/drop/spawn/member/roster/aggro/pickup/ledger + cross-reference
   AST กับทุกไฟล์เทส) พบจุดเดียวที่ปลอดภัยพอจะแก้: `MobAiRegister.mob_of()`
   (`mob_ai_control.py:557-558`) ไม่มีจุดเรียกใช้เลยทั้ง `src/` และ `tests/` ขณะที่ accessor คู่กัน
   `state_of()` มีเทสคุม ~18 assertion เลือก **พินด้วยเทสตรง 2 ตัวใหม่** แทนการลบ
   (`tests/test_mob_ai_control.py::RegisterTests`) เพราะรูปทรงเหมือน `state_of` เป๊ะและไม่มี
   หลักฐานว่าตั้งใจจะเลิกใช้ ไม่พบข้อบกพร่องอื่นในโมดูลที่ตรวจรอบนี้
   (`mob_aggro.py`/`mob_combat_membership.py`/`mob_ledger_admission.py`/
   `mob_pickup_persist.py`/`mob_scene_recompose.py`/`trade_session_membership.py`/
   `loot_roll.py` บางส่วน) -- ไม่ได้ตรวจละเอียดทุกไฟล์ (`mob_death.py` 2767 บรรทัด,
   `mob_pickup.py` 2018 บรรทัด, `mob_diag_multi_object.py`, `mob_census_wire_count.py`,
   `field_mob_tables_bg0015.py` ได้รับความสนใจน้อยหรือไม่ได้แตะรอบนี้)

## หมายเหตุ -- ระบบสั่งงานที่ launch รอบนี้อ้างข้อมูลเก่ากว่าปัจจุบันมาก

เช่นเดียวกับที่รอบ `o9ei0n` เคยบันทึกไว้แล้ว (`20260831_0542_LANE-B-STATUS-*.md`): คำสั่งงาน
อ้าง "RE-098 ค้างให้สาย B บริโภค" และ "RE-067 ยังเปิด" ทั้งสองปิดไปตั้งแต่ ~27 ส.ค. (ประมาณ
R172) ไม่ใช่งานค้างจริง -- ไม่ต้องแก้อะไรเพิ่ม แค่ยืนยันซ้ำว่า orchestrator snapshot ยังไม่รีเฟรช

## ตัวเลขที่วัดได้

```
pirate-force-server ไฟล์ที่แตะ: 3 (round-claim, 2 เทสใหม่ใน tests/test_mob_ai_control.py, round record)
pf_bridge ไฟล์ที่แตะ: 3 (round-claim, round record นี้, จดหมายนี้)
สวีตเต็ม pirate-force-server: 5704 passed, 327 skipped, 10238 subtests passed, 0 failed (142.94s)
git diff --check: silent
```

## ยังไม่ได้พิสูจน์

BUILD-006 การ wire สุดท้าย รอ `GT-146` (attended, ต้องมีคนหน้าเครื่องเกม)

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `p0qia9`
