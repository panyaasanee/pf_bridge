[LANE-B รอบ `k4wm9t` · เริ่ม 2026-09-04T12:05+07:00 · เขียนไฟล์นี้ 2026-09-04T12:17+07:00]

# หกแถวฉาก 5 (bg0005 Evil Port) ได้ใบอนุญาตฆ่าแล้ว + รับสองจุดที่ LANE-GM แตะแทน

ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน: **ยังไม่เห็นอะไรเปลี่ยนบนจอ** — Door B caller ยังไม่เสียบ
(`MOB_HIT_FRAME_CONFIRMED=None` เดิม) และ NOW.md ยังห้ามเปิดใบ GT ตีมอนฉาก 5 จนกว่า P-2 จะปิด
สิ่งที่เปลี่ยนคือ "พร้อมให้ทดสอบ": วันนี้ถ้า caller เสียบและ P-2 ปิด การตีหกมอนฉาก 5 (Red Devil,
Ned apes, Hard Blade Eagle, Black Jack, Jet cat thieves No.5/No.6) จนศูนย์ HP จะได้เฟรมตาย+ศพ
จริง ไม่ใช่ "ค้างที่ 0 HP เงียบ ๆ" เหมือนเมื่อวาน

## ใบที่บริโภครอบนี้ (สองใบ ตามคำสั่ง)

### 1. `20260904_1148_COO-DECISION-lane-b-widen-death-scope-bg0005-six-templates-approved.md`
ตัดสิน: อนุมัติใบอนุญาตฆ่า 6 แถว `MOBS.n_ID` ในฉาก 5 — 148 Red Devil · 150 Ned apes ·
144 Hard Blade Eagle · 146 Black Jack · 523 Jet cat thieves No.5 · 525 Jet cat thieves No.6

**ทำ**: เดินตามแบบแผน `COO 20260827_1350` (bg0001 full roster) เป๊ะ — เพิ่ม entry ใน
`mob_death.WIDENING_RULINGS` คีย์ชื่อ `"COO-DECISION 2026-09-04T11:48+07:00
widen-death-scope-bg0005-six-templates"` (คัดลอกจากชื่อไฟล์จดหมายตรงตัว ไม่เอาจากใบอื่น) ค่า
= `frozenset({148, 150, 144, 146, 523, 525})` และเพิ่ม entry คู่กันใน
`mob_death.WIDENING_RULING_SCENES` ผูกกับ `field_mob_tables_bg0005.SCENE` (`"bg0005"`) —
กันไม่ให้มอนสเตอร์สเกลอื่นที่บังเอิญใช้ template id ซ้ำ (bg0002/bg0015) หลุดผ่านใบนี้ไปได้

พลิกเทส `test_no_shipped_template_has_a_death_ruling_yet_and_that_refuses`
(`tests/test_field_mob_tables_bg0005.py`) เป็น
`test_the_six_shipped_templates_now_have_a_death_ruling_a_stray_row_still_refuses`:
ครึ่งแรก derive จาก `field_mob_tables_bg0005.HOSTILE_PLACEMENTS` เอง (ไม่ hard-code ซ้ำ) ว่า
ทั้งหกแถวตอบ `mob_death.ruling_for(mob)` เป็นชื่อใบนี้ · ครึ่งหลัง (ฉาก 5 แถวอื่นถ้ามียังปฏิเสธ)
พิสูจน์ด้วย stand-in ที่สร้างเอง (template 916 ซึ่งมีใบของตัวเองแต่ผูกฉาก bg0001 เท่านั้น สแตมป์
`scene="bg0005"`) เพราะฉาก 5 ไม่มีแถวชิปจริงนอกหกแถวนี้เลย (`TOWN_TARGET_PLACEMENTS` และ
`LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION` ว่างทั้งคู่) — เทคนิคเดียวกับที่
`mob_death.rulings_covering`'s docstring ใช้พิสูจน์แกน scene ที่ไม่มีแถวชิปจริงทดสอบให้

**ผลข้างเคียงที่พบและแก้ในรอบเดียวกัน** (ไม่ใช่ของนอกสโคป — เป็นเทสสองใบที่พังเพราะใบอนุญาตนี้ทำให้
ข้อสมมติของมันเป็นเท็จ):
- `tests/test_mob_death.py::test_two_real_colliding_mobs_in_different_scenes_die_independently`
  — เทสนี้เขียนคำสั่งของตัวเองไว้แล้วในคอมเมนต์รอบ jqeo2m: "the day a ruling lands that makes a
  real pair usable, this fails and the next round builds the card on it" ใบอนุญาตวันนี้ทำให้คู่ชน
  จริง 0x203C (Bg0002 template 34 กับ bg0005 template 148 ที่ placement 59 เดียวกัน) มีใบทั้งสองฝั่ง
  แล้ว จึงสร้างการ์ดใหม่บนคู่จริงนี้แทนของสร้างมือ (`field_mobs.load_roster` ทั้งสองฝั่ง ไม่ใช่
  `FieldMob(...)` มือ) ยังคงตรวจ "ตายอิสระกันคนละฉาก" เหมือนเดิมทุกข้อ
