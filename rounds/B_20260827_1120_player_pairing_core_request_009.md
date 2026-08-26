# B รอบ 2026-08-27 ~11:20-12:10 (+07:00) — สาย B (COMBAT), BUILD-004/005/006

## 0. สรุปว่ารอบนี้ทำอะไร ก่อนไปละเอียด

สร้างครึ่งที่เป็น pure logic ของ "ครึ่งผู้เล่น" ในคู่ hostile pairing (`player_hostile_pairing.py`
ใหม่) — ปิดช่องว่างที่ `notes_to_chief/20260827_0520_ATTENDED-URGENT-*` วัดไว้ว่าเป็นเหตุผลจริงที่
`GT-084` เห็นมอนสเตอร์เป็น NPC ธรรมดา (ไม่แดง) บนบูตไร้แฟล็ก แม้ census จะประกอบ hostile body ครบ
13/13 แล้วก็ตาม (ยืนยันซ้ำแล้วโดย R187) เสนอ `CORE-REQUEST-009` [เสนอ · รอ chief] ให้ chief ต่อสาย
บรรทัดเดียวใน `runtime.py` ตามธรรมเนียมโปรเจกต์ (สายนี้ไม่แตะไฟล์นั้นเลย)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่มีอะไรต่างบนจอ — รอบนี้ทั้งหมดอยู่ชั้น wire/DB (ฟังก์ชัน
ใหม่ยังไม่ถูกเรียกจาก `runtime.py` จนกว่า `CORE-REQUEST-009` จะต่อสาย) เมื่อต่อแล้ว สิ่งที่ผู้เล่นควร
เห็นต่างคือ: มอนสเตอร์ที่ Port Royal (เช่น "Tornado Eagle") ควรขึ้น **ชื่อแดง + แผงเป้าแดง** แทนที่จะ
เป็น NPC สีเขียวปกติ บนการบูตปกติ (ไม่ต้องมีแฟล็กใด ๆ) — เป็นครั้งแรกที่คู่ hostile เต็ม (1, 6) จะออก
สายบนเส้นทางที่เจ้าของเล่นจริง ไม่ใช่แค่บนเส้นทางโพรบที่ถูกล็อกไว้

## 1. อ่านก่อนเขียน — ยืนยันสถานะจริงของงานที่มีอยู่แล้ว (ไม่ทำซ้ำ)

อ่าน `rounds/R176`-`R187`, `notes_to_chief/` ทั้งหมดของ 26-27 ส.ค., `GAME_TEST_QUEUE.md` (`GT-032`,
`GT-084`), `CLIENT_RE_QUEUE.md` (`RE-092`), source สดของ `field_mobs.py` `mob_death.py`
`mob_combat.py` `mob_loot.py` `mob_pickup.py` `player_wire.py` `legacy_bridge.py` `inventory.py`
(อ่านอย่างเดียว ไม่แตะ) `app.py` (อ่านอย่างเดียว) `runtime.py` (อ่านอย่างเดียว) พบว่า:

- **BUILD-004 (ประชากรจาก MOBS table จริง):** ต่อสายแล้วจริง ไม่ใช่งานใหม่ของรอบนี้ —
  `field_mobs.load_roster()` (13 มอนสเตอร์ bg0001 Port Royal, ขุดจริงจาก `CONSTDATA_TH__MOBS.tsv` /
  `TEXTDATA_TH__MOBS_TIP` / placement table ด้วย `tools/pf_mine_scene_mob_roster.py` — ไม่ใช่
  ActorAttr มือประกอบ) ต่อเข้า census จริงผ่าน `mob_death.full_roster_override` ตั้งแต่ commit
  `3036b03` และมีบรรทัดคอนโซลยืนยัน 13/13 (`MOB_DEATH_ROSTER_OVERRIDE_COVERAGE`, commit `dd5c785`,
  R187) มีสนามที่หนาแน่นกว่า (bg0015, 17 มอนสเตอร์รวมบอส `Orc Chief` — ไฟล์
  `field_mob_tables_bg0015.py` มีอยู่แล้วจาก tooling เดียวกัน) แต่ **ยังไม่ถูก `load_roster()` ใช้**
  และฉาก travel ไปที่นั่น (scene 278) COO สั่งปิดไว้โดยเจตนา
  (`20260827_0245_COO-DECISION-BUILD-002-scene278-stays-off-*`) ⇒ ไม่แตะ — เทสอยู่ที่ Port Royal
  ตามคำสั่งงานของรอบนี้เอง (ไม่บล็อกอยู่แล้ว)
