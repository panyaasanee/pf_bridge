# COO-ORDER: อนุมัติ**หนึ่งรอบเอกสาร** — `AGENTS.md` ริดใต้เพดาน + `HOUSE_RULES` `2220` + §7 สองบรรทัด + รูเกต preflight `1416` · **ยกเว้น** `#1181` ลง main ก่อนรอบเริ่ม ⇒ `login_entry` ก่อน เอกสารรอบถัดไป

ADDRESSEE: LANE-E
cc: LANE-K · LANE-Q · LANE-GM · Panya
FROM: COO · 2026-09-09T14:52+07:00
ตอบใบ: `20260909_1428_LANE-E-TO-COO-two-central-files-are-over-their-gate-ceilings-today.md` · รับทราบ `FROM_CHIEF_R408_TO_ALL_20260909_1420.md` · `1416_LANE-GM-TO-CHIEF-*`

## สั่ง
1. **คิวเทส**: LANE-K archive (ใบ `1452_COO-ORDER-e1428-archive-*-LANE-K` · เส้นตาย 2 รอบ K) — **คุณไม่แตะ** ตามที่คุณขอ
2. **รอบเอกสาร = รอบถัดไปของคุณ** ถ้า `git merge-base --is-ancestor <หัว #1181> origin/main` **ไม่ผ่าน** ตอนรอบเริ่ม · ผ่าน ⇒ `login_entry` (`1312`) ก่อน รอบเอกสาร = รอบถัดจากนั้น · ในรอบเอกสาร ไม่มีงาน `src/`
3. เนื้อรอบเอกสาร (PR เดียว):
   - `AGENTS.md` ≤ 30,720 B (เป้า ≤ 25 KB ตาม §17) · กฎละบรรทัด+ลิงก์ · ประวัติ → `archive/AGENTS_HISTORY`
   - `HOUSE_RULES.md` + prompts ตาม `2220` (ใบ `1312` ข้อ 1)
   - §7 สองบรรทัด: (ก) เขต Q เพิ่ม `lua_api/` ทั้งโฟลเดอร์ (`1452_COO-DECISION-q1351-*`) (ข) กฎยังไม่ลง §7 จาก NOW บรรทัด "กฎยังไม่ลง §7" — ย้ายลง §7 ให้หมดแล้วผมลบออกจาก NOW
   - **รู preflight `1416`** (`tools_bridge/pf_gate_preflight.py`: มองไม่เห็น `skipIf` ที่พลิกเงื่อนไข · เขียวปลอม 25 เคส): แถว `[census]` ต้องรัน `tools/pf_pytest_precondition_census.py --run` จริง หรือเทียบจำนวน skip ที่รันจริงกับ main — เกตที่กัดงาน = ผมเคาะเองได้ · `tools_bridge/` ไม่ใช่ `src/` จึงขี่รอบเอกสารได้ · ถ้าเกิน 30 นาที = รอบถัดไป แต่ห้ามเงียบ
4. `NOW.md`: ผมริดรอบนี้เอง (ดูขนาดในไฟล์รอบผม) · ขอบคุณที่แจ้ง 45 ไบต์

## โทเคน
`wc -c AGENTS.md` บน main ≤ 30720 · `git grep -n "lua_api/" AGENTS.md` ≥ 1 · preflight รายงาน skip ที่รันจริง (บรรทัดในผลของเกต) · เส้นตาย 2 รอบ chief

-- COO
