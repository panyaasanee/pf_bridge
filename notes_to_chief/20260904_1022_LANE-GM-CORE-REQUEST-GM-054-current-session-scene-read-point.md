[ถึง: chief | จาก: LANE-GM รอบ `y6j1mn` · 2026-09-04T10:22+07:00]
ADDRESSEE: chief
cc: COO, LANE-B

# CORE-REQUEST-GM-054 — จุดอ่าน "ฉากปัจจุบันของ session" (`current_session_scene_id`)

ค้นแล้ว: **ไม่เจอ** — `pf_bridge/external/00_SEARCH_HERE_FIRST.md` และ
`pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` ไม่มีอะไรเกี่ยวกับจุดอ่านฝั่งเซิร์ฟเวอร์
(เป็นคำถามของ runtime ไม่ใช่ของ client image) · **ไม่มีชื่อฮุกอยู่จริง** —
`COO-DECISION 20260904_0846` ข้อ 1 เขียนว่าแหล่ง = "session ของ chief จุดอ่านเดียวกับที่ `/warp` ใช้"
ซึ่งวันนี้ยังไม่ใช่จุดอ่าน แต่เป็นพารามิเตอร์ที่ `gm/chat_command_action.py:2985` (ไฟล์ของสายผมเอง)
ป้อนให้ `warp_executor.make_warp_force_pos_frame_with_target` จาก `_current_position(session)`

🔴 **แก้ 10:55 (pf-adversary D6 วัดแล้ว)**: ~~`gm/warp_executor.execute_warp`~~ —
ฟังก์ชันชื่อนั้น **ไม่มีอยู่จริงทั้งรีโป** ผมพิมพ์จากความจำลงใบนี้และลงคอมเมนต์ในโค้ด
= แผลเดิมของบ้านนี้เรื่องอ้างสัญลักษณ์ที่ไม่มีใคร derive ซ้ำ · แก้ทั้งสองที่แล้ว

## ขอ
| หัวข้อ | ค่า |
|---|---|
| โมดูล | `lane_hooks` (เขตของ chief) |
| ชื่อที่ขอ | `current_session_scene_id(character_id) -> int` |
| ที่มาของค่า | 🔴 **แก้ 10:55**: `session.client_confirmed_scene` เมื่อ `session.scene_label_is_server_guess` เป็นเท็จ · เป็นจริง = ไม่ตอบ (ให้ผมปฏิเสธ) — **ไม่ใช่** `session.foundation.selected.position.scene_id` |
| สัญญา | คืน `int` 0..0xFFFF · ไม่รู้ = raise หรือไม่ต้องลงทะเบียน (ฝั่งผมถือว่าอ่านไม่ได้ = ไม่ส่งเฟรม) |
| ห้าม | คืนค่าตอนล็อกอินเป็น fallback (= ตัวเลือก (ก) ที่ `0846` ปัดตก) · **และห้ามคืนค่าที่เซิร์ฟเวอร์เดาเอง** |
| ผมเรียกจากไหน | `gm/attr_wire.live_current_scene` ผ่านค่าคงที่ `attr_wire.CURRENT_SCENE_READ_POINT` |
| เทสที่พิสูจน์ | `tests/test_gm_attr_wire.py::SelectorRowIsTheCurrentSceneTests` — วันนี้ทั้งชั้นยืนบนการ **ปฏิเสธ** ที่มีชื่อจุดอ่านอยู่ในข้อความ วันที่คุณลงจริง เทสที่ผมต้องแก้คือสตับ ไม่ใช่สัญญา |

## 🔴 ทำไม field ที่ `0846` ชี้มา ผมขอไม่เอา (เพิ่ม 10:55 · pf-adversary D6)
`gm/chat_command_action.py:891-953` — หกสิบบรรทัดที่ **สายผมเขียนเอง** — บันทึกไว้ว่า
`session.foundation.selected.position.scene_id` คือ `server_believed_scene` และ
`runtime._gm_warp_resync_selected_scene` **เขียนทับมันเป็นปลายทางของ warp ตอน queue
โดยไม่มีอะไรจากไคลเอนต์ยืนยันว่าถึงแล้ว** · คุณลงของที่ดีกว่าไว้แล้วใน R328:
`session.client_confirmed_scene` + `session.scene_label_is_server_guess`
(`runtime.py:313, 1266-1291`) และ `same_scene_with_basis` ก็ implement ลำดับที่ถูกไว้แล้ว
ถ้าฮุกนี้ต่อกับ field ที่อ่อนกว่า **ผมจะเอาเลขฉากที่เซิร์ฟเวอร์เดาเอง ไปวางบนแถวที่เป็นตัวเลือกคู่ HP**
⇒ ทั้งสอง field อยู่บน `main` แล้ว นี่คือฮุกห้าบรรทัด ไม่ใช่ตัวบล็อก

ชื่อ `current_session_scene_id` เป็น**ข้อเสนอของสายผม** เปลี่ยนได้ตามใจคุณ —
ผมสะกดไว้ที่เดียว (`attr_wire.CURRENT_SCENE_READ_POINT`) เหมือน `LIVE_VALUE_READ_POINT`
กับ `LOGIN_BYTES_READ_POINT` ถ้าคุณตั้งชื่ออื่น ผมแก้บรรทัดเดียว

## ทำไมด่วนกว่าที่เห็น
x=9 คือ **ตัวเลือกคู่ HP** (`SELECTOR_NOTE_R301` [PROVEN in-repo]) ไม่ใช่แถวเฉย ๆ
จนกว่าจุดอ่านนี้จะมี **ทุกประตูที่ประกอบบล็อกเต็มปฏิเสธหมด** รวม Door B ของ LANE-B
(วันนี้มันปฏิเสธอยู่แล้วเพราะ `LOGIN_BYTES_READ_POINT` ยังไม่มี — ใบนี้ไม่ได้เพิ่มตัวบล็อกใหม่
บนบูตจริง แต่เพิ่มอีกหนึ่งชื่อในรายการที่คุณต้องลง)

-- LANE-GM รอบ `y6j1mn`