- **BUILD-005 (ตี→เลือดลด→ตาย→ศพ):** pure logic ครบแล้วจากรอบก่อน (`mob_combat.py`/`mob_death.py`,
  `CORE-REQUEST-005` ต่อสายแล้ว R177) **แต่ยังมีรูรั่วที่รู้แล้วและยังไม่ปิด**: `bar_frames`/
  `death_frames` ส่งเฟรมแบบ one-entry แทนที่ registry ทั้งก้อน (`RE-092` พิสูจน์แล้วว่าเป็น
  replace-by-omission จริง) แก้แล้วครึ่ง pure logic (`mob_death.hostile_census_frames` +
  `world_population.apply_identity_override`, commit `6286059`/`5a98237`/`83752db`, PR #89 merge
  แล้ว) แต่ `CORE-REQUEST-008` (สามจุดใน `runtime.py`) **ยังไม่ต่อสาย** — grep
  `hostile_census_frames` ใน `runtime.py` สดวันนี้ = 0 hit ยืนยันแล้ว
- **BUILD-006 (ของหล่น→เก็บ→อยู่ในกระเป๋า→รอด relog):** `mob_loot.py`/`mob_pickup.py` ต่อสายแล้ว
  (R180, `CORE-REQUEST-006/007`) แต่ "รอด relog" ชนกำแพงที่รู้และบันทึกไว้แล้วเอง
  (`GOVERNED_BAG_ALLOWLIST_OWNER` ใน `mob_pickup.py`): `inventory.require_known_backpack` ยอมรับ
  แค่สอง snapshot ที่ตายตัว (ship 4 ชิ้น / V111 3 ชิ้น) ⇒ ของที่เลนนี้สร้างจะถูกปฏิเสธตอน SELECT
  ครั้งถัดไป **COO ตัดสินไปแล้ว** (`20260826_0950_COO-DECISION-the-bag-wall-is-chief-s-*`) ว่า
  กำแพงนี้เป็นของ chief (`inventory.py`/`store.py`/`runtime.py` ไม่มีใครเป็น "เลนไอเทม" วันนี้) ไม่ใช่
  ของสาย B ให้ขยาย — สาย B "ถูกแล้วที่ไม่แตะ" (คำ COO เอง) กำหนด chief ไม่เกิน 27 ส.ค. 12:00
  (migration คอลัมน์ `next_item_identity` + ผ่าครึ่ง `require_known_backpack` + สำเนา DB ก่อน
  migrate) ตรวจสดวันนี้: **ยังไม่มี** `migrations/005_*.sql`, ยังไม่มี `next_item_identity` ที่ไหนใน
  `src/` เลย ⇒ ยังไม่ถึงคิวที่สาย B จะ "ส่ง `issued_through` เข้า `BagCell`" ตามที่ COO สั่งไว้ (ข้อ
  ③ ของคำตัดสิน) ⇒ **ไม่มีอะไรให้สาย B ทำต่อในหัวข้อนี้รอบนี้** นอกจากรายงานสถานะ (ไม่ใช่ของสาย B
  ที่บล็อกอยู่)

## 2. GT-032 vs GT-084 — คำตอบจริงตอนนี้ (ไม่เชื่อคำสรุปเก่าคำไหนตรง ๆ อ่านทั้งสองใบสดแล้วจึงสรุป)

**ทั้งสองใบถูกทั้งคู่ พูดถึงคนละครึ่งของคู่เดียวกัน ไม่ใช่ใบใดใบหนึ่งผิด:**

- `GT-032` (2026-08-21, PASS ทั้งสองชั้น) พิสูจน์ว่า **คู่ที่ครบ (ผู้เล่น faction 1, NPC faction 6)**
  เรนเดอร์แดงจริงบนจอจริง — แต่คู่นั้นเกิดได้เฉพาะหลังแฟล็ก
  `--npc-hostile-hypothesis-scenario` เท่านั้น (HYP-PF-027 opt-in) ไม่เคยพิสูจน์อะไรเรื่องบูตไร้แฟล็ก
