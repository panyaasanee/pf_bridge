# R278 (session `lperai`) -- 2026-09-01T~04:1x+07:00

## บริบท

รอบนี้เป็น chief รอบแรกที่จับล็อกหลังตรวจ PR รอบก่อนของสาย E (#659 pf_bridge, #434 server)
ทั้งคู่ merged=true ยืนยันด้วย `pull_request_read get` (ไม่ใช้ `list_pull_requests`'s `merged`
field ซึ่งวัดแล้วรอบก่อน ๆ ว่าไม่น่าเชื่อถือ) -- งานอยู่บน main ครบ ไม่มีของหาย

หมายเหตุกระบวนการ (ไม่ใช่ของรอบนี้): PR #659/#434 (ที่ทำงานจริงเป็น "รอบ 4w5j25" ตามข้อความ
commit ของมันเอง -- priority reorg, GT-182..186) ไม่เคยถูกเปลี่ยนหัวข้อ/body ออกจาก "WIP round
claim" ก่อน merge และไม่มี `rounds/R278_*.md` เขียนไว้ ผลคือเลขรอบตามหัวข้อ 4 (นับจากไฟล์ `rounds/`
บน main) กระโดดข้ามเลข "278" เชิงความหมายไปเป็น R278 ของรอบนี้แทน (ไฟล์ล่าสุดจริงคือ R277) --
ไม่ใช่เลขชนกัน (หัวข้อ 4 ระบุนับจากไฟล์เท่านั้น) แค่บันทึกไว้เผื่อ COO อยากตรวจว่ารอบไหนทำอะไรจริง

## ต่อสาย CORE-REQUEST-GM-045/046 (หัวข้อ 17 ข้อ 3 -- ก่อนงานอื่นทั้งหมด)

พบ CORE-REQUEST 2 ใบค้างจากสาย GM รอบ `k0w291` -- ต่อสายทั้งคู่:

**GM-045** (WORLD-CENSUS-001 อ่าน scene_id ฉากต้นทางแทนฉากปลายทางหลัง live warp): เขียนเมธอด
`_gm_warp_resync_selected_scene` ใน `runtime.py` แก้เฉพาะ `scene_id` (ไม่แตะ x/y/z -- เหตุผลเต็ม
ในดอกสตริงของเมธอด + จดหมายตอบ) เรียกจาก `_gm_warp_note_position_pending` ตรงจุด arm ของ
CORE-REQUEST-GM-030 เดิม

**pf-adversary (บังคับตามหัวข้อ 10) จับบั๊กจริงหนึ่งข้อก่อน commit**: ดราฟต์แรกไม่เรียก resync
ในกิ่ง "สองวาร์ปก่อนหนึ่งเขียน" (`gm_warp_position_pending_rearmed`) ทำให้วาร์ปครั้งที่สองไปคน
ละฉากไม่ resync เลย ซ้ำอาการเดิมที่ใบขอแก้ แค่เลื่อนไปหนึ่งวาร์ป -- แก้แล้ว เพิ่มเทส
`test_a_second_warp_to_a_different_scene_resyncs_to_the_second_one` พิสูจน์เคสนี้โดยเฉพาะ
pf-adversary ยังพบข้อสังเกตรอง (moderate, มีอยู่ก่อนรอบนี้ ไม่ใช่ regression): ช่วงว่างระหว่าง
warp กับ TargetPos แรก `last_target_pos` ยังเป็นพิกัดฉากเก่า ถ้ามีเฟรม ChooseNPC ของฉาก 14 ตกใน
ช่วงนี้พอดี heading ที่คำนวณอาจผิด -- เขตของสาย A ไม่แก้ในรอบนี้ บันทึกเป็น nonclaim

**GM-046** (ไม่มีจุดเกิดปลอดภัยหลัง warp ข้ามฉาก): ตอบข้อมูล ไม่ใช่โค้ด --
`world_scene_travel.destination()`/`spawn_position()`/`entry_position()` คือตารางที่ login ใช้
อยู่แล้ว และ (แก้คำตอบที่ตรวจผิดในดราฟต์แรกของจดหมายเอง) ฉาก 278 **มี** pinned spawn จริง
(-13270.06, 22794.27, -2492.77) -- ทุกฉากที่ปักหมุดในทะเบียนวันนี้มี spawn ครบ ไม่มีช่องว่างข้อมูล
F-2 ของ GT-172 เกิดเพราะคำสั่ง `/warp <ฉาก> x y` ที่ระบุพิกัดเองไม่เคยเรียกตารางนี้เลย ไม่ใช่เพราะ
ไม่มีตาราง -- GM-A (งานในอนาคต) ต้องแค่เรียกตารางที่มีอยู่แล้ว

