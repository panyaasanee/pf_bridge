# LANE-B round oabhhe — 2026-09-06T06:03+07:00 start

## รอบนี้ขยับ NOW/M ข้อไหน
NOW.md หัวข้อ "M4 · LANE-B" / "บันไดไมล์สโตน M3" — งานที่ COO-DECISION `20260906_0548` สั่งให้ LANE-B
ทำ "รอบถัดไป" (≈07:41 กำหนด PR ฉาก 8) คือรอบนี้เอง มาถึงก่อนกำหนดเล็กน้อย

## กล่องจดหมายที่บริโภครอบนี้
- `20260906_0548_COO-DECISION-b0441-widen-death-scope-bg0008-...-LANE-B.md` — บริโภคเต็ม (ข้อ 1/2) +
  บางส่วน (ข้อ 3) ดูใบ `.CONSUMED.txt` คู่ + จดหมายถามใหม่ด้านล่าง

## ทำอะไรไปแล้ว
1. **`GT-223` เติมบล็อก `ATTENDED:`** ตาม R364 ข้อ 2 (เพิ่มก่อนหัวข้อ objective ในใบ ไม่แตะเนื้อใบเดิม)
2. **ลงทะเบียนฉาก Bg0008 (Silver Harbour)** — `pirate-force-server#895` (`claude/gifted-clarke-oabhhe`,
   ไม่ draft, มี `PF-AUTOMERGE: v4` ยืนยันแล้วด้วย GET):
   - mining tool (`--identity-rule cline`) ให้ตัวเลขตรงกับจดหมาย 0548 ทุกตัว: 9 hostile/7 templates
     มินได้ = {21,23,26,27,51,52,66,67}->{274,277,280,281,527,544} บวก placement 69->template 529
     (Nina) · cross-check กับ `world_bg0008_identity.IDENTITIES` ของ LANE-A: ตรง 9/9
   - หลัง withhold Nina: ship 8 rows / 6 templates
   - `mob_death.WIDENING_RULINGS`/`WIDENING_RULING_SCENES` ใหม่ + `field_mobs.LANE_WITHHELD_PLACEMENTS`
     ใหม่ (คู่ Carlos) + เทสสองครึ่งตามที่ 0548 สั่ง (`tests/test_field_mob_tables_bg0008.py` ใหม่ + ส่วน
     ขยาย 11 ไฟล์เทสเดิม) + `field_mob_ai_tables.py` regenerate ให้ครอบ AI ของ 6 เทมเพลตที่ ship จริง
   - full suite บน merged tree (มี origin/main ล่าสุดตอน push): 11901 passed, 365 skipped, 0 failed,
     23403 subtests · `pf_gate_preflight.py` เขียวทุกข้อยกเว้น `GAME_TEST_QUEUE.md` เกิน ceiling ของ
     pf_bridge เอง (ของเก่าก่อนรอบนี้ ไม่ใช่ของ PR) — ไม่ใช่ตัวบล็อกรอบนี้
   - `ADVERSARY_UNAVAILABLE` จาก pf-builder (ไม่มี Agent tool) → orchestrating session สั่ง `pf-adversary`
     จริงต่อบนกิ่งเดียวกันก่อน push (ต้นรอบพร้อมเริ่มงานไม่ทัน เพราะกิ่งยังไม่มีอะไรให้ตรวจตอนนั้น — สั่ง
     ทันทีที่ diff พร้อมแทน) · ผลยังไม่คืนตอน push ⇒ **`ADVERSARY_PENDING pirate-force-server#895`**
     บันทึกในไฟล์รอบนี้ · **ผลคืนหลังปลดล็อกแล้วให้รอบหน้าของสาย B หยิบเป็นงานแรก**
   - self-review ที่ pf-builder ทำจริงระหว่างเขียน: มิวเทตมือ 3 จุด (ลบ Nina ออกจาก
     `LANE_WITHHELD_PLACEMENTS`, ใส่ 529 เข้า `WIDENING_RULINGS`) ยืนยันเทสที่เกี่ยวข้องล้มจริง
3. **เริ่มขุด 5 ฉากถัดไป (read-only recon)**: `bg0006`/`Bg0007`/`Bg0011` สะอาด (ไม่มี avatar `P_`/ดรอปศูนย์)
   · `bg0009` มี 2 แถวน่าสงสัย (avatar `M0..` ปกติ แต่ดรอปศูนย์ทุกช่อง — ต่างจากเกณฑ์ Carlos/Nina) ·
   `bg0010` เครื่องมือ **crash** (`ValueError ... 'UNRESOLVED'` ที่ template_id ดิบ) ทั้งฉากมินไม่ได้เลย
   → เขียนใบถาม `20260906_0659_LANE-B-ASK-COO-five-scene-recon-...md` แทนการส่งเป็นใบเดียวตามที่ 0548
   ขอ (สองฉากติดจริง ไม่ใช่แค่ต้องรอ) — ยังไม่เกินกำหนด (≈10:41 = อีกหนึ่งรอบ)

## ไม่ได้แตะ (นอกขอบเขตรอบนี้ บันทึกให้รอบถัดไป)
- `tests/test_mob_ai_control.py` บรรทัด ~231-235: คอมเมนต์เก่าอ้างว่า Bg0015 ไม่อยู่ใน
  `field_mobs._SCENE_TABLE_MODULES` ซึ่งเท็จมาหลายรอบแล้ว (ของเก่า ไม่ใช่รอบนี้ทำเสีย)
- `mob_scene_recompose.py` docstring ~365-395: ตัวอย่างเก่าอ้างถึง "scene 8" บางจุดที่ยังไม่อัปเดต
  หลังรอบนี้ (ของเก่าเช่นกัน)
- caller `apply_hp_damage` ยังพักตาม NOW ("จนกว่า Door B ส่งจริง") ไม่แตะ
- `DEATH_SEED_WIRING` เป็นของ chief อ่าน ไม่ใช่ของสายนี้

## รอบหน้าทำอะไร
1. เช็คผล `pf-adversary` ของ `#895` ก่อนงานอื่น — มีของต้องแก้ให้แก้เป็นข้อแรก
2. รอคำตอบ `20260906_0659` (ASK-COO) เรื่อง bg0010 crash + bg0009 สองแถว — ถ้าเงียบเกิน 1 ชม. เริ่มขุด
   raw TSV เอง (static, ไม่ใช่ predicate ใหม่) แล้วส่งรายการ 5 ฉากที่เหลือ (deadline ≈10:41)
3. ถ้า `#895` merge แล้ว: cherry-pick เช็คว่า main มีจริงก่อนเขียนว่า "อยู่บน main" (ห้ามเดา)
4. งานสำรอง ถ้าติดหมด: RE/STATIC ของ COMBAT ที่ตอบได้จาก factpack/gamedata ที่ commit แล้ว (grep ก่อน)

## PR/สถานะ
- `pirate-force-server#895` — **เปิดแล้ว ไม่ draft มี marker** รอ gate + adversary + merge (ห้ามเขียนว่า
  "อยู่บน main" จนกว่ารอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`)
- `pf_bridge` claim `#1438` (`claude/practical-knuth-oabhhe`) — ปลดล็อกโดยไฟล์รอบนี้ (แก้ body เติม
  marker แยกทีหลัง)

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรวันนี้ (P-2/GT ยังปิดเหมือนเดิม) แต่โค้ดที่ทำให้มอน 6 ตัวใน
Silver Harbour ตายได้จริงแทนที่จะโดนปฏิเสธ ถึง PR แล้ว รอ gate/adversary/merge | `pirate-force-server#895`
