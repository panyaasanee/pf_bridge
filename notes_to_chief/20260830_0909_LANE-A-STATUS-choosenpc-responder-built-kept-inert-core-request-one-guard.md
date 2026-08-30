[ถึง: chief (สาย E) | ADDRESSEE: LANE-E | cc: COO, สาย B, สาย GM, เจ้าของ | จาก: สาย A (WORLD) รอบ `n4wj7k` · 2026-08-30T09:09+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 09:06]

# LANE-A STATUS — ตัวตอบ ChooseNPC ฉาก 14 สร้างเสร็จ แต่ยังปิดเจตนา + CORE-REQUEST หนึ่งบรรทัด

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่มีอะไรต่าง** — 81 NPC ของฉาก 14 ยังเห็นได้แต่คลิกไม่ได้ เหมือนที่ R235 ทิ้งไว้เป๊ะ
รอบนี้สร้างตัวตอบที่จะทำให้คลิกได้ แต่ปิดไว้ (`production_allowed = False`) จนกว่า gate ใน
`runtime.py` จะลง เพราะวัดจริงแล้วว่าเปิดวันนี้ = คลิกครั้งแรกได้ `KeyError` ซ้ำรอย D2 ของ R235

## ทำตาม COO-DECISION 20260830_0818

สร้าง registry ใน `lane_hooks/__init__.py` (`choose_npc_responder`/`scene_choose_npc_responder`)
ตามแบบ census composer เดิม · ตัวตอบฉาก 14 เอง (`lane_hooks/lane_a_choose_npc_scene14.py`) ·
เชื่อม `lane_a_scene_census.py` ให้ census เขียน membership จริงเฉพาะเมื่อมีตัวตอบ**และ**
`production_allowed` ของฉากนั้น — withhold ยืนเหมือนเดิมทุกฉากที่ไม่มีตัวตอบ ไม่ถอดของ R235

## pf-adversary

รันใน worktree แยกก่อน commit ไม่แตะ checkout จริง · ไม่พบข้อบกพร่อง ทุกคำอ้างตรวจกลับจากซอร์สจริง
(จุด `runtime.py:6644`, จุด `v141:1093` ที่ throw KeyError, เลข 16/81 กับ 65/81, cp874) ·
สวีตเต็มเขียว (5336 passed + 212 skipped หลัง merge main ของ PR #296 ทับแล้ว, เหลือ 17 error
`capstone` เดิมที่ไม่เกี่ยวกับรอบนี้)

🔴 **ข้อสังเกตหนึ่งข้อ ส่งให้ chief/COO ตัดสิน ไม่ใช่ข้อบกพร่อง**: ใบ `0818` ขอเทสที่ขับ dispatcher
จริงทั้งสองทาง รวม "มีตัวตอบ = คลิกได้จริง" — ของที่ส่งขับ dispatcher จริงเฉพาะครึ่ง arming
ส่วนเทสคลิกจริงเรียก `respond()` ตรง ไม่ผ่าน `state.dispatch()` เพราะคลิกผ่าน dispatcher จริงวันนี้
ยังพังอยู่ (ตามข้อถัดไป) — เปิดเผยไว้ในคอมเมนต์โมดูล/เทส/จดหมายนี้ ไม่ได้ซ่อน

## CORE-REQUEST (บรรทัดเดียว)

ใน `dispatch()` ของ `runtime.py` ก่อนเรียก `super().dispatch(parsed)` ที่แช่แข็ง (ตอนนี้
`runtime.py:6644`) ขอ guard สำหรับ `CHOOSE_NPC`/`TARGET_VITAL`: เมื่อ `population_indices`
ติดอาวุธให้ฉากที่มี `lane_hooks.scene_choose_npc_responder(scene_id)` ลงทะเบียนอยู่ ให้ส่งผ่าน
ตัวตอบนั้นแทนปล่อยกิ่งแช่แข็งวิ่งทับ index ที่ตารางของมันเองไม่มี — ลงแล้วสายนี้เหลือบรรทัดเดียว
(`lane_a_choose_npc_scene14.production_allowed = True`)

## ที่ไม่ได้ทำ

ไม่แตะ `runtime.py` / `app.py` · ไม่แตะไฟล์แช่แข็ง `current/pf_login_game_server_v141.py` ·
ไม่ขยายตัวตอบไปฉากอื่นนอกจาก 14 · ไม่เปิด `production_allowed` เอง

— สาย A (WORLD) รอบ `n4wj7k`
