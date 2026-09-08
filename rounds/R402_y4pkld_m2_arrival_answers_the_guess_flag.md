# R402 (y4pkld) — ธงเดาของ M2 ถูกตอบได้แล้วโดยไคลเอนต์ที่ไปถึงจริง

- เริ่ม 2026-09-08T13:52+07:00 · ล็อก `pf_bridge#1901` (ไม่มีใบ `[LANE-E]` เปิดค้างตอนเริ่มรอบ)
- heartbeat สะพาน `13:44:02+07:00` ห่างจากนาฬิกาผมตอนเริ่มรอบ 8 นาที ⇒ สะพานมีชีวิต ไม่ต้องตรวจนาฬิกาซ้ำ
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 B) · `git status` ไม่มี `LOCK_*.txt` หลุด

## รอบนี้ขยับ NOW ข้อไหน
**ประตู M โทเคน (ข)** — `NOW` "ประตู M (`1825`)" ข้อ (ข) เขียนว่า `chief G1 #1132 draft รอ (ก)` · ผมพบว่าใบนั้น
**ไม่ได้ติดรอ (ก)** จริง ๆ: R401 เขียนไว้เองว่าสิ่งที่ทำให้มัน draft คือ **D3 (CRITICAL) ของ pf-adversary**
ไม่ใช่การรอ PR ปลดธงของ LANE-A (รั้ว `login_would_accept` ที่ R401 ใส่ไว้แปลว่าลำดับ merge ไม่สำคัญอยู่แล้ว)
⇒ รอบนี้จ่าย D3 แล้วส่งใบขึ้นเป็น PR ไม่ draft พร้อม marker

## D3 คืออะไร และจ่ายอย่างไร
`_m2_transport_resync_inner` ตั้ง `scene_label_is_server_guess = True` ตอน relabel ฉากปลายทาง
แต่ทั้งไฟล์มีที่ล้างธงนั้นแค่ **สองแห่ง**: ตอนล็อกอิน กับสาขา `gm_warp_confirm_window_open`
การเดินทาง M2 ไม่เปิดหน้าต่าง confirm ของ GM ⇒ **เซสชันที่เดินทางแล้วล้างธงไม่ได้ตลอดชีวิตของมัน**
(`client_confirmed_scene` ค้าง `None` · วัดเทียบตัวคุมที่ไม่ได้เดินทางซึ่งอ่านได้ 1) ซึ่งไปถึงโทเคน `same_scene`
ของ LANE-GM และ M2 survey trial ของ LANE-A เอง — seam ติดอาวุธให้ธงแล้วปิดประตูไม่ให้ใครตอบมันได้

**สิ่งที่เพิ่ม** (`runtime.py` · เขตผมคนเดียว):
- `_M2ArrivalExpectation` — dataclass frozen ระดับโมดูล เก็บ `WarpTarget` ของจุดที่เฟรม transport ส่งไคลเอนต์ไป
  + `character_id` (ผูกตัวละครแบบเดียวกับ `gm/warp_target_record`) + `marker_id` (ไว้พิมพ์บรรทัดเดียว)
- `_m2_arrival_arm(pending, relocation)` — เรียก **เฉพาะสาขาที่ relabel สำเร็จจริง** (หลังรั้วทั้งสอง)
  ⇒ การเดินทางที่ seam ปฏิเสธเอง ไม่มี expectation ให้ตอบ
- `_m2_note_arrival_if_confirmed(candidate)` → `_m2_arrival_inner` → `_m2_arrival_say` — เรียกจาก
  **สองสาขา**ของ `_checkpoint_exact_target` (สาขา override visit และสาขารายงานตำแหน่งปกติ) เพราะรูที่เปิดแค่สาขาเดียวก็ยังเป็นรูเดิม
- ตรงกันกับหลักฐานที่ `GM_WARP_POSITION_CONFIRMED` ยืนอยู่: รายงานพิกัดที่ห่างจากจุดปลายทาง ≤ `WARP_TARGET_MATCH_TOLERANCE` (1.0)
  ⇒ `_note_client_confirmed_scene(..., "m2_arrival_report")` แล้วล้างธงในลมหายใจเดียวกัน · ไม่ตรง = ไม่ล้าง และบอกว่าห่างเท่าไร

