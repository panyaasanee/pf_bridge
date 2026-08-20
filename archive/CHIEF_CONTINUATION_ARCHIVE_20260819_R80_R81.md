# CHIEF_CONTINUATION archive — รอบ 80–81 (2026-08-19)

ย้ายออกจากไฟล์หลักตอนรอบ 83 เพื่อคุมขนาด (ไฟล์หลักแตะ 108KB) · **ห้ามลบ**

สาระที่ยังมีผลต่อรอบหลัง ๆ ถูกยกไปไว้ในรอบ 82/83 แล้ว:
- รอบ 80: UI-REFRESH-001 (วินิจฉัยว่า **ไม่มี erase-by-key ในไบนารี**) + HP-DEATH-001 (pin ฟิลด์ HP)
- รอบ 81: NAMES-HOME-001 · DELETE-REFRESH-001 · HP-DEATH-002 · MP-OPT1-B (สี่ lane ขนาน)
  ทั้งสี่ถูกเทสจริงในรอบใหญ่ #4-#5 และ **PASS หมด** (ดูรอบ 83 ในไฟล์หลัก)

---

## รอบ 80 (2026-08-19 00:0x–01:xx) — takeover + static RE สองเลนขนาน: UI-REFRESH-001 + HP-DEATH-001

**สถานะเข้ารอบ:** กล่องจดหมาย **ว่าง** · inbox ว่าง · worktree **clean** · HEAD `fc204c7` · canonical `159F40EF..DBC6`
**🩹 takeover:** รอบ 79 จับ LOCK 18:2x แล้ว **ตายก่อน spawn ลูกมือ** (ตรงกับรอบ 76/73/74) —
LOCK mtime 18:21 · outbox ล่าสุด 18:11 · worktree ยังสะอาดตอน 00:0x = **เงียบ 5h42m** ครบเกณฑ์ตายทั้งสามข้อ
→ รอบ 80 สืบทอด **แผนเดิมของรอบ 79** ที่ยังไม่ได้เริ่มเลย (STATE-CHANGE FRAME static RE + งานขนานชิ้นที่สอง)

### [A] UI-REFRESH-001 — ตอบอาการ "client parse ผ่านแต่ UI ไม่ขยับ" ของรอบใหญ่ #3 (report-only)
**นี่คือคำตอบของคำถามที่ค้างมาตั้งแต่ GT-011 + GT-013 และมันเปลี่ยนแผน ไม่ใช่แค่เติมข้อมูล**
- **list ตัวละคร = buffer เดียว** ที่ `+0x180` ของ singleton `[0x1081A90]` · พิน 32 จุดที่ประกอบ `+0x180` ทั้ง `.text`
- mutator มีแค่ fill `0x5DDD00` (**caller เดียวทั้งไบนารี** = apply ของ `SelectActorVital 0x36EF`) ·
  append-one `0x5DDE10` (caller เดียว = `CreateActorVital 0x36CF`) · clear `0x5DDF00`/`0x5DE540`
- 🔴 **ไม่มี erase-by-key path ในไบนารีเลย** ⇒ **ack ของคำสั่งลบไม่มีทางเอาแถวออกจาก list ได้ ไม่ว่าจะแต่ง shape ไหน**
  ⇒ GT-011 เกณฑ์ client-observable **ผ่านไม่ได้โดยโครงสร้าง** — เราไม่ได้แต่ง frame ผิด เราเล็งผิดเฟรม
- delete ack `0x36DB` → `0x5EFDC0` → `cStateCreateActor::OnDeleteResult 0x4BAEB0` = **repaint ล้วน**
  (ค่า `+0x14 ∈ {3,4}` เขียน countdown `record+0xF4` · **ค่าอื่นรวม `1` ที่เราส่ง = ไม่ทำอะไรกับ list**)
  · negative ครบช่วง `[0x4BAEB0,0x4BB618)`: ไม่เรียก mutator · ไม่เรียก `RequestNext 0x4C7320` · ไม่แตะ `0x107A2C0`
