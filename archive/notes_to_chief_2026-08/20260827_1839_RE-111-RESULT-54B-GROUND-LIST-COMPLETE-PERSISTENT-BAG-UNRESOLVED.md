ถึง: chief (cloud) / LANE-B

# RE-111 RESULT — DONE / BOUNDED-NEGATIVE: 54B ground-list shape is complete; persistent loot-bag/model transport remains unresolved

เวลาเริ่มใบ: `2026-08-27T18:34+07:00`  
เวลาปิดผล: `2026-08-27T18:39+07:00`  
โหมด: static only; ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB/source/queue

## คำตอบสั้น

ไม่พบ “field ที่ขาด” ซึ่งเติมเข้า `MOB_LOOT_DROP 54B` แล้วจะทำให้เป็นถุง loot ถาวร เพราะ `MOB_LOOT_DROP` เป็น **ชื่อ event ฝั่ง server ของเรา** ไม่ใช่ชื่อ message class ที่ recover จาก client. สิ่งที่ส่งจริงคือ generic `GSCN_RunTimeProtocolRes` derived-list `0x08`, หนึ่ง element, รูปทรง 54B ที่ครบตาม codec ของมันแล้ว:

`element key + dirty mask 0x12 + full item_id + XYZ`

client create path ใช้ `item_id` เดียวไป resolve `s_NAME`, `n_DROPMODEL_TYPE`; update path resolve `s_TAG_EXTRA`, `n_QUALITY`. จึงไม่มี name/rarity/model-id wire field แยกใน current shape. Optional `+0x1B/+0x1A` เป็น label-property gate/index ไม่ใช่ spawn/model gate และ mask `0x12` ตั้งใจไม่ส่งสอง field นี้; ctor มี default property อยู่แล้ว.

ผลลบชั้น static ที่เหลือ:

- concrete create/update graph ไม่มี named lookup ของ `n_ID_MODEL`; จึงยังหา resource/model ถุงเรืองแสงไม่ได้จาก graph นี้.
- item ที่ GT-084-R2 ส่งจริง `2400046/2400047` resolve เป็น `ITEM_MISC` rows 46/47 และทั้งคู่มี `n_ID_MODEL=0`; นี่เป็น candidate ต่ออาการ no-model แต่ **ยังไม่เป็น causal proof** เพราะ concrete graph ไม่มี named `n_ID_MODEL` lookup.
- external corpus มีตระกูลแยก `FightingDropModule_Client` / `FightingDropNotify`, แต่ serializer/handler ยัง `UNKNOWN` และ capture `NOT_OBSERVED` ทุก direction. transport ถุง loot แบบเดิมอาจอยู่ในตระกูลนี้ แต่ static ปัจจุบันพิสูจน์ไม่ได้ จึงห้ามเปลี่ยน candidate เป็นข้อสรุป.

## T0 — controls และ inputs

- `GameClient/GameClient.local.bin`: size `14,759,424`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `CLIENT_RE_QUEUE.md`: SHA-256 `c9bff51cf0b2fb18830cbb557e8c05b32e5a51897789f8313029f4b0469e0d46`.
- `AGENTS.md`: SHA-256 `8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3`.
- `NEW_ORDERS.txt` ถูก reread หลังเปลี่ยนระหว่าง batch; SHA ปัจจุบัน `97e9068d6d19d94454a86c63780c184064689f880aba038c9b57911c5d4dd10b`, เป็น R196 attended/GT queue เท่านั้น ไม่แก้ objective RE-111.
- ชุดค้นร่วม reuse: `external/**` 28 files / 28,965,991 bytes / fingerprint `07fdbbdc0b760f728f9266cb1f0a2b6c80f84cc014e497a33b994652b3dc8d89`; `gamedata/**` 1,109 files / 15,319,585 bytes / fingerprint `4c81ba5efc202d426d667b1abef961e2c8c0ec6c8b2075a0a8773f2213de4d8e`.
- GT-084-R2 result/addendum SHA `242247c8...341a`: wire `2400046:x1@0x100000`, `2400047:x1@0x100001`, `MOB_LOOT_DROP 54B ×2`; owner ยืนยันไม่เห็นทั้งสองชิ้น.
- current `mob_loot.py` SHA `52bd656f...40a7b`.
- immutable V141 serializer input `current/pf_login_game_server_v141.py` SHA `2eb05ed2...a4c22`.
- verifier ใบนี้ `staged/re111_loot_render_static.py` SHA-256 `b6ac2cf3216675b6b46044121c2838977ccb178776eaf8973363279f4447c87f`; final run `30/30`, `failed=0`.
- reused adversarial controls: `re066_static_verify.py` SHA `676c5837...11308`, PASS; `re067_static_verify.py` SHA `838c70ef...026e2`, `54/54` PASS.

## T1 — handler/field shape ที่ spawn generic ground element

RE-066 rerun ยืนยัน complete zero-gap path เดิม:

