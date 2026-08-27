[ถึง: chief cloud (cc) และ Panya · จาก: Codex LOCAL งาน static]

# LUA-NPC-EXTRACTED — Lua 616/616 และ native NPC 289/289

- เวลา: 2026-08-24 00:53–00:55 (+07:00)
- ลักษณะงาน: static read-only เท่านั้น; ไม่เปิดเกม, ไม่บูต server/client, ไม่ใช้ DB, ไม่จับ `LOCK_GAME`
- สคริปต์: `pf_bridge\gamedata\pf_decode_lua_npc.py` version `1.0.0`
- ผลรันจริง: exit `0`

## ช่องค้นบังคับก่อนเริ่ม

- ค้นใน `pf_bridge\external\PF_PROTOCOL_REGISTRY.tsv` และ `PF_SERIALIZER_FIELDS.tsv` แล้ว: **ไม่เจอ** roster/ตัวถอด `.lu_` หรือ `.npc` และไม่เจอคำค้น `NPCPlacement`, `SceneNPCCreation`, `MobAppear`, `Quest.SetFlag`; ชุดส่งมอบนี้เป็นทะเบียน wire serializer จึงไม่ตอบงานข้อมูลเกมรอบนี้
- ค้น `pf_bridge\gamedata\00_SEARCH_HERE_FIRST.md`, `PF_GAMEDATA_INDEX.tsv`, `PF_GAMEDATA_COLUMNS.tsv` และ `tables\` แล้ว: **เจอ** 188 ตารางเดิม แต่ก่อนเริ่ม **ไม่เจอ** `gamedata\lua\`, `gamedata\scene\` หรือ placement TSV สำเร็จรูป

## สรุปผล

### Lua

- census: 616 ไฟล์ (`Data\Script\` 310, `Data\Script\Quest\` 306)
- ตรวจ magic ครบ 616/616: เป็น `$pcz` ครบ; magic ผิด 0
- คลาย LZMA1 สำเร็จ 616, ล้มเหลว 0; output รวม 1,092,574 bytes
- error ดิบ: **ไม่มี**
- เขียน source แบบคงไบต์หลังคลายไว้ที่ `pf_bridge\gamedata\lua\` ครบ 616 ไฟล์
- index: `pf_bridge\gamedata\PF_GAMEDATA_LUA_INDEX.tsv` 616 data rows
- meta: `pf_bridge\gamedata\_LUA_meta.json`

### `.npc`

- census ทั้ง `GameClient`: 289 ไฟล์; ใต้ `Data\Scene\` 288 ไฟล์
- parse exact EOF สำเร็จ 289, ติด 0; error ดิบ/offset ที่ติด: **ไม่มี**
- version ทั้ง tree: v1 = 6 ไฟล์, v2 = 283 ไฟล์
- actual placement collection รวม 6,248 records; definition collection รวม 3,745 records
- เขียน `*.placements.tsv` ครบ 289 ไฟล์; ขนาดรวม `gamedata\scene\` = 1,529,875 bytes
- index: `pf_bridge\gamedata\PF_GAMEDATA_SCENE_INDEX.tsv` 289 data rows
- meta: `pf_bridge\gamedata\_SCENE_meta.json`

## Correction ที่พบจาก exact-EOF parser

ข้อเท็จจริง “u16 ตัวที่สองรวม 3,745 และ `bg0001` ได้ 113” ยืนยันจากไบต์จริง แต่ฟิลด์นั้น **ไม่ใช่ placement_count**; เป็น `definition_count` ของ NPC set collection แรก หลัง definition แต่ละตัว (`u32 name_len + UTF-16LE name + payload 16 bytes`) ยังมี `u16 placement_count` อีกตัว แล้วจึงเป็น `NPCPlacement` records ที่มี XYZ

| ค่า | `bg0001.npc` |
|---|---:|
| version @ `0x0` | 2 |
| definition_count @ `0x2` | 113 |
| placement_count field offset | `0x11C8` |
| actual placement_count | 149 |
| final parsed offset | `0x6BD7` = file size 27,607 |

จึงเก็บสองฟิลด์แยกกันใน scene index: `placement_count=149` และ `definition_count=113`; ไม่เปลี่ยนชื่อ definition ให้เป็น placement เพื่อบังคับผลให้ตรงสมมติฐานเดิม

## ด่าน `bg0001` / P30

- `version=2`
- raw header count @ `0x2` = 113 definitions
- actual placements = 149
- placement index 30: record `[0x1D28,0x1D89)`, name `Mob_Set_31 01`, set `Mob_Set_31`, template id 31
- XYZ เริ่มที่ `0x1D46` พอดี และ offset นี้ตกใน **placement index 30** พอดี
- XYZ = `(1747.5244140625, -7837.69775390625, 931.0413208007812)`

## ไฟล์ `.npc` ตัวที่ 289

อยู่ที่ `GameClient\Data\Palettes\PlayerViewer\PlayerViewer.npc` ไม่ได้อยู่ใต้ `Data\Scene\`; เป็น empty native NPC container สำหรับ PlayerViewer palette ตามตำแหน่งไฟล์ ขนาด 6 bytes (`02 00 00 00 00 00`): version 2, definitions 0, placements 0, exact EOF. ผลอยู่ที่ `gamedata\scene\PlayerViewer\PlayerViewer.placements.tsv`

## 10 ฉากที่มี actual placement มากที่สุด

คอลัมน์ definition แนบไว้เพื่อไม่ให้สับสนกับค่า 3,745 จากหัวไฟล์

| scene | actual placements | definitions |
|---|---:|---:|
| Bg2016 | 240 | 29 |
| Bg2006 | 227 | 28 |
| Bg1178 | 168 | 26 |
| bg0001 | 149 | 113 |
| bg0004 | 116 | 56 |
| Bg0002 | 106 | 46 |
| Bg0021 | 105 | 28 |
| Bg0010 | 100 | 40 |
| bg0020 | 93 | 31 |
| bg0005 | 92 | 65 |

## สุ่มเปิด Lua 5 ไฟล์ — 5 บรรทัดแรก

สุ่มแบบ deterministic seed `20260824` จากไฟล์ที่ 5 บรรทัดแรกเป็น ASCII เพื่อถ่ายทอดในจดหมายโดยไม่ให้ encoding ของ comment/string เปลี่ยน source จริง

`Data/Script/Quest/q_check_lv.lu_` → `lua/Quest/q_check_lv.lua`

```lua
function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
```

`Data/Script/Quest/q_day_kill3.lu_` → `lua/Quest/q_day_kill3.lua`

```lua
function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
```

`Data/Script/Quest/q_movie_teach1.lu_` → `lua/Quest/q_movie_teach1.lua`

```lua
function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
```

`Data/Script/Quest/q_send5.lu_` → `lua/Quest/q_send5.lua`

```lua
function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
```

`Data/Script/Quest/q_skill1.lu_` → `lua/Quest/q_skill1.lua`

```lua
function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function Accept_Check()
```

## Game API census จาก Lua

นับ call expression หลัง mask Lua comments, quoted strings และ long strings แล้ว; เก็บ spelling/case ตาม source ไม่ normalize ชื่อที่ดูเหมือน typo

- game API: 160 ชื่อ, ถูกเรียกรวม 12,653 ครั้ง
- namespace totals: `Player=6,423`, `Quest=3,721`, `Mob=1,189`, `Trigger=828`, `Scene=377`, `Instance=55`, `Guild=37`, `Party=23`
- ตัวอย่างที่ขอ: `Quest.SetFlag=417`, `Player.MobAppear=3,532`, `Mob.ShowAnimation=716`
- standard Lua/library calls แยกออกจากรายการ game API: `string.find=40`, `math.floor=6`, `math.mod=2`, `math.random=2`, `math.randomseed=2`, `os.time=2`

รายชื่อ game API ทั้งหมด:

```text
Guild.AddMeritExp	6
Guild.CheckMeritExp	2
Guild.CheckPlayerGuildJob	7
Guild.GetGuildLevel	15
Guild.GetPVPFaction	4
Guild.GiveDailySalary	1
Guild.OpenGuildStorage	1
Guild.SetPVPFaction	1
Instance.AddBonusPoint	2
Instance.AddBonusReward	1
Instance.AddKeyEvent	15
Instance.CallScoreCount	12
Instance.GetInstanceID	14
Instance.GetInstanceId	1
Instance.GetLastingTime	7
Instance.RemoveKeyEvent	2
Instance.SetLastingTime	1
Mob.AddBuff	411
Mob.CallMob	15
Mob.CheckApproachTarget	8
Mob.CheckMobAlive	1
Mob.CheckMobalive	6
Mob.CheckMobbuff	3
Mob.CheckMobPosition	6
Mob.EndMove	15
Mob.ShowAnimation	716
Mob.StartMove	8
Party.CastSkillAt	3
Party.CheckPartyItem	2
Party.CheckSoulmate	1
Party.EnterInstance	5
Party.GetNum	2
Party.Love	2
Party.PartySoul	1
Party.PlayMovie	2
Party.RemovePartyItem	2
Party.ShowMessage	1
Party.SignUpArena	2
Player.AddAndEquip	48
Player.AddBuff	32
Player.AddCash	6
Player.AddExp	2
Player.AddHP	1
Player.AddItem	1430
Player.Addmoralized	21
Player.AddPpClass	2
Player.AddSkillPoint	2
Player.AddST	1
Player.AppraiseCollectPiece	1
Player.AppraiseItem	1
Player.BoatHealth	1
Player.BookBattleField	1
Player.CameraFocus	16
Player.CastSkillAt	69
Player.CastSkillXYZ	2
Player.ChangeShip	1
Player.CheckAchievement	4
Player.CheckAllCollectItemSynthesisBuff	1
Player.CheckBuff	47
Player.CheckCollect	11
Player.CheckEquipItem	14
Player.CheckGender	7
Player.CheckGuild	15
Player.CheckItemNum	211
Player.CheckMoralized	14
Player.CheckParty	2
Player.CheckPartyLeader	4
Player.CheckSkill	6
Player.CheckSoulmate	4
Player.CheckThrowAnyPenpalLetter	2
Player.DropProcess	9
Player.EnableGlide	1
Player.EnterInstance	32
Player.EnterInstanceThenPlayMovie	6
Player.GetBoatHealth	1
Player.GetCash	7
Player.GetClass	60
Player.GetCurrentHP	1
Player.GetCurrentST	1
Player.GetGuildRank	2
Player.GetItemNum	99
Player.GetLv	91
Player.GetMaxHP	1
Player.GetMaxST	1
Player.GetPpClass	1
Player.GiveLvCriteriaPercentageEXP	1
Player.HasAnySailorBeenSummoned	1
Player.ItemAddon	6
Player.LeaveInstance	4
Player.LoadConditionStore	1
Player.LoadInstanceGroup	6
Player.LoadItemExchangeStore	1
Player.LoadSmithStore	1
Player.LoadStore	3
Player.MobAppear	3532
Player.OpenHelpUI	26
Player.OpenStorage	1
Player.OpenUI	31
Player.OutVehicle	11
Player.PlayMovie	7
Player.RemoveBuff	2
Player.RemoveItem	367
Player.ResetMarker	7
Player.ShowMessage	61
Player.SuveryOwner	1
Player.Teleport	35
Player.TeleportCheck	1
Player.TeleportThenPlayMovie	8
Player.TeleportWithVehicle	6
Player.Warp	10
Player.WarpNearestMarker	1
Quest.AddCriteriaCash	165
Quest.AddCriteriaExp	166
Quest.AddCriteriaSkillPoint	166
Quest.AddLvCriteriaCash	58
Quest.AddLvCriteriaExp	59
Quest.AddLvCriteriaSkillPoint	59
Quest.CanReportDailyQuest	61
Quest.CheckGuildOfflineQuest	1
Quest.CheckMobKillCount	138
Quest.CheckOpenTime	9
Quest.CheckWishQuest	1
Quest.CountDownTime	54
Quest.GetFlag	67
Quest.GetMobKillCount	20
Quest.GetQuestFlag	508
Quest.GetWeekDay	48
Quest.MobKillCount	128
Quest.PlayNPCMovie	100
Quest.PlayNPCVoice	8
Quest.ReportDailyQuest	61
Quest.ReportGuildOfflineQuest	1
Quest.RewardItemSelect	1335
Quest.SetFlag	417
Quest.SetQuestFlag	90
Quest.StartGuildOfflineQuest	1
Scene.CamaraShake	2
Scene.ChangeMainMusic	8
Scene.CheckPlacementAlive	65
Scene.CheckPlacementCombat	1
Scene.PlacementCancel	32
Scene.PlacementOFF	173
Scene.PlacementON	96
Trigger.CastSkill	9
Trigger.CastSkillBy	5
Trigger.CastSkillXYZ	11
Trigger.GetContactMode	1
Trigger.GetTeiggerStatus	1
Trigger.GetTriggerStatus	134
Trigger.HideModel	62
Trigger.HideTriggerModel	13
Trigger.NextStatus	353
Trigger.PlayFx	57
Trigger.QuestActiveProgress	8
Trigger.QuestFinishProgress	3
Trigger.SetStatus	2
Trigger.SetTriggerStatus	52
Trigger.StartAnimation	19
Trigger.StartTriggerAnimation	43
Trigger.TriggerShowMessage	55
```

## Source integrity และ reproducibility

ตัวอย่าง SHA-256 5 ไฟล์ ก่อน/หลัง:

| source | before | after |
|---|---|---|
| `Data\Script\Quest\q_add_equip.lu_` | `6ac8230b2f3b8e27f7ffee161ec39aa7f621a0b92c5a644fa5d626ab8756cf78` | เหมือนเดิม |
| `Data\Script\Quest\q_wish.lu_` | `abc2b76881c1021500eb8672b91f5dca184f0d14bcb1e0169e65710420d5dc71` | เหมือนเดิม |
| `Data\Script\t_2exch1_q1.lu_` | `60da74783b10ce3c4467a9439eeed6563f7226fe301a34e15ee4650837c692e6` | เหมือนเดิม |
| `Data\Scene\Save\bg0001\bg0001.npc` | `026bbe32ca2b69853b1433d585de7e80bb67e7f713e086b9347fd10ad1dc2070` | เหมือนเดิม |
| `Data\Scene\Save\Bg0002\Bg0002.npc` | `a649f4afab701df3698b9ffebbb83b77863531a9113c40b6f12f056b7f030b16` | เหมือนเดิม |

สคริปต์ rehash input ทั้ง 616 Lua + 289 NPC หลังจบด้วย: changed = 0. รันเต็มซ้ำหนึ่งรอบแล้วตรวจ SHA ของผลลัพธ์ 909 ไฟล์: before 909, after 909, changed 0, removed 0. Meta reuse เวลาเดิมเมื่อ source manifest และ script version เหมือนเดิม จึงได้ผล byte-identical เมื่อรันซ้ำบน snapshot เดิม

ขนาดโฟลเดอร์ผลลัพธ์:

- `pf_bridge\gamedata\lua\` = 1,092,574 bytes
- `pf_bridge\gamedata\scene\` = 1,529,875 bytes

## ชั้นหลักฐานและ nonclaims

- ชั้น static: source bytes, SHA-256, offsets, exact-EOF parse, extracted Lua และ API call census ข้างบน
- ชั้น client-observable: ว่างเปล่าโดยเจตนา; ไม่เปิดเกมและไม่มีภาพหน้าจอ
- **Lua ในไคลเอนต์ = สิ่งที่ไคลเอนต์รู้ ไม่ใช่กฎของเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้วกู้ไม่ได้**
- **ชื่อ API ที่เห็นใน Lua ไม่ได้พิสูจน์ว่าเซิร์ฟเวอร์เดิม implement มันแบบไหน**
- **placement_count จากไฟล์ไม่ได้พิสูจน์ว่า runtime โหลดครบทุกตัว**; และ correction รอบนี้แยกชัดว่า u16 @ `0x2` เป็น definition_count ไม่ใช่ actual placement_count
- ชื่อ generic ใน placement TSV (`f32_3..5`, `u16_0..6`, `version2_byte`) ตั้งใจไม่เดาความหมาย; `x/y/z` แยกเฉพาะ triple ที่ parser อ่านต่อเนื่องและผ่าน anchor `0x1D46`
