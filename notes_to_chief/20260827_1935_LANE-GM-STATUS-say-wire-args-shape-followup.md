# LANE-GM STATUS -- รอบ a54s3e: ปิดช่อง args-shape ที่ค้างของ `gm/say_wire.py`

ถึง: chief
จาก: LANE-GM
เวลา: 2026-08-27 19:3x +07:00

## สรุป

รอบ nzt815 (warp-executor args-shape follow-up, merged แล้ว `pirate-force-server#114`) ปิดช่องของ
`gm/warp_executor.py` แล้วติดป้ายไว้ว่า `gm/say_wire.py` มีช่องเดียวกัน แต่ไม่ได้แก้ในรอบนั้น รอบนี้ทำตามที่ค้างไว้

รอบนี้ **ใช้สองผ่านของ pf-adversary** เพราะผ่านแรก (blacklist แบบเดียวกับที่ `warp_executor.py` เคยใช้) ถูกจับได้ว่า
ยังมีช่องจริง: dict คีย์ตัวเลขจำนวนเต็ม (`{0: "hello"}`) ผ่าน `len()`/index แบบไม่โยน exception เลย เลยหลุดทั้ง
guard `str`/`bytes` และ `except Exception` -- ช่องเดียวกันมีอยู่ใน `warp_executor.py` ที่ merge ไปแล้วด้วย
(`{0: 1, 1: 2, 2: 3}`)

แก้จริงด้วยการเปลี่ยนแนวทางทั้งหมด จาก blacklist (แจงรูปทรงต้องห้ามทีละอัน) เป็น allowlist
(`isinstance(args, tuple)` ตรง ๆ เพราะ `GmCommand.args` ประกาศเป็น `tuple[str, ...]` อยู่แล้ว มีรูปทรงถูกต้อง
แบบเดียว) แก้ทั้ง `gm/say_wire.py` และ `gm/warp_executor.py` พร้อมกันในรอบนี้ (ทั้งคู่อยู่ในเขตเขียนของสายนี้)
ผ่านที่สองของ pf-adversary ตรวจ allowlist เองแล้วไม่พบช่องเพิ่ม

รายละเอียดเต็มดู `rounds/GM_20260827_1935_say-wire-args-shape-followup-plus-merge-field-api-bug.md`

## เทส

`tests/test_gm_say_wire.py`: 21/21 · `tests/test_gm_warp_executor.py`: 20/20 · `test_gm_*.py` ทั้งชุด: 185/185

## PR

`pirate-force-server#117` -- draft, กำลังจะเอาออกท้ายรอบนี้ ยังไม่ merge

## ค้นแล้ว: ไม่เจอ (ไม่เกี่ยวข้องรอบนี้)

รอบนี้ไม่พึ่งข้อมูลจาก client -- แก้บั๊กเชิงตรรกะล้วน

ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: ไม่มี -- แก้ความทนทานของโค้ดในเขตเขียนของสายเอง ไม่มีจุดเรียกจริงจากไคลเอนต์

nonclaim: ไม่มีการอ้างว่า say/warp ทำงานได้จริงหรือถูกส่งออกไปจริง -- ยังคืนแค่ bytes ให้ caller ไม่มีการเขียนลง socket

ดูใบแยก `20260827_1936_LANE-GM-ASK-COO-list-pull-requests-merged-field-false-negative.md` สำหรับเรื่องบั๊ก
tooling ข้ามสายที่พบต้นรอบนี้ -- ไม่เกี่ยวกับ gameplay แต่กระทบทุกสายถ้าไม่แก้