- parent codec `[0x005E3EE0,0x005E404E)` -> inbound handler `[0x005E4060,0x005E41CD)` -> handoff `0x005F53A0` -> consumer `[0x006AF970,0x006B03E3)`.
- list codec `[0x005F85B0,0x005F8869)`, SHA `ce0a58f7...f1b5b`; allocator `[0x005F82C0,0x005F83F9)`.
- create `[0x005F41E0,0x005F4897)`, SHA `d8011e41...0f105`; update `[0x005F4C00,0x005F4DEE)`, SHA `7b14d16c...c06c2`.
- ทุก span ข้างต้น decoded ครบ, gap `0`, errors `0`.

current composer pin:

- PC 44B, framed 54B; RuntimeRes derived bit `0x08`; list count `1`.
- element key: tag `0x14` u32 at runtime element `+0x10`.
- dirty mask: tag `0x0B`, value `0x12`.
- mask bit `0x02`: payload full item id, tag `0x14`, runtime `+0x14`.
- mask bit `0x10`: XYZ, tags `0x2A`, runtime `+0x1C/+0x20/+0x24`.

ดังนั้น 54B ที่ส่งมี identity/key, item payload และตำแหน่งครบสำหรับ generic ground-list create path. ไม่ได้ขาด string ชื่อ, rarity scalar หรือ model id wire field; current handler ไม่ได้อ่าน field เหล่านั้นจาก wire แยก.

## T2 — name/rarity/model path

### ชื่อและ item attributes

payload `+0x14` เป็น full item id ไม่ใช่ table row ordinal:

- create path A `0x005F46FA -> 0x00892580 -> table/row decoder` query `s_NAME`.
- create path B `0x005F426D -> 0x00892DD0 -> table/row decoder` query `n_DROPMODEL_TYPE`.
- update `0x005F4CAC -> 0x00892DD0` query `s_TAG_EXTRA`, `n_QUALITY`.

GT-084-R2 items ใน gamedata:

| full id | table row | client-resolvable name | `n_ID_MODEL` | `n_DROPMODEL_TYPE` | `n_QUALITY` | `s_TAG_EXTRA` |
|---:|---:|---|---:|---:|---:|---|
| 2400046 | `ITEM_MISC/46` | `Reward Green Gem` | 0 | 9 | 2 | `3;3` |
| 2400047 | `ITEM_MISC/47` | `Advanced Gem Pack` | 0 | 0 | 1 | empty |

`CONSTDATA_TH__ITEM_MISC.tsv` SHA `8cd1774d...d5292`; `TEXTDATA_TH__ITEM_MISC_TIP.tsv` SHA `163cf4d0...85ed2`; source drop table `DROPS_NORMAL` SHA `f8df1d7c...b913` มี full ids ทั้งคู่.

### label property / rarity appearance

RE-067 pin codec fieldsเพิ่ม:

- mask bit `0x08` -> optional gate `u8 +0x1B`.
- mask bit `0x20` -> optional selector `u8 +0x1A`.
- ctor defaults `+0x1B=0`, `+0x1A=1`; เมื่อ gate เป็น 0 create ใช้ property `0x34`.
- เมื่อ gate เปิดและ selector 1..6 จึง map ไป property ids `0x5D..0x62`; update ยัง query positive `n_QUALITY`.

current mask `0x12` ไม่มี bits `0x08/0x20`, แต่การไม่มี field นี้ **ไม่ปิด create** เพราะมี default path. และ property ids `0x34/0x5D..0x62` ยังไม่มี crosswalk ไป `FONT_COLOR`; ห้ามเรียกเลขเหล่านี้ว่าสีเขียว/rarity color จากเลขที่ดูคล้ายกัน.

### model/resource

`n_ID_MODEL` literal มีอยู่ใน image แต่ RE-066 census พบ `21` global dword refs และ **0 ref ใน concrete create/update/consumer graph ที่ปิดครบ**. จึงไม่พบ resource name ของถุงหรือ proven wire field ที่เลือก model. `n_ID_MODEL=0` ของทั้งสอง item เป็น candidate ที่ควร A/B ต่อ แต่ static นี้ไม่อ้างว่าเป็นสาเหตุ.

## Mandatory search — external

อ่าน `external/00_SEARCH_HERE_FIRST.md` แล้วค้น registry/fields/validation ทั้ง fingerprint:

- ไม่พบ class ชื่อ `MOB_LOOT_DROP`; ชื่อนี้เป็น server console label.
- พบ `FightingDropModule_Client` และ `FightingDropNotify` เป็นคนละ family, แต่ getter/vtable/serializer/handler ที่ต้องใช้ยัง `UNKNOWN` และ field rows ระบุ `registry_serializer_unresolved:getter_hits=0`.
- validation ของสองชื่อทั้ง W/R เป็น `NOT_OBSERVED`, capture count `0`.

ผลลบจำกัดที่ external snapshot นี้; ไม่ claim ว่า FightingDrop family คือคำตอบ เพียงเป็น unresolved candidate ที่ห้าม join เข้ากับ RuntimeRes ground list เพราะชื่อมีคำว่า drop.

## Mandatory search — gamedata

อ่าน `gamedata/00_SEARCH_HERE_FIRST.md` แล้วค้นทั้ง fingerprint:

- เจอ item full-id rows และ fields `s_NAME/n_ID_MODEL/n_DROPMODEL_TYPE/n_QUALITY/s_TAG_EXTRA` ข้างต้น.
- เจอ `n_DROPMODEL_TYPE` ในหก item-family tables; ไม่พบตาราง/resource crosswalk ชื่อ bag/sack/ground-loot model ที่ผูกค่านี้เข้ากับ asset.
- `FONT_COLOR` เป็นตาราง RGB แยก แต่ไม่มี crosswalk จาก item property ids; ไม่ join เพราะ id เท่ากัน.

## Prior observed boundary

current server pin เก็บผล attended เดิมของ **pipe เดียวกัน** ไว้: GT-045 เคยเห็น name label หนึ่งอันและ brown dust, label อยู่ `0.2–0.4s`, ไม่มี model ใต้ label ที่เห็น และไม่ persist. นี่พิสูจน์ว่า shape นี้ทำ generic ground announcement ได้อย่างน้อยหนึ่งกรณี; ไม่พิสูจน์ว่ามันเป็น persistent monster-loot bag และไม่ลบผลลบของ GT-084-R2 ซึ่ง owner ไม่เห็น item สองชิ้น.

## T3 — attended capture แคบที่สุด

แบ่งเป็นสองคำถาม ห้ามรวม:

1. **current handler acceptance/render:** replay one element หลัง death โดยคง key/XYZ/order/envelope ทุกอย่าง; A=`item_id 2400046`, B=เปลี่ยนเฉพาะ payload item id ไปหนึ่ง id ที่เคยทำให้ pipe วาด label (พร้อม timestamp frame และวิดีโอ high-frame-rate). ถ้า B ขึ้นแต่ A ไม่ขึ้น จึงชี้ไป item-row resolution; ยังไม่แปลว่า model field ใดเป็นเหตุ เพราะเปลี่ยน item id เปลี่ยนหลาย gamedata attributes.
2. **model candidate:** ก่อน run ให้ mine คู่ item rows ที่ `n_DROPMODEL_TYPE/n_QUALITY/s_TAG_EXTRA` เท่ากันแต่ `n_ID_MODEL` ต่างกันมากที่สุดเท่าที่หาได้; ส่ง frame เดิมเปลี่ยนเฉพาะ full item id. ผลนี้เป็น branch triage เท่านั้นจนมี client lookup crosswalk ของ `n_ID_MODEL`.
3. **label selector แยก:** A mask `0x12`; B เพิ่มเฉพาะ logical selector field (`+0x1B=1` พร้อม required mask bit; ถ้าจะทดสอบ index ให้เป็นอีก run). ใช้พิสูจน์ label property เท่านั้น ห้ามใช้พิสูจน์ model/persistence.
4. เก็บ client-observable pixels แยกจาก exact wire. หาก goal คือถุง loot ถาวรจริง ต้อง capture original-server FightingDrop traffic หรือ resolve family นั้นก่อน; ห้าม sweep unknown bytes ใน RuntimeRes frame.

## Nonclaims / method ceiling

1. ไม่ claim ว่า current 54B malformed; static และ prior attended control พิสูจน์ว่าเป็น complete generic ground-list shape.
2. ไม่ claim ว่า `n_ID_MODEL=0` ทำให้ไม่วาด model; เป็น candidate เพราะสอง current rows มี 0 และ concrete graph ยังไม่พบ named consumer.
3. ไม่ claim ว่า `n_DROPMODEL_TYPE` เป็นหรือไม่เป็น switch; current rows ต่างกัน 9/0 แต่ทั้งสองไม่ถูกเห็น และ prior evidence บอกเพียงค่าหนึ่งไม่ sufficient.
4. ไม่ claim property ids เป็นสี rarity หรือ join กับ `FONT_COLOR`.
5. ไม่ claim FightingDrop family คือ original loot transport จนได้ serializer/handler/capture; แยก wire family จาก client-observable เสมอ.
6. ไม่ claim ว่า owner พลาด label สั้น; GT-084-R2 addendum เป็น negative ชั้นจอของรอบนั้น ส่วน GT-045 เป็น positive คนละรอบ/คนละ item.
7. persistent bag/model ถึง **method ceiling** ของ current RuntimeRes concrete graph. ห้าม rerun linear/string search เดิมจนมี FightingDrop capture, receiver/model-resource xref หรือ attended one-variable evidenceใหม่.

BUILD_IMPACT: **ห้ามเติม name/rarity/model bytes แบบเดาลง 54B หรือเปลี่ยน mask สุ่ม**; current handler shape ไม่มี field เหล่านั้นและ complete สำหรับ generic ground announcement. Production lane ต้องยังบอกความจริงว่า no persistent/clickable object. งานถัดไปที่มี provenanceคือ (ก) one-variable item-row/selector A/B เพื่อแยก label path และ (ข) recover/capture `FightingDropModule_Client/FightingDropNotify` หรือ resolve model-resource consumer; ก่อนอย่างใดอย่างหนึ่งยังไม่มี safe server fix สำหรับถุงเหลืองเรืองแสง/ป้าย rarity ถาวร.
