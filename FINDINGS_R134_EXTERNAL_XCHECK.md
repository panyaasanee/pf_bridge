# FINDINGS R134 — EXTERNAL-XCHECK-001: เทียบ wire codec ของเซิร์ฟเวอร์เรา กับตารางส่งมอบ RE ของ Codex

- **รอบ:** R134 (session wgi55l · cloud) · 2026-08-24 00:0x–00:4x (+07:00)
- **ชนิดงาน:** static cross-check จาก artifact ที่ commit แล้วล้วน — ไม่มี binary/capture บน cloud
- **ทำโดย:** ลูกมือ `pf-static-re` หนึ่งรอบ + chief ตรวจซ้ำจุดที่กลายเป็น claim ด้วยตัวเอง
- **ฝั่งซ้าย:** โค้ดเซิร์ฟเวอร์เรา (`current/pf_login_game_server_v141.py` + `src/pirateforce_foundation/`)
- **ฝั่งขวา:** `pf_bridge/external/PF_PROTOCOL_REGISTRY.tsv` (519 แถว) + `PF_SERIALIZER_FIELDS.tsv` (6,931 แถว)
- 🔴 **สถานะฝั่งขวา: ยังไม่ผ่าน GT-054 (span-verify กับอิมเมจจริง)** — ทุกแถวคือ *คำอ้าง static ของเพื่อนร่วมงานคนก่อน*
  ไม่ใช่ ground truth · AGREE ในเอกสารนี้แปลว่า "โค้ดเรา ตรงกับ ตารางเขา" **ไม่ใช่** "ตรงกับอิมเมจ"

## 0. ข้อจำกัดของการเทียบ (อ่านก่อนใช้ผล)

`field_offset` ใน `PF_SERIALIZER_FIELDS.tsv` คือ **offset สมาชิกใน source object** (ฝั่ง C++ ของ client)
ส่วนโค้ดเราประกอบ **tag-length wire stream** — คนละระบบพิกัด ⇒ เทียบ field-level ได้เฉพาะเลนที่โค้ดเรา
จดทะเบียน object offset ไว้เอง (เช่น damage lane) · เลนที่เราเก็บเป็น opaque blob (actor body) เทียบไม่ได้โดยโครงสร้าง

## 1. Inventory + name match

- ข้อความที่เซิร์ฟเวอร์เรา implement จริงบน wire: **35 ชื่อ** (28 จาก v141 serializers + 7 จากโมดูล hypothesis
  ใน `src/pirateforce_foundation/` — รายชื่อเต็มพร้อม file:line อยู่ในรายงานลูกมือ ท้ายไฟล์นี้สรุปเฉพาะที่ต้องจำ)
- เทียบชื่อกับ `PF_PROTOCOL_REGISTRY.tsv`: **ตรง exact 33** · ผิดปกติ 2:
  - `ItemOperateVital` (0x36FE · v141 NAMES :475) — registry มีแต่ `ItemOperateVitalReq`/`Res` ไม่มีตัวเปล่า
  - `SkillAttr` ที่โค้ดเราอ้างเป็น id 0x1661 — registry ใช้ชื่อ **`CSkillAttr`** (ดู §5 ข้อควรระวัง token)

## 2. จุดที่ AGREE — มีค่าเป็น corroboration อิสระ

### 2.1 CHitResult 0x16F7 (เลน damage) — ตรงกันทั้งโครง ✅
เทียบ `src/pirateforce_foundation/damage_hp_link_hypothesis.py:137-149,704-724` กับแถว `CHitResult` ใน SERIALIZER_FIELDS:
header (qword 0x32 @+0x18 · u16 0x12 ×2 @+0x20/+0x22 · u32 0x14 @+0x24 · u8 0x0B @+0x28 · count u16) และ
entry ครบทุกฟิลด์ (target 0x32@+0x00 · damage 0x14@+0x08 · position 0x2A×3@+0x0C · yaw 0x2A@+0x18 · flags 0x12@+0x1C)
— **tag/len/offset/ลำดับ ตรงทุกช่องใน 12 แถวที่ resolve แล้ว** · ตาราง Codex ถอดจากอิมเมจโดยไม่เคยเห็นโค้ดเรา
⇒ นี่คือการยืนยันอิสระชั้น static ของ wire contract เลน damage (DAMAGE-MODEL-001)
🔴 **ขอบเขตที่ต้องพูดตรง ๆ (adversary D1):** สตรีม W ของ CHitResult ใน TSV มี **22 แถว** — ords 8-12
(คั่นระหว่าง count กับ entry แรก) และ 21-22 เป็น `PE_IMPORT_INVALID_PARAMETER_*` / `UNKNOWN(...wire_effect_unproved)`
· R ord16 เป็น `CALL_UNCLASSIFIED` — ชั้นเดียวกับแถว unresolved ของ UpdateAttrVital · ถ้าแถวพวกนี้ปล่อยไบต์จริง
ผู้อ่านฝั่ง client จะ desync กลาง frame ⇒ **ห้ามอ้าง §2.1 เป็น corroboration ของ payload pin 62 ไบต์ทั้งก้อน** —
มันยืนยันเฉพาะ 12 แถวที่ resolve · **nonclaim:** ยังเป็น static-static จนกว่า GT-054 ผ่าน

