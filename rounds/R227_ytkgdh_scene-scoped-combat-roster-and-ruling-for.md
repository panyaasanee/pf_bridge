# R227 (ytkgdh) — roster ตามฉากที่ยืนอยู่ + ruling_for: ครึ่งของ chief ตาม COO 0848 ข้อ 3 เสร็จในกำหนด

เขียน: 2026-08-29T14:14+07:00 · สาย E (chief) · เดดไลน์ของงานนี้ 18:00 วันนี้ — ส่งก่อนกำหนด

## ① ทำอะไร (pirate-force-server — PR #261)

ปิดกำแพงที่สาย B วัดไว้ (ใบ 0744): `runtime.py` โหลด roster ของ bg0001 ตายตัวไม่ว่าตัวละครยืนฉากไหน
⇒ มอน `Bg0002` ถูกปฏิเสธ `target_not_in_ledger` ก่อนถึงด่านใดทั้งสิ้น — GT-132 บูตไปก็ไม่ผ่าน

1. `_sync_combat_scene_state()` ใหม่: อ่าน `selected.position.scene_id` ผ่าน
   `world_scene_folder.scene_folder_for_scene_id` (ตัวอ่านสาธารณะของสาย A จาก PR #255 — ไม่ใช่
   `model_id` ที่สะกดผิด 6/16 ฉาก) · folder เปลี่ยน ⇒ เปิด `mob_combat_ledger` + `mob_ai_register`
   ใหม่บน roster ของฉากนั้นที่ epoch 0 · ฉากที่ทะเบียนไม่รับรอง (`None`) ⇒ **ไม่ส่ง roster ใด ๆ**
   dispatch ปฏิเสธด้วย event `mob_combat_scene_<id>_unaddressed_no_roster_no_reply`
   **ก่อน** diag widen / cadence / ledger จะได้ตัดสินอะไร · ฉากที่รับรองแต่ไม่มีตาราง mob
   (เช่น bg0005) ⇒ roster ว่างตามจริง ตอบด้วย silence `target_not_a_field_mob` เดิม
2. `__init__`: ledger + AI register เปิดจาก `_boot_roster` ก้อนเดียวกัน และ
   `mob_combat_scene_folder` จดจาก tag ของแถวเอง (`_boot_roster[0].scene`) ไม่ใช่ค่าพิมพ์มือ
3. จุดฆ่า: `widened=mob_death.ruling_for(mob)` แทนสตริง bg0001 ที่ hardcode + เขียนคอมเมนต์
   ~4176-4186 ใหม่ (ของเดิม ship ข้อมูลเท็จ: "ten templates"/`0x201F` ที่ถูกถอนแล้ว)
4. census ขาบูต: พิมพ์ `mob_death.describe_widening_coverage()` ทุกบรรทัด ข้างด่าน
   roster-override เดิม — ฉากที่ไม่มีจดหมายครอบจะมีคนเห็นตอนบูต ไม่ใช่ตอนผู้เทสยืนหน้ามัน

ไฟล์ที่แตะ 3: `runtime.py` · `tests/test_scene_scoped_combat_wiring.py` (ใหม่ 9 เทส) ·
`tests/test_mob_combat_census_wiring.py` (1 เทสเดิมตรึงพฤติกรรมเก่าที่ COO สั่งเลิก — ย้ายไปพิสูจน์
ด่านเดิม "anchor เก่าห้ามข้ามฉาก" ผ่านฉาก 2 ที่ยังไปถึงได้จริง)

## ② พิสูจน์แล้ว (ชั้น wire/DB · headless บน cloud)

- [วัดแล้ว] ตัวละครฉาก 2 ตี `0x2033`: `MOB_COMBAT_ANNOUNCE`+`BAR`, damage 964, HP 3857→2893
- [วัดแล้ว] ฆ่า `0x2033` จบใต้ใบ `widen-death-scope-bg0002` ของฉากเอง (register จดตาย scene='Bg0002')
- [วัดแล้ว] ฉาก 9999: ปฏิเสธด้วย event ชื่อชัด ไม่มี frame ไม่มี hit count ไม่มี scene swap
- [วัดแล้ว] ฉาก 5: roster ว่าง silence เดิม · [วัดแล้ว] เทสเดิม `_set_balance` กลางฉากไม่ถูกล้าง
  (sync เปิดใหม่เฉพาะตอน folder เปลี่ยนจริง)
- สวีตเต็ม 4,648 passed 0 failed 323 skipped เขียว(cloud sanity) · `verify_hypothesis_ledger` PASS 47
- gate เต็มยังไม่รัน — รอ Actions บน PR #261 ตามปกติ

## ③ ผลพวงที่ต้องรู้ (เขียนในจดหมายถึงสาย B ด้วย)

- provenance ของการฆ่าใน bg0001 เปลี่ยนตามกฎ LETTER-PICK ของ COO 0848 ข้อ 1:
  จากสตริง `COO-RULING-20260827-1350` ที่ hardcode → ใบ 916-training-iron-man (09:55) ที่**เก่ากว่า**ชนะ
  ตรงกับ `PIN_WIDENING_RULING` ที่ทรีตรึงอยู่แล้ว — ไม่ใช่ผลข้างเคียง เป็นคุณสมบัติที่ COO ต้องการ
- ledger/AI state ของฉากรีเซ็ตเมื่อเปลี่ยนฉาก (มอนของฉากเก่าหายไปจากโลกผู้เล่น ไม่ใช่ถูกรีเลข)
- `GT-132` ปลดบล็อกได้เมื่อ PR #261 merge (COO 0848 ข้อ 4) — ใบเป็นของสาย B สายนั้นปลดเอง

