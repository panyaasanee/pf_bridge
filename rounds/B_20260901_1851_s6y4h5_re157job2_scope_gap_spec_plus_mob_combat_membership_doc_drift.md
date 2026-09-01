# รอบ LANE-B (COMBAT) s6y4h5 -- 2026-09-01T18:51+07:00 (scheduled, ไม่มีคนเฝ้าหน้าจอ)

## ต้นรอบ

1. อ่าน `NOW.md` ก่อนเสมอ -- มีงานด่วน P-1/P-2/P-3 (ไมล์สโตนพักไว้) ตรวจแล้วไม่มีข้อไหนต้องให้สาย B
   ทำต่อตอนนี้: P-1 (ของดรอปค้างพื้น) chief ต่อสายเสร็จแล้ว รอ Panya รัน GT-188 attended เท่านั้น
   (ตรงกับกติกาใหม่ "โค้ด+เทสฝั่งเซิร์ฟเวอร์เสร็จแล้ว รอ attended = ไม่ใช่บล็อกสาย") · P-2/P-3 เป็นของ
   สาย GM/RE ไม่แตะ · ห้ามเปิดใบเทสตีมอน (GT-146 ฯลฯ) จนกว่า P-1/P-2 จะปิด -- เคารพข้อนี้ตลอดรอบ
2. ตรวจล็อก: ไม่มี PR เปิดค้างหัวข้อ `[LANE-B]` ในทั้งสองรีโป (`search_pull_requests` ยืนยัน 0 ใบ)
3. ตรวจชะตารอบก่อน (Rule A): PR `pf_bridge#737` และ `pirate-force-server#496` (รอบ `qlrf4j`) ทั้งคู่
   `merged=true` งานอยู่บน main แล้ว ไปต่อได้ ไม่ต้อง cherry-pick อะไร
4. กล่องจดหมาย (Rule B): เจอใบ `20260901_1747_CHIEF-TO-LANE-B-re157-job2-...` (ADDRESSEE: LANE-B)
   ยังไม่มี stub -- บริโภครอบนี้ (ดูหัวข้อถัดไป)

## ใบที่บริโภค: 1747_CHIEF-TO-LANE-B (RE-157 job2 scope gap)

Chief ต่อสาย `mob_combat_membership.admits()` เข้า `_dispatch_mob_combat` (runtime.py:4247-4256) และ
stamp ที่ 3 จุด census-commit (bg0001/bg0002/lane-composer) + clear ที่ GM `/warp`
(`_gm_warp_resync_selected_scene:5537-5538`) สำเร็จ แต่ pf-adversary จับได้ว่า clear ไม่ครอบสองเส้นทาง
เปลี่ยนฉากที่ผู้เล่นจริงใช้บ่อยที่สุด: `world_travel_gate.py` (เดินทางปกติ) กับ `world_m2_crossing_handoff.py`
(Columbus M2) -- ขอให้สาย B ตัดสิน (ก)/(ข)/(ค)

**ตัดสิน: (ค)** ตรวจโค้ดจริงเอง (อ่านอย่างเดียว, runtime.py เป็นของ chief แตะเองไม่ได้) ยืนยันช่องจริง:
ทั้งสองจุดครอสซิ่งมี `reset = handoff.membership_reset` ของตัวเองอยู่แล้ว (`runtime.py:7579` และ
`:5180`) ใช้ล้าง `population_indices`/`world_census_indices` แต่ไม่แตะ
`mob_combat_announced_membership` เลย -- เขียนสเปกสองจุด สองบรรทัดต่อจุด (mirror clear pattern เดิม
จาก GM warp) ลง `notes_to_chief/20260901_1838_LANE-B-REPLY-re157-job2-scope-gap-option-c-spec.md`
ให้ chief ต่อสายรอบถัดไป -- รายละเอียดเต็มอยู่ในจดหมายนั้น

Stub วางแล้วที่ `notes_to_chief/20260901_1747_..._your-call.md.CONSUMED.txt` + สำเนาต้นฉบับไป
`notes_to_chief/consumed/`

## ของที่สร้างรอบนี้ (Rule F -- ไม่ให้รอบว่างติดกัน แม้รอบก่อนไม่ว่างแล้วก็ตาม)

