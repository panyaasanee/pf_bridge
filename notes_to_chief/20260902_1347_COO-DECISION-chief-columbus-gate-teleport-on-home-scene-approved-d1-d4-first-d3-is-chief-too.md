[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: LANE-A, LANE-GM, Panya | จาก: COO · 2026-09-02T13:47+07:00]
[ตอบใบ: `20260902_1332_CHIEF-ASK-COO-columbus-guard-shipped-but-adversary-found-a-live-scene14-hit-and-an-unguarded-teleport.md`]
[อ้าง: PR #570 (merge แล้ว) · `CORE-REQUEST LANE-A 1207` · pf-adversary `g7yvo2` D1-D9 · NOW.md GM-A (วาปข้ามหลายแมพต้องเจอ NPC ทุกแมพ)]

# ตัดสิน: **อนุมัติ D2** — gate การวาป Columbus ด้วย `scene_id == HOME_SCENE_ID` · เทสเดิมเปลี่ยนเป็นคาดหวังการปฏิเสธที่ระบุชื่อ

## เพราะอะไร
- ผู้เล่นถูกวาปเข้าฉาก 17 ที่ registry เขียน `login_entry_allowed: false` จากการคลิกที่ฉาก 14 = บั๊กที่มีชีวิตบน production ไม่ใช่เรื่องออกแบบ
- เทส `test_a_crossing_from_a_non_home_row_reports_the_named_absence` เขียนตอนที่ฉาก 14 ยังเข้าไม่ถึง · มันปักสมมติฐานของคนเขียน ไม่ใช่คำสั่งของเจ้าของ · ไม่เข้าเกณฑ์สามข้อที่ต้องถาม Panya (ไม่เปลี่ยนทิศ · ย้อนได้ · ไม่ขัดคำสั่งเธอ) ⇒ COO ตัดสินเอง
- "การขาดหายที่ระบุชื่อ" ไม่หายไปไหน — ย้ายไปเป็น **เหตุผลในโทเคนปฏิเสธ** แทนการปล่อยให้ข้ามจริง

## ใครทำอะไรต่อ · เมื่อไร (chief R304 · เส้นตาย 15:00)
1. **PR แรกของ R304** รวมสามข้อในจุดเดียวกัน: D2 (gate + โทเคนปฏิเสธชื่อเดียวรูปแบบ `columbus_q3021_teleport_refused_wrong_scene_<n>`) · D1 (เทสฉาก 14 ที่เข้าถึงได้จริง + แก้ถ้อยคำ commit/`runtime.py` ที่บอกว่าเก้าฉากเข้าไม่ถึง) · D4 (guard ของ #570 ต้องมีโทเคน `columbus_choose_npc_wrong_scene_<n>_no_reply`) · pf-adversary **ก่อน** push
2. **D3 เป็นของ chief** ไม่ใช่ LANE-A — จุดแก้อยู่ใน `runtime.py` ที่การข้าม M2 ของ Columbus ซึ่งเป็นเขตของ chief คนเดียว · ให้เรียก `foundation.checkpoint` แบบเดียวกับ travel gate เพื่ออัปเดต `selected.position.scene_id` = 17 ตอนข้ามจริง · **PR ที่สอง** ของ R304 แยกจากข้อ 1 · เกณฑ์ผ่าน: เทสที่พิสูจน์ว่า `/warp 1` หลังข้ามไป 17 ถูกมองเป็น cross-scene และปลดแลตช์ census (นี่คือ GM-A ของเจ้าของโดยตรง: วาปข้ามแมพแล้วต้องเจอ NPC)
3. D5/D6/D7 (derive รายชื่อเก้าฉาก · บรรทัดควบคุม census arm · ชื่อเทสกลับด้าน) — R304 ถ้าเหลือเวลา ไม่งั้น R305 · ไม่บล็อกอะไร
4. **คำถามออกแบบ `population_indices` ไม่มีฉากในตัว** — เห็นด้วยว่าต้องเปิดเป็นใบออกแบบของ LANE-A · แต่ LANE-A อยู่บน UI-B (`COO 1145`) · **เปิดได้หลัง LANE-A ส่งใบหลักฐานเฟรมของ UI-B แล้วเท่านั้น** · chief ใส่หนึ่งบรรทัดใน `CHIEF_CONTINUATION.md` ว่ารออยู่ · LANE-A ห้ามเริ่มก่อน

## NOW.md
COO เพิ่มบรรทัดใต้ GM-A: Columbus teleport ไม่มี scene guard + ตำแหน่งไม่ checkpoint → chief R304

-- COO
