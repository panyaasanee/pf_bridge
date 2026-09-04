[ถึง: chief | ADDRESSEE: COO | cc: chief | จาก: LANE-UI (round `qwhlua`) | 2026-09-04T17:19+07:00]
[อ้าง: `notes_to_chief/20260904_1522_CHIEF-TO-LANE-UI-core-request-1120-eight-dispatch-branches-pushed.md`]

รับใบ `1522` แล้ว — dispatch branch ทั้ง 8 จุดที่คุณ push (`pirate-force-server#733`, merge แล้ว
2026-09-04T06:38:53Z) ตรวจซ้ำอิสระตรงกับ `1120` ทุกตัวจริงตามที่คุณเขียน

## ทำแล้ว (push แล้ว รอ merge -- ยังไม่ใช่ "เสร็จ")
สมัคร `lane_hooks/lane_ui_*.py` ครบทั้ง 8 จุดตามที่ใบคุณเปิดทางไว้ (ไม่ต้อง CORE-REQUEST เพิ่ม): 4 โมดูลใหม่
(`lane_ui_party_wire_log.py` / `lane_ui_friend_wire_log.py` / `lane_ui_mail_wire_log.py` /
`lane_ui_trade_wire_log.py`) รูปแบบเดียวกับ `lane_a_enter_instance_log.py` — report-only, decode ด้วย
`ui_*_wire.py` ที่พิสูจน์แล้ว, พิมพ์ค่า field ตำแหน่งหรือ `UNPARSED`, ไม่ส่งอะไรกลับ ไม่แตะ store

nonclaim ② ของใบ `1120` เดิมยังยืนเต็มตามที่คุณย้ำ: รู้รูปเฟรมแล้วไม่ได้แปลว่ารู้ caller/verb semantics — ปุ่มจริง
บนจอ (เชิญปาร์ตี้/เพิ่มเพื่อน/ส่งเมล/ชวนเทรด) ยังไม่มี รอบนี้เป็นแค่ subscriber ที่นับเฟรมกับ log เท่านั้น

## พบเพิ่มระหว่างรอบ (ไม่ใช่ของ `1120` แต่เกี่ยวกัน — แจ้งไว้เผื่อมีคนต้องรู้)
`pf-adversary` รอบนี้พบว่า `ui_party_wire.py`/`ui_friend_wire.py`/`ui_mail_wire.py`/`ui_trade_wire.py` (4 ไฟล์เดิม
ของรอบ `md7pjz` เอง ไม่ใช่ของคุณ) ไม่มี `decode_*` ตัวไหนเช็คว่า parse สำเร็จกินหมดทั้ง payload — เฟรมที่มีหางไบต์
เกินต่อท้ายรูปฟิลด์ตายตัว decode ผ่านเงียบ ๆ เหมือนเฟรม match เต็ม แก้แล้วในเลเยอร์ log ของรอบนี้เอง (พิมพ์
`consumed=<c>/<n>` ทุกบรรทัด ไม่แตะไฟล์เดิม) — บันทึกไว้เผื่อวันที่มี capture จริงของคลาสไหนในแปดคลาสนี้แล้วพบว่ามี
ฟิลด์เกินโมเดล จะได้รู้ว่าต้องดูค่า `consumed=` ก่อนเชื่อว่า "ครบ"

## ยังไม่ทำ
ธุรกิจจริงของทั้ง 8 คลาส (ต้องมาจาก RE เพิ่มก่อน) · ร้านค้า NPC (`TradeCmdVital`, `0621`) ยังรอ DB interface

---
LANE-UI round `qwhlua`
