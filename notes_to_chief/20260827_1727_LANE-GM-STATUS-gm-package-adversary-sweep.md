# LANE-GM STATUS -- รอบ 50x5xt: กวาด `pf-adversary` ทั้งแพ็กเกจ `gm/` ปิดช่องจริง 2 ข้อ (HIGH+MEDIUM)

ถึง: chief
จาก: LANE-GM
เวลา: 2026-08-27T17:27+07:00

## สรุป

ต้นรอบนี้ RE ทุกใบของสายนี้ปิดหมดแล้ว (`RE-088` ถึง `RE-105`) และ `CORE-REQUEST-011`/`012`/`015` ยังรอ
chief ต่อสาย -- ไม่มีงาน wire ใหม่ในเขตเขียนของตัวเอง ตามกฎ ADDENDUM ข้อ F เลยหยิบ technical debt:
รัน `pf-adversary` กับทั้งแพ็กเกจ `gm/` (12 โมดูล) เป็นครั้งแรก (ก่อนหน้านี้มีแต่รอบที่ตรวจทีละไฟล์ตามงาน
ที่เพิ่งแก้)

พบ 3 ข้อ แก้จริง 2 ข้อ:

1. **HIGH**: `gm/dispatch.py` เรียก `capture_raw_gm_command` (เขียนดิสก์จริง) โดยไม่มี `try`/`except`
   ทั้งที่ docstring อ้างว่าปิด "refuse by name, not by crash" ไว้แล้ว -- จริง ๆ ครอบแค่จุด lookup บัญชี
   `OSError` จากดิสก์เต็ม/สิทธิ์ไม่พอ/`capture_root` ชนไฟล์เดิม จะหลุดออกจาก handler ได้ เนื่องจาก
   `CORE-REQUEST-010` ต่อสายจุดนี้แบบ always-on ไม่มี try/except ล้อมที่ `runtime.py` ด้วย ความเสี่ยงคือ
   คำสั่ง GM ที่ authorized ถูกต้องคำสั่งเดียวอาจฆ่า connection-handling thread ทั้งเธรดสำหรับผู้เล่นทุกคน
   **แก้แล้ว**: ครอบด้วย `except OSError` คืน refusal reason แทนการโยนหลุด
2. **MEDIUM**: `gm/commands.py` สามฟังก์ชัน (`describe_warp_target`/`describe_npc_target`/
   `log_gm_command`) ไม่มี shape guard บน `command.args` เลย -- ช่องเดียวกับที่ `say_wire.py`/
   `warp_executor.py` เคยปิดไปแล้วแต่ไม่เคยย้อนมาแก้ไฟล์นี้ dict คีย์ตัวเลขทำให้ log เขียนคีย์แทนค่าจริง
   แบบเงียบ ๆ **แก้แล้ว**: เพิ่ม `_require_args_tuple()` (exact-type `type(args) is tuple`) เรียกทั้งสามจุด
3. **MEDIUM (deferred โดยตั้งใจ)**: ไม่มี rate limit ต่อบัญชีสำหรับ capture -- บันทึกเหตุผลไว้ใน
   `docs/GM_LANE.md` (ต้องมี shared state ข้าม call จริงจัง สมควรมีรอบของตัวเอง ไม่ใช่ปะท้ายรอบนี้)
   ไม่ใช่ CORE-REQUEST (อยู่ในเขตเขียนสายนี้ล้วน)

**ไม่พบ**: ไม่มีทางที่บัญชีนอก `gm_accounts` จะได้ capability ใด ๆ -- gate ยังปฏิเสธก่อนเสมอ ไม่มีบั๊ก
wire-decode ใน `command_wire.py`/`teleport_wire.py`/`state_wire.py`

pf-adversary ตรวจซ้ำ (subagent ที่สอง) ยืนยันทั้งสองข้อที่แก้ปิดจริง ไล่ทุกจุดโยน exception ได้จาก
`capture_raw_gm_command` ยืนยันเป็น `OSError` ทั้งหมด และไม่มีจุดอื่นแตะ `command.args` แบบไม่มี guard
เหลืออยู่ พบเพิ่มเรื่องเล็ก (loop retry ชน filename ใน `command_capture.py` ไม่มีเพดานรอบ -- severity ต่ำ
บันทึกคู่กับข้อ 3)

รายละเอียดเต็ม: `rounds/GM_20260827_1727_gm-package-adversary-sweep-capture-write-and-args-shape.md`

## เทส

`test_gm_*.py` ทั้งชุด: 215/215 (189 เดิม + 26 ใหม่) · repo-wide `unittest discover`: 3587 tests, error
เฉพาะ 18 รายการเดิม (`capstone` import, ไม่เกี่ยวข้อง)

## PR

`pirate-force-server#134` -- draft, กำลังจะเอาออกท้ายรอบนี้ ยังไม่ merge · `pf_bridge#218` (จดหมาย+รอบไฟล์
เท่านั้น ไม่มีโค้ด)

## ค้นแล้ว: ไม่เจอ

รอบนี้ไม่พึ่งข้อมูลจาก client เลย -- แก้ความทนทานของโค้ดล้วนบนโครง wire ที่พิสูจน์แล้วทั้งหมด

ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: ไม่มีจุดเรียกจริงจากไคลเอนต์ที่เปลี่ยน -- แต่ถ้า GT-103 (attended
capture matrix ที่คิวไว้แล้ว) เจอดิสก์เต็มหรือปัญหา `capture_root` ระหว่างเทส เมื่อวานเซิร์ฟเวอร์เสี่ยง
เธรดล่มทั้งเธรด วันนี้แค่ capture คำสั่งนั้นไม่สำเร็จคำสั่งเดียว ผู้เล่นอื่นไม่กระทบ

nonclaim: ไม่มีการอ้างว่าคำสั่ง GM ใดทำงานจริงหรือถูกส่งออกไปจริง -- ไม่มีจุดส่งข้อมูลไปยัง socket ในรอบนี้
ไม่มีการเปลี่ยนพฤติกรรมบน happy path ไม่มีการแก้ `runtime.py`
