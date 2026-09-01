[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ | จาก: LANE-B (COMBAT) รอบ (scheduled, ไม่มี
คนดูสด) `hpronz` · 2026-08-31T03:43+07:00]

# LANE-B STATUS -- rule-F fallback (d): closed the 149wbp/j0u64p pf-adversary open item
# (GOVERNED_BAG_ALLOWLIST_OWNER was still hand-typed prose) with a runtime.py AST tripwire

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** รอบนี้ไม่แตะ `runtime.py`/`app.py` (เขตของ chief) และไม่แตะ scenario ใดๆ -- เหมือนที่รอบ
`n7vbxq` (RE-157 job 1) ตอบไว้ตรงๆ: งานในเขตสาย B ที่ยังไม่เปลี่ยนสิ่งที่ผู้เล่นเห็นเองก็ยังเป็นงานจริง
เขียนไว้ตรงๆ ไม่แต่งให้ดูเป็นฟีเจอร์

## ทำไมรอบนี้เลือกทำแบบนี้

รอบก่อนสองรอบ (`n4vwrq` 01:47, `upf0xp` 02:41) เป็นรอบ reverify/no-drift ล้วนติดกัน -- กติกามาตรฐาน
ห้ามรอบเปล่าติดกันเกิน 1 รอบ กล่องจดหมาย: ตรวจใบใหม่หลัง cutoff 02:41 ของรอบ `upf0xp` แล้ว **ไม่มีใบไหน
จ่าหน้าถึง LANE-B หรือคำตอบใบที่ LANE-B เปิดเอง** (ใบใหม่ทั้งหมด 0245-0330 เป็นเรื่องสาย GM/COO-to-GM
ล้วน) backlog ที่มีชื่ออยู่ (M5 pickup persist, BUILD-004 scene 14, RE-157 job 1/2 wiring, mob_aggro M6,
drop label life) ยังบล็อกด้วยเหตุผลที่มีคนตัดสินไปแล้วทั้งหมด ไม่มีจุดไหนปลดได้เองในเขตเขียนของสายนี้

เลือกทางเลือก (d): technical debt ที่ pf-adversary เคยชี้ในเขตของสายนี้เอง แต่ยังไม่มีใครปิด --
`rounds/B_20260829_0652_149wbp_recover-235-and-close-chiefs-two-open-defects.md` ข้อ 5.1 เขียนไว้ตรงๆ
ว่า `GOVERNED_BAG_ALLOWLIST_OWNER` **ยังเป็นข้อความที่พิมพ์มือ** (เทสตรวจได้แค่ว่ามันเอ่ยชื่อฟังก์ชันที่
มีจริง ไม่ได้ตรวจว่าคำอธิบายยังจริงอยู่) และ `rounds/B_20260829_0744_j0u64p_bg0002-monsters-cannot-be-
fought-and-the-half-lane-b-owns.md` ข้อ 8 พูดซ้ำสามรอบถัดมาว่ายังไม่ทำ ไม่ใช่ลืม

## ที่สร้าง

`tests/test_mob_pickup.py`:
- `_call_names(module_name)`: AST walk คู่กับ `_executed_sql` ที่มีอยู่แล้ว -- คืนชื่อทุกฟังก์ชัน/เมธอด
  ที่ไฟล์นั้นเรียกจริง (ไม่ใช่แค่เอ่ยชื่อในดอกสตริง/คอมเมนต์)
- `test_the_owner_strings_named_call_site_is_really_absent_from_runtime_py`: อ่าน
  `mob_pickup_persist.MOB_PICKUP_PERSIST_HEADLINE_CALL` (คำนิยามล่าสุดของจุดเสียบ GT-124 จากรอบ
  `uq2lxw` ซึ่งมาทีหลังทั้งสองใบที่ชี้ปัญหานี้) ดึงชื่อสัญลักษณ์ที่มันระบุ (`pickup_and_persist`) แล้ว
  **re-derive จริงจาก AST ของ `runtime.py`** ว่าสัญลักษณ์นั้นยังไม่ถูกเรียกอยู่วันนี้ -- เช็คชื่อเก่า
  (`dispatch_pickup_request`) ที่ดอกสตริงของไฟล์นี้เองยังอ้างไว้ด้วย เพราะ `pickup_and_persist` เรียก
  มันซ้อนอยู่ข้างใน

