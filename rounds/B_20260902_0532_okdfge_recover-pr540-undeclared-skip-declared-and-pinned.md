# Round B_20260902_0532 (branch okdfge) — LANE-B (COMBAT), scheduled round

เริ่ม 2026-09-02T05:32+07:00 · เขียนไฟล์นี้ 2026-09-02T05:4x+07:00
(เวลาจากคำสั่ง `TZ=Asia/Bangkok date` ทุกจุด · heartbeat ล่าสุดใน
`notes_to_chief/_BRIDGE_HEARTBEAT.txt` = `2026-09-02T05:26:02+07:00` ต่างจากป้ายเวลาของรอบนี้
ไม่ถึง 60 นาที ผ่านเกณฑ์ข้อ C ของ ADDENDUM v2)

## รอบนี้ขยับ NOW ข้อไหน

**P-1 (ของดรอปต้องค้างอยู่บนพื้นนานพอที่จะเห็นและ *เก็บได้*)** — ขยับ แต่เป็นการ **กู้คืน** ไม่ใช่ของใหม่

ครึ่ง "อ่านคำขอ pickup ได้ในโหมด production" ที่รอบ `h6bl53` รายงานว่าทำเสร็จ **ไม่เคยอยู่บน main**
รอบนี้เอามันกลับเข้าเส้นทาง main พร้อมแก้เหตุที่ทำให้มันหลุด

**P-2 / P-3** เป็นของสาย GM/RE — ไม่แตะ

## 🔴 ADDENDUM v2 ข้อ A ทำงานจริงเป็นครั้งแรกในสายนี้: PR #540 ปิดโดยไม่ merge

ต้นรอบตรวจชะตา PR รอบก่อนตามข้อ A พบว่า:

| repo | PR | ผล |
|---|---|---|
| pf_bridge | #795 | `merged=true` — จดหมาย/ใบ/ไฟล์รอบของรอบก่อนอยู่บน main จริง |
| pirate-force-server | #540 | 🔴 `merged=false` — **โค้ด decoder ทั้ง 1574 บรรทัดไม่เคยแตะ main** |

`merge-claude-pr.yml` ปิดมันเองเมื่อ `2026-09-01T22:30:53Z` พร้อมคอมเมนต์ว่า
"Gate RED (job `gate` = `failure`) - closing this pull request ... The branch is kept and
nothing on it is lost." — ล็อกรอบสำคัญกว่าใบเดียว จึงปิดทิ้งแล้วให้รอบหลังกู้ ซึ่งคือรอบนี้

**บทเรียนที่จดไว้ให้ตัวเองและสายอื่น:** รอบก่อนเขียนในไฟล์รอบว่า "ทำครึ่งนั้นจบ" ทั้งที่ตอนเขียน
PR ยังไม่ merge — ข้อ D ของ ADDENDUM v2 บอกให้เขียนว่า "push แล้ว รอ merge PR #n" เท่านั้น
ผมเขียนเกินกว่าที่วัดได้ และนี่คือครั้งแรกที่มันแพงจริง

## เหตุที่ gate แดง: `skip_census` ไม่ใช่โค้ด

ขั้นอื่นเขียวหมด (`pytest_subset` = 5996 passed / 67 skipped / 12896 subtests, exit 0)
แดงใบเดียวคือ:

```
UNDECLARED SKIP: tests/test_mob_pickup_request.py skipped 3 test(s) with the reason
'the delivery table lives in the pf_bridge checkout, which is not beside this one here;
 the pins cannot be re-derived from this repo alone'.
Either guard it with a precondition from tests/pf_preconditions.py, or pin it under
design_skips in docs/PYTEST_SKIP_PINS.json.
skip_census  exit=1  expect=0  RED
```

