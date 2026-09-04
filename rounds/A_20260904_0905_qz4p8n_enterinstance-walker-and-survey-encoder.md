# LANE-A รอบ `qz4p8n` — walker ของตัวเองสำหรับ EnterInstance, encoder AddSurveyData, แก้ `GT-228`

เวลาเริ่ม 2026-09-04T09:00+07:00 · เขียน 2026-09-04T09:35+07:00 · สาย A (WORLD)

## รอบนี้ขยับ `NOW.md` ข้อไหน
ขยับ **`COO-DECISION 20260904_0747` ข้อ 3(ก)/(ข)/(ค)** และ **`COO-DECISION 20260904_0850` ข้อ 3**:
ทั้งสามชิ้นของรอบ 08:21/09:51 ที่ค้างอยู่ — โมดูล EnterInstance log-only, encoder AddSurveyData
(ปิดไว้), และแก้ `GT-228` ในฐานะเจ้าของใบ

## ล็อกรอบ
ต้นรอบ list PR `[LANE-A]` open ทั้งสองรีโป = ไม่มี · PR `[LANE-A]` ล่าสุดที่ merged ทั้งสองรีโป
(`pirate-force-server#713`, `pf_bridge#1089`) `merged=true` ทั้งคู่ → งานรอบก่อนอยู่บน main จริง ไม่ต้อง
กู้อะไร

## บริโภคกล่องจดหมาย (ขั้นที่สอง)
สี่ใบที่ยังไม่มี stub ตอนต้นรอบ (สี่ใบก่อนหน้ามี stub แล้วจากรอบ `azhl15`/`azhl15b`):
- `20260904_0747_COO-DECISION-...` ✅ stub + สำเนาเข้า `consumed/`
- `20260904_0801_CHIEF-TO-LANE-A-enterinstance-call-site-landed-hook-point-name.md` ✅
- `20260904_0850_COO-DECISION-...` ✅
- `20260904_0910_CHIEF-TO-LANE-A-WARNING-the-trigger-walker-cannot-decode-tag-0x12.md` ✅
  (ใบแก้ตัวของ chief เอง ต่อจากใบ `0801` ในรอบเดียวกัน — ทำตามใบนี้แทน ไม่ใช่ใบ `0801` ตรง ๆ)

## ทำอะไร (`pirate-force-server#720`)
1. `lane_hooks/lane_a_enter_instance_log.py` (ใหม่) — สมัครจุด
   `vital_inbound_navigationex_enter_instance_vital` ที่จุดยิงลงล่วงหน้าแล้วใน `#716`
   (`nested_id == NAVIGATIONEX_ENTER_INSTANCE_VITAL_ID` → `rx_frames += 1` → `lane_hooks.fire(...)` →
   `return []`) **ไม่มิเรอร์** `lane_a_island_trigger_log.py` ตามคำเตือนใบ `0910`: walker นั้นไม่มี
   tag `0x12` ในตาราง `_TAG_WIDTHS` โดยตั้งใจ (เพราะ `0x12` คือ tag เปิด vital ตัวถัดไปในบริบทของมัน)
   แต่เฟรมนี้ **ไบต์แรกคือ `0x12` เอง** — ถอดตรงตามรูปคงที่ 5 ไบต์ `12 <opaque-u16 LE> 0B 06` ที่
   `RE-227` พินไว้ทั้งความยาว/tag นำ/trailer แทนการเดินแท็ก พิมพ์ `opaque=0x....` เป็นเลขดิบ (nonclaim 3
   ของ `RE-227`) ปฏิเสธมีเสียงเมื่อรูปไม่ตรง (`UNPARSED` + hex มีเพดาน 96 ไบต์เหมือน sibling)
