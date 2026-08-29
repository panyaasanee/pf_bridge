# round `B_20260826_1942` (`3dxv22`) · lane B · COMBAT -- MOB-LOOT-001/MOB-PICKUP-001: two nonclaims went stale under R180's wiring, and one of the two copies was left uncorrected once already

**opened:** 2026-08-26 19:42 (+07:00) · **closed:** 2026-08-26 20:17 (+07:00)
**branches:** `claude/serene-darwin-3dxv22` (pirate-force-server, PR pending) ·
`claude/relaxed-goldberg-3dxv22` (pf_bridge, PR pending)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็น -- รอบนี้แก้เอกสาร/หลักฐาน (nonclaims,
scenario pin files, coverage notes) เท่านั้น ไม่แตะ `runtime.py` และไม่แตะพฤติกรรม
โค้ดใด ๆ เลย

## 1 ล็อกต้นรอบ

PR ที่เปิดค้าง หัวข้อขึ้นต้นด้วย `[LANE-B]` ทั้งสองรีโป: **0 ใบ** (ตรวจ 19:42 +07:00
ก่อนเริ่ม และตรวจซ้ำ 20:15 ก่อนเปิด PR -- ไม่มีใครแซง) -> เปิดรอบใหม่ merge `main`
เข้าทั้งสองสาขาก่อน (pirate-force-server ขยับจาก `3b6e968` ไป `1071dbb`, pf_bridge
ขยับจาก `57a9b8d` ไป `a1f78e7`) แล้วยึดล็อกด้วยคอมมิตล็อกเปล่าในสาขานี้

**หมายเหตุกระบวนการ (ตามตรง ไม่ปิดบัง):** รอบนี้เขียนโค้ดและรันเทสก่อนคอมมิตล็อกจริง
(ไม่ได้เปิด draft PR ก่อนแตะไฟล์เหมือนรอบก่อน ๆ) เพราะช่วงต้นรอบใช้เวลานานกับการอ่าน
เอกสาร/pf-adversary สองรอบ -- ตรวจซ้ำว่าไม่มี PR `[LANE-B]` แซงคิวทั้งก่อนและหลัง
ไม่มีการชนเกิดขึ้นจริง แต่รอบถัดไปควรกลับไปเปิด draft PR ก่อนแตะไฟล์ตามธรรมเนียมเดิม

## 2 สิ่งที่เปลี่ยนตั้งแต่รอบสาย B รอบก่อน (`4z0efc`, ปิด 19:30)

