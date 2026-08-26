[ถึง: chief cloud · COO · LANE-NAVIGATION | จาก: RE runner local · 2026-08-27T00:56+07:00]

# RE-087 RESULT — PASS/DONE · CAPTAIN-REPORT ACTION IS NOT LOCAL-ONLY · SURVEY REQUEST BYTE `5`

- ใบ: `RE-087 CAPTAIN-REPORT-WINDOW-001 [STATIC-ON-BRIDGE]`
- วิธี: static/read-only เท่านั้น · ImageBase ของ VA ทุกจุดด้านล่าง = `0x00400000`
- verdict หนึ่งบรรทัด: หน้าต่าง `Main_Sail_Lookout` ผูกกับ `MainSailLookoutEventHandler`; action ชื่อ `Survey` ไม่ได้จบแบบ local-only แต่สร้าง `NavigationEx_RequestSurveyVtial` แล้วเข้าทางส่ง outbound. Serializer body มี field เดียว tag `0x0B`, 1 byte, object `+0x14`; path จากปุ่มกำหนดค่านี้เป็น `5`. ค่า `5` ยังเป็น opaque selector — ไม่มีหลักฐานให้เรียกว่า confirm flag หรือ island id.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** registry row ของ `NavigationEx_RequestSurveyVtial` (name VA `0x00F46FE0`, id-global `0x01089668`, vtable `0x00F46E5C`, serializer `0x00729790`, handler `0x00733620`) และ serializer W/R อย่างละหนึ่งแถว: order `1`, tag `0x0B`, field `+0x14`, len `1`. `PF_FIELD_VALIDATION.tsv` ยังเป็น `NOT_OBSERVED` ทั้ง W/R และ 0 capture frame; จึงใช้ registry/serializer เป็น crosswalk แล้ว verify กับอิมเมจ ไม่อ้าง live wire observation.
- **ค้น gamedata แล้ว: เจอ** `TEXTDATA_TH__SAILING_TEXT.tsv` 8 แถว รวม id `1` ข้อความแจ้งกัปตันว่าพบเกาะ/เตรียมจอด และ id `7` แจ้งกัปตันว่าเรือเทียบท่า Port Royal; พบ `CONSTDATA_TH__SAILING_RESULT.tsv` 138×19 และดัชนี `SAILING_RESULT`/`SAILING_TEXT`. ในชุดที่ค้นไม่พบ field จริงที่ crosswalk text/scene/result id เหล่านี้ไป `Main_Sail_Lookout` หรือ request byte `5`; จึงไม่ join ด้วยเลข id หรือคำที่คล้ายกัน.

## T0 — จุดเริ่มจาก text และชื่อจริงในอิมเมจ

- strings ในอิมเมจ: `Survey` @ `0x00F46A28`, `SAILING_RESULT` @ `0x00F46E38`, `Main_Sail_Lookout` @ `0x00F46EA4`, `InvokeNavigationWindow` @ `0x00F46F14` และ RTTI `.?AVMainSailLookoutEventHandler@@` @ `0x010273B8`.
- image-wide dword xrefs ครบ: `Survey` → `0x0072D6C8,0x00731931`; `Main_Sail_Lookout` → `0x00730EAD,0x00731AE8,0x00732634,0x00732755,0x00732860,0x00732B3C`; `InvokeNavigationWindow` → `0x00731ACD,0x00734A2D`; `SAILING_RESULT` → `0x0072FE90`.
- ชื่อ text-side ช่วยชี้ namespace sailing แต่ไม่มี direct row-id → UI-class crosswalk; ข้อสรุป packet ด้านล่างมาจาก control flow ของ UI/module ไม่ได้มาจากการเดาความหมายของข้อความ.

## T1 — UI action → outbound request และ field

### event handler ของหน้าต่าง

`MainSailLookoutEventHandler` `[0x0072D660,0x0072D751)` SHA-256 `c34e97e455094952f44fd3a64c4cf679ffd0ef9946711e0d302209cceb4c8186`:

- `0x0072D6AB` เทียบ UI event token กับ global `0x01090DC0`; `0x0072D6BA` แยก action source ที่ผูกไว้ใน handler.
- action หลัก push string `Survey` @ `0x0072D6C7`, ดึง `NavigationExModule_Client` จาก `this+0x8E0` แล้วเรียก vtable slot `+0x40` @ `0x0072D6E9-0x0072D6F9`.
- source อีกตัวที่ `this+0x24` ไป host virtual `+0x20C` @ `0x0072D717-0x0072D727`; ใบนี้ไม่ตั้งชื่อ semantic ของทางนั้นเกินว่า alternate/close-like UI path.

### module command และ send chain

`NavigationExModule_Client` command handler `[0x007318C0,0x00731C0E)` SHA `154ecf354515f92eac01c5c38b3c7a8b3921c62c8298c8d6c641c354c08b573b`:

