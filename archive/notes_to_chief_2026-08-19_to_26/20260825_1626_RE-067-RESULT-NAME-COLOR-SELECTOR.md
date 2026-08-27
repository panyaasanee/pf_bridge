ถึง: chief (cloud)

# RE-067 RESULT — NAME-COLOR-SOURCE-001

- เวลา: `2026-08-25T16:26:03+07:00`
- สถานะ: **PASS / MIXED — item selector pinned; actor concrete graph bounded-negative**
- วิธี: static-only บนอิมเมจอ่านอย่างเดียว; ไม่เปิด GameClient/server, ไม่จับ `LOCK_GAME`, ไม่อ่านหรือแตะ canonical DB
- verifier ที่เพิ่มในเขต local writer: `pf_bridge/staged/re067_static_verify.py`
- verifier SHA-256: `838c70efb759caa3be4473fbd84f51fdadffa4d2455552fe1e1f5e52a56026e2`
- ผล verifier: `54/54` guards PASS, exit `0`
- actor-type verifier เดิม: `111/111` guards PASS, exit `0`

## สองช่องบังคับ

ค้นใน `pf_bridge/external/` แล้ว: **ไม่เจอ**
`NameColor|name_color|DrawName|NameLabel|HeadName|TitleColor|FontColor|NameBoard` ใน TSV ทั้ง 8 ไฟล์ = `0 hits` (รัน local ซ้ำ ไม่ได้ยกผล cloud อย่างเดียว)

ค้น gamedata แล้ว: **เจอ** `CONSTDATA_TH__FONT_COLOR.tsv` 57 แถว (`n_ID=1..57`, `f_RED/f_GREEN/f_BLUE`) + `CONSTDATA_TH__E_DROPS_QUALITY.tsv` + `EQUIPMENT_BASE.n_QUALITY/s_TAG_EXTRA`; **ไม่เจอ** crosswalk จริงจาก `n_QUALITY` ไป `FONT_COLOR.n_ID`; grep `FONT_COLOR|f_RED|f_GREEN|f_BLUE` ใน `gamedata/lua/` 616 ไฟล์ = `0 hits`.

## Objective — คำตอบสั้น

1. **ชื่อไอเทมบนพื้น:** จุดเลือก UI text property อยู่ใน CREATE ที่ `0x005F47FE..0x005F4822` และ UPDATE ที่ `0x005F4D04..0x005F4D5D`; ทั้งสองส่งค่าผ่าน setter `0x005BACF0` ไปยัง label/widget. ตัวเลือกอ่านจาก element `+0x1B` (gate) และ `+0x1A` (index/fallback), ใช้ตาราง dword `0x00F30EC4` ซึ่ง map `1..6 → 0x5D..0x62`; gate เป็นศูนย์จะใช้ default `0x34`.
2. dirty mask ของ element map `bit 0x08 → +0x1B` และ `bit 0x20 → +0x1A`. mask ปัจจุบัน `0x12 = 0x10|0x02` **อยู่นอกทั้งสอง field** จึง decoder คงค่า ctor `+0x1B=0`, `+0x1A=1` และ CREATE/UPDATE ตก default `0x34`.
3. **ชื่อ actor:** `actor_type=4` เลือกคลาส `CNetNPC` และ `NameBoardNPC`; มันไม่ได้เป็น branch เลือกสีโดยตรงใน concrete update. `NameBoardNPC::update 0x005BD8E0` sync ค่า `board+0x34` เข้า `LABEL_NAME` property (`virtual +0x138/+0x13C`). ในกราฟที่ decode ครบนี้ไม่พบ direct read ของ `NPCAttr faction+0x68`, direct relation comparator `0x004A1D50`, หรือ call ไป loader `FONT_COLOR 0x005491B0`.
4. upstream ที่พบสำหรับ `board+0x34` คือ setter `0x005BBCE0` (caller เดียว `0x004B9C92`) ซึ่งส่งต่อไป `0x00A97BD0`; caller คำนวณจาก `[object+0xF4] - [[0x1093198]+0x7BC]`. **ยังตั้งชื่อความหมายของค่านี้ไม่ได้จากหลักฐาน** และไม่มี crosswalk ไป faction/relation/palette. ดังนั้นครึ่ง actor ปิดแบบ bounded negative เฉพาะกราฟ `actor_type 4 → NameBoardNPC`; ไม่อ้างว่าไม่มีเส้นสีอื่นในทั้งโปรแกรม.

## ผลตามลำดับงาน

### S0 — PASS

- image: `14,759,424 B`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `FULL_ID_ROW [0x00892580,0x00892606)` SHA `1ce8aa30afadc034fcfabadcf2ab67c6bf828fad0e30bf48af68283901c368e7`, recursive CFG errors `0`, gap `0`
- `STRING_FIELD [0x00892050,0x0089207F)` SHA `550c11788729c0b64e8f27501fc7b31a831d5124abd66f70f2d56eacaac3be69`, errors `0`, gap `0`
- `CREATE [0x005F41E0,0x005F4897)` SHA `d8011e41a99fef62e6c311e804b715b20f3187dc57128276e35b947a7510f105`, errors `0`, gap `0`
- rerun `re066_static_verify.py`: 17 pinned spans ผ่านทั้งหมด.

