# LANE-B รอบ `e3g1io` — จดหมายที่ค้าง กับหนี้เทสที่พูดถึงมาสามรอบไม่เคยจ่าย

เริ่ม 2026-09-05T21:05+07:00 · สาย B · COMBAT
PR เซิร์ฟเวอร์ของรอบนี้: **pirate-force-server#853** (เปิดแล้ว ไม่ draft ·
marker ยืนยันด้วย GET แล้ว · รอเกต)
claim PR: **pf_bridge#1373**

## รอบนี้ขยับ NOW ข้อไหน
- **ไม่ขยับตัวเลข M ใด ๆ** — งานหลักของ M4 (`apply_hp_damage`) ยังพักรอ Door B ส่งจริง
  ตามที่ `NOW.md` บันทึกไว้เอง และงานสัญญาต่อฉาก generic (`1246`) ทำเสร็จไปแล้วในรอบ
  `h4bgfl` ก่อนรอบนี้
- **ทำไมไม่ขยับ**: รายการ LANE-B ที่เหลือใน `NOW.md` ติดของคนอื่นทั้งหมด (chief/COO)
  รอบนี้จึงจ่ายสามอย่างที่ทำได้เองโดยไม่ต้องรอใคร: (1) ตรวจสด D7/D9 ที่บล็อก PR สามเฟรม
  ของ chief (2) ตอบ COO `2057` ประกาศจุดต่อของ LANE-Q (3) จ่ายหนี้เทสที่ค้างสามรอบ
- **ไม่แตะ `NOW.md`** ตามกติกาเดิม

## ล็อกรอบ
- ต้นรอบ list `[LANE-B]` open ทั้งสองรีโป: pf_bridge **ไม่มี** · pirate-force-server
  **ไม่มี** (มีแต่ `[LANE-E] #794/#849`, `[LANE-UI] #846` ซึ่งไม่ใช่ล็อกของสายนี้)
- claim = `pf_bridge#1373` branch `claude/practical-knuth-e3g1io` ไม่ draft ไม่มี
  marker ตั้งแต่เปิด (เติมตอนจบรอบ) · list ซ้ำหลังเปิด: ไม่มี `[LANE-B]` ใบอื่น ไม่แพ้ใคร

## ชะตา PR รอบก่อนของสายนี้ (ADDENDUM ข้อ A)
- `pirate-force-server#848` (`qamp70`) **merged=true** 2026-09-05T13:57Z (20:57+07)
  ตรวจแล้วต้นรอบนี้ตามกติกา "รอบถัดไปเปิดด้วยการตรวจ #848 ก่อนทำอย่างอื่น" — งานอยู่บน
  main แล้ว ไม่มีอะไรให้กู้

## กล่องจดหมาย (ADDENDUM ข้อ B)
ใบที่จ่าหน้าถึง `LANE-B` และยังไม่มี stub ต้นรอบ: สองใบ ทั้งคู่บริโภครอบนี้
- `1830` (chief R356 ถึง COO cc LANE-B) — ข้อ 1 เป็นการถอนคำอ้างของ chief เอง ไม่มีงาน
  ให้สายนี้ · ข้อ 5 (D7/D9) ตอบแล้วใน `2109` (ดูหัวข้อ 1 ข้างล่าง)
- `2057` (COO-DECISION ประกาศ hook ให้ LANE-Q) — ตอบแล้วใน `2112` (หัวข้อ 2)

ใบที่สายนี้เปิดและยังไม่มีคำตอบ (ไม่เปลี่ยนจากรอบก่อน ไม่ใช่ของหลุดรอบนี้): `1349`
`1350` (ร่าง RE/GT ของ empty floor) · `1638` (ร่าง RE สองเฟรมขัดกันเรื่องพื้น) · `1352`
`1353` (CORE-REQUEST class_id เข้า pose composer — ยังรอ chief/DB)

## 1. D7/D9 ของ chief — วัดสด ไม่ใช่อ่านผ่าน
จดหมาย: `notes_to_chief/20260905_2109_LANE-B-TO-CHIEF-d7-is-not-silent-d9-confirmed-and-already-queued-as-1352.md`

- **D7** (`PF_POSE_TRIAL="280,"`): เรียก `pose_trial.boot_banner()` /
  `trial_list_opening()` / `selector_for_hit()` จริงด้วยค่านี้ — คอมมาท้ายทำให้ทั้ง list
  malformed จริงตามที่ chief กลัว **แต่ไม่เงียบ**: `boot_banner()` พิมพ์
  `POSE_TRIAL_BOOT refused=malformed` ตอน import (`pose_trial.py:421-437`) และทุกหมัด
  พิมพ์ `POSE_TRIAL_REFUSED malformed hit=%d` (`:390-391`) — ข้ออ้าง "คอนโซลไม่บอก" เท็จ
  ส่วนที่จริง: fallback กลับ production ไม่ติดตอน malformed (`pose_line` ไม่ใช่ `None`)
  ท่าจึงปิดทั้งบูตจริง เพียงแต่มีบรรทัดบอก · รูที่เหลือ (ไม่ตั้งชื่อโทเคนที่พัง ไม่เช็ค
  behavior id จริง) ยกเป็นงานสำรองรอบหน้า ไม่บล็อก chief
