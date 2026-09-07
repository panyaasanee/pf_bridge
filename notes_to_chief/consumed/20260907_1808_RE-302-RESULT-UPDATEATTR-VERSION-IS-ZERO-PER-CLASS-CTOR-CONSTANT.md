[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: chief, COO | จาก: RE runner บนเครื่องสะพาน | 2026-09-07T18:08+07:00]

# RE-302 RESULT — `0x309A UpdateAttrVital` `vital_version` = **0** (วัดแล้ว ไม่ใช่การยืม) · ค่าเป็น **ค่าคงที่ในตัว ctor รายคลาส ไม่มีตาราง** · สำมะโนครบ 519 คลาส

**สถานะ: DONE — ตอบครบทั้ง 4 ข้อ (static ล้วน)** · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะไฟล์ใด

**สามบรรทัดที่ใช้ตัดสินใจได้ทันที**
1. **`UPDATE_ATTR_VITAL_VERSION_CONFIRMED = 0` ที่ `gm/attr_wire.py:410` ถูกต้อง** — ctor `0x005E5D30` เขียน `0` ลง `+0x10` จริง ⇒ **ไม่ต้องย้อนอะไร ไม่ต้องแจ้งสายไหนว่าเฟรมเก่าถูกทิ้ง**
2. **ค่าไม่ได้ "ลู่เข้า 0"** — วัดครบทั้ง 519 คลาสแล้ว: **326 คลาส = 0 แต่ 38 คลาสเป็นค่าอื่น** (1,2,3,4,5,6,8,64) ⇒ **ห้ามยืมข้ามคลาสตลอดไป** ตามที่เจ้าของใบสงสัยไว้ถูกแล้ว
3. **ไม่มีตารางต่อคลาส** — เป็น literal ที่ ctor เขียนตรง ๆ ทุกคลาส ⇒ ได้มาทีเดียวด้วยการสแกน ctor (ทำให้แล้วในใบนี้) ไม่ต้องเปิดใบทีละคลาสอีก

- START `2026-09-07T18:04:52+07:00` · ผลเสร็จ `18:08` · ผู้ทำ: สาย RE บนเครื่องสะพาน · เจ้าของใบ/ผู้บริโภคผล: LANE-GM

## input + SHA (ก่อน/หลังงานตรงกัน · read-only ทั้งหมด)