### S6 — PASS

- `0x0045C560` เป็น allocator wrapper ของ board ขนาด `0xC0`, ไม่ใช่ ctor ตัวจริง; มันเรียก `NameBoardNPC` ctor `0x005BB3A0`.
- ctor ติด final vtable `0x00F2CD48`; slot `+0x14=0x005BE6C0` (bind), slot `+0x1C=0x005BD8E0` (update).
- `NameBoardNPC update [0x005BD8E0,0x005BDF20)` SHA `e5a09bce53d19c44bed8679dd2437a953bdee14d226dafe8133848240b523c2c`, 503 instructions, recursive CFG errors `0`, gap `0`.

### S7 — PASS (แก้ offset จากจุดตั้งต้นของใบ)

`NameBoardNPC bind [0x005BE6C0,0x005BE98E)` SHA `42b3b52404eedfeff604e9ca31dce96979a6d5499afd415f3f432d7db223203c`, errors `0`, gap `0`.

- root `NameBoard_Player` → board `+0x20`
- `HPBAR` → `+0x4C`
- `LABEL_NAME` (`0x00F0C794`) → **`+0x50`** (ไม่ใช่ `+0x54` แบบ `NameBoardPlayer`)
- `LABEL_NICKNAME` → `+0x54`
- `IMG_ARROW_FRIEND` → `+0x58`; `IMG_ARROW_ENEMY` → `+0x5C`
- พบ `LABEL_GUILD`, `IMAGE_HPBAR`, `GRID_BASE` ใน bind graph ด้วย.

### S8 — BOUNDED NEGATIVE

- factory `[0x00446990,0x00446B2C)` SHA `5f68239f8661419da2ea9bea4e4a2cb9bcdcaa37fe6e4cd53b701116aeeb697d`; actor-type verifier ยืนยัน byte `record+0x10`, type `2..6`, และ type `4 → CNetNPC`.
- actor_type แยก **คลาส board** (Player/NPC) ได้จริง แต่ concrete `NameBoardNPC` update ไม่อ่าน actor_type ซ้ำเป็นตัวเลือกสี และไม่อ่าน faction/relation โดยตรง.
- `board+0x34 setter [0x005BBCE0,0x005BBD26)` SHA `c1af02f4eb37f23de478dc628c22787c65d143d13ea84b82013ce034d88bd111`, errors `0`; direct caller เดียว `0x004B9C92` ใน `[0x004B9980,0x004B9D38)` SHA `4f0cf85e29761a4c65d1d5d4c427d2b12deec487dfad7e4e14e2a4e5df423eac`, errors `0`, padding gap `7`.
- sink `[0x00A97BD0,0x00A97BF1)` SHA `4c475681a3c05eb5413dd140532ea89f568f361cb7db0df3ad465e7f7e2cf92d`, errors `0`.
- ขอบเขตผลลบ: direct/recursive-decodable graph ของฟังก์ชันที่ระบุบนอิมเมจ SHA นี้เท่านั้น; indirect virtual consumers นอกกราฟยังไม่ถูกตัดทิ้ง.

### S5 — PASS / loader found, no crosswalk

- exact UTF-16 literals: `FONT_COLOR @0x00F23680`, `f_RED @0x00F23674`, `f_GREEN @0x00F23664`, `f_BLUE @0x00F23654`; แต่ละ literal มี `.text` reference หนึ่งจุด (`0x00549203/39/51/70`).
- loader `[0x005491B0,0x005494FE)` SHA `8820cd4127879901e582e2f47e7c30511bdcc668ee8520516ff4401d24fff3ea`, recursive CFG errors `0`, padding gap `7`; direct rel32 caller เดียว `0x0054ADDF`.
- loader นี้อ่าน RGB จริง แต่ concrete item selector และ `NameBoardNPC` update ข้างบนไม่ call มันโดยตรง.
- map ของ item selector คือ `0x5D..0x62` ขณะที่ `FONT_COLOR.n_ID` มีเพียง `1..57`; **ห้าม join เพราะเลขเหมือน/ดูคล้าย** และไม่มี crosswalk field จริง.
- nonclaim ของ S5: พิสูจน์ได้ว่ามี loader และไม่อยู่ใน concrete graph ที่ตรวจ; ไม่ได้พิสูจน์ว่า `FONT_COLOR` ไม่มี generic/indirect consumer ที่อื่น.

### S1 / S2 — PASS

- CREATE ได้ชื่อจาก item row แล้วเขียน text ก่อน; การเลือก property แยกอยู่ที่ `0x005F47FE`.
- `cmp byte [element+0x1B],0`; ศูนย์ → `push 0x34`.
- ไม่เป็นศูนย์ → ใช้ signed element `+0x1A`, รับเฉพาะ `1..6`, lookup `dword [index*4+0xF30EC4]`.
- setter `[0x005BACF0,0x005BAD1A)` SHA `f0cf5aabea9ff56e1f2f0a692cab9df0511eb0d7cf3e5a991643e8db26738a3a`, errors `0`; direct callers มีเพียง `0x005F4822`, `0x005F4D12`, `0x005F4D5D`.
- element allocator/ctor `[0x005F82C0,0x005F83F9)` SHA `d13db4d5abbccf0879a600b6d76de19a15b7958610f4f28c2c53ae5fcda26ae6`, errors `0`; defaults `+0x1B=0`, `+0x1A=1`.

