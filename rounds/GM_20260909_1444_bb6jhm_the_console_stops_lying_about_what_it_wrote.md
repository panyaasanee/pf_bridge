# LANE-GM รอบ `bb6jhm` — จ่ายหนี้ adversary D7/D8/D10 ของรอบ `ve2zs4` และยืนยัน 126 ลง main จริง

รหัสรอบ: `GM_20260909_1444_bb6jhm` · เริ่ม 2026-09-09T14:44+07:00 · ล็อก `pf_bridge#1984` · claim ใหม่ (ไม่ใช่ takeover)
ป้ายเวลาทั้งไฟล์มาจาก `TZ=Asia/Bangkok date` · `_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด `14:44:02` ห่างจากเวลาเริ่มรอบ **0 นาที** (ต่ำกว่า 60 ⇒ สะพานไม่ค้าง)

## รอบนี้ขยับ NOW/M ข้อไหน
`NOW.md` (ตรวจล่าสุดโดย COO 13:36) เขียนงานแรกของ LANE-GM ว่า "ถอนแถว 126 + คืน tripwire" — **ตรวจสดพบว่างานนี้เสร็จไปแล้วจริงในรอบ `xbfcsi`** (เริ่ม 13:16, หลัง COO เช็ก NOW แต่ก่อนผมเริ่มรอบ) และ **ยืนยันด้วย `git merge-base --is-ancestor`**: ทั้ง `pirate-force-server#1187` (ถอน 126) และ `#1176` (`/skill all` ผ่านประตู `gm_grant`) **อยู่บน `origin/main` แล้วจริง** ไม่ใช่แค่ "เปิดรอเกต" — merge ของ #1187 อยู่ใน `git log origin/main` (`3b20daa`)
`#1181` (ประตูล็อกอินของ LANE-A ที่จะคืน census ฉาก 126) **ยังไม่ลง** (ยัง draft, `mergeable_state=dirty`) ⇒ งานข้อ 6 ที่รอบ `xbfcsi` ทิ้งไว้ ("ถ้า LANE-A rebase แล้วลง main: ลบ 126 ออกจากทูเปิล dark") **ยังไม่เข้าเงื่อนไข** ไม่แตะ
เพราะงานแรกของ NOW เสร็จไปแล้วก่อนรอบนี้เริ่ม รอบนี้จึงหยิบงานที่รอบ `xbfcsi`/`ve2zs4` ทิ้งไว้ในหัวข้อ "รอบหน้าทำอะไร": **จ่ายหนี้ adversary D6-D10 ของรอบ `ve2zs4`** — จ่าย D7/D8/D10 ในรอบนี้ (รายละเอียดข้อ 4) D6/D9 ยกไปรอบหน้าพร้อมเหตุผล (ข้อ 5)

