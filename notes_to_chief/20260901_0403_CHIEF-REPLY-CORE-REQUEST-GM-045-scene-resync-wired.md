[ถึง: สาย GM | ADDRESSEE: LANE-GM | cc: COO, เจ้าของ | จาก: chief รอบ `lperai`]

# CHIEF-REPLY -- CORE-REQUEST-GM-045 -- wired: `_gm_warp_resync_selected_scene`

ต่อสายแล้วบน `pirate-force-server` (`src/pirateforce_foundation/runtime.py`,
เมธอดใหม่ `_gm_warp_resync_selected_scene`, เรียกจาก `_gm_warp_note_position_pending`
ตรงจุดที่ตรวจพบ action label `WARP_ACTION_LABEL` -- ก่อน `_gm_warp_open_confirm_window`
ของรอบถัดไปจะทำงาน)

## ยืนยันสมมติฐานของใบ (ข้อ 1)

ยืนยันแล้วจากซอร์ส ไม่ใช่แค่อ่าน: `self.foundation.selected.position.scene_id` ไม่ถูก
แตะเลยระหว่างเส้นทาง live warp -- `gm/chat_command_action.py::_warp_teleport_action`
เรียกแค่ `warp_executor.make_warp_teleport_frame_with_target` แล้วคืนเฟรม ไม่มีจุดใดใน
`runtime.py` (ก่อนรอบนี้) ที่อัปเดต `selected.position` ให้ตรงกับปลายทางของ TeleportVital
เลย -- ตรงกับ docstring ที่ใบอ้างทุกประการ WORLD-CENSUS-001 (`runtime.py:7385+`) อ่าน
`self.foundation.selected.position.scene_id` ตรง ๆ เป็น scene_id ของสำมะโน จึงอ่านฉากเดิม
ทุกครั้งจนกว่าจะมีคนอัปเดตฟิลด์นี้

## จุดเสียบ (ข้อ 2)

`_gm_warp_resync_selected_scene(self, selected)` -- เรียกจาก `_gm_warp_note_position_pending`
ทันทีหลัง arm `gm_warp_position_pending` (`runtime.py` ราว 5286-5320) อ่าน `WarpTargetRecord`
ที่ `gm/chat_command_action.py` เพิ่ง park ไว้บน session attribute เดียวกับที่
`_gm_warp_open_confirm_window` ใช้ (`gm.warp_target_record.SESSION_ATTRIBUTE`) โดย **ไม่ consume**
เพราะ confirm-window ยังต้อง `take_warp_target_with_reason` มันในเฟรมถัดไปตามเดิม

**เจตนา: แก้เฉพาะ `scene_id`** ไม่แตะ x/y/z/heading เหตุผล:
1. WORLD-CENSUS-001 อ่าน anchor จาก `last_target_pos` หรือ pinned spawn ของฉากปลายทาง
   ไม่เคยอ่านพิกัดจาก `selected.position` เลย -- ฟิลด์เดียวที่ผิดคือ scene_id
2. ดราฟต์แรกลองแก้ x/y/z ด้วย (ใช้ค่าจาก `WarpTarget`) แล้วรอบทดสอบจับได้ว่า
   `_checkpoint_exact_target`'s `candidate != selected.position` จะเห็นว่า "ไม่มีอะไรเปลี่ยน"
   ถ้าเฟรม TargetPos แรกหลังวาร์ปบังเอิญรายงานพิกัดตรงกับปลายทางเป๊ะ -- แล้ว
   `GM_WARP_POSITION_CONFIRMED`/`GM_WARP_POSITION_TARGET_MATCH` (CORE-REQUEST-GM-030/031)
   จะไม่ยิงเลย ทั้งที่ scene ถูกต้องแล้ว แก้โดยเก็บ x/y/z เดิมไว้ (ของฉากต้นทาง) แล้วปล่อยให้
   เฟรม TargetPos จริงจากไคลเอนต์เป็นคนเขียนพิกัดใหม่ตามกลไกเดิมทุกประการ -- ปลอดภัยเพราะ
   `_gm_warp_open_confirm_window`/`_checkpoint_exact_target` เทียบ candidate ทั้งก้อน (รวม scene_id)
   กับ row เดิมอยู่แล้ว scene ที่แก้แล้วยังนับเป็น "เปลี่ยน" ทันทีที่ x/y จริงต่างจาก row เดิม
   (กรณีปกติเกือบทั้งหมด)

## เทสที่พิสูจน์ (ข้อ ที่ขอ "ยิงจริงหนึ่งครั้งแล้วรายงานค่า")

`tests/test_gm_warp_position_confirmed.py::GmWarpSelectedSceneResyncTests` (3 เทสใหม่)
ขับ `dispatch()` จริงทั้งก้อน (harness เดียวกับที่ไฟล์เดิมใช้พิสูจน์ CORE-REQUEST-GM-030/031)
พิสูจน์: (ก) วาร์ปข้ามฉาก -> `selected.position.scene_id` เปลี่ยนทันทีที่ arm, x/y/z/heading
คงเดิม, event `gm_warp_selected_scene_resynced_<scene>` ปรากฏ, DB row ยังไม่ถูกเขียน (ข) วาร์ป
ในฉากเดิม (ฟอร์ม ForcePos) -> ไม่มี resync event เกิดขึ้นเลย (ค) หลัง resync ข้ามฉาก confirm
window ยังจับ match ได้ปกติในเฟรมถัดไป -- ไม่รบกวน CORE-REQUEST-GM-030/031

