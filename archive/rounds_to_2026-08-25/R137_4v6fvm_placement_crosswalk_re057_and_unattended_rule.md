# R137 (session 4v6fvm) — 2026-08-24 ~03:0x-03:3x (+07:00)

**สภาพแวดล้อม:** Routine cloud · fresh clone ทั้งสอง repo · โครงพี่น้องยืนยันแล้ว
(`../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง 11,388 bytes)

## การ์ด PR + probe
- PR เปิดค้าง `claude/*` + marker: **ไม่มีทั้งสอง repo** (list_pull_requests คืน `[]` × 2) => จับล็อกได้
- จับล็อก: empty commit `round claim: 4v6fvm` push ขึ้น `claude/exciting-goldberg-4v6fvm` => **PR #38 draft**
  (body มี `PF-AUTOMERGE: v4`) — เปิด draft ก่อนเริ่มงานตามลำดับ v5
- probe ① GitHub API/tool: ✅ อ่านได้ (list_pull_requests สำเร็จ) — ใช้เป็นทางหลัก
- probe ② ทาง D `ci-status`: ✅ มีชีวิต (`git ls-tree origin/ci-status ci/` คืนไฟล์ `ci/<sha>.json` · d_exit=0)

## เลขรอบ
เลขสูงสุดใน `rounds/` = R136 => รอบนี้ **R137** (ไม่ชน)

## กล่องจดหมาย — บริโภค 1 ใบใหม่
`20260824_0159_PANYA-RULINGS-3-and-RE056-DRAFT-placement-index-crosswalk.md` (ใบเดียวที่ยังไม่มี stub) — สามคำตัดสิน:
① GT-055 ไม่ต้องเปลี่ยนชื่อ (ยืนยันแนว R135) · ② เลือก "ทาง ก." ใบเชื่อมเลน PlacementOFF↔placement band ·
③ กติกาผลรอบ unattended สำหรับใบชั้น client-observable (Panya จะกลับมาเทสเอง 2026-08-26)
+ ร่างใบ crosswalk (ร่างใช้เลข RE-056)

## งานที่ทำ

### ① AGENTS.md — เพิ่มกติกาผลรอบ unattended ที่หายไป
จดหมาย 0159 เขียนว่า "ผู้ช่วยเขียนกติกานี้ลง AGENTS.md §9 แล้ว" แต่ **บน main ไม่มี** (grep หลายคำยืนยัน +
`git log` ของไฟล์) — commit ฝั่งสะพานล่าสุดที่แตะไฟล์นี้ไม่ได้พาบล็อกนั้นมา
=> chief เขียนลงเองรอบนี้: บล็อกใหม่ใน §9 (ตารางสี่แถว "เห็นจริง/จับภาพไม่ทัน/กล้องไม่ถึง/น่าจะไม่มีจริง")
+ pointer หนึ่งบรรทัดใน §5 กันกฎ "ผลลบมีค่าเท่าผลบวก" ขัดกับกติกาใหม่เงียบ ๆ
⚠️ ถ้าฉบับของผู้ช่วย sync ตามมาภายหลังจะซ้ำสองบล็อก — เตือนไว้ในจดหมายรอบนี้แล้วให้เก็บฉบับเดียว

### ② จ็อบ crosswalk ของร่างใบ — รันบน cloud จบไปหนึ่งจ็อบ (ลูกมือ pf-static-re)
ร่าง 0159 จ็อบ 1 สั่งหา crosswalk สคริปต์→ฉากจากตาราง `QUESTDATA_TH__*` — ตารางพวกนี้เข้า git แล้ว (R136)
จึงรันได้เลยไม่ต้องรอสะพาน · ผล: **ทางตัน — crosswalk เดียวในทั้ง 188 ตารางคือ `QUEST.s_LUASCRIPT`
(ครอบเฉพาะสคริปต์สาย `Quest/` 306 ไฟล์ ซึ่ง 0 ไฟล์เรียก `PlacementOFF`) · สคริปต์ 19 ไฟล์ที่เรียกจริง
ไม่ถูกอ้างในตารางไหนเลย** · 59/60/61 ของ Bg3002 ยืนยันซ้ำอิสระว่าไม่มี namespace ฝั่ง commit รองรับ ·
แถม: Bg3004 หายจากตารางชื่อฉากทั้งสองตาราง · กับดัก census (`lua/Quest/` ต้อง glob recursive)
รายละเอียด `FINDINGS_R137_QUEST_CROSSWALK_HUNT.md`

### ③ เปิดใบ RE-057 PLACEMENT-INDEX-CROSSWALK-001 (ลูกมือ pf-queue-author) — เข้า CLIENT_RE_QUEUE.md
ตามคำเคาะ "ทาง ก." · **เลขขยับจากร่าง (RE-056) เป็น RE-057** เพราะ 056 ถูก SKILLCAST-DIRECTION-002 ใช้แล้วใน R136 ·
เนื้อปรับตามข้อเท็จจริง R136+R137: จ็อบ crosswalk-ตาราง-commit ถูกถอดออก (ปิดแล้ว — ห้ามทำซ้ำ) ·
จ็อบที่เหลือเป็นงานสะพานล้วน (หา binding trigger→สคริปต์→ฉาก ใน section ที่ตัวถอด `.npc` ไม่ครอบ/ในไบนารี ·
probe ชี้ขาด = Bg3002 59/60/61 · ชี้ตัว >=3 จุด · ผูกกลับ band พร้อมป้ายยืนยัน/อนุมาน) · มีเกณฑ์จบ
(resolve ไม่ได้แม้บนสะพาน => ปมออกจากเลน static ถาวร ไม่เปิดใบ static ซ้ำ · ทางต่อรอ Panya เคาะ)

### ④ อัปเดตหัว CLIENT_RE_QUEUE
บรรทัดสถานะ R137 + บันทึกคำยืนยัน Panya ข้อ ① (GT-055 คงชื่อ) · ใบเปิดจริงตอนนี้: GT-055 · RE-056 · RE-057

## คิวเทสเกม (กฎ ⑤)
รอบนี้ **ไม่เพิ่มใบเทสเกม (attended)** — เลน attended พักตามคำสั่ง Panya 16:56 และคำเคาะ 0159 เลือกเดินเลน
static ("ทาง ก.") ก่อน · ใบใหม่ RE-057 เข้า `CLIENT_RE_QUEUE.md` (เลน static บนสะพาน · ไม่ต้องเปิดเกม) ·
สิ่งที่แตะฝั่ง attended รอบนี้คือ **กติกาการอ่านผล** (AGENTS.md §9) ไม่ใช่ใบใหม่

## ลูกมือที่เรียก
- `pf-static-re` — ล่า crosswalk ในตาราง commit (findings)
- `pf-queue-author` — ร่าง RE-057
- `pf-adversary` — ตรวจก่อน commit (กฎบังคับ ④): **ข้อมูลรอด re-derive ทั้งหมด · จับ defect ถ้อยคำ/hygiene 5 ตัว แก้ครบแล้ว:**
  D1 commit ต้อง add ไฟล์ใหม่ครบ (นับ staged เทียบประกาศ — ทำในขั้น commit) · D2 คำห้าม "ไม่มี/ไม่เกิด" ใน AGENTS.md
  scope ให้ชัดที่ชั้น client-observable (กันผู้เทสปฏิเสธปิดใบ wire/DB ที่วัดจริง) · D3 RE-057 เพิ่มทางออกที่สี่
  (binding ได้แต่ namespace 59/60/61 ไม่พบ ⇒ เข้าเกณฑ์จบ) · D4 คำห้าม grep ซ้ำผ่อนเป็น "ห้ามซ้ำโดยไม่มี key ใหม่"
  + qualifier "grep ด้วยชื่อไฟล์" (ID ตัวเลขยังตัดไม่ได้) · D5 จดหมายเตือนสะพาน: local edit ที่ AGENTS.md
  จะทำ sync หยุดตาย exit 4 — ให้ตรวจ/ทิ้งก่อนรอบ sync ถัดไป · nits: convention บรรทัดไฟล์ · INSTANCE count ·
  Bg3005/3006/3009 ก็หายจากตารางเช่นกัน (Bg3004 เด่นเพราะมีสคริปต์อ้างชื่อ)

## ไม่ได้พิสูจน์
- ไม่แตะ repo โค้ด (`pirate-force-server`) เลย — รอบนี้เอกสาร/คิวล้วน
- binding จริงของ 19 ไฟล์ PlacementOFF — ตอบได้จากเครื่องสะพานเท่านั้น (นั่นคือตัวใบ RE-057)
- ไม่ได้พิสูจน์ว่ากติกา unattended ใน AGENTS.md ถึงมือผู้เทสแล้ว — ถึงเมื่อ PR รอบนี้ merge + sync ฝั่งสะพาน pull
