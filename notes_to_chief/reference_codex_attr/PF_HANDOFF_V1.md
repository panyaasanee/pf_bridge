# PF External Reverse-Engineering Handoff v1

วันที่ตรึงผล: 2026-08-22  
สถานะ: ปิดส่งมอบ v1 ตามคำสั่งล่าสุด; ไม่ไล่ Priority 1 ที่เหลือ 124 รายการต่อจนกว่าจะมีหลักฐาน runtime ใหม่

## 1. สรุปสำหรับผู้รับงาน

งานนี้สกัดทะเบียน protocol/attribute/module จาก `GameClient.local.bin`, ถอดโครงสร้าง serializer แบบ static, ตรวจเทียบกับ capture จริง, ตรวจ RTTI จาก dump สอง snapshot และทำดัชนี DATA XML โดยแยก evidence source ทุกชั้นออกจากกัน

ผลหลักของ v1:

- A1 ทะเบียน 519 รายการ
- A2 ตาราง serializer 6,931 แถว; numeric tag rows 2,783
- serializer ที่ไม่มี UNKNOWN 338/519; serializer ที่ยังมี UNKNOWN 181/519
- เมื่อรวม registry identity เป็นเกณฑ์ structural closure: ปิด 337/519
- Priority 1 มี 365 รายการ; ปิดเชิงโครงสร้าง 241/365 = 66.03%; เปิด 124
- A5 สแกน capture 1,772 ไฟล์ครบ; parse สำเร็จ 11,904 message instances; mismatch ที่พิสูจน์ได้ 0
- A6 ตรวจ dump 2 ไฟล์ครบ; พบ TypeDescriptor 3,121 ต่อ dump แต่พิสูจน์ complete vtable-to-RTTI chain ได้ 0
- DATA XML 290 ไฟล์: XML มาตรฐาน 287 ไฟล์/`SurfaceMask` 916 records และ pseudo-XML 3 ไฟล์/`Item` 303 records
- corrective review และ independent review ของ A5, A6, DATA และ priority schema ผ่านโดยไม่มี P0–P3 ค้าง

คำสั่งปิด v1 ยอมรับ 241/365 เป็นผลส่งมอบ ห้ามปรับเป็น 100% ด้วยการเดา, ตัด UNKNOWN ที่ยังพิสูจน์ไม่ได้ หรือผสม DUMP/CAPTURE/DATA เข้าแถว IMAGE

## 2. Erratum ที่ต้องอ่านก่อนใช้ offset

`GameClient.bin` และ `GameClient.local.bin` มีขนาดเท่ากัน 14,759,424 ไบต์ แต่ SHA-256 ต่างกัน:

