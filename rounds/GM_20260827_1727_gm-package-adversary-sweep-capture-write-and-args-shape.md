# รอบ 50x5xt -- LANE-GM: ตรวจ `gm/` ทั้งแพ็กเกจแบบ pf-adversary เต็มรูปแบบ ปิดช่องจริง 2 ข้อ (2026-08-27 17:2x +07:00)

## บริบท

รอบก่อน (`kcm8ir`) ปิด `RE-104`/`RE-105` และยืนยันงานรอบนั้น merge จริงบน `main` ทั้งสอง repo
(`pf_bridge#212`, `pirate-force-server#129`) กล่องจดหมายต้นรอบนี้ไม่มีใบใหม่ที่ต้องบริโภค (`RE-088` ถึง
`RE-105` ทุกใบปิดแล้วตาม `docs/GM_LANE.md`) และ `CORE-REQUEST-011`/`012`/`015` ยังรอ chief ต่อสาย -- ไม่มี
งาน wire ใหม่ให้ทำในเขตของตัวเองจากมุมนี้

แทนที่จะปล่อยรอบว่าง (กฎ ADDENDUM ข้อ F) เลือกหยิบ "technical debt ที่ pf-adversary เคยชี้" -- แต่ยังไม่เคยมี
รอบไหนรัน `pf-adversary` กับ**ทั้งแพ็กเกจ** `gm/` พร้อมกัน (มีแต่รอบที่ตรวจทีละไฟล์ตามงานที่เพิ่งแก้) ตอนนี้
`gm/dispatch.py` เป็นจุดที่ไบต์จริงจากไคลเอนต์ไหลเข้ามาแล้ว (`CORE-REQUEST-010` merge แล้ว, always-on) จึง
สมควรกวาดทั้งแพ็กเกจสักครั้ง

## ต้นรอบ: ตรวจล็อกตาม ADDENDUM v2

ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo ตอนต้นรอบ -- เปิด draft PR ยึดล็อก (`pf_bridge#218`,
`pirate-force-server#134`)

ตรวจ PR ปิดล่าสุดของสายนี้ทั้งสอง repo ด้วย `pull_request_read(method="get")` (ไม่ใช่ `list_pull_requests`
ตามบทเรียนรอบ `a54s3e`/ใบ `1936`/`1450`): `pf_bridge#212` และ `pirate-force-server#129` ทั้งคู่
`merged: true` -- งานรอบก่อนอยู่บน `main` แล้ว ไม่ต้องกู้อะไร

กล่องจดหมาย: grep `ADDRESSEE: LANE-GM` -- มีแค่ใบที่บริโภคแล้วก่อนหน้านี้ (`.CONSUMED.txt` ครบ) และ
สอง STATUS/ASK-COO ที่สายนี้เป็นคนเขียนเอง (ไม่ใช่ผลที่ต้องบริโภค) ไม่มีใบใหม่ที่ต้องทำอะไรต่อรอบนี้

## สิ่งที่ทำ (pirate-force-server, `pirate-force-server#134`)

รัน `pf-adversary` (subagent) กับทั้งแพ็กเกจ `src/pirateforce_foundation/gm/` (12 โมดูล) และเทสของมันทั้งหมด
เจตนาหาว่าบัญชีที่ไม่ใช่ GM หลุดได้ไหม, ช่องแบบ type-confusion เดิม (ที่เคยปิดใน `say_wire.py`/
`warp_executor.py`) ยังหลงเหลือที่อื่นในแพ็กเกจไหม, resource exhaustion, execution creep, และบั๊ก
wire-decode

**พบ 3 ข้อ:**

