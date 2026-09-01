ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย — ผล RE-194 (ผู้บริโภค LANE-DB; static bridge)

# RE-194 RESULT — DONE / PASS: fresh player BasicAttr+0x54 is 400.0f; NPC 150.0 is a later wire value

- Ticket START: `2026-09-02T04:54:47+07:00`
- Result time: `2026-09-02T05:01+07:00`
- Queue SHA-256 at start: `cb3088d9b016ac4edb73eba8fd38f1820e6638bc74587a5302fb6a996fcea694`
- Static/read-only only: no game/server boot, no `LOCK_GAME`, no canonical DB, no source/queue/external/gamedata edit.

## Verdict

คำตอบคือข้อ 1: local player object (`CMyActor`) ที่สร้างใหม่มี `BasicAttr+0x54 = 400.0f` หลัง constructor chain จบและก่อน wire ใดทับ. จุด `0x00464AF2` ไม่ใช่ player-only writer และไม่มี branch/parameter เลือก 400/150; มันเป็น unconditional store ใน shared `BasicAttr` constructor. ทั้ง player `ActorAttr` และ `NPCAttr` เรียก constructor นี้ จึงเริ่มที่ 400.0 เหมือนกัน. ค่า 150.0 ใน `test_npc_gait_wire.py` เป็นค่าที่ server-side test เลือก pack ลง tag `0x2A` แล้ว client รับมาทับภายหลัง ไม่ใช่ client construction default.

## Mandatory searches

