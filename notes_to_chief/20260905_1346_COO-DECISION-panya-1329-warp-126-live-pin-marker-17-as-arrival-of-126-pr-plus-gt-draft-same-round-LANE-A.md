[ถึง: LANE-A | จาก: COO | 2026-09-05T13:46+07:00 | ตอบ: `20260905_1329_PANYA-DECISION-warp-126-*.md`]
ADDRESSEE: LANE-A
cc: LANE-GM (ใบ `1347` ของตัวเอง) · chief (ตั้งเลข GT · ใบ `1349`) · ka1-A · Panya

# COO-DECISION — รับ PANYA `1329` ทั้ง 4 ข้อ: จุดมาถึงถาวรของฉาก 126 = MARKER `n_ID 17` (3050, 232, 90, heading 6) · LANE-A ปักลง registry รอบ 14:21 พร้อมร่างใบ GT ในรอบเดียวกัน

## ตัดสินว่าอะไร
1. `/warp 126` (ไม่ใส่พิกัด) ต้องวาปสดเหมือน `/warp 2` — ไม่ใช่ `STAGED_NEXT_LOGIN` · คำ Panya เป็นคำสั่ง ไม่ต้องวัดใหม่
2. ต้นเหตุวัดจาก main `173addc` (COO ตรวจเอง 13:4x): `gm/warp_executor.py:469 warp_no_coords_live_target` เกตที่ `has_authored_entry` (= `entry_marker != 0`) · แถว 126 ใน `world_scene_travel.py` มี spawn แต่ `n_MARKER == 0` ตามตาราง `CONSTDATA_TH__SCENE_NAME` ⇒ คืน `None` ⇒ stage · **ครึ่งของ LANE-A ที่ค้างตั้งแต่ `CHIEF-DECISION 20260829_1603` item 1 (`login_scene_admission.py:72`) คือช่องว่างตรง ๆ**
3. วิธีปิด = **ของ LANE-A (เจ้าของ registry ตาม `1148`)**: ให้ 126 มี arrival ที่ `has_authored_entry` เป็นจริง โดยยกแถว `CONSTDATA_TH__MARKER.tsv` `n_ID 17` (`n_SCENE 126`, 3050/232/90, heading 6) เป็นหลักฐาน — evidence tier ใหม่ที่ระบุที่มาว่า "MARKER row ที่ client ใช้เอง + `PANYA-DECISION 1329`" ห้ามอ่อนตัวการตรวจ `n_MARKER` ของฉากอื่น (เทสปักฉาก 278/`GT-141` ต้องยังยืนตามเดิม) · ห้ามเดา heading ที่ teleport ใช้ (ใส่เป็นข้อสังเกตในใบ GT)
4. ตามคำตัดสิน `1130` ข้อ 1: **PR + ร่างใบ GT ในรอบเดียวกัน** — ใบ GT ตามข้อความใน `1329` §"ใบ GT": จาก Port Royal พิมพ์ `/warp 126` → กลายเป็นเรือใน "Atlantic Ocean: Rising Sun Sea" ที่ (3050,232,90) ทันที ไม่ relogin · `character_positions` บันทึก scene 126 ทันที (`PANYA 20260904_1430`) · ควบคุม `/warp 126 3050 232 90` · STOP ถ้า client ปิด/ค้าง (rollback `GT-258` `#806`) · พ่วงบูตอื่นได้ · chief ตั้งเลข (ใบ `1349`)
5. ยืนยันบนสายว่าวาปสดจริง = **LANE-GM** (ใบ `1347`) หลัง PR นี้บน main · LANE-A ไม่ต้องแตะไฟล์ `gm/`

## เพราะอะไร
ค่า 3050/232/90 ไม่ใช่ค่าชั่วคราวอีกต่อไป — มีอยู่ในไคลเอนต์ (MARKER 17) และ `WORLD_SCENE scene_id=126` ใช้ทุกรอบ (R313/R318) · Panya ยืนยันเองว่าให้ปักถาวร · ก = ข้อเดียวของ registry ที่ขาด ตัวส่ง teleport สดมีแล้ว (`WARP_CROSS_SCENE_LIVE_TELEPORT_AUTHORIZED = True` · `#745`)

## ใครทำอะไร · กำหนด
- LANE-A รอบ **14:21** (ทำก่อนใบ `1348` ข้อ 2 — ใบนี้เล็กกว่าและเป็นคำสั่ง Panya): PR เซิร์ฟเวอร์ registry 126 + เทสปัก `warp_no_coords_live_target(126)` คืนเป้า 3050/232/90 + ร่างใบ GT ในไฟล์รอบ · ตอบ `TWO_SESSIONS_SAME_SCENE:` · **ตก 15:51** = escalation
- ต่อคิวเดียวกัน (ใบ `1348` ข้อ 3): marker ฉาก 304/305 ใช้วิธีเดียวกันนี้
