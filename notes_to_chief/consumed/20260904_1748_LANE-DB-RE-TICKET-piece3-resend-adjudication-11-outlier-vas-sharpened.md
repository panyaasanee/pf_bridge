[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-DB | 2026-09-04T17:48+07:00]
[อ้าง: persistence_attr_compose.py:95-113 (## RESEND ADJUDICATION) · ค้างมาตั้งแต่รอบ `ub1j2l`/`b0ede7`/`1cajqi`/`f9p5fw` โดยไม่มีใครเปิดใบ]

# RE-TICKET — piece 3 (`0x309A` full block): 11 VA นอกคลัสเตอร์ ไม่ใช่คำถามเดียวอีกต่อไป แยกเป็นสองคำถามคนละรูป

## ที่มา

`compose_full_block`/`block_gaps` ค้างเพราะ `RESEND_ADJUDICATED: frozenset[int] = frozenset()` ว่างโดย
ตั้งใจ (docstring เดิม): 28 แถวที่มีค่า construction default มี 11 แถวที่ `write_site_va`/`producer_va`
ตกนอกสองคลัสเตอร์หลัก ⇒ โมดูลบอกตรง ๆ ว่า "เป็นคำถาม RE ที่สายนี้ตอบจากคลังเองไม่ได้" แต่ไม่เคยมีใคร
เปิดใบ RE ให้คำถามนี้จริง ๆ (ต่างจาก `RE-194` ซึ่งถามเรื่อง**ค่า**ของ x=7 คนละคำถาม)

รอบนี้สั่ง static-RE ไล่ทั้ง 11 VA จากคลัง commit แล้วเท่านั้น (`pf_rederive_attr_semantics.py` +
`PF_A2_ATTR_FIELD_DELTA.tsv` ใน `notes_to_chief/reference_codex_attr/` — ไม่แตะไบนารีไคลเอนต์ ไม่มีใน
คลาวด์) ผลคือ **คำถามเดิม ("codec write vs gameplay write") ไม่ตรงกับรูปที่ข้อมูลให้จริง** — ข้อมูล
แยกออกเป็นสามกลุ่ม ไม่ใช่สอง:

## ผลวัด (ทุกอันเป็น `[STATIC]` จากคลัง commit อ้างไฟล์:บรรทัด/แถว)

**กลุ่ม 1 — construction-time, แต่เป็นของ `CNetNPC` template ไม่ใช่ constructor กลาง (x=7, 11, 12)**
สาม VA นี้ (`0x0045C11A`/`0x0045C0D6`/`0x0045C0F9`) อยู่ใน initializer function ตัวเดียวกันของ `CNetNPC`
(span `0x0045BF40-0x0045C15D`, `pf_rederive_attr_semantics.py` แถว producer_va ของ x=7 ตรงกับ
`source_load_va=0x0045C109`/`producer_va=0x0045C11A` ในบล็อก `("CNetNPC", {...})` — ตรวจซ้ำแล้ว
`sed -n '5432,5449p'`) ไม่ใช่ตัว `default_writer_va` กลาง (`0x00464AAF-0x00464E16`) ที่ 17 แถวที่เหลือใช้
⇒ **ไม่ใช่ codec write แน่ ๆ แต่ก็ไม่ใช่คำถาม gameplay-tick เดิม** — เป็นค่าที่ populate จากตาราง MOBS
ตอนสร้าง NPC ต่างหาก คนละแหล่งจากค่า construction default 400.0/0/ฯลฯ ที่คอลัมน์นี้อ้างอิงอยู่

**กลุ่ม 2 — UI/gameplay consumer getter ที่ไม่มีเฟรมขาเข้าเกี่ยวข้อง (x=15, 30, 46, 49, 50, 51)**
ทั้งหกมี string assertion ชี้ตรงไปที่หน้าจอ/ปุ่ม UI ไม่ใช่ wire parser: x=15 `"GetPpClass"`
(แถว 5006-5007), x=30 `"Login_CharCreate_Panel_SecondPassword"`/`"TEXTBOX_INPUTPASSWORD"` (สอดคล้องกับ
`COO-DECISION 20260904_1150` ที่ตัดสินแล้วว่า x=30 = ช่องกรอกหน้าสร้างตัวละคร), x=46
`"ICON_Navy.tga"`/`"ICON_Pirate.tga"`, x=49/50/51 `"TEXTBOX_ADDRESS"`/`"TEXTBOX_AGE"`/
`"TEXTBOX_CONSTELLATION"` — ยืนยันตรวจซ้ำที่ `grep -n` ในไฟล์เดียวกัน หกแถวนี้ตรงกัน

**กลุ่ม 3 — ยังไม่มีข้อมูลอะไรเลย (x=26, x=27)**
ตรวจ `PF_A2_ATTR_FIELD_DELTA.tsv` แถวของ `ActorAttr@0x99`/`ActorAttr@0x9A` โดยตรง (ยืนยันด้วยตาเอง
รอบนี้ ไม่ใช่แค่เชื่อผลสรุป): `applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`,
`scope_status=UNKNOWN`, `scope_blocker="the field behavior/meaning is bounded, but no complete typed
owner/consumer-class census proves which concrete class attaches and consumes this Attr field"` — ไม่มี
RTTI ไม่มี string ไม่มี consumer class เลยแม้แต่ตัวเดียว คนละชั้นจากกลุ่ม 1/2 ข้างบนซึ่งอย่างน้อยยังมี
class/string ให้จับ

**ตรวจลบล้าง (negative check)**: เทียบทั้ง 11 VA (และ span ที่บรรจุมัน 15 span) กับ
`external/PF_SERIALIZER_FIELDS.tsv` (สารบัญ span ของ message serializer ที่ gate G4/G7 ใช้) ด้วย
range-intersection ตรง ๆ — **ไม่ตรงกับ span ไหนเลยทั้ง 15 span** (ควบคุมด้วยการค้นหาแถว
`CheckSecondPwdVital`/`EMPTY` ที่รู้อยู่แล้วว่าต้องเจอ เพื่อยืนยันว่า loader ไม่ได้พังเงียบ ๆ) — นี่คือ
bounded negative (พิสูจน์ว่าไม่อยู่ใน sarabanit ที่ commit ไว้ ไม่ใช่พิสูจน์ว่าไม่มีโค้ด parser ที่ไหน
แตะที่อยู่พวกนี้เลยในอิมเมจ ~10MB)

## ทำไมเรื่องนี้ไม่ปิดเองแม้จะตัด "codec write" ออกได้ 9/11

ตัดคำว่า "codec" ออกได้ไม่เท่ากับ "ปลอดภัยจะ resend" — กลุ่ม 1 (x=7/11/12) กลับชี้ไปทาง**ตรงข้าม**:
มันคือค่าเฉพาะของ NPC ตาม template ไม่ใช่ default กลางที่ 17 แถวที่เหลือใช้ ถ้า resend ค่า
`default_value` แบบเดียวกับ 17 แถวนั้นให้ actor คลาส `CNetNPC` จริง อาจจะผิดตัว (คนละแหล่งข้อมูล) —
เป็นคำเตือนใหม่ ไม่ใช่คำตอบ

## ขอ RE (สองใบคนละรูป ไม่ใช่ใบเดียวอีกต่อไป)

**(ก) กลุ่ม 1+2 (9 VA)**: เส้นทางส่ง `0x309A`/`UpdateAttrVital` ของสายนี้ (`compose_full_block`,
ถ้ายังมีผู้เรียกในอนาคต) เคยหรือจะเคยส่งให้ actor คลาส `CNetNPC` เลยไหม หรือส่งเฉพาะ player-class
(`CMyActor`/เทียบเท่า) เท่านั้น — ถ้าส่งเฉพาะ player-class จริง กลุ่ม 1/2 ทั้ง 9 แถวนี้ตกประเด็นไปเอง
(NPC-only/UI-only ไม่เกี่ยวกับ resend ของตัวละครผู้เล่น) โดยไม่ต้องพิสูจน์อะไรเพิ่มจากฝั่ง DB — คำถามนี้
เป็นเรื่อง call-site/RTTI ของฝั่งไคลเอนต์ ไม่ใช่ค่า จึงส่งเป็น RE ไม่ใช่สิ่งที่สายนี้เดาเอง

**(ข) กลุ่ม 3 (x=26, x=27)**: ยังไม่มี RTTI/consumer-class ผูกเลยแม้แต่ตัวเดียว ต้องเริ่มจากศูนย์
(หา concrete owner class ของ `ActorAttr@0x99`/`@0x9A`) — เป็นคำถามคนละระดับจาก (ก) ห้ามปนกัน

## ยังไม่อ้างอะไรเกินนี้ (nonclaims)

1. ไม่อ้างว่า `RESEND_ADJUDICATED` เติมได้แม้สักแถวเดียวจากผลรอบนี้ — ยังว่างถูกต้องตามเดิม
2. ไม่อ้างว่า negative check กับ `PF_SERIALIZER_FIELDS.tsv` พิสูจน์ว่าไม่มี codec function ใดแตะ
   ที่อยู่พวกนี้เลย — พิสูจน์แค่ว่าไม่อยู่ใน sarabanit ที่สำรวจไว้แล้ว
3. ไม่ได้ตรวจว่า `UpdateAttrVital`/`0x309A` เคยถูกส่งให้ actor คลาส `CNetNPC` จริงหรือไม่ในทางปฏิบัติ —
   นั่นคือคำถาม (ก) ข้างบน ยังไม่มีคำตอบ
4. ไม่ได้เดาความหมายของ x=26/x=27 จากชื่อฟิลด์ (`state_record_forced_flag`/
   `source_state_appearance_byte`) — ไม่มีหลักฐาน commit รองรับการเดานั้น

## กำหนดเมื่อไร

ไม่ผูก deadline ใหม่ — piece 3 ไม่มีกำหนดวันตาม `PANYA-DECISION 20260904_0233` (บันไดไมล์สโตนไม่มี
กำหนดวัน) และปัจจุบันไม่มีผู้เรียก `compose_full_block` ในโปรดักชัน (Door B ถอนออกไปแล้วตาม
`COO-DECISION 20260904_0546` ข้อ 2) ⇒ ไม่บล็อกอะไรที่มี GT ผูกอยู่ตอนนี้

— LANE-DB
