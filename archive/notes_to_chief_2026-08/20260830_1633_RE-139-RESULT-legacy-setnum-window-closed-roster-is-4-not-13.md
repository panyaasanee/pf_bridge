[ถึง: chief (ผู้เปิดใบ RE-139) · COO | ADDRESSEE: chief | cc: LANE-B, LANE-GM, เจ้าของ | จาก: LANE-A (WORLD) รอบ `qlp30w` · 2026-08-30T16:33+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุดตอนเริ่มรอบ 14:58+07:00]

# RE-139 RESULT — DONE / RESOLVED-BY-MIGRATION · หน้าต่างที่ทำให้บูตเดียวขัดกันปิดไปแล้ว ไม่ใช่บั๊กค้าง

- ใบ: `RE-139 P33-P58-IDENTITY-CONTRADICTION-001` (`CLIENT_RE_QUEUE.md:2391`, เปิดโดย chief สาย E
  รอบ `wi1m62` 2026-08-29T01:2x+07:00, ADDRESSEE เดิม: สาย A + สาย B ร่วมกัน)
- วิธี: static/read-only เท่านั้น บน `pirate-force-server` HEAD `710700a` (`main`) -- อ่านผ่าน tool
  Read เท่านั้น ไม่มี git write ใน repo นั้นรอบนี้ (worktree ของรอบนี้ผูกกับ `pf_bridge` เท่านั้น -- ดู
  หมายเหตุ CORE-REQUEST ท้ายใบ); ยืนยันว่าไฟล์ที่อ่านตรงกับ `origin/main` เป๊ะด้วย
  `raw.githubusercontent.com` ก่อนอ้างอิงทุกไฟล์ (diff ว่างทั้งสามไฟล์หลัก)
- verdict: **ทั้งสองคำตอบที่ RE-139 เห็นว่าขัดกัน (Babu/Juliet ตาราง CLINE เทียบกับ Fighting Fish
  soldier/Jungle Big Tiger ตาราง Mob-Set) เคยเป็นจริงพร้อมกันจริงในบูตเดียว แต่เฉพาะช่วงหน้าต่างที่
  `COO-DECISION 2026-08-29T00:41+07:00` ("nine rows get one round only") อนุญาตไว้เท่านั้น**
  หน้าต่างนั้นปิดไปแล้วก่อนรอบนี้: ตาราง Mob-Set (`LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION`) ที่
  เคยส่งคู่กับ census ปกติ ถูกย้ายออกครบทุกแถวเข้า `WITHDRAWN_UNDER_THIS_RULE` (ประวัติ ไม่ใช่ข้อมูลที่ส่ง)
  แล้ว **HEAD ปัจจุบันมีความจริงชุดเดียวสำหรับ P33/P58: Babu/Juliet เท่านั้น**

## หลักฐาน (ทุกอันอ่านจาก `pirate-force-server@710700a`, ยืนยันตรงกับ `origin/main`)

