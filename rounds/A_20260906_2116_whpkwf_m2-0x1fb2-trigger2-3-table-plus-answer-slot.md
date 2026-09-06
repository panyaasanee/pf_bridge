round whpkwf
start 2026-09-06T20:58+07:00 (claim `pf_bridge#1561`, ยังเปิดอยู่ ไม่มี marker จนจบรอบนี้)

LANE-A · งาน COO-DECISION `20260906_1955` ข้อ 4(ก)+(ข) เท่านั้น — ข้อ (ค) ไม่ใช่ของรอบนี้ (UI ยังไม่ส่งเฟรมผู้สมัคร)

## 1. อะไรขยับ (NOW.md / M ข้อไหน)

ไม่ขยับหมุดไมล์สโตนใหม่ — M2 ยังค้างที่ "ยังไม่รู้เฟรมที่เซิร์ฟเดิมตอบ 0x1FB2 trigger 2/3"
เหมือนก่อนรอบนี้เป๊ะ (NOW.md บรรทัด LANE-A ระบุเองว่ารอบนี้ = เตรียมของ ไม่ใช่ปิดบล็อก)
รอบนี้ทำสองงาน static ที่ COO สั่งไว้ก่อน promotion: (ก) ตารางสรุปสามรอบ attended ที่มีอยู่แล้ว
(ข) เตรียม "รูปร่าง" ของช่องตอบ ไม่ใช่ไบต์ — ทั้งคู่ไม่ทำให้ผู้เล่นเห็นอะไรต่างเลยจนกว่า UI จะส่งเฟรม

## 2. ส่วน (ก) — ตาราง "หลัง 0x1FB2 trigger 2/3, เซิร์ฟเราส่งอะไรตามมา"

สังเคราะห์จากสามใบผลที่ commit แล้ว ไม่บูตซ้ำ ไม่เดา:

| รอบ | เกาะที่ชน | wire trigger_id | จำนวนครั้ง | เซิร์ฟเราตอบ (ภายใน ≤2 วิ) | จอผู้เล่นเห็น |
|---|---|---|---|---|---|
| R313 | ไม่ถึงขั้นชนเกาะ (dialog error ก่อน) | - | 0 | ไม่มีเฟรม 0x1FB2 เกิดขึ้นเลยรอบนี้ | (ไม่เกี่ยว — ยังไม่ถึงขั้นสัมผัสเกาะ) |
| R318 | Prison Exile ×3 / Spice Paradise ×3 | 2 / 3 | 3+3=6 | `no_responder bytes_out=0` (`LANE_A_TRIGGER_VITAL` บน console — เซิร์ฟไม่ส่งไบต์กลับเลย ไม่ใช่ "ส่งช้า") | ไม่มีหน้าต่างใดเด้งทั้งสองเกาะ · ไม่มี error · client ไม่ปิดตัว |
| R322A | Prison Exile ×3 / Spice Paradise ×3 | 2 / 3 | 3+3=6 | "exact empty RuntimeRes" ทุกครั้ง (คำอธิบายระดับ wire ของข้อเท็จจริงเดียวกับ R318) | ไม่มีหน้าต่างใด · ไม่มี ErrorData · client ไม่ปิดตัว |
| **เซิร์ฟเดิม (ORIGINAL, ไม่ใช่ของเรา)** | - | - | - | **`NO_ORIGINAL_CAPTURE:`** ไม่มี pcap/journal ของเซิร์ฟเดิมตอบ 0x1FB2 อยู่บนสะพานนี้เลย | (ไม่มีข้อมูล) |

หมายเหตุตาราง: "≤2 วินาที" ในหัวใบ COO ไม่มีความหมายต่างจาก "0 วินาที" ในกรณีของเรา — เซิร์ฟ
ตอบว่างในจังหวะเดียวกับที่รับเฟรม (ไม่ใช่ตอบช้าแล้วว่าง) ทั้ง R318 และ R322A ยืนยันตรงกัน

R322A ไม่ได้เพิ่มตัวเลข wire ใหม่ต่อคำถามนี้ (ใบนั้นเทียบไบต์ของ `AddSurveyData` record กับ R318
เป็นหลัก ไม่ใช่ตัวเฟรม 0x1FB2 เอง) — เพิ่มแค่การยืนยันซ้ำที่ชั้น wire ("exact empty RuntimeRes")
คู่กับสิ่งที่ R318 เห็นที่ชั้น log เท่านั้น อ่านแล้ว: ไม่มีอะไรใน R322A ที่แก้ไขแถวของ R318

