# GM round 2026-08-27 ~15:3x-16:0x (+07:00) -- `say` wire-builder built via import from `channel_message_hypothesis.py` (CORE-REQUEST-012)

ยึดล็อกด้วย draft PR ทั้งสอง repo ก่อนเริ่ม (`pf_bridge#182`, `pirate-force-server#106`) -- ตรวจ GitHub API ก่อนยึดล็อกตาม ADDENDUM v6.2 ข้อ A: PR ล่าสุดของสายนี้ที่ `state=closed` ทั้งสอง repo (`pf_bridge#175`, `pirate-force-server#101`) ตรวจด้วย `git merge-base --is-ancestor` แล้วยืนยันว่า **merged=true จริง** (แม้ `list_pull_requests` API คืนค่า `merged: false` -- นี่คือความคลาดเคลื่อนของ field ใน list API ไม่ใช่หลักฐานว่า PR หาย, ยืนยันด้วย git ancestry ซึ่งเชื่อถือได้กว่า) จึงไม่ต้อง cherry-pick กู้อะไร

## ตรวจสถานะก่อนเริ่มงานจริง

ยืนยัน `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (ขั้นแรกบังคับของทุกรอบ) · อ่านจดหมาย order 1630 ซ้ำ · อ่านรอบก่อนหน้าเต็มฉบับ (`20260827_1415` broadcast-wire retracted) รวมถึง `docs/GM_LANE.md` เต็มไฟล์ (435 บรรทัด) ก่อนเริ่ม

**พบระหว่างตรวจ: main ของทั้งสอง repo เดินหน้าไปหลังจาก clone ครั้งแรกของ session นี้** (`pirate-force-server` origin/main จาก `b9273b5` ขยับเป็น `69640b6`, `pf_bridge` จาก `2214742` เป็น `c759fbf`) -- `git merge --allow-empty` ทั้งสอง repo ก่อนเริ่มงานจริงและก่อน push (ตามธรรมเนียม "merge origin/main before push" ที่เห็นใน git log อยู่แล้ว) เพื่อไม่ให้ PR ชนกับ history ใหม่

**สิ่งสำคัญที่พบในการ merge**: chief round R190 (`pirate-force-server@dfa61ac`) ต่อสาย `CORE-REQUEST-010` (LANE-GM inbound dispatch 0x51E9) เข้า `runtime.py` แล้วจริง -- `GM_RUN_GM_COMMAND_VITAL_ID` branch, ALWAYS ON ไม่มี scenario flag, เรียก `handle_gm_run_command_vital` ที่ `gm/dispatch.py` มีอยู่แล้ว นับ/authorize/refuse ทุกเฟรม 0x51E9 ที่เข้ามาและเขียน capture file ให้บัญชี GM จริง แต่**ยังไม่ decode สองสตริงเป็น `GmCommand` และไม่ส่งอะไรกลับ** -- ไม่กระทบงานรอบนี้โดยตรง แต่ทำให้ `docs/GM_LANE.md` ต้องแก้ให้ตรงกับ main ปัจจุบัน (ทำแล้ว ดูด้านล่าง)

## ตัดสินใจเลือกงานของรอบนี้

รอบก่อน (`20260827_1415`) ทิ้งคำแนะนำไว้ชัดใน `docs/GM_LANE.md`'s "Attempted and retracted" section: `say` ต้องการ wire builder ที่ **import** จาก `channel_message_hypothesis.py` (ของจริงที่พิสูจน์แล้ว 9 วันก่อนหน้า) ไม่ใช่สร้าง codec คู่แข่งเอง -- ตรงตาม GM-003's กฎเดิม "ใช้ของสายอื่นผ่าน import เท่านั้น ห้ามก๊อปตรรกะ" งานของรอบนี้คือทำสิ่งนั้นให้เสร็จ ตามแพทเทิร์นเดียวกับ `gm/warp_executor.py` ที่บริดจ์ `warp` เข้ากับ `gm/teleport_wire.py`

## สิ่งที่สร้าง

**ค้นแล้ว: เจอ** -- อ่าน `channel_message_hypothesis.py` เต็มไฟล์ (910 บรรทัด) ก่อนเขียนโค้ด ยืนยัน `encode_channel_message`/`make_channel_message_response` เป็น pure function ไม่ต้องผ่าน scenario/test_only gate ใด ๆ (gate นั้นคุมแค่ path ของ dispatch ผ่าน scenario JSON ซึ่งเป็นคนละเรื่องกับการเรียกฟังก์ชัน encode ตรง ๆ) และ `SHARED_SERIALIZER_CHANNEL_IDS["Channel_GMGlobalMessageVital"] = 0x9F2C` คือ dict object เดียวกับที่โมดูลอื่นใช้ ไม่มีการ copy ค่าที่จะ drift ได้

- **ใหม่** `src/pirateforce_foundation/gm/say_wire.py` -- `make_say_broadcast_frame(legacy, command, *, speaker="")` บริดจ์ `GmCommand` ชนิด `say` เข้ากับ `make_channel_message_response` ของ `channel_message_hypothesis.py` ตรง ๆ ไม่มีความรู้เรื่อง wire format ใหม่เพิ่มเลยสักบิต (field order/tag byte/length width/envelope math ทั้งหมดมาจากโมดูลที่พิสูจน์แล้ว) โมดูลนี้ไม่ส่งอะไรออกไปจริง คืนแค่ frame bytes ให้ caller เหมือน `warp_executor.py`
- **ใหม่** `tests/test_gm_say_wire.py` -- พิสูจน์ว่าเฟรมที่สร้างตรงกับ `make_channel_message_response` ไบต์ต่อไบต์, round-trip ผ่าน `decode_channel_message`, และ `GM_GLOBAL_CHANNEL_ID` เป็น object เดียวกับตาราง `SHARED_SERIALIZER_CHANNEL_IDS`

## `pf-adversary`

สองรอบ:

1. **ดราฟต์แรก**: พบ 2 ข้อจริง
   - **MEDIUM-HIGH**: `gm/commands.py`'s `MAX_SAY_MESSAGE_LENGTH` (480 ตัวอักษร) ถูกเช็คเฉพาะใน `parse_gm_command` เท่านั้น -- `say_wire.py` คือขั้น execution ที่คอมเมนต์เดิมของ cap นี้บอกตรง ๆ ว่าต้องมีตอน "execution ถูกต่อสาย" แต่ `GmCommand` ที่สร้างมือ (ตามกฎ "regardless of source" ของ `docs/GM_LANE.md`) ข้าม `parse_gm_command` ได้เสมอ ⇒ cap หายไปเงียบ ๆ
   - **MEDIUM**: `command.args` ถูกเข้าถึงด้วย `len()`/`[0]` ตรง ๆ ไม่มี guard -- `args` ที่มีรูปร่างผิด (`None`, `set`, `dict`) จะ leak `TypeError`/`KeyError`/`IndexError` แบบดิบ ไม่ใช่ `SayWireError` ตามที่ docstring/เทสสัญญาไว้ (พบว่า `gm/warp_executor.py` มีช่องโหว่แบบเดียวกันด้วย -- inherited มาจาก pattern เดิมที่รอบนี้ก็อบมา ไม่ใช่ของใหม่ที่ `say_wire.py` สร้างเอง)
   - แก้ทั้งสองข้อ: import cap มาเช็คซ้ำ (ไม่ redefine ค่า), ห่อ `len()`/indexing ด้วย `try/except` แปลงเป็น `SayWireError` เพิ่ม 5 เทสยืนยัน
2. **ยืนยันซ้ำ**: ตรวจ boundary ของ cap (480 ผ่าน, 481 ไม่ผ่าน ตรงกับ `parse_gm_command` เป๊ะ ไม่มี off-by-one), ตรวจ exception scoping ว่าไม่ swallow ผิดจุด, รัน `None`/`set`/`dict` ทั้งสามรูปแบบยืนยันแปลงเป็น `SayWireError` ครบ -- ปิดทั้งสองข้อจริง ไม่มีข้อใหม่จาก`say_wire.py`เอง

**ค้าง (ตั้งใจ ไม่แก้รอบนี้)**: `gm/warp_executor.py` มีช่องโหว่ args-shape เดียวกัน (`None`/`set`/`dict` args leak bare exception) -- ยืนยันแล้วว่ายังอยู่จริง แต่นอกขอบเขตของรอบนี้ (`say_wire.py` เท่านั้น) บันทึกไว้ใน `docs/GM_LANE.md` เป็นรอบถัดไป

## เทส

`test_gm_*.py`: 168 ข้อผ่านหมด (163 เดิมหลัง merge origin/main [150 ก่อนหน้า + 4 จาก `CORE-REQUEST-010` landing ที่ merge เข้ามา] + 14 ใหม่ของ `say_wire` [9 ดราฟต์แรก + 5 จาก pf-adversary fix]) · สวีตเต็มโปรเจกต์: `3467` เทสรัน, ผิดพลาด 18 ข้อ (ทั้งหมดคือ `ModuleNotFoundError: No module named 'capstone'` ในเทส static-RE ที่ต้อง disassembler -- ยืนยันแล้วว่าเป็นข้อจำกัดสภาพแวดล้อม cloud clone เดิม ไม่เกี่ยวกับรอบนี้ ไม่มีเทสของ `test_gm_*` อยู่ในรายการที่พัง)

## `docs/GM_LANE.md` ที่แก้

- แถว `0x9F2C` ในตาราง wire-facts: เพิ่มว่า `gm/say_wire.py` บริดจ์แล้ว
- เพิ่มหัวข้อ "Modules delivered (say-wire round)" เต็ม
- แก้หัวข้อ "What is intentionally NOT built yet": บันทึกว่า `CORE-REQUEST-010` ต่อสายจริงแล้ว (R190) พร้อมระบุว่ายังไม่มี command source จริงที่จะขับ `warp_executor.py`/`say_wire.py` ได้ (เพราะยังไม่ decode สองสตริง) และเพิ่ม `CORE-REQUEST-012` เข้ารายการที่ยังไม่ถูกต่อสาย

## จดหมาย

`notes_to_chief/20260827_1600_LANE-GM-CORE-REQUEST-012-say-broadcast-wire.md`
`notes_to_chief/20260827_1600_LANE-GM-STATUS-say-wire-frame-builder.md`

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- โมดูลที่สร้างยังไม่มีจุดเรียกจริงใน `runtime.py` (ไม่มี command source จริงที่ผลิต `GmCommand` ชนิด `say` จาก client จริงได้ เพราะ `GM_RunGMCommandVital`'s สองสตริงยังไม่ถูก decode) แม้ chief ต่อสาย `CORE-REQUEST-012` ก็ยังต้องรอ command source นั้นก่อนถึงจะมีอะไรให้ผู้เทสลอง

## nonclaim

ไม่มีการอ้างว่า `say` broadcast ทำงานได้จริงหรือถูกส่งออกไปจริง -- `make_say_broadcast_frame` คืนแค่ bytes ให้ caller เท่านั้น ไม่มีการเขียนลง socket ไม่มีการ track player state ไม่มีบัญชีใดได้อะไรที่ไม่เคยได้มาก่อนรอบนี้

## ค้าง (ตั้งใจ ไม่บล็อก)

- `CORE-REQUEST-011`/`CORE-REQUEST-012` รอ chief ต่อสายจริง -- แต่ทั้งคู่รอ command source จาก 0x51E9 ที่ยัง decode ไม่ได้ (RE territory) หรือทางอื่นที่ chief เห็นเหมาะกว่า (เช่น console/debug command)
- `gm/warp_executor.py`'s args-shape gap (เหมือน `say_wire.py` ก่อนแก้) -- ยังไม่แก้
- การ decode สองฟิลด์ wide-string ของ `GM_RunGMCommandVital` เป็นชื่อคำสั่ง/argument จริง ยังต้องรอ RE หรือ attended capture matrix -- ค้างจากหลายรอบก่อน ไม่ใช่ของใหม่
- `TeleportTarget` field-order ยังไม่เทียบกับ 132 candidate frame ที่ `A2_STATIC_OPEN` -- ค้างจากหลายรอบก่อน ไม่ใช่ของใหม่
