# gamedata: whitelist พร้อมแล้ว + สเปก API เซิร์ฟเวอร์ 160 ชื่อจาก Lua

**ผู้เขียน:** ผู้ช่วย (cloud) · **ถึง:** chief (cc) และ Panya
**คำสั่ง Panya 2026-08-24 ~01:0x:** "ทั้งสามพร้อมกัน" (① whitelist · ② สเปก API · ③ ปม GT-050)
ฉบับนี้ครอบ ① กับ ② · ③ อยู่ในจดหมายคู่กัน `..._RE055-DRAFT-...`

---

## ① `gamedata\lua\` + `gamedata\scene\` — กวาดตรวจแล้ว whitelist แล้ว เหลือ commit

### ผลกวาดตรวจ (616 `.lua` + 289 `.placements.tsv` ทุกไฟล์ ไม่ได้สุ่ม)

| สิ่งที่ค้น | พบ |
|---|---:|
| absolute path ของเครื่องเดิม (`C:\...`) | **0** |
| UNC path (`\\server\...`) | **0** |
| email | **0** |
| URL / ftp / www | **0** |
| IPv4 | **0** |
| คำว่า password / passwd / pwd / secret / apikey / token / serial / licence | **0** |
| hex blob ยาว ≥32 ตัวอักษร | **0** |
| ไซต์เรียก `dofile` / `loadfile` / `require` / `io.open` / `os.execute` | **0** |

หมายเหตุ encoding: อ่านผ่านทั้ง 616 ไฟล์ — utf-8 279 · cp874 118 · ที่เหลือ 219 ไฟล์มีไบต์ที่ทั้ง cp874 และ tis-620
ไม่รับ จึงต้อง fall back เป็น cp1252 **(ยังไม่รู้ว่าไฟล์กลุ่มนี้เข้ารหัสด้วยอะไรจริง — จดเป็นคำถามเปิด ไม่ใช่ปัญหาของ whitelist**
เพราะการกวาดทำที่ระดับไบต์/ASCII ครบทุกไฟล์อยู่แล้ว)

`pf_decode_lua_npc.py` ตรวจแยกอีกรอบตามคำเตือนของจดหมาย 20:39 (766 บรรทัด):
**ไม่มี byte guard ฝัง ไม่มี hex literal ยาว** มีแค่ magic `$pcz` กับ regex ข้อความ ⇒ ปลอดภัยที่จะ whitelist

### `.gitignore` — เติมแล้ว (6,349 → 7,638 bytes)

```
!/gamedata/PF_GAMEDATA_LUA_INDEX.tsv
!/gamedata/PF_GAMEDATA_SCENE_INDEX.tsv
!/gamedata/pf_decode_lua_npc.py
!/gamedata/pf_lua_api_census.py
!/gamedata/PF_GAMEDATA_LUA_API.tsv
!/gamedata/PF_LUA_API_SPEC.md
!/gamedata/lua/
/gamedata/lua/**
!/gamedata/lua/**/
!/gamedata/lua/**/*.lua
!/gamedata/scene/
/gamedata/scene/**
!/gamedata/scene/**/
!/gamedata/scene/**/*.placements.tsv
```

🔴 **ท่าล็อกรูปทรง:** re-ignore ทุกอย่างใต้ `lua/` และ `scene/` ก่อน แล้วค่อยเปิดเฉพาะ *ไดเรกทอรี* กับ `*.lua` / `*.placements.tsv`
⇒ ไฟล์ `.bin` `.dec` `.bak` `.log` ที่หลงเข้ามาภายหลัง **เข้า git ไม่ได้** โดยไม่ต้องแก้อะไรเพิ่ม

🔴 **ทดสอบแล้วก่อนเขียนลงไฟล์จริง:** ผู้ช่วยรัน `git check-ignore` กับ mock tree ที่จำลองโครงเดียวกัน (มีทั้งไฟล์ที่ควรผ่าน
และไฟล์ล่อ 6 ตัวที่ควรถูกบล็อก) — ผลตรงเป้าทุกไฟล์ · **ผู้ช่วยไม่ได้รันคำสั่ง git ใด ๆ บนเครื่องสะพาน** (กฎยืน)

---

## ② `PF_LUA_API_SPEC.md` — พื้นผิว API ของเซิร์ฟเวอร์ 160 ชื่อ

ไฟล์ใหม่: `gamedata\PF_GAMEDATA_LUA_API.tsv` (160 แถว) + `gamedata\PF_LUA_API_SPEC.md` (ฉบับอ่านด้วยตา)
ตัวสร้าง: `gamedata\pf_lua_api_census.py` (รันซ้ำได้)

### 🔴 re-derive อิสระผ่านแล้ว

`pf_decode_lua_npc.py` (Codex) กับ `pf_lua_api_census.py` (ผู้ช่วย) เป็นคนละโค้ด คนละท่า mask comment/string
ได้ผลตรงกันทุกตัว:

| | Codex | ผู้ช่วย |
|---|---:|---:|
| ชื่อ API | 160 | 160 |
| จุดเรียกรวม | 12,653 | 12,653 |
| `Player` / `Quest` / `Mob` / `Trigger` | 6,423 / 3,721 / 1,189 / 828 | เท่ากันทุกตัว |
| `Scene` / `Instance` / `Guild` / `Party` | 377 / 55 / 37 / 23 | เท่ากันทุกตัว |
| call site ที่วงเล็บไม่สมดุล | — | 0 |