เทส: `tests/test_gm_warp_position_confirmed.py::GmWarpSelectedSceneResyncTests` (4 เทสใหม่)
สวีตเต็ม `pytest tests/` = 6128 passed, 323 skipped, 0 failed (สองรอบ ก่อน/หลังแก้บั๊กที่
pf-adversary จับ) `tools/verify_hypothesis_ledger.py` PASS 47, `tools/verify_functional_coverage.py`
PASS ไม่มี drift ทั้งสองตัว

จดหมายตอบ: `notes_to_chief/20260901_0403_CHIEF-REPLY-CORE-REQUEST-GM-045-scene-resync-wired.md`,
`notes_to_chief/20260901_0404_CHIEF-REPLY-CORE-REQUEST-GM-046-spawn-table-pointer.md`

## คิวเทส

เปิด `GT-187` (BLOCKED รอ merge PR pirate-force-server#438) ผ่าน pf-queue-author -- ยืนยัน
client-observable ของ GM-045 ที่ยังพิสูจน์แค่ wire/DB รอบนี้

## กล่องจดหมาย

บริโภคใบถึง chief/ทุกคนที่ไม่มี stub เจอ ~35 ใบ ส่วนใหญ่จ่าหน้า COO/สายเดียว (ไม่ใช่ของ chief
ตามกฎ #19) ที่เป็นของ chief จริง: CORE-REQUEST-GM-045/046 (ตอบแล้วข้างบน), FINDING F-3
(บันทึกไว้ ไม่ต้องตอบ), GT-172 STATUS (informational), CODEX_URGENT heartbeat drop (COO มอบสาย B
แล้ว ไม่มีงาน chief จนกว่าจะมี CORE-REQUEST), KA1A-CONFIRM (ทำครบ 3 ข้อที่ขอ: เขียน
`PROCESS_GATES.md` #20 กฎ marker-substring, ยืนยัน PANYA-ORDER 0215 ถูกบริโภคแล้วตั้งแต่ R278/
4w5j25, ยืนยัน #425/#648 ไม่มีอะไรค้างบน main) -- stub ครบทุกใบที่อ่าน

## PROCESS_GATES.md

เพิ่มกฎ #20: ห้ามพิมพ์สตริง `PF-AUTOMERGE` ลง PR body นอกจากตอนต้องการ merge จริง (workflow จับ
ด้วย substring match ล้วน ประโยคที่บอกว่า "เอาออกแล้ว" ก็ยังมีสตริงจริงอยู่ -- ต้นเหตุที่ #425/#648
merge ฉบับกลางไปโดยไม่ตั้งใจ)

## WIRED

lane_hooks ตอนนี้มี 5 โมดูล (`lane_a_choose_npc_scene14`, `lane_a_scene_census`,
`lane_b_mob_ai_tick`, `lane_gm_chat_command`, `lane_gm_run_command`) ทั้งหมด
`production_allowed = True` -- เพิ่มจาก 4/4 ที่รายงานไว้ R277 (ไม่ใช่รอบนี้เพิ่ม สายอื่นเพิ่มระหว่างนั้น)
**ไม่ได้ตรวจ emission ซ้ำแบบเต็ม (บูต headless + grep console ทุกโมดูล) รอบนี้** เพราะรอบนี้ไม่ได้
แตะ `lane_hooks/` หรือจุดเสียบของมันเลย -- แก้ของรอบนี้อยู่ใน `dispatch()`/`_gm_warp_*` ซึ่งเป็น
โค้ดของ chief เองมาก่อน ไม่ใช่ lane_hooks WIRED = 5/5 [ไม่ยืนยันซ้ำรอบนี้]

## ยังไม่ทำ / ส่งต่อ

- ช่องโหว่ heading ของ ChooseNPC ฉาก 14 ที่ pf-adversary ชี้ -- แจ้งสาย A แล้วในจดหมาย ไม่แก้เอง
- F-3 (live warp ไม่ sync กับ staged login scene) -- รอ GM-A มอบสายก่อน ไม่ใช่บั๊กที่ต้องแก้ตอนนี้
- GT-072 queue-shrink (102KB) -- ยังไม่แตะ ค้างจาก R276 ต่อเนื่อง

push แล้ว รอ merge PR #<เติมหลังเปิด> (pf_bridge), #438 (pirate-force-server)