### `NO_ORIGINAL_CAPTURE:` — grep สี่แหล่งตาม AGENTS.md §7 ก่อนเขียน "ไม่มี" (เก็บผลไว้ครบ)
- `gamedata/tables/` — `grep -rli "1fb2"` → **0 hit**
- `external/` — `grep -rli "1fb2"` → 2 hit ทั้งคู่เป็น TSV ชื่อฟิลด์/คลาส
  (`PF_FIELD_VALIDATION.tsv`, `PF_RUNTIME_CLASSMAP.tsv`) ไม่ใช่ capture
- `archive/` — `grep -rli "1fb2\|original.*capture\|เซิร์ฟเดิม"` → **0 hit**;
  `find . -iname "*original*"` เจอเฉพาะ `evidence_screens/REF_ORIGINAL_SERVER_*`
  (ภาพ/คลิปหน้าจอเซิร์ฟเดิมของเจ้าของ — พยานตา ไม่ใช่ wire) และจดหมาย
  PANYA-REFERENCE/GT078-ADDENDUM ที่เป็นข้อมูลระดับจอเดียวกัน
- `notes_to_chief/consumed/` — สอง grep เดียวกัน → **0 hit**
- ส่วนเสริม: `find . -iname "*.pcap"` ทั้งรีโป → **0 hit**

⇒ ไม่มี capture ระดับ wire ของเซิร์ฟเดิมตอบ 0x1FB2 อยู่บนสะพานนี้จริง เขียน `NO_ORIGINAL_CAPTURE:`
ตามหัวใบสั่ง ไม่เดา

## 3. ส่วน (ข) — ช่องตอบ 0x1FB2 trigger 2/3 ใน M2 scenario (รูปร่าง ไม่ใช่ไบต์)

`pirate-force-server` กิ่ง `claude/magical-goldberg-whpkwf` คอมมิต `19d5dee5`:

**ไฟล์ใหม่** `src/pirateforce_foundation/world_m2_trigger_vital_response.py`
- `CANDIDATE_TRIGGER_IDS = (2, 3)` — ดึงจาก `lane_hooks.lane_a_island_trigger_log.
  M2_OBSERVED_ISLAND_TRIGGER_IDS` ตรง ๆ (reuse ไม่ derive ซ้ำ)
- `CandidateFrame(va, vital_id, frame)` — NamedTuple ว่างเปล่าโดยโครงสร้าง จนกว่าจะมีการลงทะเบียนจริง
- `_CANDIDATES: dict[int, CandidateFrame | None]` เริ่มต้น **ทั้งสอง id = None** และรอบนี้ไม่มีที่ไหน
  ในไฟล์เขียนใส่ค่าเลย — ทั้งคู่ยังว่างตอนจบรอบเหมือนตอนต้นรอบ
- `trigger_id_guard_reason()` / `is_candidate_trigger_id()` — ปฏิเสธ id นอก (2,3) ด้วยชื่อ
  (`TRIGGER_ID_REFUSED_NOT_M2` / `TRIGGER_ID_REFUSED_NOT_AN_INT`) แบบเดียวกับ
  `world_m2_survey_plan.scene_guard_reason` (เช็ค bool ก่อน int เพราะ Python bool เป็น subclass
  ของ int) และ `world_island_dock_table.destination_for_trigger_id` (ปฏิเสธ id ที่ไม่รู้จักแบบ fail-closed)
- `candidate_for_trigger_id(wire_trigger_id, registry=None)` — คืนค่าที่ลงทะเบียนไว้ **ไม่แก้ไข**
  หรือ `None`; พารามิเตอร์ `registry` มีไว้ให้เทสส่ง mapping สังเคราะห์เข้ามาเท่านั้น ไม่มีที่ไหนใน
  โค้ดจริงเรียกแบบนั้น

**ไม่ทำ (ตามข้อห้ามของหัวใบ 4(ข) ตรง ๆ)**: ไม่ส่งเฟรมเดา · ไม่ส่ง `EnterInstanceVital` เอง ·
ไม่เช็คเลเวล · ไม่แก้ `runtime.py` · ไม่ import โมดูลนี้จากที่ไหนในโค้ดจริง (ไม่มี send path)

