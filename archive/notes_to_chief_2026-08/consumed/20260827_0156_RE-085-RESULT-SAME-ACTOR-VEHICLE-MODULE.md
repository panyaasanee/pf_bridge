[ถึง: chief / COO / สาย A · cc Panya | จาก: RE runner | 2026-08-27T01:56+07:00]

# RE-085 RESULT — PASS (bounded static): vehicle state is actor-local, not a scene-only ship fixture

## คำตอบสั้น

ในสามกลไกของใบนี้ หลักฐาน static ชี้ไปทาง **(ก) ตัว actor เดิมถือ vehicle state ของตัวเอง** — แต่ให้เรียกให้แม่นว่า `CGCVehicleModule` ผูก actor ตัวเดิมเข้ากับ resident `CVehicleAttr`; ยังไม่ควรยกระดับเป็น “เปลี่ยน model id โดยตรง” จนกว่าจะ trace renderer/model slot เพิ่ม

`CGCVehicleModule` ไม่สร้าง actor เรืออีกตัวใน bounded binder/handler ที่ปิดครบ และไม่ใช่กลไก scene fixture ล้วน:

- binder `[0x006E16C0,0x006E174C)` รับ actor, type-check แล้วเก็บ pointer ไว้ที่ module `+0x18`;
- จาก **actor ตัวเดียวกัน** `+0x130` มัน lookup class id จาก global `0x010879BC` (`CVehicleAttr`), type-check แล้วเก็บ attr ที่ module `+0x1C`;
- handler `[0x006E1750,0x006E18BC)` ใช้ pointer สองตัวนี้เพื่อเปลี่ยน state/flags บน actor และ nested actor state ไม่ได้ dispatch ไป actor เรือคนละตัว;
- `CVehicleVital` เป็น qword เดียวที่ `+0x18` (tag `0x32`) ทั้ง W/R; ความหมายของ qword ยังไม่พอให้ตั้งชื่อว่า vehicle id/actor id;
- `TargetPosVital` ยังเป็น message เคลื่อนที่ 7 field ต่อทิศทาง และฝั่ง W มี capture validation 912 frames; bounded vehicle spans ไม่มี position serializer แยกมาแทนมัน

ดังนั้น server/build ควรรักษา identity ของ player actor แล้ว provision vehicle state ให้ actor นั้น ไม่ควรสร้างเรือเป็น decorative scene fixture หรือสมมติ actor เรือแยกโดยไม่มี wire evidence

## T0 — sea-scene flags

`SCENE_NAME` rows `17..23` (`Bg1001..Bg1007`, กลุ่ม Ship in the Sea) มี `n_SCENE_TYPE=4` เหมือนกันและ `n_CANRIDE=0`. นี่บอกว่าเป็น special scene family และปิด ride ปกติ แต่ **ตาราง scene อย่างเดียวไม่ใช่หลักฐานว่าเรือเป็น fixture**. ตาราง `VEHICLE` มี 79 rows แยกต่างหาก

## T1/T3 — registry / actor binding

| class | serializer / binder | handler | id global |
|---|---:|---:|---:|
| `CGCVehicleModule` | `0x006E16C0` | `0x006E1750` | `0x010879A8` |
| `CVehicleAttr` | `0x00515EC0` (empty) | `0x00463710` | `0x010879BC` |
| `CVehicleVital` | `0x006C0180` | `0x00710440` | `0x010879CC` |
| `TargetPosVital` | `0x005E50E0` | `0x00710440` | `0x01081FE0` |

จุด crosswalk ที่ตัดสินไม่ใช่เลข id ที่บังเอิญเท่ากัน แต่เป็น code path จริง: `0x006E16FD` อ่าน class id `CVehicleAttr` → `0x006E170B` lookup จาก actor `+0x130` → `0x006E1736` เก็บผลที่ module `+0x1C`

## T2 — movement

ปิดได้เพียงระดับนี้: module vehicle ผูกกับ actor ที่มีอยู่และไม่ได้เพิ่ม position codec ใน span ของมัน; `TargetPosVital` ปกติยังอยู่ครบและมี capture-positive evidence. **ไม่ได้อ้าง** ว่าเส้นทางทะเลใช้ packet cadence/ความเร็วเดียวกับการเดิน หรือว่า qword ของ `CVehicleVital` คือ actor identity

## ค้นสองที่ (บังคับ)

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ registry/serializer/validation ของ `CGCVehicleModule`, `CVehicleAttr`, `CVehicleVital`, `TargetPosVital`; vehicle สาม class เป็น `NOT_OBSERVED`, ส่วน `TargetPosVital W` เป็น `VALIDATED`. ไม่เจอ capture ที่ตั้งความหมาย qword ของ `CVehicleVital`
- **ค้น `gamedata` แล้ว:** เจอ `SCENE_NAME` rows 17–23 เป็น type 4 / canride 0, ตาราง `VEHICLE` 79 rows, `MOBS.n_VEHICLE`, buff/Lua vehicle hooks. ไม่เจอ crosswalk ที่ผูก sea scene 17–23 ไป vehicle row/model ใดแบบเจาะจง

## Verifier / integrity

- `pf_bridge\staged\re085_sea_ship_transform_static.py` SHA256 `268317259b2125992f06e363c3be8378ebbbcc4e87cf8ade726b03bbd6c540eb`
- รันสองรอบ: `SUMMARY guards=27 failed=0`, exit `0` ทั้งสองรอบ
- `GameClient.local.bin` ก่อน/หลัง: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- external pins ก่อน/หลัง: registry `27daac0c...cfb4d`, fields `99282bdf...c123`, validation `080a5f32...41c3`
- gamedata pins ก่อน/หลัง: `SCENE_NAME e38114a8...d60b`, `VEHICLE d8adc2ae...be50`
- recursive CFG ของ binder: 58 instructions / 140 decoded bytes / gap 0 / errors 0; handler: 125 instructions / 364 decoded bytes / gap 0 / errors 0

## BUILD_IMPACT

ใช้ actor identity เดิมเป็นเจ้าของ vehicle module/attr. ถ้าจะ build sea transform ต่อ ต้องหา crosswalk จริงจาก sea-scene/quest response ไป vehicle row และความหมาย `CVehicleVital.+0x18`; ห้ามเลือก vehicle id จากเลขใกล้กันหรือจากชื่อ model เดา ๆ

## Nonclaims

- ไม่ได้พิสูจน์ ship model/vehicle row ที่ใช้จริง, animation หรือ renderer slot
- ไม่ได้พิสูจน์ trigger ตอนออกท่า, sailing speed/route, dock trigger หรือ wire scene id
- ไม่ได้พิสูจน์แบบ image-wide ว่าไม่มี code path อื่นสร้าง actor แยก; คำตัดสิน “same actor” จำกัดอยู่ที่ vehicle binder/handler ที่เป็นกลไกหลักที่พบ
- ไม่ได้ใช้ linear disassembler เป็นหลักฐานผลลบ

