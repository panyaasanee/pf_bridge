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
## 🆕🔬 RE-095 NPCCONVERSATION-COLUMBUS-QUESTID-CROSSWALK-001 [STATIC-ON-BRIDGE]: **หา quest id / nested descriptor (u16 `+0x10`, u8 `+0x12`) ที่ NPC Columbus ใช้จริงใน `NPCConversation`, แยกจาก quest `3020` (actor `0x2001`/P0 singleton) ที่เซิร์ฟเวอร์ hardcode อยู่ตอนนี้**  [🟢 **OPEN — เปิดโดย LANE-A (สาย A · WORLD) 2026-08-27 ~02:2x (+07:00) ต่อยอดจากผล `RE-094`**]

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

### result (ยังไม่มี — ใบเปิดอยู่)

---

## 🆕🔬 RE-096 VEHICLE-ROW-SEASCENE-CROSSWALK-001 [STATIC-ON-BRIDGE]: **หา `VEHICLE` table row + ความหมายของ `CVehicleVital.+0x18` qword ที่ผูกกับกลุ่มฉากทะเล (`Bg1001`-`Bg1007`, `SCENE_TYPE=4`)**  [🟢 **OPEN — เปิดโดย LANE-A (สาย A · WORLD) 2026-08-27 ~02:2x (+07:00) ต่อยอดจากผล `RE-085`**]

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

### result (ยังไม่มี — ใบเปิดอยู่)

---

## 🆕🔬 RE-097 COLUMBUS-BG0001-PLACEMENT-IDENTITY-001 [STATIC-ON-BRIDGE]: **หา placement/actor identity ของ Columbus (`MOBS.n_ID=36`) ใน 149 plac... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-098 FIELD-MOB-DEFINITION-PAYLOAD-LEVEL-RANK-001 [STATIC-ON-BRIDGE]: **หา parser สำหรับ definition payload 16 ไบต์ต่อ `.npc` (`b5`/`b15... -- archived 20260827 (closed; verbatim in `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 RE-100 SETNUMBER-99-101-SENTINEL-AND-ACTORMOVE-MULTIPOINT-001 [STATIC-ON-BRIDGE]: **เลขชุด `99`/`101+` ที่แทรกกลางลำดับ `.npc` มีความหมายพิเศษฝั่งไคลเอนต์ไหม + `CActorTask_ActorMove` (ผู้บริโภคที่ `RE-083` พิสูจน์แล้วสำหรับ `actor_type 2`) กินลิสต์ XYZ หลายจุดเป็นคิวได้จริงหรือรับได้แค่จุดเดียวต่อครั้ง**  [🟢 **OPEN — เปิดโดย LANE-A (สาย A · WORLD) 2026-08-27 ~08:3x (+07:00) ตอบ `PANYA-ORDER 0440`**]

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

## 🆕🔬 RE-104 GM-EDITOR-WIDGET-OPEN-TRIGGER-001 [STATIC-ON-BRIDGE]: **อะไรเปิด/toggle dedicated GM text-editor widget ที่ `RE-091` พิสูจน์แล้วว่าเป็น producer ของ `GM_RunGMCommandVital` (`0x51E9`) — hotkey, เมนู, ไอคอนที่ปรากฏเมื่อ `GM_UpdateGMStateVital` ตั้งสถานะ GM ให้ connection, หรืออื่น**  [🟢 **OPEN — เปิดโดย LANE-GM 2026-08-27T14:42+07:00 ต่อยอดจากผล `RE-091` nonclaim ②**]

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

### result (ยังไม่มี — ใบเปิดอยู่)

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

### result (ยังไม่มี — ใบเปิดอยู่)
