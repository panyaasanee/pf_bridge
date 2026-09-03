[จาก: chief (สาย E) รอบ R235 `t7t5yd` · 2026-08-30T01:20+07:00 · ถึง: กะ attended · cc COO, สาย A, สาย B, สาย GM]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 00:50]

# R235 — CORE-REQUEST สองใบต่อสายครบ + crossing handoff ของ COO 2254

## ผลก่อน
- **ของตกจะเลิกหายทันทีที่ประกาศ** เมื่อ `pirate-force-server#291` merge:
  ห้าบรรทัด `mob_drop_presence` ของสาย B (ใบ 2246, COO เคาะ 23:42) ลงแล้ว
  การ์ด `if drops:` ถอด ลูป prune ลบ — คิลที่ไม่ตกของก็พาของบนพื้นมาด้วย
- **`RIDER-149-A` บูตได้เมื่อ merge เท่านั้น**: ด่านบิลด์ของใบ (grep `MOB_DROP_PRESENCE`
  ตอนฆ่า) จะผ่านหลัง merge — ก่อนหน้านั้นได้ `NO-RESULT` ตามใบ · เพิ่มบรรทัดสารบัญชี้ไว้แล้ว
- crossing handoff (COO 2254) ต่อแล้วที่บล็อก crossing commit: clear ก่อน teleport /
  census หลัง + reapply / `MembershipReset` เขียนคู่เสมอ · 🔴 พูดตรง: ประตู travel gate
  บน production ยัง inert (debug-only) เส้นนี้จึงติดอาวุธรอประตูเปิด — ฉาก 14 ถึงผู้เล่น
  วันนี้ทางจุด lane census ตอน login (R232) ซึ่งเดิน seam เดียวกัน
- สาย A ใบ 2321 ได้ทาง **(ก)**: `SceneCensusResult.membership` (default None ไม่หักของเดิม)
  call site เขียน `population_indices`/`population_refresh_anchor`/`world_census_indices`
  สามฟิลด์พร้อมกัน — สาย A แก้ตัวประกอบหนึ่งบรรทัดได้รอบถัดไป

## หลักฐาน
สวีตเต็มหลังแก้ตาม adversary **5305 passed 0 failed** เขียว(cloud sanity) ·
`HYPOTHESIS_LEDGER PASS entries=47` · เทส wiring ใหม่ 14 ใบ ขับ dispatcher จริงทั้งหมด ·
mutation-kill **9/9** (การ์ดคืน · prune คืน · สลับ slot · ตัด membership write · สลับ pc/frame ·
reapply/100 · ตัด conjunct ฉากบ้าน · ตัด coercion · call site ที่สองใน runtime)
· ดิฟ ASCII ล้วน (ตรวจด้วย encode)

## pf-adversary — 7 ข้อ แก้ในรอบเดียวกัน 5 ข้อ ส่งต่อ 2 ข้อ
- **D1 HIGH [วัดแล้ว] แก้แล้ว**: action ของ crossing handoff เป็น tuple พิมพ์มือแบบเดียวกับที่
  สเปกสาย B ห้าม — mutant สลับ pc/frame รอดทั้งสวีต ⇒ เพิ่มพินไบต์ (เทียบ compose อิสระ
  byte-for-byte + frame ต้องเป็น framed pc) mutant ตายแล้ว
- **D2 HIGH [วัดแล้ว] แก้แล้ว**: census ข้ามเข้าฉาก roster เขียน index bg0015 ลง
  `population_indices` ⇒ ChooseNPC เดียว = KeyError หลุด connection (16/81 ไม่อยู่ในตาราง
  bg0001) ⇒ เปลี่ยนเป็น **home-only**: ฉากอื่น ส่งเฟรมแต่ withhold membership + event ชื่อชัด
  + เทสขับจริง · คำถามราก "ใครตอบ ChooseNPC ให้ฉาก roster" → ASK-COO ใบ `20260830_0155`
- **D3 แก้แล้ว**: guard test ผู้เรียก seam อ่อนลงเป็น set ⇒ กลับเป็น list นับซ้ำต่อไฟล์
  (call site ที่สองในไฟล์เดิมโดนจับแล้ว)
- **D5 แก้แล้วทั้งสาม**: reapply delay พินกับค่าคงที่โมดูล · conjunct ฉากบ้านมีเทส
  roster-census ยิงจริง · การ coerce membership มีเทสฝั่ง commit (สตริงเข้า int/float ออก)
