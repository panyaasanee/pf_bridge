# CHIEF_CONTINUATION.md - ARCHIVE 2026-09-06 (chief LANE-E round u2o8d7 / R368)

Lane-charter blocks (LANE-DB, LANE-CS, LANE-UI, LANE-Q: who owns which write zone, when each
lane was created, what its first jobs were) moved verbatim out of CHIEF_CONTINUATION.md so that
file can come back under its 30,720 B ceiling, per the chief housekeeping rule (CHIEF.md section 17
item 9: keep section 0 plus an index of the last 20 rounds; history goes to archive/).
Nothing is edited or deleted - the live file keeps a pointer to this file, and every lane's own
write zone is stated authoritatively in prompts/<LANE>.md and CHIEF.md section 6 regardless.

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



## ดัชนีรอบที่ย้ายออกจากไฟล์สดในรอบเดียวกัน (R358-R360)
- R358 2026-09-05 20:12+07 ตั้งเลข RE-266 ให้ใบ UI ที่ค้าง 5 ชม. · GT-184/186 -> BLOCKED-ON-RE-266 · RE-265 ปิด BOUNDED-NEGATIVE · GT-233 -> READY-v2 · ลงทะเบียนเขต docs/UI_LANE.md · PR ถ้อยคำ 0x4543 -> rounds/R358_rz1fxh_re266_numbered_gt184_186_flipped_re265_closed_gt233_ready_v2_0x4543_wording.md
- R359(5ahimz) 2026-09-05T21:2x+07:00 pf_bridge only, no server PR: pf_gate_preflight.py bridge-file-size gate (GT/RE/AGENTS/CHIEF_CONTINUATION/NOW ceilings, PANYA-ORDER 20260905_2038 item 1) + self-test (28 cases) · archived 23 closed GT tickets (2.80 MB -> 2.29 MB) + 51 closed RE tickets (935 KB -> 456 KB) to archive/*_ARCHIVE_20260905_closed.md, one-line stubs left, nothing deleted -- gate still RED on GT/RE/AGENTS/CHIEF_CONTINUATION (full byte target not reached this round, said so rather than claiming green) · AGENTS.md section 7 PANYA-ORDER 2038 item 7's four lines added · LANE-Q (SCRIPT/QUEST) zone registered per 2059/2112 (Q's own spike round already running, chief did not duplicate it) · verified RE-265/GT-233 (R358's flip) are on main as claimed -> rounds/R359_5ahimz_bridgesize_gate_queue_archive_pass_lane_q_registration.md
- R360(supz66) 2026-09-05T22:52-23:5x+07:00 Scoreboard คืนชีพจริง (`PANYA-ORDER 2038` ข้อ ข ที่ตายตั้งแต่ 29 ส.ค.): `pf_scoreboard.py` เดิมเป็น render อย่างเดียวและ `SCOREBOARD_FACTS.tsv` ไม่มีในรีโป = crash ที่ `open(SRC)` ถ้ามีใครรัน ⇒ เขียนใหม่เป็น collector เก็บบรรทัด `SCOREBOARD:` จาก `rounds/*.md` 625 ใบ (คอลัมน์เครดิต derive จากชื่อไฟล์ ไม่ใช่เนื้อบรรทัด · แถว `manual` รอดข้าม regenerate · มีไฟล์รอบแต่ parse ได้ 0 บรรทัด = exit 1 ไม่ใช่ render หน้าเดิมต่อ · stdout ASCII ล้วน · self-test 19 เคส) **ผลจริงตัวแรก: 8 แถว DONE=0** · 🔴 ร่างแรกเกือบส่งจดหมายกล่าวหา 6 สายว่าไม่ส่งฟิลด์หลักฐาน — เปิดไบต์จริงแล้วไม่จริง ทุกใบเขียนเป็นย่อหน้าที่ตัดขึ้นบรรทัดใหม่ 2-4 บรรทัด หลักฐานอยู่บรรทัดถัดไปครบ ⇒ แก้ collector ให้ต่อย่อหน้า + ลงกฎ §7 ห้ามใครแก้ไฟล์รอบให้เป็นบรรทัดเดียวเพื่อเอาใจเครื่องมือ · `lupa==2.8` เข้าบรรทัด pip ของ `gate-windows.yml` (`COO 2247` · ตัดสินไม่สร้าง `requirements.txt` บรรทัด pip เป็นแหล่งจริงใบเดียว · yaml duplicate-key ผ่าน · `bash -n` ใช้ไม่ได้ทั้งไฟล์เป็น pwsh เขียนไว้ตรง ๆ) · กฎ embedded-interpreter RCE ลง §7 (`COO 2249`) · 🔴 เกต bridgesize ของ R359 จับ chief เองเป็นรายแรก: เติมกฎสองบรรทัด -> `AGENTS.md` 88820->90641 RED ⇒ ย้าย "วิธีเปิด PR" 46.9 KB ไป `HOWTO_OPEN_A_PR.md` คำต่อคำ = 44161 bytes / 21,926 อักขระ (ต่ำกว่าเพดาน 25,000 อักขระของเจ้าของครั้งแรก) ยัน 224/224 บรรทัดไม่หาย ไม่ตัดกฎข้อไหน · 🔴 ถาม COO: หน่วยเพดานขัดกันเอง หัว `AGENTS.md` สั่งนับอักขระและห้าม `wc -c` แต่ preflight ของ chief เองนับไบต์ 30720 (ไทย 3 ไบต์/อักขระ = เข้มกว่าคำสั่งเจ้าของ 3 เท่า) · หนี้ยกไปรอบหน้าตามลำดับ COO: (1) `docs/PROMOTION_BACKLOG.md` (2) `DEATH_SEED_WIRING` — เปิด PR เซิร์ฟเวอร์ได้ใบเดียวต่อรอบ ใช้ไปกับ lupa ตาม `2247` ที่สั่งให้แยกใบ · push แล้ว รอ merge -> rounds/R360_supz66_scoreboard_revived_lupa_gate_agents_split.md
