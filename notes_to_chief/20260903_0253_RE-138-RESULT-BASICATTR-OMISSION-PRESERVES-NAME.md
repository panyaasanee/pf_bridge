ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย

ถึง chief / LANE-A / Panya

# RE-138 RESULT — DONE / PASS: reconcile ไม่ส่งชื่อซ้ำ แต่ BasicAttr merge เก็บชื่อเดิมเมื่อ bit `0x0001` ถูกละ

- Ticket: `RE-138 NAME-LABELS-VANISH-AFTER-MOVE-001`
- Ticket START: `2026-09-03T02:46:41.651+07:00`
- Queue SHA-256: `86d51b29d932cdb1d51d2fccaa9dd9f31ddaf1390b6f31050fc4c10454e42177`
- Route override: Panya เจ้าของโปรเจกต์สั่งตรงให้ทำบนเครื่อง bridge เพราะคำถามต้องอ่าน current client image แม้หัวใบยังเขียน `STATIC-ON-CLOUD`
- Method: static/read-only only; ไม่เปิดเกม/server, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, source, queue, external, gamedata หรือ git

## Direct answer

**Wire/server:** retained และ entrant ต่างได้รับ `NPCAttr` ซึ่งสืบทอด/serialize `BasicAttr`; ทั้งสองกลุ่มได้ BasicAttr mask `0x030C` เหมือนกัน และ **ไม่มี name bit `0x0001`**. Entrant ต่างจาก retained เพียงได้ `MovementAttr` เพิ่มด้วย full mask `0xFF`; retained ไม่มี MovementAttr. ดังนั้นคำว่า “retained เป็น NPCAttr-only” ไม่ได้แปลว่าไม่มี BasicAttr แต่แปลว่า BasicAttr ที่อยู่ใน NPCAttr ไม่ได้บรรทุกชื่อรอบนี้.

**Client mask-within-attr:** การละ bit ชื่อ **ไม่ล้างชื่อเดิม** เมื่อมี attr เดิมให้ merge. `NPCAttr` merge slot `+0x30` ที่ `0x00466DC0` เรียก `BasicAttr` merge `0x00465610`; ที่ `0x0046564E` ตรวจ incoming/destination mask `+0x70 & 0x0001`. ถ้า bit มีอยู่จะคงค่าที่ decode เข้ามา แต่ถ้า bit ไม่มี จะ copy `std::wstring` ชื่อจาก attr เก่าที่ `source+0x28` ไป `incoming+0x28` (`0x00465654..0x0046565B`). นี่เป็น positive complete-function evidence ว่า omitted field ถูกเติมจากของเดิม ไม่ใช่ถูกเคลียร์.

ดังนั้นสมมติฐานในใบว่า “mask แคบกว่าล้าง name ภายใน attr object” **ถูกหักล้าง**. อาการป้ายชื่อหายจริงยังอาจเกิดเมื่อไม่มี attr เก่าให้เติม (เช่น object/actor ถูกสร้างใหม่หรือเส้นทาง generation เปลี่ยนเจ้าของ object) หรือจากเส้นทาง UI/actor reconciliation อื่น แต่ห้ามอ้างว่าเกิดจาก BasicAttr merge เพียงเพราะ server ละ name bit.

## Server evidence

Current implementation: `src/pirateforce_foundation/population.py`, SHA-256 `df7bedb387963b67c0e4438479b057e8023a2a63efa1016000994982de18d52f`.

- `population.py:174-177` ระบุ contract: retained มี NPCAttr; entrant มี NPCAttr + MovementAttr; omitted actor ถอนด้วย omission.
- `population.py:202-204` แยก retained/entrant/omitted จาก membership sets.
- `population.py:206-213` สร้าง NPCAttr สำหรับ **ทุก current member** โดยเรียก `make_npc_attr(... visual_preset)` โดยไม่ส่ง `basic_name`, แล้วเริ่ม attrs ด้วย NPCAttr ตัวเดียว.
- `population.py:214-223` เพิ่ม MovementAttr เฉพาะ entrant และกำหนด `mask=FULL_MOVEMENT_MASK`; `population.py:224-227` ห่อ actor entry.

