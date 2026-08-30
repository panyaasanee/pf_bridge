# LANE-B รอบ `qf83nz` -- กล่องจดหมายที่ค้าง 5 ใบ, สอง [ASSUMPTION] ที่ COO เคาะแล้ว, และ
# record ใหม่ให้ chief ต่อสายบรรทัดคอนโซลของสาขา fallback ที่ไม่เคยพูดอะไรเลย

เปิดรอบ 2026-08-30T08:43+07:00 · เขียน 08:5x+07:00
repo: `pirate-force-server` PR #296 · `pf_bridge` PR #470
สาขา: `claude/lane-b-qf83nz` · `claude/lane-b-qf83nz-bridge`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

🔴 **ในตัวเกมวันนี้: ไม่มีอะไรต่างจากรอบนี้เอง** และรอบนี้ไม่อ้างว่ามี -- โค้ดที่แก้คือ
คอมเมนต์เอกสาร (ถอดป้ายสมมติสองจุด) + record ใหม่หนึ่งตัวที่ยังไม่มีจุดเรียกใน `runtime.py`
(chief's file, ไม่แตะ)

**สิ่งที่ต่างไปแล้ว "เมื่อวาน" จริง ๆ (PR #291 ของ chief, merged ก่อนรอบนี้เปิด):** ตีมอนไม่ทำให้
NPC ที่เหลือในแมพหายไปอีกต่อไป (world-wipe ปิดแล้ว) และของที่มอนตัวแรกดร็อปไม่หายไปตอนมอน
ตัวที่สองตาย (whole-live-ledger ปิดแล้ว) -- รอบนี้ทำแค่ "COO เคาะรับรองสองข้อนี้เป็นทางการแล้ว
ถอดป้ายสมมติออกจากโค้ด" ไม่ใช่การส่งของใหม่

## ① ข้อ A ของ ADDENDUM v2 -- ชะตา PR รอบก่อน (`le2dox`)

| repo | PR รอบก่อน | ผล (ถามจาก GitHub API) |
|---|---|---|
| `pirate-force-server` | `#288` | ✅ merged |
| `pf_bridge` | `#457` | ✅ merged |

⇒ ไม่มีอะไรต้อง cherry-pick · ล็อกว่างตอนต้นรอบ (ตรวจ `pulls?state=open` ทั้งสอง repo,
ไม่มี PR หัวข้อ `[LANE-B]` ค้าง) ⇒ เปิด draft PR ยึดล็อกก่อนเริ่มงานตามกฎ

🔴 **หมายเหตุ:** `git fetch origin` พบว่า `origin/main` ในเครื่อง (ทั้งสอง repo) เป็น ref
ที่ค้างมาก (`pirate-force-server` ค้างที่ PR #53 ทั้งที่ merged ล่าสุดคือ #292) --
`git rev-parse main` ในเครื่องผิดจนกว่าจะ fetch สด ตรวจซ้ำด้วย `origin/main` หลัง fetch
เสมอ อย่าเชื่อ ref เก่าที่ค้างในเครื่อง

## ② ข้อ B -- กล่องจดหมาย

**บริโภคห้าใบ (สำเนาไป `notes_to_chief/consumed/` · stub ครบ · ไม่ลบต้นฉบับ):**

1. `20260830_0045_COO-DECISION-refused-ledger-composes-at-ceiling-and-announces.md`
   -- ถอดป้าย `[LANE-B assumption - awaiting COO confirmation]` ออกจาก
   `mob_scene_recompose.py` (ขีดฆ่า ไม่ลบ) เทสสองใบที่ COO สั่งห้ามถอดยังอยู่ครบ
2. `20260829_2342_COO-DECISION-whole-floor-generation-not-covered-by-timer-refusal.md`
   -- ถอดป้าย `[ASSUMPTION OF LANE B - AWAITING COO]` ออกจาก `mob_drop_presence.py`
   เทสสองใบที่ COO สั่งห้ามถอดยังอยู่ครบ
3. `20260829_2245_COO-DECISION-widen-death-scope-bg0002-templates-31-34-35.md` --
   ใบอนุญาตซ้ำ (สาย B แก้ตัวเองไปแล้วในรอบ `m0vp7m` ด้วยใบ `2320`: มอน Bg0002 ตายได้
   อยู่แล้วผ่านใบ `PANYA-DECISION 2026-08-27T20:10` เดิม) -- ตรวจ tie-break ของ
   `mob_death.ruling_for()` แล้ว: ถ้าลงทะเบียนสตริงซ้ำตามที่ COO สั่ง ผลลัพธ์ของทุกมอนจะ
   ยังตอบเป็นใบเดิม (เก่ากว่าชนะ) ⇒ ไม่ลงทะเบียน บันทึกเหตุผลไว้ในบันทึกนี้แทนโค้ด
4. `20260830_0005_CHIEF-REPLY-LANE-B-adversary-eight-findings-and-the-refused-no-ledger-question.md`
   -- ตอบด้วยจดหมาย `20260830_0850_LANE-B-REPLY-*` (ดูข้อ ③)
5. `20260829_2240_LANE-A-TO-LANE-B-scene14-now-has-one-populator.md` -- รับทราบ
   ไม่มีโค้ดต้องแก้ตอนนี้ (hostile splice ฉาก 14 ยังไม่เริ่ม ไม่อยู่ใน BUILD-004/5/6)

**ไม่แตะ `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` รอบนี้:** ไม่มีหัวใบของสาย B ที่มีผล
ใหม่ต้องปิด/อัปเดตจากงานรอบนี้ (การถอดป้ายสมมติ + record ใหม่ที่ยังไม่มีจุดเรียก ไม่ใช่ผล
เทสใหม่)

## ③ no_anchor_record -- ตอบคำถามของ chief (จดหมาย `0005`, รอบ `k882hm`)

chief ถามว่าถ้าโมดูลมี record สำหรับ "ไม่มี anchor / anchor คนละฉาก" เขาจะพิมพ์บรรทัด
คอนโซลของโมดูลในสาขา fallback ได้ด้วย -- สร้างแล้ว:

```
STATE_NO_ANCHOR = "no_anchor_stamped_yet"
STATE_ANCHOR_SCENE_MISMATCH = "anchor_stamped_for_another_scene"
def no_anchor_record(scene_id: int, reason: str) -> SceneRecompose: ...
```

ทั้งสอง **ไม่ใช่สมาชิกของ `COMPOSING_STATES`** (`record.composed` เป็น `False` เสมอ)
`fatal=False` ทั้งคู่โดยตั้งใจ -- ไม่ใช่ดีเฟกต์ กรณีแรกจริงทุกเซสชันก่อน arrival แรก

🔴 **คำเตือนที่ใส่ไว้ในจดหมายตอบ chief:** สอง state นี้ไม่ขึ้นต้น `refused_`/`skipped_` --
ถ้า chief ส่งผ่าน `_recompose_event_suffix()` จะชน invariant ที่
`tests/test_mob_combat_dispatch.py` พินไว้ (D6 ของ chief เอง รอบ `k882hm`) เขียนไว้ชัดใน
จดหมายว่าต้องเก็บ event token เดิมของสาขา fallback ไว้ แล้วแค่เพิ่มบรรทัดคอนโซลคู่กัน

**สามข้อที่ chief ตั้งเป็นเงื่อนไขก่อนต่อสาย "resend เฟรมเก่าที่เก็บไว้"** -- ไม่ตอบทีละข้อ
ปฏิเสธข้อเสนอทั้งก้อนแทน (รายละเอียดเต็มในจดหมาย `0850`): `recompose_frames()` ประกอบสด
จาก ledger ทุกครั้งอยู่แล้ว ไม่เคยแคชไบต์ ⇒ "เฟรมเก่าจะชุบชีวิต HP ไหม" ไม่ใช่คำถามที่เกิดกับ
โมดูลนี้ในสภาพปัจจุบัน ปัญหาจริงของสาขา `else` คือ "ยังไม่มี anchor" ไม่ใช่ "เฟรมเก่า" --
แนะนำไม่สร้างกลไกแคช ปล่อยให้ one-entry fallback เดิมเป็นทางที่ปลอดภัยที่สุดสำหรับหน้าต่าง
สั้น ๆ ต้นเซสชันนั้นต่อไป ถ้าเจ้าของ/COO ต้องการปิดหน้าต่างนั้นจริง ๆ เป็นคำถามคนละขนาดที่
ควรเปิดใบแยก -- ยังไม่เห็นหลักฐานว่าเคยเกิดกับผู้เล่นจริง จึงไม่เปิดใบเอง

เทสใหม่ 7 ใบ คลาส `NoAnchorRecordTests` ใน `tests/test_mob_scene_recompose.py`:
สอง state ไม่ใช่ composing state · ผิดชนิด/ผิด reason โยน `SceneRecomposeError` ก่อนสร้าง
record · ไม่มี FATAL banner (`fatal=False`) · ชื่อฉากตรงกับที่ compose จริงรายงาน (กัน
operator เห็นป้ายฉากสองชื่อสำหรับฉากเดียว)

## ④ ตัวเลขที่วัดได้

```
tests/test_mob_scene_recompose.py : 55 -> 62 ใบ (คลาสใหม่ NoAnchorRecordTests +7)
tests/test_mob_drop_presence.py   : 48 ใบ (ไม่เพิ่ม แก้แค่คอมเมนต์หัวไฟล์ที่ mob_drop_presence.py)
tests/test_mob_death*.py + test_mob_ledger_admission.py : 158 ใบ เขียวหมด (ตรวจว่าการ
  ถอดป้าย/แก้คอมเมนต์ไม่ได้แตะพฤติกรรม)
tests/test_mob_*.py ทั้งโฟลเดอร์ (unittest discover -p "test_mob_*.py") : 766 ใบ เขียวหมด
```

**ASCII สะอาด** ทั้งสามไฟล์ที่แตะ (`mob_scene_recompose.py`, `mob_drop_presence.py`,
`tests/test_mob_scene_recompose.py`) -- ตรวจด้วยสคริปต์นับอักขระ `ord(c) > 127`, พบ 0

**สวีตเต็มทั้ง repo จบแล้วก่อน push** (`unittest discover -p "test_*.py"`, พื้นหลังเพราะ
เกิน 120 วินาทีของเครื่องมือ):

```
Ran 5476 tests in 143.157s
FAILED (errors=18, skipped=212)
```

`errors=18` ทั้งหมดเป็น `ModuleNotFoundError: No module named 'capstone'` ที่ import
ไฟล์เทสสามไฟล์ (`test_stats_progression_static.py`, `test_use_drop_sell_static.py`,
`test_split_operate_verb_panels_static.py`) -- ไลบรารี disassembly ที่ไม่ได้ติดตั้งใน
sandbox นี้ ไม่เกี่ยวกับ `mob_scene_recompose`/`mob_drop_presence` เลย และไม่ใช่ไฟล์ที่รอบ
นี้แตะ **`failures=0`** -- ไม่มีเทสไหนที่รันได้แล้วพังจากการแก้ของรอบนี้

## ⑤ pf-adversary -- ไม่มี agent ให้เรียกจริงในสภาพแวดล้อมนี้ รายงานตรง ๆ แทนการอ้างว่าทำแล้ว

🔴 เครื่องมือของรอบนี้ไม่มี Task/Agent สำหรับเรียก `pf-adversary` หรือ `pf-queue-author`
เป็น subagent จริง (มีแค่ Read/Grep/Glob/Bash/Edit/Write) -- แทนที่จะอ้างว่ารันแล้ว รอบนี้
ทำรีวิวปฏิปักษ์เองด้วยมือแทน แล้วบันทึกไว้ตรงนี้ว่าทำอะไรจริง ไม่ใช่ pipeline เดียวกับรอบก่อน ๆ:

- ตรวจว่า `no_anchor_record` ปฏิเสธ `reason` ที่ไม่รู้จักและ `scene_id` ผิดชนิด ก่อนสร้าง
  record ใด ๆ (เทสพินแล้ว) -- กันมิวแทนต์ "รับทุกสตริงเป็น reason ที่ถูกต้อง"
- ตรวจว่าสอง state ใหม่ไม่ถูกใส่เข้า `COMPOSING_STATES` โดยเทสตรง ๆ (ไม่ใช่แค่คอมเมนต์)
  -- กันมิวแทนต์ที่ทำให้ `record.composed` เป็น `True` สำหรับ record ที่ไม่มีไบต์
- ไล่ `describe_recompose` / `_describe` ด้วยมือว่า record ที่ `heals=False` (ค่าเริ่มต้น)
  และ `unconsulted_rows=None` (ค่าเริ่มต้น) จะไม่โดนสองสาขา FATAL ท้ายฟังก์ชันจับ --
  ยืนยันด้วยเทส `test_the_console_line_names_the_state_with_no_fatal_banner`
- ตรวจ `field_mobs.scene_for_scene_id` / `composer_for_scene_id` fallback chain ด้วย
  scene id ที่ไม่มีทั้งสองตาราง (997) ด้วยมือ -- คืน `"?"` ไม่ raise, สอดคล้องกับ
  `recompose_frames`'s เดิม
- ทวนคำสั่ง COO สองข้อ (0045, 2342) กับโค้ดจริงว่าเทสที่ห้ามถอดยังอยู่ (grep ชื่อฟังก์ชัน
  ตรง ๆ ไม่ใช่จำจากความจำ) -- ดูผลในข้อ ②

**หนี้ที่เปิดไว้ตรง ๆ แทนการซ่อน:** ไม่มีมิวแทนต์เจนจริง (`mutmut`/สคริปต์เฉพาะของ
pf-adversary ไม่ได้รันจริง) -- รอบนี้เป็นรีวิวปฏิปักษ์แบบมือ ไม่ใช่การรันเครื่องมือเดิม
ยกให้รอบถัดไปหรือ pf-adversary agent จริงเวลามันพร้อมใช้ในสภาพแวดล้อมนี้

## ⑥ หนี้ที่รอบนี้จดไว้ ไม่ได้แก้

1. `mob_pickup_persist` ยังไม่มีจุดเรียกใน `runtime.py` -- ตามคิว COO-DECISION
   `20260830_0046` (chief วางจุดเสียบสาย B สามจุด ภายใน ~03:00 ของ chief) ยังไม่เห็นลง
   main ตอนต้นรอบนี้ (08:43) -- chief มี WIP PR เปิดอยู่ (`pirate-force-server#293`,
   `pf_bridge#467`, o1s522) น่าจะเป็นงานนี้ ไม่แตะ ไม่ใช่ล็อกของสาย B
2. `SCENE_RECOMPOSE_WIRING` (docstring ท้าย `mob_scene_recompose.py`) ยังอ้างชุดขั้นตอน
   wiring ที่ chief ทำต่างจากที่เขียนไว้จริง (ของจริงใน `runtime.py` เช็ค
   `census_scene_id == anchor_record.scene_id` ตรง ๆ ไม่ผ่านทรงที่ comment บรรยาย) --
   ไม่ใช่บั๊ก แค่เอกสารล้าสมัย ยกไว้รอบหน้าถ้ามีเวลา ไม่ใช่ของรอบนี้ที่แก้ (นอกสโคปที่มอบหมาย)
3. หัวข้อ 19a ของ `mob_loot.py` (`[ASSUMPTION OF LANE B - awaiting COO confirmation]`
   เรื่อง ledger shape อาจเปลี่ยนถ้า drop ไปทาง FightingDrop* transport) -- คนละเรื่องกับ
   สองป้ายที่ถอดรอบนี้ ยังไม่มีใบ ASK-COO คู่กัน ยกไว้
4. `docs/FUNCTIONAL_COVERAGE.json` ยังเขียนว่า Bg0002 มี 17 monsters -- นอกเขตสายนี้
   (ยกมาหลายรอบ)
5. เทสสองใบที่ pf-adversary รอบ `m0vp7m` ชี้ว่าอ่อน (S7) ยังไม่ได้เสริม

## ⑦ ASK-COO / CORE-REQUEST รอบนี้

ไม่มี -- ทุกอย่างที่ต้องเคาะรอบนี้ COO เคาะไปแล้วก่อนรอบเปิด (0045, 2342) รอบนี้แค่บริโภคผล