- `GameClient.bin`: `C528BF43070E2789170F41B6E3E28CCEC6B57BDC594EE73DFA061188A5D1E4BD`
- `GameClient.local.bin`: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`

จึงเป็นคนละ IMAGE source ผล static A1–A4 ทั้งชุดนี้ผูกกับ `.local.bin` เท่านั้น เลข offset ที่ดูเหมือนอยู่ช่วงเดียวกันไม่รับประกันว่าไบต์ตรงกัน รายละเอียดและคำเตือนสำหรับผู้ตรวจอยู่ใน `PF_ERRATUM_TWO_IMAGES.md`

## 3. ผล re-derive รอบสุดท้าย

รัน `pf_extract_protocol.py` ครั้งสุดท้ายกับ `GameClient.local.bin` แล้วได้:

```text
image_sha256_before=9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
PF_PROTOCOL_REGISTRY.tsv rows=519
PF_SERIALIZER_FIELDS.tsv rows=6931
PF_SERIALIZER_FIELDS.numeric_rows=2783
PF_TAG_CENSUS.tsv rows=11
serializer_success=338
serializer_unknown=181
image_sha256_after=9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
```

จากนั้น re-derive A5 อีกครั้งจาก A2 รอบสุดท้าย ได้:

```text
capture_files=1772 blocks=51894 nested_declared=13220 nested_reached=12785 pass=11904 static_open=52775 mismatch=0 unresolved_after_open=435
```

A4 รอบนี้เป็นรอบสุดท้ายของ v1 และไม่ได้รันซ้ำหลังบันทึกตัวเลขข้างต้น ส่วนหัวข้อ 5–6 ของ `PF_EXTERNAL_REPORT.md` เป็น closure addendum ที่เพิ่มหลัง A4 เพื่อรวม priority/A5 โดยไม่แก้ A1–A3

## 4. ไฟล์ส่งมอบหลักและ hash

| งาน | ไฟล์ | จำนวน/สถานะ | SHA-256 |
|---|---|---|---|
| A1 | `PF_PROTOCOL_REGISTRY.tsv` | 519 IMAGE rows | `27DAAC0C6FBBC45D88281C31B98E3A8B56F421BD1E8BC16F970FDFF5716CFB4D` |
| A2 | `PF_SERIALIZER_FIELDS.tsv` | 6,931 IMAGE rows | `99282BDF3F492EAEBDBAB4918AECC0E37BF8EFB42B904B18E1BA306767B5C123` |
| A3 | `PF_TAG_CENSUS.tsv` | 11 IMAGE rows | `63BC9A039B5B35E5B2E1F08CE99E91B05DA6E6959B5B4F173EAC66B88AEA337A` |
| A4 | `pf_extract_protocol.py` | standard library only | `0BB792BB6B0561E11592AB7F8C93C65CD1E0FBA0210E2A6BF40C9E5A8579112E` |
| Priority | `PF_PROTOCOL_PRIORITY.tsv` | 519 IMAGE rows | `D9174BC27EBC1159A7B66BA3FC36B0D6025ECF72D9D963C3DEEE9BB780C3DE55` |
| A5 | `PF_FIELD_VALIDATION.tsv` | 1,038 CAPTURE rows | `080A5F32580DF575632FEE69D3F8FAA6E2E745AD1775D05DAF3E272E4E0941C3` |
| A5 | `pf_validate_capture_fields.py` | capture validator | `0166337CBC8E9E561D9D3CD5F02364F4ED43C49070644D5423387E87B793D8C8` |
| A6 | `PF_RUNTIME_CLASSMAP.tsv` | 6,244 DUMP rows | `C53A6EAF23911765EBABD5E86CCAECF827FFDD88A1F514FC3F0F3EA2C3484985` |
| DATA | `PF_DATA_EVIDENCE.tsv` | 290 DATA rows | `FBCD7BF14FD33C7340C6FD70F4A0AA5F1A6F7719C429335540383EAB1CCF5B1F` |
| Inventory | `PF_INPUT_INVENTORY.tsv` | 2,066 source-separated rows | `729B5E73383DE8FD6E0008875D4B9B685DE2AD8D72A55118AA862093F10259D1` |
| Report | `PF_EXTERNAL_REPORT.md` | หัวข้อ 1–6 | ดู manifest/final audit ของโฟลเดอร์ v1 |

ไฟล์ `.md` คู่กับ TSV อธิบายวิธี, ขอบเขต claim, hash binding และข้อจำกัด ห้ามใช้ตารางโดยไม่อ่านรายงานคู่กัน

## 5. อะไรยืนยันสองชั้นแล้ว

คำว่า “สองชั้น” ในที่นี้หมายถึงมีข้อเท็จจริง static แถว `source=IMAGE` และ observation แยกแถว `source=CAPTURE`; ไม่ได้หมายถึงนำสองแหล่งมารวมเป็นข้ออ้างแถวเดียว

- A5 มี `VALIDATED` 37 message/direction rows ครอบคลุม 29 message ไม่ซ้ำ
- ใน 29 message นี้ มี 28 message อยู่ Priority 1 และหนึ่ง message คือ `StartGameReq` อยู่ Priority 3
- parse สำเร็จรวม 11,904 message instances; มี nested frame ไม่ซ้ำอย่างน้อย 11,427 เฟรมที่ได้รับ validation สำเร็จอย่างน้อยหนึ่งรายการ
- Priority 1 ที่ capture-validated ได้แก่ `ActionVital`, `CBlockPointHelpVital`, `CHitParadeReqVital_JP`, `COnLandVital`, `CTracePathReqVital`, `Channel_ActorBoardcastMessageVital`, `Channel_GMGlobalMessageVital`, `Channel_GuildMessageVital`, `Channel_LocalTalkMessageVital`, `Channel_PartyMessageVital`, `CheckSecondPwdVital`, `ChooseNPC`, `DeleteActorVital`, `ItemOperateVitalReq`, `LSCN_LoginVitalReq`, `LSCN_SelectServerReq`, `LoginVerifyVital`, `LogoutVital`, `MiscNotifyVital`, `MusicControlVital`, `NotifyEnterCreateActor`, `QuestOperateVital`, `ReturnSelectServerVital`, `ShowMessageVital`, `TargetPosVital`, `TargetVital`, `TeleportCheckVital`, `TriggerVital`
- ไม่พบ field mismatch ในส่วนที่ parse ได้: 0 instance และ 0 distinct message/direction/field/reason point
- การที่ capture ตรงไม่ได้ยกระดับชื่อคลาส, runtime vtable หรือความหมาย tag ที่ capture ไม่ได้พิสูจน์ และไม่ได้แก้แถว IMAGE

## 6. อะไรยังเป็น static ล้วนหรือยังไม่ผ่านการยืนยัน

- structural closure ทั้งหมด 337/519 message; ในจำนวนนี้ 29 message มี capture validation เพิ่ม ส่วนที่เหลือยังไม่มีการยืนยันระดับเดียวกันจากสายจริง
- capture มี message ที่ถูกสังเกต 46 message ไม่ซ้ำ: 29 message มีอย่างน้อยหนึ่ง direction เป็น `VALIDATED`; 17 message หยุดเป็น `A2_STATIC_OPEN`
- 473/519 message ไม่ถูกสังเกตเลยใน capture ชุดนี้ที่ระดับ message identity; ต้องเรียก `NOT_OBSERVED` ไม่ใช่ PASS หรือ FAIL
- 52,775 observed message instances หยุดที่ A2 static-open และถูกกันออกจาก mismatch count; ตัวเลขนี้ใหญ่เพราะ outer/runtime messages ที่พบซ้ำจำนวนมาก ไม่ใช่ 52,775 ชนิด message
- A6 เป็น DUMP-only negative สำหรับสอง snapshot: มี TypeDescriptor แต่ไม่มี complete chain; จึงไม่มีชื่อ runtime class ใดที่ใช้ปิด IMAGE UNKNOWN ได้
- DATA evidence ยืนยันโครงสร้าง scene surface-mask และ avatar-offset files เท่านั้น ไม่ยืนยัน protocol field order หรือ runtime class identity

## 7. Priority 1 ที่หยุดไว้ใน v1

Priority 1 ปิด 241/365 = 66.03% และเปิด 124 รายการตามคำสั่งปิด v1

สถานะของ 124 รายการ:

- registry identity เปิด 11 รายการ
- serializer เปิด 123 รายการ
- `ItemAttr` มี serializer ปิดแล้ว แต่ vtable identity ยังเปิด
- 12 รายการถูกพบใน capture แต่ทั้งหมดหยุดเป็น A2 static-open
- 112 รายการไม่ถูกสังเกตใน capture
- 0/124 เป็น capture-validated

รายชื่อครบทั้ง 124 และ blocker รายตัวอยู่ใน `PF_PROTOCOL_PRIORITY.tsv`/`.md` ส่วน `PF_DUMP_REQUEST.md` แบ่งชื่อทั้ง 124 เป็นสถานะ runtime แบบไม่ซ้ำ รวมยอดตรวจได้ 124 พอดี และระบุเพดาน `0..N` ต่อ dump โดยไม่สัญญาผลล่วงหน้า

## 8. สิ่งที่ยังไม่รู้ — ต้องรักษา UNKNOWN ไว้

### 8.1 Registry identity ที่ยังไม่ครบ

มี 11 รายการที่ getter/vtable/serializer identity ยังไม่ครบ:

- `ItemAttr` — vtable UNKNOWN แม้ serializer ปิด
- `VitalData` — vtable และ serializer UNKNOWN; มี vtable candidates มากกว่าหนึ่ง
- `PartyAttr`, `ActorCommunityDataSet`, `ActorRelationshipData`, `Activity_BasicVital`, `Activity_ActorCommandVital`, `BlackMarketItem`, `ActorPetsCommonAttr`, `FightingDropModule_Client`, `FightingDropNotify` — getter/vtable/serializer UNKNOWN เพราะ static getter census ไม่ให้ candidate ที่พิสูจน์ได้

ห้ามเลือก candidate จากความใกล้ชื่อ, RTTI string ใกล้กัน, slot ที่บังเอิญเท่ากัน หรือ address proximity

### 8.2 Serializer UNKNOWN 181 รายการ

ยอด 181 เป็น message ที่มี UNKNOWN อย่างน้อยหนึ่งจุด ไม่ใช่จำนวน UNKNOWN rows ใน A2 แต่ละ message อาจมีหลาย blockerและหลาย direction

กลุ่ม blocker สำคัญที่ยังไม่รู้จริง:

- direct call ที่ static ยังพิสูจน์ไม่ได้ว่าเป็น sub-serializer หรือ non-wire
- indirect call/jump ที่ runtime-selected และยังผูก slot/target ไม่ได้
- vtable `+0x04` target หลัง `InterlockedDecrement` ที่ไม่มี runtime class/instance identity
- object/pointer alias ของ atomic, lock และ mutable-container helper กับ stream/buffer state
- subcall stream provenance ที่ formal forwarding ไม่เป็น singleton ครบทุก path
- direction W/R ที่ mode value หรือ branch proof ยังไม่เอกฐาน
- primitive ECX provenance ที่ reaching definition ไม่ชี้ formal stream เดียว
- nested helper semantics ที่ body พิสูจน์รูป operation ได้ แต่ target หรือ alias ยังอยู่ runtime
- registry serializer ที่ getter/vtable census ให้ศูนย์หรือหลาย candidate

ห้ามลด 181 ด้วยการเปลี่ยนชื่อ tag จาก `UNKNOWN(...)` เป็นคำที่ดูเฉพาะเจาะจงกว่าโดยไม่มี proof ใหม่

### 8.3 Dynamic target และ runtime identity

ภาพ static บอกได้ว่ามี indirect call, slot offset หรือ refcount operation แต่ไม่บอกค่าปลายทาง ณ runtime เสมอไป Dump สองไฟล์ปัจจุบันเก็บ memory ไม่ครบพอสำหรับ RTTI chain จึงยังไม่รู้:

- class ที่เป็นเจ้าของ vtable ของออบเจกต์มีชีวิต
- instance count ที่เชื่อมกับ proven class/vtable pair
- dynamic method target ของ call site ที่เกี่ยวข้องกับ 124 Priority 1
- object alias ว่า pointer ที่ helper แก้ไขเป็น stream, buffer, container หรือออบเจกต์ชนิดอื่น
- lifecycle phase ที่ทำให้ target เปลี่ยนตาม state

การมี decorated TypeDescriptor name ใน dump ไม่พอ ต้องมี COL, hierarchy, base array, self base และ vtable relation ครบตามโครงสร้างก่อนรับชื่อ

### 8.4 Capture coverage

ไม่มี mismatch ไม่ได้แปลว่าไม่มี mismatch ใน message ที่ไม่เคยเกิดหรือแขนงที่ไม่เคยวิ่ง สิ่งที่ยังไม่รู้จาก capture ได้แก่:

- 473 message ที่ไม่เคยสังเกตในชุด capture
- direction ที่อีกฝั่งหนึ่งเป็น NOT_OBSERVED แม้ message เดียวกันเคยเห็นอีก direction
- gate/optional field path ที่ input ชุดนี้ไม่เคยเปิด
- loop cardinality/order ที่ capture มีเพียงค่าบางช่วง
- nested 435 instances ที่อยู่หลัง static-open boundary
- ความถูกต้องของ 52,775 instances ที่ A2 ยังเปิด; พวกนี้ไม่ใช่ mismatch แต่ก็ไม่ใช่ validation pass
- framing รูปแบบอื่นนอก PC/DECOMPRESSED blocks ที่ parser ไม่ได้รับมอบหมายให้เดา

### 8.5 Tag semantics

ตาราง census วัด tag/length/frequency เท่านั้น Semantics ที่ยืนยันมีเพียงข้อที่ได้รับหลักฐาน producer/consumer ตรง เช่น `0x2A=float32` และ `0x12=uint16` ตามขอบเขตเดิม สิ่งต่อไปนี้ยังไม่รู้:

- ชนิดเชิงความหมายของ tag อื่นแม้ length จะคงที่
- signedness, enum domain, unit, scale หรือ sentinel value
- ความหมาย gameplay ของ offset ที่เห็นจาก object/stack expression
- ว่าฟิลด์ขนาดเท่ากันใน message คนละตัวมีความหมายเดียวกันหรือไม่

### 8.6 Order, gate และ field expression

- order ใน A2 เป็น static call-site order ไม่รับประกันจำนวน iteration หรือ dynamic order ของ loop
- gate ที่ static พิสูจน์ได้บอกเงื่อนไข branch/bit ที่เห็น แต่ไม่บอกความหมาย gameplay ของ bit
- symbolic expression เช่น heap/list/stack/deref บอกที่มาที่พิสูจน์ได้ ไม่ใช่ member offset คงที่โดยอัตโนมัติ
- path ที่ decoder/dataflow หยุดยังคง UNKNOWN; ห้ามเอา instruction ที่อยู่ใกล้กันมาเติมช่องว่าง
- empty claim ใช้ได้เฉพาะ exact allowlist/body ที่ validator รองรับ ไม่ใช่เพียง “ไม่พบ WRITE/READ”

### 8.7 ความสัมพันธ์ระหว่าง IMAGE, DUMP, CAPTURE และ DATA

- ไม่มี source ใดมีสิทธิ์แก้ข้อเท็จจริงของอีก source ย้อนหลัง
- CAPTURE ยืนยันการเกิดและ parse ของเฟรมหนึ่งชุด ไม่ยืนยัน class identity ใน dump
- DUMP บอก memory snapshot ไม่ยืนยันว่า build อื่นมี layout เหมือนกัน
- DATA บอกชื่อ/โครงสร้างไฟล์ข้อมูล ไม่ยืนยัน serializer implementation
- IMAGE บอก static code/bytes ของ `.local.bin` ไม่ยืนยันว่า branch นั้นเคยวิ่งใน capture
- cross-source correspondence ต้องมีรหัส/ชื่อ/field index ตรวจย้อนกลับได้และยังคงแถวแยก

### 8.8 ขอบเขต DATA v1

DATA evidence v1 ทำดัชนี XML ที่อนุมัติ 290 ไฟล์ ไม่ได้ตีความทรัพย์สินเกมทุกชนิดในโฟลเดอร์ Data และไม่ได้ใช้ไฟล์ binary asset เพื่อแต่ง protocol schema ขึ้นมา

สาม avatar-offset files เป็น pseudo-XML ที่มีไวยากรณ์ไม่มาตรฐานตรงกัน ตัว parser รายงาน `NONSTANDARD_GRAMMAR` โดยไม่แก้ไฟล์และไม่ซ่อมค่าให้ดูเป็น XML มาตรฐาน จึงยังไม่รู้ว่า consumer จริงยอมรับ grammar ผ่าน parser ชนิดใด

### 8.9 สิ่งที่ full-memory dump อาจยังตอบไม่ได้

แม้ได้ `MiniDumpWithFullMemory` ก็ยังไม่รับประกันว่าจะปิด UNKNOWN ทุกตัว เพราะ:

- ออบเจกต์เป้าหมายอาจไม่เกิดใน state ที่เก็บ
- class อาจไม่มี RTTI หรือ RTTI ถูก strip
- vtable อาจมีแต่ไม่มี object instance ที่เชื่อมได้
- static blocker อาจเป็น direction/gate/field order ไม่ใช่ runtime identity
- snapshot ไม่บันทึกลำดับ call หรือ branch history
- target อาจเปลี่ยนตาม state และต้องใช้หลาย dump

ดังนั้น `PF_DUMP_REQUEST.md` ใช้ candidate ceiling `0..N` และกำหนด stop rule หลังชุดสถานะหลัก ไม่ใช้จำนวน candidate เป็นคำสัญญาว่าจะ resolved

## 9. สิ่งที่เกือบเดา แต่ห้ามตัวเองไว้

รายการนี้สำคัญเท่าผลสำเร็จ เพราะเป็นเส้นแบ่งระหว่าง evidence กับเรื่องเล่าที่ดูน่าเชื่อแต่ตรวจไม่ได้

1. เกือบถือว่า executable สองไฟล์เป็นไฟล์เดียวกันเพราะขนาดเท่ากัน — หยุดไว้และ hash พบว่าต่างกัน
2. เกือบใช้ offset จาก `.local.bin` ไปตรวจ `GameClient.bin` — หยุดไว้เพราะ offset เดียวกันอาจมีไบต์ต่างกัน
3. เกือบเรียก dump สองไฟล์ว่า `MiniDumpNormal` จากค่า flags ที่อ่านผิดชื่อ enum — independent review แก้เป็น `MiniDumpWithDataSegs (0x1)`; ผลนับไม่เปลี่ยนแต่ถ้อยคำต้องถูก
4. เกือบเอา decorated TypeDescriptor names 3,121 ชื่อต่อ dump ใส่ `class_name` — หยุดไว้เพราะไม่มี complete vtable chain; ชื่อเหล่านั้นอยู่คอลัมน์แยกและ `class_name=UNKNOWN`
5. เกือบสรุปว่า executable ไม่มี RTTI เพราะ A6 ได้ vtable/class chain ศูนย์ — หยุดไว้; ผลลบจำกัดเฉพาะ memory ranges ของสอง snapshot
6. เกือบใช้ string proximity ตั้งชื่อ class/vtable — หยุดไว้เพราะ heuristic นี้ถูกระบุว่าผิดใน image นี้
7. เกือบนับ candidate ceiling ในใบขอ dump เป็น resolved count — หยุดไว้และรายงานช่วง `0..N` พร้อมเกณฑ์พิสูจน์ภายหลัง
8. เกือบถือ mismatch=0 ว่า A2 ทั้งหมดผ่าน — หยุดไว้เพราะมี static-open 52,775 instances และ message ไม่ถูกสังเกตอีกจำนวนมาก
9. เกือบนับ `A2_STATIC_OPEN` เป็น mismatch — หยุดไว้เพราะ parser ไม่มีสิทธิ์เดินผ่าน UNKNOWN แล้วกล่าวว่า field ถัดไปผิด
10. เกือบเรียก NOT_OBSERVED ว่า PASS หรือ FAIL — หยุดไว้; ไม่มีเฟรมคือไม่มี observation
11. เกือบแก้ A2 ให้พอดีกับ capture — หยุดไว้; ถ้ามี mismatch ต้องรายงานข้อขัดแย้ง ไม่ดัด static table
12. เกือบนำ CAPTURE status ใส่แถว priority IMAGE — หยุดไว้; `capture_status` ใน IMAGE row เป็นเพียง pointer ไปตาราง CAPTURE แยก source
13. เกือบตีความคำว่า `Vital` ในชื่อทั้งหมดว่า combat/HP semantics — หยุดไว้; priority grouping เป็นเพียง keyword rule ที่ผู้สั่งกำหนด ไม่ใช่ semantic proof
14. เกือบตีความชื่อ `Attr`, `Module`, `Protocol`, `Vital` ว่าทุกตัวเป็น network packet — หยุดไว้; ทะเบียน 519 ปะปนหลายบทบาท
15. เกือบเลือก vtable candidate จาก serializer/handler slot ที่เท่ากัน — หยุดไว้; slot equality ไม่ทำให้ candidate identity เอกฐาน
16. เกือบถือ direct call ที่ไม่มี known primitive ว่า non-wire — หยุดไว้; absence of matched primitive ไม่ใช่ negative proof
17. เกือบตัด `_invalid_parameter_noinfo`, constructor, destructor, `c_str`, interlocked, formatting, UI, `malloc` และ throw helpers ออกจาก UNKNOWN เพียงเพราะชื่อ import ดูไม่เกี่ยว wire — หยุดไว้เพราะ argument alias, return use และ path effect ยังไม่เอกฐาน
18. เกือบเรียก `InterlockedIncrement/Decrement` ว่า smart pointer/refcount/Release — หยุดไว้; รายงานได้เพียง exact operation, offset และ dynamic vtable target ที่พิสูจน์จาก body/import
19. เกือบเรียก mutable helper ว่า vector/list/map/tree/pool จากรูปร่าง loop/pointer — หยุดไว้; ชื่อ container เป็น semantics ที่ image ยังไม่พิสูจน์
20. เกือบถือ critical-section wrapper ว่า non-wire — หยุดไว้จนกว่าจะพิสูจน์ runtime pointer non-alias กับ stream/buffer
21. เกือบถือ SecurityCookie success path ว่าทำให้ helper non-wire ทั้งตัว — หยุดไว้เพราะ failure tail target ยังไม่พิสูจน์
22. เกือบถือ W/R capability ที่สืบทอดว่าพอแทน call-site proof — หยุดไว้; stream formal, mode และ direction ต้องผูกแต่ละ edge
23. เกือบ recurse subcall ไม่จำกัดความลึกหรือเลือกหนึ่ง path จากหลาย path — หยุดไว้เพื่อไม่ให้ cycle/ambiguity กลายเป็น field ปลอม
24. เกือบถือ indirect call ที่ไม่มี push ติดหน้าว่า stack-neutral — หยุดไว้; ยอมรับเฉพาะ exact allowlist/reaching proof
25. เกือบใช้ linear-disassembly failure เป็นหลักฐานว่าไม่มี pattern — หยุดไว้; negative census สำคัญใช้ byte-pattern/full-file guards ตามกฎเดิม
26. เกือบตีความ tag จาก length เช่น 4 ไบต์เป็น int32 — หยุดไว้; length ไม่พิสูจน์ชนิดหรือ signedness
27. เกือบตีความ heap/list/stack expression เป็น fixed OBJ offset — หยุดไว้; expression provenance กับ layout semantics เป็นคนละข้ออ้าง
28. เกือบถือ static order เป็น runtime loop order/cardinality — หยุดไว้; A2 บอก call-site order ภายใต้ขอบเขตที่ถอดได้
29. เกือบใช้ DATA filename/tag names เปลี่ยน IMAGE UNKNOWN — หยุดไว้; DATA correspondence ต้องเป็นแถวแยกและไม่เลื่อน evidence grade
30. เกือบซ่อม pseudo-XML ให้ parse ได้แล้วรายงานเป็น PASS — หยุดไว้และบันทึก grammar ผิดมาตรฐานตามจริง
31. เกือบให้ pseudo-XML classifier นับเพียง Item regex แล้วมองข้าม element แปลก — independent review บังคับ full-token fail-closed parser และ mutation tests
32. เกือบเผยแพร่ TSV/MD คนละ snapshot เมื่อ commit ไฟล์ที่สองล้ม — corrective review เพิ่ม staged publish, rollback และ residue guards
33. เกือบอ้างว่า A6 มี runtime class map ที่มีชื่อ เพราะ TSV มี TypeDescriptor names — หยุดไว้; map ที่ผูก vtable ได้ยังเป็นศูนย์
34. เกือบประกาศ Priority 1 สำเร็จ 100% ตามเป้าหมายเก่า — คำสั่งใหม่สั่งปิด v1 ที่ 241/365 และย้ำว่าห้ามดันด้วยการเดา

## 10. หลักฐาน runtime ที่ควรขอเมื่อเปิดงานรุ่นถัดไป

ใช้ `PF_DUMP_REQUEST.md` เป็นใบงานสำหรับผู้ทดสอบ เอกสารนั้น:

- ขอ dump ที่มี `MiniDumpWithFullMemory` bit
- ไม่เขียนขั้นตอน boot server/client
- ระบุสถานะที่มองเห็นบนจอ
- ระบุ object types ที่ต้องมีชีวิต
- ผูกสถานะกับชื่อ UNKNOWN ครบทั้ง 124
- บอก candidate ceiling ต่อ dump เป็น `0..N`
- กำหนด stop rule เพื่อไม่เก็บ dump เฉพาะทางต่อโดยไม่มีผลตอบแทน

Codex ห้ามรัน client เองทุกกรณี งานถัดไปเริ่มได้เมื่อผู้ทดสอบวางหลักฐาน runtime ใหม่ในเครื่องและอนุมัติขอบเขตอ่านอย่างเดียวอีกครั้ง

## 11. กฎส่งต่อ

- รักษาไฟล์ต้นฉบับใต้ `GameClient` เป็น read-only
- dump/capture ห้ามออกจากเครื่องและห้ามคัดลอก raw bytes ลงรายงาน
- ตรวจ `PF_ERRATUM_TWO_IMAGES.md` ก่อนตรวจ offset
- ใช้ `source` enum `IMAGE | DUMP | CAPTURE | DATA` เท่านั้น
- ห้าม merge evidence layers ในแถวเดียว
- ห้ามแก้ A2 อัตโนมัติเพื่อให้เข้ากับ capture
- ห้ามแก้ UNKNOWN ด้วยชื่อใกล้เคียงหรือ import semantics ที่ยังไม่มี alias/path proof
- หากพบ A5 mismatch ในอนาคต ต้องย้ายสรุปขึ้นเป็นเรื่องแรกของรายงาน
- หากไม่มีหลักฐาน runtime ใหม่ ให้ถือ v1 นี้เป็นกล่องปิดและไม่ต่อยอดการไล่ 124 รายการ
