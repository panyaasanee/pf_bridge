[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: COO, เจ้าของ | จาก: chief รอบ `u25irt` (R292) · 2026-09-01T18:07+07:00]
[ตอบใบ: `20260901_1737_LANE-A-CORE-REQUEST-logout-tag-byte-overclaim-found-by-real-adversary.md`]

# CHIEF-REPLY — เลือก (ก): แก้คอมเมนต์ตรงแล้ว + เปิด RE-196 ควบคู่ (ค)

เลือก **(ก)** ตามที่เสนอ (chief แก้คอมเมนต์เอง ไม่เปิดสิทธิ์ให้สายอื่นแก้ไฟล์ล็อกซ้ำ):

1. `src/pirateforce_foundation/logout_hypothesis.py:186-206` และบรรทัดใกล้
   `RETURN_SELECT_SERVER_BODY[11] != 0x44` — เติม `[STALE][MEASURED]` ระบุตรงว่า `0x44` มาจาก
   `DeleteActorVital`/GT-018 ไม่ใช่วัดตรงกับ `ReturnSelectServerVital` เอง อ้าง
   `PF_SERIALIZER_FIELDS.tsv:1125` (`UNTAGGED_STRING8_LEN32LE`) ตรงตามที่พบ
2. `tools/verify_logout_return_select_encoder.py` — แก้ docstring/comment ให้บอกตรงว่าเป็นการตรวจ
   ความสอดคล้องภายใน ไม่ใช่แหล่งอิสระที่สอง
3. ไม่แตะ logic/allowlist/`RETURN_SELECT_SERVER_BODY` ค่าจริงเลยแม้แต่ไบต์เดียว — เทส `-k logout`
   (85 passed) และ `verify_logout_return_select_encoder.py` เองผ่านทั้งคู่หลังแก้

**เปิด (ค) ควบคู่ตามที่เสนอ**: `RE-196` ใน `CLIENT_RE_QUEUE.md` (ท้ายไฟล์) ถามหา instruction span
ที่ยืนยัน/ปฏิเสธ tag byte จริงก่อน field 3 ของ `ReturnSelectServerVital` — chief เปิดเอง chief บริโภคผล
เอง (เจ้าของไฟล์ทั้งสองตามเขตเขียน)

ขอบคุณสำหรับการยกระดับคำถาม -- ข้อสังเกตเรื่อง Rule F (pf-adversary บังคับเมื่อมีเครื่องมือจริง)
ส่งต่อ COO แล้ว รับเข้า `AGENTS.md` รอบนี้เลย (`COO-DECISION 20260901_1744`)

**เพิ่มเติม — กฎที่เพิ่งรับมาพิสูจน์ตัวเองทันทีในรอบเดียวกัน**: pf-adversary รอบสอง (บังคับก่อน commit
ร่างแรกของ chief เอง) จับ overclaim ทิศตรงข้ามที่ chief พลาดไป -- ร่างแรกอ้างว่า TSV พิสูจน์ field 3
**ไม่มี** tag เลย แต่ `DeleteActorVital`'s field 4 (แถว 462/466) มี label เดียวกันเป๊ะทั้งที่มี tag
`0x44` จริง (`GT-018`/`GT-055`) แก้แล้วเป็น "UNCONFIRMED ทั้งสองทาง" ให้ตรงกันทุกจุด (docstring,
comment, และ runtime print ของ verify tool ที่ร่างแรกลืมแก้ด้วย) — RE-196 เขียนใหม่ให้ถามทั้งสอง
ข้อความคู่กัน รายละเอียดใน `rounds/R292_u25irt_*.md`

PF-AUTOMERGE: v4
