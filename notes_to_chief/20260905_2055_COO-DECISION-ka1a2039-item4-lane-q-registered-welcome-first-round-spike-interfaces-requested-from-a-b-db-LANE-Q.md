[ถึง: LANE-Q | จาก: COO | 2026-09-05T20:55+07:00 | ตาม PANYA-ORDER `2039` ข้อ 4 · charter = `prompts/LANE-Q.md`]
ADDRESSEE: LANE-Q
cc: chief (LANE-E) · ทุกสาย (FYI)

# COO-DECISION — LANE-Q (SCRIPT/QUEST) ลงทะเบียนแล้ว · รอบแรก = Spike ตาม charter ข้อ 1 · interface จาก A/B/DB สั่งแล้ว (`2056`/`2057`/`2058`) ไม่ต้องรอ

## สถานะที่ต้องรู้ก่อนเริ่ม
- ทีม 8 สาย: chief(E) · A WORLD · B COMBAT · DB · GM · CS · UI · **Q** · เขตเขียนของคุณตาม `prompts/LANE-Q.md` · chief ลงทะเบียนเขตใน `CHIEF_CONTINUATION.md`/`AGENTS.md §7` (`2038` ข้อ 4) — **ไม่ต้องรอ chief** จึงเริ่มได้ (เขตอยู่ในพรอมป์แล้ว)
- chief ทำ Lua spike 1 รอบเช่นกัน (`2038` ข้อ 4) — **ถ้าไฟล์รอบ `rounds/E_*` หรือ `docs/SCRIPT_LANE.md` ของ chief อยู่บน main ก่อนคุณเริ่ม ⇒ ต่อยอด ห้ามทำซ้ำ** · ไม่มี ⇒ คุณทำ spike เอง chief เลิกทำ (ใครถึงก่อนเป็นเจ้าของ · แจ้ง chief หนึ่งบรรทัดในไฟล์รอบ)
- M2 ติดที่ LANE-A (`SAILING_RESULT` key `1932`) — Trigger.* ของคุณ (คิวข้อ 2) คือชั้นถัดไปที่ A ต้องใช้ · ห้ามแตะการเข้าเกาะเอง

## รอบแรกของคุณ
1. Spike ตาม charter ข้อ 1 ทั้งข้อ · `lupa` ไม่มี wheel Windows py -3 ⇒ รายงาน COO พร้อมทางเลือก **แต่ไม่หยุด** (ทำบนคลาวด์ก่อน ระบุ `WINDOWS_WHEEL_UNVERIFIED`)
2. ไฟล์รอบต้องมี: `SCOREBOARD:` · `TWO_SESSIONS_SAME_SCENE:` (สคริปต์ที่แก้สถานะโลกต้องผ่าน registry ของ A) · จำนวน `LUA_API_STUB` ที่เหลือ (ตัวเลข)
3. ติดอะไร = จดหมายจ่าหน้าถึง COO แล้วเดินต่อ ห้ามรอ

-- COO
