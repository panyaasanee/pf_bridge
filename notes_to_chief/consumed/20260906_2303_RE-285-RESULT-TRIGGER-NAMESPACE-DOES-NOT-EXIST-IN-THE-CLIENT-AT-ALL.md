[ถึง: LANE-Q | ADDRESSEE: LANE-Q | cc: chief, COO | จาก: RE runner บนเครื่อง Panya | 2026-09-06T23:03+07:00]

# RE-285 RESULT — ทั้ง namespace `Trigger` **ไม่มีอยู่ในไคลเอนต์เลย** ⇒ `GetContactMode` ตอบจากอิมเมจไม่ได้ (ตลอดกาล ไม่ใช่แค่รอบนี้)

**สถานะ: CLOSED / BOUNDED-NEGATIVE ทั้งสองเส้นทาง (static-on-bridge + client-image) · checkpoint = method ceiling — ห้าม rerun อิมเมจเดิมกับคำถามนี้**

**คำตอบหนึ่งบรรทัด:** ชื่อเมธอด `Trigger.*` 16 จาก 17 ตัว (รวม `GetContactMode`) **ไม่ปรากฏเป็นสตริงใด ๆ ในอิมเมจ 14.7 MB** และ **ป้ายชื่อ namespace `Trigger` เองก็ไม่มี** ทั้งที่ namespace อื่นครบทุกตัว ⇒ `Trigger` เป็น API ของ **Lua host ฝั่งเซิร์ฟเวอร์** ไม่ใช่ของไคลเอนต์ ⇒ ความหมายของ "contact mode" ไม่มีต้นฉบับให้ลอกในไบนารีนี้ — สายเราต้อง**นิยามเอง**

- START `2026-09-06T22:52:31+07:00` (รอบเดียวกับ `RE-280`, ใบที่สองของรอบ) · ผลเสร็จ `2026-09-06T23:03+07:00`
- ทุก input read-only · ไม่เปิดเกม ไม่จับ `LOCK_GAME`

## input + SHA (ตรวจก่อน/หลังงาน ตรงกัน)

| ไฟล์ | sha256 |
|---|---|
| `GameClient/GameClient.local.bin` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `gamedata/PF_GAMEDATA_LUA_API.tsv` (129+ แถว API) | `21dfa905a67154765f6cdc9c508220ff01441abb7e16f8285901746a62530b73` |
| `gamedata/lua/t_popmo_ui1.lua` (call site เดียวของใบ) | `971ac1f6ed9f8555f5b15e4358ff4ed3637dc2ef1832fb76480bdd5891eebb0b` |

## เส้นทางที่ 1 `[STATIC-ON-BRIDGE]` — ตรวจแล้ว: ว่าง (ตรงกับที่ใบคาด)

`gamedata/PF_GAMEDATA_LUA_API.tsv:160`:
```
Trigger.GetContactMode  Trigger  GetContactMode  1 1 1 1 1 num 1 1 t_popmo_ui1.lua
  binding_status=UNRESOLVED  delegate_va=(ว่าง)  registration_va=(ว่าง)
  binding_note="no NUL-delimited string, or no push<nameVA> + mov[esp+X],delegate pattern found"
```
`gamedata/PF_LUA_API_SPEC.md:202` มีแค่ arity/return shape ไม่มี provenance · **ค้น `external/` แล้ว: ไม่เจอ** (`grep -rIl "GetContactMode" external/` = 0 hit) · **ค้น `gamedata/` แล้ว: เจอเฉพาะ 3 จุดที่ใบอ้างไว้แล้ว** (`lua/t_popmo_ui1.lua:8`, `PF_GAMEDATA_LUA_API.tsv:160`, `_LUA_meta.json:153`) ไม่มี semantics ที่ไหน

## เส้นทางที่ 2 `[NEEDS-CLIENT-IMAGE]` — เดินแล้ว และมันปิดกว้างกว่าที่ใบเดา

### 2.1 ค้นสตริงดิบทั้งอิมเมจ

`GetContactMode` = **0 hit** · `ContactMode` = **0 hit** · `SetContactMode` = **0 hit** (ค้นทั้งไฟล์ 14,759,424 ไบต์ ไม่จำกัด section)

### 2.2 ทำสำมะโนทั้งตาราง API เพื่อพิสูจน์ว่าวิธีค้นเชื่อถือได้ (ไม่ใช่ผลลบเพราะค้นผิดวิธี)

ทดสอบด้วย **สตริงคั่น NUL แบบ exact** (`\0<ชื่อ>\0` — รูปแบบที่ตาราง registration ของ Lua ใช้จริงในอิมเมจนี้):

| namespace | เมธอดในตาราง | เจอสตริงในอิมเมจ |
|---|---|---|
| Guild | 8 | **8** |
| Party | 11 | **11** |
| Instance | 9 | 8 |
| Mob | 10 | 9 |
| Quest | 25 | 23 |
| Player | 73 | 63 |
| Scene | 7 | 5 |
| **Trigger** | **17** | **1** |

ตัวเดียวที่ "เจอ" ของ Trigger คือ `CastSkillXYZ` ที่ `0x00F0E23C` — **แต่มันไม่ใช่ของ Trigger**: มันอยู่ในบล็อกสตริงต่อเนื่อง `0x00F0E200..0x00F0E664` ที่มี `GetItemNum`, `ShowMessage`, `MobAppear`, `ResetMarker`, `Warp`, `Teleport`, ... **แล้วปิดท้ายด้วยป้ายชื่อ `Player`** ⇒ เป็นตารางลงทะเบียนของ namespace `Player` (ตรงกับที่ TSV ให้สถานะ `CastSkillXYZ` = `STUB_NOOP`)

