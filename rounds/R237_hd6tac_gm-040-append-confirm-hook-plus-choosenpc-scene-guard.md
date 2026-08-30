# R237 (session `hd6tac`) — 2026-08-30T~10:xx+07:00

**ทำอะไร:** ต่อสาย CORE-REQUEST 2 ใบ: append-confirm hook ของ `CORE-REQUEST-GM-040` (สาย GM,
เส้นตาย COO เลยมา ~9 ชม.) + ChooseNPC/TargetVital scene-responder guard ของสาย A (`20260830_0909`)
· ทั้งสองยัง inert จนกว่าสายเจ้าของจะตั้งค่าฝั่งตัวเอง · เปิด `RE-155` ตาม `COO-DECISION 0946` ข้อ 2

---

## ① CORE-REQUEST-GM-040 — append-confirm hook [วัดแล้ว]

เส้นตาย COO 23:59 (29 ส.ค.) ของ `CORE-REQUEST-GM-032` ข้อ 3 เลยมาแล้ว ~9 ชม. ตอนรับใบ
(`notes_to_chief/20260830_0835_...`) `gm/commands.py`'s `OUTCOME_QUEUED` ยัง "RESERVED, AND
UNREACHABLE ON PURPOSE" รอสัญญาณจากจุด append ที่ `runtime.py`

### สิ่งที่ทำ

`runtime.py`'s append site (`if gm_action is not None: actions = actions + [gm_action]`) เช็ค
`getattr(self, "_gm_action_queued_confirm", None)` ทันทีหลัง append — คู่ `(action, callback)`
ที่จับคู่ด้วย `is` กับ `gm_action` ตัวจริง ไม่ใช่ callback เปล่า เคลียร์ก่อนเรียก fail-closed ด้วย
try/except -> `events.append("gm_action_queued_confirm_failed_<Type>")` เมื่อ callback raise
ไม่มีอะไรตั้งค่านี้วันนี้ (inert จนกว่าสาย GM จะเขียน setter ของตัวเองใน `gm/` รอบหน้า) ไม่ได้แตะ
`gm/` ไฟล์ใดเลย (นอกเขต)

### 🔴 pf-adversary หักฉบับแรกได้ 2 ข้อ — แก้แล้วในรอบเดียวกัน

**D1 (สำคัญที่สุด · วัดแล้ว)** ฉบับแรกใช้ callback เปล่าเป็น flag: composed-then-withheld
(route คืน `None` ก่อนถึงจุด append) ทิ้ง callback ค้างบน `self` ไม่ถูกยิง แล้ว **ยิงผิดใบ**กับ
action ของเฟรมถัดไปที่ไม่เกี่ยวข้องกันเลย — adversary reproduce จริงในเวิร์กทรีแยก
**แก้แล้ว:** เปลี่ยนเป็นคู่ `(action, callback)` จับคู่ด้วย identity (`is`) ⇒ callback ค้างจากเฟรมที่
ถูก withhold จับคู่ได้แค่ object เดิมของมันเอง ซึ่งไม่ถูก append อีกตลอดกาล ⇒ ยิงผิดใบไม่ได้อีก

**D2 (วัดแล้ว)** callback ที่ re-arm ตัวเอง (ตั้งคู่ใหม่ระหว่างทำงาน) อาจยิงกับ action ของเฟรมถัดไป
ที่ไม่เกี่ยวข้อง **แก้แล้ว:** การจับคู่ด้วย identity ปิดช่องนี้ไปพร้อมกับ D1 — คู่ใหม่ยิงเฉพาะเมื่อ
action ที่มันระบุถูก append จริงเท่านั้น

เทสใหม่ 6 ใบใน `tests/test_gm_chat_command_dispatch_wiring.py::ActionQueuedConfirmHookTests`
(absent-pairing no-op · fires-once-then-clears · raising-callback ไม่ทำ dispatch พัง · คู่ที่ตั้งไว้
ตอน withhold ไม่ยิงกับ action `==` แต่ไม่ `is` ของเฟรมถัดไปที่ไม่ได้ตั้งอะไรเลย (ปิด D1) · callback
re-arm ยิงเฉพาะกับ action ที่คู่ใหม่ระบุ (ปิด D2))

## ② CORE-REQUEST (LANE-A) — ChooseNPC/TargetVital scene-responder guard [วัดแล้ว]

