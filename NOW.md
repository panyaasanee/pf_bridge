# NOW — สถานะปัจจุบัน (ประวัติอยู่ใน `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-07 08:45 +07:00 โดย COO (รอบ `0845` ×12 ใบ):
- 🔴 **`HEADLESS_PROOF:` ทุกใบ attended** (PANYA `0159`): ในบล็อก `ATTENDED:` = โทเคนคอนโซลจาก headless **บนคอมมิต main ปัจจุบัน** ว่ากลไกติดอาวุธในฉากเป้าหมาย + คอมมิต/วันที่ (≤3 วัน) · ไม่มี = ไม่ขึ้นรถบัส · ใบบนรถบัสเติมใน **2 รอบของเจ้าของ** · ka1-A รันซ้ำ ไม่ตรง = ตัดใบ · กลไกติดแฟล็ก = โทเคน SKIPPED + `FLAGGED_MECHANISM_PROOF:` (`0845`)
- 🔴 **คัดใบ attended = LANE-K** (`0159`): (ก) >7 วัน (ข) โค้ดที่ใบพึ่งพาเปลี่ยน (ค) มีผลใหม่ครอบคลุม → ถอนจากสแนปช็อต เจ้าของยืนยัน/ยกเลิก (K ยกเลิกเองไม่ได้) · ค้างตอบ = `GT-272` (DB) · `[STATIC-ON-BRIDGE]` = ติดธง ไม่ถอน
- 🔴 **`.claude/settings.json` = เขต COO+chief** (PANYA `0316`) · สายอื่นแตะ = preflight แดง
- 🔴 **แดงบนโคลนคลาวด์ ≠ เกตแดง**
- 🔴 **PANYA `1910`**: GT-233 ปิด ห้าม trial `AddSurveyData` · ห้ามขอเครื่องเจ้าของเพื่อ M2 จนมีเฟรมอ้าง binary · ชื่อใหม่ ≤100 (เกตบังคับ) ห้าม rename ของเก่า · **เลขใบ/เนื้อใบ/พับผล/archive/snapshot = LANE-K** เนื้อใบส่ง `*-TO-K-gt-body-*`

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
- **routine K ต้องได้ environment มี git ทุกรอบ** — รอบ `camatf` มีแต่ MCP เขียนคิวไม่ได้ (K `2217`)
- **`bg0002` ย้ายไปกฎ `cline` ไหม?** ตรงกับ census ของเกม (12) แต่ **ลบ template `103` ที่คุณเขียนเองในใบ 27 ส.ค.** — ไม่ย้ายจนกว่าคุณเคาะ (`0845`)
- **เพดานไฟล์ในพรอมป์ K ไม่ตรงเกต** (300/200 KB vs 2.4 M/409,600) — ยึดเลขเกต · `prompts/` คุณแก้ได้คนเดียว

## รอเครื่องคุณ (คิวจริง = `QUEUE_STATUS_SNAPSHOT.md`)
1. **`GT-288` (B) ใบแรก** — รอ B พลิก READY + `HEADLESS_PROOF:`
2. ถัดไป `GT-276` CS · `GT-220`/`GT-223` — **ทุกใบต้องมี `HEADLESS_PROOF:`** · M2 ยังไม่มีใบ

