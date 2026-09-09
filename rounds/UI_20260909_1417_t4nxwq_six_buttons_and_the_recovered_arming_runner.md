# UI รอบ `t4nxwq` — ปุ่มที่หก และ `#1167` ที่กู้กลับมาแล้ว

เริ่ม 2026-09-09T13:52+07:00 · claim `pf_bridge#1978` · ไม่ใช่ takeover
ล็อกว่างจริง: ตามที่ orchestrator ระบุมาว่าล็อกถูก claim ไว้แล้วก่อนรอบนี้เริ่ม (ไฟล์ `_claim.md` มีอยู่แล้วบนกิ่งตอนเริ่ม)
กิ่งทั้งสองรีโปตาม instruction: `pirate-force-server` = `claude/inspiring-feynman-sevsi3` (base `origin/main` `1ecf43e4438f`)
· `pf_bridge` = `claude/peaceful-pascal-sevsi3` (base `origin/main` `da564dc3`)

สะพาน: `_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุดตอนเริ่มตรวจ `2026-09-09T13:40:02+07:00` ห่างจากนาฬิกาตอนตรวจ (14:13) **33 นาที** — ไม่เข้าเงื่อนไข "ค้าง" (>60 นาที) แต่บันทึกไว้ตามกฎ

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว — โค้ดรอบนี้ (ผู้ตอบปุ่ม UI ส่งจดหมาย + สคริปต์ arming proof + เทส) ไม่แตะ world state ใด ๆ (ไม่มี scene roster / ตำแหน่งมอน / เลือดมอน / ศพ / ของพื้น) เป็นเพียง decode/re-encode payload ของผู้เล่นคนเดียวแล้วสะท้อนกลับ session เดียวกัน ไม่มีการอ่าน/เขียนสถานะร่วมของฉาก

## รอบนี้ขยับ NOW/M ข้อไหน

- **NOW บรรทัด LANE-UI**: `HEADLESS_PROOF` `GT-308` วัดใหม่บน main ปัจจุบัน (`1ecf43e4438f`) **จ่าย** (โทเคนเดิมตายเพราะ main ขยับ)
- **D11 จ่าย**: ปักเลข `187657` (ผลรวมกับเลขที่ปักไว้แล้ว `63488` = `251145` ที่ docstring อ้างมาตลอด) — ยืนยันซ้ำได้บนทั้ง Python 3.11.15 (โคลนนี้) และ 3.14.0rc2 (ล่ามของเกต ผ่าน `uv run --python 3.14`)
- **`#1167` กู้กลับมาแล้ว**: อ่าน gate log ไม่ได้ (ไม่มีสิทธิ์ Actions ผ่าน Bash) จึงซ้อมสอบท้องถิ่นแทนตามที่ orchestrator อนุญาตไว้ — merge `origin/main` เข้ากิ่ง `275a6ce3` (auto-merge สะอาด ไม่มี conflict) แล้วรันชุดเต็ม พบ **หนึ่งข้อแดงเดียว**: `EveryAnsweredButtonHasARunnerTests::test_every_reviewed_answerable_id_declares_an_arming_sample` ระบุว่า `lane_ui_friend_remove_answer.py` (ลง main **ก่อน** guard ตัวนี้จะมีอยู่บนกิ่ง `#1167`) ไม่มี `ARMING_TOKEN`/`arming_sample()` — เติมสองชื่อนี้ให้ ชุดเต็มเขียว (`15489 passed, 647 skipped, 40724 subtests` 12m25s) แล้ว push ไปยังกิ่งเดิม `claude/festive-shannon-ly40b5` (ไม่สร้างกิ่งใหม่ ตาม instruction) → sha ใหม่ `93930f68`
- **ปุ่มที่หก**: `Community_SendMailVital 0x6E12` ตอบแล้ว — layout รู้อยู่แล้วจาก `ui_mail_wire.py` (round `rqwwp8`) ไม่ต้องรอ RE
- **ปุ่มที่ห้า (`0xB9E9`) ได้ arming-proof สคริปต์เดี่ยวเป็นครั้งแรก**: `tools/pf_ui_friend_request_answer_headless.py` — ปิดช่องที่ทำให้ `GT-318` ค้างอยู่ (ปุ่มนี้ไม่มีสคริปต์วัดเองจนกว่า `#1167` จะลง main)
- **M ที่ขยับ: ไม่มี** (M2 เป็นของ LANE-A) — แต่ไม่ใช่รอบเปล่าตาม `1846`: `git diff --stat origin/main..HEAD -- src/` มี `ui_dispatch.py` + `lane_ui_mail_send_answer.py` ที่ทำให้ปุ่ม "ส่งจดหมาย" ในไคลเอนต์ตอบกลับจริงบนบูตปกติไร้แฟล็ก

