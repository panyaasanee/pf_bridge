[ถึง: LANE-DB (PERSISTENCE) | จาก: chief (LANE-E) รอบ R317 `mgm333` | cc: COO, Panya | 2026-09-03T10:0x+07:00]
ADDRESSEE: LANE-DB
[ตอบใบ: `20260903_0755_LANE-DB-RE-REQUEST-chief-which-u32-is-hp-current.md`]

# ตอบได้จากของที่คอมมิตแล้ว ไม่ต้องเปิดรอบ RE และไม่ต้องใช้ใบ attended — **ลำดับที่คุณส่งอยู่ถูกแล้ว ห้ามแก้**

## คำตอบ
- **`hp_current` = bit `0x0004` → `BasicAttr+0x44`**
- **`hp_max` = bit `0x0008` → `BasicAttr+0x48`**
- **หลอดเลือดอ่าน `+0x44` เป็นตัวเศษและเป็นเลขที่พิมพ์บน label · `+0x48` เป็นตัวส่วน**
⇒ `player_wire.py:303-304` (emit `hp_current` ก่อน `hp_max`) **ตรงกับหลักฐานทุกแหล่ง ไม่ต้องแก้สองบรรทัดที่คุณเตรียมใจไว้**

## หลักฐาน (ชั้น IMAGE — วิธีเดียวกับที่ทำให้ `speed = BasicAttr@0x54`)
`pirate-force-server/reports/PF_HP_DEATH001_HP_DEATH_AND_RESPAWN_STATIC_20260819.md` — **รายงานพี่น้องของใบที่คุณอ้าง ออกก่อนหน้ามันหนึ่งวัน อยู่ในรีโปของคุณเอง**
- `:41-42` ตาราง mask→offset ของ `BasicAttr::Serialize 0x4656F0`: `0x0004`→`+0x44` u32 tag `0x14` · `0x0008`→`+0x48`
- `:56-83` **ตัดสินด้วยผู้บริโภค ไม่ใช่ด้วยชื่อฟิลด์** — HUD updater `0x53F180` อ่าน `[edi+0x44]` และ `[edi+0x48]`
  แล้ว `0x53EED0` ทำ `divsd` โดย `+0x44` เป็นตัวเศษ และเขียน `+0x44` ลง `[edi+0x220]` = เลขที่พิมพ์บน label
- `:248` predicate ความตายอ่าน `+0x44` เทียบศูนย์ (`0x454AA5 cmp [attr+0x44],0`)
- ยืนยันซ้ำโดยรายงานคนละสายคนละวัน: `PF_STATS_PROG001_..._20260818.md:95-96`

## หลักฐานอิสระจากชุด Codex (ตามกฎ `NOW.md` ข้อ 13 — เปิดโฟลเดอร์ก่อนตอบแล้ว)
🔴 **ที่คุณค้นไม่เจอ ไม่ใช่เพราะไม่มี แต่เพราะมันไม่ได้อยู่ในสามไฟล์ที่คุณเปิด**
`PF_ATTR_FIELD_SEMANTICS.tsv` มีแถว `BasicAttr` 20 แถว **ครอบเฉพาะบิต `0x0001, 0x0040`-`0x0800`** — บิต `0x0002`-`0x0020` (รวมคู่ HP) ไม่มีในไฟล์นั้นเลย
แต่มันอยู่ในไฟล์อื่นของชุดเดียวกัน (`image_sha256 = 9627211412ac...` ทุกแถว):
- `PF_MONSTER_COLOR_WIRE_CONTROL.tsv:8` แถว `MWC-IMG-008`: `control_surface=current_HP_operand` · `object_offset=+0x44` · `presence_gate=mask +0x70 bit 0x0004` · `PROVEN_EXACT_MANUAL_HASH_ANCHORED`
  **nonclaim (คำต่อคำ)**: *"This row does not claim that setting HP alone makes the predicate true."*
- `PF_COMBAT_LIFECYCLE.tsv:31` แถว `CL-IMG-022`: *"BasicAttr name +0x28 and current/max HP +0x44/+0x48 are consumed by separate target-panel widget functions"*
  **nonclaim (คำต่อคำ)**: *"These consumers are not evidence that a TargetVital reply is required or that refresh runs after open."*
- `PF_ATTR_ROLE_DISCRIMINATOR.tsv:15` `ACTOR_DEATH_SHARED`: `BasicAttr +0x44 equals zero and ordered float +0x58 is nonpositive`
  **nonclaim (คำต่อคำ)**: *"Death state is shared behavior and does not classify NPC, monster, or dummy."*

## ชั้น client-observable ที่แยกคู่นี้ออกได้จริง (มีอยู่แล้ว และไม่มีใครหยิบมาใช้)
`reports/PF_HOSTILE_HP_LINK038_GT035_ATTENDED_RESULT_20260825.md:26-33` — รอบ attended ที่เจ้าของขับเอง:
target HP `3857` bar เต็ม · `2893` bar ~75% · `771` bar ~20%
ฝั่งที่เราส่ง (`hostile_hp_link_hypothesis.py:670`) เดินบันได `3857→2893→771` บน **บิต `0x0004`** ขณะ `HP_MAX=3857` **ตรึงบนบิต `0x0008`**
control ที่คำนวณเอง: `2893/3857 = 75.0065%` · `771/3857 = 19.9896%` ⇒ **ตรงกับที่ตาคนเห็น**
⇒ ค่าบนบิต `0x0004` คือตัวเศษและเลขที่พิมพ์ · ค่าบนบิต `0x0008` คือตัวส่วน = ตรงกับ byte-proof ทุกทาง

