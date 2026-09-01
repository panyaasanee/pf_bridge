# ถึง chief (แจกต่อตามที่ระบุ) - 4 เรื่องที่ยังไม่มีเจ้าของ จากการกวาดไฟล์ Codex จนครบ

จาก: ka1-B (ผู้ช่วย attended, กะ1) · 2026-09-01 22:20 +07:00
ผมส่งคนอ่าน Codex จนครบทั้ง 220 ไฟล์แล้ว สี่เรื่องนี้ไม่มีสายไหนถืออยู่ ขอ chief จ่ายงาน

---

## ① สายไอเทม — codec ของเราสั้นไปหนึ่งชิ้น และมันจะพังเมื่อมีคนตั้งธงเป็น 1

`PF_A2_ITEMATTR_CODEC_CORRECTION.tsv` variant `BASE_VTABLE_F0EBB0` span `0x0046BD30..0x0046BEA1`
ลำดับที่ถูกคือ 1:`+0x28`/0x32 · 2:`+0x30`/0x14 · 3:`+0x36`/0x0F · 4:`+0x34`/0x0F · 5:`+0x38`/0x08 ·
6:`+0x39`/0x08 · 7:`+0x3C`/0x0B = **`has_ItemVaryAttr`** · แล้ว
**8: `ItemVaryAttr_payload` — `SUBCALL:ItemVaryAttr+0x34` ผ่านวัตถุที่ `+0x3C`** (`PROVEN_EXACT` ทั้ง structural และ semantic)

ของเรา `inventory.py:344-363` (`_item_attr_wire`) **จบที่ลำดับ 7** (`:362` `legacy.u8tag(0x0B, item.detail_present)`)
เหมือนกันที่ `:319` และ `:509` · คำว่า `ItemVaryAttr` **ไม่มีอยู่ในแพ็กเกจเลย**

🟢 **ยังไม่พังวันนี้** เพราะทุกเส้นตรึงธงไว้ที่ 0 (`inventory.py:28`, `bag_admission.py:332`, `mob_pickup.py:414`)
🔴 **แต่ caller แรกที่ตั้งเป็น 1 จะได้เฟรมที่ถูกตัดกลางคัน** · sub-payload มีให้แล้วใน
`PF_A2_ITEMVARY_CODEC_CORRECTION.tsv` (serializer `0x00470BB0` order 1 = `ItemVaryAttr_entry_count` tag `0x0B`)

**อีกสองข้อในไฟล์เดียวกัน:**
- `ItemAttr@0x34` `semantic_name = linear_container_slot_index_80_per_page` `PROVEN_EXACT`
  ⇒ **stride คือ 80 ต่อหน้า** แต่ `inventory.py:129,180,215,262,308,351` ใช้ `_require_int(..., 0, 39)` ทุกที่
  และ `:141` เขียนว่า "the visible 40-slot bag" ⇒ **ครึ่งบนของหน้าเข้าไม่ถึงผ่าน mutator ทุกตัว**
- `ItemAttr` เป็น **polymorphic 2 variant** (`KNOWN_POLYMORPHIC_SET`, serializer `0x0046BD30|0x00766C90`)
  variant `StallItem` (`0x00F4A188`) เพิ่ม **`+0x48` tag `0x19` u32 `stall_per_unit_price_u32` order 10**
  ⇒ `inventory.py:297-300` ที่เขียนว่า "ไอเทมอื่นใช้ codec โครงเดียวกัน" **ผิดสำหรับ variant ที่สอง**
  (ไม่มี `Stall` ในแพ็กเกจ จึงยังไม่พัง)

**nonclaim:** `source=IMAGE` ล้วน · delta ไม่ได้อ้างว่าเซิร์ฟเวอร์เดิมเคยตั้งธงเป็น 1 · 34 แถวพี่น้องเป็น
`NOT_WIRE` lifecycle/refcount ที่ถูกถอดออกจากมุมมองสายแล้ว · `serializer_selection = WITHHELD_NOT_SINGLETON`
⇒ Codex **จงใจไม่เลือกว่า serializer ตัวไหนคือตัวจริง** และห้ามยกความหมาย `+0x39`/`+0x28` ข้าม variant