## 1. งานหลัก (โค้ด): ปุ่มที่หกบน main — "ส่งจดหมาย" `Community_SendMailVital 0x6E12` ตอบแล้ว

ก่อนรอบนี้ main มีผู้ตอบห้าตัว (party invite `0x37B1` · trade invite `0x3700` · party cmd `0x2466` · friend request `0xB9E9` · friend remove `0x98A1`)
อีกสอง id ที่ `runtime.py` ส่งเข้าซีมได้แล้ว (`0x6E12` send mail, `0xAF60` get-mail-content, `0x8183` delete-mail — สามตัว ก่อนรอบนี้) **ไม่มีเจ้าของ**
รอบนี้เพิ่ม `lane_hooks/lane_ui_mail_send_answer.py` (`production_allowed = True`) + สองแถวที่เขียนใน `ui_dispatch.py` (`_ANSWERER_OWNERS`, `_OUTBOUND_FRAME_SHAPES`)

- **ทำไมตอบด้วย id เดิมเป็นคำตอบ ไม่ใช่การเดา**: `RE-312` RESULT-1 `0x6E12 INBOUND_YES handler=0x00645BF0 next=0x0063F9B0` + RESULT-2 ปักตัวเรียกที่ `0x005F38B2` ในลูป batch dispatch — เหมือนกับห้าปุ่มที่ตอบไปแล้ว
- **ส่งอะไร**: ไบต์ของผู้เล่นเอง — decode แล้ว re-encode แล้วปฏิเสธถ้าไม่ตรงไบต์ต่อไบต์ · ไม่ตั้งชื่อฟิลด์ใดเลย (`CALL_UNCLASSIFIED` ตาม `ui_mail_wire.py` เดิม)
- **ความกว้าง**: คลาสนี้มีหกฟิลด์ wstring (มากกว่าคลาสเดียวที่ปุ่มก่อนหน้าใช้) จึงตั้งเพดานที่ **4096/8192** (กว้างกว่า 512/1024 ของคลาสฟิลด์เดียวตามสัดส่วน ~512 ต่อฟิลด์) — เขียนเหตุผลไว้ในคอมเมนต์แถวเอง วัดจริง: หกฟิลด์ยาว 100 ตัวอักษร = 1,250 ไบต์, กรณีว่างเกือบหมด = 52 ไบต์
- **ไบต์ที่ไม่ใช่ของผู้เล่น**: `version` ยังเป็นค่าคงที่ของโมดูล (UNPROVEN DEFAULT) เหมือนทุกปุ่มก่อนหน้า
- **D2 residual**: โมดูลนี้ยังเรียก `register_answerer()` ตรง ๆ (ยังไม่แปลงเป็น `adopt_answerer()`) — **อยู่ในระยะ residual D2 จน `_discover()` ลง main** (COO-DECISION `20260909_1312_COO-DECISION-ui2132-*`, บริโภคแล้วรอบนี้)
- **หลักฐานสองชั้นแยกกัน**: (ก) กดผ่าน `state.dispatch()` จริงหลังล็อกอินจริง (ข) เฟรมที่คาดหวังสร้างใหม่โดยไม่ผ่าน dispatcher ด้วย `legacy.make_runtime_vitals` แล้วเทียบ
- **arming proof**: `tools/pf_ui_send_mail_answer_headless.py` (สคริปต์ใหม่ วัด `ceiling_is_enforced` แทน `width_is_enforced`/`own_width_is_read` เพราะคลาสนี้เป็นเพดาน ไม่ใช่ความกว้างตายตัว) `RESULT=PASS` บนกิ่งนี้
- **coverage**: `docs/FUNCTIONAL_COVERAGE.json` โดเมน `ui_buttons` ได้แถวที่เจ็ด (`send_mail_answer`) ในคอมมิตเดียวกับปุ่ม กันช่องว่างเปิดใหม่ที่ D13 ของรอบก่อนเตือนไว้ · `python3 tools/verify_functional_coverage.py` = PASS domains=9

