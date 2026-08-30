# LANE-B round u98etz — 2026-08-30T22:48+07:00

## หนึ่งย่อหน้า

รอบต้นรอบตรวจ section A ของ ADDENDUM v2: PR ล่าสุดของสาย B ทั้งสอง repo (`pf_bridge#533`, `pirate-force-server#336`) merged แล้ว ไม่ต้องกู้ ไม่มี PR `[LANE-B]` เปิดค้าง จึงต้องเปิด draft ยึดล็อกก่อนทำงาน กล่องจดหมายพบ 2 ใบ `ADDRESSEE: LANE-B` ที่ยังไม่มี `.CONSUMED.txt`: `PANYA-ORDER 1450` (คำสั่งตรงจากเจ้าของ) และ `กะ1-A MEASURED 1509` — บริโภคทั้งคู่เป็นขั้นที่สองของรอบตามกติกา

## งานหลัก: PANYA-ORDER ข้อ ④ — ทำให้ ground-loot element ค้าง ≥30 วิ ได้ไหม พิสูจน์ headless ก่อน

### สิ่งที่พบ

`mob_drop_presence.sustain_a_kill` (production, wired อยู่แล้วใน `runtime.py`) composes เฟรมจาก **ledger ทั้งก้อน** ทุกครั้งที่เรียก ไม่ว่าจะมีคิลใหม่หรือไม่ — เรียกซ้ำด้วย `drops=()` จึงเป็น "resend" โดยไม่มีต้นทุนเพิ่มเลย (ไม่ placement ใหม่ ไม่ key ใหม่ ไม่ byte ใหม่) นี่คือกลไกเดียวกับที่ต่อสาย per-kill อยู่แล้ว เรียกอีกครั้งเฉย ๆ

### สิ่งที่สร้าง

- `pirate-force-server/tests/test_mob_drop_presence_sustained_resend_hypothesis.py` (ใหม่, 4 เทส): พิสูจน์ headless ด้วย clock จำลอง (ไม่ sleep) ว่าเรียก `sustain_a_kill(cell, legacy, ())` ซ้ำเป็นจังหวะไม่เท่ากัน (0,2,5,3,4,1,6,2,5,4,2 วิ = รวม 34 วิ) ทุกครั้งได้เฟรมไม่ว่าง แถวยังคลิกได้ (`take()` สำเร็จ) ตลอดหน้าต่าง ภายใน `DROP_LIFETIME_SECONDS=120.0` เดิม ไม่มีการแก้ไขค่านั้น เทสเพิ่มยังพิสูจน์ (a) resend ไม่ย้าย deadline/ไม่ re-place (b) หลังหมดอายุจริง resend ต้องรายงาน "ไม่มีอะไรบนพื้น" ตรง ๆ ไม่โกหก
- `pirate-force-server/src/pirateforce_foundation/mob_drop_presence.py`: เพิ่ม `DROP_PRESENCE_RESEND_ON_MOVEMENT_WIRING` (string constant, ไม่มีโค้ด production เปลี่ยน) — CORE-REQUEST ต่อสาย 1 จุดให้ chief ใน `runtime.py`: เพิ่ม branch ที่ 4 ในกลุ่ม `nested_id == legacy.TARGET_POS_VITAL` (เลียนแบบโครงที่ `ground_loot_hypothesis_scenario`/`ground_loot_nameprop_scenario` ใช้อยู่แล้ว) เรียก `sustain_a_kill` ซ้ำทุกครั้งที่มี TargetPosVital ขณะ flag ทดสอบเปิด — ไม่มี `_sent` latch (ตั้งใจ เพราะต้องการ cadence ไม่ใช่ once-per-session) ไม่มี timer/thread ใหม่ (เหตุการณ์จากไคลเอนต์เอง)

### ข้อจำกัดที่ต้องพูดตรง — ไม่ใช่ของ GT-146 โดยตรง

กลไกข้างบนอยู่ในไปป์ไลน์ของที่**มอนดรอปจริง** (`mob_loot`) ส่วน GT-146 บูตด้วย `ground_loot_hypothesis` ซึ่งเป็นเฟรมสังเคราะห์ครั้งเดียว **ไม่มี ledger/lifetime เลย** — ไม่ได้ขยายโมดูลนั้นรอบนี้ (เสี่ยงกว่า เป็นงาน wire ใหม่) เสนอแทนให้ย้าย GT-146 ไปใช้ของมอนดรอปจริง (Bg0002 template 31/34 ยืนยันตายแล้ว) — [สมมติของสาย B - รอ COO ยืนยัน] ยังไม่แก้ objective/steps เต็มรูปของ GT-146 เพราะเปลี่ยนรูปแบบใบทั้งใบ รอ chief/COO ตัดสินทิศทางก่อน

## งานรอง