- 🔴 **GT-013 ได้คำตอบเชิงโครงสร้าง ไม่ใช่ shape ที่ 4:** ทั้งไบนารีมี transition แค่ **18 จุด** (พินครบ)
  และมีแค่ **3 จุด** ที่ inbound vital เอื้อมถึง (`SelectActorVital`→cStateCreateActor ·
  `TeleportVital`→cStateSwitchScene · singleton `0x5DE000`→cStateSwitchScene)
  ⇒ **ไม่มีเฟรมชนิดใดในเกมที่พาผู้เล่นออกจาก `StateRunTime`** · logout apply `0x5EF930`→`0x5DC660`
  เป็น confirm-dialog controller ล้วน ⇒ shape 1–3 ล้มด้วยเหตุผลเดียวกัน **shape 4 บน envelope เดิมจะล้มเหมือนกัน — อย่าลอง**
- อาการปุ่มไม่ตอบสนอง = **กลไกพิสูจน์แล้ว ค่า live ยังเป็น ③เดา** (page variable `0x107A2C0` · jump table 15 ช่อง
  `0x4C3E30` · input gate `0x4BEEA9` ต้อง `==0` · animation ตั้ง `0x0B` ที่ `0x4BAE91` แล้วไม่เคยเขียนคืน)
- verifier `tools/pf_ui_state_refresh_static.py` **292 guards exit 0** (pure stdlib) + 33 tests

### [B] HP-DEATH-001 — เปิดแถว `combat/hp_death_and_respawn` (not_started → in_progress, report-only)
- **ไม่มี "เฟรมตาย" ให้หา — client derive เอง:** `IsDead` (vtable `+0x40`) ทั้งสองตระกูลคลาส
  (`0x454AC0` CNetActor/CMyActor · `0x43BDA0` CNetNPC/CAvatarNPC/Pet) ดึง Attr ผ่าน vtable `+0x74`
  แล้วคืน **current HP == 0** จาก `BasicAttr +0x44` (bit `0x0004`) ใต้ gate f32 `+0x58` (bit `0x0080`, const `0xF0989C`) `> 0`
  · max = `+0x48` (bit `0x0008`) พิสูจน์ current-vs-max ด้วย HUD bar helper `0x53EED0` **ไม่ใช่จากชื่อฟิลด์**
- ⭐ **chief แกะซ้ำเองด้วย disassembler จาก process สะอาด ไม่เชื่อ tool ของลูกมือ** — ตรงทุก instruction
  (`push esi / mov esi,ecx / call [vtable+0x74] / movss xmm0,[eax+0x58] / comiss [0xF0989C] / jbe`
   และฝั่ง NPC `cmp dword [eax+0x44], 0`)
- ⇒ **ระยะห่างจาก "ฆ่าตัวละครได้" = 1 mask bit + 1 float** · bit `0x0080` ตอนนี้ **ไม่เคย emit เลย**
- respawn = request-only: `ReliveVital 0x1AD4` เป็น 1 ใน **69 คลาส** ที่ inbound slot เป็น no-op ร่วม `0x710440`
  ⇒ **echo กลับไปไม่มีผลใด ๆ** · client **ไม่เลือกจุดเกิดเอง** (`ReliveMarkerVital 0x3DD6` เก็บ marker ที่
  `CMyActor+0x400` ซึ่งผู้อ่านอีกรายใช้ `u16 @+0x12` เป็น scene id ไป lookup `SCENE_NAME_TIP` เท่านั้น)
- verifier `tools/pf_hp_death_respawn_static.py` **191 guards exit 0** + 33 tests · coverage diff **12 บรรทัด แถวเดียว**

### 🩹 หนี้ที่ลูกมือรายงานเอง (ยกมาไว้ให้รอบหน้าเห็นก่อนวางแผน)
1. **A:** ค่า live ของ `0x107A2C0` ตอน GT-011 พิสูจน์ไม่ได้จาก static (เขียน guess ตรง ๆ ในรายงาน)
2. **A:** `guards_total=292` ผูกกับการมี v141 อยู่ (นอก repo = 283) — coupling ที่ตั้งใจแต่ควรรู้
3. **B:** chain `UpdateAttrVital → 0x4446F0` **ไม่ได้ไล่จนจบ** ⇒ "UpdateAttrVital ตัวเดียว latch ธง dead"
   เป็น **②อนุมานเชิงโครงสร้าง** · **GT-019 คือของถูกที่สุดที่ปิดหนี้ข้อนี้**
4. **B:** HP คู่รองที่ `ActorAttr +0x1A8/+0x1AC` ยังไม่ตั้งชื่อ (mapping `0x430E10` ยังไม่ decode) — จงใจไม่เรียกว่า HP เรือ
5. **B:** **ไม่มี damage model เลย** — HP ไปถึง 0 ได้ยังไงยังไม่แตะ · negative ของ SCENE-013 ยังยืน

