# PIRATE FORCE — Chief Architect continuation file

## 🔴 ลำดับงานปัจจุบัน — ไมล์สโตนเปิดกลับมา ไม่มีกำหนดวัน (`PANYA-DECISION 20260904_0233` ผ่าน `COO-DECISION 0243` · แทนคำสั่งพัก 2026-09-01T02:15 เดิม)

อ่านหัวข้อนี้ก่อนมอบหมายงานใดๆ ทุกรอบ — milestone (M1-M final/CHARTER-02) กลับมามอบหมายได้ตามปกติ **ห้ามรายงาน
"เลยกำหนด" อีก** (ไม่มีคอลัมน์กำหนดแล้ว) ผ่าน M(n) ก่อนจึงประกาศ v(n) ใบเต็ม:
`notes_to_chief/20260904_0233_*.md` · `notes_to_chief/20260904_0243_COO-DECISION-*.md` ·
ประวัติการพัก: `notes_to_chief/consumed/20260901_0215_PANYA-ORDER-*.md`

### CHARTER-02 — บันไดไมล์สโตน (คอลัมน์ "กำหนด" ถูกลบตาม `0243` ข้อ 2 · กฎสี่ข้อของเวอร์ชัน + วินัยหลักฐานคงเดิม)

- ✅ **M1/v1** เมืองมีชีวิต — ประกาศแล้ว (R249)
- ⏳ **M2/v2** ออกจากเมืองได้ — เหลือเกณฑ์เดียว: แล่นเรือชนเกาะ → หน้า "รายงานกัปตัน เรือเทียบท่า [ชื่อเกาะ]"
  เด้งเอง (ไม่ต้องคลิก · `PANYA-INFO 20260904_0409`) → ผู้เล่นกดยืนยัน → วาปเข้าเกาะ 2 (Prison Exile) และเกาะ 3
  (Spice Paradise) ได้จริงบนจอ **ทั้งสองเกาะ** → **LANE-A**
  🔴 **แก้ถ้อยคำโดย chief รอบ `3kwnnr`/R332 ตาม `COO-DECISION 20260904_0344` ข้อ 2** — ~~"ใกล้เกาะ client ยิง
  `TriggerVital` (`0x1FB2`) → server ตอบ"~~ **ถอน หักล้างแล้ว**: `0x1FB2` id 40/51/3/57/36 = trigger prop
  กลางทะเล (Seafood Cargo/Offer Altar/…) ไม่ใช่ทางเข้าเกาะ (`LANE-A 20260904_0300` จาก
  `TEXTDATA_TH__Trigger_TIP.tsv`) · **อะไรเปิดหน้ารายงานกัปตันยังไม่รู้ = ใบ RE ของ LANE-A** (ร่างรอบ 04:21 ·
  chief ตั้งเลขในรอบที่ใบถึง ตาม `0344` ข้อ 3) · ห้ามใบเทสใบไหนถือ `0x1FB2` เป็นฐานของ "เทียบท่า" อีก
- **M3** สนามมีมอนสเตอร์ (= P-2 ยกระดับ): สีชื่อมอนถูกตามสถานะ **และ** attr + relation/faction ของมอนถูกจริง
  ไม่ใช่แค่ทาสี → LANE-GM (สี) ร่วม LANE-B (attr/relation ของ roster)
- **M4** ตีได้ตายได้ — สี่ข้อครบบนจอ: (1) มอนตีกลับ HP ผู้เล่นลดจริง (2) ตายถูกต้อง ท่าตาย/ชื่อเทา/ไม่มี
  ข้อความ-ตัวนับของผู้เล่น (3) ศพไม่แข็งค้าง (4) เกิดใหม่ได้ (`GT-224`) → LANE-B
- **M5** เก็บของได้ (คงเดิม) — เก็บได้ + รอด relog · หนี้: ของผี 120 วิ · หาง P-1 · ไอคอน/ใช้ของ → LANE-B
- **M final** (ไม่มีเลข แทน M6) — เกมเล่นได้ครบวงจร เกิด-เดินทาง-สู้-เก็บ-โต-กลับมา

- **P-1** ของดรอปต้องอยู่บนพื้นนานพอให้เดินไปเก็บทัน → **LANE-B** (ตัวหลักติ๊กแล้ว · หางค้าง: กะพริบหลัง
  `#689` + หนี้ `DropLedgerCell` = `GT-225`)
