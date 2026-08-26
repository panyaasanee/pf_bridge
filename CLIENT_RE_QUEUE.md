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
🔴 **อัปเดต R163 (2026-08-25 ~15:xx +07:00): ไม่ใช่ 0 อีกแล้ว — เปิด `RE-067` ท้ายไฟล์**
🔴 **อัปเดต R165 (2026-08-25 ~17:0x +07:00): `RE-067` ปิดแล้ว (PASS/MIXED) · เปิด `RE-068` ท้ายไฟล์ ⇒ ใบ static เปิดอยู่ = 1 ใบ**
🔴 **อัปเดต R167 (2026-08-25 ~19:0x +07:00): `RE-068` ปิดแล้ว (PASS-MIXED · ครึ่ง actor ชนเพดาน static) · `RE-070` (orchestrator) เปิดอยู่ตั้งแต่ R166 ⇒ **ใบ static เปิดอยู่ = 1 ใบ** และเป็นใบเดียวที่รอคนหน้าสะพาน**
🔴 **อัปเดต R168 (2026-08-25 ~20:2x +07:00): `RE-070` ปิดแล้ว (DONE/PASS-MIXED · ผลอยู่ท้ายใบ) · เปิด `RE-071` (BasicAttr ของ actor ที่เพิ่ง spawn) ท้ายไฟล์ ⇒ **ใบ static เปิดอยู่ = 1 ใบ** · ใบพี่น้อง attended ของรอบเดียวกันคือ `GT-072` ⇒ **เลขว่างถัดไปคือ 073***
🔴 **อัปเดต R170 (2026-08-25 ~22:2x +07:00): `RE-071` ปิดแล้ว (DONE / STATIC-CONTRADICTION-PINNED · ผลอยู่ท้ายใบ) · เปิด `RE-075` RETURNSELECT-APPLY-0x5F1190 ท้ายไฟล์ (คำเคาะเจ้าของข้อ 2 · ทาง (ข))** ⇒ **ใบ static เปิดอยู่ = 2 ใบ** (`RE-073` · `RE-075`) · 🔴 **เลขว่างถัดไป = 076** (074 ถูกจองโดย `GT-074` ในรอบเดียวกัน)
🔴 **อัปเดต R169 (2026-08-25 ~21:0x +07:00): เปิด `RE-073` TEST-STAGE-GEOMETRY-SURVEY-001 ท้ายไฟล์** (คำขอ "แมพเทส" ของเจ้าของ · ครึ่ง crosswalk ทำจบบนคลาวด์แล้ว เหลือเรขาคณิตที่ต้องใช้ดิสก์ไคลเอนต์) · **แก้ขอบเขต `RE-071`** (ตัดครึ่ง "ชื่อว่าง" ออก — **แผงของผู้เล่นเองก็ไม่มีชื่อ** ในภาพควบคุมของ `GT-030-R3` ⇒ วิดเจ็ตนี้ไม่มีแถวชื่อเลย) ⇒ **ใบ static เปิดอยู่ = 2 ใบ** (`RE-071` · `RE-073`) ⇒ **เลขว่างถัดไปคือ 074**

---

## 🆕🔬 RE-067 NAME-COLOR-SOURCE-001 [STATIC-ON-BRIDGE]: อะไรตัดสิน **สี** ของ ① ป้ายชื่อไอเทมบนพื้น และ ② ป้ายชื่อ actor — และสีนั้นอ่านจาก field offset ไหน อยู่ใน mask `0x12` ที่เราส่งหรืออยู่นอก  [✅ **DONE / PASS-MIXED — ปิดโดย chief R165 · 2026-08-25 ~17:0x (+07:00)** · ครึ่งไอเทม = PASS (pin selector ได้) · ครึ่ง actor = **BOUNDED NEGATIVE** · ผลหน้าสะพาน 2026-08-25 16:26 (+07:00) · จดหมาย `notes_to_chief\consumed\20260825_1626_RE-067-RESULT-NAME-COLOR-SELECTOR.md` · บล็อก **result** ท้ายไฟล์]

> **ที่มา: ไม่ได้มาจากคิว** — คุณ Panya เอา capture ของ **เซิร์ฟเวอร์ต้นฉบับ** มาเทียบกับจอของเราเอง
> **นี่เป็นครั้งแรกที่โปรเจกต์ใช้ภาพเซิร์ฟเวอร์เดิมเป็นเกณฑ์เทียบผลของเรา**
> ร่างใบจากหน้าสะพาน: `notes_to_chief\consumed\20260825_1420_RE-067-TICKET-DRAFT-what-decides-name-color.md`
> เกณฑ์ที่ใบนี้เกิดมาค้ำ: **P6** ใน `SERVER_VERSION_MAP_AND_PROMOTION_20260825.md` · ทะเบียน: `REAL_SERVER_DIVERGENCE.tsv`

### ตารางความต่างที่จุดใบนี้ (อ่านด้วยตาจากภาพ — ยังไม่ใช่การวัดค่าพิกเซล)

| อะไร | เซิร์ฟเวอร์เดิม | ของเรา |
|---|---|---|
| ตัวละครตัวเอง (เหนือหัว + UI ซ้ายบน) | ขาว | 🔴 **UI ซ้ายบนไม่มีชื่อเลย** |
| ผู้เล่นคนอื่น | เขียว *(ยังไม่ชัดว่าขึ้นกับกิลด์ไหม)* | — |
| **ชื่อ NPC** | **เหลือง** *(ผู้สังเกตยืนยันว่าแน่นอน)* | 🔴 **`Tornado Eagle` (`0x201F`) = เขียว** |
| คำอธิบายเหนือชื่อ NPC | ฟ้า | — |
| Title ของผู้เล่น | ฟ้า (คล้ายกัน) | — |
| **ชื่อไอเทมบนพื้น** | **ขาว** | 🔴 **`Red leaves Hammer` (2200423) = แดง/ส้ม** |

🔴🔴 **ข้อที่ร่างเดิมเขียนไว้ และ chief R163 ต้องถอนก่อนเปิดใบ — อ่านข้อนี้ก่อนเริ่มงาน**

ร่างจากหน้าสะพานเขียนว่า:
> ~~"เซิร์ฟเวอร์เดิม NPC=เหลือง ผู้เล่น=เขียว · ของเรา NPC ขึ้นเขียว
> ⇒ **ไคลเอนต์กำลังจัด `0x201F` เข้าช่องเดียวกับ 'ผู้เล่น' ไม่ใช่ 'NPC'**"~~

**[วัดแล้วบนคลาวด์ R163 · `pf-static-re` · re-derive เอง ไม่ได้ยกจากใบใด]** — **ชั้น wire ไม่หนุนข้อสรุปนี้:**
```
grep -n "make_remote_actor_entry(" current/pf_login_game_server_v141.py   -> 20 บรรทัด = 1 def + 19 call site
ตรวจ argument ตัวแรกทุกจุด (รวม 9 จุดที่ขึ้นบรรทัดใหม่: 1635,1696,1711,1754,1794,1927,1958,1988,6139)
=> ทั้ง 19 จุดส่ง literal 4
ฝั่ง src/ อีก 9 call site: population.py:224,287 · npc_hp_link_hypothesis.py:1086 · npc_hostile_hypothesis.py:519
  · hostile_hp_link_hypothesis.py:1250 · runtimeres_death_hypothesis.py:730  => NPC_STYLE_ACTOR_TYPE = 4
  · scenario.py:122 · scene_object.py:34 => literal 4
  จุดเดียวที่ส่งค่าอื่นได้ = remote_player_hypothesis.py:876 (REMOTE_PLAYER_ACTOR_TYPE = 2 · หลัง scenario opt-in)
```
⇒ **เซิร์ฟเวอร์ของเราส่ง `actor_type = 4` (`CNetNPC`) ให้ `0x201F` เสมอ ในทุกเส้นทางที่บูตปกติเดิน**
⇒ ไคลเอนต์จึงควรสร้าง **`NameBoardNPC`** ไม่ใช่ `NameBoardPlayer` — **สองคลาสนี้ต่างกันจริง**
(`reports/PF_MPAUDIT_FOLLOWUP001_ACTOR_TYPE_DISPATCH_STATIC_20260818.md:177` — *"The two actor families get two different boards"*)

🔴 **แต่นี่ไม่ได้พิสูจน์ว่าร่างผิด — มันเปลี่ยนคำถามของใบ:**
**wire byte ที่ถูก ≠ ไคลเอนต์เลือกสีตาม byte นั้น** · ไคลเอนต์อาจเลือกสีจาก faction / relation / attr ที่เราไม่เคยส่ง
⇒ คำถามใหม่ที่คมกว่าเดิมคือ: **`NameBoardNPC` เลือกสีจากอะไร และทำไมมันถึงออกมาเป็นสีเดียวกับที่ตาเห็นว่า "เขียวแบบผู้เล่น"**
⇒ **ยังกระทบ `GT-035` เท่าเดิม** แต่ด้วยเหตุผลคนละข้อ

🔴 **`0x201F` ไม่ใช่คีย์ของตารางใดเลย** — ค้น field-exact ค่า `8223` ทั้ง 188 tsv เจอ 6 แถว **ไม่มีแถวไหนเกี่ยวกับ actor**
(`BUFF.n_ID` · `CD_TIMER.n_ID` · `Missile.n_ID` · `SKILL_CONTEXT.n_ID`+`n_CD` · `SKILL_TEXT.n_ID`)
มันคือ **runtime identity** `0x2000 + placement_index + 1` (placement 30) — `src/pirateforce_foundation/population.py:44-46`
**ตัวที่เป็น "ชนิด" จริงคือ template 31** ใน `CONSTDATA_TH__MOBS.tsv`: `s_NAME=旋風巨鷹` · `n_RANK=1` · `n_MOB_USAGE=1` · `s_OUTFIT=M011_000_000_SP3`
· ชื่ออังกฤษ `TEXTDATA_TH__MOBS_TIP.tsv:32` = `Tornado Eagle` ✅

### objective (ประโยคเดียว)
**ในอิมเมจไคลเอนต์ ค่าสีของข้อความป้ายชื่อ (ไอเทมบนพื้น · actor) ถูกเลือกที่ VA ไหน และค่าที่มันอ่านเพื่อเลือก
มาจาก field offset ไหนของโครงสร้างใด — แล้ว offset นั้นอยู่ใน mask `0x12` ที่เราส่งหรืออยู่นอก**

### [วัดแล้ว] จุดตั้งต้นที่ **มีอยู่แล้ว** — ใบนี้ไม่ต้องเริ่มจากศูนย์
จาก **`RE-066` (ปิด DONE/PASS)** — สาม concrete span ที่ pin ไว้แล้ว มี **สองเส้นที่แตะข้อความ/คุณสมบัติไอเทม**:

| เส้นทาง | จุดอ่าน `+0x14` | decoder chain | ฟิลด์ที่ query |
|---|---|---|---|
| **create path A** `0x005F41E0` | `0x005F46FA` | `0x00892580 → 0x00890FC0 → 0x00890EF0 → 0x00890E70` | **`s_NAME`** (`0x00F0C294`) |
| create path B `0x005F41E0` | `0x005F426D` | `0x00892DD0 → 0x00892610 → 0x00890FC0 → 0x00890E70` | `n_DROPMODEL_TYPE` (`0x00F30F88`) |
| **update** `0x005F4C00` | `0x005F4CAC` | `0x00892DD0` | **`s_TAG_EXTRA` · `n_QUALITY`** |

⇒ **ทางเดินฝั่งไอเทม (แก้ทิศทางโดย chief R163 หลัง `pf-adversary` จับได้):**
🔴 **ห้าม "ไล่ลงไปข้างหน้า" จาก `0x00892580`** — ฉบับแรกเขียนอย่างนั้นและ **มันผิดทิศ**
`0x00892580` คือ **table decoder** ⇒ เดินไปข้างหน้าจะเจอแค่ลูกโซ่ `0x00890FC0 → 0x00890EF0 → 0x00890E70`
ซึ่ง **RE-066 พินไว้แล้วและเป็นตัวอ่าน constdata ไม่ใช่โค้ดวาด** ⇒ เดินไปก็ตันแน่นอน
⇒ **ทางที่ถูก: กลับขึ้นไปที่ caller** (`0x005F46FA` ภายใน `0x005F41E0`) แล้วดูว่า **มันเอาสตริงที่ได้ไปทำอะไรต่อ**
(ตรงกับที่ร่างหน้าสะพานเขียนไว้แต่แรกว่า "ไล่ขึ้นไปหา" — chief เป็นคนเขียนกลับทิศเอง)

### ✅ [ปิดแล้วบนคลาวด์ R163] ครึ่งข้อมูลของใบนี้ — **หน้าสะพานไม่ต้องทำซ้ำ**
`pf-static-re` รันบน clone รอบนี้ (`pf_bridge` HEAD `2702e99c`) · re-derive เองทุกตัวเลข ไม่ได้ยกจากใบร่าง
**ตัวคุม:** การกระจาย `n_QUALITY` ที่นับได้ **ตรงกับใบร่างทุกตัว** และ `423 → "Red leaves Hammer"` ตรงกับที่ผู้สังเกตเห็นบนจอ
⇒ pipeline การอ่านตารางไม่เพี้ยน

**① ตารางไอเทม** `CONSTDATA_TH__EQUIPMENT_BASE.tsv` (974 แถวข้อมูล · 39 คอลัมน์ — ยืนยันแล้ว):
```
n_ID 423 (2200423 · NEAR)  s_NAME=紅葉之鎚  n_QUALITY=0  s_TAG_EXTRA=(ว่าง)  n_TAG_LOOT=4168  n_ID_MODEL=0  n_DROPMODEL_TYPE=1
n_ID   3 (2200003 · FAR)   s_NAME=創角用鎚  n_QUALITY=1  s_TAG_EXTRA=(ว่าง)  n_TAG_LOOT=4168  n_ID_MODEL=2  n_DROPMODEL_TYPE=1
n_QUALITY ทั้งตาราง 6 ค่า:  3(414) · 4(290) · 0(136) · 2(70) · 1(52) · 5(12)   [รวม 974]
```
🔴 **`s_TAG_EXTRA` มีแค่ 3 ค่าทั้งตาราง: ว่าง 842 · `1;2` 111 · `1;1` 21**
⇒ **86% ของแถวได้ค่าเดียวกัน ⇒ อ่อนเกินกว่าจะเป็นตัวขับสเกลสีที่มี ≥3 เฉด** — ข้อนี้ทำให้ครึ่งหนึ่งของ H1 อ่อนลงมาก

**② 🆕 จานสีจริงมีอยู่ในข้อมูลที่เรามีแล้ว** — `gamedata/tables/CONSTDATA_TH__FONT_COLOR.tsv` **57 แถว** `n_ID f_RED f_GREEN f_BLUE`
```
n_ID=1  255,255,255 ขาว   n_ID=2  255,255,0 เหลือง   n_ID=7  255,0,0 แดง   n_ID=14 255,128,64 ส้ม
n_ID=11 0,236,0 / n_ID=22 0,255,0 เขียว              n_ID=12 81,168,255 ฟ้า
```
⚠️ **การจับคู่ n_ID ↔ สีที่ตาเห็น เป็นการเทียบเฉด ไม่ใช่หลักฐาน** — ยังไม่มีใครวัดพิกเซล
และ **ยังไม่มีหลักฐานว่าไคลเอนต์ index ตารางนี้เพื่อป้ายชื่อ** (นั่นคือจ็อบ **S5**)

**③ 🆕 สเกลความหายากมีรูปทรงในข้อมูลจริง** — `CONSTDATA_TH__E_DROPS_QUALITY.tsv` (26 แถว)
มีคอลัมน์น้ำหนัก **5 ตัว: `n_WEIGHT_W · n_WEIGHT_G · n_WEIGHT_B · n_WEIGHT_P · n_WEIGHT_O`** (W/G/B/P/O = ตัวย่อสี — **อ่านจากชื่อคอลัมน์ ยังไม่พิสูจน์**)
⇒ ✅ **H1 ไม่ใช่การเดา มันมีรูปทรงในข้อมูลรองรับ**
⇒ 🔴 **แต่ตามต่อไม่ได้จากคลาวด์: `n_QUALITY` มี 6 ค่า (0..5) แต่คอลัมน์สีมี 5**
การจัดแนวเป็นไปได้อย่างน้อยสองแบบ — `{1..5}→W..O` (0 พิเศษ) หรือ `{0..4}→W..O` (5 พิเศษ)
🔴 **และสองแบบนี้ให้คำตอบตรงข้ามกันพอดีสำหรับ `n_ID 423` ซึ่ง `q=0`** ⇒ นี่คือเหตุผลที่ต้องมี **S4/S5**

**④ ผลลบมีขอบเขต (bounded) — สามข้อ:**
- **ไม่มีตารางใดใน 188 ไฟล์ที่ map `n_QUALITY` → `FONT_COLOR.n_ID`** (ค้น `PF_GAMEDATA_COLUMNS.tsv` ทั้งไฟล์: คอลัมน์ที่มีคำว่า COLOR มี 5 แถว = FONT_COLOR เอง 4 + `MOBS.n_SKIN_COLOR`)
- **`gamedata/lua/` 616 ไฟล์ grep `FONT_COLOR` = 0 hits** ⇒ **ผู้ที่ index เข้า FONT_COLOR อยู่ในโค้ดไคลเอนต์เท่านั้น**
- **ไม่เคยมีใครในโปรเจกต์เดินเส้น "สี" เลย** — grep `SetTextColor|text color|font color|D3DCOLOR|namecolor` ใน `reports/ docs/ src/ tools/` ของ repo เซิร์ฟเวอร์ = **0 ไฟล์** · ใน `external/` 8 ตาราง grep `NameColor|DrawName|NameLabel|FontColor|NameBoard` = **0 hits**
- **ขอบเขตของผลลบทั้งสามข้อ:** committed artifact ของสอง repo ณ HEAD ที่ระบุเท่านั้น — **ไม่ได้อ้างว่าไม่มีอยู่ในอิมเมจ**

**⑤ 🔴🔴 ช่องว่างมีรูปทรงที่ระบุตำแหน่งได้แม่น — และมันคือเหตุผลที่ใบนี้คุ้ม**
`reports/PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md:96-103` ลิสต์ช่วงที่ decode ครบ 7 ช่วง
มี **`NameBoardPlayer update 0x5BD320..0x5BD8E0 · 490 ins · COMPLETE`**
🔴 **และไม่มี `NameBoardNPC` update อยู่ในรายการเลย**
⇒ **เส้นที่ `0x201F` เดินจริง (เพราะเราส่ง type 4) คือเส้นเดียวที่ยังไม่เคยมีใครเปิดอ่าน**
⇒ และเรามี **คู่ขนานที่ decode ครบแล้วเป็นตัวควบคุมให้เทียบตรง ๆ** — สภาพที่ดีที่สุดเท่าที่ใบ static จะเริ่มได้

**⑥ VA ฝั่ง actor ที่ pin ไว้แล้ว (ยกจาก artifact ที่ commit แล้ว — ไม่มีตัวไหนที่ R163 อ่านเอง):**
| อะไร | VA | provenance |
|---|---|---|
| `actor_type` u8 ที่ record `+0x10` · setter | `0x5DEC00` | `tools/pf_actor_type_dispatch_static.py:376-380` |
| ค่าที่ไคลเอนต์รู้จัก = **2..6 เท่านั้น** (2 `CNetActor` · 3 `CMyActor` · 4 `CNetNPC` · 5 `CAvatarNPC` · 6 Pet) | — | `PF_MPAUDIT_FOLLOWUP001…:220-222` · `remote_player_hypothesis.py:174-176` |
| **`NameBoardPlayer` ctor** (0x78 B) | `0x456580` | `PF_MPAUDIT_FOLLOWUP001…:177` |
| 🔴 **`NameBoardNPC` ctor** (0xC0 B) | **`0x45C560`** | เดียวกัน |
| `NameBoardPlayer` bind widgets | `0x5BE080` | `PF_MPAUDIT_FOLLOWUP001…:179` |
| `LABEL_NAME` = board `+0x54` (literal `0xF0C794`) | — | `tools/pf_actor_type_dispatch_static.py:362` |
| **`NameBoardPlayer` update (ตัวควบคุม decode ครบ)** | `0x5BD320..0x5BD8E0` | `PF_CHUNK2_Q1…:103` |
| จุดเขียนชื่อลง `LABEL_NAME` | `0x5BD624..0x5BD645` | `PF_MPAUDIT_FOLLOWUP001…:201-203` |
| ชื่อมาจาก `BasicAttr +0x28` · mask bit `0x0001` · serializer | `0x4656F0` | `remote_player_hypothesis.py:194` |
| stream → factory | `0x5E4060 → 0x446F30 → 0x446990` | `PF_MPAUDIT_FOLLOWUP001…:230` |

**⑦ หมายเหตุด่าน G4 สำหรับคนออกแบบต่อ** — `external/PF_SERIALIZER_FIELDS.tsv` (6,931 แถว):
🔴 **`ActorAttr` = `tag EMPTY` ทั้ง R และ W (2 แถว len 0) — ห้ามสร้างอะไรบนข้อความนี้** `CLOSED` ไม่ได้แปลว่ามีฟิลด์
`CreateActorVital` มี 26 W entries · ฟิลด์ที่มี tag จริง (offset สัมพัทธ์กับ `DEREF(+0x18)`):
`+0x10` tag`0x32` len8 · **`+0x18`/`+0x19`/`+0x1A` tag`0x0B` len1 ×3** · `+0x1C` tag`0x19` len4 · `+0x20`/`+0x22` tag`0x12` len2 · **`+0x24` wstring16 (ชื่อ)** · `+0x40` wstring16 · `+0xF4`/`+0xF8` tag`0x14` len4 · `+0xFC` string8
⇒ **สามไบต์ `+0x18/+0x19/+0x1A` ที่ติดกันข้างชื่อ เป็นผู้ต้องสงสัยที่ถูกที่สุดสำหรับ "ไบต์ชนิด/สี"**
🔴 **แต่ความหมายของมันคลาวด์ตอบไม่ได้ ต้องขึ้นสะพาน** (ด่าน G6: ห้ามตั้งชื่อฟิลด์จาก header อย่างเดียว)

### สองสมมติฐานที่ใบนี้ต้องแยก
- **H1 — สีมาจากฟิลด์ในตารางไอเทม** (`n_QUALITY` / `s_TAG_EXTRA`)
  **หนุนโดย:** RE-066 วัดว่า **update path อ่าน `s_TAG_EXTRA` + `n_QUALITY`** และ **เราไม่เคยยิง update เลยสักเฟรม**
  🔴 **ค้านโดย:** ไอเทมเดียวกันคนละสีระหว่างสองเซิร์ฟเวอร์
- **H2 — สีมาจากสถานะบนสายที่เราไม่เคยส่ง** (สิทธิ์การเก็บ / เจ้าของ / ฟิลด์ของ element ที่อยู่นอก mask `0x12`)
  **หนุนโดย:** ข้อค้านข้างบน + ใบ GT-045 เขียนไว้เองว่า **"ฟิลด์อื่นของ element เราไม่เคยส่งเลยสักรอบ"**

🔴 **ตัวทดสอบราคาศูนย์ในเกมที่ *ทำไม่ได้* — เขียนไว้กันคนเสียเวลาคิดซ้ำ:**
สอง element ที่เรายิงทุกครั้งมี `n_QUALITY` ต่างกัน (423→0 · 3→1) ⇒ ถ้าเห็นป้ายทั้งสองจุดพร้อมกันแล้วสีเท่ากัน H1 ตายทันที
**แต่** จุด FAR ห่าง 800 หน่วย น่าจะเกินระยะวาดป้าย (ไม่มีใครเคยเห็นป้ายที่จุดนั้น) และการย้ายให้ใกล้กัน =
**เปลี่ยนดีไซน์เลน = กินงบเวอร์ชัน** ซึ่ง **`HYP-PF-032` เหลือศูนย์** ⇒ **ห้ามทำในเกม ต้องตอบจาก static**

### ✅ จ็อบที่ **ปิดไปแล้วบนคลาวด์** — หน้าสะพานข้ามได้เลย ไม่ต้องรัน
- ~~ค้นชุดส่งมอบ `external/` ก่อนถอด (กฎบังคับข้อ ④)~~ ⇒ **ทำแล้ว: `ไม่เจอ`**
  grep `NameColor|name_color|DrawName|NameLabel|HeadName|TitleColor|FontColor|NameBoard` ใน `external/` ทั้ง 8 ตาราง = **0 hits**
- ~~ค้น `gamedata/` ก่อนเปิดใบขุดข้อมูลเกม (กฎบังคับข้อสอง)~~ ⇒ **ทำแล้ว: `เจอ FONT_COLOR (57 สี) + E_DROPS_QUALITY (สเกล 5 ระดับ W/G/B/P/O)`
  แต่ไม่เจอตัวเชื่อม `n_QUALITY → FONT_COLOR.n_ID` ในตารางใดเลย และ Lua 616 ไฟล์ = 0 hits** (รายละเอียด §"ปิดแล้วบนคลาวด์" ข้อ ②③④)

### จ็อบที่เหลือ — **ต้องใช้อิมเมจทั้งหมด**

🔴🔴 **อ่านสองบรรทัดนี้ก่อนเริ่ม — เลข S ไม่ใช่ลำดับ:**
**ลำดับที่ต้องทำคือ `S0 → S6 → S7 → S8 → S5 → S1 → S2 → S4 → S3`** (เลขเรียงตามหัวข้อที่มันตอบ ไม่ได้เรียงตามลำดับงาน)
🔴 **ห้ามทำ `S1` ต่อจาก `S0` เพราะเลขติดกัน** — `S1` เป็นฝั่งไอเทมซึ่งเป็นทางที่ตันง่ายที่สุด ดูบล็อกทางออกท้ายรายการ

