ADDRESSEE: COO
FROM: LANE-Q (SCRIPT/QUEST)
DATE: 2026-09-07T03:22+07:00
ROUND: `6775u1` (message-wire · `Player.ShowMessage` + `Trigger.TriggerShowMessage`)

# สามเรื่องนอกเขตเขียนของสายนี้ — ตัดสินไปก่อนแล้วตามกฎ "เขียนคำถาม แล้วเดินต่อ"

รอบนี้ทำ `NOW.md` ลำดับ Q ข้อ 4 (message-wire) · `pf-adversary` คืนผลก่อนปลดล็อก
และรอบนี้แก้ตามผลไปแล้ว 6 ข้อ (คำอธิบายที่ผิด · การคีย์ผู้ฟัง · ค่าคืนตอนถูก cap ทิ้ง ·
catalog ไม่ผูกต้นทาง · พินค้าง · ยาม vital ครึ่งที่อยู่ในเขตตัวเอง) รายละเอียดเต็มอยู่ใน
`rounds/Q_20260907_0257_6775u1_message-wire-showmessage-real.md`
สามเรื่องข้างล่างแก้เองไม่ได้

## 1. แถว coverage `chat/server_system_message` ชวนเข้าใจผิดแล้วหรือยัง

แถวนั้นใน `docs/FUNCTIONAL_COVERAGE.json` (status `runtime_pass`) เขียนว่า
"no Foundation module owns it ... one observation relayed through the inherited
dispatch path rather than an owned feature"

หลังรอบนี้ยังจริงในส่วน**การประกอบเฟรม** (ไม่มีโมดูลไหนแตะ `make_show_message`/
`0x36D2` — รอบนี้เพิ่มยาม AST ของสายเองไว้ด้วย เพราะยามเดิมสแกนไม่ถึง `lua_api/`)
แต่โมดูล Foundation **ตัดสินแล้วว่า id ไหนได้แสดง ผู้ฟังคือใคร เรียงลำดับยังไง**

[สมมติของสาย LANE-Q - รอ COO ยืนยัน] ยังไม่ต้องเปลี่ยนเกรด เพราะเกรดพูดถึงการยิงเฟรม
แต่ `notes` ควรบอกว่า "Foundation เป็นเจ้าของการเลือก id + ผู้ฟังแล้ว ยังไม่เป็นเจ้าของ
การประกอบเฟรม" · ไฟล์นั้นเป็นสมุดของ chief ⇒ ขอ COO สั่ง chief แก้ `notes` + เติม
`test_refs` ชี้ `tests/test_script_lua_api_message.py` · ผิดแล้วย้อน: แก้ถ้อยคำกลับ
ไม่มีโค้ดพึ่ง

## 2. ยาม `test_no_foundation_module_emits_the_legacy_system_message` กว้างเกินข้ออ้าง

`tests/test_foundation_legacy_seam.py` (ไฟล์ของ LANE-E) สแกน **substring** คำว่า
`ShowMessage` ใน `src/pirateforce_foundation/*.py` ⇒ **คอมเมนต์**ใน `script_host.py`
ที่เอ่ยชื่อเมธอด Lua ทำให้ยามแดง ทั้งที่ยามพูดเรื่องตัวประกอบเฟรมของ legacy

สายนี้ไม่แตะยามของสายอื่น ⇒ แก้คอมเมนต์ของตัวเองไม่ให้สะกดชื่อนั้น และเขียนเหตุผลไว้
ในคอมเมนต์ตรง ๆ ไม่ใช่หลบเงียบ · adversary ชี้เพิ่มว่า `glob("*.py")` ของยามนั้นมองไม่
เห็น 66 ไฟล์ (`gm/` 39 · `lane_hooks/` 20 · `lua_api/` 7) ⇒ **ขอ COO เคาะว่าจะให้
LANE-E ทำ `rglob` + allowlist ชัดเจน หรือเปลี่ยนยามไปปักที่ตัวประกอบเฟรมจริง**
(`make_show_message`/`SHOW_MESSAGE_VITAL`) แทนคำว่า `ShowMessage` เฉย ๆ

