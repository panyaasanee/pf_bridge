[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-UI (round `npixtd`) | 2026-09-05T04:56+07:00]
[อ้าง: `notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-*.md` แถว "แผงขายเอง(stall)" และ "กิลด์คลัง" —
ทั้งคู่ยังไม่มี RE ticket เปิด (`RE-235`/`RE-236`/`RE-237` ครอบสามแถวอื่นของสารบัญไปแล้ว ยังเหลือสองแถวนี้ที่ยัง
ไม่มีใบ)]

# RE-TICKET — StallStartVital/StallOpenVital/StallOperateVital (แผงขายเอง) + ตระกูล GCSS_GuildStorage* (กิลด์คลัง): opcode รู้แล้วทั้งคู่ ฟิลด์ resolved บางส่วน ต้อง attended capture ปิดความหมาย

## ค้นก่อนถอด (`RE_STATIC_SEARCH_RULES.md`)
1. `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`/`archive/*.md`: `grep -in "stall\b"` (🔴 **แก้ `pf-adversary`
   round `npixtd`**: `\b` ไม่ได้กัน `install` ออกจริงตามที่เขียนไว้เดิม — `install` มี `stall` เป็น substring
   ที่จบพอดีท้ายคำ ⇒ `\b` ยังจับ `install` ได้ ถ้ามีคำนั้นในไฟล์ ผลลัพธ์รอบนี้ยืนตามเดิมเพราะกรองด้วยมือหลัง grep
   แล้ว ไม่ใช่เพราะ `\b`) — hit เดียวที่เกี่ยวคือ `GT-120` ซึ่งเป็นเรื่อง**คนละหัวข้อ**: ปุ่ม GO! บนแผนที่ค้างข้อความ
   "กำลังค้นหา..." (`CTracePathReqVital`) เรียกว่า "orange stall" ในความหมาย UI freeze ไม่ใช่ระบบแผงขายเอง
   `StallStartVital` ที่ใบนี้ถาม — ไม่ใช่ใบซ้ำ · `grep -in "guildstorage\|guild.storage\|กิลด์คลัง"` ทั้งสามไฟล์
   **0 hit** (ข้อนี้ verify ซ้ำแล้ว ยืนตามเดิม)
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
4. 🔴 **แก้ `pf-adversary` round `npixtd`** — `docs/FUNCTIONAL_COVERAGE.json` (pirate-force-server): เดิมข้อนี้
   เขียนว่า "0 hit ทั้งคำว่า stall และ guild storage" — **ผิดครึ่งหนึ่ง**: capability `use_drop_sell`
   (`status=in_progress`, `domains[0].capabilities[9]`) มีฟิลด์ `notes` พูดถึง `StallModule_Client`/
   `StallStartVital`/`StallOpenVital`/`StallOperateVital` ตรง ๆ พร้อม**สมมติฐานความหมายฟิลด์ที่มีอยู่แล้ว**:
   serializer `0x76A630` ของ `StallOperateVital` = `u8 tag 0x08 @+0x14` · `qword tag 0x32 @+0x18` ·
   **`u32 tag 0x14 @+0x20 = price`** · `string @+0x24` — อ้างอิงรายงานเก่า
   `reports/PF_USE_DROP_SELL001_ITEM_OPERATE_USE_DROP_SELL_STATIC_20260818.md` (chief round 75, 2026-08-18)
   ⇒ **นี่คือ static hypothesis ที่มีอยู่แล้ว ไม่ใช่กระดานเปล่า** ต้องยกมาเป็นฐานตั้งต้นของ attended trial ไม่ใช่
   เดาใหม่จากศูนย์ (ดูหัวข้อ "ขอ RE" ที่แก้ด้านล่าง) — grep ชื่อคลาสอย่างเดียวพลาดจุดนี้เพราะอยู่ใน string
   `notes` ไม่ใช่ key/id ระดับบนของ JSON (บทเรียน: "เดินทั้งต้นไม้" ที่เขียนไว้เดิมทำแค่เดิน key ไม่ได้เดินเข้า
   ไปในสตริงยาวของ `notes`) · ครึ่ง "guild storage" ของข้อเดิมยืนถูก — verify ซ้ำ 0 hit จริง (เจอแค่ 2 hit ไม่
   เกี่ยวเรื่อง "guild" ล้วน ไม่มีสักที่พูดถึง storage)

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
| อีก 10 คลาสในตระกูล (event/result/update) | นับรวมแบบ bucket เท่านั้น ตั้งแต่ 0/4 (`DBSS_GuildStorageInitialVital`) ถึง 136/293 (`GSSS_GSInitialGuildDataVital`/`GuildDataVitalRes`) | ยังไม่แกะราย field |
| 🔴 **แก้ `pf-adversary` round `npixtd`**: `GuildStorageOpenVital`(`0x5CAD`)/`GuildStorageResultVital`(`0x70D0`) — ชื่อเปล่า (ไม่มี prefix `GCSS_`/`GCGSSS_`) | **ไม่มีแถวเลยแม้แต่แถวเดียว** ทั้งใน `PF_SERIALIZER_FIELDS.tsv` และ `PF_FIELD_VALIDATION.tsv` (`grep -c "^GuildStorageOpenVital\b"`/`"^GuildStorageResultVital\b"` ทั้งคู่ = 0 ทั้งสองไฟล์ — hit ที่เจอตอน grep แบบไม่ anchor คือ `GCSS_GuildStorageOpenVital`/`GCGSSS_GuildStorageResultVital` คนละคลาสกัน) | สถานะแย่กว่า "0/4 resolved" — คลาสนี้**ไม่ถูก track ในระบบ static เลยแม้แต่แถว UNKNOWN เดียว** มี opcode จาก R38 อย่างเดียว |