Frozen wire builder: `current/pf_login_game_server_v141.py`, SHA-256 `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`.

- `v141:1139-1141` กำหนด `basic_name=""` เป็น default; population call ไม่ override.
- `v141:1149-1152` ผูก BasicAttr `+0x28`, mask bit `0x0001` กับชื่อ/LABEL_NAME.
- builder ใช้ BasicAttr mask `0x0004|0x0008|0x0100|0x0200 = 0x030C`; bit `0x0001` เพิ่มเฉพาะเมื่อ `basic_name` ไม่ว่าง.
- `v141:1837-1853` แสดงรูปเดียวกันใน frozen generation: ทุกแถว NPCAttr; เฉพาะ initial/entrant เพิ่ม MovementAttr mask `0xFF`.

สรุป mask ต่อกลุ่ม:

| กลุ่ม | NPCAttr / inherited BasicAttr | MovementAttr |
|---|---|---|
| retained | Basic mask `0x030C`, ไม่มี name bit `0x0001`; derived NPC fieldsตาม builder | ไม่มี |
| entrant | Basic mask `0x030C`, ไม่มี name bit `0x0001`; derived NPC fieldsตาม builder | full mask `0xFF` |

## Client evidence: omitted BasicAttr field preserves the old value

Client image: `GameClient.local.bin`, 14,759,424 bytes, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

- BasicAttr vtable `0x00F0E760`: slot `+0x30 = 0x00465610` (assign/merge), slot `+0x34 = 0x004656F0` (codec).
- NPCAttr vtable `0x00F0E7E0`: slot `+0x30 = 0x00466DC0`, slot `+0x34 = 0x00466EB0`.
- Complete BasicAttr merge `[0x00465610,0x004656EF)`, 223 bytes, SHA-256 `f8166d39e5e85dd5fa64091994c38c37f06e688248d308cff358ba4f60ebc4bf`.
- Complete NPCAttr merge `[0x00466DC0,0x00466EA7)`, 231 bytes, SHA-256 `2c9f05ba5accac3a6b2743aed456a7754eca7d10b2382231c68019a782461c4e`.
- Complete BasicAttr codec `[0x004656F0,0x00465983)`, 659 bytes, SHA-256 `d0c15b74a36077df30a0e60dbeb8441e878c08b82587c1ea55365ab2ebd70020`.

Decisive flow:

1. `0x00466DF6..0x00466DF9`: NPCAttr merge passes the existing/source attr to BasicAttr merge.
2. `0x00465646..0x00465649`: BasicAttr merge first merges its base.
3. `0x0046564E`: `test byte ptr [destination+0x70], 1` checks whether the incoming/destination object carried name bit.
4. Bit present -> jump over fallback copy. Bit omitted -> `0x00465654..0x0046565B` assigns `source+0x28` into `destination+0x28` through the imported `std::wstring` assignment.
5. The same function repeats this omitted-bit fallback pattern for the remaining BasicAttr fields through `0x004656E6`; both terminal exits are covered.

The field identity is independently pinned in `PF_A2_ATTR_FIELD_DELTA.tsv`: `BasicAttr@0x28.var`, mask `0x0001`, UTF-16 wstring, default empty, and exact CNetNPC nameboard consumer `[0x005BDB46,0x005BDBA0)` SHA-256 `ba82f1f510c578d04cb827cf364ae488b903fcd78fc02e7d55c484033fbd8b26`. Table SHA-256 `44f80d6aa975dfe030a0e537d5166aaa9e051c4d55f693d7e724fa2b17b19c1f`.

## Mandatory searches

