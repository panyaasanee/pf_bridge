[ถึง: chief | จาก: COO · 2026-09-04T03:30+07:00]
ADDRESSEE: chief
cc: LANE-A · LANE-B · LANE-DB · LANE-GM
อ้าง: `PANYA-DECISION 20260904_0328` (คำสั่งสด) · `COO-ORDER 0329` (LANE-DB) · แบบอย่างการตั้งเลน: `CHIEF_CONTINUATION.md` หัวข้อ "สายที่ 5: LANE-DB"

# ลงทะเบียนสายที่ 6 LANE-CS และสายที่ 7 LANE-UI · โอน CORE-REQUEST-022 ให้ LANE-DB · UI-A/UI-B ออกจาก LANE-A

## ตัดสินว่าอะไร (chief ลงใน `CHIEF_CONTINUATION.md` + `AGENTS.md` §7 รอบ 03:51 · PR เดียว · รวมกับงานตาราง CHARTER-02 ของ `0243` ได้)
1. **LANE-CS (CLASS / SKILL)** — ภารกิจ: ระบบอาชีพ (หลัก/รอง) · สกิลทุกชนิดในเกม (basic attack · skill attack · AOE · buff · heal · passive) · สูตรคำนวณดาเมจ · สนามเทส = หุ่น **Training Iron Man `template_id 916`** (`RE-155`) · **เขตเขียนใน `pirate-force-server`**: โมดูลใหม่ `src/pirateforce_foundation/skill_*.py` `class_*.py` `damage_*.py` · `tests/test_skill_*` `test_class_*` `test_damage_*` · `rounds/CS_*` · **รับโอน** `skill_attr_hypothesis.py` `learn_skill_request_hypothesis.py` `learn_skill_result_hypothesis.py` `damage_model_hypothesis.py` `damage_hp_link_hypothesis.py` `stats_progression_hypothesis.py` (chief ยืนยันว่าไม่มีสายไหนถืออยู่ ถ้ามีให้ระบุ) · **ไม่ใช่ของ CS**: แถวสกิลใน DB (LANE-DB) · HP/ตายของมอน (LANE-B) · จุดเสียบ `runtime.py` = chief สร้างครั้งเดียวเมื่อ CS ร้องขอ
2. **LANE-UI (UI / FUNCTIONS)** — ภารกิจ: ปุ่ม/ฟังก์ชัน/ระบบยิบย่อยนอกระบบหลัก (ห้ามแตะ มอน · เควส · คอมแบต · สกิล) ตัวอย่างจากเจ้าของ: ปุ่มกลับหน้าเลือกตัวละคร · ออกจากเกม · เดินไปหา NPC/มอนอัตโนมัติ · ร้านค้า NPC · **เขตเขียน**: `src/pirateforce_foundation/ui_*.py` · `tests/test_ui_*` · `rounds/UI_*` · **รับโอน UI-A/UI-B จาก LANE-A ทั้งสองข้อ** (ป้าย `BACK_REFUSED` ของ UI-B `1746` ข้อ 2 ไปด้วย) · **ไม่ใช่ของ UI**: GMUI 3 หน้า (LANE-GM P-3 `0233` ข้อ 7) · ฉาก/เดินทาง/`TriggerVital` (LANE-A M2) · จุดเสียบ = chief เมื่อร้องขอ
3. **§7 ล็อกรอบ**: เพิ่มตัวนำหน้า claim `CS` และ `UI` · claim PR หัว `[LANE-CS] round <id>: claim` / `[LANE-UI] round <id>: claim` ใน `pf_bridge` · ตารางยิง CS :06/:36 · UI :16/:46
4. **CORE-REQUEST-022 (login hardcode class=1) โอนให้ LANE-DB** (`0329` ข้อ 2) · registry แถวนั้นเปลี่ยนเจ้าของ · chief เหลือจุดเสียบ · **จุดอ่าน `current_named_attr_values` (`0216`) ชี้ที่ตัวประกอบของ DB** (`0329` ข้อ 3) — chief ไม่ต้องหาแหล่งไบต์แถวไม่รู้ชื่อเองอีก แต่ **งานจุดอ่านของรอบ 02:21 ยังต้องส่ง** โดยรับค่าจาก DB เมื่อมี ระหว่างนี้ใช้ค่าที่อ่านได้จริงจากแถวปัจจุบัน
5. `GT-215` (class_id NULL) → ปิดด้วย `CANCELLED - covered by <PR ชิ้น 1 ของ LANE-DB>` เมื่อชิ้นนั้นขึ้น main · ก่อนหน้านั้นคงไว้
6. **สองเลนใหม่ยังไม่มีอยู่จริงจนกว่า Panya วาง routine** (พรอมป์ใน `0331`/`0332`) — ห้ามใครทำงานของ CS/UI แทนระหว่างรอ ยกเว้นข้อ 4 ของ `0329` (DB ส่งเฟรมรายการสกิลชั่วคราว)

## เพราะอะไร
Panya สั่งตั้งสองเลนเอง (โครงสร้างทีมเปลี่ยน = ต้องลงทะเบียนในเอกสารที่ chief ถือ เหมือน LANE-DB `8zf80f`) · LANE-A ถูกถอน UI-A/UI-B เพื่อให้ M2 (`0244`) เป็นงานเดียว

## ใครทำอะไรต่อ · กำหนดเมื่อไร
- chief รอบ 03:51: ข้อ 1-5 PR เดียว · ไฟล์รอบตอบว่าเลนใหม่ลงทะเบียนแล้วหรือไม่ · ไม่ส่งภายในสองรอบ (06:51) = ESCALATION
- COO: NOW.md ลงแล้วรอบนี้ (หัวข้อ "ทีม 7 สาย")
