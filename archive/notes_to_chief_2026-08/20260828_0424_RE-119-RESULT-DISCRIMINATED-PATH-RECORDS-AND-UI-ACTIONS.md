[ถึง: chief cloud · LANE-A · COO | จาก: RE runner local · 2026-08-28T04:24+07:00]

# RE-119 RESULT — PASS/DONE · 0x2F92 เป็น vector ของ discriminated path records; response handler ส่ง Run/EndFindPath

- ใบ: `RE-119 TRACEPATH-GO-BUTTON-REQREPLY-LAYOUT-001 [STATIC-ON-BRIDGE]`
- START ใบ: `2026-08-28T04:15+07:00`; ทำต่อหลังปิด RE-118/RE-117 ใน batch เดียวกัน
- วิธี: static/read-only เท่านั้น · ไม่เปิดเกม/server · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB/source/queue/git
- verdict: ปิด wire shape และ consumer path ได้จาก image ที่พิน. สี่ raw32 ไม่ใช่ `vec3+scalar` ที่ serialize พร้อมกัน: discriminator `u8@record+0x16` เลือก `kind=2 -> +0/+4/+8`, `kind=1 -> +0/+C`, ค่าอื่น -> `+0` เท่านั้น. พิกัดที่ response handler แปลงเป็น float จริงคือ signed `i16@+0x10/+0x12/+0x14`. Semantic ของ request `u16@+0x14=743` ยังแยก quest/NPC/list index ไม่ได้และปิดเป็น bounded negative ไม่เดา.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** ใน shared tree 30 ไฟล์ / 29,900,221 ไบต์ fingerprint `399098b4eb5a61ef07fffb5867ce3a8bb5eab0a68f6fb3a39fc452515fc9c61c`: registry rows `CGCTracePathModule/CTracePathVital/CTracePathReqVital`, serializer rows 5491-5536 และ validation. external ระบุ response OPEN เพราะ subcall/import blockers; รอบนี้ resolve direct W/R edges ด้วย pinned image spans. **ไม่เจอ** semantic crosswalk ของ request `+0x14` หรือข้อความไทย literal.
- **ค้น gamedata แล้ว: เจอ** ใน shared tree 1,109 ไฟล์ / 15,319,585 ไบต์ fingerprint `cf7d8e93bd798bc425ce346bdf8b2bbdc0a52b1632d89bd980580ae384660d8a`: `QUESTDATA_TH__QUEST.tsv` มี `n_ID=743` และ `CONSTDATA_TH__MOBS.tsv` ก็มี `n_ID=743` (`籠裡的死囚犯`). **ไม่เจอ** TracePath/0x4391/0x2F92 crosswalk หรือ column ที่ผูก request field นี้กับตารางใดตารางหนึ่ง; numeric equality จึงใช้พิสูจน์ semantic ไม่ได้.

## T0 — input/SHA control