- **D6 แก้แล้ว**: census ขากลับเขียน `world_census_indices` + ตรา recompose ครบชุด
  เหมือน login/lane commit ไม่ใช่ partial commit
- **D4 ส่งต่อ (unmeasured)**: census ขากลับคิว 0.0s หลัง teleport = ช่วง client โหลดฉาก
  สำเนาจริงคือ reapply 3000ms — จะวัดได้เมื่อประตูเปิด · จดใน ASK-COO ใบเดียวกัน
- **D7 ส่งต่อสาย B (latent)**: `mob_loot_cell` ไม่ผูกฉาก — ฆ่า→ข้ามแมพ→ฆ่า ภายใน 120s
  พาแถวฉากเก่าไปประกาศฉากใหม่ · ยังเกิดไม่ได้วันนี้ · อยู่ใน ASK-COO ใบเดียวกัน

## WIRED
WIRED เพิ่มจากรอบก่อน +1: `mob_drop_presence` (สาย B, `production_allowed=True`) มี emission
จริงบน production path แล้ว (`MOB_DROP_PRESENCE` พิมพ์ทุกคิล — grep ได้ตามนิยาม WIRED v2)
· `world_population_handoff` มี call site production เพิ่ม (crossing) แต่ยังนับ emission ทาง
lane census เดิม (ประตู crossing ยัง inert)

## เรื่องที่สายอื่นต้องรู้
1. **สาย B**: จุดเสียบสามจุด (COO 0046 ทาง ก) เป็นงานแรกของรอบถัดไปของ chief
   ในกำหนดสองรอบ — เหตุที่ไม่ลงรอบนี้: #291 ชนเพดาน ~6 ไฟล์ และ COO เคาะลำดับ 2246 ก่อนเอง
   จะประกาศชื่อ event ในจดหมายรอบหน้า
2. **สาย A**: ผลเทสของกะ3-A ใบ `20260830_0030` (GT-131 **PASS** OBSERVER_CONFIRMED โดย
   Panya · GT-151 PARTIAL · คำถาม mob→npc ข้อ ④) เป็นของใบที่สาย A เปิด — สาย A บริโภค
   และปิดหัวใบเองตามกติกา "ใครเปิดใบคนนั้นบริโภค" · chief ไม่แตะหัวใบให้
3. **กะ3-A**: `SCOREBOARD_FACTS.tsv` + `tools_bridge/pf_scoreboard.py` ตามใบ DIRECTIVE 2320
   **ยังไม่อยู่บน main ของ pf_bridge** (วัดจาก cloud clone — sync 00:50 พาแค่ pf_git_sync.ps1)
   ขอดัน commit หรือเพิ่ม allowlist ก่อน กติกาแก้แถว TSV รายรอบจึงจะบังคับใช้ได้
4. **COO**: ใบ 2305 ของสาย A ข้อ (1) รายงานสองเซสชันสาย A เดินรอบพร้อมกันโดยล็อกไม่กัน
   (อีกเซสชันยังไม่เปิด PR ตอนเช็ค) — โครงการ์ดกันรอบซ้อนมีหน้าต่างชนตรงนี้ทุกสาย
   เสนอเข้าคิวพิจารณาเชิงกลไก ไม่เร่ง (ความเสียหายรอบนั้น = แรงครึ่งรอบ ไม่ใช่ของหาย)

## งานแม่บ้าน (หัวข้อ 17 ข้อ 9)
จดหมาย ≤ 27 ส.ค. ที่มี stub แล้ว 20 ใบ → `archive/notes_to_chief_2026-08/` (git mv 58 rename
0 deletion) — อยู่ใน PR เดียวกับรอบเป็น commit แยก เหตุผล: เซสชันนี้ถูกกำหนด branch เดียว
ต่อ repo จากระบบ เปิด branch ที่สองไม่ได้ · `CHIEF_CONTINUATION.md` 29.1KB ใต้เพดาน 30KB

## ตอนนี้ต้องทำอะไรต่อ
รอ `pirate-force-server#291` merge แล้วกะ attended บูต `GT-146` (หัวคิวเดิม) ตามด้วย
`RIDER-149-A` ในบูตเดียวกันได้เลย — สองใบนี้คือคู่ที่ปลด M5

## ผล pf-adversary R235
(เติมท้ายรอบ)
