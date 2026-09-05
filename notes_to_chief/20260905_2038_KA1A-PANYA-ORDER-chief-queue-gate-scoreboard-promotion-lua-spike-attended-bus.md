[ถึง: chief (LANE-E) | จาก: ka1-A (มือเขียนแทน Panya · เซสชัน attended) | 2026-09-05T20:38+07:00]
ADDRESSEE: chief
cc: COO · LANE-Q (สายใหม่) · ทุกสาย (FYI)

# PANYA-ORDER 20:3x — แผนเพิ่มผลผลิตทีม 5 ข้อ (Panya เคาะครบ "ก+ข+ค ง จ") — chief รับ 5 งาน + 2 งานแถม

## ที่วัดได้ (origin/main 5 ก.ย. 19:4x — ที่มาของทุกข้อ)
- `gamedata/lua/` 616 สคริปต์ (306 เควส q_* · 309 ทริกเกอร์ t_*) เรียก API เซิร์ฟเวอร์ 160 ฟังก์ชัน 12,653 จุด — `PF_LUA_API_SPEC.md` ของคุณเองบอกว่าเรามี 0/160 · 12 วันไม่มีใครอ้างถึงสเปกนี้ (0 ไฟล์รอบ) ไม่มีสายไหนเปิด .lua เลย
- scenarios 60 ตัว `production_allowed=true` แค่ 10 · hypothesis 23 โมดูล — ไม่มีใครถือหน้าที่ปลดแฟล็ก
- `tools_bridge/pf_scoreboard.py` + `SCOREBOARD_FACTS.tsv` (DONE/COMING/STUCK ของ Panya) ตายตั้งแต่ 29 ส.ค. ไม่อยู่ในรีโป
- `GAME_TEST_QUEUE.md` 2.8 MB (ใบปิดแล้ว 92/153 ยังอยู่) · `CLIENT_RE_QUEUE.md` 925 KB (ปิดแล้ว 102/121) · `AGENTS.md` 86 KB · `NOW.md` 65 KB · archive ล่าสุด 27 ส.ค. — รอบ UI wzdzf7 ใช้ 19 นาทีกว่าจะ claim เพราะอ่านไฟล์พวกนี้
- `pf-adversary` หายเป็นบางรอบทุกสาย (5 ก.ย. ไม่มี/มี: A 4/4 · B 4/2 · CS 9/0 · DB 6/0 · GM 6/2 · UI 9/3)

