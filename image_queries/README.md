# image_queries/ — คิวย้อนกลับสำหรับถามข้อเท็จจริงจากอิมเมจ

**สร้างโดย chief รอบ 93 (2026-08-20 ~02:3x)** ตามสเปกของผู้เทส
(`notes_to_chief\consumed\20260820_0115_SPEC-image-query-queue.md`) ซึ่ง Panya สั่ง "ทำได้เลยตอนนี้"

## ทำไมมันมีอยู่

`GameClient.local.bin` **จะไม่ขึ้น cloud ตลอดกาล** (คำตัดสิน Panya: แกะ binary = งาน local ถาวร)
⇒ chief ที่รันอยู่บน cloud ต้องมีช่องทางถามข้อเท็จจริงระดับไบต์ ไม่งั้นเลนนั้นตัน

⭐ **คุณสมบัติที่ทำให้มันคุ้ม: อิมเมจตรึงด้วย sha แล้ว ⇒ คำตอบทุกใบถูกต้องถาวร ไม่มีวันหมดอายุ**
⇒ คำตอบที่ตรวจแล้วถูกยกเข้ารีโปที่ `Pirate Force ServerProject\derived\image_facts\<subsystem>\`
และกลายเป็น dossier ที่โตขึ้นเองตามความต้องการจริง ยิ่งใช้ยิ่งถามน้อยลง

## โครง

```
pending\    <- chief เขียนคำถามลงที่นี่ (ไม่ต้องถือธงใด ๆ)
answered\   <- ตัวรันฝั่ง local เขียนคำตอบ + ย้ายคำถามมาไว้คู่กัน
blocked_log.tsv  <- จดทุกครั้งที่อยากได้ข้อมูลจากอิมเมจแล้วไม่มี (เริ่มจดตั้งแต่วันแรก)
```

## รูปแบบคำถาม `pending\<YYYYMMDD_HHMM>_<subsystem>_<seq>.query.json`

```json
{
  "id": "20260820_0230_deathchain_001",
  "asked_by": "chief round 93",
  "subsystem": "deathchain",
  "why": "หนึ่งประโยคว่าเลนไหนติดอยู่ ถ้าไม่มีคำตอบนี้",
  "kind": "bytes",
  "image_sha256_expected": "9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623",
  "args": { "offset": 4439408, "length": 64 }
}
```

`kind` ที่สเปกกำหนด: `bytes` · `hash` · `search` · `strings` · `disasm` · `xref`
(ลำดับที่จะ implement: `bytes` + `hash` + `search` ก่อน — สามอันนี้ครอบงานส่วนใหญ่)

## การ์ดที่ห้ามข้าม

1. `length` ต่อคำถามไม่เกิน **4096 ไบต์** สำหรับ `bytes` และ `disasm`
2. เพดานรวมต่อวัน **64 KB** — **ถ้าชนเพดาน = สัญญาณว่าออกแบบผิด ไม่ใช่สัญญาณว่าต้องขยายเพดาน** ให้หยุดแล้วคุยกับ Panya
3. ทุกคำตอบต้องฝัง sha256 ของอิมเมจ · ไม่ตรงกับ `image_sha256_expected` -> ตอบ `MISMATCH` ไม่ตอบข้อมูล
4. **ตรวจ `answered\` และ `derived\image_facts\` ก่อนถามเสมอ** — อิมเมจไม่เปลี่ยน คำตอบเก่าใช้ได้ตลอด
5. ตัวรัน **ไม่ตีความ** — คืนข้อเท็จจริงดิบ การตีความเป็นงาน chief
6. **ASCII ล้วนใน console** (บทเรียน cp874 รอบ 86/93)

## สถานะ ณ ตอนนี้ (อย่าอ่านเกินนี้)

- โครงไฟล์ + `blocked_log.tsv` = **มีแล้ว**
- `tools\pf_image_query_runner.py` = **มีแล้ว — commit `dbcbf8f` (เขียนโดยรอบ 94 · gate+commit โดยรอบ 95, job 154)**
  - kinds ที่ใช้ได้จริง: `bytes` · `hash` · `search` — ที่เหลือ (`strings`/`disasm`/`xref`) refuse ด้วยชื่อ `kind_not_implemented`
  - เทส 12 ใบ (`tests\test_image_query_runner.py`) เห็น refusal แดงครบทุกชื่อบนอิมเมจปลอม · **fresh clone รันผ่าน 12/12**
  - วิธีรันฝั่ง local: `py -3 tools\pf_image_query_runner.py --image <GameClient.local.bin> --pending <pending> --answered <answered>`
  - ตัวรันเขียน `usage_log.tsv` ใน answered\ เอง — เพดานรายวันนับข้ามรันด้วยไฟล์นี้
- **ยังไม่เคยถูกใช้จริงแม้แต่ใบเดียว** ⇒ เพดาน 4 KB / 64 KB เป็น **ข้อเสนอ ไม่ใช่ผลวัด**
