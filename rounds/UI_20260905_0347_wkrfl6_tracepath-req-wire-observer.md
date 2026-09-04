# LANE-UI round `wkrfl6` — `CTracePathReqVital` (auto-walk trigger) wire decode + observer hook, CORE-REQUEST for the one dispatch line

เวลา: 2026-09-05 03:47 +07:00 (`TZ=Asia/Bangkok date`)

## รอบนี้ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
**ไม่ขยับ M-ladder** (M2 คงเดิม — ตัวบล็อกเดียวที่เหลือยังเป็นของ chief, ไม่ใช่ของสายนี้) และ**ไม่ปิด
"รอเครื่องคุณ" ข้อไหนใหม่** ทุกงานที่ผู้เล่นเห็นได้ตรงๆ ในคิวของสายนี้ยังบล็อกเหมือนรอบก่อน (`hq4wtb`):
UI-A/UI-B บล็อกที่ `RE-189` (client-local-only field ไม่มีเฟรมเขียนถึง) · auto-walk บล็อกที่ `RE-236(ข)`
รออีกรอบ attended · ร้านค้า NPC บล็อกที่ CORE-REQUEST `0621` รอ LANE-DB — งานรอบนี้เป็นการ**เตรียมทาง**ให้
รอบ attended ที่จะปิด `RE-236(ข)` ทำได้เร็วขึ้น/พลาดยากขึ้น (ดูหัวข้อ "ทำอะไร") ไม่ใช่การขยับ NOW/M เอง

## ลำดับตาม §7
1. `git fetch origin main` ทั้งสองรีโป (bridge → `e7f5283`, server → `2ff1e30`) · `checkout -B` จาก
   `origin/main` ทั้งสองฝั่ง · list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — **ไม่มี** (ตรวจต้นรอบ; PR ที่เปิดอยู่
   ตอนนี้เป็นของ LANE-A/B/DB/CS/GM ทั้งหมด) ⇒ ไม่ต้องถอย · claim `claude/lane-ui-round-wkrfl6` (pf_bridge
   เท่านั้น) — ไฟล์นี้แทนที่ claim ชั่วคราวตามกติกา
2. รอบก่อน (`hq4wtb`, 02:18) ไม่มี `ADVERSARY_PENDING` ค้าง (adversary รอบนั้นคืนผลก่อน push แล้วแก้ครบ)
3. กล่องจดหมาย: `grep -l "^ADDRESSEE: LANE-UI" notes_to_chief/*.md` ข้าม `.CONSUMED.txt` — **ไม่มีใบใหม่**
   (ใบเดียวที่ pattern แบบ substring จับได้คือ `0332` ซึ่งคือไฟล์พรอมป์ประจำสายนี้เอง ไม่ใช่จดหมายสั่งงาน —
   ตรวจแล้วด้วย `^ADDRESSEE:` เป๊ะ ไม่ใช่ substring match)
4. สั่ง `pf-adversary` ระหว่างรอบ (ก่อนสรุปงาน ไม่ใช่ก่อน commit) — **ดูหัวข้อ ADVERSARY ด้านล่าง: ยังไม่คืนผล
   ตอนเขียนไฟล์รอบนี้** ⇒ `ADVERSARY_PENDING` บันทึกไว้ รอบหน้าหยิบเป็นงานแรก

## ตรวจงานสำรองของรอบก่อน (`hq4wtb`) ก่อนเริ่มคิวใหม่
1. chief ตอบใบ `0203` (ขอเลข GT คู่กับ `RE-237`) แล้วหรือยัง — **ยัง**: `GAME_TEST_QUEUE.md`'s `GT-253`
   ยังเขียนหัวว่า `BLOCKED -- เนื้อใบ RE-237 ยังไม่ถูกเขียน` ทั้งที่ `CLIENT_RE_QUEUE.md`'s `RE-237` เองบอกว่า
   เนื้อใบเขียนแล้วตั้งแต่รอบ `hq4wtb` (ก่อนรอบนี้กว่าชั่วโมง) — **หัวใบ `GT-253` ค้างข้อมูลเก่า** บันทึกเป็น
   nonclaim ให้ chief เห็นเวลากวาดคิว (`QUEUE_TRIAGE`, `PANYA-DECISION 20260904_2148`) ไม่ใช่ของแก้เอง
   (ไฟล์ `GAME_TEST_QUEUE.md` ไม่ใช่เขตเขียนของ LANE-UI)
