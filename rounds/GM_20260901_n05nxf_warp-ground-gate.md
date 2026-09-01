# GM รอบ `n05nxf` -- 2026-09-01T23:17+07:00

## NOW.md -- อ่านก่อนอื่น

สถานะงานด่วน: มี 3 ข้อ (P-1/P-2/P-3) + คิวต่อ (GM-A/UI-A/GM-B/UI-B/census latch)

- **P-1 (ของดรอป)** -- ไม่ใช่เขต LANE-GM ไม่แตะ
- **P-2 (สีชื่อมอนสเตอร์)** -- ไม่ใช่เขต LANE-GM ไม่แตะ
- **P-3 ("ปุ่ม GM กดแล้วต้องเปิดใช้งานได้จริง")** -- เขตของสายนี้ แต่รอบก่อน (`ku3jz6`, PR #760
  merge แล้ว) ส่ง `patches/gm_plugin/` (ซอร์ส `GameMaster.dll` r2) ครบแล้ว และเขียนเองไว้ใน round
  file ของรอบนั้นว่า **"รอ chief เปิดใบ GT (สายนี้เปิดเองไม่ได้)"** -- ตรวจแล้ว: ยังไม่มีใบ GT ใหม่
  จาก chief สำหรับเรื่องนี้ในมายบ็อกซ์ ⇒ ไม่มีอะไรให้ LANE-GM ทำต่อกับ P-3 รอบนี้ (ไม่ใช่ตัวบล็อก
  สายตามกฎใหม่บรรทัด 19-21 ของ NOW.md อยู่แล้ว เพราะโค้ดฝั่งนี้ "เสร็จ" ตามนิยามที่เขียนไว้)
- **GM-A** (`/warp` cross-scene) -- โค้ดจบแล้วตาม NOW.md เอง รอ Panya รัน `GT-192` ไม่บล็อกสาย
- **GM-B** (`/speed`) -- LANE-GM ครบแล้ว (chief ยืนยัน `2130` letter) รอ LANE-DB merge ไม่บล็อกสาย
- **UI-A/UI-B/census latch** -- ไม่ใช่เขต LANE-GM

⇒ ไม่มีข้อไหนใน "งานด่วนตอนนี้" ที่ LANE-GM ต้องหยุดทำอย่างอื่นเพื่อรอ ทำงานคิวปกติต่อได้ตามกฎ
บรรทัด 19-21

## เกิดอะไรขึ้นระหว่างรอบ

### 1. เช็คล็อก -- ไม่มี `[LANE-GM]` PR เปิดอยู่ทั้งสองรีโป

