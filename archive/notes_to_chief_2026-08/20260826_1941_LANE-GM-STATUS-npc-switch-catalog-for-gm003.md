[ถึง: chief · COO · Panya | จาก: LANE-GM (session 7fnw9e) · 2026-08-26T19:41+07:00]

# LANE-GM STATUS — npc-switch catalog เพิ่มเข้า GM-003 (`npc` command ได้ hint แล้ว)

## ค้นก่อนถอด (บังคับ)

ค้นใน `pf_bridge\gamedata\` แล้ว: เจอ (`00_SEARCH_HERE_FIRST.md` ระบุ `CONSTDATA_TH__MOBS.tsv` ไว้ตรง ๆ ตรงกับที่ใบ 1630 อ้างถึง — สกัด 7 แถว `n_GM_SWITCH=1` มาเป็นตารางย่อยของสายนี้เอง) · ค้นใน `external\` แล้ว: ไม่เกี่ยวข้อง (รอบนี้เป็นเรื่อง gamedata table ไม่ใช่ wire/serializer)

## สร้างแล้วรอบนี้ (บน `pirate-force-server`, PR รอ merge)

`gm/npc_switch_catalog.py` + `gm/data/gm_npc_switch.tsv` — mob_id -> ชื่อจาก client สำหรับ 7 NPC กิจกรรมที่ `CONSTDATA_TH__MOBS.n_GM_SWITCH=1` (855/871/882/897/902/8180/8181) · `gm/commands.py` เพิ่ม `describe_npc_target()` มิเรอร์ `describe_warp_target` เดิม (hint ไม่ใช่ gate) · เทสรวมสายนี้ตอนนี้ **96 เทส ผ่านทั้งหมด** (จาก 86) · `pf-adversary` ตรวจก่อน commit แล้ว ไม่พบข้อบกพร่อง (มีข้อสังเกตไม่บล็อก 2 ข้อ บันทึกไว้ใน `rounds/GM_20260826_1941_*.md`)

## เช็คล็อกกันเหตุการณ์ #66 ซ้ำ (ใบ 1755)

ก่อนยึดล็อก ตรวจผ่าน GitHub REST API (`curl` ตรง ไม่ใช่ `gh`) — ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo ก่อนเริ่ม (มีแค่ `[LANE-E]` #130/#71 ไม่ใช่ของสายนี้) และตรวจ `.gitattributes` ยืนยัน `*.tsv text eol=lf` (ที่ chief เพิ่มหลังใบ 1755) ครอบคลุมไฟล์ใหม่ของรอบนี้จริงผ่าน `git check-attr` — ไม่มีความเสี่ยง gate-RED ซ้ำแบบเดิม

## ไม่มีอะไรใหม่ให้เทส

`CORE-REQUEST-006` (GM state ตอน login) ยังไม่ถูกต่อสาย ยืนยันจาก `FROM_CHIEF_R179` ("GM ยังไม่ต่อสายรอบนี้") — รอบนี้เป็นโค้ด/เทสฝั่งเซิร์ฟเวอร์ล้วน ไม่มี wiring เข้า runtime ผู้เทสยังไม่มีอะไรทำในเกมจนกว่า CORE-REQUEST-006 จะ merge

## RE ที่ยังค้าง (ไม่ใช่ของใหม่)

`RE-085`-`RE-091` (ชุด GM tooling 4 ใบ + เส้นทางเรือ/ท่าเรือ 3 ใบ) ยังรอ RE runner บนสะพาน ตาม `FROM_CHIEF_R178` — ใบนี้ไม่ขอซ้ำ แค่ยืนยันสถานะ

## nonclaim ของรอบนี้

`describe_npc_target()` บอกแค่ว่า client เองติดธง `n_GM_SWITCH` ไว้กับ mob_id นี้หรือไม่ — ไม่ใช่คำยืนยันว่า toggle NPC ตัวนี้บนเซิร์ฟเวอร์จริงมีผลอะไร (ยังไม่ต่อสาย execute) และไม่ใช่คำยืนยันว่า mob_id ที่ไม่อยู่ในตาราง 7 ตัวนี้ใช้คำสั่ง `npc` ไม่ได้
