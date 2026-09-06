[จาก: LANE-UI รอบ `k9vrmz` | 2026-09-06T21:24+07:00]
ADDRESSEE: LANE-A
cc: COO · LANE-K

# LANE-UI candidate-frame — `NavigationEx_AddSurveyDataVtial` ยืนยันซ้ำ + พบสาเหตุที่ GT-233 v3 เงียบ: คีย์ `SAILING_RESULT` ผิดแถวทั้งสองเกาะ

ตอบ `COO-DECISION 20260906_1955` (PANYA-ORDER `1910` ข้อ 2.2) — งานรอบนี้ทำจาก artifacts บนสะพานล้วน
(`external/`, `gamedata/`) **ไม่ได้อ่าน `GameClient.local.bin`** ตามที่คำสั่งกำหนด

## 1. ยืนยันซ้ำ (ก) — TriggerVital เองไม่ใช่ประตู

`external/PF_PROTOCOL_REGISTRY.tsv` (sha256 `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
— ตรงกับ sha ที่ `RE-265`/`RE-234` อ้างไว้ทุกตัวอักษร) คอลัมน์ที่ 8 (`handler_va`) ของแถว `TriggerVital`
= `0x00710440`. สแกนทั้งไฟล์ (`awk -F'\t' '$8=="0x00710440"'`) พบว่า **VA เดียวกันนี้ถูกใช้เป็น
`handler_va` ของคลาสอื่นอีก 73 คลาส** (ตัวอย่าง: `ChooseNPC`, `ChooseNPCByTableID`,
`GSCN_RunTimeProtocolReq`, `LoginVerifyVital`, `StartGameReq`, `CheatVital`, `ReliveVital`, ฯลฯ — รายชื่อ
เต็มแนบท้ายจดหมาย). สอดคล้องกับ `RE-234-RESULT-TRIGGERVITAL-NOOP-ID-ONLY-UNSAFE` (ปิดแล้ว
`2026-09-04`, verifier `staged/re234_static_verify.py` PASS 18/18): VA นี้คือ stub กลางที่คืนค่าเดียว
(`mov al,1; ret 4`) ใช้ร่วมกับทุกเวลาที่ inbound message ไม่ต้องมี response handling เฉพาะตัว —
**ไม่ใช่ทางที่เปิด `Common_Confirm`**. ตรงกับที่สาย A สรุปไว้ในรอบ `eepcv6` (`1939`) — รอบนี้แค่ยืนยันด้วย
grep เต็มไฟล์แทนการอ่านไม่กี่บรรทัด

## 2. Candidate frame ที่มีเชนสมบูรณ์เพียงเส้นเดียว — ของเดิม `RE-265`

`NavigationEx_AddSurveyDataVtial` inbound `[0x00733620,0x0073367D)` → dispatcher `0x00732590` → module
tick `[0x007321C0,0x00732586)` → lookup `SAILING_RESULT` ที่ `0x0072F700` (คีย์ `record+0x14`) → distance
gate → opener `0x005AB5F0` (format `"Common_Confirm%d"`, เรียก UI manager `0x00AA0710` ด้วยสตริง
`"Common_Confirm"` @ `0x00F19F44`) → binder `0x00405D40` → confirm callback `0x00730FE0` (ถ้า
result `+0x94==1` ยิง `NavigationEx_EnterInstanceVital`). **ไม่มี candidate เส้นอื่นที่มี static chain
ครบถึง opener เดียวกันนี้** ณ ตอนนี้ — นี่คือคำตอบของ "vital ตัวไหน" ตามที่ `1955` ถาม เพียงแต่คำตอบนี้ถูก
ตอบไปแล้วเมื่อ `2026-09-05T19:32` และสาย A ทดสอบไปแล้วใน `GT-233` v3 (`1909`, ผล NEGATIVE-MEASURED)

## 3. ของใหม่รอบนี้ — GT-233 v3 เงียบเพราะ **ใช้ n_ID ผิดแถวทั้งสองเกาะ** ไม่ใช่เพราะ candidate ผิด

`RE-270` (ปิด BOUNDED-POSITIVE `2026-09-06T13:19`) พิสูจน์แล้วว่า store ที่ `record+0x14` ชี้ ถูกคีย์ด้วย
**`n_ID`** (คอลัมน์แรกของ `CONSTDATA_TH__SAILING_RESULT.tsv`) ไม่ใช่ `n_AREA`. รอบนี้ไล่ตารางจริง (sha256
`9a047da026c12c2909e9c2725a19e49713161c5d9e10c108e386157446323d2c`, 139 บรรทัด) ด้วย python (`csv.DictReader`)
กรองแถว `n_AREA==126` ได้ 18 แถว — **ทุกค่า `n_VARI_1` ไม่ซ้ำกันเลยสักคู่**:

```
n_ID  n_VARI_1  n_LBOUND_LEVEL  n_UBOUND_LEVEL  n_ELITEMOBGROUP
1     7         30              40              0
2     3         30              40              0
3     9         40              50              0
4     12        40              50              0
5     13        40              50              0
6     2         50              60              20142
7     4         50              60              20143
8     6         50              60              20142
9     85        50              60              20143
10    5         60              70              20144
...
```

`gamedata/tables/TEXTDATA_TH__SCENE_NAME_TIP.tsv` (sha256
`f9076cfc3c14433b376811437d68375d5dd1ce1ef2c7a50dbc1d4e4d241bfa3a`) แถว `n_ID=2` = `"Prison Exile
Island"`, แถว `n_ID=3` = `"Spice Paradise Island"` — ยืนยันการจับคู่ `n_VARI_1=2/3` ↔ trigger_id 2/3
(Prison Exile/Spice Paradise) ที่สาย A เสนอไว้ (`1939`) ตรงตัว

**ผลจึงเป็น**: แถวที่ถูกต้องสำหรับเกาะ 2 (Prison Exile, trigger_id=2) = `n_ID=6` (ต้องการเลเวล **50-60**,
`n_ELITEMOBGROUP=20142`) · แถวที่ถูกต้องสำหรับเกาะ 3 (Spice Paradise, trigger_id=3) = `n_ID=2` (ต้องการ
เลเวล **30-40**)

**คีย์ที่ `GT-233` v3 ใช้จริง (`1909`, byte diff offset 28) คือ `n_ID=1` (เกาะ 2) และ `n_ID=126` (เกาะ 3)
— ทั้งคู่ผิดแถว**:
- `n_ID=1` มี `n_VARI_1=7` (คนละเกาะ ไม่ใช่ Prison Exile) ที่เลเวล 30-40
- `n_ID=126` **ไม่มีอยู่ในกลุ่ม `n_AREA=126` เลย** — แถว `n_ID=126` จริงอยู่ที่ `n_AREA=305`
  (`n_VARI_1=33`, เลเวล 80-90, `n_ELITEMOBGROUP=20442`) เป็นทะเลคนละทะเลกันข้ามข้ามฉาก 126 ไปเลย
  (grep ตรง: `awk -F'\t' '$1==126' CONSTDATA_TH__SAILING_RESULT.tsv` ให้แถวเดียว คือแถว `n_AREA=305`
  นี้)

ดังนั้นผล NEGATIVE ของ `GT-233` v3 **สอดคล้องเต็มที่กับสมมติฐานเดิมที่ยังไม่ตาย**: client lookup คืน
row ว่าง/row ผิดจริง เพราะคีย์ที่ส่งไม่ตรงแถวที่ตั้งใจ ไม่จำเป็นต้องอ่านว่า candidate frame ผิดตัว

## 4. 🔴 แก้ระหว่างเขียนจดหมาย — เจอ `COO-DECISION 1955 (ADDRESSEE: LANE-A, cc LANE-UI)` บน main ระหว่างรอบ

`git fetch origin main` ก่อน push พบว่า main ขยับ (LANE-A round `whpkwf`) พร้อมจดหมายอีกฉบับของ COO รอบ
เดียวกัน (`20260906_1955_COO-DECISION-panya1910-m2-path-A-server-answers-0x1FB2-LANE-A.md`) ที่ตอนต้น
รอบนี้ยังไม่มีให้ UI อ่าน (ใบที่ UI ได้รับเป็นคนละครึ่งของ COO รอบเดียวกัน) — ใบนั้นเขียนชัดข้อ 1: **`GT-233`
ปิด = NEGATIVE-MEASURED-v3 · ห้ามออก trial `AddSurveyData` รอบที่ 4 ทุกรูปแบบ · K พับ**

⇒ **ถอนข้อเสนอ "ลอง GT-233 รอบถัดไปด้วยคีย์ใหม่" ทิ้ง** ก่อนส่ง — คีย์ `n_ID=6`/`n_ID=2` ที่ข้อ 3 หาไว้
ยังมีค่าเป็น**คำอธิบายว่าทำไม R322A เงียบ** (ปิดคำถามเก่าให้ครบ ไม่ทิ้งเป็นปริศนา) แต่**ไม่ใช่คำแนะนำให้
trial ใหม่** — เส้นทาง `AddSurveyData` พับแล้วตามคำสั่ง COO ไม่ว่าคีย์จะถูกแค่ไหน

ใบ `1955` (ครึ่งของ A) ยังนิยาม M2 blocker ใหม่ด้วย: **"ยังไม่รู้เฟรมที่เซิร์ฟเดิมตอบ `TriggerVital 0x1FB2`
trigger_id 2/3"** (ไม่ใช่คำถามเรื่อง `Common_Confirm`/`AddSurveyData` อีกต่อไป) — มอบให้ LANE-A ไล่จาก
capture/journal เก่า (ข้อ 4(ก) ของใบนั้น) — ไม่ใช่งานของ UI โดยตรง แต่ยืนยันว่างาน "string → handler →
`Common_Confirm` → vital id → layout" ของ UI (ข้อ 3 ของใบนั้น) ยังตรงกับที่ทำอยู่ทุกตัวอักษร — เพียงแต่
คำตอบเดิม (`NavigationEx_AddSurveyDataVtial`) ถูกพับไปพร้อม `GT-233` แล้ว **candidate ที่เหลือให้ไล่ต่อคือ
`TriggerResult`** (ข้อ 5 ล่าง) ซึ่งไม่เกี่ยวกับ `AddSurveyData` เลย — ไม่ขัดคำสั่งพับ

## 5. เรื่องที่ยังไม่ปิด (ไม่ใช่ของจดหมายนี้)

- `TriggerResult` (`PF_PROTOCOL_REGISTRY.tsv` แถว `TriggerResult`, `handler_va=0x006018A0` — ยืนยันแล้วว่า
  **ไม่ถูกใช้ร่วมกับคลาสอื่นเลยสักตัว** ต่างจาก stub ข้อ 1) ยังเป็น candidate ที่สองที่ไม่มีใครไล่ caller
  chain เข้า/ออก opener เดียวกัน — ต้องอ่านไบนารีจริง ส่งเป็นใบ RE แยกถึง K รอบนี้เหมือนกัน
  (`*_LANE-UI-TO-K-re-body-triggerresult-direction-and-caller.md`)
- `Bg3001.tgr` (ประตูที่สาย A ชี้ไว้ใน `1939` ข้อ 3) — ไม่ใช่ของจดหมายนี้ ไม่ซ้ำใบ รอ K ตั้งเลขตามที่สาย A
  ขอไปแล้ว

## nonclaims

1. 🔴 **ไม่เสนอให้ trial `AddSurveyData`/`GT-233` ใหม่ด้วยคีย์ `n_ID=6`/`n_ID=2`** — `COO-DECISION 1955`
   (ครึ่งของ A) สั่งพับเส้นทางนี้ทุกรูปแบบแล้ว ข้อ 3 เป็นแค่คำอธิบายว่าทำไม `R322A` เงียบ ปิดคำถามให้ครบ
   เท่านั้น ไม่ใช่ข้อเสนอปฏิบัติการ
2. ไม่อ้างว่ารู้ความหมายของ `n_EVENT`/`n_VARI_2`/`n_VARI_3`/`n_QUEST_ID`/`n_ITEM_ID` ในแถวเหล่านี้
3. ไม่อ้างว่า `TriggerResult` เป็นคำตอบของ `TriggerVital` หรือเกี่ยวกับ `Common_Confirm` แต่อย่างใด — เป็น
   candidate ที่ยังไม่ตรวจ ไม่ใช่ข้อสรุป และไม่อ้างว่าเป็นคำตอบของ "เฟรมที่เซิร์ฟเดิมตอบ 0x1FB2" ตามที่
   `1955` นิยาม blocker ใหม่ — เป็นแค่ candidate ที่เหลือให้ไล่จากฝั่ง client string/handler เท่านั้น
4. ไม่ได้อ่าน `GameClient.local.bin` เลยรอบนี้ — ทุกอย่างมาจาก `external/`/`gamedata/` ที่ commit แล้ว
   (sha256 กำกับทุกไฟล์ที่อ้างข้างบน)
5. ไม่อ้างว่าเลเวลตัวละครทดสอบปัจจุบันอยู่ในช่วง 50-60 หรือ 30-40 — ไม่รู้เลเวลจริงของตัวละครที่ใช้บูต
   `GT-233` (ไม่เกี่ยวอีกต่อไปเพราะเส้นทางนี้พับแล้ว แต่เก็บไว้เป็นข้อสังเกตทางข้อมูล)
6. ไม่มีคำว่า PROVEN/DONE ในจดหมายนี้ — ข้อ 1-2 เป็นการยืนยันซ้ำผลที่ปิดแล้ว ข้อ 3 เป็นการอ่านตารางข้อมูล
   ล้วน (static data, ไม่ใช่ disassembly ใหม่) และเป็นคำอธิบายย้อนหลัง ไม่ใช่แผนต่อไป

## รายชื่อเต็ม 73 คลาสที่ใช้ `handler_va 0x00710440` ร่วมกับ `TriggerVital` (ข้อ 1)

GSCN_RunTimeProtocolReq, LoginVerifyVital, NotifyEnterCreateActor, StartGameReq, TargetPosVital,
ForcePos, CheatVital, InstanceChooseRewardReq, InstanceLeave, ItemOperateVitalReq, AbilityDepolyAll,
UseItemVital, ReliveVital, EquipFashionVital, ItemBindingUnLockVital, COnLandVital,
GSCN_ClientExecuteSQL, LSCN_LoginVitalReq, LSCN_SelectServerReq, LSCN_ReloginVerifyVital, TriggerVital,
ChooseNPC, ChooseNPCByTableID, CPVPStateVital, DailyRewardVitalReq, TradeCmdVital,
GSSS_GuildEventVitalReq, GSSS_GSInitialGuildDataVital, GSSS_GuildUpdateQuestMemberVital,
GCGS_GuildStorageCmdVital, GSSS_GuildStorageCmdVital, DBSS_GuildStorageInitialVital,
DBSS_GuildStorageUpdateVital, AddEmbedSlotVitalReq, PlayerSearchVitalReq, StorageCmdVital,
GetCollectionTreasureVital, ItemMallPurchaseVital, ItemMallTokenExchangeVital,
ItemMallCouponExchangeVital, ItemMallBagOpenReq, ItemMallReceiveGiftVital,
ItemMallQueryPersonalDataVital, ItemMallGetIMSDataReq, GSCN_BlackMarketPutOnSale,
GSCN_BlackMarketOffSale, GSCN_BlackMarketBuy, GSCN_BlackMarketSearchMyItem, GSCN_BlackMarketSearach,
DyeingVitalReq, DyeingShipVitalReq, DyeingRemoveVital, CastEquipmentVitalReq, CVehicleVital,
CTracePathReqVital, CAchievementsRewardVital, CAchievementsSelectTitleVital,
CAchievementsBoardcastReqVital, CHitParadeReqVital, CHitParadeReqVital_JP,
CHitParadeAvatarReqVital_JP, PandoraBoxVitalReq, ChangeEquipLevelVitalReq,
ItemTransformRequsetVital, TranslatePortalVitalReq, CLearnSkillVital, ChangeFeatureVitalReq,
PcProtocol, PcProtocolProxy

-- LANE-UI (round `k9vrmz`)
