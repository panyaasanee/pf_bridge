round 03psfo
start 2026-09-07T01:21+07:00 (claim `pf_bridge#1601` — ไม่มี marker จนจบรอบ)
claim (ไม่ใช่ takeover — ตอน 01:2x ไม่มี `[LANE-A]` claim เปิดค้างอยู่เลย)

LANE-A · งานรอบนี้ = สองอย่างที่ NOW.md/กฎรอบสั่งไว้ตรง ๆ ไม่ใช่ของที่คิดเอง:
(1) **กู้ `pirate-force-server#951`** ที่ reaper ปิดไปด้วย cherry-pick บนฐาน main ปัจจุบัน
(NOW.md บรรทัดแรก "PR ที่ reaper ปิด กู้ด้วย cherry-pick บนฐาน main ปัจจุบัน หนึ่ง PR ต่อรอบ")
(2) **จ่ายหนี้ `ADVERSARY_PENDING pirate-force-server#951`** ที่รอบ `whpkwf` ฝากไว้ — ผลคืนมาแล้ว
เป็นคอมเมนต์บน `#951` (`#issuecomment-5559874947`) สอง finding CONFIRMED · กฎ COMMON_LANE_ROUND
เขียนว่า "รอบถัดไปของสายเดียวกันสั่ง/รับ adversary บนกิ่งนั้นเป็นงานแรก" — รอบนี้คืองานแรกนั้น

## 1. รอบนี้ขยับ NOW/M ข้อไหน

- **ไม่ขยับ M2** — ตัวบล็อกยังตัวเดิมเป๊ะ: ไม่มีใครรู้เฟรมที่เซิร์ฟเดิมตอบ `TriggerVital 0x1FB2`
  trigger 2/3 · **ไม่มีเฟรมผู้สมัครใหม่เข้ามาในรอบนี้** จึงไม่มีอะไรให้เติมลง `_CANDIDATES`
  (อ่านใบ UI `2124` ซ้ำจนจบแล้ว: ใบนั้น**ถอน**ข้อเสนอ `AddSurveyData` ทิ้งเองตาม `GT-233` ปิด และ
  candidate ที่เหลือ (`TriggerResult`, `handler_va=0x006018A0`) ใบนั้นเขียนเองใน nonclaim ข้อ 3 ว่า
  "ยังไม่ตรวจ ไม่ใช่ข้อสรุป" และส่งเป็นใบ RE ให้ K ไปแล้ว — **ยังไม่มีคำตอบกลับมา**) ⇒ เติมช่องตอนนี้ =
  เฟรมเดา = ผิด `PANYA 1955` ข้อ 4(ข) ตรง ๆ · ไม่ทำ
- **ขยับ**: ของ `#951` ที่หายไปกับ reaper กลับมาอยู่บนฐาน main ปัจจุบัน **และ**หนี้ adversary ของมัน
  ปิดพร้อมกันในใบเดียว ไม่ต้องรออีกรอบ

## 2. ทำอะไร (`pirate-force-server` กิ่ง `claude/nifty-euler-03psfo` — 2 คอมมิต)

**คอมมิตที่ 1 — cherry-pick `19d5dee5` ตรง ๆ ไม่แก้อะไร** (`da80fe2`)
กิ่งเดิม `claude/magical-goldberg-whpkwf` ยังอยู่ครบตามที่ SYNC-NOTICE `2258` สัญญา ·
cherry-pick สะอาด ไม่มี conflict · สองไฟล์ใหม่ 373 บรรทัด (`world_m2_trigger_vital_response.py`
+ เทสของมัน) ไม่แตะ `runtime.py`

