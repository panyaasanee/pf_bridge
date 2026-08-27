[ถึง: Panya · chief cloud · COO · สาย A (WORLD) | จาก: RE runner LOCAL · 2026-08-27T09:18+07:00]

# RE-100 RESULT — DONE/BOUNDED-NEGATIVE · ไม่พบ branch พิเศษของ 99/101 ใน native scene path · `CActorTask_ActorMove` รับหนึ่งจุดต่อ task

- ใบ: `RE-100 SETNUMBER-99-101-SENTINEL-AND-ACTORMOVE-MULTIPOINT-001`
- หมวด: `STATIC-ON-BRIDGE` ล้วน · ไม่เปิดเกม/เซิร์ฟเวอร์ · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB
- image: `GameClient\GameClient.local.bin`, ImageBase `0x00400000`, size `14,759,424`, sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- verifier: `pf_bridge\staged\re100_setnumber_actormove_static.py`, sha256 `3d6c6096b7a499c8bd7b1bb66eed22fe9408e336458a28cf4117cf346aee7187` · `45/45 PASS` สองรอบหลังแก้ไฟล์ครั้งสุดท้าย

## คำตอบสั้น

1. **T1 — BOUNDED NEGATIVE:** ใน recursive CFG ของ definition finder/loader, placement reader, generic template dispatch และ scene consumer ที่ผูกกันจริง ไม่พบ `cmp/test/sub` เทียบค่า `99`, `101` หรือค่าขอบรอบนั้นเพื่อแยก `99`/`101+` ออกจากเลขอื่น. Loader อ่าน payload `u32@+1` เข้า definition object `+0x30`; scene consumer resolve definition ด้วย **ชื่อ set** แล้วโหลด `+0x30` ส่งต่อเข้า generic dispatch โดยไม่มี branch sentinel ในเส้นทางที่ครอบคลุม.
2. **T2 — ตอบชัดว่า one point:** `CActorTask_ActorMove` เป็น object ขนาด `0x58`; destination เดียวอยู่ `task+0x40/+0x44/+0x48`. `+0x4C` เป็น scalar แยก และ `+0x50..+0x55` เป็น byte flags. updater อ่าน XYZ ชุดเดียวและใช้ `+0x4C` แยก จึงไม่มี array/count หรือพื้นที่ vec3 ชุดถัดไปใน task นี้.
3. **T3 — BOUNDED NEGATIVE:** native `.npc` path อ่าน extra triples เป็น vector จริง แต่ recursive CFG ของ extra-triple codec/placement reader/scene loader/scene consumer ไม่มี direct edge ไป `CActorTask_ActorMove`. caller ที่พิสูจน์แล้วคือ `CNetActor` network-target consumer: target ใหม่ที่ `actor+0x100..+0x108` สร้าง ActorMove หนึ่งจุดใหม่. ในขอบเขตนี้ไม่พบ client auto-patrol ที่กิน extra-triple list; ถ้าจะให้ actor เดินหลายจุดต้องให้ฝั่ง server/ผู้ควบคุมส่ง target ทีละจุด.

คำว่า BOUNDED สำคัญ: นี่ไม่ใช่คำกล่าวว่า `99/101+` ไม่มีความหมายทั่วทั้ง image หรือ extra triples ไม่มี consumer ใดเลย; คือไม่พบ special branch/ActorMove link ใน native paths ที่ระบุและถอดด้วย recursive CFG ครบเท่านั้น.

## ค้นสองที่ก่อนถอด (บังคับ)

