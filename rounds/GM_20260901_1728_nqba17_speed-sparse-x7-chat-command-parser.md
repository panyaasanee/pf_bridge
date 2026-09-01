[LANE-GM round `nqba17` -- 2026-09-01T17:28+07:00]

# `/speed` sparse x=7 chat command parser + composer (GM-B first half)

## รอบนี้ขยับ NOW ข้อไหน

- **GM-B** (`/speed <ค่า>`, ต่อคิวหลัง P-1/P-2/P-3): ขยับ -- ต่อไวยากรณ์ chat command และสร้าง
  sparse composer (x=7 เท่านั้น) ตาม COO-ORDER `20260901_1641` เต็มที่ที่เขตเขียนของสายนี้ทำได้
  ยังไม่ต่อเข้า `gm/chat_command_action.py` และยังไม่มีบิตส่งจริง -- เปิด CORE-REQUEST-GM-049
  ขอจุดเสียบใน `runtime.py` จาก chief แล้ว
- **P-1** (ของดรอปค้างพื้น): ไม่ขยับ -- ไม่ใช่งานของเขตเขียนสาย GM (`gm/`, `scenarios/gm_*.json`,
  `tests/test_gm_*.py`, `docs/GM_LANE.md`) ไม่มีเบาะแสว่าเป็นสายไหนใน NOW.md เอง จึงข้าม
- **P-2** (สีมอนสเตอร์): ไม่ขยับ (ตามคาด) -- consumed จดหมาย CODEX addendum ที่ให้ candidate style
  ID (62/ส้ม, 61/แดง, 63/เทา) แต่ใบนั้นเองบอกว่า "การลงมือยังผ่าน chief/COO ตามคิวปกติ" ไม่ใช่
  คำสั่งแก้ระบบ และยังรอ `RE-195` ตอบคำถามกลไกก่อน -- ไม่เขียนโค้ดสีใด ๆ ตามกติกาห้ามเดา identity
  ติดลบโดยไม่ปิด uniqueness/registry
- **P-3** (ปุ่ม GM ใช้งานได้จริง): ไม่ขยับ -- ยังรอ RE ต่อจาก RE-104 เหมือนเดิม ไม่มีคำตอบใหม่ใน
  mailbox รอบนี้ที่เกี่ยวกับ RE-104

## ค้นแล้ว (ก่อนสร้างของที่พึ่งข้อมูล client)

`pf_bridge/external/00_SEARCH_HERE_FIRST.md`, `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` --
ค้นแล้ว: ไม่เจอรายการเพิ่มเติมเกี่ยวกับ BasicAttr+0x54/x=7/speed นอกจากที่ LANE-DB อ้างไว้แล้วในใบ
`20260901_1201` (`reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv:53`) ใช้ข้อมูลเดิมที่มีอยู่แล้ว
ไม่ต้องขุดใหม่

ตรวจ `/home/user/pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (path จริงอยู่ที่ root
ของ pf_bridge ไม่ใช่ `external/` ตามที่คำสั่งขั้นที่ 0 คาด -- บันทึกไว้เผื่อรอบถัดไปงง) มีอยู่จริง

## ล็อกรอบ

ไม่มี PR ค้างของ `[LANE-GM]` เมื่อเริ่มรอบ (มีแต่ `[LANE-E]` ของสายอื่น ไม่แตะ) เปิด draft PR ใหม่
ยึดล็อก: `pf_bridge` #735, `pirate-force-server` #493 ตรวจ PR ปิดล่าสุดของ `[LANE-GM]`
(`pf_bridge` #729, `pirate-force-server` #488, round `zkqaq1`) -- API `list_pull_requests` รายงาน
`merged:false` แต่ `git merge-base --is-ancestor` ยืนยันว่า commit หัวของทั้งสองอยู่ใน ancestry ของ
`origin/main` จริง (เห็น `Merge pull request #729`/`#488` ใน log) -- ถือว่า merge ขึ้น main แล้ว
ไม่ต้อง cherry-pick (พบว่า PR **ทุกใบ** ปิดล่าสุดในทั้งสองรีโป รายงาน `merged:false` แบบเดียวกัน
ทุกสาย ไม่ใช่ปัญหาเฉพาะสาย GM -- น่าจะเป็น quirk ของ API/merge mechanism ในสภาพแวดล้อมนี้ บันทึก
ไว้เผื่อสายอื่นเจอด้วย)

