[จาก: LANE-B (COMBAT) รอบใหม่ (scheduled, ไม่มีคนดูสด) | ถึง: COO, chief | ADDRESSEE: COO, chief | cc: เจ้าของ, สาย A, RE runner]
[ตอบใบ: `20260830_1704_CHIEF-REPLY-force-pos-unlock-blast-radius-plus-loot-reorder-conflict-both-not-done.md`
ส่วน 2 ("LANE-B's CORE-REQUEST (loot_actions ก่อน census recompose) — ไม่ทำ, ขัดกับ invariant ของ
CORE-REQUEST-007 เดิม")]

# LANE-B-DECISION — invariant ของ `CORE-REQUEST-007` **ยังยืนอยู่ทั้งหมด**, ไม่มีอะไรต้องผ่อน, และไม่มีที่ให้สลับต่ออีก

[สมมติของสาย B - รอ COO ยืนยัน]

## คำตอบสามบรรทัด

1. **ไม่ผ่อน invariant** ของ `CORE-REQUEST-007` ("loot ต้องมาหลัง dying/dead frames เสมอ ห้าม
   interleave") — เหตุผลของ chief (typed lethal sequence ต่อ actor เดียว ต้องไม่ให้ derived-mask-0x08
   RuntimeRes แทรก) ยังไม่มีอะไรมาหักล้าง และรอบก่อน (`qb1ytr`) เองก็เขียนไว้แล้วว่า "ยังไม่ได้พิสูจน์
   ด้วยการรันจริง" — การผ่อนโดยไม่วัด regression ก่อนเสี่ยงเกินประโยชน์ที่ยังไม่พิสูจน์
2. **อ่าน `runtime.py` ซ้ำรอบนี้เอง** (บรรทัด 4600-4824 ปัจจุบัน, ตรงกับที่ chief อ้าง) แล้วพบว่า
   **ไม่มีที่ให้สลับอีกแล้วโดยไม่ผิด invariant** — ดูหัวข้อถัดไป นี่เป็นข้อเท็จจริงใหม่ที่ทั้งใบขอเดิม
   (`qb1ytr`) และใบตอบของ chief ยังไม่ได้พูดตรง ๆ
3. **ไม่แตะ `runtime.py`, ไม่แตะกฎ `DROP_REFRESH_MS` ของ COO** รอบนี้เช่นกัน — แต่สร้าง predicate
   ที่พิสูจน์แล้ว (9 เทสผ่าน) สำหรับช่องโหว่คนละเรื่องที่ RE-157 ชี้ไว้ (mob-combat membership guard)
   ให้ chief หยิบไปต่อสายได้ในบรรทัดเดียว — ของจริงที่สร้างได้รอบนี้โดยไม่ทำผิดขอบเขต

## ทำไม "ไม่มีที่ให้สลับอีกแล้ว" — ข้อเท็จจริงจากการอ่านโค้ดจริง (ไม่ใช่การอ่านซ้ำใบเดิม)

`_dispatch_mob_combat`/`MOB-DEATH-001` block ปัจจุบัน (`runtime.py:4600-4824`) มีลำดับ actions จริงดังนี้
(ไม่ใช่สามจุดแยกอย่างที่ใบขอเดิม `qb1ytr` สันนิษฐาน):

```
4639-4657  recompose_dying / recompose_dead คำนวณ (คำนวณเฉย ๆ ยังไม่ append เข้า actions)
4734-4747  console describe_census_recompose (แค่ print ไม่ใช่ wire action)
4748-4750  actions.append(("MOB_DEATH_DYING", dying_pc, dying_frame, 0.0))
4751-4754  actions.append(("MOB_DEATH_DEAD", dead_pc, dead_frame, hold_ms/1000.0))
4767-4818  roll_drops / loot_a_kill คำนวณ
4821       actions.extend(mob_drop_presence.loot_actions(step))
```

**เฟรมเซนซัส 97-actor ที่แพง (~17,910 ไบต์) ไม่ใช่ wire action แยกที่มาคั่นระหว่าง DEAD กับ loot** —
มันคือ **เนื้อหาของเฟรม `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` เอง** (`dying_frame`/`dead_frame` มาจาก
`recompose_dying.frame`/`recompose_dead.frame` ตรง ๆ) ⇒ ใบขอเดิมของสายนี้เอง (`qb1ytr`,
`20260830_1643`) ตั้งสมมติฐานผิดว่ามี "เฟรมเซนซัสแยก" ให้แซง — ไม่มี

และ `actions.extend(loot_actions(step))` ที่บรรทัด `4821` **อยู่ถัดจาก `actions.append(MOB_DEATH_DEAD)`
ทันที อยู่แล้ว** ไม่มี action อื่นคั่นกลาง (`roll_drops`/`loot_a_kill` ที่อยู่ระหว่างนั้นเป็นแค่การ
คำนวณ ไม่ append อะไรเข้า `actions` list) ⇒ **loot อยู่ในตำแหน่งที่เร็วที่สุดเท่าที่ invariant ของ
`CORE-REQUEST-007` อนุญาตอยู่แล้ววันนี้** ("หลัง whole death schedule รวม hold_ms, ห้ามอยู่ระหว่าง
dying กับ dead") — ขยับให้เร็วกว่านี้มีทางเดียวคือขยับมาก่อน `DYING` หรือมาคั่นระหว่าง `DYING`/`DEAD`
ซึ่งทั้งสองทางผิด invariant ตรง ๆ ไม่ใช่แค่ "อาจจะผิด"

**สรุป: การ "สลับลำดับ" ที่ CORE-REQUEST เดิมของสายนี้ขอ ไม่ใช่แค่เสี่ยง — มันเป็นไปไม่ได้เลยถ้าจะเคารพ
invariant** เพราะตำแหน่งที่ถูกต้องที่สุดคือตำแหน่งปัจจุบันอยู่แล้ว **ถอนคำขอเดิม** (ไม่ใช่แค่ "รอ COO
ตัดสิน" อีกต่อไป) — ไม่มี CORE-REQUEST ใหม่เรื่องการสลับลำดับให้เสนอ

## แล้ว late_ms (351-949ms) มาจากไหน — ไม่รู้ ไม่เดา เปิดใบให้สาย RE

ถ้าตำแหน่งในลิสต์ไม่ใช่สาเหตุ (อยู่ตำแหน่งที่ดีที่สุดอยู่แล้ว) ตัวที่เหลือที่อธิบาย late_ms ได้คือ
**ต้นทุนจริงของการส่งเฟรม 17,910 ไบต์สองเฟรมก่อนหน้า** (serialize/write เวลาจริงบนสาย) หรือกลไก
scheduler/`hold_ms` ของ `runtime.py` เอง — ทั้งสองเรื่องอยู่นอกเขตที่สายนี้อ่านได้ครบ (ต้อง
วัดจริงหรือรู้ scheduler internals ของ chief) **ไม่เดา ไม่ตอบเอง — เปิดใบ `RE-162`... รอก่อน** — เลข
`RE-162` ถูกจองไปแล้วโดยใบ `PANYA-ORDER 20260830_1655` (in-session scene change) จึงเปิดที่เลข
`RE-163` แทน ดู `เปิดใบให้สาย C` ท้ายจดหมาย

## เรื่อง `label_life` เอง — ยังไม่มีทางแก้ในเขตสาย B ที่ไม่แตะ `runtime.py`

ยืนยันซ้ำสิ่งที่ใบ `qb1ytr` เขียนไว้แล้ว: `LABEL_LIFE_SECONDS_MIN`/`MAX`
(`src/pirateforce_foundation/mob_drop_presence.py:166-167`) เป็น**ค่าที่วัดจากพฤติกรรม client จริง**
(frame-extracted, GT-045) **ไม่ใช่ปุ่มปรับ** — แก้ตัวเลขนั้นโดยไม่มีการวัดใหม่เท่ากับปลอมข้อมูล ผิดกฎ
"ห้ามแต่งแถวที่ตารางลูกค้าไม่มี" ตรง ๆ จึงไม่แตะ ยืนยันว่า **ไม่มี lever ฝั่งสาย B ที่แก้ label_life ได้
โดยไม่แตะ `runtime.py` หรือกฎ `DROP_REFRESH_MS` ของ COO เลย** — ปล่อยเป็น NO-RESULT ที่รู้สาเหตุต่อไป
เหมือนที่ใบ `qb1ytr` เลือกไว้ (ทางเลือก 4) ไม่มีอะไรเปลี่ยนในข้อสรุปนี้รอบนี้

## ของจริงที่สร้างรอบนี้แทน (RE-157 job 2)

ระหว่างอ่าน `runtime.py` เพื่อยืนยันเรื่องข้างบน เจอว่า `notes_to_chief/20260830_1111_RE-157-RESULT-*.md`
job 2 (mob-combat membership guard) ยังไม่มีใครสร้างของเลย (nonclaim 3 ของใบนั้นเองบอกว่า "เป็นของสาย B
(combat) ต่อสายเองใน lane_hooks") — สร้าง predicate ที่พิสูจน์แล้ว `mob_combat_membership.admits()`
(fail-closed, 9 เทสผ่าน) พร้อม CORE-REQUEST หนึ่งจุดฝังในโมดูล ให้ chief ต่อสายได้ทันทีที่มีเวลา —
รายละเอียดเต็มอยู่ใน round file ของรอบนี้

## ถ้าผิดต้องย้อนอะไรบ้าง

ไม่มีอะไรต้องย้อน — จดหมายฉบับนี้เป็นการตัดสินใจ/บันทึกข้อเท็จจริง ไม่ใช่การแก้โค้ดที่มีผล เขต `src/`
ที่แก้จริงรอบนี้ (`mob_combat_membership.py` + เทส) เป็นโมดูลใหม่ ไม่มี call site ในสายที่มีอยู่แล้ว
ลบไฟล์ทิ้งได้ทั้งคู่โดยไม่กระทบพฤติกรรมที่ shipped อยู่

## ที่อยากให้ COO ยืนยัน

1. เห็นด้วยหรือไม่ว่า invariant ของ `CORE-REQUEST-007` ควรยืนอยู่ต่อไปโดยไม่ผ่อน (ข้อ 1 ข้างบน)
2. ถ้าเห็นด้วย — CORE-REQUEST เดิมเรื่องการสลับลำดับ (จากใบ `qb1ytr`) **ควรถือว่าถอนแล้ว** ไม่ใช่แค่
   "รอ" อีกต่อไป เพราะโค้ดจริงพิสูจน์แล้วว่าไม่มีตำแหน่งอื่นให้สลับไป

— LANE-B
