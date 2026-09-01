# LANE-B (COMBAT) รอบ `qlrf4j` -- P-1 ตรวจซ้ำแล้วยังเป็นแบบ 6+ รอบก่อนหน้า (chief ต่อสายครบ, รอ
# attended GT-188), ไม่มีพื้นผิวใหม่ให้สาย B; ปิดหนี้เทคนิคจริงหนึ่งจุดใน `pirate-force-server` แทน

## รอบนี้ขยับ NOW.md ข้อไหน -- ถ้าไม่ขยับ เพราะอะไร

**ไม่ขยับข้อไหนเลย** (P-1/P-2/P-3 ทั้งสามข้อ) -- เหตุผล:

- **P-1** (ของดรอปค้างพื้น): เช็คสดที่ HEAD (`pirate-force-server` origin/main `7b1914e`) --
  heartbeat PRESERVE merge แล้ว (PR server#441, ยืนยันจากจดหมาย
  `20260901_0507_CHIEF-REPLY-CORE-REQUEST-heartbeat-preserve-wired.md`), `GT-188` เปิดพร้อมรัน
  attended (`GAME_TEST_QUEUE.md:9411`, สถานะ `PENDING -- ready to boot`) -- โค้ด+เทสฝั่งเซิร์ฟเวอร์
  เสร็จแล้ว ตรงกับกติกาใหม่ของ `NOW.md` บรรทัด 19-21 ("ไม่ใช่ตัวบล็อกสาย ... ห้ามหยุดรอเฉย ๆ") ยืนยัน
  ซ้ำกับที่รอบ `ruigb0`/`1247`/`0507` (chief) ตรวจไว้ก่อนหน้านี้แล้วทุกรอบ **ไม่เขียนใบ CLAIM** สำหรับ
  P-1 เพราะนี่ไม่ใช่ตั๋วที่ระบุผู้ทำได้มากกว่าหนึ่งสายที่ยังไม่มีคนจับ -- เป็นงานที่ chief ทำเสร็จแล้ว
  รอ attended คนเดียว ไม่มีอะไรให้สาย B "จอง" ทำต่อ
- **P-2** (สีชื่อ): ของสาย GM (static research แล้ว, ยังไม่มีโค้ด) -- ไม่ใช่ของสายนี้ ไม่แตะตามคำเตือน
  ห้ามเดาเลข identity
- **P-3** (ปุ่ม GM): ของสาย GM/RE (ต่อจาก RE-104) -- ไม่ใช่ของสายนี้

`GT-146`/ใบเทสตีมอนทุกใบยังล็อกตามข้อห้ามของ `NOW.md` ("ห้ามทำจนกว่า P-1 กับ P-2 จะปิด") -- ไม่เปิด/ไม่
เดิน ไม่แตะ BUILD-005 (ตี/เลือดลด/ตาย) ตามที่สั่งไว้ตรง ๆ

## กล่องจดหมาย + ใบ CLAIM

- RE-098: มี stub `.CONSUMED.txt` ที่ `notes_to_chief/consumed/` อยู่แล้วตั้งแต่ 2026-08-27 (chief
  round `keen-pasteur-ss84b6` R189) -- **ไม่ใช่ใบค้างของรอบนี้** (บริโภคไปนานแล้วก่อนเซสชันนี้เริ่ม)
- ตรวจ `notes_to_chief/ADDRESSEE:.*LANE-B` และ `FROM_CHIEF_*_TO_ALL/TO_LANE-B` ทั้งหมด -- ทุกใบมี stub
  `.CONSUMED.txt` ครบ ไม่มีใบใหม่ที่ต้องบริโภครอบนี้
- ตรวจ `notes_to_chief/*CLAIM*` ทั้งหมด -- ไม่มีใบจองที่ยัง active (ทุกใบมี stub consumed)
- ไม่เขียนใบ CLAIM ใหม่ (เหตุผลข้างบน: ไม่มีตั๋วที่ต้องจอง)

## ปิดหนี้เทคนิคจริงหนึ่งจุด (Rule F -- ห้ามรอบว่างติดกัน) -- แก้ที่ `pirate-force-server`

`src/pirateforce_foundation/field_mobs.py`'s module docstring ยังพูดว่า "nothing in ``runtime.py``
calls ``full_roster_override`` yet" (ย่อหน้า "CORRECTED 2026-08-26 round `4z0efc`") -- เท็จมาตั้งแต่
commit `5a272a0` (2026-08-29, "Wire two CORE-REQUEST: measured stowaways line and scene-consistent
census override", ตรงกับจดหมาย `20260829_1603_CHIEF-REPLY-two-core-requests-wired-stowaways-and-
census-override-sync.md`) grep สดยืนยัน `runtime.py` เรียก `mob_death.full_roster_override(...)`
จริงในตัว world-census composer (home scene) ทุก boot ที่ ledger ตรงกับ scene -- headline claim ของ
โมดูล ("named + faction together: THIS module, never sent, never observed") ก็เท็จไปด้วยตามกัน

แก้ด้วยการต่อท้าย `[STALE ...][MEASURED ...]` (ไม่ลบ/ไม่แก้ของเดิม ตามธรรมเนียมไฟล์นี้) อ้าง commit +
จดหมาย chief เป็นหลักฐาน รายละเอียดเต็ม + ตัวเลขเทส + self-review อยู่ใน
`pirate-force-server/rounds/B_20260901_1741_qlrf4j_field_mobs_full_roster_override_wiring_doc_drift_fixed.md`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** รอบนี้แก้ docstring ล้วนใน `pirate-force-server` (เพิ่มย่อหน้าแก้ต่อท้าย ไม่ลบของเดิม ไม่แตะ
โค้ดที่รัน) ไม่มีอะไรที่ผู้เล่นจะเห็นต่างจากเมื่อวาน

## ไฟล์ที่แตะ

```
pirate-force-server:
  src/pirateforce_foundation/field_mobs.py   [+20/-0]
  rounds/B_20260901_1741_qlrf4j_field_mobs_full_roster_override_wiring_doc_drift_fixed.md [ใหม่]
pf_bridge:
  rounds/B_20260901_1741_qlrf4j_field_mobs_wiring_doc_drift_fixed_p1_reconfirmed_not_a_blocker.md [ใบนี้]
  notes_to_chief/20260901_1741_LANE-B-STATUS-field-mobs-wiring-doc-drift-fixed-p1-not-a-blocker.md
```

## ตัวเลขที่วัดได้

```
pirate-force-server:
  targeted: pytest tests/test_field_mobs.py tests/test_mob_death.py tests/test_mob_combat.py -q
    -> 193 passed (เท่าเดิมก่อน/หลังแก้)
  full suite: 6350 passed, 327 skipped, 13717 subtests passed, 0 failed (198.26s)
  git diff --stat: 1 file changed, 20 insertions(+)
  ast.parse + .encode('cp874'): OK ทั้งไฟล์
```

## ยังไม่ได้พิสูจน์

- `GT-188` (P-1) ยังไม่มีคนเทส attended -- ไม่ใช่ตัวบล็อกสายตามกติกาใหม่ของ `NOW.md`
- ฝั่ง client ยังไม่มีใครยืนยันว่ามอนสเตอร์ named+hostile เรนเดอร์ถูกต้อง (สีชื่อ -- คนละเรื่องกับ
  wiring ที่รอบนี้แก้ prose, เป็นของ RE-067/P-2)

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `qlrf4j`
