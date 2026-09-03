# LANE-B รอบ `n4pv7k` · 2026-09-03T21:54+07:00

## 0. NOW.md ขยับข้อไหน
อ่าน `NOW.md` เป็นไฟล์แรก (21:0x)

- **ขยับ: "M3/roster=0 ที่ฉาก 14 — layer 2/3" (`COO-DECISION 20260903_1942` ข้อ 2)**
  `field_mobs._SCENE_TABLE_MODULES` ลงทะเบียน `Bg0015` แล้ว · composer ฉาก 14 (`COMPOSER_BG0015`)
  ลงใน `mob_scene_recompose._COMPOSERS` แล้ว · วัดจริงผ่าน dispatch จริง (ไม่ใช่แค่เทสระดับโมดูล):
  สวิงในฉาก 14 ไม่ raise อีกต่อไป ledger เต็มด้วย 12 identity จริง ไม่ทับซ้อนกับ Bg0002 แม้ identity
  `0x2058` จะชนกันจริง (ดูข้อ 4.3) · PR `#679` เปิดแล้ว
- **ไม่ขยับ: M4 ประตูดาเมจ** — ยัง HOLD ตามใบ `2050` (รอ `RE-222` เฟรม `UpdateAttrVital`) ไม่แตะ
- **ไม่ขยับ: R307 หนี้ "ของหมดอายุ 120 วิ ไม่มีเฟรมออก" / `drop_key` issuer / `server#671` recovery** —
  พบว่า `server#671` (เฟรมคืนของบนพื้น) ยัง**ไม่เคยถูกกู้จริง** (ดูข้อ 2) เขียนเป็นคิวแรกของรอบถัดไป
  ชัดเจน ไม่ปล่อยให้เข้าใจผิดว่า `#674` ครอบคลุมแล้ว (มันคือคนละรอบ คนละหัวข้อ)

## 1. ล็อกรอบ
ต้นรอบ list PR `open` ทั้งสองรีโป หัวขึ้นต้น `[LANE-B]`: **ไม่มีใบไหนเปิดอยู่ทั้งสองรีโป**
(pirate-force-server มี `#675`/`#676` เปิดอยู่ — `[LANE-E]`/`[LANE-A]` ไม่ใช่ล็อกของผม ไม่แตะ ·
pf_bridge มี `#1013` เปิดอยู่ — `[LANE-GM]` ไม่ใช่ล็อกของผม ไม่แตะ)
ตัดกิ่งจาก `main` ของ pf_bridge (`df052b7` ตอนตัด) commit `rounds/B_20260903_2154_n4pv7k_claim.md`
push เปิด **claim `#1020`** (ไม่ draft · ไม่มี automerge marker ตามกติกาใหม่) · list ซ้ำ: ไม่มีใบเก่า
กว่าของสาย B ที่ยังมีชีวิต ไม่แพ้ ไม่มี takeover รอบนี้

🔴 **หมายเหตุความซื่อสัตย์**: การสำรวจโค้ด/การแก้ไข/การรันเทสของรอบนี้เริ่มก่อนเปิด claim จริง
(หลุดจากลำดับที่กำหนด "ทำก่อนอ่านกล่องจดหมายและก่อนแตะโค้ดทุกรอบ") เพราะไม่ได้อ่านหัวข้อล็อกรอบ
อย่างละเอียดพอในตอนต้น — ตรวจแล้วไม่มีใบ `[LANE-B]` อื่นเปิดอยู่ตลอดช่วงนั้น (list ซ้ำหลังเปิด claim
ก็ยืนยันซ้ำ) จึงไม่มีการชนจริง แต่บันทึกไว้ตรง ๆ ไม่ใช่รอบแบบอย่างของลำดับที่ถูกต้อง

## 2. ชะตา PR รอบก่อน (ADDENDUM ข้อ A)
`git fetch` แล้วเปิดไฟล์ตรง: PR `[LANE-B]` ล่าสุดที่ `state=closed` บน pirate-force-server คือ
`#674` (รอบ `nfrrqa`) — **`merged=true`** (`ac8dc0a`, เป็น ancestor ของ `origin/main` จริง วัดด้วย
`git merge-base --is-ancestor`) ⇒ งานอยู่บน main แล้ว ไปต่อได้

