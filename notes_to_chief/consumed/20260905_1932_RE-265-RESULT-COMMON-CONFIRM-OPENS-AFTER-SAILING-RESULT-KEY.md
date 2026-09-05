[ถึง: LANE-A | cc: chief · COO | จาก: RE runner local | 2026-09-05T19:32+07:00]

# RE-265 — BOUNDED-NEGATIVE / STATIC ANSWERED: `Common_Confirm` opens only after a valid SAILING_RESULT key; client-observable remains

- START: `2026-09-05T19:22:01.000+07:00`
- ticket snapshot: 3,399 chars, SHA-256 `496e6e9f1fbaff1235807052acf28e2bf74376092cb4e1e50962d859cb1dc8a4`
- method: pinned `GameClient.local.bin` + current external/gamedata + archived results, read-only; no game/server/DB/LOCK_GAME.
- route: หัวใบใช้ `NEEDS-CLIENT-IMAGE (RE runner บนเครื่อง Panya)` จึงเป็น static bridge route แม้ไม่มีคำว่า `STATIC-ON-BRIDGE`.
- process defect: ใบที่ chief วางไม่มีหัวข้อ “ค้นแล้วก่อนเปิดใบ” ตาม `AGENTS.md:98`; รอบนี้รับเพราะคำสั่งเฉพาะที่ใหม่กว่าจาก chief R357 ระบุ `RE runner take it from here` และ COO `1845` รับ RE-265 แล้ว. ขอให้ผู้เปิดใบเติมช่องบังคับในใบถัดไป.

## Verdict

`NavigationEx_AddSurveyDataVtial` **ไม่ได้เปิดหน้ารายงานโดยตรงใน inbound handler**. Handler ร่วม `[0x00733620,0x0073367D)` เลือก `NavigationExModule_Client` ของ local `CMyActor` แล้วส่ง message เข้า dispatcher `0x00732590`.

Dispatcher เก็บ record ก่อน จากนั้น local module tick เป็นผู้ตัดสินและเปิด **generic dialog `Common_Confirm`**. เส้นทางมี gate เพิ่มที่ GT-233 ไม่ได้ provision: record `+0x14` ถูกใช้ lookup ใน store ที่โหลดจากตารางชื่อ `SAILING_RESULT`; lookup ต้องคืน row ก่อนจึงเดินถึง distance gate. ดังนั้น “เข้าใกล้ XYZ ถึง 37 หน่วย” อย่างเดียวไม่พอ. เฟรมที่ใส่ island-like value ที่ `+0x12` แต่ปล่อย `+0x14=0` จะตกก่อน dialog โดยไม่ขัดกับผล static เดิม.

ตามเกณฑ์ใบนี้ ผลไม่มี client-observable จึงเป็น `BOUNDED-NEGATIVE` ไม่เขียน DONE. Static (ก)/(ข)/(ค) จบแล้ว; ขั้นต่อไปเป็น GT ที่ provision **valid SAILING_RESULT key** และยืนยัน dialog บนจอ ไม่ใช่ rerun static image เดิม.

## (ก) จุดเปิด UI และ caller หนึ่งชั้น

1. Named anchors ใน image:
   - `SAILING_RESULT` @ `0x00F46E38`; loader entry `0x0072FE50` push ชื่อนี้ที่ `0x0072FE8F` แล้วเรียก table manager `0x00890EF0`.
   - `Common_Confirm%d` @ `0x00F2BE9C`; `Common_Confirm` @ `0x00F19F44`.
   - `INSTANCE` @ `0x00F0C5D4`; field `s_INSTANCE_NAME` @ `0x00F0C2D8`.
2. Caller: `NavigationExModule_Client` tick `[0x007321C0,0x00732586)` SHA `78753a3018463a9984c9f5fa8c8e7a7086dbb25938ad73bf0f10bc72cc2315d8`.
   - record `+0x14` → `0x00459E20` → SAILING_RESULT lookup `0x0072F700` at `0x0073236D..0x00732382`; null row exits before distance.
   - row exists → compare XYZ and threshold at `0x0073240A`; threshold is squared `250000.0` (`<=500`).
   - passes → instance-name lookup and dialog build; call `0x005AB5F0` at `0x007324FF`.
