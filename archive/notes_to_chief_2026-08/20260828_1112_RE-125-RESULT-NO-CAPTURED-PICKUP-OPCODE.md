[ถึง: chief cloud (cc), LANE-B, COO และ Panya · จาก: RE runner LOCAL]

# RE-125 RESULT — DONE/BOUNDED-NEGATIVE · ยังไม่มี opcode ของ pickup ที่ยืนยันจาก capture

- เวลา: `2026-08-28T11:12:57.224+07:00`
- ใบ: `RE-125 PICKUP-REQUEST-VITAL-ID-001`
- ticket START: `2026-08-28T11:06:23.997+07:00`
- หมวด: `STATIC-ON-BRIDGE` ล้วน · ไม่เปิดเกม/เซิร์ฟเวอร์ · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB
- image: `GameClient\GameClient.local.bin`, size `14,759,424`, sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

## คำตอบ objective

**ยังยืนยัน vital id/opcode จริงไม่ได้จากหลักฐาน static ที่มีอยู่.** ค่า `0x4543` เป็นเพียงค่า **DERIVED จากชื่อคลาส** `PickupTerrainThing` ด้วยฟังก์ชัน `sum((index+1)*ord(character)) & 0xffff`; ไม่พบมันบนสายทั้งใน corpus แช่แข็งและ capture ที่เพิ่มภายหลังทั้งหมด. ห้ามต่อ production call site ใน `runtime.py` ด้วย `0x4543` จนกว่าจะมี capture จากการคลิกวัตถุของตกพื้นที่วาดและคลิกได้จริง.

สิ่งที่ปิดได้เชิง conditional-static คือ **ถ้า** capture ในอนาคต crosswalk opcode จริงกลับมาที่คลาส `PickupTerrainThing` ตัวนี้: class body มีเพียง `object_ref_u32` แล้ว `opaque_u8`; ไม่มี claimant identity หรือ XYZ ใน serializer body. ฝั่งเซิร์ฟเวอร์จึงต้องอ่านตัวตนและตำแหน่งปัจจุบันจาก authenticated connection/session state เอง ไม่ใช่ปั้นว่ามาจาก request body.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ**
  - `PF_PROTOCOL_REGISTRY.tsv:52`: `PickupTerrainThing`, id-global VA `0x0108202C`, vtable `0x00F3005C`, serializer `0x005E5E30`, handler `0x005EF640`.
  - `PF_SERIALIZER_FIELDS.tsv:859-862`: ทั้ง W/R มีสองฟิลด์ — tag `0x14`, object `+0x14`, len 4; ตามด้วย tag `0x08`, object `+0x18`, len 1; span `[0x005E5E30,0x005E5E83)` sha256 `8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066`.
  - `PF_FIELD_VALIDATION.tsv:102-103`: W/R = `0 frames / 0 instances / 0 files`, `NOT_OBSERVED`.
  - ผู้สมัครสำรอง `FightingDropModule_Client` / `FightingDropNotify` (`PF_PROTOCOL_REGISTRY.tsv:454-455`) ยังไม่มี serializer/getter/vtable crosswalk และ `PF_FIELD_VALIDATION.tsv:906-909` เป็น `NOT_OBSERVED` ทั้ง W/R.
  - external tree: 30 files / 29,900,221 bytes / manifest sha256 `3b742370873829347ec7827e610c96e8091b0400fde70ceae9965c6f3664e811`.
- **ค้น gamedata แล้ว: เจอเฉพาะข้อมูลโดเมน ไม่เจอ protocol crosswalk**
  - `CONSTDATA_TH__VARIABLE_FLOATING.tsv:52` = `PET_PICKUP 0.5`; `:96` = `RANGE_PICKUP 600.0` (sha256 `cd73c93f7aaf1487a29aadd758888a9f1857efe5f1407adca2b4204bb99ac809`).
  - มีตาราง `DROPS_*`/item ตามดัชนี แต่ไม่พบ `PickupTerrainThing`, `FightingDrop*`, opcode, serializer หรือ named field ที่ผูกตารางกับ request wire.
  - hit ตัวเลข `4543` ใน quest/ตาราง/float/ไบต์ placement ไม่ใช่ crosswalk และไม่ถูกนำมา join เพราะเลขเท่ากัน.
  - gamedata tree: 1,109 files / 15,319,585 bytes / manifest sha256 `e8e44669b2e7b7b06a8722be9c622ee988ab5c169a4b170ad8956751d9428e5b`.

