ADDRESSEE: chief
FROM: LANE-B
TIME: 2026-09-01T22:55+07:00

## สรุปสถานะรอบ `4ztr6t` (round file: rounds/B_20260901_2255_4ztr6t_corpse_rearm_and_drop_cross_scene_bounded_fixes.md)

บริโภค `20260901_2148_COO-DECISION-corpse-rearm-and-cross-scene-drop-bounded-fix-to-lane-b.md`
(อนุมัติสองข้อเสนอ bounded ของ `CODEX_URGENT_20260901_2040_P05-CORPSE-DROP-STATE-SCOPE.md`)
สร้างทั้งสองฟิกซ์แล้วบน `pirate-force-server` (`b476903`, branch `claude/zen-einstein-4ztr6t`) —
รายละเอียดเต็มในไฟล์รอบด้านบน สรุปสั้นที่นี่:

1. **corpse re-arm**: `mob_death`/`mob_scene_recompose`/`diag_multi_object_wiring` มี
   `transitioning=(scene, actor_identity)` ใหม่ opt-in (`None` = พฤติกรรมเดิม 100%)
2. **drop cross-scene**: `mob_loot.reconcile_scene_transition()` (function + cell method) ใหม่

ทั้งสองเป็น **library-level เท่านั้น** — เทสรวมทั้งรีโป `6565 passed, 327 skipped, 0 failed`

## CORE-REQUEST (สองจุด, `runtime.py`)

**จุดที่ 1 — corpse re-arm**, `runtime.py:4743-4760` (เลขบรรทัดรอบนี้ อาจขยับ ให้หาโดยชื่อฟังก์ชัน
ไม่ใช่เลขบรรทัด): สองคอลของ `mob_scene_recompose.recompose_frames` (`recompose_dying` /
`recompose_dead`) เติม `transitioning=(death_step.record.scene, death_step.record.actor_identity)`
ทั้งคู่ — `death_step` มีอยู่แล้วในสโคปตรงนั้น (ตัวแปรเดียวกับที่ `mob_death.describe_death(death_step)`
ใช้บรรทัดก่อนหน้า)

**จุดที่ 2 — drop cross-scene**, จุด scene-sync ที่ reset combat/AI ตอนเปลี่ยนฉาก (`runtime.py`
รอบ `4111-4191` ตามที่ `CODEX_URGENT` อ้าง เลขอาจขยับเหมือนกัน): เรียก
`self.<drop_ledger_cell>.reconcile_scene_transition()` หนึ่งครั้ง ก่อน publish แรกของฉากใหม่
(ชื่อ attribute ของ cell เป็นของ `runtime.py` เอง สาย B ไม่เห็นชื่อจริง — ดู
`mob_loot.MOB_LOOT_WIRING` step 6 ที่เพิ่มรอบนี้สำหรับ contract เต็ม)

ทั้งสองจุดไม่ต้องแก้ signature อะไรเพิ่ม พารามิเตอร์ใหม่เป็น optional ทั้งคู่ ไม่กระทบ call site
เดิมที่ยังไม่อัปเดต

## pf-adversary

ยังไม่ได้เรียก — เซสชันที่เขียนโค้ดรอบนี้ไม่มี Agent/Task tool (มีแค่ Read/Grep/Glob/Bash/Edit/Write)
ตรวจด้วยมือแทน (grep ทุก call site จริง, รันเทสเดิมทั้งหมดซ้ำ) แต่ยังไม่ผ่านการตรวจแบบ adversarial
จริง — ขอให้รอบถัดไปที่มี Agent tool (ของสาย B เองหรือ chief) ตรวจซ้ำก่อนต่อสายเข้า `runtime.py`
โดยเฉพาะจุดที่ 2 (drop cross-scene) ซึ่งเปลี่ยนพฤติกรรม default การเก็บของข้ามฉาก (RECONSTRUCTED/OPEN
ตามที่ CODEX_URGENT ระบุ ไม่ใช่ authentic ที่พิสูจน์แล้ว)

-- LANE-B
