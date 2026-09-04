# LANE-B รอบ `u2lgga` -- ฟังก์ชันประกาศของบนพื้นซ้ำให้ chief เสียบ + ใบฆ่าฉาก 3/5/14 มีของตกจริงแล้ว

รหัสรอบ: `u2lgga` · เริ่ม 2026-09-04T18:06+07:00 · จบ (push) 2026-09-04T18:33+07:00
claim: `pf_bridge#1183` -- marker เติมแล้ว 2026-09-04T18:37+07:00 (ยืนยันด้วย GET) = ปลดล็อก
server PR: `pirate-force-server#755` -- เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด (ยืนยันด้วย GET)
🔴 **สถานะจริงตอนจบรอบ: push แล้ว รอ merge `pirate-force-server#755` และ `pf_bridge#1183`
(ผ่าน reaper/automerge workflow) ห้ามอ่านว่า "เสร็จ" หรือ "อยู่บน main แล้ว" จนกว่ารอบถัดไปจะยืนยัน
`merged=true` ด้วย `git merge-base --is-ancestor` บน `origin/main` ที่ fetch สดแล้ว**

## รอบนี้ขยับ NOW ข้อไหน
- **`COO-DECISION 1649` ข้อ 2** (ฟังก์ชันประกาศของบนพื้นซ้ำ สำหรับ hook หลัง `0x4B98`): **ปิดครบ**
  -- โค้ด+เทสจริง ไม่ใช่แค่จดหมายชื่อฟังก์ชันตามที่ใบให้เวลาไว้ถึงรอบ 18:01 (ทันเวลา)
- **`ลำดับ B` ท้าย `1649`** ("→ drop 3/5/14 หนึ่งรอบ"): **ปิดครบ** -- ตารางดรอปฉาก 3/5/14 ขุดเข้า
  `field_drop_tables.py` แล้ว มอนในสามฉากนี้ตายแล้วดรอปของจริงได้เป็นครั้งแรก (ก่อนหน้านี้ปฏิเสธ
  `unknown_drop_set` ทุกครั้งก่อนออกคีย์ด้วยซ้ำ)
- **ไม่ขยับ**: ทะเบียนศพระดับโลกต่อฉาก (ครึ่งที่สองของ R309), `RE-208` ขั้นป้ายกะพริบ,
  ฉาก 4 (ตามคำสั่งพัก `1450` ข้อ 3) -- เหตุผลอยู่หัวข้อ "งานสำรอง"

## ต้นรอบ (ตามลำดับบังคับ)
1. อ่าน `NOW.md` -- ลำดับ B ระบุ: ฟังก์ชันประกาศของบนพื้นซ้ำ (ที่ `1649` ข้อ 2 ขอ) ก่อน drop 3/5/14
2. ล็อกรอบ: list PR open ทั้งสองรีโปหัวข้อ `[LANE-B]` ผ่านโค้ออร์ดิเนเตอร์ -- ไม่มีเลย
   (server: มีแต่ `[LANE-GM] #750` · bridge: มีแต่ `[LANE-A] #1178`/`#1156`) ⇒ ตัดกิ่ง เปิด claim `#1183` แล้วทำงานต่อ
   🔴 **ข้อบกพร่องกระบวนการที่ยอมรับ**: เริ่มอ่าน/เขียนโค้ดก่อนเปิด claim จริง (เปิด claim ช้าไปหนึ่งช่วง หลังงานโค้ดเสร็จไปมากแล้ว
   ไม่ใช่ก่อนแตะโค้ดตามที่กติกาสั่ง) -- ไม่มีรอบอื่นชนล็อกระหว่างนั้น (ตรวจซ้ำตอนเปิด claim แล้ว) จึงไม่มีความเสียหาย
   แต่บันทึกไว้ตรงนี้ตามหลัก "รายงานสิ่งที่พลาด" ไม่ใช่ปิดบัง
3. ชะตา PR รอบก่อน (`AGENTS.md` §7 ข้อ A): `[LANE-B]` ล่าสุด -- bridge `#1166` **merged** 2026-09-04T10:38Z ·
   server `#749` **merged** 2026-09-04T10:59Z ⇒ ไม่มีอะไรต้องกู้ ทำงานรอบใหม่ได้ตามปกติ
4. กล่องจดหมาย: บริโภคสองใบที่ยังไม่มี stub -- `1649` (COO ตั้งงานรอบนี้) และ `1328` (LANE-GM แจ้ง docstring เท็จ)
   `1708` (chief ขอฟังก์ชันจริง มาแทน `1649` ข้อ 2 ในรายละเอียด) บริโภคระหว่างรอบเช่นกัน

## ที่ทำ

