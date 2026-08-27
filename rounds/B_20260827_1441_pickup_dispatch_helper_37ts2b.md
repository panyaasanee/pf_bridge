# round `B_20260827_1441` (`37ts2b`) · lane B · COMBAT -- `dispatch_pickup_request()`
collapses the pickup wiring recipe into one call, pf-adversary closes a
real test-pinning hole in it

**opened:** 2026-08-27T14:41+07:00 · **closed:** 2026-08-27T15:14+07:00
**branches:** `claude/friendly-ride-uradhe` (pf_bridge, PR #206) ·
`claude/admiring-galileo-uradhe` (pirate-force-server, PR #125)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่มีอะไรเปลี่ยนบนหน้าจอวันนี้ -- โมดูล
`mob_pickup.py` ยังไม่ถูกเรียกจากที่ไหนในโค้ดจริงเลย (`runtime.py` เป็นของ
chief) รอบนี้ทำให้จุดที่ chief ต้องต่อสายเหลือแค่เรียกฟังก์ชันเดียวแทนที่จะประกอบ
4 ขั้นตอนเอง ผลที่ผู้เล่นเห็นได้จะมาถึงก็ต่อเมื่อ chief ต่อสายบรรทัดนั้นใน
`runtime.py` แล้ว (ของหล่น -> เก็บ -> เข้ากระเป๋า, ยกเว้นการ persist ที่ยังติด
THE WALL เดิม)

## 1 ล็อกต้นรอบ

0 ใบ `[LANE-B]` เปิดค้างทั้งสองรีโปก่อนรอบนี้ (`list_pull_requests` +
`pull_request_read` method `get` เพื่อเลี่ยง known false-negative ของฟิลด์
`merged` -- ดู `notes_to_chief/20260827_1936_LANE-GM-ASK-COO-list-pull-requests-merged-field-false-negative.md`)
ใบล่าสุดของสาย B (`pf_bridge#200` / `pirate-force-server#119`, round
`s7hjdb`) ทั้งคู่ `merged=true` จริง (ยืนยันด้วย `pull_request_read`,
ไม่ใช่แค่ `list_pull_requests` ที่รายงาน `merged=false` ผิด) -- งานอยู่บน
`main` แล้ว ไม่ต้องกู้คืนตามข้อ A ของ ADDENDUM v2

ยึดล็อกด้วย draft PR `pf_bridge#206` (`14:41:0x +07:00`) และ
`pirate-force-server#125` (`14:5x +07:00`)

## 2 มลบ็อกซ์

ไม่มีใบ `ADDRESSEE: LANE-B` ค้างรอบนี้ (`grep` ทั้ง `notes_to_chief/`)
`RE-098` ที่ ADDENDUM v2 หมวด B ระบุว่าเป็นของค้างของสาย B ถูกปิด/archive
ไปแล้วตั้งแต่ก่อนรอบนี้ (`CLIENT_RE_QUEUE.md:235`, ย้ายไป
`archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`) -- ไม่มีอะไรให้บริโภค

## 3 อ่านก่อนเขียน -- สถานะ BUILD-004/005/006 ก่อนเริ่ม

อ่าน `rounds/B_20260827_1349_real_arrival_census_recompose_proof.md` §11
(รอบก่อนหน้า) + จดหมาย `CHIEF-REPLY 1700` (`WIRED v2` board) ก่อนเริ่ม:

- `BUILD-004` (28 ส.ค. 12:00): เสร็จแล้ว จริงจากตาราง MOBS, wired
  unconditional, ไม่มีความเสี่ยงใหม่
- `BUILD-005` (29 ส.ค. 23:59): `0x201F` ตายได้จริง `combat_aggro` ยังเป็น
  ❌ **โดยตั้งใจ** ตาม `COO-DECISION 20260826_0402` (ขึ้น production พร้อม
  M4 ครึ่งหลัง ไม่ใช่ของค้าง) `mob_aggro.py` เขียนสมบูรณ์แล้ว
  (`production_allowed = True`) รอ chief ต่อสายเข้า tick loop
- `BUILD-006` (31 ส.ค. 12:00): ครึ่งแรก (`mob_loot`) เสร็จ ครึ่งหลัง
  (`mob_pickup`) เขียนสมบูรณ์ในเขตเขียนสายนี้แต่ **ไม่มีจุดเรียกเลยสักจุด**
  จดหมาย `CHIEF-REPLY 1700` บอกตรงๆ ว่า combat_pickup ยังเป็น "THE WALL"
  และไม่มี CORE-REQUEST ใหม่จากสาย B ขอเรื่องนี้ -- รอสายเขียนใบถ้าต้องการ
  **นี่คือช่องที่รอบนี้เลือกทำ**

## 4 ของที่รอบนี้เขียน -- สองคอมมิต, สองรอบ `pf-adversary`

### 4.1 คอมมิต `833601b` -- `dispatch_pickup_request()` + `bag_row_write_console_line()`

`MOB_PICKUP_WIRING` (docstring ของ `mob_pickup.py`) บอก chief มาตั้งแต่ก่อน
รอบนี้ว่าต้องประกอบ 4 ขั้นตอนเองตอนต่อสาย inbound pickup request: สร้าง
`PickupClaim`, เรียก `bag_cell.commit_pickup(...)`, **ห้าม** persist
`outcome.row_write` จริง (ติด THE WALL -- เลนไอเทมยังไม่ขยาย
`inventory.require_known_backpack`) แค่ log ว่าจะ insert อะไร, แล้วส่ง
`outcome.delta` รอบนี้รวบ 4 ขั้นตอนนั้นเป็นฟังก์ชันเดียว:
`dispatch_pickup_request(bag_cell, ledger_cell, legacy, claimant_identity,
x, y, z, object_ref_u32, opaque_u8=0)` -- สร้าง claim, เรียก
`commit_pickup`, ปล่อย `MobPickupContractError` ผ่านไม่ครอบ, พิมพ์บรรทัด
คอนโซล ASCII (`bag_row_write_console_line`) แทนการ persist, คืน
`outcome` เดิม ไม่มีแฟล็ก ไม่มี scenario id ไม่แตะ `runtime.py`/`app.py`/
`pf_login_game_server_v141.py`/`scenarios/world_*.json` เลยสักบรรทัด
อัปเดต `MOB_PICKUP_WIRING` ให้บอก chief เรียกฟังก์ชันเดียวนี้แทนขั้นตอน
1/2/3(log-only)/4 เดิม (ขั้น 0 -- claim ตอน character select -- เหมือนเดิม
ไม่แตะ) เทสใหม่ 4 ตัว, สวีตไฟล์นี้ 66 -> 70, สวีตเต็ม +4 ไม่มี FAIL ใหม่
มิวเทชัน 2 แบบยืนยันเทสจับได้จริง (ครอบ exception, ครอบการ log)

### 4.2 คอมมิต `c9ceeaa` -- `pf-adversary` (agent อิสระ) พบข้อบกพร่องจริง 1 จุด แก้แล้ว

ส่งให้ agent อิสระตรวจ diff `833601b` แยกจากตัวเองก่อน พบ:

**(ยืนยันจริง, MEDIUM, แก้แล้ว):** `dispatch_pickup_request` เขียน
docstring อ้างว่าบรรทัดตัวอย่างที่ chief ต้องเรียก "ถูกเทสเดินผ่านแล้ว"
(อ้าง `test_the_wiring_line_this_lane_hands_the_chief_actually_runs`) --
แต่เทสนั้นเดินแค่สูตร 4 ขั้นตอนเดิมที่ถูกแทนที่ไปแล้ว ไม่เคยเรียกบรรทัดใหม่
headline call เลย agent พิสูจน์ด้วยการสลับลำดับ argument
`drop_ledger_cell`/`legacy` ในสตริงตัวอย่างจริง แล้วรันสวีตทั้งชุด --
**เขียว 70/70 เหมือนเดิม** นี่คือช่องเดียวกับที่ทั้งโมดูลนี้อ้างว่าออกแบบมา
เพื่อกันไว้ (docstring drift ที่ไม่มีเทสจับ) แต่กลับเปิดอยู่ในโค้ดที่รอบนี้
เพิ่งเขียนเอง แก้โดยแยก headline call เป็นค่าคงที่
`MOB_PICKUP_DISPATCH_HEADLINE_CALL` ที่ `MOB_PICKUP_WIRING` ประกอบขึ้นจาก
มัน เทสใหม่ยืนยันสองชั้น: string ปรากฏตรงเป๊ะใน `MOB_PICKUP_WIRING` จริง
**และ** `exec` สตริงนั้นกับ fixture จริงพิสูจน์ว่ารันได้จริง มิวเทชันซ้ำ
แบบเดียวกับที่ agent ทำ (สลับ argument) -> เทสใหม่ล้มทันที (เทสเก่ายังเขียว
เหมือนเดิม พิสูจน์ว่าเทสเก่าอย่างเดียวจะพลาดช่องนี้จริง) revert แล้วรันซ้ำ
เขียว

**(nit ในเทสของรอบนี้เอง, แก้แล้ว):** เทส
`test_dispatch_pickup_request_needs_the_callers_own_typed_bag_cell` ตั้งชื่อ
อ้างเกินสิ่งที่พิสูจน์จริง (อ้างว่าเช็ก "เจ้าของ" `bag_cell` แต่พิสูจน์แค่เช็ก
type) เปลี่ยนชื่อเป็น `test_dispatch_pickup_request_refuses_a_non_bagcell_type`
และแก้ docstring ให้ตรงกับที่พิสูจน์จริง

**(ช่องว่างที่พบ ไม่บล็อกรอบนี้ เป็นของเดิมไม่ใช่ regression):**
`dispatch_pickup_request` ไม่ได้ผูก `bag_cell` เข้ากับ connection ที่
`claimant_identity` มาจริง -- ส่ง `bag_cell` ของคนละ character กับ
`claimant_identity` เข้าไปก็ผ่านเงียบๆ (สืบทอดจาก `BagCell.commit_pickup`
เดิม ไม่ใช่โค้ดที่รอบนี้เขียน ไม่ใช่ regression) บันทึกเป็น `NONCLAIM 15
[OPEN RISK, NOT MEASURED]` ในไฟล์ ไม่แก้รอบนี้ (ต้องออกแบบใหม่ ใหญ่กว่า
ขอบเขต) -- **คำถามเปิดถึง COO/chief:** ตอน `runtime.py` ต่อสายจริง ใครมี
หน้าที่ยืนยันว่า `bag_cell` ที่ส่งเข้ามาเป็นของ connection เดียวกับที่ถอด
`claimant_identity` มา -- `runtime.py` เอง หรือควรมี defense-in-depth ที่
`mob_pickup.py` ด้วย

## 5 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | `tests/test_mob_pickup.py`: 66 -> 70 -> **71/71** (คอมมิตที่สอง +1) · สวีตเต็มอิสระ: 3410 -> 3414 -> **3415 passed / 327 skipped**, 0 FAIL ใหม่ทั้งสองคอมมิต · มิวเทชันเทส 3 แบบ (ครอบ exception, ครอบ log, สลับ argument headline call) ยืนยันจับได้จริงทุกแบบ ไม่ vacuous · `grep` ยืนยันสด: ไม่มีบรรทัดไหนที่ persist `outcome.row_write` เป็น INSERT จริง, ไม่มี import ที่แตะ store/DB/socket ในฟังก์ชันใหม่ |
| **client-observable** | ไม่มี -- รอบนี้ไม่ใช่รอบ attended, ไม่มีจุดเรียกจาก `runtime.py` เลย ผู้เล่นยังไม่เห็นอะไรเปลี่ยน (ตามที่บอกไว้ตอนต้น) |

## 6 ถ้าผิดต้องย้อนอะไรบ้าง

สองคอมมิตใน `pirate-force-server` แตะ `mob_pickup.py` +
`tests/test_mob_pickup.py` + `scenarios/combat_pickup_001.json` (pin file
ของโมดูลเดียวกัน) เท่านั้น ไม่มีบรรทัด `runtime.py`/`app.py` เปลี่ยนเลย:
`git revert c9ceeaa 833601b` (ลำดับจากล่าสุด) ปลอดภัย -- ไม่มีจุดเรียกจาก
production path ใดๆ ทั้งสองคอมมิตเป็นโค้ดที่ยังไม่ถูกเรียกจากที่ไหนเลยจนกว่า
chief จะต่อสาย

## 7 CORE-REQUEST ถึง chief (ไม่บล็อกรอบนี้)

ต่อสาย inbound pickup request (opcode/decoder เป็นหน้าที่ chief/สาย RE หา)
เข้า `mob_pickup.dispatch_pickup_request(bag_cell, ledger_cell, legacy,
claimant_identity, x, y, z, object_ref_u32, opaque_u8)` ที่ `runtime.py`
บรรทัดเดียว (ขั้น 0 -- `registry.claim` ตอน character select -- ต่อสายอยู่
แล้วก่อนรอบนี้ ไม่ต้องแตะ) แล้วส่ง `outcome.delta` ให้ claimant -- ดูโค้ด
ตัวอย่างที่รันได้จริงและถูกเทสปักไว้ที่ `MOB_PICKUP_DISPATCH_HEADLINE_CALL`
ใน `mob_pickup.py` (อย่า derive เอง ใช้สตริงนั้นตรงๆ กันสลับ argument)

## 8 รอบถัดไปควรทำอะไร

1. เช็คว่า chief ต่อสาย `dispatch_pickup_request` เข้า `runtime.py` แล้ว
   หรือยัง (§7) -- ถ้าต่อแล้ว ต้องมี opcode decoder จริงมาก่อน (สาย RE/chief
   หา ไม่ใช่ของสายนี้)
2. คำถามเปิด NONCLAIM 15 (§4.2) ถึง COO -- ใครยืนยัน bag_cell ตรงกับ
   claimant_identity: `runtime.py` หรือ `mob_pickup.py` ควรมี defense-in-depth
   เพิ่ม -- ยังไม่ตัดสินใจ ไม่บล็อกอะไรวันนี้เพราะยังไม่มีจุดเรียกจริง
3. `combat_aggro` ยังรอ chief ต่อสายเข้า tick loop ตามเดิม (`BUILD-005`
   29 ส.ค. -- เส้นตายใกล้เข้ามา ยังไม่มีความคืบหน้าใหม่ตั้งแต่รอบก่อน)
4. `widened=` ที่จุดเรียก `mob_death.kill()` จริง -- เช็คซ้ำว่า chief ต่อสาย
   แล้วหรือยัง (จากรอบก่อนหน้า `s7hjdb`, ยังไม่ยืนยันสด ณ ตอนเขียนรอบนี้)

-- **สาย B · COMBAT**