- `tests/test_mob_death_wired_widening.py::test_every_registered_letter_can_be_ordered_and_names_its_own_clock`
  — เพิ่ม timestamp ใบใหม่ (`202609041148`) ลงในดิกต์ที่พินทุกใบที่ลงทะเบียน

**ไม่ทำ**: ไม่อนุมัติเกินหกแถว · ไม่แตะฉาก 3/4 · ไม่เปิดใบ `GAME_TEST_QUEUE.md` (P-2 ยังไม่ปิด
ตาม NOW.md — ของพร้อมให้ทดสอบแล้ว บันทึกไว้ตรงนี้แทน)

**หนี้ "แคช live" (`0847`)**: ตรวจแล้ว **จบแล้วรอบก่อน (09:31, PR #721, merged เป็น `#722`
ตาม NOW.md)** — `mob_hit_frame.py`'s `compose_player_hit_frame` ประกอบเฟรมจาก
`gm/attr_wire.live_full_block_values` ล้วน ๆ `RawBlockCache` เหลือหน้าที่อ่าน shape +
`record_sent` เท่านั้น ไม่มีค่าใดจากแคชรั่วเข้าเฟรม (grep คอมเมนต์ในไฟล์บรรทัด 44-134, 526-621
ยืนยันตรง) จึงมาก่อน #728-gate work ตามลำดับของ COO และ**ทำไปแล้ว ไม่ต้องทำซ้ำ**

### 2. `20260904_1023_LANE-GM-TO-LANE-B-door-b-needs-a-third-read-point-two-lines-landed-out-of-zone.md`
LANE-GM แตะสองจุดนอกเขตแทน B: (a) `mob_hit_frame.py` ส่งผ่าน read point ที่สาม
`attr_wire.CURRENT_SCENE_READ_POINT` เข้า shim รูปเดียวกับ `LOGIN_BYTES_READ_POINT` (b)
`tests/test_lane_b_mob_ai_tick.py`'s `_compose(..., scene_hook=None)` derive จาก `login_hook`
เอง

**ตรวจแล้ว**: `grep -n "CURRENT_SCENE_READ_POINT" src/pirateforce_foundation/mob_hit_frame.py`
เจอทั้งสามจุด (comment อธิบาย + read + setattr) `tests/test_lane_b_mob_ai_tick.py` มี
`scene_hook=None` derive ตามที่บอก · รัน `pytest tests/test_lane_b_mob_ai_tick.py` = **61 passed,
64 subtests passed** — **รับ (ACCEPT) ทั้งสองจุด ไม่ถอนอะไร**

## ไฟล์ที่แตะ (pirate-force-server, สาขา `claude/magical-hawking-mxxqi7`)
1. `src/pirateforce_foundation/mob_death.py` — import `field_mob_tables_bg0005` +
   entry ใหม่ใน `WIDENING_RULINGS`/`WIDENING_RULING_SCENES`
2. `tests/test_field_mob_tables_bg0005.py` — พลิกเทสตามข้อ 1
3. `tests/test_mob_death.py` — สร้างการ์ดคู่ชนจริงแทนของสร้างมือ (ตามคำสั่งในเทสเอง)
4. `tests/test_mob_death_wired_widening.py` — เพิ่ม timestamp ใบใหม่ในดิกต์พิน

รวม **4 ไฟล์แตะ** (ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
`scenarios/world_*.json`) · ยืนยันสองจุดของ LANE-GM มีอยู่แล้ว (0 ไฟล์เพิ่มจากฝั่งนี้)

## เทสที่รันระหว่างทาง (เฉพาะไฟล์ที่แตะ + ไฟล์ที่พังเพราะมัน)
- `tests/test_field_mob_tables_bg0005.py` — 16 passed
- `tests/test_mob_death.py` + `test_mob_death_wired_widening.py` +
  `test_mob_death_bg0015_ruling_proposal.py` — 156 passed, 374 subtests passed
- `tests/test_field_mob_tables_bg0002.py` `test_field_mobs.py`
  `test_field_mobs_single_scene_guard.py` `test_mob_combat_dispatch.py`
  `test_mob_diag_multi_object.py` `test_mob_loot.py` `test_mob_scene_recompose.py`
  `test_mob_stat_fabrication_guard.py` `test_scene_scoped_combat_wiring.py` — 358 passed,
  259 subtests passed
- `tests/test_mob_combat_bg0015_gates.py` `test_world_scene_marker.py`
  `test_mob_stat_fabrication_guard.py` — 69 passed, 38 subtests passed
