# รอบ `yqbwri` (LANE-B / COMBAT) — 2026-09-05T03:06 → 03:40+07:00

ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน: **ยังไม่เห็นบนจอ** — สองใบนี้เป็น PR เซิร์ฟเวอร์ที่รอเกต/รอจุดเรียกของ chief
ก่อน แต่กลไกพร้อมแล้ว: (1) เมื่อ chief ปลด `GT-247` เป็น READY ผู้เทสจะตั้ง `PF_POSE_TRIAL=280,284,288,282,290,286`
แล้วคลิกตีมอนหกครั้ง เห็นคอนโซลบอกค่าที่ส่งแต่ละครั้งและ (ถ้ามี id ไหนแก้ปัญหาได้) เห็นท่าโจมตีจริงครั้งแรก
(2) เมื่อ chief เสียบจุดเรียกของตัวเอง การประกาศพื้นซ้ำระหว่างต่อสู้จะไม่รัวจนคอนโซล/ไวร์บวมอีกต่อไป (ครั้งเดียวต่อพื้นใหม่)

## NOW ขยับข้อไหน
ไม่ขยับ M — GT-247 ยังอยู่ที่ BLOCKED-ON-WIRING จนกว่า chief จะเห็น PR นี้ merge (ตามที่ใบ `0248` สั่งเอง)
งานรอบนี้คือของที่ใบ `0247`/`0248` สั่งตรง ไม่ใช่คิว BUILD-004/005/006 ของตัวเอง — งานสำรอง (BUILD-005 M4 hit/death
บน Port Royal) ไม่ได้แตะรอบนี้เพราะมีงานตรงจาก COO เต็มโควตาเวลาแล้ว

## งานที่ทำ
1. **`GT-247` (ก)** — `PF_POSE_TRIAL` รับ list คั่นจุลภาค วนหนึ่งค่าต่อหนึ่งหมัดที่ต่อจริงใน production
   `_dispatch_mob_combat` (ไม่ใช่ scenario ที่ตายแล้ว) · ไม่ตั้งค่า/ผิดรูป = byte-identical กับ main
   · พิมพ์ `POSE_TRIAL sent=<id> hit=<n>` ทุกหมัดที่ arm
2. **ground-reannounce latch** (`COO 0247` ข้อ 1) — `DropLedgerCell.surviving_blow_reannounce_due`/
   `.note_surviving_blow_reannounced` + wiring ใน `reannounce_ground_after_a_surviving_blow` ·
   133 หมัดไม่ฆ่าติดกันบนเจนเนอเรชันเดียว = ประกาศจริง 1 ครั้งพอดี
3. **`rehydrate_from_store`** (`COO 0247` ข้อ 2) — พิสูจน์ว่า `mob_ground_persistence.restore_scene_ground`
   ที่มีอยู่แล้วทำงานจริงกับ `SQLiteStore` จริงตั้งแต่ LANE-DB ลง taken-door · ไม่เขียนฟังก์ชันใหม่ซ้ำ · แก้ถ้อยคำเก่า
4. **ถ้อยคำ `mob_drop_presence.py:766-771`** (`COO 0247` ข้อ 4) — แก้จากยืนยันเป็น UNMEASURED ตามที่ chief วัดไว้

## adversary
รอบนี้สั่งสองครั้ง (ตามเพดาน 2 ครั้ง/รอบ):
- ครั้งที่ 1 (บนงานข้อ 1 เท่านั้น): พบ 1 จุดจริง — `print()` เปลือยใน `build_action_vital_echo`'s except กลายเป็น
  เข้าถึงได้จาก production path ที่มีชีวิตแล้ว (เดิมเข้าถึงได้เฉพาะทาง scenario ที่ตายแล้ว) → แก้แล้ว ผ่าน `_say()`
  พบเพิ่มอีกจุด (methodological, ไม่ใช่บั๊ก): หมัดที่ arm ได้ ActionVital สองเฟรม (เฟรมสืบทอด + เฟรมของ pose trial)
  ปฏิสัมพันธ์กับคิว `+0x20` ของไคลเอนต์ยังไม่มีใครวัด → เขียนแจ้ง ka1-A ในจดหมายถึง chief แล้ว ไม่ใช่โค้ด
- ครั้งที่ 2 (งาน latch): คืนผลแล้วก่อนปิดรอบ — พบ 2 จุดจริง ทั้งคู่แก้แล้วในรอบนี้เอง (ไม่ต้องรอรอบหน้า):
  (ก) latch ผูกกับ `DropLedger.generation` เปล่า ๆ ไม่ผูกกับฉาก — เดินข้ามฉากไม่ฆ่าอะไรจะทำให้ latch อ่านผิดว่า
  "บอกแล้ว" ทั้งที่ฉากใหม่ไม่เคยถูกบอก (Way-1 มีของหลายฉากยืนพร้อมกัน ไม่ใช่กรณีหายาก) → แก้เป็นผูกกับ
  `(scene_key, generation)` (ข) อ่าน generation โดยไม่กวาดของหมดอายุก่อน (จุดอ่านอื่นในคลาสเดียวกันกวาดก่อนเสมอ)
  → แก้ด้วยฟังก์ชันกลางที่กวาดก่อนอ่านเสมอ · เทสใหม่ 5 ตัวปักทั้งสองจุด · push เป็น commit ที่สองใน PR เดียวกัน

## ชุดเทส
- ระหว่างทำงาน: `pytest tests/test_pose_trial.py tests/test_action_ack.py
  tests/test_pose_trial_production_hit_wiring.py tests/test_mob_combat_dispatch.py
  tests/test_mob_drop_presence_surviving_blow.py tests/test_mob_drop_presence_surviving_blow_latch.py
  tests/test_mob_ground_persistence.py` — เขียวทั้งหมดหลายรอบระหว่างแก้
- ชุดเต็มสองครั้ง (เกินหนึ่งครั้งเพราะแก้ตามผล adversary รอบสองหลังชุดเต็มครั้งแรกผ่านแล้ว — ตามกติกา
  "แก้หลังชุดเต็มผ่าน ต้องรันเต็มใหม่ก่อน push"): ครั้งแรกก่อนแก้ latch **10462 passed, 323 skipped,
  19607 subtests passed, 0 failed** (382s) · ครั้งสองหลังแก้ (คอมมิตสุดท้ายจริง ก่อน push) **10491 passed,
  323 skipped, 19615 subtests passed, 0 failed** (379s) · `python3 -V` = Python 3.11.15
  (cloud sanity เท่านั้น — ยังไม่มี 3.14/cp874 บนโคลนนี้)

## จดหมาย
- `20260905_0330_LANE-B-TO-CHIEF-ground-reannounce-latch-landed-plus-gt242-ab-step-content.md`
  (สถานะสี่ข้อของ `0247` + ข้อสังเกตสองเฟรมของ `0248` + เนื้อขั้น A/B ของ `GT-242` ที่ `0215` ข้อ 5 เสนอ ขอเลขใบ)
- consumed: `0247`, `0248` (สอง `.CONSUMED.txt` วางแล้ว)

## สถานะ push
push แล้ว รอ merge PR เซิร์ฟเวอร์ `pirate-force-server#787` (เปิดแล้ว มี marker ตั้งแต่เปิด) ·
claim PR `pf_bridge#1246` เติม `PF-AUTOMERGE: v4` แล้ว = ปลดล็อกแล้ว (GET ยืนยัน marker อยู่จริงทั้งสองใบ)

-- LANE-B (COMBAT) รอบ `yqbwri`
