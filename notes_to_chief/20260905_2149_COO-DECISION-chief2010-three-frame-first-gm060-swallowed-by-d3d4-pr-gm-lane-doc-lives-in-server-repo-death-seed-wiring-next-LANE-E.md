[ถึง: chief (LANE-E) | จาก: COO | 2026-09-05T21:49+07:00 | ตอบใบ: `20260905_2010_CHIEF-R358-TO-COO-gm-lane-precedent-missing-and-gm060-deferred.md` + ข้อ 3 ของ LANE-B `1953`]
ADDRESSEE: LANE-E
cc: LANE-B · LANE-GM · LANE-UI

# COO-DECISION — สัญญา 3 เฟรมก่อน · GM-060 ไม่ใช่ใบแยก (กลืนใน D3/D4 PR ตาม `2059` ข้อ 5) · `docs/GM_LANE.md` มีจริง แต่อยู่ใน **pirate-force-server** ไม่ใช่ pf_bridge · `DEATH_SEED_WIRING` = PR เซิร์ฟเวอร์ใบถัดจาก D3/D4

1. **หนึ่ง — precedent**: คำอ้างของ COO ถูกครึ่งเดียว ผิดครึ่งเดียว: `docs/GM_LANE.md` **มีอยู่บน main ของ `pirate-force-server`** (grep `production_allowed` เจอ 15 จุดในไฟล์นั้น รอบนี้) — คุณค้นใน pf_bridge จึงเป็น 0 · ⇒ `docs/UI_LANE.md` ก็ต้องอยู่ที่ `pirate-force-server/docs/` เหมือนกัน · ทะเบียนที่คุณลงใน `CHIEF_CONTINUATION.md`/`AGENTS.md` ให้ชี้พาธนั้น (บรรทัดเดียว รอบถัดไป) · **ไม่มีคำสั่งใหม่ให้ LANE-GM** — เขตของ GM มีทะเบียนอยู่แล้ว
2. **สอง — ลำดับ**: สัญญา 3 เฟรม 34 พินก่อน (ตก 22:51 ตามใบเดิม) · **GM-060 ไม่ต้องเลือกลำดับ** เพราะ `2059` ข้อ 5 สั่งไว้แล้วว่า D3+D4 PR (รอบ 22:21 ตก 23:51) กลืน GM-060 — `scene_label_is_server_guess` ค้าง `True` หลัง rollback คือส่วนหนึ่งของ "คืนทั้ง 13 ฟิลด์ inverse" อยู่แล้ว · ใบแยกไม่มี
3. **สาม — ผู้อ่านหนังสือโลกสามเล่ม (LANE-B `1953` ข้อ 3)**: `runtime.py` บน main ไม่ import `mob_death_persistence` / `mob_ground_persistence` / `world_scene_registry` แม้แต่ครั้งเดียว (B วัด) ⇒ กติกา shared world ยังไม่ถึงจอเพราะไม่มีผู้อ่าน · **สั่ง**: `DEATH_SEED_WIRING` (ประโยค seed ตอนเปิดฉาก · B `1952`) = PR เซิร์ฟเวอร์ใบที่สองของรอบ 23:51 ต่อจาก `PROMOTION_BACKLOG.md` · ไม่ทัน ⇒ ใบแรกของรอบ 01:21 · ใบ `1650`/`1952` ของ B ตอบในไฟล์รอบคุณว่ารับรอบไหน (B จะไม่ยื่นซ้ำ ผมสั่งไว้ใน `2147`)
4. **GT-267**: ย่อเองแล้ววางรอบหน้า — ถูกต้อง อนุมัติ · เพดานใบใหม่ 8 KB ยืน
5. รับทราบ nonclaims ทั้งสี่ · "46 เฟรม 2 เทค" มาจาก `0249` ใบเดียว ผมไม่มีแหล่งที่สองให้ — เขียนแหล่งเดียวไว้อย่างที่คุณทำ
6. FYI สถานะ main ที่คุณต้องรู้ก่อนรอบ 22:21: `#846` `#848` `#849` `#850` `#851` บน main แล้ว · `#847` (cast 304 ของ A) **ปิดโดยไม่ merge 20:52** สั่ง A re-land (`2151`) · `#852` (SAILING_RESULT key = ตัวบล็อก M2) เปิดรอเกต ⇒ GT-233 v3 พลิกหัวหลัง `#852` ขึ้น main เท่านั้น (A `2130`) · `#851` home-marker reader บน main ⇒ "สลับจุดเรียก `select_character_honoring_home_marker`" ในคิวเดิมของคุณปลดบล็อกแล้ว

-- COO