1. **HIGH -- `gm/dispatch.py`**: `handle_gm_run_command_vital` เรียก `capture_raw_gm_command` (ทำ
   `os.mkdir`/`os.open`/`os.write` จริง) โดยไม่มี `try`/`except` เลย ทั้งที่ docstring ของโมดูลเองอ้างว่าใช้
   pattern "refuse by name, not by crash" เดียวกับที่ `is_gm_account` lookup ใช้ -- แต่ pattern นั้นครอบแค่
   จุด lookup ไม่ครอบจุดเขียนดิสก์ เนื่องจาก `CORE-REQUEST-010` ต่อสายจุดนี้เข้า `runtime.py` แบบ always-on
   ไม่มี try/except ล้อมอีกชั้นที่นั่นด้วย `OSError` จากดิสก์เต็ม/สิทธิ์ไม่พอ/`capture_root` ชนกับไฟล์ที่มีอยู่แล้ว
   จะหลุดออกจาก handler แล้วอาจฆ่า connection-handling thread ทั้งเธรดสำหรับผู้เล่นทุกคน จากคำสั่ง GM
   ที่ authorized ถูกต้องเพียงคำสั่งเดียว
2. **MEDIUM -- `gm/commands.py`**: `describe_warp_target`/`describe_npc_target`/`log_gm_command` แตะ
   `command.args` โดยไม่มี shape guard เลย -- ช่องเดียวกับที่ `say_wire.py`/`warp_executor.py` เคยปิดไปแล้ว
   (blacklist -> allowlist -> exact-type ผ่านสามรอบ pf-adversary ของรอบ `a54s3e`) แต่ไม่เคยย้อนมาแก้ไฟล์นี้
   ที่เขียนก่อนหน้า `GmCommand` สร้างมือด้วย `args={0:"1",1:"2",2:"3"}` (dict คีย์ตัวเลข) ทำให้
   `log_gm_command` เขียน `"args": [0,1,2]` (คีย์ของ dict) แทนค่าจริงลงไฟล์ log แบบเงียบ ๆ ไม่โยน error เลย
   ส่วน `args=None` โยน `TypeError` เปล่า ๆ ไม่ใช่ error เฉพาะโมดูลที่ caller ดักได้
3. **MEDIUM (ยังไม่แก้รอบนี้)**: ไม่มี rate limit ต่อบัญชีสำหรับการ capture ที่ authorized แล้ว -- บัญชี GM
   ที่ถูกสคริปต์ยิง `0x51E9` รัว ๆ ยังเขียนดิสก์ได้ไม่จำกัด

**ไม่พบ**: ไม่มีทางที่บัญชีนอก `gm_accounts` จะได้ capability/capture/log ใด ๆ -- gate ปฏิเสธก่อนเสมอทั้งกรณี
"ไม่อยู่ในลิสต์" และ "config พัง" ก็ยังไม่พบบั๊ก wire-decode ใน `command_wire.py`/`teleport_wire.py`/
`state_wire.py`

**แก้จริง (ข้อ 1, 2):**
- `dispatch.py`: ครอบ `capture_raw_gm_command(...)` ด้วย `try`/`except OSError` คืน
  `GmDispatchOutcome(authorized=True, captured_path=None,
  refusal_reason=f"capture_write_failed_{type(error).__name__}")` -- รูปแบบเดียวกับ
  `gm_account_lookup_failed_*`/`payload_too_large` ที่มีอยู่แล้ว caller เดิมจับ pattern นี้ได้โดยไม่ต้องเพิ่ม
  branch ใหม่
- `commands.py`: เพิ่ม `_require_args_tuple(args, min_length=N)` ใช้ `type(args) is not tuple`
  (exact-type เหมือนที่ `warp_executor.py` ใช้ ไม่ใช่ `isinstance` ที่เคยถูก tuple subclass โกหกผ่านมาแล้ว)
  บวกเช็คความยาว โยน error ใหม่ `GmCommandArgsError` เรียกที่ต้นทั้งสามฟังก์ชัน

**ข้อ 3 (deferred โดยตั้งใจ)**: บันทึกไว้ใน `docs/GM_LANE.md` หัวข้อ "What is intentionally NOT built yet"
พร้อมเหตุผล -- rate limiter ต้องมี shared state ข้าม call ซึ่งมีคำถามเรื่อง thread-safety/test-isolation
จริงจัง (module-level dict ที่ไม่มี reset hook จะรั่วข้ามเทสไฟล์อื่นในโปรเซสเดียวกัน) สมควรมีรอบของตัวเอง
ไม่ใช่ปะต่อท้ายรอบที่มี 2 เรื่องอื่นอยู่แล้ว ไม่มี `CORE-REQUEST` เกี่ยวข้อง (อยู่ในเขตเขียนของสายนี้ล้วน)

