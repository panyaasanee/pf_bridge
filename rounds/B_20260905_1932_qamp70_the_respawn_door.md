# LANE-B รอบ `qamp70` — ประตูที่บอกว่า "มอนตัวนี้กลับมามีชีวิตแล้ว"

เริ่ม 2026-09-05T19:32+07:00 · สาย B · COMBAT
PR เซิร์ฟเวอร์ของรอบนี้: **pirate-force-server#848** (เปิดแล้ว ไม่ draft · marker
ยืนยันด้วย GET แล้ว · รอเกต)
claim PR: **pf_bridge#1366**

## รอบนี้ขยับ NOW ข้อไหน
- **ขยับ M4 ข้อ (4) "เกิดใหม่ได้"** ในบันไดไมล์สโตนของ `NOW.md` ซึ่งบันทึกไว้เองว่าเป็นศูนย์
  ("3 ก.ย. วัดแล้ว: census เข้าฉากใหม่ตัดตัวตายออก ไม่มี respawn") จากศูนย์เป็น
  "ประตูมีจริง มีเทส มีหลักฐาน headless ว่าฉากเติมกลับ เหลือหนึ่งประโยคใน `runtime.py`"
- **ทำไมไม่ขยับข้ออื่น**: รายการ LANE-B ที่เหลือใน `NOW.md` (แก้ 18:47) ติดของคนอื่นทั้งหมด —
  M4 (1) `apply_hp_damage` พัก รอ Door B (`2050` อนุมัติ) · สัญญาสามเฟรม 34 พิน = chief
  ทำเอง (`1752` ข้อ 2 · `1845` เลื่อนเป็นงานแรก 21:21) สายนี้ไม่แย้งไปแล้วรอบ `x5bkvl` ·
  P-2 สีชื่อ = ใบ RE ของ LANE-GM · ฉาก 3 สองรู ปิดแล้วด้วย `#839` บน main
- **ไม่แตะ `NOW.md`** (ผู้เขียนคือ Panya กับ COO) ข้อเสนอไปทางจดหมาย `ADDRESSEE: COO` ตามกติกา

## ล็อกรอบ
- ต้นรอบ list `[LANE-B]` open ทั้งสองรีโป: pf_bridge **ไม่มี** · pirate-force-server **ไม่มี**
  (มีแต่ `[LANE-A] #1365` · `[LANE-GM] #1364` · courier `#1336` ซึ่งไม่ใช่ล็อกของสายนี้ ห้ามแตะ)
- claim = `pf_bridge#1366` branch `claude/youthful-ride-qamp70` ไม่ draft **ไม่มี marker
  ตั้งแต่เปิด** (เติมตอนจบรอบ = ปลดล็อก) · list ซ้ำหลังเปิด: ไม่มี `[LANE-B]` ใบอื่น ไม่แพ้ใคร

## ชะตา PR รอบก่อนของสายนี้ (ADDENDUM ข้อ A)
- `pirate-force-server#842` (`x5bkvl`) **merged=true** 2026-09-05T11:57Z (18:57+07) — งานอยู่บน
  main แล้ว ไม่มีอะไรให้กู้
- `pf_bridge` claim ของ `x5bkvl` ปิดแล้วเช่นกัน ไม่มีกิ่งค้าง

## กล่องจดหมาย (ADDENDUM ข้อ B)
- ใบที่จ่าหน้าถึง `LANE-B` และยังไม่มี stub: **ไม่มี** · `1813` (chief) บริโภคแล้วรอบ `x5bkvl`
- `1752` (COO · owner สัญญาสามเฟรม = สายนี้) ตอบไปแล้วรอบ `x5bkvl` = ไม่แย้ง ภายในหน้าต่างที่ให้
- `1830` (chief ถึง COO cc สายนี้) COO ตัดสินเป็น `1752` แล้ว ไม่มีอะไรค้างสายนี้
- ใบที่สายนี้เปิดและยังไม่มีคำตอบ: `1349` `1350` (ร่าง RE/GT ของ empty floor) · `1638` (ร่าง RE
  สองเฟรมขัดกันเรื่องพื้น) · `1650` (CORE-REQUEST ผู้เขียนสมุดโลก) — **`1650` เงียบเป็นรอบที่สาม
  ไม่ยื่นซ้ำอีก** ยกไปให้ COO จัดลำดับในจดหมาย `1953` แทน

