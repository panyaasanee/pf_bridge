[ถึง: chief cloud · LANE-A (WORLD) · COO | จาก: RE runner local · 2026-08-28T09:13:28.786+07:00]

# RE-123 RESULT — DONE / MIXED-POSITIVE-BOUNDED: Mirage reel คือ `n_ID=230`; client placement/Lua ไม่ได้สร้างตัวนี้

## สถานะ

ปิด `T0-T4` แบบ static-only ตามเกณฑ์ใบ `BG0002-MIRAGE-REEL-QUEST-SPAWN-CROSSWALK-001`:

- **positive:** identity ปิดได้เป็น `MOBS/TIP n_ID=230` ด้วย named-field crosswalk สองเควสต์ใน scene 2
- **positive:** ไม่ใช่แถว placement ใน `Bg0002` และไม่ใช่ client-side Lua spawn; การส่ง actor/population เป็นความรับผิดชอบฝั่ง server
- **bounded:** current static corpus ไม่มี authoritative XYZ และไม่มี lifecycle trigger/visibility rule ที่บอกว่าต้องส่งเสมอหรือส่งเมื่อ quest state ใด

ticket START `2026-08-28T09:09:23.565+07:00` · jobs `T0-T4`

## T0 — input control + ช่องค้นบังคับ

ค้นใน `pf_bridge\external\` แล้ว: **ไม่เจอ** `Mirage`, `MobAppear`, `q_movie_con4` หรือชื่อ spawn/call-mob ที่ผูกกับใบนี้ในทั้งชุด 30 files / 29,900,221 bytes. ขอบเขตเป็น deterministic path/size/SHA manifest SHA-256 `3b742370873829347ec7827e610c96e8091b0400fde70ceae9965c6f3664e811`. ผลลบนี้หมายถึงชุด client-binary deliverable ไม่มี semantic crosswalk ของ NPC ใบนี้ ไม่ได้หมายความว่า client ไม่มี actor codec ทั่วไป.

ค้น `pf_bridge\gamedata\` แล้ว: **เจอ** candidate ชื่อ `Mirage reel` 19 n_ID, quest data/text/talk, Lua `Q_MOVIE_CON4`/`Q_CON_NEW`, Lua API binding และ scene placements. ทั้งชุด 1,109 files / 15,319,585 bytes; deterministic path/size/SHA manifest SHA-256 `e8e44669b2e7b7b06a8722be9c622ee988ab5c169a4b170ad8956751d9428e5b`.

SHA pins สำคัญ:

- image `GameClient.local.bin` = `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `QUESTDATA_TH__QUEST.tsv` = `cc9927286def2bda166c320a2dddd16f5457eb4579ce5207a3d76758707527bd`
- `QUESTDATA_TH__QUESTTALK.tsv` = `e6f8cb7ac3245cb28ecc711269aadb731459018a077622316f49e2bd079f421e`
- `QUESTTEXT_TH__TEXT_QUEST.tsv` = `e192903071cfba24f882fd120dd230e512b068b67bb956316ffce871b53bb427`
- `CONSTDATA_TH__MOBS.tsv` = `3c0d33d68f832eefda56c845495008338dcef56f4277584b9ca479b7e1b3916b`
- `TEXTDATA_TH__MOBS_TIP.tsv` = `e25ac667c9029e07752fbfd5d13b548d2e62ea439936884f30187c0c553ce38f`
- `PF_GAMEDATA_LUA_API.tsv` = `21dfa905a67154765f6cdc9c508220ff01441abb7e16f8285901746a62530b73`
- `q_movie_con4.lua` / `q_con_new.lua` = `d91b3f7537dbd2ca7fc793ad32f99830eea3d76897531935d80915ab5ac459c2` / `c32123b06bac443d26c8c70adb14ec5941276d75b52a6111deac0be446bfe697`
- `Bg0002.placements.tsv` = `e57841a7018b46ff50d31972e5ba0846612548288446fe8514d819a99be92f8f`
- current `scene2_prison_exile_tables.py` = `44df3aeabb4260c457ecb6f4ef4d9785da65e014957633120a15572f8aca6fa3`
- queue / AGENTS / NEW_ORDERS = `ee3b0eb59dba48fa08c5f7b91a731c4ea643402c0290f745a4ef2535272a9cab` / `8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3` / `a19efcb410a23614d8af4106f7d712bb314a5edbbf1b3df793227c3bf811fc5c`