- **P-2** สีชื่อมอนต้องถูกสถานะ: ปกติ=ส้ม / สู้=แดง / ตาย=เทา (ห้ามชมพู) → **LANE-GM** ร่วม LANE-B (attr/relation)
  — เกณฑ์ผ่าน M3 ตั้งแต่ `0233`
- **P-3** ทุกปุ่ม/ทุกฟังก์ชันใน GMUI ทั้ง 3 หน้าต้องทำงานจริงครบทุกตัว → **LANE-GM**
- 🆕 UI-A/UI-B (ปุ่มกลับหน้าเลือกตัวละคร/logout) **ย้ายเจ้าของจาก LANE-A ไป LANE-UI** ตาม
  `notes_to_chief/20260904_0330_COO-DECISION-*.md` — ดูหัวข้อ "ทีมและเขตเขียน — สายที่ 6/7" ด้านล่าง
- 🆕 GM-B `/speed` เจ้าของ **LANE-DB** (`COO-DECISION/ORDER 20260901_1059/1100/1101`)
- `GT-146`/ใบตีมอนทั้งหมด **ห้ามเข้าคิว attended** จนกว่า P-2 จะปิด (P-1 ผ่านจอแล้ว)
- **"ตัวละคร" (class/สแตท/HP จากตาราง class)** ไม่เปิดเลนใหม่ (`0243` ข้อ 3) — แถว typed HP/เลเวล = LANE-DB ·
  `class_id` NULL = chief (`GT-215`) · ค่าเริ่มต้น HP/สแตทจากตาราง class = chief ออก CORE-REQUEST ให้ LANE-DB
  เมื่อ `GT-215` ปิด — M4 ข้อ (1) ต้องมีแถวนี้ก่อน

`SERVER_VERSIONS.md` (ที่รากรีโปเซิร์ฟเวอร์) ตารางแผน v2-v-final: ลบคอลัมน์วันที่ตามเดียวกัน — งานถัดไปของ chief
(ยังไม่ลงรอบนี้ เพื่อคุมขนาด PR ให้อยู่หนึ่งเรื่องต่อใบ)

## ทีมและเขตเขียน — 🆕 สายที่ 5: LANE-DB (PERSISTENCE)

ตั้งโดย COO ตามคำสั่งตรงเจ้าของ 2026-09-01T10:5x (`notes_to_chief/consumed/20260901_1059_COO-DECISION-*.md`,
`.../20260901_1100_COO-DECISION-create-lane-db-*.md`, `.../20260901_1101_COO-ORDER-lane-db-first-*.md`)
ลงทะเบียนที่นี่โดย chief รอบ `8zf80f` ตามที่ COO ขอ ("รอบ :51 วันนี้"):

- **ภารกิจ:** persistence ข้าม session แบบ MMORPG จริง — typed columns ใน DB เป็นแหล่งความจริง
  (ความเร็ว/HP/เลเวล/สแตท/EXP/ของสวมใส่/เควส) compose attr block จากค่า typed + บล็อบ creation ของ
  ตัวละครเอง ห้ามเดาฟิลด์ที่ไม่รู้จักเป็นศูนย์ (ข้อห้ามตรงของเจ้าของ ใบ `1059`)
- **เขตเขียนใน `pirate-force-server`:** `migrations/` (ไฟล์เลขใหม่เท่านั้น ห้ามแก้ไฟล์ที่ apply แล้ว) ·
  โมดูลใหม่ `src/pirateforce_foundation/persistence_*.py` · เพิ่ม method ใหม่ใน `store.py` ได้
  แต่ห้ามเปลี่ยน behavior ของ method เดิม · `rounds/DB_*`
- **จุดเสียบ `runtime.py`/`app.py`:** ยังไม่มี — chief สร้างให้ครั้งเดียวเมื่อ LANE-DB ร้องขอ (แบบเดียวกับ
  LANE-B `COO-DECISION 20260830_0046`) ยังไม่มีการร้องขอเข้ามาถึงรอบนี้
- **v141:** ห้ามแตะตลอดกาล เหมือนทุกสาย
- 🔴 **canonical DB (`COO-DECISION 20260901_1112` แก้ทับถ้อยคำใบ `1100`):** เป็นปลายทางที่ LANE-DB
  พัฒนาไปหา ไม่ใช่ของต้องห้าม (1) ยกระดับผ่านไฟล์ migration ของ LANE-DB **ที่ผ่าน pytest +
  pf-adversary แล้วเท่านั้น** รันอัตโนมัติตอน server boot (runner ใน `store.py` +
  `schema_migrations` checksum ledger — migration 003/004 คือแบบอย่าง) (2) ห้ามแก้ไฟล์ `.db` จริง
  ด้วยมือ/SQL ตรง/สคริปต์เฉพาะกิจ นอกเส้น migration เด็ดขาด ไม่มีข้อยกเว้น
  (3) migration ที่แตะแถวข้อมูลเดิม (backfill/UPDATE/rebuild) ต้องมี backup อัตโนมัติ (สำเนาไฟล์ .db
  ก่อน apply) มาก่อนหรือพร้อมกันใน PR เดียวกัน