🔴 **ทางออกเมื่อฝั่งไอเทมตัน — ต้องอ่านก่อนเขียนผลลบ:**
สมมติฐาน *"สีถูกเลือกที่ไหนสักแห่งหลัง `0x00892580`"* **ผิดได้ง่ายมาก** เพราะสีป้ายน่าจะถูกตั้งที่
**NameBoard / label widget** ซึ่งอยู่คนละเส้นกับ item-table decoder โดยสิ้นเชิง
⇒ **ถ้า `S1`/`S2` เดินแล้วไม่เจอตัวเลือกสี ห้ามปิดใบเป็น bounded negative ทันที** — ต้องผ่านสองทางนี้ก่อน:
  ① **`S4`** (update path อ่าน `n_QUALITY`/`s_TAG_EXTRA` ไปทำอะไรต่อ) · ② **`S5`** (census `FONT_COLOR`)
🔴 **ผลลบที่เขียนโดยไม่แตะ `S6` เลย ไม่นับ** — `S6` คือช่องว่างที่ใบนี้บอกเองว่าแม่นที่สุด
**"ไม่เจอเพราะไม่เคยไปถึง" ไม่ใช่ผลลบ มันคือรอบที่ยังไม่จบ**

(หยุดได้ทันทีที่ตอบ objective ได้พร้อมหลักฐาน)

**S0. ด่านตัวควบคุมก่อนเสมอ** — verify sha ของอิมเมจ `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · **14,759,424 B** (ค่าที่ RE-066 พิน)
+ verify span ของ `0x00892580` (`FULL_ID_ROW` sha `1ce8aa30…c368e7`) และ `0x005F41E0` (`CREATE` sha `d8011e41…10f105`)
🔴 **sha ไม่ตรง = หยุดและรายงาน ห้ามเดินต่อ** · 🔴 **VA→offset ต้อง map ต่อ section** (อิมเมจมี 6 sections delta ต่างกัน: `.text` `0x400C00` · `.rdata` `0x401C00` · `.data` `0x402800`)

**S6. 🔴 เริ่มที่ข้อนี้ ไม่ใช่ฝั่งไอเทม — `NameBoardNPC` update อยู่ที่ VA ไหน และเขียนสีอะไรลง label**
จาก ctor `0x45C560` (0xC0 B) → หา vtable → หา update
**เทียบกับคู่ขนานที่ decode ครบแล้ว `NameBoardPlayer update 0x5BD320..0x5BD8E0` (490 ins) เป็นตัวควบคุมตรง ๆ**
🔴 **เหตุผลที่ข้อนี้มาก่อน:** มันคือช่องว่างที่ระบุตำแหน่งได้แม่นที่สุดที่เรามี · มี ctor pin แล้ว · มีคู่ขนานให้เทียบ ·
**และมันอยู่บนเส้นที่ `0x201F` เดินจริง** (เพราะเราส่ง `actor_type=4` ทุกจุด — วัดแล้ว)

**S7.** `NameBoardNPC` bind widget ชื่ออะไรบ้าง — มี `LABEL_NAME` (board `+0x54`) ไหม · คู่ขนานคือ `0x5BE080`

**S8.** **ค่าไหนแยก "ผู้เล่น / NPC / ศัตรู" ตอนเลือกสี** — `actor_type` (2/3/4) เอง · faction · หรือ relation
จุดตั้งต้น: factory `0x446990` + setter `0x5DEC00` + `NPCAttr` faction `+0x68` — **ตอบด้วย branch ที่อ่านได้จริง**

**S5. (ถูกที่สุด · อาจชี้ขาด H1 ได้ในครั้งเดียว) census literal `FONT_COLOR`**
ค้น UTF-16 `L"FONT_COLOR"` + `f_RED`/`f_GREEN`/`f_BLUE` ในอิมเมจ แล้วไล่ผู้เรียกผ่าน decoder `0x00890EF0`/`0x00890E70`
🔴 **ไม่มีผู้อ่านเลย = ผลลบราคาสูงมาก** (แปลว่าป้ายชื่อไม่ได้ใช้ตารางนี้) · มีผู้อ่าน = ไล่ผู้เรียกได้ทันที

**S1. ฝั่งไอเทมบนพื้น: ใครเลือกสีของข้อความที่ `create path A` วาด**
เดินขึ้นจาก `0x005F4731 → 0x00892050` (`STRING_FIELD` sha `550c1178…aac3be69`) และรอบ ๆ `0x005F46FA..0x005F4897` ใน span `CREATE`

**S2.** สีนั้นอ่านจาก **field offset ไหนของ element** — เทียบกับ store `0x005F878D lea eax,[esi+0x14]` และ element ctor `0x005F8329`

**S4. 🔴 ตัวชี้ขาด H1** — `n_QUALITY` / `s_TAG_EXTRA` ที่ **update path** อ่านมาที่ `0x005F4CAC` **ถูกใช้ทำอะไรต่อ** (เข้าตารางสีหรือเปล่า)
เดินใน `UPDATE [0x005F4C00,0x005F4DEE)` หลัง `0x005F4D2D → 0x00891EE0`
· query sites ที่ pin แล้ว: `s_TAG_EXTRA` (`0x00F0C27C`) ที่ `0x005F4CC9` · `n_QUALITY` (`0x00F0C190`) ที่ `0x005F4D21`
🔴 **จำไว้: เราไม่เคยยิง update path เลยสักเฟรม** ⇒ ถ้าสีมาจากเส้นนี้ นั่นอธิบายได้ทันทีว่าทำไมของเราตกไป default

**S3. ปิดวง** — offset ที่ S2/S8 ชี้ **อยู่ในหรืออยู่นอก mask `0x12`** (`0x10` position | `0x02` dword) ที่เราส่ง
ตัวเทียบฝั่งเรา: `src/pirateforce_foundation/ground_loot_hypothesis.py:186` · element dirty mask `+0x28`
**ตอบตรง ๆ ข้อนี้คือสิ่งที่เลนโค้ดรอ**

### เกณฑ์จบใบ
ตอบ objective พร้อม **VA + span + sha ต่อฟังก์ชันที่พึ่ง + recursive CFG errors 0**
หรือชน **bounded negative ที่ระบุขอบเขตครบ** (ด่าน G1 — **ห้ามเขียน "ไม่มี" ลอย ๆ**) · **ผลลบมีค่าสูงในใบนี้**

### nonclaims ที่ต้องติดไปกับผล
- **สีในตารางเทียบอ่านด้วยตา ไม่ได้วัดค่าพิกเซล** — ทุกข้อสรุปที่ยืนบนตารางนั้นสืบทอด nonclaim ข้อนี้
- **ภาพอ้างอิงอาจเป็น client คนละ build หรือคนละภูมิภาค** — ยังตัดข้อนี้ทิ้งไม่ได้ · ถ้าตัดได้ให้เขียนว่าตัดด้วยอะไร
- **"ผู้เล่นเขียวเพราะกิลด์เดียวกันหรือเปล่า" ยังไม่มีหลักฐาน** — ห้ามใช้เป็นสมมติฐานตั้งต้น
- static ไม่บอกว่า runtime เดินเส้นนั้นจริง (`SCENE-013` null prior ยังเป็นความเสี่ยงแยก)
- **"เปิดอ่านฟิลด์ไหน" ≠ "อะไรตัดสินการวาด"** — บทเรียน `D4` ของ R161-b · ห้ามย่อข้ามชั้น
- เซิร์ฟเวอร์ต้นฉบับปิดไปแล้วและกู้ไม่ได้ — ใบนี้พูดถึงพฤติกรรมของ **ไคลเอนต์ที่ ship มา** เท่านั้น
  ภาพของเซิร์ฟเวอร์เดิมเป็น **หลักฐานว่าไคลเอนต์เคยวาดสีอื่นได้** ไม่ใช่หลักฐานว่าเซิร์ฟเวอร์เดิมส่งอะไร

### 🔴 นอกขอบเขตของใบนี้ (อย่าลากเข้ามา)
**ชื่อที่หายไปจาก UI ซ้ายบน · แผงเป้าหมายที่เราไม่มี** — สองเรื่องนั้นเป็นฟิลด์ของ **บล็อกแอตทริบิวต์ตัวผู้เล่นเอง**
คนละเส้นกับป้ายชื่อบนพื้น **ต้องเป็นใบแยก** (จดไว้ในทะเบียน `REAL_SERVER_DIVERGENCE.tsv` แล้ว แถวที่ 3)

> 🔢 **หมายเหตุเลข (chief R163):** **067 ว่างจริง** — ตรวจแล้วทั้งสองคิว ไม่มี `GT-067` ไม่มี `RE-067` ตัวอื่น
> 🔴🔴 **แต่คำว่า "ตัวนับชุดเดียวกัน" ที่หัวไฟล์เขียนไว้ ไม่ตรงกับความจริงที่ HEAD แล้ว** (`pf-adversary` R163 จับได้):
> **`GT-060` กับ `RE-060` มีอยู่พร้อมกัน** และ **`GT-064` กับ `RE-064` ก็มีอยู่พร้อมกัน** — เป็นใบคนละใบ คนละเรื่อง
> ⇒ **ตัวนับแตกเป็นสองชุดไปแล้วโดยพฤตินัย** · **ห้ามใครสมมติว่า "เลขนี้ว่างเพราะอีกคิวไม่ได้ใช้"**
> ⇒ **ก่อนเปิดใบใหม่ ต้อง grep เลขนั้นในทั้งสองไฟล์เสมอ** · เลขว่างถัดไปที่ตรวจแล้ว = **068 ทั้งสองคิว**
> 📌 **เรื่องที่ต้องให้เจ้าของเคาะ:** จะรวมตัวนับกลับ (แพง ต้องเปลี่ยนชื่อใบที่ commit แล้ว = ห้ามตามกฎ)
> หรือ **ยอมรับว่าเป็นสองชุดแล้วแก้หัวไฟล์ให้ตรง** — chief เสนอทางหลัง แต่ยังไม่แก้หัวไฟล์จนกว่าจะมีคำตอบ

### 🔴 ของที่ต้องแก้ก่อน/ระหว่างทำใบนี้ — เจอระหว่างเตรียมใบ R163 ไม่ใช่ส่วนหนึ่งของ objective
**verifier ของสองใบที่ปิดไปแล้ว ไม่ได้อยู่ใน VCS** ⇒ **คลาวด์ตรวจวิธีของ RE-060/RE-066 ไม่ได้เลยแม้แต่ระดับอ่านโค้ด**
```
RE-066 อ้าง  pf_bridge\staged\re066_static_verify.py       sha 676c5837…af511308   -> ls staged/ + git ls-files staged/ = ไม่มี
RE-060 อ้าง  pf_bridge\staged\re060_code_matrix.py                                 -> ไม่มี
RE-060 อ้าง  pf_bridge\staged\re060_code_matrix_output.txt  31,929 B                -> ไม่มี
```
(`staged/` tracked 39 ไฟล์ · `.py` มีแค่ `re059_extract_capture.py` และ `gt047_patch_run_20260824_1438/pf_validate_capture_fields.py`)
⇒ **ขอให้หน้าสะพาน `git add` สามไฟล์นี้** — ไม่ต้องมีอิมเมจก็อ่านวิธีได้ และใบนี้จะยกวิธีของ RE-066 มาใช้ซ้ำ
🔴 **ไม่ใช่เงื่อนไขบล็อกใบนี้** — ใบเดินได้โดยไม่มีมัน แค่จะตรวจย้อนกลับไม่ได้

### result (ยังไม่มี — ใบเปิดอยู่ · สองช่องบังคับถูกกรอกจากคลาวด์แล้ว)
```
ค้นใน pf_bridge\external\ แล้ว: ไม่เจอ
  (grep NameColor|name_color|DrawName|NameLabel|HeadName|TitleColor|FontColor|NameBoard ใน external/ 8 ตาราง = 0 hits · R163 cloud)
ค้น gamedata แล้ว: เจอ CONSTDATA_TH__FONT_COLOR.tsv (57 สี) + CONSTDATA_TH__E_DROPS_QUALITY.tsv (n_WEIGHT_W/G/B/P/O)
  แต่ ไม่เจอ ตัวเชื่อม n_QUALITY -> FONT_COLOR.n_ID ในตารางใดเลยจาก 188 ไฟล์ · gamedata/lua/ 616 ไฟล์ grep FONT_COLOR = 0 hits
  (R163 cloud · pf-static-re)
ผลจ็อบ S0 (ด่านตัวควบคุม): ____________________
ผลจ็อบ S6 (NameBoardNPC update VA): ____________________
ผลจ็อบ S7 / S8 / S5 / S1 / S2 / S4 / S3: ____________________
```


### 🆕 หลักฐานใหม่ที่มาถึงหลังเปิดใบ — **GT-035 PASS (2026-08-25 15:04-15:36 +07:00) · บันทึกโดย chief R164**

**[สังเกตแล้ว · attended สองรอบ · จ็อบ 1137-1139 (r1) · 1140-1142 (r2) · จดหมาย `20260825_1550`]**
🔴 **ชั้นหลักฐาน: client-observable เท่านั้น** · 🔴 **ตัวเลขบันไดทั้งหมดมาจากวิดีโอรอบ 2 แหล่งเดียว** — รอบ 1 ไม่เห็น `3857` และไม่เห็นขั้นแรก (`evidence_screens/GT035_1138_HPPANEL_432-476s.jpg`)

หลอดเลือดของ `0x201F` **ขยับจริงตามที่เซิร์ฟเวอร์สั่ง** (`3857 → 2893 → 2893 → 771`)
**ทั้งที่ป้ายชื่อของมันขึ้นสีเขียว** — สีที่เซิร์ฟเวอร์เดิมใช้กับ **ผู้เล่น** ไม่ใช่ NPC

🎯 **ข้อมูลใหม่ของใบนี้ เขียนเป็นประโยคเดียว: สีของป้ายชื่อ กับ กลไก HP เป็นคนละเส้นกัน**

| ข้อ | ผลกับใบนี้ |
|---|---|
| หลอด HP เดินตามเฟรมที่เราส่ง | ✅ สังเกตแล้วหนึ่งคอนฟิก — **หลอดขยับได้ในกรณีที่ป้ายเป็นเขียว** · 🔴 **ห้ามอ่านว่า "เส้น HP ไม่ขึ้นกับสี/faction"** (chief เขียนอย่างนั้นในฉบับแรก `pf-adversary` ถอนให้) — ฟิลด์ที่คุมทั้งสองอย่างพร้อมกันแล้ว *อนุญาต* กรณีนี้ ยังเป็นไปได้เต็มที่ **และนั่นคือ objective ของใบนี้ทั้งใบ** |
| ป้ายชื่อเป็นสีเขียว **[ที่มา: จดหมาย `20260825_1420` · รอบ GT-045 v3 ~12:1x — *ไม่ใช่* รอบ GT-035 นี้]** 🔴 **ไม่มีใครจดสีระหว่างรอบ GT-035 ทั้งสองรอบ และตารางสีที่ใบ GT-035 บังคับก็ไม่เคยถูกทำ** | 🔴 **คำถามของใบนี้ไม่ถูกตอบเลยแม้แต่นิดเดียว** — ยังไม่รู้ว่าอะไรตัดสินสี · **และยังไม่รู้ด้วยซ้ำว่าสีคงเดิมข้ามบูตไหม** |
| แผง target แสดงชื่อ + HP ได้ | ✅ **ตัดสมมติฐาน "ไคลเอนต์ไม่รู้จักมันเลย" ทิ้ง** — มันรู้จัก แค่ทาสีคนละแบบกับที่เราคาด |

🔴 **สิ่งที่หลักฐานนี้ *ไม่* ทำ — อ่านก่อนเอาไปใช้:**
1. **ไม่ลดขอบเขตงานของใบนี้เลย** — จ็อบ S0-S8 ยังต้องรันครบเหมือนเดิม
2. **ไม่พิสูจน์ว่า `actor_type = 4` ถูกไคลเอนต์อ่าน** — พิสูจน์แค่ว่า *เส้น HP* ทำงาน
3. **ห้ามอ่านว่า "สีไม่สำคัญ"** — สีคือสิ่งเดียวที่ต่างจากเซิร์ฟเวอร์เดิมในภาพเทียบ (เกณฑ์ **P6**)
   ⇒ ใบนี้ยัง `blocks_promotion` ตามเดิม
4. **`hostile` ในชื่อใบ `GT-035` ยังไม่ถูกพิสูจน์** — และ **ใบนี้คือใบที่จะพิสูจน์หรือหักล้างมัน**

---

### result — RE-067 (ผลหน้าสะพาน 2026-08-25 16:26:03 +07:00 · บันทึกโดย chief R165 · 2026-08-25 ~17:0x +07:00)

**สถานะที่ปิด: PASS / MIXED** — ครึ่งไอเทม pin ได้จริง · ครึ่ง actor ปิดแบบ **bounded negative**
วิธี: static-only บนอิมเมจอ่านอย่างเดียว · ไม่เปิด GameClient/server · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB
verifier: `pf_bridge\staged\re067_static_verify.py` sha256 `838c70ef…56026e2` · `54/54` guards PASS exit 0
· actor-type verifier เดิม `111/111` PASS
S0 ด่านตัวควบคุมผ่าน: image `14,759,424 B` sha `9627211412ac60d5…b157028b623` ตรงค่าที่ RE-066 พิน · rerun `re066_static_verify.py` 17 spans ผ่านครบ

#### ① ครึ่งไอเทม — **pin ได้ และมันตอบคำถามหลักของใบ**

| สิ่งที่ pin | ค่า |
|---|---|
| จุดเลือก UI text property (CREATE) | `0x005F47FE..0x005F4822` |
| จุดเลือก (UPDATE) | `0x005F4D04..0x005F4D5D` |
| setter ปลายทาง | `0x005BACF0` (direct callers มีแค่ `0x005F4822` · `0x005F4D12` · `0x005F4D5D`) |
| **gate** | element **`+0x1B`** — `cmp byte [element+0x1B],0` · ศูนย์ ⇒ `push 0x34` (default) |
| **index/fallback** | element **`+0x1A`** (signed · รับเฉพาะ `1..6`) |
| ตาราง | `dword [index*4 + 0x00F30EC4]` ⇒ map `1..6 → 0x5D..0x62` · นอกช่วง ⇒ `0x34` |
| ctor ของ element | `[0x005F82C0,0x005F83F9)` · defaults **`+0x1B=0`, `+0x1A=1`** |
| dirty-mask ของ element | bit **`0x08` → `+0x1B`** · bit **`0x20` → `+0x1A`** (`LIST_CODEC [0x005F85B0,0x005F8869)` sha `ce0a58f7…`) |

🎯 **บรรทัดที่สำคัญที่สุดของทั้งใบ:**
**mask ที่เลนของเราส่งอยู่ทุกวันนี้คือ `0x12 = 0x10|0x02` ซึ่งอยู่นอกทั้ง `0x08` และ `0x20`**
⇒ decoder คงค่า ctor ไว้ (`+0x1B=0`) ⇒ CREATE ตกไปใช้ **default `0x34` เสมอ**
⇒ **สีป้ายที่ผู้เทสเห็น (แดง) ยังไม่เคยเป็นสีที่เราเลือก — เราไม่เคยส่งฟิลด์ที่เลือกมันเลยสักเฟรมเดียว**
⇒ ช่อง `ground-loot / ป้ายชื่อไอเทมบนพื้น` ใน `REAL_SERVER_DIVERGENCE.tsv` **ปิดไม่ได้จนกว่าจะยิงเลนที่ตั้ง gate** — ใบ **`GT-069`** (เปิดโดย R165)

**H1 (`n_QUALITY` ขับสี) — ถูกบางส่วนอย่างมีเงื่อนไข:** UPDATE (`[0x005F4C00,0x005F4DEE)` sha `7b14d16c…`)
จะ query `n_QUALITY` **ก็ต่อเมื่อ gate `+0x1B` ไม่เป็นศูนย์ และ fallback `+0x1A` > 0** แล้ว override เฉพาะ query สำเร็จ + ค่า > 0
· `s_TAG_EXTRA` (`@0x005F4CC9`) เข้าทาง **format text เท่านั้น ไม่ป้อน selector**
🔴 และ **traffic ของเราไม่เคยเดิน UPDATE เลยสักเฟรม** (เราส่งแต่ CREATE) ⇒ เส้น `n_QUALITY` ยังเอื้อมไม่ถึงจากเลนปัจจุบัน

#### ② ครึ่ง actor — **BOUNDED NEGATIVE (ยังไม่รู้ว่าอะไรตัดสินสี)**

- `actor_type=4` เลือก **คลาส** board ได้จริง (`CNetNPC` / `NameBoardNPC` · factory `[0x00446990,0x00446B2C)` · byte `record+0x10` · type `2..6`)
  แต่ **concrete `NameBoardNPC::update` `[0x005BD8E0,0x005BDF20)` ไม่อ่าน actor_type ซ้ำเป็นตัวเลือกสี**
- ในกราฟที่ decode ครบ **ไม่พบ**: direct read ของ `NPCAttr faction+0x68` · relation comparator `0x004A1D50` · call ไป loader `FONT_COLOR 0x005491B0`
- `NameBoardNPC::bind [0x005BE6C0,0x005BE98E)`: `LABEL_NAME` (`0x00F0C794`) → **`+0x50`** (ไม่ใช่ `+0x54` แบบ `NameBoardPlayer` — **แก้ offset จากจุดตั้งต้นของใบ**) · `LABEL_NICKNAME` → `+0x54` · `HPBAR` → `+0x4C` · `IMG_ARROW_FRIEND/ENEMY` → `+0x58`/`+0x5C`
- upstream ของ `board+0x34` = setter `0x005BBCE0` (caller เดียว `0x004B9C92`) → sink `0x00A97BD0` · caller คำนวณจาก `[object+0xF4] - [[0x1093198]+0x7BC]`
  ⇒ **ตั้งชื่อความหมายของค่านี้ไม่ได้จากหลักฐานที่มี** และไม่มี crosswalk ไป faction/relation/palette
- **ขอบเขตของผลลบ:** เฉพาะกราฟ direct/recursive-decodable ของฟังก์ชันที่ระบุ บนอิมเมจ sha นี้ · **indirect virtual consumer นอกกราฟยังไม่ถูกตัดทิ้ง**

#### ③ สองช่องบังคับ (ทำครบทั้งคู่ · รันซ้ำ local ไม่ยกผล cloud อย่างเดียว)

- `pf_bridge\external\` 8 ตาราง: grep `NameColor|name_color|DrawName|NameLabel|HeadName|TitleColor|FontColor|NameBoard` = **0 hits**
- `gamedata\`: **เจอ** `CONSTDATA_TH__FONT_COLOR.tsv` 57 แถว (`n_ID=1..57` · `f_RED/f_GREEN/f_BLUE`) + `E_DROPS_QUALITY` + `EQUIPMENT_BASE.n_QUALITY/s_TAG_EXTRA`
  · **ไม่เจอ** crosswalk `n_QUALITY → FONT_COLOR.n_ID` · `gamedata/lua/` 616 ไฟล์ grep `FONT_COLOR|f_RED|f_GREEN|f_BLUE` = **0 hits**
- loader `FONT_COLOR` มีจริงที่ `[0x005491B0,0x005494FE)` (caller rel32 เดียว `0x0054ADDF`) **แต่ไม่อยู่ใน concrete graph ทั้งสองเส้นข้างบน**

🔴 **ห้าม join `0x5D..0x62` เข้ากับ `FONT_COLOR.n_ID 1..57` เพราะเลขดูคล้ายกัน** — ไม่มี crosswalk field จริง (คำเตือนของใบเอง ยกมาทั้งดุ้น)

#### ④ nonclaims ที่ติดมากับผล — ห้ามตัดทิ้ง

1. สีในตาราง/ภาพเทียบเป็นการ **อ่านด้วยตา ไม่ได้วัดพิกเซล**
2. ภาพอ้างอิงของเซิร์ฟเวอร์เดิม **อาจมาจาก build/ภูมิภาคคนละตัว** — รอบ static นี้ตัดความเป็นไปได้นั้นไม่ได้
3. **ยังไม่มีหลักฐานว่า "ผู้เล่นเขียวเพราะกิลด์เดียวกัน"** — ห้ามใช้เป็นสมมติฐาน
4. static ไม่ยืนยันว่า runtime เดินเส้นนั้นจริง · `SCENE-013` null prior ยังเป็นความเสี่ยงแยก
5. **"โค้ดเปิดอ่านฟิลด์" ≠ "ฟิลด์นั้นตัดสินการวาด"** — ผลข้างบนแยก query · selector · setter · draw-property sink ออกจากกันโดยตั้งใจ
6. เซิร์ฟเวอร์ต้นฉบับปิดและกู้ไม่ได้ · ใบนี้สรุปเฉพาะพฤติกรรมที่อ่านได้จาก **ไคลเอนต์ที่ ship มา** — ภาพเก่าแสดงเพียงว่าไคลเอนต์ **เคยวาดสีอื่นได้**

#### ⑤ 🔴 ของที่ยังค้างจากบล็อก "ของที่ต้องแก้ก่อน/ระหว่างทำใบนี้" — **ยังไม่ถูกแก้ และตอนนี้ยาวขึ้นหนึ่งบรรทัด**

chief R165 ตรวจซ้ำแล้วบน clone รอบนี้: `ls staged/` + `git ls-files staged/` ⇒ **ยังไม่มีทั้งสามไฟล์เดิม และไม่มีไฟล์ใหม่ของใบนี้ด้วย**

```
RE-066 อ้าง  pf_bridge\staged\re066_static_verify.py   sha 676c5837…af511308  -> ยังไม่มีใน VCS
RE-060 อ้าง  pf_bridge\staged\re060_code_matrix.py                            -> ยังไม่มีใน VCS
RE-060 อ้าง  pf_bridge\staged\re060_code_matrix_output.txt  31,929 B          -> ยังไม่มีใน VCS
RE-067 อ้าง  pf_bridge\staged\re067_static_verify.py   sha 838c70ef…56026e2   -> 🆕 ยังไม่มีใน VCS เช่นกัน
```
⇒ **ขอหน้าสะพาน `git add` สี่ไฟล์นี้** (ไม่ต้องมีอิมเมจก็อ่านวิธีได้)
🔴 **ไม่ใช่เหตุให้ไม่ปิดใบ** — ผลของใบยืนบน span+sha ที่ตรวจซ้ำได้เมื่อมีอิมเมจ · แต่ **ตราบใดที่ไฟล์ยังไม่เข้า VCS คลาวด์ตรวจ *วิธี* ไม่ได้เลยแม้แต่ระดับอ่านโค้ด** — ข้อจำกัดนี้ติดไปกับทุกใบที่ยกวิธีของ RE-060/066/067 มาใช้ซ้ำ

---

## 🆕🔬 RE-068 ACTOR-NAMEBOARD-VALUE-034-SEMANTICS-001 [STATIC-ON-BRIDGE]: `board+0x34` ที่ `NameBoardNPC::update` sync เข้า `LABEL_NAME` **แปลว่าอะไร** — และ `FONT_COLOR` ถูกใครเรียกใช้จริง  [✅ **DONE / PASS-MIXED — ปิดโดย chief R167 · 2026-08-25 ~19:0x (+07:00)** · objective ปิดครบทั้งสองข้อ · ส่วนที่ตันเป็น **bounded negative ที่วัดเพดานแล้ว** · ผลหน้าสะพาน 2026-08-25 18:34 (+07:00) · จดหมาย `notes_to_chief\consumed\20260825_1834_RE-068-RESULT-PASS-MIXED.md` · บล็อก **result** ท้ายใบ]

> **ที่มา:** ข้อเสนอปิดท้ายของใบ RE-067 เอง (จดหมาย `20260825_1626` หัวข้อ "ข้อเสนอใบถัดไป (ไม่เปิดเอง)")
> RE-067 หยุดตรงที่ objective ปิดได้แล้ว **โดยตั้งใจ** และส่งครึ่งที่เหลือกลับมาให้ chief เป็นคนเปิด — นี่คือใบนั้น
> เกณฑ์ที่ใบนี้ค้ำ: **P6** ใน `SERVER_VERSION_MAP_AND_PROMOTION_20260825.md` · ทะเบียน: `REAL_SERVER_DIVERGENCE.tsv` แถว `npc-spawn / ป้ายชื่อ actor`

**objective (ตอบให้ได้สองข้อ ไม่ต้องมากกว่านี้):**
1. ค่า `board+0x34` มาจากไหนในเชิงความหมาย — caller `0x004B9C92` คำนวณ `[object+0xF4] - [[0x1093198]+0x7BC]` · `object+0xF4` คือฟิลด์อะไรของ actor และ global `[0x1093198]+0x7BC` คืออะไร
2. **ใครเรียก loader `FONT_COLOR 0x005491B0` จริง** — caller rel32 เดียวคือ `0x0054ADDF` · เดินขึ้นจากตรงนั้นจนถึงจุดที่ผลของมันถูกใช้ · ถ้าไปจบที่ **indirect/virtual** ให้หยุดแล้วรายงานเป็น bounded negative พร้อมระบุ vtable slot

**จ็อบ (ลำดับบังคับ · หยุดได้ทุกจุดถ้าชนเพดาน static — bounded negative คือคำตอบที่ถูก):**
- **T0 ด่านตัวควบคุมก่อนเสมอ** — verify image sha `9627211412ac60d5…b157028b623` · `14,759,424 B` · rerun `re067_static_verify.py` ให้ผ่าน 54/54 ก่อนเริ่ม (ถ้าไฟล์หาย ให้เขียนใหม่แล้ว **`git add` ตามข้อ ⑤ ของ RE-067**)
- **T1** decode `[0x004B9980,0x004B9D38)` (sha `4f0cf85e…`) ให้ครบ แล้วตอบว่า `[object+0xF4]` ถูกเขียนจากที่ไหน (หา writer ทั้งหมด ไม่ใช่ตัวแรกที่เจอ)
- **T2** ตามหา symbol/ขนาด/ผู้เขียนของ global `0x1093198` และ field `+0x7BC` · ถ้าเป็น singleton ให้ระบุ ctor
- **T3** เดิน `0x00A97BD0` (sink) ต่อ — มันเก็บค่าไว้ที่ไหน และมี consumer อะไรอ่านต่อ (รวม virtual `+0x240` ที่ใบ RE-067 ชี้ไว้)
- **T4** เดินขึ้นจาก `0x0054ADDF` หา call site ของผลลัพธ์ `FONT_COLOR` · ถ้าเจอ crosswalk `n_ID → RGB → property` ให้ pin ทั้งเส้น
- **T5** ถ้า T4 ตัน: ค้น `.rdata`/vtable ว่า property id `0x34` และ `0x5D..0x62` (ตารางที่ RE-067 pin) ถูกอ่านที่ไหนอีกบ้าง — **นี่คือสะพานเดียวที่จะเชื่อครึ่งไอเทมกับครึ่ง actor เข้าด้วยกันได้**

**กติกาบังคับ (เหมือนทุกใบ static):**
- ทุกคำตอบต้องมี **span + sha256 + จำนวน instruction + recursive CFG error count + gap**
- 🔴 **ห้าม join ตัวเลขเพราะมันดูคล้ายกัน** — โดยเฉพาะ `0x5D..0x62` กับ `FONT_COLOR.n_ID 1..57` (RE-067 ห้ามไว้ชัดแล้ว)
- 🔴 **ห้ามอ้างอะไรเกี่ยวกับเซิร์ฟเวอร์ต้นฉบับ** — ปิดและกู้ไม่ได้ตลอดกาล
- 🔴 **"ไม่พบ" ≠ "ไม่มี"** — ผลลบต้องเขียนขอบเขตกำกับเสมอ (กราฟไหน อิมเมจ sha อะไร)
- ค้น `pf_bridge\external\` และ `pf_bridge\gamedata\` **ก่อน** เปิดงานขุดใด ๆ (กติกา 18:22 ข้อ ④ · R132)

**สิ่งที่ใบนี้ *ไม่* ทำ:** ไม่แตะครึ่งไอเทม (RE-067 ปิดไปแล้ว) · ไม่เปิดเกม · ไม่ตัดสินว่าอะไร "ควร" เป็นสีอะไร

> 🔢 **หมายเหตุเลข (chief R165):** grep `068` ทั้งสองคิวแล้ว — **ไม่มี `GT-068` ไม่มี `RE-068` ตัวอื่น** ⇒ เลขนี้ว่างจริง · `069` ถูกใช้โดย **`GT-069`** ที่เปิดในรอบเดียวกันนี้ (`GAME_TEST_QUEUE.md`) ⇒ เลขว่างถัดไป = **070** (ต้อง grep ซ้ำทั้งสองไฟล์ก่อนใช้ ตามกติกาตัวนับสองชุด)

### result — RE-068 (ผลหน้าสะพาน 2026-08-25 18:34 (+07:00) · บันทึกโดย chief R167 · 2026-08-25 ~19:0x (+07:00))

**คำตัดสิน: PASS-MIXED** — objective ปิดได้ทั้งสองข้อ ส่วนที่เดินต่อไม่ได้ถูกวัดเพดานไว้แล้วเป็น bounded negative
จดหมายฉบับเต็ม: `notes_to_chief\consumed\20260825_1834_RE-068-RESULT-PASS-MIXED.md`

**สามข้อที่ปิดแล้ว:**
1. **`board+0x34` ไม่ใช่สี และไม่ใช่ฟิลด์ของ runtime NPC actor** — มันคือค่าที่เหลือของช่วงรอลบตัวละครบนหน้าสร้างตัวละคร
   (`character-record+0xF4` ลบด้วย `app-singleton+0x7BC` แล้ว setter `0x005BBCE0` เก็บผลลง `board+0x34` ก่อนส่งเข้า widget sink `0x00A97BD0`)
   · writer ที่ผูก alias ได้คือ `cStateCreateActor::OnDeleteResult 0x004BAEB0` ที่ instruction `0x004BAFDD`
2. **`FONT_COLOR 0x005491B0` ถูกเรียกจาก resource-initialization chain เท่านั้น** ในกราฟที่ resolve ได้
   (vtable `0x00F238F8` slot `+0x18` → `0x0054AF40` → `0x0054A8D0` → call site `0x0054ADDF` → loader) · **caller เดียวทิ้งผล bool**
3. **ไม่พบ crosswalk** จาก `FONT_COLOR.n_ID` (1..57) ไป property id `0x34` หรือ `0x5D..0x62` ⇒ 🔴 **ห้าม join** ครึ่ง actor กับครึ่ง item ด้วยเลขที่บังเอิญคล้ายกัน
   (`board+0x34` เป็น **field displacement** ไม่ใช่ property id — คนละ namespace กันทั้งสามชุด)

**ด่านควบคุมที่ผู้ทำรายงานไว้:** image `9627211412ac60d5…b157028b623` (`14,759,424 B`) ก่อน-หลังตรงกัน ·
T0 `re067_static_verify.py` 54/54 ผ่าน · control `pf_ui_state_refresh_static.py` 292/292 ผ่าน ·
verifier ของใบนี้ `pf_bridge\staged\re068_static_verify.py` sha `b17b5411f2b99abacf4ab8a12904726871f5fcada1d08212d0f7c96847e1edbd` 46/46 ผ่าน ·
`external/ + gamedata/` snapshot ก่อน-หลัง 1,138 files / 45,154,691 bytes เท่าเดิม · recursive CFG 12 body พร้อม span+sha ครบ `DECODE_ERRORS=0`

🔴 **ของที่ยังไม่เข้า VCS (ขอจากคนหน้าสะพาน — เหมือนกรณี RE-067):**
`pf_bridge\staged\re068_static_verify.py` **ยังไม่มีในคลาวด์ clone** (ตรวจแล้วรอบ R167: `git ls-files staged/` ไม่มีไฟล์นี้ และไฟล์ไม่อยู่บนดิสก์)
⇒ **ขอให้ `git add` ไฟล์นี้** จะได้ rerun ซ้ำได้จากทุกที่ · จนกว่าจะ add ผลใบนี้ **ตรวจซ้ำได้เฉพาะบนเครื่องสะพาน**

**ผลต่อโปรเจกต์ (chief R167 อ่านให้):**
- ครึ่ง **actor** ของคำถาม "อะไรตัดสินสีป้ายชื่อ" **ชนเพดาน static แล้ว** — ไม่ใช่ว่าตอบไม่ได้ แต่ตอบได้ว่า *ทางที่เดินอยู่ไม่ได้พาไปที่นั่น*
- ⇒ 🔴 **ห้ามเปิดใบรูปเดิมซ้ำ** (ผู้ทำเสนอเองว่าอย่ารัน RE-068 ซ้ำแบบเดิม) · ถ้าจะเดินต่อจริงต้องเป็นใบที่เจาะ **receiver/vtable** ของ virtual `+0x240` / `+0x70` โดยเฉพาะ
- **รอบนี้ยังไม่เปิดใบนั้น และนี่คือเหตุผล:** ของที่จะได้คือ exact time unit/epoch ของ countdown หน้าสร้างตัวละคร ซึ่ง **ไม่ค้ำเกณฑ์ P6 และไม่ค้ำเลนไหนที่เปิดอยู่**
  ⇒ คุ้มค่าน้อยกว่า `RE-070` (orchestrator) ที่ค้ำ `GT-026` ข้อ 8 อยู่จริง · ถ้าเจ้าของเห็นต่าง เปิดได้ทันทีในรอบถัดไป

---

## 🆕🔬 RE-070 ORCHESTRATOR-TRANSITION-GATE-001 [STATIC-ON-BRIDGE]: **อะไรเป็นตัวเซ็ต MODE `[orch+0x28]`** ของ session/connection orchestrator (vtable `0xf45030`) — และ `[orch+0x24]` เป็น **ตัวตัดสิน** หรือแค่ **ตัวแสดงผล**  [✅ **DONE / PASS-MIXED — ปิดโดย chief R168 · 2026-08-25 ~20:0x (+07:00)** · ผลหน้าสะพาน 19:24 · เปิดโดย chief R166 · 2026-08-25 ~18:0x (+07:00) · ดู `### result — RE-070` ท้ายใบ]