### 2.2 AvatarAttr 0x16A0 — VA ตรงกันสองจุดอิสระ · จุดที่สาม**ขัดกัน** (adversary D5)
- id-slot: โค้ดเรา `v141:2372` = `0x1033468` ↔ registry `id_global_va = 0x01033468` ✅
- vtable: โค้ดเรา `remote_player_hypothesis.py:180` `[PROVEN VA=0xF0E088]` ↔ registry `vtable_va = 0x00F0E088` ✅
- 🔴 serializer: registry ให้ `serializer_va = 0x0043BB80` — **ค่านี้ซ้ำกัน 45 แถวใน registry** (placeholder
  ชั้น base-class · กลไกเดียวกับที่ทำให้แถว Attr เป็น EMPTY ใน §4) ↔ v141:2373 บันทึก serializer จริงของ
  AvatarAttr ที่ `0x464560` ⇒ **ห้ามเอา serializer_va ของ registry ไป "ตรวจ" per-class serializer ของเรา** —
  แถวที่ serializer_va = 0x0043BB80 ไม่มีความรู้ระดับ per-class อยู่ในนั้น

### 2.3 LogoutVital 0x1B40 (inbound) — ตรง (tag/len/ลำดับ 4 ฟิลด์) ✅

## 3. MISMATCH — ผู้ท้าชิงบั๊ก 2 จุด (ชี้ขาดได้เฉพาะบนสะพาน ⇒ ใบ GT-055)

### 3.0 ข้อเท็จจริงเชิงระบบที่เปลี่ยนกรอบทั้งหัวข้อ (adversary D2 — วัดจริงบน HEAD)
**ทั้ง 6,931 แถวของ SERIALIZER_FIELDS ไม่มีแถวไหนมี string tag (0x44/0x48) เลยแม้แต่แถวเดียว** —
string ทุกแถวในชุดส่งมอบเป็น `UNTAGGED_WSTRING16LE` (348) หรือ `UNTAGGED_STRING8` (60) ทั้งหมด ·
ขณะที่โปรเจกต์นี้มี capture เกรด A บนอิมเมจตัวเดียวกันที่เห็น wstring **มี tag 0x48 จริง** (GT-006 chat ·
ชื่อใน CreateActorDataEx/ActorAttr · `remote_player_hypothesis.py:190` "wstring tag 0x48 @ +0x28")
⇒ ป้าย `UNTAGGED_*` ของ extractor **ผิดเชิงระบบในฐานะ wire claim หรือไม่เคยเป็น wire claim ตั้งแต่แรก**
(อาจหมายถึงมุมมอง serializer-body ที่ primitive string ปล่อย tag เองข้างใน) — **คำถามนี้ต้องถามที่ตัว
extractor/เอกสารส่งมอบบนสะพาน ก่อนตีความแถว UNTAGGED ใด ๆ เป็น wire** — เข้าเป็นจ็อบ 0 ของ GT-055

### 3A. DeleteActorVital 0x36DB — string ท้าย frame: คำถามจริงคือ "รูปเต็ม" ไม่ใช่แค่ tagged/untagged
- โค้ดเรา (`src/pirateforce_foundation/delete_actor.py:90-94`): tag `0x44` + u32 len + **UTF-16LE (2 byte/char ·
  ปฏิเสธ len คี่ที่ :92-93)** — หมายเหตุ: โค้ดเราเรียก 0x44 ว่า "wstring" ทั้งที่ tag wstring ที่พิสูจน์แล้ว
  ที่อื่นในทรีคือ 0x48 — ชวนสงสัยว่า **0x44 อาจเป็น tag ของ string8 (1 byte/char)** ต่างหาก
- ตาราง Codex: `UNTAGGED_STRING8_LEN32LE` — ถ้า primitive ปล่อย tag เองข้างใน (ตาม §3.0) สองฝั่ง
  **เข้ากันได้เรื่อง tag แต่ยังขัดกันเรื่องความกว้างอักขระ**: เรา 2 byte/char · เขา 1 byte/char
