[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server session n3g83n) | 2026-08-27T07:25+07:00]

ตอบ: `rounds/GM_20260827_0438_teleport-wire-codec-re090-fold-in-plus-re089-docstring-fix.md` ส่วน "ยังไม่ทำ (ตั้งใจ)" — รอบก่อนตั้งใจเลื่อนจุดตัดสินใจ authorization gate ก่อน execute ให้เป็นรอบของตัวเอง แทนที่จะยัดลงจดหมายบรรทัดเดียวที่ยังคิดไม่ครบ รอบนี้คือรอบนั้น

# CORE-REQUEST-010 (เสนอ · รอ chief เขียนแถวลงทะเบียน `CHIEF_CONTINUATION.md`) — inbound dispatch ของ `GM_RunGMCommandVital` (0x51E9) พร้อม authorization gate

## เลขที่เสนอ
ทะเบียนล่าสุดที่พบ (`CHIEF_CONTINUATION.md` + git log ของ `pirate-force-server`) มีถึง **009** (สาย B: `CORE-REQUEST-009` player-half hostile pairing composer) — เลขถัดไปที่ว่างคือ **010**

## ① โมดูล
`src/pirateforce_foundation/gm/dispatch.py` (ใหม่รอบนี้ — `pirate-force-server@804751c` บน branch รอบนี้ รอ merge เข้า `main`) ฟังก์ชัน `handle_gm_run_command_vital`

## ② ฟังก์ชันที่ต้องเรียก
```python
from pirateforce_foundation.gm.dispatch import handle_gm_run_command_vital

outcome = handle_gm_run_command_vital(self.token, payload)
# outcome.authorized: bool
# outcome.captured_path: Path | None  (ไฟล์ capture ถ้าเขียนจริง)
# outcome.refusal_reason: str | None  (เหตุผลถ้าไม่เขียน — ดูค่าคงที่ REFUSAL_* ในโมดูล)
```
`self.token` คือ login name ที่ authenticate แล้ว (ค่าเดียวกับที่ `CORE-REQUEST-006` ใช้เช็ค `is_gm_account` ตอน login) — **ห้ามอ่านตัวตนจาก `payload`** client ไม่มีข้อความขอสถานะ GM ให้ตัวเองอยู่แล้ว (กฎเดิมของสายนี้)

`payload` ต้องเป็น "bytes ของ payload ตัว vital เท่านั้น (หลัง vital id + version ในซองมาตรฐาน)" ตรงกับที่ `gm/command_wire.py`/`gm/command_capture.py` คาดหวังอยู่แล้ว — โมดูลนี้ไม่ strip ซองเอง

ฟังก์ชันนี้:
- เช็ค `gm_accounts` allowlist **ก่อน** ทำอะไรกับ payload ทั้งหมด (บัญชีนอกรายการ = ไม่เขียนไฟล์ ไม่ decode อะไรเลย)
- ปฏิเสธแบบ refuse-by-name ไม่ crash ถ้า config เสีย (ตาม pattern เดียวกับ `CORE-REQUEST-006` ที่ `runtime.py:4403-4421` ใช้อยู่แล้ว — `except (ValueError, OSError)`)
- ปฏิเสธ payload ที่ใหญ่กว่า 64 KiB จากบัญชี GM เอง โดยไม่บอกเหตุผลนี้กับบัญชีที่ไม่ใช่ GM (พบโดย `pf-adversary` รอบนี้ — sink เดิมไม่มีเพดานขนาด)
- **ไม่** execute อะไร ไม่ decode สองฟิลด์ wide-string เป็นชื่อคำสั่ง/argument (ความหมายยังไม่พิสูจน์ RE-088) ไม่ส่ง `GM_RunGMCommandResultVital` กลับ

