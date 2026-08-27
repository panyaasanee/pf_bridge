# notes_to_chief/ — กล่องจดหมายถึง chief (ไม่ต้องรอ LOCK)

**เริ่มใช้ 2026-08-18 ~15:0x ตามคำสั่ง Panya** — เกิดจากปัญหาจริง: เซสชันหลักต้อง poll รอ LOCK
เป็นสิบนาทีเพื่อเขียน markdown 30 วินาที (เปลืองโทเคนฟรี ๆ) และเคยอ่านผิดว่า chief ตาย
จนไป takeover ทั้งที่รอบนั้นยังทำงานอยู่ (รอบ 76)

## สัญญาการใช้งาน

**ผู้เขียน = เซสชันหลัก (attended) หรือใครก็ตามที่ไม่ได้ถือ LOCK**
- หย่อนไฟล์ `<YYYYMMDD_HHMM>_<หัวข้อ>.md` ลงโฟลเดอร์นี้ **แล้วจบ ไม่ต้องขอ LOCK ไม่ต้องรอใคร**
- ใช้กับ: คำตัดสินจาก Panya · ผลเทสรอบใหญ่ · ข้อสังเกต/บทเรียน · คำขอให้ chief ทำอะไร
- เขียนให้ครบในตัว (ใคร/เมื่อไหร่/ช่องทาง/เนื้อหา) เพราะ chief จะยกไปแปะใน ledger ตรง ๆ

**ผู้อ่าน = chief (ทุกรอบ ตอนที่ถือ LOCK อยู่แล้ว)**
- อ่านทุกไฟล์ในโฟลเดอร์นี้เป็น **ขั้นแรกของทุกรอบ** (ก่อน inbox ด้วยซ้ำ)
- ย้ายเนื้อหาไปไว้ที่ถูกที่: `CHIEF_CONTINUATION.md` (คำตัดสิน/นโยบาย/บทเรียน) หรือ
  `GAME_TEST_QUEUE.md` (ผลเทส) — **chief เป็นคนเขียนไฟล์ใหญ่คนเดียว = ไม่มีวันชนกัน**
- เสร็จแล้วย้ายไฟล์ไป `notes_to_chief/consumed/` (เก็บไว้ ไม่ลบ) พร้อมจดใน release note ว่าบริโภคอะไรไป

## ทำไมต้องมี

`LOCK.txt` มีไว้กัน **bridge / พอร์ต server / หน้าต่างเกม / git commit** ซึ่งชนกันจริง
ส่วนไฟล์ประสานงานชนกันแค่วินาทีที่เขียน — ไม่ควรทำให้ใครต้องหยุดรอเป็นชั่วโมง
กล่องจดหมายนี้แยกสองเรื่องนั้นออกจากกัน


## .CONSUMED.txt naming standard (COO-DECISION 2026-08-28T00:43+07:00)

The stub that marks a letter consumed is named `<original filename in full>.CONSUMED.txt`
— append the suffix to the WHOLE original name, extension included, never strip `.md`
first. Two examples:

- `20260827_2305_KA1A-NUDGE-example.md` -> `20260827_2305_KA1A-NUDGE-example.md.CONSUMED.txt`
- `some_note.txt` -> `some_note.txt.CONSUMED.txt`

This is a rule any lane can generate with one string concatenation (`filename +
".CONSUMED.txt"`) without parsing the extension first — the extension-stripping form
(`20260827_2305_KA1A-NUDGE-example.CONSUMED.txt`) is what most existing stubs happen to
use (167 of ~187 as of this decision) but was never a written rule, and it is ambiguous
for a source file that does not end in `.md`. Existing stubs in either form are NOT
renamed retroactively — check both forms for now (`test -f "<candidate>.CONSUMED.txt"`
for either full-name or extension-stripped `<candidate>`) until the older form ages out.
New stubs from this decision forward use the full-name form only.

**Known gap, not yet resolved**: a letter addressed to more than one lane (e.g. "ถึง:
LANE-GM, chief, LANE-A") can only hold ONE stub at this path. If two different addressees
each act on their own portion of the same letter in different rounds, the second one to
arrive should NOT overwrite the first stub (that erases the first consumer's record) —
record its own consumption in its own round file / reply letter instead, and leave the
existing stub as-is. Watched round R202 (chief) hit this against a LANE-GM stub already
covering `20260827_2305_KA1A-NUDGE-*`; see `rounds/R202_9b6zl6_*.md`.

**Also note the 100-character filename cap (§9, this project's Windows-path limit)**: the
full-name form is longer than the extension-stripped form by the length of the stripped
extension (usually 3 chars for `.md`) — a source filename already near 97 characters will
push its full-name stub over the cap. When that happens, keep the stub in the
extension-stripped form for that one file rather than violate the cap, and say so in the
round file; do not silently pick one or the other without a note.

## Archive note 2026-08-27
Letters dated up to 2026-08-25, consumed letters of 2026-08-26 and all FROM_CHIEF_* up to 2026-08-26 were moved verbatim (same file names) to `archive/notes_to_chief_2026-08-19_to_26/`; the consumed/ copies to `archive/notes_to_chief_consumed_to_2026-08-26/`. Nothing was deleted. References by old path resolve there.
