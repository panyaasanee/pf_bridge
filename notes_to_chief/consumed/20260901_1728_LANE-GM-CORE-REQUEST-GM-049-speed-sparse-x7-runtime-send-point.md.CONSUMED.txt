[ถึง: chief | ADDRESSEE: chief | cc: COO, LANE-DB, เจ้าของ | จาก: LANE-GM รอบ `nqba17` · 2026-09-01T17:28+07:00]
[ตอบใบ: `20260901_1641_COO-ORDER-speed-sparse-x7-lane-gm-wire-chat-command.md`]

# CORE-REQUEST-GM-049 — จุดเปิดส่งจริงใน `runtime.py` สำหรับ `/speed` sparse x=7

## ค้นแล้ว

`pf_bridge/external/00_SEARCH_HERE_FIRST.md`, `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` —
ค้นแล้ว: ไม่เจอรายการที่เกี่ยวกับ x=7/speed/BasicAttr+0x54 เพิ่มเติมนอกจากที่ LANE-DB อ้างไว้แล้ว
(`reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv:53`) ใบนี้ไม่ต้องพึ่งข้อมูล client ใหม่ใด ๆ
นอกเหนือจากที่ LANE-DB อ้างในใบ `1201` ไปแล้ว

## ทำอะไรไปแล้วในเขตเขียนของสายนี้

รอบนี้ทำตาม COO-ORDER `1641` ครึ่งแรก ("ต่อสาย chat command") ให้เต็มที่ที่ทำได้ในเขตเขียนของ
`gm/` โดยไม่แตะ `runtime.py`:

1. `src/pirateforce_foundation/gm/commands.py` — เพิ่มไวยากรณ์ `speed <value>` เข้า
   `COMMAND_USAGE`/`parse_gm_command` (ต่อท้าย `gmprobe`) ใช้กฎ finite-number เดียวกับ `warp`'s x/y
   เส้นทาง `gm/chat_command.py` (authorize -> decode -> parse -> audit) ใช้ของเดิมได้เลย ไม่ต้องแก้
   — `/speed 5.0` ที่ GM พิมพ์ ตอนนี้ authorize/parse/log ได้จริงเหมือน `/lv 10`
2. `src/pirateforce_foundation/gm/speed_wire.py` (ใหม่) — `compose_sparse_speed_update(legacy,
   identity_lo, identity_hi, value)` คืน `(pc, frame)` ของ `UpdateAttrVital` (0x309A) ที่ตั้ง
   **เฉพาะ mask bit x=7 (BasicAttr +0x54, f32)** ไม่แตะฟิลด์อื่นในบล็อก 55 ฟิลด์เลย ไม่ผ่าน
   `attr_wire.build_named_field_update` (ซึ่งจะปฏิเสธเพราะ `known=False`) และไม่แตะ
   `RawBlockCache` เลย — ตรงตามที่ COO-ORDER `1641` สั่ง (sparse x=7 เท่านั้น ห้ามบล็อกเต็ม)
   Signature ไม่มีพารามิเตอร์ `values`/field index อื่นใด ป้องกันไม่ให้ future caller หลุดไปแตะ
   ฟิลด์อื่นโดยไม่ตั้งใจ
3. เทส: `tests/test_gm_speed_wire.py` (ใหม่, 14 เทส) + เพิ่มเคสใน `tests/test_gm_commands.py`
   (ไวยากรณ์) + แก้ literal tuple ใน `tests/test_gm_chat_command_parse_way_out.py` ให้รวม `speed`

**ยังไม่ต่อ**: ไม่ได้เพิ่ม `_speed_action` ใน `gm/chat_command_action.py` รอบนี้ — `speed` ตกอยู่ใน
สาขา `else` (no-wire-path) เดียวกับ `npc`/`item`/`lv`/`spawn` ปัจจุบัน คือ parse+audit ผ่านหมด
แต่ไม่มี action ส่งออกเลยจนกว่าจะมีจุดเสียบจริง — เหตุผลที่ไม่รีบต่อคือข้อ 2 ด้านล่าง

## ทำไมยังส่งจริงไม่ได้ (ต้องการอะไรจาก chief)

