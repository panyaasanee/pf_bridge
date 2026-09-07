# R390 · `fr81hi` · LANE-E (chief) — จ่าย CORE-REQUEST สามใบเป็นจุดเสียบ dispatch ใน PR เดียว

- เริ่ม 2026-09-07T16:52+07:00 · ล็อก `pf_bridge#1749` · กิ่ง `claude/keen-albattani-fr81hi` / `claude/adoring-turing-fr81hi`
- PR เซิร์ฟเวอร์ **`pirate-force-server#1054` เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` (GET ยืนยันแล้ว) รอ gate** — ยังไม่อยู่บน main
- VITAL_REGISTRY ยืนยันแล้ว (11,388 B) · heartbeat สะพาน `16:48` ตอนต้นรอบ ห่างน้อยกว่า 60 นาที
- `WIRED = 3 โมดูลที่ได้ emission จริงบน production path รอบนี้ (lane_gm_activity_cheat_code · lane_gm_unknown_vital_counter · จุดเสียบ op5 ที่ยังไม่มีโมดูลรับ) / 0 เลนใหม่ที่ production_allowed` — นับตาม WIRED v2 (import ไม่นับ) สองโมดูลแรก `production_allowed = True` อยู่แล้วและเพิ่งได้จุดเรียกจริงครั้งแรกในรอบนี้

## รอบนี้ขยับ NOW ข้อไหน
คิว chief ข้อ **(2) "CORE-REQUEST สามใบ PR เดียว"** — ปิดในรอบนี้ · ข้อ (1) `_Mirror` ปิดไปแล้วรอบก่อน
**ไม่ขยับ M ใด ๆ โดยตรง** และไม่อ้างว่าขยับ: ทั้งสามจุดเป็น seam ที่ไม่ส่งอะไรกลับ ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ
สิ่งที่ขยับคือ **ความสามารถในการวัด** ของสามสาย (GM P-3 แยก "ไคลเอนต์ไม่ส่ง" ออกจาก "ส่งแล้วเราทิ้ง" ได้ · DB เขียน hook ของตัวเองต่อได้โดยไม่ต้องขอ chief อีกใบ)

## ทำอะไร (5 ไฟล์ · ใน `#1054`)
| ใบ | สาขา |
|---|---|
| `20260906_1029` GM-062 | `if nested_id == ACTIVITY_CHEAT_CODE_VITAL_ID:` ใน `_dispatch_with_lanes` — นับเฟรม ยิง `vital_inbound_activity_cheat_code` ไม่ตอบอะไร · **import ค่าคงที่จาก `gm/activity_cheat_code_wire.py` ไม่ re-declare** · ตัวตนมาจาก `session.token` ไม่ใช่ payload |
| `20260906_1215` GM-063 | ตัวตรวจ "ไม่มีใครรับเฟรมนี้" ใน `dispatch()` |
| `20260906_1452` DB op5 | ท้ายบล็อก `ITEM_OPERATE_REQ_VITAL` — ยิง `vital_inbound_item_operate_op5` **ไม่มี `return` ไม่เรียก store ไม่บวก `rx_frames`** |
ลบ `registered_but_not_fired` ออกจากสอง hook module ในคอมมิตเดียวกับที่ยิงจุดนั้น (ไม่งั้น `FINDING_STALE_NEVER_FIRED_DECLARATION`) · พิน `tests/test_lane_gm_unknown_vital_counter.py` **ย้าย ไม่ได้ลบ** ไปเป็นรูป relation แบบเดียวกับ `test_lane_a_island_trigger_log.py`

## สองจุดที่ไม่ทำตามใบ และเหตุผลที่วัดมาแล้ว (เขียนไว้ในโค้ดและใน body ของ `#1054` ด้วย)
1. **GM-063 ไม่ได้อยู่ "ท้ายสายจ่ายงานตาม nested_id" ตามที่ใบขอ — เพราะจุดนั้นไม่มีอยู่จริง**
   `_dispatch_with_lanes` ยาว ~5,000 บรรทัด มี early return กระจายทั่วและมี `return` สุดท้าย **จุดเดียว** ซึ่งเป็นจุดที่ `TargetPos` และทุกเฟรมที่หาง lane ประกอบคำตอบให้ก็มาถึงเหมือนกัน ยิงตรงนั้น = บันทึก id ที่ **มีสาขารับ** ลง P-3 ซึ่ง docstring ของ hook เองบอกว่าเป็นความผิดพลาดข้อเดียวที่มันห้ามทำ
   ที่ลงจริง: ยิงเมื่อเฟรมนั้น **ไม่คืน action** และ **event ใหม่ทุกตัวเป็น `vital_walk_refused_unknown_vital_id` เท่านั้น**
2. **DB op5 = seam เปล่า ไม่มีพฤติกรรม** — ใบขอถึงขั้นเรียก `store.equip_item` + ประกอบ `ItemOperateVitalRes` ตอบกลับ นั่นคือพฤติกรรมใหม่ ซึ่ง COO เงื่อนไข (2) ห้ามในใบนี้ และตัวใบเองยังรอคำตอบ RE (`20260906_1449`) อยู่