1. **GT-146 (`GAME_TEST_QUEUE.md`)**: แก้ nonclaim ③ (ชี้ผิดใบ `GT-132`, ตอนนี้เขียนตรง ๆ ว่ายังไม่มีใบเป็นเจ้าของคำถามนี้สำหรับเฟรมของ GT-146 เอง), เพิ่ม step 0.5 P0 gate (หายภายใน ~1 วิ ให้ยกเลิกรอบทันที), demote step 6-7 (คลิกทั้งที่มองไม่เห็น) เป็นข้อสังเกตเสริม ไม่ใช่หลักฐานหลัก, ปะหัวใบด้วยผลรอบนี้ (การเปลี่ยนสถานะ header เป็น `[BLOCKED-ON-PERSISTENCE]` เต็มรูปเป็นของ chief ตาม PANYA-ORDER ⑤ ไม่ได้แตะ)
2. **ตอบกะ1-A**: template ไหนใน Bg0002 ดรอปหลายชิ้น — วัดจริง 2000 seed: template 31 (Tornado Eagle, ยืนยันตายแล้ว) และ 34 (Fighting Fish soldier, ยืนยันตายแล้ว) มี P(≥2 ชิ้น)=23.4% ต่อการฆ่าหนึ่งครั้ง, max 4 ชิ้น เท่ากันทั้งสองตัว (template 35 ตารางดรอปเหมือนกันแต่ยังไม่ยืนยันตาย ไม่แนะนำ)

## adversary pass ก่อน push

pf-adversary subagent รีวิว 2 ไฟล์ (เทสใหม่ + docstring constant ใหม่) ยิง mutant 3 มุม (เฟรมว่าง/สถานะปลอม/deadline เลื่อน) — ทุกอันถูกจับโดยเทส ไม่พบข้อบกพร่อง คำถามเปิดหนึ่งข้อ (ใครยืนยัน permission-token ของ flag ใหม่ fail-closed โดยการสร้าง ไม่ใช่ prose) — แก้แล้วโดยเพิ่มย่อหน้าใน `DROP_PRESENCE_RESEND_ON_MOVEMENT_WIRING` ชี้ให้ตามแบบ `ground_loot_hypothesis` เป๊ะ (constructor default None, identity check ไม่ใช่ equality, refuse ทุกไฟล์ที่ไม่ตรงเป๊ะ) พร้อมเทสที่ต้องมีเมื่อสร้างจริง

## เทสรัน

`pytest tests/ -q` (pirate-force-server, หลังแก้): **5462 passed, 327 skipped, 9129 subtests passed, 0 failed** (ก่อนแก้เท่ากันลบ 4 เทสใหม่ — ไม่มี regression)

## สังเกตนอกเขต (รายงาน ไม่แก้)

`_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุดยังค้างที่ `2026-08-30T14:58:02+07:00` ขณะรอบนี้เขียนที่ `22:48+07:00` — ต่างกัน **~7 ชม. 51 นาที** เคยถูกตั้งข้อสังเกตแบบเดียวกันที่ R248/R249 (ตอนนั้นภายหลังพบว่าขยับแล้ว กลายเป็น false alarm) รอบนี้ยังไม่เห็นขยับ ช่องว่างกว้างกว่าที่เคยวัดไว้เกือบสามเท่า (R248 วัดได้ ~2h34m) — นี่ไม่ใช่ไฟล์ของสาย B แก้ (`pf_git_sync` รันบนเครื่อง Windows bridge นอก git) รายงานตรงนี้เพื่อให้เจ้าของ/chief เห็น ไม่ได้บล็อกรอบนี้

## ไฟล์

- `pirate-force-server/tests/test_mob_drop_presence_sustained_resend_hypothesis.py` (ใหม่)
- `pirate-force-server/src/pirateforce_foundation/mob_drop_presence.py` (เพิ่ม docstring constant, ไม่แก้โค้ด production)
- `pf_bridge/GAME_TEST_QUEUE.md` (แก้ GT-146: nonclaim ③, P0 gate, demote steps)
- `pf_bridge/notes_to_chief/20260830_2248_LANE-B-REPLY-PANYA-ORDER-*.md` (ใหม่)
- `pf_bridge/notes_to_chief/20260830_2248_LANE-B-REPLY-KA1A-*.md` (ใหม่)
- mailbox stubs: `20260830_1450_PANYA-ORDER-*.md.CONSUMED.txt`, `20260830_1509_KA1A-MEASURED-*.md.CONSUMED.txt` (+ สำเนา `consumed/`)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ยังไม่มี — รอบนี้เป็นการพิสูจน์กลไก server-side + เอกสาร/จดหมาย ยังไม่มี call site ใหม่ใน `runtime.py` (CORE-REQUEST รอ chief) และยังไม่มีรอบ attended ใหม่บูต

PF-AUTOMERGE: v4