## ④ COO-DECISION 1344 (ตอบใบ chief 1332) — ทำครบตามคำเคาะ

- กติกา "restore ทั้ง DB ห้ามบางตาราง" ลง `AGENTS.md` §7 แล้ว (pf_bridge PR รอบนี้)
- ใบเครื่องมือกู้ attended-only เข้า `GAME_TEST_QUEUE.md` (เงื่อนไข: เจ้าของรันเอง เซิร์ฟเวอร์ปิด
  พิมพ์ diff หยุดถามก่อนเขียน + แก้ข้อความ `PermissionError` ที่ชี้ HYP-PF-008 ผิดเรื่อง รวมใบเดียวกัน)
  คิวปกติหลัง M5 ไม่ด่วน

## ⑤ จดหมายที่บริโภครอบนี้ (stub ครบ)

0744 (กำแพงสอง ชั้น B) · 1234 (ตัวอ่านของสาย A พร้อมใช้) · 1305 (สาย B ตอบ ni2wh2) ·
1344 (restore rule) — ใบ ASK-COO ของสายอื่นไม่แตะตามกฎ "ใครเปิดใบคนนั้นบริโภค"

## ⑥ WIRED

รอบนี้วัด emission จริงของเลน combat บน production path: บูต headless ฉาก 2 แล้ว console มี
`MOB-COMBAT-001 hit ... damage announced -964` + เฟรม announce/bar จริง [วัดแล้ว] ·
census ตอนนี้พิมพ์ `MOB_DEATH_WIDENING_COVERAGE` เพิ่มทุกบูต (เทสตรึงกับบรรทัดของโมดูลเอง) ·
ตัวเลข WIRED v2 เต็มกระดานล่าสุดยังเป็นของ R224 — รอบนี้ไม่ได้วัดใหม่ทั้งกระดาน

## ⑦ pf-adversary หักได้จริง — แก้ครบก่อน push

- **D1 (HIGH · วัดแล้วพร้อม control ก่อนแก้)**: ไป-กลับฉาก (เกต 1↔278 debug ของ BUILD-002) ⇒ ledger
  เปิดใหม่เต็ม HP แต่ death register (per identity+scene, อยู่ข้ามฉากโดยเจตนา) ยังจำศพ ⇒
  `repopulation_entries` ปฏิเสธ**ทุก** recompose ตลอด session + ศพรับดาเมจต่อได้ — ของใหม่จากดิฟรอบนี้เอง
  **แก้แล้ว**: เปิด ledger ใหม่แล้ว rehydrate ศพจาก register (identity ตายของฉากนั้น → HP 0)
  กลับเข้าฉาก = สภาพเหมือนไม่เคยออก · เทส round-trip ใหม่ตรึง + mutant ยืนยันตาย
- **D3**: mutant "เปิด ledger/AI register คนละ load" รอด ⇒ เทสใหม่ป้อน roster ต่างกันต่อ call ฆ่าแล้ว [วัดแล้ว]
- **D4**: คอมเมนต์ใหม่ของ chief เองเท็จอีกแบบ (`ruling_for` **raise** สำหรับมอนไม่มีใบครอบ ไม่ใช่คืน None) — แก้แล้ว
- **D2 (เปิดเผย ไม่แก้ในใบนี้ — คนละเรื่องกับใบ)**: hit ใน `Bg0002` ยังส่ง bar/dying/dead เป็น one-entry frame
  (สาขา census ของ Bg0002 ไม่ตั้ง population anchor โดยเจตนา ⇒ เลน recompose ของ RE-092 ไม่ทำงานที่นั่น)
  ชั้น wire ถูกต้อง แต่ตามหลักฐาน RE-092 ไคลเอนต์อาจลบ actor อื่นทั้ง 96 ตัวจาก registry ตอนตีครั้งแรก —
  **GT-132 ต้องกำกับความเสี่ยงนี้ตอนปลดบล็อก** (แจ้งสาย B ในจดหมายแล้ว) · recompose ฝั่ง Bg0002 = งานต่อ
- **D5 (ส่งต่อสาย B)**: docstring/pin ค้างยุคก่อน `ruling_for` มีผู้เรียกจริง — `mob_death.py:259-260` ·
  `ruling_for` docstring ("NO production caller today") · `describe_widening_coverage` docstring ·
  `tests/test_mob_death_wired_widening.py:59-61` · `diag_multi_object_wiring.RUNTIME_WIRING_PATCH` ข้อ (2)
  ทั้งหมดเป็นไฟล์เขตสาย B — แจ้งในจดหมายแล้ว ไม่แตะแทน
- **D6 (แฝง ยังไม่ถึงวันนี้)**: key ด้วย folder vs scene_id (วันที่ฉาก 186/`Bg1001` ถูก address) ·
  `display_name` ใน UNKILLABLE line ไม่ผ่านตัวกรอง cp874 (วันนี้ ASCII ล้วน [วัดแล้ว]) · loot cell ข้ามฉาก

หลังแก้: สวีตเต็ม **4,650 passed 0 failed 323 skipped** เขียว(cloud sanity) · ledger PASS 47 ·
functional coverage PASS 8 · mutation kill รวมรอบนี้ 7/7 (M1-M5 ของ adversary + 2 ใบใหม่)

## ตอนนี้ต้องทำอะไรต่อ

รอ gate บน PR #261 เขียวแล้ว workflow merge เอง → สาย B ปลดบล็อก `GT-132` (พร้อมกำกับความเสี่ยง D2/RE-092 ในใบ) แล้วเรียกผู้เทสได้