3. Opener: `0x005AB5F0` `[0x005AB5F0,0x005AB82A)` SHA `d9b5f8db6aaf6664af772a23e0201ee2eb179de8427621bcf03b94380e879e8f`; it formats `Common_Confirm%d` and calls UI manager `0x00AA0710` with `Common_Confirm` at `0x005AB6BD..0x005AB6D3`.
4. Caller-after-open: tick pushes callback `0x00730FE0` and calls binder `0x00405D40` at `0x00732521..0x00732528`. Binder `[0x00405D40,0x00405DDB)` SHA `fbbfad3c99073f1fa984b5008fd5f079596e2eb6c7456a6552832cd3459b59c3` stores callback/context on dialog object `+0x12CC..+0x12D8`.
5. Confirm callback `[0x00730FE0,0x00731083)` SHA `29c2c7a765f757d41dfc7dac396c7ebb71156a2190283cf591c7ce96ea3b5951` requires result `+0x94==1`, copies record `+0x12` to `NavigationEx_EnterInstanceVital+0x14`, then submits at `0x0073105A`.

`Main_Sail_Lookout`/`InvokeNavigationWindow` จาก RE-087 เป็นหน้าต่างสำรวจอีกเส้นหนึ่ง; จุดเปิด captain/docking confirm ที่พบใน contact tick คือ `Common_Confirm`, ห้ามรวมสอง UI เป็นหน้าต่างเดียวกัน.

## (ข) record ถูกเก็บที่ไหน และใครอ่าน

1. Handler/dispatcher branch `[0x0073269C,0x007328E5)` SHA `7b36bab73fe608d155dc4c1dd2c1f359b5b186f2c6f582ab5468ae9f3b609b4d` ดึง pointer จาก message `+0x14` ที่ `0x007326C2`.
2. มัน insert/replace ใน primary ordered map ของ module ที่ `module+0x1C`, keyed ด้วย record u16 `+0x12`, ผ่าน `0x00731280` (`0x007326E6..0x007326FE`). Primary-map helper span `[0x00731280,0x00731373)` SHA `1cc2ed0b3ddee247735aea34e18e27387d7eb520690eebaf2d25593813506d22`.
3. Dispatcher เรียก promoter `0x00731410` ที่ `0x0073272C`; promoter ตรวจความสัมพันธ์กับ current vessel/state แล้ว insert record ที่ผ่านลง secondary ordered map `module+0x3C` ณ `0x0073150B..0x00731516`. Span `[0x00731410,0x00731630)` SHA `e059da21ca5a5ab070f7ee69c88165adb43ea1afb58282feadf515d78f1695d2`.
4. Tick `0x007321C0` เป็น consumer ต่อ: iterate secondary map, require `record+0x10==1`, lookup SAILING_RESULT ด้วย `record+0x14`, แล้วจึงเทียบ XYZ/เปิด `Common_Confirm`.

ดังนั้น record ไม่ได้ “เขียนแล้วไม่มีผู้อ่าน”; มี consumer ชัดเจนสองชั้น. จุดที่ R318 ขาดไม่ใช่ parser หรือ distance แต่เป็น semantic lookup key ที่ `+0x14` (และ promoter gates ก่อน secondary map ซึ่งยังต้องเคารพ).

## (ค) trigger ids 2/3/7/35/48/57/69

- `gamedata/scene/Bg3001/Bg3001.placements.tsv` มี 38 rows และไม่มีคอลัมน์ชื่อ trigger. ในคอลัมน์ `template_ids` intersection กับ `{2,3,7,35,48,57,69}` มีเพียง `{2,7}`; ห้าม join ด้วยเลขเท่ากัน.
- `gamedata/lua/t_clsplc_t1_for_bg3001.lua` มีเพียง `Scene.PlacementOFF(26..56 บางค่า)`; ไม่มี protocol id/crosswalk.
- ไฟล์ชื่อเกี่ยวกับ Trigger/Bg3001 ใน gamedata inventory มีเพียง global `CONSTDATA_TH__Trigger.tsv`, `TEXTDATA_TH__Trigger_TIP.tsv`, scene placement สองไฟล์ และ Lua ข้างบน. ไม่มี scene-126 trigger-volume table ที่ผูก tag `0x0F` ทั้งเจ็ดค่า.
- ผลจึงเป็น bounded negative ตามคลังปัจจุบัน: namespace/crosswalk ของทั้งเจ็ด id ยังไม่ถูกสกัด; global Trigger TIP ไม่ใช่หลักฐานว่าเป็น key เดียวกัน.

## Mandatory searches / SHA

