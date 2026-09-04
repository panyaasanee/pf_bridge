round yq5gzr (LANE-B / COMBAT), 2026-09-04T07:32+07:00
boot HEAD: pirate-force-server main ff7c032 (#711) / pf_bridge main 83fa5fe
lock: pf_bridge#1084 claim (ไม่มี [LANE-B] เปิดค้างในสองรีโปตอนต้นรอบ · [LANE-A] #1083 และ
[LANE-GM] #1082 เป็นของสายอื่น ไม่แตะ · [LANE-DB] server#712 เปิดอยู่ ไม่ใช่ล็อกของเรา)

## NOW.md รอบนี้ขยับข้อไหน

**ขยับ `0643` ข้อ 3** (`--self-test` ต้องครอบ `[mainmerge]`) — ลงครบรอบนี้ สี่เคส มิวแทนต์แดง
**ขยับ M4 · Door B กลับเข้าเส้นทาง merge** — งานหนี้ D2/D3/D5/D12/D14/D15 ที่ `#710` ถือไว้
ถูกกู้กลับมาและปิดเหตุตายของมันแล้ว

**ไม่ขยับ M4 ข้อ (1) (caller ของ `apply_hp_damage`) เพราะอะไร**: builder ทรงล็อกอินของ
`gm/attr_wire.py` (LANE-GM รอบ 06:11 ตาม `0545`/`0546`) ยังไม่ขึ้น main **ตอนวัด 07:4x**
`git log origin/main -- src/pirateforce_foundation/gm/attr_wire.py` หัวล่าสุด `ca28a25` (`#700`)
LANE-GM ถือ claim `pf_bridge#1082` รอบ `4fxkam` อยู่ตอนนั้น ⇒ ประตูยังไม่มีชุดค่าให้เสียบตาม
นิยาม (b'') ใหม่ · ตาม `0546` ที่ห้ามรอ รอบนี้ไปเก็บของที่ไม่พึ่งใครแทน ไม่ได้นั่งรอ
🔴 **มันขึ้น main ระหว่างรอบ (`#715` เวลา ~08:5x)** — ประโยคข้างบนจริงตอนวัด ไม่จริงตอนจบรอบ
เก็บไว้ทั้งคู่ตามกฎ "ขีดฆ่า ไม่ลบ" · สิ่งที่เกิดต่อจากนั้นอยู่ในหัวข้อ "กฎ merge-ก่อนรันเต็ม"
ข้างล่าง · caller ยังไม่ได้เสียบ แต่ fixture ของ Door B ย้ายไปอยู่บนชุดของมันแล้ว
**ไม่ขยับ หาง P-1 (จอกะพริบ) และคิวฉาก 3/4/5** — ADDENDUM ข้อ A บังคับกู้ PR ที่ไม่ merge
ก่อนงานใหม่ และรอบนี้เป็นรอบกู้ **ครั้งที่สามติดกัน** (`#694` → `#697` → `#710`)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่เห็นอะไร และ PR ของรอบนี้ไม่อ้างว่าเห็น** Door B ยังไม่มี caller ที่ไหนใน `src/`
`MOB_HIT_FRAME_CONFIRMED` ยังเป็น `None` · `MOB_AI_PLAYER_DAMAGE_WIRING` ยัง ON HOLD
สิ่งที่ต่างคืองาน 6 หนี้กลับมาอยู่บนเส้นทางสู่ `main` แทนที่จะนอนบน PR ที่ถูกปิด

## เหตุตายของ `#710`: ขั้นเดียว และเป็นหมุดที่ไม่มีใครลบ

gate run `33818842135` บน `910eb34` — ทุกขั้นเขียวยกเว้นขั้นเดียว:

    skip_census            exit=1     expect=0     RED
    CENSUS FAILURES (1):
      - PIN DRIFT: tests/test_lane_b_mob_ai_tick.py / design skip
        'persistence_attr_compose stands behind no block at this commit, ...':
        pinned 1, observed 0

รอบ `elvg52` ถอน `persistence_attr_compose` ออกจาก Door B ทั้งก้อน (นั่นคือสิ่งที่ `0546` สั่ง
และมันถูก) การ์ด `test_the_block_is_not_adjudicated_on_this_tree` จึงหายไปพร้อม `skipTest`
ของมัน — แต่ **หมุดใน `docs/PYTEST_SKIP_PINS.json` ถูกทิ้งไว้** census จึงเห็น pinned 1
observed 0 แล้วแดง

หมายเหตุของหมุดนั้นเขียนสั่งตัวเองไว้ตรง ๆ อยู่แล้ว:

    it lifts only if x=30 leaves SENSITIVE_FIELDS, or if the card stops asking
    for a 55-row block.  Delete this pin in the same commit that removes the
    skipTest, whichever of those two happens.

เงื่อนไขข้อหลังเกิดจริง และรอบนั้นไม่ได้ลบหมุด

🔴 **บทเรียนที่กว้างกว่ารอบนี้** กฎ "ตัวเลขต้องขยับใน commit เดียวกับเทสที่ทำให้มันขยับ" ทุกคน
อ่านเป็น "เพิ่ม skip ต้องเพิ่มหมุด" · ความจริงมันวิ่ง **สองทาง** — ลบ skip คือการขยับหมุดไปเป็น
ศูนย์ และ census แดงเท่ากัน · ถ้อยคำใน NOW.md เองก็เขียนว่า "รอบที่เพิ่มไฟล์เทสใหม่ **หรือเพิ่ม
skip ใหม่** ต้องซ้อมทั้ง `pytest_subset` และ `skip_census`" ⇒ รอบที่ **ลบ** skip อ่านแล้วคิดว่า
ไม่เข้าเงื่อนไข · เสนอถ้อยคำใหม่ให้ COO เคาะ chief เขียน: "รอบที่ **แตะ** skip ใด ๆ (เพิ่ม ลบ
ย้าย) ต้องซ้อม `skip_census`" · ส่งเป็นจดหมาย `20260904_0757_LANE-B-REPORT-COO-...`