`RE-154` (เปิดโดย chief รอบก่อน R236) วัดว่าตัวตอบ `ChooseNPC` เดิมของ v141 ลูปทับ**ทั้ง**
`population_indices` แล้วทำ dict lookup แบบไม่มีการ์ดใส่ `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` —
16 ใน 81 index ของฉาก 14 ไม่มีแถวในตารางนั้น ⇒ คลิกแรกของ **ทั้ง 81 ตัว** (ไม่ใช่แค่ 16 ที่หาย)
ทำให้ `KeyError` หลุดออกมาที่ listener thread ตัดการเชื่อมต่อ สาย A สร้างตัวตอบเองแล้ว
(`lane_hooks/lane_a_choose_npc_scene14.py`, `production_allowed = False` เพราะรอ guard นี้)

### สิ่งที่ทำ

ก่อน `super().dispatch(parsed)`: เมื่อ `nested_id in (TARGET_VITAL, CHOOSE_NPC)` และฉากปัจจุบันมี
`lane_hooks.scene_choose_npc_responder(scene_id)` ที่ทั้งลงทะเบียนและ `module_production_allowed`
เป็นจริง ให้ดึง identity ที่คลิกด้วย `legacy.extract_choose_npc_identities(parsed)` แล้วเรียก
responder แทนกิ่งแช่แข็งเดิม **ไม่เรียก `super().dispatch(parsed)` เลย**สำหรับเฟรมนั้น — ตอบไม่ได้
(`None`) หรือไม่มี identity ให้ `actions = []` + event `scene_choose_npc_responder_declined`
พาร์สหรือ responder เอง raise ถูกจับด้วย try/except -> event ชื่อ `_parse_error_`/`_failed_<Type>`
ไม่แตะไฟล์ใน `lane_hooks/` เลย (นอกเขต) — inert วันนี้เพราะไม่มีฉากไหน `production_allowed = True`

### เทส

`tests/test_lane_a_choose_npc_scene14.py`: คลาส `TheCrashThisModuleGuardsAgainstTests` (เดิมพิน
ว่าคลิกจริงยัง crash เพราะไม่มี guard) เปลี่ยนชื่อเป็น `TheGuardAnsweredTheClickInsteadOfCrashingTests`
พร้อมกลับ assertion เป็น "ตอบแล้ว ไม่ crash" (ทั้ง placement ที่มีแถวและที่ไม่มีแถว) + เทสใหม่ 2 ใบ
(declined ไม่ส่งไบต์ + responder ที่ raise ไม่ทำ connection พัง) — ทั้งหมดขับ `state.dispatch()` จริง

### 🔴 pf-adversary หักได้ 2 ข้อ — แก้ด้วยการบันทึก+พิน ไม่ใช่การแก้โครงสร้าง (เหตุผลในคอมเมนต์จริง)

**1 (วัดแล้ว) — claim ฉาก TARGET_VITAL สูญ arming ของ v141 ทั้งชุด** `v141:3788-3811` set
`action_target_last_identity` / `_last_kind` / `p30_action_target_armed` โดยไม่มีเงื่อนไขทุกเฟรม
`TARGET_VITAL` อ่านโดย `ACTION_VITAL` handling ของมันเอง (`exact_p30_target`) — ฉากที่ถูก claim
ไม่เรียก `super().dispatch()` เลย ⇒ ไม่ arm เลย adversary reproduce จริง: หลังคลิกที่ guard ตอบแล้ว
`action_target_last_identity` ยังเป็น `None` ที่ v141 จะ set เป็น identity จริง ไม่กระทบฉาก 14 วันนี้
เพราะ `exact_p30_target` ต้องการรูป arena-harness ที่ actor จริงของฉาก 14 ไม่มี (บังเอิญ ไม่ใช่ออกแบบ)
**ไม่แก้ในรอบนี้** (ไม่มีทางแก้ที่ปลอดภัยโดยไม่ก็อปปี้ตรรกะ v141 ซ้ำ หรือเรียก `super().dispatch()`
แล้วจับ crash กลางคัน ซึ่งรอบนี้ไม่ได้ทำ) — เขียนคำเตือนเต็มลงคอมเมนต์จุด guard ให้ทุกฉากที่จะ
พลิกธงตัวเองอ่านก่อน + เทสพิน `test_claiming_a_target_vital_frame_skips_v141s_own_arming`