- 🔴 **ห้ามชี้บูตไปที่ canonical จนกว่าจะมีสามอย่างนี้พร้อมกันใน PR เดียว (`COO-DECISION
  20260901_1241_canon-sha-rotation`, ต่อจาก `1112`):** (1241-①) ด่านตรวจ sha ต้องแยก "sha เปลี่ยนเพราะ
  migration N apply สำเร็จ" (อ่าน `schema_migrations` เทียบ checksum — คาดหมายได้) ออกจาก "sha เปลี่ยน
  เพราะอย่างอื่น" (abort เหมือนเดิม) (1241-②) PR ที่ลง migration ที่แตะ canonical ต้องหมุนค่าใหม่ลง
  `CANON_SHA.txt` พร้อม log ชัดเจนอยู่ใน PR เดียวกันเสมอ ห้ามแยกสองรอบ (1241-③) ต้องระบุชัดว่าใครเป็นผู้บูต
  ครั้งที่ยกระดับ canonical จริง (จ็อบเฉพาะของ LANE-DB หรือแก้ `9001_play_boot.ps1`) — วันนี้ยังไม่มี
  เส้นทางไหนทำ ต้องออกแบบใหม่ ไม่ปล่อยให้เกิดเอง · เหตุผล: ขาดข้อ 1241-①/② = รอบเทส attended ถัดไปจะ abort
  ที่ด่าน sha (`exit 16 canonical mismatch`) แล้วดูเหมือน DB พัง คนจะแก้ด้วยการปลดด่านทิ้งเพราะเข้าใจผิด
  แล้วโปรเจกต์จะเสียตัวจับ corruption ตัวเดียวที่มีอยู่ไปเงียบ ๆ — ตรงกับข้อห้ามของเจ้าของเรื่อง "ปัญหาเงียบ"
  โดยตรง
- **งานแรก:** `/speed <ตัวคูณ>` ใช้เทสได้จริง (ใบ `1101`) — deadline PR แรกภายในรอบ 14:01 วันนี้,
  พร้อมเข้าคิว attended ภายใน 2026-09-02 12:00
- นัยต่อ M4 (ตีได้ตายได้): schema ปัจจุบันไม่มีคอลัมน์ HP เลย — LANE-DB คือตัวปลดล็อกจริง คิวถัดจาก
  `/speed` คือ HP/เลเวล (ตามที่ COO ตั้งข้อสังเกตไว้ในใบ `1100`)

## ทีมและเขตเขียน — 🆕 สายที่ 6: LANE-CS (CLASS / SKILL) และสายที่ 7: LANE-UI (UI / FUNCTIONS)

ตั้งโดย Panya สด (`PANYA-DECISION 20260904_0328`) ผ่าน `COO-ORDER 0329` ลงทะเบียนที่นี่โดย chief รอบ
`spo2u9` ตาม `notes_to_chief/20260904_0330_COO-DECISION-*.md` (แบบอย่างการตั้งเลน: หัวข้อ LANE-DB ข้างบน):

- **LANE-CS** — ภารกิจ: อาชีพหลัก/รอง · สกิลทุกชนิด (basic attack/skill attack/AOE/buff/heal/passive) ·
  สูตรดาเมจ · สนามเทส = หุ่น Training Iron Man `template_id 916` (`RE-155`)
  - **เขตเขียนใน `pirate-force-server`:** โมดูลใหม่ `src/pirateforce_foundation/skill_*.py` `class_*.py`
    `damage_*.py` · `tests/test_skill_*` `test_class_*` `test_damage_*` · `rounds/CS_*`
  - **รับโอน** `skill_attr_hypothesis.py` `learn_skill_request_hypothesis.py`
    `learn_skill_result_hypothesis.py` `damage_model_hypothesis.py` `damage_hp_link_hypothesis.py`
    `stats_progression_hypothesis.py` — chief ยืนยันรอบนี้ว่าไม่มีสายไหนถืออยู่ (grep `HYPOTHESIS_LEDGER.json`
    ไม่พบเจ้าของ) ถ้ามีให้แจ้ง chief
  - **ไม่ใช่ของ CS:** แถวสกิลใน DB (LANE-DB) · HP/ตายของมอน (LANE-B)
  - **จุดเสียบ `runtime.py`/`app.py`:** ยังไม่มี — chief สร้างครั้งเดียวเมื่อ CS ร้องขอ
