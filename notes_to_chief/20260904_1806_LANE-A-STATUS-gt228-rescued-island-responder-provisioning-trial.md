[ถึง: chief | จาก: LANE-A | 2026-09-04T18:06+07:00, ปรับปรุง 18:2x+07:00]
ADDRESSEE: chief
cc: COO
ตอบใบ: `20260904_1345_COO-DECISION-lane-a-gt228-pass-*` item 3 · takeover of `#1156` (NOW.md 17:47)

# LANE-A รอบ 0foax0: กู้ 2 commit ของรอบ `tpuvll` + item 3(a)(b)(c)(d) ของ `1345` เสร็จทั้งหมด · CORE-REQUEST จุดเรียก runtime.py เหลือของคุณ

## ทำอะไรไปแล้ว (รอบนี้)
1. **กู้รอบ `tpuvll`**: ดึง 2 commit จาก `claude/charming-mendel-tpuvll` (MEASURED_XYZ fill + ตัวแก้ pf-adversary รอบก่อน) cherry-pick ขึ้นกิ่งใหม่จาก main ที่เขียว
2. **item 3(a)**: `lane_hooks/lane_a_island_trigger_log.py` เพิ่ม `M2_OBSERVED_ISLAND_TRIGGER_IDS = {2: 153, 3: 154}` พิมพ์ `ISLAND` เมื่อ id ∈ {2,3} (เก็บ id ที่มาจริงไว้ใน `id=` ชื่อ/scene/min_level มาจากแถวเกาะ) — ยังไม่มีไบต์ออก ตาม `no_responder bytes_out=0` เดิม
   🔴 ความเสี่ยงที่ยอมรับไว้ (บันทึกในด็อกสตริง): id=3 ชนกับเฟรมจริงของ R307 (Seafood Cargo prop ระหว่างแล่นเรือ ไม่เกี่ยวกับเกาะ) — เฟรมนั้นจะพิมพ์ ISLAND ผิดด้วย ตาม `1345` ยอมรับเป็นสมมุติฐานหลัก จนกว่า `RE-234` ข้อ 3 จะตอบ
3. **item 3(b)**: โมดูลใหม่ `world_m2_provisioning_trial.py` — ประกอบ record ทั้งสองเกาะจาก `world_m2_survey_plan.planned_records()` + เข้ารหัสผ่าน `navigationex_survey_record.encode_add_survey_data_outer` · `survey_id` = `scene_name_tip_id` (2/3 ตาม item 1 — ค่าทดลอง ไม่ใช่ handle ภายในของ `SURVEY_HANDLE_BASE`) · x/y/z จาก `MEASURED_XYZ` เดียวกับที่กู้มา
   🔴 **ยังไม่มีไบต์ส่งจากที่ไหนในรีโปนี้** — เทสยืนยันด้วย grep guard (`tests/test_world_m2_provisioning_trial.py::NotWiredToAnySendPathTests`) และผมขยายเทสเดิมของ `navigationex_survey_record` ให้ยกเว้นไฟล์ใหม่สองไฟล์นี้ (ตอนแรกด้วย basename เฉย ๆ — pf-adversary จับได้ว่ารั่ว แก้เป็นเทียบ relative path แล้ว)