- **ค้นใน `pf_bridge\external\` แล้ว: ไม่เจอ** `CActorTask_ActorMove`, `ActorMove`, VA `0x00472A20/0x004799C0/0x00479C00`, `Mob_Set`, sentinel หรือ native `.npc` loader ในตารางส่งมอบ; เจอเพียงคำอธิบายโครง `.npc` ใน `00_SEARCH_HERE_FIRST.md` ซึ่งไม่ตอบ consumer/branch.
- **ค้น gamedata แล้ว: เจอ** `pf_decode_lua_npc.py`, `PF_GAMEDATA_SCENE_INDEX.tsv`, raw/derived `bg0001` exact-EOF layout และ 11 placements ที่มี extra triples; **ไม่เจอ** Lua/table crosswalk ของ `Mob_Set` หรือ `ActorMove` (`Mob_Set/MOBSET/ActorMove/CActorTask` = 0 ไฟล์ใน `gamedata/lua` + `gamedata/tables`). จึง verify raw/TSV แล้วตาม native loader แทนการเขียน parser ซ้ำ.

## T0 — image และ raw control

- image SHA/size/base ตรงกับ `RE-083` ทุกค่า.
- `bg0001.npc` SHA `026bbe32ca2b69853b1433d585de7e80bb67e7f713e086b9347fd10ad1dc2070`, version 2, definition 113, placement-count offset `0x11C8`; raw definition payload มีค่า `99` และ `101..113` จริง จึงเป็น positive control ว่าค่าที่ถามผ่าน loader เดียวกัน.
- derived `bg0001.placements.tsv` SHA `2e5b4115169160d609289d0e638e953d7da16a0000e267c12c118c7c1a4cfc5f`: extra triples มี 11 placements ตรง index `43,128,129,130,131,133,134,135,136,137,138`; เป็น `Mob_Set_44` 4 จุดและ `Mob_Set_102` 7 จุด.

## T1 — set number ไม่มี sentinel branch ในเส้นทางที่ครอบคลุม

สายข้อมูล native ที่ยืนยันจาก image:

1. definition loader `0x00439E90` อ่าน record เป็น helper sequence `u8/u32/u8/u8/u32/u32/u8` ที่ `0x0043A007/14/21/2E/3B/48/55`; `lea [definition+0x30]` ที่ `0x0043A00C` คือช่อง `u32@+1` ของ payload.
2. scene consumer resolve definition ด้วยชื่อ set ผ่าน `0x0043AC9D -> 0x00438790`, โหลด `[definition+0x30]` ที่ `0x0043ACAA`, แล้วส่งค่าต่อเข้า generic dispatch `0x0043ACBC -> 0x0043A6F0`.
3. recursive CFG สี่ spanที่ครอบสายนี้ถอดครบ (มีเพียง compiler alignment NOP สองก้อนที่ pin bytes แล้ว) และไม่มี comparison immediate ช่วง `98..102`; จึงไม่มีหลักฐานว่า 99 หรือ 101+ ถูกแยกด้วยเงื่อนไขพิเศษในสายนี้.

ผลนี้ไม่ตั้งชื่อ semantics ให้ `u32@+1`: เรียกตามโครงว่า definition value เท่านั้น. การที่ค่าตรงกับเลข suffix ของ `Mob_Set_NN` ไม่ใช่ crosswalk ไป `MOBS.n_ID`.

## T2 — ActorMove มีหนึ่ง destination ต่อ task

- constructor `0x00472A20` ถูก caller ทั้งเจ็ด branch จัดสรรด้วย size `0x58` ก่อนเรียก.
- `0x00472A7E/89/94` เขียน destination vec3 ที่ `+0x40/+0x44/+0x48`.
- `0x00472A9F` เขียน scalar ที่ `+0x4C`; `0x00472AA7..B3` และ `0x00472AE1` เขียน flags ที่ `+0x50..+0x55`.
- recursive CFG ของ ctor/update/step อ่าน/เขียน `task-this` สูงสุดเพียง `+0x55`; ไม่มี pointer pair, count หรือ tail ตั้งแต่ `+0x58`.
- updater `0x004799C0` อ่าน XYZ ที่ `0x00479A56/6F/83`; จากนั้นอ่าน scalar `+0x4C` ที่ `0x00479ADF` แยกต่างหาก.

ดังนั้น `+0x4C` ไม่ใช่ X ของ waypoint ถัดไป และ struct ไม่มีพื้นที่ครบสาม floatสำหรับจุดที่สอง.

## T3 — extra triples ถูกอ่าน แต่ไม่ต่อเข้า ActorMove ใน scene path

- placement reader `0x00439780` ส่ง subobject pointer `placement+0x50` เข้า codec `0x00439450` ที่ `0x00439A0F`.
- codec อ่าน `u16 count` แล้ววนอ่าน `f32 x/y/z` สามครั้งต่อ record (`0x00439592/BC/C8/D4`) เก็บใน vector ของ subobject. ดังนั้น extra triples เป็น list ในข้อมูลจริง ไม่ใช่ decoder artifact.
- แต่ CFG ของ `extra_triple_codec`, `placement_reader`, `definition_loader`, `template_dispatch`, `scene_consumer` ไม่มี call ไป ctor `0x00472A20`.
- เส้นที่พิสูจน์แล้วว่าสร้าง task ซ้ำคือ `CNetActor 0x00459160`: target network/mirror ที่ `actor+0x100` แล้ว call ctor ที่ `0x00459707` หรือ `0x004597D1`. นี่รองรับการส่งจุดใหม่ทีละจุด ไม่ใช่คิวที่ task ถือเอง.

**BUILD_IMPACT:** สาย build ห้ามส่ง extra-triple list ครั้งเดียวแล้วหวังให้ `CActorTask_ActorMove` เดินเอง. ถ้าจะทำ patrol/route ให้เก็บ queue และ advance จุดฝั่ง server/logic owner แล้วส่ง MovementAttr target ใหม่ทีละจุด; เลข set `99/101+` ห้ามใช้เป็น special class จากหลักฐานใบนี้.

`BUILD_IMPACT_NONE: 0/1`

## Action taken ต่อ `PANYA-CHASE 0915`

`Action taken: RE runner ยืนยันว่า RE-100 ไม่ครอบ 0310 §① / 0500 §③ เรื่อง placement index → MOBS.n_ID, QUEST→scene roster, SCENE_AREA/MARKER transform หรือ Hields/Sase/Columbus identity. ใบนี้ครอบเฉพาะ 99/101+ native handling และ ActorMove multi-point เท่านั้น; ห้ามใช้ผล RE-100 ปิดงาน identity crosswalk ของสาย A. งาน roster/fit transform ที่ Panya สั่งใน 0500/0915 ยังเป็นงานคนละชั้นและยังต้องส่งผลแยก.`

## Span manifest

```text
DEFINITION_FINDER     [0x00438790,0x0043880E) sha 7445aa1a...40963e  insns 54  gap 0
EXTRA_TRIPLE_CODEC    [0x00439450,0x004395F7) sha eeabd01e...9308cf  insns 146 gap 0
PLACEMENT_READER      [0x00439780,0x00439A35) sha 5ff3c49e...6705f2  insns 237 gap 0
DEFINITION_LOADER     [0x00439E90,0x0043A106) sha 39ddc523...fc776e  insns 192 gap 3 (0x43A08D `8d4900`, alignment NOP)
TEMPLATE_DISPATCH     [0x0043A6F0,0x0043A9C3) sha 28ebd3e0...a266758 insns 198 gap 0
SCENE_CONSUMER        [0x0043A9D0,0x0043AD54) sha 36dd3c9c...e9248f  insns 249 gap 7 (0x43ABF9 `8da42400000000`, alignment NOP)
CNETACTOR_CONSUMER    [0x00459160,0x004598A5) sha 40f88d22...b066674 insns 512 gap 0
ACTORMOVE_CTOR        [0x00472A20,0x00472AFB) sha bc47cd00...da88f15 insns 61  gap 0
ACTORMOVE_BEGIN       [0x004799C0,0x00479BF5) sha f69683fa...e7bbe87 insns 179 gap 0
ACTORMOVE_STEP        [0x00479C00,0x00479DCE) sha d7e51031...010912  insns 160 gap 0
```

## Nonclaims บังคับ

1. ไม่อ้างว่า 99/101+ ไม่มีความหมายทั่วทั้ง image; ผลลบจำกัดเฉพาะ CFG ที่ระบุ.
2. ไม่อ้างว่า extra triples คือ patrol route หรือไม่มี consumer อื่น; พิสูจน์เพียงว่าถูกอ่านเป็น list แต่ไม่ต่อเข้า ActorMove ใน scene path ที่ครอบคลุม.
3. ไม่อ้างว่า caller ทั้งหมดทั่ว image เป็น direct call เท่านั้น; ข้อสรุป one-point ยืนบน layout/consumer ของ task เอง ส่วน auto-patrol เป็น bounded negative ของ native scene path.
4. ไม่ join set suffix/template value กับ `MOBS.n_ID` เพราะเลขตรงกัน และไม่ตัดสิน Columbus index 0/1, Hields หรือ Sase.
5. ไม่ใช้ linear disassembler เป็นหลักฐานหลักของผลลบ: verdict มาจาก recursive CFG 10 spans + exact bytes/SHA; direct-call census ใช้เป็น supporting inventory เท่านั้น.
6. ไม่แก้ `CLIENT_RE_QUEUE.md`, `GAME_TEST_QUEUE.md`, `CHIEF_CONTINUATION.md`, source, external, gamedata หรือ canonical DB.

## Integrity / reproducibility

- external tree 30 files manifest `9525161de1f79fe1c4d73f98c39a7e854c946bd0c30c0686d23f2a9854baa837`
- gamedata tree 1,109 files manifest `ae16237dbce6c031894e83b4fb0bc0151cdf1f32e52e5d677499eb5ba25ac54d`
- parser `pf_decode_lua_npc.py` `6ab38fd52079bf31fc0c355b49063043d55a2a14a60bb33d5fe3cacb2fcccf9e`; scene index `c4016cf685671d4c7bbb1909bb300146afd802dd6b53f2d5e7b928249f26652d`
- rules/queue/new orders ก่อนส่ง: AGENTS `a31ddea8...6ad3a`; queue `82e74161...91cc9`; NEW_ORDERS `f7dae505...001c9`
- อ่านจดหมายใหม่ `PANYA-CHASE 0915` ก่อนส่งและแยก scope ให้แล้ว; ไม่เปิดใบเพิ่มเอง.

## สรุปส่ง chief

`RE-100 DONE/BOUNDED-NEGATIVE — T1 no 99/101 special branch in covered native path; T2 ActorMove one vec3 per 0x58-byte task; T3 extra list parsed but no scene-loader→ActorMove edge, so server/owner must sequence points. RE-100 does not close the separate 0310/0500 identity-crosswalk work.`
