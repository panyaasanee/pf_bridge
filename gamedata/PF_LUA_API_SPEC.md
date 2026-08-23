# PF_LUA_API_SPEC — พื้นผิว API ของเซิร์ฟเวอร์ ที่สคริปต์ Lua ของเกมเรียกจริง

> **สร้างเมื่อ 2026-08-24** โดย `gamedata/pf_lua_api_census.py` จาก `gamedata/lua/**/*.lua` (616 ไฟล์)
> ตารางเต็มอยู่ที่ `gamedata/PF_GAMEDATA_LUA_API.tsv` (160 แถว) — ไฟล์นี้คือฉบับอ่านด้วยตา

## เลขสรุป

| ค่า | จำนวน |
|---|---:|
| ไฟล์ Lua ที่สแกน | 616 |
| ชื่อ API ที่พบ | **160** |
| จุดเรียกรวม | **12,653** |
| call site ที่วงเล็บไม่สมดุล (ข้ามไป) | 0 |
| API ที่ปรากฏในซอร์สเซิร์ฟเวอร์ที่เรากำลังสร้าง | **0 / 160** |

🔴 **ผลลบที่สำคัญที่สุดของเอกสารนี้:** ค้นชื่อทั้ง 160 ตัวใน `src/` `tools/` `tests/` `docs/` ของ
`Pirate Force ServerProject` แล้วพบ **0 ตัว** ⇒ ชั้นสคริปต์ทั้งชั้นยังไม่ถูกสร้าง
เซิร์ฟเวอร์ที่มีอยู่ตอนนี้ทำงานที่ชั้น wire/DB (actor, inventory, scene load, loot) ยังไม่มีชั้นที่สคริปต์เควสต์เรียกได้

## แยกตาม namespace

| namespace | ชื่อ API | จุดเรียก | สัดส่วน |
|---|---:|---:|---:|
| `Player` | 73 | 6,423 | 50.8% |
| `Quest` | 25 | 3,721 | 29.4% |
| `Mob` | 10 | 1,189 | 9.4% |
| `Trigger` | 17 | 828 | 6.5% |
| `Scene` | 7 | 377 | 3.0% |
| `Instance` | 9 | 55 | 0.4% |
| `Guild` | 8 | 37 | 0.3% |
| `Party` | 11 | 23 | 0.2% |

## 20 ตัวที่ถูกเรียกมากที่สุด — ลำดับความสำคัญโดยพฤตินัย

| # | API | จุดเรียก | ไฟล์ | arity | รูปพารามิเตอร์ที่พบบ่อยสุด |
|---:|---|---:|---:|---|---|
| 1 | `Player.MobAppear` | 3,532 | 295 | 2 | `var|bool` |
| 2 | `Player.AddItem` | 1,430 | 272 | 2 | `var|var` |
| 3 | `Quest.RewardItemSelect` | 1,335 | 221 | 2 | `var|var` |
| 4 | `Mob.ShowAnimation` | 716 | 295 | 1 | `var` |
| 5 | `Quest.GetQuestFlag` | 508 | 366 | 1 | `var` |
| 6 | `Quest.SetFlag` | 417 | 304 | 1 | `var` |
| 7 | `Mob.AddBuff` | 411 | 239 | 2 | `var|num` |
| 8 | `Player.RemoveItem` | 367 | 137 | 2 | `var|var` |
| 9 | `Trigger.NextStatus` | 353 | 269 | 0 | `(ไม่มีพารามิเตอร์)` |
| 10 | `Player.CheckItemNum` | 211 | 105 | 2 | `var|var` |
| 11 | `Scene.PlacementOFF` | 173 | 19 | 1 | `num` |
| 12 | `Quest.AddCriteriaExp` | 166 | 166 | 0 | `(ไม่มีพารามิเตอร์)` |
| 13 | `Quest.AddCriteriaSkillPoint` | 166 | 166 | 0 | `(ไม่มีพารามิเตอร์)` |
| 14 | `Quest.AddCriteriaCash` | 165 | 165 | 0 | `(ไม่มีพารามิเตอร์)` |
| 15 | `Quest.CheckMobKillCount` | 138 | 70 | 2 | `var|var` |
| 16 | `Trigger.GetTriggerStatus` | 134 | 71 | 1 | `var` |
| 17 | `Quest.MobKillCount` | 128 | 70 | 2 | `var|var` |
| 18 | `Quest.PlayNPCMovie` | 100 | 54 | 2 | `var|num` |
| 19 | `Player.GetItemNum` | 99 | 72 | 1 | `var` |
| 20 | `Scene.PlacementON` | 96 | 46 | 1 | `var` |