- **LANE-UI** — ภารกิจ: ปุ่ม/ฟังก์ชัน/ระบบยิบย่อยนอกระบบหลัก (ห้ามแตะ มอน/เควส/คอมแบต/สกิล) เช่น ปุ่มกลับ
  หน้าเลือกตัวละคร · ออกจากเกม · เดินไปหา NPC/มอนอัตโนมัติ · ร้านค้า NPC
  - **เขตเขียนใน `pirate-force-server`:** `src/pirateforce_foundation/ui_*.py` · `tests/test_ui_*` ·
    `rounds/UI_*`
  - 🆕 **เขตเขียนใน `pf_bridge`: `docs/UI_LANE.md`** — ลงทะเบียนโดย chief รอบ `rz1fxh`/R358 ตาม
    `COO-DECISION 20260905_1949` ข้อ 2 · LANE-UI สร้างและเขียนไฟล์นี้ได้เองโดยไม่ต้องขอ chief ·
    สายอื่นห้ามแตะ · **ยังไม่มีไฟล์และยังไม่มีโฟลเดอร์ `docs/` ใน `pf_bridge`** ⇒ LANE-UI สร้างทั้งสองอย่าง
    ในรอบที่เขียนแผน · 🔴 **แก้คำอ้างในใบ `1949`**: ใบอ้าง `docs/GM_LANE.md` เป็น precedent แต่
    **ไฟล์นั้นไม่มีอยู่จริง** — `find . -name "*GM_LANE*"` บน `main` รอบนี้ = 0 hit [วัดแล้ว R358] ⇒
    ทะเบียนนี้เป็นเขตแรกของชนิดนี้ ไม่ใช่การทำตามแบบที่มีอยู่ (แจ้ง COO ในจดหมายรอบ)
  - 🔴 **PANYA-ORDER `20260905_1911` (ผ่าน ka1-A · COO `1948`) — สามข้อ มีผลทันที**
    1. **งานแรกของ LANE-UI = UI-B ปุ่มล็อกเอาต์จริง headless เป็น PR เซิร์ฟเวอร์ ก่อนใบ RE ใหม่ทุกใบ**
       ถัดไปคือ UI-A · `RE-235`/`RE-237`/`RE-261` = รอเครื่อง Panya ห้ามตรวจซ้ำ
    2. **แผนเลนเขียนลง `docs/UI_LANE.md` โดย derive จาก Protocol Registry** ไม่ใช่จากการเดา
    3. **กฎ "ไม่แตะโค้ด 2 รอบติด ⇒ รอบที่ 3 ต้องมี PR ในเขต `ui_*`"** — รอบ 21:16 ไม่มี PR = escalation
  - **รับโอน UI-A/UI-B จาก LANE-A ทั้งสองข้อ** (ปุ่มกลับหน้าเลือกตัวละคร + ปุ่ม logout จริง รวมป้าย
    `BACK_REFUSED` ของ UI-B ตามใบ `1746` ข้อ 2) — **LANE-A เลิกถือ UI-A/UI-B ตั้งแต่รอบนี้** เหลือ M2
    (ออกจากเมืองได้) เป็นงานเดียว
  - **ไม่ใช่ของ UI:** GMUI 3 หน้า (LANE-GM P-3) · ฉาก/เดินทาง/`TriggerVital` (LANE-A M2)
  - **จุดเสียบ `runtime.py`/`app.py`:** ยังไม่มี — chief สร้างครั้งเดียวเมื่อ UI ร้องขอ
- **§7 ล็อกรอบ:** ตัวนำหน้า claim ใหม่ `CS`/`UI` — claim PR หัว `[LANE-CS] round <id>: claim` /
  `[LANE-UI] round <id>: claim` ใน `pf_bridge` (เพิ่มเข้า `AGENTS.md` §7 บรรทัดตัวนำหน้าสายรอบนี้)
- **CORE-REQUEST-022** (login hardcode `class=1`) **โอนเจ้าของให้ LANE-DB** ตาม `0329` ข้อ 2 — chief เหลือ
  เฉพาะจุดเสียบเมื่อ LANE-DB ร้องขอ (ไม่มีแถวเปิดของใบนี้อยู่ในตารางด้านล่างแล้ว ณ รอบที่ลงทะเบียนนี้)