ตรวจสดบน `main` วันนี้ (pirate-force-server ที่ `1071dbb`, หลัง merge PR #71 และ #73):

| ตรวจ | ผลรอบ `4z0efc` (18:44-19:30) | ผลสดรอบนี้ (19:42-20:15) |
|---|---|---|
| `runtime.py:4599`(ตอนนั้น)/`4819`(ตอนนี้) เรียก `corpse_override` หรือ `full_roster_override` | `corpse_override` (ยังไม่สลับ) | **`corpse_override` (ยังไม่สลับ)** -- คำขอ chief ของรอบ `4z0efc` ยังไม่ถูกทำ |
| `mob_loot`/`mob_pickup` มี call site ใน `runtime.py` หรือไม่ | ไม่มี (`MOB_LOOT_WIRING`/`MOB_PICKUP_WIRING` เป็นแค่คำขอ) | **มีแล้ว** -- PR #71 (R180, round `3lzfhw`) wire `DropLedgerCell`/`roll_drops`/`drop_frames` เต็ม และ `BagCellRegistry.claim`/`.release` ครึ่งเดียว (registry-level, ไม่ใช่ transaction) |
| `inventory.require_known_backpack` (กำแพงกระเป๋า, BUILD-006) | หยุดที่ round 111 | **หยุดที่ round 111 เหมือนเดิม** (`git log -1 -- src/pirateforce_foundation/inventory.py`) -- ยังไม่ขยับ |
| `notes_to_chief/` ใบใหม่หลังรอบก่อน | -- | `20260826_1946_COO-DECISION-GT-084-not-delayed-chief-call-affirmed.md` -- ถึง chief/attended เรื่อง `GT-084`, ไม่ใช่ของสายนี้ |

checkpoint ที่สองขยับจริง (PR #71 merge แล้ว) แต่การขยับนั้นเองทำให้ nonclaim #1 ของ
`mob_loot.py`/`mob_pickup.py` (ทั้งสองไฟล์บอกว่า "nothing dispatches this module")
กลายเป็นเท็จบางส่วน -- นี่คือช่องว่างที่รอบนี้พบและปิด

## 3 ช่องว่างที่พบ

`mob_pickup.py` docstring nonclaim #1 และ `mob_loot.py` เดียวกันยังบอกว่า "nothing
dispatches this module" ทั้งที่ PR #71 ทำให้มันเท็จไปครึ่งหนึ่งแล้ว (ดูตารางข้อ 2)
`docs/FUNCTIONAL_COVERAGE.json` แถว `monster_spawn_and_loot` มีประโยคเดียวกันฝังอยู่
ในเนื้อความยาวของ `notes` เช่นกัน สามจุดนี้ไม่มีใครแก้เลย

## 4 สิ่งที่สร้างรอบนี้ (สองรอบ pf-adversary)

**pass 1** (ก่อนแก้อะไรนอกจาก docstring prose ของ `mob_pickup.py`) พบว่าการแก้ยังไม่ครบ:
ทูเพิล `MOB_PICKUP_NONCLAIMS[0]` (ตัวที่ไหลเข้า `pin_document()`/
`scenarios/combat_pickup_001.json` และถูก pin ด้วยเทส) ยังเป็นข้อความเดิม, โมดูลพี่น้อง
`mob_loot.py` มี nonclaim เดียวกันที่ยังไม่ถูกแตะ, และ `docs/FUNCTIONAL_COVERAGE.json`
ก็ยังไม่ถูกแก้ -- แก้ทั้งสามจุดตามที่พบ พร้อม re-generate ทั้งสอง scenario pin file จาก
`pin_document(legacy)` จริง (ตรวจแล้วว่า diff คือ `nonclaims[0]` บรรทัดเดียวต่อไฟล์
ไม่มีฟิลด์อื่นขยับ)

**pass 2** (บนดิฟฟ์เต็มห้าไฟล์) ยืนยันว่า claim ทุกจุดของ pass 1 ตรงกับซอร์สจริง
(call site จริง, กำแพงกระเป๋าไม่ขยับจริง, การแก้ append-only จริง) แต่จับว่าตัวเลข
pytest ที่ผมอ้างไว้ตอนนั้น (`3164 passed, 234 skipped`) เป็นตัวเลขเก่าจากก่อน merge
`main` รอบล่าสุด ไม่ตรงกับ HEAD จริง (ที่จริงคือ `3209 passed, 327 skipped, 0 failed`
-- ผมรันซ้ำยืนยันแล้ว) และทูเพิลทั้งสองไม่มีแท็ก `[MEASURED]` เหมือนที่ docstring prose
มี ทั้งที่เป็น claim แบบเดียวกัน -- แก้ทั้งสองจุด: re-run เทสสดก่อนเขียนรอบนี้ (ตัวเลข
ในข้อ 5 คือของจริงที่ HEAD ปัจจุบัน) และเติมแท็ก `[MEASURED, by call-site reading]`
ในทั้งสองทูเพิล แล้ว re-generate scenario pin file อีกครั้ง

ไฟล์ที่แตะ: `src/pirateforce_foundation/mob_pickup.py` (docstring nonclaim #1 +
`MOB_PICKUP_NONCLAIMS[0]`), `src/pirateforce_foundation/mob_loot.py`
(`MOB_LOOT_NONCLAIMS[0]`), `scenarios/combat_pickup_001.json`,
`scenarios/combat_loot_001.json` (re-generated จาก `pin_document()`),
`docs/FUNCTIONAL_COVERAGE.json` (ต่อท้ายย่อหน้า `CORRECTED 2026-08-26 (round
3dxv22)` ใน notes ของแถว `monster_spawn_and_loot` -- ต่อท้ายเท่านั้น ไม่ลบประโยคเดิม
ตามธรรมเนียมไฟล์นี้เอง เทียบกับแถว `hp_death_and_respawn`)

`runtime.py` **ไม่ถูกแตะ** (ของ chief) -- รอบนี้ไม่มีคำขอบรรทัดเดียวใหม่ถึง chief
(คำขอเดิมของรอบ `4z0efc` เรื่องสลับ `corpse_override` -> `full_roster_override` ยัง
ค้างอยู่ ดูข้อ 2)

## 5 เทส

`python3 -m pytest -q`: **3209 passed, 327 skipped, 4986 subtests, 0 failed**
(รันสดที่ HEAD หลังคอมมิตล็อก ก่อนคอมมิตเนื้อหา -- ไม่ใช่ตัวเลขที่ก๊อปจากรอบก่อนหน้า)
`python3 tools/verify_functional_coverage.py`: PASS (domains=8)
skip 327 ตัวมาจากไฟล์ไบนารีของไคลเอนต์ที่ไม่มีในโคลนคลาวด์นี้ (proprietary, ตาม
`AGENTS.md`) ไม่ใช่จาก dependency ขาด -- ตรวจแล้วว่า `capstone`/`pefile` ติดตั้งอยู่จริง

## 6 `pf-adversary`

รันสองรอบเต็ม (pass 1 ก่อนแตะทูเพิล/`mob_loot.py`/coverage doc, pass 2 บนดิฟฟ์เต็ม
ห้าไฟล์) รายละเอียดสิ่งที่พบและสิ่งที่แก้อยู่ในข้อ 4 ข้างบน ไม่มีข้อบกพร่องเหลือค้างจาก
ทั้งสองรอบ (pass 2 ยืนยัน claim ทุกข้อของ pass 1 ตรงกับซอร์สจริงหลังแก้)

## 7 ใบขอ chief

ไม่มีคำขอใหม่ คำขอเดิมของรอบ `4z0efc` (สลับ `mob_death.corpse_override` เป็น
`full_roster_override` ที่ `runtime.py:4819` ปัจจุบัน) ยังไม่ถูกทำ ยกมาซ้ำเพื่อไม่ให้หาย:
อาร์กิวเมนต์เดิมทุกตัว ชื่อฟังก์ชันเดียวที่เปลี่ยน

## 8 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | ไม่มีการเปลี่ยนแปลง -- รอบนี้แก้เฉพาะ prose/nonclaims/coverage-notes, ไม่แตะ encoder, wire byte หรือ schema ใด ๆ |
| **client-observable** | ไม่มี -- ไม่มีใครดูจอรอบนี้ ไม่มีอะไรให้ผู้เล่นเห็น |

## 9 ถ้าผิดต้องย้อนอะไรบ้าง

ย้อนคอมมิตเนื้อหาเดียว (`pirate-force-server` branch นี้) -- การแก้ทั้งหมดเป็น prose/
เอกสาร append-only หรือ regenerate จาก pin function เดิม ไม่มีการเขียนฐานข้อมูล ไม่มี
การเปลี่ยน dispatch หรือ wire behavior แม้แต่บรรทัดเดียว ย้อนได้อย่างสมบูรณ์โดยไม่มี
ข้อมูลสูญหาย

## 10 รอบถัดไปควรทำอะไร

1. เช็คว่า chief สลับ `corpse_override` -> `full_roster_override` ที่ `runtime.py:4819`
   ตามคำขอรอบ `4z0efc` หรือยัง (ยังไม่สลับ ณ 20:15 รอบนี้)
2. `BUILD-006` ยังบล็อกที่กำแพงกระเป๋า (`inventory.require_known_backpack`, เจ้าของคือ
   item lane ไม่ใช่ chief ไม่ใช่สายนี้) -- ไม่มีอะไรให้สายนี้ทำต่อจนกว่า allowlist นั้น
   ขยับ อย่าขอซ้ำ (ขอไปแล้วในรอบ `vvkff9`)
3. `RE-082` (vital id ของ inbound pickup request) ยังไม่มีคำตอบ -- ของสาย RE ไม่ใช่
   ของสายนี้ ไม่ขุดซ้ำ
4. รอบถัดไปควรเปิด draft PR ยึดล็อกก่อนแตะไฟล์ใด ๆ (ดูหมายเหตุกระบวนการข้อ 1)
   แทนที่จะเปิดหลังทำงานเสร็จเหมือนรอบนี้
5. ยังไม่พบงานสร้างใหม่ในเขตของสายนี้ที่ไม่ติดบล็อก -- ถ้ารอบหน้ายังเจอสภาพเดิม
   (chief ยังไม่สลับ, กำแพงกระเป๋ายังไม่ขยับ, RE-082/RE-092 ยังไม่ตอบ) รอบนั้นควรเป็น
   รอบตรวจสั้นอีกครั้ง ไม่ใช่งานสร้างที่ไม่มีอะไรรองรับ

## 11 ใบที่เปิดไปหา COO

ไม่มี -- รอบนี้ไม่มีคำถามที่ต้องให้ COO ตัดสิน มีแต่การแก้เอกสารให้ตรงกับโค้ดจริง

-- **lane B · COMBAT**
