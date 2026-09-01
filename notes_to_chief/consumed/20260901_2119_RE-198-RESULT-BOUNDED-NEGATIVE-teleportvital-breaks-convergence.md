[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: chief รอบ `happy-dirac-69cabr`/`focused-turing-69cabr` (R294), งานจริงทำโดย pf-static-re subagent · 2026-09-01T21:19+07:00]
[อ้าง: `CLIENT_RE_QUEUE.md` RE-198]

# RE-198-RESULT — BOUNDED-NEGATIVE: pattern อ่อนกว่าที่คิด (TeleportVital = 4 ไม่ใช่ 0)

## คำตอบข้อ 1-2 (constructor ของ 0x309A เอง)

**[NO EVIDENCE FOUND]** เจอ dispatcher/serializer (`serializer_va=0x005E42C0`, `handler_va=0x005F2400`) แต่
**ไม่เจอ** prototype constructor ของ `UpdateAttrVital` เอง (สิ่งที่ RE-105/RE-129 ใช้หา byte จริงของ
`state_wire`/`teleport_wire`) ค้นทั่ว `pf_bridge/` (`PF_SERIALIZER_FIELDS.tsv`, `PF_PROTOCOL_REGISTRY.tsv`,
`PF_A6_VTABLE_CANDIDATE_DELTA.tsv`, `PF_RUNTIME_CLASSMAP*`, `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`)
ไม่มีแถวไหนชี้ VA ของ constructor ที่เขียน `+0x10` ให้ opcode นี้โดยตรง

## คำตอบข้อ 3 (header shape เทียบ) — BOUNDED-NEGATIVE เท่านั้น

`UpdateAttrVital` (rows 825-858) **delegate** แบบเดียวกับ `ForcePos` (rows 547-554) — ทั้งคู่เริ่ม body ที่
message offset `+0x14` ผ่าน `SUBCALL` ไม่ใช่ inline แบบ `GM_UpdateGMStateVital` (rows 6255-6260) — สนับสนุน
ทางอ้อมว่า `+0x10` คือช่อง version 1 ไบต์เดียวกันทั้งสามตระกูล **แต่** delegate ของ `UpdateAttrVital`
(`0x00463DE0-0x00463FA2`) ใหญ่กว่า `ForcePos`'s delegate ~7 เท่าและส่วนใหญ่ `CALL_UNCLASSIFIED`/CRT stub
noise — เทียบโครงในไม่ได้สะอาดเท่า

## 🔴 ข้อค้นพบสำคัญที่สุด — ทำลาย convergence argument เดิม

`RE-129-RESULT` (`notes_to_chief/20260828_2009_RE-129-RESULT-VERSION-ZERO-HANDLER-NOOP.md`) ข้อ T3 **ปักหมุด
`TeleportVital`'s เอง** — คนละ vital กับ `ForcePos` แต่กลไก generic-reader เดียวกัน — constructor
`[0x005E53D0,0x005E5459)`: `mov byte ptr [esi+0x10], 4` ⇒ **ค่า 4 ไม่ใช่ 0**

เหตุผลเดิมที่ chief ใช้เลือก `0` ให้ `attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED` คือ "สอง vital ที่
พิสูจน์แล้วอิสระต่อกันในกลไกเดียวกันลู่เข้าหา 0 ทั้งคู่" (`GM_UpdateGMStateVital`=0, `ForcePos`=0) —
ข้อเท็จจริงที่ RE-198 ยืนยันคือ **มี vital ที่สามในกลไกเดียวกันเป๊ะ (`TeleportVital`) ที่ได้ 4** บันทึกอยู่ใน
ไฟล์ผลของ RE-129 เอง ซึ่ง chief อ้างถึงเป็นแหล่งแต่ไม่ได้เห็นบรรทัดนี้ตอนเลือก byte

**นี่ไม่ได้แปลว่า 0 ผิด** — `TeleportVital` เป็นคนละ opcode จาก `ForcePos`/`0x309A` ทั้งคู่ (เรื่องระบุตำแหน่ง
กับเรื่องบอกเวอร์ชันของ `UpdateAttrVital` อาจไม่ใช่ตระกูลเดียวกันจริง) แต่ pattern ที่อ้างว่า "กลไกนี้ตอบ 0
เสมอ" **ไม่จริง** — เป็น 2 ใน 3 ไม่ใช่ 3 ใน 3

## ข้อ 4 — raw capture

ไม่มี raw bytes ของ `UpdateAttrVital` ที่ยิงจริงใน clone นี้ (คาดไว้แล้ว) แต่มีตารางอนุพันธ์
`PF_FIELD_VALIDATION.tsv:101` บอกว่ามี **69 instance ใน capture 7 ไฟล์จริง** ทิศทาง client-received ที่
candidate-ID ตรงกับ `UpdateAttrVital` — แต่ status `A2_STATIC_OPEN` = candidate เท่านั้น
`parse_success_instances=0` ⇒ ไม่มีใครถอด field-level (รวม version byte) จาก 69 instance นี้เลย ยังไม่ใช่
proof แต่เป็นเบาะแสว่า capture ตัวจริงมีอยู่ (7 ไฟล์) ถ้าไปถึงเครื่องสะพานได้

## สถานะ

**BOUNDED-NEGATIVE** ตามเกณฑ์ของใบ — ไม่ถึง PASS (ไม่มี direct instruction proof ของ 0x309A เอง) แต่
สูงกว่า NO-EVIDENCE เพราะมี header-shape match บางส่วน (entry offset +0x14 เหมือนกันทั้งสามตระกูล)

## ทำอะไรต่อ

1. **แก้คอมเมนต์ของ `UPDATE_ATTR_VITAL_VERSION_CONFIRMED = 0` ใน `attr_wire.py` แล้ว** (รอบ `focused-turing-69cabr`
   เดียวกันนี้ — ตัวคอมเมนต์ที่เขียนไปแล้วโดยบังเอิญได้เอ่ยถึง TeleportVital=4 ไว้ก่อน RE-198 จะเสร็จด้วยซ้ำ
   (agent ที่ต่อสายค้นเจอเองจาก RE-129-RESULT โดยตรง) — ไม่ต้องแก้ซ้ำ ตรวจแล้วตรงกับผล RE-198 ทุกจุด)
2. **ไม่แนะนำให้เดา byte ตัวที่สอง** ถ้า `GT-193` ข้อ 8 เจอ reconnect จริง — กลับมาเปิดใบใหม่หา constructor
   ของ `0x309A` เองโดยตรง (ยังไม่มีใครทำ ต้องหา VA รอบ registration/bootstrap ของ opcode นี้)
3. **`0` ยังคงเป็นการเดาที่มีเหตุผลดีที่สุดเท่าที่มี** ภายใต้ความเสี่ยงที่ COO ยอมรับแล้ว (bounded, reversible)
   — ไม่ใช่ค่าที่วัดแล้ว จนกว่าจะมี raw capture หรือ constructor VA จริง

## สัญญาผู้บริโภค

chief บริโภคผลนี้เอง (เจ้าของ `gm/attr_wire.py`) — ปิดแล้วรอบนี้ ไม่ต้องเปิดใบใหม่ซ้ำ

PF-AUTOMERGE: v4
