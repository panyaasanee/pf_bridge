# LANE-B round 4tnhzw — 2026-09-06T09:03+07:00 start

## TWO_SESSIONS_SAME_SCENE
**ไม่ครบ — pf-adversary จับได้หลังปลดล็อก (เพิ่มบรรทัดนี้ตอนนี้ตามกฎ "ผล adversary คืนหลังปลด ⇒
เขียนลงไฟล์รอบ รอบถัดไปหยิบเป็นงานแรก"):** `mob_death_register` เป็น instance ต่อ **connection**
(`runtime.py:1404` `self.mob_death_register = mob_death.DeathRegister()` ใน
`PersistentGameSessionState.__init__`) ไม่ใช่ต่อฉาก — ยืนยันด้วย nonclaim ที่มีอยู่แล้วเองใน
`scenarios/combat_death_001.json` บรรทัด 104: "runtime.py builds a DeathRegister per CONNECTION, so
two sessions in one scene each legitimately accept a kill on the same monster" · **ไม่ใช่บั๊กใหม่ของ
รอบนี้** (`runtime.py` ไม่ถูกแตะในกิ่งนี้เลย — pf-adversary ยืนยันด้วย `git diff` แล้ว) แต่รอบนี้ขยาย
พื้นผิวที่ได้รับผลกระทบจาก 6 ฉากเป็น 10 ฉากโดยไม่เคยเขียนบรรทัดนี้แม้แต่ครั้งเดียว — คำถามที่ยังไม่มี
คำตอบ: สองผู้เล่นในฉากเดียวกัน (เช่น Bg0011) ฆ่ามอนตัวเดียวกันพร้อมกัน ผู้เล่นคนที่สองจะยังเห็นมัน
มีชีวิตอยู่ไหม และ "ฆ่า" ซ้ำได้ไหมเพราะ register คนละ instance — **ยังไม่มีคำตอบ ต้องเปิดใบ ASK-COO
รอบหน้า** ไม่ใช่แก้เองตอนนี้ (ปลดล็อกแล้ว ห้ามแตะโค้ดในรอบนี้)

## รอบนี้ขยับ NOW/M ข้อไหน
M3 "สนามมีมอนสเตอร์" — ลงทะเบียนมอนที่ตายได้จริงในสี่ฉากใหม่ (Bg0006, Bg0007, Bg0009, Bg0011)
ตามที่ COO ตัดสินใน `notes_to_chief/20260906_0748_COO-DECISION-b0659-send-four-clean-scenes-now-
bg0010-unresolved-is-a-static-ticket-body-to-chief-bg0009-zero-drop-m-avatars-are-ordinary-mobs-
LANE-B.md` (ตอบใบ `20260906_0659_LANE-B-ASK-COO-five-scene-recon-*`) — เดินตามแบบ Bg0008
(`pirate-force-server#899`, commit `88fab41`/merge `a0b892f5`) เป๊ะ

## ทำอะไรไปแล้ว
1. **ขุด roster จริงทั้งสี่ฉาก** ด้วย `tools/pf_mine_scene_mob_roster.py --identity-rule cline`
   ต่อ `pf_bridge/gamedata` clone จริง (ไม่เดา) — ผลจริง (ไม่ใช่เลขจากใบ recon `0659`):
   - **Bg0006**: 2 hostile placements, **2 templates** (222 "Crull Two Horns", 226 "Anger
     Lion") — ตรงกับที่ใบ `0659`/COO ระบุ `{222,226}`
   - **Bg0007**: 9 hostile placements, **7 templates** (388, 390, 393, 395, 397, 526, 536)
   - **Bg0009**: 5 hostile placements, **5 templates** (314, 317, 320, **546, 549**) — 546
     ("Black braid Edward") / 549 ("Bermuda Banshee") = placement 56/57 ที่ COO สั่งให้ ship
     ปกติ (avatar `M0..` ไม่ใช่ `P_`) ไม่ withhold
   - **Bg0011**: 10 hostile placements, **5 templates** (669, 674, 693, 696, 697)
   - **ไม่มีแถวไหนในสี่ฉากนี้เป็น avatar `P_` (player model)** — ไม่มี Nina/Carlos-style
     withhold ต้องทำในรอบนี้
2. **ตัวเลขต่างจากใบ `0659`**: ใบ `0659` เป็น recon summary เท่านั้น (COO เขียนกำกับไว้เอง)
   ตัวเลขที่ commit ในรอบนี้ทั้งหมดมาจากการรันเครื่องมือจริงในรอบนี้ ไม่ใช่ก็อปจากใบ recon
3. **สร้าง 4 ไฟล์ `field_mob_tables_bg000{6,7,9}.py` + `_bg0011.py`** ตามรูปแบบ
   `field_mob_tables_bg0008.py` เป๊ะ (เดียวกันทุก field/comment block)
   🔴 **หมายเหตุ casing สำคัญ**: `field_mobs.scene_for_scene_id(6)` resolve ฉาก 6 เป็น
   `'bg0006'` (lowercase) ไม่ใช่ `'Bg0006'` — `world_scene_folder.py` เองบันทึกไว้แล้วว่า
   `SCENE_NAME.s_MODLE_ID` เป็น `Bg0006` แต่โฟลเดอร์จริงบนดิสก์เป็น `bg0006` (คนละสเปลลิงเหมือน
   bg0001) — mine ด้วย `--scene bg0006` (lowercase) ให้ตรงกับโฟลเดอร์จริง ไม่ใช่ตารางชื่อ
   มิฉะนั้น `roster_for_scene_id(6)` จะได้ 0 แถว (เจอจริงระหว่างทำรอบนี้ ก่อนแก้)
4. **ลงทะเบียน 4 คีย์ใหม่** ใน `field_mobs._SCENE_TABLE_MODULES` + เพิ่ม
   `BG0006_SCENE`/`BG0007_SCENE`/`BG0009_SCENE`/`BG0011_SCENE` constants
5. **เพิ่ม `field_mobs.DROPS_UNMINED_PLACEMENTS`** (ดิกใหม่ documentary-only ไม่กรองอะไรออก)
   สำหรับ Bg0009 placement 56/57 — ต่างจาก `LANE_WITHHELD_PLACEMENTS` ตรงที่ไม่ตัดออกจากสิ่งที่
   ship จริง เป็นแค่ธงบอกว่า drop table ยังไม่ mine (งาน P-1 คนละหาง)
6. **เพิ่ม 4 รายการใน `mob_death.WIDENING_RULINGS` + `WIDENING_RULING_SCENES`** ชื่อใบ
   `"COO-DECISION widen-death-scope-bg000{6,7,9,11}-<N>-templates 2026-09-06T07:48+07:00"`
   ครอบ template set จริงของแต่ละฉาก (ไม่ใช่เดาจากใบ `0659`)
7. **เดินสาย `field_mob_ai_tables.py`** ผ่าน `tools/pf_mine_mob_ai_rows.py` (เพิ่ม import 4 โมดูล
   ใหม่ใน `load_roster_modules`) — พิสูจน์ `ai_row_missing` จริงก่อนแก้ (scene 7 พังก่อน: AI_WANDER
   10 ไม่มี, scene 9: AI_COMBAT 142 ไม่มี, scene 11: AI_COMBAT 280 ไม่มี; scene 6 ไม่พังเพราะ 2 แถว
   ของมันชี้ id ที่ union มีอยู่แล้ว) — regenerate แล้ว `mob_ai_control.open_register` เขียวทั้ง 11
   ฉากที่ live (1,2,3,4,5,6,7,8,9,11,14)
8. **`mob_scene_recompose.py`**: เพิ่ม `COMPOSER_BG0006/7/9/11` + builder function ต่อฉากละหนึ่ง
   (`_build_bg0006`..`_build_bg0011`, เรียก `world_population_bg000X.build_bg000X_population`
   ที่ LANE-A ขุด identity/population ไว้ก่อนแล้ว — cross-check แล้วโครงสร้างตรงกับ bg0008 เป๊ะ) +
   ลบ 4 รายการ (scene 6,7,9,11) ออกจาก `ACKNOWLEDGED_WITHOUT_COMPOSER` (strike-through ตามธรรมเนียม
   ไฟล์ ไม่ลบทิ้งเงียบ)
9. **เทสใหม่ 4 ไฟล์** `tests/test_field_mob_tables_bg000{6,7,9}.py` + `_bg0011.py` มิเรอร์
   `test_field_mob_tables_bg0008.py` (shape เดียวกัน: ascii/header, census, scene-reachable,
   AI-register-opens, "left other scenes alone", death-ruling+stray-row) — bg0009 มีเทสเพิ่ม
   `test_the_drops_unmined_rows_still_ship` ตรวจว่า 56/57 ยังตายได้ปกติ ไม่ถูกกรอง
10. **ต่อเทสที่มีอยู่** ให้ครอบ 4 ฉากใหม่ (นับจริง ไม่ใช่แค่ import):
    `test_mob_death_wired_widening.py` (ปักเวลาใบใหม่ 4 ใบ), `test_field_mobs.py` (คอลลิชัน
    cross-scene 17→**38 pairs** วัดจริงจาก `cross_scene_identity_collisions()`, เพิ่มเช็คว่าไม่มี
    pair ไหน template ซ้ำกัน), `test_mob_scene_registration_contract.py` (เพิ่ม
    `_POPULATION_MODULE_BY_SCENE` 4 แถว — ไม่งั้น `setUpClass` assert ล้มทันที),
    `test_mob_stat_fabrication_guard.py` (เพิ่ม 4 ชื่อไฟล์ใน `LANE_B_MODULES`),
    `test_gm_identity_registry_census.py` (checked count 7→11), `test_mob_ai_control.py`
    (AI_WANDER id ใหม่ 10 จาก scene 7), `test_mob_combat_bg0015_gates.py` (live scenes set,
    composer_scene_ids tuple, collision set — เหมือน `test_field_mobs.py`)
11. **แก้เทสข้ามสาย 2 จุดที่ตัวอย่าง "ฉากที่ยังไม่ mine" ของ LANE-A ล้าสมัยเพราะรอบนี้ mine
    ฉาก 6/9 จริงแล้ว** (ป้าย `[CROSS-LANE EDIT BY LANE-B - LANE-A MAY REVERT OR REPLACE]`
    ตามธรรมเนียมไฟล์เดิม ไม่ใช่กฎใหม่ที่คิดเอง):
    - `tests/test_mob_scene_recompose.py::test_a_scene_with_no_composer_is_a_named_answer`
      ใช้ scene 9 เป็นตัวอย่าง "ไม่มี composer" — ย้ายไป **scene 10 (bg0010)** แทน เพราะยังอยู่ใน
      `ACKNOWLEDGED_WITHOUT_COMPOSER` จริง (และเป็นฉากเดียวกับที่ใบ STATIC รอบนี้ค้างอยู่พอดี)
    - `tests/test_lane_a_scene_census.py` สองเทสใช้ `OCEAN_WALLED_CITY` (scene 6, ค่าคงที่ของ
      LANE-A เอง) เป็นตัวอย่าง "ฉากที่ LANE-B ยังไม่ mine" — ย้ายไปใช้ค่าคงที่ `DEEP_SEA_TEMPLE`
      (scene 10, มีอยู่แล้วในไฟล์) แทน — ไม่ได้แก้ค่า `OCEAN_WALLED_CITY` เอง (ยังใช้ในเทสอื่นของ
      LANE-A ที่ไม่เกี่ยวกับสถานะ mine/ไม่ mine)
12. **เพิ่ม pin ใน `docs/PYTEST_SKIP_PINS.json` ในคอมมิตเดียวกับเทสใหม่** (ไม่ใช่คอมมิตแก้ทีหลัง
    แบบรอบ `oabhhe`) — **ซ้อมจริงด้วย `git worktree add --detach`** ไปที่ `/tmp` (ไม่มี
    `pf_bridge` เป็น sibling): รันเทส 5 ไฟล์ฉากใหม่ (รวม bg0008) ใน worktree นั้น ได้
    `32 passed, 5 skipped` — skip ตรงกับ `[precondition:bridge_gamedata]` ทุกไฟล์ พอดี 1 ต่อฉาก
    ตาม pin ที่เติม ลบ worktree ทิ้งเรียบร้อยหลังตรวจ
13. รัน `git merge origin/main` (clean merge, no conflict — LANE-DB's `#902` แตะแค่
    `persistence_hp_pair_audit.py` คนละไฟล์) แล้วรันชุดเต็ม `pytest tests/` **ครั้งแรก** เจอ
    **11 failed** — ทุกตัวเป็นผลตรงจากการลงทะเบียน 4 ฉากนี้เอง (ไม่ใช่ของเก่า) วัดแล้วทีละตัวและ
    แก้เป็นคอมมิตที่สอง (`428cd4ab`):
    - digest pin `field_mob_ai_tables.py` ใน `test_field_mob_tables_bg0004.py` (union ขยายรอบ
      สอง) — recompute แล้ว
    - `test_field_mob_tables_bg0005.py`: `composer_scene_ids` (3,4,5,8,14)→(3,4,5,6,7,8,9,11,14)
      เปลี่ยนชื่อเทสจาก "five" เป็น "nine" ตามธรรมเนียมไฟล์
    - `test_mob_death_persistence.py`: ตัวอย่าง "ฉากไม่มี roster" เดิมใช้ `"Bg0006"` (ตัวใหญ่) —
      กลายเป็น wrong-spelling ของฉากที่ mine แล้ว (`bg0006` ตัวเล็ก) ย้ายไปใช้ `"Bg0010"` แทน
    - `test_world_bg000{6,7,9,11}_identity.py` (ของ LANE-A): เทส "ยังไม่มี roster module"
      กลายเป็นเท็จ — เปลี่ยนชื่อ+กลับทิศเป็นเทสครอสเช็คกับตาราง identity ของ LANE-A เอง
      (แบบเดียวกับที่ทำกับ bg0003/4/5/8 มาก่อน) ติดป้าย `[CROSS-LANE EDIT BY LANE-B]`
    - `test_world_population_bg000{6,7,9,11}.py` (ของ LANE-A): เทส "มีแค่ 2 importer" ต้องเพิ่ม
      `mob_scene_recompose.py` เป็นตัวที่ 3 (แบบเดียวกับ bg0005/bg0008)
    รันเทสเฉพาะ 11 ไฟล์ที่แก้ผ่านหมด (`225 passed, 1444 subtests`) แล้วรันชุดเต็มอีกครั้ง
    (คอมมิตที่สอง): **12057 passed, 361 skipped, 24981 subtests passed, 0 failed** (585.88s,
    exit 0) — เขียวสนิท
14. `python3 tools_bridge/pf_gate_preflight.py --repo <path>` จาก pf_bridge (รันซ้ำหลัง full
    suite เขียว): **PASS** ทุกข้อ (cp874 / skips / mainmerge / census / bridgesize /
    scoreboard-manual)

## ตัวเลขที่วัดได้
- roster ที่ mine จริง: Bg0006 = 2 hostile/2 templates · Bg0007 = 9 hostile/7 templates ·
  Bg0009 = 5 hostile/5 templates · Bg0011 = 10 hostile/5 templates (รวม 26 placements/19
  templates ต่างกัน ไม่รวมนับซ้ำ)
- ไฟล์ที่แตะทั้งหมด (pirate-force-server, นับจาก `git diff --stat` ระหว่าง `2841f3cc` (จุด
  merge origin/main) ถึง `428cd4ab` (คอมมิตสุดท้ายของรอบ)): **34 ไฟล์ไม่ซ้ำกัน** (8 ไฟล์ใหม่: 4
  `field_mob_tables_bg000{6,7,9,11}.py` + 4 `test_field_mob_tables_bg000{6,7,9,11}.py`, ที่
  เหลือแก้), 2722 บรรทัดเพิ่ม / 89 บรรทัดลบ
- เทสรอบสุดท้าย (หลัง merge origin/main + แก้ 11 pin ที่ล้า): **12057 passed, 361 skipped,
  24981 subtests passed, 0 failed**, exit code 0
- `pf_gate_preflight.py`: PASS ทั้ง 6 หัวข้อ (cp874, skips, mainmerge, census, bridgesize,
  scoreboard-manual)

## ยังไม่ได้พิสูจน์ / รอ COO
- [สมมติของสาย B - รอ COO ยืนยัน] ชื่อใบ ruling ที่ตั้งเอง (`widen-death-scope-bg000X-N-
  templates`) เป็นการตีความรูปแบบจากใบ `0548`/`0748` ตรง ๆ — ถ้า COO ต้องการชื่ออื่นแก้ได้ในรอบ
  เดียว (แค่ 8 จุดที่อ้างชื่อนี้: `WIDENING_RULINGS`/`WIDENING_RULING_SCENES` × 4 ฉาก +
  `test_mob_death_wired_widening.py`)
- gate ของ Windows ยังไม่รันจริงบน PR นี้ตอนปิดรอบ (แค่ `pf_gate_preflight.py` local + full pytest
  local เขียว) — รอบหน้าต้องเช็คผล gate จริงก่อนเชื่อว่าผ่าน (บทเรียนจากรอบ `oabhhe`/`#895`)
- `pirate-force-server` PR เปิดแล้ว: **`#907`** (ไม่ draft มี `PF-AUTOMERGE: v4` ยืนยันด้วย GET แล้ว)
- **`ADVERSARY_PENDING #907`** — สั่ง `pf-adversary` ต้นรอบ (ก่อน push) ตรวจ diff เต็มของ 5 คอมมิต
  ผลยังไม่คืนตอนปลดล็อกรอบนี้ ตามกฎ "ผลยังไม่คืนตอน push ⇒ push ตามเดิม ห้ามถือล็อกรอ" — **รอบถัดไป
  ของ LANE-B ต้องหยิบผลนี้เป็นงานแรกก่อน claim งานใหม่ใด ๆ**
- **ผลคืนแล้วหลังปลดล็อก (บันทึกตามกฎ ไม่แก้โค้ดในรอบนี้)**:
  1. **ยืนยัน** ไฟล์รอบนี้ขาดบรรทัด `TWO_SESSIONS_SAME_SCENE:` จริง (ละเมิด `PROCESS_GATES.md` §7 —
     เพิ่มแล้วข้างบนในรอบนี้ผ่านการแก้ไฟล์รอบเอง ซึ่งกฎอนุญาตเป็นข้อยกเว้นเฉพาะกรณีนี้)
  2. **ช่องโหว่จริงที่มีอยู่ก่อนรอบนี้** (ไม่ใช่ของรอบนี้ทำเสีย แต่รอบนี้ขยายพื้นผิวที่โดนจาก 6→10
     ฉาก): `DeathRegister` เป็นต่อ-connection ไม่ใช่ต่อ-ฉาก — ดูรายละเอียดในหัวข้อ
     `TWO_SESSIONS_SAME_SCENE` ข้างบน
  3. ตรวจแล้ว **ไม่พบข้อบกพร่อง** ในหกหัวข้ออื่นที่ขอให้ตรวจเข้ม (scene-tie binding, composer
     ถูกเรียกจริง, bg0009 zero-drop ไม่ถูก withhold ผิด, AI row coverage, skip pins ตรง,
     ห้ามแตะไฟล์ต้องห้าม) — ยืนยันด้วยมิวแทนต์จริงทุกข้อ (รายละเอียดเต็มอยู่ในผลของ agent เอง
     ถ้าต้องการอ้างอิงซ้ำ ให้รัน pf-adversary ใหม่ในรอบหน้า เพราะผลรอบนี้ไม่ได้ถูก commit เป็นไฟล์)

## รอบหน้าทำอะไร
1. **🔴 เปิดใบ ASK-COO เรื่อง `DeathRegister` ต่อ-connection ไม่ใช่ต่อ-ฉาก ก่อนงานใหม่ใด ๆ**
   (pf-adversary ยืนยันด้วยการอ่าน `runtime.py:1404` + nonclaim ที่มีอยู่แล้วใน
   `scenarios/combat_death_001.json:104` — ไม่ใช่บั๊กที่รอบนี้ทำเสีย แต่รอบนี้ขยายพื้นผิว 6→10 ฉาก
   โดยไม่เคยตอบคำถามนี้) คำถาม: สองเซสชันในฉากเดียวกันฆ่ามอนตัวเดียวกันพร้อมกัน ผู้เล่นคนที่สองยังเห็น
   มันมีชีวิตอยู่ไหม/ฆ่าซ้ำได้ไหม — เสนอทางแก้ (เช่น ผูก `DeathRegister` เข้ากับ world registry ของ
   LANE-A แทนที่จะเป็นต่อ connection) แล้วเดินต่อ ไม่รอคำตอบ
2. หยิบรายละเอียดเต็มของผล `pf-adversary` (6 หัวข้ออื่นผ่านหมด — ดูสรุปในหัวข้อ "ยังไม่ได้พิสูจน์ /
   รอ COO" ข้างบน) ถ้าต้องการหลักฐานเต็มให้รัน adversary ใหม่ (ผลรอบนี้ไม่ได้ commit เป็นไฟล์)
3. เช็คผล gate จริงของ `#907` (ไม่ใช่แค่ preflight local) ด้วย `mcp__github__get_job_logs` ถ้าแดง
4. เช็คว่า COO ตอบเรื่องชื่อใบ ruling หรือชื่อ casing `bg0006` (lowercase) หรือไม่ — ถ้าใช่แก้ตาม
5. เช็คว่า `#907` merge แล้วหรือยังด้วย `git merge-base --is-ancestor` ก่อนเขียนว่า "อยู่บน main"
6. รอคำตอบใบ STATIC bg0010 (`20260906_0903_LANE-B-STATIC-TICKET-bg0010-unresolved-template-id.md`)
   จาก chief — ถ้าตอบว่า "ข้ามแถวแล้วเดินต่อ" ให้ทำ PR แยกแก้ `pf_mine_scene_mob_roster.py`
   ตามที่ COO อนุญาตไว้ (ข้อ 3 ของใบ `0748`)

## งานสำรอง (ทำเมื่องานหลักติด)
1. เปิด `docs/PROMOTION_BACKLOG.md` (server repo, `#894` chief) ปลดแฟล็ก scenario ในเขต LANE-B
   ที่พิสูจน์แล้วแต่ยัง `production_allowed = false` มา 1 ตัว + เทส + ใบ GT
2. ใบ RE/STATIC ของ COMBAT ที่ตอบได้จาก factpack/gamedata commit แล้ว (grep `gamedata/` +
   `external/` ก่อนออกใบใหม่)
3. technical debt ที่ pf-adversary เคยชี้ในไฟล์รอบเก่าของสาย B (ดู `#814`/r6isy5b เป็นตัวอย่าง)

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรบนจอวันนี้ (P-2/ใบ GT ตีมอนยังปิดเหมือนเดิมตาม NOW.md) แต่
โค้ดที่ทำให้มอน 26 ตัว (2+9+5+10) ใน 4 ฉากใหม่ (Bg0006/Bg0007/Bg0009/Bg0011) ตายได้จริงแบบเดียวกับ
Bg0008 ถึง PR แล้ว รอ merge/รอ P-2 ปิดก่อนถึงมือผู้เล่น | `field_mob_tables_bg000{6,7,9,11}.py` +
`mob_death.WIDENING_RULINGS` 4 รายการใหม่ + เทส 4 ไฟล์ผ่านหมด + full suite ผ่าน (ดูตัวเลขในหัวข้อ
"ตัวเลขที่วัดได้")