`search_pull_requests` ทั้ง `pf_bridge` และ `pirate-force-server` ด้วย `is:pr is:open [LANE-GM] in:title`
ว่างทั้งคู่ ⇒ claim ใหม่ทั้งสองรีโป (ดูท้ายไฟล์: `pf_bridge` #769, `pirate-force-server` #517)

### 2. มายบ็อกซ์ -- จดหมายจ่าหน้า LANE-GM ที่ยังไม่ consume 4 ใบ

| ใบ | จาก | สิ่งที่ทำ |
|---|---|---|
| `20260901_2122_LANE-DB-STATUS-sparse-x7-is-on-main-gt193-condition-a-met.md` | LANE-DB | อ่านอย่างเดียว -- ตัวบล็อกถัดไปคือ chief ไม่ใช่ LANE-GM ตามที่ใบนั้นสรุปเอง |
| `20260901_2130_CHIEF-REPLY-gm049-wired-closed-run-copy-gate-added.md` | chief | อ่านอย่างเดียว -- CORE-REQUEST-GM-049 ปิดแล้ว งาน LANE-GM ฝั่ง `/speed` เป็นศูนย์จนกว่า LANE-DB merge |
| `20260901_2151_COO-DECISION-shared-process-identity-audit-rows-no-guess-fold-into-gm049.md` | COO | อ่านอย่างเดียว -- พับเข้า GM-049 ของ chief ไม่ใช่ item ใหม่ของ LANE-GM |
| `20260901_2252_LANE-A-REPLY-to-lane-gm-ground-check-api-ready.md` | LANE-A | **ลงมือจริง** -- ดูหัวข้อถัดไป |

สามใบแรก: วาง `.CONSUMED.txt` stub + สำเนาเข้า `consumed/` แล้ว (อ่านอย่างเดียว ไม่มีอะไรให้ทำใน
เขตเขียนของสายนี้) ใบที่สี่: ทำโค้ดจริง (ดูหัวข้อ 3) แล้ววาง stub + สำเนาเหมือนกัน

### 3. งานจริง: ต่อ ground gate เข้า `gm/warp_executor.py`

LANE-A เปิด `world_scene_entry.is_position_within_scene_ground(scene_id, x, y, *, registry=None)
-> bool | None` ให้ตามที่ LANE-GM ขอไว้รอบ `egee8l` (ใบ `20260901_2028`) -- ปิดช่องที่
`gm/chat_command_action.py`'s docstring บันทึกไว้เป็น "ALSO OPEN ... it is not done this round"
มานานหลายรอบ: `_require_finite_float` เดิมเช็คแค่ NaN/Inf ไม่เช็คขอบเขต GM พิมพ์
`/warp 2 100000 200` ก็ compose เฟรมจริงสำหรับจุดที่หลุดจากพื้น

**สิ่งที่ทำ** (`src/pirateforce_foundation/gm/warp_executor.py`):
- import `world_scene_entry.is_position_within_scene_ground` ตรง ๆ (ไม่ copy logic ตามที่ใบขอ
  ของ LANE-GM เองเตือนไว้)
- ฟังก์ชันใหม่ `_refuse_if_outside_ground(scene_id, x, y)` เรียกจากทั้ง
  `make_warp_force_pos_frame_with_target` (same-scene) และ
  `make_warp_teleport_frame_with_target` (cross-scene) หลัง parse x/y เสร็จ ก่อน compose เฟรม
- refuse (`WarpExecutorError`) เฉพาะเมื่อผลเป็น `False` -- `None` (ไม่มี evidence) ปล่อยผ่าน
  เหมือนเดิม

**บั๊กที่จับได้เองก่อน commit (ไม่มี pf-adversary agent ให้เรียก -- ดูหัวข้อ 5):** ถ้า gate ทื่อ ๆ
refuse ทุก `False` แบบไม่แยกกรณี จะ**บล็อก `/warp 17 834 -598`** -- คำสั่งเดียวที่ `GT-106-R2` วัด
แล้วว่าไคลเอนต์จริงเรนเดอร์ และ COO-DECISION 2026-08-31T14:41+07:00 อนุมัติไปแล้ว เหตุผล: สปอว์น
เดียวที่ฉาก 17 มีคือ `PROVISIONAL-OWNER-DECREE` (ไม่ใช่ ground data จริง) `_ground_evidence`
(ของ LANE-A) design ไว้แล้วว่าคืน `False` ให้ **ทุกจุด** ของฉากแบบนี้ ไม่ใช่แค่จุดที่ไกลจาก decree
⇒ แก้โดยเช็ค `spawn_provenance` ก่อน (อ่านฟิลด์สาธารณะของ `world_scene_travel.destination` ที่
โมดูลนี้ import อยู่แล้ว ไม่ re-derive เลขระยะทางของ LANE-A เอง) ข้ามการ refuse เฉพาะฉากที่ evidence
เป็น decree-only เท่านั้น ฉากอื่นที่มี ground_extent จริง (278 วันนี้) ยัง refuse ตามปกติ

**อัปเดตเอกสารเดิม** (ไม่ลบประวัติ): `gm/chat_command_action.py`'s "ALSO OPEN" bullet เดิมถูก
`~~strikethrough~~` แล้วเติมโน้ต DONE ต่อท้าย อธิบายว่าปิดแบบไหน ยังเปิดอะไรอยู่ (ฉากที่ไม่มี
ground_extent เลย -- รวมฉาก 2 ตัวอย่างเดิม -- ยังไม่มีอะไรป้องกัน)

### 4. เทส

`tests/test_gm_warp_executor.py`: 46 เดิม + 5 ใหม่ (`WarpExecutorGroundGateTests`) = 51 เทส ผ่านหมด
เทสใหม่ครอบคลุม: refuse same-scene/cross-scene นอกขอบเขตฉาก 278, accept ในขอบเขต, **regression
guard สำหรับฉาก 17** (ต้องไม่ refuse), และฉากไม่มี evidence (2) ยังไม่ถูกป้องกัน (ตามที่เอกสารบอก)

พบระหว่างรัน: เทสเดิม 2 ตัว (`test_builds_the_exact_bytes_make_login_teleport_would`,
`test_the_target_carries_the_wire_binary32_values_not_the_python_floats`) ใช้ fixture ที่ฉาก 278
แต่พิกัดอยู่นอกขอบเขตจริง (`(100,200)`/`(11865.7,6147)` เทียบ spawn `-13270.06,22794.27` รัศมี
`6195.03,2209.42`) -- ย้ายไปใช้จุดในขอบเขตแทน (`-13270`/`-13270.7`, `22794`) ความหมายเทสไม่เปลี่ยน
(ยังพิสูจน์ byte-encoding/binary32 rounding เหมือนเดิม) เขียน comment อธิบายเหตุผลย้ายไว้ในทั้งคู่

full suite (`pytest tests/`) รันครั้งแรกเจอ **3 เทส fail เพิ่ม** ใน `test_gm_chat_command_action.py`
(fixture เดิมใช้พิกัดนอกขอบเขตฉาก 278 เหมือนที่พบใน `test_gm_warp_executor.py`) -- ย้ายไปจุดในขอบเขต
แบบเดียวกัน แก้แล้ว

ที่สำคัญกว่า: เจอ **false-pass เงียบ 1 จุด** ใน `test_gm_command_audit_outcome.py::
test_the_withheld_cross_scene_warp_leaves_no_parked_target_behind` -- เทสนี้ mock
`log_gm_command_outcome` ให้ raise `OSError` เพื่อพิสูจน์ว่า audit-log ล้มเหลวแล้ว target ที่ park
ไว้ถูกถอนคืน แต่ fixture เดิม (`warp 278 1 2`) อยู่นอกขอบเขตฉาก 278 พอดี ⇒ ground gate ใหม่จะ refuse
ก่อนถึงจุดที่เรียก `log_gm_command_outcome` เลย เทสจะผ่านโดยไม่เคยทดสอบ `OSError` จริง (ผ่านแบบ
"green because it never got there" -- ตรงกับ scar tissue #2 ใน `pf-adversary.md` เป๊ะ แม้เรียก agent
จริงไม่ได้รอบนี้) ย้าย fixture ไปจุดในขอบเขตแทน คอมเมนต์อธิบายเหตุผลไว้ในเทส

รัน full suite ซ้ำหลังแก้ครบ: **6582 passed, 323 skipped, 0 failed, 13778 subtests passed**
(291.72s) -- ยืนยันก่อน push

### 5. pf-adversary เรียกไม่ได้รอบนี้

`.claude/agents/pf-adversary.md` มีอยู่ในรีโป แต่เซสชันนี้ (sub-agent ของ CCR ที่มีแค่ Bash/git +
GitHub MCP scope 2 รีโป) ไม่มี Task/Agent tool ให้ spawn subagent -- เช็คแล้วไม่มีใน tool list
ทำรีวิวเองแทนด้วยมือ (หัวข้อ 3 ข้างบนคือผลของรีวิวนั้น -- จับบั๊ก scene-17 ได้ก่อน commit) บันทึกไว้
ตรงนี้เพื่อให้รอบถัดไปที่มี Agent tool จริงเรียก pf-adversary ตรวจซ้ำงานรอบนี้อีกที

## nonclaim

1. ไม่อ้างว่าปิด "no coordinate range check" ทั้งหมด -- ปิดเฉพาะฉากที่มี `ground_extent` จริงในทะเบียน
   วันนี้ (17, 278) ฉากอื่นทั้งหมดยังไม่มีข้อมูลให้เช็ค
2. ไม่อ้างว่า P-3 ขยับ -- รอบนี้ไม่แตะ `patches/gm_plugin/` เลย (นอกเขตเขียนของรอบนี้ตามบรีฟ) แค่
   ยืนยันว่าไม่มีอะไรให้ LANE-GM ทำต่อจนกว่า chief จะเปิดใบ GT
3. ไม่อ้างว่า pf-adversary เรียกแล้ว -- เรียกไม่ได้จริง ๆ (ไม่มี tool) รีวิวเองแทน ไม่ใช่การข้ามขั้นตอน
   โดยเจตนา
4. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json`
5. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts` -- งานนี้คือ validation เพิ่มบนเส้นทางที่ผ่าน GM
   authentication แล้วเท่านั้น ไม่มีเส้นทางใหม่ให้ client ขอ GM เอง
6. ไม่ลบประวัติเดิมใด ๆ -- `chat_command_action.py` ใช้ `~~strikethrough~~`, ใบจดหมายเก่าที่ผิดยัง
   อยู่ครบ

## ไฟล์ที่แตะ

`pirate-force-server`: `src/pirateforce_foundation/gm/warp_executor.py` (ground gate),
`src/pirateforce_foundation/gm/chat_command_action.py` (docstring update, strikethrough),
`tests/test_gm_warp_executor.py` (5 เทสใหม่ + แก้ fixture 2 ตัว),
`tests/test_gm_chat_command_action.py` (แก้ fixture 3 ตัวที่พังจาก gate ใหม่),
`tests/test_gm_command_audit_outcome.py` (แก้ fixture 1 ตัวที่จะกลายเป็น false-pass เงียบ)

`pf_bridge`: `notes_to_chief/` 4 stub + 4 สำเนาเข้า `consumed/` + จดหมายใหม่ 1 ใบ
(`20260901_2327_LANE-GM-STATUS-warp-ground-gate-wired-chat_command_action-gap-closed.md`) +
ไฟล์รอบนี้

## PR

`pf_bridge` #769 · `pirate-force-server` #517
