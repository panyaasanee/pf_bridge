# GM รอบ `c637o1` -- 2026-09-02T02:31+07:00

## NOW.md -- อ่านเป็นไฟล์แรก (ตรวจสดรอบนี้)

แก้ล่าสุด 2026-09-02 01:48+07 โดย COO · "รอ Panya ติ๊ก" = **ว่าง** · "งานด่วนตอนนี้" ยังมี 3 ข้อ

| ข้อ | เขตสายนี้ไหม | รอบนี้ |
|---|---|---|
| P-1 ของดรอปค้างพื้น | ไม่ (สาย A/B) | ไม่แตะ |
| P-2 สีชื่อมอนสเตอร์ | ไม่ (Codex) | ไม่แตะ |
| P-3 ปุ่ม GM กดแล้วใช้ได้จริง | **ใช่** | ไม่ขยับ -- เหตุผลด้านล่าง |
| GM-A `/warp` ข้ามแมพ | ใช่ | โค้ดจบแล้ว รอ Panya รัน `GT-192` (กฎ NOW.md บรรทัด 19-21 = ไม่ใช่ตัวบล็อก) |
| GM-B `/speed` | **ใช่** | **ขยับรอบนี้ -- งานหลัก** |
| UI-A / UI-B / census latch | ไม่ | ไม่แตะ |

**รอบนี้ขยับ NOW ข้อไหน: GM-B** -- เงื่อนไข "ห้ามเงียบ" ของ `COO-DECISION 0147` ปิดครึ่งแรก
(log ฝั่งเซิร์ฟเวอร์ที่มี identity) · ครึ่งที่สอง (ข้อความบนจอ) เปิดใบถาม COO เพราะชนล็อกของ COO เอง