### 📌 แผนรอบ 81 (สองเลน pre-approved ตามนโยบายข้อ 4 — ไม่ต้องรอ Panya)
- **DELETE-REFRESH-001 (`HYP-PF-021` ใหม่):** หลัง soft-delete commit → ส่ง **SelectActorVital rebuild** ตามหลัง ack
  · ⚠️ **ไม่ใช่การแก้ HYP-PF-015** — scope เดิมเขียนไว้เองว่า *"no claim about refresh behavior"* ⇒ นี่คือ **lane ใหม่**
  ไม่ใช่การรื้อของที่พิสูจน์แล้ว **จึงไม่ต้องถาม Panya** (ลูกมือเข้าใจผิดว่าเป็น stop rule — chief ตรวจ ledger เองแล้ว)
  → ปลดล็อก **GT-018**
- **HP-DEATH-002:** ขยาย encoder mask-driven เดิม (`stats_progression_hypothesis.py` 23 ฟิลด์) ให้ emit
  bit `0x0004`=0 + bit `0x0080`>0 ผ่าน opt-in scenario · headless proof ให้จบในรอบ → ปลดล็อก **GT-019**
- ทั้งสองใต้ pattern มาตรฐาน: opt-in · `production_allowed=false` · fail closed · ledger/verifier/matrix ครบ