## กติกาของไฟล์นี้ (ห้ามลบสี่บรรทัดนี้)
- ผู้เขียน: **Panya และ COO เท่านั้น** · คนอื่นเสนอผ่านจดหมายจ่าหน้า `ADDRESSEE: COO`
- **"เสร็จ" ติ๊กได้โดย Panya คนเดียว** — สูงสุดที่ COO ไปถึงได้ = `รอเจ้าของยืนยัน` (ขึ้น main ไม่ใช่ "เสร็จ" · `production_allowed = False` ไม่นับว่าขยับ)
- **COO เตือน** — ย้ายข้อที่คิดว่าเสร็จขึ้น `รอ Panya ติ๊ก` ในรอบที่ตัดสิน · ค้าง >6 ชม. = ทวงผ่านช่องทางที่เธอเห็น
- เพดาน **12 KB / 60 บรรทัด** (PANYA `2039` · เกต preflight) · ข้อที่ปิดแล้ว **ลบทิ้ง** · กฎบ้านอยู่ `AGENTS.md §7` + `prompts/COMMON_LANE_ROUND.md` — NOW ไม่เก็บกฎซ้ำ ยกเว้นที่ยังไม่ลง §7
- 🔴 ยังไม่ลง §7: **`GameMaster.dll` ติดถาวร ห้าม rollback** · **reaper ปิดเอง**: claim ผี >3 ชม. / `SUPERSEDED-BY:`/`DUPLICATE-OF:` · **ห้าม `rm -r`** · `ATTENDED:` บังคับ · `prompts/` ห้ามสายแก้ · grep ที่ห้า `reference_codex_attr/` · `.LANEK-FOLDED.txt` = พับแล้ว · **pin แดงตาม docstring = กลับ pin ในใบเดียวกัน** · grep กลไกไม่ใช่การสะกด · เพดานต่อใบ 8,192 B
- 🔴 **ตัววัด**: `*RESULTS*`/`OBSERVER_CONFIRMED` ไม่มี `.LANEK-FOLDED.txt` >6 ชม. = escalation K
- 🔴 **shared world**: โลกต่อฉากใน process แชร์ทุก session · A = registry · B เขียน combat state ลง registry ของ A · DB ไม่รับงานโลก · ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:`
- 🔴 **PANYA `0039` หลักถาวร: โลกใบเดียว + ฟิลเตอร์มองเห็น NPC ต่อผู้เล่น** · `Player.MobAppear` = **ธงต่อผู้เล่น ไม่ใช่ spawn** · **rank 0 = ธง · rank>0 = ลงโลกร่วม** · ส่งให้คนนี้ = (ไม่ผูกเควส ∧ `n_MOB_APPEAR=1`) ∨ เควส `s_QUEST_BEGIN/END` ∨ ธง true · **ออกแบบฟิลเตอร์ก่อนแตะ MobAppear** (A)
- 🔴 RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING:` · `KNOWN_RED_MAIN:` `test_ui_wire_name_census` ×2 (UI ปิด) · **สิทธิ์ฆ่า: ใบเซ็น > derive > ตาราง** ฉากใหม่ต้องมีใบเซ็นหรือ census

## บันไดไมล์สโตน (`20260904_0233` · ไม่มีกำหนดวัน · ผ่าน M(n) ก่อนประกาศ v(n))
- ✅ **M1/v1** ประกาศแล้ว (R249)
- ⏳ **M2 "ออกจากเมืองได้" ← อยู่ตรงนี้ · ทาง (ก) `1910`**: ตัวบล็อก = เฟรมตอบ `0x1FB2` trigger 2/3 (`RE-286`: `TriggerResult` · A ต่อสาย) · TIER 3 ต้องมี discriminator ว่า "เกาะ ≠ น้ำเปล่า" — เฟรมเปล่าไม่ปลดล็อก · เกณฑ์ผ่าน: ใกล้เกาะ → "รายงานกัปตัน" → กด → วาปเข้า **เกาะ 2 และ 3 บนจอ** · ห้าม server ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวล
- **M3 = P-2** (ชั้นแรก ✅ GT-281 · ชั้นสอง = `GT-288`) · **M4 "ตีได้ตายได้"**: มอนตีกลับ HP ลด · ตาย · ศพไม่ค้าง · เกิดใหม่ (B `GT-224`) · **M5** เก็บได้+รอด relog · **M final** ครบวงจร
- 🔴 **LANE-DB**: แขน (ข) seam `1452` (`RE-282`: `POTENTIAL` ว่าง) · `0x309A` RE-blocked · `GT-272` ถูกถอน — ตอบ K ว่ายังวัดของเดิมไหม + `HEADLESS_PROOF:` · `GT-291` โมดูลขึ้น main แล้ว (`c19132f` ทาง `#1000`) ⇒ เติมโทเคนได้ · ใบสร้าง A/DB: ออก 126 คืน HP · BoatHealth ≠ -1
- **Q** (`TriggerResult` ไม่ใช่ของ Q): ครึ่งอ่านลงแล้ว · **`Lv` = เลเวลผู้เล่น · ปัดลง · ไม่รู้เลเวล = ปฏิเสธ (`0845`)** · งานแรก = เนื้อใบ RE ปัดเศษ · ครึ่งเขียน = คอลัมน์ DB · `Player.MobAppear` = A หลัง P-2 · `CastSkill*` encoder = CS ทำเมื่อ Q ขอ
- **LANE-K** (`0845`): D1/D2/D12 ก่อน · ห้ามต่อเข้าเกต · 18 แถว taglint = คิวพับ 3-4/รอบ · หัวใบซ้ำ = บรรทัดชี้ทาง ห้ามยุบ · **ห้ามสตับปิดปากสแกนเนอร์**

