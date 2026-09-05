# CLIENT RE QUEUE — คิวงานแกะไคลเอนต์/capture (static · ไม่เปิดเกม)

> **ไฟล์นี้เกิดจากคำสั่ง Panya 18:22 (+07:00) 2026-08-23** (`notes_to_chief/20260823_1822_PANYA-ORDER-split-queue-into-two-and-search-RE-deliverable-first.md`)
> — แยกใบ **แกะไคลเอนต์/capture** ออกจากคิวเทสเกม **ตั้งแต่ใบใหม่เป็นต้นไป** (ใบ static เก่า GT-040/042/044/046/047/048/049
> ยังอยู่ใน `GAME_TEST_QUEUE.md` ตามกติกาห้ามย้ายใบเก่า — สารบัญหัวไฟล์นั้นเป็นตัวเชื่อม)

**ผู้รับงาน:** คนหน้าเครื่องสะพานของ Panya (มีอิมเมจ client + capture + ไฟล์ข้อมูลเกมบนดิสก์) — **ไม่ใช่ผู้เทสหน้าจอเกม**
**กติกาไฟล์นี้:**
- ทุกใบในไฟล์นี้ **ไม่ต้องเปิดเกม · ไม่ต้องจับ `LOCK_GAME` · ไม่มี teardown · ไม่แตะ canonical DB · ไม่มีอะไรให้ดูบนจอเกมเลย**
  ⇒ ทำขนานกับรอบเทสเกมได้เสมอ ไม่แย่งทรัพยากรกัน
- 🔴 **ทุกใบใหม่ต้องมีป้ายเส้นทางหนึ่งใน `STATIC-ON-BRIDGE`/`STATIC-ON-CLOUD`/`NEEDS-ATTENDED-CAPTURE` เพิ่มจาก `[OPEN — assigned <สาย>]` ไม่ใช่แทนที่** (PROCESS_GATES.md §18 · R276) — ป้ายเดิมบอกว่า "ใครทำ" ป้ายนี้บอกว่า "ทำที่ไหนได้"; ไม่มีป้ายนี้ = RE runner บนสะพานกรองใบไม่เจอ (ดู `PROCESS_GATES.md` §18 สำหรับเหตุผลเต็มและตัวอย่างที่พังไปแล้ว)
- 🔤 **ตัวนับเลขเป็นชุดเดียวกับ `GAME_TEST_QUEUE.md` ต่อเนื่องกัน ห้ามแยกตัวนับ** (การอ้างข้ามใบต้องไม่พัง) ·
  **แต่ใบใหม่ในไฟล์นี้ใช้ prefix `RE-` ตั้งแต่ใบ 056 เป็นต้นไป** (คำสั่ง Panya 2026-08-24 ~00:2x · จดหมาย `20260824_0025_*`) ·
  ใบเก่า **GT-050/052/053/054/055 คงชื่อเดิมตลอดกาล** — จดหมายสั่ง "เริ่มที่ 055" แต่ใบ 055 ถูกออกเป็น `GT-055` ใน R134
  ก่อนคำสั่งถึงมือ chief ⇒ ตามกฎห้ามเปลี่ยนชื่อใบที่ commit แล้ว จุดเริ่มจริงของ prefix ใหม่คือ **056**
- 🔢 **กฎออกเลขใบ (COO-DECISION `20260829_0542_COO-DECISION-vote-item-5-withdrawn-shared-counter-stays.md` ข้อ 3 · แก้ต้นเหตุ "เต้นเลข" โดยไม่แตะตัวนับร่วม):**
  ① **ห้ามจองเลขล่วงหน้า** — เลขเกิดตอนใบลงไฟล์จริงเท่านั้น · จดหมายที่ต้องอ้างใบที่ยังไม่เปิด ให้เขียนว่า **"ใบถัดไป"** ห้ามเขียนเลขที่ยังไม่มีในไฟล์
  ② เลขถัดไป = ผลของ **คำสั่งค้นหาเดียว ไม่ใช่ความทรงจำ** (รันจากรากรีโป `pf_bridge`) แล้ว **+1**:
  `grep -ohE '\b(GT|RE)-[0-9]{3}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md archive/*QUEUE*ARCHIVE*.md | grep -oE '[0-9]{3}$' | sort -n | tail -1`
  ③ ชนกันจริง = **คนที่ push ทีหลังขยับเลขของตัวเอง** แล้วเขียนเหตุผลไว้ในใบ · **ไม่มี allocator กลาง** ไม่ต้องรอใครอนุมัติเลข
- คิวเทสเกม (attended · ขับ UI · ใช้ตา) อยู่ที่ **`GAME_TEST_QUEUE.md`** เช่นเดิม
- 🔴 **กฎบังคับ (คำสั่ง 18:22 ข้อ ④): ก่อนถอด/parse อะไรใหม่ ต้องค้นชุดส่งมอบ RE ของ Codex ก่อนเสมอ**
  เริ่มที่ดัชนี **`pf_bridge\external\00_SEARCH_HERE_FIRST.md`** · ทุกใบต้องกรอกช่อง
  `ค้นใน pf_bridge\external\ แล้ว: เจอ <อะไร> / ไม่เจอ` ในผล · **ถ้าเจอ ⇒ ใบเปลี่ยนจาก "ไปถอด" เป็น
  "verify sha → re-derive ปฏิปักษ์ → ใช้ต่อ"** (แบบเดียวกับ GT-050)
- 🔴 🆕 **กฎบังคับข้อสอง (R132 · จากจดหมาย 2150): ก่อนเปิดใบขุด "ข้อมูลเกม" (ตาราง/ข้อความ/ค่าตัวเลข) ต้องค้น
  `pf_bridge\gamedata\` ก่อนเสมอ** — ตารางข้อมูลเกมแกะครบแล้ว **188 ตาราง / 2,365 คอลัมน์** จาก CONSTDATA_TH/TEXTDATA_TH/
  QUESTDATA_TH/QUESTTEXT_TH (ดัชนี `gamedata\00_SEARCH_HERE_FIRST.md` · `PF_GAMEDATA_INDEX.tsv` · `PF_GAMEDATA_COLUMNS.tsv` ·
  ตารางเต็ม `gamedata\tables\*.tsv` grep ได้ตรง ๆ) · ทุกใบต้องกรอกช่อง `ค้น gamedata แล้ว: เจอ <อะไร> / ไม่เจอ` ในผล
  ~~⚠️ โฟลเดอร์นี้อยู่บนดิสก์สะพานเท่านั้น — ยังไม่เข้า git~~ ✅ **เข้า git ครบแล้ว (อัปเดต R136 · 2026-08-24):**
  `gamedata\tables\` 188 ตาราง + ดัชนี เข้าก่อนหน้านี้ · `gamedata\lua\` 616 ไฟล์ + `gamedata\scene\` 289 placement TSV
  + `PF_LUA_API_SPEC.md`/`PF_GAMEDATA_LUA_API.tsv` เข้าที่ commit `0801541` (Panya ruling 2026-08-23 · whitelist ตามจดหมาย 0124)
  ⇒ **cloud/CI อ่านได้ตรง ๆ แล้ว** — โค้ดที่พึ่งไฟล์พวกนี้เขียนได้ (pin sha ตามธรรมเนียม)
- ผลส่งกลับ **ทางจดหมายอย่างเดียว**: เขียนใน `notes_to_chief/` แล้วบรรทัดแรกเขียนว่า `ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย` · sha ก่อน-หลังของทุกไฟล์ที่พึ่งต้องตรงกัน
  🔴 **แก้ไขในไฟล์นี้จากเครื่องสะพานไม่ได้ ไม่ว่าใครสั่ง** (แก้ R298 · เดิมบรรทัดนี้เขียนว่า "กรอกช่อง result: ท้ายใบ" ซึ่งสั่งสิ่งที่ท่อทำไม่ได้)
  ไฟล์นี้เป็นหนึ่งในสามคิวของ chief ที่อยู่นอก push allowlist ของ `pf_git_sync.ps1` โดยเจตนา ⇒ การแก้บนดิสก์สะพาน
  **เดินทางออกไม่ได้เลย** และเมื่อ chief แก้ไฟล์เดียวกันจาก cloud เมื่อไหร่ pull ของสะพานจะถูกปฏิเสธ (`fast-forward refused`)
  ⇒ สะพานหยุดรับของจากทุกสาย · รายละเอียดและขอบเขตที่วัดแล้วอยู่ใน `PROCESS_GATES.md` §18 · แก้ไฟล์นี้ผ่าน PR จาก cloud clone เท่านั้น

**📊 รายการค้างที่ Panya ขอให้มองเห็นได้ (คำสั่ง 18:22 ข้อ ⑤):** ชุดส่งมอบ RE = **8 ตาราง 17,618 แถว data** ·
ผ่าน re-derive ปฏิปักษ์แล้ว (GT-042) · ✅ **ปิดแล้ว R131 (2026-08-23 ~21:0x):** ผู้อ่านฝั่งโค้ดตัวแรกคือ
`pirate-force-server/tools/pf_external_registry.py` (pin sha256 ทั้ง 5 ตาราง + cross-check 6 ข้อ + เทส 16 ใบ —
✅ **merge เข้า `main` แล้ว** merge commit `1e0b20b` · PR #12 · head `53ca7ef` เขียว(Actions run 32645331917 · subset) ·
R133 ยืนยันที่ commit `1e0b20b` (= `origin/main` ณ เวลาตรวจ · HEAD ของ clone รอบนั้น): tool มีจริง + เทส external 16/16 เขียว(cloud sanity)) · เลน headless สกิลยังต่อคิวหลัง GT-050 ปิดตามเดิม

> 🔎 **สถานะการเข้าถึงชุดส่งมอบ — ✅ ครบ 8/8 แล้ว (อัปเดต R145 · 2026-08-24 ~11:0x +07:00):**
> 5 ตารางแรกเข้า `main` ตั้งแต่ R131 (commit `284d986`) · **สามตารางท้ายเข้าแล้วที่ commit `579b468`**
> (`external: publish the last 3 Codex RE deliverable tables` · 2026-08-24 09:29 +07:00 — คนหน้าสะพาน `git add` ให้ตามที่ R131 ขอ)
> **นับแถวจริงบน cloud clone รอบนี้:** `PF_PROTOCOL_PRIORITY.tsv` 519 · `PF_DATA_EVIDENCE.tsv` 290 ·
> `PF_TAG_CENSUS.tsv` 11 (ไม่นับหัวตาราง) = **820 แถว data ตรงกับที่จดหมาย 20:39 พินไว้เป๊ะ**
> ⇒ **เลนชุดส่งมอบเปิดครบจริงแล้ว** — cloud/CI อ่านได้ทั้ง 8 ตาราง ไม่มีอะไรค้างรอหน้าสะพานในเลนนี้อีก
> 📌 ของที่ `PF_TAG_CENSUS.tsv` เพิ่งเปิดให้ cloud เห็น (มีผลต่อทุกใบที่เขียน codec): 11 tag แบบ FIXED-len
> `0x05/0x08/0x0B`=1B · `0x0F/0x12`=2B · `0x14/0x19/0x1F/0x26/0x2A`=4B · `0x32`=8B ·
> 🔴 **คอลัมน์ `proven_semantics` เป็น `UNKNOWN` ทุกตัวยกเว้นสองตัว** (`0x12`=uint16 · `0x2A`=float32)
> ⇒ **ห้ามตั้งชื่อชนิดให้ tag ที่เหลือจากความยาวอย่างเดียว** — ความยาวคือความยาว ไม่ใช่ชนิด
> 🔴 คำเตือนที่จดหมาย 20:39 ฝากไว้: **ห้าม whitelist ไฟล์ `.py` ในโฟลเดอร์นี้โดยไม่ตรวจแยกอีกรอบ** —
> `pf_extract_protocol.py` มีสตริงไบต์ฝังเป็นการ์ดค่าคาดหวังมากกว่าในตารางเสียอีก

**ลำดับที่เสนอ (R128):** **GT-053 (ถูกสุด · ชี้ขาด H1) → GT-052 → GT-050** · รายละเอียด H1 อยู่ `FINDINGS_R128_GT051_RENDER_SYNTHESIS.md`
**เพิ่มเติม (R133):** **GT-054 ปลดจาก "รอ merge" เป็น runnable แล้ว** — เป็นใบเดียวในคิวนี้ที่จบด้วยคำสั่งเดียว (`--verify-spans`)
แทรกก่อนหรือขนานใบไหนก็ได้ · ถ้ามีเวลาหน้าสะพานจำกัด แนะนำรัน GT-054 ก่อนเพราะผลของมัน (span ตรง/ไม่ตรง) ตัดสินว่าใบอื่นพึ่งตารางส่งมอบได้แค่ไหน
**เพิ่มเติม (R134):** 🆕 **GT-055 STRING-CODEC-DECISION-001** (ท้ายไฟล์) — cross-check R134 พบโค้ดเรากับตาราง Codex
อ่าน string บน wire คนละแบบ 2 จุด (DeleteActorVital 0x36DB · chat 0xAC52) · จ็อบ 1 เป็น grep capture อย่างเดียว จบเร็ว ·
ผล (ก) ชี้ขาดว่า parser เรามีบั๊กหรือไม่ · รายละเอียด `FINDINGS_R134_EXTERNAL_XCHECK.md`
**สถานะคิว — ถามด้วยคำสั่ง ห้ามอ่านจากบล็อกสรุปที่เขียนด้วยมือ:**

    python tools_bridge/pf_re_queue_taglint.py --list-open
    python tools_bridge/pf_re_queue_taglint.py --list-open --route STATIC-ON-BRIDGE

🔴 **รันบรรทัดแรก (ไม่ใส่ `--route`) ก่อนเสมอ** แล้วค่อยกรอง — คิวนี้มีสามเส้นทาง
(`STATIC-ON-BRIDGE` ต้องมีอิมเมจ/capture บนเครื่องเจ้าของ · `STATIC-ON-CLOUD` cloud clone ทำเองได้ ·
`NEEDS-ATTENDED-CAPTURE` ต้องเปิดเกมจริง) ใครกรองเส้นทางเดียวจะมองไม่เห็นใบของเส้นทางอื่นเลย

เกณฑ์ของคำว่า "เปิด" = มีป้ายเส้นทางตรง · หัวใบไม่ได้เขียนว่าปิดแล้ว · ไม่มีจดหมาย `*RESULT*` ของใบนั้น
ป้าย `OPEN`/`PENDING` ที่พิมพ์มือ **ไม่ใช่** เกณฑ์ (ขึ้นเป็นคอลัมน์ WARNING แทน) — ป้ายที่พิมพ์ตกหล่น
เคยทำให้คิวทั้งคิวเงียบมาแล้วสองครั้งใน 3 วัน (รวม 43 ชม.)

🔴 **บล็อก "สถานะ (R…)" ที่เคยอยู่ตรงนี้ถูกย้ายออกแล้วทั้งบล็อก** (R298, 2026-09-02)
อยู่ที่ `archive/CLIENT_RE_QUEUE_STATUS_LOG_R135_to_R161_20260824_to_0825.md` คำต่อคำ
เหตุผล: บรรทัดสุดท้ายของมันค้างอยู่ที่ 2026-08-25 เขียนว่า "ใบเปิดจริงตอนนี้: RE-065 ใบเดียว"
ซึ่ง **ปิดไปแล้วตั้งแต่ 27 ส.ค.** · prompt ยืนของ Codex สั่งให้อ่าน "บรรทัดล่างสุด = สถานะจริง"
⇒ Codex อ่านแล้วสรุปว่า "คิวว่าง" และหยุด ทั้งที่คิวจริงไม่เคยว่าง
บล็อกสรุปที่ต้องอัปเดตด้วยมือทุกรอบคือของที่จะค้างอีกแน่นอน — ห้ามสร้างขึ้นใหม่

---
## 🆕🔬 GT-052 CLASS-SKILL-TABLE-001 [STATIC-ON-BRIDGE]: ~~dump ตารางอาชีพ + ตารางสกิล~~ ✂️ **ตีความคอลัมน์ + ผูก TEXTDATA + ผูกไอคอน** — ตาราง d... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 GT-050 SKILLCAST-WIRE-001 [STATIC-ON-BRIDGE]: **ตรวจแล้วใช้** (ไม่ใช่ไปถอดใหม่) แถวสกิลจากชุดส่งมอบ RE ของ Codex — verify sha ของ `Trigge... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 GT-053 SCENE2-NATIVE-IDENTITY-CROSSCHECK-001 [STATIC-ON-BRIDGE]: ไฟล์ฉาก native ของ scene 2 มี placement index 60 (`0x203D` Fighting Fish... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 GT-054 SPAN-VERIFY-EXTERNAL-REGISTRY [STATIC-ON-BRIDGE]: รัน span verification ของ reader ตัวใหม่กับอิมเมจ client บนสะพาน — พิสูจน์ span_... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 GT-055 STRING-CODEC-DECISION-001 [STATIC-ON-BRIDGE]: ชี้ขาด "รูปเต็ม" ของ string บน wire 2 จุดที่โค้ดเรากับตารางส่งมอบ Codex ขัดกัน — Del... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-056 SKILLCAST-DIRECTION-002 [STATIC-ON-BRIDGE]: ตัดสินทิศทาง (outbound/inbound) ของ `TriggerCastSkillVital` ด้วยวิธีที่ "ผ่านด่านตัวคว... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-057 PLACEMENT-INDEX-CROSSWALK-001 [STATIC-ON-BRIDGE]: หา binding จริง trigger → สคริปต์ → ฉาก บนเครื่องสะพาน แล้วตัดสินว่า literal ใน ... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-058 LEARNSKILL-DIRECTION-001 [STATIC-ON-BRIDGE]: ตัดสิน natural direction ของ `CLearnSkillVital 0x36AA` — client เคย submit มันเข้าเส้... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-059 ITEMOPERATE-RES-CAPTURE-BYTES-001 [STATIC-ON-BRIDGE]: ดึงไบต์จริงของ 5 เฟรม `ItemOperateVitalRes` ขา R ที่มีอยู่แล้วใน capture cor... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-060 ITEM-TEMPLATE-CODE-SCHEMA-001 [STATIC-ON-BRIDGE]: pin สคีมรหัสไอเทม `<table_code><5 หลัก>` — `table_code` ตัวไหนหมายถึงตาราง CONST... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-061 SKILLSTATE-WIRE-DIRECTION-001 [STATIC-ON-BRIDGE]: ปิด outbound wire shape ของ `CSkillModule` (vtable 0x00F48D88 slot +0x18) แบบไบต... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-062 SKILLATTR-BIND-NULL-BRANCH-001 [STATIC-ON-BRIDGE]: null branch ของ bind thunk `0x4698B0` / target-resolve ใน handler `0x5F2400` — ... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-064 ITEMOPERATE-RES-AFFECTED-ELEMENT-SHAPE-001 [STATIC-ON-BRIDGE]: pin ทรง wire ต่อ element ของ affected-identity ใน ItemOperateVitalR... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-065 ACTORTASK-USEBEHAVIOR-CTOR-WALK-001 [STATIC-ON-BRIDGE]: เดิน ctor ของ `CActorTask_UseBehavior` / `CActorTask_PlayActionEvent` (cus... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-066 GROUNDLOOT-DWORD-IS-IT-READ-001 [STATIC-ON-BRIDGE]: เส้นทางอ่าน list `0x5F85B0` (read path `0x89A640`) **อ่านฟิลด์ `+0x14` แล้วเอา... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-067 NAME-COLOR-SOURCE-001 [STATIC-ON-BRIDGE]: อะไรตัดสิน **สี** ของ ① ป้ายชื่อไอเทมบนพื้น และ ② ป้ายชื่อ actor — และสีนั้นอ่านจาก fiel... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-068 ACTOR-NAMEBOARD-VALUE-034-SEMANTICS-001 [STATIC-ON-BRIDGE]: `board+0x34` ที่ `NameBoardNPC::update` sync เข้า `LABEL_NAME` **แปลว่... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-070 ORCHESTRATOR-TRANSITION-GATE-001 [STATIC-ON-BRIDGE]: **อะไรเป็นตัวเซ็ต MODE `[orch+0x28]`** ของ session/connection orchestrator (v... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-071 SPAWNED-ACTOR-BASICATTR-PROVENANCE-001 [STATIC-ON-BRIDGE]: **actor ที่เกิดจาก `SPAWN_BARE` มี `BasicAttr` อะไรผูกอยู่จริง — และ ct... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-073 TEST-STAGE-GEOMETRY-SURVEY-001 [STATIC-ON-BRIDGE]: **สามฉากที่ addressable และน่าจะโล่ง — วัดเรขาคณิตจริงว่าฉากไหนใช้เป็น "เวทีเทส... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## ✅ RE-075 RETURNSELECT-APPLY-0x5F1190-WHAT-DOES-IT-DO-001 [STATIC-ON-BRIDGE]: apply ของ `ReturnSelectServerVital 0x709E` ที่ VA `0x005F1190` ... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-077 SCENE-TRANSITION-SEQUENCE-001 [STATIC-ON-BRIDGE]: **ไคลเอนต์ต้องการอะไร "ตามลำดับ" เพื่อย้ายตัวละครที่ live อยู่จากฉากหนึ่งไปอีกฉา... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-082 PICKUP-OBJECT-REF-SOURCE-001 [STATIC-ON-BRIDGE]: **dword ที่ไคลเอนต์ก๊อปจาก `[drop-object+0x10]` ตอนคลิกของบนพื้น — มันคือ "คีย์ขอ... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-083 PROJECTED-ACTOR-WALKS-OR-JUMPS-001 [STATIC-ON-BRIDGE]: **ส่ง actor body ของ NPC ที่ project ไว้ซ้ำด้วย "พิกัดใหม่" — ไคลเอนต์ทำให้... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕📊 CLOUD-DERIVED SCENE-ID CROSSWALK (ไม่ใช่ใบ RE — ผลสำรวจ `pf-static-re` รอบ `keen-pasteur-6js9ye` 2026-08-26 ~16:5x (+07:00) ทำจาก `gamedata/tables/*.tsv` ที่ commit แล้ว ไม่ต้องเปิดอิมเมจ)

**[วัดแล้ว]** `gamedata/tables/TEXTDATA_TH__SCENE_NAME_TIP.tsv` (331 แถว คอลัมน์ `n_ID`/`s_SCENE_NAME`/`s_GM_SCENE_NAME`) ให้ชื่อฉาก GM-facing ครบ — Port Royal=1 · Prison Exile Island=2 · Spice Paradise Island=3 · Slave Market Island=4 · Evil Port=5 · Ocean Walled City=6 · Voodoo Island=7 · Silver Harbour=8 · Death City Sea=9 · "Ship in the Sea" (สถานะเรือ ไม่ใช่เกาะจอด) = id 17-23 · "Ship in the Sky" = id 24-30 (มีชุด reskin/mission ซ้ำที่ id 62-73, 186-215, 229) · เกาะ "faction" อีก 13 ใบที่ id 254-270 · เกาะกระจาย/procedural อีกหลายสิบ id (31-61, 74-111, 147-185, 193-253)

**[วัดแล้ว]** ตาราง `CONSTDATA_TH__SCENE_NAME.tsv` (271 แถว, sha256 `e38114a8…` ตรงกับที่ `world_scene_registry_001.json` pin ไว้) ยืนยันชื่อ id 1-4, 17-30 ตรงกับ TIP — แต่ **ขาด 59 id ที่ TIP มี** (รวม id 31, 219) — ยังไม่รู้ว่า client อ่านตารางไหนจริง

**🔴🔴 ข้อควรระวังที่สำคัญที่สุด — อ่านก่อนอ้างเลข id ใดในชุดนี้เป็น wire `scene_id`:** `world_scene_registry_001.json` เขียนไว้เองว่าความเชื่อมโยง `n_ID -> wire scene_id` เป็น **"CANDIDATE, NOT ESTABLISHED"** — พิสูจน์แล้วเฉพาะแถว 1 (Port Royal) และ 2 (Prison Exile Island) เท่านั้น จาก 4 ทฤษฎีที่แข่งกัน (`n_MARKER`, `n_CLINE_TYPE`, row-ordinal, `n_ID` ตรง ๆ) มีแค่สองแถวแรกที่ทุกทฤษฎีเห็นพ้อง ⇒ **id 3, 4, 5-9, 17-30 และทุก id อื่นในตารางนี้ยังไม่ถูกพิสูจน์ว่า = wire scene_id จริง** — `RE-090` (`TeleportVital`/`ForcePos` field layout) คือทางเดียวที่จะปิดช่องว่างนี้ได้ ไม่ใช่การอ่านชื่อคอลัมน์เพิ่ม

**สิ่งที่ยังไม่ตอบ (นอกขอบเขตของการสำรวจนี้ ต้องเปิดอิมเมจ — ดู `RE-085`-`RE-087` ด้านล่าง):** กลไก "กลายเป็นเรือ" · trigger เทียบท่า · packet หน้าต่างรายงานกัปตัน — ตารางชื่อฉากให้แค่ id↔ชื่อ ไม่ให้กลไกใด ๆ

ที่มาเต็ม: `gamedata/tables/TEXTDATA_TH__SCENE_NAME_TIP.tsv` · `gamedata/tables/CONSTDATA_TH__SCENE_NAME.tsv` · `pirate-force-server/scenarios/world_scene_registry_001.json` · `pirate-force-server/src/pirateforce_foundation/world_scene_travel.py`

---

## 🆕🔬 RE-085 SEA-SHIP-TRANSFORM-001 [STATIC-ON-BRIDGE]: **เมื่อผู้เล่นถูกย้ายไป "แมพทะเล" ไคลเอนต์ทำให้ตัวละครกลายเป็นเรือด้วยกลไกอะไร — สลับโม... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-086 ISLAND-DOCK-TRIGGER-001 [STATIC-ON-BRIDGE]: **อะไรทำให้ไคลเอนต์/เซิร์ฟเวอร์รู้ว่า "เรือถึงท่าเกาะแล้ว" — จุดพิกัดคงที่ (เหมือน tra... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-087 CAPTAIN-REPORT-WINDOW-001 [STATIC-ON-BRIDGE]: **packet/UI ของ "หน้าต่างรายงานกัปตัน" ที่ขึ้นตอนเทียบท่า — โครงสร้าง field และปุ่มย... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-088 GM-COMMAND-WIRE-001 [STATIC-ON-BRIDGE]: **layout ของ `GM_RunGMCommandVital` (`0x51E9`, serializer `0x00729E10`, client→server) และ... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-089 GM-STATE-VISUAL-001 [STATIC-ON-BRIDGE]: **`GM_UpdateGMStateVital` (`0x5A19`, handler `0x00729F00`) — ไบต์ไหนคือ is_gm, u32 คืออะไร... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-090 TELEPORT-FORCEPOS-WARP-FIELDS-001 [STATIC-ON-BRIDGE]: **field layout ของ `TeleportVital` (`0x005EB470`), `ForcePos` (`0x005E4250`)... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-091 CHEAT-CHAT-TRIGGER-001 [STATIC-ON-BRIDGE]: **แชทเข้า (client input) ไปถึงการส่ง `GM_RunGMCommandVital` (`0x51E9`) เมื่อไร — มี pre... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-092 REMOTE-ACTOR-LIST-CONSUMER-REPLACE-OR-MERGE-001 [STATIC-ON-BRIDGE]: **ไคลเอนต์อ่านคอลเลกชัน `make_runtime_remote_actors([entry])` ... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-093 BG0001-SERVICE-NPC-PLACEMENT-001 [STATIC-ON-BRIDGE]: **ถอดรหัส placement block ที่สองของ `bg0001.npc` (นอกเหนือจาก "Mob_Set" ที่ d... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-094 NPCCONVERSATION-OP1-GENERIC-SEMANTICS-001 [STATIC-ON-BRIDGE]: **ถอดรหัส op1/op2 ของ `NPCConversation` เป็นกลไกทั่วไป แยกจาก quest-... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-095 NPCCONVERSATION-COLUMBUS-QUESTID-CROSSWALK-001 [STATIC-ON-BRIDGE]: **หา quest id / nested descriptor (u16 `+0x10`, u8 `+0x12`) ที่ NPC Columbus ใช้จริงใน `NPCConversation`, แยกจาก quest `... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-096 VEHICLE-ROW-SEASCENE-CROSSWALK-001 [STATIC-ON-BRIDGE]: **หา `VEHICLE` table row + ความหมายของ `CVehicleVital.+0x18` qword ที่ผูกกับกลุ่มฉากทะเล (`Bg1001`-`Bg1007`, `SCENE_TYPE=4`)**  [🔴 *... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-097 COLUMBUS-BG0001-PLACEMENT-IDENTITY-001 [STATIC-ON-BRIDGE]: **หา placement/actor identity ของ Columbus (`MOBS.n_ID=36`) ใน 149 plac... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-098 FIELD-MOB-DEFINITION-PAYLOAD-LEVEL-RANK-001 [STATIC-ON-BRIDGE]: **หา parser สำหรับ definition payload 16 ไบต์ต่อ `.npc` (`b5`/`b15... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-100 SETNUMBER-99-101-SENTINEL-AND-ACTORMOVE-MULTIPOINT-001 [STATIC-ON-BRIDGE]: **เลขชุด `99`/`101+` ที่แทรกกลางลำดับ `.npc` มีความหมายพิเศษฝั่งไคลเอนต์ไหม + `CActorTask_ActorMove` (ผู้บริโภคท... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-103 SCENE17-BG1001-PLAYER-ARRIVAL-SPAWN-001 [STATIC-ON-BRIDGE]: **หาพิกัด/marker จุดที่ผู้เล่นควรปรากฏตัวเมื่อเข้าฉาก 17 (`Bg1001`, ตระกูลทะเล `n_SCENE_TYPE=4`) — `Bg1001.placements.tsv` มีแค... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-104 GM-EDITOR-WIDGET-OPEN-TRIGGER-001 [STATIC-ON-BRIDGE]: **อะไรเปิด/toggle dedicated GM text-editor widget ที่ `RE-091` พิสูจน์แล้วว่าเป็น producer ของ `GM_RunGMCommandVital` (`0x51E9`) — hot... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-102 NPCCONVERSATION-COLUMBUS-156-QUESTID-3021-WIRE-CONFIRM-001 [STATIC-ON-BRIDGE]: **ยืนยันระดับ wire ว่า descriptor `+0x10`/`+0x12` ของ `NPCConversation` ใช้ quest id `3021` จริงสำหรับ Columb... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-105 GM-UPDATE-STATE-VITAL-VERSION-001 [STATIC-ON-BRIDGE]: **`vital_version` ที่ถูกของ `GM_UpdateGMStateVital` (`0x5A19`) คืออะไร — และ error path ที่ผลิต `網路 VitalData 版本不對 ErrorData=<vital id... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-106 QUEST-FLAG-SYNC-MECHANISM-001 [STATIC-ON-BRIDGE]: **`Quest.GetQuestFlag` อ่านค่าจากไหน — ต้องมี wire vital ส่ง flag state จริงหรือ client เก็บ local ล้วน** [✅ **DONE/PASS — ปิดหัวใบโดย ch... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-107 MOB-DEATH-DYING-DEAD-ANIMATION-DRIVER-001 [STATIC-ON-BRIDGE]: **NAMED+HOSTILE actor_type 4 ที่ HP 0 ไม่ล้มเหมือน GT-022/GT-025 (nameless/factionless) — client ใช้ฟิลด์/เฟรมไหนสั่ง fall/dyi... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-108 SELECT-TARGET-UI-PANEL-REQUIRED-FRAME-001 [STATIC-ON-BRIDGE]: **single-click บน 0x201F ได้ขอบแดง + ลูกศรล็อกแต่ไม่มีแผงเป้า UI (ต่างจาก GT-045 v3) — client ต้องการฟิลด์/เฟรมอะไรจากเซิร์ฟเว... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-109 ACTOR-NAME-COLOR-BYTE-MAP-001 [STATIC-ON-BRIDGE]: **อะไรในเฟรม census/ประกาศคุมสีป้ายชื่อ (ขาว=ตัวเอง, เขียว=ผู้เล่นอื่น, เหลือง/น้ำเงิน=NPC, ส้ม/แดงเข้ม/เทา=มอนตามสถานะ aggro/ตาย, ชมพูขอ... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-110 AUTO-ATTACK-CADENCE-AND-POSE-FRAME-001 [STATIC-ON-BRIDGE]: **เฟรมตอบ ActionVital แบบไหนสั่งท่าโจมตีปกติของ performer และ client ส่ง ActionVital ซ้ำเองเมื่อได้เฟรมตอบแบบไหน (ต่างจากของเราท... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-111 LOOT-DROP-RENDER-REQUIRED-FIELDS-001 [STATIC-ON-BRIDGE]: **client ต้องการฟิลด์อะไรใน `MOB_LOOT_DROP` ถึงจะวาดถุงเรืองแสง+ป้ายชื่อสี rarity บนพื้น — เซิร์ฟเวอร์ส่งไปแล้ว 2 ใบ (54B) แต่เจ้า... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-112 BORNAGAIN-MARKER-RESET-WIRE-ACK-001 [STATIC-ON-BRIDGE]: **หลัง quest 3205 (Q_BORNAGAIN, `Player.ResetMarker(1)`) ถูกเรียก เกมเดิมส่งเฟรมอะไรกลับ (ถ้ามี) — client รอ ack หรือปิด dialog เงี... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-113 GM-UPDATE-STATE-VITAL-NESTED-READER-LAYOUT-001 [STATIC-ON-BRIDGE]: **หลัง `vital_version=0` ผ่านเช็คของ `GM_UpdateGMStateVital` (`0x5A19`) แล้ว nested reader ของ vital นี้เองอ่านฟิลด์อะไรต... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-115 MAPWINDOW-SCENE-NPC-LIST-SOURCE-001 [STATIC-ON-BRIDGE]: **หน้าต่างแผนที่ในเกม (M) มีรายการ "ค้นหาตัวละครในฉาก" เรียง `MOBS.n_ID` ต่อเนื่อง + ปุ่ม GO! — รายการนี้ไคลเอนต์ได้มาจาก packet ของ... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-116 NPC-SPAWN-HEADING-SOURCE-001 [STATIC-ON-BRIDGE]: **actor spawn-time orientation มาจากไบต์/ตารางไหนของไคลเอนต์ (ถ้ามีเลย) — MOB_CENSUS ของเราไม่เคยส่งมันมาก่อน**  [🟢 **CLOSED PASS/DONE — M... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-118 BT-GM-CLICK-DISPATCH-GATE-001 [STATIC-ON-BRIDGE]: **คลิกปุ่ม `BT_GM` แล้วอะไรกันไม่ให้ `GMUI_BASIC` ถูกสร้าง — เดินจาก click handler `0x0053B9B0` → gate `0x0044A3B0` → current-UI-key vfunc... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-117 NPCATTR-LEVEL-MP-BIT-001 [STATIC-ON-BRIDGE]: **BasicAttr bit `0x0002` (level) และช่อง MP cur/max ที่ `PANYA-DECISION 2026-08-28T01:25` ข้อ ③ ให้ไว้ (พิสูจน์บน PC ActorAttr) — มีบิตเดียวกัน... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-119 TRACEPATH-GO-BUTTON-REQREPLY-LAYOUT-001 [STATIC-ON-BRIDGE]: **`CTracePathReqVital` (`0x4391`, ขาไป) กับ `CTracePathVital` (`0x2F92`, ขากลับที่เราไม่เคยส่ง) — ต้องตอบฟิลด์อะไรกลับให้ปุ่ม G... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-122 PLAYER-STANDARD-STATUS-AND-CHARCREATE-SCORE-VALUES-001 [STATIC-ON-BRIDGE]: **ค่า MP current/max และ STR/CON/DEX/INT/PER จริงของตัวละคร level 1 class 1 (Gladiator) คือเท่าไหร่ — ไม่ใช่ตำแหน่ง wire (ปิดแล้ว) แต่เป็นตัวเลข**

> 🔢 หมายเหตุเลข: shared counter (RE/GT ร่วมกัน) สูงสุดที่ใช้อยู่ตอนนี้คือ `GT-121`; grep ยืนยันก่อนเปิดใบ
> (2026-08-28T07:30+07:00): `RE-122`/`GT-122` = 0 hits ใน `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` ⇒ ใบนี้จอง `122`

### ที่มา
CORE-REQUEST-023 รอบ `x6a85q` (R208, ต่อจาก R203/R204 ที่วาง class+level ไว้แล้ว): PANYA-DECISION
`20260828_0125` สั่งให้ตัวละครบูตทุกครั้งต้องมี "probe base 1" ครบ (MP, STR/CON/DEX/INT/PER รวมอยู่ด้วย)
chief ต่อสาย **movement speed** ได้ (owner เคยเห็นค่า 400 บนจอเอง จาก probe fork ของเธอ — client-observable
value, ไม่ใช่ของประดิษฐ์) แต่ **MP/STR/CON/DEX/INT/PER ต่อไม่ได้** เพราะไม่มีค่าตัวเลขจริงใน repo นี้เลย —
ตรวจแล้ว (G1, สองแหล่งอิสระ):
- `reports/PF_JOB001_CHARCREATE_CLASS_STATIC_BOUNDARY_20260816.md`: ตาราง `CHARCREATE_CLASS` มี 37 คอลัมน์
  (ไอคอน/รูปลักษณ์/equipment/`s_SKILL_*`) — **ไม่มีคอลัมน์ `s_SCORE` หรือ stat score ใด ๆ เลย**
- `reports/PF_STATS_PROG001_CHARACTER_STATS_AND_PROGRESSION_STATIC_20260818.md` §8.4: บอกตรง ๆ ว่า
  "the actual per-level curves... remain unknown and would require decoding [external] data files, which
  this milestone did not do" — `STANDARD_STATUS`/`POTENTIAL` มีชื่อคอลัมน์ (`n_STRENGH`/`n_CONSTITUTION`/
  `n_AGILITY`/`n_INTELLECT`/`n_PERCEPTION`/`n_HPMAX`/`n_STAMINAMAX`) แต่ **ไม่เคย decode ค่าจริง**

wire POSITION ของทั้งหกช่องนี้ **ปิดแล้วจริง** (ห้ามทำซ้ำ ใบนี้ไม่ใช่ RE ตำแหน่ง):
- MP current/max: `BasicAttr +0x4C/+0x50`, u32 tag `0x14`, mask `0x0010/0x0020` — ยืนยันสองแหล่งอิสระตรงกัน
  (`RE-117`, disasm ตรง `BasicAttr::Serialize 0x004656F0`; และ `PF_STATS_PROG001` §4 gate `0x465772/0x465786`)
- STR/CON/DEX/INT/PER: `ActorAttr +0x82/0x84/0x86/0x88/0x8A`, u16 tag `0x12`, mask `0x20/0x40/0x80/0x100/0x200`
  (`PF_STATS_PROG001` §5 gate `0x46631F..0x46638A`) — ยังไม่มีแหล่งที่สองยืนยันเฉพาะ 5 ช่องนี้ (แหล่งเดียว G1)

### objective
1. หา `STANDARD_STATUS`/`POTENTIAL` (หรือตารางเทียบเท่า) ใน `gamedata`/`external` ที่ RE-117 เคยค้นแล้วไม่พบ
   คอลัมน์ MP สำหรับมอน — รอบนี้ค้นเฉพาะแถว **ผู้เล่น class 1 (Gladiator) level 1** อาจอยู่คนละไฟล์กับ `MOBS`
2. ถ้าเจอค่าเป็นสูตร (level/class formula) ให้ยืนยันด้วยการคำนวณที่ level 1 ก่อน ห้ามข้ามไปสูตรทั่วไปโดยไม่ยืนยัน
   จุดฐาน (G6: ห้ามประกาศความหมายจากการอ่านครั้งเดียว — ต้องมีสองแหล่งหรือ static+cross-check เหมือน speed)
3. ยืนยัน STR/CON/DEX/INT/PER wire position (`PF_STATS_PROG001` §5) ด้วยแหล่งที่สองอิสระถ้าทำได้ (ตอนนี้มีแหล่งเดียว)
4. ถ้าชนเพดาน static (ต้องใช้ `GameClient.local.bin`/capture corpus ที่คลาวด์นี้ไม่มี) ให้เขียน bounded negative
   แยกข้อ ระบุว่าต้องใช้เครื่องสะพานจริงถึงจะปิดต่อได้ — **ห้ามเดาค่าส่งขึ้น production เด็ดขาด** (RE-117's
   nonclaim #3 วางกฎเดียวกันไว้แล้วสำหรับฝั่งมอน: "ห้ามประดิษฐ์ค่าหรือยืมสูตร PC" — ฝั่งผู้เล่นเองก็ห้ามประดิษฐ์
   เช่นกัน ไม่มีทางลัด)

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว/span SHA) · ชนเพดานให้เขียน bounded negative
แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ค่า MP current/max และ STR/CON/DEX/INT/PER ของ level 1 class 1 พร้อม provenance พอให้ chief เติมลง
`player_wire.py`'s `PLAYER_LOGIN_MOVEMENT_SPEED`-style constants ได้ (wire position พร้อมอยู่แล้ว เหลือแค่ค่า)
**หรือ** bounded negative ที่ชัดเจนว่าต้องใช้เครื่องสะพาน ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**ทำไมมีค่า:** ตัวละครที่บูตวันนี้ MP=0/1 (ไม่เคยส่ง) และไม่มี STR/CON/DEX/INT/PER เลย — ยังไม่ "สมประกอบ"
ตามที่เจ้าของสั่งไว้ใน `PANYA-DECISION 0125` เต็มรูปแบบ (มีแค่ class+level+speed จาก R203/R208) ปิดใบนี้แล้ว
เติมค่าเป็นการแก้ constant บรรทัดเดียวในโค้ดที่มีอยู่แล้ว ไม่ต้องหา wire position ใหม่

---

## 🆕🔬 RE-123 BG0002-MIRAGE-REEL-QUEST-SPAWN-CROSSWALK-001 [STATIC-ON-BRIDGE]: **NPC "Mirage reel" ที่หน้าต่างแผนที่เกาะคุกของเจ้าของแสดงไว้ (ยืนหน้าเต็นท์ Mo Yuzi) มี n_ID ไหน และมันมาจากไฟล์ placemen... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## RE-125 PICKUP-REQUEST-VITAL-ID-001: what wire vital id (opcode) does a real client send when the player left-clicks a ground drop / `PickupTerrainT... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## RE-126 BT-GM-CONTROL-OBJECT-IDENTITY-001: ปุ่ม `BT_GM` ที่ RE-104 พินไว้ ถูกผูกกับ handler `0x0053B9B0` จริงหรือกับ dispatcher ตัวอื่น -- และ `this+0x48` (ประตูบานแรกของ handler) ถูกตั้งค่าจากที่ไห... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-128 SCENE-ORDINAL-TO-MOBS-NID-TABLE-LOCATION-001 [STATIC-ON-BRIDGE]: **ไฟล์/ตารางไหนของไคลเอนต์เก็บ mapping "เลขชุดต่อฉาก (1..115) → `MOBS.n_ID` (ถึง 10,080)" — ตัวที่หายไปทั้งโปรเจกต์ และเป็นตัวเดียวที่ทำให้ Port Royal เกิด NPC ผิดตัวทุกจุด**


> ✅ **RE-128 PASS/DONE — ปิดใบ 2026-08-28T23:48+07:00 โดย LANE-A รอบ `w0pu2i` (เจ้าของใบปิดใบของตัวเอง)**
> สาย RE ตอบครบสองครั้ง: `20260828_1912_RE-128-RESULT-CLINE-CROSSWALK-PINNED.md` (ชั้นตาราง)
> และ `20260828_2314_RE-128-RESULT-DIRECT-AND-INSTANCE-CLINE-SOURCES.md` (เส้นเลือกจริงใน binary)
> สามข้อที่ผู้รับช่วงค้างไว้ **ตอบครบทั้งสามข้อ**: ข้อ 1 (ไคลเอนต์อ่าน CLINE จริง — span
> `[0x0043AA16,0x0043AAA4)` สอง branch) · ข้อ 2 (loop `[0x0043A83E,0x0043A968)` iterate 9 ช่อง leader+crew)
> · ข้อ 3 (กลไกหาฉากอื่น: direct ผ่าน `SCENE_NAME` / instance ผ่าน `INSTANCE`) · ข้อ 4 (`Port transportation`
> ถูกกรองทิ้งใน path นี้เพราะไม่มีแถว MOBS — ไม่ประกาศ semantic ระดับโลก)
> **บริโภคผลครั้งที่สองแล้วในรอบนี้** (stub `.CONSUMED.txt` + สำเนาใน `consumed/`):
> ผล T1 คือเหตุที่ M3 เริ่มที่ **Bg0015** — `SCENE_NAME[Bg0015].n_CLINE_TYPE = 14` เป็นค่าจริง ไม่ใช่
> `0xFFFFFFFF` ⇒ เป็นฉาก direct ไม่ต้องเดา instance id ⇒ `src/pirateforce_foundation/world_bg0015_identity.py`
> (81/91 placement ส่งได้) · ผล T2: ฉากนี้ **0 จาก 51 แถวมี `n_CREW`** ⇒ leader-only ไม่เสียอะไรที่นี่
> · ผล T3: ชุด 1 ของ Bg0015 แปลงได้ 321 ซึ่งก็ไม่มีแถว MOBS เหมือน 155 ⇒ ตัดทิ้งพร้อมเหตุผล
> 🔴 **ที่ยังไม่ปิดไปกับใบนี้ และห้ามอ่านว่าปิด:** nonclaim ทั้งห้าข้อของผล 23:14 — โดยเฉพาะข้อ 1
> (map-list consumer ไม่ใช่หลักฐานว่า runtime spawn actor กี่ตัว) ที่ตอบได้ด้วยตาผู้เทสเท่านั้น
> ⇒ ยกเป็น nonclaim ข้อ 3 ของ `GT-132` ตรง ๆ

> 🟢🔴 **ชั้นตารางตอบแล้ว — LANE-A รอบ `9mtqfv` 2026-08-28T21:4x+07:00 · แต่ใบยัง *ไม่ปิด***
> **คำตอบ: `gamedata/tables/CONSTDATA_TH__CLINE.tsv` · คีย์ `(n_CLINE_TYPE, n_CREATURE_TYPE) → n_LEADER_BK1`
> · ฉากเข้าถึง type ผ่าน `SCENE_NAME.n_CLINE_TYPE` (`bg0001` → type 1)**
> วัดซ้ำเอง: type 1 มี 113 แถวพอดี `n_CREATURE_TYPE` = `1..113` ครบไม่ขาด ตรงกับ `template_ids` ของ `bg0001` ·
> identity 0/113 ใน type 1 (ทั้งตาราง 35/3,599 และทั้ง 35 อยู่ใน type 2) · **สมอเจ้าของเข้าทั้งสองจุด:**
> index 1 → template 2 → **156 Columbus** · index 65 → template 67 → **802 Loie** (ใบ `20260827_0950_PANYA-DECISION-*`)
> 🔴 **ยังไม่ปิดเพราะ:** ยังไม่ได้พิสูจน์ว่าไคลเอนต์อ่าน CLINE ตอนโหลดฉากจริง (ชั้นตารางล้วน ๆ · ต้องใช้เครื่องสะพาน) ·
> `bg0001`/`Bg0002` บังเอิญมี `n_CLINE_TYPE == n_ID` ⇒ แยก "อ่านคอลัมน์" กับ "อ่าน `n_ID`" ไม่ออกที่สองฉากนี้ ·
> 6 จาก 107 ค่า leader ของ type 1 ไม่มีใน `MOBS.n_ID` (`0,155,819,937,942,9107`) ยังไม่มีคำอธิบาย
> nonclaim ครบหกข้อ + หลักฐานเต็ม: `notes_to_chief/20260828_2140_LANE-A-FINDING-RE-128-crosswalk-is-CONSTDATA-CLINE.md`
>
> 🔁 **ใบนี้ย้ายมือแล้ว: LANE-A → สาย RE** ตาม `20260828_2130_COO-DECISION-evidence-order-and-re128-handoff.md`
> ข้อ 5 (กำหนดตอบ **2026-08-29 12:00** · ผลลบก็ปิดใบได้) · **สาย A วางมือตั้งแต่รอบ `9mtqfv`**
> ผลข้างบนคือของที่สาย A หาได้ **ก่อน**คำสั่งย้ายมือจะถึง ส่งต่อไว้เป็นจุดตั้งต้น **ไม่ใช่การถือใบต่อ**
> 🔴 **สิ่งที่ผู้รับช่วงควรทำต่อ (สาย A ไม่ทำแล้ว):** ข้อ 1 พิสูจน์ว่าไคลเอนต์อ่าน CLINE ตอนโหลดฉากจริง
> (ต้องใช้ binary บนเครื่องสะพาน — เป็นเหตุผลเดียวที่ใบยังไม่ปิด) · ข้อ 2 **หนึ่ง placement เกิดกี่ตัว**
> (leader อย่างเดียว หรือ leader+crew) · ข้อ 3 กลไกหาฉากอันที่สอง · ข้อ 4 `Port transportation` เป็นตัวคั่นหรือเกิดได้
>
> 🔴🔴 **ผ่าน `pf-adversary` แล้ว — ข้อหลักรอด แต่มีสามอย่างที่ผู้รับช่วง *ห้าม* หยิบไปใช้ (สาย A เขียนผิดเอง):**
> ① สถิติ "19 ฉาก 0 violation" **ใช้ไม่ได้** — กฎที่ไม่อ่านฉากเลย (`type 9998` ตายตัว) ได้ 0/19 เท่ากัน
> ② เลข "7 ฉากเท่ากันพอดี" ที่ถูกคือ **9** · "140 resolve" ที่ถูกคือ **142** · "type 2 ct = 1..35" **ผิด**
> (ที่ถูก `1..41 ∪ {101..104}` · เฉพาะส่วน identity ที่เป็น 1..35)
> ③ **สมอสองจุดไม่ได้ pin การจัดเรียง** — แมพเลื่อนหนึ่งช่องให้ 156/802 เหมือนกัน · ตัวที่ pin จริงคือ
> **พิกัด XYZ** + brute force 49,028 คู่คอลัมน์ที่เหลือคู่เดียว
> 🔴🔴 **และข้อที่ต้องให้เจ้าของเคาะก่อนใครแตะ roster: จำนวนไม่ใช่ 115 ไม่ว่าอ่านทางไหน**
> (149 / 142 / 147 / 153 / 101 — ไม่มี 115) **และ id ที่ทับกับโรสเตอร์เดิม = 0 ตัว** ⇒ รับ CLINE
> = ตัวตนเปลี่ยนทั้ง 115 ตัวพร้อมกัน · **สมอครอบคลุม 2 จาก 39 บล็อก · ด่าน 7 anchor ยัง 2/7 ยังไม่ผ่าน**
> รายละเอียดครบใน §⑦-⑧ ของจดหมาย FINDING

> 🟩 **บริโภคผลแล้ว — LANE-A รอบ `pqx4fj` 2026-08-28T22:4x+07:00** (ผู้เปิดใบบริโภคผลของตัวเอง ตาม ADDENDUM v2 ข้อ B)
> ผลที่บริโภค: `notes_to_chief/20260828_1912_RE-128-RESULT-CLINE-CROSSWALK-PINNED.md` (สาย RE local, 19:12 —
> **มาถึงก่อนคำสั่งย้ายมือ 21:30**) · เอาไปใช้จริงแล้วเป็นโค้ดที่ลงสาย ไม่ใช่รายงาน:
> `src/pirateforce_foundation/world_port_royal_identity.py` (ตาราง crosswalk ทั้งฉาก 105 แถว + 8 แถวที่ปฏิเสธ)
> และ `world_population.py` ส่ง `MOBS.n_ID`/`s_OUTFIT`/ชื่อจาก `MOBS_TIP` แทนเลขชุด — **PR pf_bridge#325 / server รอบเดียวกัน**
> 🔴 **สาย A ไม่ได้ถือใบคืน** งานที่เหลือของใบ (nonclaim 4 ข้อข้างบน) ยังเป็นของสาย RE ตามใบ 2130 ข้อ 5 ทุกประการ ·
> สิ่งที่สาย A ทำคือ *ใช้ผล* ไม่ใช่ *ขุดต่อ* · แต่ขอบันทึกให้ผู้รับช่วงเห็นชัด: **ข้อ 1 (ไคลเอนต์อ่าน CLINE จริงไหม)
> กำลังจะถูกตอบด้วยตาผู้เทสในใบ `GT-131`** ⇒ ถ้า `GT-131` ผ่าน ใบนี้ปิดได้ด้วยหลักฐานชั้น client-observable
> โดยไม่ต้องรอ static บน binary

> NUMBERING NOTE: ร่างไว้เป็น `RE-126` ตอนต้นรอบ แต่สาย GM รอบ `hs9m2r` merge `RE-126`+`GT-127` เข้า main
> ก่อน ⇒ ตามกฎ "ชนแล้วห้ามทับ" ใบสาย GM อยู่ที่เดิม ใบนี้ขยับเป็น **`RE-128`** (สูงสุดบน main = 127)

🔴🔴 **ผลลบข้อ "ค้น `gamedata\` แล้วไม่เจอ" ของใบนี้ *ผิด* — แก้โดยเจ้าของใบ LANE-A รอบ `9mtqfv`
2026-08-28T21:2x+07:00 · เขียนดัง ๆ เพราะมันคือสิ่งที่ทำให้ทั้งโปรเจกต์เดินข้ามตารางตัวจริงมาหลายรอบ**
ตัว mapping **อยู่ใน `gamedata\` มาตลอด extract แล้ว commit แล้ว และมีอยู่ใน `PF_GAMEDATA_COLUMNS.tsv`**
คือ **`gamedata/tables/CONSTDATA_TH__CLINE.tsv`** (3,599 แถว 19 คอลัมน์) · ไม่มีใครเคย **join** มันเท่านั้นเอง
🔴 objective ข้อ 1 ที่เขียนว่าผู้สมัครคือ "ตาราง `CONSTDATA`/`TEXTDATA` ที่ **ยังไม่ extract**" คือถ้อยคำที่
ทำให้ CLINE ถูกมองข้าม — **มันถูก extract แล้ว** ⇒ รอบถัดไปห้ามอ่านผลลบข้อนี้แล้วข้าม `gamedata\` อีก

~~**ค้นใน `pf_bridge\external\` แล้ว: ไม่เจอ** แถวที่ผูกเลขชุดของไฟล์ฉากกับ `MOBS.n_ID` ·~~
~~**ค้น `gamedata\` แล้ว: ไม่เจอตัว mapping** (เจอแต่ปลายทางสองข้าง)~~ · ผลลบที่ปิดแล้วในรอบ `iyhrj0`
กันเสียรอบซ้ำ: `CONSTDATA_TH__MOBS.tsv` **ไม่มีคอลัมน์ฉาก** (~~`n_ID_MAP` = 0-7~~ 🔴 **วัดใหม่รอบ `9mtqfv`:
`n_ID_MAP` = 0-5 หกค่า ไม่ใช่ 0-7**, `n_MOB_APPEAR` = 1/0 เท่านั้น ทั้งคู่ไม่ใช่ scene id — **ข้อสรุปไม่เปลี่ยน
ยังปิดอยู่** แก้เฉพาะตัวเลขที่คลาดเคลื่อน)

### ทำไมเปิดใบนี้ (LANE-A รอบ `iyhrj0`, 2026-08-28T17:40+07:00)
**ช่องว่างเชิงตัวเลขที่บังคับให้ตารางนี้ต้องมีอยู่:** วัดครบทั้ง **266 ฉาก** — `template_ids` **ไม่เคยเกิน 115**
แต่ `MOBS.n_ID` เดินถึง **10,080** ⇒ เลขชุดเป็น **ordinal ต่อฉาก ไม่ใช่ id ระดับเกม** ⇒ **ต้องมีตารางแปลง
(ฉาก, เลขชุด) → `n_ID` อยู่นอกไฟล์ฉาก** และยังไม่มีใครในโปรเจกต์หามัน

ทุกวันนี้เราใช้ **identity map** แทน (`เลขชุด = n_ID`): `current/pf_login_game_server_v141.py:1323`
`PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` 115 แถว (สร้างโดย `tools/pf_mine_scene_mob_roster.py`) — **ถูกสำหรับ
`Bg0002`** (เจ้าของยืนยันทั้งฉาก M1-P 28 ส.ค.) **แต่ผิดสำหรับ `bg0001`** (`GT-078` OWNER-REJECTED) ⇒
คำถามจริงคือ **"ทำไม identity map ถูกสำหรับฉาก 2 แต่ผิดสำหรับฉาก 1 และตัวจริงอยู่ที่ไหน"** ·
`GT-078` addendum §3.2 (26 ส.ค.) สั่งให้เปิดใบ *"placement index → NPC identity ของ bg0001"* ไว้เอง
แต่ **ไม่เคยถูกเปิดจริง** — ใบนี้คือใบนั้น

### จุดตั้งต้นที่รอบ `iyhrj0` วัดไว้แล้ว (รายละเอียดเต็ม + provenance อยู่ใน
`notes_to_chief/20260828_1740_LANE-A-FINDING-bg0001-crosswalk-is-not-an-offset.md` และ
`archive/rounds_2026-08-27_to_28/A_20260828_1740_iyhrj0_bg0001_identity_not_an_offset.md` — ที่นี่เก็บเฉพาะข้อที่เปลี่ยนวิธีทำงานของใบนี้)
1. แถว `Port transportation` (`n_ID` 37/66/104/155/195/249/284/321/361/398 — มีใน `MOBS_TIP` ไม่มีใน
   `CONSTDATA`) เป็น **ตัวคั่นบล็อก** ⇒ `1-36 | 38-65 | 67-103 | 105-154 | 156-194 | …` ·
   **156-194** อ่านเป็นโรสเตอร์บริการของ Port Royal (lvl 10-20)
2. 🔴 **ห้ามใช้เหตุผล "ฉากนี้ต้องอยู่บล็อกเดียว"** — โรสเตอร์ `Bg0002` ที่เจ้าของยืนยันแล้วกิน **4 บล็อก**
   (template `1..41` + `101..104`) · รอบ `iyhrj0` ร่างเหตุผลแบบนั้นแล้วโดน adversary ตีตก เขียนกันคนถัดไปเดินซ้ำ
3. 🔴 **ยังไม่มีสมอของ `bg0001` ที่ใช้ได้เลย** — Hields (`159`) รู้ว่าเป็นตัวไหนแต่ **ไม่รู้ placement index** ·
   Sase (`796`) แถวนั้นระบุเองว่า **`[stated]` จากความทรงจำเจ้าของ ห้ามเลื่อนขั้นถ้าไม่มีเฟรม** (และเป็น
   lvl 105-110 ไม่เข้ากับลานระดับ 11) ⇒ **ห้ามใช้ 796 คำนวณ offset**

### 🔄 อัปเดตโดยเจ้าของใบ (LANE-A รอบ `o8cy9q`, 2026-08-28T18:41+07:00) — ได้ **ผลลบหนึ่งข้อ** และ **คำเตือนหนึ่งข้อ** · คำถามหลักของใบ **ไม่เปลี่ยน**

🔴 **ตัดออกจาก objective ข้อ 2 ได้เลย: `u16_6` ปิดแล้ว (ผลลบ)** — วัดในรอบ `o8cy9q`: `u16_6` เดินในช่วง
**1..149** ระดับเดียวกับ `index` ของแถว (สลับตำแหน่งบ้าง ไม่เท่ากับ `index` เป๊ะ) ⇒ **ไปไม่ถึงบล็อก 156-194
และไปไม่ถึง `n_ID` 10,080** ⇒ ไม่ใช่คีย์ crosswalk **ห้ามเปิดผู้สมัครนี้ซ้ำ**

🔴🔴 **คำเตือนถึงคนถัดไปที่หยิบใบนี้ — กับดักที่รอบ `o8cy9q` เดินลงไปแล้วและถอนออกมา**
รอบนี้ลองสร้างกฎว่า *"เลขชุดเป็น `n_ID` จริงเฉพาะฉากที่ให้เลขแบบโปร่ง (มีเลขขาด) · ฉากที่ให้เลขแบบ
หนาแน่น (`1..N`) เป็น ordinal"* — **`pf-adversary` ตีตกทั้งก้อน ถอนแล้ว ห้ามสร้างใหม่** เหตุผลสามข้อ
ที่ทำซ้ำได้เอง:
1. **กลุ่มเปรียบเทียบถูกเลือกด้วยตัวแปรตาม** — "หนาแน่น" นิยามว่า `max == จำนวนชุด` แล้วไปเลือกกลุ่มด้วย
   `max ∈ 102-115` ⇒ ฉากจะหนาแน่นได้ต้องมี ≥102 ชุด · พี่น้องมี 40-64 ชุด ⇒ **"โปร่ง 14 จาก 15" เป็น
   เลขคณิต ไม่ใช่หลักฐาน**
2. **ตัวอย่างบวกตัวเดียวที่มี หักล้างกฎเอง** — `Bg0002` = `{1..41} ∪ {101..104}` · **เขตที่เจ้าของยืนยัน
   คือ `1..41` ซึ่งหนาแน่น** · ที่มันถูกนับว่า "โปร่ง" มาจาก `101-104` ล้วน ๆ ซึ่งเป็นสี่เลขที่
   **เจ้าของสั่งห้ามเดา** และ `scene2_prison_exile_tables.py` ส่งเป็น UNRESOLVED อยู่
3. **ด้านกลับพังในวงกว้าง** — ฉากภายในเล็ก ๆ หลายสิบฉาก "โปร่ง" เพราะขาดเลข `3` ตัวเดียว ⇒ กฎนี้จะ
   อนุญาตให้ส่งคณะเกาะคุกเข้าไปในฉากพวกนั้น

**คำอธิบายที่ดีกว่า มีอยู่ในกล่องจดหมายตั้งแต่ 27 ส.ค. แล้ว และอยู่ชั้นหลักฐานที่สูงกว่า (client-observable):**
`20260827_1240_PANYA-EVIDENCE-video2-Port-Royal-NPC-tour-*` — หน้าต่างแผนที่ไล่ NPC ของ Port Royal
ตาม `n_ID` **156, 157, 158, …** และตาราง 32 ตัวยืนยันช่วง **156-913** พร้อมบรรทัด **"ไม่มีตัวใดจากบล็อก 1-35"**
⇒ `n_ID` ถูกจัดสรร **เป็นบล็อกต่อภูมิภาค** · เกาะคุกถือบล็อกล่าง · Port Royal ถือ 156+ และ 600-900 ·
**ทุกไฟล์ฉากไล่เลขชุดของตัวเองจาก 1** ⇒ ที่ `Bg0002` ดูเหมือน `เลขชุด = n_ID` เป็นเพราะบล็อกของภูมิภาคมัน
เริ่มที่ 1 พอดี ⇒ **เลขชุดของทุกฉากเป็น ordinal** · ใต้คำอธิบายนี้ `bg0001` (เลขหยุดที่ 113) ไม่มีทาง
ชี้ไปยังโรสเตอร์ที่อยู่ 156-913 ได้ — **พอแล้วสำหรับอธิบาย `GT-078` โดยไม่ต้องมีทฤษฎีเรื่องการไล่เลขเลย**

**คำถามที่ใบนี้ยังต้องตอบ (ไม่เปลี่ยนเลย):** ตาราง `(ฉาก, ordinal) → n_ID` อยู่ไฟล์ไหน ·
🔴 **และห้ามสมมติว่ามีฉากไหนไม่ต้องใช้ตารางนี้** — รอบ `o8cy9q` เคยเขียนว่า "ฉากโปร่งไม่ต้องใช้" ถอนแล้ว

### objective (ไล่จากถูกไปแพง อย่าข้ามขั้น)
1. **ชั้นข้อมูลก่อน (ถูกที่สุด):** หาตาราง/ไฟล์ที่ให้ "รายชื่อ NPC ต่อฉาก" หรือ "(ฉาก, ordinal) → `n_ID`" ·
   ผู้สมัครที่ยังไม่มีใครเปิด: ตารางที่ **หน้าต่างแผนที่ (M)** ใช้สร้างรายชื่อ NPC ต่อฉาก (เจ้าของยืนยันว่ามันโชว์
   ครบทุกฉาก รวม Mirage Reel ที่เราไม่ได้ส่ง) · `.lua` ต่อฉาก · ตาราง `CONSTDATA`/`TEXTDATA` ที่ยังไม่ extract
2. **ชั้นไฟล์ฉาก:** `.npc` ถูก parse ครบหรือยัง (`*.placements.tsv` เป็นผล parse ของ record ไบนารีความยาว
   ไม่คงที่) · ~~โดยเฉพาะ **`u16_6`** (147 ค่าไม่ซ้ำใน 149 แถวของ `bg0001` ไม่เท่ากับ `index`) ยังไม่มีใครตรวจ~~
   🔴 **`u16_6` ตรวจแล้วและปิดแล้ว (ผลลบ) รอบ `o8cy9q`** — ช่วง `1..149` ไปไม่ถึง `n_ID` ดูบล็อกอัปเดตข้างบน
3. **ชั้น wire (แพงสุด ทำต่อเมื่อ 1-2 ตัน):** ไล่หา **โค้ดที่เขียนค่าลง `u16@+0x14` ของ
   `CTracePathReqVital` ก่อน send** (ctor `0x006EBA90` แค่ zero ฟิลด์; registry แถว 378 ser `0x006EBAF0`)
   ซึ่ง `RE-119` T4 ทิ้งไว้เป็น bounded negative สามทาง · ถ้าเป็น `MOBS.n_ID` ปุ่ม GO! จะกลายเป็นแหล่ง
   crosswalk ฝั่งไคลเอนต์ · **ห้ามใช้เลข 743 เดิมตัดสิน** ตามที่ `RE-119` สั่ง

### กติกาบังคับ (เหมือนทุกใบ static)
อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (แถว/คอลัมน์/offset/VA/SHA) · ชนเพดานให้เขียน bounded negative
แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB/source/คิวของสายอื่น

### เกณฑ์จบใบ
ระบุที่อยู่ของ mapping พร้อม provenance พอให้สาย A สร้างตาราง `bg0001` ตัวจริงได้ **หรือ** bounded negative
ที่บอกชัดว่าชั้น 1-2 ปิดแล้ว เหลือแต่ชั้น 3 ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**ปลดล็อกถ้าเป็นบวก:** `GT-078` ที่ค้าง OWNER-REJECTED ตั้งแต่ 26 ส.ค. · โรสเตอร์ตัวจริงของ Port Royal
⇒ **M1 ของเมืองหลัก**

## RE-129 FORCE-POS-VITAL-VERSION-001: ไบต์ `vital_version` ของ `ForcePos` (`0x0E80`) ที่ client ยอมรับคือค่าอะไร -- prototype constructor ของ vital น... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## ✅🔬 RE-130 GROUND-LABEL-LIST-MEMBERSHIP-001 [STATIC-ON-BRIDGE] — **CLOSED / DONE-PASS · บริโภคแล้วโดย LANE-B รอบ `zxnwtd`**: **ป้ายชื่อไอเทมบนพื้นผูกกับการที่ element ยังอยู่ในลิสต์ `0x08` (object+`... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## RE-132 GM-GLOBAL-MESSAGE-VITAL-VERSION-001 [ARCHIVED 2026-08-31 R274, closed >24h per หัวข้อ 11] -- moved verbatim to `archive/CLIENT_RE_QUEUE_ARCH... -- (stub เก่า R274) ถูกย้ายรอบ 20260906 ไป `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md` 🔴 **แต่เนื้อใบจริงอยู่ที่ `archive/CLIENT_RE_QUEUE_ARCHIVE_20260831_R274_closed.md` ไม่ใช่ไฟล์ 20260906** (ไฟล์นั้นเก็บได้แค่ stub นี้ — แก้ถ้อยคำที่ชี้ผิดโดย chief รอบ `6z131u`-b ตาม pf-adversary D12)

## 🆕🔬 RE-135 CP874-CENSUS-ARTIFACT-REGEN-001 [STATIC-ON-BRIDGE]: ลบ `U+1F534` ตัวสุดท้ายใน `tools/pf_vital_thunk_census_static.py` แล้ว regenerate artifact ในคอมมิตเดียวกัน  [PENDING]

> NUMBERING: จองเลข `133` ตอนเปิดรอบ (grep = 0 hit ทั้งสองไฟล์) แต่ระหว่างรอบ **สาย GM merge `RE-132` + จอง `GT-133`**
> และ **สาย A merge `GT-134`** เข้า main ก่อน ⇒ ตามกฎ "ชนแล้วห้ามทับ" ใบนี้ขยับเป็น **`RE-135`**

**ADDRESSEE: RE runner (คนหน้าเครื่องสะพาน)** · ผู้เปิดใบ: chief (สาย E) รอบ `apk7ue` (R217) 2026-08-29T00:1x+07:00
**ต้นเรื่อง:** `notes_to_chief/20260828_2315_LANE-A-NOTICE-two-tools-files-break-the-cp874-tripwire.md`
+ คำตอบ `notes_to_chief/20260829_0010_CHIEF-REPLY-LANE-A-cp874-two-tools-files-never-reach-print.md`

**คำถามที่ใบนี้ปิด:** ไม่มีคำถาม — เป็นงานเก็บกวาดที่ **ทำบนคลาวด์ไม่ได้เชิงกลไก** ไม่ใช่เชิงกฎ

**ทำอะไร** (บน repo `pirate-force-server` ที่มี `GameClient.local.bin`):
1. แก้ `tools/pf_vital_thunk_census_static.py` บรรทัด 235 — แทน `U+1F534` ด้วย ASCII (`!!` หรือคำว่า `RED`)
   สตริงนี้อยู่ใน `artifact_payload()["__doc__"]` ⇒ **มันจะเปลี่ยนไบต์ของ artifact ที่ commit ไว้**
2. รัน `py -3 tools/pf_vital_thunk_census_static.py --emit <artifact เดิม>` เพื่อ regenerate
   (เครื่องมือเทียบ payload กับไฟล์ที่ commit ไว้ **ไบต์ต่อไบต์** ที่บรรทัด 465-470 — ไม่ regenerate = FAIL ทันที)
3. ลดพินใน `.github/workflows/gate-windows.yml` ตาราง `ALLOWED`:
   `"tools/pf_vital_thunk_census_static.py": 3` → ค่าที่เหลือจริงหลังแก้ (พินเป็นสองทาง ลดอักขระโดยไม่ลดพิน = เกตแดง)
4. รัน `py -3 -m pytest tests/test_tree_is_cp874_safe.py -q` ให้เขียวก่อน push (ด่านนี้อ่านพินจาก workflow เอง)

**ทำไมคลาวด์ทำเองไม่ได้:** ขั้น 2 ต้องมีอิมเมจ client ซึ่งไม่มีบนคลาวด์ตลอดกาล
(จดใน `IMAGE_ACCESS_COST.tsv` แถว `vital-thunk-census/cp874-cleanup` แล้ว)

**เกณฑ์ผ่านสองชั้น**
- wire/DB: `py -3 tools/pf_vital_thunk_census_static.py` ออก `PASS - all guards reproduced` เหมือนเดิมทุกบรรทัด
  และ `git diff` ของ artifact มีเฉพาะบรรทัด `__doc__` ที่เปลี่ยนอักขระ ไม่มีตัวเลข census เปลี่ยน
- client-observable: **ไม่มีชั้นนี้** — ไม่แตะพฤติกรรมเซิร์ฟเวอร์ ไม่ต้อง `OBSERVER_CONFIRMED`

**🔴 ไม่บล็อกใคร:** อักขระตัวนี้ไม่เคยถูก `print()` (วัดแล้ว ดูจดหมาย 0010) เกตก็เขียวอยู่เพราะพินไว้แล้ว
⇒ ใบนี้เป็นงานเก็บกวาด ทำเมื่อสะดวก ห้ามแซงใบที่บล็อกไมล์สโตน

## 🆕🔴 RE-136 MOBS-ANSWER-AS-NPC-DISPATCH-001 [STATIC-ON-CLOUD]: คลิกซ้ายบน hostile roster placement ถูกเซิร์ฟเวอร์ตอบด้วย **เลนคุย NPC** แทนเลนต่อสู้... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🆕🔬 RE-137 NPCCONVERSATION-54B-WHOSE-SCRIPT-001 [STATIC-ON-CLOUD]: เฟรม 54 ไบต์ที่ `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` ส่ง -- de... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-138 NAME-LABELS-VANISH-AFTER-MOVE-001 [STATIC-ON-CLOUD]: ป้ายชื่อ (เขียว) ของทุกตัวในแมพหายหลังผู้เล่นเดินออกจากบริเวณแรก เหลือแต่ป้ายฉายา (ฟ้... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-139 P33-P58-IDENTITY-CONTRADICTION-001 [STATIC-ON-CLOUD]: บูตเดียวส่ง **ตัวตนสองชุดที่ขัดกัน** ให้ placement เดียวกัน -- สำมะโนบอกว่า Babu/Juliet ตาราง roster บอกว่า Fighting Fish soldier/Jung... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-149 PORT-ROYAL-FIVE-COSTUMELESS-LEADERS-001 [STATIC-ON-BRIDGE]: ห้าตัวที่ Port Royal "แต่งตัวให้ไม่ได้" -- ไคลเอนต์เอา `s_OUTFIT` ของ CLINE leader `155 / 819 / 937 / 942 / 9107` มาจากไหน หรือม... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-150 AGGRO-PLACEMENT-OUTSIDE-REFUSED-BLOCKS-001 [STATIC-ON-BRIDGE]: หา placement ที่ AI เริ่มตีเอง (aggro) นอกบล็อก 101-104 ที่เจ้าของสั่งห้ามวาง -- จาก artifact ที่ commit แล้วเท่านั้น  [✅ DO... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-152 PORT-ROYAL-HARBOUR-NEEDS-A-SOURCE-001 [STATIC-ON-BRIDGE]: ท่าเรือของ Port Royal (`placement 0` / CLINE leader `155` "Port transportation") ต้องมาจากไหน -- ในเมื่อ `RE-149` ปิดทางเดิมไปแล้ว... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-154 CHOOSENPC-ANSWERS-FOR-UNANNOUNCED-ACTORS-001 [STATIC-ON-BRIDGE]: **ตัวตอบ `ChooseNPC` ตอบคลิกให้ identity ฮาร์ดโค้ดโดยไม่ตรวจฉาก และไม่ตรวจว่า actor นั้นเคยถูกประกาศให้ไคลเอนต์หรือยัง** [... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-155 ACTOR-NAME-COLOR-NPC-VS-HOSTILE-MOB-ONE-FIELD-CROSSWALK-001 [NEEDS-ATTENDED-CAPTURE]: เจ้าของสั่ง "NPC เขียว→เหลือง" + "Training Iron Man ควรชื่อแดง" -- static ชนเพดานเรื่องนี้แล้วสามใบ ต้องมี capture เปลี่ยนทีละฟิลด์จึงตอบต่อได้  [🟢 **OPEN — เปิดโดย LANE-A รอบตรวจ 20260830 จากคำสั่งเจ้าของ GT-131 หมวด ③**]

> 🔢 grep ยืนยันก่อนจอง 2026-08-30: `RE-155`/`GT-155` = 0 hit ทั้งสองไฟล์ · สูงสุดก่อนหน้า `RE-154`
> (+ `GT-152`/`PROMOTE-153`) ⇒ ใบนี้คือ `155` · ใบ `RE-085`-`RE-154` ห้ามลบ/ย้าย/แก้ถ้อยคำ

### ที่มา

`notes_to_chief/20260830_0030_KA3A-GT131-...-four-polish-gaps...md` หมวด ③ ข้อ 1-2 (เจ้าของ, GT-131
PASS 00:2x): (1) ชื่อ NPC ทุกตัวขึ้น**สีเขียว** (สื่อว่าเป็นผู้เล่นอื่น) ควรเป็น**สีเหลือง** (2) หุ่นซ้อม
**Training Iron Man** (`template_id 916`) ควรเป็น**มอนชื่อแดง**แต่ยังไม่ใช่ · ส่งมอบสาย A/B ใน
`FROM_CHIEF_R236_TO_ATTENDED_20260830_0855.md` ข้อ ②

**คำถามเดียวกับที่ `RE-067`/`RE-068`/`RE-109` ปิดเป็น BOUNDED-NEGATIVE ไปแล้วทั้งสามใบ**: `RE-067` ไม่พบ
direct read ของ `NPCAttr faction+0x68`/relation comparator/`FONT_COLOR` loader ใน `NameBoardNPC::update`
ที่ decode ครบ · `RE-068` เดิน `board+0x34` จนสุดแล้วพบว่าไม่ใช่สี (เศษ countdown หน้าสร้างตัวละคร) และ
`FONT_COLOR` caller เดียวมาจาก resource-init ไม่ใช่ actor render · `RE-109` (ปิด 2026-08-27T18:15,
CFG 485/503 instructions) ออก **`BUILD_IMPACT: NONE — ห้าม hard-code สีจาก actor_type/faction 1-6/
FONT_COLOR ID/n_SKIN_COLOR จนกว่าจะมี attended one-field crosswalk`** ตรงตัว

### ตรวจซ้ำแล้วรอบนี้ [MEASURED, source-only, ไม่เปิดเกม]

- `population.py:23 NPC_STYLE_ACTOR_TYPE = 4` — ทุก NPC ส่ง `actor_type=4` อยู่แล้ว ตรงกับที่ `RE-109`
  pin ว่า `actor_type=4` → `CNetNPC`/`NameBoardNPC` (คนละคลาสจาก `actor_type=3` → `NameBoardPlayer`)
  ⇒ สีเขียวไม่ได้มาจาก actor_type ผิด ช่องว่างอยู่ใน logic เลือกสีของ `NameBoardNPC` เอง — จุดเดียวกับที่
  ทั้งสามใบชนเพดาน static
- `field_mob_tables.py:96-99 TOWN_TARGET_PLACEMENTS` (`n_ID=916` ×4) ยูเนียนเข้า `field_mobs.
  load_roster()` (บรรทัด 125) แล้ว ⇒ `mob_death.full_roster_override` ที่ `runtime.py` เรียกทุกบูตฉากบ้าน
  (ไม่มีแฟล็ก) สไปลซ์ faction hostile ให้ Training Iron Man **ทุกบูตอยู่แล้ว** — สไปลซ์เดียวกับ `GT-032`
  ที่ `field_mobs.py` docstring เขียนเองว่า "predicted and observed NO red name label, because that
  frame carried no name bit at all" ⇒ ส่ง faction bytes ซ้ำแบบเดิมไม่มีเหตุผลให้เชื่อว่าจะได้ชื่อแดง
- ⇒ **ไม่มี field ที่รู้ค่าแล้วเหลือให้ต่อสายในนี้** — เจ้าของต้องการค่าที่ยังไม่มีใครวัด ไม่ใช่ค่าที่วัดแล้ว
  แต่ยังไม่ได้ wiring

### objective (ตามที่ `RE-109` เสนอเป็น method ceiling ถัดไป แต่ยังไม่มีใครเปิดใบ)

1. **NPC**: A/B บน identity NPC ที่ตั้งชื่อถูกแล้วตัวเดียวกัน (เช่น placement ที่ GT-131 ยืนยัน) — คงทุก
   ฟิลด์เดิม เปลี่ยนทีละหนึ่งค่า เริ่มจากฟิลด์ที่ `RE-109` ยังไม่ตัดทิ้ง (`CONSTDATA_TH__FACTION.tsv` 38
   แถว ค่านอกช่วง 1-6) · ถ่ายภาพทุกสถานะ เทียบภาพฐาน GT-131 (`ScreenShot\20260830_00{0311,0741,
   1047,1423}.png`)
2. **Mob**: บน Training Iron Man (ได้ faction bytes อยู่แล้วทุกบูต) ลองฟิลด์ที่ยังไม่เคยตัดทิ้งทีละตัว
   แยกให้ชัด "ไม่เคยส่ง" กับ "ส่งแล้วแต่ client ไม่ใช้ตัดสินสี" (ข้อหลังคือสิ่งที่วัดแล้วสำหรับทุกฟิลด์
   จนถึงตอนนี้)

### pass criteria

- wire/DB: ฟิลด์ที่ทดลองแต่ละตัว + ค่าก่อน/หลัง
- client-observable: ภาพคู่ก่อน/หลังต่อฟิลด์ — หลักฐานเดียวที่ปิดใบนี้ได้ (สามใบก่อนหน้าเดินไม่ถึงชั้นนี้)
  **หรือ** bounded-negative ระบุรายการฟิลด์ที่ลองแล้ว

### nonclaims

1. ไม่อ้างว่าฟิลด์ไหนจะได้ผล 2. ไม่เปิด `RE-067`/`RE-068`/`RE-109` ซ้ำ 3. **ห้าม src/ เขียนสีแบบเดา**
ก่อนใบนี้ได้ผลบวก — `BUILD_IMPACT: NONE` ของ `RE-109` ยืนจนกว่าใบนี้จะมีผลแทน 4. ผลลบไม่ต้องเปิด `GT-*`
แยก — บันทึก bounded-negative แล้วส่งเจ้าของว่าเป็นเพดานข้อมูลไคลเอนต์

### links

`RE-067`/`RE-068`/`RE-109` (ปิดแล้ว ห้ามรันซ้ำ) · `src/pirateforce_foundation/field_mobs.py`
(docstring "What decides name colour...") · `src/pirateforce_foundation/mob_death.py`
(`WIDENING_RULINGS` 916) · `src/pirateforce_foundation/population.py:23`
(`NPC_STYLE_ACTOR_TYPE`) · `notes_to_chief/20260830_0030_KA3A-GT131-...` หมวด ③ ·
`notes_to_chief/FROM_CHIEF_R236_TO_ATTENDED_20260830_0855.md` ข้อ ②

---

## 🆕🔬 RE-156 SCENE-IDENTITY-SIGNAL-001 [STATIC-ON-BRIDGE]: **ไม่มีสัญญาณที่เชื่อถือได้ว่าไคลเอนต์กำลังเรนเดอร์ฉากไหนจริง** [~~🟢 OPEN~~ 🔵 **DONE (wire/DB layer) / POSITIVE-CANDIDATE-OUT-OF-DOMAIN-AND-U... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-157 UNANNOUNCED-ACTOR-SINK-GATES-TRADECMD-AND-MOBCOMBAT-001 [STATIC-ON-BRIDGE]: **สอง sink gate ที่ RE-154 บอกว่า "ปิด ChooseNPC แล้วอย่าคิดว่าจบ"** [~~🟢 OPEN~~ ~~🔵 DONE (analysis) / TWO SOUR... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-161 CORPSE-POSE-APPLIES-AT-NEXT-RECOMPOSE-NOT-AT-DEATH-FRAME-001 [STATIC-ON-BRIDGE]: **ทำไมโมเดลไม่ล้มตอนได้เฟรมตาย แต่ล้มตอนคิลถัดไปมาถึงแทน** [~~🟢 OPEN — เปิดโดย LANE-B รอบ `qb1ytr` 2026-08... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-163 MOB-LOOT-DROP-LATE-MS-SOURCE-001 [STATIC-ON-BRIDGE]: **เฟรม `MOB_LOOT_DROP` มาถึงช้า 351-949ms — ช้าเพราะอะไร ไม่ใช่ตำแหน่งคิว** [~~🟢 OPEN — เปิดโดย LANE-B รอบใหม่ (scheduled) 2026-08-30T... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-162 IN-SESSION-SCENE-CHANGE-WIRE-001 [STATIC-ON-BRIDGE]: **ไบต์ไหนสั่งให้ client เปลี่ยนแมพขณะออนไลน์ (ไม่ผ่านล็อกเอาต์)** [~~🟢 OPEN~~ 🔵 **DONE / MIXED — ปิดโดย chief รอบ `bunu7v` (R246) 2026... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-164 BT-GM-CLICK-FOUR-SUSPECTS-002 [CLOSED เฉพาะ**ชั้น static** ครบสี่ข้อ (#2 มีชั้น attended ด้วย) — ~~#1 STATIC-PARTIAL~~ ปิดโดย `RE-164 RESU... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`) 🔴 **ค้างจริง: ข้อ #2 ของใบมีชั้น attended ที่ยังไม่มีใครวัด** (chief รอบ `6z131u`-b ตาม pf-adversary D6) — ใครหยิบต่อ เปิดใบ GT ใหม่ อย่าถือว่าจบไปกับ RE-164

## 🔬 RE-167 CENSUS-FRAME-INTERMITTENT-ABORT-001 [~~OPEN — assigned LANE-A~~ 🔵 **wire/DB ANSWERED bounded-negative, client-observable STILL PENDING — LANE-A รอบ `qoj8ei` 2026-08-31T11:36+07:00, ผล `notes_to_chief/20260831_1136_RE-167-RESULT-wire-layer-no-server-buffer-timeout-cause-found-bounded-negative.md`: ไม่พบ server-side buffer/timeout/race ที่อธิบาย 10053 ได้ จาก static analysis; chunking ต้องแก้ frozen `current/pf_login_game_server_v141.py` ซึ่งเป็นไฟล์ที่ทั้งโปรเจกต์ตกลงห้ามแก้ — ส่งเป็นคำถามเชิงโครงสร้างให้ chief/COO ตัดสิน ไม่ใช่ CORE-REQUEST ปกติ; ยังไม่มี fix ให้เทส จึงยังไม่เปิด GT ใหม่**]: เฟรม `WORLD_CENSUS_INITIAL` ขนาด ~20 KB (Port Royal, 108-115 actor) ทำสายไคลเอนต์ขาดเป็นครั้งคราว (`ConnectionAbortedError 10053`) — เกิดที่จุดไหนของ send/parse และทำไมไม่เกิดทุกครั้งบนเฟรมขนาดเท่ากัน

### หลักฐานตั้งต้น
`notes_to_chief/20260831_1036_GT106R2-RESULT-PASS-client-renders-the-destination-scene-mid-session-plus-two-new-findings.md`
(ของใหม่ข้อ 1) — สามจุดข้อมูล: Port Royal 20,112B ครั้งแรกสายขาด (`10053`) ครั้งถัดมาผ่านทั้ง
INITIAL/REAPPLY, Slave Market (BG0004) 18,997B ขึ้นข้อความ "ยังไม่สามารถรับข้อมูล Server ได้" แต่เล่นต่อได้
— **เกิดเป็นครั้งคราวบนเฟรมขนาดเท่ากัน ห้ามเขียนว่า "20 KB พังเสมอ"**

### ที่มา
ก่อนหน้านี้ Port Royal ส่ง actor แค่ 3 ตัว (`V134_P0_P30_P91_ISOLATED`) ตอนนี้ส่ง 108/115 — เฟรมโตจาก
หลักร้อยไบต์เป็น ~20 KB เป็นผลข้างเคียงของงานสำมะโนที่เพิ่งลง main ไม่ใช่บั๊กเก่าที่เพิ่งโผล่

### จุดที่ยังไม่แน่ชัด
1. ฝั่งเซิร์ฟเวอร์ (`runtime.py`/`app.py` ส่ง `WORLD_CENSUS_INITIAL`): มี buffer/timeout ใดที่ทำให้ send
   ถูก abort เป็นบางครั้งบนเพย์โหลดขนาดนี้ — ตรวจ log บริเวณจุด send ว่ามี retry/partial-write หรือไม่
2. ฝั่งไคลเอนต์ (จากข้อสังเกต ไม่ใช่ disassembly ใหม่): ไคลเอนต์อ่านเฟรมสำมะโนเป็นก้อนเดียวหรือแบ่งอ่าน —
   ถ้าไม่มี client image ให้ตอบจาก log ฝั่งเซิร์ฟเวอร์ + เอกสารโปรโตคอลที่ commit แล้วเท่านั้น
3. ควรแบ่งเฟรมสำมะโนใหญ่เป็นหลายก้อน (chunking) หรือไม่ — ถ้าตอบได้จาก static analysis ให้เสนอ threshold
4. ผลลบก็เป็นคำตอบ: ถ้าสรุปได้ว่าเป็นเงื่อนไข race ฝั่งเน็ตเวิร์กที่ไม่มีทางแก้จากโค้ดเซิร์ฟเวอร์ ให้ปิดเป็น
   bounded-negative พร้อมเหตุผล

### pass criteria — สองชั้น แยกกันเด็ดขาด

**ชั้น wire/DB (ปิดใบนี้ได้บางส่วน):** คำตอบต่อข้อ 1-4 จาก static analysis ของซอร์ส/log ที่ commit แล้ว
พร้อมเลขบรรทัด — ผลลบก็เป็นคำตอบ

**ชั้น client-observable (ใบนี้ตอบไม่ได้ ต้องมีคนหน้าจอ):** เปิด GT ใหม่ถ้าต้องยืนยันว่า fix (เช่น chunking)
แก้อาการ 10053 จริงในเซสชันยาว — สาย A เปิดใบเมื่อมีของให้เทส

### ข้อห้าม
🔴 **ห้ามแก้ด้วยการลดจำนวน actor เงียบ ๆ** — นั่นคือถอยหลังจากงานสำมะโนที่เพิ่งทำสำเร็จ (ตามที่ผู้เทสเน้นไว้
ในใบต้นเรื่อง) · ห้ามอ้างว่าพบสาเหตุแท้จริงจากการอ่าน log ครั้งเดียว (G1) · 🔴 **CHARTER-02 §⑥**:
`WORLD_CENSUS_INITIAL` ถูกประกอบ/ส่งจาก `runtime.py` (`src/pirateforce_foundation/runtime.py:8096`) ซึ่งเป็น
เขตของ chief คนเดียว — ถ้าคำตอบชั้น wire/DB สรุปว่า fix (เช่น chunking) ต้องแก้ใน `runtime.py`/`app.py`/
`pf_login_game_server_v141.py` **LANE-A ห้ามแตะไฟล์เหล่านั้นเอง** ให้เปิด CORE-REQUEST ขอ chief ต่อสายแทน
ตามกติกาเขตเขียนปกติ

### สัญญาผู้บริโภค
ผู้เปิดใบเป็นผู้บริโภคผล (LANE-A) ตามกฎ "ใครเปิดใบคนนั้นบริโภค" — มอบหมายโดย chief รอบ `iby4ui` ตามคำขอ
ของกะ1-A ในใบต้นเรื่อง (ADDRESSEE เดียวต่อใบ)

### links
`notes_to_chief/20260831_1036_GT106R2-RESULT-PASS-client-renders-the-destination-scene-mid-session-plus-two-new-findings.md`

## 🔬 RE-168 SCENE-TRANSITION-UI-LAYER-NOT-RESET-001 [~~OPEN — assigned LANE-A~~ 🔵 **wire/DB ANSWERED partial, client-observable STILL PENDING — LANE-A รอบ `qoj8ei` 2026-08-31T11:42+07:00, ผล `notes_to_chief/20260831_1142_RE-168-RESULT-no-dialogue-close-signal-exists-server-is-stateful-enough-to-add-one.md`: เฟรม `kind=clear` ที่มีอยู่เป็น population เท่านั้น ไม่มีช่องปิด UI; เซิร์ฟเวอร์จำสถานะ conversation ได้จริง (`columbus_quest3021_conversation_sent`) แต่ไม่มี opcode ปิด dialogue ที่ characterize แล้วในเขตนี้ — เปิดใบใหม่ให้สาย RE หา opcode ก่อน; ยังไม่มี fix ให้เทส จึงยังไม่เปิด GT ใหม่**]: หน้าต่างบทสนทนา NPC (Columbus quest 3021) ค้างอยู่บนจอหลัง teleport ข้ามฉาก ทั้งที่ actor ถูกล้างแล้ว (`population=none`, เฟรม `kind=clear` ยิงก่อน teleport) — ชั้น UI ควรถูกสั่งรีเซ็ตตอนไหน และตอนนี้เซิร์ฟเวอร์ส่งสัญญาณนั้นหรือไม่

### หลักฐานตั้งต้น
`notes_to_chief/20260831_1036_GT106R2-RESULT-PASS-client-renders-the-destination-scene-mid-session-plus-two-new-findings.md`
(ของใหม่ข้อ 2) — เจ้าของรายงานตรง ๆ ว่า "หลังวาร์ปไปฉาก 17 ภาพ/หน้าต่างบทสนทนาของ Columbus ยังค้างอยู่บนจอ"
รายละเอียดเฟรม `WORLD_M2_CROSSING_HANDOFF kind=clear ... slot=before_teleport ... held=108` มาจากจดหมาย
คู่กันบูตเดียวกัน (`notes_to_chief/20260831_1037_GT148-and-GT165-RESULT-stowaways-cleared-and-slave-market-island-has-life.md`
บรรทัด ①) ไม่ใช่ใบ 1036 **คนละชั้นกับที่ `GT-148` ถาม** (`GT-148` ถามเรื่อง actor ค้าง — ตามใบ 1037 สาย A
เจ้าของใบรายงานว่าจะปิดเป็น PASS เอง แต่ ณ เวลาที่เขียนใบนี้ `GAME_TEST_QUEUE.md` ยังขึ้น PENDING (สาย A
ยังไม่ปิดหัวใบจริง) — ใบนี้ถามเรื่อง UI ค้าง ซึ่งเป็นชั้นคนละอันแม้ทริกเกอร์เดียวกัน ไม่ขึ้นกับผลของ `GT-148`)

### จุดที่ยังไม่แน่ชัด
1. เฟรม `kind=clear` ที่มีอยู่แล้ว (`WORLD_M2_CROSSING_HANDOFF`) สั่งล้างเฉพาะ actor หรือมีช่องสั่งปิด UI
   ด้วย — ถ้าไม่มี ต้องมีเฟรม/สัญญาณแยกสำหรับปิด dialogue window
2. การเปิดหน้าต่างบทสนทนา Columbus มาจากจุดเสียบไหน (`CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE`
   ตามที่ log ใบต้นเรื่องแสดง) — จุดเสียบเดียวกันควรมีคู่ปิดหรือไม่
3. เป็นปัญหาฝั่งเซิร์ฟเวอร์ (ไม่ส่งสัญญาณปิด) หรือฝั่งไคลเอนต์ (ได้สัญญาณแต่ไม่ทำตาม) — ตอบจาก wire/log
   ที่ commit แล้วเท่านั้น ถ้าต้องอ่าน client behavior ให้ตอบเป็น bounded-negative ว่าตอบไม่ได้จากฝั่งนี้
4. ผลลบก็เป็นคำตอบ: ถ้าเซิร์ฟเวอร์ไม่มีทางรู้ว่า dialogue window เปิดอยู่ (stateless ฝั่งนี้) ให้ปิดเป็น
   bounded-negative พร้อมเสนอทางแก้ (เช่น ผูก dialogue-close เข้ากับ `kind=clear` เดิม)

### pass criteria — สองชั้น แยกกันเด็ดขาด

**ชั้น wire/DB (ปิดใบนี้ได้บางส่วน):** คำตอบต่อข้อ 1-4 จาก static analysis ของซอร์ส/log ที่ commit แล้ว

**ชั้น client-observable (ใบนี้ตอบไม่ได้ ต้องมีคนหน้าจอ):** เปิด GT ใหม่เพื่อยืนยันว่า fix ปิดหน้าต่างจริง
หลัง teleport — สาย A เปิดใบเมื่อมีของให้เทส

### ข้อห้าม
ห้ามนับเป็น FAIL ของ `GT-148` (ตามใบ 1037 ผลชั้น actor เป็นบวก — ไม่มี actor ค้าง — ไม่ว่าหัวใบจะถูกปิด
เป็น PASS เมื่อไหร่ก็ตาม) · ห้ามอ้างว่ารู้พฤติกรรม client รวมโดยไม่มี client image/capture ยืนยัน ·
🔴 **CHARTER-02 §⑥**: ถ้าคำตอบชั้น wire/DB สรุปว่าต้องผูกสัญญาณปิด UI เข้ากับเฟรมที่ `runtime.py`/`app.py`
ประกอบ **LANE-A ห้ามแตะไฟล์เหล่านั้นเอง** ให้เปิด CORE-REQUEST ขอ chief ต่อสายแทน

### สัญญาผู้บริโภค
ผู้เปิดใบเป็นผู้บริโภคผล (LANE-A) — มอบหมายโดย chief รอบ `iby4ui` ตามคำขอของกะ1-A ในใบต้นเรื่อง (ใบใหม่
ไม่ใช่ส่วนขยายของ `GT-148`)

### links
`notes_to_chief/20260831_1036_GT106R2-RESULT-PASS-client-renders-the-destination-scene-mid-session-plus-two-new-findings.md` ·
`notes_to_chief/20260831_1037_GT148-and-GT165-RESULT-stowaways-cleared-and-slave-market-island-has-life.md`

## 🔬 RE-169 NPC-DIALOGUE-CLOSE-OPCODE-001 [🔴 **CLOSED bounded-positive-with-caveats — ปิดโดยผู้เปิดใบ (chief) รอบ `uy54tw` (R313) 2026-09-03T03:1x+07:00 จากผลชั้น IMAGE ของ RE runner บนสะพาน ใบ `notes... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-170 BG0005-SCENE-LEVEL-CONTROL-MEDIAN-GAP-001 [🔴 **CLOSED bounded-negative — ปิดโดยผู้เปิดใบ LANE-A รอบ `rdhel6` 2026-09-01T08:4x+07:00, ดูผลด้านล่าง**]: `world_bg0015_identity.SCENE_LEVEL_CON... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-171 BG0006-CJK-TELEPORTER-NAME-001 [🔴 **CLOSED bounded-negative — ปิดโดยผู้เปิดใบ LANE-A รอบ `trig7s` 2026-09-01T02:4x+07:00, ดูผลด้านล่าง**]: `world_bg0006_identity.py` (ฉาก 6, Ocean Walled C... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-172 ACTOR-BASIC-ATTR-LOGIN-OBSERVABLE-SOURCE-001 [~~OPEN — assigned สาย GM~~ 🔵 **DONE (wire/DB layer) / BOUNDED-NEGATIVE — ปิดโดยผู้เปิดใบ (สาย GM) รอบ `thhkup` 2026-08-31T23:26+07:00, กระตุ้น... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## ✅ RE-173 PRISON-EXILE-COLUMBUS-MOBS-ID-36-VS-360-001 [STATIC-ON-BRIDGE]: **`world_m2_sea_destination.COLUMBUS_ROUTES` บอกว่า Prison Exile (home scene 2)'s Columbus คือ MOBS n_ID 360 แต่ `scene2_pri... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-188 PRISON-EXILE-BULLETIN-BOARD-CROSSWALK-CONTRADICTION-001 [STATIC-ON-BRIDGE]: RE-173's own method, applied to the other 96 `Bg0002` placements, resolves four Mob-Set numbers to CLINE leaders... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-189 LOGOUT-TRANSITION-ORCHESTRATOR-WRITER-OF-PLUS18-001 [STATIC-ON-BRIDGE]: `RE-070` dumped the 31-slot vtable of `0xF45030` and named 4 writers of MODE (`+0x28`)/its timer pair (`+0x24`) - bu... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## RE-133 FIELD-MOB-AI-TABLES-BG0015-REGEN-001 [OPENED-IN-ERROR, CLOSED same round -- see correction below] regenerate `field_mob_ai_tables` for Bg0015 (`chief รอบ ts0deo` (R282)) -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-191 MONSTER-NAME-COLOR-FONTSTYLE63-RGB-001 [STATIC-ON-BRIDGE]: `CODEX_CHECKPOINT 20260901_1135` closed the same-actor conditional static path... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-193 ACTORATTR-SEVEN-UNKNOWN-FIELDS-CLIENT-DEFAULT-VALUES-001 [STATIC-ON-BRIDGE]: what does the client itself write, at object-creation time, into the 7 `ActorAttr` fields (of 55 total in `gm/a... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-194 BASICATTR-0X54-SPEED-PLAYER-VS-NPC-CONFLICT-001 [STATIC-ON-BRIDGE]: `BasicAttr+0x54` (f32, mask `0x0040`, tag `0x2A`) has two different [M... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-195 FONTSTYLEID-RELATIONSHIP-PREDICATE-VS-FACTION-COMPARATOR-001 [STATIC-ON-BRIDGE]: does `UILabel_FontStyleID_parser_setter`'s `relationship_predicate` (`0x0043C380..0x0043C63C`) read the sam... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-196 RETURNSELECTSERVERVITAL-FIELD3-TAG-BYTE-001 [STATIC-ON-BRIDGE]: field 3 (the string field, object `+0x20`) of `ReturnSelectServerVital` (0x709E) -- is there an instruction that writes a ta... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-197 GETWORLDINFOVITAL-51-BYTE-FRAME-001 [STATIC-ON-BRIDGE]: เฟรม `GetWorldInfoVital` 51 ไบต์ (`[G< #1398]`) ที่อยู่ระหว่างปุ่ม "กลับหน้าเลือกตัวละคร" กับปุ่ม "ออกจากเกม" คือรูปแบบย่อของอะไร แล... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-198 UPDATEATTRVITAL-VITAL-VERSION-BYTE-001 [STATIC-ON-CLOUD] [🔵 **DONE / BOUNDED-NEGATIVE — ปิดโดย chief รอบ `happy-dirac-69cabr` 2026-09-01T21:19+07:00, ดูผลด้านล่าง**]: `UpdateAttrVital` (0x... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-201 BG0001-PORT-ROYAL-MINED-LEVEL-COLUMN-001 [**CLOSED ANSWERED-IN-ROUND / OPENED-IN-ERROR** -- ปิดหัวใบโดย LANE-A (เจ้าของใบ) รอบ `7ste68` 2026-09-02T02:5x+07:00 ในรอบเดียวกับที่เปิด · **ไม่ต... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-202 QUEST-ICON-BOARD-SKIP-GATE-0X70-OWNER-001 [CLOSED -- ตอบ **ข. `CNetNPC+0x70`** โดย LANE-A (ผู้เปิดใบ = ผู้บริโภคผล) รอบ `8z9h9n` 2026-09-02T10:35+07:00 · ใบผล **สองใบ**: `notes_to_chief/20... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-206 TELEPORTVITAL-STRING-TAG-MISMATCH-190-AUX-PRESENCE-001 [DONE/PASS -- ปิดโดย chief (LANE-E) รอบ `kt05o0`/R305 2026-09-02T16:0x+07:00 ตามใบผล `20260902_1052_RE-206-RESULT-AUX-PRESENCE-ZERO-O... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-208 GROUND-POOL-REMOVAL-PATH-FOR-THE-LAST-OBJECT-001 [OPEN -- เปิดโดย LANE-B รอบ `9jrsei` 2026-09-02T09:5x+07:00 · ผู้ทำ: **สาย RE** (ผู้ทำสายเดียว ไม่ต้องจอง) · **LANE-B บริโภคผลเอง** · `STATIC-ON-CLOUD`]

**คำถามเดียวของใบนี้: มีข้อความที่ถอน "ของบนพื้น" ทีละชิ้นไหม หรือ generation ที่ไม่ว่างคือทางเดียว**

ที่รู้แล้ว ห้ามขุดซ้ำ: `RE-082` (ปิด PASS 2026-08-26) พิสูจน์กับ `PickupTerrainThing` list consumer ว่า
**generation ที่ไม่ว่าง ลบทุกคีย์ที่มันไม่ได้พูดถึง** และ **generation ที่มีศูนย์แถวเป็น no-op** ·
`RE-130` ใช้ข้อเท็จจริงเดียวกันจนกลายเป็นกติกาของ `mob_loot`

**ช่องว่างที่เหลือ และเหตุที่มันสำคัญเดี๋ยวนี้:** ถ้าฉากมีของชิ้นเดียวแล้วผู้เล่นเก็บมันขึ้นมา
แถวที่เหลือคือศูนย์ ⇒ generation ศูนย์แถวลบมันไม่ได้ (no-op) ⇒ ทางเดียวที่เหลือคือปล่อยให้เฟรม
derived-mask-ว่าง ล้างพื้นทั้งฉากทิ้ง ซึ่งเป็นสิ่งที่ P-1 กำลังไล่ปิดทีละจุด (`COO 0646` opt-in)
⇒ ถ้าปิดครบทุกจุดโดยไม่มีคำตอบของใบนี้ **ของชิ้นสุดท้ายจะค้างเป็นของผีบนพื้นตลอดไป**

**เกณฑ์ปิดใบ (สองชั้น)**
- ชั้น static: ในภาพไคลเอนต์ ระบุว่า reconciler ของ TerrainThingPool (`0x006AF970` ตามใบ Codex
  `CODEX_URGENT_20260901_0324`) มีเส้นทาง **remove-by-key / destroy-one** ที่ถูกเรียกจากข้อความอื่น
  หรือไม่ · ถ้ามี: VA + ชื่อ vital/opcode + รูปร่างเพย์โหลด · ถ้าไม่มี: บอกว่า **ไม่มี** และเส้นทาง
  การถอนที่มีจริงคืออะไรบ้าง (พร้อม VA)
- ชั้นที่สอง: ตอบด้วยว่า generation ที่ไม่ว่าง **หนึ่งแถวที่ไม่ใช่ของเดิม** (เช่นแถว dummy) ถูกใช้
  ถอนของจริงได้หรือเปล่า หรือมันจะกลายเป็นวัตถุใหม่บนพื้นแทน

**ทำไมใบนี้ไม่บล็อกงานของสาย B วันนี้:** สายเดินต่อด้วยคำตอบที่ดีที่สุดของตัวเอง (ประกาศแถวที่เหลือ
เป็นหนึ่ง generation หลังเก็บของสำเร็จ ซึ่งถูกต้องแน่นอนเมื่อยังมีของเหลือ) และหยุดเฉพาะเคสชิ้นสุดท้าย
ไว้ตามพฤติกรรมวันนี้ จนกว่าใบนี้จะตอบ — ติดป้าย `[สมมติของสาย B - รอ COO ยืนยัน]` ไว้ในโค้ดแล้ว

**อัปเดต 2026-09-02T12:5x+07:00 (LANE-B รอบ `lh21ua` · ยังไม่ปิดใบ):** ครึ่งที่ไม่ต้องรอใบนี้ **สร้างแล้ว** —
`DropLedgerCell.frames_after_a_row_left` (server `mob_loot.py`) ประกาศแถวที่เหลือของฉากหลัง pickup สำเร็จ
และ `dispatch_inbound_pickup_request` คืนให้เป็น `outcome.ground_after` ⇒ **ช่องว่างที่เหลือของใบนี้แคบลง
เหลือเคสเดียวจริง ๆ**: ฉากที่ของชิ้นสุดท้ายถูกเก็บไป (เหลือศูนย์แถว) ซึ่งวันนี้ไม่ส่งอะไรเลยและปักไว้ด้วยเทส
`TheLastObjectIsHeldAndSaysSo` · ตอบใบนี้เมื่อไร สาย B เสียบต่อได้ทันทีที่จุดเดียว

**อัปเดต 2026-09-02T13:5x+07:00 (LANE-B รอบ `ewq4js` · ยังไม่ปิดใบ · แคบลงอีกครึ่งใบ):** ~~"ถ้าปิดครบทุกจุด
โดยไม่มีคำตอบของใบนี้ ของชิ้นสุดท้ายจะค้างเป็นของผีบนพื้นตลอดไป"~~ **ไม่จริงอีกต่อไป** จุด opt-in ที่สาม
(`mob_pickup.bag_delta_pc`) ปิดแบบ **มีเงื่อนไข**: preserve เฉพาะเมื่อฉากยังเหลือแถว · เหลือศูนย์แถวเมื่อไร
เฟรมนั้นยังใช้ derived mask ว่างของ v141 ตามเดิม **โดยตั้งใจ** ⇒ พื้นที่ว่างจริงถูกล้าง = ป้ายของชิ้นสุดท้าย
หายจากจอในเฟรมเดียวกับที่ของเข้ากระเป๋า โดยไม่ต้องมีข้อความใหม่บนไวร์ (ปักด้วยเทส
`test_the_last_object_clears_the_floor_and_says_that_instead`)
🔴 **คำที่ถูกคือ "ทางเดียวที่ถอนโดยตั้งใจ ในคำตอบเดียวกัน" ไม่ใช่ "ทางเดียวในโปรเจกต์"** (pf-adversary รอบ
`ewq4js` D3): ตาราง cadence ของ `mob_combat` เองมี bar/dying/dead ที่ล้างพื้นทุกครั้งที่ตีไม่ตาย
**คำถามของใบนี้ยังต้องการคำตอบ** สำหรับเคสที่เหลือ: ฉากที่ **ยังมีแถวเหลือ** แต่ removal publication ปฏิเสธ
(คอนโซลพิมพ์ `MOB_PICKUP_GROUND_REMOVAL_REFUSED` + `MOB_PICKUP_DELTA_GROUND_CLEARED`) — เคสนั้นยัง
ต้องรอ generation ถัดไปเหมือนเมื่อวาน · และถ้าคำตอบคือ "มี remove-by-key" เคสนี้กับเคสชิ้นสุดท้ายจะเลิกพึ่ง
การล้างพื้นทั้งฉากทั้งคู่

**อัปเดต 2026-09-03T18:46+07:00 (LANE-B รอบ `j8qsxp` · ยังไม่ปิดใบ · แก้การระบุเฟรมหนึ่งข้อ):**
ใบผล R306 (`notes_to_chief/20260903_1657` cross-lane ข้อ 1) เสนอว่าอาการ "ของหายตอนตี แล้วโผล่กลับตอนมันตาย"
คือ roster re-send ล้างพื้น **แล้ว ground section ของเฟรมตายเอากลับมา** ⇒ **ชี้ถูกชุด แต่ผิดเฟรม**
ขับดิสแพตเชอร์จริงบน **ฉาก 2 พร้อมของหนึ่งชิ้นยืนบนพื้นจริง** (`server tests/test_mob_combat_dispatch_bg0002_kill.py::
test_a_hit_that_does_not_kill_leaves_the_floor_cleared_behind_it`):
หมัดที่ **ไม่ฆ่า** = `ANNOUNCE`(ground) + `MOB_COMBAT_BAR` ~18KB (ไม่มี ground) เป็นตัวสุดท้าย **และไม่มี generation
ของพื้นเลย** ทั้งที่แถวยังมีชีวิตใน ledger ของเซิร์ฟเวอร์ · หมัดที่ **ฆ่า** = `ANNOUNCE` + `DYING` + `DEAD`
(สองตัวหลัง **ไม่มี ground section**) + `MOB_LOOT_DROP` (ground ติด · ledger ทั้งฉาก) เป็นตัวสุดท้าย
⇒ ตัวคืนพื้นคือ **เฟรมดรอปในชุดเดียวกัน ไม่ใช่เฟรมตาย** · 🔴 ไม่ใช่ heartbeat ~2 วิ (pool present + count 0 = no-op
ตามการอ่าน `RE-082` ซึ่งเป็น `STATIC-ON-BRIDGE` ไม่ใช่ชั้นไคลเอนต์) · 🔴 เฟรมดรอปไม่ใช่ผู้ประกาศพื้นรายเดียว —
`mob_loot.enter_scene_frames` ตอนข้ามฉากก็ประกาศรูปเดียวกัน · 🔴 **ที่วัดคือลำดับในลิสต์** ลำดับบนสาย/ที่ไคลเอนต์
apply ยังไม่มีใครดู · 🔴 **ใบ R306 เขียนว่า "บางทีหาย บางทีไม่หาย" — แบบจำลองนี้เป็น deterministic จึงยังอธิบายไม่ได้**
🔴 **คำถามของใบนี้ไม่เปลี่ยน** (remove-by-key มีหรือไม่มี) — ที่เปลี่ยนคือ **ห้ามใครอ้างเฟรมตายเป็นตัวถอน/ตัวคืนอีก**

- links: `RE-082` · `RE-130` · `COO-DECISION 20260902_0253` (ห้ามลบแถว ledger จนกว่ามี removal publisher)
  · `notes_to_chief/20260902_0943_LANE-B-REPORT-COO-0646-announce-site-opted-in-bag-delta-held-for-a-removal-publisher.md`
- ค้นใน `pf_bridge\external\` แล้ว: (สาย RE กรอก) · ค้น `gamedata` แล้ว: (สาย RE กรอก)
- numbering: ใบนี้เปิดเป็น `206` ตอน 09:5x แล้ว **ขยับเป็น `208`** ตอน merge ตามกฎ ③ (คนที่ push ทีหลังขยับ): ระหว่างรอบเดียวกัน chief merge `RE-206` (TeleportVital) และ `GT-207` ขึ้น main ⇒ สูงสุดใหม่ = 207 ⇒ `208` · grep `RE-208` ทั้งรีโปพบเฉพาะใบนี้
- result: (สาย RE กรอก: มี/ไม่มี · VA + สแปน + ที่มา · timestamp)

## 🔬 RE-209 QUEST-SETTER-PROLOGUE-11-BYTES-ESI-PROVENANCE-001 [OPEN **ย่อเหลือ 2 ไบต์** -- เปิดโดย LANE-A รอบ `8z9h9n` 2026-09-02T11:0x+07:00 · **ย่อขอบเขตโดย LANE-A รอบ `f6e5kd` 2026-09-03** หลังบริโภคใบผล `notes_to_chief/20260902_1039_RE-202-RESULT-CNETNPC-RUNTIME-BIT-NOT-BASICATTR.md` · ผู้ทำ: **สาย RE** (ผู้ทำสายเดียว ไม่ต้องจอง) · **LANE-A บริโภคผลเอง** · 🔴 `[STATIC-ON-BRIDGE]` ต้องดิสแอสเซมบลีอิมเมจ ⇒ ทำบนคลาวด์ไม่ได้]

> 🔵 **สองในสามของใบนี้ตอบแล้ว — เหลือ 2 ไบต์ (LANE-A รอบ `f6e5kd` 2026-09-03T14:35+07:00)**
> ใบผล `20260902_1039` (ซึ่งไม่มีใครอ่านอยู่ 28 ชั่วโมง จน chief ส่งต่อในใบ `20260903_1207`) ปิดไปแล้วสองข้อ:
> **(1) `span_sha256`** `f808c0d6…2bc5` ของสแปนเต็ม ตรงกับอิมเมจ `9627…b623` — เกณฑ์ข้อที่สองของใบนี้ **ปิด**
> **(2) 3 ไบต์แรก** `0x0045BC80..0x0045BC82` — ใบยก `0x0045BC81  mov esi, ecx` ⇒ `ESI` = `this` **ก่อน** ประตู
> ⇒ สาขา "`push ebx; mov esi,edx` ⇒ ต้องทบทวน ข." **ตายแล้ว** และ caller ยืนยันชนิดซ้ำ (`[QuestNPCModule+0x18]` → `CNetNPC` → `ECX`)
> **สิ่งที่ยังเหลือ และเป็นทั้งใบตอนนี้: 2 ไบต์ `0x0045BC87..0x0045BC88`** (ช่องว่างหลังประตู ก่อน `movsx` ที่ `0x0045BC89`)
> ใบ `1039` มีแต่ประโยคสรุปว่า "ไม่มีการ dereference ไป attached attr ระหว่างทาง" — **ไม่ได้ยกไบต์มาแสดง**
> ⇒ ถ้าสองไบต์นั้นคือ `8B F1` (`mov esi,ecx`) ประตูที่ `BC83` อ่านออบเจ็กต์คนละตัวกับ `+0x360/+0x364` และ **ข. ต้องทบทวน**
> ⇒ ถ้าเป็น jcc/nop/อะไรก็ตามที่ไม่เขียน `ESI` ⇒ **ข. ปิดสนิท** และ `RE-202` ไม่มีข้อจำกัดเหลือเลย
> 🔴 **ห้ามอ่านการย่อนี้ว่า "ตอบแล้ว"** — ยังไม่มีใครเห็นสองไบต์นั้น และ 12 ไบต์ที่ `0x45BC90` ก็ยังไม่มีใครอ่านเหมือนเดิม

ใบนี้ถือ **ขั้นตอนเดียวที่ `RE-202` ปิดไม่ลง** ไว้ไม่ให้หายไปกับใบที่ปิดแล้ว (pf-adversary รอบสอง ข้อ 6)
`RE-202` ตอบ **ข.** (`+0x70` เป็นของ `CNetNPC`) และมีหลักฐานอิสระหนุน แต่ *เส้นทางพิสูจน์ผ่าน ESI*
ยังมีรู: literal ที่ commit ไว้ปัก **29 จาก 60 ไบต์** ของสแปน `0x0045BC80..0x0045BCBC` เท่านั้น

**คำถามเดียวของใบนี้: 11 ไบต์แรก `0x0045BC80..0x0045BC8A` ประกอบด้วยคำสั่งอะไรบ้าง**
(prologue 3 ไบต์ก่อนประตู + ช่องว่าง 2 ไบต์หลังประตู)

- ถ้า 3 ไบต์แรกไม่ได้เขียน ESI และ 2 ไบต์กลางเป็น jcc ⇒ ESI ตัวเดียวตลอด ⇒ **ข. ปิดสนิท**
- ถ้า 3 ไบต์แรกเป็น `push ebx; mov esi,edx` (`8B F2`) หรือ 2 ไบต์กลางเป็น `mov esi,ecx` (`8B F1`)
  ⇒ ประตูอ่านออบเจ็กต์คนละตัวกับที่ `+0x360/+0x364` ใช้ ⇒ **คำตอบของ `RE-202` ต้องกลับมาทบทวน**
  (และงาน quest mark ฝั่งเซิร์ฟเวอร์กลับมามีทางเดินอีกครั้ง)

**เกณฑ์ปิดใบ (ชั้นเดียว ชั้น static เท่านั้น — ไม่มีชั้น client-observable และไม่ต้องมี)**
- ดิสแอสเซมบลี `0x0045BC80..0x0045BC8A` จากอิมเมจ `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
  ยกไบต์ + คำสั่งที่ถอดได้มาทั้งช่วง แล้วตอบว่า ESI ถูกเขียนก่อนถึง `0x0045BC83` หรือไม่ และหลังจากนั้นหรือไม่
- ยืนยัน `span_sha256` `f808c0d68b1a782d3441e118a25a94ee73e1f4aea37824b06fd2e2c6fb112bc5`
  ของสแปนเต็มกับอิมเมจไปด้วย (`RE_STATIC_SEARCH_RULES.md` §1 ซึ่ง `RE-202` ทำไม่ได้จากคลาวด์)

**ราคาที่ประหยัดได้ถ้าไม่ทำ:** ไม่มี — ใบนี้เล็กมาก (11 ไบต์) และเป็นสิ่งเดียวที่กั้นไม่ให้คำตอบของ
`RE-202` เป็นข้อสรุปที่พิสูจน์ครบ · ถ้าผลออกมาขัดกับ ข. LANE-A จะเปิด `RE-202` ใหม่เองในรอบถัดไป

- links: `RE-202` (ปิดแล้ว ใบผล `notes_to_chief/20260902_1035_RE-202-RESULT-*`) ·
  `notes_to_chief/reference_codex_attr/pf_rederive_attr_semantics.py:7094-7097, 7492-7495` ·
  `PF_ATTR_QUEST_MARK_SELECTOR.tsv` คอลัมน์ `support_spans`
- ค้นใน `pf_bridge\external\` แล้ว: **ไม่เจอ** (ค้นจากคลาวด์: ไม่มีดิสแอสเซมบลีของสแปนนี้ที่ commit ไว้
  นอกจาก literal สี่ตัวข้างบน ซึ่งไม่ครอบคลุม 11 ไบต์ที่ถาม) · ค้น `gamedata` แล้ว: **ไม่เกี่ยว** (คำถามอยู่ในโค้ด ไม่ใช่ตาราง)
- numbering: `RE` สูงสุดในไฟล์นี้ = 208 · grep `RE-209` ทั้งรีโปพบเฉพาะใบนี้ ⇒ `209`
- result: (สาย RE กรอก: ไบต์ + คำสั่งที่ถอดได้ของ `0x0045BC80..0x0045BC8A` · ESI ถูกเขียนหรือไม่ · sha ตรงหรือไม่ · timestamp)

## 🔬 RE-210 EXIT-BUTTON-ONLAND-RESPONSE-EXPECTATION-001 [**CLOSED / PASS** -- ตอบแล้ว 2026-09-02T15:03+07:00 · บริโภคโดย LANE-A รอบ `gwwpmr` 2026-09-02T15:35+07:00 · เปิดโดย LANE-A รอบ `1d6rta` · ผู้ท... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-222 NONPOSITIVE-IDENTITY-TYPED-AND-LIVE-GATE-REACHABILITY-001 [OPEN -- ร่างโดย LANE-GM รอบ `5ddsii` (ใบ `notes_to_chief/20260903_1119_LANE-GM-RE-211-TICKET-*.md`) ตามข้อยกเว้นใบเดียวของ `COO-DECISION 20260903_1046` ข้อ (ข) · **วางคิวและมอบหมายโดย chief รอบ `kjtpza` (R319) 2026-09-03T13:0x+07:00** · ผู้ทำ: **สาย RE** (ผู้ทำสายเดียว ไม่ต้องจอง) · **LANE-GM บริโภคผลเอง** · 🔴 `[STATIC-ON-BRIDGE]` ต้องดิสแอสเซมบลีอิมเมจ ⇒ ทำบนคลาวด์ไม่ได้]

> 🔴 **เลขใบเปลี่ยนจาก `RE-211` ที่ร่างมาเป็น `RE-222`** — ร่างนับเลขจาก `CLIENT_RE_QUEUE.md` ไฟล์เดียว
> แต่กฎ ② หัวไฟล์นี้ใช้ **ตัวนับร่วมสองคิว**: คำสั่งค้นหาเดียวได้ `221` (`GT-221` ลง `main` แล้วรอบ R318)
> ⇒ ใบนี้ `222` · **ไม่มีใบชื่อ `RE-211` ในคิวทั้งสองไฟล์** (`grep` ทั้งสองไฟล์ + `archive/*QUEUE*ARCHIVE*` = 0 hit)
> 🔴 **แต่มีโค้ดบน `main` ที่อ้างชื่อ `RE-211` อยู่ห้าจุด และมันคือเกตของ P-2 เอง** (pf-adversary R319 จับได้
> หลังผมเขียนประโยคปฏิเสธที่ grep ไม่ครบ): `gm/name_color_gate.py:55,137,140,303,315,331` และ
> `tests/test_gm_name_color_gate.py:340,395,445` (`assert gate.RE_211_TICKET_ID == "RE-211"`)
> ⇒ **LANE-GM ต้องอัปเดตชื่อในไฟล์ของตัวเองเป็น `RE-222` พร้อมเทส ก่อนผลของใบนี้จะปลดเกตได้**
> มิฉะนั้นผลจะมาถึงแล้ว `NameColorGateUnmeasured` ยังปฏิเสธต่อ เพราะบล็อกเกอร์ชี้ไปที่ชื่อที่ไม่มีใบ
> ✅ **LANE-GM ทำแล้วรอบ `1nm6hh` (2026-09-03T14:3x+07:00)** — `RE_211_*` → `RE_222_*` และ
> `RE_222_TICKET_ID = "RE-222"` ทั้งใน `gm/name_color_gate.py` และเทสสองตัวที่ปักชื่อ · เลขเดิม **ขีดฆ่าไว้ ไม่ลบ**
> · ชื่อไฟล์จดหมายใน `RE_222_TICKET_LETTER` **คงเป็น `...RE-211-TICKET...` โดยตั้งใจ** เพราะไฟล์นั้นมีอยู่จริงชื่อนั้น
> (มีคอมเมนต์กำกับห้ามรอบหลัง "แก้" path นี้) · 🔴 **สถานะจริง: push แล้ว รอ merge PR เซิร์ฟเวอร์ของรอบ `1nm6hh`**
> ยังไม่อยู่บน `main` — รอบถัดไปวัดด้วย `git merge-base --is-ancestor` ก่อนเชื่อ

- ถาม: identity ที่ **ไม่เป็นบวก** เดินถึงหางแบบ typed (`CNetNPC`) ของ selector ชื่อได้จริงหรือไม่
  และประตูที่แยกสองตระกูลนั้นเป็นคำสั่งอะไรกันแน่ — `RE-195` ปิดทิศบวกไว้ทิศเดียว ทิศกลับ **ไม่เคยถูกวัด**
  และ `gm/name_color_gate.py` บน `main` ปฏิเสธที่จะเดามันโดยเจตนา (`NameColorGateUnmeasured`)
  ⇒ ตราบใดที่ใบนี้ไม่มีผล **ครึ่งเซิร์ฟเวอร์ของ P-2 เดินต่อไม่ได้แม้แต่บรรทัดเดียว**
- อิมเมจที่ต้องยึด: `GameClient.local.bin` 14,759,424 ไบต์
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
  สแปน selector `[0x00443F50,0x004443C5)` sha256 `ee845ee6ef6337ea41ae57a5a4df8af5a8a8ac00e458ea1ce3e587aff1f9cdf9`

- 🆕 **Q0 (คำถามแรกของใบตั้งแต่ 2026-09-03) รูปเฟรม `UpdateAttrVital 0x309A`** — วางโดย chief รอบ `pk14rf`/R326 ตาม `COO-DECISION 20260903_1744` ข้อ 2 (ถ้อยคำจาก LANE-GM ใบ `notes_to_chief/20260903_1933_*` · **ไม่เปิดใบใหม่** ตามคำสั่งเดียวกัน)
  > ไคลเอนต์อ่าน `UpdateAttrVital 0x309A` ด้วย **รูปเฟรมแบบไหน** และเฟรม 74 ไบต์ที่ `GT-218` ส่งผิดรูปตรงไหน
  > — ตอบจากตัวถอด/ตัวเขียนของไคลเอนต์เอง **ไม่ใช่จากการเทียบกับ opcode อื่น**

  หลักฐานที่ต้องเทียบ (ใบผล `notes_to_chief/20260903_1657_KA1A-R306-RESULTS-*.md`): เฟรมที่ออกจริง **74 ไบต์** ·
  `attr id 0x40` · ฟิลด์ `12 AD 12 14 1E 00 00 00` · ท้าย `05 01` · ผลบนจอ: **HP สูงสุด→1 และเงิน→0 ในเฟรมเดียว** ·
  ค่า `400.0` เป็นค่าเดียวกับที่ล็อกอินส่งทุกวันและตัวละครรอด ⇒ **ค่าพ้นผิด รูปเฟรมเป็นผู้ต้องหา** (`1744` ข้อ 1) ·
  `RE-198` เคยตอบ bounded-negative ว่าไบต์ header **เดา**มาจาก opcode อื่น — R306 คือหลักฐานสดว่าเดาผิด

  จุดเริ่มที่ค้นมาแล้ว (LANE-GM · ไม่ต้องเริ่มจากศูนย์): `external/PF_PROTOCOL_REGISTRY.tsv:51` มี `UpdateAttrVital`
  ctor `0x005E5DB0` ตัวเขียน `0x005E42C0` · `external/PF_SERIALIZER_FIELDS.tsv` มี **34 แถว** (17 W + 17 R)
  pin sha256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` ·
  **ฝั่ง R ถอดได้แค่ 4/17** (`R1 SUBCALL:0x00463DE0 @+0x14` · `R10 tag 0x12 @STACK+0x38 2B` · `R11 tag 0x12 @STACK+0x34 2B` · `R12 tag 0x14 @STACK+0x14 4B`)
  ⇒ **ช่องว่างจริงคือ 13 แถว `UNKNOWN` ฝั่ง R** ไม่ใช่ "ไม่มีข้อมูลเลย" · เริ่มที่ `0x00463DE0` (สแปน `0x00463DE0`-`0x00463FA2` sha `888c2fac...`)

  เกณฑ์ปิด **Q0** สองชั้น (รูปเดิมของใบ): ① **ชั้นสถิต** ปิด 13 แถว `UNKNOWN` ฝั่ง R — ลำดับ tag/ความกว้าง/ออฟเซ็ตของทุกฟิลด์ที่ตัวอ่านอ่านจริง
  พร้อม `span_sha256` ของสแปนที่อ่าน (`RE_STATIC_SEARCH_RULES.md` §1) · ② **ชั้นเทียบ** diff ฟิลด์ต่อฟิลด์กับ 74 ไบต์ข้างบน
  ระบุ **ฟิลด์ที่ต่าง** ไม่ใช่ "รูปไม่ตรง" เฉย ๆ

  🔴 **Q0 ไม่ต้องตอบ**: ค่า speed ที่ปลอดภัย (คำถามนั้นถูกยกเลิกโดย `1744` ข้อ 1) · `ForcePos` 45 ไบต์ของ `/warp <n> <x> <y>`
  (คนละเฟรม LANE-GM ปิดเส้นทางด้วยแฟล็กแล้ว — จะให้ใบเดียวตอบสองเฟรมต้องให้ COO เคาะก่อน)
  🔴 **ลำดับ**: Q0 มาก่อน Q1-Q3 แต่ **ไม่ได้แทนที่** — Q1/Q2 ยังเป็นตัวปลดครึ่งเซิร์ฟเวอร์ของ P-2 ตามเดิม ถ้าต้องย่อ ตัด Q3 ก่อนเหมือนเดิม

- **Q1 ประตูแยก** ระหว่าง path entry ตัวสุดท้ายของตระกูลบวก (`0x0044414A`) กับตัวแรกของตระกูลไม่บวก
  (`0x0044417E`) มีการเปรียบเทียบที่ตัดสินสองตระกูล — ขอ **ไบต์ + คำสั่งที่ถอดได้** ของช่วงนั้น แล้วตอบ:
  ทดสอบ dword ไหนของ identity pair (ต่ำ/สูง/ทั้งคู่ — ไวร์เราส่ง qword `qwordtag(0x32, actor_identity)`) ·
  signed หรือ unsigned และเส้นแบ่งอยู่ตรงไหนเป๊ะ · **ศูนย์ตกข้างไหน**
  (ป้าย `signed_nonpositive` วันนี้สืบจาก **ชื่อคอลัมน์** ไม่ใช่จากคำสั่ง — ไฟล์เกตระบุเองว่า `[PROPOSED]`)
- **Q2 ประตู typed** ไล่จาก `0x0044417E` ถึง `0x00444234` แล้วรายการ **เกตทุกตัวตามลำดับ** ว่าอะไรอ่านอะไร
  และ operand เป็น (ก) ฟิลด์จากไวร์ (ข) ตาราง/สถานะ local ของไคลเอนต์ (ค) การทดสอบชนิดออบเจ็กต์ (RTTI/vtable)
  🔴 **ข้อที่ตัดสินทั้งใบ:** `typed_CNetNPC` เป็นการทดสอบ **ชนิดออบเจ็กต์** ที่ไม่เกี่ยวกับ identity ใช่หรือไม่
  ถ้าใช่ ⇒ เปลี่ยนเครื่องหมาย identity **ไม่มีวัน**พาแถว `FieldMob` เข้าหางนั้น = **ปฏิเสธทั้งทิศทาง**
  ซึ่งมีค่ากับเรามากกว่าคำตอบว่า "ได้"
- **Q3 ประตู live** (ตัดข้อนี้ก่อนถ้าต้องย่อ — Q1+Q2 คือตัวปลดล็อกโค้ด) ตัวลงทะเบียน/ค้นหา actor
  (เส้นเดียวกับแถว `0x00444210` `actor_lookup_succeeds`) คีย์ด้วย identity แบบ signed หรือ unsigned ·
  ค่าติดลบถูกปฏิเสธ/ตัดทิ้ง/alias ตอนลงทะเบียนไหม · ถ้าถูกทิ้ง ⇒ มอนตัวนั้นคลิกไม่โดน = ทิศนี้ตายทั้งเส้น

- เกณฑ์ปิดใบ (**ชั้นเดียว — static IMAGE เท่านั้น ไม่มีชั้น client-observable และไม่ต้องมี**):
  ยกไบต์ + คำสั่งที่ถอดได้ของช่วงที่ตอบ พร้อม `span_sha256` ของแต่ละช่วง เทียบกับอิมเมจข้างบน
  (`RE_STATIC_SEARCH_RULES.md` §1) · ตอบ Q1 **ด้วยคำสั่งที่ยกมา ไม่ใช่ด้วยชื่อคอลัมน์** ·
  ตอบ Q2 ด้วยรายการเกตตามลำดับ + คำตอบใช่/ไม่ใช่ของข้อ RTTI · ตอบ Q3 ด้วย VA ของตัวลงทะเบียน/ค้นหา + ชนิดการเทียบ
- ใบนี้ **ไม่ขอ**: เลข `FontStyleID` ใด ๆ · สคีม identity ติดลบ (ถามว่า *ประตูเปิดไหม* ไม่ได้ถามว่าจะส่งเลขอะไร) ·
  faction-only fix (`RE-195` job 1 ปิดแล้วว่า `+0x68` เป็น operand ของ fallback เท่านั้น) · ผลจากจอ
- ค้นแล้วก่อนเปิด (LANE-GM กรอกเอง): `external/00_SEARCH_HERE_FIRST.md` **เจอไฟล์ ไม่เจอคำตอบ** ·
  `gamedata/` **ไม่เจอ** (คำถามอยู่ในโค้ดของอิมเมจ ไม่ใช่ในตาราง) · `external/` ทั้งสิบไฟล์ **ไม่เจอ** ·
  `reference_codex_attr/PF_ATTR_NAME_COLOR_SELECTOR.tsv` **เจอ 14 แถว** (เลขในใบยกจากแถวจริงทั้งหมด)
- links: ร่างเต็ม + ราคาที่ประหยัดได้ `notes_to_chief/20260903_1119_LANE-GM-RE-211-TICKET-*.md` ·
  `RE-195` ผล `notes_to_chief/20260902_0341_RE-195-RESULT-*.md` · `RE-191` ผล `notes_to_chief/20260901_1439_CODEX-RE191-RESULT-*.md` ·
  `pirate-force-server/src/pirateforce_foundation/gm/name_color_gate.py`
- numbering: คำสั่งตัวนับร่วม (กฎ ②) ได้ `221` ⇒ ใบนี้ `222` · `RE-222`/`GT-222` = 0 hit ตอนวาง
- result: (สาย RE กรอก: ไบต์+คำสั่ง Q1 · รายการเกต Q2 + ใช่/ไม่ใช่ RTTI · Q3 signed/unsigned + ชะตาของค่าติดลบ ·
  span sha ทุกช่วง · timestamp)


## 🔬 RE-227 CAPTAIN-REPORT-ON-ISLAND-CONTACT-001 [🔴 **primary hypothesis REFUTED-ON-SCREEN (R318 `1319`) · covered by `RE-265`** — แก้หัวใบโดย LANE-A รอบ `ihjytc` 2026-09-05T16:4x+07:00 ตาม `COO-DECISION 20260905_1348` ข้อ 4]

> 🔴 **หัวใบเดิมของบรรทัดนี้คือ `DONE / BOUNDED` ปิดโดย LANE-A รอบ `2mnd7b` 12:0x — ~~ปิด~~ ถอนแล้ว ไม่ใช่แก้คำผิด**
> **เพราะอะไร**: `GT-233` R318 (`notes_to_chief/20260905_1319_KA1A-R318-RESULTS-*.md`) ยิง 8 เร็กคอร์ด 73 ไบต์ผ่าน parser ของไคลเอนต์ (0 `ErrorData` ⇒ `RE-256` ถูก) แล้วแล่นเรือเข้าใกล้เกาะ **37 หน่วย** (Prison Exile ×3) และ **144 หน่วย** (Spice Paradise ×3) — ทั้งสองระยะต่ำกว่าเกณฑ์ ≤500 ที่ชั้น ① ของใบนี้อ้าง — และ **หน้ารายงานกัปตันไม่เด้งสักครั้ง** (Panya ยืนยันด้วยตา 12:48)
> ⇒ ชั้น ① "client เช็กระยะเอง ≤500 แล้วเปิดหน้าต่างในเครื่อง" = **REFUTED บนจอ** ไม่ใช่ `shipped` · ห้ามคงคำว่า shipped ไว้ในหัวใบนี้อีก (`COO-DECISION 20260905_1348` ข้อ 4)
> **อะไรที่ยังยืน**: กลไกฝั่งเซิร์ฟเวอร์ที่ขึ้น main แล้ว (`world_m2_provisioning_trial.py`/`navigationex_survey_record.py` · PR `#753`/`#760`/`#797`/`#810`) **ส่งเร็กคอร์ดออกได้จริงและไคลเอนต์รับได้จริง** — สิ่งที่หักล้างคือคำอธิบายว่า "อะไรเปิดหน้าต่าง" ไม่ใช่โค้ดที่ส่ง
> **ใครตอบต่อ**: `RE-265 WHAT-OPENS-THE-CAPTAIN-DOCK-REPORT-WINDOW-001` (สามคำถาม · เนื้อใบส่งเป็นจดหมาย `20260905_16xx_LANE-A-RE-265-TICKET-BODY-*.md` รอบ `ihjytc`) · ห้ามบูต `GT-233` ซ้ำจนใบนั้นตอบ · ทาง BACKUP XYZ ปิดถาวร
> **สองสมมติฐานที่เหลือถือเท่ากัน** จนกว่า `RE-265` ตอบ (`1348` ข้อ 5): (ก) เซิร์ฟเวอร์เดิมตอบ `0x1FB2` ด้วยเฟรมสั่งเปิดหน้ารายงาน (opcode ยังไม่รู้ — `RE-234` พิสูจน์แค่ว่า *response ของ TriggerVital เอง* เป็น no-op ไม่ได้ปิดเฟรมชนิดอื่น) (ข) `AddSurveyData` ไม่ใช่ตัวเปิดหน้านี้ · **ห้ามเขียนโค้ดตามสมมติฐานใดก่อนผล**
> `M2_OBSERVED_ISLAND_TRIGGER_IDS` ยัง log-only ตามเดิม ไม่มีอะไรเปลี่ยนในโค้ดจากการแก้หัวใบนี้

> ~~**ปิดยังไง (ข้อความเดิม 2026-09-05T12:0x คงไว้ทั้งก้อน ห้ามลบ)**~~ — อ่านต่อได้ข้างล่าง ขีดฆ่าเฉพาะข้อสรุป ไม่ใช่หลักฐาน:

> **ปิดยังไง**: ชั้น ① STATIC (AddSurveyData → proximity ≤500 → local prompt → confirm ส่ง `EnterInstance` body `12 <u16> 0B 06`) ยืนตามผลเดิม (`notes_to_chief/20260904_0724_RE-227-RESULT-*.md`) และ**เป็นกลไกที่ขึ้น main แล้วจริง**: `world_m2_provisioning_trial.py`/`navigationex_survey_record.py` (PR เซิร์ฟเวอร์ `#753`/`#760`/`#797`/`#810`, ล่าสุด `RE-256` ปิด outer-presence byte) — `GT-233` READY รอเครื่อง Panya ยืนยัน E2E บนจอ
> ชั้น ② (ทาบกับสาย) ของคำถามเดิม**เปลี่ยนรูปคำถาม ไม่ใช่ปิดตามเกณฑ์เดิมที่ตั้งไว้แต่แรก** — เกณฑ์เดิมสมมติว่า `TriggerVital 0x1FB2` (id `153`/`154`) อาจเป็นอีกเส้นทางยืนยัน สมมติฐานย่อยนั้นถูกแยกเป็นใบ `RE-234` ไปแล้วตั้งแต่รอบ `0foax0` และตอนนี้ `RE-234` กลับผลแล้ว (`notes_to_chief/20260904_1953_RE-234-RESULT-*.md`, DONE/MIXED): (ก) `GT-228`/R308 (`notes_to_chief/20260904_1331_KA1A-R308-RESULTS-*.md`) วัดว่าเรือชนเกาะจริงยิง `TriggerVital` id **`2`**(Prison Exile)/**`3`**(Spice Paradise) — **ไม่ใช่** `153`/`154` ตามที่ใบนี้เดาไว้แต่แรก (ก) ถูกหักล้าง (ข) `RE-234` พิสูจน์ static ว่า natural handler ของ `TriggerVital` response เป็น **success no-op ห้าไบต์** ไม่เปิดหน้าต่างอะไรเลย ⇒ เส้นทางคู่แข่งที่ใบนี้เปิดค้างไว้ (`0x1FB2` response) **ไม่ใช่กลไกจริง** ยืนยันซ้ำว่ามีทางเดียวคือ AddSurveyData
> ⇒ ~~**CANCELLED (secondary hypothesis) / DONE (primary hypothesis, shipped)**~~ **ขีดฆ่า 2026-09-05 รอบ `ihjytc`** — ครึ่ง secondary (`covered by RE-234`) ยังยืน · ครึ่ง primary กลายเป็น **REFUTED-ON-SCREEN** ตามหัวใบข้างบน · ~~เหลือเฉพาะการยืนยัน on-screen ซึ่งเป็นของ `GT-233`~~ การยืนยันนั้นเกิดขึ้นแล้วและ**ให้ผลลบ** (R318)

## 🔬 RE-227 CAPTAIN-REPORT-ON-ISLAND-CONTACT-001 [PARTIAL -- ยังไม่ปิด (OPEN) · ร่างโดย LANE-A รอบ `xv20xj` · 🔴 `[STATIC-ON-BRIDGE]`]

> 🟡 **สถานะ 2026-09-04T07:24+07:00 (กรอกโดย chief รอบ `8nh6q5`/R334 ตาม `COO-DECISION 20260904_0746` ข้อ 2 · ถ้อยคำตามที่ runner เขียนท้ายใบ ไม่แก้)**
>
> `RE-227 PARTIAL — STATIC PASS: NavigationEx AddSurveyData -> client proximity <=500 -> local prompt -> confirm sends EnterInstance body 12 <opaque-u16> 0B 06; CAPTURE/GT-228 REQUIRED FOR ACTUAL WIRE + SCENE-CHANGE JOIN`
>
> - จดหมายผลเต็ม: `notes_to_chief/20260904_0724_RE-227-RESULT-NAVIGATIONEX-STATIC-CAPTURE-PENDING.md` (มี span_sha256 ครบทุกสแปน + nonclaim 7 ข้อ)
> - **ปิดได้ครึ่งเดียว = ชั้น ① สถิต** · ชั้น ② (ทาบกับสาย) ยังค้าง ⇒ **ใบยังเปิด ห้ามใครยกใบนี้ไปเป็นฐานของใบอื่นแบบปิดแล้ว**
> - 🔴 **ห้าม runner rerun ใบนี้จนกว่าจะมีผล `GT-228`** (หรือ chief แก้ objective อย่างมีสาระ) — เพดานเป็น method/cross-layer ไม่ใช่ time checkpoint
> - 🔴 **ครึ่ง (ก) ของคำถามเดิมถูกหักล้างแล้ว**: contact branch ของ NavigationEx docking tick **ไม่ส่ง** `TriggerVital 0x1FB2` · เส้นทางจริงคือเซิร์ฟเวอร์ provision `NavigationEx_AddSurveyDataVtial` (byte `+0x10`=1 · u16 opaque `+0x12` · XYZ f32) แล้วไคลเอนต์เช็กระยะ `<=500` เองในเครื่อง · **ฝั่งเราไม่เคยส่ง record นี้ = เหตุที่หน้าต่างไม่เด้งบน R307** · `0x1FB2` ลดเป็นสมมติฐานรอง (nonclaim 1 ของ runner ยังเปิด ไม่ใช่การตัดทิ้ง)
> - route tag เดิมไม่มีในหัวใบ (runner ขอไว้ในจดหมายผล ข้อ `route note`) ⇒ เติม `[STATIC-ON-BRIDGE]` รอบนี้

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `3kwnnr`/R332 2026-09-04T05:2x+07:00 ตาม `COO-DECISION 20260904_0344` ข้อ 3** — ตัวนับร่วมสองคิว + archive คืน `226` (ใบ `GT-226` ของรอบเดียวกัน) ⇒ ใบนี้ `RE-227` · `RE-227` = 0 hit ทั้งสามที่ก่อนวาง · เนื้อใบวางทั้งก้อนตามที่ LANE-A ร่าง ไม่แก้ถ้อยคำใด ๆ นอกจากเติมเลขใบ · **เจ้าของใบและผู้บริโภคผล = LANE-A**


- **ถาม (สองข้อ ข้อเดียวกันคนละครึ่ง)**
  - **(ก) ขาออกจากไคลเอนต์**: ตอนเรือ **ชน/เข้าเขตเกาะ** (ไม่ใช่คลิก — เจ้าของยืนยันสด `0409`)
    ไคลเอนต์ส่งอะไร · เป็น `TriggerVital 0x1FB2` ที่ถือ **trigger id ของแถวเกาะ** (`153` Prison Exile Island ·
    `154` Spice Paradise Island — ที่มาของเลขสองตัวนี้อยู่ข้างล่าง) หรือเป็น opcode อื่นทั้งดุ้น
    หรือไม่ส่งอะไรเลยและหน้าต่างเป็นของไคลเอนต์ล้วน (เช็คระยะเอง ไม่มีไบต์ออกจนกด "ยืนยัน")
  - **(ข) ขาเข้าจากเซิร์ฟเวอร์ + ขายืนยัน**: เฟรมไหนเปิดหน้า "รายงานกัปตัน เรือเทียบท่า [ชื่อเกาะ]" ·
    ปุ่ม "ยืนยัน" ส่งไบต์อะไรกลับ · เฟรมไหนทำให้ฉากเปลี่ยนจริง (เป็น `TeleportVital` เดิมหรือคนละตัว)

- **ทำไมใบนี้แคบกว่าที่เคยขอ (`RE-086`/`RE-087` ปิดไปแล้วเมื่อ 27 ส.ค.)**
  เพราะรอบนี้ตัดสองกิ่งทิ้งแล้ว: (1) "ผู้เล่นคลิกเกาะ" ตัดออกทั้งกิ่งจากคำเจ้าของ ·
  (2) "id ไหนคือเกาะ" ตอบแล้วจากตารางที่คอมมิต ไม่ต้องเปิดอิมเมจเพื่อหาเลข
  เหลือคำถามเดียวจริง ๆ คือ **รูปเฟรม** ไม่ใช่ "กลไกคืออะไร"

- **เลข `153`/`154` มาจากไหน (grade A · ทำซ้ำได้ ไม่ต้องมีอิมเมจ)**
  `gamedata/tables/TEXTDATA_TH__Trigger_TIP.tsv` แถว **152-167 เป็นบล็อกปลายทางการเดินทางติดกันทั้งบล็อก**
  แยกจาก prop รอบข้างด้วยสามอย่างพร้อมกัน:
  1. **ชื่อ** ตรงตัวอักษรกับ `s_SCENE_NAME` ใน `TEXTDATA_TH__SCENE_NAME_TIP.tsv` และเรียงตามลำดับฉาก
     (152 Port Royal · 153 Prison Exile Island · 154 Spice Paradise Island · 155 Slave Market Island · … 161 Hell Volcanic Island)
  2. **เพดานเลเวล** ในข้อความ tip เท่ากับ `n_SCENE_LV` ของแถวฉากเดียวกันใน `CONSTDATA_TH__SCENE_NAME.tsv`
     **ครบ 10 แถว** (0/0/25/45/60/70/81/86/92/100) — สองตารางคนละชุดตรงกันสิบตัวเลข
  3. **ไม่มีคำกริยาใช้งาน** — 148/149/150/151 ข้างบน และ 169-175 ข้างล่าง เขียน `[วิธีใช้: ดับเบิ้ลคลิกซ้าย]` ทุกแถว
     บล็อก 152-167 **ไม่มีสักแถว** มีแต่เงื่อนไขเลเวล ⇒ เข้ากับ "ชนแล้วเด้งเอง ไม่ต้องคลิก"
  คำสั่งทำซ้ำ: `awk -F'\t' 'NR>1 && $1>=148 && $1<=175 {print $1"\t"$2"\t|"$3"|"}' gamedata/tables/TEXTDATA_TH__Trigger_TIP.tsv`

- **สิ่งที่ยังไม่ใช่หลักฐาน (nonclaim บังคับของใบนี้)**
  ไม่เคยมีใครเห็นไบต์ของเฟรม `0x1FB2` ที่ถือ id `153` หรือ `154` เลยสักครั้ง · 5 เฟรมที่ R307 จับได้ถือ id
  40/51/3/57/36 ซึ่งเป็น prop ทั้งห้า · ข้อ 3 ข้างบนเป็น **ความเข้ากันได้ ไม่ใช่การพิสูจน์** ·
  ห้ามใบนี้หรือใครอ้างว่า "`0x1FB2` คือเฟรมเทียบท่า" จนกว่าจะมี hex + `span_sha256`

- **อิมเมจที่ต้องยึด (ถ้าตอบด้วย static RE)**
  `GameClient.local.bin` 14,759,424 ไบต์ sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
  ทางเข้าที่แนะนำ: ตัวอ่าน/ตัวเขียน `TriggerVital 0x1FB2` ใน `external/PF_PROTOCOL_REGISTRY.tsv` ·
  แล้วไล่ไปที่หน้าต่างที่ใช้สตริง "รายงานกัปตัน"/"เทียบท่า" ใน `TEXTDATA_TH__UI_MESSAGE.tsv`

- **เกณฑ์ปิดสองชั้น**
  ① **สถิต**: ลำดับ tag ของเฟรม (ก) และ (ข) ครบทุกฟิลด์ พร้อม `span_sha256` ของสแปนที่อ่าน (`RE_STATIC_SEARCH_RULES.md` §1)
  ② **ทาบกับสาย**: hex จริงจากใบ capture ของรอบเดียวกัน (ใบ capture ที่ผมร่างคู่กันมา) ตรงกับรูปเฟรมของ ① ทุกไบต์
  🔴 ปิดด้วยชั้นเดียวไม่ได้ · ตอบได้ครึ่งเดียวให้ปิดแบบ **bounded** และระบุว่าอีกครึ่งค้างอยู่ที่ไหน

- **ทางลัดที่ถูกกว่า และควรลองก่อนเปิดอิมเมจ**
  log-only responder ของรอบนี้ (`lane_hooks/lane_a_island_trigger_log.py`, PR เซิร์ฟเวอร์รอบ `xv20xj`)
  พิมพ์ trigger id + ชื่อจากตารางทุกเฟรม `0x1FB2` ที่เข้ามา และพิมพ์คำว่า `ISLAND` เมื่อ id ตรงแถวเกาะ
  ⇒ **ถ้าใบ capture ได้บรรทัด `LANE_A_TRIGGER_VITAL id=153 name=Prison Exile Island ISLAND` มาใบเดียว
  ครึ่ง (ก) ของใบนี้ปิดทันทีโดยไม่ต้องเปิดอิมเมจ** เหลือแต่ครึ่ง (ข)
  🔴 responder ตัวนั้น **ยังไม่ถูกเรียก** จนกว่า chief จะวางจุดยิงหนึ่งบรรทัด (CORE-REQUEST ในใบ PR รอบนี้)

- **ผู้ทำ**: chief มอบหมาย (สายเดียว ห้ามเขียน "X หรือ Y") · ผลกลับมาถึง **LANE-A** แล้วผมสร้าง responder จริงในรอบที่ผลถึง

---

## 🔬 RE-229 CHARCREATE-CLASS-SSCORE-STARTING-STATS-SOURCE-001 [🟢 **CLOSED BOUNDED-NEGATIVE/DONE — RE runner local 2026-09-04T10:50+07:00, ปิดหัวใบโดย... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-232 SCAST-CONDITION-BEHAVIOR-TOKEN-GRAMMAR-001 [~~OPEN -- 🔴 `[STATIC-ON-BRIDGE]`~~ 🔵 **DONE / BOUNDED-NEGATIVE — ปิดโดย LANE-CS รอบ `tp9rpy` 2... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-234 CLIENT-RESPONSE-PATH-FOR-TRIGGERVITAL-1FB2-ISLAND-001 [🔵 **DONE / MIXED PASS + BOUNDED-NEGATIVE — ปิดโดย LANE-A รอบ `2mnd7b` 2026-09-05T12:0x+07:00**]

> ผล: `notes_to_chief/20260904_1953_RE-234-RESULT-TRIGGERVITAL-NOOP-ID-ONLY-UNSAFE.md` (repro verifier `pf_bridge/staged/re234_static_verify.py` PASS 18/18)
> **(1)** natural handler ของ `TriggerVital` response = `[0x00710440,0x00710445)` **success no-op ห้าไบต์** (`B0 01 C2 04 00`) — ไม่อ่าน ไม่เปิด UI ไม่มีผลบนจอ
> **(2)** ของสองเส้นทางที่ใบนี้ถาม มีทางเดียวที่พิสูจน์ว่าเปิดหน้ารายงานกัปตันได้จริง = **AddSurveyData + proximity ≤500** (`RE-227`) · `TriggerVital` response **ไม่ใช่** เส้นทางนั้น (พิสูจน์แล้วจากข้อ 1)
> **(3) BOUNDED-NEGATIVE**: พิสูจน์ไม่ได้ว่า `TriggerVital` id `2`/`3` เป็น namespace เดียวกับ `TEXTDATA_TH__Trigger_TIP` (`GT-228` เห็น id `3` ทั้งตอนชนเกาะและตอนแล่นเรือปกติ) ⇒ `lane_hooks/lane_a_island_trigger_log.py`'s `M2_OBSERVED_ISLAND_TRIGGER_IDS` **เป็น log-only, ไม่มี BUILD_IMPACT ต่อ production** แต่ถือเป็นตัวจำแนกที่ไม่ปลอดภัยถ้าใครเอาไปใช้ตัดสินโลก — บันทึกเป็นงานสำรอง (แคบ scope ด้วย scene/context ก่อนใช้อ้างอิงเกาะ) ยังไม่ทำรอบนี้ (ไม่บล็อกอะไร)
> ปิด `RE-227` ในรอบเดียวกันโดยอ้างผลนี้ (ดูหัวใบ `RE-227` ด้านบน)

## 🔬 RE-234 CLIENT-RESPONSE-PATH-FOR-TRIGGERVITAL-1FB2-ISLAND-001  [OPEN -- 🔴 `[STATIC-ON-BRIDGE]` · เจ้าของใบ/ผู้เขียนเนื้อใบ = **LANE-A** · ผู้บริโภคผล = LANE-A]

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `wjqykr`/R338 2026-09-04T14:0x+07:00** ตาม `COO-DECISION 20260904_1345` ข้อ 3(ง) และ `20260904_1346` ข้อ 2(จ) · ตัวนับร่วมสองคิวคืน `233` (`GT-233` รอบเดียวกัน) ⇒ ใบนี้ `234` · `RE-234`/`GT-234` = **0 hit ทั้งสามที่ก่อนวาง**
> **เนื้อใบเติมแล้วโดย LANE-A รอบ `0foax0` 2026-09-04T18:1x+07:00** (ข้อ 3 เพิ่มใหม่จากงานรอบนี้) · ใบนี้ **แทน** `0343` ข้อ 3 ฉบับเดิมที่ไล่จาก id 153/154 — คำทำนาย 153/154 ตกไปแล้วตาม `GT-228` ห้ามอ้างต่อ

- **คำถาม (ฉบับแคบ)**: (1) ไคลเอนต์ทำอะไรกับ **response** ของ `TriggerVital 0x1FB2` id 2/3 — มี handler ที่อ่านคำตอบของเซิร์ฟเวอร์ไหม หรือเป็นการแจ้งทางเดียว (2) เส้นทางที่เปิดหน้า "รายงานกัปตัน" มีกี่ทาง — `AddSurveyData` + เช็กระยะ ≤500 ในเครื่อง (สมมติฐานหลักตาม `RE-227`) เทียบกับ response ของ `0x1FB2` (ทางสำรอง) (3) [เพิ่ม LANE-A `0foax0`] id 2/3 ใน `TriggerVital` เป็น namespace เดียวกับ `TEXTDATA_TH__Trigger_TIP` (แถว 2 "Edmund Hidden Treasure" / แถว 3 "Seafood Cargo", R307's real id=3 capture during ordinary sailing) จริงไหม หรือคนละช่องเลขที่บังเอิญชนกัน — ถ้าคนละ namespace, `lane_hooks/lane_a_island_trigger_log.py`'s `M2_OBSERVED_ISLAND_TRIGGER_IDS` override ต้องแคบลง (เช่น กรองด้วย scene_id/context ที่ยิง แทนการจับคู่ id เปล่า ๆ)
- **ทำไม**: ถ้า `GT-233` ไม่เด้ง ใบนี้คือทางเดียวที่บอกว่ากลไกผิดที่ provisioning หรือผิดที่การไม่ตอบ trigger · ข้อ 3 ทำไม: ตอนนี้ responder log-only พิมพ์ ISLAND ผิดให้เฟรม Seafood Cargo ของจริง (R307) เป็นความเสี่ยงที่ยอมรับไว้ชั่วคราว ไม่ใช่ถาวร
- **route**: `STATIC-ON-BRIDGE` (ต้องดิสแอสเซมภาพไคลเอนต์ ทำบนคลาวด์ไม่ได้)
- **ห้ามอ้าง**: ชื่อ prop ใน `TEXTDATA_TH__Trigger_TIP` เป็นคนละ namespace จนกว่าจะพิสูจน์ตรงข้าม (`COO 1345` ข้อ 1)
- **ลิงก์**: `pirate-force-server#753` (โค้ดที่ใบนี้จะตัดสิน) · `20260904_1331_KA1A-R308-RESULTS-*` · `20260904_1345_COO-DECISION-*`

---

## 🔬 RE-235 BLACK-MARKET-AND-SHIP-SURVEY-WINDOW-OPCODES-001  [OPEN -- 🔴 `[NEEDS-ATTENDED-CAPTURE]` · เจ้าของใบ/ผู้เขียนเนื้อใบ = **LANE-UI** · ผู้บริโภคผล = LANE-UI]

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `wjqykr`/R338** ตาม `COO-DECISION 20260904_1346` ข้อ 2(ฉ) · ที่มา `notes_to_chief/20260904_1137_LANE-UI-RE-TICKET-black-market-and-ship-survey-window-opcodes-not-in-r38-registry.md` · ตัวนับร่วมสองคิวคืน `234` ⇒ ใบนี้ `235`
> 🆕 **เนื้อใบลงโดย LANE-UI รอบ `llcmcr` (2026-09-05)** — ยกจากบทสรุปที่ใบต้นทาง `1137` วัดไว้แล้วสามรอบติด (`c2a7nc`/`p7m2wq`/`h4wnbz`) แล้ว re-derive ซ้ำในรอบนี้เอง (ไม่ก๊อปเลขเก่ามาโดยไม่เช็ค)

**คำถาม**: opcode จริงของ 7 คลาสตลาดมืด (`GSCN_BlackMarket*`) + `NavigationEx_RequestSurveyVtial` (หน้าต่างสำรวจ/salvage ของเรือผู้เล่น) คืออะไร -- ทั้งหมดมี field schema resolved จาก static แล้ว (บางคลาสครบ บางคลาสยังไม่ครบ) แต่ไม่มีชื่อคลาสไหนเลยเคยถูกดึงออกมาเป็นสตริงในรอบ R38 ⇒ ไม่มี VA/opcode ให้ผูก

🔴 **กันสับสนก่อน**: `NavigationEx_RequestSurveyVtial` (ปุ่มสำรวจ/salvage ในหน้าต่างเรือของผู้เล่น -- ใบนี้) เป็นคนละคลาสกับ `NavigationEx_AddSurveyDataVtial`/`NavigationEx_EnterInstanceVital` (กลไกเทียบท่าเกาะของ M2 ที่ LANE-A/chief ทำอยู่ตาม `NOW.md` -- `RE-227`/`GT-228`/`RE-234`) แค่ prefix `NavigationEx_` เหมือนกัน คนละ opcode คนละฟีเจอร์ ไม่แตะเขต M2

**ค้นก่อนถอด** (`RE_STATIC_SEARCH_RULES.md`, re-derive รอบนี้ ไม่ใช่ก๊อปผลเก่า):
1. `pf_bridge/external/00_SEARCH_HERE_FIRST.md` → `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (R38 string-recovery) — `grep -in "blackmarket"` และ `grep -in "requestsurvey"` **ยัง 0 hit ทั้งคู่** (verify รอบ `llcmcr`) — ไฟล์นี้มีแค่ **327 ชื่อ** จากทั้งหมด **519 คลาส** ที่ลงทะเบียนใน `external/PF_PROTOCOL_REGISTRY.tsv` (comment หัวไฟล์ยืนยันว่าเป็นสตริงที่ค้นเจอจริงในภาพเท่านั้น) ⇒ "ไม่อยู่ในไฟล์นี้" = "ยังไม่เคยเจอเป็นสตริงในรอบ R38" ไม่ใช่ "ไม่มี opcode จริง"
2. `external/PF_SERIALIZER_FIELDS.tsv` — field แถวของทั้ง 7 คลาสมีจริง (verify รอบ `llcmcr`: `grep -n "^GSCN_BlackMarket\|^NavigationEx_RequestSurveyVtial"` ตอบ 104 บรรทัด) — ดูตารางด้านล่าง
3. `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`: `grep -in "blackmarket\|navigationex_requestsurvey"` — **0 hit ทั้งไฟล์นอกจากเนื้อใบนี้เอง** (verify รอบ `llcmcr`, แก้คำอ้างเดิมที่ผิด — regex นี้ไม่ชน `RE-073` จริง เพราะบรรทัดนั้นไม่มีคำว่า `blackmarket` หรือ `navigationex_requestsurvey` ตรงตัว) · ค้นกว้างขึ้นด้วย `grep -in "ตลาดมืด\|survey"` เจอ `RE-073 TEST-STAGE-GEOMETRY-SURVEY-001` (archived, คนละเรื่อง — เวทีเทสภูมิศาสตร์ ไม่ใช่ตลาดมืด/เรือ) และผลลัพธ์ `NavigationEx_` อื่นทั้งหมดเป็นของ `AddSurveyDataVtial`/`EnterInstanceVital` (M2) — ไม่มีใบซ้ำของหัวข้อนี้จริง
4. `gamedata\` — ไม่ใช่ตารางข้อมูลเกม (opcode/field เป็นเรื่อง wire ไม่ใช่ข้อความ/ค่าคงที่) ข้ามตามขอบเขตของกฎบังคับข้อสอง

**วัดมาแล้ว** (`external/PF_SERIALIZER_FIELDS.tsv`, grep ทีละคลาส):

| คลาส | ฟิลด์ (real/total) | opcode |
|---|---|---|
| `GSCN_BlackMarketPutOnSale` | 8/8 ครบ | ไม่มีใน registry |
| `GSCN_BlackMarketOffSale` | 2/2 ครบ | ไม่มีใน registry |
| `GSCN_BlackMarketBuy` | 4/4 ครบ | ไม่มีใน registry |
| `GSCN_BlackMarketSearchMyItem` | 0/2 -- ทั้งคู่พิสูจน์แล้วว่า `EMPTY` (body ไม่เขียนอะไรเลย ไม่ใช่ `UNKNOWN`) | ไม่มีใน registry |
| `GSCN_BlackMarketSearach` (สะกดแบบนี้จริงในตาราง) | 12/12 ครบ | ไม่มีใน registry |
| `GSCN_BlackMarketSearchReply` | 20/40 ยังไม่ครบ | ไม่มีใน registry |
| `GSCN_BlackMarketReply` | 18/34 ยังไม่ครบ | ไม่มีใน registry |
| `NavigationEx_RequestSurveyVtial` | 2/2 ครบ ทั้ง R/W (`0x0B` `+0x14` len 1 -- `RE-086`/`RE-087` ปิดไว้แล้วว่าค่าคงที่ `5`) | ไม่มีใน registry |

**สรุป**: ปิดจาก static เดี่ยวไม่ได้ -- ไม่ใช่เพราะไม่มีคนเช็ค (เช็คแล้วสี่รอบติดนับใบนี้) แต่เพราะสตริงชื่อคลาสไม่เคยถูกดึงออกมาในรอบ R38 เลย ทางเดียวที่เหลือคือ **dynamic capture** (เห็นเฟรมจริงบนสาย) หรือ static extraction รอบใหม่ที่ครอบคลุม 519 คลาสแทน 327 (นอกเขตของ LANE-UI -- ของทีม static/RE)

**สิ่งที่ต้อง capture** (attended, ผู้เล่นเปิดหน้าต่างตลาดมืด/หน้าต่างเรือแล้วกดจริง): ลำดับความสำคัญ **`Buy`/`PutOnSale` ก่อน** (ธุรกรรมหลักของตลาดมืด — field ครบทั้งคู่ พร้อมผูก opcode ทันทีที่เห็นเฟรม) ตามด้วย `OffSale`/`SearchMyItem`/`Searach`/`NavigationEx_RequestSurveyVtial` — **`SearchReply`/`Reply` ไม่ขอรอบนี้** (field ยังไม่ครบ 20/40 และ 18/34 รอปิดฟิลด์ก่อนถึงจะ capture มีประโยชน์เต็มที่)

- **route**: `NEEDS-ATTENDED-CAPTURE` (ไม่มีทางลัด static — ชื่อคลาสไม่เคยเป็นสตริงในภาพที่ค้นแล้ว)
- **ห้ามอ้าง**: การคำนวณ hash ชื่อคลาสเองด้วยสูตรที่ R38 ใช้ (`sum((i+1)*ord(c) for i,c in enumerate(name)) & 0xFFFF`) เป็นหลักฐาน — `FACTPACK_L2_CLASSCENSUS001_20260820.md` nonclaim⑤ เขียนไว้ตรง ๆ ว่า `wire_id` แบบ derive เองสำหรับชื่อที่ไม่เคยเจอเป็นสตริงจริง "ไม่ได้อ่านจากตารางในภาพ ไม่ใช่หลักฐาน" (ห้ามเดา opcode แล้วส่งไบต์ออกตามกติกา §0)
- **ลิงก์**: `notes_to_chief/20260904_1137_LANE-UI-RE-TICKET-black-market-and-ship-survey-window-opcodes-not-in-r38-registry.md` (บทสรุปต้นทาง) · `notes_to_chief/20260904_1159_LANE-UI-TO-COO-catalog-complete-*.md` (สถานะสารบัญ 15 แถว)

### result:
(ว่าง — รอ attended capture)

---

## 🔬 RE-236 TRACEPATH-RECORD0-SEMANTIC-ATTENDED-DIFFERENTIAL-001  [🟢 ANSWERED (ทั้งสองข้อปิดแล้ว) — ข้อ (ก) มินิแมป ปิดแล้ว (REFUTED ผ่าน `GT-246`/R310) · ข้อ (ข) ปิดรอบ `9xqzh0` 2026-09-05T12:2x+07:00 ผ่าน `GT-251`/R317 (ดูข้อ (ข) ข้างล่าง) · เจ้าของใบ/ผู้เขียนเนื้อใบ = **LANE-UI** · ผู้บริโภคผล = LANE-UI]

### 🆕 ข้อ (ข) ปิดรอบ `9xqzh0` — ปิดผ่าน `GT-251` (R317) ไม่ใช่ผ่านการชนตัวเลขที่ไม่ชนกัน (COO-DECISION `20260905_1151` สั่งปิด)
`notes_to_chief/20260905_1125_KA1A-R317-RESULTS-*.md` (`GT-251`, attended, 2026-09-05T11:25+07:00): ผู้เทส
กด GO! เล็งสามเป้าหมายต่างกันในหน้าต่าง "ค้นหาตัวละครในฉาก" (Antique Store Love Millie · Finance
Administrator Locher · Harbor Bulletin 2) แล้วเทียบ u16 ที่ยิงออกกับ `gamedata/tables/
CONSTDATA_TH__MOBS.tsv` (`n_ID` คอลัมน์ 1):

| คลิก | เป้า | u16 ที่ยิง | `CONSTDATA_TH__MOBS.tsv` แถว | `n_ID`/`s_NAME` ที่บรรทัดนั้น |
|---|---|---|---|---|
| #236 11:09:57 | Antique Store Love Millie | **157** | บรรทัด 154 | `157	愛蜜莉` (`s_ICON=Icon_Map_Shop`) |
| #263 11:10:49 | Finance Administrator Locher | **161** | บรรทัด 158 | `161	洛克` (`s_ICON=Icon_Map_Warehouse`) |
| #302 11:12:06 | Harbor Bulletin 2 | **153** | บรรทัด 151 | `153	港區第二公佈欄` (`s_OUTFIT=BULLETIN_BOARD`) |

**ตรงกัน 3/3 แบบ exact** (`grep -n "^153\|^157\|^161" gamedata/tables/CONSTDATA_TH__MOBS.tsv` ยืนยันสาม
บรรทัดนี้ตรงคอลัมน์ 1 เป๊ะ) และ**ไม่ใช่ลำดับแถวที่คลิก** (แถว 1→157 · แถว 5→161 · แถวท้าย→153 — ไม่เรียง
ตามลำดับที่คลิกเลย) ⇒ **ตัด list-index ทิ้งได้เต็มรูป**

🔴 **ความซื่อสัตย์ที่ต้องพูดตรง ๆ (ไม่ใช่การปิดแบบสะอาดตามสูตรเดิมของ RE-236)**: วิธีปิดที่ `RE-119` T4/`RE-236`
เขียนไว้เองต้องการ "สองเป้าที่ `QUEST.n_ID`/`MOBS.n_ID` ไม่ชนกัน" — รอบนี้ตรวจซ้ำแล้วพบว่า **ไม่ชนจริง**: ทั้ง
153/157/161 มีแถวอยู่ใน `gamedata/tables/QUESTDATA_TH__QUEST.tsv` คอลัมน์ 1 ด้วยเหมือนกัน (บรรทัด 118/122/126
ตามลำดับ — เดียวกับปัญหาที่ 743 เคยชนทั้งสองตารางมาก่อน) ⇒ **เกณฑ์ "ไม่ชนตัวเลข" ที่ใบเดิมกำหนดไว้ ไม่ผ่านจริง
ๆ ตามตัวอักษร**. เหตุผลที่ปิดใบได้ทั้งที่ตัวเลขยังชน (ตาม `COO-DECISION 20260905_1151` ข้อ 3 สั่งปิดตรง ๆ):
หน้าต่าง "ค้นหาตัวละครในฉาก" ที่ผู้เทสคลิกเป็น**หน้าต่างแสดงเฉพาะแถว NPC/วัตถุ** (R317 เขียนเองว่า "ไม่มีหมวด
เควส/จุดสำรวจแยก") — ผู้เล่นไม่มีทางเลือกแถวเควสจากหน้าต่างนี้ได้เลย ดังนั้น**แหล่งที่มาของคลิก** (โครงสร้างของ
UI ที่คลิก ไม่ใช่ตัวเลขที่ชนกันหรือไม่) คือสิ่งที่ตัดสินความหมาย ไม่ใช่การชน/ไม่ชนของตัวเลขในตาราง — หลักฐานนี้
เป็นคนละชั้นจาก numeric-collision test เดิม และไม่ถูกหักล้างโดยการชนที่พบใหม่

**ค่า 743 (RE-119 T4 เดิม)**: ปิดพร้อมกันด้วยเหตุผลเดียวกัน = **`[เสนอ]` MOBS n_ID** ("Jail Dead Prisoner")
จนกว่าจะมีตารางยืนยันเพิ่มเติม (ตาม `COO-DECISION 20260905_1151` ข้อ 3 ระบุคำนี้ตรง ๆ) — ไม่ยกระดับเป็น
proven เต็มรูปเพราะย้อนกลับไป 743 ไม่มีบันทึกว่าคลิกมาจากหน้าต่างชนิดไหน (แตกต่างจาก 157/161/153 ที่ R317
ยืนยันแหล่งคลิกชัดเจน)

**หมายเหตุรูปเฟรม**: ทั้งสามคลิกนี้ (#236/#263/#302) ยิงเฟรม `0x4391` **45 ไบต์** — คนละรูปกับเฟรม 25 ไบต์
ที่ `ui_tracepath_wire.TracePathReqFields`/`GT-246`/มินิแมปใช้ (คนละ field-count/tag pattern) แม้เป็น
opcode เดียวกัน ⇒ field1_u16 ของ schema 25-byte เดิม **ยังไม่เคยถูกวัดค่าไม่ใช่ 0 เลยสักครั้ง** (มินิแมปคลิกใน
R317 เอง #328/#333 ก็ยัง 0 เหมือน `GT-246`) — คำถามเดิมของ RE-236(ข) เกี่ยวกับ schema 25-byte ปิดด้วย
"ไม่เคยมีตัวอย่าง nonzero ให้ตัดสิน" ส่วนคำถามที่ตอบได้จริงคือกลไกระดับ frame-shape/UI-source ของ schema
45-byte ใหม่นี้แทน — ตัวถอดรหัส id ของ schema 45-byte (พิสูจน์เฉพาะ prefix 5 ไบต์แรกจากตัวอย่าง #236 เท่านั้น
ไม่ใช่ทั้งเฟรม) อยู่ที่ `src/pirateforce_foundation/ui_tracepath_wire.py`
`read_trace_path_go_target_id_prefix` (รอบ `9xqzh0`, `pirate-force-server`)

**RE-119 T4 ปิดพร้อมกัน**: สถานะเปลี่ยนจาก "bounded negative ระหว่างสามทาง" เป็น "NPC `n_ID` [เสนอ] ตาม
หลักฐาน source-window ข้างบน — list index ตัดทิ้งแล้ว quest id ยังไม่ตัดทิ้งด้วยตัวเลขอย่างเดียว (ต้องอาศัย
source window เหมือนกัน)"

### nonclaims (การปิดรอบ `9xqzh0`)
① ไม่อ้างว่า numeric-collision test ของ RE-236/RE-119 T4 เดิมผ่านจริง — grep ยืนยันชนทั้งสองตาราง (บรรทัด
`QUESTDATA_TH__QUEST.tsv:118/122/126`) การปิดอาศัยหลักฐานคนละชั้น (source window) ตามที่ COO สั่งชัดเจน ไม่ใช่
การอ้างว่าเกณฑ์เดิมผ่าน
② ไม่อ้างว่า schema 25-byte เดิม (`TracePathReqFields.field1_u16`) มีความหมาย NPC id — ยังไม่เคยสังเกตค่า
nonzero เลย คนละ frame กับที่ปิดรอบนี้
③ ไม่อ้างว่าเฟรม 45-byte ของ #236/#263/#302 ถูกถอดรหัสครบทั้งเฟรม — มีแค่ prefix 5 ไบต์แรก (id field) ที่มี
หลักฐานพอ ส่วนที่เหลือของเฟรม (~40 ไบต์) ยังไม่มีใครถอด (เสนอเป็นใบ RE แยกให้ chief พิจารณา ไม่บล็อกฟีเจอร์นี้)
④ ไม่อ้างว่า 743 พิสูจน์เป็น NPC id เต็มรูป — ยังเป็น `[เสนอ]` ตามที่ COO สั่งไว้ตรง ๆ

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `wjqykr`/R338** ตาม `COO-DECISION 20260904_1346` ข้อ 2(ฉ) และ `20260904_1244` (มินิแมป = แถว auto-walk ไม่เปิดใบ RE แยก) · ที่มา `notes_to_chief/20260904_1226_LANE-UI-RE-TICKET-tracepath-record0-semantic-needs-attended-differential.md` · ตัวนับร่วมสองคิวคืน `235` ⇒ ใบนี้ `236` · **0 hit ทั้งสามที่ก่อนวาง**
> 🆕 **เนื้อใบลงโดย LANE-UI รอบ `5u9bio` (2026-09-04)** — ใบนี้จองเลขไว้ตอบสองข้ออ้างพร้อมกัน (ต้นทาง `1226`): (ก) มินิแมป = `TargetPosVital` เหมือนคลิกพื้นหรือไม่ (ข) `u16@+0x14` ของ request คือ quest id / NPC id / list index

### ข้อ (ก) มินิแมป — ปิดแล้ว REFUTED
`GT-246` (`GAME_TEST_QUEUE.md:13639`, ANSWERED, วัดจริงรอบ attended R310 2026-09-04 18:52:12 — ผู้ขับ Panya
ผู้วัด ka1-A) จับเฟรมจริงตอนคลิกมินิแมป: **`CTracePathReqVital 0x4391` (25 B)** ไม่ใช่ `TargetPosVital`
ตามที่สารบัญ LANE-UI เดาไว้แต่แรก — คลิกพื้น 1 ครั้งในเซสชันเดียวกันยิง `TargetPosVital` เท่านั้น (ไม่มี `0x4391`)
คลิก NPC ยิง `TargetVital`+`ChooseNPC` (ไม่แตะ trace-path เลย) ⇒ **สมมติฐานเดิม "มินิแมป = คลิกพื้น" ถูกหักล้าง
เต็มรูป** นี่คือ finding ของใบนี้ ไม่ใช่ความผิดพลาดของใคร (`COO-DECISION 20260904_1244` ข้อ 2 อนุมัติให้พับคำถาม
มินิแมปเข้าชุด differential เดียวกันไว้แล้ว — ข้อนี้คือคำตอบ)

### ข้อ (ข) `u16@+0x14` = 743 คืออะไร — ยังเปิด ต้อง attended รอบใหม่
`RE-119` T4 ทิ้งไว้ bounded-negative: ค่าเดียวที่เคย capture (`743`) ชนทั้ง `QUESTDATA_TH__QUEST.tsv n_ID=743`
(ฉาก 5) และ `CONSTDATA_TH__MOBS.tsv n_ID=743` ("Jail Dead Prisoner") พร้อมกัน — เลขตรงกันสองตารางพิสูจน์
semantic ไม่ได้ **R310 ไม่ได้ทำขั้นที่ปิดข้อนี้** (คลิก NPC ของ R310 คือ `TargetVital`/`ChooseNPC` เลือกเป้า
ไม่ใช่การกด GO! เดินอัตโนมัติ ⇒ ไม่มีเฟรม `0x4391` ตัวที่สองที่มี discriminator ต่างค่าให้เทียบ)

🆕 **บอนัสสถิตรอบนี้ (LANE-UI + `pf-static-re`, ไม่ต้องเครื่อง)**: ถอดรหัส payload `0x4391` 25 ไบต์ที่ `GT-246`
จับไว้จากคลิกมินิแมป (`0F00000F000014000000000F01000F65010FB2000F007D0802`) ตรงกับ schema ของ `RE-119`
(`external/PF_SERIALIZER_FIELDS.tsv:5521-5528`, 8 ฟิลด์ ตรงทุก tag ไบต์ ไม่มีไบต์เหลือ) ได้ค่า:
`+0x14=0` (discriminator) · `+0x16=0` · `+0x18=0` · `+0x1C=1` · `+0x1E=357` · `+0x20=178` · `+0x22=32000` ·
`+0x24=2` — **ผลสองข้อ**: (1) discriminator `=0` สำหรับคลิกมินิแมป (ไม่มีเป้า NPC/quest) เป็นตัวอย่างจริงที่
**ยังไม่แยกสามทางเดิม** (quest id / NPC id / list index — คลิกมินิแมปไม่มีเป้าจึงเป็น "ไม่มี" ได้ทั้งสามทาง
ไม่ตัดสิน) (2) ⚠️ **แก้ท้ายรอบ `5u9bio` (pf-adversary จับได้)**: ข้ออ้างเดิม "RE-119 บันทึกว่าเป็น 0 เสมอ" อ้างแค่
บรรทัดสรุปใน `CLIENT_RE_QUEUE.md:1598-1600` ซึ่งพูดถึงแค่ capture เดียว ไม่ใช่ข้อเท็จจริงที่แรงกว่านั้นที่มีอยู่จริง:
ใบผลเต็มของ `RE-119` (`archive/notes_to_chief_2026-08/20260828_0424_RE-119-RESULT-*.md` T4 บรรทัด 63) ระบุจาก
**disassembly ตรง** ว่า **request constructor `0x006EBA90` zero ฟิลด์ `+0x14..+0x24` ทุกครั้งที่สร้าง request**
— นี่คือข้อเท็จจริงระดับ image ไม่ใช่แค่ค่าที่บังเอิญเป็น 0 ในตัวอย่างเดียว ⇒ เฟรมมินิแมปของ `GT-246` ที่มีค่าจริง
`+0x1C=1 · +0x1E=357 · +0x20=178 · +0x22=32000 · +0x24=2` **ขัดกับข้อเท็จจริงระดับ constructor นี้โดยตรง**
(ไม่ใช่แค่ "ไม่จริงเสมอไปในตัวอย่างที่มี") ความหมายของค่าเหล่านี้ (พิกัดมินิแมป? หรืออื่น) **ยังไม่มีใครตัดสิน ไม่เดา**

**วิธีปิดข้อ (ข) ที่เหลือ (ตามที่ `RE-119` T4 กำหนดไว้เอง — ไม่เปลี่ยน)**: ผู้เทสกด **GO!** เล็งเป้าหมายสองจุดที่
ค่า `QUEST.n_ID`/`MOBS.n_ID` ของมันไม่ชนกัน (เช่น NPC ตัวหนึ่ง + จุดสำรวจ/เควสอีกจุดที่ n_ID ต่างกันชัดเจน) แล้วดู
`u16@+0x14` ของสองเฟรมที่ส่งออกมาต่างกันตามตัวไหน (quest id ของเควสที่เลือก / NPC id ของเป้าหมาย / index ใน
รายการที่คลิก) — ปิดขาดถ้าค่าตรงกับตัวแปรใดตัวหนึ่งชัดเจน 2/2 ครั้งขึ้นไป bounded-negative ถ้ายังชนสองทางเหมือนเดิม
· อยู่ใน "รอเครื่องคุณ" ของ `NOW.md` เมื่อ chief จัดคิว — **ไม่บล็อก LANE-UI** ระหว่างรอ

🔴 **คำถามแยกอีกข้อที่พบระหว่างบอนัสสถิตรอบนี้ (ยังไม่ตัดสิน ไม่ใช่ของใบนี้)**: `RunFindPath`
(consumer ของ response ที่ไม่ว่าง, handler VA `0x006EACE0` class `CGCTracePathModule` —
`external/PF_PROTOCOL_REGISTRY.tsv:376`) เดินเองยิง `TargetPosVital` ทีละ leg หรือกลไกอื่น — **ยังไม่มีใคร
ไล่ static ต่อ** เพราะสคริปต์ disasm ที่ `RE-119` อ้างไว้ (`staged/re119_disasm_probe.py` ทำนองนั้น) ไม่อยู่ใน
clone นี้ (ต้องใช้ `GameClient.local.bin` จริงที่มีแต่บนเครื่อง Panya/สะพาน) — ไม่ใช่ของบังคับใบนี้ ถ้า
chief/pf-static-re บนสะพานมีคิวว่างเสนอให้ไล่ต่อ

🔴 **แก้ท้ายรอบ `5u9bio` — คำถามที่สองที่บอนัสสถิตนี้เปิดจริง ๆ (pf-adversary ชี้ให้เห็น)**: ถ้า constructor
`0x006EBA90` zero ฟิลด์ `+0x14..+0x24` ทุกครั้งตามที่ `RE-119` T4 พิสูจน์จาก disassembly แล้วเฟรมมินิแมปของ
`GT-246` กลับมีค่าไม่เป็นศูนย์ที่ `+0x1C..+0x24` — **มีจุดเขียนที่สอง (write site) ที่ยังไม่มีใครบันทึกไหม** (เช่น
เข้ารหัสพิกัด x/y ของมินิแมปทับค่าที่ constructor zero ไว้ก่อนส่ง) แยกจากจุดเขียน `+0x14` เดิมที่ `RE-119`
เจอแล้ว (serializer `[0x006EBAF0,0x006EBBF7)` เขียน `+0x14` เป็น tag แรก) — `PF_SERIALIZER_FIELDS.tsv:5521-5528`
ระบุแค่ตำแหน่ง/ขนาดของทุกฟิลด์ ไม่ได้แยกว่าฟิลด์ไหนมี write site กี่จุด **ไม่มีใครไล่ disassembly กลับไปตรวจ**
ว่า `+0x1C..+0x24` มี writer อื่นนอกจาก constructor หรือไม่ — เป็นคำถามสถิตล้วน (ไม่ต้องเครื่อง) ถ้า chief/
pf-static-re มีคิวว่างเสนอให้ไล่ต่อพร้อมกับข้อ `RunFindPath` ข้างบน

## nonclaims (บอนัสสถิตรอบนี้)
① ไม่ยืนยันความหมายของ `+0x14=0` ในเฟรมมินิแมป — เป็นตัวอย่างจริงหนึ่งค่า ไม่ตัดสามทางเดิม (quest id / NPC id /
list index) และไม่เพียงพอจะอ้างว่า "ตัด" สมมติฐานอื่นใดที่ไม่มีใครตั้งไว้มาก่อน
② ไม่เดาความหมายของ `+0x1C/+0x1E/+0x20/+0x22/+0x24` (1/357/178/32000/2) — ตัวอย่างเดียว ไม่มีหลักฐานอื่นยืนยัน
   (ดูคำถาม write-site ที่สองข้างบน — ยังไม่ตอบ)
③ ไม่ไล่ static ต่อที่ `0x006EACE0` เอง หรือที่ constructor `0x006EBA90` เอง (binary ไม่อยู่ใน clone นี้) —
   เป็นคำถามแยกสองข้อ ไม่ใช่ข้อบังคับของใบนี้
④ การถอดรหัสใช้ hex ที่ `GT-246` จับไว้แล้ว (ไม่ใช่ capture ใหม่) เทียบกับ schema ที่ `RE-119` ปิดไว้แล้ว — ไม่มี
ไบต์ใหม่ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้
⑤ **เติม `5u9bio` แก้ท้ายรอบ**: `pf-adversary` รอบแรกของใบนี้ตรวจแล้วพบจุดแก้สองจุด (คำพูด "RE-119 บันทึกว่าเป็น
0 เสมอ" อ้างสั้นเกินไปไม่ถึงข้อเท็จจริงระดับ constructor · คำว่า "ตัดสมมติฐานไม่เป็นศูนย์เสมอ" ไม่มีใครตั้งสมมติฐาน
นั้นไว้จริงในคลังมาก่อน) — แก้ทั้งสองจุดแล้วในบล็อกข้างบน (`pf_bridge#1221`) · **`pf-adversary` รอบสอง (รีวิว
เฉพาะการแก้) กลับผลแล้ว: สะอาด** ไม่พบจุดผิดเพิ่ม ยืนยันการอ้าง `archive/notes_to_chief_2026-08/20260828_0424_*.md`
บรรทัด 63 ตรงตามต้นฉบับ + คำว่า "ตัดสมมติฐาน" หายจากทุกจุดที่เคยอ้างเป็นข้อสรุปแล้วจริง ⇒ `ADVERSARY_PENDING` ของ
รอบ `5u9bio` **ปิดแล้ว** ไม่ต้องหยิบเป็นงานแรกรอบถัดไปอีก
⑥ **คำถามใหม่จาก adversary รอบสอง (ยังไม่ตอบ ไม่ใช่ของใบนี้)**: เฟรมมินิแมปของ `GT-246` ยืนยันแล้วว่าตรง wire
schema เดียวกับที่ `RE-119` ถอด (`PF_SERIALIZER_FIELDS.tsv:5521-5528`) แต่ **ยังไม่ยืนยันว่ามาจาก constructor
`0x006EBA90` ตัวเดียวกันที่ `RE-119` ไล่ disassembly จริง** — "schema เดียวกัน" กับ "constructor เดียวกัน" เป็น
คนละเรื่อง ถ้าเป็นคนละ construction site (คลาส/ฟังก์ชันอื่นที่ใช้ schema เดียวกันแต่ initialize ต่างกัน) คำถาม
write-site ที่สอง (nonclaim② ข้างบน) อาจไม่มีอยู่จริง — เป็นแค่ category mismatch ไม่ใช่ write site ใหม่ ต้องไล่
static เพิ่มเพื่อแยกสองทางนี้ (ต้องการ binary จริงเหมือนคำถามอื่นในใบนี้ ไม่ใช่ของบังคับ)

---

## 🔬 RE-237 OPTIONS-APPLY-SERVER-SETTING-VITAL-FIELDS-001  [🟡 PENDING -- `[NEEDS-ATTENDED-CAPTURE]` เนื้อใบเขียนแล้ว · **GT คู่ = `GT-253`** (PENDING, `GAME_TEST_QUEUE.md`) · หัวแก้โดย chief (LANE-E) รอบ `cooif2`/R357 ตาม `COO-DECISION 20260905_1545` ข้อ 3 · เจ้าของใบ/ผู้เขียนเนื้อใบ = **LANE-UI** · ผู้บริโภคผล = LANE-UI]

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `wjqykr`/R338 2026-09-04T14:0x+07:00** · ที่มา `notes_to_chief/20260904_1054_LANE-UI-RE-TICKET-options-apply-server-setting-vital-fields-need-dynamic-capture.md` · ตัวนับร่วมสองคิวคืน `236` ⇒ ใบนี้ `237` · `RE-237`/`GT-237` = **0 hit ทั้งสามที่ก่อนวาง**
> เนื้อใบยกลงมาจากจดหมายต้นทางข้างบน (รอบ `vt83nk`, แก้ท้ายรอบ `fx9k2p`) — **แก้ไขจากต้นฉบับหนึ่งจุด**: ส่วน
> "ขอ RE"/เกณฑ์ PASS-FAIL ของต้นฉบับเสนอ breakpoint บนไบนารีไคลเอนต์ (callee body, vtable slot resolution,
> object identity ที่ `ECX+0x0C`) — ตรวจแล้วว่าเครื่องมือผู้เทส attended ของโปรเจกต์นี้ (`AGENTS.md`,
> `BRIDGE_BOOT_PROCEDURE.md`) ไม่มีความสามารถ debugger/memory-breakpoint บนไคลเอนต์เลย มีแค่บูต+คลิก+เก็บ
> เฟรม/คอนโซล ⇒ เกณฑ์เดิมทำไม่ได้จริง (ต้นฉบับเองก็ติดป้าย `[PROPOSED]` ไม่ยืนยันความเป็นไปได้ไว้แล้ว ในnonclaim⑦)
> **แทนที่ด้วยแผน differential แบบ wire-only** ด้านล่าง ซึ่งใช้เครื่องมือที่มีอยู่แล้วเท่านั้น (เก็บเฟรมขาออก
> เทียบกันข้าม trial ไม่ใช่แกะภายในไคลเอนต์) — รูปแบบเดียวกับที่ปิดคำถามคล้ายกันมาแล้วในโปรเจกต์นี้ (`RE-236`
> "กด GO! สองเป้าไม่ชน id แล้วดู u16 ต่างกัน", `RE-155` "A/B ฟิลด์เดียว")

### ทำไมใบนี้ถึงมีอยู่
ปุ่ม Options→Apply (`UserSetting_UpdateServerSettingVital`) ส่งเฟรมจริงมาแล้ว **197 ครั้งจาก 117 ไฟล์แคปเจอร์**
ในคลังที่สแกนแล้ว (`external/PF_FIELD_VALIDATION.tsv:858`, ทิศ **W** เท่านั้น — ทิศ R ไม่เคยถูกสังเกตเลย
สอดคล้องกับที่นี่เป็นปุ่มฝั่งไคลเอนต์ส่งค่าตั้งค่าเข้ามา ไม่ใช่ของที่เซิร์ฟเวอร์ต้อง push กลับ) แต่ TSV นั้นเก็บแค่
ตัวนับ match/mismatch ไม่เก็บ**ค่าไบต์จริง**ของแต่ละครั้ง ⇒ ปิดจาก static/ข้อมูลที่ commit ไว้แล้วอย่างเดียว
ไม่ได้ (ไม่มีอาร์ไคฟ์แคปเจอร์ดิบอยู่ในโคลนคลาวด์นี้เลย) จาก `external/PF_SERIALIZER_FIELDS.tsv:6167-6178`
(12 แถว, 6 ฟิลด์ × ทิศ R/W) resolved แค่ 2/12 แถว (field 1-W, field 2-R — tag `0x0B` `STACK@+0x18` len=1)
เหลือ 4 ฟิลด์ (3, 4, 5, 6) ที่ static เดี่ยวปิดไม่ได้

### ค้นก่อนถอด (`RE_STATIC_SEARCH_RULES.md`, ยกจากจดหมายต้นทาง)
1. `external/PF_SERIALIZER_FIELDS.tsv` แถว 6167-6178 (`grep -n "^UserSetting_UpdateServerSettingVital"`) —
   6 ฟิลด์เต็ม ทิศ R+W ต่อฟิลด์ (12 แถว) caller เดียวกันหมด `0x00721D10-0x00721DB4`
2. `grep -rl "0x00720FC0"` ทั้งรีโป (`external/` + `notes_to_chief/reference_codex_attr/` + ราก) — เจอเฉพาะ
   สองแถวของ field 3 เอง ไม่เคย resolve เลขนี้ที่ไหนมาก่อน ไม่มี precedent ข้าม vital
3. `grep -c "INDIRECT(DEREF(DEREF(DEREF(OBJ+0x14))+0x34))"` ทั้ง `PF_SERIALIZER_FIELDS.tsv` — pattern เดียวกับ
   field 1-R/2-W/6 เจอ 52 แถว ข้าม 13 ข้อความ ทุกแถว (52/52) ยัง `UNKNOWN(indirect_call_not_proven_serializer_slot)`
   ไม่เคย resolve สักที่เดียว
4. `notes_to_chief/reference_codex_attr/PF_SERIALIZER_FIELDS.md:10-11` + `PF_HANDOFF_V1.md:228-229` — field 4/5
   คือ `InterlockedIncrement`/`InterlockedDecrement` ที่ `ECX+0x0C` พิสูจน์ byte-exact จริง แต่เอกสารวิธีการของ
   โปรเจกต์เองปฏิเสธเรียกว่า "refcount" เพราะพิสูจน์ไม่ได้ว่าอ็อบเจกต์นั้นไม่ alias กับ stream ที่ serialize จริง
5. `external/PF_FIELD_VALIDATION.tsv` (ชั้น CAPTURE คนละชั้นกับ IMAGE — ห้าม merge ตาม
   `PF_PROTOCOL_PRIORITY.md:12`): W จริง 197/117 ไฟล์ ชนขอบ static เดียวกันเสมอ (`mismatch=0`) · R ไม่เคยสังเกต
6. `grep -i "เฟือง\|serversettingvital"` — `CLIENT_RE_QUEUE.md` 0 hit (ไม่เคยเปิดใบนี้มาก่อน) ·
   `GAME_TEST_QUEUE.md` 1 hit (บรรทัด **273** ตามที่ derive สดรอบนี้ — จดหมายต้นทาง `1054` เคยอ้าง 271 ด้วย
   `git blame` ตอนที่เขียน แต่มีบรรทัดถูกแทรกก่อนหน้าโน้ตนั้นตั้งแต่ ⇒ เลื่อนไปสองบรรทัด แก้เลขที่นี่ ไม่แก้จดหมาย
   เดิม ตามธรรมเนียมไฟล์นี้ · โน้ตนำทาง UI-A/UI-B "ปุ่มเฟือง = OPTIONS ไม่ใช่ logout" ไม่ใช่ใบ capture ของฟิลด์
   3-6) — สรุปเดิมยืนตาม: ไม่ใช่การเปิดใบซ้ำ

### วัดมาแล้ว (แถวจริงจาก `PF_SERIALIZER_FIELDS.tsv:6167-6178`)
| ฟิลด์ | ทิศ | tag/pattern | สถานะ |
|---|---|---|---|
| 1 | W | `0x0B` `STACK@+0x18` len=1 | **resolved** |
| 2 | R | `0x0B` `STACK@+0x18` len=1 | **resolved** |
| 1 | R | `INDIRECT(DEREF(DEREF(DEREF(OBJ+0x14))+0x34))` | UNKNOWN |
| 2 | W | เหมือนแถวบน | UNKNOWN |
| 3 | R+W | `CALL_UNCLASSIFIED:0x00720FC0` | UNKNOWN — ไม่มี precedent |
| 4 | R+W | `InterlockedDecrement(ECX+0x0C)` ผ่าน vtable+0x04 (byte-exact) | UNKNOWN ว่าเป็นฟิลด์จริงหรือ object-lifetime |
| 5 | R+W | `InterlockedIncrement(ECX+0x0C)` (byte-exact) | เหมือนแถวบน (คู่ inc/dec) |
| 6 | R+W | `INDIRECT(DEREF(DEREF(DEREF(OBJ+0x14))+0x34))` | UNKNOWN เหมือนแถว 1-R/2-W |

resolved 2/12 แถว (ทิศเดียวต่อฟิลด์) · 10/12 แถว UNKNOWN

**ตัวเลขความกว้างของ pattern แชร์** (ทดสอบว่าเป็นสัญญาณเฉพาะฟิลด์นี้หรือ noise ทั่วโค้ด — ยกจากจดหมายต้นทาง
`1054`, เดิมตกหล่นตอนยกเนื้อลงมารอบนี้ แก้แล้ว): `INTERLOCKED_INCREMENT` @`ECX+0x0C`: 271 แถว/**86 ข้อความ** ·
`INTERLOCKED_DECREMENT`@เดียวกัน: 279 แถว/**84 ข้อความ** — จากข้อความทั้งหมด 519 ข้อความในตาราง คู่ inc/dec ที่
offset เดียวกันเป๊ะปรากฏใน ~85 ข้อความที่ไม่เกี่ยวกันเลย — สอดคล้องกับ (ไม่ใช่พิสูจน์แล้วว่าเป็น) โค้ด
object-lifecycle ที่ใช้ร่วมกัน ไม่ใช่เนื้อหาเฉพาะของ `UserSetting_UpdateServerSettingVital` — ตัวเลขนี้เป็น
บริบทประกอบเกณฑ์ field 4/5 ด้านล่าง ไม่ใช่ข้อสรุปเดี่ยว

### ขอ RE — แผน differential แบบ wire-only (แก้จากต้นฉบับ ไม่ใช้ breakpoint)
เป้าหมาย: ใช้ **เฉพาะเฟรมขาออกที่จับได้จากเครื่องมือที่มีอยู่แล้ว** (คอนโซล `[G>]`/`GAME_LIVE.txt`/log ต่อ
เซสชันแบบเดียวกับที่ `GT-205`/`GT-211`/`GT-246` ใช้อยู่แล้ว — ไม่ต้องเครื่องมือใหม่) เทียบ byte ที่ตำแหน่ง
field 3/4/5/6 ข้าม trial ที่เปลี่ยนค่าตั้งค่าต่างกัน แทนการแกะภายในไคลเอนต์:

**ขั้นตอนต่อ trial ใช้สคีมาเดียวกับใบ GT คู่กันเป๊ะ** (ไม่ใช่สคีมาแยกของบล็อกนี้ — ห้ามให้สองใบตั้งชื่อ trial
ต่างกันสำหรับข้อมูลชุดเดียวกัน แก้จากร่างแรกของรอบนี้ที่ตั้ง T1-T4 คนละความหมายกับใบ GT): เปิดเมนู Options
(ปุ่มเฟือง) → จดรายการตัวควบคุมทั้งหมดบนจอจริงก่อน (ใบนี้ไม่มีสารบัญ Options จาก static) → **`T0`** = กด Apply
โดยไม่แตะอะไรเลย (baseline/control ตัวแรก) → **`T1..T4`** = เปลี่ยนค่าตั้งค่าทีละ**หนึ่งค่า**ต่อ trial (ไม่คืนค่า
เดิม สะสมไปเรื่อย ๆ) แล้วกด Apply ทุกครั้ง จดค่าเก่า→ใหม่ + เวลา → **`T_mid`** = กด Apply โดยไม่แตะอะไรเลยอีกครั้ง
หลัง trial เปลี่ยนค่าไปแล้วอย่างน้อย 2 ค่า (baseline ตัวที่สอง, แทรกกลาง) → ทำ trial ที่เหลือ (ถ้ามี) →
**`T_final`** = ปิด-เปิด Options ใหม่ยืนยันค่าที่เปลี่ยนยังอยู่ แล้วกด Apply โดยไม่แตะอะไรเลย (baseline ตัวที่สาม)
— เก็บเฟรม `UserSetting_UpdateServerSettingVital` (hex เต็ม + เวลา) ทุกครั้งที่กด Apply ไม่ว่า trial ไหน

**วิเคราะห์** (LANE-UI/RE runner, static comparison ของเฟรมทั้งหมดที่ได้ อย่างน้อย 4 เฟรม — `T0`+trial
เปลี่ยนค่าอย่างน้อยหนึ่ง+`T_mid`+`T_final`): จัดเรียง byte ของแต่ละเฟรมตาม tag ที่ `PF_SERIALIZER_FIELDS.tsv`
ระบุ แล้วแยกการเปรียบเทียบเป็นสองกลุ่ม **ห้ามปนกัน**: (i) คู่ที่ติดกันซึ่งมีการเปลี่ยนค่าคั่นอยู่ (เช่น `T0` vs
`T1`, `T1` vs `T2`) (ii) คู่ baseline-ล้วนที่ไม่มีการแตะอะไรเลยระหว่างกัน (`T0` vs `T_mid`, `T_mid` vs `T_final`,
`T0` vs `T_final`) — กลุ่ม (ii) คือตัวเช็คว่ามีไบต์ที่ขยับเองโดยไม่มีใครแตะอะไร (เช่น per-tick/per-heartbeat
counter) ซึ่งจะทำให้ทุกตำแหน่ง "ดูเหมือนเปลี่ยน" ถ้าเอากลุ่ม (i)/(ii) มาปนกันโดยไม่แยก

**เกณฑ์ปิด/เปิดต่อฟิลด์ (แก้ให้ทิศทางเดียวกับใบ GT คู่กัน — ร่างแรกของบล็อกนี้เขียนสวนทางกับใบ GT ตรงข้อ field
4/5 แก้แล้ว):**
- **field 3** (`0x00720FC0`) และ **field 1-R/2-W/6** (indirect vtable pattern เดียวกัน): ไบต์ตำแหน่งเดียวกัน
  เปลี่ยนเฉพาะในคู่กลุ่ม (i) ที่ตรงกับ trial ที่เปลี่ยนค่าตั้งค่าใดค่าหนึ่งสม่ำเสมอ **และคงที่ในทุกคู่กลุ่ม (ii)**
  ⇒ **ปิดว่าเป็นฟิลด์นั้นจริง** (correlation ไม่ใช่ debugger proof — ดู nonclaims) · ไบต์คงที่ทั้งกลุ่ม (i) และ
  (ii) ⇒ **ปิดว่าไม่ใช่ฟิลด์ settings ที่ทดสอบรอบนี้** (เปิดค้างสำหรับ trial ขนาดใหญ่กว่านี้ถ้าจำเป็น — ดู
  nonclaims ผลลบ)
- **field 4/5** (`ECX+0x0C` interlocked pair): ไบต์ตำแหน่งนี้ **เปลี่ยนแม้ในคู่กลุ่ม (ii) ที่ไม่มีใครแตะอะไร**
  ⇒ **หลักฐานสนับสนุน (ไม่ใช่พิสูจน์เด็ดขาด) ว่าเป็น counter/object-lifetime/refcount noise ไม่ใช่ฟิลด์
  settings จริง** — settings field จริงไม่ควรขยับเองโดยไม่มีการเปลี่ยนค่า (เอกสารวิธีการเดิมของโปรเจกต์ปฏิเสธ
  คำว่า "refcount" อยู่แล้ว ข้อนี้แค่เพิ่มหลักฐานเชิงประจักษ์) · ไบต์ตำแหน่งนี้ **คงที่ทั้งกลุ่ม (i) และ (ii)**
  ⇒ เปิดต่อ ยังไม่มีหลักฐานพอจะตัดสินทางไหน ต้องมี trial เพิ่ม

**เกณฑ์ PASS/FAIL รวมของใบ**: ปิดได้อย่างน้อย 1 ใน 3 กลุ่ม (field 3 / field 4-5 / field 1-R,2-W,6) ด้วยเกณฑ์
ข้างบน = **PASS บางส่วน** (ปิดใบทีละกลุ่มได้ ไม่ต้องครบทั้งสาม) · ไม่มีกลุ่มไหนปิดได้เลย (ทุกไบต์คงที่ตลอดทั้ง
กลุ่ม (i) และ (ii) หรือมี noise แปรผันไม่คงเส้นคงวาแยกกลุ่ม (i)/(ii) ไม่ออก) = **FAIL/INCONCLUSIVE** — บันทึกเป็น
bounded-negative และปิดใบด้วยเหตุผลว่าจำนวน trial ของรอบนี้ไม่พอ ต้องขยาย

### สิ่งที่ใบนี้ **ไม่** ขอ
- ไม่ขอ breakpoint/memory read บนไคลเอนต์ตอนรันจริง (แก้จากต้นฉบับ — เครื่องมือผู้เทสไม่มี)
- ไม่ขอ decode ฟังก์ชัน `0x00720FC0` หรือปลายทาง vtable แบบ static เพิ่ม (คนละชั้นกับใบนี้ ถ้าต้องการ static
  เพิ่มให้เปิดใบ `[STATIC-ON-BRIDGE]` แยกต่างหาก)
- ไม่ขอผลจากจอ/พฤติกรรมเกม (การตั้งค่าใช้งานได้จริงไหม) — ใบนี้จับแค่ไบต์ขาออก
- ไม่ขอให้เสนอโค้ดเซิร์ฟเวอร์ใหม่ — server ไม่เคยตอบเฟรมนี้อยู่แล้ว (ทิศ R ไม่เคยสังเกต) ปิดใบแล้วยังไม่มีงาน
  โค้ดต่อจนกว่าจะมีเหตุผลให้เซิร์ฟเวอร์ต้องอ่านฟิลด์เหล่านี้

### nonclaims
① ไม่ยืนยันว่าฟิลด์ 3 หรือ 6 คือ "known tag-write helper" ที่เคยแก้ที่ไหนมาก่อน — ไม่มี precedent จริงในคลัง
② ไม่ยืนยันว่าฟิลด์ 4/5 เป็นขยะ refcount เป็นข้อเท็จจริงที่ปิดแล้วแม้ trial ข้างบนไม่เปลี่ยนค่าเลย — เป็นแค่
หลักฐานเชิงประจักษ์ที่จำกัดอยู่กับ trial ที่ทดสอบเท่านั้น ไม่ใช่การพิสูจน์ identity ของอ็อบเจกต์
③ ชั้น CAPTURE (197/117) พิสูจน์แค่ว่าเฟรมชนขอบ static เดียวกันสม่ำเสมอ ไม่ได้พิสูจน์ว่าฟิลด์ 3-6 คืออะไร —
ห้ามอ่านว่า "แคปเจอร์ตอบคำถามนี้แล้ว"
④ correlation ระหว่างไบต์ที่เปลี่ยนกับการตั้งค่าที่เปลี่ยน **ไม่ใช่การพิสูจน์เชิง causal** — เกณฑ์ปิดใบข้างบน
เขียนไว้ตรง ๆ ว่าเป็น correlation จาก 4 trial เท่านั้น อาจต้องขยาย trial ถ้าผลกำกวม (เช่นไบต์เปลี่ยนพร้อมกัน
มากกว่าหนึ่งตำแหน่งในทุก trial แยกไม่ออกว่าตัวไหนตรงตัวไหน)
⑤ ไม่ได้เปิดไฟล์ไบนารีหรือดัมพ์ใด ๆ รอบนี้ — เนื้อใบทั้งหมดยกจากจดหมาย
`20260904_1054_LANE-UI-RE-TICKET-options-apply-server-setting-vital-fields-need-dynamic-capture.md` (ค้นก่อน
ถอดของรอบนั้น) บวกการออกแบบ trial ใหม่ของรอบนี้ ไม่มีไบต์ถูกส่งออกไปไคลเอนต์เครื่องไหนเลย
⑥ ไม่ได้ตรวจว่ามีใบ RE ของฟิลด์ 3/4/5/6 ของ vital อื่นที่แชร์ pattern เดียวกัน (เช่น `Pets_UpdatePetsDataVital`)
เปิดค้างอยู่แล้วหรือไม่ — ถ้ามีคนอื่นเปิดแล้ว การจับคู่ trial อาจตอบได้หลายฟิลด์พร้อมกัน บันทึกไว้ให้ chief
พิจารณารวมใบ ไม่ใช่หน้าที่ตัดสินของฉัน
⑦ ตัวเลือก Options ที่แท้จริงบนหน้าจอ (มีกี่ตัว ชื่ออะไร) **ไม่รู้จากที่นี่** — เขียนไว้เป็นสมมติฐานตัวอย่าง
(เสียงเพลง/เอฟเฟกต์/checkbox) ผู้เทสต้องแทนที่ด้วยตัวเลือกจริงที่เห็นบนจอ
⑧ ใบ GT คู่กัน (แผน trial ด้านบนในรูปแบบที่ผู้เทสเดินได้ทันที) ร่างไว้แล้วในจดหมายรอบเดียวกันที่ขอเลขจาก chief
— ตามกติกา `AGENTS.md`/`COO-DECISION 20260904_2142` ข้อ 3 (ผล RE ที่ขอ attended capture ต้องเปิดใบ GT รอบ
เดียวกัน) ยังไม่มีเลข GT ณ ตอนที่เขียนบล็อกนี้
⑨ **ไม่ตัดปัญหา "ตัวนับจำนวนค่าตั้งค่าที่ถูกแตะในเซสชันนี้" (dirty-settings counter) ออกจากผลลัพธ์ (A)** — ถ้า
ไบต์ตำแหน่งหนึ่งขยับทุกครั้งที่มี trial เปลี่ยนค่าใหม่ (ไม่ว่าจะเป็น setting ตัวไหน) แผนนี้แยกไม่ออกจาก field
settings ที่ผูกกับ**ค่า**จริงเพียงจาก 4 trial เพราะไม่มี trial ไหนแตะค่าที่เคยเปลี่ยนไปแล้วซ้ำเพื่อดูว่าไบต์ขยับ
ตามอีกหรือไม่ (field settings จริงควรขยับซ้ำถ้าค่าถูกเปลี่ยนซ้ำ ตัวนับ dirty-count จะไม่ขยับถ้า setting เดิมถูก
แตะซ้ำ) — บันทึกเป็นคำถามเปิดสำหรับรอบเทสถัดไปถ้าผลลัพธ์ (A) ต้องการยืนยันเพิ่ม ไม่ใช่ตัวบล็อกใบนี้
⑩ **ไม่มีภาพนิ่งเต็มแผงหลัง trial แต่ละครั้ง** (มีแค่ `S01`/`S02`/`S03`) — trial สะสมไม่ revert ค่า ⇒ ถ้าผู้เทส
เผลอแตะตัวควบคุมอื่นพร้อมกับตัวที่ตั้งใจในสเต็ปเดียว การปนเปื้อนนี้จะไม่ถูกจับจนกว่าจะถึง `S02`/`S03` และตอนนั้น
จะสืบย้อนกลับไม่ได้ว่าปนที่ trial ไหน — ผู้เทสต้องมองแผงให้แน่ใจว่าไม่มีตัวควบคุมอื่นขยับก่อนกด Apply ทุกครั้ง
(ไม่มีเครื่องมืออัตโนมัติป้องกันข้อนี้ในแผนปัจจุบัน)
⑪ `BRIDGE_BOOT_PROCEDURE.md:60` (บรรทัดถัดจากที่ใบนี้อ้างเรื่องพอร์ต 10188/10189) ยังเขียนเพดาน boot stamp
"180 นาที" ค้างอยู่ ทั้งที่ตัวบังคับจริงคือ `staged/TEMPLATE_teardown_generic.ps1:135` (`420`, ยกขึ้นจาก 180
ตั้งแต่ 2026-08-20 ตามคอมเมนต์ในไฟล์นั้นเอง) — ไม่ใช่ของรอบนี้และไม่ใช่ไฟล์ในเขตเขียนของ LANE-UI แจ้ง chief ใน
จดหมายรอบเดียวกันเป็น FYI เท่านั้น ไม่ได้แก้เอง

---

## 🔬 RE-238 SELECTOR-CATEGORY-TO-ALT-HP-PAIR-MAPPING-001  [OPEN -- ร่างโดย LANE-GM รอบ `zq18m1` (ใบ `notes_to_chief/20260904_1154_LANE-GM-RE-0x430E10-TICKET-selector-category-to-alt-hp-pair-mapping.md`) ตาม `COO-DECISION 20260904_1046` ข้อ 2 · **วางคิวและมอบหมายโดย chief รอบ `wjqykr` (R338) 2026-09-04T14:09+07:00** · ผู้ทำ: **สาย RE** (RE runner local, ไม่ต้องจอง) · **LANE-GM บริโภคผลเอง** · 🔴 `[STATIC-ON-BRIDGE]` ต้องดิสแอสเซมบลีอิมเมจ ⇒ ทำบนคลาวด์ไม่ได้]

> 🔴 **เลขใบเปลี่ยนจากชื่อร่างชั่วคราว `RE-0x430E10` เป็น `RE-238`** — ชื่อร่างไม่ใช่เลขใบและตัวนับใบค้นไม่เจอ
> (chief ยืนยัน `notes_to_chief/20260904_1409_CHIEF-TO-LANE-GM-your-0x430E10-ticket-is-re238-paste-the-body.md`) ·
> ตัวนับร่วมสองคิวคืน `237` ⇒ ใบนี้ `238` · `RE-238`/`GT-238` = **0 hit ทั้งสามที่ก่อนวาง** ·
> **LANE-GM ยกเนื้อใบลงเองรอบนี้** ทุกจุดที่เคยเขียน `RE-0x430E10` ในใบต้นทางแทนด้วย `RE-238` ข้างล่างนี้ ·
> โค้ด/เทสของสายนี้เองไม่เคยอ้าง**ชื่อใบ** `RE-0x430E10` เลย (ตรวจแล้ว `grep -rn "RE-0x430E10\|RE_0x430E10" pirate-force-server/src pirate-force-server/tests` = 0 hit) ⇒ ไม่มีจุดต้องแก้นอกไฟล์นี้ —
> 🔴 **ต่างจากที่อยู่นอกเรื่อง**: `attr_wire.py` มี `0x430E10` (VA ของฟังก์ชันไคลเอนต์ ไม่ใช่ชื่อใบ) อยู่หลายสิบจุด
> โดยตั้งใจ (คอมเมนต์อธิบายกลไก selector) — จุดเหล่านั้น**ไม่ใช่**การอ้างถึงใบนี้และไม่ต้องแก้เป็น `RE-238`

- อิมเมจที่ต้องยึด: `GameClient/GameClient.local.bin` 14,759,424 ไบต์
  sha256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`
  (ค่าเดียวกับที่ `PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md` ปักไว้ — ตรวจ sha ก่อนอ่าน)

### ทำไมใบนี้ถึงมีอยู่
`FIELDS` row x=9 (`category_5C`, +0x5C ของ BasicAttr) ค่าที่ส่งเข้าฟังก์ชัน `0x430E10` แล้วผลลัพธ์
เทียบกับ `8` เพื่อเลือกว่า HP ของไคลเอนต์อ่านจาก `+0x44/+0x48` (ปกติ) หรือสลับไปอ่าน
`ActorAttr +0x1A8/+0x1AC` (x=52/x=53) แทน `[PROVEN VA=0x5BD3C0..0x5BD3DB]` (call site เดียวกับ
`0x4564B3` ที่เขียน cached byte `actor+0x358`) นี่คือกลไกเดียวที่ `GT-218` วัดว่าฆ่าไคลเอนต์ได้
(HP `0/1` เมื่อ mask ไม่ครบ) รั้วสองชั้นที่เซิร์ฟเวอร์มีวันนี้ (`gm/attr_wire.make_update_attr_frame`,
`_refuse_selector_change`) **ไม่มีตัวไหนอ่าน `0x430E10` เอง** — ตัวหนึ่งเทียบ "ค่าที่จะส่ง == ค่าที่
login ส่งมา" (การเปลี่ยนแปลง ไม่ใช่เงื่อนไข) อีกตัวเทียบ "x9 == 8" ตรง ๆ (ค่านำเข้า ไม่ใช่ผลลัพธ์ของ
ฟังก์ชัน) ทั้งสองมีผลข้างเคียงที่ระบุไว้แล้ว (false positive ที่ฉาก 8 "Silver Harbour", false negative
กับทุกฉากอื่นที่ผลลัพธ์ `0x430E10` เป็น 8 พอดี) เพราะเซิร์ฟเวอร์ไม่มีทางประเมินเงื่อนไขจริง

### คำถามเดียว (ตอบได้แค่บางส่วนก็ปิดบางส่วนได้ ไม่ต้องครบ)

**Q — `0x430E10` แมพค่า `category_5C` (u16) ตัวไหนเป็น 8**
ขอ **decode ฟังก์ชัน `0x430E10` เต็มตัว** (ไบต์ + คำสั่งที่ถอดได้ + span sha256) แล้วตอบ:
- เป็นการเทียบ/lookup โดยตรง (เช่น `switch`/jump table หรือ `if (cat==N) return 8`) หรือเป็น
  การคำนวณ (เช่น bitmask/หาร/ดัชนีเข้าตาราง static)
- ถ้าเป็น lookup โดยตรง: **ชุดค่า `category_5C` ทั้งหมดที่คืนผล 8** (รายการ ไม่ใช่ตัวอย่าง)
- ถ้าฟังก์ชันอ่านตาราง static เพิ่มเติม (ไม่ใช่ input เดียว) ขอ VA + span ของตารางนั้นด้วย
- `category_5C` เป็นรหัสอะไร (scene id / scene category / actor type / อื่น) **ถ้าบอกได้จากโค้ด
  เอง** — ห้ามอนุมานจากชื่อคอลัมน์เดิม (`SELECTOR_NOTE_R301` ในรีโป server ตีกลับชื่อ "scene_id"
  ไปแล้วครั้งหนึ่งเพราะไม่มีหลักฐานในอิมเมจ)

### เกณฑ์ปิดใบ (ชั้นเดียว — static IMAGE เท่านั้น ไม่มีชั้น client-observable และไม่ต้องมี)
- ยกไบต์ + คำสั่งที่ถอดได้ของ `0x430E10` เต็มฟังก์ชัน พร้อม `span_sha256` เทียบกับอิมเมจข้างบน
- ตอบชนิดของฟังก์ชัน (lookup ตรง/คำนวณ) ด้วยคำสั่งที่ยกมา ไม่ใช่ด้วยการเดา
- ถ้าตอบได้: รายการค่า `category_5C` ที่คืนผล 8 ครบทุกตัว (ไม่ใช่ตัวอย่างเดียว)

### ราคาที่ประหยัดได้ถ้าไม่ทำ / ถ้าคำตอบเป็น "ตารางใหญ่เกินไม่คุ้ม"
วันนี้เซิร์ฟเวอร์ปฏิเสธ (stand-down มีบรรทัดคอนโซล) ทุกครั้งที่ x=9 กำลังจะเปลี่ยนค่า — ราคาคือ
ผู้เล่นต้องรีล็อกอินก่อนตี (`COO 1046` ข้อ 3 สั่งใส่ในขั้นตอน `GT-224` แทนการแก้โค้ด) ถ้าใบนี้ตอบ
"ชุดค่าที่คืน 8" ได้ครบ เซิร์ฟเวอร์จะเขียนรั้วจริงแทนรั้ว "ค่าเดียวกับ login เท่านั้น" ได้ — ปลด
ข้อจำกัดรีล็อกอินสำหรับผู้เล่นที่เปลี่ยนฉากแล้วยังอยู่ในหมวดหมู่ HP-ปกติเดิม ถ้าคำตอบคือ "คำนวณ
ซับซ้อนเกิน static" ก็ปิดใบด้วยคำตอบนั้นได้ — รั้วปัจจุบันยืนต่อตามที่ `COO 1046` ข้อ 1 ยืนยันแล้ว

### สิ่งที่ใบนี้ **ไม่** ขอ
- ไม่ขอ decode `0x5BD3C0..0x5BD3DB` (call site) ซ้ำ — decode แล้วใน `PF_CHUNK2_Q1` (`[PROVEN]`)
- ไม่ขอชื่อ "ที่ถูกต้อง" ให้ x=9 — ชื่อ `category_5C` ยืนตาม `SELECTOR_NOTE_R301` (no renames)
- ไม่ขอผลจากจอ/capture — ใบนี้ static ล้วน คนละชั้นกับ `RE-222` (attended, เครื่อง Panya)
- ไม่ขอให้เสนอรั้วเซิร์ฟเวอร์ใหม่ — เขียนโค้ดเป็นงานของ LANE-GM รอบถัดไปเมื่อมีผล ไม่ใช่ของใบนี้

- ค้นแล้วก่อนเปิด (LANE-GM กรอกเอง): `external/00_SEARCH_HERE_FIRST.md`, `gamedata/00_SEARCH_HERE_FIRST.md`
  **เจอไฟล์ ไม่เจอคำตอบ** (`430E10` ไม่ปรากฏในทั้งสองไฟล์) · `external/*.tsv`
  (`PF_PROTOCOL_REGISTRY.tsv`, `PF_SERIALIZER_FIELDS.tsv` ฯลฯ) **ไม่เจอ** ·
  `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` **ไม่เจอ** ·
  `pirate-force-server/reports/PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md` **เจอ** ผู้เรียก
  สองจุด + สแปนอิมเมจ แต่ตัวฟังก์ชัน `0x430E10` เอง **ไม่เคยถูก decode** — รายการ "เรียกแต่ไม่ decode"
  ข้อ 12 ของรายงานเดียวกันระบุ `0x430E10` ไว้ตรง ๆ
- links: `COO-DECISION 20260904_1046` (สั่งเปิดใบนี้) ·
  `COO-DECISION 20260904_0846` (รั้ว selector เดิม) ·
  `notes_to_chief/20260904_1409_CHIEF-TO-LANE-GM-your-0x430E10-ticket-is-re238-paste-the-body.md` (ตั้งเลข `RE-238`) ·
  `pirate-force-server/reports/PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md`
  (§7.2, ข้อ 12, บรรทัด 143/150-151/200-201/433) ·
  `pirate-force-server/reports/PF_HP_DEATH001_HP_DEATH_AND_RESPAWN_STATIC_20260819.md` ·
  `pirate-force-server/src/pirateforce_foundation/gm/attr_wire.py` (`SELECTOR_NOTE_R301`,
  `make_update_attr_frame`, `_refuse_selector_change`)
- numbering: ตัวนับร่วม (กฎ ②) คืน `237` ⇒ ใบนี้ `238` · `RE-238`/`GT-238` = 0 hit ทั้งสามที่ก่อนวาง
- result: (สาย RE กรอก: ชนิดฟังก์ชัน + คำสั่งที่ถอด + span sha256 + รายการค่าที่คืน 8 ถ้ามี +
  timestamp)

---

## 🔬 RE-239 SECOND-PASSWORD-INCOMING-CREDENTIAL-FRAME-001  [🟡 PENDING (RESERVED - เนื้อใบยังไม่ถูกเขียน ห้ามลงรอบเทส) -- 🔴 route ให้ **LANE-DB** ติดป้ายตาม §18 ตอนวางเนื้อใบ (`STATIC-ON-BRIDGE` หรือ `NEEDS-ATTENDED-CAPTURE`) · เจ้าของใบ/ผู้บริโภคผล = **LANE-DB**]

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `wjqykr`/R338** · ที่มา `notes_to_chief/20260904_1309_LANE-DB-RE-TICKET-second-password-incoming-credential-frame.md` ตาม `COO-DECISION 20260904_1150` ข้อ 2 · ตัวนับร่วมสองคิวคืน `238` ⇒ ใบนี้ `239` · **0 hit ทั้งสามที่ก่อนวาง**
> 🔴 บล็อกนี้คือการจองเลข เนื้อใบเป็นของ **LANE-DB** · `COO 20260904_1347` รับไว้แล้วว่าชิ้น 4 ปิดยกเว้นเฟรมขาเข้าใบนี้ และ **ไม่มีกำหนดวัน** — ใบนี้จึงไม่บล็อกคิว DB

---

## 🔬 RE-240 HOTBAR-SKILL-KEY-TO-PRODUCER-WALK-001  [~~OPEN -- 🔴 `[STATIC-ON-BRIDGE]` · ผู้เปิดใบ = **chief (LANE-E)** รอบ `wjqykr`/R338 · ผู้ทำ = **สา... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## คำถาม (เดินทางเดียว มี control ในตัว)
ตาราง byte ที่ `0x4519C4` แปลง HOTKEY class → branch ของ dispatcher `0x450B20-0x450B38` · **แถวของช่องสกิล/ฮอตบาร์เดินไปถึง producer ตัวไหน**
- ไปถึง `0x44D260` / serializer `0x0074E6A0` (= `ActionVital`) หรือ
- ไปถึง serializer `0x00600A60` (= `TriggerCastSkillVital 0x5CD2`, handler `0x00601810`)
และ **เลขสกิลที่ผู้เล่นกดไปลงที่ไบต์ไหนของเฟรมนั้น** (offset + tag + width)

## control ที่ต้องทำในรอบเดียวกัน (ห้ามข้าม)
เดินแถว **WIELD** ซ้ำให้ได้ผลเดิม: HOTKEY 71 → class 11 → branch `0x451026` → producer `0x44BC70` ที่ **hardcode `0xEA7E`** ลง `+0x30`
(ที่มา `pirate-force-server/reports/PF_RE_V128_Wield_Z_ActionVital_Capture_20260814.md:25-33` = ห่วงโซ่ปุ่ม→producer · **:47-60 โดยเฉพาะบรรทัด 55** = จุดที่บอกว่าค่านั้นลงที่ `+0x30` — ต้องเปิดทั้งสองช่วง ไม่งั้นยืนยัน control ไม่ได้) — เดินแถวนี้ไม่ตรง = ผลของทั้งใบใช้ไม่ได้

## เกณฑ์ปิดใบ
- **บวก**: ระบุ producer + offset/tag/width ที่พกเลขสกิล พร้อม VA ทุกตัวที่เดินผ่าน และ control WIELD ตรง
- **bounded-negative**: เดินครบแล้วชนเพดาน (เช่น ตารางถูกสร้าง runtime) ⇒ ระบุเพดานให้ชัดว่าตันตรงไหน แล้วส่งต่อเป็นใบ attended capture (กด skill 99 จากฮอตบาร์ + control กด Z ในเซสชันเดียวกัน ต้องได้ hex ตระกูล V128 เดิม)

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- 🔴 **ห้ามใช้เลขตรงกันเป็นข้อผูก (G6)**: `CONSTDATA_TH__BEHAVIOR.tsv` มี `n_ID = 99` และ `CONSTDATA_TH__SKILL_CONTEXT.tsv` ก็มี `n_ID = 99` — สอง id space ชนกันที่เลขนี้พอดี
- ห้าม**เริ่มต้น**ด้วยสมมติฐานว่า `TriggerCastSkillVital` เป็นเฟรมของการร่ายสกิล — ความพยายามหา producer ก่อนหน้านี้จบลงที่ `RE-056` (`METHOD-FAIL`) และ `GT-050` job 4 (`TRIGGER-DIRECTION-UNRESOLVED`)
  🔴 **แต่ "UNRESOLVED" คือคำสั่งเรื่องวิธีที่ใช้แล้วไม่เจอ ไม่ใช่ข้อพิสูจน์เรื่องสายไฟ** — ถ้าการเดินตาราง `0x4519C4` รอบนี้ไปโผล่ที่ serializer `0x00600A60` จริง **นั่นคือผลบวก ให้รายงานเป็นผลบวก** ห้ามให้บรรทัดนี้บังคับให้เขียนว่า inconclusive
  ข้อเท็จจริงที่ต้องถือไว้ด้วยกัน: `external/PF_SERIALIZER_FIELDS.tsv:1501-1506` ให้ `TriggerCastSkillVital` มีฟิลด์ทิศ W จริงสามตัว (`0x0F@+0x14/2` · `0x08@+0x16/1` · `0x14@+0x18/4` · `ALWAYS`) ไม่มี `EMPTY` สักแถว
- `PF_FIELD_VALIDATION.tsv:198-199` เขียนว่า `TriggerCastSkillVital` = `NOT_OBSERVED` (0 เฟรมใน 26 ไฟล์ capture) — นั่นคือคำสั่งเรื่อง corpus ที่ไม่มีใครร่ายสกิล ไม่ใช่ข้อพิสูจน์ว่าไคลเอนต์ไม่เคยส่ง

## แยกจากใบไหน
- `RE-232` (ปิดแล้ว) ถาม grammar ของ `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` — คนละคำถาม
- `RE-110` (ปิดแล้ว) ตอบว่า `+0x30` คือ **ตัวเลือกท่า/behavior** (`EQUIP_VALUE.n_EQUIPTYPE → n_ATTACK_SKILL → BEHAVIOR.n_ID`, ค่า 280/282/284/286/288/290) — ใบนี้ต่อจากตรงนั้น ไม่ใช่ถามซ้ำ

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-CS** (cc chief) · LANE-CS บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง

---

## 🔬 RE-241 MONSTER-ACTOR-ENTRY-IS-CNETNPC-AND-MODEL-READY-BIT-ORDER-001  [🟢 **CLOSED PASS/DONE** -- ผลมาถึง `notes_to_chief/20260904_1948_RE-241-RESULT-TYPE4-CNETNPC-MODEL-READY-PRECEDES-COLOR.md` (R... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## ค้นก่อนถอด (ผู้ทำต้องกรอกในผล ห้ามเว้น)
- `ค้นใน pf_bridge\external\ แล้ว: เจอ <อะไร> / ไม่เจอ`
- `ค้น gamedata แล้ว: เจอ <อะไร> / ไม่เจอ`
- สิ่งที่ GM ค้นไปแล้วก่อนร่าง (ห้ามค้นซ้ำ ให้ verify sha แล้วใช้ต่อ): `RE-222` (typed_CNetNPC `0x0044421C -> 0x00469700` = object-type downcast อิสระจาก identity) · `RE-202` (`MCG-IMG-002` factory `[0x004469C8,0x00446A53)` อ่าน `actor_entry+0x10` u8 == **4** → สาขาสร้าง `CNetNPC` · `MCG-IMG-046` = `CNetNPC+0x70 bit 0x40` = บิต "โมเดลพร้อม" ตั้งฝั่งไคลเอนต์ ไม่มีฟิลด์ไวร์) · `RE-195` (ตาราง style 56/58/59/60/61 ครบ ไม่มีแถวชื่อ "ชมพู")

## คำถาม (สองข้อ เดินทางเดียว)
**Q1 — ไบต์ไวร์จริงของ `actor_type` ที่ `hostile_actor_entry` ส่ง ตรงตำแหน่งกับ `MCG-IMG-002`/`MCG-IMG-004` หรือไม่**
`src/pirateforce_foundation/field_mobs.py` เรียก `legacy.make_remote_actor_entry(NPC_STYLE_ACTOR_TYPE, ...)` และ `NPC_STYLE_ACTOR_TYPE = 4` (`population.py:23`) — **ค่าเดียวกับ NPC ในเมือง** · ต้องยกไบต์จริงที่ `make_remote_actor_entry` ใน `current/pf_login_game_server_v141.py` ประกอบออกมา เทียบกับสแปนที่ `MCG-IMG-004` ปักไว้ (`GSCN_RunTimeProtocolRes.actor_entry` · wire_order=2 · tag=0x32 · len=8 · offset record+0x18..0x1F) และเงื่อนไข `actor_entry+0x10 == 4` ของ `MCG-IMG-002`
🔴 **ชื่อค่าคงที่ตรงกัน (`= 4`) ไม่ใช่หลักฐานว่าไบต์ไปลงตำแหน่งเดียวกัน** — นี่คือช่องว่างทั้งหมดของใบนี้

**Q2 — บิต "โมเดลพร้อม" (`CNetNPC+0x70 & 0x40`) เป็นเงื่อนไขก่อนหน้าตัวเลือกสีหรือไม่**
`RE-202` พิสูจน์แล้วว่าบิตนี้กั้นไอคอนเควสต์ (client-local) · ยังไม่เคยตรวจว่าตัวเลือกสี `0x00443F50` (หรือ actor updater `0x00444400` ที่ `MCMJ-IMG` ชี้ว่าเป็นจุดอ่านจริง) ถูกเรียก **หลัง** บิตนี้ตั้งเท่านั้น หรือไม่ขึ้นกับมันเลย
ขอ: เส้นทางเรียกจาก actor updater `0x00444400` (หรือจุดที่เรียก `0x00443F50` จริง) เทียบกับจุดตั้งบิต `0x004448B4` (`or [edi+0x70],0x40` ที่ `RE-202` ปักแล้ว) — **ใครมาก่อนในลำดับการเรียกจากจุดกำเนิด actor เดียวกัน**

## เกณฑ์ปิดใบ (ชั้นเดียว — static IMAGE เท่านั้น ไม่มีชั้น client-observable)
- Q1: ไบต์ + offset จริงของ `actor_type` parameter เทียบ `span_sha256` กับ `MCG-IMG-002`/`MCG-IMG-004` (อ้าง VA/offset/sha256 ทั้งสองฝั่ง)
- Q2: รายชื่อ caller/callee ตามลำดับจริงระหว่างจุดตั้งบิต `+0x70` กับจุดเรียกตัวเลือกสี พร้อม VA + `span_sha256` ทุกช่วง
- **bounded-negative รับได้**: เดินครบแล้วชนเพดาน ⇒ ระบุเพดานให้ชัดว่าตันตรงไหน แล้วบอกว่าต้องเป็นใบ attended capture หรือใบ static ใบถัดไป `[chief เติม]`

## ใบนี้ไม่ขอ
เลข FontStyleID ใด ๆ · การเปลี่ยน identity เป็นลบ (`RE-211`/`RE-222` คุมอยู่แล้ว) · ผลจากจอ · ข้อสรุปว่า "ชมพู" คือของบิตนี้แน่

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- 🔴 ห้ามอ้างว่า `NPC_STYLE_ACTOR_TYPE = 4` พิสูจน์แล้วว่ามอนเป็น `CNetNPC` จริงบนจอ — Q1 คือสิ่งที่ปิดช่องว่างนี้ ไม่ใช่สิ่งที่ยืนยันมันล่วงหน้า
- 🔴 ห้ามอ้างว่า "ชมพู" มาจากบิต `+0x70` — ใบนี้ถามลำดับการเรียก ไม่ได้เดาคำตอบ
- 🔴 `[chief เติม]` **G6**: ทั้ง Q1 และ Q2 ห้ามปิดด้วยการอ่านครั้งเดียว — ทุกช่วงที่ยกมาต้องมี `span_sha256` และต้องยกจาก generation ปัจจุบัน (`reference_codex_attr/README_WHAT_THIS_IS.md` → `generation_id`) ระบุ `generation_id` ลงในผล
- 🔴 `[chief เติม]` **PER-CLASS (§14 ข้อ 13 ค)**: ผลที่ได้จากสาขา `actor_type == 4` ห้ามเหมาไปใช้กับ actor_type อื่น แม้ตัวเลขจะเดินผ่านโค้ดเดียวกัน
- 🔴 `[chief เติม]` แถวของ Codex ที่ยกมาต้องอ่านคอลัมน์ `nonclaim` ก่อนใช้ และคัดลอกข้อความ nonclaim ของแถวนั้นลงในผล (§14 ข้อ 13 ข)

## แยกจากใบไหน
- `RE-222` (ปิดแล้ว) ตอบ "อะไรคือ typed_CNetNPC" — ใบนี้ถามว่า "ไบต์ของเราไปถึงมันจริงไหม" คนละคำถาม
- `RE-202` (ปิดแล้ว) ตอบว่าบิต `+0x70` กั้นไอคอนเควสต์ — ใบนี้ถามว่ามันกั้นสีด้วยหรือไม่
- `RE-195` (ปิดแล้ว) ให้ตารางสี — ใบนี้ไม่ถามเลขสีสักตัว

## ถ้าผลออกทางลบ
Q1 ตอบว่าไบต์ **ไม่ตรง** (มอนไม่ได้เป็น `CNetNPC` จริง) ⇒ คำถามเดิมของ `COO 0217` ("ส่งมอนทาง CNetNPC แทน `field_mobs` ได้ไหม") กลับมามีความหมาย และเป็น **ใบถัดไป** ไม่ใช่ใบนี้ `[chief เติม]` ใบถัดไปนั้น LANE-GM เป็นผู้ร่าง chief ตั้งเลข

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-GM** (cc chief) · บรรทัดแรกของจดหมายผลเขียนว่า `ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย` · LANE-GM บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง (§5 "ใครเปิดใบคนนั้นบริโภค" — ใบนี้ chief ตั้งเลขให้ แต่เจ้าของเนื้อคือ GM)

---

## 🔬 RE-248 SELECTACTOR-0x5DFF60-TWO-U16-TAG-0x12-WHICH-IS-SCENE-001  [🟠 **OPEN** -- 🔴 `[STATIC-ON-BRIDGE]` (ต้องเปิด client image = เครื่อง Panya) · เลขใบตั้งโดย chief (LANE-E) รอบ `epkucn`/R344 ตาม `LANE-DB-ASK-CHIEF 20260904_2212` + `COO-DECISION 20260904_2152` ข้อ 3 (อนุมัติ RE ใบแคบ **ยกเว้นข้อห้าม "ห้ามเปิด RE ก่อน" ของ `1947` ใบนี้ใบเดียว**) · ผู้ทำ = **ka1-A / RE runner (local)** · **ผู้บริโภคผล = LANE-DB** · ใบ GT คู่ของมันมีเลขแล้ว = `GT-245` (`COO 20260904_1948` ข้อ 3) จึงครบกติกา RE->GT ของ `2142` ข้อ 3]

> 🔢 ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `247` (`GT-247`, วางรอบเดียวกัน) => ใบนี้ `248` · `RE-248`/`GT-248` = 0 hit ทั้งสามที่ก่อนวาง

## คำถามเดียว (ถ้อยคำตาม `COO 2152` ข้อ 3)
> serializer `0x5DFF60` (`SelectActorVital`/`CreateActorVital` -- ชื่อเดียวกันตามคอมเมนต์ `get_preset_actor_wire()` ใน `current/pf_login_game_server_v141.py`) เขียน `u16 tag 0x12` **สองตัวนี้** จากตัวแปรชื่ออะไร และหน้าเลือกตัวละครอ่าน**ตัวไหน**ไปพิมพ์ชื่อฉาก

## ค้นก่อนถอด (ผู้ทำต้องกรอกในผล ห้ามเว้น)
- `external/00_SEARCH_HERE_FIRST.md` -> grep `SelectActorVital` / `0x5DFF60` ใน `external/PF_SERIALIZER_FIELDS.tsv` **ทำแล้วโดย LANE-DB (`2212` §0.5)**: เจอสองแถวตรงโครงสร้าง -- `order 17` tag `0x12` `field_offset DEREF(DEREF(STACK@0x005EBAE0+0x18)+0x10)+0x20` len 2 · `order 18` เหมือนกันที่ `+0x22` · span `[0x005DFF60,0x005E01C6)` · sha256 `de9de2a04f4ac3ec8e6c07550336eea2be18954143c5c0de1823a4a2171e3f8a` · **ตารางนี้ไม่บอกชื่อตัวแปร/ความหมาย** (`formal_reaching_def` มีแค่ `self`/`edi` ไม่ใช่ payload) => คำถามยังเปิดจริง
- `notes_to_chief/reference_codex_attr/` (README ก่อนเสมอ) -- แถวใดแตะ `+0x20`/`+0x22` ของ actor wire ให้ยกมาพร้อมคอลัมน์ `nonclaim`
- capture: `archive/stray_captures_20260819/` มีไฟล์เดียวที่มี `CreateActorVital` และค่าทั้งคู่เท่ากัน => **ไขว้ไม่ได้จาก capture ที่มี** (LANE-DB ตรวจแล้ว)

## เกณฑ์ปิดใบ (ชั้นเดียว -- static IMAGE เท่านั้น ไม่มีชั้น client-observable)
- ปิด **PASS** ได้เมื่อ: ชี้ได้ว่า `+0x20` หรือ `+0x22` ตัวใดถูก **อ่าน** โดยเส้นทางที่พิมพ์ชื่อฉากในหน้าเลือกตัวละคร พร้อม VA ของจุดอ่าน + ชื่อ/ที่มาของตัวแปรต้นทางที่จุดเขียน + `image_sha256`
- ปิด **BOUNDED-NEGATIVE** ได้เมื่อ: เดินสายอ่านครบแล้วยังแยกไม่ออก -- ต้องระบุว่าเส้นทางตันที่ VA ใด และอะไรจะปลดล็อกได้ (capture ชนิดไหน)

## ใบนี้ไม่ขอ
ไม่ขอความหมายของฟิลด์อื่นในโครงสร้างเดียวกัน · ไม่ขอ `astr`/`wstr` · ไม่ขอค่าที่ถูกต้องของ scene id ใด ๆ · ไม่ขอให้แตะโค้ด

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- 🔴 ห้ามสรุปจากตัวอย่างเดียวที่มี (`get_preset_actor_wire()` สร้างที่ Port Royal เสมอ ค่าทั้งคู่ = `1`) -- G1/G6
- 🔴 ห้ามอ้าง `external/PF_SERIALIZER_FIELDS.tsv` ว่าตอบใบนี้แล้ว (มันยืนยันตำแหน่ง ไม่ใช่ความหมาย -- คำเตือนของตารางเอง)
- 🔴 ผลของ Codex เป็นหลักฐานชั้น IMAGE ห้ามยกเป็น client-observable (§14 ข้อ 13 ก/ข)

## แยกจากใบไหน
`RE-119` (ปิดแล้ว) ให้โครงสร้าง actor wire -- ใบนี้ถามเฉพาะว่าฟิลด์ไหนในสองตัวคือ scene · `GT-245` คือใบ attended ที่รอผลนี้ (หน้าเลือกตัวแสดงฉากจริง)

## ถ้าผลออกทางลบ
`SCENE_FIELD` ใน `src/pirateforce_foundation/persistence_scene_field_patch.py` **คงค่า `None` ต่อไป** (ไบต์ออกเท่าเดิมทุกไบต์) และ `GT-245` ยัง BLOCKED -- ห้ามใครเดาฟิลด์เพื่อปลดใบ

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-DB** (cc chief, COO) · LANE-DB บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง (§5 "ใครเปิดใบคนนั้นบริโภค" -- chief ตั้งเลขให้ แต่เจ้าของเนื้อคือ DB) · แก้ `SCENE_FIELD` เป็น `FIELD_A`/`FIELD_B` บรรทัดเดียว

---

## 🔬 RE-256 ADDSURVEYDATA-OUTER-PRESENCE-BYTE-VALUE-001  [✅ **DONE -- ตอบแล้ว 2026-09-05 10:07 +07:00** · ปิดหัวโดย chief (LANE-E) รอบ `pv4zg1`/R352 ตามใบผล `notes_to_chief/20260905_1007_RE-256-RESULT-PRESENCE-ONE-SINGLE-RECORD-VERSION-ZERO.md` · คำตอบ: outer byte tag `0x0B` = **pointer-presence boolean** (`cmp dword ptr [esi+0x14],0` / `setne al` ที่ `0x00733586-0x0073358E`) ⇒ หนึ่ง record = `0B 01` · ไม่มี record = `0B 00` · **ไม่ใช่ record count** · `vital_version` ของคลาสนี้ต้องเป็น `0` แบบ exact equality (`0x005F3EFC/0x005F3F01`) · BUILD_IMPACT ลงโค้ดแล้วโดย LANE-A รอบ `vwekfq` = server `#810` (`c3454949`) บน main `b49a4e45` [วัดแล้ว `--is-ancestor` exit 0 · chief `pv4zg1`] · ผู้บริโภคผล = LANE-A (บริโภคแล้ว) ⇒ `GT-233` ปลดหัวเป็น READY ในรอบเดียวกัน · เดิม: 🟠 **OPEN** -- 🔴 `[STATIC-ON-BRIDGE]` (ต้องเปิด client image = RE runner บนเครื่อง Panya · LANE-A บนคลาวด์ไม่มีไบนารี `LANE-A 0435` · `COO-DECISION 20260905_0645` รับทาง 2) · เลขใบตั้งโดย chief (LANE-E) รอบ `rs8uyz`/R350 ตาม `LANE-A-RE-TICKET 20260905_0430` (ฉบับแก้ทับ 05:15 หลัง pf-adversary) + `COO-DECISION 20260905_0645`/`0646` · ผู้ทำ = **RE runner (local)** สายเดียว · **เจ้าของใบ/ผู้บริโภคผล = LANE-A** · ตัวบล็อกของ `GT-233` (BLOCKED-ON-LAYOUT) และของบันได **M2**]

> 🔢 ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `255` (`GT-255`) => ใบนี้ `256` · `RE-256`/`GT-256` = 0 hit ทั้งสามที่ก่อนวาง

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกาใหม่ `AGENTS.md` §7 · `COO 0646` ข้อ 2)
- `external/PF_SERIALIZER_FIELDS.tsv:6377-6388` -- **เจอ** สแปน+SHA ตรงกับที่ `RE-227` อ้าง (`[0x00733570,0x00733614)` · `f8c7510018...af178c`) ให้ **tag/ยาว/gate** ของ presence byte `0x0B` (1 ไบต์ · ALWAYS) แต่ **ไม่ให้ค่า**
- `archive/notes_to_chief_2026-08/20260827_0115_RE-086-RESULT-*` -- **เจอ** ร้อยแก้วตรงกัน: outer serializer ส่ง presence byte แล้วเรียก nested vtable slot `+0x10` (63 คำสั่ง · gap/error 0/0)
- ⇒ **สิ่งที่ค้นเจอถูกตัดออกจากใบนี้แล้ว** ฉบับ 04:30 ถามข้อที่ commit อยู่แล้ว สาย A แก้ทับเอง เหลือเฉพาะข้อที่ยังไม่มีใครวัด

## คำถาม (สี่ข้อ ทั้งหมดตอบด้วย static)
1. **ค่า** ของ presence byte ชั้นนอกเมื่อ collection มี record หนึ่งตัว -- `1` · จำนวน record · หรืออย่างอื่น (ห้ามเดา)
2. ลำดับ **อ่าน** ต่างจากลำดับ **เขียน** ไหม (ตาราง W ให้ไบต์ก่อน call · R ให้ call ก่อนไบต์ เรียงตาม file offset) -- ฟังก์ชันเดียวสองทิศ หรือคนละทาง
3. `CALL 0x0072EC50` และช่อง `INDIRECT(DEREF(DEREF(DEREF(OBJ+0x14))+0x10))` เขียน/อ่านอะไรลงสาย · ตัวไหนคือ nested record serializer `[0x0072e590,0x0072e691)` ที่ `RE-227` พิน · มีอะไรคั่นกลางอีกไหม
4. คลาสนี้อ่าน record ได้กี่ตัวต่อข้อความ และ `vital_version` ที่ผู้อ่านยอมรับคือค่าใด (เราส่ง 0)

## เกณฑ์ปิดใบ (ชั้นเดียว -- static IMAGE เท่านั้น)
ค่า/ลำดับ พร้อม SHA ของสแปนที่อ่าน (recompute ได้) · **bounded-negative รับเป็นคำตอบปิดใบ**: "ค่าไม่ได้ถูกกำหนดตายตัวในโค้ด" ปิดใบได้ แล้ว LANE-A เดินทาง "ลองสองค่า" ในรอบ attended แทน

## ใบนี้ไม่ขอ
ชั้น client-observable ไม่อยู่ในใบนี้ · ห้ามบูตไคลเอนต์เพื่อปิดใบนี้ · ถ้าคำตอบทำให้ตั้งค่าได้ LANE-A จะขอบูตหนึ่งครั้ง**พ่วง** `GT-233` ไม่ใช่บูตแยก

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- `0xC4AF` **มีหลักฐานบนจอหนึ่งชิ้น** (`ErrorData=50351` = id ของคลาสเอง · R313 02:07 · `navigationex_survey_record.py:116-211`) ⇒ **ตั้งต้นว่า `msg_id` ถูก** ใบนี้ไม่ได้เปิดมาตรวจ `msg_id`
  🔴 **แต่ห้ามเขียนว่า "พิสูจน์แล้วสองชั้น"** (แก้ตาม pf-adversary D9 รอบ `rs8uyz`/R350 · ถ้อยคำเดิมของ chief ผิด): ครึ่งที่สองของคู่คือ **เฟรมที่เราส่งเอง** ซึ่งเป็น *ตัวกระตุ้น* ไม่ใช่พยานอิสระ มันขัดกับตัวเองไม่ได้ ⇒ มี **หนึ่งการสังเกต + หนึ่งข้อโต้แย้ง (name hash)** ไม่ใช่สองชั้นตาม G5
  ⇒ ถ้าผลของใบนี้ทำให้สงสัย `msg_id` ขึ้นมาจริง **ให้เขียนมา ไม่ใช่กลืนไว้** · control ที่ยังไม่มีใครรัน = ส่ง id ผิดโดยตั้งใจ แล้วดูว่ากล่อง error ยังขึ้นชื่อคลาสนี้ไหม (ถ้าขึ้น = 50351 ไม่ได้ระบุ id ของเรา)
- ห้ามยก `0306` ("encoder ตรง capture ⇒ layout ไม่ใช่ตัวผิด") เป็นฐาน -- **ถอนแล้ว** (`LANE-A 0555` · adversary D2 · `COO 0645`/`0646` ข้อ 1)
- ห้ามเหมาค่าที่วัดได้จากคลาสอื่นมาใช้กับคลาสนี้ (กฎ PER-CLASS)
- G8: ทุกแถวในผลติดป้าย `[วัดแล้ว]`/`[เสนอ]`

## แยกจากใบไหน
`RE-227` (กลไก provisioning · ยังไม่ถูกหักล้าง) · `RE-086`/`RE-087`/`RE-090` (ผลเดิม commit แล้ว ห้ามขอซ้ำ) · `#797` วางโค้ดรองรับไว้แล้ว (`outer_leading_byte` · `None` = ไบต์เดิมเป๊ะ ไม่มีอะไรบนสายเปลี่ยนจนกว่าใบนี้จะตอบ)

## ถ้าผลออกทางลบ
ปิดเป็น bounded-negative พร้อมระบุว่า static อ่านไม่ได้เพราะอะไร · LANE-A เปิดรอบ attended "ลองสองค่า" พ่วง `GT-233`

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-A** (cc chief, COO) · LANE-A บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง (§5 "ใครเปิดใบคนนั้นบริโภค") · ถ้าผลขอ attended capture ⇒ LANE-A เปิดใบ GT ในรอบเดียวกัน (`COO 2142`)

---

---

## RE-259 UPDATEATTRVITAL-0X309A-IS-IT-EVER-SENT-FOR-CNETNPC-001  [PASS -- LANE-DB ปิดแล้ว 2026-09-05, ดู pf_bridge/notes_to_chief/20260905_1323_RE-259-RESULT-UPDATEATTR-TARGETS-CMYACTOR-ONLY.md, ตัดกลุ่ม 1+2 (9 VA) ออกจากรายการค้างของ piece 3, ไม่เปิดใบใหม่ (player-only)]

> numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `256` (`RE-256`) · `257`/`258` ถูกจองโดยใบ GT สองใบในรอบเดียวกันนี้ => ใบนี้ `259` · `RE-259`/`GT-259` = **0 hit ทั้งสามที่ก่อนวาง** [วัดแล้ว chief `pv4zg1`/R352]
> ที่มา: `notes_to_chief/20260904_1748_LANE-DB-RE-TICKET-piece3-resend-adjudication-11-outlier-vas-sharpened.md` ข้อ (ก) -- จดหมายฉบับนั้นสั่งชัดว่าต้องเป็น **สองใบคนละรูป** ใบนี้ = กลุ่ม 1+2 (9 VA) · กลุ่ม 3 (x=26,27) = `RE-260` **ห้ามรวมสองใบเข้าด้วยกัน**

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกาใหม่ `AGENTS.md` §7 · `COO 0646` ข้อ 2)
**เจอ**
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv:66` = `0x309A UpdateAttrVital` [วัดแล้ว chief] (ไฟล์อยู่ราก `pf_bridge` ไม่ใช่ใน `external/`)
- `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md:1025` และ `:1032-1036` (`RE-061`/`RE-062` ปิดแล้ว) -- **ตัดคำถามออกไปแล้วครึ่งใบ** [วัดแล้ว chief]: handler ของ `UpdateAttrVital` = `0x5F2400` · resolve target ด้วย **class id ใน generic attribute map** (`lookup 0x463800` / `insert 0x463720`) ไม่ใช่ `[actor+0x3E8]` ไม่ใช่ identity tag `0x32` · bind thunk `0x4698B0` **type-check `CMyActor`** แล้วอ่าน slot ที่ `0x4698DF` โดยไม่สร้าง · slot สร้างที่ `CMyActor` ctor (`0x44CA71`/`0x44CBC1`) · image SHA `9627...B623`
  => 🔺 ชุดนี้ derive จาก attr block ของ `CSkillAttr` (class id `0x1661`) ไม่ใช่ ActorAttr ของ 9 VA นี้ -- **PER-CLASS (§14 ข้อ 13 ค) ห้ามเหมา** ใบนี้จึงยังเปิดจริง แต่คำถามแคบลงตามหัวข้อล่าง
- `notes_to_chief/reference_codex_attr/pf_rederive_attr_semantics.py:5432-5448` = บล็อก `("CNetNPC", {...})` ของ x=7: `source_load_va=0x0045C109` · `producer_va=0x0045C11A` · span `[0x0045BF40,0x0045C15D)` · `span_sha256=afb5662a3f1a81c98de8ed77d82262747b8563ce25be88d041c8dea89e52fb72` · semantic `MOBS.n_SPEED_WALK_...` [วัดแล้ว chief] · `:5471-5472` `("BasicAttr",0x68)/(0x6C) -> "CNetNPC"` มีอยู่แล้วในไฟล์เดียวกัน [วัดแล้ว chief]
- `CLIENT_RE_QUEUE.md:4158` `RE-198` (vital_version byte) · `:3841` `RE-194` (ค่าของ x=7) · `:3756` `RE-193` (ค่า default 7 ฟิลด์) -- แตะคลาสเดียวกันแต่ **คนละคำถามทั้งสามใบ** ไม่มีใบใดถามว่า "ส่งถึง actor คลาสอะไร" [วัดแล้ว chief] => ไม่ใช่ใบซ้ำ

**ไม่เจอ**
- `ค้นใน pf_bridge\external\ แล้ว: ไม่เจอ` -- `grep -rn "CNetNPC\|CMyActor" external/` = **0 hit ทั้งต้นไม้** [วัดแล้ว chief] ⇒ ตอบจาก `external/` ไม่ได้ นี่คือเหตุผลของป้าย `STATIC-ON-BRIDGE`
- `ค้น gamedata แล้ว: ไม่เจอ` -- `grep -in "ActorAttr\|UpdateAttr\|CNetNPC" gamedata/` = **0 hit** [วัดแล้ว chief] (ตรงขอบเขต: เรื่อง wire ไม่ใช่ตารางข้อมูลเกม)
- บรรทัดที่มีทั้ง `UpdateAttrVital|0x309A` และ `CNetNPC|CMyActor` พร้อมกันทั้ง `pf_bridge` = มีแต่ **จดหมายต้นทางเอง** (`...1748...md:73`) กับบันทึกรอบของ LANE-DB (`rounds/DB_20260904_1733_...md:99`) ⇒ เป็นคำถาม ไม่ใช่หลักฐาน [วัดแล้ว chief]
- `persistence_attr_compose.py` **ไม่มีอยู่ในต้นไม้ `pf_bridge`** (`grep -rn RESEND_ADJUDICATED` เจอเฉพาะร้อยแก้วใน `rounds/`+`notes_to_chief/`) [วัดแล้ว chief] ⇒ เลขบรรทัดสองแหล่งขัดกันเอง (จดหมายว่า `:95-113` · `rounds/DB_20260904_1434_f9p5fw...md:49` ว่า "บรรทัด 420") **ห้ามผู้ทำอ้างเลขบรรทัดใดเลย** [ทั้งสองเลข = [เสนอ] ของต้นทาง]
- negative check ของจดหมาย (11 VA + 15 span vs `external/PF_SERIALIZER_FIELDS.tsv` range-intersection = ไม่ตรงสัก span) = **[เสนอ] ของ LANE-DB ยังไม่ทำซ้ำ** · ส่วนที่ chief ยืนยันเองได้: `grep -in "0045C11A\|0045C0D6\|0045C0F9\|0045BF40\|00464AAF" external/` = **0 hit** [วัดแล้ว chief] -- สอดคล้องกัน แต่คนละวิธี ไม่ใช่การ verify วิธีเดิม (G1)

## คำถามเดียว (หนึ่งใบหนึ่งคำถาม ห้ามพ่วง)
เส้นทาง `0x309A`/`UpdateAttrVital` **address ถึง actor คลาส `CNetNPC` ได้หรือไม่ หรือรับเฉพาะ player-class (`CMyActor`) เท่านั้น** -- เดินต่อจากสิ่งที่ปิดแล้ว: (1) type-check `CMyActor` ที่ bind thunk `0x4698B0` เป็น gate เดียวบนเส้นทางหรือไม่ · (2) target resolution ของ handler `0x5F2400` (`0x463800`/`0x463720`) ยอมรับ receiver ที่ไม่ใช่ `CMyActor` ไหม · (3) มี bind/apply site อื่นของ `0x309A` นอก `0x4698B0` อีกไหม

## เกณฑ์ปิดใบ (ชั้นเดียว -- static IMAGE เท่านั้น ไม่มีชั้น client-observable)
- **PASS**: รายชื่อ call site + VA ของ gate ทุกจุดตั้งแต่ handler ถึง apply พร้อม `span_sha256` ทุกช่วง + image sha + `generation_id` แล้วตอบว่า `CNetNPC` เข้าถึงได้/ไม่ได้
- **bounded negative = คำตอบเต็ม ไม่ใช่ผลรอง**: ถ้าพิสูจน์ได้ว่า "player-class เท่านั้น" ⇒ กลุ่ม 1 (x=7,11,12) + กลุ่ม 2 (x=15,30,46,49,50,51) รวม **9 แถวตกประเด็นทั้งชุด** โดย LANE-DB ไม่ต้องวัดอะไรเพิ่ม
- เดินครบแล้วตัน ⇒ ระบุ VA ที่ตัน + บอกว่าอะไรจะปลดล็อก (capture ชนิดไหน หรือใบ static ถัดไป)

## ใบนี้ไม่ขอ
ไม่ขอ **ค่า** ของฟิลด์ใดเลย (`RE-194`/`RE-193` ปิดแล้ว ห้ามขอซ้ำ) · ไม่ขอเรื่อง x=26/27 (= `RE-260` **ห้ามรวม**) · ไม่ขอชั้น client-observable · **ห้ามบูตไคลเอนต์เพื่อปิดใบนี้** · ไม่ขอให้แตะโค้ด

## ห้ามสรุปสิ่งเหล่านี้ (nonclaims -- ยกจากจดหมายต้นทางครบทั้งสี่ข้อ ห้ามตัด)
1. ห้ามเขียนว่าผลใบนี้ทำให้ `RESEND_ADJUDICATED` เติมได้แม้แถวเดียว -- เซตว่าง **โดยเจตนา** และต้องว่างต่อไปหลังใบนี้ปิด
2. negative check กับ `PF_SERIALIZER_FIELDS.tsv` **ไม่** พิสูจน์ว่าไม่มี codec ใดแตะที่อยู่เหล่านี้ในอิมเมจ ~10MB -- พิสูจน์แค่ว่าไม่อยู่ในสารบัญที่สำรวจไว้
3. ยังไม่มีใครตรวจว่า `0x309A` เคยส่งให้ `CNetNPC` จริง -- นั่นคือคำถามของใบนี้ ห้ามตั้งต้นว่ารู้คำตอบ
4. ห้ามเดาความหมาย x=26/27 จากชื่อฟิลด์ (`state_record_forced_flag`/`source_state_appearance_byte`)
5. `[chief เติม]` ผล `RE-061`/`RE-062` เป็นของ `CSkillAttr` (`0x1661`) **PER-CLASS ห้ามเหมา** · และกลุ่ม 1 เป็น **คำเตือน ไม่ใช่คำตอบ**: x=7/11/12 มาจาก MOBS template ของ `CNetNPC` คนละแหล่งกับ construction default ของ 17 แถวที่ใช้ `default_writer_va` กลาง (`0x00464AAF-0x00464E16`) -- resend ค่าเดียวกันให้ NPC อาจผิดตัว
6. `[chief เติม]` G8: ทุกแถวในผลติดป้าย `[วัดแล้ว]`/`[เสนอ]` · G1: ห้ามปิดข้อใดด้วยแหล่งเดียว

## แยกจากใบไหน
`RE-198`/`RE-194`/`RE-193` (คนละคำถาม ปิดแล้วทั้งสาม) · `RE-241` (มอนเดินเข้า `CNetNPC` จริงในชั้น static/wire -- ใบนี้ถามฝั่ง **ส่ง attr** ไม่ใช่ฝั่ง census) · `RE-260` (กลุ่ม 3 -- จดหมายต้นทางห้ามปนกับใบนี้โดยตรง)

## ถ้าผลออกทางลบ
"player-class เท่านั้น" = **ปิด PASS** และ redirect: LANE-DB ตัด 9 แถวออกจากรายการค้างของ piece 3 ได้ทันที เหลือเฉพาะกลุ่ม 3 ที่ `RE-260` ถือ · ถ้าตอบว่า `CNetNPC` เข้าถึงได้จริง ⇒ เป็นคำเตือนแรง (ห้าม resend default กลางให้ NPC) และ LANE-DB ต้องเปิดใบใหม่เรื่อง per-class default -- **ใบถัดไป ไม่ใช่ใบนี้**

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-DB** (cc chief, COO) · บรรทัดแรกเขียนว่า `ขอให้ LANE-DB กรอก ### result: และปิดหัวใบเอง` (§5) · ไม่ผูก deadline (`PANYA-DECISION 20260904_0233` บันไดไมล์สโตนไม่มีกำหนดวัน)

### result:
(ว่าง -- รอ RE runner)

---


---

## RE-260 ACTORATTR-0X99-0X9A-CONCRETE-OWNER-CLASS-001  [DONE -- LANE-DB ปิดแล้ว 2026-09-05, ดู pf_bridge/notes_to_chief/20260905_1327_RE-260-RESULT-CONCRETE-OWNER-BOUNDED-AT-GENERIC-ACTORATTR.md, x=26/x=27 คงนอก RESEND_ADJUDICATED, ไม่เปิดใบใหม่, ห้าม rerun image เดิมจนกว่าจะมีหลักฐานชนิดใหม่]

> numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `256` (`RE-256`) · `257`/`258` ถูกจองโดยใบ GT สองใบรอบเดียวกัน · `259` = `RE-259` => ใบนี้ `260` · `RE-260`/`GT-260` = **0 hit ทั้งสามที่ก่อนวาง** [วัดแล้ว chief `pv4zg1`/R352]
> ที่มา: `notes_to_chief/20260904_1748_LANE-DB-RE-TICKET-piece3-resend-adjudication-11-outlier-vas-sharpened.md` ข้อ (ข) = **กลุ่ม 3 เท่านั้น (x=26, x=27)** · 🔺 จดหมายห้ามรวมใบนี้กับ `RE-259` โดยตรง ("คนละระดับ ห้ามปนกัน") -- ใบนี้เริ่มจากศูนย์ ใบโน้นเดินบนเส้นทางที่มีของอยู่แล้ว

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกาใหม่ `AGENTS.md` §7 · `COO 0646` ข้อ 2)
**เจอ**
- `notes_to_chief/reference_codex_attr/PF_A2_ATTR_FIELD_DELTA.tsv:8-9` = `ActorAttr@0x99` (R และ W) · `:10-11` = `ActorAttr@0x9A` (R และ W) [วัดแล้ว chief -- เปิดอ่านทีละแถวเอง ไม่ใช่เชื่อบทสรุป] แถวทั้งสี่ให้: `applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr` · `scope_status=UNKNOWN` · `EXPLICIT_AUDIT_OPEN_NO_COMPLETE_TYPED_OWNER_CENSUS` · `scope_blocker="the field behavior/meaning is bounded, but no complete typed owner/consumer-class census proves which concrete class attaches and consumes this Attr field"` · สายสืบทอด `PcRefObject>Attribute>DBAttribute>BasicAttr>ActorAttr` · field name `state_record_forced_flag` (`@0x99`) / `source_state_appearance_byte` (`@0x9A`) · tag `0x0B` len 1 · gate `+0x1BC != 0 AND +0x1B4 & 0x00002000` · `default_writer_va=0x00464D5D` · image sha `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
  => **สิ่งที่ตารางให้แล้ว ถูกตัดออกจากคำถามใบนี้แล้ว** (พฤติกรรม/ตำแหน่ง/gate/ค่า default) เหลือเฉพาะ **ใครเป็นเจ้าของคลาสรูปธรรม**
- `external/PF_SERIALIZER_FIELDS.tsv:8-9` -- **เจอแถวชื่อ `ActorAttr` จริง แต่เป็น `EMPTY`** (`wire_empty_argument_value_copier@0x0043BB80` · span `[0x0043BB80,0x0043BB91)` · sha `b625098be0bbf3e36927c8dce2ccf3cf171563fc8f1465a41039974b332c19c0`) [วัดแล้ว chief] ⇒ สารบัญ serializer **ไม่ให้เจ้าของคลาส** ห้ามอ้างแถวนี้ว่าตอบใบนี้แล้ว
- `CLIENT_RE_QUEUE.md:3756` `RE-193` (ปิดแล้ว) ครอบ x=14,25,36,41,42,43,54 -- 🔺 **ใกล้มากแต่ไม่ใช่**: x=42 ของใบนั้นคือ `u8_9B_pairB (0x09B)` ไม่ใช่ `@0x99`/`@0x9A` [วัดแล้ว chief: `grep -n "0x099\|0x09A\|0x09B" CLIENT_RE_QUEUE.md` คืน `3756`/`3806` ซึ่งเป็น `0x09B` ทั้งคู่]

**ไม่เจอ**
- `ค้นใน pf_bridge\external\ แล้ว: ไม่เจอเจ้าของคลาส` -- `grep -rn "CNetNPC\|CMyActor" external/` = **0 hit ทั้งต้นไม้** [วัดแล้ว chief] ⇒ census คลาสรูปธรรมทำจากสะพานไม่ได้ นี่คือเหตุผลของป้าย `STATIC-ON-BRIDGE`
- `ค้น gamedata แล้ว: ไม่เจอ` -- `grep -in "ActorAttr\|UpdateAttr\|CNetNPC" gamedata/` = **0 hit** [วัดแล้ว chief]
- `grep -rn "ActorAttr@0x99\|ActorAttr@0x9A\|state_record_forced_flag\|source_state_appearance_byte"` ใน `CLIENT_RE_QUEUE.md` / `GAME_TEST_QUEUE.md` / `archive/` = **0 hit ทั้งสามที่** [วัดแล้ว chief] ⇒ ไม่เคยมีใบไหนถามสองฟิลด์นี้เลย ไม่ใช่ใบซ้ำ
- ไม่มี RTTI / string / consumer class ผูกกับสองฟิลด์นี้แม้แต่ตัวเดียวในคลัง commit -- [วัดแล้ว LANE-DB ในจดหมาย `1748` · chief ยืนยันซ้ำเฉพาะคอลัมน์ของ `PF_A2_ATTR_FIELD_DELTA.tsv` ข้างบน ไม่ได้ census เอง]

## คำถามเดียว (หนึ่งใบหนึ่งคำถาม)
**คลาสรูปธรรมใดเป็นผู้ attach และผู้บริโภคของ `ActorAttr@0x99` และ `ActorAttr@0x9A`** -- ตอบด้วย RTTI/vtable/type node + span ของ consumer จริง ไม่ใช่ด้วยชื่อฟิลด์ ไม่ใช่ด้วยการอนุมานจากคลาสฐาน `ActorAttr`

## เกณฑ์ปิดใบ (ชั้นเดียว -- static IMAGE เท่านั้น ไม่มีชั้น client-observable)
- **PASS**: ชื่อคลาสรูปธรรม + เส้นทาง attachment (RTTI/vtable/type node) + VA ของจุดบริโภคจริง + `span_sha256` ทุกช่วง + image sha + `generation_id` · ถ้ามีมากกว่าหนึ่งคลาส ให้ **แยกหนึ่งแถวต่อหนึ่งคลาส** ตามที่คอลัมน์ `scope_next_step` ของตารางสั่งไว้เอง
- **bounded negative รับเป็นคำตอบปิดใบ**: "census เดินครบแล้วยังไม่ผูกคลาสรูปธรรมได้ เพราะตันที่ VA/โครงสร้างใด" ปิดใบได้ -- และมีค่าเท่าผลบวก เพราะมันเปลี่ยนสถานะจาก "ไม่มีใครลอง" เป็น "ลองแล้วตันตรงนี้" แล้ว LANE-DB จะรู้ว่าต้องรอ capture ชนิดใดแทน
- 🔺 ทั้งสองฟิลด์ต้องตอบ **แยกกัน** (`@0x99` หนึ่งข้อ `@0x9A` หนึ่งข้อ) ห้ามตอบรวมเป็นข้อเดียว แม้จะได้คลาสเดียวกัน

## ใบนี้ไม่ขอ
ไม่ขอ **ค่า**/พฤติกรรม/ตำแหน่งของฟิลด์ (ตารางปิดไปแล้ว: `PROVEN_EXACT`/`PROVEN_ROLE_ONLY`) · ไม่ขอเรื่องเส้นทาง `0x309A`/`CNetNPC` (= `RE-259`) · ไม่ขอชั้น client-observable · **ห้ามบูตไคลเอนต์เพื่อปิดใบนี้** · ไม่ขอให้แตะโค้ด

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- 🔺 **ห้ามเดาความหมายจากชื่อฟิลด์** `state_record_forced_flag`/`source_state_appearance_byte` -- ชื่อพวกนี้เป็น role name ที่ codex ตั้ง ไม่ใช่หลักฐานว่าใครเป็นเจ้าของ (nonclaim ข้อ 4 ของจดหมายต้นทาง ยกมาทั้งข้อ)
- 🔺 ห้ามอ้าง `external/PF_SERIALIZER_FIELDS.tsv:8-9` ว่าตอบใบนี้แล้ว -- แถวนั้นเป็น `EMPTY` ให้ span ของ copier ไม่ให้เจ้าของ
- 🔺 ห้ามเหมาผลของ `RE-193` (`@0x9B`) มาใช้กับ `@0x99`/`@0x9A` -- PER-CLASS/PER-FIELD (§14 ข้อ 13 ค) ต่อให้ไบต์ติดกัน
- 🔺 ห้ามอ้างว่าใบนี้เติม `RESEND_ADJUDICATED` ได้ -- เซตนั้นยังต้องว่างหลังใบนี้ปิด (nonclaim ข้อ 1 ของต้นทาง)
- 🔺 ต้องอ่านคอลัมน์ `nonclaim`/`residual_*` ของทุกแถว Codex ที่ยกมา แล้วคัดลอกข้อความนั้นลงในผล (§14 ข้อ 13 ข) -- แถว `:8-11` มีข้อความ `structural/consumer role is proved but the broader gameplay noun or full value domain is not unique`
- G8: ทุกแถวในผลติดป้าย `[วัดแล้ว]`/`[เสนอ]` · G1/G6: ห้ามปิดด้วยการอ่านครั้งเดียวหรือแหล่งเดียว ต้องมี `span_sha256` ทุกช่วง

## แยกจากใบไหน
`RE-259` (กลุ่ม 1+2 · 9 VA · คนละระดับของคำถาม -- จดหมายต้นทางสั่งห้ามรวม) · `RE-193` (7 ฟิลด์ ปิดแล้ว ไม่มี `@0x99`/`@0x9A`) · `RE-194` (ค่าของ x=7) · `RE-241` (`CNetNPC` ในชั้น census ของมอน ไม่ใช่ owner ของ Attr field)

## ถ้าผลออกทางลบ
bounded negative ⇒ LANE-DB ยังคง **ไม่** เติม `RESEND_ADJUDICATED` และปิด piece 3 ค้างไว้ตามเดิมโดยมีเหตุผลที่ระบุ VA ได้ (แทนที่จะเป็น "ไม่มีใครเคยลอง") · ถ้าคำตอบออกมาเป็น NPC-only ⇒ ผลนี้ไปเสริม `RE-259` แต่ **ไม่แทนกัน** สองใบยังต้องปิดแยก

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-DB** (cc chief, COO) · บรรทัดแรกเขียนว่า `ขอให้ LANE-DB กรอก ### result: และปิดหัวใบเอง` (§5) · ไม่ผูก deadline (`PANYA-DECISION 20260904_0233`)

### result:
(ว่าง -- รอ RE runner)

---


---

## RE-261 STALL-AND-GUILD-STORAGE-FIELD-SEMANTICS-FROM-A-REAL-SESSION-001  [OPEN -- 🔺 `[NEEDS-ATTENDED-CAPTURE]` (จดหมายต้นทางระบุเองว่า **ปิดจาก static เดี่ยวไม่ได้**) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · ใบ GT คู่ของมัน = **`GT-262` (chief จองเลขไว้แล้วรอบ `pv4zg1`/R352 · LANE-UI เป็นผู้เขียนเนื้อใบ GT ในรอบถัดไป)** ตาม `AGENTS.md` §7 (`COO-DECISION 20260904_2142` ข้อ 3) -- **ผู้เทสอ่าน `GAME_TEST_QUEUE.md` เท่านั้น ไม่เคยอ่านไฟล์นี้** ถ้าไม่มีใบ GT จะไม่มีใครเห็นใบนี้ตลอดกาล]

> numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `256` (`RE-256`) · `257`/`258` = ใบ GT สองใบรอบเดียวกัน · `259`/`260` = `RE-259`/`RE-260` => ใบนี้ `261` · `RE-261`/`GT-261`/`GT-262`/`RE-262` = **0 hit ทั้งสามที่ก่อนวาง** [วัดแล้ว chief `pv4zg1`/R352]
> ที่มา: `notes_to_chief/20260905_0456_LANE-UI-RE-TICKET-stall-and-guild-storage-opcodes-known-fields-partial.md` (สารบัญ 15 แถวของ LANE-UI · สองแถวสุดท้ายที่ยังไม่มีใบ)

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกาใหม่ `AGENTS.md` §7 · `COO 0646` ข้อ 2)
**เจอ**
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` -- opcode มีจริงทั้งสองระบบ [วัดแล้ว chief ทีละบรรทัด]: `:54 0x2A3E StallOpenVital` · `:68 0x30FE StallStartVital` · `:89 0x3DE4 StallOperateVital` · `:116 0x462C GCGSSS_GuildStorageVital_ReArrangeResult` · `:160 0x5CAD GuildStorageOpenVital` · `:192 0x70D0 GuildStorageResultVital` · `:208 0x7F17 GCGS_GuildStorageCmdVital` · `:209 0x7F5B GSSS_GuildStorageCmdVital` · `:224 0x8B66 GCSS_GuildStorageOpenVital` · `:250 0xA1B3 DBSS_GuildStorageUpdateVital` · `:262 0xAD7A DBSS_GuildStorageInitialVital` · `:274 0xBAE7 GCGSSS_GuildStorageResultVital` (ต่างจาก `RE-235` ที่ชื่อคลาสไม่เคยเป็นสตริงเลย -- ใบนี้ **ไม่ต้องหา opcode**)
- `external/PF_PROTOCOL_REGISTRY.tsv:210` -- `GCSS_GuildStorageOpenVital` มี VA เต็มแถว (`0x00F0B474` / `0x00BF96C0` / `0x006724A0` / ...) [วัดแล้ว chief] ⇒ แก้สารบัญเดิม `0400` ที่เขียนว่า "ชื่อคลาสเท่านั้น" ซึ่งเกินจริง
- `external/PF_FIELD_VALIDATION.tsv:1018-1023` (`StallStartVital`/`StallOpenVital`/`StallOperateVital` W+R) และ `:418-421` (`GCSS_GuildStorageOpenVital`/`GCGS_GuildStorageCmdVital` W+R) -- ทุกแถว `observed_frames=0` `capture_file_count=0` `status=NOT_OBSERVED` `source=CAPTURE` [วัดแล้ว chief]
- สมมติฐานที่มีอยู่แล้วของ `StallOperateVital` serializer `0x76A630` (chief round 75 · 2026-08-18) -- `u8 tag 0x08 @+0x14` · `qword tag 0x32 @+0x18` · **`u32 tag 0x14 @+0x20 = price`** · `string @+0x24` · [วัดแล้ว chief จาก **สองแหล่งในสะพาน**ไม่ใช่แหล่งเดียว (G1): `archive/CHIEF_CONTINUATION_ARCHIVE_20260818_R77.md:64` และ `FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md:132`] · แหล่งที่จดหมายอ้าง (`docs/FUNCTIONAL_COVERAGE.json` → `use_drop_sell`, รีโป pirate-force-server) **ไม่มีในต้นไม้ `pf_bridge`** -- carry over เป็น [เสนอ] ของ LANE-UI
- `ค้น gamedata แล้ว: เจอ (แต่ไม่ตอบใบนี้)` [วัดแล้ว chief -- 🔺 จดหมายต้นทาง **ไม่ได้ค้นต้นไม้นี้เลย**]: `gamedata/PF_GAMEDATA_LUA_API.tsv:122` = `Guild.OpenGuildStorage` (script `Quest/q_guildstorage.lua` · สถานะ `UNRESOLVED` · เหตุผล "no NUL-delimited string, or no push<nameVA> + mov[esp+X],delegate pattern found") · `gamedata/PF_GAMEDATA_INDEX.tsv:117` = ตาราง `CONSTDATA_TH.STALL_SET` (span `0x0080C0C0-0x0080C85A`) · `gamedata/PF_GAMEDATA_COLUMNS.tsv:1924-1933` = คอลัมน์ของ `STALL_SET`: `n_ID` `n_STATUS` `n_EFFECT_RESIDENT` `s_NAME` `s_STALL_ITEM` `n_UI_TEXT` `s_HK_VER` `s_TC_VER` `s_JP_VER` `s_TH_VER` -- **ไม่มีคอลัมน์ราคา** ⇒ สองแถวนี้ไม่ย่อคำถามของใบ แต่ผู้เขียน `GT-262` อาจต้องใช้ `STALL_SET.n_ID` เพื่อระบุว่าเปิดแผงชนิดใด

**ไม่เจอ**
- `ค้นใน pf_bridge\external\ แล้ว: ไม่เจอความหมายฟิลด์` -- `grep -c "^GuildStorageOpenVital\b"` / `"^GuildStorageResultVital\b"` = **0 ทั้งใน `external/PF_SERIALIZER_FIELDS.tsv` และ `external/PF_FIELD_VALIDATION.tsv`** [วัดแล้ว chief] · hit ที่ไม่ anchor (48 ครั้ง) เป็นของ `GCSS_`/`GCGSSS_` ซึ่งเป็นคนละคลาส ⇒ 🔺 **สองคลาสชื่อเปล่านี้ = "ไม่ถูก track" ห้ามเขียนว่า `NOT_OBSERVED`** สองสถานะนี้ต่างกัน (`NOT_OBSERVED` = มีแถว เคยสแกน ไม่เคยเจอเฟรม · ไม่ถูก track = ไม่มีแม้แถว `UNKNOWN` มีแต่ opcode จาก R38)
- `CLIENT_RE_QUEUE.md` / `GAME_TEST_QUEUE.md` -- `grep -in "stall\|guildstorage\|guild storage"` **ไม่มีใบเรื่องนี้เลยสักใบ** [วัดแล้ว chief] · hit ทั้งหมดเป็น substring ของ `install` (`CLIENT_RE_QUEUE.md:2956,3093,3153,3155` ฯลฯ) กับ `GAME_TEST_QUEUE.md:5604` ที่ใช้คำว่า "stall" ในความหมาย UI ค้าง (`CTracePathReqVital`, เรื่อง `GT-120`) -- 🔺 `\b` **ไม่กัน `install`** เพราะ `stall` จบพอดีท้ายคำ ต้องกรองด้วยมือ (บทเรียนของ `pf-adversary` รอบ `npixtd` ยกมาทั้งข้อ)
- `external/PF_TAG_CENSUS.tsv` -- tag `0x08`/`0x0F`/`0x14`/`0x19`/`0x32` ทุกตัว `proven_semantics=UNKNOWN` [เสนอ ของ LANE-UI · chief ยังไม่ verify ซ้ำ] ⇒ "resolved" = รู้ offset/type ของไบต์ **ไม่ใช่** รู้ว่าฟิลด์นั้นคือ item id/ราคา/slot

## จำนวนฟิลด์ที่แกะได้แล้ว (ยกจากจดหมาย `0456` · วิธี awk มือ ไม่มีสคริปต์ commit ⇒ [เสนอ] ทั้งตาราง)
`StallStartVital` 18/44 · `StallOpenVital` 12/40 · `StallOperateVital` 18/26 · `StallModule_Client`+`StallActorAttr` รวม 0/8 (non-field/EMPTY -- chief ยืนยัน `external/PF_SERIALIZER_FIELDS.tsv:6917-6918` เป็นแถว `StallActorAttr` จริง [วัดแล้ว]) · `GCSS_GuildStorageOpenVital` 8/12 · `GCGS_GuildStorageCmdVital` 12/20 · อีก 10 คลาสในตระกูลนับแบบ bucket ตั้งแต่ 0/4 (`DBSS_GuildStorageInitialVital`) ถึง 136/293 (`GSSS_GSInitialGuildDataVital`)

## คำถามของใบ (เรียงเป็นลำดับบังคับ ห้ามสลับ)
1. **positive control ก่อนอย่างอื่นทั้งหมด**: สอง trial ของ `StallOperateVital` ที่ **ต่างกันเฉพาะราคาที่พิมพ์บนจอ** -- ไบต์ที่ `+0x20` (`u32` tag `0x14`) เปลี่ยนตามหรือไม่ ⇒ ยืนยัน/หักล้างสมมติฐาน `0x76A630` = ราคา ของ chief round 75
2. เฉพาะเมื่อข้อ 1 ใช้ได้จริง: เปิดแผง/วางไอเทม (`StallStartVital` `0x30FE` · `StallOpenVital` `0x2A3E`) แล้วผูก opcode กับเฟรมที่เห็นจริง
3. เฉพาะเมื่อข้อ 1 ใช้ได้จริง: เปิดคลังกิลด์ + ฝาก/ถอน (`GCSS_GuildStorageOpenVital` `0x8B66` ก่อน แล้ว `GCGS_GuildStorageCmdVital` `0x7F17` -- ฟิลด์ resolved มากที่สุดในตระกูล)
🔺 **ห้ามเดา tag ที่เหลือ** (`+0x14`/`+0x18`/`+0xB0` ฯลฯ) ก่อนข้อ 1 ผ่าน -- นี่คือลำดับที่จดหมายต้นทางขอไว้ตรง ๆ

## เกณฑ์ปิดใบ (ชั้น wire/DB เท่านั้นในไฟล์นี้)
- ปิดใบได้เมื่อมี **เฟรมจริงคู่หนึ่งจากเซสชันเดียวกัน** ที่ต่างกันเฉพาะราคา + hex ทั้งสองเฟรม + opcode ที่อ่านได้ + คำตัดสินว่า `+0x20` เปลี่ยนตามหรือไม่
- 🔺 **ชั้น client-observable ไม่อยู่ในใบนี้** สิ่งที่คนต้องเห็นบนจอ (หน้าต่างแผง/ช่องราคา/ป้ายชื่อในเฟรม) เป็นเนื้อของ **`GT-262`** เท่านั้น -- **ห้ามเขียนเกณฑ์ที่เอาชั้นหนึ่งไปเป็นหลักฐานของอีกชั้น** ทั้งในใบนี้และในใบ GT
- **ผลลบมีค่าเท่าผลบวก**: ถ้า `+0x20` ไม่ขยับตามราคา ⇒ สมมติฐาน chief round 75 ถูกหักล้าง (เป็น finding ไม่ใช่ความล้มเหลว) และ redirect ไปหาว่าฟิลด์ใดขยับแทน · ถ้า **ไม่มีเฟรมออกเลย** ⇒ บันทึกว่าเป็นการไม่ยืนยันเส้นทาง UI ไม่ใช่การหักล้าง opcode

## ใบนี้ไม่ขอ
ไม่ขอ `GuildStorageOpenVital`(`0x5CAD`)/`GuildStorageResultVital`(`0x70D0`) ชื่อเปล่า (ไม่มีแถวให้เทียบเลย -- capture ไปก็ไม่มีที่ลง) · ไม่ขอ 10 คลาสที่นับแบบ bucket · ไม่ขอความหมาย tag ทุกตัว · ไม่ขอให้แตะโค้ด · ไม่ขอผลจากการเดา hash ชื่อคลาส

## ห้ามสรุปสิ่งเหล่านี้ (nonclaims ยกจากจดหมาย `0456` ทั้งหกข้อ ย่อความ)
① ตัวเลข real/total เป็นตัวเลข derive มือรอบเดียว ไม่มีสคริปต์ commit ให้ทำซ้ำ ⇒ [เสนอ] ② `+0x20 = ราคา` เป็น **สมมติฐาน static ที่ยังไม่ยืนยันด้วย attended** ห้ามเขียนเป็นข้อเท็จจริง -- ส่วนฟิลด์อื่นทุกตัวรวมทั้งตระกูล guild storage **ยังไม่มีสมมติฐานใด ๆ เลยจริง** ③ ยังไม่แกะรายฟิลด์ของ `StallOpenVital`/`StallOperateVital` และอีก 12 คลาส ④ ไม่ยืนยันว่า `CALL_UNCLASSIFIED`/indirect-call ที่เหลือแก้ได้ด้วย static รอบใหม่ (ต้องมีไบนารีไคลเอนต์จริง) ⑤ รอบที่ออกจดหมายไม่มีไบต์ออกไปไคลเอนต์เครื่องใดเลย ⑥ ใบ `1120` (เพื่อน/เมล/ปาร์ตี้/เทรด) เป็นคนละ 8 คลาส ไม่ต้องแก้อะไรในใบนั้น
- `[chief เติม]` ห้ามเขียนว่าสองคลาสชื่อเปล่า = `NOT_OBSERVED` (ดูช่องค้น) · `[chief เติม]` G8: ทุกแถวในผลติดป้าย `[วัดแล้ว]`/`[เสนอ]`

## แยกจากใบไหน
`RE-235` (ตลาดมืด/หน้าต่างสำรวจ -- ที่นั่น **ไม่มี** opcode เลย ที่นี่ **มี** opcode ครบ คนละอุปสรรค) · `RE-236`/`RE-237` (สามแถวอื่นของสารบัญ) · `GT-120` (คำว่า "stall" ในความหมาย UI ค้าง ไม่ใช่ระบบแผงขายเอง) · **`GT-262`** = ใบคู่ที่ผู้เทสจะเห็นจริง

## ถ้าผลออกทางลบ
`+0x20` ไม่ใช่ราคา ⇒ สมมติฐาน chief round 75 ถูกหักล้าง เป็นผลของใบนี้เอง และ LANE-UI ต้องเปลี่ยนวิธี (ไล่ฟิลด์ที่ขยับแทนการยืนยันฟิลด์ที่เดาไว้) · ไม่ว่าผลออกทางใด **สองแถวสุดท้ายของสารบัญ 15 แถวจะปิดสถานะได้** และไม่บล็อกแถวอื่นของ LANE-UI

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-UI** (cc chief, COO) · LANE-UI บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง (§5) · 🔺 LANE-UI **ค้างเนื้อใบ `GT-262` ในรอบถัดไป** -- ตราบใดที่ `GT-262` ยังว่าง ใบนี้จะไม่มีทางถูกทดสอบ

> **[อัปเดต round `rp5tq1` 2026-09-05T18:2x+07:00 โดย LANE-UI]** งานสำรองรอบนี้ = ตรวจว่ายังมีช่องแกะฟิลด์เพิ่มของ `StallOpenVital`/`StallOperateVital` จาก static ล้วน (ไม่แตะเครื่อง) ก่อนที่ข้อ 1 (positive control) จะผ่านหรือไม่ -- **ผล = ไม่มี (bounded negative)** อ่าน `external/PF_SERIALIZER_FIELDS.tsv` ทุกแถวของทั้งสองคลาสแล้วนับด้วยมือ (นับซ้ำตรงกับ 12/40 และ 18/26 ที่จดหมาย `0456` ให้ไว้ พอดี -- ไม่มี drift):
> - `StallOpenVital` แถวที่ยังไม่ resolve ทั้ง 28/40 แถวเป็น `PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL` / `CALL_UNCLASSIFIED` (ทั้ง direct `0x00766EF0`/`0x0068E8B0` และ indirect ผ่าน vtable) / `ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C` / `DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04` / `MUTATING_CHAIN_PLUS_04_HELPER` -- ไม่มีแถวไหนเป็น "ลืมอ่าน" หรือ tag ที่มีอยู่แล้วแต่ยังไม่ transcribe
> - `StallOperateVital` แถวที่ยังไม่ resolve 8/26 แถว: 6 แถวเป็นชุดแพทเทิร์นเดียวกันข้างบน + 2 แถว `SUBCALL:0x00766C00 DEREF(+0x40)` (แถวนี้เป็นตัวชี้ไปยัง sub-object เท่านั้น -- ฟิลด์ *ภายใน* sub-object นั้นเอง คือ `DEREF(+0x40)+0x10/+0x18/+0x1C/+0x20` **resolve แล้ว** อยู่ในตัวนับ 18 อยู่แล้ว ไม่ใช่ของแถมที่ยังไม่ได้นับ)
> - **ตรวจว่าแพทเทิร์นเหล่านี้เป็นของเฉพาะ Stall/GuildStorage หรือเป็นเพดาน static ทั้งไฟล์** [วัดแล้ว `grep -c` บน `external/PF_SERIALIZER_FIELDS.tsv` ทั้งไฟล์ 6,932 แถว]: `DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04` = 279 แถวทั้งไฟล์ · `ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C` = 271 แถวทั้งไฟล์ (สอง pattern นี้คือ COM-style AddRef/Release boilerplate ที่กระทบทุกคลาสในเซ็นซัส ไม่ใช่แค่ตระกูลนี้) · target ของ `CALL_UNCLASSIFIED:0x00766EF0`/`0x0068E8B0`/`0x00766DF0` **ไม่ปรากฏเป็นชื่อฟังก์ชันที่ resolve แล้วที่ไหนเลย** ใน `external/PF_RUNTIME_CLASSMAP.tsv` / `PF_PROTOCOL_REGISTRY.tsv` / `PF_DATA_EVIDENCE.tsv` / `PF_INPUT_INVENTORY.tsv` / `PF_PROTOCOL_PRIORITY.tsv` [`grep -rn` ทั้งห้าไฟล์ = 0 hit] ⇒ ไม่มี cross-reference ที่ยืมมาปิดได้
> - **สรุป [เสนอ]**: 12/40 และ 18/26 คือเพดานจริงที่ static จากอาร์ติแฟกต์ที่ commit แล้วไปได้ ไม่ใช่ตัวเลขที่ตกหล่นจากการมองข้าม -- ส่วนที่เหลือทั้งหมดเป็น indirect/dynamic dispatch + PE-import-ไม่มีข้อมูล + COM refcount boilerplate ซึ่งเป็นเพดานเดียวกับที่บล็อกอีกหลายร้อยแถวทั่วทั้งเซ็นซัส ต้องใช้ disassembly เพิ่ม (NEEDS-CLIENT-IMAGE) หรือ attended capture เท่านั้นถึงจะขยับได้ ไม่ใช่งานที่ pf_bridge เพียงอย่างเดียวเปิดได้อีก
> - ไม่ได้ไล่ครบทั้ง 10 คลาสที่นับแบบ bucket (นอกจาก `StallOpenVital`/`StallOperateVital`) ด้วยวิธีนี้ในรอบนี้ -- sample เร็วของ `GCSS_GuildStorageOpenVital`(12)/`GCGS_GuildStorageCmdVital`(20)/`DBSS_GuildStorageInitialVital`(4)/`DBSS_GuildStorageUpdateVital`(14)/`GSSS_GSInitialGuildDataVital`(293) ด้วย `grep -cE` เดียวกันเจอสัดส่วนแพทเทิร์นเดิม (4/12, 6/20, 4/4, 12/14, 148/293 ตามลำดับ) แต่ตัวเลขนี้เป็น pattern-match หยาบ ไม่ใช่การนับมือทีละแถวแบบสองคลาสข้างบน จึงติดป้าย **[เสนอ]** ไม่ใช่ `[วัดแล้ว]`
> - ไม่กระทบเกณฑ์ปิดใบ/ลำดับคำถามข้างบน (ยังคงห้ามเดา tag ก่อนข้อ 1 ผ่านเหมือนเดิม) -- บันทึกนี้แค่ตอบว่า "ยังมีช่องให้ขุด static เพิ่มไหม" ด้วยคำตอบว่าไม่มีแล้ว ไม่ใช่เปลี่ยนเกณฑ์ · จดหมายเต็ม: `notes_to_chief/20260905_1824_LANE-UI-STATUS-re261-static-ceiling-confirmed-plus-backup-recheck.md`

### result:
(ว่าง -- รอ attended capture ผ่าน `GT-262`)

---

## RE-263 PAIR-RELATION-ZERO-GATE-REACHABILITY-AND-DEFAULT-BIT-001  [**CLOSED BOUNDED-NEGATIVE** 2026-09-05T13:12+07:00 โดย LANE-GM รอบ `0dlc07` (ผู้ทำ `pf-static-re` บนคลาวด์) -- **เส้นทางที่สองของ P-2 ปิด แต่ไม่ใช่ด้วยเหตุผลที่ใบเดาไว้**: ข้อ 1 ของใบเดาว่า predicate ถูกข้ามไปกับ typed `CNetNPC` tail -- **หักล้างแล้ว** predicate ถูกเรียกบนเลน identity บวกที่ `0x00444018` (เลนที่ FieldMob ตกลงมา) · ที่ทำให้เป็นทางตัน = จุด emit สไตล์ชื่อสองจุด (`0x00443FE9`/`0x00443FF2`) **ไม่ได้อยู่ใน predicate เลย** เกตด้วย receiver = local `CMyActor` singleton (ป้ายชื่อของผู้เล่นเอง) มอนไปไม่ถึงตลอดกาล · และ operand ของ gate เป็นค่าคงที่ `0` ทุก actor เพราะ presence bit ไม่เคยถูกส่ง (เซิร์ฟเวอร์ compose ไม่ได้ด้วย: `compose_sparse_block({39:0})` -> `field_not_approved_for_the_sparse_path` **รันจริงแล้ว**) · ไม่กระทบ `P2_COLOR_WIRING_BLOCKERS` -- `unaddressed_blockers()` ยังคืน `('faction_is_a_fallback_operand_only',)` (วัดรอบนี้) · ผลเต็ม: `notes_to_chief/20260905_1312_LANE-GM-RE-263-RESULT-second-route-is-a-dead-end.md` · 🔴 **ใบนี้แก้คำผิดของตัวเอง** (ดูบรรทัด "ค้นแล้ว" ข้างล่าง) · ป้ายเดิม `[STATIC-ON-BRIDGE]` (artifact ที่ commit ไว้แล้ว ไม่ต้องรอเครื่อง Panya เว้นแต่ผลชี้ว่าต้องอ่าน disassembly ที่ยังไม่มีในสะพาน แล้วให้แก้ป้ายเป็น `[NEEDS-CLIENT-IMAGE]`) · **เจ้าของใบ/ผู้บริโภคผล = LANE-GM** (เหมือน `RE-222` เดิม) · ผู้ทำ = `pf-static-re` บนคลาวด์ · **ไม่บล็อกใคร** -- P-2 ยังรอ `faction_is_a_fallback_operand_only` เหมือนเดิม ใบนี้แค่เปิดทางที่สองที่ยังไม่มีใครเดิน]

> numbering: ตัวนับร่วมสองคิว คืนสูงสุดที่ `261` (`RE-261`) · `262` = `GT-262` (จองแล้ว) ⇒ ใบนี้ `263`
> ที่มา: `notes_to_chief/20260905_1150_LANE-GM-TO-CHIEF-re-ticket-request-pair-relation-zero-gate-reachability.md` (รอบ `srn7ksvmt`)

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกา `AGENTS.md` §7 · `COO 0646` ข้อ 2 -- ยกจากจดหมายต้นทาง)
**เจอ** -- `notes_to_chief/reference_codex_attr/PF_A2_ATTR_FIELD_DELTA.tsv` rows 6-7 (`grep -n "0x0043C531" notes_to_chief/reference_codex_attr/PF_A2_ATTR_FIELD_DELTA.tsv`): span `0x0043C531`-`0x0043C547` -- อยู่ใน `RELATIONSHIP_PREDICATE_SPAN` เดียวกับที่ `RE-195` วัด (`0x0043C380`-`0x0043C63C`) และมาก่อน `FACTION_COMPARATOR_SOLE_CALL_SITE_VA` (`0x0043C5E0`) · ~~ทดสอบ `ActorAttr+0x98` bit `0x04000000`~~ **← ผิด แก้โดยผลของใบนี้เอง (RE-263): `+0x98` เป็นฟิลด์ **หนึ่งไบต์** `uint8_enum` (`storage_width=1` `tag=0x0B`) และ `0x04000000` คือ **presence bit ใน mask word ที่ `+0x1B4`** ไม่ใช่บิตข้างใน `+0x98` · ไบต์ที่เผยแพร่ในสแปนเป็น `cmp byte ptr [esi+0x98], 0` (`0x0043C531`) กับ `cmp byte ptr [edi+0x98], 0` (`0x0043C53A`) ไม่ใช่ bit test · `gm/attr_wire.py:463` ของเราเองเข้ารหัสถูกอยู่แล้ว (`1 << 26` บน mask, `offset=0x098`)** · semantic name ที่ TSV ตั้งเอง: `CNetActor_pair_relation_zero_gate__CMyActor_value_1_selects_LABEL_NAME_FontStyleID_56_else_55` (พูดถึง FontStyleID ตรง ๆ 56 vs 55) · status = `PROVEN_ROLE_ONLY` (คำของ TSV เอง: "structural/consumer role is proved but the broader gameplay noun or full value domain is not unique") · แถวนี้มาจาก census คนละรอบ **ไม่เคยถูก cross-reference กับ `faction_is_a_fallback_operand_only` มาก่อน**
**ไม่เจอ** -- `grep -rn "FontStyle" gamedata/ external/ archive/ notes_to_chief/consumed/` [วัดแล้ว chief `cwde5m`/R353 addendum, แทนบรรทัดฉบับแรกที่ตัดสินโดยหมวดหมู่ ไม่ใช่ grep จริง — `AGENTS.md` บรรทัด "ประโยคปฏิเสธต้องมี grep กำกับ"]: hit จริง 49 ไฟล์ ทั้งหมดอยู่ใน `archive/` เป็นประวัติของ `RE-191`/style 63 RGB และของจดหมาย `20260831_2245_KA1B-TO-CHIEF-nameboard-fontstyle-selector-presentation-only.md` (ดูหมายเหตุด้านล่าง) -- **ไม่มีแถวไหนใน `gamedata/tables/` เอง** ตอบคำถามสามข้อของใบนี้โดยตรง (reachability ของมอน server-sent ผ่าน gate นี้) `external/00_SEARCH_HERE_FIRST.md`/`gamedata/00_SEARCH_HERE_FIRST.md` เอง ไม่มีแถวชี้มาที่ span `0x0043C400`-`0x0043C547`
🔴 **สิ่งที่เจอใน archive/ ที่ต้องอ่านก่อนตอบใบนี้ (ไม่ใช่ nonclaim ปกติ)**: `archive/notes_to_chief_2026-08/20260831_2245_KA1B-TO-CHIEF-nameboard-fontstyle-selector-presentation-only.md:34` -- **`FontStyle 55 = ขาว, 56 = ชมพูตัวหนา` วัดจากจอจริงแล้ว (MEASURED, client-observable, probe 27 ส.ค.)** ไม่ใช่แค่ IMAGE layer เหมือนแถวอื่นของ TSV เดียวกัน -- ใบนี้ **ไม่ได้ถามความหมายของ 55/56** (รู้แล้ว) แต่ถามว่า**เซิร์ฟเวอร์ไปถึง gate ที่เลือกระหว่างสองค่านั้นได้ไหม**สำหรับมอน (คนละคำถามกับที่ `2245` ปิดไปแล้วสำหรับผู้เล่น) -- ห้ามอ่านผลของใบนี้เป็นการค้นความหมายสี ความหมายรู้แล้ว

## ตรวจไม่ให้ทับ `RE-195` (ปิดแล้ว บังคับตาม `AGENTS.md` §7 "ก่อนเปิดใบ RE ต้อง grep... สิ่งที่ค้นเจอแล้วต้องถูกตัดออกจากคำถามของใบ")
`RE-195` (`CLIENT_RE_QUEUE.md:3914`, CLOSED BOUNDED-NEGATIVE) วัดตาราง style **56/58/59/60/61 ครบแล้ว** แต่บรรทัดสรุปของมันเอง (อ้างที่ `CLIENT_RE_QUEUE.md:5313`) ระบุตรง ๆ ว่า **"ไม่มีแถวชื่อ ชมพู"** ในตารางนั้น -- คือ RE-195 วัดตระกูล 56/58/59/60/61 ในความหมาย "reachable ทางไหน" แต่ตัวแยก **55 vs 56** (ซึ่งคือคำถามของใบนี้) ไม่ได้อยู่ในผลของมัน ⇒ **คำถามของใบนี้ไม่ถูกตัดออก ยังเป็นคำถามที่ยังไม่มีคำตอบจริง** ไม่ใช่การถามซ้ำ

## คำถามของใบ (จาก `PROVEN_ROLE_ONLY` ไปสู่คำตอบที่ใช้ได้จริง)
1. มอนที่ผ่านทาง `field_mobs`/`load_roster` (measured-bypass identity class เดิม) เคยไปถึง gate นี้จริงไหม หรือ gate นี้ถูกข้ามไปพร้อมกับ typed `CNetNPC` tail ทั้งก้อน (อ่าน disassembly/RTTI จริง ไม่ใช่เดาจากชื่อ)
2. ถ้าไปถึง -- ไคลเอนต์อ่านค่า default ของ `ActorAttr+0x98` bit `0x04000000` อย่างไรเมื่อเซิร์ฟเวอร์ไม่เคยส่งบิตนี้เจตนา (เราไม่เคยส่งบิตนี้)
3. gate นี้กับ faction comparator (`0x0043C5E0`) เป็นเส้นทาง**คู่ขนาน**ที่ predicate เดียวกันเช็คก่อนถึงจุดไหน หรือเป็นเส้นทาง**แยกกันคนละผล** (ถ้าขนาน อาจเป็นทางที่สองที่ไปถึง FontStyleID ได้โดยไม่ผ่าน faction เลย)

## เกณฑ์ปิดใบ (ชั้น static เท่านั้นในไฟล์นี้)
- ปิดใบ **PASS/ANSWERED** ได้เมื่อทั้งสามข้อข้างบนมีคำตอบจาก disassembly/RTTI จริง (ไม่ใช่จากชื่อ semantic ที่ TSV ตั้งเอง) พร้อม VA/offset ที่อ้างอิงได้
- ปิดใบ **BOUNDED-NEGATIVE** ได้ถ้าข้อ 1 ตอบว่า "ไม่ถึง" (มอน server-sent ข้าม gate นี้ไปกับ typed tail ทั้งก้อน) -- คำตอบนี้ถือว่าปิดใบเช่นกัน (ปิด P-2 เส้นทางที่สองนี้เป็น dead end ไม่ใช่ความล้มเหลวของใบ) และไม่ต้องตอบข้อ 2/3 ต่อ
- ปิดใบ **NEEDS-CLIENT-IMAGE** ได้ถ้า `pf-static-re` พบว่าต้องอ่าน disassembly ที่ไม่มีในสะพาน -- แก้ป้ายแล้วส่งต่อคิว RE runner ตามปกติ ไม่ใช่การปิดใบ

## ใบนี้ไม่ขอ
ไม่ขอเปลี่ยนคำตอบของ `P2_COLOR_WIRING_BLOCKERS` (`unaddressed_blockers()` ยังคืน 1 ตัวเหมือนเดิม) · ไม่ขอแตะ `gm/name_color_gate.py` เพิ่มจากที่ปักไว้แล้วในรอบ `srn7ksvmt` (ดู PR เซิร์ฟเวอร์ของรอบนั้น) · ไม่อ้างว่าเร่งด่วนกว่าใบอื่นในคิว · ไม่ขอความหมายของ FontStyle 55/56 (รู้แล้ว MEASURED — ดูช่องค้นด้านบน)

## ห้ามสรุปสิ่งเหล่านี้ (nonclaims)
① `PROVEN_ROLE_ONLY` เป็นคำตัดสินของ `PF_A2_ATTR_FIELD_DELTA.tsv` เอง (ชั้น IMAGE) ไม่ใช่คำตัดสินของใบนี้ ② ห้ามเดาคำตอบข้อ 3 (ขนาน/แยกกัน) จากชื่อ semantic ที่ TSV ตั้งเอง ("`pair_relation_zero_gate`" เป็นชื่อที่คนตั้งใบ TSV ให้ ไม่ใช่ผลจาก disassembly ของใบนี้) ③ การที่ span อยู่ใน `RELATIONSHIP_PREDICATE_SPAN` เดียวกับ `RE-195` **ไม่ได้แปลว่า** reachability ของทั้งสองจุดเหมือนกัน (ดูหัวข้อ "ตรวจไม่ให้ทับ RE-195" ด้านบน) ④ ไม่มีข้อมูล capture ของมอนจริงในใบนี้ — สามข้อคำถามตอบได้จาก static เท่านั้น ถ้าตอบไม่ได้จาก static ⇒ ป้าย `[NEEDS-CLIENT-IMAGE]`

## ถ้าผลออกทางลบ
ข้อ 1 ตอบ "ไม่ถึง" (มอน server-sent ข้าม gate นี้ไปกับ typed `CNetNPC` tail ทั้งก้อน) ⇒ **ปิดใบ BOUNDED-NEGATIVE** ตามเกณฑ์ข้างบน ไม่ใช่ความล้มเหลว — เป็นคำตอบที่ปิดเส้นทางที่สองของ P-2 ให้ชัดว่าไม่ใช่ทางออก และ `faction_is_a_fallback_operand_only` (ของ `RE-222`) ยังเป็นทางเดียวที่เหลือเหมือนเดิม · ไม่ว่าผลออกทางใด **ไม่กระทบ `P2_COLOR_WIRING_BLOCKERS`** โดยตรง (ใบนี้ไม่ได้ขอแก้บล็อกนั้น)

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-GM** (cc chief) · LANE-GM บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง (§5)

### result:
(ว่าง)

---

## RE-265 WHAT-OPENS-THE-CAPTAIN-DOCK-REPORT-WINDOW-001  [**CLOSED BOUNDED-NEGATIVE / STATIC ANSWERED** 2026-09-05T19:32+07:00 โดย RE runner บนเครื่อง Panya · ปิดหัวโดย chief (LANE-E) รอบ `rz1fxh`/R358 ตาม `COO-DECISION 20260905_1949` ข้อ 1 · ผลเต็ม: `notes_to_chief/20260905_1932_RE-265-RESULT-COMMON-CONFIRM-OPENS-AFTER-SAILING-RESULT-KEY.md` · **คำตอบหนึ่งบรรทัด**: `NavigationEx_AddSurveyDataVtial` ไม่ได้เปิดหน้าเอง — module tick ของ client เป็นคนเปิด `Common_Confirm` แต่มีเกตที่ GT-233 ไม่ได้ provision: record `+0x14` ต้องเป็น key ที่ lookup ตาราง `SAILING_RESULT` แล้ว**คืนแถวจริง** row ว่าง = ออกก่อนเกตระยะ (ระยะ 37 หน่วยจึงไม่พอ) → กดยืนยัน → client ยิง `EnterInstanceVital` เอง · **ปิดเป็น BOUNDED-NEGATIVE ไม่ใช่ DONE** เพราะไม่มีชั้น client-observable — ชั้นนั้นเป็นของ `GT-233` (READY-v2 ข้างล่าง) · checkpoint = **cross-layer ceiling**: ห้าม RE runner rerun image เดิมจนกว่า chief จะเปลี่ยน objective · **เจ้าของใบ/ผู้บริโภคผล = LANE-A** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A** · เนื้อใบเต็มวางโดย chief (LANE-E) รอบ `cooif2`/R357 ตาม `notes_to_chief/20260905_1638_LANE-A-RE-265-TICKET-BODY-*.md`]

> 🔴 **ทำไมต้องมีใบนี้**: `GT-233` R318 วัดเป็นลบบนจอ (`notes_to_chief/20260905_1319_KA1A-R318-RESULTS-*.md` · `OBSERVER_CONFIRMED 2026-09-05T12:48+07:00`) -- record `NavigationEx_AddSurveyDataVtial` 73 ไบต์ผ่าน parser ของไคลเอนต์แล้ว (ไม่มี `ErrorData` ทั้งรอบ) และเรือเข้าใกล้พิกัดใน record ถึง **37 หน่วย** แต่ **หน้ารายงานกัปตันไม่เด้ง** ⇒ สมมติฐานหลักของ `RE-227` ("ไคลเอนต์เช็กระยะเองแล้วเปิดหน้าเอง") ถูกหักล้างบนจอ

**สถานะ**: OPEN · **ผู้เปิดใบและผู้บริโภคผล**: LANE-A · **ผู้ตอบ**: RE runner (ข้อ ก/ข) · ข้อ (ค) LANE-A ตอบบางส่วนแล้วบนคลาวด์

**สิ่งที่ต้องไม่ทำระหว่างรอผล** (`COO-DECISION 20260905_1348` ข้อ 2/5): ห้ามบูต `GT-233` ซ้ำ · ห้ามสร้างสวิตช์ `PF_M2_SURVEY_XYZ` หรือทาง BACKUP ใด ๆ (ปิดถาวร) · ห้ามเขียนโค้ดตามสมมติฐาน (ก) หรือ (ข) ก่อนผลออก

### คำถาม -- สามข้อ ตอบแยกกันได้
**(ก) [คำถามหลัก] ในไบนารีของไคลเอนต์ อะไรสั่งเปิด UI "รายงานกัปตัน เรือเทียบท่า"** -- ไล่จาก string table → UI id → caller → เป็น handler ของ vital ตัวไหน หรือ Lua ตัวไหน ต้องการเป็นคำตอบ: ชื่อ/VA ของจุดที่เรียกเปิดหน้าต่าง + สายเรียกย้อนกลับหนึ่งชั้นว่าใครเรียกมัน

**(ข) handler `NavigationEx_AddSurveyDataVtial` เก็บ record ไว้ที่ไหน และใครอ่านต่อ** -- เร็กคอร์ด 73 ไบต์ ×8 ของเราผ่าน parser แล้วไปนอนอยู่ที่โครงสร้างไหน มีใครอ่านมันไหม หรือเขียนแล้วไม่มีผู้อ่าน

**(ค) ตารางทริกเกอร์ของฉาก 126 -- index tag `0x0F` id 2/3/7/35/48/57/69 คืออะไร** -- **LANE-A ตอบบางส่วนแล้วในรอบ `ihjytc`**: `gamedata/scene/Bg3001/Bg3001.placements.tsv` (sha256 `571c147f...c3dc9bdb8`, ตรงกับ world_scene_registry_001.json แถว 126) มี placement/definition ของ NPC/Mob_Set เท่านั้น ไม่มีคอลัมน์ตารางทริกเกอร์ · จากเจ็ด id ที่ R318 เห็น (2,3,7,35,48,57,69) มีแค่ 2 กับ 7 ที่บังเอิญตรงกับ `template_ids` ของ placement -- 3/35/48/57/69 ไม่มีอยู่เลย ⇒ **"trigger id = placement template id" ผิด**, id ที่ยิงจริงยังเป็นคนละ namespace (ยืนยัน `RE-234` ข้อ 3 ด้วยตัวเลข) · ตารางทริกเกอร์จริงต้องมาจากไฟล์ตระกูลอื่นของ `Bg3001` ที่ยังไม่ถูกสกัดเข้ารีโป -- ที่เหลือยังเป็นของ RE runner

### เกณฑ์ปิดใบ (สองชั้นตามกติกาบ้าน)
- ชั้น STATIC: ตอบ (ก) ด้วย VA/ชื่อฟังก์ชันพร้อม provenance (ไฟล์ + span_sha256) ไม่ใช่คำบรรยาย
- ชั้น client-observable: ใบ GT ที่ออกตามผล (chief ตั้งเลขทีหลัง) ทำให้หน้ารายงานกัปตันเด้งบนจอได้จริงหนึ่งครั้ง
- ปิดโดยไม่มีชั้นที่สอง = `BOUNDED-NEGATIVE` เท่านั้น ห้ามเขียน DONE

### สองสมมติฐานที่ถือเท่ากันจนกว่าใบนี้จะตอบ (`1348` ข้อ 5)
- (ก) เซิร์ฟเวอร์เดิมตอบ `0x1FB2` ด้วยเฟรมสั่งเปิดหน้ารายงาน (opcode ยังไม่รู้) -- `RE-234` พิสูจน์แค่ว่า *response ของ `TriggerVital` เอง* เป็น success no-op ห้าไบต์ ไม่ได้ปิดความเป็นไปได้ของเฟรมชนิดอื่น
- (ข) `AddSurveyData` ไม่ใช่ตัวเปิดหน้านี้เลย

### result:
**CLOSED BOUNDED-NEGATIVE 2026-09-05T19:32+07:00** -- `notes_to_chief/20260905_1932_RE-265-RESULT-COMMON-CONFIRM-OPENS-AFTER-SAILING-RESULT-KEY.md`

- (ก) ตอบแล้ว: ตัวเปิดคือ local module tick `NavigationExModule_Client` `[0x007321C0,0x00732586)` → opener `0x005AB5F0` สร้าง dialog `Common_Confirm` · callback `[0x00730FE0,0x00731083)` ต้องการ `+0x94==1` แล้วคัด record `+0x12` ลง `NavigationEx_EnterInstanceVital+0x14` — **client ยิงเอง เซิร์ฟเวอร์ห้ามส่งให้**
- (ข) ตอบแล้ว: dispatcher `0x00732590` insert ลง primary map `module+0x1C` (key = record u16 `+0x12`) → promoter `0x00731410` คัดลง secondary map `module+0x3C` → tick อ่านต่อ (`record+0x10==1`) · record มีผู้อ่านสองชั้น ไม่ใช่ "เขียนแล้วไม่มีคนอ่าน"
- (ค) **BOUNDED NEGATIVE**: `Bg3001.placements.tsv` 38 แถว ไม่มีคอลัมน์ trigger · ไม่มี scene-126 trigger crosswalk ในคลังปัจจุบัน · **ห้าม join ด้วยเลขเท่ากัน**
- **BUILD_IMPACT (LANE-A บริโภค)**: ห้าม retry เฟรมเดิมที่ใส่เพียง `record+0x12=2/3` · ต้อง derive/provision **valid SAILING_RESULT key** ที่ `record+0x14` และรักษา promoter conditions · **ห้ามเลือก row จากเลขที่เท่ากัน** (nonclaim 2 ของผล)
- **คำท้วงเชิงกระบวนการที่ chief รับ**: ใบนี้ไม่มีหัวข้อ "ค้นแล้วก่อนเปิดใบ" ตาม `AGENTS.md:98` — รอบนี้ RE runner รับไว้เพราะ `COO 1845` รับแล้ว · **ใบที่ chief วางต่อจากนี้ทุกใบต้องมีช่องนี้** (`COO 1949` ข้อ 1 · `RE-266` ข้างล่างมีแล้ว)

> 🔴 **ห้ามสายอื่นใช้เลข `RE-265`** · เนื้อใบเต็มเขียนโดย LANE-A รอบ `ihjytc` (`notes_to_chief/20260905_1638_LANE-A-RE-265-TICKET-BODY-*.md`)
> 🔴 **ห้ามบูต `GT-233` ซ้ำจนกว่าใบนี้จะตอบ** (`COO-DECISION 20260905_1348` ข้อ 1-2 · ทาง BACKUP ปิดถาวร)

- numbering: `RE-265`/`GT-265` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนจอง **[วัดแล้ว รอบก่อน]** · ตัวนับร่วมสองคิว + archive คืนสูงสุดที่ `264` (`GT-264` วางในรอบเดียวกัน) ⇒ ใบนี้ `265`

---

---

## RE-270 SAILING-RESULT-STORE-KEY-COLUMN-DERIVATION-001  [🔴 **OPEN** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A** · ตั้งเลขโดย chief (LANE-E) รอบ `6z131u`/R362 ตาม `COO-DECISION 20260905_2349` ข้อ 3 + `20260906_0147` ข้อ 3 · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_0004_LANE-A-TO-CHIEF-re-ticket-request-*` คำต่อคำ · ป้ายเส้นทางของบ้าน **[STATIC-ON-BRIDGE]** (ต้องเปิดอิมเมจ client จึงเป็นงานบนเครื่องสะพาน ไม่ใช่คลาวด์ · `CHIEF.md` §1) — LANE-A เสนอคำว่า `[NEEDS-CLIENT-IMAGE]` ใน `0004` ซึ่งไม่ใช่หนึ่งในสามป้ายที่ `pf_re_queue_taglint.py` รู้จัก chief จึงแปลงเป็นป้ายบ้านให้ ความหมายเดียวกัน · **ไม่บล็อก `GT-233` v3** (`2349` ข้อ 3 ระบุชัดว่า "ไม่เลือก (ก) เป็นเงื่อนไขบูต")]

**ทำไมต้องมีใบนี้**: `RE-265` ปิด BOUNDED-NEGATIVE โดยวัดได้ว่า record `+0x14` ถูก lookup ใน store ที่ client สร้างจากตาราง `SAILING_RESULT` จริง **แต่ไม่เคยวัดว่า store นั้นคีย์ด้วยคอลัมน์ไหน** (pf-adversary รอบ `tk4hr7` D3: `n_ID` เป็นสมมติ ไม่ใช่ค่าที่วัด) · `GT-233` v3 ใช้นัดเดียวที่มีทดสอบสองสมมติฐานพร้อมกัน (dock 153 = `n_ID` · dock 154 = `n_AREA`) — ใบนี้ตอบคำถามเดียวกันจาก disassembly แทนที่จะต้องเดาจากผลบนจอ

## ค้นแล้วก่อนเปิดใบ (`AGENTS.md` §7 grep-before-RE · LANE-A รายงานใน `0004`)
**ไม่เจอ** -- `external/PF_PROTOCOL_REGISTRY.tsv` · `external/PF_SERIALIZER_FIELDS.tsv` · `external/00_SEARCH_HERE_FIRST.md` grep `0072F700`/`0x0072F700` = 0 hit ⇒ ไม่มี layout ที่พิสูจน์แล้วบนสะพานสำหรับ VA นี้ (chief ยืนยันซ้ำรอบ `6z131u`: คำสั่งเดียวกัน 0 hit)

## คำถาม
`SAILING_RESULT` store ที่ client สร้างที่ `0x0072FE50` (`RE-265` วัดไว้) คีย์ด้วยคอลัมน์ไหนของ `CONSTDATA_TH__SAILING_RESULT.tsv` — อ่าน key จาก loop ที่ `0x0072F700` ตอนสร้าง store · ผู้สมัคร: `n_ID` (สมมติเดิม ไม่เคยวัด) · `n_AREA` (สมมติใหม่ `2349`) · composite/packed index ที่ TSV export ไม่เก็บ (ยังไม่ตัดทิ้ง)

## เกณฑ์ปิดใบ
- ปิดได้เมื่อชี้คอลัมน์ได้หนึ่งคอลัมน์พร้อม provenance (VA + `span_sha256` + บรรทัด disassembly ที่อ่าน field นั้นจริง) — หรือพิสูจน์ว่า key ไม่ได้มาจากคอลัมน์เดี่ยว (composite/packed) พร้อมสูตรที่อ่านได้
- **ผลลบเป็นผลที่ใช้ได้**: "อ่าน loop แล้วแยกไม่ออกว่าคอลัมน์ไหน" = ปิดแบบ `BOUNDED-NEGATIVE` พร้อมขอบเขตที่ค้นไปจริง
- ปิดโดยไม่มีชั้น client-observable = `BOUNDED-NEGATIVE` เท่านั้น ห้ามเขียน DONE (ชั้น client-observable ของเรื่องนี้คือ `GT-233` v3 ไม่ใช่ใบนี้)

## nonclaims ของใบนี้
ไม่ขอให้ตัดสินว่า `GT-233` v3 ควรบูตหรือไม่ (บูตได้แล้ว ไม่รอใบนี้) · ไม่ขอคำตอบว่าหน้ารายงานกัปตันเปิดด้วยอะไร (คนละคำถาม ถ้าจะถามต้องเป็นใบใหม่) · ไม่ขอให้แก้โค้ดเซิร์ฟเวอร์

ATTENDED: ใบนี้เป็น static ล้วน — **ไม่ต้องเปิดเกม ไม่ต้องจับ `LOCK_GAME` ไม่กินคิวเครื่องของผู้เทส**
ATTENDED: สิ่งที่ต้องมีบนเครื่อง = อิมเมจ client + disassembler เท่านั้น (RE runner งานปกติ) — อ่าน `0x0072F700` ถึง `0x0072FE50`
ATTENDED: ผลที่ส่งกลับ = ชื่อคอลัมน์ + VA + `span_sha256` — หรือคำว่า "อ่านแล้วแยกไม่ออก" พร้อมเขตที่ค้น

### result:
(ว่าง)

> 🔴 **ห้ามสายอื่นใช้เลข `RE-270`** · numbering: คำสั่งนับเลขของบ้าน (`grep -ohE '\b(GT|RE)-[0-9]{3}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md archive/*QUEUE*ARCHIVE*.md | ... | tail -1`) คืน **267** รอบ `6z131u` ⇒ เลขว่างตัวแรกคือ 268 **แต่ chief ข้ามไป 270** โดยเจตนา: `GT-268` (LANE-A ฉาก 304 census) และ `GT-269` (LANE-GM P-3 GMUI) ถูกประกาศเป็นของสองสายนั้นไปแล้วในจดหมาย `FROM_CHIEF_R361_TO_ALL_20260906_0040.md` (เนื้อใบยังไม่ลงไฟล์ จึงยังไม่นับในคำสั่งข้อ ②) — การหยิบ 268/269 มาใช้จะชนกับสองสายที่กำลังเขียนเนื้อใบอยู่
> 🔵 ตัวนับร่วมกับ `GAME_TEST_QUEUE.md` · ใบนี้ไม่จองเลขล่วงหน้า — เนื้อใบมาครบก่อนลงไฟล์ตามข้อ ① ของกติกาไฟล์นี้

## RE-266 0X709E-DOWNSTREAM-AND-GETWORLDINFO-REPLY-WAIT-001  [🔴 **OPEN** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · ตั้งเลขโดย chief (LANE-E) รอบ `rz1fxh`/R358 ตาม `COO-DECISION 20260905_1845` ข้อ 4 · เนื้อใบเต็มเขียนโดย LANE-UI รอบ `4j99rh` (`notes_to_chief/20260905_1405_LANE-UI-RE-TICKET-0x709E-handler-gate-already-answered-by-re075-real-gap-is-getworldinfo-wait.md`) · ป้ายชั้น: **ข้อ 1 = `[STATIC-ON-BRIDGE]`** (artifact ที่ commit แล้ว) · **ข้อ 2 = `[STATIC-ON-BRIDGE]` และมีแนวโน้มสูงที่จะจบด้วย `[NEEDS-CLIENT-IMAGE]`** · **ตัวบล็อกของ `GT-184`/`GT-186`** (ทั้งสองใบพลิกเป็น `BLOCKED-ON-RE-266` รอบเดียวกัน)]

**ทำไมต้องมีใบนี้**: `COO-DECISION 20260905_1352` ข้อ 3 สั่งใบ RE แคบใบเดียวสองคำถาม หลัง R311+R319 วัดเป็นลบบนจอ (HYP-PF-040 FALSIFIED) · LANE-UI ค้นก่อนแล้วพบว่าคำถาม (ก) ของ `1352` **ถูกตอบไปแล้วโดย `RE-075`** ใบนี้จึงเหลือเฉพาะปลายที่ `RE-075` ไม่ได้เดิน กับคำถาม (ข) ที่ยังไม่มีใครตอบเลย

## ค้นแล้วก่อนเปิดใบ (`AGENTS.md` §98 · `RE_STATIC_SEARCH_RULES.md`)
**เจอ** -- `RE-075` (DONE/PASS 2026-08-26, `archive/notes_to_chief_2026-08-19_to_26/20260825_2318_RE-075-RESULT-FALSE-BRANCH-NOOP-ZERO-FIELD-GATE.md`) ปิดเกตสองชั้นของ `0x709E` ครบ: ชั้น 1 `apply 0x005F1190` อ่าน live-state `[0x1093198]+0x34C` เช็ก `cStateCreateActor` ไม่ตรง = `mov al,1; ret 4` ทันที · ชั้น 2 `0x004B2A50` ต้องการ `vital+0x14 == 0x1E` · `RE-196`/`RE-197`/`RE-189` CLOSED · `VITAL_REGISTRY...tsv:191`, `external/PF_PROTOCOL_REGISTRY.tsv:73`, `PF_SERIALIZER_FIELDS.tsv:1123-1128`, `PF_FIELD_VALIDATION.tsv:144-145` · `PF_TAG_CENSUS.tsv` = 0 hit
**ไม่เจอ** -- ไม่มีรายงาน static ใดเดิน downstream ของ true-branch (`0x4B04A0`/`0x5DD890` ที่ `RE-075` T3 ทิ้งค้าง) · ไม่มีใบใดปิดคำถาม (ข) ของ `1352` · `serializer_status` ของ `0x3D4B` ใน `PF_PROTOCOL_PRIORITY.tsv:67` = **OPEN**

## คำถาม -- สองข้อ เรียงลำดับบังคับ
1. **downstream ของเกตที่ `RE-075` เปิดค้างไว้** -- ตาม call ไป `0x4B04A0`/`0x5DD890` (true-branch ของเกตทั้งสองชั้น): เขียน/เรียกอะไรที่แตะ UI/state transition จริงหรือไม่ — เป้าหมายคือรู้ว่า **ถ้าส่ง `0x709E` ที่ state ถูก + `+0x14=0x1E` จริง** จะพาไปหน้าเลือกตัวละครได้หรือไม่ในทางทฤษฎี ก่อนจะจ่ายเวลา attended รอบใหม่
2. **`0x3D4B` (`GetWorldInfoVital`) ฝั่ง R** -- ไล่ `CALL_UNCLASSIFIED:0x005DFD00` และ `0x00708E20` เท่าที่ artifact ที่ commit แล้วพาไปได้: มี pending-reply flag/state ที่ gate การเปิด dialog ต่อไปหรือไม่ · **ไล่ต่อไม่ได้เพราะต้องใช้ disassembly ที่ไม่ได้ commit ⇒ แปะป้าย `[NEEDS-CLIENT-IMAGE]` ตรงจุดนั้น ห้ามเดา**
3. ใบนี้ **ไม่ขอให้ตอบคำถาม (ก) ของ `1352` ซ้ำ** — `RE-075` ตอบครบทั้งสองเกตแล้ว

## เกณฑ์ปิดใบ (ชั้น static เท่านั้น)
- ข้อ 1 ปิดได้เมื่อ: ไล่ downstream สำเร็จพร้อม provenance (`path:บรรทัด`/VA + `span_sha256`) **หรือ** สรุปว่าต้องมีไบนารีไคลเอนต์ถึงไล่ต่อได้ (`[NEEDS-CLIENT-IMAGE]`) -- ทั้งสองแบบถือว่าปิด
- ข้อ 2 ปิดได้แบบเดียวกัน · **ผลลบ/ผลไม่คืบก็เป็นผลที่ใช้ได้** (`RE-189` ธงไว้แล้วว่ามีแนวโน้มจบด้วย "ต้อง attended")
- ปิดโดยไม่มีชั้น client-observable = `BOUNDED-NEGATIVE` เท่านั้น ห้ามเขียน DONE
- 🔴 **ชั้น client-observable ไม่อยู่ในใบนี้** — ถ้าผลชี้ว่าต้อง attended ถึงจะปิดคำถาม (ข) ได้ **LANE-UI ต้องเปิดใบ GT คู่ในรอบเดียวกันที่บริโภคผล** (`AGENTS.md` §7 · `COO-DECISION 20260904_2142` ข้อ 3 · ขอเลขจาก chief)

## ใบนี้ไม่ขอ
ไม่ขอให้เดาว่า `0x709E` เป็น vital ที่ถูกสำหรับปุ่มนี้หรือไม่ (`RE-075` nonclaim 4) · ไม่ขอให้บูตซ้ำ (`1352` ข้อ 2) · ไม่ขอให้ลองลำดับ "ส่งหลัง ACK" (เป็นการเดาลำดับ ไม่ใช่ผลวัด)

### result:
(ว่าง)

> 🔴 **ห้ามสายอื่นใช้เลข `RE-266`** · numbering: `RE-266` = 0 hit ทั้งสามที่ (`CLIENT_RE_QUEUE.md` · `GAME_TEST_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนตั้ง **[วัดแล้ว รอบ `rz1fxh`/R358]** · ใบนี้มีหัวข้อ "ค้นแล้วก่อนเปิดใบ" ตาม `AGENTS.md` §98 ตามที่ RE runner ท้วงใน `1932`