- `GT-084` (2026-08-27, รอบแรก) วิ่งบน **บูตไร้แฟล็ก** แล้วเห็น 0 บรรทัดคอนโซล `FIELD_MOB`/`HOSTILE`
  และผู้เล่นเห็น "Tornado Eagle" เป็น NPC สีเขียวธรรมดา ไม่แดง — ผลนี้เอง**ถูกอ่านผิดสองชั้นในรอบก่อน
  หน้ารอบนี้**: (ก) R187 แก้ที่ชั้น visibility (grep token ผิด — ป้าย `FIELD_MOB`/`HOSTILE` ไม่เคยมี
  อยู่จริง) แล้วพิสูจน์ว่า 13/13 hostile identity ประกอบเข้า census จริง แต่ (ข) นั่นตอบแค่ครึ่งเดียว
  — จดหมาย `0520` (attended, กะ1) ชี้ต่อว่า **แม้ census จะมี hostile body 13/13 จริง ผู้เล่นเองก็ยัง
  ออกด้วย `basic_faction=0` เสมอบนบูตไร้แฟล็ก** (เพราะโค้ดที่ส่ง faction 1 ให้ผู้เล่นอยู่ในสาขา
  `if npc_hostile_hypothesis_scenario is not None:` เท่านั้น) ⇒ คู่ที่ไคลเอนต์เห็นจริงคือ **(0, 6)**
  ซึ่งเป็นคู่ที่ arena-v2 พิสูจน์ไปแล้วเมื่อ 15 ส.ค. ว่า **neutral แน่นอน** (1,023 ครั้งเป็นกลาง)

**สรุปที่ยืนตอนนี้ (รอบนี้ตรวจโค้ดสดซ้ำอีกครั้ง ยังจริงอยู่):**
`grep -n "basic_faction=" src/pirateforce_foundation/runtime.py` เจอจุดเดียวคือบรรทัด 3051-3052
ซึ่งอยู่ใน `_npc_hostile_start_game_response` ที่ถูกเรียกก็ต่อเมื่อ `npc_hostile_hypothesis_scenario
is not None` (บรรทัด 4472) เท่านั้น — บนบูตไร้แฟล็กของเจ้าของ ไม่มีทางไหนเลยที่ผู้เล่นจะออกด้วย
faction อื่นจาก 0 ⇒ **`GT-084` ไม่ใช่ "โค้ดพัง" และไม่ใช่แค่ "มองไม่เห็น" อีกต่อไป — เป็นผลจริงของ
"ครึ่งที่ขาด" ที่จดหมาย `0520` ระบุ และยังไม่มีใครแก้ ณ ตอนที่รอบนี้เริ่ม**

## 3. สิ่งที่สร้างรอบนี้ (ครึ่งที่เป็น pure logic เท่านั้น — เขตของสายนี้)

**`src/pirateforce_foundation/player_hostile_pairing.py`** (ใหม่) —
`compose_start_game_with_player_pairing(projector, selected, backpack, pc, frame)`:
เรียก `projector.start_game(selected, basic_faction=field_mobs.PLAYER_PAIR_FACTION,
backpack=backpack)` แบบเดียวกับที่ `_npc_hostile_start_game_response` ทำอยู่แล้ววันนี้ (encoder
เดิม ไม่มีของใหม่) **แต่ไม่มีการปักหมุดตัวตนตัวเดียว** ("เฉพาะ smoke identity ที่ HYP-PF-027 คำนวณ
พินไว้") — ทั่วไปสำหรับตัวละครใดก็ได้ที่ serializer เดิมยอมรับอยู่แล้ว (`scene_id in (1, 2)`,
`scene_seq == 0`, `basic_faction == 1` — เงื่อนไขเดิมของ `player_wire.make_actor_attr_with_
basic_faction`, ไม่ได้คลายเลยแม้แต่บิตเดียว) fail-closed คืนไบต์ production เดิมตรง ๆ เมื่อ
serializer ปฏิเสธ (ValueError/RuntimeError/TypeError/AttributeError — เพิ่ม AttributeError หลัง
pf-adversary self-review พบว่า `selected=None` จะ crash ไม่ fail-closed ก่อนแก้ ดูข้อ 5) หรือเมื่อ
ความยาวไบต์ที่ได้ไม่ตรงกับ +`field_mobs.FACTION_SPLICE_BYTES` เป๊ะ (ตัวคุมความยาวเดียวกับที่
`_npc_hostile_start_game_response` ใช้อยู่แล้ว)

