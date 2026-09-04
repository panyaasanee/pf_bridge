[ถึง: chief cloud · COO · LANE-A | จาก: RE runner local · 2026-09-04T07:24+07:00]

# RE-227 RESULT — PARTIAL · STATIC HALF DONE; SAME-ROUND CAPTURE PENDING

- ใบ: `RE-227 CAPTAIN-REPORT-ON-ISLAND-CONTACT-001 [OPEN]`
- START: `2026-09-04T07:12:00.601+07:00`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB หรือ source/queue/git
- route note: หัวใบไม่มี route tag แต่ objective ระบุ `GameClient.local.bin`, static RE และเกณฑ์ static ชัดเจน จึงรับทำบน bridge ตามกติกา missing-route; ขอ chief เติม `STATIC-ON-BRIDGE` ตอนปิด/แก้หัวใบ
- verdict: **ปิดครึ่ง static ได้ แต่ยังปิดสองชั้นไม่ได้**. เส้นทาง NavigationEx ที่เป็นเจ้าของการชนเขต/เทียบท่าไม่ส่ง `TriggerVital 0x1FB2` ตอนเข้าเขต; server provision survey record มาก่อน, client เช็กระยะ `<=500` และเปิด prompt ภายในเครื่อง. เมื่อ callback ได้ result `1` จึงส่ง `NavigationEx_EnterInstanceVital` body `12 <opaque-u16-le> 0B 06`. Static ยังพิสูจน์ไม่ได้ว่าเฟรม scene-change จริงคือ `TeleportVital`; ต้องทาบ capture ของ `GT-228`/ใบคู่รอบเดียวกัน.

## Input pins

