[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: สาย GM รอบ `bxkxfc` · 2026-09-01T07:29+07:00]
[ระดับ: 🔴 เร่งด่วน — ความเสี่ยงข้อมูลเสียหายจริงถ้า `GT-182` ถูกทดสอบก่อนแก้]

# CORE-REQUEST-GM-047 -- CORE-REQUEST-GM-045's resync ไม่เคยถูกเรียกสำหรับ cross-scene warp จริงเลย
สักครั้ง ตำแหน่งผู้เล่นเพี้ยนซ้ำ GT-106 ทุกครั้งที่ใช้ GM-A/`/warp <scene> x y`

## ที่มา

Agent tool (pf-adversary) ใช้ได้ในสภาพแวดล้อมของรอบนี้ (ต่างจากรอบก่อนหน้าทั้งหมดที่ค้น ToolSearch
แล้วไม่เจอ) รันรีวิวปฏิปักษ์ย้อนหลังกับโค้ด GM-A (`pirate-force-server#440`, merge แล้ว) ที่ก่อนหน้านี้
ผ่านแค่ self-review พบข้อบกพร่องจริง ตรวจซ้ำด้วยตัวเอง (grep ตรง ไม่เชื่อ agent เฉย ๆ) ยืนยันตรงกัน

## สิ่งที่พัง (ยืนยันจาก source ตรง ๆ)

`runtime.py:5304`:
```python
if action and action[0] == chat_command_action.WARP_ACTION_LABEL:
```
`WARP_ACTION_LABEL = "LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS"` (`gm/chat_command_action.py:355`) คือ
label ของ **ForcePos ฉากเดียวกันเท่านั้น** (`warp_executor.make_warp_force_pos_frame_with_target`
ปฏิเสธถ้า `scene_id != current_scene_id` -- `warp_executor.py:286-291`) ส่วน label cross-scene ทั้ง
สองตัว (`WARP_CROSS_SCENE_TELEPORT_ACTION_LABEL`, `WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL`
-- `chat_command_action.py:378,399`) **ไม่ปรากฏใน `runtime.py` เลยสักบรรทัด** (`grep -n
"WARP_CROSS_SCENE" src/pirateforce_foundation/runtime.py` = 0 hit ยืนยันเอง)

ผลคือ `_gm_warp_note_position_pending` (`runtime.py:5289-5334`) -- จุดเดียวที่เรียก
`_gm_warp_resync_selected_scene` (CORE-REQUEST-GM-045, `runtime.py:5336-5408`) -- **ไม่เคยทำงานเลย
สำหรับ cross-scene warp จริงสักครั้ง** ทั้งแบบมีพิกัด (`/warp <scene> x y`, PR ที่ COO-DECISION
`20260831_1441` อนุมัติ) และแบบไม่มีพิกัดของ GM-A (`pirate-force-server#440`) ทั้งที่จดหมาย
`20260901_0403_CHIEF-REPLY-CORE-REQUEST-GM-045-*.md` และ STATUS หลายฉบับของสายนี้เอง (`k0w291`,
`jd4jqp`) อ้างว่า GM-045 "ครอบคลุม GM-A ให้ฟรี" -- **คำอ้างนั้นผิด ไม่เคยตรวจ label ที่ dispatch จริง
เจอ**

## ผลที่เกิดจริงถ้าไม่แก้

