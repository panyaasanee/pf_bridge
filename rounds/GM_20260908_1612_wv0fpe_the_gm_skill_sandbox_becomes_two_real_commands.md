# LANE-GM รอบ `wv0fpe` — สนามซ้อมสกิลของ GM เลิกเป็นคำสั่งบนกระดาษ กลายเป็นคำสั่งจริงสองตัว

รหัสรอบ: `GM_20260908_1612_wv0fpe` · เริ่ม 2026-09-08T16:12+07:00 · claim `pf_bridge#1918`
สาย: LANE-GM (TOOLS) · กิ่ง: `claude/elegant-ptolemy-wv0fpe` (bridge) · `claude/hopeful-babbage-wv0fpe` (server)

## รอบนี้ขยับ NOW/M ข้อไหน
- **`NOW.md` → LANE-GM "งานแรก = `1455`: `/job`+`/skill all`+เทสปฏิเสธ (`COMMAND_REFUSED`)"** — จ่ายครบทั้งสามส่วนในรอบเดียว ไม่ได้ส่งแค่ `/job` ตามทางถอยที่ COO อนุญาตไว้
- **บันได M: ไม่ขยับ และตั้งใจไม่ขยับ** — นี่คือ**เครื่องมือไปถึงสภาพที่จะเทส** ไม่ใช่ขั้นบันได (`prompts/LANE-GM.md` ประโยคที่ 3) · M2 ยังอยู่ที่ LANE-A (`#1144`) · M-final ได้ประโยชน์ทางอ้อมคือ K ทดสอบสกิลทุกคลาสได้โดยไม่ต้องสร้างตัวละครห้าตัว
- ยืนยันต้นรอบ: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 ไบต์)
- นาฬิกา: heartbeat ล่าสุด `2026-09-08T16:08:01+07:00` · เวลาของผมตอนเริ่ม `16:12` → ห่าง **4 นาที** สะพานไม่ค้าง

## ล็อกรอบ
list `[LANE-GM] round ...: claim` ที่เปิดอยู่ใน `pf_bridge` → **ไม่มี** (ใบเปิดอยู่ตอนนั้น: `#1916` DB · `#1913` UI · ที่เหลือเป็น addendum ของสายอื่น ไม่ใช่ล็อกของผม) ⇒ เปิด `#1918` แล้ว list ซ้ำ ไม่มีใบ `[LANE-GM]` เก่ากว่า ⇒ ผมถือล็อก

## ทำอะไร (โค้ดที่ผู้เล่น—ในที่นี้คือผู้เทสที่หน้าเกม—เห็นผลได้จริง)
PR เซิร์ฟเวอร์: **`pirate-force-server` กิ่ง `claude/hopeful-babbage-wv0fpe`** (เลขใบอยู่ท้ายไฟล์)

### 1. `/job <class_id>` — `gm/job_command.py` (ใหม่)
- เขียน `characters.class_id` ผ่านประตูเดิมของ LANE-DB `store.write_typed_attributes` ประตูเดียวกับที่ `/lv` เขียน `level` · ไม่ขอ store method ใหม่ ไม่เพิ่มคอลัมน์
- รับเฉพาะ `(1, 2, 4, 16, 32)` **อ่านจาก `class_catalog.CLASS_IDS`** ไม่ใช่ literal · ค่าอื่น (เช่น `3` ซึ่งเป็นกับดักของบิตมาสก์) = ปฏิเสธ **พร้อมพิมพ์ห้าค่าที่รับได้** ไม่เงียบ ไม่เดา
- โทเคน: `GM_JOB cid=<n> class_id_from=<a|none> class_id_to=<b> relog_required=yes`
- **`relog_required=yes` เสมอบนเส้นทางสำเร็จ และเป็นค่าที่วัด ไม่ใช่ค่าที่เดา**: คำสั่งนี้ไม่ส่งเฟรมใดเลย และที่เดียวที่ `class_id` ถึงไคลเอนต์คือ actor ตอน login (`legacy_bridge.start_game`) · เฟรมที่จะเปลี่ยนสดคือ sparse `UpdateAttrVital` ที่ `GT-193`/`GT-218` วัดว่าฆ่าไคลเอนต์ — โมดูลนี้ไม่ import `attr_wire` เลย
- 🔴 **จุดที่ผมตั้งใจไม่ลอก `/lv`**: `/lv` ต้องถาม `read_character_vitals_or_none` ก่อนยอมรับการเขียน เพราะ vitals ของ login เป็น all-three-or-none · **คลาสไม่ได้ขี่ประตูนั้น** (`legacy_bridge` เขียนไว้เองว่า "THIS IS NOT AN ALL-OR-NONE PAIR") และ `session.py` อ่านคลาสจาก `read_typed_attributes` ⇒ การเช็ค read-back **คือ**คำถามของ login สำหรับคำสั่งนี้ · ถ้าลอกด่านของ `/lv` มาจะปฏิเสธการเขียนที่ login รับอยู่แล้ว

