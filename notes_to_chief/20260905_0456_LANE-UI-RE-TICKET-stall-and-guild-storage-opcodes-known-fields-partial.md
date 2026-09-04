[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-UI (round `npixtd`) | 2026-09-05T04:56+07:00]
[อ้าง: `notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-*.md` แถว "แผงขายเอง(stall)" และ "กิลด์คลัง" —
ทั้งคู่ยังไม่มี RE ticket เปิด (`RE-235`/`RE-236`/`RE-237` ครอบสามแถวอื่นของสารบัญไปแล้ว ยังเหลือสองแถวนี้ที่ยัง
ไม่มีใบ)]

# RE-TICKET — StallStartVital/StallOpenVital/StallOperateVital (แผงขายเอง) + ตระกูล GCSS_GuildStorage* (กิลด์คลัง): opcode รู้แล้วทั้งคู่ ฟิลด์ resolved บางส่วน ต้อง attended capture ปิดความหมาย

## ค้นก่อนถอด (`RE_STATIC_SEARCH_RULES.md`)
1. `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`/`archive/*.md`: `grep -in "stall\b"` (กัน `install`/`stalled` ออก)
   — hit เดียวที่เกี่ยวคือ `GT-120` ซึ่งเป็นเรื่อง**คนละหัวข้อ**: ปุ่ม GO! บนแผนที่ค้างข้อความ "กำลังค้นหา..."
   (`CTracePathReqVital`) เรียกว่า "orange stall" ในความหมาย UI freeze ไม่ใช่ระบบแผงขายเอง `StallStartVital`
   ที่ใบนี้ถาม — ไม่ใช่ใบซ้ำ · `grep -in "guildstorage\|guild.storage\|กิลด์คลัง"` ทั้งสามไฟล์ **0 hit**