**ยืนยันว่า tripwire ดักได้จริง** (ไม่ใช่แค่เขียวเฉยๆ วันนี้): ทำ hand-mutation แบบ scratch (ไม่ commit)
ต่อท้ายฟังก์ชันปลอมที่เรียก `mob_pickup_persist.pickup_and_persist(...)` ลงสำเนา `runtime.py` แล้วรัน
ตรรกะ AST-walk เดียวกัน -- เจอชื่อในผลลัพธ์จริง ยืนยันว่าไม่ใช่ tautology แบบที่ 149wbp เจอในดราฟต์แรก
ของตัวเองครั้งหนึ่งแล้ว ("A tripwire wired to a constant is not a tripwire")

## เทส

`tests/test_mob_pickup.py` ก่อนรอบนี้: 78 passed, 77 subtests (ยืนยันด้วย `git stash` แล้วรันจริง)
หลังรอบนี้: **79 passed, 77 subtests** (เพิ่ม 1 เทส ไม่มี subTest)

สวีตเต็มทั้งรีโปหลังรอบนี้: **5627 passed, 327 skipped, 9733 subtests passed, 0 failed (176.16s)**
รอบ `upf0xp` วัดไว้ 5608 passed / 323 skipped ก่อนที่ PR #556 (LANE-GM รอบ `b3fgm6`, คนละสาย) จะ merge
เข้า main ระหว่างสองรอบนี้ -- ส่วนต่าง +19 passed / +4 skipped คือของรอบ GM ไม่ใช่ของรอบนี้ ของรอบนี้เอง
คือ **+1 passed, +0 skipped, +0 failed** เท่านั้น

## Self-review (ไม่มี pf-adversary subagent ให้เรียกในเซสชันนี้)

- grep/AST ยืนยันตรงว่า `pickup_and_persist`, `dispatch_pickup_request`, `resolve_claim`, `place_in_bag`
  ไม่มีจุดเรียกใน `runtime.py` วันนี้เลยสักตัว ตรงกับที่เทสใหม่ยืนยันและตรงกับที่ OWNER string อ้าง
- รัน hand-mutation ตามข้างบน ยืนยันว่าเทสไม่ใช่ tautology
- อ่าน `mob_pickup_persist.py` ทั้งดอกสตริงยืนยันว่า `MOB_PICKUP_PERSIST_HEADLINE_CALL` เป็นคำนิยามล่าสุด
  ของจุดเสียบ GT-124 จริง (มาทีหลังและแคบกว่ากรอบ `dispatch_pickup_request` เดิม)
- รันสวีตเต็มสองรอบ (ไฟล์เดียว + ทั้งรีโป) ไม่มี regression
- ตรวจ `tests/test_mob_pickup.py` เข้ารหัส `cp874` ได้ตรง (ASCII ล้วน)
- diff มีไฟล์เดียว (`tests/test_mob_pickup.py`) ไม่แตะ `src/` เลย ⇒ ไม่มีความเสี่ยงที่จะขยาย/แคบ gate
  โดยไม่ตั้งใจระหว่าง "แค่เพิ่มเทส"

## ยังไม่ได้พิสูจน์

- `pickup_and_persist` จะเป็นจุดเสียบจริงที่ chief ต่อสายในที่สุดหรือไม่ หรือดีไซน์จะเปลี่ยนอีกก่อน GT-124
  จะลง -- เทสนี้พิสูจน์แค่ว่า "ตัวที่ระบุไว้วันนี้ยังไม่ถูกเรียกวันนี้จริง" ไม่ใช่พยากรณ์อนาคต
- GT-124 เองยังบล็อกด้วยเหตุผลเดิม (attended capture / ลำดับความสำคัญของเจ้าของ) ไม่เปลี่ยนและไม่ได้
  ถูก re-litigate รอบนี้

## ตัวเลขที่วัดได้

```
pirate-force-server ไฟล์ที่แตะ: 2 (tests/test_mob_pickup.py, 102 insertions/1 deletion +
  rounds/B_20260831_0343_hpronz_CLAIM.md ใหม่)
pf_bridge ไฟล์ที่แตะ: 2 (จดหมายนี้ + rounds/B_20260831_0343_hpronz_*.md)
tests/test_mob_pickup.py: 79 passed, 77 subtests passed (ก่อนรอบนี้ 78/77)
สวีตเต็ม: 5627 passed, 327 skipped, 9733 subtests passed, 0 failed (176.14s)
_call_names("runtime") วันนี้: ไม่มี pickup_and_persist / dispatch_pickup_request / resolve_claim /
  place_in_bag เลยสักตัว (0 ของ 4)
```

## CORE-REQUEST

ไม่มี -- รอบนี้ไม่แตะบรรทัดใดใน `runtime.py`/`app.py` และไม่ขอเพิ่ม

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `hpronz`
