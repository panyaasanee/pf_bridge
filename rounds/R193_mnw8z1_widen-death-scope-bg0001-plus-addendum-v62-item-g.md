# R193 (session mnw8z1) — widen death scope to bg0001 roster, ADDENDUM v6.2 item G, mailbox cleanup

## บริบท
รอบก่อน (R192, session 4txjyg) ทั้งสองรีโปถูก `list_pull_requests` รายงาน `merged: false`
ทั้งที่ merge จริงแล้ว (ยืนยันด้วย `git merge-base --is-ancestor` และ `pull_request_read(get)`
สด — pf_bridge PR #196 head `edbe1733` และ server PR #113 head `5d9cfd34` ทั้งคู่เป็น ancestor
ของ `origin/main`) — ตรงกับบั๊กที่สาย GM รายงานไว้ (`20260827_1936`) และ COO ยืนยันแล้ว (`20260827_1350`
ADDENDUM v6.2 item A). ไม่มีอะไรต้อง cherry-pick

workflow ทั้งสองรีโปตรวจแล้วยังมีชีวิต: `merge-claude-pr` (pf_bridge) และ `merge-claude-pr`+`gate-windows`
(server) รันสำเร็จต่อเนื่อง รวมถึง run ที่เกิดจาก round-claim commit ของรอบนี้เอง

## งานที่ทำ

### 1. widen death scope ไปมอนจริง 13 ตัว (10 template id) จากตาราง MOBS ใน bg0001
ตาม COO-DECISION 2026-08-27 13:50 (`widen-death-scope-bg0001-full-roster-approved`,
อนุมัติ `LANE-B-ASK-COO` 15:00) — คำนวณ template id set เองจาก `field_mob_tables.py`
(ไม่เชื่อตัวเลขจากจดหมาย, re-derive สด) ก่อนเริ่มแก้: 13 placements,
10 distinct template_id = {31, 34, 35, 60, 61, 62, 65, 94, 97, 103}

🔴 **พบระหว่างรอบว่า LANE-B ทำครึ่งงานไปแล้วบน `main`** (คนละ PR, ยังไม่เห็นตอนเริ่มรอบเพราะ fetch
ครั้งแรกยังไม่เห็น) — `pirate-force-server#119` (LANE-B, merge แล้วระหว่างรอบนี้เอง) เพิ่ม key เดียวกัน
เป๊ะเข้า `mob_death.WIDENING_RULINGS` (ชื่อ ruling และ template id set ตรงกับที่ chief re-derive เองทุก
ตัว) พร้อมเทสระดับ unit 3 ตัวใหม่ใน `tests/test_mob_death.py` — **ถูกต้องตามเขตเขียน** (`mob_death.py`
เป็นโมดูลของสาย B เอง) และ LANE-B เจตนาไม่แตะ `runtime.py` (เขตเขียนของ chief คนเดียว) ตรวจพบตอน
`git fetch origin main` ก่อน push (ไม่ใช่ตอนเริ่มรอบ) ⇒ **ทิ้งการแก้ `mob_death.py` ของ chief เอง
ทั้งหมด** (`git checkout -- mob_death.py`) แล้ว `git merge origin/main` เก็บของ LANE-B ไว้ทั้งชุด
conflict เดียวคือบรรทัด import ซ้อนกันในไฟล์เทส (`import dataclasses` ของ chief กับ `import contextlib`/
`import io` ของอีกรอบ) แก้โดยเก็บทั้งสามบรรทัด ไม่มีอะไรเสียหาย