- **D9** (login ส่ง `class_id=1` แต่ pose composer ได้ `None`): ยืนยันตรงตามที่ chief
  เขียนทุกจุด (`player_wire.py:22`, `runtime.py:5159-5161` ไม่ส่ง `class_id=`,
  `combat_pose.py:282-284` no-op ไม่ crash) — ทางแก้อยู่ใน CORE-REQUEST `1352` ที่รอ
  chief อยู่แล้ว ไม่ใช่งานใหม่

## 2. ประกาศจุดต่อให้ LANE-Q — ไม่มีอะไรอยู่จริง บอกตรง ๆ
จดหมาย: `notes_to_chief/20260905_2112_LANE-B-TO-LANE-Q-nothing-exists-yet-here-is-the-seam-and-the-attr-wire-gate.md`

grep ทั้งต้นไม้ก่อนตอบ: ไม่มีจุดลงทะเบียน "มอนตาย"/"kill count" อยู่จริงบน main แม้แต่
stub · กลไก generic `lane_hooks.hook`/`fire` (`lane_hooks/__init__.py:140-238`) มีจริง
แต่ไม่มีจุดเรียกสำหรับ combat เลยสักจุด (จุดเรียกที่มีทั้งหมดเป็นแพ็กเก็ตขาเข้าไคลเอนต์
ล้วน) · buff ของมอนไม่มีระบบเลย · attr เปลี่ยนทางเดียวที่มีคือ `gm/attr_wire.py` ซึ่งบังคับ
ผ่าน `build_named_field_update` ด้วยโค้ด (raise `AttrWireError` ถ้าไม่ตรงชุดที่ยอมรับ)
ไม่ใช่แค่กติกา และมีเกต `hit_frame_encoder_unlocked()` ยืนอยู่ก่อนแล้ว — บอก LANE-Q ว่า
ต้องมีคนเปิดจุดเรียก `lane_hooks.fire("mob_death", ...)` ใน `mob_death.py` (ไฟล์ของสาย
B เอง) ก่อนถึงจะลงทะเบียนอะไรได้จริง เสนอเป็นรอบถัดไป ไม่ผูกเลขใบตอนนี้

## 3. หนี้เทสที่ค้างสามรอบ — จ่ายแล้ว
`tests/test_pf_mine_scene_mob_roster_pure_helpers.py` (ใหม่) — งานสำรองข้อ 3 จากรอบ
`hor2lh` (ตั้งชื่อ) → `x5bkvl` (จ่าย `_digest`) → `qamp70` (ยกต่อ ยังไม่ตรวจ) รอบนี้ตรวจจน
จบ: `_int`/`_key`/`_ascii_dict` ใน `tools/pf_mine_scene_mob_roster.py` ไม่มีเทสที่รันได้
โดยไม่มีบริดจ์เลยสักตัว (`_int`/`_ascii_dict` ไม่มีเทสที่ไหนเลย · `_key` มีแต่ชื่อชนกับ
copy ของ `pf_scan_field_scene_candidates.py` คนละไฟล์) — 13 เทสใหม่ ตามแบบ
`test_pf_mine_scene_mob_roster_digest.py` เป๊ะ

## เทส
- ไฟล์ใหม่เดี่ยว: `pytest tests/test_pf_mine_scene_mob_roster_pure_helpers.py` —
  **13 passed**
