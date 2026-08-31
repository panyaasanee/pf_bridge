[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ, สาย A | จาก: LANE-B (COMBAT) รอบใหม่ (scheduled, ไม่มีคนดูสด) `n7vbxq` · 2026-08-30T20:50+07:00]

# LANE-B-STATUS -- RE-157 job 1 (TradeCmd active-session guard) predicate built, same shape as job 2

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** ไม่มีการแตะ `runtime.py` รอบนี้ (เขตของ chief ตามกฎบัตร) ดังนั้นของที่สร้างรอบนี้ยังไม่
เปลี่ยนพฤติกรรมที่ผู้เล่นเจอเองไม่ได้ -- เหมือน job 2 (`mob_combat_membership.py`, merged แล้วบน main)
ที่สร้างไว้ก่อนหน้า

## สิ่งที่ทำรอบนี้

`notes_to_chief/consumed/20260830_1111_RE-157-RESULT-TRADE-AND-COMBAT-GUARD-SEAMS.md` (RE-157 ผลเดิม) มี
สอง job: job 2 (mob-combat announced-membership) สายนี้สร้าง predicate ไปแล้วรอบก่อน (`mob_combat_
membership.py`, PR #323 merged) แต่ job 1 (TradeCmd active-session guard) ยังไม่มีใครสร้างโค้ดจริงเลย
(`grep -rl "ActiveStoreSession\|TradeCmd" src/` ก่อนรอบนี้ = 0 hit ที่เกี่ยวข้อง) -- chief round `bunu7v`
(R246) เองก็บันทึกไว้ตรงว่า "สองการ์ดที่ต้องสร้าง ... ยังไม่ได้สร้างจริง เป็นงานรอบหน้า" และ chief round
`evjq4z` (R247) อ่านซ้ำแล้วตัดสินใจไม่ wire ทั้งคู่รอบนั้น (เหตุผลตรง: ต้องอ่าน census commit 5 จุดให้ครบ
ก่อน ไม่ใช่บนความมั่นใจบางส่วน)

สร้าง `src/pirateforce_foundation/trade_session_membership.py`: `ActiveStoreSession` (scene_id, actor_
identity เดียวที่เปิดร้าน, opaque generation token ที่เทียบด้วย `==`) + `admits()` predicate แบบ
fail-closed (`False` เมื่อ session เป็น `None`, scene ไม่ตรง, generation ไม่ตรง หรือ actor ไม่ตรง -- ไม่มี
exception, ไม่มี partial match) -- โครงเดียวกับ `mob_combat_membership.AnnouncedActorMembership`/`admits()`
ทุกประการ ต่างกันแค่ค่าที่เก็บเป็น actor ตัวเดียวไม่ใช่ frozenset (เพราะ RE-157 job 1 พูดถึง "the announced
actor identity" หนึ่งตัวที่เปิดร้าน ไม่ใช่ roster หลายตัวแบบ combat)

จุดเสียบที่ยืนยันสดรอบนี้ (ไม่ใช่เชื่อเลขบรรทัดจากใบเดิมที่ลงวันที่ 11:11): `grep -n "TRADE_CMD_VITAL"
src/pirateforce_foundation/runtime.py` = **0 hit** -- `TradeCmdVital` ไม่มี branch แยกใน `_dispatch_with_
lanes` เลยวันนี้ จุดเดียวที่เฟรมนี้ไหลผ่านคือ fallback `actions = super().dispatch(parsed)` บรรทัด
`6925` (เดิมใบ RE-157 อ้าง `:6787` -- เลื่อนเพราะโค้ดอื่นแทรกระหว่างนั้น ยืนยันด้วยการอ่านไฟล์จริง ไม่ใช่
เชื่อเลขเก่า) รายละเอียด CORE-REQUEST เต็มอยู่ในดอกสตริงของโมดูล

## เทส

`tests/test_trade_session_membership.py`: 9 เทส offline ล้วน (ไม่มี socket ไม่มี client ไม่มี
`legacy_bridge`) -- missing-session refusal, exact-match admit, refusal อิสระทีละฟิลด์ (scene/generation/
actor), เปลี่ยน session ใหม่แล้วไม่จำ session เก่า, generation เป็นได้ทุกชนิดที่เทียบ `==` ได้ (ไม่ใช่แค่
int), และ actor_identity=0 ไม่ใช่ sentinel

## เทสเดิมที่ชนและแก้แล้ว

`tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests::
test_no_foundation_module_implements_quest_or_shop_behavior` ชนคำว่า "trade" ในโมดูลใหม่ (การ์ดสถาปัตยกรรม
กันไม่ให้โมดูลไหนใน `src/pirateforce_foundation` implement quest/shop/trade behavior จริง) -- เพิ่ม
`"trade_session_membership.py": {"trade"}` เข้า `ALLOWED_HITS` พร้อมคอมเมนต์อธิบายเหตุผล (โมดูลนี้เป็นแค่
predicate ตรวจ identity ไม่มี cart/price/product logic เลย) ตามรูปแบบ exemption เดิมที่มีอยู่แล้วสำหรับ
`runtime.py`("quest") และ `world_port_royal_identity.py`("shop") -- ไม่ได้ทำให้การ์ดอ่อนลง แค่ยอมรับคำเดียว
ในไฟล์เดียวตามเหตุผลเดียวกับ exemption อื่น ๆ ที่มีอยู่ก่อนแล้ว

**ไม่ชน** `tests/test_mob_stat_fabrication_guard.py`'s `LANE_B_MODULES` (ต่างจาก job 2 ที่เคยชน) --
ไฟล์นี้ชื่อไม่ขึ้นต้น `mob_*` จึงไม่อยู่ในขอบเขตการ์ดนั้น ยืนยันด้วยสวีตเต็มผ่านหลังแก้จุดเดียว

## ตรวจก่อนคอมมิต (ไม่มี pf-adversary subagent ให้เรียกในสภาพแวดล้อมนี้ -- ตรวจเข้มเองแบบ adversarial)

- อ่านโมดูล `mob_combat_membership.py` (job 2, ผ่านการตรวจมาแล้วรอบก่อน) เทียบทุกบรรทัดกับโมดูลใหม่เพื่อให้
  โครง fail-closed เหมือนกันเป๊ะ ไม่มี branch แถมที่ widen การตัดสิน
- grep `TRADE_CMD_VITAL`/`TradeCmdVital` ทั่ว `runtime.py` สดเพื่อยืนยันจุดเสียบจริงก่อนเขียนดอกสตริง ไม่ใช่
  เชื่อเลขบรรทัดจากใบ RE-157 เดิม (พบว่าเลื่อนจาก `:6787` เป็น `:6925` จริง)
- ยืนยัน `shop_store5_open_sent`/`trade_store_close_capture_count` ใน `current/pf_login_game_server_v141.py`
  ตรงกับที่ใบ RE-157 อ้าง (ไฟล์ frozen จึงไม่ควรขยับ -- ตรวจแล้วตรงเป๊ะ `:3534`, `:4211-4223`)
- รันสวีตเต็มสองครั้ง (ก่อน/หลังแก้ `ALLOWED_HITS`) ยืนยัน 0 failed ทั้งคู่ยกเว้นจุดที่รู้สาเหตุแล้ว
- cp874-encodability: เช็คทั้งสองไฟล์ใหม่ผ่าน `.encode("cp874")` ตรง ๆ -- ผ่าน (โค้ด/ดอกสตริงเป็น ASCII
  ล้วน)
- ตรวจว่าไม่มีคำถามเปิดที่ยังไม่ตอบตกค้างในดอกสตริง (ทุกจุดที่ไม่รู้ระบุชัดว่า "chief's call" ไม่เดา)

## ยังไม่ได้พิสูจน์

- ว่า `ActiveStoreSession` contract (scene + actor เดียว + generation) ตรงกับ state จริงที่ `runtime.py`
  เก็บได้ไม่ต้องออกแบบเพิ่ม -- เหมือน job 2 เดิมที่ทิ้งคำถามนี้ไว้เป็นของ chief
- ว่า generation counter ของสอง guard (TradeCmd นี้ กับ mob-combat เดิม) ควรใช้ตัวเดียวกันหรือคนละตัว --
  ไม่เดา ทิ้งไว้ให้ chief ตัดสินตอน wire จริง

## ไฟล์ที่แตะ

`pirate-force-server`:
- `src/pirateforce_foundation/trade_session_membership.py` (ใหม่, 1 ไฟล์)
- `tests/test_trade_session_membership.py` (ใหม่, 1 ไฟล์, 9 เทส)
- `tests/test_npc_interaction_wire.py` (แก้ 1 จุด, เพิ่ม `ALLOWED_HITS` entry)
- `rounds/B_20260830_2050_n7vbxq_CLAIM.md` (ใหม่)

`pf_bridge`:
- `notes_to_chief/20260830_2050_LANE-B-STATUS-trade-session-membership-predicate-built-re157-job1.md`
  (ไฟล์นี้)
- `rounds/B_20260830_2050_n7vbxq_trade-session-membership-predicate-built.md` (ใหม่, round record เต็ม)

## ตัวเลขที่วัดได้

- `trade_session_membership.py`: 2 ฟังก์ชันสาธารณะ (`build_session`, `admits`), 1 `NamedTuple`, 9 เทส 9/9
  ผ่าน
- สวีตเต็ม `pirate-force-server` หลังแก้ครบ: **5541 passed, 327 skipped, 9706 subtests passed, 0 failed**
  (ขึ้นจาก R247 baseline 5537 passed 323 skipped -- ส่วนต่าง skip นับได้ 4 มาจาก environment ของเครื่องนี้
  เอง ไม่ใช่จากการแก้รอบนี้ -- ตรงกับที่โปรเจกต์เคยบันทึกไว้แล้วว่าตัวเลขขยับข้ามเครื่องได้
  (`FINDINGS_R106_R12_MEASURED_ON_A_SECOND_MACHINE.md`), ส่วนที่เพิ่มจริงจากรอบนี้คือ +9 เทสใหม่)
- `verify_hypothesis_ledger.py`: `PASS entries=47` ไม่มี drift

## CORE-REQUEST (ฝังในดอกสตริงโมดูล ไม่ได้จองเลขทะเบียนเอง)

สำหรับ chief, `runtime.py`, `_dispatch_with_lanes`: ก่อน fallback `actions = super().dispatch(parsed)`
(ปัจจุบันบรรทัด `6925`) เมื่อ `nested_id == legacy.TRADE_CMD_VITAL` ให้เรียก
`trade_session_membership.admits(self.active_store_session, scene_id=..., actor_identity=..., generation=
...)` แล้ว refuse (`return []`, log `trade_cmd_no_active_session_no_reply`) เมื่อ `False` และ stamp
`self.active_store_session` ด้วย `build_session()` เฉพาะตอน store-open frame ถูก queue จริงจาก announced
P91 identity (`v141:4433-4442`) พร้อม clear ที่ close command/scene handoff/census replace -- รายละเอียด
เต็มอยู่ในดอกสตริงโมดูล ไม่จองเลข `CORE-REQUEST-0XX` เอง (ตามธรรมเนียมเดียวกับ job 2) ให้ chief กำหนดเลขตอน
หยิบไปต่อสาย

## เปิดใบให้สาย C

none -- ไม่มีจุดไหนต้องเดาหรือวัดเพิ่มรอบนี้ที่ตอบเองไม่ได้จาก source ที่มีอยู่แล้ว

-- LANE-B