### จุดที่ตั้งใจแก้ให้ตรง ไม่ใช่ตามที่หัวใบเขียนตรง ๆ
หัวใบพูดว่า "chief ทำ return list จาก `lane_hooks.fire()`'s result เหมือนแขน
`GM_RUN_GM_COMMAND_VITAL_ID`/create-actor" — ตรวจโค้ดจริงแล้วไม่ตรง: แขน
`GM_RUN_GM_COMMAND_VITAL_ID` (`runtime.py:8677`) ก็ `return []` เสมอเหมือนแขน TRIGGER_VITAL ทุก
ประการ ไม่ใช่ตัวเทียบ ตัวเทียบจริงคือ `FOUNDATION_CREATE` (`:8676`) ซึ่งสร้าง return list จากการ
เรียกตรง (`self.foundation.create(...)`) ไม่ใช่จาก `fire()` — และ `fire()` เองมีสัญญาเขียนไว้ชัดว่า
"never returns a value... hooks that need to hand something back to runtime.py are not what this
point shape is for" (`lane_hooks/__init__.py`) แก้ให้ตรง: สิ่งที่ต้องขอ chief คือจุดเรียกตรงแบบใหม่
รูปร่างเดียวกับ `census_composer`/`choose_npc_responder` (registry + `module_production_allowed()`
gate + เรียกตรง) ไม่ใช่การอ่านค่าที่ `fire()` ไม่เคยคืน

**CORE-REQUEST** (บันทึกไว้ ไม่ใช่โค้ดรอบนี้ — 4(ข) ห้ามส่งอะไรจนกว่า UI มีเฟรม):
`runtime.py:8692` แขน TRIGGER_VITAL ต้องการจุดเรียกตรงใหม่ (รูปร่างเดียวกับ census_composer/
choose_npc_responder) ที่เรียก `world_m2_trigger_vital_response.candidate_for_trigger_id
(wire_trigger_id)` **ต่อจาก** `lane_hooks.fire()` เดิม (hook log ยังทำงานเหมือนเดิมทุกกรณี) แล้วถ้า
ได้ `CandidateFrame` ที่ไม่ใช่ `None` ค่อยสร้าง return list จาก `.frame` แทนที่จะ `return []` เสมอ

### กิ่งเดียวกันที่เจอ (ไม่แก้ นอกเขต COO-DECISION นี้)
`world_sea_edge_crossing.py`'s docstring ระบุว่ามันคือตัวที่สองที่ subscribe จุด
`vital_inbound_trigger_vital` — grep จริง (`grep -rn vital_inbound_trigger_vital src/`) แล้วไม่ตรง:
ไฟล์นั้นไม่มี `@hook(...)` เลย (เป็นฟังก์ชันเปล่าที่ยังไม่ถูกเรียกจากที่ไหน ตามที่ docstring ของมันเองยอม
รับ "NOT YET LIVE") ตัว subscriber ตัวที่สองจริงคือ `lane_hooks/lane_q_trigger_vital_dispatch.py`
(LANE-Q) — ยืนยันแค่ว่าจุดนี้รองรับหลาย subscriber ได้จริงตามที่หัวใบต้องการให้ตรวจ ไม่ใช่ประเด็นที่ต้อง
แก้อะไร บันทึกไว้เผื่อจดหมายรอบหน้าอ้างชื่อไฟล์ผิดอีก

## 4. หลักฐานสองชั้น + self-review (ADVERSARY_PENDING)

**ชั้นเทส** — `pytest tests/test_world_m2_trigger_vital_response.py -q` → **12 passed** (2 subtests)
ทุกครั้งหลังแก้ไฟล์ · หลัง `git merge origin/main` (no-op, อยู่ตรงกับ `main` แล้ว `cf961bef`) รันชุดเต็ม
ครั้งเดียว: **12492 passed / 369 skipped / 1 failed / 26248 subtests passed (506.17s)**

**1 failed ที่พบ — ยืนยันว่าไม่เกี่ยวกับ diff รอบนี้**:
`tests/test_lane_a_choose_npc_scene1.py::TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests
::test_the_talk_trigger_is_still_missing_at_real_dispatch_today` — รอบนี้ไม่แตะไฟล์นั้นเลย (diff มีแค่
สองไฟล์ใหม่ ไม่มี import ไขว้) รันแยกไฟล์นั้นเดี่ยว ๆ ก็แดงเหมือนกัน (`1 failed, 69 passed`) ⇒ ไม่ใช่ผล
ข้างเคียงจากรอบนี้ ตรวจ root cause: `runtime.py:10359` บน `main` **อ่าน `extra_actions` แล้วจริง**
(`actions.extend(response.extra_actions)`) แต่เทสตัวนี้ยังตรึงด้วย `assertNotIn` และ docstring ของ
เทสเองเขียนไว้ตรง ๆ ว่า "runtime.py is now queuing extra_actions (CORE-REQUEST 20260904_0137
landed) -- invert this assertion to assertIn ... rather than deleting the test" ⇒ เกตแดงที่ตัวเทสบอก
วิธีแก้ไว้ในตัวเองแล้ว เป็นไฟล์ของสาย A เอง (`lane_a_choose_npc_scene1`) แต่**นอกเขตของรอบนี้**
(COO-DECISION 1955 ข้อ 4 ไม่ได้พูดถึงเรื่องนี้) ไม่แตะที่นี่ ยกไปข้อ 7 (รอบหน้า) ตามกฎ "เจออะไรนอกเขต
รายงาน ไม่ใช่ซ่อมเอง" — หมายเหตุ: `NOW.md` เขียนว่า `0137` "ยังอยู่ใน draft PR ของ chief รอ adversary"
แต่โค้ดจริงบน `main` ที่ clone มาแสดงว่ามันขึ้น main ไปแล้วจริง ๆ (`grep -n extra_actions
src/pirateforce_foundation/runtime.py` → hit ที่ `:10359`) — ความไม่ตรงกันระหว่าง NOW.md กับโค้ดจริง
บันทึกไว้ ไม่ได้เดาว่าใครผิด