## รายการเต็ม แยกตาม namespace

### `Player` — 73 ชื่อ · 6,423 จุดเรียก

| API | จุดเรียก | arity | รูปพารามิเตอร์บ่อยสุด | รูปที่ต่างกัน |
|---|---:|---|---|---:|
| `MobAppear` | 3,532 | 2 | `var|bool` | 1 |
| `AddItem` | 1,430 | 2 | `var|var` | 4 |
| `RemoveItem` | 367 | 2 | `var|var` | 6 |
| `CheckItemNum` | 211 | 2 | `var|var` | 5 |
| `GetItemNum` | 99 | 1 | `var` | 2 |
| `GetLv` | 91 | 0 | `—` | 1 |
| `CastSkillAt` | 69 | 1 | `var` | 3 |
| `ShowMessage` | 61 | 1 | `num` | 2 |
| `GetClass` | 60 | 0 | `—` | 1 |
| `AddAndEquip` | 48 | 2 | `num|num` | 2 |
| `CheckBuff` | 47 | 1 | `var` | 3 |
| `Teleport` | 35 | 1 | `var` | 2 |
| `AddBuff` | 32 | 2 | `var|var` | 3 |
| `EnterInstance` | 32 | 1 | `var` | 2 |
| `OpenUI` | 31 | 0-2 | `—` | 2 |
| `OpenHelpUI` | 26 | 1 | `var` | 2 |
| `Addmoralized` | 21 | 1 | `expr` | 2 |
| `CameraFocus` | 16 | 1 | `var` | 2 |
| `CheckGuild` | 15 | 0 | `—` | 1 |
| `CheckEquipItem` | 14 | 1 | `num` | 1 |
| `CheckMoralized` | 14 | 1 | `var` | 1 |
| `CheckCollect` | 11 | 1 | `var` | 1 |
| `OutVehicle` | 11 | 0 | `—` | 1 |
| `Warp` | 10 | 4 | `var|var|var|var` | 1 |
| `DropProcess` | 9 | 1 | `var` | 1 |
| `TeleportThenPlayMovie` | 8 | 2 | `var|var` | 2 |
| `CheckGender` | 7 | 1 | `var` | 1 |
| `GetCash` | 7 | 0 | `—` | 1 |
| `PlayMovie` | 7 | 1 | `var` | 2 |
| `ResetMarker` | 7 | 1 | `var` | 2 |
| `AddCash` | 6 | 1 | `var` | 2 |
| `CheckSkill` | 6 | 1 | `var` | 1 |
| `EnterInstanceThenPlayMovie` | 6 | 2 | `var|var` | 2 |
| `ItemAddon` | 6 | 3 | `var|var|var` | 2 |
| `LoadInstanceGroup` | 6 | 1 | `var` | 1 |
| `TeleportWithVehicle` | 6 | 1 | `var` | 1 |
| `CheckAchievement` | 4 | 1 | `var` | 1 |
| `CheckPartyLeader` | 4 | 0 | `—` | 1 |
| `CheckSoulmate` | 4 | 0 | `—` | 1 |
| `LeaveInstance` | 4 | 0 | `—` | 1 |
| `LoadStore` | 3 | 1 | `var` | 1 |
| `AddExp` | 2 | 1 | `call` | 1 |
| `AddPpClass` | 2 | 1 | `var` | 1 |
| `AddSkillPoint` | 2 | 1 | `call` | 1 |
| `CastSkillXYZ` | 2 | 4 | `var|var|var|var` | 1 |
| `CheckParty` | 2 | 0 | `—` | 1 |
| `CheckThrowAnyPenpalLetter` | 2 | 0 | `—` | 1 |
| `GetGuildRank` | 2 | 0 | `—` | 1 |
| `RemoveBuff` | 2 | 1 | `var` | 1 |
| `AddHP` | 1 | 1 | `var` | 1 |
| `AddST` | 1 | 1 | `var` | 1 |
| `AppraiseCollectPiece` | 1 | 0 | `—` | 1 |
| `AppraiseItem` | 1 | 0 | `—` | 1 |
| `BoatHealth` | 1 | 1 | `var` | 1 |
| `BookBattleField` | 1 | 1 | `var` | 1 |
| `ChangeShip` | 1 | 1 | `var` | 1 |
| `CheckAllCollectItemSynthesisBuff` | 1 | 0 | `—` | 1 |
| `EnableGlide` | 1 | 0 | `—` | 1 |
| `GetBoatHealth` | 1 | 0 | `—` | 1 |
| `GetCurrentHP` | 1 | 0 | `—` | 1 |
| `GetCurrentST` | 1 | 0 | `—` | 1 |
| `GetMaxHP` | 1 | 0 | `—` | 1 |
| `GetMaxST` | 1 | 0 | `—` | 1 |
| `GetPpClass` | 1 | 0 | `—` | 1 |
| `GiveLvCriteriaPercentageEXP` | 1 | 0 | `—` | 1 |
| `HasAnySailorBeenSummoned` | 1 | 0 | `—` | 1 |
| `LoadConditionStore` | 1 | 1 | `var` | 1 |
| `LoadItemExchangeStore` | 1 | 1 | `var` | 1 |
| `LoadSmithStore` | 1 | 1 | `var` | 1 |
| `OpenStorage` | 1 | 0 | `—` | 1 |
| `SuveryOwner` | 1 | 0 | `—` | 1 |
| `TeleportCheck` | 1 | 1 | `var` | 1 |
| `WarpNearestMarker` | 1 | 0 | `—` | 1 |