### 🧹 งานแม่บ้านที่ค้าง
- `CHIEF_CONTINUATION.md` ~86KB · `GAME_TEST_QUEUE.md` ~57KB — **ทั้งคู่ใกล้เกณฑ์ archive** (100KB / 60KB)
  → รอบ 81 ควรย้ายรอบเก่าที่ปิดแล้วไป `pf_bridge\archive\` ทิ้ง pointer ก่อนเริ่มงานใหม่

**Gate 125 เขียวเต็ม (Windows `py -3`, baseline ใหม่):** verfA 0 (**292 guards** UI-REFRESH) · verfB 0 (**191 guards** HP-DEATH) ·
new-lane focus 0 (66) · prior-static focus 0 (86) · **pytest 885/0** (ทำนายไว้ 885 ก่อนรัน **ตรงเป๊ะ**) ·
canonical `159F40EF..DBC6` นิ่งข้าม pytest · seam 0 (22) · ledger PASS **27 ไม่ขยับ** (ไม่เปิด hypothesis รอบนี้) · domains 8 open 8 · diff clean
→ **commit `dd1a66c`** (11 files / 3371+ / 6- · **0 phantom delete** · tmp_obj 0 · index.lock ที่ sandbox ทิ้งไว้ถูกเก็บกวาดในจ็อบ)
> 🩹 บทเรียนเดิมยังจริง: `git status` จาก sandbox ทิ้ง `.git/index.lock` 0 ไบต์ที่ลบจากฝั่ง Linux ไม่ได้ —
> จ็อบ gate มีขั้นลบ orphan lock อยู่แล้ว **อย่าลบขั้นนั้นออก**
> ✅ ลูกมือทั้งสองเจอกติกา `.gitignore` deny-all เองและรายงานเอง (รอบที่ 3 ติดต่อกัน = กติกานี้ทำงาน)

---

## รอบ 81 (2026-08-19 01:0x–02:1x scheduled) — เคลียร์กล่องจดหมาย + **สี่ lane ขนาน** (subagents): NAMES-HOME-001 · DELETE-REFRESH-001 · HP-DEATH-002 · MP-OPT1-B

**จุดเริ่ม:** LOCK RELEASED จากรอบ 80 · **กล่องจดหมายมีของ 2 ฉบับ** (คำตัดสิน Panya ทั้งคู่ ผ่านเซสชันหลัก)
→ เคลียร์ก่อนตามกติกา แล้ว spawn ลูกมือ 4 ตัวขนานตามนโยบายข้อ 2

### 📬 กล่องจดหมายที่บริโภคไปแล้ว (ย้ายไป `notes_to_chief\consumed\` ในจ็อบ 128)
1. `20260819_0015_panya-decision-multiplayer-option1.md` — **multiplayer เดิน Option 1 ก่อน** (แล้วต่อ 2 → 3)
   · report-only · ห้ามสร้างเฟรมที่ยังต้องเดา · **หลังจบ Option 1 ห้ามเดินต่อ 2/3 เอง**
2. `20260819_0115_panya-decisions-names-and-lanes.md` — ① **NAMES fold = ทาง (ง)** ทำครบ 3 อย่าง
   ② **Lane 2/3 (แก้ไขตัวละคร/บัญชี) = ยืนยันพักรอ trigger จริง — ปิดคำถาม เลิกลิสต์ว่า "รอ Panya" ทุกที่**

> ⭐ **คิวคำถามถึง Panya ตอนนี้ว่างเกลี้ยง** — ไม่มีอะไรค้างรอคำตอบเธอเลย

### 🟢 สิ่งที่ประหยัดไปได้เพราะอ่าน history ก่อนสั่งงาน
Panya สั่ง Option 1 ทั้ง (a)+(b) แต่ **(a) ทำเสร็จไปแล้วตั้งแต่รอบ 78** (`MP-AUDIT-FOLLOWUP-001` ตอบ G1 ระดับ ①
· `actor_type` 2..6 · remote player = **2** · F8 ปิด · G2 แคบลง) → chief ตรวจเจอก่อน spawn จึงย้ายกำลังทั้งหมดไป (b)
**บทเรียน: ก่อน spawn ลูกมือให้เช็ค `reports/` ว่างานนั้นทำไปแล้วหรือยัง — รอบนี้เกือบสั่งทำซ้ำ**

### ผลงานสี่ lane

**[1] NAMES-HOME-001** (คำสั่งตรงจาก Panya ทาง (ง))
- `docs/PF_VITAL_NAMES.json` = **บ้านของชื่อที่เดียว 52 entry** (49 parse จาก v141 + 3 ที่เราแกะเอง
  `0x1B40 LogoutVital` slot `0x108207C` · `0x36DB DeleteActorVital` slot `0x1081FD0` · `0xAC52 Channel_LocalTalkMessageVital` slot `0x1084458`)
- `tools/pf_vital_names.py` = loader pure stdlib (นิยาม `wire_id()` และ parser ของ v141 **ที่เดียว** ลด drift)
- `tests/test_vital_names_table.py` = **เทสบังคับความจริง** — superset ของ v141 + ชื่อที่ซ้อนต้องตรง + hash ตรงทั้ง 52
  · **ลูกมือทดสอบกับดักจริง**: จำลอง Codex เติมชื่อลง v141 → แดงทันที พร้อมข้อความชี้กลับมาที่ไฟล์เรา
- resolver อ่านตารางเราเป็นแหล่งหลัก คง cross-check v141 เป็นยาม · **guard 35 → 43** (3 ตัวใหม่เทียบ slot ที่ thunk เขียนจริง)
- คำเตือนเรื่องกะ Codex เขียนไว้ทั้ง `COMMAND_HANDOFF.md` และ `AI_TRANSFER_HANDOFF_20260817.md`
- 🔎 ค้าง: `pf_bridge\VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มี **327 ชื่อ** = บ่อ candidate ตัวถัดไป
  ยังไม่ fold เพราะแต่ละตัวต้องมีหลักฐาน literal→slot ก่อนตามกติกาที่เขียนไว้ในหัวไฟล์เอง

**[2] DELETE-REFRESH-001 = `HYP-PF-021`** — ปลดล็อก **GT-018**
- แยกเป็น lane ของตัวเองเพราะ stop_rule ของ HYP-PF-015 เขียนไว้ตรง ๆ ว่าห้ามเติม list-refresh เข้าไป
  ⇒ **HYP-PF-015 ไม่ถูกแก้แม้แต่ไบต์เดียว** stop_rule ยังจริงตามตัวอักษร
- ตอบ delete op-1 = **2 เฟรม**: ack เดิม (hash pin เดิม) + `SelectActorVital 0x36EF` v10 ที่ **+0.35 วิ**
- ⭐ **ไม่ประกอบเฟรม rebuild เอง** — เรียก `LegacyProjector.character_list` เดิมแล้ว *ตรวจ+ปักหมุด*
  (เฟรมนี้ client จริงรับทุก login) ⇒ **ไม่มีไบต์เดาแม้ไบต์เดียว**
