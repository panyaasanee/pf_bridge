# CLIENT RE QUEUE -- ARCHIVE 20260906 (closed tickets moved verbatim from `CLIENT_RE_QUEUE.md` per AGENTS.md section 7 file-size gate; each has a one-line stub left in place; nothing here is deleted)

## RE-129 FORCE-POS-VITAL-VERSION-001: ไบต์ `vital_version` ของ `ForcePos` (`0x0E80`) ที่ client ยอมรับคือค่าอะไร -- prototype constructor ของ vital นี้เขียนอะไรลง `+0x10`  [**CLOSED DONE/PASS** -- ปิดหัวใบโดย LANE-GM (เจ้าของใบ) รอบ `fo2lgh` 2026-08-28T22:30+07:00 จากผล `notes_to_chief/20260828_2009_RE-129-RESULT-VERSION-ZERO-HANDLER-NOOP.md` · คำตอบ: **`ForcePos vital_version = 0`** (constructor `[0x005E5170,0x005E51A2)` ทำ `xor ecx,ecx` แล้ว `mov byte ptr [eax+0x10],cl` ที่ `0x005E5186`; generic reader เทียบ exact equality ที่ `0x005F3EFC`) · **`TeleportVital = 4`** (`mov byte ptr [esi+0x10],4` ที่ `0x005E5425`) ⇒ สี่ค่าที่วัดแล้ว `0x5A19`→0 / `ForcePos`→0 / `SelectActor`→10 / `TeleportVital`→4 **ไม่มี default ของโปรเจกต์** · ปิดเพิ่ม: สาม f32 อยู่ที่ `ForcePos +0x14/+0x18/+0x1C` · **ยังไม่ปิด (bounded negative):** ชื่อแกน x/y/z -- ไม่มี client crosswalk แยกค่าที่หนึ่ง/สอง/สาม ⇒ ยังเป็น `[สมมติของสาย GM - รอ RE]` · 🔴 **ผลที่สำคัญกว่าคำตอบหลัก:** handler ที่ client **จดทะเบียนไว้**สำหรับ `ForcePos` คือบอดี้ทั้งก้อน `[0x00710440,0x00710445)` = `mov al,1; ret 4` ไม่อ่าน payload ไม่เขียนตำแหน่ง ⇒ version ถูก = เงื่อนไข**จำเป็น ไม่ใช่เพียงพอ** · 🔴 **การปิดใบนี้ไม่ได้ปลดล็อกอะไร:** `COO-DECISION 20260828_2130` ล็อก `FORCE_POS_VITAL_VERSION_CONFIRMED = None` ไว้จนกว่าจุดเขียนแบบยืนยัน (`CORE-REQUEST-GM-030`) จะอยู่บน main -- บังคับด้วย `pirate-force-server/tests/test_gm_force_pos_version_lock.py` · consumed stub: `notes_to_chief/20260828_2009_*.CONSUMED.txt`]

> NUMBERING NOTE: ตัวนับร่วมกับ `GAME_TEST_QUEUE.md` -- เลขสูงสุดบน main ก่อนจอง = `RE-128` (สาย A,
> SCENE-ORDINAL-TO-MOBS-NID-TABLE-LOCATION-001) และ `GT-127` (สาย GM) · grep ยืนยันก่อนจอง 2026-08-28T18:2x:
> `RE-129` = 0 hit ทั้งสองไฟล์ ⇒ ใบนี้ = `RE-129`

**ค้นใน `pf_bridge\external\` แล้ว: ไม่เจอ** -- `grep -inE "0x0E80|ForcePos|vital_version|version"
external/00_SEARCH_HERE_FIRST.md` = 0 แถว
**ค้นใน `pf_bridge\gamedata\` แล้ว: ไม่เจอ** -- `grep -inE "ForcePos|version" gamedata/00_SEARCH_HERE_FIRST.md`
= 0 แถว (ใบนี้เป็นคำถาม code ไม่ใช่คำถาม gamedata)

### คำถามเดียว
`ForcePos` (vital id `0x0E80`) -- prototype constructor ของ vital นี้ `mov` ค่าอะไรลงไบต์ `message+0x10`
(ช่อง `vital_version` ที่ generic reader เทียบแบบ exact-equality) · ต้องการ **ตัวเลข + VA ของไซต์ที่เขียน**
ไม่ใช่การอนุมานจาก vital ตัวอื่น

### วิธีที่พิสูจน์แล้วว่าได้ผล -- ทำซ้ำของ RE-105 ตัวต่อตัว
RE-105 (STATIC-ON-BRIDGE, DONE/PASS, `notes_to_chief/20260827_1613_RE-105-RESULT-VITAL-VERSION-ZERO-GENERIC-MISMATCH-PATH.md`)
ตอบคำถามรูปเดียวกันนี้ให้ `0x5A19` สำเร็จมาแล้ว และระบุกลไกไว้ครบ:
- generic VitalData collection reader ที่ `[0x005F3E20, 0x005F406D)` เทียบ **exact-equality** กับ `message+0x10`
- ไบต์นั้นถูกตั้งโดย **prototype constructor ของ vital แต่ละตัวเอง** ด้วย `mov` ตรง ๆ
  (`0x5A19` -> bootstrap `0x007299B0` เขียน `0`)
⇒ ใบนี้คือ "ทำข้อเดียวกันกับ `0x0E80`": หา bootstrap/prototype ctor ของ `0x0E80` แล้วอ่านไบต์ที่มัน `mov`
VA ตั้งต้นที่มีอยู่แล้วในโปรเจกต์: `external/PF_PROTOCOL_REGISTRY.tsv` มีแถว `ForcePos` พร้อม VA

### 🔴 ทำไมเรื่องนี้เป็นคอขวดจริง (ไม่ใช่ความอยากรู้)
1. **มันคือไบต์เดียวที่กั้นระหว่าง "GM พิมพ์ /warp แล้วไม่มีอะไรเกิดขึ้น" กับ "ตัวละครขยับบนจอ"**
   สาย GM สร้างเส้นทางครบแล้วรอบ `gr2q9j`: `gm/chat_command_action.py` (ใหม่) รับบรรทัดแชท -> ตรวจ
   allowlist -> parse -> ประกอบเฟรม `ForcePos` ผ่าน `gm/warp_executor.py` -> คืน action ให้ dispatch ส่ง
   ทุกขั้นมีเทสเขียว **ยกเว้นขั้นสุดท้ายที่ถูกกั้นไว้เอง** ด้วย
   `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED = None`
2. **เดาไม่ได้ เพราะเดาแล้วฆ่าเซสชันของเจ้าของ** -- GT-101 (attended, OBSERVER_CONFIRMED 2026-08-27T14:39+07:00)
   วัดของจริง: ส่ง `0x5A19` ด้วย version ที่ยังไม่พิสูจน์ (`1`) -> client ขึ้น modal error เรียกชื่อ vital
   ตาม id -> **หยุดประมวลผลทั้ง connection แล้วปิด socket เอง**
3. **ไม่มีค่า default ของโปรเจกต์ให้ fallback** -- ค่าที่รู้แล้วสองตัวไม่เท่ากัน:
   `0x5A19` = `0` (RE-105) · `SELECT_ACTOR_VITAL` = `10` (`pf_login_game_server_v141.py:2205, 2289`
   พิสูจน์ด้วยทุก login ที่สำเร็จของโปรเจกต์นี้) ⇒ per-vital จริงตามที่ RE-105 บอก ห้ามอนุมาน

### objective
1. VA ของ prototype/bootstrap ctor ของ `0x0E80` และไบต์ที่มัน `mov` ลง `+0x10` (คำตอบหลัก)
2. 🔴 **คำถามที่สอง เพิ่มหลัง pf-adversary รอบ `gr2q9j`: สาม f32 ของ `ForcePos` คือแกนอะไร ตามลำดับไหน**
   `PF_SERIALIZER_FIELDS.tsv` พิสูจน์แค่ "f32 สามตัวที่ struct +0/+4/+8" **ไม่มีชื่อแกนในตาราง**
   ชื่อ `x, y, z` ใน `gm/teleport_wire.py::ForcePosBody` เป็นชื่อที่สาย GM ตั้งเอง [สมมติของสาย GM - รอ RE]
   และรอบนี้ทำให้มัน load-bearing (จับคู่ args ของคำสั่งกับ `Position.z`) · ลำดับ (x,y,z) ของ `Position`
   พิสูจน์แล้วกับ `make_login_teleport` **แต่นั่นคนละ message** สองชั้นที่ตรงกันคือความสอดคล้อง ไม่ใช่หลักฐาน
   ถ้าตัวที่สามไม่ใช่ระดับความสูง warp จะเอาตัวละครไปใต้พื้น -- อยากรู้ก่อนบูต ไม่ใช่ตอนบูต
3. (ถ้าทำได้ในใบเดียวกัน ไม่บังคับ) ค่าเดียวกันของ `TeleportVital` `0x25A2` และ `CWarpResult` `0x1BA4`
   -- สองตัวนี้เป็นขั้นถัดไปของ warp ข้ามฉาก จะได้ไม่ต้องเปิดใบซ้ำ
4. ถ้า `0x0E80` ไม่มี prototype ctor ในรูปเดียวกับ `0x5A19` -- เขียน bounded negative ว่าเส้นทางต่างกันตรงไหน
   แล้วปิด อย่าเดาค่า

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (VA/offset) · ชนเพดานให้เขียน bounded negative แล้วปิด
· ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ตัวเลขหนึ่งตัว + VA ของไซต์ที่เขียน **หรือ** bounded negative ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`
สิ่งที่สาย GM จะทำทันทีที่ได้คำตอบ: แก้ค่าคงที่ `FORCE_POS_VITAL_VERSION_CONFIRMED` **ค่าเดียว**
ในไฟล์เดียว (`src/pirateforce_foundation/gm/teleport_wire.py`) -- ไม่มีโค้ดอื่นต้องแก้ เทสรออยู่แล้ว
🔴 **ปิดใบแล้วแจ้งกลับในกล่องทันที**

**ADDRESSEE: RE** · ผู้เปิดใบ: LANE-GM (รอบ `gr2q9j`, 2026-08-28T18:24+07:00) -- ผลกลับมาที่สาย GM บริโภค

## RE-132 GM-GLOBAL-MESSAGE-VITAL-VERSION-001 [ARCHIVED 2026-08-31 R274, closed >24h per หัวข้อ 11] -- moved verbatim to `archive/CLIENT_RE_QUEUE_ARCHIVE_20260831_R274_closed.md` (was CLOSED/PASS since 2026-08-29; byte size corrected here: real span measured heading-to-next-heading is 8,059 B, not the 154,463 B cited in notes_to_chief/20260831_1747_PANYA-DECISION-*.md and repeated in the 22:55 CHASE3 letter -- that figure was a measurement error, not this entry)

## 🆕🔬 RE-137 NPCCONVERSATION-54B-WHOSE-SCRIPT-001 [STATIC-ON-CLOUD]: เฟรม 54 ไบต์ที่ `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` ส่ง -- descriptor ที่ถึงจอเป็นชุด `q3021` (Columbus) หรือ `q3020` (Sebastian)  [✅ **ANSWERED (ชั้นตาราง) - answered by `notes_to_chief/consumed/20260829_0238_LANE-A-RESULT-for-RE-137-the-54B-frame-is-not-what-titles-that-window.md`** · ปิดหัวใบโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 · **คำตอบคือ "ไม่ใช่ทั้งสองข้อ"**: เฟรม 54 ไบต์เป็น `q3021` แน่นอน **แต่ไม่ใช่สิ่งที่ตั้งชื่อ/เนื้อ/เสียงของหน้าต่างนั้น** — ไคลเอนต์ประกอบจาก `TEXTDATA_TH__MOBS_TIP.tsv` ของ template ที่มันเชื่อว่า actor ตัวนั้นเป็น (`n_ID=2` Sebastian · `s_NPC_VOICE 20;21`) ไม่ใช่จาก quest id ที่เราส่ง · มี **control** ในจดหมาย: กฎ decode เดียวกันคืนสตริงที่ขึ้นจอจริงในบูตเดียวกันสองอัน (`Atlantic Ocean:Rising Sun Sea`, `Port Royal`) · 🔴 **nonclaim**: VA ฝั่ง UI ที่อ่าน `MOBS_TIP` ยัง `[UNKNOWN]` — ต้องเปิดอิมเมจ ทำบนคลาวด์ไม่ได้ ⇒ อยู่กับ `GT-170` (`STATIC-ON-BRIDGE`) · จดหมายผลถูก consume ตั้งแต่ 29 ส.ค. แต่ไม่มีใครปิดหัวใบ = ค้างบัญชี 7 วัน ไม่ใช่ช่องเทส (พบโดยลูกมือตรวจของ chief รอบนี้ จากรายการกวาดของ ka1-A `20260905_0106`)]

**ADDRESSEE: RE** · ผู้เปิดใบ: chief (สาย E) รอบ `wi1m62` (R218) 2026-08-29T01:0x+07:00
**ต้นเรื่อง:** ใบผลเดียวกัน ข้อ ② · ปิดครึ่งที่ค้างของ `GT-102` (เกรด `PARTIAL` เพราะข้อนี้ข้อเดียว)

**สิ่งที่วัดแล้ว [MEASURED]:** คลิก Columbus ⇒ ยิง `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE`
(54 bytes) ครั้งเดียวจริง · หน้าต่างเปิดจริงพร้อมสองออปชัน · **แต่ป้ายผู้พูด = "Sebastian"**
เนื้อบทขึ้นต้น "Prison Exile Island ข้าคือผู้..." และ **เสียงพากย์ที่ดังขึ้นเป็นเสียง Sebastian**
(เจ้าของจำเสียงจากเซิร์ฟเวอร์ต้นฉบับได้ -- ยืนยันตอน 00:17)

**คำถาม:** ถอดไบต์ 54 ตัวนั้นทีละฟิลด์จาก builder ที่ commit แล้ว แล้วบอกว่า **เลข descriptor
ที่เราส่งจริงคือเลขอะไร** และตรงกับ `q3021` หรือ `q3020` ในตารางที่เรามี
[เสนอ ยังไม่วัด] คอนโซลบิลด์นี้พิมพ์เองว่า ChooseNPC path ส่ง "one **q3020** NPCConversation descriptor"
⇒ ถ้าจริง เราส่งบทของ Sebastian ทุกครั้งโดยไม่เกี่ยวกับ NPC ที่คลิก **ห้ามสรุปจากบรรทัดคอนโซลนั้นอย่างเดียว**

**เกณฑ์ผ่านสองชั้น**
- wire/DB: แผนที่ฟิลด์ครบ 54 ไบต์ + เลข descriptor ที่ส่งจริง พร้อม file:line ของ builder
- client-observable: ต้องเป็นใบเทสรอบใหม่ (แก้แล้วคลิก Columbus ต้องได้บทของ Columbus) -- ยังไม่เปิด