- ⇒ เคสที่น่าจะจริงที่สุดที่ระบบ verdict สองทางมองไม่เห็น: **wire = `0x44` + u32 len + string8** —
  ถ้าใช่ parser เราปฏิเสธ frame ชื่อความยาวคี่ทุกใบ (`byte_length & 1`) และอ่านชื่อ ASCII ความยาวคู่เป็น
  UTF-16LE ผิด ๆ · **คำตัดสินของ GT-055 จึงต้องเป็น "รูปเต็มที่วัดได้" (tag? + ความกว้าง?) ไม่ใช่เลือกสองทาง**
- ตัดสินจาก capture corpus + อิมเมจเท่านั้น — **needs bridge machine**

### 3B. Channel_LocalTalkMessageVital 0xAC52 — ป้าย UNTAGGED ขัด capture จริงของเราตรง ๆ
- โค้ดเรา (`chat_input_hypothesis.py:26-39,56`): prefix จับจริงจาก GT-006 เริ่ม `48 00 00 00 00 48 18 00 00 00`
  อ่านเป็น tag-`0x48` u32-len wstring สองตัว
- ตาราง Codex: `UNTAGGED_WSTRING16LE_LEN32LE` — ถ้าอ่านเป็น wire ตรง ๆ byte แรก `0x48` ต้องเป็น len u32 = 72
  ซึ่งขัด payload จริง 34 ไบต์ (ลองทั้ง len-เป็นไบต์และเป็นอักขระแล้ว ขัดทั้งคู่ — adversary ตรวจซ้ำ)
  ⇒ สำหรับ 0xAC52 ป้าย UNTAGGED **ถูกหักล้างในฐานะ wire claim ด้วยหลักฐานบน cloud แล้ว** —
  สิ่งที่เหลือให้สะพานทำคือยืนยันที่ระดับ serializer ในอิมเมจ + ตอบคำถาม §3.0 ว่าป้ายนี้แปลว่าอะไรกันแน่

## 4. CANNOT-COMPARE — ช่องว่างใหญ่สุดของชุดส่งมอบ

ตัวพา 5 ตัวที่เราใช้งานหนักที่สุด — **ActorAttr · MovementAttr · NPCAttr · ItemAttr · AvatarAttr** —
ในตาราง Codex เป็นแถว `EMPTY` (extractor ไม่ตามเข้า serializer ที่ delegate/vtable-dispatch)
⇒ **ชุดส่งมอบไม่มีข้อมูล field-level ของ Attr carriers เลย** · ที่เรามี (mask-gated body ใน
`player_wire.py` ฯลฯ) จึงยังยืนบนหลักฐาน capture ของเราเองฝ่ายเดียวเหมือนเดิม — ไม่ได้แย่ลง แต่อย่าหวังพึ่ง
ตารางนี้ในเลน Attr · เช่นกัน: `TargetPosVital`/`CreateActorVital` เทียบไม่ได้เพราะฝั่งเราเก็บ opaque โดยเจตนา

## 5. ช่องว่างฝั่งเราเอง + erratum (ยังไม่แก้ — จดพิกัดครบเพื่อรอบที่จะแก้)

### 5.1 `docs/PF_VITAL_NAMES.json` ปิดชื่อ 3 id ที่โค้ดเราใช้อยู่ไม่ได้ **โดยกติกาของมันเอง**
- ขาด: `0x16A0` (AvatarAttr) · `0x1661` · `0x16F7` (CHitResult) — ทั้งสามถูกใช้จริงใน
  `remote_player_hypothesis.py:180-182` และ `damage_hp_link_hypothesis.py:135`
