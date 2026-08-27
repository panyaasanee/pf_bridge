ถึง: chief (cloud) / LANE-B

# RE-110 RESULT — DONE / MIXED: ActionVital +0x30 selects attack behavior; auto-repeat and cadence are bounded-negative

เวลาเริ่มใบ: `2026-08-27T18:21:31.588+07:00`  
เวลาปิดผล: `2026-08-27T18:32+07:00`  
โหมด: static only; ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB/source/queue

## คำตอบสั้น

ปิดใบได้ตามเกณฑ์ mixed positive/bounded-negative:

1. **ท่า/animation เป็น positive field map:** inbound `ActionVital` handler อ่าน `u32 +0x30`, ส่งค่าเข้า behavior lookup `0x00702A10` แล้วสร้าง `CActorTask_UseBehavior` ที่ `0x0047AB30`. `EQUIP_VALUE.n_ATTACK_SKILL` เป็น crosswalk จริงจากชนิดอาวุธไป `BEHAVIOR.n_ID`; behavior ที่ map ได้มี `s_ANIMATION=_C_ATTACK_*`.
2. ACK ปัจจุบัน copy ค่า inbound `+0x30 = 0xEA7D (60029)` กลับไป unchanged แต่ gamedata snapshot นี้ **ไม่มี** `BEHAVIOR.n_ID=60029`; จึงเป็น selector ที่ lookup ไม่ resolve บน snapshot นี้ และอธิบายได้ว่าทำไม reply ปัจจุบันไม่ทำให้เกิดท่าโจมตี.
3. **auto-repeat เป็น bounded negative:** complete zero-gap concrete update ของ inbound `CActorTask_UseBehavior` ไม่มี direct call ไป local ActionVital producer, action queue หรือ serializer. Candidate repeat controller ยังอยู่ที่ local input branches ของ observe-only probe; static นี้ไม่พิสูจน์ว่า reply frame ใดทำให้ยิง ActionVital รอบถัดไปเอง.
4. **cadence เป็น bounded negative:** attack behavior rows ของผู้เล่นที่ crosswalk ได้มี `n_MOB_CD=0` ทั้งหมด และไม่พบ named attack-cadence/interval column. ไม่มี provenance สำหรับแทน `ATTACK_CADENCE_MS_PROVISIONAL=600`.

## T0 — controls และ inputs

- `GameClient/GameClient.local.bin`: size `14,759,424`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `CLIENT_RE_QUEUE.md`: SHA-256 `c9bff51cf0b2fb18830cbb557e8c05b32e5a51897789f8313029f4b0469e0d46`.
- `AGENTS.md`: SHA-256 `8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3`.
- `NEW_ORDERS.txt`: SHA-256 `8fb0f048e49db92b20d6b40aeb08f1fb87a2b4f4e6a7dc00893643dd357ab89f`; ประกาศเฉพาะ GAME_TEST_QUEUE/GT-109 ไม่แก้ objective ใบนี้.
- ชุดค้นร่วม reuse ทั้ง batch: `external/**` 28 files / 28,965,991 bytes / fingerprint `07fdbbdc0b760f728f9266cb1f0a2b6c80f84cc014e497a33b994652b3dc8d89`; `gamedata/**` 1,109 files / 15,319,585 bytes / fingerprint `4c81ba5efc202d426d667b1abef961e2c8c0ec6c8b2075a0a8773f2213de4d8e`.
- verifier `staged/re110_auto_attack_static.py`: SHA-256 `3cccbcb2f6645fe281ead2cd7ab555d61db5e18df27995207e000fc809642c7c`; final run `36/36`, `failed=0`.
- carrier control `re065_static_verify.py` SHA `8c703f9e...c3e61` rerun PASS.

## T1 — reply frame กับ auto-repeat

ActionVital carrier ยัง pin เหมือนเดิม:

- registry: serializer `0x0074E6A0`, inbound handler `0x007516C0`.
- 13 fields ต่อ direction; `+0x30` เป็น `u32`, tag `0x14` ทั้ง W/R.
- serializer main span SHA `ff1183bc...a4e4d`; nested XYZ helper span SHA `b5f5a206...47454`; validation mismatch `0`.

