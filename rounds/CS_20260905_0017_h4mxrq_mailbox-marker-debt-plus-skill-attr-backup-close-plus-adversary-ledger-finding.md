# CS round h4mxrq — mailbox marker debt closed (10 ใบ) + งานสำรอง `plg1ne` ข้อ 2/3 ปิดผลลบ + adversary ยืนยัน `docs/HYPOTHESIS_LEDGER.json` ค้างบน `#768`

เวลาเริ่ม 2026-09-05 00:13 +07:00 · เวลาปิด 2026-09-05 00:17 +07:00 · claim `pf_bridge` PR #1228
(หัว `[LANE-CS] round h4mxrq: claim` เดิม ทับด้วยไฟล์นี้)

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]`

`pirate-force-server` open: #773 (`[LANE-E]`) `#774` (`[LANE-GM]`) `#775` (`[LANE-DB]`) — ไม่มี
`[LANE-CS]` · `pf_bridge` open: ไม่มี (ก่อนเปิด claim ของรอบนี้) ⇒ ไม่ถอย เปิด claim ได้ตามปกติ

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ** — รอบนี้ไม่มีโค้ด/เทสใหม่ในต้นไม้ `pirate-force-server` เลย (`git status`/`git diff` ว่างตลอด
รอบ ยังอยู่ที่ `origin/main` = `2eaecf8f` ฝั่ง `pf_bridge`) งานหลักของ CS ที่ขยับ M ได้จริง (ผูก
`resolve_skill_damage`/`damage_by_skill.py` เข้าฟิลด์ skill id จริง) ยังติดผลจับภาพ attended ของ `GT-243`
เหมือนเดิม (`2046`/`2113` ระบุแล้ว ไม่ใช่ตัวบล็อกใหม่) — รอบนี้จึงเป็นรอบซ่อมหนี้ marker + งานสำรอง (อ่าน/
ตรวจสอบ) + หยิบผล `ADVERSARY_PENDING` ค้างจากรอบก่อนตามลำดับ §7 ข้อ 2

## งานที่ทำ

### 1. หยิบผล `ADVERSARY_PENDING pirate-force-server#768` (งานแรกของรอบ ตาม §7 ข้อ 2)

สั่ง `pf-adversary` ตรวจ diff ของ `#768` (merge แล้วเป็น `2bec84e1`) ตั้งแต่ต้นรอบ พบ **defect จริงหนึ่งข้อ
ระดับสูง (governance gate false green)**: `docs/HYPOTHESIS_LEDGER.json` entry `HYP-PF-033` ไม่ถูกแตะโดย
`#768` เลย ยังเขียนว่า "FIVE pinned frames" + `stop_rule` ห้ามขยายจำนวน step โดยไม่เพิ่ม tracked
version/entry ใหม่ทั้งที่โค้ดที่ merge แล้วส่ง 6 เฟรมจริง และเกตที่มีไว้จับเรื่องนี้ (`tools/
verify_hypothesis_ledger.py`) ผ่านเขียวเพราะเช็คแค่สตริง marker ไม่เคยแปลความหมาย prose/นับ step จริง —
รายละเอียดเต็ม + สิ่งที่ adversary หักล้างไม่ได้ (self-guard ไม่ใช่ dead code, scenario/table drift ถูกจับจริง,
`starting_skill_ids(1)` ไม่ใช่ค่าเดา, index bounds ถูกต้อง, `production_allowed=False` คุมครบ) อยู่ในจดหมาย
`notes_to_chief/20260905_0013_LANE-CS-TO-CHIEF-adversary-confirms-hypothesis-ledger-stale-on-768-governance-gate-false-green.md`

**ไม่แก้ `docs/HYPOTHESIS_LEDGER.json` เอง** — ไฟล์นี้ผูกกลไกอนุมัติระดับเจ้าของ (`approval_id`/
`approved_entry_ids`/`approved_through`) ตามที่รอบ `30kpco` ระบุไว้แล้วตอนถามคำถามนี้ครั้งแรก (จดหมาย
`2256`, ยังไม่มีคำตอบ) รอบนี้ส่งจดหมายซ้ำถึง chief พร้อมหลักฐาน adversary ยืนยันว่าเป็นปัญหาจริง ไม่ใช่แค่
ข้อสงสัย — ขอวิธี bump ที่ถูกต้องก่อนแก้

