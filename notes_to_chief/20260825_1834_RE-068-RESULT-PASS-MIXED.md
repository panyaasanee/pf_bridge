ถึง chief — ผล RE-068 ACTOR-NAMEBOARD-VALUE-034-SEMANTICS-001 (STATIC-ON-BRIDGE)

# สรุปคำตัดสิน

**PASS-MIXED — ปิด objective ทั้งสองข้อ; ส่วนที่ตันเป็น bounded negative ที่วัดเพดานแล้ว**

1. `board+0x34` ในกราฟนี้ **ไม่ใช่สีและไม่ใช่ฟิลด์ของ runtime NPC actor** แต่เป็นค่าคงเหลือของช่วงรอลบตัวละครบนหน้าสร้างตัวละคร: `character-record+0xF4 - app-singleton+0x7BC` แล้ว setter เก็บผลลง board field `+0x34` ก่อนส่งให้ widget sink
2. `FONT_COLOR 0x005491B0` ถูกเรียกจาก resource-initialization chain เท่านั้นในกราฟที่ resolve ได้: vtable `0x00F238F8` slot `+0x18` → `0x0054AF40` → `0x0054A8D0` → call site `0x0054ADDF` → loader `0x005491B0` → สร้าง RGB object → UI-manager virtual `+0x70` ผล bool ของ wrapper ถูก normalize แล้ว caller เดียว **ไม่อ่านผล**
3. ไม่พบ crosswalk จาก `FONT_COLOR.n_ID` ไป property id `0x34` หรือ `0x5D..0x62` ในกราฟที่ตรวจ ดังนั้น **ห้าม join** ครึ่ง actor กับครึ่ง item ด้วยเลขที่บังเอิญคล้ายกัน

# ด่านควบคุม / ขอบเขต

- static ล้วน: ไม่เปิด server, ไม่เปิด GameClient, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่ใช้ network
- image: `GameClient.local.bin` ขนาด `14,759,424 B`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- T0 `re067_static_verify.py`: `54/54` guards ผ่าน, exit 0
- control เพิ่มเติม `pf_ui_state_refresh_static.py`: `292/292` guards ผ่าน, exit 0
- verifier ใบนี้: `pf_bridge/staged/re068_static_verify.py`, SHA-256 `5c97efbdb7a2519a4bc4f42cb2999ba8f6de88cee43357abe393c60e20382e07`, `46/46` guards ผ่าน, exit 0

# ค้นสองที่ก่อนถอด (ช่องบังคับ)

- **ค้นใน `pf_bridge/external/` แล้ว:** เจอ `GSCN_RunTimeProtocolRes` handler `0x005E4060` และ `SelectActorVital` handler `0x005EFC40` ใน `PF_PROTOCOL_REGISTRY.tsv` เมื่อค้น VA ของ writer; **ไม่เจอ** semantic row ที่ตั้งชื่อ `FONT_COLOR` หรือ `NameBoard` โดยตรงในไฟล์ข้อความ `.tsv/.md/.txt` ใต้ external
- **ค้น gamedata แล้ว:** เจอ `FONT_COLOR` 57 แถว (`n_ID` 1..57 พร้อม `f_RED/f_GREEN/f_BLUE`), `VEHICLE.s_NAMEBOARD`, `NAMEBOARD_RANGE_*`, และ `NAMEBOARD_PERCENT_*`; **ไม่เจอ** crosswalk จากแถวเหล่านี้ไป countdown field หรือ item property `0x34/0x5D..0x62`

# T1 — ความหมายและ writer ของ `object+0xF4`

ที่ `0x004B9C7D..0x004B9C96` มีสายตรง:

`record+0xF4` → ลบ `[0x1093198]+0x7BC` → push ผล → call `0x005BBCE0`

alias ที่พิสูจน์ได้จาก character-select collection ชี้ว่า `record+0xF4` เป็นค่า deadline/countdown ของสถานะ pending-delete ใน record ของตัวละคร ไม่ใช่ฟิลด์ของ runtime NPC actor ตัว writer ที่ผูก alias นี้ได้คือ `cStateCreateActor::OnDeleteResult 0x004BAEB0`, instruction `0x004BAFDD`, ซึ่งเขียน argument จาก `DeleteActorVital field+0x18` เข้า `record+0xF4` เมื่อ status field `+0x14` เป็น 3 หรือ 4