- 🔴 **สองเลนนี้ยังไม่มีอยู่จริงจนกว่า Panya จะวาง routine** (พรอมป์ `0331`/`0332`) — ห้ามใครทำงานของ
  CS/UI แทนระหว่างรอ ยกเว้นข้อ 4 ของ `0329` (LANE-DB ส่งเฟรมรายการสกิลชั่วคราว)

## ทีมและเขตเขียน — 🆕 สายที่ 8: LANE-Q (SCRIPT / QUEST)

ตั้งโดย Panya (`PANYA-ORDER 20260905_2038`/`2039` ข้อ 4) · routine คู่วางแล้ว 21:12 (ka1-A `2112`) · charter
เต็ม `prompts/LANE-Q.md` · ลงทะเบียนที่นี่โดย chief รอบ `5ahimz`/R359 ตาม `COO-DECISION 20260905_2059` ข้อ 7:

- **ภารกิจ**: เป็น Lua host ให้สคริปต์ต้นฉบับของไคลเอนต์ (`gamedata/lua/` 616 ไฟล์ — 306 เควส `q_*`, 309
  ทริกเกอร์ `t_*`) เรียก API เซิร์ฟเวอร์ 160 ฟังก์ชันที่ `PF_LUA_API_SPEC.md`/`PF_GAMEDATA_LUA_API.tsv` ระบุ
  (วัดแล้ว 5 ก.ย.: 0/160 wired) · ลำดับคิว: spike (`lupa`) → `Trigger.*` 17 ฟังก์ชัน (ปลด M2 ให้ LANE-A) →
  `Quest.*` 25 → `Player.*` 73
- **เขตเขียนใน `pirate-force-server`:** `src/pirateforce_foundation/script_*.py` ·
  `src/pirateforce_foundation/lua_api/` · `tests/test_script_*` · `docs/SCRIPT_LANE.md` · `lane_hooks/lane_q_*`
- **เขตเขียนใน `pf_bridge`:** `rounds/Q_*`
- **อ่านได้ แก้ไม่ได้:** `gamedata/lua/` (ต้นฉบับไคลเอนต์)
- **ไม่ใช่ของ Q:** world registry (LANE-A) · combat state (LANE-B) · คอลัมน์สถานะเควสใน DB (LANE-DB เจ้าของ
  ตาราง — Q ขอ interface ผ่าน CORE-REQUEST เหมือนสายอื่น)
- **§7 ล็อกรอบ:** ตัวนำหน้า claim ใหม่ `Q` — claim PR หัว `[LANE-Q] round <id>: claim` ใน `pf_bridge`
- **จุดเสียบ `runtime.py`/`app.py`:** ยังไม่มี — chief สร้างครั้งเดียวเมื่อ Q ร้องขอ
- รอบแรกของ Q (spike ตาม `prompts/LANE-Q.md` คิวข้อ 1) เริ่มแล้ว 21:12 — chief **ไม่ทำ Lua spike ซ้ำ**
  (`2112` แก้ `2038` ข้อ 4) เหลือแค่รีวิว PR ของ Q เหมือนสายอื่นเมื่อมันมา

## ดัชนีรอบเก่า (รอบ 44-178) — ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา

## 0. โครงสร้างทีมคืนนี้ + เช็คก่อนเริ่มทุกครั้ง ⇒ ย้ายคำต่อคำไป [`HOUSE_RULES.md`](HOUSE_RULES.md) (`COO-DECISION 20260903_0848` ข้อ ① · R317 `mgm333` · ไฟล์เป็น ๆ ไม่ใช่ `archive/` กฎยังมีผล ไม่มีอะไรถูกลบหรือย่อ)

---

## CORE-REQUEST registry — ตัวนับเดียวทุกสาย (COO-DECISION 20260826_0656 · ตารางนี้สร้างโดย chief R174 · ตัด+สรุปเหลือเฉพาะแถวเปิด R211 28jd9c)

กติกา: chief เท่านั้นเขียนแถวนี้ · สายเสนอเลขถัดไปในจดหมายตัวเองกำกับ `[เสนอ · รอ chief]` · `ต่อแล้ว` เขียนได้ก็ต่อเมื่อโค้ดอยู่บน `main` แล้วจริง (`COO-DECISION 0401 §③`)

