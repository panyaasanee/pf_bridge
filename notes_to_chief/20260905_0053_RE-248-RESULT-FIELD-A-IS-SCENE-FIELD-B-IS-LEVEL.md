[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: chief, COO | จาก: RE runner local · 2026-09-05T00:53+07:00]

# RE-248 RESULT — PASS/DONE: FIELD_A (`+0x20`) = scene id; FIELD_B (`+0x22`) = character level

## คำตอบสั้น

- `u16 tag 0x12` ตัวแรก / order 17 / `CreateActorDataEx+0x20` = **scene id** (`scene_id`) และหน้าเลือกตัวละครอ่านตัวนี้ไป lookup `SCENE_NAME_TIP.n_ID` แล้วพิมพ์ `s_SCENE_NAME` ลง `LABEL_SCENE`.
- `u16 tag 0x12` ตัวที่สอง / order 18 / `CreateActorDataEx+0x22` = **character level** (`character_level`) และหน้าเดียวกันอ่านตัวนี้ไปตั้ง `NUMLABEL_CHARLV`; ไม่ใช่ scene id.
- ดังนั้นผู้บริโภคแก้ค่าคงตัวได้เป็น **`SCENE_FIELD = FIELD_A`**. ใบนี้เป็นหลักฐานชั้น IMAGE เท่านั้น; `GT-245` ยังเป็นผู้พิสูจน์ client-observable แยกชั้น.

## Ticket START / input pins