### 2.3 หลักฐานปิด: ป้ายชื่อ namespace

| namespace | ป้ายชื่อ (สตริงคั่น NUL) |
|---|---|
| Player | `0x00F0E664` |
| Quest | `0x00F32264` |
| Guild | `0x00F39100` |
| Party | `0x00F347E8` |
| Mob | `0x00F0D60C` |
| Scene | `0x00F313BC` |
| Instance | `0x00F312F0` |
| **Trigger** | **ไม่มีในอิมเมจ** |

(สตริงที่ขึ้นต้นด้วย `Trigger` ที่มีอยู่คือ `TriggerModule_C...` `0x00F0F5EC`, `TriggerVital` `0x00F317CC`, `TriggerResult`, `TriggerCastSkillVital`, `TriggerSyncVital`, `TriggerMessageVital`, `TurnTrigger`, RTTI `.?AVTriggerStatus@@` — **เป็นคลาส/ข้อความเน็ตเวิร์กของระบบ trigger ไม่ใช่ชื่อ Lua API**)

⇒ **สรุปเส้นทางที่ 2: ไม่ใช่แค่ `GetContactMode` ที่หาไม่เจอ — ไคลเอนต์บิลด์นี้ไม่เคยลงทะเบียน namespace `Trigger` ให้ Lua เลย**

## แปลว่าอะไรสำหรับ LANE-Q (ข้อเสนอ ไม่ใช่คำสั่ง)

1. `lua_api/trigger.py` ทั้งไฟล์ **ไม่มีต้นฉบับฝั่งไคลเอนต์ให้เทียบ** — สคริปต์ `.lua` ของฉากรันบน Lua host ของ **เซิร์ฟเวอร์เดิม** ซึ่งเราไม่มีไบนารี ⇒ ทุก `Trigger.*` เป็นสิ่งที่สายเรานิยามเอง แล้วพิสูจน์ด้วยพฤติกรรมบนจอ ไม่ใช่ด้วย RE
2. เฉพาะ `GetContactMode(22)`: ข้อสังเกตของใบที่ว่า `22` เป็น literal ไม่ใช่ `Trigger.VarN` **ยังยืนอยู่** และตอนนี้แข็งขึ้น — เพราะไม่มีสัญญา ABI ฝั่งไคลเอนต์มาบังคับรูปแบบ argument เลย สายเราจึงเลือกความหมายได้ตามที่ทำให้สคริปต์ 616 ไฟล์ทำงานถูก
3. ทางที่เหลือที่ยังไม่ตัน (ไม่ใช่ RE): (ก) เดินคลัง `.lua` ทั้ง 616 ไฟล์หา `Trigger.*` ตัวอื่นที่รับ literal คล้ายกัน เพื่ออนุมานว่า argument คือ trigger id หรือ mode id · (ข) `.tgr` ของฉาก (ที่ `RE-273` เปิดทางไว้) มีคอลัมน์ต่อ trigger ที่อาจเป็น "contact mode" อยู่แล้ว — **ตรวจตารางนั้นน่าจะได้คำตอบเร็วกว่า attended** · ทั้งสองข้อเป็นงานอ่านข้อมูล ไม่ใช่งานอิมเมจ ⇒ ทำบนคลาวด์ได้ ไม่ต้องรอ RE runner
4. บล็อก `ATTENDED:` ของใบยังใช้ได้ตามเดิม แต่ **ไม่จำเป็นต่อการปลดบล็อกอีกต่อไป**ถ้าสายเรานิยาม semantics เอง

## nonclaims

1. ไม่อ้างว่าไคลเอนต์ "ไม่รู้จัก trigger" — ระบบ trigger มีจริงในไคลเอนต์ (`TriggerVital`, `TriggerStatus`, `TriggerModule`) · สิ่งที่ไม่มีคือ **สะพาน Lua ชื่อ `Trigger.*`**
2. ไม่อ้างว่าเซิร์ฟเวอร์เดิมนิยาม contact mode ว่าอะไร — พิสูจน์ได้แค่ว่า **ไม่ได้อยู่ในไคลเอนต์**
3. ผลลบนี้มีขอบเขต = การค้นสตริง (ดิบ + คั่น NUL) ทั้งไฟล์ · ถ้าชื่อถูกเก็บแบบเข้ารหัส/บีบอัด/ประกอบขึ้นตอนรัน การค้นแบบนี้จะพลาด — **แต่หลักฐานค้าน**คือ namespace อื่นทั้ง 7 ตัวเก็บชื่อเป็นสตริงธรรมดาทั้งหมด (129 เมธอดเจอ 122) ⇒ บิลด์นี้ไม่ได้ซ่อนชื่อ
4. ไม่ได้ใช้ linear disassembler เป็นหลักฐานผลลบ (ผลลบนี้มาจากการค้นสตริง + สำมะโนเปรียบเทียบ ไม่ใช่การเดินโค้ด)
5. ไม่ได้แตะ/แก้ไฟล์ใด ๆ ใน `GameClient/`, `external/`, `gamedata/`, `SERVER/` หรือไฟล์คิว

## BUILD_IMPACT

ไม่มีการแก้โค้ด · ผลคือ **ปลดข้อสมมติ**: หยุดรอ RE สำหรับ `Trigger.*` ทั้งตระกูล (17 เมธอด รวมตัวที่มี call count สูงอย่าง `NextStatus` 353 ครั้ง / `GetTriggerStatus` 134 ครั้ง) — ไม่มีคำตอบให้ขุดจากไคลเอนต์ ⇒ ประหยัดรอบ RE ในอนาคตทั้งหมดที่จะเปิดใบถามชื่อ `Trigger.*` ตัวอื่น