### `Quest` — 25 ชื่อ · 3,721 จุดเรียก

| API | จุดเรียก | arity | รูปพารามิเตอร์บ่อยสุด | รูปที่ต่างกัน |
|---|---:|---|---|---:|
| `RewardItemSelect` | 1,335 | 2 | `var|var` | 1 |
| `GetQuestFlag` | 508 | 1 | `var` | 3 |
| `SetFlag` | 417 | 1 | `var` | 1 |
| `AddCriteriaExp` | 166 | 0 | `—` | 1 |
| `AddCriteriaSkillPoint` | 166 | 0 | `—` | 1 |
| `AddCriteriaCash` | 165 | 0 | `—` | 1 |
| `CheckMobKillCount` | 138 | 2 | `var|var` | 2 |
| `MobKillCount` | 128 | 2 | `var|var` | 2 |
| `PlayNPCMovie` | 100 | 2 | `var|num` | 1 |
| `SetQuestFlag` | 90 | 2 | `var|num` | 4 |
| `GetFlag` | 67 | 0 | `—` | 1 |
| `CanReportDailyQuest` | 61 | 0 | `—` | 1 |
| `ReportDailyQuest` | 61 | 0 | `—` | 1 |
| `AddLvCriteriaExp` | 59 | 0 | `—` | 1 |
| `AddLvCriteriaSkillPoint` | 59 | 0 | `—` | 1 |
| `AddLvCriteriaCash` | 58 | 0 | `—` | 1 |
| `CountDownTime` | 54 | 1 | `var` | 2 |
| `GetWeekDay` | 48 | 0 | `—` | 1 |
| `GetMobKillCount` | 20 | 1 | `var` | 1 |
| `CheckOpenTime` | 9 | 2 | `num|num` | 2 |
| `PlayNPCVoice` | 8 | 1 | `expr` | 1 |
| `CheckGuildOfflineQuest` | 1 | 0 | `—` | 1 |
| `CheckWishQuest` | 1 | 0 | `—` | 1 |
| `ReportGuildOfflineQuest` | 1 | 0 | `—` | 1 |
| `StartGuildOfflineQuest` | 1 | 0 | `—` | 1 |

### `Mob` — 10 ชื่อ · 1,189 จุดเรียก

