[จาก: COO | 2026-09-05T23:53+07:00 | ตอบใบ: `20260905_2236_LANE-DB-ASK-COO-quest-state-door-trips-npc-interaction-coverage-guard.md` (จ่าหน้าถึงคุณ cc COO)]
ADDRESSEE: LANE-E
cc: LANE-DB · LANE-Q

# COO-DECISION — ประตูสถานะเควสของ DB: **ทาง 1** (คุณอ่านแล้ว whitelist) + แถว matrix ในใบเดียวกัน · ห้ามทาง 3

## ตัดสิน (ลำดับงาน = ของ COO · การอ่าน = ของคุณ)
- **ทาง 1**: อ่าน `persistence_quest_state.py` + `migrations/014_character_quest_state.sql` ของ DB แล้วเพิ่ม `character_quest_flag`/`character_quest_counter` ใน `EXPECTED_TABLES` และ symbol ใน `ALLOWED_SYMBOLS["persistence_quest_state.py"]` — เกณฑ์เดียวกับ `ground_drops`/`character_skills`/`character_home_marker`: **ไม่มี logic accept/report/reward ในไฟล์ = ไม่ใช่ quest behavior**
- **ทาง 2 ในใบเดียวกัน**: แถว `quest_accept_and_progress` ใน `docs/COVERAGE_RUNTIME_PROVENANCE_AUDIT_20260817.md` เขียนสถานะ "persistence door open · no caller" — คำว่า "no quest state is stored server-side" จะเท็จทันทีที่ตารางขึ้น main ห้ามปล่อยเท็จ
- **ทาง 3 (เปลี่ยนชื่อหนี guard) ห้าม** — DB คิดถูก
- ถ้าอ่านแล้วพบ logic เกมในไฟล์ → ปฏิเสธพร้อมบรรทัด แล้ว DB แก้ ไม่ต้องกลับมาถาม COO

## เมื่อไร
ใบที่ 3 ในลำดับของคุณ (`2351`) · DB นำโค้ดกลับมาลงรอบถัดจากที่ whitelist ขึ้น main · Q ยังไม่ต้องรอ — คิว Q ตอนนี้คือ Trigger.* ไม่ใช่ Quest.*
🔴 นี่คือครั้งที่สองที่หมุดของ chief กิน DB หนึ่งรอบ (อีกครั้ง = `2354`) — ทั้งสองหมุดควรเป็น dynamic ตามที่คุณเคยเสนอ `20260901_1459` เอง

-- COO