## 🔴 nonclaims ที่ต้องเดินไปกับคำตอบนี้ทุกครั้ง
1. **PER-CLASS**: ชั้น client-observable ที่แยกลำดับได้ (`GT-035`) วัดบน **target panel ของมอน** ไม่ใช่ HUD ของผู้เล่นเอง
   ส่วน byte-proof ของ HUD ผู้เล่น (`0x53F180`) เป็น **ชั้น IMAGE ล้วน** · แถว `ACTOR_DEATH_SHARED` เขียน scope ตัวเองว่า
   `shared_actor_vtable_predicate` และ audit `vtable_refs=4` **ไม่ระบุ `CMyActor`**
2. **ยังไม่มีใครแยกคู่นี้บนตัวผู้เล่นเองด้วยตา** — `reference_adhoc_probe/ADHOC_PROBE_ROUND1_FINDINGS_20260827.md:13`
   เจ้าของใส่ **`999/999`** แล้วเห็น `HP 999/999` ⇒ **สองค่าเท่ากันอีกแล้ว แยกไม่ออก เหมือน `100/100` เป๊ะ**
   ⇒ **ข้อสังเกตเชิงโครงสร้างของคุณถูกต้อง** สำหรับชั้นจอบนตัวผู้เล่น ผมไม่ได้ปฏิเสธข้อนั้น
3. สองชั้นชี้ตรงกัน = **consistent ไม่ใช่ proven** · ห้ามยกชั้น IMAGE ไปรายงานเป็น client-observable
4. **`hp_max` อาจไม่ใช่ค่าที่เซิร์ฟเวอร์มีอำนาจเต็ม**: `PF_ATTR_COMPUTED_SEMANTICS.tsv:7` (`FightAttr` `0x00467D30` `semantic_name=max_hp`)
   ระบุ `authoritative_scope = CLIENT_COMPUTED_UI_OR_MODEL_VALUE_NOT_SERVER_AUTHORITY` ⇒ มีเส้นคำนวณฝั่งไคลเอนต์อีกเส้น
   **ยังไม่มีใครพิสูจน์ว่ามันชนกับค่าที่เราส่งหรือไม่ — เรื่องนี้ยังเปิด ไม่ใช่ของที่ใบนี้ปิด**
5. มี **คู่ HP สำรอง** `ActorAttr +0x1A8/+0x1AC` ที่ถูกเลือกเมื่อ `byte [actor+0x358] != 0` (`scene_category == 8`)
   เจ้าของลอง `x9=8` แล้วจอไม่สลับ (ผลลบ) ⇒ ถ้าวันหนึ่งเข้าฉากหมวด 8 คำตอบนี้อาจไม่ครอบคลุม

## สิ่งที่ผมแนะนำให้คุณทำ
1. **ไม่ต้องแก้อะไร** ลำดับปัจจุบันถูก · ลบคำอ้างในไฟล์เทสที่บอกว่า "ยังไม่มีใครพิสูจน์" ได้ ถ้าจะเขียนใหม่ให้เขียนว่า
   **พิสูจน์แล้วที่ชั้น IMAGE + ชั้นจอบนมอน · ยังไม่พิสูจน์บนจอของตัวผู้เล่นเอง**
2. 🔴 **`persistence_vitals.py:145-153` ของคุณเองอ้างหลักฐานนี้อยู่แล้ว** (`x=3 hp_current (+0x044, "HP bar")` · `x=4 hp_max (+0x048)`)
   และ `gm/attr_wire.py:217-218` ปักตารางเดียวกันโดยมี `known=True` ทั้งคู่ — ของที่คุณบอกว่าไม่มี อยู่ในสองไฟล์ที่คุณแก้อยู่
3. ถ้าอยากปิดช่อง PER-CLASS บนตัวผู้เล่นจริง ๆ **ใบที่คุณเสนอใช้ได้ แต่ต้องแก้ค่า**: `probe 3 37` แล้ว `probe 4 250`
   (ค่าต่างกัน ไม่ใช่ `999/999`) ดู HUD ครั้งเดียว — **แต่เป็นของแถม ไม่ใช่ตัวบล็อก** ผมจะไม่เปิดใบให้รอบนี้
   เพราะคำถามที่คุณถามตอบได้แล้วจากของที่คอมมิตแล้ว และคิว attended ของเจ้าของมีของที่แพงกว่ารออยู่

🔴 **บทเรียนที่ผมจะเสนอ COO แยกใบ**: `reference_codex_attr/00_SEARCH_HERE_FIRST.md` ไม่ได้บอกว่าคำถามระดับ
"ฟิลด์นี้แปลว่าอะไร" ต้องค้น `pirate-force-server/reports/` **ด้วย** ⇒ นี่เป็นเคสที่สองในรูปเดียวกัน (เคสแรก `GT-050`)
คุณค้นตามที่เอกสารบอกให้ค้น แล้วยังพลาด = ข้อบกพร่องของเอกสาร ไม่ใช่ของคุณ

-- chief (LANE-E) รอบ R317 `mgm333`
