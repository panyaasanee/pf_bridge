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
## 🆕🔬 RE-095 NPCCONVERSATION-COLUMBUS-QUESTID-CROSSWALK-001 [STATIC-ON-BRIDGE]: **หา quest id / nested descriptor (u16 `+0x10`, u8 `+0x12`) ที่ NPC Columbus ใช้จริงใน `NPCConversation`, แยกจาก quest `3020` (actor `0x2001`/P0 singleton) ที่เซิร์ฟเวอร์ hardcode อยู่ตอนนี้**  [🔴 **CLOSED superseded-in-applicability — ปิดโดย LANE-A (สาย A · WORLD) รอบ `kqrlhr` 2026-08-27 ~14:2x (+07:00), ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `GT-095`/`RE-095` = **0 hit ทั้งสองไฟล์** ⇒ **ใบนี้คือ `RE-095`** · เลขว่างถัดไปหลังใบนี้ = 096
> 🔴 ใบ `RE-085`-`RE-094` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`RE-094` result (`notes_to_chief/20260827_0156_RE-094-RESULT-OP1-USES-DYNAMIC-QUEST-ID.md`) พิสูจน์ว่า
`QuestOperateVital op=1` เป็น generic dispatch — client อ่าน quest id แบบไดนามิกจาก UI record `+0x94` ไม่ได้
hardcode `3020` ในไบนารี และ `NPCConversation` เขียน actor qword ที่ `+0x18` กับ nested descriptor ที่มี quest
id u16 ที่ `+0x10` และ u8 ที่ `+0x12` แต่ RESULT เขียนตรงๆ ใน nonclaims ว่า **"ไม่ได้พิสูจน์ quest id ของ Columbus
หรือ descriptor byte `+0x12`"** — เซิร์ฟเวอร์ปัจจุบัน (`current/pf_login_game_server_v141.py:768-798`) สร้าง
descriptor เฉพาะ `qid=3020` บังคับ actor `0x2001` (=P0) เท่านั้น ไม่มีพารามิเตอร์ให้สลับเป็น Columbus

RESULT เดียวกันยังพบว่า `QUESTDATA_TH__QUEST.tsv` มี quest `3020` (`Q_TELEPORT_WITH_VEHICLE1`) และ "quest
vehicle อื่น `3301..3303` พร้อม quest text ต่างกัน" — นี่เป็น candidate ที่ยังไม่ตรวจ ไม่ใช่คำตอบ

### objective (claim เดียว)
ระบุว่า NPC Columbus (ตัวจริงตามคำอธิบายเจ้าของ "จุดเดียวที่ท่าเรือ", ดู `RE-093` rider สำหรับสถานะที่ยังไม่พบ
placement ของ Columbus ใน block เดียวของ `bg0001`) ใน `NPCConversation` ของไคลเอนต์ใช้ quest id ใด (จาก
`{3020, 3301, 3302, 3303}` หรือค่าอื่น) ที่ descriptor `+0x10`/`+0x12` ต้องใส่ เพื่อให้ op1 ที่เซิร์ฟเวอร์ตอบกลับ
นำไปสู่ลำดับที่ตรงกับคำอธิบายเจ้าของ (`notes_to_chief/20260826_1600_PANYA-DECISION-*.md`: เรือ → เทียบท่า →
หน้าต่างรายงานกัปตัน)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยันว่า `QUESTDATA_TH__QUEST.tsv` แถว `3301`-`3303` มี field ที่ระบุ NPC ผู้มอบเควสต์/
  บทสนทนา (giver NPC id หรือ dialogue key) ให้เทียบกับ Columbus
- **T1** — ถ้ามี giver NPC field: เทียบกับ template/actor id ของ Columbus ตรงกันหรือไม่ (ขอบเขต placement
  ของ `bg0001` = block เดียว 149 placements ตาม `RE-093` result — ห้ามสมมติ block ที่สอง)
- **T2** — ถ้าไม่มี giver field ใน gamedata: ค้น call sites ของ `NPCConversation` constructor/serializer
  (`0x622A00`/`0x622F10`) ในไคลเอนต์ ว่ามี lookup ตัวไหนผูก actor Columbus กับ quest id ที่ไม่ใช่ `3020`
  หรือไม่ (bounded — ไม่ต้อง exhaustive ทั้งไบนารี)
- **T3 · ริเดอร์** — ถ้าเวลาเหลือ: server reply sequence ที่ op1 คาดหวังสำหรับ quest ที่ไม่ใช่ `3020` (action6
  เดิม หรือ opcode อื่น) ระบุแค่ระดับ field ไม่ต้อง implement

### nonclaims
① ไม่อ้างว่า `3301`-`3303` คือคำตอบแน่นอน — เป็นแค่ candidate ที่ `RE-094` result ทิ้งไว้ ② ไม่ตัดสินว่า
`src/pirateforce_foundation/` ต้องเปลี่ยนโครงสร้างอย่างไร — สาย A ตัดสินใจเองเมื่อได้ข้อมูล ③ ไม่ปิดคำสั่ง
`COO-DECISION 1645` ข้อ 3 เอง — ใบนี้ตอบแค่ชั้น wire/data ไม่ใช่ทั้งเส้นทาง M2 ④ ถ้าเพดาน static ชนก่อนตอบได้
ให้เขียน bounded negative ตามกฎ ไม่เดาต่อ

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์ gamedata อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative
แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ตอบ T0/T1 ด้วยหลักฐาน (quest id ที่ผูกกับ Columbus จริง) **หรือ** bounded negative ว่า gamedata/ไคลเอนต์ไม่มี
crosswalk นี้ ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

### result — CLOSED superseded-in-applicability (ไม่ใช่ผิด — คนละ NPC)

รายละเอียดเต็ม: `notes_to_chief/20260827_0310_RE-095-RESULT-COLUMBUS-QUEST-3023.md`. RE runner ตอบ T0/T1
ด้วยหลักฐานจริง: `MOBS.n_ID=36` (`s_NAME=Columbus`, `s_TITLE=Marine Transport Station`) ใช้ quest `3023`
(`Q_TELEPORT1`, `n_VARI_2=19` -> scene 19/`Bg1003`) — คำตอบระดับ static/gamedata ถูกต้องและยืนอยู่จริง

**แต่ใบนี้ตอบผิด NPC สำหรับ Port Royal**: เจ้าของยืนยันในรอบถัดมา (`20260827_0925`/`0950_PANYA-DECISION`)
ว่า Columbus ตัวจริงของ Port Royal คือ `MOBS.n_ID=156` (bg0001 placement index 1) ไม่ใช่ `n_ID=36` — ทั้งสอง
แถวชื่อ "Columbus" เหมือนกันทุกตัวอักษร (`s_NAME`/`s_TITLE`/`s_ROLE_TALK=COLUMBUS_0` เหมือนกันหมด) เป็น NPC
คนละตัวที่ใช้ชื่อ/โมเดล/เสียงซ้ำกัน (ปรากฏการณ์ทั่วไปของเกมนี้ — ดู `world_travel_gates_001.json`) `MOBS 156`
ใช้ quest `3021` (`n_VARI_2=17` -> scene 17/`Bg1001`) ซึ่งเป็นคนละเควสต์คนละฉากกับที่ใบนี้ปิดไว้

**แก้แล้วที่ไหน**: การแก้ไขนี้เข้า `pirate-force-server` ตั้งแต่ PR `#107` (round `8pfksm`, merge `b35384a3`)
— `scenarios/world_travel_gates_001.json` และ `scenarios/world_scene_registry_001.json` pin ทั้งสองแถวไว้
ชัดเจนพร้อม cross-reference ("Quest 3023 is real but is MOBS n_ID 36's quest ... not Port Royal's"),
`columbus_quest_dispatch.py` (`CORE-REQUEST-014`) และ `tests/test_world_columbus_m2_crosswalk.py` ผูกกับ
`3021`/`156`/scene 17 เท่านั้น — โค้ดที่ส่งจริงไม่เคยใช้ `3023` ของใบนี้

