# LANE-DB round `rjqssc` -- skill_points/unspent_points null audit (backlog item), piece 3 status report to COO

รหัสรอบ: `rjqssc` · เวลาเริ่ม: 2026-09-06T13:16+07:00 · claim (ไม่ใช่ takeover)

## 0. ขยับ NOW/M ข้อไหน

ไม่ขยับบันไดไมล์สโตนโดยตรง (M2/M3/M4 ไม่แตะ) รอบนี้ตอบ `COO-DECISION 20260906_1043` (สั่งให้ส่งพีซ 3
`0x309A` เป็น PR รอบนี้ "ไม่รอ RE") ด้วยการตรวจสอบก่อนแล้วพบว่า**พีซ 3 (โมดูล compose gate) ปิดโค้ดไปแล้ว
ตั้งแต่รอบ `dqwqr0`/2026-09-04** — ที่เหลือทั้งหมดบล็อกด้วย RE จริง (ดู §3.1) เขียนไม่ได้โดยไม่เดาไบต์ ⇒
แทนที่จะเขียนโค้ดเดา รอบนี้ปิดหนี้ backlog อื่นของสายตัวเอง (`skill_points`/`unspent_points` null audit,
ที่รอบ `64da3x` ของสายตัวเองเสนอไว้เป็นงานสำรองข้อ 2) เป็น PR จริง + adversary ในรอบ ตามที่ `1043` สั่งใน
รูปแบบ "PR จริงในรอบ" แม้เนื้อจะไม่ใช่พีซ 3 ตรงตัว (ติดป้าย `[สมมติของสาย DB - รอ COO ยืนยัน]` ในจดหมาย
ที่ส่งไปพร้อมกัน)

## 1. ล็อกรอบ

`git fetch origin main` ทั้งสองรีโปสด (`pf_bridge` @ `3e7a5a93`, `pirate-force-server` @ `7cb34bc`) ·
`search_pull_requests`/`list_pull_requests` (pf_bridge, open, title `[LANE-DB] round`): **ว่างเปล่า** ก่อน
เปิดใบตัวเอง (ใบล่าสุดของสาย `#1464` ปิดไปแล้ว) ⇒ ไม่มีล็อกค้าง ไม่ต้อง takeover · ใช้กิ่งที่ระบบสุ่มให้
ทั้งสองรีโปตรง (`pf_bridge`: `claude/epic-meitner-rjqssc`, `pirate-force-server`:
`claude/cool-babbage-rjqssc`) commit `rounds/DB_20260906_1316_rjqssc_claim.md` push เปิด `pf_bridge#1485
[LANE-DB] round rjqssc: claim` (ไม่มี marker ตอนเปิด) · list ซ้ำทันที: มีใบเดียวคือของตัวเอง ⇒ ไม่แพ้
ทำงานต่อ

## 2. แหล่งความจริงที่อ่านตามลำดับ

1. `NOW.md` (fetch สด `13:16`) — บรรทัด "LANE-DB: PANYA-ORDER สวมอาวุธ ... มาก่อนทุกอย่าง" กับ
   "ชิ้น 3 `0x309A` typed ทำเลย (`1043`)"
2. mailbox `ADDRESSEE: (LANE-)?DB` ไม่มี `.CONSUMED.txt` คู่: พบใบล่าสุด `20260906_1043_COO-DECISION-...`
   (สั่งพีซ 3 ตรง ๆ) — ใบเก่ากว่านั้นตรวจแค่สองใบที่เกี่ยวกับงานรอบนี้โดยตรง (ดู §3.2 — เจอว่า consume
   ไปแล้วจริง ไม่ใช่ของค้าง)
