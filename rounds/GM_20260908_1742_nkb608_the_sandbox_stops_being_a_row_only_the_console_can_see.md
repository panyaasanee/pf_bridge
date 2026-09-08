# LANE-GM รอบ `nkb608` — สนามซ้อมเลิกเป็นแถวที่มีแต่คอนโซลเห็น + จ่ายหนี้ adversary หกข้อ

รหัสรอบ: `GM_20260908_1742_nkb608` · เริ่ม 2026-09-08T17:42+07:00 · claim `pf_bridge#1932`
สาย: LANE-GM (TOOLS) · กิ่ง: `claude/friendly-bell-nkb608` (bridge) · `claude/gracious-franklin-nkb608` (server)
**ต่อยอด `pirate-force-server#1155`** (คำสั่ง `/job` + `/skill all` ของรอบ `wv0fpe` · ยังไม่ merge · ยืนยันรอบนี้ `git merge-base --is-ancestor 45ccc55 origin/main` = **เท็จ**)

## รอบนี้ขยับ NOW/M ข้อไหน
- **`NOW.md` → LANE-GM `1455`** — ครบไปแล้วรอบก่อน · รอบนี้จ่าย**หนี้ adversary ของงานนั้น** (ข้อ 1 ของ "รอบหน้าทำอะไร") + เพิ่มคำสั่งที่ทำให้สนามซ้อม**ตรวจสอบได้จากหน้าจอ** หลังรีล็อก
- **`NOW.md` → `warp #1136`**: ยืนยันรอบนี้ว่า **merge แล้ว** (รอบ `iu5xks` รายงานไว้ 07:31Z) ⇒ บรรทัดนั้นใน NOW เป็นของที่ปิดแล้ว
- **`NOW.md` → `SANCTIONED_BARRED_SCENES` 126**: **วัดแล้วว่ายังไม่ถึงเวลา** — `#1137` ยัง open+draft+dirty · บน main `login_entry_is_pinned(126)` ยัง `False` ⇒ เก็บแถว เขียนเหตุผลลง docstring ผูกการถอนกับเหตุการณ์ (รายละเอียด: จดหมายถึง LANE-A `1805`)
- **บันได M: ไม่ขยับ และตั้งใจไม่ขยับ** — GM คือเครื่องมือไปถึงสภาพที่จะเทส ไม่ใช่ขั้นบันได (`prompts/LANE-GM.md` ประโยคที่ 3)
- ยืนยันต้นรอบ: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 ไบต์)
- **นาฬิกา**: heartbeat ล่าสุด `2026-09-08T16:08:01+07:00` · เวลาผมตอนเริ่ม `17:42` ⇒ ห่าง **94 นาที** เกิน 60 ⇒ ตรวจกับหลักฐานอิสระตามกฎ: `pf_bridge#1931` `created_at` = `2026-09-08T10:33:03Z` = `17:33+07` ซึ่งอยู่ก่อนเวลาผมไม่กี่นาที ⇒ **นาฬิกาผมถูก สะพานค้าง** · push ต่อตามกฎ ไม่หยุดรอบ

## ล็อกรอบ
list `[LANE-GM] round ...: claim` ที่เปิดอยู่ใน `pf_bridge` → **ไม่มี** (ที่เปิดอยู่: `#1931` DB · `#1925` E · ที่เหลือเป็น addendum ของสายอื่น) ⇒ เปิด `#1932` แล้ว list ซ้ำ ไม่มีใบ `[LANE-GM]` เก่ากว่า ⇒ ผมถือล็อก
`pirate-force-server#1155` (PR ของรอบก่อน) เปิดรออยู่ **ไม่ใช่ล็อก ไม่ถอย** ตาม COMMON ข้อ 1

## งานแรกตามที่รอบก่อนสั่ง: `pf-adversary` บนกิ่งนี้ ต่อ*ตัวแก้*แปดข้อของรอบ `wv0fpe`
สั่งต้นรอบพร้อมเริ่มงาน · **ผลคืนก่อนปลดล็อก** ⇒ ต้องจ่ายในรอบนี้ · **ผล: NOT CLEAN — 11 ข้อ (1 CRITICAL · 4 HIGH · 4 MEDIUM · 2 LOW)**
adversary ทำงานใน worktree แยกและยืนยันเองว่าไฟล์ในขอบเขตไม่ขยับระหว่างวัด (`job_command.py` sha1 `33948f90a704` · `skill_all_command.py` `584fce71bcc8` เท่ากันทั้ง `426c3ae` และ `a9e9bbb`)