## รอบนี้ทำอะไร

### ฝั่ง pirate-force-server (PR ของรอบ)

1. `git cherry-pick 8273aec` และ `910eb34` จาก `claude/magical-hawking-elvg52` ลงกิ่งที่ตัดจาก
   main วันนี้ (`ff7c032`) — สะอาดทั้งคู่ ไม่มี conflict ไม่ได้พิมพ์โค้ดใหม่สักบรรทัด
   (ADDENDUM ข้อ A: ห้ามเริ่มใหม่จากศูนย์ · ใบ `0704_SYNC-NOTICE` สั่งข้อเดียวกัน)
2. ลบรายการ `design_skips` ที่ค้างใน `docs/PYTEST_SKIP_PINS.json` พร้อม **คำจารึก** ในบล็อก
   `why` ของไฟล์เดียวกัน (ขีดฆ่า ไม่ใช่ลบเงียบ) ระบุว่าเงื่อนไขปลดข้อไหนเกิดจริง รอบไหนทำให้เกิด
   และกฎมันวิ่งสองทาง · เหลือ `design_skips` หนึ่งรายการ
   เทสที่กินไฟล์นี้ (`tests/test_pytest_precondition_census.py`) วนทั้งลิสต์อยู่แล้ว ไม่มีตัวไหน
   ปักความยาว — `design_skips[0]` ที่ถูกอ้างอิงยังมีของอยู่

### ฝั่ง pf_bridge

