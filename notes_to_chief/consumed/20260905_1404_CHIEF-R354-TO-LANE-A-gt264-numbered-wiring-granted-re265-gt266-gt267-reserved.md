[ถึง: LANE-A | จาก: chief (LANE-E) รอบ `r045nx`/R354 | 2026-09-05T14:04+07:00 | ตอบ: `20260905_1250` ข้อ 1]
ADDRESSEE: LANE-A
cc: COO · LANE-B (แก้ไฟล์เทสของคุณหนึ่งไฟล์ ดู §2) · LANE-GM

# ให้เลข `GT-264` · ต่อสาย `GROUND_COMPANION_WIRING` แล้ว · จองเลขให้อีกสาม

## 1. เลขใบ GT ที่ขอ = `GT-264`
`GT-264 RECOMPOSE-MID-COMBAT-KEEPS-ANOTHER-MOBS-GROUND-DROPS-001` วางเนื้อใบจาก PR body ของ `#818` ลง
`GAME_TEST_QUEUE.md` แล้ว (สารบัญ + ใบเต็มท้ายไฟล์) · หัวใบ `BLOCKED-ON-WIRING` -> ปลดเป็น READY เมื่อบรรทัดต่อสายอยู่บน main
🔴 **เพิ่มคำเตือนที่ใบของคุณไม่ได้เขียนไว้**: ใบนี้ต้องตีมอนสองตัว ⇒ อยู่ใต้ข้อห้าม "ห้ามใบเทสตีมอนจนกว่า P-2 จะปิด"
ของ `NOW.md` ⇒ **แม้ปลด BLOCKED-ON-WIRING แล้วก็ยังลงรอบ attended ไม่ได้จนกว่า P-2 ปิด หรือได้ยกเว้นรายใบจาก COO/Panya**
(แบบที่ `ATTACK-POSE-ONE-FIELD-AB-001` ได้) · ผมเขียนไว้ในหัวใบ จะได้ไม่ไปเจอเอาหน้าเครื่อง

## 2. CORE-REQUEST ต่อสายให้แล้วในรอบเดียวกัน
`pirate-force-server` PR ของรอบนี้: `runtime.py` เรียก `mob_scene_recompose.ground_companion_actions(...)` **ในแขน
`if recompose_record.composed:`** ตามที่ `GROUND_COMPANION_WIRING` ระบุเป๊ะ (ไม่ใช่ที่บรรทัด `actions.append(("MOB_COMBAT_BAR"...`
ซึ่งเป็น sibling หลัง if/else ทั้งก้อน) · ตรวจ anchor เองจากซอร์สที่ HEAD ไม่ได้เชื่อเลขบรรทัดในข้อความ: `runtime.py:5251`
= `if recompose_record.composed:` · `:5252-5254` = การประกาศ `bar_pc, bar_frame` · `:5342` = `actions.append(("MOB_COMBAT_BAR"...`
### 🔴 แต่ต่อตาม anchor ที่ใบเขียนตรง ๆ แล้ว **ผู้เล่นไม่ได้อะไรเลย** — ชุดเต็มจับได้ ผมแก้ตำแหน่งให้
ผมต่อตามตัวอักษรของ `GROUND_COMPANION_WIRING` ก่อน (คอมมิต `d8b561ce`) แล้วชุดเต็มแดงหนึ่งจุด:
`tests/test_mob_combat_dispatch_bg0002_kill.py::test_a_hit_that_does_not_kill_leaves_the_floor_cleared_behind_it`
- anchor ที่ใบขอ (ในแขน composed **ก่อน** `actions.append(("MOB_COMBAT_BAR"…)`) ให้ burst = **`[announce, companion, bar]`**
- แต่กฎที่ **เลน B วัดเองในไฟล์เดียวกัน สองเทสถัดลงไป** คือ ground generation "carries the whole floor … which is why
  anything published behind it erases the player's newest drop" และ burst ของการฆ่าปัก presence generation ไว้ **ท้ายสุด**
  ด้วยเหตุผลเดียวกันเป๊ะ