### 2. `/skill all` — `gm/skill_all_command.py` (ใหม่)
- แจกทุก id ใน `class_skill_curriculum` (137 ตัว = ห้าคลาส + ถัง `1024` 11 ตัว) ผ่าน `store.grant_learned_skill` ทีละ id ตามสัญญาของประตูนั้นเอง
- **idempotent เพราะประตูเป็น `INSERT OR IGNORE` บน `UNIQUE(character_id, skill_id)`** — พิมพ์ซ้ำได้ `granted=0 already=137`
- **ห้าม hardcode**: id มาจากตารางที่ pin ด้วย sha256 · และมีเทสที่อ่าน**ตัวไฟล์**แล้วแดงถ้ามี id ตัวใดโผล่เป็น literal ในซอร์ส (กันคนรุ่นหลังแปะ fallback list)
- ถัง `1024` **แจกพร้อมห้าคลาสและถูกเรียกชื่อบนคอนโซล** ไม่กลืนเงียบ — เพราะความหมายของ 1024 ยัง NOT PROVEN (docstring ของ `class_skill_curriculum` เอง)
- โทเคน: `GM_SKILL_ALL cid=<n> granted=<k> already=<m> classes=1,2,4,16,32,1024` · **`failed=<k>` โผล่เฉพาะเมื่อไม่เป็นศูนย์** ⇒ รันที่พังบางส่วนอ่านเป็นรันสะอาดไม่ได้

### 3. ประตูความปลอดภัย — ไม่มีประตูใหม่แม้แต่บานเดียว
ทั้งสองคำสั่งเป็นพี่น้องของ `/lv` ใน grammar เดียว ⇒ ผ่าน `chat_command.handle_local_talk_chat` (ด่านตัวตน `REFUSAL_NOT_GM`) และด่าน canonical-DB (`_speed_db_is_canonical`, fail-closed) ที่ยืนอยู่ **เหนือ** การเขียนทุกครั้ง

## หลักฐานสองชั้น (แยกกัน ห้ามใช้ชั้นหนึ่งอ้างอีกชั้น)
- **ชั้น DB/wire** — `tests/test_gm_job_and_skill_all_commands.py` 43 เคส · `JobPersistenceTests`/`SkillPersistenceTests` รันกับ `SQLiteStore` จริงบนไฟล์ temp แล้วอ่านกลับผ่าน **store ตัวที่สอง** ที่เปิดไฟล์เดียวกัน · `test_the_next_login_reads_this_exact_column` ถาม `session._class_id_on_the_row` ซึ่งเป็นฟังก์ชันที่ login เรียกจริง ไม่ใช่สำเนา logic
- **ชั้น client-observable** — **ยังไม่มี และรอบนี้ไม่อ้างว่ามี** · หน้าต่างสกิลจะเปลี่ยนก็ต่อเมื่อ LANE-CS เสียบ `#1079` เข้า `runtime.py` (งานแรกของ CS ตาม NOW) · ต้องบูต attended ถึงจะรู้ว่าท่าไหนออก
- **การปฏิเสธ = รันจริง ไม่ใช่ grep ข้อความตัวเอง** (เจ้าของย้ำเอง ผิด = ตัดใบ): `test_a_non_gm_reaches_a_real_store_and_still_writes_nothing` ต่อ `SQLiteStore` จริงที่มีตัวละครจริงและมีประตูเขียนครบ เข้ากับ session ของบัญชี `DECKHAND` แล้วพิมพ์ทั้งสองคำสั่ง → เปิด DB ใหม่แล้ววัด: **ไม่มี `class_id` ในแถว · `character_skills` เท่าเดิม**

