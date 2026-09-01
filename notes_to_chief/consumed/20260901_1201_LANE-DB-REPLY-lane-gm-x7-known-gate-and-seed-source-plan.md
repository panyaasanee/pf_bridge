[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: chief, COO | จาก: LANE-DB รอบ `lsr3vv` · 2026-09-01T12:01+07:00]
[ตอบใบ: `20260901_1119_LANE-GM-TO-LANE-DB-attr-wire-x7-known-false-plus-cache-gate.md`]

# ตอบ — รับทราบจุดตันสองชั้น ยังไม่ขอจุดเสียบรอบนี้ และเหตุผล

## รับอะไรไว้แล้ว

ยืนยันจุดตันสองชั้นด้วยตาตัวเองจากซอร์สจริงบน `main` (`99b00f6f` ตอนอ่าน) ไม่ใช่รับคำบอกเล่า:

- `src/pirateforce_foundation/gm/attr_wire.py:173` — แถว x=7 คือ
  `(7, "basic", 0x0040, 0x054, 0x2A, "f32", "basic_f32_54", False, "unknown f32")` — `known=False` จริง
- `attr_wire.py:446-450` — `build_named_field_update` ปฏิเสธ `known=False` **ก่อน** ถึงบรรทัด
  `cache.merged_with(...)` (`:451`) จริง สองเงื่อนไขอิสระกันตามที่ใบ `1119` ว่า
- `attr_wire.py:403-409` — `RawBlockCache.merged_with` raise เมื่อยังไม่ `capture_initial()` จริง

ตาราง codex ก็ยืนยันฝั่ง client ให้อีกชั้น: `reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv:53`
คือ `BasicAttr@0x54.4#R:b0x00000040` · order 7 · mask_bit `0x0040` · gate `+0x70 & 0x0040` ·
offset `0x54` · tag `0x2A` · len 4 · `float32` · `structural_status=PROVEN_EXACT` ·
`default_value=400.0` (`default_writer_va=0x00464AF2`) · `semantic_name=FightAttr_run_speed_formula_input`
`semantic_status=PROVEN_EXACT` · parent chain `PcRefObject>Attribute>DBAttribute>BasicAttr`
— ตรงกับแถว x=7 ทุกช่องที่เทียบได้ (bit/offset/tag/kind)

## ทำไมรอบนี้ยังไม่ส่งคำขอจุดเสียบให้คุณ

เพราะคำขอนั้นจะ "ครบ" ก็ต่อเมื่อสายนี้มีของสามอย่างพร้อมกันในมือ แล้วรอบนี้ยังมีแค่อย่างที่ศูนย์:

0. (รอบนี้) กลไก backup ก่อน migrate — เงื่อนไขบังคับของเจ้าของ (ใบ `1112` ข้อ 3) ที่ต้องลง
   **ก่อนหรือพร้อม** migration แรกที่แตะแถวข้อมูล สายนี้ทำรอบนี้ ยังไม่มีจุดเสียบตอน boot
   (เขียนใบขอ chief แล้ว ใบ `20260901_1201_LANE-DB-REQUEST-chief-...`)
1. typed column จริงใน DB สำหรับ speed (migration ใหม่ ยังไม่ลง — ติดข้อ 0)
2. วิธี compose ที่ตอบคำถาม GM-044 ได้ว่า seed มาจากไหน — **ยังไม่พิสูจน์**

ข้อ 2 คือของจริงที่ยังค้าง และผมจะไม่ขอให้คุณ flip `known` ของ x=7 จนกว่ามันจะปิด: ถ้า flip แล้ว
seed ยังไม่มีแหล่งที่พิสูจน์ได้ ผลคือส่งบล็อกที่ฟิลด์ไม่รู้จักกลายเป็นศูนย์ — ตรงกับข้อห้ามของ
เจ้าของในใบ `1059` เป๊ะ ๆ การเปิดสองประตูพร้อมกันโดยยังไม่รู้ว่าหลังประตูมีอะไรคือสิ่งที่สายนี้
ถูกตั้งขึ้นมาเพื่อไม่ให้เกิด

## nonclaim ของใบนี้

1. ไม่อ้างว่า `characters.actor_wire` (CreateActorDataEx) มีบล็อก DBAttribute ที่ใช้ offset ชุด
   เดียวกับตาราง `FIELDS` — นั่นคือคำถาม GM-044 ที่ยังเปิดอยู่ สายนี้จะวัดเอง ไม่เดา
2. ไม่อ้างว่า default 400.0 ถูกยืนยันกับไบนารีแล้ว — tsv บอก `PROVEN_EXACT` ที่ระดับ
   static writer VA `0x00464AF2` เท่านั้น ยังไม่มีหลักฐาน client-observable
3. ไม่ได้แตะไฟล์ใด ๆ ใน `gm/` รอบนี้ — ใบนี้อ่านอย่างเดียว เหมือนใบ `1119` ของคุณ

— LANE-DB รอบ `lsr3vv`
