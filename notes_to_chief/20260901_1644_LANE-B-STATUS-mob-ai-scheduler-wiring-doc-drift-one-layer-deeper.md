[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ | จาก: LANE-B (COMBAT) รอบ `bgwgso`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-09-01T16:44+07:00]

# LANE-B STATUS -- ตรวจ BUILD-004/5/6 ซ้ำสดครบ (ยังไม่มีของใหม่จริง), แก้ docstring drift ของ
# mob_ai_scheduler/mob_ai_control ที่รอบ `3w2mfu` ไล่ไม่ถึง (wrapper แก้แล้ว, โมดูลที่ wrapper ห่อยัง
# ไม่แก้)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** รอบนี้แก้ docstring/comment/nonclaims (prose ล้วน) สามไฟล์ใน `pirate-force-server`
(`mob_ai_scheduler.py`, `mob_ai_control.py`, `tests/test_mob_ai_scheduler.py`) บวก regenerate pin
หนึ่งไฟล์ -- ไม่เปลี่ยนพฤติกรรมรันไทม์ `mob_ai_scheduler.tick_session` ยัง "composes no frame"
เหมือนเดิมทุกประการ

## ① ต้นรอบ -- merge + ล็อก + กล่องจดหมาย

`pirate-force-server` เช็คเอาต์จาก `origin/main` tip (`49284252`) ครั้งเดียวตอนต้นรอบ ไม่มี PR
`[LANE-B]` ค้างเปิดตอนต้นรอบ กล่องจดหมาย `ADDRESSEE: LANE-B` สะอาด (ตรวจ `git log` ตั้งแต่ merge ของ
รอบ `3w2mfu` (`7cf633d8`) ถึง HEAD ปัจจุบัน (`2129337c`) -- ไม่มีจดหมายใหม่จ่าหน้าสายนี้)

**หมายเหตุระหว่างรอบ**: orchestrator เตือนกลางรอบว่า stop-hook เห็น `pf_bridge` บนแบรนช์นี้ถูก
reset กลับ `origin/main` -- ตรวจแล้วยืนยันว่าเป็นแค่การ `git checkout -B ... origin/main` ครั้งแรก
ครั้งเดียวที่ทำก่อนแตะไฟล์ใด ๆ ทั้งสองรีโป (ตามใบสั่งงานเอง) ไม่ใช่การ re-run ระหว่างที่มีคอมมิตค้าง --
ไม่มีงานหาย ตรวจด้วย `git status`/`git log` ทั้งสองรีโปแล้วทั้งคู่ตรงกับที่คาด

## ② ตรวจ BUILD-004/5/6 ซ้ำจากซอร์สสดของรอบนี้เอง

```
grep -c mob_pickup_persist runtime.py       -> 0 (BUILD-006 จุดสาม ยังไม่ต่อสาย)
grep -n lane_b_mob_ai_tick runtime.py       -> :37, :5188-5210 (AI-tick ต่อสายแล้วจริงตั้งแต่
  รอบ p05wire)
grep -c mob_combat_membership runtime.py    -> 0 (RE-157 job2 -- CORE-REQUEST ค้างในโมดูลเอง)
```

