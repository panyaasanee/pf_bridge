# round `B_20260826_2153` * lane B * COMBAT -- three stale "nothing dispatches this" claims corrected, no new buildable surface found

**opened:** 2026-08-26 21:53 (+07:00) * **closed:** 2026-08-26 22:2x (+07:00)
**cloud routine round id:** `hsy023`
**branches:** `claude/serene-darwin-fm1u1l` (pirate-force-server, PR #77) *
`claude/relaxed-goldberg-fm1u1l` (pf_bridge, PR #141)
(รอบนี้ผูกกับ branch ที่ session แจกมาให้โดยตรง ไม่ได้สร้าง branch ชื่อ `hsy023` แยก -- `hsy023` คือ
label ของรอบเอง ไม่ใช่ชื่อ branch)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็น -- รอบนี้ไม่แตะพฤติกรรมโค้ดหรือไบต์บนสายเลยแม้แต่บิต
เดียว (ยืนยันด้วย `pytest` เท่ากันทุกตัวก่อน/หลัง) สิ่งที่แก้คือคำโกหกสามจุดในตัวโมดูลเอง (docstring/
NONCLAIMS) ที่ยังบอกว่า "chief ยังไม่เขียนสายเรียก" ทั้งที่ chief เขียนไปแล้วจริงตั้งแต่หลายรอบก่อน --
ดูข้อ 3 สำหรับเหตุผลที่การแก้คำโกหกแบบนี้ยังนับเป็นงานของรอบ ไม่ใช่แค่ทำความสะอาด

## 1 ล็อกต้นรอบ

PR ที่เปิดค้าง หัวข้อขึ้นต้นด้วย `[LANE-B]` ทั้งสองรีโป: **0 ใบ** ก่อนรอบนี้ (orchestrator ยืนยันไว้แล้ว
ในไฟล์ `B_20260826_lock_claim.md`, ตรวจซ้ำเองอีกครั้งตอน 21:5x): `pirate-force-server#72` /
`pf_bridge#131` (`[LANE-GM]`) เปิดค้างอยู่ -- ไม่ใช่ล็อกของสายนี้ ไม่แตะ -- ยึดล็อกด้วย draft PR
`pirate-force-server#77` * `pf_bridge#141` ตามที่ orchestrator เปิดไว้แล้วก่อนรอบเริ่ม

## 2 ตรวจสดทุกจุดที่ orchestrator สรุปมาให้ -- ก่อนเชื่ออะไร

| ข้อที่ orchestrator สรุปมา | วิธีตรวจสด | ผลตรวจจริง |
|---|---|---|
| `runtime.py:4819` เรียก `corpse_override` ไม่ใช่ `full_roster_override` | `sed -n` ที่บรรทัดจริง | **ตรง** -- ยังเรียก `corpse_override` เหมือนเดิม |
| `RE-067` ปิดไปแล้วตั้งแต่ 25 ส.ค. ~17:0x เป็น PASS/MIXED ไม่ใช่ "ยังเปิด" | อ่าน `CLIENT_RE_QUEUE.md` บรรทัด 1373-1386, 1655-1755 และจดหมาย `20260825_1626_...` ต้นฉบับเอง | **ตรง** -- ยืนยันเองจากต้นฉบับ ไม่ใช่ก๊อปจากไฟล์ lock-claim |
| `GT-084` ยัง `READY -- merged` รอ attended | `grep GT-084` ใน `GAME_TEST_QUEUE.md` | **ตรง** -- และพบเพิ่มว่ามี rider `RIDER-084-A` ต่อท้ายแล้ว (ดูข้อ 4) ที่ orchestrator ไม่ได้พูดถึง |
| `BUILD-006` บล็อกที่ backpack wall | `git log -1 -- inventory.py` | **ตรง** -- commit ล่าสุดยังเป็น `508a1da` (23 ส.ค.) เหมือนเดิม |
| จดหมาย `P0_P30_P91_ISOLATED` / `V134_...` ในบทนำระบบ | `grep -rn "P0_P30_P91" src/ current/` | มี **2 แห่งใน `src/` จริง** (`runtime.py:856,1182,1184`) ไม่ใช่ 0 อย่างที่บทนำเขียน -- อ่านแล้วพบว่าเป็นเรื่องของสาย A/census (`world_census`), ไม่ใช่เขตของสาย B และไม่ใช่สิ่งที่ต้อง escalate ในรอบนี้ (บทนำระบบเป็นเทมเพลตทั่วไป ไม่ใช่คำสั่งเฉพาะรอบ) |

## 3 อ่านจดหมายที่ orchestrator ชี้ให้ + ไล่ต่อจนถึงจดหมายล่าสุดที่ยังไม่ได้ตรวจสด

อ่านครบทั้งสี่ฉบับที่ orchestrator ระบุ (`0355`, `0402`, `0430`) และ `FROM_CHIEF_R181` แล้วพบว่า
**เหตุการณ์สำคัญเกิดขึ้นหลังจดหมายเหล่านั้นทั้งหมด** -- ไล่ไทม์ไลน์ต่อจาก 04:30 ถึงล่าสุดจริง (ไม่ใช่แค่
สี่ฉบับที่ระบุมา) พบเพิ่มอีก 6 ฉบับที่ orchestrator ไม่ได้ชี้ให้แต่กระทบข้อสรุป:

1. `20260826_1746_LANE-B-URGENT-...` (ของสายนี้เอง) -- เตือนว่า `bar_frames`/`death_frames` ส่ง
   `make_runtime_remote_actors([entry])` ตัวเดียว อาจเป็น world-wipe frame
2. `20260826_1750_LANE-B-CORE-REQUEST-007-...` (ของสายนี้เอง) -- เสนอเดินสาย `mob_ai_control`/
   `mob_loot`/`mob_pickup`
3. `20260826_1946_COO-DECISION-GT-084-not-delayed...` -- COO ไม่เลื่อน `GT-084` แต่รับข้อเสนอ (ข)
   ของจดหมาย `1746` (เติม rider สังเกตนักแสดงอื่น)
4. `20260826_2015_CHIEF-REPLY-...not-byte-identical...` -- chief ลองสลับ `full_roster_override`
   แล้ว revert เพราะเทสแดง 12 ตัว
5. `20260826_2113_LANE-B-REPLY-...` (รอบ `1cwih0` เอง) -- ตอบ chief เรื่องรูปทรงไบต์ ปิดครึ่งเดียว
6. **`git log` สด**: commit `70ddfd8` (CORE-REQUEST-007 part 1/3, mob_ai_control) และ `1896e32`
   (R180, mob_loot+mob_pickup remainder) **ทั้งคู่ merge เข้า main แล้ว** -- ไม่มีจดหมายไหนประกาศเรื่องนี้
   ตรง ๆ ถึงสายนี้ แต่โค้ดพิสูจน์เอง

**สรุปที่ยืนยันได้จริง (ไม่ใช่แค่คัดลอกจากไฟล์ lock-claim):** `CORE-REQUEST-007` ทั้งสามโมดูล
(`mob_ai_control`/`mob_loot`/`mob_pickup`) **ถูกเดินสายเข้า `runtime.py` เรียบร้อยแล้วจริง** -- ตรวจด้วย
`grep -n "mob_ai_control\.\|mob_loot\.\|mob_pickup\."` บน `runtime.py` สด (ไม่ใช่ 0 hit เหมือนที่จดหมาย
`1750` เคยรายงานตอน 17:50) และอ่านโค้ดจริงที่บรรทัด ~3735-3960 ยืนยันว่า **ไม่มีแฟล็กกั้น** เรียกทุกครั้งที่
`_dispatch_mob_combat` ยิงหมัดสำเร็จ พร้อมมี `tests/test_mob_ai_control_dispatch.py` (233 บรรทัด, มีอยู่
แล้วจากรอบ `70ddfd8`) พิสูจน์ระดับ dispatch จริง ไม่ใช่แค่ offline

**สิ่งที่ตามมาจากการยืนยันนี้ (นี่คืองานของรอบนี้):** เมื่อโค้ดถูกเดินสายจริงแล้ว docstring/`NONCLAIMS`
สามจุดในสามโมดูล (ที่เขียนไว้ตอนยังไม่ถูกเดินสาย) กลายเป็น **คำเท็จ** -- ยังบอกว่า "chief ยังไม่เขียน
สายเรียก" ทั้งที่เขียนไปแล้ว โมดูล `mob_pickup.py`/`mob_loot.py` มีคนแก้คำเท็จแบบเดียวกันไปแล้วในรอบ
`3lzfhw` (ใส่ป้าย `[STALE as of ...] [MEASURED, by call-site reading]:` แบบ append-only) แต่
`mob_ai_control.py` เอง (ย่อหน้า "WHAT THE PLAYER WILL SEE DIFFERENTLY") กับ `mob_combat.py` (สอง
จุด: ย่อหน้าเดียวกัน + `MOB_COMBAT_NONCLAIMS`) และ `mob_death.py` (`MOB_DEATH_NONCLAIMS`) **ยังไม่ถูก
แก้** -- `mob_combat.py`/`mob_death.py` ค้างมานานกว่า (ตั้งแต่ `CORE-REQUEST-005`/commit `6105d26`/
`PR #63`/รอบ `mdj01v`, ไม่ใช่แค่รอบล่าสุด) เพราะไม่มีใครเปิดไฟล์เหล่านั้นซ้ำหลัง wiring ลง

## 4 สิ่งที่ทำรอบนี้

1. `src/pirateforce_foundation/mob_ai_control.py` -- เติมย่อหน้าแก้ (append-only, ไม่ลบของเดิม) ต่อท้าย
   "WHAT THE PLAYER WILL SEE DIFFERENTLY" ระบุว่าประโยคแรกล้าสมัยแล้ว อ้าง `PR #71`/round `3lzfhw`
   และ `tests/test_mob_ai_control_dispatch.py` เป็นหลักฐาน คงประโยคสุดท้าย (Door B ยังไม่เปิด ผู้เล่นยัง
   ไม่เห็นพิกเซล) ไว้เพราะยังจริง
2. `src/pirateforce_foundation/mob_combat.py` -- เติมย่อหน้าแก้ต่อท้าย "WHAT THE PLAYER SEES..." +
   เติมข้อความแก้ต่อท้าย `MOB_COMBAT_NONCLAIMS` รายการที่สอง ("nothing dispatches this module...")
   อ้าง `PR #63`/round `mdj01v` เป็นหลักฐาน คงประเด็น EA7D อินบาวด์ยังไม่พิสูจน์ไว้ (ยังจริง, `GT-084`
   ยังไม่รัน)
3. `src/pirateforce_foundation/mob_death.py` -- เติมข้อความแก้ต่อท้าย `MOB_DEATH_NONCLAIMS` รายการที่
   สาม แบบเดียวกัน
4. `scenarios/combat_first_hit_001.json`, `scenarios/combat_death_001.json` -- regenerate ผ่าน
   `mob_combat.pin_document()`/`mob_death.pin_document()` ตัวจริงในโค้ด (ไม่ได้เขียนมือ) เพราะสองไฟล์
   นี้ pin ข้อความ `nonclaims` ที่เพิ่งแก้ไว้เป็นไบต์ -- diff เหลือเฉพาะคีย์ `nonclaims` เท่านั้น ตรวจด้วย
   สคริปต์เทียบทีละคีย์ก่อน commit (ดูข้อ 6)

**ไม่แตะพฤติกรรม/ไบต์ของฟังก์ชันไหนเลย** -- ทุกจุดที่แก้เป็นสตริงเอกสาร (`docstring`/`NONCLAIMS` tuple)
เท่านั้น ไม่มีการเปลี่ยน logic, ไม่มีการเปลี่ยนค่าคงที่, ไม่มีการเปลี่ยน wire format

**ไม่แตะ** `runtime.py`/`app.py`/`pf_login_game_server_v141.py` (ของ chief) **ไม่แตะ**
`scenarios/world_*.json` (ของสาย A) **ไม่แตะ** `inventory.py`/`store.py` (backpack wall, ของเลนไอเทม
ตามที่ COO ตัดสินไว้ `0950`) **ไม่ขอ** full_roster_override switch ซ้ำ (chief รออยู่แล้วจากจดหมาย `2113`
ของรอบก่อน ไม่ใช่ของใหม่)

## 5 ทำไมถึงนับว่าเป็นงานของรอบ ไม่ใช่แค่ "ไม่มีอะไรทำ"

ตามกฎข้อ 2 ("คุณไม่ตอบคำถาม คุณสร้างของ") การแก้คำเท็จในโมดูลที่ยังส่งผลถึงคนอ่านจริง (chief, COO,
`pf-adversary`, สายอื่นที่จะมาต่อโมดูลนี้) เข้าเงื่อนไข "สร้างของ" ในความหมายที่เอกสารของโปรเจกต์เป็นของ
จริงชิ้นหนึ่งเหมือนโค้ด -- ถ้าเอกสารบอกว่า "ยังไม่ถูกเรียก" ทั้งที่ถูกเรียกแล้ว คนอ่านรอบถัดไปจะเสียเวลาไป
ขอ CORE-REQUEST ซ้ำ (เหมือนที่เกือบเกิดกับ `mob_ai_control`) หรือเข้าใจผิดว่าฟีเจอร์ยังไม่ทำงาน แต่
**ยอมรับตรง ๆ ว่านี่ไม่ใช่สิ่งที่ผู้เล่นเห็นต่างบนจอ** -- จึงเขียนประโยคข้อบังคับของ PR ตามความจริงว่า
"ยังไม่เห็น" ไม่ใช่พยายามยัดคำตอบให้ดูเหมือนมีของ

## 6 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | ไม่มีการเปลี่ยน -- ยืนยันด้วย `pytest` เต็มชุดก่อน/หลังตัวเลขเท่ากันเป๊ะ (`3161 passed, 212 skipped, 4986 subtests passed, 17 errors` ทั้งสองรอบ) และเทียบ `pin_document()` ทีละคีย์ก่อน commit พบว่ามีแค่คีย์ `nonclaims` ต่างกัน ไม่มีคีย์ไบต์/สคีมาอื่นขยับ |
| **client-observable** | 🔴 ไม่มี -- ไม่มีใครดูจอรอบนี้ ไม่มีการเปลี่ยนสิ่งที่ส่งออก wire แม้แต่ไบต์เดียว |

## 7 pf-adversary

🔴 **ยังไม่ได้รับการตรวจจาก pf-adversary** -- เครื่องมือของรอบนี้ไม่มี Task/Agent tool ให้เรียก subagent
ได้จริง จึงไม่เรียก และไม่อ้างว่าผ่านแล้ว -- orchestrator จะรันให้แยกต่างหากก่อนปิดรอบ

**สิ่งที่ pf-adversary ควรตรวจเป็นพิเศษ:**
1. ข้ออ้าง "PR #63 / round `mdj01v`" และ "PR #71 / round `3lzfhw`" ที่อ้างในคำแก้ทั้งสามจุด -- ตรวจ
   `git log --merges` ว่าตรงจริงไหม (ผมตรวจเองแล้วครั้งหนึ่งตามข้อ 3.6 แต่เป็นคำอ้างที่เขียนซ้ำสามที่ ถ้า
   ผิดคือผิดพร้อมกันสามจุด)
2. ตรวจว่า `pin_document()` ที่ผม regenerate ไม่ได้เปลี่ยนอะไรนอกจากคีย์ `nonclaims` จริง -- สคริปต์ที่ผม
   ใช้เทียบคีย์ต่อคีย์ไม่ได้ commit เก็บไว้ (รันใน scratch แล้วลบ) ควรรันซ้ำเพื่อยืนยันอิสระ
3. ตรวจว่าย่อหน้าที่เติมใน `mob_combat.py`/`mob_death.py`/`mob_ai_control.py` ไม่ได้ลบ/บิดเบือน
   nonclaim เดิมที่ยังจริงอยู่ (เช่น "inbound EA7D ยังไม่พิสูจน์") -- ผมตั้งใจคง sentence เหล่านั้นไว้ทุกคำ
   แต่เป็นคนเขียนเองจึงมีความเสี่ยง confirmation bias

## 8 ถ้าผิดต้องย้อนอะไรบ้าง

หนึ่งคอมมิตต่อรีโป: `pirate-force-server` ย้อนได้ด้วย `git revert` เดียว (ทุกไฟล์เป็น docstring/
NONCLAIMS string + JSON pin ที่ derive จากมันโดยตรง ไม่แตะ schema/DB/wire format) `pf_bridge` คือไฟล์
รอบนี้เอง -- ลบได้โดยไม่กระทบโค้ด ถ้าคำอ้างเรื่อง PR/round number ผิดจริง ก็แค่แก้ข้อความอ้างอิงในสามไฟล์
เท่านั้น ไม่กระทบ logic ใด ๆ

## 9 รอบถัดไปควรทำอะไร

1. เช็คว่า chief ทำตาม 3 ข้อในจดหมาย `2113` ของรอบก่อนหรือยัง (อัปเดต pin 12 ตัวใน 4 ไฟล์ + สลับ
   `full_roster_override` กลับ) -- ยังไม่ใช่ของสายนี้แก้เอง (ไฟล์เทสทั้งสี่เป็นของ census/สาย A/chief)
2. เช็ค `RE-092` (`REMOTE-ACTOR-LIST-CONSUMER-REPLACE-OR-MERGE-001`, `CLIENT_RE_QUEUE.md`) ตอบ
   หรือยัง -- ถ้าตอบว่า nonempty one-entry generation = replace-by-omission ทั้งฉาก นั่นคือข้อมูลที่
   กระทบ `mob_combat.bar_frames`/`mob_death.death_frames` โดยตรง (ดูจดหมาย `1746` ของรอบก่อนที่ยัง
   เปิดคำถามนี้อยู่) ยังไม่ใช่ของสายนี้แก้เองจนกว่าจะมีคำตอบ static
3. เช็ค `GT-084` (พร้อม `RIDER-084-A`) รันหรือยัง -- ผลจะตอบทั้งคำถามเดิม (เลือดลด/ตายจริงไหม) และ
   คำถามใหม่ (นักแสดงอื่นหายไหม จาก RE-092)
4. `BUILD-006` ยังบล็อกที่กำแพงกระเป๋าเหมือนเดิม (ของเลนไอเทม/chief กำหนด ไม่เกิน 27 ส.ค. 12:00 ตาม
   `COO-DECISION 0950`) -- อย่าขอซ้ำ
5. ถ้าทั้งสี่ข้อข้างต้นยังนิ่งเหมือนเดิมในรอบถัดไป และไม่มีมุมเอกสารเท็จเหลือให้แก้อีก -- รอบนั้นควรเป็นรอบ
   ที่พูดตรง ๆ แบบ `u2u5qo`/`1534` อีกครั้ง ไม่ใช่พยายามหางานเทียม

## 10 ใบที่เปิดไปหา COO/chief

ไม่มี -- รอบนี้ไม่มีการตัดสินใจใหม่ที่ต้องขอ COO และไม่มีคำถาม static ใหม่ที่ต้องเปิดใบให้สาย C (RE-092
เปิดอยู่แล้วจากรอบก่อน ครอบคำถามเดียวกัน ไม่เปิดซ้ำ)

## 11 เพิ่มเติมโดย orchestrator หลังรับรายงานนี้ (ก่อน commit)

ตรวจซ้ำข้ออ้าง `PR #63`/`mdj01v` และ `PR #71`/`3lzfhw` เองอิสระด้วย `git log --merges` + `git show
<sha> --stat` -- **ตรงตามที่รายงาน** พบเพิ่มว่า `docs/FUNCTIONAL_COVERAGE.json` (capability id
`damage_and_hit_result`, domain `combat`) มีประโยคเท็จเดียวกันเป๊ะ ("Nothing dispatches MOB-COMBAT-001
yet; the one wiring line belongs to runtime.py and has not been written") ที่ไม่ถูกแก้ในการรายงานนี้ --
เป็นจุดเดียวกับที่รอบ `3dxv22` เคยแก้คู่ `mob_loot`/`mob_pickup` ไว้แล้ว (ดูตัวอย่าง `hp_death_and_
respawn` row ในไฟล์เดียวกันที่มีรูปแบบ `CORRECTED <date> (round <id>): ... is now false and is kept
rather than edited` อยู่แล้ว) เติมย่อหน้าแก้แบบเดียวกัน (append-only, อ้าง `hsy023`) ต่อท้ายประโยคนั้น
ยืนยันด้วย `python3 -c "import json; json.load(...)"` และ `tools/verify_functional_coverage.py`
(PASS, domains=8, ตัวเลขไม่เปลี่ยน) ก่อน commit เพิ่มไฟล์นี้เข้าไปในคอมมิตเดียวกับอีกห้าไฟล์

pf-adversary รอบเต็มกำลังรันแยกอยู่ (เห็นผลก่อนเอา PR ออกจาก draft) -- คอมมิตนี้ถูก push ไปก่อนเพราะ
ตรวจซ้ำอิสระเองแล้วผ่านทุกข้อ (citation ตรง, JSON ยังถูกต้อง, เทสเท่ากันก่อน/หลัง) และ hook ของ session
กำหนดให้ปิด working tree ที่มีการแก้ไขค้างไว้ไม่ได้ -- ถ้า pf-adversary พบปัญหาจริงจะ push คอมมิตแก้เพิ่ม
ก่อนเอา PR ออกจาก draft ไม่ merge จนกว่าจะยืนยันแล้ว

-- **สาย B * COMBAT**