### จ่ายแล้วในรอบนี้ หกข้อ — ทุกข้อมีเคสที่ตายเองได้ถ้าปัญหากลับมา (`TheFixesOfRoundNkb608Tests`)
| # | ระดับ | เรื่อง | ทำอะไร |
|---|---|---|---|
| **D-A** | CRITICAL | `grant_all` **raise `TypeError`** สองทางออกจากหก — ส่ง 5 อาร์กิวเมนต์เข้าเรกคอร์ด 6 ฟิลด์ (รอบก่อนแทรก `counts_are_complete` แล้วแก้แค่สี่จุดหลังลูป) ⇒ หลุดขึ้นเธรดฟัง ทิ้ง audit `issued` ที่ไม่มี `outcome` · **สองบรรทัดนั้นไม่เคยถูกรันเลย** เพราะไม่มีเคสไหนเรียกด้วย id ที่ไม่ใช่ `1` | แก้ทั้งสองทางออก + เคสที่กวาดทุกทางออก (`0`/`None`/`True`/store ไม่มีประตู) |
| **D-B** | HIGH | undo ที่ **หายไปบนสาขาปฏิเสธ** — `_make_action` อ่าน "ไม่มี undo" = "ผลถูกทิ้งพร้อม audit" ⇒ `/skill all` ที่ตัวละครหายกลางทางพิมพ์ `granted=20` แล้วบรรทัดถัดมาบอกว่าทิ้งหมด ทั้งที่ 20 แถวอยู่บนดิสก์และลบไม่ได้ | ติด undo แบบตอบ `False` เสมอ **เฉพาะ**ปฏิเสธที่ทิ้งของไว้จริง (`_job_refusal_undo` + `result.granted`) · ปฏิเสธที่ไม่ได้เขียนอะไร **คงไม่มี undo** เพราะสำหรับมัน "ทิ้งพร้อม audit" คือความจริง |
| **D-C** | HIGH | แถวที่ `class_id` เป็น NULL (สภาพปกติของตัวละครก่อน migration 006) **ไม่มีอะไรให้คืน** ⇒ `_repair` คืน `""` ⇒ คำปฏิเสธไม่มีคำว่า durable เลย ทั้งที่แถวถือคลาสใหม่อยู่ · อ่านพลาดชั่วคราวหนึ่งครั้ง = ล็อกอินถัดไปส่งคลาสนั้นจริงหลังคำปฏิเสธ | `NO_PREVIOUS_SUFFIX = "_row_kept_the_new_class"` + ประโยคในตาราง `_JOB_BLOCKERS` |
| **D-D** | HIGH | การคืนค่า**ไม่ถูกอ่านกลับ** ⇒ พิมพ์ "the previous class was put back" ให้ store ที่เขียนครั้งที่สองแล้วเงียบ | อ่านกลับผ่านประตูเดียวกับ `login_would_send` · มิวแทนต์ (`if False`) **ตายจริง** วัดแล้วในรอบนี้ |
| **D-G** | MEDIUM | docstring สามจุดอ้างไฟล์เทสสองชื่อที่ **ไม่เคยมี** — หนึ่งในนั้นคือ "หลักประกัน" ว่า literal `job <1|2|4|16|32>` ไม่ drift จาก `class_catalog.CLASS_IDS` (ตัวหลักประกันมีจริง ชื่ออ้างผิด) | แก้ทั้งสาม + เคสที่เดินทุก path ที่ถูกอ้างในสี่ไฟล์ของสายนี้ แล้วแดงถ้าอันไหนไม่ใช่ไฟล์ |
| **D-K** | LOW | `KeyError` จาก reader จริง = "ไม่มีตัวละครแถวนี้" ถูกกลืนเป็น "อ่าน store ไม่ได้" ⇒ ชี้ผู้ปฏิบัติงานไปผิดที่ | sentinel `_ROW_MISSING` → `REFUSED_ROW_MISSING` |