3. `AGENTS.md` §7: อ่านทั้งหมด — ไม่มีกฎใหม่ขัดกับรอบนี้
4. ไฟล์รอบล่าสุดของสายตัวเอง `rounds/DB_20260906_1006_r0dxxv_...md` หัวข้อ "รอบหน้าทำอะไร" ข้อ 3 ("เช็คว่า
   `RE-272-RESULT`/`GT-272` มาหรือยัง — มาแล้วเขียน migration รับผลก่อนงานอื่นทุกชนิด") — เช็คแล้ว
   (§3.1) ยังไม่มีผลจับ ⇒ ข้อ 3 ยังไม่เข้าเกณฑ์ ไปงานอื่นตามลำดับ NOW/mailbox แทน
5. ไม่มีจดหมาย broadcast ใหม่ที่ยังไม่ consume

## 3. งานที่ทำจริง

### 3.1 ตรวจสถานะพีซ 3 (`0x309A` compose gate) ก่อนเขียนโค้ดตาม `1043`

`grep -in "RE-272.*RESULT\|GT-272.*RESULT"` ทั่ว `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` = 0 hit
เหมือนรอบก่อน (ยังไม่มีผลจับจากเครื่อง Panya) `src/pirateforce_foundation/persistence_attr_compose.py`
(`pirate-force-server`): `git diff origin/main` ของไฟล์นี้ = ว่างเปล่า (ไม่ขยับตั้งแต่ PR #823) ·
`SERVER_OWNED_FIELDS` ครบ 22 ฟิลด์ คอลัมน์ built ทุกตัว (`migrations/006`) · `block_gaps`/
`compose_full_block`/`live_unlock_report` ทำงานจริง ผ่านเทสทั้งไฟล์ · รอบของสายตัวเอง `64da3x`
(2026-09-05T17:39+07:00) เขียน nonclaim ข้อ 3 ไว้ตรง ๆ แล้วว่าพีซ 3 ยังบล็อกด้วยเหตุผลเดิม (RE-259/
RE-260 bounded negative ไม่ปลดล็อก, x=26/27 owner พิสูจน์ไม่ได้) — เหตุผลเดิมยังจริงอยู่วันนี้ (grep ซ้ำ
ยืนยัน) เขียนโค้ดเพิ่มตอนนี้จะเป็นการเดาไบต์ ขัด `COO-DECISION 20260901_1059` เขียนจดหมายสถานะแทน
(`notes_to_chief/20260906_1319_LANE-DB-REPORT-COO-piece3-gate-already-complete-since-round-dqwqr0-this-
round-closed-skill-points-audit-backlog-instead.md`) พร้อมทำงานอื่นที่ไม่ต้องเดาแทน (§3.3)

### 3.2 บริโภคจดหมาย + แก้คำพลาดของตัวเอง

consume `20260906_1043_COO-DECISION-...` (ใบสั่งพีซ 3 ของรอบนี้) — เขียน `.CONSUMED.txt` +
สำเนา `consumed/` ชี้จดหมายตอบ (§3.1)

ระหว่างกวาด mailbox เจอใบเก่า `1510`/`2119` (CORE-REQUEST จาก LANE-CS เรื่อง skill_points/
grant_learned_skill) ในลิสต์ "ยังไม่ consume" ของผม — **พลาด**: เขียนทับ `.CONSUMED.txt` ที่มีอยู่แล้ว
(จากรอบ `64da3x`/`aghbh2`) ด้วยข้อความทั่วไปของตัวเองก่อนตรวจ `git diff` เจอว่ามีเนื้อหาเดิมที่ละเอียด
กว่าอยู่แล้ว — **revert กลับด้วย `git checkout origin/main -- <path>` ก่อน commit จริง** ไม่มีอะไรถูก
เขียนทับไปถึง `main` (รายละเอียดเต็มอยู่ในจดหมาย §"กล่องจดหมาย" ของ `notes_to_chief/20260906_1319_...md`)
เพิ่มแค่สำเนา archival ที่ขาดของ `1510` ใน `consumed/` (เนื้อหาเดิม ไม่ใช่ของใหม่) บทเรียน: grep
`ADDRESSEE:` เฉยๆ ไม่พอสำหรับสรุปว่าใบไหนยังค้าง ต้องเช็คไฟล์ `.md.CONSUMED.txt` คู่กันก่อนเสมอ — ~70 ใบ
ที่เหลือใน mailbox ที่มี `ADDRESSEE: DB` อาจมีอีกหลายใบที่ consume ไปแล้วเหมือนกันแต่ยังไม่ได้ตรวจแบบ
ถูกวิธี (รอบนี้ตรวจแค่ 2 ใบที่เกี่ยวกับงานตรง เกินนั้นเกินงบเวลา)

### 3.3 `skill_points`/`unspent_points` null audit (backlog `64da3x` งานสำรองข้อ 2)

`src/pirateforce_foundation/persistence_skill_points_null_audit.py` (ใหม่) — สอง group แยกจาก
`persistence_null_audit.NULL_AUDIT_COLUMNS` เดิม (ไฟล์นั้นสงวนไว้เฉพาะ 4 คอลัมน์ที่มี birth `DEFAULT`
จริงตาม `009` — `skill_points`/`unspent_points` ไม่มี ผสมกันจะรายงานผิด): `WIRED_COLUMNS` (`skill_points`
— มี store door จริง `get_skill_points`/`spend_skill_points` จากรอบ `64da3x` + ผู้บริโภคฝั่ง CS สี่ไฟล์)
กับ `UNWIRED_COLUMNS` (`unspent_points` — schema เฉยๆ ตั้งแต่ `006` ไม่มีใครแตะ) · `store.py`: เมธอดใหม่
`skill_points_null_audit()` ตามแบบ `hp_pair_audit()` เป๊ะ ไม่แตะเมธอดเดิม · `tests/test_persistence_
skill_points_null_audit.py` (ใหม่ 17 เทส) รวมเทส grep โค้ดจริงยืนยัน grouping (ไม่ใช่แค่คำพูด)

`pf-adversary` เรียกต้นรอบพร้อมเริ่มงาน (ตามกฎ) — คืนผล 2 จุดจริง แก้ทั้งคู่ก่อน push:
1. docstring ของโมดูลเอ่ยชื่อ `stats_progression_hypothesis` ตรง ๆ ทำให้
   `tests/test_stats_progression_hypothesis.py::ContainmentTests::
   test_exactly_two_foundation_modules_import_the_lane` แดง (โมดูลนั้นมี containment rule ว่าต้องมีแค่
   สองไฟล์ที่เอ่ยชื่อมันได้) — แก้เป็นพูดอ้อมไม่สะกดชื่อ
2. เทสไฟล์มี `_CONSUMER_ALLOWED_FILES` เป็น class attribute แต่เทสตัวที่สองพิมพ์ลิสต์เดียวกันซ้ำแบบ
   hardcode แทนที่จะใช้ตัวแปรเดียวกัน (ขัดกฎบ้าน "derive ไม่ retype") — แก้ให้ใช้ `self.
   _CONSUMER_ALLOWED_FILES` ทั้งคู่
เพิ่มพารากราฟบันทึกข้อจำกัดที่ adversary ถามไว้ (เทส grouping เป็น grep string-based จับ future
consumer ที่อ้างผ่านค่าคงที่แทนชื่อ string ตรงๆ ไม่ได้) — เขียนไว้เป็นข้อจำกัดที่รู้ ไม่ใช่ bug ที่แก้
(ตรวจแล้วว่าไม่มี caller จริงแบบนั้นวันนี้)

## 4. ชุดเทสของรอบ

- ระหว่างทาง: `tests/test_persistence_skill_points_null_audit.py` (17 เทส) เดี่ยว ผ่าน · ร่วมกับ
  `test_persistence_null_audit.py`/`test_persistence_hp_pair_audit.py`/`test_persistence_attr_compose.py`/
  `test_persistence_typed_attr_columns.py`/`test_store_skill_points.py`/
  `test_stats_progression_hypothesis.py` (หลัง fix ข้อ adversary) — ผ่านหมด
- ก่อน push: `git merge origin/main` (fast-forward, ไม่มี conflict, ดึง PR #917 UI lane เข้ามาด้วย) →
  `pytest tests/` ชุดเต็มครั้งเดียว: **12220 passed, 369 skipped (ชื่อ/เหตุผลเดิมทั้งหมด), 0 failed**
- `python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server`: **PASS** (cp874, no new skips,
  ทั้งสองกิ่งถูกต้อง, bridgesize เดิมไม่ใช่ของรอบนี้)

## 5. หลักฐาน — สองชั้นแยกกัน

### 5.1 client-observable

ศูนย์ — เครื่องมือ audit ฝั่ง ops/COO ไม่มี caller ในเซสชันผู้เล่น เหมือน `hp_pair_audit`/
`typed_column_null_audit` ทั้งคู่ (คนละอย่างจาก M2/M3/M4 ที่ผู้เล่นเห็น)

### 5.2 wire/DB

`pirate-force-server#920` (`claude/cool-babbage-rjqssc`, PF-AUTOMERGE: v4, non-draft, ยืนยันด้วย
`pull_request_read get` ว่า marker อยู่จริง) — 3 ไฟล์ 549 บรรทัดเพิ่ม ไม่แตะเมธอดเดิม · เทส 17 ตัวใหม่ +
ชุดเต็ม 12220 ผ่าน

## 6. nonclaims

1. ไม่อ้างว่าพีซ 3 (`0x309A` full block) compose ได้แล้ว — สามเหตุผลเดิม (resend adjudication ว่าง,
   7 unsourced fields, x=30 refused ถาวร) ยังจริงทุกข้อ
2. ไม่อ้างว่า RE ticket `1748`/`RE-272`/`GT-272` มีผลใหม่ — grep ยืนยันซ้ำว่ายังไม่มี
3. ไม่อ้างว่า `skill_points_null_audit` มีผู้เรียกจริงในโปรดักชัน
4. ไม่อ้างว่าตรวจ mailbox ทั้ง 70 ใบแบบถูกวิธีแล้ว — ตรวจแค่ 2 ใบที่เกี่ยวกับงานรอบนี้ (ดู §3.2)
5. ไม่อ้างว่า `pirate-force-server#920` ขึ้น `main` แล้ว — ณ ตอนปลดล็อกสถานะคือ "เปิดแล้ว รอ gate"
6. ไม่อ้างว่าการตัดสินใจทำ skill_points audit แทนพีซ 3 ได้รับอนุมัติจาก COO แล้ว — ติดป้าย
   `[สมมติของสาย DB - รอ COO ยืนยัน]` ในจดหมายที่ส่งไปพร้อมกัน รอคำตอบ

## 7. รอบหน้าทำอะไร

🔴 **ด่วนที่สุด อ่านก่อนข้ออื่นทั้งหมด**: ระหว่าง merge `origin/main` ท้ายรอบนี้ (13:4x) เจอจดหมายใหม่
`notes_to_chief/20260906_1312_PANYA-DECISION-deadline-0155-0156-moved-1400-to-2300-equip-arm-b-is-db-
first-job.md` (Panya สดผ่านกะ1-B 13:12+07:00) — **เส้นตาย `0156` เลื่อนเป็น 23:00 คืนนี้ + สั่งตรงๆ ว่า
"รอบถัดไปของ LANE-DB = แขน (ข) สวมอาวุธ เป็นงานแรก"** ต้องขึ้น `main` ก่อน ~20:30 รอบนี้ไม่ทันเปิดงานนี้
(เพิ่งเจอตอนใกล้จบรอบ + ยังมี PR #920 ค้างอยู่) ⇒ **รอบถัดไปเปิดงานนี้ก่อนอย่างอื่นทั้งหมด ไม่ใช่แค่ก่อน
คิวปกติของสาย**

สิ่งที่รู้แล้ว (ไม่ต้องหาใหม่):
- **เฟรมขาเข้า (client→server) รู้ครบแล้ว ไม่ต้อง RE เพิ่ม**: `ItemOperateVitalReq` (`0x4BED`) 16 bytes
  `0B 05 14 08000000 32 0400000000000000` = op=5, value=8, identity=0x4 (Blade) — ยืนยันซ้ำ 3 ครั้งไบต์
  เดิมทุกครั้ง (`notes_to_chief/20260906_1255_KA1A-R321-RESULTS-...md` §2, ภาคผนวก A)
- **เฟรมขาออก (server→client) ที่คาดว่าเป็นคำตอบ**: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv:125`
  ระบุ `0x4C13 ItemOperateVitalRes` (คู่กับ `0x4BED ItemOperateVitalReq` แถวติดกันที่ `:123`) —
  `external/PF_SERIALIZER_FIELDS.tsv` มีแถวของมันแล้วจริง (grep `"ItemOperateVitalRes"` เจอ ~26 แถว
  เริ่มบรรทัด 769) **แต่หลายแถว R/W ยังเป็น `UNKNOWN`/`indirect_call_not_proven_serializer_slot`/
  `direct_call_not_proven_serializer`** ไม่ใช่ layout สำเร็จรูปที่อ่านแล้วเขียนโค้ดได้ทันที — ต้องมีคนอ่าน
  ทั้ง ~26 แถวแล้วตัดสินว่าพอสร้าง encoder ได้จริงไหม หรือยังต้องส่งเป็น RE ticket ใหม่ (รอบนี้ grep เจอ
  แค่ยังไม่ได้อ่านแปลผลเต็ม — เวลาไม่พอ ห้ามเดาต่อจากตรงนี้)
- ถ้ารอบหน้าอ่าน 26 แถวแล้วยังไม่พอสร้าง encoder ได้ชัด: เปิด RE ticket ทันทีเป็นงานแรก (อย่าลืม
  ระบุ "grep แล้ว: เจอแถวใน `PF_SERIALIZER_FIELDS.tsv:769-794` แต่ R/W หลายจุดยัง unproven" กันเสียรอบ RE
  runner ฟรี) · ถ้าติด `runtime.py`/`store.py` seam ⇒ CORE-REQUEST ถึง chief **ในรอบแรก** ตามที่ `1312` สั่ง
- เกณฑ์ปิด (ตาม `1312`): เปิดกระเป๋า → สวม → ช่องอุปกรณ์แสดงอาวุธ → relog → ยังสวมอยู่ · ใบ `GT-272`
- ติดอะไรที่ทำให้ไม่ทัน 20:30 ⇒ จดหมาย COO **ทันที** ไม่ใช่ตอน 22:00 (`1312` ข้อ 2.4)

รายการเดิม (ทำหลังข้อบนเท่านั้น ถ้าเวลาเหลือ):
1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. เช็ค `pirate-force-server#920` ผ่านเกตหรือยัง (`GATE_UNVERIFIED` ถ้ายังไม่ทราบตอนจบรอบนี้)
3. เช็คว่า COO ตอบจดหมายสถานะพีซ 3 (`1319`) หรือยัง — เห็นด้วยกับการสลับงานหรือสั่งอย่างอื่น
4. ถ้าเวลาเหลือและไม่มีงานหลักติด: เริ่มตรวจ mailbox ~70 ใบ `ADDRESSEE: DB` แบบถูกวิธี (เช็คคู่
   `.md`/`.md.CONSUMED.txt` ก่อนสรุปว่าใบไหนยังค้างจริง — บทเรียนจาก §3.2) ทีละชุดเล็ก ไม่ใช่ทีเดียวหมด

## งานสำรอง (ทำเมื่องานหลักติด)

1. RE ticket แคบสำหรับ x=26/x=27 (owner ยังพิสูจน์ไม่ได้) — audit/RE ไม่ใช่ diff+เทส
2. ตรวจ mailbox แบบถูกวิธี (ข้อ 5 ข้างบน)
3. คิวเดิม: ชิ้น 2/4 ของ PLAYER/CHARACTER รอผล RE runner, ประตูเควสรอ chief whitelist

SCOREBOARD: COMING | เครื่องมือวัด (audit) ใหม่สำหรับ skill_points/unspent_points เปิด PR แล้ว รอ gate — ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ (นี่คือเครื่องมือฝั่ง ops ไม่ใช่ฟีเจอร์ที่ผู้เล่นสัมผัส) | `pirate-force-server#920` (PF-AUTOMERGE: v4 ยืนยันด้วย GET) · จดหมาย `notes_to_chief/20260906_1319_LANE-DB-REPORT-COO-piece3-gate-already-complete-since-round-dqwqr0-this-round-closed-skill-points-audit-backlog-instead.md`
