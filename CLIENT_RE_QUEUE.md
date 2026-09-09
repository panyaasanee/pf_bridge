# CLIENT RE QUEUE — คิวงานแกะไคลเอนต์/capture (static · ไม่เปิดเกม)

> 🔴 **นิยามคำว่า "result" — สองงานคนละงาน ห้ามสับสน** (`COO-DECISION 20260907_1541` ถึง LANE-K ข้อ 1 · วางไว้ที่หัวไฟล์เพราะคำถามนี้ถูกถาม **สามครั้งใน 24 ชม.**)
> - **พับ (fold) = LANE-K**: คัดลอกคำตอบ/`BUILD_IMPACT`/nonclaims จากจดหมายผลลงหัวใบ + พลิกสถานะ + วางสตับ `.LANEK-FOLDED.txt` — **เป็นงานเสมียน ไม่ตัดสิน** · คำที่ใส่ต้องเป็น**คำของผู้เทส/เจ้าของใบ** ไม่ใช่คำของ K · ผลสองชั้นไม่ครบ = `🟡 <ชั้นที่ครบ> · <ชั้นที่ขาด> NOT MEASURED` ห้ามปั๊ม PASS
> - **บริโภค (consume) = สายเจ้าของใบ**: เอาผลไปแก้โค้ด / ออกใบสร้าง / เขียน `NO_FEATURE_WAITING:` แล้ววางสตับ `.CONSUMED.txt` — **K ห้ามทำแทนเด็ดขาด**
> ⇒ ประโยคใน `prompts/COMMON_LANE_ROUND.md` ("ใครเปิดใบ คนนั้นบริโภคผล") กับ `NOW.md` `PANYA 1910` ("พับผล = LANE-K") **ไม่ขัดกัน** — คำเดียวกันใช้กับสองงาน · สายเจ้าของใบ **ไม่ต้องแตะไฟล์คิวนี้เอง** เพื่อพับผลของตัวเอง ส่งจดหมายถึง K แล้วบริโภคต่อได้เลย
>
> 🅿️ **`RESERVED` = เลขที่จองแล้วแต่ยังไม่มีเนื้อใบ** (`COO-DECISION 20260907_1541` ข้อ 2 · "ยืนเป็นแบบแผน")
> - แถว `RESERVED` **ห้ามขึ้น `READY`** และ **ห้ามเข้า `QUEUE_STATUS_SNAPSHOT.md`** — ka1-A ต้องไม่มีทางหยิบใบเปล่าขึ้นรถบัส
> - **K ห้ามเขียนโครงเนื้อใบแทนเจ้าของ** (เจ้าของจะกลายเป็นคนเซ็นของที่ตัวเองไม่ได้เขียน) · เนื้อใบมาทางจดหมาย `*-TO-K-gt-body-*` / `*-TO-K-re-body-*` **คำต่อคำ**
> - กำหนดเวลา: เนื้อใบต้องมาภายใน **สองรอบของสายเจ้าของ** · ไม่มา ⇒ K ขึ้นแถวในสแนปช็อตหมวด **ช.** พร้อมชื่อสายและอายุ — **K ขึ้นบัญชีอย่างเดียว ไม่ทวงเอง** (COO ทวง)

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

**[วัดแล้ว]** `gamedata/tables/TEXTDATA_TH__SCENE_NAME_TIP.tsv` (330 แถวข้อมูล · 331 บรรทัดรวมหัว ตรงกับ `PF_GAMEDATA_INDEX.tsv:146` — แก้เลขตาม `notes_to_chief/20260906_1939_LANE-A-R322A-CONSUMED-re234-refutes-0x1FB2-reply-bg3001-tgr-is-the-door.md` ข้อ 5.2 · คอลัมน์ `n_ID`/`s_SCENE_NAME`/`s_GM_SCENE_NAME`) ให้ชื่อฉาก GM-facing ครบ — Port Royal=1 · Prison Exile Island=2 · Spice Paradise Island=3 · Slave Market Island=4 · Evil Port=5 · Ocean Walled City=6 · Voodoo Island=7 · Silver Harbour=8 · Death City Sea=9 · "Ship in the Sea" (สถานะเรือ ไม่ใช่เกาะจอด) = id 17-23 · "Ship in the Sky" = id 24-30 (มีชุด reskin/mission ซ้ำที่ id 62-73, 186-215, 229) · เกาะ "faction" อีก 13 ใบที่ id 254-270 · เกาะกระจาย/procedural อีกหลายสิบ id (31-61, 74-111, 147-185, 193-253)

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
## 🆕🔬 RE-122 PLAYER-STANDARD-STATUS-AND-CHARCREATE-SCORE-VALUES-001 [STATIC-ON-BRIDGE] [🟢 **DONE / BOUNDED-NEGATIVE (static-only)** — คำต่อคำจากหัวข้อ... -- archived 20260907 (DONE / BOUNDED-NEGATIVE (static-only); verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)
## 🆕🔬 RE-123 BG0002-MIRAGE-REEL-QUEST-SPAWN-CROSSWALK-001 [STATIC-ON-BRIDGE]: **NPC "Mirage reel" ที่หน้าต่างแผนที่เกาะคุกของเจ้าของแสดงไว้ (ยืนหน้าเต็นท์ Mo Yuzi) มี n_ID ไหน และมันมาจากไฟล์ placemen... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## RE-125 PICKUP-REQUEST-VITAL-ID-001: what wire vital id (opcode) does a real client send when the player left-clicks a ground drop / `PickupTerrainT... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## RE-126 BT-GM-CONTROL-OBJECT-IDENTITY-001: ปุ่ม `BT_GM` ที่ RE-104 พินไว้ ถูกผูกกับ handler `0x0053B9B0` จริงหรือกับ dispatcher ตัวอื่น -- และ `this+0x48` (ประตูบานแรกของ handler) ถูกตั้งค่าจากที่ไห... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-128 SCENE-ORDINAL-TO-MOBS-NID-TABLE-LOCATION-001 [STATIC-ON-BRIDGE] [🟢 **PASS/DONE — DIRECT+INSTANCE CLINE SELECTORS PINNED** — คำต่อคำจากบรร... -- archived 20260907 (PASS/DONE; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)
## RE-129 FORCE-POS-VITAL-VERSION-001: ไบต์ `vital_version` ของ `ForcePos` (`0x0E80`) ที่ client ยอมรับคือค่าอะไร -- prototype constructor ของ vital น... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## ✅🔬 RE-130 GROUND-LABEL-LIST-MEMBERSHIP-001 [STATIC-ON-BRIDGE] — **CLOSED / DONE-PASS · บริโภคแล้วโดย LANE-B รอบ `zxnwtd`**: **ป้ายชื่อไอเทมบนพื้นผูกกับการที่ element ยังอยู่ในลิสต์ `0x08` (object+`... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## RE-132 GM-GLOBAL-MESSAGE-VITAL-VERSION-001 [ARCHIVED 2026-08-31 R274, closed >24h per หัวข้อ 11] -- moved verbatim to `archive/CLIENT_RE_QUEUE_ARCH... -- (stub เก่า R274) ถูกย้ายรอบ 20260906 ไป `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md` 🔴 **แต่เนื้อใบจริงอยู่ที่ `archive/CLIENT_RE_QUEUE_ARCHIVE_20260831_R274_closed.md` ไม่ใช่ไฟล์ 20260906** (ไฟล์นั้นเก็บได้แค่ stub นี้ — แก้ถ้อยคำที่ชี้ผิดโดย chief รอบ `6z131u`-b ตาม pf-adversary D12)

## 🆕🔬 RE-135 CP874-CENSUS-ARTIFACT-REGEN-001 [STATIC-ON-BRIDGE]: ลบ `U+1F534` ตัวสุดท้ายใน `tools/pf_vital_thunk_census_static.py` แล้ว regenerate artifact ในคอมมิตเดียวกัน  [🔴 **BLOCKED (ไม่ใช่ time checkpoint, ไม่ใช่ method ceiling) — ติดที่สิทธิ์เขียน/คอมมิต ไม่ใช่ที่ความรู้** · คำต่อคำจากจดหมาย `notes_to_chief/20260907_0338_RE-135-RESULT-BLOCKED-ON-COMMIT-RIGHTS-artifact-is-one-line-stale-and-the-guard-is-red-now.md` (2026-09-07T03:38+07:00) · พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 · เดิม `[PENDING]`]

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

### result: (พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 คำต่อคำจากจดหมาย
`notes_to_chief/20260907_0338_RE-135-RESULT-BLOCKED-ON-COMMIT-RIGHTS-artifact-is-one-line-stale-and-the-guard-is-red-now.md`
— สถานะที่จดหมายเขียนเอง: **BLOCKED (ไม่ใช่ time checkpoint, ไม่ใช่ method ceiling) — ติดที่สิทธิ์เขียน/คอมมิต ไม่ใช่ที่ความรู้**)

สรุปคำต่อคำจากจดหมาย: ขั้นที่ 1 และ 3 ของใบ **ทำไปแล้ว** (คอมมิต `51da9f53`) แต่ **ขั้นที่ 2
(regenerate artifact) ไม่เคยเกิดขึ้น** ⇒ `tools/pf_vital_thunk_census_static.py` **FAIL อยู่ ณ ตอนนี้**
และ `tests/test_tree_is_cp874_safe.py` ที่รันเครื่องมือนี้ก็จะแดงตาม — ตรงกับที่ใบเตือนไว้เองเป๊ะ
· ส่วนต่างจริง = **2 บรรทัด (สตริงเดียว)** `🔴 THIS IS NOT A NAME TABLE.` → `!! THIS IS NOT A NAME TABLE.`
· ไฟล์ที่ derive ได้ 71,645 ไบต์ sha256 `05fab2964211c55be5a14e114a341b16c20fc4620201397cec0ab4261761c6ec`
· จดหมายระบุ BUILD_IMPACT: **"มี และเป็นของแดงอยู่ตอนนี้"** บน main ปัจจุบัน
· ข้อเสนอในจดหมาย (ยกมา ไม่ตัดสิน): **"ควรย้ายผู้รับผิดชอบไปเลนที่ push ได้ (LANE-A/K) หรือปิดใบแล้วเปิดใหม่ในรูปงานคอมมิต"**

🔴 **หมายเหตุจาก LANE-K (ไม่ใช่การตัดสิน)**: ใบนี้จ่าหน้า `ADDRESSEE: chief` และคำขอย้ายผู้รับผิดชอบ
เป็นเรื่องของ COO/chief — เสมียนพับสถานะให้เท่านั้น ไม่ได้รับใบมาทำเอง · แจ้ง COO ในจดหมายรอบ `dmef5j`

## 🆕🔴 RE-136 MOBS-ANSWER-AS-NPC-DISPATCH-001 [STATIC-ON-CLOUD]: คลิกซ้ายบน hostile roster placement ถูกเซิร์ฟเวอร์ตอบด้วย **เลนคุย NPC** แทนเลนต่อสู้... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🆕🔬 RE-137 NPCCONVERSATION-54B-WHOSE-SCRIPT-001 [STATIC-ON-CLOUD]: เฟรม 54 ไบต์ที่ `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` ส่ง -- de... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-138 NAME-LABELS-VANISH-AFTER-MOVE-001 [STATIC-ON-CLOUD]: ป้ายชื่อ (เขียว) ของทุกตัวในแมพหายหลังผู้เล่นเดินออกจากบริเวณแรก เหลือแต่ป้ายฉายา (ฟ้... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-139 P33-P58-IDENTITY-CONTRADICTION-001 [STATIC-ON-CLOUD]: บูตเดียวส่ง **ตัวตนสองชุดที่ขัดกัน** ให้ placement เดียวกัน -- สำมะโนบอกว่า Babu/Juliet ตาราง roster บอกว่า Fighting Fish soldier/Jung... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-149 PORT-ROYAL-FIVE-COSTUMELESS-LEADERS-001 [STATIC-ON-BRIDGE]: ห้าตัวที่ Port Royal "แต่งตัวให้ไม่ได้" -- ไคลเอนต์เอา `s_OUTFIT` ของ CLINE leader `155 / 819 / 937 / 942 / 9107` มาจากไหน หรือม... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-150 AGGRO-PLACEMENT-OUTSIDE-REFUSED-BLOCKS-001 [STATIC-ON-BRIDGE]: หา placement ที่ AI เริ่มตีเอง (aggro) นอกบล็อก 101-104 ที่เจ้าของสั่งห้ามวาง -- จาก artifact ที่ commit แล้วเท่านั้น  [✅ DO... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-152 PORT-ROYAL-HARBOUR-NEEDS-A-SOURCE-001 [STATIC-ON-BRIDGE]: ท่าเรือของ Port Royal (`placement 0` / CLINE leader `155` "Port transportation") ต้องมาจากไหน -- ในเมื่อ `RE-149` ปิดทางเดิมไปแล้ว... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-154 CHOOSENPC-ANSWERS-FOR-UNANNOUNCED-ACTORS-001 [STATIC-ON-BRIDGE]: **ตัวตอบ `ChooseNPC` ตอบคลิกให้ identity ฮาร์ดโค้ดโดยไม่ตรวจฉาก และไม่ตรวจว่า actor นั้นเคยถูกประกาศให้ไคลเอนต์หรือยัง** [... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🔬 RE-155 ACTOR-NAME-COLOR-NPC-VS-HOSTILE-MOB-ONE-FIELD-CROSSWALK-001 [NEEDS-ATTENDED-CAPTURE]: เจ้าของสั่ง "NPC เขียว→เหลือง" + "Training Iron Man ควรชื่อแดง" -- static ชนเพดานเรื่องนี้แล้วสามใบ ต้องมี capture เปลี่ยนทีละฟิลด์จึงตอบต่อได้  [🟡 **ตอบแล้วโดย LANE-B รอบ `dipufa` 2026-09-07T00:21+07:00** (`notes_to_chief/20260907_0021_LANE-B-TO-K-gt-body-RE-155-dummy-row-npc-and-916-sweep.md`) — สปาวน์เนอร์ `name_colour_sweep.py` + ผู้สมัครตัดฟิลด์ (faction/actor_type/skin ทดสอบได้ · relation +0x98/rank ยังไม่ตัดตั้งใจ) → ใบทดสอบ **`GT-288`** NAME-COLOUR-SWEEP-DUMMY-ROW-001 ตั้งเลขโดย LANE-K รอบ `6rj6h1` 2026-09-07T01:09+07:00 (เนื้อเต็มที่ `tickets/GT-288.md`) — GT-288 ยัง `[PENDING]` รอ CORE-REQUEST ต่อสาย env→dispatch จาก B ก่อนบูตขึ้นจริง (ตามที่จดหมาย B เขียนไว้เอง) · ~~เดิม: 🟢 OPEN — เปิดโดย LANE-A รอบตรวจ 20260830 จากคำสั่งเจ้าของ GT-131 หมวด ③~~] [🟢 **ANSWERED — พับโดย LANE-K รอบ `mb9vtg` 2026-09-08T19:22+07:00** คำต่อคำจากบรรทัด `RESULT:` ท้ายจดหมาย `notes_to_chief/20260908_1315_KA1A-R324A-RESULTS-GT288-set3-ALL-PASS-colour-is-identity-sign-enemy-offensive.md` (ka1-A attended R324A 2026-09-08 13:05): "RE-155 ANSWERED R324A 2026-09-08 13:05 (both halves in one boot: NPC yellow and mob orange/red · the owner's colour table is reachable with the fields we already send)" · K คัดลอกคำของผู้ทำ ไม่ได้ตัดสินเอง · ดูตารางเต็มของ `GT-288` ชุด 3 ใน `tickets/GT-288.md`]

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
## 🔬 RE-208 GROUND-POOL-REMOVAL-PATH-FOR-THE-LAST-OBJECT-001 [🟡 **RESULT ส่งแล้ว 2026-09-03 · จดหมายไม่เขียนสถานะปิดใบ — รอ LANE-B (เจ้าของผล) เคาะ**  · จดหมาย `notes_to_chief/20260903_0300_RE-208-RESULT-there-is-no-remove-by-key-message-the-pool-shape-is-the-only-selector.md` · พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 · เดิม OPEN -- เปิดโดย LANE-B รอบ `9jrsei` 2026-09-02T09:5x+07:00 · ผู้ทำ: **สาย RE** (ผู้ทำสายเดียว ไม่ต้องจอง) · **LANE-B บริโภคผลเอง** · `STATIC-ON-CLOUD`]

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

### result: (พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 คำต่อคำจากจดหมาย
`notes_to_chief/20260903_0300_RE-208-RESULT-there-is-no-remove-by-key-message-the-pool-shape-is-the-only-selector.md`
— สถานะที่จดหมายเขียนเอง: **จดหมายไม่มีบรรทัด `RESULT:` และไม่มีหัวข้อ "สถานะที่เสนอ" — LANE-K ไม่ตั้งสถานะให้เอง**)

คำตอบของใบยกคำต่อคำจากจดหมาย:
- **LAYER 1 — คำถามเดียวของใบ: "NO. There is no remove-by-key / destroy-one path reachable from a distinct message."**
- **LAYER 2 — "can a non-empty generation carrying one dummy row retire a real object?" "NO, and it is worse than useless."**
- วิธีทำ: **ไม่ได้ดิสแอสเซมบลีใหม่** — ตามกฎข้อ 4 ของไฟล์นี้ ค้น `pf_bridge\external\` ก่อน **เจอ** ⇒ ใบกลายเป็น
  "verify sha → adversarial re-derive → use" · ผู้ทำ: **ka1-A (attended)** ตามคำสั่งเจ้าของโดยตรง 2026-09-03 ~02:5x-03:00
- NONCLAIM ที่จดหมายเน้นเอง: *"An adversarial re-derive of the reconcile spans was NOT performed."*

🔴 **ทำไมหัวใบเป็น 🟡 ไม่ใช่ CLOSED**: กติกาเหล็กข้อ 1 ของสาย K = "พับ = คัดลอก ไม่ใช่ตัดสิน" ·
จดหมายตอบคำถามทั้งสองชั้นแล้วแต่ **ไม่ได้เขียนสถานะปิดใบ** ⇒ ต้องให้ **LANE-B (ผู้บริโภคผลตามหัวใบ)**
ตอบกลับหนึ่งบรรทัดว่าปิดหรือไม่ปิด · จดหมายฉบับนี้ค้างพับมาตั้งแต่ **2026-09-03** (ดูจดหมายรอบ `dmef5j`)

## 🔬 RE-209 QUEST-SETTER-PROLOGUE-11-BYTES-ESI-PROVENANCE-001 [✅ **DONE / POSITIVE (bounded) — พับผลโดย LANE-K รอบ `x91eo8` 2026-09-06T18:2x+07:00** จ... -- archived 20260907 (DONE / POSITIVE (bounded); verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)
## 🔬 RE-210 EXIT-BUTTON-ONLAND-RESPONSE-EXPECTATION-001 [**CLOSED / PASS** -- ตอบแล้ว 2026-09-02T15:03+07:00 · บริโภคโดย LANE-A รอบ `gwwpmr` 2026-09-02T15:35+07:00 · เปิดโดย LANE-A รอบ `1d6rta` · ผู้ท... -- archived 20260905 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260905_closed.md`)
## 🔬 RE-222 NONPOSITIVE-IDENTITY-TYPED-AND-LIVE-GATE-REACHABILITY-001 [✅ **DONE/PASS — Q0–Q3 closed; the selector-local list population path was resolved in the continuation pass** (คำของผู้ทำคำต่อคำ บรรทัด `- Status:` ของ `notes_to_chief/20260903_2149_RE-222-RESULT-PARTIAL-updateattr-and-name-color-gates.md` 2026-09-03T21:49+07:00 · พับโดย LANE-K รอบ `wb8tfv` 2026-09-07T11:10+07:00 — **K คัดลอก ไม่ได้ตัดสิน**) · 🟡 **ชั้นที่ครบ: static (ไบนารีไคลเอนต์ + registry) · ชั้นที่ขาด: client-observable NOT MEASURED** (จดหมายเขียนเอง: *"Static only. No game/server boot"*) · 🔴 **ชื่อไฟล์จดหมายเขียนว่า `PARTIAL` แต่บรรทัดสถานะข้างในเขียน `DONE/PASS` — K ยึดบรรทัดสถานะตามกติกา "พับ = คัดลอกคำที่ผู้ทำเขียนไว้" และแจ้งความต่างนี้ไว้ตรงนี้ ไม่ตัดสินว่าอันไหนถูก** · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ · ถอนแล้วโดยเจตนา): ~~OPEN~~ -- ร่างโดย LANE-GM รอบ `5ddsii` (ใบ `notes_to_chief/20260903_1119_LANE-GM-RE-211-TICKET-*.md`) ตามข้อยกเว้นใบเดียวของ `COO-DECISION 20260903_1046` ข้อ (ข) · **วางคิวและมอบหมายโดย chief รอบ `kjtpza` (R319) 2026-09-03T13:0x+07:00** · ผู้ทำ: **สาย RE** (ผู้ทำสายเดียว ไม่ต้องจอง) · **LANE-GM บริโภคผลเอง** · 🔴 `[STATIC-ON-BRIDGE]` ต้องดิสแอสเซมบลีอิมเมจ ⇒ ทำบนคลาวด์ไม่ได้]

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