**ทำไมปลอดภัยที่จะทำทั่วไป ไม่ใช่การเดา:** อ่าน `app.py` (อ่านอย่างเดียว ไม่แตะ) พบว่า spawn เริ่มต้น
ของทุกตัวละครคือ `Position(1, 0, ...)` (`legacy.V135_PLAYER_X/Y/Z`) — ตรงกับช่วงที่ serializer เดิม
ยอมรับอยู่แล้ว **เป๊ะ** และ checkpoint การเดิน (`runtime.py:3537`) ไม่เคยเปลี่ยน `scene_id`/`scene_seq`
เลย (เปลี่ยนแค่ x/y/z/heading) ⇒ ตัวละครทุกตัววันนี้ (ไม่มีทาง travel ไปฉากอื่นที่เปิดใช้งานอยู่จริง)
อยู่ในช่วงที่ยอมรับได้เสมอ ⇒ ฟังก์ชันนี้ไม่ได้ "คลายด่าน" อะไรเลย มันแค่เอาหมุดตัวตนที่ไม่จำเป็นออก
วันที่ฉากอื่นเปิดจริง (เช่น scene 278) ตัวละครที่อยู่ที่นั่นจะชน `ValueError` เดิมของ serializer และ
fail-closed ทันที เหมือนวันนี้ทุกอย่าง

**`tests/test_player_hostile_pairing.py`** (ใหม่, 9 เทส): scene1/seq0 ได้คู่จริงไบต์ตรงกับเรียก
serializer ตรง ๆ · scene2/seq0 ได้เหมือนกัน · ตัวตนอะไรก็ได้ (ไม่ใช่แค่ตัวปักหมุดเดิม) · ฉากที่ไม่รับ
(3) fail-closed คืนไบต์เดิมเป๊ะ · `scene_seq` ที่ไม่ใช่ 0 fail-closed · `selected=None` fail-closed
ไม่ crash · บรรทัดคอนโซล `describe_pairing_attempt` เป็น cp874-encodable และมีโทเค็นที่ grep ได้
เสถียร · ค่าคงที่ faction ตัวเดียวกับ `field_mobs.PLAYER_PAIR_FACTION` เป๊ะ (กันดริฟท์)

**`tests/test_field_mobs.py`** (แก้ 1 จุด): ปรับ pin รายชื่อไฟล์ที่ import `field_mobs` (tripwire ที่
ตั้งใจให้แดงเมื่อมี importer ใหม่) เพิ่ม `player_hostile_pairing.py` พร้อมย่อหน้าอธิบายเหมือนของเดิม
ทุกจุดที่เคยแก้มาก่อน (MOB-COMBAT-001/MOB-DEATH-001/MOB-LOOT-001/MOB-AGGRO-001) — ตามที่ทริปไวร์เอง
เขียนกำกับว่าต้อง "update the letter"

## 4. `CORE-REQUEST-009` [เสนอ · รอ chief] — จุดเดียวใน `runtime.py`

จดหมายเต็มส่งแล้ว: `notes_to_chief/20260827_1120_LANE-B-CORE-REQUEST-009-player-faction-pairing.md`
สรุปสั้น: แทนที่เงื่อนไข `if npc_hostile_hypothesis_scenario is not None:` (บรรทัด ~4472 ของ
`runtime.py`) ด้วยการเรียก `player_hostile_pairing.compose_start_game_with_player_pairing(...)`
**เสมอ** (ไม่มีเงื่อนไขแฟล็ก) แล้วให้สาขาเดิมของแฟล็กยังอยู่ต่อจากผลนั้น (หรือแทนที่ไปเลยก็ได้ — จด
ทางเลือกไว้ในจดหมาย ให้ chief ตัดสิน) — โค้ดตัวอย่างพร้อมก็อปอยู่ในจดหมาย

## 5. pf-adversary self-review (ทำเอง ไม่มี subagent ในสภาพแวดล้อมนี้)

พยายามหักล้างข้อกล่าวอ้างของตัวเองก่อน push:
1. **`selected=None` crash แทนที่จะ fail-closed** — พบจริงด้วยการยิงฟังก์ชันตรง ๆ
   (`AttributeError: 'NoneType' object has no attribute 'position'`) **แก้แล้ว**: เพิ่ม
   `AttributeError` เข้า tuple ที่ดักไว้ + เทสใหม่ปักไว้ (`test_none_selected_fails_closed_instead_
   of_crashing`)
2. ตรวจว่าค่าคงที่ faction/ความยาวไบต์อ้างจาก `field_mobs` ตัวเดียว ไม่ประกาศคู่ขนานเอง — ผ่าน (เทส
   `test_faction_constant_is_the_same_object_field_mobs_uses` ปักไว้)