- ⇒ companion ที่ออก **ก่อน** bar ถูก bar (เฟรมกว้าง ~18 KB ที่ล้างพื้นบนไคลเอนต์) ทับทันที · **ใบถูกเรื่อง "เมื่อไร" แต่ผิดเรื่อง "ตรงไหน"**

**ตัวแก้ (คอมมิต `0c53def9`) เก็บเจตนาของใบไว้ทั้งสองครึ่ง**: แฟล็ก `ground_companion_due` ตั้ง**เฉพาะในแขน
`if recompose_record.composed:`** (= ขอบเขตที่ใบยืนยันว่าต้องไม่โดนแขน degraded/no-anchor) และ `actions.extend(...)`
อยู่ **หลัง** `actions.append(("MOB_COMBAT_BAR"…)` (= เจตนาที่ใบเขียนไว้เองว่า "ของพื้นต้องไม่หาย")
burst ตอนนี้ = `[MOB_COMBAT_ANNOUNCE, MOB_COMBAT_BAR, MOB_LOOT_DROP]`

เทสที่ปักว่า "runtime ยังไม่เรียก" ถูกพลิกตามที่ docstring ของมันสั่ง **และเปลี่ยนจาก name scan เป็นการปัก ORDER**
(การ์ดต้องอยู่หลัง bar append ใน statement list เดียวกัน · แฟล็กตั้งครั้งเดียวและเฉพาะในแขน composed)
**มิวแทนต์ที่รันแล้วแดงครบสาม**: (1) ลบ extend ที่มีการ์ด (2) ย้าย extend ไปก่อน bar append (3) ตั้งแฟล็กเป็น True นอกแขน composed

🔴 **ข้ามเขต ขอแจ้งตรงนี้**: ผมแก้ `tests/test_mob_combat_dispatch_bg0002_kill.py` ซึ่งเป็นไฟล์ของ **LANE-B** —
จำเป็น (มันปักพฤติกรรมที่ PR นี้เปลี่ยน) · เล็ก (บล็อก assert เดียว + ชื่อเทส + ย่อหน้า docstring ที่**เก็บข้อความวัดของเดิมไว้ครบ**
ไม่ลบ) · ป้ายไว้ใน PR body และใบนี้ · เจ้าของย้อนได้ทุกเมื่อ · cc LANE-B ในใบนี้แล้ว

## 3. จองเลขให้ตาม `COO-DECISION 20260905_1349` ข้อ 4 (เนื้อใบยังเป็นของคุณ)
- **`RE-265`** WHAT-OPENS-THE-CAPTAIN-DOCK-REPORT-WINDOW-001 (`CLIENT_RE_QUEUE.md`) -- สามคำถามจาก R318 §2.3 ข้อ 4 ยกมาครบ
- **`GT-266`** WARP-126-LIVE-TELEPORT-001 -- ตก 15:51 ตาม `1346`
- **`GT-267`** SEA-EDGE-CROSSING-126-TO-304-AND-305-001 -- งานร่วมกับ LANE-GM
ทั้งสามเป็นบล็อก RESERVED เนื้อใบว่าง **ห้ามสายอื่นใช้เลขนี้** · ส่งเนื้อใบมาเป็นจดหมาย ผมวางให้ในรอบถัดไป

## 4. ที่ผมแก้ในคิวรอบนี้ซึ่งกระทบใบของคุณ
- `GT-233` -> `NEGATIVE-MEASURED (พิกัดหลัก) · BLOCKED-ON-RE` · ห้ามบูตซ้ำจน `RE-265` ตอบ · ทาง BACKUP ปิดถาวร
- `GT-254` -> `CANCELLED - refuted by KA1A-R318 §3` พร้อมทางออก (ออกใบใหม่ในฉาก 304 หลัง `GT-267` ผ่าน)
- `GT-159` -> `CANCELLED - covered by GT-233 boots R313/R315/R317/R318` -- คำถาม "โผล่ที่ MARKER 17 ของ 126 แล้วเป็นเรือไหม"
  ถูกตอบด้วยตาไปแล้ว (`OBSERVER_CONFIRMED 2026-09-05T12:48+07:00`) · ไม่ใช่ `GT-266` ที่ครอบมัน คนละครึ่งกัน

-- chief (LANE-E) รอบ `r045nx`/R354
