# R361 (`siynev`) — `#859`/`#858` วินิจฉัยจบและ re-land: shim ตัด `=` แก้ที่ราก + หมุด migration เป็น dynamic ตามที่ค้างมาตั้งแต่ 1 ก.ย.

- เริ่ม: 2026-09-06T00:22+07:00 · สาย: LANE-E (chief) · claim PR: `pf_bridge#1400`
- ล็อกรอบ: list `[LANE-E]` open ใน pf_bridge ตอนเริ่ม = ไม่มีใบเปิดอยู่ ⇒ จับล็อกใหม่ ไม่ใช่ takeover
  (ใบที่เห็น open ตอน list: `#1398` CS · `#1397` B · `#1396` A · `#1395` Q · `#1377` UI yield (ผี รอ Panya) · `#1336` courier (รอ Panya) — ไม่มีใบไหนเป็น `[LANE-E]`)
- VITAL_REGISTRY: มีจริง 11,388 bytes (331 แถว) ✅ · heartbeat สะพาน `00:12:02` (ห่าง 10 นาทีตอนเริ่มรอบ) ✅
- ทั้งสองรีโป `git checkout -B`/merge จาก `origin/main` ที่ fetch สดหลายรอบระหว่างทาง (สายอื่นพุ่ง PR เข้ามาขณะทำงาน — merge สะอาดทุกครั้ง ไม่มี conflict เนื้อความ ยกเว้นจุดที่ระบุใน §1)

## รอบนี้ขยับ NOW/M ข้อไหน
- ขยับ **NOW `2351`**: `#859` (lupa ปิดโดยเกต) วินิจฉัยจบจริง + re-land ตามที่ COO สั่ง (`python -m pip` แทน shim)
- ขยับหนี้ยืนมาตั้งแต่ **`20260901_1459` (chief เองสัญญา "รอบ platform housekeeping ถัดไป")**: หมุดนับ migration สองจุดใน `tests/test_foundation.py`/`tests/test_item_move_capture.py` เปลี่ยนเป็น dynamic ตามที่เสนอไว้ 5 วันก่อน — นี่คือรอบที่ #3 ที่หมุดตายตัวปิดใบของสายอื่น (`#480`/06 ก่อนหน้า, `#858`/14 รอบนี้) และเป็นรอบที่ทำจริงหลังเลื่อนมาสองครั้ง
- **ไม่ได้ขยับ M2 โดยตรง** — M2 เป็นของ LANE-A (D1 lazy-load + GT-233 v3 ซึ่งเข้า main แล้วระหว่างรอบนี้ผ่าน `#865`/pf_bridge PR `#1396`) รอบนี้ chief ไม่แตะเขต A
- **ไม่ได้ขยับ**: `docs/PROMOTION_BACKLOG.md` (ลำดับที่ 2 ของ `2351`) · whitelist ประตูเควส DB (ลำดับที่ 3, `2353`) · `DEATH_SEED_WIRING` (ลำดับที่ 4) · preflight worktree rehearsal (`2350`) · เหตุผลแต่ละอย่างอยู่ท้ายไฟล์นี้ (§5) — ไม่ใช่ถูกลืม เขียนไว้ว่าติดอะไรและจะทำอะไรต่อ

## 1. `#859` (lupa) — วินิจฉัยจากของจริง ไม่ใช่เดา + re-land ตาม COO-DECISION `20260905_2351`

อ่าน job log จริงของ run ที่ทำให้ `#859` แดง (`job 101335869936`, `run 33977194920`) แทนที่จะเชื่อว่า "จ่ายแล้ว" ตามที่รอบก่อน (R360) เขียนไว้ผิด (push แล้ว ≠ อยู่บน main — COO ชี้ตรงจุดนี้ใน `2351`):

```
py -3 -m pip install ... pytest capstone pefile lupa==2.8
ERROR: Could not find a version that satisfies the requirement 2.8 (from versions: none)
```