### ยังไม่จ่าย ห้าข้อ — มีเจ้าของและลำดับ ไม่ใช่ค้างลอย
| # | ระดับ | เรื่อง | ใคร/เมื่อไร |
|---|---|---|---|
| **D-E** | HIGH | `/skill all` เขียน `source='learned'` ทั้งที่ LANE-DB สร้าง `store.grant_gm_skills` (`source='gm_grant'` + migration `018`) ไว้ให้คำสั่งนี้โดยเฉพาะ และประตูนั้น **ไม่มีผู้เรียกเลย** · `character_skills` ไม่มีประตูลบ ⇒ 137 แถวถาวร | **งานแรกรอบหน้าของผม** · สลับประตูต้องยกตัวนับ `granted=` ไปด้วย ไม่งั้นตกสาขา D-I ทันที ⇒ ใบ `ASK-COO 1805` (ถามด้วยว่าแถวที่เขียนไปแล้วต้อง backfill ไหม = LANE-DB) |
| **D-F** | MEDIUM | โน้ตบนจอ (`SKILL NOTSET` / `JOB NOCHANGE`) ยังบอกว่า "ไม่มีอะไรถูกเขียน" บนสาขาเดียวกับที่ D-B วัดว่ามีแถวลงแล้ว — คอนโซลแก้แล้ว จอยังไม่แก้ | รอบหน้า พร้อม D-E (ต้องหาประโยคใหม่ใน 12 อักขระ) |
| **D-H** | MEDIUM | สองเซสชันบนตัวละครเดียว: `granted=` ของแต่ละใบไม่เท่าแถวที่ใบนั้นแทรก (137 บนดิสก์ · 143 เมื่อบวกสองใบ) และ `counts_are_complete` ยัง `True` ⇒ ธง degraded ยิงผิดเงื่อนไข | รอบหน้า พร้อม D-E |
| **D-I** | MEDIUM | baseline ของ `granted` คร่อมสองประตู (`list_character_skills` ครั้งแรก แล้ว `grant_learned_skill` ต่อ) · และสาขา `REFUSED_NOTHING_GRANTED` ยังพิมพ์ปฏิเสธ**ไม่มีตัวเลข** = D4 เดิมกลับมา ถ้าประตูคืนค่าแบบ one-call | **ผูกกับ D-E** — นี่คือสาขาที่การสลับประตูจะลงทันที |
| **D-J** | LOW | `console_line` บังคับ ASCII ของตัวเอง แต่ `_print_*_line` เติม `account={token!r}` ที่ไม่ผ่านตัวกรอง ⇒ บน stderr cp874 บรรทัด `GM_SKILL_ALL` ทั้งบรรทัดหายได้ (ตั้งชื่อบน `.events` แล้ว จึงเป็น LOW) | รอบหน้า |

### สิ่งที่ adversary **ลองแล้วพังไม่ได้** (หลักฐานฝั่งบวก บันทึกตามกฎ)
ด่านตัวตน (บัญชี `DECKHAND` ไปไม่ถึงการเขียนทั้งสองคำสั่ง) · ด่าน canonical-DB (fail-closed ทุกรูป) · การอ่านบังคับก่อนแจก (`before is None` ⇒ ไม่มี call ถึงประตูเขียน) · idempotence ครบวงจร (`137/0` แล้ว `0/137`) · ไม่มี skill id เป็น literal ใน `skill_all_command.py` · `write_class_id` ไม่มี raise หลุด (D7 ของรอบก่อน**จริง** — แค่ไม่ได้ทาลงโมดูลพี่น้อง)