**ทำไม expectation ไม่ consume-once เหมือนของ GM** — ของ GM consume ทิ้งเพราะ RE-129 วัดว่าไคลเอนต์ **เมิน** ForcePos
รายงานถัดไปจึงไม่ใช่ผลของเฟรมนั้น · M2 ใช้ composer อีกตัว (TeleportVital ที่ GT-106-R2 วัดว่ากลไกขยับจอจริง)
และต้นทุนของการเดาผิดไม่สมมาตร: expectation ที่ถูกกินไปก่อนหนึ่งเฟรม = ธงค้างทั้งเซสชัน = D3 กลับมาอีกรอบ
⇒ ค้างไว้จนกว่าจะถูกตอบ / ถูกแทนที่ด้วยการเดินทางใบใหม่ / ถูกทิ้งเพราะป้ายไม่ใช่ "เดา" อีกแล้ว
สิ่งที่กันไม่ให้กลายเป็น "ตรงเมื่อไรก็ได้" คือ tolerance 1.0 (การเดินก้าวละ 400-500 หน่วยตาม `move_authority_hypothesis`)
ไม่ใช่การนับเฟรม

## หลักฐาน (สองชั้น ห้ามปน)
- **สถานะเซิร์ฟเวอร์:** เดินทาง → `lane_a_m2_arrival_armed_scene_<n>` · รายงานที่ปลายทาง →
  `lane_a_m2_arrival_confirmed_scene_<n>` + `client_confirmed_scene_<n>_m2_arrival_report` + ธงเป็น False ·
  รายงานที่อื่น → `lane_a_m2_arrival_not_at_target_<ระยะ>` ธงยังตั้ง · ตัวคุมที่ไม่เดินทางอ่าน `client_confirmed_scene = 1`
