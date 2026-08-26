# GM round 2026-08-26 ~18:3x (+07:00) — RE-088 follow-up (schema-aware GM-002 decoder)

🎯 อ่านจดหมายค้าง (`notes_to_chief/` "ยังไม่ consumed") พบ `20260826_1811_RE-088-RESULT-GM-COMMAND-WIRE-PINNED.md` — RE runner ปิดเลข `RE-088` แล้ว: layout ระดับไบต์ของ `GM_RunGMCommandVital` (`0x51E9`) และ `GM_RunGMCommandResultVital` (`0x8C77`) พิสูจน์ครบ (`STRUCTURAL-LAYOUT-PINNED`) และปิดคำถาม "สอง sub-path" ที่ `docs/GM_LANE.md` เคยค้างไว้ (มี nested body เดียว คุมด้วย presence flag ไม่ใช่ sub-opcode) `BUILD_IMPACT` ของใบบอกตรงว่า GM-002 เปลี่ยนจาก raw capture เป็น schema-aware decode ได้ และ GM-003 ได้ codec ที่ตรวจอิมเมจแล้ว — แต่ยังห้าม execute/ตั้งชื่อ command จนกว่า `RE-091` (semantic + live trigger) จะปิด

ยึดล็อกด้วย draft PR ทั้งสอง repo ก่อนเริ่ม (`pf_bridge#128`, `pirate-force-server#69`) — ตรวจแล้วไม่มี PR `[LANE-GM]` เปิดค้างก่อนหน้า (ทั้งสอง repo คืนค่าว่าง)

## สร้าง/แก้ (`pirate-force-server`, เขตเขียนของสายนี้ทั้งหมด)

- **ใหม่** `src/pirateforce_foundation/gm/command_wire.py` — `decode_gm_run_command_vital` / `decode_gm_run_command_result_vital` ถอด wire ตาม RE-088 พิน ชื่อฟิลด์เป็นตำแหน่งล้วน (`field_0x10` `field_0x14` `field_0x18` `string_0x1c` `string_0x38`) ไม่ตั้งชื่อความหมายใด ๆ ตาม nonclaim ของ RE-088 เอง ไม่ execute ไม่ dispatch ไม่อ่านจาก socket จริง
- **แก้** `src/pirateforce_foundation/gm/command_capture.py` (GM-002) — เพิ่มส่วน decode พยายามถอด schema ทุกครั้งที่ capture ควบคู่ hex dump เดิม (hex dump ไม่เปลี่ยน) decode ล้มเหลวจับไว้ในตัวไม่ throw ออกมา (capture ต้องไม่หายเพราะ decode พัง) สตริงที่ถอดได้ผ่าน escape เดียวกับ `account_name` (กัน header injection)
- **แก้** `docs/GM_LANE.md` — อัปเดตตาราง wire-facts และหัวข้อ RE-open ให้ตรงกับ RE-088 (structural PASS/DONE, semantic ยังเปิดผ่าน RE-091) เพิ่มหัวข้อ "Modules delivered (RE-088 follow-up round)"
- **ใหม่** `tests/test_gm_command_wire.py` (21 เทส) · **แก้** `tests/test_gm_command_capture.py` (+4 เทส) — รวมเทสใหม่สายนี้ 25 เทส

## ผลตรวจ

- ชุดเทส GM ทั้งหมด (`test_gm_*.py`): **86 เทส ผ่านทั้งหมด** (จากเดิม 61 ก่อนรอบนี้ + 25 ใหม่)
- `pf-adversary` ตรวจก่อน push ครั้งที่สอง (หลัง commit แรก) ตามกฎบังคับ — พบ 3 ข้อยืนยันได้จริง + 2 ช่องว่างเทสที่โจทย์ขอให้ตรวจ ทั้งหมดแก้แล้วก่อนปิด draft (รายละเอียดด้านล่าง) ไม่มีอะไรหลุดเข้า `main` ระหว่างนี้

## แก้ไขหลัง `pf-adversary`

`pf-adversary` ตรวจ diff เต็ม (4 ไฟล์: `command_wire.py` ใหม่, `command_capture.py` แก้, เทสสองไฟล์) เทียบกับ `PF_SERIALIZER_FIELDS.tsv` จริงและใบ RE-088 จริง พบ:

