[ถึง: chief สาย E · COO · สาย A/B/GM · cc Panya | จาก: ผู้ช่วยเซสชัน attended "กะ3-A" (บัญชี [กะ3]) | 2026-08-29T00:18+07:00]

# ผลรอบ attended รวม 3 ใบในบูตเดียว — GT-122 **PASS** · GT-102 **PARTIAL (ผ่านพร้อม finding ผู้พูดผิดตัว)** · GT-104 **NO-RESULT/BLOCKED-BY-FINDING** + เปิด finding ใหม่ 2 เรื่อง

`OBSERVER_CONFIRMED: 2026-08-29T00:17+07:00` (เวลาประมาณ — Panya ยืนยันรายการสังเกตทั้ง 6 ข้อในแชท และขยายข้อ 3 เรื่องเสียงพูด)

## T0 — เงื่อนไขรอบ
- **BOOT_COMMIT `3baf65de0319c8905afd7f426d599f12f2e7e664`** = origin/main HEAD · code delta 0 · ci decision success
- flagless แท้ (SERVER_CMDLINE พิสูจน์แล้วใน job log — ไม่มี `--*-scenario`/`--export-events`/`--second-password-mode`/`--world-census-actors`)
- jobs: `1327` hold+resolve · `1328` boot (วิดีโอ 30fps ต่อเนื่อง 905.8 s, frame proof 3/3) · `1329` teardown (เจ้าของกดผ่าน `STOP_ROUND_AND_VIDEO.bat` 00:01) · `1330` release
- run DB `run_gt122_20260828_234621` · backup `backup\pirateforce_before_GT-122_20260828_234621.sqlite3`
- canonical sha `4FF37060…8454` **ตรงทั้งก่อนและหลัง** · teardown: listeners 0 · clients 0 · ffmpeg 0 · integrity ok · fk 0 · sessions selected 12 · max_lease 13 ไม่ถอยหลัง
- 🔴 **การรวม 3 ใบเข้าบูตเดียว + การแก้ grep ด่าน 2 ของ GT-122 เป็นคำเคาะสดของเจ้าของ** (2026-08-28 ~23:0x และ ~23:5x) — รายละเอียดใน LOCK history และท้ายใบนี้ข้อ ⑥

## ① GT-122 — **PASS ทั้งสองชั้น** (สถานะที่ควรกรอก: `PASS`)

**wire (ถอดจาก hexdump `FOUNDATION_SELECTED_START_GAME` 436 bytes ใน capture — payload 423 bytes):**
- `BasicAttr` mask = `0x10010001` ⇒ **บิต `0x0001` SET** · ตามด้วย wstring `Arena01` (UTF-16LE ที่ payload offset 56) ✅
- `ActorAttr` mask = **`0x0000000000000801` เป๊ะ** ✅ · pattern ของ mask เก่า `0x01000801` = **0 hit** ✅
- ไล่ u64 mask ทุกตัวในเฟรม (13 ตัว): **ไม่มีตัวไหนมีบิต `0x01000000`** ✅ (absent ไม่ใช่ present-and-zero)
- ความยาวเฟรม 436 bytes — บันทึกเป็น baseline รอบนี้ (ไม่มี capture ก่อนแก้ให้เทียบ)

**client-observable (ตา Panya + ภาพ full-res 234821/234839):**
- ป้ายชื่อเหนือหัว = `Arena01` **สีขาว** ชื่อล้วน ไม่มี guild artifact ใด ๆ · HUD = Arena01 · HP 100/100 · Lv.1
- หน้าต่าง `CHARACTER`: ช่องชื่อ = `Arena01` · **ไม่มีช่องกิลด์อยู่เลยทั้งหน้าต่าง** (แข็งกว่า "มีแต่ว่าง")
- dropdown ใต้ชื่อคือช่อง**ฉายา** อ่านว่า **"ยังไม่ได้เลือกฉายา"** — คือ GREATTITLE (probe x14) ไม่ใช่ช่องกิลด์
  🔴 ผู้ช่วยเคยอ่านผิดเป็น "ไม่ได้เลือกกลาน/แคลน" — เจ้าของแก้ให้แล้ว บันทึกตัวสะกดที่ถูกไว้ที่นี่
- NO-CRASH sweep ×2 ผ่าน
- สีป้าย: ป้ายตัวเอง = ขาว · ป้ายอื่นในเฟรม = none

⇒ P1 ✅ P2 ✅ · CORE-REQUEST-027 ทำสิ่งที่อ้างจริงบนจอและบนสาย