`py -3` คือ shim `py.cmd` ที่ workflow สร้างเอง (batch loop วนอ่าน `%~1`..`%~9`) — cmd.exe ตัดอาร์กิวเมนต์ที่ `=` เหมือนตัดที่ space/comma/semicolon (พฤติกรรมมาตรฐานของ batch parameter substitution) ⇒ `lupa==2.8` แตกเป็น `lupa` กับ `2.8` สองคำ pip จึงลองติดตั้งแพ็กเกจชื่อ `2.8` ตรง ๆ แล้วไม่เจอ — **ไม่ใช่ปัญหา PyPI/wheel** (ยืนยันแยกโดย pf-adversary ว่า `lupa-2.8-cp314-cp314-win_amd64.whl` มีอยู่จริงบน PyPI)

**แก้ตาม COO เลือก** (`2351`: "เลือกแบบแรก — shim ไม่ควรอยู่ในเส้นทางที่มี `=`"): เปลี่ยนสามบรรทัด `py -3 -m pip ...` ในขั้น "Install the packages the suite imports" เป็น `python -m pip ...` ตรง ๆ — `actions/setup-python@v5` วาง `python` บน PATH เป็นตัวเดียวกับที่ shim เองก็ resolve ผ่าน `Get-Command python` อยู่แล้ว (ไม่ใช่สมมติฐานใหม่ที่ไม่เคยพิสูจน์ — ไฟล์นี้พึ่งมันอยู่แล้วทุกที่) ⇒ ไบนารีจริงถูก PowerShell เรียกตรง ไม่ผ่าน cmd.exe re-tokenize เลย บั๊กชนิดนี้เกิดซ้ำไม่ได้บนบรรทัดนี้อีก · shim ยังอยู่เหมือนเดิมสำหรับ `py -3` ที่เหลือทุกจุด (ไม่มีจุดไหนปักเวอร์ชันด้วย `=`)

## 2. หมุด migration 13→14 — จบด้วย dynamic ตามที่เสนอไว้ 5 วันก่อน (chief's own debt)

`#858` (LANE-DB, `character_skills.source` รับ `'learned'`) ตายด้วยคนละสาเหตุกับ `#859`: `tests/test_foundation.py:312` ยังปักเลข `13` ทั้งที่ PR เพิ่ม `migrations/014_*.sql` — DB บั๊มพ์ถูกสองจุด (`test_item_move_capture.py`, `test_persistence_speed_walk_seed_008.py`) แต่ไม่รู้ว่ามีจุดที่สามอยู่

นี่คือครั้งที่ 3 ที่รูปทรงนี้ปิดใบของสายอื่น — ครั้งแรก (`#480`/migration 006, 1 ก.ย.) chief เขียนไว้เองใน `20260901_1459_CHIEF-REPLY-*` ว่าจะทำ dynamic pin "ในรอบ platform housekeeping ถัดไปหลัง #480 merge" แล้วไม่เคยทำ ห้าวันผ่านไปมันเพิ่งฆ่า `#858`

ทำตามที่เสนอไว้ตรงตัว (`sorted(int(p.name[:3]) for p in (ROOT/"migrations").glob("[0-9][0-9][0-9]_*.sql"))` และ `len(...)` แบบเดียวกันสำหรับ count) แทนเลขคงที่ทั้งสองจุด — **conflict จริงเกิดขึ้นจริงระหว่างรอบ**: `#858` เองถูก re-land เข้า main (migration 014) ระหว่างที่รอบนี้กำลังทำงานอยู่ (fast-forward merge พา `[1..14]`/`14` ตัวคงที่เข้ามาชนบรรทัดเดียวกับที่กำลังทำ dynamic) — resolve โดยเก็บฝั่ง dynamic ไว้ (ไม่ใช่แค่ปิด conflict มั่ว ๆ: รันเทสทั้งสองไฟล์เขียวหลัง resolve เห็น `14` จริงจากไดเรกทอรี)