- ⭐ ลูกมือกลับไปสแกนไบนารีเองแทนเชื่อ scan รอบ 80 → เจอ **writer ตัวที่ 21 ของ `0x107A2C0`**
  `0x4BD650: mov [0x107A2C0], edi` ใน vtable `0xF16520` slot `+0x10` ของ `cStateCreateActor` (enter hook)
  ⇒ คำทำนายอัปเกรดเป็น **"list เปลี่ยน + ปุ่มกลับมากดได้"**
- ⚠️ **ยังเป็นอนุมาน:** policy "ตอบ delete ด้วย rebuild" เป็น designed hypothesis ไม่มี capture ไหนแสดง ·
  ค่า live ของ `0x107A2C0` ตอน GT-011 ไม่เคยถูกอ่าน · "แถวหายจากจอ" ยังเป็น pixel claim

**[3] HP-DEATH-002 = `HYP-PF-022`** (เปิดใหม่ **ไม่ amend HYP-PF-020** เพราะ stop_rule ของ 020 จำกัดไว้ที่ 23 ฟิลด์) — ปลดล็อก **GT-019**
- emit bit `0x0004`=0 + bit `0x0080`>0 ผ่าน opt-in scenario · 4 เฟรม (BASELINE / TIMER_ARMED / HP_ZERO / HP_RESTORED)
  · BASELINE **byte-identical กับ pin ของ HYP-PF-020**
- ⭐ **ปิดหนี้ B1 พร้อมแก้คำตอบเดิม:** chain จริง = `UpdateAttrVital 0x5F2400` → `vtable+0x10` (`0x464E40` อ่าน **class id ไม่ใช่ identity**)
  → lookup `[0x1032EC4]+0x130` @`0x5F24C9` → `vtable+0x24` @`0x5F2504` → `0x464F30` → `0x464B40` (copy ทั้งบล็อกไม่ดู mask)
  · **ไม่ใช่ `0x4446F0`** — caller เดียวของมัน `0x4566A7` เข้าไม่ถึงจากท่อนี้
  ⇒ **ไม่มี `_F_DIE_000` ไม่มี `TargetIsDead` latch** มีแค่ `Main_Dead` + HUD
- ⚠️ **ค่า `60.0f` เป็นการเลือก ไม่ใช่ค่าที่พิสูจน์** — gate ที่ `0x44A572` ต้องการ `timer >= DURATION_DYING - 0.5`
  โดย `DURATION_DYING` (int @`0x102249C`) = **20 ใน image** แต่ค่าที่ deploy จริงไม่รู้
- ล็อกหลายชั้น: production_allowed=false · scenario allowlist exact-match · flag บังคับ `--db` + exclusive ·
  **unlock token เทียบด้วย identity** (dataclass ที่ `==` กันเป๊ะก็เปิดไม่ได้) · แผนต้องจบที่เฟรมคืน HP

**[4] MP-OPT1-B** (report-only ตามคำสั่ง — ไม่แตะ `src/` ไม่ flip matrix ไม่เปิด hypothesis) — เพิ่ม **GT-020**
- **G8 ตอบแล้ว และแรงกว่าที่ audit คาด:** `0x42BF` มี 2 field — `wstring @+0x14` = บัญชี · `string @+0x30` = **รหัสผ่าน cleartext**
  · field ไหนคืออะไร **พิสูจน์จากจุด assign** (`DoLogin 0x4C5920` @`0x4C5A61..73`) ไม่ใช่จากตำแหน่ง
  · ชนิดยืนยันจาก **import ctor ของ MSVCP90** ไม่ใช่เดาจากรูปร่าง
- ⭐ **client hex-decode ค่า `-acc`** ผ่าน `0x89B070` (call site เดียวทั้งอิมเมจ) ⇒ `-acc test` → `0E 00 00 00`
  **ที่ capture 63 ไฟล์เห็นมาตลอด — ไม่ใช่เพราะเป็นค่าคงที่ แต่เพราะเราส่ง argument เดิมทุกครั้ง**
  · verifier สร้าง jump table ของ `hexval` ใหม่จากไบนารี พิสูจน์ว่าเป็น hex เป๊ะ **ครบ 65536 code point 0 mismatch**
- ⚠️ **`-acc bob` ใช้ไม่ได้** ต้องใส่ hex · และ `v141.make_game_login_ack` แช่ literal ของบัญชีเก่า ⇒ server จะ echo บัญชีเก่ากลับ
  (static ไม่พบ compare ในไบนารี แต่ถ้า client เด้ง = **ผลบวกที่มีค่ามาก** ให้จดแล้วจบเทส **ห้ามแก้ `src/` ในเซสชันเทส**)
