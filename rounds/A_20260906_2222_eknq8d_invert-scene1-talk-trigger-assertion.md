round eknq8d
start 2026-09-06T22:22+07:00 (claim `pf_bridge#1574` · ไม่มี marker จนจบรอบนี้)

LANE-A · งานตาม `COO-DECISION 20260906_2141` ข้อ (1)+(2) ทั้งสองข้อ — ทำครบในรอบเดียว

## 1. รอบนี้ขยับ NOW/M ข้อไหน

- **ขยับ**: NOW `KNOWN_RED_MAIN:` แถวของสาย A (`test_lane_a_choose_npc_scene1.py
  ...still_missing_at_real_dispatch_today`) — `pirate-force-server#957` ลบแถวนี้เมื่อ merge
  (ชุดเต็มบนกิ่ง: **12479 passed, 373 skipped, 26243 subtests, 0 failed**)
- **ขยับ**: ท่อ promotion อันดับ 2 (`lane_a_choose_npc_scene1.py`) — **ครึ่ง "แอ็กชัน" ของราคาปลดแฟล็ก
  จ่ายครบแล้ว** วัดที่ dispatch จริง ไม่ใช่ที่ `respond()` · ไม่มีงานของสาย A เหลือในลิสต์ step 1-7
- **ไม่ขยับ**: M2 (0x1FB2 trigger 2/3) — รอบนี้ไม่แตะตามคำสั่ง COO ที่ให้แทรกงานเทสก่อน
  · `#951` (ตาราง 0x1FB2) ยังเปิดรอ merge เหมือนเดิม · **ไม่ส่งเฟรมเดา** ตาม `1955`

## 2. ทำอะไร (`pirate-force-server#957` · 2 ไฟล์ · เปิดแล้ว ไม่ draft มี marker · **รอ gate**)

### (ก) กลับ assertion ตามคำสั่ง — เทสเดียว ชื่อเดียว
`TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests`:
`assertNotIn` → `assertIn` · ชื่อเมท็อดใหม่ `test_the_talk_trigger_rides_the_real_dispatched_click_today`
· **ไม่ลบคลาส** ตาม docstring ของคลาสเอง · เพิ่มการปักหมุดว่า label ของ frozen path ต้อง **ไม่อยู่**
ในคำตอบ (มิวแทนต์ที่จะรอด: label `_VIA_LANE_A` โผล่จากทางอื่น — ปิดด้วยคู่ assertNotIn + จำนวน 2 แถว)

### (ข) ยืนยันว่า talk trigger ถึง actions ของคลิกจริง (ข้อ 2 ของคำสั่ง) — ถึงจริง
วัดผ่าน `runtime.make_state_class` ด้วย responder ลงทะเบียนจริง (ไม่ใช่ slot ปลอม):

| คลิก | frozen (main วันนี้) | ผ่าน responder |
|---|---|---|
| P3 | `V98_NPC_FACE_PLAYER_POSITION_HEADING_P3` + `V98_NPC_CONVERSATION_DEFAULT_P3` | `LANE_A_..._FACE_P3` + `V98_NPC_CONVERSATION_DEFAULT_P3_VIA_LANE_A` |
| P91 ร้าน | `V112_TEST_HARNESS_FACE_PLAYER_P91` + `..._TRADE_ZOOM_STORE5_SWORD_SOUL` | `LANE_A_..._FACE_P91` + `..._TRADE_ZOOM_STORE5_SWORD_SOUL_VIA_LANE_A` · **คลิกที่ 2 ในเซสชันเดียวกัน = face เปล่า** (`shop_store5_open_sent=True`) |
| P1 Columbus | face + talk + `CORE_REQUEST_014_COLUMBUS_Q3021_...` | สามแอ็กชันเท่ากัน (สอง label เป็นของสาย) |
| P30 | `[]` | `LANE_A_..._FACE_P30` (ได้เพิ่ม) |
| P0 | `[]` | `[]` (เท่ากัน — ไม่ใช่ regression) |

⇒ ตอบข้อ 2 ของ COO: **ถึงจริง ไม่ต้องเขียนจดหมายว่า `0137` ต่อไม่ครบ** · เพิ่มเทส dispatch อีก 2 ตัว
(ร้านเปิดครั้งเดียวต่อเซสชัน · Columbus ไม่เสีย quest action) เพราะครึ่งที่ตัดสินว่า "ปลดแฟล็กแล้ว
เมืองเสียร้านไหม" คือ latch ไม่ใช่ talk trigger

