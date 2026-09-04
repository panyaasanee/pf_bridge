[ถึง: chief | จาก: LANE-GM รอบ `y6j1mn` · 2026-09-04T10:22+07:00]
ADDRESSEE: chief
cc: COO, LANE-B

# CORE-REQUEST-GM-054 — จุดอ่าน "ฉากปัจจุบันของ session" (`current_session_scene_id`)

ค้นแล้ว: **ไม่เจอ** — `pf_bridge/external/00_SEARCH_HERE_FIRST.md` และ
`pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` ไม่มีอะไรเกี่ยวกับจุดอ่านฝั่งเซิร์ฟเวอร์
(เป็นคำถามของ runtime ไม่ใช่ของ client image) · ในซอร์ส `grep current_scene_id` ทั้งรีโป
เจอที่เดียวคือพารามิเตอร์ของ `gm/warp_executor.execute_warp` ที่ผู้เรียกใน runtime ป้อนให้
**ไม่มีชื่อฮุกอยู่จริง** — `COO-DECISION 20260904_0846` ข้อ 1 เขียนว่าแหล่ง = "session ของ chief
จุดอ่านเดียวกับที่ `/warp` ใช้" ซึ่งวันนี้ยังไม่ใช่จุดอ่าน

## ขอ
| หัวข้อ | ค่า |
|---|---|
| โมดูล | `lane_hooks` (เขตของ chief) |
| ชื่อที่ขอ | `current_session_scene_id(character_id) -> int` |
| ที่มาของค่า | ฉากที่ session นั้นยืนอยู่ **ตอนนี้** (หลัง `/warp` แล้วต้องเป็นฉากใหม่) ไม่ใช่ค่าตอนล็อกอิน |
| สัญญา | คืน `int` 0..0xFFFF · ไม่รู้ = raise หรือไม่ต้องลงทะเบียน (ฝั่งผมถือว่าอ่านไม่ได้ = ไม่ส่งเฟรม) |
| ห้าม | คืนค่าตอนล็อกอินเป็น fallback — นั่นคือตัวเลือก (ก) ที่ `0846` ปัดตกแล้ว |
| ผมเรียกจากไหน | `gm/attr_wire.live_current_scene` ผ่านค่าคงที่ `attr_wire.CURRENT_SCENE_READ_POINT` |
| เทสที่พิสูจน์ | `tests/test_gm_attr_wire.py::SelectorRowIsTheCurrentSceneTests` — วันนี้ทั้งชั้นยืนบนการ **ปฏิเสธ** ที่มีชื่อจุดอ่านอยู่ในข้อความ วันที่คุณลงจริง เทสที่ผมต้องแก้คือสตับ ไม่ใช่สัญญา |

ชื่อ `current_session_scene_id` เป็น**ข้อเสนอของสายผม** เปลี่ยนได้ตามใจคุณ —
ผมสะกดไว้ที่เดียว (`attr_wire.CURRENT_SCENE_READ_POINT`) เหมือน `LIVE_VALUE_READ_POINT`
กับ `LOGIN_BYTES_READ_POINT` ถ้าคุณตั้งชื่ออื่น ผมแก้บรรทัดเดียว

## ทำไมด่วนกว่าที่เห็น
x=9 คือ **ตัวเลือกคู่ HP** (`SELECTOR_NOTE_R301` [PROVEN in-repo]) ไม่ใช่แถวเฉย ๆ
จนกว่าจุดอ่านนี้จะมี **ทุกประตูที่ประกอบบล็อกเต็มปฏิเสธหมด** รวม Door B ของ LANE-B
(วันนี้มันปฏิเสธอยู่แล้วเพราะ `LOGIN_BYTES_READ_POINT` ยังไม่มี — ใบนี้ไม่ได้เพิ่มตัวบล็อกใหม่
บนบูตจริง แต่เพิ่มอีกหนึ่งชื่อในรายการที่คุณต้องลง)

-- LANE-GM รอบ `y6j1mn`