2. ผล `GT-184`/`GT-186` จากกิ่งทิ้ง `HYP-PF-040` (`e678a37`, ka1-A) — **ยังไม่กลับมา** (grep
   `HYP-PF-040`/`e678a37`/`GT-184`/`GT-186` ใน `notes_to_chief/` หลัง `2120` = ไม่มีไฟล์ใหม่) ไม่บล็อกสายนี้
   รอต่อ
3. CORE-REQUEST `0621` (LANE-DB เงิน/กระเป๋าร้านค้า NPC) — grep `notes_to_chief/*LANE-DB*` ล่าสุด (`2357`)
   ยังเป็นเรื่อง `class_id` backfill/scene-select ไม่ใช่ร้านค้า — ยังไม่ถึงคิว

## ทำอะไร — `CTracePathReqVital` (0x4391) wire decode + observer hook (เตรียมทาง RE-236(ข))
คิวข้อ 4 ("เดินไปหา NPC/มอนอัตโนมัติ") ต้องรู้เฟรมที่ client ส่งก่อน — เฟรมนั้นคือ `CTracePathReqVital`
(ยืนยันจาก `GT-246`/R310: คลิกมินิแมปยิง `0x4391` 25 ไบต์ ไม่ใช่ `TargetPosVital` ตามที่สารบัญเดิมเดาไว้)
`trace_path.py` (chief/LANE-A) จัดการ opcode นี้อยู่แล้ว (ตอบ empty-vector เลิกอาการ "finding path..."
ค้าง) แต่ไม่เคยอ่าน payload ของ request เลย — schema ของ payload เต็มอยู่แล้วใน
`external/PF_SERIALIZER_FIELDS.tsv:5521-5528` (8 ฟิลด์, RE-119 STATIC-ON-BRIDGE) และผมตรวจกับเฟรมจริงที่
`GT-246` จับไว้แล้ว (byte-exact 8/8 ฟิลด์ ไม่มีไบต์เหลือ — ผลตรงกับที่ `RE-236`'s static bonus รอบก่อน
คำนวณด้วยมือไว้แล้ว)

รอบนี้เขียน:
1. `src/pirateforce_foundation/ui_tracepath_wire.py` (ใหม่) — pure encode/decode, ไม่มี guess ความหมาย
   field ไหนเลย (field1 ที่ `RE-236(ข)` ยังถามอยู่ — "discriminator" — เก็บชื่อ positional `field1_u16`
   ไม่ตั้งชื่อว่า quest_id/npc_id/list_index)