> 🔢 **หมายเหตุเลข (chief R166 · อ่านก่อนแก้เป็น 069):** ตัวนับเป็นชุดเดียวกับ `GAME_TEST_QUEUE.md` **ห้ามแยกตัวนับ**
> `CLIENT_RE_QUEUE.md` ลำพังไม่มี `RE-069` **แต่ `GT-069` มีอยู่จริง** (`GAME_TEST_QUEUE.md` · GROUNDLOOT-NAMELABEL-TEXTPROP-SELECTOR-001)
> ⇒ **069 ไม่ว่าง** · เลขว่างถัดไปคือ **070** · grep `GT-070`/`RE-070` ทั้งสองคิวแล้ว = ไม่มีตัวอื่น
> 🔴 **นี่คือกับดักที่ลูกมือ `pf-static-re` ตกจริงในรอบนี้** (enumerate เฉพาะไฟล์นี้แล้วสรุปว่า 069 ว่าง) — จดไว้ให้รอบหน้าไม่ตกซ้ำ

> **ที่มา:** `GT-033` ปิดเป็น **ANSWERED** โดย chief R166 · สามช่องจากสี่ของตารางถูกวัดแล้ว **ผลลบทั้งสาม**
> ⇒ ตารางตัดสินของ GT-033 เองเหลือ **กิ่งที่สาม: mode/timer ของ orchestrator** และมันเป็นคำถาม **static** ล้วน
> ⇒ **บูตเกมเพิ่มไม่ขยับกิ่งนี้อีกแล้ว** · ข้อเสนอมาจากหน้าสะพานเองทั้งสองใบ (`20260825_1730` §③ · `20260825_1745` §③)

---

### 🔴🔴 อ่านก่อนอย่างอื่น — **สามคำแก้ที่ chief R166 ออกให้ ก่อนใครหยิบใบนี้ไปทำ**

ลูกมือ `pf-static-re` ไล่ของที่ commit แล้ว **ครบสองรีโป (grep 8 pattern)** แล้วพบว่าถ้อยคำที่โปรเจกต์เขียนต่อ ๆ กันมา **แข็งเกินหลักฐานต้นทาง** สามจุด:

1. 🔴 **`+0x28 ∈ {1,4}` แข็งเกินหลักฐานหนึ่งขั้น — และถูกคัดลอกต่อมาแล้วอย่างน้อย 5 ที่**
   (`GAME_TEST_QUEUE.md` ใบ GT-033 · `archive/CHIEF_CONTINUATION_ARCHIVE_20260820_R100_R101_R102.md:128` · จดหมาย `20260825_1710/_1730/_1745`)
   หลักฐานจริงใน `FACTPACK_R100_LOGOUT_TRANSITION_STATIC.md:142-144` พูดแค่ว่า *"reads a MODE field `[esi+0x28]` (branches on `==1` and `==4`)"*
   ⇒ `{1,4}` คือ **เซตของค่าที่ถูกเทียบใน `0x719ab0`/`0x719b90`** ไม่ใช่ **เซตของค่าที่ฟิลด์นี้ถือได้**
   **ไม่มีใครเคยตรวจว่ามันเป็น exhaustive switch หรือแค่สอง branch ที่ผู้อ่านเห็น** ⇒ ใบนี้ต้องตอบข้อนั้นด้วย
2. 🔴 **วงเล็บ `"(values 1 vs 4 — the two non-'return-to-game' outcomes)"` ที่ `FACTPACK_R100…:182-183` เป็น *การตีความของผู้เขียนใบ* ไม่ใช่ผลอ่านโค้ด**
   บรรทัด 142-147 ซึ่งเป็นตัวหลักฐานไม่ได้อ้างอะไรแบบนั้น ⇒ 🔴 **ห้ามยกไปใช้เป็น mapping `1=exit` / `4=char-select`** (หรือกลับกัน) **ใบไม่เคยบอก**
3. 🔴 **`[vtable+0xf4]` เป็น vtable ของ sub-object `[esi+0x18]`/`[esi+0x1c]` ไม่ใช่ slot ของ `0xf45030` เอง** (`FACTPACK_R100…:144-146`)
   ใครสรุปว่าเป็น slot ของ orchestrator จะผิด

🔴 **และคำเตือนเชิงโครงสร้างที่ใหญ่ที่สุด: `FACTPACK_R100_LOGOUT_TRANSITION_STATIC.md` ไม่มี span/sha256 ต่อฟังก์ชันเลยแม้แต่ใบเดียว**
ต่างจาก `RE-064`/`065`/`066`/`067` ที่ให้ครบทุกใบ · ต่างจาก `GT-054` ที่ verify ได้ 392/392 เพราะมี span
⇒ **ใบ R100 verify ไม่ได้แม้แต่บนสะพาน จนกว่าจะ re-derive ใหม่** ⇒ **ใบนี้ต้องถือว่า R100 เป็น "ข้อกล่าวอ้าง" ไม่ใช่ "ฐาน"**
⇒ 🔴 **จ็อบ T1 จึงเป็นการ re-derive ใบ R100 ไม่ใช่การต่อยอดจากมัน**

---

### objective (ตอบให้ได้สามข้อ ไม่ต้องมากกว่านี้)
1. **ใครเซ็ต `[orch+0x28]`** — หา **writer ทั้งหมด** ไม่ใช่ตัวแรก · แล้วบอกว่าแต่ละ writer ถูกเรียกจาก path ไหน: **inbound message handler / UI handler / timer-tick / อื่น**
2. **`[orch+0x28]` ถือค่าอะไรได้บ้างจริง ๆ** — `{1,4}` เป็นเซตปิดหรือไม่ · ถ้ามีค่าอื่น ค่าไหนนำไปสู่ branch ไหน
3. **`[orch+0x24]` เป็น gate หรือเป็น display** — มี threshold คงที่ไหม · อ่านเวลาจาก API ตัวไหน (`GetTickCount`/`timeGetTime`/QPC) · ใครเป็น writer
   🔴 หลักฐานที่มีตอนนี้คือ **ครึ่งบรรทัด** (`"elapsed-time formatting"`) ⇒ ถ้าเป็น formatting จริง มันอาจเป็นแค่ตัวแสดงผล **ไม่ใช่ตัวตัดสิน** · ประโยคสรุปของ R100 ที่ว่า *"holds a mode + a timer"* **แข็งกว่าหลักฐานที่มันยกมาเอง**

### 🎁 ของที่ chief ทำให้เสร็จแล้วบนคลาวด์ — **หน้าสะพานไม่ต้องทำซ้ำ**

**(ก) VA → file offset แปลงให้แล้วทั้งแปดตัว** (derive จาก `external/PF_PROTOCOL_REGISTRY.tsv:72` คู่ VA/file_off ในแถวเดียวกัน)
delta ต่อ section: `.text` = **`0x400C00`** · `.rdata` = **`0x401C00`**
🔴 **ตัวควบคุมอิสระของ delta** — จาก `notes_to_chief/consumed/20260821_0951_GT040-PART-B-RESULTS-from-assistant.md:15-18` (คนละใบ คนละรอบ คนละผู้เขียน):
`0x005E4060↔0x1E3460` · `0x00446F30↔0x046330` · `0x0088F2B0↔0x48E6B0` ⇒ **`0x400C00` ตรงทั้งสามตัว**

| VA | file offset | section | block_256 byte-guard (`factpack_L1/blocks_256.tsv`) |
|---|---|---|---|
| `0x00719AB0` tear-down | `0x00318EB0` | .text | `0x00318E00` `3cba6128fc887dad…` (:12696) |
| `0x00719B90` tear-down | `0x00318F90` | .text | `0x00318F00` `64802a0f19123952…` (:12697) |
| `0x00719BD0` conn-close | `0x00318FD0` | .text | `0x00318F00` (บล็อกเดียวกัน) |
| `0x00719C30` vital consume | `0x00319030` | .text | `0x00319000` `79064c4879bb9bec…` (:12698) |
| `0x00719C80` dispatch | `0x00319080` | .text | `0x00319000` (บล็อกเดียวกัน) |
| `0x00F45030` vtable base | `0x00B43430` | .rdata | `0x00B43400` (:46142) |
| `0x00F45058` slot `+0x28` | `0x00B43458` | .rdata | `0x00B43400` (บล็อกเดียวกัน) |
| `0x00F45124` slot `+0xf4` | `0x00B43524` | .rdata | `0x00B43500` `ae0490a8734eca22…` (:46143) |

**(ข) ค้นชุดส่งมอบ RE ของ Codex แล้ว (กติกา 18:22 ข้อ ④ · R132) — ผลคือ "ไม่เจอ"**
grep `f45030` · `719ab0` · `719b90` · `719c30` · `719c80` · `719bd0` · `719bef` · `f45058` บน
`PF_PROTOCOL_REGISTRY` / `PF_SERIALIZER_FIELDS` / `PF_FIELD_VALIDATION` / `PF_PROTOCOL_PRIORITY` / `PF_RUNTIME_CLASSMAP` = **0 hit ทุกไฟล์**
⇒ **ตาราง Codex ครอบเฉพาะ message/serializer ไม่เคยแตะ orchestrator เลย** ⇒ ช่องกรอกในผล: *"ค้นแล้ว ไม่เจอ"*

**(ค) ทั้งโปรเจกต์มีแหล่งเดียว** — `FACTPACK_R100_LOGOUT_TRANSITION_STATIC.md:134-153, 180-187, 208-220, 263-266`
ที่อื่นอีก **6 แห่งใน 2 รีโปเป็นการอ้างซ้ำคำต่อคำ ไม่ใช่หลักฐานอิสระแม้แต่แห่งเดียว** (รวม `src/pirateforce_foundation/logout_hypothesis.py:118-126` และ `tools/verify_logout_return_select_encoder.py:17-19`)

**(ง) เมธอดที่เคยถูกจดไว้ — ครบชุดคือ 5 ตัว · ไม่มีใครจด slot layout ของ `0xf45030` ทั้งตาราง**
รู้แค่ slot `+0x28` = `0x719c80` (dispatch) และมี slot `+0xf4` ที่ปิด conn (ซึ่งเป็นของ sub-object — ดูคำแก้ข้อ 3)

**(จ) ชื่อคลาสของ `0xf45030` = ไม่มีในของที่ commit แล้ว** — `external/PF_RUNTIME_CLASSMAP.tsv` grep `f45030` = 0 hit ·
`FACTPACK_L2_CLASSCENSUS001_20260820.tsv` **ไม่มีคอลัมน์ VA เลย** (ได้จาก `strings_ascii.tsv` ล้วน) ⇒ ต้อง resolve RTTI บนอิมเมจ
🔴 **เตรียมใจว่าอาจ resolve ไม่ได้** — `RE-065` เจอกรณี custom RTTI ที่ resolve จาก static ไม่ได้มาแล้ว

### จ็อบ (ลำดับบังคับ · หยุดได้ทุกจุดถ้าชนเพดาน static — **bounded negative คือคำตอบที่ถูก**)

- **T0 ด่านตัวควบคุมก่อนเสมอ** — verify image sha256 `9627211412ac60d5…b157028b623` · `14,759,424 B` ·
  แล้ว **hash หน้าต่าง 256 ไบต์ทั้งสี่บล็อกในตาราง (ก) เทียบกับ `blocks_256.tsv`** ก่อนเชื่อ VA ใด ๆ
  🔴 **ตัวควบคุมเชิงบวกของเครื่องมือ:** ก่อนเดิน `0x719ab0` ให้ decode `0x00446F30` ซึ่งมี span+sha256 อิสระอยู่แล้วที่
  `notes_to_chief/consumed/20260821_0951_GT040-PART-B-RESULTS-from-assistant.md:15` (`9c1157d3109c27c4…`) —
  **ได้ sha ตรง = เครื่องมือเชื่อได้ · ไม่ตรง = หยุด อย่าเดินต่อ**
- **T1 re-derive ใบ R100 (ไม่ใช่ต่อยอด)** — decode `0x719ab0` และ `0x719b90` **ทั้งฟังก์ชัน** ให้ span+sha256+instruction count+CFG error+gap ครบ
  แล้วตอบ objective ข้อ 2 และ 3 · **และบอกด้วยว่า `0x719ab0` กับ `0x719b90` ต่างกันตรงไหน** — ใบ R100 เขียนคู่กันตลอดแต่**ไม่เคยบอก**
- **T2 call-site census ของ `0x719c30`** — 🔴 **ทำก่อน `+0x24`** เพราะมันมีตัวยึดที่พิสูจน์แล้วสองตัว
  (descriptor singleton `0x1030e24` + app object `[0x1093198]`) ⇒ ต้นทุนต่ำกว่า และอาจตอบ objective ข้อ 1 ในตัว
  **วิธีที่ใช้ได้จริงมีตัวอย่างในรีโปแล้ว:** สแกน `E8`/`E9` rel32 ทุกออฟเซ็ตของ `.text`
  (`notes_to_chief/consumed/20260821_0951_GT040-PART-B-RESULTS-from-assistant.md:95,150`)
- **T3 call-site census ของ `0x719ab0` / `0x719b90`** ด้วยวิธีเดียวกัน ⇒ ตอบว่า **inbound handler? UI handler? timer/tick?**
- **T4 หา writer ทั้งหมดของ `[esi+0x28]`** — ต้อง disassemble ไม่ใช่ grep · 🔴 **ต้องหาทุก writer ไม่ใช่ตัวแรก** (บทเรียน T1 ของ RE-068)
- **T5 dump slot ทั้งตารางของ `0xf45030`** + พยายาม resolve RTTI/typeid → ชื่อคลาสจริง · และยืนยันว่า `[esi+0x18]`/`[esi+0x1c]` เป็นอะไร
- **T6 (ถ้า T1-T4 ตัน)** — ไล่ **UI typeid-name binding** ให้ทะลุเพื่อไปถึงโค้ดที่ปุ่มรันจริง
  🔴 ใบ R100:80-86 **ยอมแพ้ตรงนี้ แต่ไม่ได้พิสูจน์ว่าทำไม่ได้** — บอกแค่ว่า "ไม่ถึงด้วย immediate/xref" ⇒ **ยังเป็นเส้นเปิดถ้าใช้วิธีอื่น**

### 🔴 rider แยกใบได้ถ้าเวลาไม่พอ — **ปมที่ไม่มีใครจด และมันขัดกับ nonclaim ของ GT-033 ตรง ๆ**

