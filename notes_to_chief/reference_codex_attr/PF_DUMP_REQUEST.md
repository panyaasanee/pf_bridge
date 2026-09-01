# ใบขอหลักฐาน runtime สำหรับงานถัดจาก v1

## วัตถุประสงค์

ขอ full-memory dump ของ `GameClient.local.bin` เพื่อปลดข้อจำกัด runtime identity ที่หลักฐาน v1 ตอบไม่ได้ โดยงาน v1 หยุดไว้ที่ Priority 1 ปิดเชิงโครงสร้าง 241/365 และเปิด 124 รายการตามจริง ห้ามใช้ dump ใหม่เพื่อเติมชื่อหรือ field แบบเดา

หลักฐานที่มีอยู่สองไฟล์เป็น `MiniDumpWithDataSegs` (`flags=0x1`) ไม่ใช่ full-memory dump แม้พบ TypeDescriptor 3,121 รายการต่อ snapshot แต่ไม่มี vtable-to-RTTI chain ที่ครบในช่วง memory ที่ถูกเก็บ จึงพิสูจน์ชื่อคลาสจาก vtable ไม่ได้

## คุณสมบัติ dump ที่ต้องการ

- ต้องเป็น dump ที่มีบิต `MiniDumpWithFullMemory` (`0x00000002`) อยู่ใน `MINIDUMP_TYPE`; อาจมี flag อื่นร่วมได้ แต่ห้ามใช้ `MiniDumpNormal` หรือ `MiniDumpWithDataSegs` เพียงอย่างเดียว
- ต้องมาจาก process ที่รัน `GameClient.local.bin` SHA-256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623` เท่านั้น
- dump และ capture ต้องอยู่ในเครื่องนี้ตลอดกาล ห้ามอัปโหลดหรือส่งออกนอกเครื่อง
- ต่อไฟล์ให้บันทึกเฉพาะ metadata ประกอบ: ชื่อสถานะด้านล่าง, เวลาที่เก็บ, ขนาดไฟล์, SHA-256, image SHA-256 และคำบรรยายสิ่งที่เห็นบนจอ
- ใบนี้ไม่กำหนดวิธีเปิดเซิร์ฟเวอร์หรือเกม ให้ใช้ runtime playbook ของผู้ทดสอบที่มีอยู่แล้ว

## วิธีอ่านตัวเลข “หนึ่ง dump ตอบได้กี่ตัว”

ตัวเลขด้านล่างเป็นจำนวน UNKNOWN เป้าหมายที่มีเหตุให้ตรวจจากออบเจกต์ซึ่งควรมีชีวิตในสถานะนั้น (`candidate ceiling`) ไม่ใช่จำนวนที่รับประกันว่าจะปิดได้จริง

หนึ่ง dump ปิดได้อย่างรับประกันล่วงหน้า `0` ตัว และมีเพดาน `N` ตามตาราง เพราะ full memory ช่วยพิสูจน์ vtable/class/instance identity แต่บางรายการยังติด call path, direction, gate หรือ field order ที่ snapshot เดียวไม่แสดง การรับผลต้อง re-run parser แล้วพิสูจน์ chain ต่อรายการเท่านั้น ดังนั้นให้ใช้ช่วง `0..N จาก 124` เพื่อชั่งน้ำหนัก ไม่ใช้ `N` เป็นผลสำเร็จล่วงหน้า

## ลำดับสถานะที่ควรเก็บ

| ลำดับ | ป้ายสถานะ | เงื่อนไขที่สังเกตได้บนจอ | ออบเจกต์ที่ต้องมีชีวิต | candidate ceiling ต่อ dump |
|---:|---|---|---|---:|
| 1 | `WORLD_READY_ACTORS` | ยืนอยู่ในแมพ เห็น minimap, แถบ HP/ทรัพยากร, ตัวละครตนเอง, NPC อย่างน้อยหนึ่งตัว และ monster อย่างน้อยหนึ่งตัวครบ | player/actor, NPC, monster, world/position/teleport state, actor effects | `0..14` |
| 2 | `INVENTORY_EQUIPMENT_OPEN` | อยู่ในแมพและเปิดหน้าต่างกระเป๋า/อุปกรณ์ เห็นช่องที่มี item จริงอย่างน้อยหนึ่งชิ้นและรายละเอียดอุปกรณ์ครบ | item, item attr, bag/container, equipped/fashion/collection objects | `0..13` |
| 3 | `COMBAT_AND_DROP_LIVE` | มี monster เป็นเป้าหมาย เห็นแถบ HP และค่าบนจอเปลี่ยน; เก็บอีก snapshot หลัง monster ตายขณะที่ของตกยังเห็นอยู่และยังไม่ถูกเก็บ | combat/HP/buff/cooldown, relive marker ถ้ามี, fighting-drop/loot objects | `0..5` ต่อ snapshot; ควรเก็บอย่างน้อยสองจังหวะ |
| 4 | `CHARACTER_SELECT_READY` | อยู่หน้ารายชื่อตัวละคร เห็น slot/ชื่อตัวละครครบและปุ่มเลือกหรือเข้าเกมพร้อมใช้งาน แต่ยังไม่เข้าแมพ | login response, select actor, login/session protocol objects | `0..3` |
| 5 | `PARTY_PANEL_LIVE` | อยู่ในแมพ มีสมาชิกอื่นใน party อย่างน้อยหนึ่งคน เห็นชื่อและแถบ HP ใน party panel | party attr/update/search objects | `0..3` |
| 6 | `NPC_DIALOG_QUEST_LIVE` | ยืนหน้า NPC และหน้าต่างสนทนาหรือ quest เปิดอยู่ เห็นข้อความ/ตัวเลือกหรือ tracker ที่เกี่ยวข้องครบ | NPC conversation/movie, quest-NPC, quest misc, gathering/treasure point เมื่อมีบนจอ | `0..6` |
| 7 | `STORAGE_TRADE_STALL_LIVE` | เปิดหน้าต่าง storage, trade หรือ stall ที่มีรายการจริงปรากฏ; เก็บแยกต่อชนิดหน้าต่าง | storage/trade/stall/conditional-store/black-market objects | `0..11` รวมกลุ่ม; หนึ่งหน้าต่างมักตอบได้เพียงบางส่วน |
| 8 | `GUILD_STORAGE_EVENT_LIVE` | เปิด guild storage หรือ guild event panel และเห็นข้อมูลสมาชิก/ช่องเก็บ/รายการ event ถูกโหลดแล้ว | guild storage command/result/update และ guild event/data objects | `0..13` รวมกลุ่ม; ควรแยก storage กับ event |
| 9 | `ITEM_MALL_LIVE` | เปิด item mall และ item-mall bag เห็นสินค้า/ของขวัญหรือข้อมูลส่วนตัวที่โหลดแล้ว | item-mall bag/update/transfer/gift/IMS/gashapon objects | `0..9` |
| 10 | `PET_PANEL_AND_PET_LIVE` | pet ถูกเรียกออกมาเห็นในโลก และเปิดหน้าต่าง pet ที่เห็น equipment, learned skill และ AI setting | pet common/data/equipment/skill/AI/merge objects | `0..7` |
| 11 | `COMMUNITY_MAIL_EXPRESS_LIVE` | เปิด friend/community/mail หรือ express panel และเห็นรายการจริงอย่างน้อยหนึ่งรายการ; เก็บแยกตาม panel | actor relationship, friend/blacklist/mail/vow/soulmate, player search, express objects | `0..15` รวมกลุ่ม; หนึ่ง panel ตอบได้เพียงบางส่วน |
| 12 | `INSTANCE_ARENA_ACTIVITY_LIVE` | อยู่ใน instance/arena หรือเปิด ranking/activity/achievement panel ที่มีข้อมูลจริง; สำหรับผล arena ให้เก็บอีก snapshot เมื่อหน้าผลปรากฏ | instance, arena, activity, achievement, ranking/hit-parade, daily reward objects | `0..16` รวมกลุ่ม; ต้องแบ่งหลายสถานะย่อย |
| 13 | `SPECIAL_FEATURE_LIVE` | เปิด feature ที่ต้องการตรวจและเห็นข้อมูลจริงครบ เช่น crystal, winemaking, newsflash, system gift หรือ skill result | feature-specific objects ตามรายการท้ายเอกสาร | `0..9` รวมกลุ่ม; โดยทั่วไป `0..1` หรือ `0..2` ต่อหน้าจอ |

ลำดับ 1–5 ให้ผลตอบแทนต่อเวลาสูงสุด เพราะเป็นสถานะหลักและมีออบเจกต์หลายชนิดอยู่พร้อมกัน หากมีงบเพียงหนึ่ง dump ให้เลือก `WORLD_READY_ACTORS`; หากมีสอง ให้เพิ่ม `INVENTORY_EQUIPMENT_OPEN` โดยคงโลกและตัวละครไว้ใน snapshot เดียวกันเท่าที่สถานะจริงอนุญาต

## รายการ UNKNOWN เป้าหมายต่อสถานะ

### `CHARACTER_SELECT_READY` — 3

`GSCN_LoginProtocol`, `SelectActorVital`, `LSCN_LoginVitalRes`

### `WORLD_READY_ACTORS` — 14

`CNSS_BoardcastToSpecifiedActorVtial`, `CNSS_BoardcastToAllActorVtial`, `CreateActorVital`, `TeleportVital`, `UpdateAttrVital`, `ServerAddedInfoVital`, `GetWorldInfoVital`, `ActorInspectVital`, `VitalData`, `VitalProtocol`, `TriggerSyncVital`, `NPCAppearModule_Client`, `ActorEffectsModule_Client`, `CTracePathVital`

### `COMBAT_AND_DROP_LIVE` — 5

`ReliveMarkerVital`, `CBuffVital`, `CStartCooldownVital`, `FightingDropModule_Client`, `FightingDropNotify`

### `INVENTORY_EQUIPMENT_OPEN` — 13

`ItemBagAttr_Equiped`, `ItemAttr`, `ItemBagAttr`, `ItemOperateVitalRes`, `ItemLockVital`, `EquipFashionVital`, `FashionChangeVital`, `ItemBindingLockVitalRes`, `CustomItem`, `Equipment_ReceiveCandidateCastingItemVital`, `CollectionBookDataVitalRes`, `CollectionObj_UpdateCollectionObjBagVital`, `CollectionObj_UpdateCollectEffectVital`

### `PARTY_PANEL_LIVE` — 3

`PartyAttr`, `PartyUpdateVital`, `CSearchPartyVital`

### `NPC_DIALOG_QUEST_LIVE` — 6

`QuestNPCModule`, `NPCConversation`, `UpdateQuestMiscDataVital`, `Gathering_UpdateSceneGatheringPointVital`, `TreasureHunt_UpdateSceneTreasurePointVital`, `NPC_MovieModule`

### `STORAGE_TRADE_STALL_LIVE` — 11

`TradeItemResultVital`, `UpdateConditionalStoreItemVital`, `StorageOpenVital`, `StorageCmdVital`, `StorageResultVital`, `TradeCmdVital`, `TradeZoomVital`, `StallStartVital`, `StallOpenVital`, `StallOperateVital`, `BlackMarketItem`

### `GUILD_STORAGE_EVENT_LIVE` — 13

`GCSS_GuildStorageOpenVital`, `GCGS_GuildStorageCmdVital`, `GCGSSS_GuildStorageResultVital`, `GSSS_GuildStorageCmdVital`, `DBSS_GuildStorageInitialVital`, `DBSS_GuildStorageUpdateVital`, `GCGSSS_GuildStorageVital_ReArrangeResult`, `GSSS_GuildEventVitalReq`, `GSSS_GuildEventVitalRes`, `GSSS_GuildDataVitalRes`, `GSSS_GSInitialGuildDataVital`, `GSSS_GuildUpdateEventVital`, `GSSS_GuildUpdateQuestMemberVital`

### `ITEM_MALL_LIVE` — 9

`ItemMallBagAttr`, `ItemMallUpdatePersonalDataVital`, `ItemMallBagOpenRes`, `ItemMallBagUpdate`, `ItemMallBagItemTransfer`, `ItemMallPersonalGiftVital`, `ItemMallGiftNotifyVital`, `ItemMallIMSDataRes`, `ItemMallGashaponDesVital`

### `PET_PANEL_AND_PET_LIVE` — 7

`ActorPetsCommonAttr`, `Pets_UpdatePetsDataVital`, `Pets_ChangePetEquipmentVital`, `Pets_UpdateLearnedPetSkillVital`, `Pets_SetPetSkillVital`, `Pets_SetPetAIVital`, `Pets_UpdatePetsMegringDataVital`

### `COMMUNITY_MAIL_EXPRESS_LIVE` — 15

`ActorCommunityDataSet`, `ActorRelationshipData`, `Community_InitalizeActorCommunityVital`, `Community_AddFriendVital`, `Community_AddBlackListVital`, `Community_ReceiveNewMailVital`, `Community_RequestSoulMateMatchVital`, `Community_GetActorVowLockListVital`, `Community_UpdateActorVowLockVital`, `Community_ReplyPenpalLetterVital`, `PlayerSearchVitalRes`, `Express_InitalizeActorExpressVital`, `Express_ClientGetExpressItemAttrsVital`, `Express_ClientReceiveNewExpressVital`, `Express_ClientSendExpressVital`

### `INSTANCE_ARENA_ACTIVITY_LIVE` — 16

`InstanceStatisticVital`, `InstanceInviteVital`, `InstanceRefreshVital`, `CArenaVital`, `CArenaGameDataVital`, `CArenaResultVital`, `Activity_BasicVital`, `Activity_ActorCommandVital`, `Activity_SendRankingVital`, `ActorActivity_UpdateDailyActivityStateVital`, `CAchievementsBoardcastReqVital`, `CHitParadeVital`, `CHitParadeActorDataVital`, `CHitParadeResVital_JP`, `CHitParadeAvatarResVital_JP`, `DailyRewardVitalRes`

### `SPECIAL_FEATURE_LIVE` — 9

`BuildingCrystal_UpdateCrystalSlotVital`, `Winemaking_UpdateWindPotSlotVital`, `Winemaking_UpdateLearnedFormulaVital`, `UserSetting_UpdateServerSettingVital`, `GetNewsflashVital`, `GM_RunGMCommandVital`, `CWebGMVital_GSGC`, `GSCN_AskForSystemGiftVital`, `CLearnSkillResultVital`

ยอดรวมรายการไม่ซ้ำในภาคผนวกนี้เท่ากับ 124 พอดี

## เกณฑ์รับหลักฐานรอบใหม่

1. ตรวจ dump header ว่ามี `MiniDumpWithFullMemory` bit จริงก่อนวิเคราะห์
2. ตรวจ image SHA-256 ใน metadata ให้ตรง `.local.bin`
3. วิเคราะห์แต่ละ dump แยก `source=DUMP`; ห้ามนำชื่อกลับไปเขียนเป็นข้อเท็จจริง `source=IMAGE`
4. ยอมรับ class name เฉพาะ RTTI chain ที่ครบถึง vtable และมี offset ตรวจย้อนกลับได้
5. รายงานต่อ UNKNOWN ว่า `RESOLVED`, `INFORMED_NOT_CLOSED`, `NOT_PRESENT` หรือ `UNRESOLVED`; ห้ามนับ candidate ceiling เป็น resolved
6. ถ้าหลังชุดลำดับ 1–5 ไม่มี vtable chain ใหม่ ให้หยุดและทบทวนต้นทุนก่อนเก็บสถานะเฉพาะทางต่อ
