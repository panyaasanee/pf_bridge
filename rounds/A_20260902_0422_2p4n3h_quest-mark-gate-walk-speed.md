[LANE-A (WORLD) round `2p4n3h` -- 2026-09-02T04:22+07:00]

# ประตูที่ปิดไอคอนเหนือหัว NPC ทุกตัวมาตลอด: บิต `0x0040` ที่ census ไม่เคยส่ง

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

NPC ในเมืองทุกตัว **ผ่านเงื่อนไขข้อแรกที่ไคลเอนต์ใช้ตัดสินว่าจะเรียกบอร์ดไอคอนเหนือหัวหรือไม่**
เป็นครั้งแรก — เมื่อวาน ไคลเอนต์ **ข้ามการเรียกบอร์ดไปเลย** สำหรับชาวเมืองทุกคนในทุกฉาก
โดยไม่ได้ประเมินเงื่อนไขอื่นสักข้อ · ไม่ต้องเปิดแฟล็ก ติดทุกบูต
🔴 **ไม่ได้อ้างว่าไอคอนจะขึ้น** — เปิดได้หนึ่งในสี่ท่อนของเงื่อนไขข้าม อีกสามท่อนเป็นของไคลเอนต์
`GT-202` คือใบที่ตัดสินด้วยตาบนจอ · และผลลบ (ไม่มีไอคอน) มีค่าเท่าผลบวก

ของแถมที่วัดได้จริงในไบต์: NPC สำมะโนส่ง `MOBS.n_SPEED_WALK` ของตัวเองแล้วทุกตัว แทนที่จะไม่ส่งอะไร

## 1. NOW.md (อ่านก่อนทุกอย่าง)

"งานด่วนตอนนี้" มี **P-1** (ของดรอปค้างพื้น — ตัวบล็อกคือ `runtime.py` ของ chief + decoder ของสาย B)
· **P-2** (สีชื่อมอนสเตอร์ — Codex ระบุ `NOT_READY_FOR_POLICY_CHANGE` ยังไม่มีโค้ดเปิดใช้)
· **P-3** (ปุ่ม GM — RE ต่อจาก RE-104) · ทั้งสามข้อ **ไม่ใช่เขตของสายนี้** และไม่มีอะไรให้สาย A ทำ
คิวถัดไป GM-A/UI-A/GM-B/UI-B/census-latch: ส่วนที่เป็นโค้ดของสายนี้ **จบแล้วทั้งหมด รอ Panya รัน
`GT-192`/`GT-200`** ซึ่งตามกฎใหม่ในหัวไฟล์ NOW.md เอง (Panya ยืนยันสด 2026-09-01 14:47+07)
**ไม่ใช่ตัวบล็อกสาย** ⇒ รอบนี้เดินคิวปกติต่อ ตามใบมอบหมายที่ chief จ่ายไว้

**รอบนี้ขยับ NOW ข้อไหน: ไม่ขยับข้อไหนโดยตรง** — พูดตรง ๆ ไม่อ้อม
เหตุผล: P-1/P-2/P-3 อยู่คนละเขต และข้อที่เป็นของสายนี้ในคิวถัดไปขยับไม่ได้แล้วด้วยโค้ด
(เหลือแต่รอคนหน้าจอ) · สิ่งที่รอบนี้ทำคือ **ใบมอบหมายที่ chief จ่ายให้สาย A โดยตรง**
(`20260902_0205` เรื่องที่ 2, quest mark) ซึ่งเป็นงานที่ NOW.md ระบุให้ต่อคิวหลังสามข้อด่วน
🔴 และมันเกี่ยวกับ P-2 ตรงที่ **ไม่แตะกันเลย**: รอบนี้ไม่แตะสี ไม่แตะ faction ไม่แตะ identity
ไม่แตะ FontStyleID แม้แต่บิตเดียว ตามที่ Codex กำชับ

## 2. Section A (addendum v2) — ชะตา PR รอบก่อน