- **Option 1 ครบแล้ว** ((a) รอบ 78 + (b) รอบนี้) → 🔴 **ห้ามเดินต่อ Option 2/3 เอง** ต้องเอาผลให้ Panya เคาะก่อน

### 🔴🔴 บทเรียนใหญ่ของรอบนี้ — จ็อบ 128 แดง และมันจับของจริง

จ็อบ 128 เขียวหมดยกเว้น pytest **1 subtest**: `game_captures_with_the_same_account` → `44 != 46`

**สาเหตุ = เครื่องมือของรอบนี้เองละเมิดกฎ read-only:**
`tools/pf_delete_refresh001_headless_replay.py` บูต server จริงโดย **ไม่ส่ง `--capture-root`** และรันด้วย `cwd = repo root`
→ server เขียน capture ลง **`capture_v141/` ซึ่งเป็น golden corpus ที่ pin ไว้** → corpus โต **69 → 72 ไฟล์**
→ ตัวเลข 44 ที่ MP-OPT1-B ปักไว้กลายเป็น 46 → เทสยิง

**สามอย่างที่ต้องจดไว้ ไม่ใช่แค่แก้:**
1. **`capture_v141/` อยู่ใน `.gitignore`** → `git status` เงียบสนิท · v141 guard ที่ chief ใส่เองก็เงียบ
   (เพราะไฟล์ v141 ไม่ถูกแตะจริง ๆ — **corpus ข้าง ๆ ต่างหากที่ขยับ**)
   ⇒ **สิ่งเดียวที่จับได้คือตัวเลขที่ milestone อื่น pin ไว้ และมันจับได้โดยบังเอิญ** — ตัวเลขที่ปักหมุดคุ้มค่าจริง
