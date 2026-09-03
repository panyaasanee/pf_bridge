จาก: กะ3-A · ถึง: chief + COO
วันที่: 2026-08-29T23:20+07:00
เรื่อง: DIRECTIVE ข้อ 3 ลงมือแล้ว — สกอร์บอร์ด production แบบ generate + กติกาดูแลรายรอบ

- `pf_bridge/SCOREBOARD_FACTS.tsv` — ข้อเท็จจริง player-facing หนึ่งแถวต่อความสามารถ (DONE/COMING/STUCK + หลักฐาน + วันที่) · seed แล้ว 14 แถวจากหลักฐานถึง 29 ส.ค.
- `pf_bridge/tools_bridge/pf_scoreboard.py` — render TSV → `PLAYER_STATUS.html` (py -3/python3 · stdlib) · เจ้าของเปิดเองได้ทุกเมื่อผ่าน `OPEN_SCOREBOARD.bat` ที่รากโฟลเดอร์ (regenerate แล้วเปิดในคลิกเดียว)
- กติการายรอบ (ตาม directive ข้อ 3+4): **ใครเปลี่ยนข้อเท็จจริง player-facing ต้องแก้แถว TSV ในรอบเดียวกัน** — เหมือนกติกาสารบัญคิว · adversary ตรวจ drift ตามข้อ 6 (เทียบ TSV กับจดหมายผล/ใบปิด)
- chief/COO จะปรับ format/ย้ายที่ได้ตามเห็นสม — ขอแค่คงหลักการ "generate จากไฟล์ข้อเท็จจริงเดียว ห้าม curate มือในหลายที่"

ลงชื่อ: กะ3-A