**ทำไม `#951` ถึงแดงตอนนั้น และทำไมรอบนี้ไม่แดงด้วยเหตุเดิม** — สาเหตุที่รอบ `whpkwf` วัดไว้เองใน
ไฟล์รอบข้อ 4 คือเทสที่**ไม่เกี่ยวกับ diff ของมันเลย**:
`tests/test_lane_a_choose_npc_scene1.py::…::test_the_talk_trigger_is_still_missing_at_real_dispatch_today`
แดงอยู่บน main ตัวเปล่า ๆ (เพราะ `runtime.py:10359` อ่าน `extra_actions` แล้ว แต่เทสยังตรึงด้วย
`assertNotIn`) · ตัวแก้คือ `#957` ซึ่ง **merge แล้ว** และ `#963` (จ่าย adversary ของ `#957`) ก็
**merge แล้ว** (`merged_at 2026-09-06T17:47:31Z`, `merged_by github-actions[bot]`) ⇒ ฐาน main
วันนี้ไม่มีเทสแดงตัวนั้นอีกแล้ว ยืนยันด้วยชุดเต็มในข้อ 3 ไม่ใช่ด้วยการอนุมาน

**คอมมิตที่ 2 — จ่าย adversary finding ของ `#951` ทั้งสองข้อ**

- **finding 1 (LOW, CONFIRMED)**: docstring ของ `candidate_for_trigger_id()` เขียน "Never raises"
  แต่ `registry=[]` โยน `AttributeError` เปล่า ๆ จาก `.get`
  **แก้แบบทำให้ประโยคเป็นจริง ไม่ใช่แบบลบประโยคทิ้ง**: อาร์กิวเมนต์สองตัวนี้ควรมีท่าที**ตรงข้ามกัน**
  และตอนนี้พูดออกมาแล้ว + บังคับจริง —
  `wire_trigger_id` มาจากสาย ⇒ ตอบ `None` ทุกค่า ทุกชนิด **ไม่โยนเด็ดขาด** (ตรึงด้วยเทสไล่ 16 ค่า
  รวม unhashable/`object()`/`bytes`/`None`) ·
  `registry` มาจากเทสในรีโปนี้เท่านั้น ⇒ ปฏิเสธ**ดัง ๆ มีชื่อ**
  `TypeError(REGISTRY_REFUSED_NOT_A_MAPPING)` ผ่านตัวช่วยใหม่ `_table_for()` ที่ lookup ทั้งสองตัว
  (`candidate_for_trigger_id` + `registered_count`) ใช้ร่วมกัน — กลืนไว้เงียบ ๆ = ซ่อนบั๊กของเทส
  ไว้หลัง `None` ที่ดูสมเหตุสมผล ซึ่งแย่กว่า
  **ลำดับการ์ดไม่เปลี่ยนและตรึงเพิ่ม**: wire id นอก M2 ยังได้ `None` **ก่อน**ที่ registry จะถูกแตะ
- **finding 2 (LOW, CONFIRMED)**: docstring บอกว่าแขน `TRIGGER_VITAL` ของ `runtime.py`
  `return []` "regardless of what any subscribed hook does" — เกินจริง เพราะ `lane_hooks.fire()`
  จับ `Exception` ไม่ใช่ `BaseException` (grep จริงรอบนี้: `except Exception` สามที่ในและรอบ `fire()`
  ที่ `lane_hooks/__init__.py:235,239,245`) ⇒ hook ที่โยน `SystemExit` หลุดออกไปและ `return []`
  ไม่ได้ทำงานเลย · **แก้เป็นการเรียกชื่อช่องโหว่ ไม่ใช่ลบทิ้ง**: เขียนตรง ๆ ว่านี่เป็นพฤติกรรมที่
  **สืบทอดมาจาก `fire()`** ใช้ร่วมกับทุก hook point ในแพ็กเกจ ไม่ใช่ของที่โมดูลนี้ส่งมอบ (โมดูลนี้ไม่
  subscribe อะไรเลย และไม่มีใครนอกเทสของมัน import) แต่คำว่า "always returns []" เป็นคำที่ผิด จึงเลิกใช้

**ไม่ทำ (เหมือน `whpkwf` ทุกข้อ)**: ไม่เติม `CandidateFrame` · ไม่ส่งเฟรมเดา · ไม่ส่ง
`EnterInstanceVital` เอง · ไม่เช็คเลเวล · ไม่แตะ `runtime.py` · ไม่ import โมดูลนี้จากที่ไหนในโค้ดจริง
· `production_allowed` ไม่มีตัวไหนถูกแตะ

## 3. หลักฐานสองชั้น (แยกกัน ไม่อ้างชั้นเดียวกันซ้ำ)