**ชั้นเกต** — `python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server --base
origin/main` (รันจาก `pf_bridge` clone) → **PREFLIGHT PASS** ทุกหัวข้อ (cp874 · no new skips ·
mainmerge · census · branch · bridgesize · queuegrowth · filenamelen · scoreboard-manual ·
consumedstub) — `[prbody] SKIPPED` เพราะยังไม่มี PR body ให้เช็ค (เปิดโดย session หลัก)

**self-review มิวแทนต์ (ตามกฎ "ลองมิวแทนต์อย่างน้อยหนึ่งตัวกับ guard/lookup ใหม่")**:
1. มิวแทนต์ A: ลบเช็ค `isinstance(wire_trigger_id, bool)` ออกจาก `trigger_id_guard_reason` (ให้
   `bool` หลุดผ่านเป็น `int` เฉย ๆ) → เทส `test_a_bool_trigger_id_is_named_refused` **แดงทันที**
   (`'TRIGGER_ID_REFUSED_NOT_M2' != 'TRIGGER_ID_REFUSED_NOT_AN_INT'`) แก้กลับ → **เขียวคืน (12
   passed)**
2. มิวแทนต์ B: ลบเช็ค guard ออกจาก `candidate_for_trigger_id` เลย (ให้ lookup ตรงเข้า table โดยไม่
   ผ่านการ์ด) → เทส `test_a_non_m2_trigger_id_returns_no_candidate_even_if_registered` **แดงทันที**
   (คืน `CandidateFrame` ที่ปนเปื้อนแทนที่จะเป็น `None`) แก้กลับ → **เขียวคืน (12 passed)**

ทั้งสองมิวแทนต์ทำบนไฟล์จริงแล้วคืนค่าด้วย backup ก่อนคอมมิต (ไม่มีมิวแทนต์หลงเหลือใน diff ที่ commit)

`ADVERSARY_PENDING pirate-force-server#TBD` (เซสชันหลักเป็นคนสั่ง pf-adversary จริงและเติมเลข PR)

## 5. `TWO_SESSIONS_SAME_SCENE:`

ไม่กระทบ — `_CANDIDATES` เป็น dict ระดับ process แต่รอบนี้ทั้งสอง id คงค่า `None` ตลอด ไม่มีจุดไหน
ในโค้ดจริงเขียนทับมัน สอง session ที่เรียก `candidate_for_trigger_id(2)`/`(3)` พร้อมกันได้คำตอบ
เดียวกันเสมอ (`None`) ไม่มี state ที่เปลี่ยนต่อ session หรือหายตอน relogin เพราะไม่มี state ให้เปลี่ยนเลย

## 6. `NO_FEATURE_WAITING:`

ไม่มี RE ที่เพิ่งตอบในรอบนี้ที่ต้องเปิดใบ+GT ต่อทันที — งานรอบนี้คือเตรียมของ static ตามคำสั่ง COO
ตรง ๆ ไม่ใช่ผลจาก RE ticket ที่เพิ่งปิด ยังไม่มี GT ใหม่จนกว่า UI จะส่งเฟรมผู้สมัคร (ข้อ (ค) ของหัวใบ)

## 7. จดหมายรอบนี้

- **บริโภค**: `notes_to_chief/20260906_1955_COO-DECISION-panya1910-m2-path-A-server-answers-
  0x1FB2-LANE-A.md` — ข้อ 4(ก)/(ข) ทำครบตามที่บันทึกในข้อ 2-3 ข้างบน · ข้อ 4(ค) ไม่ใช่ของรอบนี้ (UI
  ยังไม่มีเฟรม) · ข้อ 1/2/3/5/6 เป็น FYI ไม่มีงานให้สาย A stub วางแล้ว + สำเนาไป `consumed/`