- **Searched `pf_bridge\external\`:** complete tree 2,683 files / 930,201,065 bytes; one-pass metadata fingerprint `b68405023755ccad7dc388f578166e9426412ee4595e715a68944ca057b0f1b2`. Terms: `NPCAttr|BasicAttr|CNetNPC|PickupTerrainThing|TerrainThingPool|TerrainThing|0x006AF970|006AF970`. Relevant hits appeared in 15 files, including `PF_A2_ATTR_FIELD_DELTA.tsv`, `PF_A2_BASIC_CODEC_CORRECTION.tsv`, `PF_ATTR_*`, `PF_SERIALIZER_FIELDS.tsv`, `PF_PROTOCOL_REGISTRY.tsv`, and `PF_FIELD_VALIDATION.tsv`. The image-backed field table provides the name/mask/nameboard crosswalk used above; capture validation remains `NOT_OBSERVED`, so this letter does not claim a captured runtime frame.
- **Searched `pf_bridge\gamedata\`:** complete tree 1,109 files / 15,319,585 bytes; one-pass metadata fingerprint `47ae2e8837460ff118eebe6a2bc220363f417235257bb5ce27ba88dbc5df4ed3`. Same term family produced zero matching files/hits; no table/Lua crosswalk changes the image-derived BasicAttr merge result.

`PF_PROTOCOL_REGISTRY.tsv` SHA-256 `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`.

## Evidence-layer separation

- **wire/source proven:** exact retained/entrant attr composition and masks emitted by current server source.
- **client static proven:** BasicAttr name bit/field/nameboard identity and omitted-bit fallback copy inside complete merge functions.
- **client-observable not claimed:** ไม่ได้เปิดเกมและไม่ได้ยืนยันว่าป้ายชื่อยังอยู่/หายหลังเดินใน build นี้. ใบ attended หลังแก้ที่หัวใบขอไว้ยังไม่ได้เปิดโดยงานนี้.
- **DB not claimed:** ไม่อ่านหรือแตะ canonical DB และไม่มี DB evidence ในข้อสรุปนี้.

## Nonclaims

- ไม่อ้างว่าการละ name bit เป็นสิ่งที่ควรทำตามนโยบาย “ส่ง attr ให้ครบที่สุด”; ตอบเฉพาะผลเชิงกลไกใน current client.
- ไม่อ้างว่า actor-generation reconciler จะ reuse object/attr เดิมทุกกรณี. ถ้ามันสร้าง object ใหม่ ค่า default ชื่อว่างยังเป็นไปได้และต้องพิสูจน์ด้วยใบแยกหรือ attended evidence.
- ไม่อ้างว่า MovementAttr มีผลต่อ nameboard.
- ไม่อ้าง wire opcode จาก ID ที่เท่ากันโดยไม่มี crosswalk; ข้อสรุปยึด class/vtable/field consumer และ source builder โดยตรง.
- ไม่ใช้ linear disassembly เป็นหลักฐานผลลบ: ข้อสรุป preservation เป็น positive complete-function flow; ขอบเขตที่ยังไม่พิสูจน์ถูกระบุข้างต้น.

## BUILD_IMPACT

**ไม่ต้องแก้ client และผลนี้ไม่รองรับการแก้ด้วยการส่ง name ซ้ำเป็นข้อจำเป็นเชิง protocol.** Current client มี merge semantics ที่เก็บค่าชื่อเดิมเมื่อ bit `0x0001` ถูกละ. ถ้าจะทำตามนโยบายส่ง attr ให้ครบ การเพิ่ม `basic_name` ใน population reconcile ยังเป็น hardening ที่สมเหตุผล แต่ต้องถือว่าเป็น policy/robustness change ไม่ใช่ root-cause ที่ static นี้พิสูจน์แล้ว. Root cause ของอาการ “ชื่อหายหลัง move” ต้องตรวจต่อที่ object lifetime / actor generation reuse หรือยืนยัน client-observable หลัง server ส่งชื่อครบ.

