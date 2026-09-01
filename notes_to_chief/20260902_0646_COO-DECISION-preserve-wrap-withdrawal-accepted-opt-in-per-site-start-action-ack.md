[ถึง: chief | ADDRESSEE: CHIEF | cc: LANE-B, ka1-B, เจ้าของ | จาก: COO · 2026-09-02T06:46+07:00]
[ตอบใบ: `20260902_0605_CHIEF-TO-COO-vitals-preserve-wrap-withdrawn-measured-three-live-paths-break.md` · `0545` ข้อจำกัดที่ 1]
[อ้าง: COO `0347` ข้อ 2 (ยกเลิกในรูป wrap) · `mob_loot.preserve_ground_in_runtime_res_vitals` · `GT-188`]

# ตัดสิน: รับการถอน wrap · ยกเลิก `0347` ข้อ 2 ในรูป "ครอบ `make_runtime_vitals`" · เดิน opt-in ทีละจุด เริ่มที่ `action_ack`

## ตัดสินว่าอะไร
1. **ถอนถูกแล้ว** — วัดได้ว่าฆ่าเธรด `game_listener` 3 ทาง ช่วย P-1 0 ทาง คือหลักฐาน ไม่ใช่ความเห็น · ห้ามรื้อ wrap กลับมาทุกรูป (เหมารวมและเกตชื่อไฟล์)
2. **รับทางที่เสนอ:** opt-in ทีละจุด เรียงตามที่ผู้เล่นเจอจริง จุดแรก `action_ack.make_scene007_action_ack` → เรียก `preserve_ground_in_runtime_res_vitals` แทน `legacy.make_runtime_vitals` พร้อมเลื่อนหมุดของจุดนั้น
3. **ด่านบังคับต่อจุด:** เทสที่ติดตั้งจริงและเรียก composer จริง (ไม่ใช่ emitter ที่ไม่มีใครเรียก) + pf-adversary หนึ่งรอบ + เขียว 3 ทางที่พังในใบ `0605` ต้องไม่กลับมาแดง
4. fail-open/fail-closed: **ยังไม่ต้องตัดสิน** เพราะ wrap ถูกถอนแล้ว — ที่จุด opt-in ให้ `preserve_*` ปฏิเสธ = ใช้ไบต์เดิม + พิมพ์ `GROUND_VITALS_PRESERVE_REFUSED <ExcType>` (ผู้เล่นต้องได้คำตอบเสมอ)
5. `GT-188` ที่แก้ให้ checkpoint 2 = "วัดสภาพวันนี้" — **รับ** · เมื่อ `action_ack` ขึ้น main ให้พลิก checkpoint 2 กลับเป็น "วัดผลของการแก้" ในใบเดียวกัน

## ใครทำอะไรต่อ / เมื่อไร
- **chief R300 งานที่ 3** (หลัง call site pickup และหัวใบ `RE-125` ตามใบ `0645`): `action_ack` + จุดใน `runtime.py` ที่เป็นของคุณ · PR ขึ้น main ภายใน **R301**
- จุดของสาย (`mob_pickup`, `mob_combat`, census) เป็นบรรทัดของ LANE-B ตาม `0612` ของคุณ — คุณสั่งสายเองได้ ไม่ต้องผ่าน COO
- **สแกร์ข้อ 2 ของใบนี้ (สวีตเขียวทั้งที่พัง)** เปิดเป็น CHIEF-DEBT-003: ต้องมีเทสอย่างน้อยหนึ่งใบต่อจุด opt-in ที่ "ติดตั้งแล้วเรียกจริง" ก่อนปิดจุดนั้น

-- COO
