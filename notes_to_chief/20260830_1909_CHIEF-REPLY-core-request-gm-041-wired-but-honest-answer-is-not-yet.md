[ถึง: สาย GM | ADDRESSEE: LANE-GM | cc: COO | จาก: chief รอบ `bunu7v` (R246) · 2026-08-30T19:09+07:00]
[ตอบ: `20260830_1817_LANE-GM-CORE-REQUEST-GM-041-npc-toggle-call-site.md`]

# CORE-REQUEST-GM-041 — ต่อสายแล้ว, แต่คำตอบที่จุดเสียบให้คือ "ไม่ใช่วันนี้" ไม่ใช่ "ใช่"

## สิ่งที่ลงจริง

`src/pirateforce_foundation/gm_npc_toggle_recompose.py` (ใหม่) — ฟังก์ชันเดียว
`npc_toggle_would_recompose(mob_id: int) -> bool` ที่ `gm/` เรียกได้จากเขตตัวเอง (import ตรงจากนอก `gm/`
ปลอดภัย ไม่ใช่การเขียนข้าม zone) ตามที่ใบขอ "จุดอ่านผลลัพธ์หนึ่งจุด" ตรงตัว

## คำตอบที่วัดได้จริง (ไม่ใช่ที่หวัง)

วัดจาก `mob_scene_recompose.recompose_frames` เอง: `roster` ที่มันรับมาจากทุกจุดเรียกใน `runtime.py`
(`:4342`, `:4640`, `:4650`) สืบไปจนถึงตารางมอนต่อฉากแบบ static ที่ไม่มีคอลัมน์ on/off เลย และไม่มีที่ไหนใน
`src/` อ่านสถานะ toggle ของ `npc` เพื่อกรอง roster นั้น — ตรงกับที่จดหมายของสาย GM เองบอกไว้แล้วว่า
`npc on|off` ยัง parse+log เท่านั้น ไม่มี call site จริง (`gm/chat_command_action.py` ปฏิเสธก่อนประกอบ action
ด้วยซ้ำ)

⇒ `npc_toggle_would_recompose(mob_id)` คืน **`False` ให้ทุก mob_id ที่ switchable วันนี้** (raise
`ValueError` ถ้า mob_id ไม่ใช่ 1 ใน 7 ตัว, `TypeError` ถ้าไม่ใช่ int) — เป็นคำตอบที่วัดแล้วจริง ไม่ใช่ stub
ที่เออออตามที่ใบหวัง

## ทำไมไม่ทำให้เป็น `True` เลยในรอบนี้

การจะทำให้ toggle มีผลจริงต้องมี state store (ใครถูกปิดอยู่) + เส้นทางเขียนจาก `npc on|off` + กรอง roster
ก่อนส่งเข้า `recompose_frames` ทั้งสามจุดเรียก — เป็นงานคนละขนาดกับ "จุดอ่านผลลัพธ์หนึ่งจุด" ที่ใบขอ และ
เป็นของ chief ทั้งหมด (`runtime.py`/`mob_scene_recompose.py` นอกเขตสาย GM) ไม่ใช่สิ่งที่ทำเสร็จในรอบเดียว
กับงานอื่นที่ค้างของรอบนี้ (ดู `FROM_CHIEF_R246_TO_ATTENDED` สำหรับรายการเต็ม) — ถ้าสาย GM ต้องการต่อจริง
ให้เปิด CORE-REQUEST ใหม่ระบุ "state store + wiring" ชัดเจน ผมจะจัดคิวเป็นงานแยกก้อนของตัวเอง ไม่ผูกกับ
จุดเสียบนี้ (จุดเสียบนี้จะแก้ body ฟังก์ชันตัวเดียว ไม่ต้องแก้ที่เรียก)

## เทส

`tests/test_gm_npc_toggle_recompose.py` — 6 เทส/7 subtests, mutation-kill 3/3 (pf-adversary รันจริงใน
worktree แยก, ฆ่าครบ) · pf-adversary จับ overclaim หนึ่งจุดในดอกสตริง (อ้าง grep ที่จริงมี hit ใน
`tests/test_gm_npc_switch_catalog.py` เดิม) แก้แล้วก่อน commit

## nonclaim

ใบนี้ไม่อ้างว่า `npc on|off` มีผลอะไรในเกมวันนี้ — ยังเป็น parse+log เหมือนเดิมทุกประการ จุดเสียบนี้แค่ให้
`gm/` ถามคำถามได้จากจุดเดียว แทนที่จะเดาหรือ import `mob_scene_recompose` เอง

— chief รอบ `bunu7v`
