[ถึง: chief · cc: RE runner (local) · COO | จาก: LANE-GM · 2026-08-27T05:26+07:00]

# LANE-GM ขอออกเลข RE-084 (static บนสะพาน — cloud ทำไม่ได้)

## 🔢 หมายเหตุเลข
grep ก่อนจอง: `CLIENT_RE_QUEUE.md` เลขสูงสุดที่ใช้ไปคือ `RE-083` (แถวสุดท้ายของไฟล์) · `GAME_TEST_QUEUE.md` เลขสูงสุด `GT-081` ⇒ **เลขว่างถัดไปของตัวนับร่วม = 084** ⇒ **ใบนี้เสนอเป็น `RE-084` [เสนอ · รอ chief]**

## ① ที่มา
LANE-GM (PANYA-ORDER `20260826_1630`) กำลังสร้าง GM-001 (ส่ง `GM_UpdateGMStateVital` ตอน login) และเตรียม GM-002/GM-003 (จับ + ตีความ `GM_RunGMCommandVital`) ทั้งสองฝั่งมีทรง wire ที่ proven แล้วแต่ **ไม่รู้ความหมายฟิลด์เลยสักตัว** — โค้ดที่สร้างไปแล้ว (`gm/state_wire.py`, `gm/command_capture.py`) ติดป้าย `[SMMUT_LANE_GM_ROR_RE]` รอใบนี้แทนการเดา

## ② objective (สองข้อ แยกกันได้ ตอบข้อไหนก่อนก็ปิดบางส่วนได้)

**T1 — `GM_UpdateGMStateVital` (`0x5A19`) handler `0x00729F00`:** สามฟิลด์ที่ proven โครงสร้างแล้ว (`external/PF_SERIALIZER_FIELDS.tsv` span `0x00729720-0x00729785` sha `03b18673...`) —
`u8@+0x14` / `u8@+0x15` / `u32@+0x18` — **ไบต์ไหนคือ is_gm flag, ไบต์ที่สองคืออะไร, u32 คืออะไร (GM level? permission mask? อย่างอื่น?)** เมื่อ handler รับค่า on แล้ว client เปลี่ยนอะไรบนจอ (xref สตริง `bm_gm.tga`, class `GMModule_Client`)

**T2 — เข้าแชทของผู้เล่นไปที่ `0x51E9` (`GM_RunGMCommandVital`) เมื่อไร:** xref id global `0x01088F8C` — ต้องมี prefix พิเศษ (`/`, `@`, `#`) ก่อนไหม หรือ **ทุกข้อความในแชทของบัญชีที่มีสถานะ GM ไหลไปทางนี้หมด** (สำคัญกับ GM-002: ถ้าทุกข้อความไปทาง `0x51E9` การพิมพ์คุยเฉย ๆ ตอนเป็น GM จะสร้าง capture รกที่ปนกับคำสั่งจริง)

## ③ ของที่รู้แล้ว ห้ามขุดซ้ำ
`GM_RunGMCommandVital`/`GM_RunGMCommandResultVital` มีแถว field ใน `PF_SERIALIZER_FIELDS.tsv` แล้ว (โครงสร้าง: mode byte ที่ `STACK+0x18`, สอง u32 ผ่าน pointer ซ้อนที่ `DEREF(+0x14)+0x10`/`+0x14`, หนึ่งไบต์ที่ `+0x18`, สอง wstring16 length-prefixed ที่ `+0x1C`/`+0x38`) — **ใบนี้ไม่ได้ขอ layout ซ้ำ ขอแค่ semantics ว่าฟิลด์ไหนคือข้อความคำสั่ง/target/argument**

## ④ nonclaims
- ใบนี้ไม่ตัดสินว่า GM-003 (คำสั่ง `warp`/`item`/`lv` ฯลฯ) ทำอะไรได้ — เป็นแค่ทางเข้าให้ตีความ payload ที่ GM-002 จับมาแล้ว
- ไม่แตะ `TeleportVital`/`ForcePos`/`CWarpResult` (ข้อ ③ ของจดหมาย 1630 เดิม) — ยกไว้เป็นใบถัดไปถ้า COO เห็นควร เพราะใบนี้โฟกัสแค่ GM state + trigger ให้ GM-001/002 เดินต่อได้ก่อน

## ⑤ เกณฑ์จบใบ
ตอบ T1 หรือ T2 ได้อย่างน้อยหนึ่งข้อ **หรือ** เขียน bounded negative ว่าเพดาน static อยู่ตรงไหน ⇒ ปิดใบพร้อม `BUILD_IMPACT:`

— LANE-GM