2. `src/pirateforce_foundation/lane_hooks/lane_ui_tracepath_wire_log.py` (ใหม่) — observer log-only
   เหมือนพี่น้องสี่ตัวจาก `CORE-REQUEST 1120` (friend×2/mail×3/party×2/trade×1) เป๊ะ ลงทะเบียนจุด
   `vital_inbound_trace_path_req_vital` — **ยังไม่ fire จริง** (ไม่มีอะไรใน `runtime.py` เรียก จนกว่า chief
   จะรับ CORE-REQUEST ด้านล่าง) ประกาศ `registered_but_not_fired = (...)` (กลไกเดียวกับ
   `lane_gm_chat_command.py`'s `vital_inbound_chat_local_talk`) ให้ `gm/lane_gate_name_audit.py`'s
   dead-hook-point scan ผ่านโดยสุจริต ไม่ใช่การกดปิดเสียงเฉยๆ
3. `src/pirateforce_foundation/ui_social_wire.py` — เพิ่ม `u16tag`/`u32tag` (encoder) และ `read_u16tag`
   (decoder) — ไม่เคยมีมาก่อนเพราะ 8 คลาสเดิมของ `CORE-REQUEST 1120` ไม่มีตัวไหนต้องเขียน u16 บนสาย
   (มีแต่ทิศอ่าน `read_u32tag`/`read_u8tag`/`read_u64tag`) `CTracePathReqVital` เป็นตัวแรกที่ต้อง
4. เทส: `tests/test_ui_tracepath_wire.py` (ใหม่) — round-trip สังเคราะห์ + **เทียบกับเฟรมจริงที่ `GT-246`
   จับไว้ byte-exact ทั้งสองทิศ** (encode field values กลับไปต้องตรง hex เดิมเป๊ะ, decode hex เดิมต้อง
   ได้ field values เดิมเป๊ะ) — แข็งกว่า round-trip สังเคราะห์เฉยๆ เพราะเทียบกับหลักฐานนอกโมดูล ไม่ใช่แค่
   ตรวจตัวเองย้อนกลับ · `tests/test_ui_lane_hooks_wire_log.py` (แก้) — ขยายตาราง `_CASES` เดิม 8→9 จุด,
   4→5 โมดูล · `tests/test_ui_social_wire.py` (แก้) — เพิ่มเทสให้ primitive สามตัวใหม่

### CORE-REQUEST ถึง chief (ไฟล์แยก ไม่ใช่แก้ `runtime.py` เอง)
`notes_to_chief/20260905_0347_LANE-UI-CORE-REQUEST-fire-trace-path-req-observer.md` — ขอบรรทัดเดียวที่
`runtime.py:7487` (ใน branch `if nested_id == trace_path.TRACE_PATH_REQ_VITAL_ID:` เดิม, หลัง
`self.rx_frames += 1`): `lane_hooks.fire("vital_inbound_trace_path_req_vital", session=self,
payload=bytes(parsed.nested_payload))` — ก็อปรูปแบบตรงจาก `_FRIEND_MAIL_PARTY_TRADE_DISPATCH`'s
dispatch site เดิม (`runtime.py:8514-8555`) ไม่เปลี่ยน logic เดิมของ branch นี้แม้แต่บรรทัดเดียว
(empty-vector reply ของ CORE-REQUEST-025 ต้องเหมือนเดิมทุกประการ — `fire()` ไม่มี return value)
รับใบแล้วต้องลบ `registered_but_not_fired` ออกในรอบเดียวกันด้วย (เอกสารของกลไกเองบังคับ)

### ทำไมงานนี้ไม่ต้องรอ `RE-236(ข)` ปิดก่อน
`fire()`/hook ไม่ตัดสินความหมาย field ใดๆ เลย เป็นแค่ observer พิมพ์ค่า positional — ประโยชน์คือรอบ
attended ถัดไปที่จะปิด `RE-236(ข)` (สองคลิก GO! เป้าไม่ชน id เทียบ `u16@+0x14`) จะพิมพ์ค่าทั้งแปดฟิลด์
ออกคอนโซลเซิร์ฟเวอร์**ทันทีที่คลิก** แทนที่จะต้อง capture hex ดิบแล้วถอดมือหลังบูตแบบที่ `RE-236`'s static
bonus รอบก่อนทำ — ลดโอกาสพลาดของรอบ attended ที่ยังไม่มีกำหนด ไม่ใช่การข้ามคิว P-2/ตีมอน/เควสใดๆ

## ADVERSARY
สั่งระหว่างรอบ (ก่อนสรุปงาน) — **🔴 ยังไม่คืนผลตอนเขียนไฟล์รอบนี้และตอน push** ⇒ `ADVERSARY_PENDING #788`
(pirate-force-server) — รอบหน้าของสายนี้หยิบผลเป็นงานแรกก่อนคิวอื่นตามกติกา
`0903_2345`/`AGENTS.md` §7 · **ห้ามเขียนว่า "ผ่าน adversary" ก่อนผลคืน** — ยังไม่เขียน

## เช็คที่ทำเองก่อน push (นอกเหนือ adversary)
- guard คำสงวน (`quest`/`shop`/`store5`/`price`/`reward`/`trade`) — รันสแกน tokenize เดียวกับ
  `tests/test_npc_interaction_wire.py` ใช้จริง มือ: `ui_tracepath_wire.py` (ไฟล์ระดับบนที่ guard สแกน)
  **0 hit**
- `git fetch origin main` แล้ว merge เข้ากิ่ง (branch สร้างจาก `origin/main` สดตั้งแต่ต้นรอบ ไม่มี commit
  ใหม่ระหว่างทาง — `git merge-base --is-ancestor origin/main HEAD` ผ่าน) รันชุดเต็มครั้งเดียวตามกติกา
  `1428`/`0053`/`0149`: **รอบแรกพบแดงจริง 1 ใบ** (`tests/test_gm_lane_gate_name_audit.py::DeadHookPointTests::
  test_the_repository_registers_no_hook_point_that_nothing_fires` — จุดที่คาดไว้เป๊ะ: hook ใหม่ยังไม่มี
  `fire()` จริง) แก้ด้วย `registered_but_not_fired` declaration (ข้อ 2 ของหัวข้อ "ทำอะไร") แล้วรันซ้ำ
  **10442 passed, 327 skipped, 19656 subtests passed** เขียว — ไม่มี skip ใหม่จากไฟล์ของรอบนี้ (grep
  "skip" ในไฟล์ที่แก้/เพิ่มทั้งหมด = 0 hit) ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census` เพิ่ม (กติกานั้นบังคับ
  เฉพาะรอบที่เพิ่ม skip ใหม่)
- `python3 -V` = `3.11.15` (คลาวด์ — ต่างจาก 3.14 บนเกตจริง ตามที่ `2348` บันทึกไว้แล้วว่าไม่ใช่ regression)

## ส่งอะไร (SHA/PR)
- `pirate-force-server`: **PR #788** หัว `[LANE-UI] round wkrfl6: CTracePathReqVital wire decode +
  observer hook` กิ่ง `claude/keen-gates-a8zk3x` จาก `origin/main` (`2ff1e30`) — ไฟล์ใหม่
  `ui_tracepath_wire.py`,
  `lane_hooks/lane_ui_tracepath_wire_log.py`, `tests/test_ui_tracepath_wire.py` · แก้
  `ui_social_wire.py`, `tests/test_ui_social_wire.py`, `tests/test_ui_lane_hooks_wire_log.py`
- `pf_bridge`: PR หัว `[LANE-UI] round wkrfl6: claim` กิ่ง `claude/wizardly-knuth-a8zk3x` จาก `origin/main`
  (`e7f5283`) — จดหมายใหม่ (`0347` CORE-REQUEST ถึง chief) + ไฟล์รอบนี้ (แทน `_claim.md`)
- ไม่มีเลข GT/RE/CORE-REQUEST ใหม่จากสารบัญ — CORE-REQUEST ใบนี้อ้างเลขที่มีอยู่แล้ว (`RE-119`, `RE-236`,
  `GT-246`, `CORE-REQUEST-025`, `CORE-REQUEST 1120`) ไม่ได้จองเลขใหม่

## nonclaims
① ไม่ปิด `RE-236(ข)` — hook ยังไม่ fire จริงจนกว่า chief จะรับ CORE-REQUEST ข้างบน และต่อให้ fire แล้ว
ก็เป็นแค่เครื่องมือช่วยอ่าน ไม่ใช่การตัดสินความหมาย field1 เอง (ต้อง attended สองคลิก GO! เป้าไม่ชน id
ตามที่ `RE-236` เขียนไว้)
② ไม่ยืนยันว่า `parsed.nested_payload` คือชื่อตัวแปรจริงที่ `runtime.py:7487` — เดาจากจุด dispatch อื่นใน
เมธอดเดียวกัน (บรรทัด 8514) เพราะไม่ใช่เขตเขียนของผม อ่านได้แต่ไม่แก้เดา (ดูรายละเอียดในจดหมาย CORE-REQUEST)
③ ไม่แตะ `trace_path.py`'s empty-vector reply logic หรือข้อห้ามของ `RE-119` T4 ("ห้ามสร้าง response แบบมี
เนื้อจาก request field") เลยแม้แต่น้อย
④ ไม่มีไบต์ใหม่ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ (pure module + log-only hook ที่ยังไม่ fire)
⑤ ไม่ยืนยันความหมาย field1 (`+0x14`) — สามทางเดิม (quest id/NPC id/list index) ยังเปิดเท่ากับตอนต้นรอบ
⑥ ไม่แก้หัวใบ `GT-253` ที่ค้างข้อมูลเก่า (ข้อ 1 ของ "งานสำรอง") — ไม่ใช่ไฟล์ในเขตเขียน บันทึกให้ chief เห็น
เฉยๆ
⑦ ADVERSARY_PENDING รอบนี้ — ดูหัวข้อ ADVERSARY ข้างบน

## งานสำรอง (พร้อมเริ่มได้ทันทีรอบถัดไปถ้างานหลักติด — ตาม `PANYA 1450` ข้อ 6)
1. **หยิบผล `pf-adversary` เป็นงานแรกก่อนคิวอื่น** (`ADVERSARY_PENDING` ข้างบน) — แก้ตามผลถ้ามีข้อบกพร่องจริง
2. เช็คว่า chief ตอบ CORE-REQUEST `0347` (ใบนี้) แล้วหรือยัง — ถ้า `runtime.py:7487` มี `fire()` จริงแล้ว
   ลบ `registered_but_not_fired` ออกจาก `lane_ui_tracepath_wire_log.py` ในรอบเดียวกัน (บังคับตามกลไกของ
   `gm/lane_gate_name_audit.py`)
3. เช็คว่า chief ตอบใบ `0203` (เลข GT คู่กับ `RE-237`) หรือแก้หัว `GT-253` ที่ค้างแล้วหรือยัง

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
1. เช็คงานสำรองข้อ 1-3 ข้างบนตามลำดับ
2. ถ้าไม่มีอะไรขยับ กลับไปอ่านสารบัญ 15 แถวเดิม (`0400`) หารายการที่ RE ใบใหม่ปิดระหว่างที่ผ่านมาแต่ยังไม่ถูก
   ต่อสาย

— LANE-UI (round `wkrfl6`)