## ของใหม่ของรอบนี้: `sandbox` — คำสั่งที่ตอบว่า "แถวถืออะไรอยู่" (`gm/sandbox_readback.py`)
**ปัญหาที่มันแก้ตรง ๆ**: สนามซ้อมคือสองคำสั่งที่เขียนแถวแล้วไม่ขยับพิกเซล · ทั้งคู่ตอบบนจอ**ตอนพิมพ์** แล้วผู้เทสรีล็อก — **หลังรีล็อกไม่มีทางถามว่าแถวรอดไหม** · คลาสไคลเอนต์วาดเอง แต่ 137 แถวสกิล **ยังไม่มีใครส่ง** (LANE-CS ถือ seam นั้น `#1159`) ⇒ "สนามซ้อมพร้อมหรือยัง" เป็นคำถามที่ตอบได้จากคอนโซลเซิร์ฟเวอร์เท่านั้น ซึ่งไม่ใช่ที่ที่คนพิมพ์กำลังมอง
- **ถามประตูที่ล็อกอินถามเอง ไม่ใช่สำเนาของมัน**: คลาสมาจาก `session._class_id_on_the_row` (ฟังก์ชันที่ `legacy_bridge.start_game` เรียกจริง) · สกิลมาจาก `store.list_character_skills` (ประตูเดียวกับที่ `/skill all` นับ) ⇒ "จอบอกอะไร" กับ "ล็อกอินหน้าจะส่งอะไร" ขัดกันไม่ได้เชิงโครงสร้าง
- **ห้าประโยค หา*ใน* 12 อักขระ ไม่ใช่เขียนอิสระ**: `JOB016 SK137` · `NO JOB SK137` · `JOB016 SK???` · `NO JOB SK???` · `COUNT TOOBIG`
- `NO JOB` **รวมสองสาเหตุโดยตั้งใจ** (คอลัมน์ NULL กับอ่านไม่ได้) เพราะ `_class_id_on_the_row` รวมมันเองตาม `COO-DECISION 20260904_0446` ข้อ 3 — ล็อกอินส่งค่าคงที่ทั้งสองกรณี · คอนโซลแยกให้ (`class_id=none` + `rows=unknown|<n>`)
- `SK<n>` **นับ id ในหลักสูตร ไม่ใช่จำนวนแถว** (ตัวละครถือสกิลที่สายนี้ไม่เคยแจกได้) · จำนวนแถวไปอยู่บนคอนโซลเป็น `rows=`
- **ไม่มีประตูใหม่** · และ**ตั้งใจไม่ใส่ด่าน canonical-DB**: ด่านนั้นยืนหน้าคำสั่งที่ **เขียน** · การปฏิเสธไม่บอกว่าแถวถืออะไรบนบูต canonical คือการกลืนประโยคเดียวที่บอกผู้ปฏิบัติงานว่าเขาอยู่บนบูตนั้น
- โทเคน: `GM_SANDBOX cid=<n> class_id=<a|none> skills=<k>/<total> rows=<m|unknown> notice='<body>'`

## หลักฐานสองชั้น (แยกกัน ห้ามใช้ชั้นหนึ่งอ้างอีกชั้น)
- **ชั้น DB** — `TheAnswerIsMeasuredOnDiskTests` เขียนผ่านประตูเดียวกับที่ `/job`/`/skill all` เขียน แล้วอ่านกลับด้วย **store ตัวที่สอง** ที่เปิดไฟล์เดียวกัน (ตัวที่ไม่เคยเห็นการเขียน) · ตัวละครใหม่ = `NO JOB SK000` · หลังเขียน = `JOB016 SK137` · บางส่วน = `JOB032 SK005`
- **ชั้น wire/จอ** — ทุกสาขาของ `notice_body` ถูก**ประกอบเป็นเฟรมจริง**ผ่าน `say_wire.make_local_talk_notice_frame` ซึ่งปฏิเสธ body ที่ไม่ใช่ 12 ASCII พอดี ⇒ ประโยคที่เอาขึ้นจอไม่ได้ แดงที่นี่ ไม่ใช่ที่บูต attended
- **ชั้นที่ยังไม่มี และรอบนี้ไม่อ้างว่ามี**: ยังไม่มีไคลเอนต์เห็นผลของ `sandbox` — ต้องบูต attended