- `pf_bridge#778` (`[LANE-A] round 7ste68`) — `merged_at 2026-09-01T20:11:58Z` ⇒ อยู่บน main
- `pirate-force-server#524` (`[LANE-A] census actors carry their mined level`) —
  `merged_at 2026-09-01T20:25:31Z` ⇒ อยู่บน main
- ไม่มีงานรอบก่อนหายจาก main ⇒ ไม่ต้อง cherry-pick · branch รอบนี้ตั้งจาก `origin/main` สด ๆ ทั้งสอง repo
- ต้นรอบไม่มี PR เปิดค้างที่หัวข้อขึ้นต้น `[LANE-A]` ในทั้งสอง repo (มีของ `[LANE-GM]` สองใบ ไม่ใช่ล็อกของเรา
  และไม่แตะ) ⇒ เปิด draft PR ยึดล็อกก่อนลงมือ

## 3. Section B — mailbox (บริโภคครบสองใบ)

ตรวจสองแพทเทิร์นตาม `CHIEF-DECISION 20260901_2357` พบใบที่ `ADDRESSEE: LANE-A` ยังไม่บริโภคสองใบ:

1. `20260902_0205_CHIEF-TO-LANE-A-avatarattr-and-questattr-assigned.md` — **งานหลักของรอบนี้**
   (เรื่องที่ 2) · เรื่องที่ 1 (AvatarAttr 22 ฟิลด์) ยังไม่ทำ เขียนเหตุผลไว้ใน stub และข้อ 8 ล่างนี้
2. `20260902_0215_CHIEF-REPLY-hyp-pf-042-registration-queued-next-pr.md` — chief ยังไม่ลงทะเบียน
   ledger และพูดตรง ๆ ว่ายังไม่ทำ ⇒ **ไม่มีงานค้างฝั่งนี้** ไม่ใส่ annotation (ตามที่ chief ยืนยันว่าถูกแล้ว)

stub `.CONSUMED.txt` ครบทั้งสองใบ + สำเนาต้นฉบับเข้า `consumed/` · ไม่ลบต้นฉบับ

## 4. งานหลัก: ทำไมไม่มี NPC ตัวไหนเคยมีไอคอนเหนือหัวเลย

ใบสั่งเขียนว่า "ช่องว่างจริงคือเราไม่เคยส่ง `QuestAttr` เลย ⇒ งานคือส่ง `QuestAttr`"
ใบต้นทางของมัน (ka1-B `20260901_2220` ข้อ ③) กำชับเองว่า **"ให้อ่านแถวจริงก่อนลงมือ อย่าอ้างใบนี้
เป็นหลักฐาน"** รอบนี้จึงอ่านแถวจริงก่อน แล้วได้ข้อเท็จจริงที่เปลี่ยนลำดับงาน:

**ทั้ง 10 แถว** ของ `reference_codex_attr/PF_ATTR_QUEST_MARK_SELECTOR.tsv` มีคอลัมน์
`skip_conditions` เป็นสายเดียวกันเป๊ะ และท่อนแรกคือ

> `CNetNPC setter skips the board call when +0x70 mask 0x40 is clear,
>  board +0x360 is null, or cached selector +0x364 is unchanged`

`+0x70` คืออะไร — `PF_ATTR_FIELD_SEMANTICS.tsv` ทั้งไฟล์มีฟิลด์ที่ `offset=0x70` ในตระกูล
BasicAttr **แถวเดียว**: `BasicAttr@0x70` `semantic_name=field_presence_mask` `PROVEN_EXACT`
`gate=ALWAYS` tag `0x12` len 2 = **mask u16 ที่ `make_npc_attr` เขียน**
บิต `0x0040` ในไฟล์เดียวกันคือ `BasicAttr@0x54` `applies_to_class=CNetNPC`
`semantic_name=MOBS.n_SPEED_WALK_to_initial_visual_horizontal_locomotion_scalar`
`PROVEN_EXACT` tag `0x2A` len 4 · และ `make_npc_attr` ของ chief เขียนกำกับเรื่องเดียวกันไว้เองตั้งแต่ V73