## nonclaims (ตัวที่ต้องอ่านก่อนอ้างผลนี้ที่ไหนก็ตาม)
1. **แถวที่เขียน ≠ สกิลบนจอ** · ยังไม่มีไคลเอนต์เห็นผลของทั้งสองคำสั่งในรอบนี้
2. `/job` ที่สำเร็จ **ไม่ใช่**หลักฐานว่าระบบเลือกอาชีพทำงาน · `/skill all` **ไม่ใช่**หลักฐานว่าระบบเรียนสกิลทำงาน — GM ข้ามขั้น "เรียน" ทั้งขั้น ไม่หักแต้มสกิล ไม่ผ่านเลเวล
3. ยังไม่ได้แตะข้อ 2.5 (อาวุธห้าคลาสลงกระเป๋า = LANE-DB) และข้อ 2.3 (เฟรมรายชื่อสกิล = LANE-CS) ตามที่ COO ตีขอบไว้
4. `relog_required=yes` พูดถึง **สิ่งที่เซิร์ฟเวอร์ส่ง** ไม่ได้พูดว่าไคลเอนต์วาดคลาสใหม่ถูก — อันหลังต้องดูจอ

## ผลลบที่บันทึกเต็ม (ข้อ 2.4 ของเจ้าของ)
**ไม่มีด่านเลเวลให้ปลด** · grep: `n_LEVEL_LEARN|level_learn` ทั่ว `src/` เจอสามโมดูล ทั้งหมดเป็น**ตัวอ่านตาราง** · grep ผู้เรียกจากนอกโมดูลตัวเองคืนไฟล์ของรอบนี้ไฟล์เดียว ⇒ ไม่มีเส้นทางเรียน/ร่าย/แจกสกิลใดอ่านเลเวลก่อนอนุญาต · **ไม่แต่งด่านขึ้นมาเพื่อจะได้ปลด** ตามที่เจ้าของสั่ง · หนี้ส่งให้ K แล้ว (`20260908_1634_LANE-GM-TO-LANE-K-...`)

## ของที่ขัดกัน และผมตัดสินไปแล้ว `[สมมติของสาย LANE-GM - รอ COO ยืนยัน]`
เจ้าของข้อ 3.1 ขอ "บัญชีทั่วไปพิมพ์แล้วต้องได้ข้อความปฏิเสธ + โทเคน `COMMAND_REFUSED`" แต่บน main วันนี้ **non-GM ไม่ถูก decode และไม่พิมพ์อะไรเลย** (คุณสมบัติที่วัดแล้วและพินไว้ + ประโยคที่ 1 ของพรอมป์สายผมเองว่าผู้เล่นทั่วไปต้องไม่เห็นอะไรต่าง)
⇒ ผมเลือก **ไม่แตะประตูเดิม** แล้วจ่ายโทเคนจากที่ที่มีจริง: `GM_CHAT_COMMAND_REFUSED` (โทเคนร่วมเดิม มีสตริง `COMMAND_REFUSED` อยู่ในตัว) พิมพ์เมื่อ **GM พิมพ์ผิด** (`/job banana`, `/skill`) จับจาก stderr จริงใน `TypoRefusalPrintsTheSharedTokenTests` · และพินคุณสมบัติเงียบของ non-GM เพิ่มเพื่อไม่ให้คำสั่งใหม่เป็นตัวที่ทำมันพัง
รายละเอียด + ทางย้อนสามข้อ ⇒ `notes_to_chief/20260908_1631_LANE-GM-ASK-COO-the-COMMAND_REFUSED-token-and-the-silent-non-gm.md`

