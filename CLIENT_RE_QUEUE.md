# CLIENT RE QUEUE — คิวงานแกะไคลเอนต์/capture (static · ไม่เปิดเกม)

> **ไฟล์นี้เกิดจากคำสั่ง Panya 18:22 (+07:00) 2026-08-23** (`notes_to_chief/20260823_1822_PANYA-ORDER-split-queue-into-two-and-search-RE-deliverable-first.md`)
> — แยกใบ **แกะไคลเอนต์/capture** ออกจากคิวเทสเกม **ตั้งแต่ใบใหม่เป็นต้นไป** (ใบ static เก่า GT-040/042/044/046/047/048/049
> ยังอยู่ใน `GAME_TEST_QUEUE.md` ตามกติกาห้ามย้ายใบเก่า — สารบัญหัวไฟล์นั้นเป็นตัวเชื่อม)

**ผู้รับงาน:** คนหน้าเครื่องสะพานของ Panya (มีอิมเมจ client + capture + ไฟล์ข้อมูลเกมบนดิสก์) — **ไม่ใช่ผู้เทสหน้าจอเกม**
**กติกาไฟล์นี้:**
- ทุกใบในไฟล์นี้ **ไม่ต้องเปิดเกม · ไม่ต้องจับ `LOCK_GAME` · ไม่มี teardown · ไม่แตะ canonical DB · ไม่มีอะไรให้ดูบนจอเกมเลย**
  ⇒ ทำขนานกับรอบเทสเกมได้เสมอ ไม่แย่งทรัพยากรกัน
- 🔤 **ตัวนับเลขเป็นชุดเดียวกับ `GAME_TEST_QUEUE.md` ต่อเนื่องกัน ห้ามแยกตัวนับ** (การอ้างข้ามใบต้องไม่พัง) ·
  **แต่ใบใหม่ในไฟล์นี้ใช้ prefix `RE-` ตั้งแต่ใบ 056 เป็นต้นไป** (คำสั่ง Panya 2026-08-24 ~00:2x · จดหมาย `20260824_0025_*`) ·
  ใบเก่า **GT-050/052/053/054/055 คงชื่อเดิมตลอดกาล** — จดหมายสั่ง "เริ่มที่ 055" แต่ใบ 055 ถูกออกเป็น `GT-055` ใน R134
  ก่อนคำสั่งถึงมือ chief ⇒ ตามกฎห้ามเปลี่ยนชื่อใบที่ commit แล้ว จุดเริ่มจริงของ prefix ใหม่คือ **056**
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
- ผลส่งกลับทางเดิม: จดหมายใน `notes_to_chief/` + กรอกช่อง **result:** ท้ายใบ · sha ก่อน-หลังของทุกไฟล์ที่พึ่งต้องตรงกัน

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
**สถานะ (R135 · 2026-08-24 ~08:4x +07:00):** ✅ **ปิดแล้ว 3 ใบ — GT-054 PASS (392/392) · GT-053 PASS (H1 รอด) · GT-052 PASS** (ผลหน้าสะพาน 00:33/00:38/00:44 +07:00) · 🟡 **GT-050 PARTIAL** (00:55: จ็อบ 1–3 ปิด · `CLearnSkillResultVital` codec CLOSED · direction ของ `TriggerCastSkillVital` ชนเพดาน static — ทางต่อเป็น observe-only attended) · **เหลือเปิดจริง: GT-055 ใบเดียว** · 📦 ของใหม่บนสะพาน (จดหมาย 0055 อีกใบ): `gamedata\lua\` 616 ไฟล์ + `gamedata\scene\` 289 placement TSV — ยังไม่เข้า git · correction: u16@0x2 ของ `.npc` = definition_count ไม่ใช่ placement_count (bg0001: def 113 / actual 149) · Bg0002 actual = 106 **ตรงกับ GT-053 โดยอิสระ** ✓
**สถานะ (R136 · 2026-08-24):** ✅ `gamedata\lua\`+`scene\`+API spec **เข้า git แล้ว** (commit `0801541`) · 🆕 **RE-056 SKILLCAST-DIRECTION-002** เปิดท้ายไฟล์ (ตามร่างจดหมาย 0126 — เลขขยับจาก RE-055 เพราะ 055 ถูก GT-055 ใช้แล้ว) · ⏳ external/ ยังอยู่ที่ **5/8 ตาราง** — สามตาราง (`PF_PROTOCOL_PRIORITY` · `PF_DATA_EVIDENCE` · `PF_TAG_CENSUS`) ยังรอคนหน้าสะพาน `git add` (ตามจดหมาย `FROM_CHIEF_R131_*`)
**สถานะ (R137 · 2026-08-24 ~03:0x +07:00):** 🆕 **RE-057 PLACEMENT-INDEX-CROSSWALK-001** เปิดท้ายไฟล์ (Panya เลือก "ทาง ก." จดหมาย 0159 · ร่างเดิมใช้เลข 056 — ขยับเป็น 057 เพราะ 056 ถูก SKILLCAST-DIRECTION-002 ใช้แล้วใน R136) · จ็อบ crosswalk-ในตาราง-commit ของร่างถูกปิดบน cloud แล้ว: **ทั้ง 188 ตารางไม่มีตารางไหนอ้างสคริปต์ที่เรียก `PlacementOFF` เลย (grep ด้วยชื่อไฟล์ — การอ้างด้วย ID ตัวเลขยังตัดไม่ได้จนกว่าจะมี map ชื่อ→ID จากอิมเมจ)** (crosswalk เดียวที่มีคือ `QUEST.s_LUASCRIPT` — ครอบเฉพาะสาย `Quest/`) — ดู `FINDINGS_R137_QUEST_CROSSWALK_HUNT.md` · Panya ยืนยันซ้ำ (จดหมาย 0159 ข้อ ①): **GT-055 ไม่ต้องเปลี่ยนชื่อ** — จุดเริ่ม `RE-` คือ 056 ตามที่หัวไฟล์เขียนไว้แล้ว · ใบเปิดจริงตอนนี้: **GT-055 · RE-056 · RE-057 · RE-058** *(+RE-058 — เติมเข้าบรรทัดนี้โดย R140 ไม่ใช่ของเดิม R137 · กำกับโดย R141 ตาม adversary D5)*
**สถานะ (R140 · 2026-08-24 ~06:xx +07:00):** 🆕 **RE-058 LEARNSKILL-DIRECTION-001** เปิดท้ายไฟล์ — direction census
ของ `CLearnSkillVital 0x36AA` (ครึ่งหลักฐานของเลนโค้ด LEARN-SKILL-REQUEST-001 / HYP-PF-034 ที่ R140 เปิด —
decoder ฝั่ง server ยืนบน W codec ที่ commit แล้ว แต่ยังไม่มีใครพิสูจน์ว่า client ส่งจริง)
**สถานะ (R141 · 2026-08-24 ~07:0x +07:00):** 📎 เลนโค้ดที่ RE-058 อ้างถึง **merge เข้า `main` แล้ว** — PR #15
(head `7613ad8`) เขียว(Actions run 32674183978 · subset · อ่านทาง D ci-status) · merge `de3ecef` · re-derive
บน main clone เขียว(cloud sanity 2017/324/0 · ledger PASS entries=42) ⇒ ใบ RE-058 ตัวมันเองไม่เคยติด merge
(งาน static บนอิมเมจล้วน) แต่ผลของใบนี้จะถูก chief ใช้แก้สถานะ nonclaim ของ **HYP-PF-034 ที่อยู่บน main แล้ว** —
ผู้รับงานกรอกผลตามใบได้เลย ไม่ต้องรออะไรอีก
**สถานะ (R143 · 2026-08-24 ~09:xx +07:00):** ✅ **GT-055 PASS/DONE** (ผลหน้าสะพาน 02:41: `0x36DB` = **string8** tag `0x44` + uint32le byte_len · `0xAC52` = UTF-16LE tag `0x48` · ป้าย `UNTAGGED_*` = ขอบเขต helper ของ serializer body ไม่ใช่ full-wire absence claim) ⇒ **parser เราผิดจริงฝั่ง `0x36DB`** — chief แก้ในรอบเดียวกัน (`opaque_string8` + เลิกบังคับความยาวคู่ + dated amendment HYP-PF-015/021 รวม 5 จุด) · สถานะโค้ด ณ ตอนเขียน: **PR โค้ด #16 (commit `fa1e804`) เปิดแล้ว รอ gate — ยังไม่เข้า `main`** · merge อัตโนมัติเมื่อเขียว · ถ้ารอบหน้าไม่เห็น merge ให้เช็ค PR #16 (branch `claude/amazing-goodall-mmtl2a` — งานอยู่บน branch ครบแม้ PR ถูกปิด) · ✅ **RE-056 DONE/METHOD-FAIL** (ผล 07:28: registrar `0x5F3DF0` = inbound prototype tree สำหรับ `CreateById` — จำแนก outbound ไม่ได้ ตกที่ control ⇒ เลน static ของ direction **ปิดถาวรตามเกณฑ์จบใบ** · direction `TriggerCastSkillVital` **ยังไม่ตัดสิน** · ทางต่อ = observe-only attended ตาม checkpoint `PF_SKILL001_...20260816.md` — พักตามคำสั่ง 16:56) · **ใบเปิดจริงตอนนี้: RE-057 · RE-058**

**สถานะ (R145 · 2026-08-24 ~11:xx +07:00):** ✅ **RE-057 DONE/STATIC-LANE-CLOSED** + ✅ **RE-058 DONE/BOUNDED-NEGATIVE** (ปิดโดย R144 — ป้ายอยู่บนหัวใบทั้งสองแล้ว) ⇒ **คิวนี้ไม่มีใบเปิดค้างเลยชั่วขณะ** · 🆕 เปิดใหม่สองใบท้ายไฟล์ **ทั้งคู่อยู่บนเลนลูท (loot lane)** ซึ่งเป็นเลนเดียวที่มี "ของจริงรออยู่แล้ว" ไม่ต้องไปถอดใหม่:
  · 🆕 **RE-059 ITEMOPERATE-RES-CAPTURE-BYTES-001** — `PF_FIELD_VALIDATION.tsv` แถว `ItemOperateVitalRes:R` บอกว่ามี **เฟรมจริง 5 เฟรมใน 4 ไฟล์ capture** บนสะพาน · `parse_success=0` แต่ 🔴 **`mismatch_frames=0`** ⇒ "ถอดไม่ได้" ไม่ใช่ "ขัดกัน" · ใบนี้ไปเอา **ไบต์ดิบ** ออกมา ไม่ใช่ไปถอด serializer ซ้ำ (GT-054 verify span ให้แล้ว 392/392)
  · 🆕 **RE-060 ITEM-TEMPLATE-CODE-SCHEMA-001** — คอมเมนต์ `current/pf_login_game_server_v141.py:2470` (`2600001 # STORE_NORMAL row 1 -> ITEM_MISC row 1`) **ผิดอย่างน้อยสองจุด** (พบโดยลูกมือ static) · ใบนี้ pin สคีม `<table_code><5 หลัก>` ด้วยหลักฐาน · 🔴 `current/` เป็น v141 immutable — ใบนี้ **หาหลักฐาน ไม่ใช่แก้โค้ด**
  · 📎 หมายเหตุข้ามใบ: **RE-060 เป็น precondition เชิงความหมายของ RE-059 แต่ไม่ใช่ precondition เชิงเทคนิค** — รันขนานกันได้ ไม่ต้องรอกัน · 📌 ที่มาของคำตอบเลนลูท: `ItemOperateVitalRes 0x4C13` encoder มีอยู่แล้วใน `pirate-force-server/src/pirateforce_foundation/inventory.py` 3 ทรง ⇒ ไม่เปิดเลนโค้ดใหม่

**สถานะ (R146 · 2026-08-24 ~11:5x +07:00):** 🆕 เปิด **RE-061 SKILLSTATE-WIRE-DIRECTION-001** (ท้ายไฟล์) — prerequisite ของเลนโค้ด skill-state sender ที่จะปลดล็อก GT-058 (หน้าต่างสกิลเปิดไม่ได้) · pf-static-re R146 ยืนยัน **NEEDS-BRIDGE-IMAGE**: `CSkillModule`/`CSkillAttr` serializer row = EMPTY, capture = NOT_OBSERVED, id `0x1F7B`/`0x1661` = name-hash candidate ไม่ใช่ opcode ⇒ ปิด wire+direction จากอิมเมจเท่านั้น · **ใบเปิดจริงตอนนี้: RE-059 · RE-060 · RE-061**

**สถานะ (R149 · 2026-08-24 ~22:xx +07:00):** ✅ **ปิดครบสามใบในวันเดียว — RE-059 · RE-060 · RE-061 DONE ทั้งหมด** (ผลเต็มอยู่ในบล็อกของแต่ละใบท้ายไฟล์) · RE-061 ออกทาง **บวก**: `CSkillAttr` ขี่ `UpdateAttrVital 0x309A` class_id `0x1661` + gate หน้าต่าง Skill พิสูจน์จากอิมเมจ ⇒ **chief เปิดเลนโค้ด sender แล้วในรอบเดียวกัน** (opt-in · headless proof · ดู `GAME_TEST_QUEUE.md` ใบเทสใหม่ GT-059) · 🆕 เปิด **RE-062 SKILLATTR-BIND-NULL-BRANCH-001** (ท้ายไฟล์ — คำถามเปิดจาก pf-adversary: inbound `0x1661` **สร้าง** container ที่ `[actor+0x3E8]` ได้ไหมตอน null · กุญแจอ่านผลลบของ GT-059) · **ใบเปิดจริงตอนนี้: RE-062 ใบเดียว**

**สถานะ (R152 · 2026-08-24 ~18:2x +07:00):** ✅ **RE-062 DONE** (ผลหน้าสะพาน 17:01 +07:00 · จดหมาย `notes_to_chief\20260824_1701_RE-062-RESULT-INBOUND-OTHER-PATH-NO-SLOT-WRITE.md`) — คำตอบ **(ค) เส้นทางอื่น**: inbound สร้าง `CSkillAttr` ชั่วคราวได้ผ่าน factory แต่ resolve/insert ลง **generic attribute map** ด้วย class id `0x1661` เท่านั้น · **ไม่มีแขนงใดเขียน `[actor+0x3E8]`** (slot มาจาก `CMyActor` ctor · bind ตอน null = no-op ไม่ repair) ⇒ กุญแจอ่านผลลบ GT-059 พร้อมแล้ว (ดูใบ GT-059 ใน `GAME_TEST_QUEUE.md` — อัปเดต R152) · **ไฟล์นี้ไม่มีใบเปิดค้างแล้ว — 0 ใบ**

**สถานะ (R154 · 2026-08-24 ~20:xx +07:00):** 🆕 เปิด **RE-064 ITEMOPERATE-RES-AFFECTED-ELEMENT-SHAPE-001** (ท้ายไฟล์) — ชี้ขาดทรง per-element ของ `0x4C13` ตอน `affected_identity_count>0` (R13 `0x005ED2F0` อยู่ใน loop ไหม) · เหตุ: chief R154 เปิดเลนโค้ด GT-063 (HYP-PF-037) โดยตรึง count=0 ทุกเฟรมเพราะทรงนี้ยังเปิด — ปิดใบนี้ = ปลดล็อก sweep variant count>0 · **ใบเปิดจริงตอนนี้: RE-064 ใบเดียว**