**สิ่งที่ chief ทำจริงในรอบนี้หลังพบว่า LANE-B ทำครึ่งแรกไปแล้ว**:
- `src/pirateforce_foundation/runtime.py` — จุดเรียก `mob_death.kill(...)` เดียวในโปรดักชัน
  (ใน `step.death_due` block, เขตเขียนของ chief คนเดียว, LANE-B เจตนาเว้นไว้ให้) ส่ง
  `widened="COO-RULING-20260827-1350 widen-death-scope-bg0001"` แบบไม่มีเงื่อนไข (ปลอดภัยเพราะ gate
  เช็คเฉพาะ `actor_identity != SANCTIONED_FIRST_TARGET_IDENTITY` — ผ่าน 0x201F เหมือนเดิมทุกกรณี) +
  แก้คอมเมนต์เดิมที่บอกว่า "wiring นี้ไม่ส่ง widened=" ซึ่งกลายเป็นเท็จ (คอมเมนต์สั้น อ้างกลับไปที่
  `mob_death.py` แทนที่จะอธิบายซ้ำ — ที่นั่นมีคำอธิบายเต็มจาก LANE-B อยู่แล้ว)
- `tests/test_mob_combat_dispatch.py` — เทสเดิม
  `test_a_killing_blow_on_an_unsanctioned_identity_finishes_no_kill` ตั้งสมมติฐานว่า roster
  ทุกตัวนอก 0x201F ต้องไม่ตาย ซึ่งเป็นเท็จหลังการ widen นี้ (มันรันพังจริงตอนรันเทส ไม่ใช่คาดเดา — เทสนี้
  ทดสอบระดับ end-to-end ผ่าน dispatch จริง ไม่ใช่ unit level ที่ LANE-B ปิดไปแล้วใน `test_mob_death.py`)
  แก้เป็นสองเทส: (ก) `..._now_finishes_a_kill` พิสูจน์ roster mob ที่ widen แล้วตายจริงผ่าน dispatch จริง
  (ข) `..._on_a_template_no_ruling_names_still_finishes_no_kill` (mock `field_mobs.load_roster`
  ใส่มอน synthetic template_id=1 ที่ไม่มีใน ruling ไหนเลย) พิสูจน์ประตูยังปิดกับมอนที่ไม่มีชื่อจริง ๆ

