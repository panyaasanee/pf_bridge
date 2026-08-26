[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-083 RESULT — PASS/DONE · actor เดิมใช้เป้าหมายแยก + `CActorTask_ActorMove`

- เวลา: `2026-08-26T11:23:45+07:00`
- ใบ: `RE-083 PROJECTED-ACTOR-WALKS-OR-JUMPS-001`
- หมวด: `STATIC-ON-BRIDGE` ล้วน · ไม่เปิดเกม/เซิร์ฟเวอร์ · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB
- image: `GameClient\GameClient.local.bin`, ImageBase `0x00400000`, size `14,759,424`, sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- verifier ใหม่: `pf_bridge\staged\re083_projected_actor_walk_static.py`, sha256 `43c9c19b69c169229d1dd4c7ec6f7979f6467f811077d4c462d9649f32169e97` · exit 0 สองรอบ · 9 recursive-CFG spans, gap 0 / decode errors 0 ทุก span
- verifier เดิมของ MovementAttr: `tools\pf_remote_movement_projection_static.py` exit 0 และ `tests\test_remote_movement_projection_static.py` = `12 passed`

## คำตอบ objective ประโยคเดียว

**คำตอบคือ (ข) สำหรับ actor เดิม `actor_type 2 / CNetActor`: body ใหม่คัดลอกตำแหน่งไปที่ mirror `actor+0x100..+0x108`, แล้วเส้น existing-actor สร้าง `CActorTask_ActorMove` ซึ่งมี destination vec3 แยกที่ `task+0x40..+0x48`; updater ของ task อ่าน destination นั้นและขับ movement controller — ไม่ใช่ช่อง render/current ช่องเดียว และไม่ต้องอาศัยช่อง attack/Door B.**

มีข้อจำกัดที่ต้องเขียนตรง ๆ: body แรกของ actor ที่ยังไม่ initialized มีทาง seed model position โดยตรง แต่ routine ตั้ง `actor+0x70 |= 2` ทันที; body ถัดไปของ actor ที่มีอยู่แล้ว (โจทย์ของใบนี้) ถูก branch `0x004592D7..0x004592DB -> 0x00459401` ข้ามทาง seed และไปทาง task.

## ช่องค้นบังคับก่อนถอด

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** `BasicAttr`, `ActorAttr`, `MovementAttr` ใน `PF_PROTOCOL_REGISTRY.tsv` (getter/vtable/registration VAs) และเจอ rows ใน `PF_SERIALIZER_FIELDS.tsv`; แต่ rows หลังเป็น `EMPTY` เพราะ serializer จริงอยู่ใน generic/class methods จึงไม่ตอบ render/current-vs-target semantics. ใช้เป็น index แล้ว verify image SHA ก่อนใช้หลักฐานเดิม.
- **ค้น gamedata แล้ว: เจอ** `CONSTDATA_TH__MOBS.tsv` และ `PF_GAMEDATA_COLUMNS.tsv`: `n_SPEED_WALK` column 15 / byte offset 60, `n_SPEED_RUN` column 16 / byte offset 64; เจอ `AI_WANDER.n_OFFESIVE`/`n_AGGRO`. **ไม่เจอ** code VA, actor offset, task crosswalk หรือคำตอบ walk-vs-snap. ไม่ join เพราะเลข id/offset เท่ากันเฉย ๆ.

## T0 — field ตกที่ไหนและใครอ่าน

สายข้อมูลที่พิสูจน์จาก image:

1. `MovementAttr::CopyTo 0x00465450` คัดลอก pos `+0x28/+0x2C/+0x30` เข้า actor-owned MovementAttr ที่ `actor+0x244`.
2. actor apply `0x004446F0` โหลด `[actor+0x244]` ที่ `0x0044470A`, เรียก copier **จริง** `0x00440170` ที่ `0x00444717`, ทำให้ pos กลายเป็น `actor+0x100/+0x104/+0x108` ใน mirror `actor+0xD8`, แล้วตั้ง dirty byte `actor+0x128=1` ที่ `0x00444723`.
3. vtable `+0x24` ของ `CNetActor` คือ `0x00459160`; routine นี้ gate ด้วย dirty byte ที่ `0x00459188`, อ่าน target pointer `lea edi,[actor+0x100]` ที่ `0x0045958E`, เทียบกับ model/controller position ผ่าน `0x004A1670`, แล้วประกอบ movement task.

หมายเหตุแก้ pin เก่า: call target ที่ `0x00444717` คือ `0x00440170` ไม่ใช่ `0x00444170`/`0x004444170` ตาม typo ในรายงานเก่าบางฉบับ.

## T1 — มีสองช่อง จึงเป็น (ข)

- ตอน body แรกและ `actor+0x70 bit 2` ยัง clear, `0x004592FC..0x0045932A` seed model/current position ผ่าน `0x004845A0`/`0x00484610`; แล้ว `0x004593FD` ตั้ง bit 2.
- ตอน actor เดิมรับ body ใหม่ bit 2 ติดอยู่แล้ว: `0x004592D7 test [actor+0x70],2` และ `0x004592DB jne 0x00459401` ข้าม seed ทั้งก้อน.
- เส้นถัดไปใช้ `actor+0x100` เป็น target, เปรียบระยะ แล้วเรียก constructor `0x00472A20` ที่ `0x00459707` (mode 0) หรือ `0x004597D1` (mode nonzero).
- constructor วาง destination แยกที่ `task+0x40/+0x44/+0x48` (`0x00472A7E..0x00472A94`).

ดังนั้นสำหรับ **existing actor** จุดที่ body เขียนไม่ใช่ current/render ช่องเดียว; มันไหลลง destination ของ task แยก. ข้อนี้ตอบเกณฑ์จบใบโดยตรง.

## T2 — consumer คือ `CActorTask_ActorMove`

- constructor `0x00472A20` ติด vtable `0x00F0F090`.
- vtable `+0x08 = 0x004799C0`, `+0x0C = 0x00479C00`.
- updater `0x004799C0` อ่าน `task+0x40/+0x44/+0x48` ที่ `0x00479A56/0x00479A6F/0x00479A83`, แปลง target ให้ controller แล้วเรียก movement-control routines; เส้น step `0x00479C00` เดิน controller ต่อและตัดสิน task completion.

นี่พิสูจน์ว่ามี updater/task กิน target จริง ไม่ใช่แค่ buffer ที่ไม่มี consumer. Static ไม่พิสูจน์พิกเซลหรือ pathfinding; สิ่งนั้นอยู่ใน nonclaims ด้านล่าง.

## T3 — BasicAttr gait แยก claim ตาม actor type

- wire fact พิสูจน์: `BasicAttr` mask bit `0x0040` serialize f32 `+0x54` ที่ `0x0046579A..0x004657AE`.
- claim เดิมเรื่อง walk/run พิสูจน์กับ **`CNetNPC / actor_type 4`**: initial visual path `0x0045D2EA` อ่าน NPC attr `+0x54` แล้วเรียก `0x00484580`; runtime เดิม V67/V68/V69 เทียบ V85 บอกว่าถ้าไม่ส่งซ้ำทุก movement generation ท่าเปลี่ยนจากเดินเป็นวิ่ง.
- แต่ใบนี้ระบุ **`CNetActor / actor_type 2`**. ในขอบเขต recursive CFG ของ `CActorTask_ActorMove` (`0x004799C0..0x00479BF5`, `0x00479C00..0x00479DCE`, scalar resolver `0x004768B0..0x00476DDC`) ไม่พบ memory read displacement `+0x54`; updater เรียก `0x004768B0` สร้าง controller scalar แล้วค่อยเรียก `0x00484580`.

**BOUNDED NEGATIVE:** จาก static ชุดนี้ห้ามย้ายข้อสรุป `BasicAttr 0x0040 ต้องส่งทุก generation` จาก actor_type 4 มาเป็น actor_type 2 และยังตอบ numeric default ของ actor_type 2 ไม่ได้. “ไม่พบใน task chain ที่ถอดครบ” ไม่เท่ากับ “ไม่มีทั่ว image”; ไม่ใช้ linear disassembler เป็นหลักฐานของผลลบนี้.

ถ้าสาย build เลือกส่งมอนสเตอร์เป็น `actor_type 4`, กฎเดิมยังคงเป็นส่ง `n_SPEED_WALK` ผ่าน bit `0x0040` ทุก generation. ถ้าเลือก `actor_type 2`, ต้องเปิด/วัด gait แยก; ห้ามเอาค่า MOBS=100 มา join เข้ากับ CNetActor โดยไม่มี crosswalk.

## T4 — N/A

ผลเป็น (ข), ไม่ใช่ snap-only (ก), จึง **ไม่วัดและไม่แนะนำ refresh frequency**. ไม่มีข้อความใดในผลนี้เป็นใบอนุญาตให้ลด interval; ถ้าจะเปลี่ยนความถี่ต้องผ่าน COO ตาม rider ของใบ.

## Correction ต่อคำอธิบาย mode เดิม

คำอธิบายเก่าบางจุดเขียนสั้นเกินไปว่า `mode!=0` เท่านั้นที่สร้าง ActorMove. CFG ของ `CNetActor 0x00459160` แสดง call `0x00472A20` ทั้ง branch mode 0 (`0x00459707`) และ mode nonzero (`0x004597D1`). จึงห้ามสรุปว่า MovementAttr `+0x38=1` คือ “walk mode”; runtime เดิมก็เคยได้ bad movement เมื่อบังคับค่านี้.

## Span manifest

```text
MOVEMENT_COPY_TO       [0x00465450,0x004654C0) len  112 sha afbbbd83879f29460b09590f336acf5e21758a944a9e6ba390553c282256d4a1 insns  43
MOVEMENT_MIRROR_COPY   [0x00440170,0x004401DC) len  108 sha a366b1c04290f293e190dae2961f95e7e60492ede37033345a0671a5ef7c7d7b insns  33
ACTOR_APPLY_DISPATCH   [0x004446F0,0x00444730) len   64 sha e4e5b3719b24f7ee32791e4a419ff37942031610691f25c4d943cae9f1ae4508 insns  21
CNETACTOR_CONSUMER     [0x00459160,0x004598A5) len 1861 sha 40f88d227b827e59d6b082787f71d6b26a22ac567af8ba8069625d815b066674 insns 512
ACTORMOVE_CTOR         [0x00472A20,0x00472AFB) len  219 sha bc47cd00fdb3e6c7df487cd2b2dc9ef28c1acbb8fe45fcb5e989e7da6da88f15 insns  61
ACTORMOVE_BEGIN_UPDATE [0x004799C0,0x00479BF5) len  565 sha f69683fadb760a8219683f306301ee4d0e0e3b9f3c912b00d1a572d01e7bbe87 insns 179
ACTORMOVE_STEP         [0x00479C00,0x00479DCE) len  462 sha d7e5103159325a8b382593bde72c64d6551c1100d8865aae0d94e37032010912 insns 160
ACTORMOVE_SCALAR       [0x004768B0,0x00476DDC) len 1324 sha 324e1b87af112e5b864195c582616ba9168b63e88ca42225be4103443a89ede2 insns 338
VEC3_THRESHOLD_COMPARE [0x004A1670,0x004A1720) len  176 sha cf44f0b6bed5f1009f0823580efc88f8317b3939ba888a0fa046a79ee3556ba9 insns  46
```

ทุก span ใช้ ImageBase `0x00400000`; recursive CFG coverage เต็ม span, gap 0 / decode errors 0. ผลลบ T3 จำกัดเฉพาะ task chain สาม spanที่ระบุ.

## SHA ก่อน = หลัง / reproducibility

- image `96272114...b623`; AGENTS `5ff41a9d...8519`; queue `defa753f...d90f`; NEW_ORDERS `d311e10f...73c3`
- external tree 30 files `50c7f616...538f`; gamedata tree 1109 files `9ba99235...a3ab`
- MOVE-PROJECT report `31008a6a...302`; Q2 report `e690c489...f628`; Q3 report `6ebfe098...c318`; V67–V87 gait report `aa7bfc48...1537`; handoff `0be6cd3d...2876`
- official tool `165b1902...64b1`; official test `9aadd2ea...7476`; generated `field_mob_ai_tables.py` `049a453b...63c`

ทุก input/source ข้างต้นตรงก่อน–หลัง. มีไฟล์เพิ่มเฉพาะ verifier ในเขต `staged\` และจดหมายฉบับนี้; ไม่แก้ client/external/gamedata/server source/คิว.

## Nonclaims บังคับ

1. ใบนี้ **ไม่เปิด Door B**: เดินได้ยังไม่เท่ากับตีได้; `ATTACK_INTENT_DELIVERABLE` ไม่ขยับ.
2. ใบนี้ **ไม่ยกเพดานหลักฐาน `MOB-AGGRO-001`**: `mob_aggro_and_server_ai` ยัง `not_started` จนมี attended/client-observable pass เห็นการตอบเฟรมจริง.
3. ใบนี้ **ไม่ตัดสิน pathing**: ActorMove ไปหา point ไม่พิสูจน์การหลบสิ่งกีดขวาง.
4. ใบนี้ **ไม่ตัดสินว่ามอนสเตอร์ควรเดินเมื่อไร**: นั่นเป็นหน้าที่ `mob_aggro.tick`; ใบนี้ตอบเฉพาะ carrier/consumer.
5. `field_mob_ai_tables.py` ผูก placement จริง: 10/13 ตัวใน `bg0001` ใช้ AI_WANDER row 16 ซึ่ง `n_OFFESIVE=0, n_AGGRO=0`; มีเพียง 3/13 ใช้ row 11 (`1,1200`). ต่อให้ movement carrier ใช้ได้ ภาพที่คาดตาม logic คือ **สามตัว** อาจเข้าหา ไม่ใช่ทั้งสนาม.
6. ไม่ claim ว่า actor_type 2 ใช้ gait/default เดียวกับ actor_type 4, ไม่ claim ว่าการเคลื่อนไหว smooth บนจอ, และไม่ claim ค่า cadence ใดจาก static.

`BUILD_IMPACT: ทำให้ RE-083 ส่งมอบ INTENT_FACE_AND_APPROACH และ INTENT_RETURN_TO_LEASH ของ MOB-AGGRO-001 ผ่าน MovementAttr position ไปยัง CActorTask_ActorMove ของ actor_type 2 ได้ในขั้น build ถัดไป; ผู้เล่นจะเห็นสามมอนสเตอร์ที่ aggro-enabled เดินเข้าหา/กลับ leash ได้หลังมี encoder + attended verification โดยไม่ต้องรอ Door B.`

`BUILD_IMPACT_NONE: 0/1`

## สรุปส่ง chief

`RE-083 PASS/DONE — objective=(ข) สำหรับ existing actor_type 2 · T0/T1/T2 ปิด · T3 bounded ตาม actor type · T4 N/A · static-only.`