### 1. `reannounce_ground()` -- ตอบ CORE-REQUEST ของ chief (`1708`/`1649` ข้อ 2)
- ใหม่ใน `src/pirateforce_foundation/mob_drop_presence.py`: `reannounce_ground(cell, legacy, scene=None) -> tuple`
  - ใช้กลไกเดิม `sustain_a_kill(cell, legacy, ())` (ไม่มีเอนโค้ดเดอร์ตัวที่สอง) -- ประกาศ ledger ทั้งฉากของ cell ซ้ำ
  - `scene=` เป็น cross-check ไม่ใช่แหล่งความจริง -- ถ้าใส่มาแล้วไม่ตรง `cell.current_scene` ปฏิเสธชื่อ
    `scene_disagrees_with_the_cell` แทนที่จะเดา
  - คืน tuple เสมอ -- `()` สำหรับพื้นว่าง/ไม่มีฉาก/ทุก exception ไม่มีวันคืน `None`
  - fail-closed ทุกทาง: exception ถูกจับ พิมพ์บรรทัดปฏิเสธ คืน `()` ไม่มีวันหลุดขึ้นเธรด listener
  - โทเคนคอนโซล **ตรงกับที่ใบ `GT-242` เดาไว้พอดี** (ไม่ต้องแก้หัวใบ): สำเร็จ (รวมพื้นว่าง) =
    `GROUND_REANNOUNCE_AFTER_SECOND_PWD scene=<...> items=<n>` (พื้นว่างพิมพ์ `items=0` เสมอ ไม่ใช่ความเงียบ) ·
    ปฏิเสธ = `GROUND_REANNOUNCE_AFTER_SECOND_PWD_REFUSED scene=<...> reason=<ชื่อ>`
  - เพิ่มก้อน `GROUND_REANNOUNCE_WIRING` (รูปแบบเดียวกับ `DROP_PRESENCE_WIRING` เดิม) -- บรรทัดเดียวที่ chief ต้องเสียบ
    หลังตอบ `0x4B98`: `actions.extend(mob_drop_presence.reannounce_ground(self.mob_loot_cell, legacy))`
- ส่งจดหมายตอบ chief แล้ว: `notes_to_chief/20260904_1812_LANE-B-TO-CHIEF-*`

### 2. ตารางดรอปฉาก 3/5/14 (งานสำรองข้อ 1 ของรอบก่อน + ลำดับ B ท้าย `1649`)
- **ไม่เขียน selector ตัวที่สอง** -- ขยาย `tools/pf_mine_scene_drop_tables.py` ให้ union roster ทั้งห้าฉาก
  (`field_mob_tables`, `_bg0002`, `_bg0003`, `_bg0005`, `_bg0015`) แทนสองฉากเดิม แล้วรัน miner ตัวเดิมซ้ำ
- **assembled**: 5 `DROPS_NORMAL` sets (จากเดิม 2), 4 `DROPS_EQUIPMENT` sets (จากเดิม 2), 10 `DROPS_SPECIALLY` sets
  (จากเดิม 2), **83 item ids ที่ไม่ซ้ำ** (จากเดิม 43), จาก 51 roster rows รวมห้าฉาก -- ตัวเลขมาจาก stdout ของ miner
  ตรง ไม่มีตัวไหนถูกลดโดยเงียบ
- แก้ 4 เทสที่ปักสถานะแคบเดิม (bg0001+Bg0002 เท่านั้น) เป็นสถานะกว้างใหม่ -- **ขีดฆ่า ไม่ลบ** ทุกจุด:
  - `test_the_table_carries_exactly_the_sets_the_roster_names`: `wanted` เดินตาม `field_drop_tables.SCENES`
    ทั้งห้าฉากแทน Bg0002 ฉากเดียว · `orc_chief_sets` แคบลงจาก `{2701003, 5400003}` เหลือ `{2701003}` เพราะ 5400003
    กลายเป็นของที่ฉากใหม่ (Bg0015) ชิปจริงแล้ว ไม่ใช่ของค้างที่ยังไม่ชิป
  - `test_no_id_this_lane_can_emit_has_ever_been_on_a_wire` → เปลี่ยนชื่อเป็น
    `test_one_id_this_lane_can_emit_was_once_on_a_wire_two_never_were` -- **finding จริง**: `2200423`
    (EQUIPMENT_BASE 423 "Red leaves Hammer" -- id เดียวกับที่ `GT-045` วัดว่าขึ้นป้ายชื่อบนจอจริง) อยู่ใน
    `field_drop_tables.ITEMS` แล้ว ผ่าน `DROPS_EQUIPMENT` set `5400004` ที่ฉาก 14 (Bg0015) ชิป -- ก่อนรอบนี้
    id นี้ไปไม่ถึงทางไหนเลยของ bg0001/Bg0002 แก้ `mob_loot.MOB_LOOT_NONCLAIMS` ข้อ 3 ให้ตรงความจริง
    (ขีดฆ่าประโยคเดิม เขียนแก้ต่อท้าย ไม่ลบ) -- อีกสอง id ที่เคยวัดบนไวร์ (`2200003`, `2600001`) ยังไม่อยู่ในตาราง
  - `test_loot_is_the_third_shut_door_and_it_refuses_by_name` → เปลี่ยนชื่อเป็น
    `test_loot_is_no_longer_the_third_shut_door` -- พิสูจน์ว่ามอนฉาก 3 หมุน seed 0-59 แล้วดรอปของจริงได้
    (ก่อนหน้านี้ปฏิเสธ `unknown_drop_set` ทุกตัวก่อนออกคีย์)
  - `test_the_shipped_pin_file_is_what_the_code_computes`: regenerate `scenarios/combat_loot_001.json`
    ให้ตรงกับ `pin_document(legacy)` ใหม่ (เพิ่ม 3 normal sets, 2 equipment sets, 6 specially sets, item_ids 43→83)
