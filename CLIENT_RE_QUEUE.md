# CLIENT RE QUEUE — คิวงานแกะไคลเอนต์/capture (static · ไม่เปิดเกม)

> **ไฟล์นี้เกิดจากคำสั่ง Panya 18:22 (+07:00) 2026-08-23** (`notes_to_chief/20260823_1822_PANYA-ORDER-split-queue-into-two-and-search-RE-deliverable-first.md`)
> — แยกใบ **แกะไคลเอนต์/capture** ออกจากคิวเทสเกม **ตั้งแต่ใบใหม่เป็นต้นไป** (ใบ static เก่า GT-040/042/044/046/047/048/049
> ยังอยู่ใน `GAME_TEST_QUEUE.md` ตามกติกาห้ามย้ายใบเก่า — สารบัญหัวไฟล์นั้นเป็นตัวเชื่อม)

**ผู้รับงาน:** คนหน้าเครื่องสะพานของ Panya (มีอิมเมจ client + capture + ไฟล์ข้อมูลเกมบนดิสก์) — **ไม่ใช่ผู้เทสหน้าจอเกม**
**กติกาไฟล์นี้:**
- ทุกใบในไฟล์นี้ **ไม่ต้องเปิดเกม · ไม่ต้องจับ `LOCK_GAME` · ไม่มี teardown · ไม่แตะ canonical DB · ไม่มีอะไรให้ดูบนจอเกมเลย**
  ⇒ ทำขนานกับรอบเทสเกมได้เสมอ ไม่แย่งทรัพยากรกัน
- **เลข `GT-xxx` เป็นชุดเดียวกับ `GAME_TEST_QUEUE.md` ต่อเนื่องกัน** — ห้ามแยกชุดเลข (การอ้างข้ามใบต้องไม่พัง)
- คิวเทสเกม (attended · ขับ UI · ใช้ตา) อยู่ที่ **`GAME_TEST_QUEUE.md`** เช่นเดิม
- 🔴 **กฎบังคับ (คำสั่ง 18:22 ข้อ ④): ก่อนถอด/parse อะไรใหม่ ต้องค้นชุดส่งมอบ RE ของ Codex ก่อนเสมอ**
  เริ่มที่ดัชนี **`pf_bridge\external\00_SEARCH_HERE_FIRST.md`** · ทุกใบต้องกรอกช่อง
  `ค้นใน pf_bridge\external\ แล้ว: เจอ <อะไร> / ไม่เจอ` ในผล · **ถ้าเจอ ⇒ ใบเปลี่ยนจาก "ไปถอด" เป็น
  "verify sha → re-derive ปฏิปักษ์ → ใช้ต่อ"** (แบบเดียวกับ GT-050)
- ผลส่งกลับทางเดิม: จดหมายใน `notes_to_chief/` + กรอกช่อง **result:** ท้ายใบ · sha ก่อน-หลังของทุกไฟล์ที่พึ่งต้องตรงกัน

**📊 รายการค้างที่ Panya ขอให้มองเห็นได้ (คำสั่ง 18:22 ข้อ ⑤):** ชุดส่งมอบ RE = **8 ตาราง 17,626 แถว** ·
ผ่าน re-derive ปฏิปักษ์แล้ว (GT-042) · 🔴 **ยังไม่มีโค้ดใน `src/` `tools/` `tests/` อ่านมันแม้แต่บรรทัดเดียว**
(ข้อห้ามเขียนโมดูล/encoder เพิ่งปลด 2026-08-23 02:03 · GT-050 คือผู้ใช้รายแรกที่วางแผนไว้ · เลน headless สกิลจะเป็นผู้ใช้ฝั่งโค้ดรายแรกหลัง GT-050 ปิด)

