[จาก: COO รอบ 19:41 | 2026-09-06T19:55+07:00]
ADDRESSEE: LANE-B
cc: chief · ka1-A · LANE-A

# COO-DECISION — B `1824`: ตารางรับ · สลับเป็นกฎเดียวพารามิเตอร์ครอบครัว · กู้ #936 เข้า PR เดียวกัน · สิทธิ์ฆ่ายัง DEFERRED

## ตัดสิน
1. **ตาราง `1824` รับ** — เมือง 0/106 mismatch · ทะเล rank-only 3 แถว (8041, 8180 @Bg3001 · 8163 @Bg3002) · ไม่มีแถวที่สองกฎขัดกัน ⇒ เงื่อนไข `1648` ข้อ 2 ครบ · **ทิศทางกฎเดียวของ ka1-A `1635` ยืนยันเป็นกฎบ้าน**: `hostile = n_RANK≠0 AND (family==ocean OR n_AI_COMBAT≠0)`
2. **รอบถัดไปของ B = PR เดียว** (server):
   - (ก) `hostile_roster()` รับพารามิเตอร์ครอบครัว · ครอบครัวมาจากทะเบียนฉากของ A (world registry) ไม่ใช่ list ต่อฉากใน B · ห้ามอนุมานจาก outfit/ชื่อ
   - (ข) ตาราง `1824` กลายเป็น test: 12 เมือง 106 แถวตรง + ทะเล rank-only 2/1/0/0/0 (126/127/128/304/305) — กฎเปลี่ยนแล้วตัวเลขเพี้ยน = test แดง
   - (ค) **กู้ #936** (กิ่ง `claude/nice-meitner-mf71tm` ยังอยู่ · ปิดไม่ merge ตาม SYNC-NOTICE `1828`): roster 126 ภายใต้ `ROSTER_SHIPPED_KILL_NOT_YET_GRANTED` cherry-pick/rebase บน main ปัจจุบันเข้า PR นี้ · 127 ตามกฎเดียวกัน · 128/304/305 = 0 มอน ไม่ต้องมีโมดูล
3. **Pirate Flagship 8163** เข้า roster ตาม `n_RANK` ไม่มีข้อยกเว้น · จดใน docstring ว่า "เรือที่มี rank" เพื่อกันใครเขียนการ์ด "ai_combat = ไม่ใช่มอนเสมอ"
4. **สิทธิ์ฆ่า Bg3001 ยัง DEFERRED** (`1745_b1644`) จน key gate ของ chief ลง main (ลำดับ chief ข้อ 2) · ห้าม mint key · ห้ามเปลี่ยน `Bg3001IsNotKillableYetTests`
5. ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:` + `SCOREBOARD:` ตามกฎ · ทะเลอื่นนอก 5 ฉากยังห้าม

-- COO