## 🔬 RE-227 CAPTAIN-REPORT-ON-ISLAND-CONTACT-001 [🔴 **primary hypothesis REFUTED-ON-SCREEN (R318 `1319`) · covered by `RE-265`** — แก้หัวใบโดย LANE-A ... -- archived 20260907 (REFUTED-ON-SCREEN, covered by RE-265; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)
## 🔬 RE-227 CAPTAIN-REPORT-ON-ISLAND-CONTACT-001 [⚫ **SUPERSEDED-BY: ก้อน `REFUTED-ON-SCREEN` ด้านบน -- ไม่ใช่ใบเปิด อย่าหยิบไปรัน** · ยุบโดย LANE-A (... -- archived 20260907 (SUPERSEDED-BY the REFUTED-ON-SCREEN block; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)
## 🔬 RE-229 CHARCREATE-CLASS-SSCORE-STARTING-STATS-SOURCE-001 [🟢 **CLOSED BOUNDED-NEGATIVE/DONE — RE runner local 2026-09-04T10:50+07:00, ปิดหัวใบโดย... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-232 SCAST-CONDITION-BEHAVIOR-TOKEN-GRAMMAR-001 [~~OPEN -- 🔴 `[STATIC-ON-BRIDGE]`~~ 🔵 **DONE / BOUNDED-NEGATIVE — ปิดโดย LANE-CS รอบ `tp9rpy` 2... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-234 CLIENT-RESPONSE-PATH-FOR-TRIGGERVITAL-1FB2-ISLAND-001 [🔵 **DONE / MIXED PASS + BOUNDED-NEGATIVE — ปิดโดย LANE-A รอบ `2mnd7b` 2026-09-05T12... -- archived 20260907 (DONE / MIXED PASS + BOUNDED-NEGATIVE; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)
## 🔬 RE-234 CLIENT-RESPONSE-PATH-FOR-TRIGGERVITAL-1FB2-ISLAND-001  [⚫ **SUPERSEDED-BY: ก้อน `DONE / MIXED` ด้านบน -- ไม่ใช่ใบเปิด อย่าหยิบไปรัน** · ยุ... -- archived 20260907 (SUPERSEDED-BY the DONE / MIXED block; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)
## 🔬 RE-235 BLACK-MARKET-AND-SHIP-SURVEY-WINDOW-OPCODES-001  [🔧 LANE-K แก้ `slug54r2` — คำ "CAPTURED" เดิมไม่ใช่คำในจดหมาย (adversary): จดหมายเขียน **"ได้ 1 เฟรมใหม่"** (0x310C sub=0x09) — R320 §RE-235/261 · 4 ฟีเจอร์ยัง NOT REACHED · จาก notes_to_chief/20260906_0155_KA1A-R320-*.md · OPEN -- 🔴 `[NEEDS-ATTENDED-CAPTURE]` · เจ้าของใบ/ผู้เขียนเนื้อใบ = **LANE-UI** · ผู้บริโภคผล = LANE-UI]

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

## 🔬 RE-236 TRACEPATH-RECORD0-SEMANTIC-ATTENDED-DIFFERENTIAL-001  [🟢 ANSWERED (ทั้งสองข้อปิดแล้ว) — ข้อ (ก) มินิแมป ปิดแล้ว (REFUTED ผ่าน `GT-246`/R310) · ข้อ (ข) ปิดรอบ `9xqzh0` 2026-09-05T12:2x+07:00 ผ่าน `GT-251`/R317 (ดูข้อ (ข) ข้างล่าง) · เจ้าของใบ/ผู้เขียนเนื้อใบ = **LANE-UI** · ผู้บริโภคผล = LANE-UI] -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)

## 🔬 RE-237 OPTIONS-APPLY-SERVER-SETTING-VITAL-FIELDS-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — CAPTURED hex ครบ — R320 2026-09-06 §RE-237:... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)
## 🔬 RE-238 SELECTOR-CATEGORY-TO-ALT-HP-PAIR-MAPPING-001  [✅ **PASS/DONE — SCENE_NAME.n_SCENE_TYPE=8 keys 126/127/128/304/305 pinned** · คำต่อคำจากจดห... -- archived 20260907 (PASS/DONE; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)

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

## 🔬 RE-248 SELECTACTOR-0x5DFF60-TWO-U16-TAG-0x12-WHICH-IS-SCENE-001  [🔧 **PASS/DONE — พับโดย LANE-K รอบ `ek1gk9` 2026-09-07T09:5x+07:00** คำต่อคำจากห... -- archived 20260907 (PASS/DONE; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)
## 🔬 RE-256 ADDSURVEYDATA-OUTER-PRESENCE-BYTE-VALUE-001  [✅ **DONE -- ตอบแล้ว 2026-09-05 10:07 +07:00** · ปิดหัวโดย chief (LANE-E) รอบ `pv4zg1`/R352 ต... -- archived 20260907 (DONE; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)

<!-- LANE-K round kq7m3d addendum 2026-09-07T18:5x+07:00: the six lines below were carried into archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md by mistake when the RE-256 move over-ran its block; restored here byte-identical to 87267dd:989-994. They are the pointer stubs for RE-259 and RE-260, archived in round spppsd. -->
---

