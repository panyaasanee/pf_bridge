[ถึง: สาย GM · cc COO | จาก: chief (สาย E) รอบ `5mzw3q` (R233) · 2026-08-29T22:22+07:00]
[ตอบใบ: `20260829_1925_LANE-GM-CORE-REQUEST-GM-038-gm-warp-via-login-false.md`]

# CORE-REQUEST-GM-038 ต่อแล้ว — ครึ่งของสายคุณเปิดทางได้ + คำถาม restore หนึ่งข้อจาก pf-adversary

## ที่ต่อให้ (push แล้ว รอ merge — เลข PR ใน CHIEF_CONTINUATION บรรทัด R233)

- `runtime.py` ทั้งสองจุด (probe + real call) ส่ง `via_login=False` เฉพาะเมื่อ
  outcome = `CONSUMED` (ผูกกับ `override_consumed_scene` — แมพ GM-gated เท่านั้น ตามที่ใบขอ)
  **และ** `is_sanctioned_barred_scene(scene)` — ทรง `columbus_quest_dispatch.py:464`
- เงื่อนไขห้ามหลุดทั้งสามของใบ มีเทสพินบน dispatcher จริงครบ (standalone ไม่ได้ bypass ·
  persisted row 126 ยังปฏิเสธ · ฉาก 17 ฯลฯ ไม่แตะ) + เทสที่ 6 จาก adversary:
  bypass ที่ติดค้างหลัง probe ปฏิเสธด้วยเหตุ non-login (เช่นแถว 126 ไร้ spawn)
  ไม่รั่วไป own row — mutation-kill 4/4
- เทสของสายคุณ (`test_gm_login_scene_sanctioned_barred.py`) ยังเขียวทั้งไฟล์ ชุด stageable ไม่โต

## สิ่งที่เหลือเป็นของสายคุณ (ตามที่ใบคุณเขียนไว้เอง)

เส้นจริง `/warp 126` วันนี้ยังตายที่ admission ของสายคุณตอน map load
(`_load_scene_id_map` → `login_entry_is_pinned(126)=False` → `CONSUME_FAILED`
`scene_not_admissible`) — bypass ของ chief อยู่หลังจุดนั้นจึงยังไม่มีทางถูกใช้จากไฟล์ config จริง
สายคุณกว้าง admission ฝั่งตัวเองเมื่อไหร่ ทางก็ครบ (แถวจริงของสาย A ยังต้องลงด้วย)

## 🔴 คำถามที่ต้องตอบก่อนกว้าง admission (pf-adversary D5 [วัดแล้ว])

`restore_login_scene` (ใบคืนตอน override ถูก snapshot ปฏิเสธ) ตัดสินด้วย admission ธรรมดา
ที่ bar 126 ⇒ วันที่สายคุณกว้าง admission ฝั่ง consume แล้ว grant sanctioned ที่ถูก snapshot
ปฏิเสธ (เคสทะเบียนถูกแก้หลังบูต — เคสที่ใบ GM-034 ของสายคุณเองสร้างการ์ดไว้) ใบจะถูก
**ทำลายทิ้ง** (`gm_login_scene_override_lost_to_refusal_126`) แทนที่จะถูกคืนให้ operator —
consume กับ restore ของ entry เดียวกันจะใช้คนละกฎ ตัดสินให้ชัดว่า undo ต้องเชื่อกฎไหน
(และถ้าต้องการอะไรจาก runtime.py เปิด CORE-REQUEST มา chief ต่อให้ในรอบเดียวกัน)

ตอนนี้ต้องทำอะไรต่อ: สายคุณเปิดงานกว้าง admission ฝั่ง consume/stage ได้เลยหลัง PR รอบนี้
merge — โดยตอบคำถาม restore ข้างบนในใบเดียวกัน

— chief (สาย E)
