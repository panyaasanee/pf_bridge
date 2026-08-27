[ถึง: chief cloud · LANE-A/LANE-B · COO | จาก: RE runner local · 2026-08-28T05:16:11.800+07:00]

# RE-116 RESULT — CNetNPC spawn heading มาจาก MovementAttr; ยังไม่พบ crosswalk จาก `.npc`/MARKER

## สถานะ

**DONE / PASS (static-only)** — ปิด T0–T4 ครบตามใบ `NPC-SPAWN-HEADING-SOURCE-001` โดยไม่เปิดเกม/เซิร์ฟเวอร์และไม่แตะ canonical DB

- ticket START: `2026-08-28T05:10:11.835+07:00`
- client SHA-256: `GameClient.local.bin = 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- verifier: `staged/re116_npc_spawn_heading_static.py` SHA-256 `26160fce67b2a4c5927bf492ef38d92c3831afa45ecbfdb82bb78f88cf84be0d`
- marker probe: `staged/re116_marker_probe.py` SHA-256 `0403f8df34b4da4fe209064d6c9c83ae187d8ac7bcec8c59cb482ff5cc57ae52`
- verifier ผ่านอิสระ 2 รอบ: `RESULT=PASS`, `checks=83 failed=0 pinned_spans=6` ทั้งสองรอบ

## T0 — input/control และ mandatory searches

ค้น `pf_bridge/external/` แล้วทั้งชุด: 30 files, 29,900,221 bytes, deterministic manifest SHA-256 `cd91774757396c8e216d41dc3b13015d1013a4297e293630790e9b633392f483`

- พบ `MovementAttr` เพียง class เดียวใน `PF_PROTOCOL_REGISTRY.tsv`: vtable `0x00F0D0F8`, ช่องที่ตารางเรียก `serializer_va=0x0043BB80`
- `PF_SERIALIZER_FIELDS.tsv` มี W/R สองแถวเป็น `EMPTY` ที่ `0x0043BB80`; `PF_FIELD_VALIDATION.tsv` ระบุ 0 frames / `NOT_OBSERVED`
- พบรายงานเดิม `PF_MOVE_PROJECT001_REMOTE_MOVEMENT_PROJECTION_STATIC_20260818.md` ซึ่งชี้ full serializer ที่ `0x004671C0`; รอบนี้ตรวจกับไบนารีซ้ำเอง

ค้น `pf_bridge/gamedata/` แล้วทั้งชุด: 1,109 files, 15,319,585 bytes, deterministic manifest SHA-256 `81c087df74dea1171cb55de5644195d10ffeee43355b98b660fb1744c689c54a`

- พบ `MARKER` 390 rows / 6 columns: `n_ID,n_SCENE,n_X,n_Y,n_Z,n_DIRTECTION`; scene 2 มี 18 rows
- พบ `Bg0002.npc` raw SHA-256 `a649f4afab701df3698b9ffebbb83b77863531a9113c40b6f12f056b7f030b16`, 11,652 bytes, version 2, 46 definitions, 106 placements
- derived `Bg0002.placements.tsv` SHA-256 `e57841a7018b46ff50d31972e5ba0846612548288446fe8514d819a99be92f8f` เก็บ raw float ทั้งหกค่า แต่ schema ไม่มีคอลัมน์ชื่อ heading/direction/rotation/facing/yaw
- พบ marker `n_ID=2` ที่พิกัดเดียวกับจุดเข้า scene ตามบริบทเดิม แต่ไม่มี crosswalk field ไป NPC placement จึงไม่จับคู่ด้วยเลข/พิกัดอย่างเดียว

SHA ควบคุมสำคัญเพิ่มเติม:

- `CLIENT_RE_QUEUE.md = 753a80cce7f596b4413e779ce8621aed657eb2eb8b4b00a5c4d08cd031d176f0`
- `AGENTS.md = 8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3`
- `NEW_ORDERS.txt = 9f0039f691ffa13a80448d31629ff8f29b1f824c5b155393712000056449c3b6`
- `PF_PROTOCOL_REGISTRY.tsv = 27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv = 99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_FIELD_VALIDATION.tsv = 080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- `CONSTDATA_TH__MARKER.tsv = 723c713aeb604b9b594777517d69f333bbe1509d4931b40294fa720163bd67dc`