## T1 — identity/crosswalk: `n_ID=230`

`TEXTDATA_TH__MOBS_TIP.tsv` มีชื่อ `Mirage reel` 19 n_ID ตาม candidate set ของใบจริง. การเลือก `230` ไม่ได้มาจากชื่อซ้ำหรือเลขเท่ากัน แต่จาก named fields ต่อไปนี้:

1. `QUESTTEXT_TH__TEXT_QUEST.tsv:52`, row `n_ID=51`, ชื่อเควสต์ `การติดต่อจากคุก`, ช่อง briefing อ้าง `<text ... path="230">[52500230]</text>` โดยตรง.
2. `QUESTDATA_TH__QUEST.tsv:31`, row 51 มี `n_SCENE=2`, `s_LUASCRIPT=Q_MOVIE_CON4`.
3. `CONSTDATA_TH__MOBS.tsv:226`, row `n_ID=230`, มี `s_QUEST_END=51;86;3167;3241` และ `s_QUEST_BEGIN=749;926;3167;3241`.
4. join candidate `MOBS.s_QUEST_BEGIN/END -> QUEST.n_ID -> QUEST.n_SCENE` ทั้งหมดแล้ว มีเพียง `n_ID=230` ที่ผูก scene 2: `END quest 51` และ `BEGIN quest 926`; candidate อีก 18 ตัวไม่มี scene-2 quest link แบบนี้.
5. `QUESTDATA_TH__QUEST.tsv:708`, quest 926 มี `n_SCENE=2`, `s_LUASCRIPT=Q_CON_NEW`; `QUESTTEXT_TH__TEXT_QUEST.tsv:926` ชื่อ `คำเตือนจาก Warden`. เป็น cross-check อิสระอีกทิศจาก quest 51.

ดังนั้น identity สำหรับ NPC/quest object ที่เจ้าของเรียก “Mirage Reel” ใน Prison Exile คือ **`MOBS/TIP n_ID=230`**.

## T2 — placement boundary

- `Bg0002.placements.tsv` 106 rows มี template-id crosswalk จริงในคอลัมน์ `template_ids`; **ไม่มี 230**.
- scan `*.placements.tsv` ทุกฉากที่ extract ไว้แล้วก็ **ไม่มี template 230** เช่นกัน.
- Mo Yuzi anchor มีจริงที่ Bg0002 index 67, `template_ids=39`, XYZ `(-10690.4873046875, -4295.1767578125, 5658.3505859375)`. คำว่า “ยืนข้าง” จากภาพไม่ได้ให้ offset/XYZ ของ 230 จึงห้ามยืมพิกัด 39 หรือแต่งจุดข้างเต็นท์.
- current `scene2_prison_exile_tables.py` pin แหล่งเดิม 106 placements / 97 known / 9 unresolved และไม่มี row 230; source/test SHA ไม่ขยับ.

ผล: ห้ามเพิ่ม 230 เข้า placement-derived `KNOWN_PLACEMENTS` เพราะไม่มี placement row/crosswalk ให้ทำอย่างนั้น.

## T3 — Lua/spawn mechanism

- Quest 51 และ 926 มี `n_VARI_13..20 = 0` ทุกช่อง.
- `q_movie_con4.lua:26-32,78-84` และ `q_con_new.lua:425-442,742-759` เรียก `Player.MobAppear` ได้เฉพาะเมื่อ `Quest.Var13..20 > 0`; สอง quest นี้จึงไม่ส่ง 230 เข้า call ดังกล่าว.
- scan `QUESTDATA_TH__QUEST.tsv` ทั้งตาราง: ไม่มี candidate 19 ตัวอยู่ใน `n_VARI_1..20` ของ quest scene 2 เลย และไม่มี candidate ใดอยู่ใน MobAppear slots `n_VARI_13..20` ของ quest ใดทั้งตาราง.
- สคริปต์ทั้งสองไม่มี `Mob.CallMob`.
- `PF_GAMEDATA_LUA_API.tsv:2` ผูก `Player.MobAppear` เป็น `STUB_NOOP` ที่ VA `0x0045FA00`; verify image จริงได้ body ครบ `33 c0 c2 04 00` (`xor eax,eax; ret 4`). ดังนั้นแม้ quest อื่นมีค่า nonzero client body นี้ก็ไม่สร้าง actor/send/wait เอง.

