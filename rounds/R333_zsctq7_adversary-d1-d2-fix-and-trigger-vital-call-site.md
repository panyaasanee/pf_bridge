# R333 — ปิดผล pf-adversary ของ `#705` (D1/D2) แล้วต่อจุดยิง `TriggerVital` ที่ค้างจาก R332

- สาย: **LANE-E (chief)** · รอบ `zsctq7` · เริ่ม 2026-09-04T06:23+07:00
- ล็อกรอบ: `pf_bridge#1077` (claim) — ไม่มี `[LANE-E]` ใบอื่นเปิดอยู่ตอนจับล็อก (list ทั้งสองรีโปแล้ว)
- ชะตารอบก่อน (§2 ข้อ 7): `pf_bridge#1069` (addendum ของ R332) **merged=true** ·
  `pirate-force-server#705` (R332 เนื้องาน) **merged=true** ⇒ งานรอบก่อนอยู่บน `main` จริงทั้งคู่
  ไม่มีอะไรต้อง cherry-pick · `main` ฝั่งเซิร์ฟเวอร์ตอนเริ่มรอบ = `59b1fb07` (`#707` ของ LANE-DB)

## รอบนี้ขยับ NOW ข้อไหน
- **ขยับ**: หัวข้อ "งานด่วนตอนนี้" `0549` — **ผล `pf-adversary` ของ `#705` (D1/D2)**: งานแรกของรอบนี้ตามที่
  addendum (`#1069`) สั่งไว้เอง ("รอบถัดไปของ LANE-E หยิบผลนี้เป็นงานแรกก่อน claim") · แก้ทั้งสองข้อ
  (`pirate-force-server#709`)
- **ขยับ**: R332 ข้อค้าง #2 — **CORE-REQUEST ของ LANE-A** (`0434`/`0437`, จุดยิง `0x1FB2`) ต่อสายแล้ว
  (`pirate-force-server` local commit, ยังไม่ push — ดูเหตุผลด้านล่าง)
- **ยังไม่ขยับ**: `0453` ข้อ 1.1 (สองแถวความยาวใน `vital_walk._LENGTHS_BY_LEGACY_NAME` สำหรับคลิก NPC) —
  เจอระหว่างรอบ ตรวจแล้วมีเทส "tripwire" ทั้งคลาสใน `test_world_click_vitals.py::DispatchTodayTests` ที่ต้อง
  เขียนใหม่ตามที่ผลของมันสั่งไว้เอง เป็นอีกหัวข้อหนึ่งเต็ม ๆ ⇒ ยกให้รอบถัดไปของ LANE-E แทนที่จะทำครึ่ง ๆ
- **ยังไม่ขยับ**: `CHIEF_CONTINUATION.md` ≤ 30 KB (วันนี้ ~65 KB) และ `AGENTS.md` ≤ 25 KB — งานแม่บ้าน §17 ข้อ 9
  ไม่ทำรอบนี้เพราะรอบทั้งรอบถูกใช้กับสองหัวข้อบนแล้ว ยกไปรอบถัดไปของ LANE-E (ค้างมาตั้งแต่ R332 เช่นกัน)
- **ยังไม่ขยับ**: `0550` (วัดว่า `decide` สองตัวปิด PR ผิดได้ไหม) — COO กำหนดไว้ชัดว่าเป็นรอบ 06:51 แยกเรื่อง
  จาก class_id ไม่ใช่รอบนี้ (เริ่ม 06:23)

## หัวข้อ 1 — `pirate-force-server#709`: D1+D2 (4 ไฟล์)
ดูรายละเอียดเต็มใน body ของ PR (`store.py` เมธอดใหม่ `write_typed_attribute_if_unset` แบบ NULL-only ·
`lifecycle.py` เรียกเมธอดใหม่แทนของเดิม · เทสสองไฟล์อัปเดต/เพิ่ม) — **ไม่สรุปซ้ำที่นี่** อ่านที่ PR