## ผลลบ/สิ่งที่วัดแล้วและสองใบไม่รู้ (มีค่ากว่าที่คาดไว้ ส่งเป็นจดหมายถึง GM แล้ว)
- **`rx_frames` ถูกบวกบนเส้นทางกลาง** ที่เฟรมวิ่งผ่านไม่ว่าจะเกิดอะไรกับมัน — ร่างแรกของตัวตรวจใส่เงื่อนไข "`rx_frames` ไม่ขยับ" แล้ว **ยิงไม่ออกเลยสักเฟรม** (วัดด้วย `ItemOperateVitalReq` ที่ทุก reader ปฏิเสธ: ตัวนับยังขึ้นหนึ่ง)
- 🔴 **`vital_walk` บันทึก event ให้ id ที่ไม่มีใครรับอยู่แล้ววันนี้**: `_vital_walk_note_refusal` เหตุผล `unknown_vital_id` → event `vital_walk_refused_unknown_vital_id` (grep ของใบ GM-063 พลาดเพราะมันเป็น refusal **หลัง** walk ไม่ใช่ print ก่อน dispatch) ⇒ เงื่อนไข "ไม่มี event ใหม่" ก็ยิงไม่ออกเช่นกัน · event ตัวนี้ **คือ**บันทึกเดิมว่าไม่มีตารางไหนรับ id นั้น จึงเป็นข้อยกเว้นที่ถูกต้องข้อเดียว
- **เฟรมแรกของทุก session ประกอบ `RUNTIME_RES_ACK_FIRST_REQ`** (v141 `:3768` ครั้งเดียวต่อ connection) ⇒ เฟรมนั้นเฟรมเดียวต่อคอนเนกชันรายงานเป็น unknown ไม่ได้ตลอดกาล — บันทึกไว้เป็นข้อจำกัดที่รู้ ไม่ใช่บั๊กที่ซ่อน
- ตัวตรวจ **under-report โดยการออกแบบ** (สาขาที่บันทึก event แล้ว `return []` มองไม่เห็นจากตรงนี้ — ถูกต้องแล้ว) และ under-report = ความเงียบ ซึ่ง hook module ระบุเองว่าเป็นฝั่งที่กู้คืนได้

## หลักฐาน
- `pytest tests/` บนต้นไม้ที่ merge `origin/main` แล้ว เป็นคอมมิตสุดท้ายจริง: **13515 passed · 401 skipped · 0 failed** — **เขียว(cloud sanity)** python 3.11 · ไม่พูดแทนเกต Windows (เกตรัน 3.14)
- `tools_bridge/pf_gate_preflight.py --repo <server>`: **PREFLIGHT PASS**
- ไฟล์ข้างเคียงที่การแก้นี้แตะสัญญาด้วย: `test_gm_activity_cheat_code_dispatch.py` + `test_lane_a_island_trigger_log.py` + `test_gm_lane_gate_name_audit.py` = 118 passed, 407 subtests
- ไฟล์เทสใหม่ `tests/test_core_request_dispatch_seams_wiring.py` 12 เทส สามคลาส หนึ่งคลาสต่อหนึ่งสาขา (เงื่อนไข COO ข้อ 1)

## ลูกมือ
`ADVERSARY_PENDING pirate-force-server#1054` — สั่ง `pf-adversary` บนกิ่งนี้แล้ว ผลยังไม่คืนตอน push
🔴 **งานแรกของ chief รอบถัดไป = อ่านผล adversary ใบนี้แล้วจ่ายสิ่งที่มันเจอ** ก่อนไปคิวข้อ (3)

## QUEUE_TRIAGE
`QUEUE_TRIAGE:` รอบนี้ไม่มีรายการเข้า/ออก `GAME_TEST_QUEUE.md` — ไม่มีอะไรให้เทสบนจอจากรอบนี้ และเขียนเหตุผลไว้ตรงนี้ตามกติกา: ทั้งสาม seam **ไม่ส่งเฟรมกลับหาไคลเอนต์เลย** จึงไม่มีชั้น client-observable ให้ตั้งเกณฑ์ผ่าน · ใบที่ควรเกิดจากงานนี้เป็นของ **สายเจ้าของ** (GM ออกใบ P-3 ที่อ่าน `capture/gm_command_capture/` หลัง seam 0x6CEC ลง main · DB ออกใบตอนมี hook + คำตอบ RE) และเลขใบ/เนื้อใบ/สแนปช็อต = **LANE-K** ตาม `PANYA 1910`
`READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ:` ไม่ได้สำรวจรอบนี้ — รอบนี้ใช้โควตางานไปกับคิว chief ข้อ (2) ตามที่ NOW กำหนด "หนึ่งงานต่อรอบ" · การคัดกรองรอบถัดไปต้องทำ (กติกา "อย่างน้อยทุก 6 ชม.")

## รอบหน้าทำอะไร
1. 🔴 ผล `pf-adversary` ของ `#1054` (งานแรก)
2. คิว chief ข้อ (3): `gate-windows` เช็คเอาต์ `pf_bridge` + `fetch-depth: 0` — โทเคนที่ต้องมีคือรันที่ **แดงจริงเพราะจดหมายหาย** ไม่ใช่แค่ "ไม่ SKIP แล้ว"
3. ใบ `20260905_1922` GM-060 — COO สั่งอ่านให้จบและตัดสินในรอบเดียว (ค้างมาแล้ว ต้องไม่ค้างต่อ)
4. คัดกรองใบ attended + บรรทัด `READY/PENDING …` ให้ครบ
5. ใบ CORE-REQUEST ที่เหลือสองใบ: `20260907_0907` LANE-CS class gate · `20260907_1113` LANE-Q reward_store

SCOREBOARD: COMING | สามสายที่รออยู่ (GM สองใบ · DB หนึ่งใบ) มีจุดเสียบจริงใน runtime.py แล้ว: 0x6CEC ที่เคยถูกทิ้งเงียบตอนนี้ถึง hook ของ GM · เฟรมที่ไม่มีใครรับถูกนับต่อ session · op=5 (สวมอาวุธ) มี seam ให้ DB ต่อเองโดยไม่ต้องขอ chief อีก | pirate-force-server#1054 (เปิด รอ gate) · pf_bridge#1749
