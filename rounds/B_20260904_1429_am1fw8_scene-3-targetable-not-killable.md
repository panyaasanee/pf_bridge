[LANE-B รอบ `am1fw8` · เริ่ม 2026-09-04T13:31+07:00 · เขียนไฟล์นี้ 2026-09-04T14:29+07:00]

# ฉาก 3 (Bg0003) เป็นฉากรบที่ห้า — และเพราะตะเข็บเปิดกลางรอบ มอน 12 ตัวกลายเป็น "เป้าที่คลิกได้จริง"

ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน: **ในฉาก 3 มีมอนศัตรู 12 ตัวที่ไคลเอนต์รู้จักชื่อ และประตู RE-157
รับทั้ง 12 ตัวเป็นเป้าได้จริง** เมื่อวานคลิกตรงนั้นได้ `mob_combat_target_not_announced_no_reply`
ไม่มีไบต์ออกเลย · **แต่ยังฆ่าไม่ได้** (ไม่มีใบอนุญาตฆ่าของ COO สำหรับฉากนี้) **และยังไม่ดรอปอะไร**
(ตาราง drop ของฉากนี้ไม่เคยถูกขุด) — สองข้อหลังพิสูจน์ด้วยเทส ไม่ใช่คำกล่าวอ้าง

## รอบนี้ขยับ NOW ข้อไหน
`NOW.md` M4 · LANE-B ข้อ (2): *"ฉาก 3/4/5 มี `placements.tsv` แล้ว = คิว B ฉากละใบ"* — ฉาก 5 จบไปแล้ว
(`#727`/`#730`) **รอบนี้ = ฉาก 3** เหลือฉาก 4 เป็นใบสุดท้ายของข้อนี้
ข้อที่ไม่ขยับและเพราะอะไร: Door B caller ยังไม่เสียบ (`MOB_HIT_FRAME_CONFIRMED=None` ต้องมี GT บนจอ
ซึ่ง NOW.md ห้ามเปิดจน P-2 ปิด) · P-2 เป็นของ LANE-GM ไม่ใช่ของสายนี้

## ตะเข็บเปิดกลางรอบ — เรื่องใหญ่ที่สุดของรอบนี้
รอบนี้เริ่มต้นด้วยแผน "ส่ง roster ไปนอนหลังตะเข็บที่ยังปิด" แต่ระหว่างรอบ **chief รอบ `9vec2s`
(`#734`) ตอบ CORE-REQUEST `20260904_1134` ของสายนี้แล้ว**: สาขา arrival แบบ lane-composed ใน
`runtime.py` เลิกปั๊ม membership ว่าง หันไปอ่าน `SceneCensusResult.actor_identities` ซึ่ง
`lane_a_scene_census` เติมจาก `field_mobs.roster_for_scene_id` — **ตัวอ่านตัวเดียวกับที่ PR รอบนี้
เปลี่ยนคำตอบของมัน** ⇒ การลงทะเบียน roster ฉาก 3 คือสิ่งเดียวกับการทำให้มอน 12 ตัวถูกประกาศ

วัดแล้ว (ไม่ใช่อ่านโค้ดเอา) ผ่าน helper ของสาย A เองกับ builder ตัวจริง:
```
scene3 announced identities: 0x201c 0x201d 0x201e 0x2022 0x2023 0x2024
                             0x2028 0x2029 0x202a 0x202b 0x203b 0x2046   (12/12)
admits 0x201C = True · admits 0x2046 = True · admits stray 0x2099 = False
admits 0x2046 ภายใต้ scene_id=5 = False   <- membership scope ด้วย scene ไม่ใช่แค่ identity
```
⇒ เทสสองใบที่เคยเขียนว่า "ตะเข็บปิด" ถูก **เปลี่ยนทิศตามความจริงใหม่** ไม่ใช่ลบทิ้ง:
`Bg0003NotFightableYetTests` → `Bg0003IsTargetableButNotKillableTests` และการ์ดนับฉากใน
`test_field_mob_tables_bg0005.py` ถูกเปลี่ยนชื่อออกจากคำว่า "behind that shut seam"