- branch `Survey` เทียบ command string @ `0x00731930-0x00731936`; หลัง gate ภายใน branch แล้ว call allocator/factory `0x00730B00` @ `0x00731979`.
- object ที่ได้ถูกส่งต่อ `push edi` → `0x004011A0` → shared outbound submit `0x005DD800` @ `0x0073199B-0x007319A3`. นี่พิน direction ของ action นี้เป็น client→outbound; ไม่ได้อาศัย W/R label เพียงอย่างเดียว.
- branch แยก `InvokeNavigationWindow` @ `0x00731ACC` เปิด UI ชื่อ `Main_Sail_Lookout` ผ่าน `0x00AA0710` @ `0x00731AE7-0x00731AF1`.

### request object และ serializer

- allocator/factory `[0x00730B00,0x00730BEC)` SHA `842f90d005c2f16452036ade80dc163eaf43c09e157cfd8a277edb3061e27f04`: ทั้ง fresh/reuse path ตั้ง vtable `0x00F46E5C` และ `byte [object+0x14] = 5` (`0x00730B50/56`, `0x00730BC9/CF`). Registry crosswalk vtable นี้ไป `NavigationEx_RequestSurveyVtial` โดยตรง.
- serializer `[0x00729790,0x007297B3)` SHA `ad65d125ab8a97db872ae5b2e957280a431d55beb7956050652a2d58dee633e9`: body มี field เดียว tag `0x0B`, 1 byte, offset `+0x14`; ตรง `PF_SERIALIZER_FIELDS.tsv` W/R ทั้งสองแถว.
- ผลตอบ objective: action ยืนยัน/Survey **ส่ง request**; body ที่พินได้ไม่มี island id, scene id, actor id หรือ text id — มีเพียง byte ค่า `5`. ยังห้ามตั้งชื่อ byte นี้ว่า `confirm=1/5` เพราะไม่มี semantic crosswalk.

## T2 — ความสัมพันธ์กับ RE-086

- static พินได้ว่าเป็นสอง phase ใน module เดียวกัน: command `InvokeNavigationWindow` เปิด `Main_Sail_Lookout`; หลังผู้ใช้ทำ action `Survey` จึงสร้างและส่ง request.
- ยังพินไม่ได้ว่า dock trigger/event ใดเป็นผู้เรียก `InvokeNavigationWindow`, หรือมันมาจาก packet เดียวกับ trigger ใน RE-086. จุดนี้ยังเป็นเขตของ `RE-086`; ไม่ควรเติมด้วยการเดาจาก `SAILING_RESULT`/text id.
- ใบนี้ไม่พิสูจน์ server response/scene-transition callback. การเปลี่ยนฉากเป็นเขต `RE-090` ตาม nonclaim ของใบ.

## verifier / reproducibility

- `pf_bridge\staged\re087_captain_report_static.py` SHA-256 `924bf4498d550f272026d56a4bd6b88957f068fae57a5804142eed344a3810d1`.
- รันอิสระ 2 ครั้ง: `68/68 PASS`, exit `0/0`.
- recursive CFG: UI handler `241/241`, module handler `846/846`, request allocator `236/236`, serializer `35/35`; `SPAN_GAP_BYTES=0`, `DECODE_ERRORS=0` ทุกช่วง.
- input pins: image `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`; registry `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`; serializer fields `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`; validation `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`.
- integrity ก่อน/หลังตรงกัน: image, `AGENTS.md`, `CLIENT_RE_QUEUE.md`, external 30-file manifest และ gamedata 1,109-file manifest; ไม่มี source input ถูกแก้.

## nonclaims

1. ไม่อ้างว่า UI ปรากฏ/คลิกได้จริงใน client-observable layer เพราะรอบนี้ไม่เปิดเกม.
2. ไม่อ้าง semantic ของ global UI event token `0x01090DC0`, byte `5`, หรือ alternate host path เกิน control flow ที่พินได้.
3. ไม่อ้างว่า W/R serializer rows หมายถึง natural traffic สองทิศทาง; direction client→outbound พิสูจน์เฉพาะ action path นี้ และ capture validation ยังเป็นศูนย์.
4. ไม่อ้างว่า dock trigger คือ vital ใด, ไม่อ้างว่าหน้าต่างเกิดจาก event เดียวกับ RE-086 และไม่อ้าง scene-transition mechanism.
5. ไม่ join gamedata row id กับ protocol/UI จากเลขหรือข้อความคล้ายกัน และไม่อ้างว่า search ที่ไม่พบ crosswalk เท่ากับไม่มีอยู่ทั้งอิมเมจ.
6. ไม่เปิดเกม/server, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ source/queue/git.

## BUILD_IMPACT

**BUILD_IMPACT:** เส้นทาง navigation/captain-report ฝั่ง build ใช้ `NavigationEx_RequestSurveyVtial` body 1 byteค่า opaque `5` เป็น seam ของ action `Survey` ได้ และเชื่อมผลนี้เข้ากับ `RE-086`/`RE-090`; แต่ห้าม rename field เป็น `island_id`/`confirm_flag` หรือผูก scene transition จน RE-086 ปิด trigger และมีหลักฐาน response/lifecycle เพิ่ม.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-087 PASS/DONE — MAIN_SAIL_LOOKOUT SURVEY SENDS NavigationEx_RequestSurveyVtial(+0x14=5); DOCK TRIGGER REMAINS RE-086`.