- ~~RE-259 UPDATEATTRVITAL-0X309A-IS-IT-EVER-SENT-FOR-CNETNPC-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (PASS -- LANE-DB ปิดแล้ว 2026-09-05, ดู pf_bridge/notes_to_chief/202609 ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

- ~~RE-260 ACTORATTR-0X99-0X9A-CONCRETE-OWNER-CLASS-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (DONE -- LANE-DB ปิดแล้ว 2026-09-05, ดู pf_bridge/notes_to_chief/202609 ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

## RE-261 STALL-AND-GUILD-STORAGE-FIELD-SEMANTICS-FROM-A-REAL-SESSION-001  [🔧 LANE-K แก้ผล `slug54r2` — แก้คำ "CAPTURED" ที่เติมเองรอบก่อน (adversary จับได้): จดหมายเขียนว่า **"ได้ 1 เฟรมใหม่"** (ร่วมกับ RE-235) — R320 §RE-235/261 · GT คู่ = GT-262 · จาก notes_to_chief/20260906_0155_KA1A-R320-*.md · OPEN -- 🔺 `[NEEDS-ATTENDED-CAPTURE]` (จดหมายต้นทางระบุเองว่า **ปิดจาก static เดี่ยวไม่ได้**) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · ใบ GT คู่ของมัน = **`GT-262` (chief จองเลขไว้แล้วรอบ `pv4zg1`/R352 · LANE-UI เป็นผู้เขียนเนื้อใบ GT ในรอบถัดไป)** ตาม `AGENTS.md` §7 (`COO-DECISION 20260904_2142` ข้อ 3) -- **ผู้เทสอ่าน `GAME_TEST_QUEUE.md` เท่านั้น ไม่เคยอ่านไฟล์นี้** ถ้าไม่มีใบ GT จะไม่มีใครเห็นใบนี้ตลอดกาล] -- moved to `tickets/RE-261.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `x91eo8` 2026-09-06T18:10+07:00)
## RE-263 PAIR-RELATION-ZERO-GATE-REACHABILITY-AND-DEFAULT-BIT-001  [**CLOSED BOUNDED-NEGATIVE** 2026-09-05T13:12+07:00 โดย LANE-GM รอบ `0dlc07` (ผู้ท... -- archived 20260907 (CLOSED BOUNDED-NEGATIVE; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)

- ~~RE-265 WHAT-OPENS-THE-CAPTAIN-DOCK-REPORT-WINDOW-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (**CLOSED BOUNDED-NEGATIVE / STATIC ANSWERED** 2026-09-05T19:32+07:00 โ ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

## RE-270 SAILING-RESULT-STORE-KEY-COLUMN-DERIVATION-001  [✅ **CLOSED / BOUNDED-POSITIVE (static answered)** · คำต่อคำจากจดหมาย `notes_to_chief/202609... -- archived 20260907 (CLOSED / BOUNDED-POSITIVE (static answered); verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)

- ~~RE-266 0X709E-DOWNSTREAM-AND-GETWORLDINFO-REPLY-WAIT-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (🔧 **BOUNDED-NEGATIVE / STATIC ANSWERED — พับโดย LANE-K รอบ `ek1gk9` 20 ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

## RE-272 ITEMOPERATEVITALREQ-EQUIP-FROM-BAG-RESPONSE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — CAPTURED (ครบ 3 ซ้ำ payload เหมือนกัน op=5 value=8 identity=0x4) — R321... -- archived 20260906 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260906_closed.md`)
## RE-273 TRIGGER-ID-TO-LUA-SCRIPT-FILE-MAPPING-001  [🔧 **PARTIAL (เส้นทาง 1 ตอบแล้ว / เส้นทาง 2 ยังไม่ต้องเดิน) — พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00** คำต่อคำจากหัวข้อ "สถานะที่ขอให้ chief พิจารณา" ของจดหมายผล `notes_to_chief/20260906_1340_RE-273-RESULT-TGR-FILE-IS-THE-TRIGGER-ID-TO-LUA-TABLE.md` (RE runner 2026-09-06T13:40+07:00): "`RE-273` → **PARTIAL (เส้นทาง 1 ตอบแล้ว / เส้นทาง 2 ยังไม่ต้องเดิน)** · checkpoint = **time+scope checkpoint ไม่ใช่ method ceiling** ... ขอให้ **LANE-Q ตัดสิน** ว่าจะให้ต่อในใบนี้หรือแยกใบใหม่" · K คัดลอกคำของผู้ทำ **ไม่ได้ตัดสินเอง** · 🔴 **ใบนี้ยังอยู่บนรถบัสตาม `COO-DECISION 20260907_0445` ข้อ 3 ("ติดธง ไม่ถอน") — การพับหัวใบไม่ได้ถอนใบ** แต่ก่อนหน้านี้หัวใบเขียน `OPEN` ทั้งที่จดหมายผลถูก consume ไปตั้งแต่ 13:40 ของเมื่อวาน · 🔴 **ผู้อ่านต้องรู้ก่อนหยิบไปรัน**: "เส้นทาง 1" ของใบนี้เดินด้วย `staged/re273_tgr_parse.py` ซึ่ง **ไม่อยู่ในรีโป** (K วัดเองรอบ `73i74a`: `ls staged/*.py` คืนไฟล์เดียวคือ `re059_extract_capture.py`) และ `pf_git_sync.ps1` ทำให้ไฟล์ใหม่ใต้ `staged/` ขึ้นมาเองไม่ได้ ⇒ ต้องมีคนบนเครื่องสะพาน `git add` ให้ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน = ถอนแล้วโดยเจตนา ไม่ใช่สถานะสด): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` เป็นเส้นทางแรก และ `[NEEDS-ATTENDED-CAPTURE]` เป็นเส้นทางที่สอง (สองเส้นทาง หนึ่งใบ ตาม `COO-DECISION 20260906_0146` ข้อ 2) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-Q** · ตั้งเลขโดย chief (LANE-E) รอบ `xcbnbn`/R364 ตาม `COO-DECISION 20260906_0256` ข้อ 1 · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_0155_LANE-Q-RE-TICKET-trigger-id-to-lua-file-mapping.md` คำต่อคำ · **ตัวบล็อกเดียวที่เหลือของเกณฑ์ charter สาย Q** ("ผู้เทสแล่นเรือชนทริกเกอร์แล้วสคริปต์ทำงาน")] [🔎 **เกณฑ์ (ข) ตรวจแล้วโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 — ยังอยู่บนรถบัส ไม่ถอน** · ไฟล์ที่ใบเอ่ยถึง `src/pirateforce_foundation/lua_api/trigger.py` **เปลี่ยน 3 คอมมิตหลังใบถูกเขียน** (`24b058ca` 2026-09-07T00:25 · `06a9d17d` 2026-09-07T03:08 "message-wire: Player.ShowMessage + Trigger.TriggerShowMessage real" · `09580096` 2026-09-07T03:30) ⇒ ตัวเลข **"state machine 5/17 real"** ในเนื้อใบ **น่าจะล้าสมัยแล้ว** — ขอ **LANE-Q (เจ้าของใบ)** ยืนยัน/แก้ตัวเลขในรอบถัดไปของตัวเอง · **ไม่ถอนจากสแนปช็อต** เพราะเส้นทางแรกของใบเป็น `[STATIC-ON-BRIDGE]` (ไม่กินเวลาเครื่องเจ้าของ) และคำถามของใบอยู่ฝั่งไคลเอนต์ ไม่ได้วัด `trigger.py` ⇒ การถอนไม่ประหยัดเวลาเจ้าของแม้แต่นาทีเดียว ซึ่งเป็นเหตุผลเดียวของ `PANYA-ORDER 0159` ข้อ 2 (LANE-K ไม่แตะเนื้อใบ)]

🔴 **[LANE-K รอบ `qz3m7v` addendum 2026-09-07T20:20+07:00 — พับคำตัดสินของเจ้าของใบที่ค้างมา 28 ชม. · ความผิดของเสมียนเอง]** จดหมาย `notes_to_chief/20260906_1525_LANE-Q-RE-273-DECISION-continue-same-ticket-narrowed-to-tgr-ordinal-wire-crosswalk.md` (LANE-Q · 2026-09-06T15:25+07:00) **ไม่มีทั้ง `.CONSUMED.txt` และ `.LANEK-FOLDED.txt`** และไม่เคยถูกยกลงหัวใบนี้เลย — ทั้งที่หัวใบซึ่ง K พับเองเมื่อ 2026-09-07T10:09 ยังยกประโยค *"ขอให้ **LANE-Q ตัดสิน** ว่าจะให้ต่อในใบนี้หรือ…"* มาวางไว้ **19 ชั่วโมงหลังจากที่ LANE-Q ตัดสินไปแล้ว**
🟢 **คำตัดสินของเจ้าของใบ คำต่อคำ** (K ไม่ตีความ): *"**การตัดสินรอบนี้: ต่อในใบเดิม (RE-273) ไม่แยกใบใหม่**"* เพราะ *"คำถามที่เหลือเป็นคำถามเดียวกัน (id ไหนตรงกับ id ไหน) แค่แคบลงเหลือข้อเดียว ไม่ใช่คำถามใหม่"*
🟢 **คำถามเดียวที่เหลือของใบนี้ (คำของเจ้าของใบ)**: serializer ของ `TriggerVital 0x1FB2` (`0x006007C0` ตาม `PF_SERIALIZER_FIELDS.tsv`) **อ่าน field ไหนของเรคคอร์ด `.tgr`** ไปเทียบกับ tag `0x0F` ที่ส่งบนสาย — ถ้าเป็น field เดียวกับ `trigger_ordinal` ก็ปิดคำถาม · ถ้าเป็นคนละ field (เช่น index ของเรคคอร์ดในไฟล์ ไม่ใช่ `trigger_ordinal` ที่ฝังในเรคคอร์ด) ก็เป็นผลลบที่มีค่า
🔴 **ดังนั้นข้อความ "เส้นทาง 2 ยังไม่ต้องเดิน" ในหัวใบข้างบน *ล้าสมัย*** — ไม่ลบตามกติกาบ้าน แต่ **ห้ามใช้ตัดสินว่าใบนี้ไม่มีอะไรให้รัน** · RE runner ที่หยิบใบนี้ **มีงานหนึ่งข้อที่รันได้จริง** ตามย่อหน้าบน
🔵 **สิ่งที่ K ไม่ทำ**: ไม่แก้สถานะ `PARTIAL` (เจ้าของใบเท่านั้นที่ปิดใบ) · ไม่วาง `.CONSUMED.txt` แทน LANE-Q (บริโภคผล = สายเจ้าของใบ · `COO-DECISION 1541`) · วางเฉพาะ `.LANEK-FOLDED.txt` ซึ่งเป็นสตับของงานพับ
🔴 **ทำไมตัววัดของบ้านนี้มองไม่เห็น**: จดหมายฉบับนี้ชื่อ `-DECISION-` ไม่ใช่ `-RESULT-` และในเนื้อ **ไม่มีบรรทัด `RESULT:`** ⇒ หลุดทั้งการเกรปด้วยชื่อไฟล์และการเกรป `^RESULT:` · ตัววัด `NOW.md` ("`*RESULTS*` ไม่มี `.LANEK-FOLDED.txt` >6 ชม.") **มองไม่เห็นชนิดนี้เลย** — เขียนขึ้น COO แล้วในจดหมายรอบ

**คำถามของใบ**: อะไรคือตาราง/เส้นทางโค้ดที่แม็ป trigger id ของเฟรม `TriggerVital` (`0x1FB2`) ไปเป็นไฟล์ `.lua` ที่ไคลเอนต์ต้นฉบับรันสำหรับทริกเกอร์นั้น · มีสคริปต์ทริกเกอร์ที่ ship มา 309 ไฟล์ (`gamedata/lua/t_*.lua`) แต่ไม่มีสิ่งที่ commit ไว้ที่ไหนบอกว่า id ไหนยิงไฟล์ไหน · `lua_api/trigger.py` (state machine **8/17 real** — วัดสดรอบ `02mkqc` 2026-09-07T07:05+07:00 จาก `len(trigger.REAL_METHODS)`/`len(REAL_METHODS)+len(STILL_STUBBED)` บน `origin/main` `550a36d`: `GetTeiggerStatus` · `GetTriggerStatus` · `NextStatus` · `QuestActiveProgress` · `QuestFinishProgress` · `SetStatus` · `SetTriggerStatus` · `TriggerShowMessage` · เลขเดิม "5/17 รอบ `456vso`" ล้าสมัยตามที่ LANE-K รอบ `dmef5j` ชี้ และ `COO-DECISION 20260907_0445` ข้อ 5 สั่งให้เจ้าของใบแก้ — **เลขนี้ไม่เปลี่ยนคำถามของใบ** ซึ่งอยู่ฝั่งไคลเอนต์ ไม่ได้วัด `trigger.py`) พร้อมถูกเรียกแล้ว ขาดแค่เส้นทาง dispatch สดที่ป้อน trigger id จริงให้มัน

### ค้นแล้ว (รอบ `4jsydv` ยืนยันซ้ำรอบ `vqng2z`) — เริ่มต่อจากนี้ ห้าม grep ซ้ำ
- `gamedata/tables/`: ไม่มีคอลัมน์ไหนตรง `\.lua|ScriptStart|script_name|s_Script` เลย · `CONSTDATA_TH__Trigger.tsv` มีแค่ `n_ID`/voice/`n_MESSAGE_TYPE` ไม่มีคอลัมน์ชื่อสคริปต์
- `gamedata/scene/*/*.placements.tsv`: ตรวจแถวหัวแล้ว ไม่มีคอลัมน์ชื่อสคริปต์
- `external/`: มีแค่ `PF_SERIALIZER_FIELDS.tsv` (layout ของเฟรม ไม่ใช่ตาราง id->file)
- `archive/` และ `notes_to_chief/consumed/`: ไม่เจอ
- **ชื่อไฟล์สคริปต์ไม่ได้เข้ารหัส id ในตัวเอง** — `t_nex_t6.lua` ไม่ได้แปลว่า "ทริกเกอร์ 6 ในฉาก nex" (อ่านซอร์สแล้ว: `Var1..Var6` ของมันคือทริกเกอร์**อื่น**หกตัวที่มันรออยู่ ไม่เกี่ยวกับชื่อตัวเอง)
- **grep ที่ห้า** `notes_to_chief/reference_codex_attr/` — chief ตรวจเองรอบ `xcbnbn`: `grep -rilE 'trigger.*lua|script_name|s_Script'` = 0 hit (ที่นี้เป็นตาราง ActorAttr ต่อคลาส ไม่ใช่ตารางสคริปต์)

### สองเส้นทาง หนึ่งใบ (`COO-DECISION 20260906_0146` ข้อ 2)
1. **`[STATIC-ON-BRIDGE]` ก่อน**: `pf-static-re` ค้น artifact ที่ commit แล้วซึ่งถอดมาจากไคลเอนต์ หาอย่างใดอย่างหนึ่ง (ก) ไฟล์ `.scn` ที่ `*.placements.tsv` เป็นเพียงการถอดบางส่วนของมัน ถ้ามีอยู่ในรีโป หรือ (ข) ตาราง lookup resource-path ในไบนารีใดก็ตามที่ disassemble ไว้แล้วใต้ `external/`/`archive/` — เซสชันคลาวด์ grep เองแล้วไม่เจอตามข้างบน pass ที่ลึกกว่านั้นต้องให้ `pf-static-re` รันข้างสำเนาไคลเอนต์ของสะพาน (`GameClient\` read-only)
2. **`[NEEDS-ATTENDED-CAPTURE]` ถ้า (1) ว่าง**: RE runner ทำ static disassembly pass บนอิมเมจไคลเอนต์จริงของสะพาน หาตาราง/ฟังก์ชัน lookup id -> resource path รูปเดียวกับ `RE-263`/`RE-266`

### `ATTENDED:` (ห้าบรรทัดพอดี ตาม `COO-DECISION 20260906_0146` ข้อ 3)
ATTENDED: แล่นเรือไปที่ทริกเกอร์ของ Prison Exile Island id `153` (ฉาก/พิกัดเดียวกับที่ `GT-233` บูตเข้าไปอยู่แล้ว) แล้วจับ log เครือข่ายฝั่งไคลเอนต์ ณ วินาทีที่ไปถึง
ATTENDED: ใน capture อ่านค่าของ `TriggerVital` (`0x1FB2`) tag `0x0F` (ฟิลด์ที่ `RE-234`/รอบ `ihjytc` พิสูจน์แล้วว่าถือ trigger id) คู่กับสิ่งที่ debug/log ของไคลเอนต์พิมพ์ใน tick เดียวกัน — ชื่อไฟล์สคริปต์หรือ resource path ถ้ามันพิมพ์เลย
ATTENDED: ผ่าน = จับคู่ trigger id (ค่าของ `0x1FB2` tag `0x0F`) กับชื่อไฟล์สคริปต์หนึ่งชื่อจาก capture เดียวกันได้อย่างน้อยหนึ่งคู่
ATTENDED: ไม่ผ่าน (ยังมีค่า) = ยืนยันว่าไม่มี log ฝั่งไคลเอนต์ที่บอกชื่อไฟล์สคริปต์ที่ verbosity ปกติ = บีบเส้นทาง 2 ให้เหลือ binary RE ล้วนไม่มีทางลัด
ATTENDED: บูต = บูตไคลเอนต์ปกติเข้าฉากแล่นเรือ M2 ที่อยู่ในทรี `GT-233` แล้ว ไม่มีธง/env พิเศษ (เป็น pass สังเกตการณ์บนทริกเกอร์ที่ไปถึงได้อยู่แล้ว ไม่ใช่เส้นทางโค้ดใหม่)

### เกณฑ์ปิดใบ
ปิดได้เมื่อตอบข้อใดข้อหนึ่ง: (ก) ชี้ตาราง/ฟังก์ชันที่แม็ป id -> ไฟล์ พร้อม VA/แถวอ้างอิง หรือ (ข) **BOUNDED-NEGATIVE**: ทั้งสองเส้นทางว่าง = การแม็ปอยู่ในโค้ดไคลเอนต์ที่ยังไม่มี disassembly ⇒ ขั้นถัดไปของ LANE-Q คือ CORE-REQUEST ขอ hook สังเกตการณ์ฝั่งเซิร์ฟเวอร์ (log trigger id ที่ไคลเอนต์ส่งจริงต่อฉาก) **ไม่ใช่การถอยของสิ่งที่สร้างไปแล้ว**

### ใบนี้ไม่ขอ / nonclaims
1. ไม่อ้างว่าการแม็ปนี้ไม่มีในไคลเอนต์ — อ้างแค่ว่าไม่มีในสิ่งที่ commit ไว้ในรีโปนี้ (หลักฐาน grep ข้างบน)
2. ไม่อ้างว่า capture `ATTENDED:` จำเป็นเหนือเส้นทาง 1 — เป็น fallback ที่ระบุชื่อไว้ถ้า static RE บนสำเนาไคลเอนต์ของสะพานว่าง
3. ไม่อ้างว่า `0x1FB2` tag `0x0F` เป็นฟิลด์**เดียว**ที่เกี่ยวในเฟรม — เป็นแค่ฟิลด์เดียวที่งาน RE ก่อนหน้า (`RE-234`) พิสูจน์แล้วว่าถือ trigger id

### result:
(ว่าง)

> 🔴 **ห้ามสายอื่นใช้เลข `RE-273`** · numbering: คำสั่งนับเลขของบ้าน (ข้อ ② หัวไฟล์นี้) รันสดรอบ `xcbnbn`/R364 คืน **272** ⇒ เลขว่างตัวถัดไปคือ **273** [วัดแล้ว รอบนี้] · ตรวจ 0 hit ของ `GT-273`/`RE-273` ทั้งสามที่ (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*.md`) ก่อนวาง
> 🔴 **ใบ GT คู่ของมันยังไม่มี และยังไม่ควรมี** — ใบนี้เป็นคำถาม static เส้นทางแรก ยังไม่มีสิ่งที่ผู้เทสจะเห็นบนจอจนกว่าจะรู้การแม็ป · เมื่อใบนี้ตอบแล้ว LANE-Q เปิดใบสร้าง + ใบ GT ในรอบเดียวกัน หรือเขียน `NO_FEATURE_WAITING:` (`COO-DECISION 20260906_0146` ข้อ 5)

- ~~RE-278 LV-LIVE-UPDATE-FRAME-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (🔧 **DONE (static) / POSITIVE + BOUNDED-NEGATIVE — พับโดย LANE-K รอบ `7 ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

- ~~RE-280 ITEMOPERATEVITALRES-EQUIP-WORN-FLAG-AND-W9-CROSSCHECK-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (🔧 **DONE — พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00** · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `dccuar` 2026-09-07T15:24+07:00 · ไม่มีบล็อก `ATTENDED:` ค้าง · ไม่ลบอะไรทั้งสิ้น)

## RE-283 GMUI-THREE-PAGES-BUTTON-TO-OPCODE-MAP-001  [✅ **ปิดครบทั้ง 5 ข้อแล้ว** (คำของจดหมายเอง) · `notes_to_chief/20260907_0331_RE-283-RESULT-FINAL-... -- archived 20260907 (CLOSED (owner LANE-GM consumed FINAL, asked head closed); verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`)

- ~~RE-285 TRIGGER-GETCONTACTMODE-ARGUMENT-SEMANTICS-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (🔧 **CLOSED / BOUNDED-NEGATIVE — พับโดย LANE-K รอบ `ek1gk9` 2026-09-07T ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

## RE-289 BG3001-TGR-ISLAND-CONTACT-DISCRIMINATOR-001  [🔧 **PASS / BOUNDED-POSITIVE — พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260907_0955_RE-289-RESULT-ordinal-2-and-3-exist-as-point-boxes-discriminator-is-real.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907_0942` 2026-09-07T09:55+07:00): "สถานะ: **PASS / BOUNDED-POSITIVE** — ตอบครบทั้งสองข้อของเกณฑ์ผ่าน และได้ตารางครบทุกเรคคอร์ด (52/52 ไม่มี `PARSE_FAILED`)" · K คัดลอกคำของผู้เทส **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน = ถอนแล้วโดยเจตนา ไม่ใช่สถานะสด): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` (อ่านไฟล์ข้อมูลไคลเอนต์บนเครื่องสะพาน read-only -- **ไม่ใช่ attended ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่กินเวลาเครื่องเจ้าของ** ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` ซึ่งบังคับเฉพาะใบ attended) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A (WORLD)** · ผู้ทำ = RE runner บนเครื่องสะพาน · ตั้งเลขโดย LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00 (ภายในรอบที่เห็นคำขอ) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_0426_LANE-A-TO-K-gt-body-re-bg3001-tgr-island-discriminator.md` คำต่อคำ · เปิดตาม `COO-DECISION 20260907_0405` ข้อ 3 (TIER 3 ต้องมี discriminator วัดจริงว่า "เกาะ != น้ำเปล่า" = ตัวบล็อก M2 ใน `NOW.md`)] -- moved to `tickets/RE-289.md` (เนื้อใบ 8,806 B > เพดาน 8,192 B ของ body ในคิว เจ้าของใบวัดมาเอง, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/`) [🟢 **หลักฐานตรวจซ้ำได้จากรีโปแล้ว — ช่องว่างที่ LANE-A ทวงสองรอบปิดแล้ว** · วางโดย LANE-K รอบ `dccuar` 2026-09-07T15:24+07:00 · dump เต็มของ `Bg3001.tgr` **คำต่อคำ 52 เรคคอร์ด** อยู่ในรีโปที่ `notes_to_chief/20260907_1510_RE-289-ARTIFACT-Bg3001-tgr-full-dump-verbatim.md` (จดหมายฉบับนั้น *คือ* ตัวไฟล์ ไม่ใช่คำบรรยายของไฟล์) · parser อยู่ในรีโปแล้วที่ `tools_bridge/re289_tgr_extract.py` (4,211 B · sha256 `eab4ce35f6ee39947bd2a09de0adeb488544a4cf88d4a455d8ced177bb0db283`) · อินพุต `GameClient\Data\Scene\Save\Bg3001\Bg3001.tgr` (25,013 B · sha256 `e0022e94e6b780cd0d364ec83e328c5f76b7e1215daf57cc24b51e93153a525f`) อยู่บนเครื่องสะพาน read-only · ทำซ้ำ: `python3 tools_bridge/re289_tgr_extract.py "<GameClient>/Data/Scene/Save/Bg3001/Bg3001.tgr"` · 🔴 คำเตือนของผู้ส่งคำต่อคำ: *บรรทัด `FILE` บรรทัดแรกของ dump เป็น path ของเครื่องสะพาน — ต่างเครื่องจะต่างกัน บรรทัดอื่นทั้งหมดต้องตรงทุกตัวอักษร* · 🔴 K **ไม่ได้** `git mv` และไม่ได้ย่อ dump — คัดลอกไว้ที่เดิมตามกฎ `0945` (จดหมายฐานกุญแจสด คัดลอกเท่านั้น) · หมายเหตุถึงผู้อ่านที่มาจากคำขอในเนื้อใบ `RE-297` ("`staged/re289_tgr_extract.py` และ `staged/RE-289_Bg3001_tgr_full_dump.txt` ไม่มีในรีโป"): ของทั้งสองชิ้นมาถึงแล้วแต่**คนละที่**กับที่คำขอเขียนไว้ ตามที่ระบุข้างบน]

### result:
**PASS / BOUNDED-POSITIVE** -- พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00 · คัดลอกจาก `notes_to_chief/20260907_0955_RE-289-RESULT-ordinal-2-and-3-exist-as-point-boxes-discriminator-is-real.md` คำต่อคำ · **K ไม่ได้รันอะไรเองและไม่ได้ตัดสินผล**

> ## สถานะ: **PASS / BOUNDED-POSITIVE**
> ตอบครบทั้งสองข้อของเกณฑ์ผ่าน และได้ตารางครบทุกเรคคอร์ด (52/52 ไม่มี `PARSE_FAILED`)
>
> **(1) ordinal 2 และ 3 มีอยู่จริงในไฟล์นี้** — ทั้งคู่เป็น `Trigger TELCHK_LV`, `model = null`, `script = T_TELCHK_LV.lua`
>
> **(2) ทั้งคู่เป็นกล่องเฉพาะจุด ไม่ใช่กว้างเท่าฉาก**
>
> | ordinal | pos x, y, z | extent x, y, z | % ของกรอบฉาก (x / y) |
> |---|---|---|---|
> | **2** | -5426.19, 5129.33, 86.01 | 2000 x 2000 x 500 | **10.6% / 10.6%** |
> | **3** | -1916.55, -6137.92, 86.02 | 1800 x 1800 x 500 | **9.6% / 9.6%** |
>
> เกณฑ์ใบคือ < 20% ทั้งสองแกน ⇒ **ผ่านทั้งคู่**
>
> ⇒ ในชั้นข้อมูลไคลเอนต์ **มีกล่องเฉพาะจุดให้จำแนกจริง** · `world_m2_trigger_vital_response.ISLAND_CONTACT_DISCRIMINATOR` (วันนี้ `None`) มีของให้เติมแล้ว · ทาง `.tgr` **ไม่ปิด**

🔴 **nonclaims ของใบและของผล — K ยกมาครบ ห้ามอ่านบล็อกข้างบนโดยไม่อ่านสี่ข้อนี้** (คัดลอกคำต่อคำจากจดหมายผลและจาก `tickets/RE-289.md`)
1. `tickets/RE-289.md` หัวข้อ "สิ่งที่ใบนี้ **ไม่** ถาม" ข้อ 1: *"⇒ ผลใบนี้ **ยังไม่พอ** เติม `ISLAND_CONTACT_DISCRIMINATOR` ด้วยตัวเอง"* — 🔴 **ประโยค "มีของให้เติมแล้ว" ข้างบนไม่ใช่ใบอนุญาตให้ assign ชื่อลงไปหนึ่งบรรทัด**
2. nonclaim ของผล: *"ไม่ได้พิสูจน์ว่า `trigger_ordinal` = wire trigger id ของ `TriggerVital 0x1FB2` tag `0x0F`"* — 🔴 ห้ามจับคู่กับ `+0x3C` ของ `RE-286` เพราะเลขเท่ากัน
3. nonclaim ของผล: *"ไม่ได้พิสูจน์ว่ากล่องสามใบนั้น 'คือเกาะ' — การเรียกมันว่าเกาะเป็นการตีความของ LANE-A ไม่ใช่ของผล"*
4. `BUILD_IMPACT` ของผล ข้อ 2: **`Player.TeleportCheck` เป็น `STUB_NOOP` บนเซิร์ฟเวอร์** — สคริปต์ที่กล่องทั้งสามเรียก **วันนี้ยังไม่ทำอะไร**

🟡 **ชั้นที่ขาด (K ไม่ปั๊มให้ครบ)**: nonclaim ข้อ 4 ของจดหมายเขียนเองว่า *"ผลนี้เป็นชั้น wire/DB-side static ล้วน **ไม่มีชั้น client-observable**"* ⇒ ใบนี้ปิดในฐานะใบ static เท่านั้น เหมือน `RE-278`/`RE-280`

🔴 **ถอนการอ้าง artifact สามชิ้น — ไม่มีชิ้นไหนอยู่ในรีโป และ "รอ sync" เป็นคำตอบที่ผิด** (K วัดเองรอบ `73i74a` หลังผล `pf-adversary`)
จดหมายผลอ้างสามไฟล์พร้อม sha256 · `ls staged/*.py` บนโคลนนี้คืน **`staged/re059_extract_capture.py` ไฟล์เดียว**:

| ไฟล์ที่จดหมายอ้าง | สถานะจริงในรีโป |
|---|---|
| `staged/re289_tgr_extract.py` (3,873 B) | **ไม่มี** |
| `staged/RE-289_Bg3001_tgr_full_dump.txt` (19,089 B) | **ไม่มี** — 🔴 **นี่คือไฟล์ที่ถือ "ตารางครบทุกเรคคอร์ด" ซึ่งเป็นเกณฑ์ผ่านของใบเอง** (`tickets/RE-289.md`: "ไม่ผ่าน = รายงานเฉพาะ ordinal 2-3 โดยไม่ให้ตารางเต็ม") |
| `staged/re273_tgr_parse.py` (2,406 B) | **ไม่มี** — อยู่ในตาราง "SHA (ก่อน = หลัง ตรวจแล้ว)" ของจดหมาย ทั้งที่ git ไม่เคยถือไฟล์นี้ |

🔴 **"รอ sync ของสะพานพามาก่อน" ที่ K เขียนไว้ตอนแรกในบล็อกนี้ = ผิด ถอนทิ้งแล้ว** · `pf_git_sync.ps1` **ออกแบบมาให้เป็นไปไม่ได้**: `staged` ไม่อยู่ใน `$ALLOWLIST` (บรรทัด 165-167 = รายการเดียวที่สแกนด้วย `--untracked-files=all`) และ `$SHARED_TRACKED` (บรรทัด 188) สแกนด้วย `--untracked-files=no` ซึ่งคอมเมนต์ของตัวมันเองบรรทัด 712-715 อธิบายว่า *"a file that is not already in git cannot appear here"* ⇒ **ไฟล์ใหม่ใต้ `staged/` ไม่มีทางขึ้นมาเองตลอดกาล**
⇒ **ทางเดียวคือมีคนบนเครื่องสะพาน `git add` ไฟล์นั้นตรง ๆ** · K ทำแทนไม่ได้ (ไม่มีไฟล์) · **ปฏิบัติแบบเดียวกับที่ K ทำกับ `RE-234` เมื่อ 08:35**: หลักฐานส่วนที่อ้างไฟล์เหล่านี้ **ไม่มี artifact ที่ commit แล้วรองรับ** — สถานะ `PASS` ข้างบนยังเป็นคำของผู้เทสคำต่อคำ (K ไม่ถอนคำตัดสินของใคร) แต่ **ผู้อ่านต้องรู้ว่าตรวจซ้ำจากรีโปไม่ได้**
🔴 **ครั้งที่สามติดกันของสาเหตุเดียวกัน**: `RE-234` (`staged/re234_static_verify.py`) · `RE-273` (`staged/re273_tgr_parse.py`) · `RE-289` (สามไฟล์ข้างบน) ⇒ K ยกเป็นคำถามเชิงระบบถึง COO ในจดหมายรอบ `73i74a`
🔸 K ตรวจตัวเลขในผลเองด้วย: จดหมายเขียน `52/52` · ตารางในจดหมายแสดง **23 แถว** และร้อยแก้วบอกว่า "ที่เหลืออีก **27** แถว (ord 32, 71-98)" แต่ `1 + 28 = 29` ไม่ใช่ 27 (23+29 = 52 ถูก) ⇒ **เลข 27 คลาดสอง** · K ไม่แก้คำในจดหมาย และ **ตรวจซ้ำไม่ได้** เพราะไฟล์ dump ไม่อยู่ในรีโป
🟢 **[LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00] ผู้ทำใบยืนยันเองแล้วว่า K ถูก — เลขที่ถูกคือ 29 ไม่ใช่ 27** · คำต่อคำจาก `notes_to_chief/20260907_1455_RE-289-CORRECTION-the-remaining-row-count-is-29-not-27.md` (RE runner ผู้ทำ `RE-289` เอง): *"`ord 32` (1 ใบ) + `ord 71..98` (28 ใบ) = **29** ไม่ใช่ 27 · LANE-K รอบ `73i74a` ตรวจเจอเองและบันทึกไว้ในหัวใบ ⇒ **ยืนยันว่าถูกต้อง เลข 27 ของผมคลาดไปสอง**"* · ตารางที่ผู้ทำใบส่งมา: เรคคอร์ดทั้งหมด **52** · แถวในตารางของจดหมาย **23** · แถว `TIP`+`Ocean_Arrow_000 nn` ที่ย่อไว้ **29** · 23+29 = 52 · 🔴 **สิ่งที่ไม่เปลี่ยน (คำของผู้ทำใบ)**: *"คำตอบของใบ (ordinal 2 และ 3 มีจริง · extent 2000x2000 และ 1800x1800 = กล่องเฉพาะจุด) **ไม่ได้อาศัยเลข 27/29 เลย** ⇒ ข้อสรุปของ `RE-289` ไม่กระทบ"* และ `52/52` ไม่มี `PARSE_FAILED` ยังถูกต้องตามเดิม · **สถานะของใบไม่ขยับ** — K แก้เฉพาะตัวเลขที่ผู้ทำใบแก้เอง ไม่ได้ตัดสินผลใหม่ · ยังค้าง: ไฟล์ `staged/RE-289_Bg3001_tgr_full_dump.txt` (19,089 B) ยังอยู่แต่บนสะพาน ⇒ ตรวจซ้ำจากรีโปยังไม่ได้ (K ตอบรับข้อเสนอของผู้ทำใบแล้วในจดหมาย `notes_to_chief/20260907_1422_LANE-K-TO-RE-RUNNER-yes-send-the-re289-dump-inline.md`)

✅ **[LANE-K รอบ `wb8tfv` 2026-09-07T11:10+07:00] หนึ่งในสามชิ้นเข้ารีโปแล้ว — ตัว parser** ที่ `tools_bridge/re289_tgr_extract.py`
COO ส่งซอร์สเต็มมาในจดหมาย `notes_to_chief/20260907_1052_COO-TO-K-and-A-re289-parser-source-inline-because-staged-cannot-travel.md` (เส้นทางเดียวที่ของใหม่เดินออกจากสะพานได้โดยไม่แตะ `.gitignore`) และยืนยันว่า **บรรทัด un-ignore + การเลือกไฟล์ที่อยู่ถาวร = งาน LANE-K** ⇒ ปิดป้าย `[สมมติของสาย LANE-K - รอ COO ยืนยัน]` ที่ค้างอยู่บนบรรทัด `!/tools_bridge/pf_results_index.py`
- **K วัดเอง**: `sha256(tools_bridge/re289_tgr_extract.py)` = `eab4ce35f6ee39947bd2a09de0adeb488544a4cf88d4a455d8ced177bb0db283` = ค่าที่**ทั้งจดหมายผล (`0955` ตาราง SHA) และจดหมาย COO (`1052`) เขียนไว้ตรงกัน** · ไฟล์ ASCII ล้วน (`.decode('ascii')` ผ่าน) · `git status` ลิสต์ไฟล์นี้จริงหลังเติมบรรทัด un-ignore (ถ้าไม่เติม = ถูก ignore = หายเงียบแบบ chief R232)
- 🔴 **K วางไฟล์ ไม่ได้รับรองว่า parser ถูก** — ไม่เคยรัน ไม่มี `Bg3001.tgr` บนโคลนคลาวด์ · ผลของใบยังยืนตามคำผู้ทำเหมือนเดิม
- 🔴 **ตัวเลขสองตัวในจดหมายผลขัดกันเอง K ไม่ตัดสินว่าตัวไหนผิด**: ตาราง SHA ของจดหมาย `0955` เขียน `staged/re289_tgr_extract.py` = **3,873 B** คู่กับ sha256 `eab4ce35...` · แต่ไฟล์ที่ให้ sha256 นั้นจริง ๆ ยาว **4,211 B** (วัดบนไฟล์ที่เพิ่งวาง) ⇒ ขนาดกับ sha มาจากไบต์คนละชุด อย่างน้อยหนึ่งตัวในจดหมายผิด · **K เชื่อ sha256 เพราะตรวจซ้ำได้เอง และเพราะสองจดหมายที่ไม่พึ่งกันเขียนค่าเดียวกัน** ส่วนขนาดยกให้เจ้าของใบ/ผู้ทำตอบ
- 🔴 **อีกสองชิ้นยังไม่มีในรีโป**: `staged/RE-289_Bg3001_tgr_full_dump.txt` (ไฟล์ที่ถือ "ตารางครบทุกเรคคอร์ด" = เกณฑ์ผ่านของใบเอง) และ `staged/re273_tgr_parse.py` ⇒ **บล็อกถอนการอ้าง artifact ข้างบนยังยืนสำหรับสองชิ้นนั้น** · ทางเดียวยังคงเป็นคนบนเครื่องสะพานหรือคนที่ถือไฟล์ ส่งเนื้อมาทางจดหมายแบบที่ COO เพิ่งทำกับ parser

**ข้อที่สองที่จดหมายขอ**: MEMORY ของ RE runner เข้าไม่ถึงจากเซสชันของผู้ทำ — เป็นคำขอถึง Panya ไม่ใช่งานเสมียน

🟢 **บริโภคและปิดโดย LANE-A (เจ้าของใบ) รอบ `qvdk7n` 2026-09-07T10:22+07:00** -- `pirate-force-server#1015`: `ISLAND_EXTENT_BOXES` เติมสามแถว (ordinal **1/2/3** = กล่องจัตุรัสทุกใบที่ผ่านบาร์ของใบเอง `< 20% ทั้งสองแกน` -- ไม่ใช่แค่ 2/3 เพราะการเลือกด้วยเลข wire id คือ crosswalk ที่ใบนี้ไม่ได้พิสูจน์) อ้างใบนี้ + sha256 ของจดหมายผลทุกแถว และมีเทสคำนวณกล่องย้อนจากสตริง citation ของตัวเอง · กล่อง = `pos ± extent/2` · คีย์ = ordinal ของ `.tgr` **ไม่ใช่ wire trigger id** (ตารางถูกอ่านด้วย `.values()` เท่านั้น)

🔴 **`ISLAND_CONTACT_DISCRIMINATOR` ยังเป็น `None`** -- ตรงกับ nonclaim ข้อ 1 ที่ K ยกมาข้างบนเป๊ะ ๆ · รอ **ใบ crosswalk ordinal <-> wire trigger id** (ยังไม่มีเลข) · รอบแรกของ `qvdk7n` เผลอเติมชื่อ pf-adversary จับได้ commit ที่สองย้อนแล้ว

🟡 **สองข้อที่ LANE-A รับไปทำต่อจากบล็อกนี้**: (1) เนื้อใบ RE เรื่อง `pos` = กึ่งกลางหรือมุมต่ำ และ `extent` = กว้างเต็มหรือครึ่ง ส่ง K แล้ว `notes_to_chief/20260907_1022_LANE-A-TO-K-re-ticket-body-tgr-extent-is-full-or-half-width.md` (สองข้อนี้ตัดสินว่ากล่องอยู่ตรงไหนจริง และข้อ `pos` **ไม่ fail-closed**) · (2) LANE-A ยืนยันการวัดของ K เรื่อง artifact: `ls staged/ | grep -i re289` = **0 hit** บนโคลนคลาวด์เช่นกัน ⇒ commit ให้จากคลาวด์ไม่ได้

> numbering: ตัวนับร่วมสองคิว + `archive/*ARCHIVE*` + `tickets/` คืนสูงสุด **288** (`GT-288`, ตั้งเลขรอบ `6rj6h1`) ⇒ ใบนี้ **289** · ตรวจ 0 hit ของ `GT-289`/`RE-289` ทั้งสามที่ + `notes_to_chief/` + `NOW.md` ก่อนวาง [ตรวจโดย LANE-K รอบ `70l5du`]

- ~~RE-286 TRIGGERRESULT-DIRECTION-AND-CALLER-CHAIN-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (🔧 **DONE — พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00** · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `dccuar` 2026-09-07T15:24+07:00 · ไม่มีบล็อก `ATTENDED:` ค้าง · ไม่ลบอะไรทั้งสิ้น)

- ~~RE-290~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (CLOSED / PASS-BOUNDED-POSITIVE -- LANE-B ปิดตามคำขอเจ้าของใบ (RE-290 consumed, GT-288 ชุด 2 ผู้สมัคร AT5 คงไว้) · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `0sw9f6` 2026-09-07T21:23+07:00 · ไม่มีอะไรถูกลบ)

- ~~RE-292~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (PASS/BOUNDED-POSITIVE -- LANE-GM (GM_RunGmCommand 0x51E9 leading pair + presence slot answered) · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `0sw9f6` 2026-09-07T21:23+07:00 · ไม่มีอะไรถูกลบ)

## RE-293 PLAYER-STR-DERIVATION-SOURCE-001  [🔧 **PASS / DONE (ข้อ 2 ปิด) — พับโดย LANE-K รอบ `xsaz4f` 2026-09-07T23:13+07:00** คำต่อคำจากบรรทัด "สถานะ" ของจดหมายผล `notes_to_chief/20260907_2043_RE-293-RESULT-item2-no-addition-anywhere-and-STANDARD_BUFF-is-the-per-level-stat-table.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907_2033` 2026-09-07T20:43+07:00): "PASS / DONE (ข้อ 2 ปิด)" · K คัดลอกคำของผู้ทำ **ไม่ได้ตัดสินเอง** · ข้อ 2 ปิดด้วยผลลบ: ไม่มีจุดใดในไคลเอนต์ที่คำนวณ STR (ทุกจุดเขียน `ActorAttr+0x82` เป็น zero-init/copy/masked-copy เท่านั้น) ⇒ STR บนจอ = ค่าที่เซิร์ฟเวอร์ส่งมาตรง ๆ · จดหมายเดียวกันแก้ `BUILD_IMPACT 4` ของผลรอบก่อน: ตารางสแตทต่อเลเวลของผู้เล่นมีอยู่แล้วคือ `gamedata/tables/CONSTDATA_TH__STANDARD_BUFF.tsv` (256 แถว 36 คอลัมน์ ไม่ใช่ `POTENTIAL` ซึ่งว่าง 0 แถวถาวร) · nonclaims ครบตามใบ (ไม่อ้างว่า `STANDARD_BUFF.n_ID` = เลเวลตัวละคร · ไม่อ้างว่าไคลเอนต์เขียน `STANDARD_BUFF` ลง `ActorAttr+0x82` โดยตรง · ไม่อ้างสแตทต่ออาชีพ)] 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🟡 **PARTIAL** (ตอบข้อ 1 · 3 · 4 ครบ · **ข้อ 2 ยังเปิด** = เดินจาก `0x005888D5` หา `find(key)` และดูว่าค่าถูกบวกกับอะไรก่อนลง `ActorAttr+0x82`)~~ · 🔺 `[STATIC-ON-BRIDGE]` (อ่านไบนารี/ไฟล์ที่มีอยู่แล้วบนเครื่องสะพาน read-only -- **ไม่ใช่ attended ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่กินเวลาเครื่องเจ้าของ** ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` ซึ่งบังคับเฉพาะใบ attended) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-CS (CLASS/SKILL)** · ผู้ทำ = RE runner บนเครื่องสะพาน · ตั้งเลขโดย LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00 (ภายในรอบที่เห็นคำขอ 06:18) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_0618_LANE-CS-TO-K-re-body-where-the-player-str-comes-from.md` คำต่อคำ · เปิดตาม `COO-DECISION 20260907_0445` ข้อ 3 ("ใช่ — เปิดใบ RE/STATIC") · ชนิด = STATIC จาก client image (ไม่ต้อง attended)]
> RE-293 PLAYER-STR-DERIVATION-SOURCE-001  [🔧 **PARTIAL — ตอบข้อ 1, 3, 4 ครบ · ข้อ 2 ยังเปิด — พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260907_1330_RE-293-RESULT-potential-is-keyed-by-n_ID-and-s_SCORE-is-never-read.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907_1100-OWNER-ORDERED-FULL-SWEEP`): "สถานะ: **PARTIAL — ตอบข้อ 1, 3, 4 ครบ · ข้อ 2 ยังเปิด**" · K คัดลอกคำของผู้ทดสอบ **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` (อ่านไบนารี/ไฟล์ที่มีอยู่แล้วบนเครื่องสะพาน read-only -- **ไม่ใช่ attended ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่กินเวลาเครื่องเจ้าของ** ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` ซึ่งบังคับเฉพาะใบ attended) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-CS (CLASS/SKILL)** · ผู้ทำ = RE runner บนเครื่องสะพาน · ตั้งเลขโดย LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00 (ภายในรอบที่เห็นคำขอ 06:18) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_0618_LANE-CS-TO-K-re-body-where-the-player-str-comes-from.md` คำต่อคำ · เปิดตาม `COO-DECISION 20260907_0445` ข้อ 3 ("ใช่ — เปิดใบ RE/STATIC") · ชนิด = STATIC จาก client image (ไม่ต้อง attended)]
> ผลกลับแล้ว 2026-09-07T13:30 · `notes_to_chief/20260907_1330_RE-293-RESULT-potential-is-keyed-by-n_ID-and-s_SCORE-is-never-read.md` · **บริโภคแล้วโดยเจ้าของใบ (LANE-CS) รอบ `0fmem3`** (สตับ `.CONSUMED.txt` + สำเนาใน `consumed/`) · BUILD_IMPACT 3 จ่ายเป็นโค้ดแล้ว (`pirate-force-server` `909c765`) · BUILD_IMPACT 4 = คำถามออกแบบ ส่ง `20260907_1345_LANE-CS-ASK-COO-potential-ships-empty-who-sets-base-str.md` · 🔴 **แก้รายการในใบ**: `POTENTIAL_BINDS` มี **7** ตัว ตัวแรก `0x4A43BE` = `n_ID` คือ **คีย์** และ `0x4A449D` = `n_LEVEL` **ไม่ใช่สแตท**

### คำถามเดียวของใบ
ค่า **STR ของตัวละครผู้เล่น** ที่ไคลเอนต์เอาไปแสดง/ใช้ ถูก **derive** มาอย่างไร — ตารางที่ยังไม่ dump, สูตรจากเลเวล, หรือผลสะสมของแต้มที่ผู้เล่นแจก · ต้องได้ **ที่มาของตัวเลข** ไม่ใช่แค่ตำแหน่งบนสาย

### grep แล้ว (ตามกฎ "grep ก่อนออกใบ") — เจอ/ไม่เจอ อะไรบ้าง
**เจอ (ไม่ต้องถามซ้ำ):**
1. **ตำแหน่งบนสายรู้แล้ว** — STR = `ActorAttr +0x82`, u16, tag `0x12`, mask `1<<5` (`src/pirateforce_foundation/gm/attr_wire.py` แถว 18 `LABEL_STR`; CON/DEX/INT/PER = `+0x84/86/88/8A`) ⇒ **ใบนี้ไม่ได้ถามหา offset/tag/mask ห้ามตอบด้วยของที่มีแล้ว**
2. **ชื่อตารางรู้แล้ว** — `CONSTDATA_TH__POTENTIAL` มีคอลัมน์ `n_STRENGH` (สะกดแบบนี้จริงในเกม), `n_CONSTITUTION`, `n_AGILITY`, `n_INTELLECT`, `n_PERCEPTION` (`tools/pf_stats_progression_static.py:88,1273` · สตริงชื่อตารางที่ `0xF14B94`)
3. **จุดผูกตารางรู้แล้ว** — `POTENTIAL_BINDS = [0x4A449D, 0x4A44C5, 0x4A44E5, 0x4A4502, 0x4A4522, 0x4A4542]` (ไฟล์เดียวกัน บรรทัด 658)
4. `STANDARD_STATUS` มีคอลัมน์ `n_POINT_ABILITY` (งบแต้มต่อเลเวล **อย่างมากที่สุด** — `persistence_standard_status.py:53`) และ **ไม่มีคอลัมน์ต่อสแตท** (`src/pirateforce_foundation/data/standard_status.tsv` หัวตารางมี 8 คอลัมน์ ไม่มีสแตทเลย)
5. `Attribute (0x1306)` และ `FightAttr (0x1285)` ชี้ serializer ไปที่ `0x515EC0` = `ret 8` ⇒ **ไม่มีฟิลด์บนสายในบิลด์นี้** (`pf_stats_progression_static.py:84-86`) — อย่าไปตามทางนั้น

**ไม่เจอ (นี่คือช่องว่างจริง):**
- `CONSTDATA_TH__POTENTIAL.tsv` ที่ commit แล้ว **มีแต่หัวตาราง ศูนย์แถวข้อมูล** (`class_catalog.py:61-64`) ⇒ ค่าตัวเลขจริงไม่มีอยู่ในรีโปทั้งสอง
- `s_SCORE` บน `CHARCREATE_CLASS` — โครงการนี้ **ไม่เคย RE ความหมายของมัน** (นับรวมใน "37 other columns" ของ `reports/PF_JOB001_...` และไม่ถอดสักคอลัมน์)
- ไม่มีที่ไหนในสองรีโปที่บอกว่า STR ผูกกับ **เลเวล** หรือกับ **คลาส** หรือทั้งคู่ (grep `n_STRENGH` = 3 hit ทั้งหมดเป็น comment)

### ที่อยากได้กลับมา (เรียงตามความสำคัญ ตอบได้เท่าไรเอาเท่านั้น)
1. **คีย์ของตาราง `POTENTIAL`** — จากโค้ดที่ `POTENTIAL_BINDS` ทั้งหก: ตารางนี้ lookup ด้วยอะไร (class id? level? class×level?) และผลลัพธ์ถูกเขียนลง `ActorAttr+0x82..0x8A` ตรง ๆ หรือผ่านการบวก
2. **ผู้เรียก** — มีเส้นทางไหนที่เอา `n_POINT_ABILITY` (งบแต้ม) มาบวกทับค่าจากตาราง เช่นตอน `AbilityDepolyAll` ⇒ ถ้าใช่ STR ที่เห็นบนจอ = ค่าฐานจากตาราง + แต้มที่ผู้เล่นแจก (สองแหล่ง ไม่ใช่แหล่งเดียว)
3. **`s_SCORE`** — คอลัมน์นี้ถูกอ่านที่ VA ไหน และถูกใช้เป็นค่าเริ่มต้นของสแตทหรือไม่ (ตอบ "ไม่ถูกอ่านเลย" ก็เป็นคำตอบที่มีค่า)
4. ถ้าตาราง `POTENTIAL` ตัวเต็มอยู่ในไฟล์ข้อมูลนอก image — บอก **ชื่อไฟล์/ที่อยู่ที่ไคลเอนต์เปิด** ก็พอ (จะได้ออกใบ dump ต่อ ไม่ใช่เดาค่า)

### ทำไมสาย CS ต้องใช้
สูตรดาเมจฝั่งผู้เล่นตอนนี้ตีด้วย **ค่าคงที่ตัวเดียว** (`MOB_COMBAT_DEFAULT_ATTACKER`) ⇒ ผู้เล่นทุกอาชีพทุกเลเวลตีแรงเท่ากันบนจอ · ครึ่ง level แก้ได้แล้วด้วย `CORE-REQUEST` รอบนั้น · **ครึ่ง STR แก้ไม่ได้จนกว่าใบนี้ตอบ** และตามคำสั่ง COO ห้ามเดาแหล่ง ห้าม hardcode ตัวเลขที่ไม่มีที่มา

### nonclaims
- ใบนี้ **ไม่ได้อ้างว่า `POTENTIAL` คือคำตอบ** — มันเป็นผู้ต้องสงสัยที่ชื่อคอลัมน์ตรงที่สุด เท่านั้น
- ไม่อ้างว่า STR มีผลต่อดาเมจในบิลด์นี้ (สูตรฝั่งมอนใช้ `strength` — ฝั่งผู้เล่นยังไม่มีใครวัด)
- ไม่ขอ capture จากเครื่องเจ้าของ: ตอบได้จาก image ที่มีอยู่แล้ว ⇒ **ไม่มีบล็อก `ATTENDED:`** และไม่กินคิวรถบัส

### result:
**PARTIAL — ตอบข้อ 1, 3, 4 ครบ · ข้อ 2 ยังเปิด** -- พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · คัดลอกจาก `notes_to_chief/20260907_1330_RE-293-RESULT-potential-is-keyed-by-n_ID-and-s_SCORE-is-never-read.md` คำต่อคำ · **K ไม่ได้รันอะไรเองและไม่ได้ตัดสินผล**

> RE-293 RESULT — ตาราง `POTENTIAL` คีย์ด้วย **`n_ID`** · `s_SCORE` **ไม่ถูกอ่านเลยทั้งอิมเมจ**
>
> สถานะ: **PARTIAL — ตอบข้อ 1, 3, 4 ครบ · ข้อ 2 ยังเปิด**
> checkpoint = **time checkpoint ไม่ใช่ method ceiling** — รอบหน้าทำต่อได้จาก VA ที่ระบุท้ายจดหมาย
>
> (หลักฐานเต็ม ตาราง VA และ nonclaims อยู่ในจดหมายต้นฉบับ — K ไม่ย่อความ ไม่ตีความ)

> numbering [LANE-K รอบ `4af3qf`]: ต่อจาก `RE-292` ในรอบเดียวกัน ⇒ ใบนี้ **293** · ตรวจ 0 hit ครบสี่ที่ก่อนวาง

- ~~RE-294~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (PASS/DONE -- LANE-UI (Stall vital tail calls: StallOpen writes nothing extra, StallStart writes via 0x766C00) · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `0sw9f6` 2026-09-07T21:23+07:00 · ไม่มีอะไรถูกลบ)

- ~~RE-295~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (PASS/DONE -- LANE-Q (quest reward rounding is double-truncate, Lv reads player level via AddLvCriteriaExp) · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `0sw9f6` 2026-09-07T21:23+07:00 · ไม่มีอะไรถูกลบ)

## RE-296 CONSTDATA-MOBS-OUTFIT-SEMICOLON-WHICH-VARIANT-001  [🔧 **PARTIAL — พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260907_1450_RE-296-RESULT-outfit-kept-as-a-list-split-on-semicolon-tab-space.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907_1100-OWNER-ORDERED-FULL-SWEEP`): "สถานะ: **PARTIAL** — ตอบ "จุดที่ขอให้ RE เปิด" ข้อ 1 ครบและเด็ดขาด · ตัวเลือกปลายทางยังเปิด" · K คัดลอกคำของผู้ทดสอบ **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` (อ่านตัวโหลด CONSTDATA ของไคลเอนต์บนเครื่องสะพาน read-only — **ไม่ใช่ attended ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่กินเวลาเครื่องเจ้าของ** ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` ซึ่งบังคับเฉพาะใบ attended) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-B (COMBAT)** · ผู้ทำ = RE runner บนเครื่องสะพาน · ตั้งเลขโดย LANE-K รอบ `wb8tfv` 2026-09-07T11:10+07:00 (ภายในรอบที่เห็นคำขอ 10:46) ตาม `NOW.md` `PANYA 1910` ("เลขใบ/เนื้อใบ = LANE-K") · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_1046_LANE-B-TO-K-re-body-outfit-semicolon-picks-which.md` **คำต่อคำ K ไม่แก้สำนวนใด ๆ และไม่ได้ตัดสินคำถามของใบ** · ผูกกับ `NOW.md` "M4 · LANE-B ข้อ 1b" (`;` ใน `s_OUTFIT` ⇒ ใบ RE outfit งานหน้า) และ placement 40 ตัวของ M3 ชั้นสอง]
🔒 **SUPERSEDED-BY: PANYA 20260907_1313** — ปิดใบตามคำสั่ง `notes_to_chief/20260907_1346_COO-DECISION-panya1313-ticket-heads-citing-103-LANE-K.md` ข้อ 3 (*"ถ้ามีใบ RE ที่ตั้งไว้เพื่อถาม '`;` ใน `s_OUTFIT` แปลว่าอะไร' ให้ปิดด้วย `SUPERSEDED-BY: PANYA 20260907_1313` — COO ตัดสินแล้วว่าไม่ต้องออกใบ RE outfit"*) · วางโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · 🔸 **ข้อเท็จจริงที่ COO ยังไม่เห็นตอนเคาะ (13:46)**: ผล `RE-296` มาถึงหลังจากนั้น (จดหมาย stamp `1450`) และถูกพับไว้ในบล็อก `### result:` ของใบนี้แล้ว — K **ไม่ลบผล** ตามกติกา "ห้ามลบอะไรทั้งสิ้น" · ปิดใบ = ไม่ต้องใช้เวลา RE runner กับคำถามนี้อีก ไม่ใช่การลบสิ่งที่วัดมาแล้ว · 🔴 คำเคาะที่กลืนใบนี้ (`PANYA 1313` ผ่าน `NOW.md`): *"ศัตรู = `n_RANK`+`n_AI_COMBAT` เท่านั้น — `s_OUTFIT` (ลิสต์ `;`) **ไม่มีผลต่อกฎเลือก**"*

หัวข้อ: **`s_OUTFIT` ที่มี `;` ไคลเอนต์เลือกตัวไหน**

## คำถามเดียว
แถวใน `gamedata/tables/CONSTDATA_TH__MOBS.tsv` คอลัมน์ที่ 7 `s_OUTFIT` ที่มีหลายค่าคั่นด้วย `;`
**ไคลเอนต์เลือกค่าไหนมาสวมให้มอนหนึ่งตัว** และเลือกด้วยอะไร:
(ก) ตัวแรกเสมอ · (ข) สุ่มตอน spawn · (ค) ชี้ด้วยคอลัมน์อื่นในแถวเดียวกัน ·
(ง) ชี้ด้วยฟิลด์ที่ **เซิร์ฟเวอร์ส่งมาในเฟรม spawn** (ถ้าใช่ ขอชื่อฟิลด์ + ช่วงค่า)

## ทำไมต้องรู้ (ผลต่อผู้เล่นโดยตรง)
placement 40 ตัวของ M3 ชั้นสอง ต้องส่ง attr ของมอนจริงจากตาราง ไม่ใช่ attr ที่ประกอบเอง
ถ้าคำตอบเป็น (ง) แล้วเซิร์ฟเวอร์ไม่ส่งฟิลด์นั้น = มอนขึ้นจอผิดตัว/ไม่มีโมเดล ทั้งที่ชื่อแดงถูก
ถ้าเป็น (ก) หรือ (ข) = ผมวางได้เลยโดยไม่ต้องรออะไร

## วัดมาแล้วบนของที่ commit แล้ว (ตัวเลขจากรอบนี้ ทำซ้ำได้)
- `CONSTDATA_TH__MOBS.tsv` มี 3,210 แถวข้อมูล · **565 แถวมี `;` ใน `s_OUTFIT`** (17.6%)
- จำนวนค่าที่คั่น: 2 ค่า **507 แถว** · 3 ค่า **50 แถว** · 5 ค่า 3 แถว · 6 ค่า 2 แถว · **9 ค่า 3 แถว**
- ตัวอย่างจริง (คอลัมน์ 2 = `s_NAME`): `山地鹿` -> `M005_000_000_SP1;M005_000_000_SP2` ·
  `醉狼海賊團` -> `M001_000_000_N;M001_000_000_SP1` · `海軍士兵` -> `P_MALE_002_000_SP1;P_MALE_002_000_PAK`
- รูปของค่า: `M<nnn>_<nnn>_<nnn>_<N|SP1|SP2|...>` ⇒ ต่างกันที่ **suffix ท้าย** เป็นหลัก (N / SP1 / SP2 / PAK)

## grep แล้ว: เจอ/ไม่เจอ (ตาม COMMON_LANE_ROUND "แผนที่โปรโตคอล")
- `external/PF_SERIALIZER_FIELDS.tsv` — grep `outfit` (case-insensitive) = **0 hit** ⇒ ไม่มี layout ที่พิสูจน์แล้วของฟิลด์นี้
- `gamedata/lua/` (616 ไฟล์) — grep `outfit` = **0 ไฟล์** ⇒ สคริปต์เควสไม่ได้เลือก outfit
- `gamedata/PF_GAMEDATA_COLUMNS.tsv` — `s_OUTFIT` เป็นคอลัมน์ชนิดเดียวกัน (3/4) ในห้าตาราง
  (`MOBS` col 6-ฐาน0, `SHIP`, `GET_SHIPCORPSE`, `SAILING_RESULT`, และ `PETDATA` ใช้ชื่อ `s_OUTFITTING`)
  ⇒ ตัวอ่านฝั่งไคลเอนต์น่าจะเป็นตัวเดียวกันทั้งห้าตาราง ซึ่งช่วยให้หาได้จากทาง `SHIP` ก็ได้
- `notes_to_chief/reference_codex_attr/` — grep `outfit` = 0 hit (grep ที่ห้าตาม NOW.md)

## จุดที่ขอให้ RE เปิด (ทำจาก static ได้ ไม่ต้องบูตเกม)
1. ตัวโหลด CONSTDATA ของไคลเอนต์: หาโค้ดที่ split สตริงด้วย `';'` ในเส้นทางโหลดตาราง
   ถ้ามี = คำตอบอยู่ตรงนั้นว่าเก็บเป็นลิสต์แล้วเลือกทีหลัง หรือเลือกตอนโหลด
2. ถ้าไม่มี split ตอนโหลด ⇒ ค่าทั้งสตริง (`"A;B"`) ถูกส่งต่อไปที่ตัวสร้างโมเดล ⇒ ขอชื่อฟังก์ชันที่รับ
   และดูว่ามันเทียบกับ `n_ID_MODEL` (คอลัมน์ 4) หรือ index อะไร
3. ถ้าเจอการสุ่ม ขอบอกด้วยว่าใช้ seed อะไร (per-actor id / เวลา) — ถ้า seed มาจาก id ที่เซิร์ฟเวอร์ให้
   แปลว่าเซิร์ฟเวอร์คุมหน้าตาได้โดยไม่ต้องมีฟิลด์ใหม่

## ถ้า RE ตอบไม่ได้ในรอบเดียว
ผมเดินต่อด้วยสมมติ **(ก) ตัวแรกเสมอ** ติดป้าย `[สมมติของสาย LANE-B - รอ COO ยืนยัน]`
เพราะเป็นสมมติเดียวที่ deterministic และย้อนได้ด้วยการแก้ค่าเดียวในตัว placement
ผิดแล้วเสียอะไร: มอน 565 แถวขึ้นจอด้วย variant แรกเสมอ (หน้าตาซ้ำ) ไม่ทำให้ตี/ตาย/ลูทพัง

### result:
**PARTIAL** -- พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · คัดลอกจาก `notes_to_chief/20260907_1450_RE-296-RESULT-outfit-kept-as-a-list-split-on-semicolon-tab-space.md` คำต่อคำ · **K ไม่ได้รันอะไรเองและไม่ได้ตัดสินผล**

> RE-296 RESULT — ไคลเอนต์ **ไม่เลือกตอนโหลด** · แตกเป็นลิสต์เก็บไว้ทุกค่า · ตัวคั่นคือ **`;` + tab + space**
>
> สถานะ: **PARTIAL** — ตอบ "จุดที่ขอให้ RE เปิด" ข้อ 1 ครบและเด็ดขาด · ตัวเลือกปลายทางยังเปิด
> checkpoint = **time checkpoint ไม่ใช่ method ceiling**
>
> (หลักฐานเต็ม ตาราง VA และ nonclaims อยู่ในจดหมายต้นฉบับ — K ไม่ย่อความ ไม่ตีความ)

### result (ต่อ): พับโดย LANE-K รอบ `xsaz4f` 2026-09-07T23:13+07:00 · คัดลอกจาก `notes_to_chief/20260907_2053_RE-296-RESULT-avt-path-is-charcreate-ui-not-the-mob-consumer-and-outfit-corpus-has-no-tab-or-space.md` คำต่อคำ · **K ไม่ได้รันอะไรเองและไม่ได้ตัดสินผล** · 🔴 **ใบนี้ยังปิดอยู่ (`SUPERSEDED-BY: PANYA 20260907_1313` ด้านบน) — ผลนี้มาถึงหลังปิดใบ K ไม่ลบผล ไม่เปิดใบซ้ำ ตามกติกา "ห้ามลบอะไรทั้งสิ้น"**

> RE-296 RESULT (ข้อ 2 ต่อ) — เส้นทาง `.avt` คือ **UI สร้างตัวละคร ไม่ใช่ผู้บริโภค `s_OUTFIT` ของมอน** · คลัง `s_OUTFIT` **ไม่มี tab/space เลย** (0/3,210 แถว)
>
> สถานะ: **PASS / BOUNDED-POSITIVE** — ตอบคำถามหลักของใบ: ไคลเอนต์เอา **token ตัวแรกเสมอ ด้วย index ที่เขียนตายเป็น 0** ที่ `0x0059AA52` (ฟังก์ชัน `0x0059A7A0`) — ไม่ใช่สุ่ม (ไม่มีค่าคงที่ LCG ของ `rand()` CRT ในอิมเมจ) ไม่ใช่เซิร์ฟเวอร์ชี้ (ไม่มีฟิลด์บนสายแตะ index นี้)
> BUILD_IMPACT: `world_bg000x_identity.py` ที่ทำ `s_OUTFIT.split(';')[0]` อยู่แล้ว **ถูกต้อง** ทั้งตัวคั่นและ index · เสนอ COO ปลดรายการ `MONSTER_PRESENTATION@ACTIVE_SELECTION#N` เฉพาะส่วน outfit (ส่วน action/idle ยังค้าง) — **K ไม่ตัดสินเอง ส่งต่อ COO**
> (หลักฐานเต็ม ห่วงโซ่ VA ครบ ตาราง xref และ nonclaims อยู่ในจดหมายต้นฉบับ — K ไม่ย่อความ ไม่ตีความ)

> numbering [LANE-K รอบ `wb8tfv`]: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` + `tickets/` คืนสูงสุด **295** (`RE-295`, ตั้งเลขรอบ `73i74a`) ⇒ ใบนี้ **296** · ตรวจ **0 hit** ของ `GT-296`/`RE-296` ครบทุกที่ก่อนวาง (live สองคิว + `archive/` + `tickets/` + `notes_to_chief/` + `NOW.md`) ⇒ เลข 296 ไม่ได้ถูกจอง
> 📌 [LANE-K รอบ `wb8tfv`] เจ้าของใบเขียนมาเองว่า *"ถ้ามีใบเก่าครอบคลุมอยู่แล้ว ขอให้ K พับใบนี้ทิ้งแล้วชี้ใบเดิมกลับมา"* ⇒ K ค้นก่อนตั้งเลข: grep `OUTFIT`/`outfit` ในสองคิว + `archive/*QUEUE*ARCHIVE*` + `tickets/` (hit ทั้งหมด **54** แห่งบนสถานะก่อนรอบนี้ อ่านทีละแห่ง) = **ไม่มีใบ GT/RE ใบใดถาม "ไคลเอนต์เลือกค่าไหนเมื่อมี `;`" มาก่อน** — hit ที่เหลือทั้งหมด**ใช้** `s_OUTFIT` เป็นคอลัมน์อ้างอิง (`RE-149` `RE-171` `RE-173` `RE-188`) ไม่ได้ถามกลไกการเลือก ⇒ ตั้งเลขใหม่ ไม่ใช่ใบซ้ำ
> 🟡 **[LANE-K รอบ `wb8tfv`] ของที่บ้านนี้เคยวัดไว้แล้ว และ RE ควรอ่านก่อนเริ่ม (K ชี้ทาง ไม่ได้ตอบใบ)**: `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md:835` — nonclaim ข้อ 3 ของใบ LANE-A ที่ปิดไปแล้ว เขียนคำต่อคำว่า *"`n_ID 910` (Saben) มี `s_OUTFIT` เป็น **รายการหลายตัวคั่นด้วย `;`** สาย A ส่ง **ตัวแรก** เพราะส่งทั้งสตริง = ชื่อไฟล์ที่ไม่มีจริง ⇒ ไม่มีร่าง"* ติดป้าย `[สมมติของสาย A - รอ COO ยืนยัน]`
> ⇒ ข้อสังเกตนี้บอกว่า **"ส่งทั้งสตริง" ≠ "(ก) ตัวแรกเสมอ"** — ถ้าคำอธิบายนั้นถูก แผนสำรองของเจ้าของใบ (เดินต่อด้วย (ก)) ต้อง**ตัดสตริงเองก่อนส่ง** ไม่ใช่ส่งทั้งค่า · 🔴 K **ไม่ตัดสิน**ว่าข้อสังเกตนั้นถูกหรือผิด (มันติดป้ายสมมติของสาย A มาแต่ต้น และไม่เคยมีใครยืนยัน) — ~~K แค่ไม่ยอมให้บ้านนี้จ่ายรอบ RE runner ไปกับสิ่งที่มีคนเคยเห็นบนจอแล้ว~~
> 🔴 **[แก้โดย LANE-K รอบ `k01t0u` 2026-09-07T12:15+07:00 หลัง pf-adversary D2 — ประโยคที่ขีดฆ่าข้างบนเป็นความผิดของ K เอง ไม่ลบ]** **ไม่มีใครเคยเห็นเรื่องนี้บนจอ** และ K ไม่มีสิทธิ์เขียนว่ามีคนเห็น · วัดสามทางแล้ว: (1) บล็อกที่อ้างคือ `### nonclaims` ของ `GT-131` ซึ่งเขียน**ก่อน**รันเทส และบล็อก `### result (ผู้เทสกรอก)` ของใบเดียวกันใน archive **ว่างเปล่า** · (2) ต้นทางของ nonclaim นั้น `archive/rounds_2026-08-27_to_28/A_20260828_2240_pqx4fj_port-royal-real-identities.md:72-75` เขียนตรงข้าม: *"ถ้าส่งทั้งสตริงจะกลายเป็นชื่อไฟล์ `.avt` ที่ไม่มีจริง ⇒ actor ไม่มีร่าง · **แก้แล้ว: ส่งตัวแรก**"* = เงื่อนไข และแก้ไปก่อน commit · (3) `pirate-force-server` `origin/main` วันนี้: `world_bg0003_identity.py:160` `bg0004:183` `bg0005:199` `bg0006:145` ทำ `s_OUTFIT.split(';')[0]` พร้อม `MULTI_VARIANT_OUTFITS` + `_self_check` ที่ปฏิเสธตั้งแต่ import ถ้ามี `;` ดิบหลุดเข้าตาราง ⇒ **เคสส่งทั้งสตริงเกิดไม่ได้โดยโครงสร้าง**
> ⇒ 🔴 **ผลของการแก้นี้ทำให้ `RE-296` เร่งด่วนขึ้น ไม่ใช่ถูกตอบไปครึ่งใบ**: เซิร์ฟเวอร์ **แยกสตริงเองแล้วส่ง variant `[0]` เป็นชื่อไฟล์สำเร็จรูป** ⇒ ถ้าตัวโหลด CONSTDATA ของ**ไคลเอนต์**ต่างหากที่เป็นคนแยก เซิร์ฟเวอร์กำลังส่งรูปผิดอยู่แล้ววันนี้ · **K ยังไม่ตัดสิน**ว่าฝั่งไหนแยก นั่นคือคำถามของใบ
> 🔴 K **ไม่ได้ตัดสิน** ว่าคำตอบคือ (ก)/(ข)/(ค)/(ง) และไม่ได้รับรองตัวเลข 3,210/565/17.6% — ตัวเลขทั้งหมดเป็นของเจ้าของใบ วัดเอง ทำซ้ำได้ตามที่ใบบอก

- ~~RE-297~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (PASS/BOUNDED-POSITIVE -- LANE-A (bg3001 TGR box anchor is centre, extent is full width; item 2/4 open) · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `0sw9f6` 2026-09-07T21:23+07:00 · ไม่มีอะไรถูกลบ)

- ~~RE-298~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (PASS/BOUNDED-POSITIVE -- LANE-A (open-water frame is trigger 35, ordinal is a stored field) · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `0sw9f6` 2026-09-07T21:23+07:00 · ไม่มีอะไรถูกลบ)

- ~~RE-302~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (DONE -- LANE-GM (UpdateAttrVital version is zero per-class ctor constant, static, 4/4 answered) · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `0sw9f6` 2026-09-07T21:23+07:00 · ไม่มีอะไรถูกลบ)

## RE-303 CAPTAIN-REPORT-CONFIRM-INBOUND-VITAL-AND-OK-REPLY-001  [🔧 **PASS — พับโดย LANE-K รอบ `xsaz4f` 2026-09-07T23:13+07:00** คำต่อคำจากบรรทัด "สถานะ" ของจดหมายผล `notes_to_chief/20260907_2150_RE-303-RESULT-teleportcheck-0x4477-opens-confirm-22-ok-echoes-marker.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907_2137-OWNER-ORDERED-NO-CAP` 2026-09-07T21:50+07:00): "PASS — ตอบครบทั้งสามข้อด้วยไบต์ · สมมติฐานของเจ้าของใบถูก" · K คัดลอกคำของผู้ทำ **ไม่ได้ตัดสินเอง** · คำตอบ: vital ขาเข้า = `TeleportCheckVital` id `0x4477` · ฟิลด์เดียว u16 tag `0x0F` = `MARKER.n_ID` · เลือกข้อความ "เทียบท่า"(22)/"เดินหน้า"(21) จาก `SCENE_NAME[MARKER[u16].n_SCENE].n_SCENE_TYPE` · กด OK = ส่งเฟรมเดิมกลับพร้อม `MARKER.n_ID` เดิม · Cancel = ไม่ส่งอะไร · มีทางลัดที่ไคลเอนต์ ACK เองไม่เปิดหน้าต่างถ้าเงื่อนไขภายในตรง (รายละเอียดใน addendum `20260907_2158`) · **ผลนี้คือ "ประตู M" ก้าวสุดท้ายของ M2 ที่ `NOW.md` รอ** · BUILD_IMPACT ครบ 6 ข้อและ nonclaims ครบ 10 ข้ออยู่ในจดหมายต้นฉบับ (K ไม่ย่อ ไม่ตีความ) · artifact probe เจ็ดตัวอยู่ที่ `notes_to_chief/reference_re303_probes/` ตาม `notes_to_chief/20260907_2155_RE-303-ARTIFACT-*`] 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🟠 **OPEN (static-on-bridge) — เนื้อใบมาถึงแล้วและวางครบ**~~ (พลิกโดย LANE-K รอบ `lpjqus` 2026-09-07T20:25+07:00 · เนื้อใบจาก `notes_to_chief/20260907_1932_LANE-A-TO-K-re-body-captain-report-confirm-window.md` 19:32 **คำต่อคำ**) · ชื่อใบเปลี่ยนตามที่เจ้าของตั้งเอง (เดิม `CAPTAIN-REPORT-COMMON-CONFIRM-INBOUND-VITAL-001` เป็นชื่อที่ K ตั้งชั่วคราวตอนจองเลข) · เดิม ~~🅿️ **RESERVED — เลขจองแล้ว รอเนื้อใบจากเจ้าของ**~~ · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A (WORLD)** ตาม `NOW.md` บรรทัด "ประตู M (PANYA `1825`)" และ `COO-ORDER` ใน `notes_to_chief/20260907_1849_COO-ORDER-panya1825-number-the-captain-report-re-ticket-this-round-LANE-K.md` · ตั้งเลขโดย LANE-K รอบ `qz3m7v` 2026-09-07T19:29+07:00 = **รอบแรกที่ K เห็นคำสั่ง** (คำสั่งลงกล่อง 18:49 · อายุ 0 รอบ ตาม `1849`) · 🔴 **ยังไม่มีเนื้อใบ**: จดหมาย `*_LANE-A-TO-K-re-body-*` สำหรับใบนี้ **ยังไม่มาถึงกล่องของ K** (เกรปทั้งกล่อง `notes_to_chief/*.md` แล้ว ณ 19:29 — ใบที่มีคือ `20260907_1849_COO-ORDER-panya1825-write-the-re-body-for-the-captain-report-frame-LANE-A.md` ซึ่งเป็นคำสั่งถึง A ไม่ใช่เนื้อใบ) ⇒ K จองเลขตามกฎ `COO-DECISION 20260907_1541` ข้อ 2 เพื่อกันเลขชนและกันงานหาย **แต่ไม่เขียนเนื้อใบแทน LANE-A** (กติกาเสมียนข้อ 3 · COO เขียนไว้เองในใบ `1849`: "ห้ามเขียนเนื้อ/นิยาม FAIL เอง ยกมาจากจดหมายของ A คำต่อคำ") · ขอบเขตที่เจ้าของ/COO เคาะไว้ (คำต่อคำจากบรรทัด "ประตู M" ใน `NOW.md` ไม่ใช่คำของ K): *"vital ขาเข้าตัวไหนเปิด `Common_Confirm` รายงานกัปตัน · layout · กด OK ส่งอะไรกลับ"* · รูปเนื้อใบที่ COO บังคับไว้ (คำต่อคำจากใบ `1849`): *"string UTF-16 → xref → handler ขาเข้า → id + layout · ผลลบต้องบอกขอบเขต"* — เนื้อใบที่ไม่ครบรูปนี้ K ตีกลับหา A ใบเดียว ไม่เติมเอง · เส้นทางที่เจ้าของเคาะ: `[STATIC-ON-BRIDGE]` (Codex runner) ⇒ **ไม่ใช่ใบ attended** ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` · แถว `RESERVED` **ไม่เข้า `QUEUE_STATUS_SNAPSHOT.md`** ตามกฎหัวไฟล์ `GAME_TEST_QUEUE.md` · นาฬิกาเนื้อใบ: **รอบที่ 0 จาก 2 ของ LANE-A** เริ่มนับ 2026-09-07T19:29+07:00] [🔵 **ADDENDUM ต่อท้ายใบโดย LANE-K รอบ `lruqz2` 2026-09-07T22:16+07:00** — LANE-A เกรป `RE-227`/`RE-265`/`RE-270` ตามที่ K ขอ แล้วแคบ objective ของใบนี้ลงเหลือเฉพาะ "ประตูที่สอง" (ประตูแรกปิดแล้วโดย `RE-265`/`RE-270`) กันไม่ให้ runner เดินพื้นที่ซ้ำ · เนื้อเต็มต่อท้าย `tickets/RE-303.md` คำต่อคำจาก `notes_to_chief/20260907_2104_LANE-A-TO-K-re-body-ADDENDUM-re303-three-closed-tickets-and-a-narrower-objective.md` · เนื้อใบเดิมไม่ถอน ไม่แก้คำเดิม]

🔴 **[addendum รอบ `qz3m7v` 20:30 · `pf-adversary` D10 · K ยืนยันเอง] เกณฑ์ตีกลับของ K ที่เขียนไว้ข้างบน "ไม่ครบ" — เติมข้อที่ขาด**: คำสั่ง COO `1849` ถึง LANE-A เขียนไว้เองว่า *"`RE-285` ปิดลบ · `RE-286` ตอบว่าไม่ใช่ตัวเปิด — **ทั้งสองใบต้องถูกอ้าง**ในหัวข้อ 'อะไรถูกตัดออกไปแล้ว'"* ⇒ เนื้อใบที่มาถึงต้องมี**หัวข้อ "อะไรถูกตัดออกไปแล้ว" ที่อ้าง `RE-285` และ `RE-286`** ไม่ใช่แค่รูปสี่ท่อน (`string UTF-16 → xref → handler ขาเข้า → id + layout`) · ไม่มี = K ตีกลับ
🔵 **ของเก่าที่ K เจอในกล่องและยกมาบอก ไม่ใช่คำตัดสินว่าซ้ำ**: `notes_to_chief/consumed/20260904_0434_LANE-A-TO-CHIEF-RE-TICKET-captain-report-frame-on-island-contact.md` (LANE-A) ถามคำถามรูปเดียวกัน *"เฟรมไหนเปิดหน้า 'รายงานกัปตัน เรือเทียบท่า [ชื่อเกาะ]' · ปุ่ม 'ยืนยัน' ส่งไบต์อะไรกลับ"* และได้เลขไปแล้วเป็น **`RE-227`** (`CLIENT_RE_QUEUE.md:571` · `primary hypothesis REFUTED-ON-SCREEN (R318 1319)` · `covered by RE-265` · archived 20260907) ⇒ **LANE-A ควรเกรป `RE-227`/`RE-265`/`RE-285`/`RE-286` ก่อนเขียนเนื้อใบ** จะได้ไม่ถาม RE runner ซ้ำในพื้นที่ที่ปิดไปแล้ว · 🔴 **K ไม่ยุบใบและไม่ตัดสินว่าซ้ำ** — ยกมาบอกอย่างเดียว
🔴 **ความผิดของเสมียนที่บันทึกไว้ตรง ๆ**: ตอนตั้งเลข `RE-302` K ตรวจใบเก่าครอบคลุมและเขียนผลไว้ในจดหมาย (`20260907_1711_LANE-K-NUMBERED-RE-302.md`) · ตอนตั้ง `RE-303` **K ข้ามขั้นนั้น** — `pf-adversary` จับได้ ไม่ใช่ K

🟢 **[LANE-K รอบ `lpjqus` 2026-09-07T20:25+07:00] เนื้อใบวางแล้ว คำต่อคำ · เกณฑ์ตีกลับที่ K ประกาศไว้เอง — ตรวจทีละข้อ ผ่านทุกข้อ**
- รูปสี่ท่อนที่ `COO-ORDER 1849` บังคับ (`string UTF-16 → xref → handler ขาเข้า → id + layout`): **มี** — หัวข้อ "วิธีที่ใบนี้ระบุ (เจ้าของกำหนดรูปไว้ ห้ามย่อ)" สี่ข้อเรียงตามนั้นตรงตัว
- หัวข้อ "อะไรถูกตัดออกไปแล้ว" ที่ต้องอ้าง `RE-285` **และ** `RE-286`: **มี** ทั้งสองใบ พร้อมสถานะและรอบที่พับ (`ek1gk9` / `73i74a`) และข้อห้ามจับคู่ `+0x3C` กับ `trigger_ordinal`
- ผลลบต้องบอกขอบเขต: **มี** หัวข้อ "nonclaim ที่ผลใบนี้ต้องเขียนไว้เอง"
- เส้นทาง `[STATIC-ON-BRIDGE]` ตามที่เจ้าของ/COO เคาะ ⇒ **ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:`** (`NOW.md` `0159`) · **ใบนี้ไม่ขึ้นรถบัส capture และไม่กินเวลาเครื่องเจ้าของ**
🔵 **สิ่งที่เจ้าของใบยังไม่ได้ทำ และ K ไม่ถือเป็นเหตุตีกลับ (บันทึกไว้ตรง ๆ ไม่ใช่คำตัดสิน)**: จดหมายเนื้อใบเขียนเมื่อ 19:32 — **ก่อน** จดหมายของ K ที่แจ้งเรื่องใบเก่า (`20260907_1958_LANE-K-TO-A-re303-reserved-for-the-captain-report-frame.md` 19:58) 26 นาที ⇒ เนื้อใบจึง **ไม่ได้อ้าง `RE-227`/`RE-265`** ซึ่ง K ยกมาบอกไว้ใน addendum ของรอบ `qz3m7v` · เกณฑ์บังคับของ COO คือ `RE-285`/`RE-286` เท่านั้น ⇒ **ผ่าน** · เรื่อง `RE-227`/`RE-265` ส่งกลับหา LANE-A เป็นจดหมาย ไม่กั้นใบ
🔴 **ความล่าช้าที่เป็นของเสมียน ไม่ใช่ของ LANE-A**: เนื้อใบมาถึง **19:32** ซึ่งเป็น **3 นาทีหลัง** จากที่รอบ `qz3m7v` เกรปกล่องแล้วไม่เจอ (19:29) · รอบนั้นไม่ได้เกรปซ้ำก่อนจบรอบ ทั้งที่บรรทัด `RECHECK:` ของแถวนี้สั่งไว้เอง ⇒ ใบค้าง **53 นาที** ที่ไม่ควรค้าง · นาฬิกาเนื้อใบของ LANE-A ปิดที่ **รอบที่ 1 จาก 2** (มาก่อนกำหนด)
🔴 K **ไม่ได้รับรอง** VA (`0x0072F700` ฯลฯ) ค่าพิกัด ชื่อคลาส หรือข้อสรุปใดในเนื้อใบ — ทุกบรรทัดเป็นของ LANE-A · หน้าที่เสมียนคือคัดลอกและวางให้ตรงที่

body: `tickets/RE-303.md` (เนื้อใบเต็ม · คำถาม 3 ข้อ / วิธี / grep แล้วเจอ-ไม่เจอ / สมมติฐาน / อะไรถูกตัดออกไปแล้ว / เกณฑ์ผ่าน / nonclaims)

owner: LANE-A (WORLD) — เจ้าของใบ · ผู้เขียนเนื้อใบ · ผู้บริโภคผล · ผู้ทำ: สาย RE (`[STATIC-ON-BRIDGE]` บนเครื่องสะพาน read-only)

result: PASS -- ตอบครบทั้งสามข้อด้วยไบต์ · สมมติฐานของเจ้าของใบถูก (notes_to_chief/20260907_2150_RE-303-RESULT-teleportcheck-0x4477-opens-confirm-22-ok-echoes-marker.md 2026-09-07T21:50+07:00) -- vital ขาเข้า = TeleportCheckVital id 0x4477 · ฟิลด์เดียว u16 tag 0x0F = MARKER.n_ID · confirm 21/22 เลือกจาก SCENE_NAME[MARKER[n_SCENE]].n_SCENE_TYPE · OK ส่งเฟรมเดิมกลับพร้อม MARKER.n_ID เดิม · Cancel ไม่ส่งอะไร -- addendum notes_to_chief/20260907_2158_RE-303-ADDENDUM-the-auto-ack-gate-that-skips-the-window.md เติมรายละเอียดประตู auto-ACK (ไม่เปลี่ยนสถานะ) -- artifact notes_to_chief/20260907_2155_RE-303-ARTIFACT-probe-sources-and-sha-for-the-captain-report-walk.md

🔴 **[แก้ 20:55 · `pf-adversary` M2 · K ทดลองเองแล้ว adversary ถูก] `RECHECK:` เดิมพิสูจน์ไม่ได้ในสิ่งที่หัวใบอ้าง** — ไฟล์ 19 ไบต์ที่มีแต่คำว่า `[STATIC-ON-BRIDGE]` ก็ผ่านโทเคนเดิม ทั้งที่สิ่งที่หัวใบอ้างคือ "คำต่อคำครบ" ⇒ เปลี่ยนเป็นโทเคนที่เทียบกับ**จดหมายต้นฉบับ**จริง
~~RECHECK เดิม: `ls tickets/RE-303.md && grep -c "STATIC-ON-BRIDGE" tickets/RE-303.md`~~ **ถอน เก็บไว้ไม่ลบ**

RECHECK (รันจากรากรีโป `pf_bridge` · ต้องพิมพ์ `VERBATIM_OK`):
```
diff <(sed -n '13,92p' notes_to_chief/20260907_1932_LANE-A-TO-K-re-body-captain-report-confirm-window.md | sed 's/RE-<เลข>/RE-303/') \
     <(awk 'NR>=10' tickets/RE-303.md) && echo VERBATIM_OK
```
ต่างแม้บรรทัดเดียว = เนื้อใบในคิวไม่ตรงกับที่เจ้าของใบเขียน ⇒ ความผิดของเสมียน แก้ที่ `tickets/` ไม่ใช่ที่จดหมาย (K รันแล้วผ่าน ณ 2026-09-07T21:0x)

> 🗂️ บรรทัด `RECHECK:` เดิมของยุค `RESERVED` เก็บไว้ตามกฎ "ห้ามลบอะไรทั้งสิ้น": RECHECK: `grep -n "RE-303" CLIENT_RE_QUEUE.md` (แถวยังอยู่) · `ls notes_to_chief/ | grep -i "LANE-A-TO-K.*re-body.*captain\|LANE-A-TO-K.*re-body.*confirm"` (ว่าง = ยังไม่มีเนื้อใบ · มีผล = K ต้องผูกเนื้อใบในรอบนั้นทันที)

## RE-305 ITEMOPERATE-OP5-VALUE32-IS-IT-THE-EQUIP-SLOT-BIT-INDEX-001  [🔧 **WIRE-HALF-DONE — พับโดย LANE-K รอบ `xsaz4f` 2026-09-07T23:13+07:00** คำต่อคำจากบรรทัด `RESULT:` ท้ายจดหมาย `notes_to_chief/20260907_2305_KA1A-R323D-RESULTS-RE305-slot-bit-table-GT288-set1-faction-green-pink.md` (ka1-A attended · Panya ที่คีย์บอร์ด R323D 2026-09-07T22:3x+07:00): "op=5 value32 = 1<<N · 13-slot bit table pinned to owner-stated slot order · drag only · client accepts any item on any slot · server reply half still open" · K คัดลอกคำของผู้ทำ **ไม่ได้ตัดสินเอง** · client→server ครึ่งสายจบแล้ว ครึ่งเซิร์ฟเวอร์ (reply) ยังเปิดเป็น `BUILD_PROPOSED` สองรายการถึง LANE-DB (ItemOperateVitalRes handler + equip slot bit-table constant) · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🟡 **READY (attended) — แต่ยัง `ตกรถ: ไม่มีโทเคน HEADLESS_PROOF`**~~ · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-DB** · ผู้ทำ: **ka1-A (attended · อ่านหน่วยความจำไคลเอนต์ตอนรัน ไม่ใช่ static)** · ตั้งเลขและวางเนื้อใบโดย LANE-K รอบ `lpjqus` 2026-09-07T20:25+07:00 = **รอบแรกที่ K เห็นคำขอ** (จดหมายเข้ากล่อง 2026-09-07T19:16) · เนื้อใบมาจาก `notes_to_chief/20260907_1916_LANE-DB-TO-K-re-body-does-op5-value32-carry-the-equip-slot-bit.md` **คำต่อคำ K ไม่แก้สำนวนแม้คำเดียว** · ออกใบตามกฎ `NOW.md` `1349` (ผลลบที่รู้สาเหตุ ⇒ ใบสร้าง/ใบ RE ในรอบที่รู้)]

> numbering [LANE-K รอบ `lpjqus`]: ดูบรรทัด numbering เต็มที่หัวใบ `GT-304` ใน `GAME_TEST_QUEUE.md` (ตัวนับร่วม `GT-`/`RE-` · สูงสุดก่อนรอบนี้ **303** ⇒ `GT-304` แล้ว `RE-305`) · ตรวจ 0 hit ของ `GT-305`/`RE-305` ครบสี่ที่ก่อนวาง
> 🔍 **ตรวจใบเก่าครอบคลุมก่อนตั้งเลข (กติกา ค.)**: `RE-280` (`0x39 IS A SHIFT BIT INDEX FF MEANS NOT EQUIPPED` · พับแล้ว) ตอบ **ฝั่งไคลเอนต์เขียนอะไรลงหน่วยความจำ** — ใบใหม่ถามสิ่งที่ `RE-280` **ไม่ได้**ตอบ คือ `value32` **บนสาย** ของ `ItemOperateVitalReq op=5` และตาราง `template_id -> n_EQUIPTYPE` · เจ้าของใบอ้าง `RE-280` ไว้เองในหัวข้อ "grep แล้ว: เจอ/ไม่เจอ" ⇒ **ไม่ยุบใบ ตั้งเลขใหม่** · 🔴 K **ไม่ตัดสิน**ว่า `RE-280` ตอบพอหรือไม่ — นั่นเป็นของเจ้าของใบกับสาย RE

🔴 **ทำไมใบนี้ยังไม่ขึ้นรถบัส capture (กฎ `PANYA-ORDER 20260907_0159`)**: บล็อก `ATTENDED:` ของเจ้าของใบเขียนบรรทัดไว้ตรง ๆ ว่า **`HEADLESS_PROOF: NONE`** พร้อมเหตุผลของเขาเองคำต่อคำ: *"ใบนี้ไม่ต้องการกลไกฝั่งเซิร์ฟเวอร์เลย มันอ่านสิ่งที่ไคลเอนต์เขียนของมันเอง (เซิร์ฟเวอร์ในรอบนี้ไม่ตอบเฟรม op=5 และใบนี้ไม่ได้ขอให้ตอบ)"* ⇒ กฎ `0159` เขียนไว้ว่า **"ไม่มีบรรทัดโทเคน = ไม่ขึ้นรถบัส"** โดยไม่มีข้อยกเว้นให้เสมียนใช้ ⇒ ใบเข้าหมวด **"ตกรถ: ไม่มี HEADLESS_PROOF"** พร้อมชื่อเจ้าของใบ
🔵 **คำถามที่เจ้าของใบส่งให้ K ตัดสิน และ K ตัดสินไม่ได้** (คำต่อคำ): *"ถ้ากติกาบ้านต้องการบรรทัด `HEADLESS_PROOF:` ที่เป็นโทเคนเสมอ ให้ตีใบนี้เป็น `[STATIC-ON-BRIDGE]` ไม่ได้ — มันไม่ใช่ static มันคือการอ่านหน่วยความจำไคลเอนต์ตอนรัน · ตัดสินเป็นของคุณ"* — 🔴 **ไม่ใช่ของเสมียน**: `0159` เป็นคำสั่งของเจ้าของโปรเจกต์ และการเปิดช่องยกเว้นใหม่ (ใบ attended ที่ไม่มีกลไกฝั่งเซิร์ฟเวอร์ให้พิสูจน์) คือการแก้กฎ ไม่ใช่การคัดลอก ⇒ K ส่งคำถามถึง COO ใบเดียว (`notes_to_chief/20260907_2039_LANE-K-ASK-COO-attended-ticket-with-no-server-mechanism-to-prove.md`) 🔴 **[แก้ 20:55 · `pf-adversary` H2]** พอยน์เตอร์เดิมเป็น glob ที่ K เขียนไว้ล่วงหน้าตอน 20:25 แล้วตั้งชื่อไฟล์จริงตอน 20:39 ไม่ตรงกัน (`attended-**ticket**-with-...`) ⇒ `ls` ตาม glob เดิมไม่เจอไฟล์ และคนอ่านจะสรุปว่า K อ้างการกระทำที่ไม่ได้ทำ — **ชื่อไฟล์เต็มแทน glob ตั้งแต่นี้ไป** และ **วางใบไว้ในหมวดตกรถระหว่างรอ** ไม่ทิ้ง ไม่ยกระดับเอง
🔴 K **ไม่ได้รับรอง** VA (`0x005833AF`/`0x005833F6`/`0x005833F9`) ค่า `8` หรือข้อสรุปใดในเนื้อใบ — ทุกบรรทัดเป็นของ LANE-DB

body: `tickets/RE-305.md` (เนื้อใบเต็ม · grep แล้วเจอ-ไม่เจอ / คำถาม 2 ข้อ / `ATTENDED:` / ทำไมคุ้มเวลาเครื่องเจ้าของ / nonclaims)

owner: LANE-DB · ผู้ทำ: ka1-A (attended) · ผู้บริโภคผล: LANE-DB

result: WIRE-HALF-DONE R323D 2026-09-07 22:3x (op=5 value32 = 1<<N · 13-slot bit table pinned to owner-stated slot order · drag only · client accepts any item on any slot · server reply half still open) -- notes_to_chief/20260907_2305_KA1A-R323D-RESULTS-RE305-slot-bit-table-GT288-set1-faction-green-pink.md

RECHECK (สองบรรทัด รันจากรากรีโป `pf_bridge`):
```
grep -c "HEADLESS_PROOF: NONE" tickets/RE-305.md          # >=1 = สถานะตกรถในหัวใบยังจริง · 0 = เจ้าของส่งโทเคนมาแล้ว K ต้องพับ+ย้ายหมวดในรอบนั้น
diff <(sed -n '10,$p' notes_to_chief/20260907_1916_LANE-DB-TO-K-re-body-does-op5-value32-carry-the-equip-slot-bit.md) \
     <(awk 'NR>=17' tickets/RE-305.md) && echo VERBATIM_OK
```
🔴 **[เพิ่ม 20:55 · `pf-adversary` M2/M1]** โทเคนเดิมเช็คแค่การมีอยู่ของสตริง ⇒ ไฟล์เปล่าที่มีคำนั้นคำเดียวก็ผ่าน · โทเคนใหม่เทียบกับจดหมายต้นฉบับจริง และ **บรรทัดที่ 17 คือจุดเริ่มเนื้อใบหลังบล็อกคำอธิบายของเสมียน** (บล็อกนั้นมีการคืนสองบรรทัดที่ K เคยตัดทิ้ง — อ่านที่หัวไฟล์ `tickets/RE-305.md`) · K รันแล้วผ่าน ณ 2026-09-07T21:0x

## RE-310 BEHAVIOUR-PREDICATE-0x0045C160-NAME-COLOUR-FIELD-READ-001  [✅ **ANSWERED (static-on-bridge)** · เนื้อใบเต็ม + ผลคำต่อคำ ย้ายไป `tickets/RE-310.md` โดย LANE-K รอบ `0511` 2026-09-08T05:11+07:00 (ใบเดิม >8,192 B ต่อใบตามเพดานจัดคิวของ K — เตรียมไว้แล้วโดยรอบ `ugr4cx` แต่ยังไม่ได้แก้หัวใบนี้จนรอบนี้) · ผลพับโดย LANE-K รอบ `ugr4cx` 2026-09-08T03:15+07:00 จาก `notes_to_chief/20260908_0032_RE-behaviour-predicate-0x0045C160-RESULT-ahead-of-numbering-LANE-K.md` · **เจ้าของใบ/ผู้บริโภคผล = LANE-B (COMBAT)**]

owner: LANE-B (COMBAT) · body: `tickets/RE-310.md` (เนื้อใบเต็ม + ผล · ย้ายออกจากคิวเพราะเกิน 8,192 B ต่อใบ)

---
## RE-311 KNOWLEDGEGURU-SHARED-PREFIX-0069F980-WRITES-BYTES-OR-NOT-001  [✅ **PASS (static-on-bridge)** · ผลพับโดย LANE-K รอบ `8qv5pm` 2026-09-08T11:24+07:00 จาก `notes_to_chief/20260908_1031_RE-311-RESULT-0069F980-writes-one-tagged-u32-all-five-resolved.md` (RE runner รอบ `RE-RUNNER-20260908_1027-OWNER-ORDERED-NO-CAP-4` · ส่งผล 2026-09-08T10:31+07:00) · สถานะเป็นคำของผู้ทำคำต่อคำ K ไม่ได้ตัดสินเอง · ผลเต็มอยู่ท้าย `tickets/RE-311.md` · **ผู้บริโภคผล = LANE-UI ยังไม่บริโภค** (จดหมายต้นทางยังไม่มี `.CONSUMED.txt`) · เปิดโดย LANE-K รอบ `0511` · เปิดโดย LANE-K รอบ `0511` 2026-09-08T05:11+07:00 · เนื้อใบเต็ม (คำถาม/anchors/grep/nonclaims) ย้ายไป `tickets/RE-311.md` เพราะเกิน 8,192 B ต่อใบ — คำต่อคำจาก `notes_to_chief/20260908_0200_LANE-UI-TO-K-re-body-knowledgeguru-shared-prefix-0069F980.md` (LANE-UI รอบ `splep7`) · `[STATIC-ON-BRIDGE]` — อ่าน client image บนเครื่องสะพาน read-only ไม่ใช่ attended ไม่มีบล็อก `ATTENDED:` ไม่ต้อง `HEADLESS_PROOF:` · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · อ้างแถวในแผน `docs/UI_LANE.md` แถวสุดท้ายของตาราง หัวข้อ `KnowledgeGuru_`]

> numbering [LANE-K รอบ `0511`]: คำสั่งค้นหาเดียวตามกฎ ② ที่หัวไฟล์นี้ (`grep -ohE '\b(GT|RE)-[0-9]{3,4}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md archive/*QUEUE*ARCHIVE*.md tickets/*.md 2>/dev/null | grep -oE '[0-9]{3,4}$' | sort -n | tail -1`) คืน **310** · เลขจองในจดหมาย (`NOW.md`/`FROM_CHIEF_*`/`COO-DECISION`/`LANE-K-NUMBERED-*`) สูงสุดก็ **309** ⇒ เลขว่างถัดไป **311** แล้ว **312** (ใบถัดไปของ LANE-UI ในรอบเดียวกัน) · ตรวจ 0 hit ของ `GT-311`/`RE-311`/`GT-312`/`RE-312` ครบทุกที่ก่อนวางทั้งคู่

owner: LANE-UI · body: `tickets/RE-311.md` (เนื้อใบเต็ม · ย้ายออกจากคิวเพราะเกิน 8,192 B ต่อใบ)

---

## RE-312 UI-EIGHT-VITALS-INBOUND-HANDLER-CENSUS-001  [🟡 **PARTIAL (bounded) → ครึ่งที่ค้างตอบแล้วใน RESULT-2 (static-on-bridge)** · ผลพับโดย LANE-K รอบ `8qv5pm` 2026-09-08T11:24+07:00 จากสองจดหมาย: `notes_to_chief/20260908_1038_RE-312-RESULT-all-eight-inbound-yes-handler-va-is-vtable-x1C.md` (สถานะคำต่อคำ **PARTIAL (bounded)**) + `notes_to_chief/20260908_1105_RE-312-RESULT-2-receive-dispatch-is-0x005F38B2-inside-the-batch-handler.md` (หัวจดหมายคำต่อคำ: "ปิดครึ่งที่ค้าง: ตัวเรียก vtable slot +0x1C คือ 0x005F38B2") · จดหมายทั้งสองไม่ได้เขียนคำว่า PASS — K ไม่ปั๊มเอง **สถานะสุดท้ายเป็นของเจ้าของใบ LANE-UI** · ผลเต็มอยู่ท้าย `tickets/RE-312.md` · **ผู้บริโภคผล = LANE-UI ยังไม่บริโภค** · เปิดโดย LANE-K รอบ `0511` · เปิดโดย LANE-K รอบ `0511` 2026-09-08T05:11+07:00 · เนื้อใบเต็ม (คำถาม/grep/เกณฑ์ผ่าน/nonclaims) ย้ายไป `tickets/RE-312.md` เพราะเกิน 8,192 B ต่อใบ — คำต่อคำจาก `notes_to_chief/20260908_0336_LANE-UI-TO-K-re-body-what-the-client-does-when-it-RECEIVES-the-eight-ui-vitals.md` (LANE-UI รอบ `gws4gs` · claim `pf_bridge#1844`) · ประเภท: static RE จาก client image ที่ commit แล้ว (ไม่ต้องบูตเกม) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · อ้างแถวในแผน `docs/UI_LANE.md` แถว `Community/Party/Trade (8 classes)` (สถานะรอบ `gws4gs`: SEAM OPEN, NOTHING ANSWERED YET) — คอลัมน์ "ขั้นถัดไป" ของแถวนั้นชี้มาที่ใบนี้โดยตรง]

> numbering [LANE-K รอบ `0511`]: ต่อจาก `RE-311` ในรอบเดียวกัน (ดูบล็อก numbering ของ `RE-311` สำหรับคำสั่งค้นหาเต็ม) · ตรวจ 0 hit ของ `RE-312`/`GT-312` แล้วในบล็อกเดียวกัน

owner: LANE-UI · body: `tickets/RE-312.md` (เนื้อใบเต็ม · ย้ายออกจากคิวเพราะเกิน 8,192 B ต่อใบ)

---

## RE-314 ACTORATTR-0X1A0-CALLER-AND-REAL-ACTOR-APPEAR-FRAME-001  [✅ **DONE/PASS — jobs 1-3 closed** พับโดย LANE-K รอบ `ci8200` 2026-09-08T17:xx+07:00 จากจดหมายผล `notes_to_chief/20260908_1552_RE-314-RESULT-UPDATEATTR-0X309A-CALLS-ACTORATTR-CODEC.md` — ผลเต็มอยู่ท้ายบล็อกนี้ · แก้ตัวสะกด route tag เป็น `[STATIC-ON-BRIDGE]` ตัวใหญ่ตามที่จดหมายผลขอ (เดิมพิมพ์ `static-on-bridge` ตัวเล็กทำ taglint หาไม่เจอ)] [🅿️ ประวัติป้ายเดิมก่อนพับ (ไม่ลบ): ~~OPEN (static-on-bridge)~~ · ตั้งเลขโดย LANE-K รอบ `lhrmkq` 2026-09-08T15:14+07:00 = รอบแรกที่ K เห็นคำสั่ง (`COO-DECISION 20260908_1341` ข้อ 3 ลงกล่อง 13:41) · เนื้อใบคำต่อคำจากคำสั่งของ COO ในจดหมายนั้น (COO เป็นผู้เขียนเนื้อใบเอง ไม่ใช่สายผู้เปิด) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = สาย RE/static — ไม่ใช่ LANE-B** (คำสั่ง COO ข้อ 3 คำต่อคำ: "ห้ามใส่เป็นเงื่อนไขของใบ attended ใบไหน — นี่เป็นงาน static ล้วน ไม่กินเวลาเจ้าของ") · ที่มา: ภาคผนวก 3 ของ `KA1A-TO-COO` (`notes_to_chief/20260908_1140_KA1A-TO-COO-B-sweep-all-addendum3-send-actorattr-0x1A0-rows-per-RE310.md` — เก้าแถว `ActorAttr +0x1A0`) **ถูกยกเลิกโดย `COO-DECISION 1341` ข้อ 2 ตาม `1934`** (LANE-B วัดแล้วว่าประกอบไม่ได้ · ผล `R324A` ตอบคำถามที่ภาคผนวกมีไว้ถามอยู่แล้ว) · **K ตรวจแล้ว: ภาคผนวก 3 ไม่เคยถูกเติมเข้า `tickets/GT-288.md` หรือคิวใดเลย ⇒ ไม่มีอะไรให้ถอน** · ใบนี้แทนที่ภาคผนวก 3 ด้วยงาน RE ล้วน~~] [🔴 **แก้โดย LANE-K รอบ `adv2k9` 2026-09-08T15:31+07:00 ตาม pf-adversary**: ข้อ 2 ของเนื้อใบมีประโยค "ต้องตอบว่าไฟล์ไหนถูก" ต่อท้ายซึ่ง**ไม่มีในจดหมายต้นทาง** (`COO-DECISION 1341` ข้อ 3 จบที่ "สองไฟล์ในรีโปขัดกันเอง") — ตัดออกแล้ว เหลือเนื้อใบคำต่อคำจริง]

> numbering [LANE-K รอบ `lhrmkq`]: คำสั่งค้นหาเดียวตามกฎ ② (`grep -ohE '\b(GT|RE)-[0-9]{3,4}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md archive/*QUEUE*ARCHIVE*.md tickets/*.md 2>/dev/null | grep -oE '[0-9]{3,4}$' | sort -n | tail -1`) คืน **313** · เลขจองในจดหมาย (`NOW.md`/`FROM_CHIEF_*`/`COO-DECISION`/`LANE-K-NUMBERED-*`) สูงสุดก็ **313** ⇒ เลขว่างถัดไป **314** · ตรวจ 0 hit ของ `GT-314`/`RE-314` ครบทุกที่ก่อนวาง

owner: RE/static (ไม่ใช่ LANE-B) · body below (เนื้อใบคำต่อคำจาก `COO-DECISION 1341` ข้อ 3)

---

## ใบนี้ตอบอะไร — สามข้อ ไม่รับคำตอบครึ่งเดียว
1. ผู้เรียกของ `0x00466230` — `RE-310` nonclaim 5 บอกว่ายังไม่ได้เดินหา · รีจิสทรีชี้ `0x0043BB80` ซึ่งเป็นสตับ `ret 8`
2. `ActorAttr@0x1A0` คือ `Navy_Pirate_icon_selector` (`PF_ATTR_FIELD_SEMANTICS.tsv` `PROVEN_EXACT` consumer `0x0046664C`) หรือเป็นตัวเลือกสีชื่อ —
   `PF_ATTR_NAME_COLOR_SELECTOR.tsv` (15 แถวของ `0x00443F50`) **ไม่มีแถว `1A0`** ⇒ สองไฟล์ในรีโปขัดกันเอง
3. ถ้าผู้เรียกไม่ใช่ `0x309A` และมีเฟรมที่ actor-appear ใช้จริง → บอกชื่อเฟรมนั้น

## ประเภทงาน
`[STATIC-ON-BRIDGE]` — อ่าน client image/registry บนเครื่องสะพาน read-only ไม่ใช่ attended ไม่มีบล็อก `ATTENDED:` และไม่ต้อง `HEADLESS_PROOF:`

## nonclaims (จากคำสั่ง COO ห้ามตัดออก)
- ไม่อ้างว่า `0x0043BB80` คือผู้เรียกจริง — เป็นแค่สิ่งที่รีจิสทรีปัจจุบันชี้ และเป็นสตับ `ret 8` ซึ่งน่าสงสัย
- ไม่อ้างว่าภาคผนวก 3 (เก้าแถว) เคยถูกใช้ตัดสินผลใดของ `GT-288` — `R324A` ปิดคำถามที่ภาคผนวกมีไว้ถามไปแล้วก่อนใบนี้เปิด

<!-- RE-314 result folded by LANE-K round ci8200 2026-09-08T17:xx+07:00 -->
## RE-314 RESULT — DONE/PASS, jobs 1-3 closed [พับโดย LANE-K รอบ `ci8200` 2026-09-08T17:xx+07:00 คำต่อคำจากบรรทัด "สถานะที่เสนอ" ของจดหมายผล `notes_to_chief/20260908_1552_RE-314-RESULT-UPDATEATTR-0X309A-CALLS-ACTORATTR-CODEC.md` (ไม่มีบรรทัด `RESULT:` แบบมาตรฐาน — ใบนี้เขียนโดยสาย RE/static ไม่ใช่ ka1-A จึงอ่านหัวข้อ "Status" แทนตามกฎข้อ 1 ของ K)]
**Status: DONE/PASS — jobs 1-3 closed** (จดหมายเขียนเอง คำต่อคำ)
- Job 1: ผู้เรียกของ `0x00466230` คือ generic attribute-container codec `[0x00463DE0,0x00463FA2)` เรียกจาก `UpdateAttrVital` serializer wrapper `0x005E42C0` — ไม่ใช่ `0x0043BB80` (สตับ `ret 8` เดิมในรีจิสทรี)
- Job 2: `ActorAttr@0x1A0` = `Navy_Pirate_icon_selector` (`PROVEN_EXACT`) ไม่ใช่ input ของ name-colour selector `0x00443F50` — สองไฟล์ในรีโปไม่ได้ขัดกันจริง เป็นคนละชั้น (semantic consumer `0x0053E8B5` vs wire sink `0x0046664C`)
- Job 3: ผู้เรียกยืนยันเป็น `UpdateAttrVital 0x309A` จริง (job 1 พิสูจน์แล้ว) · `CreateActorVital 0x36CF` ไม่ใช่เส้นทางทดแทนของ ActorAttr codec นี้
- Route note ของจดหมาย: หัวใบสะกด `static-on-bridge` ตัวเล็กทำ taglint หา tag ไม่เจอ ทั้งที่เนื้อใบมี `[STATIC-ON-BRIDGE]` อยู่แล้ว — K แก้ตัวสะกดหัวใบ RE-314 ด้านบนเป็นตัวใหญ่ให้ตรงกันแล้ว
- Nonclaims เต็มอยู่ในจดหมายต้นทาง (ไม่คัดลอกซ้ำที่นี่ตามกฎพับ = อ้างที่มา ไม่ใช่ก็อปเนื้อทั้งหมด)

<!-- RE-316 opened by LANE-K round ci8200 2026-09-08T17:23+07:00 -->
## RE-316 BIRTH-SKILL-POINTS-CHARCREATE-FIELD-VALUE-001  [🟢 **DONE/PASS (bounded negative, accepted by COO)** [STATIC-ON-BRIDGE] · ตั้งเลขโดย LANE-K รอบ `ci8200` 2026-09-08T17:23+07:00 = รอบแรกที่ K เห็นคำสั่ง (`COO-DECISION 20260908_1642_COO-DECISION-open-an-RE-ticket-for-birth-skill-points-LANE-K.md` ตอบใบ `20260908_1518_LANE-CS-TO-COO-birth-skill-points-is-an-ASSUMPTION-no-shipped-table-declares-it.md`) · เนื้อใบคำต่อคำจากคำสั่งของ COO ในจดหมายนั้น (COO เขียนเนื้อใบเอง ไม่ใช่สายผู้เปิด) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-CS** (CS ห้ามไล่ค้นซ้ำสิ่งที่ทำแล้วด้านล่าง — ทำงานแรกของตัวเองต่อ) · **ห้ามติดธง `[STATIC-ON-BRIDGE]`** (ต้องการ client image binary ซึ่งบนคลาวด์ไม่มี — ถ้าไม่มีใครมีอิมเมจ ให้ค้างในคิวตามปกติ ไม่ใช่ปิดเป็นผลลบ)] [🔴 **พับผล + แก้ป้าย route โดย LANE-K รอบ `g3nkno` 2026-09-09T14:31+07:00** ตาม `COO-DECISION 20260908_2141_COO-DECISION-fold-re316-and-normalise-its-route-metadata-LANE-K.md` คำต่อคำจากบรรทัด `RESULT:`/หัวจดหมาย `notes_to_chief/20260908_2115_RE-316-RESULT-CHARCREATE-DOES-NOT-WRITE-SKILL-POINTS.md`: "CharCreate/CreateChar send path เขียนฟิลด์แต้มสกิลไม่ได้เลย — `ActorAttr+0x7C` ไม่ได้ถูกส่งมาในคำขอสร้างตัวละคร" · K คัดลอกคำของผู้ทำ ไม่ได้ตัดสินเอง · 🔴 **แก้ป้ายย้อนหลัง**: หัวใบเดิม (บรรทัดบน) เขียนห้ามติดธง `[STATIC-ON-BRIDGE]` เพราะตอนตั้งเลข คลาวด์ไม่มีอิมเมจไคลเอนต์ — แต่ผู้รันจริงอยู่บนสะพาน มีอิมเมจปักหมุดแล้ว (ใบไม่ใช่ attended) COO สั่งให้ป้ายตรงกับร้อยแก้ว (taglint อ่านป้าย ไม่อ่านย่อหน้า) ⇒ เติมธงนี้ ณ ตอนพับ ไม่ใช่ตอนตั้งเลข · 🔴 **`BIRTH_SKILL_POINTS` ยังคงป้าย `ASSUMPTION` ห้ามเขียน `MEASURED`** — ผลนี้บอกว่าวัดจากไคลเอนต์ไม่ได้ ไม่ใช่ว่าวัดได้แล้วเป็น 0]

> numbering [LANE-K รอบ `ci8200`]: คำสั่งค้นหาเดียวตามกฎ ② (`grep -ohE '\b(GT|RE)-[0-9]{3,4}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md archive/*QUEUE*ARCHIVE*.md tickets/*.md notes_to_chief/*.md 2>/dev/null | grep -oE '[0-9]{3,4}$' | sort -n | tail -1`) คืน **315** (เพราะ `GT-315` ตั้งไปแล้วในรอบเดียวกันก่อนหน้านี้) ⇒ เลขว่างถัดไป **316** · ตรวจ 0 hit ของ `GT-316`/`RE-316` ครบทุกที่ก่อนวาง

owner: LANE-CS (ตอบ) · ตั้งเลข/วางคิว = LANE-K · body below (เนื้อใบคำต่อคำจาก `COO-DECISION 1642`)

---

## คำถามของใบ (คำเดียว ห้ามขยาย)
ไคลเอนต์/เซิร์ฟเวอร์ต้นฉบับให้ตัวละครที่เพิ่งสร้างถือแต้มสกิลเท่าไร — ฟิลด์ไหนในบล็อกตัวละครที่เส้นทาง `CharCreate`/`CreateChar` เขียนตอนสร้าง

## ที่ CS ไล่แล้วและไม่เจอ (ใส่ลงใบ เพื่อไม่ให้ใครไล่ซ้ำ)
- หัวตาราง `CONSTDATA_TH__CHARCREATE_{CLASS,PACKAGE,LOOK,SKIN}` ครบทีละคอลัมน์ — ไม่มีคอลัมน์แต้มสกิล (`s_SKILL_1..4` = รหัสสกิลเกิด ไม่ใช่จำนวนแต้ม)
- `gamedata/tables/*.tsv` ทุกใบที่มี `SP`/`SKILL_POINT`: `n_SP` · `n_QUEST_SP` · `n_PVP_SP` · `f_SP` · `f_REWARD_SP` · `f_RATIO_SP` · `n_Get_GuildSkill_Point_at_GuildLV*` — **ทุกตัวเป็นต่อเลเวล/ต่อมอน/ต่อเควส/กิลด์/PVP ไม่มีตัวไหนแปลว่าค่าเกิด**
- grep ครบสี่ที่ตาม §7: `external/` · `archive/` · `notes_to_chief/consumed/` · `gamedata/tables/` — ไม่เจอ
- `SetSkillPoint` ไม่ปรากฏใน `gamedata/` ทั้งไดเรกทอรี มีแต่ `AddSkillPoint`/`Quest.AddCriteriaSkillPoint`/`AddLvCriteriaSkillPoint`

## ที่ยังไม่ได้ไล่ และเป็นเนื้อของใบ
เส้นทาง `CharCreate`/`CreateChar` ในอิมเมจไคลเอนต์ — ต้องมี binary ⇒ ใบนี้ **ห้ามติดธง `[STATIC-ON-BRIDGE]`** ว่าตอบได้บนคลาวด์ ถ้าไม่มีใครมีอิมเมจ ให้ค้างในคิวตามปกติ ไม่ใช่ปิดเป็นผลลบ

## ประเภทงาน
ต้องการ client image binary (ไม่มีบนคลาวด์) — ค้างในคิวจนกว่าจะมีผู้เข้าถึงอิมเมจ · ไม่ใช่ attended ไม่มีบล็อก `ATTENDED:` และไม่ต้อง `HEADLESS_PROOF:`

## ใครทำอะไรต่อ
CS แก้สองบรรทัด (`BIRTH_SKILL_POINTS` + ป้ายเป็น `MEASURED` พร้อมชื่อตาราง) เมื่อใบนี้ตอบ — ประตู `birth_skill_points()` จะบังคับให้แก้ครบเอง · CS **ห้ามไล่ซ้ำ** สิ่งที่บันทึกไว้ข้างบนแล้ว

## nonclaims
- ไม่อ้างว่าไม่มีค่าเกิดจริง — เพียงแค่ยังไม่พบตารางที่ shipped ประกาศไว้หลังไล่ครบสี่ที่
- ไม่อ้างว่า `s_SKILL_1..4` แปลว่าแต้มสกิล — เป็นรหัสสกิลเกิด คนละความหมาย
- ไม่อ้างว่า CS ทำงานผิด — CS ไล่ครบตามที่ COO สั่งแล้วไม่เจอจริง

## RE-321 NPCATTR-0X7C-EIGHT-UNWALKED-AVT-XREFS-READER-001  [🟢 **DONE/PASS — STATIC-ON-BRIDGE** (พับโดย COO แทน LANE-K (HOLD `1705`) 2026-09-09T17:25+07:00 จาก `notes_to_chief/20260909_1343_RE-321-RESULT-npcattr-7c-feeds-final-avt-xref-whole.md` · ผลบอกเอง "complete 8/8; no incomplete source path" · BUILD_PROPOSED → LANE-B) · เดิม: 🅿️ OPEN — assigned LANE-B · `STATIC-ON-BRIDGE` (ไม่ใช่ `STATIC-ON-CLOUD` — ต้องมีอิมเมจไคลเอนต์ ซึ่งไม่มีบนโคลนคลาวด์) · ตั้งเลขโดย LANE-K รอบ `vgaj0v` 2026-09-08T21:37+07:00 = รอบแรกที่ K เห็นคำสั่ง (คำขอเข้ากล่อง 21:15 · อนุมัติ `COO-DECISION 20260908_2055_COO-DECISION-the-eight-unwalked-avt-xrefs-get-an-re-ticket-send-k-the-body-LANE-B.md`) · เนื้อใบคำต่อคำจาก `notes_to_chief/20260908_2115_LANE-B-TO-K-re-body-the-eight-unwalked-avt-xrefs.md` K ไม่แก้สำนวนแม้คำเดียว · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-B**]

> numbering [LANE-K รอบ `vgaj0v`]: คำสั่งค้นหาเดียวตามกฎ ② ที่หัว `GAME_TEST_QUEUE.md` (`grep -ohE '\b(GT|RE)-[0-9]{3,4}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md archive/*QUEUE*ARCHIVE*.md tickets/*.md notes_to_chief/*.md 2>/dev/null | grep -oE '[0-9]{3,4}$' | sort -n | tail -1`) คืน **320** ⇒ เลขว่างถัดไป **321** · ตรวจ 0 hit ของ `GT-321`/`RE-321` ครบทุกที่ (คิวสองไฟล์ · `archive/` · `tickets/` · กล่องจดหมาย) ก่อนวาง

owner: LANE-B (เจ้าของใบ/เขียนเนื้อใบ/บริโภคผล) · ตั้งเลข/วางคิว = LANE-K · body below (เนื้อใบคำต่อคำจากจดหมาย `20260908_2115`)

---

**ชื่อใบ:** wstr ที่เซิร์ฟเวอร์เขียนที่ `NPCAttr+0x7C` — ฝั่งไคลเอนต์ใครอ่าน และอ่านทั้งสตริงหรือโทเคนแรก
**เจ้าของใบ:** LANE-B · **เส้นทาง:** `STATIC-ON-BRIDGE` · **ไม่ต้องเปิดเกม ไม่ต้องใช้จอ ไม่กินคิวเครื่องเทส**

### ทำไมต้องมีใบนี้
วันนี้ในทรีมีประโยคที่ยืนอยู่โดย **ไม่มีการวัดรองรับ**: "เซิร์ฟเวอร์ส่งเบสเนมเดียวเพราะไคลเอนต์อ่านโทเคนแรก"
สิ่งที่วัดแล้วจริง ๆ คือ `RE-296` ผล 2 (2026-09-07T20:53 · PASS/BOUNDED-POSITIVE) อ่านฟังก์ชันที่ `0x0059A7A0`:
ไคลเอนต์โหลดแถว `MOBS.s_OUTFIT` **ของตัวเอง** แล้ว tokenise แล้ว push ค่า `0` ที่ `0x0059AA52` เพื่อเอาโทเคนแรก
นั่นคือการวัดว่า **ไคลเอนต์อ่านตารางของตัวเองยังไง** — ไม่ใช่การวัดว่าไคลเอนต์ทำอะไรกับ wstr ที่เซิร์ฟเวอร์เขียนลง `NPCAttr+0x7C`
และ nonclaim 2 ของผลใบเดียวกันเขียนเองว่า เดิน `%s%s.avt` xref ไปแค่ **5 จาก 13** ⇒ เหลือ **8 เส้นที่ไม่มีใครเดิน**

### สิ่งที่ขอให้ทำ
เดิน `%s%s.avt` xref ที่เหลืออีก 8 เส้น ไปให้ถึงสตริงต้นทาง แล้วตอบสามข้อ:
- **(ก)** มีเส้นไหนอ่าน wstr ที่ `NPCAttr+0x7C` ไหม
- **(ข)** ถ้ามี มัน tokenise หรือใช้ทั้งสตริง
- **(ค)** ถ้าไม่มีเลย แปลว่าฟิลด์นั้นไปทางอื่น — ทางไหน

### grep แล้วก่อนออกใบ (ตามกฎแผนที่โปรโตคอลใน `COMMON_LANE_ROUND.md`)
- `external/PF_SERIALIZER_FIELDS.tsv`: **เจอ** layout ของ `NPCAttr` — แต่ **ไม่เจอ** แถวไหนที่บอกว่าใครอ่านฟิลด์ `0x7C` ฝั่งไคลเอนต์
- `external/PF_PROTOCOL_REGISTRY.tsv`: **เจอ** คลาส/serializer — **ไม่เจอ** ผู้อ่านฝั่งไคลเอนต์ของฟิลด์นี้
⇒ สิ่งที่ต้องการคือ **ผู้อ่าน (reader)** ไม่ใช่ layout · layout มีแล้ว ใบนี้จึงไม่ซ้ำกับสิ่งที่ตอบได้จาก artifact ที่ commit แล้ว

### เกณฑ์ปิดใบ
ปิดได้เมื่อทั้งสามข้อมีคำตอบ **พร้อม VA ของแต่ละเส้นที่เดิน** และระบุชัดว่าเส้นไหนเดินจบ เส้นไหนเดินไม่จบเพราะอะไร
ผลลบ (= ไม่มีเส้นไหนอ่าน `0x7C` เลย) **เป็นผลที่รับได้และมีค่า** — แต่ต้องมาพร้อมคำตอบข้อ (ค)

### BUILD_IMPACT ถ้าคำตอบออกมาว่า "ไคลเอนต์ใช้ทั้งสตริง"
ต้องย้อน **ข้อมูลในตารางเดียว** (regenerate `field_mob_tables_bg0002.py` ใหม่ด้วย `--outfit-rule any`) ไม่ใช่โครงสร้าง
⇒ ราคาย้อนต่ำ · **ใบนี้ไม่บล็อกใคร** และห้ามใครใช้ใบนี้เป็นเหตุผลหยุดงาน (COO `2055` ข้อ 4)

### NONCLAIMS ของใบนี้
- ใบนี้ **ไม่ถาม** ว่าเบสเนมชี้ไปยังไฟล์ที่ ship จริงไหม — ไม่มีใครฝั่งเซิร์ฟเวอร์ตอบได้ และไม่ใช่คำถามนี้
- ใบนี้ **ไม่ถาม** ว่าใครเป็นศัตรู — นั่นคือ `n_RANK` + `n_AI_COMBAT` และไม่มีอย่างอื่น (PANYA `1313`)
- ใบนี้ **ไม่ได้อ้าง** ว่าวันนี้มีบอดี้วาดไม่ขึ้น — ยังไม่มีใครวัดเรื่องนั้น การส่งเบสเนมเดียวเป็นคำสั่ง COO-DECISION `2026-09-08T17:42` ไม่ใช่ข้อสรุปจากการวัดฝั่งไคลเอนต์

### result — พับคำต่อคำจาก `notes_to_chief/20260909_1343_RE-321-RESULT-npcattr-7c-feeds-final-avt-xref-whole.md` โดย COO แทน LANE-K (HOLD `1705`) 2026-09-09T17:25+07:00
RESULT: **DONE/PASS — STATIC-ON-BRIDGE** — all eight previously unwalked `%s%s.avt` xrefs were walked to their source strings.

## Direct answer

**(a) Yes.** Exactly one of the eight remaining xrefs reaches the `basic_string<wchar_t>` at `NPCAttr+0x7C`: the `%s%s.avt` use whose literal dword is at **VA `0x0078AB08` / file offset `0x00389F08`** (the `push` starts at `0x0078AB07`).

The complete same-object chain is:

1. `NPCAttr` binds to `CNetNPC+0x358` at `0x004697DD..0x004697EB`.
2. `0x0045DB4E` loads `[CNetNPC+0x358]`; `0x0045DB54` takes `NPCAttr+0x7C`; `0x0045DB58..0x0045DB5B` assigns the full wstring to presentation descriptor `+0x60`.
3. The descriptor constructor at `0x0045C220` installs vtable `0x00F0DF3C`; vtable slot `+0x14` at `0x00F0DF50` is `0x0078AA50`.
4. `0x0078AAF4` takes `c_str()` directly from descriptor `+0x60`; `0x0078AAFD` pushes that pointer as the second `%s`; `0x0078AB07` pushes `L"%s%s.avt"`; `0x0078AB0D` formats the path.

**(b) The `.avt` path uses the whole wire string as its basename.** There is no semicolon, tab, or space tokenizer between descriptor `+0x60` and the format call. A list cell such as `A;B` would therefore be formatted literally as `.\Data\GC\V\A;B.avt`, not reduced to `A` at this xref.

The same upstream function also splits `NPCAttr+0x7C` on underscore (`L"_"` at `0x00F0E07C`) at `0x0045DB61..0x0045DB96`, takes token index 0, and assigns that separate result to `CNetNPC+0x338` at `0x0045DB9C..0x0045DBA2`. That token does **not** feed the `.avt` format: the `.avt` vfunc reads the earlier full copy at descriptor `+0x60`.

Question (c) does not apply because a positive reader was found. The actual route is nevertheless pinned above so the field does not remain an unexplained wire value.

## Build consequence

The existing single-basename wire rule is now backed by the actual `NPCAttr+0x7C` consumer: a raw multi-value cell must be reduced before it is written to this field. The client does not split `;`, tab, or space on the `.avt` route.

BUILD_PROPOSED: replace the RE-321-open wording in `mob_avatar_basename.py` and generated roster provenance with this static proof while retaining the existing single-basename wire guard | LANE-B (COMBAT) | `py -3 -m pytest tests/test_mob_avatar_basename.py -q`

## nonclaims

1. This does not prove which basename a server should select from a multi-value `s_OUTFIT` cell; it proves only that `NPCAttr+0x7C` must already contain the one complete basename the client will use. RE-296 separately proves index 0 for the client's own `MOBS.s_OUTFIT` table path.
2. This does not claim the internal `+0x28` or `+0xF8` fields belong to `NPCAttr`; their concrete classes remain unnamed here.
3. This does not claim every `.avt` path in the image comes from `NPCAttr`; seven of these eight do not.
4. The underscore split in `0x0045DAE0` feeds `CNetNPC+0x338`; it is not evidence that the `.avt` basename is underscore token 0.
5. This is static IMAGE evidence only. It does not prove that any particular basename exists on disk, renders a body, or matches a server-side gameplay choice.

(ตารางสำมะโน 8 เส้น + proof spans 14 แถว + trap test อยู่ในจดหมายต้นฉบับ ไม่คัดลอกซ้ำ — sha256 จดหมาย = 300d592899afadd40c41ef1467399ba8fb266d6b8078cb661466768af267e39f)
