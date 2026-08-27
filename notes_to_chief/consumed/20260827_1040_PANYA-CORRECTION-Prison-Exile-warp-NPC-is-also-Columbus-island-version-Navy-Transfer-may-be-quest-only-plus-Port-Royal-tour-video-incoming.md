[ถึง: สาย A · chief · RE runner · cc COO · สาย B | จาก: Panya (เจ้าของ) ผ่านเซสชัน attended กะ1 — คำแย้ง 10:3x (+07:00) | เขียน 10:40 (+07:00) | แก้ 1020 ①]

# PANYA-CORRECTION — NPC ประตูวาร์ปออกจากเกาะคุกไปแมพทะเลก็คือ **Columbus (เวอร์ชันของเกาะนั้น)** ไม่ใช่ Navy Transfer · Navy Transfer อาจเป็นแค่ NPC เควสหรือไม่ทำอะไรเลย

คำเจ้าของ (คำต่อคำ 10:3x): *"เกาะคุก npc ที่ทำหน้าที่เป็นประตูวาปออกจากเกาะไปแมพทะเล ก็เป็น Columbus (ในเวอร์ชั่นของเกาะนั้น) ตัว Navy Transfer อาจไม่ได้เกี่ยวข้องกับการวาปอาจเป็นแค่เควส หรือไม่ได้ทำอะไรเลย"*

## ผลต่อสิ่งที่เขียนไปแล้ว

1. **ถอน** ข้อสังเกตใน 1020 ① ที่ว่า *"Navy Transfer 1 คือ NPC ท่าเรือของเกาะคุก (บทบาทเดียวกับ Columbus ในเมือง)"* — ภาพ `REF_ORIGINAL_SERVER_PrisonExile_NavyTransfer_at_dock_gate` แสดงแค่ว่า Navy Transfer **ยืน**อยู่ที่ประตูท่า ไม่ได้แสดงว่าเป็นตัววาร์ป · บทบาทวาร์ปของทุกเกาะ = Columbus ตัวของเกาะนั้น (ตรงกับตาราง MOBS ที่มี Columbus "Marine Transport Station" คนละ n_ID ต่อเกาะ: 36 · 67 · 105 · 156 · 196 … และตรงกับ `RE-095` ที่ Columbus 36 ผูก quest 3023)
2. **สาย A / travel (M2):** ตัว transfer ของแต่ละฉากที่ต้องต่อสายคือ Columbus ของฉากนั้น — Port Royal = 156 · Prison Exile = ต้องหาว่า Columbus ตัวไหนของบล็อก 1–35 (ในบล็อกนั้นไม่มี "Columbus" — มี 36 ต้นบล็อกถัดไป ⇒ สมมติฐาน: Columbus 36 อาจเป็นของ Prison Exile ไม่ใช่ Spice ⇒ **ขอบบล็อกที่ผมเสนอใน 0500 §③(ข) อาจเลื่อนไปหนึ่งคู่** ให้ตรวจด้วย `s_QUEST_BEGIN` ของ Columbus 36 (quest 3023 → `QUEST.n_SCENE`) ก่อนใช้) · Navy Transfer 1 ห้ามถูกใช้เป็นจุดวาร์ปในโค้ดใด ๆ
3. **สาย B:** ไม่กระทบ

## ของที่กำลังจะมา

เจ้าของให้คลิป YouTube **"[Pirate Force]#2 tutorial ที่อยู่NPCในเมือง"** (PoppyZaa Channel · `vAD8TuO3ApA`) = พาชม Port Royal ทั้งเมืองพร้อมเสียงบรรยายหน้าที่ของ NPC แต่ละตัว — เซสชัน attended จะแกะเป็นหลักฐาน (เฟรมป้ายชื่อ + minimap + คำบรรยายต่อ NPC) ผ่านท่อเดิมใน `decoded external videos/` (คลิป #1 = `ItQQqKIQSLU`) ทันทีที่ไฟล์ลง `source/` · **สาย A ไม่ต้องรอ**: roster/transform ตาม 0915 ③ ทำต่อได้ ส่วนตาราง index→n_ID จะได้แถวจากคลิปนี้เพิ่มทีหลัง

— Panya (ผ่านเซสชัน attended กะ1)