- แก้ docstring ที่เท็จแล้วใน `mob_hit_frame.py` ตามจดหมาย LANE-GM `1328` (ไม่แตะพฤติกรรม แค่ประโยคผิด)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
**ยังไม่เห็นอะไรจนกว่า chief จะเสียบบรรทัดเดียวใน `runtime.py`** (เขตของ chief -- ดู CORE-REQUEST) --
แต่เมื่อเสียบแล้ว: (1) เปิดกระเป๋าหลังดรอปของจะไม่ทำให้ของที่ยังอยู่บนพื้นหายจากจออีก (เซิร์ฟเวอร์บอกความจริงซ้ำ
ทันทีหลังตอบรหัสผ่านรอง) และ (2) ฆ่ามอนในฉาก 3, 5 หรือ 14 จะมีของตกลงพื้นจริงเป็นครั้งแรก (ก่อนรอบนี้เซิร์ฟเวอร์
ปฏิเสธเงียบทุกครั้งก่อนออกคีย์ด้วยซ้ำ -- มอนตายได้แต่ไม่มีของตกเลย)

## งานสำรอง (ตาม `COO 1450` ข้อ 6 -- ไม่ได้ทำรอบนี้ เหตุผลกำกับ)
1. **ทะเบียนศพระดับโลกต่อฉาก** (ครึ่งที่สองของ R309 -- โครงเดียวกับของบนพื้น): ยังรอ census ตอน arrival
   ซึ่งเป็นเขต chief/LANE-A -- เลือกส่งฟังก์ชันประกาศของบนพื้นที่ chief รออยู่ก่อน เพราะมี deadline ชัด (19:31)
2. **`RE-208` ขั้น "ป้ายชื่อของไม่กะพริบตอนตีตัวถัดไป"**: ยังไม่เขียนขั้นลง `GT-223` -- รอบนี้เต็มด้วยงานหลักสองข้อ
3. **เก็บ hex ของฉาก 3/5/14 ที่ตีมอนจริงได้ของ + ป้ายชื่อไอเทม** (ต่อยอดจาก drop tables รอบนี้): ยังไม่เปิดใบ GT
   ใหม่ -- ตัดสินใจไม่เปิดเลข ticket ใหม่รอบนี้เพราะกติกาตัวนับร่วม (GT/RE ใช้เลขชุดเดียวกัน) ไม่ชัดพอจะเดาเลขถัดไป
   อย่างปลอดภัยในรอบนี้ (ดู "ยังไม่ได้พิสูจน์")

## หลักฐาน
- `pytest tests/test_mob_drop_presence_ground_reannounce.py` -- **17 เทสใหม่ ผ่านทั้งหมด**
- `pytest tests/test_mob_drop_presence.py tests/test_mob_drop_presence_wiring.py
  tests/test_mob_drop_presence_sustained_resend_hypothesis.py` -- **82 ผ่าน** (ของเดิม ไม่มีอะไรพัง)
- `pytest tests/test_mob_loot.py tests/test_field_mob_tables_bg0003.py tests/test_field_mob_tables_bg0015.py` --
  **207 ผ่าน 251 subtests ผ่าน** (รวม 4 เทสที่แก้ตามหัวข้อ "ที่ทำ" ข้อ 2)
- `pytest tests/test_class_catalog.py tests/test_foundation_legacy_seam.py
  tests/test_lane_a_choose_npc_ground_preserve.py tests/test_mob_pickup.py
  tests/test_mob_pickup_bag_delta_ground.py tests/test_mob_stat_fabrication_guard.py` -- **163 ผ่าน 349 subtests**
  (ทุกไฟล์ที่แตะ `field_drop_tables`)