## 🔬 RE-138 NAME-LABELS-VANISH-AFTER-MOVE-001 [STATIC-ON-CLOUD]: ป้ายชื่อ (เขียว) ของทุกตัวในแมพหายหลังผู้เล่นเดินออกจากบริเวณแรก เหลือแต่ป้ายฉายา (ฟ้า) -- รอบ reconcile ส่งอะไรไม่ครบ  [✅ CLOSED/ANSWERED -- ปิดโดย chief (ผู้เปิดใบ) รอบ `l39ees` (R322) 2026-09-03T16:01+07:00 ตาม `COO-DECISION 20260903_1546` · ผล: `notes_to_chief/20260903_0253_RE-138-RESULT-BASICATTR-OMISSION-PRESERVES-NAME.md` · **คำถามของใบตอบแล้ว และสมมติฐานของใบเองถูกหักล้าง**: mask ที่แคบกว่า **ไม่ล้าง** ชื่อเดิม -- BasicAttr merge `0x00465610` ตรวจ bit `0x0001` ที่ `0x0046564E` แล้วเมื่อ bit **ถูกละ** จะ copy ชื่อเดิมจาก `source+0x28` (`0x00465654..0x0046565B`) ⇒ การที่เซิร์ฟเวอร์ละ name bit **ไม่ใช่** ต้นเหตุที่ป้ายชื่อหาย · ฝั่งเซิร์ฟเวอร์: retained กับ entrant ได้ BasicAttr mask `0x030C` เท่ากัน ไม่มี name bit ทั้งคู่ (`population.py:206-213`) ต่างกันแค่ entrant ได้ MovementAttr `0xFF` (`:214-223`) ⇒ ประโยค "retained เป็น NPCAttr-only" ไม่ได้แปลว่าไม่มี BasicAttr · 🔴 ~~ชั้น client-observable ของใบนี้ไม่เคยเปิด ⇒ ห้ามยกใบนี้ไปเป็นฐานว่า "ป้ายชื่อไม่หายแล้ว"~~ **ปิดแล้ว (LANE-A รอบ `2mnd7b` 2026-09-05T12:0x+07:00, NOW.md `1152` ข้อ 4)**: `GT-250` (R317, `notes_to_chief/20260905_1125_KA1A-R317-RESULTS-*.md` §2) วัดตรงอาการเดิม (ภาพ 235212 = ป้ายชื่อหายหลังเดินออกนอกสายตา) บนบิลด์ปัจจุบัน — เดินออกจนพ้นสายตา (X:-4,735 Y:-1,219) แล้วกลับ: **ป้ายชื่อครบทุกตัวเหมือนเดิม ไม่มีตัวไหนเหลือแต่ title** ⇒ **NEGATIVE, ไม่ reproduce** หลัง fix นี้ขึ้น main · ชั้น client-observable ของใบนี้ปิดด้วยผลลบที่วัดจริงแล้ว object lifetime / actor generation reuse ที่เคยเป็น nonclaim ค้างไว้ **ไม่ใช่ต้นเหตุที่ยังพิสูจน์อยู่ ณ ตอนนี้** เพราะอาการไม่เกิดให้ไล่ต่อ (ถ้าเกิดใหม่ในอนาคต NOW.md M-ladder ระบุเจ้าของถัดไป = LANE-A หลัง P-2) อาการที่เจ้าของเห็น (ภาพ 235212) **มีเจ้าของแล้ว: RE-138's BasicAttr-omission fix, ยืนยัน client-observable ด้วย `GT-250`** · chief ไม่เปิดใบใหม่ในรอบนี้ตามคำสั่ง `NOW.md` P-2 (ห้ามเปิด RE ใหม่) เสนอ COO ในจดหมายรอบ R322]

**ADDRESSEE: RE** · ผู้เปิดใบ: chief (สาย E) รอบ `wi1m62` (R218) 2026-08-29T01:0x+07:00
**ต้นเรื่อง:** ใบผลเดียวกัน ข้อ ④.2 (เจ้าของเห็นเอง ยืนยันแล้ว)

**สิ่งที่วัดแล้ว [MEASURED, ภาพ 235212]:** `Fighting Fish soldier` เหลือ title ฟ้าลอยเดี่ยว ไม่มีชื่อเขียว ·
`Loie` เหลือ "Royal Navy Engineer" ฟ้า ไม่มีชื่อ · ตัวที่มีแต่ป้ายฟ้าอยู่แล้ว = ป้ายหายทั้งใบ

**คำถาม:** ในรอบ reconcile หลังผู้เล่นเดิน โค้ดส่ง attr อะไรให้ตัวที่ **retained** และอะไรให้ตัวที่ **entrant**
-- ตัว retained ได้ `BasicAttr` (ที่ถือชื่อ) ซ้ำหรือไม่ ยกบรรทัดที่ตัดสินมาเป็น file:line
[เสนอ ห้ามใช้เป็นฐานใบอื่นจนกว่าจะวัด] คอนโซลบิลด์นี้เขียนเองว่า retained actors เป็น **NPCAttr-only**
ส่วน entrants ใช้ full-mask MovementAttr ⇒ ถ้าจริง ตัว retained เสียชื่อในรอบ reconcile โดยการ **ละ** ไม่ใช่การ **ลบ**
อ่านคู่กับ `RE-130` (reconcile แทนด้วย omission)

**เกณฑ์ผ่านสองชั้น**
- wire/DB: mask ที่ส่งจริงของ retained vs entrant พร้อม file:line · ระบุว่าชื่ออยู่ใน attr ตัวไหน
- client-observable: ใบเทสรอบใหม่หลังแก้ (เดินไปกลับแล้วป้ายชื่อยังอยู่) -- ยังไม่เปิด

🔴 นโยบายของบ้านนี้ข้อ 12 (ตัวละครสมประกอบ) แตะเรื่องนี้ตรง ๆ: "ส่ง attr ให้ครบที่สุดเท่าที่รู้
ไม่ใช่ขั้นต่ำที่พอไม่พัง" -- ใบนี้คือกรณีที่ขั้นต่ำที่พอไม่พัง ทำให้ผู้เล่นเห็นแมพที่ไม่มีชื่อใครเลย

### 🔎 กลไกที่เป็นตัวเก็งอันดับหนึ่ง -- เจอจากซอร์สรอบ `wi1m62` (chief + `pf-static-re`)
[วัดแล้ว ชั้นซอร์ส] `make_v98_conversation_face_state` (`current/pf_login_game_server_v141.py:1078-1106`)
**ประกอบสมาชิกทั้งฉากใหม่ทั้งหมด** จาก `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` ผ่าน
`make_npc_attr(template_id, aid, 1, 0, preset)` ทุกครั้งที่มีคนคลิกอะไรสักตัว
และ `make_npc_attr` (`v141:1139-1141`) **ไม่มีพารามิเตอร์ faction เลย** · ค่าตั้งต้น `basic_name=""`, `hp=100/100`
⇒ แพ็กเกต 10,610 ไบต์ทุกใบไม่มีชื่อ ไม่มี faction 6 ไม่มี HP ที่ขุดมา และใช้ template id ดิบของ Mob-Set
⇒ **ทุกคลิกล้าง `full_roster_override` ของทั้งเมืองในทางส่ง** (`runtime.py:6086-6094` เป็นคนใส่ค่านั้น)
🔴 [ยังไม่วัด — ห้ามข้ามไปสรุป] การส่ง NPCAttr ที่ mask แคบกว่า **ล้าง**ค่าเดิม (ชื่อ/faction) ในฝั่ง client
หรือไม่ ยังไม่มีใครวัด · `RE-092` พิสูจน์ replace-by-omission ที่ระดับ **ชุด actor** ไม่ใช่ระดับ **บิตใน mask**
⇒ นี่คือคำถามจริงของใบนี้ และเป็นคำถามที่ต้องใช้เครื่องสะพาน

### result: [✅ ANSWERED · 2026-09-03 · ใบผล `20260903_0253` · กรอกโดย chief R322 ตาม `COO-DECISION 20260903_1546`]

**ตอบคำถามของใบตรง ๆ (ชั้น wire/source):** retained และ entrant ได้ `NPCAttr` ทั้งคู่ ซึ่ง serialize `BasicAttr` mask `0x030C`
เท่ากัน และ **ไม่มี name bit `0x0001` ทั้งคู่** (`src/pirateforce_foundation/population.py:206-213`) · entrant ต่างตรงที่ได้
`MovementAttr` full mask `0xFF` เพิ่ม (`:214-223`) · ตัวประกอบแช่แข็งให้รูปเดียวกัน (`current/pf_login_game_server_v141.py:1139-1141`,
`:1149-1152`, `:1837-1853`) ⇒ ชื่ออยู่ใน `BasicAttr +0x28` และถูกส่งเฉพาะเมื่อ `basic_name` ไม่ว่าง

**ตอบคำถามที่ใบเขียนว่า "ต้องใช้เครื่องสะพาน" (ชั้น client static):** การละ bit **ไม่ล้างค่าเดิม** เมื่อมี attr เก่าให้ merge ·
`NPCAttr` merge `0x00466DC0` เรียก `BasicAttr` merge `0x00465610` · ที่ `0x0046564E` ทดสอบ `[destination+0x70] & 0x0001` ·
bit มี = ใช้ค่าที่ decode เข้ามา · **bit ถูกละ = copy `source+0x28` ทับ `destination+0x28`** (`0x00465654..0x0046565B`) ·
เป็น positive complete-function evidence ไม่ใช่ linear disassembly

**⇒ สมมติฐานอันดับหนึ่งของใบ (mask แคบกว่าล้างค่าใน attr object) ถูกหักล้าง**

**สิ่งที่ยังไม่ตอบ และห้ามใครอ่านผลนี้แล้วสรุปแทน**
- ชั้น client-observable **ไม่เคยเปิด** — ไม่มีใครเดินไปกลับแล้วดูป้ายในบิลด์นี้ · `G-OBS` ยังไม่มีลายเซ็น
- อาการจริงที่เจ้าของเห็น (ภาพ 235212) **ยังไม่มีต้นเหตุ** — เส้นทางที่เหลือคือ object lifetime / actor generation reuse
  (ถ้า reconciler สร้าง object ใหม่ ก็ไม่มี attr เก่าให้เติม ค่า default ชื่อว่างยังเป็นไปได้) หรือเส้นทาง UI อื่น
- **BUILD_IMPACT: ไม่ต้องแก้ client** · การเติม `basic_name` ใน population reconcile ยังสมเหตุผลตามนโยบายข้อ 12 (ตัวละครสมประกอบ)
  แต่เป็น **hardening ไม่ใช่ root-cause fix** ห้ามรายงานว่าแก้แล้วป้ายจะกลับมา

## 🔬 RE-191 MONSTER-NAME-COLOR-FONTSTYLE63-RGB-001 [STATIC-ON-BRIDGE]: `CODEX_CHECKPOINT 20260901_1135` closed the same-actor conditional static path for the monster-name-color write (`MCG-IMG-025..033` now `PROVEN_EXACT`, death branch conditionally writes style 63 via `CNetNPC` vslot `+0x3C` -> `0x0043BD70`) but never read the actual RGB triple that `fontstyle_id=63` resolves to through `UILabel_FontStyleID_parser_setter` (`0x00AA488F`) — what color does style 63 actually set, compared against the already-decoded controls 61/62? 🔴 **ไม่ใช่การยืนยันล่วงหน้าว่า 63 = เทา** — `20260901_0921_LANE-GM-STATUS-*.md`'s own nonclaim ①: "ไม่อ้างว่า fontstyle 63 คือสีเทาของมอนตาย — ตารางเองปฏิเสธการอ้างนี้ตรง ๆ" ใบนี้มีอยู่เพื่อหาคำตอบนั้น ไม่ใช่เพื่อยืนยัน `NOW.md` P-2's ตาย=เทา ที่ยังไม่มีหลักฐาน  [🟢 **CLOSED PASS/DONE (ชั้น conditional static + DATA palette เท่านั้น; runtime pixels ยังเปิด) — ผลมาถึง 2026-09-01T14:39+07:00 (Codex static RE), ปิดหัวใบโดย LANE-GM รอบ `wggs0i` 2026-09-02T10:35+07:00 ตามสัญญาผู้บริโภคของใบเอง, ดูผลด้านล่าง**] ~~[OPEN — assigned LANE-GM]~~

### ทำไมเปิดใบนี้ (มอบหมายตรงจาก COO)

`COO-DECISION 20260901_1241_p2-re-routing-fontstyle63` (`ADDRESSEE: chief`) สั่งตรงให้ chief มอบข้อนี้
ให้สาย RE/Codex เป็นลำดับแรกของรอบถัดไปที่มี capacity — **นี่คือรอบที่สามที่สาย GM ขอเรื่องนี้**
(`h6rsgl` → `p4cndg` → `sched-20260901`, ใบล่าสุด `notes_to_chief/20260901_1225_LANE-GM-STATUS-*.md`)
โดยไม่มีของใหม่ให้ทำต่อเพราะติดอยู่ที่ข้อเดียวนี้ P-2 (สีชื่อมอนสเตอร์) เป็นหนึ่งในสามอันดับสูงสุดของ
`PANYA-ORDER 20260901_0215` — ไมล์สโตนอื่นทั้งหมดพักไว้จนกว่า P-1/P-2 จะปิด และ `GT-146`/ใบตีมอนทุกใบ
ถูกล็อกจนกว่า P-1/P-2 จะปิด ⇒ ข้อนี้คือคอขวดเดียวที่เหลือของ P-2 ทั้งก้อน ไม่ใช่แค่ของสาย GM

`CODEX_CHECKPOINT 20260901_1135` ระบุวิธีปิดไว้เองแล้ว (static/IMAGE-layer ล้วน — **ไม่ต้อง attended
capture**): เทียบ `fontstyle_id=63` กับ 61/62 ที่ถอดแล้วเป็น control ผ่าน parser/setter ตัวเดียวกัน
(`0x00AA488F`) — ใบนี้ทำแค่จุดเดียวที่ checkpoint ทิ้งไว้เปิด ไม่เปิดเลนใหม่

### ค้นแล้ว (ก่อนเปิดใบ ตามกฎบังคับข้อ ④)

`pf_bridge/external/PF_MONSTER_COLOR_GATE.tsv`/`.md` ที่ checkpoint อ้างถึง (SHA-256 `f99347e4...`/
`7b6626ac...`) **ยังไม่มีในโคลนคลาวด์นี้** (`external/` ไม่มีไฟล์ชื่อนี้ ณ commit ที่ fetch รอบนี้ —
`git log --oneline -- external/` ล่าสุดคือ sync ไฟล์เดียวตอน 05:24 ไม่ใช่ไฟล์นี้) — **สาเหตุ (แก้ไขจาก
draft แรกที่เข้าใจง่ายเกินไป, pf-adversary จับได้):** ไม่ใช่แค่รอคนหน้าสะพาน `git add` — `.gitignore` ของ
`pf_bridge` ใช้ deny-all กับ `external/` (`/external/*` แล้วค่อย allowlist ทีละไฟล์ตรง ๆ) และ
`PF_MONSTER_COLOR_GATE.tsv`/`.md` (รวมถึง `PF_GROUND_DROP_LIFETIME.tsv`/`.md`) **ยังไม่อยู่ใน allowlist
นั้นเลย** ⇒ ต้องแก้ `.gitignore` เพิ่มบรรทัด allow ตรงชื่อไฟล์ก่อน แล้วค่อย `git add` (`pf_git_sync.ps1`'s
`SHARED_TRACKED` สแกนด้วย `--untracked-files=no` — ไฟล์ที่ gitignore กันไว้จะไม่มีวัน sync แม้ `git add`
เพราะไม่มีทาง track ได้ตั้งแต่แรก) — เข้าเค้าเดียวกับ "deny-all `.gitignore` กลืนทั้งโฟลเดอร์" ที่โปรเจกต์นี้
เจอมาก่อน — **ไม่ใช่เหตุให้ปิดใบหรือหยุดรอ**: งานถอด RGB ทำบนอิมเมจโดยตรง (RE
runner/Codex บนสะพาน) ไม่ต้องพึ่งไฟล์นี้ในคลาวด์เลย ไฟล์นี้เป็นแค่บริบทอ้างอิง ถ้าใครเจอไฟล์หายบนสะพานเอง
ให้บันทึกลง `IMAGE_ACCESS_COST.tsv` ตามกติกา

### สิ่งที่ต้องตอบ

1. RGB triple (หรือ ARGB ถ้า parser คืนแบบนั้น) ที่ `fontstyle_id=63` ตั้งจริงผ่าน
   `UILabel_FontStyleID_parser_setter` (`0x00AA488F`) — อ่านจากตารางค่าคงที่/args ของ call site เดียวกับ
   ที่ปิด 61/62 แล้ว ไม่ใช่การเดาจากชื่อ "เทา"
2. ค่าที่ได้เทียบกับ 61/62 อย่างไร (ทั้งสามค่าคนละสี / บางคู่ซ้ำกัน) — บันทึกทั้งสามค่าไว้ในผลเดียวกัน
   เพื่อกันเปิดใบซ้ำถ้าอนาคตต้องการ cross-check style อื่น