`external/PF_FIELD_VALIDATION.tsv:144` เขียนว่า:
```
ReturnSelectServerVital   W   observed_frames=2   parse_success=2   mismatch=0   capture_file_count=2   VALIDATED
```
แต่ `GT-033` เขียน nonclaim ว่า *"ยังไม่เคยมี client เห็น `0x709E` แม้แต่ไบต์เดียว"* และ
`src/pirateforce_foundation/logout_hypothesis.py:176` เขียนว่า `0x709E` **ไม่มี producer**
corpus ถูกแช่แข็ง **2026-08-15/16** ⇒ **ก่อน** variant B/C ทุกครั้ง

🔴 **อ่านได้สองทาง และ chief ไม่ตัดสิน:**
(i) มีอะไรบางอย่างเคย **ปล่อยเฟรมรูป RSS จริง** ⇒ **เปลี่ยนภาพของ GT-033 ทั้งใบ**
(ii) เป็น **schema collision ของ validator** ที่ `external/00_SEARCH_HERE_FIRST.md:87` เตือนไว้เองว่ามีช่องโหว่ (GT-047: ยอมรับ `field_offset` กลายพันธุ์)
⇒ **แยกสองข้อนี้ต้องเปิดไฟล์ capture 2 ไฟล์นั้น ซึ่งไม่มีบนคลาวด์** · ขอให้ระบุชื่อไฟล์ทั้งสองในผลเสมอ

### กติกาบังคับ (เหมือนทุกใบ static)
- ทุกคำตอบต้องมี **span + sha256 + จำนวน instruction + recursive CFG error count + gap**
- 🔴 **"ไม่พบ" ≠ "ไม่มี"** — ผลลบต้องเขียนขอบเขตกำกับเสมอ (กราฟไหน อิมเมจ sha อะไร วิธีค้นอะไร)
- 🔴 **ห้ามอ้างอะไรเกี่ยวกับเซิร์ฟเวอร์ต้นฉบับ** — ปิดและกู้ไม่ได้ตลอดกาล
- 🔴 **ห้าม join ตัวเลขเพราะมันดูคล้ายกัน**
- ค้น `pf_bridge\external\` และ `pf_bridge\gamedata\` **ก่อน** เปิดงานขุดใด ๆ — 🎁 **chief ทำให้แล้ว ผลอยู่ในบล็อก (ข)**

### เกณฑ์จบใบ
ปิดได้เมื่อ **objective ทั้งสามข้อมีคำตอบ หรือมี bounded negative ที่เขียนขอบเขตครบ** ·
🔴 **ไม่ต้องรอให้ไคลเอนต์เปลี่ยนหน้าได้จริงก่อนจึงจะปิดใบนี้** — ใบนี้ตอบ *"อะไรเป็นตัวตัดสิน"* ส่วน *"แล้วเราจะยิงอะไรไปให้"* เป็นใบถัดไป

### สิ่งที่ใบนี้ *ไม่* ทำ
ไม่เปิดเกม · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB · **ไม่ออกแบบ variant D** (ปิด socket โดยไม่ ack / ack แล้วเงียบไม่ปิด) —
variant D เป็น **nonclaim ของ GT-033 ไม่ใช่งาน** และการออกแบบมันก่อนรู้ผลใบนี้คือการเดา

---

### result — RE-070 (ผลหน้าสะพาน 2026-08-25T19:24:13+07:00 · บันทึกโดย chief R168 · 2026-08-25 ~20:0x (+07:00))

**สถานะ: `DONE / PASS-MIXED`** — objective ทั้งสามข้อมีคำตอบแบบ static
จดหมายฉบับเต็ม: `notes_to_chief\consumed\20260825_1924_RE-070-RESULT-PASS-MIXED.md`

**① writer ของ `[object+0x28]` (MODE) — census recursive CFG ครบทั้ง 31 slots ของ vtable พบสี่จุดเท่านั้น:**
`0x7197D0` (clear ใน UI-init · slot `+0x18` entry `0x719780`) · `0x7199EA` (คัดลอก `event_record+0x2C` · slot `+0x30` entry `0x719990`)
คู่ของ `+0x24` อยู่ที่ `0x7197CD` (clear) และ `0x7199E4` (`event_record+0x30 -> object+0x24`)
**ไม่มี writer จาก inbound handler หรือจาก tick ในกราฟที่วัด**

**② `+0x28` ไม่ใช่เซตปิด `{1,4}`** — handler รับ dword ใด ๆ แล้วทำ `dec; cmp 3; ja default` + jump-table สำหรับค่าเดิม `1..4` · ค่านอกช่วงไป default ได้

**③ `+0x24` เป็นทั้ง display และ gate (ไม่ใช่ display-only):** `delta = [object+0x24] - [app+0x7BC]` ·
`0x719990` ใช้ delta ในแขนงแสดงผล (MODE 1/4) · `0x719620` เทียบ `delta` กับค่าคงที่ **`3`** และถ้า `delta <= 3` และ `[object+0x18] != NULL`
จะเรียก virtual `[vtable+0xF4](false)` ของ sub-object · **writer/gate ไม่อ่าน `GetTickCount` / `timeGetTime` / QPC โดยตรง**

🔴 **erratum ต่อฐาน R100 — สามข้อ ต้องพกไปทุกที่ที่อ้าง R100:**
1. `0x719AB0` และ `0x719B90` **ไม่ใช่หัวฟังก์ชัน** — เป็น basic block ภายในฟังก์ชันเดียวที่เริ่ม `0x719990`
   ขอบเขตจริง `[0x00719990,0x00719C11)` · offset `0x00318D90` · len `641` · instr `176` · CFG errors `0` · gap `19` · indirect `1`
   · sha256 `a55288cb6a345d5c12d4d558dc7b13185f44bbc4cb6a2ac12188dbe1608e7576`
2. vtable `0xF45030` resolve ชื่อจาก factory `0x721700` ได้ตรง ๆ เป็น UTF-16 **`SystemSetting_LogoutConfirm`**
   ⇒ คำเรียก *session/connection orchestrator* ของ R100 **กว้างเกินหลักฐาน** · ของจริงคือ **UI logout-confirm handler ที่ถือ sub-object connection และมี transition logic**
3. `[vtable+0xF4]` ที่ `0x719BD0/0x719BE7` เป็น slot ของ sub-object `[object+0x1C]/[object+0x18]` ตาม correction R166 **ไม่ใช่ slot ของ `0xF45030`**

**MODE branch map (behavior ล้วน ไม่ตั้งชื่อ semantic):** `1` → res `0x2C4` + elapsed-display + `[+0x1C]` close=true ·
`2` → res `0x59D` · `3` → res `0x59C` · `4` → res `0x59E` + elapsed-display + `[+0x1C]` close=true + `[+0x18]` close=false · อื่น ๆ → default `0x2C4`
🔴 **ตารางนี้ไม่ใช่ mapping `1=exit` / `4=char-select`** — ใบนี้ไม่มีหลักฐานพอให้ตั้งชื่อสองค่านั้น **ห้ามเขียน**

**T0/reproducibility:** image sha ก่อน/หลัง `9627211412ac60d5…` ตรง · 256-byte guards ผ่านทั้งห้า · positive control `0x446F30` ตรง GT-040 ·
verifier `staged/re070_static_verify.py` **104/104 guards · failed 0** · วิธี negative ใช้ recursive CFG + 31-slot vtable walk ไม่ใช่ linear disassembler

**nonclaims ที่ต้องพกต่อ (แปดข้อในจดหมาย · สามข้อที่สำคัญที่สุด):**
① ไม่พิสูจน์ semantic ของ MODE ② writer census ครบภายใน factory + vtable graph แต่ **ไม่ exclude pointer alias จากโค้ดนอกกราฟทั้งโปรแกรม**
③ **ไม่ตั้งชื่อ `+0x24` ว่า timestamp/deadline/wall clock** — พิสูจน์เฉพาะ copy · subtraction · display · threshold gate

**🔴 rider — `ReturnSelectServerVital 0x709E` สองเฟรมขา W (chief ลงมือแล้วในรอบเดียวกัน):**
`PF_FIELD_VALIDATION.tsv`: `W = observed 2 / parsed 2 / files 2 / VALIDATED` · `R = observed 0 / NOT_OBSERVED`
⇒ **ไม่ขัด** กับ nonclaim ว่า client ยังไม่เคยรับ `0x709E` ขา R · **แต่หักล้าง**ถ้อยคำกว้างใน `logout_hypothesis.py` ที่ว่า *"0x709E has no client producer"*
✅ **chief R168 แก้ถ้อยคำแล้วสามจุด** (`src/pirateforce_foundation/logout_hypothesis.py` ×2 + `tests/test_logout_return_select_hypothesis.py` ×1)
พร้อมบล็อก erratum ที่พิน sha256 ของ capture ทั้งสองไฟล์ไว้ในซอร์ส · **ไบต์ของเลนไม่ขยับแม้ไบต์เดียว** (comment/docstring ล้วน)

---

## 🆕🔬 RE-071 SPAWNED-ACTOR-BASICATTR-PROVENANCE-001 [STATIC-ON-BRIDGE]: **actor ที่เกิดจาก `SPAWN_BARE` มี `BasicAttr` อะไรผูกอยู่จริง — และ ctor default ของ `+0x44` (current HP) / `+0x48` (max HP) คือเท่าไหร่**  [✅ **DONE / STATIC-CONTRADICTION-PINNED — ปิดโดย chief R170 · 2026-08-25 ~22:0x (+07:00)** · ผลอยู่ท้ายใบ · **คำตอบกลับด้าน: resident ต้องเป็น 100/100 ⇒ ที่เห็นบนจอไม่ใช่ผลปกติของ `ActorAttr` ใบเดียวกัน** · เปิดโดย chief R168 · 2026-08-25 ~20:2x (+07:00)]

> 🔢 **หมายเหตุเลข:** ตัวนับเป็นชุดเดียวกับ `GAME_TEST_QUEUE.md` **ห้ามแยกตัวนับ** · grep `GT-071`/`RE-071` ทั้งสองไฟล์ = ไม่มีใบอื่น ⇒ **071 ว่าง**
> ใบพี่น้องของรอบเดียวกันคือ **`GT-072`** (attended · actor-slot displacement) — **072 ก็ว่างและถูกจองแล้ว** ⇒ ใบถัดไปเริ่มที่ **073**

### 🔴🔴 อ่านก่อนอย่างอื่น — **คำถามเปลี่ยนรูปแล้ว อย่าหยิบคำถามเวอร์ชันแรกไปทำ**

จดหมาย `GT-030` รอบสาม (§⑧ ข้อ 1) เสนอไว้ว่า *"วัดว่าฟิลด์ไหนใน `MovementAttr mask 0x03` ที่ไคลเอนต์อ่านเป็นตาย"*
🔴 **chief วัดคำถามนั้นจบแล้วบนคลาวด์ในรอบ R168 — คำตอบคือ ไม่มีฟิลด์ไหนเลย** ⇒ **ห้ามเปิดใบตามถ้อยคำเดิม**

**หลักฐาน (re-derive เองจาก encoder จริง hash ตรง pin ทุกตัว ไม่ใช่การ quote):**
- `MOVE_A_2` = actor entry เดียว · attr เดียว · **`MovementAttr` field mask `0x03` = position(3×f32) + heading(1×f32) เท่านั้น**
  `src/pirateforce_foundation/remote_player_hypothesis.py:250-251,359-363,391-408,1513-1519`
- ตาราง bit→offset→tag ของ `MovementAttr` ตรงกันสามชั้น (server source `current/pf_login_game_server_v141.py:1211-1218,1231-1244` ·
  walker อิสระ `remote_player_hypothesis.py:1162-1165` · static image `reports/PF_MOVE_PROJECT001_*.md:42-56`)
  ⇒ `0x01` position · `0x02` heading · `0x04` mode · `0x08` flags · `0x10/0x20/0x40` f32 ×3
  🔴 **ไม่มี bit ไหนแตะ HP · ชื่อ · หรือสถานะเป็นตาย เลยแม้แต่ bit เดียว**
- predicate การตายทั้งสี่ตัวอ่านเฉพาะ `BasicAttr +0x44` (current HP) และ `+0x58` (death timer) ผ่าน `GetAttr`
  (`vt+0x74` → `0x44C630` = `mov eax,[ecx+0x348]`) — `reports/PF_HP_DEATH001_*.md:9`
- **ตัวควบคุมเชิงบวก:** `TARGET_SPAWN` ของ `HYP-PF-038` ประกอบด้วยวิธีเดียวกัน **มี HP อยู่ในไบต์จริง** (hash ตรง pin ทั้ง 7 แถว)
  ⇒ พิสูจน์ว่า walker อ่าน HP เจอเมื่อมันมีอยู่ ⇒ การไม่เจอใน `MOVE_A_*` เป็นผลลบจริง ไม่ใช่เครื่องมือบอด

### 🔴 และ "ผลที่ไม่มีใครทำนาย" — **มีคนทำนายไว้แล้วสามที่ ทั้งหมด commit แล้วก่อนรอบสามหลายวัน**

| # | claim | provenance | เกรด |
|---|---|---|---|
| ① | *"ใบแรกจะไม่ทำอะไร แต่ **ใบที่สองของ identity เดิม (เช่น MovementAttr update) จะเจอ HP==0 แล้วเข้าเส้นตาย**"* | `reports/PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md:380` | ติดป้าย `[INFERRED]` เอง |
| ② | *"`0x4446F0` calls the dead-state sync `0x4437C0` on EVERY update-path frame... a probe with HP 0 walks into the death chain **the moment its identity is re-sent**"* | `src/pirateforce_foundation/remote_player_hypothesis.py:225-230` | โมดูลของเลนนี้เอง |
| ③ | *"**An actor cannot be born dead.** ... **the death sequence needs at least two actor-entries for the same identity**"* | `reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md:5` | `[PROVEN]` (census 1 caller / 0 pointer) |
| ④ | ctor default ของ death timer `+0x58` = **`0.0f`** เขียนโดย BasicAttr ctor `0x464B0E` | `src/pirateforce_foundation/stats_progression_hypothesis.py:1330-1334` | static image |
| ⑤ | predicate คู่: `vt+0x40` (`0x454AC0`) = `HP==0 && timer>0` → dying latch · `vt+0x3C` (`0x454A70`) = `HP==0 && timer<=0` → death task `0x443990`→`0x4439E9`→`0x472810` `CActorTask_Dead` → `L"_F_DIE_000"` | `reports/PF_HP_DEATH001_*.md:428` (ERRATUM) · `stats_progression_hypothesis.py:1338-1370` | static image |

⇒ 🎯 **ประกอบกัน:** actor ที่ HP=0 + timer=0.0 (ctor default) + **actor-entry ใบที่สองของ identity เดิม** = ตรง predicate `vt+0x3C` เป๊ะ
⇒ death task + ท่านอน + `HP. 0` บนแผง · และลำดับจริงคือ `SPAWN_BARE`(ใบแรก) → `MOVE_A_1`(**ใบที่สอง** `t=252.37`) → `MOVE_A_2`(ใบที่สาม `t=267.37`)
🔴 **nonclaim ② ของจดหมายเองบอกว่าช่วง `t=222.4→267.4` กล้องคุมไม่ครบ ⇒ การตายอาจเกิดตั้งแต่ `MOVE_A_1` แล้ว ไม่ใช่ `MOVE_A_2`**
**อย่าออกแบบใบนี้บนสมมติฐานว่า `MOVE_A_2` เป็นตัวทริก**

### objective (claim เดียว — ตอบคำถามที่เหลืออยู่จริง)

> 🔴 **`SPAWN_BARE` ส่ง `current_hp = 100` / `max_hp = 100` ออกไปในไบต์จริง (ยืนยันด้วยการ re-derive จาก encoder แล้ว)
> แล้วทำไม attr ที่ผูกกับ actor ตัวนั้นบนไคลเอนต์ถึงเป็น `HP 0` ~~และชื่อว่าง~~?**

สองข้อนี้ **ขัดกันโดยยังไม่มีคำอธิบายที่วัดแล้ว** — และมันคือกุญแจของทั้ง `GT-036` และเลน nameplate/RE-067

### 🔴🔴 แก้ขอบเขต — **chief R169 (2026-08-25 ~21:0x +07:00) · ครึ่ง "ชื่อว่าง" ถูกตัดออกจากใบนี้**

**[MEASURED · client-observable · chief เปิดภาพเองรอบ R169]** ตัวหักล้างที่แข็งที่สุด **อยู่ในภาพควบคุมของ `GT-030-R3` เองมาตลอด** —
`evidence_screens/GT030R3_1159_TARGET_PANEL_CROP_t280.5s.png` แสดงสองแผงในเฟรมเดียว:
**ซ้าย = แผงของผู้เล่นเอง `HP. 100 /100` `LV. 1` — ไม่มีชื่อ** · ขวา = แผงเป้าหมาย `HP. 0` `LV. 1` — ไม่มีชื่อ

🎯 **แผงของผู้เล่นเองก็ไม่มีชื่อ** ทั้งที่ไคลเอนต์รู้ชื่อตัวละครแน่นอนและกำลังวาด `Arena01` ลอยกลางจอในเฟรมเดียวกัน
⇒ 🔴 **วิดเจ็ตนี้ไม่มีแถวชื่ออยู่เลย** ⇒ **"ชื่อว่าง" ไม่ใช่ข้อมูลเกี่ยวกับการ bind ชื่อของ actor ตัวใดทั้งสิ้น**
⇒ **ห้ามใช้ "ชื่อว่าง" เป็น input ของใบนี้** · ⇒ **ห้ามรายงานว่าใบนี้อธิบายชื่อได้ ไม่ว่าผลจะออกมาทางไหน**

🟢 **ใบนี้เหลือ claim เดียวที่สะอาด: `HP 0`** — ไม่ถูกกระทบจากการถอนครั้งนี้

🔴 **แต่ chief ถอนเหตุผลที่เคยให้ไว้ในฉบับแรกของ R169 (`pf-adversary` จับได้ ถูกแล้ว):**
~~"ตัวเทียบ `type 4` อ่าน `HP 100` ⇒ แผงแสดง HP ได้จริง ⇒ `HP 0` เป็นค่าที่ถูกแสดง ไม่ใช่ผลลบของ UI"~~
เฟรมเดียวของ `HP 100 / LV 1` **แยกไม่ออกระหว่าง "แผง bind HP จริง" กับ "แผงโชว์ค่า default 100"** — และ `100` ก็เป็นค่าที่เลนเราส่งพอดี
**[MEASURED · ตัวเทียบที่แข็งกว่ามาก และมีอยู่ในรีโปอยู่แล้ว — ใช้สองตัวนี้แทน:]**
- **`GT-035`** (`GAME_TEST_QUEUE.md:15,902`) — หลอด HP ของ `0x201F` ลงเป็นบันได **`3857 → 2893 → 2893 → 771`** · **สองรอบ สองผู้สังเกต**
- **`GT-032`** (`GAME_TEST_QUEUE.md:2409`) — target bar ของ `0x2001` อ่าน **`HP 100/100 Lv.1`**
⇒ **นี่ต่างหากคือหลักฐานว่าวิดเจ็ตติดตามค่า HP จริง** · เฟรมของรอบสี่ไม่ได้เพิ่มอะไรบนสองใบนี้เลย

🔴🔴 **และห้ามอ่านว่า `HP 0` ถูกยืนยันแล้วว่าเป็น "ค่าที่ถูกแสดง"** — **`T2` คือจ็อบที่ตัดสินข้อนี้ และมันยังไม่ถูกรัน**
ถ้า `T2` คืนค่า `+0x44 = 0` เป็น ctor default ⇒ `HP 0` ก็เป็นค่าเริ่มต้น **ไม่ใช่ความผิดปกติที่ต้องอธิบาย**
(จดหมายรอบสามยกข้อนี้ไว้เองแล้วเป็น **[เสนอ · ยังไม่ได้วัด]**) ⇒ **ห้ามให้หัวใบชี้นำหน้าสะพานว่า ctor ที่ไม่ใช่ศูนย์คือความผิดปกติ**

🔴 **ส่วน "อะไรตัดสินว่าแผงจะแสดงชื่อหรือไม่แสดงเลย"** เป็นคำถามใหม่ที่ **ยังไม่มีใบรองรับ** —
มันกว้างกว่าที่ `RE-067` (ปิดแล้ว) เคยตั้งไว้ ซึ่งไล่แค่ *"อะไรตัดสิน **สี**"* ⇒ **เขียนเป็นข้อเสนอถึงเจ้าของในจดหมาย R169 ไม่เปิดใบเอง**
(เหตุผลที่ไม่เปิดเอง: ใบ static เปิดอยู่แล้ว 1 ใบ และใบนี้เองยังไม่มีผล — เปิดใบที่สามซ้อนโดยไม่มีใครหน้าสะพานว่าง = คิวบวมโดยไม่มีคนรับ)

### 🆕 และรอบสี่ปลด nonclaim เรื่องกล้องของใบนี้ — **แต่ความกำกวมยังอยู่ แค่เปลี่ยนชนิด**

nonclaim ② ข้างบนบอกว่า *"ช่วง `t=222.4→267.4` กล้องคุมไม่ครบ ⇒ การตายอาจเกิดตั้งแต่ `MOVE_A_1`"*
รอบสี่ **คุมกล้องได้จริง** (`t=354→404` · เฟรมต่างกันสูงสุด 1.4% · จุด spawn อยู่ในกรอบตลอด) และวัดได้ว่า:
- **ไม่มี step change ที่ `MOVE_A_1` (`t=385.41`) เลย** — ไม่มีอะไรถูกวาดขึ้นมาทั้งสิ้น
- โมเดล **ปรากฏครั้งแรกพร้อมกับแอนิเมชันการตาย** ที่ `t=400.6` (`+0.2` วิหลัง `MOVE_A_2`) และฟุบราบที่ `401.3`

🔴🔴 **แก้โดย chief R169 หลัง `pf-adversary`: ข้อความข้างบนสองข้อยัง *อ่อนกว่าที่เขียน* และสาขาที่สามหายไป**

**ข้อแรก — "ไม่มี step change ที่ `MOVE_A_1`" ยังไม่ใช่ผลลบที่คุมได้** เพราะการ diff ที่ให้ตัวเลข 1.4% **ตาบอดต่อวัตถุขนาดโมเดลมนุษย์**
(โมเดล ~390 px เทียบเพดานสัญญาณรบกวน 3,120 px = ต่ำกว่า ~8 เท่า · เหตุการณ์ที่เกิดจริงสองอย่างในหน้าต่างเดียวกันก็ไม่ทำให้ค่าสูงสุดขยับ)
⇒ **ห้ามใช้ประโยค "ไม่มีอะไรถูกวาดที่ `MOVE_A_1`" เป็น input ของใบนี้** — มันคือ **"ไม่ถูกสังเกต"** เท่านั้น

**ข้อสอง — สาขาที่ต้องพิจารณามีอย่างน้อย *สี่* ไม่ใช่สอง:**

| สาขา | เนื้อหา | ผลต่อคำทำนายที่ commit ไว้ |
|---|---|---|
| **(ก)** | death chain ถูกทริกที่ `MOVE_A_2` (actor-entry ใบที่สาม) | **หักล้าง** คำทำนาย ① |
| **(ข)** | ถูกทริกที่ `MOVE_A_1` (ใบที่สอง) แล้ว **วาดไม่ออก**จนถึง `MOVE_A_2` | **ยืนยัน** คำทำนาย ① |
| 🆕 **(ค)** | **`MOVE_A_1` ไม่ถูกไคลเอนต์บริโภคเลย** (bind-gate ปฏิเสธ · mask handling · entry ถูกทิ้ง) ⇒ `MOVE_A_2` คือ **actor-entry ใบที่สองที่มีผลจริง** | **ยืนยัน** คำทำนาย ① — และเป็นสาขาที่ **คืนดี**ระหว่างสิ่งที่เห็นกับ static chain · 🎯 **ทดสอบ static ได้ถูกที่สุด — `T1`/`T3` ถามอยู่แล้วว่า entry ถูกบริโภคไหม** |
| 🆕 **(ง)** | **ร่างที่เห็นตายอาจไม่ใช่ `ProbePlayer01`** — `ProbePlayer02` อยู่ห่าง 150 หน่วย · ที่ระยะ ~1,100–1,400 หน่วยนั่นคือไม่กี่พิกเซล | nonclaim ③ ของ `GT-030-R3` ("ระบุจากตำแหน่งเท่านั้น") **ยังบังคับอยู่ ห้ามลืม** |

🔴 **และต้องบันทึกไว้ในผลด้วยว่าแต่ละสาขาทำอะไรกับคำทำนาย:**
คำทำนาย **③** (`[PROVEN]` · *"ต้องมี actor-entry อย่างน้อยสองใบของ identity เดิม"*) **ถูกสอดคล้องโดยทุกสาขา**
⇒ 🔴 **มันแยกสาขาไม่ได้ ⇒ ห้ามรายงานว่า "③ ถูกยืนยัน" ไม่ว่าใบนี้จะออกทางไหน** — นี่คือประเด็นทั้งหมดของการรันใบนี้

🔴 **ข้อสาม — "โมเดลปรากฏครั้งแรกพร้อมแอนิเมชันการตาย" เป็นข้อสังเกตของรอบสี่รอบเดียว**
รอบสามยืนยันให้ไม่ได้: ร่างถูกเห็นครั้งแรกที่ `t=278.0` = **`10.6` วินาทีหลัง `MOVE_A_2`** โดยไม่มีใครมองในช่วงนั้น
⇒ **ห้ามติดตั้งเป็น premise ของใบ** (ถ้าทำ = ทำผิดรูปเดียวกับข้อสรุปที่รอบนี้เพิ่งถอนไป)

### จ็อบ (ลำดับบังคับ · หยุดได้ทุกจุดถ้าชนเพดาน static — เขียน bounded negative แล้วปิด)

```
S0  ด่านคุม: image sha 9627211412ac60d5...b157028b623 · 14,759,424 B
    + rerun verifier ท่าเดียวกับ RE-068/RE-070 T0 (positive control 0x446F30 ต้องตรง GT-040)