| API | จุดเรียก | arity | รูปพารามิเตอร์บ่อยสุด | รูปที่ต่างกัน |
|---|---:|---|---|---:|
| `ShowAnimation` | 716 | 1 | `var` | 1 |
| `AddBuff` | 411 | 2 | `var|num` | 2 |
| `CallMob` | 15 | 2 | `var|var` | 1 |
| `EndMove` | 15 | 0-1 | `—` | 3 |
| `CheckApproachTarget` | 8 | 0 | `—` | 1 |
| `StartMove` | 8 | 1 | `var` | 2 |
| `CheckMobPosition` | 6 | 5 | `var|var|var|var|var` | 1 |
| `CheckMobalive` | 6 | 1 | `var` | 1 |
| `CheckMobbuff` | 3 | 2 | `var|var` | 1 |
| `CheckMobAlive` | 1 | 1 | `var` | 1 |

### `Trigger` — 17 ชื่อ · 828 จุดเรียก

| API | จุดเรียก | arity | รูปพารามิเตอร์บ่อยสุด | รูปที่ต่างกัน |
|---|---:|---|---|---:|
| `NextStatus` | 353 | 0 | `—` | 1 |
| `GetTriggerStatus` | 134 | 1 | `var` | 2 |
| `HideModel` | 62 | 0 | `—` | 1 |
| `PlayFx` | 57 | 0 | `—` | 1 |
| `TriggerShowMessage` | 55 | 2 | `num|var` | 2 |
| `SetTriggerStatus` | 52 | 2 | `var|var` | 2 |
| `StartTriggerAnimation` | 43 | 4-5 | `var|var|var|num` | 3 |
| `StartAnimation` | 19 | 3-4 | `var|var|num|num` | 3 |
| `HideTriggerModel` | 13 | 0-1 | `num` | 3 |
| `CastSkillXYZ` | 11 | 4 | `var|var|var|var` | 1 |
| `CastSkill` | 9 | 1 | `var` | 1 |
| `QuestActiveProgress` | 8 | 1 | `var` | 1 |
| `CastSkillBy` | 5 | 1 | `var` | 1 |
| `QuestFinishProgress` | 3 | 1 | `var` | 1 |
| `SetStatus` | 2 | 1 | `var` | 1 |
| `GetContactMode` | 1 | 1 | `num` | 1 |
| `GetTeiggerStatus` | 1 | 1 | `var` | 1 |

### `Scene` — 7 ชื่อ · 377 จุดเรียก

| API | จุดเรียก | arity | รูปพารามิเตอร์บ่อยสุด | รูปที่ต่างกัน |
|---|---:|---|---|---:|
| `PlacementOFF` | 173 | 1 | `num` | 2 |
| `PlacementON` | 96 | 1 | `var` | 2 |
| `CheckPlacementAlive` | 65 | 1 | `var` | 2 |
| `PlacementCancel` | 32 | 1 | `var` | 2 |
| `ChangeMainMusic` | 8 | 0-2 | `var|expr` | 2 |
| `CamaraShake` | 2 | 2 | `var|var` | 1 |
| `CheckPlacementCombat` | 1 | 1 | `var` | 1 |

### `Instance` — 9 ชื่อ · 55 จุดเรียก

| API | จุดเรียก | arity | รูปพารามิเตอร์บ่อยสุด | รูปที่ต่างกัน |
|---|---:|---|---|---:|
| `AddKeyEvent` | 15 | 1 | `var` | 1 |
| `GetInstanceID` | 14 | 0 | `—` | 1 |
| `CallScoreCount` | 12 | 0 | `—` | 1 |
| `GetLastingTime` | 7 | 0 | `—` | 1 |
| `AddBonusPoint` | 2 | 0-1 | `—` | 2 |
| `RemoveKeyEvent` | 2 | 1 | `var` | 1 |
| `AddBonusReward` | 1 | 0 | `—` | 1 |
| `GetInstanceId` | 1 | 0 | `—` | 1 |
| `SetLastingTime` | 1 | 1 | `var` | 1 |

### `Guild` — 8 ชื่อ · 37 จุดเรียก