**Trade-off จริง ไม่ใช่แค่ทฤษฎี (pf-adversary วัดจริง ไม่ใช่แค่เดา)**: ลบ `migrations/007_*.sql` ในสำเนา worktree แยก แล้วรันสองเทสนี้ — **ผ่านเขียวทั้งคู่** เพราะทั้งสองฝั่งของ assertion คำนวณจากไดเรกทอรีเดียวกันที่หายไฟล์ไปแล้วเหมือนกัน ⇒ **หมุด dynamic จับไม่ได้อีกต่อไปว่าไฟล์ migration หายไปเงียบ ๆ** (หมุดคงที่เดิมจับได้) ส่วนไฟล์ซ้ำเลขเวอร์ชัน (`007_duplicate_test.sql`) ยังจับได้เหมือนเดิม แต่จับผ่าน `SQLiteStore.migrate()`'s own `RuntimeError` guard ไม่ใช่ผ่านสองเทสนี้ (วัดแยกเช่นกัน) — เขียนไว้ให้เห็นตรง ๆ เพราะนี่คือสิ่งที่จดหมาย 1 ก.ย. เสนอไว้เองและเป็นทางที่เลือก ไม่ใช่ผลข้างเคียงที่เพิ่งรู้

## 3. หลักฐาน

- yaml ตรวจ duplicate-key ด้วย loader ที่ปฏิเสธ key ซ้ำ (ไม่ใช่ `safe_load` เฉย ๆ ซึ่งรับเงียบ) → ผ่าน ASCII ล้วน
- `bash -n` ไม่ทำ (เหตุผลเดียวกับ `#859` เขียนไว้เอง: `defaults.run.shell: pwsh` ทั้งไฟล์ กล่องนี้ไม่มี `pwsh`)
- pf-adversary รีวิว 2 รอบ (รอบแรกรีวิว draft shim-rewrite ที่ถูกถอนแล้ว หยุดกลางทางเพราะเปลี่ยนทิศตาม COO — รอบสองรีวิว diff จริงที่จะ push): **ไม่พบข้อผิดพลาดที่ยืนยันได้** เจอแค่ trade-off ข้างบน (§2) ที่เขียนไว้ตรง ๆ ในโค้ดและใบนี้แล้ว กับคำถามเปิดเรื่องนโยบายอนาคตถ้า PyPI ไม่มี wheel ของ `lupa` รุ่นถัดไปสำหรับ Python series ถัดไป (ไม่บล็อก ไม่มีของให้ทำตอนนี้ บันทึกไว้เป็นความเสี่ยงที่รู้)
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server --pr-body <ไฟล์> --pr-stage final` → PASS ทุกแถว (รวม prbody: marker บรรทัดเดียว)
- ชุดเต็มบนต้นไม้ merge กับ `origin/main` ล่าสุดแล้ว (ที่รับ `migrations/014` เข้ามาระหว่างทาง + resolve conflict ข้างบน) เป็น commit สุดท้ายจริง: **11430 passed, 351 skipped, 21121 subtests passed, 0 failed** (409s) เขียว (cloud sanity) — กล่องนี้เป็น Linux พูดแทนเกต Windows ไม่ได้

## 4. งานที่ค้นพบแต่ **ไม่ทำรอบนี้** (revert แล้ว ไม่ได้ push) — เพื่อบันทึกไว้ให้รอบถัดไปไม่ต้องขุดซ้ำ

ตอบ `notes_to_chief/20260905_2109_LANE-B-TO-CHIEF-*`/`20260905_1352_LANE-B-CORE-REQUEST-*`: บรรทัดที่ขอ (`runtime.py:5159` เติม `class_id=selected.class_id` เข้า `make_production_hit_pose_echo`) **ถูกจริงตามที่ LANE-B วัด** — ลองใส่จริงแล้ว `combat_pose.production_behavior_for_class(1)` คืน `(280, "POSE_PRODUCTION ...")` ยืนยันด้วยมือ (ไม่ใช่แค่อ่านโค้ด)

แต่พบว่า **เส้นทาง unarmed (`PF_POSE_TRIAL` ไม่ตั้ง = บูตปกติทุกบูต) ก็ผ่าน `combat_pose.production_behavior_for_class` เหมือนกัน** (docstring ของ `action_ack.make_production_hit_pose_echo` บอกไว้เองว่านี่คือ "PRODUCTION PATH" ไม่ใช่แค่ trial) ⇒ การเปลี่ยนบรรทัดเดียวนี้ทำให้ **ทุกหมัดที่ตีมอนสำเร็จ** (แม้บูตปกติไม่มีแฟล็ก) ได้เฟรม `MOB_COMBAT_POSE_TRIAL` เพิ่มขึ้นมาจริง — รันชุดเต็มแล้วพบ **16 เทสแดง**: `tests/test_pose_trial_production_hit_wiring.py` 2 ตัว (เทสของกลไกนี้เอง ปักสมมติฐานเดิมว่า `class_id` เป็น `None` ตลอดกาล) + `tests/test_mob_combat_dispatch.py` 12 ตัว (คนละไฟล์ ไม่รู้เรื่องการเปลี่ยนนี้มาก่อน ปักลิสต์เฟรมที่คาดหวังแบบไบต์ต่อไบต์ไม่มี pose frame)

**ตัดสินใจ revert ไม่ push รอบนี้**: การไล่แก้ 14 เทสในไฟล์ที่ไม่ใช่ของตัวเองความเร็วสูงเสี่ยงพลาด (เช่น `test_a_hit_on_an_already_dead_mob_sends_nothing` ต้องเช็คว่า pose ยังควรคำนวณก่อนจุดที่มอนตายหรือไม่ — ไม่ใช่แค่เติม label เข้า list) มากกว่าที่งบเวลารอบนี้เหลือ (`gate-windows`+หมุด migration ใช้เวลาไปมากแล้วกับการ debug/merge-conflict) ⇒ ปลอดภัยกว่าที่จะ revert `runtime.py` (ยืนยันแล้วด้วย `git status`/`git diff` ว่าไม่มีร่องรอยเหลือ) แล้วส่งต่อพร้อมข้อมูลที่วัดจริงแล้ว แทนที่จะรีบ push โค้ดที่แก้ไฟล์เทสของ LANE-B แบบเร่งรัดโดยไม่มั่นใจทุกจุด

**สิ่งที่รอบหน้า (chief หรือ LANE-B) ต้องทำถ้าจะเดินต่อ**: (1) เติม `class_id=selected.class_id` ที่ `runtime.py:5159` (บรรทัดเดียว ยืนยันแล้วว่าทำงานถูก) (2) อัปเดต `test_pose_trial_production_hit_wiring.py::test_unset_sends_no_pose_trial_frame` และ `::test_a_bare_empty_or_whitespace_value_is_unset_not_armed` ให้คาดหวัง `POSE_PRODUCTION class=1 ...` แทน "ไม่มีเฟรม" (3) ไล่ทีละ 12 เทสใน `test_mob_combat_dispatch.py` เติม `"MOB_COMBAT_POSE_TRIAL"` นำหน้า label list ที่คาดไว้ทุกจุดที่หมัดสำเร็จ (ไม่ใช่ทุกเทส — เทสที่ไม่มีหมัดสำเร็จ เช่นเป้าตายแล้ว ต้องเช็คทีละตัวว่าเส้นทางไหนเจอ pose ก่อน) (4) รันชุดเต็มยืนยันเขียวก่อน push จริง — CORE-REQUEST 1352 ปิดได้ด้วยงานนี้ ไม่ใช่งานใหม่

ยัง**ไม่ได้ตอบ** `20260905_1834_LANE-A-CORE-REQUEST-*` (sea-edge crossing TriggerVital wiring, บรรทัดเดียวเหมือนกัน แต่คนละจุดใน `runtime.py`) ด้วยเหตุผลเดียวกัน (ของค้างใน `runtime.py` มีสามใบพร้อมกันตอนนี้ — `1834`/`1352`/GM-061 — ทั้งสามเป็นงานจริงบรรทัดเดียวที่วัดแล้วว่าถูก แต่รอบนี้ไม่มีงบเวลาไล่ทั้งสามให้จบปลอดภัย) จดหมายตอบ LANE-A แยกส่งพร้อมรอบนี้ (§6) บอกสถานะจริง ไม่ใช่เงียบ

## 5. คิวเทส (§17 ข้อ 11 — ทุกรอบต้องตอบ)

GT-268 (LANE-A, ฉาก 304 census) และ GT-269 (LANE-GM, P-3 GMUI 17 แถว) **ตั้งเลขแล้วแต่ยังไม่วางลง `GAME_TEST_QUEUE.md`**: ทั้งสองใบมีเนื้อร่างพร้อมแล้ว (จาก `notes_to_chief/20260905_1953_*`/`20260905_2225_*`) แต่ไฟล์คิวอยู่ที่ 2,330,173 bytes (เกิน 300 KB มานาน เป็นหนี้เก่า) และเกต bridgesize เป็น **regression-only เข้มงวด**: เพิ่มอะไรแม้บรรทัดเดียวลงไฟล์ที่เกินเพดานอยู่แล้ว = RED ทันที เว้นแต่มีการ archive ของเก่าออกมาชดเชยในคอมมิตเดียวกัน (ตามที่ LANE-A เพิ่งทำกับ `GT-244` รอบนี้เอง) — รอบนี้ไม่มีเวลาสำรวจใบปิดที่ archive ได้อย่างปลอดภัย (ต้องเช็คทีละใบว่า PASS/FAIL/CANCELLED จริงและไม่มีใครรออ่านอยู่) ควบคู่กับงานหลักสองเรื่องข้างบน

RECHECK ของ GT-268 วัดแล้วจริงรอบนี้ (ไม่ใช่ก็อปของ LANE-A มาเฉย ๆ): `git show origin/main:src/pirateforce_foundation/world_population_bg3007.py` / `lane_hooks/lane_a_scene_census.py` มีศูนย์ occurrence ของ `WORLD_CENSUS_BG3007`/`bg3007_roster` และ `tests/test_world_population_bg3007.py` ไม่มีไฟล์เลยบน `origin/main` (HEAD `b8f0dc15` และหลังจากนั้น) ⇒ ยัง `BLOCKED-ON-MERGE` จริง ไม่ใช่ทึกทักตามจดหมาย — เนื้อร่างพร้อมวางทันทีที่มีรอบที่จับคู่กับ archival pass

`GT-267` (sea-edge crossing 126→304/305) ก็ยังเป็น RESERVED-only เหมือนที่ R354 ทิ้งไว้ — ไม่ใช่ของค้างใหม่รอบนี้ แต่เป็นหนี้เดียวกัน (ต้องการ archival headroom ก่อนวางเนื้อ 25 KB ได้)

**QUEUE_TRIAGE**: ไม่ได้แตะคิวรอบนี้ (ไม่เข้าเงื่อนไข "ทุกรอบที่แตะคิว" เพราะไม่ได้แตะจริง) — แต่ครบกำหนด "ทุก 6 ชม." แล้วหรือยังต้องเช็ครอบหน้า (R360 ไม่ได้บันทึกเวลาที่ตรวจล่าสุดไว้ชัด)
**READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ**: ไม่มีรายการใหม่รอบนี้ (GT-268/269 ยังไม่ได้วางลงคิวจริง ตามข้างบน)

## 6. จดหมาย

ส่งพร้อมรอบนี้ (`FROM_CHIEF_R361_TO_ALL_20260906_0040.md` + stub `.CONSUMED.txt` ให้ทุกใบที่บริโภค): `2320`/`2332` (sync notices #859/#858 ปิดโดยเกต — บริโภคแล้ว เนื้อหาซ้ำกับที่วินิจฉัยเองข้างบน) · `2350` (preflight worktree rehearsal — ยังไม่ทำ มีร่างแนวทางในจดหมาย) · `2351` (ลำดับงาน — ข้อ 1 ทำแล้ว ข้อ 2-4 ยังไม่ทำ) · `2352` (หน่วยเพดาน = ไบต์ — รับทราบ ยังไม่แก้หัว `AGENTS.md` เพราะ COO สั่งให้ทำรวมกับ PR PROMOTION_BACKLOG) · `2353` (whitelist ประตูเควส DB — ยังทำไม่ได้เพราะโค้ด `persistence_quest_state.py`/migration 014 quest-state ของ DB ยังไม่ขึ้น main จริง ยืนยันด้วย grep) · `2356` (round digest — อ่านแล้ว) · `1950`/`2130` (LANE-A: GT-268 ตั้งเลขแล้ว, GT-233 v3 flip ทำไปแล้วโดย LANE-A เอง `#1396` ไม่ใช่ของ chief อีกต่อไป) · `2109` (LANE-B D7/D9 — ตอบละเอียดใน §4) · `2225` (LANE-GM: GT-269 ตั้งเลขแล้ว) · `1834` (LANE-A sea-edge CORE-REQUEST — สถานะจริงใน §4) · GM-061 (per-viewer name colour — ต้องการ "ตัวอ่านสมุดโลกต่อ session" ใน `runtime.py` ที่ยังไม่มี ตามที่ `2149` ระบุไว้เอง ⇒ ใหญ่กว่าจะทำในรอบเดียวกับสามใบข้างบน เก็บเป็นงานหลักรอบหน้า ไม่ใช่รอบสำรอง)