3. ระบุด้วยว่า path นี้เป็น conditional (ตามที่ checkpoint บอกว่า `MCG-IMG-025..033` ยัง "conditional
   static path" ไม่ใช่ unconditional render) — RGB ที่พบเป็นค่าที่ตั้งเมื่อ path นี้ทำงานจริงเท่านั้น
   ไม่ใช่การยืนยันว่า path ทำงานทุกครั้ง (ข้อนั้นเป็นคำถามคนละชั้น ไม่ใช่ของใบนี้)

### pass criteria

- **PASS**: RGB ของ 63 อ่านได้ตรงจาก parser/setter เดียวกับ 61/62 พร้อม provenance (VA/offset/args)
  ครบเหมือนที่ปิด 61/62 ไปแล้ว — ปิดใบ ส่งผลกลับให้ chief ต่อสาย GM ไปใช้เขียนโค้ดสี (ยังไม่ใช่งานของใบนี้)
- **BOUNDED-NEGATIVE**: parser คืนค่าที่ resolve ไม่ได้ตรง ๆ (เช่น ต้องผ่าน lookup table ที่ยังไม่ถอด) —
  เขียนไว้ตรง ๆ ว่าต้องถอดอะไรเพิ่มก่อนถึงจะปิดได้ ไม่ใช่เดาสี

### ข้อห้าม

ห้ามเขียนโค้ดสีมอนสเตอร์ใด ๆ จากใบนี้ (ขัด `RE-109` `BUILD_IMPACT: NONE` — สาย GM ยืนยันเองในจดหมาย
`1225` ว่ายังไม่เขียนโค้ดจนกว่าจะรู้ RGB จริง) · ห้ามเดาว่า 63 = เทา จากชื่อ state โดยไม่มี provenance
จากไบนารี

### สัญญาผู้บริโภค

เปิดโดย chief (มอบหมายตรงจาก `COO-DECISION 20260901_1241`) — **สาย GM บริโภคผล** (ผู้ที่ขอเรื่องนี้มา
สามรอบและเป็นผู้เขียนโค้ดสีต่อ) ตามกฎ "ใครเปิดใบคนนั้นบริโภค" ข้อยกเว้นที่ chief เปิดแทนเพราะเป็นงาน
มอบหมายข้ามสาย (RE/Codex ไม่ใช่ chief ไม่ใช่ GM) — สาย GM อ่านผลรอบถัดไปที่เห็นแล้วปิดหัวใบเอง

### links

`notes_to_chief/CODEX_CHECKPOINT_20260901_1135_COLOR-DROP-GM-STATIC-UNLOCK.md` (วิธีปิดที่ checkpoint
ระบุไว้) · `notes_to_chief/20260901_1241_COO-DECISION-p2-re-routing-fontstyle63-third-round-waiting.md`
(คำสั่งมอบหมายตรง) · `notes_to_chief/20260901_1225_LANE-GM-STATUS-sched-20260901-*.md` (รอบที่สามที่ขอ)
· `notes_to_chief/20260901_0921_LANE-GM-STATUS-p2-color-static-research-fontstyle63-gap-re-followup-proposed.md` (รอบ `h6rsgl` ที่เสนอวิธีปิดนี้ครั้งแรก) ·
`pf_bridge/NOW.md` P-2


### result — 🟢 CLOSED PASS/DONE (ปิดหัวใบโดย LANE-GM รอบ `wggs0i` 2026-09-02T10:35+07:00)

ผล: `notes_to_chief/20260901_1439_CODEX-RE191-RESULT-FONTSTYLE63-RGBA.md`
(LANE-GM บริโภคไปแล้วตั้งแต่รอบ `r2jfjm` — มี `.CONSUMED.txt` คู่กัน) — **แต่หัวใบไม่เคยถูกปิด**
จึงค้างอยู่ใน `python tools_bridge/pf_re_queue_taglint.py --list-open` ต่อมาอีก ~20 ชม.

🔴 **ทำไมเครื่องมือถึงมองไม่เห็นว่าใบนี้มีผลแล้ว (วัดจริงรอบนี้ ไม่ใช่สมมติฐาน):**
`pf_re_queue_taglint.py::has_result_letter()` เทียบ `ticket_id in filename` ตรงตัว = มองหา `"RE-191"`
แต่ชื่อไฟล์ผลเขียนว่า `CODEX-RE191-RESULT-...` (**ไม่มีขีด**) ⇒ ไม่แมตช์ ⇒ ใบถูกรายงานว่ายังเปิด
`tools_bridge/` ไม่ใช่เขตเขียนของสาย GM — แจ้ง chief ไว้ในใบ `20260902_1035_LANE-GM-TO-CHIEF-*`
(นี่เป็นคนละเรื่องกับข้อสังเกตของ ka1-B ใบ `0955` ที่ว่า runner ข้ามเพราะป้าย `assigned LANE-GM`
ซึ่ง ka1-B ติดป้าย `[สมมติฐาน]` ไว้เอง — รอบนี้ไม่ยืนยันและไม่หักล้างข้อนั้น วัดได้แค่ข้อของเครื่องมือ)

**คำตอบของใบ (สรุปสามบรรทัด — ตัวเลขจริงอยู่ในใบผล ไม่คัดลอกมาที่นี่ และไม่คัดลอกลงโค้ด
ตาม "ข้อห้าม" ของใบนี้เอง):**
1. คำถามหลักปิดแล้ว: FontColor/OutlineEffectColor RGBA ของ 61 / 62 / 63 อ่านได้ครบทั้งสามค่าพร้อม provenance
   `[ORIGINAL EVIDENCE: DATA]` แยกจาก `[ORIGINAL EVIDENCE: IMAGE / MCG-IMG-057..058]`
2. **premise ของใบถูกแก้โดยผลเอง**: `0x00AA488F` **ไม่ใช่** RGB parser — เป็น branch ของ `UILabel.FontStyleID`
   ตัว palette จริงเดินผ่าน `0x00A9DAE0` (มี direct caller แค่ 2 จุดจาก full six-section E8 census)
3. เพดานที่ยังยืน: conditional static + DATA เท่านั้น · **ไม่ได้แปลว่า style 63 = ตาย ในทุกบริบท**
   และยังไม่มีหลักฐานว่า live actor ผ่าน gate นั้น (ต้องเห็น live registry node + requested/applied ID + pixels)

**คำถามที่เหลือของ P-2 ไม่ใช่ RGB อีกต่อไป** แต่เป็น reachability — เดินต่อและปิดใน `RE-195` ด้านล่าง
(ผลลัพธ์: ยังทำไม่ได้ในวันนี้) · ข้อห้าม "ห้ามเขียนโค้ดสีมอนสเตอร์จากใบนี้" **ยังยืนอยู่** และรอบ `wggs0i`
ปฏิบัติตามโดยไม่คัดลอก palette ลงรีโปเลยแม้แต่ค่าเดียว

## 🔬 RE-229 CHARCREATE-CLASS-SSCORE-STARTING-STATS-SOURCE-001 [🟢 **CLOSED BOUNDED-NEGATIVE/DONE — RE runner local 2026-09-04T10:50+07:00, ปิดหัวใบโดย LANE-DB รอบ `1szq3m` 2026-09-04T11:4x+07:00, ดูผลด้านล่าง**] ~~[OPEN -- 🔴 `[STATIC-ON-BRIDGE]` · 🔴 **ขอบเขตแคบลงในรอบเดียวกัน หลัง `pf-adversary` พบว่า `RE-122` ตอบไปแล้วครึ่งใบ — อ่านบล็อกแก้ก่อนทำ**]~~

ผล: `notes_to_chief/20260904_1053_RE-229-RESULT-BOUNDED-NEGATIVE-NO-SIX-TO-FIVE-CROSSWALK.md` — ไม่พบ field/consumer ที่ผูก component ทั้งหกของ `s_SCORE` (`STATUS_STR/AGI/CON/INT/PER/CHA`) เข้ากับห้า ActorAttr wire fields ในขอบเขต manifest (`external/` + `gamedata/`) ที่ค้นแล้ว — คำตอบคือ **UNPROVEN** ไม่ใช่ `CHA` โดยอัตโนมัติ ห้ามใช้สมมติฐาน `AGI->DEX`/ทิ้ง `CHA` `BUILD_IMPACT: hard guard / keep current fallback` — LANE-DB คง `DEFAULT_PRIMARY_STAT = 100` ต่อ ห้าม seed `4;3;4;1;1;2` หรือ permutation ใดจาก `s_SCORE` นี่คือ **method ceiling** (ห้าม rerun ด้วย corpus/image เดิม) ไม่ใช่ time checkpoint — ชิ้น 2/5 ของ PLAYER/CHARACTER ยังไม่มีกำหนด ตาม `COO-DECISION 20260904_0745`/`0942`

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `8nh6q5`/R334 2026-09-04T07:5x+07:00 ตาม `COO-DECISION 20260904_0746` ข้อ 1**
> ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน `228` (ใบ `GT-228`) ⇒ ใบนี้ `RE-229` · `RE-229`/`GT-229` = 0 hit ทั้งสามที่ก่อนวาง
> **เปิดตามคำขอของ LANE-DB** (`notes_to_chief/20260904_0542_LANE-DB-RE-TICKET-piece-2-starting-stats-has-no-committed-source-table.md` · ค้างสองรอบ)
> **เจ้าของใบ = chief (มอบหมาย) · ผู้บริโภคผล = LANE-DB** (ชิ้น 2/5 ของงาน PLAYER/CHARACTER)

> 🔴🔴 **แก้ขอบเขตในรอบเดียวกัน (chief `8nh6q5`/R334 2026-09-04T09:0x+07:00 · ที่มา: `pf-adversary` D2)**
> ผมเปิดใบนี้โดย **ไม่ได้ค้น `CLIENT_RE_QUEUE.md` เอง** และเชื่อคำอธิบายในจดหมายของ LANE-DB ชั้นเดียว (ผิดกฎ G1)
> ความจริงคือ **`RE-122 PLAYER-STANDARD-STATUS-AND-CHARCREATE-SCORE-VALUES-001` (`CLIENT_RE_QUEUE.md:1662`)
> ตอบคำถามนี้ไปแล้วตั้งแต่ 2026-08-28 สถานะ `DONE / BOUNDED-NEGATIVE`**
> จดหมายผล: `notes_to_chief/consumed/20260828_0815_RE-122-RESULT-SCORE-IS-SIX-AXIS-MP-UNPROVEN.md`
>
> **สิ่งที่ `RE-122` ตอบไปแล้ว — ห้ามสั่ง runner ทำซ้ำ**
> - **(ก) ตอบแล้ว**: `s_SCORE` = **six-axis char-create score** ผูกกับ
>   `GameClient/Data/GUI/Model/Login_CharCreate_Main.model` (SHA `eef1eb1a…`) แกนคือ
>   **`STATUS_STR` · `STATUS_AGI` · `STATUS_CON` · `STATUS_INT` · `STATUS_PER` · `STATUS_CHA`**
>   🔴 **ไม่ใช่ `STR/CON/DEX/INT/PER + ตัวที่หก` อย่างที่ผมเขียนไว้ข้างล่าง** — ช่องที่หกคือ `CHA` และมีหลักฐานพินแล้ว
> - **(ข) ตอบแล้ว**: `CONSTDATA_TH__POTENTIAL.tsv` SHA `d798d5ac…` = **11 คอลัมน์ 0 แถวข้อมูล** พร้อมสแปน loader
>   `0x004A2C00..0x004A4500` (SHA `e567f27c…`) · `docs/FUNCTIONAL_COVERAGE.json` ไปไกลกว่านั้น:
>   ตัวเลขเส้นโค้งความก้าวหน้า **ไม่ได้อยู่ในไฟล์รันเลย** มีแต่ชื่อคอลัมน์กับโค้ดที่ไปอ่าน static data ภายนอก
>   ⇒ **ทางเลือก (ข) ปิดแล้ว ห้ามให้ runner ไปเปิดใหม่**
> - `RE-122` มี **คำสั่งห้าม rerun** เขียนไว้เอง และระบุ objective เดียวที่จะปลดล็อกได้:
>   *"recovered crosswalk ที่ผูก six-axis UI score เข้ากับห้า wire fields"*
>
> 🔴 **ข้ออ้างที่ผมยกมาผิด และถอนทิ้ง**: ที่เขียนว่า `reports/PF_JOB001_..._20260816.md` "นับ `s_SCORE` รวมใน
> 37 other columns" — `RE-122` §T1 ระบุว่ารายงานนั้น **stale** (มัน 37 คอลัมน์และ **ไม่มี `s_SCORE` อยู่เลย**)
> วัดสดรอบนี้: `CONSTDATA_TH__CHARCREATE_CLASS.tsv` มี **38 คอลัมน์ · `s_SCORE` = คอลัมน์ที่ 3 · 5 แถว** ตรงกับ `RE-122`
> · docstring ของ `class_catalog.py` ที่ผมยกไปยืนยันให้ LANE-A/LANE-DB **ก็ stale ด้วย** อ้างรายงานฉบับเดียวกัน
>
> **⇒ คำถามที่เหลือจริงของใบนี้ เหลือข้อเดียว (แทนคำถาม (ก)/(ข) ข้างล่างทั้งคู่)**
> **มี crosswalk ที่ผูกหกแกนของ UI (`STR/AGI/CON/INT/PER/CHA`) เข้ากับ *ห้า* wire fields ที่เซิร์ฟเวอร์ส่งจริง
> หรือไม่ · ถ้ามี แกนไหนหายไปและใครกินช่องนั้น** (นี่คือ objective ที่ `RE-122` เขียนไว้เองว่าจะปลดคำสั่งห้าม rerun)
> 🔴 **ห้าม runner เริ่มก่อนอ่าน `RE-122` + จดหมายผลของมันจบทั้งฉบับ** · ถ้า `RE-122` ตอบครบแล้วจริง ให้ปิดใบนี้
> เป็น `SUPERSEDED - covered by RE-122` แล้วบอกกลับมา **นั่นคือผลที่ใช้ได้ ไม่ใช่ใบล้ม**
>
> **ค้นใน `pf_bridge\external\` แล้ว:** (สาย RE กรอก — 🔴 chief เปิดใบครั้งแรกโดยลืมแถวนี้ ถือเป็นข้อบกพร่องของใบ)
> **ค้น `gamedata` แล้ว:** (สาย RE กรอก — เช่นเดียวกัน)
>
> 🟢 **ข่าวดีสำหรับ LANE-DB**: หกแกนมีชื่อและมีหลักฐานพินแล้วตั้งแต่ 28 ส.ค. ⇒ ชิ้น 2 อาจ **ไม่ต้องรอใบนี้เลย**
> ดูจดหมาย `notes_to_chief/20260904_0905_CHIEF-TO-LANE-DB-CORRECTION-*.md`

- **ถาม (สองเส้นทาง ตอบได้เส้นใดเส้นหนึ่งก็พอ ไม่ต้องตอบทั้งคู่)**
  - **(ก)** คอลัมน์ `s_SCORE` ใน `gamedata/tables/CONSTDATA_TH__CHARCREATE_CLASS.tsv` (หกตัวเลขคั่น `;`
    ต่อแถว เช่น Gladiator `4;3;4;1;1;2`) ไคลเอนต์อ่านไปทำอะไร · **ลำดับของหกช่องคืออะไร**
    (สมมติฐานที่ต้องหักล้างหรือยืนยัน: STR/CON/DEX/INT/PER + ตัวที่หกอีกหนึ่ง) ·
    ค่าที่อ่านได้เป็น **ค่าสแตทเริ่มต้นจริง** หรือเป็นน้ำหนัก/แถบพรีวิวตอนสร้างตัว หรืออย่างอื่นทั้งดุ้น
  - **(ข)** `gamedata/tables/CONSTDATA_TH__POTENTIAL.tsv` มีแต่ header ไม่มีแถวใน snapshot นี้ —
    ในไบนารีไคลเอนต์มีแถวจริงของตารางนี้ที่ยังไม่ถูกดึงเข้า `gamedata/tables/` หรือไม่ ·
    ถ้ามี ให้คืนสคีมา + แถว พร้อมที่อยู่ที่ดึงมา

- **ทำไมถึงเปิดใบ (วัดแล้ว ไม่ใช่สมมติฐาน — LANE-DB `0542`)**
  ชิ้น 2/5 คือ "ค่าเกิดจากตารางแทน `DEFAULT 100`" แต่สองตารางที่ `PANYA-DECISION 20260904_0328` ระบุชื่อไว้
  **ไม่มีคอลัมน์สแตทเริ่มต้นต่อคลาสเลย**:
  1. `CONSTDATA_TH__STANDARD_STATUS.tsv` 255 แถว = ตาราง EXP/แต้มความสามารถ **ต่อเลเวล**
     (`n_ID`=เลเวล · `n_EXP_CURRENTLV` · `n_POINT_ABILITY` · `n_DEADLOSS` · `n_PVP_*` · `n_DEFENCE_CONSTANT`) ·
     `n_POINT_ABILITY` = แต้มที่ได้ตอนเลเวลอัพ (0 ที่เลเวล 1) ไม่ใช่ค่าที่มีอยู่แล้ว
  2. `CHARCREATE_CLASS.s_SCORE` = ตัวเลือกเดียวที่รูปร่างเหมือนสแตท แต่ **ไม่เคยถูก RE เลย** —
     `class_catalog.py` บน main เขียนใน docstring ของตัวเองว่า "s_SCORE's semantics have never been RE'd" ·
     `reports/PF_JOB001_CHARCREATE_CLASS_STATIC_BOUNDARY_20260816.md` นับมันรวมใน "37 other columns" โดยไม่ถอดสักตัว
  3. `POTENTIAL.tsv` = ตารางเดียวที่ `docs/FUNCTIONAL_COVERAGE.json` เรียกว่าผู้สมัครจริง แต่ไม่มีแถว

- **สิ่งที่ยังไม่ใช่หลักฐาน (nonclaim บังคับของใบนี้)**
  🔴 **ความยาวหกช่องเข้ากับจำนวนสแตทที่เราคิดว่ามี = ความเข้ากันได้ ไม่ใช่การพิสูจน์** ·
  ห้ามใครประกาศลำดับช่องจากการนับจำนวนหรือจากค่าที่ "ดูสมเหตุสมผล" ·
  ห้ามยกใบนี้ปิดด้วยการอ่าน `.tsv` ซ้ำ — คำตอบต้องมาจากโค้ดที่ **อ่านคอลัมน์นี้** ในอิมเมจ (G6: ห้ามประกาศความหมายของฟิลด์จากการอ่านครั้งเดียว)

- **อิมเมจที่ต้องยึด**
  `GameClient.local.bin` 14,759,424 ไบต์ sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
  ทางเข้าที่แนะนำ: ตัวโหลด `CHARCREATE_CLASS` (ชื่อตาราง/ชื่อคอลัมน์เป็นสตริงในอิมเมจ) → ตัวที่ split `;`
  → ผู้บริโภคของแต่ละช่อง · เทียบกับ `POTENTIAL` loader เส้นคู่ขนาน

- **เกณฑ์ปิด (ชั้นเดียวพอ — ใบนี้เป็น static ล้วน ไม่มีชั้น client-observable)**
  ① ระบุสแปนที่อ่าน พร้อม `span_sha256` ทุกสแปน (`RE_STATIC_SEARCH_RULES.md` §1) ·
  ② สำหรับ **แต่ละช่องในหกช่อง** ระบุ consumer crosswalk จริง หรือประกาศตรง ๆ ว่าช่องนั้น `opaque` ·
  ③ ตอบแบบ **bounded** ได้ ถ้าตอบได้บางช่อง — ระบุว่าช่องไหนค้างและค้างเพราะอะไร
  🔴 ตอบไม่ได้เลยก็เป็นผลที่ใช้ได้ (`BOUNDED-NEGATIVE`) — LANE-DB จะได้เลิกรอและคง `DEFAULT 100` ต่ออย่างเปิดเผย

- **ผลไปถึงใคร**: จดหมายผลจ่าหน้า **LANE-DB** (cc chief, COO) · LANE-DB บริโภคเองและปิดหัวใบนี้ในรอบที่ผลถึง
  (กฎ "ใครเปิดใบคนนั้นบริโภค" — ใบนี้เปิดแทน LANE-DB ตามคำขอของเขา)
- **ผู้ทำ**: **สาย RE (RE runner local)** — สายเดียว ไม่ต้องจอง · route `STATIC-ON-BRIDGE` เพราะต้องดิสแอสเซมบลีอิมเมจ ⇒ ทำบนคลาวด์ไม่ได้
- **ผลกระทบถ้าไม่ตอบ**: ชิ้น 2/5 ของ PLAYER/CHARACTER **ไม่มีกำหนด** (`COO-DECISION 20260904_0745`) · `DEFAULT 100` คงไว้ ห้ามเดา

---

## 🔬 RE-232 SCAST-CONDITION-BEHAVIOR-TOKEN-GRAMMAR-001 [~~OPEN -- 🔴 `[STATIC-ON-BRIDGE]`~~ 🔵 **DONE / BOUNDED-NEGATIVE — ปิดโดย LANE-CS รอบ `tp9rpy` 2026-09-04T12:1x+07:00 ตามผล `notes_to_chief/20260904_1055_RE-232-RESULT-BOUNDED-NEGATIVE-EIGHT-ROWS-DO-NOT-CLASSIFY.md`: grammar มีโครงสร้าง condition-line → behavior-line จริง แต่ 8-row sample ที่ขอบเขตใบนี้กำหนดไม่มีตัวแทน AOE/self-buff/heal ที่ label ได้อิสระเลยสักแถว ⇒ แยก single-target/AOE/self-buff/heal ไม่ได้จากกลุ่มตัวอย่างนี้ · `BUILD_IMPACT: no classifier change` (`damage_by_skill.py`/`skill_catalog.py` เก็บ `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` เป็น raw field ต่อไป) · เดินต่อได้เฉพาะถ้ามีใบใหม่แยกต่างหากที่เพิ่ม ≥8 แถว label อิสระ (2 single-target + 2 AOE + 2 self-buff + 2 heal) เป็น 16-row targeted follow-up — ใบนั้นยังไม่มีอยู่ ณ รอบที่ปิดนี้**]

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `2vfbtf`/R335 2026-09-04T09:3x+07:00 ตาม `COO-DECISION 20260904_0848` ข้อ 5**
> ตัวนับร่วมสองคิว คืน `231` (`GT-231`) ⇒ ใบนี้ `RE-232` · `RE-232`/`GT-232` = 0 hit ทั้งสามที่ก่อนวาง (`CLIENT_RE_QUEUE.md`, `GAME_TEST_QUEUE.md`, `archive/*QUEUE*ARCHIVE*`)
> **เปิดตามคำขอของ LANE-CS** (`notes_to_chief/20260904_0755_LANE-CS-TO-COO-round-6o11t1-orphan-closed-marker-risk-found-npassive-is-not-the-type-column.md` ข้อ 4)
> **เจ้าของใบ = chief (มอบหมาย) · ผู้บริโภคผล = LANE-CS**

- **ถาม**: token grammar ของคอลัมน์ `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` (มินิแลงเกวจ `GO(0)`, `CHASE(n)`, `SKIP(n)`, `ISVIP_I(n)`, ... ที่ `GT-052` 24 ส.ค. นับ token distinct ไว้ 224/2112 ตัว ยังไม่มีใครถอด) แยกแยะ "โจมตีเป้าเดียว vs AOE vs buff ตัวเอง vs heal" ได้จริงหรือไม่ · ถ้าได้ กติกา token ที่แยกแต่ละคู่คืออะไร
  🔴 **ขอบเขตแคบ ตามคำขอของ LANE-CS เอง**: ถอดเฉพาะแถวของ **8 สกิลที่มีอยู่ในสารบัญตอนนี้** (`skill_catalog.py` บน main) — **ห้ามขยายไปตาราง `s_CAST_*` เต็ม 2,165 แถว** ในใบนี้ ถ้าผลจาก 8 สกิลชี้ว่าต้องขยาย ให้เปิดใบใหม่แยกต่างหากพร้อมเหตุผล

- **ทำไมถึงเปิดใบ (วัดแล้ว ไม่ใช่สมมติฐาน — LANE-CS `0755` ข้อ 3)**
  `n_PASSIVE` (คอลัมน์ที่เคยสงสัยว่าเป็นชนิดสกิล basic/attack/AOE/buff/heal/passive) **ถูกหักล้างแล้วสองทาง**
  (`pf-static-re` ไล่ title/description ทั้ง 6 ค่า + `pf-adversary` ตรวจ 8 สกิลที่รู้จักคู่ขนาน): สกิล 99
  "Normal Attack" มี `n_PASSIVE=2` **เท่ากับ** สกิลกระโดด 110/111 (ไม่ใช่โจมตี) และ **ต่างจาก** Basic
  Training ทั้งห้า (`n_PASSIVE=1` ทั้งหมด) · แพทเทิร์นจริงดูเหมือนเป็น "แถวนี้เป็นของระบบย่อยไหน" ไม่ใช่ชนิด
  สกิลเชิงเกม — ปักไว้แล้วด้วยเทส `NPassiveIsNotATypeColumnTests` ใน `tests/test_skill_catalog.py`
  ⇒ **`n_PASSIVE` ปิดทางนี้แล้ว** ที่เหลือที่ยังไม่ลองคือ `s_CAST_CONDITION`/`s_CAST_BEHAVIOR`

- **สิ่งที่ยังไม่ใช่หลักฐาน (nonclaim บังคับของใบนี้)**
  🔴 **ผลจาก 8 สกิลนี้ไม่ใช่การพิสูจน์ว่ากติกาใช้ได้กับตารางเต็ม** — 8 แถวคือกลุ่มตัวอย่างเพื่อตอบคำถาม
  "grammar นี้มีศักยภาพตอบคำถามหรือไม่" ไม่ใช่การ derive กติกาสุดท้าย · ห้ามอ้างว่าปิดคำถามชนิดสกิลทั้งระบบ
  จากใบนี้ใบเดียว · ห้ามประกาศความหมาย token จากการอ่านครั้งเดียว (G6) — ต้องยันกับ ≥2 สกิลต่อ token ที่อ้างว่าเข้าใจ

- **อิมเมจที่ต้องยึด**
  `GameClient.local.bin` 14,759,424 ไบต์ sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
  ทางเข้าที่แนะนำ: ตัวโหลด/ตัว parse `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` ของ 8 สกิลใน `skill_catalog.py`
  → ตัวแปล token (`GO`/`CHASE`/`SKIP`/`ISVIP_I`/...) → ผู้บริโภคของแต่ละ token ในโค้ดฝั่งไคลเอนต์

- **เกณฑ์ปิด (ชั้นเดียวพอ — ใบนี้เป็น static ล้วน ไม่มีชั้น client-observable)**
  ① ระบุสแปนที่อ่าน พร้อม `span_sha256` ทุกสแปน (`RE_STATIC_SEARCH_RULES.md` §1) ·
  ② สำหรับ 8 สกิล ระบุว่า token ไหนแปลได้ + ความหมาย พร้อมหลักฐาน ≥2 จุดต่อ token ที่อ้าง หรือประกาศ `opaque` ตรง ๆ ·
  ③ ตอบตรง ๆ ว่า grammar นี้แยก "โจมตีเป้าเดียว vs AOE vs buff ตัวเอง vs heal" ได้หรือไม่จากกลุ่มตัวอย่างนี้ ·
  ④ ตอบแบบ `BOUNDED-NEGATIVE` ได้ ถ้า 8 สกิลไม่พอสรุป — ระบุว่าต้องขยายไปกี่แถวจึงจะพอ

- **ผลไปถึงใคร**: จดหมายผลจ่าหน้า **LANE-CS** (cc chief) · LANE-CS บริโภคเองและปิดหัวใบนี้ในรอบที่ผลถึง
- **ผู้ทำ**: **สาย RE (RE runner local)** — สายเดียว ไม่ต้องจอง · route `STATIC-ON-BRIDGE` เพราะต้องดิสแอสเซมบลีอิมเมจ ⇒ ทำบนคลาวด์ไม่ได้
- **ผลกระทบถ้าไม่ตอบ**: LANE-CS ไม่มีเส้นทางอื่นตอบคำถามชนิดสกิลตอนนี้ · ไม่บล็อกอะไรใน M1-M5 (LANE-CS ยังไม่แตะดาเมจจนกว่าจะอ่าน `mob_combat.py` ของ LANE-B ให้ครบตาม `0755`)

---

## 🔬 RE-240 HOTBAR-SKILL-KEY-TO-PRODUCER-WALK-001  [~~OPEN -- 🔴 `[STATIC-ON-BRIDGE]` · ผู้เปิดใบ = **chief (LANE-E)** รอบ `wjqykr`/R338 · ผู้ทำ = **สาย RE (RE runner local)** · **ผู้บริโภคผล = LANE-CS**~~ 🔵 **DONE / BOUNDED-NEGATIVE — ปิดโดย LANE-CS รอบ `1z31do` 2026-09-04T18:0x+07:00 ตามผล `notes_to_chief/20260904_1714_RE-240-RESULT-HOTBAR-DISPATCH-EXITS-NO-PRODUCER.md`: HOTKEY class 20 (ทุกแถว TOOLBAR*/SKILLBAR*) ออกที่ epilogue `0x4518F3` ก่อนถึงทั้ง `ActionVital`/`0x44D260` และ `TriggerCastSkillVital`/`0x00600A60` — ไม่มี producer ให้ตั้งชื่อ skill-id field จากเส้นนี้ · control WIELD ผ่าน (เส้นทาง RE ใช้ได้ ปัญหาอยู่ที่ branch สกิลเอง) · `BUILD_IMPACT: no server field named` (`damage_by_skill.py` ยังไม่ผูก skill id กับฟิลด์ใด) · ส่งต่อเป็นใบ attended capture ใบถัดไป (เปิดพร้อมกันในรอบนี้)**]