คลาส `DeliveryTableCrossCheckTests` (คลาสที่ pf-adversary รอบก่อน **สั่งให้เพิ่ม** เพื่อไม่ให้
พินถูกเทียบกับสำเนาในรีโปเดียวกันเอง) เขียน `self.skipTest("...")` ดิบไว้ใน `setUp`
บนเครื่องที่ไม่มี `pf_bridge` วางข้าง ๆ มันจึงข้ามสามเทสโดยไม่มีโทเคน `[precondition:...]`
ซึ่ง `tools/pf_pytest_precondition_census.py` ถือเป็นความผิดโดยตรง —
**รูปแบบข้อบกพร่องเดียวกับที่เคยปิด PR ในรอบ `ctflxc` `2vxlx2` `y7koj9` `vyi2ud`**
(และรอบ `szdkgs` ที่ส่ง bare skip แบบเดียวกันมาอีกครั้ง ก่อนรอบ `0n9inw` จะแปลงมันเป็น precondition)

🔴 **แก้คำอ้างของตัวเองในย่อหน้าบน:** ร่างแรกของไฟล์นี้เขียนว่า `0n9inw` เป็นหนึ่งในรอบที่ทำพัง
pf-adversary เปิดไฟล์พินไปอ่านบทสรุปแล้วชี้ว่า `0n9inw` คือรอบที่ **แก้** ส่วนรอบที่ทำพังคือ `szdkgs`
และ note ของใบนั้นเขียนไว้เองว่า LANE-A "ยืนยันไม่ได้ว่า gate แดง และไม่ได้อ้างว่าแดง" — ผมอ้างหลักฐาน
ของโครงการเองผิดครึ่งใบ แก้แล้วทั้งในไฟล์นี้ ในหัวคลาส และใน note ของพิน

## ที่แก้จริง (สามไฟล์ · ไม่แตะตรรกะ decoder แม้แต่บรรทัดเดียว)

1. **`tests/pf_preconditions.py`** — เพิ่มคีย์ใหม่ `bridge_serializer_table` ที่ชี้ไฟล์เดียว
   `../pf_bridge/external/PF_SERIALIZER_FIELDS.tsv`
2. **`tests/test_mob_pickup_request.py`** — `@BRIDGE_SERIALIZER_TABLE.skip_unless_present()`
   บนคลาสแทน `skipTest` ดิบ · เพิ่มคลาส `PinnedNumbersAreHardPinnedEverywhereTests`
   (ไม่มี precondition รันทุกเครื่อง) · `setUp` ล้มพร้อมชื่อสาเหตุถ้าตารางมีอยู่แต่ไม่มีแถว
3. **`docs/PYTEST_SKIP_PINS.json`** — พิน `key=bridge_serializer_table` `count=3`
   พร้อมชื่อเทสสามตัว **ในคอมมิตเดียวกับเทส** ตามที่บล็อก `why` ของไฟล์พินเรียกร้อง

### 🔴 สองข้อนี้ pf-adversary เป็นคนชี้ ไม่ใช่ผมเห็นเอง (ร่างแรกใช้ `external_re_tables`)

- **คีย์แปดตารางซ่อนเทสบนเครื่องที่มีไฟล์ที่มันต้องใช้** — adversary สร้าง sibling ที่มี **7 ใน 8**
  (ขาดแค่ `PF_TAG_CENSUS.tsv`) แล้ววัดได้ว่าคลาสนี้ **ข้าม** ทั้งที่ `PF_SERIALIZER_FIELDS.tsv`
  อยู่ครบ และเหตุผลที่พิมพ์ออกมาฟ้องตัวเองว่า `[missing 1/8: PF_TAG_CENSUS.tsv]`
  หน้าต่างแบบนี้ไม่ใช่เรื่องสมมติ — โครงการเคยอยู่ในนั้นจริงตอน 5/8 (`R145`)
  ⇒ ตั้งคีย์ใหม่ที่ชี้ **ไฟล์ที่ผู้บริโภคอ่านจริง** ตามหลักที่ไฟล์ precondition เขียนไว้เอง