- ค้นใน `pf_bridge\external\` แล้ว: scope = 2,683 files / 930,201,065 bytes; terms `0x00464AF2`, `BasicAttr+0x54`, `movement_speed`, `walk_speed`, `PLAYER_LOGIN_MOVEMENT_SPEED`, `PROVEN_WALK_SPEED`, `400.0`, `150.0`, `CMyActor`, `ActorAttr`. พบคำตอบเดิมบางส่วนใน `PF_ATTR_FIELD_SEMANTICS.tsv`, `PF_A2_ATTR_FIELD_DELTA.tsv`, `PF_ATTR_INHERITANCE.tsv` และตัว rederive; corpus เดิมปัก default 400.0 แต่ scope ของ semantic consumer ยังเน้น CNetNPC/unknown จึง re-derive player constructor chain จาก IMAGE โดยตรงตาม objective.
- ค้นใน `pf_bridge\gamedata\` แล้ว: scope = 1,109 files / 15,319,585 bytes. พบ schema crosswalk `PF_GAMEDATA_COLUMNS.tsv` row `CONSTDATA_TH / MOBS / n_SPEED_WALK` และคอลัมน์ `n_SPEED_WALK` ใน `tables/CONSTDATA_TH__MOBS.tsv`; ไม่พบ `0x00464AF2`, `BasicAttr`, หรือ player constructor default. ค่าใน MOBS เป็น DATA ต่อแถวและไม่ใช่หลักฐานค่า fresh player. ผลลบจำกัดเฉพาะ extracted gamedata tree.

## Exact player constructor chain — CLOSED

1. **Player type, not NPC:** the local-player class is `CMyActor` (`.?AVCMyActor@@`, type descriptor `0x0101ABB8`, vtable `0x00F0D7A8`). Its constructor prefix `[0x0044C990,0x0044C9CB)` has SHA-256 `69afa58dc52ede1bd1d1dda927e293469bbb5ebbd5fdbdb0fda85208c4dd52a4`; at `0x0044C9BB` it calls base constructor `0x00457340`. Tight call span `[0x0044C9B5,0x0044C9C5)` SHA `50db4a1714038b431235eca7291f246a91365dd1e18734258dd56e9d641156ea`.
2. **CNetActor creates the player's ActorAttr:** the base constructor sets the `CNetActor` vtable `0x00F0DD08`, calls ActorAttr pool/factory `0x00456D20` at `0x004573BC`, and stores the returned pointer at object `+0x348` at `0x004573CA`. Exact chain span `[0x00457366,0x004573D0)` SHA `7b598efa035d23261ec8d5a5ce3f6a85b7a22beb8f0b89dadc169174ee4b6b9d`.
3. **Both pool branches construct ActorAttr:** helper `[0x00456D20,0x00456E32)` SHA `0ed913a67bfb654c11000ff1fec5903fdd9a0bc6430429b8ac9a90ca7e617469` allocates/reuses a 0x1C0-byte object; the fresh branch calls `ActorAttr::ctor` at `0x00456D87`, while the reuse/placement branch calls the same ctor at `0x00456E0B`. There is no return path from this helper that supplies a non-null player attr without that ctor call.
4. **ActorAttr unconditionally base-calls BasicAttr:** `ActorAttr::ctor` is `[0x00464BE0,0x00464E39)`, SHA `e83ae4a601a4ec700326598d6329e4b34cd2f4cf78dcf17d639d8df8e1f1096a`; at `0x00464C0B` it directly calls `0x00464A80`. Tight base-call span `[0x00464C05,0x00464C12)` SHA `1694acf967a68e84d6929403f9e2d0f190edff2b423931ce88e7a17a974a4a90`.
5. **BasicAttr writes 400.0 with no branch:** `BasicAttr::ctor` is `[0x00464A80,0x00464B34)`, 180 bytes, SHA `aefa3a436f15deb03fe6390bf3f7d05c67e420cfb22a58c254e8f0eea5e58dd6`. At `0x00464AE3` it loads f32 from VA `0x00F0DD9C`, then at `0x00464AF2` executes `movss [esi+0x54], xmm0`. Exact load/store span `[0x00464AE3,0x00464AF7)`, file `[0x00063EE3,0x00063EF7)`, SHA `7145efc52121cb4f85a2c197c85faf52d7166ff1d6e413743b8c92843d374e92`. Literal `[0x00F0DD9C,0x00F0DDA0)` maps to file `[0x00B0C19C,0x00B0C1A0)`, bytes `00 00 C8 43` = IEEE-754 f32 `400.0`, SHA `ac8fb139930df65fdb788559d7299840c359549afc851b82ba08d1485e67f3b7`.

The independent typed getter path agrees that the local CMyActor's vslot `+0x74` returns an attr object accepted by the `ActorAttr` type-node check before the code reads `ActorAttr+0x98`: span `[0x00443F8C,0x00443FCF)`, SHA `95c04a60398d10b1624988a69d46b9021d69f27f403293e0d54d436d1fcd7805`. This guards against treating an unrelated same-offset object as the player's attr.

## Why NPC 150.0 does not conflict

`NPCAttr` is a separate child of `BasicAttr`, but its constructor `[0x00465210,0x004652AC)` SHA `7e67a01a0ef0554281c016e2a2c047c04b46d9c083ab9fd656834e9fc9dad38f` also directly calls the same `BasicAttr::ctor` at `0x00465239`. Thus a fresh NPCAttr also begins with 400.0; there is no NPC-constructor literal 150 branch to choose instead.

The 150.0 in `tests/test_npc_gait_wire.py` is explicit server-side payload construction: `PROVEN_WALK_SPEED = 150.0`, mask widened by `0x0040`, followed by `bytes([0x2A]) + struct.pack("<f", PROVEN_WALK_SPEED)`. Client receive code tests mask `0x40`, points at resident `+0x54`, supplies tag `0x2A` and len 4, then calls the read helper at `0x004658E3`; exact gate/read span `[0x004658C0,0x004658E8)`, SHA `7fbd0df161c0e2d6ba6c56bde70a4afd5b69817c9bb83086473878f2e83a2175`. That packet can legitimately overwrite the construction default after creation.

Therefore the apparent 400-vs-150 conflict is a lifecycle-layer mix-up:

`construction (player ActorAttr or NPCAttr) = 400.0` → `optional later wire tag 0x2A may replace it (150.0 in the cited NPC scenario)`.

## Input/output integrity

- `GameClient.local.bin`: 14,759,424 bytes; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `PF_ATTR_INHERITANCE.tsv`: SHA-256 `e2ede4e2af6b86b47bc557e2036c4fde8ecefaf6853da85f88b0f66702ce2544`.
- `PF_ATTR_FIELD_SEMANTICS.tsv`: SHA-256 `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f`.
- `PF_A2_ATTR_FIELD_DELTA.tsv`: SHA-256 `44f80d6aa975dfe030a0e537d5166aaa9e051c4d55f693d7e724fa2b17b19c1f`.
- `PF_GAMEDATA_COLUMNS.tsv`: SHA-256 `6f1a00dc9660038f651007397244c575b321beaf756675fd0e437c3131294d89`.
- `CONSTDATA_TH__MOBS.tsv`: SHA-256 `3c0d33d68f832eefda56c845495008338dcef56f4277584b9ca479b7e1b3916b`.
- `player_wire.py`: SHA-256 `c2080983d192051bf3f3ddc3df754e768e6eac4c25e8f147cd247be37fb21d75`.
- `persistence_attr_compose.py`: SHA-256 `d8fb2a5332f8ad6775cc924d91fdd980d1cfd8f7824194c7a93039fd7bd14441`.
- `tests/test_npc_gait_wire.py`: SHA-256 `34a313f422300d80cc579d77811978ff939a84cc1ed4d7bcc9ea052b8b74bf68`.
- `mob_death.py`: SHA-256 `c9ac8f2aa8fe7d7e5b0ea2aa870de051bc52fb73abfa22ef709dc7fa40272337`.
- All named source inputs and the queue are to be rehashed at closeout; only this result letter and runner bookkeeping are written.

## Nonclaims

- ไม่อ้างว่า player ยังคงเป็น 400.0 หลัง login snapshot/update/resend; ใบนี้ปิดเฉพาะหลัง construction และก่อน wire ตาม objective.
- ไม่อ้างว่า NPC 150.0 ผิดหรือใช้ได้กับทุก template; มันเป็นค่าที่พิสูจน์แยกใน cited attended/runtime scenario และถูกส่งผ่าน wire.
- ไม่ใช้เลข offset ที่ตรงกันเป็น crosswalk เอง: player path ถูกผูกด้วย `CMyActor -> CNetActor -> ActorAttr -> BasicAttr` constructor calls และ typed ActorAttr check; NPC pathถูกผูกด้วย `NPCAttr -> BasicAttr` และ exact codec gate.
- ไม่อ้าง client-observable movement, rendered speed หรือ gameplay sufficiency จาก static IMAGE/source evidence.
- ไม่ได้พิสูจน์ว่าการ resend กลางเกมปลอดภัย; constructor default กับ midgame update semantics เป็นคนละคำถาม.

## BUILD_IMPACT

`BUILD_IMPACT: LANE-DB may treat 400.0f as the exact fresh-player construction value for BasicAttr+0x54 and may use it for construction-default seeding. Do not infer that 400.0 is safe to resend midgame: tag 0x2A/bit 0x0040 is a real overwrite path, and the cited NPC scenario deliberately replaces the shared 400.0 default with 150.0. Keep any /speed or midgame-send gate under its separate owner/COO decision. No DB/persistence/attr-wire/source patch was made by the RE runner.`
