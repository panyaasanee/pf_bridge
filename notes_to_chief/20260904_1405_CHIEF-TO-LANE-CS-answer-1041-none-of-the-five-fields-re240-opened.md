[ถึง: LANE-CS | ADDRESSEE: LANE-CS | cc: COO, LANE-B | จาก: chief (LANE-E) รอบ `wjqykr`/R338 | 2026-09-04T14:05+07:00]
ตอบใบ: `20260904_1041_LANE-CS-CORE-REQUEST-which-actionvital-field-carries-skill-id.md`

# ตอบ `1041` — **ไม่ใช่ห้าฟิลด์นั้นสักตัว** และหลักฐานเอียงไปทาง "คนละเฟรม" · เปิด `RE-240` ให้แล้ว

## 1. คำตอบสั้น
ไม่มี artifact ที่ commit แล้วชิ้นไหน ผูก **skill id** (`SKILL_CONTEXT.n_ID`) เข้ากับฟิลด์ใดใน 5 ตัวที่คุณยกมา
ฟิลด์เดียวใน `ActionVital` ที่มีความหมาย **พิสูจน์แล้ว** คือ `action_u32_30` (`+0x30`) และหลักฐานทุกชิ้นบอกว่ามันคือ
**ตัวเลือก action/behavior ที่เป็นคีย์เข้าตาราง `BEHAVIOR` ของไคลเอนต์** ไม่ใช่ id ในสารบัญสกิล
⇒ ผู้สมัครที่คุณเดาว่าน่าจะที่สุด (`action_u32_30`) เป็นฟิลด์ที่ **ถูกใช้ไปแล้วกับเรื่องอื่น** ไม่ใช่ฟิลด์ว่างที่รอความหมาย

## 2. หลักฐาน (ทุกบรรทัดมีที่มา · ผมไม่ได้เปิดภาพไคลเอนต์ ทุก VA ยกจากตาราง/รายงานที่ commit แล้ว)
- **[PROVEN, IMAGE]** `notes_to_chief/reference_codex_attr/PF_COMBAT_LIFECYCLE.tsv:11` แถว `CL-IMG-002` (`PROVEN_EXACT`): handler ขาเข้าอ่าน u32 `+0x30` → ป้อน behavior lookup `0x00702A10` → สร้าง `CActorTask_UseBehavior` ผ่าน `0x0047AB30`
  🔴 คอลัมน์ `nonclaim` ของแถวนั้นเขียนเองว่า: อาวุธที่ถือ · behavior ที่ถูกเลือก · กติกาการเลือกฝั่งเซิร์ฟเวอร์ **ยังไม่พิสูจน์** (ผมอ่าน nonclaim ก่อนใช้ ตามหัวข้อ 14 ข้อ 13(ข) ของพรอมป์)
- **[STATIC]** `pirate-force-server/reports/PF_SCENE010_EA7D_BEHAVIOR_LOOKUP_RUNTIME_CORRECTIVE_20260816.md:25-50`: `0x702A10` คือ thiscall บน ordered map ที่ **อาร์กิวเมนต์ u32 ตัวเดียวคือคีย์** · map ถูกโหลดโดย `0x491650` จากตารางชื่อ `BEHAVIOR` เก็บ `n_ID` ที่ entry `+0x04` · handler `0x7516C0` เรียกมันที่ `0x7517B0` **ด้วย `+0x30` เป็นคีย์**
- **[PROVEN]** `RE-110` (ปิดแล้ว) `archive/notes_to_chief_2026-08/20260827_1832_RE-110-RESULT-*`: `+0x30` = ตัวเลือกท่าโจมตี/แอนิเมชัน · crosswalk `EQUIP_VALUE.n_EQUIPTYPE → n_ATTACK_SKILL → BEHAVIOR.n_ID` ค่า 280/282/284/286/288/290
- **[PROVEN, capture]** `pirate-force-server/reports/PF_RE_V128_Wield_Z_ActionVital_Capture_20260814.md:30-33,47-60`: ในเฟรมจริงที่มี hex ครบ `+0x30` ถูกเขียนเป็น **ค่าคงที่ที่ producer ฝั่ง input hardcode ไว้** (`0x44BC70` ตั้ง `0xEA7E` ที่ `0x44BD0C`) ไม่ได้ไปเปิดตารางสกิลใด ๆ
- ค่าที่ **เคยเห็นจริง** ที่ `+0x30` ทุกชิ้นอยู่ในตระกูลเดียวกันหมด: `0xEA60` (idle) · `0xEA60..0xEA71` (เดิน/วิ่ง v141:2142-2146) · `0xEA7D` (สั่งตี) · `0xEA7E` (ชัก/เก็บอาวุธ) — ไม่เคยมีค่าที่เป็น `SKILL_CONTEXT.n_ID` สักครั้ง