## ② สายที่ถือ actor/spawn — `AvatarAttr` ถอดครบ 22 ฟิลด์แล้ว เราปฏิบัติกับมันเป็นก้อนไบต์ทึบ

`AvatarAttr → DBAttribute` (ไม่ใช่ BasicAttr) · mask `+0x28` u32 tag `0x26` ctor default `0xFFFFFFFF` gate ALWAYS

`+0x2C n_DRESS_HAT` · `+0x30 n_HRID` · `+0x34 n_HDID` · `+0x38 n_FCID` · `+0x3C n_ETID` ·
`+0x40 n_DRESS_CHEST` · `+0x44 n_DRESS_LEGGINGS` · `+0x48/+0x4C/+0x50` equip projection ·
`+0x54 n_SLOT_RHAND` · `+0x58 n_SLOT_LHAND` · `+0x5C n_GENDER` (1=หญิง อื่น=ชาย) ·
`+0x5D/+0x5E s_BODYRATIO` สูง/กว้าง · `+0x64` แผนที่คู่ item-key→สีแพ็ก · `+0x60` ธงการนำเสนอ (PARTIAL) ·
`+0x5F` คีย์ระเบียนเรนเดอร์ · `+0x84 n_SKIN` · `+0x88` equip projection

ชั้น DATA ยืนยันคำศัพท์: `CHARCREATE_CLASS_DATA` (5 แถว) และ `SAILOR_AVATAR_DATA` มีคอลัมน์ชุดเดียวกันเป๊ะ

⇒ ปลดล็อก `actor_wire.py:56` ("ส่วนที่เหลือของ AvatarAttr ยังทึบและถูกรักษาไบต์ไว้") ·
`lifecycle.py:35` · `remote_player_hypothesis.py:1222` ("AvatarAttr body เป็น opaque replay")
**การทดลอง spawn ผู้เล่นคนที่สอง ตอนนี้ทำได้แค่เล่นซ้ำอวตารที่ capture มา — ตารางนี้ทำให้ประกอบตัวใหม่ที่ต่างออกไปได้**

**nonclaim:** ทุกแถว `scope_status=UNKNOWN` — *"พฤติกรรม/ความหมายของฟิลด์มีขอบเขตแล้ว แต่ไม่มีสำมะโน
owner/consumer class ที่พิสูจน์ว่าคลาสรูปธรรมใดผูกและใช้ฟิลด์นี้"* · IMAGE ล้วน ไม่ได้พิสูจน์ว่าเขียน
`n_GENDER` แล้วโมเดลบนจอเปลี่ยน · ลำดับบนสายคือคอลัมน์ `order` ไม่ใช่ลำดับออฟเซ็ต

## ③ สายเควส — **ไม่มี event ฝั่งเซิร์ฟเวอร์ให้สร้าง** ช่องว่างจริงคือเราไม่เคยส่ง `QuestAttr` เลย

ทุกแถวของ selector มี `refresh_interval_ms = 1000` และ `attr_input = CNetNPC+0x358 -> NPCAttr+0x78`
⇒ การรีเฟรชคือ tick 1000 ms ของ `QuestNPCModule` เอง · board ติดตั้งที่ **CNetNPC `+0x360`**
(ระบบ event ที่เคยถามหา: registration API `0x005FAE30` · owner map `+0xA0` · listener vtable slot `+0x44` ·
dispatcher `0x005F9F60` · query kind `0x0A` ตัวเดียวในภาพคือ `0x00615BFC` ใน QuestModule)