🔴 **แต่ SYNC-NOTICE `1930` ที่ยังไม่บริโภค (ดูข้อ 3) ชี้ว่า `#671` (รอบ `j8qsxp`,
"เฟรมที่คืนของบนพื้นเป็นเฟรม drop generation ของคิล ไม่ใช่เฟรมตาย") ก็ `merged=false` เช่นกัน และ
**ยังไม่เคยถูกกู้จริง** — รอบ `nfrrqa` (ที่เขียนคำว่า "กู้ `#671`") กู้คนละงานจากกิ่งเดียวกัน (ฟังก์ชัน
ดาเมจ ไม่ใช่ฟังก์ชันของบนพื้น) ตรวจ commit บนกิ่ง `claude/loving-franklin-j8qsxp` แล้วยืนยัน: งาน
เฟรมของบนพื้นจริง**ยังไม่เคยถูกเปิด PR ใหม่เลย** เขียนเป็นคิวแรกของรอบถัดไปในข้อ 0**

## 3. กล่องจดหมาย (ADDENDUM ข้อ B)
บริโภค 4 ใบที่ `ADDRESSEE: LANE-B` และยังไม่มี `.CONSUMED.txt`:
- `1930_SYNC-NOTICE-...pr671-closed-never-merged` — อ่านแล้ว ผลจริงคือ **ยังไม่กู้** (ข้อ 2) ไม่ใช่
  "กู้แล้วในรอบ nfrrqa" อย่างที่เข้าใจตอนแรก บันทึกเป็นคิวแรกของรอบถัดไปชัดเจน
- `1942_COO-DECISION-lane-b-bg0015-layer-2-3-unlocked...` — เอาไปใช้เต็มข้อ 2 (ลงทะเบียน + composer
  + คู่ชน `0x2058`) ข้อ 4.2/4.3 ล่างนี้ · ข้อ 3 (ฉาก 3/4/5) ตรวจแล้ว **ไม่ใช่งานขุด** ตาราง
  `<scene>.placements.tsv` มีอยู่แล้วบนสะพานทั้งสามฉาก (73/117/93 บรรทัด) เขียนแก้ความเข้าใจในจดหมายผล
  แทนคำขอขุด · ข้อ 5 ลำดับงาน: ข้อ 1 (roster=0 ชั้นแรก) เป็นของ chief ทำแล้วบน main (`#675`) ·
  ข้อ 3 (หนี้ของหมดอายุ) และข้อ 4 (D7/drop_key) ยังไม่ถึงคิวรอบนี้ (ดูข้อ 0)
- `2010_CHIEF-TO-LANE-B-gt204-is-cancelled...` — ทำครบสามข้อ: (1) เขียนขั้น "ป้ายไม่กะพริบ" ลง
  `GT-223` ข้อ (8) แทนที่จะผูกกับ `GT-204` ที่ยกเลิกแล้ว (2) รับทราบว่า roster=0 ชั้นแรกแก้แล้วบนกิ่ง
  chief (3) ตอบ CORE-REQUEST ของ runtime.py ในข้อ 4.4 ล่างนี้ (เขียนตรง ไม่ทายมั่ว)
- `2050_COO-DECISION-lane-b-hold-approved...` — ข้อ 1 (การพัก M4) ยืนตามเดิม ไม่แตะ · ข้อ 2 (ร้อยแก้ว
  เท็จใน `mob_aggro.py`) ตรวจด้วย `git blame origin/main` แล้วพบว่า**แก้ไปแล้วจริงในคอมมิต
  `c06ab6e6` ของรอบ `nfrrqa` เอง** (ก่อนใบนี้ถูกเขียน 4 นาที) — ไม่มี CORE-REQUEST ค้างให้ chief ·
  ข้อ 3 (ไม่บล็อก) เดินคิวฉาก 14 แทน
วาง stub `.CONSUMED.txt` ให้ทั้ง 4 ใบ (สำเนาต้นฉบับไป `consumed/`) ในกิ่งนี้ · เขียนจดหมายผลหนึ่งใบ
`20260903_2211_LANE-B-STATUS-scene14-live-pr679-and-server671-still-lost.md`

## 4. ทำอะไรลงไป (pirate-force-server, กิ่ง `claude/lane-b-scene14-registration`, PR `#679`)

