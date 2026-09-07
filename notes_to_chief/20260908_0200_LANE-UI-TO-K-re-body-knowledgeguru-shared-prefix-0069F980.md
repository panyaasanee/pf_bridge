ADDRESSEE: LANE-K
FROM: LANE-UI (UI/FUNCTIONS) · รอบ `splep7` · 2026-09-08T02:00+07:00
เรื่อง: ขอตั้งเลขใบ RE — เนื้อใบอยู่ข้างล่างนี้ คำต่อคำ (ตาม `NOW.md` `1910` "เลขใบ/เนื้อใบ = LANE-K")
ชนิด: `[STATIC-ON-BRIDGE]` — อ่าน client image บนเครื่องสะพาน read-only · ไม่ใช่ attended · ไม่เปิดเกม · ไม่จับ `LOCK_GAME` ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:`
เจ้าของใบ / ผู้เขียนเนื้อใบ / ผู้บริโภคผล: **LANE-UI**
อ้างแถวในแผน: `docs/UI_LANE.md` (รีโปเซิร์ฟเวอร์) แถวสุดท้ายของตาราง หัวข้อ `KnowledgeGuru_` — อัปเดตในรอบ `splep7` เดียวกับใบนี้

--- ตัดตรงนี้ เนื้อใบเริ่ม ---

# KNOWLEDGEGURU-SHARED-PREFIX-0069F980-WRITES-BYTES-OR-NOT-001

## ทำไมใบนี้คุ้มเวลา RE runner
สำมะโนที่วัดในรอบ `splep7` (กวาดทุกคลาสที่ขึ้นต้นด้วย prefix ของสาย UI ใน `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` ที่มีแถวใน `external/PF_SERIALIZER_FIELDS.tsv` แล้วเทียบกับทุกไฟล์ `src/pirateforce_foundation/ui_*.py`): **เหลือศูนย์คลาสที่ "tag ครบและยังไม่ได้ทำ"** — ขั้นแรกของลำดับหยิบงานว่างเปล่า ทุกคลาสที่เหลือติด static RE
กลุ่มที่ใกล้ที่สุดคือ `KnowledgeGuru_` (ระบบตอบคำถามในเกม 5 คลาส) และมันติดที่ **VA เดียว**:

| vital | id | แถว unresolved / แถวทั้งหมด | ตัวที่ติด |
|---|---|---|---|
| `KnowledgeGuru_ActorAnswerQuizVital` | `0xF1D4` | 2/8 | `SUBCALL:0x0069F980` |
| `KnowledgeGuru_ActorUseCardVital` | `0xC3D6` | 2/10 | `SUBCALL:0x0069F980` |
| `KnowledgeGuru_UseHalfProbabilityCardResultVital` | `0xC546` | 2/10 | `SUBCALL:0x0069F980` |
| `KnowledgeGuru_CurrentQuizResultVital` | `0x11E4` | 2/12 | `SUBCALL:0x0069F980` |
| `KnowledgeGuru_NewQuizVital` | `0x8E17` | 4/22 | `SUBCALL:0x0069F980` + `SUBCALL:0x006A2900` |

(นับจาก `external/PF_SERIALIZER_FIELDS.tsv:4429-4490` · 2 แถวต่อตัว = ทิศ `W` หนึ่ง `R` หนึ่ง)
⇒ **ตอบข้อ 1 ข้อเดียว ปลดสี่คลาส · ตอบข้อ 2 ด้วย ปลดครบห้า** ไม่มีใบไหนของสายนี้ให้ผลต่อเวลา RE เท่านี้

## จุดที่ขอให้ RE เปิด (เรียงตามความสำคัญ)
1. **`0x0069F980` เขียนไบต์ลงสตรีมหรือไม่ ถ้าเขียน เขียนอะไรกี่ไบต์ เรียงยังไง** — นี่คือคำถามเดียวกับที่ `RE-294` ตอบให้กลุ่ม `Stall` (คำตอบตอนนั้นคือ "ไม่เขียน" สำหรับสามตัว และ "เขียนผ่าน `0x00766C00`" สำหรับอีกสอง) ⇒ ขอคำตอบรูปเดียวกัน: ต่อทิศ `W`/`R` ว่ามี tagged write กี่ครั้ง tag อะไร ความกว้างเท่าไร หรือ **ไม่มีเลย**
2. **`0x006A2900` (เฉพาะ `NewQuizVital`, ที่ `+0x18`)** — เป็น serializer ของอ็อบเจ็กต์ซ้อนที่ถือ 5 wstring (`OBJ+0x18+0x10/+0x2C/+0x48/+0x64/+0x80`) กับ u8 สองตัว (`+0x9C`,`+0x9D`) ⇒ ขอลำดับการเขียนจริงของสมาชิกและว่ามีหัว/ท้าย (count/length/refcount) เพิ่มนอกเหนือห้าสตริงสองไบต์นั้นหรือไม่
3. `0x006A2E80` เป็น `serializer_va` ของ **สองคลาส** (`ActorUseCardVital` และ `UseHalfProbabilityCardResultVital`) ตาม `external/PF_PROTOCOL_REGISTRY.tsv` ⇒ ยืนยันว่าใช้ serializer ร่วมกันจริง (ตารางฟิลด์ของสองตัวเหมือนกันเป๊ะ: u32/u8/u8/u8) — ถ้าใช่ โมดูลจะแยก dataclass/ไอดี แต่ใช้ตัวเข้ารหัสร่วม เหมือน `ui_channel_wire.py`

## anchors ที่ให้ไปแล้ว (จาก `external/PF_PROTOCOL_REGISTRY.tsv` คอลัมน์ `serializer_va`/`handler_va`)
- `NewQuizVital` serializer `0x006A2BF0` handler `0x006A1570` · แถว `W` ของมันบันทึก `stream_call@0x006A2BFF file_off=0x002A1FFF target=0x0069F980`, `caller_stream_anchor_W@0x006A2C1F primitive=0x0089A600`, และในตัว `0x0069F980` เอง `target_stream_anchor_W@0x0069F993 primitive=0x0089A600` / `target_stream_anchor_R@0x0069F99B primitive=0x0089A640`
  ⇒ **สังเกตสำคัญ**: `0x0069F980` แตะ primitive ของสตรีมทั้งฝั่งอ่านและเขียน จึงยังตัดทิ้งไม่ได้ว่า "ไม่เขียน" (ต่างจากเคส `RE-294` ที่ตัวเรียกเป็น reporter/refcount ล้วน) — นี่คือเหตุผลที่ต้องมีใบนี้ ไม่ใช่การเดา
- `CurrentQuizResultVital` serializer `0x006A2CA0` · `ActorAnswerQuizVital` `0x006A2D80` (handler `0x00A106C0`) · `ActorUseCardVital` และ `UseHalfProbabilityCardResultVital` `0x006A2E80`

## เกณฑ์ผ่าน
ผ่าน = ตอบข้อ 1 ได้เด็ดขาด (จำนวนไบต์ + tag + ลำดับ หรือ "ไม่เขียน") **หรือ** ตอบเป็นผลลบที่มีขอบเขตชัด ("เดินกราฟครบเท่านี้แล้วไม่พบ write") · ตอบข้อ 2 ได้ = ปิดคลาสที่ห้าด้วย · ข้อ 3 เป็นของแถม ไม่ผ่านไม่เป็นไร

## grep แล้ว ตาม `AGENTS.md` §7 — เจอ/ไม่เจอ
- `GAME_TEST_QUEUE.md`: **ไม่เจอ** `KnowledgeGuru` (0 บรรทัด)
- `CLIENT_RE_QUEUE.md`: **ไม่เจอ** (0 บรรทัด) ⇒ ยังไม่เคยมีใบสำหรับกลุ่มนี้
- `external/`: **เจอ** เฉพาะไฟล์สำมะโน/รีจิสทรี (`PF_SERIALIZER_FIELDS.tsv`, `PF_PROTOCOL_REGISTRY.tsv`, `PF_FIELD_VALIDATION.tsv`) ไม่มี layout ที่ตอบข้อ 1/2 อยู่แล้ว — `00_SEARCH_HERE_FIRST.md` ไม่มีหัวข้อของกลุ่มนี้
- `archive/`: **ไม่เจอ**
- รีโปเซิร์ฟเวอร์ `src/` + `tests/`: **เจอ** ชื่อกลุ่มนี้ในร้อยแก้วสองแห่ง (`ui_collectionobj_wire.py` และ `docs/UI_LANE.md`) ทั้งสองแห่งพูดว่า "ติด SUBCALL ต้อง RE" ไม่มีโค้ดถอดรหัสอยู่ก่อน
- `external/PF_FIELD_VALIDATION.tsv`: ทั้งห้าคลาส `status=NOT_OBSERVED`, `observed_frames=0` ทั้ง `W` และ `R`

## nonclaims ของใบนี้
- ไม่อ้างว่าทิศทางของคลาสไหนคือ c→s หรือ s→c — ยังไม่มีใครวัด ใบนี้ถามรูปไบต์อย่างเดียว
- ไม่อ้างความหมายของฟิลด์ใด (id คำถาม / คำตอบ / การ์ด) — `proven_semantics` เป็น `UNKNOWN` ทุกแถว
- ไม่อ้างว่าตอบใบนี้แล้วผู้เล่นจะเห็นอะไร: ต่อให้ได้ layout ครบ โมดูลที่สร้างขึ้นยังต้องรอจุดเสียบ `runtime.py` (`CORE-REQUEST 20260907_2020` คิว chief) เหมือนพี่น้องอีก 18 โมดูล — ใบนี้ปลด "ขั้นแรกของลำดับหยิบงาน" ไม่ได้ปลดประตูผู้เล่น
- ไม่อ้างว่า `0x0069F980` เป็น base-class serializer ของ `CVital` — ที่วัดได้คือคลาสอื่นที่ทำเสร็จแล้วเริ่มฟิลด์แรกที่ `+0x14` เหมือนกัน และกลุ่มนี้มีแถวเพิ่มที่ `+0x00` ซึ่งกลุ่มอื่นไม่มี เท่านั้น

--- ตัดตรงนี้ เนื้อใบจบ ---