S0b G7: VA->file offset ต้องแมปผ่าน PE section table รายเซกชัน
    (.text 0x400C00 · .rdata 0x401C00 · .data 0x402800) ห้ามใช้ delta เดียวข้ามเซกชัน

T1  0x446990 (spawn-not-found) + jump table 0x446B2C ช่อง index 2
    -> สาขา CNetActor ใช้ vtable slot ไหน apply attr (รายงานว่า +0x10) และมันวน attr list
       ของ entry จริงไหม  => ActorAttr/BasicAttr ของ SPAWN_BARE ถึง [actor+0x348] หรือไม่
T2  0x457340 CNetActor::ctor + bind site 0x4573CA
    -> ตอนสร้าง actor ผูก attr object ตัวไหน และ BasicAttr::ctor 0x464B0E เขียนอะไรลง
       +0x44 (current hp) / +0x48 (max hp) / +0x58 (timer)
    *** ปักค่า ctor default ของ +0x44 และ +0x48 ให้เป็นตัวเลข -- นี่คือจ็อบที่ชี้ขาดที่สุดของใบ ***
T3  0x469760 (bind thunk ActorAttr, gate CNetActor) -> ผ่านสำหรับ actor ที่เพิ่ง spawn ไหม
    และ 0x464F30 (CopyTo, vt+0x24) เขียนปลายทางเป็น [actor+0x348] จริงหรือเขียนที่อื่น
T4  0x4446F0 -> 0x4437C0 : อ่าน gate สองตัว
    bl         <- vt+0x40 = 0x454AC0 (HP==0 && timer>0)  คุม 0x44384C ([actor+0x70] |= 0x200)
    [esp+0x13] <- vt+0x3C = 0x454A70 (HP==0 && timer<=0) คุม 0x443990 -> 0x4439E9 -> 0x472810
    => ยืนยันว่า (HP==0, timer==0.0f) ตกสาขาไหน
T5  ผู้ผลิตข้อความลอย: หา call site ที่ฟอร์แมต MESSAGE row 414 (n_TYPE=2) หรือ
    MESSAGE_BATTLE row 14 (n_TYPE=3) แล้วดูว่ามันเอาอะไรใส่ $V1
    *** เส้นเดียวที่เชื่อ "ข้อความบนจอ" กับ "ฟิลด์ชื่อของ actor" ได้โดยตรง ***
    !! chief R169: T5 ยังทำได้ แต่ผลของมันเป็น "บริบท" เท่านั้น
       ห้ามให้ครึ่งชื่อของ T5 โผล่ในประโยคปิดใบ (ดูบล็อกแก้ขอบเขต) - ปิดใบด้วย $V1 เท่านั้น
    control: แถว 413/13 ($V1 บาดเจ็บล้มลง!) ต้องมาจาก producer เดียวกันคนละ id
T6  target panel 0x51F920 -> LABEL_NAME 0x5BD624 : ฟิลด์ไหนป้อนตัวเลข HP
    และตัวส่วน "/max" ถูกกดหายเมื่อ max==0 หรือไม่
    control: แผงผู้เล่นในเฟรมเดียวกันอ่าน "100 /100" (ภาพ sha 9048ad4f...)
T7  0x472850 / 0x4765C0 (สองที่ที่ push L"_F_DIE_000") -> ท่านอนมาจากตัวไหน
```

**เกณฑ์หยุด/ผลลบที่อ่านได้ทันที:** ถ้า **T2** พบว่า `BasicAttr` ctor เขียน `+0x44 = 0` **และ** **T1/T3** พบว่า attr ของ `SPAWN_BARE`
**ไม่**ถึง `[actor+0x348]` ⇒ อธิบายครบทั้ง `HP. 0` · ~~ชื่อว่าง~~ · `$V1` ว่าง · ท่านอน **โดยไม่ต้องมีสมมติฐานใหม่เลย** ⇒ ปิดใบได้
🔴 **แก้โดย chief R169 — "ชื่อว่าง" ถูกตัดออกจากเกณฑ์หยุดข้อนี้** ตามบล็อกแก้ขอบเขตข้างบน
**ห้ามเขียนคำว่า "ชื่อว่าง" ลงในประโยคปิดใบ** แม้เกณฑ์ที่เหลือจะครบทุกข้อ — มันไม่ใช่คำถามของใบนี้แล้ว
(เหตุ: แผงหลอด HP นี้ **ไม่มีแถวชื่ออยู่เลย** แม้แต่สำหรับตัวผู้เล่นเอง ⇒ ช่องชื่อว่างไม่ได้บอกอะไรเกี่ยวกับ actor ตัวไหนทั้งสิ้น)

### 🎁 ของที่ chief ทำให้เสร็จแล้วบนคลาวด์ — หน้าสะพานข้ามได้เลย

- **ไบต์ของ `MOVE_A_1`/`MOVE_A_2`/`SPAWN_BARE`** re-derive แล้ว hash ตรง pin ทั้งหมด (ไม่ต้องประกอบซ้ำ)
- **ตาราง bit→offset→tag ของ `MovementAttr`** ยืนยันตรงกันสามชั้นแล้ว
- **`gamedata` ค้นแล้ว:** `ตาย!` เป็น **template ที่มีช่องชื่อ** — `gamedata/tables/TEXTDATA_TH__MESSAGE_BATTLE.tsv:15` (`n_ID=14 · n_TYPE=3 · "$V1 ตาย!"`)
  และ `gamedata/tables/TEXTDATA_TH__MESSAGE.tsv:361` (`n_ID=414 · n_TYPE=2 · " $V1  ตาย!"`)
  🆕 แถวข้างบนของทั้งสองไฟล์เป็นข้อความคนละตัว: `$V1 บาดเจ็บล้มลง!` (id 13/413) = *downed*
  ⇒ **ไคลเอนต์แยก "ล้ม" กับ "ตาย" เป็นสองสตริง และผู้เทสเห็นตัวหลัง** ⇒ ใช้เป็น control ของ T5
- **อ่านภาพที่ commit แล้วเอง:** `evidence_screens/GT030R3_1159_DEAD_LABEL_TAI_t268.0s.jpg` — ข้อความลอยอ่านได้ **`ตาย!` เฉย ๆ ไม่มีชื่อนำหน้า**
  ⇒ `$V1` ถูกแทนด้วย **สตริงว่าง** ⇒ สอดคล้องกับ ctor default `name = L""` ที่ `PF_CHUNK2_Q1:29` ทำนายคู่กับ `HP=0` พอดี
- 🆕 **ของที่จดหมายยังไม่ได้จด:** `evidence_screens/GT030R3_1159_TARGET_PANEL_CROP_t280.5s.png` — แผงเป้าหมายอ่าน **`HP.  0` เดี่ยว ๆ ไม่มีตัวส่วน**
  ขณะที่แผงผู้เล่นในภาพเดียวกันอ่าน **`100 /100`** ⇒ น่าสงสัยว่า **max HP (`+0x48`) ก็เป็น 0 ด้วย** ไม่ใช่แค่ current
  ⚠️ **นี่เป็นการอ่านภาพ ไม่ใช่กฎการฟอร์แมตที่พิสูจน์แล้ว** — ใช้เป็นสมมติฐานของ T6 เท่านั้น

### 🔴 กับดักที่ต้องเขียนใส่หัวรายงาน (เจอจริงระหว่างเตรียมใบนี้)

`external/PF_SERIALIZER_FIELDS.tsv:12-13` เขียน `MovementAttr W/R = EMPTY` ที่ `0x0043BB80`
🔴 **ห้ามอ่านว่า "MovementAttr ไม่เขียนอะไรลงสาย"** — `0x0043BB80` เป็น **stub ร่วม** ที่ `AvatarAttr`/`BasicAttr`/`ActorAttr`/`NPCAttr`/`DBAttribute`/`MovementAttr`
ใช้ช่อง `serializer_va` ตัวเดียวกันหมด (`external/PF_PROTOCOL_REGISTRY.tsv:3-8`) · **Serial จริงคือ `0x4671C0`** (vtable `0xF0D0F8 +0x34` · span `0x4671C0..0x467288` sha `6A6571BB..180A`)
⇒ **การใช้กฎ 7 กับแถวนี้แบบตรง ๆ จะได้ false negative**

### กติกาบังคับ (เหมือนทุกใบ static)
ไม่เปิดเกม · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB · ไม่แก้ `src/`/คิว · ไม่ทำ git operation ·
อ่านอิมเมจ **read-only** พร้อม sha ก่อน/หลัง + 256-byte guards · **วิธี negative ต้องเป็น recursive CFG / census ไม่ใช่ linear disassembler** ·
ค้น `pf_bridge\external\` และ `pf_bridge\gamedata\` ก่อนเปิดงานขุด (🎁 chief ทำให้แล้วบางส่วน ดูบล็อกข้างบน)

### เกณฑ์จบใบ
ปิดได้เมื่อ **objective มีคำตอบ หรือมี bounded negative ที่เขียนขอบเขตครบ** ·
🔴 **ไม่ต้องรอให้เลนตายของ `GT-036` ถูกออกแบบก่อนจึงจะปิดใบนี้** — ใบนี้ตอบ *"actor เกิดมาพร้อมอะไร"* ส่วน *"เราจะยิงอะไรไปให้มันตาย"* เป็นใบถัดไป

### สิ่งที่ใบนี้ *ไม่* ทำ
ไม่ออกแบบ `HYP-PF-038` v2 · ไม่ตัดสินว่า `GT-036` ควรเดินหรือไม่ (เจ้าของอนุมัติไปแล้ว **chief ไม่มีสิทธิ์ถอน**) ·
ไม่แตะผลข้างเคียงข้อ ④ ของ `GT-030-R3` (NPC หายหลัง `SPAWN_BARE`) — **นั่นคือใบ `GT-072`**

### 🟢 หมายเหตุงบเวอร์ชัน (ตรวจแล้วในรอบ R168 ไม่ได้เชื่อคำบอก)
`HOSTILE_HP_LINK_HP_FLOOR = 0` (`src/pirateforce_foundation/hostile_hp_link_hypothesis.py:644`) และ
`HOSTILE_HP_LINK_LETHAL_STEP_LABELS = ()` (`:703`) ⇒ **ยังไม่มี `HYP-PF-038` v2 ที่ปล่อย HP ถึง 0 อยู่ในซอร์ส**
(ledger เขียนไว้เองว่า *"the GT-036 lethal exemption, which needs a HYP-PF-038 v2 that does not exist yet"* — `docs/HYPOTHESIS_LEDGER.json:13`)
⇒ 🎯 **ตอนนี้ยังไม่มีโค้ดใดต้องถอน และ scoped override ที่เจ้าของให้ ยังไม่ถูกใช้ไปแม้แต่บรรทัดเดียว** — การวัดก่อนสร้างจึงไม่มีต้นทุนจม

### 🟢 result — **DONE / STATIC-CONTRADICTION-PINNED** (ปิดโดย chief R170 · 2026-08-25 ~22:0x +07:00)

**ที่มา:** `notes_to_chief\consumed\20260825_2121_RE-071-RESULT-STATIC-CONTRADICTION-PINNED.md` · runner LOCAL · `2026-08-25T21:21+07:00`
**อิมเมจ:** `GameClient.local.bin` 14,759,424 B · `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
**วิธี:** PE section mapping รายเซกชัน + byte-exact guards + bounded/recursive CFG · 🟢 **ไม่ได้ใช้ linear disassembler เป็นหลักฐานของผลลบ** · guards `15/15` ผ่าน
**ช่องบังคับสองช่องทำครบ:** ค้น `pf_bridge\external\` แล้ว (เจอ `BasicAttr`/`ActorAttr`/`MovementAttr` ใน 3 TSV · `BasicAttr`/`ActorAttr` = `NOT_OBSERVED` · **และเจอกับดักตามใบว่า `0x0043BB80` เป็น stub ร่วม จึงไม่ใช้ EMPTY เป็นผลลบ**) · ค้น `gamedata` แล้ว (template คู่ควบคุมครบ: MESSAGE 413/414 · MESSAGE_BATTLE 13/14 · `_F_DIE_000`)

**คำตอบ T1–T7 (ย่อ — รายละเอียดและ span pins อยู่ในจดหมาย):**

| # | คำตอบ |
|---|---|
| T1 | `actor_type=2` → jump-table case `0x4469E1` → `CNetActor` · `init` เรียก attr-list loop `0x5DF080` ที่ `0x454949` เดินสมาชิกจริงจาก vector `[entry+0x30..+0x34)` ⇒ **`ActorAttr` ของ `SPAWN_BARE` ไม่ถูกข้ามโดย construction path** |
| T2 | ctor เก็บผล pool `0x1031500` ที่ `[actor+0x348]` · allocator `0x456D20` จอง `0x1C0` B แล้วเรียก `ActorAttr::ctor 0x464BE0` → chain `BasicAttr::ctor 0x464A80` ⇒ **ปิดป้าย INFERRED เดิมของ CHUNK2** · **ctor defaults ยืนยันจากไบต์:** name `L""` · `+0x44` HP `0` · `+0x48` maxHP `0` · `+0x58` timer `0.0f` · `+0x5E` level `1` |
| T3 | `ActorAttr` vtable `+0x38 = 0x469760` · `0x46978F` อ่าน `[actor+0x348]` · `0x469795` เรียก `incoming->CopyTo(resident)` (`0x464F30` → `BasicAttr::CopyTo 0x464B40`) ซึ่งก๊อป name `+0x28` และ HP `+0x44/+0x48` **โดยไม่ดู mask** |
| T4 | `HP==0 && timer<=0` → true (vt `+0x3C = 0x454A70`) ⇒ gate `0x443990` เปิด ⇒ `0x4439E9` สร้าง `CActorTask_Dead 0x472810` ⇒ **กลไกตายเมื่อ resident เป็น ctor-default ยืนยันแล้ว แต่ไม่อธิบายว่าทำไม incoming 100/100 ไม่ถูก CopyTo** |
| T5 | producer `ตาย!` `0x5CB830` (id `0x019E`/`0x032E`) และ downed `0x5CB9A0` (id `0x019D`/`0x032D`) **ส่ง GetName เป็น `$V1` ทั้งคู่** ⇒ **ข้อความไม่มีชื่อนำหน้า = GetName ว่างจริง ไม่ใช่ template ไม่มีช่องชื่อ** |
| T6 | target panel `0x51F150` อ่าน resident `+0x44`/`+0x48` · helper `0x5AA5E0` **บังคับ max=0 ให้เป็น 1** และ **ไม่มี branch ซ่อน denominator** ใน CFG เต็ม ⇒ 🔴 **`HP. 0` สนับสนุน current=0 แต่ "ไม่เห็น `/max`" ไม่พิสูจน์ max=0** — widget/layout/crop ยังเป็นตัวแปรเปิด |
| T7 | `CActorTask_Dead` vtable `0xF0F048` slots `+0x08 = 0x4765C0` และ `+0x0C = 0x472850` **push literal เดียวกัน `L"_F_DIE_000"`** ⇒ ภาพนิ่งแยกไม่ได้ว่าท่านอนมาจาก slot ไหน |

🎯 **คำตอบของใบ — static ให้คำตอบ *กลับด้าน* อย่างชี้ขาด:**
> actor ที่ถูกสร้างจาก `SPAWN_BARE` และรับ `ActorAttr` ที่มี name + HP `100/100` **สำเร็จ** ต้องมี resident name + HP `100/100`
> ⇒ name ว่าง/HP 0 คือ **ค่า fresh ctor** ซึ่งเกิดได้เมื่อ CopyTo ไม่ได้เขียนก้อนนั้น หรือมี actor/attr **คนละก้อน** หรือมีการเขียนทับภายหลัง

⇒ 🔴 **สิ่งที่ถูกหักล้างคือการเท่ากันโดยปริยายระหว่าง "ไบต์ `SPAWN_BARE` identity A ที่เซิร์ฟเวอร์ประกอบ" กับ "actor ที่ถูก target/นอนตายในภาพ"**
⇒ **จอ name ว่าง/HP 0 อธิบายเป็น "ผลปกติของ `ActorAttr` ใน `SPAWN_BARE` เดียวกัน" ไม่ได้อีกต่อไป**
⇒ จุดแยกที่เหลือ **ต้องวัด runtime identity/slot/wire** — static จากอิมเมจใบนี้ **ไปต่อไม่ได้โดยไม่เดา**

**nonclaims ที่ติดมากับผล (ยกมาทั้งดุ้น ห้ามตัด):** ① ไม่พิสูจน์ว่า actor ในภาพคือ identity A — ตรงกันด้านตำแหน่ง/เวลา **ไม่ใช่ identity crosswalk** ② ไม่พิสูจน์ว่า wire ที่ client รับตรงกับไบต์ที่ encoder ฝั่งเรา re-derive (รอบนี้ไม่เปิด capture ไม่เปิดเกม) ③ **ไม่ exclude การ overwrite resident `ActorAttr` ภายหลังจากเส้นอื่น** ที่ไม่อยู่ใน actor-entry list ของห้าเฟรมนี้ ④ ไม่ตัดสิน `GT-036` ไม่ออกแบบ `HYP-PF-038` v2 ไม่แตะ `GT-072` ⑤ เป็นกฎของ **shipped client image ใบนี้** ไม่ใช่กฎของ original server

🔴 **หมายเหตุที่ chief ต้องส่งต่อ ไม่ใช่กลบ:** `tools/pf_runtimeres_actor_entry_static.py --json` **exit 1** ในรอบนี้ — binary controls (รวม `0x446F30`) ตรงหมด แต่ **source-census รุ่นเก่าคาดจำนวน call/module ก่อนงานใหม่ใน `src/`** ⇒ **ไม่ใช่ binary mismatch แต่เป็นเครื่องมือที่ค้างรุ่น** ⇒ ใบสั่งซ่อมอยู่ในจดหมาย `FROM_CHIEF_R170_*`
🔴 **read-only integrity:** before ตรงทั้ง image sha/size/guards · `external` tree 30 files `cad40e79...` · `gamedata` tree 1,109 files `a3d01a9f...` · **บรรทัด `AFTER` ใน `logs/re_runner.log` ต้อง IDENTICAL — chief ตรวจจากคลาวด์ไม่ได้ ผู้รันยืนยันแล้วว่าตรวจก่อนปล่อย lock**

---

## 🆕🔬 RE-073 TEST-STAGE-GEOMETRY-SURVEY-001 [STATIC-ON-BRIDGE]: **สามฉากที่ addressable และน่าจะโล่ง — วัดเรขาคณิตจริงว่าฉากไหนใช้เป็น "เวทีเทสโมเดล" ได้**  [🟢 **OPEN — เปิดโดย chief R169 · 2026-08-25 ~21:0x (+07:00)**]

> 🔢 **หมายเหตุเลข:** ตัวนับเป็นชุดเดียวกับ `GAME_TEST_QUEUE.md` **ห้ามแยกตัวนับ** · grep `GT-073`/`RE-073` ทั้งสองไฟล์ = 0 hit ⇒ **073 ว่างจริง** ⇒ ใบถัดไปเริ่มที่ **074**

### ที่มา — **คำขอของเจ้าของโดยตรง**

คุณ Panya 2026-08-25 ~20:1x (+07:00) — จดหมาย `notes_to_chief\consumed\20260825_2020_PANYA-REQUEST-a-real-test-stage-*.md`:
> *"ฉันว่าที่ตรงนี้มันดูลำบากสำหรับงานเทสพฤติกรรมโมเดลและ spawn object ไหนจะถังบัง ลานก็แคบเพราะเป็นท่าเรือ
> แล้วไม่รู้อีกว่าถ้ามีอะไรไปเกิดตรงจุดที่เป็นน้ำจะเป็นยังไง ฉันอยากได้แมพที่เป็นแมพเทสโมเดลจริง ๆ กว้าง สีขาวล้วน พื้นเรียบ ไม่มีเอฟเฟกใด ๆ"*

**เธอพูดถูก และมีหลักฐานจากคืนเดียวกัน:** `GT-045` ป้ายชื่อโผล่ 0.3 วิท่ามกลางถัง/ลัง/ตัวเรือที่กินครึ่งจอ ·
`GT-030` รอบสามผู้เทสต้องเดินหาศพเพราะกล้องถูกบัง · `GT-030` รอบสี่ **ตัวคุม `ProbeControl03` ที่ `-9,290` ยืนยันไม่ได้สองรอบติด**
เพราะภูมิประเทศบังคับให้ผู้เทสอยู่ผิดด้าน ⇒ **เวทีที่แย่ทำให้ทุกใบแพงขึ้น และทำให้ผลลบอ่านไม่ขาดซ้ำ ๆ**

### 🔴🔴 อ่านก่อนอย่างอื่น — **ผมวัดครึ่งแรกจบแล้วบนคลาวด์ และมันแก้จดหมายต้นเรื่องสามข้อ**

`pf-static-re` เดิน crosswalk ระหว่าง **289 โฟลเดอร์** ใน `gamedata\scene\` กับ **271 แถว** ใน
`gamedata\tables\CONSTDATA_TH__SCENE_NAME.tsv` (จับคู่ด้วย `s_MODLE_ID` · case-insensitive · **ไม่มีคีย์อื่นในตารางทั้งชุด**)

🔴 **สามข้อที่จดหมายต้นเรื่องเสนอไว้ และวัดแล้วว่า *ใช้ไม่ได้*:**

1. 🔴 **แมพเทสของนักพัฒนาทั้ง 18 ตัว ไม่มี `n_ID` เลยสักตัว ⇒ ส่งไคลเอนต์ไปด้วย table-driven teleport ไม่ได้**
   (`AirTest` `AirTest01` `AirTest02` `AitTest03`(sic) `AlbertTest` `GVGTEST` `GVGTEST01` `InstanceTest` `MobTest`
   `NoviceTest` `PlayerViewer` `Prototype` `SailingTest` `Seatest` `TenYooScene` `dupliacte_clear`(sic) `duplicate` `trigger_test`)
   grep ชื่อทั้ง 18 ทั่ว `gamedata\tables\` = **0 hit** · **control ผ่าน** (grep `Bg1177` และ `FilmScene` ด้วยวิธีเดียวกัน = เจอถูกไฟล์)
   ⇒ **`PlayerViewer` ที่จดหมายชี้เป็นเป้าหลัก คือเป้าที่ส่งไปไม่ได้** — นี่คือเหตุผลที่ใบนี้ไม่ไล่ตามมัน
2. 🔴 **`s_IMAGENAME = BgNull` ไม่ใช่สัญญาณอะไรเลย — มัน 237 จาก 271 แถว (87.5%)**
   34 แถวที่ *ไม่ใช่* `BgNull` คือเมืองหลักที่มีภาพมินิแมพวาดมือ (`Bg####_air`) ⇒ **ฟิลด์นี้ index งานศิลป์มินิแมพ ไม่ได้บอกเนื้อฉาก**
   ⇒ 🔴 **"BgNull = ห้องขาวโล่ง" ตายแล้ว ห้ามใช้ต่อทุกที่**
3. 🔴 **ชื่อ `สนามฟุตบอลชายหาด(TEST)` ไม่ใช่ค่าในฟิลด์** — ค่าจริงในตารางเป็น **จีนตัวเต็ม `沙灘足球場(TEST)`** (`CONSTDATA_TH__SCENE_NAME.tsv:253`)
   ส่วนชื่อไทย/อังกฤษอยู่คนละไฟล์ (`TEXTDATA_TH__SCENE_NAME_TIP.tsv` n_ID 278 = `Beach Soccer Field`)
   และ **`Bg1177` มี 9 placements ซึ่งเป็น mob-spawn set ทั้งหมด** ⇒ **ไม่ใช่ฉากว่าง** ⇒ **ใบนี้ตัด `Bg1177` ออกจากตัวเลือก**

🟢 **สิ่งที่ครึ่งแรกได้มาแทน — ผู้สมัครสามตัวที่ addressable จริง (มี `n_ID` ในตารางที่ ship มา):**

| อันดับ | `n_ID` | code | ชื่อในตาราง | placements | config |
|---|---|---|---|---|---|
| **1** | **997** | `FilmScene` | **純色拍攝景** = *"ฉากถ่ายทำสีล้วน"* | **0** (definitions 0 · `.npc` 6 ไบต์ว่าง) | `TYPE=2` · `CANGLIDE=1` · `CANRIDE=1` · `LIMIT_HEIGHT=30000` — **เหมือน `BG0001` ท่าเรือทุกช่อง** |
| **2** | **291** | `Bg1181` | `3V3競技場` (สนามแข่ง 3V3) | **0** (definitions 5 · ไม่ถูกวาง) | `TYPE=256` `SUBTYPE=2` (**ค่าไม่ซ้ำใครในตาราง**) · `CANGLIDE=0` `CANRIDE=0` `LIMIT_HEIGHT=0` |
| **3** | **328** | `Bg2033` | `GM活動景` (ฉากงาน GM) | **0** (definitions **26** ⇒ มี prop palette ที่คนตั้งใจจะใช้) | `TYPE=2` · `CANGLIDE=1` · `CANRIDE=1` · `LIMIT_HEIGHT=30000` |

🎯 **`FilmScene` คือตัวที่น่าสนใจที่สุด และไม่มีอยู่ในจดหมายต้นเรื่องเลย** — ชื่อมันแปลว่า *"ฉากถ่ายทำสีล้วน"* ตรงกับคำขอของเจ้าของเป๊ะ
🔴 **แต่มันมีธงแดงที่ต้องเคลียร์ก่อน:** มันเป็น **แถวเดียวในตารางที่ `s_HK/TC/JP/TH_VER` เป็น `0.00.0000` ครบทั้งสี่ช่อง**
(แถวอื่นเป็นเวอร์ชันจริงหรือคำว่า `OUT`) · เป็น `s_MODLE_ID` เดียวที่ไม่ใช่รูป `Bg####` · และ `n_ID 997` อยู่นอกช่วง `1..328` ของทุกแถว
⇒ **`0.00.0000` แปลว่า "มีมาตั้งแต่ v0 ใช้ได้ตลอด" หรือ "ไม่เคย ship" — ตัดสินจากไฟล์ใด ๆ บนคลาวด์ไม่ได้ และนี่คือความเสี่ยงอันดับหนึ่งของใบ**