## 1. งานหลักของรอบ — ประตู respawn
`src/pirateforce_foundation/mob_respawn.py` (ใหม่) · `production_allowed = True` · ไม่มีแฟล็ก

**สิ่งที่วัดก่อนเขียน** (ไม่ใช่สิ่งที่เดา):
- `mob_death_persistence.py` เขียนไว้เองว่า "a dead monster is dead until something respawns
  it, and NOTHING IN THIS TREE RESPAWNS ONE TODAY ... `WorldDeaths.forget` exists
  unused-by-production and named, waiting for the respawn round that will be its only caller"
- `runtime.py:_sync_combat_scene_state` เปิด ledger ใหม่ที่ HP เต็มจากตาราง แล้วใส่ศูนย์
  ทีละแถวตาม `self.mob_death_register` และ **ไม่มีอะไรในทรีนี้เคยเอาแถวออกจาก register นั้น**
  ⇒ ฆ่ามอน 12 ตัวในฉาก 3 = ฉาก 3 ว่างจนกว่าจะรีสตาร์ตโปรเซส
- `grep runtime.py`: **ไม่ import `mob_death_persistence` / `mob_ground_persistence` /
  `world_scene_registry` เลยสักตัว** ⇒ สิ่งที่ขาดคือ **ผู้อ่าน** (`DEATH_SEED_WIRING`)
  (ยกให้ COO ในจดหมาย `1953`)
  🔴 **สายนี้เขียนผิดในร่างแรกและถอนแล้วในรอบเดียวกัน**: ร่างแรกอ้างว่า "สมุดโลกว่างเปล่า
  เพราะ `commit_death` ไม่ส่ง `world=`" — เท็จ `commit_death` เรียก `remember_death(...)`
  ทุกครั้ง และ `remember_death` แปลง `world=None` เป็น singleton ⇒ **ทุกการฆ่าถูกฝังลง
  สมุดโลกอยู่แล้ว** (pf-adversary D2) · ผลคือค่าปริยายของ `world=` เปลี่ยนเป็นสมุดโลกจริง

**สิ่งที่ส่ง**:
- `sweep_the_session_register(register, *, now=None, world=THE_PROCESS_BOOK, delay=...)` →
  `(register, RespawnOutcome)` · **ไม่ raise เข้าหาผู้เรียกเลย** ทุกความล้มเหลวเป็นชื่อ
- ลบเป็น **removal** จาก register **และจากสมุดหลุมศพของโลกพร้อมกันโดยค่าปริยาย**
  (`WorldDeaths.forget`) ไม่ใช่ filter ที่ census — เหตุผลเต็มใน docstring: ledger/register
  ที่ขัดกันคือ `REFUSE_LEDGER_DISAGREES_WITH_REGISTER` ที่จุดเรียกซึ่งทำให้เธรด listener คลาย
- generation ขยับเมื่อ **ลบ** เท่านั้น ไม่ขยับตอนลงเวลา (เพราะ `buried_at` เป็น `compare=False`
  = ค่าเดียวกัน) และ sweep ที่ไม่ขยับอะไรเลย **คืน object เดิม** ไม่ใช่สำเนา
- `mob_death.DeathRecord.buried_at` (`compare=False, repr=False`) + `REFUSE_CLOCK_NOT_A_READING`
- `MOB_RESPAWN_WIRING` = ประโยคเดียวที่ chief วางได้ พร้อมเหตุผลว่าทำไมต้องจุดนั้นจุดเดียว

**สิ่งที่ pf-adversary จับได้และแก้ในรอบนี้ทั้งหมด (12 ข้อ)** — ดูหัวข้อ adversary ข้างล่าง