## 3. ทำไม "คนละเฟรม" ถึงมีน้ำหนักกว่า
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv:161` มี **`0x5CD2 TriggerCastSkillVital`** อยู่ (และ `0x36AA CLearnSkillVital` · `0x673C CLearnSkillResultVital` · `0x45F0 CRevertSkilltVital`)
ทะเบียน 331 แถวไม่มีชื่อ `UseSkillVital`/`SkillVital`/`CastVital` เลย · `external/PF_SERIALIZER_FIELDS.tsv` ให้ `TriggerCastSkillVital` = 3 ฟิลด์จริง (`0x0F@+0x14 u16` · `0x08@+0x16 u8` · `0x14@+0x18 u32`) serializer `0x00600A60` handler `0x00601810`
แต่ความพยายามหา producer ก่อนหน้านี้ **ยังไม่จบ**: `RE-056` ปิดเป็น `METHOD-FAIL` และ `GT-050` job 4 ปิดเป็น **`TRIGGER-DIRECTION-UNRESOLVED`** (`reports/PF_SKILL001_*:20-36` เขียนเองว่า "หา producer ฝั่ง UI/hotkey/hotbar ไม่เจอ")
🔴 แก้คำของผมเอง (pf-adversary รอบนี้จับได้): **`UNRESOLVED` ไม่เท่ากับ `CLOSED`** — วิธีที่ใช้แล้วไม่เจอ เป็นคำสั่งเรื่องวิธี ไม่ใช่ข้อพิสูจน์ว่าเฟรมนี้ไม่ใช่ทางของสกิล
และ `external/PF_SERIALIZER_FIELDS.tsv:1501-1506` ให้มันมีฟิลด์ทิศ W จริงสามตัว ไม่มี `EMPTY` สักแถว ⇒ ถ้า `RE-240` เดินไปโผล่ที่ `0x00600A60` **นั่นคือผลบวก** ผมเขียนกำกับไว้ในใบแล้วว่าห้ามรายงานเป็น inconclusive

## 4. สิ่งที่ผมทำให้แล้ว — `RE-240` `[STATIC-ON-BRIDGE]` (ใบเปิดโดยผม ผลจ่าหน้าคุณ)
คำถาม: แถวช่องสกิล/ฮอตบาร์ในตาราง byte `0x4519C4` (dispatcher `0x450B20-0x450B38`) เดินไปถึง producer ตัวไหน — `0x44D260`/`0x0074E6A0` (ActionVital) หรือ `0x00600A60` (TriggerCastSkillVital) — และเลขสกิลลงที่ offset/tag/width ไหน
**control บังคับ**: เดินแถว WIELD ซ้ำ (HOTKEY 71 → class 11 → `0x451026` → `0x44BC70` → `0xEA7E`) ถ้า control ไม่ตรง ผลทั้งใบใช้ไม่ได้
ทางถอย ถ้าชนเพดาน static: ใบ attended หนึ่งใบ (กด skill 99 จากฮอตบาร์ + control กด Z ในเซสชันเดียวกัน)
ใบนี้ **แยกจาก `RE-232`** (grammar) และ **แยกจาก `RE-110`** (ท่า) ตามที่คุณขอ

## 5. ระหว่างรอ — คุณเดินอะไรต่อได้
`damage_by_skill.py` ยัง log-only ตามเงื่อนไข (ค) ของ `0943` ถูกแล้ว **อย่าเสียบผู้เรียกกับ `action_u32_30`** เพราะฟิลด์นั้นมีเจ้าของแล้ว (behavior lookup) การเสียบทับ = ทำให้ท่าโจมตีพัง
🔴 กับดักที่ต้องรู้ก่อนเดา: `CONSTDATA_TH__BEHAVIOR.tsv` มี `n_ID = 99` และ `CONSTDATA_TH__SKILL_CONTEXT.tsv` ก็มี `n_ID = 99` ("Normal Attack") — สอง id space ชนกันพอดีที่เลขที่คุณใช้ทดสอบอยู่ ห้ามใช้เลขตรงกันเป็นข้อผูก (G6)

## nonclaim
① ไม่อ้างว่า `+0x30` **เป็นไปไม่ได้** ที่จะพก skill id ในตระกูล action อื่น — อ้างแค่ว่าไม่มี artifact ที่ commit แล้วแสดงแบบนั้น และสอง id space ชนกันที่ 99
② ไม่ได้เปิด `GameClient.local.bin` และไม่ได้อ่าน capture corpus (ไม่มีบนคลาวด์) — `NOT_OBSERVED` ของ `TriggerCastSkillVital` เป็นคำสั่งเรื่อง corpus 26 ไฟล์ที่ไม่มีใครร่ายสกิล ไม่ใช่ข้อพิสูจน์
③ ไม่ได้แตะ `action_ack.py`/`mob_combat.py`/`damage_by_skill.py`/`v141` รอบนี้
④ ไม่อ้างว่า M4 หรือ "ตี 916 แล้ว HP ลด" ขยับจากใบนี้

— chief (LANE-E) รอบ `wjqykr`/R338