- image `GameClient.local.bin` SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`, ImageBase `0x00400000`
- queue SHA `cfb53ab44409979d0f62cfb7e5d80fac3ecae2bafc9efb82dc0d7faaccb64719`
- external registry / serializer / validation SHA `27daac0c...cfb4d` / `99282bdf...c123` / `080a5f32...41c3`
- QUEST/MOBS table SHA `cc992728...527bd` / `3c0d33d6...3916b`

## T1 — CTracePathVital W/R และ container

wrapper `0x006EC0D0` บวก object `+0x14` แล้ว dispatch ตาม mode:

- W: `0x006EC0DA..E8 -> 0x006EBD50`
- R: `0x006EC0EB..F9 -> 0x006EC050`
- W span `[0x006EBD50,0x006EBE64)` SHA `1940cd4500e3218d701abafa56a82ca6a45b1147143e21e4ad2d97ae27724f28`
- R+wrapper span `[0x006EC050,0x006EC0FC)` SHA `e2e745981e5b98273fce8e9f2b5158c1af41e4ed329398d8f90568ddbb7bb4a3`

ทั้งสองขาเริ่มด้วย `tag 0x12 / width 2` เป็นจำนวน records. ตัว vector มี begin/end/capacity ที่ response object `+0x14/+0x20`; loop stride `0x18`. R สร้าง local record 24 ไบต์, เรียก shared reader แล้ว append ผ่าน `0x006F8B10`; call นี้คือ vector append ไม่ใช่ field serializer จึงไม่เพิ่ม bytes บน wire. นี่ resolve `direct_call_not_proven_serializer`; invalid-parameter calls อยู่เฉพาะ fail-fast bounds/invariant branches และไม่มี wire primitive บน branch นั้น.

## T2 — record layout; สี่ tag 0x14 ไม่ใช่ vec3+scalar พร้อมกัน

shared W/R serializer `[0x006EB960,0x006EBA88)` SHA `b95745c2130cb09405d30553e0c236b440b3058acab5de779ce67e6a39e19ba8` ใช้ wire order ต่อ record:

| order | offset | tag/width | gate |
|---:|---:|---|---|
| 1 | `+0x16` | `0x08` / 1 | always; discriminator |
| 2 | `+0x10` | `0x0F` / 2 | always |
| 3 | `+0x12` | `0x0F` / 2 | always |
| 4 | `+0x14` | `0x0F` / 2 | always |
| 5 | `+0x00` | `0x14` / 4 | always |
| 6 | `+0x04` | `0x14` / 4 | only `kind==2` |
| 7 | `+0x08` | `0x14` / 4 | only `kind==2` |
| 6 alt | `+0x0C` | `0x14` / 4 | only `kind==1` |

tag `0x14` พิสูจน์ได้เพียง raw 32-bit. Consumer `0x006EAC47..ACB3` แปลง signed words `+0x10/+0x12/+0x14` ด้วย `cvtsi2ss` เป็น float vec3 และส่งพร้อม low `u16` ของ `record+0` เข้า `0x0044A0C0`. จึงหักสมมติฐานเดิม: waypoint position ที่ handler ใช้ไม่ใช่ raw32 `+0/+4/+8`; semantic เต็มของ union payload ยังไม่ควรตั้งชื่อเกิน `kind1/kind2 raw32 payload`.

## T3 — response consumer และ UI action

registered response handler `[0x006EA9E0,0x006EACD3)`:

1. resolve `CGCTracePathModule`, copy vector จาก response `+0x14` ไป module `+0x20` ผ่าน `0x006EA280`, แล้ว set module state `+0x1C=0`.
2. response vector ว่างและ module ไม่อยู่ใน runnable state -> lookup UI object UTF-16 `Main_FindPath` แล้ว dispatch action `EndFindPath`.
3. response vectorไม่ว่าง -> lookup objectเดียวกันแล้ว dispatch `RunFindPath`.
4. ถ้ามี record จะดึงพิกัด signed i16 triplet และ low u16 ของ `+0` จาก endpoint recordไป `0x0044A0C0`; module handler `0x006EACE0` จากนั้น consume vector `+0x20` เป็น state machine ต่อ ไม่ใช่รอ serverตอบทีละ waypoint.

string VAs: `Main_FindPath=0x00F2F918`, `EndFindPath=0x00F19588`, `RunFindPath=0x00F195A0`. ค้น literal `กำลังค้นหาเส้นทาง` ใน image ทั้ง UTF-8/UTF-16LE/CP874/TIS-620 และ external/gamedata แล้วไม่เจอ. ดังนั้นพิสูจน์ได้ว่า response handlerสั่ง UI actions สองชื่อ แต่ **ไม่อ้าง** ว่า action ใดลบ text node ภาษาไทยโดยตรง; การหายจริงยังเป็น client-observable.

## T4 — request `u16@+0x14=743` bounded negative

request constructor `0x006EBA90` zeroes fields `+0x14..+0x24`; serializer `[0x006EBAF0,0x006EBBF7)` เขียน `+0x14` เป็น first `tag 0x0F/u16`. capture มี 743 จริง แต่ image registration/serializer pathไม่มี field-name crosswalk และ gamedataให้ทั้ง `QUEST.n_ID=743` กับ `MOBS.n_ID=743`. UI context "เลือก NPC แล้ว GO" เป็น hypothesis ไม่ใช่ proof. สถานะจึงเป็น:

- quest id: compatible แต่ unproved
- NPC `n_ID`: compatible แต่ unproved
- list index: ยังตัดทิ้งไม่ได้จาก static evidence ที่อ่าน
- วิธีปิด: instrument producer assignment ก่อน send หรือ attended สลับเลือกสองรายการที่ quest/NPC IDs ไม่ชนแล้วเทียบ outbound field; ห้ามใช้เลข 743 เดิมตัดสิน

## verifier / reproducibility

- `pf_bridge\staged\re119_tracepath_layout_static.py`: pins image + 3 serializer spans + branches + handler actions + table collision; PASS `checks=30 pinned_spans=3`
- `pf_bridge\staged\re119_disasm_probe.py` และ output `.txt`: targeted disassembly ของ shared/W/R/response/module/request envelope
- `pf_bridge\staged\re119_string_probe.py`: string/Thai-literal probe
- verifier รันอิสระสองครั้ง exit 0/0 ก่อน closeout; source inputsจะตรวจ SHA ซ้ำปลายรอบ

## nonclaims

1. ไม่อ้างว่า `record+0` คือ scene/map/NPC id; handlerใช้เพียง low u16 ร่วมกับ vec3 และไม่มี semantic label.
2. ไม่อ้าง raw32 fields เป็น IEEE float แม้ tag 0x14; primitive เดียวกันใช้ raw 4 bytes และ branchนี้ไม่มี typed arithmeticพอปิดชนิด.
3. ไม่อ้าง serverตอบ empty vector แล้ว auto-walk; empty pathเลือก `EndFindPath` เท่านั้น.
4. ไม่อ้าง `RunFindPath` ทำให้ข้อความไทยหายบนจอจริง; static พิสูจน์ action dispatch ไม่ใช่ rendering.
5. ไม่อ้าง 743 เป็น NPC/quest/list indexจาก numeric equality และไม่เสนอ hardcode 743.
6. ไม่อ้าง capture validation ของขากลับ; `CTracePathVital W/R` ยัง `NOT_OBSERVED` ใน capture ledger.

## BUILD_IMPACT

**BUILD_IMPACT:** สาย A เขียน encoder `0x2F92` เป็น `u16 count` ตามด้วย records ขนาด logical 0x18 และ conditional fieldsตาม discriminatorข้างบนได้; safe UI-only fallback คือ empty vectorเพื่อให้ clientเข้า `EndFindPath`, แต่ actual auto-walkต้องมี provenance ของ `record+0`, discriminator และ payloadจาก producer/attended differential ก่อนส่ง nonempty response. ห้ามใช้ `743` เป็น NPC idโดยอัตโนมัติ.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-119 PASS/DONE — 0x2F92 DISCRIMINATED RECORDS; REQUEST 743 SEMANTIC BOUNDED`.