**ผ่าน pf-adversary หนึ่งรอบก่อน commit** (บังคับตามกฎข้อ 10, รันก่อนที่จะรู้เรื่อง LANE-B#119) —
ยืนยันเลข template_id set ถูกต้อง (re-derive จาก AST เอง ไม่เชื่อจดหมาย), ไม่มี call site อื่นที่พลาด,
ไม่มี side effect ตอนส่ง `widened=` ให้ 0x201F, ไม่มี downstream logic ที่แยกมอน "widened" ออกจาก
"sanctioned" ผิดที่ · พบช่องว่างสถาปัตยกรรมระดับกลาง (ยังเจาะไม่ได้วันนี้): `WIDENING_RULINGS` เช็คแค่
`template_id` ไม่เช็ค scene — **LANE-B พบช่องเดียวกันนี้เองอย่างเจาะจงกว่า** (คอมเมนต์ `[OPEN RISK, NOT
MEASURED]` ใน `mob_death.py` ของพวกเขาเอง ชี้ตรงว่า `field_mob_tables_bg0015.py` ที่ commit ไว้แล้วจริง
มี 4 ใน 10 template id ซ้อนกับชุดนี้ (31, 34, 35, 103) แม้ยังไม่ถูกเรียกผ่าน `load_roster()` เลยก็ตาม —
มี guard test ของ LANE-B เองกันไว้ไม่ให้ wire โดยไม่ตั้งใจ) — ไม่มีใครเปิด COO-DECISION เรื่องนี้อย่างเป็น
ทางการ (LANE-B ทิ้งไว้แค่คอมเมนต์โค้ด) ⇒ chief แก้ `20260827_1425_CHIEF-ASK-COO-*.md` ให้อ้างอิงการพบ
ซ้ำสองทาง (chief + LANE-B) แทนที่จะเสนอเป็นการค้นพบเดี่ยว ไม่บล็อกอะไรวันนี้เพราะ bg0015 ยังไม่ถูก merge
เข้า `load_roster()` จริง

**เทส**: full suite (หลัง merge LANE-B#119 เข้าแล้ว) `3363 passed, 0 fail, 17 pre-existing capstone-import
collection errors (baseline เดิม ไม่เกี่ยวกับรอบนี้)`. รันแยก: `test_mob_death.py` 70 passed (67 เดิม +
3 ใหม่ของ LANE-B), `test_mob_combat_dispatch.py` 12 passed (11 เดิม -1 เทสที่ถูกแทนที่ +2 เทสใหม่ของ
chief) รวม 82 ก่อนรวมสวีต

**ผู้เล่นเห็นอะไรเพิ่ม**: มอนสเตอร์แดง 10 ชนิดจากตาราง MOBS ของ bg0001 (Tornado Eagle, Fighting Fish
soldier/Sergeant, Jungle Big Tiger, Toxic Vine, Ancient Civilization Alert Weapon, Ward Apes,
An Gebo Little Firebird, Mutant Green Eagle, Orc Chief) จะล้มและกลายเป็นศพจริงเมื่อถูกตีจนเลือดหมด
พร้อมมีสิทธิ์ดรอปไอเทม (loot roll มีอยู่แล้วจาก CORE-REQUEST-007) แทนที่จะค้างเงียบที่ 1 HP เหมือนก่อนหน้า
**ยังไม่ยืนยันชั้น client-observable** — ใบเทสใหม่ `GT-104` (ผ่าน `pf-queue-author`, ไม่บล็อก M4) ถูกเพิ่มลง
`GAME_TEST_QUEUE.md` รอบนี้

### 2. ADDENDUM v6.2 item G (broadcast ให้สาย A/B/GM)
`pull_request_read(method="get")` ต่อ PR เท่านั้น ห้ามอ่าน `merged` จาก `list_pull_requests`
(ยืนยันบั๊กสดด้วยตัวเองในหัวข้อบริบทข้างบน) — ส่งเป็นจดหมายกว้าง เพราะ ADDENDUM v6.2 ไม่มีไฟล์กลาง
เป็นข้อความที่กระจายผ่านจดหมาย/PR body ทุกรอบตามที่ v6.2 §18 ข้อ 5 ตั้งใจไว้แต่แรก
ดู `notes_to_chief/20260827_1420_CHIEF-BROADCAST-ADDENDUM-v6.2-item-G-pull-request-read-not-list.md`

### 3. เก็บกวาดกล่องจดหมาย (PANYA-ORDER 14:05 ข้อ 14/17)
- Stub ย้อนหลัง `RE-092` (หัวใบปิดไปแล้วตั้งแต่รอบ q4z3vi, ไม่มี stub ค้าง 20+ ชม.) —
  RE-085/086/087/093/094 อีก 5 ใบที่ PANYA-ORDER อ้างถึง ตรวจแล้วมี stub ครบแล้วจริง (รอบอื่นทำไปแล้ว
  ระหว่าง 13:55 ถึงตอนนี้) ไม่ต้องแตะซ้ำ
- อัปเดต stub `20260826_0910_..._.CONSUMED.txt` (ใน `archive/`) ให้มีบรรทัด "Action taken: superseded
  by CORE-REQUEST-013" ตามคำสั่ง COO 1350
- Stub 5 ใบ COO-DECISION 1350 ที่เพิ่งทำครบตามคำสั่งในจดหมายนั้นแล้วในรอบนี้ (item A/G, RE-096/103
  priority note, bagwall no-op, widen-death-scope wiring, world-pop-handoff stub)
- backlog ที่เหลือ (RE-088..103 ที่สาย A/B/GM เปิดเอง) **ไม่แตะ** ตามกฎใหม่ "ใครเปิดใบ คนนั้นบริโภคผล"
  (PANYA-ORDER 14:05 ข้อ 13) — ปล่อยให้สายเจ้าของใบบริโภคเอง

## WIRED v2 (นิยาม emission จริงบน production path, ไม่ใช่ import เฉย ๆ)
ไม่มีการเปลี่ยนแปลงจากบอร์ดล่าสุด (audit `20260827_1700`, ไม่มีเลนใหม่ถูก wire รอบนี้ — งานรอบนี้คือ
ปรับ scope ของเลนที่ wire แล้ว ไม่ใช่เพิ่มเลนใหม่)

**WIRED = 9/10**

### 4. PANYA-ORDER 12:30 (แก้ 12:4x) — ข้อ 4/5 ทำ, ข้อ 1 เลื่อนพร้อมเหตุผล
- ข้อ 4 (ป้ายเวลาต้องมาจาก `TZ=Asia/Bangkok date`, เทียบ heartbeat) → เพิ่มลง `AGENTS.md` §7
  **แล้วจับความผิดพลาดของตัวเองได้ทันทีที่ dogfood**: ร่างจดหมาย/stub รอบนี้เขียนเวลาไว้ `20:0x`
  (เข้าใจผิดว่าใกล้เส้นตาย M2 20:00) ทั้งที่เวลาจริงคือ `14:2x` (`TZ=Asia/Bangkok date` เทียบ
  `_BRIDGE_HEARTBEAT.txt`=13:50 ต่างกัน 29 นาที ไม่เกิน 60 นาที = ปกติ) → แก้ทุกไฟล์ที่พลาดแล้ว
  (จดหมาย 3 ใบ + stub 5 ใบ + ดัชนี `CHIEF_CONTINUATION.md`) ก่อน commit
- ข้อ 5 (regenerate/no-diff ก่อน commit ไฟล์ ledger) → เพิ่มลง `AGENTS.md` §7 อ้าง root cause จาก R189
- ข้อ 1 (โครง `lane_hooks/`) **ยังไม่เริ่ม** — งานสถาปัตยกรรมของตัวเอง (auto-discover, ต้องผ่าน
  pf-adversary ก่อนเสนอ merge) ไม่ใช่บรรทัดเดินสายเดียว ตัดสินใจไม่ยัดเข้ารอบนี้ที่มีงานโค้ด gameplay จริง
  อยู่แล้ว (ความเสี่ยงรีบทำ = ขัดหลัก "ทำครั้งเดียวจบ") **สัญญารอบหน้า: ทำเป็นลำดับแรกก่อนงานอื่นทั้งหมด**
- ข้อ 2 (จำกัด PR ~6 ไฟล์/เรื่อง) รับทราบ — โค้ด 3 ไฟล์ของรอบนี้อยู่ในเพดาน mailbox bookkeeping
  แยกเป็นคนละเนื้อหา ไม่ใช่การเลี่ยงเพดานด้วยการนับไฟล์เยอะ

### 5. รับทราบ PANYA-ORDER 14:25 (GM warp-to-other-maps, สองทาง) — ยังไม่มีอะไรให้ chief wire รอบนี้
มาถึงตอนท้ายรอบพอดี (merge origin/main ก่อน push) — ระบุ chief ให้ "ต่อจุดเรียก 2 จุด" (login scene
override + census ตาม scene_id) แต่ทาง ก ต้องรอ LANE-GM สร้าง config (`gm_login_scene`) และ census logic
ก่อน (เพดานเวลาที่ใบสั่งเองกำหนด: "ใบแรกรอบถัดไปของสาย GM") — ยังไม่มีโมดูลให้ chief import/wire จริงตอนนี้
ไม่แตะรอบนี้ รอ CORE-REQUEST จาก LANE-GM ตามลำดับปกติ

## ที่ยังไม่ได้พิสูจน์
- ชั้น client-observable ของการ widen death scope (ใบเทสใหม่ในคิว รอผู้เทส)
- CORE-REQUEST backlog ของสาย A/B/GM: ตรวจแล้วไม่มีใบค้างที่ต้อง chief ต่อสายรอบนี้ (say-wire/GM-012,
  combat-loot, CORE-REQUEST-008/010 ล้วน wired ไปแล้วในรอบก่อน ตามจดหมายที่อ่านเจอ)

## สถานะ PR
push แล้ว รอ merge — pf_bridge #203, pirate-force-server #121 (ทั้งคู่ยังเป็น draft ระหว่างทำรอบนี้)
