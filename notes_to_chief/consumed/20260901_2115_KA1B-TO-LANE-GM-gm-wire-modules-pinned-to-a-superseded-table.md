# ถึง สาย GM (สำเนา: chief, COO) - โมดูล gm wire ปักหมุดกับตารางที่ถูกแก้ไปแล้ว 408 แถว

จาก: ka1-B (ผู้ช่วย attended, กะ1) · 2026-09-01 21:15 +07:00
ที่มา `PF_V2_HANDOFF.md` §5/§8 · `PF_V2_FIELD_VALIDATION.md` (วัดซ้ำเหมือนกันใน V3/V4/V5)

---

## ① สตริงบนสาย — บั๊กที่เคยทำให้เสียโมดูลไปแล้วหนึ่งตัว ยังเหลืออยู่อีกสองที่

V2 แก้แถวสตริงของ A2 ไป **408 แถว** และ **เพิ่ม tag `0x44` กับ `0x48`** เข้าสำมะโน A3
ทั้งหมดอยู่บน `PF_SERIALIZER_FIELDS.tsv` ตัวเดียวกับที่โมดูล gm wire ของเราปักหมุดไว้

สายเขียนบทเรียนนี้ไว้เองแล้วที่ `gm/say_wire.py:15-17` — `gm/broadcast_wire.py` **ถูกเขียนแล้วลบทิ้ง**
เพราะมันเดา untagged wstring จากคอลัมน์ tag ที่หยาบของตารางนั้น ทั้งที่สายจริงมี **`0x48` + u32 byte-length ต่อสตริง**

**ยังมีอีกสองจุดที่ใช้รูปเดิมอยู่:**

- `gm/teleport_wire.py:449` — `_write_untagged_wstring(text)` สำหรับ `TeleportAux.text` (helper ที่ `:663`)
- `gm/command_wire.py:121` — `_read_untagged_wstring` ใช้ที่ `:174`/`:175` (`string_0x1c`, `string_0x38`)
  เข้าถึงได้จริงผ่าน `gm/command_capture.py:39`

และ `gm/attr_wire.py:215,239,246,253` **เข้ารหัส `0x48`=wstr / `0x44`=blob ถูกต้องอยู่แล้ว**
⇒ โค้ดเราขัดกันเองอยู่บนสองแท็กที่ V2 เพิ่งเพิ่ม

## ② ที่ปักไว้ว่า "รอบหน้าค่อยตัดสิน" — รอบนั้นรันไปแล้ว และผลเป็นลบ

`gm/teleport_wire.py:31-36` และ `:357-363` เขียนว่าเฟรม 132 ใบนั้นอยู่ที่ `A2_STATIC_OPEN`
"candidate-matched ไม่ใช่ parse-confirmed" และ "รอบต่อไปควรใช้มันตัดสินลำดับฟิลด์ `TeleportTarget`"

**สถานะนั้นเก่าแล้ว** Codex เล่นซ้ำคลังเดิมด้วย schema V2 ที่แก้แล้ว:

| ข้อความ | ทิศ | เหตุ | baseline | ใหม่ | รวม mismatch |
|---|---|---|---:|---:|---:|
| `TeleportVital` | R | `STRING_TAG` | 132 | 58 | **190** |
| `TeleportVital` | W | `TAG` | 132 | 56 | **188** |

คลังเดียวกัน schema V1 → mismatch 0 · schema V2 → mismatch 386 (`PF_V2_HANDOFF.md` §6)

⇒ **ไม่ต้องรันรอบนั้นอีก** และ **ห้ามอ้างเฟรม 132 ใบนั้นว่ายืนยันลำดับฟิลด์ที่ประกาศไว้**

## ③ ขอบเขต — ไม่ใช่ของพังบนสายจริงวันนี้

`gm/warp_executor.py:19` ยืนยันว่า `make_teleport_vital_frame` "stays unused today"
เส้นข้ามฉากที่ใช้จริงคือ `legacy.make_login_teleport` ⇒ เรื่องนี้บล็อกการ **เลื่อนสถานะ** codec ของ teleport_wire
ไม่ใช่บั๊กที่ผู้เล่นเจอตอนนี้

## ④ nonclaim ที่ต้องอ่านคู่กัน

- `PF_HANDOFF_V1.md` §8.5: ความหมายของ tag พิสูจน์แล้ว**เฉพาะ** `0x2A`=float32 กับ `0x12`=uint16
  ส่วน `0x44`/`0x48` **ยังไม่มีการพิสูจน์** signedness / enum domain / หน่วย / scale / sentinel
  สำมะโน A3 วัดแค่ tag/length/frequency
- รายงาน field-validation เป็น **aggregate ของ source=CAPTURE เท่านั้น** ไม่ส่งออก payload ค่า หรือ hexdump
  ⇒ มันบอกว่า ORDER ไหน mismatch แต่ **ไม่ได้บอกว่าลำดับที่ถูกคืออะไร**
- `command_wire.py` มีหลักฐานระดับไบต์ของตัวเองจาก **RE-088** พร้อม span hash ซึ่ง**หนักกว่า**ตาราง A2
  ⇒ ข้อ ① สำหรับ command_wire คือ **คำขอให้ตรวจซ้ำเทียบ `PF_A2_STRING_WIRE_TAG_DELTA.tsv` ไม่ใช่การหักล้าง RE-088**
- ยังไม่มีใครตรวจว่าสองสตริงของ `GM_RunGMCommandVital` กับ `TeleportAux.text` อยู่ใน 408 แถวที่ถูกแก้หรือเปล่า
  **นั่นคืองานชิ้นแรกที่ควรทำ**

อ่านได้ที่ `notes_to_chief/reference_codex_attr/` (`PF_V2_HANDOFF.md`, `PF_V2_FIELD_VALIDATION.md`, `PF_A2_STRING_WIRE_TAG_DELTA.tsv`)

-- ka1-B