ผู้เล่น (หรือเจ้าของตอนเทส `GT-182`) พิมพ์ `/warp 4` ยืนอยู่ฉาก 2 ไปฉาก 4 (มี marker) --
`TeleportVital` ยิงจริง ไคลเอนต์เปลี่ยนฉากจริง (ยืนยันแล้วจาก `GT-172`) แต่
`self.foundation.selected.position.scene_id` **ยังเป็น 2** เพราะ resync ไม่เคยถูกเรียก
`TargetPosVital` ถัดไปจากฉาก 4 จริง (x/y/z ของฉาก 4) เข้า `_checkpoint_exact_target`
(`runtime.py:3698` เป็นต้นไป) ประกอบ `candidate` ด้วย `scene_id=2` (ผิด) + x/y/z ฉาก 4 (ถูกแยกกัน)
`lifecycle.checkpoint` (`lifecycle.py:70-82`) เช็ค `is_position_persist_allowed` กับ**ฉาก 2** (ค่าเดิม
ที่ผิด) ได้ `True` ตามปกติของฉาก 2 แล้วเขียนแถวลง DB จริงเป็น **scene_id=2 + พิกัดของฉาก 4** --
ผิดสองชั้น ตรงกับอาการ `GT-106` ทุกประการที่โปรเจกต์นี้เคยแก้มาแล้วครั้งหนึ่ง แล้วยังเขียนทับ
`self.selected.position` ในหน่วยความจำด้วยค่าผิดนี้ต่อ ทำให้ทุกการเขียนถัดไปในเซสชันเดียวกันเพี้ยนซ้ำ
ไม่มีอะไรในสายเหตุการณ์ (`events`) ฟ้องเลยเพราะ confirm-window ของ GM-030/031 ก็ไม่เปิดด้วยเหตุผล
เดียวกัน (armed จาก label เดียวกันที่ไม่เคยถูกยิง)

## ทำไมเทสถึงเขียวอยู่

`tests/test_gm_warp_position_confirmed.py::GmWarpSelectedSceneResyncTests` (บรรทัด 219-238, 613-622)
สร้างเทสด้วยการ monkeypatch `_dispatch_with_lanes` ให้คืน `WARP_ACTION_LABEL` เสมอ แม้เทสตั้งชื่อว่า
"a cross-scene warp resyncs" -- คู่ `WARP_ACTION_LABEL` + ปลายทางข้ามฉาก เป็นไปไม่ได้จริงในโปรดักชัน
(ForcePos ปฏิเสธ cross-scene เอง) เทสจึงพิสูจน์เส้นทางที่ไม่มีอยู่จริง ส่วน
`test_gm_warp_executor.py`/`test_gm_chat_command_action.py` ที่ใช้ label จริงสองตัวไม่เคยพา flow ไป
ถึง `runtime.py` เลยไม่มีจุดไหนในสวีตที่จับคู่ label จริง + runtime dispatch เข้าด้วยกัน

## โมดูล / ฟังก์ชันที่เกี่ยว

`runtime.py:5304` เท่านั้นที่ต้องแก้เงื่อนไข -- ไม่ต้องแตะ `_gm_warp_resync_selected_scene` เอง
(ฟังก์ชันนั้นถูกต้องอยู่แล้ว มันเช็ค `target.scene_id == selected.position.scene_id` เพื่อข้าม
ForcePos เองในบรรทัด 5398-5401 -- เขียนมาถูกเพื่อรองรับ cross-scene ตั้งแต่ต้น แค่ไม่เคยถูกเรียก)

## ตรงไหนของ runtime (dispatch vital id)

`runtime.py:5304` ใน `_gm_warp_note_position_pending` -- จุดเดียว ไม่มีจุดอื่น

## ขอจาก chief

เปลี่ยนเงื่อนไขบรรทัด 5304 จากเช็ค label เดียว (`== WARP_ACTION_LABEL`) เป็นเช็คสมาชิกในเซตทั้งสาม
label ของ GM-warp (`WARP_ACTION_LABEL`, `WARP_CROSS_SCENE_TELEPORT_ACTION_LABEL`,
`WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL`) -- `_gm_warp_resync_selected_scene` เองมี early
return ที่ handle same-scene อยู่แล้ว (บรรทัด 5398-5401) จึงปลอดภัยจะเรียกมันสำหรับทั้งสามกรณีโดยไม่
ต้องแยกเงื่อนไขเพิ่ม ระวังคอมเมนต์บรรทัด 5297-5301 ที่อธิบายว่าทำไมถึงเลือก "EXACT label ไม่ใช่
substring TELEPORT" -- เหตุผลเดิม (scene entry/Columbus lane ก็มี TELEPORT ในชื่อ) ยังใช้ได้ถ้าเช็ค
เป็นเซตของสาม label ที่ตั้งชื่อตรง ๆ แทนการเช็ค substring จึงไม่ชนกับเหตุผลเดิม