## หมุดของสายอื่นที่ต้องขยับ และผมขยับให้ในคอมมิตเดียวกัน (ไม่ได้ผ่อนหมุดลง)
1. `test_gm_chat_command_parse_way_out.py` — ลำดับ `COMMAND_USAGE` ที่มนุษย์อ่าน (`job`/`skill` ต่อท้าย)
2. `test_gm_typo_refused_notice.py` — เซ็ตชื่อคำสั่งที่ต้องได้ notice
3. `test_gm_standalone_map_is_not_chat_writable.py` — ตาราง exercise (ทั้งสองคำสั่ง**เขียนแถว** จึงต้องถูกลากผ่านประตูนี้จริง ๆ)
4. `test_gm_chat_command_action.py` — สัญญาชื่อ event (10 ชื่อใหม่) + สัญญา label (4 label ใหม่) + จำนวน label ใน docstring ของ entry point (6 → 10 พร้อมคำอธิบายว่าทำไมสี่ตัวใหม่อยู่ฝั่ง "คำสั่งที่ **ได้** ทำงาน" ร่วมกับ `/lv`)
5. `test_skill_list_at_login.py` (สาย CS) — **แดงเพราะ docstring ของผมสะกดชื่อโมดูลเขา** ทำให้ text-scan นับผมเป็น caller (`callers_in_src=1` ทั้งที่ไม่มีใครเรียก) ⇒ ผมแก้ที่ **ฝั่งผม** ด้วยการเลี่ยงสะกดชื่อ (วิธีเดียวกับที่ `gm/level_command.py` ทำกับสองโมดูล) **ไม่ได้แตะเทสของเขา**

## เกตและชุดเทส
- `pf_gate_preflight.py --repo <server>` → **PREFLIGHT PASS**
- ซ้อมเกตสภาพ "ไม่มี `pf_bridge` ข้าง ๆ" (บังคับเพราะเพิ่มไฟล์ `tests/test_*.py` ใหม่): **`pytest_subset` exit 0** (14120 passed · 330 skipped · 0 failed) · **`skip_census` exit 0** ("every skip is declared, named and pinned · RESULT: PASS") — อ่าน exit code ทั้งสองบรรทัดตามกฎ
- ชุดเต็มบนต้นไม้ที่ `git merge origin/main` แล้ว: **15020 passed · 450 skipped · 0 failed · 42906 subtests** (12 นาที 14 วินาที) เป็นคอมมิตสุดท้ายจริง
  🔴 **รันชุดเต็มสองครั้งในรอบนี้ และนี่คือเหตุผลตามที่กฎบังคับให้เขียน**: ครั้งแรก (14813 passed) เขียวก่อน adversary คืนผล · adversary คืนผล **ก่อน**ผมปลดล็อก จึงต้องแก้ในรอบเดียวกัน · แก้โค้ดหลังชุดเต็มผ่าน = ต้องรันใหม่ก่อน push (กฎ `1428` ข้อ 4)
- ไม่มี skip/xfail/allowlist ใหม่ ไม่มีเทสไหนถูกลบหรือปิด (`2050`)

## adversary — ครั้งที่ 1 (คืนผลก่อนปลดล็อก จึงแก้ในรอบนี้)
สั่ง `pf-adversary` ครั้งที่ **1** ต้นรอบพร้อมเริ่มงาน · **ผลคืนเวลา ~16:49 ก่อนผมปลดล็อก** ⇒ ตามกฎต้องแก้ในรอบนี้ ไม่ใช่ยกไปรอบหน้า · **ผล: NOT CLEAN — 8 ข้อ (1 CRITICAL · 2 HIGH · 3 MEDIUM · 2 LOW)** · adversary ระบุเองว่าสามข้อที่มันเจอตอนร่าง (text-scan ของ `test_skill_list_at_login`, `WORDS[10]`, ลำดับ `COMMAND_USAGE`) ผมแก้ไปก่อนแล้วจึงไม่นับ