### (ค) docstring ของโมดูล — ขีดฆ่า step 1 และ step 2 (บรรทัดของ chief ลง main แล้ว)
แทนตาราง "WHAT THE FLIP WOULD COST TODAY" ด้วยแถวที่วัดรอบนี้ · หด "เหตุผลที่แฟล็กยังปิด" เหลือ
ข้อเดียว: **คีย์ decline สามตัวของ step 4/5** (`world_census_identity_resolved`, `runtime_ack_sent`,
`exact_frozen_marker1_ready_pc`) ยังไม่มี call site ไหนใน `runtime.py` ส่ง (grep ที่ HEAD)
· `production_allowed` **ยังเป็น `False`** รอบนี้ไม่แตะ

## 3. หลักฐาน / เกต
- `pf_gate_preflight.py --repo <server>`: **PREFLIGHT PASS**
- ชุดเต็มหลัง `git merge origin/main` (Already up to date): **0 failed** (611 วินาที)
- `ADVERSARY_PENDING pirate-force-server#957` — สั่ง `pf-adversary` ต้นรอบบนสโคปนี้เป๊ะ
  ผลยังไม่คืนตอน push · **รอบถัดไปของสาย A หยิบผลนี้เป็นงานแรก**

## 4. จดหมายที่เขียนรอบนี้
- `20260906_2315_LANE-A-TO-CHIEF-scene1-class-rename-needs-coverage-note-and-seam-pin.md`
  — ชื่อคลาสยังเขียนว่า "Drops" ซึ่งเท็จแล้ว แต่ถูกอ้างเป็นสตริงใน `docs/FUNCTIONAL_COVERAGE.json`
  และคอมเมนต์+หมุด digest ใน `tests/test_foundation_legacy_seam.py` — **นอกเขตเขียนของสาย A**
  จึงไม่เอื้อมไปแก้ ส่งให้ chief แทน (คอมเมนต์ในไฟล์ seam ยังเขียนว่าเทสนี้ "pins an absence" = เท็จ)
- `20260906_2318_LANE-A-CORE-REQUEST-scene1-three-decline-keywords-last-gate.md`
  — สามบรรทัดสุดท้ายก่อนปลดแฟล็ก (ข้อความเต็มอยู่ในค่าคงที่ของโมดูลแล้ว)

## 5. บริโภคผลใบที่ถึงสายนี้
- `20260906_2141_COO-DECISION-gm2046-...-invert-assertion-LANE-A` → **ใช้ครบทั้งสองข้อ** (ข้อ ก/ข ข้างบน)
- `20260906_2124_LANE-UI-TO-A-candidate-frame-addsurveydata-sailing-key-fix` → **อ่านแล้ว ยังใช้ไม่ได้
  รอบนี้**: ใบนั้นเป็นเรื่อง M2/`AddSurveyData` ซึ่ง `PANYA-ORDER 1910` + `COO-DECISION 1955` สั่งพับแล้ว
  (UI ถอนข้อเสนอ trial เองในใบ) · ของที่ยังมีค่าคือคีย์ `n_ID=6`/`n_ID=2` เป็น**คำอธิบายย้อนหลัง**ว่า
  ทำไม `GT-233` v3 เงียบ และ candidate ที่เหลือคือ `TriggerResult` — ทั้งคู่เป็นวัตถุดิบของรอบ M2
  ถัดไป ไม่ใช่ของรอบนี้ที่ COO สั่งให้ทำเทสก่อน · **ไม่ออกใบ trial ใหม่ ไม่ส่งเฟรมเดา**

## 6. รอบหน้าทำอะไร (เรียงตามลำดับ)
1. **ผล `pf-adversary` ของกิ่ง `claude/nifty-euler-eknq8d` (`#957`) — งานแรก ห้ามข้าม**
2. M2 ต่อจาก `1955`/`#951`: ใช้ใบ UI `2124` (candidate `TriggerResult` · คีย์ `n_ID` ที่แก้แล้ว)
   ไล่ต่อจาก artifacts ที่ commit แล้วเท่านั้น — **ห้ามส่งเฟรมเดา ห้าม trial `AddSurveyData`**
3. ถ้าสามบรรทัด decline ของ `CORE-REQUEST 2318` ลง main แล้ว: ร่างใบ attended ของ step 3
   (คลิกคนเมือง / ร้านค้า / P30 พร้อมอาวุธผูก) ส่งเป็น `*-TO-K-gt-body-*` แล้วค่อยขอปลดแฟล็ก
4. ยังไม่ลง: ทวง `#951` และ `#957` ตามสถานะ gate (ห้ามเปิดใบที่สาม เหตุเดิมสองรอบติด)

SCOREBOARD: COMING | คลิก NPC ที่ Port Royal ผ่าน responder ของสายนี้ตอบ "หันหน้า + เปิดบทสนทนา" ครบ และร้านค้าเปิดครั้งเดียวต่อเซสชันแล้วที่ชั้น dispatch จริง (ยังไม่ถึงผู้เล่น แฟล็กยังปิด รอสามบรรทัด decline ของ chief) | pirate-force-server#957 · pf_bridge#1574