🔴 R211+R229 housekeeping: full table rows 001-026 -> `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` · row 027 (closed, wired R210, merge verified) + R211 preamble + stale WIRED-count note -> `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ตารางข้างล่าง = เฉพาะแถวที่ยังเปิด

(แถวเปิด 011 012 014 015 017 021 026 — สรุปย่อคำต่อคำย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ถ้อยคำเต็มอยู่ใน `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` เหมือนเดิม · เลขจองล่าสุด: 031)

- 031 CORE-REQUEST (สาย A รอบ `xlraox` · `notes_to_chief/20260901_2007_LANE-A-CORE-REQUEST-logout-vitalcount-envelope-gap-classifier-built.md`) — UI-B "ออกจากเกม" จริงยาว 119 ไบต์ (`vital_count=4`) ไม่ใช่ 34 ที่ pin ไว้ (vital อื่นห่อมาด้วย) `classify_logout_attempt` เดิมเช็ค `vital_count == 1` ตกทันที ยืนยันด้วย parser จริง · **ต่อแล้ว (wired) รอบ `f7zt8z` (R295)**: `vital_count >= 1` + `nested_payload` เทียบแบบ branch ตาม `vital_count` (`==1` ยัง exact-equal เท่าเดิม กัน trailing-junk false-accept ที่ pf-adversary จับได้ · `>=2` เทียบ prefix 14 ไบต์) · full suite 6564/0 failed, ledger PASS=49 · `GT-194` `BLOCKED-ON-WIRING`→`READY` (RECHECK 1-3 ผ่าน) — ปิดสมบูรณ์ฝั่ง chief

- 030 CORE-REQUEST-GM-049 (สาย GM รอบ `nqba17`) — `/speed` sparse x=7 runtime send point · **ต่อสายแล้ว (wired) รอบ R294**, เขตเขียนปิดสมบูรณ์ฝั่ง chief · **`GT-193` ยังไม่ READY**: ครึ่ง DB-persistence ของ LANE-DB (`persistence_attr_compose.py`'s sparse write) ยังไม่ขึ้น main · ประวัติเต็ม (blocked/unblocked ข้าม R292-R294, COO gate สามเงื่อนไข, SENSITIVE_FIELDS caveat) → `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260901_row030_full_history.md`

- 028 CORE-REQUEST-GM-047 (สาย GM รอบ `bxkxfc` · P0) — cross-scene GM warp resync label fix, ต่อแล้ว (wired) ยืนยันรอบ `69r41m` (R283): `pf_bridge#680` + `pirate-force-server#452` merged · `GT-182` ปลดเป็น `BLOCKED-ON-ATTENDED` ถ้อยคำเต็ม: `archive/CHIEF_CONTINUATION_ARCHIVE_20260904_row028_full_text.md`

- 029 (สาย A รอบ `s3m1f7`) — ถอนแถว หลังตรวจพบว่าใบนี้ล้าสมัยไปแล้วก่อนถูกเปิดด้วยซ้ำ (ฉาก 4 ต่อสายครบอยู่ก่อนแล้ว server#465 ปิดถูกต้อง ไม่มีงาน chief) ถ้อยคำเต็ม: `archive/CHIEF_CONTINUATION_ARCHIVE_20260904_row029_full_text.md`







- ดัชนีรอบ R174-R288 ทั้งหมดย้ายไป archive แล้ว (เพดาน 30 KB, ยุบบรรทัดซ้ำรอบ `happy-dirac-69cabr` R294):
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260827_R166_R178.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260828_R179_R190.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` (R186-R209 + แถว 027 + WIRED note) ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R210_R214.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R215_R221.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R222_R223.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R224_R230.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R231_R238.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R239_R242.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R243_R246.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R247_R252.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R253_R258.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R259_R261.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R262_R264.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R265_R272.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R273_R280.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R281_R282.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R283_R284.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R285_R286.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R287_R288.md` ·
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R289.md` (moved R296, size housekeeping)
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260902_R290_R291.md` (moved R297, size housekeeping)
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260902_R292_R293.md` (moved R297b, size housekeeping)
- (R294-R303 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md` แล้ว โดย chief รอบ `gjyxt5` (R324) 2026-09-03 ตามเพดาน 30 KB ของหัวข้อ 17 ข้อ 9 (ง) — ไม่มีบรรทัดไหนถูกลบ)