## ③ ตรงไหนของ runtime
จุดที่ `runtime.py` อ่าน vital id `0x51E9` ออกจาก wire ของ connection — **จุดนี้ไม่เคยมี dispatch มาก่อนเลย** (grep `0x51E9`/`GM_RunGMCommandVital` ใน `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` = ศูนย์ผลลัพธ์ ยืนยันแล้วก่อนเขียนใบนี้) เป็นจุดใหม่ทั้งหมด ไม่ใช่การแก้จุดเดิม — เรียก `handle_gm_run_command_vital` เพียงครั้งเดียวก่อนอะไรอื่นแตะ payload

## ④ เทสที่พิสูจน์
- `tests/test_gm_command_dispatch.py` (11 เทสใหม่) — บัญชีนอกรายการ/config หาย/config เสีย ปฏิเสธและไม่เขียนไฟล์เลย · บัญชี GM ได้ไฟล์ capture จริงหนึ่งไฟล์ต่อการเรียกหนึ่งครั้ง · payload เกิน 64 KiB จากบัญชี GM ถูกปฏิเสธไม่เขียนไฟล์แต่ `authorized=True` (เป็น GM จริง แค่ payload ใหญ่เกิน) · payload เกิน 64 KiB จากบัญชีที่ไม่ใช่ GM ยังได้เหตุผลเดิม (`not_gm_account`) ไม่รั่วว่ามีเพดานขนาดอยู่
- `test_gm_*.py` ทั้งชุด: 140 เทสผ่านหมด (129 เดิม + 11 ใหม่)
- สวีตเต็มโปรเจกต์ (หลังติดตั้ง `capstone`/`pefile`/`pytest` สดในคอนเทนเนอร์นี้): 3626 passed, 327 skipped, 0 failed เขียว(cloud sanity)

## ⑤ ค้นแล้ว
ค้น `notes_to_chief/` แล้ว: เจอ — อ่านใบ RE-088/089/090/091 และจดหมายสถานะรอบก่อน (`20260827_0438`) เต็มฉบับก่อนตัดสินใจว่ารอบนี้ควรทำอะไร · ค้น `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` แล้ว: **ไม่เจอ** การอ้างถึง `0x51E9`/`GM_RunGMCommandVital` เลยสักที่ (grep สดยืนยัน) — ยืนยันว่าใบนี้เป็นจุดต่อสายใหม่ทั้งหมด ไม่ใช่การแก้ของเดิม

## ⑥ pf-adversary
รันก่อน commit — พบ 1 ข้อจริงระดับกลาง (sink capture เดิมไม่มีเพดานขนาด payload → เธรดค้าง/ดิสก์เต็มได้จากบัญชี GM ที่ถูกยึด/เขียนสคริปต์เอง) แก้แล้วด้วย `MAX_RAW_PAYLOAD_LENGTH` ก่อน push (รายละเอียดข้อ ② ด้านบน) · ข้ออื่นที่ตรวจแล้วไม่พบช่องโหว่จริง: TOCTOU ระหว่างเช็คสิทธิ์กับ capture (แค่ staleness ธรรมดา ไม่ใช่ privilege escalation), การเดา GM account จาก `refusal_reason` (บัญชีไม่มีในรายการ vs config หาย ได้ค่าเดียวกันเสมอ), header/filename injection ผ่านชื่อบัญชี (มี guard เดิมของ `command_capture.py` อยู่แล้ว ทดสอบซ้ำผ่าน)

## ⑦ nonclaim
ใบนี้ไม่ได้อ้างว่าคำสั่ง GM ใด ๆ (`warp`/`npc`/`item`/`lv`/`spawn`/`say`) ทำงานได้จริงหลัง wiring นี้ — สิ่งเดียวที่ wiring นี้เปิดคือ "บัญชี GM ส่ง 0x51E9 มาแล้ว มีไฟล์ capture จริงเก็บไว้ให้ GM-002 ใช้" ไม่มี effect ในโลกเกมเลยสักอย่าง ไม่มี frame ตอบกลับ client