complete recursive CFG ที่ใช้เป็นขอบเขตผลลบ ทุก span `SPAN_GAP_BYTES=0`, `DECODE_ERRORS=0`:

- `CActorTask_UseBehavior::update` `[0x0047AEE0,0x0047B2BF)`, 279 instructions, SHA `d1b7c22f...25cee8`.
- local ActionVital producer `[0x0044D260,0x0044D5F3)`, 263 instructions, SHA `50731991...e9eaf`.
- action queue `[0x005DD800,0x005DD887)`, 45 instructions, SHA `965efce3...159af`.

complete UseBehavior update ไม่มี direct call ไป `0x0044D260`, `0x005DD800` หรือ `0x0074E6A0`. นี่ตอบได้เพียงว่า **inbound behavior-task completion ไม่ได้ต่อ direct edge ไป outbound repeat ใน concrete body นี้**; virtual/resource consumers และ input/controller state อื่นยังอยู่นอกขอบเขต.

observe-only producer config SHA `1226cf89...15fad7` pin candidate local branches ไว้สองจุด (`0x00450D79` / queue call `0x00450E1E`, และ `0x00450F6E` / queue call `0x00450FE2`). config เป็น instrumentation plan ไม่ใช่ runtime result จึงไม่เลือก branch ใดจาก static.

## T2 — field ที่ทำให้เกิด attack pose

ใน inbound handler:

- `0x007516E7/EA` ใช้ `+0x1C/+0x18` resolve performer.
- `0x0075175B` และ `0x007517A5` อ่าน `+0x30`.
- ค่าเดียวกันไหลเข้า behavior lookup `0x00702A10`; handler จากนั้นเรียก `CActorTask_UseBehavior` ctor `0x0047AB30`.

gamedata มี crosswalk แบบมีชื่อ field ชัด ไม่ได้จับคู่เพราะ ID เท่ากัน:

| `EQUIP_VALUE.n_EQUIPTYPE` | `n_ATTACK_SKILL` = `BEHAVIOR.n_ID` | attack animation |
|---:|---:|---|
| 1 | 280 | `_C_ATTACK_000;30` |
| 2 | 284 | `_C_ATTACK_000;28` |
| 8 | 288 | `_C_ATTACK_000;24` |
| 16 | 282 | `_C_ATTACK_000;17` |
| 32 | 290 | `_C_ATTACK_000;24` |
| 64 | 286 | `_C_ATTACK_018;28` |

ดังนั้น reply composition ต้อง resolve อาวุธที่ equip อยู่จริงไป `EQUIP_VALUE.n_ATTACK_SKILL` ก่อน แล้วใช้ behavior id นั้นที่ ActionVital `+0x30`. ใบนี้ยังไม่รู้ว่า Arena01 equip type ใด จึงไม่เลือก 280/282/284/286/288/290 ให้โดยเดา.

server `action_ack.py` SHA `0318f1f2...a08ae` ปัจจุบัน encode `fields["action_u32_30"]` unchanged. ค่าที่ capture/config อ้างคือ `0xEA7D=60029`; `CONSTDATA_TH__BEHAVIOR.tsv` SHA `79ee11e4...bf4e` มี 2,279 rows แต่ไม่มี row 60029.

## T3 — cadence

- `CONSTDATA_TH__BEHAVIOR.n_MOB_CD` มีอยู่จริง แต่หก normal player attack rows ข้างบนเป็น `0` ทั้งหมด จึงไม่ให้ cadence.
- suffix ใน `s_ANIMATION` เช่น `;17`, `;24`, `;28`, `;30` ไม่มี field/crosswalk บอกว่าเป็น milliseconds จึงห้ามเอาไปแทน cadence.
- ค้น `PF_GAMEDATA_COLUMNS.tsv` และ gamedata snapshot แล้วไม่พบ named `ATTACK_CADENCE`, `ATTACK_INTERVAL` หรือ `CADENCE_MS` column.
- `mob_combat.py` SHA `6af6f1b8...bd36` ยังระบุ `ATTACK_CADENCE_MS_PROVISIONAL = 600` และบอกชัดว่าเป็น guess รอ RE-110. Static result นี้ยังไม่มีค่าจริงมาแทน.

## Mandatory search — external

