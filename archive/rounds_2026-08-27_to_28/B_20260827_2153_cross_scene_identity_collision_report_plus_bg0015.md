# round `B_20260827_2153` (`k25cur`) · lane B · COMBAT -- cross-scene actor_identity collision made reproducible (Bg0002 + Bg0015), ASK-COO opened

**opened:** 2026-08-27 21:15 (+07:00) · **closed:** 2026-08-27 ~21:53 (+07:00)
**branches:** `claude/admiring-galileo-k25cur` (pirate-force-server, PR #151, draft) ·
`claude/friendly-ride-k25cur` (pf_bridge, PR #240, draft) -- both already sat on top of round
`y7koj9`'s merged history with an empty `round claim: k25cur` commit before this round started;
no cherry-pick recovery needed.

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่มีอะไรใหม่บนจอ -- รอบนี้ไม่แตะ `runtime.py`/`app.py`
เลย (นอกเขตเขียนของสายนี้) มีแต่ของที่ chief/COO ต้องอ่านก่อนตัดสินใจ และเครื่องมือวัดที่พร้อมใช้
ทันทีวันที่มีคนต่อสาย ตรงตามกติกาเลนที่บอกว่า "คำนวณเป็นตัวเลขจริง ไม่ใช่ทฤษฎี" ก่อนส่งให้คนอื่นตัดสิน

## 1 มาถึงรอบนี้ด้วยอะไร

`notes_to_chief/20260827_2117_LANE-B-STATUS-bg0002-death-scope-mountain-deer-swap.md` (รอบก่อน
`y7koj9`) ปิดท้ายด้วยช่องโหว่ที่ "แจ้งไว้ ไม่ปิด": `FieldMob.actor_identity` (`0x2000 +
placement_index + 1`) ไม่มีมิติ scene เลย ทำให้ bg0001 กับ Bg0002 ชนกันจริง 4 wire identity (8
มอนต่างกัน) -- นอกเขตเขียนของสายนี้เพราะการแก้จริงต้องแตะ `world_population.py`
(เขตของ chief/สาย A) พอดีกันในรอบเดียวกันนี้ สาย A (`cyp4zt`) ส่ง
`notes_to_chief/20260827_2112_LANE-A-CORE-REQUEST-021-*` ขอให้ chief ต่อสาย login path เข้า
Bg0002 census composer ใหม่จริง -- ทำให้ "ช่องโหว่ที่แจ้งไว้เฉย ๆ" ใกล้จะกลายเป็นของที่ถูกใช้งานจริง
เร็วกว่าที่รอบก่อนคาด นี่คือเหตุผลที่รอบนี้เลือกทำเรื่องนี้ต่อ แทนที่จะปล่อยรอ

grep `notes_to_chief/` และ `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` หา `actor_identity`/
`collision` ก่อนเริ่ม -- ไม่มีใบ CORE-REQUEST/ASK-COO ใดพูดเรื่องนี้ตรง ๆ มาก่อน (มีแต่ prose ใน
docstring `field_mobs.load_roster` กับเทสเดี่ยว `test_bg0001_and_bg0002_actor_identities_are_NOT_
disjoint_a_real_collision`) -- ตรงเงื่อนไขที่ task ข้อ 1 บอกไว้ว่าเป็นผู้สมัครที่ดีของรอบนี้

## 2 ตรวจสายอื่นก่อนเลือก (mob_pickup/inventory ไม่ใช่ของที่ทำได้รอบนี้)

อ่าน `mob_pickup.py` (1770 บรรทัด) + `inventory.py` (524 บรรทัด) เต็มทั้งคู่ก่อนตัดสินใจ:
`dispatch_pickup_request` ต่อสายพร้อมแล้วครบ (`CORE-REQUEST-015` + `CHIEF-REPLY` 15:50) แต่ยังบล็อก
จริงที่ RE opcode decoder ของ inbound pickup (`GT-060`, attended, BLOCKED-CONDITIONAL รอผู้เทส) --
ไม่ใช่ของที่สายนี้ทำต่อได้เอง `inventory.require_known_backpack`'s "THE WALL" (ห้ามขยาย allowlist
จนกว่า M5 ของจริงจะมา) เป็นการตัดสินใจสถาปัตยกรรมที่ตั้งใจแช่ไว้ ไม่ใช่ของที่ค้างเพราะไม่มีคนทำ --
แตะตอนนี้เสี่ยงเปิดกำแพงที่ตั้งใจปิดไว้โดยไม่มีเหตุผลใหม่ RE-111 (loot render fields) ปิด BOUNDED
NEGATIVE ไปแล้วตั้งแต่รอบก่อน ไม่มีอะไรให้ทำต่อแบบ static เลย

## 3 ของที่รอบนี้สร้างจริง: `field_mobs.cross_scene_identity_collisions()`

`pirate-force-server/src/pirateforce_foundation/field_mobs.py`:
- แยก loop parse แถวของ `load_roster` ออกมาเป็น `_parse_hostile_placements(module)` ที่ใช้ร่วมกัน
  (พฤติกรรม `load_roster` เดิมไม่เปลี่ยนแม้แต่บรรทัดเดียว -- แค่ factor)
- `cross_scene_identity_collisions(table_modules=None)` -- ฟังก์ชัน pure วัดทุกคู่ scene ที่ตาราง
  ที่ให้มาชน `placement_index` กัน แล้วรายงาน `actor_identity`/template/ชื่อของทั้งสองฝั่งเป็น dict
  ค่าเริ่มต้น (ไม่ส่ง `table_modules`) = สองฉากที่ `load_roster` โหลดได้จริงวันนี้ (bg0001, Bg0002)
  เท่านั้น -- **ไม่รวม Bg0015 เป็นค่าเริ่มต้นโดยเจตนา**
- `describe_cross_scene_identity_collisions(...)` -- บรรทัดคอนโซล ASCII ล้วน รูปแบบเดียวกับ
  `mob_death.describe_roster_override_coverage`

### 3.1 กับดักที่เจอเองระหว่างทำ (แก้ก่อนส่ง ไม่ใช่ปล่อยให้ pf-adversary เจอ)

ดราฟต์แรก import `field_mob_tables_bg0015` เข้า `field_mobs.py` ตรง ๆ (เพื่อให้ค่าเริ่มต้นครบ 3
ฉาก) -- สวีตเต็มจับได้ทันที: `tests/test_field_mob_tables_bg0015.py`'s
`test_nothing_under_src_imports_the_bg0015_module` (COO-DECISION 2026-08-26T12:46+07:00: ตาราง
ฉากที่สามต้องไม่ถูก import ที่ไหนใต้ `src/pirateforce_foundation/` เลยจนกว่าเกทที่สองของสาย A +
เช็ค geometry จะผ่าน) เกทนี้เดิน AST **และ** กวาดข้อความล้วน (string sweep) ทั้งไฟล์ -- แก้รอบแรก
(เอา `import` ออก) ยังไม่พอ เพราะ docstring/comment ที่พิมพ์ชื่อโมดูลเป็นข้อความล้วนก็ติดเกทเหมือนกัน
(`assertEqual` fail ซ้ำสองครั้งติดกันก่อนแก้ครบ) แก้จริงคือ: เอา literal `field_mob_tables_bg0015`
ออกจาก `field_mobs.py` **ทั้งหมด** (คงเหลือแค่คำว่า "Bg0015" เฉย ๆ ซึ่งเกทนี้ไม่แตะ เพราะสตริงที่ตรวจ
คือชื่อโมดูลเต็ม ไม่ใช่ชื่อฉาก) -- ค่าเริ่มต้นของฟังก์ชันจึงเหลือแค่สองฉาก และเทสของฉากที่สาม (Bg0015)
ทั้งหมดอยู่ใน `tests/test_field_mobs.py` (นอกแพ็กเกจ, import ได้ตามที่เกทอนุญาต) ส่งเป็น
`table_modules=` ชัดเจน ไม่ใช่ค่าเริ่มต้น

## 4 ตัวเลขที่วัดได้จริง (ไม่ใช่ทฤษฎี)

```
bg0001 vs Bg0002: 4 คู่ชน -- placement 58, 59, 60, 95 (identity 0x203B/0x203C/0x203D/0x2060)
bg0001 vs Bg0015: 3 คู่ชน -- placement 30, 59, 63   (identity 0x201F/0x203C/0x2040)
Bg0002 vs Bg0015: 3 คู่ชน -- placement 59, 61, 78   (identity 0x203C/0x203E/0x204F)
รวมทั้งสามฉากที่มีอยู่จริงวันนี้: 10 คู่ชน (เทส test_all_three_known_tables_together_find_ten_
pairwise_collisions ปักไว้)
```

ตัวอย่างที่เป็นรูปธรรม: placement 59 ชนกันทั้งสามฉาก (`bg0001`=Toxic Vine, `Bg0002`=Fighting Fish
soldier, `Bg0015`=Tornado Eagle) -- มอนสามตัวคนละชื่อคนละสถิติ คำนวณ `actor_identity` ออกมาเป็นเลข
เดียวกันหมด (`0x203C`) เป็นตัวอย่างที่ชี้ให้เห็นว่าปัญหาไม่ได้ผูกกับ template_id (31/34/35/103 ตามที่
เคยพูดถึงเรื่อง `WIDENING_RULINGS`) แต่ผูกกับ `placement_index` ตรง ๆ ซึ่งเป็นตัวเลขที่แต่ละฉากออกให้
เองอิสระจากกันโดยสิ้นเชิง

## 5 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | `tests/test_field_mobs.py` เดี่ยว: 33 -> 44 เทส เขียวหมด (`python3 -m unittest tests.test_field_mobs tests.test_field_mob_tables_bg0015 -v`) · สวีตเต็ม (`python3 -m unittest discover -s tests -p "test_*.py"`): ก่อนแตะ = `Ran 3729 tests` / `error=18` (capstone เดิม, `ModuleNotFoundError: No module named 'capstone'`) / `skip=212` / `FAIL=0` -- หลังแตะ = `Ran 3738 tests` / `error=18` (เท่าเดิมเป๊ะ ไฟล์เดิม) / `skip=212` (เท่าเดิมเป๊ะ) / `FAIL=0` -- ส่วนต่าง 9 เทสคือเทสใหม่ทั้งหมดของรอบนี้ ไม่มีเทสเดิมหายหรือแดง |
| **client-observable** | ไม่มี -- ไม่ใช่รอบ attended รอบนี้ไม่แตะ `runtime.py`/`app.py` เลยแม้แต่บรรทัดเดียว |

## 6 `pf-adversary`

Agent tool `pf-adversary` ไม่มีในสภาพแวดล้อมรอบนี้ (ไม่มี Task/Agent tool ให้เรียก) -- ทำเองแทนตามที่
งานอนุญาต: ไล่อ่าน diff ทั้งไฟล์ซ้ำ, ตรวจจุดที่ pf-adversary มักจับได้ในรอบก่อน ๆ ของสายนี้ --
1. **ขอบเขตอำนาจ**: ฟังก์ชันใหม่ทั้งคู่ไม่แตะ `_SCENE_TABLE_MODULES`/`load_roster` เลย ยืนยันด้วยเทส
   `test_bg0015_is_measurable_even_though_load_roster_refuses_it` ที่ยิง `load_roster(scene="Bg0015")`
   แล้วคาดว่าต้อง raise เหมือนเดิม
2. **เกท Bg0015**: จับได้เองตามข้อ 3.1 ข้างบน (ไม่ใช่ปล่อยให้สวีตเต็มจับ) -- รันซ้ำสองรอบยืนยันเขียว
3. **false positive**: เพิ่มเทส `test_two_disjoint_scenes_report_zero_collisions` +
   `test_describe_reports_zero_by_name_not_by_absence` ยิงกับตารางปลอมที่ตั้งใจไม่ให้ชนกัน ยืนยันว่า
   ฟังก์ชันไม่ปั้นผลลวง
4. **ASCII/cp874**: `test_describe_is_ascii_and_carries_the_same_count` เช็ค `line.isascii()` และ
   `line.encode("cp874")` ทุกบรรทัด -- ผ่าน (ชื่อมอนที่ mine มาทั้งหมดเป็นอังกฤษล้วน)
5. **การ dedupe ด้วยชื่อ scene**: ถ้าโมดูลสองตัวประกาศ `SCENE` ซ้ำกันแต่เนื้อหาต่างกัน
   ฟังก์ชันจะเก็บของโมดูลแรกที่เจอเงียบ ๆ (`if scene in rosters: continue`) -- ไม่มีเทสตรงจุดนี้
   บันทึกไว้ตรงนี้เป็น nonclaim แทนที่จะแก้ก่อนมีเหตุผลจริง (ค่าเริ่มต้นของโปรเจกต์ไม่เคยส่งโมดูลชื่อ
   scene ซ้ำเข้ามาเอง)

## 7 จดหมาย: `notes_to_chief/20260827_2153_LANE-B-ASK-COO-actor-identity-needs-a-scene-term.md`

ไม่ตัดสินใจแทน COO (สถาปัตยกรรม wire format ข้ามเลน ตรงเงื่อนไข "กระทบเลนอื่น/ของ chief" ไม่ใช่
กรณีตัดสินแทนได้เอง) แต่เสนอสามตัวเลือกพร้อมข้อดี-ข้อเสียให้เคาะเร็ว ติดป้าย [สมมติของสาย B - รอ COO
ยืนยัน] ที่ทางเลือกแนะนำ (ตัวเลือก 3: ผูก key ด้วย `(scene, actor_identity)` ที่ชั้นเก็บสถานะ
เช่น `DeathRegister`/census override แทนที่จะเปลี่ยนสูตร wire -- ไม่กระทบ pin เดิมของ bg0001 เลย
สักตัว) -- ไม่บล็อกงาน ระบุชัดว่ารอบนี้ไม่เขียนโค้ดแก้จริงเพราะทั้งสามตัวเลือกกระทบ `world_population.py`
(เขต chief/สาย A) อย่างน้อยหนึ่งจุดเสมอ

## 8 ถ้าผิดต้องย้อนอะไรบ้าง

ฟังก์ชันใหม่ทั้งคู่เป็น pure function ที่ไม่มีใครเรียกจาก runtime path ใด ๆ -- ย้อนได้ด้วยการลบสอง
ฟังก์ชัน + เทสที่เพิ่ม ไม่กระทบ `load_roster`/`_parse_hostile_placements` ที่ฟังก์ชันเดิมพึ่งอยู่ (มี
เทสเดิมคุ้มครองอยู่แล้วว่า `load_roster` พฤติกรรมไม่เปลี่ยน)

## 9 รอบถัดไปควรทำอะไร

1. เช็คจดหมายข้อ 7 ก่อนอื่น -- ถ้า COO เคาะทางเลือกมา และ chief/สาย A ต่อสายจริงที่
   `world_population.py`/`mob_death.DeathRegister` แล้ว ให้ยืนยันด้วยสวีตเต็ม
2. ถ้า `LANE-A-CORE-REQUEST-021` ถูกต่อสายจริง (bg0002 login path มีชีวิต) ก่อนจดหมายข้อ 7 ถูกตอบ --
   ยังไม่มีบั๊กที่เห็นจริงทันที เพราะ `DeathRegister` เป็น per-connection (`self.mob_death_register`,
   ผูกกับ session เดียว ไม่ใช่ global) และการข้าม scene ภายในเซสชันเดียว (M2) ยังพักอยู่ -- แต่ถ้า M2
   ถูกปลดพักเมื่อไหร่ ให้ยกจดหมายข้อ 7 ขึ้นมาอ่านก่อนเดินสาย ไม่ใช่หลังเจอบั๊กจากผู้เล่นจริง
3. `BUILD-006` (M5 loot pickup) ยังรอ RE opcode decoder (`GT-060`) เหมือนเดิม ไม่มีอะไรให้สายนี้ทำ
   เพิ่มฝั่ง pure-function จนกว่าจะมีของใหม่จาก attended session

-- **สาย B · COMBAT**