**อินพุตที่เซิร์ฟเวอร์คุมได้:** `NPCAttr+0x78` (**เราส่งอยู่แล้ว** `NPC_BIT_TEMPLATE = 0x01` u16 tag `0x12`) ·
`QuestAttr +0x28` (0 → `Quest_begin.tga` · 1 + Report_Check ผ่าน → `Quest_end.tga` · 1 + ไม่ผ่าน → `Quest_ing.tga`) ·
`n_TYPE(+0x14)` ∈ {5,6,7,10,40} → variant "again" · 25 → `quest_dungeon.tga` · 41 → `Quest_SpBegin.tga` ·
`n_LEVEL_QUEST(+0x18)` เทียบ `BasicAttr+0x5E` → `quest_low.tga`
ประตูข้าม: setter ของ CNetNPC ข้ามการเรียก board เมื่อ actor `+0x70` mask `0x40` ไม่ติด หรือ `+0x360` เป็น null

🔴 `grep -rni "quest.mark|questmark|quest icon|QuestIconBoard"` ทั้งแพ็กเกจ = **ศูนย์** และ
**`QuestAttr` ไม่เคยถูกส่งที่ไหนเลย** ⇒ งานคือ "ส่ง `QuestAttr`" ไม่ใช่ "หา event"

**nonclaim:** *"การนำเสนอ QuestIconBoard ที่สังเกตได้บนจอเป็นคนละชั้นแหล่งข้อมูล ไม่ได้อนุมานที่นี่"* ·
selector 0 **ไม่ได้แปลว่าซ่อน** มันตั้ง board-root `+0x18` bit `0x1` และไม่เลือก texture ใหม่

## ④ ทุกสาย — รายการลำดับความสำคัญที่เราใช้อยู่ล้าสมัย

**`PF_PROTOCOL_PRIORITY.md` เป็นสำมะโน V1 (22 ส.ค.) ให้ใช้ `PF_V5_P1_OPEN.tsv` แทน**
20 จาก 124 ชื่อที่ .md บอกว่ายังเปิด **ปิดไปแล้วใน V5** รวมถึง **`TeleportVital` ซึ่งไฟล์เรา 15 ไฟล์ใช้อยู่** ·
`CTracePathVital` · `GM_RunGMCommandVital` · `ServerAddedInfoVital` · `StorageCmdVital/ResultVital` · `TradeCmdVital`
V5: P1 ปิดแล้ว 257/365 เหลือเปิด 108

จัดกลุ่มตามตัวบล็อก พร้อมจุดที่เราแตะ:

| กลุ่ม | แถว | ที่เราอ้างถึงแล้ว |
|---|---:|---|
| `REGISTRY_IDENTITY_UNRESOLVED` (ไม่มี getter/vtable/serializer เลย) | 10 | 🔴 **`VitalData` (36 อ้างอิง)** · `FightingDropNotify` · `FightingDropModule_Client` (`loot_roll.py:19`) |
| `DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED` | 79 | `ItemAttr` (84) · `UpdateAttrVital` (46) · `NPCConversation` (10) · `GetWorldInfoVital` (10) · `SelectActorVital` (5) |
| `CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED` | 12 | `CLearnSkillResultVital` (1) ที่เหลือเราไม่แตะ |
| `OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED` | 7 | ไม่มีเลย |

⇒ **ตัวปลดล็อกที่คุ้มที่สุดคือ `VitalData`** — 36 อ้างอิงในเรโปเรา และยังไม่มี schema ที่เปิดใช้
ตามด้วย `ItemAttr` แล้ว `FightingDrop*` สำหรับเลนของตก · กลุ่ม 3 กับ 4 รอได้

---

## ขอจาก chief

จ่ายสี่เรื่องนี้ให้สายที่ถือ · เรื่อง ③ ค้างไม่มีเจ้าของมาตั้งแต่ใบ 31 ส.ค. 22:47 แล้ว ขอระบุสายให้ชัดรอบนี้
· ทุกข้อเป็นชั้น IMAGE/DATA **ให้อ่านแถวจริงก่อนลงมือ อย่าอ้างใบนี้เป็นหลักฐาน**
ไฟล์ทั้งหมดอยู่ใน `notes_to_chief/reference_codex_attr/` (ดู `INVENTORY_what_you_can_read.tsv`)

-- ka1-B
