[ถึง: chief, COO, เจ้าของ, กะ1-A | ADDRESSEE: chief | cc: COO, Panya, กะ1-A | จาก: สาย GM รอบ `gm17278` ·
2026-08-31T02:28+07:00]
[อ้างอิง: `20260831_0152_PANYA-ORDER-LANE-GM-make-the-BT_GM-button-and-GMUI_BASIC-window-actually-work.md`
(consumed รอบนี้)]

# LANE-GM STATUS — BT_GM/GMUI_BASIC experiment fork สร้างแล้ว, `RE-164`/`GT-165`/`CORE-REQUEST-GM-043` เปิด

## สรุปสั้น

ตามคำสั่งเจ้าของ สร้าง `gm/bt_gm_probe.py` (14 frame variant + 3 suspect hypothesis stub, ดู
`docs/GM_LANE.md` รอบ `gm17278`) และเทส 22 ตัวที่ตรวจแค่ frame construction เปิด `RE-164`
(`CLIENT_RE_QUEUE.md`) กับ `GT-165` (`GAME_TEST_QUEUE.md`) เป็นคู่กัน — **`GT-165` ยัง 🔴 BLOCKED**
เพราะตรวจ `runtime.py` แล้วพบว่าจุดเรียกที่มีอยู่ยิงค่าคงที่เดียวตอนล็อกอินเท่านั้น ไม่มีทางยิง variant อื่น
ระหว่าง session ⇒ เปิด `CORE-REQUEST-GM-043` คู่กันขอจุดเสียบใหม่

## ผลแยกสองชั้น

**wire/DB:** ยังไม่มี — ไม่มีการส่งเฟรมจริงไปยังไคลเอนต์รอบนี้เลย
**client-observable:** ยังไม่มี — ไม่มีการคลิกจริง `BT_GM` ยังไม่รู้ว่า `GMUI_BASIC` เปิดหรือไม่จาก variant
ใด ทั้งสองชั้นรอ `CORE-REQUEST-GM-043` ลง แล้ว `GT-165` ถึงบูตได้

## nonclaim

สาย GM สร้าง probe และเขียนสเปกเท่านั้น — ไม่ได้คลิกเอง ไม่ได้เห็นผลด้วยตาตัวเอง ห้ามอ่านว่ารอบนี้พิสูจน์
(หรือหักล้าง) ว่าปุ่ม `BT_GM` ทำงาน — ยังไม่มีใครทดสอบจริงเลย

## ค้นแล้ว: เจอ/ไม่เจอ

ค้นชุดส่งมอบ RE: เจอ (registry tsv ทั้งสามไฟล์มีจริง, span_sha256 เดิมของ `state_wire.py` ยังใช้ได้ไม่ต้อง
verify ใหม่เพราะไม่มี field ใหม่) · ค้น fork ทดลอง GM state เดิม: ไม่เจอ (ไม่มี probe module มาก่อนรอบนี้)

## ของที่ค้างขอ chief

`CORE-REQUEST-GM-043` — จุดเรียกยิง state-vital variant ระหว่างเซสชัน (สองทางเลือกเสนอไว้ในใบ) เป็นตัวบล็อก
เดียวของ `GT-165` ตอนนี้

รายละเอียดเต็ม: `rounds/GM_20260831_0228_bt_gm_probe_fork_re164_gt165_core043_opened.md`

— สาย GM รอบ `gm17278`
