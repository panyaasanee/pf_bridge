# 🔴 อ่านก่อนจะเปิดใบ "ไปขุดข้อมูลเกม" ใด ๆ

> ### 🔴 โฟลเดอร์ไหนเก็บอะไร — กฎตัดสินประโยคเดียว (2026-08-24)
> **ถอดมาจากอิมเมจ `GameClient.local.bin` (โค้ดที่เกม *รัน*) → `pf_bridge\external\`**
> **ถอดมาจากไฟล์ข้อมูลเกม `.pc_` / `.lu_` / `.npc` (เนื้อหาที่เกม *อ่าน*) → `pf_bridge\gamedata\`**
> 🔴 `.pc_` และ `.lu_` ใช้ `$pcz`+LZMA · **`.npc` ไม่ถูกบีบอัด** เป็นไบนารีเปล่า
> โครง: `u16 version` → `u16 **definition_count**` → นิยาม NPC set → `u16 **placement_count**` → เรกคอร์ด `NPCPlacement` (มี XYZ)
> ⚠️ `u16` ตัวที่สอง **ไม่ใช่** placement count (ผู้ช่วยเคยอ่านผิดจุดนี้ 2026-08-24) · placement จริงรวม 6,248 · definition รวม 3,745
> ตัวเลขต่อฉากอ่านจาก `gamedata\PF_GAMEDATA_SCENE_INDEX.tsv`
> เกณฑ์แบ่งบ้านคือ **ถอดมาจากไหน** ไม่ใช่ **บีบอัดด้วยอะไร**
> ⚠️ ชื่อ `external\` บอกว่า *ใครทำ* ไม่ได้บอกว่า *มันคืออะไร* — ชื่อที่ตรงคือ `clientbin\`
> **ห้ามเปลี่ยนชื่อจนกว่า GT-054 จะผ่าน** (`tools\pf_external_registry.py` ฮาร์ดโค้ด `pf_bridge\external` ไว้)


**โฟลเดอร์นี้คือตารางข้อมูลของเกมทั้งหมด แกะออกมาแล้ว — 188 ตาราง · 2,365 คอลัมน์ · จาก 4 ไฟล์ต้นทาง**
ทุกตารางถูก dump เป็น TSV ที่ `tables\<SOURCE>__<TABLE>.tsv` ⇒ **`grep` ได้ตรง ๆ**

## กติกาข้อเดียว

> **ก่อนสั่งให้ใครไปขุดข้อมูลเกม (ไอเทม มอน สกิล อาชีพ ดรอป เควส ข้อความ) — ค้นที่นี่ก่อนเสมอ**
> แล้วเขียนในจดหมายว่า **"ค้น gamedata แล้ว เจอ / ไม่เจอ"**

**ทำไมกฎนี้ถึงเกิด (2026-08-23):** ตัวถอดเดิม `derived\v97_mapping_audit\parse_pc_tables.py`
**พังตั้งแต่ 13 ส.ค.** (`UnicodeDecodeError` ที่ position 120256) ⇒ สารบัญของ CONSTDATA ไม่เคยถูกสร้าง
⇒ ไม่มีใครรู้ว่าข้างในมีอะไร ⇒ ทุกครั้งที่อยากได้ข้อมูล ก็เปิดใบให้คนไปขุดใหม่ทีละครั้ง **ทั้งที่ของอยู่ตรงนี้มา 10 วัน**

---

## แหล่งข้อมูล 4 แหล่ง

| source | ตาราง | ไฟล์ต้นทาง | มีอะไร |
|---|---|---|---|
| `CONSTDATA_TH` | **120** | `B_CONSTDATA_TH.pc_` | ตัวเลขของเกมทั้งหมด — ไอเทม มอน สกิล อาชีพ ดรอป บัฟ เพ็ต |
| `TEXTDATA_TH` | **65** | `B_TEXTDATA_TH.pc_` | ข้อความทั้งเกม — template ระบบ ชื่อไอเทม คำอธิบาย |
| `QUESTDATA_TH` | 2 | `B_QUESTDATA_TH.pc_` | ข้อมูลเควส |
| `QUESTTEXT_TH` | 1 | `B_QUESTTEXT_TH.pc_` | ข้อความเควส |

**สารบัญเต็ม:** `PF_GAMEDATA_INDEX.tsv` (188 แถว) · **คอลัมน์ทุกตัว:** `PF_GAMEDATA_COLUMNS.tsv` (2,365 แถว)

---

## ตารางที่มีค่าที่สุด (เรียงตามเรื่อง)

### อาชีพ / สกิล
```
CONSTDATA_TH__CHARCREATE_CLASS.tsv     5 แถว  x 38 คอลัมน์   n_ID เป็น bitmask: 1,2,4,16,32
CONSTDATA_TH__SKILL_CONTEXT.tsv     2,165 แถว x 20 คอลัมน์   <- ตารางสกิลทั้งเกม
CONSTDATA_TH__CURRICULUM.tsv          137 แถว x  7 คอลัมน์
CONSTDATA_TH__LEVEL_SP.tsv            120 แถว x  2 คอลัมน์
CONSTDATA_TH__BUFF.tsv              9,302 แถว x 14 คอลัมน์
CONSTDATA_TH__STANDARD_BUFF.tsv       256 แถว x 36 คอลัมน์
```
**`SKILL_CONTEXT` มีของที่ต้องใช้ออกแบบเซิร์ฟเวอร์ครบ:**
`n_ID` · `n_LEVEL_LEARN` · `n_PASSIVE` · `n_ISCLASS` (bitmask อาชีพ) · `n_LEVELS` ·
**`f_SP_LEVE1` / `f_SP_LEVEL2PLUS`** (ค่า SP) · **`n_CD`** (คูลดาวน์) · **`n_TARGET`** ·
**`n_STAMINA_COST`** · `n_EQUIPTYPE` · `s_CAST_CONDITION` · `s_CAST_BEHAVIOR`

### ลูท / ดรอป
```
CONSTDATA_TH__DROPS_NORMAL.tsv        267 แถว x 121 คอลัมน์  <- ตารางดรอปหลัก
CONSTDATA_TH__DROPS_SPECIALLY.tsv     584 แถว x  64 คอลัมน์
CONSTDATA_TH__DROPS_EQUIPMENT.tsv      53 แถว x  44 คอลัมน์
CONSTDATA_TH__E_DROPS_QUALITY.tsv      26 แถว x   9 คอลัมน์
```

### ไอเทม / มอน / เพ็ต
```
CONSTDATA_TH__MOBS.tsv              3,210 แถว x 54 คอลัมน์
CONSTDATA_TH__STANDARD_MOB.tsv        255 แถว x 38 คอลัมน์
CONSTDATA_TH__ITEM_MISC.tsv         1,646 แถว x 39 คอลัมน์
CONSTDATA_TH__ITEM_CONSUMABLES.tsv  1,260 แถว x 39 คอลัมน์
CONSTDATA_TH__ITEM_USING.tsv          947 แถว x  9 คอลัมน์
CONSTDATA_TH__ITEM_QUEST.tsv          579 แถว x 38 คอลัมน์
CONSTDATA_TH__PETDATA.tsv             109 แถว x 13 คอลัมน์
```

### ข้อความระบบ (ตัวเชื่อมกับสิ่งที่เห็นบนจอ)
```
TEXTDATA_TH__MESSAGE.tsv              907 แถว x 4 คอลัมน์   <- template ระบบทั้งหมด
TEXTDATA_TH__UI_MESSAGE.tsv         1,954 แถว
TEXTDATA_TH__MOBS_TIP.tsv           3,139 แถว              <- ชื่อมอน
TEXTDATA_TH__ITEM_MISC_TIP.tsv      1,922 แถว              <- ชื่อ/คำอธิบายไอเทม
TEXTDATA_TH__SCENE_NAME_TIP.tsv       330 แถว
```

---

## ท่าค้น

```powershell
cd "C:\Users\Panya\Desktop\Pirate Force\pf_bridge\gamedata"