**2 (วัดแล้ว) — multi-select ตอบได้แค่ตัวเดียว** กิ่งแช่แข็งตอบทุก identity ที่แยกกันในเฟรม
multi-select (เฟรมละหนึ่ง) แต่ responder ทุกตัวคืน `ChooseNpcResponse` ได้แค่หนึ่งต่อครั้ง (ออกแบบให้
ลองทีละ identity จนตอบได้ ไม่ใช่ตอบทุกตัว) ⇒ ฉากที่ถูก claim ตอบ multi-select ได้แค่ตัวแรกที่ตอบได้
เสื่อมแบบไม่พัง (ตอบหนึ่งดีกว่า crash) แต่ไม่เท่าของเดิม **ไม่แก้ในรอบนี้** (ต้องเปลี่ยน
`ChooseNpcResponse` ให้เป็นชุดคำตอบ ซึ่งเป็นการออกแบบของ `lane_hooks`/สาย A นอกเขต guard)
เทสพิน `test_a_multi_select_click_answers_only_the_first_identity`
🔴 กับดักเทสของตัวเอง: identity ตัวที่สองที่เลือกทดสอบชนกับ `columbus_quest_dispatch.
COLUMBUS_PLACEMENT_INDEX = 1` โดยบังเอิญ (index ต่ำสุดสองตัวของฉาก 14 คือ 0,1 พอดี) ทำให้ action
ที่สองในผลลัพธ์เป็นของ branch Columbus ที่ไม่เกี่ยวข้องกันคนละเรื่อง ไม่ใช่ของ guard เอง แก้เทสให้
กรองเฉพาะ label `LANE_A_CHOOSE_NPC_SCENE14_FACE_*` แทนการนับ action ทั้งหมด

### 🔴 near-miss ของตัวเอง จับได้จากสวีตเอง ไม่ใช่จาก adversary

คอมเมนต์ที่เขียนอธิบายข้อ 1/2 ข้างบน มีอิโมจิ 🔴 หลุดเข้าไปในคอมเมนต์ของ `runtime.py` (บรรทัด 6672)
`tests/test_tree_is_cp874_safe.py` จับได้ทันทีตอนรันสวีตเต็ม (ตรงกับกฎหัวข้อ 9: ต้องเทสด้วยเครื่องมือ
encode ไม่ใช่ดูด้วยตา) — แก้เป็น `!!` ตามธรรมเนียมคอมเมนต์อื่นในไฟล์เดียวกัน ก่อน push

## nonclaims

1. ทั้งสองการเดินสาย **inert** วันนี้ — ไม่มีสายไหนพลิกธงตัวเอง ผู้เล่นยังไม่เห็นอะไรต่างจากเมื่อวาน
2. ไม่มีชั้น client-observable ในรอบนี้ (G-OBS) — ไม่มีใครเปิดเกม
3. `GT-127` ยัง HOLD — ครึ่งของ chief (append confirm hook) เสร็จ แต่ครึ่งอ่านของสาย GM ยังไม่ต่อ
4. `lane_a_choose_npc_scene14.production_allowed` ยังเป็น `False` — เป็นการตัดสินใจแยกของสาย A
   ไม่ได้ถูกพลิกในรอบนี้
5. guard ของ ② **ไม่ใช่ตัวแทนสมบูรณ์ของกิ่งแช่แข็ง** สำหรับฉากที่ claim — ดู pf-adversary ข้อ 1/2
   ข้างบน ก่อนสายไหนจะพลิกธงตัวเอง ต้องเช็คว่าฉากนั้นพึ่ง `action_target_last_identity`/multi-select
   หรือไม่

## หลักฐานรวม

สวีตเต็ม 5370 passed 0 failed เขียว(cloud sanity) · error 17 ใบเป็น `capstone`/`tools` ที่มีอยู่ก่อน
รอบนี้ (วัดด้วย `git stash -u` เทียบ baseline แล้วเท่ากันเป๊ะ) · `HYPOTHESIS_LEDGER PASS entries=47`
ไม่มี drift · โค้ดใหม่ ASCII ล้วน (หลังแก้ near-miss ข้างบน — เทส `test_tree_is_cp874_safe.py` +
`test_the_runtime_source_stays_pure_ascii` ยืนยันแล้ว)

## WIRED

`WIRED = 10 / 10` — ไม่เปลี่ยนจากรอบก่อน ทั้งสองจุดเสียบของรอบนี้ inert (ไม่มี emission จริงบน
production path เพราะไม่มีสายไหนพลิกธงตัวเอง)

## สถานะ push

push แล้ว รอ merge PR — เลขจะเติมหลัง PR เปิด (`pirate-force-server` + `pf_bridge`)
🔴 งานอยู่บน main ต่อเมื่อรอบถัดไปเห็น `merged=true` เท่านั้น