## T1 — แหล่ง heading ที่ CNetNPC ใช้ตอน initial apply

vtable `CNetNPC` ที่ `0x00F0DF58` มี slot `+0x10 -> 0x0045D200` และตรวจ recursive CFG เต็มช่วง `[0x0045D200,0x0045D485)` ได้ 183 instructions / 645 bytes / gap 0 / error 0; span SHA-256 `f3859d6de337bf53fbcdd31e0d0620dbecf573c89941eafc6072134e37eeddd5`

dataflow ที่ปักหมุด:

1. `0x0045D34F` โหลด actor field `[esi+0x244]` ซึ่งเป็น `MovementAttr`
2. `0x0045D355` อ่าน `MovementAttr+0x34`
3. ค่านี้ถูกเขียนไป model `+0x30` แล้วเรียก normalizer `0x00484450`
4. จากนั้นเขียนค่าเดียวกันไป model `+0x2C` แล้วเรียก normalizerเดิมอีกครั้ง

ดังนั้น consumer ตอนสร้าง/initial-apply ของ CNetNPC ใช้ heading จาก `MovementAttr+0x34` โดยตรง ไม่ได้อ่านค่าจากตาราง NPC ในฟังก์ชันนี้

## T2 — raw `.npc` bytes นอก XYZ

ตรวจ native loader chain แบบ recursive CFG:

- placement reader `[0x00439780,0x00439A35)`: 237 instructions, gap/error 0, span SHA-256 `5ff3c49eb37252c69e5899245ce82cd004f36a15854f2701c690940df56705f2`
- template dispatch `[0x0043A6F0,0x0043A9C3)`: 198 instructions, gap/error 0, span SHA-256 `28ebd3e05d5c05f956dbb7919a882b4c6654bf821637d653d9f32d1c0a266758`
- scene consumer `[0x0043A9D0,0x0043AD54)`: 249 instructions, error 0, มี alignment gap ที่คาดหมายเพียง `0x0043ABF9: 8da42400000000`, span SHA-256 `36dd3c9ce064ad07924b1efc977e807f821a96fab3c3d042890103a784e9248f`

reader เก็บ raw float หกตัวต่อเนื่องที่ placement object `+0x2C..+0x40`; scene consumer ส่ง pointer `placement+0x2C` เข้า dispatcher แต่ dispatcher อ่านเฉพาะ pointer `+0` และ `+4` ก่อน overwrite register นั้น ไม่มี read ที่ `+8/+0x0C/+0x10/+0x14` ใน dataflow นี้ และ complete covered path ไม่มี direct edge ไป CNetNPC initial apply, `MovementAttr` apply/Serial หรือ heading normalizer

**bounded negative:** ใน native loader/consumer path ที่ครอบคลุมข้างต้น ไม่พบหลักฐานว่า raw `f32_3/f32_4/f32_5` หรือ byte อื่นใน placement record feed ค่า network spawn heading; แหล่งตรงที่ CNetNPC ใช้ยังเป็น `MovementAttr+0x34`

## T3 — `MARKER.n_DIRTECTION`

ไบนารีมี UTF-16 literal `n_DIRTECTION` ที่ `0x00F15F90` และ `MARKER` ที่ `0x00F15FAC` การสแกน raw pointer occurrence ใน `.text` ให้ผล:

- pointer ไป `n_DIRTECTION`: 1 จุดเท่านั้น ที่ immediate operand `0x004B4D0A` ของคำสั่ง `push` ที่ `0x004B4D09`
- pointer ไป `MARKER`: 2 จุด ที่ `0x004B4CEB` และ `0x005F227A`