**สถานะ (R156 · 2026-08-25 ~00:0x +07:00):** ✅ **RE-064 DONE — PINNED** (ผลหน้าสะพาน 2026-08-24 22:41 +07:00 · จดหมาย `notes_to_chief\20260824_2241_RE-064-RESULT-R13-INSIDE-LOOP-PREDICTION-FALSIFIED.md`) — element = tag `0x32` กว้าง 8 แล้ว tag `0x08` กว้าง 1 · R13 `0x005ED2F0` = **INSIDE loop** และเป็น collection-insert helper (ไม่กิน wire tag — คำทำนาย TRAILER **ผิด**) · count R10 อ่านเป็น u8 tag `0x08` มี signed initial gate · rider 15-byte PC prefix: **IDENTICAL 15/15** (capture PC #101 vs v141 candidate) ⇒ ErrorData บน control frame ของ GT-063 จะชี้ session context ไม่ใช่ envelope prefix · chief R156 บันทึกลง ledger HYP-PF-037 แล้ว (3 ฟิลด์ · re-pin canonical sha 5629F715 · ผ่าน pf-adversary — 3 defect แก้ครบก่อน commit) · 🔴 **ยังไม่ compose เฟรม count>0** — stop_rule + expiry decision ของ ledger บังคับรอผลตา GT-063 + คำเคาะ Panya ก่อนเปิด NEW VERSION (คำถามเสนอ Panya อยู่ในจดหมาย R156) · **ใบเปิดจริงตอนนี้: 0 ใบ**

**สถานะ (R161 · 2026-08-25 ~09:5x +07:00):** ✅ **RE-066 ปิดแล้วเป็น DONE/PASS — YES · T2 หักล้าง · T1 ทดสอบได้** (ผลกลับ 09:38 +07:00 · บล็อก **result** ท้ายไฟล์)
⇒ 🟢 **ใบ static เปิดอยู่ตอนนี้ = 0 ใบ** · ของแถมที่ได้มาฟรี: **ใน concrete inbound graph ของ list `0x5F85B0`** ไคลเอนต์เปิดอ่าน **`n_DROPMODEL_TYPE`** และ **ไม่มี named lookup ของ `n_ID_MODEL`**
🔴 **ขอบเขตนี้ตัดทิ้งไม่ได้** — ใบไม่ได้อ้างว่า `n_ID_MODEL` ไม่ถูกอ่านที่อื่นในโปรแกรม และ **ไม่ได้อ้างว่าฟิลด์ไหนเป็นตัวขับการวาดโมเดล**
*(สถานะเดิม R158 · 2026-08-25 ~08:0x: ✅ RE-065 ปิดแล้วเป็น DONE/YES (static) พร้อม erratum ต่อ factpack R100 · 🆕 เปิด RE-066 หนึ่งใบ ⇒ ใบเปิดจริงตอนนั้น: RE-066 ใบเดียว)*
> RE-066 ไม่ได้เปิดเพื่อหางานให้ทำ — มันมาจาก **ข้อค้านของ `pf-adversary` ต่อเลนโค้ด GT-045 v3 ของรอบนี้เอง**: เราไม่มีหลักฐานชั้นไหนเลยว่าไคลเอนต์ **อ่าน** ฟิลด์ `+0x14` และถ้ามันไม่อ่าน รอบ attended ถัดไปจะฆ่าสมมติฐานที่ถูก ด้วยเหตุผลที่ผิด ⇒ ใบนี้ตอบก่อนได้ **โดยไม่ต้องเผารอบ attended**

**สถานะ (R157 · 2026-08-25 ~00:3x +07:00):** 🆕 เปิด **RE-065 ACTORTASK-USEBEHAVIOR-CTOR-WALK-001** (ท้ายไฟล์) — ครึ่งที่หายของ Door B (attack/action) ตาม draft R98 หัวข้อ 7 ข้อ 1 · NEEDS-BRIDGE-IMAGE · กุญแจปลด `INTENT_ATTACK_UNDELIVERABLE` ของ MOB-AGGRO-001 (เลน pure-logic ใหม่ของ R157) · หมายเหตุเลข: 064 ถูกออกซ้ำสองใบ (RE-064/GT-064) ตามกฎห้ามเปลี่ยนชื่อ ทั้งคู่คงเดิม ⇒ เลขว่างถัดไปคือ 065 · **ใบเปิดจริงตอนนี้: RE-065 ใบเดียว**

---
## 🆕🔬 GT-052 CLASS-SKILL-TABLE-001 [STATIC-ON-BRIDGE]: ~~dump ตารางอาชีพ + ตารางสกิล~~ ✂️ **ตีความคอลัมน์ + ผูก TEXTDATA + ผูกไอคอน** — ตาราง dump แล้วทั้งคู่ (`gamedata\` · จดหมาย 2150)  [✅ **PASS/DONE — ผลหน้าสะพาน 2026-08-24 00:44 (+07:00) · บันทึกโดย chief R135 · ผลลบติดใบ: ไม่พบ legend ของ `n_TARGET` ในชุดที่ค้น — ห้ามตั้ง label ("ไม่พบ" ≠ "ไม่มีใน client")**]

> 🔢 **หมายเหตุเลข (chief):** ร่างในจดหมาย 1656 ข้อ ④ เสนอใบนี้เป็น **GT-049** แต่ **GT-049 ถูกใช้ไปแล้ว**
> (LOOT-CHAT-TEMPLATE-001 · เปิดใน R127) ⇒ ใบนี้ขยับเลขเป็น **GT-052** · เนื้อหาคงตามร่าง 1656 ข้อ ④ ทุกประการ

> ✂️ **SCOPE-CUT (chief R132 · 2026-08-23 ~22:0x +07:00 · จากจดหมาย `20260823_2150_GAMEDATA-EXTRACTED-…`):**
> ขา "ไปดึงตาราง" ของใบนี้ **ปิดแล้ว** — ตัวถอดใหม่ `gamedata\pf_extract_gamedata.py` dump ครบ:
> - `CONSTDATA_TH__CHARCREATE_CLASS.tsv` — **5 แถว x 38 คอลัมน์** · `n_ID` เป็น **bitmask** (1=Gladiator 2=Paladin 4=Sniper
>   16=Necromancer 32=Sorcerer) · 🔴 **voodooist ไม่อยู่ในตารางสร้างตัวละคร** — ผลผูกไอคอน (step 4 เดิม) ออกแล้วบางส่วน:
>   ตาราง 5 ≠ ไอคอน 6 · เหลืออธิบายว่า voodooist เป็นอะไร (อย่าเดา — จดเป็นคำถามเปิด)
> - `CONSTDATA_TH__SKILL_CONTEXT.tsv` — **2,165 แถว x 20 คอลัมน์** · ฟิลด์ที่เห็นชื่อแล้ว: `n_ID` · `n_LEVEL_LEARN` · `n_PASSIVE` ·
>   `n_ISCLASS` (bitmask อาชีพ) · `n_LEVELS` · `f_SP_LEVE1` · `f_SP_LEVEL2PLUS` · `n_CD` · `n_TARGET` · `n_STAMINA_COST` ·
>   `n_EQUIPTYPE` · `n_EQUIPTYPE_LHAND` · `s_CAST_CONDITION` · `s_CAST_BEHAVIOR`
> **งานที่เหลือของใบ (แทน steps 2-3 เดิม):** ① ตีความคอลัมน์ — ค่าจริงของ `n_TARGET`/`s_CAST_CONDITION`/`s_CAST_BEHAVIOR` ฯลฯ
> แปลว่าอะไร (🔴 **รู้ชื่อคอลัมน์ ≠ รู้ความหมายค่า — ห้ามเดา** · ตีความจากข้อมูลจริง + cross-ref เท่านั้น) ·
> ② ผูกชื่อสกิลจากฝั่ง **TEXTDATA_TH** (ตารางข้อความ) เข้ากับ `n_ID` — ระบุ crosswalk field จริง ห้าม join ด้วยเลขเท่ากันเฉย ๆ (บทเรียน GT-044) ·
> ③ ผูก `n_ISCLASS` bitmask กับ 6 ไอคอน + ปมค่า bitmask 8 หายไป (1,2,4,16,32 — ไม่มี 8) — เกี่ยวกับ voodooist ไหม **ห้ามเดา ให้รายงานที่เจอ** ·
> ④ ตัวอย่างแถวจริง ≥3 แถวต่อข้อสรุปหนึ่งข้อ + sha256 ของ TSV ที่พึ่ง · precondition ไฟล์ `.dec` เดิมยังใช้ได้ถ้า re-derive
> แต่ทางหลักตอนนี้คืออ่าน `gamedata\tables\*.tsv` ตรง ๆ · ช่องบังคับใหม่: กรอก `ค้น gamedata แล้ว: …` ในผลด้วย

**ที่มา:** `notes_to_chief\20260823_1656_PANYA-DIRECTION-pause-attended-open-class-skill-lane.md` **ท่อน ③ + ④** (เลนอาชีพ/สกิล · ร่างใบ) ·
กำกับวิธีทำงานจาก `notes_to_chief\20260823_1718_GT050-SCOPE-CUT-codex-registry-already-has-the-skill-answer.md` (ข้อสังเกตท้ายจดหมาย)

ทำไมสำคัญกว่าที่เห็น: Panya ระบุเองว่าอาชีพ/สกิลเป็น **core หลักของเกม** · เลนนี้ผลเป็น **ตัวเลข** (ค่าใช้ MP/SP · cooldown · ระดับ)
⇒ พิสูจน์ได้ทั้ง headless และอ่านจาก DB/HUD **โดยไม่ต้องพึ่งเฟรมเสี้ยววินาทีและไม่ต้องพึ่งมุมกล้อง** — เลี่ยงจุดบอด attended ของคำสั่ง Panya 16:56

**หมวด:** `STATIC-ON-BRIDGE` — เปิดอ่านไฟล์ constdata ที่ decode แล้วบนเครื่องสะพาน · ผู้รับงานคือคนหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม ·
**ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว** · กติกา stamp 420 นาที / teardown / canonical DB ไม่เกี่ยวกับใบนี้ (ไม่บูตอะไรทั้งสิ้น)

### 🔴 จ็อบ 0 บังคับก่อนเริ่ม (กติกาใหม่จากจดหมาย 1718)
**ก่อนถอด/parse อะไรใหม่ ต้องเปิด `pf_bridge\external\*.tsv` ดูก่อนเสมอ** — คำถามหลายข้อที่เราเปิดใบไปอาจมีคำตอบอยู่ในชุดส่งมอบ RE ของ Codex แล้ว ·
ถ้าตารางอาชีพ/สกิลปรากฏใน `PF_SERIALIZER_FIELDS.tsv` / `PF_RUNTIME_CLASSMAP.tsv` (เช่นแถว `CSkillModule` `CSkillAttr` ที่ 1718 จดไว้)
ให้จดว่ามันตอบอะไรได้บ้างก่อน แล้วค่อยไป constdata เพื่อ **ตารางค่าตัวเลข** (constdata กับ serializer field คนละของ — อย่าเอามาแทนกัน)

### objective (claim เดียว)
**ใน `B_CONSTDATA_TH.pc_.dec` มีตารางอาชีพกี่แถว ไอดีอะไร · มีตารางสกิลหรือไม่ ถ้ามี กี่แถว ฟิลด์อะไรบ้าง**
(ค่าใช้ MP/SP · cooldown · ระดับ · ผูกกับอาชีพไหน) — แล้วตารางนั้น **ตรงกับ 6 อาชีพที่เห็นจากไอคอนหรือไม่**

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — เปิดอ่านไฟล์ constdata + `external\*.tsv` อย่างเดียว
🔴 **ห้ามแก้ไฟล์ constdata / TSV ส่งมอบ — เปิดอ่านอย่างเดียวทั้งหมด**

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- **ไฟล์ constdata ที่ decode แล้ว (ตัวเดียวกับที่ GT-044 ใช้):**
  `Pirate Force ServerProject\derived\v97_mapping_audit\B_CONSTDATA_TH.pc_.dec` (พาธตามจดหมาย 1656)
  🔴 **GT-044 อ้างสำเนาเดียวกันจาก path backups** (`...\backups\v103_one_item_backpack_20260814_103143\derived\v97_mapping_audit\B_CONSTDATA_TH.pc_.dec`)
  ⇒ **จด sha256 ของไฟล์ที่พึ่งจริง** และระบุว่าใช้สำเนาไหน · จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง
- **6 อาชีพที่อ่านจากไอคอน (สำรวจไว้ให้แล้ว):** `gladiator` · `necromancer` · `paladin` · `sniper` · `sorcerer` · `voodooist`
  จากไฟล์ `GameClient\Data\GUI\ICON\icon_class_*.tg_` (6 ไฟล์) · ไอคอนที่ชื่อมี skill = 14 ไฟล์
- **เครื่องมือ:** ~~`parse_pc_tables.py`~~ 🔴 **R132: ห้ามใช้ตัวนี้** — จดหมาย 2150 ②: พังกับ CONSTDATA มาตั้งแต่ 13 ส.ค.
  (อ่านชนิดฟิลด์หลัง version ผิด · `UnicodeDecodeError` กลางไฟล์ — traceback บน console cp874 อาจตายซ้อนใน print) ⇒
  ใช้ **`gamedata\pf_extract_gamedata.py`** (ตัวใหม่ · ตรวจชนิดอัตโนมัติ · re-derive 1.4 วิ) หรืออ่าน `gamedata\tables\*.tsv` ตรง ๆ ·
  ⚠️ **คำถามเปิด (adversary R132):** GT-044 เคย PASS ด้วยตัวเก่ากับไฟล์เดียวกัน — ขัดกับ "พังตั้งแต่ตารางแรก" ·
  ค่า derive ของ GT-044 ควร re-verify เทียบ `gamedata\tables\` (ถามผู้ช่วยแล้วในจดหมาย R132 — ห้ามเดาคำตอบ) ·
  ดัชนีเลขตารางดูจาก `FACTPACK_R100_CONSTDATA_MONSTER_LOOT.md` หัวข้อดัชนีตาราง (ท่าเดียวกับ GT-044 ที่ SCENE_NAME=007 / MAP_SCENE_LIST=101)

### steps
1. **จ็อบ 0 ก่อน** (เปิด `external\*.tsv` — ดูบล็อกจ็อบ 0 ข้างบน) · จดว่า TSV ตอบอะไรได้/ไม่ได้
2. หา **เลขตารางอาชีพ** และ **เลขตารางสกิล** จากดัชนีตารางใน FACTPACK · ถ้าไม่มีในดัชนี census ชื่อคอลัมน์ที่มีคำว่า class/skill/job
3. parse ตารางที่เจอเป็น TSV **เต็มทุกแถวทุกคอลัมน์** · จด offset/จำนวนแถว/จำนวนคอลัมน์ + sha256 ของ TSV แต่ละไฟล์
4. ผูกแถวอาชีพกับ 6 ชื่อจากไอคอน — ตรงกันครบ 6 ไหม · ถ้าตารางมีมากกว่า/น้อยกว่า 6 หรือชื่อไม่ตรง **ให้รายงานว่าต่างตรงไหน** (ไม่ต้องบังคับให้ตรง)
5. ถ้ามีตารางสกิล จด **ฟิลด์จริง** ที่พบ (ค่า MP/SP · cooldown · level · foreign key ไปตารางอาชีพ) + **ตัวอย่างแถวจริงอย่างน้อย 3 แถว** ต่อหนึ่งตาราง

### pass criteria
**ชั้น static (ชั้นเดียวของใบนี้ — ไม่มีชั้น client-observable):**
- TSV dump ครบทุกตารางที่อ้าง + **sha256 ของ TSV แต่ละไฟล์** + **จำนวนแถว** + **ตัวอย่างแถวจริง** (ไม่ใช่ schema เปล่า)
- ตอบ objective เป็นประโยคเดียวได้: จำนวนอาชีพ = N แถว ไอดี ... · ตารางสกิล = มี/ไม่มี · ถ้ามี = M แถว ฟิลด์ ... ผูกอาชีพผ่านคอลัมน์ ...
- sha256 ของไฟล์ constdata ก่อน-หลังตรงกัน · ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0

**ชั้น client-observable:** 🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้** (เหมือน GT-044/GT-047/GT-048/GT-049) ·
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย**

### 🔴 ผลลบมีค่าเท่าผลบวก
- **"ไม่มีตารางสกิลใน constdata"** = คำตอบที่ใช้ได้เต็มร้อย ⇒ แปลว่าสกิลอยู่ที่อื่น (อิมเมจ client / serializer field / ไฟล์ข้อมูลอื่น) ·
  จดพร้อมกำกับว่า **census คอลัมน์/ตารางไปถึงไหน** ("ไม่พบ" ≠ "ไม่มี" ถ้ายังไม่ census ครบดัชนีตาราง)
- **ตารางอาชีพไม่ตรง 6 ไอคอน** = ผลที่มีค่า ⇒ ไอคอนกับตารางข้อมูลเป็นคนละ namespace (บทเรียน GT-044: ห้าม join เพราะเลขเท่ากัน)

### nonclaims (ติดไปกับผลทุกกรณี)
- **ตารางในไคลเอนต์/constdata = สิ่งที่ไคลเอนต์รู้ ไม่ใช่กฎของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล
- ไม่พิสูจน์ว่า runtime *ใช้* ค่าเหล่านี้ตอนร่ายสกิลจริง — พิสูจน์แค่ mapping/ค่าในไฟล์ข้อมูล (การพิสูจน์ runtime = เลน headless replay ทีหลัง)
- **ห้าม join ข้ามตารางเพียงเพราะเลข id เท่ากัน** (บทเรียน GT-044) — ต้องมี crosswalk field จริง
- **ไม่พึ่ง `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส** — UNKNOWN 100% (บันทึกผลลบ ไม่ใช่แหล่งชื่อ)
- **result:** ✅ **PASS/DONE (2026-08-24 00:44 +07:00)** — จดหมายเต็ม `notes_to_chief/20260824_0044_GT052-RESULT-CLASS-SKILL-TABLE-CROSSWALKS.md` ·
  ค้น external แล้ว: เจอ skill protocol/serializer 10 ชื่อ 88 field rows (แต่ `CSkillModule`/`CSkillAttr` EMPTY · CLASSMAP ค้น Skill = 0) — ไม่ใช่ตารางค่า/ชื่อ · ค้น gamedata แล้ว: เจอครบ (`CHARCREATE_CLASS` 5×38 · `SKILL_CONTEXT` 2165×20 · `CURRICULUM` 137×7 · `SKILL_TEXT` 940×6 · `CONTENT_CLASS` 6×3) ·
  อาชีพ 5 แถว `n_ID=1,2,4,16,32` ผูกไอคอนตรงทั้งหมด · bit 8 = Voodoo/Voodooist มีข้อมูลสามชั้น (CONTENT_CLASS row 8 · 35 skill rows · icon voodooist) แต่ไม่มีแถวสร้างตัวละคร · ชื่อสกิลผูกได้ 898 จุดตัด (`SKILL_CONTEXT.n_ID = SKILL_TEXT.n_ID` · unique 100% ทั้งสองข้าง) · `n_ISCLASS` เป็น bitmask (row 99 = 63) ·
  `CURRICULUM.n_SKILL` 137/137 + `CHARCREATE_CLASS.s_SKILL_1..4` 20/20 resolve ครบ · `n_PASSIVE` codes 0..5 ไม่ใช่ boolean · `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` เป็น DSL (`GO`/`BUFF_I`/`RANGE` · `CHASE`/`SKIP`) ·
  🔴 **ผลลบ: `n_TARGET` codes `0:1904 1:167 2:30 4:62 5:2` — ไม่พบ legend ในชุดที่ค้น ห้ามตั้ง label** ("ไม่พบ" ≠ "ไม่มีใน client") · sha ทุกไฟล์ก่อน/หลังตรงกัน


## 🆕🔬 GT-050 SKILLCAST-WIRE-001 [STATIC-ON-BRIDGE]: **ตรวจแล้วใช้** (ไม่ใช่ไปถอดใหม่) แถวสกิลจากชุดส่งมอบ RE ของ Codex — verify sha ของ `TriggerCastSkillVital`/`CLearnSkillVital` · re-derive ปฏิปักษ์ · ปิด `CLearnSkillResultVital` · หาทิศทาง+ตัวจุดชนวนของ `TriggerCastSkillVital`  [🟡 **PARTIAL — ผลหน้าสะพาน 2026-08-24 00:55 (+07:00) · บันทึกโดย chief R135 · จ็อบ 1–3 ปิด (span PASS · re-derive PASS · `CLearnSkillResultVital` CLOSED) · จ็อบ 4 = bounded negative ชนเพดาน static: direction/trigger ของ `TriggerCastSkillVital` ยังตัดสินไม่ได้ — ทางต่อเป็น observe-only probe แบบ attended (เลนพักตามคำสั่ง 16:56)**]

**ที่มา:**
- `notes_to_chief\20260823_1656_PANYA-DIRECTION-pause-attended-open-class-skill-lane.md` **ท่อน ③ + ④** (เปิดเลนสกิล · ร่าง GT-050 ฉบับเดิม "ไปถอด")
- `notes_to_chief\20260823_1718_GT050-SCOPE-CUT-codex-registry-already-has-the-skill-answer.md` (**scope-cut — ฉบับนี้ยึดตามใบนี้**: ชุดส่งมอบถอดไว้ให้แล้ว เหลือ "ตรวจแล้วใช้")

🔴 **เปลี่ยนจาก "ไปถอด" เป็น "ตรวจแล้วใช้":** แถวของสกิลอยู่ใน `pf_bridge\external\PF_PROTOCOL_REGISTRY.tsv` + `PF_SERIALIZER_FIELDS.tsv` ครบแล้ว
พร้อม VA / span / sha256 (ชุดส่งมอบของ Codex) · **แต่ยังไม่มีโค้ดของเราบรรทัดไหนอ่านมัน** ⇒ GT-050 = ผู้ใช้รายแรกจริง ·
กติกาเดิม *"ห้ามเขียนโมดูล/encoder จนกว่า GT-042 จะปิด"* — GT-042 ปิดแล้ว 02:03 วันนี้ ⇒ ปลดล็อกแล้ว

**หมวด:** `STATIC-ON-BRIDGE` — เปิด `GameClient.local.bin` + TSV ส่งมอบบนสะพาน จึงทำบน cloud clone ไม่ได้ ·
ผู้รับงานคือคนหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · **ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว** · stamp 420/teardown/canonical ไม่เกี่ยวกับใบนี้

### objective (claim เดียว)
**ยืนยันแถวสกิลของชุดส่งมอบ RE ด้วยการ verify sha + re-derive ปฏิปักษ์ · ปิดช่องเดียวที่ Codex ทำเครื่องหมาย UNKNOWN ไว้ (`CLearnSkillResultVital`)
· และหา "ทิศทาง + ตัวจุดชนวน" ของ `TriggerCastSkillVital` (ไคลเอนต์ส่งผ่าน `0x0089A600` WRITE หรือรับผ่าน `0x0089A640` READ)**
🔴 **ตารางบอกฟิลด์ แต่ไม่ได้บอกทิศทางและตัวจุดชนวน — ข้อนั้นยังต้องทำเอง (ท่าเดียวกับ GT-046)**

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — เปิดอ่านอิมเมจ + อ่าน TSV ส่งมอบอย่างเดียว
🔴 **ห้ามแก้ อิมเมจ / capture / TSV ส่งมอบ — เปิดอ่านอย่างเดียวทั้งหมด**

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- **อิมเมจ (sha/size เดียวกับที่ GT-046/GT-048/GT-049 พิน):** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  🔴 **จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ**
- **TSV ส่งมอบ RE ของ Codex ที่ `pf_bridge\external\`:** `PF_PROTOCOL_REGISTRY.tsv` (520 บรรทัด) · `PF_SERIALIZER_FIELDS.tsv` (6,932) ·
  `PF_TAG_CENSUS.tsv` · `PF_FIELD_VALIDATION.tsv` · `PF_RUNTIME_CLASSMAP.tsv` (6,244 data rows — 6,245 รวม header ตามจดหมาย 1718 · UNKNOWN 100% — ห้ามพึ่งเป็นชื่อคลาส)
- **ท่าทำงาน:** ตามวินัย `pf-static-re` · 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative** (บทเรียนรอบ 83) ·
  census ด้วย byte matching (`E8`/`E9 rel32` ทุกออฟเซ็ต) + dword refs + vtable slots ·
  สวีป exec section ทั้งสอง: `.text` (`0x00401000`, Vsize `0x00838A2C`) และ `.code` (`0x00C3A000`, Vsize `0x2E1`)

### ของที่ชุดส่งมอบให้มา (จาก 1718 · 🔴 verify sha ก่อนพึ่งด้วยตัวเอง — นี่คือจ็อบ 1)
```
TriggerCastSkillVital  (ตัวหลักของเลน)
  serializer_va  0x00600A60      handler_va  0x00601810
  vtable_va      0x00F3175C      getter_va   0x00600A40      id_global  0x0108284C
  span           [0x00600A60, 0x00600AD7)
  span_sha256    396200629ab4082b8eef730dda809124f5df8eca6f0ced5419d7a2ac7e3500ec
  ฟิลด์ (W และ R เหมือนกันทั้งสามช่อง):
    #1 tag 0x0F @ +0x14 len 2   ·   #2 tag 0x08 @ +0x16 len 1   ·   #3 tag 0x14 @ +0x18 len 4

CLearnSkillVital
  serializer 0x00755AC0 · span [0x00755AC0,0x00755B13)
  sha        b99487413ffa79784deda46283aafc2f3954d98a85362d35304b745d6c062fc4
  ฟิลด์:     #1 tag 0x14 @ +0x14 len 4   ·   #2 tag 0x0B @ +0x18 len 1

CLearnSkillResultVital  <- ตัวเดียวที่ยังไม่ปิด (Codex ติด UNKNOWN อย่างซื่อสัตย์)
  มีแถว SUBCALL + PE_IMPORT_INVALID_PARAMETER_NOINFO_* ระบุตรง ๆ ว่า wire_effect_unproved

ของแถมในทะเบียน (ไม่ใช่เป้าใบนี้ · จดไว้เฉย ๆ):
  CSkillModule (vtable 0x00F48D88) · CSkillAttr · ActorLearnedPetsSkillData ·
  Pets_SetPetSkillVital / Pets_LearnPetSkillVital / Pets_UpdateLearnedPetSkillVital

stream primitive  0x0089A600 (WRITE / outbound)  ·  0x0089A640 (READ / inbound)  [พิสูจน์แล้วตั้งแต่ GT-040]
```

### จ็อบ (ทำตามลำดับ 1 -> 2 -> 3 -> 4 · 🔴 **ห้ามข้ามข้อ 1 และ 2** — ตารางเป็นของที่คนอื่นทำ ต้องผ่านปฏิปักษ์ก่อนพึ่ง)
1. **verify** — เทียบ sha256 ของ span ทั้งสองข้างบน (`TriggerCastSkillVital` `[0x00600A60,0x00600AD7)` และ `CLearnSkillVital` `[0x00755AC0,0x00755B13)`)
   กับอิมเมจจริง · 🔴 **ไม่ตรงแม้ตัวเดียว = หยุดแล้วรายงาน span ที่เพี้ยน ห้าม re-derive ทับ**
2. **re-derive แบบปฏิปักษ์เฉพาะสามตัวนี้** — รัน extractor ในไดเรกทอรีเปล่านอกโฟลเดอร์ส่งมอบ ชี้อิมเมจเดิม เทียบว่าได้แถวเดิมไบต์ต่อไบต์ไหม
   (ท่าเดียวกับ GT-042 ที่ผ่านแล้ว) · image sha ไม่เปลี่ยน
3. **ปิดช่องเดียวที่ยังไม่ปิด — `CLearnSkillResultVital`** ท่อน `PE_IMPORT_*` / `SUBCALL` ที่ติด UNKNOWN ·
   ไล่ว่ามันเป็น serializer จริงหรือแค่ทางเรียก import/subcall · จด span/VA/len/sha256 ของสิ่งที่ปิดได้ หรือประกาศว่าปิดไม่ได้พร้อมเหตุ
4. **หาทิศทาง + ตัวจุดชนวนของ `TriggerCastSkillVital`** (ท่าเดียวกับ GT-046):
   - ใครเรียก constructor / อ้าง vtable literal `0x00F3175C` · ตามสายขึ้นไปจนถึงจุดที่ object เข้าสตรีม
   - เข้าสตรีมผ่าน **`0x0089A600` (WRITE = ไคลเอนต์ส่ง)** หรือ **`0x0089A640` (READ = ไคลเอนต์รับ)** — ตัวตัดสินทิศทาง
   - ถ้าเป็น WRITE: ตัวจุดชนวนคือ **input callback** (ท่าปุ่ม/คลิก แบบ `WM_LBUTTONDOWN 0x201` ที่ GT-046 เจอ) หรือ **timer/passive** · ค่าที่ใส่ `+0x14/+0x16/+0x18` มาจากไหน
   - ถ้าเจอ inbound handler ให้ไล่ต่อว่าแตกเป็น message id อะไร (แบบที่ GT-046 ทำกับ `FC/FD/FE -> 0x1F/0x03/0x22`)

### pass criteria — **STATIC-ON-BRIDGE (span + sha256 + re-derive · ชั้นเดียว)**
**ชั้น static (ชั้นเดียวของใบนี้):**
- verify sha ของ **ทุก** span ที่พึ่งก่อน re-derive · 🔴 **sha ไม่ตรงแม้ตัวเดียว = หยุด รายงาน ห้าม re-derive ทับ** (จ็อบ 1)
- re-derive ปฏิปักษ์ผ่านครบสามตัว · image sha ไม่เปลี่ยน (จ็อบ 2)
- ตอบทิศทางของ `TriggerCastSkillVital` เป็นประโยคเดียวได้: `สร้าง/เขียนที่ <VA> เข้าสตรีมผ่าน 0x0089A600 (WRITE) ตัวจุดชนวน = <input/timer/...>`
  **หรือ** `เข้าสตรีมผ่าน 0x0089A640 (READ) = inbound แตกเป็น message id ...` **หรือ** `ไม่พบจุดเข้าสตรีมเลยหลัง census E8/E9 + indirect ครบ`
- `CLearnSkillResultVital`: ปิดได้ (span/VA/len/sha256) หรือประกาศปิดไม่ได้พร้อมเหตุ + สถานะ census
- แนบ span `[start,end)` + file offset + len + sha256 ของ **ทุก** ฟังก์ชันที่อ้าง (รูปแบบเดียวกับ GT-040/GT-042/GT-046/GT-048/GT-049) ·
  ระบุสถานะการไล่ indirect (E8/E9 + dword ref + vtable slot · ครบ/ค้าง) · sha อิมเมจ+TSV ก่อน-หลังตรงกัน ·
  ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0

**ชั้น client-observable:** 🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้** (เหมือน GT-046/GT-047/GT-048/GT-049) ·
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย** ·
🔴 **ห้ามใครอ้าง static เป็นหลักฐานว่าจอเห็นการร่ายสกิลหรือค่าลด MP/cooldown ใด** — คนละชั้นหลักฐาน

### 🔴 ผลลบมีค่าเท่าผลบวก
- **span sha ไม่ตรง** = ข่าวที่มีค่า ⇒ ชุดส่งมอบเพี้ยน/อิมเมจคนละตัว · หยุดทั้งใบ รายงาน ไม่ต้องทำจ็อบ 3-4
- **re-derive ไม่ได้แถวเดิม** = ข่าวที่มีค่า ⇒ extractor ไม่ deterministic หรือ span ป้ายผิด (บทเรียน erratum handler ของ GT-042)
- **"ไม่พบจุดเข้าสตรีมเลย"** = ผลที่มีค่าเท่าการเจอ ⇒ แต่ต้องกำกับว่าไล่ indirect ครบหรือยัง ("ไม่พบ WRITE" ≠ "ไคลเอนต์ไม่ส่ง")
- **`CLearnSkillResultVital` ปิดไม่ได้** = ผลที่ใช้ได้ ⇒ ระบุว่าติดตรง `PE_IMPORT_*`/`SUBCALL` ไหน เพื่อให้ใบถัดไปหยิบต่อ

### nonclaims (ติดไปกับผลทุกกรณี · ตามจดหมาย 1718)
- **ยังไม่รู้ความหมายของฟิลด์** — `tag 0x0F len 2` / `tag 0x08 len 1` / `tag 0x14 len 4` **ยังไม่รู้ว่าอันไหนคือ skill id / target / level** 🔴 ห้ามเดา
- **ยังไม่รู้ทิศทางจริงของ `TriggerCastSkillVital`** — ตารางมีทั้งแถว W และ R เพราะ serializer ตัวเดียวทำสองทาง **ไม่ได้แปลว่าไคลเอนต์ส่งจริง** (จ็อบ 4 ต้องตัดสิน)
- **static ไม่พิสูจน์ว่ารันไทม์ส่ง/รับจริง** — พิสูจน์ได้แค่ว่ามี/ไม่มีเส้นทางในอิมเมจ
- **ไม่ claim ว่ารู้ชื่อคลาส** — vtable ไม่มี RTTI/name literal · ห้ามเดาชื่อ = ห้ามประดิษฐ์ wire format · **ไม่พึ่ง `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส**
- **ไม่ claim เรื่องเพ็ตสกิล** (`Pets_*`) — เป็นของแถมในทะเบียน ไม่ใช่เป้าใบนี้
- **ขั้นต่อไปที่ตั้งใจไว้ (ยังไม่ใช่คำสั่งให้เขียนโค้ด):** พอรู้รูปแบบไบต์แล้ว ทำ **เลน headless replay ของการร่ายสกิล** พิสูจน์ MP/cooldown/ผลลัพธ์จบในตัว **โดยไม่ต้องเปิดเกมเลย**
- **result:** 🟡 **PARTIAL STATIC / BOUNDED NEGATIVE (2026-08-24 00:55 +07:00)** — จดหมายเต็ม
  `notes_to_chief/20260824_0055_GT050-RESULT-CLEARNRESULT-CLOSED-TRIGGER-DIRECTION-UNRESOLVED.md` ·
  ค้น external แล้ว: เจอสามชื่อครบ (field rows 6+4+20) · ค้น gamedata แล้ว: เจอ `SKILL_CONTEXT` แต่ไม่ตอบ wire direction ·
  **จ็อบ 1 PASS:** span SHA ทั้งสองตรง pin · **จ็อบ 2 PASS:** re-derive ปฏิปักษ์ได้ TSV byte-identical ทั้งสามไฟล์ (รวม `PF_TAG_CENSUS.tsv` `63bc9a03…`) ·
  **จ็อบ 3 CLOSED:** `CLearnSkillResultVital` wire shape พิสูจน์ครบ — `count u16/tag 0x12` + N records ขนาด 12 ไบต์ `(u32 0x14 · u16 0x12 · u32 0x14)` + trailing `u8/tag 0x0B @+0x2C` · UNKNOWN 7 จุด = `_invalid_parameter_noinfo` (container guard ไม่ใช่ field) · `0x0077FC30` = vector append หลัง READ ·
  **จ็อบ 4 UNRESOLVED (bounded negative):** `TriggerCastSkillVital` มี inbound-capable consumer `0x00601810` → local slot setter `0x00449110` · **ไม่พบ chain ไป outbound submit `0x005DD800`** แต่ indirect generic-registry dispatch ยังปิดไม่ได้ ⇒ ห้ามสรุปว่า client ส่งจริง/รับอย่างเดียว/trigger เป็นอะไร (เพดานเดียวกับ checkpoint 20260816) · ทางต่อ = observe-only probe แบบ attended ·
  probe ทำซ้ำได้: `tools\pf_gt050_skill_wire_probe.py` sha `325ca7d8…` (อยู่นอก git โดย `.gitignore /tools/*` ฝั่งสะพาน) · sha อิมเมจ+TSV ทุกไฟล์ก่อน/หลังตรงกัน

## 🆕🔬 GT-053 SCENE2-NATIVE-IDENTITY-CROSSCHECK-001 [STATIC-ON-BRIDGE]: ไฟล์ฉาก native ของ scene 2 มี placement index 60 (`0x203D` Fighting Fish soldier) จริงไหม — จุดเดียวที่ตรวจแล้วอาจฆ่า H1 ได้ทันที  [✅ **PASS/DONE — ผลหน้าสะพาน 2026-08-24 00:38 (+07:00) · บันทึกโดย chief R135 · N=106 ≥ 61 ⇒ `0x203D` in-band ⇒ H1 รอด**]

**ที่มา:**
- `FINDINGS_R128_GT051_RENDER_SYNTHESIS.md` **ท่อน ② (H1) + ④ ข้อ 1** — chief ทำ GT-051 เสร็จแล้ว · ระบุ SCENE-005 เป็น **ช่องว่างหลักฐานเดียวที่ชี้ขาด H1 ได้**
- `reports\PF_SCENE005_FACTION1_HOSTILE_RELATION_RUNTIME_PASS_20260815.md` (เคส render-success ที่ต้อง cross-check · identity `0x203D` · 31-byte `TargetVital`)
- `notes_to_chief\20260823_1718_GT050-SCOPE-CUT-...md` (กติกา: ก่อนถอดใหม่เปิด `external\*.tsv` ก่อน) · ท่าไฟล์ฉาก native พิสูจน์แล้วใน **GT-048 PASS** (path `Data\Scene\Save\bg0001\bg0001.npc`)

**สมมติฐานที่ใบนี้ทดสอบ (RENDER-DISCRIMINATOR-H1 จาก GT-051):**
> ไคลเอนต์วาด/เปลี่ยนสถานะ entity บนจอ **เฉพาะเมื่อ identity ชี้ไปยังของที่ client วางเองจาก native scene**
> (band `0x2000 + placement_index + 1`) หรือ actor ของผู้เล่นเอง · wire actor_entry = **อัปเดตสถานะ ไม่ใช่สร้างตัวใหม่**

SCENE-005 วาด Fighting Fish soldier `0x203D` (= `0x2000` + 60 + 1 ⇒ placement index 60 · template 34 · preset `M025_001_000_N` · scene 2) บนจอสำเร็จ
(ชื่อชมพู/แดง + ขอบแดง + Tab เลือกได้ + 31-byte `TargetVital` เป๊ะ) · **แต่ยังไม่มีใครยืนยันว่าไฟล์ฉาก native ของ scene 2 มี placement ถึง index 60 จริง**
🔴 **เกณฑ์ชี้ขาดของใบนี้คือ band membership — จำนวน placement N ของไฟล์ฉาก scene 2:**
**N ≥ 61 (มี index 60) = `0x203D` in-band = H1 รอด · N < 61 = SCENE-005 วาด identity นอก band = H1 ตายทันที**
⚠️ **identity/template ที่ index 60 ตรง/ไม่ตรง `0x203D`/34 ไม่ใช่เกณฑ์ฆ่า H1** — SCENE-007 (scene 1) พิสูจน์แล้วว่า
wire override template/พิกัดของ identity ใน band ได้และ client ยังวาด (ดู `FINDINGS_R128` ตาราง ①) · ตรง = โบนัสยืนยัน · ไม่ตรง = จดรายงาน

**หมวด:** `STATIC-ON-BRIDGE` — ไฟล์ฉาก native อยู่บนเครื่องสะพานเท่านั้น (ไม่มีบน cloud) · ผู้รับงานคือคนหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม ·
**ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว** · stamp 420 / teardown / canonical DB ไม่เกี่ยวกับใบนี้ (ไม่บูตอะไรทั้งสิ้น)

### 🔴 จ็อบ 0 บังคับก่อนเริ่ม (กติกา 1718)
**ก่อนถอด/parse อะไรใหม่ ต้องเปิด `pf_bridge\external\*.tsv` ดูก่อนเสมอ** — ถ้าชุดส่งมอบ RE มี roster/placement ของ scene 2 อยู่แล้ว ให้จดว่ามันตอบอะไรได้ก่อน แล้วค่อยไปไฟล์ฉาก native

### objective (claim เดียว)
**ไฟล์ฉาก native ของ scene 2 (`Data\Scene\Save\<โฟลเดอร์ฉาก scene 2>\*.npc` — ท่าเดียวกับ `bg0001.npc` ที่ GT-048 พิสูจน์ path)
มี placement ทั้งหมดกี่ตัว (N) — N ≥ 61 (index 60 มีจริง = `0x203D` in-band) หรือ N < 61 —
ตอบด้วยหลักฐานระดับ offset + f32 triple + sha256 ของไฟล์ฉาก (แบบเดียวกับที่ GT-048 ทำกับ `bg0001.npc` offset `0x1D46`)**
🔴 **ชื่อโฟลเดอร์ฉากของ scene 2 ต้อง resolve จากตาราง SCENE_NAME (007) / MAP_SCENE_LIST (101) ที่ GT-044 dump แล้ว — ห้ามเดา**

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — เปิดอ่านไฟล์ฉาก native + ตาราง GT-044 + scenario อย่างเดียว
🔴 **ห้ามแก้ไฟล์ฉาก / อิมเมจ / TSV / scenario — เปิดอ่านอย่างเดียวทั้งหมด**

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- **ไฟล์ฉาก native ของ scene 2:** อยู่ใต้ `GameClient\Data\Scene\Save\<โฟลเดอร์>\*.npc` (โฟลเดอร์ยังไม่รู้ — จ็อบ 1 resolve) ·
  🔴 **จด sha256 + ขนาด ของไฟล์ฉากที่พึ่งจริง · ก่อนเริ่มและหลังจบต้องตรงกัน (อ่านอย่างเดียว)**
- **ตาราง GT-044 (dump แล้ว · PASS 2026-08-23):** `outbox\GT044_SCENE_NAME_007.tsv` (271 แถว) + `GT044_MAP_SCENE_LIST_101.tsv` (15 แถว) ·
  ใช้ resolve ชื่อโฟลเดอร์ฉากของ scene 2 · verify sha ของ TSV ก่อนพึ่ง
  🔴 **บทเรียน GT-044: ห้าม join `MAP_SCENE_LIST.n_ID` กับ `SCENE_NAME.n_ID` เพียงเพราะเลขเท่ากัน** — namespace แยกกัน ·
  และ `scene_id: 2` ใน scenario เป็นเลขที่เลนใช้ **ไม่ใช่แถว index เดียวกับตารางโดยอัตโนมัติ** — resolve ให้ครบ crosswalk อย่าลัด
- **scenario ที่ SCENE-005 ใช้ (ในโค้ด repo · อ่านอย่างเดียว):**
  `scenarios\scene2_fighting_fish_soldier_hp3857_player_faction1.json` — id `scene2_fighting_fish_soldier_p60_hp3857_player_faction1`
  ค่าที่ต้องใช้เทียบ: `remote_actor.placement_index = 60` · `actor_identity = 0x203D` · `template_id = 34` · `visual_preset = M025_001_000_N` ·
  `scene_id = 2` · `scene_seq = 0` · entity `x 21421.0059 · y 9277.1123 · z 590.6788`
  🔴 **อ่าน provenance ให้ถูกด้าน:** `coordinate_provenance = synthetic_p60_minus100x_minus50y_samez` เป็นของ
  **ตำแหน่งผู้เล่น (`entry.position` = P60 −100X −50Y Z เท่าเดิม)** — **พิกัด entity `21421.0059/9277.1123/590.6788`
  คือค่า authentic ของ P60** ตาม ledger `GEO-PF-002` (*"P60 placement is evidence-backed; only the transient player
  offset is synthetic"*) และ `docs/COMMAND_HANDOFF.md` (*"rendered at the authentic P60 placement"*)
  ⇒ **f32 triple นี้คือตัว verify การ resolve+parse ที่แรงที่สุดของใบ** (ท่าเดียวกับ GT-048 offset `0x1D46`) — ดูจ็อบ 3
- **ท่า native scene (พิสูจน์แล้ว GT-048 · verify sha ก่อนพึ่ง):** loader path อ่าน `Data\Scene\Save\bg0001\bg0001.npc` ผ่าน
  `SceneNPCCreation` (trigger `0x0043A9D0` · loader `0x00439E90` · parser `0x00439780` · per-placement create `0x0043A6F0`) ·
  GT-048 เจอ f32 triple ของ P30 ที่ offset `0x1D46` ของ `bg0001.npc` — โครงไฟล์ฉากตัวเดียวกัน ใช้ parser ตัวเดียวกันกับ scene 2
- **อิมเมจ (ถ้าต้องยืนยันโครง parser ซ้ำ · sha/size เดียวกับ GT-046/GT-048):** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · จด sha ก่อน-หลังตรงกัน (ถ้าเปิด)

### จ็อบ (ทำตามลำดับ 1 -> 2 -> 3 -> 4)
1. **resolve ชื่อโฟลเดอร์ฉากของ scene 2** จาก `GT044_SCENE_NAME_007.tsv` / `GT044_MAP_SCENE_LIST_101.tsv` —
   หา s_MODLE_ID / s_IMAGENAME / ชื่อไฟล์ฉากของ scene 2 (ท่าเดียวกับที่ GT-044 ผูก `BG0001` = scene id 1) ·
   จดเส้นทางการ resolve ให้ re-derive ได้ · 🔴 ถ้า resolve ไม่ได้จากสองตารางนี้ = หยุด รายงาน (อย่าเดาว่าเป็น `bg0002`)
2. **เปิดไฟล์ฉาก native ของ scene 2** ด้วย parser โครงเดียวกับที่ GT-048 อ่าน `bg0001.npc` · นับ **จำนวน placement ทั้งหมด = N** ·
   ถ้า N ≥ 61 อ่านค่า placement ที่ **index 60 (นับตัวแรกเป็น index 0 — ท่าเดียวกับ P0→`0x2001`)** · จด identity/template/preset/f32 triple
3. **verify การ parse ด้วย f32 triple (ตัวยืนยันหลัก):** เทียบ triple ของ index 60 กับพิกัด authentic P60 ของ scenario
   (`21421.0059 / 9277.1123 / 590.6788`) —
   - **ตรง f32-exact** = ยืนยันว่า resolve โฟลเดอร์ถูกและ parse ถูกแกน · แนบ offset + triple + sha256 (รูปแบบ GT-048 `0x1D46`)
   - **ไม่ตรง** = 🔴 **สัญญาณเตือนว่า resolve/parse อาจผิดไฟล์หรือผิดโครง — ห้ามบันทึกคำตัดสิน H1 จนกว่าจะอธิบายได้**
     (เช็คก่อน: ผิดโฟลเดอร์? โครง record คนละขนาด? index เlื่อน?) · ถ้าอธิบายไม่ได้ = จบใบด้วย "ตอบไม่ได้" พร้อมหลักฐานที่เจอ
   - identity/template ที่ index 60 ตรง `0x203D`/34 = โบนัสยืนยันสูตร band ใช้กับ scene 2 · **ไม่ตรงแต่ triple ตรง** = จดรายงาน
     (สูตร identity อาจไม่ใช่ `0x2000+idx+1` บน scene 2 — อย่า force คำตัดสิน ให้รายงานสิ่งที่เห็น)
4. **คำตัดสิน H1 (band membership เท่านั้น):**
   - **N ≥ 61** (และจ็อบ 3 ยืนยันการ parse) ⇒ `0x203D` in-band ⇒ **H1 รอด** — SCENE-005 เข้าตารางเคส in-band ของ GT-051
   - **N < 61** (และจ็อบ 3 ยืนยันว่า parse ถูกไฟล์ถูกโครง — ใช้ f32 ของ placement ตัวอื่นที่รู้ค่า ถ้ามี) ⇒ SCENE-005 วาด identity นอก band
     ⇒ **H1 ตายทันที** · แนบ N + offset ช่วงตาราง + sha256 ครบ

### pass criteria — **STATIC-ON-BRIDGE (offset + f32 triple + sha256 · ชั้นเดียว)**
**ชั้น static (ชั้นเดียวของใบนี้):**
- verify sha ของ **ทุก** ไฟล์/TSV ที่พึ่งก่อน re-derive · 🔴 **sha ไม่ตรงแม้ตัวเดียว = หยุด รายงาน ห้าม re-derive ทับ**
- ตอบ objective เป็นประโยคเดียวได้อย่างใดอย่างหนึ่ง:
  `ไฟล์ฉาก scene 2 (<โฟลเดอร์>\<ไฟล์>.npc) มี N=<N> placement ≥ 61 · index 60 f32 ตรง P60 authentic ที่ offset <off> ⇒ 0x203D in-band ⇒ H1 รอด` **หรือ**
  `ไฟล์ฉาก scene 2 มี N=<N> < 61 placement (parse ยืนยันแล้ว) ⇒ SCENE-005 วาด identity นอก band ⇒ H1 ตาย` **หรือ**
  `resolve โฟลเดอร์ไม่ได้ / f32 verify ไม่ผ่านและอธิบายไม่ได้ — ตอบไม่ได้จากชุดนี้ (ห้ามบันทึกคำตัดสิน H1)`
- แนบ **ชื่อโฟลเดอร์+ไฟล์ฉาก + เส้นทาง resolve + offset + f32 triple + จำนวน placement ทั้งหมด + sha256** ของไฟล์ฉาก (รูปแบบเดียวกับ GT-048)
- sha256 ไฟล์ฉาก + TSV (+ อิมเมจถ้าเปิด) ก่อน-หลังตรงกัน · ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0

**ชั้น client-observable:** 🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้** (เหมือน GT-044/GT-047/GT-048/GT-049/GT-050) ·
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย** ·
🔴 **ห้ามใครอ้าง static เป็นหลักฐานว่าจอเห็นหรือไม่เห็น Fighting Fish soldier** — คนละชั้นหลักฐานกับ SCENE-005 attended

### 🔴 ผลลบมีค่าเท่าผลบวก (ใบนี้ decisive ทั้งสองทาง)
- **N ≥ 61** = H1 รอด ⇒ SCENE-005 เข้าตารางเคส in-band ของ GT-051 · ถ้า identity/template ที่ index 60 ตรงด้วย = ยืนยันสูตร band ใช้กับ scene 2 (เดิมยืนยันแค่ bg0001)
- **N < 61** = **H1 ตายทันที** ⇒ ข่าวใหญ่: wire วาด identity นอก band ได้จริง ⇒ redirect ทั้งข้อสรุป GT-051 และเลน multiplayer (GT-030) ·
  🔴 แต่ต้องผ่าน f32 verify (จ็อบ 3) ก่อน — "N < 61" บนไฟล์ผิด/parse ผิด = คำตัดสินปลอม
- **identity/template ที่ index 60 ไม่ตรง แต่ triple ตรง** = ผลที่มีค่า ⇒ สูตร identity ของ scene 2 อาจต่างจาก bg0001 — รายงานตามที่เห็น อย่า force
- **resolve โฟลเดอร์ไม่ได้** = ผลที่มีค่า ⇒ จดว่าตาราง GT-044 ชุดนี้ไม่พอ crosswalk scene 2 · เสนอว่าต้อง dump ตารางไหนเพิ่ม (ยังไม่เปิดใบใหม่เอง)

### nonclaims (ติดไปกับผลทุกกรณี)
- **N ≥ 61 ไม่พิสูจน์ว่า native path รันจริงตอน SCENE-005** และไม่พิสูจน์ว่า client "อัปเดตของเดิม" หรือ "สร้างตัวที่สอง"
  (SCENE-007 เปิดคำถามนี้ไว้ — ดู FINDINGS_R128 ④ ข้อ 4) — ใบนี้บอกได้แค่ **H1 รอด/ตาย ที่ระดับ band membership**
- **พิกัด entity ใน scenario เป็นค่า authentic ของ P60** (ตัวสังเคราะห์คือตำแหน่ง*ผู้เล่น*) — ตาม ledger GEO-PF-002 ·
  ถ้า triple ใน scenario ไม่ตรงกับไฟล์ฉากจริง = ปัญหาการ parse หรือปัญหา provenance ของ ledger — รายงาน อย่าเลือกข้างเอง
- **ห้ามเดาชื่อโฟลเดอร์ฉาก scene 2** (เช่น สมมติ `bg0002`) — ต้อง resolve จากตาราง GT-044 เท่านั้น
- **band `0x2000+p+1` ยืนยันจริงเฉพาะ bg0001** (GT-022/GT-048) ก่อนใบนี้ — การอ่าน `0x203D` = index 60 สำหรับ scene 2 เป็น **การอนุมานรูปแบบที่ใบนี้ต้องพิสูจน์** ไม่ใช่ของที่รู้แล้ว
- **ไม่ claim เรื่องเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล · faction 1 ของ scenario เป็น `candidate_not_authentic_player_faction` ตาม SCENE-005 (ไม่เกี่ยวกับใบนี้ แต่ห้ามยกมาอ้างเป็นของแท้)
- **ไม่พึ่ง `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส** — UNKNOWN 100%
- **result:** ✅ **PASS/DONE (2026-08-24 00:38 +07:00)** — จดหมายเต็ม `notes_to_chief/20260824_0038_GT053-RESULT-SCENE2-N106-H1-SURVIVES.md` ·
  ค้น external แล้ว: เจอ inventory/capture scene 2 + `PF_DATA_EVIDENCE.tsv` (Bg0002) แต่ไม่มี placement roster · ค้น gamedata แล้ว: เจอ `SCENE_NAME` แถว `n_ID=2 → s_MODLE_ID=BG0002` + `MOBS n_ID=34` (ยังไม่มี `gamedata\scene\` — `.npc` decode ยังไม่มา) ·
  resolve โฟลเดอร์ด้วย crosswalk จริง: `scene_id 2 → SCENE_NAME → BG0002 → Data\Scene\Save\Bg0002\Bg0002.npc` (11,652 bytes · sha `a649f4af…`) ·
  **N=106 placements** (count field @`0x6E0` = `6A 00`) · parse guard ครบ 106 records จบ exact EOF · index 60 @`0x1CAE`: instance `MOBSET_34 03` · XYZ f32 @`0x1CCA` ตรง P60 authentic **bit-exact** · template key 34 → `MOBS n_ID=34` → preset `M025_001_000_N` ตรง scenario · record attrs มี `3D 00` (=61) ·
  **คำตัดสิน: `0x203D` in-band ของ index 60 ⇒ H1 รอด** (ไม่ยกสูตร `0x2000+p+1` เป็นกฎสากล) · cross-check ท่าอ่านกับ bg0001 GT-048 anchor ตรง · sha ทุกไฟล์ก่อน/หลังตรงกัน

---

## 🆕🔬 GT-054 SPAN-VERIFY-EXTERNAL-REGISTRY [STATIC-ON-BRIDGE]: รัน span verification ของ reader ตัวใหม่กับอิมเมจ client บนสะพาน — พิสูจน์ span_sha256 ของชุดส่งมอบตรงกับไบต์จริงในอิมเมจ  [✅ **PASS/DONE — ผลหน้าสะพาน 2026-08-24 00:33 (+07:00) · บันทึกโดย chief R135 · spans 392/392 verified · mismatch 0 · unreadable 0**]

**Background:** ตาราง `pf_bridge\external\` merge เข้า main แล้ว 2026-08-23 (คำตัดสิน Panya 20:39 +07:00) ·
tool ใหม่ `tools/pf_external_registry.py` ใน `pirate-force-server` = โค้ด reader ตัวแรกที่อ่านชุดส่งมอบจริง ·
มัน pin sha256 ของไฟล์และ cross-check ความสอดคล้องภายในได้บน cloud **แต่ span_sha256 เทียบกับอิมเมจจริงตรวจได้เฉพาะบนสะพานเท่านั้น**
(อิมเมจไม่เคยออกจากเครื่องนั้น) · 🔴 **กฎยืน: verify span sha ก่อนพึ่งแถวใด ๆ เสมอ** — ใบนี้คือการทำกฎนั้นครั้งแรกด้วยโค้ด

**หมวด:** `STATIC-ON-BRIDGE` — ต้องเปิด `GameClient.local.bin` จึงรันบน cloud clone ไม่ได้ · ผู้รับงานคือคนหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม ·
**ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว** · stamp 420 / teardown / canonical DB ไม่เกี่ยวกับใบนี้ (ไม่บูตอะไรทั้งสิ้น)

### ✅ Dependency ปิดแล้ว (R133 · 2026-08-23) — **ใบนี้ runnable แล้ว**
~~tool อยู่บน PR ที่ ต้องผ่าน gate และ merge เข้า `pirate-force-server` main ก่อน~~ ✅ **merge แล้ว:**
PR #12 · head `53ca7ef` เขียว(Actions run 32645331917 · subset) · merge commit `1e0b20b` ·
R133 ยืนยันฝั่ง cloud ที่ commit `1e0b20b` (= `origin/main` ณ เวลาตรวจ — อย่า re-verify ด้วย `git checkout main` บน clone เก่าโดยไม่ fast-forward ก่อน): `tools/pf_external_registry.py` มีจริง + เทส external 16/16 เขียว(cloud sanity) ·
🔴 ก่อนเริ่ม runner ยังต้อง **pull main ล่าสุด** แล้วยืนยันว่า `tools\pf_external_registry.py` มีอยู่จริงบนเครื่องตัวเอง (ถ้าไม่มี = pull ยังไม่ถึง `1e0b20b` · หยุด รายงาน commit ที่ตัวเองเห็น)

### 🔴 ช่องบังคับ (กฎ 18:22): ค้นใน pf_bridge\external\ แล้ว
**เจอ** — ชุดส่งมอบเองคือ object under test ของใบนี้: `PF_SERIALIZER_FIELDS.tsv` (6,931 field rows) ให้ 392 distinct spans ·
ใบนี้ไม่ได้ไปถอดของใหม่ แต่เป็น "verify span sha ของชุดส่งมอบด้วยอิมเมจจริง" ตามกฎยืน

### objective (claim เดียว)
**span_sha256 ของทั้ง 392 distinct spans ในชุดส่งมอบตรงกับไบต์จริงที่ map มาจากอิมเมจ client บนสะพาน** (mismatched=0 และ unreadable=0)

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — รัน tool อ่านอิมเมจ + TSV ส่งมอบอย่างเดียว
🔴 **ห้ามแก้อิมเมจ / TSV ส่งมอบ — tool เปิดอ่านอย่างเดียว · จด sha อิมเมจ+TSV ก่อน-หลังต้องตรงกัน**

### exact command (Windows bridge · cp874-safe · ASCII output)
```
cd <pirate-force-server clone>
py -3 tools\pf_external_registry.py --verify-spans ..\GameClient\GameClient.local.bin
```
สำหรับแนบลงจดหมาย (JSON เต็ม รวม image_sha256 + รายการ mismatched/unreadable):
```
py -3 tools\pf_external_registry.py --verify-spans ..\GameClient\GameClient.local.bin --json
```

### expected output shape (prediction — เขียนไว้ล่วงหน้า)
บรรทัดเดียว: `spans=392 verified=V mismatched=M unreadable=U`
คาดว่า `spans=392 verified=392 mismatched=0 unreadable=0` · **exit code 0 ก็ต่อเมื่อ M=0 และ U=0 เท่านั้น** (M>0 หรือ U>0 => exit 1) ·
🔴 ถ้า tool ตอบ `REFUSED ... exit 3` — **exit 3 มีสองทาง อ่านข้อความก่อนแก้** (R133 ตามที่ adversary จับ):
① `REFUSED: the deliverable tables are not present at ...pf_bridge\external` = tool หา TSV ส่งมอบไม่เจอ —
มันบังคับว่า clone `pf_bridge` ต้องเป็น**โฟลเดอร์พี่น้องชื่อ `pf_bridge` เป๊ะ** ข้างโฟลเดอร์ clone เซิร์ฟเวอร์ (เช็คนี้ยิง**ก่อน**เช็คอิมเมจ) — แก้ตำแหน่ง/ชื่อโฟลเดอร์ bridge ไม่ใช่ path อิมเมจ
② `REFUSED` ที่พูดถึงอิมเมจ = อิมเมจไม่อยู่ที่ path ที่ให้ — แก้ path อิมเมจ
ทั้งสองแบบ = ยังไม่ได้รันจริง อย่านับเป็นผล

### pass criteria — สองชั้นตามบ้าน (ปรับให้เข้ากับใบ static)
**ชั้น 1 (artifact / wire-equivalent — headless ได้ ไม่ต้องพึ่งคน):**
- exit code = 0 · `spans=392` · `verified=392` · `mismatched=0` · `unreadable=0`
- ต้องบันทึกค่า `image_sha256` จากผล tool ลงในจดหมายผล (field มาในโหมด `--json`)
- sha อิมเมจ + TSV ส่งมอบ ก่อน-หลัง ตรงกัน

**ชั้น 2 (human-observable — คนหน้าสะพานต้องทำเอง):**
- runner **paste บรรทัดสรุปเต็ม** (`spans=... verified=... mismatched=... unreadable=...`) **+ `image_sha256`** ลงในจดหมาย
  `notes_to_chief/` ที่ตั้งชื่อด้วย timestamp
- runner **ระบุ commit ของ `pirate-force-server` ที่รัน** (commit hash ที่ pull มา) ในจดหมายเดียวกัน

### 🔴 Failure protocol (ถ้า mismatched>0 หรือ unreadable>0)
- **ห้าม retry ด้วยการ tweak ใด ๆ** · paste รายการ `mismatched_spans` / `unreadable_spans` (จากโหมด `--json`) ลงจดหมายแล้ว **หยุด**
- mismatch = อย่างใดอย่างหนึ่งผิด: **คำอ้างของชุดส่งมอบ** หรือ **การ map section-delta ของเรา (`0x400C00`)** ผิดสำหรับ span เหล่านั้น ·
  chief ต้องเห็นว่าเป็น span ไหนก่อน ห้ามให้อะไรพึ่งแถวเหล่านั้นจนกว่าจะตัดสิน

### 🔴 ผลลบมีค่าเท่าผลบวก
- **mismatched>0** = ข่าวที่มีค่า => ชุดส่งมอบเพี้ยน/อิมเมจคนละตัว/section-delta ผิด — redirect ไปตรวจว่าฝั่งไหนผิดก่อนใช้แถวใด
- **unreadable>0** = ข่าวที่มีค่า => span map ออกนอกไฟล์ => delta หรือ span bound ผิด — จดว่าตัวไหน
- **verified=392 พอดี** = ยืนยันว่าชุดส่งมอบพึ่งได้ที่ระดับ byte-of-span (แต่ดู nonclaims — ไม่ได้แปลว่ารู้ความหมาย)

### nonclaims (ติดไปกับผลทุกกรณี)
- **ผ่านไม่ได้พิสูจน์ความหมายของฟิลด์ (field MEANINGS)** — พิสูจน์แค่ว่าไบต์ของ span ตรง sha
- **ไม่พิสูจน์ว่า client ส่งแถว W จริง** — W row แปลว่า serializer เขียนฟิลด์ได้ ไม่ใช่ว่าไคลเอนต์ส่งจริง
- **ครอบเฉพาะ 392 spans ของ 503 known-serializer messages** — 16 UNKNOWN-serializer messages **ไม่มี span ให้ verify โดยเจตนา** (spanless 32 field rows คือ W+R ของ 16 ตัวนั้น)
- **ไม่ claim เรื่องเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล

- **result:** ✅ **PASS/DONE (2026-08-24 00:33 +07:00)** — จดหมายเต็ม `notes_to_chief/20260824_0033_GT054-RESULT-SPANS-392-VERIFIED.md` ·
  ค้น external แล้ว: เจอ `PF_SERIALIZER_FIELDS.tsv` (object under test) · ค้น gamedata แล้ว: ไม่เจอ (มีแต่ pointer กลับไป external — ถูกต้อง) ·
  รันที่ server main `1e0b20bd240b…` (`pull --ff-only` = Already up to date) · คำสั่งเดียว `--verify-spans … --json` · exit 0 ·
  **`spans=392 verified=392 mismatched=0 unreadable=0`** · `image_sha256 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` ·
  sha อิมเมจ + TSV ทั้ง 5 + tool ก่อน/หลังตรงกันหมด · **ผลนี้ยก span ทั้ง 392 ของ `PF_SERIALIZER_FIELDS.tsv` จาก static-static เป็น verified-กับ-อิมเมจ** (nonclaim: พิสูจน์เฉพาะไบต์ span ไม่ใช่ความหมายฟิลด์/ทิศทาง W · คอลัมน์ VA ของ `PF_PROTOCOL_REGISTRY.tsv` และตารางอื่นของชุดส่งมอบไม่ได้ถูก verify โดยใบนี้)

---

## 🆕🔬 GT-055 STRING-CODEC-DECISION-001 [STATIC-ON-BRIDGE]: ชี้ขาด "รูปเต็ม" ของ string บน wire 2 จุดที่โค้ดเรากับตารางส่งมอบ Codex ขัดกัน — DeleteActorVital 0x36DB และ chat 0xAC52 + ตอบว่าป้าย `UNTAGGED_*` ของชุดส่งมอบแปลว่าอะไรกันแน่  [✅ **PASS/DONE — ผลหน้าสะพาน 2026-08-24 02:41 (+07:00) · บันทึกโดย chief R143 · `0x36DB` = string8 (tag `0x44`) · `0xAC52` = UTF-16LE (tag `0x48`) · `UNTAGGED_*` = ขอบเขต helper ไม่ใช่ full-wire claim · parser เราผิดจริงฝั่ง `0x36DB` — แก้แล้ว: PR โค้ด #16 (`fa1e804`) รอ gate ยังไม่เข้า main ณ R143**]

**Background (R134 · `FINDINGS_R134_EXTERNAL_XCHECK.md` §3):** cross-check โค้ดเรา vs ชุดส่งมอบพบข้อขัดแย้ง
2 จุด และข้อเท็จจริงเชิงระบบหนึ่งข้อที่ครอบทั้งคู่:
- 🔴 **ข้อเท็จจริงเชิงระบบ:** ทั้ง 6,931 แถวของ `PF_SERIALIZER_FIELDS.tsv` ไม่มีแถวไหนมี string tag เลย —
  string ทุกแถวเป็น `UNTAGGED_WSTRING16LE` (348) / `UNTAGGED_STRING8` (60) · แต่ capture เกรด A ของเรา
  บนอิมเมจเดียวกันเห็น wstring **มี tag `0x48` จริง** (GT-006) ⇒ ป้าย `UNTAGGED_*` ผิดเชิงระบบในฐานะ wire claim
  **หรือ**ไม่เคยเป็น wire claim (primitive string อาจปล่อย tag เองข้างใน มุมมอง extractor เลยไม่เห็น)
- **(ก) DeleteActorVital 0x36DB string ท้าย frame:** โค้ดเรา = tag `0x44` + u32 len + UTF-16LE 2 byte/char ·
  ปฏิเสธ len คี่ (`src/pirateforce_foundation/delete_actor.py:90-94`) · ตาราง Codex = `UNTAGGED_STRING8_LEN32LE`
  (1 byte/char) · เคสที่ระบบสองทางมองไม่เห็นและอาจจริงที่สุด: **wire = tag `0x44` + u32 len + string8** —
  ถ้าใช่ parser เราปฏิเสธชื่อความยาวคี่ทุกใบ และอ่านชื่อ ASCII ความยาวคู่เป็น UTF-16 ผิด ๆ = **บั๊กจริง**
- **(ข) chat 0xAC52 wstring header:** ป้าย UNTAGGED ถูกหักล้างในฐานะ wire claim ด้วย capture GT-006 แล้ว
  (byte แรก `0x48` เป็น len=72 ไม่ได้กับ payload 34 ไบต์) — เหลือยืนยันระดับ serializer ในอิมเมจ

**หมวด:** `STATIC-ON-BRIDGE` — ต้องใช้ capture corpus + `GameClient.local.bin` · ผู้รับงานคือคนหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม

### 🔴 ช่องบังคับ (กฎ 18:22): ค้นใน pf_bridge\external\ แล้ว
**เจอ** — แถว `DeleteActorVital` และ `Channel_LocalTalkMessageVital` ใน `PF_SERIALIZER_FIELDS.tsv` คือคู่กรณีของใบนี้เอง
### 🔴 ช่องบังคับข้อสอง (R132): ค้น gamedata แล้ว
**ไม่เจอ** — ใบนี้เป็นเรื่อง wire codec ไม่ใช่ตารางข้อมูลเกม

### objective (claim เดียว)
**บันทึก "รูปเต็มที่วัดได้" ของ string ในสองจุดนี้จากหลักฐาน binary/capture — จุดละหนึ่งแถวคำตอบในรูป
`(tag: 0x44 / 0x48 / ไม่มี) + (ความกว้าง: 1 หรือ 2 byte/char) + (len นับอะไร)` พร้อมไบต์อ้างอิง —
และตอบว่าป้าย `UNTAGGED_*` ของ extractor หมายถึง wire จริงหรือมุมมอง serializer-body**
🔴 **ห้ามตอบเป็น "tagged/untagged" สองทาง** — ระบบคำตอบสองทางทำใบนี้ปิดเขียวปลอมได้ (adversary R134 D2/D3)

### db / server args
**ไม่ใช้ DB · ไม่บูตอะไรทั้งสิ้น** — grep capture corpus + เปิดอิมเมจ/สคริปต์ส่งมอบอ่านอย่างเดียว

### จ็อบ (ทำตามลำดับ)
0. **ความหมายของป้าย UNTAGGED (ตอบก่อน — ราคาถูกสุด):** เปิดเอกสาร .md ประกบตารางในโฟลเดอร์ส่งมอบ
   บนดิสก์สะพาน (`PF_SERIALIZER_FIELDS.md` ฯลฯ) + สคริปต์ `pf_extract_protocol.py` — หาว่า extractor
   สร้างป้าย `UNTAGGED_*` จากอะไร (มัน model tag ไหม หรือมองไม่เห็น tag โดยโครงสร้าง) · paste บรรทัด/โค้ด
   ที่ตัดสินลงจดหมาย
1. **capture (ชี้ขาดเร็วสุดถ้าเจอ):** ค้น corpus (ชุดเดียวกับที่ GT-042 ใช้ · อยู่บนดิสก์สะพาน) หา frame
   0x36DB ที่มี string ไม่ว่าง · **ตำแหน่งที่ดู:** ใน nested vital record ลำดับ field บน wire คือ
   `0x12 id · 0x0B version · 0x08 · 0x08 · 0x14 + ค่า 4 ไบต์` — string เริ่ม **ไบต์ถัดจากค่า 4 ไบต์ของ
   field tag-0x14** (อย่านับ "u32 ที่สาม" — บน wire มี tag-0x14 แค่ตัวเดียว)
   🔴 **deliverable คือ hex paste ± 16 ไบต์รอบจุดนั้น + parse ทีละไบต์ในจดหมาย** — ห้ามรายงานเป็น
   คำตัดสินเปล่า ๆ จากไบต์เดียว (เคสชน: string len 68 = `0x44` ทำ "เห็น 0x44" เกิดได้ทั้งสองสมมติฐาน)
   วัดจาก hex: มี tag ไหม · len นับอะไร · อักขระกว้างกี่ไบต์ (ดูจากมี `00` สลับหรือไม่ + ความยาวรวม)
   · 0xAC52 ใช้ capture GT-006 ที่มีอยู่แล้ว ทำ parse เดียวกันซ้ำเพื่อบันทึกเป็นหลักฐานในใบนี้
2. **ถ้า corpus ไม่มี frame 0x36DB แบบมี string:** ไปที่อิมเมจตรงจุดที่ตารางชี้ให้แล้ว —
   แถว DeleteActorVital ใน `PF_SERIALIZER_FIELDS.tsv` ฝัง `string_wire_call@0x005E4E52 file_off=0x001E4252`
   และ `@0x005E4E85 file_off=0x001E4285` · เปิดอิมเมจที่ file_off ทั้งสอง ดูไบต์รอบ call site ว่ามีการเขียน
   tag ก่อน len หรือไม่ และ primitive ที่ถูกเรียกคือตัว 1-byte หรือ 2-byte (เทียบ pattern กับ call site ของ
   0xAC52: หา `string_wire_call` ในแถว `Channel_LocalTalkMessageVital` แบบเดียวกัน — ตัวนั้นรู้คำตอบแล้ว
   จาก capture ว่าเป็น tag `0x48` + wstring ⇒ ใช้เป็น **ตัวเทียบรูป opcode** ของ "แบบมี tag + 2 byte")
   · จด opcode/hex ± รอบจุด พร้อม file offset — ไม่ต้องใช้ disassembler เต็มตัว เทียบ byte pattern พอ
3. จดคำตอบข้อละแถวตาม objective + คำตอบจ็อบ 0 · ทุกแถวต้องชี้กลับไปที่ hex ที่ paste ไว้

### pass criteria — STATIC-ON-BRIDGE (ชั้นเดียว: หลักฐาน byte-level)
- (ก) และ (ข) มีแถวคำตอบรูปเต็มครบสามช่อง + hex/opcode evidence ที่คนอื่น re-derive ตามได้
  (ระบุไฟล์ capture หรือ file offset ในอิมเมจ) · จ็อบ 0 มีคำตอบพร้อม paste จากเอกสาร/สคริปต์ส่งมอบ
- sha อิมเมจ + TSV ก่อน-หลัง ตรงกัน (เปิดอ่านอย่างเดียว)

### 🔴 ผลลบมีค่าเท่าผลบวก
- **รูปจริง (ก) ≠ ที่ parser เราคาด** (เช่น tag 0x44 + string8): = บั๊กจริงใน `delete_actor.py` —
  chief จะเสนอแพตช์ parser + เทสเป็น PR ผ่าน gate ตาม pattern มาตรฐานเมื่อผลมาถึง
  (แก้ตามหลักฐาน byte-level · fail closed เดิม · ไม่ลบของที่พิสูจน์แล้ว — ถ้า Panya เห็นต่างค้านได้ที่ PR)
- **รูปจริง (ก) = ที่ parser เราคาด**: = ป้าย `UNTAGGED_STRING8` ของชุดส่งมอบผิดในฐานะ wire claim
  อย่างน้อยหนึ่งจุด — รวมกับคำตอบจ็อบ 0 จะบอกว่าแถว `UNTAGGED_*` ทั้ง 408 แถวต้องอ่านยังไงทั้งชั้น
- **หา frame ตัดสิน (ก) ไม่ได้ทั้งสองทาง:** จดว่าค้นอะไรไปบ้าง — เป็นข้อมูลว่า corpus ไม่ครอบ 0x36DB-with-string

### nonclaims (ติดไปกับผลทุกกรณี)
- ใบนี้ตัดสิน **รูป string สองจุดนี้ + ความหมายป้าย UNTAGGED เท่านั้น** — ไม่ตัดสินความหมายฟิลด์
  ไม่ตัดสินแถวอื่นของตารางเป็นรายแถว
- ไม่ claim เรื่องเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล

- **result:** · 🔴 ช่องบังคับ (คำสั่ง 18:22): `ค้นใน pf_bridge\external\ แล้ว: เจอ <อะไร> / ไม่เจอ` ·
  🔴 ช่องบังคับข้อสอง (R132): `ค้น gamedata แล้ว: เจอ <อะไร> / ไม่เจอ` ·
  (ผู้รับงานกรอก: คำตอบจ็อบ 0 + แถวคำตอบรูปเต็ม (ก)(ข) + hex paste · ไฟล์/offset ที่ใช้ · เวลา ·
  sha อิมเมจ+TSV ก่อน-หลัง)

---
## 🆕🔬 RE-056 SKILLCAST-DIRECTION-002 [STATIC-ON-BRIDGE]: ตัดสินทิศทาง (outbound/inbound) ของ `TriggerCastSkillVital` ด้วยวิธีที่ "ผ่านด่านตัวควบคุมก่อน" — ไล่ generic registrar `0x5F3DF0` ว่าเก็บ prototype ที่ตารางไหนและใครเดินตารางนั้น (สายที่ GT-050 ยัง exclude ไม่ได้)  [✅ **DONE/METHOD-FAIL — ผลหน้าสะพาน 2026-08-24 07:28 (+07:00) · บันทึกโดย chief R143 · จ็อบ 0 ตก: registrar = inbound `CreateById` tree — control `PickupTerrainThing` ก็ถูก register ทั้งที่ outbound จริงคือ `0x006B0639`→`0x005DD800` นอก tree ⇒ วิธีนี้จำแนก outbound ไม่ได้ · เลน static ของ direction ปิดถาวรตามเกณฑ์จบใบ · direction `TriggerCastSkillVital` ยังไม่ตัดสิน**]

> 🔢 หมายเหตุเลข (chief): จดหมายต้นเรื่อง `notes_to_chief\20260824_0126_RE055-DRAFT-outbound-census-is-blind-measured-against-a-known-control.md`
> ร่างใบนี้ไว้เป็น RE-055 แต่ 055 ถูกออกเป็น GT-055 (STRING-CODEC-DECISION-001) ไปแล้วใน R134 ก่อนคำสั่งถึงมือ chief
> ตามกฎหัวไฟล์ (ห้ามเปลี่ยนชื่อใบที่ commit แล้ว · prefix RE- เริ่มจริงที่ 056) => ใบนี้คือ RE-056
> เนื้อหาคงตามร่าง 0126 ทุกประการ

ที่มา:
- `notes_to_chief\20260824_0126_RE055-DRAFT-outbound-census-is-blind-measured-against-a-known-control.md` (ร่างใบ + ผลวัดเพดาน)
- ต่อจาก GT-050 จ็อบ 4 (bounded negative · direction ของ `TriggerCastSkillVital` ชนเพดาน static) และ
  `notes_to_chief\20260824_0055_GT050-RESULT-CLEARNRESULT-CLOSED-TRIGGER-DIRECTION-UNRESOLVED.md`

พื้นเรื่อง (re-derive จากไบต์แล้วทั้งหมด · จดหมาย 0126): ปม direction ของ `TriggerCastSkillVital` ไม่ได้อยู่ที่ "ของไม่มี"
แต่อยู่ที่ "วิธีที่ใช้อยู่มองไม่เห็นแม้กับของที่รู้คำตอบ" — จดหมาย 0126 เอาข้อความที่รู้แน่ว่า outbound (`PickupTerrainThing`)
มาผ่านสองวิธีเดินย้อน แล้วทั้งคู่พลาดตัวควบคุม:
- direct `E8/E9` เข้า submit `0x005DD800` ทั้งอิมเมจ = 277 จุด (re-derive อิสระตรงกับ GT-050)
- vtable-literal window scan (0x200 ไบต์ก่อนจุดเรียก submit) ครอบ 23/502 (4.6%) · 🔴 ไม่พบตัวควบคุม
- id_global window scan ครอบ 5/519 (1.0%) · 🔴 ไม่พบตัวควบคุม
- จุดสร้างตัวควบคุม (`0x006B0610`-`0x006B0660`) ไม่อ้าง vtable ของมัน (`0x00F3005C`) และไม่อ้าง id_global ของมัน (`0x0108202C`) เลย
  => การเดินย้อนจาก vtable/id_global โครงสร้างไปไม่ถึงอยู่แล้ว
🔴 สมมติฐานที่ตายแล้ว (จดไว้เพื่อไม่ให้ใครเดินซ้ำ · ห้าม re-walk): literal `0x00F0A8D0` (push 683 จุด) และ `0x00F0A90C`
(push 1,276 จุด) ทั่วไปเกินกว่าจะเป็นตัวระบุรายข้อความ (น่าจะเป็น RTTI/exception record หรือ literal ร่วมของ MSVC)

หมวด: `STATIC-ON-BRIDGE` — เปิด `GameClient.local.bin` อ่านอย่างเดียวบนเครื่องสะพาน จึงทำบน cloud clone ไม่ได้ ·
ผู้รับงานคือคนหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว

### 🔴 ช่องบังคับ (กฎ 18:22): ค้นใน pf_bridge\external\ แล้ว
(ผู้รับงานกรอก: เจอ <อะไร> / ไม่เจอ) — แถว `TriggerCastSkillVital` (serializer `0x00600A60` · vtable `0x00F3175C` ·
id_global `0x0108284C`) อยู่ใน `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv` แล้ว แต่ตารางบอกฟิลด์ ไม่ได้บอกทิศทาง —
ต้องเดินอิมเมจเอง · ถ้าชุดส่งมอบมีแถวที่ระบุ registrar `0x5F3DF0` หรือ dispatch table ใด ให้จดว่ามันตอบอะไรได้ก่อนไปเปิดอิมเมจ
### 🔴 ช่องบังคับข้อสอง (R132): ค้น gamedata แล้ว
(ผู้รับงานกรอก: เจอ <อะไร> / ไม่เจอ) — ชั้น Lua ของ `gamedata\` เห็นจุดเรียกร่ายสกิล 97 จุด (`Player.CastSkillAt` 69 ·
`Trigger.CastSkillXYZ` 11 · `Trigger.CastSkill` 9 · `Trigger.CastSkillBy` 5 · `Party.CastSkillAt` 3) ·
🔴 นี่คือหลักฐานชั้นสคริปต์ ไม่ใช่หลักฐานทิศทางบน wire — คนละชั้น อ้างอิงได้แต่ห้ามเอามาแทนคำตอบของใบนี้

### objective (claim เดียว)
ตัดสินทิศทางของ `TriggerCastSkillVital` (outbound = ไคลเอนต์ส่ง / inbound = ไคลเอนต์รับ) ด้วยวิธีที่ผ่านด่านตัวควบคุม
`PickupTerrainThing` ก่อน — โดยไล่ generic registrar `0x5F3DF0` ว่ามันเก็บ prototype ไว้ที่ตารางไหน และใครเดินตารางนั้น
แล้วสายนั้นวิ่งเข้า outbound submit `0x005DD800` (WRITE) หรือ inbound path (READ)
🔴 คำตอบต้องเป็นประโยคเดียว: `outbound ผ่าน <สาย> ตัวจุดชนวน = <input/timer/...>` หรือ `inbound ผ่าน <สาย>`
หรือ `registrar 0x5F3DF0 ไม่ได้ถือ dispatch ของ outbound (ตัดแนวนี้ทิ้ง)` — ห้ามตอบสองทาง

### db / server args
ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client — เปิดอ่านอิมเมจ + TSV ส่งมอบอย่างเดียว
🔴 ห้ามแก้ อิมเมจ / capture / TSV ส่งมอบ — เปิดอ่านอย่างเดียวทั้งหมด

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- อิมเมจ (sha/size เดียวกับที่ GT-046/GT-048/GT-049/GT-050 พิน): `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  🔴 จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ
- ตัวควบคุม `PickupTerrainThing` (พิสูจน์แล้ว GT-046 · outbound แน่นอน): สร้างที่ `0x006B0639` · เข้าคิวส่งออกที่
  `0x006B0653` · direct `E8 call 0x005DD800` ที่ `0x006B0653` (file offset `0x002AFA53` · bytes `e8 a8 d1 f2 ff`) ·
  ตัวจุดชนวน `WM_LBUTTONDOWN 0x201` · vtable `0x00F3005C` · id_global `0x0108202C`
- เป้า `TriggerCastSkillVital` (จาก GT-050 · verify sha span ก่อนพึ่ง): serializer `0x00600A60` · span `[0x00600A60,0x00600AD7)` ·
  vtable `0x00F3175C` · id_global `0x0108284C` · stream primitive `0x0089A600` (WRITE/outbound) · `0x0089A640` (READ/inbound)
- ท่าทำงาน: ตามวินัย `pf-static-re` · 🔴 ห้ามใช้ linear disassembler เป็นหลักฐานของ negative (บทเรียนรอบ 83) ·
  census ด้วย byte matching (`E8`/`E9 rel32` ทุกออฟเซ็ต) + dword refs + vtable slots

### จ็อบ (ทำตามลำดับ 0 -> 1 -> 2 -> 3 · 🔴 ห้ามข้ามจ็อบ 0)
0. 🔴 ด่านตัวควบคุม (บังคับก่อนแตะเป้า): เอาวิธีที่จะใช้ตอบทิศทาง (ไล่ registrar `0x5F3DF0` ตามจ็อบ 1) มารันกับ
   `PickupTerrainThing` ก่อน — วิธีนั้นต้องบอกได้ว่า `PickupTerrainThing` เป็น outbound (วิ่งเข้า `0x005DD800` ผ่านสายที่
   registrar/dispatch table ชี้) 🔴 ถ้าวิธีนั้นบอกไม่ได้ว่าตัวควบคุมเป็น outbound = วิธีตก หยุดทั้งใบ รายงานว่าวิธีตก
   ห้ามเดินต่อไปที่เป้า (ตัวควบคุมคือของที่เรารู้คำตอบ — ถ้ามองไม่เห็นมัน ผลกับเป้าเชื่อไม่ได้)
1. ไล่ generic registrar `0x5F3DF0` (สายที่ GT-050 บอกเองว่ายัง exclude ไม่ได้): หาว่ามันเขียน prototype ลงตาราง/โครงสร้างไหน
   (dword store ปลายทาง) แล้วใครอ่าน/เดินตารางนั้น (dword ref เข้ามา) · สายที่เดินตารางไปจบที่ `0x005DD800` (WRITE) หรือ
   inbound consumer (READ) · จด VA/file offset/hex +- รอบจุด store และจุด walk ทุกจุด
2. ใช้สายที่จ็อบ 1 พบ ตัดสินเป้า `TriggerCastSkillVital`: prototype ของมัน (vtable `0x00F3175C` / id_global `0x0108284C`)
   ถูก register ผ่าน `0x5F3DF0` ไหม · ถ้าใช่ สายเดียวกันพา object เข้า `0x0089A600` (WRITE) หรือ `0x0089A640` (READ) ·
   ระบุตัวจุดชนวนถ้าเป็น WRITE (input callback แบบ `0x201` ที่ GT-046 เจอ / timer / passive)
3. จดคำตอบเป็นประโยคเดียวตาม objective + สถานะการไล่ indirect (E8/E9 + dword ref + vtable slot · ครบ/ค้าง) ·
   ทุกคำตัดสินต้องชี้กลับไปที่ VA/offset/hex ที่ paste ไว้

### 🔴 ห้ามทำซ้ำ (เพดานวัดแล้ว · จดหมาย 0126)
- ห้ามรัน direct-call census แบบ vtable-literal / id_global window scan ซ้ำแล้วคาดหวังคำตอบอื่น — เพดานถูกวัดแล้ว
  (4.6% / 1.0% · พลาดตัวควบคุมทั้งคู่)
- ห้าม re-walk literal `0x00F0A8D0` (683) / `0x00F0A90C` (1,276) — สมมติฐานตายแล้ว

### pass criteria — STATIC-ON-BRIDGE (VA + offset + hex + re-derive · สองชั้นตามกฎบ้าน)
ชั้น wire/DB (ชั้นเดียวที่ใบนี้ผลิต):
- จ็อบ 0 ต้องผ่านก่อน: วิธีระบุ `PickupTerrainThing` เป็น outbound ได้ พร้อม VA/offset/hex ที่ re-derive ตามได้ ·
  🔴 ถ้าจ็อบ 0 ตก = ใบตกที่วิธี (ไม่ใช่คำตอบเรื่องเป้า) — บันทึกว่าวิธีตกและหยุด
- ตอบทิศทาง `TriggerCastSkillVital` เป็นประโยคเดียว: `outbound ผ่าน 0x0089A600 ตัวจุดชนวน = ...` หรือ
  `inbound ผ่าน 0x0089A640 = ...` หรือ `registrar 0x5F3DF0 ไม่ได้ถือ dispatch ของ outbound => ตัดแนวนี้`
- แนบ VA + file offset + hex +- 16 ไบต์ + (span/sha256 ถ้าอ้าง span) ของ registrar `0x5F3DF0` · จุด store prototype ·
  จุด walk table · และทุกฟังก์ชันที่อ้าง (รูปแบบเดียวกับ GT-046/GT-048/GT-050) ·
  ระบุสถานะการไล่ indirect (ครบ/ค้าง) · sha อิมเมจ+TSV ก่อน-หลังตรงกัน ·
  ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0
- 🔴 ทุกอย่างที่ tool print ลง console ต้องเป็น ASCII (console cp874 บนสะพาน)

ชั้น client-observable: 🔴 ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้ (เหมือน GT-046/GT-047/GT-048/GT-049/GT-050/GT-055) ·
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ผู้เทสหน้าจอไม่ต้องทำอะไรกับใบนี้เลย ·
🔴 ห้ามใครอ้าง static เป็นหลักฐานว่าจอเห็นการร่ายสกิลหรือค่าลด MP/cooldown ใด — คนละชั้นหลักฐาน

### 🔴 ผลลบมีค่าเท่าผลบวก
- "registrar `0x5F3DF0` ไม่ได้ถือ dispatch ของ outbound" = คำตอบที่ใช้ได้เต็ม => ปิดแนว registrar อย่างมีหลักฐาน
  (ต้องแนบว่าไล่ store/walk ครบแล้วจริง · "ไม่พบ" ต้องมากับสถานะ census ครบ ไม่ใช่ค้าง)
- จ็อบ 0 ตก (วิธีมองตัวควบคุมไม่เห็น) = ข่าวที่มีค่า => วิธีนี้ใช้ตอบเรื่องเป้าไม่ได้ · บันทึกว่าวิธีตกที่ไหน
- "ไล่ registrar ครบแล้วยังตัดสินทิศทางเป้าไม่ได้" = ผลที่ใช้ได้ => ดูเกณฑ์จบด้านล่าง

### 🔴 เกณฑ์จบ (บังคับ · ห้ามให้ใบค้างไร้ทางออก)
ถ้า RE-056 ตก (จ็อบ 0 ตก · หรือไล่ registrar ครบแล้วยังตัดสินทิศทาง `TriggerCastSkillVital` ไม่ได้) =>
ปมนี้ออกจากเลน static อย่างถาวร ไม่เปิดใบ static เพิ่มเพื่อไล่ปมเดิมอีก ·
ขั้นต่อไปคือ observe-only attended probe ที่เขียนไว้แล้วแต่ยังไม่เคยรันใน
`pirate-force-server\reports\PF_SKILL001_TRIGGER_AND_STATE_STATIC_CHECKPOINT_20260816.md`
(เลนนั้นวัด runtime ได้จริง ซึ่ง static พิสูจน์ไม่ได้)

### nonclaims (ติดไปกับผลทุกกรณี)
- static image พิสูจน์ได้แค่ว่ามี/ไม่มีเส้นทางในอิมเมจ — ไม่พิสูจน์ว่า runtime เดินสายไหนจริงตอนร่ายสกิล
  (ข้อนั้นเป็นของเลน headless/attended)
- 97 จุดเรียกร่ายสกิลชั้น Lua เป็นหลักฐานว่ามีเส้นทาง "สคริปต์สั่งร่ายสกิล" — ไม่ใช่หลักฐานทิศทางบน wire ·
  ยังไม่มีใครผูกชื่อ API ฝั่งสคริปต์เข้ากับชื่อข้อความฝั่ง wire ได้สักคู่ · ห้ามเอามาแทนคำตอบ
- ตารางมีทั้งแถว W และ R เพราะ serializer ตัวเดียวทำสองทาง — ไม่ได้แปลว่าไคลเอนต์ส่งจริง
- ไม่ claim เรื่องเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล

- **result:** · 🔴 ช่องบังคับ (คำสั่ง 18:22): `ค้นใน pf_bridge\external\ แล้ว: เจอ <อะไร> / ไม่เจอ` ·
  🔴 ช่องบังคับข้อสอง (R132): `ค้น gamedata แล้ว: เจอ <อะไร> / ไม่เจอ` ·
  (ผู้รับงานกรอก: ผลจ็อบ 0 = วิธีระบุตัวควบคุม outbound ได้/ตก · คำตอบทิศทาง `TriggerCastSkillVital` ประโยคเดียว ·
  VA/offset/hex ของ registrar `0x5F3DF0` + store + walk · สถานะ census indirect · ถ้าตกให้ระบุว่าเข้าเกณฑ์จบ
  (ย้ายไป observe-only probe) หรือไม่ · เวลา · sha อิมเมจ+TSV ก่อน-หลัง)

---
## 🆕🔬 RE-057 PLACEMENT-INDEX-CROSSWALK-001 [STATIC-ON-BRIDGE]: หา binding จริง trigger → สคริปต์ → ฉาก บนเครื่องสะพาน แล้วตัดสินว่า literal ใน `Scene.PlacementOFF(N)` ชี้ namespace ไหน (ตัวชี้ขาด: 59/60/61 ของ Bg3002 ที่ไม่มีตาราง commit ใดรองรับ)  [✅ **DONE/STATIC-LANE-CLOSED — ผลหน้าสะพาน 2026-08-24 09:30 (+07:00) · บันทึกโดย chief R144 · `Scene.PlacementOFF`/`ON`/`Cancel` ทั้งสามผูก delegate no-op ตัวเดียวกัน `0x0045FA00` (`xor eax,eax; ret 4`) — ไม่อ่าน argument เลย ⇒ 59/60/61 ไม่มี namespace ใน shipped build · ด่านตัวควบคุมผ่าน (Bg3003/4 ที่อยู่ในช่วงก็ถูก ignore แบบเดียวกัน) · จ็อบ 3–4 N/A — ห้ามผูก band `0x2000+N+1` กับ literal ฝั่งสคริปต์ · ห้ามเปิดใบ static ซ้ำเพื่อไล่ namespace เดิม (งาน prework 09:01 ที่พบ literal เกินขอบทั้งสองแบบ ถูกอธิบายด้วยกลไกเดียวกันนี้)**]

> 🔢 หมายเหตุเลข (chief): จดหมายต้นเรื่อง `notes_to_chief\20260824_0159_PANYA-RULINGS-3-and-RE056-DRAFT-placement-index-crosswalk.md`
> ร่างใบนี้ไว้เป็น RE-056 แต่เลข 056 ถูกออกเป็น **RE-056 SKILLCAST-DIRECTION-002** ไปแล้วใน R136 ก่อนจดหมายถึงมือ chief
> ตามกฎหัวไฟล์ (ห้ามเปลี่ยนชื่อใบที่ commit แล้ว · ตัวนับต่อเนื่องชุดเดียว) => ใบนี้คือ RE-057
> เนื้อหาปรับจากร่าง 0159 ตามข้อเท็จจริงใหม่ R136/R137 (จ็อบ 1 เดิมของร่างถูกตอบไปแล้วบน cloud — ดูพื้นเรื่อง)

ที่มา:
- คำสั่ง Panya 2026-08-24 ~01:5x เลือก "ทาง ก." (ใบเชื่อมเลน Lua `Scene.PlacementOFF` เข้ากับเลน placement index/band ฝั่ง native) ·
  ร่างเต็มใน `notes_to_chief\20260824_0159_PANYA-RULINGS-3-and-RE056-DRAFT-placement-index-crosswalk.md`
- `FINDINGS_R136_LUA_PLACEMENTOFF_XCHECK.md` — หักล้างสมมติฐานสะพานตรง ๆ "literal = `.npc` index" แล้ว
- `FINDINGS_R137_QUEST_CROSSWALK_HUNT.md` — ปิดทางตาราง commit ทั้งหมดแล้ว (ดูพื้นเรื่อง)
- ต่อยอด GT-053 (PASS: `Bg0002` N=106 · band `0x2000+idx+1`) และ `gamedata\PF_LUA_API_SPEC.md`

พื้นเรื่อง (สิ่งที่ตอบไปแล้ว — งานที่เหลือของใบนี้อยู่บนเครื่องสะพานทั้งหมด):
- **R136 (FINDINGS_R136_LUA_PLACEMENTOFF_XCHECK.md):** literal 112 จุดอยู่ใน 4 ไฟล์ `t_clsplc_t1_for_bg300N.lua` เท่านั้น ·
  อีก 61 จุดเป็น `Trigger.VarN` ใน 15 ไฟล์ · ภายใต้ binding จากชื่อไฟล์ (ซึ่งเองก็ยังไม่พิสูจน์ — เป็นเจตนา dev ไม่ใช่หลักฐาน)
  **42/112 หลุดช่วง placement index แบบ 0-based · 40/112 แบบ 1-based** · จุดชี้ขาด: **Bg3002 literal 59/60/61
  ไม่มีคอลัมน์ไหนใน artifact ที่ commit แล้วอธิบายได้เลย** (u16_6 / template_ids / def_count ลองครบแล้ว)
- **R137 (FINDINGS_R137_QUEST_CROSSWALK_HUNT.md):** จ็อบ "หา crosswalk สคริปต์ → ฉากในตาราง commit" ของร่าง 0159 **ตอบแล้ว
  และทางตัน**: crosswalk lua→scene ตัวเดียวในทั้ง 188 ตารางคือ `QUESTDATA_TH__QUEST.tsv` (`n_SCENE` คอลัมน์ 3 ·
  `s_LUASCRIPT` คอลัมน์ 5) และครอบเฉพาะสคริปต์สาย `Quest/` · **สคริปต์ที่เรียก `PlacementOFF` ทั้ง 19 ไฟล์
  (4 ไฟล์ `t_clsplc_t1_for_bg300N` + 15 ไฟล์สาย `Trigger.VarN`) ไม่ปรากฏในตาราง commit ใดเลย** (grep ทั้ง 188 ตาราง = 0) ·
  ตาราง Trigger (`CONSTDATA_TH__Trigger.tsv` · `TEXTDATA_TH__Trigger_TIP.tsv` · 312 แถว) ไม่มีคอลัมน์ฉากและไม่มีคอลัมน์สคริปต์ ·
  59/60/61 ของ Bg3002 ยืนยันซ้ำโดยอิสระว่าไม่มี namespace ฝั่ง commit รองรับ (placements.tsv 39 แถว · max template_ids 58 =
  def_count · MARKER/SCENE_AREA/QUEST ของฉาก 127 ตรวจแล้ว · INSTANCE ไม่มีแถวฉาก 127) ·
  **Bg3004 ไม่อยู่ในตารางใดเลย** (ไม่มีใน `CONSTDATA_TH__SCENE_NAME.tsv` และ `CONSTDATA_TH__MAP_SCENE_LIST.tsv`
  ทั้งที่ `gamedata\scene\Bg3004\` มีจริง) · scene id ที่ยืนยัน: Bg3001=126 · Bg3002=127 · Bg3003=128 (SCENE_NAME แถว 119-121)
- ⚠️ กับดัก census (R137): `gamedata\lua\` มีโฟลเดอร์ย่อย `Quest\` (306 ไฟล์) — glob แบบไม่ recursive จะมองไม่เห็น ·
  (ใน `Quest\` ไม่มีจุดเรียก `PlacementOFF` ⇒ census ของ R136 ยังยืน)
- 🔴 **KILL TEST รันไปแล้ว — อยู่ในพิสัย ≠ หลักฐาน:** `max(literal)=61` <= พิสัย index รวมทุกฉาก 239 พิสูจน์อะไรไม่ได้เลย —
  เลข 13..61 อยู่ในพิสัยของอะไรก็ได้ที่นับถึง 239 · ห้ามใครหยิบข้อนี้มาอ้างเป็นหลักฐาน (กติกาบ้านจาก GT-044:
  เลขอยู่ในพิสัยเดียวกันไม่ใช่ join key — ต้องมี crosswalk field จริง)

หมวด: `STATIC-ON-BRIDGE` — อ่านอิมเมจ client + ไฟล์ฉากต้นฉบับบนเครื่องสะพาน (ส่วนที่ตัวถอด `.npc` ไม่ครอบ) จึงทำบน
cloud clone ไม่ได้ · ผู้รับงานคือคนหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว

### 🔴 ช่องบังคับ (กฎ 18:22): ค้นใน pf_bridge\external\ แล้ว
(ผู้รับงานกรอก: เจอ <อะไร> / ไม่เจอ) — เริ่มที่ `external\00_SEARCH_HERE_FIRST.md` · ถ้าชุดส่งมอบมีแถวที่พูดถึง
trigger data / scene section / placement namespace ให้จดว่ามันตอบอะไรได้ก่อนไปเปิดอิมเมจ
### 🔴 ช่องบังคับข้อสอง (R132): ค้น gamedata แล้ว
✅ **ตอบไปแล้วใน R137** (`FINDINGS_R137_QUEST_CROSSWALK_HUNT.md` — 188 ตาราง grep ครบ · สคริปต์ทั้ง 19 ไฟล์ไม่อยู่ในตารางใด ·
59/60/61 ไม่มีที่มาในของ commit) — **ผู้รับงานไม่ต้อง grep ตาราง commit ซ้ำ** · แต่ต้องกรอกช่องนี้ด้วยสิ่งที่ตัวเอง
**ค้นบนอิมเมจ/ไฟล์ฉากต้นฉบับ** แทน: `ค้นบนอิมเมจแล้ว: <ค้นอะไร ที่ไหน เจอ/ไม่เจอ>`

### objective (claim เดียว)
**literal ที่สคริปต์ส่งให้ `Scene.PlacementOFF(N)` ชี้เข้า namespace ไหน** — ตัดสินด้วย binding จริง trigger → สคริปต์ → ฉาก
ที่หาได้จากเครื่องสะพาน (ไม่ใช่จากชื่อไฟล์) · ตัวชี้ขาดคือ **Bg3002: 59/60/61** — namespace ใดอธิบายสามค่านี้ได้ นั่นคือคำตอบ
🔴 คำตอบต้องเป็นประโยคเดียว: `เป็น placement index เดิมภายใต้ denominator ที่ครบกว่า (พิสูจน์ด้วยตัวอย่างชี้ตัว >=3 จุด ...)`
หรือ `คนละ namespace — คือตาราง/ฟิลด์ <ชื่อจริง+ที่อยู่> (พิสูจน์ด้วย 59/60/61 ...)` หรือ
`binding resolve ไม่ได้แม้บนสะพาน — ปิดเลน static ของคำถามนี้` หรือ
`binding resolve ได้ แต่หา namespace ของ 59/60/61 ไม่พบใน static — เข้าเกณฑ์จบ` — ห้ามตอบสองทาง

### db / server args
ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client — เปิดอ่านอิมเมจ + ไฟล์ฉากต้นฉบับ + TSV อย่างเดียว
🔴 ห้ามแก้ อิมเมจ / ไฟล์ฉาก / TSV ใด — เปิดอ่านอย่างเดียวทั้งหมด

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- อิมเมจ (sha/size เดียวกับที่ GT-046/GT-048/GT-049/GT-050/RE-056 พิน): `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · จด sha ก่อนเริ่มและหลังจบ ต้องตรงกัน
- `gamedata\` @ commit `0801541`: `lua\t_clsplc_t1_for_bg300{1..4}.lua` (literal 112 จุด) · 15 ไฟล์สาย `Trigger.VarN` ·
  `scene\Bg300{1..4}\*.placements.tsv` · `PF_GAMEDATA_LUA_API.tsv` · `PF_GAMEDATA_SCENE_INDEX.tsv`
- ไฟล์ฉากต้นฉบับ (`.npc` และไฟล์ section อื่นของฉาก) บนดิสก์สะพาน — ตัวถอดปัจจุบันครอบเฉพาะส่วน placement ที่มันมองเห็น
  (caveat ของ R136 sec ③: trigger/event placements อาจอยู่ใน section ที่ตัวถอดไม่ครอบ)
- อ่าน `FINDINGS_R136_LUA_PLACEMENTOFF_XCHECK.md` + `FINDINGS_R137_QUEST_CROSSWALK_HUNT.md` ก่อนเริ่ม — ของที่ตายแล้ว/ตอบแล้ว
  อยู่ในนั้นครบ

### จ็อบ (ทำตามลำดับ 1 → 2 → 3 → 4 · จ็อบ 3-4 รันได้ก็ต่อเมื่อ 1-2 ให้คำตอบ)
1. **หา binding จริง trigger → สคริปต์ → ฉาก บนสะพาน** — ที่ที่น่าจะอยู่: section ประเภท trigger/region/event ของ
   ไฟล์ฉากต้นฉบับที่ตัวถอด `.npc` ไม่ครอบ · หรือ trigger data ในไบนารี client · 🔴 **ห้ามเดาจากชื่อไฟล์** (`_for_bg300N`
   คือเจตนา dev ไม่ใช่ binding) · 🔴 **ห้ามกลับไปไล่ตาราง commit ซ้ำโดยไม่มี key ใหม่** — grep ด้วยชื่อไฟล์หมดแล้ว
   (FINDINGS_R137: 188 ตาราง = 0) · **แต่ถ้าได้ ID/key ใหม่จากอิมเมจ** (เช่น script registry ที่ map ชื่อ→เลข)
   **ให้กลับมาไล่ตาราง commit ด้วย key นั้นได้และควรทำ** — ที่ห้ามคือการทำซ้ำแบบเดิม ไม่ใช่การใช้กุญแจใหม่ ·
   binding ที่ได้ต้องชี้ที่มา (ไฟล์/offset/โครงสร้าง) กลับได้ทุกจุด · ถ้าหาไม่ได้ = **หยุด รายงาน** (นั่นคือคำตอบที่ใช้ได้ — ดูเกณฑ์จบ)
2. **หา namespace ที่ literal ชี้เข้า** — เมื่อมี binding จริงแล้ว ให้หาว่าโครงสร้างไหนรับเลข 13..61 · **probe ชี้ขาด:
   Bg3002 ค่า 59/60/61** — namespace ที่อธิบายสามค่านี้ได้คือคำตอบ · ถ้าปรากฏว่า namespace นั้นคือ placement index ของ `.npc`
   เองภายใต้ denominator ที่ครบกว่า (รวม trigger/event placements ที่ตัวถอดเดิมไม่เห็น — caveat ที่ R136 ยอมรับเอง)
   ให้ระบุอย่างนั้นพร้อมตารางฉบับเต็มที่นับได้จริง (แถว/ช่วง/ที่มา)
3. **ยืนยันแบบชี้ตัว >=3 จุด** (ตัวที่ทำให้ใบนี้เป็นข้อพิสูจน์ ไม่ใช่แค่ความสอดคล้อง — จากร่าง 0159 จ็อบ 3):
   เลือกไซต์ที่ resolve ฉาก+namespace ได้อย่างน้อย 3 จุด เปิดแถวที่ index = N จด `name`/`MOBSET`/template ของแถวนั้น
   แล้วดูว่า **บริบทสคริปต์รอบบรรทัดนั้นพูดถึง entity ตัวเดียวกันไหม** ·
   🔴 ตรงทั้ง 3 = ข้อพิสูจน์ · ตรงบ้างไม่ตรงบ้าง = รายงานตามที่เห็น ห้าม force
4. **ผูกกลับไปหา band** — ถ้าจ็อบ 3 ผ่าน ให้ระบุเป็นประโยคเดียวว่า `Scene.PlacementOFF(N)` ชี้ entity ที่ wire เรียกว่า
   `0x2000 + N + 1` หรือไม่ · 🔴 **band ยืนยันจริงเฉพาะ `bg0001` (GT-022/048) และ `Bg0002` (GT-053)** — ฉากอื่นทุกฉาก
   (รวม Bg300N ทั้งหมด) ต้องเขียนกำกับว่าเป็น **อนุมานรูปแบบ** ไม่ใช่ของที่ยืนยันแล้ว

### 🔴 ห้ามทำซ้ำ (ตอบแล้ว/ตายแล้ว)
- ห้าม grep หา crosswalk **ด้วยชื่อไฟล์สคริปต์** ในตาราง commit ซ้ำ — R137 ทำครบ 188 ตารางแล้ว = 0
  (อ้าง `FINDINGS_R137_QUEST_CROSSWALK_HUNT.md`) · ข้อยกเว้น: ได้ ID/key ใหม่จากอิมเมจ ⇒ grep ด้วย key นั้นได้ (ดูจ็อบ 1)
- ห้ามอ้าง kill test "61 <= 239" เป็นหลักฐานทางบวก — วัดแล้ว พิสูจน์อะไรไม่ได้
- ห้าม assume "literal = `.npc` index ตามที่ถอดได้" — หักล้างแล้ว 42/112 (R136) · ถ้าจะกลับมาที่ index เดิมต้องมาพร้อม
  denominator ฉบับเต็มตามจ็อบ 2 เท่านั้น

### pass criteria — ชั้น static ชั้นเดียว
ชั้น wire/DB-equivalent (static · ชั้นเดียวที่ใบนี้ผลิต):
- ตอบ objective เป็นประโยคเดียวได้อย่างใดอย่างหนึ่ง:
  `เป็น index เดียวกันภายใต้ denominator ที่ครบกว่า (พิสูจน์ด้วยตัวอย่างชี้ตัว >=3 จุด: <ไฟล์+บรรทัด+แถว+entity>)` /
  `คนละ namespace — คือ <ตาราง/โครงสร้าง+ฟิลด์จริง ที่อยู่ไฟล์/offset> (พิสูจน์ด้วย 59/60/61 ของ Bg3002)` /
  `binding resolve ไม่ได้แม้บนสะพาน — ตอบไม่ได้จากชั้น static · เข้าเกณฑ์จบ` /
  `binding resolve ได้ แต่หา namespace ของ 59/60/61 ไม่พบใน static — เข้าเกณฑ์จบ (แนบ binding ที่ได้ + รายการที่ค้นครบ)`
- ทุกคำตัดสินชี้กลับไปที่หลักฐาน re-derive ได้: ไฟล์/offset/hex ของ section ที่พบ binding · แถวจริงของ namespace ที่อ้าง ·
  sha256 ของทุกไฟล์ที่พึ่ง ก่อน-หลัง ต้องตรงกัน · ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0
- 🔴 ทุกอย่างที่ tool print ลง console ต้องเป็น ASCII (console cp874 บนสะพาน)

ชั้น client-observable: 🔴 ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้ (เหมือน RE-056/GT-055) ·
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ผู้เทสหน้าจอไม่ต้องทำอะไรกับใบนี้เลย ·
🔴 ห้ามใครอ้างผล static ของใบนี้เป็นหลักฐานว่าจอเห็น placement เปิด/ปิดจริง — คนละชั้นหลักฐาน

### 🔴 ผลลบมีค่าเท่าผลบวก
- **คนละ namespace** = ข่าวใหญ่ ⇒ เลขฝั่งสคริปต์มาจากโครงสร้างอื่น — ต้องระบุชื่อ+ที่อยู่จริง · และเตือนซ้ำ:
  อย่าเอาเลขฝั่งสคริปต์ไปยัดใส่ band ตอนสร้างเซิร์ฟเวอร์
- **binding resolve ไม่ได้แม้บนสะพาน** = คำตอบที่ใช้ได้เต็ม ⇒ ปิดเลน static ของคำถามนี้อย่างมีหลักฐาน
  ("ไม่พบ" ต้องมากับรายการว่าค้น section/โครงสร้างไหนครบแล้ว ไม่ใช่ค้างกลางทาง) — ดูเกณฑ์จบ
- **จ็อบ 3 ตรงบ้างไม่ตรงบ้าง** = ผลตามจริง ⇒ รายงานทุกจุดทั้งตรงและไม่ตรง ห้ามเลือกเฉพาะจุดที่ตรง

### 🔴 เกณฑ์จบ (บังคับ · ห้ามให้ใบค้างไร้ทางออก)
ถ้า RE-057 จบที่ `binding resolve ไม่ได้แม้บนสะพาน` **หรือ** `binding resolve ได้ แต่หา namespace ของ
59/60/61 ไม่พบใน static` ⇒ **คำถามนี้ออกจากเลน static อย่างถาวร** —
ตาราง commit หมดแล้ว (R137) และอิมเมจ/ไฟล์ฉากหมดแล้ว (ใบนี้) · ไม่เปิดใบ static เพิ่มเพื่อไล่ปมเดิมอีก ·
ขั้นต่อไปโดยธรรมชาติคือการวัด runtime (headless หรือ attended — ดูว่า runtime เรียก `PlacementOFF` แล้ว entity ไหนหาย) —
🔴 **แต่ยังไม่เปิดใบนั้นตอนนี้** · จดไว้เป็นคำถามเปิดในผล แล้วรอ Panya ตัดสินทิศทาง

### nonclaims (ติดไปกับผลทุกกรณี)
- **สคริปต์ในไคลเอนต์ = สิ่งที่ไคลเอนต์รู้ ไม่ใช่กฎของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล
- **ไม่พิสูจน์ว่า runtime เรียก `PlacementOFF` จริงตอนเล่น** — พิสูจน์แค่ mapping ของเลขในไฟล์
- **ห้าม join เพราะเลขอยู่ในพิสัยเดียวกัน** — ต้องมี crosswalk field/โครงสร้างจริง (บทเรียน GT-044)
- **ยังไม่มีใครผูกชื่อ API ฝั่งสคริปต์เข้ากับชื่อข้อความฝั่ง wire ได้สักคู่เดียว** — ใบนี้ก็ไม่ได้ทำข้อนั้น
  (จ็อบ 4 ผูกที่ระดับ entity index ไม่ใช่ระดับชื่อข้อความ)
- **ไม่ re-verify band `0x2000+idx+1` เอง** — ใช้ผล GT-022/048/053 เป็น input เท่านั้น · ฉากนอก bg0001/Bg0002
  เป็นการอนุมานรูปแบบเสมอ

- **result:** · 🔴 ช่องบังคับ (คำสั่ง 18:22): `ค้นใน pf_bridge\external\ แล้ว: เจอ <อะไร> / ไม่เจอ` ·
  🔴 ช่องบังคับข้อสอง (R132): `ค้น gamedata แล้ว: ตอบแล้วใน R137 (FINDINGS_R137_QUEST_CROSSWALK_HUNT.md) ·
  ค้นบนอิมเมจแล้ว: <ผู้รับงานกรอก: ค้นอะไร ที่ไหน เจอ/ไม่เจอ>` ·
  (ผู้รับงานกรอก: binding ที่พบ + ที่มา (ไฟล์/offset/hex) · namespace ที่ 59/60/61 ชี้ · คำตอบ objective ประโยคเดียว ·
  ตัวอย่างชี้ตัว >=3 จุดถ้ามี · คำตอบจ็อบ 4 พร้อมป้าย "ยืนยัน/อนุมานรูปแบบ" · ถ้าตกให้ระบุว่าเข้าเกณฑ์จบหรือไม่ ·
  เวลา · sha อิมเมจ+ไฟล์ฉาก+TSV ก่อน-หลัง)

---
## 🆕🔬 RE-058 LEARNSKILL-DIRECTION-001 [STATIC-ON-BRIDGE]: ตัดสิน natural direction ของ `CLearnSkillVital 0x36AA` — client เคย submit มันเข้าเส้น outbound จริงไหม (ครึ่งหลักฐานที่ decoder ฝั่ง server ของ R140 ยังไม่มี)  [✅ **DONE/BOUNDED-NEGATIVE — ผลหน้าสะพาน 2026-08-24 09:14 (+07:00) · บันทึกโดย chief R144 · ไม่พบ exact chain จาก object/vtable `0x00F48E94` เข้า outbound submit `0x005DD800` (constructor callers 3 จุด = pool/registration เท่านั้น) · handler `+0x1C/+0x20` = `return true` stub · แต่ยัง exclude indirect generic-registry path ไม่ได้ ⇒ ไม่ใช่หลักฐาน inbound-only · direction ยังไม่ตัดสิน — nonclaim ของ decoder R140 (LEARN-SKILL-REQUEST-001) คงเดิมทุกตัว · pin correction ติดใบ: vtable จริง `0x00F48E94` (ใบเดิมเขียน `0xF48F00` ซึ่งเป็น name literal)**]

ที่มา:
- R140 เปิดเลนโค้ด **LEARN-SKILL-REQUEST-001 (HYP-PF-034)** — strict decoder ฝั่ง server ของ body 0x36AA
  (`u32 tag 0x14 @+0x14` · `u8 tag 0x0B @+0x18` · 7 ไบต์ · จากแถว W/R สมมาตรใน `external\PF_SERIALIZER_FIELDS.tsv`
  ที่ GT-050 job 1-2 ยืนยัน/re-derive แล้ว) · decoder ยืนบน "client **เขียน** shape นี้ได้" — **ยังไม่มีใครพิสูจน์ว่า client
  เคย **ส่ง** มันจริง** · nonclaim ข้อแรกของโมดูลคือใบนี้
- วิธีวัดลอกจาก GT-050 job 4 (ที่ทำกับ `TriggerCastSkillVital` แล้วได้ bounded negative) — คราวนี้ทำกับ 0x36AA
- `IMAGE_ACCESS_COST.tsv` แถว 2026-08-24T06:1x บันทึกความต้องการนี้ไว้แล้ว

หมวด: `STATIC-ON-BRIDGE` — ต้องเปิดอิมเมจ client จริง (cloud ไม่มีอิมเมจ) · ผู้รับงานคือคนหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม

### 🔴 ช่องบังคับ (กฎ 18:22): ค้นใน pf_bridge\external\ แล้ว
(ผู้รับงานกรอก: เจอ <อะไร> / ไม่เจอ) — จุดตั้งต้นที่รู้แล้ว: `PF_PROTOCOL_REGISTRY.tsv` + `PF_SERIALIZER_FIELDS.tsv`
มีแถว `CLearnSkillVital` (4 field rows) · สิ่งที่ตารางส่งมอบ **ไม่ตอบ** คือ direction — ถ้าเจอแถว/ตารางอื่นที่พูดถึง
producer/consumer ของ 0x36AA ให้จดก่อนเปิดอิมเมจ
### 🔴 ช่องบังคับข้อสอง (R132): ค้น gamedata แล้ว
(ผู้รับงานกรอก) — คาดว่าไม่ตอบ direction (ตารางข้อมูลเกมไม่ใช่โค้ด) แต่ต้องกรอกช่องนี้ตามกฎ

### objective (claim เดียว)
**มี decoded chain จาก object/vtable ของ `CLearnSkillVital` เข้า generic outbound vital submit `0x005DD800` หรือไม่**
คำตอบต้องเป็นประโยคเดียว: `พบ chain outbound (พิกัด: <va ทุก hop>)` หรือ
`bounded negative แบบเดียวกับ GT-050 job 4 — ไม่พบ exact chain และยัง exclude indirect generic-registry ไม่ได้` หรือ
`พบหลักฐานว่าเป็น inbound-only (consumer path + ไม่มี W producer)` — ห้ามตอบสองทาง · ผลลบมีค่าเท่าผลบวก

### db / server args
ไม่ใช้ DB · ไม่บูตอะไรทั้งสิ้น — อ่านอิมเมจอย่างเดียว · sha ก่อน-หลังต้องตรง

### สิ่งที่ต้องมี (precondition)
- อิมเมจ `GameClient\GameClient.local.bin` · size `14759424` · sha256
  `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- pin ตั้งต้น (จาก `tools/pf_stats_progression_static.py` COHORT + `external\PF_SERIALIZER_FIELDS.tsv`):
  serializer `CLearnSkillVital` span `[0x00755AC0,0x00755B13)` len 83 sha256
  `b99487413ffa79784deda46283aafc2f3954d98a85362d35304b745d6c062fc4` · vtable `0xF48F00` · sizeof `0x1C` ·
  get-id stub `0x755AA0` · serializer slot `+0x18` — ยืนยัน pin ก่อนเริ่ม (แบบ GT-050 job 1)
- probe แม่แบบ: `tools\pf_gt050_skill_wire_probe.py` (sha ใน GT-050 letter) — ดัดแปลงเป้าจาก 0x5CD2 → 0x36AA ได้
  แต่ต้องรันในไดเรกทอรีใหม่และห้ามแตะตัวเดิม

### จ็อบ (ลำดับ 1 → 2 → 3)
1. ไล่ slots ของ vtable `0xF48F00` (getter/factory/serializer/consumer) + registration block ที่ยัด literal vtable
   เข้า generic registrar `0x5F3DF0` — จด span/sha ทุกฟังก์ชัน (แบบ GT-050 job 4)
2. **census producer:** byte-wise E8/E9 census หา exact direct caller ของ serializer + factory + chain เข้า
   `0x005DD800` (outbound vital submit) · dword refs ของ vtable literal ใน executable sections ·
   🔴 ห้ามใช้ linear disassembler เป็นหลักฐานของผลลบ (บทเรียนรอบ 83) · recursive CFG decode error ต้อง = 0
3. **census consumer:** slot consumer/handler ของ 0x36AA มี READ path ไหม (แบบเดียวกับที่ GT-050 พบ `0x601810`
   ของ Trigger) — ถ้ามี ให้จดว่า candidate ไปลง state ไหน
- ทุกฟังก์ชันที่อ้าง: แนบ `[start,end)` + file offset + len + sha256 · sha อิมเมจก่อน-หลังตรงกัน

### pass criteria — ชั้น static ชั้นเดียว
- คำตอบ objective หนึ่งประโยค + หลักฐาน span/sha ครบทุก hop ที่อ้าง · ผลลบต้องแนบ census ที่แสดงว่าไล่ครบ
  (จำนวน candidate ที่ตรวจ · เหตุที่แต่ละตัวตก)
- ⚠️ ผลของใบนี้ **แก้สถานะ nonclaim ของ HYP-PF-034**: พบ outbound chain ⇒ decoder ยืนบนหลักฐานจริง (chief จะ
  อัปเดต ledger รอบถัดไป) · พิสูจน์ inbound-only ⇒ เข้าเกณฑ์ falsification ของ entry — **ห้ามผู้รับงานแก้ ledger เอง**

### nonclaims
- ใบนี้ไม่ตอบว่า UI ปุ่มไหนยิง 0x36AA (นั่นคือชั้น runtime/attended) · ไม่ตอบ semantics ของ field ทั้งสอง ·
  ไม่อ้างพฤติกรรมเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล

### result:
(ผู้รับงานกรอก — จดหมายเข้า `notes_to_chief/` ตามปกติ)

---
## 🆕🔬 RE-059 ITEMOPERATE-RES-CAPTURE-BYTES-001 [STATIC-ON-BRIDGE]: ดึงไบต์จริงของ 5 เฟรม `ItemOperateVitalRes` ขา R ที่มีอยู่แล้วใน capture corpus ออกมาเป็น hex — แล้วบอกให้ได้ว่าแต่ละเฟรม `bag_present_flag` เท่าไหร่ · `affected_identity_count` เท่าไหร่ · ItemBagAttr ข้างในหน้าตาอย่างไร  [✅ **DONE — EXTRACTED 5/5 (ผลหน้าสะพาน 2026-08-24 14:13 +07:00 · R149 บันทึก)**]

> ✅ **ผล (จดหมาย `20260824_1413`):** ทั้งห้าเฟรม opcode `0x4C13` ver 2 · `R4=0` · `bag_present_flag=1` ตรงคำทำนาย 5/5 · `affected_identity_count=0` ทุกเฟรม (ไม่มี R11/R12 ให้ตั้งชื่อ) · nested `ItemBagAttr` ยาว 43/52/69/69/43 ไบต์ โครงลงตัวทุกเฟรม: base(`0B u8`,`32 qword`) → update collection(element = `32 qword + 14 u32 + 0F + 0F + 08 + 08 + 0B`) → removal collection · `template_id` ที่พบ: `2600001`, `2400901` (ความหมาย → RE-060) · full hex ทั้งห้าเฟรมอยู่ในจดหมาย · nonclaim: จำกัดที่ 5 เฟรมนี้ ไม่ยกระดับเป็น encoder ทุกทรง

ที่มา:
- `external\PF_FIELD_VALIDATION.tsv` แถว `ItemOperateVitalRes` ทิศ R:
  `observed_frames=5 · parse_success_frames=0 · a2_static_open_frames=5 · mismatch_frames=0 · capture_file_count=4 · status=A2_STATIC_OPEN · source=CAPTURE`
  ⇒ 🔴 **เฟรมจริงมีอยู่แล้ว 5 เฟรม กระจายใน 4 ไฟล์ capture บนเครื่องสะพาน และไม่เคยถูก parse สำเร็จสักเฟรม** · `mismatch_frames=0` = "ถอดไม่ได้" ไม่ใช่ "ขัดกัน"
- GT-054 PASS (392/392) ยืนยัน span ของ serializer `0x005EDA20` แล้ว ⇒ ใบนี้ **ไม่ต้องไปถอด serializer ซ้ำ**
- GT-049 (PASS · ปิดแล้ว) พิสูจน์ static ว่า handler `0x005EF5E0` -> chat emitter `0x005CC309` ยิงข้อความ id 131 `ได้รับ [ $V1 ] * $V2` ได้ — **แต่ไม่ได้พิสูจน์ว่า payload หน้าตาแบบไหนทำให้มันยิง** · ใบนี้คือครึ่งที่หายไปนั้นในชั้นที่ static ทำได้

หมวด: `STATIC-ON-BRIDGE` — capture corpus อยู่บนดิสก์สะพานเท่านั้น (cloud มีแต่ตารางสรุป) · ผู้รับงานคือคนหน้าสะพาน · **ใบนี้ไม่บูตอะไรทั้งสิ้น ไม่มีอะไรให้ดูบนจอเกม** · กติกา stamp/teardown/canonical ไม่เกี่ยวกับใบนี้

### 🔴 ช่องบังคับ (กฎ 18:22): ค้นใน pf_bridge\external\ แล้ว
(ผู้รับงานกรอก: `เจอ <อะไร> / ไม่เจอ`) — สิ่งที่ค้นให้แล้ว ไม่ต้องค้นซ้ำ:
- `PF_PROTOCOL_REGISTRY.tsv`: `ItemOperateVitalRes` · `serializer_va=0x005EDA20` · `handler_va=0x005EF5E0` · `getter_va=0x005EBF70` · `vtable_va=0x00F30668`
- `PF_SERIALIZER_FIELDS.tsv` แถว R เต็ม (ตารางข้างล่าง)
- `PF_PROTOCOL_PRIORITY.tsv`: `serializer_status=OPEN` · blocker 5 ตัว **เป็น blocker ของแถว call ทั้งหมด ไม่ใช่แถวฟิลด์**
- `PF_INPUT_INVENTORY.tsv` = บัญชี capture + sha256 ⇒ ใช้ยืนยันว่า 4 ไฟล์ที่เจอเป็นไฟล์เดิม
- 🔴 สิ่งที่ชุดส่งมอบ **ไม่มี**: **ไบต์ดิบของ 5 เฟรมนั้น** — ตารางเก็บแค่ตัวนับ

### 🔴 ช่องบังคับข้อสอง (R132): ค้น gamedata แล้ว
(ผู้รับงานกรอก) — คาดว่า `gamedata\` ไม่ตอบใบนี้ (ตารางข้อมูลเกมไม่ใช่เฟรม wire) แต่ต้องกรอกตามกฎ · ถ้าถอด `template_id` ออกมาได้ ให้ลองค้นเลขนั้นใน `gamedata\tables\` แล้วจดว่าเจอตารางไหน — 🔴 **แต่ห้ามใช้ผลนั้นสรุปสคีมรหัสไอเทม นั่นเป็นงาน RE-060**

### objective (claim เดียว)
**ไบต์จริงของ 5 เฟรม `ItemOperateVitalRes` ทิศ R ที่มีอยู่ใน capture ถูกถอดออกมาเป็น hex ครบทุกเฟรม พร้อมระบุต่อเฟรมว่า `bag_present_flag` · `affected_identity_count` · ItemBagAttr ข้างในหน้าตาอย่างไร** — หรือรายงานเป็นตัวเลขว่าถอดไม่ได้เพราะอะไร (เฟรมไหนตกที่ไบต์ที่เท่าไหร่ ด้วยเหตุใด)
🔴 คำตอบต้องเป็นประโยคเดียว: `ถอดครบ 5/5` · `ถอดได้ N/5 — เฟรมที่เหลือตกที่ <ออฟเซ็ต> เพราะ <เหตุผลข้อเท็จจริง>` · `ถอดไม่ได้ 0/5 — สาเหตุ <ระบุ> · หาไฟล์เจอ/ไม่เจอ <ระบุ>`

### db / server args
ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์/client — เปิดอ่าน capture + TSV + (ถ้าจำเป็น) อิมเมจ อย่างเดียว · 🔴 **ห้ามแก้ capture · ห้ามแก้ตารางส่งมอบ · ห้ามบูตเกม** · sha256 ของทุกไฟล์ที่พึ่ง ก่อน-หลัง ต้องตรงกัน

### shape ขา R ที่ derive แล้ว (🔴 ห้าม re-derive ซ้ำ · เรียงตาม `file_off_claim` ไม่ใช่ `order` · VA = file_off + 0x400C00)
serializer `0x005EDA20` span `[0x005EDA20, 0x005EDC31)` sha256 `b5f6a1586a810c0a98ceb7c925a0d4afa10cff41db661eb0947b8918f3a11d54` (GT-054 verify แล้ว 392/392) · opcode `ITEM_OPERATE_RES_VITAL = 0x4C13`

| # | file_off | VA | tag | field_offset | len | หมายเหตุ |
|---|---|---|---|---|---|---|
| R1 | 0x001ECE91 | 0x005EDA91 | (indirect call) | `DEREF(DEREF(DEREF(OBJ+0x14))+0x34)` | N/A | blocker |
| R2/R3 | 0x001ECED2/0x001ECEF8 | | (IAT call) | `MSVCR90!_invalid_parameter_noinfo` | N/A | blocker |
| **R4** | 0x001ECF33 | 0x005EDB33 | **0x08** | `+0x30` | 1 | ฟิลด์จริงตัวแรก |
| **R5** | 0x001ECF48 | 0x005EDB48 | **0x0B** | `STACK@0x005EDA20+0x58` | 1 | **= `bag_present_flag`** |
| R6 | 0x001ECF61 | 0x005EDB61 | (direct call) | `0x0046F4D0` | N/A | **nested ItemBagAttr** |
| R7/R8 | 0x001ECF73/0x001ECF81 | | (refcount) | `InterlockedDecrement/Increment` | N/A | blocker |
| R9 | 0x001ECF90 | 0x005EDB90 | (indirect call) | เหมือน R1 | N/A | blocker |
| **R10** | 0x001ECFA2 | 0x005EDBA2 | **0x08** | `STACK@0x005EDA20+0x54` | 1 | **= `affected_identity_count`** |
| **R11** | 0x001ECFBD | 0x005EDBBD | **0x32** | `STACK@0x005EDA20+0x1C` | 8 | ต่อ element — 🔴 `UNKNOWN` ห้ามตั้งชื่อ |
| **R12** | 0x001ECFCD | 0x005EDBCD | **0x08** | `STACK@0x005EDA20+0x1B` | 1 | ต่อ element — 🔴 `UNKNOWN` ห้ามตั้งชื่อ |
| R13 | 0x001ED006 | 0x005EDC06 | (direct call) | `0x005ED2F0` | N/A | blocker |

🔴 **สามข้อควรระวัง:** ① blocker 5 ตัวเป็นของ "แถว call" ทั้งหมด แถวฟิลด์ R4/R5/R10/R11/R12 ไม่ถูกแตะ ② ขา R อ่าน element ลง stack temp (`+0x1C`/`+0x1B`) ส่วนขา W เขียนจากตัว element เอง (`elem+0x10`/`+0x18`) — **อย่าเอาออฟเซ็ตขา W ไปเดินไบต์ขา R** ③ "ItemBagAttr ขนาด `0x68`" = ขนาดในหน่วยความจำ **ไม่ใช่ความยาว wire** — ความยาว wire ต้องออกมาจากเดินไบต์จริง

### คำทำนาย (🔴 นี่คือ **คำทำนาย** ไม่ใช่ข้อเท็จจริง — ทำนายผิด = ผลงาน)
encoder ฝั่งเรา `src/pirateforce_foundation/inventory.py` ประกอบ payload = `u8tag(0x08,0) + u8tag(0x0B,1) + item_bag + u8tag(0x08,0)` ⇒ **ทำนายว่า** ทั้ง 5 เฟรมจะได้ `bag_present_flag=1` และ `affected_identity_count=0` (ไม่มี element R11/R12) · 🔴 **ถ้าเฟรมจริงไม่เป็นตามนี้แม้เฟรมเดียว = ข่าวใหญ่** ⇒ encoder 3 ทรงของเรา (move-delta/swap/merge) สร้างเฟรมที่ client จริงไม่เคยได้รับ — **ผู้รับงานแค่รายงาน ห้ามแก้ encoder/ledger เอง**

### จ็อบ (1 -> 2 -> 3 · จ็อบ 3 รันเมื่อ 2 ติดที่ nested bag)
1. **หา 5 เฟรมให้เจอ** — เดินตามทางที่ `pf_validate_capture_fields.py` ใช้นับ · ระบุ 4 ไฟล์ + sha256 + จำนวนเฟรมต่อไฟล์ (รวม 5) · 🔴 รวมไม่เท่า 5 = หยุดรายงานทันที (ตารางกับ corpus เดินคนละทาง เป็นผลมีค่าในตัว)
2. **dump ไบต์ดิบต่อเฟรม** — เดินไบต์ด้วยมือ R4->R5->R6(nested)->R10->(R11,R12)xcount · จดต่อเฟรม: `0x08@R4` · `bag_present_flag` · ความยาว+hex ของ nested bag · `affected_identity_count` · ค่า R11/R12 · 🔴 ไบต์ไม่ลงตัว = หยุดที่ไบต์นั้น จดออฟเซ็ต/ไบต์ที่เห็น/ไบต์ที่คาด ห้าม "ปรับ" ให้ลงตัว
3. **(เมื่อจ็อบ 2 ติดที่ nested bag)** เปิดอิมเมจอ่าน `0x0046F4D0` · แนบ `[start,end)` + file offset + len + sha256 · recursive CFG decode error = 0 · 🔴 ห้ามใช้ linear disassembler เป็นหลักฐานผลลบ (บทเรียนรอบ 83)

### pass criteria — 🔴 สองชั้น
**ชั้น wire/DB (ชั้นเดียวที่ใบนี้ผลิตหลักฐานได้):** คำตอบ objective ประโยคเดียว · ตารางต่อเฟรม 5 แถว (ไฟล์·sha256·index·opcode·ความยาว·hex เต็ม·`0x08@R4`·`bag_present_flag`·nested-bag len+hex·`affected_identity_count`·element) · ทุกข้อสรุป re-derive ได้ · ถ้าเขียนสคริปต์ commit ลง `tools/` รันซ้ำได้ + guard `frames==5` + exit 0 · 🔴 print ต้อง ASCII ล้วน (cp874)
**ชั้น client-observable: 🔴 ว่างเปล่าโดยเจตนา** — อ่านไฟล์บนดิสก์ล้วน ไม่บูตอะไร ไม่มีจอ · 🔴 ห้ามอ้างผล static เป็นหลักฐานว่าจอเห็นข้อความสีเขียว id 131

### 🔴 ผลลบมีค่าเท่าผลบวก
- ถอดไม่ได้ 0/5 + ตัวเลข = redirect เลนลูททันที (shape จากอิมเมจอธิบายเฟรมจริงไม่ได้) · หาไฟล์/เฟรมไม่ครบ = ตาราง `PF_FIELD_VALIDATION` กับ corpus ไม่ตรง กระทบทุกใบที่พึ่งตัวนับในตารางนั้น รายงานเด่น ๆ · ถอดได้แต่ค่าไม่ตรงคำทำนาย = ข่าวดีที่สุด (encoder เราผิด รู้ก่อนเอาไปให้คนหน้าจอ)

### 🔴 เกณฑ์จบ (บังคับ)
ถ้าจบที่ `ถอดไม่ได้ 0/5` หรือ `ติดที่ nested bag แม้เปิดอิมเมจ` ⇒ คำถาม "payload แบบไหน" ออกจากเลน static (capture หมด + อิมเมจหมด) · **ไม่เปิดใบ static เพิ่ม** · ขั้นต่อไปคือ capture ใหม่แบบ attended (ให้เซิร์ฟเวอร์เราส่ง `0x4C13` แล้วดู client) — 🔴 **ยังไม่เปิดใบนั้น** จดเป็นคำถามเปิดรอ Panya

### nonclaims
ไม่พิสูจน์ความหมายฟิลด์ (R11/R12 ยัง UNKNOWN) · ไม่พิสูจน์ว่า encoder เราถูก/ผิด (แค่ "เฟรมจริงหน้าตาอย่างนี้") · ไม่พิสูจน์ทิศทาง · ไม่พิสูจน์อะไรเกี่ยวกับข้อความบนจอ · capture = สิ่งที่ client เคยได้รับ ไม่ใช่กฎเซิร์ฟเวอร์ต้นฉบับ · 5 เฟรมไม่ครอบทุกทรงของ 0x4C13

### result:
🔴 `ค้นใน pf_bridge\external\ แล้ว: ___` · 🔴 `ค้น gamedata แล้ว: ___` · (ผู้รับงานกรอก: objective ประโยคเดียว · พาธ root capture corpus แบบเต็ม · 4 ไฟล์+sha256+เฟรมต่อไฟล์ · ตารางต่อเฟรม 5 แถว+hex · ผลเทียบคำทำนาย · sha ก่อน-หลัง · จดหมายเข้า notes_to_chief/)

---
## 🆕🔬 RE-060 ITEM-TEMPLATE-CODE-SCHEMA-001 [STATIC-ON-BRIDGE]: pin สคีมรหัสไอเทม `<table_code><5 หลัก>` — `table_code` ตัวไหนหมายถึงตาราง CONSTDATA ตัวไหน (คอมเมนต์ v141:2470 ผิดอย่างน้อยสองจุด)  [✅ **DONE — PINNED 5 CODES (ผลหน้าสะพาน 2026-08-24 14:22 +07:00 · R149 บันทึก)**]

> ✅ **ผล (จดหมาย `20260824_1422`):** `22=EQUIPMENT_BASE` · `24=ITEM_CONSUMABLES` · `25=ITEM_QUEST` · `26=ITEM_MISC` · `35=ITEM_ITEMMALL` (หลักฐานชนิด ค: matrix 7,210 occurrences จาก 120 ตาราง `CONSTDATA_TH` ที่มี `n_ID` — แต่ละ code เหลือ candidate 100%-hit ตารางเดียว) · image ยืนยันกลไกถอด: `full_id / 100000 → runtime table map` (magic จริง `0x14F8B589` — ไม่ใช่ magic ใน hint) · `full_id % 100000 → n_ID` · crosswalk ชื่อ Thai build: join ด้วย `n_ID` (ไม่ใช่ row order — คู่ n_ID=10 พิสูจน์) ผ่าน `PF_GAMEDATA_INDEX.flags: ITEM_MISC → ITEM_MISC_TIP` เช่น `2600001 → Adventure Key` · โบนัส: ข้ออ้าง "packed" ของ TEXTDATA/Lua **หมดอายุแล้ว** (แตกได้จริง) แต่ decoded Lua corpus ไม่มี UI caption assets · nonclaim: ไม่สรุปว่าทั้งเกมมีแค่ห้า code

ที่มา:
- `current/pf_login_game_server_v141.py:2470`: `V103_ITEM_TEMPLATE = 2600001  # STORE_NORMAL row 1 -> ITEM_MISC row 1, Adventure Key` · บรรทัด 2474: `V110_CASK_TEMPLATE = 2400901  # ... ITEM_CONSUMABLES row 901`
- **ลูกมือ static ตรวจแล้ว คอมเมนต์ 2470 ผิดอย่างน้อยสองจุด** (🔴 ห้ามตรวจซ้ำ): ① `2600001` **ไม่ปรากฏเป็น `n_ID` ในตาราง CONSTDATA ใดเลย** (grep = 0 hit) — เป็นค่าที่ถูกอ้างถึง ไม่ใช่คีย์ · ② ไม่ได้อยู่ row 1: อยู่ที่ `STORE_NORMAL.tsv` บรรทัด 2 คอลัมน์ `n_ID_ITEM15` และ `STORE_GOODS.tsv` บรรทัด 154 คอลัมน์ `n_ID_ITEM1`
- ส่วนที่อาจถูก: `ITEM_MISC.tsv` บรรทัด 2 `n_ID=1 · s_NAME=冒險之鑰` · `TEXTDATA_TH__ITEM_MISC_TIP.tsv` บรรทัด 2 `n_ID=1 · s_NAME=Adventure Key` · 🔴 **แต่ไม่มีตารางไหนผูก `26` กับ ITEM_MISC** · `PF_GAMEDATA_INDEX.tsv` ให้ index ITEM_MISC = **042** (ไม่ใช่ 26) · ITEM_CONSUMABLES = **041** (ไม่ใช่ 24) ⇒ `table_code` **ไม่ใช่ index** และ **ไม่ใช่ index+ค่าคงที่** (041->24 ต่าง 1 แต่ 042->26 ต่าง 2)
- prefix ที่วัดได้ในตาราง store: **`26` x261 · `24` x115 · `22` x10 · `35` x4** ⇒ มีสคีม `<table_code><5 หลัก>` แน่ แต่ `table_code -> ชื่อตาราง` ยังไม่มีหลักฐาน
- 🔴 `current/` เป็น **v141 immutable — ห้ามแก้** ⇒ ใบนี้ **หาหลักฐาน ไม่ใช่แก้โค้ด**

### ทำไมสำคัญกว่าที่หน้าตามันดู
`$V1` ในข้อความ id 131 `ได้รับ [ $V1 ] * $V2` **คือชื่อไอเทมที่ไคลเอนต์ resolve เอง** จาก template id ที่เซิร์ฟเวอร์ส่ง (เซิร์ฟเวอร์ไม่ได้ส่งชื่อ) ⇒ **ตีความสคีมผิด = ข้อความขึ้นชื่อผิดตัวหรือไม่ขึ้น** และเลนลูททั้งเลนขี่อยู่บนเรื่องนี้ · 🔴 นี่เป็นข้อผิดที่ **ไม่แสดงอาการตอนเทส wire** — เฟรมถูกทุกไบต์ แต่คนหน้าจอเห็นชื่อผิด

### หมวด
`STATIC-ON-BRIDGE` — จ็อบ 1/3/4 ทำบน cloud ได้ (`gamedata\` เข้า git ครบที่ `0801541`) · **จ็อบ 2 ต้องเปิดอิมเมจ ทำบนสะพานเท่านั้น** · ไม่บูตอะไร ไม่มีจอ

### 🔴 ช่องบังคับ (18:22): ค้นใน external\ แล้ว
(กรอก) — ลอง `PF_DATA_EVIDENCE.tsv` (290 แถวไฟล์ข้อมูลเกม parse แล้ว) · `PF_PROTOCOL_REGISTRY.tsv`/`PF_RUNTIME_CLASSMAP.tsv` คำว่า `Item` · 🔴 `PF_RUNTIME_CLASSMAP.tsv` มี 6,244 แถวแต่ `class_name` เกือบทั้งหมด UNKNOWN

### 🔴 ช่องบังคับข้อสอง (R132): ค้น gamedata แล้ว
(กรอกละเอียด — ใบนี้ค้น gamedata เป็นเนื้องานหลัก) · ค้นให้แล้ว: `2600001` เป็น `n_ID` = 0 hit · `PF_GAMEDATA_INDEX.tsv` คอลัมน์ `start`/`end` = **ออฟเซ็ตในไฟล์ `.dec` ไม่ใช่ VA** · คอลัมน์ `flags` = **ชื่อตาราง TIP คู่ของมัน** (ITEM_MISC -> `ITEM_MISC_TIP`) = crosswalk จริงที่มีชื่อ ไม่ใช่จับคู่เพราะเลขเท่ากัน (บทเรียน GT-044)

### objective (claim เดียว)
**ตาราง `table_code -> ชื่อตาราง CONSTDATA` ถูก pin ด้วยหลักฐาน** — รับได้ 3 ชนิด: (ก) ตัวถอดในไคลเอนต์ · (ข) ตาราง/โครงสร้าง index ที่ผูก code เข้าตาราง · (ค) การนับที่ falsifiable (มาพร้อมกำลังแยกแยะ) — หรือรายงานว่า static ปิดเลนนี้ไม่ได้ พร้อมเหตุผล+รายการที่ค้นครบ
🔴 ประโยคเดียว: `pin ได้ — 26=<ตาราง> 24=<ตาราง> ... (หลักฐาน ก/ข/ค: <ที่อยู่>)` · `pin ได้บางส่วน — ...` · `pin ไม่ได้จากชั้น static — เข้าเกณฑ์จบ`

### db / server args
ไม่ใช้ DB · ไม่บูต — เปิดอ่าน `gamedata\`+`external\`+อิมเมจ · 🔴 **ห้ามแก้ v141 · ห้ามแก้ตาราง · ห้ามแก้อิมเมจ** · sha ก่อน-หลังตรง

### สิ่งที่ต้องมี
`gamedata\` @ `0801541` · อิมเมจ `GameClient.local.bin` size 14759424 sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · ไฟล์ `.dec` ของ CONSTDATA · 🔴 **ห้ามใช้ `parse_pc_tables.py`** (พังกับ CONSTDATA · UnicodeDecodeError) — ใช้ `pf_extract_gamedata.py` หรืออ่าน `tables\*.tsv` ตรง ๆ

### จ็อบ (1 กับ 2 อิสระ)
1. **การนับ falsifiable (ถูกสุด · cloud ทำได้)** — รวบรวมรหัส 7 หลักทุกตัวจากคอลัมน์ไอเทม (STORE_NORMAL.n_ID_ITEM1..20 · STORE_GOODS · DROPS_* · COMBINE · DECOMPOSITION · DAILY_REWARD · ITEM_USING) · จดจำนวนรหัส+ตาราง/คอลัมน์ที่ scan · แยก (code, remainder) · เมทริกซ์ hit rate: code x ตาราง CONSTDATA ที่มี n_ID · 🔴 **hit rate 100% ไม่พอถ้าหลายตารางได้ 100%** (ตาราง n_ID ต่อเนื่อง N ใหญ่ได้ 100% กับอะไรที่เล็กกว่า N — กับดัก GT-044 รูปแบบใหม่) ⇒ รายงานจำนวนตารางที่ได้ 100% ต่อ code · ได้ตารางเดียว = หลักฐาน (ค) ใช้ได้ · หลายตาราง = ตัดสินไม่ได้ พูดตรง ๆ · คำทำนาย (🔴 คำทำนาย): `26->ITEM_MISC` `24->ITEM_CONSUMABLES` (จากคอมเมนต์ที่รู้ว่าไม่น่าเชื่อถือ — เป็นเป้าให้ยิงตก) · `22`/`35` ไม่มีคำทำนาย (น้อยเกิน)
2. **หาตัวถอดในไคลเอนต์ (หลักฐาน ก — แข็งสุด · บนสะพาน)** — หาโค้ดแยกรหัส 2+5 หลักแล้วเลือกตาราง · ร่องรอยให้ลอง (🔴 จุดตั้งต้น ต้องเปิด disassembler ยืนยันเอง): literal `0x000186A0` (=100000) · magic หาร unsigned `0xA7C5AC47` (÷100000) / `0xD1B71759` (÷10000) · switch case `0x16/0x18/0x1A/0x23` · ตัวโหลด CONSTDATA ต่อตาราง · แนบ `[start,end)`+file offset+len+sha256 · CFG decode error = 0 · 🔴 linear disassembler ไม่ใช่หลักฐานผลลบ · "grep ไม่เจอ" ต้องมากับว่า grep อะไร ครอบเท่าไหร่
3. **ทดสอบข้อจำกัดเก่าอาจหมดอายุ** — `tools/pf_split_operate_verb_panels_static.py:33-36` อ้างว่า caption ปิดตายเพราะ `B_TEXTDATA_TH.pc_` packed · 🔴 อาจไม่จริงแล้ว (gamedata แตกออกมา 188 ตาราง + lua 616 ไฟล์) · เช็คสองครึ่ง: (ก) `B_TEXTDATA_TH.pc_` ปิดไหม — หลักฐานว่าไม่ปิด: `TEXTDATA_TH__ITEM_MISC_TIP.tsv` 1,922 แถวอ่าน plaintext ได้ · (ข) UI Lua `.lu_` ปิดไหม — `gamedata\lua\` 616 ไฟล์เป็น UI จริงหรือ quest/trigger (⚠️ กับดัก R137: มีโฟลเดอร์ `Quest\` 306 ไฟล์ · glob ไม่ recursive มองไม่เห็น) · ผลเขียนเป็นข้อเสนอ amend docstring · 🔴 ห้ามผู้รับงานแก้ไฟล์เอง
4. **เดินเส้นทางชื่อจนสุด** — `2600001 -> ITEM_MISC n_ID=1 -> ชื่อ` · 🔴 `ITEM_MISC.s_NAME` = `冒險之鑰` (จีน) แต่ `ITEM_MISC_TIP.s_NAME` = `Adventure Key` ⇒ **ไคลเอนต์ไทยหยิบชื่อจากตารางไหน** คือสิ่งที่ `$V1` แสดงจริง · crosswalk ต้องมีชื่อจริง (`PF_GAMEDATA_INDEX.flags` ผูก ITEM_MISC->ITEM_MISC_TIP) · 🔴 พิสูจน์ว่า join ด้วย `n_ID` ไม่ใช่ลำดับแถว (ITEM_MISC 1,646 vs TIP 1,922 แถว — join ลำดับแถวผิดแน่) ยืนยัน >=3 คู่

### 🔴 ห้ามทำ
ห้ามแก้ v141 · ห้าม grep `2600001` เป็น n_ID ซ้ำ (0 hit แล้ว) · ห้าม join เพราะเลขอยู่พิสัยเดียวกัน (GT-044) · ห้ามสรุปจาก hit rate โดยไม่รายงานกำลังแยกแยะ · ห้ามเดา `table_code`=index (หักล้างแล้ว)

### pass criteria — 🔴 สองชั้น
**ชั้น wire/DB (static/data-equivalent):** objective ประโยคเดียว · ตาราง `table_code->ตาราง` พร้อมป้ายชนิดหลักฐาน (ก/ข/ค) · code ที่ pin ด้วย (ค) ล้วนติดป้าย "หลักฐานเชิงนับ ไม่ใช่ตัวถอด" · เมทริกซ์ hit rate เต็ม + จำนวนรหัส/ตารางที่ scan · คำตอบจ็อบ 3 แยก (ก)/(ข) · จ็อบ 4 + ตัวอย่าง >=3 คู่ · re-derive ได้ · sha ก่อน-หลังตรง · 🔴 print ASCII ล้วน — **สำคัญพิเศษ:** ข้อมูลมีจีน+ไทย ⇒ **ห้าม print `s_NAME` ดิบลง console** ให้ escape/hex หรือเขียนไฟล์ UTF-8
**ชั้น client-observable: 🔴 ว่างเปล่าโดยเจตนา** — อ่านตาราง+อิมเมจบนดิสก์ล้วน ไม่มีจอ · 🔴 ห้ามอ้างเป็นหลักฐานว่า `$V1` ขึ้นชื่อถูกบนจอ — ต้องเป็นใบ attended ใน `GAME_TEST_QUEUE.md` เท่านั้น (ยังไม่เปิด)

### 🔴 ผลลบมีค่าเท่าผลบวก
การนับตัดสินไม่ได้ = บอกเราว่าห้ามใช้การนับ pin สคีมอีก ต้องไปทางตัวถอด · ไม่พบตัวถอด + census = ผลเต็ม · จ็อบ 3 พบข้อจำกัดเก่ายังจริง = docstring ไม่ต้อง amend · คำทำนาย `26->ITEM_MISC` ถูกยิงตก = ข่าวใหญ่สุด (คอมเมนต์ v141 ผิดสามจุด)

### 🔴 เกณฑ์จบ (บังคับ)
จบที่ `pin ไม่ได้จากชั้น static` ⇒ คำถามออกจากเลน static (ตาราง+อิมเมจหมด) · ไม่เปิดใบ static เพิ่ม · ขั้นต่อไป = วัด attended (ส่ง `0x4C13` มี template_id ที่เลือกเอง แล้วดูจอขึ้นชื่ออะไร) — 🔴 ยังไม่เปิดใบนั้น จดคำถามเปิดรอ Panya

### nonclaims
ไม่พิสูจน์ว่าเซิร์ฟเวอร์ต้นฉบับใช้สคีมนี้ (พิสูจน์แค่ไคลเอนต์/ข้อมูลเกมที่ ship มาเข้าใจแบบไหน) · ไม่พิสูจน์ว่าจอขึ้นชื่อถูก · ไม่พิสูจน์ความหมายคอลัมน์อื่น (GT-052) · ไม่แก้ ledger/HYP · ไม่ครอบ table_code ที่ไม่อยู่ในตาราง store (วัดได้แค่ 4 code — 🔴 ห้ามสรุปว่ามีแค่ 4 code ในเกม)

### result:
🔴 `ค้นใน external\ แล้ว: ___` · 🔴 `ค้น gamedata แล้ว: ___` · (กรอก: objective · ตาราง table_code->ตาราง+ป้ายชนิด · เมทริกซ์ hit rate+จำนวน scan · VA/span/sha ตัวถอด (หรือ census) · จ็อบ 3 แยก (ก)/(ข)+ข้อเสนอ docstring · จ็อบ 4 ว่า `$V1` มาจากคอลัมน์ไหน+>=3 คู่ · ผลคำทำนาย 26->ITEM_MISC · sha ก่อน-หลัง · จดหมาย notes_to_chief/)

## 🆕🔬 RE-061 SKILLSTATE-WIRE-DIRECTION-001 [STATIC-ON-BRIDGE]: ปิด outbound wire shape ของ `CSkillModule` (vtable 0x00F48D88 slot +0x18) แบบไบต์เป๊ะ + หา carrier ของ `CSkillAttr` (vtable 0x00F48B78, chains DBAttribute) + ตัดสินจากอิมเมจว่าไคลเอนต์มี inbound decoder + skill-window-open ขึ้นกับ skill state ไหม (🔴 corpus เป็น emulator-only ตอบ direction ของ server ต้นฉบับไม่ได้ — SCENE-013) — ทดสอบ wire premise ของ root-cause "server ไม่เคยส่ง skill state"  [✅ **DONE — STATIC POSITIVE `CSkillAttr` / STATIC NEGATIVE `CSkillModule` (ผลหน้าสะพาน 2026-08-24 14:37 +07:00 · R149 บันทึก)**]

> ✅ **ผล (จดหมาย `20260824_1437` · ผู้ทำ: Codex local):** ผลออกทาง **บวก** ตามเงื่อนไข R146 ⇒ chief เปิดเลนโค้ด sender แล้ว (R149):
> - **`CSkillModule` ว่างจริง**: vtable `0xF48D88+0x18` = `mov al,1; ret 4` (0 fields · 0 body bytes) · `+0x1C` = bare `ret 4` ⇒ ไม่มี frame body และไม่มี inbound apply · `0x1F7B` เป็น name-hash ไม่ใช่ opcode
> - **`CSkillAttr` ขี่ `UpdateAttrVital 0x309A`** เป็น attr block `class_id 0x1661` (ไม่ใช่ standalone opcode): frame = `0x309A → 0x12 attr_count → 0x12 class_id(0x1661) → 0x14 body_len → [0x0B db_mask → (bit0: 0x32 identity) → 0x12 record_count → N×(0x12 key · 0x12 opaque_u16 · 0x14 opaque_u32)]` · serializer `0x7520B0` · inbound apply มีจริง (`0x5F2400` → `+0x24 = 0x751C70` · bind thunk อ่าน `[actor+0x3E8]`)
> - **gate ของหน้าต่าง Skill พิสูจน์แล้ว**: K (key 75 → `ABILITY`) และปุ่ม `Bt_main_Skill` เปิดชื่อเดียวกัน `Skill_Main2` · controller ctor `0x760DE0` อ่าน `[actor+0x3E8]` (=`CSkillAttr`) · init `0x761ED0` **คืน false ถ้า `controller+0x88` เป็น null** ⇒ `CSkillAttr` เป็น prerequisite ที่ falsifiable
> - nonclaims สำคัญ: one packet ไม่ถูกพิสูจน์ว่า "เพียงพอ" ให้ K เปิด (มี base/UI checks อื่น) · opaque u16/u32 ยังไม่มีชื่อ · corpus ตอบ direction ต้นฉบับไม่ได้ (UNANSWERABLE ตาม SCENE-013)

ที่มา (ทำไมใบนี้ถึงเกิด — ฉบับสั้น):
- ใบ attended **GT-058** (คิว `GAME_TEST_QUEUE.md`) ค้าง เพราะหน้าต่าง Skill (ฮอตคีย์ **K**) ไม่ยอมเปิดใน baseline ท้องถิ่นของเรา
- cloud audit (จดหมาย `20260824_1119` + CORRECTION `20260824_1147`) root-cause ว่า: **server ของเราไม่เคยส่ง skill STATE ให้ client เลย** — คลาส `CSkillModule` และ `CSkillAttr` · client มีข้อมูลสกิลครบ (`SKILL_CONTEXT` 2,165 แถว + ไอคอน จาก GT-052) ⇒ **ฟีเจอร์ไม่ได้ถูกปิด** · หน้าต่างไม่มีอะไรให้ populate เพราะไม่มี skill-state vital วิ่งมาถึง
- 🔴 root-cause นี้เป็น **HYPOTHESIS ยังไม่ได้พิสูจน์** · ใบนี้คือใบที่ทดสอบ **wire premise** ของมัน
- แก้จริงเป็นงานเลนโค้ดฝั่ง server (ตัวส่ง) แต่เลนโค้ด **สร้าง sender ไม่ได้** จนกว่า outbound WIRE SHAPE ของสองคลาสนี้จะถูกปิดจากอิมเมจ client — ท่าเดียวกับ GT-050
- บน cloud clone ปิดไม่ได้ (bounded-negative แล้ว · ยืนยันด้วย pf-static-re R146): **ชุดส่งมอบ RE ของ Codex มี `CSkillModule`/`CSkillAttr` เป็น serializer row EMPTY** (`PF_SERIALIZER_FIELDS.tsv`) และ **capture = NOT_OBSERVED 0 เฟรม** (`PF_FIELD_VALIDATION.tsv`) และ `PF_RUNTIME_CLASSMAP` ค้น "Skill" = 0 แถว ⇒ **ต้องปิดจากอิมเมจบนสะพาน** ไม่ใช่จากชุดส่งมอบ

ข้อเท็จจริงที่ resolve แล้ว (ส่งให้ผู้รับงาน จะได้ไม่ derive ซ้ำ — 🔴 pin ทุกตัวยังต้อง verify-first แบบ GT-050 job 1):
- `CSkillModule`: `FACTPACK_L2_CLASSCENSUS001_20260820.tsv` **row 300** — family `module_subsystem` · vtable **0x00F48D88** · RTTI `.?AVCSkillModule@@` · rtti_va `0x0101E180`
  🔴 **id `0x1F7B` เป็น name-hash candidate เท่านั้น ไม่ใช่ opcode ที่พิสูจน์แล้ว** — FACTPACK L4 เขียนเอง: *"wire_id is DERIVED from the name by the round-62 hash. It is NOT read from any table in the image"* · แถวนี้ `in_names_table=False` และ `in_round38_tsv=False` (ไม่อยู่ทั้งใน registry และ name table) ⇒ **ห้ามใช้ 0x1F7B เป็น opcode จนกว่าจะเจอในตาราง dispatch จริงในอิมเมจ**
  🔴 **`0x00F48E84` ที่ FACTPACK บันทึกคือ `literal_va` (name-literal VA) ไม่ใช่ vtable ตัวที่สอง** — ระวังเหมือน erratum RE-058 (`0xF48F00` เคยถูกเขียนผิดเป็น vtable ทั้งที่เป็น name literal) · vtable จริงที่จะไล่ serializer คือ `0x00F48D88`
- `CSkillAttr`: family `attr_state_block` (Attr — state block ผูกกับ actor · sibling ของ `BasicAttr` / `CBuffAttr` / `CCooldownAttr`) ⇒ **น่าจะขี่มากับ collection แบบ ActorAttr ไม่ใช่ standalone opcode** — 🔴 ผู้รับงานต้องยืนยันเอง
  pin ที่มีแล้ว (จาก `external/PF_PROTOCOL_REGISTRY.tsv` L503 + reports STATS-PROG001/MPAUDIT/CHUNK2): vtable **0x00F48B78** · `Serialize` **0x7520B0** · chains `DBAttribute` · bind กับ `CMyActor` ที่ `actor+0x3E8` · bind thunk `0x4698B0` · 🔴 id/hash `0x1661` เป็น name-hash candidate (ไม่ใช่ opcode) · 🔴 STATS-PROG001 report ปฏิเสธ object offset ไว้ชัด (*"No CSkillAttr object offset is claimed"* — serializer stage ค่าผ่าน stack temp, displacement เป็น ESP/EBX-relative)
  รูปบางส่วนที่จดไว้แล้ว (`EXPERIMENT_LEDGER.md` L45 SKILL-001): `u16 count` + container ของ `(key u16, opaque u16, opaque u32)` — **แต่ไม่มี opcode และไม่มี object offset ⇒ ประกอบเฟรม byte-exact ไม่ได้** ⇒ นี่คือสิ่งที่ใบนี้ต้องปิดให้ครบ
- 🔴 **caution — serializer stub ในอิมเมจ:** `PF_SERIALIZER_FIELDS.tsv` บันทึก serializer ของสองตัวนี้เป็น EMPTY stub: `CSkillModule` `@0x00710440` = `write_al_1_then_ret_4` (ตั้ง AL=1 แล้ว ret 4 — ไม่ปล่อย field เลย) · `CSkillAttr` `@0x0043BB80` = empty arg copier · **สอง address นี้อาจไม่ใช่ serializer จริงของ skill-state** (อาจเป็น container/ตัวห่อ) ⇒ ต้องไล่จาก vtable slot +0x18 เอง · **ถ้า serializer จริงก็เป็น stub ที่ไม่ปล่อย field จริง = ข่าวใหญ่** (แปลว่า skill state อาจเดินทางทางอื่นทั้งหมด เช่นใน ActorAttr collection)
- วิธีพิสูจน์แล้วสามครั้ง (GT-040/042/046/050): vtable -> serializer slot **+0x18** -> เดิน field tag/offset/len · W serializer อยู่แถบ **0x0089A600** · R serializer อยู่แถบ **0x0089A640** (ตาม GT-050)

หมวด: `STATIC-ON-BRIDGE` — ต้องเปิดอิมเมจ client จริง + capture corpus บนสะพาน (cloud ไม่มีทั้งอิมเมจและ corpus) · ผู้รับงานคือคนหน้าเครื่องสะพานของ Panya ไม่ใช่ผู้เทสหน้าจอเกม · **ใบนี้ไม่บูตเกม · ไม่จับ `LOCK_GAME` · ไม่มี teardown · ไม่แตะ canonical DB · ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว**

### 🔴 ช่องบังคับ (กฎ 18:22): ค้นใน pf_bridge\external\ แล้ว
(ผู้รับงานกรอก: `เจอ <อะไร> / ไม่เจอ`) — จุดตั้งต้นที่รู้แล้ว จาก GT-052 + pf-static-re R146: `PF_PROTOCOL_REGISTRY.tsv` มี `CSkillAttr` (L503, vtable 0x00F48B78) + `CSkillModule` (L504, vtable 0x00F48D88) · `PF_SERIALIZER_FIELDS.tsv` field rows ของทั้งสอง = **EMPTY** · `PF_FIELD_VALIDATION.tsv` = **NOT_OBSERVED 0 เฟรม** · `PF_RUNTIME_CLASSMAP.tsv` ค้น "Skill" = **0 แถว**
- 🔴 งานของใบนี้คือ **ปิด span จากอิมเมจ** ไม่ใช่ปิดจากชุดส่งมอบ (ชุดส่งมอบว่างแล้ว)

### 🔴 ช่องบังคับข้อสอง (R132): ค้น gamedata แล้ว
(ผู้รับงานกรอก) — คาดว่า `gamedata\` **ไม่ตอบ wire shape/direction** (ตารางข้อมูลเกมไม่ใช่โค้ด/เฟรม · GT-052 ปิด SKILL_CONTEXT แล้ว) แต่ต้องกรอกช่องนี้ตามกฎ · 🔴 ห้ามใช้ค่าในตารางข้อมูลเกมมาตั้งชื่อ/ชนิด field บน wire

### objective (claim เดียว)
**outbound serializer field layout ของ `CSkillModule` (จาก vtable 0x00F48D88 slot +0x18) ถูกปิดแบบไบต์เป๊ะ · carrier ของ `CSkillAttr` ถูก resolve (เป็น attr block ใน collection หรือ standalone) · และไคลเอนต์มี inbound decode/apply path ของสองคลาสนี้ไหม + โค้ดเปิดหน้าต่าง Skill (K) ขึ้นกับ state นั้นไหม (static จากอิมเมจ)**
🔴 คำตอบต้องเป็นประโยคเดียว 3 ส่วน:
- `CSkillModule W layout = [tag/offset/len ...] span [start,end) sha <...>` (หรือ "serializer เป็น stub ไม่ปล่อย field — <span/sha>")
- `CSkillAttr carrier = attr block ใน <collection id / mask bit / tag chain>` **หรือ** `standalone opcode <id>` **หรือ** `resolve ไม่ได้ + census ที่ไล่ครบ`
- `client apply = มี inbound decoder ของ CSkillModule/CSkillAttr ที่ <VA> และโค้ดเปิด skill-window อ่าน state นั้นที่ <VA/gate>` **หรือ** `ไม่พบ decoder/ไม่พบ gate (census ไล่ครบ)` — 🔴 **นี่คือหลักฐาน direction ที่ falsifiable ได้จริง ไม่ใช่ corpus** (ดู 🔴 CORPUS ELIGIBILITY)

### db / server args
ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client — เปิดอ่านอิมเมจ + capture + TSV ส่งมอบอย่างเดียว
🔴 **ห้ามแก้ อิมเมจ / capture / TSV ส่งมอบ — เปิดอ่านอย่างเดียวทั้งหมด** · sha256 ของทุกไฟล์ที่พึ่ง ก่อน-หลัง ต้องตรงกัน

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- อิมเมจ (sha/size เดียวกับ GT-046/048/049/050/058): `GameClient\GameClient.local.bin` · size `14759424` · sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000` · 🔴 จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง
- stream primitive (พิสูจน์แล้วตั้งแต่ GT-040): `0x0089A600` (WRITE / outbound) · `0x0089A640` (READ / inbound)
- capture corpus บนสะพาน: `PF_INPUT_INVENTORY.tsv` = บัญชี capture + sha256 · ระบุ **พาธ root corpus แบบเต็ม** ในผล — 🔴 อ่าน CORPUS ELIGIBILITY ก่อนใช้
- 🔴 **CORPUS ELIGIBILITY (บังคับอ่านก่อนแตะ capture):** corpus ที่มีทั้งหมดเป็น **client ↔ emulator ของเราเอง** ไม่ใช่ traffic ของ server ต้นฉบับ (`pirate-force-server/docs/EXPERIMENT_LEDGER.md` **SCENE-013**: *"All six are GameClient -> local-emulator receive logs; eligible original server -> client frames are zero … `bounded_target_negative=false`: this proves the curated corpus cannot answer the inbound question, not that any packet is absent from the real protocol"*) · ⇒ **corpus พิสูจน์ไม่ได้ว่า server ต้นฉบับส่ง skill state หรือไม่** — emulator เราไม่เคยส่ง (นั่นคือ premise ของใบนี้) ดังนั้น "ไม่เจอเฟรมใน corpus" = **การยืนยัน premise ซ้ำ ไม่ใช่หลักฐาน** · corpus ใช้ได้แค่ **corroboration** และ **ต้องทำ eligibility pre-check ก่อน:** corpus มีเฟรม S->C ของ server ต้นฉบับ (ไม่ใช่ emulator) แม้แต่เฟรมเดียวไหม — ถ้าไม่มี ให้บันทึกว่า **corpus UNANSWERABLE** ห้ามบันทึกเป็น bounded-negative
- 🔴 **ระวัง false positive:** corpus มีเฟรม S->C `0x673C` (CLearnSkillResultVital) จริง 5 เฟรมอยู่แล้ว (GT-058) — แต่นั่นคนละ vital · เพราะ id ของ CSkillModule/CSkillAttr เป็น name-hash candidate จึง **ไม่มี opcode filter ที่เชื่อได้** ⇒ ห้ามนับเฟรม skill-family ใด ๆ เป็น positive จนกว่าจะพิสูจน์ด้วยรูป body จาก Tier A ว่าเป็น body ของสองคลาสนี้จริง
- ท่าทำงาน `pf-static-re` · probe แม่แบบ `tools\pf_gt050_skill_wire_probe.py` (sha ในจดหมาย GT-050) — ดัดแปลงเป้าได้ แต่รันในไดเรกทอรีใหม่ ห้ามแตะตัวเดิม
- 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative** (บทเรียนรอบ 83) · census ด้วย byte matching (E8/E9 rel32) + dword refs + vtable slots · recursive CFG decode error ต้อง = 0

### จ็อบ (ลำดับ 1 -> 2 -> 3 -> 4 · 🔴 ห้ามข้ามข้อ 1)
1. **verify pin ก่อน** — ยืนยัน vtable `0x00F48D88` เป็นของ `CSkillModule` จริง (RTTI `.?AVCSkillModule@@`) และ vtable `0x00F48B78` เป็นของ `CSkillAttr` จริง · 🔴 ไม่ตรง = หยุด รายงาน pin ที่เพี้ยน ห้าม derive ทับ · 🔴 อย่าเชื่อ id 0x1F7B/0x1661 เป็น opcode
2. **trace outbound serializer ของ `CSkillModule`** — จาก vtable `0x00F48D88` slot `+0x18` เดิน field: tag/offset/len · ลำดับ body · ความกว้างต่อ field · แนบ span `[start,end)` + file offset + len + sha256 ของ **ทุก** ฟังก์ชันที่อ้าง · 🔴 ถ้า slot +0x18 ชี้ไป stub `0x00710440` (write_al_1_then_ret_4) จริง ให้ยืนยันว่าเป็น stub ไม่ปล่อย field แล้วไล่ว่าใครเรียก serializer จริงของ skill state แทน
3. **resolve wire form ของ `CSkillAttr`** — จาก vtable `0x00F48B78` / `Serialize 0x7520B0`: เป็น attr block ที่ emit ใน collection แบบ ActorAttr (ระบุ **mask bit / collection id / tag chain**) หรือ standalone · แนบ span+sha · 🔴 resolve ไม่ได้ = รายงาน census ที่ไล่ครบ (candidate + เหตุที่ตก)
4. **CLIENT APPLY + WINDOW-OPEN GATE (static · หลักฐาน direction ตัวหลัก)** — จากอิมเมจ: ไคลเอนต์มี inbound decoder ของ `CSkillModule`/`CSkillAttr` ไหม (VA) · โค้ดที่เปิดหน้าต่าง Skill (K) อ่าน/gate บน skill state นั้นไหม (VA/เงื่อนไข) · 🔴 นี่ตอบคำถามจริงที่ต้องการ: "ถ้า server ส่ง state จะปลดหน้าต่างไหม" ได้แบบ falsifiable โดยไม่พึ่ง corpus · ถ้าไม่พบ decoder หรือ window-open ไม่ขึ้นกับ state = census ต้องไล่ครบ (candidate + เหตุที่ตก)
   - **corpus = corroboration only:** หลัง eligibility pre-check (ดู precondition) ถ้า corpus มีเฟรม S->C ของ server ต้นฉบับจริง ค่อยค้น body ของสองคลาสนี้ พร้อม hex · 🔴 ถ้า corpus เป็น emulator-only = บันทึก **UNANSWERABLE** ไม่ใช่ bounded-negative

### pass criteria — 🔴 สองชั้น (Tier A / Tier B แยกกัน ห้ามเอาชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
**Tier A (wire/static):**
- serializer field layout ของ `CSkillModule` ปิดแบบไบต์เป๊ะ (หรือพิสูจน์ว่าเป็น stub ไม่ปล่อย field พร้อมชี้ตัวปล่อยจริง) + span `[start,end)` + file offset + len + sha256 ครบทุกฟังก์ชันที่อ้าง
- carrier ของ `CSkillAttr` resolve (attr block ใน collection พร้อม mask/collection-id/tag-chain · หรือ standalone · หรือ census-ไล่ครบ-แต่ปิดไม่ได้พร้อมเหตุ)
- image sha256 ก่อน==หลัง · TSV ส่งมอบที่เปิดอ่าน sha ก่อน==หลัง
- 🔴 linear disassembler ไม่ถูกใช้เป็นหลักฐานของผลลบ (รอบ 83) · CFG decode error = 0 · ถ้าเขียนสคริปต์ commit ลง `tools/` รันซ้ำได้ + guard count + exit 0 · 🔴 print ASCII ล้วน (cp874)
**Tier B (client apply + window-open gate · static · corpus = corroboration only):**
- หลักฐานตัวหลักคือ static จากอิมเมจ: มี/ไม่มี inbound decoder ของ CSkillModule/CSkillAttr (VA) และ skill-window-open ขึ้นกับ state นั้นหรือไม่ (VA/gate) — census ไล่ครบพร้อม span/sha
- corpus (ถ้าผ่าน eligibility) = corroboration: เฟรม S->C ของ server ต้นฉบับที่แบก body ถูก quote เป็น hex (ไฟล์+sha256+index+ทิศ+hex, พิสูจน์ว่าเป็น body สองคลาสนี้ด้วยรูปจาก Tier A) · 🔴 corpus emulator-only = **UNANSWERABLE** ไม่ใช่ bounded-negative
- 🔴 Tier A **ไม่ใช่** หลักฐานของ Tier B และกลับกัน — มี serializer ในอิมเมจ ไม่ได้แปลว่า server เคยส่ง · ไม่พบ decoder/gate ไม่ได้แปลว่า serializer ไม่มี

**ชั้น client-observable: 🔴 ว่างเปล่าโดยเจตนา** — อ่านอิมเมจ+capture บนดิสก์ล้วน ไม่บูตอะไร ไม่มีจอ (เหมือน GT-046/050/058/059/060) · ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย** · 🔴 ห้ามใครอ้าง static/capture เป็นหลักฐานว่าหน้าต่าง Skill (K) เปิดหรือ populate ได้ — นั่นเป็นชั้น attended ของ GT-058

### 🔴 ผลลบมีค่าเท่าผลบวก
- **ไคลเอนต์ไม่มี inbound decoder ของสองคลาสนี้ / skill-window-open ไม่ขึ้นกับ state นั้น** (static census ไล่ครบ) = คำตอบที่ใช้ได้เต็มร้อย ⇒ **การส่ง state จะไม่ปลดหน้าต่าง** ⇒ ตัวขวางมีสาเหตุอื่น การสร้าง sender จะไม่ปลด GT-058
- 🔴 **"ไม่เจอเฟรมใน corpus" ตัวมันเอง ไม่ใช่ผลลบที่ใช้ได้** — corpus เป็น emulator-only (SCENE-013) จึงได้ผลนี้แน่นอนไม่ว่าความจริงจะเป็นอย่างไร ⇒ บันทึกเป็น **UNANSWERABLE** และ **ห้ามใช้มันสรุปว่าตัวขวางมีสาเหตุอื่น**
- **`CSkillAttr` resolve ไม่ได้จาก static** = ผลที่มีค่า ⇒ ระบุ census ที่ไล่ครบเพื่อให้ใบถัดไปหยิบต่อ
- **serializer ของ `CSkillModule` เป็น stub ไม่ปล่อย field / ป้าย field ต่างจาก FACTPACK** = ข่าวใหญ่ ⇒ FACTPACK row 300 + สมมติฐาน "vital เดี่ยว" ต้อง re-verify

### 🔴 เกณฑ์จบ + ขั้นต่อไปที่ตั้งใจไว้ (ยังไม่ใช่คำสั่งให้เขียนโค้ด) — **สามผลลัพธ์ ไม่ใช่สอง**
- **(บวก) ไคลเอนต์มี inbound decoder + skill-window-open ขึ้นกับ skill state** (พิสูจน์จากอิมเมจ · id ที่อ้างพิสูจน์ด้วยรูป body จาก Tier A ไม่ใช่ name-hash): ขั้นต่อไป **เปิด hypothesis เลนโค้ดฝั่ง server** ให้ emit skill state หลัง opt-in scenario (`production_allowed=false` · fail-closed · headless proof) แล้ว rerun attended **GT-058** — 🔴 **ยังไม่เปิดใบนั้น** จดเป็นคำถามเปิดรอ Panya
- **(ลบ) ไคลเอนต์ไม่มี decoder / window-open ไม่ขึ้นกับ state** (static census ไล่ครบ): การส่ง state ไม่ปลดหน้าต่าง ⇒ ห้ามเปิดเลน sender · ตัวขวาง GT-058 มีสาเหตุอื่น · จดคำถามเปิดรอ Panya
- **(UNANSWERABLE) static ตอบไม่ขาด + corpus เป็น emulator-only:** 🔴 **ห้ามสรุปทั้งบวกและลบ** · direction เป็นคำถามที่หลักฐานที่มีตอบไม่ได้ ⇒ ส่งการตัดสินใจให้ Panya (สร้าง sender แบบ opt-in เพื่อทดลองกับ client จริง เป็น "ทางเดียวที่เหลือ" หรือหา original-server capture) · **ห้าม auto-abandon สมมติฐานด้วยผล UNANSWERABLE**

### nonclaims (ติดไปกับผลทุกกรณี)
- **ผลลบที่ใช้ได้คือ static** ("ไคลเอนต์ไม่มี decoder / window-open ไม่ขึ้นกับ state") ไม่ใช่ผลจาก corpus — 🔴 "ไม่เจอเฟรมใน corpus" เป็น **UNANSWERABLE** เพราะ corpus เป็น emulator-only (SCENE-013) ห้ามใช้สรุปว่าตัวขวางมีสาเหตุอื่น
- **ตาราง/serializer ในไคลเอนต์ = สิ่งที่ client รู้ ไม่ใช่กฎของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล
- **root-cause ของ cloud (server-ไม่เคยส่ง-skill-state) เป็น HYPOTHESIS ไม่ใช่ข้อพิสูจน์** — ใบนี้คือใบที่ทดสอบ wire premise ของมัน ไม่ได้ยืนยันมัน
- **id 0x1F7B / 0x1661 เป็น name-hash candidate ไม่ใช่ opcode** — ห้ามอ้างเป็น wire id จนกว่าจะเจอในตาราง dispatch จริง
- **ห้ามตั้งชื่อ semantics ของ field ใด ๆ เกินกว่าที่ serializer/capture พิสูจน์** — ความยาวคือความยาว ไม่ใช่ชนิด
- static ไม่พิสูจน์ว่า runtime ส่ง/รับจริง · capture = สิ่งที่ client เคยได้รับ ไม่ใช่กฎ server ต้นฉบับ · ไม่พึ่ง `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส (UNKNOWN 100%)
- ใบนี้ไม่ตอบว่าหน้าต่าง Skill (K) จะเปิด/populate ได้จริงไหม (ชั้น attended · GT-058)

### result:
🔴 `ค้นใน pf_bridge\external\ แล้ว: ___` · 🔴 `ค้น gamedata แล้ว: ___` · (ผู้รับงานกรอก: objective 3 ส่วนประโยคเดียว · CSkillModule W layout + span/offset/len/sha ทุกฟังก์ชัน · CSkillAttr carrier + census · Tier B (static): inbound decoder VA + skill-window-open gate VA หรือ census-ไล่ครบ · corpus eligibility pre-check (มีเฟรม server ต้นฉบับไหม) + ถ้าใช่ hex เฟรม/ถ้าไม่ = UNANSWERABLE · พาธ root corpus เต็ม + sha · sha อิมเมจ+TSV ก่อน-หลัง · จดหมายเข้า notes_to_chief/)

---

## 🆕🔬 RE-062 SKILLATTR-BIND-NULL-BRANCH-001 [STATIC-ON-BRIDGE]: null branch ของ bind thunk `0x4698B0` / target-resolve ใน handler `0x5F2400` — เฟรม `0x1661` ขาเข้า **สร้าง** container ที่ `[actor+0x3E8]` ได้ไหม หรือได้แค่ **อัปเดต** ของที่มีอยู่  [✅ **DONE — คำตอบ (ค) เส้นทางอื่น: inbound ไม่เขียน slot เลย** (ผลหน้าสะพาน 2026-08-24 17:01 +07:00 · บันทึก R152)]

ที่มา (คำถามเปิดจาก pf-adversary R149 — ข้อเดียวที่ดีไซน์ HYP-PF-035 ยังตอบไม่ได้):
- RE-061 พิสูจน์แล้ว: inbound apply ของ `CSkillAttr` มีจริง (`UpdateAttrVital` handler `0x5F2400` iterate attr blocks → resolve live target → เรียก incoming attr `vtable+0x24 = 0x751C70` copy DB base + record tree) · bind thunk `0x4698B0` type-check `CMyActor` แล้ว **อ่าน `[actor+0x3E8]`** ก่อนส่ง target เข้า apply
- 🔴 **ช่องที่ยังไม่มีใคร trace: ตอน `[actor+0x3E8]` เป็น null** (ซึ่งคือสภาพที่สมมติฐาน GT-058 บอกว่าเป็นอยู่) — ถ้า bind thunk no-op / handler drop block เมื่อ slot null ⇒ **sweep ของ HYP-PF-035 พลิก gate `0x761ED0` ไม่ได้เชิงโครงสร้าง** ไม่ว่าเฟรมถูกแค่ไหน และผล GT-059 จะออก "รับแล้วแต่ K ไม่เปิด" ด้วยเหตุที่ไม่ใช่ทั้ง wire shape และ gate hypothesis
- ⇒ ใบนี้คือกุญแจอ่านผลลบของ GT-059: **ผลลบ + null-branch=no-op** = เลนส่งต้องเปลี่ยนวิธี (เช่น หา path ที่ client สร้าง container เอง ตอน entry/vital อื่น) · **ผลลบ + null-branch=สร้างได้** = gate มี check อื่นขวาง

objective หนึ่งประโยค: **ตัดสินจากอิมเมจ (recursive CFG · byte-exact) ว่าเส้นทางรับ `0x1661` ตอน `[actor+0x3E8]` = null ทำอะไร: (ก) allocate/construct `CSkillAttr` ใหม่แล้วเก็บลง slot · (ข) no-op/drop block · (ค) เส้นทางอื่น (ระบุ)** — พร้อม span + sha ของทุกฟังก์ชันที่อ้าง

ขอบเขต/กติกา (เหมือน RE-061): STATIC-ON-BRIDGE ล้วน · ไม่บูตอะไร · ไม่แตะ DB · read-only SHA before=after · ค้น `pf_bridge\external\` และ gamedata ก่อนถอด (ช่องบังคับ เจอ/ไม่เจอ) · ห้าม linear disassembly เป็นหลักฐานผลลบ · จุดเริ่ม: `0x5F2400` (handler) · `0x4698B0` (bind thunk) · `0x751C70` (apply) · ctor `CSkillAttr 0x751B90` (ใครเรียกบ้าง — มี call site จาก path รับไหม) · ระบุด้วยว่า target resolution ของ handler ผูกกับ identity ใน DBAttribute (`0x32` qword) อย่างไร
- **result:** ✅ DONE (2026-08-24 17:01 +07:00 · จดหมายเต็ม `notes_to_chief\20260824_1701_RE-062-RESULT-INBOUND-OTHER-PATH-NO-SLOT-WRITE.md` · วิธี: recursive CFG + byte-exact census · read-only: input manifest before/after IDENTICAL 7/7 ไฟล์ — SHA อิมเมจค่าเดี่ยว `9627...B623` ไม่ขยับ) — คำตอบ **(ค) เส้นทางอื่น**:
  1. decoder สร้าง `CSkillAttr` **ชั่วคราว** ได้จริงผ่าน registry/factory → clone → pool/ctor (ctor `0x751B90` มี call site 3 จุดเท่านั้น: `0x44B3A4` · `0x44B422` · `0x5F8BB8` — ไม่มีใน receive decoder ตรง ๆ)
  2. handler `0x5F2400` resolve target ด้วย **class id `0x1661` ใน generic attribute map** (lookup `0x463800` / insert `0x463720`) — ไม่ใช้ `[actor+0x3E8]` และไม่ใช้ identity tag `0x32` เป็น lookup key (qword `0x32` เป็น payload ที่ถูก copy ภายหลัง ไม่ใช่ key)
  3. **ไม่มีแขนงใดใน decode/handler/lookup/insert/bind/apply เขียน `[actor+0x3E8]`** — exhaustive overlapping decode รอบ displacement `0x3E8` พบ write 13 จุดทั้งอิมเมจ แต่ intersection กับ inbound spans = **0** (ผลลบไม่ได้อาศัย linear disassembly)
  4. slot สร้างที่ `CMyActor` ctor (`0x44CA71` zero · `0x44CBC1` เขียน pointer + register เข้า live manager) — เกิดก่อนรับเฟรม · bind `0x4698B0` อ่าน slot ที่ `0x4698DF` โดยไม่สร้าง · apply `0x751C70` ตรวจ null แล้ว return
  ⇒ **ผลต่อ GT-059:** sender ซ่อม slot null ไม่ได้เชิงโครงสร้าง แต่ normal construction สร้าง slot ไว้ก่อนแล้ว — ผลลบ GT-059 ต้องแยกเคส `slot null` / `slot non-null + gate อื่น` ด้วยหลักฐาน runtime · nonclaims เต็มอยู่ในจดหมาย (ไม่อ้างว่า slot เป็น null จริงใน runtime · ไม่อ้างว่า slot ไม่มีทางถูก clear หลัง construction)

## 🆕🔬 RE-064 ITEMOPERATE-RES-AFFECTED-ELEMENT-SHAPE-001 [STATIC-ON-BRIDGE]: pin ทรง wire ต่อ element ของ affected-identity ใน ItemOperateVitalRes (0x4C13) ตอน R10 (affected_identity_count) > 0 — เดินไบต์บนอิมเมจ read-only ของเครื่องสะพาน · ตัดสินว่า call ไม่จำแนก R13 (0x005ED2F0) อยู่ "ใน" loop ต่อ element หรือเป็น trailer ของ message · และ tag/width order ของหนึ่ง element  [✅ **DONE — PINNED · ผลหน้าสะพาน 2026-08-24 22:41 (+07:00) · จดหมาย `20260824_2241` · บันทึกโดย chief R156** — R13 = INSIDE loop / collection-insert helper (TRAILER prediction falsified) · element = `0x32`/8 + `0x08`/1 · rider prefix IDENTICAL 15/15]

ที่มา:
- RE-059 (DONE · EXTRACTED 5/5) พิสูจน์แล้ว: ทั้ง 5 เฟรมจริงใน capture corpus มี affected_identity_count (R10) = 0 ทุกเฟรม ⇒ **ไม่มีเฟรมจริงสักเฟรมที่ walk ทรง element ต่อ R10>0 ได้** · ทรง element วันนี้จึงเป็น candidate ล้วน ไม่เคยเดินกับ record จริง
- candidate ปัจจุบัน (จาก PF_SERIALIZER_FIELDS.tsv แถว file_off_claim 769-794 + ความกว้างจาก PF_TAG_CENSUS.tsv):
    R11 = tag 0x32 qword (u64, 8 ไบต์) `STACK@0x005EDA20+0x1C` file_off 0x001ECFBD VA 0x005EDBBD
    R12 = tag 0x08 u8 (1 ไบต์)       `STACK@0x005EDA20+0x1B` file_off 0x001ECFCD VA 0x005EDBCD
    R13 = CALL_UNCLASSIFIED:0x005ED2F0 file_off 0x001ED006 VA 0x005EDC06 (direct_call_not_proven_serializer)
  ⇒ candidate เรียง "u64 tag 0x32 (R11) แล้ว u8 tag 0x08 (R12) ต่อ element" · 🔴 R13 ยังไม่รู้ว่าอยู่ในหรือนอก loop
- serializer 0x4C13 ขา R = 0x005EDA20 span [0x005EDA20, 0x005EDC31) sha256 b5f6a1586a810c0a98ceb7c925a0d4afa10cff41db661eb0947b8918f3a11d54 (GT-054 verify 392/392) — 🔴 ห้าม re-derive span ซ้ำ

ทำไมสำคัญกว่าที่หน้าตามันดู:
- รอบ cloud R154 ของ chief สร้างเลน sweep ฝั่งเซิร์ฟเวอร์ GT-063 (ITEMOP-RES-GREENLINE-001 · HYP-PF-037) โดย **ตรึง affected_identity_count = 0 ในทุกเฟรม** เพราะทรงนี้ยังเปิดอยู่
- เฟรม count=1 ที่ร่างไว้ในตั๋วนั้น **ประกอบแบบ fail-closed ไม่ได้** จนกว่าใบนี้จะปิด — ปิดใบนี้ = ปลดล็อก sweep variant count>0 (HYP-PF-037 เวอร์ชันใหม่ ภายใต้ stop_rule เดิม ต้องมีรอบของตัวเอง · ใบนี้ไม่เปิดรอบนั้น)

หมวด: STATIC-ON-BRIDGE — อ่านอิมเมจ read-only + TSV บนดิสก์สะพานล้วน · 🔴 ไม่บูตเซิร์ฟเวอร์/client · ไม่มี LOCK_GAME · ไม่ต้อง capture · กติกา stamp/teardown/canonical/DB-copy ไม่เกี่ยวกับใบนี้

### 🔴 ช่องบังคับ (18:22): ค้นใน pf_bridge\external\ แล้ว
(ผู้รับงานกรอก: เจอ <อะไร> / ไม่เจอ) — chief ค้นให้แล้วตอนเปิดใบ ไม่ต้องค้นซ้ำ:
- PF_SERIALIZER_FIELDS.tsv แถว 769-794 = ทรงขา R/W ของ 0x4C13 เต็ม (R11/R12/R13 ตามข้างบน)
- PF_PROTOCOL_REGISTRY.tsv: ItemOperateVitalRes serializer_va=0x005EDA20 · ItemBagAttr (nested) serializer_va=0x0046EC10 · call site ใน 0x4C13 R-side (R6) = 0x0046F4D0
- PF_TAG_CENSUS.tsv = ความกว้างต่อ tag (0x32 -> 8 · 0x08 -> 1)
- PF_PROTOCOL_PRIORITY.tsv: serializer_status=OPEN · blocker "direct_call_not_proven_serializer" = ของแถว call รวมถึง R13 0x005ED2F0
- 🔴 สิ่งที่ชุดส่งมอบ **ไม่มี**: การจำแนกว่า 0x005ED2F0 (R13) เป็น serializer/nested/loop-internal และ loop bound ที่กิน R10 element

### 🔴 ช่องบังคับข้อสอง (R132): ค้น gamedata แล้ว
(ผู้รับงานกรอก) — คาดว่า gamedata\ ไม่ตอบใบนี้ (ตารางข้อมูลเกมไม่ใช่ control flow ของ serializer) แต่ต้องกรอกตามกฎ

### objective (claim เดียว)
**เดินไบต์บนอิมเมจ (recursive CFG · byte-exact) เพื่อ pin ทรง wire ต่อ element ของ affected-identity ใน 0x4C13 ขา R ตอน R10>0 ให้ครบ: (ก) loop ที่กิน R10 element เริ่ม-จบที่ instruction ไหน (bound) · (ข) call ไม่จำแนก R13 (0x005ED2F0) อยู่ INSIDE loop นั้นหรือเป็น trailer หลัง loop · (ค) tag/width order ของหนึ่ง element ตามที่ code เขียน/อ่านจริง**
🔴 คำตอบต้องเป็นประโยคเดียว รูปใดรูปหนึ่ง:
- `pin ได้ — element = <ลำดับ tag/width> · R13 0x005ED2F0 = INSIDE-loop|TRAILER · loop bound [<start VA>, <end VA>) กิน R10 รอบ · หลักฐาน span+sha`
- `pin ได้บางส่วน — <ส่วนที่ได้> · ส่วนที่ตัน <ที่ instruction ไหน เพราะอะไร>`
- `pin ไม่ได้จากชั้น static — control flow ตันที่ <VA> เพราะ <เหตุผลข้อเท็จจริง> · เข้าเกณฑ์จบ`

### db / server args
ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์/client — เปิดอ่านอิมเมจ + TSV อย่างเดียว · 🔴 ห้ามแก้อิมเมจ · ห้ามแก้ตารางส่งมอบ · ห้ามบูตอะไร · sha256 ของทุกไฟล์ที่พึ่ง ก่อน-หลัง ต้องตรงกัน (อิมเมจ GameClient.local.bin sha256 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623 ค่าเดี่ยว ต้องไม่ขยับ)

### คำทำนาย (🔴 นี่คือ **คำทำนาย** ไม่ใช่ข้อเท็จจริง — ทำนายผิด = ผลงาน)
จาก field order candidate (R11 ก่อน R12) และตำแหน่ง R13 ที่เขียนหลัง R12 ในลำดับ serializer:
- **ทำนายว่า** loop ต่อ element กิน R11 (0x32 u64) แล้ว R12 (0x08 u8) เป็นคู่ต่อ element และวน R10 รอบ
- **ทำนายว่า** R13 (0x005ED2F0) เป็น **TRAILER** หลัง loop จบ (call เดียวท้าย message) ไม่ใช่ loop-internal — เพราะ file_off ของมัน (0x001ED006) อยู่หลังทั้ง R11/R12 และไม่มี tag ฟิลด์คั่น
- 🔴 **ถ้ากลับกัน** (R13 อยู่ใน loop / element เป็นลำดับอื่น / loop กินมากกว่าคู่ R11-R12) = ข่าวใหญ่: เฟรม count=1 ที่เคยร่างไว้จะมีจำนวน call/element ผิด ⇒ ผู้รับงานแค่รายงาน 🔴 **ห้ามแก้ encoder/ledger/เฟรมร่างเอง**

### จ็อบ (control gate: 1 ต้องผ่านก่อนถึงจะเชื่อ verdict ของ 2/3)
1. **[control gate] reproduce loop ที่รู้แล้วก่อน** — เดิน per-element loop ที่ RE-059 ถอดสำเร็จ (update collection ใน nested ItemBagAttr เข้าถึงผ่าน call R6 0x0046F4D0 · element = 32 qword + 14 u32 + 0F + 0F + 08 + 08 + 0B) ด้วยวิธี recursive CFG เดียวกับที่จะใช้กับ R11-R13 · แสดงว่า method ระบุ loop bound + counter ของ loop ที่ "รู้คำตอบแล้ว" ได้ถูก · 🔴 method ที่ reproduce loop เดิมไม่ได้ = verdict ต่อ R11-R13 เชื่อไม่ได้ หยุดรายงาน
2. **จำแนก R13 0x005ED2F0** — เปิดอิมเมจอ่าน 0x005ED2F0 · ตอบว่าเป็น (i) serializer ฟิลด์ · (ii) nested serializer (เรียก sub-serializer) · (iii) loop-internal helper ของ element · (iv) trailer helper เดียวท้าย message · แนบ [start,end) + file offset + len + sha256 ของ 0x005ED2F0 · recursive CFG decode error = 0 · 🔴 ห้ามใช้ linear disassembler เป็นหลักฐานผลลบ (บทเรียนรอบ 83)
3. **pin loop bound + element order** — ในช่วง [0x005EDBBD (R11), 0x005EDC31) หา back-edge/counter ที่กิน R10 (STACK@...+0x54) · จด: instruction ที่เพิ่ม counter · การเปรียบเทียบกับ R10 · call R13 อยู่ในหรือนอก body · ลำดับ tag/width ที่ถูก emit/consume จริงต่อรอบ · 🔴 ถ้า control flow ไม่ลงตัว = หยุดที่ instruction นั้น จด VA/opcode/ที่คาด ห้าม "ปรับ" ให้ลงตัว

4. **[rider · 15 ไบต์เดียว] เทียบ PC prefix ของเฟรม capture #1 กับ prefix ของ envelope v141** — เปิด capture file (sha256 2e43b706... · PC index 101 · wrapper off 15 — extractor ของ RE-059 หาอยู่แล้ว) อ่าน 15 ไบต์แรกของ PC block แล้วเทียบกับ prefix ที่ `make_runtime_vitals` ของ v141 สร้าง (`129D6E140000000008040B02120100`) · ตอบ: `identical` / `differs ที่ offset <n>: capture=<hex> v141=<hex>` · เหตุ: เลน HYP-PF-037 replay byte-exact ได้แค่ชั้น message — ถ้า attended เจอ ErrorData ที่เฟรม control จะแยกไม่ออกว่า prefix หรือ session context จนกว่าจะเทียบ 15 ไบต์นี้ (falsification clause ของ ledger ชี้มาที่ rider นี้)

### pass criteria — 🔴 สองชั้น
**ชั้น wire/DB (ชั้นเดียวที่ใบนี้ผลิตหลักฐานได้):**
- คำตอบ objective ประโยคเดียว
- จ็อบ 1 (control gate) ผ่าน: loop ที่รู้แล้ว (ItemBagAttr update collection) ถูก reproduce bound/counter ตรง RE-059
- จำแนก R13 0x005ED2F0 หนึ่งใน (i)-(iv) + [start,end)+file_off+len+sha256 · CFG decode error = 0
- loop bound ต่อ R10: back-edge VA + counter VA + compare VA · verdict INSIDE|TRAILER ของ R13 · ลำดับ element (tag/width)
- ทุกข้อสรุป re-derive ได้ · ถ้าเขียนสคริปต์ commit ลง tools/ รันซ้ำได้ + exit 0 · 🔴 print ต้อง ASCII ล้วน (cp874)
**ชั้น client-observable: 🔴 ว่างเปล่าโดยเจตนา** — อ่านอิมเมจบนดิสก์ล้วน ไม่บูตอะไร ไม่มีจอ · 🔴 ห้ามอ้างผล static เป็นหลักฐานว่าจอเห็นอะไร หรือว่า green line/id 131 อ่านฟิลด์นี้

### 🔴 ผลลบมีค่าเท่าผลบวก
- `R13 = TRAILER` (ตรงคำทำนาย) = เฟรม count=1 ต้องมี 1 call ท้าย ปลดล็อก sweep variant count>0 · `R13 = INSIDE-loop` (ผิดคำทำนาย) = ข่าวดีที่สุด: เฟรมร่าง count=1 มีจำนวน call ผิด รู้ก่อนเอาเข้ารอบ sweep · `pin ไม่ได้ (control flow ตัน)` = คำถามทรง element ออกจากเลน static ⇒ ต้องพึ่งเส้นทางอื่น (ดูเกณฑ์จบ) กระทบทุกใบที่พึ่ง candidate นี้ รายงานเด่น ๆ

### 🔴 เกณฑ์จบ (บังคับ)
ถ้าจบที่ `pin ไม่ได้จากชั้น static` (control flow ตันแม้เปิดอิมเมจ) ⇒ คำถาม "ทรง element ตอน R10>0" ออกจากเลน static (candidate เดินกับ record จริงไม่ได้เพราะ corpus มีแต่ count=0) · **ไม่เปิดใบ static เพิ่ม** · เส้นทางสำรอง (🔴 ยังไม่เปิด จดเป็นคำถามเปิดรอ chief): capture ใหม่แบบ attended ที่ทำให้เซิร์ฟเวอร์เราส่ง 0x4C13 ที่ affected_identity_count>0 แล้วเดินไบต์เฟรมจริง — ทางนี้ก็ปิดใบนี้ได้ แต่เป็นชั้น attended คนละรอบ

### nonclaims
ไม่ตั้ง semantics ของค่า R11/R12/R13 (ห้ามตั้งชื่อ ยัง UNKNOWN — ความยาว/ลำดับ คือความยาว/ลำดับ ไม่ใช่ชนิด) · ไม่อ้างว่าเซิร์ฟเวอร์ต้นฉบับเคยส่ง count>0 (กู้ไม่ได้ตลอดกาล) · ไม่อ้างว่า green line/handler อ่านฟิลด์นี้ · ไม่พิสูจน์ทิศทาง runtime · candidate ทรงจาก serializer ไม่ใช่กฎเซิร์ฟเวอร์ต้นฉบับ · ไม่พิสูจน์ว่า encoder เราถูก/ผิด (แค่ "code อ่าน/เขียนทรงนี้")

### result:
🔴 `ค้นใน pf_bridge\external\ แล้ว: ___` · 🔴 `ค้น gamedata แล้ว: ___` · (ผู้รับงานกรอก: objective ประโยคเดียว · ผลจ็อบ 1 control gate (reproduce loop เดิมตรง/ไม่ตรง) · จำแนก R13 0x005ED2F0 + span/off/len/sha · loop bound VA + verdict INSIDE/TRAILER · ลำดับ element tag/width · sha อิมเมจ+TSV ก่อน-หลัง · จดหมายเข้า notes_to_chief/)

---

## 🆕🔬 RE-065 ACTORTASK-USEBEHAVIOR-CTOR-WALK-001 [STATIC-ON-BRIDGE]: เดิน ctor ของ `CActorTask_UseBehavior` / `CActorTask_PlayActionEvent` (custom RTTI ไม่ใช่ MSVC — vtable->name resolve จาก static ไม่ได้) — ครึ่งที่หายของ Door B: เฟรม behavior-id ขาเข้าจากเซิร์ฟเวอร์เรา **สร้าง attack task ให้ `CNetNPC` ที่ project ไว้** ได้ไหม  [✅ **DONE/YES (static) — ผลหน้าสะพาน 2026-08-25 02:50 (+07:00) · จดหมาย `20260825_0250_RE-065-RESULT-ACTIONVITAL-CONSTRUCTS-NPC-TASK.md` · บันทึกโดย chief R158** — `ActionVital` handler `0x007516C0` resolve actor จาก handle (`0x00402A20`/`0x00446170`) · lookup BEHAVIOR `0x00702A10` · เรียก ctor `CActorTask_UseBehavior` `0x0047AB30` · type gate ที่ผ่านคือ `CActorBaseClient` token `0x0102CE88` ซึ่ง `CNetNPC` (actor_type 4) เป็นลูกอยู่ใต้ (verifier 111 guards) · task ถูก commit เป็น vtable `0x00F0EF10` + flags `8` **ก่อน** gate `[actor+0x14]` ⇒ gate ตกก็ยังคืน task · control gate ผ่าน (`CActorTask_Dead` เดินซ้ำได้ตรง) · `CHitResult` = bounded direct negative · `CKnockdownVital` = UNRESOLVED static (virtual builder) — ห้ามตั้งชื่อ task ของเส้นนั้น
> 🔴 **ERRATUM ต่อ `FACTPACK_R100_DOORB_ATTACK_TASK_CTORS_STATIC.md` (ลงโดย chief R158 ตามที่ผู้รันขอ — ไม่แก้ไฟล์เก่า):** ข้อความเดิม *"ctor ของ `CActorTask_PlayActionEvent` NOT FOUND / ฟังก์ชัน ~`0x471E90` เป็น dtor"* **ผิด** · ctor มีจริง byte-exact ที่ `[0x00471EB0,0x00471F47)` (base ctor `0x00485D40` ที่ `0x00471EDD` · ติดตั้ง vtable `0x00F0EF28` ที่ `0x00471EEE` · `ret 0x14` ที่ `0x00471F44`) · `0x471E90..0x471EAC` เป็น tail ของเมท็อดอื่น
> 🔴 **nonclaim ที่ต้องติดไปกับผลนี้เสมอ:** YES ฝั่ง static แปลว่า *"มีเส้นทางสร้าง task อยู่ในอิมเมจ"* เท่านั้น · **ไม่**พิสูจน์ว่า lookup `0x00702A10` คืนแถว BEHAVIOR จริงตอน runtime (SCENE-013 null prior ยังเป็นความเสี่ยงแยก) และ **ไม่**พิสูจน์ว่ามอนสเตอร์โจมตีบนจอแล้ว ⇒ `INTENT_ATTACK_UNDELIVERABLE` ของ MOB-AGGRO-001 **ยังห้ามเลื่อนเป็น runtime-deliverable จากผลนี้ลำพัง** ต้องมีแถว BEHAVIOR ที่ resolve ได้ + การสังเกตแบบ attended ก่อน]

> 🔢 **หมายเหตุเลข (chief R157):** ตัวนับชุดเดียวกับ `GAME_TEST_QUEUE.md` — 063 ถูกใช้โดย GT-063 (R153) · 064 ถูกออก **สองครั้ง** (RE-064 ใน R154 และ GT-064 ใน R155 — ชนกันแล้วในไฟล์ ตามกฎห้ามเปลี่ยนชื่อใบที่ commit แล้ว ทั้งคู่คงชื่อเดิม) ⇒ เลขว่างถัดไปคือ **065** ใบนี้จึงเป็น RE-065

**ที่มา:** `pirate-force-server\drafts\MOB_AGGRO_SERVER_AI_STATIC_AND_DESIGN_R98_20260820.md` **หัวข้อ 7 ข้อ 1** (open static-RE question มูลค่าสูงสุดของเลน mob-aggro) + บริบทหัวข้อ 3 (task-id space) · draft ระบุเองว่า "walking those two ctors is the single highest-value next static step for Door B"

**ทำไมตอนนี้:** เลนเซิร์ฟเวอร์ MOB-AGGRO-001 (สไลซ์ตัดสินใจ pure-logic) เข้าแล้ว — มันตัดสินใจ "จะโจมตี" ได้ แต่ **ส่งมอบ intent นั้นให้ไคลเอนต์ render ไม่ได้** เพราะ Door B (attack/action) ยังไม่มีเส้นทาง server->client ที่พิสูจน์แล้ว · ใบนี้คือคำถามชี้ขาดฝั่ง static: เฟรม behavior-id ที่เรามีอยู่สองตระกูล ไปจบที่การสร้าง task `UseBehavior`/`PlayActionEvent` ให้ actor แบบ `CNetNPC` หรือไม่ — ไม่มี `CActorTask_Attack` ในอิมเมจ การโจมตีขี่สองตัวนี้ผ่านแถว BEHAVIOR เท่านั้น (draft หัวข้อ 3)

**หมวด:** `STATIC-ON-BRIDGE` — **NEEDS-BRIDGE-IMAGE**: อิมเมจ client ไม่มีบน cloud clone ⇒ ใบนี้ทำได้เฉพาะคนหน้าเครื่องสะพานที่มีอิมเมจ (เส้นทาง pf-static-re บน artifact ที่ commit แล้วใช้ไม่ได้ — ไบต์ที่ต้องใช้ไม่เคย commit) · อ่านอิมเมจ read-only ล้วน · 🔴 ไม่บูตเซิร์ฟเวอร์/client · ไม่มี `LOCK_GAME` · ไม่แตะ DB ใด · กติกา stamp 420 นาที / teardown / canonical DB ไม่เกี่ยวกับใบนี้

### 🔴 ช่องบังคับ (18:22): ค้นใน pf_bridge\external\ แล้ว
(ผู้รับงานกรอก: เจอ <อะไร> / ไม่เจอ) — ที่ chief รู้ตอนเปิดใบ: ตารางส่งมอบครอบ **vital serializer** ไม่ครอบครอบครัว `CActorTask_*` (task ไม่ใช่ wire object) · 🔴 `PF_RUNTIME_CLASSMAP.tsv` = UNKNOWN 100% ห้ามพึ่งเป็นชื่อคลาส — การผูก vtable->name ต้องมาจาก custom RTTI ในอิมเมจเอง ไม่ใช่จากตาราง

### 🔴 ช่องบังคับข้อสอง (R132): ค้น gamedata แล้ว
(ผู้รับงานกรอก) — คาดว่า gamedata\ ไม่ตอบใบนี้ (control flow ของ ctor ไม่ใช่ตารางข้อมูลเกม) แต่ต้องกรอกตามกฎ · ถ้าไปแตะแถว BEHAVIOR/`.beh` ให้จดว่าเจออะไร — แต่การ populate แถว BEHAVIOR จริงเป็นคำถามแยก (draft หัวข้อ 7 ข้อ 3 — **ไม่ใช่ของใบนี้**)

### objective (claim เดียว)
**เดินไบต์บนอิมเมจ (recursive CFG · byte-exact) เพื่อระบุ ctor VA + vtable + custom-RTTI linkage ของ `CActorTask_UseBehavior` และ `CActorTask_PlayActionEvent` แล้ว pin ว่าเส้นทางขาเข้า (inbound) เส้นไหน — ถ้ามี — เป็นผู้สร้าง task สองตัวนี้ให้ actor แบบ `CNetNPC` (ไม่ใช่แค่ local player)** และตอบคำถามเดียวของ Door B:
🔴 คำตอบต้องเป็นประโยคเดียว รูปใดรูปหนึ่ง:
- `YES — vital behavior-id จากเซิร์ฟเวอร์สร้าง attack task ให้ projected NPC ได้: เส้นทาง <carrier> -> <VAs> -> ctor <VA> · type gate ที่ผ่าน = <หลักฐาน>`
- `NO — ทุกเส้นทางขาเข้าที่ถึง ctor ติด gate เฉพาะ local player / ไม่มีเส้นทางถึง ctor เลย: ตันที่ <VA> เพราะ <ข้อเท็จจริง>`
- `UNRESOLVED — <ส่วนที่ได้> · ตันที่ <instruction ไหน เพราะอะไร> · เข้าเกณฑ์จบ`

### db / server args
ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์/client — เปิดอ่านอิมเมจอย่างเดียว · 🔴 ห้ามแก้อิมเมจ/ตารางส่งมอบ · sha256 ของทุกไฟล์ที่พึ่ง ก่อน-หลัง ต้องตรงกัน

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- **อิมเมจตัวเดียวกับทุกใบ static:** `GameClient\GameClient.local.bin` · sha256
  `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · ImageBase `0x400000` ·
  🔴 จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง
- **ข้อเท็จจริงตั้งต้น (พินแล้วใน draft R98 + SCENE/COMBAT reports — verify ก่อนพึ่ง):**
```
carrier 1: CHitResult (0x16F7)
  reaction factory 0x48D870 อ่าน behavior id จาก CHitResult+0x22 · selector +0x28
  -> BEHAVIOR lookup 0x702A10 (singleton 0x102DAD8) · missing row fallback 0x48AE40
carrier 2: CKnockdownVital (0x3123)
  consumer 0x750700 ใช้ raw +0x20 เป็น BEHAVIOR key -> 0x47CAD0
  -> wrapper vtable 0xF0F7DC (flags 0x40000005) -> task queue ที่ actor+0x40
task-id ctor cluster: 0x472000-0x476000 เขียน 0x800000XX ลง [task+0x10]
  (kind ที่พบมีสี่: 0x80000002 / 04 / 05 / 06 · CActorTask_Dead = vtable 0xF0F048 kind 05)
RTTI: custom ไม่ใช่ MSVC — ชื่อครอบครัว CActorTask_* มีเป็น name record แต่ vtable->name
  resolve จาก static ไม่ได้สำหรับส่วนใหญ่ (นี่แหละคือกำแพงที่ใบนี้ต้องเดินอ้อม)
ไม่มี CActorTask_Attack — attack ขี่ UseBehavior/PlayActionEvent ผ่านแถว BEHAVIOR (draft หัวข้อ 3)
```
- **ท่าทำงาน:** วินัย pf-static-re · recursive CFG · byte-exact · 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของผลลบ** (บทเรียนรอบ 83) · census ด้วย `E8`/`E9 rel32` ทุกออฟเซ็ต + dword refs + vtable slots

### คำทำนาย (🔴 นี่คือ **คำทำนาย** ไม่ใช่ข้อเท็จจริง — ทำนายผิด = ผลงาน)
- **ทำนายว่า** ctor ทั้งสองอยู่ในหรือใกล้ cluster `0x472000-0x476000` และเขียน kind หนึ่งในสี่ค่าที่รู้จักลง `[task+0x10]`
- **ทำนายว่า** เส้นทาง `CKnockdownVital` (0x750700 -> 0x47CAD0 -> queue ที่ `actor+0x40`) ไปจบที่ ctor หนึ่งในสองตัวนี้ — เพราะมันเข้าคิว task ให้ actor อยู่แล้ว
- **ผลรวมไม่แน่ (uncertain by design):** โอกาสออก NO/UNRESOLVED สูง — ทุก behavior lookup ที่เคยสังเกตใน runtime คืน null (SCENE-013 corpus negative) และ `ActionVital` inbound พิสูจน์แล้วว่า inert (SCENE-008) · ทำนายผิดทางไหนก็เป็น finding

### จ็อบ (ทำตามลำดับ · control gate ข้อ 1)
1. **[control gate] reproduce ของที่รู้แล้วก่อน** — ด้วย method เดียวกับที่จะใช้ทั้งใบ ให้เดินถึง `CActorTask_Dead` (kind `0x80000005` · vtable `0xF0F048` · token `_F_DIE_000` ที่ `0xF0F060`) จาก cluster ได้ถูก · 🔴 method ที่หาของที่รู้คำตอบแล้วไม่เจอ = verdict ที่เหลือเชื่อไม่ได้ หยุดรายงาน
2. **ผูกชื่อ -> vtable -> ctor** — เริ่มจาก custom-RTTI name record ของ `CActorTask_UseBehavior` และ `CActorTask_PlayActionEvent` (registrar/typeinfo ในอิมเมจ) เดินไปหา vtable และ ctor ของแต่ละตัว · จด: ctor VA · vtable VA · kind `0x800000XX` ที่เขียนลง `[task+0x10]` · span `[start,end)` + file offset + len + sha256 ของทุกฟังก์ชันที่อ้าง · ถ้าผูกไม่ได้ (กำแพง RTTI จริง) จดว่าตันที่ record/instruction ไหน
3. **ไล่ call site ของ ctor ขึ้นทางขาเข้า** — ใครเรียก ctor ทั้งสอง (census E8/E9 + indirect + vtable slot) · ตัดแยกให้ชัดว่า call site ไหนอยู่บนเส้นทาง inbound vital (สองตระกูล carrier ข้างบน + เส้นอื่นถ้าเจอ) และเส้นไหนเป็นเส้น local-input/script
4. **pin actor-type gate** — บนเส้นทางขาเข้าที่ถึง ctor: มี type check แบบ `CMyActor`-only ไหม (บทเรียน RE-062: bind thunk type-check ก่อนใช้ slot) หรือรับ actor ทั่วไป/`CNetNPC` ได้ · queue ปลายทางคือ `actor+0x40` ของ actor ตัวไหน (performer จากเฟรม หรือ local player เสมอ)
5. **ตอบ objective ประโยคเดียว** (YES/NO/UNRESOLVED ตามรูปข้างบน)

### pass criteria — 🔴 สองชั้น
**ชั้น wire/DB (ชั้นเดียวที่ใบนี้ผลิตหลักฐานได้ — static ทำ headless บนสะพานได้ ไม่ต้องมีคนหน้าจอเกม):**
- จ็อบ 1 (control gate) ผ่าน: เดินถึง `CActorTask_Dead` ด้วย method เดียวกันได้ถูก
- ctor VA + vtable VA + kind ของทั้งสองคลาส (หรือประกาศผูกไม่ได้พร้อมจุดตัน) · span `[start,end)` + file_off + len + sha256 ของ **ทุก** ฟังก์ชันที่อ้าง · recursive CFG decode error = 0
- verdict ต่อ carrier: `CHitResult` path และ `CKnockdownVital` path แต่ละเส้น ถึง/ไม่ถึง ctor · actor-type gate = <หลักฐาน VA>
- คำตอบ objective ประโยคเดียว (YES/NO/UNRESOLVED)
- sha อิมเมจก่อน-หลังตรงกัน · ทุกข้อสรุป re-derive ได้ · ถ้าเขียนสคริปต์ commit ลง `tools/` รันซ้ำได้ + exit 0 · 🔴 print ต้อง ASCII ล้วน (console cp874)
**ชั้น client-observable: 🔴 ว่างเปล่าโดยเจตนา** — อ่านอิมเมจบนดิสก์ล้วน ไม่บูตอะไร ไม่มีจอ · 🔴 ห้ามใครอ้างผล static ของใบนี้เป็นหลักฐานว่า NPC เล่นท่าโจมตีบนจอ — นั่นเป็นใบ attended คนละใบ (แนว HYP-PF-028) และต้องมีคนหน้าจอเสมอ

### 🔴 ผลลบมีค่าเท่าผลบวก
- **NO (มี gate local-player-only / ไม่มีเส้นทางถึง ctor)** = ข่าวใหญ่ที่สุดที่ใบนี้ให้ได้ ⇒ Door B ปิดเชิงโครงสร้างสำหรับ carrier ที่มี — `INTENT_ATTACK_UNDELIVERABLE` คงชื่อถาวรจนกว่าจะเจอ carrier/เส้นทางอื่น · redirect: เลน MOB-AGGRO หยุดลงทุนกับ attack frame แล้วไปเข้มที่ Door A/C ที่พิสูจน์แล้ว · ผลลบแบบนี้สอดคล้อง prior ทั้งหมด (SCENE-013: ทุก behavior lookup คืน null)
- **UNRESOLVED (กำแพง RTTI/control flow)** = ผลที่ใช้ได้ ⇒ จดจุดตันให้ใบถัดไปหยิบต่อ และคำถามอาจต้องออกจากเลน static (ดูเกณฑ์จบ)
- **YES** ก็ยังไม่ใช่ชัยชนะบนจอ — ดู nonclaims

### 🔴 เกณฑ์จบ (บังคับ)
ถ้าจบที่ UNRESOLVED เพราะ control flow/RTTI ตันแม้เปิดอิมเมจ ⇒ **ไม่เปิดใบ static เพิ่มในคำถามเดิม** · เส้นทางสำรอง (🔴 ยังไม่เปิด จดเป็นคำถามเปิดรอ chief): probe แบบ attended ตามร่าง HYP-PF-028 ใน draft (ยิง `CKnockdownVital` key ชี้แถว `.beh` ที่เชื่อว่ามีของ เช่น `7101.beh` แล้วดูจอ) — นั่นเป็นชั้น attended คนละรอบ คนละใบ

### nonclaims (ติดไปกับผลทุกกรณี)
- **YES ฝั่ง static ≠ NPC โจมตีบนจอ** — static พิสูจน์แค่ "มีเส้นทางในอิมเมจ" · runtime lookup `0x702A10` อาจคืน null เหมือนทุกครั้งที่ผ่านมา (SCENE-013) · การ populate แถว BEHAVIOR จริงเป็นคำถามแยก (draft หัวข้อ 7 ข้อ 3)
- ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับ (ปิดแล้ว กู้ไม่ได้ตลอดกาล) เคยส่งเฟรม behavior-id แบบใด — ทุกเฟรมที่จะตามมาเป็นดีไซน์เราล้วน
- ไม่ตั้ง semantics ให้ฟิลด์ใดเกินที่ carrier พิสูจน์แล้ว (`+0x22`/`+0x28`/`+0x20` คือออฟเซ็ตที่ code อ่าน ไม่ใช่ชื่อความหมาย)
- ใบนี้ **ไม่ compose เฟรม ไม่แก้ encoder ไม่เปิด HYP-PF-028 เอง** — รายงานอย่างเดียว การเปิดรอบต่อเป็นของ chief + คำเคาะ Panya
- ไม่แตะคำถาม `CAIStateCombatProxy` (draft หัวข้อ 7 ข้อ 2) — คนละใบ ห้ามลากมารวม

### result:
🔴 `ค้นใน pf_bridge\external\ แล้ว: ___` · 🔴 `ค้น gamedata แล้ว: ___` · (ผู้รับงานกรอก: objective ประโยคเดียว YES/NO/UNRESOLVED · ผลจ็อบ 1 control gate · ctor/vtable/kind ของทั้งสองคลาส + span/off/len/sha ทุกฟังก์ชัน · verdict ต่อ carrier + actor-type gate VA · sha อิมเมจก่อน-หลัง · จดหมายเข้า `notes_to_chief/`)

---

## 🆕🔬 RE-066 GROUNDLOOT-DWORD-IS-IT-READ-001 [STATIC-ON-BRIDGE]: เส้นทางอ่าน list `0x5F85B0` (read path `0x89A640`) **อ่านฟิลด์ `+0x14` แล้วเอาไปทำอะไรหรือเปล่า** — โดยเฉพาะว่ามันไปถึง item decoder ที่ RE-060 พินไว้ (`0x00892530` → `0x00890FC0` → `0x00890EF0`) ไหม  [✅ **DONE / PASS — YES · T2 หักล้างแล้ว · T1 ทดสอบได้** — ผลกลับ 2026-08-25 09:38:47 (+07:00) · RE runner LOCAL · จดหมาย `notes_to_chief\consumed\20260825_0938_RE-066-RESULT-ITEM-ID-REACHES-DROPMODEL.md` · บันทึกโดย chief R161 (2026-08-25 ~09:5x +07:00) — ดูบล็อก **result** ท้ายใบ]

**ที่มาของใบ (สำคัญ — อย่าอ่านข้ามช่วงนี้):** `pf-adversary` หักล้างเลนโค้ด GT-045 v3 ของรอบนี้ด้วยข้อค้านหนึ่งที่ยังไม่มีใครตอบได้:
รอบ attended 1104 ส่ง `2600001` ซึ่ง **ไม่มี drop model** แล้ว **ยังได้ฝุ่น "ของตกพื้น"** ⇒ ทฤษฎีสองอันอธิบายผลนั้นได้ดีเท่ากัน

| ทฤษฎี | ทำนายอะไรถ้าเปลี่ยนเลขไอเทม |
|---|---|
| **T1** ไคลเอนต์เอา `+0x14` ไปเปิดตารางไอเทมแล้ววาดโมเดลตามแถวนั้น | เปลี่ยนเป็นไอเทมที่มี drop model ⇒ **เห็นโมเดล** |
| **T2** handler เล่นเอฟเฟกต์ตามตำแหน่งตอนเรคคอร์ดมาถึง **โดยไม่เคยแตะ dword เลย** | เปลี่ยนเลขอะไรก็ได้ผลเหมือนเดิม ⇒ **ฝุ่นอย่างเดียวตลอดไป** |

🔴 **ทำไมต้องตอบก่อน:** ถ้า T2 จริง รอบ attended ถัดไปจะได้ "ฝุ่นอย่างเดียว" แล้วเกณฑ์ปิดใบจะ**ฆ่าสมมติฐาน "เลขไอเทมคือสาเหตุ"
ทั้งที่สมมติฐานนั้นไม่เคยถูกทดสอบเลย** เพราะ dword ไม่เคยถูกอ่าน · **ใบนี้ตอบได้จาก static ล้วน ไม่ต้องเปิดเกม ไม่ต้องใช้รอบ attended**

### objective (ประโยคเดียว)
**ในอิมเมจไคลเอนต์ ค่าที่ถูกอ่านจากออฟเซ็ต `+0x14` ของ element ใน list `0x5F85B0` ถูกใช้ต่อในเส้นทางใด — และเส้นทางนั้นไปถึง
item-table decoder ที่ RE-060 พินไว้หรือไม่ (`0x00892530` → `0x00890FC0` → `0x00890EF0`)**

### จ็อบ (ทำตามลำดับ · หยุดได้ทันทีที่ตอบ objective ได้พร้อมหลักฐาน)
0. **ด่านตัวควบคุมก่อนเสมอ:** verify sha ของอิมเมจ + verify span ของ `[0x005F85B0,0x005F8869)` (sha `ce0a58f7…` ที่ GT-042 พินไว้)
   และของ read path `0x89A640` · ถ้า sha ไม่ตรงกับที่พินไว้ **หยุดและรายงาน ห้ามเดินต่อ**
1. เดิน read path `0x89A640` แบบ recursive CFG · หา store ของฟิลด์ `+0x14` ลงโครงสร้าง element แล้ว **ตามตัวที่อ่านมันกลับออกมา**
   (dword ref / call census) — ผลลัพธ์ที่ต้องการคือรายชื่อ **ผู้อ่าน `+0x14` ทุกตัว** พร้อม VA
2. สำหรับผู้อ่านแต่ละตัว: ไปถึง `0x00892530` (หรือ `0x0046B3E0` / `0x00892580` ตามที่ RE-060 พิน) ได้ไหม — ตอบด้วย call chain ที่เดินได้จริง
3. ถ้าไม่มีผู้อ่านเลย ⇒ **นั่นคือคำตอบ (T2) และเป็นผลลบที่มีค่าสูงมาก** — แต่ต้องเป็น **bounded negative** ที่ระบุขอบเขตชัด
   (ค้นอะไรบ้าง · exclude indirect/virtual path ได้หรือไม่ได้) **ห้ามเขียน "ไม่มี" ลอย ๆ** (ด่าน G1)
4. ถ้ามีผู้อ่านและไปถึง decoder ⇒ ระบุด้วยว่า **ฟิลด์ไหนของแถวถูกอ่าน** (`n_ID_MODEL` / `n_DROPMODEL_TYPE` / อื่น ๆ)
   — ถ้าตอบข้อนี้ได้ **คำถามเรื่องฟิลด์ที่ GT-045 v3 ตอบไม่ได้โดยดีไซน์ จะถูกตอบด้วย static แทน**

### เกณฑ์จบใบ
ตอบ objective ได้พร้อม **VA + span + sha ต่อฟังก์ชันที่พึ่ง + recursive CFG errors 0** · หรือชน **bounded negative** ที่ระบุขอบเขตครบ

### nonclaims ที่ต้องติดไปกับผล
- ผล static ไม่บอกว่า runtime จะเดินเส้นนั้นจริง (SCENE-013 null prior ยังเป็นความเสี่ยงแยก)
- ผลใบนี้ **ไม่แทนที่รอบ attended GT-045** — มันแค่ทำให้อ่านผลรอบนั้นถูก
- ห้ามผูกเลข/ชื่อจาก `gamedata` เข้ากับเส้น code เพื่อพิสูจน์ control flow (กติกาเดิม)
- เซิร์ฟเวอร์ต้นฉบับปิดไปแล้วและกู้ไม่ได้ — ใบนี้พูดถึงพฤติกรรมของไคลเอนต์ที่ ship มาเท่านั้น

> 🔢 **หมายเหตุเลข (chief R158):** ตัวนับชุดเดียวกับ `GAME_TEST_QUEUE.md` — 065 ถูกใช้โดย RE-065 (R157) ⇒ เลขว่างถัดไปคือ **066**

### ✅ result (บันทึกโดย chief R161 · 2026-08-25 ~09:5x +07:00 · จากจดหมาย `20260825_0938`)

**คำตอบ objective: YES — `+0x14` ถูกอ่านกลับเป็น full item ID จริง และเดินถึง item-row decoder**
🔴 **สองเส้นทาง อย่ายุบรวมกัน:** เส้นที่ไปถึง `0x00892580` ที่ **RE-060 พินไว้** คือ **path A ซึ่ง query `s_NAME`** ·
ส่วน **`n_DROPMODEL_TYPE` เป็นของ path B** ซึ่งเดิน `0x00892DD0 → 0x00892610 → 0x00890FC0 → 0x00890E70`
และ **ไม่ได้แตะ `0x00892580` หรือ `0x00890EF0` เลย** ⇒ ประโยคแบบ *"ไปถึง decoder ที่ RE-060 พิน แล้วอ่าน `n_DROPMODEL_TYPE`"* **ผิด**
⇒ **T2 หักล้างเชิงโครงสร้างแล้ว** (สำหรับอิมเมจไคลเอนต์ที่ ship มา) · **T1 กลายเป็นสมมติฐานที่ทดสอบได้จริง**

**ผู้อ่าน `+0x14` — สามกลุ่ม (concrete inbound graph):**

| เส้นทาง | จุดอ่าน | decoder chain | ฟิลด์ที่ query |
|---|---|---|---|
| compare/update decision `0x006AF970` | `0x006AFCF8` · `cmp` ที่ `0x006AFD0D` | — (ตัดสินไป update branch) | — |
| **create path A** `0x005F41E0` | `0x005F46FA` | `0x00892580 → 0x00890FC0 → 0x00890EF0 → 0x00890E70` | **`s_NAME`** (`0x00F0C294`) |
| **create path B** `0x005F41E0` | `0x005F426D` | `0x00892DD0 → 0x00892610 → 0x00890FC0 → 0x00890E70` | **`n_DROPMODEL_TYPE`** (`0x00F30F88`) |
| update `0x005F4C00` | `0x005F4CAC` | `0x00892DD0` | `s_TAG_EXTRA` · `n_QUALITY` |

🔴 **ผลข้างเคียงที่ตอบจ็อบ 4 และปิดคำถามที่ GT-045 v3 ตอบไม่ได้โดยดีไซน์:**
**ฟิลด์ที่ graph นี้เปิดอ่านคือ `n_DROPMODEL_TYPE` — ไม่มี named lookup ของ `n_ID_MODEL` เลยในสาม concrete span**
(`n_ID_MODEL` มี UTF-16 occurrence เดียวที่ `0x00F1D3C8` · raw dword refs ทั้งอิมเมจ 21 จุด · **แต่ใน `CREATE`/`UPDATE`/`CONSUMER` = 0**)
⇒ ยืนยันคำแก้ของ chief R158 (§⑥ ข้อ ①) โดยอิสระ **ในขอบเขตที่ใบนี้วัดได้เท่านั้น** คือ:
**ใน concrete inbound graph นี้ ไคลเอนต์เปิดอ่าน `n_DROPMODEL_TYPE` และไม่เปิดอ่าน `n_ID_MODEL`**
🔴 **ห้ามย่อเป็น "`n_DROPMODEL_TYPE` คือฟิลด์ที่ถือความหมาย"** — นั่นเป็นคำกล่าวเชิง**สาเหตุ**ว่าอะไรตัดสินการวาด
ซึ่ง **ใบนี้ไม่ได้วัด** และ `GAME_TEST_QUEUE.md` ห้ามไว้ตรง ๆ · "เปิดอ่านฟิลด์ไหน" ≠ "อะไรตัดสินการวาด"
⇒ สิ่งที่สรุปได้จริง: **เกณฑ์เลือกไอเทมของ GT-045 v3 เล็งฟิลด์ที่มีหลักฐานว่าไคลเอนต์อ่านจริง**
(ทั้ง `2200423` และ `2200003` มี `n_DROPMODEL_TYPE=1`) — **ไม่ใช่** ว่าฟิลด์นั้นเป็นตัวขับโมเดล

**ด่านตัวควบคุมผ่านครบ:** image sha `9627211412ac…7028b623` (14,759,424 B) ก่อน=หลัง · list codec span sha `ce0a58f7…8a4f1b5b` ตรง pin ของ GT-042 ·
recursive CFG **17 span · gap 0 · decode errors 0 ทุกแถว** · verifier `pf_bridge\staged\re066_static_verify.py` sha `676c5837…af511308` exit 0 สองรอบ · ASCII output ·
sha ของ external/gamedata/จดหมายที่พึ่งทุกไฟล์ ก่อน=หลัง ตรงหมด · **ไม่แตะคิว/ซอร์ส/DB ใด**

**census ที่ทำให้ผลลบย่อยเชื่อถือได้:** `0x005F41E0` มี rel32 caller จุดเดียว (`0x006B01A0`) raw dword refs 0 ·
`0x005F4C00` caller จุดเดียว (`0x006AFDE9`) refs 0 · `0x005F85B0` callers `0x005E3F63`/`0x005E4042` refs 0 ·
element vtable `0x00F313C4` refs สามจุดอยู่ใน dtor/allocator ล้วน

**nonclaims ที่ต้องพกไปกับผลนี้ (ยกมาจากจดหมาย ห้ามตัด):**
- static ไม่บอกว่า **runtime** จะเดินเส้นนี้จริง — `SCENE-013` null prior ยังเป็นความเสี่ยงแยก
- **ไม่แทนที่รอบ attended GT-045** — ทำให้ *อ่านผล* รอบนั้นถูกเท่านั้น
- ไม่อ้างว่า `n_ID_MODEL` ไม่ถูกอ่านที่อื่นในโปรแกรม — รายงานเฉพาะ named lookup ใน concrete graph นี้
- ไม่ตัด indirect alias ที่ไม่มี literal/rel32 ทั่วทั้งโปรแกรมด้วยชื่อชนิดอย่างเดียว
- ไม่ใช้ join ของ `gamedata` พิสูจน์ control flow · ไม่พูดถึง original server (ปิดและกู้ไม่ได้)

**สถานะคิวหลังใบนี้:** 🟢 **ใบ static เปิดอยู่ = 0 ใบ**