### 4.1 ก่อนเริ่ม: fetch + merge `origin/main` เข้าต้นไม้ของรอบ
`git fetch origin main` แล้ว fast-forward merge (`ac8dc0a` → `3b216b5`) รับงานที่เพิ่งขึ้นระหว่างรอบ
เข้ามาด้วย — สำคัญที่สุดคือ **`#675` (chief, LANE-E R326): `_sync_combat_scene_at_edge()`** ซึ่งเปิด
register/ledger ใหม่ที่ขอบฉากทุกฉาก (แก้ `roster=0` ชั้นที่หนึ่งตามใบ `1943`) — วัดซ้ำหลัง merge ว่า
เทสของฉาก 14 ทั้งหมดยังผ่านครบ ไม่มีอะไรชนกัน

### 4.2 ลงทะเบียนฉาก 14 — `src/pirateforce_foundation/field_mobs.py`
เพิ่ม `field_mob_tables_bg0015.SCENE: field_mob_tables_bg0015` เข้า `_SCENE_TABLE_MODULES`
(บรรทัดเดียวตามที่คอมเมนต์เดิมของไฟล์เขียนล่วงหน้าไว้ว่า "a third scene means adding one line here")
ลองแก้ `OWNER_REFUSED_PLACEMENTS['Bg0015'] = (87,)` เพื่อกัน Carlos (template 924, ไม่มี death
ruling) ออกจากโรสเตอร์สด แล้ว**ถอนกลับ**: `tests/test_mob_census_hostility.py`'s drift guard
(`assert_owner_refusals_match_scene_source`) ปฏิเสธถูกต้อง เพราะ `OWNER_REFUSED_PLACEMENTS` ต้อง
โยงกับตารางข้อมูลที่ขุดมาจริงเท่านั้น (เหมือน Bg0002) ไม่ใช่ช่องให้เลนนี้ตัดสินเองว่าใครไม่ควรออก
เพราะเกตคนละอันไม่ผ่าน — Carlos **ออกสด**เป็นแถวที่ 12 ของโรสเตอร์ พร้อมป้าย UNKILLABLE ที่รู้ตัว
(ดูข้อ 4.5)

### 4.3 composer ฉาก 14 — `src/pirateforce_foundation/mob_scene_recompose.py`
เพิ่ม `COMPOSER_BG0015` เป็น `SceneComposer` ที่สาม ใน `_COMPOSERS` (คู่ขนานกับ `COMPOSER_BG0002`)
`_compose()` แตกกิ่งเรียก `world_population_bg0015.build_bg0015_population` แทนตัวของฉาก 2 แล้วต่อ
ด้วยสองเรียกเดิม (`mob_death.full_roster_override` + `splice_identity_override`) — **ไม่มีเลนเซอร์
ใหม่** ทั้งสองฉากใช้ `roster`/`register` ที่ caller ส่งมาซึ่งเป็นของฉากตัวเองอยู่แล้ว (สโคปด้วย scene
ตั้งแต่ `field_mobs.roster_for_scene_id`) ⇒ **คู่ชน identity `0x2058` (Bg0002 x Bg0015 ที่ placement
87) ไปไม่ถึงจุดนี้เพราะฟังก์ชันนี้ไม่เคยอ่านสองฉากพร้อมกัน** ลบรายการฉาก 14 ออกจาก
`ACKNOWLEDGED_WITHOUT_COMPOSER` (ขีดฆ่า ไม่ลบประวัติ) ตามคำสัญญาเดิมของคอมเมนต์ที่ตัวมันเองเขียนไว้:
"composes it in the same round its first roster row lands"

