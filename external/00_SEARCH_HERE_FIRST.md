# 🔴 อ่านไฟล์นี้ก่อนจะ "ไปถอด" อะไรใหม่จากไบนารี

## 🔴 V2 checkpoint ปัจจุบัน — อ่านส่วนนี้ก่อน V1

**A5 พบ IMAGE/CAPTURE mismatch 386 instances ที่ 3 field locations / 4 field+reason points** หลังทาบ effective V2 schema กับ capture ที่ตัดเนื้อหาซ้ำตาม SHA-256 แล้ว ตาราง IMAGE ไม่ถูกแก้ให้เข้ากับ CAPTURE

ลำดับอ่าน:

1. `PF_V2_MANIFEST.md` — namespace, SHA-256 และ checkpoint verification
2. `PF_V2_HANDOFF.md` — วิธีรวม V1 + overlay โดยไม่สร้าง duplicated output
3. `PF_V2_FIELD_VALIDATION.md` / `.tsv` — A5 mismatch 3 field locations / 4 field+reason points / 386 instances
4. `PF_V2_EFFECTIVE_STATUS.md` / `PF_V2_P1_OPEN.tsv` — IMAGE-static Priority 1 CLOSED 250/365, OPEN 115
5. `PF_V1_MANIFEST.md` / `PF_HANDOFF_V1.md` — ฐาน V1 immutable

⚠️ **ห้ามใช้ `PF_SERIALIZER_FIELDS.tsv` V1 เดี่ยว ๆ เป็นผลล่าสุด** และห้าม append TSV overlay ทุกไฟล์เข้าด้วยกันตรง ๆ: ใช้ `CHANGED` เป็นการแทนที่, `REMOVE*` เป็นการลบ และ `ADD*` เป็นการเพิ่มตามลำดับใน `PF_V2_HANDOFF.md`. Attr serializer 59 รายการมี correction ที่ slot `+0x34`; การเก็บแถว `+0x18` เดิมร่วมกับแถว correction จะสร้างข้อเท็จจริงซ้ำ/ผิด

ผล V2 เป็น local-only ใน `pf_bridge\external` และถูก repository ignore อยู่: ผู้ที่เข้าถึงเครื่องนี้อ่านได้ แต่ clean clone/remote จะไม่ได้ไฟล์ชุดนี้โดยอัตโนมัติ

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


**V1 core ของโฟลเดอร์นี้มี 8 ตาราง รวม 17,626 แถว; ผลล่าสุด V2 อยู่ในรูป additive overlays + derived indexes + manifest ตามรายการด้านบน**
มันแกะไคลเอนต์ไปแล้วเป็นวัน ๆ และ **คำตอบของคำถามหลายข้อที่เรากำลังจะเปิดใบใหม่ อยู่ในนี้แล้ว**

## กติกาข้อเดียวที่ต้องทำทุกครั้ง

> **ก่อนเริ่มงาน static ใด ๆ: `grep` หาชื่อ message / ชื่อคลาส / VA ที่สนใจในโฟลเดอร์นี้ก่อนเสมอ**
> แล้วเขียนในจดหมายว่า **"ค้นชุดส่งมอบแล้ว เจอ / ไม่เจอ"** — บังคับทุกใบ

**ทำไมกฎนี้ถึงเกิด (เรื่องจริง 2026-08-23):** ผู้ช่วยร่างใบ GT-050 ว่า *"ให้ไปถอด serializer ของ `TriggerCastSkillVital`"*
แล้วอีก 20 นาทีต่อมาเปิดไฟล์ในโฟลเดอร์นี้ **พบว่ามันถอดไว้ครบแล้ว** ทั้ง VA · span · sha256 · ฟิลด์ทั้งสามช่อง
⇒ เกือบสั่งให้คนไปทำงานซ้ำที่ทำเสร็จแล้ว **ถ้าคุณเริ่มเซสชันใหม่และไม่รู้เรื่องนี้ คุณจะพลาดแบบเดียวกัน**

---

## มีอะไรอยู่ในนี้บ้าง

| ไฟล์ | แถว | ใช้ตอบคำถามอะไร |
|---|---|---|
| **`PF_PROTOCOL_REGISTRY.tsv`** | **519** | **ทุก message ในเกม** — ชื่อ + `vtable_va` + `serializer_va` + `handler_va` + `getter_va` + file offset ครบ ⇒ *"ข้อความชื่อนี้อยู่ที่ VA ไหน"* |
| **`PF_SERIALIZER_FIELDS.tsv`** | **6,931** | **ฟิลด์ของทุก message** — `tag` · `field_offset` · `len` · ทิศทาง W/R · `span_start/end` · `span_sha256` ⇒ *"ข้อความนี้มีกี่ฟิลด์ อยู่ออฟเซ็ตไหน ยาวเท่าไร"* |
| `PF_PROTOCOL_PRIORITY.tsv` | 519 | สถานะความพร้อมของแต่ละ message — อันไหนถอดครบ อันไหนติดอะไร |
| `PF_FIELD_VALIDATION.tsv` | 1,038 | เอา schema ไปทาบ capture จริงแล้วผ่านกี่เฟรม · `mismatch` · `A2_STATIC_OPEN` |
| `PF_RUNTIME_CLASSMAP.tsv` | 6,244 | vtable -> ชื่อคลาส (จาก dump) · 🔴 `class_name` เป็น UNKNOWN เกือบ 100% |
| `PF_INPUT_INVENTORY.tsv` | 2,066 | บัญชีไฟล์ input ที่แช่แข็งไว้ (capture 1,772 ไฟล์) + sha256 |
| `PF_DATA_EVIDENCE.tsv` | 290 | ไฟล์ข้อมูลในเกมที่ parse แล้ว |
| `PF_TAG_CENSUS.tsv` | 11 | ความหมายของ `tag` แต่ละตัว + ความถี่ + ตัวอย่าง |

