# PANYA-DECISION → COO · เคาะ 2 งาน: B = ตัวแปลกฎ AI_COMBAT + ขับ wander · UI = แถบ "เฟรม client ที่ server รู้จัก n/327"

ADDRESSEE: COO (ยกลง NOW · จัดเข้ารอบของ B และ UI) · cc: chief · LANE-B · LANE-UI
FROM: ka1-A (มือเขียนแทน Panya) · ทาง: บุรุษไปรษณีย์ (เครื่องเจ้าของปิด)
เวลาเคาะ: 2026-09-06 ~20:30 +07 (โดยประมาณ) · คำเจ้าของในแชท: **"เคาะ 1,2"** (ข้อเสนอ ka1-A หลังอ่านแผนที่ Q ตามที่เธอสั่ง "รอแผนที่ Q ก่อน แล้วค่อยเสนอ")
ลำดับ: **ไม่แซง P-2 ชั้นสอง (สี/attr) ของ B และไม่แซงลำดับระบบ 1–5 ของ COO `1846`** — เป็นงานประจำสายที่ COO จัดคิวเองว่าเข้าเมื่อไร · ไม่มีอะไรต้องใช้เครื่องเจ้าของ

## งาน 1 — LANE-B: ตัวแปลกฎ AI_COMBAT (7 คำ) + ตัวขับ wander จาก AI_WANDER
สิ่งที่วัดแล้ว (ka1-A จาก gamedata/tables บน main · B ต้องวัดซ้ำเองก่อนเขียน):
- `CONSTDATA_TH__AI_COMBAT` 276 แถว (`s_CONDITOIN` ↔ `s_ACTION` ขนานบรรทัด · ยาวสุด 18 บรรทัด) · คำศัพท์เงื่อนไขทั้งคลัง = **BUFF_I, RATE(n), GO(0), KD_ENEMY, DOONCE, BUFF_ENEMY, HP_ENEMY</>(x), DISTANCE_ENEMY>(n)** · การกระทำเดียว = **CHASE(n)** (n = ช่องสกิลใน `MOBS.s_SKILLS` — ความหมายแท้ของ n ยังไม่ได้พิสูจน์ ต้องระบุเป็นสมมติฐาน)
- `CONSTDATA_TH__AI_WANDER` 73 แถว: `s_WANDER` = `IDLE;a;b\nRUN;c;d` + `n_FACTION` + `n_OFFESIVE` (0/1) + `n_AGGRO` (200–8000) · `MOBS` 3,210 แถวชี้ AI_WANDER 62 ค่า / AI_COMBAT 185 ค่า / AI_TACTIC 7 ค่า
- ที่มีอยู่แล้วในเขต B: `field_mob_ai_tables.py` (แถว AI คัดลอกไม่แต่ง) · `mob_aggro.py` (threat table + tick Idle→Aggro→Attack→Dead/Leash) · `mob_ai_control.py` (`tick_step`) — B เขียนไว้เองว่า "ยังไม่ขับ wander"
ส่งมอบ (ตามรอบ · pure-logic ก่อน · ห้ามแตะ wire จนกว่า COO เห็นเทส):
1. `mob_ai_rules.py` (ชื่อเสนอ): parser ของภาษากฎ 7 คำ → โครงสร้าง (เงื่อนไข, การกระทำ) ต่อแถว · **ต้อง parse ครบ 276 แถวโดยไม่มี unknown token** (เทส: นับ token ที่ parse ไม่ได้ = 0) · 6 แถวที่บรรทัดไม่ขนาน + 8 แถวที่ไม่จบด้วย GO(0) (B เคยวัดไว้ใน `AI_COMBAT_PARALLEL`) ต้องมีพฤติกรรมที่ประกาศชัด
2. ตัวประเมินกฎต่อ tick: รับสถานะ (HP ตัวเอง/ศัตรู, ระยะ, บัฟ, KD, ทอย RATE) → คืน CHASE(n) แถวแรกที่เงื่อนไขจริง · RATE(n) = โอกาส n% **ต่อการประเมินหนึ่งครั้ง** (สมมติฐาน — ระบุในเอกสาร) · DOONCE = ครั้งเดียวต่อชีวิตมอน
3. ตัวขับ wander: อ่าน `IDLE;a;b / RUN;c;d` → สลับหยุด/เดินรอบจุดเกิด · **หน่วยของ a,b,c,d (วินาที? เมตร?) ยังไม่รู้ — B ต้องเลือกการอ่านหนึ่งแบบ เขียนเป็น nonclaim และทำให้เปลี่ยนได้ในค่าคงที่เดียว** · ยังไม่ต้องส่งตำแหน่งขึ้นสาย (ส่วนนั้นเป็นรอบถัดไปหลัง COO อนุมัติ)
4. เชื่อมกับ `mob_aggro.tick` โดยไม่เขียน controller ซ้ำ (COO-DECISION 2026-08-26 §1.3 ห้ามมี threat logic สองชุด) · ห้ามแตะ `Player.MobAppear`/spawn (เขต A ตาม COO `1846` ข้อ 3)
5. `SCOREBOARD:` แถว `ai-rules parsed 276/276 · combat eval real/stub · wander real/stub`

## งาน 2 — LANE-UI: แถบความคืบหน้า "เฟรม client ที่ server รู้จัก n/327" ในสารานุกรม
- แหล่ง: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (327 ชื่อ/hex id) เทียบกับ `src/` + `tests/` ของ pirate-force-server · ka1-A นับด้วย regex hex id ได้ **69/327** (ตัวเลขทางการ = census ของ UI เอง)
- ส่งมอบ: สคริปต์ census (รันซ้ำได้ทุกรอบ) + หน้า/ส่วนในสารานุกรมที่แสดง: รวม n/327 · แยกตามตระกูล (Community 38 · Equipment 17 · Pets 16 · Channel 16 · Express 12 · BuildingCrystal 12 · Activity 9 · GSSS 7 · CollectionObj 6 · Winemaking 5 · KnowledgeGuru 5 · GSCN 4 · GM 4 · …) · แต่ละชื่อ: รู้จัก (มี handler/encoder อ้างไฟล์:บรรทัด) / รู้แค่ชื่อ / ยังไม่แตะ · แยก `…Req` (client ส่ง ~13) ออกจากเฟรมที่ server ส่ง
- ใช้เป็นแถววัดถาวรใน scoreboard (`wire-names known n/327`) — เจ้าของใช้ดูว่า "งาน RE เฟรม" เหลือเท่าไรและหมดได้จริง

## สิ่งที่เจ้าของไม่ได้เคาะ (อย่าขยาย)
- ไม่เปลี่ยนลำดับระบบ 1–5 ของ COO `1846` · ไม่เปลี่ยน milestone · ไม่ตั้งเวลาเปิดเครื่อง · ไม่อนุมัติงานเครื่องเจ้าของใด ๆ

ใครทำอะไร: COO ลง NOW ทั้งสองงานพร้อมบอกว่าเข้ารอบไหน · B/UI เริ่มตามคิวสาย · ติดอะไรเขียนถึง COO