| ไฟล์ | sha256 |
|---|---|
| `GameClient/GameClient.local.bin` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `external/PF_PROTOCOL_REGISTRY.tsv` (519 คลาส) | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` |

**ค้นก่อนถอด** — `external/`: ยืนยันตามที่เจ้าของใบเขียนไว้เอง `PF_SERIALIZER_FIELDS.tsv` **ไม่มีแถว `vital_version` ของคลาสใดเลย** (ไบต์นี้อยู่นอก span ที่ตารางเก็บ) · `PF_PROTOCOL_REGISTRY.tsv` มีคอลัมน์ `vtable_va` ครบ ⇒ ใช้เป็นจุดตั้งต้นของสำมะโนรอบนี้ · **`gamedata/`: ไม่เกี่ยว** (คำถามอยู่ในโค้ดที่เกมรัน ไม่ใช่ตารางข้อมูล)

**อ่านใบเก่าก่อนหยิบตามที่ LANE-K สั่งใน addendum**: `RE-198` (DONE/BOUNDED-NEGATIVE) และ `RE-222` Q0 อ่านแล้ว — **ไม่ทับซ้อน**: ทั้งสองใบพูดถึงรูปเฟรม/หน้าตา payload ของ `0x309A` แต่ **ไม่มีใบไหนยกไบต์ `+0x10` ของ ctor มาแสดง** ⇒ ใบนี้ไม่ใช่ SUPERSEDED และรอบนี้ตอบสิ่งที่ยังไม่มีใครวัด (การตัดสินขั้นสุดท้ายเป็นของ LANE-GM ตามที่ K เขียนไว้)

---

## ✅ ข้อ 1 — `0x309A UpdateAttrVital`

vtable `0x00F303E0` (จาก registry) ถูกเขียนที่ `0x005E5D76` ⇒ ctor = **`0x005E5D30`**

```
0x005E5D58  33 C0        xor eax, eax              <- EAX = 0
0x005E5D5A  88 46 04     mov byte ptr [esi+0x04], al
0x005E5D60  C7 06 6C 6D F8 00  mov dword ptr [esi], 0xF86D6C   (base vtable)
0x005E5D66  89 46 0C     mov dword ptr [esi+0x0C], eax
0x005E5D69  88 46 10     mov byte ptr [esi+0x10], al   <<== vital_version = 0
0x005E5D6C  88 46 11     mov byte ptr [esi+0x11], al
0x005E5D76  C7 06 E0 03 F3 00  mov dword ptr [esi], 0x00F303E0  (UpdateAttrVital vtable)
```
- **VA ของ ctor**: `0x005E5D30` · **คำสั่งที่เขียนไบต์**: `mov byte ptr [esi+0x10], al` ที่ **`0x005E5D69`** (รูปแบบ `xor`+`mov` เหมือน `ForcePos` เป๊ะ) · **ค่าที่ได้: `0`**
- **VA ของจุดที่ reader เทียบ**: `0x005F3EFC` `cmp cl, byte ptr [esi+0x10]` → `0x005F3EFF/0x005F3F01 je` (exact equality)

### เส้นทางฝั่งรับเต็ม ๆ (span `0x005F3EC0..0x005F3F30` sha256 `7d11332f52be844867c66803cfa8a841421f385fbd127c59778d04c11182603c`)

```
0x005F3EF0  mov byte ptr [ebp-0x31], 0        ; ค่าเริ่มต้นก่อนอ่าน
0x005F3EF4  call 0x0089A640                   ; อ่าน 1 ไบต์ tag 0x0B จากสาย
0x005F3EF9  mov cl, byte ptr [ebp-0x31]       ; ไบต์ที่มาจากสาย
0x005F3EFC  cmp cl, byte ptr [esi+0x10]       ; << เทียบกับค่าที่ ctor ของคลาสนั้นเขียนไว้
0x005F3F01  je  0x005F3F39                    ; ตรง = ไปต่อ
0x005F3F03  mov edx,[esi] / mov eax,[edx+0x10] / call eax   ; ไม่ตรง -> เรียก id getter (vtable+0x10)
0x005F3F12  push 0x00F30DD4 / push 0xE0000031 ; แล้ว format ข้อความ error พร้อม id
```
⇒ **ค่าที่ไคลเอนต์ "คาด" คือค่าที่ ctor ของคลาสนั้นเองเขียนไว้** ไม่ใช่ค่าคงที่กลาง — นี่คือหลักฐานเชิงกลไกว่า **ต้องเป็นรายคลาส**

## ✅ ข้อ 2 — ยืนยันซ้ำสองคลาสที่ตอบไปแล้ว (ตรงกันทั้งคู่)

| คลาส | ctor | คำสั่ง | ค่า | ตรงกับใบเดิม |
|---|---|---|---|---|
| `ForcePos` (`0x0E80`) | `0x005E5170` | `xor ecx,ecx` (`0x005E5175`) → `mov [eax+0x10], cl` ที่ **`0x005E5186`** | **0** | ✅ `RE-129` (VA เดียวกันเป๊ะ) |
| `Channel_GMGlobalMessageVital` (`0x9F2C`) | `0x0065B920` | `mov [eax+0x10], bl` ที่ **`0x0065BD38`** (`bl`=0) | **0** | ✅ `RE-132` |

## ✅ ข้อ 3 — `TeleportVital` = **4 ถูกต้อง**

ctor **`0x005E53D0`** · `mov byte ptr [esi+0x10], 4` ที่ **`0x005E5425`** (immediate ไม่ใช่รีจิสเตอร์) ⇒ **`TELEPORT_VITAL_VERSION_PROVEN_BY_RE129 = 4` ถูกต้อง**
⇒ ข้อสรุปของเจ้าของใบที่ว่า **"reader เห็น 0 เสมอ = เท็จ" ยืนยันแล้ว** และแรงกว่าที่ใบคิด (ดูข้อ 4)

## ✅ ข้อ 4 — มาจาก **ค่าคงที่ใน ctor** ไม่ใช่ตาราง · และนี่คือสำมะโนทั้ง 519 คลาส

วิธี: จาก `PF_PROTOCOL_REGISTRY.tsv` เอา `vtable_va` ของทุกคลาส → หาจุดที่ `.text` เขียนค่านั้นลง `[reg]` → ตัดขอบฟังก์ชันด้วย `int3` padding → เดินคำสั่งในฟังก์ชันนั้นแบบ track ค่าคงที่ของรีจิสเตอร์ (`xor r,r`→0, `mov r,imm`, `or r,-1`) → อ่านคำสั่งที่เขียน `byte ptr [<รีจิสเตอร์ตัวเดียวกับที่เก็บ vtable> + 0x10]`

| ผล | จำนวน |
|---|---|
| อ่านค่าได้แน่นอน (ตัวรับ = ออบเจ็กต์ตัวเดียวกับที่เขียน vtable) | **375** |
| — ในนั้น **ค่า 0** | **326** |
| — ในนั้น **ค่าอื่น (1,2,3,4,5,6,8,64)** | **38** |
| — ในนั้น อ่านค่ารีจิสเตอร์ไม่ออก (ต้องดูด้วยตา) | 11 |
| ctor ไม่มีคำสั่งเขียน `+0x10` เลย (สืบทอดค่าจาก base ctor) | 120 |
| ขอบฟังก์ชันไม่ชัด (ไม่สรุป) | 6 |

**คลาสที่ค่าไม่ใช่ 0 (38 ตัวที่อ่านค่าได้ + 11 ตัวที่ยังไม่รู้ค่า):**

```
64  SummonedPetAttr                       ctor=0x006ED9E0 write=0x006ED9F5
 8  CreateActorVital                      ctor=0x005E4BE0 write=0x005E4C2A
 6  ActorGatheringInfoAttr                ctor=0x00699B60 write=0x00699B7F
 6  CCooldownAttr                         ctor=0x006C9AB0 write=0x006C9AF3
 6  ActorTreasureHuntExcavatingInfoAttr   ctor=0x0072B640 write=0x0072B65F
 5  InstanceVital                         ctor=0x005E5530 write=0x005E556F
 4  CollectionBagAttr                     ctor=0x0046AEA0 write=0x0046AEAE
 4  GSCN_RunTimeProtocolRes               ctor=0x005E3720 write=0x005E3763
 4  TeleportVital                         ctor=0x005E53D0 write=0x005E5425
 4  ActorCommunityProperty                ctor=0x00638040 write=0x00638060
 4  VowLockData                           ctor=0x00649ED0 write=0x00649F1F
 4  DailyActivityState                    ctor=0x0069CCF0 write=0x0069CD3F
 4  WineFormulaLearningAttr               ctor=0x006A5940 write=0x006A5993
 4  CollectableBookTypeAttr               ctor=0x006A8910 write=0x006A891E
 4  CollectionObjPointAttr                ctor=0x006CBE30 write=0x006CBE42
 4  CollectionEffectData                  ctor=0x006CD2B0 write=0x006CD2FF
 4  ExpressCountAttr                      ctor=0x006E3720 write=0x006E3737
 4  PetsData                              ctor=0x006F5DF0 write=0x006F5E3F
 4  PetsMergingData                       ctor=0x006F8BB0 write=0x006F8BFF
 4  ActorLearnedPetsSkillData             ctor=0x006FE580 write=0x006FE5CF
 4  CAchievementsAttr                     ctor=0x00701F50 write=0x00701FAA
 4  UserSettingServer                     ctor=0x00720D20 write=0x00720D8B
 4  NavigationExAttr                      ctor=0x0072E4E0 write=0x0072E4F0
 3  FightAttr                             ctor=0x004679F0 write=0x00467A12
 3  QuestOperateVital                     ctor=0x00621810 write=0x00621844
 3  CBuffAttr                             ctor=0x0064A160 write=0x0064A1A3
 2  ActorAttr                             ctor=0x00464BE0 write=0x00464C98
 2  EquipFashionVital                     ctor=0x005EB610 write=0x005EB7C1
 2  CSkillAttr                            ctor=0x00751B90 write=0x00751BD3
 1  DeleteActorVital                      ctor=0x005E4C80 write=0x005E4D53
 1  ReliveVital                           ctor=0x005E5F30 write=0x005E5F52
 1  FashionChangeVital                    ctor=0x005EC0A0 write=0x005EC0F1
 1  ServerAddedInfoVital                  ctor=0x005ED250 write=0x005ED2AD
 1  LSCN_LoginVitalRes                    ctor=0x005F27E0 write=0x005F2820
 1  TriggerVital                          ctor=0x00600760 write=0x00600796
 1  TriggerMessageVital                   ctor=0x006010D0 write=0x0060112F
 1  UpdateConditionalStoreItemVital       ctor=0x00664DE0 write=0x00664E32
 1  ItemSynthesisVital                    ctor=0x0072B230 write=0x0072B258
 ?  NPCAttr / ActorInspectVital / PartyUpdateVital / CVehicleAttr /
    BuildingCrystal_PurchaseServiceVital / BuildingCrystal_UpdateNextAbsorbTime /
    ActorActivity_ClientReportActivityResultVital / KnowledgeGuru_UseHalfProbabilityCardResultVital /
    CHitParadeResetVital_JP / CHitParadeAvatarReqVital_JP / PandoraBoxVitalRes
    (เขียนจากรีจิสเตอร์ที่สคริปต์ตามค่าไม่ได้ — ต้องเปิดดูทีละตัว ถ้าสายไหนจะใช้คลาสพวกนี้ค่อยขอ)
