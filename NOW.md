# NOW — สถานะปัจจุบัน (ประวัติอยู่ใน `COO-ROUND-*`)

ตรวจล่าสุด: 2026-09-07 04:05 +07:00 โดย COO (รอบ `0405` ใบ ×7 · คำสั่งเจ้าของ `0159`+`0316`):
- 🔴 **`HEADLESS_PROOF:` ทุกใบ attended** (PANYA `0159`): บรรทัดเดียวในบล็อก `ATTENDED:` = โทเคนคอนโซลจากรัน headless **บนคอมมิต main ปัจจุบัน** ว่ากลไกติดอาวุธในฉากเป้าหมาย + วันที่ + คอมมิต (≤3 วัน) · ไม่มี = ไม่ขึ้นรถบัส · ใบที่อยู่บนรถบัสเติมใน **2 รอบของเจ้าของใบ** (จาก K `kxpzxi`) · ka1-A รันซ้ำก่อนบูต ไม่ตรง = ตัดใบ
- 🔴 **คัดใบ attended = LANE-K** (PANYA `0159` ข้อ 2 · ย้ายจาก chief): (ก) >7 วัน (ข) โค้ดที่ใบพึ่งพาเปลี่ยน (ค) มีผลใหม่ครอบคลุม → ถอนจากสแนปช็อต เจ้าของยืนยันซ้ำ/ยกเลิก (K ยกเลิกเองไม่ได้) · ถอนแล้ว `GT-258` GM · `GT-262` UI · `GT-151` A → ตอบ `*-TO-K-*`
- 🔴 **`.claude/settings.json` = เขต COO+chief** (PANYA `0316`): มี `deny` (force push · `rm -r` · `reset --hard` · `branch -D` · `clean -f` · เขียนนอกรีโป · `curl`/`wget`) · **ห้าม** `enableAllProjectMcpServers` · สายอื่นแตะ = preflight แดง
- ✅ **main เขียวสองรีโป** (`#969` `#972` `#974` `#975`) · `PF_NAME_COLOUR_SWEEP` (RE-155) บน main → **`GT-288` พลิก READY ได้** · PR ที่ reaper ปิด กู้ด้วย cherry-pick **บนฐาน main ปัจจุบัน หนึ่ง PR ต่อรอบ** · fetch main ก่อนเปิด PR
- 🔴 **PANYA `1910`**: GT-233 ปิด ห้าม trial `AddSurveyData` · ห้ามขอเครื่องเจ้าของสำหรับ M2 จนมีเฟรมอ้าง binary · ชื่อไฟล์ใหม่ ≤100 รวม `.md` ห้าม rename ไฟล์เก่า · **เลขใบ/เนื้อใบ/พับผล/archive/snapshot = LANE-K** (`1259`) เนื้อใบส่ง `*-TO-K-gt-body-*`

## รอ Panya ติ๊ก  ← คุณดูหัวข้อนี้หัวข้อเดียวพอ
(ห้ามเกิน 5 ข้อ · ติ๊กแล้วลบทั้งข้อ)
- **routine K ต้องได้ environment มี git ทุกรอบ** — รอบ `camatf` มีแต่ MCP เขียนคิวไม่ได้ (K `2217`)

## รอเครื่องคุณ (คิวจริง = `QUEUE_STATUS_SNAPSHOT.md`)
1. **`GT-288` (B) ใบแรก** — sweep บน main แล้ว รอ B พลิก READY · จอเห็น Fish ชมพู/Eagle เขียว (R322B)
2. ถัดไป `GT-272` DB · `GT-220`/`GT-223` · `GT-276` CS — **ทุกใบต้องมี `HEADLESS_PROOF:` ก่อน** · M2 ยังไม่มีใบ

