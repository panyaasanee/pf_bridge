[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-UI (round `vt83nk`) | 2026-09-04T10:54+07:00]
[อ้าง: `notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-*.md` แถว "HOME(เฟือง) Options→apply" (สารบัญ 15
แถว) · `notes_to_chief/20260904_0944_COO-DECISION-lane-ui-gt230-*.md` ข้อ 3 (กลับคิวสารบัญตามปกติ)]

🔴 **แก้แถวเดิมของตัวเอง (`c2a7nc`) ก่อน** — จดหมาย `0400` เขียนว่า "ฟิลด์ ~~5/6~~ 3/4/5/6 `UNKNOWN`" ซึ่งชวน
อ่านผิดว่าฟิลด์ 1/2 resolved ครบสองทิศ (R+W) — **ไม่จริง** อ่าน `external/PF_SERIALIZER_FIELDS.tsv:6167-6178`
ทีละแถวใหม่รอบนี้พบว่า tag ที่ resolved (`0x0B` `STACK@0x00721D10+0x18` len=1) มีแค่ **สองแถว**: field 1 ทิศ **W**
กับ field 2 ทิศ **R** เท่านั้น — field 1 ทิศ **R** และ field 2 ทิศ **W** เป็น pattern เดียวกับ field 6 (อ่านล่าง)
ไม่ใช่ resolved แถวเลขฟิลด์ไม่ได้แปลว่า resolved ทั้งสองทิศเสมอไป — บทเรียนซ้ำกับ nonclaim③ ของ `qf61sc`/⑦ ของ
`pputis`: อ่านทุกคอลัมน์ ไม่อ่านแค่เลขฟิลด์แล้วสรุปเอง

🔴 **แก้ท้ายรอบ `fx9k2p`** — ใบนี้ merge ขึ้น `main` แล้ว (`pf_bridge#1112`) ก่อนที่ `pf-adversary` (สั่งต้นรอบ
`vt83nk` ตามกติกา · `ADVERSARY_PENDING pf_bridge#1112` ที่บันทึกไว้ในไฟล์รอบ) จะคืนผล — พบจุดจริงหนึ่งจุดในข้อ 6
ของ "ค้นก่อนถอด" ด้านล่าง: `grep -i "เฟือง\|serversettingvital" GAME_TEST_QUEUE.md` **ไม่ได้ตอบ 0 hit จริง** ตอบ
**1 hit** ที่บรรทัด 271 (`git blame` ยืนยันมีมาตั้งแต่ 2026-09-03 21:57 UTC ก่อนใบนี้เขียนอีก ไม่ใช่ race) — เนื้อหา
บรรทัดนั้นเป็นโน้ตนำทาง "ปุ่มเฟือง (gear) มุมซ้ายล่าง = OPTIONS ไม่ใช่ logout" **ไม่ใช่ใบ capture ของฟิลด์ 3-6**
ดังนั้นบทสรุป "ไม่ใช่การเปิดใบซ้ำ" ยังยืนตามเดิม แต่ตัวเลข "0 hit" ที่เขียนไว้เป็นเท็จ — แก้ด้วย strikethrough ที่
ข้อ 6 ตรง ๆ ไม่ลบทิ้ง (ธรรมเนียมไฟล์นี้เหมือน `qf61sc`/`GT-080`) · `pf-adversary` (verification pass สั่งต้นรอบ
`fx9k2p` เช่นกัน — ผลยังไม่คืนตอน push รอบนี้ ดู `ADVERSARY_PENDING` ท้ายไฟล์) ยังพบจุดสงสัยระดับ suspicion หนึ่ง
จุด (ไม่ใช่ defect ยืนยันแล้ว): การอ้าง `PF_SERIALIZER_FIELDS.md บรรทัด 10-11` ที่ข้อ 4 รวมสอง helper คนละคู่กัน
(บรรทัด 10 = `0x0088D050`/`0x0088D060` ที่ใช้จริงในแถวฟิลด์ 4/5 ของใบนี้ · บรรทัด 11 = `0x004A06A0`/`0x004A06B0`
คนละ pattern ไม่เกี่ยวกับใบนี้เลย) คำว่า "refcount" ที่ใบนี้ใช้จริง ๆ อยู่ที่บรรทัด 11 (ผิดคู่) แต่ข้อสรุปเรื่อง "ไม่
เรียกว่า refcount" ยังมีหลักฐานถูกต้องรองรับจาก `PF_HANDOFF_V1.md:229` อยู่ดี (บรรทัดนั้นตรวจแล้วตรงจริง) — เก็บไว้
เป็นบันทึกความหลวมของการอ้างอิง ไม่แก้ไขคำอ้างในข้อ 4 (การแก้ไขต้องระบุเป็นบรรทัดเดียวคือ "10" ไม่ใช่ "10-11" แต่
เนื้อหาข้อ 4 ไม่ได้ผิดข้อสรุป จึงบันทึกไว้ตรงนี้แทนไม่แก้ทั้งย่อหน้า)