## ② GT-102 — **PARTIAL: กลไกยิงจริง หน้าต่างเปิดจริง แต่ "ผู้พูด" เป็นคนละตัวกับ NPC ที่คลิก** (เสนอสถานะ: `PASS-WITH-FINDING` หรือ `PARTIAL` — chief เคาะ)

**wire:** คลิก Columbus (P1) แล้วคอนโซลยิงตามลำดับ: `TargetVital` → `V98_NPC_FACE_PLAYER_POSITION_HEADING_P1` (10,610 bytes) → `V98_NPC_CONVERSATION_DEFAULT_P1` → **`CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` (54 bytes)** ✅ — เส้น CORE-REQUEST-014 ทำงานจริง ยิงครั้งเดียวตามชื่อ

**client-observable (ตา Panya · ภาพ 234958):**
- แผงเป้าเปิด: `Columbus HP 100 LV.1` · Columbus มีลูกศรเหลือง + วงแหวนเหลือง
- **หน้าต่าง QUEST เปิดจริง มีสองออปชัน:** `มุ่งหน้าไป Atlantic Ocean: Rising Sun Sea` · `ตั้งฐานทัพที่ Port Royal`
- 🔴 **finding 1: ป้ายผู้พูดในหน้าต่าง = "Sebastian"** และเนื้อบทขึ้นต้น "Prison Exile Island ข้าคือผู้…" — ทั้งที่คลิก Columbus
- 🔴 **finding 2 (เจ้าของขยายตอนยืนยัน): มีเสียงพากย์ NPC ดังขึ้นตอนหน้าต่างเปิด และเป็นเสียงของ Sebastian (ตัวที่อยู่เกาะคุก) ไม่ใช่เสียง Columbus** — เจ้าของจำเสียงจากเซิร์ฟเวอร์ต้นฉบับได้
  ⇒ เสียง+ป้าย+เนื้อบทชี้ทางเดียวกัน: **เนื้อ conversation ที่ client เล่นคือชุดของ Sebastian** [สมมติฐานกลไก — ไม่ยืนยัน]: สอดคล้องกับที่คอนโซลบิลด์นี้พิมพ์เองว่า ChooseNPC path ส่ง "one **q3020** NPCConversation descriptor" — ว่า descriptor ที่ไปถึงจอเป็น q3020 (Sebastian) ไม่ใช่ q3021 หรือไม่ **ต้องเปิดใบถอดไบต์เฟรม 54 bytes นั้นตรง ๆ** ห้ามสรุปจากใบนี้
- ออปชันที่ 1 ตรงกับปลายทางที่ `REAL_SERVER_DIVERGENCE`/ใบ M2 เดิมชี้ (ฉาก 126 Rising Sun Sea) — เกี่ยวกับ M2 โดยตรง
- 🔴 divergence สี: **ชื่อ NPC ทุกตัวเป็นสีเขียว** (ต้นฉบับ = เหลือง เช่นภาพ REF deer herd orange names) — จดสีอย่างเดียว ไม่อนุมานสาเหตุ (`RE-067` เปิดอยู่) → ควรลง `REAL_SERVER_DIVERGENCE.tsv` (เขต chief)

## ③ GT-104 — **NO-RESULT / BLOCKED-BY-FINDING** (ไม่มี attack เกิดขึ้นเลยแม้แต่ครั้งเดียว)

- มอน field render จริงตรงพิกัด roster: เจ้าของเจอ **P33 Fighting Fish soldier** และ **P58 Jungle Big Tiger** (พิกัด HUD ในภาพตรงตาราง `HOSTILE_PLACEMENTS` ทั้งคู่) · `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13 missing=none` ในบูตเดียวกัน ⇒ **สำมะโน/override ไม่ใช่ครึ่งที่พัง**
- 🔴 **แต่คลิกซ้ายบนมอนถูกเซิร์ฟเวอร์ตอบด้วยเลนคุย NPC**: ทั้ง P33 และ P58 ได้ `V98_NPC_FACE_PLAYER_POSITION_HEADING_P<n>` + `V98_NPC_CONVERSATION_DEFAULT_P<n>` → จอเปิด**หน้าต่าง QUEST เปล่า** (หัวเป็นชื่อมอน เนื้อว่าง — ภาพ 235212/235955) → ไม่มีทางเข้าโหมดโจมตี
- ผู้ช่วยตรวจ log ทั้งไฟล์: **ไม่มีเฟรม attack/damage/death เกิดขึ้นเลย** — NO-RESULT สะอาด ไม่ใช่ผลลบของ widening
- ⇒ **ใบนี้และทุกใบคอมแบต (GT-129, GT-084-R2 ฯลฯ) ถูกบล็อกโดย finding ใหม่ข้อ ④.1 จนกว่าจะแก้**

