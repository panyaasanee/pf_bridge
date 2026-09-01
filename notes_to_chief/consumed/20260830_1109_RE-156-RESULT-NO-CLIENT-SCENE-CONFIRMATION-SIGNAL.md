ถึง chief — ผล RE-156 SCENE-IDENTITY-SIGNAL-001 (STATIC-ON-BRIDGE)

# RE-156 — DONE / PASS (static, bounded to committed artifacts)

TICKET START: `2026-08-30T11:03:56.748+07:00`  
โหมด: static/read-only เท่านั้น; ไม่เปิดเกม ไม่บูต server/client ไม่ใช้ capture และไม่แตะ canonical DB

## คำตอบสั้น

**ใน protocol corpus + receive path ที่ commit อยู่ตอนนี้ ไม่มีไบต์จาก client ที่นับเป็นการยืนยันว่า client เรนเดอร์ scene ใดจริง**

- proxy ที่ใกล้ที่สุดคือ `TargetPosVital` (`0x2A90`) ตัวแรก/ตัวถัดไปหลัง server ส่ง teleport แต่ payload ที่ตัวรับตีความมีเพียง `x, y, z, heading, moving, derived_mask`; **ไม่มี scene id หรือ scene seq**
- `runtime_ack_sent` ไม่ใช่ scene ACK: มันเป็น latch ว่าได้รับ `RuntimeReq` แรกแล้ว ไม่ตรวจชนิด vital หรือ scene
- `TeleportCheckVital` (`0x4477`) ที่รับได้มีเพียง `u16 +0x14` ซึ่ง source ตั้งชื่อแบบ offset และระบุ semantics ว่า unassigned; ไม่ใช่ scene id
- client image มี static **R codec** ของ `TeleportVital` (`0x25A2`) ซึ่ง schema ของ target object มี `SceneID` ได้ แต่ codec availability ไม่พิสูจน์ว่า client ส่ง vital นี้กลับหลัง load; current v141 ไม่มี inbound `TELEPORT_VITAL` parser/dispatch branch เลย จึงยกให้เป็น scene-confirmation ไม่ได้

นี่คือ **ขีดจำกัดถาวรของ protocol ที่วัดได้ใน committed corpus ปัจจุบัน**: จนกว่าจะมี attended capture แสดง client-originated vital ที่พก scene หรือมี artifact/crosswalk ใหม่ เราบอกได้เพียง “server ตั้งใจ/เชื่อว่าอยู่ scene X” ไม่ใช่ “client ยืนยันว่าเรนเดอร์ scene X แล้ว”

## Job 1 — inbound signal audit: DONE

### `TargetPosVital` (`0x2A90`)

- ID pin: `current/pf_login_game_server_v141.py:395`, name map `:447`
- decoder: `:2981-2992` อ่าน float32 `x/y/z/heading` และ byte `moving`; ไม่มี field scene
- exact V141 singleton validator: `:2995-3018` อ่าน `x/y/z/heading/moving/derived_mask`; ไม่มี field scene
- receive sink: `:4235-4260` เก็บเพียง `self.last_target_pos = (x, y, z, heading)`

ดังนั้น TargetPos หลัง teleport บอกได้ว่า client ส่งพิกัดอะไรกลับมา แต่ไม่มี crosswalk ในเฟรมที่บอกว่าพิกัดนั้นเป็นของ scene ใด การนำ `selected.position.scene_id` ของ server มาประกบเป็น scene claim จะเป็นการใช้ค่าที่ server เขียนเอง ไม่ใช่ client confirmation

### `runtime_ack_sent`

`current/pf_login_game_server_v141.py:3768-3772` ส่ง empty runtime response เมื่อเจอ RuntimeReq แรก แล้วตั้ง `runtime_ack_sent=True` ทันที โดยไม่ตรวจ scene และไม่ผูกกับ TargetPos/Teleport; จึงเป็นเพียง transport/progress proxy

### `TeleportCheckVital` (`0x4477`)

- ID pin: `current/pf_login_game_server_v141.py:394`, name map `:446`
- decoder `:3199-3223` อ่าน `field_u16_14` ค่าเดียว และ docstring ระบุความหมายยังไม่ถูกพิสูจน์
- receive branch `:4052-4068` ตรวจ challenge echo ที่ exact shape/value; ไม่มี scene field และไม่ตอบเฟรม

ค่าเดียวกันกับ scene id โดยบังเอิญไม่ใช่ crosswalk; ห้ามจับคู่เพราะเลขเท่ากัน

### `TeleportVital` (`0x25A2`)

`external/PF_SERIALIZER_FIELDS.tsv` มี W/R schema และใน R path มี target-object subcall `0x005DF250` พร้อม tag `0x12` ที่ object offset `+0x12` (scene-bearing object schema) แต่:

1. `external/PF_FIELD_VALIDATION.tsv:73` ยังจัด R side เป็น `A2_STATIC_OPEN`, ไม่ใช่ observed client emission
2. current v141 ใช้ `TeleportVital` ฝั่งส่ง (`make_v137_marker1_transport`, `make_login_teleport`) แต่ grep ทั้งไฟล์ไม่มี `nested_id == TELEPORT_VITAL` inbound branch และไม่มี `parse_teleport_vital`
3. static read/write codec existence บอกได้ว่า object อ่าน/เขียนรูปทรงใด ไม่บอกว่า client emit เมื่อ scene-load สำเร็จ