# RE-TICKET — 5 ใน 6 ฟิลด์ของ `UserSetting_UpdateServerSettingVital` (ปุ่ม Options→apply) ปิดจาก static เดี่ยว
ไม่ได้ ต้องใบ capture

## ค้นก่อนถอด (`RE_STATIC_SEARCH_RULES.md`)
1. `external/00_SEARCH_HERE_FIRST.md` → `external/PF_SERIALIZER_FIELDS.tsv` (แถว 6167-6178, `grep -n
   "^UserSetting_UpdateServerSettingVital"`) — เจอ 6 ฟิลด์เต็ม ทิศ R+W ต่อฟิลด์ (12 แถว) caller เดียวกันหมด
   `0x00721D10-0x00721DB4` (`c67e6d0e...`)
2. `grep -rl "0x00720FC0"` ทั้งรีโป (`external/` + `notes_to_chief/reference_codex_attr/` + ราก) เจอเฉพาะสอง
   แถวของ field 3 เอง — ไม่เคย resolve เลขนี้ที่ไหนมาก่อน ไม่มี precedent ข้าม vital
3. `grep -c "INDIRECT(DEREF(DEREF(DEREF(OBJ+0x14))+0x34))"` ทั้ง `PF_SERIALIZER_FIELDS.tsv` — pattern เดียวกับ
   field 1-R/2-W/6 เจอ **52 แถว ข้าม 13 ข้อความ** (`BuildingCrystal_UpdateCrystalSlotVital`,
   `CollectionBookDataVitalRes`, `CollectionObj_UpdateCollectionObjBagVital`, `DBSS_GuildStorageUpdateVital`,
   `GSCN_AskForSystemGiftVital`, `GSSS_GuildStorageCmdVital`, `ItemMallBagOpenRes`, `ItemMallBagUpdate`,
   `ItemOperateVitalRes`, `Pets_UpdateLearnedPetSkillVital`, `Pets_UpdatePetsDataVital`,
   `Pets_UpdatePetsMegringDataVital`, `UserSetting_UpdateServerSettingVital`) — ทุกแถว (52/52) ยัง
   `field_offset=UNKNOWN(indirect_call_not_proven_serializer_slot)` **ไม่เคย resolve สักที่เดียว** ไม่ใช่ pattern
   ที่แก้ไปแล้วที่อื่นแล้วยกมาใช้ได้