## T0 — input gate / SHA PASS

manifest เริ่มงานอยู่ที่ `staged/re125_input_manifest_20260828_1106.txt`. พินหลัก: queue `649323bf...e0af4`, AGENTS `8b7fab9e...6ed6e3`, orders `0e107cd3...29c315`, registry `27daac0c...6cfb4d`, serializer fields `99282bdf...b5c123`, validation `080a5f32...e0941c3`, capture inventory `729b5e73...0259d1`, server `mob_pickup.py` `e4c9f1b1...e7fed`, `runtime.py` `9ea21621...febac`.

## T1 — capture census ปัจจุบัน: bounded negative

รัน `staged/re125_capture_census.py` แบบอ่านอย่างเดียว โดย reuse framing/schema parser จาก `external/pf_validate_capture_fields.py` และไม่ publish ทับ external:

- frozen inventory: 1,772 files / 595,134,426 bytes / manifest `ec7540dc32aab362487bc890a8ce8f9ced57ffd4c404ca673cc5716a7c5bb7e5`; SHA ตรง 1,772/1,772, missing 0, mismatch 0.
- capture ที่อยู่นอก inventory เดิม: 334 files / 65,064,695 bytes / manifest `6ac497b0163beb6eb57dfb3204c7c5eef166978bfbb37051e28cc2788b54655f`.
- corpus ปัจจุบันรวม: 2,106 files / 660,199,121 bytes / manifest `164c36db978155fdce1622fd64a76e79ab26064256b562d397bfe459dde0b12c`.
- parse scope ปัจจุบัน: 1,223 text files, 75,208 PC/decompressed blocks, nested declared 24,387, nested reached 23,782, unknown message ids 0, block errors 0.
- ผลเป้าหมายทั้ง corpus ปัจจุบัน: `PickupTerrainThing` W=0/R=0; `FightingDropModule_Client` W=0/R=0; `FightingDropNotify` W=0/R=0 — ทุกตัว 0 frame / 0 instance / 0 file.
- ไม่มี directory ชื่อ GT-060/pickup และไม่มีข้อความ `PickupTerrainThing`, `pickup_listener`, `0x4543` ใน capture text; ข้อนี้เป็นเพียง corroboration. หลักฐานผลลบหลักคือตัว parse 75,208 blocks ข้างบน ไม่ใช่ชื่อไฟล์.

ดังนั้น corpus ที่มีอยู่ไม่มีการคลิก pickup จริงซึ่งให้ crosswalk event→opcode ได้. การไม่มี unknown id ช่วยตัดกรณี "มี id แปลกที่ parser ไม่รู้จัก" ใน blocks ที่ parse ได้ แต่ยังไม่ทำให้ message ชื่ออื่นกลายเป็น pickup โดยไม่มี event crosswalk.

## T2 — `0x4543` เป็น candidate เท่านั้น

- `external/pf_validate_capture_fields.py` (sha256 `0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8`) คำนวณ `protocol_id("PickupTerrainThing") = 0x4543` จากชื่อ.
- id-global VA `0x0108202C` อยู่ virtual-zero tail ของ section `.data`: delta `0x6802C` แต่ section raw size `0x11E00`; จึงไม่มี raw on-disk id bytes ให้พิน ค่าเริ่มต้นใน image เป็นศูนย์ก่อน runtime registration.
- เพราะ capture count ของ candidate นี้เป็นศูนย์ `0x4543` จึงยังเป็น `DERIVED/NOT_OBSERVED`, ไม่ใช่ vital id จริงที่ยืนยันแล้ว.

## T3 — payload shape ที่ปิดได้แบบ conditional-static

re-run verifier เดิม `staged/re082_static_verify.py` (sha256 `b72e39aa29906f23bcd33a02298ef0e9a67730a4a33a3c27399b3756ca6d70ab`) ผ่าน image/span pins และ recursive CFG เต็มอีกครั้ง:

1. left-click producer สร้าง request ที่ `0x006B0639`.
2. `0x006B0642 -> 0x006B0645 -> 0x006B0649` ก๊อป `runtime+0x7C -> element+0x10` ไป `PickupTerrainThing+0x14` โดยไม่มี transform; RE-082 ปิดแล้วว่าเป็น live element key / `drop_key` u32.
3. factory กำหนด `+0x18=0`; click path overwrite เฉพาะ `+0x14`.
4. serializer spanส่งเพียง `u32 +0x14` แล้ว `u8 +0x18`. ไม่มี claimant identity, X, Y หรือ Z ใน class body นี้.

ผลต่อ `mob_pickup.PickupClaim`: `object_ref_u32` และ `opaque_u8` สอดคล้องกับ conditional class shape; ส่วน `claimant_identity/x/y/z` เป็น server/session inputs สำหรับ ownership/range validation ไม่ใช่ฟิลด์ที่พิสูจน์ว่ามากับ request. ข้อนี้ **ยังไม่อนุญาต production wiring** เพราะ opcode จริงและ event crosswalk ยังไม่ปิด.

## T4 — เกณฑ์จบ / method ceiling

`DONE/BOUNDED-NEGATIVE`: static corpus ปัจจุบันไปต่อถึง actual opcode ไม่ได้. ทางต่อที่เปลี่ยนเพดานหลักฐานคือ attended capture ใหม่ซึ่งมีวัตถุของตกพื้น **วาดจริงและคลิกได้จริง**, จดเวลาคลิก และเก็บ outbound frame ก่อน/หลังคลิกเพื่อ crosswalk id+payload. นั่นเป็นใบ attended แยกต่างหาก; RE runner รอบนี้ไม่เปิดเกมและไม่หยิบ GT-060/GT-124.

**ห้ามรัน RE-125 ซ้ำ** จนกว่าจะมี capture ดังกล่าวเพิ่มหรือ chief แก้ objective/jobs อย่างมีสาระ. การสแกน corpus เดิมซ้ำจะได้เพดานวิธีเดิม.

## Nonclaims

1. ไม่อ้างว่า `0x4543` คือ opcode จริงของ original client/server wire; มันเป็น name-derived candidate เท่านั้น.
2. ไม่อ้างว่า `FightingDrop*` คือหรือไม่ใช่ request จริง; เส้นนั้นยัง unresolved และ unobserved.
3. ผลลบจำกัดที่ capture tree ปัจจุบัน 2,106 ไฟล์ / 75,208 blocks ที่ parser อ่านได้; ไม่อ้างถึง packet ที่ไม่เคยถูก capture.
4. static producer/serializer พิสูจน์ shape ของคลาสใน image แต่ไม่พิสูจน์ว่าคลาสนั้นขึ้นสายด้วย id ใด.
5. ไม่อ้างว่า claimant identity/XYZ ไม่เคยอยู่ใน outer transport/envelope ทุกชนิด; claim แคบคือไม่มีใน `PickupTerrainThing` class body สองฟิลด์ที่พินแล้ว.
6. ไม่แตะ `runtime.py`, `mob_pickup.py`, source/server/client/external/gamedata/queue, canonical DB หรือ git.

`BUILD_IMPACT: ไม่มี production patch ที่ปลอดภัยจากผลนี้ — คง runtime call site unwired และห้าม promote 0x4543. เมื่อ attended capture ยืนยัน opcode→PickupTerrainThing แล้ว chief จึงต่อ decoder สองฟิลด์ object_ref_u32/opaque_u8 เข้ากับ dispatch_pickup_request โดยอ่าน claimant identity และ XYZ จาก authenticated session state.`

`BUILD_IMPACT_NONE: 1/1`

## สรุปส่ง chief

`RE-125 DONE/BOUNDED-NEGATIVE · T0-T4 ปิด · actual pickup opcode ยัง unobserved · current corpus 2,106 files / 75,208 blocks มี target 0 frames · ต้องใช้ attended click capture ใหม่ก่อน production wiring.`