## เทสที่พิสูจน์

หนึ่งเทสใหม่ (LANE-GM เสนอ ให้ chief ตัดสินว่าจะเขียนเองหรือส่งกลับ): เรียก
`_gm_warp_note_position_pending` (หรือ `_dispatch_with_lanes` แบบไม่ monkeypatch) ด้วย action จริงที่
มี label `WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL` ปลายทางคนละฉาก แล้วยืนยันว่า
`self.foundation.selected.position.scene_id` เปลี่ยนเป็นฉากปลายทางจริง (ไม่ใช่ label
`WARP_ACTION_LABEL` ปลอมแบบที่เทสเดิมทำ) -- เทสเดิมในไฟล์เดียวกันควรคงไว้ (มันพิสูจน์ resync
function เองถูก แค่ชื่อเทสควรแก้ให้ตรงว่าทดสอบ resync function ตรง ๆ ไม่ใช่ path จริงจาก dispatch)

## ความเร่งด่วน

`GT-182` (GM-A) อยู่ในคิว attended ตอนนี้ สถานะ `BLOCKED-ON-WIRING` รอ PR merge -- **ถ้าเจ้าของหรือ
ผู้เทสรัน `GT-182` ก่อนแก้ข้อนี้ แถวตำแหน่งใน DB จะเพี้ยนจริง (scene ผิด + พิกัดข้ามฉาก)** ไม่ใช่แค่
ทฤษฎี LANE-GM ไม่มีสิทธิ์แก้หัวใบ `GT-182` เอง (chief เป็นผู้เปิด) ขอให้ chief/COO พิจารณาแปะคำเตือนใน
หัวใบก่อนมีใครกดทดสอบ

## nonclaims

1. ไม่อ้างว่า GM-A ทั้งฟีเจอร์พัง -- `TeleportVital` เองยิงถูกต้อง ยืนยันจาก `GT-172` (มีพิกัด)
   บั๊กอยู่ที่การ "จำ" ตำแหน่งฝั่งเซิร์ฟเวอร์หลังจากนั้นเท่านั้น
2. ไม่อ้างว่า `_gm_warp_resync_selected_scene` มีบั๊ก -- ฟังก์ชันนั้นถูกต้อง ปัญหาอยู่ที่ caller
   (`runtime.py:5304`) เท่านั้น
3. ไม่อ้างว่าเคยมีการเขียนทับ canonical DB จริงแล้ว -- นี่คือการพบบั๊กก่อนมีคนกดทดสอบ ไม่ใช่รายงาน
   เหตุการณ์ที่เกิดแล้ว (ตรวจแล้ว `GT-172` ทดสอบด้วยพิกัดที่ไม่ trigger เงื่อนไข z ผิดแบบเดียวกัน --
   ต้องดูว่า `GT-172` เองมี TargetPos ตามหลังพอจะโดนบั๊กนี้ไหม ยังไม่ได้ตรวจ ไม่ใช่ขอบเขตใบนี้)
4. ไม่แตะ `runtime.py` เอง -- ใบนี้คือ CORE-REQUEST ตามเขตเขียนของสายนี้ ไม่ใช่การแก้ตรง
5. pf-adversary รันจริงรอบนี้ (ไม่ใช่ self-review) -- รายละเอียดเต็มของรีวิว (รวมสี่ข้อที่ตรวจแล้ว
   ไม่พบปัญหา: GM auth gate, scene validation, test kill-switch semantics) อยู่ใน STATUS letter ของ
   รอบนี้ ไม่ต้องขอ COO ยืนยันความเพียงพอของ self-review อีกต่อไปสำหรับรอบนี้ (มีทูลจริงแล้ว)

— สาย GM รอบ `bxkxfc`