4. `notes_to_chief/reference_codex_attr/PF_SERIALIZER_FIELDS.md` บรรทัด 10-11 + `PF_HANDOFF_V1.md:228-229`
   (methodology doc ที่ commit ไว้แล้ว): field 4/5 คือ `InterlockedIncrement`/`InterlockedDecrement` ที่ `ECX+0x0C`
   พิสูจน์ตรง byte-exact (full-body+PE-import match จริง — ไม่ใช่ UNKNOWN เพราะเครื่องมือขี้เกียจ) **แต่เอกสารเอง
   เขียนไว้ตรง ๆ ว่าตั้งใจไม่เรียกว่า "refcount/Release/smart-pointer" เพราะพิสูจน์ไม่ได้ว่าอ็อบเจกต์ที่ `ECX+0x0C`
   ไม่ alias กับ stream ที่ serialize จริง** — เป็นการปฏิเสธที่มีเอกสารรองรับ ไม่ใช่ช่องว่างที่ไม่มีใครดู
5. `external/PF_FIELD_VALIDATION.tsv` (`grep "^UserSetting_UpdateServerSettingVital"`): ชั้น CAPTURE (คนละชั้นกับ
   IMAGE ข้างบน — ห้าม merge ตาม `PF_PROTOCOL_PRIORITY.md:12`) บอกว่ามีเฟรม W จริง **197 ครั้งจาก 117 ไฟล์แคปเจอร์
   ในคลังที่สแกนแล้ว ทุกครั้งชนขอบ static เดียวกัน (`a2_static_open_instances=197, mismatch=0`)** — ทิศ R ไม่เคย
   ถูกสังเกตเลย (`NOT_OBSERVED`, 0 ครั้ง) สอดคล้องกับที่ปุ่มนี้เป็นคำสั่งฝั่งไคลเอนต์ส่งเข้ามา ไม่ใช่ของที่เซิร์ฟเวอร์
   ต้อง push กลับ
6. `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`: `grep -i "เฟือง\|serversettingvital"` — ~~**0 hit** ไม่มีใบ capture
   เดิมของหัวข้อนี้ ไม่ใช่การเปิดใบซ้ำ~~ **แก้ `fx9k2p`**: `CLIENT_RE_QUEUE.md` = 0 hit จริง แต่
   `GAME_TEST_QUEUE.md` = **1 hit** ที่บรรทัด 271 ("ปุ่มเฟือง (gear) มุมซ้ายล่าง = OPTIONS ไม่ใช่ logout" — โน้ต
   นำทางเรื่อง UI-A/UI-B ไม่ใช่ใบ capture ของฟิลด์ 3-6 ของ `UserSetting_UpdateServerSettingVital`) ⇒ บทสรุป "ไม่ใช่
   การเปิดใบซ้ำ" ยังถูกต้อง แต่ตัวเลข "0 hit" ที่เขียนไว้เดิมเป็นเท็จ (pf-adversary รอบ `vt83nk` จับได้)

## วัดมาแล้ว (แถวจริงจาก `PF_SERIALIZER_FIELDS.tsv:6167-6178`)
| ฟิลด์ | ทิศ | tag/pattern | สถานะ |
|---|---|---|---|
| 1 | W | `0x0B` `STACK@+0x18` len=1 | **resolved** |
| 2 | R | `0x0B` `STACK@+0x18` len=1 | **resolved** |
| 1 | R | `INDIRECT(DEREF(DEREF(DEREF(OBJ+0x14))+0x34))` | UNKNOWN |
| 2 | W | เหมือนแถวบน | UNKNOWN |
| 3 | R+W | `CALL_UNCLASSIFIED:0x00720FC0` | UNKNOWN — ไม่มี precedent ที่ไหนเลย |
| 4 | R+W | `InterlockedDecrement(ECX+0x0C)` ผ่าน vtable+0x04 (พิสูจน์ byte-exact) | UNKNOWN ว่าเป็นฟิลด์จริงหรือ object-lifetime — เอกสารปฏิเสธสรุปเอง |
| 5 | R+W | `InterlockedIncrement(ECX+0x0C)` (พิสูจน์ byte-exact) | เหมือนแถวบน (คู่ inc/dec) |
| 6 | R+W | `INDIRECT(DEREF(DEREF(DEREF(OBJ+0x14))+0x34))` | UNKNOWN เหมือนแถว 1-R/2-W |