2. `navigationex_survey_record.py` (ใหม่) — encoder nested record `NavigationEx_AddSurveyDataVtial`
   ตามลำดับ field ที่ `RE-227` พินทีละฟิลด์ (`0B` kind byte `+0x10=1` · `12` u16 opaque `+0x12` ·
   สอง `12` u16 ที่ยังไม่วัด `+0x14`/`+0x16` · สาม `2A` f32 XYZ `+0x18/+0x1C/+0x20` · `32` qword
   `+0x28` ที่ยังไม่วัด · `12` u16 ท้าย `+0x30` ที่ยังไม่วัด) ห่อด้วย `make_runtime_vital()` ของไฟล์
   แช่แข็ง (shape เดียวกับที่ `damage_model_hypothesis.py` ใช้กับ vital อื่นอยู่แล้ว — ไม่ได้เดา envelope
   ใหม่ เพราะ `RE-227` ให้แค่ span+hash ของ outer ไม่ได้ให้ field breakdown)
   🔴 **`msg_id` ไม่มีค่า default** — เลข wire id ของ `NavigationEx_AddSurveyDataVtial` ไม่มีอยู่ใน
   `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (grep แล้วไม่เจอ ต่างจาก `TriggerVital`/
   `NavigationEx_EnterInstanceVital` ที่มีบรรทัดจริง) census อื่น (`reports/PF_NAMES_FOLD003_...
   census.json`) เดา `0xC4AF` ไว้แบบไม่มี provenance เท่า registry ตัวจริง ⇒ **ไม่เขียนเลขนั้นลง
   โค้ดเป็นข้อเท็จจริง** ปล่อยให้ chief เติมตอนมี CORE-REQUEST พร้อมโค้ดตัวเลขจริง
   **ไม่ต่อสายส่งจริงที่ไหนเลยในรีโป** — เทสของตัวเอง grep ทั้งรีโป (ไม่ใช่แค่ `src/` ดู pf-adversary ข้างล่าง)
3. แก้สองเทสใน `tests/test_lane_a_navigationex_enter_instance_dispatch_wiring.py` (ของ `#716`) ตาม
   docstring เดิมสั่งไว้เอง (`test_the_point_has_no_subscriber_yet` / `test_an_unsubscribed_frame_...`)
   → เปลี่ยนเป็นยืนยันว่าโมดูลนี้สมัครและถอดค่า opaque ถูกต้องจริงผ่าน dispatcher จริง ไม่ใช่แค่ token ทั่วไป
4. แก้ `GT-228` ในฐานะเจ้าของใบ (chief `0638`/`0747` ยกให้ตัดสินเอง) — ขีดฆ่าคำทำนายเดิม (`0x1FB2` ถือ
   id เกาะ) เขียนคำทำนายใหม่ตาม `RE-227`: **ไม่มีไบต์ออกตอนชนคือผลที่คาดไว้** (ไม่ใช่รอบล่ม) เพราะ
   contact tick ของ NavigationEx ไม่มี direct call ไป outbound submit เลย + เพิ่มขั้นอ่าน HUD `X Y`
   ในขั้น 9-11 ทุกจังหวะชน (แหล่ง XYZ ของ encoder ข้อ 2) — ไม่แตะหัวใบ/objective บรรทัดแรก/เกณฑ์ผ่าน/สเต็ปอื่น

## `pf-adversary` สั่งต้นรอบ ผลกลับมาก่อน merge → แก้ในคอมมิตเดียวกัน (ไม่มี `ADVERSARY_PENDING` ค้าง)
- **D1 [วัดแล้วด้วย mutation]**: guard "ไม่ต่อสายส่งจริง" ฉบับแรก grep แค่ `src/` — เพิ่ม `import
  navigationex_survey_record` ลง `tools/pf_damage_hp_link_headless_replay.py` (ไฟล์ที่ยิง socket จริง
  อยู่แล้ว) แล้ว guard เดิมยังเขียว ⇒ ขยาย grep ให้ครอบทั้งรีโป (ยกเว้นไฟล์ตัวเองกับเทสตัวเอง) วัดซ้ำว่า
  mutation เดียวกันตอนนี้แดงจริง
- **D2 [วัดแล้ว]**: `console_line` ของ EnterInstance hook ไม่มีเพดานความยาว hex ต่างจาก sibling ที่มี
  `_MAX_HEX_BYTES=96` พร้อมเหตุผลเดียวกัน (payload มาจากไคลเอนต์ อาจเป็นของร้าย) — วัดตรง: payload
  2,000,000 ไบต์ผลิตบรรทัดยาว 4,000,072 ตัวอักษรก่อนแก้ ⇒ เติมเพดานเดียวกัน + เทสยืนยันทั้งกรณีตัดและไม่ตัด
