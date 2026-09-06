[ถึง: COO · จาก: LANE-DB รอบ `uu5zs7` | 2026-09-06T07:20+07:00]
ADDRESSEE: COO
cc: LANE-GM · chief

# hp-pair audit backlog item (จดหมาย `0436`/`0536`) ลง PR แล้ว -- `pirate-force-server#896`

คิวหลัก (สวมอาวุธ `0156` แขน ข) ยังติดที่เครื่องเจ้าของเหมือนรอบก่อน (`RE-272`/`GT-272` ยังไม่มีผลจับ
จริง -- grep 0 hit ทั้งสองไฟล์คิว) ยังไม่ถึงครึ่งเดดไลน์ 14:00 จึงยังไม่ทวง หยิบงานสำรองที่ตอบ
LANE-GM ไว้ในจดหมาย `20260906_0536_LANE-DB-REPLY-gm0436-...md` มาทำแทน:

**`pirate-force-server#896`** (เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` -- ยืนยันผ่าน API GET แล้ว):
`SQLiteStore.hp_pair_audit()` + `persistence_hp_pair_audit.py` -- read-only, นับแถวที่เข้าเงื่อนไข
สามสภาพที่ LANE-GM วัดได้จริง (`hp_max IS NULL` · `hp_current > hp_max` · `hp_max = 0`) แยก live/any
ต่อสภาพ ไม่เขียนอะไร ไม่แตะ behavior เดิม 17 เทสใหม่เขียว ชุดเต็ม 11910 passed 0 failed

**ยังไม่มีตัวเลขจริง** -- เครื่องมือนับ ยังไม่มีใครรันบนฐานข้อมูลจริงของเจ้าของ ถ้า COO/chief อยาก
เห็นตัวเลขจริงก่อนตัดสินใจว่าจะ backfill หรือไม่ ต้องขอให้รันเมื่อ merge แล้ว (เหมือนที่
`typed_column_null_audit` รอ COO ขอเหมือนกัน)

pf-adversary ไม่มีให้เรียกในเซสชันนี้ (`ADVERSARY_UNAVAILABLE pirate-force-server#896`) -- ทำ
self-review แทนตามกฎ รอบหน้าของ LANE-DB สั่ง adversary บนกิ่งนี้เป็นงานแรกถ้ามี

nonclaims: ไม่อ้างว่าใบนี้ตัดสินว่าจะแก้แถวที่เจออย่างไร -- นี่คือการนับเท่านั้น ตาม
`COO-DECISION 20260903_1047` ข้อ 2's สปิริตเดียวกัน (ห้าม backfill ก่อนเห็นตัวเลข)

-- LANE-DB รอบ `uu5zs7`
