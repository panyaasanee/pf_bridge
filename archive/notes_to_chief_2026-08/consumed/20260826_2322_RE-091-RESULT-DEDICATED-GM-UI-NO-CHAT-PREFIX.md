[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-091 RESULT — PASS/DONE: `0x51E9` มาจาก dedicated GM UI; ไม่มี prefix branch ใน main chat

- เวลา: `2026-08-26T23:22+07:00`
- ใบ: `RE-091 CHEAT-CHAT-TRIGGER-001 [STATIC-ON-BRIDGE]`
- verdict: **PASS/DONE — objective เดิมเป็น false dichotomy**: ไคลเอนต์ไม่ได้ตรวจ prefix ของข้อความใน main chat แล้วสลับไป `GM_RunGMCommandVital`; อิมเมจมีช่อง editor ของ GM UI โดยเฉพาะที่สร้าง `GM_RunGMCommandVital` เมื่อกด Enter บนข้อความไม่ว่าง ขณะที่ main chat ใช้ตระกูล `Channel_*MessageVital` แยกต่างหาก
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ source/queue/git
- ImageBase ของ VA ทุกจุดด้านล่าง: `0x00400000`

## ค้นสองที่ก่อนถอด (บังคับ)

- **ค้นใน `pf_bridge/external/` แล้ว:** เจอ `PF_PROTOCOL_REGISTRY.tsv` พิน `GM_RunGMCommandVital`: id global `0x01088F8C`, getter `0x00726DE0`, vtable `0x00F45A20`, serializer `0x00729E10`, handler/default `0x00A106C0`; เจอ serializer layout จาก `RE-088` และ `PF_FIELD_VALIDATION.tsv` ยังเป็น `NOT_OBSERVED`/0 frame ทั้ง W/R — **ไม่เจอ semantic trigger/prefix** ใน external
- **ค้น gamedata แล้ว:** ค้นทั้ง tree ด้วย `GM_RunGMCommandVital`, `RunGMCommand`, `0x51E9`, `20969`, `0x01088F8C`, `GMCommandArg`, `GMUI1`, `cheat`, `prefix` — **ไม่เจอ trigger/crosswalk ที่เกี่ยวข้อง**; พบเพียงข้อความ/แถวเครื่องมือ GM หรือคำว่า “Cheat” ที่เป็น lexical hit คนละข้อมูล จึงไม่ join หรืออ้างเป็นหลักฐานของใบนี้

## T0 — xref global `0x01088F8C`

byte-level literal census ใน PE ทั้งไฟล์พบ dword นี้ **2 จุดเท่านั้น** และยืนยัน instruction boundary แยกจาก overlapping decode:

1. read: `0x00726DE0  mov ax, word ptr [0x01088F8C] ; ret` — id getter (7 bytes)
2. write: registrar `[0x00C07EA0,0x00C07EB8)`: resolve ชื่อที่ `0x00F463A4` แล้ว `0x00C07EB1  mov word ptr [0x01088F8C], ax ; ret`

ดังนั้น global xref เองเป็น registration/getter ไม่ใช่ chat trigger; ตอนส่งจริง id ถูกเรียกผ่าน virtual getter ใน vtable ของ vital

## T1 — จุดที่ text ไปเป็น `0x51E9`

### shared GM sender

- `[0x00728200,0x007282A2)` sha256 `28716062a95830c8f7d197c83ef8f7b943a8ab667a3c2541b4fd259aa1011a82`; recursive CFG `162/162` bytes, gap `0`
- `0x0072823C` ขอ object `GM_RunGMCommandVital` จาก pool `0x00727EB0`
- `0x0072825D` ใส่ `GMCommandArg*` ที่ vital `+0x14`
- `0x0072826E` wrap แล้ว `0x00728275 -> 0x005DD800` ส่งออก
- byte-level direct-call census พบผู้เรียก `0x00728200` สองจุด: `0x00729380` (GM tool/panel producer) และ `0x0072953B` (GM text editor producer); ไม่พบ absolute pointer/table xref ของ sender นี้

### GM text editor producer — ไม่มี prefix branch

- `[0x00729410,0x0072957D)` sha256 `c777ccc6a223889e1d1e4aa85eeedc54ebe1df24d2ca4a9adbea6b3064717a81`; recursive CFG **365/365 bytes, gap 0**
- gates ที่เห็นครบทั้งฟังก์ชัน: input/context มีอยู่, editor/widget มีอยู่และ active/visible, event code ที่ `0x00729480` เท่ากับ `0x0D` (Enter), และ wstring ไม่ว่างที่ `0x007294A1`
- `0x007294C0` allocate `GMCommandArg`; `0x007294E4` assign **wstring ทั้งก้อน** เข้า argument `+0x1C`; `0x007294FC` set kind `0x20`; `0x00729514` หา `GMModule_Client`; `0x0072951A` type-check; `0x0072953B` ส่งผ่าน shared sender
- ใน CFG ครบทั้ง 365 bytes ไม่มี compare ของอักษร prefix แบบ `/` (`0x2F`) หรือ prefix-like candidates และไม่มี substring/erase ระหว่างดึงข้อความกับ assign ทั้งก้อน

### แยกจาก main chat และขอบเขต GM state

- หลักฐานเดิม `reports/PF_CHAT_ECHO004_LOCALTALK_HANDLER_STATIC_20260818.md` (sha256 `d046413d90abe299e8eb3a5c61b1bd25a15e91aaf88c64a7ca7c94deb590ba07`) พิน normal local chat เป็น `Channel_LocalTalkMessageVital` (`0xAC52`) สอง wstring และ dynamic dispatch; ไม่ใช่ wrapper `0x00728200`
- `GM_UpdateGMStateVital` handler `[0x00729F00,0x00729F5D)` sha256 `89b9c320510c7aa61fe92a2bf41c8b761661db2cf8ccd467ca098ca554689e46`, CFG `93/93`, เรียก `0x00727AB0` ซึ่งเขียน GM module `+0x18/+0x19/+0x1C`
- GM editor sender ไม่อ่านสาม field นี้โดยตรง; สิ่งที่พินได้ในใบนี้คือ sender อยู่หลัง dedicated GM UI/widget gates ไม่ใช่ prefix ของ main chat ส่วนความหมาย `is_gm`/level และวิธีเปิด UI เป็นขอบเขต `RE-089` ไม่ claim ข้ามใบ

## T2 rider — prefix/strip

- **ไม่มี prefix บนเส้น text→`0x51E9` ที่วัดได้**
- จึงไม่มีอักษรให้ระบุและไม่มี strip operation; ข้อความถูก assign เป็น wstring ทั้งก้อนเข้า `GMCommandArg+0x1C`
- คำตอบไม่ใช่ “ทุก main-chat string ถูกส่งให้เซิร์ฟเวอร์ตีความ”; normal chat กับ dedicated GM editor เป็นคนละ producer/คนละ vital ตั้งแต่ต้น

## Reproducer / verifier

`pf_bridge/staged/re091_cheat_chat_trigger_static.py`

- script sha256: `c2067b311d9d721896809767c9ee030eb5b0408bce02c2422c91a074322d6407`
- รัน `py -3 -B` สองครั้ง: PASS เหมือนกัน
- พิน CFG เต็ม gap 0: `0x00728200`, `0x007282B0`, `0x007286E0`, `0x00729410`, `0x00729F00`
- ไม่ใช้ linear disassembler เป็นหลักฐานของผลลบ; ข้อสรุป prefix มาจาก recursive CFG เต็มของ producer text และ exact whole-string data flow

## Integrity / provenance

| input | sha256 ก่อน | sha256 หลัง |
|---|---|---|
| `GameClient/GameClient.local.bin` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `external/PF_PROTOCOL_REGISTRY.tsv` | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` |
| `external/PF_SERIALIZER_FIELDS.tsv` | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` |
| `external/PF_FIELD_VALIDATION.tsv` | `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3` | `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3` |

หมายเหตุ concurrent sync: ระหว่างรอบ `CLIENT_RE_QUEUE.md` เปลี่ยนจาก sha ก่อนรอบ `3b7762d8c6574e9abfcd699de6858dc2555c4fd98b55d440c92b28b3ba943800` เป็น `0571614a66eb1570e5466a67c3eee9cd0b0f46c5584617cc5749ccf6362af41a` (`mtime 23:06:04+07`); อ่านทั้งไฟล์ใหม่แล้ว `RE-091` ยัง OPEN/PENDING, เนื้อ objective/jobs/nonclaims ข้างต้นไม่เปลี่ยน และไม่มีผล RE-091 ทั้ง root/consumed. `NEW_ORDERS` บอกเฉพาะ `GAME_TEST_QUEUE.md`/R182 attended และ RE-092 closure ไม่ได้เปลี่ยนลำดับงาน RE นี้

## nonclaims

1. ไม่ได้นิยาม command set/authorization policy ของเซิร์ฟเวอร์ (`GM-003`)
2. ไม่ claim ว่า UI นี้เข้าถึงได้ใน runtime โดยผู้เล่นทั่วไป หรือ `GM_UpdateGMStateVital` field ใดคือ is_gm/level — เป็น `RE-089`
3. ไม่ claim capture/runtime observation; external validation ของ `0x51E9` ยัง `NOT_OBSERVED`
4. ไม่ใช้ lexical gamedata hit, id เท่ากัน, หรือ normal-chat evidence ไป join เป็น trigger โดยไม่มี crosswalk

## BUILD_IMPACT

**BUILD_IMPACT:** อย่าจำลอง original client ด้วยการดัก `/` ใน main chat แล้วเปลี่ยนเป็น `0x51E9`; ให้รักษา normal chat (`Channel_*MessageVital`) แยกจาก privileged GM-command lane หากจะรองรับ UI/โปรโตคอลเดิม ให้เปิด dedicated GM editor หลัง authorization/state gate, ส่งข้อความทั้งก้อนใน `GMCommandArg` แล้วสร้าง `GM_RunGMCommandVital`. การตีความคำสั่งจากข้อความแชทธรรมดาที่ server ปัจจุบันทำอยู่เป็น **project policy/design** ไม่ใช่พฤติกรรม original client ที่ใบนี้พิสูจน์

