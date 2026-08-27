[ถึง: chief cloud · COO · LANE-B | จาก: RE runner local · 2026-08-26T22:23+07:00]

# RE-092 RESULT — PASS/DONE · REPLACE-BY-OMISSION · NETWORK-ACTOR-REGISTRY-SCOPE

ใบ: `RE-092 REMOTE-ACTOR-LIST-CONSUMER-REPLACE-OR-MERGE-001` · หมวด `STATIC-ON-BRIDGE` · ImageBase ทุก VA = `0x00400000`

คำตอบสั้น: **(ก) replace-by-omission** — ทุกครั้งที่ consumer รับ actor collection แบบ nonempty มันเพิ่ม generation, lookup/create/update และ stamp เฉพาะ identity ที่มากับรอบนั้น แล้วกวาดสมาชิกใน network-actor manager ที่ stamp ไม่ตรง generation ออกใน call เดียวกัน ยกเว้น object ที่ `IsKindOf(0x0102CB04)` (`CMyActor`/local player). ดังนั้น one-entry combat/death frame คง actor เป้าหมายกับ local player ไว้ แต่ actor อื่นที่อยู่ใน manager เดียวกันและไม่ exempt มี removal path ทำงาน; static นี้พิสูจน์ registry removal ไม่ใช่ภาพบนจอ.

## correction ด่าน T0

ข้อความ objective ของใบเรียกคอลเลกชันนี้ว่า derived-mask `0x08`; **ไม่ตรงกับ source และ image ที่พิน**:

- `make_runtime_remote_actors()` ส่ง derived bit `0x02`, object `RunTimeProtocolRes+0x1C`, codec `0x005E1C10/0x005E1AD0`; `mob_combat.bar_frames()` และ `mob_death.death_frames()` ยังเรียก `make_runtime_remote_actors([entry])` จริง.
- bit `0x08` อยู่ object `+0x20`, codec `0x005F85B0`; เป็นคอลเลกชันพี่น้องที่ RE-082 สอบกับ `PickupTerrainThing`, ไม่ใช่ consumer ของ combat/death.
- actor entry ใช้ identity tag `0x32` / qword; bit-`0x08` element ใช้ key tag `0x14` / u32. คนละ consumer และคนละ key shape จึงยืมคำตอบ RE-082 มาแทนไม่ได้.

## ช่องค้นบังคับก่อนถอด

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** `GSCN_RunTimeProtocolRes` ใน `PF_PROTOCOL_REGISTRY.tsv` (vtable `0x00F2FFC0`, serializer `0x005E3EE0`, handler `0x005E4060`) และ serializer rows ที่พิน subcodecs; validation ฝั่ง R มี 10,073 frames/134 files แต่ `PickupTerrainThing` W/R ยัง `NOT_OBSERVED`. ชุด external พินจุดเริ่มและรูป wire แต่ไม่ตอบ membership consumer จึง verify SHA แล้ว re-derive จาก image.
- **ค้น gamedata แล้ว: ไม่เจอ** `RunTimeProtocolRes`, `GSCN`, remote-actor consumer, derived mask, `PickupTerrainThing` หรือ VA ที่เกี่ยวข้องในทั้ง tree 1,109 ไฟล์. ขอบเขตนี้หมายถึงไม่พบ crosswalk ใน gamedata ที่ค้น ไม่ใช่คำอ้างว่า client ไม่มี semantics และไม่ได้ join ตารางเพราะเลข id เท่ากัน.

## T1 — replace หรือ merge

เส้นทางที่ re-derive จาก image:

1. handler `[0x005E4060,0x005E41CD)` อ่าน object `+0x1C` ที่ `0x005E4073`; ถ้ามีค่า เรียก manager accessor `0x00402A20` แล้ว actor reconcile `0x00446F30` ที่ call site `0x005E4085`.
2. reconcile `[0x00446F30,0x004470DE)` เพิ่ม `[manager+4]` generation ที่ `0x00446F37`.
3. incoming loop lookup identity (`0x00446F91 -> 0x00446170`), create เมื่อไม่พบ (`0x00446FA3 -> 0x00446990`), update ผ่าน vtable `+0x20` (`0x00446FB6/0x00446FBC`) แล้ว stamp object `+0xD0` ด้วย generation ปัจจุบัน (`0x00446FC1`).
4. registry loop เปรียบ object `+0xD0` กับ `[manager+4]` (`0x0044702F/0x00447035`). ถ้าไม่ตรงและไม่ผ่าน `IsKindOf(0x0102CB04)` (`0x00447047..0x0044704C`) จะเรียก removal `0x00441C40` ที่ `0x004470B2` แล้ว set flag `0x100000`.
5. removal `[0x00441C40,0x00441C91)` deregister จาก global manager `0x01093198 + 0x180`, clear intrusive link `+0x1C`, แล้ว cleanup.

คำตอบ T1 = **A / replace-by-omission**. Full executable rel32 census ของอิมเมจพบ direct caller ของ reconcile แห่งเดียว `0x005E4085`, caller ของ removal แห่งเดียว `0x004470B2`, และ factory insertion แห่งเดียว `0x00446AA8`; absolute dword census ของ `0x00446F30` = 0. ผลลบนี้ไม่อ้าง computed/indirect dispatch ที่ census แบบนี้มองไม่เห็น.

## T2 — scope