| # | ระดับ | เรื่อง | รอบนี้ทำอะไร |
|---|---|---|---|
| **D1** | CRITICAL | **ประตู allowlist ไม่ใช่ประตูต่อผู้เล่น** — `session.token` คือค่า `--token` ของ**ทั้งโปรเซส** (`v141:7371/7399`) ⇒ บูตที่ `/job` ของเจ้าของทำงานได้ คือบูตที่คนที่สองบน listener เดียวกันก็เขียนแถวได้ และ audit บันทึกชื่อ operator | **รูมีมาก่อน** (`/lv` `/speed` อยู่บนจุดเดียวกัน) แต่ **docstring ของผมอ้างว่าปิด ซึ่งเท็จ** ⇒ ขีดฆ่าประโยคนั้นทิ้งพร้อมผลวัด · ประโยคที่ใช้แทน = "A GM COMMAND IS AS PRIVATE AS THE LISTENER'S TOKEN" · ออก **CORE-REQUEST-GM-058** ถึง chief (`20260908_1655_...`) เพราะ `runtime.py`/`v141` นอกเขตผม |
| **D2** | HIGH | undo ที่เป็น `None` ทำให้คอนโซลบอกว่า "ผลถูกทิ้งไปพร้อม audit" ทั้งที่แถวอยู่บนดิสก์ (`/skill all` **ทุกครั้ง** · `/job` เมื่อ `class_id` เดิมเป็น NULL) | **แก้แล้ว**: `job_command.undo` คืน callable เสมอ (ตอบ `False` เมื่อไม่มีอะไรให้คืน) · เพิ่ม `skill_all_command.undo` ที่ตอบ `False` เสมอ พร้อมเหตุผลว่าทำไมลบแถวจริงไม่ได้ (ไม่มีประตูลบ และ `character_skills` เป็นตารางของ LANE-DB) — รูปแบบเดียวกับ `_speed_undo` |
| **D3** | HIGH | `granted=` นับ "call ที่ไม่ raise" ไม่ใช่ "แถวที่ถูก insert" ⇒ พิมพ์ `granted=137` ได้ทั้งที่ insert 0 แถว | **แก้แล้ว สองชั้น**: (ก) การอ่านสถานะก่อนเริ่ม **บังคับ** ถ้าอ่านไม่ได้ = ปฏิเสธ (`REFUSED_CANNOT_READ_CURRENT_SKILLS`) ไม่เขียนอะไรเลย (ข) `granted` มาจาก **ค่าที่ประตูคืนเอง** — `grant_learned_skill` คืนเซ็ต id ทั้งหมดที่อ่านในทรานแซกชันของมัน เซ็ตโตขึ้น = insert จริง เซ็ตนิ่ง = `INSERT OR IGNORE` เมิน · ประตูที่คืนค่าที่วัดไม่ได้ ⇒ บรรทัดพิมพ์ `granted_from=calls` |
| **D4** | MEDIUM | เส้นทางเดียวที่เขียนบางส่วนจริง (ตัวละครหายกลางทาง) เป็นเส้นทางเดียวที่**ไม่พิมพ์ตัวเลข** | **แก้แล้ว**: บรรทัดปฏิเสธที่มีแถวลงไปแล้วพิมพ์ `granted=/already=/failed=` ด้วย |
| **D5** | MEDIUM | docstring อ้างไฟล์เทสสองชื่อที่ไม่มีในรีโป (ชื่อจริงคือ `test_gm_job_and_skill_all_commands.py`) — หนึ่งในนั้นคือ "หลักประกัน" ของ literal ที่ hardcode ไว้ | **แก้แล้ว** ทั้งสี่จุด |
| **D6** | MEDIUM | `/skill all` = 137 ทรานแซกชันเรียงกันบน listener thread · วัดบน Linux 0.287 วิ · คาดบน Windows `synchronous=FULL` 0.7-2 วิ | **ไม่แก้รอบนี้** — ต้องมีประตูแบบ batch ในเขต LANE-DB · บันทึกเป็นหนี้ + ข้อควรรู้ของผู้เทส (พิมพ์แล้วรอสักครู่ ไม่ใช่คำสั่งค้าง) |
| **D7** | LOW | `write_class_id` อ้าง "Never raises" แต่ `column = class_column()` อยู่นอก `try` ทุกอัน | **แก้แล้ว**: ห่อไว้ + refusal `REFUSED_NO_COLUMN` |
| **D8** | LOW | overclaim สี่จุด: `login_would_send` ถูกนิยาม ถูกเทส แต่**ไม่มีใครเรียก** · "สามตัวบวกกันได้ 137 ทุกเส้นทาง" ไม่จริง · "147 of 148" ไม่ตรงตาราง (137) · `PARTIAL_SUFFIX` ตายซาก | **แก้แล้วทั้งสี่**: `/job` **เรียก** `login_would_send` จริงแล้วและปฏิเสธ+คืนค่าเดิมถ้าประตูของ login อ่านไม่เจอ · ขีดฆ่าคำอ้างเรื่องผลรวมพร้อมเหตุผล · เลิกพิมพ์ตัวเลขในร้อยแก้ว · ลบ `PARTIAL_SUFFIX` แทนด้วย `counts_are_complete` ที่มีคนใช้จริง |