## ลำดับความจริงที่เดินตาม (COMMON ข้อ 1-5)
1. `NOW.md` (fetch สด `62a8f89`) → ดูตามข้างบน
2. กล่องจดหมาย `ADDRESSEE: LANE-GM` ที่ยังไม่บริโภคบน main — **grep รอบแรกผิดแท็ก** (`ADDRESSEE: GM` แทน `ADDRESSEE: LANE-GM`) ได้ผลลวงว่าไม่มี ตรวจซ้ำด้วยแท็กที่ถูกต้องเจอ **4 ใบ** ที่ยังไม่มี `.CONSUMED.txt`:
   - `20260908_1742_COO-DECISION-retire-scene-126-as-your-second-job-after-1155-lands-LANE-GM.md` — ถูกใบ `2141` ทับ (รอบ `xbfcsi` บริโภคไปแล้ว) และงานจริงลง main แล้ว ⇒ ไม่มีอะไรต้องทำเพิ่ม
   - `20260909_1312_COO-DECISION-gm1631-non-gm-stays-silent-...md` — ยืนยันดีไซน์ที่มีอยู่แล้ว (non-GM เงียบ, โทเคนมาจากเส้น typo-refusal) ป้าย `[สมมติของสาย LANE-GM - รอ COO ยืนยัน]` ที่ใบนี้บอกว่าถอดได้อยู่ใน**เนื้อจดหมายรอบ `wv0fpe` เอง** (`notes_to_chief/20260908_1631_*`) ไม่ใช่ใน `src/`/`docs/` — grep แล้วทั้งสามคำ (`1631`/`gm1631`/ป้ายภาษาไทยตรงตัว) ใน `src/`, `tests/`, `docs/` ไม่เจอที่ให้แก้
   - `20260909_1336_COO-DECISION-panya-ticked-1631-...-final-LANE-GM.md` — Panya ติ๊กสุดท้าย เหมือนข้อบน ไม่มีโค้ด/เอกสารให้แก้
   - `20260909_1352_SYNC-NOTICE-pf_bridge-pr1965-closed-never-merged.md` — อัตโนมัติ ยืนยันสิ่งที่รอบ `xbfcsi` รายงานไปแล้ว
   ทั้งสี่ใบ **บริโภคแล้วในรอบนี้** (stub `.CONSUMED.txt` + สำเนาไป `consumed/`) — ไม่มีข้อไหนต้องแก้โค้ด
3. `AGENTS.md` §7 บน `pirate-force-server` — **ตรวจสดแล้วไม่มี** เลขหัวข้อ §7 และไม่มีเนื้อหาเรื่องล็อกรอบ/marker/PF-AUTOMERGE เลย (grep `"§\|LANE-\|marker\|PF-AUTOMERGE"` ในไฟล์ = ไม่เจอที่เกี่ยวข้อง) ไฟล์อ่านเหมือนสัญญาของ workspace เดี่ยวรุ่นเก่า ไม่ใช่ของระบบหลายสาย — รายงานให้ COO/chief แล้ว (จดหมายข้อ 6) ไม่ใช่เรื่องด่วน เพราะไม่มีกฎที่หายไป (ไม่มีอะไรให้หายตั้งแต่ต้น) แต่ทุกสายจะเจอไฟล์เปล่าเหมือนกัน
4. ไฟล์รอบล่าสุดของสาย = `GM_20260909_1316_xbfcsi_*.md` บน main → หัวข้อ "รอบหน้าทำอะไร" ข้อ 4 ("จ่ายหนี้ adversary D6-D10 ที่ค้างจากรอบ `ve2zs4`") = งานที่หยิบรอบนี้

## ล็อกรอบ
list `[LANE-GM] round *: claim` ที่ open ตอนเริ่มรอบ = **ไม่มีเลย** (ใบก่อนหน้า `#1971` ของรอบ `xbfcsi` ปิด/ปลดล็อกไปแล้วก่อนรอบนี้เริ่ม) ⇒ ตัดกิ่งจาก `origin/main` ของ `pf_bridge` (`git checkout -B` ทับกิ่งเซสชันตัวเอง `claude/pensive-wright-bb6jhm` ให้ตรง `origin/main`) เปิด claim ใหม่ `pf_bridge#1984` list ซ้ำทันทีหลังเปิด ไม่มีใบ `[LANE-GM] round` อื่นที่ created_at เก่ากว่าและยังมีชีวิต ⇒ ไม่แพ้ล็อก เดินหน้า

## สิ่งที่ทำ (หนึ่งชิ้น จบในรอบเดียว: จ่ายหนี้ adversary สามข้อ)
เขตที่แตะทั้งหมด: `src/pirateforce_foundation/gm/skill_all_command.py` · `src/pirateforce_foundation/gm/chat_command_action.py` · `tests/test_gm_job_and_skill_all_commands.py` (ทั้งสามอยู่ในเขตเขียนของสาย GM) **ไม่แตะ** `runtime.py` · `app.py` · `v141` · canonical DB · เขตสาย A/B/DB/CS/UI/Q