**ข้อจำกัดที่ยอมรับ ไม่ใช่ซ่อน**: `mob_death.py` ห้าม import `time` (เทสของมันเองปักไว้
ข้าง `socket`/`random`) ⇒ `kill()` ปล่อยหลุมศพไว้ไม่มีเวลา และ sweep ลงเวลาให้ครั้งแรกที่เห็น
⇒ นาฬิกาเริ่มที่ขอบฉากแรกหลังฆ่า ช้ากว่าเวลาตายจริงอย่างมากหนึ่งขอบฉาก ไม่มีทางเร็วกว่า
· ค่า 120.0 วินาที = `[ASSUMPTION OF LANE B - AWAITING COO]` (เท่ากับ `DROP_LIFETIME_SECONDS`)

## 2. จดหมายของรอบ
- `notes_to_chief/20260905_1952_LANE-B-CORE-REQUEST-one-statement-respawns-a-monster-at-a-scene-open.md`
- `notes_to_chief/20260905_1953_LANE-B-ASK-COO-respawn-delay-and-three-world-books-with-no-production-reader.md`

## 3. ทำไมไม่มีใบ GT ในรอบนี้
`NOW.md` หัวข้อ "ห้ามทำจนกว่า P-2 จะปิด": **ใบเทสตีมอนทุกใบห้ามออก** และการวัด respawn บนจอ
ต้องฆ่ามอนก่อน ⇒ ออกใบ GT ตอนนี้คือขัดคำสั่งตรง ๆ · หลักฐานชั้น wire/headless อยู่ใน
`SceneOpenProofTests` แล้ว · ใบ GT จะขอเลขจาก chief ทันทีที่ P-2 ปิด ตามกติกา `2142`
(ไม่ใช่ `NO_FEATURE_WAITING` เพราะไม่มี RE ปิดใหม่ที่รอบนี้บริโภค — กติกา `1130` ไม่เข้าเงื่อนไข)

## เทส
- ไฟล์ใหม่เดี่ยว: `pytest tests/test_mob_respawn.py` — **59 passed** (44 ก่อน adversary)
- ระหว่างทาง (ไฟล์ที่รอบนี้แตะ + เพื่อนบ้านที่อ่าน DeathRecord): mob_death ·
  mob_death_persistence · hp_death_encoder · hp_death_respawn_static · hp_death_erratum ·
  static_verifier_pins_cloud · world_scene_registry · mob_combat · mob_respawn —
  **475 passed · 20 skipped · 130 subtests**
- **ซ้อมเกตในสภาพไม่มี `pf_bridge` ข้าง ๆ** (`git worktree add --detach "$(mktemp -d)" HEAD`
  แล้วคัดลอกไฟล์เข้าไป): `test_mob_respawn.py` **44 passed · 0 skipped** (วัดก่อน adversary) ·
  `test_mob_death.py` + `test_mob_death_persistence.py` **158 passed · 0 skipped**
  ⇒ ไฟล์เทสใหม่ **ไม่เพิ่ม skip แม้แต่ตัวเดียว** `skip_census` จึงขยับไม่ได้ และไม่มีสตริง
  `capture_v141`/`GameClient` ใน docstring (ไม่หลุดออกจาก selection ของเกต)
- ชุดเต็ม (ครั้งเดียวต่อรอบ บน commit สุดท้ายจริง `b18b493` หลัง `git fetch origin main` +
  merge `f12a904` เข้าต้นไม้แล้ว = **หลัง**แก้ตามผล adversary ครบ):
  **11279 passed · 327 skipped · 20985 subtests passed · 0 failed** (589 วินาที)
  — ไม่มีตัวแดงเลย · `KNOWN_RED_MAIN:` **ไม่มี**
- `BYTECODE_PURGED:` ทุกคำสั่งของรอบนี้รันด้วย `PYTHONDONTWRITEBYTECODE=1` + `python3 -B`
  ทั้งรอบ ไม่มี `.pyc` ถูกเขียนเลย จึงไม่มีแคชให้ค้าง
- cp874: ไฟล์ใหม่ทั้งสองเป็น ASCII ล้วน (ตรวจไบต์ต่อไบต์ = 0 ไบต์ >= 0x80) ·
  `grep -nE "rm +-[a-z]*r"` ในคำสั่งของรอบนี้: ว่าง (ใช้ `mktemp -d` + worktree ตาม `1546`)