การค้น displacement `+0xF4` ทั้งอิมเมจมี hit ของโครงสร้างอื่นด้วย จึง **ไม่ join ด้วย offset อย่างเดียว**; คำว่า “writer เดียว” ด้านบนจำกัดเฉพาะ alias ของ character-select collection ที่ control 292/292 pin ไว้

# T2 — `0x1093198` และ field `+0x7BC`

- `[0x1093198]` เป็น process-wide app singleton; startup `0x0040AE70` allocate `0x948` bytes, เรียก ctor `0x0040AAD0`, แล้ว publish pointer ที่ `0x0040B152`
- ctor ติด vtable `0x00F09FD0` และ zero `this+0x7BC` ที่ `0x0040AC22`
- writer census ของ literal displacement `+0x7BC` ใน executable sections พบครบ 3 จุด:
  - `0x0040AC22`: ctor ตั้ง 0
  - `0x005E40F7`: `GSCN_RunTimeProtocolRes` คัดลอก `[message+0x24]+0x10`
  - `0x005EFC7A`: `SelectActorVital` คัดลอก `message+0x14`
- จากการถูกใช้เป็นตัวลบออกจาก pending-delete value พิสูจน์ได้ระดับโครงสร้างว่าเป็น **app-wide countdown reference/baseline**; exact epoch, หน่วยเวลา, และชื่อดั้งเดิมยังพิสูจน์ไม่ได้

# T3 — setter / sink / consumer

- `0x005BBCE0` เก็บ argument ลง `board+0x34` แล้วเรียก `0x00A97BD0`
- sink `0x00A97BD0` clamp เป็น `max(value, 0)`, เก็บลง `receiver+0x220`, แล้วเรียก method จาก receiver vtable slot `+0x240`
- จุด `virtual +0x240` เป็นเพดาน static ของ sink นี้: sink มี direct callers หลายชนิดและไม่มีหลักฐาน alias พอเลือก concrete receiver/vtable สำหรับ call ของ NameBoard โดยไม่เดา
- consumer ที่เห็นจากอีกด้านใน `NameBoardNPC::update 0x005BD8E0` อ่าน `board+0x34`, เปรียบกับค่าปัจจุบันของ widget แล้วส่งเข้า `LABEL_NAME` virtual slot `+0x13C`

# T4 — ผู้เรียก `FONT_COLOR` และการใช้ผล

- loader `0x005491B0` มี rel32 caller เดียว `0x0054ADDF`
- caller อยู่ท้าย wrapper `0x0054A8D0`; wrapper `test al` / `setne al` และ return bool
- wrapper มี rel32 caller เดียว `0x0054B24C` ภายใน `0x0054AF40`; instruction ถัดไปคือ `mov ecx, esi` / call `0x00548050` — ไม่มี test/move/push ของค่า `AL`, จึงพิสูจน์ว่า caller เดียวทิ้งผล bool
- `0x0054AF40` ถูกอ้างจาก vtable `0x00F238F8 + 0x18 = 0x00F23910`; ชื่อ concrete class ไม่ได้ resolve จากหลักฐานที่มี
- ภายใน loader: เปิดตาราง `FONT_COLOR`, อ่าน `f_RED/f_GREEN/f_BLUE`, allocate `0x1A0`, ctor `0x00ABC790`, normalize RGB ด้วยค่าคงที่ `/255`, เรียก `0x00511230`, แล้วส่ง object เข้า UI-manager virtual slot `+0x70`

# T5 — สะพาน property id

- item literal table ของ RE-067 ยัง pin เป็น `[0, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62, 0x63]` ที่ `0x00F30EC4`
- ใน resolved graph รวม `0x005491B0`, `0x0054A8D0`, `0x0054AF40` ไม่พบ direct ref ไป `0x00F30EC4`, item property setter `0x005BACF0`, board setter `0x005BBCE0`, หรือ `NameBoardNPC::update 0x005BD8E0`
- `FONT_COLOR.n_ID` มีช่วง 1..57; item property ids มีค่า 93..98; และ `board+0x34` เป็น **field displacement** ไม่ใช่ property id `0x34` — ตัวเลขทั้งสามอยู่คนละ namespace/role

# Recursive-CFG evidence

ทุกแถวใช้ image SHA ข้างต้น และ `DECODE_ERRORS=0`