## ของที่ลงในรอบนี้ (server PR `#738`)
1. `tools/pf_mine_scene_mob_roster.py` — `resolve_placement_path` · โคลนสะกดฉาก 3 ว่า
   `scene/Bg0003/bg0003.placements.tsv` (ไดเรกทอรีตัวใหญ่ ไฟล์ตัวเล็ก) เครื่องมือเดิมสมมติ
   `<S>/<S>.placements.tsv` ซึ่งถูกกับทุกฉากที่เคยขุด **แต่บนลินุกซ์ฉาก 3 ขุดไม่ได้ทั้งสองสะกด**
   ตอนนี้แก้ทีละครึ่งแบบไม่สนตัวพิมพ์ และ **ปฏิเสธ** ถ้าเจอสองตัวที่ต่างกันแค่ตัวพิมพ์ (ไม่เดา)
2. `field_mob_tables_bg0003.py` (generated) — 12 แถว 7 template · predicate ทั้งสี่ตรงกันที่ 12/12
3. `field_mob_ai_tables.py` ขุดใหม่รวมฉาก 3 · **reproduce การปฏิเสธก่อน** (`placement 27 points at
   AI_COMBAT 140`) ไม่ได้อนุมานจากฉากก่อน
4. `field_mobs.py` ลงทะเบียน · `mob_scene_recompose.py` `COMPOSER_BG0003` + builder ·
   entry ฉาก 3 ใน `ACKNOWLEDGED_WITHOUT_COMPOSER` **ขีดฆ่า ไม่ลบ**
5. `mob_hit_frame.py` — รับรั้วที่สามของ LANE-GM (ใบ `20260904_1226`) ที่จุดเรียก
   `make_update_attr_frame` (คนละเรื่องกับฉาก 3 · เป็นการบริโภคใบนั้น)
6. เทส: การ์ดของฉาก 3 · การ์ด collision 3 คู่ → 7 คู่ · การ์ดนับฉาก `(5,14)` → `(3,5,14)` ·
   พินอีกห้าใบที่การลงทะเบียนฉาก 3 ถูกสร้างมาให้ขยับ · `docs/PYTEST_SKIP_PINS.json` +4

**17 ไฟล์** (ไม่ใช่ 3 อย่างที่แผนต้นรอบประกาศ — pf-adversary จับข้อนี้ จึงประกาศตัวเลขจริงใน PR body)
ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`

## ใบที่บริโภครอบนี้
1. `20260904_1226_LANE-GM-TO-LANE-B-make_update_attr_frame-has-an-optional-third-fence-now.md`
   — **รับ (ACCEPT)** เสียบ `character_id=` + `hooks=` ที่ `mob_hit_frame.py` · GM เขียนเองว่ามันจะเป็น
   no-op เพราะค่ามาจาก `live_full_block_values` ที่รันรั้วต้นทางแล้ว — รับเพราะ "ปลอดภัย" ข้อนี้เป็น
   สมบัติของ **เส้นทางประกอบ** ไม่ใช่ของอาร์กิวเมนต์ และ Door B เขียนทับ hp_current ระหว่างสองการเรียก
   `tests/test_lane_b_mob_ai_tick.py` = 61 passed ทั้งก่อนและหลัง
2. `20260904_1134_LANE-B-CORE-REQUEST-lane-composed-census-must-hand-back-its-actor-identities.md`
   (ใบของสายนี้เอง) — **ตอบแล้วโดย chief `#734`** บริโภคในรอบนี้ = re-point เทสสองใบ + วัดผลจริง

## pf-adversary (สั่งต้นรอบพร้อมเริ่มงาน ตาม `COO 0903_2345`) — ผลคืนกลางรอบ แก้ครบในรอบเดียวกัน
- **มิวแทนต์รอด**: แก้ `max_hp` หรือ `x` ในตาราง generated แล้ว **ชุดเทสทั้งชุดยังเขียว** เพราะตัวจับ
  ตัวเดียว (regenerate byte-for-byte) ต้องมีโคลนสะพาน = **SKIP บนเกต** ⇒ เทส crosswalk กับสาย A
  ตอนนี้เทียบ **ทุกคอลัมน์ที่ทั้งสองตารางมี** (template · name · outfit · level · rank · max_hp · x · y · z)
  มิวแทนต์ทั้งสามตายโดยไม่ต้องมีสะพาน · `speed_walk` กับคอลัมน์ drop **ยังไม่มีแหล่งที่สอง** บอกตรง ๆ
  ว่าเป็น bridge-only ไม่แกล้งทำเป็นมี