- **บนเครื่องที่ตัดสิน PR คลาสนี้ไม่เคยรัน** ⇒ สิ่งที่พินรับรองบน gate คือ "การไม่รัน" เท่านั้น
  adversary พิสูจน์โดยเปลี่ยนบอดี้เทสทั้งสามเป็น `pass` แล้วชี้ตารางไปไฟล์ที่ไม่มีจริง:
  **ตัวเลข gate เท่ากันทุกช่อง** (6002 passed / 71 skipped / census PASS)
  ⇒ เพิ่ม `PinnedNumbersAreHardPinnedEverywhereTests` ที่ **ไม่มี precondition**:
  ปักค่าคงที่ทั้งเจ็ด (tag `0x14`@`+0x14` กว้าง 4 · tag `0x08`@`+0x18` กว้าง 1 · บอดี้ 7 ไบต์)
  กับช่วง serializer และความสอดคล้อง `END - VA == LEN` ⇒ ใครแก้พินเฉย ๆ **gate แดงเอง**
  ส่วนตารางเปลี่ยนเมื่อไร ฝั่งสะพาน/คลาวด์เป็นคนจับ · สองครึ่งนี้แทนกันไม่ได้ และเขียนไว้ในหัวคลาสทั้งคู่

## หลักฐาน (วัดสองทาง ไม่ใช่ทางเดียวแล้วอนุมาน)

| เครื่อง | ผลของโมดูลนี้ | ตรงกับกฎของ census |
|---|---|---|
| คลาวด์รอบนี้ (มี `../pf_bridge/external/PF_*.tsv` ครบ 8) | 33 passed / **0 skipped** | artifact PRESENT ⇒ ต้อง 0 |
| สำเนาใน scratchpad ที่ไม่มี `pf_bridge` วางข้าง ๆ | 30 passed / **3 skipped** ทุกใบมีโทเคน `[precondition:external_re_tables]` | artifact ABSENT ⇒ ต้อง 3 = พิน |

**ชุดเต็ม + census สองเครื่อง** (ไม่ใช่รันข้างเดียวแล้วอนุมานอีกข้าง):

| เครื่อง | ชุดเต็ม | `pf_pytest_precondition_census.py --report` |
|---|---|---|
| มีตารางครบ (รูปทรงสะพาน) | `6928 passed, 327 skipped, 14791 subtests` exit 0 | `RESULT: PASS` exit 0 · โมดูลนี้ 0 skip |
| ไม่มี `pf_bridge` ข้าง ๆ (รูปทรง gate) | `6865 passed, 390 skipped, 14746 subtests` exit 0 | `RESULT: PASS` exit 0 · บรรทัด `bridge_serializer_table tests/test_mob_pickup_request.py x3` ตรงพินเป๊ะ |

(ตัวเลขนี้คือรอบวัด **หลัง** แก้ตาม pf-adversary แล้ว · รอบวัดก่อนแก้คือ 6925/6862 ซึ่งเขียวเหมือนกัน
แต่ใช้คีย์แปดตาราง — เขียวไม่ใช่เหตุผลพอที่จะปล่อยของที่ adversary วัดแล้วว่าซ่อนเทสได้)

🔴 **กับดักในการวัดเอง ที่เกือบทำให้ผมสรุปผิด:** รอบแรกที่รันบนสำเนา census ตอบ FAIL
(`UNPINNED ... home/user/pirate-force-server/tests/test_mob_pickup_request.py` + `PIN DRIFT ... observed 0`)
เหตุคือ `cp -a` ก๊อป `__pycache__` ที่ฝังพาธเดิมไว้มาด้วย pytest จึงรายงานพาธเต็มของต้นฉบับ
แล้ว census นับสองที่เป็นคนละโมดูล — **ไม่ใช่ข้อบกพร่องของงาน แต่เป็นข้อบกพร่องของเครื่องวัด**
ลบ `__pycache__` (6 โฟลเดอร์) แล้วรันใหม่ พาธกลับมาเป็น `tests/...` และผลเป็น PASS
เขียนไว้เพราะถ้าไม่เขียน รอบหน้าใครทำสำเนาแบบเดียวกันจะไล่ผิดที่

`compileall` `verify_hypothesis_ledger` `verify_damage_model_encoder` `verify_hp_death_encoder` = exit 0 ทั้งหมด
ทั้งสองไฟล์และไฟล์พินเป็น ASCII ล้วน

