ADDRESSEE: COO (บันทึกคำสั่งสด · COO เขียนแทน) · cc chief · LANE-DB · LANE-A · LANE-B · LANE-GM

# PANYA-DECISION: LANE-DB ถืองานชั่วคราว "PLAYER / CHARACTER" ทำให้สำเร็จ · ตั้งเลนใหม่ 2 เลน: Class/Skill และ UI/Functions

- when: 2026-09-04 ~03:2x+07:00 · channel: Panya พิมพ์สดในเซสชัน COO (หลังอ่านรายงานรอบ 02:41) · ถ้อยคำในเครื่องหมายคำพูดคือของเธอ
- ต่อยอด `PANYA-DECISION 20260904_0233` (ไมล์สโตนเปิด) · **แทนที่** `COO-DECISION 20260904_0243` ข้อ 3 ("ตัวละคร" ไม่เปิดเลนใหม่ / แบ่ง DB-chief) ทั้งข้อ

## 1. LANE-DB ถืองานชั่วคราว PLAYER / CHARACTER — ก่อนอย่างอื่น
Panya: "ทุกอย่างบน HUD ของตัวละครตอนนี้เป็นค่าคงตัว: อาชีพที่เลือกถูกทิ้ง (class_id NULL → Gladiator ตายตัว), MP/CP/cash/stat NULL, HP 100 จาก DEFAULT, EXP ไม่มี, skill window ว่าง ไม่มีแม้แต่ basic attack skill, /speed ฆ่าตัวเพราะทรงเฟรม UpdateAttrVital ผิด · chief ทำเป็น CORE-REQUEST ทีละจุด (022 hardcode class=1) เพราะไม่มีเจ้าของ · เลนนี้ถือ: แกะ CreateActorVital ลง DB · ค่าเกิดจากตาราง class (CHARCREATE_CLASS/STANDARD_STATUS) · UpdateAttrVital ทรงถูก · level/EXP/skill point/STR CON DEX INT PER/ช่องนามแฝง(นามปากกา) ที่หน้าสร้างตัวละครให้ใส่ค่า มาลง DB / ค่ารหัสผ่านรอง ที่ใช้เปิดกระเป๋า MD5 แล้วมาลง DB / ค่าอื่นๆ ที่สมควรนำมาเก็บ · ทำให้ 'ตัวละคร' เป็นของจริงก่อน ไม่งั้นทุกใบตีมอน/เก็บของ/เควสต์วัดบนตัวปลอม"
⇒ ใบสั่ง `COO-ORDER 20260904_0329` (ADDRESSEE: LANE-DB)

## 2. เลนใหม่ที่ 6: LANE-CS (CLASS / SKILL)
Panya: "Lane Class\Skill เพื่อโค้ดดิ้งระบบอาชีพ คลาส อาชีพหลัก/อาชีพรอง สกิลทั้งหมดในเกม ไม่ว่าจะเป็น Basic attack, Skill attack, AOE, buff, heal, passive ทุกอัน หาและดูแลเรื่องสูตรคำนวนดาเมจ เอาไว้เทสกับมอนหุ่น Training Iron Man"

## 3. เลนใหม่ที่ 7: LANE-UI (UI / FUNCTIONS)
Panya: "Lane UI\Functions ยิบย่อยในเกม ทำมาเพื่อไล่เคลียปุ่ม / functions และทุกระบบยิบย่อยต่างๆ ในเกมนอกเหนือออกจากระบบหลัก (พวกมอน เควส คอมแบต สกิล ไม่เกี่ยว) ปุ่มกลับหน้าเลือกตัวละคร/ออกจากเกม ระบบเดินทางไปหา npc, monster อัตโนมัติ npc's shop คือตัวอย่าง เพื่อให้เกมโดยรวมสมบูรณ์ขึ้น ทำงานทุก 90 นาทีเหมือนกับ Lane อื่น"

## กลไก (COO ตัดสินภายใต้อำนาจ CHARTER-01 · Panya สั่ง "แปลเจตนา พัฒนาเป็นคำสั่ง แล้วทำ")
- ชื่อป้าย: `LANE-CS` (claim `[LANE-CS] round <id>: claim` · `rounds/CS_*`) และ `LANE-UI` (claim `[LANE-UI] round <id>: claim` · `rounds/UI_*`)
- ตารางยิง 90 นาที (สอง routine สลับ): **LANE-CS :06/:36 · LANE-UI :16/:46** (ช่องว่างที่ไม่ชนสายเดิม DB :01/:31 · GM :11/:41 · A :21/:51 · B :31/:01 · chief :51/:21 · COO :41 ทุกชั่วโมง)
- พรอมป์ของสองเลน = `notes_to_chief/20260904_0331_LANE-PROMPT-LANE-CS.md` และ `20260904_0332_LANE-PROMPT-LANE-UI.md` — **Panya วาง routine เอง** (COO ไม่มีสิทธิ์ตั้ง routine ของบัญชีเธอ) · จนกว่าจะวาง สองเลนยังไม่มีอยู่จริง งานที่จ่าหน้าให้สองเลนนี้จะรอ ไม่มีใครทำแทน
- ลงทะเบียนเขตเขียน/§7 = chief (`COO-DECISION 20260904_0330`) · CHARTER-02 ตารางเลน: 5 → 7 สาย
- UI-A/UI-B ย้ายจาก LANE-A → LANE-UI · GMUI (P-3) ยังเป็น LANE-GM ตาม `0233` ข้อ 7 · ปุ่มใน GMUI ไม่ใช่ของ LANE-UI

## nonclaims
COO ไม่ได้แตะไฟล์ใดนอก `NOW.md` และ `notes_to_chief/` · ไม่ได้ตั้ง routine · ไม่ได้แก้พรอมป์ของสายเดิม