มอบให้ pf-builder subagent ตรวจหาหนี้เทคนิคจริงในเขตสาย B (`src/pirateforce_foundation/`,
ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py` ของ chief, ไม่แตะ `scenarios/world_*.json`
ของสาย A, ไม่เปิด/แก้ใบเทสตีมอนใดๆ) ผลลัพธ์: มันตรวจ `mob_combat_membership.py` แยกอิสระและเจอช่องเดียวกัน
กับที่ตัดสินไปข้างบนโดยไม่ได้อ่านจดหมายของฉันก่อน (corroboration อิสระ) พร้อมพบว่า docstring หัวไฟล์
ยังอ้างว่า "no call site in runtime.py" / อ้าง CORE-REQUEST ค้าง ทั้งที่ commit `798507ee`
(รอบ `57alcd` ของ chief วันเดียวกัน) ต่อสายจริงแล้ว -- เท็จมาตั้งแต่วันนี้

แก้ด้วยการต่อท้าย `[STALE][MEASURED]` (ไม่ลบของเดิม ไม่แตะโค้ดที่รัน) อ้าง commit + บรรทัดจริงที่ตรวจแล้ว
(`runtime.py:4247-4256`, `:7941-7947`, `:8204-8209`, `:8556-8565`, `:5537-5538`) และบันทึกช่อง
scene-transition เดียวกับข้างบนไว้ใน docstring ด้วย เผื่อคนอ่านโมดูลนี้เจอก่อนอ่านจดหมาย

## ตัวเลขที่วัดได้

```
ไฟล์ที่แตะ: src/pirateforce_foundation/mob_combat_membership.py (+44/-0, docstring เท่านั้น)
targeted: test_mob_combat_membership.py + test_mob_combat_membership_wiring.py -- 15 passed (เท่าเดิม)
full suite: 6387 passed, 323 skipped, 13726 subtests passed, 0 failed
```

## pf-adversary

pf-builder ไม่มี Agent/Task tool ในบริบทที่รันจริง เลยรีวิวเองแบบปฏิปักษ์ (อ่าน runtime.py ตรงทุกบรรทัด
ที่จะอ้าง ไม่เชื่อ grep อย่างเดียว) จับข้อผิดพลาดของตัวเองได้หนึ่งจุดก่อน commit (เขียนชื่อรอบผิดเป็น
`zen-einstein` -- ชื่อ branch prefix ไม่ใช่ round-id -- แก้เป็น `s6y4h5`) ยืนยัน cp874-encodable +
`ast.parse()` ผ่านทุกครั้งที่แก้

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี** -- รอบนี้เป็นจดหมายตัดสินใจ + เอกสารในโค้ดล้วน ไม่มีบรรทัดตรรกะไหนถูกแตะ

## เขตที่แตะ

`src/pirateforce_foundation/mob_combat_membership.py` เท่านั้น (pirate-force-server) --
ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py` ไม่แตะ `scenarios/world_*.json`

## CORE-REQUEST

ส่งแล้วในจดหมาย `20260901_1838_LANE-B-REPLY-...` -- สองจุดใน `runtime.py` (`:7579` และ `:5180`)
เพิ่ม `self.mob_combat_announced_membership = None` + `self.mob_combat_announced_membership_generation
+= 1` มิเรอร์ clear pattern เดิมจาก GM warp (`:5537-5538`)

## เปิดใบให้สาย C

ไม่มี

## ไฟล์ที่เขียน

- `rounds/B_20260901_1851_s6y4h5_re157job2_scope_gap_spec_plus_mob_combat_membership_doc_drift.md`
  (ไฟล์นี้)
- `notes_to_chief/20260901_1838_LANE-B-REPLY-re157-job2-scope-gap-option-c-spec.md`
- `notes_to_chief/20260901_1747_CHIEF-TO-LANE-B-re157-job2-wired-scene-transition-gap-your-call.md.CONSUMED.txt`
  + สำเนาต้นฉบับใน `notes_to_chief/consumed/`

-- LANE-B (COMBAT) รอบ `s6y4h5`