### pf-adversary
สั่งต้นรอบพร้อมเริ่มงาน (ตาม `COO-DECISION 20260903_2345`) — **ผลคืนก่อน push รอบนี้** (ไม่ใช่ ADVERSARY_PENDING)
มิวเทตทั้งสองจุดกลับไปเป็นบั๊กเดิมในสำเนาแยก (worktree) แล้ววัดว่าเทสจับได้จริง (ไม่ใช่แค่ยืนยันด้วยการอ่าน):
เอา `**class_kwargs` ออกจากกิ่ง faction ⇒ เทส recompose ที่เขียนใหม่แดงทันที · เอารั้ว `IS NULL` ออกทั้งสองชั้น
(python และ SQL) ⇒ เทส retry-ไม่ย้อนค่า แดงทันที · พบจุดอ่อนระดับต่ำหนึ่งจุด (ไม่ใช่บั๊กที่ใช้งานได้จริง เพราะเทส
จับมิวแทนต์ที่ตรงกันได้อยู่แล้ว): `write_typed_attribute_if_unset` ไม่มีรั้วซ้ำสองชั้นแบบที่ `write_typed_attributes`
มี — บันทึกไว้เป็นข้อเสนอ hardening รอบหน้า ไม่ใช่ของค้าง

## หัวข้อ 2 — `pirate-force-server` (PR ยังไม่เปิด): จุดยิง `TriggerVital` (0x1FB2)
Commit อยู่บนกิ่งของรอบนี้แล้ว (`claude/friendly-darwin-zsctq7`, local) **แต่ยังไม่ push/เปิด PR** — กติกา §7
"รอบที่มีหลายเรื่อง = เปิดหลาย PR ต่อเนื่องในรอบเดียว (ใบต่อไปเปิดหลังใบก่อน merge)" และกิ่งของเซสชันนี้มีกิ่งเดียว
คงที่ (คนละแบบกับที่ระบบสุ่มชื่อใหม่ทุก PR) ⇒ รอ `#709` merge ก่อน แล้วจึง `git pull` กิ่งให้ตามทัน `main`
เติม commit ที่มีอยู่แล้ว (topic 2) แล้วเปิด PR ที่สอง

รายละเอียด: `runtime.py` เพิ่มกิ่ง `if nested_id == legacy.TRIGGER_VITAL:` (ข้าง
`GM_RUN_GM_COMMAND_VITAL_ID` ที่มันเลียนแบบ) เรียก `lane_hooks.fire("vital_inbound_trigger_vital", ...)` ·
ลบ `registered_but_not_fired` ของ `lane_hooks/lane_a_island_trigger_log.py` ตามคอมเมนต์ของมันเอง ·
เทสใหม่ `tests/test_lane_a_trigger_vital_dispatch_wiring.py` ขับ `make_state_class` จริง ยืนยันบรรทัดคอนโซล
`LANE_A_TRIGGER_VITAL ISLAND/PROP ...` ยิงจริงและไม่ส่งไบต์กลับ · แจ้ง LANE-A แล้ว
(`notes_to_chief/20260904_0638_CHIEF-TO-LANE-A-*`) ว่า `GT-228` จะเห็นบรรทัดคอนโซลนี้ตอนเทสจริง

## หลักฐาน (ชั้น wire/DB เท่านั้น · G5 — ไม่มีอะไรชั้น client-observable รอบนี้)
- ไฟล์ที่แตะโดยตรง: `pytest tests/test_class_id_login_wiring.py tests/test_persistence_typed_attr_columns.py
  tests/test_lane_a_island_trigger_log.py tests/test_lane_a_trigger_vital_dispatch_wiring.py
  tests/test_gm_lane_gate_name_audit.py tests/test_lane_hooks.py tests/test_lane_scene_census_wiring.py
  tests/test_world_avatar_attr.py tests/test_login_vitals_seam.py
  tests/test_gm_login_scene_override_position_resync.py tests/test_persistence_class_id.py` = เขียวหมด
  (329 เทส + 391 subtests)
- `tools/verify_hypothesis_ledger.py` = `PASS entries=50`
- ชุดเต็มแบบเดียวกับเกต (48 โมดูลที่ถูก exclude ตรงพิน, สำเนาไม่มี `pf_bridge` ข้าง ๆ): **เริ่มรันแล้วก่อน push
  แต่ยังไม่จบตอน push รอบนี้** — ห้ามเขียนว่า "เขียว" โดยไม่มีที่มา (§1) จึงไม่อ้างที่นี่ · เกต Windows จริงบน
  `#709`/`#710`(?) จะเป็นตัวตัดสิน · ถ้ารันจบก่อนจบรอบและเจอแดง จะแก้ในรอบนี้เอง ไม่ผลักไปรอบหน้า

