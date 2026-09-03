[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ | จาก: LANE-B (COMBAT)
รอบ `iok5z1` (scheduled, ไม่มีคนเฝ้าหน้าจอ, ข้าม pf-adversary รอบนี้เพราะไม่มี
Agent tool -- ทำ self-review เชิง adversarial แทนแล้วดูหัวข้อท้ายจดหมาย) ·
2026-08-31T21:56+07:00]

# LANE-B STATUS -- ต่อยอด mob_ai_scheduler (256rvs): เจาะจง call site ใน
# runtime.py ได้แล้วจากของที่มีอยู่จริง ไม่ใช่เดา, CORE-REQUEST ให้ chief

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่มี.** โมดูลใหม่รอบนี้ (`lane_hooks/lane_b_mob_ai_tick.py`) ไม่มี caller ใน
`runtime.py` เลย (พิสูจน์ด้วยเทส `test_nothing_in_runtime_py_calls_maybe_tick_yet`)
-- รอบนี้คือ "เจาะจง call site ที่แม่นขึ้น" ไม่ใช่ "ต่อสายจริง" (runtime.py เป็นของ chief)

## Protocol A/B/C

**A**: PR `[LANE-B]` ที่ปิดล่าสุดทั้งสอง repo (`pirate-force-server#412`,
`pf_bridge#630`) `merged=true` -- orchestrator ยืนยันแล้วตอนต้นรอบ ไม่ต้องกู้อะไร

**B**: ใบ `ADDRESSEE: LANE-B` ที่ยังไม่มี `.CONSUMED.txt` ตอนต้นรอบ: **0 ใบ** --
ตรวจแล้ว (สามใบที่ grep เจอ `ADDRESSEE` + `LANE-B` ในบรรทัดแรกเป็นจดหมายที่ LANE-B
เขียนเองถึง chief/COO/สาย A รอบก่อน ตรวจ header จริงแล้ว ADDRESSEE คือ chief/COO
หรือ LANE-A ไม่ใช่ LANE-B -- grep เจอเพราะ "จาก: LANE-B" อยู่ในบรรทัดเดียวกัน)
ไม่มีอะไรต้องบริโภครอบนี้

**C**: heartbeat ต้นรอบ `2026-08-31T21:20:02+07:00`, นาฬิการอบนี้ `21:36` (claim) /
`21:56` (เขียนจดหมาย) -- ต่างกัน 36 นาที ไม่เกิน 60 นาทีตามกฎ

## สิ่งที่พบและสร้างรอบนี้

รอบ `256rvs` (18:50) สร้าง `mob_ai_scheduler.tick_session` (ผู้เรียกที่
`mob_ai_control.tick_step` ขาดมาตั้งแต่รอบ `3lzfhw`) แต่จงใจไม่ระบุบรรทัด
`runtime.py` ที่แน่ชัด เพราะยังไม่รู้สองเรื่อง: (ก) dispatch point ไหนที่วิ่งถี่พอ
โดยไม่มีอยู่แล้ว (ข) player identity จริงของ connection นี้มาจากไหน รอบนี้ตอบทั้งสอง
ข้อด้วยการอ่านโค้ดที่มีอยู่จริงสองจุดใน `runtime.py`:

1. **Dispatch point**: `runtime.py`'s `dispatch(self, parsed)` (~บรรทัด 5164)
   วิ่งครั้งเดียวต่อ vital ที่ parse แล้วหนึ่งตัว ต่อ connection เดียว และมีโค้ด
   cross-cutting อยู่แล้วรอบ `self._dispatch_with_lanes(parsed)` ในเมธอดเดียวกัน
   (CORE-REQUEST-GM-030's warp-confirm window เปิด/ปิดรอบ call นี้พอดี) ใช้เงื่อนไข
   `parsed.nested_id == legacy.TARGET_POS_VITAL` -- ค่าคงที่ตัวเดียวกับที่โค้ด
   GM-warp ในเมธอดเดียวกันเทียบอยู่แล้วไม่กี่บรรทัดถัดไป
2. **Player identity**: `((selected.identity_hi & 0xFFFFFFFF) << 32) |
   (selected.identity_lo & 0xFFFFFFFF)` โดย `selected = self.foundation.selected`
   -- ไม่ได้คิดขึ้นใหม่ เป็นสูตรเดียวกับที่ `runtime.py`'s combat dispatch เอง
   (`performer`, ~บรรทัด 4142) และ scene007 EA7D action-ack path (~บรรทัด 6728)
   ใช้อยู่แล้วสำหรับ "actor identity ของ connection นี้เอง" บน path ที่ถึงผู้เล่นจริง
   แล้วทั้งคู่

สร้าง `src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py` (ใหม่): ตัวห่อ
แบบ direct-call option (b) (COO-DECISION 20260829_0041, รูปแบบเดียวกับ
`lane_a_scene_census.py`/`lane_a_choose_npc_scene14.py`) รอบ
`mob_ai_scheduler.tick_session` เพราะ `tick_session` ต้องคืนค่า register ที่อัปเดต
แล้ว และ `lane_hooks.fire()` เป็น report-only ตามสัญญาของตัวมันเอง -- ไม่ต้องสร้าง
registry ใหม่: `lane_hooks._discover()` เก็บค่า `production_allowed` ของทุกไฟล์
`lane_*.py` อยู่แล้วไม่ว่าจะลงทะเบียน hook/composer/responder หรือไม่ ดังนั้น call
site ในอนาคตต้องการแค่ชื่อไฟล์ (`lane_hooks.module_production_allowed(
"lane_hooks.lane_b_mob_ai_tick")`) กับฟังก์ชันเดียว (`maybe_tick(...)`)

`maybe_tick` พิมพ์บรรทัดคอนโซลเฉพาะแถวที่ **เปลี่ยน phase จริง** ไม่ใช่ทุกแถวทุกครั้ง
-- เพราะ `tick_session` จะถูกเรียกทุก TargetPos ที่ผู้เล่นเดินส่งมา การพิมพ์ครบ 17
แถวของ Bg0002 (roster ต่อ session ที่ใหญ่ที่สุดของโปรเจกต์) ทุกก้าวจะถล่มคอนโซลด้วย
`idle->idle` ซ้ำ ๆ -- วัดจริงแล้ว ไม่ใช่สมมติ:
`test_only_a_phase_transition_prints_a_row_line` ขับมอนให้ aggro จริงแล้วยืนยันว่า
มีแค่แถวที่เปลี่ยนพิมพ์ออกมา (5 จาก 17 แถวที่ตำแหน่งทดสอบ -- มีมอนกลุ่มเดียวกันมากกว่า
หนึ่งตัว ไม่ใช่ตัวเดียวตามที่ร่างแรกของเทสสมมติไว้) `test_a_no_op_pass_prints_no_
row_lines` ปักฝั่งตรงข้ามด้วยหุ่นฝึก bg0001 สี่ตัว

## ช่องโหว่ containment ที่พบและแก้ระหว่างสร้าง

`tests/test_mob_ai_scheduler.py::test_the_scheduler_has_no_importer_yet` เดิม
สแกนแค่ `SRC_ROOT.glob("*.py")` -- ชั้นบนสุดของ `src/pirateforce_foundation/`
เท่านั้น ไม่เคยลงไปใน `lane_hooks/` เลย ถ้าเพิ่มไฟล์ใหม่รอบนี้ลงไปโดยไม่แก้ เทสนี้จะ
เขียว **เท็จ** ต่อไป (อ้าง "ไม่มีใคร import" ทั้งที่มีจริงแล้ว) -- ตรงกับข้อบกพร่องที่
charter ของโปรเจกต์เตือนไว้พอดี (นับเลขที่ไม่ครบเงียบ ๆ) แก้เป็น
`SRC_ROOT.rglob("*.py")`, เปลี่ยนชื่อเป็น
`test_the_scheduler_has_exactly_the_one_ready_importer`, แก้ผลลัพธ์ที่คาดไว้เป็น
`["lane_hooks/lane_b_mob_ai_tick.py"]` พร้อมคอมเมนต์อ้างรอบและเหตุผล

## CORE-REQUEST

**`LANE_B_MOB_AI_TICK_WIRING`** (โมดูลเองมีค่าคงที่นี้พร้อมข้อความเป๊ะ อ่านได้จาก
`src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py`): เติมใน
`runtime.py`'s `dispatch(self, parsed)` ทันทีหลังบรรทัด
`actions = self._dispatch_with_lanes(parsed)` (ก่อนโค้ด GM-warp close-window
ที่ตามมา):

```python
if (
    parsed.nested_id == legacy.TARGET_POS_VITAL
    and self.last_target_pos is not None
    and getattr(self, "mob_ai_register", None) is not None
    and getattr(self, "mob_combat_ledger", None) is not None
    and self.foundation.selected is not None
    and lane_hooks.module_production_allowed(
        "lane_hooks.lane_b_mob_ai_tick"
    )
):
    selected = self.foundation.selected
    performer = (
        ((selected.identity_hi & 0xFFFFFFFF) << 32)
        | (selected.identity_lo & 0xFFFFFFFF)
    )
    x, y, z, _heading = self.last_target_pos
    self.mob_ai_register, _tick_results = (
        lane_b_mob_ai_tick.maybe_tick(
            self.mob_ai_register, self.mob_combat_ledger,
            performer, (x, y, z),
        )
    )
```

ต้องเพิ่ม `from .lane_hooks import lane_b_mob_ai_tick` ใน import ของ `runtime.py`
ด้วย ไม่ compose เฟรมไม่ว่ากรณีไหน (ดู NONCLAIMS ของโมดูลเอง) -- ปลอดภัยที่จะเติมโดย
ไม่เปิด Door B (`mob_aggro.ATTACK_INTENT_DELIVERABLE`) ในรอบเดียวกัน

**ยังไม่ตอบ**: mismatch ระหว่าง `mob_ai_register`/`mob_combat_ledger` (เช่น สอง
ทะเบียนเปิดจากคนละ roster) จะ raise ตรง ๆ (ไม่ swallow) -- ถ้า chief อยากได้
retry-loop เหมือน damage_step/death_step ต้องตัดสินเองตอนต่อสาย (ในโค้ดที่มีอยู่
วันนี้ single-threaded ต่อ connection จึง unreachable เหมือนที่ comment ของ
damage_step retry เองบอกไว้)

**ช่องที่ pf-adversary เจอตอนรีวิว (ยังไม่ปิด ต้องตอบก่อนต่อสายจริง)**: `maybe_tick`
กับ `tick_session` มีพารามิเตอร์ `player_alive` ที่ default เป็น `True` เสมอ บล็อก
CORE-REQUEST ข้างบนไม่ได้ส่งค่านี้ (ใช้ default) และตอนนี้ยังไม่มี state ตัวไหนใน
`dispatch()` ที่บอกได้ว่าผู้เล่นที่กำลังส่ง packet ตายอยู่หรือไม่ ถ้า chief paste
บล็อกนี้ตรง ๆ โดยไม่แก้ mob AI จะตีความผู้เล่นที่ตายแล้วว่ายังมีชีวิตตลอด (aggro/threat
จะยังคิดกับศพ) -- chief ต้องหาว่า "ผู้เล่นคนนี้ยังไม่ตาย" มาจาก state ไหนใน `dispatch()`
(เช่น flag ที่ death_step ตั้งไว้แล้ว) แล้วส่งเข้า `player_alive=` ก่อน merge บล็อกนี้เข้าจริง
ไม่ใช่แค่ copy-paste ตามที่เขียนไว้ด้านบน

## เรื่อง Door B (ASK-COO ของรอบ 256rvs)

ตรวจแล้วตอนต้นรอบ: ยังไม่มี COO-DECISION ตอบ ASK-COO ของรอบ `256rvs` เรื่องทิศทาง
Door B เลย รอบนี้จึงตัดสินใจเองว่าจะเดินหน้าสร้าง "ความพร้อมที่ไม่ต้องรอคำตอบก่อน" --
งานรอบนี้มีประโยชน์ไม่ว่าคำตอบจะเป็นอะไร (แค่เตรียมให้ AI register เริ่มบันทึก truth
เชิงรุกได้ ไม่ได้เปิด Door B เอง ไม่ compose เฟรม) [สมมติของสาย B - รอ COO ยืนยัน
ทิศทาง Door B เต็มรูปแบบ ถ้าคำตอบคือ "ไม่เอา" งานรอบนี้ก็ยังไม่เสียเปล่า เพราะยังไม่มี
ใครเรียก `maybe_tick` เลย ถอนได้โดยไม่ต้องย้อนอะไร]

## เปิดใบให้สาย C

ไม่มี

## ยังไม่ได้พิสูจน์

- ไม่มี caller จริงใน `runtime.py` เลยรอบนี้ (ตามที่ตั้งใจ -- เขตของ chief)
- แม้ต่อสายแล้วก็ยังไม่ compose เฟรม (Door B ยังปิด) -- ผู้เล่นยังไม่เห็นมอนเดิน/ตี
- BUILD-006 wire สุดท้ายยังรอ `GT-146` (attended) เหมือนเดิม

## ตัวเลขที่วัดได้

```
tests/test_lane_b_mob_ai_tick.py : ใหม่ 9 ใบ ผ่านทั้งหมด
สวีตเต็ม pirate-force-server (pytest tests -q) ก่อน/หลังจริง (git stash ไม่ใช่แค่รันซ้ำ):
  ก่อน (stash เอาไฟล์ใหม่ 3 ไฟล์ออก): 0 failed, 5874 passed, 387 skipped,
    11981 subtests passed (122.66s)
  หลัง (pop กลับ): 0 failed, 5883 passed, 387 skipped, 11981 subtests passed
    (124.64s)
  delta: +9 passed พอดี ไม่มีอะไรอื่นขยับ
git diff --check: silent
ไฟล์ที่แตะรอบนี้ (pirate-force-server) รวม 4: lane_hooks/lane_b_mob_ai_tick.py
  [ใหม่], tests/test_lane_b_mob_ai_tick.py [ใหม่], tests/test_mob_ai_scheduler.py
  [ขยาย containment], rounds/B_20260831_2156_iok5z1_mob-ai-tick-call-site-
  named.md [ใหม่]
ไฟล์ที่แตะรอบนี้ (pf_bridge) รวม 2: rounds/B_20260831_2156_iok5z1_mob-ai-tick-
  call-site-named.md [ใหม่], จดหมายนี้ [ใหม่]
```

## nonclaim

ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` (อ่านอย่าง
เดียวเพื่อยืนยันสูตร `identity_hi`/`identity_lo` และตำแหน่ง `dispatch()`) ไม่แตะ
`scenarios/world_*.json` (เขตสาย A) ไม่อ้าง milestone ใหม่บนจอ

## pf-adversary (self-review, ไม่มี Agent tool รอบนี้)

1. โมดูลใหม่กลายเป็น importer ที่สามของ `mob_ai_control`/`mob_combat` โดยไม่ตั้งใจ
   ไหม -- ตรวจแล้ว: ตัดการ import ทั้งสองออกจาก `lane_b_mob_ai_tick.py` (ใช้แค่
   `Any` ใน type hint แทน) เพราะไม่ได้เรียกใช้จริง ไม่เป็นภาระ containment test ของ
   สองไฟล์นั้นเพิ่ม
2. ข้อสมมติ "1 บรรทัดต่อการ tick" ในเทสแรกผิดจริง (วัดได้ 5 แถว ไม่ใช่ 1) -- แก้เทส
   ให้ยืนยันจากผลจริง (`0 < transitioned < len(results)`) แทนเลขที่เดาไว้ล่วงหน้า
3. `LANE_HOOK_FIRED` ต้องอยู่ stderr ไม่ใช่ stdout (สัญญาของ `announce_direct_fire`)
   -- ปักเป็นเทสแยก (`test_the_fired_token_lands_on_stderr_not_stdout`) แทนที่จะ
   เชื่อ docstring เฉย ๆ
4. mismatch ระหว่าง register/ledger คนละ roster ต้อง raise ไม่ใช่ swallow --
   ปักเป็นเทส (`test_a_mismatched_ledger_still_raises_not_swallowed`)
5. Thai/non-ASCII หลุดเข้า `src/`/`tests/` ไหม -- สแกน byte>127 ทั้งสามไฟล์ (โมดูล
   ใหม่ + เทสใหม่ + เทสที่แก้) = 0 ทุกไฟล์
6. containment gap ของ `test_the_scheduler_has_no_importer_yet` (glob ไม่ลง
   subdir) -- พบและแก้ก่อน commit (ดูหัวข้อด้านบน) นี่คือของที่ pf-adversary น่าจะ
   เจอถ้ามีรอบนี้ บันทึกไว้ตรง ๆ ว่าพบเอง ไม่ใช่ปกปิด

-- LANE-B (COMBAT) รอบ `iok5z1`