- **wire/DB:** ไม่มีอะไรใหม่ในชั้นนี้จากรอบนี้ — แถวถาวรยังเขียนโดย `lifecycle.checkpoint` เส้นเดิม (ทดสอบเดิมของ #1132 ยังเขียว)
- **[วัดแล้ว] ฝั่งเซิร์ฟเวอร์เท่านั้น** ไม่มีใครเห็นไคลเอนต์วาดการมาถึง = `GT-309` จังหวะ (ค) ซึ่ง HELD

`tests/test_m2_teleport_check_seam_wiring.py`: 55 → **70 passed** · เพื่อนบ้านที่อ่านฟิลด์เดียวกัน
(`test_gm_warp_position_confirmed` · `test_lane_hooks` · `test_gm_chat_command_action` ·
`test_gm_warp_persist_census_anchor` · `test_gm_warp_scene_persist`) = 442 passed
**มิวแทนต์ 8 ตัว ตายทั้ง 8**: ตัดจุดเรียกในสาขารายงานปกติ · consume-once · ล้างธงโดยไม่ดูว่าตรงไหม ·
ถอดการผูกตัวละคร · พิมพ์ทุกเฟรม · arm ก่อนรั้ว · ไม่เช็คว่าป้ายเป็นเดา · ล้างธงโดยไม่บันทึกฉาก

## ของที่ self-review ของรอบนี้จับได้เอง (ไม่ใช่เทสเดิม ไม่ใช่ adversary)
ดราฟต์แรกล็อกบรรทัดคอนโซลไว้ครั้งเดียวต่อการเดินทางถูกแล้ว แต่ **ยัง append event ทุกเฟรมที่รายงาน**
⇒ เซสชันที่เดินทางแล้วเดินต่อไปเรื่อย ๆ ทำให้ `self.events` โตไม่จำกัด (รูปเดียวกับที่เพดาน `lane_hooks.fire()`
ของ R393 มีไว้กัน) · แก้ให้ latch เดียวคุมทั้งบรรทัดและ event + เทสที่เดินห้าก้าวแล้วนับ event ต้องได้ 1
และหลังเดินครบยังตอบการมาถึงได้อยู่ (คอมมิตที่สองของใบ)

## QUEUE_TRIAGE:
ไม่มีการแก้ `GAME_TEST_QUEUE.md` ในรอบนี้โดยเจตนา — `PANYA 1910` ย้าย **เนื้อใบ/เลขใบ/พับผล** ไป LANE-K
สิ่งที่รอบนี้ผลิตให้คิวคือ *เนื้อ* ที่ K ต้องเติมลง `GT-309` จังหวะ (ค): โทเคนคอนโซลบรรทัดใหม่
`LANE_A_M2_TELEPORT_CHECK ARRIVAL marker=<m> scene=<n> dist=<d> confirmed=<0|1>` ส่งเป็นจดหมาย `*-TO-K-gt-body-*`
READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ไม่มีใบใหม่ของรอบนี้ · คิวจริงตาม `QUEUE_STATUS_SNAPSHOT.md` (K ดูแล)

## จดหมายที่บริโภครอบนี้ (สำเนาไป `notes_to_chief/consumed/` + stub ครบทุกใบ)
`1232` LANE-DB→chief (0206 เป็น kill จริง) · `1236` LANE-B→chief (โทเคน actors=24 วัดวันนั้นไม่ได้) ·
`1246` COO-DECISION ×2 (0206 แทรกหลัง G1 · D4 ทาง (ก) เจ้าของ = chief) · `1314` SYNC-ALARM สามใบไร้เจ้าของ
`1218` PANYA-DECISION เป็นใบ ALL-LANES ⇒ ตาม `NOW 0442` ไม่วาง `.CONSUMED.txt` ร่วม อ้างเลขเวลาที่นี่แทน

## รอบหน้าทำอะไร (เรียงแล้ว)
1. 🔴 **CORE-REQUEST `0206`** — raise หลัง commit + listener v141 ไม่มี `except` = เซิร์ฟเวอร์หยุดรับทุก session
   **พิกัดจริงบนทรีรอบนี้ (DB อ้าง `:1945` จากทรีของเขา): `src/pirateforce_foundation/runtime.py:2081-2082`**
   ```python
   if self.foundation.backpack != MERGED_V111_BACKPACK:
       raise RuntimeError("committed V111 Backpack state mismatch")
   ```
   🔴 ของแถมที่หาเจอในรอบนี้และทำให้ใบง่ายลงมาก: **สาขาพี่น้องอีกสองใบในไฟล์เดียวกัน
   (`:2107` `item_move_capture_wrong_current_state_no_reply` และ `:2162`
   `item_move_hypothesis_wrong_current_state_no_reply`) เปรียบเทียบค่าเดียวกันอยู่แล้วด้วยรูป
   `events.append(...) + return []`** ⇒ รูปที่ถูกมีอยู่ในไฟล์แล้วสองที่ ใบนี้คือทำใบที่สามให้เหมือนพี่มัน
   ไม่ใช่การประดิษฐ์นโยบายใหม่ · + ลบ/แก้คอมเมนต์ที่บอกว่า inbound pickup ยังไม่ต่อสาย (DB อ้าง `:10180-10184`
   ต้อง grep ใหม่บนทรีของรอบนั้น) ในคอมมิตเดียวกัน (COO `1246` · เส้นตาย ≤ 2 รอบ chief)
   · source pin ของ DB `tests/test_class_weapon_census.py::TheDoorThatMustStayShutUntilCoreRequest0206Tests`
   จะแดงวันที่ใบลง = ถูกต้อง ให้ DB ปลดเอง (เขียนใน PR body)
2. ใบ **workflow ใบเดียว** (ค้างสี่รอบ): reportchars `fE` + tee `LANE_DB_SKIP_CENSUS` + แถว scoreboard ไร้เลข PR = `MALFORMED` (COO `1246` ข้อ 2)
3. `CHIEF_CONTINUATION.md` §0 ลงใต้เพดานอย่างมีที่เหลือ (ใบเล็กแยก) · `AGENTS.md` ≤ 30,720
4. D4 ทาง (ก) หลังผล `GT-288` ชุด 3 กลับมา · กู้ `#1095` (cherry-pick) → `#1084` D1/D3 → `#1076`

## nonclaims
- ธงที่ล้างได้ **ไม่ได้แปลว่าไคลเอนต์ไปถึงจริง** — ครึ่ง "ฉาก" ของการเปรียบเทียบเป็น tautology (relabel ใส่ฉากปลายทางลง
  `candidate.scene_id` ไปแล้ว) สิ่งที่ถูกทดสอบจริงคือ x/y/z ห่างไม่เกินหนึ่งหน่วยจากพิกัดในตาราง MARKER (นี่คือ nonclaim R328 D6 คำต่อคำ)
- ผู้เล่นที่ไม่เคยออกจากฉากต้นทางแล้วบังเอิญยืนห่างจากพิกัดปลายทาง ≤1 หน่วย จะ confirm ผิด — แคบ แต่มีจริง และเขียนไว้ในโค้ด
- ใบนี้ยังเป็นโทเคน **(ข)** ของประตู M ไม่ใช่ตัวประตู · (ก) และ (ค) เป็นของ LANE-A/K
- `TRANSPORT_DURABLE_WRITE_ALLOWED` ถูกอ่าน ไม่ถูกพลิก
- **TWO_SESSIONS_SAME_SCENE:** ทุกฟิลด์ที่เพิ่ม (`_m2_arrival_expected` · `_m2_arrival_said`) เป็นของ connection เดียว
  ตายไปกับ socket ไม่มีอะไรใช้ร่วมกัน ไม่มีบรรทัดไหนเขียนลง world registry ของ LANE-A · สองเซสชันที่เดินทางไปฉากเดียวกัน
  ต่างคนต่าง arm ต่างคนต่าง confirm แถวของตัวเอง
## ชุดเต็ม (บนต้นไม้ที่มี origin/main อยู่แล้ว)
FULL_SUITE: `pytest tests/` = **14,831 passed · 450 skipped · 42,711 subtests passed** ใน 744.38 s (12:24)
บน `87ed577` ซึ่งเป็นคอมมิตสุดท้ายจริงของกิ่ง (`origin/main` `53c5941` เป็นบรรพบุรุษอยู่แล้ว `[mainmerge] PASS`)
ไม่มี skip ใหม่ (`[skips] PASS`) · preflight PASS · รอบก่อนหน้าการแก้ latch วัดได้ 14,830 passed บน `1e50a82`

ADVERSARY_RETURNED_NOT_CLEAN `pirate-force-server#1140` — สั่งตั้งแต่ต้นรอบ คืนผลก่อนปลดล็อก **จ่ายสามข้อในรอบนี้**
(ชุดเต็มของ adversary เองบนคอมมิตกลางรอบ: 14,629 passed — ทุกข้อข้างล่างคือของที่ชุดเทสมองไม่เห็น)

- 🔴 **D1 CRITICAL — ความผิดของแพตช์รอบนี้เอง** วางจุด arm ไว้ **ระหว่าง**การตั้งธงกับบล็อก KA1A-ROOTCAUSE
  และ `_m2_arrival_arm` การ์ดแค่ `OverflowError/TypeError/ValueError` ⇒ `marker_id` ที่ raise อย่างอื่น
  (property/`__int__`) หลุดเข้า blanket `except` ของ `_m2_transport_resync_selected_scene`
  แล้ว **ตัดทั้งบล็อกที่เหลือทิ้ง** · วัดแล้วพร้อมตัวคุม: `world_census_sent=True` บนแถวที่ relabel ไปแล้ว
  = CRITICAL ของ R399 คำต่อคำ (สำมะโนปลายทางไม่เคยยิง · ActionVital ของมอนทุกตัวถูกปฏิเสธ) + บรรทัด `applied=1` หาย
  **จ่าย:** ย้าย arm ไปท้ายสุด + ห่อ `_m2_arrival_arm` ให้ไม่ raise จริง ๆ (มี `_m2_arrival_arm_inner`)
- 🔴 **D2 CRITICAL — ทางฟอกหลักฐาน** `marker_destination(N)` **เท่ากันบิตต่อบิตกับ spawn ของฉาก N ในทะเบียน**
  11 จาก 12 มาร์กเกอร์ที่ seam นี้ relabel ได้ · relabel ทิ้ง x/y/z ไว้ที่แถวต้นทางโดยเจตนา · `Position` มี `heading`
  ⇒ **รายงานที่เปลี่ยนแค่ heading** มาถึงตัวตรวจพร้อมพิกัดต้นทาง แล้ว confirm ที่ `dist=0.000`
  โดยไคลเอนต์ไม่เคยประมวลผลเฟรม transport เลย · ผลต่อสายอื่น: `lane_hooks.current_session_scene_id`
  เปลี่ยนจาก "ปฏิเสธอย่างซื่อสัตย์ (`NoConfirmedScene`)" เป็น **ตอบผิดอย่างมั่นใจ**
  **จ่าย:** expectation จำ **จุดต้นทาง** ไว้ด้วย · การยืนยันต้องมีทั้ง "ขยับจากจุดต้นทาง" และ "ถึงจุดปลายทาง"
  ⇒ เดินทางที่จุดต้นทาง=จุดปลายทาง จะไม่มีวัน confirm ซึ่งเป็นคำตอบที่ซื่อสัตย์ (แยกไม่ออกจริง ๆ)
- 🔴 **D3 HIGH — ความผิดของแพตช์รอบนี้เอง** เพราะ expectation ไม่ consume และเพราะ D2 (มาร์กเกอร์=spawn)
  การ **`/warp` ของ GM** ที่ลงจุดเดียวกันถูก seam นี้เคลมเป็นการมาถึงของ M2: พิมพ์ `confirmed=1` ให้การเดินทางที่ไม่ส่งใครไปไหน
  และ **กลืน event `client_confirmed_scene_<n>_warp_confirmed` ของสาย GM** (เพราะ `_note_client_confirmed_scene`
  return เร็วเมื่อค่าเดิม) **จ่าย:** ยอมยกเฟรมให้ระหว่าง `gm_warp_confirm_window_open` เปิดอยู่ (ไม่ consume)
- **D4 MEDIUM — จ่ายไปแล้วระหว่างรีวิวโดย self-review ของรอบนี้เอง** (event ต่อเฟรม) ผู้รีวิวยืนยันว่า `87ed577` ปิดแล้วพร้อมพิน

**หนี้ที่ยังไม่จ่าย = งานแรกของรอบถัดไปก่อน `0206`:**
- **D5 MEDIUM** latch หนึ่งบรรทัดต่อการเดินทางพิมพ์ที่ "เฟรมแรก" ซึ่งตามเหตุผลของไฟล์เองคือเฟรม **ก่อน** teleport
  ⇒ near-miss ทีหลัง (เช่นพลาด 1.5 หน่วย) **เงียบสนิท** ผู้เทสอ่านได้แค่ "ห่าง 43,203" แล้วสรุปผิดว่าไม่มีอะไรเกิด
  (ผมแจ้งข้อจำกัดนี้ให้ K ในจดหมาย `1410` แล้ว เพื่อไม่ให้ใบ `GT-309` อ่านความเงียบเป็นผลลบ)
- **D6 MEDIUM** จุดเสียบสาขา `login_scene_override_visit` **ไม่มีเทสไหนในรีโปวิ่งผ่านเลย** (มิวแทนต์ลบทิ้ง = เขียวทั้งชุด)
  และสาขานั้นไม่มี durable write ⇒ ยืนยันแล้ว in-memory จะไม่ตรงแถวถาวร ยังไม่มีใครเทส
- **D7/D8 LOW** เทส "ไม่ raise" ของผมพิสูจน์ทางที่ `distance_to_target` จับไว้เองอยู่แล้ว ไม่ใช่ทาง `except` จริง ·
  `marker_id = -1` ไม่เคยถูกรัน
- **คำถามปิดท้ายของผู้รีวิวที่ผมยังตอบไม่ได้ และต้องไปอยู่ในใบ attended:** ยังไม่มีใครวัดว่า **ไคลเอนต์จริง**
  ที่ได้รับเฟรมนี้ รายงานพิกัดปลายทางกลับมาจริงไหม — ตราบใดที่ยังไม่วัด `confirmed=1` กับการล็อกอินกับ `/warp`
  เป็นการสังเกตแบบเดียวกันหมด (การบังคับ displacement ในรอบนี้ทำให้แคบลง แต่ไม่ได้ตอบคำถามนั้นแทน)

SCOREBOARD: COMING | ผู้เล่นที่เดินทางออกทะเลแล้วไปถึงจริง จะทำให้เซิร์ฟเวอร์เลิกเดาว่าเขาอยู่ฉากไหน — ป้ายฉากของเซสชันที่เดินทางถูกยืนยันด้วยพิกัดที่ไคลเอนต์รายงานเอง แทนที่จะค้างเป็น "เดา" ไปตลอดทั้งเซสชัน | pirate-force-server #1140 (เปิดแล้ว ไม่ draft · ครอบ #1132) · GT-309 โทเคน (ข) · rounds/R402_y4pkld_m2_arrival_answers_the_guess_flag.md
