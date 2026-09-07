ADDRESSEE: LANE-K
CC: COO
FROM: LANE-UI
DATE: 2026-09-08T05:02+07:00
ROUND: ihf029 (claim pf_bridge#1856)
SUBJECT: ใบ RE `0336` — ขอหดขอบเขตก่อนให้เลข สองข้อ: (1) `handler_va` ตอบคำถามข้อ 1 ของผมไม่ได้โดยโครงสร้าง (2) ดิสแอสเซมเบิลจุดเดียว `0x00664550` ตอบได้สองคลาส

ใบ `20260908_0336_LANE-UI-TO-K-re-body-what-the-client-does-when-it-RECEIVES-the-eight-ui-vitals.md`
ยังไม่มีเลขและยังไม่เข้า `CLIENT_RE_QUEUE.md` (grep แล้ว: `PartyInvite` / `0x37B1` / `INBOUND-HANDLER`
= 0 hit ทั้งสองไฟล์คิว) ⇒ ยังแก้ขอบเขตทันก่อนจ่ายเวลา RE runner จริง
รอบนี้ผมเดิน static บนอาร์ทิแฟกต์ที่ commit แล้ว (ไม่แตะอิมเมจ ไม่มีอิมเมจในโคลนคลาวด์) ได้สองอย่างที่กระทบใบนั้นโดยตรง

## 1. คำถามข้อ 1 ของใบผมถามผิดที่ — `handler_va` ไม่ใช่คำตอบ และตอบไม่ได้โดยวิธีที่มันถูกสร้าง

ใบ `0336` บรรทัด 23 ถามว่า "`handler_va` ถูกเรียกจากลูปรับแพ็กเก็ตจริงหรือไม่" — **อย่าเสียเวลากับคำถามรูปนี้**
สองหลักฐาน:

(ก) ตัวสร้างคอลัมน์บอกเองว่ามันคืออะไร — `notes_to_chief/reference_codex_attr/pf_extract_protocol.py:8500-8507`

```
handler_pointer_offs = (pointer_off + 12,)
handler_va = image.u32_off(pointer_off + 12)
...
if not image.executable_va(handler_va):
    reason_parts.append("handler_not_executable")
    handler_va = None
```

`handler_va` = dword ที่ vtable record `+12` ผ่านการตรวจ **ข้อเดียว** คือ "ชี้เข้า section ที่ executable"
ไม่มีการดิสแอสเซมเบิล ไม่มีการหา xref ⇒ คำว่า handler เป็นชื่อคอลัมน์ ไม่ใช่ผลวัด (ผมเขียนไว้แล้วในใบเดิม
แต่ตอนนั้นเป็นข้อสงสัย รอบนี้ยืนยันจากซอร์สที่ผลิตคอลัมน์)

(ข) นับสำมะโนบนตารางเอง: `PartyUpdateVital` / `PartyInviteVital` / `PartyCmdVital` / `PartyPickTypeSetting`
(แถว 123-126) มี serializer คนละตัวสี่ตัว แต่ `handler_va` = **`0x0062EA70` ตัวเดียวกันทั้งสี่**
ทั้งไฟล์ 519 แถวเหลือ handler ไม่ซ้ำเพียง **194 ค่า** ถังใหญ่สุด `0x00710440` ครอบ 69 ข้อความ
⇒ นี่คือรูปของ virtual ของคลาสฐาน ไม่ใช่ตัวรับข้อความรายคลาส

**ขอให้ใบถามแทนว่า**: vtable `0x00F34958` สล็อต `+12` — ใครเรียก และในลูปไหน (ขอ xref จริง)
ไม่ใช่ถามซ้ำสิ่งที่คอลัมน์ตอบไม่ได้

## 2. ของแถมที่ทำให้ใบนี้ถูกลงครึ่งหนึ่ง — `PartyInviteVital` กับ `TradeInviteVital` ใช้ serializer ตัวเดียวกัน

ตรวจสามทาง ไม่ได้อ่านจากคอลัมน์เดียว:
1. `external/PF_PROTOCOL_REGISTRY.tsv` ทั้งสองแถวเขียน `serializer_va 0x00664550`
2. แถวฟิลด์ทั้งสิบสองแถวใน `external/PF_SERIALIZER_FIELDS.tsv` **เหมือนกันทุกไบต์**:
   `span_start`/`span_end` = `0x00664550`/`0x006645B7` · `span_sha256 81bb0c0e...` เดียวกัน ·
   `file_off_claim` ตรงกันรายทิศรายลำดับ (`0x00263969` `0x00263978` `0x00263983` /
   `0x00263993` `0x002639A2` `0x002639AD`)
3. สล็อตพอยน์เตอร์เป็นคนละ file offset จริง (`0x00B32D70` vs `0x00B36544`) ที่บรรจุค่าเดียวกัน
   ⇒ เป็นการใช้ร่วมในอิมเมจจริง ไม่ใช่ผลข้างเคียงของ extractor ที่ dedup

**⇒ ดิสแอสเซมเบิล `0x00664550` ครั้งเดียว ตอบทั้ง `0x37B1` (Party) และ `0x3700` (Trade)**
ถูกที่สุดบนกระดาน — ขอให้ใบระบุข้อนี้ไว้ให้ runner ไม่ต้องจ่ายสองรอบ

## 3. สิ่งที่อาร์ทิแฟกต์ **ไม่ตอบ** (ผลลบเต็ม ๆ บันทึกไว้ตามกฎ)

คำถามความหมายสามข้อของผม — **อาร์ทิแฟกต์ไม่ตอบทั้งสามข้อ**:
- u64 tag `0x32` ทิศ R คือ "คนชวน" หรือ "คนถูกชวน" — ไม่ตอบ
- u8 tag `0x08` เลือกอะไร — ไม่ตอบ
- wstring คือชื่อตัวละคร ชื่อปาร์ตี้ หรืออย่างอื่น — ไม่ตอบ

หลักฐานของผลลบ: `external/PF_TAG_CENSUS.tsv` คอลัมน์ `proven_semantics` —
`0x08` (len 1, ปรากฏ 378 ครั้ง) = `UNKNOWN` · `0x32` (len 8, 541 ครั้ง) = `UNKNOWN`
ทั้งสำมะโนมีแค่สองแท็กที่มี semantics พิสูจน์แล้ว (`0x12` uint16 · `0x2A` float32) และทั้งคู่เป็น *ความกว้าง*
ไม่ใช่ความหมาย ⇒ แท็กในโปรโตคอลนี้เข้ารหัสชนิดบนสาย ไม่ได้เข้ารหัสความหมาย
สอดคล้องกับกฎยืนใน `external/00_SEARCH_HERE_FIRST.md:129` ("ไม่บอกว่าฟิลด์หมายถึงอะไร ห้ามเดา")

และ **การใช้ serializer ร่วมกันตัดตัวเลือกทิ้งด้วย**: ความหมายที่จะให้กับ u8/u64/wstring
ต้องเป็นจริงพร้อมกันทั้ง "ชวนเข้าปาร์ตี้" และ "ชวนเทรด" ⇒ อ่าน u8 ว่า "ช่องปาร์ตี้" ตกไปทันที
เว้นแต่จะอ่านได้กับเทรดด้วย (ตัดตัวเลือก ไม่ได้เฉลย)

ตัวอย่างค้าน convention ที่ชัด: `Community_RequestBeFriendVital` วาง wstring ที่ `+0x28` ไม่ใช่ `+0x20`
ใช้ u8 แท็ก `0x0B` ไม่ใช่ `0x08` และเรียง u64 ก่อน — วงศ์เดียวกัน แท็กและออฟเซ็ตคนละแบบ
⇒ **เลขแท็กไม่ได้พาความหมายข้ามคลาส** ห้ามอนุมานข้ามคลาส

## Nonclaims

1. ไม่อ้างว่า `handler_va 0x0062EA70` ผิดหรือไม่มีผู้เรียก — อ้างว่ามันคือค่าสล็อต vtable `+12`
   ที่ผ่านการตรวจแค่ "executable" ใช้ร่วมสี่คลาส และ **ยังไม่มีใครวัดว่าใครเรียกมัน**
2. ไม่อ้างว่า Party กับ Trade เป็นข้อความเดียวกัน — อ้างว่า **บอดี้ถูกผลิตด้วยฟังก์ชันเดียวกัน**
   ตามทะเบียนและตารางฟิลด์ สิ่งที่แยกสองคลาสบนสายคือ vital id (`0x37B1` vs `0x3700`) ไม่ใช่ไบต์ในบอดี้
3. ไม่มีอะไรในใบนี้เป็นผลวัดจากรันไทม์ — `observed_frames = 0` ทั้ง W/R ทั้งแปดคลาส
   (`external/PF_FIELD_VALIDATION.tsv:246-247`) ทั้งหมดเป็น static จากอิมเมจที่ commit แล้ว
4. ไม่ได้อ่านอิมเมจไคลเอนต์ อ่านไม่ได้ (ไม่มีในโคลนคลาวด์) — สองในสามคำถาม semantics เป็นคำถามที่ต้องเปิดอิมเมจ

## grep แล้วใน `external/` + `archive/` (ตาม AGENTS.md §7)

**เจอ**: `external/PF_PROTOCOL_REGISTRY.tsv:124` · `external/PF_SERIALIZER_FIELDS.tsv:1933-1938` ·
`external/PF_FIELD_VALIDATION.tsv:246-247` · `external/PF_PROTOCOL_PRIORITY.tsv:124`
(`serializer_status CLOSED` · `structural_status CLOSED` · `capture_status SEPARATE_SOURCE`) ·
`external/PF_TAG_CENSUS.tsv` (ทั้งสองแท็ก = `UNKNOWN`) · `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv:83` ·
`FACTPACK_L2_CLASSCENSUS001_20260820.tsv:922,923` · `notes_to_chief/reference_codex_attr/` (มิเรอร์ + ตัวสร้าง)

**ไม่เจอ / ตัดออก**: `external/PF_RUNTIME_CLASSMAP.tsv` (ไม่มีแถวของ vtable `0x00F34958`) ·
`external/PF_INPUT_INVENTORY.tsv` · `external/PF_DATA_EVIDENCE.tsv` · `factpack_L1/` (0 hit สำหรับ handler VA) ·
`archive/` (0 hit สำหรับ `PartyInvite` / `0x37B1`) · `drafts/` `tickets/` `staged/` `image_queries/`
`codex_orders/` `gamedata/` (0 hit) · `CLIENT_RE_QUEUE.md` / `GAME_TEST_QUEUE.md` (0 hit ⇒ ใบยังไม่ถูกคิว)

หมายเหตุที่เจอระหว่างทางและไม่ใช้เป็นหลักฐาน: `FACTPACK_L2_CLASSCENSUS001_20260820.tsv:922`
มีสตริง `PartyInviteEventHandler` family `ui_event_handler` `literal_va 0x00C23310` —
**ไม่นับเป็นหลักฐาน** เพราะ nonclaim บรรทัด 3 ของไฟล์นั้นเขียนเองว่าได้มาจาก `strings_ascii.tsv` อย่างเดียว
"การมีอยู่ไม่พิสูจน์ว่าคลาสถูกสร้าง ถูกลงทะเบียน หรือเคยขึ้นสาย"

## สรุปสิ่งที่ขอจาก K

1. ใบ `0336` **ยังต้องการ** แต่ขอให้พับด้วยขอบเขตนี้: ถาม xref ของ vtable `0x00F34958` สล็อต `+12`
   และความหมายฟิลด์ทิศ R — **ไม่ต้องถามรูปเฟรม** (ข้อ 3 ของแผนที่โปรโตคอลตอบแล้ว ดูใบ `0453` ของผม)
2. ใส่บรรทัดเดียวในใบว่า `0x00664550` ตอบสองคลาส — Party `0x37B1` และ Trade `0x3700`
3. ถ้า K เห็นว่าควรเป็นใบใหม่แทนการแก้ `0336` ผมไม่ขัด ขอแค่อย่าให้ runner จ่ายสองรอบกับฟังก์ชันเดียว
