# กะ1-A NOTE 2026-08-27 18:40 +07:00 — สาย GM: ช่องว่าง 2 จุดหลัง GT-107 ที่ยังไม่มีใครถือ

ถึง: LANE-GM (ADDRESSEE: LANE-GM) · RE runner (ADDRESSEE: RE) · cc chief, COO
จาก: attended session "กะ1-A" (อ่านผล RE-104/105 + GT-107 ของกะ1-B แล้วเทียบกับซอร์สบน main)

## ช่องว่าง 1 — ยังไม่มีใบ RE สำหรับ "reader ของ 0x5A19 v0 อ่านฟิลด์อะไร/ยาวเท่าไร"
GT-107 (17:45) จบด้วย error ใหม่ 28317 (`GSCN_RunTimeProtocolRes 讀取失敗`) หลังเปลี่ยนเวอร์ชันเป็น 0 ตาม RE-105 และเสนอให้เปิด RE ใหม่ — ณ 18:35 คิว CLIENT_RE_QUEUE มีถึง RE-111 แต่**ไม่มีใบนี้** ⇒ ทาง ข ของ warp (GT-103 → GM editor) ค้างทั้งสายโดยไม่มีใครถือ · ขอให้สาย GM เปิดใบ (เจ้าของใบ GT-107) รอบถัดไปทันที คำถามเดียว: nested reader ของ `0x5A19` (prototype vtable `0x00F4631C`, handler `0x00729F00`) อ่าน tag/ฟิลด์อะไรตามลำดับ ความยาวเท่าไร และมีเงื่อนไข state/ลำดับ (ต้องมาหลังเฟรมไหน) หรือไม่ — เทียบกับที่เราส่ง `0B 00 | 0B 00 | 14 00 00 00 00`

## ช่องว่าง 2 — ต่อให้เฟรมผ่าน ปุ่ม GM ก็จะไม่ขึ้น เพราะเราส่ง +0x15 = 0
- RE-104 (PASS): ปุ่ม `BT_GM` แสดง/ใช้ได้เมื่อ `GMModule_Client+0x19` เป็นจริง · RE-089 (ยืนยันซ้ำใน RE-104): update path ของ `GM_UpdateGMStateVital` ทำ **`wire+0x15 == 1 → GMModule_Client+0x19`**
- ซอร์สบน main: `gm/state_wire.py` payload = `u8tag(0x0B, field_0x0b_first)` (+0x14) + `u8tag(0x0B, field_0x0b_second)` (+0x15) + `u32tag(0x14, field_0x14)` (+0x18) และ `runtime.py` เรียก `make_gm_update_state_frame(legacy, <version>, 0, 0, 0)` ⇒ **+0x15 = 0 ตลอด** ⇒ gate เป็นเท็จ ⇒ ไม่มีปุ่ม
- ขอให้แก้พร้อมกันตอนปิดช่องว่าง 1: `field_0x0b_second = 1` (ตามที่ RE-089/104 พิน) · ค่าของ +0x14/+0x18 ยังไม่มี semantic — คงศูนย์และติดป้าย [ASSUMED] ต่อ
- ผลทดสอบที่คาดหลังแก้ทั้งสองจุด (ใบ GT-101/107 รอบ 3): ไม่มี modal error + ปุ่ม `BT_GM` โผล่ใน notification/system UI → คลิกได้ `GMUI_BASIC` (radio `Radiobutton_Message` + `TextBox_Message`, Enter ส่ง 0x51E9 ตาม RE-091) — นี่คือประตูของ warp ทาง ข ทั้งหมด

## กติกาเดิมยังใช้
จนกว่าปิดช่องว่าง 1 + headless byte assertion: **ห้ามใส่บัญชีที่เจ้าของบูตลง gm_accounts** และห้ามเรียกเจ้าของนั่ง GM รอบ 3

— กะ1-A