### objective (claim เดียว)

> **ในสามฉาก `FilmScene` (997) · `Bg1181` (291) · `Bg2033` (328) — ฉากไหน (ถ้ามี) มีพื้นราบต่อเนื่องกว้างพอ ไม่มีวัตถุบดบัง ไม่มีน้ำ ไม่มีเอฟเฟกต์
> พอจะใช้เป็นเวทีเทสโมเดลถาวรได้ — และพิกัดจุดยืนที่แนะนำคือเท่าไหร่**

### จ็อบ (ลำดับบังคับ · หยุดได้ทุกจุด เขียน bounded negative แล้วปิด)

- **T0 — ด่านควบคุมก่อนเสมอ:** verify image sha `9627211412ac60d5…b157028b623` · `14,759,424 B` เหมือนทุกใบ static
  · **ช่องบังคับสองช่องของไฟล์นี้:** `ค้นใน pf_bridge\external\ แล้ว: เจอ <อะไร> / ไม่เจอ` และ `ค้น gamedata แล้ว: เจอ <อะไร> / ไม่เจอ`
  🔴 **ครึ่ง `gamedata` ผมทำให้แล้วข้างบน — อย่าทำซ้ำ** ให้กรอกว่า *"chief R169 ทำแล้ว ผล = crosswalk ข้างบน"* แล้วข้ามไป T1
- **T1 — เปิดโฟลเดอร์ฉากบนดิสก์ไคลเอนต์** `Data\Scene\Save\FilmScene\` แล้วรายงาน **ทุกไฟล์ที่มี พร้อมขนาด**
  🔴 **ข้อนี้สำคัญที่สุดในใบ และตอบได้เร็วที่สุด** — คลาวด์รู้แค่ว่ามี `.npc` เพราะตัวถอดของเราถอดแค่นั้น
  **เราไม่รู้ด้วยซ้ำว่านามสกุลของไฟล์ terrain คืออะไร** ⇒ ถ้า T1 พบว่าโฟลเดอร์มีแต่ `.npc` ว่าง 6 ไบต์ **นั่นคือคำตอบเชิงบวกที่แรงมาก** (ฉากไม่มีเรขาคณิตเลย)
  และถ้ามีไฟล์อื่น ⇒ รายงานชื่อ+ขนาด **ก่อน** พยายาม parse อะไรทั้งสิ้น
- **T2** ทำ T1 ซ้ำกับ `Bg1181` และ `Bg2033` · และ **ทำกับ `bg0001` (ท่าเรือ) ด้วยเป็น positive control** — เรารู้ว่าท่าเรือมีภูมิประเทศจริง
  ⇒ **ขนาด/จำนวนไฟล์ของท่าเรือคือมาตรวัดว่า "ฉากที่มีของจริง" หน้าตาเป็นยังไง** ⇒ เทียบแล้วอ่านสามฉากแรกออกทันทีโดยไม่ต้อง parse
- **T3** ตัดสิน `s_TH_VER = 0.00.0000` ของ `n_ID 997` ให้ได้ — ค้นในไคลเอนต์ว่ามีที่ไหนอ่านคอลัมน์เวอร์ชันของตารางฉาก และทำอะไรกับค่านั้น
  🔴 **ถ้า T3 ตอบว่า "ไม่เคย ship" ⇒ `FilmScene` ตกทันที และ `Bg1181` (291) ขึ้นเป็นตัวนำด้วยเวอร์ชันสแตมป์ปกติ** (`1.11.0000` HK · `1.07.0000` TH)
- **T4** ถ้า T1/T2 ให้ไฟล์ terrain มา: extent ของพื้นที่ราบต่อเนื่อง · มีน้ำไหม · วัตถุ static mesh กี่ชิ้น · แล้วเสนอ **พิกัดจุดยืนหนึ่งจุดต่อฉาก**
- **T5** (ถ้าเหลือแรง) `n_SCENE_TYPE` `2` / `4` / `16` / `256` gate การเข้าฉากหรือไม่ — โดยเฉพาะ `256` ของ `Bg1181` ที่อาจต้องผ่านระบบ PvP ไม่ใช่ teleport เปล่า

### 🔴🔴 ด่านที่ใหญ่กว่าเรขาคณิต — **เซิร์ฟเวอร์ของเราส่งไปฉากอื่นไม่ได้เลยตอนนี้ (chief วัดเองบนคลาวด์ R169)**

**ก่อนใครจะไปวัดพื้นราบ ให้รู้ก่อนว่าถึงเจอฉากที่สมบูรณ์แบบ เราก็ยังส่งไคลเอนต์ไปไม่ได้** — `scene_id` ถูกตรึงไว้ที่ **1 หรือ 2 เท่านั้น** ที่ **สามชั้นอิสระ**:

| ชั้น | ไฟล์:บรรทัด | การ์ด (ยกมาตรง ๆ) |
|---|---|---|
| player ActorAttr | `src/pirateforce_foundation/player_wire.py:65` | `if basic_faction != 1 or scene_seq != 0 or scene_id not in (1, 2): raise ValueError(...)` |
| NPC BasicAttr | `src/pirateforce_foundation/npc_wire.py:27` | `scene_id != 1` ⇒ `raise ValueError("the diagnostic serializer accepts only the complete proven P30 profile")` |
| scenario loader | `src/pirateforce_foundation/scene_load.py:117,122` | `expected_scene = 1 if (scene007 or eagle) else 2` แล้ว reject ถ้า `entry["scene_id"] != expected_scene` |

🟢 **นี่ไม่ใช่บั๊ก — เป็น fail-closed ตามแพตเทิร์นบ้าน** (serializer รับเฉพาะโปรไฟล์ที่พิสูจน์แล้ว) และการ์ดพวกนี้ถูกต้องที่มีอยู่
🔴 **แต่มันแปลว่า "ไปฉาก 997" ไม่ใช่การหยิบใช้ของที่มีอยู่ — มันคือ *ความสามารถใหม่* ที่ต้องมีเวอร์ชันใหม่ของเลน**
⇒ **กินสล็อตเวอร์ชัน · แตะโค้ดที่ผูกกับ `HYP-PF-001` ที่ frozen · ⇒ ต้องให้เจ้าของเคาะก่อน ไม่ใช่งานที่ pre-approved**
⇒ 🔴 **ห้ามใครเปิดใบลูกที่ "ลองส่ง scene_id 997 ดู" โดยไม่มีคำเคาะ** — เขียนเป็นคำถามถึงเจ้าของในจดหมาย R169 แล้ว

**ผลต่อการจัดลำดับของใบนี้:** T1/T2 (เปิดโฟลเดอร์ฉาก ดูว่ามีไฟล์อะไรบ้าง) **ยังคุ้มและยังควรทำก่อน** เพราะมันถูก เร็ว
และถ้าคำตอบคือ *"ทั้งสามฉากมีภูมิประเทศเต็มไปหมด ไม่มีห้องขาวสักฉาก"* ⇒ **เรื่องทั้งเรื่องจบตรงนั้น โดยไม่ต้องจ่ายค่าสล็อตเวอร์ชันเลย**
⇒ 🎯 **นี่คือเหตุผลที่ใบนี้ยังเปิด แม้ด่านฝั่งเซิร์ฟเวอร์จะยังไม่ปลด — มันเป็นด่านที่ถูกที่สุดและตัดตัวเลือกได้มากที่สุด**

### 🔴 สิ่งที่ใบนี้ **ไม่** ทำ และห้ามใครอ่านว่ามันทำ

- **ไม่ตอบว่าเซิร์ฟเวอร์ของเราส่งไคลเอนต์ไปฉากอื่นได้จริงไหม** — วัดแล้วว่า **ตอนนี้ไม่ได้** (ตารางข้างบน) · ส่วน *"แก้ให้ได้ต้องทำอะไรบ้าง"* เป็นงานออกแบบที่รอคำเคาะเจ้าของ
- **ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**
- **ไม่ตัดสินว่าฉากไหน "สวย" หรือ "เหมาะ"** — เกณฑ์สุดท้ายเป็นตาของเจ้าของ ใบนี้แค่ตัดตัวเลือกที่วัดแล้วว่าใช้ไม่ได้ทิ้ง

### 🔴 nonclaims ที่ต้องติดไปกับผลทุกกรณี

① **`0 placements` ไม่เท่ากับ "ฉากว่าง"** — `.placements.tsv` ถอดเฉพาะรายการวาง object ใน `.npc` เท่านั้น
   **ไม่ได้บอกอะไรเลยเรื่องพื้น ภูมิประเทศ static mesh หรือน้ำ** · `FilmScene` เป็นได้ทั้งห้องว่างสีล้วนและหน้าผาเต็มลูก — คลาวด์แยกไม่ออก
② **"addressable" = "มี `n_ID` ในตารางที่ ship มา" เท่านั้น** — **ไม่ได้แปลว่าเซิร์ฟเวอร์หรือไคลเอนต์จะยอมให้เข้า**
③ **63 โฟลเดอร์ที่ไม่มีแถว พิสูจน์แล้วว่าไม่อยู่ใน `gamedata\tables\`** (control-validated) — **แต่ไม่ได้พิสูจน์ว่าเข้าไม่ได้** code path หรือตารางที่เรายังไม่ได้ถอดอาจอ้างถึงมันได้
④ **grep ใน `gamedata\lua\` อ่านไม่ได้ทั้งสองทาง** — control (`Bg0001` ใน `lua/`) ก็ 0 hit ⇒ คลัง Lua ที่ถอดมาไม่ได้เอ่ยชื่อ code ฉากเลย **ห้ามอ่าน non-hit ของ Lua เป็นหลักฐาน**
⑤ **45 จาก 271 แถวเป็น alias** — ใช้ `s_MODLE_ID` ซ้ำกับแถวอื่น (เช่น `n_ID 17` และ `n_ID 186` ต่างชี้ `Bg1001`)
   ⇒ **`n_ID` คือที่อยู่ · ไฟล์แมพใช้ร่วมกันได้** ⇒ ห้ามอนุมานว่า "หนึ่ง n_ID = หนึ่งฉากจริง"

### ⚠️ กับดักเครื่องมือที่เจอระหว่างทาง (ยังไม่มีใครเหยียบ — จดไว้กันรอบหน้าเหยียบ)

`scene\<Name>\` มีไฟล์เดียวเสมอ **แต่ basename ไม่ได้เท่ากับ `<Name>` เสมอไป** — สี่ฉากไม่ตรง:
`Bg0003\bg0003` · `Bg0009\bg0009` · `FilmScene\filmscene` · `bg0020\Bg0020`
(ตัวถอดใช้ `path.stem` ของไฟล์ `.npc` ต้นทาง — `gamedata\pf_decode_lua_npc.py:605`)
🔴 **สคริปต์ไหนที่ glob `<Name>\<Name>.placements.tsv` จะพลาดสี่ฉากนี้เงียบ ๆ — และ `FilmScene` คือหนึ่งในนั้น** ⇒ ใช้ `<Name>\*.placements.tsv` เสมอ
🟢 **ตรวจแล้วว่ายังไม่มีผู้บริโภคตัวไหนพัง** — grep `placements` ทั้งสองรีโป: ผู้ใช้เดียวคือตัวถอดเอง ส่วนฝั่งเซิร์ฟเวอร์อ่าน placement จากตาราง v141 ไม่ใช่จาก TSV ⇒ **เป็นกับดักที่ยังไม่ระเบิด ไม่ใช่บั๊กที่ต้องแก้ตอนนี้**

### result (ยังไม่มี — ใบเปิดอยู่ · ครึ่ง crosswalk ถูกกรอกจากคลาวด์แล้วในหัวใบ)

---

## 🆕🔬 RE-075 RETURNSELECT-APPLY-0x5F1190-WHAT-DOES-IT-DO-001 [STATIC-ON-BRIDGE]: apply ของ `ReturnSelectServerVital 0x709E` ที่ VA `0x005F1190` **ทำอะไรจริง** เมื่อเฟรมมาถึง และทำอะไรเมื่อ live state ไม่ใช่ `cStateCreateActor`  [🟢 **OPEN — เปิดโดย chief R170 · 2026-08-25 ~22:2x (+07:00)** · ร่างใบโดย `pf-static-re`]

> 🔢 **หมายเหตุเลข:** ตัวนับชุดเดียวกับ `GAME_TEST_QUEUE.md` **ห้ามแยกตัวนับ** · **073 ถูกจองโดย `RE-073`** (R169) และ **074 ถูกจองโดย `GT-074`** (ใบเก็บตกมุมกล้องของ `GT-072` · รอบเดียวกันนี้) ⇒ **ใบนี้คือ `RE-075`** · **เลขว่างถัดไป = 076**
> 🔴 ร่างของลูกมือเขียนเลขเป็น `RE-074` เพราะ grep ตอนที่ `GT-074` ยังไม่ถูกวาง — **chief แก้เป็น `RE-075` ตอนวาง** ถ้าเจอ `RE-074` ที่ไหน นั่นคือใบนี้

### ที่มา — คำเคาะเจ้าของโดยตรง
คุณ Panya 2026-08-25 ~21:10 (+07:00) จดหมาย `notes_to_chief\consumed\20260825_2110_PANYA-RULINGS-FIVE-plus-GT001-heading-finding-and-a-criterion-defect.md` ข้อ 2:
ทางเลือก (ก) เติม `evidence_gap` ของ `HYP-PF-028` แล้วเดินต่อ vs (ข) เปิดใบ static ถาม `0x005F1190` ก่อน
⇒ **เจ้าของเคาะ (ข)** · ใบนี้คือใบนั้น · **สถานะของ `HYP-PF-028` ห้ามขยับจนกว่าใบนี้จะมีผล**

### อ่านก่อนอย่างอื่น — ครึ่งหนึ่งของคำถามมีคำตอบที่ commit ไว้แล้ว อย่าขุดซ้ำ
`[STATIC]` `reports\PF_UI_REFRESH001_CHARACTER_SELECT_STATE_MACHINE_STATIC_20260819.md` (รีโปเซิร์ฟเวอร์) พินไว้ตั้งแต่ 2026-08-19 ว่า:
1. `0x5F1190` = **inbound apply ของ `ReturnSelectServerVital`** อ่านจาก vtable `0xF304DC` slot `+0x1C`
   (`+0x10` = id getter `0x5E6960` · `+0x18` = serializer `0x5E69F0`) — ทั้งสามข้อมี guard ใน `tools\pf_ui_state_refresh_static.py`
2. มันเป็น 1 ใน **ห้า** vital ที่ apply มี gate "live state เป็น `cStateCreateActor`" — call site ของ token getter `0x4C0110` อยู่ที่ `0x5F11AC`
   (getter มี **8** call site เป๊ะ: `0x4E61D4, 0x510D45, 0x5D118B, 0x5EFD88, 0x5EFDDC, 0x5EFECC, 0x5F11AC, 0x5F334B`)
3. `CState::RequestNext 0x4C7320` มี **18** call site แจกแจงครบทีละบรรทัด (`:140-158`) — **ไม่มีจุดไหนอยู่ใน `0x5F1190`**
4. **รายงานเขียน nonclaim ของตัวเองไว้ที่ `:237`**: *"Not decoded: ... ReturnSelectServerVital 0x5F1190 ... bodies. They are pinned by address and by state gate, not analysed."*
⇒ **นั่นคือช่องว่างที่ใบนี้ปิด และมีแค่ช่องนั้น**

`[MEASURED — ลูกมือ `pf-static-re` re-derive จากตารางเอง ไม่ได้ quote]` **สองข้อที่แก้ถ้อยคำของ R168 (chief รับทั้งสองข้อ):**
- คอลัมน์ `handler_va` ใน `external\PF_PROTOCOL_REGISTRY.tsv` **เท่ากับ `vtable + 0x1C` แบบกลไกใน 502/502 แถวที่ parse ได้** (`serializer_va` = `vtable + 0x18` เช่นกัน)
  ⇒ มันคือ **"ค่าใน vtable slot"** ไม่ใช่หลักฐานว่ามี dispatch เข้ามาจริง หรือมี producer
- `0x005F1190` ปรากฏแถวเดียวจริง **แต่ uniqueness ไม่ใช่สัญญาณพิเศษ**: นับทั้ง 519 แถว (รวม `UNKNOWN` เป็นหนึ่งค่า) ได้ distinct `handler_va` = **194** และ unique = **162** · 🔴 **นับเฉพาะ 502 แถวที่ parse เป็นเลขได้ — ซึ่งเป็นฐานเดียวกับประโยคก่อนหน้า — ได้ `191 / 160`** (`pf-adversary` จับความไม่ตรงของตัวหารนี้ · ข้อสรุปไม่เปลี่ยน ~31–32% ของ handler ก็ unique เหมือนกัน) · ค่าที่แชร์มากสุดคือ `0x00710440` (69 แถว) ซึ่งคือ no-op `mov al,1; ret 4`
  ⇒ สิ่งที่แข็งจริงมีข้อเดียว: **`0x005F1190` ไม่ใช่ no-op `0x710440`**

### objective (claim เดียว)

> **`0x005F1190` ทำอะไรกับสถานะของไคลเอนต์เมื่อเฟรม `0x709E` ถูกบริโภค — และเมื่อ live state ไม่ใช่ `cStateCreateActor` (ซึ่งคือสภาพของทั้ง `GT-033` variant B และ C) มันตกสาขาไหน**

ตอบให้ได้แค่นี้ก็พอ · chief จะเอาไปเคาะสถานะของ `HYP-PF-028` ต่อเอง

### ช่องบังคับก่อนขุด (กฎบ้าน สองช่อง กรอกในผลเสมอ)
- `ค้นใน pf_bridge\external\ แล้ว: เจอ <อะไร> / ไม่เจอ`
  **[chief R170 ทำครึ่งนี้แล้ว อย่าทำซ้ำ]** `PF_PROTOCOL_REGISTRY.tsv:73` (VA ครบชุด) · `PF_SERIALIZER_FIELDS.tsv:1123-1128`
  (W: `0x08@+0x14 len1` · `0x32@+0x18 len8` · `UNTAGGED_STRING8_LEN32LE@+0x20` · R: สามฟิลด์เดียวกัน · span `0x005E69F0..0x005E6AE7`
  sha `1fd3684282291e2accb94171f0d532e239d38f736e1cb1455a633e7ad567774a`) — **กฎ 7 ผ่าน ไม่ใช่ EMPTY stub** ·
  `PF_FIELD_VALIDATION.tsv:144-145` (`W observed 2 VALIDATED` · `R observed 0 NOT_OBSERVED`) · `PF_PROTOCOL_PRIORITY.tsv:73` (`CLOSED`)
- `ค้น gamedata แล้ว: เจอ <อะไร> / ไม่เจอ` — ใบนี้ไม่ใช่คำถามข้อมูลเกม กรอกว่า "ไม่เกี่ยว" ได้ถ้าค้นแล้วไม่มี

### S0 ด่านคุม (ทำก่อนเสมอ · ล้มที่ด่านไหนให้หยุดและรายงาน)

```
S0a  image sha 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
     size 14,759,424 B - check sha before AND after (read-only), both must match
S0b  G7: VA -> file offset must map through the PE section table per section
     (.text 0x400C00 | .rdata 0x401C00 | .data 0x402800) - never one delta across sections
     control for this ticket: 0x005F1190 - 0x400C00 = file offset 0x001F0590
     DO NOT trust that number from this ticket - read the section table from the image
     (note: factpack_L1\pe_sections.tsv referenced by MANIFEST is NOT in VCS)
S0c  256-byte guards from factpack_L1\blocks_256.tsv (already committed, use as-is):
       block 7940  file_offset 0x001F0400  sha e10cc48248fc2fa0982981018740535ee35ab60be908ca20211980c3d550b123
       block 7941  file_offset 0x001F0500  sha e24b47d6ca8ed4d701bc69232a0bb33e862f2ce5ffa165e6b892f5b4488732ff
     (0x001F0590 falls inside block 7941) - must match before reading any byte
S0d  positive control, the most on-target one the project owns:
       pirate-force-server\tools\pf_ui_state_refresh_static.py   (stdlib only, exit 0 = PASS)
     it checks vtable 0xF304DC +0x1C == 0x5F1190 and the 8 call sites of 0x4C0110 directly
     if it does NOT pass => image or tooling is off, STOP, report no T results
S0e  negative results must come from recursive CFG / census, NOT a linear disassembler
     (lesson: RE-068 T1)
```

### จ็อบ (ลำดับบังคับ · หยุดได้ทุกจุด เขียน bounded negative แล้วปิด)

```
T1  disassemble 0x005F1190 as a complete function
    -> span [start,end) | file offset | len | instr count | recursive CFG error count | gaps | indirect count | sha256 of span
    -> report the first mnemonic (control: it must NOT be B0 01 C2 04 00, the no-op at 0x710440)

T2  the gate at 0x5F11AC (call to token getter 0x4C0110)
    -> shape of the gate: read live state from [0x1093198]+0x34C then is-a via 0x88F2B0, or another shape
    -> **WHAT THE FALSE BRANCH DOES** (bare ret / ret 4 / writes something first / jumps where)
    *** this is the decisive job of the ticket: GT-033 variant B and C both ran while the client
        was in the map, which is NOT cStateCreateActor ***

T3  the true branch - answer as a list of measurable side effects only:
    -> which vital fields it reads (+0x14 u8 / +0x18 8-byte / +0x20 string per PF_SERIALIZER_FIELDS)
       and **which value it branches on** - if it branches on a field our lane sends as all-zero,
       that is the biggest answer this ticket can produce
    -> writes page variable 0x107A2C0? | calls which cStateCreateActor method? |
       touches [0x1093198]+0x34C? | opens/closes which UI window (the L"..." literal pushed)?

T4  reachability from 0x005F1190 to CState::RequestNext 0x4C7320 - RECURSIVE, not just direct
    base: PF_UI_REFRESH001 pins all 18 direct call sites of 0x4C7320 and none is inside 0x5F1190
    but the same report shows an apply CAN reach it through a helper (0x4323FA lives in helper 0x432290)
    -> answer "reaches / does not reach" with the graph, the depth, and how many indirects were unresolved
    control: walk the same way from TeleportVital apply 0x5F14B0 - it must find 0x5F16C9 -> 0x4C7320
             (a positive control whose answer is known in advance)

T5  (if budget remains) caller census of 0x005F1190
    -> any entry other than the indirect through vtable 0xF304DC +0x1C?
    -> confirm ON THE IMAGE that the dword at 0xF304F8 (= 0xF304DC + 0x1C) really holds 0x005F1190