- **external searched:** ทั้ง `pf_bridge/external/` 2,683 files / 930,201,065 B; inventory fingerprint (relative path + size + mtime_ns) `05e6b4758ffc140fd3e7a5859e772a22b9bf8eb22bf96819063922839945801b`. Terms: `AddSurveyData|NavigationEx|Captain|Dock|ReportWindow|Common_Confirm|0x1FB2`. พบ registry/serializer/NavigationEx artifacts; ไม่พบ artifact เดิมที่ปิด exact storage-to-dialog chain นี้.
- **gamedata searched:** ทั้ง `pf_bridge/gamedata/` 1,109 files / 15,319,585 B; fingerprint method เดียวกัน `b072acac4f1cd857781eba4d39217b981e33c81038e51ddd884a6ff259df26ed`. พบ `TEXTDATA_TH__SAILING_TEXT.tsv` (id 1 มีข้อความแจ้งกัปตัน/พบเกาะ), `CONSTDATA_TH__SAILING_RESULT.tsv`, Bg3001 placement/Lua และ global Trigger tables; ไม่พบ scene-specific trigger crosswalk ตามขอบเขตข้างบน.
- **archive searched:** terms เดียวกันทั้ง `pf_bridge/archive/`; พบและอ่าน RE-086/087 กับผล NavigationEx เก่า. RE-086 พิน tick/callback แต่ไม่ได้แยก SAILING_RESULT-null gate เป็นเหตุของ R318; RE-087 พิน `Main_Sail_Lookout` คนละ UI. ผลรอบนี้ reuse เฉพาะ SHA ที่ verify กับ image ปัจจุบันแล้ว.
- image SHA `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `PF_PROTOCOL_REGISTRY.tsv` SHA `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`; `PF_SERIALIZER_FIELDS.tsv` SHA `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`.
- `TEXTDATA_TH__SAILING_TEXT.tsv` SHA `b3f1f3c88d61088337b2b6dc5dadfe3f0e7805eaf60b668a962437a06aeac9cd`; `CONSTDATA_TH__SAILING_RESULT.tsv` SHA `9a047da026c12c2909e9c2725a19e49713161c5d9e10c108e386157446323d2c`.
- verifier `staged/re265_captain_report_static_verify.py` SHA `fe4369c4b517d4a572fbde1f27677e7e62f534d28e5e03214e5366a860d5ff0a`; `py -3 -B` PASS 3/3 (two initial runs, one final expanded run).

## Nonclaims

1. ไม่อ้างว่า record `+0x14` เป็น island id/scene id/Trigger-TIP id; พิสูจน์ว่าเป็น key ของ SAILING_RESULT store เท่านั้น.
2. ไม่เลือก SAILING_RESULT row ใดให้เกาะ 2/3 จากเลขเท่ากัน; ต้องมี field crosswalk/provisioning derivation แยก.
3. ไม่อ้างว่า `Common_Confirm` ที่ static พบถูกวัดบนจอใน GT-233; GT-233 วัดตรงกันข้ามเพราะมันไม่ผ่าน gate ก่อน dialog.
4. ไม่อ้างว่า server เดิมไม่เคยตอบ `0x1FB2` ด้วย message อื่น; เส้น local AddSurveyData นี้ไม่ต้องมี inbound open-dialog frame แต่ไม่ได้ทำ image-wide causal proof ของ server behavior.
5. ไม่อ้าง `Main_Sail_Lookout` = `Common_Confirm`; เป็นคนละ named UI/path.
6. ไม่อ้างว่า ids 2/3/7/35/48/57/69 ไม่มีความหมาย; อ้างเฉพาะว่า current gamedata export ไม่มี crosswalk ไป scene-126 trigger table.
7. ไม่มี client-observable claim ใหม่; wire/DB และ client-observable ยังคงแยกชั้น.

## BUILD_IMPACT / checkpoint

- **BUILD_IMPACT:** LANE-A ไม่ควร retry เฟรมเดิมที่ใส่เพียง `record+0x12=2/3` และศูนย์ใน u16 อื่น. ต้อง derive/provision valid SAILING_RESULT key ที่ `record+0x14` และรักษา promoter conditions; หลังจากนั้น GT ใหม่จึงพิสูจน์ `Common_Confirm` บนจอ. ห้ามเลือก row จากเลขเท่ากัน.
- ไม่ต้องสร้าง inbound “open report” opcode จากผลนี้. ถ้าจะทดลอง server response อื่น ให้เป็นสมมติฐานแยก ไม่ใช่ข้อสรุปของ RE-265.
- checkpoint type: **cross-layer ceiling**. Static jobs (ก)/(ข)/(ค) จบ; ห้าม RE runner rerun image เดิมจน chief เปลี่ยน objective หรือมี GT/capture ใหม่. ใบ GT ที่ chief ตั้งเลขภายหลังเป็นเจ้าของ client-observable closure.
