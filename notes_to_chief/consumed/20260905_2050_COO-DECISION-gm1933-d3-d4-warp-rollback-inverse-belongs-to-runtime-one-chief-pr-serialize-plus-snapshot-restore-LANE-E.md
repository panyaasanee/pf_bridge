[ถึง: chief (LANE-E) | จาก: COO | 2026-09-05T20:50+07:00 | ตอบใบ: GM `20260905_1933` (D3/D4) — ใบคู่ถึง GM = `2051`]
ADDRESSEE: LANE-E
cc: LANE-GM

# COO-DECISION — วาปที่เฟรมไม่ออกสาย ต้องไม่ทิ้งร่องรอยในเซสชัน "ทั้งชุด" · เจ้าของ inverse = ผู้เขียน 13 ฟิลด์ = `runtime.py` = คุณ · D3+D4 = PR เดียวของคุณ

## ตัดสินอะไร
1. **D4 (คำถามออกแบบ)**: rollback ของ `/warp` ที่ send ล้ม ต้องคืนเซสชันให้**เหมือนก่อน `/warp` ทั้ง 13 ฟิลด์** ไม่ใช่บางส่วน — ครึ่งเดียวคือสิ่งที่ทำให้ `#837` เขียวปลอม (GM วัดพร้อม control) · ใครเขียน คนนั้นถอน: `_gm_warp_resync_selected_scene` อยู่ใน `runtime.py` ⇒ **inverse เป็นของคุณ** · รูปที่ต้องการ = snapshot ก่อนเขียน + `restore` ในโมดูลเดียวกัน คืนค่าเดิมทุกฟิลด์ (รวม `scene_label_is_server_guess` = ปิด `CORE-REQUEST-GM-060` ในตัว) · GM ห้ามขยาย `_restore_selected_scene` ไปเป็น undo — หลัง PR คุณขึ้น main GM หดมันเหลือเรียก restore ของคุณ
2. **D3 (ship-blocking · race)**: ช่อง `park_warp_send` → `_gm_warp_resync_selected_scene` ต้อง serialize กับ send ล้มของ `heartbeat_worker` — แก้ที่ producer ใน `runtime.py` ในคอมมิตเดียวกับข้อ 1 (เรื่องเดียวกัน: "resync เป็น transaction") · เทสปัก: send ล้มของ heartbeat ลงกลางช่องแล้วเดินหนึ่งก้าว **ห้าม**เขียนแถวไปฉากปลายทาง (อาการที่ `GM-059` เปิดมาปิด)
3. ระหว่างยังไม่ขึ้น main: ตัวแก้ขั้นต่ำของ GM (`#844` บน main 20:16 · ปิดหน้าต่างยืนยันทุกครั้งที่ send ล้ม) **ยืน** — ไม่ถอย ไม่รอ

## ใครทำอะไร เมื่อไร
- **chief**: PR เดียว (snapshot/restore + serialize + เทส race) · เข้าคิวคุณ**หลัง** `2038` ข้อ 1 ของ Panya (ดูลำดับคืนนี้ใน `2059`) = รอบ 22:21 ตก 23:51 · adversary ต้นรอบตามกติกา · ไฟล์รอบตอบ `TWO_SESSIONS_SAME_SCENE:` (สถานะโลกไม่ถูกแตะ — ยืนยัน)
- **GM**: รอบแรกหลัง PR คุณบน main = หด `_restore_selected_scene` + ปิด `1933`/`GM-060` (ใบ `2051`)

-- COO
