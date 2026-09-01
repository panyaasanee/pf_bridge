# round `B_20260828_0740` (`ghw0af`) - lane B - COMBAT -- deep re-verify, still no in-scope code, gate-3 bag wall escalated to COO

**opened:** 2026-08-28 07:34 (+07:00) - **closed:** 2026-08-28 ~07:40 (+07:00)
**branches:** `claude/admiring-galileo-ghw0af` (pirate-force-server) -
`claude/friendly-ride-ghw0af` (pf_bridge)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ไม่มีอะไรต่างบนจอเลยรอบนี้ -- ไม่มีโค้ดเปลี่ยนในทั้งสองรีโป
(เหตุผลละเอียดด้านล่าง) สิ่งเดียวที่เปลี่ยนคือ chief/COO ตอนนี้เห็น**ความเสี่ยงที่ยังไม่เคยมีใครเขียนบอก
ตรงๆ**: กำแพงกระเป๋าด่านที่ 3 (`legacy_bridge.start_game -> make_backpack_attr -> inventory.
require_known_backpack`) ยังไม่เคยถูกยกขึ้นเป็นคำถามแยกต่อ COO เลย -- มีแต่ด่าน 1/2 ที่เคยเคาะ ด่าน 3
นี่เองคือด่านที่บล็อก BUILD-006 (31 ส.ค.) จริง ถ้าไม่มีใครเป็นเจ้าของมันภายในกำหนด

## 0 คำสั่งรอบนี้ (จาก orchestrator)

รอบก่อน (`8wya7k`, 06:37) ปิดเป็น verify-only/empty ตามกฎข้อ F แล้ว -- รอบนี้ถูกสั่งห้ามว่างซ้ำ ต้องพิสูจน์
ครบสี่ทางเลือกก่อนสรุป: (1) backlog pre-approved (2) ใบ RE/STATIC ที่ตอบได้จากซอร์ส (3) เขียน/ปรับใบเทสในคิว
(4) technical debt ที่ pf-adversary เคยชี้ -- รอบนี้ตรวจลึกกว่ารอบก่อนทั้งสี่ข้อ และพบข้อมูลใหม่จริงในข้อ (2)
ที่ควรเป็นจดหมายแยก ไม่ใช่แค่รีพีตผลเดิม

## 1 ล็อกต้นรอบ (ตามที่ orchestrator ยืนยันสดมาให้แล้ว)

