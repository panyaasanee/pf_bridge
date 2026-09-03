[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ | จาก: LANE-B (COMBAT) รอบ `3w2mfu`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-09-01T15:40+07:00]

# LANE-B STATUS -- ตรวจ BUILD-004/5/6 ซ้ำสดครบ (ยังไม่มีของใหม่จริง), แก้ docstring drift ของ
# mob_ai_tick wiring ที่รอบ `p05wire` ทิ้งไว้

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** รอบนี้แก้ docstring สองไฟล์ใน `pirate-force-server` เท่านั้น (`lane_hooks/
lane_b_mob_ai_tick.py`, `tests/test_lane_b_mob_ai_tick.py`) ไม่เปลี่ยนพฤติกรรมรันไทม์ -- ยืนยันด้วย
full suite ผ่านเหมือนเดิมทุกจุด (`mob_ai_tick` ยัง "composes no frame" เหมือนก่อนแก้)

## ① ต้นรอบ -- merge + ล็อก + กล่องจดหมาย

`pirate-force-server` ตามหลัง `origin/main` หนึ่ง merge commit (PR #483 `[LANE-A]`) --
`git merge origin/main` fast-forward สำเร็จ ไม่ชนอะไร ไม่มี PR `[LANE-B]` ค้างเปิดตอนต้นรอบ
(ยืนยันแล้วโดย orchestrator) กล่องจดหมาย `ADDRESSEE: LANE-B` สะอาด (ตรวจซ้ำท้ายรอบด้วย -- ไม่มีใบใหม่
landed ระหว่างรอบ)

## ② ตรวจ BUILD-004/5/6 ซ้ำจากซอร์สสดของรอบนี้เอง (ไม่เชื่อจดหมายเก่าเฉย ๆ)

อ่านรอบ B ล่าสุด 6 รอบ (`4qwc1x`/`hqzp16`/`ruigb0`/`fbql13`/`p05wire`/`62o506`) แล้ว grep ซ้ำที่ HEAD:

```
grep -c mob_pickup_persist runtime.py         -> 0  (BUILD-006 จุดสาม ยังไม่ต่อสาย)
grep -n lane_b_mob_ai_tick runtime.py         -> :37, :5188-5210  (AI-tick ต่อสายแล้วจริง, รอบ p05wire)
grep -c mob_combat_membership runtime.py      -> 0  (RE-157 job2 -- CORE-REQUEST ค้างในโมดูลเอง)
```

**พบว่า BUILD-004 ฉาก 14 (Bg0015) เดินสายจริงแล้ว** ตั้งแต่รอบ `yfbqmg` ของสาย A (ไม่ใช่รอบนี้) --
`lane_a_choose_npc_scene14.py` เรียก `field_mob_hostile_bg0015.scene14_hostile_overrides` (โมดูล
pre-wire ของสายนี้เอง) จริงแล้ว ผู้เล่นเห็นมอนแดง 12 ตัวในฉาก 14 (Hell Volcano Island) มาตั้งแต่ตอนนั้น
สรุปคือ **ไม่มีจุดไหนในสาม BUILD ที่สายนี้แก้เองได้เพิ่มโดยไม่ทำผิดกฎ** (chief's file / COO-decision /
attended-only) -- ตรงกับ 6 รอบก่อนหน้าทุกจุด

**P-1 (NOW.md):** ตรวจ `GT-188` (`GAME_TEST_QUEUE.md:9411`) แล้วสถานะ `PENDING -- ready to boot`
(โค้ด+เทสฝั่งเซิร์ฟเวอร์เสร็จจริงจาก PR #441/#437) เข้ากฎใหม่ของ `NOW.md` เอง ("โค้ด+เทสเสร็จ เหลือรอ
attended = ไม่ใช่ตัวบล็อกสาย") -- สายนี้จึงไม่ติดค้าง ไปทำงานคิวปกติ (= รอบนี้) ได้ทันที

## ③ กฎ F -- ปิดหนี้เทคนิคจริงหนึ่งจุด: mob_ai_tick wiring doc drift

รอบ `p05wire` (COO-DECISION 20260901_0145) ต่อสาย `lane_hooks.lane_b_mob_ai_tick.maybe_tick` เข้า
`runtime.py`'s `dispatch()` จริงแล้ว (commit `5ac93b31`) และพลิกชื่อเทสจากลบเป็นบวก
(`test_nothing_in_runtime_py_calls_maybe_tick_yet` ->
`test_runtime_py_now_calls_maybe_tick_per_coo_decision_0145`) แต่ทิ้ง prose สองจุดที่ยังพูดว่า
"nothing calls this yet" ไว้ไม่แก้ -- ทั้งใน module docstring ของไฟล์ที่ต่อสายเอง และใน module
docstring ของไฟล์เทสที่สัญญาไว้ตรง ๆ ว่า "this test fails the day that stops being true without the
module docstring... being updated to match" (วันนั้นมาแล้วแต่ไม่มีใครทำตามสัญญา) แก้ตามธรรมเนียม
โปรเจกต์: ขีดฆ่าไม่ลบ ต่อท้ายด้วย `[STALE ...][MEASURED ...]` อ้างรอบ/commit/COO-DECISION จริง

**self-review พบบั๊กของตัวเอง 1 จุดก่อน push:** ร่างแรกเขียน "all five guard conditions" แต่
`runtime.py:5195-5202` มีจริง 6 เงื่อนไข (ลืมนับ `module_production_allowed(...)`) -- แก้แล้วในคอมมิต
เดียวกัน (overclaim-by-omission คลาสเดียวกับที่ pf-adversary จับได้ในรอบ `hqzp16`) ไม่มี Agent/Task
tool ให้เรียก `pf-adversary` subagent ตรงในเซสชันนี้ -- self-review แทนโดยอ่านโค้ดจริงนับซ้ำ

## ตัวเลขที่วัดได้

```
pytest tests/test_lane_b_mob_ai_tick.py -q: 9 passed
full suite (รันสองครั้งหลังแก้): 6302 passed, 323 skipped, 13373 subtests passed, 0 failed
git diff --check: silent
cp874-encodability ของทั้งสองไฟล์ที่แก้: ยืนยันด้วย .encode('cp874') -- ไม่มี error
```

## ยังไม่ได้พิสูจน์

- `GT-188` (P-1) ยังไม่มีคนเทส attended
- P-2/P-3 ยังบล็อกภายนอก ไม่ใช่ของสายนี้
- BUILD-006 จุดเสียบที่สามยังรอ `GT-124` (attended capture opcode pickup จริง)

## CORE-REQUEST

ไม่มี -- มี CORE-REQUEST เก่าค้างในตัวโมดูลเอง (`mob_combat_membership.py`, RE-157 job 2: หนึ่ง
predicate call ใน `_dispatch_mob_combat`) รอ chief หยิบเมื่อมีที่ว่างในคิว ไม่ใช่คำขอใหม่ของรอบนี้

## เปิดใบให้สาย C

ไม่มี

รายละเอียดเต็ม: `pirate-force-server/rounds/B_20260901_1540_3w2mfu_mob_ai_tick_wiring_doc_drift_fixed_no_new_src_surface_confirmed_again.md`

-- LANE-B (COMBAT) รอบ `3w2mfu`

PF-AUTOMERGE: v4
