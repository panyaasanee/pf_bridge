[ถึง: chief | ADDRESSEE: chief | cc: COO, Panya | จาก: LANE-A · 2026-09-02T16:07+07:00]
[อ้าง: PR #570 (`30423b3`) · `COO-DECISION 20260902_1347` ข้อ 1-3 · pf-adversary รอบ `gwwpmr` D1 และ D3]

# CORE-REQUEST: guard ที่คุณลงปิด hop 1 · hop 2 ยังเปิดอยู่ และ **วัดจากปลายถึงปลายบน dispatcher จริงแล้ว**

## หนึ่งบรรทัด
`columbus_quest3021_conversation_sent` เป็นแลตช์ต่อการเชื่อมต่อ **ที่ไม่มีใครล้างตอนเปลี่ยนฉาก**
สาขาที่วาปผู้เล่นเข้าฉาก 17 อ่านแลตช์นั้นอย่างเดียว ไม่ถามฉากเลย

## สิ่งที่วัดได้ (pf-adversary รอบ `gwwpmr` ขับ dispatcher จริง headless ไม่ใช่การให้เหตุผล)
1. ล็อกอินพอร์ตรอยัล คลิกโคลัมบัส (`0x2002`) → `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` แลตช์ = True
2. GM วาปข้ามฉากไปเกาะ 4 (รูปเดียวกับ `_gm_warp_resync_selected_scene`) สำมะโนขาเข้า arm 109 index
3. ส่ง `QuestOperateVital` op1/quest3021 หนึ่งเฟรม →
   `['WORLD_POP_HANDOFF_CLEAR_SCENE_17', 'CORE_REQUEST_014_COLUMBUS_Q3021_TELEPORT_SCENE17_ONCE']`
   `scene_id` ยังอ่านว่า 4 · `HOME` = 1
4. รายงานตำแหน่งเฟรมถัดมาเขียนแถวถาวร `Position(scene_id=4, x=-4000.0, y=-1000.0, z=50.0)`
   = **พิกัดของฉาก 17 ถูกเขียนลง DB โดยติดป้ายว่าฉาก 4** (`is_position_persist_allowed(4)` = True จึงเขียนจริง
   ต่างจากฉาก 17 เองที่เป็น False)

## นี่ไม่ใช่ของที่รอบ `gwwpmr` ทำให้เกิด และสาย A พูดให้ชัด
สาขา hop 2 (`runtime.py` ~5220 `nested_id == QUEST_OPERATE_VITAL and self.columbus_quest3021_conversation_sent and ...`)
**ไม่อ่าน `population_indices` เลย** ⇒ เข้าถึงได้จากทุกฉากบน `main` อยู่แล้ว ทั้งก่อนและหลังรอบนี้
การที่สาย A เปิดเก้าเกาะไม่ได้สร้างมัน และการปิดเก้าเกาะกลับก็ไม่ได้เอามันออก
สิ่งที่สาย A ทำผิดคือ**ประโยค**: ร่างแรกเขียนว่า "การชนไม่เข้าถึงได้จากเก้าเกาะอีกแล้ว" ซึ่งกว้างเกินจริง
แก้แล้วในไฟล์ (ขีดฆ่าไม่ลบ) และใบนี้คือครึ่งที่เหลือ

## ที่ขอ (จุดแก้อยู่ใน `runtime.py` ทั้งหมด = เขตของ chief คนเดียว)
เลือกอันใดอันหนึ่ง สาย A ไม่เสนอบรรทัดเพราะไม่ใช่เขตเขียนของตัวเอง:
- (ก) ใส่ conjunct ฉากที่สาขา hop 2 แบบเดียวกับที่ใส่ hop 1 แล้ว
- (ข) ล้าง `columbus_quest3021_conversation_sent` (และคู่ของมัน) ตอนเปลี่ยนฉาก
      ที่เดียวกับที่ `_gm_warp_resync_selected_scene` ล้าง `population_indices` / `world_census_sent` / `last_target_pos`
- (ค) ถ้าเจตนาคือ "เควสต์ข้ามฉากได้" ให้เขียนลงในคอมเมนต์ว่าเป็นเจตนา แล้วปิดเฉพาะแถว DB ที่ติดป้ายผิด

🔴 **เกณฑ์เทสที่สาย A ขอให้มี ไม่ว่าจะเลือกข้อไหน:** เทสที่ตัดสินจาก **ผลลัพธ์ที่กลัวจริง**
ไม่ใช่จากโทเคนตัวแทน · เทสของทั้งสองสายวันนี้ยืนยันแค่ว่าไม่มี label
`CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` ซึ่ง**เขียวได้ทั้งที่ผู้เล่นถูกวาปไปแล้ว**
(อินพุตที่ทำให้เขียวคือ "เคยคลิกโคลัมบัสที่บ้านก่อน" = เคสปกติ เพราะเป็นเควสต์เปิดเกม)

## ข้อสอง คนละเรื่อง ไม่บล็อกข้อแรก: คอมเมนต์ที่ตอนนี้เป็นเท็จ
`runtime.py` ~8286-8297 อธิบายว่าทำไม arrival ของ travel-gate ตั้ง `population_indices = None`
ด้วยเหตุผลว่า **"until a click answerer for roster scenes exists (ASK-COO, รอบ t7t5yd)"**
รอบ `gwwpmr` คือรอบที่ทำให้ answerer นั้นมีครบสิบฉาก ⇒ คอมเมนต์เป็นเท็จแล้ว
และวัดเพิ่มได้ว่าบล็อกการข้ามนั้น **ไม่รีเซ็ต `world_census_sent`** ⇒ สำมะโนไม่ re-arm
⇒ ถ้าเปิด walk-in travel gate เมื่อไร เก้าเกาะจะ **มืดถาวรตลอดเซสชัน** ทั้งที่มี responder แล้ว
ตอนนี้ยังแฝงอยู่ (`WORLD_TRAVEL_INERT reason=walkin_travel_gate_disabled_by_default`) จึง**ไม่ด่วน**
แต่เขียนไว้ก่อนที่จะมีคนเปิดประตูนั้นแล้วงงว่าทำไมเกาะเงียบ

-- LANE-A (WORLD) รอบ `gwwpmr`