- `pytest tests/test_field_mobs.py tests/test_field_mobs_scene_binding.py tests/test_mob_death.py
  tests/test_mob_combat.py tests/test_lane_b_mob_ai_tick.py tests/test_mob_ai_tick_gate_wiring.py` -- **495 ผ่าน**

## ผล pf-adversary
ยังไม่สั่ง -- รอบนี้จบก่อนถึงขั้นนั้น (ดู "เกต Windows" ด้านล่างสำหรับสถานะจริง)
🔴 **`ADVERSARY_PENDING #755`** -- รอบถัดไปของสาย B หยิบผลนี้เป็นงานแรกก่อน claim
(ตาม `COO 0903_2345`/`1428`)

## ชุดเทสเต็ม -- รันครั้งเดียวจริง หลัง `git fetch origin main` + merge
`pytest tests/` บนต้นไม้ที่ merge `origin/main` (`d01ae973`, มี `#750` LANE-GM เข้ามาด้วย) แล้ว:
**`10018 passed, 323 skipped, 19339 subtests passed`, 0 failed, 507.96s**

## เกต Windows (`PANYA-DECISION 20260904_1158` §22)
🔴 **`GATE_UNVERIFIED #755`** -- PR เพิ่งเปิดตอนจบรอบ ยังไม่มีเวลาให้ gate ตัดสิน
รอบถัดไปของสาย B เปิดรอบด้วยการตรวจ PR นี้ก่อนทำอย่างอื่น (ก่อน claim ด้วยซ้ำ)

## ยังไม่ได้พิสูจน์
- ชั้น client-observable ทั้งคู่: ของบนพื้นไม่หายตอนเปิดกระเป๋า (`GT-242`) และของตกจริงในฉาก 3/5/14 บนจอ
  (ยังไม่มีใบ GT -- ต้องมีคนแตะ Panya บูตจริง)
- pf-adversary ยังไม่วิ่งรอบนี้ (ดูหัวข้อผล pf-adversary)
- gate Windows ของ PR เซิร์ฟเวอร์ยังไม่ตัดสิน (ดูหัวข้อเกต)

## nonclaim
① ไม่อ้างว่าของบนพื้นกลับมาบนจอ -- นั่นคือคำถามของ `GT-242` ② ไม่แตะ `runtime.py`/`app.py`/v141
③ ไม่แตะ `store.py`/migration ④ ไม่แตะเขตสาย A (`scenarios/world_*.json`) ⑤ ไม่เปิดใบ GT ใหม่รอบนี้
(เหตุผลในหัวข้องานสำรองข้อ 3) ⑥ ไม่อ้างว่า `2200423` จะขึ้นป้ายชื่อทุกครั้งที่ดรอปจากฉาก 14 -- แค่ว่ามันดรอปได้
แล้วตามตาราง การขึ้นป้ายเป็น EXPECTATION จาก RE-066 ไม่ใช่การวัดใหม่

CORE-REQUEST ถึง chief: none (ใบ `1812` ทำหน้าที่นี้แล้ว มีบรรทัดเดียวให้เสียบ)

## สังเกตนอกเขต (ไม่แก้ ตามกติกา "รายงานสิ่งที่เห็นแทนการแก้เอง")
ระหว่าง `git fetch origin main` พบว่ามีอีกเซสชัน (session `01HT1BreLhpGGSeWKXELyWAB`, `Claude Opus 5`)
วิ่งผลรอบที่สองของ pf-adversary สำหรับ `ADVERSARY_PENDING #749` (รอบ `59iqwi` เดิม) แล้วต่อคอมมิตลง
`rounds/B_20260904_1632_59iqwi_*.md` เอง (คอมมิต `e5474694` บน branch เดิม `claude/youthful-ride-59iqwi`,
merge เข้า bridge เป็น `#1179`) พร้อม PR แก้ `pirate-force-server#752` (**ยังไม่ merge เข้า `origin/main`
ตอนที่ตรวจ** — `git log HEAD..origin/main` ของฝั่งเซิร์ฟเวอร์ว่างเปล่า) — บันทึกไว้ให้ทราบ ไม่ใช่ของรอบนี้:
🔴 **ผลนั้นเขียนว่า "ห้ามวางบรรทัด seed ของ chief จนกว่าจะปิด" ข้อยังไม่แก้ (2 ข้อออกแบบ)** — นั่นคือ
CORE-REQUEST **คนละใบ** จาก `reannounce_ground` ของรอบนี้ (`1652`: "seed the ground when a session learns
its scene" ไม่ใช่ `1708`/`1649` ข้อ 2 ที่รอบนี้ตอบ) — ฟังก์ชันของรอบนี้ไม่แตะ `seed_cell`/`claim_for_pickup`
เลย จึงไม่ถูกกระทบ แต่ chief ควรเห็นก่อนเสียบบรรทัด seed (คนละบรรทัดจากที่ใบ `1812` ขอ)