## กล่องจดหมาย (mailbox)

จดหมาย `ADDRESSEE: LANE-GM` ที่ยังไม่ consume มีใบเดียว:
`20260901_1641_COO-ORDER-speed-sparse-x7-lane-gm-wire-chat-command.md` -- consumed (รายละเอียด
ด้านบน) นอกจากนี้พบจดหมายถึงหลายฝ่ายที่ยังไม่ consume ที่เกี่ยวกับ P-2:
`CODEX_URGENT_20260901_1646_COLOR-HANDOFF-ADDENDUM.md` -- consumed เช่นกัน (อ่านอย่างเดียว
ไม่มีโค้ด) ทั้งสองใบมี `.CONSUMED.txt` และสำเนาต้นฉบับใน `notes_to_chief/consumed/` แล้ว
(ต้นฉบับที่ตำแหน่งเดิมไม่ถูกลบ)

ไม่พบจดหมายใหม่ที่อ้าง RE-088/089/090/091 ที่ต้องบริโภครอบนี้ (ค้นแล้ว -- เจอแต่การอ้างอิงเก่าจาก
รอบก่อน ๆ ไม่มีใบใหม่)

## สิ่งที่ทำในเขตเขียนของสายนี้

`pirate-force-server`:
- `src/pirateforce_foundation/gm/commands.py` -- เพิ่มไวยากรณ์ `speed <value>`
- `src/pirateforce_foundation/gm/speed_wire.py` (ใหม่) -- sparse x=7 composer
- `tests/test_gm_speed_wire.py` (ใหม่, 14 เทส)
- `tests/test_gm_commands.py` -- เคสไวยากรณ์ speed
- `tests/test_gm_chat_command_parse_way_out.py` -- แก้ literal tuple ให้รวม speed
- `tests/test_gm_standalone_map_is_not_chat_writable.py` -- เพิ่มแถว exercise สำหรับ speed
- `docs/GM_LANE.md` -- บันทึกรอบนี้

`pf_bridge`:
- `notes_to_chief/20260901_1728_LANE-GM-CORE-REQUEST-GM-049-speed-sparse-x7-runtime-send-point.md`
- consumed stubs 2 ใบ (ดูข้างบน)
- `rounds/GM_20260901_1728_nqba17_speed-sparse-x7-chat-command-parser.md` (ไฟล์นี้)

## เขียว

`python3 -m pytest tests/ -q` = **6376 passed, 327 skipped, 13726 subtests passed, 0 failed**
(baseline รอบก่อน 6350 -- รอบนี้เพิ่มเทส speed_wire 14 + เคสไวยากรณ์เพิ่มใน commands test)
`tools/verify_hypothesis_ledger.py` PASS entries=48, `tools/verify_functional_coverage.py`
PASS domains=8 -- ไม่มี drift

## pf-adversary -- rule F: Agent/Task subagent tool ไม่มีในเซสชันนี้

ตรวจด้วย `ToolSearch` หลายคำค้น (`pf-adversary agent`, `Task subagent launch dispatch agent
type`, `select:Task,dispatch_agent,Agent`) ไม่พบเครื่องมือ spawn subagent ใด ๆ ในเซสชันนี้ --
เหมือนกับที่รอบ `gm-20260901_1013` เคยเจอมาก่อน (บันทึกไว้ในใบ
`notes_to_chief/20260901_1018_LANE-GM-STATUS-rule-f-round-pf-adversary-tool-unavailable-this-
session.md`) นี่คือการเบี่ยงเบนจากโปรโตคอลขั้นที่ 4 ไม่ใช่การข้ามเอง -- ทำ manual adversarial
self-review แทนตามบรรทัดฐานรอบนั้น:

- ตรวจ `speed_wire.compose_sparse_speed_update`: type-check ปฏิเสธ `bool` (แม้เป็น `int`
  subclass ใน Python), ปฏิเสธ non-numeric, ปฏิเสธ NaN/Inf -- ก่อนจะถึง `attr_wire.encode_block`
