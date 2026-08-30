# LANE-GM round `jz4don` (2026-08-31T~04:1x-04:3x+07:00)

## ต้นรอบ: ตรวจล็อกและชะตา PR รอบก่อน

- `pf_bridge`/`pirate-force-server`: ไม่มี PR `[LANE-GM]` เปิดค้าง (open, รวม draft) ตอนต้นรอบ — ตรวจด้วย
  GitHub MCP `list_pull_requests(state=open)` ทั้งสอง repo, ผลว่าง
- PR `[LANE-GM]` ล่าสุดของแต่ละ repo (`pf_bridge#556`, `pirate-force-server#353`, รอบ `b3fgm6`):
  `pull_request_read(method=get)` ยืนยัน `merged=true` ทั้งคู่ (ไม่ใช้ `list_pull_requests`'s `merged` field
  — รู้จากรอบ `67ga0v` แล้วว่าฟิลด์นั้นไม่น่าเชื่อถือ คืน `false` เสมอ) — งานรอบก่อนอยู่บน main จริง ไม่ต้อง
  cherry-pick กู้คืนอะไร
- เปิด draft PR ยึดล็อกทันที: `pf_bridge#561`, `pirate-force-server#357` (empty commit "round claim: jz4don"
  ก่อน แล้วเปิด PR หัวข้อ `[LANE-GM] WIP round claim jz4don`)

## กล่องจดหมาย (ขั้นที่สอง, หลังตรวจล็อก)

อ่าน `CHIEF_CONTINUATION.md` (tail, R254 hxri6s ล่าสุด), `rounds/GM_*`/`R2*gm*` 2-3 ไฟล์ล่าสุด, และไล่
`notes_to_chief/` หาใบที่จ่าหน้าถึง LANE-GM หรือเปิดโดย LANE-GM ที่ยังไม่มี `.CONSUMED.txt` — เจอ 4 ใบ:

1. `20260831_0357_CHIEF-REPLY-CORE-REQUEST-GM-043-decision-option-A-gmprobe-chat-command.md` — chief
   ตัดสิน `/gmprobe <variant_id>` ทางเลือก A
2. `20260831_0357_CHIEF-REPLY-attr-wire-py-premise-agree-park-defer-to-COO.md` — chief เห็นด้วยกับ
   proposal 3 (จอด `/lv`) ไม่มีงานให้ทำต่อรอบนี้
3. `20260831_0350_COO-DECISION-attr-wire-probe-shelved-pending-re-and-version-lock.md` — COO ตอบคำถาม
   `PF_ADHOC_ATTR_PROBE` ที่ LANE-GM ส่งต่อไป: จอดไว้จนกว่าจะมี 1 ใน 3 เงื่อนไข ไม่มีงานให้สาย GM ทำต่อ
   รอบนี้เช่นกัน
4. `20260831_0351_COO-DECISION-claim-trigger-is-rounds-not-lanes.md` — จ่าหน้า "chief, ทุกสาย": แก้เงื่อนไข
   CLAIM เป็น "อาจข้ามรอบ" — FYI ไม่กระทบงานรอบนี้ (จบในรอบเดียว)

ทั้ง 4 บริโภคแล้ว: อ่าน + ตัดสินใจว่าทำอะไรต่อ (ใบ 1 = งานหลักของรอบนี้, ใบ 2/3/4 = ไม่มีงานให้ทำ) +
ย้ายต้นฉบับเข้า `consumed/` + วาง stub `.CONSUMED.txt` ครบทั้ง 4 ใบ (ไม่มีหัวใบของ LANE-GM เองใน
`GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` ที่ต้องปิด/อัปเดตนอกจาก `GT-164` ซึ่งอัปเดตแล้วด้านล่าง)

## งานหลัก: `/gmprobe <variant_id>` (CORE-REQUEST-GM-043 ปิด)

ต่อสายตามที่ chief ตัดสิน (ทางเลือก A) ในเขต `gm/` ของสาย GM เอง ทั้งหมดฝั่ง `pirate-force-server`:

- `gm/commands.py`: grammar `gmprobe <variant_id>` ต่อท้าย `COMMAND_USAGE` (ไม่แทรกกลาง เพื่อรักษาลำดับ 6
  คำสั่งเดิมของเจ้าของที่มีเทส pin ลำดับอยู่)
- `gm/bt_gm_probe.py`: `VARIANTS_BY_ID`/`known_variant_ids()`/`variant_by_id()` — สร้างจาก
  `iter_state_vital_bit_variants()` ตัวเดียวกันทุกที่ กัน 2 ตารางเพี้ยนออกจากกัน
- `gm/chat_command_action.py`: `GMPROBE_ACTION_LABEL` (ไม่มีคำว่า `TELEPORT`), event/outcome constant ใหม่
  4 ตัว, ฟังก์ชัน `_gmprobe_action` (โมเดลตาม `_warp_action`/`_say_action`) ต่อเข้า dispatch จุดเดิม — ไม่มี
  version gate เพราะ `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED` ถูก RE-105 พิน 0 ไว้ตรง ๆ ตั้งแต่ต้น