# ตารางไหนมีคำนี้บ้าง
Select-String -Path PF_GAMEDATA_INDEX.tsv -Pattern "SKILL"

# คอลัมน์ของตารางหนึ่ง
Select-String -Path PF_GAMEDATA_COLUMNS.tsv -Pattern "SKILL_CONTEXT"

# หาข้อความในเกม
Select-String -Path tables\TEXTDATA_TH__MESSAGE.tsv -Pattern "ได้รับ"

# ดูสกิลของอาชีพหนึ่ง (n_ISCLASS เป็น bitmask)
Get-Content tables\CONSTDATA_TH__SKILL_CONTEXT.tsv | Select-Object -First 5
```

**ตัวอย่างผลจริง** — คำถามทั้งใบของ GT-049 ตอบได้ในคำสั่งเดียว:
```
TEXTDATA_TH__MESSAGE.tsv  id 0x83 (131)  col2=1   "ได้รับ [ $V1 ] * $V2"
```

---

## 🔴 สิ่งที่ตารางพวกนี้ **ไม่ได้** บอก

1. **ไม่บอกว่าเซิร์ฟเวอร์ต้นฉบับทำงานยังไง** — นี่คือข้อมูลที่ *ไคลเอนต์* ถืออยู่ **ไม่ใช่กฎของเซิร์ฟเวอร์**
   เซิร์ฟเวอร์ต้นฉบับปิดไปแล้วและกู้ไม่ได้ตลอดกาล ⇒ **ห้ามเขียนว่า "เซิร์ฟเวอร์เดิมทำแบบนี้"**
2. **ไม่บอกความหมายของคอลัมน์** — รู้ชื่อ `n_TARGET` แต่ไม่รู้ว่าเลขแต่ละค่าแปลว่าอะไร **ห้ามเดา**
3. **ไม่ใช่ชั้น wire** — ตารางคือข้อมูล ไม่ใช่รูปแบบแพ็กเก็ต · การจะรู้ว่าส่งอะไรออกไปยังต้องดู `pf_bridge\external\PF_SERIALIZER_FIELDS.tsv`
4. **ไม่ได้ตรวจความถูกต้องของค่า** — แค่แกะโครงสร้างออกมาให้อ่านได้

## re-derive

```
python3 pf_extract_gamedata.py --out <dir> <ไฟล์ .dec ทั้ง 4>
```
ใช้เวลา ~1.4 วินาที · อ่านอย่างเดียว ไม่แตะไฟล์ต้นทาง
sha256 ของ input บันทึกไว้ใน `_<SOURCE>_meta.json` ทุกไฟล์ ⇒ เทียบได้ว่าแกะจากไฟล์เดียวกันไหม

**หมายเหตุโครงสร้าง:** `TEXTDATA` ใช้ฟิลด์ flags เป็น u32 · `CONSTDATA`/`QUESTDATA` ใช้เป็น
**ชื่อตาราง tip ที่ผูกกัน แบบ length-prefixed utf16** — ตัวถอดตรวจจับเองอัตโนมัติ
**นี่คือจุดที่ตัวถอดเดิมพัง** และเป็นเหตุผลที่ CONSTDATA ไม่เคยมีสารบัญมาก่อน
