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

> 🔎 **สถานะการเข้าถึงชุดส่งมอบ (อัปเดต R131 · 2026-08-23 ~21:0x +07:00):**
> ✅ **5/8 ตาราง + ดัชนีเข้า `main` แล้ว** (commit `284d986` · Panya ruling 20:39 "push ทั้งไฟล์ ไม่ mask") —
> cloud/CI อ่านได้แล้ว · ❌ อีก **3 ตาราง (820 แถว): `PF_PROTOCOL_PRIORITY.tsv` · `PF_DATA_EVIDENCE.tsv` ·
> `PF_TAG_CENSUS.tsv`** — จดหมาย 20:39 ยืนยันชื่อ+สะอาดแล้ว · R131 whitelist ใน `.gitignore` ให้แล้ว
> ⇒ เหลือขั้นเดียว: **คนหน้าสะพาน `git add` สามไฟล์นี้** (ดูจดหมาย `FROM_CHIEF_R131_*`) —
> **เลนนี้เปิดครบจริงเมื่อครบ 8 ตาราง**
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
**สถานะ (R137 · 2026-08-24 ~03:0x +07:00):** 🆕 **RE-057 PLACEMENT-INDEX-CROSSWALK-001** เปิดท้ายไฟล์ (Panya เลือก "ทาง ก." จดหมาย 0159 · ร่างเดิมใช้เลข 056 — ขยับเป็น 057 เพราะ 056 ถูก SKILLCAST-DIRECTION-002 ใช้แล้วใน R136) · จ็อบ crosswalk-ในตาราง-commit ของร่างถูกปิดบน cloud แล้ว: **ทั้ง 188 ตารางไม่มีตารางไหนอ้างสคริปต์ที่เรียก `PlacementOFF` เลย (grep ด้วยชื่อไฟล์ — การอ้างด้วย ID ตัวเลขยังตัดไม่ได้จนกว่าจะมี map ชื่อ→ID จากอิมเมจ)** (crosswalk เดียวที่มีคือ `QUEST.s_LUASCRIPT` — ครอบเฉพาะสาย `Quest/`) — ดู `FINDINGS_R137_QUEST_CROSSWALK_HUNT.md` · Panya ยืนยันซ้ำ (จดหมาย 0159 ข้อ ①): **GT-055 ไม่ต้องเปลี่ยนชื่อ** — จุดเริ่ม `RE-` คือ 056 ตามที่หัวไฟล์เขียนไว้แล้ว · ใบเปิดจริงตอนนี้: **GT-055 · RE-056 · RE-057**

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

## 🆕🔬 GT-055 STRING-CODEC-DECISION-001 [STATIC-ON-BRIDGE]: ชี้ขาด "รูปเต็ม" ของ string บน wire 2 จุดที่โค้ดเรากับตารางส่งมอบ Codex ขัดกัน — DeleteActorVital 0x36DB และ chat 0xAC52 + ตอบว่าป้าย `UNTAGGED_*` ของชุดส่งมอบแปลว่าอะไรกันแน่  [🟠 **PENDING — งาน static บนเครื่องสะพานล้วน · ไม่บูต server/client/DB · ไม่มี `LOCK_GAME`/teardown · ไม่มีอะไรให้ดูบนจอเกม**]

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
## 🆕🔬 RE-056 SKILLCAST-DIRECTION-002 [STATIC-ON-BRIDGE]: ตัดสินทิศทาง (outbound/inbound) ของ `TriggerCastSkillVital` ด้วยวิธีที่ "ผ่านด่านตัวควบคุมก่อน" — ไล่ generic registrar `0x5F3DF0` ว่าเก็บ prototype ที่ตารางไหนและใครเดินตารางนั้น (สายที่ GT-050 ยัง exclude ไม่ได้)  [🟠 PENDING — งาน static บนเครื่องสะพานล้วน · ไม่บูต server/client/DB · ไม่มี LOCK_GAME/teardown · ไม่มีอะไรให้ดูบนจอเกม]

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
## 🆕🔬 RE-057 PLACEMENT-INDEX-CROSSWALK-001 [STATIC-ON-BRIDGE]: หา binding จริง trigger → สคริปต์ → ฉาก บนเครื่องสะพาน แล้วตัดสินว่า literal ใน `Scene.PlacementOFF(N)` ชี้ namespace ไหน (ตัวชี้ขาด: 59/60/61 ของ Bg3002 ที่ไม่มีตาราง commit ใดรองรับ)  [🟠 PENDING — งาน static บนเครื่องสะพานล้วน · ไม่บูต server/client/DB · ไม่มี LOCK_GAME/teardown · ไม่มีอะไรให้ดูบนจอเกม]

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