## งานของ chief (เรียงตามลำดับทำ · ทั้งหมดเป็นงานครั้งเดียว — กฎถาวรอยู่ใน `prompts/CHIEF.md` + `prompts/COMMON_LANE_ROUND.md` แล้ว)
1. **(ก) ล้างคิวครั้งเดียว + เกตกันบวม**: archive ใบ GT/RE ที่ปิดแล้ว >24 ชม. ทั้งหมดไป `archive/*_ARCHIVE_20260905_*.md` ทิ้ง stub บรรทัดเดียว (PR แยกใบเล็ก) · `AGENTS.md` เหลือกฎที่ยังมีผล ≤30 KB ประวัติไป archive · แล้วเพิ่มด่านใน `tools_bridge/pf_gate_preflight.py`: ขนาดไฟล์บนกิ่งที่จะ push `GAME_TEST_QUEUE.md` >300 KB · `CLIENT_RE_QUEUE.md` >200 KB · `AGENTS.md` >30 KB · `CHIEF_CONTINUATION.md` >30 KB · `NOW.md` >12 KB = RED (แสดงขนาดจริง) · self-test ครอบ · เกณฑ์ปิด: preflight บน main เขียวหลังล้าง
2. **(ข) Scoreboard คืนชีพ**: ขยาย `tools_bridge/pf_scoreboard.py` ให้ derive แถวจากบรรทัด `SCOREBOARD: <DONE|COMING|STUCK|NONE> | <ประโยคผู้เล่น> | <หลักฐาน>` ท้ายไฟล์ `rounds/*.md` (รูปแบบใน COMMON) รวมกับแถวมือเดิม → เขียน `SCOREBOARD_FACTS.tsv` + `PLAYER_STATUS.html` ที่ราก pf_bridge ทุกรอบของคุณ (ka1-A เปิด .gitignore ให้ 3 ไฟล์นี้แล้ว) · เกณฑ์ปิด: PLAYER_STATUS.html บน main มีแถวจากรอบจริง
3. **(ค) ท่อ promotion**: สร้าง `docs/PROMOTION_BACKLOG.md` ในรีโปเซิร์ฟเวอร์ — ทุก scenario ที่ `production_allowed=false` + hypothesis module: ชื่อ · "ผู้เล่นจะเห็นอะไร" หนึ่งประโยค · หลักฐานที่พิสูจน์แล้ว (GT/ใบ) · สายเจ้าของ · ค่าใช้จ่ายปลดแฟล็ก (S/M/L) · COO จัดอันดับ 5 ตัวแรกลง NOW · ทุกสายมี "ปลดแฟล็ก 1 ตัว" เป็นงานสำรองข้อแรกแล้ว (COMMON)
4. **(ง) Lua spike 1 รอบ** (ก่อนส่งต่อ LANE-Q): ฝัง Lua ใน Python (`lupa` — ตรวจ wheel สำหรับ Windows py -3 ด้วย) โหลด `gamedata/lua/t_nex_t6.lua` + `gamedata/lua/Quest/q_kill5.lua` ด้วย API stub ครบ 160 (จาก `PF_GAMEDATA_LUA_API.tsv`) รัน headless ให้จบไม่ error · รายงาน: ทำได้/ติดอะไร/ทางเลือกถ้า lupa ใช้ไม่ได้ · **ลงทะเบียนเขต LANE-Q** ใน CHIEF_CONTINUATION + AGENTS §7: `src/pirateforce_foundation/script_*.py` · `src/pirateforce_foundation/lua_api/` · `tests/test_script_*` · `docs/SCRIPT_LANE.md` · `lane_hooks/lane_q_*` · `rounds/Q_*` (charter เต็ม = `prompts/LANE-Q.md`)
5. **(จ) รถบัส capture**: ตั้งแต่รอบนี้ ใบที่ต้องการเครื่อง Panya ต้องมีบล็อก `ATTENDED:` ≤5 บรรทัด (กดอะไร · ดูเฟรม/ค่าอะไร · เกณฑ์ผ่าน · ทรี/ธง/env) ก่อนเข้า READY — ไม่มี = ตีกลับสายเจ้าของ · บรรทัด `READY/PENDING …` เรียงใบที่บูตร่วมกันได้ไว้ด้วยกัน · ka1-A เก็บทั้งกองในบูตเดียว (ใบค้างตอนนี้: RE-235/237/261 ของ UI · GT-255/257)

## งานแถม 2 ข้อ
6. **adversary หายเป็นบางรอบ**: หาตัวแยกจากรอบที่มี/ไม่มี (สมมติฐาน ka1-A: `.claude/agents/` โหลดเฉพาะเมื่อ cwd ของเซสชันอยู่ในรีโปตอนเริ่ม) รายงาน COO · ระหว่างนี้ทุกสายใช้ token `ADVERSARY_UNAVAILABLE <PR>` + self-review + รอบถัดไปของสายรัน adversary บนกิ่งนั้นก่อน (COMMON แล้ว)
7. **AGENTS.md §7 เพิ่ม 4 บรรทัด** (กฎละบรรทัด): `prompts/` เจ้าของ Panya ห้ามทุกสายแก้ (ใบ 1910) · บล็อก `ATTENDED:` บังคับ · บรรทัด `SCOREBOARD:` บังคับท้ายไฟล์รอบ · เพดานขนาดไฟล์กลาง (ข้อ 1)

ทุกข้ออ้างอิงคำสั่ง Panya พูดสดในเซสชัน 5 ก.ย. 20:3x ("เอา ก+ข+ค ง จ") — ถามซ้ำได้ที่ COO เท่านั้น

-- ka1-A
