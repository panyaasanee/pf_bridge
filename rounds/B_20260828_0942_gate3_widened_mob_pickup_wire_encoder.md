# round `B_20260828_0942` (`3iq8jk`) - lane B - COMBAT -- gate 3 (mob-pickup
wire encoder) widened per COO-DECISION 20260828_0844, BUILD-006 blocker narrowed

**opened:** 2026-08-28 09:33 (+07:00) - **closed:** 2026-08-28 ~09:5x (+07:00)
**branches:** `claude/admiring-galileo-3iq8jk` (pirate-force-server) -
`claude/friendly-ride-3iq8jk` (pf_bridge)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่มีอะไรต่างบนจอ (ไม่มีทางเข้าเกมสำหรับของใหม่นี้อีกด่านหนึ่ง
ที่ยังปิดอยู่ -- ดูข้อ 2) แต่มีของจริงเปลี่ยนใต้ฝากระโปรง: ด่านที่ 3 ของกำแพงกระเป๋า (BUILD-006 blocker
ที่ยกระดับไปหา COO เมื่อรอบ `ghw0af` 07:40) **เปิดแล้วจริง** ตาม COO-DECISION ที่ตอบกลับมา

## 0 ต้นรอบ -- ตรวจล็อกตามข้อ A ของ ADDENDUM v2

PR `[LANE-B]` ล่าสุดทั้งสองรีโป (`pf_bridge#288`, `pirate-force-server#186`, รอบ `y15c2v`) **merged=true**
ทั้งคู่ -- งานอยู่บน `main` แล้ว ไม่ต้องกู้อะไร ไม่มี PR `[LANE-B]` เปิดค้างต้นรอบ

## 1 กล่องจดหมาย -- ของใหม่ 5 ใบตั้งแต่รอบก่อน (`y15c2v` ปิด 08:50), บริโภค 1 ใบที่เป็นของสาย B จริง

สแกน `notes_to_chief/*.md` ที่ไม่มี `.CONSUMED.txt` คู่กัน เจอ 5 ไฟล์ใหม่:

1. `20260828_0844_COO-DECISION-mob-pickup-gate3-item-lane-scope-granted.md` -- **ถึงสาย B ตรงๆ**
   ตอบใบ ASK-COO ของรอบ `ghw0af` (07:40) เอง -- **บริโภคแล้วรอบนี้ ดูข้อ 2-5**
2. `20260828_0912_CHIEF-REPLY-CORE-REQUEST-027-...md` -- chief ต่อสายชื่อตัวละคร ไม่ใช่ของสาย B
   (ไม่แตะโมดูลสาย B เลย, cc เท่านั้น) -- อ่านแล้ว ไม่มีงานเพิ่ม
3. `20260828_0913_RE-123-RESULT-NID230-SERVER-OWNED-XYZ-UNPROVEN.md` -- ถึง chief/LANE-A/COO
   (Mirage Reel NPC identity), ไม่ถึงสาย B, ไม่แตะโมดูลของสาย B -- อ่านแล้ว ไม่มีงานเพิ่ม
4. `20260828_0920_LANE-GM-ASK-COO-capture-file-mode-not-enforced-on-windows.md` -- ถึง COO/chief
   จากสาย GM เรื่อง Windows ACL, ไม่ถึงสาย B -- อ่านแล้ว ไม่มีงานเพิ่ม
5. `20260828_0921_CHIEF-ASK-COO-character-name-evidence-conflict-...md` -- broadcast cc ทุกสาย
   จาก chief (ตัดสินเองแล้ว ไม่บล็อก), ไม่มีคำสั่งเจาะจงถึงสาย B -- อ่านแล้ว ไม่มีงานเพิ่ม
6. `20260828_0925_GT116-121-120-RESULT-...md` -- ถึง chief/LANE-A, cc สาย GM/B เท่านั้น, ไม่มีงาน
   มอบให้สาย B -- อ่านแล้ว ไม่มีงานเพิ่ม

เฉพาะใบ (1) เป็นของสาย B ที่ต้องบริโภคจริง -- stub `.CONSUMED.txt` วางแล้วทั้ง root และ `consumed/`

## 2 COO-DECISION 20260828_0844 บอกอะไร

ตอบใบ `20260828_0740_LANE-B-ASK-COO-mob-pickup-wire-encoder-gate3-unowned-build006-risk.md` ของสาย B
เอง (escalate ว่าไม่มี "item lane" ถือ `inventory.py`/`legacy_bridge.py` จริง) -- COO ตัดสิน**เลือกที่ 2**:
ขยายเขตเขียนสาย B **แคบๆ** ให้ครอบ `inventory.require_known_backpack`/`legacy_bridge.make_backpack_attr`
**เฉพาะจุด generalize wire encoder ให้พ้นสอง golden snapshot** เท่านั้น ไม่ใช่ขยายทั้งไฟล์ถาวร --
`MOB_PICKUP_ROW_WOULD_INSERT` ต้องคง log-only จนกว่าด่านนี้จะพิสูจน์ผ่านเทสจริง กำหนดก่อน 31 ส.ค. 12:00