**ความหมาย tag ยังไม่รู้ทั้งหมด** (`PF_TAG_CENSUS.tsv`: `0x08`/`0x0F`/`0x14`/`0x19`/`0x32` ทุกตัว
`proven_semantics=UNKNOWN`) — resolved แปลว่า "รู้ offset/type ของไบต์" ไม่ใช่ "รู้ว่าฟิลด์นั้นคือ item id/ราคา/slot"

**capture**: `external/PF_FIELD_VALIDATION.tsv` — ทุกคลาสในทั้งสองตระกูลที่**มีแถวอยู่ในไฟล์นี้จริง** (14 แถวที่
เช็ค) ทิศ **`NOT_OBSERVED` ทั้งหมด** ไม่เคยมีเฟรมจริงจากทั้งสองระบบนี้ในคลังแคปเจอร์ที่สแกนไว้เลยสักครั้ง —
**ยกเว้น** `GuildStorageOpenVital`/`GuildStorageResultVital` (ชื่อเปล่า) ที่ไม่มีแถวในไฟล์นี้เลย (ดูตารางข้างบน)
ซึ่งไม่ใช่ `NOT_OBSERVED` แต่เป็น "ไม่ถูก track" คนละสถานะกัน

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
**ทดสอบสมมติฐานที่มีอยู่แล้ว** ไม่ใช่เดาจากศูนย์: `docs/FUNCTIONAL_COVERAGE.json`'s `use_drop_sell` (chief round
75) เสนอไว้แล้วว่า `StallOperateVital`'s `+0x20` (`u32` tag `0x14`) = **ราคา** — ตั้งราคาคนละค่าข้าม trial แล้ว
เทียบไบต์ที่ offset นั้นก่อนสิ่งอื่น (positive control ที่ง่ายที่สุดของใบนี้) — เดาความหมาย tag ที่เหลือ
(`+0x14`/`+0x18`/`+0xB0` ฯลฯ) ต่อเมื่อ trial แรกยืนยันวิธีนี้ใช้ได้จริง — ไม่ต้องรอผลก่อนคิวถัดไปของฉัน เป็น
บล็อกเกอร์เฉพาะสองแถวนี้ในสารบัญ ไม่บล็อกแถวอื่น

## nonclaims
① ตัวเลขฟิลด์ real/total ของ `StallStartVital`/`StallOperateVital` (18/44, 18/26) เป็นตัวเลขที่ derive เองรอบนี้
ด้วยวิธี "tag ตัวเลขจริงหรือ wstring — ไม่นับ CALL_UNCLASSIFIED/atomic/interlocked/import" — วิธีเดียวกับที่นับ
ฟิลด์ resolved ของ `RE-237` — แต่ไม่มีสคริปต์ที่ commit ไว้ให้ re-derive ซ้ำอัตโนมัติ (ทำด้วย `awk` มือรอบนี้)
② 🔴 **แก้ `pf-adversary` round `npixtd`**: เดิมเขียนว่า "ไม่ยืนยันความหมาย field ใดเลยสักตัว" — เกินจริง
`StallOperateVital`'s `+0x20` มีสมมติฐาน "ราคา" อยู่แล้ว (`use_drop_sell`, chief round 75 — ดูข้อ 4 ของ "ค้นก่อน
ถอด" และหัวข้อ "ขอ RE" ที่แก้ด้านบน) เป็น**สมมติฐานที่ยังไม่ยืนยันด้วย attended** ไม่ใช่ข้อเท็จจริง — ฟิลด์อื่น
ทุกตัว (รวม guild storage ทั้งตระกูล) ยังไม่มีสมมติฐานความหมายใด ๆ เลยจริง
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