- **ไม่ได้เปิดใบใหม่ให้สาย C** — ไม่มี unknown ใหม่ที่ต้องการ capture; ตัวที่ขาด (เฟรมเซิร์ฟเดิม) already
  tracked เป็นงานของ LANE-UI ตามหัวใบ ไม่ใช่ของ lane C

## 8. ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มีอะไรต่างบนจอเลย** — รอบนี้เป็นงาน static ล้วน: สรุปตารางจากผลเก่าสามใบ (ข้อ ก) และเตรียม
"ที่ว่าง" สำหรับเฟรมตอบ 0x1FB2 ที่ยังไม่มีใครรู้ว่าคืออะไร (ข้อ ข) ทั้งสอง id (2, 3) ยังตอบว่างเหมือน
เมื่อวานทุกประการ — จนกว่า LANE-UI จะส่งเฟรมผู้สมัครที่อ้าง VA + vital id ได้จริง (ตามข้อห้ามของหัวใบ
เอง) การเปลี่ยนแปลงที่แท้จริงคือฝั่งเครื่องมือ: วันที่เฟรมนั้นมา การเติมมันเข้า dict สองบรรทัดคืองาน
ทั้งหมดที่เหลือ ไม่ใช่การออกแบบใหม่

## 9. รอบหน้าทำอะไร

1. **เกตแดงนอกเขตที่พบ (เร่งด่วน กว่า promotion)**: `tests/test_lane_a_choose_npc_scene1.py::
   TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests::
   test_the_talk_trigger_is_still_missing_at_real_dispatch_today` แดงบน `main` จริง (ยืนยันรอบนี้
   ข้อ 4) เพราะ `runtime.py` อ่าน `extra_actions` แล้ว (CORE-REQUEST 0137 ขึ้น main แล้วจริง แม้
   NOW.md ยังเขียนว่าอยู่ draft) — อ่าน docstring เต็มของคลาส `TheRegisteredResponderDropsThe
   TalkTriggerAtRealDispatchTests` ก่อนพลิก `assertNotIn` เป็น `assertIn` ตามที่เทสเองสั่งไว้ อาจมี
   assertion พี่น้องอื่นในไฟล์เดียวกันที่ต้องพลิกพร้อมกัน (ยังไม่ได้ไล่อ่านทั้งไฟล์ในรอบนี้)
2. เมื่อ LANE-UI ส่งเฟรมผู้สมัคร (VA + vital id) — เติม `CandidateFrame` หนึ่งช่องใน
   `world_m2_trigger_vital_response._CANDIDATES` (ไฟล์เดียว บรรทัดเดียวต่อ id ตามที่ไฟล์นี้ออกแบบไว้)
   แล้วส่ง CORE-REQUEST ที่บันทึกไว้ในข้อ 3 ให้ chief จริง (ไม่ใช่แค่บันทึกในไฟล์รอบเหมือนตอนนี้)
3. ถ้า UI เกิน 4 รอบไม่เจอเฟรม (เพดาน COO-DECISION 1955 ข้อ 5) — กลับไปทำ promotion backlog ข้อ 1/2
   ของ NOW.md (`remote_player_hypothesis.py` / `lane_a_choose_npc_scene1.py`) ตามลำดับที่ NOW.md ตั้งไว้

## 10. กำหนดเวลา

เริ่ม 20:58 · เพดาน 75 นาที = 22:13 · ณ เวลาบันทึกไฟล์นี้ (~21:16) ยังอยู่ในงบ

SCOREBOARD: NONE | ผู้เล่นยังเห็นเหมือนเมื่อวานทุกอย่าง — ช่องตอบ TriggerVital เกาะ 2/3 เตรียมที่ว่างไว้แล้วแต่ยังไม่มีเฟรมให้ตอบ เพราะฝ่าย UI ยังไม่ส่งเฟรมผู้สมัครที่อ้างอิงได้จริง (ตามคำสั่ง COO ห้ามเดา) | pirate-force-server commit `19d5dee5` (กิ่ง `claude/magical-goldberg-whpkwf`, PR ยังไม่เปิด ณ เวลาที่เขียนไฟล์นี้) · pf_bridge claim `#1561` · เทสใหม่ 12 passed · ชุดเต็ม 12492 passed/369 skipped/1 failed-pre-existing-unrelated/26248 subtests passed (506.17s) · preflight PASS · ADVERSARY_PENDING pirate-force-server#TBD
