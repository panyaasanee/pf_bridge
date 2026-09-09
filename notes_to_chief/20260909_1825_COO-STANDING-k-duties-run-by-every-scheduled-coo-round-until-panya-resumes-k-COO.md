# COO-STANDING: งานเสมียนคิว (LANE-K) ทำโดย **รอบ COO ตามตารางทุกรอบ** จนกว่า Panya ปลด HOLD K — ใบนี้คือความจำข้ามรอบ อ่านทุกรอบ

ADDRESSEE: COO
cc: chief · Panya
FROM: COO (session แชตของ Panya 15:41-18:25) · 2026-09-09T18:25+07:00
ที่มา: PANYA 16:55 "Hold K และคุณมารับงานแทน K" · PANYA 18:20 ถามว่ารอบนาที 41 จะทำต่อได้ไหม → คำตอบ: ได้ **ถ้าใบนี้อยู่** (รอบตามตารางเป็น session ใหม่ทุกครั้ง ไม่มีความจำจากแชต · สิ่งเดียวที่ข้ามรอบได้คือ NOW + จดหมาย)

## ทำทุกรอบ หลังขั้นที่ 1 (กล่องจดหมาย) และ 1ข (ประตู M) ของ `prompts/COO.md`
เปิด `prompts/LANE-K.md` แล้วทำ "คิว (ลำดับตายตัวทุกรอบ)" ข้อ 1-5 ในฐานะ K โดยใช้กติกาเหล็กของ K ทุกข้อ (พับ = คัดลอก ไม่ตัดสิน · ห้ามลบ · ห้ามแตะเนื้อใบ · เลขใบตรวจ 3 ที่ก่อนวาง):
1. **พับผล**: ทุกจดหมาย `*RESULT*`/`*RESULTS*`/`OBSERVER_CONFIRMED` ที่ไม่มี `.CONSUMED.txt`/`.LANEK-FOLDED.txt` → หัวใบ + result block คำต่อคำ → stub · **ฉบับ `STANDING-*-RESULT-*` ใหม่ = ต่อบรรทัดในดัชนี `tickets/RE-325.md` (A) `RE-326` (B) `RE-327` (C) `RE-328` (D) แล้ว `.CONSUMED.txt`** ไม่ตั้งเลขใหม่ (`1452` k1317)
2. **ตั้งเลข**: คำขอ `*-TO-K-gt-body-*` / `*RE-TICKET*` / `*numbering*` ที่ไม่มี `.CONSUMED.txt` → เลขถัดไป (ล่าสุด **GT-324 / RE-328** ณ 18:00 · ตรวจ `grep -rhoE '\b(GT|RE)-[0-9]{3}\b'` 5 ที่ก่อนวาง) · เนื้อคำต่อคำลง `tickets/<id>.md` · stub ≤1 KB ในคิว · จดหมาย `<เวลา>_COO-AS-K-NUMBERED-<id>-<สาย>.md`
3. **เพดาน**: `GAME_TEST_QUEUE.md` ≤307,200 B (ตอนนี้ 230,060) · ใบใหม่ >8,192 B ย้ายเนื้อไป `tickets/` ตั้งแต่วาง · stub ≤1 KB (`ATTENDED:`/`HEADLESS_PROOF:`/`owner:` คงคำต่อคำ)
4. **`QUEUE_STATUS_SNAPSHOT.md`**: เติมหัวข้อรอบบนสุดแบบ K (ตาราง ใบ/เจ้าของ/รอบก่อน/รอบนี้/ใครขยับต่อ) · รัน `python3 tools_bridge/pf_queue_status.py` ก่อน/หลังแก้คิว แล้ว diff สถานะ — **ต่างได้เฉพาะที่ตั้งใจ** (เครื่องมือเขียน `.generated.md` ให้อ่านแล้วลบ · `drift-missing` ทั้งหมด = สารบัญมือถูกลบ รอ chief `1600` ไม่ใช่ drift)
5. **จดหมายรอบ** `<เวลา>_COO-AS-K-ROUND-<ตัวอักษรถัดไป>-<สรุป>-ALL-LANES.md` (ชื่อไฟล์ ≤100 ตัวอักษร) ท้ายด้วย `SCOREBOARD: NONE | ... |` · ตัวอย่างล่าสุด = `20260909_1730_COO-AS-K-ROUND-B-*` และ `20260909_1800_COO-AS-K-ROUND-C-*` (อ่านสองใบนี้ก่อนเริ่ม = รู้ว่าคิวอยู่ตรงไหน)
6. รอบว่าง (ไม่มีอะไรพับ/ตั้งเลข) = สุ่มตรวจ 20 ใบ (หัว vs RESULT) แล้วจบ · ห้ามหาเรื่องแก้เนื้อใบ

## กติกากันชนกัน
- **ทำจาก session ตามตารางเท่านั้น** (นาที 41) · session แชตของ Panya ทำงานคิวต่อเมื่อ Panya สั่งในแชต และต้อง `git fetch` + ดู `notes_to_chief/*COO-AS-K-ROUND-*` ล่าสุดก่อนแตะ
- แก้ไฟล์คิวผ่าน git clone เท่านั้น (ไม่ใช่ MCP เขียนไฟล์) · PR หัว `[COO as K]` body มี `PF-AUTOMERGE: v4` · preflight ต้อง PASS ก่อน push (`python3 tools_bridge/pf_gate_preflight.py` — server clone ต้อง `git merge --ff-only origin/main` ก่อน ไม่งั้น `[mainmerge]` แดงหลอก · `NOW.md` ≤12,288 B · ชื่อไฟล์ใหม่ ≤100)
- เขต: เขียนได้ = `GAME_TEST_QUEUE.md` `CLIENT_RE_QUEUE.md` `archive/*QUEUE*` `tickets/` `QUEUE_STATUS_SNAPSHOT.md` `notes_to_chief/` `NOW.md` — ตามคำสั่งเจ้าของ 16:55 เท่านั้น · `prompts/` `AGENTS.md` `tools_bridge/` `src/` ยังห้าม

## จบเมื่อ
Panya ปลด HOLD K (บรรทัด HOLD ใน NOW หายไป + ใบ `COO-RESUME-*-LANE-K`) → รอบ COO กลับไปทำแค่ขั้น 1/1ข/2 ตาม `prompts/COO.md` · ใบนี้เขียน `.CONSUMED.txt` วันนั้น

-- COO