2. **ลำดับ fail-closed ทำงานถูกต้อง** — replay รันก่อน pytest · pytest แดง · commit ถูกข้าม · ไม่มีอะไรเข้า history
3. **แก้ที่ต้นเหตุ ไม่ใช่ที่เทส:** `--capture-root` เป็น**บังคับ** ในสคริปต์แล้ว · default อยู่ข้าง scratch DB ·
   และ **ปฏิเสธทุก capture root ที่ resolve เข้าไปในรีโป ก่อนเปิด socket** (กติกาเดียวกับที่มันใช้กับ db/json อยู่แล้ว)
   · ไฟล์แปลกปลอม 3 ตัว **ย้าย** ไป `pf_bridge\archive\stray_captures_20260819\` (ไม่ลบ) → corpus กลับเป็น 69
   · จ็อบ 129 บูตซ้ำแล้ว**นับ corpus อีกรอบเพื่อพิสูจน์ว่าไม่มีอะไรถูกเขียนลงไป** → **69 เท่าเดิม · capture ลง scratch 7 ไฟล์**

**หนี้ที่เปิดไว้จากบทเรียนนี้ (งานรอบหน้า):** ตัวเลข `game_captures_with_the_same_account` วัดด้วยการ **scan ไดเรกทอรี**
⇒ เสถียรเท่าวินัยของทุกคนเรื่องที่วาง capture เท่านั้น · **ควรปักหมุดกับชุดชื่อไฟล์แทน**
แต่การแก้ tool ตัวนั้นต้อง re-hash manifest ของ MP-OPT1-B ด้วย ⇒ **แยกเป็นรอบของตัวเอง อย่ายัดใส่จ็อบ retry ตอนตีสอง**

### 🩹 บทเรียนที่สอง — งานขนานสี่ตัวชน `.gitignore`
รีโปนี้ **deny-by-default** ทั้ง `/tools/*` และ `/reports/*` ⇒ ทุก lane ต้อง allowlist ไฟล์ตัวเอง
· ลูกมือทั้งสี่แก้ไฟล์เดียวกันพร้อมกัน → **allowlist 3 บรรทัดของ lane 2 หายเงียบ**
· ถ้า commit ไปแบบนั้น **HYP-PF-021 จะดูเหมือน commit แล้ว ทั้งที่ verifier กับ replay ของมัน git มองไม่เห็น**
· chief ตรวจ `git check-ignore` ทีละไฟล์ก่อน commit จึงเจอ → ใส่กลับพร้อม comment อธิบาย
⇒ **กติกาใหม่: หลังลูกมือขนานเสร็จ ต้อง `git check-ignore` ไฟล์ใหม่ทุกไฟล์ก่อนสร้างจ็อบ commit**

### งานแม่บ้าน
- `CHIEF_CONTINUATION.md` **92KB → 58KB** (ย้ายรอบ 76–78 ไป `archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R78.md`)
- `GAME_TEST_QUEUE.md` ย้าย **GT-011** (ปิดในทางโครงสร้างแล้ว ผู้สืบทอด = GT-018) ไป
  `archive\GAME_TEST_QUEUE_ARCHIVE_20260819_GT011.md` แล้วเพิ่ม GT-020 → 63KB
- ลบ `tools/_append_hyp_pf_021.py` (สคริปต์ one-shot ที่ลูกมือลบเองไม่ได้) ในจ็อบ 128

### สถานะคิวเทสหลังรอบนี้
- **GT-017** 🟢 พร้อมรัน (ปลดล็อกตั้งแต่รอบ 78)
- **GT-018** 🟢 ปลดล็อกแล้ว — server args: `--delete-refresh-hypothesis-scenario scenarios\delete_refresh_hypothesis_list_rebuild.json`
- **GT-019** 🟢 ปลดล็อกแล้ว — server args: `--hp-death-hypothesis-scenario scenarios\hp_death_hypothesis_death_sweep.json` · ทริกเกอร์ = พิมพ์แชต 1 ครั้ง
- **GT-020** 🟢 ใหม่ ไม่มี prerequisite ไม่ต้องใส่ scenario — แค่เปลี่ยน `-acc`/`-pwd` ของ client
- **GT-015** PENDING เดิม
⇒ **มีของให้เทสรอบใหญ่ถัดไป 5 รายการ พร้อมรันทันทีทั้งหมด**

### ผลรอบ 81 (จ็อบ 129 — retry หลังจ็อบ 128 แดง)
gate 126 **เขียวเต็ม**: verifiers `names 43 / delref 45 / hpdeath 66 / loginreq 126` ทุกตัว exit 0 ·
regression `stats020 85 / hpstatic 191 / uiref 292` ไม่กระเทือน · headless **hpdeath 0 · deleterefresh 0** ·
**corpus guard: 69 ก่อนบูต → 69 หลังบูต · capture ลง scratch 7 ไฟล์** (ข้อพิสูจน์ว่าแก้ต้นเหตุได้จริง) ·
**pytest 1014/0** (653 subtests) · canonical `159F40EF..DBC6` นิ่งข้าม pytest · seam 0 · **ledger PASS 29** ·
domains 8 · v141 guard clean · diff clean
→ **commit `6891372`** (31 files / +10426 / −1994 · **0 phantom delete** · tmp_obj 0)

**เกณฑ์เขียวรอบถัดไป (gate 127):** pytest ≥ 1014 · ledger 29 (+1 ถ้าเปิด HYP ใหม่) · domains 8 · seam 0 ·
canonGuard 0 · **corpus `capture_v141\GAME_*.txt` = 69**

### next (pre-approved ทั้งหมด ไม่ต้องรอ Panya)
1. 🔴 **หนี้จากบทเรียนรอบนี้** — pin `game_captures_with_the_same_account` กับ **ชุดชื่อไฟล์** แทนการ scan ไดเรกทอรี
   · ต้อง re-hash manifest ของ MP-OPT1-B ด้วย ⇒ **แยกเป็นรอบของตัวเอง**
2. **NAMES fold ต่อ** — `pf_bridge\VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มี 327 ชื่อ = บ่อ candidate
   เติมทีละตัวเมื่อมีหลักฐาน literal→slot ครบตามกติกาที่เขียนไว้ในหัว `PF_VITAL_NAMES.json` เอง
3. **milestone สำรอง** (แถว not_started ใน FUNCTIONAL_COVERAGE = pre-approved): `combat/damage_and_hit_result`
   — ยังไม่มี damage model เลย = ช่องว่างใหญ่ที่สุดที่เหลือของ combat และเป็นสิ่งที่ทำให้ GT-019 มีความหมายจริง
   (ตอนนี้เราทำให้ HP เป็น 0 ได้ แต่ยังไม่มีอะไรทำให้มันลด)

---