🔴 บรรทัดดัชนีต้องเป็น **หนึ่งประโยค** ชี้ไปไฟล์รอบเสมอ (prompt หัวข้อ 4) — R294-R297b เคยเขียนเป็นย่อหน้ายาว
รวม 9,772 ไบต์จากเพดาน 30 KB · ฉบับเต็มคำต่อคำอยู่ที่ `archive/CHIEF_CONTINUATION_INDEX_R294_to_R298_verbatim_20260902.md`
- ดัชนีรอบ R304-R321 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260904_R304_R321.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ ub8svt, เพดาน 30 KB)
- ดัชนีรอบ R322-R340b ด้านล่างนี้ถูกย่อเหลือหนึ่งประโยคต่อรอบ (chief รอบ ub8svt, เพดาน 30 KB) — ถ้อยคำเต็มคำต่อคำอยู่ที่ `archive/CHIEF_CONTINUATION_ARCHIVE_20260904_R322_R340b_verbatim.md`
- 🔴 ดัชนีรอบเก่ากว่า 20 รอบล่าสุด (RR322-RR341b) ⇒ [`archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md`](archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md) (ย้ายคำต่อคำ R360 · ไม่มีอะไรถูกลบ)
- ดัชนีรอบ R350-R357 -> ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R350_R357.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ `ald09i`/R367)
- ดัชนีรอบ R358-R360 -> ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R358_R360.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ `m6xifr`/R368)
- ดัชนีรอบ R361-R363 -> ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R361_R363.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ `m6xifr`/R369)
- ดัชนีรอบ R364-R366 -> ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260906_R364_R366.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา (chief รอบ `jz5vtt`/R370)
- R367(ald09i) 2026-09-06T09:22+07:00 takeover of `#1440`/R365 (อายุเกิน 3 ชม.แล้วตอนตรวจ): ปิดช่องว่างที่ R365 เปิดค้าง — เสียบ `viewer_identity` ผ่าน `mob_death.hostile_census_frames`/`diag_multi_object_wiring.hostile_census_frames`/`mob_scene_recompose.recompose_frames` ครบสามจุดที่เหลือ + ต่อเข้า `runtime.py` ทั้งสามจุดเรียกจริง (บาร์ตอนตี, dying/dead ตอนตาย) · ต่อสาย LANE-B D11 (`commit_death_and_prepare_hook`+เขียนกลับก่อนยิง hook) · **pf-adversary พบข้อบกพร่องจริง**: เทสสองไฟล์ที่พลาดตอนแรกทำให้ 5 เคสแดงบน commit ที่ push ไปแล้วก่อนชุดเต็มรันเสร็จจริง — แก้ในรอบเดียวกัน (`ff71c44`) ยืนยันชุดเต็มเขียว 12031 passed/365 skipped/0 failed บนต้นไม้ merge origin/main สองรอบ (`#902`,`#903`) · TWO_SESSIONS_SAME_SCENE ตอบแล้วด้วยการอ่านโค้ด `dispatch()` จริง (per-connection instance, ไม่มีทางถึง session อื่น) · GT-275 ร่างเนื้อใบเต็มแล้วแต่ถอนจาก `GAME_TEST_QUEUE.md` รอบนี้เพราะเกต bridgesize แดงจริง (ไม่เข้าข้อยกเว้นแคบของ R364) — เก็บไว้ในไฟล์รอบ รอ archive pass รอบหน้า · archive ดัชนีรอบเก่า R350-R357 ไปไฟล์แยกเพื่อดันไฟล์นี้กลับลงมาใกล้เพดาน (57236->~4x KB) · CORE-REQUEST ใหม่จาก LANE-A (`0914`, world-ground เข้า ground-companion recompose) มาถึงกลางรอบ ยังไม่ทำ ยกเป็นงานที่สองของรอบหน้า -> rounds/R367_ald09i_viewer_identity_combat_recompose_plus_d11_hook_ordering.md
- R368(m6xifr) 2026-09-06T12:22-12:4x+07:00 takeover of `#1440`/R365 (>6h, no real round file, NOW.md already flags it a ghost claim for Panya) -- job (0) archive pass: patched `pf_queue_status.py` to recognize CANCELLED/FAIL (per `0747`), moved 13 closed-not-yet-stubbed GT tickets + 10 closed RE tickets to `archive/*_ARCHIVE_20260906_closed.md`, verified open-ticket count unchanged (102/102) · caught and fixed two header-regex false positives mid-round (`GT-016`, `RE-195` were cross-reference notes, not real ticket headers, wrongly matched and archived -- both restored verbatim) and a same-named-archive-file overwrite (merged instead of clobbered) · **measured, not assumed: the `<=307,200`/`<=204,800` byte targets are unreachable by archiving closed tickets alone** -- GAME_TEST_QUEUE.md 2,280,915->2,176,775 B (still 1.87 MB over; only ~174 KB of the file is closed-ticket content, the rest is 86 open tickets' mandatory evidence blocks) · CLIENT_RE_QUEUE.md 362,594->356,292 B (still 151 KB over) · `[bridgesize]` reads PASS (shrank, didn't grow) · ASK-COO with the math + options sent, did not stop and wait · ADVERSARY_PENDING `pf_bridge#1479` -> rounds/R368_m6xifr_archive_pass_open_count_invariant_plus_the_cap_the_math_says_is_unreachable.md
- R369(m6xifr) 2026-09-06T12:51-13:1x+07:00 [same session, follow-up to R368] pf-adversary's review of R368 returned after unlock and merge, found two real defects: (1) extraction cut ticket sections at "next header of any level" instead of "next ticket header," leaving ~16/22 tickets' own `### steps/pass-criteria/nonclaims` subsections orphaned headerless in the live files (~214 KB, nothing lost, just structurally broken) (2) `RE-234` has two headers in the source file (one DONE, one genuinely OPEN) and R368's script archived the OPEN one as closed -- a real violation of "never touch an untested ticket," confirmed directly against the commit, not just taken on the adversary's word (its 3rd claim, that RE-195 was never fixed, was independently checked and found false -- R368's RE-195 fix was correct) · reverted `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`/both `archive/*_20260906_closed.md` byte-for-byte to pre-R368 (`b8891a8`, diff verified empty, no other lane touched these 4 files since) rather than patch in place -- same failure mechanism twice in one sitting, stopped rather than risk a third · kept the orthogonal `pf_queue_status.py` CANCELLED/FAIL patch · `[bridgesize]` now RED on purpose (reverting to the larger, correct content reads as "grew" against the already-merged corrupted base) -- recorded plainly, not hidden · byte-cap-unreachable conclusion from R368 still holds, only its cited numbers are now stale -> rounds/R369_m6xifr_revert_the_archive_pass_adversary_confirmed_it_corrupted_two_files.md
- R370(jz5vtt) 2026-09-06T13:52-15:0x+07:00 takeover of `#1440` (>14h, dirty, NOW.md ghost) -- **PANYA-ORDER `1315` implemented**: the reaper's no-marker path now closes two owner-authorised categories in `pf_bridge/.github/workflows/merge-claude-pr.yml` -- (1) a stale claim (claim title + no `rounds/` file beyond `*_claim.md` + **head commit** older than `PF_REAP_STALE_CLAIM_HOURS=3`, so the `_claim.md` checkpoint COMMON already asks for buys another 3h; `updated_at` deliberately not used) and (2) an author-declared `SUPERSEDED-BY: #n`/`DUPLICATE-OF: #n` at line start in the body or the author's own latest comment, target must be a PR in the same repo, merged or open -- both keep the branch, both write `notes_to_chief/<time>_REAPER-CLOSED-<repo>-<n>.md` via the contents API · answered the owner's collision question: **no collision with `#1430`** -- that guard only looks at MARKED PRs, this only at UNMARKED ones, and both ask the same question with the same `PF_ROUND_FILE_FILTER` (one criterion, two paths) · 🔴 measured mismatch reported rather than papered over: category (1) **refuses `#1440`** because its branch does carry a real round file (R365, 71 lines) -- its real defect is `dirty`, so chief commented `SUPERSEDED-BY: #1491` and it goes out through category (2); widening (1) to catch it would also catch finished rounds still owed a marker · `server#894` commented `SUPERSEDED-BY: #906` (verified #906 merged and says so itself) · cross-repo record measured impossible today (`grep secrets\.` = 0 hit in both workflows) -> optional named secret `PF_BRIDGE_NOTES_TOKEN`, never a silent close · validation before push: duplicate-key-rejecting yaml load, `bash -n` on both `run:` blocks, ASCII-only, and a **10/10 logic self-test on fixtures before touching anything live** (R369's lesson applied in the right order) · did NOT touch any queue file on purpose (bridgesize red, ASK-COO `1234` unanswered, LANE-K is the clerk now) · 🔴 debt stated plainly: three CORE-REQUESTs needing `runtime.py` (UI `2006`, A `0914`, B `1952`) are R371 jobs 1-3, second round in a row they have not moved · `ADVERSARY_PENDING pf_bridge#1491` -> rounds/R370_jz5vtt_reaper_closes_ghost_claims_and_author_declared_supersedes.md
