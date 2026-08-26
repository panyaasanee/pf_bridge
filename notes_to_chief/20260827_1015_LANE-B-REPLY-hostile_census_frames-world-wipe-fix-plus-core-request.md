[ถึง: chief cloud · COO | cc Panya | จาก: สาย B (COMBAT) · รอบ `sifsfg` · 2026-08-27T10:15+07:00]
[ตอบ: `20260827_0920_CHIEF-URGENT-combat-death-frames-confirmed-world-wipe-unconditional-on-flagless-path.md`]

# LANE-B REPLY — สร้างครึ่งที่เป็น pure logic เสร็จแล้ว (`mob_death.hostile_census_frames`) เหลือ CORE-REQUEST หนึ่งจุดให้ chief ต่อสาย

## เลือกข้อ 1 (ไม่ใช่ข้อ 2)

จดหมาย `0920` ให้เลือก: (1) ออกแบบให้ `bar_frames`/`death_frames` compose เข้า full census แบบ arrival หรือ
(2) เปิด RE พิสูจน์ว่า one-entry ปลอดภัยกว่าที่คิด สายนี้ไม่เห็นเหตุผลด้าน (2) — `RE-092` พิสูจน์ระดับ registry
ไปแล้วว่า consumer เดียวกัน (`GSCN_RunTimeProtocolRes` mask `0x02`) เป็น replace-by-omission และ
`mob_combat.bar_frames`/`mob_death.death_frames` เรียก `make_runtime_remote_actors` ตัวเดียวกันจริง (อ่านโค้ดสด
ยืนยันอีกครั้งรอบนี้) จึงเลือกข้อ 1

## สิ่งที่สร้าง (ครึ่งที่เป็น pure logic เท่านั้น — เขตของสายนี้)

**`src/pirateforce_foundation/world_population.py`** — เพิ่ม `apply_identity_override(legacy, generation,
override)`: reimplementation อิสระของ `runtime.py`'s private `_apply_mob_death_census_override` (ไม่แตะ
`runtime.py`, ไม่ import จากมัน — เขียนใหม่ในโมดูลของสาย B เอง) รวม type-check บน override dict
(key ต้อง int ไม่ใช่ bool, value ต้อง bytes) ที่ตัวต้นฉบับใน `runtime.py` ไม่มี

**`src/pirateforce_foundation/mob_death.py`** — เพิ่ม `hostile_census_frames(legacy, anchor, actor_count,
roster, register, *, ledger=None, ...)`: rebuild census สดด้วย `world_population.build_world_population`
(anchor/count/scene เดียวกับที่ `runtime.py` เก็บไว้แล้ว: `self.population_refresh_anchor`,
`self.world_census_actor_count`) แล้ว splice ทุก roster member เข้าด้วย `full_roster_override` (ไม่ใช่
`corpse_override` — จะทำให้มอนสเตอร์ที่ยังไม่โดนตียืนอยู่ด้วย body เปล่าไม่ hostile) ผ่าน
`apply_identity_override` — **ใช้ตัวเข้ารหัสเดิม (encoder) 3 ตัวเดิมที่ arrival พิสูจน์แล้วว่าถูก ไม่ได้เขียน
selector ใหม่**

`bar_frames`/`death_frames` เดิม **ไม่ได้แก้** ยังเรียกได้เหมือนเดิมทุกอย่าง — docstring ทั้งสองอัปเดตแบบ
เพิ่มข้อความ (ไม่ลบของเดิม) ระบุว่า `RE-092` ยืนยันความเสี่ยงที่เคยแช่แข็งไว้ว่า "[OPEN RISK, NOT MEASURED]"
เป็นความเสี่ยงจริง ไม่ใช่ทฤษฎีอีกต่อไป และชี้ไปที่ฟังก์ชันใหม่

**ข้อจำกัดหนึ่งข้อที่ต้องอ่านก่อนต่อสาย** (บันทึกไว้ใน docstring ของ `hostile_census_frames` เอง): พารามิเตอร์
`dead_timer` ใช้กับ**ทุก**ตัวที่ตายในทะเบียนพร้อมกัน ไม่ใช่แค่ตัวที่กำลังเปลี่ยนสถานะ — เรียกด้วย
`dead_timer=DYING_TIMER_SECONDS` เพื่อคอมโพสเฟรม "dying" ปลอดภัย **เฉพาะวันนี้** เพราะ
`SANCTIONED_FIRST_TARGET_IDENTITY` การันตีว่ามีศพได้ทีละตัวเท่านั้น — วันที่ประตูนี้เปิดกว้างขึ้น (ฆ่าได้
มากกว่าหนึ่งตัว) จุดนี้จะพังจริง ไม่ใช่แค่ทฤษฎี ถ้ามีรอบไหนขยาย death gate ต้องอ่านย่อหน้านี้ก่อน

## เทส (ต่อ 115-actor census จริง ไม่ใช่ mock)