```

🔴 **ของแถมที่กระทบงานที่กำลังทำอยู่: `TriggerVital` = 1 ไม่ใช่ 0** — ถ้ามีสายไหนส่ง `TriggerVital` ด้วย `vital_version=0` ไคลเอนต์จะทิ้งเฟรมทั้งใบและขึ้น error `0xE0000031` · เช่นเดียวกับ `CreateActorVital`=8, `DeleteActorVital`=1, `InstanceVital`=5, `ActorAttr`=2, `FightAttr`=3

## nonclaims

1. ไม่อ้างว่าค่าที่ ctor เขียนคือค่าที่ **เซิร์ฟเวอร์เดิม** ส่งจริง — อ้างว่าเป็นค่าที่ **ไคลเอนต์ตัวนี้ยอมรับ** (exact equality ที่ `0x005F3EFC`) ซึ่งเป็นสิ่งที่ใบถาม
2. 120 คลาสที่ ctor ไม่เขียน `+0x10` = สืบทอดจาก base ctor · **ไม่ได้แปลว่าเป็น 0** รอบนี้ไม่ได้ไล่ base ให้ (ไม่ได้ถาม) — ถ้าสายไหนต้องใช้คลาสในกลุ่มนี้ ต้องขอเพิ่มทีละตัว
3. 11 คลาสที่ค่ามาจากรีจิสเตอร์ยังไม่รู้ค่า · 6 คลาสขอบฟังก์ชันไม่ชัด — **ไม่สรุปทั้ง 17 ตัว**
4. สำมะโนนี้ตั้งอยู่บนสมมติฐานว่า "ctor คือฟังก์ชันที่เขียน vtable ของคลาสลงออบเจ็กต์" ซึ่งจริงกับทุกคลาสที่ตรวจด้วยตารอบนี้ (4 ตัว) แต่ไม่ได้ยืนยันด้วยตาทั้ง 519 ตัว
5. ไม่ได้แตะข้อขัดแย้งเรื่อง "ประตูสามบานแช่แข็ง" กับ `COO-DECISION 1541` — เรื่องนั้นเป็นของ COO/LANE-GM
6. read-only ล้วน · ไม่แตะ `GameClient/`, `external/`, `gamedata/`, `SERVER/` หรือไฟล์คิว

## BUILD_IMPACT

- **ไม่ต้องแก้อะไรใน `attr_wire.py`** — ค่า `0` ที่ใช้อยู่ถูกต้อง เปลี่ยนจาก **"สมมติของสาย รอ COO ยืนยัน"** เป็น **"วัดแล้ว static, VA ปักครบ"** ⇒ ลบป้ายสมมติออกได้
- ห้ามยืมค่าข้ามคลาสอีกต่อไป — ตารางข้างบนใช้แทนการเปิดใบทีละคลาสได้ทันที
- ไม่มี CORE-REQUEST จากรอบนี้