### S4 — PASS; H1 แยกได้

`UPDATE [0x005F4C00,0x005F4DEE)` SHA `7b14d16ca60fc6917328cc9a59f8c8f7ab6e13052eac3764c69dae45d41c06c2`, errors `0`, gap `0`.

- `s_TAG_EXTRA @0x005F4CC9` เข้าทาง format text เท่านั้น ไม่ได้ป้อน selector table โดยตรง.
- `0x005F4D04` gate element `+0x1B`; ศูนย์ → default `0x34`.
- gate ไม่ศูนย์ → เริ่มจาก signed element `+0x1A`; เมื่อ fallback >0 จึง query `n_QUALITY`, และใช้ `n_QUALITY` override เฉพาะ query สำเร็จและค่า >0; จากนั้นรับ `1..6` แล้ว map `0xF30EC4`, นอกช่วง → `0x34`.
- ดังนั้น H1 ถูกบางส่วนอย่างมีเงื่อนไข: `n_QUALITY` ขับ UI property ใน UPDATE ได้ แต่ต้องผ่าน element `+0x1B` ก่อน; traffic ที่เราส่งไม่เคยเดิน update และ mask ปัจจุบันปล่อย gate เป็นศูนย์.

### S3 — PASS

`LIST_CODEC [0x005F85B0,0x005F8869)` SHA `ce0a58f72c5798f1d5263ebdb5ee449659ed04e2974f63f77657ea968a4f1b5b`, errors `0`, gap `0`.

- bit `0x02` → element `+0x14` dword
- bit `0x04` → `+0x18` u16
- bit `0x08` → `+0x1B` byte (**selector gate**)
- bit `0x10` → `+0x1C` complex/position
- bit `0x20` → `+0x1A` byte (**selector index/fallback**)
- mask `0x12` มี `0x10|0x02`; จึงส่ง position/id แต่ไม่ส่ง gate/index ของ UI property.

## Integrity / เขตเขียน

- จด SHA-256 ก่อนและหลังให้ input ที่พึ่งทั้งหมด 18 ไฟล์ (client image, helper/verifier เดิม, external TSV 8 ไฟล์ + guide, gamedata 4 ไฟล์ + guide, actor tool): **ตรงกันทุกไฟล์**.
- ไม่แก้ `CLIENT_RE_QUEUE.md`, `GAME_TEST_QUEUE.md`, `CHIEF_CONTINUATION.md`, `src/`, `tools/`, `GameClient/`, `external/`, `gamedata/`.
- เขียนเพิ่มเฉพาะ verifier ใน `pf_bridge/staged/`, จดหมายนี้, log และ automation memory; ไม่มี push/force/rebase.

## Nonclaims บังคับ

- สีในตาราง/ภาพเปรียบเทียบเป็นการอ่านด้วยตา **ไม่ได้วัดค่าพิกเซล**; ข้อสรุปที่อาศัยการเทียบเฉดสืบทอดข้อจำกัดนี้.
- ภาพอ้างอิงอาจมาจาก client คนละ build หรือคนละภูมิภาค; รอบ static นี้ยังตัดความเป็นไปได้นั้นไม่ได้.
- ยังไม่มีหลักฐานว่า “ผู้เล่นเขียวเพราะกิลด์เดียวกัน”; ไม่ใช้สมมติฐานนี้ในผล.
- static ไม่ยืนยันว่า runtime เดินเส้นนั้นจริง; `SCENE-013` null prior ยังเป็นความเสี่ยงแยก.
- การพบว่าโค้ด “เปิดอ่านฟิลด์” ไม่เท่ากับพิสูจน์ว่า field นั้น “ตัดสินการวาด”; ผลข้างบนแยก query, selector, setter และ draw-property sink ออกจากกัน.
- เซิร์ฟเวอร์ต้นฉบับปิดและกู้ไม่ได้; ใบนี้สรุปเฉพาะพฤติกรรมที่อ่านได้จาก **ไคลเอนต์ที่ ship มา**. ภาพเก่าแสดงเพียงว่าไคลเอนต์เคยวาดสีอื่นได้ ไม่ได้พิสูจน์ว่าเซิร์ฟเวอร์เดิมส่งอะไร.

## ข้อเสนอใบถัดไป (ไม่เปิดเอง)

ถ้าต้องการชื่อ semantic ของ actor `board+0x34`, ให้ chief เปิดใบแยกติดตาม indirect consumer/virtual `+0x240` หลัง `0x00A97BD0` และ crosswalk ของค่าจาก `[object+0xF4] - global+0x7BC`; รอบนี้หยุดเมื่อ objective ปิดได้ตามเกณฑ์ mixed positive + bounded negative.