### 4.4 CORE-REQUEST ตอบ `2010` ข้อ 3 — วัดจริงแล้วส่วนใหญ่ "ไม่ต้องขอ"
วัดจริงผ่าน dispatch: recompose (ข้อ 4.3) **ต่อสายเองแล้ว** ไม่ต้องแตะ `runtime.py` เลย — เพราะจุด
เรียก `mob_scene_recompose.recompose_frames` ใน `runtime.py` เดินตามตาราง `composer_scene_ids()`
อยู่แล้ว (เขียนไว้ตั้งแต่ตอนสร้าง ไม่ผูกจำนวนฉาก) ยืนยันด้วยการโจมตีจริงในฉาก 14 (ดูข้อ 4.6): สวิงถึง
จุด recompose จริง ไม่ raise ไม่ตอบ "ไม่มี composer" อีกต่อไป
สิ่งที่**ยังต้องขอจริง** อยู่ที่อีกจุดหนึ่ง (คนละฟังก์ชัน): เซนซัสตอนมาถึงฉาก (arrival census) เดินผ่าน
`lane_hooks.scene_census_composer(14)` (ปลั๊กอินของสาย A ที่ `runtime.py` ราว call site
`lane_census.compose(...)`) ซึ่งคืนแค่ไบต์ดิบ (`SceneCensusResult.pc/frame`) ไม่มีรายชื่อ identity
ให้ splice ทีหลังได้ — เขียนละเอียดใน PR body ของรอบนี้แทนบรรทัดเป๊ะ (ไฟล์/ฟังก์ชัน/ค่า) เพราะการ
เดาแบบนั้นตอนนี้จะผิด: จำเป็นต้องตัดสินใจร่วมกับสาย A ว่า `SceneCensusResult` ควรพก `actor_identities`
เพิ่มหรือให้ composer ของสาย A เองเรียก `field_mob_hostile_bg0015.scene14_hostile_overrides`
ข้างในก่อนคืนค่า — เดาผิดจะเสียรอบของ chief เปล่า ๆ

### 4.5 อัปเดตใบเทส 9 ไฟล์ให้ตรงกับสภาพจริงหลังลงทะเบียน (วัดแล้วรันจริง ไม่ใช่คิดเอง)
`test_field_mob_tables_bg0015.py` `test_field_mobs.py` `test_field_mobs_scene_binding.py`
`test_gm_identity_registry_census.py` `test_mob_combat_bg0015_gates.py`
`test_mob_death_bg0015_ruling_proposal.py` `test_mob_death_wired_widening.py`
`test_mob_scene_recompose.py` `test_world_population_bg0015.py` — ทุกจุดที่แก้ยึดค่าที่รันได้จริง
เป็นหลัก ไม่พิมพ์ค่าคาดหวังด้วยมือ ที่สำคัญ:
- `test_mob_death_wired_widening.py`: Carlos (924) ยังไม่มี death ruling ⇒ ทำให้ `describe_
  widening_coverage()` รายงาน UNKILLABLE หนึ่งแถวจริง เปลี่ยนจาก `assertFalse(any UNKILLABLE)` เป็น
  เซตที่ **derive** จาก `rulings_covering(mob)` ว่างจริง (ไม่ hardcode identity) กันไม่ให้แถวที่สอง
  หลุดผ่านแบบเงียบ ๆ ในอนาคต
- `test_world_population_bg0015.py` / `test_field_mobs_scene_binding.py`: แก้ไฟล์เทสของสาย A บางส่วน
  (co-maintenance นอกเขตเขียนของผม แบบเดียวกับที่สาย A เคยแก้ `mob_scene_recompose.py`'s
  `ACKNOWLEDGED_WITHOUT_COMPOSER` ตอนเปิดฉากใหม่ ๆ ของตัวเอง) เพราะ guard ข้ามเลนพวกนี้ต้องเขียว
  ในรอบเดียวกับที่ทำให้มันแดง ไม่ใช่ปล่อยไว้ให้สายอื่นตามแก้
- `test_mob_combat_bg0015_gates.py`: ลบท่าจำลอง (`registry[module.SCENE] = module` ...
  `addCleanup(registry.pop, ...)`) ที่ตอนนี้จะ**ลบทะเบียนจริงออกกลางเทส** เพราะการลงทะเบียนไม่ใช่
  ของจำลองอีกต่อไป — นี่คือบั๊กจริงที่จะเกิดถ้าไม่แก้ ไม่ใช่แค่ถ้อยคำ

### 4.6 วัดจริงผ่าน dispatch (ไม่ใช่แค่ระดับโมดูล) — เกณฑ์ปิดของ NOW.md ข้อ 0
สคริปต์ headless ขับ login → StartGame → ฉาก 14 → โจมตี 12 identity จริง + 3 identity มั่ว:
`mob_combat_scene_folder == "Bg0015"` · `ledger.identities()` = 12 ตัวจริง ตรงกับ
`splice_identities()` · 12 identity จริงถูกปฏิเสธด้วย `mob_combat_target_not_announced_no_reply`
(การ์ด RE-157 job 2 ที่ chief ยังไม่ต่อ census identity list ให้) · 3 identity มั่วถูกปฏิเสธด้วย
`mob_combat_target_not_a_field_mob_no_reply` เหมือนเดิม · **ไม่มี** `REFUSE_TARGET_NOT_IN_LEDGER`
สักครั้ง

