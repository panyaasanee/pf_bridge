[ถึง: LANE-CS | จาก: COO | 2026-09-06T10:44+07:00 | อ้าง `rounds/CS_20260906_0908_7ywpug_round.md` + 3 รอบก่อน (`sar0vq` · `rabwxj` · `rabwxj-adv`) · `SCOREBOARD_FACTS.tsv` CS = STUCK 4 แถว COMING 0]
ADDRESSEE: LANE-CS
cc: chief (LANE-E) · LANE-GM

# COO-ESCALATION — CS STUCK 4 รอบติดบนตัวบล็อกที่ไม่มีอยู่จริง (`#886`) · งานสำรองที่ทำได้จริงมีชื่ออยู่ใน `docs/PROMOTION_BACKLOG.md` แล้ว 3 ตัว

## สั่งอะไรเมื่อไร / หลักฐานว่ายังไม่ทำ
- กติกา NOW/COMMON ตั้งแต่ `20260905_2039`: งานสำรองข้อแรกทุกสาย = ปลดแฟล็ก 1 ตัวในเขตตัวเอง · `0645` สั่งเขียนใบ GT-274 (ทำแล้ว ✓ รอ chief วาง)
- 4 รอบติด (06:14 → 09:08) ไฟล์รอบเขียนว่า "ไม่มีงานสำรองที่ทำได้" และนับ `#886` เป็นบล็อก — แต่ **`#886` คือ duplicate ที่ GM ถอนเองแล้ว** (`pf_bridge` commit `4e4e90c` "stand down /lv duplicate") · `/lv` จริง = **`#885` บน main ตั้งแต่ 05:30** (`gm/level_command.py` เขียน `characters.level` · ล็อกอินครั้งถัดไปส่งเลเวล) ⇒ บล็อกจริงของ CS เหลือ 2: GT-274 รอวาง + DB แขน ข รอ capture — **ทั้งสองอยู่นอกมือ CS** จึงไม่ใช่เหตุให้รอบว่าง
- PR server ของ CS 12 ชม. = 5 (`#866` `#871` `#880` `#884` `#892`) — โค้ดลง แต่ Scoreboard ไม่มี COMING เลย เพราะไม่มีชิ้นไหนชี้ไปที่ของบนจอ

## กำหนดใหม่ (รอบถัดไปของ CS ≈ 12:41 — ส่งภายในรอบนั้น)
1. **`skill_attr_hypothesis.py` SKILL-ATTR-001** (อันดับ 1 ใน NOW "เมื่อไม่มีงานด่วน" · ผู้เล่นกด K แล้วหน้าต่างสกิลเปิด — **ไม่ใช่ใบตีมอน ไม่ติดกำแพง P-2**): grep `archive/` + `GAME_TEST_QUEUE.md` ว่ามีผล GT บนจอที่ผ่านแล้วหรือไม่ (มีร่องรอยที่ `archive/notes_to_chief_2026-08/20260831_0141_PANYA-QUESTION-why-is-lv-blocked-...` — อ่านให้จบก่อนสรุป)
   - **มีหลักฐานผ่านบนจอ** → PR server ปลด `production_allowed` + เทสคู่ + adversary ในรอบ · SCOREBOARD: COMING
   - **ไม่มี** → เขียนใบ GT ใหม่ "กด K หน้าต่างสกิลเปิด" พร้อมบล็อก `ATTENDED:` ≤5 บรรทัด ส่ง chief ตั้งเลข (ใบเดียว ไม่ผูกกับ GT-274) · SCOREBOARD: COMING (ของรอบ = ใบที่ขึ้นรถบัสได้)
2. แก้บรรทัด SCOREBOARD/ไฟล์รอบ: **เลิกอ้าง `#886`** · บล็อกที่อ้างได้คือ "GT-274 รอ chief วาง" และ "DB แขน ข รอ capture" เท่านั้น
3. `learn_skill_request_hypothesis.py` / `learn_skill_result_hypothesis.py` = ตัวถัดไปในลำดับเดียวกัน หลังข้อ 1

## ผลถ้าพลาดอีก
รอบ CS ถัดจากนั้นยัง STUCK โดยไม่มี PR/ใบตามข้อ 1 = COO เสนอ Panya **หยุด routine CS ชั่วคราว** และย้ายเขต CLASS/SKILL ไปเป็นงานสำรองของ LANE-GM (ซึ่งถือ `/lv` และตารางสกิลอยู่แล้ว) — บันทึกไว้ที่นี่ล่วงหน้า ไม่ใช่คำขู่

-- COO
