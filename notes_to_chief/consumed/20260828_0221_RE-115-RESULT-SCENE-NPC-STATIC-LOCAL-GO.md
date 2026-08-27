[ถึง: chief cloud (cc), Panya, สาย A · จาก: RE runner LOCAL]

# RE-115 RESULT — map NPC list มาจาก scene `.npc` + client tables; GO ส่ง local NPC id

- status: **DONE (STATIC-ON-BRIDGE; bounded where noted)**
- ticket start: `2026-08-28T02:01:25.798+07:00`
- result time: `2026-08-28T02:21+07:00`
- mode: static only; ไม่เปิด server/GameClient, ไม่จับ `LOCK_GAME.txt`, ไม่อ่าน/แตะ canonical DB

## Verdict

รายการ “NPCs in this scene” ไม่ได้ถูกคัดลอกจาก actor census และไม่พบ packet รายชื่อแยกในหลักฐาน static ที่ตรวจ: client โหลด scene-local file `\.\Data\Scene\Save\<scene>\<model>.npc`, แยก `MOBSET` เป็น record `{NPC id, X, Y}`, แล้วสร้างแถว UI โดย lookup `MOBS`/`MOBS_TIP` ด้วย NPC id ที่มี crosswalk จริงใน record. `MAP_SCENE_LIST` เป็นทางสร้างรายการ scene/world-map อีกชุด ไม่ใช่แหล่ง per-scene NPC rows.

ปุ่ม `GO!` เก็บ NPC id ที่เลือกไว้ใน map object และส่ง local event type `0x14` ที่มี NPC id เท่านั้น; complete CFG ของ click path ไม่มี X/Y และไม่มี network-send call. พิกัดมีอยู่แล้วใน record ที่ client แยกจาก scene `.npc`, จึงเป็น **client-local resolution** ไม่ใช่พิกัดจาก actor census payload หรือ request ใหม่ ณ จุดคลิก.

## T0 — pinned inputs

- `GameClient.local.bin`: size `14,759,424`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `CLIENT_RE_QUEUE.md`: SHA-256 `25977b9ca7905e8d49c8017b5dad66b459b2d6312c1f4dd4e19aaac023f9aef5`
- `AGENTS.md`: SHA-256 `8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3`
- `NEW_ORDERS.txt`: SHA-256 `735b0d27c7deb4bf7d6b8143c019d0744d4b7ab410c7e1ea6987e7c627b25e75`
- verifier: `staged/re115_mapwindow_static.py`, SHA-256 `43df72ae9550b1838590b5da3cbf239df98d57303ab0df2670a0b135db08b30c`; result `PASS failures=0`

## Mandatory search before disassembly

### `external/`

ค้น `MapWindow`, `MAP_SCENE_LIST`, `Main_Map`, `WorldMap`, `BUTTON_START`, `BUTTON_GOTO`, `UpdateNPC`, `SCROLLABLEITEMLIST_NPC` และคำ map/NPC packet ที่เกี่ยวข้องทั่วชุด: **ไม่พบ hit ที่เป็น handler/opcode ของรายการ NPC หรือ GO**. ขอบเขตคือ 30 files, 29,900,221 bytes; manifest fingerprint (sorted `relative<TAB>len<TAB>sha256`) `50c7f6162cdd03845bb9dfdb10620f2692d2c23b571167993a8cd3e60672538f`.

### `gamedata/`

ค้น index/columns/tables ทั้งชุด: 1,109 files, 15,319,585 bytes; manifest fingerprint `9ba992357c2e6a7edbd366b996a801d3b354930babf695f35b615251bce3a3ab`. พบแหล่งที่เกี่ยวข้อง:

- `tables/CONSTDATA_TH__MOBS.tsv`: 3,210 data rows, 54 columns, SHA-256 `3c0d33d68f832eefda56c845495008338dcef56f4277584b9ca479b7e1b3916b`; มี `n_CAPABILITY`, `s_NAME`, `s_TITLE`, `s_ICON`, `s_LOCATION` และ quest fields.
- `tables/CONSTDATA_TH__MAP_SCENE_LIST.tsv`: 15 data rows, 15 columns, SHA-256 `9564867136111fd8655aa40acb14aeaf84b8e586070e7bb78db21841cc6c63b9`; เป็น island/world-map button metadata (`n_MAP_X`, `n_MAP_Y`, `n_NPC_ID`, `s_MAP_NAME`, button assets), ไม่ใช่ per-scene NPC list.
- scene placement corpus มี `.npc`/`MOBSET` data ซึ่งตรงกับ path/parser ใน binary; ไม่จับคู่ด้วยเลขเท่ากันลอย ๆ — crosswalk ที่ใช้คือ NPC id ที่ parser เขียนลง record แล้วส่งเป็น key เข้า `MOBS` lookup โดยตรง.

## T1/T2 — UI และ list source

UI binder span `[0x00524990,0x0052501B)` SHA-256 `b8713c8374222d7d72e72664b227043d67d2ec3b1d2ea85b89c706ee1a7f8b52` bind `BUTTON_START` -> object `+0x34`, `SCROLLABLEITEMLIST_NPC` -> `+0x38`, `LABEL_NPC_SCENE_LIST` -> `+0x3C`. Literals `Main_Map_2`, `Main_NPCList`, `UpdateNPC` pin module/list/update path.

แหล่งสมาชิกของ scene:

1. `[0x0052B010,0x0052B1E7)` SHA-256 `873b9fa05b29683fa746fba1b1c00c86c696cf7ca637d2384213d729947ebc07` ส่ง current scene id และ output collection `object+0x118` เข้า `0x0043A9D0`.
2. `[0x0043A9D0,0x0043AD54)` SHA-256 `36dd3c9ce064ad07924b1efc977e807f821a96fab3c3d042890103a784e9248f` query `SCENE_NAME`, อ่าน `n_CLINE_TYPE`/scene model, และประกอบ path จาก ASCII literals `\.npc`, `\.\Data\Scene\Save\`, `%s\\%s` ก่อนโหลดไฟล์ local.
3. `[0x0043A6F0,0x0043A9C3)` SHA-256 `28ebd3e05d5c05f956dbb7919a882b4c6654bf821637d653d9f32d1c0a266758` เดิน parsed scene records, filter CLINE/MOBSET fields, แล้วเขียน NPC id ที่ record `+0x10` และ X/Y floats ที่ `+0x14/+0x18` ลง collection.
4. list builder `[0x0052A050,0x0052A4E3)` SHA-256 `f2dd34d1c4edba78094122afbadb3dd3bc4b1951b16e29d00127d33bb2d04e33` เดิน collection `+0x118..+0x12C`, ผ่าน local eligibility gate `0x00525910`, require `MOBS.n_CAPABILITY == 1`, สร้าง `Main_NPCList`, เติมชื่อ/title/icon จาก `MOBS/MOBS_TIP`, และเก็บ NPC id จริงที่ item `+0x94`.
5. alternate/new map builder `[0x0052D6E0,0x0052DA83)` SHA-256 `a8eef2621d4d442ab4c92a005b5e7b7c1d896b6fde3ef74e83b3ebc5ddedb1b9` ทำรูปแบบเดียวกันกับ collection `+0x18C..+0x1A0`.

`UpdateNPC` handler ที่ `0x0052AD80` เรียก list builder เดิมอีกครั้ง เป็น local UI refresh; ไม่ได้ decode list payload. ลำดับแถวคือการ iterate container ที่สร้างจาก scene records; รอบนี้ไม่ตั้งชื่อ comparator/sort key เพราะยังไม่ได้ปิด type/comparator ของ container และไม่จำเป็นต่อ verdict ว่าไม่ใช่ packet list.

## T3 — packet/opcode

**Not applicable by positive source identification.** ไม่พบ separate map-NPC-list opcode/handler ใน external scope ข้างต้น และ complete CFG ของ source/UI paths แสดง local file/table path โดยตรง. ผลลบนี้จำกัดอยู่ที่ fingerprint และ CFG spans ที่ระบุ; ไม่ใช้ linear disassembly เป็นหลักฐานการไม่มีทั้ง binary.

## T4 — GO path

- row click callback `0x00525040` copy `item+0x94` -> selected NPC id `map+0x9C`.
- GO path `[0x00526660,0x0052677C)` SHA-256 `45589d94675d2742f0023f2de0a4d64044ef9544ea1360fcb199f680d9d15228` อ่าน `map+0x9C`, ทำ local scene/level gate (`SCENE_NAME` path in `[0x00525E60,0x00525F0B)`, SHA-256 `89a58de52239e4ab6d779f11e45f5ce49bdf8cd73a0e9f326bb4fa334bcfd349`), แล้ว dispatch local event type `0x14` พร้อม NPC id.
- complete GO CFG ส่ง **ไม่มี X/Y** และไม่มี network-send call; X/Y ถูกเก็บไว้แล้วใน local `.npc` record ตาม T2. ข้อสรุปที่รองรับจึงเป็น “GO เริ่มจาก local NPC id และ resolve กับ scene-local data”; รอบนี้ไม่ตั้งชื่อ semantic ของ event `0x14` เกินหลักฐาน.

## Client-observable context (แยกชั้น)

- Port Royal screenshot SHA-256 `500f2a40529d3b3dd27da130a9c5f4a9fbf103d6254d67e4c3c244edc8f5d317` แสดง list + GO.
- Prison Exile screenshot SHA-256 `68ffc53357cd69bf19f7ff824bfdaede3ba60f416954f4e0a5dff27ff5f6dbe3` และ M1P note SHA-256 `d26f76c7c14581a625179738e34296a1a026132de44a352ce6c41c1597888162` แสดง Mirage Reel อยู่ใน list ทั้งที่ไม่เห็นใน census window.

สองข้อนี้เป็น client-observable corroboration เท่านั้น; static path ข้างบนเป็นหลักฐานคนละชั้นและไม่ได้ใช้ screenshot พิสูจน์เหตุภายใน client.

## Nonclaims

- ไม่อ้างว่า server ไม่มี map/actor traffic อื่นนอก scoped functions/fingerprint.
- ไม่อ้างว่า event type `0x14` คือ wire opcode หรือระบุ downstream semantic เกิน local dispatch.
- ไม่อ้าง UI order/comparator ที่ยังไม่ปิด และไม่จับคู่ field ด้วย id เท่ากันเฉย ๆ.
- ไม่อ้างว่า `MAP_SCENE_LIST.n_NPC_ID` เป็น per-scene NPC member; code path แยกกัน.
- ไม่เปิดเกม ไม่เก็บ wire/DB ใหม่ และไม่ใช้ client-observable แทน static proof.

## BUILD_IMPACT

- Server ไม่ควร invent packet รายชื่อ NPC เพื่อทำให้หน้าต่าง M แสดงรายการ; client มี source + display metadata + coordinates อยู่แล้วจาก scene `.npc` และ `MOBS/MOBS_TIP`.
- สิ่งที่ server ต้องรักษาคือ scene identity/transition และ NPC ids ที่ compatible กับ client data; actor census ไม่ต้องครบทุกชื่อเพื่อให้ list แสดง.
- ถ้าจะทำ GO behavior ให้เหมือน client ให้ไล่ต่อจาก local event `0x14`/NPC id โดยรักษา client-local resolution; อย่าส่ง X/Y หรือ list packet เพิ่มโดยไม่มี wire evidence.

