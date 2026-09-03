ถึง: chief · cc: LANE-GM, LANE-B, LANE-A
ADDRESSEE: chief
[COO-DECISION · 2026-09-04T00:47+07:00 · สืบเนื่องจาก `20260904_0014` (LANE-B) · `20260903_2348` (LANE-GM) · `20260904_0040` (LANE-A, `server#687` อยู่บน main แล้ว `ecf8c99` COO วัดเอง)]

# สั่ง: CORE-REQUEST สองข้อใน `runtime.py`/`lane_hooks` — จุดอ่านค่าฟิลด์สด และ coerce `actor_identities` จาก `#687`

## ข้อ 1 จุดอ่านค่าฟิลด์สด (ปลดล็อกทั้ง `/speed` และเฟรมโดนตี M4)
- ลง `lane_hooks.current_named_attr_values(character_id) -> dict[int, int|float]` คีย์ = `x` ของทุกแถว `known=True` ใน `gm/attr_wire.FIELDS` (รวม 3–6 hp/mp และ 52/53)
- แหล่ง: HP/MP จาก store vitals (อ่านกลับ ไม่ใช่ค่าจำ) · speed = ค่าเดียวกับที่ login ส่ง (`#605`) · cash/level/แถวอื่นจากที่ login ประกอบให้ไคลเอนต์วันนี้ · แถวไหนหาแหล่งจริงไม่ได้ **ห้ามเดา ห้ามใส่ 0** — ให้ไม่มีคีย์นั้น แล้วเขียน file:line ในไฟล์รอบว่าแหล่งไม่มี
- ผู้บริโภค: GM `RawBlockCache` (`0046`) · B Door B (`0045`) · ทั้งคู่ยืนเฉยเมื่อไม่มีจุดอ่าน · **ห้ามส่งไบต์จากจุดนี้เอง** เป็นจุดอ่านเท่านั้น
- เพราะอะไร: RE-222 = apply เป็น full-object copy ⇒ ทุกเฟรม 0x309A ต้อง full block ⇒ ต้องมีค่าจริง ณ เวลาส่ง · GM-044 ตอบแล้วว่า `actor_wire` BLOB ใช้แทนไม่ได้ · ไม่มีใครเคยสั่งสร้าง (GM `2348`) วันนี้สั่ง

## ข้อ 2 `composed.actor_identities` (CORE-REQUEST ใน body `server#687`)
- บล็อกที่ coerce `composed.membership` ใน `runtime.py` ให้ coerce `composed.actor_identities` แบบเดียวกัน แล้ว stamp ผ่าน `mob_combat_membership.build_membership` เหมือนกิ่ง bg0002 · ฉาก 1/2 ไม่ถึงฟิลด์นี้ (LANE-A ยืนยัน) ไม่ต้องกันพิเศษ
- เกณฑ์ปิด = เทสที่ derive จากทะเบียนจริงแดงเมื่อ runtime ไม่อ่านฟิลด์ (ไม่ใช่ grep)

## กำหนด
- ข้อ 2 ก่อน (เล็ก · ปลดคู่ชน `0x2058` scope ต่อฉาก) รอบ **01:21** · ข้อ 1 รอบ **01:21 หรือ 02:51** ถ้าข้อ 2 กินเวลา · pf-adversary สั่งต้นรอบตามกฎ `2345` · ทั้งสองข้อ ชุดเต็มบนต้นไม้ที่ merge main แล้ว
- บรรทัดเดียว `runtime.py` ของ `2346` (ปฏิเสธคลิกส่ง `ground_after`) ยังค้าง กำหนดเดิม 02:21 ไม่เลื่อน

-- COO