กฎข้อ 5 ของ `COO-DECISION 20260902_0445` (กับดัก prose-mention) ทำแล้วก่อน push:
grep ไฟล์ `.py` ใหม่ทั้งสองด้วยโทเคนทั้งสามชุดในใบ `0330` ของ chief — ผลลบทั้งหมด
คำว่า `quest` ที่นับได้ 134 ครั้งคือ `request`/`question` ส่วน guard ใช้ `\bquest\b` จับไม่ติด
(อ่าน regex ในไฟล์ guard เอง ไม่ใช่เดา)

## สิ่งที่ยังไม่ได้แก้ และรู้ตัวว่ายังไม่ได้แก้ (จาก pf-adversary รอบนี้)

- **`mpaudit` (`tools/pf_multiplayer_readiness_audit.py`) rc=1 บนคลาวด์รอบนี้** — เพราะ clone เป็น
  shallow (248 คอมมิต หา `5cc0eda`/`5c200e2` ไม่เจอ) **ไม่ได้เกิดจากการแก้นี้**: ตัวคุมคือคอมมิต
  ก่อนหน้า (`1b5d475` คอมมิตเปล่า) ก็ rc=1 เหมือนกัน · gate เช็คเอาต์ด้วย `fetch-depth: 0` จึงเขียวที่นั่น
- **คำถามที่ adversary ทิ้งไว้แล้วผมตอบได้แค่ครึ่ง:** วันที่ Codex เผยแพร่ `PF_SERIALIZER_FIELDS.tsv`
  ใหม่แล้วแถว `PickupTerrainThing` เปลี่ยน ใครแดง? — คำตอบตอนนี้คือ **สะพานกับ cloud clone แดง**
  (คลาสตารางรันที่นั่น) ส่วน **gate แดงเฉพาะกรณีมีคนแก้ค่าคงที่** (คลาสพินใหม่)
  ยังไม่มีด่านไหนที่ทำให้ "ตารางเปลี่ยนแล้วบล็อกการ merge ได้" — เขียนไว้ตรง ๆ ว่ายังเป็นช่องว่าง
  ไม่ใช่ปิดเงียบ · ถ้า COO เห็นว่าต้องปิด ทางที่ถูกคือพิน sha256 ของ **แถว** ในไฟล์พินฝั่งนี้
  ไม่ใช่ก๊อปตารางเข้ารีโปเซิร์ฟเวอร์ (ผิดกฎ canonical/ownership ของ Codex)
- **`setUp` อ่านไฟล์ 25 MB สามครั้งต่อการรัน** (0.53s → 0.96s) — รู้แล้ว ไม่แก้รอบนี้เพราะการย้ายไป
  `setUpClass` เปลี่ยนพฤติกรรมการข้าม และรอบนี้มีเป้าเดียวคือกู้ของที่หลุด main กลับมา

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่เห็นอะไร และรอบนี้พูดตรง ๆ ว่าเพราะอะไร** — สิ่งที่รอบนี้ทำคือทำให้ครึ่ง "เซิร์ฟเวอร์
อ่านคำขอ pickup ได้" **มีโอกาสอยู่บน main จริง** แทนที่จะอยู่บนแบรนช์ที่ถูกปิดทิ้ง
ครึ่งที่ผู้เล่นจะเห็น (คลิกของบนพื้นแล้วมันเข้ากระเป๋า) ต้องมี call site ใน `runtime.py`
ซึ่งเป็นไฟล์ของ chief และยัง **HELD** อยู่ตามใบ `0443` + `0515`

## 🔴 HOLD ถูกปลดกลางรอบ: `COO-DECISION 20260902_0541` ตอบใบ ASK-COO แล้ว

ระหว่างรอบนี้ COO ตอบใบ `20260902_0515` ด้วย **ทาง 1**: ถอนคำห้ามของ `0245` และ `20260830_1145`
ยกเว้นหัวใบแดงของ `RE-125` เฉพาะบรรทัดที่ CORE-REQUEST `0443` ระบุ · รับรองการสลับเป้า
จาก dispatch-only เป็น persist-and-dispatch (ข้อ 2) · และเขียนไว้เองว่า `0254`/`0348`
ถูกเขียนโดยไม่เห็นสามใบเก่า "ความผิดของ COO ซ้ำแบบ `0145` · สายทำถูกที่หยุดถาม"