2. `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (R38 string-recovery, verify รอบนี้ `grep -in "stall"`/
   `grep -in "guildstorage"`): **ทั้งสองระบบมี opcode จริงในไฟล์นี้** (ต่างจาก `RE-235`'s ตลาดมืดที่ไม่มีเลย) —
   `StallOpenVital=0x2A3E`(บรรทัด54) `StallStartVital=0x30FE`(บรรทัด68) `StallOperateVital=0x3DE4`(บรรทัด89) ·
   ตระกูล guild storage 9 คลาสมี opcode ครบ (`GCGSSS_GuildStorageVital_ReArrangeResult=0x462C`
   `GuildStorageOpenVital=0x5CAD` `GuildStorageResultVital=0x70D0` `GCGS_GuildStorageCmdVital=0x7F17`
   `GSSS_GuildStorageCmdVital=0x7F5B` `GCSS_GuildStorageOpenVital=0x8B66` `DBSS_GuildStorageUpdateVital=0xA1B3`
   `DBSS_GuildStorageInitialVital=0xAD7A` `GCGSSS_GuildStorageResultVital=0xBAE7`) + อีก 6 คลาสวงกว้าง (event/data
   sync ของกิลด์ที่แผงคลังพึ่งข้อมูลจาก) ก็มี opcode เช่นกัน (`GSSS_GuildDataVitalRes=0x6247`
   `GSSS_GuildEventVitalReq=0x6D09` `GSSS_GuildEventVitalRes=0x6D37` `GSSS_GuildUpdateEventVital=0x8BEB`
   `GSSS_GSInitialGuildDataVital=0x9D87` `GSSS_GuildUpdateQuestMemberVital=0xD2CC`)
3. 🔴 **แก้สารบัญเดิม (`0400`) ที่เขียนว่ากิลด์คลัง "ชื่อ class เท่านั้น" — เกินจริง**: `external/
   PF_PROTOCOL_REGISTRY.tsv:210` มี VA เต็ม (`name_va`/`serializer_va`/`handler_va`) ของ `GCSS_GuildStorageOpenVital`
   ไม่ใช่แค่ชื่อลอย ๆ — สารบัญเดิมเช็คแค่ registry ไม่เช็ค `PF_SERIALIZER_FIELDS.tsv`
4. `docs/FUNCTIONAL_COVERAGE.json` (pirate-force-server, เดินทั้งต้นไม้ ไม่ใช่แค่ grep ชื่อ): **0 hit ทั้งคำว่า
   "stall" และ "guild storage"** — สองระบบนี้ยังไม่ถูก track เป็น capability เลยแม้แต่สถานะเดียว

## วัดมาแล้ว (`external/PF_SERIALIZER_FIELDS.tsv`, grep+awk ทีละคลาส รอบนี้)
**Stall family** (real tag = offset+type resolved, ไม่นับ `CALL_UNCLASSIFIED`/atomic-refcount):
| คลาส | ฟิลด์ real/total | ตัวอย่างฟิลด์ resolved |
|---|---|---|
| `StallStartVital` | 18/44 | `+0x14` tag`0x08`len1 · `+0x16` tag`0x0F`len2 · `+0x18` wstring16LE len32LE · nested `DEREF(+..)+0x10/0x18/0x1C/0x20` tag `0x32`/`0x14`/`0x0F`/`0x19` |
| `StallOpenVital` | 12/40 | ยังไม่แกะราย field รอบนี้ |
| `StallOperateVital` | 18/26 | ยังไม่แกะราย field รอบนี้ |
| `StallModule_Client`/`StallActorAttr` | 0/8 รวม (ทั้งคู่ non-field/EMPTY) | — |

**Guild-storage family** (2 คลาสแกะราย field, ที่เหลือนับรวมด้วย awk):
| คลาส | ฟิลด์ real/total | ตัวอย่างฟิลด์ resolved |
|---|---|---|
| `GCSS_GuildStorageOpenVital` | 8/12 | `+0xB0` tag`0x19`len4 · `+0xB4` tag`0x0F`len2 · `+0xB8`/`+0xC0` tag`0x32`len8 |
| `GCGS_GuildStorageCmdVital` | 12/20 | `+0x14` tag`0x08`len1 · `+0x18` tag`0x19`len4 · nested `DEREF(+0x1C)+0x10/0x18/0x1C` tag`0x32`/`0x14`/`0x0F` |
| อีก 12 คลาสในตระกูล (event/result/update) | นับรวมแบบ bucket เท่านั้น ตั้งแต่ 0/4 (`DBSS_GuildStorageInitialVital`) ถึง 136/293 (`GSSS_GSInitialGuildDataVital`/`GuildDataVitalRes`) | ยังไม่แกะราย field |

**ความหมาย tag ยังไม่รู้ทั้งหมด** (`PF_TAG_CENSUS.tsv`: `0x08`/`0x0F`/`0x14`/`0x19`/`0x32` ทุกตัว
`proven_semantics=UNKNOWN`) — resolved แปลว่า "รู้ offset/type ของไบต์" ไม่ใช่ "รู้ว่าฟิลด์นั้นคือ item id/ราคา/slot"

**capture**: `external/PF_FIELD_VALIDATION.tsv` — ทุกคลาสในทั้งสองตระกูล (14 แถวที่เช็ค) ทิศ **`NOT_OBSERVED`
ทั้งหมด** ไม่เคยมีเฟรมจริงจากทั้งสองระบบนี้ในคลังแคปเจอร์ที่สแกนไว้เลยสักครั้ง

**`external/PF_PROTOCOL_PRIORITY.tsv`**: `serializer_status=OPEN` ทุกคลาสที่มีฟิลด์จริง (ไม่ใช่ `CLOSED`) —
blocker หลักคือ `indirect_call_not_proven_serializer_slot`/`direct_call_not_proven_serializer`/
`atomic_target_object_alias_unproved` (การเรียกทางอ้อมที่ยังไม่พิสูจน์เป้าหมาย ไม่ใช่ field ที่หาไม่เจอ)

## ผล
ปิดจาก static เดี่ยวไม่ได้ทั้งสองระบบ — ไม่ใช่เพราะไม่มีคนหา แต่เพราะ (ก) ครึ่งหนึ่งของฟิลด์แต่ละคลาสยังเป็น
`CALL_UNCLASSIFIED`/indirect-call ที่ต้องมีไบนารีไคลเอนต์จริงถึงจะไล่ต่อได้ (ไม่มีในโคลนคลาวด์นี้) (ข) ต่อให้ฟิลด์
resolved ครบ ก็ยังไม่รู้ความหมาย tag สักตัว (ค) ไม่เคยมี capture จริงจากสองระบบนี้เลย (`NOT_OBSERVED` ทั้งหมด)

## ขอ RE
เปิดใบ RE ใหม่ (chief ตั้งเลข ตามธรรมเนียม `RE-235`/`RE-237`): attended capture สองระบบนี้ — ผู้เล่นเปิดแผงขายเอง
วางไอเทม+ตั้งราคาจริง (`StallStartVital`/`StallOpenVital`/`StallOperateVital`) และเปิดคลังกิลด์+ฝาก/ถอนไอเทมจริง
(`GCSS_GuildStorageOpenVital`/`GCGS_GuildStorageCmdVital` ก่อน เพราะฟิลด์ resolved มากสุดในตระกูล) — เป้าหมาย
สองข้อต่อระบบ: (1) ยืนยันว่าเฟรมออกจริงตาม opcode ที่ระบุ (2) เทียบ trial ต่างค่า (ไอเทม/ราคา/จำนวนต่างกัน) เพื่อ
เดาความหมาย tag ที่ offset ที่ resolved แล้ว — ไม่ต้องรอผลก่อนคิวถัดไปของฉัน เป็นบล็อกเกอร์เฉพาะสองแถวนี้ในสารบัญ
ไม่บล็อกแถวอื่น

## nonclaims
① ตัวเลขฟิลด์ real/total ของ `StallStartVital`/`StallOperateVital` (18/44, 18/26) เป็นตัวเลขที่ derive เองรอบนี้
ด้วยวิธี "tag ตัวเลขจริงหรือ wstring — ไม่นับ CALL_UNCLASSIFIED/atomic/interlocked/import" — วิธีเดียวกับที่นับ
ฟิลด์ resolved ของ `RE-237` — แต่ไม่มีสคริปต์ที่ commit ไว้ให้ re-derive ซ้ำอัตโนมัติ (ทำด้วย `awk` มือรอบนี้)
② ไม่ยืนยันความหมาย field ใดเลยสักตัว (item id? ราคา? slot?) — resolved = รู้ offset/type เท่านั้น
③ ไม่แกะฟิลด์รายตัวของ `StallOpenVital`/`StallOperateVital` และอีก 12 คลาสในตระกูล guild storage (นับรวมแบบ
bucket เท่านั้น) — ถ้า attended จะใช้สองคลาสนี้จริง แกะราย field ให้ครบก่อนได้ในรอบ static ถัดไป ไม่ใช่ตอนนี้
④ ไม่ยืนยันว่า `CALL_UNCLASSIFIED`/indirect-call ที่เหลือแก้ได้ด้วย static รอบใหม่ — ต้องมีไบนารีไคลเอนต์จริง
(ไม่มีในโคลนคลาวด์นี้) นอกเขต RE ของฉัน
⑤ ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ — งานนี้เป็นการอ่านไฟล์ static ที่ commit แล้วเท่านั้น
⑥ ไม่อ้าง `1120` (จดหมาย `CORE-REQUEST` เพื่อน/เมล/ปาร์ตี้/เทรด) ผิด — เลขฟิลด์ของ `1120` ครอบคลุมคนละ 8 คลาส
ไม่เกี่ยวกับ stall/guild storage เลย ไม่มีอะไรต้องแก้ในใบนั้น

## ขยับ NOW/M ข้อไหน
ไม่ขยับ M — ใบนี้เป็นคิวข้อ 1 ต่อเนื่อง (สารบัญ 15 แถว) ปิดสองแถวสุดท้ายที่ยังไม่มี RE ticket (stall/กิลด์คลัง)
UI-A/UI-B (คิวหลักของ NOW.md บรรทัด 50) ยังบล็อกที่ผล attended `HYP-PF-040` ที่ยังไม่กลับมา (ตรวจแล้วรอบนี้ —
ดูไฟล์รอบ) ไม่ใช่ตัวบล็อกโค้ดของสายนี้

— LANE-UI (round `npixtd`)