- accessor `0x00402A20` คืน singleton `0x0102C6C0`; ctor วาง map ที่ `+0x0C` และ registry/list ที่ `+0x24`.
- actor factory `0x00446990` รับ actor type `2..6` แล้ว insert ผ่าน `0x00446090` ที่ `0x00446AA8`.
- verifier แยก actor type จาก image ได้: 2=`CNetActor`, 3=`CMyActor`, 4=`CNetNPC`, 5=`CAvatarNPC`, 6=`Pet`; token exemption `0x0102CB04` คือ `CMyActor`/local player.

ดังนั้น scope ที่พิสูจน์ได้คือ **manager-owned network actors ที่มาจาก actor collection/factory ชุดนี้** ไม่ใช่ “ทุก object ในฉาก” แบบไร้ขอบเขต. สมาชิก non-exempt ที่ถูก omit (รวม remote actor/NPC/pet ตาม class ที่อยู่ใน registry นี้) เข้าสู่ removal path; local player exempt. Population ที่สร้างจาก scene-load หรือ subsystem อื่นและไม่อยู่ manager นี้ยังพิสูจน์ว่าได้รับผลไม่ได้.

## T3 — key tag rider

**ต่างจริง**: actor stream bit `0x02` ใช้ tag `0x32` เป็น qword identity (`0x005E2238`), ส่วน RE-082 bit `0x08` ใช้ tag `0x14` เป็น u32 element key (`0x005F875C`). เป็นคนละ collection ที่อยู่ใต้ RunTimeProtocolRes เดียวกัน.

## verifier / reproducibility

- verifier ใบนี้: `pf_bridge\staged\re092_remote_actor_collection_static.py`, SHA-256 `a6f403ec28d1f6077dd1265da14d91514f1c4700a7214c40e84fa804179676a0`; final exit 0 อิสระสองรอบ ผล `PASS_REPLACE_BY_OMISSION_NETWORK_ACTOR_SCOPE` ตรงกัน.
- recursive CFG coverage เต็มและ gap/error `0/0` สำหรับ handler, reconcile, removal, manager accessor/ctor/lookup และ bit-`0x08` codec; exact span SHA pin ใช้กับ serializer/list/actor codecs/factory. ไม่ใช้ linear disassembler เป็นหลักฐานผลลบ.
- actor-type verifier `Pirate Force ServerProject\tools\pf_actor_type_dispatch_static.py`, SHA `b58811fbf2b7ed7ea3259700910bec28f011e24be75ed97832a9f4673cc15408`, exit 0, guards 111.
- image `GameClient.local.bin` size 14,759,424 SHA `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` ก่อน=หลัง.
- source pins หลัง sync: legacy `2eb05ed2...ea4c22`, `mob_combat.py` `156cb54d...a5820`, `mob_death.py` `aa7cd015...daa65`; สอง verifier passes ใช้ pins ชุดเดียวกัน.
- aggregate ก่อน=หลัง: `external` 30 files `324f9e189a06239213d5fcd81d8fa96aa5bc616cc1018ac246bca152bd4720cc`; `gamedata` 1,109 files `3482f4fe7d6c29411f28d3983aabd1c8627ee07188d9a29209b7198c8de88b32`.
- ใช้หลักฐานที่มีอยู่แล้ว `20260821_0951_GT040-PART-B-RESULTS-from-assistant.md` SHA `4c83939e...e0525` และ `20260823_0203_GT042-REDERIVE-PASS-WITH-HANDLER-SPAN-ERRATUM.md` SHA `74eede40...df2` หลัง verify SHA แล้ว re-derive ปฏิปักษ์กับ image ปัจจุบัน.

ระหว่างรอบ sync อิสระเปลี่ยน queue `46977ed6...0a37e -> 3b7762d8...43800`, `NEW_ORDERS 52173d6a...587a8 -> f9691985...0b2a5` และ `mob_death.py 7f824f64...5020c -> aa7cd015...daa65`. อ่าน R180/R181, queue และ diff ใหม่ครบ: RE-092 ยัง OPEN และ body ไม่เปลี่ยน; RE-093/094 เป็นใบใหม่; source diff ล่าสุดเป็น docstring-only และ one-entry call ที่ `death_frames()` ยังเดิม. Runner ไม่ได้แก้ไฟล์เหล่านี้.

## nonclaims

1. ผล static พิสูจน์ registry removal path ไม่ใช่ pixels/visibility; client-observable ต้องวัดใน attended `GT-084` rider.
2. ไม่อ้างพฤติกรรมของ original server และไม่ตัดสินว่า server ควรแก้ composer, roster หรือ dispatch อย่างไร.
3. ไม่อ้างว่า scene-load population ทุกชุดอยู่ใน manager นี้ และไม่เหมารวมผลของ bit `0x02` ไปยัง RE-082 bit `0x08`.
4. ไม่อ้างว่าไม่มี computed/indirect caller ทั่วอิมเมจ; census ที่รายงานครอบคลุม direct rel32 และ absolute dword ตามที่ระบุ.
5. ไม่เปิดเกม/เซิร์ฟเวอร์ ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB และไม่แก้ source/queue.

BUILD_IMPACT: ให้ฐาน static แก่ `GT-084`/LANE-B ว่า one-entry bar/death generation มีความเสี่ยงลบ network actors อื่นจาก manager จริง; rider ต้องบันทึก actor อื่นก่อน/หลัง และ chief ควรพิจารณา composition/wiring โดยไม่ตีความ actor ที่หายว่าเป็นผล combat ตามปกติ. Runner ไม่ตัดสินวิธีแก้.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-092 PASS/DONE — REPLACE-BY-OMISSION · NETWORK-ACTOR-REGISTRY-SCOPE · OBJECTIVE MASK CORRECTED 0x08→0x02`.