อ่าน `external/00_SEARCH_HERE_FIRST.md` แล้วค้น textual corpus ทั้ง fingerprint ข้างต้น:

- เจอ ActionVital registry/serializer/handler/getter, exact W/R field rows และ capture validation ดังที่ระบุ.
- ไม่พบ semantic crosswalk ชื่อ `AutoAttack|AttackCadence|CadenceMs|AttackInterval`.

ผลลบจำกัดที่ 28-file external snapshot และ named semantic rows; ไม่ claim ว่า client ไม่มี controller state ภายใน.

## Mandatory search — gamedata

อ่าน `gamedata/00_SEARCH_HERE_FIRST.md` แล้วค้นทั้ง fingerprint ข้างต้น:

- เจอ `EQUIP_VALUE.n_ATTACK_SKILL -> BEHAVIOR.n_ID -> s_ANIMATION` crosswalk สำหรับ attack pose.
- ไม่พบ `BEHAVIOR.n_ID=60029`.
- normal player attack rows ให้ `n_MOB_CD=0`; ไม่พบ named cadence/interval column.

ผลลบจำกัดที่ snapshot นี้; ไม่ตีความเลข suffix animation หรือ `n_MOB_CD` อื่นเป็นเวลาโดยไม่มี crosswalk.

## T4 — attended capture แคบที่สุด

one-field A/B เท่านั้น:

1. ระบุ equip type ของผู้เล่นจาก source ที่มี provenance แล้ว resolve `n_ATTACK_SKILL` ตามตารางด้านบน.
2. ส่ง ActionVital reply สองชุดที่ performer/target/XYZ/heading/ทุก field เหมือนกัน; control ใช้ `+0x30=0xEA7D`, mutant เปลี่ยนเฉพาะ `+0x30` เป็น resolved behavior id.
3. เก็บ client-observable pose/animation แยกจาก wire timestamps. พร้อมกันเปิด existing producer probe แบบ observe-only แล้ว timestamp outbound ActionVital ทุกครั้ง; ห้าม patch client, sweep หลาย behavior id หรือเปลี่ยน cadence พร้อมกัน.
4. ยอมรับ pose mapping เมื่อ one-field mutant เปลี่ยนท่าซ้ำได้. ยอมรับ auto-repeat/cadence เมื่อ wire แสดง outbound ActionVital รอบถัดไปเองหลายช่วงและวัด interval distribution ได้; screenshot อย่างเดียวพิสูจน์ cadence ไม่ได้.

## Nonclaims / method ceiling

1. ไม่ claim ว่า ActionVital reply ไม่มีทางทำให้ repeat; claim เพียง complete concrete UseBehavior update ไม่มี direct outbound edge.
2. ไม่ claim ว่า candidate branch ใดเป็น auto-repeat จน observe-only probe ได้ runtime evidence.
3. ไม่ claim ว่า `0xEA7D` เป็น message id หรือ behavior ที่ถูกต้อง; ที่นี่เป็น observed `+0x30` value เท่านั้น.
4. ไม่ claim ว่า animation suffix หรือ `n_MOB_CD` เป็น milliseconds.
5. ไม่เลือก attack behavior ของ Arena01 โดยเดา; ต้องมี equip-type crosswalk ของ actor ปัจจุบัน.
6. ไม่ใช้ server provisional 600ms เป็น original-client evidence.
7. auto-repeat/cadence ถึง **method ceiling** ของ static snapshot นี้; ห้าม rerun linear/static search เดิมจนมี controller symbol/crosswalk ใหม่หรือ attended observe-only capture. Pose field ปิดแบบ positive และทำ one-field validation ต่อได้.

BUILD_IMPACT: server reply ควรเลิกถือ observed `0xEA7D` เป็น pose selector ที่ใช้ได้ และเตรียม resolve `equipped weapon type -> EQUIP_VALUE.n_ATTACK_SKILL -> ActionVital +0x30`; แต่ยังไม่ควรแก้ production composition จน one-field A/B ยืนยัน actor/equipment provenance. คง `ATTACK_CADENCE_MS_PROVISIONAL=600` พร้อมป้าย provisional ต่อไป เพราะไม่มีค่าจริงจาก static และห้ามแทนด้วย animation suffix/`n_MOB_CD`.