## 2. `#1167` กู้กลับมา — ปลด `_discover()`/`adopt_answerer` และ D11 ไปพร้อมกัน

- PR `#1167` ปิดแล้วแต่ไม่ merge, กิ่ง `claude/festive-shannon-ly40b5` ยังอยู่ที่ `275a6ce3` (base main เก่า `48eaf82a`)
- ไม่อ่าน CI log ผ่าน Actions ได้ (ไม่มีสิทธิ์) → ซ้อมสอบท้องถิ่นแทนตามที่ orchestrator สั่งไว้อย่างชัดเจน
- `git merge origin/main` เข้ากิ่งนั้น: auto-merge สะอาด ไม่มี conflict marker (`git status --short` ว่างหลัง merge)
- รันชุดเต็มก่อนแก้: พบ **หนึ่งข้อแดง**: `lane_ui_friend_remove_answer.py` (ลง main ก่อน guard ของกิ่งนี้จะมีอยู่) ไม่มี `ARMING_TOKEN`/`arming_sample()` ที่ `EveryAnsweredButtonHasARunnerTests` (guard ของกิ่งนี้เอง) ต้องการ
- แก้: เติมสองชื่อ ในรูปแบบเดียวกับผู้ตอบพี่น้องอีกสามตัวบนกิ่งเดียวกัน (party invite/trade invite/party cmd/friend request ล้วนมีอยู่แล้ว) — ไม่แตะ `lane_hooks/__init__.py`, ไม่แตะตัวรัน, ไม่แตะ guard
- ชุดเต็มหลังแก้: **`15489 passed, 647 skipped, 40724 subtests passed` 12m25s (0 failed)**
- push commit ใหม่ `93930f68` เข้ากิ่งเดิม (ไม่สร้างกิ่งใหม่) — orchestrator ต้องเปิด PR ใหม่จากกิ่งนี้เอง (PR เดิมถูกปิดไปแล้ว reopen ไม่ได้ผ่าน git push อย่างเดียว)

## 3. `GT-308` — โทเคนวัดใหม่บน main ปัจจุบัน

- โทเคนเดิมของรอบ `ncejt8` (`head=104004da58f7 code=45948fb90412`) ตายแล้วเพราะ main ขยับ (กลไก UI-B เองไม่เปลี่ยน)
- วัดใหม่บน `origin/main` `1ecf43e4438f7ee2c7abf429b8d3a148b77d5de6`:
  `HEADLESS_PROOF: UI_LOGOUT_EXIT_GAME_ARMED subcode=1 ack=1 lease_closed=1 close_scheduled_ms=250 closer_called=1 relogin_after=ok head=1ecf43e4438f code=344b27154c11 RESULT=PASS`
  + negative control ในการรันเดียวกันยังผ่าน
- ขั้นที่สอง (กด X, COO `1943`) เติมไว้แล้วในเนื้อใบตั้งแต่รอบก่อน ไม่ต้องส่งซ้ำ
- ส่งจดหมาย `20260909_1413_LANE-UI-TO-K-gt308-remeasured-on-main-1ecf43e4-plus-six-button-body.md` (สองเรื่องในใบเดียว: โทเคน `GT-308` ใหม่ + ข้อเสนอเนื้อใบรวมหกปุ่มให้ `GT-318`)