ข้อสรุประดับกลไก: actor 230 ต้องมาจาก **server-owned actor population/census** ไม่ใช่ client placement และไม่ใช่ Lua ที่สร้าง actor local. แต่ quest association 51/926 เพียงอย่างเดียวไม่ได้พิสูจน์ว่า server เดิมเปิด/ปิด actor 230 ที่ state ใด; `n_MOB_APPEAR=1` ก็ใช้เป็นตัวชี้ไม่ได้ เพราะเป็นค่าของ 2,960/3,210 MOBS rows (92%).

## T4 — BUILD_IMPACT / static ceiling

`BUILD_IMPACT: ไม่มี source patch จากใบนี้ — hard guard` เพราะ identity ปิดได้ แต่ authoritative XYZ และ visibility/lifecycle policy ยังไม่ปิด. LANE-A สามารถแยก mental model ได้แล้วว่า 230 ต้องอยู่ใน **server-owned quest/service-NPC population** คนละแหล่งกับ placement-derived 97-row census; ห้ามเพิ่ม static row 230 ใน `scene2_prison_exile_tables.py`, ห้ามใช้ XYZ ของ Mo Yuzi และห้ามตีความ quest 51/926 ว่าเป็น trigger โดยไม่มี field เพิ่ม. ถ้าเจ้าของให้ exact XYZ/visibility policy หรือมี original-server actor capture แล้ว ค่อยเปิด BUILD/RE ใบใหม่เพื่อส่ง actor_type 4 n_ID 230 ผ่าน census path ที่มีอยู่.

`BUILD_IMPACT_NONE: 1/1` — เหตุผลคือข้อมูลที่ขาดเป็นพิกัดและ policy ไม่ใช่ encoder/path ฝั่ง server.

## verifier / reproducibility

- `staged/re123_mirage_quest_static.py` SHA-256 `b3b5105767dc66a162d14585ecf041935acf2a9ec825c36ede6d5b0d1f8d4bcc`
- PASS 35 checks / 14 pinned files สองครั้งติดกัน; assertions ครอบ candidate set, named quest links, all-scene placement absence, all-quest VAR absence, Lua API binding และ image bytes ที่ `0x0045FA00`.
- existing `tests/test_scene2_prison_exile_tables.py`: `17 passed`.
- SHA หลังงานของ image/queue/AGENTS/orders/tables/Lua/placement/server source ตรงก่อนงานทุกตัวที่ระบุด้านบน.

## nonclaims

1. ไม่อ้างว่า 230 ต้องปรากฏตลอดเวลา หรือปรากฏเฉพาะเมื่อ quest 51/926 active; static corpus นี้ไม่ให้ trigger policy.
2. ไม่อ้าง XYZ ของ 230 จากภาพ “ข้าง Mo Yuzi” และไม่ใช้พิกัด 39 แทน.
3. ไม่อ้างว่า `n_MOB_APPEAR=1` แปลว่า quest-spawn; มันเป็นค่าปกติของ 92% ตาราง.
4. ไม่อ้างว่าตาราง client บอกพฤติกรรม original server; ข้อสรุป server-owned จำกัดแค่ว่า client placement/Lua paths ที่ตรวจไม่ผลิต actor นี้ จึงต้องมี actor จากฝั่งเครือข่ายหากจะ render.
5. ผลลบจำกัดที่ exact named-field joins, 19-candidate scan, all extracted placement TSVs, all quest VAR columns, two pinned Lua scripts และ exact client no-op body; ไม่ใช้ linear disassembler/string absence เป็นหลักฐานผลลบ.
6. ไม่มีเกม/server boot, ไม่มี capture ใหม่, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, source, queue, external หรือ gamedata.