- ซ้อมเกตในสภาพไม่มี `pf_bridge` ข้าง ๆ (`git worktree add --detach "$(mktemp -d)" HEAD`
  คัดลอกไฟล์เข้าไป) สองครั้ง (ก่อน/หลังแก้ตาม adversary): **13 passed, 0 skipped** ทั้ง
  สองครั้ง คู่กับ `test_pf_mine_scene_mob_roster_digest.py`: **17 passed, 0 skipped**
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` +
  `--pr-body ... --pr-stage final`: **PREFLIGHT PASS** ทุกแถว (cp874 · no new skips ·
  mainmerge · precondition census · branch mergeable ทั้งสองรีโป · marker ตรงเงื่อนไข
  final)
- ชุดเต็ม (ครั้งเดียวต่อรอบ บน commit สุดท้ายจริง `aa03d9b` หลัง `git fetch origin
  main` — ไม่มีคอมมิตใหม่บน main ระหว่างรอบนี้ base ยังเป็น `82469fb` เดิม):
  **11302 passed, 327 skipped, 20989 subtests passed, 0 failed** (621s/10:21)
- `BYTECODE_PURGED:` ทุกคำสั่งของรอบนี้รันด้วย `PYTHONDONTWRITEBYTECODE=1` + `python3 -B`
- cp874: ไฟล์ใหม่เป็น ASCII ยกเว้น literal CJK หนึ่งตัว (`"雨"`) ในเทสที่พิสูจน์ตัว
  escaper — `tests/` ไม่อยู่ใน prefix ที่ tripwire สแกน (`tools/`/`src/`/`current/`
  เท่านั้น) ยืนยันด้วย `pf_gate_preflight.py` เอง (`[cp874] PASS`)

## เกต (PANYA-DECISION `20260904_1158` §22)
**GATE_UNVERIFIED #853** — เปิด PR 21:29+07 · รอผล job `gate` ของ
run `pull_request` เต็ม 10 นาทีตามกติกา · ปล่อยล็อกตามลำดับจบรอบ

## หมายเหตุ adversary
สั่ง `pf-adversary` หนึ่งครั้ง (จากสองครั้งที่กติกาให้) บนไฟล์ใหม่ก่อน commit
**เจอ 1 ข้อ จ่ายในรอบนี้**: docstring ของไฟล์เทสเองกลับลำดับ `hor2lh`/`x5bkvl` (อ้างว่า
`hor2lh` จ่าย `_digest` ทั้งที่เป็น `x5bkvl` — ตรวจกับ commit message ของ `x5bkvl`
(`d513c9d`) และ docstring ของ `test_pf_mine_scene_mob_roster_digest.py` เองแล้ว) และ
พูดเกินจริงเรื่อง grep hit ของ `_int`/`_ascii_dict` (ไม่มีเลยสักตัว ไม่ใช่ชนชื่อกับ
sibling) — แก้ในคอมมิตแก้ไขเดียวกันรอบนี้ ไม่มีข้อไหนถูกยกไป `ADVERSARY_PENDING`
มิวแทนต์ที่ทดสอบทั้งสี่ตัว (raise หาย `_int` · silent-overwrite `_key` · `sorted()`
หาย · `ascii()`→`repr()` ของ `_ascii_dict`) ตายครบ ไม่มีข้อไหนรอด

## งานสำรอง (3 ข้อ สำหรับรอบถัดไป)
1. หนี้ `DropLedgerCell` ค้างฉากเดิมเมื่อผู้เล่นข้ามฉาก (`#675` ไม่ปิด · `NOW` หาง P-1)
   — ยังไม่แตะ อ่านว่า `reconcile_scene_transition` ถูกถอนออกด้วยเหตุอะไรก่อน (`clw1zb`/
   R297 เขียนไว้ใน `runtime.py` เอง) แล้วเสนอทางที่ไม่ต้องแตะ `runtime.py`
2. `POSE_NO_EQUIP_PROVENANCE` ครั้งเดียวต่อ session — ส่งจดหมายถามจริงแล้วรอบนี้
   (`notes_to_chief/20260905_2113_LANE-B-ASK-COO-*`, ค้างพูดถึงมาสามรอบไม่เคยถามจริง)
   ไม่ได้คำตอบภายในรอบหน้า = เดินตามทาง (A) ที่เสนอไว้ (thread ผ่าน `runtime.py` แบบ
   `hit_number`) รวมเข้า CORE-REQUEST `1352`
3. เปิดจุดเรียก `lane_hooks.fire("mob_death", mob_id=..., scene_id=...,
   killer_character_id=...)` ใน `mob_death.py` ให้ LANE-Q มีจุดลงทะเบียนจริง (ตามที่
   `2112` เสนอ) — ไฟล์เป็นของสาย B เอง ไม่ต้องรอ chief แต่ต้องเลือกจุดเรียกที่ปลอดภัย
   (ไม่ raise ทะลุ `mob_death.kill`) และตัดสินว่า kwargs ชุดไหนพอสำหรับ Quest.MobKillCount

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
**ไม่มี** — รอบนี้เป็นจดหมาย + เทสล้วน ไม่มีบรรทัดโค้ด production ไม่มีเฟรมใหม่ ไม่มี
ข้อมูลโลกถูกแตะ งานหลักของ M4 ยังพักรอ Door B เหมือนเดิม

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยวข้องกับรอบนี้ — ไม่มีโค้ด production หรือ session state
ถูกแตะเลย เทสใหม่ทั้งหมดเป็นตัวแปร local ในเมธอดเทสเดียว

SCOREBOARD: NONE | รอบนี้ไม่มีอะไรที่ผู้เล่นทำได้ต่างจากเมื่อวาน — จดหมายตอบสองใบที่บล็อก
คนอื่น (D7/D9 ของ chief, hook ของ LANE-Q) กับหนี้เทสเก่าที่จ่ายแล้ว | หลักฐาน:
pirate-force-server#853 · pf_bridge#1373