## 4. `GT-318` และเนื้อใบหกปุ่ม (item 5 ของงานที่ได้รับมอบหมาย)

- `tickets/GT-318.md` (party invite เดี่ยว) ถูกค้างอยู่เพราะไม่มีใครวัด token ซ้ำบน main ในรอบที่ผ่านมา — วัดใหม่แล้วในจดหมายฉบับเดียวกับข้อ 3 (สี่ปุ่มบน main จริง, `code=` วัดจาก **worktree สะอาด** ของ `origin/main` แยกจากกิ่งรอบนี้ เพื่อไม่ให้ `code=` ปนกับไฟล์ใหม่ของรอบนี้)
- เสนอเนื้อใบ `ATTENDED:` รวมหกปุ่มในบูตเดียว (login ครั้งเดียว หกการกด teardown ครั้งเดียว) แทนหกใบแยก — K เป็นผู้ตัดสินเรื่องเลขใบ/จะพับหรือไม่ (ตาม `1910`)
- คำถามปิดท้ายของ pf-adversary รอบ `ncejt8` (echo ที่ไม่ตรวจสอบไปหา `0x0063F9B0` ที่ไม่มีใครอ่าน) ยกเข้าเป็นบรรทัดบังคับในเนื้อใบที่เสนอ ไม่ใช่เชิงอรรถ ตามที่รอบก่อนสัญญาไว้

## 5. หลักฐาน เกต และสิ่งที่ยังไม่จ่าย

- `pytest tests/` ชุดเต็มบนต้นไม้ `pirate-force-server` หลัง `git merge origin/main` (no-op, ตรงกันอยู่แล้ว) เป็นคอมมิตสุดท้ายจริง: **`15700 passed, 446 skipped, 43473 subtests passed` 844.12s (14m04s), 0 failed**
  🔴 **รอบก่อนแก้ `GRADE_SUBSET_SHA256`**: ชุดแรก (ก่อนแก้ pin) คือ `2 failed, 15698 passed` — `docs/FUNCTIONAL_COVERAGE.json` ที่แก้เพิ่มแถวที่เจ็ดทำให้ digest ที่ปักไว้ใน `tests/test_foundation_legacy_seam.py` ไม่ตรง (กฎบ้าน: ไฟล์ ledger ต้อง regenerate/recompute ก่อน commit) — คำนวณ digest ใหม่ตรง ๆ ด้วย `grade_digest()` เดียวกับที่เทสใช้ แล้วปักพร้อมย่อหน้าอธิบายการเคลื่อนไหว (ตามรูปแบบทุก pin ก่อนหน้าในไฟล์เดียวกัน) เขียนไว้เพราะเป็นหลักฐานว่ากฎ "รันชุดเต็มก่อน push" ไม่ใช่พิธีกรรม
- `python3 tools_bridge/pf_gate_preflight.py --repo /tmp/pirate-force-server` = **PREFLIGHT PASS** (cp874/skips/mainmerge/census/branch/bridgesize/queuegrowth/filenamelen/scoreboard-manual/consumedstub/modebits ทั้งหมดเขียว)
- `python3 tools/verify_functional_coverage.py` = PASS domains=9 · `python3 tools/verify_hypothesis_ledger.py` = PASS entries=50
- **ADVERSARY_UNAVAILABLE `claude/inspiring-feynman-sevsi3` (ระดับ builder เท่านั้น)** — เซสชันที่เขียนโค้ดไม่มี Agent/Task tool ให้เรียก `pf-adversary` จริง ทำ self-review แทนตอนบันทึกข้อนี้ครั้งแรก แต่ **เซสชัน orchestrator มี Agent tool และเรียก `pf-adversary` จริงหลังเปิด PR ทั้งสองใบ** — ผลกลับมาแล้วทั้งคู่: `#1189` (ปุ่มที่หก + D11 + arming-proof scripts) ไม่พบข้อบกพร่อง (มี FYI หนึ่งข้อไม่บล็อก) · `#1190` (กู้ `#1167`) พบหนึ่งข้อ RECORDED-NOT-PAID ก่อนหน้ารอบนี้ (runner สคริปต์ไม่เช็ค `sample_id == vital_id` เอง พึ่งเทสหน่วยแทน — ไม่ใช่ของใหม่ที่รอบนี้สร้าง) และหนึ่งข้อ PAID ในรอบนี้เอง (แก้ `docs/UI_LANE.md` แถวที่ล้าสมัยเรื่อง `#1167`) — ทั้งสองใบปลด draft แล้ว ใส่ `PF-AUTOMERGE: v4` แล้ว
- D2 (ownership ของ `_ANSWERERS`) ยังไม่จ่ายในเชิงกลไก — คงเดิมตามคำตอบ COO `ui2132`: ไม่ใช่งานของเลนนี้
- คำถามปิดท้ายของ pf-adversary (echo ไปหา `0x0063F9B0` ที่ไม่มีใครอ่าน) ยังไม่ได้จ่าย — ตอนนี้ครอบหกปุ่มแล้ว ไม่ใช่ห้า `#1189` ระบุตรง ๆ ว่าถึงเวลาต้องเป็นใบของตัวเองแทนย่อหน้าเดิมซ้ำทุกรอบ

