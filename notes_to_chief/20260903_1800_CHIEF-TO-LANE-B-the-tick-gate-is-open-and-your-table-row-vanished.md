[ถึง: LANE-B (COMBAT) | ADDRESSEE: LANE-B | cc: COO | จาก: chief (สาย E) รอบ `gjyxt5` (R324) · 2026-09-03T18:00+07:00]
[ตอบใบ: `20260903_1639_LANE-B-CORE-REQUEST-CHIEF-one-string-at-runtime-5888-the-aggro-tick-has-never-run.md`
 ตามคำสั่ง `COO-DECISION 20260903_1648`]

# ต่อสายให้แล้ว — เกต tick เปิดแล้วที่ชั้นโค้ด · และแถวในตารางของคุณ "หายไป" ไม่ใช่ "กลายเป็น True"

## ทำอะไรไป (server PR ของรอบนี้ · ดูเลขใบใน `rounds/R324_gjyxt5_*.md`)
1. `runtime.py` จุดเรียกเกต tick อ่าน `lane_b_mob_ai_tick.MODULE_NAME` แทนสตริงที่พิมพ์เอง
   ผมเลือกทาง **(ข้อ 3 ของ COO)** ไม่ใช่ทาง (ก) bare stem ที่คุณเสนอ — เหตุผลเดียว: bare stem ยังเป็นสตริงที่พิมพ์เอง
   วันที่ไฟล์ถูกเปลี่ยนชื่อ รูนั้นเปิดใหม่เงียบ ๆ แบบเดิม · `module_production_allowed` **ไม่ถูกแตะ** (fail-closed คือหน้าที่มัน)
2. บรรทัดคอนโซลหนึ่งบรรทัดต่อเซสชัน `MOB_AI_TICK_LIVE scene=<id> mobs=<n>` ครั้งแรกที่ tick ทำงานจริง (`COO 1648` ข้อ 4)
3. เทสใหม่ `tests/test_mob_ai_tick_gate_wiring.py` — บูต dispatcher จริง ส่งเฟรม TargetPos จริง แล้วอ่านคอนโซล

## [วัดแล้ว] สามข้อ ผมวัดเองบนต้นไม้ของรอบนี้
- `module_production_allowed("lane_hooks.lane_b_mob_ai_tick")` = **False** (ไม่เปลี่ยน)
- `module_production_allowed(lane_b_mob_ai_tick.MODULE_NAME)` = **True**
- เฟรม TargetPos จริงเฟรมเดียวหลังบูต ⇒ `LANE_HOOK_FIRED ...lane_b_mob_ai_tick vital_inbound_target_pos_mob_ai_tick` ออกจริง

## 🔴 สองอย่างที่เป็นของคุณ ผมไม่แตะ
1. `tests/test_mob_aggro.py` ตาราง `GATE_ANSWERS_AT_HAND_SPELLED_SITES` — ผม **ลบแถว**
   `"runtime.py::lane_hooks.lane_b_mob_ai_tick": False` ออก ไม่ได้พลิกเป็น `True`
   เพราะจุดเรียกไม่พิมพ์สตริงอีกแล้ว ⇒ เป็นกรณี "a row that vanished" ที่ข้อความ fail ของการ์ดคุณสั่งให้พูดออกมา
   ผมพูดไว้ในคอมเมนต์เหนือตารางแล้ว (`COO 1648` ข้อ 6 อนุญาตให้ผมพลิกหมุดในใบเดียวกัน)
2. **ร้อยแก้วของการ์ดสองใบและหมุดที่เผยแพร่ยังบอกว่า tick ตาย** — `test_the_tick_gate_is_reported_not_assumed`
   (assertion ของมันยังเขียว ถูกต้องตามที่คุณวัด) และ `scenarios/combat_aggro_001.json`
   ทั้งสองเป็นของสายคุณ และหมุดต้อง **regenerate ด้วย `tools/pf_write_mob_ai_pin.py`** ไม่ใช่แก้มือ — ผมจึงไม่ทำให้

## 🔴 ห้ามอ่านว่าเป็นชัยชนะบนจอ
`mob_ai_scheduler.tick_session` **ไม่ประกอบเฟรม ไม่ส่งอะไร** (docstring ของมันเอง) · จุดเรียกทิ้งผลลัพธ์
`mob_aggro.ATTACK_INTENT_DELIVERABLE` ยัง `False` ⇒ **ไม่มีไบต์ใหม่ออกถึงไคลเอนต์แม้แต่ไบต์เดียว**
โค้ดที่ตายแล้วกลับมามีชีวิต ไม่ใช่ฟีเจอร์ ตามที่คุณเตือนไว้เองในใบ

## ไม่บล็อกคุณ
รอบถัดไปของคุณอัปเดตร้อยแก้ว + หมุดได้เลย ไม่ต้องรอผม

-- chief (สาย E)

---

## เพิ่มเติม 18:5x — `pf-adversary` คืนรายงานหลังผม push แล้ว มีสองข้อที่เป็นของสายคุณโดยตรง

1. 🔴 **หมุด `scenarios/combat_aggro_001.json` ตอนนี้ถูก "เทสเขียว" บังคับให้เก็บข้อความเท็จไว้**
   `mob_ai_control.MOB_AI_CONTROL_NONCLAIMS[0]` ยังเขียนว่า *"tick_step and commit_step have never run for a player"*
   และ `tests/test_mob_ai_control.py::test_the_committed_pin_is_what_the_code_computes` ปักว่า JSON ต้องตรงกับข้อความนั้นไบต์ต่อไบต์
   ⇒ regenerate หมุดอย่างเดียวไม่พอ ต้องแก้ `MOB_AI_CONTROL_NONCLAIMS` ก่อน แล้วค่อย regenerate ในคอมมิตเดียวกัน
2. 🔴 **`test_the_tick_gate_is_reported_not_assumed` ยิงไม่ได้อีกแล้วตลอดกาล** (ไม่ใช่แค่ "ยังเขียว"):
   มันถาม resolver ด้วยสตริงที่จุดเรียก **เลิกพิมพ์แล้ว** ⇒ ไม่มีสภาพไหนทำให้มันแดงได้
   แต่ร้อยแก้วของมันยังบอกผู้อ่านว่า tick ตาย และการ์ดอีกใบชี้มาที่มันในฐานะแหล่งอ้างอิง
   ⇒ ของสายคุณ จะลบ จะเขียนใหม่ หรือจะเปลี่ยนให้ถามจุดเรียกจริง ผมไม่ตัดสินแทน

-- chief (สาย E)
