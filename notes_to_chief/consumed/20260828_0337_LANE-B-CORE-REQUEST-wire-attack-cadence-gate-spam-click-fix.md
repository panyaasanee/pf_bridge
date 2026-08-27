# LANE-B CORE-REQUEST 2026-08-28T03:37+07:00 -- wire the attack-cadence gate into runtime.py (spam-click = runaway-damage fix, built and tested, sitting unwired)

ถึง: chief (ADDRESSEE: chief -- the wiring point is runtime.py, chief's file) · cc COO, สาย A, สาย GM

## ติดอะไร

`20260827_1635_PANYA-REFERENCE-*.md` ข้อ (ก) สั่งสาย B ปิดช่อง "สแปมคลิก = ดาเมจรัว" ฝั่งเซิร์ฟเวอร์
ก่อนเรื่องอื่นทั้งหมดในใบนั้น เพราะมันกระทบปริมาณดาเมจต่อวินาทีจริงของผู้เล่น สาย B เขียนกลไกนี้ไว้แล้ว
ใน `pirate-force-server/src/pirateforce_foundation/mob_combat.py`:

- `AttackCadenceLedger` / `CadenceRecord` -- ledger ต่อ performer, sorted/unique, replace-not-append
  (โครงเดียวกับ `CombatLedger`/`mob_death.DeathRegister` ที่มีอยู่แล้ว)
- `check_attack_cadence(cadence, performer_identity, at_ms, cadence_ms=ATTACK_CADENCE_MS_PROVISIONAL)`
  -- pure function, caller ป้อน wall-clock เอง ไม่แตะ `time.time()`/`time.monotonic()` เอง, fail-closed
  บน clock skew (คะแนนเป็น reject สูงสุด ไม่ใช่ผ่านฟรี), reject ไม่ขยับ deadline (สแปมคลิกไม่เลื่อนหน้าต่าง
  ของตัวเอง)
- `describe_cadence_rejection(check)` -- บรรทัดคอนโซล ASCII ตามที่ PANYA-REFERENCE ขอ (พิมพ์ทุกครั้งที่ปฏิเสธ)
- `ATTACK_CADENCE_MS_PROVISIONAL = 600` -- ค่าชั่วคราว ติดป้าย PROVISIONAL ตามกติกา (RE-110 ยังไม่มีค่าจริง
  จากเซิร์ฟเวอร์เดิม -- ปิดแล้วเป็น BOUNDED-NEGATIVE, "อย่าเปลี่ยนจนกว่าจะมี attended A/B")
- ครบทุกอย่างและมีเทสของตัวเอง (unit tests ผ่านทั้งหมดใน `tests/test_mob_combat.py`)

**สิ่งที่ยังไม่มี**: ไม่มีอะไรเรียกฟังก์ชันนี้จริงในเกม กลไกนี้นั่งอยู่เฉย ๆ ตั้งแต่สร้างเสร็จ (ก่อนรอบนี้)
เพราะจุดเรียกต้องอยู่ใน `runtime.py` (`_dispatch_mob_combat`) ซึ่งเป็นเขตของ chief ตามกติกาเขตเขียน --
สาย B แตะเองไม่ได้ และไม่เคยมีจดหมาย CORE-REQUEST อย่างเป็นทางการขอให้ต่อสาย มีแค่หมายเหตุในโค้ด
(`MOB_COMBAT_CADENCE_WIRING` ใน `mob_combat.py` บรรทัด ~229) ที่ไม่มีใครอ่านเจอจนกว่าจะเปิดไฟล์เอง
⇒ **ผู้เล่นสแปมคลิกได้ดาเมจรัวไม่จำกัดใน production วันนี้** ทั้งที่ทางแก้เขียนเสร็จแล้ว

## ทางเลือกที่เห็น

(ก) เขียนจดหมาย CORE-REQUEST นี้ให้ chief ต่อสายตามข้อความที่ `MOB_COMBAT_CADENCE_WIRING` บอกไว้แล้ว
    เป๊ะ (การเปลี่ยนแปลง 1 จุดใน `_dispatch_mob_combat`, ก่อนเรียก `attack_from_observed_action`)
(ข) รอจน lane_hooks ลง main แล้วให้สาย B ต่อสายเองผ่าน hook (ตามใบสั่ง 1230 ข้อ 1) -- แต่ lane_hooks
    ยังไม่ลง main ตอนนี้ และช่องโหว่นี้เปิดอยู่ทุกวันที่รอ
(ค) เพิกเฉย รอรอบถัดไปค่อยเขียนจดหมาย -- ไม่เลือก เพราะเป็นช่องโหว่เกมเพลย์จริงที่กระทบทุกการทดสอบ combat
    ที่ทำไปแล้ว (GT-084-R2 เห็นอาการนี้ตรง ๆ: "สแปมคลิกได้ดาเมจรัวผิดปกติ")

## เลือกอันไหนไปแล้ว

เลือก (ก) -- เขียนจดหมายนี้ทันที ไม่รอรอบถัดไป ตามหลัก "เขียนคำถาม/คำขอ แล้วเดินต่อ" ไม่ใช่ CORE-REQUEST
ที่บล็อกงานสาย B เอง (เขตเขียนสาย B ไม่มีอะไรค้างจากเรื่องนี้ -- ฟังก์ชันสร้างเสร็จแล้ว)

## ถ้าผิดต้องย้อนอะไรบ้าง

การต่อสายนี้เป็นการเพิ่มเงื่อนไข reject ก่อนเรียกฟังก์ชันเดิม (ไม่เปลี่ยน `attack_from_observed_action`
เอง) -- ย้อนได้ด้วย `git revert` commit เดียวใน `runtime.py`, ไม่มี schema/DB change, ไม่มี wire format
ใหม่ (การ reject คือ "ไม่ส่งเฟรม" ไม่ใช่เฟรมใหม่)

-- **สาย B · COMBAT**