⇒ **census ธรรมดาไม่เคยตั้งบิตนี้เลย** helper แช่แข็งตั้งให้เฉพาะเมื่อได้ `movement_speed` และ
composer ทั้ง 13 ตัวส่ง `None` มาตลอด ⇒ selector ไม่เคยถูกประเมินสำหรับชาวเมืองสักตัวในประวัติโปรเจกต์

🔴 **ทำไมส่ง `QuestAttr` แล้วไม่ช่วยอะไรในวันนี้** — Codex เขียนเองในใบ checkpoint P0-3 ว่า
"QuestAttr lookup 0 รวมทั้ง missing entry และ stored zero" ⇒ `QuestAttr` ที่ถือค่า 0 (ค่าเดียว
ที่เซิร์ฟเวอร์นี้ส่งได้อย่างซื่อสัตย์วันนี้ เพราะไม่มี state การรับเควสอยู่ที่ไหนเลย) **มีผลเท่ากับไม่ส่งเป๊ะ**
ส่วนประตู `0x0040` ไม่เท่า · รอบนี้จึงทำครึ่งที่เปลี่ยนอะไรจริงก่อน แล้วเขียนเหตุผลไว้
แทนที่จะส่ง no-op ที่ดูเหมือนความคืบหน้า (ใบ ASK-COO ข้อ 2)

**ข้อมูลที่ทำให้เรื่องนี้คุ้มทำ ไม่ใช่แค่ถูกทฤษฎี**: join 100 n_ID ที่ Port Royal ส่งจริง เข้ากับ
`gamedata/tables/CONSTDATA_TH__MOBS.tsv` แล้ว **91 ตัวมี `s_QUEST_BEGIN`/`s_QUEST_END` ไม่ว่าง**
(ทั้งตาราง 811 จาก 3210 แถว) ⇒ ถ้ากลไกครบ เมืองควรมีไอคอนเต็มไปหมด ไม่ใช่ตัวสองตัว

### สิ่งที่สร้าง

`src/pirateforce_foundation/world_census_gait.py` (Foundation-owned additive · ไม่แตะ v141 /
`runtime.py` / `app.py`):

- `WALK_SPEED_BY_MOBS_N_ID` — crosswalk `MOBS.n_ID -> n_SPEED_WALK` **563 แถว** = ยูเนียนของ
  n_ID ที่ census source ทั้ง 13 ตัวส่งจริง (ตารางเกมอยู่ใน `pf_bridge` ไม่ใช่รีโปเซิร์ฟเวอร์
  ทุกตารางที่ mine ในแพ็กเกจนี้จึงเป็น literal ตามขนบเดิม)
- `walk_speed_for(mobs_n_id)` — **ปฏิเสธ ไม่มี default** · id ที่ไม่ได้ mine = actor ที่สายนี้ไม่เคยวัด
- `census_npc_attr(...)` — keyword-only wrapper บน `world_census_level.leveled_npc_attr`
  (keyword-only ด้วยเหตุผลเดิม: พารามิเตอร์แรกของ helper แช่แข็งต้องเป็น `MOBS.n_ID` จริง
  ไม่ใช่ Mob-Set number — ความผิดพลาดของ `GT-078`)
- `read_walk_speed(...)` — อ่านค่ากลับ **ออกจากไบต์** เดินทีละฟิลด์จาก mask (ชื่อ → level → คู่ HP)
  ไม่ได้เขียน offset คงที่ · คืน `None` ถ้าไม่มีบิต = คำตอบของ census ทุกตัวก่อนรอบนี้
- `quest_board_gate_is_open(...)` — ตอบเฉพาะท่อนที่เซิร์ฟเวอร์คุมได้ ไม่แตะอีกสามท่อน

แก้ `world_census_level.leveled_npc_attr` ให้รับ `movement_speed` แล้วส่งต่อ (ดีฟอลต์ `None`
= บอดี้เดิมเป๊ะทุกไบต์) · level อยู่ **หน้า** คู่ HP (บิต 0x0002) และ gait อยู่ **หลัง** (บิต 0x0040)
สองฟิลด์จึงไม่แย่งตำแหน่งกัน และตัวตรวจ layout เดิมของ `with_level` ไม่กระทบ