| API | จุดเรียก | arity | รูปพารามิเตอร์บ่อยสุด | รูปที่ต่างกัน |
|---|---:|---|---|---:|
| `GetGuildLevel` | 15 | 0 | `—` | 1 |
| `CheckPlayerGuildJob` | 7 | 1 | `var` | 1 |
| `AddMeritExp` | 6 | 1 | `var` | 1 |
| `GetPVPFaction` | 4 | 0 | `—` | 1 |
| `CheckMeritExp` | 2 | 1 | `var` | 1 |
| `GiveDailySalary` | 1 | 0 | `—` | 1 |
| `OpenGuildStorage` | 1 | 0 | `—` | 1 |
| `SetPVPFaction` | 1 | 1 | `var` | 1 |

### `Party` — 11 ชื่อ · 23 จุดเรียก

| API | จุดเรียก | arity | รูปพารามิเตอร์บ่อยสุด | รูปที่ต่างกัน |
|---|---:|---|---|---:|
| `EnterInstance` | 5 | 1 | `var` | 1 |
| `CastSkillAt` | 3 | 1 | `var` | 1 |
| `CheckPartyItem` | 2 | 2 | `var|var` | 1 |
| `GetNum` | 2 | 0 | `—` | 1 |
| `Love` | 2 | 1 | `var` | 1 |
| `PlayMovie` | 2 | 1 | `var` | 1 |
| `RemovePartyItem` | 2 | 2 | `expr|expr` | 2 |
| `SignUpArena` | 2 | 0 | `—` | 1 |
| `CheckSoulmate` | 1 | 0 | `—` | 1 |
| `PartySoul` | 1 | 0 | `—` | 1 |
| `ShowMessage` | 1 | 1 | `var` | 1 |

## วิธีอ่านคอลัมน์รูปพารามิเตอร์

`var` = ตัวแปร/ค่าคงที่ที่ตั้งชื่อไว้ · `num` = ตัวเลขตรง ๆ · `str` = สตริง · `bool` = true/false ·
`nil` · `call` = ผลของฟังก์ชันอื่น · `expr` = นิพจน์อื่น

ตัวอย่าง `Player.MobAppear` รูปบ่อยสุดคือ `var|bool` ⇒ รับสองพารามิเตอร์: อะไรสักอย่างที่ตั้งชื่อไว้ กับธงเปิด/ปิด

## 🔴 nonclaims — ติดไปกับทุกการใช้เอกสารนี้

- **นี่คือสิ่งที่สคริปต์ของไคลเอนต์ *เรียก* ไม่ใช่สิ่งที่เซิร์ฟเวอร์ต้นฉบับ *ทำ*** — เซิร์ฟเวอร์ต้นฉบับปิดไปแล้ว กู้ไม่ได้ตลอดกาล
- **arity กับรูปพารามิเตอร์มาจากไซต์เรียก ไม่ใช่จาก signature** ⇒ บอกได้ว่าถูกเรียกด้วยอะไร แต่ไม่ได้บอกว่าฟังก์ชันรับอะไรได้บ้าง
- **ชนิดพารามิเตอร์เป็นการจัดกลุ่มทางไวยากรณ์ ไม่ใช่ชนิดข้อมูลจริง** — `var` แปลว่า "ตัวระบุ" ไม่ได้แปลว่า integer
- **ความหมายของแต่ละฟังก์ชันยังไม่ได้พิสูจน์** — ชื่อชวนให้เดา แต่ชื่อไม่ใช่หลักฐาน (บทเรียน GT-044)
- **จำนวนครั้ง = ความถี่ในซอร์ส ไม่ใช่ความถี่ตอนรัน** — ฟังก์ชันที่ถูกเรียกครั้งเดียวอาจอยู่ในลูปที่วิ่งทุกวินาที
- **ไม่ได้พิสูจน์ว่าไคลเอนต์รันสคริปต์เหล่านี้จริงทุกไฟล์** — บางไฟล์อาจเป็นของที่เลิกใช้แล้ว
- ตัวเลขทั้งหมดถูก re-derive อิสระสองครั้ง: `pf_decode_lua_npc.py` (Codex) และ `pf_lua_api_census.py` (ผู้ช่วย)
  ได้ **160 ชื่อ / 12,653 จุดเรียก / namespace totals ตรงกันทุกตัว** — คนละโค้ด คนละท่า mask comment/string