- ticket block (บรรทัดหัว RE-227 ถึง EOF, 4,073 chars): SHA-256 `e73677618913f15f698dc731e274bcc5bff4301837cede38dda7abca988ceB44`
- `GameClient.local.bin` 14,759,424 B: SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `external/PF_PROTOCOL_REGISTRY.tsv`: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `external/PF_SERIALIZER_FIELDS.tsv`: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `external/PF_FIELD_VALIDATION.tsv`: `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- gamedata rows used: `TEXTDATA_TH__Trigger_TIP.tsv` `bccbb0430a40793611d1bc864a7d81711fa46831c38c2f9769f9ffceaed7503f`; `TEXTDATA_TH__UI_MESSAGE.tsv` `2d97ff4836955e72bceBff2fcda4c1e703df880b8490d241624df20c34efa2c1`; `TEXTDATA_TH__SAILING_TEXT.tsv` `b3f1f3c88d61088337b2b6dc5dadfe3f0e7805eaf60b668a962437a06aeac9cd`; `CONSTDATA_TH__SAILING_RESULT.tsv` `9a047da026c12c2909e9c2725a19e49713161c5d9e10c108e386157446323d2c`

## ช่องค้นบังคับ

- **ค้น `pf_bridge/external/` แล้ว:** recursive text search ใน inventory 2,683 files / 930,201,065 B ด้วย `TriggerVital|TeleportVital|captain report|dock|docking|island contact|report captain|0x1fb2`; inventory fingerprint `762176848ccf3940dbf4d834367fbcfd59d570395bd8ee6212d901363037e29a`. พบ registry/serializer/validation ของ `TriggerVital`, `NavigationEx_RequestSurveyVtial`, `NavigationEx_AddSurveyDataVtial`, `NavigationEx_EnterInstanceVital`, `TeleportVital` และผลเดิม RE-086/087/090. ไม่พบ crosswalk ที่ผูก Trigger-TIP row `153/154` เข้ากับ field ของ `TriggerVital` หรือ NavigationEx.
- **ค้น `gamedata/` แล้ว:** recursive text search ใน inventory 1,109 files / 15,319,585 B ด้วยคำไทย/อังกฤษเรื่องกัปตัน, เทียบท่า, เกาะ และชื่อ message; inventory fingerprint `a1ef1e325f90d7ef28aefe30306d0dc94578525c840b892b287b4fd2aaf39e5e`. พบ `Trigger_TIP` id `153=Prison Exile Island`, `154=Spice Paradise Island` และ `UI_MESSAGE` id `1133="รายงานกัปตัน เรือกำลังเทียบท่า $V1"`. พบชื่อ/ข้อความ แต่ **ไม่พบ field crosswalk** จากเลขแถวเหล่านี้ไป protocol field; จึงห้าม join ด้วยเลขหรือชื่อคล้ายกัน.

## คำตอบ (ก) — ตอนชน/เข้าเขตเกาะ

### เส้นทางที่พินได้จริง

1. Server สามารถ provision `NavigationEx_AddSurveyDataVtial` เข้าคอลเลกชันของ `NavigationExModule_Client` ก่อนถึงจุด. Outer serializer `[0x00733570,0x00733614)` SHA `f8c751001819813123fa70eb2fee9ccf5d866418703dce39185dcf7b56af178c`; nested record serializer `[0x0072e590,0x0072e691)` SHA `5b714541671c8731a3b88df657089f97645ad1a6d2dc7ec9f06ee7ee271aa8f2` มี field ตามลำดับ:
   - `0B` byte @ record `+0x10`
   - `12` u16 @ `+0x12`, `12` u16 @ `+0x14`, `12` u16 @ `+0x16`
   - `2A` f32 @ `+0x18`, `2A` f32 @ `+0x1C`, `2A` f32 @ `+0x20`
   - `32` qword @ `+0x28`
   - `12` u16 @ `+0x30`
   เฉพาะ float triple มี consumer crosswalk จริงเป็น XYZ; field อื่นคง opaque.
2. Tick `[0x007321c0,0x00732586)` 966 B SHA `78753a3018463a9984c9f5fa8c8e7a7086dbb25938ad73bf0f10bc72cc2315d8` เลือก record ที่ byte `+0x10==1`, เทียบตำแหน่งผู้เล่นกับ XYZ และ branch ผ่านเมื่อ squared distance `<=250000` หรือระยะ `<=500`.
3. เมื่อเข้าเขต Tick ดึง opaque u16 `+0x12`, สร้าง local prompt/callback และตั้ง waiting flag. Recursive-CFG/full-function call census ครบทั้งสแปน (gap/error `0/0`) **ไม่มี direct call** ไป outbound submit `0x005dd800`, TriggerVital allocator หรือ TriggerVital serializer ใน contact branch; ผลลบนี้จำกัดเฉพาะ NavigationEx docking tick ที่พิน ไม่ได้มาจาก linear disassembly search.
4. Callback `[0x00730fe0,0x00731083)` 163 B SHA `29c2c7a765f757d41dfc7dac396c7ebb71156a2190283cf591c7ce96ea3b5951` ส่งเฉพาะเมื่อ callback/event `+0x94==1`; มันคัดลอก record u16 `+0x12` ไป EnterInstance `+0x14`, allocator คง byte `+0x16=6`, แล้วเข้าทาง submit. Serializer `[0x006a7310,0x006a735b)` SHA `17eb10304fdd86b85c22b4494b7fff4f6bd049e58a576a177d20d11cfce91cfa` ให้ body:

   `12 <opaque-u16 little-endian> 0B 06`

ดังนั้นคำตอบแบบ bounded คือ **ตอนชนเขตยังไม่มี outbound ในเส้นทางนี้; prompt เป็น local proximity gate และ outbound แรกที่พินได้อยู่หลังยืนยัน เป็น `NavigationEx_EnterInstanceVital`, ไม่ใช่ `TriggerVital 0x1FB2`.**

### `TriggerVital 0x1FB2` ที่ถอดแยกไว้

Registry พิน getter `0x006007a0`, vtable `0x00f31714`, serializer `0x006007c0`, handler `0x00710440`, runtime id global `0x01082844`. Serializer `[0x006007c0,0x0060082b)` SHA `2f30bd87df466c5df7df89818704ab636c9b875f4b5c74c01b62553a92791a12` มี body ครบทุก field:

`0F <u16@+0x14> 0B <u8@+0x16> 2A <f32@+0x18> 2A <f32@+0x1C> 2A <f32@+0x20>`

ยังไม่มี crosswalk ที่อนุญาตให้เรียก u16 หรือ byte ใดใน message นี้ว่า Trigger-TIP row id; จึง **ไม่อ้าง** ว่า `153/154` ถูกส่งใน `0x1FB2`.

## คำตอบ (ข) — prompt, confirm และ scene change

- **เฟรมเปิด prompt:** static ไม่พบ dedicated inbound frame ที่เข้ามา “ตอนชน” แล้วเปิด prompt. สิ่งที่พินได้คือ `AddSurveyData` provision record มาก่อน แล้ว client tick เปิด prompt เมื่อระยะผ่าน. การพบ `UI_MESSAGE[1133]` เป็นเพียงข้อความใน gamedata; ยังไม่มี code/field crosswalk พิสูจน์ว่ามันคือ prompt object เดียวกัน.
- **ปุ่มยืนยัน:** callback result `1` ส่ง EnterInstance body `12 <u16 copied unchanged from survey record +0x12> 0B 06`. Static พิสูจน์ gate และ byte shape แต่ไม่พิสูจน์ชื่อปุ่ม/การคลิกจาก client-observable.
- **เส้น `Main_Sail_Lookout/Survey` แยกต่างหาก:** RE-087 พินว่า Survey action ส่ง `NavigationEx_RequestSurveyVtial` body `0B 05` ผ่าน serializer `[0x00729790,0x007297b3)` SHA `ad65d125ab8a97db872ae5b2e957280a431d55beb7956050652a2d58dee633e9`; ยังไม่มีหลักฐานว่า UI นี้เป็น prompt “รายงานกัปตัน” จาก proximity path จึงไม่รวมเป็น timeline เดียวกัน.
- **เฟรมเปลี่ยนฉาก:** `TeleportVital` เป็น candidate ที่มี natural inbound handler แต่ static ยังไม่มี causal edge จาก EnterInstance request ไป Teleport response. Serializer `[0x005eb470,0x005eb609)` SHA `fbe813dbd1f9b94d87ee3c101867e8b12aaa36d69c08e68068c8ff06df990487` มีลำดับ field:
  1. `0B` top byte `+0x18`
  2. `0B` target-presence; ถ้ามี target: `12` scene_id u16 `+0x12`, `32` sequence qword `+0x18`, `0B` bytes `+0x10/+0x11`, `2A` XYZ f32 `+0x20/+0x24/+0x28` (nested span `[0x005df250,0x005df2f9)`, SHA `ec9a5421ad5304372e440ecbb35184d6e93624444a262b3058569a724df0b5ef`)
  3. `0B` aux-presence; ถ้ามี aux: wstring, u16, u32, u32, qword, u32 ตาม codec `[0x005def10,0x005defe9)`, SHA `105bad91394ee1dc636ef80cfe3444c293a4114d5f371fafe3ebc76ccc049c93`
  4. `0B` top byte `+0x20`, `0F` top u16 `+0x22`

ต้องใช้ capture เพื่อระบุว่า original/live server ตอบ message ใดและยืนยัน byte-for-byte; ห้ามยก Teleport codec นี้เป็นเหตุการณ์จริงก่อนเห็นสาย.

## Reuse verification

- RE-086 result SHA `ddf6d8385d10df41bc9d28514125dfa5a99ea76710b56fddefa5c3322f0737f9`; verifier `staged/re086_dock_trigger_static.py` SHA `82bf2fb70789d7f7bfb1eced77e0e0de1ebab9126de1483a1f4933f79390c02c`: **110 PASS / 0 FAIL**, exit 0.
- RE-087 result SHA `9e7b75e8f8a57fc4e7557cedee376a417773259f4e5662fba6c36fb4ae569a85`; verifier SHA `924bf4498d550f272026d56a4bd6b88957f068fae57a5804142eed344a3810d1`: **68 PASS / 0 FAIL**, exit 0.
- RE-090 result SHA `6c6b898be4220df7a84a42799e121cc1db143dbd5543bd420a50b1e93973a2a0`; verifier SHA `7578fd6ae41819e36dab7cef2408fbdf5cad65862b488d5d15460c0317be8e61`: **53 PASS / 0 FAIL**, exit 0.
- LANE-A table audit `20260904_0601...` is consistent: no committed placement/crosswalk maps trigger rows `153/154` to protocol or scene placement; COO accepted this at `20260904_0642...` and left M2 waiting on GT-228/capture.

## Nonclaims

1. ไม่อ้างว่า `TriggerVital 0x1FB2` ไม่มีทางถูกส่งจากส่วนอื่นทั้งโปรแกรม; อ้างเพียงว่า contact branch ของ NavigationEx tick ที่พินไม่ส่งมัน.
2. ไม่อ้างว่า Trigger-TIP `153/154` คือค่า protocol ใด แม้ชื่อแถวเข้ากับชื่อเกาะ; ไม่มี field crosswalk.
3. ไม่อ้างว่า survey-record u16 `+0x12` / EnterInstance u16 `+0x14` คือ island id, scene id หรือ Trigger-TIP id; พิสูจน์เพียง copy unchanged.
4. ไม่อ้างว่า callback result `1` มาจากปุ่มที่ผู้ใช้เห็นชื่อ “ยืนยัน”; static เห็นเพียง gate.
5. ไม่อ้างว่า `UI_MESSAGE[1133]`, `Main_Sail_Lookout` และ proximity prompt เป็น UI เดียวกัน.
6. ไม่อ้างว่า original server ส่ง AddSurveyData tuple ใด, ตอบ EnterInstance อย่างไร หรือส่ง TeleportVital จริง; ต้องมี wire capture.
7. wire/DB evidence และ client-observable evidence แยกชั้น; รอบนี้ไม่มีหลักฐาน client-observable ใหม่.

## Checkpoint / BUILD_IMPACT

- **PARTIAL แบบ method/cross-layer ceiling, ไม่ใช่ time checkpoint.** Static half จบแล้ว; ห้าม runner rerun ใบนี้จนมี capture/GT-228 result หรือ chief แก้ objective อย่างมีสาระ.
- สิ่งที่ค้าง: same-round capture ระหว่างเข้าเขต → prompt → confirm → scene change เพื่อทาบ actual hex กับ codec และระบุ message sequence จริง.
- **BUILD_IMPACT:** ฝั่ง server/build ควร provision `NavigationEx_AddSurveyDataVtial` ด้วย record/XYZ และรองรับ `NavigationEx_EnterInstanceVital(opaque u16 copied, byte=6)`. ห้าม implement docking ด้วย `TriggerVital id=153/154` หรือ compose Teleport เป็นคำตอบจากชื่อ/เลขเท่ากัน. ให้ GT-228/capture เป็นตัวตัดสิน outbound/inbound sequence และ scene-change vital ก่อนปิดงานสองชั้น.

สถานะที่ chief ควรกรอก: `RE-227 PARTIAL — STATIC PASS: NavigationEx AddSurveyData -> client proximity <=500 -> local prompt -> confirm sends EnterInstance body 12 <opaque-u16> 0B 06; CAPTURE/GT-228 REQUIRED FOR ACTUAL WIRE + SCENE-CHANGE JOIN`.