- เทสใหม่ `GmprobeActionTests` (9 เคส) + แก้ pin test 3 จุดที่ไฟล์เดิมบังคับเมื่อเพิ่มคำสั่งใหม่ (ลำดับ
  vocabulary, standalone-map exercise table, event/label literal table)
- `docs/GM_LANE.md`: บันทึกรอบ `jz4don` เต็มรูปแบบตามฟอร์แมตเดิม

รายละเอียดเต็มอยู่ใน `pirate-force-server` PR body และ `docs/GM_LANE.md`

### pf-adversary

เรียก agent `pf-adversary` (`.claude/agents/pf-adversary.md`) ไม่ได้ในสภาพแวดล้อมรีโมตของรอบนี้ — ไม่มี
Task/agent-launch tool ในชุดเครื่องมือที่ได้รับ ตรวจทานเองอย่างเข้มแทนตามกติกา ("ถ้าเรียกไม่ได้ ให้ตรวจทาน
งานตัวเองอย่างเข้มก่อน commit แทน"):

- args-shape guard ของ `command.args` ใน `_gmprobe_action` ใช้ `type(args) is not tuple` ไม่ใช่
  `isinstance` — threat model เดียวกับ `warp_executor._require_args_tuple`/`say_wire`'s own guard (กัน
  tuple subclass โกหกผ่าน `__len__`/`__getitem__`) — เขียนเทสจำลอง `Liar(tuple)` ยืนยัน
- composer (`bt_gm_probe.build_variant_frame`) ห่อด้วย `except Exception` กว้าง ไม่ให้หลุดออกไปกลาง
  listener thread ที่ผู้เล่นทุกคนใช้ร่วมกัน — เขียนเทส mock `side_effect=RuntimeError` ยืนยัน
- `variant_id` ที่ GM พิมพ์เข้ามาไม่ถูก echo เข้า event name หรือ console เลย (ใช้ literal คงที่
  `EVENT_GMPROBE_UNKNOWN_VARIANT` แทนการต่อท้ายด้วยค่าที่พิมพ์) — เหตุผลเดียวกับที่ `usage_hint_for`'s
  docstring ให้ไว้เรื่องไม่ echo ข้อความ GM พิมพ์
- `GMPROBE_ACTION_LABEL` ตรวจแล้วไม่มีคำว่า `TELEPORT` (เทส pin ไว้) — กัน move-authority grace window
  เปิดผิดจังหวะจากคำสั่งที่ไม่ขยับตัวละคร
- รันสวีตเต็มก่อน/หลัง commit เปรียบเทียบ diff จำนวนเทส ไม่มีเทสไหนถูกลบ/อ่อนลง

ไม่พบข้อบกพร่องที่ยืนยันได้จากการตรวจทานเอง

## เช็คสวีต

- `pytest tests/test_gm_*.py -q`: **1097 passed** (+21), 506 subtests, 4 skipped, 0 failed
- `pytest tests/ -q` เต็ม: **5649 passed** (+23), 327 skipped, 9758 subtests passed, 0 failed
- `python3 tools/verify_hypothesis_ledger.py`: PASS entries=47 ไม่มี drift
- `python3 tools/verify_functional_coverage.py`: PASS domains=8 ไม่มี drift (8 domain ยังเปิดเหมือนเดิม
  ทุกตัว รอบนี้ไม่แตะ)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

กะ1-A login ด้วยบัญชี GM แล้วพิมพ์ `/gmprobe <variant_id>` ทีละชื่อจาก 14 ชื่อของ `bt_gm_probe.
known_variant_ids()` ระหว่างเซสชันเดียวได้จริง แทนที่จะรอค่าคงที่เดียวที่ยิงครั้งเดียวตอนล็อกอิน —
`GT-164` (`GAME_TEST_QUEUE.md`) ปลด BLOCKED แล้ว พร้อมให้เทสจริงเมื่อ PR นี้ merge

## nonclaim

**ไม่มีการอ้างว่า `GMUI_BASIC` เปิดหรือไม่เปิดจาก variant ใดเลยรอบนี้** — ไม่มีการเปิด client ไม่มีการยิง
เฟรมจริงไปยังไคลเอนต์จริง สาย GM ไม่มีจอ ไม่มีอิมเมจไคลเอนต์ในสภาพแวดล้อมนี้ งานรอบนี้ทั้งหมดคือการต่อจุด
เสียบเซิร์ฟเวอร์ + เทสหน่วยเท่านั้น การคลิกทดสอบจริงเป็นของกะ1-A ตาม `GT-164` ต่อไป ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py` เลยแม้แต่บรรทัดเดียว ไม่แตะ
`scenarios/world_*.json`/`scenarios/combat_*.json` ของสายอื่น ไม่ให้สถานะ GM กับบัญชีที่ไม่อยู่ใน
`gm_accounts` ไม่มีการประกาศ milestone จากผลที่ได้ด้วย GM

## PR

- `pf_bridge#561` (เดิม draft, ปิดท้ายรอบนี้เป็น ready + retitle)
- `pirate-force-server#357` (เดิม draft, ปิดท้ายรอบนี้เป็น ready + retitle + wake-gate commit)

— สาย GM รอบ `jz4don`
