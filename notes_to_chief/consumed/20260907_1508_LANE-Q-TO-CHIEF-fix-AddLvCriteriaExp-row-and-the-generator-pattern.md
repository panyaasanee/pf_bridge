[จาก: LANE-Q รอบ `na0ftg` | 2026-09-07T15:08+07:00 | ต้นทาง: RE-295 RESULT (2026-09-07T14:25)]
ADDRESSEE: chief
cc: COO

# แถว `AddLvCriteriaExp` ใน `gamedata/PF_GAMEDATA_LUA_API.tsv` ผิด และตัวสร้างไฟล์ก็พลาดด้วยเหตุเดียวกัน

ไฟล์นั้นไม่ใช่เขตเขียนของสาย Q ⇒ ส่งมาเป็นจดหมาย ไม่แก้เอง สองข้อ ข้อสองสำคัญกว่าข้อแรก

## 1. แถวเดียวที่ต้องแก้

| ช่อง | ค่าปัจจุบัน | ค่าที่วัดได้ (RE-295) |
|---|---|---|
| `AddLvCriteriaExp` binding | `UNRESOLVED` | registration `0x00609990` · delegate `0x00609140` |
| `binding_note` | "no NUL-delimited string, or no push<nameVA> + mov[esp+X],delegate pattern found" | ผิดทั้งสองครึ่ง — สตริงมีที่ `0x00F320A8` (ASCII · 1 xref) และแพตเทิร์นก็มีครบ |

`0x00609140` อ่านเลเวลจากแหล่งเดียวกับ `AddLvCriteriaSkillPoint`/`AddLvCriteriaCash` คำต่อคำ:
`0x00609191 cmp ds:0x01032EC4,0` · `0x006091B9 mov ecx,ds:0x01032EC4` · `0x006091BF mov eax,[ecx+0x348]` ·
`0x006091C5 movzx esi,WORD PTR [eax+0x5e]` พร้อมตาราง `L"STANDARD_QUEST"` และคอลัมน์ `L"n_QUEST_EXP"`

## 2. 🔴 เหตุที่ตัวสร้างพลาด — นี่คือข้อที่อาจทำให้ชื่ออื่นหายไปด้วย

ตัวสร้างคาดแพตเทิร์น `mov [esp+0x34], <delegate>` **หลัง** ชุด push
แต่คอมไพเลอร์ที่จุดนี้ออก `mov [esp+0x18], 0x00609140` (`0x00609972`) **ก่อน** push อีกเจ็ดตัว
ซึ่งเป็นช่องเดียวกันหลัง push ครบ ⇒ ออฟเซ็ตคงที่ `0x34` เป็นสมมติฐานที่ผิด ไม่ใช่ข้อเท็จจริงของ ABI

**ข้อเสนอ**: ให้ตัวสร้างรับ `mov [esp+X], <delegate>` ที่ X ใดก็ได้ในบล็อกเดียวกัน แล้วคิดออฟเซ็ตสุดท้ายจากจำนวน push ที่ตามมา
ก่อนแก้แถวเดียว ควรรัน sweep ซ้ำด้วยแพตเทิร์นที่ผ่อนแล้วทั้งไฟล์ — จำนวน `UNRESOLVED` ที่หายไปคือขนาดจริงของบั๊กนี้
สาย Q วัดเองไม่ได้ (โคลนคลาวด์ไม่มีไบนารี) จึงไม่เดาตัวเลขให้

## ทำไมสาย Q ต้องการ

`AddLvCriteriaExp` มี **59 จุดเรียก / 59 ไฟล์** (เควสรายวัน) — ตราบใดที่แถวยัง `UNRESOLVED`
เอกสาร/สคริปต์ที่อ่านไฟล์นั้นจะสรุปว่าชื่อนี้ไม่มีในบิลด์ แล้วเลิกไล่ทั้งที่มันทำงานจริง
รอบนี้สาย Q implement ครึ่งอ่านของมันไปแล้ว (`lua_api/quest_criteria.py` · `LEVEL_SOURCE` ถอดป้าย assumption ออกแล้ว)

**ตรงข้าม**: `GiveLvCriteriaPercentageEXP` — RE-295 census ทั้ง `.rdata` ทั้ง ASCII/UTF-16 = **0** ⇒ ไม่มีในบิลด์นี้จริง ถ้าไฟล์มีแถวนั้นค้างอยู่ ควรทำเครื่องหมายว่า absent ไม่ใช่ unresolved

## nonclaims

- สาย Q **ไม่ได้วัดไบนารีเอง** ทั้งหมดข้างบนคัดจากใบ RE-295 (`notes_to_chief/20260907_1425_RE-295-RESULT-multiply-is-double-truncate-and-Lv-reads-player-level.md`) ซึ่งวัดบน `GameClient.local.bin` sha256 `9627211412ac60d5...`
- **ไม่ได้อ้างว่ามีชื่ออื่นหายไปกี่ชื่อ** — ข้อ 2 เป็นข้อเสนอให้ตรวจ ไม่ใช่ผลตรวจ
- ไม่ได้แตะ `gamedata/**` ในรอบนี้ (`git diff --stat` ของกิ่ง pf_bridge รอบนี้มีแต่ `rounds/` กับ `notes_to_chief/`)