## nonclaims
1. `JOB016 SK137` บอกว่า **แถวถืออะไร** ไม่ได้บอกว่าไคลเอนต์วาดคลาส 16 · ไม่ได้บอกว่าสกิลร่ายได้ · ไม่ได้บอกว่าหน้าต่างสกิลเปิด — ยังไม่มีใครส่งรายการสกิล
2. **ใช้ GM ข้ามขั้นไหน**: ข้ามการเรียนสกิลทั้งขั้น ไม่หักแต้ม ไม่ผ่านเลเวล · `sandbox` เป็นเครื่องมืออ่าน ไม่ใช่หลักฐานว่าระบบเรียนสกิล/เลือกอาชีพทำงาน
3. ตัวเลขส่วน `SK` เป็นของหลักสูตรใต้หมุด sha256 — ตารางโตเมื่อไร ตัวส่วนโตตาม
4. D-E ยังไม่จ่าย ⇒ แถวที่ `/skill all` เขียนยังมี provenance `'learned'` ซึ่งประตูของ LANE-DB เรียกว่าประโยคเท็จ · **อย่าอ้างผลของ `/skill all` เป็นหลักฐาน provenance**

## หมุดของสายอื่น/ของตัวเองที่ต้องขยับ และผมขยับให้ในคอมมิตเดียวกัน (ไม่ผ่อนหมุดลง)
1. `test_gm_chat_command_parse_way_out.py` — ลำดับ vocabulary + `NO_ARGUMENT_COMMANDS` (`sandbox` เป็นตัวที่สอง)
2. `test_gm_typo_refused_notice.py` — เซตชื่อคำสั่ง + กวาด "อาร์กิวเมนต์ผิดของกริยาไร้อาร์กิวเมนต์" ทั้งสองกริยา
3. `test_gm_standalone_map_is_not_chat_writable.py` — ตาราง exercise
4. `test_gm_chat_command_action.py` — สัญญาชื่อ event (3 ชื่อใหม่) + สัญญา label (1 ใหม่) + จำนวน notice label ใน docstring ของ entry point (**สิบ → สิบเอ็ด** พร้อม split)
ไม่มี skip/xfail/allowlist ใหม่ · ไม่มีเคสไหนถูกลบหรือปิด (`2050`)

## เกตและชุดเทส
- `pf_gate_preflight.py --repo <server>` → **PREFLIGHT PASS**
- ชุดเต็มบนต้นไม้ที่ `git merge origin/main` แล้ว: **15158 passed · 450 skipped · 0 failed · 43014 subtests** (11 นาที 53 วินาที · `EXIT=0`) เป็นคอมมิตสุดท้ายจริง
  🔴 **รันชุดเต็มสองครั้ง และนี่คือเหตุผลตามที่กฎบังคับให้เขียน**: ครั้งแรก **แดงหนึ่งเคส** — `test_gm_chat_no_bytes_line.py::test_every_blocker_is_one_ascii_line_within_the_cap` จับประโยค blocker ใหม่ของ D-C ที่ยาว **254 > 240** (`MAX_CONSOLE_HINT_LENGTH`) · หมุดทำงานถูกต้องตามที่มันถูกเขียนมา ⇒ ย่อประโยค + ให้เคสของ D-C วัดเพดานเองด้วย แล้วรันใหม่ทั้งชุด
- มิวแทนต์ที่รันจริงรอบนี้: ถอดการอ่านกลับใน `_repair` (`if False`) ⇒ `test_a_restore_that_did_not_take_is_not_reported_as_put_back` **แดง** · คืนค่า `""` แทน `NO_PREVIOUS_SUFFIX` ⇒ `test_a_row_that_had_no_class_...` **แดง** · ทั้งสองเขียวกลับหลังคืนโค้ด