> 🔢 เลขใบตั้งโดย chief รอบ `wjqykr`/R338 2026-09-04T14:0x+07:00 · ตัวนับร่วมสองคิวคืน `239` ⇒ ใบนี้ `240` · **0 hit ทั้งสามที่ก่อนวาง**
> ที่มา: `notes_to_chief/20260904_1041_LANE-CS-CORE-REQUEST-which-actionvital-field-carries-skill-id.md` — คำตอบของ chief คือ "ไม่ใช่ห้าฟิลด์นั้น และน่าจะเป็นคนละเฟรม" ใบนี้คือทางที่ตัดสินได้จริง

## 🆕🔴 RE-136 MOBS-ANSWER-AS-NPC-DISPATCH-001 [STATIC-ON-CLOUD]: คลิกซ้ายบน hostile roster placement ถูกเซิร์ฟเวอร์ตอบด้วย **เลนคุย NPC** แทนเลนต่อสู้ -- จุดไหนในโค้ดตัดสิน และมันแยก mob ออกจาก NPC ด้วยอะไร (ถ้าแยก)  [**ANSWERED (ชั้นซอร์ส) โดย chief รอบ `wi1m62` 2026-08-29T01:2x+07:00 -- ไม่ต้องส่งให้ RE runner แล้ว · เหลือ "งานแก้" ซึ่งอยู่ในไฟล์ของ chief** -- คำตอบสี่ข้อและใบสั่งงานอยู่ท้ายใบนี้]

**ADDRESSEE: RE (ตอบได้จากซอร์สที่ commit แล้ว ไม่ต้องมีอิมเมจ)** · ผู้เปิดใบ: chief (สาย E) รอบ `wi1m62` (R218) 2026-08-29T01:0x+07:00
**ต้นเรื่อง:** `notes_to_chief/20260829_0018_KA3A-GT122-PASS-GT102-PARTIAL-GT104-BLOCKED-mobs-answer-as-npc.md` ข้อ ③ และ ④.1

🔴 **ใบนี้บล็อกทุกใบคอมแบต** -- `GT-104`, `GT-129`, `GT-084-R2` ตัดสินอะไรไม่ได้เลยจนกว่าจะปลด

**สิ่งที่วัดแล้ว [MEASURED, attended, flagless commit `3baf65de`, 2026-08-29T00:1x+07:00]:**
- คลิกซ้ายบน **P33 Fighting Fish soldier** และ **P58 Jungle Big Tiger** (พิกัดตรงตาราง `HOSTILE_PLACEMENTS` ทั้งคู่)
  ⇒ คอนโซลออก `V98_NPC_FACE_PLAYER_POSITION_HEADING_P<n>` แล้วตามด้วย `V98_NPC_CONVERSATION_DEFAULT_P<n>`
- จอเปิด **หน้าต่างบทสนทนาเปล่า** (หัวเป็นชื่อมอน เนื้อว่าง)
- **ไม่มีเฟรม attack/damage/death ในล็อกทั้งไฟล์** ⇒ ไม่ใช่ "ตีแล้วไม่ตาย" แต่คือ "ไม่มีทางเข้าโหมดตี"
- ฝั่งส่งไม่ใช่ครึ่งที่พัง: `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13 missing=none` ในบูตเดียวกัน

**คำถามที่ใบนี้ต้องตอบ (สี่ข้อ ตอบแยกข้อ)**
1. จุดใดใน `src/pirateforce_foundation/` ที่ปล่อย `V98_NPC_FACE_PLAYER_POSITION_HEADING` และ
   `V98_NPC_CONVERSATION_DEFAULT` -- ยกเงื่อนไขของกิ่งนั้นมาเป็น file:line
2. เฟรมขาเข้าระบุ "ตัวที่ถูกคลิก" ด้วยอะไร (vital id? index? พิกัด?) และโค้ดแยก NPC ออกจาก
   hostile placement ด้วยอะไร -- **ถ้าไม่แยกเลย ให้ตอบว่าไม่แยก** พร้อมบรรทัดที่พิสูจน์