### 2. หนี้ marker กล่องจดหมาย — 10 ใบ

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`) เจอ 11 ใบ ตรวจเนื้อหาทีละใบ (อ่าน
เต็มทุกใบ ไม่ใช่แค่หัวเรื่อง) พบว่า **10 ใบถูกตอบ/บริโภคไปแล้วจริงในประวัติรอบก่อนหน้า** แต่ `.CONSUMED.txt`
ไม่เคยถูกสร้าง (รอบ `30kpco` ระบุใน "ส่งอะไร" ว่าจะสร้าง marker ของใบ `2154` แต่ push จริงไม่มีไฟล์นั้น — ตรวจ
แล้วบน `origin/main` ก่อนรอบนี้ไม่มี) สร้าง marker ย้อนหลังทั้ง 10 ใบ พร้อมสรุปหลักฐานการปิดแต่ละใบในจดหมาย
`notes_to_chief/20260905_0013_LANE-CS-TO-COO-mailbox-marker-gap-closed-plus-skill-attr-backup-item-2-3-negative.md`
(รายชื่อใบ + หลักฐาน 10 ข้ออยู่ในจดหมายนั้น ไม่ซ้ำที่นี่)

ใบที่ 11 (`1346`, `COO-DECISION-chief-1310-accepted-...`) **ไม่ปิด** — grep เจอเพราะข้อความ
"ADDRESSEE: LANE-CS" ปรากฏในเนื้อใบ (อ้างอิงถึงใบอื่น) ไม่ใช่จ่าหน้าใบนี้จริง (จ่าหน้าจริง `ถึง: chief`) — false
positive ของ grep บันทึกไว้ในจดหมายกันงงซ้ำรอบหน้า

### 3. งานสำรองข้อ 2/3 ของ `plg1ne` — ปิดผลลบ

อ่าน `skill_attr_hypothesis.py` (843 บรรทัด, HYP-PF-035) ให้จบทั้งไฟล์ (เดิมอ่านแค่ 40 บรรทัดแรกในรอบ
`plg1ne`) — ไม่พบช่องว่างแบบ "มีค่าแต่ไม่มีชื่ออ่าน" เหมือนที่ `skill_catalog.py` เคยมี โมดูลสมบูรณ์ในตัวเอง
ครบ RE-061 wire shape (encoder/decoder/self-guard/scenario-gate) รอแค่ใบ GT attended เหมือน
`learn_skill_result_hypothesis.py` ⇒ **ข้อ 3 (`n_EQUIPTYPE`/`n_EQUIPTYPE_LHAND` accessor) ปิดผลลบ** — เงื่อนไข
เดิมคือเติมเฉพาะถ้าข้อ 1/2 เจอเหตุผลใช้จริง ทั้งสองข้อไม่เจอ งานสำรองสามข้อของ `plg1ne` ปิดครบแล้ว

### 4. งานสำรองใหม่ 3 ข้อ (รอบหน้าเริ่มได้ทันที)

รายละเอียดเต็มอยู่ในจดหมาย COO ข้างบน สรุป: (1) อ่าน `stats_progression_hypothesis.py` (2,681 บรรทัด ยังไม่
เคยอ่านจบ) เทียบ `tools/pf_damage_hit_result_static.py` หาตารางที่ยัง upgrade ไม่ครบ (2) เตรียม caller ของ
`resolve_skill_damage` ทันทีที่ผล `GT-243` ถึง (ยังไม่ใช่ backup item จริงจนกว่าผลมา) (3) ทบทวน
`persistence_class_id.py`+`persistence_starting_skills.py` คู่กันตอนถึงคิวเริ่มต้นข้อ 5

**เทส**: ไม่มีโค้ดเปลี่ยนรอบนี้ ⇒ ไม่รันชุดเต็มใหม่ (ไม่มีอะไรให้พิสูจน์ว่าไม่พัง) `git status`/`git diff` ของ
`pirate-force-server` ว่างตลอดรอบ ยืนยันแล้ว

## pf-adversary

สั่งแล้วต้นรอบ (ข้อ 1 ข้างบน) — ผลคืนครบภายในรอบนี้ **ไม่มี `ADVERSARY_PENDING` ใหม่ทิ้งไว้ให้รอบหน้า**
(รอบนี้เองไม่มีโค้ด/เทสใหม่จึงไม่ต้องสั่งซ้ำสำหรับงานของตัวเอง ตรงข้อยกเว้นของ `COO-DECISION 20260904_1428`
ข้อ 2 "รอบที่แก้ถ้อยคำ/อ่านอย่างเดียว = ไม่สั่ง adversary")

## ส่งอะไร

**pirate-force-server**: ไม่มีการเปลี่ยนแปลง — ไม่เปิด PR ใหม่

**pf_bridge**: PR #1228 (แทน `rounds/CS_h4mxrq_claim.md` ด้วยไฟล์นี้), เพิ่ม:
- `notes_to_chief/20260905_0013_LANE-CS-TO-COO-mailbox-marker-gap-closed-plus-skill-attr-backup-item-2-3-negative.md`
- `notes_to_chief/20260905_0013_LANE-CS-TO-CHIEF-adversary-confirms-hypothesis-ledger-stale-on-768-governance-gate-false-green.md`
- `.CONSUMED.txt` ของ 10 ใบ (รายชื่อในจดหมาย COO ข้างบน)

## nonclaims

- ไม่อ้างว่า `docs/HYPOTHESIS_LEDGER.json` ถูกแก้ — ยังค้าง รอ chief บอกวิธี bump
- ไม่อ้างว่าใบ `1346` ถูกปิด — ไม่ใช่ของ CS จริง (false positive grep) ปล่อยเปิดไว้ให้ chief/COO
- ไม่อ้างว่า `GT-249` เนื้อในคิวสมบูรณ์ — chief ยังไม่คัดลอกร่างจากจดหมาย `2256` เข้า `GAME_TEST_QUEUE.md`
- ไม่อ้างว่างานสำรองใหม่ข้อ 1 (`stats_progression_hypothesis.py`) มีช่องว่างอะไร — ยังไม่ได้อ่าน แค่ตั้งคิว
- ไม่อ้างว่ารอบนี้ขยับ M ใด ๆ — เหตุผลอยู่ด้านบน

## ติดอะไร / ใครปลด

- **`docs/HYPOTHESIS_LEDGER.json` bump** — รอ chief ตอบวิธี (จดหมายรอบนี้ ซ้ำคำถามเดิมของ `2256` พร้อม
  หลักฐาน adversary)
- **งานหลัก CS (skill id → damage caller จริง)** — ติดผลจับภาพ attended `GT-243`/`GT-249` (รอเครื่อง Panya)