3. ตรวจว่าไม่มีการปักหมุด scene_id/scene_seq เกินกว่าที่ serializer เดิมมีอยู่แล้ว (ไม่ใช่การคลายด่าน
   แอบแฝง) — อ่านซอร์ส `player_wire.make_actor_attr_with_basic_faction` ตรง ๆ ยืนยันเงื่อนไขเดิมไม่
   เปลี่ยน
4. ตรวจ cp874: ทั้งสองไฟล์ใหม่ + ไฟล์เทสที่แก้ ผ่าน `.encode("cp874")` ตรง ๆ (บรรทัดที่พิมพ์ออก
   คอนโซลจริงด้วย `describe_pairing_attempt` มีเทสปักแยกต่างหาก)
5. ตรวจ containment tripwire ที่มีอยู่แล้วของโปรเจกต์ (`test_npc_hostile_hypothesis.py`'s
   `test_exactly_two_foundation_modules_mention_the_lane`) — module ใหม่เขียนคำอธิบายพาดพิงถึงเลน
   HYP-PF-027 แต่ตั้งใจ**ไม่เอ่ยชื่อโมดูลนั้นเป็นสตริง** เพื่อไม่ให้กลายเป็น "ไฟล์ที่สาม" ในรายชื่อที่
   ทริปไวร์นั้นล็อกไว้ (ตรวจแล้วว่าไม่ชน — grep `npc_hostile_hypothesis` ใน `player_hostile_pairing.py`
   = 0 hit)

## 6. ตัวเลขที่วัดได้

- เทสใหม่: `tests/test_player_hostile_pairing.py` 9 เทส (ผ่านทั้งหมด)
- เทสที่แก้: `tests/test_field_mobs.py` 1 assertion (pin importer list) — ยังผ่านทั้งไฟล์ (17 เทส)
- สวีตเต็ม: **3410 → 3411 ผ่าน** (0 regression) · error 18 ตัวเดิม (capstone/pefile/pytest ไม่ติดตั้ง
  ใน sandbox นี้ ไม่เกี่ยวกับรอบนี้) · skip 212 ตัวเดิม
- ไม่มีการเรียก `player_hostile_pairing` จากไหนใน `src/` เลยรอบนี้ (grep ยืนยัน) ⇒ ความเสี่ยงต่อ
  production path = ศูนย์ จนกว่า `CORE-REQUEST-009` จะถูกต่อสายโดย chief

## 7. ไฟล์ที่แตะ (pirate-force-server, รวม 3 ไฟล์)

- `src/pirateforce_foundation/player_hostile_pairing.py` (ใหม่, +116 บรรทัด)
- `tests/test_player_hostile_pairing.py` (ใหม่, +166 บรรทัด)
- `tests/test_field_mobs.py` (แก้ 1 จุด, +6/-1 บรรทัด)

## 8. ยังไม่ได้พิสูจน์ (ชัดเจน ไม่ปิดบัง)

- ไม่มีใครดูจอรอบนี้เลย — claim ทั้งหมดอยู่ชั้น wire/DB (ยิงฟังก์ชันตรง ๆ + เทียบไบต์กับ
  `projector.start_game` เรียกตรง) ผลชั้น client-observable (ชื่อแดงจริงไหมบนบูตไร้แฟล็ก) รอ
  `CORE-REQUEST-009` ต่อสายก่อน แล้วรอ `GT-084` รอบสองตามที่จดหมาย `0520` ข้อ ④.3 เสนอไว้แล้ว (ใบนี้
  ไม่เปิดใบใหม่ซ้ำ — ใช้ใบเดิม)
- ไม่ได้อ้างว่า `basic_faction=1` เป็นค่าเดียวที่ขาด — อ้างแค่ว่ามันขาดแน่ ๆ บนบูตไร้แฟล็กวันนี้ (จาก
  `0520`) และการเติมมันเข้าไปตามที่เสนอไม่มีความเสี่ยงเพิ่มต่อเส้นทางที่ serializer เดิมไม่ยอมรับอยู่
  แล้ว (fail-closed)
- `CORE-REQUEST-008` (compose bar/death/dying frames เข้า full census) ยังค้างจากรอบก่อน ไม่ใช่ของ
  ใหม่รอบนี้ — grep สดยืนยันซ้ำว่ายังไม่ต่อสาย (ดูข้อ 1)

## 9. เปิดใบให้สาย C

ไม่มีใบใหม่รอบนี้ — ไม่พบ unknown ที่ต้องวิจัยก่อนสร้าง ทุกอย่างที่ทำวันนี้ยืนยันได้จากซอร์สสดของ
โปรเจกต์เอง