## จดหมายและใบที่บริโภครอบนี้

- ส่ง 1 ใบ: `20260909_1413_LANE-UI-TO-K-gt308-remeasured-on-main-1ecf43e4-plus-six-button-body.md`
- บริโภค 1 ใบ (สตับ `.CONSUMED.txt` + สำเนาไป `consumed/`): COO-DECISION `20260909_1312_COO-DECISION-ui2132-*`
- ใบ ALL-LANES สองใบ (`0442`, `1142`) อ่านแล้วตั้งแต่รอบก่อน ไม่วางสตับใหม่ (ตามเหตุผลเดิม)

## รอบหน้าทำอะไร

0. **จ่ายแล้วระหว่างรอบ**: pf-adversary เรียกจริงโดย orchestrator บน `#1189`/`#1190` ทั้งคู่ ผลกลับมาแล้ว ไม่บล็อก ทั้งสองใบปลด draft + มี marker แล้ว
1. **ยืนยัน `#1167` (`93930f68` บนกิ่ง `#1190`) ลง main แล้ว** (`git merge-base --is-ancestor 93930f68 origin/main`) → ปลด `_discover()`/`adopt_answerer` (งานของ chief แต่ต้องยืนยันก่อนอ้างว่าใช้ได้)
2. **วัด arming token ของปุ่มที่หก (`0x6E12`) บน main จริง** ทันทีที่ `#1189` merge (`git merge-base --is-ancestor` ก่อน ห้ามเชื่อจดหมาย) → ส่ง `*-TO-K-*` อัปเดตด้วยหกบรรทัดจริงบน main
3. **เขียนใบถึง COO/chief เรื่องคำถามปิดท้าย `0x0063F9B0`** (หกปุ่มแล้ว ไม่ใช่ห้า, `#1189` ยกเป็นข้อเสนอ ไม่ใช่การตัดสิน) — ควรกลายเป็น RE ticket ของตัวเองหรือยัง
4. **ปุ่มถัดไปถ้า COO ไม่สั่งหยุด**: `0xAF60` (`Community_GetMailContentVital`) หรือ `0x8183` (`Community_DeleteMailVital`) — layout รู้แล้วทั้งคู่จาก `ui_mail_wire.py` เดียวกัน ไม่ต้องรอ RE
5. **ติดตามคำตอบ K เรื่องเนื้อใบรวมหกปุ่มของ `GT-318`** — ถ้า K ตัดสินพับเป็นใบเดียว ต้องเขียนใบ GT ให้ครบก่อนส่ง
6. **`docs/UI_LANE.md`**: เพิ่มแถวปุ่มที่หก (`0x6E12`) ให้ครบ — รอบนี้แก้แค่แถวเก่าที่ล้าสมัย (ที่ pf-adversary ชี้) ยังไม่ได้เพิ่มแถวใหม่
7. **RECORDED-NOT-PAID จาก `#1190`**: `ui_party_invite_answer_headless.py` runner ไม่เช็ค `sample_id == vital_id` เอง (พึ่งเทสหน่วยแทน) — อยู่ในเขตเขียนของเลนนี้ (`ui_*.py`) แก้ได้เมื่อมีเวลา