3. `tools_bridge/pf_gate_preflight.py` — `--self-test` ครอบ `[mainmerge]` แล้ว (`0643` ข้อ 3)
   `_mainmerge_self_test_cases()` สร้าง repo git จริงในไดเรกทอรีชั่วคราวแล้วเรียก
   `check_base_is_ancestor` **ตัวจริง** ไม่ mock git สักบรรทัด สี่เคส:

       RED   HEAD ตามหลัง base ไม่มีไฟล์ทับกันเลย   <- ทรงเดียวกับ #697 เป๊ะ
       RED   HEAD ตามหลัง base มีไฟล์ทับกันหนึ่งไฟล์ <- คลุมข้อความอธิบายอีกทาง
       PASS  merge base เข้ามาแล้ว                   <- ต้นไม้ที่ 0053/0149 บังคับ
       None  base resolve ไม่ได้ = INCONCLUSIVE ห้ามอ่านเป็น PASS

   จำนวนเคสพินไว้ข้าง ๆ (`MAINMERGE_SELF_TEST_CASES = 4`) ไม่ derive จากลิสต์ตัวเอง
   ตามบทเรียน D3 ของ R328 ⇒ เคสหาย หรือเครื่องไม่มี git = แดง ไม่ใช่รายงานเขียวที่สั้นลง
4. `0643` ข้อ 2 (ข้อความ RED ต้องพิมพ์คำสั่งแก้สองบรรทัดพร้อมกัน) — **มีอยู่แล้ว ไม่ได้เติม**
   ยืนยันจากผลรันจริง ไม่ใช่จากการอ่านซอร์ส (ผลอยู่ในหัวข้อหลักฐาน)
5. บริโภคใบ `0643` และ `0704` (stub + สำเนาเข้า `consumed/`) · จดหมายรายงาน COO หนึ่งใบ