ของที่ตารางผู้ช่วยเพิ่มมาจากของ Codex: **arity (ต่ำสุด/สูงสุด/ที่พบบ่อยสุด)** · **รูปพารามิเตอร์จากไซต์เรียกจริง**
(`var|bool`, `var|num`, …) · **จำนวนรูปที่ต่างกัน** · **จำนวนไฟล์ที่เรียก** · ตัวอย่างไฟล์

### 🔴 ผลลบที่สำคัญที่สุด: **0 / 160**

ค้นชื่อทั้ง 160 ตัวใน `src\` `tools\` `tests\` `docs\` ของ `Pirate Force ServerProject` — **ไม่พบแม้แต่ชื่อเดียว**
⇒ **ชั้นสคริปต์ทั้งชั้นยังไม่ถูกสร้าง** เซิร์ฟเวอร์ปัจจุบันทำงานที่ชั้น wire/DB (actor · inventory · scene load · loot ·
hypothesis modules) ยังไม่มีชั้นที่สคริปต์เควสต์เรียกได้เลย
(นี่ไม่ใช่คำตำหนิ — เป็นแผนที่ว่ายังขาดอะไร และเพิ่งจะรู้ได้วันนี้เพราะเพิ่งถอด Lua ออกมา)

### 15 ตัวที่ถูกเรียกมากที่สุด = ลำดับความสำคัญโดยพฤตินัย

| API | จุดเรียก | arity | รูปพารามิเตอร์บ่อยสุด |
|---|---:|---|---|
| `Player.MobAppear` | 3,532 | 2 | `var\|bool` |
| `Player.AddItem` | 1,430 | 2 | `var\|var` |
| `Quest.RewardItemSelect` | 1,335 | 2 | `var\|var` |
| `Mob.ShowAnimation` | 716 | 1 | `var` |
| `Quest.GetQuestFlag` | 508 | 1 | `var` |
| `Quest.SetFlag` | 417 | 1 | `var` |
| `Mob.AddBuff` | 411 | 2 | `var\|num` |
| `Player.RemoveItem` | 367 | 2 | `var\|var` |
| `Trigger.NextStatus` | 353 | 0 | — |
| `Player.CheckItemNum` | 211 | 2 | `var\|var` |
| `Scene.PlacementOFF` | 173 | 1 | `num` |
| `Quest.AddCriteriaExp` | 166 | 0 | — |
| `Quest.AddCriteriaSkillPoint` | 166 | 0 | — |
| `Quest.AddCriteriaCash` | 165 | 0 | — |
| `Quest.CheckMobKillCount` | 138 | 2 | `var\|var` |

🔴 **`Scene.PlacementOFF(num)` 173 จุด** — สคริปต์ปิด placement ด้วย **เลข index ตรง ๆ** ⇒ ต่อตรงกับเลน
placement/identity ที่ GT-053 เพิ่งปิด (`Bg0002` 106 placement · band `0x2000+idx+1`) · เป็นสะพานระหว่างสองเลนที่ยังไม่มีใครเดิน

### nonclaims (อยู่ท้ายเอกสารสเปกด้วย)
- นี่คือสิ่งที่สคริปต์ *เรียก* ไม่ใช่สิ่งที่เซิร์ฟเวอร์ต้นฉบับ *ทำ* — เซิร์ฟเวอร์ต้นฉบับปิดไปแล้ว กู้ไม่ได้ตลอดกาล
- arity/รูปพารามิเตอร์มาจาก **ไซต์เรียก ไม่ใช่ signature** ⇒ ไม่ได้บอกว่าฟังก์ชันรับอะไรได้บ้าง
- `var` = "ตัวระบุ" ไม่ได้แปลว่า integer — เป็นการจัดกลุ่มทางไวยากรณ์ ไม่ใช่ชนิดข้อมูล
- **ความหมายของแต่ละฟังก์ชันยังไม่ได้พิสูจน์** ชื่อชวนให้เดา แต่ชื่อไม่ใช่หลักฐาน (บทเรียน GT-044)
- จำนวนครั้ง = ความถี่ในซอร์ส **ไม่ใช่ความถี่ตอนรัน**
- ไม่ได้พิสูจน์ว่าไคลเอนต์รันสคริปต์เหล่านี้จริงทุกไฟล์

---

## สิ่งที่ chief ควรทำต่อ

1. รอ commit ของ `gamedata\` (Panya จะสั่ง Codex) แล้ว `gamedata\lua\` `scene\` `PF_LUA_API_SPEC.md` จะอ่านได้จาก cloud
2. 🔴 **อย่าเพิ่งเปิดใบ "implement API ตัวนั้นตัวนี้"** — 0/160 ไม่ได้แปลว่าต้องทำครบ 160
   ลำดับที่ข้อมูลบอกเองคือ `Player.MobAppear` (3,532) มาก่อนทุกอย่างอย่างขาดลอย
3. `Scene.PlacementOFF` เชื่อมเลน Lua กับเลน placement ที่ GT-053 เพิ่งปิด — ใบเชื่อมสองเลนนี้น่าจะคุ้มที่สุดใบถัดไป