## สถานะ PR เซิร์ฟเวอร์

- `pirate-force-server#1189` (`claude/inspiring-feynman-sevsi3`) — หลัง pf-adversary (orchestrator เรียกจริง) คืนผลไม่บล็อก ปลด draft ใส่ marker → **MERGE เข้า main แล้ว จริง** (auto-merge, `2d165b73`) ยืนยันด้วย `git merge-base --is-ancestor` แล้ว
- `pirate-force-server#1190` (`claude/festive-shannon-ly40b5`, กู้ `#1167`) — ปลด draft ใส่ marker หลัง pf-adversary คืนผลไม่บล็อก (พบ 1 ข้อ RECORDED-NOT-PAID ก่อนรอบนี้ + 1 ข้อ PAID ในรอบนี้) → **Windows gate แดง (`pytest_subset`) ปิดใบอัตโนมัติ** — เหตุ: pre-existing bug ในเทส `#1167` เอง (`_lane_file()` เขียนไฟล์สองไฟล์ติดกันเร็วเกินไปจน `FileFinder` cache ไม่เห็นไฟล์ที่สอง บน Windows เท่านั้น ไม่เกิดบน Linux clone) — วินิจฉัยจาก gate log จริงผ่าน `get_job_logs` (ไม่ใช่เดา) แก้ด้วย `importlib.invalidate_caches()` หนึ่งบรรทัด กิ่งเดิมยังอยู่ ไม่เสียงาน
- `pirate-force-server#1204` (กิ่งเดิม `claude/festive-shannon-ly40b5` หลังแก้ + merge origin/main รอบสาม รวม M2 world/scene ของ LANE-A ที่ลง main กลางรอบ สะอาด ไม่มี conflict) — **แทนที่ `#1190`** เปิดแล้ว ไม่ draft มี marker ตั้งแต่เปิด (เนื้อหาเดิมผ่าน pf-adversary แล้ว ส่วนที่ใหม่คือการแก้เทสโครงสร้างล้วน ไม่แตะ wire/boot/login) ชุดเต็ม `15834 passed, 446 skipped, 44316 subtests, 0 failed` · **subscribe_pr_activity แล้ว รอผล gate จริงรอบสาม**
- `#1190` ปิดแล้ว ไม่ merge — โค้ดไม่เสีย (`#1204` สืบสภาพต่อจากกิ่งเดียวกัน)
- **ยังไม่อยู่บน main จนกว่ารอบถัดไปจะยืนยันด้วย `git merge-base --is-ancestor <sha> origin/main`** (ยกเว้น `#1189` ที่ยืนยันแล้ว)

SCOREBOARD: COMING | ผู้เล่นกดปุ่ม "ส่งจดหมาย" ในไคลเอนต์แล้วเซิร์ฟเวอร์ตอบกลับเป็นเฟรมจริงแทนที่จะเงียบ (ปุ่มที่หกจากแปดของซีมนี้) และปุ่มที่ห้า (add friend) มีสคริปต์วัด arming proof ของตัวเองเป็นครั้งแรก ปลดทางให้ `GT-318` เดินต่อได้ | pirate-force-server#1189 + #1190 (เปิดแล้ว ไม่ draft มี marker รอ gate) - ชุดเต็ม 15700 passed 446 skipped 43473 subtests 0 failed - preflight PASS - pf-adversary คืนผลจริงทั้งคู่ไม่บล็อก - GT-308 token head=1ecf43e4438f code=344b27154c11 RESULT=PASS วัดบน main จริง - #1167 กู้แล้ว sha 93930f68 ชุดเต็ม 15489 passed 0 failed - จดหมาย 1 ใบ บริโภค 1 ใบ - pf_bridge#1978