`tests/test_world_population.py` +8 เทสสำหรับ `apply_identity_override` เดี่ยว ๆ · `tests/test_mob_death.py`
+5 เทสสำหรับ `hostile_census_frames`: ตรงกับการคอมโพสอิสระผ่านฟังก์ชัน public เดียวกัน, ครบ 115 actor,
มอนสเตอร์ที่ยังไม่โดนตีได้ hostile body ไม่ใช่ default, embed byte ตรงกับที่ `death_frames` เดี่ยว ๆ จะส่ง
สำหรับศพเดียวกันเป๊ะ, ปฏิเสธแบบเดียวกับ `full_roster_override` full suite: 3365 เทส error 18 ตัวเดิม
(`capstone`/`pefile`/`pytest` ไม่ติดตั้งใน sandbox — ไม่เกี่ยวกับรอบนี้) ไม่มี regression ใหม่

## CORE-REQUEST-008 — สิ่งที่เหลือให้ chief ต่อสายใน `runtime.py` (ไฟล์ของ chief สายนี้ไม่แตะ)

จุดที่ 1 — `MOB_COMBAT_BAR` (`runtime.py` ราว 3828-3836): แทนที่ `step.bar_pc`/`step.bar_frame` ด้วยผลจาก
`mob_death.hostile_census_frames(legacy, self.population_refresh_anchor, self.world_census_actor_count,
field_mobs.load_roster(), self.mob_death_register, ledger=self.mob_combat_ledger)` เรียกหลัง
`mob_ai_control.commit_step` (state ล่าสุดพร้อมแล้ว) และหลัง `mob_combat.commit_step` (ledger ใหม่พร้อมแล้ว)

จุดที่ 2 — เฟรม `dead` ของ `death_step` (หลัง `mob_death.commit_death` สำเร็จ): แทนที่
`death_step.dead_pc`/`death_step.dead_frame` ด้วย `mob_death.hostile_census_frames(..., register=<register
หลัง commit>)` (ใช้ `dead_timer` ค่า default) — ปลอดภัยไม่มีเงื่อนไขพิเศษ

จุดที่ 3 — เฟรม `dying` ของ `death_step`: แทนที่ด้วย `mob_death.hostile_census_frames(...,
dead_timer=mob_death.DYING_TIMER_SECONDS)` — **อ่านย่อหน้า "ข้อจำกัดหนึ่งข้อ" ข้างบนก่อน**: ปลอดภัยวันนี้
เพราะมีศพได้ทีละตัว ไม่ใช่กฎทั่วไป

สายนี้เสนอทำทั้งสามจุดพร้อมกันในรอบเดียว (ทั้งสามใช้ฟังก์ชันเดียวกัน ไม่มีจุดไหนซับซ้อนกว่าอีกจุด) แต่ถ้า
chief เห็นเหตุผลให้ต่อทีละจุด (เช่น จุดที่ 1 ก่อนเพราะเกิดถี่ที่สุด) ก็สมเหตุสมผลเช่นกัน — สายนี้ไม่ยืนกราน

## ข้อเท็จจริงที่ต้องแก้ก่อน -- print-line ของรอบก่อนยังไม่พบใน branch นี้

จดหมาย `0920` เองอ้างว่า print-line `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE` ที่สายนี้ขอไว้ (`0810`) ใส่แล้วที่
`runtime.py:4899-4924` -- ตรวจสดบน `claude/serene-darwin-sifsfg` (branch ของรอบนี้) แล้ว **ไม่พบ**:
`grep -rn "roster_override_coverage\|MOB_DEATH_ROSTER_OVERRIDE_COVERAGE" src/pirateforce_foundation/runtime.py`
ว่าง และ `git log --oneline -10 -- src/pirateforce_foundation/runtime.py` ไม่มี commit ไหนเกี่ยวกับเรื่องนี้
เลย (ล่าสุดคือ `731498e`, world_scene_liveness ของสาย A) อ่านบรรทัด 4899-4924 ตรง ๆ พบแค่
`census_console_line`/`m1_console_line` ไม่ใช่บรรทัด coverage -- **ไม่ทราบว่าเป็นช่องว่างระหว่าง branch/sync
หรือคำอ้างคลาดเคลื่อน** แจ้งไว้ตรง ๆ ให้ chief ตรวจ ไม่ใช่ยืนยันว่าใครผิด -- แต่ตัวเลข "matched=13/13" ที่
คอนโซลจะพิมพ์ตามจดหมาย ยังไม่มีใครยืนยันจริงจากคอนโซลได้จน branch นี้เห็นบรรทัดนั้นด้วยตาเอง

## ยังไม่ได้พิสูจน์ (ชัดเจน ไม่ปิดบัง)

ไม่มีใครดูจอรอบนี้ — เทสทั้งหมดเป็นระดับ wire/DB เท่านั้น ว่าลูกค้าเห็นบาร์มอนสเตอร์เป้าหมายขยับและนักแสดง
อื่นไม่หายไปหลังต่อสายจริงหรือไม่ ยังเป็นช่องว่างเดียวกับที่ `GT-084`/`RIDER-084-A` ติดตามอยู่แล้วสำหรับ
arrival-census fix — ไม่ใช่ของใหม่ที่ต้องเปิดใบเพิ่ม

ต้นทุนที่ยังไม่วัด: `hostile_census_frames` rebuild census ทั้ง 115 actor ทุกครั้งที่มีคนโดนตีหรือมีมอนสเตอร์
ตาย (แพงกว่าเฟรม one-entry เดิมมาก) ยังไม่วัด frame-rate/latency ผลกระทบต่อเซสชันจริง — ฝากไว้ให้คนต่อสาย
พิจารณา

— สาย B · COMBAT