### ที่ต่อสาย (15 จุด)

census source ทั้ง 13 ตัวใน `world_scene_travel.CENSUS_SOURCES` (ฉาก 1 · 2 · 3 · 4 · 5 · 6 · 7 ·
8 · 9 · 10 · 11 · 14 · 130) **บวกอีกสองจุดที่ไม่ได้อยู่ในใบสั่ง แต่ต้องแก้พร้อมกัน**:
`lane_hooks/lane_a_choose_npc_scene1.py` และ `lane_a_choose_npc_scene14.py`
สองไฟล์นี้ **ประกอบ roster ทั้งชุดใหม่ทุกครั้งที่มีคนคลิก NPC** และเรียก `legacy.make_npc_attr`
ตรง ๆ ⇒ 🔴 **มันย้อนทั้ง gait และ level ของทุกตัวบนสาย ทันทีที่ผู้เล่นคลิกใครสักคน**
(ของ level เป็นการถดถอยที่รอบ `7ste68` ทิ้งไว้โดยไม่รู้ตัว — รอบนี้ปิดด้วย)
นี่คือกฎ "ต้องมีในทุก generation" ที่ coverage row ของ gait พินไว้เองจากการถดถอย walk→run ของ V85

ฉาก 2 ส่ง `placement.speed_walk` ของตัวเอง (ตารางฉากนั้น mine คอลัมน์เดียวกันไว้ก่อนแล้ว)
ไม่ใช่ค่าจาก crosswalk · เทสจับสองตารางมาชนกัน: **ตรงกันทั้ง 97 placement / 40 n_ID**
= cross-check เดียวที่รอบนี้มีว่าการถอดตาราง 563 แถวเป็นคอลัมน์ที่ถูก ไม่ใช่คอลัมน์ข้าง ๆ

## 5. หลักฐานสองชั้น

- **wire/DB (ทำแล้ว)**: `tests/test_world_census_gait.py` (20 เทส + subtests) อ่านค่ากลับ
  **ออกจาก `generation.pc`** รายตัวครบทั้ง 13 census source · พิน tag `0x2A` เป็น literal
  และเทียบไบต์บนสายกับ literal (ไม่ใช่กับค่าคงที่ของโมดูลเอง) · พินว่า `make_npc_attr` เปล่า ๆ
  **ยังไม่ตั้งบิต 0x0040** (กัน revert เงียบ) · พินว่า crosswalk ครอบคลุมทุก id ที่ census ส่งจริง
  โดยเดินจาก**ตารางที่ส่ง** ไม่ใช่จากตารางที่เขียน · ปฏิเสธ id ที่ไม่ได้ mine / ค่านอกโดเมน /
  ค่าที่ไม่ใช่ int · reader ปฏิเสธบอดี้ที่ตั้งบิตแต่ไม่มีฟิลด์
- **client-observable (ยังไม่ทำ ต้องมีคนหน้าจอ)**: `GT-202` (ท้าย `GAME_TEST_QUEUE.md`)
  สถานะ `PENDING` จนกว่า PR รอบนี้จะขึ้น main · ใบเขียนไว้ชัดว่า **NEGATIVE-RESULT ไม่ใช่ FAIL**

## 6. ตัวเลขที่ขยับ และทำไมมันขยับเท่านั้นพอดี

ทุกบอดี้ census โตขึ้น **5 ไบต์** (tag 1 + f32 4) ไม่มากไม่น้อย:
- staircase ทั้ง 4 ระดับที่ anchor ทั้งสองใน `scenarios/world_population_full_001.json`:
  3→+15 · 20→+100 · 60→+300 · 108→+540 (= 5 ต่อ actor เป๊ะทุกช่อง) · membership/ลำดับ **ไม่ขยับ**