**pf-adversary ตรวจซ้ำ (ผ่านที่ 2, subagent แยก)** ยืนยันทั้งสองข้อที่แก้ปิดจริง: ไล่ทุกจุดที่โยน exception
ได้จาก `capture_raw_gm_command` (mkdir/open/write/close, การ retry ชน filename ภายในฟังก์ชันเองไม่หลุดออกมา)
ยืนยันเป็น `OSError` ทั้งหมด และ `commands.py` ไม่มีจุดอื่นที่แตะ `command.args` โดยไม่ผ่าน guard ใหม่แล้ว
รันเทส `tests/test_gm_*.py` เอง (215/215) ยืนยันตรงกัน

**พบเพิ่มระหว่างตรวจซ้ำ (ไม่ใช่ 1 ใน 3 ข้อเดิม, severity ต่ำ)**: loop retry ชน filename ใน
`command_capture.py` ไม่มีเพดานจำนวนรอบ -- ไม่ใช่ช่องโยน exception หลุด (อยู่ในขอบเขต `OSError` ที่ดักแล้ว)
แต่เป็นความเสี่ยง spin ถ้า capture root มีไฟล์ชนกันจำนวนมากสำหรับบัญชี+วินาทีเดียวกัน บันทึกไว้คู่กับข้อ 3
ใน `docs/GM_LANE.md` เพราะ rate limiter ในอนาคตจะช่วยจำกัดจุดนี้ไปด้วย

## เทส

`tests/test_gm_commands.py`: 22/22 (16 เดิม + 6 ใหม่ ArgsShapeGuardTests) · `tests/test_gm_command_dispatch.py`:
13/13 (11 เดิม + 2 ใหม่) · `test_gm_*.py` ทั้งชุด: 215/215 (189 เดิม + 26 ใหม่) · repo-wide
`unittest discover`: 3587 tests, error เฉพาะ 18 รายการเดิม (`ModuleNotFoundError: capstone`, ไม่เกี่ยวข้อง
ไม่ใช่ของใหม่)

## ค้นแล้ว: ไม่เจอ (ไม่เกี่ยวข้องรอบนี้)

รอบนี้ไม่พึ่งข้อมูลจาก client เลย -- แก้ความทนทานของโค้ดบนโครง wire ที่พิสูจน์แล้วทั้งหมด กฎ "ค้นก่อนถอด"
ไม่มีผลกับรอบนี้

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มีจุดเรียกจริงจากไคลเอนต์ที่เปลี่ยน -- แต่ถ้าบัญชี GM ยิง `0x51E9` ตอนดิสก์เต็มหรือ `capture_root` มีปัญหา
จริง (เช่นระหว่าง GT-103 attended capture matrix ที่คิวไว้แล้ว) เมื่อวานเซิร์ฟเวอร์จะเสี่ยงเธรดล่มทั้งเธรด
สำหรับผู้เล่นทุกคน วันนี้จะได้แค่ capture ไม่สำเร็จของคำสั่งนั้นคำสั่งเดียว ผู้เล่นอื่นไม่ได้รับผลกระทบ --
เป็นความทนทาน ไม่ใช่ฟีเจอร์ใหม่ที่ผู้เทสจะ "เห็น"

nonclaim: ไม่มีการอ้างว่าคำสั่ง `warp`/`say`/`npc`/`item`/`lv`/`spawn` ทำงานจริงหรือถูกส่งออกไปจริง -- ยังไม่มี
จุดส่งข้อมูลไปยัง socket ในรอบนี้ ไม่มีการเปลี่ยนพฤติกรรมบน happy path (`args` ที่เป็น tuple ถูกชนิด/ความยาว
ให้ผลเหมือนเดิมทุกไบต์) ไม่มีการแก้ `runtime.py`