**ชั้นเทส/มิวแทนต์** — `pytest tests/test_world_m2_trigger_vital_response.py -q` → **16 passed,
22 subtests** (เดิม 12 passed/2 subtests) · มิวแทนต์สองตัวบนซอร์สจริง แล้วคืนค่าด้วย backup:
1. ลบเช็ค `isinstance(registry, Mapping)` ออกจาก `_table_for` → **แดง 5 เทส** (รวม subtest ทุกชนิด
   ของ registry ปลอม) แก้กลับ → เขียว 16
2. สลับให้ `_table_for(registry)` ทำงาน**ก่อน**การ์ด wire id ใน `candidate_for_trigger_id` →
   **แดงเทสเดียว ตรงตัว** `test_a_refused_wire_id_is_answered_before_a_bad_registry_is_seen`
   (คือเทสที่เขียนมาเพื่อจับลำดับนี้พอดี ไม่ใช่เทสอื่นบังเอิญแดง) แก้กลับ → เขียว 16

🔴 **บันทึกไว้เพราะเกือบรายงานผิด**: หลังคืนค่ามิวแทนต์ B แล้วเทสยัง "แดง" อยู่หนึ่งตัว ทั้งที่ `diff`
กับ backup บอกว่าไฟล์ IDENTICAL — สาเหตุคือ `__pycache__` ค้าง (มิวแทนต์ B เป็นการสลับบรรทัดล้วน
ขนาดไฟล์เท่าเดิม) traceback ชี้เลขบรรทัดของโค้ดเก่าอยู่ · ลบ `__pycache__`/`.pytest_cache` แล้วเขียว
16 ทันที · ใครรันมิวแทนต์ที่ไม่เปลี่ยนขนาดไฟล์ในรีโปนี้ต้องล้าง cache ก่อนอ่านผล ไม่งั้นจะสรุปผิดว่า
"ตัวแก้พัง"

**ชั้นเกต** — `python3 tools_bridge/pf_gate_preflight.py --repo <server> --base origin/main`
(รันจาก `pf_bridge` clone) → **PREFLIGHT PASS** ครบทุกหัวข้อ (cp874 · no new skips · mainmerge ·
census · branch · bridgesize · queuegrowth · filenamelen · scoreboard-manual · consumedstub) ·
รันสองครั้ง: ครั้งแรกก่อนมี PR body (`[prbody] SKIPPED`) และครั้งที่สอง
ด้วย `--pr-body <ไฟล์> --pr-stage final` → `[prbody] PASS` (marker บรรทัดเดียว บรรทัดที่ 1)
ก่อนเปิด PR จริง — ไม่ได้เปิดแล้วค่อยหวังว่า body ถูก

**ชั้นสาย/การเข้าถึงจริง** — grep ทั้งรีโปว่าใครเรียกโมดูลนี้บ้าง
(`grep -rn "candidate_for_trigger_id\|registered_count\|world_m2_trigger_vital_response" src/ tests/`)
→ **นอกไฟล์ตัวเองมีแต่ `tests/test_world_m2_trigger_vital_response.py` เท่านั้น 16 hit ไม่มี hit ใน
`src/` เลย** ⇒ raise ตัวใหม่ **ไม่มีทางถูกแตะจากอินพุตบนสาย** (ประโยคปฏิเสธนี้มี grep กำกับตามกฎ)

**ชุดเต็ม** — รันครั้งเดียวหลัง `git merge origin/main` (already up to date) บนต้นไม้ที่ push จริง:
**12564 passed / 379 skipped / 26519 subtests passed / 0 failed (621.36s)** — ศูนย์ failed ทั้งชุด
ยืนยันว่าเหตุที่ `#951` โดนปิดหายไปจากฐานแล้วจริง (รอบ `whpkwf` วัดไว้ 1 failed ตัวนั้น)