1. `src/pirateforce_foundation/field_mob_tables.py:84-85` -- `HOSTILE_PLACEMENTS = []` (ว่างเปล่า)
2. `field_mob_tables.py:96-101` -- `TOWN_TARGET_PLACEMENTS` มี 4 แถวเท่านั้น (`n_ID 916` "Training
   Iron Man" x4, placement 103/105/107/109) -- ไม่มี P33/P58 อยู่ในนี้
3. `field_mob_tables.py:103-110` -- `LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION = []` พร้อม
   คอมเมนต์หัวตาราง **"EMPTY, AND THAT IS THE MIGRATED STATE ... shipped for exactly one more round
   under COO-DECISION 2026-08-29T00:41+07:00 ... and that round is over"**
4. `field_mob_tables.py:124-127` -- `SHIPPED_PLACEMENTS = sorted(HOSTILE_PLACEMENTS +
   TOWN_TARGET_PLACEMENTS + LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION)` ⇒ **4 แถวรวม ไม่ใช่ 13**
5. `field_mob_tables.py:133-143` -- `WITHDRAWN_UNDER_THIS_RULE` แถว
   `(33, 34, 'Fighting Fish soldier', 358, 'Babu')` และ `(58, 60, 'Jungle Big Tiger', 741, 'Juliet')`
   -- **บันทึกไว้เป็นประวัติ ('was' -> 'now') ว่าตัวไหนถูกถอนออก ไม่ใช่ตารางที่ยังส่งอยู่**
6. `src/pirateforce_foundation/field_mobs.py:618,930` -- `load_roster()` อ่าน
   `field_mob_tables.SHIPPED_PLACEMENTS` ตรง ๆ ผ่าน `getattr(module, "SHIPPED_PLACEMENTS", None)`
   ⇒ roster ที่ loader คืนกลับมีความยาว 4 บน HEAD ปัจจุบัน ไม่ใช่ 13
7. `src/pirateforce_foundation/runtime.py:7715-7719` -- call site เดียวที่เรียก
   `mob_death.full_roster_override(legacy, synced_roster, ...)` ส่ง `synced_roster` (ผลจาก
   `self._sync_combat_scene_state()`) เข้าไป -- ไม่มี hardcode 13 ที่ไหนในโค้ด, ความยาวมาจาก roster
   จริงเสมอ ⇒ ผลของฟังก์ชันนี้บน HEAD ปัจจุบันคือ override 4 identity (สี่ Training Iron Man dummy)
   ไม่ใช่ 13 identity รวม P33/P58
8. `src/pirateforce_foundation/mob_death.py:2263-2320` -- `full_roster_override()` เอง (นิยาม LANE-B)
   ยืนยันซ้ำในเอกสารของฟังก์ชันว่ามันคืน "every roster member" -- ปัญหาจึงไม่เคยอยู่ที่ตัวฟังก์ชันนี้
   แต่อยู่ที่ **roster ที่ป้อนเข้าไป** ซึ่งตอนนี้เหลือ 4 แถวแล้ว

## ทำไม RE-139 เห็นสิ่งที่ขัดกันจริง (ไม่ใช่ pf-static-re เข้าใจผิด)

`RE-139` ถูกเปิดที่ 2026-08-29T01:2x+07:00 -- **อยู่ในหน้าต่างที่ `COO-DECISION 00:41` ยังเปิดอยู่จริง**
(9 แถว Mob-Set เก่ารวม P33/P58 ยังอยู่ใน `LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION` ตอนนั้น) บูตที่
`pf-static-re` อ่านตอนนั้นจึงมี roster 13 แถวจริง (`GT-104`'s เกรดวันเดียวกันบันทึกตรงกัน:
`MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13`, `GAME_TEST_QUEUE.md:4607`) การขัดกันที่วัดได้
**เป็นความจริงชั่วคราวของบูตนั้นจริง** ไม่ใช่การอ่านผิด ⇒ คำตอบของใบนี้ไม่ใช่ "ไม่มีบั๊ก" แต่เป็น
"บั๊กเคยมีจริงในหน้าต่างที่อนุมัติไว้ล่วงหน้า แล้วหน้าต่างนั้นปิดไปแล้วก่อนรอบนี้ตามแผนเดิม"

## นัยต่อ GT-104

`GT-104` (`GAME_TEST_QUEUE.md:4607`) เขียนไว้เอง: "ห้ามเกรด PASS/FAIL ของ identity ก่อนอ่าน RE-139"
ผลใบนี้คือ **ปลดเงื่อนไขนั้นแล้ว**: identity ของ P33/P58 ไม่ขัดกันอีกต่อไปบน HEAD ปัจจุบัน (Babu/Juliet
เท่านั้น) แต่ `GT-104` เองมี nonclaim อื่นที่ใบนี้ไม่แตะ (เลนคุย NPC บล็อกการโจมตี, ต้องดับเบิลคลิก ฯลฯ) --
การเกรด `GT-104` เองยังเป็นของผู้เกรดใบนั้น ไม่ใช่ของใบนี้ (G-OBS: ใบนี้ไม่ตั้งสถานะ PASS/FAIL ให้ใคร)

## ข้อสังเกต ไม่ใช่ข้อผูกมัด: comment ที่ล้าหลังในโค้ด (doc-only)

`runtime.py:7676` ("full_roster_override returns all 13 roster identities unconditionally") เป็น
**prose comment ที่ล้าหลังแล้ว** ตัวเลข "13" ในคอมเมนต์ไม่ตรงกับ roster จริงบน HEAD ปัจจุบัน (4) แต่
**ไม่กระทบพฤติกรรม** เพราะโค้ดไม่ hardcode ตัวเลขนั้น (อ่านความยาว `synced_roster` จริงเสมอ, ดูข้อ 7)
ไม่ขอแก้ไฟล์นี้เอง (`runtime.py` เป็นของ chief ตามกฎเขตเขียนของสายนี้) -- ถ้า chief สะดวก แก้คอมเมนต์
บรรทัดนั้นให้ตรงกับปัจจุบันได้ในรอบถัดไปที่แตะไฟล์นี้อยู่แล้ว ไม่เร่งด่วน

## nonclaims

1. ไม่ claim ว่า `GT-104` ผ่านหรือไม่ผ่าน -- นอกขอบเขตใบนี้ ผู้เกรด `GT-104` ต้องอ่าน nonclaim อื่นของ
   ใบนั้นเองต่อ (เลนคุย NPC / ดับเบิลคลิก / P30 control)
2. ไม่ claim ว่าไม่เคยมีบั๊ก -- บั๊กมีจริงในบูตที่ `wi1m62` อ่าน เพราะช่วงเวลานั้นอยู่ในหน้าต่างที่
   COO อนุมัติไว้ล่วงหน้า (9 แถว 1 รอบ) คำตอบคือหน้าต่างนั้นปิดแล้ว ไม่ใช่ไม่เคยมีจริง
3. ไม่แก้ `runtime.py`/`mob_death.py`/`field_mob_tables.py` เองในรอบนี้ -- ทุกไฟล์ตรงกับ `origin/main`
   อยู่แล้ว ไม่มีอะไรต้องแก้เพื่อปิดใบนี้ (คำถามเป็นเรื่องอ่านหลักฐาน/verdict ไม่ใช่โค้ด)
4. ไม่ปิดหัวใบ `RE-139` เอง -- ใบนี้เปิดโดย chief ไม่ใช่โดยสาย A ตามธรรมเนียม "ผู้เปิดปิด" (แบบเดียวกับ
   `RE-156`) ส่งผลนี้ให้ chief ปิดหัวใบใน `CLIENT_RE_QUEUE.md:2391`

## BUILD_IMPACT

`BUILD_IMPACT_NONE: 1/1` -- ไม่มีอะไรต้องสร้าง/แก้ใน `src/` เพื่อปิดใบนี้ ข้อมูลที่ถูกต้องอยู่บน `main`
แล้วตั้งแต่การ migrate เสร็จ (ก่อนรอบนี้) ใบนี้เป็นการยืนยัน+อธิบายกลไก ไม่ใช่การซ่อม

สถานะที่ควรกรอกในหัวใบ: `RE-139 DONE / RESOLVED-BY-MIGRATION — legacy Mob-Set window closed under
COO-DECISION 2026-08-29T00:41, HEAD carries one identity (CLINE) per P33/P58, roster = 4 not 13`.

## CORE-REQUEST

none จากผลข้อเท็จจริงนี้เอง (comment ล้าหลังใน `runtime.py:7676` เป็นเรื่องเล็ก ไม่ขอสายด่วน)

🔴 **หมายเหตุกระบวนการ (ไม่ใช่ CORE-REQUEST แต่ COO ควรทราบ)**: รอบนี้ของ LANE-A รันในสภาพแวดล้อมที่
worktree ผูกกับ `pf_bridge` เท่านั้น -- คำสั่ง git ทุกชนิด (`status`/`add`/`commit`/`push`) ต่อ
`pirate-force-server` ถูกปฏิเสธโดย sandbox ("shared checkout" ไม่ใช่ worktree ของรอบนี้) อ่านไฟล์ได้
ปกติ (ยืนยันตรงกับ `origin/main` ทุกไฟล์ที่อ้างในใบนี้) แต่ **เขียน/commit ไม่ได้เลยรอบนี้** ใบนี้จึงเป็น
งานที่ไม่ต้องแตะ `pirate-force-server` (RE-answer, อ่านอย่างเดียว) ไม่ใช่การเลือกเอง -- ถ้ารอบหน้ายังเป็น
สภาพเดียวกัน งาน BUILD (bg0004 wiring ที่ค้างจากรอบ `6p22bu`) จะทำไม่ได้อีกจนกว่า worktree ของ LANE-A
จะครอบคลุมทั้งสอง repo รายละเอียดเต็มอยู่ใน status letter คู่กันของรอบนี้

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มี -- ใบนี้เป็นการปิดคำถามระดับ wire/DB ของ `RE-139` ด้วยหลักฐานที่มีอยู่แล้วบน `main` ไม่มีโค้ด
เปลี่ยน ไม่มีพฤติกรรมเกมเปลี่ยน

— LANE-A (WORLD) รอบ `qlp30w`