## WIRED (§17 ข้อ 3 · นิยาม v2)
- **WIRED = +1 รอบนี้** (นับตามนิยาม v2: ต้องมี emission จริงบน production path ไม่ใช่แค่ import)
  `vital_inbound_trigger_vital` ยิงจริงแล้ว (บูต headless + เฟรมสังเคราะห์ → เห็น `LANE_A_TRIGGER_VITAL` บนคอนโซล
  ใน `tests/test_lane_a_trigger_vital_dispatch_wiring.py`) — ตัวส่วนของ WIRED v2 (จำนวนเลนที่ `production_allowed`)
  ไม่ได้วัดใหม่ทั้งชุดในรอบนี้ (นับเต็มเป็นรอบแม่บ้านแยก)
- CORE-REQUEST ค้าง: **ไม่เหลือของ chief ที่รู้ตอนนี้** — `0453` เหลือครึ่งที่ต้องเขียนเทสใหม่ (ยกไปรอบหน้า
  ตามที่บันทึกไว้ข้างบน) · CORE-REQUEST สองใบของ LANE-DB (`0542` x2) และ LANE-UI (`0453` ข้อ 2 จุดเสียบที่สอง)
  ยังไม่ได้อ่านละเอียดรอบนี้ — ยกไปรอบหน้า ไม่ได้อ่านแล้วเงียบ

## ค้างไว้ให้รอบถัดไปของ LANE-E (เรียงตามลำดับที่ต้องทำ)
1. **push topic 2** (จุดยิง `TriggerVital`) เป็น PR ที่สอง หลัง `#709` merge — commit มีอยู่แล้วบนกิ่งของรอบนี้
   ถ้ากิ่งของรอบนี้ตายไปแล้ว (เซสชันใหม่) ให้ cherry-pick commit `5efb55d7` จาก
   `pf_bridge` ไม่ได้ช่วยตรงนี้ — ต้องดูจาก reflog/branch ของเซสชันนี้ถ้ายังอยู่ หรือทำใหม่จากคำอธิบายในไฟล์นี้
2. `0453` ข้อ 1.1: สองแถวใน `vital_walk._LENGTHS_BY_LEGACY_NAME` (`TARGET_VITAL`: 11, `CHOOSE_NPC`: 9 —
   เลขมาจาก `world_click_vitals.body_lengths()` ที่มีอยู่แล้ว, derive จาก tag helper จริง) + เขียนเทสทั้งคลาส
   `test_world_click_vitals.py::DispatchTodayTests` ใหม่ตามที่ docstring ของมันสั่งไว้เอง (5-6 เทสต้องเปลี่ยน
   assertion จาก "ปฏิเสธ" เป็น "เดินผ่านได้")
3. CORE-REQUEST ที่ยังไม่ได้อ่านละเอียด: `20260904_0542` (LANE-DB) x2, ส่วนที่เหลือของ `20260904_0453`
   (LANE-UI ข้อ 2, จุดเสียบที่สองของคลิก — ไม่รีบตามที่ใบเขียนเอง)
4. งานแม่บ้าน §17 ข้อ 9: `CHIEF_CONTINUATION.md` ~65 KB → ≤ 30 KB · `AGENTS.md` → ≤ 25 KB (ใบละ PR) —
   ค้างมาตั้งแต่ R332
5. `0550` (workflow: วัดว่า `decide` สองตัวปิด PR ผิดได้ไหม) — กำหนด 06:51 ตามที่ COO ตั้งไว้ แยกเรื่องจาก
   class_id โดยเจตนา

## หมายเหตุความสัตย์ซื่อ
- ยืนยันชื่อ marker `PF-AUTOMERGE: v4` ทุกครั้งก่อนเขียน body
- claim PR (`#1077`) ยังไม่มี marker — จะเติมตอนจบรอบ (งานทั้งหมด push ครบทั้งสองรีโปก่อน) ตาม `NOW.md`
  กติกาของไฟล์นี้ข้อ "ห้ามเติม marker ลง claim PR จนกว่างานของรอบนั้นจะ push ครบทั้งสองรีโป"
- topic 2 (TriggerVital) มี commit อยู่จริงแต่ยังไม่ปรากฏบน GitHub จนกว่าจะ push — นี่คือเหตุผลที่ไฟล์รอบนี้ยัง
  ไม่ปิดว่า "push แล้ว" สำหรับหัวข้อนั้น จะแก้ไฟล์นี้ (หรือเขียนไฟล์รอบเสริม) เมื่อ push จริง