## เกต (PANYA-DECISION `20260904_1158` §22)
**`GATE_UNVERIFIED #848`** — เปิด PR 20:30+07 · รอผล job `gate` ของ run `pull_request`
บน sha `b18b493` เต็ม 10 นาทีตามกติกา (ตรวจทุก 30 วินาที) · ทั้งสอง run ยังเป็น
`in_progress` ไม่มี conclusion ⇒ **ยังไม่ตัดสิน ไม่ใช่แดง** · ปล่อยล็อกตามลำดับจบรอบ
🔴 **รอบถัดไปของสาย B เปิดด้วยการตรวจ `#848` ก่อนทำอย่างอื่น** (แดง = แก้ใต้รหัสรอบเดิม ·
merged = ไปต่อ · closed ไม่ merge = `git fetch` กิ่ง `claude/sharp-newton-qamp70` แล้ว
cherry-pick `b18b493` ตาม ADDENDUM ข้อ A)
· ไม่ push commit เปล่า "wake gate" เพราะ run เกิดเองจาก event เปิด PR แล้วทั้งสองอัน

## หมายเหตุ adversary
สั่ง `pf-adversary` หนึ่งครั้ง (จากสองครั้งที่กติกา `1428` ให้) บนสภาพก่อน commit
**เจอ 12 ข้อ จ่ายครบทุกข้อในรอบนี้** ไม่มีข้อไหนถูกยกไป `ADVERSARY_PENDING`

สองข้อที่ไม่ใช่บั๊ก แต่เป็น **คำอ้างเท็จของสายนี้เอง** — บันทึกไว้เพราะสำคัญกว่าบั๊ก:
- **D2** docstring อ้างว่าสมุดหลุมศพของโลกไม่มีผู้เขียนฝั่ง production · เท็จ ·
  `commit_death` → `remember_death(step.record, world=world)` ทุกครั้ง และ `remember_death`
  แปลง `world=None` เป็น singleton `world_deaths()` ⇒ ทุกการฆ่าถูกฝังอยู่แล้ว
  **ถ้าปล่อยไว้**: sweep จะเปิดหลุมศพในเซสชันแต่ทิ้งไว้บนสมุดโลก = สองสมุดขัดกัน และวันที่
  `DEATH_SEED_WIRING` ลง seed จะดึงกลับมาพร้อม `buried_at=None` ทุกครั้ง = **respawn เป็นศูนย์
  ถาวรและเงียบ** · แก้: `world=` ค่าปริยาย = สมุดโลกจริง (`THE_PROCESS_BOOK`)
- **D5** ใบสั่งบอก chief ให้วาง `print(console_safe(line))` · `runtime.py` ไม่มีชื่อเปล่านั้น
  (มีแต่ `lane_hooks.console_safe`) ⇒ วางตามจะเป็น `NameError` ในสาขาที่ถูก catch = เงียบสนิท
  ทรงเดียวกับเกตตาย 3 วันของ `a7k5gy` · แก้ + เทสอ่าน `runtime.py` จริงทุกชื่อที่ใบสั่งใช้

ข้ออื่นที่จ่ายแล้ว: **D1** ลืมลงทะเบียนโมดูลใหม่ใน `LANE_B_MODULES` (เทส fabrication guard แดง) ·
**D3** ฟิลด์ `mob_death_register` ต้องประกาศในบล็อก atomic เท่านั้น ไม่ใช่เหนือจุด raise ของ
`open_register` (ไม่งั้นเซสชันค้าง `ledger_disagrees_with_register`) · **D4** สมุดโลกที่ raise
= ผลบางส่วนที่นับได้ ไม่ใช่ refusal และไม่ทิ้งหลุมศพที่เหลือ (`break`→`continue`) ·
**D7** โทเคน `alive_again` เป็น delta ที่สวมชื่อเป้าหมาย → `removed_from_the_death_register` ·
**D8** sweep ที่ลงเวลาอย่างเดียวต้องพิมพ์ ไม่ใช่เงียบ · **D9** "ตารางเวลาเดียวกัน" → "ระยะเวลา
เท่ากัน คนละจุดเริ่ม" · **D10** เทสสองตัวที่ล้มไม่ได้ (substring import check, `is not None`)
เปลี่ยนเป็น AST และเป็นการเทียบไบต์กับเซสชันที่ไม่เคยฆ่าอะไร พร้อมตัวคุมด้านลบ ·
**D11** `describe_sweep` ที่ได้ชนิดผิดตอบเป็นชื่อ ไม่ใช่ความเงียบ · **D12** บรรทัด
`TWO_SESSIONS_SAME_SCENE:` (อยู่ท้ายไฟล์นี้และในหัว PR)

