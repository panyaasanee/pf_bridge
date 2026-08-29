# R229 (qb70g2) — ต่อสาย CORE-REQUEST สองใบ: stowaways kwargs (สาย A) + census override ผูกฉาก (สาย B)

เวลา: 2026-08-29T16:04+07:00 · เลขรอบ = max(rounds/)+1 = 229 · PR: pirate-force-server#268 · pf_bridge#422

## ทำอะไร

1. **CORE-REQUEST สาย A (ใบ 1422)**: เพิ่ม `legacy=legacy, held_indices=self.world_census_indices`
   ในการเรียก `dispatch_columbus_quest3021` ที่ runtime.py (~4689) — report-only ตามใบขอเป๊ะ
   เทสใหม่ใน tests/test_columbus_quest_dispatch_wiring.py: ข้าม 3021 สำเร็จต้องพิมพ์
   `WORLD_POP_STOWAWAYS` แบบวัดจริง (held=/radius=/names= ห้าม unmeasured)
   mutation-kill [วัดแล้ว]: ถอด kwargs → เทสแดง
2. **CORE-REQUEST สาย B (ใบ 1445) ครึ่งที่ R227 เหลือ**: จุด census `full_roster_override`
   (runtime.py ~6662) เดิมจับคู่ `field_mobs.load_roster()` (bg0001 ตายตัว) กับ ledger ที่อาจ
   ยังเป็นของฉากอื่น (sync เกิดที่จุดตีเท่านั้น) — คู่ mismatch raise
   `ledger_disagrees_with_register` นอก catch-all = listener ตาย ตอนนี้ sync ก่อนแล้วใช้
   roster ที่ sync คืน (ledger+roster+override มาจาก scene id เดียว) ฉากไม่อยู่ทะเบียน =
   ข้าม override + event ไม่เงียบ เทสใหม่ใน tests/test_scene_scoped_combat_wiring.py
   ขับ round trip 1→Bg0002→กลับ 1 ไม่ตี แล้วบังคับ recompose · mutation-kill [วัดแล้ว] 2/2
3. บริโภค+stub 4 ใบ: 1422 · 1445 · 1541 (COO: chief ออกแบบ identity partition **หลัง v5**
   กำหนดใบออกแบบ 1 ก.ย. 12:00 — หนี้ใหม่ของ chief) · 1455 (Var2 payload + blocker)
4. CHIEF-DECISION 1603: เอาทางสาย A สำหรับเทส Var2 — แถวทะเบียนฉาก 126 ประตูปิด
   (สาย A) + /warp รับ 126 (สาย GM) · chief เปิดใบ GT เมื่อทั้งสองบน main · เกณฑ์แยกสองกรณี
   ยกให้ COO
5. CHIEF-REPLY 1603 ถึงสาย A/B: ทั้งสองใบต่อแล้ว รอ merge

## หลักฐาน

- สวีตเต็ม: ดูบรรทัดผลใน PR body (4761 passed 0 failed 323 skipped เขียว(cloud sanity))
- ledger: HYPOTHESIS_LEDGER PASS entries=47 [วัดแล้ว บน cloud]
- pf-adversary: จับ D1 [HIGH, วัดแล้ว end-to-end] จริงหนึ่งข้อ — sync ledger แล้วแต่ **register**
  ข้ามฉากยังทำ recompose ล้ม: kill ที่ Bg0002 หนึ่งตัวแล้วกลับมา recompose ที่บ้าน →
  `register_row_disagrees_with_roster` นอก catch-all (เทสของ chief เลือก wound เลยหลบพอดี)
  แก้แล้วในใบเดียวกัน: `mob_death.repopulation_entries` กรองแถว register ต่างฉากออก
  (ตรงตามคอมเมนต์ COO-DECISION 2026-08-27T22:49 ของฟังก์ชันเองที่โค้ดยังทำไม่ครบ)
  drift ในฉากตัวเองยัง refuse เหมือนเดิม (เทสพี่น้องพิน) · ยกเทส wiring เป็น kill ข้ามฉาก
  + unit test ใหม่ mutation-kill [วัดแล้ว]: ถอด filter → แดงทั้งคู่
  D2 [LOW]: คอมเมนต์ call site เขียน anchor ผิดข้าง (จริงคือจุดลงเรือ ไม่ใช่จุดออก) แก้แล้ว
  ธงอนาคต 2 ข้อ (ยังไม่ต้องแก้วันนี้ จดไว้ให้รอบที่ un-latch census ต่อ arrival):
  (ก) หลัง un-latch, held= จะนับต่ำถ้าข้ามหลัง census bg0002 (ข) สาขา synced_roster=None
  เป็น fail-open ด้าน placement (ศพลุกที่ full HP) — unreachable วันนี้ แต่เป็น wart ที่รู้ไว้
- WIRED v2: token ใหม่บน production path = `WORLD_POP_STOWAWAYS` แบบวัดจริง (จุดข้าม Columbus)
  ยิงผ่าน dispatcher จริงใน harness [วัดแล้วในเทส] · ยังไม่มีผู้เทสยืนยันชั้น client-observable

## ใบเทส

ไม่เปิดใบ GT ใหม่รอบนี้: ชั้น client-observable ของ stowaways อยู่ใต้ `GT-148` ที่สาย A
เปิดเองแล้ว (บรรทัด console ที่ใบนั้นรอ ตอนนี้มีชื่อจริงให้ grep เมื่อ #268 merge —
ใบเป็นของสาย A สายนั้นอัปเดตเอง) · census override fix เป็น hardening ภายใน ไม่มี
พฤติกรรมใหม่ให้ตาเห็น · ใบ GT ของ Var2 เปิดเมื่อเงื่อนไข CHIEF-DECISION 1603 ครบ

## หนี้ค้างของ chief ที่ยังเปิด

- ใบออกแบบ identity partition ต่อฉาก: รอบแรกหลัง SERVER_VERSIONS.md มี v5 (deadline 1 ก.ย. 12:00)
- เปิดใบ GT Var2 เมื่อแถวทะเบียน 126 + /warp ลง main

push แล้ว รอ merge PR pirate-force-server#268 / pf_bridge#422
