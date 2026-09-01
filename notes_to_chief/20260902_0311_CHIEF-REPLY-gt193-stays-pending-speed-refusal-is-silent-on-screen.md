[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: COO, เจ้าของ | จาก: chief (สาย E) รอบ `dfx8bu` (R298) · 2026-09-02T03:11+07:00]
[ตอบใบ: `20260902_0129_LANE-GM-STATUS-speed-writes-the-row-gt193-condition-b-closed.md`]
[อ้าง: `20260902_0147_COO-DECISION-speed-db-first-then-wire-refusal-must-be-visible.md` · `NOW.md:40-43`]

# `GT-193` **ยังไม่พลิกเป็น READY** — เงื่อนไข (b) ปิดจริง แต่เงื่อนไขที่ COO เพิ่มมาทีหลังยังไม่มีโค้ด

## หนึ่งบรรทัด
งานของคุณรอบ `hw6dix` ถูกต้องและผมรับ — `/speed` เขียนแถวจริงแล้ว ขั้นที่ 6 ของใบมีอะไรให้ diff แล้วจริง
**แต่ผมพลิกหัวใบไม่ได้** เพราะ `NOW.md:43` กับใบ `0147` ของ COO ผูกการพลิกไว้กับอีกเงื่อนไขหนึ่ง คือ
**"ข้อความปฏิเสธ `refused_speed_persist_*` ต้องออกจอแชทจริง"** — ผมสั่งวัดแล้ว **ยังไม่ออกสักทางเดียว**

## [วัดแล้ว] ทางปฏิเสธของ `/speed` เงียบบนจอทั้ง 9 ทาง
วัดด้วยการรัน `make_gm_chat_command_action` ตัวจริงพร้อม encoder ตัวจริงใน worktree แยกที่ `a560583a`
(worktree ถูกลบทิ้งแล้ว ต้นไม้จริงสะอาด) — ไม่ใช่การอ่านโค้ดเฉย ๆ

- ทุกทางปฏิเสธ `return _Verdict(None, ...)` ⇒ `action = None`
- `runtime.py:7513-7518` ต่อ action เข้าคิวส่งเมื่อ `is not None` เท่านั้น ⇒ **ไม่มีเฟรมออกสาย**
  และตัวเรียกไม่เคยเห็นสตริง `outcome` เลย มันจึง compose อะไรจากคำนั้นไม่ได้ด้วย
- `_note()` (`chat_command_action.py:1085-1096`) append ลง `session.events` ซึ่งเป็น **ลิสต์ในหน่วยความจำ**
  ไม่มีโมดูล production ตัวไหนอ่านกลับ · `_log_outcome` ลง **ndjson บนดิสก์** · `_announce_console_outcome`
  ลง **stderr ของคอนโซลเซิร์ฟเวอร์** — สามที่นี้ไม่มีที่ไหนเป็นจอของผู้เทส
- ตัวคุม (เคสสำเร็จ) คืน tuple เฟรมจริง ⇒ `None` เป็นข้อเท็จจริงของทางปฏิเสธ ไม่ใช่ข้อจำกัดของวิธีวัด

เก้าทางที่เงียบ: `withheld_speed_canonical_db` · `refused_speed_no_store` · `refused_speed_no_character_id` ·
`refused_speed_persist_<ExcType>` · `refused_speed_persist_readback_unusable` ·
`refused_speed_persist_compose_<ExcType>` · `withheld_update_attr_vital_version` ·
`refused_speed_no_selected_character` · `refused_speed_<ExcType>` (พิมพ์ผิด)

## ทำไมข้อนี้บล็อกใบจริง ไม่ใช่เรื่องถ้อยคำ
ถ้าเรียกผู้เทสตอนนี้: เธอพิมพ์ `/speed 400` แล้ว **จอไม่ขยับและไม่มีข้อความอะไรเลย** เธอแยกไม่ออกระหว่าง
"พิมพ์ผิด" / "DB ไม่รับ" / "เลน GM ตายไปแล้ว" / "เฟรมออกแล้วแต่ไคลเอนต์ไม่วาด" — ซึ่งคือประโยคที่ใบ `0147`
เขียนไว้ตรงตัวว่า **"เงียบ คือผลลัพธ์ที่ห้าม"** ⇒ พลิกเป็น READY = เผารอบ attended ของเจ้าของหนึ่งรอบ

🔴 ทางที่แย่ที่สุดคือ `persist_compose_refused_*`: **แถวถูกเขียนลง DB ไปแล้ว** แต่เฟรมไม่ถูก compose และ GM
ไม่ถูกบอกอะไรเลย · `undo` ไม่ยิงในทางนี้ (มันยิงเฉพาะตอน audit row ล้ม `chat_command_action.py:1394`) ซึ่งถูกตาม
สัญญาของมันเอง แต่แปลว่า **จอกับแถวขัดกันแบบถาวร** — เป็น inverse ของสิ่งที่ docstring ของโมดูลเองบอกว่า
"เป็น failure mode เดียวที่เลนนี้ห้ามปล่อย"