**มิวแทนต์ที่รอดชุดเทสเดิม 2 ตัว ตายแล้วทั้งคู่** (รันซ้ำยืนยันในรอบนี้):
`keep.append` ในสาขา clock-went-backwards ถูกลบ → 1 แดง · `continue`→`break` ในลูปสมุดโลก
→ 1 แดง · เพิ่มมิวแทนต์ที่สาม (ค่าปริยาย `world=` ไม่ถึงสมุดโลก) → 1 แดง

## งานสำรอง (3 ข้อ สำหรับรอบถัดไป)
1. หนี้ `DropLedgerCell` ค้างฉากเดิมเมื่อผู้เล่นข้ามฉาก (`#675` ไม่ปิด · `NOW` หาง P-1) —
   อ่านว่า `reconcile_scene_transition` ถูกถอนออกด้วยเหตุอะไร (`clw1zb`/R297 เขียนไว้ใน
   `runtime.py` เอง) แล้วเสนอทางที่ไม่ต้องแตะ `runtime.py`
2. `POSE_NO_EQUIP_PROVENANCE` ครั้งเดียวต่อ session — ยังติด `COO 1045` ข้อ 2
3. ตรวจว่ามีจุด "ตัวคุมที่ไม่มีเทสเมื่อไม่มีสะพาน" อีกไหมใน `pf_mine_scene_mob_roster.py`
   นอกจาก `_digest` (ยกมาจากรอบก่อน ยังไม่ได้ตรวจ)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
**วันนี้ยังไม่เห็น และรอบนี้พูดตรง ๆ แทนที่จะเลี่ยง** — สิ่งที่ลงคือประตูกับหลักฐาน
บรรทัดที่เหลืออยู่ใน `runtime.py` ซึ่งเป็นไฟล์ของ chief และ PR นี้แนบใบสั่งไปด้วยแล้ว

ทันทีที่ใบสั่งนั้นถูกวาง: **ฆ่ามอนในฉาก 3 เดินออกไปฉาก 4 กลับมาหลัง 120 วินาที — มอนยืนอยู่
ที่เลือดเต็ม** แทนที่จะเป็นศพจนกว่าจะรีสตาร์ตโปรเซสเซิร์ฟเวอร์ นั่นคือ M4 ข้อ (4) ซึ่ง
`NOW.md` บันทึกวันนี้ว่าเป็นศูนย์ที่วัดแล้ว

TWO_SESSIONS_SAME_SCENE: ครึ่งเซสชันของ sweep เป็นของเซสชันเดียว ⇒ ผู้เล่นคนที่สองที่ยืนอยู่ใน
ฉากเดียวกันยังเห็นศพของตัวเองจนกว่าจะเปิดฉากเอง · **สมุดหลุมศพของโลกถูกเปิดให้ทุกคนด้วยการ
เรียกเดียวกัน** (ค่าปริยาย `world=` หลังแก้ D2) · ส่วนที่ยังต่างกันเป็นหนี้ของ **ผู้อ่านที่ยัง
ไม่มี** (`mob_death_persistence.DEATH_SEED_WIRING` ยังไม่ถูกวางใน `runtime.py`) ยกให้ COO
จัดลำดับในจดหมาย `1953` · หนี้ที่มีชื่อ ไม่ใช่การหรี่
