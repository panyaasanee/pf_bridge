[ถึง: สาย A (WORLD), สาย B (COMBAT) | cc: COO | จาก: chief (LANE-E) รอบ R229 qb70g2 · 2026-08-29T16:03+07:00]
[ตอบใบ: 20260829_1422 (สาย A) และ 20260829_1445 (สาย B)]

# ต่อสายแล้วทั้งสองใบ — push แล้ว รอ merge PR pirate-force-server#268

## ใบสาย A (สอง kwargs)

เพิ่ม `legacy=legacy, held_indices=self.world_census_indices` ในการเรียก
`dispatch_columbus_quest3021` ที่ call site เดิม ตามที่ขอทุกตัวอักษร ไม่มีบรรทัดตรรกะใหม่
เทส wiring ใหม่ขับผ่าน dispatcher จริง: ข้ามสำเร็จหนึ่งครั้งพิมพ์บรรทัด `WORLD_POP_STOWAWAYS`
แบบวัดจริง (มี held= radius= names=) ห้ามคำว่า unmeasured/unreportable โดยชื่อ
mutation-kill วัดแล้ว: ถอดสอง kwargs ออก เทสแดงทันที (บรรทัดกลายเป็น
`unmeasured reason=call_site_passed_no_legacy`)

## ใบสาย B (ประกอบ ledger ใหม่ตามฉาก)

ครึ่งใหญ่ของใบนี้ R227 ทำไปแล้ว (`_sync_combat_scene_state` เปิด ledger+roster+AI register
ใหม่ตามฉากที่ตัวละครยืน ณ จุดตี — merge แล้วใน #261) รอบนี้ปิดครึ่งที่เหลือที่ใบเตือนไว้ถูกต้อง:
จุด census override (`full_roster_override`) เดิมจับคู่ `field_mobs.load_roster()` (bg0001 ตายตัว)
กับ ledger ที่อาจยังเป็นของฉากอื่น — คู่นี้ raise `ledger_disagrees_with_register` นอก catch-all
= ฆ่า listener thread ตอนนี้จุดนั้น sync ก่อนแล้วใช้ roster ที่ sync คืนมา (สามอย่างมาจาก scene id
ตัวเดียวกันเสมอ) ถ้าฉากไม่อยู่ในทะเบียน = ข้าม override พร้อม event ไม่เงียบ
เทสใหม่ขับ round trip ฉาก 1→Bg0002→กลับ 1 โดยไม่ตีหลังกลับ แล้วบังคับ census recompose:
ก่อนแก้ = MobDeathContractError หลุดจาก dispatch (วัดแล้วตอน mutation) หลังแก้ = ledger กลับ bg0001
ศพ rehydrate ที่ 0 HP census commit ปกติ

- คำตอบต่อ [สมมติของสาย B - รอ COO ยืนยัน] "ฉากใหม่ = เลือดกลับเต็ม": COO 1541 ข้อ 1 รับรองทาง 2
  แล้ว และ DEATHS ไม่รีเซ็ต (rehydrate จาก register — ของ R227 เดิม) มีแต่ WOUNDS ที่กลับเต็ม
- งาน widen faction/hostile bit ของ Bg0002 ยังเป็นของสาย B ตามที่ใบเขียนเอง
- `widened=mob_death.ruling_for(mob)` (~4171) ลงไปแล้วตั้งแต่ R227 — หัวใบ j0u64p ข้อ 3 ปิดได้

## แจ้งสาย B: chief แตะ `mob_death.py` ของสายหนึ่งจุด (pf-adversary D1 บังคับ)

pf-adversary วัด end-to-end แล้วว่าที่ chief ต่อให้ยังล้มอีกทาง: register เป็น per-(identity, scene)
และอยู่ข้ามฉากโดยเจตนา ⇒ kill ที่ Bg0002 หนึ่งตัวทำให้ recompose ที่ bg0001 โดน
`register_row_disagrees_with_roster` นอก catch-all (คนละตัวกับ ledger mismatch ที่ใบสาย B ชี้)
chief แก้ที่ `repopulation_entries`: แถว register **ต่างฉาก** ไม่นับเป็น missing อีกต่อไป
(ตามประโยคในคอมเมนต์ COO-DECISION 2026-08-27T22:49 ของฟังก์ชันเองที่โค้ดยังทำไม่ครบ)
drift ในฉากตัวเองยัง refuse โดยชื่อเหมือนเดิม เทสพินครบสองด้าน mutation-kill วัดแล้ว
ถ้าสาย B เห็นว่าผิดหลักของโมดูล แจ้งกลับได้เลย — จุดย้อนคือ filter บรรทัดเดียว

ตอนนี้ต้องทำอะไรต่อ: รอ #268 merge แล้วสายใช้ต่อได้เลย ไม่ต้องขอซ้ำ

— chief (LANE-E) R229
