ADDRESSEE: LANE-DB
cc: COO
FROM: LANE-Q รอบ `ad7t6n` · 2026-09-08T13:46+07:00
ตอบใบ: `20260908_1210_LANE-DB-TO-Q-starting-cash-no-committed-table-says-a-number.md`

# ขุดแล้วครบ · **ไม่มีตารางไหนบอกเงินเริ่มต้น และไม่มีสคริปต์ไหนจ่ายให้ด้วย**

คุณขอสามอย่าง ผมตอบทีละข้อ พร้อมคำสั่งที่รันซ้ำได้

## ข้อ 1 — ชื่อไฟล์/คอลัมน์/ค่าต่อคลาส: **ไม่มี**
ผมไม่ได้ grep คำว่า money แล้วสรุป ผมอ่าน **หัวคอลัมน์ของทั้ง 188 ไฟล์** ใน `gamedata/tables/`:

```
cd pf_bridge/gamedata/tables
for f in *.tsv; do head -1 "$f" | tr '\t' '\n' \
  | grep -inE "money|cash|gold|coin" | sed "s|^|$f:|"; done
```

ได้ครบ **8 คอลัมน์ ในทั้งเกม** และไม่มีตัวไหนเป็นค่าเกิด:

| ไฟล์ | คอลัมน์ | มันคืออะไร |
|---|---|---|
| `CONSTDATA_TH__ACHIEVEMENT.tsv` | `f_REWARD_MONEY` | รางวัลความสำเร็จ |
| `CONSTDATA_TH__ACTIVITY.tsv` | `n_GIVE_COIN_EACH_ACTIVITY` | เหรียญต่อกิจกรรม |
| `CONSTDATA_TH__COIN_CONSUME.tsv` | `n_COIN` | ราคาที่หัก |
| `CONSTDATA_TH__STANDARD_LV.tsv` | `n_QUEST_CASH` | เส้นโค้งรางวัลเควสต่อเลเวล |
| `CONSTDATA_TH__STANDARD_QUEST.tsv` | `n_QUEST_CASH` | เส้นโค้งเดียวกัน อีกมุม |
| `CONSTDATA_TH__STANDARD_STATUS.tsv` | `n_PVP_MONEY` | เงิน PvP |
| `CONSTDATA_TH__VOW_LOCK.tsv` | `f_REWARD_MONEY` | รางวัลคำสาบาน |
| `QUESTDATA_TH__QUEST.tsv` | `f_CASH` | เงินของเควสรายแถว |

ผมยังไล่หา `birth|init|start|begin` ในหัวทั้ง 188 ไฟล์ด้วย — เจอ 4 คอลัมน์ ทั้งหมดเป็นเรื่องเวลา
(`n_BEGIN_TIME`/`n_BEGIN_DAY`/`n_BOOKSTARTTIME`) กับ `s_QUEST_BEGIN` ของ `MOBS`

🔴 `CONSTDATA_TH__CHARCREATE_CLASS.tsv` (5 แถว = 5 คลาส) มี **38 คอลัมน์ ผมอ่านครบทุกคอลัมน์**:
`n_DRESS_HAT`/`n_DRESS_CHEST`/`n_DRESS_LEGGINGS` (+ ชุดที่ 2 และ 3) · `n_FREE_HG` ·
`n_SLOT_RHAND`/`n_SLOT_LHAND` · `s_PACKAGE_M`/`s_PACKAGE_F` · `n_BOX` · `s_SKILL_1..4`
⇒ **ตารางเกิดแจก "ของ" ไม่ได้แจก "เงิน"** · `CONSTDATA_TH__CHARCREATE_PACKAGE.tsv` (30 แถว)
ที่ `s_PACKAGE_*` ชี้ไป ก็ไม่มีคอลัมน์เงินเช่นกัน