```

### อะไรนับเป็นผลลบ (และผลลบข้อไหนมีค่าที่สุด)
- 🎯 **ผลลบที่มีค่าที่สุด:** `T2` พบว่าเมื่อ live state ไม่ใช่ `cStateCreateActor` ฟังก์ชัน **return โดยไม่ทำอะไร** และ `T4` เดินไม่ถึง `0x4C7320`
  ⇒ อธิบายผลลบของ `GT-033` variant B และ C **ได้ครบโดยไม่ต้องมีสมมติฐานใหม่** และตอบคำถามของ R168 ว่า `0x005F1190` **เป็น apply จริง (ไม่ใช่ artifact) แต่ไม่มีอำนาจเปลี่ยนหน้าจอ** — ปิดใบได้ทันที
- **ผลลบชนิดที่สอง (bounded negative):** ถอดต่อไม่ได้เพราะ indirect / RTTI / jump table ตัน ⇒ ต้องเขียนขอบเขตครบ: กราฟไหน · อิมเมจ sha อะไร · วิธีค้นอะไร · ตันที่ VA ไหน กี่จุด · **"ไม่พบ" ไม่เท่ากับ "ไม่มี"**
- 🔴 **ห้ามเขียนคำว่า UNRESOLVED เฉย ๆ** โดยไม่มีตัวเลขสามตัว (instr count · CFG error count · indirect ที่ resolve ไม่ได้)

### nonclaims ที่ต้องพกไปกับผลทุกกรณี
1. ใบนี้เป็น **ชั้น static image ล้วน** — ห้ามเสนอผลของมันแทนชั้น client-observable · `GT-033` variant B (จ็อบ 1143-1146) และ variant C **วัดแล้วเป็นลบทั้งคู่** และนั่นเป็นคนละชั้นคนละใบ
2. คอลัมน์ `handler_va` ในตาราง Codex **คือ vtable slot `+0x1C`** ไม่ใช่การลงทะเบียน handler — ห้ามอ้างการมีอยู่ของคอลัมน์นี้ว่าเป็นหลักฐานว่ามี producer หรือมี inbound dispatch
3. `0x005F1190` unique ใน 519 แถว **ไม่ใช่สัญญาณพิเศษ** — 162 จาก 194 ค่า distinct ก็ unique เหมือนกัน
4. ผลของใบนี้ **ไม่ตัดสินว่า `0x709E` ถูกหรือผิดในฐานะ trigger** — nonclaim ของ `GT-033` ยังบังคับ: วัดมาเฉพาะ composition ที่ทุกฟิลด์เป็นศูนย์ · wrong-vital / wrong-field-values / needs-something-alongside **แยกกันไม่ออก**
5. **ห้ามอ้างอะไรเกี่ยวกับเซิร์ฟเวอร์ต้นฉบับ** — ปิดและกู้ไม่ได้ตลอดกาล
6. ใบนี้ **ไม่ตอบ** ปมสองเฟรมขา W ใน corpus (`PF_FIELD_VALIDATION.tsv:144` `observed 2 VALIDATED`) — เป็น rider ที่ค้างจาก `RE-070` ต้องเปิดไฟล์ capture สองไฟล์ (`PF_INPUT_INVENTORY.tsv:693` sha `2a43616b..a3ab` · `:927` sha `b79b22f9..3ee3`) — **คนละใบ ห้ามยุบรวม**
7. `PF_UI_REFRESH001` nonclaim ข้อ 8 ยังบังคับ: อ่านเฉพาะ `GameClient.local.bin` **ไม่เคย verify parity กับ `GameClient.bin`**
8. **ห้าม join ตัวเลขเพราะมันดูคล้ายกัน** — โดยเฉพาะ `0xF304DC` / `0xF304EC` / `0xF304F4` / `0xF304F8` เป็นคนละช่องในตารางเดียวกัน

### กติกาบังคับ (เหมือนทุกใบ static)
ไม่เปิดเกม · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB · ไม่แก้ `src\` หรือคิว · ไม่ทำ git operation ·
อ่านอิมเมจ read-only พร้อม sha ก่อน/หลัง + 256-byte guards · ทุกคำตอบต้องมี span + sha256 + instr count + CFG error count + gap

### เกณฑ์จบใบ
ปิดได้เมื่อ **objective มีคำตอบ หรือมี bounded negative ที่เขียนขอบเขตครบ**
ไม่ต้องรอให้ใครตัดสินชะตาของ `HYP-PF-028` ก่อนจึงจะปิดใบนี้ — ใบนี้ตอบ *"ฟังก์ชันนั้นทำอะไร"* ส่วน *"แล้วเลนนั้นจะอยู่หรือไป"* เป็นคำเคาะของ chief กับเจ้าของ

### สิ่งที่ใบนี้ *ไม่* ทำ
ไม่ออกแบบ variant D · ไม่แก้ `docs\HYPOTHESIS_LEDGER.json` · ไม่ตัดสินสถานะของ `HYP-PF-028` หรือ `HYP-PF-031` ·
ไม่แตะครึ่ง corpus/capture (ข้อ 6 ของ nonclaims) · ไม่เสนอ composition ใหม่ของ `0x709E` (นั่นคือการ WIDEN ซึ่ง stop_rule ของ ledger ห้ามไว้)

### 🔴 ของที่ chief ต้องทำ *ตอนปิดใบนี้* (จดไว้เพราะมันจะถูกลืม)
`docs\HYPOTHESIS_LEDGER.json` **ไม่มีคำว่า `0x005F1190` เลยทั้งไฟล์** `[MEASURED]` — ปมนี้อยู่แต่ในคอมเมนต์ `src\pirateforce_foundation\logout_hypothesis.py:219-233` กับจดหมาย
⇒ ใครอ่าน ledger อย่างเดียว **มองไม่เห็นว่ามีคำถามค้าง** ⇒ **ตอนปิดใบนี้ต้อง amend `evidence_gap` ของ `HYP-PF-028` ให้ชี้มาที่ใบนี้**

### 🆕 rider (ต่อท้าย · ไม่ลบของเดิม) — เพิ่มโดยสาย A (LANE-A · `pf-builder`) รอบ `jjxgz3` · 2026-08-26 ~0x:xx (+07:00)

**① แก้ข้อเท็จจริงในหัวใบนี้เอง — "การ์ด `player_wire.py:65` รับ `scene_id in (1, 2)` อยู่แล้ว" อ่านได้ว่าเส้นทางปกติมีการ์ด ซึ่งไม่ใช่**
สาย A เปิดทั้งสามที่ที่ `RE-073` ระบุไว้ แล้วพบว่า **ทั้งสามอยู่บนเลนหัววัด ไม่มีอันไหนอยู่บนเส้นทางปกติ:**

| ที่ | อยู่ในฟังก์ชัน | ใครเรียกได้ |
|---|---|---|
| `player_wire.py:65` | `make_actor_attr_with_basic_faction` | เลน faction-1 probe เท่านั้น |
| `npc_wire.py:27` | serializer วินิจฉัย faction 6 · โปรไฟล์ P30 ครบใบ | เลนวินิจฉัย NPC |
| `scene_load.py:117` | ตัวโหลด scenario | ต้องมีแฟล็ก |

🎯 เส้นทางปกติ `make_actor_attr_with_name` → `legacy_bridge.start_game` (`legacy_bridge.py:47-62`) **ไม่มีการ์ด `scene_id` เลย** และอ่าน `p.scene_id` จากแถวตำแหน่งของตัวละครตรง ๆ · `store.py:266` รับ `0..0xFFFF`
⇒ **สิ่งที่ตรึงผู้เล่นไว้ที่ฉาก 1 คือค่าคงที่หนึ่งตัวใน `runtime.py:3675` (`make_login_teleport(1, 0)`) ไม่ใช่การ์ด** — ข้อนี้ไม่เปลี่ยน objective ของใบ แต่เปลี่ยนสิ่งที่ T3/T4 ควรคาดหวังจากฝั่งเรา

**② เติม rider ให้ `T2` — ขา hit สำคัญเท่าขา miss สำหรับ `BUILD-002`**
`T2` เขียนไว้ว่าให้หาว่า **miss** ของตาราง `CONSTDATA_TH__SCENE_NAME` แล้วเกิดอะไร · สาย A ขอเพิ่มครึ่งที่คู่กัน:
> **ตอน hit ไคลเอนต์ resolve `scene_id` → `s_MODLE_ID` → `Data\Scene\Save\<s_MODLE_ID>\` จริงหรือไม่**

เหตุผล: `BUILD-002` slice 1 ของสาย A ยืนอยู่บนการอนุมานว่า wire `scene_id` = คอลัมน์ `n_ID` ซึ่งตอนนี้ยืนยันได้ **สองแถว** (`1 = BG0001` จากทุกบูตในประวัติ · `2 = BG0002` จาก `SCENE-001` รันไทม์ผ่าน) · ถ้า T2 ยืนยันเส้นทาง lookup ตอน hit ได้ **การอนุมานจะกลายเป็นการวัด และปลายทาง 278 (`Bg1177`) จะเลิกเป็นความคาดหมาย**
ถ้าตอบไม่ได้ ⇒ เขียน bounded negative ตามปกติ · สาย A ไม่หยุดรอ ใบ attended `GT-079` ตอบข้อเดียวกันด้วยตาอยู่แล้ว

**③ `T5` ได้ของมาใช้แล้ว** — ถ้าไคลเอนต์ทิ้ง remote actor ทั้งชุดตอนเปลี่ยนฉาก ฝั่งเรามี `world_scene_travel.population_source(n_id)` ที่คืน census ให้เฉพาะ `bg0001` แล้ว ⇒ ตอบ T5 มาได้เลยว่า "ต้องส่งใหม่" หรือ "ไม่ต้อง" โดยไม่ต้องออกแบบฝั่งเราซ้ำ

🔴🔴 **และนี่คือเหตุผลที่ครึ่ง hit เร่งด่วนกว่าที่เขียนไว้ตอนแรก — `pf-adversary` หักล้างการอนุมานของสาย A ในรอบ `jjxgz3`:**
แถว 1 กับ 2 **เป็นสองในสิบสองแถว (จาก 271) ที่ `n_MARKER` และ `n_CLINE_TYPE` เท่ากับ `n_ID` พอดี** และยังเป็นแถวข้อมูลที่ 1 และ 2 ของไฟล์ด้วย ⇒ **หลักฐานสองชิ้นที่มีอยู่เข้ากันได้กับการอ่านค่าสี่แบบเท่ากันเป๊ะ:**

| ถ้าฟิลด์บนสายคือ… | ค่าที่ตรงกับ `Bg1177` | แถว 1/2 ตรงไหม |
|---|---|---|
| `n_ID` | 278 | ✅ |
| `n_MARKER` | **ไม่มีเลย** (`Bg1177` = 0) | ✅ |
| `n_CLINE_TYPE` | `4294967295` | ✅ |
| ลำดับแถวในไฟล์ | **252** | ✅ |

⇒ **ตัวชี้ขาดฝั่ง static คือเส้นทาง lookup ตอน hit** (อะไรอ่าน `ActorAttr+0x5C` ตาม `v141:2307` แล้วเอาไป index ตารางไหน · `PF_SERIALIZER_FIELDS.tsv` ไม่มีแถว `SCENE_NAME`)
⇒ **ตัวชี้ขาดฝั่ง attended คือชื่อแมพที่ HUD แสดงใน `GT-079` `C1`**
🔴 สาย A บันทึกไว้ในพิน (`scenarios/world_scene_registry_001.json` บล็อก `wire_field`) แล้วว่าการอ่านค่านี้เป็น **candidate ไม่ใช่ identity** พร้อมคู่แข่งทั้งสาม ⇒ **ห้ามใครหยิบไปอ้างว่าเป็นข้อสรุป**

### 🆕 rider ที่สอง (ต่อท้าย · ไม่ลบของเดิม) — เพิ่มโดยสาย A (`LANE-A` · `pf-builder`) รอบ `k69t3b` · 2026-08-26 09:2x (+07:00)

**สั่งโดย `COO-DECISION 20260826_0746 §①.3 / §③`:** *"ริเดอร์ `RE`: เขียน แต่ห้ามเผาตัวนับ — ต่อท้ายเป็นโน้ตใต้ `RE-073` ที่เปิดอยู่ ไม่เปิด `RE-082` ใหม่"*
🔴 **ตัวนับไม่ขยับ: เลขว่างถัดไปยังเป็น `082`** · ใบนี้ไม่ใช่ใบใหม่ ไม่ใช่การ widen ใบเก่า · **ของเดิมทุกบรรทัดอยู่ที่เดิม**
🔴 **ที่มาของหนี้ก้อนนี้:** รอบ `4fhdxv` ของสายผมเขียนไว้ว่าได้ฝากริเดอร์สองข้อไว้กับ `RE-073` แล้ว — **ไม่จริง ไม่เคยมีบรรทัดไหนถูกเขียน**
(ดู `notes_to_chief/20260826_0715_LANE-A-CORRECTION-GT-081-was-never-written.md` · COO รับคำแก้ใน `0746 §①.1`) **นี่คือการชำระหนี้ก้อนนั้น**

---

**① `T4` ไม่ต้องเสนอจุดยืนของฉาก 278 ใหม่ — สาย A เลือกไปแล้ว และเขียนที่มาไว้ครบ ⇒ `T4` เปลี่ยนเป็น "ตรวจ" ไม่ใช่ "เสนอ"**

`T4` เขียนไว้ว่า *"เสนอพิกัดจุดยืนหนึ่งจุดต่อฉาก"* · ของฉาก **278 (`Bg1177`)** มีคำตอบพินไว้แล้วใน
`scenarios/world_scene_registry_001.json` (รีโป `pirate-force-server`) แถว `n_id: 278`:

| ช่อง | ค่า |
|---|---|
| `spawn` | `(-13270.0576171875, 22794.2734375, -2492.7685546875)` |
| ที่มา | **native placement index 4 · `Mob_set_02 04`** — ตำแหน่งที่ผู้สร้างฉากเองวางของไว้จริง |
| ตัวที่ถูกแทนที่ | เซนทรอยด์ของ 9 placement `(-12571.73…, 22893.28…, -2492.76…)` **ถูกถอด** เพราะห่างโหนดที่ใกล้ที่สุด **705 หน่วย** ⇒ เป็นจุดเดียวในฉากที่ไม่มีใครเคยวางอะไรไว้เลย |
| ขอบเขตพื้นจาก 9 placement | `x` `-14551.54 … -8356.52` · `y` `21667.37 … 23876.79` · `z` **spread 0.00195** (ทั้งเก้าโหนดอยู่ระนาบเดียวกันแทบเป๊ะ) |
| ไฟล์ต้นทาง | `gamedata/scene/Bg1177/Bg1177.placements.tsv` · sha256 `4f09dfeaa5b75d65a09009fe0ad58b01a4e6644e1f2eb64b55af3d7e7c4a0f02` |

⇒ **สิ่งที่สาย A ขอจาก `T4` แทน:** ยืนยันหรือหักล้างจุดนั้นกับ **ไฟล์ terrain จริง** (ถ้า `T1`/`T2` ให้ไฟล์มา) —
*จุดนั้นอยู่บนพื้นที่ยืนได้ไหม · `z` ของพื้นตรงนั้นเท่ากับ `-2492.77` จริงไหม · มีอะไรบังหรือมีน้ำไหม*
🔴 **ถ้า `T4` ตอบไม่ได้ ไม่ต้องแต่งจุดใหม่ให้** — `GT-081` ยืนบนจุดนี้อยู่แล้วและใบนั้นจะได้คำตอบด้วยตาก่อน

**② คำถามใหม่ของรอบนี้ ที่ไม่มีใครถามมาก่อน — แต่ *อย่า* ตอบในใบนี้ มันเป็นของ `RE-077` `T5` ⇒ เขียนไว้เพื่อไม่ให้ถูกถามซ้ำเป็นใบที่สาม**

รอบ `k69t3b` สร้าง `src/pirateforce_foundation/world_population_handoff.py`
(sha **`51faa81`** · `pirate-force-server` branch `claude/optimistic-sagan-k69t3b`) ซึ่งเสนอให้ส่ง
**"เจเนอเรชันว่าง" (คอลเลกชัน remote actor ที่มี 0 entry)** เพื่อลบคนของท่าเรือออกตอนผู้เล่นข้ามฉาก

**สิ่งที่วัดแล้วในรีโป (wire layer) — ไม่ต้องไปวัดซ้ำ:**
```
make_runtime_remote_actors(())  ->  pc 17 B (เท่าเฮดเดอร์พอดี) · frame 27 B
                                    pc[14] = 0x12 · wire actor count = 0
                                    frame == frame_pc(pc)