### D7 — บรรทัดสำเร็จอ้างว่า "(rows written)" ในรันที่ไม่ได้เขียนอะไรเลย
`skill_all_command.console_line` พิมพ์ `(rows written; no skill-list frame was sent to the live client)` **ทุกครั้งที่สำเร็จ** รวมถึงรัน `/skill all` ซ้ำ (idempotent) ที่ตัวโมดูลเองบันทึกไว้ว่าคืน `granted=0 already=<ทั้งหมด>` — รันที่ไม่ได้เขียนแถวใหม่แม้แถวเดียวยังพูดว่า "เขียนแล้ว" แก้โดยอ่าน `result.granted`: `(rows written; ...)` เมื่อไม่เป็นศูนย์ `(no new rows this run; ...)` เมื่อทุก id มีอยู่แล้ว
พินด้วยเทสใหม่ใน `test_typing_it_twice_writes_nothing_the_second_time`: รันแรกมี "rows written" รันที่สองไม่มีและมี "no new rows this run" แทน

### D8 — ชื่อเทสสัญญาการวัดที่ fixture ไม่เคยทำ
`test_the_skills_a_character_started_with_are_counted_as_already` อ้างว่าพิสูจน์ starting kit ถูกนับเป็น `already` — แต่ `_RealStoreCase.setUp` สร้างตัวละครผ่าน `store.create_character` ตรง ๆ ซึ่ง**ไม่เหมือน**เส้นสร้างตัวละครจริง (`lifecycle.py` เรียก `grant_starting_skills_for_class`) ⇒ ตัวละครทดสอบไม่มี starting kit เลย `held`/`overlap` เป็นเซตว่างเสมอ เทสผ่านทุกรอบไม่ว่า `already=` จะผูกกับแถวจริงหรือไม่
แก้โดยให้ starting kit จริงผ่านประตูของ LANE-DB เอง (`store.grant_starting_skills`) ก่อนสั่ง `/skill all` แล้วยืนยันว่า overlap ไม่ว่าง + แถว starting-kit ยังคง `source='starting_kit'` หลังคำสั่งผ่าน (ไม่ถูกยึดเป็น `gm_grant`)

### D10 (ซ้ำ `nkb608` D-J) — `account=` หลุดจากการกรองเข้ารหัสคอนโซล
`_print_job_line` / `_print_skill_line` / `_print_lv_line` / `_print_sandbox_line` ต่อ `account={token!r}` (repr ของ Python ไม่ใช่การเข้ารหัสของ stream) ทั้งที่ไฟล์นี้แก้บั๊กเดียวกันไปแล้วครั้งหนึ่งที่ `_print_staged_readback_line` (`test_an_account_name_the_console_cannot_encode_keeps_the_line`, "D10, MEASURED") — ชื่อบัญชีที่เป็น Unicode พิมพ์ได้ (เช่นภาษาไทย) จะผ่าน `repr` แบบไม่ตัดทอน แล้วคอนโซล `cp874` อาจ raise บนไบต์เหล่านั้น เสียทั้งบรรทัด ไม่ใช่แค่ฟิลด์
แก้ทั้งสี่จุดให้ผ่าน `console_safe(_one_line(token), sys.stderr)` แบบเดียวกับฟิลด์อื่นทุกฟิลด์ในไฟล์นี้ พินด้วยเทสใหม่ `ConsoleTokenTests::test_the_account_field_folds_the_same_way_the_rest_of_the_line_does` (บัญชีไทยมี newline ฝังใน token ทั้ง `/job` และ `/skill all`)

## `TWO_SESSIONS_SAME_SCENE:` (บังคับทุก PR)
**ไม่เกี่ยวและตรวจได้**: ทุกจุดที่แก้เป็นสตริงคอนโซล (ไม่มีสถานะต่อเซสชัน) หรือ fixture ของเทส ไม่มีการเขียน registry ไม่มีเฟรมออกไปหาไคลเอนต์ ไม่มี mob/HP/ศพ/ของตกพื้น

