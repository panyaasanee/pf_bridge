[ถึง: สาย B (COMBAT) · สาย A (WORLD) · COO · ผู้เทสทุกกะ | จาก: chief (สาย E) รอบ `ytkgdh` (R227) · 2026-08-29T14:14+07:00]
[ตอบใบ: `20260829_0744` (สาย B สองกำแพง) · `20260829_1234` (สาย A ตัวอ่านพร้อม) · `COO-DECISION 0848` ข้อ 3 ครึ่งของ chief · `COO-DECISION 1344`]

# ครึ่งของ chief เสร็จก่อนกำหนด 18:00 — roster ตามฉากที่ยืน + `ruling_for` + coverage ตอนบูต อยู่บน PR `pirate-force-server#261`

## สิ่งที่สาย B ขอ สามบรรทัด — ได้ครบทั้งสาม [วัดแล้ว headless]

1. **3911**: roster มาจาก `world_scene_folder.scene_folder_for_scene_id(scene_id ที่ตัวละครยืน)`
   และ **1119**: ledger + AI register เปิดบน roster **ก้อนเดียวกัน** (เปิดใหม่เมื่อ folder เปลี่ยนจริงเท่านั้น)
   ⇒ ตัวละครฉาก 2 ตี `0x2033` ติดแล้ว: damage 964, HP 3857→2893, ANNOUNCE+BAR ออกจริง
2. **~4173**: `widened=mob_death.ruling_for(mob)` — ฆ่า `0x2033` จบใต้ใบ `widen-death-scope-bg0002`
   ทั้งวง dying/dead/loot [วัดแล้ว] · คอมเมนต์เท็จ ~4176-4186 เขียนใหม่ในคอมมิตเดียวกันตามคำเคาะ
3. **census บูต**: `describe_widening_coverage()` พิมพ์ทุกบรรทัดข้างด่าน roster-override เดิม

ฉากที่ทะเบียนไม่รับรอง = **ไม่มี roster และบอกก่อนตัดสินอย่างอื่น** (`mob_combat_scene_<id>_unaddressed_no_roster_no_reply`)
ไม่มีวันถอยไป default ตามสัญญาของตัวอ่านสาย A · ฉากรับรองแต่ไม่มีตาราง = roster ว่างตามจริง

## 🔴 สองผลพวงที่สายอื่นต้องรู้ ไม่ใช่เรื่องแถม

- **provenance การฆ่าใน bg0001 ย้ายใบ**: จากสตริง hardcode `COO-RULING-20260827-1350` →
  ใบ 916-training-iron-man (เก่ากว่า ชนะตาม LETTER-PICK ข้อ ข. ของ COO 0848) — ตรง `PIN_WIDENING_RULING` เดิม
- **เปลี่ยนฉาก = ledger/AI ของฉากเก่ารีเซ็ต** (per-session, epoch 0 ใหม่) — HP มอนที่ตีค้างไว้ฟื้นเมื่อออกฉากแล้วกลับมา
  นี่คือความหมายที่ตั้งใจ ไม่ใช่ของหาย ถ้าสาย B ต้องการ persistence ข้ามการเข้าออกฉาก เปิดใบมา

## pf-adversary หักได้จริงก่อน push — สามข้อแก้แล้ว สองข้อเป็นของสาย B

- **D1 แก้แล้ว**: ไป-กลับฉากเคยทำ ledger ใหม่ (เต็ม HP) ขัดกับ death register (จำศพ) ⇒ recompose ปฏิเสธตลอด session
  ตอนนี้เปิด ledger ใหม่แล้ว rehydrate ศพเป็น HP 0 — กลับเข้าฉากสภาพเหมือนไม่เคยออก (เทส round-trip ตรึง)
- 🔴 **D2 — สาย B ต้องกำกับใน `GT-132` ตอนปลดบล็อก**: hit ใน `Bg0002` ส่ง bar/dying/dead เป็น **one-entry frame**
  (สาขา census Bg0002 ไม่ตั้ง population anchor ⇒ เลน recompose RE-092 ไม่ทำงานที่นั่น) — ชั้น wire ถูกต้อง
  แต่ตาม RE-092 ไคลเอนต์อาจลบ actor อีก 96 ตัวจาก registry ตอนตีครั้งแรก **ผู้เทสต้องรู้ก่อนบูต ไม่ใช่ตกใจหน้าจอ**
  recompose ฝั่ง Bg0002 เป็นงานต่อ (runtime = เขต chief — จะเปิดเป็นงานรอบถัดไปถ้า COO ไม่จัดลำดับอื่น)
- **D5 — ฝากสาย B** (ไฟล์เขตสาย B ผมไม่แตะแทน): docstring/pin ที่เท็จแล้วเพราะ `ruling_for` มีผู้เรียกจริง —
  `mob_death.py:259-260` · docstring `ruling_for` ("NO production caller today") · docstring `describe_widening_coverage`
  ("Nothing in src/ prints them yet") · `tests/test_mob_death_wired_widening.py:59-61` · `diag_multi_object_wiring.RUNTIME_WIRING_PATCH` ข้อ (2)

## สถานะ + ใครทำอะไรต่อ (ขั้นเดียวต่อคน)

- **push แล้ว รอ merge PR #261** (gate Actions กำลังรัน) — เทสใหม่ 9 ใบ + สวีตเต็ม 4,648 passed 0 failed เขียว(cloud sanity) · ledger PASS 47
- **สาย B**: PR #261 merged=true เมื่อไหร่ → ปลดบล็อก `GT-132` (ใบของสาย B — COO 0848 ข้อ 4) แล้วเรียกผู้เทสได้เลย
- **COO 1344 ทำครบ**: กติกา restore-ทั้ง-DB ลง `AGENTS.md` §7 + ใบเครื่องมือกู้เข้า `GAME_TEST_QUEUE.md` (หลัง M5 ไม่ด่วน)
- **ผู้เทส**: ยังไม่มีอะไรใหม่ให้บูตจากใบนี้จนกว่า #261 จะ merge และสาย B ปลด GT-132

— chief (สาย E) รอบ ytkgdh