| body | span | file off | len | instructions | gap | indirect jumps | span SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| app startup | `[0x0040AE70,0x0040B277)` | `0x0000A270` | 1031 | 250 | 0 | 0 | `b543e03e752471b32ce84ad89d2eabb2d9bd722a2eea7d3ba74151551aefd0d8` |
| app ctor | `[0x0040AAD0,0x0040ACDF)` | `0x00009ED0` | 527 | 116 | 0 | 0 | `f8e7671b8d7180d433d67dd7553975d6e882f1aa2645b74ee2b5229009f09aa1` |
| character-slot rebuild | `[0x004B9980,0x004B9D38)` | `0x000B8D80` | 952 | 252 | 7 | 0 | `4f0cf85e29761a4c65d1d5d4c427d2b12deec487dfad7e4e14e2a4e5df423eac` |
| OnDeleteResult | `[0x004BAEB0,0x004BB5E0)` | `0x000BA2B0` | 1840 | 403 | 81 | 1 | `3ddb1f98bbae5d3ba35dacd70dade6ad34dfd574927f0b86cfd869d0840b745c` |
| GSCN handler | `[0x005E4060,0x005E41CD)` | `0x001E3460` | 365 | 119 | 0 | 0 | `85ff71ffceff5345f94facc9b7fa1c39c8efd2e429248d112cdba578d3df944e` |
| SelectActor handler | `[0x005EFC40,0x005EFD48)` | `0x001EF040` | 264 | 80 | 0 | 0 | `ce5b10218fa2d8edaa6de670ff7881eff03e186e34e2883fb0c89dc36926f300` |
| board setter | `[0x005BBCE0,0x005BBD26)` | `0x001BB0E0` | 70 | 22 | 0 | 0 | `c1af02f4eb37f23de478dc628c22787c65d143d13ea84b82013ce034d88bd111` |
| property sink | `[0x00A97BD0,0x00A97BF1)` | `0x00696FD0` | 33 | 11 | 0 | 0 | `4c475681a3c05eb5413dd140532ea89f568f361cb7db0df3ad465e7f7e2cf92d` |
| NameBoardNPC update | `[0x005BD8E0,0x005BDF20)` | `0x001BCCE0` | 1600 | 503 | 0 | 0 | `e5a09bce53d19c44bed8679dd2437a953bdee14d226dafe8133848240b523c2c` |
| FONT_COLOR loader | `[0x005491B0,0x005494FE)` | `0x001485B0` | 846 | 246 | 7 | 0 | `8820cd4127879901e582e2f47e7c30511bdcc668ee8520516ff4401d24fff3ea` |
| loader wrapper | `[0x0054A8D0,0x0054ADEE)` | `0x00149CD0` | 1310 | 360 | 0 | 0 | `4a874071302e5bc02a83bbf4234536bfb4cd05bc7ad19a3c504e752b0bdaf98a` |
| resource initializer | `[0x0054AF40,0x0054B285)` | `0x0014A340` | 837 | 303 | 0 | 0 | `117b5d26db0a3453acb884f98f0d88fdf7b8ccd2af4ffbd7cdc392a8286b5a67` |

# Integrity / nonclaims

- source image before/after SHA ตรงกัน: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `CLIENT_RE_QUEUE.md` ยัง SHA `4bb5f19fdd1e53114e429e8e103f8d080ca1d03ea809edb8cd8c11f514db31aa`; `AGENTS.md` ยัง SHA `25082302097d6c5f351b59d50062013a5f92998334876faa197345117b0ffca6`
- `external/ + gamedata/` snapshot ก่อน/หลังยัง 1,138 files, 45,154,691 bytes; ไม่มี source write ในรอบนี้
- ไม่อ้างชื่อฟิลด์ดั้งเดิม, exact time unit/epoch, concrete target ของ virtual `+0x240`/`+0x70`, runtime behavior, หรือสิ่งใดเกี่ยวกับ original server
- ผล “ไม่พบ crosswalk” จำกัดที่ image SHA ข้างต้น, recursive graph ของสาม body ที่ระบุ, item literal table, และ local `external/gamedata` snapshot นี้; **ไม่เท่ากับยืนยันว่า crosswalk ไม่มีในทุกแหล่ง**

ข้อเสนอ: ไม่ควรรัน RE-068 ซ้ำแบบเดิม เพราะ static ceiling ถูกวัดแล้ว หากต้องการ exact time unit/epoch หรือ concrete virtual target ให้ chief เปิดใบใหม่แบบเจาะ receiver/vtable โดยเฉพาะ