- ตรวจแล้วไม่พัง (deliverable เชิงลบ): byte math ของ encoder เทียบ `u8tag/u16tag/f32tag/qwordtag` ตัวจริง
  ในไฟล์แช่แข็ง (ไม่ใช่แค่ self-consistent กับ fixture ตัวเอง) · เทส dispatch-wiring ที่แก้ไม่ trivial
  (มิวแทนต์ byte-order/tag/trailer ทุกจุดจับได้จริงผ่าน `state.dispatch()` จริง) · hook/`fire()` contract
  (`production_allowed=True` · string literal ใน `@hook()` ตาม `lane_gate_name_audit.py`) ·
  field-offset ในเอกสารสอดคล้องกันเอง (ไม่ใช่การเดา wire ใหม่)

## ชุดเทส
- ระหว่างทาง: `pytest tests/ -k "lane_a or navigationex or lane_hooks"` = 430 passed, 1792 subtests
- ชุดเต็ม (commit สุดท้าย บนต้นไม้ที่ merge `origin/main` แล้ว — main ขยับระหว่างรอบเพราะ `#718` LANE-DB
  merge เข้ามา จึง merge แล้วรันซ้ำหนึ่งครั้งเพิ่ม): **9559 passed · 323 skipped · 18733 subtests**
  (7m42s) — เหตุผลที่รันเต็มมากกว่าหนึ่งครั้งในรอบนี้ (กติกา COO เรื่องชุดเต็มครั้งเดียวต่อรอบ):
  ครั้งแรกก่อน merge `origin/main` เข้าต้นไม้ (9553 passed) ยังไม่ใช่ commit สุดท้ายจริง (`origin/main`
  ขยับระหว่างที่รอผล adversary) ⇒ ตามกฎ "ห้าม push สภาพที่ไม่เคยถูกรันเต็มหลัง merge main" ต้องรันซ้ำ

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
บนจอผู้เล่นยังไม่มีอะไร (log-only + encoder ที่ยังไม่ต่อสายส่ง) — สิ่งที่ต่างคือ **คนที่นั่งหน้าจอในใบ
`GT-228`**: เมื่อวานใบทำนายว่าเกาะจะยิง `0x1FB2` id 153/154 วันนี้ใบบอกตรงกันข้ามและอธิบายว่าทำไม (ไม่มี
survey record ที่เซิร์ฟเวอร์ต้อง provision ก่อน) พร้อมขอให้เขาอ่าน HUD พิกัดตอนชน — และถ้าเฟรมยืนยัน
เข้าเกาะมาถึงเซิร์ฟเวอร์จริงเมื่อไร คอนโซลจะพิมพ์ค่า opaque ที่ถอดได้ให้เห็นทันทีแทนที่จะเงียบสนิทหรือถูก
อ่านผิดเป็น hook พัง

## nonclaim
ไม่ได้พิสูจน์ wire id ของ `NavigationEx_AddSurveyDataVtial` · ไม่ได้พิสูจน์ความหมายของฟิลด์ opaque
สี่ตัวที่เหลือ (`+0x14`/`+0x16`/`+0x28`/`+0x30`) · ไม่ได้พิสูจน์ว่าเฟรมชนเกาะจริงจะเรียง nested vital
ตัวแรกเสมอ (ความเสี่ยง D13 เดิมจากรอบ `azhl15b` ยังอยู่ ยังไม่ใช่ของรอบนี้) · ไม่แตะ `runtime.py`/`app.py`

## สถานะจบรอบ
- `pirate-force-server`: push แล้ว รอ merge PR `#720` ("เปิดแล้ว รอ gate")
- `pf_bridge`: ไฟล์รอบ + จดหมายผล + stub ลงกิ่งเดียวกับ claim แล้ว push
- ไม่มี `ADVERSARY_PENDING` ค้างของสาย A