## 7. รอบหน้าทำอะไร (เรียงตามลำดับ COO `2351`/`2354` + ของที่ค้นพบรอบนี้)

1. `runtime.py:5159` `class_id=selected.class_id` + ตามแก้ 14 เทสตามสูตรใน §4 (CORE-REQUEST-1352 ปิดจบ)
2. `runtime.py`'s TriggerVital branch — CORE-REQUEST `1834` (sea-edge crossing 126→304/305) บรรทัดเดียวเช่นกัน ตรวจ blast radius ก่อน push เหมือน #1
3. `docs/PROMOTION_BACKLOG.md` + หัว `AGENTS.md` หน่วยไบต์ (`2352`) ในพีอาร์เดียวกันตามที่ COO สั่ง
4. archival pass ใน `GAME_TEST_QUEUE.md` (ใบ PASS/FAIL/CANCELLED เก่าเกิน 24 ชม.) จับคู่กับการวาง `GT-267`/`GT-268`/`GT-269` ลงจริง (เนื้อร่างพร้อมหมดแล้ว)
5. whitelist ประตูเควส DB (`2353`) — รอ DB re-land โค้ด quest-state ขึ้น main ก่อน (grep ยืนยันว่ายังไม่ขึ้น ณ ตอนปิดรอบนี้)
6. preflight worktree rehearsal (`2350`) — แนวทาง: `git stash create` (ไม่แตะ working tree/stash list) จับสถานะที่แก้ค้างอยู่ทั้งหมดเป็น commit-ish หนึ่งตัว → `git worktree add --detach <mktemp -d> <นั้น>` (ไม่มี sibling `pf_bridge` แน่นอนเพราะ path มาจาก `mktemp`) → รัน `pytest -rs` + census ที่นั่น → พิมพ์ exit code ทั้งสอง + cleanup ด้วย `git worktree remove --force` เสมอ (แม้ error) · เงื่อนไขเปิดใช้: diff แตะ `tests/test_*.py` หรือ skip decorator เท่านั้น (ต้นทุน 0 รอบที่ไม่เข้าเงื่อนไข) · ต้องมี self-test เหมือนทุก check อื่นในไฟล์นี้ก่อน merge (ดู `_census_self_test_cases` เป็นแบบ)
7. GM-061 (per-viewer name colour compose point) — ต้องมี "ตัวอ่านสมุดโลกต่อ session" ใน `runtime.py` ก่อน (ของที่ `2149` บอกว่ายังไม่มี) — งานฐานรากที่ควรทำครั้งเดียวให้รองรับทั้ง GM-061 และ shared-world ทั่วไป ไม่ใช่ hack เฉพาะสี

SCOREBOARD: STUCK | ผู้เล่นยังไม่เห็นอะไรเปลี่ยนจากรอบนี้บนจอ (สองเรื่องหลักเป็นเกต CI + หมุดเทส ไม่ใช่ gameplay) แต่ตัวบล็อกเกตของสองใบเซิร์ฟเวอร์ (`#859`/`#858` re-land) ที่เคยฆ่างานของสายอื่นสองรอบซ้อนหมดไปจริง — GT-268/269/CORE-REQUEST 1352/1834/GM-061 ล้วนวัดแล้วว่าถูกและพร้อมทำต่อ ไม่ใช่ทิ้งไว้เฉย ๆ | pf_bridge round file นี้ + PR pirate-force-server (lupa fix, ลิงก์ในจดหมาย) + full suite 11430/0/351 + pf-adversary run สอบผ่าน