จึงไม่ใช่คำตอบบวกของใบนี้

## Job 2 — closest proxy / boundary: DONE

ลำดับ proxy ที่ honest ที่สุดในระบบปัจจุบันคือ:

1. server ส่ง `TeleportVital` ที่มี scene/target ตามค่าที่ server เลือก
2. `runtime_ack_sent` ยืนยันเพียงว่ามี runtime traffic ต่อ
3. exact `TargetPosVital` ยืนยันเพียงว่ามี client-originated position tuple ต่อ
4. server-side `selected.position.scene_id` บอก intended/selected scene เท่านั้น

สามค่าหลังรวมกันยังไม่สร้าง client-originated scene id; จึงห้ามเรียก gate ที่อ่านชุดนี้ว่า “client scene admission/confirmation”

## Mandatory searches (ทำก่อน source audit)

### `pf_bridge/external/`

- ขอบเขต: recursive ทั้ง root, `130 files`, `37,060,029 bytes`
- manifest SHA-256: `3a665f1dce22530eddc177e85699faa22ab9abfaf444182269119345ddea624e`
- เจอ: registry/field rows ของ `TargetPosVital`, `TeleportVital`, `TeleportCheckVital`; โดยเฉพาะ `PF_PROTOCOL_REGISTRY.tsv:33,37,70`, `PF_FIELD_VALIDATION.tsv:64-65,72-73,138-139`, และ serializer rows ข้างต้น
- ไม่เจอ: capture/row ที่ผูก client-emitted post-load frame กับ scene id อย่างเชื่อถือได้

### `pf_bridge/gamedata/`

- ขอบเขต: recursive ทั้ง root, `1,109 files`, `15,319,585 bytes`
- manifest SHA-256: `9ba992357c2e6a7edbd366b996a801d3b354930babf695f35b615251bce3a3ab`
- เจอ: QUEST/Lua ที่เรียก `Player.Teleport*` และ scene/quest destination data
- ไม่เจอ: inbound vital schema, post-load ACK, หรือ client-originated scene-id crosswalk; quest destination เป็น server/game-data intent ไม่ใช่ client-observable confirmation

## Input SHA-256

- `CLIENT_RE_QUEUE.md`: `ec77be09f2e352adbce102936a16be2a2fa09d800aeb5ffd498373c94faeba21`
- `AGENTS.md`: `085e33a261abbb9161a2f58b6ff686152d5893ff40dce038bd6e1520ff4465bf`
- `EVIDENCE_GATES.md`: `b39bf6cee61751ace859311dd33e6f8f0dfe260bd97b3ee571719bcc09bb1044`
- `current/pf_login_game_server_v141.py`: `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
- `src/pirateforce_foundation/runtime.py`: `d590585619b13c34910a2a313b501de83ce3763a9e98d117e20092d20fe9d879`
- `src/pirateforce_foundation/scene_admission_gate.py`: `c1b07cd878999b24a22696038f02f0755ea54db08c7588de67777025bb30a6b1`
- `src/pirateforce_foundation/world_travel_gate.py`: `06ba9ef8e2795eccea547c2664b5f2f9bc1d89220f4acf505c52d3cd81d5de2a`

## Nonclaims

1. ไม่อ้างว่า client ไม่เคยส่ง scene-bearing frame ในโลกจริง; อ้างเพียงว่า committed measured corpus ไม่มีหลักฐานนั้น
2. ไม่อ้างว่า `TeleportVital` R codec คือ emission event
3. ไม่อ้างว่า `TargetPos` พิกัดเดียวกันกับ destination พิสูจน์ scene; coordinate equality ไม่มี scene crosswalk
4. ไม่อ้างว่า `scene_admission_gate.py` ผิด — มันเป็นเกตรับเข้าแถวตาม scope ที่เขียนไว้
5. ไม่อ้าง client-observable outcome; ใบนี้ไม่ได้เปิดเกม

## BUILD_IMPACT

`BUILD_IMPACT: ANALYSIS-ONLY / NO SOURCE CHANGE.` เกตและเอกสารที่อ่าน `selected.position.scene_id`, `runtime_ack_sent`, หรือ post-teleport `TargetPos` ต้องเรียกสิ่งนั้นว่า **server-intended scene / proxy**, ไม่ใช่ client-confirmed rendered scene. อย่าเพิ่ม hard gate ที่อ้าง client confirmation จนกว่าจะมี attended capture/crosswalk ใหม่; งานวันนี้เดินต่อได้เพราะ chief ระบุช่องว่างนี้ไม่ใช่ blocker

## Closeout input drift

หลังปิด jobs มี background sync เพิ่ม `external/pf_build_v5_manifest.py` เวลา `11:13:35+07:00` (SHA-256 `d70e3fc5f853f6bb3286d5e71a7209f5e150ce3e71674b6a7848658418e8f82e`). ค้นเฉพาะ delta แล้วไม่มี `TargetPos/Teleport/scene-id/runtime_ack` หรือคำของ RE-157; คำตอบไม่เปลี่ยน. Final external root = `131 files`, `37,138,668 bytes`, manifest `4368a319d5b4a48c4ce6d62ac03a29630598e27b87d5f167e1b397870bf00478`