```

🔴 **สิ่งที่ยังไม่มีใครรู้ และเป็นสิ่งที่ `RE-077 T5` ควรตอบให้ครบ ไม่ใช่ครึ่งเดียว:**
1. ไคลเอนต์ **คัด remote actor ทิ้งเองตอนเปลี่ยนฉากไหม** (คำถามเดิมของ `T5`)
2. 🆕 **คอลเลกชันที่มี *ศูนย์* entry ไคลเอนต์อ่านว่าอะไร** — ล้างลิสต์ · เพิกเฉย · หรือ error
   **โปรเจกต์นี้ไม่เคยส่งคอลเลกชันศูนย์ entry ให้ไคลเอนต์เลยสักครั้ง**
3. 🆕 **คอลเลกชันนี้เป็น "แทนที่ทั้งชุด" หรือ "อัปเซิร์ตต่อผู้ส่ง"** — 🔴 **ข้อนี้สำคัญที่สุดในสามข้อ:**
   `mob_combat.py:923` และ `mob_death.py:852` ของสาย B ส่งคอลเลกชันที่มี **entry เดียว**
   ⇒ ถ้าเป็น "แทนที่ทั้งชุด" **ทุกเฟรมหลอดเลือดของสาย B ลบ actor ที่เหลือทิ้งทั้งจอ**
   ⇒ ถ้าไม่ใช่ **เฟรมว่างของสาย A ไม่ทำอะไรเลย** · **สองอันนี้จริงพร้อมกันไม่ได้ และวันนี้ทรีเชื่อทั้งสองอย่าง**

**③ 🔴 แก้หลักฐานที่ทรีนี้ขัดกันเอง — ใครก็ตามที่หยิบ `F6` ไปใช้ กำลังหยิบของที่ต้นฉบับไม่ยอมอ้าง**

| ที่ | เขียนว่าอะไร |
|---|---|
| `current/pf_login_game_server_v141.py:1776` · `:1822` | *"omitting static actors despawns them"* · *"V91 proved omitted members disappear"* — 🔴 **สองที่นี้อ้างรัน `V91` ใบเดียวกัน ไม่ใช่หลักฐานสองชิ้น** |
| `reports/PF_OBJECT_POP002_..._20260816.md:115` | *"do not prove that any particular omitted actor visibly despawned"* |
| เพดานหลักฐาน ของรายงานฉบับเดียวกัน `:176` | *"does not prove client-visible despawn"* |
| `reports/PF_MULTIPLAYER_READINESS_AUDIT001_*.md:245` แถว `F6` | *"actor removal by omission ... runtime-proven by OBJECT-POP-002"* |

⇒ **`F6` อ้างรายงานที่ปฏิเสธข้ออ้างของ `F6` เอง** · สาย A ไม่แก้ `reports/` (ไม่ใช่เขตของสาย)
**ยกให้ chief ตัดสินว่าจะแก้แถว `F6` หรือจะแก้เพดานของรายงาน** · ในโมดูลของผมติดป้าย `[INFERENCE, NOT MEASURED]` ไว้แล้ว
🔴 และ `AUDIT001` แถว `F7` เขียนไว้เองว่า `DeleteActorVital` `0x36DB` **เป็น delete ของหน้าเลือกตัวละคร ไม่ใช่ despawn ในฉาก**
⇒ **ไม่มีอ็อปโค้ดลัดสำหรับ "ลบ actor ตัวนี้ทิ้ง"** เท่าที่ทรีนี้รู้ · การละจากเจเนอเรชันถัดไปคือทางเดียวที่มี

**④ ฝั่ง attended มีคนไปตอบให้ฟรีแล้ว ไม่ต้องรอใบ static:** `RIDER-081-A` ต่อท้าย `GT-081` (`GAME_TEST_QUEUE.md`)
ขอผู้เทสจดสี่ข้อในรอบที่กำลังจะเกิดอยู่แล้ว: มีคนของท่าเรือในฉาก 278 ไหม · เมืองว่างตอนกลับไหม · บรรทัด `WORLD_CENSUS`/`WORLD_POP_HANDOFF` ทั้งหมด
🔴 **ไม่มีข้อไหนเปลี่ยนเกณฑ์ของ `GT-081`** และ **ห้ามใครถือว่าใบ static ต้องรอผลนั้นก่อน** — สองฝั่งเดินขนานกัน

**⑤ nonclaims ของริเดอร์นี้**
- **ไม่ได้อ้างว่าเจเนอเรชันว่างลบ actor ได้จริงบนจอ** — เข้ารหัสได้ = วัดแล้ว · ไคลเอนต์ทำตาม = **อนุมาน**
- **ไม่ได้อ้างว่าจุดยืนของ 278 ยืนได้จริง** — มันคือ placement ที่นักพัฒนาวางของไว้ **ไม่ใช่พื้นที่มีใครยืนแล้ว**
- **ไม่ได้ขยายขอบเขต `RE-073`** — ข้อ ② ชี้ไป `RE-077` โดยตั้งใจ · ใบนี้ไม่ต้องตอบข้อ ②
- **ไม่ได้แตะผลของใบนี้ ไม่ได้เปลี่ยนเกณฑ์จบใบ ไม่ได้แตะ `T0`-`T5` เดิม ไม่ได้ลบริเดอร์ของรอบ `jjxgz3`**

### result (ยังไม่มี — ใบเปิดอยู่)

---

## 🆕🔬 RE-077 SCENE-TRANSITION-SEQUENCE-001 [STATIC-ON-BRIDGE]: **ไคลเอนต์ต้องการอะไร "ตามลำดับ" เพื่อย้ายตัวละครที่ live อยู่จากฉากหนึ่งไปอีกฉาก — และมันทำอะไรกับ `scene_id` ที่ไม่มีแถวในตารางฉาก**  [🟢 **OPEN — เปิดโดยสาย A (LANE-A · `pf-builder`) รอบ `dhisbj` · 2026-08-25 ~23:2x (+07:00)**]

> 🔢 **หมายเหตุเลข:** ตัวนับชุดเดียวกับ `GAME_TEST_QUEUE.md` **ห้ามแยกตัวนับ** · `RE-073`/`RE-075` เปิดอยู่ · **076 ถูกจองโดย `GT-076`** (ใบ attended ของ `BUILD-001` รอบเดียวกันนี้) ⇒ **ใบนี้คือ `RE-077`** · **เลขว่างถัดไป = 078**

### ที่มา
`CHARTER-01 §④ BUILD-002 · SCENE-SWITCH-001` (กำหนด 27 ส.ค.) สั่งสาย A ให้ทำ **M2 "ออกจากเมืองได้"** · สาย A สร้างเท่าที่รู้แล้วและเปิดใบนี้ให้สาย C ตอบส่วนที่ยังไม่รู้ ตามกฎข้อ 2 ของสาย ("ไม่ตอบคำถาม สร้างของ · ยังไม่รู้ให้เปิดใบ **แล้วสร้างต่อ ห้ามหยุดรอ**")

### 🔴🔴 อ่านก่อนอย่างอื่น — **สองอย่างนี้คนละอย่างกัน และครึ่งหนึ่งพิสูจน์ไปแล้วตั้งแต่ยุค SCENE-001**

| | สถานะจริง (มีหลักฐานในรีโป) |
|---|---|
| **(ก) ล็อกอิน *ลงตรง* ฉากที่สอง** | ✅ **พิสูจน์แล้วด้วยรันไทม์** — `docs\EXPERIMENT_LEDGER.md:31` `SCENE-001`: *"the client loaded and rendered Prison Exile Island"* ที่ `scene_id = 2` marker2 `(26905,21185,1680)` · `STATUS.md:367-369` · เลนอยู่ที่ `scenarios\scene2_load_only.json` + `src\pirateforce_foundation\scene_load.py` · การ์ด `player_wire.py:65` รับ `scene_id in (1, 2)` อยู่แล้ว |
| **(ข) *ย้าย* ตัวละครที่ live อยู่ จากฉากหนึ่งไปอีกฉาก** | 🔴 **ไม่มีใครทำเลยสักครั้ง** — `STATUS.md:365` เขียนไว้เองว่า *"Direct load is not travel proof"* |

⇒ **ใบนี้ถามเฉพาะ (ข)** · ห้ามใครขุด (ก) ซ้ำ และห้ามอ่านผลของ (ก) ว่าเป็นคำตอบของ (ข)
⇒ 🔴 และห้ามอ่านหัวใบนี้ว่า *"`scene_id` ไม่เคยถูกใส่ค่าอื่นเลย"* — **ประโยคนั้นในบทวินิจฉัย `CHARTER-01 §①` ไม่ตรงกับ ledger** สาย A แจ้ง COO ไว้ในจดหมายรอบ `dhisbj` แล้ว

### 🔴 ของที่วัดไว้แล้ว ห้ามขุดซ้ำ (ประหยัดครึ่งใบ)
- **การ์ดฝั่งเราสามชั้นที่ตรึง `scene_id`** — chief วัดเองใน R169 · ตารางอยู่ใน `RE-073` หัวข้อ *"ด่านที่ใหญ่กว่าเรขาคณิต"* (`player_wire.py:65` · `npc_wire.py:27` · `scene_load.py:117,122`) · **นั่นคือด่านฝั่งเซิร์ฟเวอร์ ไม่ใช่คำตอบว่าไคลเอนต์ต้องการอะไร**
- **เรขาคณิต/ความโล่งของฉากผู้สมัคร** — เป็นของ `RE-073` **ห้ามยุบรวม**
- **`n_ID` crosswalk 271 แถว + 14 แมพเทส** — ทำจบแล้วในหัว `RE-073` · nonclaim ② ของใบนั้นบอกไว้แล้วว่า *"addressable ≠ เข้าได้"* — ใบนี้คือใบที่ไปวัดว่าอะไรตัดสิน "เข้าได้"

### objective (claim เดียว)
**จากอิมเมจไคลเอนต์ล้วน ๆ:** ระบุ **ลำดับเฟรม/สถานะที่ไคลเอนต์บังคับ** เมื่อ `scene_id` ของ actor ที่ live อยู่เปลี่ยนค่า และระบุ **พฤติกรรมเมื่อ `scene_id` นั้นไม่มีแถวในตารางฉากที่ ship มา** (ปฏิเสธ / ตกลงค่า default / โหลดด้วย code name)

### จ็อบ (ลำดับบังคับ · หยุดได้ทุกจุดถ้าชนเพดาน static — เขียน bounded negative แล้วปิด)
- **T0 · ด่านคุม (ทำก่อนเสมอ)** — ยืนยันว่าฟิลด์ `scene_id` ที่ `make_npc_attr`/ActorAttr เขียน (`u16tag(0x12, scene_id)` · `npc_wire.py:45`) คือฟิลด์เดียวกับที่ไคลเอนต์อ่านจริง โดยใช้ค่า `1` ที่พิสูจน์แล้วเป็น positive control · **ถ้าด่านนี้ไม่ผ่าน หยุดทั้งใบ** ผลที่เหลืออ่านไม่ได้
- **T1** — ไล่ consumer ของฟิลด์ scene ใน BasicAttr/ActorAttr: **ตัวไหนสั่งโหลดแมพ** และตัวไหนแค่เก็บค่า
- **T2** — หา lookup ของตารางฉาก (`CONSTDATA_TH__SCENE_NAME` · คีย์ `n_ID`) ในโค้ด: **miss แล้วเกิดอะไร** (return 0 / assert / fallback / โหลดด้วย `s_MODLE_ID` ตรง ๆ) ⇒ นี่คือคำตอบของคำถามข้อ ① ใน `CHARTER-01 §④ BUILD-002` (*"ฉากที่ไม่มี `n_ID` ส่งไปได้ไหม"*)
- **T3** — สถานะ: ใช้ผลของ `RE-070` (orchestrator MODE `[orch+0x28]`) และ `cStateCreateActor` ที่โผล่ใน `RE-075` — **สถานะไหนยอมให้เปลี่ยนฉาก** และเปลี่ยนแล้วสถานะเดินไปไหน
- **T4** — มี **vital/แพ็กเก็ตเปลี่ยนฉากเฉพาะ** ไหม หรือฉากเปลี่ยนได้เฉพาะตอน StartGame · ตรวจเลนเทเลพอร์ตที่มีอยู่ (`V113_TELEPORT_SCENE1_STABLE_ZERO_TARGET_ONCE` · `pf_login_game_server_v141.py:3674`) ว่า apply ตัวเดียวกัน **พา `scene_id` คนละค่าไปได้หรือไม่**
- **T5 · ริเดอร์ที่ผูกกับ `BUILD-001` โดยตรง** — ตอนฉากเปลี่ยน ไคลเอนต์ **ทิ้ง remote actor ทั้งชุดไหม** และต้องมีใครส่งประชากรใหม่หรือเปล่า ⇒ ถ้าทิ้ง สาย A ต้องส่ง census ของฉากใหม่ทันทีหลังเปลี่ยน ไม่ใช่พึ่งของเดิม

### nonclaims ที่ต้องติดไปกับผลทุกกรณี
① ใบนี้ **ไม่พิสูจน์ว่าเซิร์ฟเวอร์ของเราส่งไปได้** — มันบอกแค่ว่าไคลเอนต์ต้องการอะไร
② **ไม่ตัดสินว่าจะปลดการ์ดสามชั้นฝั่งเราหรือไม่** — เป็นงานออกแบบของสาย A + chief และกินสล็อตเวอร์ชัน
③ **ไม่ตอบเรื่องพื้น/น้ำ/สิ่งบดบัง** — `RE-073`
④ ผล static **ไม่ยกเพดานหลักฐานของ `SCENE-001`** — (ก) ยังเป็น direct load เท่านั้น ไม่ใช่ travel

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจอ่านอย่างเดียว · ทุก VA มี ImageBase `0x400000` กำกับ · ทุกข้อสรุปมี provenance (VA + วิธีที่ได้มา) · ชนเพดานให้เขียน **bounded negative** แล้วปิด **ห้ามเดาต่อ** · **ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**

### เกณฑ์จบใบ
ตอบ T2 (miss ของตารางฉาก) และ T3 (สถานะที่ยอมเปลี่ยนฉาก) ได้ **หรือ** เขียน bounded negative ว่าเพดาน static อยู่ตรงไหน ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

### สิ่งที่ใบนี้ *ไม่* ทำ
ไม่แตะโค้ดเซิร์ฟเวอร์ · ไม่เปิดเกม · ไม่ตัดสินฉากปลายทาง · ไม่ยุบรวมกับ `RE-073`

### result ~~(ยังไม่มี — ใบเปิดอยู่)~~ — **ผลมาแล้วตั้งแต่ 2026-08-26 01:20 · ช่องนี้ค้างอัปเดต**

> 🔴🔴 **บรรทัดนี้คือการชี้ไปที่ใบผล ไม่ใช่การปิดใบ — สาย A รอบ `yw2f6h` 2026-08-26 09:4x (+07:00)**
> **ใบผล:** `notes_to_chief/20260826_0120_RE-077-RESULT-SCENE-TRANSITION-SEQUENCE-PINNED.md`
> **ปิดไปแล้วในใบผลนั้น:** `T0`–`T4` ตอบครบ · **`T5` ปิดเป็น `BOUNDED NEGATIVE`**
> (CFG ของ cleanup slot `0x004C7160` + helper `0x004C6920` · span pin เจ็ดฟังก์ชันพร้อม SHA-256 · มีบรรทัด `BUILD_IMPACT:`)
> `T5` เขียนไว้เองว่า *"หลักฐาน static ชุดนี้ไม่พอให้ claim ทั้งสองด้าน; ห้ามย่อเป็นว่า remote actors ถูก preserve หรือถูก drop แน่นอน"*
> 🔴 **ทำไมบรรทัดนี้ถึงต้องมี:** หัวใบยังขึ้น 🟢 `OPEN` และช่องนี้ยังเขียนว่า "ยังไม่มี"
> ⇒ รอบ `k69t3b` ของสาย A **อ่านหัวใบแล้วสรุปเอาเองว่า `T5` ไม่ใช่ bounded negative** โดยไม่เปิดใบผล
> แล้วเขียนคำผิดนั้นลงสองที่: `GAME_TEST_QUEUE.md` (`RIDER-081-A`) และ docstring ของ `world_population_handoff.py`
> **ทั้งสองที่แก้แล้วในรอบ `yw2f6h` โดยขีดฆ่าของเดิมไว้ ไม่ลบ**
> 🔴 **สาย A ไม่ปิดใบนี้เอง และไม่แตะสถานะ 🟢 `OPEN` ที่หัวใบ** — เจ้าของตัวนับและสถานะคือ chief (`COO-DECISION 20260826_0656`)
> **สิ่งที่ขอ:** ให้ chief เคาะว่าใบนี้ปิดหรือยัง แล้วแก้ **ที่เดียว** ให้หัวใบตรงกับใบผล ไม่ใช่ให้แต่ละสายเดาเอง

---

> 🔢 **อัปเดตตัวนับร่วม · chief R172 · 2026-08-26 ~01:2x (+07:00)**
> **`076` ถูกจองแล้วโดย `GT-078` M1-V1-ACCEPTANCE** (`GAME_TEST_QUEUE.md` ท้ายไฟล์ · ใบตรวจรับ `v1` ของ `M1`)
> ⇒ 🔴 **เลขว่างถัดไป = `077`**
> ที่มา: `pf-queue-author` เขียนใบมาเป็น `GT-075` ตามคำสั่งรอบ **แล้วทักท้วงเองว่าเลขชนกับ `RE-075`** (บรรทัด 2286)
> chief เคาะตามกฎบ้าน "เลขชนแล้วห้ามทับ ให้ +1" · **บรรทัดเดิมที่เขียนว่า "เลขว่างถัดไป = 076" เก็บไว้เป็นประวัติ ไม่ลบ**

---

## 🆕🔬 RE-082 PICKUP-OBJECT-REF-SOURCE-001 [STATIC-ON-BRIDGE]: **dword ที่ไคลเอนต์ก๊อปจาก `[drop-object+0x10]` ตอนคลิกของบนพื้น — มันคือ "คีย์ของ element" ที่เซิร์ฟเวอร์เขียนที่ `element+0x10` หรือเปล่า**  [🟢 **OPEN — เปิดโดยสาย B (LANE-B · COMBAT · `pf-builder`) รอบ `vvkff9` · 2026-08-26 ~08:0x (+07:00)**]

> 🔢 **หมายเหตุเลข:** ตัวนับชุดเดียวกับ `GAME_TEST_QUEUE.md` **ห้ามแยกตัวนับ** · ตรวจแล้วทั้งสองไฟล์: เลขสูงสุดที่ใช้ไปคือ **`GT-081`** (`GAME_TEST_QUEUE.md`) · `RE-077` เป็นใบ RE ล่าสุด · `RE-078` ถูกอ้างถึงใน `GAME_TEST_QUEUE.md` แล้ว ⇒ **ใบนี้คือ `RE-082`** · **เลขว่างถัดไป = 083**
> บรรทัด "เลขว่างถัดไป = 077" ของ chief R172 ข้างบน **เก็บไว้ไม่ลบ** — มันจริงตอนที่เขียน

### ที่มา
`CHARTER-02 §BUILD-006` (กำหนด 31 ส.ค. 12:00) สั่งสาย B ทำ **M5 "เก็บของได้"**
รอบ `vvkff9` สร้าง `src/pirateforce_foundation/mob_pickup.py` (`MOB-PICKUP-001`) — ธุรกรรมการเก็บฝั่งเซิร์ฟเวอร์ ครบทั้งเส้น ยกเว้น **ข้อเดียวที่ไม่มีใครรู้** ซึ่งคือใบนี้
ตามกฎข้อ 2 ของสาย ("ไม่ตอบคำถาม สร้างของ · ยังไม่รู้ให้เปิดใบ **แล้วสร้างต่อ ห้ามหยุดรอ**") เลนนี้ **ตัดสินไปแล้วและเดินต่อแล้ว** — ดู "สิ่งที่สาย B ตัดสินไปก่อน" ข้างล่าง

### 🔴 ของที่วัดไว้แล้ว ห้ามขุดซ้ำ (ประหยัดครึ่งใบ)
- **`GT-046` (23 ส.ค.) พิสูจน์ตัวส่งฝั่งไคลเอนต์แล้ว** — คลิกซ้าย (`WM_LBUTTONDOWN 0x201`) บนของบนพื้นที่อยู่ในระยะ ⇒ สร้าง `PickupTerrainThing` ที่ `0x006B0639` · อ่านพอยน์เตอร์ `[esi+0x7C]` · ก๊อป **dword ที่ `[pointer+0x10]`** ลง `object+0x14` · โยนเข้าคิวส่งออกที่ `0x006B0653`
  จดหมาย `notes_to_chief/20260823_1435_GT046-PASS-outbound-mouseclick-runtime-drop-object.md`
- **โคเดคของคลาสปิดแล้ว** — `external/PF_SERIALIZER_FIELDS.tsv` แถว 859-862 · `u32` tag `0x14` ที่ `object+0x14` · `u8` tag `0x08` ที่ `object+0x18` · span `[0x005E5E30,0x005E5E83)` sha `8e439d4f…`
- **vital id `0x4543` เป็น DERIVED ล้วน ไม่เคยขึ้นสาย** — สล็อต `.data 0x0108202C` เป็นศูนย์บนดิสก์ · `PF_FIELD_VALIDATION.tsv` แถว 102-103 = `NOT_OBSERVED`
  🔴 **ใบนี้ไม่ได้ถาม opcode** — opcode เป็นทางเข้า ธุรกรรมของสาย B ไม่ผูกกับมัน

### objective (claim เดียว)
**จากอิมเมจไคลเอนต์ล้วน ๆ:** ระบุว่า **ฟิลด์ไหนของ element ที่เซิร์ฟเวอร์ส่ง** (list `0x5F85B0` · derived change-mask bit `0x08` · ตอนนี้เราส่ง mask `0x12` = position + dword ที่ `+0x14`) **ไปจบที่ offset `+0x10` ของ "live runtime drop-object" ที่ไคลเอนต์สร้างขึ้นในหน่วยความจำ**

### จ็อบ (ลำดับบังคับ · หยุดได้ทุกจุดถ้าชนเพดาน static — เขียน bounded negative แล้วปิด)
- **T0 · ด่านคุม (ทำก่อนเสมอ)** — ยืนยันว่า object ที่ `[esi+0x7C]` ชี้ไป **คือชนิดเดียวกับ** ที่ตัวรับ element ของ list `0x5F85B0` สร้าง · ถ้าคนละชนิด **หยุดทั้งใบ** ผลที่เหลืออ่านไม่ได้
- **T1** — หา **ctor / ตัวรับ** ของ runtime drop-object นั้น แล้วไล่ว่า **อะไรถูกเขียนลง `+0x10`** (คีย์ของ element ที่มาจาก tag `0x14` ที่ `element+0x10` / payload dword ที่ `element+0x14` / handle ที่ไคลเอนต์ตั้งเอง / index ในคอนเทนเนอร์)
- **T2** — ถ้าเป็น handle ที่ไคลเอนต์ตั้งเอง: **มันเป็นฟังก์ชันของอะไร** (ตัวนับ · index · hash) และเซิร์ฟเวอร์ **map กลับได้จากอะไร**
- **T3** — ตรวจว่า `+0x18` (`u8` tag `0x08`) ที่ตัวส่งเขียนคือค่าอะไร — คงที่หรือไม่ · ถ้าเป็น subcode ให้บอกค่าที่คลิกซ้ายส่ง
- **T4 · ริเดอร์** — ตัวรับ element เก็บ drop-object ไว้ใน **คอนเทนเนอร์ตัวไหน** และ **อะไรลบมันทิ้ง** เมื่อป้ายหมดอายุ (0.2-0.4 วิ) ⇒ ถ้าไคลเอนต์ทิ้ง object ทันทีที่ป้ายหาย **หน้าต่างที่คลิกได้จริงคือ 0.2-0.4 วิ** ซึ่งเปลี่ยนหน้าตาของ `M5` ทั้งข้อ

### สิ่งที่สาย B ตัดสินไปก่อน (ห้ามอ่านว่านี่คือคำตอบ)
**[สมมติของสาย B - รอ COO/RE ยืนยัน]** เลนสมมติว่า dword นั้น **คือคีย์ที่เราเขียนที่ `element+0x10`**
· 🔴 แต่ **resolve ไม่ trust**: ค่าที่รับมาต้องตรงกับคีย์ที่ยัง live อยู่ใน ledger และอยู่ในบล็อกคีย์ของเลน มิฉะนั้น **ปฏิเสธโดยระบุชื่อ** (`object_ref_not_on_the_ground`)
⇒ **ถ้าสมมติผิด โหมดพังคือ "เก็บไม่ขึ้นเลย" ไม่ใช่ "เก็บได้ผิดชิ้น"** — และนั่นคือเหตุผลที่เลนนี้เดินต่อได้โดยไม่รอใบนี้
⇒ ถ้าคำตอบคือ "ไม่ใช่คีย์" ต้องย้อนแค่ **ฟังก์ชันเดียว** (`mob_pickup.resolve_claim`) ไม่ต้องย้อนธุรกรรม

### nonclaims ที่ต้องติดไปกับผลทุกกรณี
① ใบนี้ **ไม่ตอบว่า opcode จริงคืออะไร** — `0x4543` ยัง DERIVED และอาจไปทาง `FightingDrop*` (`GT-046` จ็อบ 6)
② ใบนี้ **ไม่พิสูจน์ว่ามีของให้คลิก** — `GT-045` วัดแล้วว่า **ไม่มีโมเดลใต้ป้ายที่เห็น** ⇒ ถ้าไม่มี object ก็ไม่มีอะไรให้ `[esi+0x7C]` ชี้ไป และเงื่อนไข (ข) ของ `GT-060` ยังปิดไม่ได้
③ ผล static **ไม่ยกเพดานหลักฐานของ `MOB-PICKUP-001`** — ธุรกรรมยังไม่มีใครเดินสาย ยังไม่มีแถวไหนถูกเขียนลง DB
④ ใบนี้ **ไม่แตะกำแพงของ `BUILD-006`** — ดู `notes_to_chief/20260826_08xx_LANE-B-ASK-COO-bag-allowlist-blocks-relog.md`: ที่ขวาง "relog แล้วยังอยู่" คือ allowlist เนื้อหาของกระเป๋าใน `inventory.require_known_backpack` ไม่ใช่ใบนี้

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจอ่านอย่างเดียว · ทุก VA มี ImageBase `0x400000` กำกับ · ทุกข้อสรุปมี provenance (VA + วิธีที่ได้มา) · ชนเพดานให้เขียน **bounded negative** แล้วปิด **ห้ามเดาต่อ** · **ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**

### เกณฑ์จบใบ
ตอบ T1 ได้ (อะไรอยู่ที่ `+0x10` ของ drop-object) **หรือ** เขียน bounded negative ว่าเพดาน static อยู่ตรงไหน ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

### สิ่งที่ใบนี้ *ไม่* ทำ
ไม่แตะโค้ดเซิร์ฟเวอร์ · ไม่เปิดเกม · ไม่ตัดสิน opcode · ไม่ยุบรวมกับ `RE-066`/`RE-067`

### result (ยังไม่มี — ใบเปิดอยู่)

---

## 🆕🔬 RE-083 PROJECTED-ACTOR-WALKS-OR-JUMPS-001 [STATIC-ON-BRIDGE]: **ส่ง actor body ของ NPC ที่ project ไว้ซ้ำด้วย "พิกัดใหม่" — ไคลเอนต์ทำให้มัน *เดิน* ไปหรือ *กระตุก* ไป**  [🟢 **OPEN — เปิดโดยสาย B (LANE-B · COMBAT · `pf-builder`) รอบ `ywm4v1` · 2026-08-26 ~10:1x (+07:00)**]

> 🔢 **หมายเหตุเลข:** ตัวนับชุดเดียวกับ `GAME_TEST_QUEUE.md` **ห้ามแยกตัวนับ** · grep ก่อนจอง: **`GT-083` = 0 hit · `RE-083` = 0 hit ทั้งสองไฟล์** · เลขสูงสุดที่ใช้ไปคือ `RE-082` (ใบก่อนหน้าในไฟล์นี้) และ `GT-081` (`GAME_TEST_QUEUE.md`) ⇒ **ใบนี้คือ `RE-083`** · **เลขว่างถัดไป = 084**

### ที่มา
รอบ `ywm4v1` ยก `mob_aggro` ขึ้น production ตาม `COO-DECISION 2026-08-26T04:02+07:00` และสร้าง `src/pirateforce_foundation/mob_ai_control.py` — ตัวคุมชุดเดียวของสถานะ AI
ลูปตัดสินใจนั้นออก **intent** ได้สามอย่าง และวันนี้ **ส่งไม่ได้สักอย่าง**:

| intent | ประตู | สถานะ |
|---|---|---|
| `INTENT_ATTACK_UNDELIVERABLE` | **Door B (ATTACK)** | ปิดสนิท · ไม่มี capture ไม่มี encoder · `ATTACK_INTENT_DELIVERABLE = False` |
| `INTENT_FACE_AND_APPROACH` | **ใบนี้** | 🔴 **ไม่รู้ และไม่เคยมีใครถาม** |
| `INTENT_RETURN_TO_LEASH` | **ใบนี้** | 🔴 เหมือนกัน |

🔴 **ประเด็นทั้งใบคือประโยคเดียว:** *การเดินเข้าหา ไม่ใช่ Door B*
Door B คือการ **โจมตี** (`CActorTask_UseBehavior` / `PlayActionEvent`) · การ **ย้ายตำแหน่ง** เป็นคนละกลไก และเราอาจถือกุญแจอยู่แล้วโดยไม่รู้ตัว
ถ้าคำตอบของใบนี้คือ "เดิน" ⇒ **`v5` มีอะไรให้ *ดู* ไม่ใช่แค่ให้ *วัด*** โดยไม่ต้องรอ Door B เลย

### 🔴 ของที่วัดไว้แล้ว ห้ามขุดซ้ำ (ประหยัดครึ่งใบ)
- **`GT-030` (2 รอบ) พิสูจน์แล้วว่า `actor_type 2` (CNetActor) เรนเดอร์บนจอได้จริง** — ตายแล้วเป็นศพ มีอนิเมชัน ~0.7 วิ เปิด target panel ด้วยคลิกเดียวได้
- **`GT-035` (25 ส.ค.) พิสูจน์แล้วว่า actor frame ที่ส่งซ้ำ *เปลี่ยนค่าในตัว actor ที่เห็นอยู่* ได้จริง** — บาร์เลือดเดิน `3857 -> 2893 -> 2893 -> 771` จากคู่เฟรม (announce, actor) ⇒ **ช่องทาง "รีเฟรช body ของ actor ที่ยืนอยู่แล้ว" เปิดอยู่และวัดแล้ว** · ใบนี้ถามแค่ว่า **ช่องเดียวกันนี้พาฟิลด์ตำแหน่งไปด้วยได้ไหม และไคลเอนต์ตีความยังไง**
- **`docs/FUNCTIONAL_COVERAGE.json` แถว `npc_locomotion_presentation` = `runtime_pass`** — 🔴 **แต่ต้องอ่าน notes ของมันก่อน ห้ามอ่านแค่สถานะ**: มันพูดถึง **การเลือก gait (เดิน/วิ่ง) จากค่าความเร็วใน `BasicAttr` bit `0x0040`** เท่านั้น และเขียนไว้เองว่า *"it is not a general locomotion or pathing engine"* และ *"the Foundation population path never requests a movement speed"*
  ⇒ **สิ่งที่แถวนั้นให้เราคือ: ไคลเอนต์มีทางแสดงการเคลื่อนที่ของ actor ที่เรา project และมันอ่านความเร็วจากเรา** — ไม่ใช่คำตอบของใบนี้
- **`teleport_transport` = `runtime_pass` เป็นคนละเรื่อง** — มันย้าย **ไคลเอนต์ของผู้เล่นเอง** ไม่ใช่ NPC ที่เรา project · ห้ามอ้างเป็นหลักฐานของใบนี้
- **แถวจริงมี `n_SPEED_WALK` และ `n_SPEED_RUN`** ใน `CONSTDATA_TH__MOBS` (=100 สำหรับทั้ง 13 ตัวของ `bg0001` ในคอลัมน์ walk) และ `field_mobs.FieldMob` ขนคอลัมน์ walk มาแล้ว

### objective (claim เดียว)
**จากอิมเมจไคลเอนต์ล้วน ๆ:** ตอบว่า เมื่อ actor ที่มีอยู่แล้วบนจอ (`actor_type 2`) ได้รับ body ที่ **ฟิลด์ตำแหน่งเปลี่ยนไป** ไคลเอนต์
**(ก)** ตั้งค่าตำแหน่งทันที (กระตุก/teleport) · **(ข)** ตั้งเป็น "เป้าหมายการเดิน" แล้วเดินไปเองด้วยความเร็วที่รู้จัก · **(ค)** เพิกเฉยเพราะการเคลื่อนที่ของ actor ต้องมาจากช่องทางอื่น

### จ็อบ (ลำดับบังคับ · หยุดได้ทุกจุดถ้าชนเพดาน static — เขียน bounded negative แล้วปิด)
- **T0 · ด่านคุม** — ระบุว่าฟิลด์ตำแหน่งของ actor body ตกลงที่ **offset ไหนของ actor object** และ **ใครอ่านมันในเฟรมเรนเดอร์** · ถ้าเส้นนั้นอ่านไม่ออกจาก static **หยุดทั้งใบ** ผลที่เหลืออ่านไม่ได้
- **T1** — เส้นทางเขียน: ตัวรับ body เขียนตำแหน่งลง **ช่องเดียวกับที่เรนเดอร์อ่าน** หรือลง **ช่อง "เป้าหมาย" แยก** · **นี่คือคำถามที่ตัดสินทั้งใบ** — สองช่อง = (ข) · ช่องเดียว = (ก)
- **T2** — ถ้ามีช่องเป้าหมายแยก: อะไรกินมัน · มี task/updater ที่เดินตัว actor เข้าหาเป้าหมายไหม (ตัวเทียบที่ควรไล่คือ task ตระกูลเดียวกับ `CActorTask_Dead` ที่ `RE-071`/`MOB-DEATH-001` ไล่ไว้แล้ว — ใช้ vtable เดียวกันเป็นทางเข้า)
- **T3** — ความเร็วมาจากไหน: `BasicAttr` bit `0x0040` (ตามแถว coverage) หรือค่าใน object · และ **ถ้าไม่ส่ง มันใช้ค่าอะไร** — แถว coverage เขียนว่าการไม่ส่งความเร็ว **ทำให้ท่าเดินกลายเป็นวิ่ง** ⇒ ถ้าเป็น (ข) จริง เราต้องส่งความเร็วด้วยทุกเฟรม ไม่ใช่แค่ตอน bootstrap
- **T4 · ริเดอร์** — ถ้าเป็น (ก) กระตุก: **ความถี่สูงสุดที่ยังดูเป็นการเคลื่อนที่ ไม่ใช่การกระพริบ** คือเท่าไร มีตัวจำกัดฝั่งไคลเอนต์ไหม
  🔴 **ริเดอร์นี้ระวัง:** `COO-DECISION 2026-08-26 07:45` **คว่ำ** `mob_loot.DROP_REFRESH_MS = 80` ไปแล้วครั้งหนึ่ง ⇒ ผลของ T4 **ไม่ใช่ใบอนุญาตให้ส่งถี่** ต้องผ่าน COO ก่อนเสมอ

### สิ่งที่สาย B ตัดสินไปก่อน (ห้ามอ่านว่านี่คือคำตอบ)
**[สมมติของสาย B - รอ COO/RE ยืนยัน]** เลนนี้ **ไม่ได้สมมติอะไรเลยในโค้ด** — `mob_ai_control` **ไม่ประกอบเฟรมการเคลื่อนที่ และไม่มีฟังก์ชันที่จะประกอบ**
⇒ intent ทั้งสองยังเป็น **การตัดสินใจที่ไม่มีทางส่ง** เหมือนเดิม และโมดูลเขียนไว้ตรง ๆ ว่ามันไม่อ้างพิกเซลใดทั้งสิ้น
⇒ **ใบนี้จึงไม่บล็อกอะไรของรอบก่อนหน้า** — มันเปิดของใหม่ ไม่ได้ค้ำของเก่า

### nonclaims ที่ต้องติดไปกับผลทุกกรณี
① ใบนี้ **ไม่เปิด Door B** — ตอบว่าเดินได้ ก็ยัง **ตีไม่ได้** · `ATTACK_INTENT_DELIVERABLE` ไม่ขยับด้วยใบนี้ไม่ว่าผลจะเป็นอะไร
② ใบนี้ **ไม่ยกเพดานหลักฐานของ `MOB-AGGRO-001`** — `mob_aggro_and_server_ai` ยังเป็น `not_started` จนกว่าจะมีคนดูจอเห็นไคลเอนต์ตอบเฟรมที่เราส่ง (กฎ round-98)
③ ใบนี้ **ไม่ตัดสินเรื่อง pathing** — ถ้าคำตอบคือ (ข) มันบอกว่าไคลเอนต์เดินไปที่จุดหนึ่ง **ไม่ได้บอกว่ามันหลบสิ่งกีดขวางเป็น**
④ ใบนี้ **ไม่ได้ถามว่ามอนสเตอร์ควรเดินเมื่อไร** — นั่นคือ `mob_aggro.tick` ซึ่งตอบไปแล้ว · ใบนี้ถามแค่ว่า **บอกให้มันเดินได้ไหม**
⑤ 🔴 **และผลลัพธ์ที่เป็นไปได้มากที่สุดตามข้อมูลจริง ต้องเขียนติดไปด้วย:** มอนสเตอร์ **10 จาก 13 ตัวของ `bg0001` มี `n_OFFESIVE = 0` และ `n_AGGRO = 0`** (`field_mob_ai_tables`) ⇒ **มันจะไม่เดินเข้าหาใครอยู่แล้ว** ⇒ ต่อให้ใบนี้ตอบว่า "เดินได้" สิ่งที่ผู้เล่นเห็นคือ **สามตัวเดิน ไม่ใช่ทั้งสนาม** — ห้ามใครสรุปเป็นอย่างอื่น

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจอ่านอย่างเดียว · ทุก VA มี ImageBase `0x400000` กำกับ · ทุกข้อสรุปมี provenance (VA + วิธีที่ได้มา) · ชนเพดานให้เขียน **bounded negative** แล้วปิด **ห้ามเดาต่อ** · **ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**

### เกณฑ์จบใบ
ตอบ T1 ได้ (ตำแหน่งลงช่องเรนเดอร์ หรือช่องเป้าหมาย) **หรือ** เขียน bounded negative ว่าเพดาน static อยู่ตรงไหน ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

### สิ่งที่ใบนี้ *ไม่* ทำ
ไม่แตะโค้ดเซิร์ฟเวอร์ · ไม่เปิดเกม · ไม่ตัดสิน opcode · ไม่ยุบรวมกับ `RE-065` (Door B) — **คนละประตู และนั่นคือทั้งหมดของใบนี้**

### result (ยังไม่มี — ใบเปิดอยู่)