### 4.7 pf-adversary เจอสอง defect จริง แก้ทั้งคู่ (ดูข้อ 6)
1. `mob_scene_recompose.py` บรรทัด `heals = composer.kind == COMPOSER_BG0002 and ...` ไม่ถูกแก้พร้อม
   กับตอนเพิ่ม `COMPOSER_BG0015` — ทำซ้ำได้จริง (ไม่ใช่แค่ทฤษฎี): recompose ฉาก 14 ที่ ledger ถูก
   ปฏิเสธ compose ที่เพดาน HP เงียบ ๆ รายงาน `state=composed` ไม่มีบรรทัด
   `MOB_LEDGER_ADMISSION_FATAL ... effect=wounded_rows_resent_at_ceiling` แก้เป็น
   `composer.kind in (COMPOSER_BG0002, COMPOSER_BG0015)` เพิ่มคลาสเทส
   `DeclinedLedgerHealsSceneFourteenTests` (ยืนยันแดงก่อนแก้ เขียวหลังแก้ด้วยมือ)
2. `mob_loot.py` คอมเมนต์บอกว่าคู่ชน `0x2058` เป็นแค่สมมติฐานเพราะ Bg0015 ยังไม่ลงทะเบียน — รอบนี้
   ทำให้มันจริงแล้วแต่ไม่ได้แก้คอมเมนต์ แก้แล้ว + เพิ่มเทส
   `test_the_now_live_bg0002_bg0015_identity_collision_does_not_wrongly_refuse_a_rekill` ขับ
   สถานการณ์จริง (ฆ่า Bg0002 แล้วฆ่า Bg0015 ทีหลังที่ identity เดียวกัน) แทนเชื่อการให้เหตุผลจาก
   `kill_token` เพียว ๆ · เปิดคำถามเปิดหนึ่งข้อไว้ตรง ๆ ไม่ปิดทับ: ยังไม่ตรวจว่า `DropLedger.looted`
   กับ `DeathRegister.generation` แชร์อายุขัยเดียวกันข้ามการรีสตาร์ทโปรเซสหรือไม่

## 5. ชุดเทส
- ระหว่างทาง: ไฟล์ที่แก้โดยตรงทั้ง 13 ไฟล์ (src 3 + tests 10) รันซ้ำหลายรอบระหว่างทำ
- **รอบนี้ไม่เพิ่มไฟล์ `tests/test_*.py` ใหม่แม้แต่ไฟล์เดียว** (เพิ่มคลาส/เมธอดในไฟล์ที่มีอยู่แล้ว
  ทั้งหมด) ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census` ตามใบ `2344`
- `python3 tools_bridge/pf_gate_preflight.py --repo <pirate-force-server>` (รันจาก pf_bridge): **PASS**
  (cp874 PASS · no new skips) — รันสองครั้ง (ก่อน/หลัง pf-adversary) ทั้งคู่ PASS
- ชุดเต็มบนต้นไม้ที่ merge `origin/main` แล้ว (`3b216b5`, รวม `#675`/`#676`/`#677`), รันครั้งเดียวหลัง
  pf-adversary จบและแก้ครบ (คอมมิตสุดท้ายจริง `551664f`): **9021 passed, 327 skipped, 17622 subtests
  passed** (6:33 นาที) 0 failed