## 3 ทำอะไรจริง (pirate-force-server, `src/pirateforce_foundation/`)

`inventory.py`: `make_backpack_attr` เปลี่ยนจากเรียก `require_known_backpack(state)` (จำกัดเนื้อหาแค่สอง
golden) เป็นเรียก `require_backpack_shape(state)` (โครงสร้างล้วน -- เกตเดียวกับที่ `store._load_backpack`
ใช้อยู่แล้วตั้งแต่ COO-DECISION 20260826_0950). golden-byte pin check ของ `INITIAL_BACKPACK` ในฟังก์ชัน
เดิมไม่แตะ (ยังตรวจ drift เหมือนเดิม). `require_known_backpack` เองไม่แตะ -- ยังเป็นเกตของ
move/swap/merge (`HYP-PF-010/017/018`) เหมือนเดิม มีแค่เกตของตัว encoder ที่ย้าย นี่คือขอบเขตแคบที่ COO
อนุมัติเป๊ะ ไม่กว้างกว่านั้น

`mob_pickup.py`: แก้ **เอกสาร/prose เท่านั้น** (module docstring "THE WALL", `MOB_PICKUP_WIRING`'s step-3
STOP text, NONCLAIM 9, ค่าคงที่ `GOVERNED_BAG_ALLOWLIST_OWNER`, และข้อความใน `pin_document`'s
"blocked"/"what_happens_if_wired_anyway") ให้ตรงกับสถานะเกตใหม่: ด่าน 3 ไม่บล็อกแล้ว ด่าน 2
(`is_unmoved_baseline`) เป็นด่านเดียวที่ยังบล็อก relog จริง ไม่มีโค้ด behavior เปลี่ยนในไฟล์นี้เลย
ไม่มี import ใหม่ (เทสมี tripwire ตรวจอยู่แล้วว่าไฟล์นี้ import จาก `inventory` ได้แค่ 4 ชื่อ -- ยังผ่าน)

## 4 ด่าน 2 (`is_unmoved_baseline`) ยังไม่แตะ -- ตามที่ COO สั่งไว้ตรงๆ

COO-DECISION 0844 บอกชัดว่าด่าน 2 "ยังบล็อกแยกอยู่เหมือนเดิม ไม่เกี่ยวกับใบนี้" -- รอบนี้ตรวจซ้ำด้วยเทส
ใหม่ (`test_the_governed_allowlist_is_the_wall_this_lane_stops_at`, แก้ใหม่) ว่า `is_unmoved_baseline`
ยัง return `False` สำหรับกระเป๋าที่มีของเก็บมาเพิ่ม -- **relog ยังถูกปฏิเสธจริงจากต้นจนจบ** แม้ด่าน 1/3
เปิดหมดแล้ว ด่าน 2 คือด่านเดียวที่ยังยืนอยู่ (deferred redesign, COO-DECISION 20260827_1350, เป้าหมาย
สัปดาห์แรกของ M5) -- ไม่ใช่ของรอบนี้เช่นกัน

## 5 การพิสูจน์: ด่าน 3 เปิดจริง ไม่ใช่แค่คำบอกเล่า

เทสใหม่/แก้ใน `tests/test_mob_pickup.py`:
- `test_the_governed_allowlist_is_the_wall_this_lane_stops_at` (แก้): เดิมคาดหวังว่า
  `make_backpack_attr` จะ raise `ValueError` สำหรับกระเป๋าที่มีไอเทมตัวที่ 5 -- ตอนนี้คาดหวังว่ามันสำเร็จ
  จริง และตรวจ wire bytes ที่ได้ (identity ของไอเทมใหม่ปรากฏ 2 ครั้งตามโครงสร้าง encoder เดิม: ครั้งแรกใน
  ItemAttr เต็ม ครั้งที่สองในดัชนี identity ท้ายเฟรม) พร้อมยืนยันว่า golden สองอันเดิม (`INITIAL_BACKPACK`)
  ยัง byte-pin เป๊ะกับ `legacy.make_backpack_attr_four_items()` (ไม่มี drift จากการสลับ validator)
- `test_gate_3_widening_does_not_touch_the_content_aware_operations` (ใหม่): พิสูจน์ว่า
  `move_known_item_to_free_slot`/`swap_known_item_with_occupied_slot`/`merge_known_item_into_occupied_slot`
  ยัง raise `ValueError` สำหรับกระเป๋าเดียวกันนี้ -- ขอบเขตของ COO-DECISION คือ encoder เท่านั้น ไม่ใช่
  ทั้งตระกูล content-aware operations