เส้นทาง named access แรกเปิดตาราง MARKER ที่ `0x004B4CEA`, ขอ field `n_DIRTECTION` ที่ `0x004B4D09`, lookup ผ่าน `0x00892480`, เก็บผล AL ลง object `+0x10`, แปลง/scale แล้วใช้กับ orientation ของ player/model ที่มีอยู่ในเส้นทาง teleport/scene-entry; จุด MARKER อีกแห่งที่ `0x005F2279` ขอ field ชื่ออื่น ไม่ใช่ `n_DIRTECTION`

**bounded negative:** ภายในพื้นผิว named-field access ที่ exhaustive ตาม literal/pointer นี้ ไม่พบ consumer ของ `n_DIRTECTION` นอก teleport/player scene-entry และไม่พบ crosswalk field ไป NPC placement

## T4 — reconcile `0x0043BB80` กับ `0x004671C0`

ไม่ใช่ class-name collision: มี `MovementAttr` เพียง class เดียวและ vtable เดียว `0x00F0D0F8`

- vtable `+0x18 -> 0x0043BB80`; bytes `8b4424048b54240889411889511cc20800` เป็น common argument copier: เอาสอง argument เขียน `this+0x18` และ `this+0x1C`, แล้ว `ret 8`; ไม่มี stream primitive
- vtable `+0x34 -> 0x004671C0`; นี่คือ full `MovementAttr::Serial`
- recursive CFG apply `[0x00467130,0x004671BC)`: 53 instructions / gap 0 / span SHA-256 `97dd85ca3425b380316a047878f41b8bfd5497d9d400b51204dbdef2dc9b3b88`
- recursive CFG Serial `[0x004671C0,0x00467326)`: 142 instructions / gap 0 / span SHA-256 `b4642a28e80a890d8c4a1717490c543d1590adc5ebdce982d84f2a8579cb1633`
- ทั้ง write/read branches ใช้ mask bit `0x02` กับ tag `0x2A` ที่ object `+0x34`

สรุปคือ external row เก็บ bytes/identity ถูก แต่ label `serializer_va` ชี้ slot `+0x18` ที่เป็น copier จึงเป็น **slot-semantic mismatch ใน external registry**; serializer จริงอยู่ vtable `+0x34 = 0x004671C0`

## Nonclaims / ขอบเขตที่ผลนี้ไม่พิสูจน์

- static client พิสูจน์ว่า client consume heading ที่มากับ `MovementAttr`; ไม่พิสูจน์ว่า original server เลือกค่าต้นทางอย่างไร
- ไม่กล่าวว่า raw `f32_3/f32_4/f32_5` ไร้ความหมายทั่วทั้งโปรแกรม; ผลลบจำกัดอยู่ที่ loader/CNetNPC spawn path ที่ครอบคลุม
- named-literal xref ไม่ตัด generic/index-based table access ที่ไม่อ้าง literal `n_DIRTECTION`
- ไม่มี client-observable evidence และไม่ใช้ static แทนหลักฐาน attended test
- ค่า four-way headings ปัจจุบันยังเป็น synthetic policy ไม่ใช่ authentic recovered per-placement data

## BUILD_IMPACT

`BUILD_IMPACT: hard guard / no direct patch requested` — wire contract ปัจจุบันรองรับ per-NPC heading อยู่แล้วผ่าน `MovementAttr mask 0x02`, field `+0x34`, tag `0x2A`; แต่ยังไม่มี static source/crosswalk จาก `.npc` หรือ MARKER ที่ให้อ้างเป็น authentic per-placement heading ได้ ดังนั้น LANE-A/LANE-B ต้องไม่เปลี่ยนชื่อหรืออธิบาย round-robin four-way ปัจจุบันว่าเป็นข้อมูลที่ recover จาก client/gamedata หากจะคงไว้ให้ระบุชัดว่าเป็น synthetic cosmetic policy จนกว่าจะมี authored source หรือหลักฐาน crosswalk ใหม่

ไม่มีการแก้ `GameClient/`, server, `external/`, `gamedata/`, queue หรือไฟล์ source ใด ๆ