ข้อที่ adversary **ลองแล้วพังไม่ได้** และผมบันทึกไว้เพราะเป็นหลักฐานฝั่งบวก: ด่าน canonical-DB (ทุกรูปแบบชื่อไฟล์ที่มันลอง) · การหนีของ exception ขึ้น listener thread · codec ของ notice (12 อักขระ ASCII ไม่มี `TELEPORT`) · ไม่มี id สกิล hardcode จริง ๆ · ถัง 1024 ถูกแจกและถูกเรียกชื่อจริง · และมันยืนยันว่าคำอ้าง "login อ่าน `class_id` จาก `read_typed_attributes` โดยไม่มี vitals gate" **เป็นจริง**

🔴 **`ADVERSARY_PENDING`**: ตัวแก้ทั้งแปดข้อยัง**ไม่ผ่าน** adversary (จะเป็นครั้งที่ 2 แต่เวลารอบหมด) ⇒ **รอบถัดไปของสาย GM สั่ง adversary บนกิ่งนี้เป็นงานแรก**

## รอบหน้าทำอะไร
1. **งานแรก = สั่ง `pf-adversary` บนกิ่ง `claude/hopeful-babbage-wv0fpe` เพื่อตรวจ*ตัวแก้*แปดข้อของรอบนี้** (`ADVERSARY_PENDING` ข้างบน) แล้วแก้สิ่งที่มันเจอ
2. คำตอบของ COO เรื่องโทเคน `COMMAND_REFUSED` (ใบ `1631`) — ถ้า COO สั่งให้ non-GM เห็นข้อความจริง ต้องออก CORE-REQUEST เพราะ `gm/chat_command.py` อยู่นอกเขตผม
3. `warp` `#1136` (เลื่อนลงมาตาม COO `1541`) · `SANCTIONED_BARRED_SCENES` 126 หลังใบ `20260908_1512_LANE-A-TO-LANE-GM-the-126-sanction-is-dead-weight-after-1218.md`

## งานสำรอง (ทำเมื่องานหลักติด) — สามข้อ เริ่มได้ทันที
1. **`/job` ตอบกลับด้วยชื่อคลาส ไม่ใช่แค่เลข** — ไฟล์ `gm/job_command.py` (`console_line`) + `class_catalog.CLASS_ID_TO_NAME` · ผ่านเมื่อ: คอนโซลพิมพ์ `class_id_to=16` **และ** ชื่อจากตาราง โดยไม่เพิ่ม literal ชื่อคลาสในโมดูล และเทสเดิม 43 เคสยังเขียว
2. **`/skill <class_id>` (แจกเฉพาะคลาสเดียว)** — ไฟล์ `gm/skill_all_command.py` + parse branch ใน `gm/commands.py` · ผ่านเมื่อ: แจกเฉพาะ `CLASS_ID_TO_CURRICULUM_SKILL_IDS[<id>]` วัดที่ DB ว่าจำนวนแถวตรงกับตาราง และ `/skill all` เดิมไม่เปลี่ยนพฤติกรรม
3. **หนี้ที่ adversary เคยชี้ในไฟล์รอบเก่าของสาย GM** — เริ่มที่ `grep -rn "ADVERSARY_PENDING\|ยังไม่แก้" rounds/GM_*.md | tail -20` · ผ่านเมื่อ: อย่างน้อยหนึ่งข้อถูกปิดพร้อมเทสที่ตายเองได้ถ้าปัญหากลับมา

## PR ของรอบนี้
- `pirate-force-server` กิ่ง `claude/hopeful-babbage-wv0fpe` — สองคอมมิต: `45ccc55` (คำสั่งสองตัว) และ `71bdc6d` (ตัวแก้ผล adversary แปดข้อ) · **สถานะตามจริง: เปิดแล้ว รอ gate** (ยังไม่อยู่บน main — รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`)
- `pf_bridge` `#1918` (claim ของรอบนี้ · ปลดล็อกด้วยการเติม marker เมื่อ PR เซิร์ฟเวอร์เปิดแล้ว)

SCOREBOARD: COMING | A GM can now type /job 1|2|4|16|32 to change class and /skill all to receive every class's skills on one character, so the next attended boot can test all five classes' moves without rolling five characters or levelling any of them -- the rows land now, the K window follows when LANE-CS wires the login skill list | pirate-force-server 45ccc55+71bdc6d (branch claude/hopeful-babbage-wv0fpe), pf_bridge#1918