- digest sha256 ทั้ง 4 rung ใน `test_world_census_wiring.py` — re-derive จาก dispatcher จริง
  ที่ `PIN_ANCHOR` ไม่ได้พิมพ์มือ · เลขเดิมเก็บเป็นประวัติ ไม่ลบ
- `test_the_census_is_one_shot_per_session`: +520 = **104 × 5** — 4 ตัวที่ถูกทับด้วยบอดี้ hostile
  ไม่ขยับ เพราะ `field_mobs` ส่งฟิลด์นี้มาตั้งแต่ `COO-DECISION 2026-08-28T01:46`
  🔴 เลข 104/4 ตัวเดียวกันนี้เคยใช้กับ **ฟิลด์ level** ในรอบก่อน ⇒ การที่ข้อยกเว้นชุดเดิมตรงกัน
  ข้ามสองฟิลด์สองรอบ คือตัวควบคุมที่บอกว่าการแยกนี้เป็นของจริง ไม่ใช่ความบังเอิญ
- `test_mob_combat_bg0015_gates`: +81×5 (pc) และ +(81−12)×5 (frame) — 12 ตัวที่ splice hostile ไม่ขยับ
- ทุกจุด **เก็บเลขเดิมไว้เป็นประวัติ** ตามขนบของไฟล์เหล่านั้น และเขียนเป็น**เลขคณิต**ไม่ใช่เลขที่รันแล้วก๊อบมา

## 7. guard สองตัวที่แดง และทำไมการแก้มันไม่ใช่การอ่อนข้อ

**(ก) `test_npc_gait_wire.py::test_no_foundation_module_requests_a_movement_speed`**
guard นี้เขียนไว้ตั้งแต่ต้นว่า *"ถ้ามีคนต่อ gait เข้า Foundation population เทสพวกนี้จะล้ม
และ coverage matrix row ต้องถูกทบทวนในการเปลี่ยนแปลงเดียวกัน"* ⇒ รอบนี้ทำตามที่มันสั่ง:
เพิ่ม `world_census_gait.py` / `world_census_level.py` เข้า `KNOWN_GAIT_REQUESTING_MODULES`
พร้อมเหตุผล และ **เขียน `docs/FUNCTIONAL_COVERAGE.json` แถว `npc_locomotion_presentation` ใหม่
ใน commit เดียวกัน** — ประโยคเดิมที่ว่า "The Foundation population path never requests a movement
speed" **เก็บไว้เป็นประวัติในบันทึกของแถวนั้น ไม่ลบ** พร้อมบอกว่ามันไม่จริงแล้วและทำไม
🔴 เทสไบต์สองตัวของ guard นั้น **ไม่ถูกแก้และยังเขียว**: มันคุม `population.py` (เส้นทาง legacy
nearest-20) ซึ่งรอบนี้ไม่แตะ

**(ข) `test_npc_interaction_wire.py::test_no_foundation_module_implements_quest_or_shop_behavior`**
guard grep คำอังกฤษธรรมดาใน `src/*.py` — chief ระบุเองในใบ `20260902_0330` ว่าใบนี้คือ
**จุดที่เสี่ยง false-positive สูงสุดในต้นไม้** และยังไม่มีคำตัดสินหลักการจาก COO
รอบนี้ทำสองอย่าง แทนที่จะขยาย allowlist เฉย ๆ:
1. **เขียนคอมเมนต์ของ composer ทั้ง 13 ไฟล์ใหม่ให้ไม่ต้องพึ่งข้อยกเว้นเลย** (พูดถึง "icon board"
   ตรง ๆ) ⇒ เหลือไฟล์เดียวที่ต้องยกเว้นคือ `world_census_gait.py` ซึ่งเป็นไฟล์ที่หัวข้อนั้น**เป็น
   เนื้อหาของมันจริง ๆ**