> 🔎 **สถานะการเข้าถึงชุดส่งมอบ (R129 · 2026-08-23 ~19:00 +07:00):** `external/` **ยังไม่เคยเข้า git เลย** —
> `.gitignore` ของ repo นี้เป็น deny-all และไม่เคย whitelist โฟลเดอร์นี้ ⇒ ตาราง 8 ใบอยู่บนดิสก์เครื่องสะพานเท่านั้น
> (คนหน้าสะพานเปิดอ่านได้ตามปกติ — path `pf_bridge\external\` ในใบทุกใบหมายถึงสำเนาบนดิสก์นั้น)
> แต่ **ฝั่ง cloud/CI มองไม่เห็น จึงยังเขียนโค้ด/เทสที่อ่านตารางไม่ได้** · R129 whitelist รายชื่อไฟล์แล้ว
> **เฉพาะ 5/8 ตารางที่รู้ชื่อ + ดัชนี** — ขั้นถัดไป: **คนหน้าสะพาน `git add` รายไฟล์ตามจดหมาย `FROM_CHIEF_R129_*`**
> (ปลด 5 ตารางแรก ≈16,803 แถว) · อีก 3 ตาราง (~823 แถว) ยังไม่รู้ชื่อไฟล์ ⇒ ต้องรอคำตอบชื่อจริงจากหน้าเครื่อง
> แล้ว chief whitelist เพิ่มอีกหนึ่งรอบ — **เลนนี้เปิดครบจริงเมื่อครบ 8 ตาราง ไม่ใช่หลัง add รอบแรก**

**ลำดับที่เสนอ (R128):** **GT-053 (ถูกสุด · ชี้ขาด H1) → GT-052 → GT-050** · รายละเอียด H1 อยู่ `FINDINGS_R128_GT051_RENDER_SYNTHESIS.md`

---
## 🆕🔬 GT-052 CLASS-SKILL-TABLE-001 [STATIC-ON-BRIDGE]: dump ตารางอาชีพ + ตารางสกิลจาก `B_CONSTDATA_TH.pc_.dec` (ท่าเดียวกับ GT-044) แล้วผูกกับ 6 อาชีพที่เห็นจากไอคอน  [🟠 **PENDING — งาน static บนเครื่องสะพานล้วน · ไม่บูต server/client/DB · ไม่มี `LOCK_GAME`/teardown · ไม่มีอะไรให้ดูบนจอเกม**]

> 🔢 **หมายเหตุเลข (chief):** ร่างในจดหมาย 1656 ข้อ ④ เสนอใบนี้เป็น **GT-049** แต่ **GT-049 ถูกใช้ไปแล้ว**
> (LOOT-CHAT-TEMPLATE-001 · เปิดใน R127) ⇒ ใบนี้ขยับเลขเป็น **GT-052** · เนื้อหาคงตามร่าง 1656 ข้อ ④ ทุกประการ

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
- **เครื่องมือ:** `parse_pc_tables.py` (ตัวเดิมที่ GT-044 ใช้ parse SCENE_NAME/MAP_SCENE_LIST และ STANDARD_MOB) ·
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
- **result:** · 🔴 ช่องบังคับ (คำสั่ง 18:22): `ค้นใน pf_bridge\\external\\ แล้ว: เจอ <อะไร> / ไม่เจอ` · (ผู้รับงาน static บนสะพานกรอก: จำนวนอาชีพ/สกิล + ไอดี + ฟิลด์ + ตัวอย่างแถวจริง · path TSV + sha256 ทุกไฟล์ ·
  ผลผูก 6 ไอคอน (ตรง/ต่างตรงไหน) · สถานะ census ดัชนีตาราง · เวลา · sha ไฟล์ constdata ก่อน-หลัง)


## 🆕🔬 GT-050 SKILLCAST-WIRE-001 [STATIC-ON-BRIDGE]: **ตรวจแล้วใช้** (ไม่ใช่ไปถอดใหม่) แถวสกิลจากชุดส่งมอบ RE ของ Codex — verify sha ของ `TriggerCastSkillVital`/`CLearnSkillVital` · re-derive ปฏิปักษ์ · ปิด `CLearnSkillResultVital` · หาทิศทาง+ตัวจุดชนวนของ `TriggerCastSkillVital`  [🟠 **PENDING — งาน static บนเครื่องสะพานล้วน · ไม่บูต server/client/DB · ไม่มี `LOCK_GAME`/teardown · ไม่มีอะไรให้ดูบนจอเกม**]

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
- **result:** · 🔴 ช่องบังคับ (คำสั่ง 18:22): `ค้นใน pf_bridge\\external\\ แล้ว: เจอ <อะไร> / ไม่เจอ` · (ผู้รับงาน static บนสะพานกรอก: ผล verify sha สาม span · ผล re-derive ปฏิปักษ์ · ประโยคทิศทาง+ตัวจุดชนวนของ `TriggerCastSkillVital` +VA ·
  สถานะ `CLearnSkillResultVital` · xref chain span/file-offset/len/sha256 ทุกฟังก์ชัน · สถานะ census indirect · เวลา · sha อิมเมจ+TSV ก่อน-หลัง)

## 🆕🔬 GT-053 SCENE2-NATIVE-IDENTITY-CROSSCHECK-001 [STATIC-ON-BRIDGE]: ไฟล์ฉาก native ของ scene 2 มี placement index 60 (`0x203D` Fighting Fish soldier) จริงไหม — จุดเดียวที่ตรวจแล้วอาจฆ่า H1 ได้ทันที  [🟠 **PENDING — งาน static บนเครื่องสะพานล้วน · ไม่บูต server/client/DB · ไม่มี `LOCK_GAME`/teardown · ไม่มีอะไรให้ดูบนจอเกม**]

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
- **result:** · 🔴 ช่องบังคับ (คำสั่ง 18:22): `ค้นใน pf_bridge\\external\\ แล้ว: เจอ <อะไร> / ไม่เจอ` · (ผู้รับงาน static บนสะพานกรอก: ชื่อโฟลเดอร์+ไฟล์ฉาก scene 2 + เส้นทาง resolve จาก GT-044 · N placement ทั้งหมด ·
  index 60: identity/template/preset + offset + f32 triple · ผลเทียบ triple กับค่า authentic P60 (`21421.0059/9277.1123/590.6788`) ·
  คำตัดสิน H1 รอด/ตาย (band membership) หรือ "ตอบไม่ได้" · เวลา · sha ไฟล์ฉาก+TSV ก่อน-หลัง)