## หลักฐาน

    $ python3 tools_bridge/pf_gate_preflight.py --self-test        (pf_bridge)
      mainmerge HEAD behind mainline, no file touched by both (the #697 shape) expected=False got=False ok
      mainmerge HEAD behind mainline, one file touched by both sides           expected=False got=False ok
      mainmerge mainline merged into HEAD - the tree the suite must be run on  expected=True  got=True  ok
      mainmerge base does not resolve (nothing fetched)                        expected=None  got=None  ok
      SELF-TEST PASS: 19 cases, 19 compared.

    ข้อความ RED ที่เคสแรกพิมพ์ออกมาจริง (0643 ข้อ 2 มีครบอยู่แล้ว):
      Fix: git fetch origin main && git merge origin/main,
      then run the FULL suite again on that tree (NOW.md `0053`/`0149`), then push.

    มิวแทนต์ (stub check_base_is_ancestor ให้คืน True เสมอ = รูรั่วที่ฆ่า #694/#697):
      SELF-TEST RED: 3 of 19 case(s) wrong.

    $ python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server   (ก่อน push จริง)
      [cp874] PASS  ·  [skips] PASS - no new skip markers vs origin/main
      [mainmerge] PASS - origin/main (f27005c) is already in HEAD
      [prbody] PASS - exactly one marker line          (ตรวจ body ของ #717 ก่อนเปิด)

    $ python3 tools/verify_functional_coverage.py     FUNCTIONAL_COVERAGE PASS domains=8
    $ python3 tools/verify_hypothesis_ledger.py       HYPOTHESIS_LEDGER PASS entries=50
    $ python3 -m pytest tests/test_lane_b_mob_ai_tick.py tests/test_pytest_precondition_census.py \
        tests/test_gm_attr_wire.py tests/test_gm_login_mask.py tests/test_foundation_legacy_seam.py -q
      276 passed, 1205 subtests passed

    ซ้อมเกตสองช่อง บน worktree ที่ไม่มี pf_bridge ข้าง ๆ (AGENTS.md §7)
    บน commit สุดท้ายจริง `6d0e3378` (merge main `f27005c0` = #713 #714 #715 แล้ว):
      $ grep -l 'GameClient\|capture_v141' tests/*.py | sort -u \
          | grep -v test_foundation_legacy_seam.py > excl.txt          # 48 โมดูล
      $ python3 -m pytest tests -q -rs $(sed 's|^|--ignore |' excl.txt) > log.txt
        8583 passed, 83 skipped, 16681 subtests passed in 376.04s      pytest_subset exit=0
      $ python3 tools/pf_pytest_precondition_census.py --report log.txt --excluded excl.txt
        every skip is declared, named and pinned
        RESULT: PASS                                                   skip_census  exit=0

    🔴 ช่อง `skip_census` คือช่องเดียวที่แดงใน `#710` · เขียวแล้วบนต้นไม้เดียวกับที่ push

    ชุดเต็มแบบธรรมดา (มี pf_bridge ข้าง ๆ · commit เดียวกัน `6d0e3378`):
        9522 passed, 323 skipped, 18710 subtests passed in 404.10s     exit=0

    🔴 ทำไมรอบนี้รันเต็ม **สองครั้ง** (กฎบังคับให้เขียน): มันคนละ selection และมาจากคนละกฎ
    (ก) ซ้อมเกตสองช่องต้องรันในสภาพ "ไม่มี pf_bridge ข้าง ๆ" และ **ตัด 48 โมดูล** ตามสูตรของ
        เกตเอง — เป็นช่องที่ปิด `#710` และเป็นสิ่งที่รอบนี้ต้องพิสูจน์ว่าแก้แล้ว
    (ข) ชุดเต็มแบบธรรมดามี 48 โมดูลนั้นด้วย และรอบนี้ยก cherry-pick ขึ้น main ที่ขยับไปแล้ว
        (`59b1fb0` → `ff7c032`) ⇒ โมดูลที่ (ก) ตัดทิ้งไม่เคยถูกรันเทียบ main ใหม่เลย
    (ก) อย่างเดียวไม่ครอบ (ข) และ (ข) อย่างเดียวไม่ครอบ (ก) — รอบก่อนรัน (ข) อย่างเดียว แล้วตาย
    ที่ (ก) จึงไม่ยอมจ่ายราคานั้นซ้ำอีกรอบ
    🔴 และรันซ้ำอีกชุดหลัง `#715` ขึ้น main กลางรอบ (ดูหัวข้อถัดไป) เพราะกฎห้าม push
    สภาพที่ไม่เคยถูกรันเต็ม · ตัวเลขข้างบนคือชุดสุดท้ายบน `6d0e3378` ที่ push จริง

## pf-adversary — ผลคืนก่อน push แก้ครบในรอบเดียวกัน

สั่งต้นรอบพร้อมเริ่มงานตาม COO `0903_2345` · ผลคืนเวลา ~07:5x (19 นาที) ก่อน push ⇒ ไม่มี
`ADVERSARY_PENDING` รอบนี้ · **หกข้อ แก้ห้า ถามหนึ่ง** ทุกข้อที่แก้ซ้อมมิวแทนต์ก่อน commit

- **D1 (HIGH)** การ์ด `..._is_never_invoked_at_runtime` อ้างว่า "ไม่มีเส้นทางไหนผ่านมันได้"
  **เท็จ** — `patch.object` ผูกกับ **แอตทริบิวต์ของโมดูล** เอื้อมไม่ถึงชื่อที่ประตูผูกไว้
  **ตอน import ตัวเอง** · มิวแทนต์สองบรรทัดระดับโมดูล (`import_module` + `getattr`
  ต่อสตริงทั้งคู่) เรียก `block_gaps` ตัวจริงโดยการ์ดทั้งสองใบเขียว
  แก้: การ์ดใหม่ถามว่า **ชื่อในเนมสเปซของประตูผูกกับ "วัตถุ" อะไร** ไม่ใช่ว่าสะกดยังไง
  และเขียนตรง ๆ ว่ายังไม่ครอบอะไร (คำอ้างว่าครอบทุกอย่างครั้งก่อนคือสิ่งที่ผิด)
- **D2 (HIGH)** เกตกันเขียนแคช (D7) เป็น AST อย่างเดียว และ **เหตุผลที่ว่าทำไมถึงเป็น AST
  อย่างเดียวหมดอายุใน commit เดียวกับที่เขียนมันเอง** — การถอน adjudicator ของรอบนี้คือสิ่งที่
  ทำให้เขียนการ์ดพฤติกรรมได้แล้ว · มิวแทนต์ผ่าน `getattr(cache, 'capture_'+'initial')`
  ทิ้ง 55 แถวไว้ในคอนเนกชันที่ประตูเพิ่ง **ปฏิเสธ** โดยทุกการ์ดเขียว
  แก้: การ์ดพฤติกรรมขับประตูจริง — ปฏิเสธ = แคชต้องไม่ถูก seed · ทางบวก = ขยับได้แถวเดียว
  (แถวของเฟรมเอง) เป็นค่าที่สั่งเท่านั้น · 🔴 **วัดได้ว่าทางบวกแคช "ขยับจริง" โดยชอบ**
  เพราะ `build_named_field_update` เรียก `record_sent` ขาออก — ร่างแรกของการ์ดนี้ assert ว่า
  แคชต้องเหมือนเดิมเป๊ะแล้วแดงตรงนั้น จึงแก้เป็นการปักรูปร่างของการขยับแทนการห้ามขยับ
- **D3 (MEDIUM) — และนี่คือ "คลาส" ของเรื่องทั้งรอบ** `preconditions` มีการ์ดสองใบที่ derive
  จากซอร์สของโมดูล ⇒ ลบ guard แล้วแดงในเครื่อง · **`design_skips` ไม่มีอะไรแบบนั้นเลย**
  หมุดที่ skip ของมันหายไปแล้วจึงผ่านทุก selection ในเครื่อง และแดง **เฉพาะบนเกต Windows**
  นั่นคือวิธีที่ `#710` ตายเป๊ะ ๆ · แก้: `design_skip_sites()` + การ์ดสองใบ
  ซ้อมด้วยหมุดผี ⇒ แดงในเครื่องภายใน 2.7 วินาที แทนที่จะเสียไปทั้งรอบ
- **D4 (MEDIUM)** เหลือคำอ้างปัจจุบันกาลสองที่ว่า `build_named_field_update` ต้องการ
  "26 แถว `named_field_x()`" · **ผิดสองชั้น**: ชุดนั้นมี **27** แถววันนี้ (x=9 เข้าไปตั้งแต่
  `5ce0d39`) และตัวตรวจความครบอ่าน **`all_field_x()` ทั้ง 55 แถว** (`0215`)
  ⇒ `mob_hit_frame.py` ขัดกับ docstring ของตัวเองห่างกันสิบเอ็ดบรรทัด บนคำอ้างที่แบกน้ำหนัก
  ที่สุดของการถอน · commit message รอบก่อนเขียนว่าแก้ครบทุกที่แล้ว ซึ่งไม่จริง
- **D5 (MEDIUM)** คำจารึกที่ **รอบนี้เพิ่งเขียนเอง** ระบุการ์ดผิดใบว่าเป็นบ้านของ skip
  ตัว `skipTest` อยู่บรรทัด 1183 ใน `test_when_the_adjudicator_agrees_the_frame_is_a_full_block`
  ส่วนใบที่ reason ของหมุดเอ่ยถึงนั้นเป็นแค่ใบที่ **วัด** เงื่อนไข · แก้ในที่เดิม เพราะคำจารึก
  คือบันทึกถาวรของ "ทำไม" ถ้ามันชี้ผิดบรรทัด คนอ่านรอบหน้าจะหาไม่เจอ
- **D6 (MEDIUM · ดีไซน์) ไม่แก้ ถาม** ประตูตรวจ **คีย์** ของ `live` แล้ว **ทิ้งค่าของมัน**
  เฟรมประกอบจากแคชของคอนเนกชัน ⇒ เกตสองตัวเฝ้าข้อมูลที่ไม่มีผลต่อไบต์เลย และไม่มีใครบังคับว่า
  แคช "สด" ทั้งที่ `RE-222` บอกว่าทุกแถวทับของเดิมบนจอ · ติดป้าย
  `[OPEN QUESTION - LANE-B raised, COO to decide]` ไว้ที่เกต และเปิดใบ
  `20260904_0800_LANE-B-ASK-COO-door-b-validates-live-values-then-ships-the-cache.md`
  เข้าเงื่อนไข "หยุดรอได้" ข้อ (ก) และประตูยังส่งศูนย์ไบต์ ⇒ ไม่มีอะไรพังระหว่างรอ

ที่ตรวจแล้วไม่พังและไม่ต้องแก้: การลบหมุดถูกต้องจริง (ไม่มี skip กลไกใดเหลือในโมดูลนั้นเลย
ตรวจด้วย grep · AST walk · โคลนสดที่ artifact หายทุกตัว · และเทียบกับลิสต์ `--ignore` 48 โมดูล
ที่ derive ใหม่จากสูตรของเกตเอง ซึ่งไม่ได้ซ่อนโมดูลนี้) · ไม่มีอะไรในรีโปพึ่งรายการที่ลบหรือพึ่ง
ไบต์ของไฟล์หมุด · หมุดทุกตัว derive ใหม่ที่ HEAD แล้วยังตรง (`GRADE_SUBSET_SHA256`,
`COVERAGE_EVIDENCE_DEBT_PIN`=0, จำนวนและสมาชิก 48 โมดูล, หมุดแถว vital ของ D5)
· cherry-pick ทั้งสองใบเป็น patch ที่ byte-identical กับต้นฉบับ

### ของแถมที่เจอเองระหว่าง preflight (ไม่ใช่ข้อของ adversary)
การ์ดใหม่ของ D3 มี fixture ที่เป็น "ซอร์สที่พูดถึง skip" ⇒ `pf_gate_preflight.py` ซึ่งจับด้วย
ข้อความล้วน อ่านเป็น **skip ใหม่ 5 ตัวที่ไม่มีหมุด** และขึ้น RED · แก้ด้วยการประกอบ fixture
จากชิ้นส่วน แบบเดียวกับที่ `MARKER_TOKEN` ในเครื่องมือนั้นทำกับตัวเอง ด้วยเหตุผลเดียวกัน
🔴 แล้วคอมเมนต์ที่ **อธิบายการแก้นั้นเอง** ก็เพิ่ม RED อีกสองบรรทัด เพราะไปยกสตริงมาอ้าง
— แก้อีกครั้งด้วยการชี้ไปที่ `SKIP_MARKERS` แทนการพิมพ์ซ้ำ · เป็นบทเรียนเดียวกับ `#672`/`#1015`
ที่ marker หลุดเพราะประโยคที่เตือนเรื่อง marker

## 🔴 กฎ merge-ก่อนรันเต็ม จับ `#697` ได้จริงรอบนี้ (ของใหม่ ไม่ใช่ทฤษฎี)

หลังเปิด PR เซิร์ฟเวอร์ #717 แล้ว `git fetch` พบว่า main ขยับอีกจาก `dff25e3d` เป็น `f27005c0`
(`#713` `#714` `#715`) — และ **`#715` ของ LANE-GM แตะ `gm/attr_wire.py`** ซึ่งเทส Door B อ่านอยู่

merge เข้ามาแล้วรันเทสของสายเอง ⇒ **แดงสามใบทันที**

    AttrWireError: refusing to build a 0x309A frame that is not login-shaped:
    55 rows given ... admitted login shapes are [[1,2,3,4,7,9,10,13,24], ...]

นี่คือกลไก `#697` เป๊ะ ๆ (กิ่งเขียว · ต้นไม้ที่ merge แล้วแดง · **ไม่มีไฟล์ทับกันสักไฟล์**)
ต่างกันที่รอบนี้เห็นมันในเครื่องตัวเองแทนที่จะไปเห็นตอนเกตปิด PR
⇒ กติกา `0053`/`0149` + เช็ก `[mainmerge]` ที่รอบนี้เพิ่งเขียนเทสให้ **คุ้มค่าตัวเองในรอบเดียว**

**และนี่คือ builder ที่รอบนี้เขียนไว้ตอน 07:4x ว่า "ยังไม่ขึ้น main"** — ตอนวัดยังไม่ขึ้นจริง
มันขึ้นระหว่างรอบ · Door B จึงเดินตาม `0546` ได้แล้วบางส่วนในรอบนี้เอง:

- `_full_valid_baseline()` seed ชุดที่กว้างที่สุดจาก `login_mask.admitted_field_x_sets(legacy)`
  **derive จากฟังก์ชันของ LANE-GM เอง ไม่พิมพ์เลขแถวลงไป** (พิมพ์เอง = ปักชุดที่สายเราไม่ได้เป็น
  เจ้าของ และนั่นคือหมุดที่เพิ่งเน่าให้ดูเมื่อกี้)
- การ์ดทางบวกเคย assert ว่า **ทั้ง 55 แถว** ต้องมีบิต — ถูกเมื่อ (b'') แปลว่าทั้งบล็อก
  ตอนนี้ถามคำถามเดิมกับชุดของแคชแทน **และถามสองทาง**: บิตที่ตั้งให้แถวที่แคชไม่มี
  = ศูนย์บนจอผู้เล่น ไม่ใช่ "ไม่เปลี่ยน" (`RE-222` Q0) ⇒ mask กว้างเกินผิดเท่ากับแคบเกิน
- 🔴 คำแก้ D4 ที่ **รอบนี้เพิ่งเขียนเองเมื่อชั่วโมงที่แล้ว** ("อ่าน `all_field_x()` ทั้ง 55 แถว")
  กลายเป็นเท็จภายในชั่วโมงเดียว · ประโยคนั้นผิดมาแล้ว **สองครั้ง** ⇒ เขียนใหม่ให้ชี้ไปที่
  `login_mask` ว่าใครคือเจ้าของคำตอบ **แทนการพิมพ์ตัวเลข** ทั้งในโค้ดและในเทส

## ที่ยังไม่ได้พิสูจน์รอบนี้

ไม่มีไบต์ออกไปหาผู้เล่นสักไบต์ · เกตของ Door B ปิดครบทุกตัว · การที่ `skip_census` เขียวบนเครื่อง
นี้ไม่ใช่คำสัญญาว่าเกต Windows เขียว — สิ่งที่วัดได้คือ PIN DRIFT ตัวที่ปิด `#710` หายไปแล้ว

## รออะไรอยู่ / รอบถัดไปทำอะไร

builder ทรงล็อกอิน **ขึ้น main แล้วระหว่างรอบนี้** (`#715`) ⇒ ไม่มีตัวบล็อกนี้อีกต่อไป
รอบนี้พา fixture ของ Door B ไปอยู่บนชุดเดียวกับมันแล้ว แต่ **ยังไม่ได้เสียบ caller**
รอบถัดไปของ LANE-B ตามลำดับ:
1. หยิบคำตอบใบ `0800_LANE-B-ASK-COO-...` (D6) ถ้า COO ตอบแล้ว — เป็นงานแรกก่อน claim ใหม่
2. เสียบ Door B เข้ากับ `login_mask` ตาม `0546` (ตอนนี้มีของให้เสียบจริงแล้ว)
3. ถ้าข้อ 2 ติด ให้ไปคิวฉาก 3/4/5 (`COO 2246`)

## บันทึกท้ายรอบ

push แล้ว รอ merge **PR #717** (pirate-force-server · `[LANE-B] round yq5gzr: #710 recovered,
and the design pin nobody deleted now has a local witness`) — **เปิดแล้ว ไม่ draft มี marker
ยืนยันด้วย GET แล้ว · รอ gate** · commit สุดท้าย `6d0e3378`

pf_bridge: claim **PR #1084** — เติม marker ตอนจบรอบ = ปลดล็อก

🔴 **ห้ามอ่านว่า "เสร็จ" หรือ "อยู่บน main แล้ว"** — รอบถัดไปของ LANE-B ต้องตรวจชะตาของ #717
เป็นงานแรกตาม ADDENDUM ข้อ A ก่อน claim อะไรใหม่ · ถ้ามัน `merged=false` ให้กู้จากกิ่ง
`claude/sharp-newton-yq5gzr` ตามเดิม (นี่จะเป็นรอบกู้ครั้งที่สี่ติดกัน ถ้าเกิดขึ้นให้รายงาน COO
ในฐานะ "กฎหยุดสองครั้ง" — แต่เหตุตายต้องเป็น **เหตุเดิม** ถึงจะนับ · `#710` ตายที่ `skip_census`
ซึ่งรอบนี้ปิดทั้งอินสแตนซ์และคลาสแล้ว)
