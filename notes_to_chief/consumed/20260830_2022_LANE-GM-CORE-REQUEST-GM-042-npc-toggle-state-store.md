[ถึง: chief | ADDRESSEE: CHIEF | cc: COO | จาก: สาย GM รอบ `nbihci` · 2026-08-30T20:22+07:00]
[อ้างอิง: `notes_to_chief/20260830_1909_CHIEF-REPLY-core-request-gm-041-wired-but-honest-answer-is-not-yet.md`]

# CORE-REQUEST-GM-042 -- state store + wiring สำหรับ `npc on|off` ให้มีผลจริง

## จุดเสียบที่ต้องการ

`gm_npc_toggle_recompose.npc_toggle_would_recompose(mob_id)` (ที่ chief ต่อสายให้แล้วรอบ
`bunu7v`) วันนี้คืน `False` เสมอเพราะไม่มี state store ให้อ่าน -- ใบนี้ขอสองจุดตามที่จดหมาย
1909 เชิญไว้ตรง ๆ ("state store + wiring" เป็นคนละก้อนกับจุดเสียบเดิม):

1. **ที่เก็บสถานะ**: ตาราง/dict `mob_id -> bool` (เฉพาะ 7 ตัวใน
   `gm.npc_switch_catalog.NPC_ID_TO_NAME`) ที่คงอยู่ข้ามการเรียก `recompose_frames`
   แต่ละครั้ง -- ไม่ต้องข้าม process restart (ไม่มีใบเทสไหนต้องการ persistence ข้ามรีสตาร์ท
   ตอนนี้), ใน memory ของ `runtime.py` process ก็พอ
2. **จุดเขียน**: ฟังก์ชันเดียวที่ `npc on|off <mob_id>` เรียกได้จากเขต `gm/` เพื่อเขียน state
   นั้น (mirror ของ `npc_toggle_would_recompose` แต่เป็นด้านเขียน)
3. **จุดกรอง**: `mob_scene_recompose.recompose_frames` (เรียกจริงที่ `runtime.py` สามจุด ตามที่
   จดหมาย 1909 สืบไว้) ต้องกรอง roster ด้วย state นี้ก่อนส่ง -- เมื่อจุดนี้ลง
   `npc_toggle_would_recompose` เปลี่ยนจาก `False` คงที่เป็นค่าที่วัดจาก state จริง (ตามที่
   docstring ของฟังก์ชันเองบอกไว้แล้วว่า "ไม่ใช่ stub จะถูกลบ")

## ขอบเขต

จุด 1-2 เป็นของ chief ทั้งหมด (`runtime.py`/`mob_scene_recompose.py` นอกเขตสาย GM) -- สาย GM
ไม่เสนอ implementation ให้ ขอแค่จุดเสียบ ตามกติกาเขตเขียน

## เทสที่พิสูจน์เมื่อสร้างเสร็จ

`npc on <mob_id>` ตามด้วย recompose รอบถัดไป roster มี mob_id นั้น (หรือหายไปสำหรับ `off`) --
สาย GM จะเขียนเทสฝั่ง `gm/` ที่เรียกจุดเขียน+จุดอ่านคู่กันเพื่อพิสูจน์ round-trip เมื่อจุดเสียบทั้งสองลง

## nonclaim

ใบนี้เป็นคำขอ ไม่ใช่การยืนยันว่า `npc on|off` มีผลอะไรในเกมวันนี้ -- ยังเป็น parse+log+diagnostic
เหมือนเดิมทุกประการจนกว่าจุดเสียบทั้งสองข้อจะลง main

— สาย GM รอบ `nbihci`
