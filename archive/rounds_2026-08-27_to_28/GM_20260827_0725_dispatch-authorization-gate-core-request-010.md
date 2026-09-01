# GM round 2026-08-27 ~06:5x-07:3x (+07:00) — 0x51E9 inbound dispatch + authorization gate (CORE-REQUEST-010)

ยึดล็อกด้วย draft PR ทั้งสอง repo ก่อนเริ่ม (`pf_bridge#168`, `pirate-force-server#94`) — ตรวจ GitHub API ก่อนยึดล็อก: ไม่มี PR หัวข้อขึ้นต้น `[LANE-GM]` เปิดค้างในทั้งสอง repo (pf_bridge มีแค่ `[LANE-E]` #167, pirate-force-server มี `[LANE-E]` #93 และ `[LANE-A]` #91 — ไม่ใช่ล็อกของสายนี้ ไม่แตะ)

## ตรวจสถานะก่อนเริ่มงานจริง

ยืนยัน `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (ขั้นแรกบังคับของทุกรอบ) · อ่านจดหมาย order 1630 ซ้ำ · อ่านจดหมายสถานะรอบก่อน (`20260827_0438`) เต็มฉบับ: รอบนั้นตั้งใจเลื่อนงาน "authorization gate ก่อน execute" ให้เป็นรอบของตัวเอง เพราะ "ใหญ่กว่าจดหมาย CORE-REQUEST บรรทัดเดียว" — รอบนี้คือรอบนั้น

**ค้นแล้ว: เจอ** — อ่าน `docs/GM_LANE.md` เต็มไฟล์ก่อนเริ่ม ยืนยันโมดูลที่มีอยู่แล้ว (`accounts.py` `state_wire.py` `command_capture.py` `command_wire.py` `commands.py` `teleport_wire.py` `scene_catalog.py` `npc_switch_catalog.py`) และช่องว่างที่เอกสารระบุไว้เอง (ไม่มี inbound dispatch ของ 0x51E9 เลย ไม่มี authorization gate) · grep `0x51E9`/`GM_RunGMCommandVital` ใน `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` แล้ว: **ไม่เจอ** ยืนยันว่าไม่มีจุดต่อสายเดิมให้ชนกัน

## สร้าง (`pirate-force-server`, เขตเขียนของสายนี้ทั้งหมด)

- **ใหม่** `gm/dispatch.py` — `handle_gm_run_command_vital(account_name, raw_payload)` จุดต่อสายเดียวที่ `CORE-REQUEST-010` ขอให้ chief เรียกที่จุดอ่าน 0x51E9 ออกจาก wire ใน `runtime.py` เช็ค `gm_accounts` allowlist **ก่อน** ทำอะไรกับ payload ทั้งหมด (ปฏิเสธแบบ refuse-by-name ไม่ crash ถ้า config เสีย ใช้ pattern เดียวกับ `CORE-REQUEST-006` ที่ `runtime.py:4403-4421` มีอยู่แล้ว) เฉพาะบัญชี GM เท่านั้นที่ไปถึง `command_capture.capture_raw_gm_command` (sink เดิมของ GM-002) — บัญชีนอกรายการไม่เขียนอะไรลงดิสก์เลย ไม่ decode สองฟิลด์ wide-string เป็นคำสั่ง (ความหมายยังไม่พิสูจน์) ไม่ execute ไม่ส่ง `GM_RunGMCommandResultVital` กลับ
- **ใหม่** `tests/test_gm_command_dispatch.py` (11 เทส หลังแก้ตาม adversary)
- **แก้** `docs/GM_LANE.md` — เพิ่มหัวข้อ "Modules delivered (dispatch/authorization-gate round)" + แก้บรรทัด "no command execution path" ให้ตรงสถานะใหม่

## `pf-adversary` (บังคับก่อน commit)

รอบเดียว พบ 1 ข้อจริงระดับกลาง + ยืนยันไม่พบช่องโหว่จริงอีก 4 เรื่องที่ลองเจาะ:

1. **MEDIUM** — `command_capture.py`'s `_hex_dump` ไม่มีเพดานขนาด payload เลย (pure-Python loop) และ `dispatch.py` รอบนี้คือจุดแรกที่ทำให้ sink นี้เอื้อมถึงได้จาก wire จริง — agent ทดสอบจริงด้วย payload 50MB จากบัญชี GM: ใช้เวลา 21.67 วินาที สร้างไฟล์ 249MB บล็อกเธรดจัดการได้จริง ไม่ใช่แค่ทฤษฎี แก้ด้วย `MAX_RAW_PAYLOAD_LENGTH = 65536` (64 KiB ใหญ่กว่า shape จริงที่ RE-088 พิสูจน์ไว้มาก) ปฏิเสธ payload เกินเพดานจากบัญชี GM โดยไม่เขียนไฟล์ (`authorized=True` เพราะเป็น GM จริง แต่ `captured_path=None`) และไม่รั่วเรื่องเพดานนี้ให้บัญชีที่ไม่ใช่ GM รู้ (เช็คสิทธิ์ก่อนเช็คขนาดเสมอ) — เพิ่ม 3 เทสยืนยัน push ก่อนปิดรอบ
2. ตรวจแล้วไม่พบช่องโหว่จริง: TOCTOU ระหว่างเช็คสิทธิ์กับ capture (แค่ staleness ธรรมดา — บัญชีที่เพิ่งถูกถอดสิทธิ์อาจมีคำสั่งที่ค้างอยู่ระหว่างทางยังถูก capture ได้ ไม่ใช่ privilege escalation), การเดา GM account จาก `refusal_reason` (บัญชีไม่มีในรายการ vs config หาย ได้ค่าเดียวกันเสมอ ทดสอบตรงยืนยัน), header/filename injection ผ่านชื่อบัญชี (มี guard เดิมของ `command_capture.py` อยู่แล้ว ทดสอบซ้ำด้วยชื่อมี `\n` และภาษาไทยผ่าน), mutation test บน branch ปฏิเสธ (ลบ/สลับเงื่อนไขแล้วอย่างน้อย 3 เทสจับได้จริง)
3. หมายเหตุที่ตรวจไม่ครบ: รัน sandbox เป็น root ทำให้ `chmod 000` ไม่ trigger `PermissionError` จริง — ยืนยันแค่กิ่ง `ValueError`/`JSONDecodeError` ของ `except (ValueError, OSError)` ไม่ใช่กิ่ง `OSError` จริง ไม่ใช่บั๊กที่พิสูจน์แล้ว แค่ช่องว่างการทดสอบที่บันทึกไว้

## เทส

`test_gm_command_dispatch.py` 11 เทสใหม่ผ่านหมด · `test_gm_*.py` ทั้งชุด 140 เทสผ่านหมด (129 เดิม + 11 ใหม่) · สวีตเต็มโปรเจกต์ (ติดตั้ง `capstone`/`pefile`/`pytest` สดในคอนเทนเนอร์นี้ก่อนรัน — หายไปจาก python3 ของ session นี้เหมือนรอบก่อน ๆ): **3626 passed, 327 skipped, 0 failed** เขียว(cloud sanity)

## push

`pirate-force-server@804751c` บน `claude/youthful-johnson-n3g83n` (PR #94)

## จดหมาย

`notes_to_chief/20260827_0725_LANE-GM-CORE-REQUEST-010-gm-run-command-inbound-dispatch.md` — ขอเลข CORE-REQUEST-010 (เลขถัดจาก 009 ของสาย B ที่พบในทะเบียน)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ยังไม่มี — รอบนี้เป็นโค้ด/เอกสารฝั่งเซิร์ฟเวอร์ล้วน ไม่มี wiring เข้า `runtime.py` จริง (รอ chief ต่อสายตาม CORE-REQUEST-010) ไม่มีอะไรให้ client เห็นต่างไปจากเดิม

## nonclaim

ไม่มีการอ้างว่าคำสั่ง GM ใด ๆ ทำงานได้จริงหลังรอบนี้ — สิ่งเดียวที่สร้างคือจุดต่อสายที่ปลอดภัย (เช็คสิทธิ์ก่อนเสมอ มีเพดานขนาด) รอ chief เรียกจริง ไม่มี effect ในเกมเลยสักอย่างจนกว่าจะ wiring เสร็จ

## ค้าง (ตั้งใจ ไม่บล็อก)

- CORE-REQUEST-010 รอ chief ต่อสายจริง
- การ decode สองฟิลด์ wide-string ของ `GM_RunGMCommandVital` เป็นชื่อคำสั่ง/argument จริง ยังต้องรอ RE หรือ attended capture matrix (RE-088's own nonclaim) — ไม่เปิดใบ RE ใหม่รอบนี้ ไม่มีอะไรให้ถอดเพิ่ม แค่ต้องมีเฟรมจริงมาเทียบ
- `TeleportTarget` field-order ยังไม่เทียบกับ 132 candidate frame ที่ `A2_STATIC_OPEN` (ค้างจากรอบก่อน ไม่ใช่ของใหม่รอบนี้)