- **ไม่ใช่ความสะเพร่า:** ทั้งสามไม่อยู่ใน `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (327 candidates)
  ⇒ fold รอบ 85 รับไม่ได้ · และ provenance ที่รับได้มีสามชั้นเท่านั้น (v141 / RESOLVE-001 / thunk-proven fold)
- external registry มีครบทั้งสาม **แต่ยังไม่ใช่ provenance ที่รับได้ + ยังไม่ผ่าน GT-054**
- ⏳ **คำถามค้างถึง Panya:** หลัง GT-054 ผ่าน ควรเปิด provenance ชั้นที่ 4
  ("แถว external registry ที่ span-verified แล้ว") ให้ตารางชื่อไหม — chief ไม่ตัดสินเอง
- 🔴 **กับดัก token 0x1661:** src/ เว้นชื่อคลาสของ 0x1661 **โดยเจตนา** (standing negative ของ
  `tools/pf_stats_progression_static.py` — src/ ต้องมี token progression เป็นศูนย์ ·
  `remote_player_hypothesis.py:184-188` เขียนเหตุผลไว้เอง) ⇒ ถ้าวันหน้าจะเติมชื่อเข้า names file
  ต้องตรวจก่อนว่า witness สแกน docs/ ด้วยไหม — **ห้ามเติมโดยไม่รัน witness**

### 5.2 Erratum: ประโยค stale "unknown to the server registry" — พินไว้ 4 ที่
`chat_input_hypothesis.py:3` อ้างว่า 0xAC52 "unknown to the server registry" — จริงเฉพาะ NAMES ของ v141
แต่ `PF_VITAL_NAMES.json` ตั้งชื่อ `Channel_LocalTalkMessageVital` ให้มันแล้วตั้งแต่ RESOLVE-001 (รอบ 62)
· ประโยคนี้ถูก**พินด้วยเทส** `tests/test_chat_channel_family_static.py:682` และซ้ำใน
`docs/FUNCTIONAL_COVERAGE.json:726` + `docs/HYPOTHESIS_LEDGER.json:1358` (ledger = บันทึกประวัติศาสตร์ อาจคงไว้)
⇒ การแก้คือแพตช์ 3 ไฟล์ + gate หนึ่งรอบ — **เกินขอบเขตรอบเอกสารนี้ จดเป็นงานค้างสำหรับรอบโค้ดรอบหน้า**

## 6. สิ่งที่รอบนี้ไม่ได้พิสูจน์ (nonclaims รวม)

- ไม่มีอะไรในเอกสารนี้เป็น `[PROVEN]` ชั้น client-observable — ทั้งหมดคือ wire/DB static
- AGREE = โค้ดเราตรงกับตาราง Codex — **สองฝั่งยังไม่มีฝั่งไหน verify กับอิมเมจบน clone นี้ได้**
- ชื่อตรง 33 ตัว พิสูจน์แค่ความเท่ากันของ string ไม่ใช่ความถูกของ VA/serializer
- ทิศทางจริง (client ส่งแถว W ไหม) พิสูจน์ไม่ได้จากตาราง — ตารางเองก็ประกาศไว้
- ไม่ claim อะไรเกี่ยวกับเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้วและกู้ไม่ได้ตลอดกาล

## ภาคผนวก: รายงานดิบของลูกมือ pf-static-re

เก็บเฉพาะสาระที่ยังไม่อยู่ข้างบน — ตาราง inventory เต็ม 35 ชื่อพร้อม file:line:

**Group A (v141):** LSCN_LoginVitalRes(:627) · LSCN_SelectServerRes(:634) · LoginVerifyVital(:646) ·
GSCN_RunTimeProtocolRes(:689,:747) · GSCN_LoginProtocol(:605) · SelectActorVital(:2204,:2288) ·
CreateActorVital(:2292) · StartGameRes(:2707) · GetWorldInfoVital(:2781) · TeleportVital(:2431) ·
TeleportCheckVital(:887) · NPCConversation(:768,:782) · TradeZoomVital(:866) · TradeItemResultVital(:986) ·
QuestOperateVital(:924,:956) · ShowMessageVital(:1030) · MusicControlVital(:1046) · CheckSecondPwdVital(:1058) ·
UpdateNPCAppearVital(:715) · UpdateAttrVital(:2343) · ActionVital(:2139) · NPCAttr(:1139) · ActorAttr(:2306) ·
MovementAttr(:2390,:1204) · AvatarAttr(:2369,:2263) · BackpackAttr(:2446,:2566,:2593) · ItemAttr(:2492-2543) ·
ItemOperateVitalRes(:2653,:2672)

**Group B (src/pirateforce_foundation):** CHitResult 0x16F7 (damage_hp_link_hypothesis.py:135) ·
Channel_LocalTalkMessageVital 0xAC52 (chat_input_hypothesis.py:52) · Channel_WhisperVital 0x556C
(channel_message_hypothesis.py:188) · DeleteActorVital 0x36DB (delete_actor.py:13) · LogoutVital 0x1B40
(logout_hypothesis.py:26) · ReturnSelectServerVital 0x709E (logout_hypothesis.py:179) · TargetPosVital 0x2A90
(inbound เท่านั้น — scenario.py:158, runtime.py:2867) · อ้างอิง id 0x16A0/0x1661 (remote_player_hypothesis.py:180-182)

**UpdateAttrVital ฝั่ง Codex:** 17 แถวแต่ ord 3-5,8-17 เป็น `PE_IMPORT_*`/`CALL_UNCLASSIFIED`/`UNKNOWN`
(unresolved) — ใช้ได้จริงแค่ ord2 (0x12 count) + ord7 (0x14) · body delegate ไป ActorAttr ซึ่ง EMPTY (§4)

**LogoutVital เทียบเต็ม:** 0x08@+0x14 ×2 (TSV ซ้ำ offset — quirk ของ resolver ฝั่ง Codex ไม่ใช่ข้อเท็จ wire) ·
0x14@+0x1C · 0x14@+0x20 — ตรงลำดับ/tag/len กับ bytes จับจริงใน logout_hypothesis.py:33-41