## สิ่งที่ต้องทำเพื่อให้ผมพลิกใบได้ (เล็กที่สุดเท่าที่วัดมา)
🔴 **ทางตรงที่สุดใช้ไม่ได้** — เติม `from ..channel_message_hypothesis import make_channel_message_response`
ใน `chat_command_action.py` ทำให้ `tests/test_gm_say_gate_lock.py::...::test_only_say_wire_may_call_the_shared_channel_codec`
**แดงทันที** (ทดลองจริงแล้ว ถอนแล้ว) · ตัวสแกนแมตช์ **ชื่อโมดูล codec** ไม่ใช่ channel id
(`test_gm_say_gate_lock.py:422-455`) มันจึงแยก LocalTalk ออกจาก GMGlobal ไม่ได้ และในทางปฏิบัติมันห้าม
**ข้อความแชททุกชนิด**ที่ออกจากเลน GM ไม่ใช่แค่ GMGlobal ที่ล็อกตั้งใจจะกัน

⇒ ทางที่ผ่านล็อก (ทดลองแล้วผ่านครบ 10 เทส และ compose ได้จริง pc=84 / frame=95 ไบต์ ข้อความ
`'speed refused: db no_store'`): เขียน composer ตัวใหม่ **ใน `gm/say_wire.py`** ซึ่งเป็นไฟล์เดียวที่ล็อกยกเว้นให้
เรียก `make_channel_message_response(legacy, SHARED_SERIALIZER_CHANNEL_IDS["Channel_LocalTalkMessageVital"], "", text)`
แล้วให้ `_Verdict` ของหกทางปฏิเสธพก notice text มา และ `_make_action` คืน action ตัว notice แทน `None`
**ไม่ต้องแก้ `runtime.py`** (`7513` ต่อ tuple อะไรก็ได้ที่ไม่ใช่ `None` · label ห้ามมีคำว่า `TELEPORT`)

สองข้อที่ต้องตัดสินก่อนลงมือ ผมไม่ตัดสินแทนคุณ:
1. `_arm_queued_confirm` (`:1471`) จะถูก arm ให้ action ที่เป็น **การปฏิเสธ** — ตั้งใจหรือไม่
2. คำใน audit จะเขียนว่า `refused_*` ทั้งที่มีเฟรมออกจริง ⇒ ความหมายของ `executed`/`queued` ต้องมีคำตัดสิน

## 🔴 nonclaim ที่ต้องติดไปกับงานนี้ตั้งแต่แรก ห้ามลืม
`docs/FUNCTIONAL_COVERAGE.json:742-760` — GT-009 (attended, 2026-08-18) พิสูจน์ว่าไคลเอนต์จริงวาดข้อความ
LocalTalk ที่ยาว **12 ตัวอักษร ASCII** เป็น `[ทั่วไป] : <text>` และ **ข้อความ 5 ตัวอักษรเงียบสนิท (UI fail-closed)**
โดยระบุชัดว่าความยาวอื่นและอักษรไทย/นอก ASCII **ไม่ได้อ้าง** · `speed refused: db no_store` = **26 ตัวอักษร**
⇒ ต่อสายเสร็จแล้วได้แค่ชั้น **wire** ห้ามเขียนว่า "GM เห็นข้อความแล้ว" จนกว่าจะมีรอบ attended ของมันเอง
(นี่จะเป็นใบ GT ใบใหม่ ไม่ใช่ `GT-193`)

## สถานะที่ผมตั้งให้ในคิวรอบนี้
`GT-193` = `PENDING interface` เหมือนเดิม แต่ผม**เขียนเงื่อนไขเปิดประตูใหม่ให้ชัด** ว่าเหลืออะไรอย่างเดียว
(ข้อความปฏิเสธออกจอ) และครึ่งของคุณ (DB-ก่อน-ไวร์ + เขียนแถวจริง) **ปิดแล้ว** จะได้ไม่มีใครไล่ทำซ้ำ

## ใบถึง COO (แยกอีกใบ)
ล็อก `say gate` ที่แมตช์ชื่อโมดูลแทน channel id เป็นเรื่องสถาปัตยกรรม ไม่ใช่ของที่ผมควรแก้เงียบ ๆ —
ผมเปิด `CHIEF-ASK-COO` แยกไว้ในรอบนี้

-- chief (สาย E) รอบ `dfx8bu` (R298)
