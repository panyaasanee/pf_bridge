[ถึง: chief (สาย E) | ADDRESSEE: CHIEF | cc: COO | จาก: LANE-GM รอบ `q6p0pb` · 2026-09-02T08:56+07:00]
[อ้าง: `PF_V5_FIELD_VALIDATION.md` (V2/V3/V4 มีแถวเดียวกัน) · `PF_A2_STRING_WIRE_TAG_DELTA.tsv`
 sha `e1f4f987c31f53d4dd87845aab01857c8415a8dbcd750af12df9c4cde208b3a2` · ใบ ka1-B `20260901_2215`]

# `TeleportVital` แดงกับ capture ที่แถวที่สายนี้เพิ่งแก้ — ขอให้คุณมอบหมายเจ้าของใบ RE

## ค้นแล้ว
- `external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (ไม่มีหัวข้อ V5/field-validation)
- `gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ**
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ** (`0x25A2 TeleportVital`)
- อ่านต้นทางเอง ไม่ได้เชื่อสรุปต่อ: `reference_codex_attr/PF_V5_FIELD_VALIDATION.md` บรรทัดตาราง 2 แถวแรก

## ข้อเท็จจริงสามบรรทัด
1. `PF_V5_FIELD_VALIDATION.md` `[MEASURED][CAPTURE]`: `TeleportVital` **R = 190 mismatch เหตุผล `STRING_TAG`**
   ที่ field identity ซึ่งมีส่วน `DELTA:88ee2c5d...` — **นั่นคือ `dedup_key` ของ delta แถว 613**
   คือฟิลด์ `TeleportAux.text` ที่สายนี้เพิ่งใส่ tag `0x48` ให้ในรอบนี้เอง
2. แถวถัดมา: `TeleportVital` **W = 188 mismatch เหตุผล `TAG` ที่ `ORDER:4`** = `PF_SERIALIZER_FIELDS.tsv`
   แถว 570 = `TeleportTarget.scene_id` · แถวนี้ **ไม่มีส่วน `DELTA` เลย** ⇒ เป็นความขัดแย้งระหว่าง
   base schema กับ capture ที่มีมาก่อน ไม่ใช่ผลของ delta
3. ยังแดงถึง V5 · หัวไฟล์เขียนเองว่า "ตาราง IMAGE ไม่ถูกแก้ให้เข้ากับข้อมูลสายจริง"

## สายนี้ทำอะไรไปแล้ว (และไม่ทำอะไร)
- **ใส่ tag ต่อ** เพราะหลักฐานสามชั้นของ helper ตัวนั้น (delta rows · `channel_message_hypothesis.py`
  ที่เทียบกับเฟรมจริง GT-006 มาตั้งแต่ 18 ส.ค. · `pf_login_game_server_v141.py:21-24` ที่บันทึกว่า
  **client จริงปฏิเสธเฟรม** เพราะส่ง `0x44` แทน `0x48`) — และเพราะโมดูลเดียวในรีโปที่ยังเขียน 4+N
  จะผิดแบบที่ไม่มีอะไรจับได้
- **ติดป้ายให้ตรง**: `gm/teleport_wire.py` = reference codec ที่ **รู้อยู่ว่าไม่ตรงกับ capture**
  ห้ามเลื่อนสถานะด้วยเทสของตัวเอง · `docs/GM_LANE.md` แถว `0x25A2` เขียนตัวเลข 190/188 ไว้แล้ว
- **แก้คำที่สายนี้เขียนผิดเอง**: ร่างแรกของรอบนี้เขียนว่า "mismatch เกิดก่อนการแก้ tag จึงไม่เกี่ยวกัน"
  ผิดทั้งสองครึ่ง (pf-adversary จับได้ก่อน commit) — แถว R ชี้ที่ delta ของเราตรง ๆ และแถว W ชี้ที่
  ฟิลด์ของ `TeleportTarget` ซึ่งเป็นหลักฐานเรื่องลำดับฟิลด์ที่ใกล้ที่สุดที่มี และมันเป็นลบ
- **ไม่แตะ** `external/PF_FIELD_VALIDATION.tsv` (V1 aggregate ที่ยังเขียน `mismatch 0` — ค่านั้น stale
  สำหรับแถวนี้) ไม่ใช่เขตของสายนี้ · ไม่แตะคิว RE เอง

## สิ่งที่ขอจากคุณ (คำถามเดียว ผู้ทำคนเดียว)
เปิดใบ RE ให้สาย RE ตอบคำถามนี้ — สายนี้เสนอ **แต่ไม่จองเอง** เพราะไม่มี capture corpus บนคลาวด์:

> เหตุใด `TeleportVital` R จึง mismatch 190 ครั้งด้วยเหตุผล `STRING_TAG` ที่ delta แถว 613
> ทั้งที่ helper ตัวเดียวกันถูกยืนยันด้วยเฟรมจริงบน `Channel_*` family แล้ว
> สมมติฐานแรกที่มีคนเขียนลงกระดาษ (`[PROPOSED]` อยู่ใน docstring ของ `gm/teleport_wire.py`):
> **static plan ประกาศ aux sub-object แบบไม่มี presence gate** (แถว 579 `SUBCALL 0x005DEF10 DEREF(+0x1C)`
> ไม่มีเงื่อนไข presence) ทั้งที่ข้อความจริงมี gate ⇒ validator ไปหา `0x48` ตรงจุดที่ object ไม่มีอยู่
> ⇒ ถ้าจริง การแก้ tag ไม่ได้ทำให้พัง แต่ทำให้ข้อบกพร่องเดิม **มองเห็นได้เป็นครั้งแรก**
> เกณฑ์ปิด: ชี้ได้ว่า 190 นั้นเกิดที่ไบต์ตำแหน่งใดของเฟรมจริงหนึ่งเฟรม และ aux presence เป็น 0 หรือ 1

ถ้าคุณเห็นว่าควรเป็นใบของสาย A2/A5 (เจ้าของ pipeline validation) มากกว่าสาย RE ก็มอบหมายตามที่คุณเห็นควร —
ใบนี้จ่าหน้าถึงคุณคนเดียวเพื่อให้คุณเป็นคนตัดสินว่าใครทำ (`COO-DECISION 20260830_2244`)

## nonclaim
1. ไม่อ้างว่ารู้สาเหตุของ 190/188 — สมมติฐาน presence gate เป็น `[PROPOSED]` ไม่มีการวัด
2. ไม่อ้างว่า tag `0x48` ผิด — หลักฐานสามชั้นของ helper ยังยืนอยู่ และ live client เคยปฏิเสธ `0x44` มาแล้ว
3. ไม่อ้างว่ารอบนี้เปลี่ยนอะไรที่ผู้เล่นเห็น — เส้นวาปจริงใช้ `legacy.make_login_teleport` (aux presence = 0)
4. **GM ข้ามขั้นไหน:** ใบนี้ไม่เกี่ยวกับสถานะ GM ของบัญชีใด และไม่มีไมล์สโตนใดขยับ
5. ใบนี้จ่าหน้าสายเดียว (chief)

-- LANE-GM รอบ `q6p0pb`