3. วันนี้บนเส้นทางไร้แฟล็ก **มีเลนโจมตีที่คลิกนั้นไปถึงได้ไหม** ถ้ามี ต้องเกิดอะไรจึงจะถึง
   (แฟล็ก? vital id คนละตัว? เฟรมที่สองจากดับเบิลคลิก?)
4. จุดแก้อยู่ในไฟล์ของ chief (`runtime.py`/`app.py`) หรือในโมดูลของสาย B -- ข้อนี้ตัดสินว่าใครทำงาน

**เกณฑ์ผ่านสองชั้น**
- wire/DB: ตอบครบสี่ข้อ ทุกคำตอบมี file:line ที่ commit แล้ว · ข้ออนุมานติดป้าย [เสนอ] แยกจาก [วัดแล้ว]
- client-observable: **ยังไม่ใช่ใบนี้** -- การพิสูจน์ว่าคลิกแล้วเข้าโหมดตีได้จริงเป็น `GT-104` ที่รอปลดอยู่

**nonclaim ที่ต้องติดไปกับทุกคำตอบ:** วัดจาก 2 ใน 12 identity เท่านั้น (P33, P58) ห้าม generalize
ว่า "ทุก hostile ตอบเป็น NPC" จนกว่าจะเห็นโค้ดที่บังคับข้อนั้น หรือเห็นตัวที่สาม

---

### ✅ คำตอบ (chief รอบ `wi1m62` · `pf-static-re` บนโคลนคลาวด์ · ทุกบรรทัดมีที่มา ไม่มีการอ่านอิมเมจ)

**1. จุดที่ปล่อยสองเลเบล [วัดแล้ว]** = `current/pf_login_game_server_v141.py:4395-4478` (ไฟล์แช่แข็ง)
ไปถึงจาก `src/pirateforce_foundation/runtime.py:5779` (`actions = super().dispatch(parsed)`)
เลเบลเป็น f-string ⇒ **grep หาสตริงตรง ๆ ใน `src/` ได้ 0 hit ตลอดกาล นี่คือเหตุผลที่ไม่มีใครเจอมาก่อน**
เงื่อนไขกิ่ง: `nested_id in (TARGET_VITAL, CHOOSE_NPC) and self.population_indices is not None
and not self.v138_marker1_population_sent` (`TARGET_VITAL=0x1ADD`, `CHOOSE_NPC=0x0FB6`, `v141:396,401`)

**2. ตัวระบุเป้า และตัวแยก mob/NPC [วัดแล้ว]** ตัวตน = u64 ใน record `ChooseNPC` (tag `0x32`)
แปลงเป็น index ด้วย `idx = actor_identity - 0x2000 - 1` (`v141:4409`) แล้วเช็คว่าอยู่ใน
`self.population_indices` ซึ่งบนบูตไร้แฟล็กคือ **สำมะโนทั้งฉาก** (`runtime.py:6123`)
🔴 **ตัวแยก mob/NPC: ไม่มีเลย** มีแต่ยกเว้นแบบฮาร์ดโค้ดสามตัว (`V112_MONSTER_INDEX=30`,
`V112_SHOP_TRIGGER_INDEX=91`, `V129_QUEST_ACTOR_INDEX=0` ที่ `v141:4411-4415`)
และ **ช่องตัวตนของสองระบบเป็นช่องเดียวกัน** (`field_mobs.py:299-300` ใช้สูตร `0x2000+idx+1` เดียวกับ `v141:4409`)
⇒ เช็คทำได้ง่ายมาก แต่ไม่มีใครเช็ค · **P30 คือข้อยกเว้นโดยบังเอิญ และนั่นคือเหตุผลที่ `GT-084-R2` ตีได้**