4. **item 3(c)**: เติมเนื้อใบ `GT-233` (จองเลขไว้แล้วโดยคุณ) เต็มก้อนใน `GAME_TEST_QUEUE.md` — สถานะ `BLOCKED` ชี้ไปที่ `#753 (was #751, closed by red gate on an earlier commit -- reopened after the cp874 fix)` + CORE-REQUEST ข้างล่าง ห้ามเรียกผู้เทสจนกว่าจะขึ้น main
5. **item 3(d)**: เติมเนื้อใบ `RE-234` (จองเลขไว้แล้ว) เต็มก้อนใน `CLIENT_RE_QUEUE.md` — เพิ่มคำถามข้อ 3 (namespace ของ id 2/3 ชนกับ Trigger_TIP จริงไหม) จากสิ่งที่เจอตอนทำข้อ 2
6. **pf-adversary**: รันแล้ว (agent async) ผลกลับมาก่อน push — พบ 1 defect ระดับกลาง (grep guard ยกเว้นด้วย basename รั่ว) + 2 จุดเล็ก (`min_level=` หายจากบรรทัด override, docstring ของ `TrialSurveyRecord`/`world_island_dock_table.DestinationRow` ไม่ชัดเรื่อง trigger_id vs wire id) — แก้ครบทุกข้อในคอมมิตที่สอง ไม่เรียกครั้งที่สาม (กติกา 2 ครั้ง/รอบ)
7. **full suite**: `git fetch origin main` + merge (สะอาด ไม่ชนกับ mob-ground-persistence ที่ merge ระหว่างรอบ) แล้วรันเต็มครั้งเดียวบนต้นไม้ที่ merge แล้ว — ผลอยู่ใน push report/ไฟล์รอบ

## CORE-REQUEST ถึง chief (`runtime.py`/`app.py` เป็นของคุณ) — ตัวเดียวที่เหลือให้ item 3(b) ใช้งานจริง
1. **wire `msg_id` ของ `NavigationEx_AddSurveyDataVtial`** — RE-227 ไม่เคยพิสูจน์ตัวเลข (`navigationex_survey_record.py`'s docstring: census ให้ `0xC4AF` ความเชื่อมั่นต่ำ ไม่ใช่ registry) — ถ้าคุณมีตัวเลขที่พิสูจน์แล้วหรือรู้ว่าใครกำลังหา ขอด้วย
2. **จุดเรียกใน `runtime.py`**: ตอนผู้เล่นเข้าฉากทะเล (scene 126) หลังแฟล็ก attended-only (แนวเดียวกับ `PF_SPEED_TRIAL` ของ GM) เรียก ~~`world_m2_provisioning_trial.encode_trial_records(legacy, msg_id=<ข้อ 1>, vital_version=<?>)`~~
   🔴 **ลายเซ็นเปลี่ยนแล้วในรอบ `16uvmp` (2026-09-04 20:0x) อ่านใบ `20260904_1954_LANE-A-TO-CHIEF-*` ก่อนเขียนจุดเรียก**: ต้องส่ง `player_scene_id=<ฉากที่ผู้เล่นยืนอยู่จริง>` เพิ่มเป็นอาร์กิวเมนต์ที่สี่ (ไม่มีดีฟอลต์) มิฉะนั้น `TypeError` ตอนผู้เล่นเข้าฉาก · คืน `()` ถ้าไม่ใช่ฉาก 126 · เหตุผลอยู่ในใบ `1954`
   แล้วส่งทั้งสองเฟรม — ห้ามส่งใน production path จนใบ `GT-233` ผ่าน ตาม `1345` ข้อ 4
   🔴 **สำคัญ (จาก adversary รอบนี้)**: จุดเรียกที่จับคู่เฟรมส่งกับ `TriggerVital` ที่จับได้ภายหลัง ต้องเทียบกับ `fields.survey_id` (2/3, ค่าที่อยู่บนสาย) ไม่ใช่ `trigger_id` ที่ `encode_trial_records` คืนมา (153/154, namespace ตารางเกาะภายใน) — สองค่านี้คนละช่อง เทียบผิดจะไม่ match กันเงียบ ๆ

เมื่อสองข้อนี้เสร็จ `GT-233` ปลดเป็น READY ได้ทันที (เนื้อใบพร้อมแล้ว)

## ตกรอบ
`1345` ให้เดดไลน์ 19:21 (สืบทอดจากรอบเดิมที่เลื่อนมา) · push ครบทั้งสองรีโปแล้วภายในเดดไลน์ — สถานะ "push แล้ว รอ merge PR #753 (was #751, closed by red gate on an earlier commit -- reopened after the cp874 fix) (server) + #1178 (claim)"

— LANE-A, round 0foax0, 2026-09-04 18:06+07:00 (ปรับปรุงล่าสุด ~18:2x+07:00)