**ไฟล์ `.md` ชื่อเดียวกัน = คำอธิบายของตารางนั้น** · `PF_HANDOFF_V1.md` (32 KB) และ `PF_EXTERNAL_REPORT.md` (49 KB) = รายงานเต็ม
**สคริปต์ `pf_*.py` ในโฟลเดอร์นี้ = ตัวที่สร้างตารางพวกนี้** ⇒ **re-derive ได้เอง** (GT-042 พิสูจน์แล้วว่าออกมาไบต์ต่อไบต์เท่าเดิม)

---

## ท่าค้นที่ใช้ได้เลย

```powershell
# 1) message ชื่อนี้มีอยู่ไหม อยู่ VA ไหน
Select-String -Path PF_PROTOCOL_REGISTRY.tsv -Pattern "Skill"

# 2) ฟิลด์ของ message ตัวนี้มีอะไรบ้าง
Select-String -Path PF_SERIALIZER_FIELDS.tsv -Pattern "^TriggerCastSkillVital"

# 3) เคยเอาไปทาบ capture แล้วผลเป็นยังไง
Select-String -Path PF_FIELD_VALIDATION.tsv -Pattern "TriggerCastSkill"

# 4) tag ตัวนี้แปลว่าอะไร
Get-Content PF_TAG_CENSUS.tsv
```

**ตัวอย่างผลจริง** — `TriggerCastSkillVital` ค้นเจอทันทีโดยไม่ต้องเปิด disassembler:
```
serializer_va 0x00600A60 · handler_va 0x00601810 · vtable_va 0x00F3175C
span [0x00600A60,0x00600AD7) sha 396200629ab4082b8eef730dda809124f5df8eca6f0ced5419d7a2ac7e3500ec
  #1 tag 0x0F @ +0x14 len 2
  #2 tag 0x08 @ +0x16 len 1
  #3 tag 0x14 @ +0x18 len 4
```

---

## 🔴 สิ่งที่ตารางพวกนี้ **ไม่ได้** บอก — อย่าเข้าใจผิด

1. **ไม่บอกทิศทางจริง** — มีทั้งแถว `W` และ `R` เพราะ serializer ตัวเดียวทำสองทาง
   **ไม่ได้แปลว่าไคลเอนต์ส่งจริง** ⇒ ต้องไล่ผู้เรียกเองว่าเข้าสตรีมผ่าน `0x0089A600` (W) หรือ `0x0089A640` (R) — แบบที่ GT-046 ทำ
2. **ไม่บอกตัวจุดชนวน** — ว่าอะไรทำให้ข้อความถูกส่ง (คลิกเมาส์? timer? entity update?) ต้องไล่เอง
3. **ไม่บอกความหมายของฟิลด์** — รู้ว่า `tag 0x0F len 2` แต่ไม่รู้ว่ามันคือ skill id หรืออะไร **ห้ามเดา**
4. **`PF_RUNTIME_CLASSMAP` แทบไม่มีชื่อคลาส** — 6,244 แถว `class_name` เป็น `UNKNOWN` เกือบหมด
5. **ยังต้อง verify ก่อนพึ่งเสมอ** — เทียบ `span_sha256` กับอิมเมจจริงก่อน ถ้าไม่ตรงแม้ตัวเดียว **หยุดแล้วรายงาน**
   *(ตารางนี้เป็นงานของคนอื่น ต้องผ่านปฏิปักษ์ก่อน — GT-042 ผ่านแล้วครั้งหนึ่ง แต่กติกายังบังคับให้เช็คทุกครั้งที่พึ่ง)*

## สถานะการใช้งาน ณ 2026-08-23

- ✅ ผ่าน re-derive ปฏิปักษ์แล้ว (GT-042 · ไบต์ต่อไบต์)
- 🟡 `pf_validate_capture_fields.py` **มีช่องโหว่** — มันยอมรับการกลายพันธุ์ `field_offset` (GT-047) ⇒ **ห้ามใช้ผล validator ตัวเดียวเป็นเหตุผลเลื่อนขั้น schema**
- 🔴 **ยังไม่มีโค้ดใน `src/` `tools/` `tests/` อ่านไฟล์พวกนี้เลยแม้แต่บรรทัดเดียว** — ข้อห้าม "ห้ามเขียนโมดูล/encoder" เพิ่งปลดเมื่อ 2026-08-23 02:03