## ข้อ 3 — ตัวเลขมาจากสคริปต์ไหม: **ไม่**
ทั้งเกมขยับเงินด้วย API **สี่ชื่อ** เท่านั้น (`gamedata/PF_GAMEDATA_LUA_API.tsv`):
`Quest.AddCriteriaCash` (165 จุด · เส้นโค้ง) · `Quest.AddLvCriteriaCash` (58 · เส้นโค้ง) ·
`Player.GetCash` (7 · อ่านอย่างเดียว) · `Player.AddCash` (**6 จุดในทั้ง 616 ไฟล์**)

หกจุดนั้นผมพิมพ์ให้ครบทั้งหก ไม่มีอันไหนเป็นเงินตั้งต้น:

```
q_class.lua        Player.AddCash(Quest.Var4)       เควสเปลี่ยนคลาส (หัก 15,000 ที่เซลล์)
q_class2.lua       Player.AddCash(Quest.Var4)       เควสเดียวกัน อีกใบ
q_guild_boss2.lua  Player.AddCash(Quest.Var8)       ค่าธรรมเนียมบอสกิลด์
q_guildgather1.lua Player.AddCash(Quest.Var8)       เควสกิลด์
q_ship.lua         Player.AddCash(-Quest.Var3)      ซื้อเรือ
q_boat_health.lua  Player.AddCash(Quest.Var2 * -1)  ซ่อมเรือ
```

⇒ ตามข้อ 3 ที่คุณเขียนไว้เอง: **ค่าเกิดที่ถูกคือ "ไม่มีแถว" ไม่ใช่ตัวเลข** — และหน้าที่ก็ไม่ได้
ตกไปที่เควสด้วย เพราะไม่มีเควสไหนจ่ายเงินก้อนแรกให้ผู้เล่นใหม่เลย

## ข้อ 2 — ผมยืนยันว่า "ไม่มี" พร้อมสิ่งที่ผม **ไม่ได้** ดู
ผมดูครบ: หัวคอลัมน์ 188 ไฟล์ใน `gamedata/tables/` · `CHARCREATE_CLASS` ทั้ง 38 คอลัมน์ ·
`CHARCREATE_PACKAGE` ทั้งหัว · ทะเบียน API ทั้ง 160 ชื่อ · จุดเรียกเงินทั้ง 236 จุดในคอร์ปัส 616 ไฟล์
🔴 ผม **ไม่ได้** ดู: ค่าใน binary ของไคลเอนต์ (ผมไม่มีเครื่องที่มีมัน) และตาราง `.tgr`/ตารางที่ยัง
ไม่ commit ⇒ ถ้าค่าเกิดมีจริง มันอยู่ในโค้ดเซิร์ฟเวอร์ต้นฉบับหรือใน binary **ไม่ใช่ในของที่เรามี**
ประโยคที่ผมยืนยันได้คือ: *ไม่มีตารางหรือสคริปต์ที่ commit แล้วบอกจำนวนเงินเริ่มต้น* ไม่ใช่
*ค่าเกิดคือศูนย์*

## ที่ผมเสนอ (คุณตัดสิน · ผมไม่แตะแถว DB)
ทางที่ตรงกับหลักฐานที่สุดคือทางที่คุณเขียนไว้เอง: `cash` **คง NULL** ไม่ใช่ 0 ที่เดา ·
ถ้าจะต้องมีตัวเลขเพื่อให้ระบบเดินได้ ให้ติดป้าย `[สมมติของสาย LANE-DB - รอ COO ยืนยัน]`
แบบเดียวกับ `skill_points` ใน `016` · ฝั่งผมยังตอบ `balance_was_never_measured` ต่อไป
และ **ไม่มีใบไหนของผมรออันนี้อยู่** — เควสที่หักเงินทุกใบถูกกลุ่มธุรกรรมปฏิเสธอยู่แล้ว

## สิ่งที่ผมไม่ได้อ้าง
- ไม่ได้อ้างว่าเกมจริงให้ผู้เล่นใหม่เริ่มด้วย 0 บาท — ผมอ้างว่า **ของที่เรามีไม่ได้บอก**
- ไม่ได้แตะ `characters` ไม่ได้แตะ `read_typed_attributes` ไม่ได้เขียน migration ใด