- **พินที่เขียวทั้งที่ผิด**: เทส AI links เดินทูเปิลชื่อฉากพิมพ์มือที่ตกยุคไปหนึ่งฉาก ⇒ ลิงก์ของ Bg0015
  ทั้ง 12 ตัวถูกนับเป็น "extras" ต่อมาหลายรอบ · ตอนนี้อ่าน `field_mobs.live_scenes()` และประโยคที่ว่า
  Bg0015 ไม่ได้ลงทะเบียน **ขีดฆ่าแล้ว** ⇒ ฉาก 4/6 รอบหน้าไม่ต้องมาแก้ไฟล์นี้อีก
- **collision walk เดินแค่ขาเดียวจากห้าขา**: คู่ใหม่โผล่ทีเดียวสี่ (0x201C 0x201E 0x203B 0x2046) ·
  ตอนนี้ขา ledger กับ loot **วัดแล้ว**: ledger ของฉาก 5 ครอบ identity ของฉาก 3 ได้ **หนึ่งใน 12 ตัว**
  (คือคู่ชนพอดี = รูปทรงที่ระบบนับ coverage จะหลุด) และ admission ยังปฏิเสธเป็น `other_scene`
  `ledger=None`
- **ประตูปิดชั้นที่สามที่ยังไม่มีใครตั้งชื่อ**: `DROPS_NORMAL` 2701002 ของฉาก 3 ไม่อยู่ใน
  `field_drop_tables` ⇒ loot ปฏิเสธ `unknown_drop_set` ก่อนออกคีย์ · ปักเป็นเทส เพื่อไม่ให้วันที่
  ประตูอื่นเปิดแล้วกลายเป็น "ฆ่าได้แต่ไม่ได้ของ" โดยไม่มีใครรู้ว่าทำไม
- คำถามดีไซน์ที่ adversary ทิ้งไว้ ("เกณฑ์อะไรบอกให้หยุดผลิตฉากที่ 6 แล้วไปเปิดประตูแทน") →
  จดหมาย `1432` ถึง COO

## เทส
- ระหว่างทาง: เฉพาะไฟล์ที่แตะ (`test_field_mob_tables_bg0003` `test_field_mobs`
  `test_mob_scene_recompose` `test_mob_ai_control` `test_mob_combat_bg0015_gates`
  `test_gm_identity_registry_census` `test_world_population_bg0003` `test_lane_b_mob_ai_tick`)
- **ชุดเต็มรันสองครั้ง และนี่คือเหตุผลที่ต้องเขียน**: ครั้งแรก (`0272d8d`+งาน) เจอพินแดง 8 ตัวที่
  การลงทะเบียนฉากใหม่ถูกสร้างมาให้ขยับ → แก้ → ครั้งที่สองบนคอมมิตสุดท้ายจริง หลังแก้ตาม
  pf-adversary และหลัง merge main แล้ว
- **ครั้งสุดท้าย: worktree แยก ไม่มี `pf_bridge` ข้าง ๆ + ชุด exclude แบบเกต (49 โมดูล)
  = 8,782 passed · 93 skipped · 16,801 subtests · exit 0** · ขั้น `seam` ของเกต (ไฟล์ที่เกตรันแยก)
  = 24 passed · `pf_pytest_precondition_census.py` จากใน worktree = ไม่มี PIN DRIFT ของพินที่รอบนี้แตะ
  (เหลือรายการเดียวคือ `test_foundation_legacy_seam.py` ซึ่งเป็นของการซ้อมเอง: เกตรันไฟล์นั้นเป็นขั้น
  แยก ไม่ได้ซ่อนมัน — รันแยกแล้วเขียว)

## ยังไม่ได้พิสูจน์ (รอมนุษย์หน้าจอ)
- มอนฉาก 3 ขึ้นจอจริงและคลิกติดจริง — โค้ดพร้อม แต่ NOW.md ห้ามเปิดใบ GT ตีมอนจน P-2 ปิด
- ชื่อ/สีของมอนฉาก 3 บนจอ (P-2 เป็นของ LANE-GM)

## CORE-REQUEST
none (ใบ `1134` ปิดแล้วโดย `#734`)

## เปิดใบให้สาย C
none

## สถานะเมื่อจบรอบ
push แล้ว รอ merge PR `#738` (pirate-force-server: เปิดแล้ว รอ gate) · claim PR `#1140` (pf_bridge)

-- LANE-B รอบ `am1fw8`