## งานด่วนตอนนี้
- **หาง P-1**: ปิดด้วย `GT-223` · หนี้ `DropLedgerCell` ข้ามฉาก · ห้ามลบแถว ledger
- **P-2 สีชื่อ (= M3)**: ค่าจริงจาก `GT-288` · สี = คู่ (คนดู, มอน) `NPCAttr+0x98` · ห้าม faction-only/hardcode
- **LANE-GM** (`0641`: ผู้อ่าน = คน cp874 · หยุดชุบแข็ง · `_Mirror`/`lane_hooks` = chief): ดัน PR `vxr32s` ให้เขียว · P-3 `GT-279`: ปุ่มส่ง `0x51E9` จริง แต่ `capture_raw_gm_command` ไม่เขียนไฟล์ · host-property แดงซ้ำ = หยุด เขียน COO
- **M4 · LANE-B**: **1b (`0845`): ห้าม regenerate bg0002/ลบ `103` — ตัวจริง = `;` ใน `s_OUTFIT` ปฏิเสธ 40 placement ⇒ ใบ RE "เลือก outfit ตัวไหน" งานหน้า** → 2 `2032` parser (ห้ามแตะ wire) → respawn 120 s → สมุดโลก · `apply_hp_damage` พัก Door B · **`_letter_exists_for` = ลายมือ git (`COO:`) ไม่มี git = แดง (`0845`) งานแรก** · `GT-288` พลิก READY + `HEADLESS_PROOF:`
- **chief (`0641` หนึ่งงานต่อรอบ)**: **(1) กู้ `#997`: ตัด `yaml` · deps เท่าเกต · แดงถ้า 0 เทส · pin ก่อน blocking (เขียว = suite) → (2) กฎ marker ทุก PR สองรีโป + ห้ามสะกดสตริง + วัดอะไร merge `#922` (`0845`) → (3) ตัวกรองสแกนผลยังไม่พับ (เฉพาะใบอ้าง `GT-`/`RE-`) → (4) `_Mirror`: encoding + เขียนอะตอมมิก (ห้ามแตะ v141) → (5) `lane_hooks.fire()` ครอบ `BaseException` re-raise `KeyboardInterrupt` → (6-11) `AGENTS.md`<30 KB · §7(+host-property) · preflight server · coverage `make_show_message` · #948 seed · ชื่อยกเว้น 180
- **LANE-A**: tier 3 รับรอง (`0845`) · ใบ RE `Bg3001.tgr` → K → ใบ attended · `TriggerResult` = ของ A · **ห้ามส่งเฟรมเดา**
- **LANE-UI**: **พิน 30/286/11 · evidence ตัดเลขบรรทัด (`0845`) ปิด** · งานแรก `2032` แถบ n/327 · tool ข้าม docstring (AST) · express/community ห้าม · **CS** (`0845`): งานแรก `CORE-REQUEST` ประตูคลาส · `#1002` ห้ามใส่ marker คืน/ห้ามปิด · สูตรเปลี่ยน = ขยับ pin 891 คอมมิตเดียวกัน

## ห้ามทำจนกว่า P-2 ปิด
- GT-146 + ใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (`0904_2115`) + `GT-274` (`0645`)

## เมื่อไม่มีงานด่วน — ท่อ promotion (`2039` ข้อ 3)
- 5 ตัวแรก (`docs/PROMOTION_BACKLOG.md`): 1 `remote_player_hypothesis` A · 2 `lane_a_choose_npc_scene1` A · 3 `ground_loot_hypothesis` B · 4 `logout_dialog_open_hypothesis` UI · (`skill_attr` ถอนตาม `1348`) · `item_operate_res` = รอ seam ของ B (`0845`) · 9 แถว B รอ P-2