**ข้อที่ไม่ขยับและเพราะอะไร**
- **P-3** -- ตรวจสดรอบนี้ ไม่ copy จากรอบก่อน: `grep GAME_TEST_QUEUE.md` หา `GameMaster.dll`/`BT_GM`/
  `GMUI`/`P-3` = เจอเฉพาะใบเก่า (GT-107-R3, GT-164) · `ls -t notes_to_chief/*.md | head -25` ไม่มีใบ
  `ADDRESSEE: LANE-GM` ใหม่เรื่องนี้ ⇒ **ว่างเพราะรอ chief มอบสาย RE ต่อจาก `RE-104`**
  (ซอร์ส `GameMaster.dll` สายนี้ส่งครบแล้วรอบ `ku3jz6`/r2, PR #760 merge แล้ว)
- **P-1 / P-2 / UI-A / UI-B / census latch** -- ไม่ใช่เขตเขียนของสายนี้

## 1. ล็อกรอบ

`list_pull_requests(state=open)` ทั้งสอง repo: เปิดค้างอยู่ `[LANE-E] #781/#526` · `[LANE-A] #778/#524`
· `[LANE-B] #525` -- **ไม่มี `[LANE-GM]` สักใบ** ⇒ ล็อกของสายนี้ว่าง ยึดทันที
empty commit `round claim: c637o1` + draft PR ตั้งแต่วินาทีแรก:
`pf_bridge` **#782** · `pirate-force-server` **#527**

## 2. ชะตา PR รอบก่อน (ADDENDUM v2 ข้อ A)

รอบก่อน = `hw6dix` -> `pf_bridge#777` **merged=true** (19:02:53Z) · `pirate-force-server#523`
**merged=true** (19:12:22Z) ⇒ งานรอบก่อนอยู่บน `main` แล้ว ไม่มีอะไรต้อง cherry-pick

## 3. กล่องจดหมาย (ADDENDUM v2 ข้อ B)

`grep -l "ADDRESSEE: LANE-GM"` แล้วเทียบกับ `.CONSUMED.txt`:
**เจอใบเดียวที่ยังไม่มีใครบริโภค** -- `20260902_0147_COO-DECISION-speed-db-first-then-wire-refusal-must-be-visible.md`
บริโภคแล้วรอบนี้: stub + สำเนาเข้า `consumed/` · ผลของการบริโภคคือ**งานหลักของรอบนี้ทั้งรอบ**

อ่านเพิ่ม (ไม่ใช่ใบของสายนี้ แต่ผูกพัน): `20260902_0148_COO-DECISION-two-strike-rule-*`
cc ถึงสายนี้ -> รอบนี้รัน `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`
ก่อน push ตามข้อ 2 ของใบนั้น ผล **PREFLIGHT PASS (cp874 + no new skips)**

## 4. งานหลัก: บรรทัดปฏิเสธบอกได้แล้วว่าเป็นของคอนเนกชันไหน

### คำสั่งที่ต้องทำตาม
`COO-DECISION 2026-09-02T01:47+07:00` ยืนยัน **DB-ก่อน-ไวร์** (ถอดป้าย `[สมมติของสาย GM]` ออกจาก
ลำดับนั้นได้แล้ว โค้ดอยู่บน main ตั้งแต่ PR #523) แล้วผูกเงื่อนไขบังคับมาด้วย: **ห้ามเงียบ**
ทุกครั้งที่ปฏิเสธเพราะ DB ต้องมี (ก) ข้อความในแชทให้ GM เห็นทันที และ (ข) log ฝั่งเซิร์ฟเวอร์
หนึ่งบรรทัดที่มี **identity** และเหตุ

### (ข) ปิดรอบนี้
บรรทัด `GM_CHAT_NO_BYTES_SENT` มี "เหตุ" มาตั้งแต่รอบ `tvbiqc` แล้ว (`why=` + `blocked_on=`)
แต่ **ไม่มี identity** สิ่งที่มีคือ `account=` ซึ่ง docstring ของโมดูลเองบันทึกไว้ว่าเป็น
`--token` ระดับโปรเซส -- สตริงเดียวที่ทุกคอนเนกชันใช้ร่วมกัน จึงตอบ "แถวของใคร" ไม่ได้เลย

`_print_no_bytes_way_out` เติมสองฟิลด์ อ่านผ่านจุดอ่านเดิมที่ `_speed_action` ใช้เอง
(`_selected_speed_character_id` / `_selected_speed_identity` -- ทั้งคู่ defensive ไม่ raise):

```
GM_CHAT_NO_BYTES_SENT account='GM_ONE' command=speed why=refused_speed_persist_RuntimeError
  blocked_on='...' character_id=4242 identity=2864434397:287454020
```

`character_id` = rowid ที่ `/speed` เขียน = แถวที่ผู้เทส diff ในขั้นที่ 6 ของ `GT-193`
`identity=<lo>:<hi>` = คู่ที่เฟรมจ่าหน้า = จับคู่กับเฟรมที่ capture ได้
"ไม่มีตัวละครถูกเลือก" พิมพ์ `none` **ไม่ใช่ช่องว่าง** -- เป็นสถานะเดียวกับที่ `why=` บรรทัดนั้นบอกอยู่

### (ก) ทำไม่ได้ และไม่ได้แอบทำ
ทางส่ง **ข้อความตัวอักษร** server->client ที่พิสูจน์แล้วมีทางเดียว
`say_wire.make_say_broadcast_frame` (0x9F2C) และ action หนึ่งใบไป **ซ็อกเก็ตเดียว** คือของ GM เอง
จึงตรงกับที่ 0147 ต้องการทุกอย่าง ยกเว้นว่า `GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED = None`
ถูก `COO-DECISION 2026-08-29T00:41` ล็อกด้วยสามเงื่อนไขที่รอบนี้เคลียร์ไม่ได้สักข้อ:
(A) identity fix ใน `runtime.py` (เขต chief) · คำเคาะของ COO เอง · (B) จอ (GT-016/GT-133)
ครึ่ง RE ปิดไปแล้วโดย RE-132 (V=0) และ `tests/test_gm_say_gate_lock.py` มีไว้ให้ **แดง**
ถ้าสายไหนพลิกค่าคงที่นั้นเองเพื่อสนองคำสั่งใหม่ -- สายนี้จึง **ถาม ไม่พลิก**
ใบ `notes_to_chief/20260902_0229_LANE-GM-ASK-COO-speed-refusal-on-screen-needs-the-say-gate.md`
เสนอสามทางให้ COO เลือก (ก ข้อยกเว้นแคบเฉพาะบรรทัดปฏิเสธของ `/speed` บนซ็อกเก็ตของ GM เอง ·
ข ยอมรับ console-only ระหว่างรอ (A)+(B) · ค เปิด CORE-REQUEST ขอทางส่งใหม่ เช่น `0x8C77
GM_RunGMCommandResultVital` ซึ่ง layout เป็นของสาย RE ห้ามเดา)
**[สมมติของสาย GM - รอ COO ยืนยัน]: ระหว่างรอ เดินทาง ข ไม่หยุดรอ**

### 🔴 สิ่งที่รอบแรกของรอบนี้เขียนเกินจริง และแก้แล้วก่อน commit
สองฟิลด์นี้บอก **"แถวไหน" ไม่ใช่ "ใคร"** (pf-adversary D5 วัด): สองคอนเนกชันที่เลือกตัวละคร
เดียวกันพิมพ์ค่าเท่ากันเป๊ะ · `identity_hi` = 0 ทุกตัวละคร · เซิร์ฟเวอร์เดินทีละราย (R18)
ประโยคเดิมที่อ้างว่า "การรัน GT-193 หลายคอนเนกชันจับคู่ไม่ได้" ถูกตัดทิ้งแล้ว — เซิร์ฟเวอร์นี้
โฮสต์การรันแบบนั้นไม่ได้ตั้งแต่แรก

### วัดจริงรอบนี้ ไม่ใช่สมมติ: สี่สถานะแยกกันตรงไหน
COO ต้องการให้ผู้เทสแยก "พิมพ์ผิด" / "DB ไม่รับ" / "เฟรมส่งแล้ว" -- วัดผ่านเส้นทางจริง:
- **พิมพ์ผิด** `/speed not-a-number` `/speed inf` `/speed nan` `/speed 1e400` ถูกปฏิเสธที่
  `parse_gm_command` **เหนือ** `_speed_action` -> พิมพ์ `GM_CHAT_COMMAND_REFUSED ... usage='speed <value>'`
  คนละ **โทเคน** ซึ่งแยกสถานะได้แรงกว่าโทเคนเดียวกันคนละฟิลด์
- **เซิร์ฟเวอร์ตัดทิ้ง** (ใหม่รอบนี้) -> `GM_CHAT_DROPPED_BEFORE_DISPATCH ... why=rate_limited ...`
- **DB ไม่รับ** -> `GM_CHAT_NO_BYTES_SENT ... why=refused_speed_persist_* character_id=.. identity=..`
- **เฟรมส่งแล้ว** -> `LANE_GM_CHAT_ACTION speed route=action` และ **ไม่มี** บรรทัดปฏิเสธเลย

ผลพลอยได้ที่ต้องบันทึก: branch `refused_speed_<ExcType>` ของ `_speed_action` เอง
**เอื้อมไม่ถึงผ่านเส้นทางจริงวันนี้** เป็น defence in depth ต่อ `GmCommand` ที่ประกอบมือ
(ความซื่อสัตย์แบบเดียวกับที่ `SpeedCoverageHonestyTests` ประกาศไว้แล้ว) และเป็นเหตุผลที่จดหมายบอกว่า
identity ปิดให้เฉพาะสถานะฝั่ง DB ไม่ใช่สถานะพิมพ์ผิด

### เทส
`tests/test_gm_speed_action.py::TheRefusalNamesThisConnectionTests` 9 ใบ + double `_StoreThatReturnsNone`
ซึ่งต้องมีเพราะ `FakeStore` พูดเคสของ COO ไม่ได้ (`readback = None` แปลว่า "ใช้ค่า default"
ไม่ใช่ "คืน None") · สามเคสที่ COO สั่งชื่อมาเอง (parse ล้ม / DB คืน None / สำเร็จ) มีครบ
**mutation control ก่อน commit:** ลบสองฟิลด์ออก -> **5 ใบแดง** · เอา account token ไปใส่แทน
identity -> **6 ใบแดง**

## 5. เขียว

`python3 -m pytest tests/ -q` = **6663 passed · 327 skipped · 13821 subtests** เขียว(cloud sanity)
(ก่อนรอบนี้ 6638/327/13805 -- ส่วนต่างคือเทสใหม่ของรอบนี้เอง ไม่ใช่เทสที่เคยแดง
 ตัวเลขกลางรอบ 6647 คือก่อนแก้ทั้งเจ็ดข้อของ adversary)
`tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` = **PREFLIGHT PASS**
(cp874 236 ไฟล์ + ไม่มี skip marker ใหม่เทียบ origin/main) ตาม `COO-DECISION 0148` ข้อ 2

## 6. pf-adversary -- **เรียกจริง คืนผลแล้ว ไม่ approve เจอ 6 ข้อ + 1 suspicion แก้ครบทั้ง 7**

subagent รัน 21 นาที ทำ mutation test จริงใน worktree แยก แล้วลบ worktree ทิ้ง live tree สะอาด
**คำตัดสิน: NOT APPROVED** — เหตุผลของมันคือ "โค้ดไม่อันตราย แต่สามประโยคที่รอบนี้กำลังจะถูก merge
ด้วย วัดได้ว่าเท็จทั้งสามประโยค" ทั้งเจ็ดข้อแก้ในคอมมิตบน branch เดียวกัน **ก่อน**ปลด draft

| # | สิ่งที่มันวัดได้ | แก้อย่างไร | control |
|---|---|---|---|
| D1 | ประโยคหลักของรอบ "ทุกการปฏิเสธมีบรรทัด ไม่มีอะไรเงียบ" **เท็จ** — ยิง `/speed 400` 25 ครั้งรวด ได้ route line 20 แล้ว **เงียบสนิท 5** ที่ตัวจำกัดอัตราตัดทิ้ง (เพดาน 20/5 วิ ผู้เทสมือคนถึงได้) เหมือน "ไม่เคยต่อสาย" เป๊ะ | โทเคนที่สาม `GM_CHAT_DROPPED_BEFORE_DISPATCH` + `_print_server_drop_way_out` ครอบ rate limit · โควตา audit log · เขียน audit log ไม่ได้ (ทั้งสามเป็น `authorized=True` จึงพูดได้โดยไม่ผิดกฎ) รายชื่ออยู่ใน `chat_command.SERVER_SIDE_DROP_REFUSALS` ข้างค่าคงที่ | ถอดจุดเรียกออก -> **3 แดง** |
| D2 | **2 ใน 9 เทสใหม่เขียวทั้งที่ลบฟีเจอร์ทิ้งหมด** · เทสที่ตั้งชื่อว่ากัน mutant "เอา token มาใส่แทน identity" ถูกฆ่าด้วย `identity='GM_ONE'` — อัญประกาศตัวเดียว · เทส "forge ไม่ได้" ไม่ได้ลอง forge อะไรเลย | assert ด้วย **ค่าของฟิลด์** ไม่ใช่ substring · เทส forge จริงผ่านประตูเดียวที่มี (`.selected.id` เป็นสตริงมีขึ้นบรรทัดใหม่) · เทสใหม่ **สองแถวในโปรเซสเดียว** | hardcode -> เดิม **1 แดง** ตอนนี้ **12** · stale cache -> เดิม 1 ตอนนี้ตายด้วยเทสเดียวกัน |
| D3 | ประโยค "ทางส่งข้อความ server->client ที่พิสูจน์แล้วมีทางเดียว" **ถูกหักล้างด้วยหลักฐานของ repo เอง** — `docs/FUNCTIONAL_COVERAGE.json` แถว `chat_input_echo_hypothesis` = **`runtime_pass`** อ้าง GT-009 attended ว่าจอจริงเรนเดอร์ข้อความ echo บน `0xAC52` ขณะที่ `0x9F2C` ยังไม่มีใครเห็นบนจอเลย ⇒ ปิดทางเลือกที่สี่จาก COO โดยไม่ได้ตั้งใจ | เปิดไฟล์ยืนยันเอง (ไม่รับมาจาก subagent) แล้ว **ขีดฆ่า**ประโยคใน docstring + แก้จดหมาย เพิ่ม **ทาง ง** = เร่ง `PROMOTE-153` (OPEN เจ้าของ chief) พร้อมขอบเขตสี่ข้อว่าทำไมยังใช้วันนี้ไม่ได้ | -- (แก้คำอ้าง) |
| D4 | **อันตรายใหม่ที่รอบนี้สร้างเอง** — `/speed` ใบแรกของตัวละครที่ `speed_walk` เป็น NULL: commit 400.0 -> audit เขียนไม่ลง -> undo ไม่มีอะไรให้คืน -> แถวค้างที่ 400.0 **แต่บรรทัดพิมพ์ว่า "anything it had in hand was dropped with it"** ข้าง ๆ `character_id=` ที่ชี้แถวนั้นพอดี | คำที่สอง `WHY_AUDIT_ROW_NOT_WRITTEN_EFFECT_KEPT` + ประโยค "STILL IN PLACE -- read the row" · เดินสาย `reverted` จาก `_make_action` เข้า `_announce_console_outcome` (`None` = ไม่มีอะไรให้ undo ต่างจาก `False`) | ยุบกลับเป็นคำเดียว -> **1 แดง** |
| D5 | "`account=` ไม่ใช่ identity แต่สองฟิลด์นี้ใช่" **เกินจริง** — เป็น per-CHARACTER ไม่ใช่ per-connection · `select_character` ไม่มีด่านกันซ้ำ · `identity_hi`=0 ทุกตัว · และเซิร์ฟเวอร์เดินทีละราย การรันหลายคอนเนกชันที่อ้างถึงโฮสต์ไม่ได้อยู่แล้ว | แก้คำอ้างในโค้ด เทส จดหมาย และไฟล์นี้ ให้เป็น "แถวไหน" ไม่ใช่ "ใคร" | -- (แก้คำอ้าง) |
| D6 | ไฟล์ contract ของบรรทัดนี้เอง (`test_gm_chat_no_bytes_line.py`) **ไม่ครอบคลุมเลย** ลบสองฟิลด์ทิ้ง = **0 แดง** ในไฟล์นั้น · และ `FakeSelected` ของมันไม่มี identity เลย บรรทัดของอีกหกคำสั่งจึงกลายเป็น `identity=none` เงียบ ๆ | เติม `TheIdentityFieldsOnEveryCommandTests` + `TheServerSideDropLineTests` · `FakeSelected` มี identity แล้ว · ตรึงทั้งหกคำสั่ง | ลบสองฟิลด์ -> เดิม 0 แดงในไฟล์นี้ ตอนนี้แดงด้วย |
| D7 | (suspicion) สองฟิลด์ใหม่เป็นฟิลด์เดียวบนบรรทัดที่ **ไม่ผ่าน** `console_safe`/`_one_line` | ผ่านทั้งคู่แล้ว พร้อมเหตุผลว่าเป็นเรื่องวินัย ไม่ใช่ว่ามีช่องจริงวันนี้ | -- |

**mutation control วัดใหม่หลังแก้ครบ** (สามไฟล์เทส):

| mutant | ก่อน -> หลัง |
|---|---|
| ลบสองฟิลด์ | 5 -> **18 แดง** |
| เอา account token มาใส่แทน (แบบมีอัญประกาศ) | **0** -> **18 แดง** |
| hardcode เป็นค่าของ suite เอง | 1 -> **12 แดง** |
| สลับ lo/hi | 4 -> **14 แดง** |
| ไม่พิมพ์บรรทัด server-drop | -- -> **3 แดง** |
| ยุบ D4 กลับเป็นคำเดียว | -- -> **1 แดง** |

**ข้อที่ adversary ลองแล้วพังไม่ได้ (บันทึกเพราะเป็นส่วนหนึ่งของผล):** "diagnostic ห้ามเปลี่ยน
dispatch" ยังจริง · ทำให้ฟิลด์รั่วข้อความที่ GM พิมพ์ไม่ได้ · forge บรรทัดที่สองผ่านเส้นทางจริงไม่ได้
· ไม่ทำ grep ของ runbook/GT-193 พัง (ทั้งสองไม่เคย grep โทเคนนี้) · ไม่ได้พลิก say gate จริง ๆ
· สาขาปฏิเสธทั้งสิบของ `_speed_action` ถึงบรรทัดและมี identity ครบทุกตัว
**คำเตือนที่รับมาแต่ยังไม่แก้:** ประโยค "neither read raises" ในโค้ดนั้นจริงเฉพาะกรณีที่เอื้อมถึงวันนี้
(`getattr` กลืนแค่ `AttributeError`) -- ยกเป็น backlog ไม่ใช่ของรอบนี้

## ค้นแล้ว (กฎ "ค้นก่อนถอด")

- `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` -- **ค้นแล้ว: เจอ**
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` -- **ค้นแล้ว: เจอ**
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` -- **ค้นแล้ว: เจอ**
- ทางส่งข้อความตัวอักษร server->client อื่นในซอร์สนอกจาก 0x9F2C -- **ค้นแล้ว: ไม่เจอ**
- `GAME_TEST_QUEUE.md` หา `GameMaster.dll`/`BT_GM`/`GMUI`/`P-3` -- **ค้นแล้ว: เจอเฉพาะใบเก่า**
- `notes_to_chief/*CLAIM*` ที่อายุยังไม่เกิน 90 นาที -- **ค้นแล้ว: ไม่เจอ** และงานรอบนี้มาจากใบที่
  จ่าหน้า `ADDRESSEE: LANE-GM` สายเดียวอยู่แล้ว จึงไม่ต้องจอง
- รอบนี้ **ไม่ได้อ้างข้อเท็จจริงใหม่จาก client binary เลย**

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**สองอย่าง** — (1) grep คอนโซลบรรทัดเดียวแล้วรู้ว่า `/speed` ที่ถูกปฏิเสธเป็นของ **ตัวละครแถวไหน**
เมื่อวานทุกบรรทัดเขียน `account='GM_ONE'` ซึ่งคือ `--token` ระดับโปรเซส เหมือนกันทุกบรรทัด
ผู้เทสจึงบอกไม่ได้ว่าตรงกับแถวที่ตัวเองกำลัง diff ในขั้นที่ 6 หรือเปล่า
(2) **มีบรรทัดให้เห็นเลย** เมื่อพิมพ์ `/speed` เร็วเกินเพดาน — เมื่อวานได้ความเงียบสนิท
ซึ่งอ่านออกมาเหมือน "สายตายทั้งเส้น" ไม่ต่างกัน

## nonclaim

1. **ไม่อ้างว่า `GT-193` ผ่าน** และ **ไม่อ้างว่า GM-B ปิด** -- ไม่มี client อยู่ในหลักฐานรอบนี้เลย
   (กฎ NOW.md: โค้ดขึ้น main ไม่ใช่ "เสร็จ" ติ๊กได้โดย Panya คนเดียว)
2. **ไม่มีอะไรในรอบนี้เป็น client-observable** -- เป็น stderr ของโฮสต์เซิร์ฟเวอร์ล้วน GM ที่หน้าจอเกม
   ยังไม่เห็นอะไรเพิ่มจากเมื่อวานเมื่อ `/speed` ถูกปฏิเสธ นั่นคือครึ่งที่ใบถาม COO พูดถึงพอดี
3. **ไม่พลิก `GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED`** และไม่สร้างเส้นทางประกอบที่สองมาเลี่ยงล็อก
   (รอบ `GM_20260827_1415` เคยทำแล้วและถอนไปแล้ว)
4. ไม่แตะ `runtime.py` / `app.py` / `current/pf_login_game_server_v141.py` / canonical DB /
   `scenarios/world_*.json` / `scenarios/combat_*.json` / ไฟล์ของ LANE-DB / หัวใบของสายอื่นในคิว
5. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json` · client ยกระดับตัวเองไม่ได้ · ไม่ประกาศ milestone
6. ไม่ลบประวัติเดิม -- ประโยค "Two fields, both lane-authored" ต่อท้ายด้วยย่อหน้าใหม่ ไม่ได้ลบ ·
   ประโยค "ทางส่งข้อความเดียวที่พิสูจน์แล้ว" และคอมเมนต์ "STILL SILENT AFTER THIS ROUND" ใน
   `chat_command.py` **ขีดฆ่าพร้อมเหตุผล ไม่ลบ**
7. **ไม่อ้างว่าความเงียบหมดไปแล้ว** -- การปฏิเสธสี่ชนิดเหนือด่าน `is_gm` (ไม่ใช่ GM · บทสนทนาปกติ
   ของ GM · อ่านรายชื่อไม่ได้ · เฟรมพิการ) ยังเงียบโดยตั้งใจ และเขียนไว้ในซอร์สแล้ว
8. **ไม่อ้างว่าสองฟิลด์ระบุคอนเนกชันหรือระบุคน** -- ระบุ **แถว** เท่านั้น (D5)
9. **GM ข้ามขั้นไหน:** `/speed` เป็นคำสั่ง GM · บรรทัด log ที่อ่านออกช่วยผู้ปฏิบัติการเท่านั้น
   ไม่ใช่หลักฐานว่าเส้นทาง attribute ของผู้เล่นปกติทำงาน
10. ไม่อ้างว่าตัวเลขเขียวของรอบนี้ re-derive ได้ทุกเครื่อง -- ข้อสังเกต 60 ใบ passed->skipped
   ในไฟล์รอบ `hw6dix` ยังไม่ถูกไล่ทีละใบ ยังเป็น backlog

## backlog (ยกไปรอบหน้า พร้อมบอกว่าติดที่ใคร)

- **P-3 ปุ่ม GM** -- ติดที่ **chief** ยังไม่มอบสาย RE ต่อจาก `RE-104` (ซอร์ส `GameMaster.dll` ส่งครบแล้ว)
- **ครึ่ง (ก) ของ 0147 (ข้อความบนจอ)** -- ติดที่ **COO** ใบ `20260902_0229_LANE-GM-ASK-COO-*`
- **GM-A / GM-B** -- ติดที่ **Panya** รัน `GT-192` / `GT-193` (ไม่ใช่ตัวบล็อกสายตามกฎ NOW.md)
- **ประโยค "neither read raises"** ในโค้ด (adversary ชี้ว่า `getattr` กลืนแค่ `AttributeError`)
  -- ของสายนี้เอง ยกไปรอบหน้า
- **60 ใบ passed->skipped** ที่ต่างกันระหว่าง clone นี้กับ worktree ของ pf-adversary -- ยังไม่ไล่ทีละใบ

## ไฟล์ที่แตะ

`pirate-force-server` (เขต `gm/` + `tests/test_gm_*` + `docs/GM_LANE.md` เท่านั้น):
`src/pirateforce_foundation/gm/chat_command_action.py` · `src/pirateforce_foundation/gm/chat_command.py`
· `tests/test_gm_speed_action.py` · `tests/test_gm_chat_no_bytes_line.py` · `docs/GM_LANE.md`
`pf_bridge`: จดหมายใหม่ 1 ใบ + stub 1 + สำเนา `consumed/` 1 + ไฟล์รอบนี้

## PR

`pf_bridge` #782 · `pirate-force-server` #527