`ADVERSARY_*` — สั่ง `pf-adversary` บนกิ่งนี้แล้วต้นงาน (ก่อน push) ให้ไล่สี่ข้อ: (ก) raise ใหม่แตะ
สายได้ไหม (ให้ grep เอง ห้ามเชื่อคำผม) (ข) เทสใหม่จับมิวแทนต์ได้จริงไหม (ค) ข้อความใน docstring ที่
แก้ยังจริงกับ HEAD ไหม รวมเลขบรรทัด `runtime.py` ที่เน่าง่าย (ง) อะไรใน cherry-pick ที่จริงตอน `#951`
แต่**เท็จแล้ว**กับ main วันนี้ (main ขยับไป `#957`/`#963`/`#964`/`#965`/`#967`) — **ผลยังไม่คืนตอน
ปิดรอบ** ⇒ `ADVERSARY_PENDING pirate-force-server#969` (push ตามเดิมตามกฎ ห้ามเขียนว่า "ผ่าน adversary")

## 4. `TWO_SESSIONS_SAME_SCENE:`

ไม่กระทบ · `_CANDIDATES` เป็น dict ระดับ process ตามเดิม แต่ทั้งสอง id คงค่า `None` ตลอด ไม่มีจุดใด
ในโค้ดจริงเขียนทับ · `_table_for()` **อ่านอย่างเดียว ไม่เขียน ไม่ก็อป** (คืนตัว mapping เดิม) ⇒ สอง
session ในฉากเดียวกันได้คำตอบเดียวกันเสมอ (`None`) และไม่มี state ให้รีเซ็ตตอน relogin

## 5. `NO_FEATURE_WAITING:`

ไม่มี RE ที่เพิ่งตอบถึงสายนี้ในรอบนี้ที่ต้องเปิดใบสร้าง+GT ทันที · ใบ RE `TriggerResult` ที่ UI ส่งให้ K
(`2124`) ยังไม่มีคำตอบ — ตัวนั้นคือสิ่งเดียวที่จะปลดข้อ 1 ข้างบนได้ และไม่ใช่ใบของสายนี้

## 6. บริโภคใบที่ถึงสายนี้ (วาง stub + สำเนาไป `consumed/` ครบ ไม่ลบต้นฉบับ)

1. `20260906_2258_SYNC-NOTICE-pirate-force-server-pr951-closed-never-merged.md` — **ใช้เต็มใบ**
   ทำตามข้อ 1-3 ของมัน: อ่านเหตุแดง (คอมเมนต์ปิดของ workflow ชี้ commit `19d5dee5`), พบว่าเหตุนั้น
   ถูกแก้ไปแล้วบน main โดย `#957`, กู้ด้วย cherry-pick แทนการทำใหม่จากศูนย์ตามที่ใบเตือนไว้ตรง ๆ
2. `20260906_2241_COO-DECISION-a957-is-the-only-fix-keep-it-one-line-reopen-if-reaped-LANE-A.md`
   — ข้อ 1/2 จบไปแล้วตั้งแต่รอบ `eknq8d`/`20udga` (`#957` merge, `#963` merge) · ข้อ 3 เป็นของ COO
   (ผมไม่แตะ NOW ตามที่ใบสั่ง) · **ข้อ 4 = งานรอบนี้** (กลับไป M2 `#951`) ทำแล้วตามข้อ 2 ข้างบน
3. `20260907_0043_COO-DECISION-panya0039-visibility-filter-is-law-mobappear-is-a-flag-LANE-A.md`
   — อ่านจนจบ · ใบนี้เขียนเองว่า "**ลำดับงานไม่เปลี่ยน** เจ้าของไม่ได้สั่งเริ่มโค้ดฟิลเตอร์ทันที ·
   สิ่งที่ต้องทำ**ตอนนี้** = อย่าเขียนโค้ดใหม่ที่ขัดข้อ 1–4" ⇒ ตรวจ diff รอบนี้กับข้อ 1-4 ทีละข้อ:
   ไม่สร้างโลกที่สอง (ไม่มี state ใหม่เลย) · ไม่แตะ census/appear · ไม่ทำ `MobAppear` เป็น spawn
   (ไม่แตะ `MobAppear` เลย) · ไม่มีรายชื่อมือ · **ไม่ขัดสักข้อ** · เอกสารออกแบบฟิลเตอร์ 1 หน้าเป็น
   ของ "เมื่อถึงข้อ 3 หลัง P-2" ไม่ใช่รอบนี้ ตามที่ใบกำหนดเอง

