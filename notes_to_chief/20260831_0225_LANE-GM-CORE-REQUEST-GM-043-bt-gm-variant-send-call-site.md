[ถึง: chief | ADDRESSEE: chief | cc: COO, Panya | จาก: สาย GM รอบ `gm17278` · 2026-08-31T02:25+07:00]
[อ้างอิง: `20260831_0152_PANYA-ORDER-LANE-GM-make-the-BT_GM-button-and-GMUI_BASIC-window-actually-work.md`
(ใบสั่งเจ้าของ) · เปิดคู่กับ `RE-164`/`GT-165` ใน `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`]

# CORE-REQUEST-GM-043 — จุดเรียกให้ยิง `GM_UpdateGMStateVital` variant ได้ตามสั่งระหว่างเซสชัน ไม่ใช่แค่ค่าคงที่ตอนล็อกอิน

## ทำไมรอบนี้

รอบนี้สร้าง `gm/bt_gm_probe.py` (14 variant ของเฟรม `GM_UpdateGMStateVital` ทีละฟิลด์ ดู `RE-164`) เพื่อให้
กะ1-A คลิก `BT_GM` หลังแต่ละ variant ตามใบสั่งเจ้าของ (ทำ fork ทดลองแบบ `PF_ADHOC_ATTR_PROBE` แทนอ่าน
disassembly ต่อ) แต่ตรวจ `runtime.py` แล้วพบว่า **จุดเรียกที่มีอยู่ตอนนี้ยิงค่าคงที่เดียว (`0, 1, 0`) ครั้งเดียว
ตอนล็อกอินสำเร็จของบัญชี GM เท่านั้น** (`runtime.py:6429-6438`, คอมเมนต์ที่จุดเรียกเองระบุ "ALWAYS ON, no
scenario flag") — ไม่มีทางยิง variant อื่นระหว่างเซสชันเดียวกันได้เลยตอนนี้ ถ้าไม่มีจุดเสียบใหม่ `GT-165` ทำ
ไม่ได้ (ต้อง relogin ใหม่ทุกครั้งที่จะลอง variant ถัดไป ซึ่งเสี่ยง confound เรื่อง session/connection-context
— ตรงกับผู้ต้องสงสัย ① เองพอดี)

## สิ่งที่วัดสด รอบนี้ (source บน `origin/main` ปัจจุบัน)

- `runtime.py:40-41` import `state_wire`/`make_gm_update_state_frame` อยู่แล้ว
- `runtime.py:6424-6438`: เงื่อนไขเดียวคือ `is_gm and VERSION_CONFIRMED is not None` แล้วยิงค่า `(0, 1, 0)`
  ตายตัว — ไม่มีพารามิเตอร์ ไม่มีทางสั่งค่าอื่นจากภายนอกฟังก์ชันนี้
- `gm/bt_gm_probe.py` (ใหม่รอบนี้) มี `iter_state_vital_bit_variants()`/`build_variant_frame()` พร้อมใช้
  แล้วในเขต `gm/` — สิ่งที่ขาดคือจุดที่ `runtime.py` เรียกมันได้ระหว่าง session ไม่ใช่แค่ตอนล็อกอิน

## คำขอ

จุดเสียบหนึ่งจุด (รูปแบบเดียวกับที่ `CORE-REQUEST-011`/`-041` ให้ `warp`/`npc`): ทางใดทางหนึ่งที่ chief เลือก
เอง —
1. **ทางเลือก A (แนะนำ เสี่ยงต่ำสุด):** ต่อกับ GM chat-command dispatcher ที่มีอยู่แล้ว (`gm/dispatch.py`)
   เป็นคำสั่งใหม่ เช่น `gmstate <variant_id>` ที่อ่านชื่อ variant จาก `bt_gm_probe.iter_state_vital_bit_variants()`
   แล้วยิงเฟรมนั้นไปยัง connection ปัจจุบันทันที (ไม่ต้อง relogin, ไม่กระทบ path ตอนล็อกอินเดิม)
2. **ทางเลือก B:** debug/opt-in scenario flag (แบบเดียวกับ `--scene-load-scenario` ที่ `GT-158` ใช้) ที่รับ
   ชื่อ variant จาก command line แล้วยิงหลัง login แทนค่าคงที่ `(0,1,0)` เดิม

ทั้งสองทางไม่แตะพฤติกรรมเดิมของบัญชี non-GM หรือ path ล็อกอินปกติ — เพิ่มทางเลือกเท่านั้น chief เป็นคนตัดสิน
ว่าทางไหนเสี่ยงน้อยกว่าตามเกณฑ์ของตัวเอง

## ทำไมยังไม่ทำเอง

`runtime.py` และ `gm/dispatch.py`'s wiring เข้ากับ `runtime.py` (ไม่ใช่ตัว `dispatch.py` เอง) อยู่นอกเขต
เขียนที่ปลอดภัยของสายนี้ตามกฎบ้าน (`runtime.py` ห้ามแตะโดยตรง) — ฝั่งนี้ทำได้แค่ระบุจุดที่ขาดและเสนอจุดเสียบ

## nonclaim

ใบนี้เป็นคำขอจุดเสียบ ไม่ใช่หลักฐานว่า variant ใดทำให้ `GMUI_BASIC` เปิด — `bt_gm_probe.py` ยังไม่เคยถูกส่ง
ไปยังไคลเอนต์จริงเลยสักครั้งจนถึงตอนนี้ `GT-165` ยังคง BLOCKED จนกว่าจุดเสียบนี้จะลง ไม่มีการเปิด client
ไม่มีการวัดกับไคลเอนต์จริงในใบนี้ ทั้งหมดวัดจาก grep/read บนซอร์สที่ commit แล้วบน `origin/main`

— สาย GM รอบ `gm17278`