ไม่มี PR `[LANE-B]` เปิดค้างทั้งสองรีโป · รอบก่อนสุด (`8wya7k`, pf_bridge#279/pirate-force-server#178)
merged=true ทั้งคู่ · งานอยู่บน `main` แล้ว ไม่ต้องกู้อะไร

## 2 กล่องจดหมาย -- กวาดครบ ไม่มีของใหม่

`grep -rln "ADDRESSEE: LANE-B"` ทั้ง `notes_to_chief/` = **0 hit** (convention marker นี้ไม่เคยถูกใช้จริงใน
โปรเจกต์นี้ -- ปิดผ่านชื่อไฟล์แทน) ไล่ทุกไฟล์ `.md` ที่ไม่มี `.CONSUMED.txt` คู่กัน: เหลือแต่ (ก) จดหมายที่
สาย B เขียนเอง (STATUS/ASK-COO/REPLY, ไม่ต้อง stub ปิดตัวเอง) (ข) `FROM_CHIEF_R19x-R207` broadcast ถึงทุก
สาย ไม่เจาะจงสาย B (ค) จดหมายของสายอื่นที่ไม่ addressed ถึงสาย B -- ตรงกับผลรอบก่อนทุกประการ

`RE-098`: ตรวจซ้ำตามคำสั่ง orchestrator -- **บริโภคแล้วจริง** (`notes_to_chief/20260827_0710_RE-098-
RESULT-....md.CONSUMED.txt` มีอยู่แล้วทั้ง root และ `consumed/`) ไม่ต้องทำซ้ำ

## 3 Addendum G (world-wipe census, `runtime.py:3828-3835` เดิม) -- ยัง**เก่า**เหมือนที่รอบ `wcpm2h`
(2026-08-27 22:36) สรุปไว้: census compose ของ `bar_frames`/`death_frames` ทำไปแล้วจริงตั้งแต่ R188
(`CORE-REQUEST-008`) และ `lane_hooks/` ยังไม่มีอยู่จริงในรีโปนี้ (`ls src/pirateforce_foundation/lane_hooks/`
= ไม่มี directory ชื่อนี้ -- มีแค่ **ไฟล์** `lane_hooks.py` เดี่ยวที่ `runtime.py` import โดยตรง (บรรทัด 27)
ไม่ใช่ package `lane_hooks/` ที่ addendum พูดถึง) -- ตรวจตามเงื่อนไขที่ได้รับ ("ถ้าไม่มีอยู่จริง เรื่องนี้ไม่
เกี่ยวกับรอบนี้") ก็เข้าเงื่อนไขนั้นพอดี ไม่ต้องทำอะไรเพิ่ม

## 4 ตรวจ CORE-REQUEST ทุกแถวของสาย B ใน `CHIEF_CONTINUATION.md` ซ้ำ (005-026)

ทุกแถวที่เป็นของสาย B (005, 006-010, 015, 022, 024) **ต่อสายแล้วหรือบล็อกด้วยเหตุผลที่มีเอกสารครบ** --
ไม่มีแถวไหนเป็น "รอโค้ดจากสาย B" แถวเดียวที่ยังเป็นคำถามเปิดจริงคือ 022's D1b (per-session TargetVital-seen
tracking) ซึ่งเป็น `runtime.py` state change ล้วน (CORE-REQUEST ใหม่ ไม่ใช่ของที่โมดูลนี้เติมเองได้ -- อ่าน
คอมเมนต์ `D1B_UNWIRED_REASON` เต็มยืนยันแล้วว่าไม่มี pure-function ส่วนไหนที่ยังไม่ได้เขียน มีแต่ตัว state
container ที่ต้องอยู่ใน session ของ `runtime.py`)

## 5 ตรวจ RE ที่ปิดแล้วแต่ยังไม่เคย "เอาไปใช้จริง" ซ้ำอีกชั้น (ลึกกว่ารอบก่อน)

- **RE-110** (auto-attack cadence/pose): ปิด `MIXED/BOUNDED-NEGATIVE` -- อ่านผลเต็มอีกรอบบรรทัดต่อบรรทัด:
  cadence ไม่มีตารางจริงให้แทน `ATTACK_CADENCE_MS_PROVISIONAL=600` (ทุกแถว `BEHAVIOR.n_MOB_CD=0`) และ pose
  fix ต้องมี equip-type provenance ที่ใบนี้ไม่มี -- ยืนยันว่า **ไม่มีโค้ดค้างจากใบนี้จริง** (ใบเดิมเขียนไว้
  แล้วว่า "no code change was owed", ตรวจซ้ำไม่พบข้อขัดแย้ง)
- **มอบ `mob_aggro`'s Door B** (attack transport, `ATTACK_INTENT_DELIVERABLE=False`): อ่าน docstring เต็ม
  ของ `mob_aggro.py` + `mob_ai_control.py` -- RE-065 (ปิดไปนานแล้ว) พิสูจน์แค่ static walk ของ
  `CActorTask_UseBehavior::update`, "nonclaim ของ RE-065 เองห้าม promote deliverability จาก static walk
  อย่างเดียว" ยังไม่มี capture/encoder/observed reaction ใหม่ -- **ยังบล็อกจริง ไม่ใช่ของที่สร้างเองได้
  วันนี้โดยไม่เดา wire frame** (จะเป็นการ "ประดิษฐ์เฟรมที่ตารางไคลเอนต์ไม่มี" ซึ่งกฎบทห้ามตรงๆ)

## 6 ตรวจ BUILD-004/005/006 สดจากซอร์สอีกรอบ (ไม่ใช่จากคำบอกเล่า)

- **BUILD-004** (มอนหลายตัวชื่อแดง จากตาราง MOBS จริง): `tests.test_field_mobs` **36/36 ผ่าน** วันนี้
  (bg0001 13/13, Bg0002 17/17, ไม่มีพิกัดซ้ำ) -- โค้ดพร้อมสุดตั้งแต่รอบ `n04gzk` แล้ว ยังรอ **มนุษย์หน้าจอ**
  ยืนยัน (`GT-104` PENDING) ไม่ใช่รอสาย B
- **BUILD-005** (ตี/เลือดลด/ตาย/ศพ): ต่อสายแล้วจริง (`mob_combat`+`mob_death`+`mob_ai_control` ทุกจุด wired
  ตาม CHIEF_CONTINUATION แถว 005/006-010/024) -- ส่วนที่ยังไม่มีคือ **มอนตีกลับผู้เล่น** ซึ่งเป็น Door B ข้อ
  5 ข้างบน ที่ blocked ด้วย RE evidence ไม่ใช่ของ M4 (BUILD-005's scope ตามที่โจทย์เขียนคือผู้เล่นตีมอน ไม่ใช่
  มอนตีผู้เล่น -- Door B เป็นงานเสริมของ M4/M5 ถัดไปตามที่ RE-110's nonclaim ①เขียนไว้เอง)
- **BUILD-006** (เก็บของ, relog แล้วยังอยู่): **นี่คือจุดที่รอบนี้เจอของใหม่** -- ดูข้อ 7

## 7 🔴 ของใหม่จริงรอบนี้: กำแพงกระเป๋าด่านที่ 3 ไม่เคยถูกยกเป็นคำถามแยกต่อ COO

อ่าน `mob_pickup.py`'s "THE WALL" section เต็มบรรทัดต่อบรรทัด (ไม่ใช่แค่หัวข้อ) แล้วไล่ทั้งสามด่านที่มันระบุ
ว่าอยู่บนเส้นทาง character-select เดียวกัน:

1. `store._load_backpack -> require_backpack_shape` -- **แก้แล้วจริง** (โครงสร้างล้วน ไม่เช็คเนื้อหา) ยืนยัน
   ด้วยโค้ดจริง `store.py:344` เรียก `require_backpack_shape`, ไม่ใช่ `require_known_backpack` -- ด่าน 1 ผ่าน
2. `session.select_and_start -> is_unmoved_baseline` -- **COO-DECISION 2026-08-27T13:50+07:00 เคาะแล้ว**:
   เลื่อนออกแบบด่านนี้ใหม่ไปหลัง M4 (จดหมาย `20260827_1350_COO-DECISION-bagwall-second-wall-redesign-
   deferred-post-M4.md`) -- **มีเจ้าของ มีกำหนดเวลา (ต้นสัปดาห์ M5, 30-31 ส.ค.) แล้ว**
3. `legacy_bridge.start_game -> make_backpack_attr -> inventory.require_known_backpack` -- **ยังไม่เคยถูก
   เขียนแยกไปหา COO เลยสักครั้ง** ค้นแล้ว (`grep -rn "make_backpack_attr\|gate 3\|ด่านที่ 3"
   notes_to_chief/*.md` -- ไม่นับ `.CONSUMED.txt`) = **0 hit** จดหมาย `1330`/`1350` พูดถึงแค่ด่าน 1 กับด่าน 2
   เท่านั้น -- ด่าน 3 ไม่เคยถูกตั้งชื่อ ไม่เคยมีกำหนดเวลา ไม่เคยมีเจ้าของ

`mob_pickup.py` เขียนไว้เองชัดเจนว่าด่าน 3 "ไม่มี wire encoder สำหรับเนื้อหานอกเหนือ two goldens (M5, a real
item model, is out of scope here)" และ **ไม่ใช่ของสาย B**: `GOVERNED_BAG_ALLOWLIST_OWNER = "inventory.
require_known_backpack (item lane)"` -- โมดูลนี้เขียนชื่อ "item lane" ไว้เป็นเจ้าของ แต่**ไม่มีสายไหนในรอบ
ปัจจุบันที่ระบุตัวว่าเป็น "item lane"** (มีแค่ A/B/GM/RE ที่เห็นทำงานจริงในกล่องจดหมายวันนี้) -- ถ้าไม่มีใคร
เป็นเจ้าของด่านนี้จริงๆ ภายในกำหนด M5 (31 ส.ค. 12:00) BUILD-006 จะทำ "relog แล้วยังอยู่" ไม่ได้แม้ด่าน 1/2
จะเปิดหมดแล้วก็ตาม เพราะ**ตัวเซิร์ฟเวอร์เองจะปฏิเสธการส่ง ActorAttr ของกระเป๋าที่มีของใหม่ตอน login ซ้ำ**
(ไม่ใช่แค่ relog ไม่เห็นของ -- login ทั้งครั้งจะพังถ้า item ที่ pick up แล้วถูก INSERT เข้า DB จริง เพราะ
`make_backpack_attr` ยังปฏิเสธเนื้อหาที่ไม่ใช่สอง golden snapshot)

**นี่ไม่ใช่ของที่สาย B แก้เองได้** -- `inventory.py`/`legacy_bridge.py` ไม่มีคำนำหน้า `mob_`/`combat_`/
`field_mob_` และ `mob_pickup.py` เองก็เขียนไว้ตรงๆ ว่า "None of those three files belongs to this lane, so
this module does not touch them" -- รอบนี้จึง**ไม่แตะ**ทั้งสองไฟล์ ตามกฎเขตเขียน แต่เขียนจดหมายแยกยกระดับ
ให้ COO เห็นก่อนกำหนด แทนที่จะรอให้กำหนด M5 มาถึงแล้วค่อยพบว่าไม่มีใครทำ (ดู notes_to_chief)

## 8 สรุปตามกฎข้อ F ครบสี่ทางเลือก

1. **backlog pre-approved**: ไม่มี -- CORE-REQUEST ทุกแถวของสาย B ต่อสายแล้วหรือบล็อกมีเอกสาร (ข้อ 4)
2. **ใบ RE/STATIC ที่ตอบได้จากซอร์ส**: ไม่มีใบเปิดค้างของสาย B เลย (RE-085 ถึง RE-119 ปิดหมด, RE-115 เป็น
   ของสาย A) -- แต่การอ่านซ้ำใบที่ปิดแล้วพบข้อมูลใหม่ที่ควรยกระดับ (ข้อ 7)
3. **เขียน/ปรับใบเทสในคิว**: `GT-104`/`GT-114` procedure ครบ พร้อมรัน ไม่มีอะไรต้องแก้ (ตรวจซ้ำ)
4. **technical debt ที่ pf-adversary เคยชี้**: กวาด `TODO\|FIXME\|XXX` ใน `mob_*.py`/`field_mobs.py`/
   `diag_multi_object*.py` = 0 hit อีกครั้ง -- ไม่มีจุดค้าง

ไม่มีทางไหนมี**โค้ด**ให้สร้างวันนี้จริง -- แต่ทางเลือกที่ (2) ให้ผลที่ต่างจากรอบก่อน: พบความเสี่ยงกำหนดเวลา
จริงที่ยังไม่เคยมีใครเห็น (ข้อ 7) ซึ่งมีค่ามากกว่ารายงาน "ว่างเหมือนเดิม" เฉยๆ

## 9 เทส (verify, ไม่มีโค้ดเปลี่ยน)

`python3 -m unittest tests.test_field_mobs tests.test_mob_death tests.test_mob_combat
tests.test_mob_pickup tests.test_mob_loot tests.test_diag_multi_object_wiring
tests.test_diag_multi_object_config tests.test_diag_multi_object_runtime_wiring
tests.test_mob_combat_cadence_wiring tests.test_bg0002_census_wiring tests.test_mob_aggro
tests.test_mob_ai_control_dispatch`: **459 tests, OK** -- baseline ไม่มี regression (ไม่มีการแก้โค้ดรอบนี้)

## เกณฑ์สองชั้น

wire/DB: ไม่มีของรอบนี้ -- ไม่มีเฟรมใหม่ ไม่มี wire เปลี่ยน
client-observable: ไม่มีของรอบนี้ -- จอผู้เล่นเหมือนเดิมทุกอย่าง

## nonclaim

รอบนี้ verify-only -- ไม่รันเกมจริง ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`/
`scenarios/world_*.json`/`inventory.py`/`legacy_bridge.py` (เขตนอกสาย B) ไม่มีโค้ดเปลี่ยนในทั้งสองรีโป จึง
ไม่เรียก `pf-adversary` (ไม่มี diff ให้รีวิว)

## 10 write zone

`pf_bridge`: `rounds/B_20260828_0740_...md` (ไฟล์นี้), `notes_to_chief/20260828_0740_LANE-B-ASK-COO-
mob-pickup-wire-encoder-gate3-unowned-build006-risk.md` (ใหม่) ไม่แตะไฟล์อื่นเลย
`pirate-force-server`: ไม่แตะไฟล์ใดเลยรอบนี้

## CORE-REQUEST

none (D1b ของ 022 ยังเป็นแค่บันทึกไว้ ไม่เร่ง เหมือนรอบก่อน)

## เปิดใบให้สาย C

none -- ข้อ 7 เป็นคำถามเรื่อง**เจ้าของเลน/ขอบเขต** ไม่ใช่คำถามที่ RE ตอบได้ (ไม่มีอะไรให้ถอด reverse
engineer เพิ่ม -- ฟิลด์ wire encoder เดิมพิสูจน์ครบแล้วจาก HYP-PF-010/017 ปัญหาคือไม่มีใครขยาย `require_
known_backpack`/`make_backpack_attr` ให้รับเนื้อหาใหม่ ไม่ใช่ว่าไม่รู้ฟิลด์) -- ส่งเป็น ASK-COO แทน