**3. เลนโจมตีเข้าถึงได้ไหมวันนี้ -- ได้ ด้วยเฟรมคนละรูป [วัดแล้ว + พิสูจน์แล้วบนจอ]**
`runtime.py:3806-3990` `_dispatch_mob_combat` เรียกที่ `runtime.py:6228-6231` เมื่อ
`nested_id == ACTION_VITAL` (`0x1AEA`) เท่านั้น -- ไม่มีแฟล็ก ไม่ใช่ probe lane
เฟรม `TargetVital`/`ChooseNPC` ไปถึงไม่ได้เลยเพราะคนละ `nested_id`
**ตัวที่ยิง `ActionVital` คือดับเบิลคลิก** และเคยพิสูจน์บนจอแล้วบนบูตไร้แฟล็กบิลด์นี้:
`notes_to_chief/20260827_1620_GT084R2-RESULT-*` ("ดับเบิลคลิก = วิ่งเข้าไปตีหนึ่งครั้งต่อหนึ่งดับเบิลคลิก
เลขดาเมจขึ้น 5 ActionVital = 5 ครั้ง") · faction คู่ (ผู้เล่น 1 / มอน 6) ครบอยู่แล้วบนบูตไร้แฟล็ก
⇒ 🔴 **"คอมแบตตายทั้งเลน" เป็นข้อสรุปที่ผิด** สิ่งที่เกิดจริงคือ **คลิกเดียวเปิดหน้าต่างทับเป้า
ก่อนที่ผู้เล่นจะได้ดับเบิลคลิก** ตรงกับที่ผู้เทสจดไว้เองท้ายใบผล

**4. จุดแก้อยู่ในไฟล์ของใคร [วัดแล้ว]** = **chief** · ต้นทางอยู่ใน `v141` ซึ่งแก้ไม่ได้ (`AGENTS.md:41,130`)
⇒ ต้องแก้ที่ `runtime.py`: กันเฟรมก่อน `super().dispatch(parsed)` หรือกรอง action `V98_*` ที่คืนมา
สำหรับ identity ที่อยู่ใน roster · **สาย B ไม่ต้องแก้อะไรเลย** predicate ที่ต้องใช้มีให้แล้ว
(`field_mobs.hostile_placement_indices()` `field_mobs.py:595-597` · `overlapping_identities()` `:600`)

### 🔧 งานที่ตามมา (chief) -- ยังไม่ทำในรอบ `wi1m62` เพราะวินัยหนึ่งเรื่องหนึ่ง PR
[เสนอ ยังไม่วัด] ใน `runtime.py` เท่านั้น: ระงับคู่ `V98_NPC_FACE_*`/`V98_NPC_CONVERSATION_DEFAULT_*`
เมื่อ `idx` อยู่ใน `field_mobs.hostile_placement_indices()` -- คือการ**ขยายข้อยกเว้นที่ `v141:4411`
ให้ P30 อยู่แล้ว** ให้มาจาก roster แทนค่าคงที่ · ปลดสิ่งกีดขวางหนึ่งชิ้น **ไม่ใช่การรับประกันว่าจะตีได้**
(การตียังขึ้นกับ client ยิง `ActionVital` ซึ่งพิสูจน์แล้วว่ายิงเมื่อดับเบิลคลิก)

### 🔴 คำเตือนสำหรับใครก็ตามที่จะไปทำซ้ำ -- ชื่อตารางในใบนี้ stale บน HEAD
ใบผลและสถานะ `GT-104` เขียนว่าพิกัด P33/P58 ตรงตาราง `HOSTILE_PLACEMENTS`
**จริงที่ commit บูต `3baf65de` แต่ไม่จริงบน HEAD แล้ว**: `field_mob_tables.py:93-94`
`HOSTILE_PLACEMENTS = []` (ว่างสำหรับ bg0001) แถวย้ายไป `LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION`
(`:118-128`) แล้วรวมเข้า `SHIPPED_PLACEMENTS` (`:151-154`) ซึ่ง `field_mobs._parse_hostile_placements`
(`field_mobs.py:526-528`) เลือกใช้ · grep `HOSTILE_PLACEMENTS` บน main จะได้ศูนย์แถวและสรุปผิดว่า roster ว่าง

### nonclaim ของคำตอบชุดนี้
- ไม่ได้อ่าน `GameClient.local.bin` แม้ไบต์เดียว · คำถามว่า **ทำไม client ยิง `ChooseNPC` ใส่ actor faction 6**
  ตอบไม่ได้จากที่นี่ ต้องใช้เครื่องสะพาน
- ไม่อ้างว่าคลิกซ้ายบน hostile "ควร" ยิง `ActionVital` · หลักฐาน negative ของ SCENE-005 วัดด้วย **Tab** ไม่ใช่เมาส์
- ไม่อ้างว่าการถอด V98 ออกจะทำให้ตีได้ -- มันถอดสิ่งกีดขวางหนึ่งชิ้นเท่านั้น

## 🔬 RE-164 BT-GM-CLICK-FOUR-SUSPECTS-002 [CLOSED เฉพาะ**ชั้น static** ครบสี่ข้อ (#2 มีชั้น attended ด้วย) — ~~#1 STATIC-PARTIAL~~ ปิดโดย `RE-164 RESULT` `20260902_1143` รอบ `qhowwu` · 🔴 **ชั้น client-observable ของข้อ 3 ยังไม่ปิด และใบนี้ไม่เคยปิดมัน** — ถูกถือโดยขั้นที่ตัดสินของ `GT-207` (คลิกแล้ว `GMUI_BASIC` เปิดไหม) ซึ่งแทนที่ "`GT-164` variant ใหม่" ที่ nonclaim 7 พูดถึงและจะไม่มีวันมี]: **ของสี่ผู้ต้องสงสัยที่ `RE-126` ทิ้งไว้โดยไม่เดา (connection context / query-0x25 gate ตอนคลิก / current-UI object-key จริง / create path `0x007280D0`) ตัวไหนคือประตูที่หยุด `GMUI_BASIC` จริง — ข้อ 2 กับ 4 ปิดแล้วด้วย static synthesis จากใบเก่า (`RE-104`+`RE-118`) ที่ไม่เคย cross-reference กันมาก่อน ข้อ 2 ได้ชั้น attended เพิ่มจาก `GT-164` (bounded negative: 14/14 variant คลิกแล้วไม่เปิด)**

> 🆕 **อัปเดตรอบ `ku3jz6` 2026-09-01T21:xx+07:00 (LANE-GM):** ข้อ 3 **ปิดแล้วด้วย static** จาก
> committed artifact ที่เพิ่ง sync เข้า repo รอบ `a0909b1` (19:54+07, หลังรอบก่อนหน้าที่ตรวจ 06:26
> ยังไม่เจอไฟล์นี้จริง) — ดูบล็อกใหม่ในข้อ 3 ด้านล่าง ข้อ 1 ได้ write-site แล้วแต่ยังไม่ปิดสนิท (ดูบล็อกใหม่
> ในข้อ 1) 🔴 **สิ่งที่สำคัญที่สุดของรอบนี้ไม่ใช่ static fact แต่เป็นบรรทัดปฏิบัติการที่ไม่ใช่หลักฐาน
> IMAGE/DATA**: source artifact เอง (`PF_GM_PLUGIN_GATE.md` บรรทัด "UNPINNED OPERATIONAL INVENTORY")
> ระบุว่า ณ ตอนสร้างไฟล์ **inventory ของเครื่องบริดจ์ไม่พบ `GameMaster.dll`** ข้าง client — ถ้าจริงและยังจริง
> อาการ "เห็นปุ่มแต่คลิกไม่เปิด" ที่ตามหากันมาตั้งแต่ RE-104 (27 ส.ค.) สอดคล้องเป๊ะกับเส้น fallback ที่พิสูจน์
> แล้วใน GM-IMG-001/002/003 (DLL/export หาไม่เจอ → fallback object 4 ไบต์ → slot+0x04 คืน NULL เสมอ →
> dispatcher หยุดก่อนถึง factory) **นี่เป็นข้อสังเกตเชิงปฏิบัติการ ไม่ใช่ข้อเท็จจริง IMAGE/DATA** ต้องมีคนตรวจ
> จริงว่าไฟล์นั้นควรอยู่ตรงไหนของ client install และหายไปจริงหรือไม่ (ดูจดหมายที่เปิดคู่กับรอบนี้)

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนเขียนลงไฟล์นี้ 2026-08-31T03:2x+07:00: `RE-164`/`GT-164` = 0 hit ทั้งสอง
> ไฟล์นี้และ `GAME_TEST_QUEUE.md` ก่อนใบนี้ — เลขที่ใช้แล้วสูงสุดคือ `RE-163`/`GT-163`(reserved)
> 🔴 ใบนี้แก้เลขคู่จากที่รอบก่อน (`gm17278`) เขียนไว้ใน `pirate-force-server` PR #350 และ
> `docs/GM_LANE.md` ว่าคู่กับ `GT-165` — **นั่นผิด กติกาโปรเจกต์คือ RE-N คู่กับ GT-N เลขเดียวกันเสมอ**
> (ดู `RE-161`/`GT-161`, `RE-162`/`GT-162`, `RE-163`/`GT-163` ด้านบน) เลขที่ถูกคือ `GT-164` ไม่ใช่ `GT-165`
> — แก้ไว้ก่อนที่ตัวเลขผิดจะกระจายไปที่อื่น ดู nonclaim 4 ด้านล่าง
>
> 🆕 **ป้ายเส้นทางแก้แล้ว รอบ `jd4jqp` (`PROCESS_GATES.md` §18, กฎที่ chief เพิ่งเขียนกลับรอบ `jjs9bi`/R276
> ตามใบ `20260831_2325_KA1A-ROOTCAUSE-RE-runner-idle-30h-*.md`):** ข้อ 1/3 เดิมติดป้าย
> `NEEDS-ATTENDED-CAPTURE` มาตั้งแต่เปิดใบ (ก่อนป้ายเส้นทางสามแบบจะมีอยู่ด้วยซ้ำ) — **ป้ายนั้นผิดประเภทงาน**
> ข้อความของใบนี้เองบอกตรง ๆ ว่าทั้งสองข้อ "ต้องไล่ disassembly เพิ่มที่ไม่มีในอิมเมจของ clone นี้ ... ต้อง
> เปิดใบ RE runner บนสะพานถ้าจะไล่ต่อทาง static **หรือ**รอ attended capture" (nonclaim 5 เดิม) — คืองาน
> อ่านไบนารีต่อบนเครื่องสะพาน (มี image + disassembler) ไม่ใช่งานที่ต้องมีคนนั่งหน้าจอเกม แก้เป็น
> `STATIC-ON-BRIDGE` เพื่อให้ RE runner ที่ว่างอยู่ (ตามใบ ROOTCAUSE เดียวกัน) กรองใบนี้เจอ — สาย GM เป็น
> ผู้เปิดใบนี้เอง จึงแก้ป้ายของใบตัวเองได้ตามกฎ mailbox (chief เองเลือกไม่แปะป้ายแทนใบของสายอื่น)
> **ไม่เปลี่ยนเนื้อหา/ผล/nonclaim อื่นใดของใบนี้แม้แต่บรรทัดเดียว — แก้เฉพาะป้ายเส้นทางในหัวใบเท่านั้น**

### ที่มา — ใบนี้ควรถูกเปิดตั้งแต่รอบ `gm17278` แต่ไม่ได้ถูก push จริง

รอบ `gm17278` (2026-08-30T19:14 UTC / ~02:25+07:00 31 ส.ค.) สร้าง
`src/pirateforce_foundation/gm/bt_gm_probe.py` + `tests/test_gm_bt_gm_probe.py` บน `pirate-force-server`
จริง (PR #350, `merged=true`, ยืนยันด้วย GitHub API) และ `docs/GM_LANE.md` ของรอบนั้นบันทึกไว้ว่า "เปิด
`RE-164`" กับ "เปิด `CORE-REQUEST-GM-043`" — แต่ `pirate-force-server#350` เองเขียนไว้ในตัวว่า "Companion to
`pf_bridge#RE-164`/`GT-165`/`CORE-REQUEST-GM-043`" คือ**อีก PR หนึ่งฝั่ง `pf_bridge`** ซึ่งไม่เคยถูกเปิดเลย —
grep `pf_bridge` PR ทั้งหมดที่หัวข้อมี `gm17278` = 0 ผลลัพธ์ ยืนยันด้วย GitHub API ไม่ใช่จากรายงาน (ตามกฎ
ADDENDUM v2 ข้อ A ที่ห้ามเชื่อ `rounds/`/`docs/` ว่า "เสร็จ" ถ้า PR ไม่ merge) รอบนี้ (`b3fgm6`) จึงเขียนสามใบที่
ค้างอยู่จริง: ใบนี้ (`RE-164`), `GT-164` (`GAME_TEST_QUEUE.md`), และ `CORE-REQUEST-GM-043`
(`notes_to_chief/`)

### objective

ตอบจาก artifact ที่ commit แล้วก่อน (ห้ามเดาแล้วให้ผู้เทสยิงใส่ client จริงโดยไม่มี provenance):

1. **connection context** — เดินจาก click handler `0x0053B9B0` (RE-126 ยืนยันแล้วว่าเป็นตัวจริง) หา
   ที่มาของ connection/session context ที่มันอ่าน — context นั้นตรงกับ session ที่ state vital ถูกส่งไปหรือ
   อาจไม่ตรงกันได้ (เช่น หลาย login รวดกัน)
   🟡 **[STATIC-PARTIAL รอบ `1q7nxu`]** ทราบแค่ *ตำแหน่ง* เช็ค: handler เช็ค global `[0x01032EC4]` ไม่เป็น
   null เป็นสเต็ป 2 ของกิ่ง `0x0053BC51..0x0053BC96`
   (`notes_to_chief/20260828_0411_RE-118-RESULT-CURRENT-UI-KEY-MUST-BE-NONEMPTY.md:26-28`) — แต่ยังไม่รู้ว่า
   context ตัวนั้น *ตรง* กับ session ที่ state vital ถูกส่งไปหรือไม่ ต้องไล่ write-site ของ `0x01032EC4`
   เพิ่ม ไม่มีในเอกสารที่ commit แล้ว — RE-126 nonclaim 3 ระบุเองว่าไม่เคยอ้างเรื่อง match/mismatch นี้
   (`notes_to_chief/20260828_1809_RE-126-RESULT-BT-GM-SAME-CONTROL.md:53`) **[STATIC-ON-BRIDGE ยืนยัน — แก้ป้ายรอบ jd4jqp]**
   🟡 **[STATIC-PARTIAL เพิ่ม รอบ `ku3jz6`]** เจอ write-site แล้ว: `notes_to_chief/reference_codex_attr/
   pf_rederive_attr_semantics.py:25900-25902` pin `assert_bytes("CMyActor_singleton_store", 0x0044CB7D,
   b"\x89\x35\xC4\x2E\x03\x01")` = `mov [0x01032EC4], esi` อยู่ท้าย `CMyActor` constructor ทันทีหลัง
   `constructor_vtable_store` (`0x0044C990..0x0044C9CB`) — ยืนยันซ้ำอิสระใน `PF_ATTR_FIELD_SEMANTICS.tsv`
   (แถว `singleton_store=0x0044CB7D..0x0044CB83`) และ `PF_COMBAT_LETHAL_TAIL_DELTA.tsv:13` ("CMyActor
   singleton at 0x01032EC4 is nonnull") **สรุปเชิงความหมาย: `[0x01032EC4]` คือ singleton ของ `CMyActor`
   (ตัวละครผู้เล่นโลคัลของ client เอง) ไม่ใช่ object ที่ผูกกับ "session"/"connection" ของเซิร์ฟเวอร์โดยตรง** —
   นี่ตอบคำถามเดิมบางส่วน (ตัวแปรนี้เป็น "มี local player actor สร้างแล้วหรือยัง" ไม่ใช่ตัวติดตาม
   หลาย-connection) แต่ **ยังไม่ปิดสนิท**: ไม่พบ write-site ตัวที่สอง (clear/dtor ตอน logout/relog) ในทั้ง
   สอง repo แม้ค้นตรง VA แล้ว จึงยังตอบไม่ได้ว่า global ตัวนี้ค่าเก่าอาจค้างข้ามรอบ relog หรือไม่ — ต้องไล่
   caller-graph ของ `constructor_vtable_store`/`0x0044C990` ต่อ ยังเป็น **STATIC-ON-BRIDGE จริง** สำหรับ
   ส่วนนี้ ไม่ได้ปิดทั้งข้อ (รายละเอียดเต็ม: `notes_to_chief/20260901_2132_RE-164-RESULT-item3-closed-item1-writesite-found-plus-gamemasterdll-flag.md`)
   ✅ **[STATIC ปิดแล้ว รอบ `qhowwu` — บริโภคโดย LANE-GM ผู้เปิดใบ]** `notes_to_chief/
   20260902_1143_RE-164-RESULT-local-actor-singleton-clear-sites.md` ปิด write-site ตัวที่สองที่รอบ `ku3jz6`
   หาไม่เจอ: direct-reference census ของ DWORD `0x01032EC4` ใน `.text` = **2,016 จุด ตรงกับ
   relocation target ครบ** ถอดตามขอบเขตคำสั่งแล้วเป็น read/test 2,013 จุด และ **direct write สามจุด**:
   publish `0x0044CB7D` (ctor) · conditional clear `0x0044C4E2..0x0044C4EF` (dtor — `cmp` ก่อน จึง
   **ไม่ล้างทับ object ใหม่**) · unconditional clear `0x004B4B33` ก่อน path ที่ผูก actor ตัวใหม่
   ⇒ คำถามเดิมของข้อ 1 ตอบได้แล้ว: `[0x01032EC4]` **ไม่ใช่ตัวระบุ connection/session** และ
   lifecycle ปกติมีการล้างก่อนเปลี่ยน actor ⇒ สมมติฐาน "click handler อ่าน context ของคนละ
   connection เพราะ login เร็ว ๆ กัน" **ถูกถอน** · evidence spans มี SHA-256 ครบสามช่วงในใบผล
   🔴 **เพดานของการปิด อ่านก่อนเอาไปอ้าง:** ปิดเฉพาะ **lifecycle ปกติที่เดินผ่านสามจุดนี้**
   (nonclaim 2 ของใบผล: crash / forced termination / corruption ไม่ถูกอ้าง) · และ census นี้เป็น
   **หลักฐานเชิงบวกจาก clear-site ไม่ใช่ผลลบจาก linear disassembler** (nonclaim 3) — indirect alias /
   bulk overwrite ที่ไม่ฝัง absolute address ยังไม่ถูกตัด
   🔴 **สิ่งที่ใบนี้ไม่เคยปิดและการปิดหัวใบนี้ไม่ได้ทำให้หายไป:** คำถาม "มี `GameMaster.dll` อยู่ข้าง exe
   ก่อนติดตั้งของเราไหม" (`NOW.md` P-3) เป็นคำถาม **เชิงปฏิบัติการจากเครื่องจริง ไม่ใช่งาน static RE**
   (nonclaim 4 ของใบผลปฏิเสธเองว่าไม่ตอบเรื่องนี้) — มันถูกถือโดย **ใบ `GT-207` หัวข้อ "ของแถม"**
   ("ของแถม (`RE-164` · NOW.md P-3): มี `GameMaster.dll` อยู่ข้าง exe **ก่อน** ติดตั้งของเราไหม")
   ⇒ การปิดหัวใบนี้ **ไม่ทำให้ P-3 ขยับ** และ **ไม่ทำให้คำถามนั้นหาย** — มันย้ายไปอยู่ที่เดียว
   ที่ตอบมันได้ คือคนที่นั่งอยู่หน้าเครื่องจริง
   🔴 **ชั้น client-observable ไปอยู่ที่ไหน (อย่าอ่านหัวใบแล้วคิดว่ามันหายไป):** คำตอบของข้อ 3 ในใบนี้
   เขียนเองว่าชั้น client-observable ยังไม่ปิดและต้องมี `GT-164` variant ใหม่ยืนยัน · **ไม่มี variant นั้น
   และจะไม่มี** — สิ่งที่แทนมันคือขั้นที่ตัดสินของ **`GT-207`** (คลิก `BT_GM` แล้ว `GMUI_1` เปิดถึง tab
   `GMUI_BASIC` หรือไม่) ซึ่ง `[READY]` รอเครื่องจริงอยู่แล้ว ⇒ การปิดหัวใบนี้ปิด **ชั้น static** เท่านั้น
   ไม่ใช่การปิดคำถามของ P-3
   🔴 **อ้าง `GT-207` ด้วยเลขใบ ไม่ใช่เลขบรรทัด** — `GT-207` ขยับ `10552`->`10614` ภายในวันเดียว และ
   `NOW.md:31` ที่ pin `:10552` ค้างไปแล้ว · สายนี้แก้ `GAME_TEST_QUEUE.md` ไม่ได้ จึงไม่ทิ้ง pin ที่ซ่อมเองไม่ได้
   ⚖️ **ข้อขัดแย้งที่สายนี้ยกขึ้นเอง (เหมือนรอบ `wggs0i`):** `ADDENDUM v2 ข้อ B` ให้สิทธิ์สายที่เปิดใบ
   ปิดหัวใบของตัวเอง แต่ `PROCESS_GATES.md` §19 (บรรทัด 146) เขียนว่าใบที่กระทบทะเบียนกลางให้ **chief**
   ปิด · ใบผลขอให้ "LANE-GM/chief" ปิด สายนี้จึงปิดตามคำขอนั้น — **ถ้า chief อ่านตาม §19 แล้วจะย้อนหัวใบ
   กลับไปแล้วปิดเอง สายนี้ไม่โต้**
2. **query-0x25 gate ตอนคลิก** — adapter `0x00726D30` (อ่าน `GMModule_Client+0x19`, RE-104 พิสูจน์ว่าคุมการ
   วาด/enable ปุ่ม) ถูกเรียกซ้ำตอนคลิกด้วยหรือคืนค่าจากตอนวาดครั้งเดียว — ถ้าเรียกซ้ำ ค่าที่อ่าน ณ
   เวลาคลิกอาจต่างจากตอนวาด
   ✅ **[STATIC ปิดแล้ว รอบ `1q7nxu`]** เรียกซ้ำ ไม่ใช่ค่าจากตอนวาด — click handler เรียก `0x0044A3B0`
   ตรวจ `module+0x19` ใหม่ที่กิ่ง `0x0053BC51..0x0053BC96` เป็นการเรียกแยกจากเช็ควาด/enable เป็นระยะที่
   `[0x0053B150,0x0053B324)` (สองที่คนละจุด) — สองใบยืนยันตรงกัน:
   `archive/notes_to_chief_2026-08/consumed/20260827_1518_RE-104-RESULT-BT-GM-MODULE-PLUS19-GATE.md:41` และ
   `notes_to_chief/20260828_0411_RE-118-RESULT-CURRENT-UI-KEY-MUST-BE-NONEMPTY.md:27-31` (ทั้งสองมีมาก่อน
   `RE-164` เปิด แค่ไม่เคย cross-reference กัน — เป็นช่องว่างของการสังเคราะห์ ไม่ใช่หลักฐานใหม่)
   🟢 **[ATTENDED เพิ่ม รอบ `szmgeh`, `GT-164`]** กะ1-A คลิก `BT_GM` จริงหลังยิงทั้ง 14 variant — **ไม่มี
   variant ไหนเปิด `GMUI_BASIC`** แม้ปุ่มมองเห็นได้และ query-gate ถูกเรียกซ้ำตามที่พิสูจน์ไว้ (ด้านบน) ⇒
   ข้อ 2 (ตัวเฟรมนี้เอง) **ถูกตัดออกจากการเป็นประตูที่หยุดหน้าต่าง** ทั้งชั้น static และ attended ตรงกัน —
   ผลข้างเคียง: พบว่า `field_0x0b_second` (ไม่ใช่ field ที่ query-0x25 อ่าน) คือสวิตช์การ**มองเห็น**ปุ่ม
   แยกจากการคลิก ยืนยันมิติใหม่ของฟิลด์ที่รู้จักอยู่แล้วจาก `RE-089`/`RE-104`/`CORE-REQUEST-020` (เดิมรู้แค่
   ตอน login ครั้งเดียว รอบนี้ยืนยันว่าใช้ได้กลางเซสชันด้วย ไม่ต้อง relog) — รายละเอียดเต็มดู
   `notes_to_chief/20260831_0901_GT164-RESULT-bounded-negative-on-suspect-2-plus-field-0x0b-second-is-the-button-visibility-switch.md`
   และ `gm/bt_gm_probe.py`'s `observed_button_visible`/`guaranteed_visible_variant_ids` (รอบนี้เพิ่ม)
3. **current-UI object-key จริง** — `RE-118` เดาว่าต้องไม่ว่าง `GT-103` A/B หักล้างข้อเสนอนั้นแล้ว (4 สถานะ
   UI เงียบหมด) เงื่อนไขจริงคืออะไร ไล่ vfunc `[0x01093198]+0x7C8+0x04` ต่อจากจุดที่ `RE-118` หยุด
   🟡 **[STATIC-PARTIAL รอบ `1q7nxu`]** `RE-118` ไล่ถึง predicate ที่ `[0x008946C0,0x008946EA)` (ตรวจ
   UTF-16 ไม่ว่าง) แต่หยุดที่ "ไม่มี literal/crosswalk ผูก key กับชื่อ panel"
   (`notes_to_chief/20260828_0411_...md:38,62`) — `GT-103AB`
   (`notes_to_chief/20260828_1140_GT103AB-RESULT-...md:51`) ยืนยันช่องว่างนี้ยังเปิดอยู่ ไม่มีใบไหนไล่ต่อจาก
   จุดนั้น **[STATIC-ON-BRIDGE ยืนยัน — แก้ป้ายรอบ jd4jqp]**
   🟢 **[STATIC ปิดแล้ว รอบ `ku3jz6`]** ตอบได้จาก committed artifact ที่เพิ่งมาถึง repo รอบ sync `a0909b1`
   (2026-09-01T19:54+07 — ยังไม่มีตอนรอบ `20260901_0626` ที่เคย "ค้นแล้ว: ไม่เจอ" สามไฟล์นี้ตรง ๆ):
   `notes_to_chief/reference_codex_attr/PF_GM_PLUGIN_GATE.tsv`/`.md` เดินสายเต็ม 17 IMAGE row + 2 DATA
   row ทุกแถว `PROVEN_EXACT`/`PROVEN_EXACT_CONDITIONAL` พร้อม evidence span + sha256:
   `GM-IMG-001` (loader `LoadLibraryW(L"GameMaster.dll")` → `GetProcAddress("CreateGameMaster")` →
   เรียก export → เก็บผลที่ `application+0x7C8`) → `GM-IMG-002/003` (ถ้า DLL/export/call ล้มเหลว จะสร้าง
   fallback object 4 ไบต์แทน ซึ่ง vtable slot `+0x04` คืน `NULL` เสมอ) → `GM-IMG-006/007` (คลิกเรียก
   slot `+0x04` ผ่าน dispatcher `0x00AA0710..0x00AA0799` ซึ่งเช็ค empty-predicate `0x008946C0..
   0x008946EA` — **จุดเดียวกับที่ RE-118 หยุดไว้พอดี** — ถ้า NULL/ว่าง จะ `ret` ก่อนถึง factory เสมอ) →
   `GM-IMG-008` (factory `0x007280D0` ต้อง exact-match UTF-16 กับ key จาก slot `+0x04` เท่านั้นจึงสร้าง
   panel) → `GM-IMG-009`/`GM-IMG-013` (`GMUI_BASIC` เป็นแค่ child/tab lookup **หลัง** panel ถูกสร้างแล้ว
   ไม่ใช่ค่าที่ slot `+0x04` ต้องคืน — ถอนสมมติฐานเดิมที่เคยเข้าใจผิดแบบนี้) ผสาน DATA: `GM-DATA-001/002`
   (`GMUI.project`/`GMUI_1.model`) ยืนยันว่า model ที่มี child `GMUI_BASIC` จริงชื่อ `GMUI_1` ไม่ใช่
   `GMUI_BASIC` เอง — **คำตอบข้อ 3 (ตัดสินสองชั้นแยกกัน):**
   - **ชั้น wire/DB/static — ปิด:** current-UI object-key คือค่าที่ slot `+0x04` ของ GM-plugin interface
     คืน (ไม่ใช่ literal ที่เคยเดา) เดินทางผ่าน dispatcher → factory (exact-match) → GUI-model resolver
     ที่ประกอบ `.\Data\GUI\Model\<key>.model`; ค่าที่ "ควรจะ" ทำให้ panel เปิดได้ตาม DATA ที่มีคือ `GMUI_1`
     (**[RECONSTRUCTED POLICY — PROPOSED]** ของ artifact เอง ไม่ใช่ค่าที่วัดได้จาก DLL เดิมโดยตรง)
   - **ชั้น client-observable — ยังไม่ปิด:** ไม่มีหลักฐานว่า panel เปิดจริงถ้าแก้ปัญหาด้านล่างแล้ว ต้อง
     `GT-164` variant ใหม่ยืนยัน (ดู "ห้ามทำจนกว่า" ในหมายเหตุ nonclaim 8 ด้านล่าง)
   🔴 **ข้อสังเกตเชิงปฏิบัติการที่สำคัญกว่า static fact เองทั้งหมด** — artifact ต้นทาง (`PF_GM_PLUGIN_GATE.md`,
   ส่วน "UNPINNED OPERATIONAL INVENTORY — NOT IMAGE/DATA EVIDENCE") บันทึกไว้ตรง ๆ ว่า ณ ตอนสร้างไฟล์
   inventory ของเครื่องบริดจ์ **ไม่พบ `GameMaster.dll`** ข้างไฟล์ client จริง — generator เองไม่ได้ enumerate/
   hash inventory นี้ (อาจ stale) แต่ถ้ายังจริง **นี่คือคำอธิบายที่สอดคล้องกับอาการทั้งหมดที่สังเกตมาตั้งแต่
   RE-104**: ปุ่มโชว์ได้ (field `0x0b_second` คุมแยกจากนี้) แต่คลิกแล้วไม่มีอะไรเกิดเพราะ interface ที่แท้จริง
   ไม่เคยโหลดเลย ไม่ใช่ปัญหาการผูกปุ่ม/handler/query-gate ที่ RE-104/RE-118/RE-126/RE-164#2/#4 ไล่ตรวจไปแล้ว
   ทั้งหมด (ทุกจุดนั้นถูกต้องอยู่แล้ว ปัญหาอยู่ *ก่อน* จุดเหล่านั้นทั้งหมด) — **ไม่ใช่ข้อเท็จจริง IMAGE/DATA
   ห้ามใช้ปิดใบเพียงอย่างเดียว** ต้องมีคนตรวจ client install จริงว่าไฟล์นี้ควรอยู่ที่ไหนและหายไปจริงหรือไม่
   (แจ้งผ่านจดหมาย `notes_to_chief/20260901_2132_RE-164-RESULT-item3-closed-item1-writesite-found-plus-gamemasterdll-flag.md`
   ให้ chief/COO/เจ้าของตัดสินว่าจะตรวจยังไง — `pf_bridge` แผนกนี้ไม่มี client image ไม่มีทางยืนยันเอง)
   หาก DLL หายไปจริงและกู้คืนไม่ได้ artifact เดียวกันนี้ยังทิ้ง **สเปกปลั๊กอินทดแทนที่เข้ากันได้** ไว้ครบ
   (ABI ของ slot `+0x00`/`+0x04`/`+0x08`, allocator ที่ต้องใช้ `MSVCR90 operator new` ไม่ใช่ UCRT/modern
   heap, ชื่อ export ต้องตรง `CreateGameMaster` ไม่มี decoration) — เป็นทางเลือกสำรองถ้าจะสร้างปลั๊กอินเอง
   แทนการกู้ไฟล์เดิม (nonclaim: นี่เป็นสเปกที่ derive จาก IMAGE ไม่ใช่ค่าที่วัดจาก DLL เดิมโดยตรง)
4. **create path** — factory `0x007280D0` ที่สร้าง `GMUI_BASIC`/`GMModule_Client+0x48` ถูกเรียกไหมเมื่อคลิก
   หรือมี early-return ตัดก่อนถึง
   ✅ **[STATIC ปิดแล้ว รอบ `1q7nxu`]** มี early-return แบบมีเงื่อนไข: dispatcher
   `[0x00AA0710,0x00AA0799)` เรียก empty-key predicate ก่อน ถ้า true จะ `ret 0x10` ทันทีไม่มี log/frame —
   create path (`0x00A9E080` ซึ่ง vtable-crosswalk ไปที่ factory `0x007280D0` ผ่าน `GMModule_Client+0x48`)
   ไม่ถูกเรียก (`notes_to_chief/20260828_0411_...md:36,42-44`; สรุปซ้ำใน
   `archive/rounds_2026-08-27_to_28/GM_20260828_0418_re118-closed-gt103-ab-procedure-added.md:35`)

### pass criteria — สองชั้น แยกกันเด็ดขาด

**ชั้น wire/DB (ปิดใบนี้ได้บางส่วน):** คำตอบต่อข้อ 1-4 จาก static analysis ของ artifact ที่ commit แล้ว
พร้อมเลขบรรทัด/VA — ผลลบก็เป็นคำตอบ (เช่น "ข้อ 2 คืนค่าเดิมเสมอ ไม่ถูกเรียกซ้ำตอนคลิก" ปิดข้อนั้นได้)
🆕 **สถานะรอบ `ku3jz6`:** ข้อ 2/3/4 ปิดชั้นนี้แล้ว ข้อ 1 ยัง STATIC-PARTIAL (write-site เจอ, clear-site ยังไม่เจอ)

**ชั้น client-observable (ใบนี้ตอบไม่ได้ ต้องมีคนหน้าจอ):** `GT-164` (`GAME_TEST_QUEUE.md`) — คลิก `BT_GM`
ทีละ variant ของ `gm/bt_gm_probe.py`'s `iter_state_vital_bit_variants()` แล้วดูว่า `GMUI_BASIC` เปิดไหม —
🟢 **เสร็จแล้วรอบ `szmgeh`** (`CORE-REQUEST-GM-043` ปลด BLOCKED รอบ `jz4don`, กะ1-A คลิกจริงรอบ `GT164-RESULT`
2026-08-31T08:50-08:55+07:00) — ผลคือ bounded negative ต่อข้อ 2 (ดูรายละเอียดในข้อ 2 ด้านบน)

### ข้อห้าม
ห้ามเดาความหมายของฟิลด์ `field_0x14` บิต 8-31 (ไม่ครอบคลุมโดย `bt_gm_probe.py` รอบก่อน ตั้งใจเว้นไว้) ·
ห้ามอ้างว่าประตูไหน "คือ" สาเหตุโดยไม่มี VA/บรรทัดอ้างอิง · ห้ามใช้ผลของใบนี้อ้างว่าทางแชท (`0xAC52`) เป็น
ทางเข้า `GMUI_BASIC` อีกทาง (RE-126 ปิดคำถามนั้นแล้วว่าไม่ใช่)

### สัญญาผู้บริโภค
ผู้เปิดใบเป็นผู้บริโภคผล (LANE-GM) ตามกฎ ADDENDUM v2 ข้อ B — เมื่อได้ผล (บวก ลบ หรือ bounded-negative)
สาย GM ปิดหัวใบนี้เองรอบที่บริโภค พร้อม consumed stub

### nonclaims
1. รอบ `1q7nxu` ไม่ได้ยิงเฟรมใด ๆ ใส่ client จริง — ข้อ 2 กับ 4 ปิดได้ด้วยการอ่านใบเก่าที่ commit แล้ว
   สองใบ (`RE-104`, `RE-118`) เฉย ๆ ไม่ใช่หลักฐานใหม่ ไม่ใช่การอ่าน disassembly เพิ่ม
2. ไม่ได้ตรวจว่า `bt_gm_probe.py`'s 14 variant ครอบคลุมพอจะตอบข้อ 2 (query-gate timing) ได้จริง — นั่นเป็น
   คำถามเรื่องเวลา ไม่ใช่ค่า ตัว frame variant ปัจจุบันตอบไม่ได้ ต้องมีกลไกจับเวลาเพิ่ม (ดู `bt_gm_probe.py`
   docstring ของ `QUERY_GATE_VALUE_AT_CLICK_TIME_SUSPECT`) — ไม่กระทบคำตอบข้อ 2 ที่ปิดแล้ว (เรื่องคนละชั้น:
   "เรียกซ้ำไหม" ปิดแล้วด้วย static, "ค่าอะไรตอนคลิกจริง" ยังต้องใช้เวลา/attended)
3. ไม่ได้ตัดสินว่า `GT-164` ควรปลด BLOCKED ด้วยทางไหน (GM chat-command ใหม่ หรือ debug scenario flag) —
   เป็นดุลยพินิจของ chief ตาม `CORE-REQUEST-GM-043`
4. เลข `GT-164` (แก้จาก `GT-165` ที่รอบก่อนเขียนผิดในเอกสารที่ไม่เคย push) คือเลขที่ยึดตามใบนี้ ถ้าเอกสาร
   ที่ไหนยังอ้าง `GT-165` สำหรับเรื่องนี้ ให้ถือว่าเอกสารนั้นล้าสมัย ไม่ใช่ไฟล์คิวสองไฟล์นี้
5. ~~ข้อ 1 กับ 3 ยังไม่ปิด — ข้อ 1 ต้องไล่ write-site ของ `[0x01032EC4]` เพิ่ม ข้อ 3 ต้องไล่ vfunc chain ต่อจาก
   `[0x008946C0,0x008946EA)` ทั้งคู่ไม่มีในอิมเมจของ clone นี้ (ไม่มี client image ไม่มี disassembler)
   ต้องเปิดใบ RE runner บนสะพานถ้าจะไล่ต่อทาง static หรือรอ attended capture~~
   **แก้รอบ `ku3jz6`:** ข้อ 3 ปิดแล้วด้วย static จาก `PF_GM_PLUGIN_GATE.tsv` ที่เพิ่ง sync เข้ามา (ไม่ต้อง
   ใช้ image/disassembler เพิ่ม — เดินสายจาก IMAGE row ที่มีอยู่แล้วในไฟล์นั้น) ข้อ 1 เจอ write-site แล้ว
   (`pf_rederive_attr_semantics.py:25900-25902`) แต่ clear-site/cardinality ยังไม่เจอ ยังเป็น
   STATIC-ON-BRIDGE จริงสำหรับส่วนที่เหลือของข้อ 1 เท่านั้น
6. `GT-164` ปิดแล้วเป็น bounded negative ต่อข้อ 2 เท่านั้น (รอบ `szmgeh`) — **ไม่ใช่หลักฐานว่า `RE-164` ปิด
   ครบ** ข้อ 1 ยังเปิดบางส่วน และการที่ปุ่ม "มองเห็นได้" ระหว่างเทส (`field_0x0b_second=1`) ก็ไม่ได้แปลว่าคลิกได้
   ผล — สองเรื่องคนละชั้นกัน (visibility vs. click-success) ตามที่ `gm/bt_gm_probe.py`'s
   `observed_button_visible` docstring ระบุไว้ชัดเจน
7. **[ใหม่ รอบ `ku3jz6`]** ข้อ 3 ที่ปิดแล้วเป็นชั้น IMAGE/DATA เท่านั้น — `GMUI_1` เป็น
   **[RECONSTRUCTED POLICY — PROPOSED]** ของ `PF_GM_PLUGIN_GATE.md` เอง ไม่ใช่ค่าที่วัดได้จาก DLL เดิม
   โดยตรง ไม่อ้างว่า panel จะเปิดจริงถ้าลองค่านี้ — ต้องมี `GT-164` variant ใหม่ยืนยันชั้น client-observable
8. **[ใหม่ รอบ `ku3jz6`]** ไม่อ้างว่า `GameMaster.dll` หายไปจริงจาก client install ปัจจุบัน — แหล่งข้อมูลเอง
   ระบุว่า inventory นั้นอาจ stale และไม่ใช่ IMAGE/DATA evidence เป็นเพียงข้อสังเกตเชิงปฏิบัติการที่ต้อง
   ตรวจซ้ำโดยคนที่มี client install จริง (LANE-GM ไม่มี client image ไม่มีทางยืนยันเอง)

### links
`pirate-force-server` PR #350 (merged, `bdbef5c`) · `src/pirateforce_foundation/gm/bt_gm_probe.py` ·
`tests/test_gm_bt_gm_probe.py` · `notes_to_chief/20260828_1809_RE-126-RESULT-BT-GM-SAME-CONTROL.md` ·
`notes_to_chief/20260828_1140_GT103AB-RESULT-...md` ·
`notes_to_chief/20260831_0152_PANYA-ORDER-LANE-GM-make-the-BT_GM-button-and-GMUI_BASIC-window-actually-work.md` ·
`archive/notes_to_chief_2026-08/consumed/20260827_1518_RE-104-RESULT-BT-GM-MODULE-PLUS19-GATE.md` ·
`notes_to_chief/20260828_0411_RE-118-RESULT-CURRENT-UI-KEY-MUST-BE-NONEMPTY.md` ·
`rounds/GM_20260831_0822_re164_partial_static_synthesis.md` ·
`notes_to_chief/20260831_0901_GT164-RESULT-bounded-negative-on-suspect-2-plus-field-0x0b-second-is-the-button-visibility-switch.md` ·
`notes_to_chief/reference_codex_attr/PF_GM_PLUGIN_GATE.tsv` (+`.md`, +`.pair.json`) ·
`notes_to_chief/reference_codex_attr/pf_rederive_attr_semantics.py:25900-25902,26108,26413` ·
`notes_to_chief/reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv` (แถว `singleton_store=0x0044CB7D..`) ·
`notes_to_chief/reference_codex_attr/PF_COMBAT_LETHAL_TAIL_DELTA.tsv:13` ·
`notes_to_chief/20260901_2132_RE-164-RESULT-item3-closed-item1-writesite-found-plus-gamemasterdll-flag.md`

## RE-125 PICKUP-REQUEST-VITAL-ID-001: what wire vital id (opcode) does a real client send when the player left-clicks a ground drop / `PickupTerrainThing` object, and what does its payload contain (object reference dword position, anything else)  [**CLOSED — 🔴 คำอ้างเชิงลบของใบนี้ถูกหักล้างแล้ว 2026-09-05**: `0x4543` **ถูกเห็นบนไวร์แล้ว** — R303 attended capture 20260902_1755 = 46 เฟรมขาเข้า 2 เทคจบ ยืนยันซ้ำ R306 · `COO-DECISION 20260905_0249` ข้อ 1 ปิด `GT-146` ด้วยเหตุผลนี้ และข้อ 2 สั่งพลิกถ้อยคำในซอร์ส ซึ่ง chief จ่ายรอบ `rz1fxh`/R358 (13 จุด 12 ไฟล์) · หัวใบนี้แก้ในรอบเดียวกันเพราะคำอ้างเก่ากับใหม่อยู่ด้วยกันไม่ได้ (chief `1810` §3) · ถ้อยคำเดิมที่ถอนแล้วแต่เก็บเป็นประวัติ: ~~**CLOSED BOUNDED-NEGATIVE — opcode ยัง UNOBSERVED: `0x4543` เป็นค่า DERIVED จากชื่อคลาสเท่านั้น, corpus ปัจจุบัน 2,106 ไฟล์ / 75,208 blocks มี `PickupTerrainThing` W=0/R=0 ⇒ ~~🔴 ห้ามต่อ production call site ของ `dispatch_pickup_request` ใน `runtime.py` ด้วย `0x4543` · ปลดล็อกได้ด้วย attended click capture ใหม่เท่านั้น (ใบแยก)~~ **LIFTED by COO-DECISION 20260902_0541** (ขีดฆ่า ไม่ลบ) — call site ต่อแล้วโดยคำตัดสิน `0541` ทาง 1 · ~~สิ่งที่ **ยังจริงไม่เปลี่ยน**: เลข `0x4543` ยัง **UNOBSERVED บนไวร์**~~ 🔴 **ถอนโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 — ข้อความนี้ถูกหักล้างแล้วตั้งแต่ 2026-09-02**: รอบ attended R303 (`notes_to_chief/20260902_1755_KA1A-R303-RESULTS-*` หัวข้อ "0x4543 IS NO LONGER DERIVED - please strike the caveat") วัดเฟรมขาเข้า `0x4543` **46 เฟรม** และสองเฟรมในนั้นทำให้เกิดแถวในกระเป๋าจริง · ยืนยันซ้ำ R306 (`20260903_1657` · `VITAL_WALK_PROMOTED vital=0x4543`) ⇒ `0x4543` เป็น **OBSERVED บนไวร์** แล้ว ไม่ใช่ค่า derive จากชื่อคลาสอย่างเดียวอีกต่อไป · จดหมาย R303 ถูก consume แล้วแต่ไม่มีใครลงมือถอน ค้าง 3 วัน (พบโดยลูกมือตรวจของ chief รอบนี้) · 🔴 **คอมเมนต์ในซอร์สเซิร์ฟเวอร์ยังไม่ถูกแก้และผมยังแก้ไม่ได้ในรอบนี้** — `runtime.py:7886` · `mob_pickup_request.py:23` · `mob_loot.py:935` · `loot_roll.py:37` · `app.py:282` · `runtime.py:2835` · `runtime.py:7945` ยังเขียนว่า never observed และถูก **พินด้วยเทสบนเกต** (`test_the_call_site_is_absent_or_is_the_published_one`) ตาม `COO-DECISION 20260902_0542` ข้อ 1 ⇒ เกตกำลังบังคับข้ออ้างที่การวัดหักล้างแล้ว · **แก้ต้องผ่าน COO** เพราะถ้อยคำนั้นถูกคำตัดสินตรึงไว้ = จดหมาย `20260905_02xx_CHIEF-ASK-COO-*` และเงื่อนไขของ `0541` คือข้อเท็จจริงนี้ต้องเขียนไว้ที่ call site (เทส `test_the_call_site_is_absent_or_is_the_published_one` บังคับบน gate) · ต่อเป็น persist path (`dispatch_inbound_pickup_request`) ไม่ใช่ dispatch ล้วน ตาม `0541` ข้อ 2 · payload shape ปิดแบบ conditional-static แล้ว: class body = `object_ref_u32` + `opaque_u8` ไม่มี claimant identity/XYZ ⇒ เซิร์ฟเวอร์ต้องอ่านตัวตน/ตำแหน่งจาก authenticated session state · ปิดโดย RE runner LOCAL 2026-08-28T11:12+07:00, บริโภคโดย LANE-B รอบ `rbuta4` 2026-08-28T17:49+07:00, ดู `notes_to_chief/20260828_1112_RE-125-RESULT-NO-CAPTURED-PICKUP-OPCODE.md`**~~]

> NUMBERING NOTE: shared counter with `GAME_TEST_QUEUE.md` -- this round also opened `GT-124` there (grep
> confirmed 2026-08-28: `GT-124`/`RE-124`/`RE-125` = 0 hits before either was reserved). `GT-124` took `124`
> first (opened earlier in the same round); this entry is `125`. Highest prior number was `RE-123`
> (BG0002-MIRAGE-REEL-QUEST-SPAWN-CROSSWALK-001, CLOSED).

**ค้นใน `pf_bridge\external\ แล้ว:** ไม่เจอ -- `grep -in "pickup|Terrain.*Thing|4543|ground.*loot|item.*operate"
external/00_SEARCH_HERE_FIRST.md` ให้ผล 0 แถว (ตรวจตามกฎบังคับข้อแรกของไฟล์นี้ก่อนเปิดใบ)

### ทำไมเปิดใบนี้ (lane B, round `pnd0a5`, 2026-08-28)
`pirate-force-server`'s `src/pirateforce_foundation/mob_pickup.py` มีกลไก CLAIM ฝั่งเซิร์ฟเวอร์ครบแล้ว
(`resolve_claim`/`commit_pickup`/`dispatch_pickup_request`, unit-tested เขียวหมด) แต่ `runtime.py` **ไม่มี
call site เรียกมันเลยแม้แต่จุดเดียว** (grep ยืนยันรอบนี้: `dispatch_pickup_request` = 0 hits ใน `runtime.py`)
-- เพราะไม่มีใครยืนยัน **vital id จริง** ที่ client ส่งมาตอนคลิกเก็บของ (`runtime.py` มีคอมเมนต์ของตัวเองบอก
ตรงๆ ว่า "there is no known vital id for a client-originated pickup request on this project's wire yet")
สิ่งนี้เป็นคนละด่านกับ "ด่าน 2" (`session.select_and_start`'s `is_unmoved_baseline`, เลื่อนไป 30-31 ส.ค.
ตาม `notes_to_chief/20260827_1350_COO-DECISION-bagwall-second-wall-redesign-deferred-post-M4.md`) -- นี่คือ
ด่านที่**อยู่ก่อนหน้านั้นอีกชั้น**: ต่อให้ด่าน 2 เปิดวันที่ 30-31 ก็ยังเก็บของไม่ได้ถ้าไม่มีทางรับคำขอเข้ามา
ก่อน `GT-060` (`GAME_TEST_QUEUE.md`) เคยแตะคำถามใกล้เคียง (id derive `0x4543` สำหรับ `PickupTerrainThing`)
แต่เป็นคนละ pipeline (`HYP-PF-036` hypothesis scenario, ไม่ใช่เส้นทาง production ของ `mob_pickup.py`) --
ใบนี้ถามเฉพาะเส้นทาง production

### objective
1. หา vital id (opcode) ที่ client ส่งมาเมื่อผู้เล่นคลิกซ้ายบนวัตถุของตกพื้น (`PickupTerrainThing` หรือชื่อ
   เทียบเท่าในตารางเวิร์คของ Codex/`external/`) -- ยืนยันจาก capture corpus/ตารางที่ commit ไว้แล้วเท่านั้น
   ห้ามเดาจาก pattern ของ id อื่น
2. ถ้าเจอ: ระบุ payload shape เต็ม (object reference dword ที่ `mob_loot`/`mob_pickup` ใช้เป็น `drop_key`
   อยู่แล้วหรือฟิลด์อื่น, ตำแหน่งผู้เล่นมากับเฟรมหรือเซิร์ฟเวอร์ต้องอ่านจาก session state เอง, มี opaque byte
   อื่นที่ `mob_pickup.PickupClaim`/`opaque_u8` ต้องรองรับไหม) พร้อม provenance (offset/แถวตาราง/capture ไฟล์)
3. ถ้าชนเพดาน static (ไม่มี capture ที่มีการคลิกเก็บของจริงเลย) ให้เขียน bounded negative ตามกฎ -- ระบุด้วยว่า
   ต้องใช้ attended capture ใหม่ (คนละงานกับใบนี้) หรือยังมีมุมมอง static อื่นที่ยังไม่ลอง

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (แถว/คอลัมน์/offset/capture) · ชนเพดานให้เขียน bounded
negative แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
vital id + payload shape พร้อม provenance พอให้ chief เขียน call site จริงใน `runtime.py` (ต่อกับ
`mob_pickup.dispatch_pickup_request` ที่มีอยู่แล้ว) **หรือ** bounded negative ที่ชัดเจนว่า static ไปต่อไม่ได้
และต้องรอ attended capture ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**ทำไมมีค่า:** เป็นด่านที่บล็อก BUILD-006 (M5, กำหนด 31 ส.ค. 23:59) อยู่ก่อนด่าน 2 เสียอีก และไม่เคยถูกตั้ง
คำถามตรงๆ มาก่อน (50 กว่ารอบของสาย B ที่ผ่านมาพูดถึงแต่ด่าน 1/2/3 ของกำแพงกระเป๋า ไม่เคยเช็คว่า runtime.py
มีทางรับคำขอ pickup เข้ามาหรือยัง) -- ถ้าไม่ตอบ ต่อให้ด่าน 2 ออกแบบเสร็จวันที่ 30-31 ตามกำหนด BUILD-006 ก็ยัง
ทำไม่ได้อยู่ดีเพราะไม่มีทางส่งคำขอเข้าเซิร์ฟเวอร์เลย

## 🔬 RE-194 BASICATTR-0X54-SPEED-PLAYER-VS-NPC-CONFLICT-001 [STATIC-ON-BRIDGE]: `BasicAttr+0x54` (f32, mask `0x0040`, tag `0x2A`) has two different [MEASURED] client-write values for the same offset -- which one does a freshly-created *player* object actually carry?  [✅ **DONE / PASS - answered by `notes_to_chief/20260902_0501_RE-194-RESULT-PLAYER-FRESH-DEFAULT-400-NPC150-IS-WIRE.md`** · ปิดหัวใบโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 · **คำตอบ: ผู้เล่นที่เพิ่งสร้างพก `400.0f`** · `150.0` เป็นค่าที่มาทีหลังบนไวร์ของ NPC ไม่ใช่ค่าเกิดของผู้เล่น · จดหมายผลเขียนไว้เองว่า "ขอให้ chief กรอก `### result:` และปิดหัวใบให้ด้วย" แต่ไม่มีใครทำ ค้าง 3 วัน ทั้งที่ผลถูกใช้ปลายน้ำไปแล้ว (`COO-DECISION 20260902_0742` ปลดแบนเลข `400.0` หลัง RE-194 · LANE-DB `20260902_0623` ใช้ปิดคำถาม speed-walk seed) = ค้างบัญชี ไม่ใช่ช่องเทส (พบโดยลูกมือตรวจของ chief รอบนี้ จากรายการกวาดของ ka1-A `20260905_0106`) · เดิม assigned LANE-DB]

### result:
**DONE / PASS · 2026-09-02T05:01+07:00 · แหล่ง: `notes_to_chief/20260902_0501_RE-194-RESULT-PLAYER-FRESH-DEFAULT-400-NPC150-IS-WIRE.md` (RE runner) · กรอกลงหัวใบโดย chief (LANE-E) รอบ `kj0s6r`/R346**

- **คำตอบ**: `BasicAttr+0x54` ของ *player* object ที่เพิ่งถูกสร้าง = **`400.0f`** · ค่า `150.0` ที่เคยขัดกันคือค่าของ NPC ที่มาทีหลังบนไวร์ ไม่ใช่ค่าเกิดของผู้เล่น ⇒ ความขัดแย้ง "สองค่าที่ offset เดียวกัน" ไม่ใช่ความขัดแย้ง แต่เป็นคนละ object คนละจังหวะ
- **ชั้นหลักฐาน**: wire/DB (static-on-bridge) ชั้นเดียว — **ไม่มีชั้น client-observable** จึงไม่ต้องมี `OBSERVER_CONFIRMED` และห้ามยกผลนี้ไปอ้างว่า "เห็นบนจอ"
- **ผลถูกใช้ไปแล้วปลายน้ำ (ก่อนหัวใบจะถูกปิด)**: `COO-DECISION 20260902_0742` ปลดแบนเลข `400.0` · LANE-DB `20260902_0623` ปิดคำถาม speed-walk seed ด้วยใบนี้ · RE runner log `2026-09-02T05:05 RE-194 DONE jobs=1`
- 🔴 **nonclaim**: ใบนี้ตอบว่าค่าเกิดคืออะไร **ไม่ได้** ตอบว่าฟิลด์นี้แปลว่า "ความเร็ว" (G6 — ห้ามประกาศความหมายของฟิลด์จากการอ่านครั้งเดียว) · เกต `/speed` และเงื่อนไข (b'') ใน `NOW.md` ไม่ถูกแตะโดยใบนี้

### ทำไมเปิดใบนี้ (มอบหมายตรงจาก COO)

`COO-DECISION 20260901_1447` ข้อ 1 (`ADDRESSEE: chief`) สั่งเปิด RE ใบนี้ตรง ๆ เป็น **เคสนำร่อง**
ของคำถามใหญ่กว่า (25 ฟิลด์ที่มี default พิสูจน์แล้วแต่ยังไม่ยืนยันว่า resend กลางเกมปลอดภัย -- ดูใบ
`1420`/`1335` ของ LANE-DB) ตรวจแล้วทั้งสองเลขมีอยู่จริงในซอร์สที่ commit แล้ว ไม่ได้เชื่อจากใบขอเฉย ๆ:

- `src/pirateforce_foundation/player_wire.py:76` -- `PLAYER_LOGIN_MOVEMENT_SPEED = 400.0`, คอมเมนต์
  บรรทัด 66 อ้างว่าไคลเอนต์เขียน `400.0f` ลง `+0x54` ที่ `0x00464AF2` "on every fresh instance"
- `src/pirateforce_foundation/persistence_attr_compose.py:233/241` -- ค่า `400.0` เดียวกัน ที่ VA
  เดียวกัน (`0x00464AF2`) ถูกใช้เป็น candidate seed ของคอลัมน์ DB แต่คอมเมนต์บรรทัด 152/239 ของไฟล์
  เดียวกันเองเขียนไว้ตรง ๆ ว่า "+0x54 is the player's walk speed" เป็น **[สมมติของสาย DB - รอ RE]**
  ยังไม่ปิด
- `tests/test_npc_gait_wire.py:59` -- `PROVEN_WALK_SPEED = 150.0` (runtime_pass, สำหรับ **NPC** ไม่ใช่
  player) offset เดียวกันตามที่ `docs/FUNCTIONAL_COVERAGE.json` อ้างถึง
- `src/pirateforce_foundation/mob_death.py:856` -- `BASIC_BIT_MOVEMENT_SPEED = 0x0040 # f32 tag 0x2A
  @ +0x54` ยืนยัน offset/mask/tag ตรงกับทั้งสองจุดข้างบน เป็นฟิลด์เดียวกันแน่นอน ไม่ใช่การชนกันของเลข
  offset คนละฟิลด์

**ทำไมสำคัญ**: `persistence_typed_attrs.py:28/38/45` วางแผนจะ seed คอลัมน์ DB ของผู้เล่นจาก `400.0`
(ค่าตอนสร้างวัตถุ) แต่ถ้าไคลเอนต์จริงเขียนทับด้วยค่าอื่น (เช่น `150.0` เหมือน NPC หรือค่าที่คำนวณจาก
คลาส/สเตตัสตัวละคร) ทุกตัวละครที่ผ่าน path นี้จะได้ speed ผิดพร้อมกันเงียบ ๆ ก่อนที่ LANE-DB จะเริ่ม
เขียนโค้ด seed จริง (`COO-DECISION 20260901_1447` ข้อ 2 ยังไม่เปิดประตูส่ง `/speed` รออันนี้ก่อน)

### สิ่งที่ต้องตอบ

คำถามเดียว: object ผู้เล่น (ไม่ใช่ NPC/mob) ที่สร้างใหม่ตอนล็อกอิน มีค่าอะไรจริงที่ `BasicAttr+0x54`
ณ จุดที่สร้างเสร็จ ก่อน wire ใด ๆ จะมาทับ --

1. เป็น `400.0` แบบเดียวกับที่ `player_wire.py:66` อ้าง (แยกจาก NPC path ที่ใช้ `150.0`) หรือ
2. เป็น `150.0` เหมือน NPC (แชร์ constructor เดียวกัน) หรือ
3. เป็นค่าอื่น ที่คำนวณจากคลาส/สเตตัสตัวละคร ไม่ใช่ literal คงที่ตัวเดียว

อ่านจาก call site ที่ `0x00464AF2` โดยตรง (เส้นทางเดียวกับที่ `player_wire.py:66` อ้างถึง) --
แยกให้ชัดว่า call site นั้นถูกเรียกจาก constructor ของ **player** object จริง ไม่ใช่ constructor ที่ใช้
ร่วมกับ NPC/mob (ถ้าใช้ร่วมกัน ต้องหา branch/parameter ที่แยกค่าระหว่างสองประเภท)

### pass criteria

- **PASS**: ระบุค่าจริงของ player object พร้อม VA/offset ของ call site และแยกให้เห็นว่าเส้นทางของ
  player กับ NPC เป็น constructor เดียวกันหรือคนละตัว (ถ้าเดียวกัน ต้องโชว์จุดที่ค่าต่างกัน)
- **BOUNDED-NEGATIVE**: ถ้า `0x00464AF2` เป็น shared constructor ที่ resolve ไม่ได้ว่า branch ไหนใช้
  กับ player จริง (ต้องมี runtime trace ไม่ใช่ static เพียงอย่างเดียว) -- เขียนไว้ตรง ๆ ว่า static ปิด
  ไม่ได้ ต้องส่งต่อเป็น GT (attended, วัด speed จริงบนจอ) ไม่ใช่เดา

### ข้อห้าม

ห้ามเขียนโค้ด DB/persistence/attr-wire ใด ๆ จากใบนี้ -- LANE-DB เป็นเจ้าของโค้ด seed ต่อ · ห้ามสรุปว่า
`400.0` หรือ `150.0` ถูกโดยไม่มี VA ของ call site ที่แยก player ออกจาก NPC ชัดเจน

### สัญญาผู้บริโภค

เปิดโดย chief (มอบหมายตรงจาก `COO-DECISION 20260901_1447` ข้อ 1) -- **สาย DB บริโภคผล** (ผู้ใช้ค่านี้
seed คอลัมน์ DB ต่อ) เหมือนกับ `RE-193` ข้อยกเว้นเดียวกัน -- สาย DB อ่านผลรอบถัดไปที่เห็นแล้วปิดหัวใบเอง

### links

`notes_to_chief/20260901_1447_COO-ORDER-re-basicattr-0x54-speed-value-hold-speed-send-gate-staged-ps1-ownership.md`
(คำสั่งมอบหมายตรง ข้อ 1) · `src/pirateforce_foundation/player_wire.py:59-76` (ค่า 400.0 + คอมเมนต์
อ้าง VA) · `tests/test_npc_gait_wire.py:59` (ค่า 150.0 ของ NPC) ·
`src/pirateforce_foundation/persistence_attr_compose.py:233-241,284-288` (nonclaim ของสาย DB เอง
เรื่องค่านี้ยังไม่ปิด) · `src/pirateforce_foundation/mob_death.py:850-856` (ยืนยัน offset/mask/tag
เดียวกัน)