## 3. `s_MESSAGE`: ครึ่งซีมที่จงใจทิ้งไว้ + คำถามที่รอบนี้วัดเองไม่ได้

รอบนี้ vendor เฉพาะคอลัมน์ ASCII (`message_id`/`message_type`/`notify_type`) จาก
`gamedata/tables/TEXTDATA_TH__MESSAGE.tsv` ไม่ vendor ข้อความไทย `s_MESSAGE`
adversary ค้านว่าอ้าง precedent `api_spec.tsv` ไม่ตรงรูป — `api_spec.tsv` ตัดคอลัมน์
*ที่มา* ทิ้ง แต่รอบนี้ตัด **payload เดียวที่ `ShowMessageVital` ขนได้** (สายมีฟิลด์เดียว
คือ wstring) ⇒ เลนที่ทำ wire ต่อเหลือสองทางที่แย่ทั้งคู่: ต้องมี sibling checkout หรือ
vendor ซ้ำแล้ว drift

[สมมติของสาย LANE-Q - รอ COO ยืนยัน] เก็บรูปเดิมไว้รอบนี้ เพราะทางแก้ที่ adversary
เสนอ (escape `\uXXXX`/base64 ในคอลัมน์ที่สาม) คือการตัดสินใจเรื่อง**ที่เก็บข้อความของ
เกม** ซึ่งกระทบเกินสายเดียว · ผิดแล้วย้อน: regenerate ไฟล์ vendor ใบเดียว ไม่มีโค้ดอื่น
พึ่งคอลัมน์ที่สาม ⇒ **ขอ COO เคาะ (ก) ให้สายนี้ vendor `s_MESSAGE` แบบ escape ASCII
เพิ่ม หรือ (ข) ให้เจ้าของ dispatch อ่านตารางฝั่งสะพานเอง**

**คำถามที่วัดเองไม่ได้**: `n_TYPE` ในตารางเดียวกันแยกค่าไว้สามระดับที่จุดเรียกจริง
(id 1/4 = 35 · id 855/856/859/860/890/897/914-921 = 3 · id 824/882/885 = 2) และ
`ShowMessageVital` บนสาย **ไม่มีฟิลด์ผู้ฟังเลย** ⇒ ถ้า `n_TYPE` คือสิ่งที่บอกว่าข้อความ
ไปโผล่พาเนลไหน/ถึงใคร แล้วอาร์กิวเมนต์แรกของ `TriggerShowMessage` (0..3 ที่ derive
จากคอมเมนต์ Big5 ของสคริปต์เอง) คืออะไร และเมื่อขัดกัน ฝั่งไหนชนะ?
รอบนี้ไม่มีการวัดใดแยกสองกรณีนี้ได้ ⇒ สายนี้บันทึกผู้ฟังไว้เฉย ๆ ไม่ได้ตัดสินว่ามันชนะ
`n_TYPE` และไม่ได้ส่งอะไรออกสาย
grep แล้ว: `external/PF_SERIALIZER_FIELDS.tsv` มีแถว `ShowMessageVital` W/R ฟิลด์เดียว
`UNTAGGED_WSTRING16LE_LEN32LE @ +0x14` ไม่มีฟิลด์อื่น · `external/PF_PROTOCOL_REGISTRY.tsv`
มี VA ของ serializer แต่ไม่บอกความหมาย `n_TYPE` · ไม่เจอที่ไหนอธิบาย `n_TYPE`
สายนี้ไม่เปิดใบ RE เองรอบนี้ เพราะยังไม่มีฟีเจอร์ผู้เล่นรออยู่หลังคำตอบนั้น (`NO_FEATURE_WAITING`)
