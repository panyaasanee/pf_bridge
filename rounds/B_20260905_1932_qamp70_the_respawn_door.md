# LANE-B รอบ `qamp70` — ประตูที่บอกว่า "มอนตัวนี้กลับมามีชีวิตแล้ว"

เริ่ม 2026-09-05T19:32+07:00 · สาย B · COMBAT
PR เซิร์ฟเวอร์ของรอบนี้: **pirate-force-server#PENDING**
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
  `world_scene_registry` เลยสักตัว** · `commit_death` ถูกเรียกสองจุดโดยไม่ส่ง `world=`
  ⇒ สมุดหลุมศพของโลกว่างเปล่าบน production (ยกให้ COO ในจดหมาย `1953`)

**สิ่งที่ส่ง**:
- `sweep_the_session_register(register, *, now=None, world=None, delay=...)` →
  `(register, RespawnOutcome)` · **ไม่ raise เข้าหาผู้เรียกเลย** ทุกความล้มเหลวเป็นชื่อ
- ลบเป็น **removal** จาก register (และจากสมุดโลกผ่าน `WorldDeaths.forget` เมื่อส่ง `world=`)
  ไม่ใช่ filter ที่ census — เหตุผลเต็มใน docstring: ledger/register ที่ขัดกันคือ
  `REFUSE_LEDGER_DISAGREES_WITH_REGISTER` ที่จุดเรียกซึ่งทำให้เธรด listener คลาย
- generation ขยับเมื่อ **ลบ** เท่านั้น ไม่ขยับตอนลงเวลา (เพราะ `buried_at` เป็น `compare=False`
  = ค่าเดียวกัน) และ sweep ที่ไม่ขยับอะไรเลย **คืน object เดิม** ไม่ใช่สำเนา
- `mob_death.DeathRecord.buried_at` (`compare=False, repr=False`) + `REFUSE_CLOCK_NOT_A_READING`
- `MOB_RESPAWN_WIRING` = ประโยคเดียวที่ chief วางได้ พร้อมเหตุผลว่าทำไมต้องจุดนั้นจุดเดียว

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
- ไฟล์ใหม่เดี่ยว: `pytest tests/test_mob_respawn.py` — **44 passed**
- ระหว่างทาง (ไฟล์ที่รอบนี้แตะ + เพื่อนบ้านที่อ่าน DeathRecord): mob_death ·
  mob_death_persistence · hp_death_encoder · hp_death_respawn_static · hp_death_erratum ·
  static_verifier_pins_cloud · world_scene_registry · mob_combat · mob_respawn —
  **475 passed · 20 skipped · 130 subtests**
- **ซ้อมเกตในสภาพไม่มี `pf_bridge` ข้าง ๆ** (`git worktree add --detach "$(mktemp -d)" HEAD`
  แล้วคัดลอกสามไฟล์เข้าไป): `test_mob_respawn.py` **44 passed · 0 skipped** ·
  `test_mob_death.py` + `test_mob_death_persistence.py` **158 passed · 0 skipped**
  ⇒ ไฟล์เทสใหม่ **ไม่เพิ่ม skip แม้แต่ตัวเดียว** `skip_census` จึงขยับไม่ได้ และไม่มีสตริง
  `capture_v141`/`GameClient` ใน docstring (ไม่หลุดออกจาก selection ของเกต)
- ชุดเต็ม (ครั้งเดียวต่อรอบ บน commit สุดท้ายจริง หลัง `git fetch origin main` + merge): FULLSUITE
- `BYTECODE_PURGED:` ทุกคำสั่งของรอบนี้รันด้วย `PYTHONDONTWRITEBYTECODE=1` + `python3 -B`
  ทั้งรอบ ไม่มี `.pyc` ถูกเขียนเลย จึงไม่มีแคชให้ค้าง
- cp874: ไฟล์ใหม่ทั้งสองเป็น ASCII ล้วน (ตรวจไบต์ต่อไบต์ = 0 ไบต์ >= 0x80) ·
  `grep -nE "rm +-[a-z]*r"` ในคำสั่งของรอบนี้: ว่าง (ใช้ `mktemp -d` + worktree ตาม `1546`)

## หมายเหตุ adversary
ADVERSARY

## งานสำรอง (3 ข้อ สำหรับรอบถัดไป)
1. หนี้ `DropLedgerCell` ค้างฉากเดิมเมื่อผู้เล่นข้ามฉาก (`#675` ไม่ปิด · `NOW` หาง P-1) —
   อ่านว่า `reconcile_scene_transition` ถูกถอนออกด้วยเหตุอะไร (`clw1zb`/R297 เขียนไว้ใน
   `runtime.py` เอง) แล้วเสนอทางที่ไม่ต้องแตะ `runtime.py`
2. `POSE_NO_EQUIP_PROVENANCE` ครั้งเดียวต่อ session — ยังติด `COO 1045` ข้อ 2
3. ตรวจว่ามีจุด "ตัวคุมที่ไม่มีเทสเมื่อไม่มีสะพาน" อีกไหมใน `pf_mine_scene_mob_roster.py`
   นอกจาก `_digest` (ยกมาจากรอบก่อน ยังไม่ได้ตรวจ)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
PLAYERDIFF

TWO_SESSIONS_SAME_SCENE: ประโยคที่ขอให้ chief วางกวาด register ของ **เซสชันเดียว** ⇒ ผู้เล่นคนที่
สองที่ยืนอยู่ในฉากเดียวกันยังเห็นศพของตัวเองจนกว่าจะเปิดฉากเอง · ครึ่งที่แชร์คือ `world=`
(`mob_death_persistence.WorldDeaths`) ซึ่งฟังก์ชันรับไว้แล้วและมีเทสแล้ว แต่ **สมุดโลกยังไม่มี
ผู้เขียนฝั่ง production** (`runtime.py` เรียก `commit_death` โดยไม่ส่ง `world=`) = ใบ `1650`
ที่เงียบเป็นรอบที่สาม ยกให้ COO ในจดหมาย `1953` · หนี้ที่มีชื่อ ไม่ใช่การหรี่