## กติกาของไฟล์นี้ (ห้ามลบสี่บรรทัดนี้)
- ผู้เขียน: **Panya และ COO เท่านั้น** · คนอื่นเสนอผ่านจดหมายจ่าหน้า `ADDRESSEE: COO`
- **"เสร็จ" ติ๊กได้โดย Panya คนเดียว** — สถานะสูงสุดที่ COO ไปถึงได้คือ `รอเจ้าของยืนยัน` (โค้ดขึ้น main ไม่ใช่ "เสร็จ" · `production_allowed = False` ยังไม่นับว่าขยับ)
- **COO เตือน** — ย้ายข้อที่คิดว่าเสร็จขึ้น `รอ Panya ติ๊ก` ทันทีในรอบที่ตัดสิน · ค้างเกิน 6 ชม. = ทวงเธอผ่านช่องทางที่เธอเห็นจริง
- เพดาน **12 KB / 60 บรรทัด** (PANYA `2039` · เกต preflight) · ข้อที่ปิดแล้ว **ลบทิ้ง** · กฎบ้านอยู่ `AGENTS.md §7` + `prompts/COMMON_LANE_ROUND.md` — NOW ไม่เก็บกฎซ้ำ ยกเว้นที่ยังไม่ลง §7
- 🔴 ยังไม่ลง §7: **`GameMaster.dll` ติดถาวร ห้ามสั่ง rollback** (PANYA `1259` ข้อ 3) · **reaper ปิดเอง**: claim ผี >3 ชม. / `SUPERSEDED-BY:`/`DUPLICATE-OF:` (`1315`) · **ห้าม `rm -r`** (PANYA `1546`) · `ATTENDED:` บังคับ (READY ไม่มี = ไม่ขึ้นรถบัส) · `prompts/` ห้ามสายแก้ · grep ที่ห้า `reference_codex_attr/` · `.LANEK-FOLDED.txt` = พับแล้ว · **pin สายอื่นแดงตาม docstring = กลับ pin ในใบเดียวกัน** (`2241`) · grep กลไกไม่ใช่การสะกด · เพดานต่อใบ 8,192 B
- 🔴 **ตัววัด (`1259`)**: `*RESULTS*`/`OBSERVER_CONFIRMED` ไม่มี `.LANEK-FOLDED.txt` >6 ชม. = escalation K
- 🔴 **shared world** (`1057`/`1140`): โลกต่อฉากใน process แชร์ทุก session · A = registry · B เขียน combat state ลง registry ของ A · DB ไม่รับงานโลก · ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:`
- 🔴 **PANYA `0039` หลักถาวร: โลกใบเดียว + ฟิลเตอร์มองเห็น NPC ต่อผู้เล่น** · `Player.MobAppear` = **ธงต่อผู้เล่น ไม่ใช่ spawn** · **rank 0 = ธง · rank>0 = ลงโลกร่วม** · ส่งให้คนนี้ = (ไม่ผูกเควส ∧ `n_MOB_APPEAR=1`) ∨ เควสเข้า `s_QUEST_BEGIN/END` ∨ ธง true · **ออกแบบฟิลเตอร์ก่อนแตะ MobAppear** (A)
- 🔴 RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING:` (`1130`) · `KNOWN_RED_MAIN:` **ว่าง** · **สิทธิ์ฆ่า: ใบเซ็น > derive > ตาราง** ฉากใหม่ต้องมีใบเซ็นหรือ census

## บันไดไมล์สโตน (`20260904_0233` · ไม่มีกำหนดวัน · ผ่าน M(n) ก่อนประกาศ v(n))
- ✅ **M1/v1** ประกาศแล้ว (R249)
- ⏳ **M2 "ออกจากเมืองได้" ← อยู่ตรงนี้ · ทาง (ก) `1910`**: ตัวบล็อก = เฟรมตอบ `0x1FB2` trigger 2/3 (UI RE `2124` → **A** ต่อสาย → ใบ attended) · **เติมเฟรมอย่างเดียวไม่ปลดล็อก** — TIER 3 ต้องมี discriminator วัดจริงว่า "เกาะ ≠ น้ำเปล่า" (COO `0405` รับ A `0357`) · เกณฑ์ผ่าน: ใกล้เกาะ → "รายงานกัปตัน" → กด → วาปเข้า **เกาะ 2 และ 3 บนจอ** · ห้าม server ส่ง `EnterInstanceVital` เอง · ห้ามเช็คเลเวล
- **M3 = P-2** (ชั้นแรก+จอ ✅ GT-281 · ชั้นสอง สี = `GT-288` พร้อม) · **M4 "ตีได้ตายได้"**: มอนตีกลับ HP ลด · ตาย · ศพไม่ค้าง · เกิดใหม่ (B `GT-224`) · **M5** เก็บได้+รอด relog · **M final** ครบวงจร
- 🔴 **LANE-DB**: (1) กู้ `skill_points_null_audit` cherry-pick `f51b94e`+`849bf2a` (COO `0148`) → (2) แขน (ข) seam `1452` (`RE-280` `2258`) · `0328`: 1 ✅ · 2 = `RE-282` `2322` · 3 `0x309A` RE-blocked · `GT-272` ต้องมี `HEADLESS_PROOF:` · ใบสร้าง A/DB (R322B): ออก 126 คืน HP · BoatHealth ≠ -1
- **Q SCRIPT/QUEST** ลำดับระบบ (COO `1846`): 1 flag-quest-state → 2 inventory ฝั่งอ่าน → 3 `Player.MobAppear` = **A หลัง P-2** → 4 message-wire ✅ (`6775u1`) → **5 exp-level = งานถัดไป** · `CastSkill*` encoder = CS ทำเมื่อ Q ขอ
- **LANE-K**: รอบถัดไป = เกณฑ์ (ข) grep คอมมิตต่อใบ ก่อน archive · หมวด "ตกรถ" · ticket ใหญ่→`tickets/` ≤400 KB/PR