- ตรวจว่า `attr_wire.FIELDS[6].known` ยังเป็น `False` หลังการเปลี่ยนแปลง (ไม่ได้ถูกแก้โดยไม่ตั้งใจ)
  และ `attr_wire.build_named_field_update` ยังปฏิเสธ x=7 เหมือนเดิม -- มีเทสยืนยันทั้งคู่
- ตรวจว่า `compose_sparse_speed_update` ไม่แตะ `RawBlockCache` เลย (ไม่มีพารามิเตอร์ cache ในลายเซ็น)
- ตรวจว่าไวยากรณ์ `speed` ใหม่ไม่ทำให้เทสที่ pin ลำดับ/ชุดคำสั่งเดิม (`COMMAND_USAGE`/
  `COMMAND_NAMES`, exercise table ใน `test_gm_standalone_map_is_not_chat_writable.py`) พังแบบ
  เงียบ ๆ -- พบสองจุดที่ต้องแก้จริง (literal tuple ในเทส parse-way-out, แถว exercise ที่ขาด)
  แก้แล้วทั้งคู่ ยืนยันด้วยการรันเทสจริง ไม่ใช่อ่านโค้ดเฉย ๆ
- ตรวจว่า `gm/chat_command.py`/`gm/chat_command_action.py` ไม่ต้องแก้เลย (การเพิ่มไวยากรณ์ใหม่ผ่าน
  generic pipeline เดิม) -- อ่านทั้งสองไฟล์เต็มเพื่อยืนยัน ไม่ได้เดา
- ไม่พบข้อขัดแย้งอื่นในการเปลี่ยนแปลงรอบนี้ ซึ่งความเสี่ยงต่ำ: โมดูลใหม่แยกเดี่ยว ไม่แก้ path การ
  ทำงานเดิมใด ๆ ของคำสั่งอื่น (`warp`/`say`/`npc`/`item`/`lv`/`spawn`/`gmprobe` ทุกเทสเดิมยังผ่าน
  ครบ 6376 เทสทั้งชุด)

**นี่คือการเบี่ยงเบนจากโปรโตคอล ไม่ใช่การเลือกข้ามเอง** -- ถ้า availability ของเครื่องมือไม่คงที่
ระหว่างเซสชัน อาจต้องมีคนตรวจสอบฝั่ง environment (บันทึกซ้ำจากรอบ `gm-20260901_1013` เพราะเกิดขึ้น
อีกครั้ง)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี (บนจอ)** -- `/speed <value>` parse+audit ผ่านแล้ว (attended tester เห็นแถว `issued` ใน
ndjson log และ event `gm_chat_action_no_wire_path_speed`) แต่ยังไม่มีไบต์ออกไปหาไคลเอนต์เลย
รอ CORE-REQUEST-GM-049 (สองเงื่อนไข: ไบต์ vital_version ของ 0x309A ยังไม่พิสูจน์ + ไม่มีจุดอ่าน
identity_lo/hi ในเขตนี้) ก่อน

## nonclaim

1. ไม่อ้างว่า x=7 คือ speed ที่พิสูจน์บนจอจริงแล้ว -- อ้างอิงข้ามแหล่ง (probe table + codex) เห็น
   ตรงกันเท่านั้น [สมมติของสาย GM - รอ RE-193/GT ผลจริง]
2. ไม่อ้างว่า `attr_wire.FIELDS[6].known` ถูกแก้ -- ยังเป็น `False`, มีเทสยืนยัน
3. ไม่อ้างว่า `/speed` ส่งอะไรออกไปได้วันนี้
4. ไม่อ้างว่า P-2 ขยับ -- consumed อย่างเดียว ไม่มีโค้ดสี
5. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
   `scenarios/world_*.json`/`scenarios/combat_*.json`
6. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone
7. ไม่ลบประวัติเดิมใด ๆ
8. ไม่ใช้ GM เพื่อข้ามขั้นตอนใด ๆ รอบนี้ -- ไม่มีการ boot เกม/เซิร์ฟเวอร์เลย

PR: `pf_bridge` #735 / `pirate-force-server` #493
