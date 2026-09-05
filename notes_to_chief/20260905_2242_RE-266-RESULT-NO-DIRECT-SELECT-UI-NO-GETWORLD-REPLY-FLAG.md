[ถึง: LANE-UI | ADDRESSEE: LANE-UI | cc: chief, COO | จาก: RE runner บนเครื่อง Panya | 2026-09-05T22:42+07:00]

# RE-266 RESULT — true branch ของ `0x709E` ทำ session/transport handoff ไม่ได้เปิดหน้าเลือกตัวละครตรง ๆ; `GetWorldInfoVital` R ไม่มี pending-reply flag ใน natural path

**สถานะ: BOUNDED-NEGATIVE / STATIC ANSWERED (ไม่เขียน DONE เพราะไม่มี client-observable ตามเกณฑ์ใบ)**  
**checkpoint: method/cross-layer ceiling — ห้ามรัน image เดิมซ้ำจนกว่า chief เปลี่ยน objective หรือมี attended/capture ใหม่**

## START / input pins

- START `2026-09-05T22:34:10.086+07:00`; ticket snapshot `RE-266` 3,688 chars SHA-256 `28A7C19A9B0F13B94A3CC7FE3D35005B76CBB8C7467C690AA96B6E78E07AB781`.
- `GameClient/GameClient.local.bin` SHA-256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`.
- `external/PF_PROTOCOL_REGISTRY.tsv` SHA-256 `27DAAC0C6FBBC45D88281C31B98E3A8B56F421BD1E8BC16F970FDFF5716CFB4D`; `external/PF_SERIALIZER_FIELDS.tsv` SHA-256 `99282BDF3F492EAEBDBAB4918AECC0E37BF8EFB42B904B18E1BA306767B5C123`.

## ค้นก่อนถอด

- **ค้นชุดส่งมอบ `pf_bridge/external/` แล้ว:** สแกนทั้ง tree ครั้งเดียว 2,683 files / 930,201,065 bytes, inventory fingerprint (relative path + size + mtime_ns) `A5FD84555ACB17B1B5C1DE0F50AD7F6CF467183C1C5DF721193937E8F9839998`. เจอ registry/serializer rows ของ `ReturnSelectServerVital` และ `GetWorldInfoVital`, รายงาน RE-075 เดิม, และหลักฐานว่า `0x005DFD00`/`0x00708E20` ถูกจัดเป็น `CALL_UNCLASSIFIED`; ได้ verify span กับ image จริงด้านล่างก่อนใช้.
- **ค้น `pf_bridge/gamedata/` แล้ว:** สแกนทั้ง tree ครั้งเดียว 1,109 files / 15,319,585 bytes, fingerprint `D2BB6A2D098A9D49C4B17FB567066B158DC3B11D26ACBF2A9FF00D29FE1D1A94`. ไม่พบ semantic/crosswalk ของ vital, pending-reply, หรือ state transition นี้; hit `0x3D4B` ที่พบเป็นค่าพิกัดใน placement เท่านั้นและไม่ใช่ crosswalk.
- อ่าน mailbox root+consumed ตามเวลาและทำ content manifest: 4,937 files / 33,917,597 bytes / `5587219E21696CE9D6D5549ABDE74C905A1ABD7FADC408482FA6E66EF9186935`.

## Job 1 — downstream ของ true branch `ReturnSelectServerVital 0x709E`

`apply [0x005F1190,0x005F11D0)` (SHA `51EEC271...7DD25`) ยืนยัน RE-075: ต้องอยู่ใน typed `cStateCreateActor` ก่อนจึงเรียก `0x004B2A50`.

ที่ `[0x004B2A50,0x004B2AC5)` (SHA `72056825...85E39`) true branch ทำตามลำดับนี้:

1. เช็ก `vital+0x14 == 0x1E`; ไม่ตรงคืนทันที.
2. เรียก singleton getter `0x004011A0` แล้วเขียน `singleton+0xD8 = 1` (`0x004B2A5C..0x004B2A68`).
3. เรียก session preparation `0x005DCA40`, แล้ว `Sleep(2000)` (`0x004B2A68..0x004B2A84`).
4. ขอ object จาก pool `0x004B04A0`, ซึ่งสร้าง object vtable `0x00F30DAC` ผ่าน ctor `0x005F2B30`; vtable นี้มี serializer entry `0x005E6970` ของตระกูล `ReturnSelectServerVital`. จากนั้น copy incoming `+0x18`, `+0x1C`, และ string `+0x20` ลง clone (`0x004B2A86..0x004B2AB3`).
5. ส่ง clone เข้า dispatcher `0x005DD890` (`0x004B2AB3..0x004B2AC0`); span dispatcher `[0x005DD890,0x005DD96E)` SHA `1A91C8D4...D0C1C` เป็น session/transport routing และ ownership transfer ไม่ใช่ UI opener.

**คำตอบข้อ 1:** มี side effect จริง แต่ไม่พบ call เปิด UI/หน้าเลือกตัวละครใน downstream นี้. ยิ่งกว่านั้น apply gate บังคับว่าขณะเข้าทางนี้ client ต้องอยู่ใน `cStateCreateActor` อยู่แล้ว; จึงไม่ใช่เส้นที่ HOME ใช้กระโดดตรงไปหน้าเลือกตัวละคร. สิ่งที่พิสูจน์ได้คือ set session flag + prepare + รอ 2 วินาที + clone/dispatch vital. การที่ transport/session handoff อาจทำให้ state เปลี่ยนภายหลังเป็นคนละชั้นและยังพิสูจน์ไม่ได้จาก span นี้.

## Job 2 — `GetWorldInfoVital 0x3D4B` R-side

Natural outer codec `[0x005EB800,0x005EB8A9)` SHA `42022332...C93D1` อ่าน presence byte; ฝั่ง R ที่มี payload จัดสรร object ผ่าน `0x005E1FF0` แล้วเรียก nested codec `0x005E06B0`.

ใน nested R path `[0x005E06B0,0x005E0865)` SHA `2822A9B5...59C6`:

- `0x005DFD00` ที่ `0x005E07DC` เป็น pool allocate/reuse ของ record 0x3C bytes (`[0x005DFD00,0x005DFE0B)` SHA `8D92D032...EEA95`), ไม่ใช่ pending flag.
- `0x005DF420` ที่ `0x005E07FF` decode field ของ record (`[0x005DF420,0x005DF4D9)` SHA `DB16491D...73F04`).
- `0x00708E20` ที่ `0x005E0827` เป็น ordered-map insertion keyed by record `+0x10` (`[0x00708E20,0x00708F0F)` SHA `56574DB5...B9384`), ไม่ใช่ state-transition/reply gate.

Natural handler `[0x005F0B00,0x005F0C0B)` SHA `425ED743...E2E27` สร้าง local payload จาก `vital+0x14`, lookup receiver ด้วย string ตาม image คือ `SystemSetting_Switch`, **`SysetmSetting_Logout`** (สะกด `Sysetm` จริงในไบนารี), และ `SystemSetting_ESC`, แล้วเรียก vfunc `+0x210` ของ receiver ที่พบแต่ละตัว. ถ้า receiver ใดไม่พบก็ข้าม; handler ยังคืน `AL=1`. ใน full handler ไม่มี read/write pending-request flag, ไม่มี comparison กับ request-in-flight, ไม่มี clear-ack bit และไม่มี call ขอ state transition.

**คำตอบข้อ 2:** สอง `CALL_UNCLASSIFIED` ที่ใบชี้เป็น container mechanics; natural R handler fan-out ข้อมูลไปยังสาม SystemSetting receivers. ไม่พบหลักฐาน static ว่า reply `0x3D4B` เป็น ack ที่ gate dialog ถัดไป. นี่เป็น **ผลลบแบบมีขอบเขต** เฉพาะ codec + natural handler; ไม่ใช่ image-wide proof ว่าไม่มี subsystem อื่นรอข้อมูล world และไม่แทน attended observation.

## BUILD_IMPACT

- `GT-184`/`GT-186`: ห้าม retry `0x709E` จาก HOME ด้วย payload tweak; natural apply จะตก state gate ก่อน และ true branch ที่ผ่านไม่ได้เรียก selection UI โดยตรง.
- อย่าเพิ่ม server-side “wait for / ack `0x3D4B`” จากสอง `CALL_UNCLASSIFIED`; ทั้งคู่เป็น record allocation/map insertion.
- ถ้า LANE-UI ต้องตัดสิน client-observable ว่า flow หน้าเลือกตัวละครรอ world-info จริงหรือไม่ ต้องเปิด/ใช้ GT คู่ตามกติกา โดยวัด UI พร้อม wire แยกชั้น; static ใบนี้ถึง method ceiling แล้ว.

## Nonclaims

1. ไม่อ้างว่า `0x709E` ผิดสำหรับทุก state; อ้างเพียง natural apply และ downstream ที่ pin ไว้.
2. ไม่อ้างว่า session flag `+0xD8` แปลชื่อ semantic ใดเกิน “field written before prepare/dispatch”.
3. ไม่อ้างว่าไม่มี consumer อื่นของ world-info map ทั้ง image; ผลลบจำกัดที่ R codec และ natural handler.
4. ไม่ใช้ `FINDINGS_R40` ซึ่งเป็น wire/DB เก่าแทน client-observable.
5. ไม่จับคู่ id/เลข address จาก gamedata เพราะค่าเท่ากัน.

Verifier: `staged/re266_returnselect_getworld_static_verify.py` (ต้อง PASS กับ image SHA ข้างบน).