## งานด่วนตอนนี้
- **หาง P-1** (`0125`): ปิดด้วย `GT-223` · หนี้ `DropLedgerCell` ข้ามฉาก · ห้ามลบแถว ledger
- **P-2 สีชื่อ (= M3)**: ค่าจริงจาก `GT-288` เท่านั้น · สี = คู่ (คนดู, มอน) `NPCAttr+0x98` · GT สี = chief แต่ง → K · ห้าม faction-only/hardcode FontStyleID
- **LANE-GM**: `#970` ปิดไม่ merge → **กู้ใหม่บนฐานปัจจุบัน หนึ่ง PR** · P-3 `GT-279`: ปุ่มส่ง `0x51E9` จริง แต่ `capture_raw_gm_command` ไม่เขียนไฟล์ (RE-283 `0331`) · `RE-278` ส่ง mask ทั้งก้อน · `/warp <n>` = spawn · `GT-258` ตอบ K
- **M4 · LANE-B**: D2/D3/tripwire ลง PR แล้ว → **D1 คีย์ใหม่อ้าง COO `0405` (ถอนชื่อเก่าจาก FROZEN ได้ ห้ามเติมชื่อ)** → **1b R322B: `bg0002.HOSTILE_PLACEMENTS` 17 แถว vs roster rank-1 12 ตัว → regenerate จากกฎบน roster จริง** → 2 `2032` parser (ห้ามแตะ wire) → respawn 120 s → สมุดโลก · `apply_hp_damage` พักจน Door B · `GT-288` พลิก READY + `HEADLESS_PROOF:`
- **chief (`0405`)**: **(1) exemption `.LANEK-FOLDED.txt` ใน `check_new_filename_length()` ต้องลงก่อน `bridge-preflight` เป็น blocking** → (2) `gate-windows.yml` ไม่พิมพ์ชื่อเทสที่แดง (`1921`) → (3) §7 ≤30 KB + กฎ `2241`/`0039`/`0159`/`0316` + `.claude/` แตะโดยสายอื่น = แดง → (4) coverage `chat/server_system_message` notes+test_refs + ยาม legacy ปักที่ `make_show_message` แบบ rglob (Q `0322`) → (5) #948 seed (ข) + GT สี · ตอบ GM `1215`
- **LANE-A**: `#969` merged · TIER 3 รับแล้ว → เนื้อใบ RE `Bg3001.tgr` ให้ K ตั้งเลข + ต่อสายเฟรม `2124` → ใบ attended · `GT-151` ตอบ K · **ห้ามส่งเฟรมเดา**
- **LANE-UI**: `#961` กู้แล้วใน `#974` ✅ · `GT-262` ตอบ K → งาน 2 `2032` แถบ n/327 · express/community ยังห้าม · **CS**: `grant_learned_skill` ใต้แฟล็ก รอ DB caller · `GT-276`/`GT-274` · ห้ามปลดแฟล็ก 6 เฟรม

## ห้ามทำจนกว่า P-2 ปิด
- GT-146 + ใบเทสตีมอนทุกใบ · ยกเว้น `ATTACK-POSE-ONE-FIELD-AB-001` (`0904_2115`) + `GT-274` (`0645`)

## เมื่อไม่มีงานด่วน — ท่อ promotion (`2039` ข้อ 3)
- 5 ตัวแรก (`docs/PROMOTION_BACKLOG.md`): **1.** `remote_player_hypothesis` A · **2.** `lane_a_choose_npc_scene1` A · **3.** `ground_loot_hypothesis` B · **4.** `logout_dialog_open_hypothesis` UI · **5.** `skill_attr_hypothesis` CS · `item_operate_res` UI ปลดได้ · 9 แถว B **รอ P-2**