## 7. ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มีอะไรต่างบนจอ** และรอบนี้พูดตรง ๆ ว่าอย่างนั้น — สิ่งที่ต่างคือ *ของที่หายไปกับ reaper กลับมา*:
เมื่อวานช่องตอบ TriggerVital 2/3 หายไปจาก main พร้อม `#951` ที่ถูกปิด วันนี้มันอยู่บนฐานปัจจุบันและ
สัญญาที่มันเขียนไว้กับตัวเอง ("ไม่โยน") เป็นจริงแล้วแทนที่จะเป็นแค่คำอ้างใน docstring · วันที่ LANE-UI
หา VA + vital id ของเฟรมผู้สมัครเจอ งานที่เหลือยังเป็นเติม dict สองบรรทัด ไม่ใช่ออกแบบใหม่

## 8. รอบหน้าทำอะไร (เรียงลำดับ)

1. **ผล pf-adversary ของกิ่งนี้** ถ้ายังไม่คืนตอนปิดรอบ (ดู SCOREBOARD) — งานแรกของรอบหน้า ตามกฎ
   PENDING เดียวกับที่รอบนี้เพิ่งจ่ายให้ `#951`
2. **M2 ยังบล็อกที่เดิม**: รอคำตอบใบ RE `TriggerResult` (UI ส่งให้ K ในรอบ `2124`) — ได้ VA + vital id
   เมื่อไหร่ ค่อยเติม `CandidateFrame` หนึ่งช่อง **แล้วส่ง CORE-REQUEST ที่ `whpkwf` ข้อ 3 ร่างไว้ให้
   chief จริง ๆ** (จุดเรียกตรงรูปแบบ `census_composer`/`choose_npc_responder` ที่แขน `TRIGGER_VITAL`
   เรียก *ต่อจาก* `fire()` เดิม) — ยังไม่ส่งรอบนี้เพราะยังไม่มีของให้แขนนั้นตอบ ส่งไปก็เป็นงานเปล่าให้ chief
3. **`CORE-REQUEST 2318`** (สาม decline-keyword ใน `runtime.py`) ยังไม่ลง — ทวงรอบนี้เป็นรอบที่สอง
   ตามที่ `20udga` ข้อ 5 กำหนด ถ้ารอบหน้ายังเงียบ = เปิด ASK-COO ไม่ใช่เปิดจดหมายใบที่สี่เรื่องเดิม
4. **D10/D11/D12** (LOW, ค้างจาก adversary ของ `#957`) ยังค้างเหมือนเดิม — หยิบได้เมื่อรอบไหนว่างจริง
5. promotion ข้อ 2 (`lane_a_choose_npc_scene1`) **ยังห้ามพลิกแฟล็ก** จนกว่า `2318` ลง **และ** D13
   (สาย store-session ของ LANE-B ลงครึ่งเดียว) ถูกแก้ — เหตุผลเต็มอยู่ในไฟล์รอบ `20udga` ข้อ 2/6.3

## 9. เวลา

เริ่ม 01:21 · เพดาน 75 นาที = **02:36** · ปิดไฟล์นี้ 01:40 · อยู่ในงบสบาย ๆ
(ชุดเต็มกิน 10 นาที 21 วินาที เป็นก้อนเวลาที่ใหญ่ที่สุดของรอบ)

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรต่าง แต่ช่องตอบ TriggerVital เกาะ 2/3 ที่หายไปกับ PR ที่ reaper ปิดกลับมาอยู่บนฐาน main ปัจจุบันแล้ว และคำสัญญา "ไม่โยน" ที่มันเขียนไว้กับตัวเองเป็นจริงแล้วแทนที่จะเป็นแค่คำอ้างใน docstring | pirate-force-server#969 (open, ไม่ draft, marker ยืนยันด้วย GET แล้ว, cherry-pick 19d5dee5 + 1 คอมมิตแก้ adversary) · pf_bridge claim #1601 · เทสโมดูล 16 passed/22 subtests · ชุดเต็ม 12564 passed/379 skipped/26519 subtests/0 failed (621.36s) · preflight PASS (รวม prbody) · ADVERSARY_PENDING pirate-force-server#969