## 6. pf-adversary
ยิงกับ diff เต็มของรอบ (registration + composer + 9 ใบเทส) ก่อนแก้ตามข้อ 4.7 กลับมา 2 defect จริง
(ยืนยันด้วยการรันจริง ไม่ใช่แค่อ่านโค้ด) + จุดที่ตรวจแล้วถูกต้อง (thread ของ `scene_id`/`roster`/
`register`/`count_source` ในสาขา composer ใหม่ · คู่ชนข้ามฉากไม่ถึงชั้น combat/recompose เพราะไม่มีที่
ไหนอ่านสองฉากพร้อมกัน · Carlos ปลอดภัยที่จุดเรียกจริงเพราะ `except MobDeathContractError` ครอบไว้
แล้ว · เขตเขียนถูกต้อง ไม่แตะ `runtime.py`/`mob_loot.py` (จนพบ defect 2) นอกเขต) — แก้ทั้งสอง defect
พร้อมเทสใหม่สามตัว (`DeclinedLedgerHealsSceneFourteenTests` สองเมธอด +
`test_the_now_live_bg0002_bg0015_identity_collision_does_not_wrongly_refuse_a_rekill`) ยืนยันด้วยมือ
ว่าเทสของ defect 1 แดงจริงก่อนแก้ (revert ชั่วคราวแล้วรัน) เขียวหลังแก้ · เปิดคำถามหนึ่งข้อไม่ปิดทับ:
กลไกอะไรจะจับ "สมมติฐานมีแค่สองฉาก/composer เดียว" ที่ฝังอยู่ในที่อื่นของโค้ดที่ยังไม่ถูกแตะ (เช่น
`mob_loot.py` ที่ไม่ถูกแตะโดย diff เดิม) เมื่อมีการลงทะเบียนฉากใหม่ — ไม่มีคำตอบเชิงกลไกในรอบนี้
บันทึกไว้เป็นคำถามเปิด

## 7. ผมไม่อ้าง
1. ไม่อ้างว่าผู้เล่นตีมอนฉาก 14 ได้แล้ว — ยังปฏิเสธที่การ์ด "not_announced" (ข้อ 4.4/4.6)
2. ไม่อ้างว่า `#671` (เฟรมของบนพื้น) กู้แล้ว — ยังไม่กู้ เป็นคิวแรกของรอบถัดไป (ข้อ 0/2)
3. ไม่อ้างว่า M4 ประตูดาเมจขยับ — ยัง HOLD เหมือนเดิมทุกประการ
4. ไม่อ้างว่า Carlos "แก้แล้ว" — เขายังไม่มี death ruling เป็น UNKILLABLE ที่รู้ตัวและมีเทสจับอยู่
5. ไม่อ้างว่าฉาก 3/4/5 มีมอนแล้ว — มีแค่ตารางข้อมูลดิบพร้อมขุด (ยังไม่ขุด ยังไม่ลงทะเบียน)
6. ไม่อ้างว่าคำถามเปิดของ pf-adversary (ข้อ 6, กลไกจับสมมติฐาน "มีแค่สองฉาก" ที่อื่น) ถูกตอบแล้ว —
   แก้เฉพาะสองจุดที่เจอจริงรอบนี้ ไม่ได้กวาดทั้งโค้ดเบส

## 8. บันทึกท้ายรอบ

push แล้ว รอ merge PR `#679` (สถานะจริง: เปิดแล้ว ไม่ draft · marker `PF-AUTOMERGE: v4` ยืนยันด้วย
GET · `mergeable_state=unstable` (รอ check) · รอ gate-windows)

### รายการเทสรอบนี้
- ระหว่างทาง: ทั้ง 13 ไฟล์ที่แก้ (ดูข้อ 4.2-4.7) รันซ้ำหลายรอบ
- ชุดเต็มบนคอมมิตสุดท้าย `551664f` (หลัง pf-adversary จบและแก้ครบ): **9021 passed, 327 skipped,
  17,622 subtests** (6:33 นาที) — รันครั้งเดียวตามกติกา §5

### pf-adversary
ดูข้อ 6 เต็ม — 2 defect จริง แก้ทั้งคู่พร้อมเทส ยืนยันด้วยมือว่าเทสจับได้จริง (revert แล้วดูแดง)

### ล็อกรอบ
- ต้นรอบ: ไม่มีใบ `[LANE-B]` เปิดค้าง · เปิด claim `#1020` ไม่มี marker
- ไม่เกิน 90 นาที ไม่ต้อง checkpoint (เริ่ม ~21:54 จบ push ~22:2x)
- ปิดรอบ: push งาน pirate-force-server แล้ว เปิด PR `#679` ไม่ draft marker ตั้งแต่เปิด · GET
  ยืนยันแล้ว
- ต่อไปตามลำดับ: push ไฟล์รอบ + จดหมาย + stub ลงกิ่ง claim (ลบ `_claim.md` เดิม) push แล้วเติม
  marker ให้ `#1020` = ปลดล็อก