## รอบหน้าทำอะไร
1. **งานแรก = D-E + D-I + D-H เป็นก้อนเดียว**: สลับ `/skill all` ไปประตู `store.grant_gm_skills` (`source='gm_grant'`) **พร้อมยกตัวนับ `granted=` ไปอยู่บนค่าที่ประตูใหม่คืน** และปิดสาขา `REFUSED_NOTHING_GRANTED` ที่พิมพ์ปฏิเสธไร้ตัวเลข · ผ่านเมื่อ: `SELECT source` บน `SQLiteStore` จริงคืน `gm_grant` ทั้ง 137 แถว **และ** `granted=` เท่าจำนวนแถวที่แทรกจริงเมื่อรันสองเซสชันพร้อมกัน
2. **D-F** — โน้ตบนจอที่ยังบอกว่าไม่มีอะไรถูกเขียน (ต้องหาประโยคใน 12 อักขระ) · **D-J** — `account={token!r}` ผ่านตัวกรอง ASCII เดียวกับ `console_line`
3. คำตอบ COO ใบ `1631` (โทเคน `COMMAND_REFUSED`) และใบ `1805` (provenance) — ใครมาก่อนใช้ก่อน
4. **ผูกกับเหตุการณ์ ไม่ผูกกับความจำ**: รอบแรกที่ `git merge-base --is-ancestor <sha #1137> origin/main` เป็นจริง ⇒ ถอนแถว `126` พร้อมซ่อม 25 เคส/5 ไฟล์ + `docs/GM_LANE.md` ในคอมมิตเดียว

## งานสำรอง (ทำเมื่องานหลักติด) — สามข้อ เริ่มได้ทันที
1. **`/job` ตอบด้วยชื่อคลาสบนคอนโซล** (`class_catalog.CLASS_ID_TO_NAME`) · ผ่านเมื่อ: คอนโซลพิมพ์ทั้งเลขและชื่อจากตาราง โดยไม่เพิ่ม literal ชื่อคลาสในโมดูล
2. **`/skill <class_id>`** — แจกเฉพาะ `CLASS_ID_TO_CURRICULUM_SKILL_IDS[<id>]` · ผ่านเมื่อ: จำนวนแถวที่ DB ตรงกับตาราง และ `/skill all` เดิมไม่เปลี่ยนพฤติกรรม
3. **`sandbox` ตอบเลเวลด้วย** บนคอนโซล (จอเต็ม 12 อักขระแล้ว) ผ่านประตู `read_character_vitals_or_none` ที่ `/lv` ถาม · ผ่านเมื่อ: เลเวลบนบรรทัดมาจากประตูของล็อกอิน ไม่ใช่ประตูอื่น

## PR ของรอบนี้
- `pirate-force-server` กิ่ง `claude/gracious-franklin-nkb608` — สามคอมมิต: `426c3ae` (merge main · ต่อยอด `#1155`) · `a9e9bbb` (`sandbox`) · `e48422e` (จ่าย adversary หกข้อ) · **สถานะตามจริง: เปิดแล้ว รอ gate** (ยังไม่อยู่บน main — รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`)
- `pf_bridge#1932` (claim ของรอบนี้ · ปลดล็อกด้วยการเติม marker เมื่อ PR เซิร์ฟเวอร์เปิดแล้ว)
- **หลังเปิด `#1162` main ขยับ (LANE-UI ลงชุดใหญ่) ⇒ `mergeable_state: dirty`** · merge `origin/main` เข้ากิ่ง (ไม่มี conflict) แล้ว**รันชุดเต็มอีกครั้งบนต้นไม้นั้น: 15294 passed · 450 skipped · 0 failed · 43067 subtests (11 นาที 57 วินาที · `EXIT=0`) + PREFLIGHT PASS** แล้ว push (`b9f3b52`) — PR ที่ชนกับ base คือของที่ต้องแก้ทันที ไม่ใช่ของที่รอ
- คอมมิตของรอบ: `426c3ae` merge · `a9e9bbb` `sandbox` · `e48422e` adversary หกข้อ · `3acffea` เพดานคอนโซล · `2ed9c96` ชื่อไฟล์จดหมายในคอมเมนต์

SCOREBOARD: COMING | A GM who has relogged can now type /sandbox and read on the game screen whether the sandbox row survived -- which class the row holds and how many of the 137 curriculum skills are on it -- instead of asking the server console, which is not where the person testing is looking; and the /job and /skill all pair stopped crashing the listener thread on two of its own exits and stopped telling the operator that rows on disk had been thrown away | pirate-force-server branch claude/gracious-franklin-nkb608 (a9e9bbb+e48422e+3acffea+2ed9c96, builds on open #1155), pf_bridge#1932, full suite 15158 passed / 0 failed, PREFLIGHT PASS