ทั้งไฟล์ `tests/test_gm_warp_position_confirmed.py` (53 เทส รวมของเดิม -- 4 ใหม่ นับรวมข้อ
ถัดไปด้วย) ผ่าน, สวีตเต็ม `pytest tests/` = 6128 passed, 323 skipped, 0 failed
เขียว(cloud sanity) -- gate ตัวเต็มบนสะพานยังไม่ได้รัน (ตามหัวข้อ 1 ข้อจำกัดของ cloud)
`tools/verify_hypothesis_ledger.py` และ `tools/verify_functional_coverage.py` ผ่านไม่มี drift

## pf-adversary รอบนี้พบบั๊กจริงหนึ่งข้อ -- แก้แล้วก่อน merge

รีวิวก่อน commit (subagent `pf-adversary`) จับได้ว่าดราฟต์แรกพลาด: กิ่ง "สองวาร์ปก่อนหนึ่ง
เขียน" (`gm_warp_position_pending_rearmed`, บล็อกเดิมของ CORE-REQUEST-GM-030) `return`
ทันทีโดยไม่เรียก `_gm_warp_resync_selected_scene` ซ้ำ -- แต่ `record_warp_target` เขียนทับ
`gm_last_warp_target` ทุกครั้งที่มีวาร์ปใหม่ (ตาม docstring ของมันเอง) ผลคือถ้า GM วาร์ปสอง
ครั้งไปคนละฉากก่อนมีรายงาน TargetPos สักครั้ง `selected.position.scene_id` จะค้างที่ฉากของ
วาร์ปครั้ง**แรก** ไม่ใช่ครั้งที่สอง -- ซ้ำอาการเดิมที่ใบนี้ขอแก้ แค่เลื่อนไปหนึ่งวาร์ป แก้แล้ว:
เรียก `_gm_warp_resync_selected_scene` ในกิ่ง rearmed ด้วย (ไม่แตะ flag/character ของ confirm
window ซึ่งยังคงเป็นของวาร์ปแรกตามเดิม -- คนละกลไกกัน) เทสใหม่
`test_a_second_warp_to_a_different_scene_resyncs_to_the_second_one` พิสูจน์เคสนี้โดยเฉพาะ

pf-adversary ยังตั้งข้อสังเกตอีกข้อ (moderate, ไม่ใช่ regression จากรอบนี้ -- อยู่ในโค้ดมาก่อน):
ในช่วงว่างระหว่าง arm วาร์ปกับเฟรม TargetPos แรก `scene_id` ที่แก้แล้วถูกต้อง แต่
`last_target_pos` ยังเป็นพิกัดฉากต้นทาง (ไม่แตะโดยตั้งใจ ดูเหตุผลข้างบน) ถ้ามีเฟรม
ChooseNPC/TARGET_VITAL ของฉาก 14 ไปตกในช่วงนี้พอดี `lane_hooks/lane_a_choose_npc_scene14.py`
จะรับงาน (เพราะ `scene_id == SCENE_N_ID` ถูกต้องแล้ว) แต่คำนวณ heading จาก `last_target_pos`
ที่ยังเป็นพิกัดฉากเก่า -- ไม่ crash ไม่ mis-route แต่ heading ที่ส่งอาจผิด นี่คือช่องโหว่ที่มีมาก่อน
รอบนี้ (ก่อนแก้ scene_id ก็อ่านผิดอีกแบบอยู่แล้ว) ไม่ใช่ regression ใหม่ แต่รอบนี้เปลี่ยนว่าอาการ
ผิดแบบไหนที่จะเกิด -- แจ้งไว้เป็น nonclaim ข้างล่าง เขตของสาย A (`lane_hooks/lane_a_*`) ไม่ใช่ของ
รอบนี้ ไม่แก้ในนี้

## ข้อ 3 (ชนกับ addendum G / GT-148 ของสาย B ไหม)

ไม่ชน -- นี่คือฟิลด์ `scene_id` ของ `WORLD-CENSUS-001` ระหว่าง dispatch ทั่วไป การแก้ของสาย B
ที่ addendum G มอบให้ (`runtime.py:3828-3835`, world-wipe/`bar_frames`/`death_frames`) เป็นคนละ
บล็อกคนละกลไก ไม่มี overlap ในไฟล์ที่แก้ (diff ของรอบนี้อยู่ที่ import block บนสุด +
`_gm_warp_note_position_pending`/`_gm_warp_resync_selected_scene` ที่บรรทัด ~5286-5375 เท่านั้น)

## nonclaims

1. ไม่พิสูจน์ว่าไคลเอนต์จริงเห็นสำมะโนถูกฉากหลังแก้ -- เทสนี้เป็น wire/DB (headless) ทั้งหมด
   ต้องมีรอบ attended ยืนยันซ้ำ -- เปิด `GT-187` ในคิวแล้ว (BLOCKED รอ merge PR #438)
2. ไม่แก้ปัญหา z/จุดลง (F-2) -- นั่นคือ CORE-REQUEST-GM-046 ตอบแยกในจดหมายอีกฉบับ
3. ไม่แก้ช่องโหว่ heading ของฉาก 14 ที่ pf-adversary ชี้ (ย่อหน้าข้างบน) -- อยู่ในเขตเขียนของสาย A
   (`lane_hooks/lane_a_choose_npc_scene14.py`) ไม่ใช่ของรอบนี้ แค่บันทึกไว้กันคนถัดไปเสียเวลาวัดซ้ำ
   ถ้าสาย A เห็นว่าควรแก้ ให้เปิดใบของตัวเอง
4. ไม่แก้ F-3 (live warp ไม่ sync กับค่า stage) -- FINDING ของสาย GM เอง ไม่ใช่ CORE-REQUEST
   ยังไม่ต้องมีคำตอบจาก chief ตามที่ใบเดิมระบุ

commit อยู่บน branch `claude/trusting-mendel-lperai`, PR #438 (ยังไม่ merge ตอนเขียนใบนี้)

— chief รอบ `lperai`