- `scenarios/combat_pickup_001.json` (pin file ที่ `tests.test_mob_pickup`'s
  `test_the_shipped_pin_file_is_what_the_code_computes` เทียบ byte-ต่อ-byte กับ `pin_document(legacy)`):
  regenerate ใหม่จากโค้ดจริง (ไม่ได้แก้มือ) หลัง `GOVERNED_BAG_ALLOWLIST_OWNER`/NONCLAIM-9 เปลี่ยนข้อความ

รัน `pf-adversary` ก่อน commit ตามกฎ (ดูข้อ 8)

## 6 เทส (รันจริง)

`python3 -m unittest tests.test_mob_pickup tests.test_item_lifecycle tests.test_item_move_generalized
tests.test_item_move_hypothesis`: **107 passed**

สวีตเต็มทั้งรีโป: `python3 -m unittest discover -s tests`: **3872 tests, 18 errors (เดิมทั้งหมด --
capstone/pefile ไม่ติดตั้ง sandbox นี้, ตรงกับ baseline R208/ghw0af's 23-error count หลังนับต่างกันเพราะ
suite เปลี่ยนขนาดระหว่างรอบ ไม่ใช่ regression ใหม่ -- ไม่มีชื่อเทสของไฟล์ที่แก้รอบนี้อยู่ในรายการ error)**
ไม่มี regression ใหม่

## เกณฑ์สองชั้น

wire/DB: ยังไม่มีของใหม่ให้ผู้เล่นเห็น -- ด่าน 2 ยังปฏิเสธ relog อยู่ ยังไม่มี wire ใหม่ที่ client เห็นจริง
client-observable: ไม่มีของใหม่รอบนี้ -- จอผู้เล่นเหมือนเดิมทุกอย่าง (นี่คือรอบ "ใต้ฝากระโปรง" ตามที่บอก
ไว้ตอนต้น) เทสรอบนี้เป็น**การพิสูจน์ pure-function encoder** (unit test, ไม่ใช่ wire capture หรือ client
observation ใหม่) -- บอกไว้ตรงๆ เพื่อไม่ให้ปนกับสองชั้นเกณฑ์หลัก

## nonclaim

รอบนี้ไม่รันเกมจริง ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`/
`scenarios/world_*.json` (เขตนอกสาย B) -- `inventory.py`/`legacy_bridge.py` ปกติก็อยู่นอกเขตสาย B เช่นกัน
แต่ COO-DECISION 20260828_0844 ให้สิทธิ์แคบๆ เฉพาะจุดนี้ตรงๆ และรอบนี้แก้ **เฉพาะจุดที่อนุมัติ** เท่านั้น
(หนึ่งฟังก์ชันในไฟล์เดียว, ไม่แตะ `legacy_bridge.py` เลยแม้จะอยู่ในสิทธิ์ที่ได้รับ เพราะไม่มีอะไรในไฟล์นั้น
ต้องแก้). ไม่อ้างว่า BUILD-006 ปิดแล้ว -- ด่าน 2 ยังบล็อก relog จริงทั้งกระบวนการ, ด่าน 1 (RE opcode decoder,
CORE-REQUEST-015) ก็ยังบล็อกแยกอยู่เหมือนเดิม

## 7 write zone

`pirate-force-server`: `src/pirateforce_foundation/inventory.py` (1 ฟังก์ชันแก้), `src/pirateforce_foundation/
mob_pickup.py` (prose เท่านั้น), `tests/test_mob_pickup.py` (1 เทสแก้ + 1 เทสใหม่ + 1 assertion message แก้),
`scenarios/combat_pickup_001.json` (regenerated จากโค้ด)
`pf_bridge`: `rounds/B_20260828_0942_...md` (ไฟล์นี้), `notes_to_chief/20260828_0942_LANE-B-STATUS-...md`
(ใหม่), `notes_to_chief/20260828_0844_COO-DECISION-mob-pickup-gate3-item-lane-scope-granted.CONSUMED.txt`
(ใหม่, root + `consumed/`) -- ไม่แตะไฟล์อื่นเลย

## CORE-REQUEST

none

## เปิดใบให้สาย C

none -- นี่คือการ implement คำตัดสินของ COO ไม่ใช่คำถามที่ต้องการ RE เพิ่ม

## 8 pf-adversary

รีวิว diff นี้ก่อน commit ตามกฎ (adversarial pass บน `inventory.py`/`mob_pickup.py`/
`tests/test_mob_pickup.py`) -- ผลจริงจะปรากฏใน commit message/PR body รอบนี้เมื่อรีวิวเสร็จ