1. **ยืนยันจริง (medium)** — `_decode_section` เขียนบรรทัด `"# decode: presence=1"` เป็นค่าคงที่เสมอ ไม่ว่าไบต์จริงจะเป็นอะไร (ค่าที่ไม่ใช่ 0 ทุกค่าถือว่า "มี nested body" ตามเงื่อนไข `!= 0` ของ RE-088 เอง แต่ log ควรโชว์ค่าที่วัดได้จริง ไม่ใช่ normalize เป็น 1) — ถ้า client ส่ง presence=200 (fuzzed/malformed) ไฟล์ capture จะโกหกว่าเห็น 1 แก้โดยเก็บค่า `presence` จริงไว้ใน `GmRunCommandBody` และพิมพ์ค่าจริงในบรรทัด decode
2. **ยืนยันจริง (gap)** — สัญญาเรื่อง `raw` param ว่าต้องเป็น "payload เท่านั้น ไม่ใช่ทั้งเฟรม" ประกาศไว้ใน docstring ของ `command_wire.py` อย่างเดียว `command_capture.py` ไม่ได้บอกไว้เลยและยังไม่มี wiring จริงมาทดสอบขอบเขตนี้ — ถ้า wiring ในอนาคตส่งทั้งเฟรมมาแทน decode section จะพัง (`FAILED` ตลอดไป เงียบ ๆ ไม่ crash) แก้โดยเขียนสัญญาเดียวกันไว้ทั้งสอง docstring ชัดเจน พร้อมชี้ผลถ้าใครทำผิด (hex dump ยังถูกเสมอ)
3. **ยืนยันจริง (gap)** — สาม `span_sha256` pin ใน `command_wire.py` ไม่มีเทสคุม ต่างจากธรรมเนียมของ `scene_catalog.py` เอง (เช็ค sha ตอน import) แก้ด้วย pin-lock test (เทียบค่าคงที่ตรง ๆ กัน edit พลาดโดยไม่ตั้งใจ)
4-5. **ช่องว่างเทสที่โจทย์ขอให้ตรวจ** — เพิ่มเทส presence byte ที่ไม่ใช่ 0/1 (200) และเทส declared string length สูงสุด (`0xFFFFFFFF`)

เทสรวมหลังแก้: 86 (จากเดิม 81 ก่อนแก้) ผ่านทั้งหมด — commit แก้แยกจาก commit แรก (`17426ab` ทับ `0c6c97e`) ตาม branch เดียวกัน

## ยังไม่ทำ (ตั้งใจ)

- ยังไม่ execute หรือ dispatch command ใด ๆ — `RE-091` (semantic ของสองสตริง + live chat trigger) ยังเปิดอยู่ ตาม nonclaim ของ RE-088 เอง
- ยังไม่มี wiring จริงเรียก `capture_raw_gm_command` จาก `runtime.py` — สัญญาเรื่อง payload-only ยังไม่มีอะไรพิสูจน์จริงจนกว่าจะมี wiring (ดูข้อ 2 ด้านบน) — เมื่อ chief ต่อสาย `CORE-REQUEST-006`/`0x51E9` dispatch ควรตรวจสัญญานี้ตรง ๆ
- `GM-003` (`gm/commands.py`) ไม่แตะรอบนี้ — codec ใหม่พร้อมให้ใช้แต่ยังไม่ผูกกับ grammar ที่มีอยู่ เพราะสองสตริงจาก wire ยังไม่พิสูจน์ว่า = command/argument (RE-091)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ยังไม่มี** — รอบนี้เป็นการยกระดับ decoder ฝั่งเซิร์ฟเวอร์ล้วน (unit test เท่านั้น ไม่มี client ไม่มี wiring เข้า runtime) `CORE-REQUEST-006` (ส่ง GM state ตอน login) ยังไม่ถูกต่อสายโดย chief (ยืนยันจาก `notes_to_chief/FROM_CHIEF_R179_TO_ATTENDED_20260826_1900.md`: "GM ยังไม่ต่อสายรอบนี้") ผู้เทสยังไม่มีอะไรทำในเกมจนกว่าจะ merge

## nonclaim

โค้ดรอบนี้ทั้งหมดเป็นเทสหน่วยฝั่งเซิร์ฟเวอร์ (`unittest`, ในโปรเซส, ไม่มี client, ไม่มี capture จริง) — ไม่มีการอ้างว่าไบต์จริงจาก client ตรงกับที่ decoder นี้คาดไว้ จนกว่าจะมี capture จริงจาก GM-002 หรือคำตอบ `RE-091`

## ค้าง

- `RE-091` (semantic ของสองสตริง + live chat trigger ของ `0x51E9`) — ของสาย RE ไม่ใช่ของสายนี้
- `CORE-REQUEST-006` รอ chief ต่อสาย (ยังไม่ทำตาม R179)
- payload-vs-frame boundary ระหว่าง `command_wire.py`/`command_capture.py` ยังไม่มีอะไรพิสูจน์จนกว่าจะมี wiring จริง (จุดที่ pf-adversary ชี้ ข้อ 2 ด้านบน) — เตือน chief ไว้ในจดหมายสถานะรอบนี้ให้ตรวจตอนต่อสาย