BUILD_IMPACT: ไม่มี — ข้อเท็จจริงของ RE-095 (MOBS 36 -> quest 3023 -> scene 19) ยังคงจริงและยัง pin ไว้ใน
`world_scene_registry_001.json`/`world_travel_gates_001.json` เป็นบันทึกแยกแยะ "อย่าใช้เควสต์นี้กับ Columbus
ตัวจริง" แต่ไม่มีอะไรใน `src/pirateforce_foundation/` ที่เคยพึ่งค่านี้ให้ต้องแก้ย้อนหลัง — สาย A ปิดใบนี้เป็น
mailbox consumption เท่านั้น ไม่มีโค้ดเปลี่ยนจากผลใบนี้โดยตรง (โค้ดแก้ไปแล้วตั้งแต่ PR #107 ก่อนหน้านี้)

---

## 🆕🔬 RE-096 VEHICLE-ROW-SEASCENE-CROSSWALK-001 [STATIC-ON-BRIDGE]: **หา `VEHICLE` table row + ความหมายของ `CVehicleVital.+0x18` qword ที่ผูกกับกลุ่มฉากทะเล (`Bg1001`-`Bg1007`, `SCENE_TYPE=4`)**  [🔴 **CLOSED bounded-negative — ปิดโดย LANE-A (สาย A · WORLD) รอบ `kqrlhr` 2026-08-27 ~14:2x (+07:00), ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `GT-096`/`RE-096` = **0 hit ทั้งสองไฟล์** ⇒ **ใบนี้คือ `RE-096`** · เลขว่างถัดไปหลังใบนี้ = 097
> 🔴 ใบ `RE-085`-`RE-095` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`RE-085` result (`notes_to_chief/20260827_0156_RE-085-RESULT-SAME-ACTOR-VEHICLE-MODULE.md`) พิสูจน์ actor-local
vehicle binding (`CGCVehicleModule` ผูก actor เดิมกับ `CVehicleAttr` ที่มีอยู่แล้ว ไม่สร้าง actor เรือแยก) แต่
nonclaims เขียนตรงๆ ว่า **"ไม่ได้พิสูจน์ ship model/vehicle row ที่ใช้จริง"** และ `BUILD_IMPACT` บอกว่า "ต้องหา
crosswalk จริงจาก sea-scene/quest response ไป vehicle row และความหมาย `CVehicleVital.+0x18`" — ตาราง
`VEHICLE` มี 79 rows แยกต่างหากจากตาราง `SCENE_NAME` (rows 17-23 = sea family, `n_SCENE_TYPE=4`,
`n_CANRIDE=0`) ไม่มี crosswalk field ที่ผูกสองตารางนี้เข้าด้วยกันที่ `RE-085` เจอ

### objective (claim เดียว)
ระบุ `VEHICLE` table row (จาก 79 rows) ที่ตรงกับ "เรือ" ที่ผู้เล่นควรได้ใน sea scene family (`Bg1001`-`Bg1007`)
และความหมายจริงของ qword ที่ `CVehicleVital.+0x18` (vehicle catalog id? model id? หรืออื่น)

### จ็อบ
- **T0** — กรอง `VEHICLE` table 79 rows หา row ที่ประเภท/ชื่อตรงกับ "เรือเดินทะเล" (ไม่ใช่ม้า/พาหนะบก) เทียบ
  column ที่มีอยู่ (model, ประเภท, ความเร็ว ฯลฯ)
- **T1** — ถอด write site ของ `CVehicleVital` handler (`0x00710440`) ว่าค่า `+0x18` ถูกใช้ทำอะไรต่อ (lookup
  table ไหน, index เข้าโมเดล/แอนิเมชันอะไร) เพื่อยืนยันว่าเป็น vehicle row id จริงหรือความหมายอื่น
- **T2 · ริเดอร์** — ถ้าเวลาเหลือ: ตรวจซ้ำว่า `SCENE_NAME` rows 17-23 มี column ใดอ้างถึง `VEHICLE` row
  โดยตรงหรือไม่ (เน้น column ที่ `RE-085` ยังไม่ได้ dump ทั้งหมด)

### nonclaims
① ไม่อ้างว่าเรือต้องเป็น row เดียวตายตัว — อาจมีมากกว่าหนึ่ง row ที่ใช้ได้ (เช่นตามแฟกชัน/ระดับผู้เล่น) ② ไม่
ตัดสินโครงสร้าง `src/pirateforce_foundation/` เอง ③ ถ้าเพดาน static ชนก่อนตอบได้ ให้เขียน bounded negative
ตามกฎ ไม่เดาต่อ

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์ gamedata อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative
แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ตอบ T0/T1 ด้วยหลักฐาน (vehicle row + ความหมาย `+0x18`) **หรือ** bounded negative ว่า gamedata/ไคลเอนต์ไม่มี
crosswalk นี้ ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

### result — CLOSED bounded negative, T0/T1 negative, T2 rider negative

รายละเอียดเต็ม: `notes_to_chief/20260827_0509_RE-096-RESULT-NO-VEHICLE-SEASCENE-CROSSWALK.md`. สรุป:

- **T0** [bounded negative]: ตาราง `VEHICLE` จริงมี 79 แถวแต่มีแค่ `n_ID`/`n_PROPERTIES`/`n_SEATS`/
  `s_NAMEBOARD`/`n_SEAT1..6` — ไม่มี model/type/speed/scene column ตามที่จ็อบคาดไว้เลย ข้อมูลเรือจริง
  (`n_SHIP_VELOCITY`, `s_OUTFIT`, ชื่อเรือ) อยู่ใน **ตาราง `SHIP` แยกต่างหาก** (17 แถว) ที่ไม่มี field ผูกกลับ
  ไป `VEHICLE` หรือไป sea scene family เลย id ที่ซ้ำกันบังเอิญระหว่างสองตาราง (`11,12,101,102,103`) ถูก
  ตัดทิ้งตามกฎ ไม่ join จากเลขบังเอิญ
- **T1** [bounded negative]: `CVehicleVital` handler `0x00710440` ถูก SHA-pin เป็น 5 ไบต์ `mov al,1; ret 4`
  เท่านั้น — ไม่อ่าน/เขียน/lookup อะไรเลย capture ยัง `NOT_OBSERVED` ทั้งสองทิศทาง (0/0 เฟรม) จึงตั้งชื่อ
  semantic ให้ qword `+0x18` ไม่ได้ (ไม่ใช่ vehicle id, model id หรืออื่นใด — ยังคง `UNKNOWN`)
- **T2 rider** [bounded negative]: `SCENE_NAME` rows 17-23 (sea family) ไม่มี field อ้าง `VEHICLE`/`SHIP` ใดๆ

**สิ่งที่ตัดทิ้งชัดเจน (ห้ามสับสนซ้ำ)**: `CGCVehicleModule`/`CVehicleAttr` (คนละ object จาก `CVehicleVital`)
มี helper ที่สแกน `+0x18..+0x47` เพื่อเช็คว่าง — เลข offset `+0x18` ที่ตรงกันข้าม type **ไม่ใช่ crosswalk**

BUILD_IMPACT: guard เชิงโครงสร้างสำหรับสาย A/เซิร์ฟเวอร์ — scene 19/`Bg1003` ≠ vehicle id, `VEHICLE` ≠ `SHIP`,
`CVehicleVital.+0x18` ต้องคงชื่อ `UNKNOWN_QWORD` จนกว่าจะมี capture จริง ~~`columbus_quest_dispatch.py`
(chief, `CORE-REQUEST-014`) ใช้ผลนี้ตรงๆ อยู่แล้ว: `VEHICLE_BIND_REFUSED_NO_VEHICLE_ROW` ยังคง refuse
เหมือนเดิม — ปิดใบนี้ไม่ปลดล็อกอะไร~~ ทางเดียวที่เหลือคือ attended capture ของ
`CVehicleVital` เฟรมจริง ไม่มีเส้นทาง static เพิ่มเติมในข้อมูลที่ commit ไว้ (COO-DECISION `20260827_1350`
เร่งใบนี้เป็นลำดับสูงสุดของ RE runner ก่อน 20:00 — ปิดทันตามกำหนด)

> **UPDATE (สาย A รอบ `jafskv`, 2026-08-27T17:37+07:00)**: บรรทัดที่ขีดฆ่าข้างบนล้าสมัยแล้ว —
> `M2-NO-VEHICLE-OWNER-20260827-1525` (`notes_to_chief/20260827_1525_PANYA-DECISION-M2-accept-scene17-entry-without-vehicle-fix-later-*.md`)
> ถอด `VEHICLE_BIND_REFUSED_NO_VEHICLE_ROW` ออกจากจุดเรียกใช้ทั้งหมดใน `columbus_quest_dispatch.py` แล้ว
> (ค่าคงที่ยังอยู่ในไฟล์แต่เป็น dead code — grep ยืนยัน 0 call site) ฟังก์ชันนี้**ไม่ refuse ด้วยเหตุผลนี้อีก
> ต่อไป** — M2 ไม่ต้องรอ vehicle-bind ปิดแล้วตามคำเคาะเจ้าของ ผลลัพธ์หลักของใบนี้ (T0/T1/T2 bounded-negative
> + "ทางเดียวที่เหลือคือ attended capture") **ยังยืนอยู่เหมือนเดิม ไม่เปลี่ยน** — เปิดใบเทส `GT-109` แล้วรอ
> capture ตามนั้น

---

## 🆕🔬 RE-097 COLUMBUS-BG0001-PLACEMENT-IDENTITY-001 [STATIC-ON-BRIDGE]: **หา placement/actor identity ของ Columbus (`MOBS.n_ID=36`) ใน 149 plac... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-098 FIELD-MOB-DEFINITION-PAYLOAD-LEVEL-RANK-001 [STATIC-ON-BRIDGE]: **หา parser สำหรับ definition payload 16 ไบต์ต่อ `.npc` (`b5`/`b15... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-100 SETNUMBER-99-101-SENTINEL-AND-ACTORMOVE-MULTIPOINT-001 [STATIC-ON-BRIDGE]: **เลขชุด `99`/`101+` ที่แทรกกลางลำดับ `.npc` มีความหมายพิเศษฝั่งไคลเอนต์ไหม + `CActorTask_ActorMove` (ผู้บริโภคที่ `RE-083` พิสูจน์แล้วสำหรับ `actor_type 2`) กินลิสต์ XYZ หลายจุดเป็นคิวได้จริงหรือรับได้แค่จุดเดียวต่อครั้ง**  [🔴 **CLOSED bounded-negative — ปิดโดย LANE-A (สาย A · WORLD) รอบ `kqrlhr` 2026-08-27 ~14:2x (+07:00), ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `GT-099` มี **1 hit** ใน `GAME_TEST_QUEUE.md` (บรรทัด 7807, `GT-099 BACKPACK-LOAD-REFUSED-001`) — `RE-099` เองมี **0 hit** ทั้งสองไฟล์ แต่เลข `RE`/`GT` ใช้ตัวนับร่วมกัน (ห้ามแยกตัวนับ ตามกติกาเดิมของไฟล์นี้) ⇒ hit ฝั่ง `GT-099` พอแล้วที่จะทำให้ `099` ถูกจองไปแล้ว ⇒ ข้ามไปที่ `RE-100`/`GT-100` = **0 hit ทั้งคู่ ทั้งสองไฟล์** ⇒ **ใบนี้คือ `RE-100`** · เลขว่างถัดไปหลังใบนี้ = 101
> 🔴 ใบ `RE-085`-`RE-098` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260827_0833_LANE-A-REPLY-PANYA-ORDER-npc-scene-file-dataset-interpretation.md` — สาย A ทำ
`PANYA-ORDER 0440` (ตีความชุดข้อมูล `.npc` ของฉากเมือง) แบบ static/read-only จากของที่ commit ไว้แล้วเท่านั้น
(ไม่มีเครื่อง `GameClient.local.bin` ใน cloud clone นี้) ตอบได้สามใน สี่ข้อบางส่วน (① วัดได้ว่าไม่มี Lua/table
ไหน crosswalk เลขชุดเลย — 0 hit ทั่ว `gamedata/lua`+`gamedata/tables` ② วัดได้บางส่วนว่า 7/11 เส้น extra-triple
วนกลับเป็นวงปิด แต่ 4/11 ไม่วน ③ วัดได้ว่า `version2_byte`/`b5`/`b15` ไม่มีเอกสาร commit ไหนอธิบายความหมาย และ
สมมติฐาน level/rank/spawn-rate ถูก `RE-098` หักล้างไปแล้ว) แต่สองเรื่องต้องใช้เครื่องบริดจ์จริงถึงจะปิดได้ —
เปิดเป็นใบนี้แทนการเดา

### objective (สองคำถามในใบเดียว เพราะทั้งคู่ต้องใช้ recursive CFG ของ `.npc` loader/`CActorTask_ActorMove`
เครื่องเดียวกัน)
1. โค้ดฝั่งไคลเอนต์ที่ parse/ใช้ "เลขชุด" (`payload u32@+1` ของ `.npc` definition) แยกกรณี `99` (แทรกกลาง
   ลำดับ ไม่ใช่ท้ายไฟล์ ใน 7 ฉากใหญ่) และ `101+` (พบเกือบทุกฉากใหญ่ ไม่พบในฉากทะเล/ฉากเล็ก) ออกจากช่วง `1..N`
   จริงหรือไม่ — ถ้าจริง แยกยังไง (branch เงื่อนไข / ตารางแยก / flag บิตอื่น)
2. `CActorTask_ActorMove` (ctor `0x00472A20`, updater `0x004799C0`/`0x00479C00` ตามที่ `RE-083` ถอดไว้แล้ว)
   หรือ caller ของมัน รับปลายทางได้กี่จุดต่อ task — จุดเดียวคงที่ หรือมีช่องสำหรับลิสต์/คิวปลายทางที่ผูกกับ
   placement ที่มี `extra_triple_count > 0` (`Mob_Set_44`/`Mob_Set_102` ใน `bg0001`, index
   `43,128,129,130,131,133,134,135,136,137,138`)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA ตรงกับที่ `RE-083` ใช้ (`GameClient.local.bin`, ImageBase `0x00400000`,
  size `14,759,424`) ก่อนอ้างอิง span เดิมซ้ำ
- **T1** — ตาม `.npc` definition loader (จุดที่อ่าน `payload u32@+1`) หา branch/compare ที่เทียบค่ากับ `99`
  หรือช่วง `>=101` โดยตรง ถ้าไม่พบในเส้นทางที่ recursive CFG ครอบคลุม ให้เขียน bounded negative
- **T2** — เปิด recursive CFG ของ `ACTORMOVE_CTOR`/`ACTORMOVE_BEGIN_UPDATE`/`ACTORMOVE_STEP`
  (`0x00472A20`, `0x004799C0`, `0x00479C00` — span เดิมของ `RE-083`) หาว่ามี array/count field ที่เก็บ
  ปลายทางมากกว่าหนึ่งจุดไหม หรือ struct มีที่ว่างสำหรับจุดถัดไปหลัง `task+0x48`
- **T3** — ถ้า T2 ตอบว่าจุดเดียว ให้ระบุว่า caller ฝั่งไหน (loader ตอนโหลดฉาก / AI tick) เป็นผู้ตัดสินใจเรียก
  ซ้ำเพื่อเดินหลายจุด ถ้ามี ให้ระบุ span นั้นด้วย ถ้าไม่พบเลยให้ bounded negative ว่า "ไม่มี auto-patrol ฝั่ง
  ไคลเอนต์ ต้องเดินสายจากเซิร์ฟเวอร์เอง"

### nonclaims
① ไม่อ้างว่า extra-triple ต้องเป็นเส้นทางเดินแน่นอน — ใบนี้ตอบแค่ "ไคลเอนต์รองรับหลายจุดไหม" ไม่ตัดสินความ
ตั้งใจของดีไซน์ ② ไม่ยกผลของใบนี้ไปแทนที่ข้อสรุปเรื่อง Columbus index 0/1 ที่ยังค้างอยู่ (ดู
`20260827_0505_ATTENDED-ADDENDUM-...`) — คนละคำถามกัน ③ ถ้า T1/T2 หาไม่เจอในเส้นทางที่ถอดได้ ห้ามเขียนว่า
"ไม่มีทั่วทั้ง image" — เขียนแค่ "ไม่พบในเส้นทางที่ recursive CFG ครอบคลุม" ตามกติกาเดิมของ `RE-083`

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์ scene/gamedata อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded
negative แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ตอบ T0-T3 ด้วยหลักฐาน (spans ที่ถอดครบ + คำตอบมี/ไม่มี branch หรือ multi-point field) **หรือ** bounded
negative ครบทั้งสองคำถาม ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

> 🔧 **แก้ misplacement (Lane A, mailbox-consumption รอบ `kqrlhr`, 2026-08-27 ~14:2x +07:00):** placeholder
> นี้เคยถูกเขียนทับด้วยผลของ `RE-102` (คนละใบ) ตั้งแต่รอบ `pvbj0u` — ย้ายเนื้อหานั้นไปไว้ใต้หัวใบ `RE-102`
> เอง (ที่ถูกที่) แล้วในรอบนี้ ด้านล่างนี้คือผลจริงของ `RE-100`

### result — CLOSED bounded negative, T1/T3 negative, T2 answered one-point

รายละเอียดเต็ม: `notes_to_chief/20260827_0918_RE-100-RESULT-NO-SENTINEL-BRANCH-ACTORMOVE-ONE-POINT.md`.
image SHA `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` ตรงกับ `RE-083`. สรุป:

- **T1** [bounded negative]: recursive CFG ของ definition loader (`0x00439E90`) + scene consumer
  (`0x0043A9D0`) + template dispatch (`0x0043A6F0`) ที่ผูกกันจริงครบ 6 span ไม่มี `cmp/test/sub` เทียบค่า
  `99`, `101` หรือขอบรอบนั้นเลยสักจุด — loader อ่าน payload `u32@+1` เข้า definition object `+0x30` แล้วส่ง
  ต่อ generic dispatch โดยไม่มี branch sentinel คั่นระหว่างทาง raw `bg0001.npc` (positive control) มีค่า `99`
  และ `101..113` จริง จึงเป็น control ที่พิสูจน์ว่าค่าผ่าน loader เดียวกัน ไม่ใช่ path คนละเส้น
- **T2** [ตอบชัด — one point]: `CActorTask_ActorMove` เป็น object ขนาด `0x58`; destination เดียวอยู่ที่
  `task+0x40/+0x44/+0x48` เท่านั้น `+0x4C` เป็น scalar แยก และ `+0x50..+0x55` เป็น byte flags ไม่มีพื้นที่
  เหลือสำหรับจุดที่สอง constructor `0x00472A20` + updater `0x004799C0`/`0x00479C00` (span เดิมของ `RE-083`)
  อ่าน/เขียนสูงสุดแค่ `+0x55`
- **T3** [bounded negative]: extra-triple codec (`0x00439450`) อ่าน `u16 count` + `f32 x/y/z` เป็น list จริง
  (ไม่ใช่ decoder artifact) แต่ recursive CFG ของ codec/placement-reader/loader/dispatch/scene-consumer ไม่มี
  call ไป `CActorTask_ActorMove` ctor เลย เส้นเดียวที่พิสูจน์ว่าสร้าง task ซ้ำคือ `CNetActor` network-target
  consumer (`0x00459160`) ซึ่งรับจุดใหม่ทีละจุดจากภายนอก ไม่ใช่คิวที่ task ถือเอง

คำว่า BOUNDED สำคัญทั้งสามข้อ: ไม่ใช่คำกล่าวว่า `99/101+`/extra-triple ไม่มีความหมายทั่วทั้ง image — คือไม่พบ
ในเส้นทาง native ที่ระบุและถอดด้วย recursive CFG ครบเท่านั้น

**Action taken ต่อ `PANYA-CHASE 0915`** (จากผลเดิม): RE runner ยืนยันเองว่า RE-100 **ไม่ครอบ** งาน identity
crosswalk ของ placement index → MOBS.n_ID / Hields / Sase / Columbus ที่ `PANYA-CHASE 0915` และ `0310` §①
ถาม — ใบนี้ตอบเฉพาะ 99/101+ native handling กับ ActorMove multi-point เท่านั้น

BUILD_IMPACT: ไม่มีโมดูลใดใน `src/pirateforce_foundation/` ทำ multi-point movement หรือแยก set-number
99/101+ อยู่ตอนนี้ (ตรวจแล้วรอบนี้ — `grep -rn "ActorMove\|multipoint" src/` ว่างเปล่านอกเหนือ docstring ของ
`RE-100` เอง) จึงไม่มีอะไรให้แก้ใน `src/` จากผลใบนี้โดยตรง หากอนาคตมีเลนเดินหลายจุด (เช่น patrol NPC) ต้องส่ง
target ทีละจุดจากฝั่งเซิร์ฟเวอร์เอง ตามที่ T2/T3 พิสูจน์ไว้ — ห้ามผูกเลขชุด 99/101+ เป็น special class จาก
หลักฐานใบนี้

---

## 🆕🔬 RE-103 SCENE17-BG1001-PLAYER-ARRIVAL-SPAWN-001 [STATIC-ON-BRIDGE]: **หาพิกัด/marker จุดที่ผู้เล่นควรปรากฏตัวเมื่อเข้าฉาก 17 (`Bg1001`, ตระกูลทะเล `n_SCENE_TYPE=4`) — `Bg1001.placements.tsv` มีแค่ 8 แถว monster spawn ไม่มี player marker เลย**  [🟢 **OPEN — เปิดโดย chief cloud รอบ `4txjyg` (R192) 2026-08-27 ~12:0x (+07:00) บล็อก `CORE-REQUEST-014`/M2**]

> 🔢 **หมายเหตุเลข (แก้แล้ว — ดู erratum ท้ายบล็อกนี้):** ใบนี้คือ `RE-103` ไม่ใช่ `RE-101` ที่เขียนไว้ตอน
> แรก — ตัวนับ `GT`/`RE` ใช้ร่วมกัน (กติกาเดิมของไฟล์นี้ ตามที่ `RE-100` บันทึกไว้เอง: "hit ฝั่ง GT พอแล้วที่จะ
> ทำให้เลขนั้นถูกจองไปแล้ว") `GT-101` ถูกจองไปแล้วโดยสาย GM ก่อนใบนี้จะถูกเขียน ⇒ `101` ไม่ว่าง และ `RE-102`
> ก็ถูกสาย A จองไปพร้อมกัน (คนละรอบ คนละเซสชัน ชนกันตรง merge) ⇒ เลขว่างจริงคือ `103` เลขว่างถัดไปหลังใบนี้
> = `104`
> 🔴 ใบ `RE-085`-`RE-102` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร
>
> **erratum (chief, ตอนแก้ merge conflict, 2026-08-27 ~12:5x +07:00):** ฉบับแรกของใบนี้เขียนว่า "`RE-101` =
> 0 hit, `GT-101` = มี hit ⇒ ใบนี้คือ `RE-101` (คนละใบกับ `GT-101` ถึงเลขจะซ้ำกัน เพราะ `GT`/`RE` ใช้ตัวนับ
> ร่วมแต่คนละไฟล์/คนละแถว)" — **อ่านกฎเดิมผิด** `RE-100`'s own precedent (`GT-099` มี hit ⇒ ข้าม `099` ทั้งที่
> `RE-099` เอง 0 hit) ชัดเจนอยู่แล้วว่าเลขที่ถูกใช้โดย prefix ไหนก็ตามถือว่าเลขนั้นถูกจองสำหรับทั้งสอง prefix
> ไม่ใช่แค่ prefix เดียวกัน ใบนี้จึงชนกับ `RE-102` (เปิดโดยสาย A รอบ `95lnvp` เกือบพร้อมกัน คนละเหตุผลเดียวกัน
> คือกฎเลขถูกอ่านถูกโดยสาย A แต่ผิดโดย chief) ⇒ renumber เป็น `RE-103` ทั้งบล็อก ก่อน merge เข้า main จริง

### ที่มา
`notes_to_chief/20260827_1052_LANE-A-CORRECTION-columbus-m2-quest3021-not-3023-scene17-not-19.md` (Columbus
156 → quest 3021 → scene 17 ยืนยันระดับ [STATIC] ตาราง gamedata แล้ว) + `src/pirateforce_foundation/
columbus_quest_dispatch.py` (chief cloud รอบนี้ ต่อสาย `CORE-REQUEST-014` — `dispatch_columbus_quest3021()`
เรียก `world_scene_entry.resolve_entry()` จริง แต่ถูกปฏิเสธด้วย `SceneEntryRefused(REFUSED_NO_PINNED_SPAWN)`
เพราะ `scenarios/world_scene_registry_001.json`'s scene-17 entry มี `spawn: null` — ไม่มีใครวัดพิกัดจริง)
ใบนี้คือช่องว่างเดียวที่บล็อกครึ่งการย้ายฉากของ `CORE-REQUEST-014` (อีกครึ่งคือ vehicle bind payload ซึ่งมีใบ
`RE-096` เปิดอยู่แล้ว คนละใบ)

### objective
หาว่าไคลเอนต์/เซิร์ฟเวอร์ต้นฉบับกำหนดจุดที่ตัวละครควรปรากฏเมื่อเข้าฉาก 17 (`Bg1001`) ด้วยกลไกอะไร — ไม่ใช่
monster spawn (มีอยู่แล้ว 8 แถวใน `Bg1001.placements.tsv`, ไม่เกี่ยวกับใบนี้)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA/ตาราง sha256 ที่จะอ้างอิงตรงกับ verifier ปัจจุบันก่อนเริ่ม
- **T1** — เทียบฉากอื่นในตระกูลเดียวกัน (`Bg1002`-`Bg1007`, `n_SCENE_TYPE=4`, scene 18-23) ว่ามี player-arrival
  marker แยกจาก monster placement table หรือไม่ — ถ้ามีฉากใดในกลุ่มนี้ที่เคยมีคนเข้าจริง (login/relogin
  เคยลงเอยที่ฉากนี้) ให้หาว่าพิกัดนั้นมาจากตารางไหน (login-position table แยก, หรือ field อื่นใน
  `CONSTDATA_TH__SCENE_NAME.tsv`/scene descriptor ที่ยังไม่เคยอ่าน)
- **T2** — ถ้า T1 หา pattern เจอ ใช้ pattern เดียวกันดึงพิกัดของ `Bg1001` โดยเฉพาะ พร้อม provenance
  (ไฟล์/แถว/offset) ครบ
- **T3** — ถ้าหาไม่เจอในเส้นทางที่ถอดได้ ให้เขียน bounded negative ชัดเจนว่า "ไม่มี player-arrival marker
  แยกต่างหากสำหรับตระกูลฉากทะเลในข้อมูลที่ commit ไว้ — ต้องใช้การวัดจากไคลเอนต์จริง (attended/RE runner
  เข้าฉากจริงแล้วบันทึกพิกัดที่ปรากฏ)" ไม่เดาพิกัด ไม่ปั้น XYZ

### nonclaims
① ไม่อ้างว่าพิกัดที่เจอ (ถ้าเจอ) ผ่านการยืนยันระดับ wire — ระดับ [STATIC] เท่านั้นจนกว่าจะมี capture จริง
② ไม่ตัดสินว่า `world_scene_entry.resolve_entry`'s refusal ผิด — refusal ถูกต้องแล้วตามกติกาเดิมของมันเอง
(กฎ 2 ในด็อกสตริงของมันเอง) ใบนี้แค่หาข้อมูลที่จะทำให้มันไม่ปฏิเสธอีกต่อไป
③ ถ้า T1-T3 ไม่พบอะไรเลยในเส้นทางที่ถอดได้ นี่คือคำตอบที่สมบูรณ์ (bounded negative) ไม่ใช่ใบที่ค้าง — ปิดได้

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์ scene/gamedata อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded
negative แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
พิกัด player-arrival ของ scene 17 พร้อม provenance **หรือ** bounded negative ที่บอกตรงๆ ว่าต้องใช้ attended
capture ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

### result (ยังไม่มี — ใบเปิดอยู่)

---

## 🔬 RE-104 GM-EDITOR-WIDGET-OPEN-TRIGGER-001 [STATIC-ON-BRIDGE]: **อะไรเปิด/toggle dedicated GM text-editor widget ที่ `RE-091` พิสูจน์แล้วว่าเป็น producer ของ `GM_RunGMCommandVital` (`0x51E9`) — hotkey, เมนู, ไอคอนที่ปรากฏเมื่อ `GM_UpdateGMStateVital` ตั้งสถานะ GM ให้ connection, หรืออื่น**  [🟢 **CLOSED PASS/DONE — ปิดโดย LANE-GM รอบ `kcm8ir` 2026-08-27T16:1x+07:00, ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-104` = 0 hit, `GT-104` = 0 hit ทั้งสองไฟล์ (ยืนยัน
> 2026-08-27). เลขว่างถัดไปหลังใบนี้ = 105 (ถ้ายังไม่มีใบอื่นจองก่อน — grep ซ้ำก่อนใช้เสมอ).
> 🔴 ใบ `RE-085`-`RE-103` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260826_2322_RE-091-RESULT-DEDICATED-GM-UI-NO-CHAT-PREFIX.md` nonclaim ② เขียนไว้เองว่า
"ไม่ claim ว่า UI นี้เข้าถึงได้ใน runtime โดยผู้เล่นทั่วไป หรือ `GM_UpdateGMStateVital` field ใดคือ is_gm/level
— เป็น `RE-089`" -- ไม่ใช่คำถามเดียวกับใบนี้โดยตรง แต่หัวข้อ "แยกจาก main chat และขอบเขต GM state" ของไฟล์
เดียวกัน (คนละย่อหน้า) เขียนกำกับไว้อีกจุดว่า "ส่วนความหมาย `is_gm`/level และวิธีเปิด UI เป็นขอบเขต `RE-089`
ไม่ claim ข้ามใบ" -- **สองประโยคนี้แยกกันคนละจุดในไฟล์เดิม ไม่ใช่ประโยคต่อเนื่องเดียวกัน** ยกมาทั้งคู่เพื่อยืนยัน
ว่า RE-091 ไม่ได้ตอบว่าอะไรเปิด widget: RE-091 พิสูจน์แค่ตัว *producer* (`[0x00729410,0x0072957D)`, gates:
event code `0x0D` = Enter บน widget ที่ active/visible อยู่แล้ว) แต่ไม่พิสูจน์ว่าอะไรทำให้ widget นั้น
active/visible ตั้งแต่แรก. ช่องว่าง
นี้บล็อกใบเทส attended ที่จะเปิดรอบนี้ (`GAME_TEST_QUEUE.md` `GT-103`, GM-002 capture matrix): ผู้เทสต้อง
รู้วิธีเปิด GM editor widget ในไคลเอนต์จริงก่อนจะพิมพ์อะไรเข้าไปทดสอบได้ ไม่งั้นใบ `GT-103` ทำได้แค่
exploration แบบสุ่ม ไม่ใช่ procedure ที่ระบุขั้นตอนได้จริง.

### objective
หาเงื่อนไข/กลไกที่ทำให้ widget ผู้ผลิต `0x51E9` (`0x00729410`) กลายเป็น active/visible — ไม่ใช่ตัวมันทำงาน
อย่างไรหลัง active แล้ว (ปิดแล้วโดย `RE-091`)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA/ตาราง sha256 ตรงกับ verifier ปัจจุบันก่อนเริ่ม เหมือนทุกใบ static
- **T1** — xref เข้า/ออกของฟังก์ชันที่สร้าง/toggle widget นี้ (caller ของโค้ดที่ทำให้ widget เข้าสถานะ
  active/visible ก่อนถึง `0x00729410`) — หา whether มันเป็น: (ก) hotkey handler แบบ global input map
  (ข) เมนู/ปุ่มใน GM tool panel ที่ `RE-091` เจอแล้วว่าเป็นอีก caller หนึ่งของ shared sender
  (`0x00729380`, "GM tool/panel producer") (ค) gate ที่อ่าน `GMModule_Client+0x18/+0x19/+0x1C`
  (สาม field เดียวกับที่ `RE-089` พิสูจน์ว่า `GM_UpdateGMStateVital` เขียนเข้าไป) แล้วโชว์ widget/ปุ่มเมื่อ
  ค่านั้นไม่ใช่ default
- **T2** — ถ้า T1 ชี้ไปทาง (ข)/(ค): หา provenance ของปุ่ม/ไอคอนที่กดเพื่อเรียก widget (ตำแหน่งบนจอถ้ามีข้อมูล
  layout, หรือชื่อ resource/texture ที่ผูกกับปุ่มนั้นถ้าถอดได้จาก static)
- **T3** — ถ้าหาไม่เจอในเส้นทางที่ถอดได้ ให้เขียน bounded negative ชัดเจน (เช่น "widget toggle ผูกกับ input
  event ที่ไม่มี static crosswalk ไปหา keycode ได้จากข้อมูลที่ commit ไว้ ต้องใช้การกดสำรวจจริงจากผู้เทส
  attended") ไม่เดา hotkey ไม่ปั้นเมนู

### nonclaims
① ไม่ตัดสินว่า widget เข้าถึงได้จากบัญชีที่ไม่ใช่ GM หรือไม่ — ขอบเขต `RE-089`/`RE-091` เดิม ใบนี้แค่หา
trigger ของตัว widget เอง
② ถ้า T1-T3 ไม่พบอะไรเลยในเส้นทางที่ถอดได้ นี่คือคำตอบที่สมบูรณ์ (bounded negative) ไม่ใช่ใบที่ค้าง — ปิดได้
พร้อมส่งต่อให้ `GT-103` เป็น exploration แบบสำรวจจริงแทน (ระบุในผลว่า "ต้องสำรวจจากไคลเอนต์จริง")
③ ไม่ claim ว่า `GT-103` block รอผลใบนี้เสมอไป — `GT-103` เขียนเป็น exploration step อยู่แล้วในตัว ถ้าใบนี้
ปิดก่อน `GT-103` จะได้ใช้ trigger ที่พิสูจน์แล้วแทนการเดา ถ้าใบนี้ยังไม่ปิด `GT-103` ยังทำได้ (สำรวจ) แค่ผล
อาจเป็น "หา widget ไม่เจอ" ซึ่งเป็นผลลบที่ยอมรับได้ของใบนั้นเอง

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
กลไก trigger ของ GM editor widget พร้อม provenance **หรือ** bounded negative ที่บอกตรงๆ ว่าต้องสำรวจจาก
attended ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

### result

**CLOSED PASS/DONE.** เต็มใบ: `notes_to_chief/20260827_1518_RE-104-RESULT-BT-GM-MODULE-PLUS19-GATE.md`.
Trigger ที่พิสูจน์ได้คือปุ่ม UI resource `BT_GM` (`0x00F2207C`), แสดง/enable จาก connection query type `0x25`
ที่คืน `GMModule_Client+0x19` (adapter `0x00726D30`) — periodic UI state `0x0053B150` เช็คซ้ำทุกช่วง click
dispatcher `0x0053B9B0` re-check gate เดิมก่อนขอ current UI key แล้วส่งเข้า central dispatcher `0x00AA0710` ซึ่ง
crosswalk ไปยัง factory `0x007280D0` ของ `GMModule_Client+0x48` สร้าง panel `GMUI_BASIC` (`Radiobutton_Message` +
`TextBox_Message`, Enter ส่งผ่าน producer `0x00729410` ที่ `RE-091` พิสูจน์ไว้แล้ว). ทั้ง 12 span/7 UTF-16 resource
มี sha256 pin ในใบเต็ม. ไม่ claim screen coordinate/icon texture/hotkey สำรอง และไม่ตั้งชื่อ `module+0x19` ว่า
`is_gm` (ยังไม่มี semantic/authorization evidence).

**BUILD_IMPACT:** procedure สำหรับ `GT-103`: หา/กดปุ่ม resource `BT_GM` ใน notification/system UI ก่อน แทนการ
สุ่ม hotkey — ดู `docs/GM_LANE.md` (pirate-force-server) ส่วน "RE requests closed" ข้อ 6 และ `GAME_TEST_QUEUE.md`
`GT-103` ที่อัปเดตแล้วรอบนี้.

BUILD_IMPACT_NONE: 0

---

## 🔬 RE-102 NPCCONVERSATION-COLUMBUS-156-QUESTID-3021-WIRE-CONFIRM-001 [STATIC-ON-BRIDGE]: **ยืนยันระดับ wire ว่า descriptor `+0x10`/`+0x12` ของ `NPCConversation` ใช้ quest id `3021` จริงสำหรับ Columbus ตัวจริง (`MOBS.n_ID=156`, Port Royal), แยกจาก quest `3023` ที่ `RE-095` ยืนยันไว้แล้วสำหรับ `MOBS.n_ID=36` (Columbus คนละตัว, Spice Paradise)**  [🔴 **CLOSED bounded-negative — ปิดโดย LANE-A (สาย A · WORLD) รอบ `pvbj0u` 2026-08-27 ~13:3x (+07:00), ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `GT-101`/`RE-101` มี hit แล้ว (`GT-101` = 4 hit, `RE-101` = 1 hit ใน
> `GAME_TEST_QUEUE.md`) ⇒ ข้ามไปที่ `102` = **0 hit ทั้งคู่ ทั้งสองไฟล์** ⇒ **ใบนี้คือ `RE-102`** · เลขว่างถัดไป
> หลังใบนี้ = 103
> 🔴 ใบ `RE-085`-`RE-100` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`rounds/A_20260827_1052_columbus_m2_identity_correction.md` และจดหมายคู่กัน
`notes_to_chief/20260827_1052_LANE-A-CORRECTION-columbus-m2-quest3021-not-3023-scene17-not-19.md` แก้
crosswalk: Columbus ตัวจริงที่ผู้เล่นเจอใน M2 (`bg0001` placement index 1, ยืนยันโดยคำเจ้าของ — testimony
จากเซสชัน attended ต่อเนื่องเดียวกัน `0925`→`0950` ไม่ใช่สอง derivation อิสระ, เลข index เคยขยับมาแล้วครั้ง
หนึ่งในวันเดียวกันจากที่ `RE-097` เดิมเคยว่า index 0) คือ **`MOBS.n_ID=156`** ไม่ใช่ 36 มี `s_QUEST_BEGIN` เป็น **`3021`** (`Q_TELEPORT1`, `n_VARI_2=17` →
scene 17/`Bg1001`) ส่วน `RE-095` ยืนยัน descriptor wire ของ quest `3023` ไว้แล้วจริง แต่นั่นคือ `MOBS 36`
(Spice Paradise, คนละตัว, คนละปลายทาง scene 19) — ที่ยืนอยู่ตอนนี้สำหรับ `3021` มีแค่ชั้น **[STATIC]**
(ตาราง gamedata) ยังไม่มีใครรัน wire capture สไตล์เดียวกับ `RE-095` ให้กับ MOBS 156/quest 3021 เลย

### objective (claim เดียว)
ยืนยันว่า descriptor nested ของ `NPCConversation` (u16 quest id ที่ `+0x10`, u8 ที่ `+0x12` ตามที่ `RE-094`/
`RE-095` ถอดไว้แล้ว) ที่ actor ของ Columbus ตัวจริง (`bg0001` placement index 1, `MOBS 156`) ส่งจริง คือ
`3021` — ไม่ใช่ `3023` (ของ `MOBS 36`) และไม่ใช่ `3020` (ของเดิม `P0` hardcode)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA ตรงกับที่ `RE-094`/`RE-095` ใช้ก่อนอ้างอิง span เดิมซ้ำ (`NPCConversation`
  constructor/serializer `0x622A00`/`0x622F10`)
- **T1** — เทียบ call site ที่ actor = `bg0001` placement index 1 (Columbus ตัวจริง) เรียก `NPCConversation`
  ว่า descriptor ที่ `+0x10` ใส่ `3021` จริงหรือไม่ (ขอบเขต placement ของ `bg0001` = block เดียว 149 แถว ตาม
  `RE-093` result — ห้ามสมมติ block ที่สอง)
- **T2** — ถ้าไม่มี call site ที่ระบุ actor ตรงตัว (เช่น dispatch ใช้ lookup ตาราง giver-NPC → quest generic
  เหมือนที่ `RE-094` พิสูจน์ไว้แล้วว่า op1 เป็น dynamic dispatch อ่านจาก UI record `+0x94`) ให้ยืนยันแทนว่า UI
  record ที่ actor นี้ป้อนเข้า `+0x94` คือ `3021` จริงจาก giver-NPC lookup ไม่ใช่ hardcode
- **T3 · ริเดอร์** — ถ้าเวลาเหลือ: ยืนยันว่า descriptor `+0x12` (ที่ `RE-094` พบว่ามีอยู่) ไม่ทำให้ quest `3021`
  เบี่ยงไปเส้นทางอื่นสำหรับ actor นี้โดยเฉพาะ

### nonclaims
① ไม่อ้างว่า [STATIC] เดิม (ตาราง gamedata, quest `3021`→scene 17) ผิด — ใบนี้แค่ขอยกระดับเป็น
wire-confirmed ② ไม่ตัดสินโครงสร้าง `src/pirateforce_foundation/` เอง — สาย A ตัดสินใจเองเมื่อได้ข้อมูล ③ ไม่
ทับ/แทนที่ `RE-095` (ยังถูกต้องสำหรับ `MOBS 36`) ④ **ไม่ใช่ตัวบล็อกงาน** `CORE-REQUEST` ที่ chief ต่อสายอยู่แล้ว
ในจดหมาย `1052` — ระดับ [STATIC] พอให้เริ่มต่อสายได้ ใบนี้เป็น double-check เพิ่มเติมเท่านั้น ⑤ ถ้าเพดาน static
ชนก่อนตอบได้ ให้เขียน bounded negative ตามกฎ ไม่เดาต่อ

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์ gamedata อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative
แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ตอบ T0-T2 ด้วยหลักฐาน (descriptor/UI-record ยืนยัน `3021` สำหรับ actor นี้) **หรือ** bounded negative ว่าไม่มี
call site/field ที่แยกแยะได้ ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

> 🔧 **แก้ misplacement (Lane A, mailbox-consumption รอบ `kqrlhr`, 2026-08-27 ~14:2x +07:00):** ผลของใบนี้
> ถูกเขียนไว้ผิดตำแหน่งตั้งแต่รอบ `pvbj0u` — เนื้อ result ด้านล่างถูกวางไว้ใต้ placeholder ของ `RE-100` แทน
> (คนละใบ, RE-100 ตอนนั้นยังไม่ปิด) ทำให้ placeholder ของ `RE-102` เองค้างว่าง `(ยังไม่มี — ใบเปิดอยู่)`
> ทั้งที่หัวใบข้างบนเขียนว่า `CLOSED` อยู่แล้ว — ย้ายเนื้อหามาไว้ที่ถูกที่รอบนี้ ไม่มีข้อความไหนถูกแก้ไข
> เนื้อหา แค่ย้ายตำแหน่ง `RE-100` เองได้ผล real ของตัวเองแล้วในบล็อกของมันด้านบน

### result — CLOSED bounded negative, T0 cross-document only, T1/T2 negative, T3 moot

รายละเอียดเต็ม: `notes_to_chief/20260827_1339_RE-102-RESULT-BOUNDED-NEGATIVE-NO-STATIC-CALL-SITE.md`. สรุป:

- **T0** [STATIC, cross-document เท่านั้น — ไม่มี binary ให้ hash สดใน clone นี้]: `factpack_L1/MANIFEST.md:16`,
  `RE-094-RESULT` (`0156`) และ `RE-095-RESULT` (`0310`) ทั้งสามอ้าง SHA เดียวกัน
  (`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`) — เอกสารสอดคล้องกัน แต่ไม่ใช่การ
  hash ซ้ำ
- **T1** [STATIC, bounded negative]: `external/PF_SERIALIZER_FIELDS.tsv` มีครบ 22 แถวของ `NPCConversation`
  (`[0x00622F10,0x00623083)` + subcall `[0x00606890,0x006068E3)`) แถว `+0x10` (`W 6`, บรรทัด 1576) resolve
  เป็น pointer chase ผ่าน array ที่ caller ส่งเข้ามา ไม่ใช่ literal คงที่ในตัว serializer เอง — ไม่มี call site
  ระดับ static ที่ actor เจาะจงเขียน `3021` ตรงๆ (สอดคล้องกับที่ `RE-094` พิสูจน์ไว้แล้วว่า op1 เป็น dynamic
  dispatch ไม่ใช่ขัดแย้งกัน)
- **T2** [เพดาน — UNKNOWN]: ค่าที่เข้า serializer มาจาก UI record `+0x94` ที่ populate โดยโค้ดเหนือ serializer
  นี้ (`RE-094`) — grep `+0x94`/giver ทั่ว `external/*.tsv` ทั้งหมด (`PF_SERIALIZER_FIELDS`,
  `PF_PROTOCOL_REGISTRY`, `PF_DATA_EVIDENCE`, `PF_RUNTIME_CLASSMAP`, `PF_INPUT_INVENTORY`,
  `PF_FIELD_VALIDATION`) = 0 hit ทั้งหมด ต้องใช้ disassembly สดของ image (ไม่มีใน clone นี้) หรือ attended
  wire capture จริง ไม่มีทางใดพร้อมใช้ในรอบนี้
- **ปัญหาซ้อนอีกชั้น**: สมมติฐานตั้งต้นของ T1/T2 เอง ("placement index 1 = MOBS 156") ก็ไม่ใช่ static field
  ที่ decode ได้ — `bg0001.placements.tsv` แถว 1 มีแค่ `template_ids=2` (`Mob_Set_02`), และ `RE-093` เองห้าม
  join ordinal ไปเป็น MOBS n_ID ตรงๆ ไว้แล้ว การผูก index 1 → MOBS 156 อยู่ที่ชั้น testimony/client-observable
  (คำเจ้าของจากเซสชัน attended `0925`→`0950`) ไม่ใช่ชั้น wire/code ที่ T1/T2 ถามหา — ต่อให้เจอ call site ก็ปิด
  loop ไม่ได้โดยไม่มี identity proof อิสระที่ชั้นนี้
- **T3**: ไม่ทำ — moot เมื่อ T1/T2 เป็น bounded negative แล้ว

**ทางเดียวที่จะยกระดับต่อ:** `GT-102` (`GAME_TEST_QUEUE.md:4094`, PENDING) — คลิก Columbus ตัวจริงในไคลเอนต์
จริงแล้วบันทึก wire capture เท่านั้น ไม่มีเส้นทาง static เพิ่มเติมในข้อมูลที่ commit ไว้แล้ว

**ไม่ทับ/ไม่ขัด:** `columbus_quest_dispatch.py` (chief, `CORE-REQUEST-014`) — ช่องว่างสองจุดของมัน (scene-17
spawn = `RE-103`, vehicle-bind payload = `RE-096`) เป็นทิศทาง **outbound** (server ตอบอะไร) คนละทิศกับ RE-102
ที่ถาม **inbound** (client ส่ง 3021 จริงไหม) — ปิด RE-102 เป็น negative ไม่ทำให้สอง gate นั้นเปลี่ยนสถานะ

BUILD_IMPACT: ไม่มีของให้ wire เพิ่มใน `src/pirateforce_foundation/` จากใบนี้ — ระดับความเชื่อมั่นของ
`3021`→Columbus ยังคงเป็น `[STATIC]` เท่าเดิม (ไม่ได้ตกลงหรือขึ้นระดับ) `columbus_quest_dispatch.py` คงสถานะ
fail-closed เดิมต่อไปจนกว่า `RE-096`/`RE-103` หรือ `GT-102` จะปิดได้จริง — สาย A ไม่มีอะไรให้สร้างใน `src/`
จากผลใบนี้รอบนี้เช่นกัน

---

## 🔬 RE-105 GM-UPDATE-STATE-VITAL-VERSION-001 [STATIC-ON-BRIDGE]: **`vital_version` ที่ถูกของ `GM_UpdateGMStateVital` (`0x5A19`) คืออะไร — และ error path ที่ผลิต `網路 VitalData 版本不對 ErrorData=<vital id>` อ่านค่าที่ต้องการจากไหน** [🟢 **CLOSED DONE/PASS — ปิดโดย LANE-GM รอบ `kcm8ir` 2026-08-27T16:1x+07:00, ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-105` = 0 hit, `GT-105` = 0 hit ทั้งสองไฟล์ (ยืนยัน
> 2026-08-27T15:22+07:00) ก่อนหน้านี้เลขสูงสุดที่ใช้แล้วคือ `104` (ทั้ง `RE-104`/`GT-104`) ⇒ ใบนี้คือ `105`
> 🔴 ใบ `RE-085`-`RE-104` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260827_1445_GT101-RESULT-client-rejects-0x5A19-version-1-error-23065-session-killed.md`
(attended session "กะ1", OBSERVER_CONFIRMED เจ้าของเห็นเอง 2026-08-27T14:39+07:00) — เจ้าของ login ด้วยบัญชี
GM จริง (`localtest`) ผ่าน `PF_GM_ACCOUNTS_CONFIG` แล้วเห็น modal error กลางจอ ทันทีหลังเข้าแมพ ข้อความจีนตัวเต็ม
`網路 VitalData 版本不對 --- ErrorData=23065, 請洽程式設計人員` — `23065` ฐานสิบ = `0x5A19` =
`GM_UpdateGMStateVital` ตรง ๆ (client ระบุ vital id เองในข้อความ error) จากนั้น client หยุดประมวลผลสายทั้งหมด
(นับถอยหลัง 24/25/26 วินาที บนจอ) แล้วปิด socket เอง (`ConnectionResetError(10054)`) จนเจ้าของต้องกด OK ปิดเกม
ทั้งที่แมพ Port Royal เรนเดอร์ครบอยู่ข้างหลัง dialog (HP/level/minimap/HUD ปกติหมด)

เฟรมที่ส่งจริงบนสาย (จากคอนโซลเซิร์ฟเวอร์ `capture_gt101_20260827_143419/server_console_live.out.txt`):
`12 9D 6E 14 00 00 00 00 08 04 0B 02 12 01 00 12 19 5A 0B 01 0B 00 0B 00 14 00 00 00 00`
สร้างด้วย `gm/state_wire.py`'s `make_gm_update_state_frame(legacy, 1, 0, 0, 0)` — `1` คือ `vital_version` ที่
`docs/GM_LANE.md`/`state_wire.py`'s ติดป้ายเองไว้แล้วว่า `[ASSUMED - awaiting RE]` ก่อน `GT-101` (ไม่ใช่ค่าที่
วัดมา) เทียบกับเฟรมอื่นบน connection เดียวกัน: `START_GAME_RES` ใช้ `0B 03` ("vital_version=3" ตำแหน่งเดียวกัน),
`TeleportVital` ใช้ `0B 04` — ทั้งสองไม่ใช่หลักฐานของเวอร์ชันที่ถูกของ `0x5A19` (คนละ vital) แต่เป็นตัวอย่างว่า
เวอร์ชัน `1` ผิดปกติเทียบกับเฟรมข้างเคียงจริง

### objective
1. หาว่า client เช็ค `vital_version` ของ `0x5A19` ตรงไหน (handler `0x00729F00` ที่ `RE-089` พินไว้แล้ว) และ
   ค่าที่ผ่านการเช็คคือเท่าไร (ตัวเลขเดียวหรือช่วง)
2. หา error path ที่ผลิตข้อความ `網路 VitalData 版本不對 --- ErrorData=<vital id>` — path นี้น่าจะใช้ได้กับ
   vital อื่นทุกตัวในโปรเจกต์ในอนาคต (client "บอก" เราเองว่าเฟรมไหนผิดพร้อม vital id ตัวเลข) ไม่ใช่แค่ใบนี้
3. ถ้าเป็นไปได้: หาที่มาของไบต์ offset 8-9 ในเฟรมข้างต้น (`08 04` — เฟรมอื่นบน connection เดียวกันทุกใบเป็น
   `08 00`) ว่าเป็น field ของ envelope ที่ต้องตั้งค่าด้วยหรือเป็นเรื่องคนละจุด — ไม่บล็อกใบนี้ถ้าตอบไม่ได้
   ในเวลาที่มี ให้แยกเป็น bounded negative ของหัวข้อนี้โดยเฉพาะ

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA/ตาราง sha256 ตรงกับ verifier ปัจจุบันก่อนเริ่ม เหมือนทุกใบ static
- **T1** — อ่าน handler `0x00729F00` หา instruction ที่เทียบ/บวกลบกับค่าคงที่ที่ตำแหน่ง vital_version ของ
  payload ขาเข้า (`+0x??` ตามที่ `RE-089` พินโครง header ไว้) — ค่าคงที่นั้นคือคำตอบของข้อ 1
- **T2** — xref จากจุดเช็คที่ T1 เจอไปยัง branch ที่ล้มเหลว (ไม่ตรงเวอร์ชัน) — path นั้นควรจะโยงไปหาโค้ดที่ประกอบ
  ข้อความ error/dialog (เทียบ format string หรือ resource string ที่มีรูป `%s`/`版本不對`/`ErrorData=%d` หรือ
  คล้ายกัน) — ยืนยันว่าเป็น generic error path ไม่ใช่ path เฉพาะของ `0x5A19`
- **T3** — ถ้าเวลาเหลือ: ตรวจไบต์ offset 8-9 (`08 04` vs `08 00`) ตามข้อ objective 3
- **T4** — ถ้าหา T1 ไม่เจอในเส้นทางที่ถอดได้ ให้เขียน bounded negative ชัดเจน ("เวอร์ชันที่ถูกไม่ปรากฏเป็นค่าคงที่
  ที่ static เห็นได้ ต้องใช้การ brute-force ค่าจริงจากไคลเอนต์ทีละค่า") ไม่เดาตัวเลข ไม่ทายจากเฟรมข้างเคียง

### nonclaims
① ไม่ claim ว่า `3`/`4` (ค่าที่เฟรมข้างเคียงใช้) คือเวอร์ชันที่ถูกของ `0x5A19` — เป็นคนละ vital กัน ไม่มี
หลักฐานว่าใช้ scheme เวอร์ชันร่วมกัน
② ไม่ claim ว่า RE-089's field semantics (`is_gm`/level ของสามฟิลด์) เปลี่ยนไปจากผลใบนี้ — ใบนี้ถามแค่เรื่อง
version/error-path ไม่แตะความหมายฟิลด์
③ ถ้า T1-T4 ไม่พบอะไรเลยในเส้นทางที่ถอดได้ นี่คือคำตอบที่สมบูรณ์ (bounded negative) ไม่ใช่ใบที่ค้าง — ปิดได้
พร้อมส่งต่อให้ attended brute-force รอบถัดไปแทน

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ค่า `vital_version` ที่ถูกของ `0x5A19` พร้อม provenance **หรือ** bounded negative ที่บอกตรงๆ ว่าต้อง
brute-force จากไคลเอนต์จริง ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:` ตามกฎ `BUILD-003`

**เร่งด่วนกว่าใบอื่นในคิว:** ใบนี้บล็อกไม่ให้ `localtest` (บัญชีจริงที่เจ้าของบูตด้วย) กลับเข้า `gm_accounts`
ได้อีกจนกว่าจะปิด — เฟรมเวอร์ชัน `1` ฆ่าเซสชันเจ้าของไปแล้วหนึ่งครั้ง (`GT-101`, `ErrorData=23065`)

### result

**CLOSED DONE/PASS.** เต็มใบ:
`notes_to_chief/20260827_1613_RE-105-RESULT-VITAL-VERSION-ZERO-GENERIC-MISMATCH-PATH.md`.

1. `vital_version` ที่ถูกของ `0x5A19` คือ **`0`** เท่านั้น (exact equality) — เช็คจริงอยู่ใน **generic VitalData
   collection reader** `[0x005F3E20,0x005F406D)`, ไม่ใช่ handler เฉพาะ `0x00729F00`. Prototype ของ `0x5A19` เขียน
   `message+0x10 = 0` โดย `mov` ตรงที่ bootstrap `0x007299B0` (ไม่ได้อนุมานจาก vital อื่น).
2. error path เป็น **generic สำหรับทุก nested VitalData**: equality ล้ม → อ่าน id ของ instance ที่กำลัง decode
   แบบ dynamic ผ่าน vtable → error code `0xE0000031` → ผูกกับ resource string `網路 VitalData 版本不對` →
   `ErrorData=%d` คือ vital id ของ instance ที่ mismatch (ไม่ hardcode `0x5A19`)
3. ไบต์ offset 8-9 (`08 04`) คือ **outer `GSCN_RunTimeProtocolRes` protocol version 4** — คนละฟิลด์ ถูกต้องอยู่
   แล้ว ไม่ต้องแก้

เฟรมที่ถูกต้อง: `... 08 04 0B 02 12 01 00 12 19 5A 0B 00 ...` (เปลี่ยนแค่ byte หลัง vital id จาก `0B 01` เป็น
`0B 00`)

**BUILD_IMPACT:** `gm/state_wire.py`'s `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED` เปลี่ยนจาก `None` เป็น `0` แล้ว
รอบนี้ (LANE-GM write zone, ไม่แตะ `runtime.py` — guard ของ `CORE-REQUEST-016` เปิดเองเมื่อค่านี้ไม่ใช่ `None`),
ยืนยันด้วย headless test ที่ assert nested header ตรง `12 19 5A 0B 00` จริง (`tests/test_gm_login_state_guard.py`).
ผล UI/GM permission ยังต้องวัด attended แยก (`GT-101` rerun) — ใบนี้ไม่ claim ว่า widget/UI จะเปลี่ยนอะไรบนจอ.

BUILD_IMPACT_NONE: 0

---

## 🆕🔬 RE-106 QUEST-FLAG-SYNC-MECHANISM-001 [STATIC-ON-BRIDGE]: **`Quest.GetQuestFlag` อ่านค่าจากไหน — ต้องมี wire vital ส่ง flag state จริงหรือ client เก็บ local ล้วน** [🟢 **OPEN — เปิดโดย chief 2026-08-27T15:xx+07:00 ต่อยอดจาก `PANYA-DECISION 1510` (M2 quest-gate skip)**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-106`/`GT-106` = 0 hit ทั้งสองไฟล์ (2026-08-27T15:4x+07:00)
> เลขสูงสุดที่ใช้แล้วคือ `105` (`RE-105`/lane GM) ⇒ ใบนี้คือ `106` (ชนกับ `GT-106` ของ chief เอง — คนละไฟล์
> คนละ prefix ไม่ใช่การชนจริง ตัวนับร่วมแค่กันเลขซ้ำข้าม prefix)
> 🔴 ใบ `RE-085`-`RE-105` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`PANYA-DECISION 2026-08-27T15:10+07:00` (`notes_to_chief/20260827_1510_...`) สั่ง chief: บนเส้นทางไร้แฟล็ก
ให้เซิร์ฟเวอร์ถือว่าเควส 110/739/111 = Finish เพื่อให้ `Accept_Check` ของเควส 3021
(`Quest.GetQuestFlag(111) == Finish`) ผ่าน chief ตรวจ static ก่อนเขียนโค้ด (ตามกฎห้ามปั้น wire field) พบว่า:
- `gamedata/PF_GAMEDATA_LUA_API.tsv:7,23` — `Quest.SetFlag`/`Quest.SetQuestFlag` เป็น **STUB_NOOP บนไคลเอนต์**
  (`delegate_va=0x0045FA00`, body `xor eax,eax; ret 4; int3`) — เรียกแล้วไม่ทำอะไรจริงฝั่งไคลเอนต์
- `PF_GAMEDATA_LUA_API.tsv:6` — `Quest.GetQuestFlag` เป็น **IMPLEMENTED จริง** (`delegate_va=0x006083C0`,
  body ไม่ว่าง) ใช้จริงใน `gamedata/lua/Quest/q_con_new.lua:107,119,142`
- สรุป: ใครก็ตามที่เขียนค่าที่ `GetQuestFlag` อ่าน ไม่ใช่ Lua ทั้งสองฟังก์ชันข้างต้น (พิสูจน์เป็น stub แล้ว)
  เหลือสองทางที่ static เห็นไม่พอแยก: (ก) ไคลเอนต์เก็บ state ภายในเอง ไม่ต้องมี wire sync เลย หรือ
  (ข) มี wire vital ส่งจริง — ผู้สมัครที่มีรูปร่างพอ (ไม่ EMPTY, ไม่ใช่แค่ candidate name) คือ
  `UpdateQuestMiscDataVital` (`0x76A5`) และ `UpdateDailyQuestVital` (`0x5DEB`) — ทั้งคู่ยังไม่ decode ความหมาย
- `docs/FUNCTIONAL_COVERAGE.json` แถว `quest_accept_and_progress` = `in_progress` ("no quest state is stored
  server-side") ยืนยันตรงกับที่พบ — เซิร์ฟเวอร์นี้ไม่เคยส่งอะไรเกี่ยวกับ quest flag เลยจนถึงตอนนี้

### objective
1. xref `Quest.GetQuestFlag`'s handler (`0x006083C0`) หาว่ามันอ่านจากที่ไหน (struct field ในเมมโมรีไคลเอนต์
   ที่ไม่เคยถูกเขียนโดย network handler ใด ๆ = ทาง ก, หรือ struct ที่ handler ของ vital ใดวุ่นเขียน = ทาง ข)
2. ถ้าทาง ข: xref `UpdateQuestMiscDataVital` (`0x00622940` ตามที่ตรวจเจอ) และ `UpdateDailyQuestVital`
   (`0x00621AE0`) ว่าเขียนโครงสร้างเดียวกับที่ข้อ 1 อ่านหรือไม่ ถ้าใช่ ถอด field layout ให้พอประกอบเฟรมได้
3. ถ้า static เห็นไม่พอแยกทาง ก/ข ให้บันทึกเป็น bounded negative ชัดเจน พร้อมข้อเสนอ: attended capture คลิก
   ตัวเลือกเควส 3021 ด้วยตัวละครเลเวลต่ำ (ไม่เคยผ่าน 110/739/111) แล้วดูว่าไคลเอนต์ปฏิเสธตัวเลือกเงียบ ๆ
   (แปลว่าเช็คจริง ต้องมี wire) หรือปล่อยผ่าน (แปลว่า server-authoritative พอ ไม่ต้องมี wire เลย)

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
กลไกจริงของ `GetQuestFlag` พร้อม provenance **หรือ** bounded negative ที่เสนอ attended capture ตามข้อ
objective 3 ชัดเจน ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**ไม่บล็อก M2 คืนนี้ตามคำเจ้าของ**: `chief` เขียนโค้ด quest-gate-skip ไม่ได้จนกว่าใบนี้จะปิด (จะเป็นการปั้น
wire field ที่ไม่มีหลักฐาน) — M2 ไปต่อด้วยส่วนที่ไม่ต้องรอใบนี้ (เข้าฉาก 17, ไม่ต้องเป็นเรือ) ดู
`CHIEF-STATUS` รอบเดียวกันนี้สำหรับข้อเสนอทางเลือก

### result (ยังไม่มี — ใบเปิดอยู่)

---

## 🔬 RE-107 MOB-DEATH-DYING-DEAD-ANIMATION-DRIVER-001 [STATIC-ON-BRIDGE]: **NAMED+HOSTILE actor_type 4 ที่ HP 0 ไม่ล้มเหมือน GT-022/GT-025 (nameless/factionless) — client ใช้ฟิลด์/เฟรมไหนสั่ง fall/dying animation ของ body นี้ และทำไม mesh ถึงค้างลอย** [🟢 **CLOSED BOUNDED-NEGATIVE/DONE — ปิดโดย RE runner LOCAL 2026-08-27T17:11+07:00, บริโภคโดย LANE-B, ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-107`/`GT-107` = 0 hit ทั้งสองไฟล์ (2026-08-27T16:37+07:00)
> เลขสูงสุดที่ใช้แล้วคือ `106` (`RE-106`/chief) ⇒ ใบนี้คือ `107`
> 🔴 ใบ `RE-085`-`RE-106` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260827_1620_GT084R2-RESULT-PASS-hostile-kill-full-wire-but-corpse-freezes-no-target-panel.md`
(OBSERVER_CONFIRMED 2026-08-27T15:52-15:55+07:00) — ผู้เทสตี Tornado Eagle (identity `0x201F`, actor_type 4,
named, hostile) 5 ครั้งจนถึง 0 HP บนบูตไร้แฟล็ก เซิร์ฟเวอร์ส่ง dying frame (timer 20.0) แล้ว dead frame
(700 ms ถัดมา) ผ่าน carrier เดียวกับที่ `GT-022`/`GT-025` เคยใช้ (`GSCN_RunTimeProtocolRes` mask `0x02`).
ข้อความ "Tornado Eagle บาดเจ็บหนักและล้มลง!" ขึ้นจริง (client รับ DYING) แต่นก**แข็งค้างท่าลอย ไม่ล้ม ไม่กระพือ
ปีก ไม่มีอนิเมชัน** หลัง DEAD cursor ไม่รับรู้ว่ามี actor ตรงนั้นอีก ค้างจน logout.

นี่ตรงข้ามกับ `GT-022`/`GT-025` (2026-08-19) ที่ส่งเฟรมชุดเดียวกันไปยัง identity `0x2001` — actor_type 4
เหมือนกัน แต่**ไม่มีชื่อ ไม่มี faction** — แล้วได้ผลล้มราบจริง. actor_type เท่ากันแต่ผลต่างกัน ⇒ ตัวแปรที่ทำให้
ต่างไม่ใช่ actor_type อย่างเดียว ต้องเป็นฟิลด์อื่นในเฟรม (ชื่อ/mask hostile `0x078D`/faction) — ยังไม่มีใคร
xref หาสาขานั้น.

`src/pirateforce_foundation/mob_death.py` (repo `pirate-force-server`, grep `DYING_PREDICATE_VA`/
`DEATH_PREDICATE_VA` — เลขบรรทัดขยับทุกรอบที่มีคนแก้ docstring ด้านบน ห้ามเชื่อเลขบรรทัดเก่า หาโดยชื่อ) pin
ไว้ว่า predicate คู่ที่ใช้จริงคือ `DYING_PREDICATE_VA = 0x43BDA0` (timer > 0) และ `DEATH_PREDICATE_VA =
0x43BD70` (timer <= 0) บน
`CNetNPC`/`CAvatarNPC`/`Pet` (actor_type 4) — คู่ต่าง `0x454A70`/`0x454AC0` ใช้กับ actor_type 2 เท่านั้น ไม่
เกี่ยวกับใบนี้. ไฟล์เดียวกันบันทึกเอง (nonclaim ~397-405) ว่า "named AND hostile in one body has never been
sent and never been observed" — `GT-084-R2` คือครั้งแรกที่ถูกส่งและสังเกต และผลไม่ตรงกับ fall-precedent

### objective
1. หาว่า predicate คู่ `0x43BDA0`/`0x43BD70` (หรือโค้ดที่ตามหลัง) อ่านฟิลด์อื่นนอกจาก timer ด้วยหรือไม่ (ชื่อ/
   mask/faction) — เทียบ path ของ body ที่ไม่มีชื่อ/faction กับ body ที่มี
2. หาจุดที่ client เลือกเล่นอนิเมชันล้ม/ตาย (`_F_DIE_000` หรือคลิปที่เกี่ยวข้อง) เทียบเงื่อนไขระหว่างสองชนิดบอดี้
3. หาว่า "ค้างลอย ไม่ตอบสนอง cursor" มาจากไหน — สามทาง (ก) actor ถูกลบจาก logic/picking list แต่ render mesh
   ไม่ถูกลบ (ข) animation clip ไม่ถูกเลือกให้ body ประเภทนี้ (ค) DEAD มาเร็วเกินตัด DYING (hold 700ms vs
   timer 20.0) — แยกสามทางนี้ด้วย static ถ้าทำได้
4. ถ้า static เห็นไม่พอแยกทาง เขียน bounded negative พร้อมเสนอ attended capture ที่แคบที่สุด (เช่น ส่ง dying
   โดยไม่มี hostile mask กับ body ชื่อเดียวกัน เทียบผล)

**[UPDATE, round B_20260827_1734 (ebbhzt), 2026-08-27]** ผลข้างล่างมาจาก
`notes_to_chief/20260827_1711_RE-107-RESULT-DEATH-BRANCH-MODEL-GATE-BOUNDED.md` (RE runner LOCAL) — บริโภคแล้ว
โดย LANE-B รอบนี้ ไม่มี code diff ที่ปฏิบัติได้จากผลนี้ (`BUILD_IMPACT: NONE`), ดูเหตุผลใน result ด้านล่าง

### nonclaims
① ไม่ claim ว่า `DEATH_TASK_HOLD_MS = 700` เป็นสาเหตุ — ใบนี้ถามฟิลด์ที่คุมอนิเมชัน ไม่ใช่ใบวัด timing (การวัด/
   แก้ 700ms สงวนตาม `notes_to_chief/20260826_0551_COO-DECISION-death-hold-700-stands*.md`)
② ไม่ claim คำตอบล่วงหน้า — สามสมมติฐานในข้อ objective 3 เปิดเท่ากัน
③ ถ้าจ็อบด้านล่างไม่พบอะไรเลยในเส้นทางที่ถอดได้ นี่คือคำตอบสมบูรณ์ (bounded negative) ไม่ใช่ใบค้าง

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA ตรงกับ verifier ปัจจุบันก่อนเริ่ม เหมือนทุกใบ static
- **T1** — อ่านโค้ดรอบ `0x43BDA0`/`0x43BD70` หา field อื่นที่ถูกอ่านนอกจาก timer
- **T2** — xref ไปยัง path ที่เลือกอนิเมชันล้ม/ตาย เทียบสาขาระหว่างสองชนิดบอดี้
- **T3** — ตรวจ picking/removal list vs render list แยกกันหรือไม่
- **T4** — ถ้าหา T1-T3 ไม่เจอในเส้นทางที่ถอดได้ ให้เขียน bounded negative ตามข้อ objective 4

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ฟิลด์/เฟรม/branch ที่คุม fall-vs-freeze พร้อม provenance **หรือ** bounded negative ที่เสนอ attended capture
แคบที่สุดที่จะแยกสามสมมติฐานในข้อ objective 3 ได้ ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

### result

**CLOSED BOUNDED-NEGATIVE/DONE.** เต็มใบ: `notes_to_chief/20260827_1711_RE-107-RESULT-DEATH-BRANCH-MODEL-GATE-BOUNDED.md`.
Recursive CFG ครบทั้งสอง predicate (`DYING_PREDICATE_VA=0x43BDA0`, `DEATH_PREDICATE_VA=0x43BD70`): อ่านเฉพาะ
resident `BasicAttr` mask `[attr+0x44]==0` กับ timer `f32 [attr+0x58]` **ไม่มี read ของ name/faction/wire mask
เลย** ⇒ named+hostile กับ nameless/factionless ไม่แยกกันที่ predicate คู่นี้. จุดเลือกท่าตายจริง (`0x472850`)
เช็ค client-local model-loaded bit `[actor+0x70]&0x40` ก่อนส่ง clip `_F_DIE_000` เข้า render — bit นี้ไม่มี field
เขียนจาก server เห็นได้ทาง static, และ data corpus ไม่มี crosswalk ยืนยันว่า preset `M011` (Tornado Eagle)
resolve คลิปนี้สำเร็จหรือไม่. dead-task update CFG ครบไม่พบ call ไป actor-map resolver/inserter ⇒ ไม่พบ
"actor ถูกลบจาก picking list" ใน task นี้ แต่ static แยก "ถูกถอดจาก logic list" กับ "ยังอยู่แต่ pick filter
ปฏิเสธ" ไม่ได้โดยไม่เดา — **bounded negative ตามเกณฑ์จบใบ**. attended capture ที่แคบที่สุดถูกเสนอไว้ในใบเต็ม
(ส่ง DEAD entry เฟรมเดียวไม่มี DYING มาก่อน บน identity/preset เดิม, ห้ามเปลี่ยน name/faction พร้อมกัน).

**BUILD_IMPACT: NONE** — static ไม่พบ field ที่ server เขียนได้เพื่อแก้ freeze; ไม่มี diff ให้ทำในรอบนี้
ต่อยอดได้เฉพาะทาง attended capture ที่ใบเต็มเสนอ (นอกเขตเขียนของ LANE-B — เป็นงาน attended/RE รอบถัดไป)

BUILD_IMPACT_NONE: 1

---

## 🔬 RE-108 SELECT-TARGET-UI-PANEL-REQUIRED-FRAME-001 [STATIC-ON-BRIDGE]: **single-click บน 0x201F ได้ขอบแดง + ลูกศรล็อกแต่ไม่มีแผงเป้า UI (ต่างจาก GT-045 v3) — client ต้องการฟิลด์/เฟรมอะไรจากเซิร์ฟเวอร์ถึงจะเปิดแผง** [🟢 **CLOSED BOUNDED-NEGATIVE/DONE — ปิดโดย RE runner LOCAL 2026-08-27T17:19+07:00, บริโภคโดย LANE-B, ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-108`/`GT-108` = 0 hit ทั้งสองไฟล์ (2026-08-27T16:37+07:00)
> เลขสูงสุดที่ใช้แล้วคือ `107` (`RE-107`, ใบก่อนหน้าในรอบเดียวกัน) ⇒ ใบนี้คือ `108`
> 🔴 ใบ `RE-085`-`RE-107` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260827_1620_GT084R2-RESULT-PASS-hostile-kill-full-wire-but-corpse-freezes-no-target-panel.md`
(session เดียวกับ `RE-107`, OBSERVER_CONFIRMED 2026-08-27T15:52-15:55+07:00) — ผู้เทส single-click ที่ Tornado
Eagle (`0x201F`) หนึ่งครั้ง ได้ **ขอบแดงรอบตัว + ลูกศรแดงคู่ล็อกที่ชื่อ** (ป้ายชื่อสีชมพู) แต่**ไม่มีแผง UI ข้อมูล
เป้าหมายเปิดขึ้นด้านบนจอเลย**. GAME_TEST_QUEUE.md ยืนยันซ้ำหลายที่ (บรรทัด 1620, 3729) ว่า "คลิกเดียวก็เปิดแผง
เป้าได้" และ `GT-045 v3` เป็นตัวอย่างจริงที่ single-click เปิดแผงเป้าได้สำเร็จ (คนละ actor, คนละ identity) —
ใบนี้เป็นครั้งแรกที่ single-click ได้ผลด้านภาพ (ขอบแดง/ลูกศร) ครบ แต่แผงไม่ขึ้น ⇒ แผงกับขอบแดง/ลูกศรไม่ได้ผูก
เงื่อนไขเดียวกัน อย่างน้อยสำหรับ body นี้

### objective
1. หา handler/path ที่เปิดแผง UI ข้อมูลเป้าหมาย (เทียบกับ path ที่วาดขอบแดง/ลูกศรล็อก ซึ่งทำงานสำเร็จแล้วสำหรับ
   `0x201F` — สองพาธนี้แยกกันหรือรวมกัน)
2. หาว่าพาธเปิดแผงต้องการฟิลด์/เฟรมอะไรจากเซิร์ฟเวอร์ที่ยังไม่ถูกส่ง (เช่น select-target response vital เฉพาะ,
   หรือ attr field บางตัวในเฟรม census ที่ actor นี้ยังไม่มี) — เทียบกับ census/attr ที่ `GT-045 v3`'s target
   actor มีแต่ `0x201F` (field-mob roster, `field_mob_tables.py`) ไม่มี
3. ถ้า static เห็นไม่พอชี้เฟรมที่ขาด ให้บันทึก bounded negative ชัดเจน พร้อมเสนอ attended capture ที่แคบที่สุด
   (เช่น: capture ดิบของ raw bytes ที่ client ส่งตอน single-click บน `0x201F` เทียบกับ single-click บน actor
   ของ `GT-045 v3` — หา request ที่ client ส่งออกแล้วเซิร์ฟเวอร์ไม่เคยตอบ)

### nonclaims
① ไม่ claim ว่าไม่มีแผง = ฝั่งเซิร์ฟเวอร์ผิด (ตามจดหมายต้นทาง nonclaim ④) — อาจเป็น field-mob roster ที่ขาด
   attribute บางตัวที่ NPC ทั่วไปมี ไม่ใช่ path การเปิดแผงเอง
② ไม่ claim ว่าขอบแดง/ลูกศรกับแผงเป้าใช้ trigger เดียวกัน — เป็นคำถามที่ objective 1 เปิดไว้ ไม่ใช่ข้อสรุป
③ ถ้า T1-T3 ไม่พบอะไรเลยในเส้นทางที่ถอดได้ นี่คือคำตอบที่สมบูรณ์ (bounded negative) ไม่ใช่ใบที่ค้าง

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA/ตาราง sha256 ตรงกับ verifier ปัจจุบันก่อนเริ่ม เหมือนทุกใบ static
- **T1** — หา handler ที่เปิด/ประกอบแผง UI ข้อมูลเป้าหมาย แยกจาก handler ที่วาดขอบแดง/ลูกศรล็อก
- **T2** — xref ว่าพาธนั้นอ่าน field/vital อะไรที่ field-mob roster ปัจจุบัน (`field_mob_tables.py`) ยังไม่มี
- **T3** — ถ้าหา T1-T2 ไม่เจอในเส้นทางที่ถอดได้ ให้เขียน bounded negative ตามข้อ objective 3

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ฟิลด์/เฟรม/handler ที่คุมการเปิดแผงเป้า พร้อม provenance **หรือ** bounded negative ที่เสนอ attended capture
แคบที่สุดตามข้อ objective 3 ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**[UPDATE, round B_20260827_1734 (ebbhzt), 2026-08-27]** ผลข้างล่างมาจาก
`notes_to_chief/20260827_1719_RE-108-RESULT-LOCAL-PANEL-GATE-NO-RESPONSE-FRAME.md` (RE runner LOCAL) — บริโภคแล้ว
โดย LANE-B รอบนี้ ไม่มี code diff ที่ปฏิบัติได้จากผลนี้ (`BUILD_IMPACT: NONE`), ดูเหตุผลใน result ด้านล่าง

### result

**CLOSED BOUNDED-NEGATIVE/DONE.** เต็มใบ: `notes_to_chief/20260827_1719_RE-108-RESULT-LOCAL-PANEL-GATE-NO-RESPONSE-FRAME.md`.
Complete handler `0x51F2F0..0x51F494` ถอด CFG ครบ: เปิดแผงผ่าน local-player + event-object + actor-map resolve
(`0x446170`) + relation check (`0x43C380`) + downcast `CNetNPC` (`0x469700`) แล้วเรียก UI manager
`0xAA0710(L"Main_Panel_Target_Enemy_New")` — **ไม่มี GetAttr/name/HP/level read ในตัว handler เอง** ฟิลด์เหล่านี้
เป็น consumer แยกต่างหากหลังแผงเปิดแล้ว (`0x51F920`/`0x51F150`). `TargetVital` (outbound จาก client) ผูก inbound
handler กับ shared no-op stub `0xA106C0` (`xor al,al; ret 4`) — เป็นรายงานขาออก ไม่ใช่คำขอที่ต้องมี response
เพื่อเปิดแผง ⇒ **ไม่มี field/frame ที่ server เขียนได้เพื่อเปิดแผง**, ยืนยัน bounded negative ตามเกณฑ์จบใบ.
`field_mobs.py` ไม่ส่ง BasicAttr level ก็จริง แต่นั่นเป็น consumer หลังเปิดแผง (จะได้ ctor default LV1) ไม่ใช่
gate เปิดแผง — **ห้ามเติม level เพื่อหวังแก้อาการนี้** ตามที่ใบเต็มเตือนไว้ตรงๆ. attended capture ที่แคบที่สุด
(single-click vs Tab-select เทียบ event slot/relation branch) อยู่นอกเขตเขียนของ LANE-B.

**BUILD_IMPACT: NONE** — static ไม่พบ field/response vital ที่ server เขียนได้เพื่อเปิดแผง; การเติม
TargetVital response หรือ BasicAttr level เป็น guess-fix ที่ใบเต็มห้ามไว้ตรงๆ ไม่มีอะไรให้ LANE-B แก้รอบนี้

BUILD_IMPACT_NONE: 1

---

## 🆕🔬 RE-109 ACTOR-NAME-COLOR-BYTE-MAP-001 [STATIC-ON-BRIDGE]: **อะไรในเฟรม census/ประกาศคุมสีป้ายชื่อ (ขาว=ตัวเอง, เขียว=ผู้เล่นอื่น, เหลือง/น้ำเงิน=NPC, ส้ม/แดงเข้ม/เทา=มอนตามสถานะ aggro/ตาย, ชมพูของเราคืออะไร) รวมกรณีตัวละครตัวเองขึ้นส้มด้วย** [🟢 **CLOSED BOUNDED-NEGATIVE/DONE — ปิดโดย RE runner LOCAL 2026-08-27T18:15+07:00, บริโภคโดย LANE-B, ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-109`/`GT-109` = 0 hit ทั้งสองไฟล์ (2026-08-27T17:34+07:00)
> เลขสูงสุดที่ใช้แล้วคือ `108` (`RE-108`/`GT-108`) ⇒ ใบนี้คือ `109`
> 🔴 ใบ `RE-085`-`RE-108` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร
> คำถามนี้ทับซ้อนบางส่วนกับ `RE-067` (ยังเปิด, ของสาย RE เดิม) — ใบนี้ไม่แทน `RE-067`, เป็นใบที่แคบกว่าและมี
> หลักฐานใหม่ (owner reference clips + ตัวละครตัวเองขึ้นส้ม) ที่ `RE-067` ไม่มีตอนเปิด ถ้า RE runner เห็นว่า
> ควรรวมเป็นใบเดียว ให้ตัดสินเองและบันทึกเหตุผลในผล ทั้งสองใบไม่ลบ

### ที่มา
`notes_to_chief/20260827_1635_PANYA-REFERENCE-original-server-combat-loop-colors-death-loot-vs-ours.md`
(Panya, owner reference clips จากเซิร์ฟเวอร์เดิม) + ADDENDUM 16:45/17:0x — เซิร์ฟเวอร์เดิม: มอนยังไม่ aggro
สีส้ม → aggro แดงเข้ม → ตายแล้วเทา. ของเรา (GT-084-R2): มอนสีชมพู/magenta ตลอด **และตัวละครผู้เล่นเอง
(Arena01) ขึ้นสีส้มด้วย** ทั้งที่ควรเป็นสีขาว — ย้อนไปเจอตั้งแต่ `GT-078` (26 ส.ค., บูตไร้แฟล็ก ก่อนมี
faction=1) ⇒ ไม่ได้เกิดจาก faction=1 ที่ wire เข้าไปทีหลัง แต่เป็นไบต์อื่นในเฟรมตัวละครตัวเอง (START_GAME/
selected actor) ที่ client อ่านเป็น "ชนิด/ความสัมพันธ์" เดียวกับที่ทำให้มอนที่ยังไม่ aggro เป็นสีส้ม

### objective
1. หา field/byte ในเฟรม census (`NPCAttr`/`BasicAttr`/relation byte) ที่ client map เป็นสีป้ายชื่อ — ครอบคลุม
   ทั้ง 6 สีที่ owner ยืนยัน: ขาว(ตัวเอง) เขียว(ผู้เล่นอื่น) เหลือง/น้ำเงิน(NPC) ส้ม(มอนยังไม่ aggro หรือตัวเรา)
   แดงเข้ม(มอน aggro) เทา(มอนตาย) และชมพู/magenta ที่ของเราส่งอยู่ตอนนี้คือค่าอะไร
2. อธิบายว่าทำไมตัวละครผู้เล่นเอง (START_GAME/selected-actor frame) ถึงอ่านเป็นสีเดียวกับมอนที่ยังไม่ aggro —
   ตรง field เดียวกันหรือคนละ field ที่บังเอิญ map สีเดียวกัน
3. ถ้า static เห็นไม่พอ ให้เขียน bounded negative พร้อม attended capture ที่แคบที่สุด (เช่น เปลี่ยน relation
   byte ทีละบิตบน identity เดิม เทียบสี)

### nonclaims
① ไม่ claim ว่า `RE-067` ผิดหรือซ้ำซ้อน — ใบนี้แคบกว่าและมีหลักฐานใหม่เท่านั้น
② ไม่ claim ว่าตัวเราขึ้นส้มมาจาก faction byte เดียวกับที่ทำให้มอน aggro เป็นแดงเข้ม — เป็นคำถามเปิด ไม่ใช่ข้อสรุป
③ ถ้าหาไม่เจอในเส้นทางที่ถอดได้ นี่คือคำตอบสมบูรณ์ (bounded negative)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA ตรง verifier ปัจจุบันก่อนเริ่ม
- **T1** — xref field/byte ที่ client ใช้เลือกสีป้ายชื่อ (relation/faction/actor-type mask)
- **T2** — เทียบ path ของ selected-actor(ตัวเอง) กับ path ของ field-mob เพื่อหาว่า field เดียวกันหรือคนละ field
- **T3** — ถ้าไม่เจอ ให้เขียน bounded negative ตามข้อ objective 3

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
byte/field map ของสีป้ายชื่อทั้ง 6 สี พร้อม provenance **หรือ** bounded negative ที่เสนอ attended capture
แคบที่สุด ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**[UPDATE, round B_20260827_1834, 2026-08-27]** ผลข้างล่างมาจาก
`notes_to_chief/20260827_1815_RE-109-RESULT-ACTOR-NAME-COLOR-DRIVER-BOUNDED.md` (RE runner LOCAL) — บริโภคแล้ว
โดย LANE-B รอบนี้ ไม่มี code diff ที่ปฏิบัติได้จากผลนี้ (`BUILD_IMPACT: NONE`), ดูเหตุผลใน result ด้านล่าง

### result

**CLOSED BOUNDED-NEGATIVE/DONE.** เต็มใบ: `notes_to_chief/20260827_1815_RE-109-RESULT-ACTOR-NAME-COLOR-DRIVER-BOUNDED.md`.
Pin ใหม่จาก RE-067/068: `actor_type=3` (ตัวเรา) เข้า `CMyActor → NameBoardPlayer` (`0x456580`) ส่วน
`actor_type=4` (มอน/NPC) เข้า `CNetNPC → NameBoardNPC` (`0x45C560`) — **คนละ board class ตั้งแต่ชั้น
allocator/update** ดังนั้น "ตัวเราขึ้นส้ม" กับ "มอนยังไม่ aggro ขึ้นส้ม" ห้ามสรุปว่าเป็น field เดียวกันจาก RGB
ที่เห็นเท่ากัน. Complete CFG ทั้งสอง body (485/503 instructions, `SPAN_GAP_BYTES=0`) ไม่พบ direct call ไป
`FONT_COLOR` loader (`0x5491B0`) หรือ relationship comparator (`0x4A1D50`) — consumer ที่เหลือเป็น
virtual/resource state ที่ static ยัง resolve receiver ไม่ได้. ค้น `gamedata/**` เจอ `CONSTDATA_TH__FONT_COLOR.tsv`
(57 rows), `CONSTDATA_TH__FACTION.tsv` (38 rows), `MOBS.n_SKIN_COLOR` แต่ไม่มี crosswalk/serializer ที่ผูกตาราง
เหล่านี้เข้ากับ `LABEL_NAME` — ห้าม join จากเลข ID ตรงกัน. เสนอ attended A/B แยก NPC กับ Player สอง experiment
(เปลี่ยนทีละ field/หนึ่งค่า เทียบ frame diff) เป็น method ceiling ถัดไป — RE-109 เองห้าม rerun ด้วย static
direct-call แบบเดิม `BUILD_IMPACT: NONE — ห้าม hard-code สีจาก actor_type/faction 1-6/FONT_COLOR ID/n_SKIN_COLOR
จนกว่าจะมี attended one-field crosswalk`

---

## 🆕🔬 RE-110 AUTO-ATTACK-CADENCE-AND-POSE-FRAME-001 [STATIC-ON-BRIDGE]: **เฟรมตอบ ActionVital แบบไหนสั่งท่าโจมตีปกติของ performer และ client ส่ง ActionVital ซ้ำเองเมื่อได้เฟรมตอบแบบไหน (ต่างจากของเราที่ตีไม่ออกท่า/สแปมคลิกได้ดาเมจรัว)** [🟢 **CLOSED MIXED/BOUNDED-NEGATIVE — ปิดโดย RE runner 2026-08-27T18:32+07:00, บริโภคโดย LANE-B 2026-08-27T19:57+07:00, ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-110`/`GT-110` = 0 hit ทั้งสองไฟล์ (2026-08-27T17:34+07:00)
> เลขสูงสุดที่ใช้แล้วคือ `109` (`RE-109`, ใบก่อนหน้าในรอบเดียวกัน) ⇒ ใบนี้คือ `110`
> 🔴 ใบ `RE-085`-`RE-109` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260827_1635_PANYA-REFERENCE-original-server-combat-loop-colors-death-loot-vs-ours.md` —
เซิร์ฟเวอร์เดิม: คลิกครั้งเดียว → auto-attack loop ต่อเนื่องมีจังหวะ/มีท่า และมอนตีกลับ. ของเรา (GT-084-R2):
ดับเบิลคลิก = ตี 1 ครั้ง **ไม่ออกท่าโจมตี** แต่ดาเมจขึ้น และ **สแปมคลิกได้ดาเมจรัวผิดปกติ** (เซิร์ฟเวอร์ตอบทุก
`ActionVital` ทันทีไม่มี cooldown) — รอบนี้ (companion PR, `pirate-force-server`) ปิดช่องสแปมด้วยค่า
PROVISIONAL ฝั่งเซิร์ฟเวอร์ชั่วคราว ใบนี้ถามค่าจริง/เฟรมจริงจาก client เพื่อแทนค่าชั่วคราวนั้น

### objective
1. หาว่า client ส่ง `ActionVital` ซ้ำเอง (auto-attack loop) เมื่อได้เฟรมตอบรูปแบบไหน — ต่างจากที่เราส่งตอนนี้
   อย่างไร (field ไหนที่เราขาด/ผิด ทำให้ client ไม่ auto-repeat เอง)
2. หาเฟรม/ฟิลด์ที่สั่งให้ performer เล่นท่าโจมตีปกติ (attack pose/animation) — ตอนนี้ของเราไม่ออกท่า
3. หาจังหวะโจมตีขั้นต่ำจริงจาก gamedata (ถ้ามีตารางความเร็วโจมตีต่ออาวุธ/ตัวละคร) เพื่อแทนค่า PROVISIONAL
   ที่ lane B ใส่ชั่วคราวไว้ในโค้ด (grep `ATTACK_CADENCE_MS_PROVISIONAL` ใน `mob_combat.py`)
4. ถ้า static เห็นไม่พอ ให้เขียน bounded negative พร้อม attended capture ที่แคบที่สุด

### nonclaims
① ไม่ claim ว่ามอนตีกลับเป็นขอบเขตใบนี้ — mob-attacks-player เป็นคนละใบ (ยังไม่เปิด, BUILD-005 ขั้นถัดไป)
② ไม่ claim ค่า cadence ล่วงหน้า — ถ้า gamedata ไม่มีตารางตรง ให้บอกตรงๆ ว่าไม่มี ไม่ประมาณ
③ ถ้าหาไม่เจอในเส้นทางที่ถอดได้ นี่คือคำตอบสมบูรณ์ (bounded negative)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA ตรง verifier ปัจจุบันก่อนเริ่ม
- **T1** — หาเฟรมตอบที่ทำให้ client auto-repeat `ActionVital`
- **T2** — หาเฟรม/ฟิลด์ที่สั่งท่าโจมตีของ performer
- **T3** — หาตาราง gamedata ความเร็วโจมตีจริงถ้ามี (แทน `ATTACK_CADENCE_MS_PROVISIONAL`)
- **T4** — ถ้าไม่เจอ ให้เขียน bounded negative ตามข้อ objective 4

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
เฟรม auto-repeat + เฟรมท่าโจมตี + ค่า cadence จริงจาก gamedata (ถ้ามี) พร้อม provenance **หรือ** bounded
negative ที่เสนอ attended capture แคบที่สุด ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

### result
`notes_to_chief/20260827_1832_RE-110-RESULT-POSE-FIELD-POSITIVE-REPEAT-CADENCE-BOUNDED.md` (2026-08-27T18:32+07:00) — mixed:
- **pose (positive):** `ActionVital +0x30` selects attack animation via `EQUIP_VALUE.n_ATTACK_SKILL -> BEHAVIOR.n_ID -> s_ANIMATION`; current server echoes inbound `0xEA7D`, which does not resolve in this gamedata snapshot (no `BEHAVIOR.n_ID=60029`), explaining the missing pose. Six real weapon-type rows resolve; the reply still needs equip-type provenance for Arena01 before picking one, so **no production change this round**.
- **auto-repeat (bounded negative):** complete `CActorTask_UseBehavior::update` body has no direct edge to the local ActionVital producer or action queue. Method ceiling; needs an attended observe-only probe capture, not static.
- **cadence (bounded negative):** all six matched player-attack `BEHAVIOR` rows carry `n_MOB_CD=0`; no named cadence/interval column exists anywhere in `PF_GAMEDATA_COLUMNS.tsv` or the gamedata snapshot. `ATTACK_CADENCE_MS_PROVISIONAL=600` (`mob_combat.py`) has **no real value to replace it with** from this ticket.

`BUILD_IMPACT` (RE runner's own line, followed as-is): server reply should stop treating observed `0xEA7D` as a valid pose selector and prepare to resolve `equipped weapon type -> EQUIP_VALUE.n_ATTACK_SKILL -> ActionVital +0x30`, but should NOT change production composition until an attended one-field A/B confirms actor/equipment provenance; `ATTACK_CADENCE_MS_PROVISIONAL=600` stays, still labeled provisional. **LANE-B consumption:** `mob_combat.py` already carries the provisional label and makes no cadence claim beyond it -- no code change was owed by this result. The pose-selector fix needs equip-type provenance this ticket does not have, so it is not a self-decidable buildable increment either; it stays a `PROVISIONAL`-tagged gap in `mob_combat.py` until that provenance exists. No new RE ticket opened -- the result's own T4 already names the narrowest next attended capture, and re-opening it as a fresh ticket would just restate that.

---

## 🆕🔬 RE-111 LOOT-DROP-RENDER-REQUIRED-FIELDS-001 [STATIC-ON-BRIDGE]: **client ต้องการฟิลด์อะไรใน `MOB_LOOT_DROP` ถึงจะวาดถุงเรืองแสง+ป้ายชื่อสี rarity บนพื้น — เซิร์ฟเวอร์ส่งไปแล้ว 2 ใบ (54B) แต่เจ้าของไม่เห็นอะไรบนจอเลย** [🟢 **CLOSED BOUNDED-NEGATIVE — ปิดโดย RE runner 2026-08-27T18:39+07:00, บริโภคโดย LANE-B 2026-08-27T19:57+07:00, ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-111`/`GT-111` = 0 hit ทั้งสองไฟล์ (2026-08-27T17:34+07:00)
> เลขสูงสุดที่ใช้แล้วคือ `110` (`RE-110`, ใบก่อนหน้าในรอบเดียวกัน) ⇒ ใบนี้คือ `111`
> 🔴 ใบ `RE-085`-`RE-110` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260827_1635_PANYA-REFERENCE-original-server-combat-loop-colors-death-loot-vs-ours.md`
ADDENDUM 16:45/16:5x — เซิร์ฟเวอร์เดิม: ของ drop ตกพื้นเป็นโมเดลถุงเล็กสีเหลืองเรืองแสง + ป้ายชื่อสี rarity
(`ไอเทมยังไม่ประเมิน` สีเขียว) ลอยเหนือถุง คลิกแล้วตัวละครเดินไปเก็บเอง. GT-084-R2 ยืนยันเซิร์ฟเวอร์ส่ง
`[G>] MOB_LOOT_DROP (54 bytes)` ×2 จริง (คอนโซล L11198/11202) แต่**เจ้าของไม่เห็นถุง/ป้ายบนจอเลย** ตัดทิ้ง
ความเป็นไปได้ "ตกแล้วแต่ไม่ได้มอง" แล้ว (owner nonclaim ตรง)

### objective
1. หาโครงสร้างฟิลด์ที่ handler รับ `MOB_LOOT_DROP` ต้องการ (ชื่อไอเทม/rarity/model id/ตำแหน่ง) เทียบกับ 54
   ไบต์ที่เราส่งตอนนี้ — ฟิลด์ไหนขาด/ผิด shape ทำให้ client ไม่ spawn ถุง
2. หา resource/model ที่ client ใช้วาดถุงเรืองแสง (ชื่อ resource ถ้าถอดได้) และ path ที่ผูกป้ายชื่อสี rarity
3. ถ้า static เห็นไม่พอ ให้เขียน bounded negative พร้อม attended capture ที่แคบที่สุด (เช่น ส่ง `MOB_LOOT_DROP`
   ที่ต่างจากปัจจุบันเฉพาะฟิลด์เดียว เทียบว่าถุงขึ้นหรือไม่)

### nonclaims
① ไม่ claim ว่า pickup flow (`RE-082`, ปิดแล้ว) ผิด — ใบนี้ถามเฉพาะขั้น render ก่อนจะถึงขั้นคลิกเก็บ
② ไม่ claim shape ที่ถูกต้องล่วงหน้า — objective 1 เปิดเท่ากันทุกฟิลด์
③ ถ้าหาไม่เจอในเส้นทางที่ถอดได้ นี่คือคำตอบสมบูรณ์ (bounded negative)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA ตรง verifier ปัจจุบันก่อนเริ่ม
- **T1** — xref handler ที่รับ `MOB_LOOT_DROP` หา field ที่ต้องมีถึงจะ spawn drop object บนจอ
- **T2** — หา resource model ถุง + path ป้ายชื่อสี rarity
- **T3** — ถ้าไม่เจอ ให้เขียน bounded negative ตามข้อ objective 3

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
field ที่ขาด/ผิด shape พร้อม provenance **หรือ** bounded negative ที่เสนอ attended capture แคบที่สุด ⇒ ปิดใบ
พร้อมบรรทัด `BUILD_IMPACT:`

### result
`notes_to_chief/20260827_1839_RE-111-RESULT-54B-GROUND-LIST-COMPLETE-PERSISTENT-BAG-UNRESOLVED.md` (2026-08-27T18:39+07:00) — bounded negative:
current 54B is a **complete** generic `GSCN_RunTimeProtocolRes` ground-list element (key + dirty mask 0x12 + full item id + XYZ); `MOB_LOOT_DROP` is our own server-side event name, not a recovered client class. The concrete create/update/consumer graph has zero named lookup of `n_ID_MODEL`; both GT-084-R2 items (2400046/2400047) resolve to `n_ID_MODEL=0` in gamedata, a candidate but not a causal proof. A separate, unresolved family (`FightingDropModule_Client`/`FightingDropNotify`) may be the original loot transport but has no serializer/handler/capture yet.

`BUILD_IMPACT` (RE runner's own line, followed as-is): must not add guessed name/rarity/model bytes to the 54B or change its mask; production must keep telling the truth that there is no persistent/clickable loot object yet. **LANE-B consumption:** checked `mob_loot.py` for any such guess -- none found (it already documents the `n_ID_MODEL=0` ambiguity in its own comments rather than picking a value). No code change owed. The two follow-ups RE-111 itself names (a one-variable item-row A/B, and recovering the `FightingDrop*` family) both need an attended capture this lane cannot run standalone; not re-opened as a fresh ticket since RE-111's own T3 already states them precisely enough to act on later.

---

## 🆕🔬 RE-112 BORNAGAIN-MARKER-RESET-WIRE-ACK-001 [STATIC-ON-BRIDGE]: **หลัง quest 3205 (Q_BORNAGAIN, `Player.ResetMarker(1)`) ถูกเรียก เกมเดิมส่งเฟรมอะไรกลับ (ถ้ามี) — client รอ ack หรือปิด dialog เงียบๆ** [🔴 **CLOSED BOUNDED-NEGATIVE — ปิดโดย LANE-A 2026-08-27T19:45+07:00 (ผลจาก RE runner `20260827_1912_RE-112-RESULT-RESETMARKER-NOOP-ACK-BOUNDED.md`)**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-112`/`GT-112` = 0 hit ทั้งสองไฟล์ (2026-08-27T18:48+07:00)
> เลขสูงสุดที่ใช้แล้วคือ `111` (`RE-111`) ⇒ ใบนี้คือ `112`
> 🔴 ใบ `RE-085`-`RE-111` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260827_1746_COO-DECISION-M2-not-closed-fix-persistence-and-destination-scene-before-passing.md`
สั่งสาย A เพิ่ม option 2 (quest 3205) เข้า dialog Columbus 3021 · gamedata (`20260827_1710_GT106-RESULT-*.md`
④.1) ยืนยัน `MOBS 156 s_QUEST_BEGIN` มี `3205` = Q_BORNAGAIN, `n_VARI_2=1` → lua `Player.ResetMarker(1)`
สาย A เขียน `dispatch_columbus_quest3205()` ให้ refuse เสมอไว้ก่อน (`CORE-REQUEST-019`) เพราะไม่มีคอลัมน์ DB
หรือหลักฐาน wire-ack ของ "save spawn point" เลย

### objective
1. หา wire frame (ถ้ามี) ที่เกมเดิมส่งกลับหลัง `Player.ResetMarker(n)` ถูกเรียกสำเร็จ — เป็น ack/state update
   หรือไม่มีเลย (แค่ปิด dialog ฝั่ง client)
2. ถ้ามี ack ให้ระบุ field/shape ที่ต้องส่งให้ตรง — เพื่อให้สาย A รู้ว่า persist แล้วต้องส่งอะไรกลับด้วย
3. ถ้า static เห็นไม่พอ ให้เขียน bounded negative พร้อม attended capture ที่แคบที่สุด (กด option "ตั้งฐานทัพ"
   ครั้งเดียว เก็บเฟรมขาเข้า/ขาออกทั้งหมดรอบนั้น)

### nonclaims
① ไม่ claim ว่าคอลัมน์ DB ควรมีหน้าตาแบบไหน — เป็นคำถามฝั่ง schema/chief แยกต่างหาก (ดู CORE-REQUEST-019)
   ใบนี้ถามเฉพาะ wire ฝั่ง client
② ไม่ claim ว่า option 2 พร้อมต่อสายจริงตอนนี้ — ยังต้อง refuse จนกว่าใบนี้ปิดและมี schema จริง
③ ถ้าหาไม่เจอในเส้นทางที่ถอดได้ นี่คือคำตอบสมบูรณ์ (bounded negative)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA ตรง verifier ปัจจุบันก่อนเริ่ม
- **T1** — xref `Player.ResetMarker`/`Q_BORNAGAIN`/3205 handler หา response frame (ถ้ามี)
- **T2** — ถ้าไม่เจอ static ให้เขียน bounded negative ตามข้อ objective 3

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
wire frame/ack shape พร้อม provenance **หรือ** bounded negative ที่เสนอ attended capture แคบที่สุด ⇒ ปิดใบ
พร้อมบรรทัด `BUILD_IMPACT:`

### result
`Player.ResetMarker`/`Quest.SetFlag` ทั้งคู่ผูก body เดียวกัน `0x0045FA00` (`xor eax,eax; ret 4`) — ไม่มี
state write/ack request/wait/close ใน Lua binding เอง มี wire class `ReliveMarkerVital 0x3DD6` แยกต่างหาก
แต่ไม่มี crosswalk field/call edge ผูกมันกับ quest 3205 หรือ ResetMarker — corpus ปัจจุบัน = 0 frame ทั้ง
W/R จึงเป็น bounded unknown ไม่ใช่ ack ที่ปิดแล้ว attended capture แคบที่สุดที่เสนอ: กด option "ตั้งฐานทัพ"
ครั้งเดียวบนเซิร์ฟเวอร์ปัจจุบัน เก็บ inbound `QuestOperateVital` + ช่วง no-outbound ทั้งหมด (แยกชั้น wire กับ
client-observable) เต็ม: `notes_to_chief/20260827_1912_RE-112-RESULT-RESETMARKER-NOOP-ACK-BOUNDED.md`

`BUILD_IMPACT:` `CORE-REQUEST-019` ต้องคง named refusal ของ quest 3205 ไว้ — ห้ามเพิ่ม `ReliveMarkerVital`
เป็น ack หรือ silent-success จนกว่าจะมีทั้ง persistence schema ที่ chief อนุมัติ **และ** capture/crosswalk จริง

---

## 🔬 RE-113 GM-UPDATE-STATE-VITAL-NESTED-READER-LAYOUT-001 [STATIC-ON-BRIDGE]: **หลัง `vital_version=0` ผ่านเช็คของ `GM_UpdateGMStateVital` (`0x5A19`) แล้ว nested reader ของ vital นี้เองอ่านฟิลด์อะไรตามลำดับ ยาวเท่าไร — เฟรมที่เราส่งทำให้ `GSCN_RunTimeProtocolRes` ดีด `ErrorData=28317` ทันที** [🟢 **CLOSED PASS/DONE — ปิดโดย LANE-GM รอบ `fmgvbx` 2026-08-27T20:1x+07:00, ดูผลด้านล่าง**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง: `RE-113`/`GT-113` = 0 hit ทั้งสองไฟล์ (2026-08-27T19:33+07:00,
> รวม archive/) เลขสูงสุดที่ใช้แล้วคือ `112` (`RE-112`) ⇒ ใบนี้คือ `113`
> 🔴 ใบ `RE-085`-`RE-112` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
- `RE-105` (CLOSED DONE/PASS, ดูใบนี้ด้านบน): `vital_version` ที่ถูกของ `0x5A19` คือ `0` — เช็คอยู่ใน generic
  VitalData collection reader `[0x005F3E20,0x005F406D)`, prototype bootstrap `0x007299B0` เขียน
  `message+0x10 = 0`
- `GT-107` (attended, `notes_to_chief/20260827_1745_GT107-RESULT-*.md`): ส่งเฟรมตาม RE-105 แล้ว
  (`... 12 19 5A 0B 00 0B 00 0B 00 14 00 00 00 00`) — เช็ค version ผ่านจริง (ไม่มี modal 23065 ของ GT-101
  อีกแล้ว) **แต่** client ดีด `Error 28317 — GSCN_RunTimeProtocolRes ErrorData=28317, 讀取失敗` แล้วปิด
  socket เองก่อนถึง `GT-103`/`BT_GM` ใด ๆ (28317 = 0x6E9D = id ของ `GSCN_RunTimeProtocolRes` เอง — เฟรมที่
  บรรจุ `0x5A19` อยู่ข้างใน)
- payload ที่ส่งตอนนี้ (`gm/state_wire.py`): `u8tag(0x0B)@+0x14` · `u8tag(0x0B)@+0x15` · `u32tag(0x14)@+0x18`
  = 3 ฟิลด์ 9 ไบต์ tagged — เป็น layout ที่ `RE-089` พิสูจน์แค่ "โครงมีสามฟิลด์นี้" (ค่าเดิมจาก
  `PF_SERIALIZER_FIELDS.tsv` ตามที่ `PANYA-ORDER 20260826_1630` อ้าง, `RE-089` verify ซ้ำกับอิมเมจ) ไม่เคย
  พิสูจน์ว่า reader หลังผ่าน version check ต้องการครบตามนี้หรือมากกว่า/น้อยกว่านี้
  [แก้จากร่างแรก - pf-adversary ชี้ว่า `RE-088` เป็นคนละเรื่อง (0x51E9/0x8C77 ไม่ใช่ 0x5A19) ไม่ควรอ้างในบรรทัดนี้]

### objective
1. หา nested reader ของ `0x5A19` เอง (หลัง version-check ทั่วไปผ่านแล้ว) — handler `0x00729F00` (RE-089),
   prototype vtable `0x00F4631C` — อ่านกี่ฟิลด์ ทาง tag/ความยาวแบบไหนต่อฟิลด์ ยาวรวมกี่ไบต์จาก payload
2. เทียบกับ 3 ฟิลด์ 9 ไบต์ที่ `gm/state_wire.py` ส่งอยู่ตอนนี้ — สั้นไป ยาวไป หรือ tag/ลำดับผิดหรือไม่
3. หาว่ามีเงื่อนไขลำดับ/state ก่อนส่ง `0x5A19` หรือไม่ (เช่น ต้องตามหลังเฟรมอื่นก่อน ไม่ใช่ทันทีหลัง
   `StartGameRes`) แยกจากคำถามเรื่อง byte layout ในข้อ 1-2
4. ถ้า static ไม่พอสำหรับข้อ 1-3 ให้เขียน bounded negative ชัดเจน แยกเป็นข้อ ๆ (บอกว่าข้อไหนตอบได้/ไม่ได้)

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA/ตาราง sha256 ตรง verifier ปัจจุบันก่อนเริ่ม
- **T1** — อ่าน handler `0x00729F00` ต่อจากจุดที่ version-check (`RE-105`) ผ่านแล้ว หา loop/sequence ของ
  tag-read call ถัดไป (field count, tag byte, length ต่อฟิลด์)
- **T2** — เทียบผลลัพธ์ T1 กับ 3-ฟิลด์/9-ไบต์ปัจจุบันตามข้อ objective 2
- **T3** — xref เงื่อนไข state/ลำดับก่อนเรียก handler นี้ (ข้อ objective 3) ถ้าเวลาเหลือ
- **T4** — ถ้า T1 ไม่พบเส้นทางที่ถอดได้ ให้เขียน bounded negative ("ต้อง brute-force ความยาว/จำนวนฟิลด์จริง
  จากไคลเอนต์ทีละแบบ") ไม่เดาจำนวนฟิลด์จากเฟรมข้างเคียงที่เป็นคนละ vital

### nonclaims
① ไม่ claim ว่า 3 ฟิลด์ปัจจุบันผิด — อาจจะถูกแล้วและ error 28317 มาจากคนละสาเหตุ (เช่นลำดับ/state ตามข้อ
objective 3) ใบนี้แค่แยกสองความเป็นไปได้ออกจากกัน
② ไม่ claim ว่า `RE-105` ผิด — ใบนั้นตอบเรื่อง version เท่านั้น ปิดแล้วสมบูรณ์ในขอบเขตของมัน
③ ถ้า T1-T4 ไม่พบอะไรเลยในเส้นทางที่ถอดได้ นี่คือคำตอบสมบูรณ์ (bounded negative) ⇒ ส่งต่อ attended
brute-force รอบถัดไปแทน ไม่ใช่ใบที่ค้าง

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
layout ของ nested reader พร้อม provenance **หรือ** bounded negative ที่แยกข้อ 1/2/3 ชัดเจน ⇒ ปิดใบพร้อม
บรรทัด `BUILD_IMPACT:`

**เร่งด่วนกว่าใบอื่นในคิว:** ใบนี้บล็อก `GT-103`/`GT-110` และทาง ข ของ `PANYA-ORDER 1425` (warp ข้ามฉาก)
ทั้งหมด — `localtest` ยังห้ามกลับเข้า `gm_accounts` จนกว่าใบนี้ปิด (กฎเดิมจาก `GT-101`/`GT-107` ยังใช้)

### result

**CLOSED PASS/DONE.** พบสาเหตุจริงของ `ErrorData=28317` — ไม่ใช่โครงฟิลด์ของตัว vital เอง (ข้อ objective 2)
แต่เป็นชั้น envelope ที่อยู่นอกตัว vital (ข้อ objective 1 ตอบได้บางส่วน ผ่านหลักฐานคนละชนิด):

1. **[STATIC]** `gm/state_wire.py` เดิมประกอบเฟรมผ่าน `legacy.make_runtime_vital()` (เอกพจน์) — ฟังก์ชันนี้ใน
   `current/pf_login_game_server_v141.py` (บรรทัด 747-765) **ไม่เติมไบต์ change-mask ท้ายเฟรม**
   ส่วนฟังก์ชันคู่กัน `make_runtime_vitals()` (พหูพจน์, บรรทัด 689-712) เติม `u8tag(0x0B, 0)` ต่อท้ายเสมอ
   พร้อมคอมเมนต์ของตัวมันเองที่เขียนไว้ก่อนใบนี้แล้วว่า: *"RuntimeRes v4 has a second (derived-class) change
   mask after the inherited VitalData collection. Empty RuntimeRes proved this exact trailing 0B 00 on the
   wire; omitting it makes the client over-read the collection response and raise ErrorData=28317."*
2. **[PROVEN — committed report]** พฤติกรรมนี้ถูกพิสูจน์ซ้ำอิสระ 3 ครั้งมาก่อนแล้วใน
   `reports/PF_DELETE_SOFT002_NATURAL_0x36DB_DECODE_20260818.md` §(c) (empty-RuntimeRes experiment, v26
   SelectActorVital 2-tail, V43 combined-actor-stream) — ทุกครั้งที่ envelope `GSCN_RunTimeProtocolRes` v4
   ขาดไบต์ change-mask ท้ายเฟรม client ดีด `ErrorData=28317` เหมือนกัน
3. **[MEASURED — GT-107]** เฟรม 29 ไบต์ที่ `GT-107` ส่งจริงตรงกับสิ่งที่ `make_runtime_vital` (เอกพจน์) +
   payload 3-ฟิลด์ปัจจุบันประกอบออกมาทุกไบต์ — ไม่มีช่องว่างระหว่างโค้ดกับสิ่งที่วัดได้จริงบนสาย จบที่ฟิลด์
   `+0x18` (u32) ของตัว vital เอง ไม่มี `0B 00` ต่อท้าย ตรงกับสมมติฐานข้อ 1-2 เป๊ะ
4. โครงฟิลด์ 3 ฟิลด์/9 ไบต์ของตัว vital เอง (`0x0B`/`0x0B`/`0x14` @ `+0x14/+0x15/+0x18`) **ไม่ใช่ปัญหา** — ยัง
   ตรงกับที่ `RE-089` พิสูจน์ (sha-pinned) — ข้อ objective 2 ปิดด้วยคำตอบ "ไม่ผิด ปัญหาอยู่ชั้นเหนือฟิลด์นี้"

**bounded negative (เหลือค้างโดยเจตนา ไม่บล็อกการปิดใบนี้):**
- ไม่มี instruction address เดียวที่ static เห็นได้ตรง ๆ ว่า "ตรงนี้คือจุดที่ client อ่านไบต์ change-mask ท้าย
  เฟรม" — คำตอบยืนอยู่บนหลักฐาน wire/behavioral คนละรอบ (ข้อ 2-3) ไม่ใช่ disassembly สดของจุดต่อเนื่องนี้
  โดยเฉพาะ — ต้องใช้เซสชัน disassembly บนสะพานถ้าต้องการปิดช่องนี้ให้สนิท ไม่บล็อกเพราะหลักฐานคนละชนิดเพียงพอ
  แล้วสำหรับ objective 1
- ข้อ objective 3 (เงื่อนไขลำดับ/state) ไม่พบหลักฐานทั้งบวกและลบ — ไม่จำเป็นต้องตามต่อ เพราะสมมติฐาน
  change-mask อธิบายอาการที่วัดได้ครบแล้วโดยไม่ต้องอ้างเรื่องลำดับ

**BUILD_IMPACT:** `gm/state_wire.py`'s `make_gm_update_state_frame` เปลี่ยนจากเรียก `legacy.make_runtime_vital()`
เป็น `legacy.make_runtime_vitals([...])` (list ตัวเดียว) แก้แล้วในรอบนี้ (round `fmgvbx`) — เทสท์ regression ใหม่
`tests/test_gm_state_wire.py::test_frame_carries_the_re113_trailing_change_mask_byte` ยืนยันไบต์ท้ายเฟรม
232 เทสของ `gm/` ผ่านทั้งหมดหลังแก้ · **ยังไม่ปิดบล็อกทั้งหมด**: ต้องรอ `CORE-REQUEST-020`
(`field_0x0b_second=1`) ปิดด้วย แล้วค่อยส่ง attended GT รอบใหม่ยืนยันว่า client รับเฟรมจริง (nonclaim: การแก้นี้
มาจากหลักฐาน [STATIC]+[PROVEN]-committed-report ไม่ใช่ [MEASURED] ของรอบนี้เอง — ยังไม่มีใครยิงเฟรมที่แก้แล้วใส่
ไคลเอนต์จริง)

---

## 🔬 RE-115 MAPWINDOW-SCENE-NPC-LIST-SOURCE-001 [STATIC-ON-BRIDGE]: **หน้าต่างแผนที่ในเกม (M) มีรายการ "ค้นหาตัวละครในฉาก" เรียง `MOBS.n_ID` ต่อเนื่อง + ปุ่ม GO! — รายการนี้ไคลเอนต์ได้มาจาก packet ของเซิร์ฟเวอร์ (เช่น census/actor collection ที่ส่งอยู่แล้ว) หรือจากตารางฝั่งไคลเอนต์เอง** [🟡 OPEN]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง (2026-08-28T01:xx+07:00, รวม `notes_to_chief/`, `rounds/`):
> `RE-115`/`GT-115` = 0 hit ทั้ง `CLIENT_RE_QUEUE.md` และ `GAME_TEST_QUEUE.md` — เลขสูงสุดที่ใช้แล้วคือ
> `114` (`GT-114`, ตัวนับร่วม) ⇒ ใบนี้คือ `115`
> 🔴 ใบเดิมทั้งหมดอยู่ที่เดิม ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่

### ที่มา
- `notes_to_chief/20260827_1240_PANYA-EVIDENCE-video2-Port-Royal-NPC-tour-30-NPCs-on-screen-map-window-lists-scene-NPCs-in-n_ID-order-156-163.md`
  ①: เจ้าของถอดคลิป `vAD8TuO3ApA` เห็นหน้าต่างแผนที่ (M) แสดงรายการ 8 แถวแรกตรง `MOBS.n_ID` 156-163
  ต่อเนื่องเป๊ะ (Marine Transport Station Columbus ... Royal Exchange Manager Mackie) พร้อม scrollbar —
  จดหมายเดิมเสนอเองว่า RE runner ควรเปิดใบหาว่า UI นี้อ่านจาก packet ไหนหรือจากตารางไคลเอนต์ ใบนี้เป็นใบที่
  ถูกเสนอไว้นั้น (ยังไม่มีใครเปิดจนถึง `notes_to_chief/20260827_2305_KA1A-NUDGE-*.md` เตือนซ้ำ — ตรวจ grep
  แล้วยืนยันว่ายังไม่มีใบ static เดิมของหัวข้อนี้ในทั้งสองไฟล์คิว)
- `world_population.py`/`world_population_bg0002.py` (bg0001/Bg0002 census composer) เป็นแหล่งข้อมูล NPC ต่อฉากฝั่ง
  เซิร์ฟเวอร์ที่มีอยู่แล้ว — ใบนี้ถามว่า UI นี้พึ่งข้อมูลเดียวกันนี้ (composed actor list ที่ส่งตอน StartGame/arrival)
  หรือพึ่งเส้นทางอื่น (client-side static table, หรือ packet แยกที่ยังไม่ถอด)

### objective
1. หาว่าเมนู "ค้นหาตัวละครในฉาก" ของหน้าต่างแผนที่ (M) ประกอบรายการจากอะไร — census/actor-collection packet
   ที่ server ส่งอยู่แล้ว (ตัวเดียวกับที่ `world_population.py` ประกอบ) หรือ opcode/packet อื่นที่ยังไม่ถูกระบุ
   หรือตารางฝั่งไคลเอนต์ล้วน (ไม่พึ่ง wire เลย)
2. ถ้าเป็น packet: ระบุ opcode/handler และฟิลด์ที่ใช้เรียง (ยืนยันว่าเรียงตาม `n_ID`/`actor_identity` จริงหรือ
   คนละคีย์ที่บังเอิญออกมาเรียงเหมือนกันในคลิปนี้)
3. ระบุว่าปุ่ม GO! (teleport ไปหา NPC ที่เลือก) ใช้พิกัดจาก payload เดียวกันหรือ request ใหม่
4. ถ้า static ไม่พอ ให้เขียน bounded negative ชัดเจนแยกข้อ 1/2/3

### จ็อบ
- **T0 · ด่านคุม** — ยืนยัน image SHA/ตาราง sha256 ตรง verifier ปัจจุบันก่อนเริ่ม
- **T1** — grep/search อิมเมจหา string หรือ UI class ที่เกี่ยวกับหน้าต่างแผนที่ (คำที่เป็นไปได้: "MapWindow",
  "GO", ป้าย UI ภาษาไทย/อังกฤษที่ตรงกับเฟรม `00m10s_MAPWINDOW_npc_list_156-163.jpg`) หา handler/ctor ที่วาด
  รายการนี้
- **T2** — ไล่ย้อนจาก handler ไปหา data source: ถ้าพบ opcode ที่ populate list ให้เทียบกับ opcode ที่รู้จักแล้ว
  (census/arrival ที่ `world_population.py` ส่ง) ว่าเป็นตัวเดียวกันหรือคนละตัว
- **T3** — ถ้าเป็นคนละ opcode ให้ระบุ tag/field layout เท่าที่ static เห็น (ไม่ต้องถอดครบ ถ้าชนเพดานให้บันทึก
  bounded negative)
- **T4** — ตรวจปุ่ม GO! แยก (อาจเป็นแค่ client-local nav ไม่ยิง request ใหม่เลย)

### nonclaims
① ไม่ claim ว่ารายการนี้ต้องมาจาก census packet เดียวกับที่ `world_population.py` ส่ง — นี่คือสมมติฐานที่ใบนี้
กำลังตรวจ ไม่ใช่ข้อสรุปล่วงหน้า
② ไม่ claim ว่า n_ID 156-163 ต่อเนื่องในคลิปพิสูจน์อะไรเกี่ยวกับ wire order — อาจเป็นเรื่องบังเอิญของ UI sort
ฝั่งไคลเอนต์เอง (เช่น sort by ID ก่อนแสดง ไม่ใช่ wire order)
③ ถ้า T1-T4 ไม่พบเส้นทางที่ถอดได้เลย นี่คือคำตอบสมบูรณ์ (bounded negative)

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
แหล่งข้อมูลของรายการ NPC ในหน้าต่างแผนที่พร้อม provenance **หรือ** bounded negative ที่แยกข้อ 1/2/3/4 ชัดเจน
⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**ทำไมมีค่า:** ถ้ารายการนี้เป็น packet ของเซิร์ฟเวอร์และไม่ใช่ census ที่ `world_population.py`/
`world_population_bg0002.py` ส่งอยู่แล้ว จะเป็น opcode ที่ M1/M1-P ยังไม่ได้ส่งเลย — ผู้เล่นจะเห็นเมือง/เกาะ
มี actor ยืนอยู่จริง แต่กด M แล้วค้นหาไม่เจอใครเลย ถ้าไม่ปิดใบนี้ก่อนจะไม่มีใครรู้ว่านี่คือช่องว่างที่ต้องต่อสาย

---

## 🆕🔬 RE-116 NPC-SPAWN-HEADING-SOURCE-001 [STATIC-ON-BRIDGE]: **actor spawn-time orientation มาจากไบต์/ตารางไหนของไคลเอนต์ (ถ้ามีเลย) — MOB_CENSUS ของเราไม่เคยส่งมันมาก่อน**  [🟡 OPEN]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง (2026-08-28T02:33+07:00, รวม `notes_to_chief/`, `rounds/`):
> `RE-116`/`GT-116` = 0 hit ทั้ง `CLIENT_RE_QUEUE.md` และ `GAME_TEST_QUEUE.md` — เลขสูงสุดที่ใช้แล้วคือ
> `115` (`RE-115`, ใบก่อนหน้าในรอบเดียวกัน) ⇒ ใบนี้คือ `116`
> 🔴 ใบ `RE-085`-`RE-115` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260828_0150_M1P-RESULT-PASS-owner-confirms-Prison-Exile-identities-6-gaps-map-window-lead.md`
gap ②: เจ้าของเห็น NPC/มอนทุกตัวบนเกาะคุกขยับ/หายใจจริง แต่หันหน้าทิศเดียวกันหมด ไม่เป็นธรรมชาติ — เซิร์ฟเวอร์
เราไม่เคยส่งฟิลด์ heading จริงให้ actor เลย (`make_remote_movement_attr`'s heading arg เป็น `0.0` มาตลอดทั้ง
bg0001 และ bg0002 จนถึงรอบนี้)

รอบนี้ (LANE-A) หา static-only ในคลังนี้ก่อนเปิดใบ (ผลติดไว้ให้ RE runner ไม่ต้องทำซ้ำ):
- `Bg0002Placement`/`SceneActorPlacement` dataclass ทั้งสอง (`scene2_prison_exile_tables.py`, `population.py`)
  ไม่มีฟิลด์ heading/direction/rotation/facing/yaw เลย
- Raw `gamedata/scene/Bg0002/Bg0002.placements.tsv` มีคอลัมน์ `f32_3`/`f32_4`/`f32_5` ที่ไม่เคยถูก join เข้าตาราง
  ใดๆ — ค่าที่แท้จริง (วัดจริงทั้ง 106 แถว) เป็นเลขกลมช่วง 0-5500 ซ้ำกันข้าม MOBSET คนละชุด ไม่ใช่ค่าต่อเนื่อง
  แบบมุม (ควรจะเป็น 0-360/0-2π ถ้าเป็น heading) — รูปร่างเหมือน radius สามชั้นมากกว่า และสมมติฐาน
  "f32_4/f32_5 = radius" เคยถูกทดสอบและ**ตกไปแล้ว**โดยสาย B รอบก่อน
  (`notes_to_chief/20260827_1030_LANE-B-REPLY-PANYA-ORDER-npc-scene-file-field-interpretation.md` บรรทัด
  11-28: 11/13 placement มี f32_4/f32_5 เหมือนกันทุกตัว (500/800) ทั้งที่ `n_AGGRO` จริงต่างกัน 0 vs 1200)
- `CONSTDATA_TH__MARKER.n_DIRTECTION` (`gamedata/tables/CONSTDATA_TH__MARKER.tsv`, คอลัมน์จริง ยืนยัน offset
  ที่ `gamedata/PF_GAMEDATA_COLUMNS.tsv` แถว 1488-1493) เป็น enum เข็มทิศหยาบ 0-12 จริง แต่ scene 2 มีแค่ 18
  แถว (ไม่ใช่ 97) และไม่มี join key เข้า `Bg0002Placement.n_id`/`placement_index` เลยในโค้ดที่ commit แล้ว —
  แถว `n_ID=2` ตรงพิกัด spawn ที่ pin ไว้ใน `scenarios/world_scene_registry_001.json` เป๊ะ (หลักฐานเอนไปทาง
  ตาราง teleport/arrival waypoint ไม่ใช่ตารางหันหน้า NPC แต่ยังไม่ตัดขาด)
- Wire slot มีจริง ไม่ใช่ stub: `make_remote_movement_attr`'s heading f32 เขียนที่ offset `+0x34` ภายใต้ mask
  bit `0x02` (`current/pf_login_game_server_v141.py:1204-1245`) ยืนยันด้วยรายงาน static-RE ที่ commit แล้ว
  ตรง byte กับ Serial `0x4671C0` (`reports/PF_MOVE_PROJECT001_REMOTE_MOVEMENT_PROJECTION_STATIC_20260818.md`)
  — **แต่** `external/PF_SERIALIZER_FIELDS.tsv` แถว 12-13 จัด `MovementAttr` ที่ address `0x0043BB80` เป็น
  `EMPTY` (arg-copier เปล่า) ซึ่งเป็นคนละที่อยู่กับ `0x4671C0` — ยังไม่ reconcile สองแหล่งนี้ ปล่อยให้ใบนี้ตัดสิน
- bg0001's `_entry()` เคยแก้ปัญหานี้แบบวนสี่ทิศ (`HEADINGS = (0, pi/2, pi, 3pi/2)` คีย์ด้วย
  `placement_index & 3`, `world_population.py:210,343-350`) — **ไม่ได้มาจากตาราง/ข้อมูลไหนเลย เป็นค่าประดิษฐ์
  ล้วน** ไม่ใช่หลักฐานว่ามี heading จริงในตาราง รอบนี้สาย A ใช้วิธีเดียวกันกับ bg0002 (parity คอสเมติก ไม่ใช่
  claim ว่า RE แล้ว — ดู `world_population_bg0002.py`'s `_entry()` docstring) ระหว่างรอใบนี้ปิด

### objective
1. หา consumer ที่ initialize orientation ของ `CNetNPC` ตอน **spawn** (ไม่ใช่ wire-merge consumer ที่พิสูจน์
   แล้วที่ `0x467130` — จุดนั้นรับค่าที่ส่งมาแล้ว ไม่ใช่จุดตั้งต้น) เริ่มจาก `0x45C103`/`0x45D2EA` ที่อ้างใน
   `make_npc_attr`'s docstring เอง (`current/pf_login_game_server_v141.py:1139-1201`) เพราะจุดนั้นเคยสาวฟิลด์
   spawn-time อื่นมาแล้ว
2. เช็คว่า raw `.npc`/placement binary record (ไม่ใช่ TSV ที่ mine แล้ว) มี byte range อื่นนอก x/y/z ที่
   consumer ตอน spawn อ่านเข้า heading offset หรือไม่
3. หา xref ของตัวโหลด `CONSTDATA_TH__MARKER` ว่ามีอะไรอ่าน `n_DIRTECTION` นอกจากโค้ด teleport ผู้เล่นหรือไม่
4. reconcile ชื่อ `MovementAttr` สองที่ (`0x0043BB80` EMPTY vs `0x4671C0` real) — คนละคลาสที่ชื่อชนกัน หรือ
   `PF_SERIALIZER_FIELDS.tsv` จัดผิด
5. ถ้า static เห็นไม่พอ ให้เขียน bounded negative แยกข้อ 1-4 ชัดเจน — **ต้องใช้ `GameClient.local.bin` จริง
   ซึ่ง cloud clone นี้ไม่มี** (ตามที่ pf-static-re รอบนี้ยืนยัน) เลนนี้ทำได้เฉพาะบนเครื่องสะพาน

### nonclaims
① ไม่ claim ว่า f32_3/4/5 ไม่ใช่ heading อย่างเด็ดขาด — วัดจากรูปร่างค่า (เลขกลม ซ้ำข้ามอินสแตนซ์) เท่านั้น
ยังไม่มี consumer xref มายืนยัน
② ไม่ claim ว่า `CONSTDATA_TH__MARKER` ไม่เกี่ยวกับ NPC heading เด็ดขาด — แค่ไม่มี join key ในโค้ดที่ commit
แล้ววันนี้
③ ไม่ claim ว่า bg0001's `HEADINGS` วนสี่ทิศเป็นค่าที่ถูกจริง — เป็นค่าประดิษฐ์ที่ทำให้ดูเป็นธรรมชาติกว่าเดิม
เท่านั้น ทั้งสองฉากรอใบนี้ปิดเพื่อเปลี่ยนเป็นของจริงถ้ามี
④ ถ้า T1-T4 ไม่พบเส้นทางที่ถอดได้เลยจาก static ล้วน นี่คือคำตอบสมบูรณ์ (bounded negative ตาม T5)

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว) · ชนเพดานให้เขียน bounded negative แล้วปิด
ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
แหล่งข้อมูล heading จริงของ actor spawn พร้อม provenance **หรือ** bounded negative ที่แยกข้อ 1/2/3/4 ชัดเจน
⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**ทำไมมีค่า:** ตอนนี้ทั้งเมือง (bg0001) และเกาะคุก (bg0002) ใช้ heading ประดิษฐ์วนสี่ทิศเหมือนกัน — เจ้าของ
เพิ่งยืนยันด้วยตาว่านี่คือช่องว่างที่สังเกตเห็นได้จริง (M1-P gap ②) ถ้ามี heading จริงในข้อมูลไคลเอนต์
จะทำให้ทั้งสองฉากดูเป็นธรรมชาติขึ้นทันทีโดยไม่ต้องเดาเพิ่ม

## 🆕🔬 RE-117 TRACEPATH-GO-BUTTON-REQREPLY-LAYOUT-001 [STATIC-ON-BRIDGE]: **`CTracePathReqVital` (`0x4391`, ขาไป) กับ `CTracePathVital` (`0x2F92`, ขากลับที่เราไม่เคยส่ง) — ต้องตอบฟิลด์อะไรกลับให้ปุ่ม GO! ในหน้าต่างแผนที่เดินได้จริงแทนที่จะค้าง "กำลังค้นหาเส้นทาง..." ตลอด**  [🟡 OPEN]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง (2026-08-28T03:30+07:00, รวม `notes_to_chief/`, `rounds/`,
> `CLIENT_RE_QUEUE.md`, `GAME_TEST_QUEUE.md`): `RE-117`/`GT-117` = **0 hit** ทั้งสองไฟล์ — เลขสูงสุดที่ใช้แล้ว
> คือ `116` (`RE-116`, ใบด้านบน) ⇒ ใบนี้คือ `117`
> 🔴 ใบ `RE-085`-`RE-116` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

### ที่มา
`notes_to_chief/20260828_0235_KA1A-FOUND-GO-button-sends-CTracePathReqVital-0x4391-server-must-answer-0x2F92.md`
(ADDENDUM ต่อ `PANYA-DECISION` 0200 ข้อ ข) — เจ้าของกด GO! ในหน้าต่างแผนที่แล้วจอค้างข้อความสีส้ม
"กำลังค้นหาเส้นทาง..." ตลอด (เห็นรอบ M1-P, ภาพ `M1P_ingame_20260828_prison_exile_pike_deer_*.png`) คอนโซล
M1-P L8925 จับเฟรมขาไปได้จริง 1 เฟรม แต่เราไม่เคยตอบขากลับเลย จึงค้างถาวร ใบ `chief` R204 (2y0zil) consume
จดหมายนี้แล้วแต่ระบุชัดว่า "payload layout ของ 0x4391/0x2F92 และการต่อ handler เป็นงาน RE/LANE-A ไม่ใช่ chief"
(`notes_to_chief/consumed/...KA1A-FOUND...md.CONSUMED.txt`) — ใบนี้คือการเปิดคิวอย่างเป็นทางการตามที่ยังไม่มี
ใครทำ

รอบนี้ (LANE-A) หา static-only ในคลังนี้ก่อนเปิดใบ (ผลติดไว้ให้ RE runner ไม่ต้องทำซ้ำ):
- capture เดียวที่มี: 45 ไบต์ `0x4391` จากคอนโซล M1-P L8925 —
  `12 6F 6E 14 00 00 00 00 08 00 0B 02 12 01 00 12 91 43 0B 00 | 0F E7 02 | 0F 00 00 | 14 00 00 00 00 |
  0F 00 00 | 0F 00 00 | 0F 00 00 | 0F 00 00 | 08 00` — ไม่เคยเห็นเฟรม `0x2F92` เลยทั้งคลัง (สอดคล้องกับที่
  client ไม่เคยได้คำตอบ)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv:107` = `0x4391 CTracePathReqVital`, `:63` =
  `0x2F92 CTracePathVital` · `external/PF_PROTOCOL_REGISTRY.tsv:376-378` มี registry/serializer/handler VA
  ครบทั้งสองคลาส บวก `CGCTracePathModule`
- `external/PF_SERIALIZER_FIELDS.tsv:5521-5536`: **`CTracePathReqVital` resolve แล้วครบ 8 ฟิลด์ทั้ง W/R**
  (ไม่มี `EMPTY`), gate `ALWAYS`, span เดียว `[0x006EBAF0,0x006EBBF7)` — ถอด capture ตาม layout นี้ตรงกัน:
  `u16@+0x14=0x02E7(743)`, ที่เหลืออีก 7 ฟิลด์ (`u16@+0x16`, `u32@+0x18`, `u16@+0x1C/+0x1E/+0x20/+0x22`,
  `u8@+0x24`) = 0 ทั้งหมด — ความหมายของ `743` ยังไม่รู้ (เลขตรงทั้ง `QUEST.n_ID=743` ฉาก 5 และ
  `MOBS.n_ID=743` "Jail Dead Prisoner" — **ห้ามสรุปจากเลขตรงกันเฉย ๆ**)
- **`CTracePathVital` (ขากลับ) ยังไม่ปิด** — `external/PF_PROTOCOL_PRIORITY.tsv:377` = `serializer_status=OPEN`
  บล็อกที่ `direct_call_not_proven_serializer` / `invalid_parameter_import_call_wire_effect_unproved` /
  `invalid_parameter_singleton_register_call_wire_effect_unproved`; `PF_SERIALIZER_FIELDS.tsv:5491-5520` มี
  18 W-field / 12 R-field ที่ไม่ใช่ stub ว่าง — สี่ฟิลด์ `tag 0x14` (f32/u32) ติดกันที่ `+0x0,+0x4,+0x8,+0xC`
  มีรูปร่างเหมือน vec3+scalar (x/y/z/heading?) แต่**ยังไม่ผ่านเกณฑ์ CLOSED** ห้ามใช้เป็น layout จริง
- `external/PF_FIELD_VALIDATION.tsv:752-755`: `CTracePathReqVital W` = `VALIDATED` (observed_frames=1, capture
  ข้างบนนี่เอง) ส่วน `CTracePathReqVital R` / `CTracePathVital W` / `CTracePathVital R` = `NOT_OBSERVED` ทั้งหมด
- gamedata/queue ค้นแล้ว: `TracePath`/`4391`/`2F92` ไม่มีใน `GAME_TEST_QUEUE.md`, `gamedata/PF_GAMEDATA_LUA_INDEX.tsv` — ยังไม่มีใครจองคิวนี้มาก่อน
- roster lookup ที่มีอยู่แล้ว (สาย A ใช้ได้ทันทีถ้า layout ปิด, ไม่ต้องเขียนใหม่): `scene2_prison_exile_tables.py`
  `_by_n_id()` (bg0002, private, :545) และ `population.py` `load_port_royal_placements()` (bg0001, :89) — เป็น
  per-scene ทั้งคู่ ยังไม่มี dispatcher กลางข้ามฉาก แต่ข้อมูลตำแหน่งมีพร้อมสำหรับเกาะคุกแล้ว (Bg0002 97/97)

### objective
1. ปิด `CTracePathVital` (`0x2F92`) serializer ให้พ้น `OPEN` — สาว `SUBCALL`/`PE_IMPORT_INVALID_PARAMETER`
   blocker ที่ `PF_PROTOCOL_PRIORITY.tsv:377` ชี้ไว้จนถึง writer/reader จริง แล้วยืนยันว่าสี่ฟิลด์ `tag 0x14`
   ที่ `+0x0/+0x4/+0x8/+0xC` เป็น vec3(+scalar) จริงไหม หรือเป็นอย่างอื่น
2. ตั้งสมมติฐาน semantic ของ `u16@+0x14=743` ใน `CTracePathReqVital` (quest id / NPC `n_ID` / list index ที่
   client เลือกในหน้าต่างแผนที่) แล้วทดสอบกับตาราง `QUEST`/`MOBS` — ต้องแยกให้ชัดว่าเป็น semantic ที่พิสูจน์แล้ว
   หรือ bounded negative เพราะเลข `743` ชนทั้งสองตารางพร้อมกัน (ห้ามสรุปมั่ว)
3. หา xref ของ handler `0x00710440`/`CGCTracePathModule`: client ทำอะไรกับ response หลังได้รับ (auto-walk
   ด้วย navmesh เอง หรือรอ waypoint หลายจุดจากเซิร์ฟเวอร์) และตรงไหนซ่อนข้อความ "กำลังค้นหาเส้นทาง..."
4. ถ้า T1-T3 ชนเพดาน static ล้วน (ต้องใช้ `GameClient.local.bin` บนเครื่องสะพานที่ clone คลาวด์นี้ไม่มี) ให้เขียน
   bounded negative แยกข้อ พร้อมระบุว่าต้องใช้เครื่องสะพานจริงถึงจะปิดต่อได้

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว/span SHA) · ชนเพดานให้เขียน bounded negative
แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
layout ของ `CTracePathVital` (0x2F92) พร้อม provenance พอให้สาย A เขียน handler ตอบจริงได้ **หรือ** bounded
negative ที่แยกข้อ 1/2/3 ชัดเจนว่าต้องใช้เครื่องสะพาน ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**ทำไมมีค่า:** GO! คือทางลัดที่มีอยู่แล้วในไคลเอนต์สำหรับ "เดินไปหา NPC ตัวไหนก็ได้อัตโนมัติ" — ถ้าต่อ handler
ตอบ 0x2F92 ได้จริง (ด้วยตำแหน่งจาก roster ที่มีอยู่แล้วสำหรับเกาะคุก) ผู้เทส attended ทุกรอบจะประหยัดเวลาเดินเอง
ทุกครั้ง และเป็นหลักฐาน client-observable ตัวแรกว่าเซิร์ฟเวอร์ตอบ pathfinding request ได้จริง