- START `2026-09-05T00:32:34.048+07:00`; ticket block ล่าสุดจากหัว `RE-248` ถึง EOF = 6,241 UTF-8 bytes, SHA-256 `5f08ee45b547d472b3c7d99cabe61e052ec4142f27afd35a463d9b93cad373d1`.
- image `GameClient.local.bin` SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `PF_SERIALIZER_FIELDS.tsv` SHA-256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`; `PF_PROTOCOL_REGISTRY.tsv` SHA-256 `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`.
- Codex mirror authority SHA-256 `4faae5f0dc3bc86b4e71ef5069dda43c3ea86cec2ea3fa3c156307f22fd24fbf`; README SHA-256 `41745046be3137d4f0c1e0712af1c30d5a102e1ee812acd7896aa94631857970`; `PF_MONSTER_COLOR_GATE.tsv` SHA-256 `8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcEDC1D9F207720BCBAA0`.

## ค้นก่อนถอด

### `pf_bridge/external/`

ค้นหนึ่งรอบทั่ว 2,683 ไฟล์ / 930,201,065 bytes (inventory fingerprint `d31c5470a76d60b7f0b39e53d9242ce0b0f92076ff646e9e26dee5b3ba2bee3c`) ด้วย `SelectActorVital`, `CreateActorVital`, `0x5DFF60`, `+0x20`, `+0x22`:

- เจอ registry และ serializer rows ตามใบ: SelectActorVital W order 17 = `+0x20`, order 18 = `+0x22`; CreateActorVital W order 10/11 เป็นสองช่องเดียวกัน. Codec `[0x005DFF60,0x005E01C6)` SHA-256 `de9de2a04f4ac3ec8e6c07550336eea2be18954143c5c0de1823a4a2171e3f8a`.
- เจอ Codex row ว่า record คือ `CreateActorDataEx`, constructor ตั้งทั้ง `+0x20/+0x22 = 1`, และ record นี้แยกจาก RuntimeRes actor-entry. ตาม `nonclaim` ตารางเดิมไม่บอกความหมายของสองช่องและห้ามเหมา field semantic ข้ามคลาส จึงใช้เพียงเป็น structural pin ไม่ใช้เป็นคำตอบ.
- เจอ capture CreateActorVital ที่ค่าทั้งสองเท่ากันตามจดหมาย LANE-DB; ตัวอย่างนี้ไม่ crosswalk ความหมายและไม่ได้ใช้ตัดสิน.

### `pf_bridge/gamedata/`

ค้นหนึ่งรอบทั่ว 1,109 ไฟล์ / 15,319,585 bytes (inventory fingerprint `b8d2410fc1817bb2505d18d4208c1e76f3313b502b27ab3f01ec02d5fbdf5674`):

- เจอ `tables/TEXTDATA_TH__SCENE_NAME_TIP.tsv` (`n_ID`, `s_SCENE_NAME`, `s_GM_SCENE_NAME`) SHA-256 `f9076cfc3c14433b376811437d68375d5dd1ce1ef2c7a50dbc1d4e4d241bfa3a` และ `tables/CONSTDATA_TH__SCENE_NAME.tsv` SHA-256 `e38114a802576266ce37b2abcf8ebce3f105d7d5abaf4bc5ca066e7848c5d60b`.
- ไม่พบ message/field crosswalk สำหรับ SelectActorVital/CreateActorVital ใน gamedata; ขอบเขตผลลบคือชื่อ message/codec/offset/scene-id terms ใน 1,109 ไฟล์ ไม่ใช่คำกล่าวว่าไม่มี scene data.

## Static IMAGE trace ที่ปิด crosswalk

1. **wire fields:** codec W ที่ `0x005DFFCB..0x005DFFE9` ส่ง `self+0x20` ก่อน แล้ว `self+0x22`, ทั้งคู่ tag `0x12`, width 2. Read branch เติมสองช่องเดียวกันที่ `0x005E00C0..0x005E00DC`.
2. **SelectActorVital -> exact object:** handler `0x005EFC9C..0x005EFCB1` ส่ง container `outer+0x18` เข้า `0x005DDD00`. ฟังก์ชัน `[0x005DDD00,0x005DDE0E)` เดิน container แล้ว insert คู่ key / pointer `[node+0x10]` ลง map ที่ singleton `0x004011A0` `+0x180`. นี่คือ pointer `CreateActorDataEx` ที่ codec สร้าง ไม่ใช่การจับคู่เพราะเลข id เท่ากัน.
3. **same map -> named event:** screen builder `0x004C0830` เรียก singleton เดียวกัน (`0x004C08DE`). ที่ `0x004C1D84..0x004C1F30` มันเดิน map `singleton+0x180`, เอา value pointer `[node+0x10]`, ใส่ payload ของ event ชื่อ UTF-16 **`Actor_Info`**, แล้ว dispatch ไป UI.
4. **typed receiver:** `0x00510EF0..0x00510F42` รับ `Actor_Info`, เอา payload ที่ event `+0x48`, ทำ runtime type check (`0x005DEC10` -> cast helper `0x0088F2B0`), แล้วส่ง pointerเดิมเข้า binder `0x005105C0`.
5. **FIELD_B name:** binder อ่าน `word [payload+0x22]` ที่ **`0x00510732`** แล้วตั้ง widget ที่ `this+0x1C`; resolver `0x00510420..0x00510510` ผูกช่องนี้กับชื่อ UTF-16 **`NUMLABEL_CHARLV`**. จึงเป็น character level.
6. **FIELD_A name + scene print:** binder อ่าน `word [payload+0x20]` ที่ **`0x005107E2`**, ใช้เป็น row key ของ table UTF-16 **`SCENE_NAME`**, field UTF-16 **`s_SCENE_NAME`**, แล้วส่งผลให้ widget `this+0x20`; resolver ผูกช่องนี้กับ **`LABEL_SCENE`**. จึงเป็น scene id ที่หน้าเลือกตัวใช้พิมพ์ชื่อฉาก.

Pinned proof slices:

- handler edge `[0x005EFC9C,0x005EFCB1)` SHA `66d2069f06f586e4c82da4f4a66bc889afcc2d4f0e22a8825d7b096f62776483`
- container-to-map `[0x005DDD00,0x005DDE0E)` SHA `c1ef50dca2ccd298096bc5555038a2c1f54e7e42982123c89d5ec9d8ba9a6b99`
- same-singleton call `[0x004C08DE,0x004C08E7)` SHA `752d65c8cd0fa43b885e0bb0feafb73398acd51b4ad1b4c08060b8359f708011`
- map-to-Actor_Info `[0x004C1D84,0x004C1F30)` SHA `fee94e7d9410fc0ee025b5a68c531e60c2f824aeddb6c1f4aa1792e5e79cf3d8`
- Actor_Info typed receiver `[0x00510EF0,0x00510F42)` SHA `4f3d6d723cd86c396439206e636ecf5234fc6769ec1dde37c7ccd5f45a5c8616`
- named widget resolver `[0x00510420,0x00510510)` SHA `e479b4df864eebf88b618fa574215f0b4aec6817c085b6fbdd55b12f43092cfc`
- UI binder `[0x005105C0,0x00510869)` SHA `c29d7f98c8b3a3a86588a5ddb9eb5791a246300433881b286d35a426d22861f3`

## Nonclaims

1. ไม่อ้างว่าค่าฉาก/เลเวลที่ server ควรส่งคือเลขใด; พิสูจน์เฉพาะความหมายและ consumer ของสองช่อง.
2. ไม่ใช้ค่า `1/1` ใน capture หรือ default constructor เป็น semantic evidence.
3. ไม่อ้างว่า IMAGE trace คือ client-observable; การเห็นข้อความจริงเป็นหน้าที่ `GT-245`.
4. ไม่เหมา `+0x20/+0x22` ไปยัง record class อื่น และไม่อ้างว่า Codex table เดิมตอบ semantic นี้.
5. ชื่อ symbol ต้นฉบับถูก strip; `scene_id` / `character_level` เป็นชื่อ normalized จาก named DATA/UI bindings ข้างต้น ไม่ใช่ source-level debug symbol.

## BUILD_IMPACT

`BUILD_IMPACT: LANE-DB may change only SCENE_FIELD from None to FIELD_A (+0x20); no serializer/layout/reorder/backfill/runtime change is justified by this result.`

ไม่มีการเปิดเกม/เซิร์ฟเวอร์, ไม่แตะ canonical DB/LOCK_GAME, และไม่แก้ client/server/source/queue/external/gamedata/git.