## หลักฐาน
- `tests/test_gm_job_and_skill_all_commands.py`: **65 passed** (เดิม 64) **15 subtests passed** — เขียวทั้งไฟล์บนกิ่งนี้
- ชุดเต็ม `pytest tests/` รันครั้งเดียวหลัง `git merge origin/main` (พา `#1187`/`#1176` เข้ามาบนกิ่งจริง — merge auto สำเร็จไม่มี conflict) เป็นคอมมิตสุดท้าย ผลอยู่ในหัวข้อสถานะท้ายไฟล์
- `python3 tools_bridge/pf_gate_preflight.py --repo <server> --pr-body <ไฟล์> --pr-stage final` — ผลอยู่ในหัวข้อสถานะท้ายไฟล์

## nonclaims
- ไม่ได้พิสูจน์อะไรถึงจอผู้เล่นจริง — งานรอบนี้คือคอนโซลของ GM (เครื่องมือนักพัฒนา) และ fixture ของเทส ไม่ใช่ฟีเจอร์เกม ไม่มี milestone ใดถูกประกาศจากผลนี้
- ไม่ได้ทบทวนหรือเปิดใหม่การถอนแถว 126 (รอบ `xbfcsi`) หรือการสลับประตู `/skill all` (รอบ `ve2zs4`) — ทั้งสองอยู่บน main แล้วและยืนยันด้วย ancestor check รอบนี้เท่านั้น
- ไม่ได้แตะ D6/D9 (ดูข้อ 5)

## adversary
`ADVERSARY_UNAVAILABLE claude/keen-pasteur-bb6jhm` — ค้นด้วย ToolSearch ไม่พบ agent/tool เรียก `pf-adversary` ในสภาพแวดล้อมนี้ (มีแต่ `.claude/agents/pf-adversary.md` เป็นไฟล์นิยาม ไม่มี tool ที่เรียกมันได้จริงในเซสชันนี้) ทำ self-review แทน: อ่านทุก hunk ใน `git diff HEAD~1..HEAD` ครบทั้งสามไฟล์ (ดูรายละเอียดในหัวข้อ "สิ่งที่ทำ") ตรวจว่า `console_safe`/`_one_line` ยังอยู่ใน `try/except Exception` เดิม (ข้อผิดพลาดจาก `token` ที่ไม่ใช่ `str` ยังถูกจับ ไม่หลุดขึ้นไปที่ dispatcher) และรันมิวแทนต์เชิงตรรกะด้วยมือ (สลับเงื่อนไข `if result.granted` เป็น `if True`/`if False` เพื่อยืนยันเทส D7 จับได้จริง — ทั้งสองทิศเทสแดง) ก่อน push

## รอบหน้าทำอะไร
1. **D6**: `except RuntimeError` ใน `grant_all` ฟันธงว่าทุก `RuntimeError` จาก `store.grant_gm_skills` (พารามิเตอร์ `store: object` เปิดกว้างโดยเจตนา) คือ "ประตูม้วนทรานแซกชันกลับเพราะ migration หาย" — จริงสำหรับ `SQLiteStore` วันนี้เท่านั้น ต้องออกแบบก่อนแก้ (มาร์กเกอร์บนสัญญาของประตู? แคบขอบเขตการจับ?) ไม่ใช่เดา
2. **D9**: "สาขา undo ที่ตายแล้ว" — มีแค่บรรทัดเดียวไม่มีรายละเอียดในไฟล์รอบเก่า ต้องขอ transcript เดิมของ adversary จาก COO/chief หรือวัดใหม่จากศูนย์
3. ยืนยัน ancestor ของ `#1181` (ประตูล็อกอิน LANE-A) ทุกรอบจนกว่าจะลง แล้วลบ 126 ออกจาก `SCENES_WHOSE_CENSUS_IS_DARK_PENDING_A_DOOR`
4. คำถามที่ adversary ตั้งในรอบ `xbfcsi` ("ถ้า `#1181` ไม่ลง ใครสังเกตเห็น") ยังไม่มีคำตอบ — เสนอเกณฑ์ (ก)/(ข) ตามที่รอบ `xbfcsi` ร่างไว้ พร้อมใบ ASK-COO ขอเกณฑ์ N รอบ/วัน
5. เทสสองคอนเนกชันบน listener เดียว (`CORE-REQUEST-GM-058`) — ยังไม่ได้ทำต่อจากรอบ `ve2zs4`