2. **พิสูจน์เงื่อนไขของข้อยกเว้น ไม่ใช่เถียง** — เทสใหม่ `test_the_gait_modules_quest_hits_are_all_prose`
   tokenize ไฟล์แล้วบังคับว่า token ทุกตัวที่มีคำนั้นต้องเป็น `COMMENT` หรือ `STRING`
   ⇒ วันที่มันโผล่เป็นชื่อตัวแปร แอตทริบิวต์ หรือการเรียกฟังก์ชัน guard จะแดงทันที
   (แพทเทิร์นเดียวกับ `test_the_identity_tables_shop_hits_are_all_npc_title_data` ที่ไฟล์นั้นใช้อยู่แล้ว)

## 8. nonclaim

1. **ไม่ได้อ้างว่าไอคอนจะขึ้น** — เปิดได้หนึ่งในสี่ท่อน อีกสามท่อน (`+0x360` null · cache `+0x364`
   · predicate ของเควส) เป็นของไคลเอนต์ · ตาราง selector ทั้งใบเป็นชั้น `IMAGE` และ Codex เขียน
   nonclaim เองว่าการนำเสนอบนจอเป็นคนละชั้นแหล่งข้อมูล
2. **ไม่ได้อ้างว่า NPC จะเดิน** — ฟิลด์นี้ชื่อ "initial visual horizontal locomotion scalar"
   เป็นสเกลาร์ ไม่ใช่คำสั่งให้เคลื่อนที่ · ไม่มีใครสั่งให้ census actor เดิน และรอบนี้ไม่ได้ทำ
3. **การอ่าน `+0x70` ว่าเป็น mask ของ BasicAttr เป็นของสายนี้** ติดป้าย
   `[LANE-A ASSUMPTION - AWAITING COO CONFIRMATION]` ในโค้ด + ใบ ASK-COO `20260902_0437`
   ถ้าผิด **ไม่ต้องย้อนไบต์ ต้องย้อนเหตุผล**: ค่าที่ส่งคือคอลัมน์ที่ shipped อยู่แล้วของแถวนั้น
4. **ไม่แตะ `QuestAttr`** (ดูข้อ 4) และไม่แตะ `AvatarAttr` เรื่องที่ 1 ของใบสั่งเลย — เรื่องนั้นยัง
   เป็นของสาย A จะทำรอบถัดไปเป็นใบ "ตรวจก่อน" ตามกติกาข้อ (ง) ที่ใบสั่งกำชับ
5. **ไม่แตะสี/faction/ชนิด actor/identity sign** แม้แต่บิตเดียว — P-2 ยังเปิด
6. เส้นทางอื่นที่ประกอบ NPCAttr เองและ **ยังไม่ได้ไล่**: `world_face_frame` · `npc_wire` ·
   `gm/state_wire` · โมดูล `*_hypothesis` ทั้งหมด · `population.py` (เส้น legacy nearest-20)
   พวกนี้ไม่ใช่ census ปกติและไม่อยู่ในใบสั่งนี้ · `mob_scene_recompose` สืบทอดการแก้นี้เอง
   เพราะใช้ `world_population_bg0002` เป็น composer ตรง ๆ
7. `n_SPEED_WALK = 0` มีจริงในตาราง และส่งไปตามนั้น — ไม่ได้ยกพื้นให้ เพราะการแต่งเลขขึ้นเองแย่กว่า

## 9. จบรอบ

push ทั้งสอง repo → แก้หัวข้อ/body ให้มี `PF-AUTOMERGE: v4` (GET ยืนยัน) → ปลด draft ด้วย
`update_pull_request(draft=false)` → ยืนยัน `draft:false` → **wake gate commit เปล่าเฉพาะ
`pirate-force-server`**

**รอบนี้ขยับ NOW ข้อไหน: ไม่ขยับข้อไหน** (เหตุผลเต็มในข้อ 1) — ทำใบมอบหมายที่ chief จ่ายให้สายนี้
โดยตรงแทน ซึ่งเป็นงานคิวถัดไปตามที่ NOW.md เองระบุ · ยังติ๊กอะไรไม่ได้ ต้องรอ Panya รัน `GT-202`

-- LANE-A (WORLD) round `2p4n3h`