## ④ ขอเปิด finding/ใบใหม่ 2 เรื่อง (chief เป็นคนตั้งเลขใบ)

**④.1 MOBS-ANSWER-AS-NPC (บล็อกทุกใบคอมแบต — สำคัญสุดของรอบ):**
คลิกบน hostile roster placement ถูก route เข้าเลน NPC conversation (`V98_NPC_*`) แทนเลนต่อสู้
วัดจากจอ+log บนบูต flagless commit `3baf65de` · เห็นบน P33 และ P58 (2/2 ที่ลอง) · census ฝั่งส่งพิสูจน์แล้วว่าดี
คำถามที่ใบใหม่ต้องตอบ: ตัวแยก mob/NPC ฝั่ง server dispatch (ChooseNPC handler?) แยกด้วยอะไร และทำไม roster identity ไม่ถูกแยกออกจาก NPC list
[หมายเหตุผู้ช่วย ไม่ใช่ข้อสรุป: เซิร์ฟเวอร์ต้นฉบับใช้ "ดับเบิลคลิก = โจมตี" — รอบนี้เจ้าของยังไม่ทันได้ดับเบิลคลิกเพราะ single click เปิดหน้าต่าง QUEST ทับเสียก่อน]

**④.2 NAME-LABELS-VANISH-AFTER-MOVE (เจ้าของเห็นเอง · ยืนยันแล้ว):**
หลังเดินออกจากบริเวณแรก **ป้ายชื่อสีเขียวของทุกตัวในแมพหายหมด** เหลือแต่ป้ายฟ้า (title) · ตัวที่มีแต่ป้ายฟ้าอยู่แล้ว = ป้ายหายทั้งใบ (ภาพ 235212: Fighting Fish soldier เหลือ title ฟ้าลอยเดี่ยว · Loie เหลือ "Royal Navy Engineer" ฟ้า ไม่มีชื่อเขียว)
[สมมติฐานกลไก — ห้ามใช้เป็นฐานใบอื่นจนกว่าจะวัด]: ทุกคลิกยิง refresh 10,610-byte และคอนโซลบิลด์นี้เขียนเองว่า "retained actors are **NPCAttr-only** and entrants use authentic full-mask MovementAttr" ⇒ อ่านคู่ `RE-130` (reconcile แทนด้วย omission) — ตัว retained ไม่ได้รับ BasicAttr (ที่ถือชื่อ) ซ้ำ จึงเสียชื่อไปในรอบ reconcile · ต้องเปิดใบ static/wire วัดตรง

## ⑤ หลักฐาน
- วิดีโอต่อเนื่อง 905.8 s (frame proof 3/3) — ห้ามลบจากสะพาน · ภาพเจ้าของ: `GameClient\Data\ScreenShot\20260828_234821 / 234839 / 234958 / 235212 / 235955.png`
- capture root `GameClient\capture_gt122_20260828_234621\` (console out/err + capture_v141) · job logs `outbox\1327/1328/1329_*`

## ⑥ nonclaims
- ไม่อ้างว่าเนื้อ conversation บนจอคือ quest 3021 — ป้าย/เสียง/เนื้อชี้ว่าเป็นชุด Sebastian; การชี้ขาดต้องถอดเฟรม 54B
- ไม่อ้างสาเหตุสีเขียวของชื่อ NPC (`RE-067` เปิดอยู่) · ไม่อ้างกลไกป้ายหาย (④.2 เป็นสมมติฐานติดป้ายแล้ว)
- ไม่อ้างว่า widening ของ mob_death ผิดหรือถูก — มันไม่เคยถูกถึงตัวเพราะคลิกถูกดักที่เลน NPC ก่อน
- ผลลบ/บล็อกของ GT-104 วัดจาก 2 ใน 12 identity เท่านั้น (P33, P58) — ไม่ generalize เกินนั้น แม้อาการจะชี้ทางเดียว
- การรวม 3 ใบเข้าบูตเดียว และการแทน grep g3 ที่ stale ด้วย 2 greps ที่แน่นกว่า เป็น**คำเคาะเจ้าของ** ไม่ใช่ดุลยพินิจผู้เทส — ขอ chief แก้ถ้อยคำ ด่าน 2 ของใบ GT-122 ในคิวให้ตรงโค้ดจริง (`make_actor_attr_with_name_and_class` ใน legacy_bridge.py · `return _make_...` ใน player_wire.py)
- ไม่แตะ src/ ไม่ commit ไม่แก้คิว/ledger — ใบนี้คือการส่งผล chief เป็นผู้ประมวล

— กะ3-A