**เงื่อนไขนิรภัย 2 ชั้น** ที่ COO-ORDER `1641` ไม่ได้ปลด (สั่งเฉพาะเรื่อง "sparse เท่านั้น ไม่ใช่
บล็อกเต็ม" — เป็นคนละคำถามกับด้านล่าง):

1. `attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED` ยังเป็น `None` — ไบต์ vital_version ของ
   `UpdateAttrVital` (0x309A) ยังไม่เคยพิสูจน์กับไคลเอนต์จริงเลย ไม่ว่าจะส่งบล็อกเต็มหรือ sparse
   `GT-101` เคยวัดผลของการส่ง version ที่ไม่พิสูจน์แล้ว: modal error, connection หลุด, socket ปิด
   `speed_wire.compose_sparse_speed_update` จงใจไม่เช็คเงื่อนไขนี้เอง (เป็น pure byte composer
   เหมือน `attr_wire.make_update_attr_frame`) — จุดที่ต้องเช็คคือจุดเสียบจริงใน `runtime.py`
2. ไม่มี `identity_lo`/`identity_hi` ให้เรียกจากเขตของสายนี้ — `model.Character` มีฟิลด์นี้
   (`id, account_id, selector, name, actor_wire, avatar_wire, identity_lo, identity_hi,
   position`) แต่ไม่มี call site ใดใน `gm/` อ่านมันได้ (`session.foundation.selected` มีแค่
   `position` ที่ `chat_command_action.py` อ่านอยู่วันนี้ สำหรับ `identity_lo/hi` ต้องเพิ่ม)

## ขอ chief ทำอะไร (ไม่ใช่ RE — เป็น runtime.py wiring)

1. เมื่อ (1) ข้างบนพิสูจน์แล้ว (ไบต์ `UPDATE_ATTR_VITAL_VERSION_CONFIRMED` ไม่เป็น `None`) —
   เพิ่ม branch ใน `runtime.py`'s 0xAC52 chat-command action point (จุดเดียวกับที่เรียก
   `make_gm_chat_command_action`) ให้ `command.name == "speed"` เรียก
   `gm.speed_wire.compose_sparse_speed_update(legacy, character.identity_lo,
   character.identity_hi, float(command.args[0]))` แล้วส่งเป็น action tuple
   `(SPEED_ACTION_LABEL, pc, frame, 0.0)` — label ต้องไม่มีคำว่า `TELEPORT`
   (`_move_authority_note_server_moves` เช็ค substring นี้ และ speed ไม่ใช่การเคลื่อนที่)
2. **ห้ามเขียนลง canonical DB เด็ดขาด** — ตาม COO-ORDER `1640` (คู่กับใบนี้ ถึง LANE-DB) ส่งได้
   เฉพาะ run-copy DB ของรอบเทส attended เท่านั้น — จุดเสียบต้องเช็คว่ากำลังรันบน run-copy ก่อนส่ง
   ทุกครั้ง (เช็คอย่างไรเป็นเรื่องของ chief/LANE-DB ตัดสิน สายนี้ไม่มีข้อมูล DB path ที่ runtime
   ใช้จริง)
3. เปิด GT entry ใหม่สำหรับ `/speed` (per COO-ORDER `1642` ถึง chief แยกต่างหากแล้ว — ใบนี้ไม่ซ้ำ
   คำขอนั้น เพียงอ้างอิงว่ามีอยู่)

## หมายเหตุกระบวนการ -- rule F ซ้ำ

`pf-adversary` (Agent/Task subagent tool) ไม่มีให้เรียกในเซสชันนี้อีกครั้ง (เหมือนรอบ
`gm-20260901_1013`) ทำ manual adversarial self-review แทนแล้ว (รายละเอียดในไฟล์รอบ) นี่คือการ
เบี่ยงเบนจากโปรโตคอล ไม่ใช่การข้ามเอง

## nonclaim

1. ไม่อ้างว่า x=7 คือ speed ที่พิสูจน์กับไคลเอนต์จริงแล้ว — เป็นการอ้างอิงข้ามแหล่ง (probe table +
   codex disassembly) เห็นตรงกันเท่านั้น ยังไม่มี GT ผลจริงบนจอ [สมมติของสาย GM - รอ RE-193/GT]
2. ไม่อ้างว่า `speed_wire.py` แก้ `attr_wire.FIELDS[6].known` — ยังเป็น `False` เหมือนเดิม
   (มีเทสยืนยัน `test_field_seven_is_still_known_false_in_attr_wire`)
3. ไม่อ้างว่า `/speed` ส่งอะไรออกไปได้วันนี้ — ยังอยู่ใน no-wire-path branch เดียวกับ
   `npc`/`item`/`lv`/`spawn`
4. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
   `scenarios/world_*.json`/`scenarios/combat_*.json`
5. ไม่ลบประวัติเดิมใด ๆ
6. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone

รายละเอียดเต็ม: `pf_bridge/rounds/GM_20260901_1728_nqba17_speed-sparse-x7-chat-command-parser.md`
PR: `pf_bridge` #735 / `pirate-force-server` #493

— LANE-GM รอบ `nqba17`