ไม่มีพื้นผิว src ใหม่ให้สายนี้ทำเพิ่มโดยไม่ผิดกฎ (chief's file / COO-decision / attended-only) --
ตรงกับ 7 รอบก่อนหน้าทุกจุด `GT-146`/ใบเทสตีมอนทุกใบยังล็อกตาม `NOW.md` ("ห้ามทำจนกว่า P-1 กับ P-2
จะปิด") -- ยืนยันซ้ำที่ `GAME_TEST_QUEUE.md:33,7420`

## ③ กฎ F -- ปิดหนี้เทคนิคจริงหนึ่งจุด: ไปลึกกว่ารอบ `3w2mfu` หนึ่งชั้น

รอบ `3w2mfu` แก้ docstring drift ของ **wrapper** `lane_hooks/lane_b_mob_ai_tick.py` (และเทสของมัน)
ไปแล้ว หลังรอบ `p05wire`/`COO-DECISION 20260901_0145` ต่อสาย `maybe_tick` เข้า `runtime.py` จริงที่
commit `5ac93b31` -- แต่ไม่ได้ไล่ตาม import chain ลงไปแก้โมดูลที่ wrapper นั้นห่ออยู่: `maybe_tick`
เรียก `mob_ai_scheduler.tick_session` ตรง ๆ (`lane_hooks/lane_b_mob_ai_tick.py:181`) ซึ่งเรียก
`mob_ai_control.tick_step`/`commit_step` ต่อแถว (`mob_ai_scheduler.py:265`) -- ทั้งสองโมดูลนี้ยัง
พูดว่า "nothing calls this today" / "no caller anywhere in this tree runs it in production" /
"What remains UNDISPATCHED is the tick loop" อยู่ ทั้งที่ตอนนี้มี caller จริงผ่าน wrapper แล้ว
(`production_allowed = True` ทั้งสามโมดูลในสาย -- เส้นทาง flagless จริง ไม่ใช่ probe)

แก้ตามธรรมเนียมโปรเจกต์ (ขีดฆ่าไม่ลบ ต่อท้ายด้วย `[STALE ...][MEASURED ...]`) ใน 5 จุด: docstring
`mob_ai_scheduler.py` 3 ย่อหน้า + คอมเมนต์เหนือ `MOB_AI_SCHEDULER_WIRING` (ไม่แก้ตัวสตริงเอง เพราะ
เทสสองเส้นยังพินสตริงย่อยไว้) + `MOB_AI_CONTROL_NONCLAIMS[0]` (ครึ่ง tick_step แก้, ครึ่ง reconcile()
ยังจริงอยู่ ไม่แตะ) + module docstring ของไฟล์เทส (อ้างชื่อเทสผิด -- ชื่อจริงเปลี่ยนไปแล้วตั้งแต่รอบ
`iok5z1` แต่ docstring ไม่ตามไปแก้) + คอมเมนต์เหนือเทสที่ชื่อฟังก์ชันเองอ้างว่า "stays unwired today"
(ไม่เปลี่ยนชื่อฟังก์ชัน -- ทิ้งเป็นข้อสังเกตให้รอบที่มีเวลาตรวจครบกว่านี้)

`scenarios/combat_aggro_001.json` (pin ที่ generate จาก `mob_ai_control.pin_document()`) regenerate
แล้ว -- `git diff --stat` ยืนยัน 1 บรรทัดเปลี่ยน ตรงกับ nonclaim ที่แก้พอดี ไม่มีตัวเลข/ฟิลด์อื่นขยับ

## Self-review (ไม่มี Agent/Task tool ให้เรียก pf-adversary subagent ตรงในเซสชันนี้)

ทำเองตามขั้นตอน pf-adversary: cross-check บรรทัด `runtime.py`/wrapper/scheduler ที่อ้างทั้งหมดด้วย
การอ่านโค้ดจริง, ตรวจ pin diff มีแค่ 1 บรรทัด, รันเทสที่พินสตริงไว้ (`test_the_wiring_line_names_
runtime_py_and_stays_unwired_today`, `test_the_committed_pin_is_what_the_code_computes`) ยืนยันผ่าน
ทั้งคู่, อ่าน diff เต็มด้วยตายืนยันไม่มีบรรทัด logic เปลี่ยน, `git diff --check` silent, cp874+ast
ผ่านทั้งสามไฟล์ที่แก้ **พบ 1 จุดในร่างแรกของตัวเอง**: อ้างผิดว่าคอมเมนต์เหนือ
`test_the_scheduler_has_exactly_the_one_ready_importer` เป็น "docstring" -- ที่จริงเป็น inline
comment (ฟังก์ชันนั้นไม่มี `"""..."""` ของตัวเอง) แก้คำก่อน push

## ตัวเลขที่วัดได้

```
pytest tests/test_mob_ai_scheduler.py tests/test_mob_ai_control.py tests/test_lane_b_mob_ai_tick.py -q
  -> 82 passed, 37 subtests passed (ก่อนแก้และหลังแก้เท่ากัน)
+ tests/test_mob_combat.py -q -> 139 passed, 37 subtests passed
full suite (รันพื้นหลังระหว่างรอบ, เกิน timeout 120s ปกติ): 6352 passed, 323 skipped,
  13717 subtests passed, 0 failed (265.62s)
git diff --check: silent
cp874-encodability ของ 3 ไฟล์ที่แก้: ยืนยันด้วย .encode('cp874') -- ไม่มี error
scenarios/combat_aggro_001.json regenerate: 1 บรรทัดเปลี่ยน
```

## ยังไม่ได้พิสูจน์

- `GT-188` (P-1) ยังไม่มีคนเทส attended
- P-2/P-3 ยังบล็อกภายนอก ไม่ใช่ของสายนี้
- BUILD-006 จุดเสียบที่สามยังรอ `GT-124` (attended capture opcode pickup จริง)
- `reconcile()` ใน `mob_ai_control.py` ยังไม่มี dispatcher จริง (ยังจริงอยู่ ไม่ใช่ overclaim ที่แก้)
- ชื่อเทส `test_the_wiring_line_names_runtime_py_and_stays_unwired_today` ยังไม่เปลี่ยน (ทิ้งเป็น
  คอมเมนต์ให้รอบถัดไปที่มีเวลาตรวจครบกว่านี้)

## CORE-REQUEST

ไม่มี -- CORE-REQUEST เก่าที่ยังค้าง (`mob_combat_membership.py`, RE-157 job 2: หนึ่ง predicate call
ใน `_dispatch_mob_combat`) ไม่ใช่คำขอใหม่ของรอบนี้

## เปิดใบให้สาย C

ไม่มี

รายละเอียดเต็ม:
`pirate-force-server/rounds/B_20260901_1644_bgwgso_mob-ai-scheduler-wiring-doc-drift-one-layer-deeper.md`

-- LANE-B (COMBAT) รอบ `bgwgso`

PF-AUTOMERGE: v4
