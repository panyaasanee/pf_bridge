# R278 (round `4w5j25`) — LANE-E (PLATFORM), 2026-09-01T03:5x+07:00

## เหตุการณ์หลักของรอบ

`PANYA-ORDER 20260901_0215` (คำสั่งตรงจากเจ้าของผ่านกะ1-A หลังจบ `GT-172` ด้วยตัวเอง) พักไมล์สโตน
M1-M6 ทั้งหมด ทุ่มไปที่ P-1 (ของดรอปอยู่บนพื้นนานพอ) / P-2 (สีชื่อมอนถูกสถานะ ห้ามชมพู) / P-3 (เปิดปุ่ม GM)
บวกงานสร้างใหม่ 4 ชิ้น (GM-A `/warp` ไม่ใส่พิกัด, GM-B `/speed`, UI-A กลับหน้าเลือกตัวละคร, UI-B logout จริง)
และคำสั่งให้เซิร์ฟเวอร์ส่ง NPC เองไม่ต้องรอผู้เล่นเดิน จดหมายนี้ค้างไม่มี stub ตั้งแต่ 02:15 — เป็นงานสำคัญ
ที่สุดของรอบนี้ ทำก่อนหัวข้ออื่นทั้งหมด

## ทำอะไรไปบ้าง

1. **ประกาศลำดับงานใหม่** — มอบหมาย P-1→LANE-B, P-2→LANE-GM, P-3→LANE-GM, GM-A/GM-B→LANE-GM,
   UI-A/UI-B→LANE-A (หนึ่งเรื่องหนึ่งสายตาม PROCESS_GATES.md #12/#15) พร้อมข้อมูล Codex ที่ใช้ได้ทันที
   (`PF_ATTR_NAME_COLOR_SELECTOR.tsv` สำหรับ P-2, `ACTORATTR_PROBE_TABLE_x_y.md` field x7/+0x54 สำหรับ
   GM-B) → `notes_to_chief/20260901_0302_FROM_CHIEF_R278_priority-reorg-*.md`
2. **เปิดใบคิว `GT-182`..`GT-186`** (5 ใบ — แยก UI-A เป็นสองใบตามกฎหนึ่งใบหนึ่งข้อพิสูจน์) พร้อม routing tag
   `NEEDS-ATTENDED-CAPTURE` และ RECHECK line ทุกใบ + ปรับหัว `GAME_TEST_QUEUE.md` ประกาศพักไมล์สโตน +
   ห้าม `GT-146`/ใบตีมอนเข้าคิว attended
3. **มอบหมาย pf-static-re ตรวจต้นเหตุ NPC-auto-spawn** พบว่า `CORE-REQUEST-026` (bg0002 เท่านั้น) แก้ปัญหา
   เดียวกันนี้ไว้แล้วตั้งแต่รอบแรก ๆ แค่ไม่เคยขยายไปฉากอื่น
4. **ให้ pf-builder ต่อสายให้จริง** — ขยาย disjunct ของ `WORLD-CENSUS-001` (`runtime.py`) จาก "เฉพาะ bg0002"
   เป็น "ทุกฉากยกเว้นเมือง" (11 ฉาก: 3-11, 14, 130) เมืองไม่แตะเพราะขับ dispatcher จริงแล้วเจอ `TypeError`
   จาก v141:4395-4416 (ไม่มี ChooseNPC responder กันไว้เหมือนฉาก 14) — เทสใหม่ปักกันไม่ให้ใครถอดทิ้งเงียบ ๆ
   เทสเต็มชุด **6089 passed / 0 failed / 323 skipped / 13118 subtests** (ยืนยันซ้ำเองอีกรอบ ไม่ใช่แค่เชื่อ
   ลูกมือ) ledger `HYPOTHESIS_LEDGER PASS entries=47` / `FUNCTIONAL_COVERAGE PASS domains=8` ไม่มี drift
5. **pf-adversary รีวิว** (บังคับเพราะแตะเส้นบูต/เฟรม ตาม PROCESS_GATES.md #9) — หาข้อบกพร่อง 6 จุดที่ตั้งไว้
   ทดสอบ ไม่มีข้อไหนรอด รวมถึงทำ mutation test เอง (ถอด exclusion ของเมืองออกชั่วคราวในเวิร์กทรีแยก ยืนยัน
   เทสจับได้จริง) **พบข้อสังเกตหนึ่งข้อ ไม่ใช่บั๊ก**: `WORLD-CENSUS-001` เป็นกลไกตอนล็อกอินเท่านั้น คนละตัวกับ
   CROSSING (ตอนเดินข้ามประตูกลางเซสชัน) — ผลประโยชน์จริงของงานรอบนี้อาจแคบกว่าที่ประกาศไว้ (ช่วยเคส relog
   เข้าฉากที่ไม่ใช่เมืองโดยตรง ไม่ใช่เคส "เดินจากเมืองเข้าแมพใหม่" ที่เจ้าของน่าจะบ่นถึงจริง) → ส่งคำถามกลับให้
   LANE-A ยืนยันว่า CROSSING เดินสำมะโนทันทีอยู่แล้วหรือไม่ ใน
   `notes_to_chief/20260901_0354_FROM_CHIEF_R278_npc-eager-census-widened-scope-caveat-*.md`
6. **บริโภคจดหมาย 44 ใบ** — 41 ใบผ่านลูกมือ (38 ปิดจริง + 2 คงเปิดไว้ตรง ๆ เพราะต้องรอเจ้าของเลือกทาง:
   v141 sendall break drops census reapply, attr-wire path1-vs-path2) + 3 ใบที่ chief อ่านเองโดยตรง
   (PANYA-ORDER เอง, COO-DECISION runtime.py write-zone [ยืนยัน mob_ai_tick wired จริงที่ runtime.py:37,5198
   เทส 9/9 ผ่าน], LANE-B automerge-marker-in-prose incident [ตรงกับ PROCESS_GATES.md #16 ที่มีอยู่แล้ว])

## WIRED = 4/4 (ไม่เปลี่ยนจากรอบก่อน — ไม่มีเลนใหม่ import เพิ่มรอบนี้)

## ไม่ได้พิสูจน์ / nonclaim

- NPC-auto-spawn ที่ขยายแล้วยังไม่ผ่านการยืนยัน client-observable จริง (11 ฉากใหม่คำนวณ headless ถูก
  แต่ไม่มีใครเห็นบนจอ) — รอ attended round ยืนยัน
- คำถาม CROSSING path ที่ส่งให้ LANE-A ยังไม่มีคำตอบตอนจบรอบนี้
- P-2 (สีชื่อมอน) มีแค่ 2 ค่า FontStyleID (61/62) ในตาราง Codex ไม่ครบ 3 สถานะที่เจ้าของขอ — ช่อง "ตาย=เทา"
  ยังไม่พบแถวที่ตรง ต้องขุดต่อ (RE-067/RE-155)
- ใบ 2 ใบยังค้างรอเจ้าของเลือกทางเดิน (v141 sendall break, attr-wire path1/2) — ไม่ใช่ของที่ chief ตัดสินเองได้

## เขตที่แตะ

pf_bridge: `notes_to_chief/**` (44 ใบ + broadcast + follow-up), `GAME_TEST_QUEUE.md` (banner + GT-182..186),
`rounds/R278_*.md`, `CHIEF_CONTINUATION.md` (บรรทัดเดียว) — pirate-force-server:
`src/pirateforce_foundation/runtime.py`, `tests/test_bg0002_census_wiring.py`,
`tests/test_world_census_arrival_trigger.py` (ใหม่) — ไม่แตะ `app.py`/`scenarios/`/`.github/`
