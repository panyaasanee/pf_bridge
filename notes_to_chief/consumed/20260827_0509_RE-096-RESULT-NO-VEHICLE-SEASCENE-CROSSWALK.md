[ถึง: chief / COO / สาย A · cc Panya | จาก: RE runner | 2026-08-27T05:09+07:00]

# RE-096 RESULT — DONE / BOUNDED-NEGATIVE: ไม่มี crosswalk จาก sea scene ไป `VEHICLE` row; `CVehicleVital.+0x18` ยังตั้ง semantic ไม่ได้

## คำตอบสั้น

ปิดใบตามทาง bounded negative: จากข้อมูลที่ใบระบุและ direct class-specific path ของไคลเอนต์ **ยังเลือก `VEHICLE` row ใดเป็นเรือของ `Bg1001..Bg1007` ไม่ได้** และ **ยังตั้งชื่อ qword `CVehicleVital.+0x18` ว่า vehicle catalog id / model id / actor id ไม่ได้**

เหตุผลชี้ขาดมีสองชั้นที่ไม่ควร join กัน:

1. ตาราง `VEHICLE` จริงมี 79 แถว แต่ 10 คอลัมน์มีเพียง `n_ID`, `n_PROPERTIES`, `n_SEATS`, `s_NAMEBOARD`, `n_SEAT1..n_SEAT6` — ไม่มี model/type/speed/name/scene field ตามที่ T0 คาดไว้ ข้อมูลเรือที่มี outfit/velocity/name อยู่ในตาราง **`SHIP` แยกต่างหาก** (17 แถว; ชื่อ 14 แถวอยู่ `SHIP_TEXT`).
2. `CVehicleVital` มี wire field เดียว `tag 0x32`, 8 ไบต์ ที่ object `+0x18` ทั้ง W/R แต่ handler `0x00710440` เป็น exact `mov al,1; ret 4` ไม่อ่าน field และไม่ lookup ตารางใด; capture เป็น `NOT_OBSERVED` 0 เฟรมทั้งสองทิศทาง จึงไม่มี semantic crosswalk ให้ตั้งชื่อ qword.

## T0 — ตารางที่มีจริง

- `CONSTDATA_TH__VEHICLE.tsv`: 79 แถว; schema ตามข้างต้น ไม่มีคอลัมน์ model/type/speed/scene/ship.
- `CONSTDATA_TH__SHIP.tsv`: 17 แถว; มี `n_SHIP_VELOCITY`, `s_OUTFIT`, `f_SHIP_ROTATE_SPEED`.
- `TEXTDATA_TH__SHIP_TEXT.tsv`: มีชื่อเรือ 14 แถว เช่น `Civilian Barge`, `Bermuda Ship`, `Main Warship`, `Armed Brig Barge`.
- `SCENE_NAME` rows 17–23 คือ `Bg1001..Bg1007`, `n_SCENE_TYPE=4`, แต่ไม่มี field ที่อ้าง `VEHICLE` หรือ `SHIP`.
- id ที่บังเอิญซ้ำกันระหว่างตาราง `VEHICLE` และ `SHIP` คือ `[11, 12, 101, 102, 103]` — **ไม่ใช้เป็น crosswalk** เพราะไม่มี field เชื่อมจริงตามกฎใบ.

ดังนั้นคำตอบ T0 ไม่ใช่ “row X” แต่เป็น bounded negative ว่า schema ที่ใบชี้มาไม่มีทางกรองหา row เรือ และตารางเรือจริงก็ยังไม่มี field ผูกกลับไป scene family.

## T1 — `CVehicleVital.+0x18`

หลักฐาน direct path:

- initializer `[0x006E3440,0x006E3466)` ตั้ง qword `+0x18/+0x1C` เป็นศูนย์;
- serializer `[0x006C0180,0x006C01A3)` อ่าน/เขียน 8 ไบต์ด้วย tag `0x32` เท่านั้น;
- handler `[0x00710440,0x00710445)` SHA-pinned เป็น `B0 01 C2 04 00` (`AL=1; ret 4`) — ไม่มี read/write/lookup;
- raw anchor ของ id-global `0x010879CC` มีเพียง getter กับ registrar 2 จุด; object-vtable `0x00F40AEC` มี initializer anchor 1 จุด;
- `PF_FIELD_VALIDATION.tsv`: `CVehicleVital W/R` = `NOT_OBSERVED`, observed frames 0/0.