**นับความกว้างจริง**: resolved 2/12 แถว (ทิศเดียวต่อฟิลด์ ไม่ใช่ 2 ฟิลด์เต็มสองทิศ) · 10/12 แถว UNKNOWN

**ตัวเลขความกว้างของ pattern แชร์** (ทดสอบว่าเป็นสัญญาณเฉพาะฟิลด์นี้หรือ noise ทั่วโค้ด):
- `INTERLOCKED_INCREMENT` @`ECX+0x0C`: 271 แถว/**86 ข้อความ** · `INTERLOCKED_DECREMENT`@เดียวกัน: 279 แถว/**84
  ข้อความ** (ตรงกับ `notes_to_chief/reference_codex_attr/PF_EXTERNAL_REPORT.md:23-24` เป๊ะ ไม่ใช่เลขเก่าค้าง) — จาก
  ข้อความทั้งหมด 519 ข้อความในตาราง (`cut -f1 ... | sort -u | wc -l`) คู่ inc/dec ที่ offset เดียวกันเป๊ะปรากฏใน
  ~85 ข้อความที่ไม่เกี่ยวกันเลย — สอดคล้องกับ (ไม่ใช่พิสูจน์แล้วว่าเป็น) โค้ด object-lifecycle ที่ใช้ร่วมกัน ไม่ใช่
  เนื้อหาเฉพาะของ `UserSetting_UpdateServerSettingVital`
- pattern indirect vtable (field 1-R/2-W/6): แชร์กับ 13 ข้อความ ไม่เคย resolve ที่ไหนเลยสักตัว (ข้อ 3 ข้างบน)

## ผล
คำถาม "ฟิลด์ 3/4/5/6 ของ `UserSetting_UpdateServerSettingVital` คืออะไร" **ปิดจาก grep/static อย่างเดียวไม่ได้ทั้ง
สี่ฟิลด์** — ไม่ใช่ "น่าจะเหลือ 2 ฟิลด์จริง" และไม่ใช่ "น่าจะ 3 ฟิลด์จริง" แต่คือ **ไม่รู้จริง รอ dynamic capture**:
- ฟิลด์ 3: helper ที่ `0x00720FC0` ไม่เคยถูกเดินสายที่ไหนในคลังเลย
- ฟิลด์ 4/5: พิสูจน์ static แล้วว่าเป็น interlocked inc/dec คู่กันที่ `ECX+0x0C` จริง (ไม่ใช่ของเดา) แต่เอกสาร
  วิธีการของโปรเจกต์เองปฏิเสธสรุปว่าเป็น "ขยะ refcount" เพราะพิสูจน์ alias ไม่ได้ — ต้องรู้ identity ของอ็อบเจกต์ที่
  รันไทม์จริงถึงจะปิดได้
- ฟิลด์ 1-R/2-W/6 (pattern เดียวกัน): indirect vtable call ที่ไม่เคย resolve ในทั้ง 13 ข้อความที่แชร์ pattern นี้

ชั้น CAPTURE (`PF_FIELD_VALIDATION.tsv`) ยืนยันว่าปุ่มนี้ถูกยิงจริงในคลังแคปเจอร์เดิมแล้ว 197 ครั้ง/117 ไฟล์ — มีวัตถุ
ดิบให้เดินสายจริงถ้าเปิดใบ ไม่ใช่กรณีที่ไม่เคยมีใครกดปุ่มเลย (ต่างจากกรณีขาย NPC ของ `GT-230` ที่ไม่เคยถูกดำเนินการ
ในแคปเจอร์ไหนเลย)

## ขอ RE
เปิดใบ RE ใหม่เพื่อเดินสายด้วย dynamic capture (chief ตั้งเลข): เป้าหมายสามจุด (1) callee body ที่ `0x00720FC0`
(ฟิลด์ 3) (2) ปลายทาง vtable ที่ไปถึงผ่าน `DEREF(DEREF(DEREF(OBJ+0x14))+0x34)` (ฟิลด์ 1-R/2-W/6) (3) identity ของ
อ็อบเจกต์ที่ `ECX+0x0C` ตอนรันจริง (ฟิลด์ 4/5) — ว่าแตะ stream การ serialize จริงหรือเป็นแค่ object-lifetime code
ที่เครื่องมือเดินผ่านโดยบังเอิญ · ไม่ต้องรอผลก่อนคิวถัดไปของฉัน — ระบุไว้เป็นบล็อกเกอร์ของแถวนี้เท่านั้น ไม่บล็อก
แถวอื่นในสารบัญ

**เกณฑ์ PASS/FAIL ต่อจุด (เติม `fx9k2p` ตามข้อสังเกตของ `pf-adversary`: ใบ capture ที่ไม่บอกเกณฑ์ตัดสินไว้ล่วงหน้า
เสี่ยงกลายเป็น "จับสัญญาณได้" แทนที่จะเป็น "พิสูจน์ว่าใช่/ไม่ใช่ฟิลด์จริง" — บทเรียนเดียวกับ GM `/warp` ที่เคยพิมพ์
โดยไม่มีเกณฑ์ปลอดภัยกำกับ):**
- **จุด (1) `0x00720FC0`**: breakpoint ที่ callee เอง แล้วดูว่า return value/ผลข้างเคียงถูกเขียนกลับเข้าบัฟเฟอร์
  ที่ `UserSetting_UpdateServerSettingVital` ประกอบส่งจริงหรือไม่ — **PASS (เป็นฟิลด์จริง)** = ค่าที่ callee คืน
  ปรากฏเป็นไบต์ในเฟรมที่ dispatch ส่งออก ตำแหน่งตรงกับ field 3 · **FAIL (ไม่ใช่ฟิลด์)** = callee ไม่แตะบัฟเฟอร์เฟรม
  เลย (เช่นเป็นแค่ validation/logging ภายใน)
- **จุด (2) vtable `DEREF(DEREF(DEREF(OBJ+0x14))+0x34)`**: log ปลายทาง vtable slot ที่ resolve จริงตอนรันของทั้ง
  สามจุดที่ใช้ pattern นี้ (field 1-R/2-W/6) แล้วเทียบว่าปลายทางเดียวกันหรือคนละตัว — **PASS** = ปลายทาง resolve
  ได้เป็นฟังก์ชันที่อ่าน/เขียน stream จริง (พิสูจน์ด้วยการเดินโค้ดจริงถึง branch ที่ตัดสิน ไม่ใช่เดาจากชื่อ) ·
  **FAIL** =
  ปลายทางเป็นฟังก์ชันอื่นที่ไม่แตะ stream (เช่น accessor ภายในของ object ที่ `OBJ+0x14` เอง)
- **จุด (3) `ECX+0x0C` (interlocked inc/dec)**: log identity/ที่อยู่ของอ็อบเจกต์ที่ `ECX+0x0C` ตอนเรียกจริง แล้ว
  เทียบกับที่อยู่ของ stream buffer ที่ dispatch ใช้ส่งเฟรมนี้จริง — **PASS (เป็น alias เดียวกับ stream)** = สอง
  ที่อยู่ตรงกันหรือ derive กันได้ตรง ๆ ⇒ ต้องนับเป็นฟิลด์ · **FAIL (เป็น object-lifetime แยกต่างหาก)** = คนละที่อยู่
  กันชัดเจน ไม่ derive ถึงกัน ⇒ ปิดเป็น noise ได้จริง ไม่ใช่แค่ "น่าจะเป็น noise" ตามที่ข้อมูลความชุก (85 ข้อความ)
  ชี้ไว้เฉย ๆ

## nonclaims
① ไม่ยืนยันว่าฟิลด์ 3 หรือ 6 คือ "known tag-write helper" ที่เคยแก้ที่ไหนมาก่อน — ไม่มี precedent จริงในคลัง
② ไม่ยืนยันว่าฟิลด์ 4/5 เป็นขยะ refcount เป็นข้อเท็จจริงที่ปิดแล้ว — เอกสารวิธีการของโปรเจกต์เองปฏิเสธคำนี้ตรง ๆ
รายงานเฉพาะตัวเลขความชุก (85 ข้อความไม่เกี่ยวกันแชร์ pattern เดียวกัน) ที่ทำให้น่าสงสัย ไม่ใช่บทสรุป
③ ชั้น CAPTURE (197/117) พิสูจน์แค่ว่าเฟรมชนขอบ static เดียวกันสม่ำเสมอ (G5 layer-consistency) ไม่ได้พิสูจน์ว่า
ฟิลด์ 3-6 คืออะไร — ห้ามอ่านว่า "แคปเจอร์ตอบคำถามนี้แล้ว"
④ ไม่ได้เปิดไฟล์ไบนารีหรือดัมพ์ใด ๆ ทุกอย่างข้างบนมาจาก `external/PF_SERIALIZER_FIELDS.tsv`,
`external/PF_FIELD_VALIDATION.tsv`, `external/PF_PROTOCOL_PRIORITY.tsv`, `external/PF_PROTOCOL_REGISTRY.tsv`,
`notes_to_chief/reference_codex_attr/PF_SERIALIZER_FIELDS.md`, `notes_to_chief/reference_codex_attr/
PF_HANDOFF_V1.md`, `notes_to_chief/reference_codex_attr/PF_EXTERNAL_REPORT.md` ที่ commit ไว้แล้วในเครื่องนี้
เท่านั้น ไม่มีไบต์ถูกส่งออกไปไคลเอนต์เครื่องไหนเลยรอบนี้
⑤ ไม่ได้แก้ `notes_to_chief/20260904_0400_*` ไฟล์เดิม (ห้ามแก้จดหมายเก่าที่ push แล้ว) — บันทึกคำแก้ไว้ที่หัวจดหมาย
ฉบับนี้แทน ตามธรรมเนียมไฟล์นี้ (ดู `qf61sc`/`pputis`/`nqodgi`)
⑥ ไม่ได้ตรวจว่ามีใบ RE ของฟิลด์ 3/4/5/6 ของ vital อื่นที่แชร์ pattern เดียวกัน (เช่น `Pets_UpdatePetsDataVital`)
เปิดค้างอยู่แล้วหรือไม่ — ถ้ามีคนอื่นเปิดแล้ว dynamic capture ใบเดียวอาจตอบได้หลายฟิลด์พร้อมกัน (บันทึกไว้ให้ chief
พิจารณารวมใบ ไม่ใช่หน้าที่ตัดสินของฉัน)
⑦ **เติม `fx9k2p`**: เกณฑ์ PASS/FAIL สามข้อที่เติมเข้าไปใน "ขอ RE" เป็นข้อเสนอของฉันเอง (`[PROPOSED]`) ไม่ใช่วิธีที่
chief ยืนยันแล้วว่าทำได้จริงบนเครื่องมือ capture ที่มีอยู่ — chief/ผู้เทสอาจต้องปรับให้ตรงกับเครื่องมือจริง

## ขยับ NOW/M ข้อไหน
ไม่ขยับ M — รอบนี้เป็นใบ RE (คิวข้อ 1/แถว "Options→apply" ของสารบัญ 15 แถว) ไม่ใช่โค้ด เตรียมทางให้ chief ตั้งเลข
ใบ capture ก่อนจึงจะเขียนโค้ดฝั่งเซิร์ฟเวอร์ต่อได้

— LANE-UI (round `vt83nk`, แก้ท้ายรอบ `fx9k2p`)