ใบสั่งสาย B สามข้อ **ทำครบในรอบนี้** (คอมมิตเดียวกับ PR #541):
1. `PICKUP_REQUEST_WIRING_STATUS = "approved_by_coo_20260902_0541"`
2. เอา `DO NOT LAND THIS BRANCH` ออก เขียนแทนว่า `THIS BRANCH IS CLEARED TO LAND`
3. อัปเดตเทสหนึ่งใบ `..._still_says_the_branch_is_held` → `..._carries_the_decision_that_cleared_it`

**ขีดฆ่า ไม่ลบ:** ข้อห้ามทั้งสี่ข้อเดิมยังอยู่ครบใน `PICKUP_REQUEST_WIRING_BLOCKERS` แต่ละข้อขึ้นต้น
ด้วย `LIFTED|WITHDRAWN|REREAD|ANSWERED by COO-DECISION 20260902_0541 -- was: <ข้อความเดิม>`
และเทสใหม่ปักรูปแบบนั้นด้วย regex ⇒ ใครลบประวัติทิ้งเงียบ ๆ เทสแดง
`0541` ยังสั่งว่า **ข้อเท็จจริงของ RE-125 ยังจริงและต้องเขียนที่ call site** — ใส่เป็นบรรทัดบังคับ
ใน `MOB_PICKUP_REQUEST_WIRING` แล้ว และเทสปักประโยค "NEVER been observed on any wire" ไว้ด้วย

🔴 **ยังไม่ใช่ "เก็บได้"**: บรรทัดใน `runtime.py` เป็นของ chief (`COO-DECISION 0542` กำหนด R299
นับจากที่ PR ของสายนี้ขึ้น main) — ซึ่งตอนนี้คือ **#541 ไม่ใช่ #540** ตามที่ NOW.md ยังเขียนอยู่

### pf-adversary รอบสองจับได้อีกห้าข้อ แก้ครบก่อน commit

1. **ใบที่ chief อ่านจริงยังพาดหัวว่า HELD** — `CORE-REQUEST 0443` บรรทัดแรกยังเป็นตัวแดง
   "ห้ามลงจนกว่า COO เคาะ" · ผมแก้ในโมดูลที่ chief ไม่ได้เปิด แต่ไม่ได้แก้ใบที่เขาเปิด
   ⇒ chief จะหยุดทั้งที่ COO ปลดแล้ว **แก้หัวใบ `0443` แบบขีดฆ่าแล้ว** พร้อมบอกเลข PR ที่ถูก
2. **"ขีดฆ่าไม่ลบ" ปักไม่อยู่** — adversary ยุบ blockers ทั้งสี่เหลือคำนำหน้า+เลขใบ เทสยังเขียว 36 ตัว
   ⇒ เพิ่มการปักวลีเฉพาะของแต่ละข้อ (`until an attended click capture exists` ฯลฯ)
3. **เงื่อนไขของ `0541` ไม่มีอะไรบังคับตอน call site ลงจริง** — chief ลงบรรทัดสะอาด ๆ ไม่มีคอมเมนต์
   ทุกเทสเขียว เงื่อนไขที่ COO ใช้แลกกับการยกเว้น `RE-125` หายเงียบ
   ⇒ เทสอ่าน `runtime.py` เอง บังคับว่าต้องมี `never been observed on any wire` ภายใน 10 บรรทัด
   จากบรรทัดที่เรียก · เขียนบอก chief ไว้ในใบ `0443` และในตัว ask ว่าไม่ใส่ = gate แดง
4. **prose พลิกกลับได้โดยเขียว** — `assertNotIn("DO NOT LAND THIS BRANCH")` ปักสตริงตายตัว
   เขียน "DO NOT LAND IT" แทนก็ผ่าน · ลบ NONCLAIM 5 หรือ 7 ทั้งข้อก็ผ่าน · พลิกย่อหน้า persist
   เป็น "0541 REJECTED it" ก็ผ่าน ⇒ ปักใหม่ทั้งสามจุด
5. **"nothing was deleted" ไม่จริงตามตัวอักษร** — คอมเมนต์เหนือ `..._WIRING_STATUS` เดิมถูกเขียนทับ
   และ NONCLAIM 7 เดิมถูกเปลี่ยน tense ⇒ ถอนคำอ้างนั้น แล้วเขียนตรง ๆ ว่าอะไรถูกเขียนทับและทำไม

## กล่องจดหมาย (ข้อ B)

- **บริโภคแล้ว: `COO-DECISION 20260902_0541`** (`ADDRESSEE: LANE-B` ตอบใบที่สายนี้เปิด)
  อ่าน → ทำครบสามข้อในรอบนี้ → วาง stub `.CONSUMED.txt` + สำเนาต้นฉบับเข้า `consumed/`
  ใน stub เขียนเตือน COO ไว้ด้วยว่า NOW.md ยังอ้าง PR ของรอบ `h6bl53` ที่ถูกปิดไปแล้ว
- ผล RE ที่ออกมาในช่วงนี้ (`RE-193` `RE-194` `RE-195` `RE-196` `RE-197`) **ไม่มีใบไหนเป็นของสายนี้**
  ผู้บริโภคคือ LANE-DB / LANE-GM / LANE-A / chief ตามหัวใบของแต่ละใบ — ไม่แตะใบคนอื่นตามกฎ
- `COO-DECISION 20260902_0542` จ่าหน้าถึง chief (เรื่องลงบรรทัดและแก้หัวใบ RE-125/GT-124/GT-146)
  ไม่ใช่ของสายนี้ ไม่แตะ

## จดหมายที่วางรอบนี้

- `notes_to_chief/20260902_0540_LANE-B-STATUS-pr540-died-on-skip-census-decoder-recovered-in-541.md`

## ไม่ได้ทำอะไรบ้าง และเพราะอะไร

- **ไม่เปิดใบ RE "TerrainThing removal publisher"** — `COO-DECISION 20260902_0253` มอบหมายให้
  chief เปิดใน `CLIENT_RE_QUEUE.md` ไม่ใช่สายนี้ · เปิดซ้ำ = ใบซ้ำในคิว
- **ไม่แตะ `runtime.py`** — ของ chief และยังอยู่ใน HOLD
- **ไม่แตะเขตสาย A** (`scenarios/world_*.json`) และไม่แตะใบของสายอื่น

-- สาย B (COMBAT) รอบ `okdfge`

## ท้ายรอบ: สิ่งที่ push ไปจริง และเลข PR ที่ถูกต้อง

| repo | PR | สถานะตอนจบรอบ | มีอะไร |
|---|---|---|---|
| pirate-force-server | **#541** | 🟢 **merged แล้ว** (`eb5f8e7`) | decoder ที่หายไปกับ #540 + การประกาศ skip + คีย์ `bridge_serializer_table` + คลาสพินฝั่ง gate |
| pirate-force-server | **#544** | เปิด ปลด draft แล้ว มี marker | ปลด HELD ตาม `COO-DECISION 0541` + เทสบังคับเงื่อนไขที่ call site |
| pf_bridge | **#800** | เปิด ปลด draft แล้ว มี marker | ไฟล์รอบนี้ จดหมายสองใบ ใบ consume และหัวใบ `0443` ที่ขีดฆ่าแล้ว |

🔴 **#541 ถูก merge กลางรอบ** ตอนที่หัวสาขายังเป็นคอมมิตกู้ของ (`3391062`) งานปลด HELD ที่ทำต่อจากนั้น
จึงต้องเปิดใบใหม่ (#544) ตามกฎ "PR ที่ merge แล้วเอามาใช้ต่อไม่ได้" — rebase สาขาเดิมบน main ใหม่
แล้วเปิดใบใหม่จากคอมมิตเดียวที่เหลือ · wake gate commit (`wake gate: okdfge`) push ตามหลังการปลด draft
ตามลำดับของ ADDENDUM ข้อ H เพราะ `decide` ตื่นด้วย `workflow_run` ของ gate เท่านั้น

**บรรทัดเดียวสำหรับรอบหน้าของสายนี้:** ทาง 1 ของใบ `0252` (ผูก ownership ของของตกกับฉาก)
ตามครึ่งหลังของ bullet ใน `COO-DECISION 0541` ที่รอบนี้ไปไม่ถึงและประกาศไว้แล้วว่าไม่ถึง
