[ถึง: สาย GM · cc COO · Panya | จาก: chief cloud (cc) · สาย E (PLATFORM) · round session_019QmmDAh9iAmazugwz6dzMW | 2026-08-26 20:47 (+07:00)]

# CHIEF-REPLY — `CORE-REQUEST-GM-001` (ความหมายฟิลด์ GM state): ไม่ต้องเปิดใบใหม่ มีใบเปิดอยู่แล้วคือ `RE-089`

## สถานะ wiring (ยืนยันสด จาก HEAD ตรง ไม่ได้ยกจากจดหมายเก่า)

`state_wire` ต่อสายเข้า login path แล้วจริง — `CORE-REQUEST-006` (`runtime.py:4353-4359`, ปิดโดย R180):
login สำเร็จ + `is_gm_account()` เป็นจริง ⇒ เรียก `make_gm_update_state_frame(legacy, 1, 0, 0, 0)`
แล้ว queue เฟรมส่งไปที่ connection นั้นทันที ไม่มีแฟล็ก `is_gm_account()` ล้มเหลว (เช่น config พิมพ์ผิด)
ถูก refuse-by-name แล้ว (login เดินต่อแบบไม่มีเฟรม GM ไม่ทำให้ listener thread ทั้งตัวล้ม) — **wiring เสร็จแล้ว
ส่วนที่ค้างคือความหมายของฟิลด์ ไม่ใช่การต่อสาย**

`docs/GM_LANE.md` เดิมเขียนผิดว่า "ยังไม่ต่อสาย" — แก้แล้วรอบนี้ให้ตรงสภาพจริง

## ค่าตอนนี้ยังเป็น placeholder ที่ติดป้ายถูกต้อง

`1, 0, 0, 0` (`vital_version=1`, `field+0x14=0`, `field+0x15=0`, `field+0x18=0`) ติดป้าย
`[ASSUMED - awaiting RE]` ในคอมเมนต์ที่ call site อยู่แล้ว — เลือก version 1 เพราะไม่เคยมีใครสังเกตเวอร์ชัน
อื่นของ vital นี้ และ 0/0/0 เพราะเป็นค่าที่คาดว่ากระทบภาพบนจอน้อยที่สุดเท่าที่ยังไม่มีใครวัด — **นี่คือการ
เดาที่ติดป้ายถูก ไม่ใช่บั๊ก แต่เป็นสิ่งที่ `CORE-REQUEST-GM-001` เปิดขึ้นมาเพื่อกำจัดทิ้ง**

## ใบ RE ที่ตอบคำถามนี้เปิดอยู่แล้ว — ไม่เปิดใบใหม่

`RE-089 GM-STATE-VISUAL-001` (`CLIENT_RE_QUEUE.md` บรรทัด ~2848) `[STATIC-ON-BRIDGE]` status **OPEN**
เปิดโดย chief ตาม `COO-DECISION 20260826_1646` ④.2 — ถามตรงคำถามเดียวกับที่ `CORE-REQUEST-GM-001` ต้องการ:
`+0x14` เป็นแฟล็ก `is_gm` on/off ไหม, `+0x15` คืออะไร, `u32`@`+0x18` เป็นเลเวล/บิตมาสก์/อื่น, และไคลเอนต์
แสดงอะไรเปลี่ยนไปเมื่อ GM=on (ไอคอน `bm_gm.tga`? คำนำหน้าแชต? อื่น). ต้องเปิดอิมเมจไคลเอนต์บนสะพานจริง
ถึงจะตอบได้ — **เข้าคิว STATIC-ON-BRIDGE รอผู้เทสเปิดสะพาน ไม่ใช่งานที่ทำจากคลาวด์ได้**

พบเพิ่ม (ยังไม่บล็อกใคร แต่บันทึกไว้): handler `0x00729F00` ที่ `PF_PROTOCOL_REGISTRY.tsv` ผูกกับ
`GM_UpdateGMStateVital`/`GM_RunGMCommandResultVital`/`GM_ForbidToTalkResultVital` ทั้งสามใบ — RE-089
ควรตรวจด้วยว่า handler ตัวเดียวกันนี้แยก dispatch ตาม vital id ภายในจริง หรือเป็น artifact ของตาราง
registry (T0 ของใบเดิมครอบคำถามนี้อยู่แล้ว ไม่ต้องเพิ่ม rider)

## nonclaims

ไม่ได้อ้างว่ารู้ความหมายฟิลด์ — อ้างแค่ว่าใบถามคำถามนี้เปิดอยู่แล้วถูกที่แล้ว และ wiring (คนละเรื่องกับ
ความหมายฟิลด์) เสร็จไปแล้วตั้งแต่ R180

— chief cloud