- `tests/test_lane_b_mob_ai_tick.py` (ยืนยันจุดของ LANE-GM) — 61 passed, 64 subtests passed
- `tests/test_tree_is_cp874_safe.py` `test_gm_source_is_cp874_safe.py` — 8 passed,
  621 subtests passed

## pf-adversary
ไม่มี Task/Agent tool ให้เรียก `pf-adversary` เป็น subagent ตรง ๆ ในรอบนี้ — ทำเอง (ตาม
`.claude/agents/pf-adversary.md` checklist) อ่านดิฟฟ์ของตัวเองแบบปฏิปักษ์:
- **เช็ค "stale pin"**: `WIDENING_RULINGS[ruling_name]` ในเทสไม่ hard-code รายการหกไอดีซ้ำ —
  derive จาก `field_mob_tables_bg0005.HOSTILE_PLACEMENTS` ตรง ๆ (ดูโค้ด)
- **เช็ค "green because it never got there"**: รันจริงยืนยันว่า `mob_death.ruling_for(stray)`
  โยน `MobDeathContractError` จริง (reason `target_outside_the_sanctioned_scope`) ไม่ใช่ error
  คนละคลาสหลุดผ่าน `except` ที่ `runtime.py:5239` จับ
- **เช็ค tie-break ระหว่างใบที่ขนาดเท่ากัน**: bg0015 (6 templates) กับ bg0005 (6 templates) ใหม่
  ไม่มี template id ซ้ำกันเลย (148/150/144/146/523/525 ปะทะ 343/345/348/350/353/355) จึงไม่มีวัน
  ชนกันใน `ruling_for`'s sort — ตรวจด้วยโค้ดจริง ไม่ใช่อนุมาน
  ตรงกับที่ NOW.md เตือนไว้แล้ว ("คู่ชน `0x2058` ต้อง scope ด้วย scene_id") — คู่นั้น (Carlos/
  Bg0002 template 103) ยังไม่มีทั้งสองฝั่งมีใบ จึงยังไม่ต้องแตะ
- **เช็ค describe_widening_coverage() ไม่พังกับชื่อ non-ASCII**: ชื่อมอนทั้งหกเป็นอังกฤษล้วน
  cp874-encodable (ตรวจแล้วด้านบน) ไม่กระทบเทส `test_the_report_encodes_to_the_console_this_
  project_actually_has`
- **ไม่พบข้อบกพร่องใหม่ที่ยังไม่แก้** — สองจุดที่พบ (เทสคู่ชนกับเทส timestamp) แก้ในคอมมิตเดียวกัน
  แล้ว ไม่ใช่ ADVERSARY_PENDING

## ชุดเทสเต็ม (บังคับก่อน push)
`git fetch origin main` = `origin/main` อยู่ที่ `d896972` (`#728` merged) — `git merge-base
--is-ancestor origin/main HEAD` = true อยู่แล้ว (สาขานี้แตกจาก main หลัง `#728` merge) **ไม่ต้อง
merge เพิ่ม**

รันบน `git worktree` แยก ไม่มี `pf_bridge` วางข้าง ๆ (ตาม NOW.md กติกาเดียวกับรอบ jqeo2m) ด้วยชุด
exclude แบบเดียวกับเกต (`Select-String -Pattern 'GameClient|capture_v141'` = **49 โมดูล** ถูก
`--ignore`):

**`pytest tests -q -rs --ignore=... (49 ตัว)` บนคอมมิต `000a5d8`:
8691 passed, 89 skipped, 16621 subtests passed, exit=0** (299.19s) — ทุก skip เป็น precondition
เดิม (`bridge_gamedata`/`audit_head_history`/`login_req_capture`/`backups_tree`/
`bridge_attr_corpus`) ไม่มี skip ใหม่จากรอบนี้

ไม่มีการแก้ไขไฟล์หลังรันชุดเต็ม จึงไม่ต้องรันซ้ำ

## ยังไม่ได้พิสูจน์ (รอมนุษย์หน้าจอ)
- ผู้เล่นตีมอนฉาก 5 จนตายจริงบนจอ — ยังไม่มีใคร watch เพราะ (ก) Door B caller ยังไม่เสียบ
  (ข) P-2 ยังไม่ปิด NOW.md ห้ามเปิดใบ GT
- ท่าตาย/ศพของมอนฉาก 5 บนจอ (bg0001's GT-084-R2 พบว่า "ตาย" ของมอนมี effect ต่างกันตามตัว —
  body-dependent ไม่ใช่สมบัติเดียวของ actor_type 4 — ฉาก 5 ยังไม่มีใครสังเกต)

## CORE-REQUEST
none

## เปิดใบให้สาย C
none

-- LANE-B รอบ `k4wm9t`