จุดที่ห้ามสับสน: `CGCVehicleModule` ใช้ resident **`CVehicleAttr` คนละ object**; helper `[0x006E2D40,0x006E2D5B)` สแกน qword หกช่อง `CVehicleAttr.+0x18..+0x47` ว่าว่างทั้งหมดหรือไม่เพื่อขับ state/flags. เลข offset `+0x18` ที่ตรงกันในคนละ type **ไม่ใช่ crosswalk** ไป `CVehicleVital` และไม่พิสูจน์ catalog id.

ผล T1 จึงจำกัดว่า qword เป็น wire payload 8 ไบต์ที่ semantic ยัง `UNKNOWN`; ไม่มีหลักฐานให้ตั้งชื่อเป็น vehicle row id หรือ model id.

## T2 rider — sea-scene cross-check

`SCENE_NAME` rows 17–23 มี 24 คอลัมน์และไม่มี `vehicle`/`ship` field. เส้น Columbus ที่ปิดโดย RE-095 คือ quest `3023`, script `Q_TELEPORT1`, `n_VARI_2=19` → scene 19 / `Bg1003`; แถวนี้ให้ scene id แต่ไม่ให้ `VEHICLE`/`SHIP` id. จึงไม่เกิด crosswalk เพิ่มจาก rider.

## ค้นสองที่ (บังคับ)

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ registry/serializer/validation ของ `CVehicleVital` (`serializer 0x006C0180`, handler `0x00710440`, qword tag `0x32` @`+0x18`, W/R); เจอว่า capture 0 เฟรม. **ไม่เจอ** consumer/lookup ที่ตั้ง semantic ของ qword หรือผูกมันกับ `VEHICLE`/`SHIP` row.
- **ค้น `gamedata` แล้ว:** เจอ `VEHICLE` 79 แถว, `SHIP` 17 แถว, `SHIP_TEXT` 14 ชื่อ, `SCENE_NAME` rows 17–23 และ quest 3023 → scene 19. **ไม่เจอ** field crosswalk จาก sea scene ไป `VEHICLE`/`SHIP` row หรือจาก qword ไป catalog row.

## BUILD_IMPACT

สาย A/เซิร์ฟเวอร์ยังไม่ควรเลือก vehicle/ship row เอง. สิ่งที่ build ได้จากใบนี้คือ guard เชิงโครงสร้าง: scene 19/`Bg1003` ไม่เท่ากับ vehicle id, `VEHICLE` ไม่เท่ากับ `SHIP`, และ `CVehicleVital.+0x18` ต้องคงชื่อ `UNKNOWN_QWORD` จนกว่าจะมี capture จริงหรือ client code path ที่เชื่อม `SCENE_TYPE=4` ไป catalog lookup ด้วย field จริง.

## Verifier / integrity

- `pf_bridge\staged\re096_vehicle_seascene_crosswalk_static.py` SHA256 `aaf39eb1273a25ccc597b23dfffbea818a16a15b1bcfccde519f60b4a11f9037`
- รันสองรอบ: `SUMMARY guards=40 failed=0`, exit 0 ทั้งคู่
- `GameClient.local.bin` ก่อน/หลัง: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- external pins: registry `27daac0c...cfb4d`, fields `99282bdf...c123`, validation `080a5f32...41c3`
- gamedata pins: `VEHICLE d8adc2ae...be50`, `SHIP 4823b0e0...1ad3`, `SHIP_TEXT 3ce8d25c...9551`, `SCENE_NAME e38114a8...d60b`, `QUEST cc992728...27bd`
- span pins: initializer `d2f53a6e...4414`, serializer `c0910c6e...3bce`, handler `f4c6d7ae...2863`, attr scan `b6d9f688...7e2f`

## Nonclaims

- ไม่อ้างว่า sea scene ไม่มี ship/vehicle crosswalk ที่อื่นทั้งเกม; ผลลบจำกัดที่ตารางที่เกี่ยวข้อง + direct `CVehicleVital` class path ที่วัดครบ
- ไม่อ้างว่า `SHIP` row ใดเป็นเรือของผู้เล่น และไม่ join จาก id ที่บังเอิญซ้ำ
- ไม่อ้างทิศทางจริงของ `CVehicleVital`; ตาราง W/R ไม่พิสูจน์ client send/receive และ capture ยัง 0
- ไม่อ้างว่า `CVehicleAttr` หก qword มี semantic อะไร หรือเป็นค่าเดียวกับ `CVehicleVital.+0x18`
- ไม่ใช้ linear disassembler เป็นหลักฐานผลลบ; ข้อสรุปพึ่ง exact spans, vtable/type anchors, schema และ SHA-pinned verifier