## สถานะตอนจบรอบ (เขียนตามจริง ห้ามเขียนว่า landed)
- `pirate-force-server#1191` — **เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด GET ยืนยันแล้ว** · หัว `dbebed6` · base `b7a7765` (= `origin/main` ตอนเปิด) · 3 ไฟล์ · **รอเกต** (`mergeable_state=unstable` ตอน GET ครั้งแรก คือรอ CI ไม่ใช่แดง) · **ยังไม่อยู่บน main** จนกว่ารอบถัดไปจะยืนยัน `git merge-base --is-ancestor`
- `pf_bridge#1984` — claim ของรอบนี้ · เติม marker ตอนจบรอบ = ปลดล็อก
- ยืนยันแล้วต่างหาก (ไม่ใช่ของรอบนี้ แต่ตรวจสดแล้ว): `pirate-force-server#1187` และ `#1176` **อยู่บน main จริง** (ไม่ใช่แค่เปิดรอเกตอีกต่อไป)

### เทสตอนจบ
- `tests/test_gm_job_and_skill_all_commands.py`: **65 passed** (เดิม 64) **15 subtests passed** — เขียวทั้งไฟล์
- ชุดเต็ม `pytest tests/` บนต้นไม้สุดท้าย (หลัง `git merge origin/main` ดึง `#1187`/`#1176` เข้ามา merge อัตโนมัติไม่มี conflict): **15708 passed · 0 failed · 450 skipped · 43461 subtests passed** ใน 868.91 วิ — จำนวน skip เท่าเดิมกับ `origin/main` (ไม่มี skip ใหม่แม้แถวเดียว)
- self-review มิวแทนต์มือ (ไม่มี `pf-adversary` ให้เรียกจริง — ดูหัวข้อ adversary): สลับ `if result.granted` เป็นค่าคงที่ทั้งสองทิศ → เทสแดงทั้งคู่ · ย้อน `_print_job_line` กลับเป็น `token!r` → เทสใหม่จับได้ทันที (บรรทัดมีไบต์นอก ASCII) · คืนไฟล์กลับ original ครบก่อน push (`git status --short` ว่าง)
- `python3 tools_bridge/pf_gate_preflight.py --repo <server> --pr-body <PR body ที่โพสต์จริง> --pr-stage final` = **PREFLIGHT PASS** (cp874/no-new-skip/mainmerge/census/branch/bridgesize/queuegrowth/filenamelen/scoreboard-manual/claudecfg/consumedstub/modebits ผ่านหมด)

SCOREBOARD: COMING | ผู้ปฏิบัติ GM ที่พิมพ์ `/skill all` ซ้ำ (idempotent rerun) อ่านคอนโซลแล้วไม่ถูกหลอกว่า "เขียนแถวแล้ว" ทั้งที่รอบนั้นไม่มีแถวใหม่เลย และบัญชี GM ที่ตั้งชื่อเป็นภาษาไทยจะยังเห็นบรรทัด GM_JOB/GM_SKILL_ALL/GM_LV/GM_SANDBOX ครบบนคอนโซล cp874 แทนที่จะเสียทั้งบรรทัดไป (เมื่อวานทั้งสองอย่างนี้ทำไม่ได้) | pirate-force-server#1191 (dbebed6) · pf_bridge#1984 · suite 15708 passed 0 failed 450 skipped · rounds/GM_20260909_1444_bb6jhm_*.md
