# LANE-A รอบ `tk4hr7` — re-land `#852` (SAILING_RESULT key) พร้อมหมุด skip ที่หายไป

รหัสรอบ: `tk4hr7` · เริ่ม 2026-09-05T22:22+07:00 · claim `pf_bridge#1384`
กิ่ง: server `claude/nifty-euler-tk4hr7` · bridge `claude/pensive-cerf-tk4hr7`

## รอบนี้ขยับ NOW/M ข้อไหน

**M2 "ออกจากเมืองได้" — ตัวบล็อกโค้ดตัวเดียวของทั้งไมล์สโตน**
NOW `2152` เขียนว่า `#852` "รอเกต" ซึ่งไม่จริงแล้วตั้งแต่ 21:54: เกตแดงและ
reaper ปิดใบทิ้ง (SYNC-NOTICE `2204` มาถึงตอน 22:04) รอบนี้เอางานกลับขึ้นมาใหม่
พร้อมแก้สาเหตุที่ทำให้มันตาย ⇒ `GT-233` v3 ยังบูตไม่ได้จนกว่าใบใหม่จะขึ้น main
(กฎ NOW ข้อ "รอเครื่องคุณ" ข้อ 1 ยังยืน)

## ล็อกรอบ

list PR ทั้งสองรีโป 22:22 — ไม่มี `[LANE-A]` open เลยทั้งคู่ (`#852` ปิด 21:54,
`#847` ปิด 20:52) ⇒ ไม่ใช่ takeover เปิด claim ใหม่ `pf_bridge#1384` 22:22
list ซ้ำหลังเปิด: `#1384` เป็น `[LANE-A]` ใบเดียว ใบอื่นเป็น GM/DB/UI/courier
ไม่ใช่ล็อกของสายนี้ ไม่แตะ

## สาเหตุที่เกตแดง — ตอบ COO-DECISION `2151` ข้อ 2 ข (หนึ่งบรรทัดตามที่สั่ง)

**ช่อง `skip_census` ช่องเดียว ไม่ใช่เทส ไม่ใช่ cp874 ไม่ใช่ census tripwire ของฉาก:**
`UNPINNED: tests/test_world_m2_sailing_result_key.py skipped 1 test(s) on
precondition 'bridge_gamedata'. Add it to docs/PYTEST_SKIP_PINS.json in the
same commit.` ⇒ `RESULT: FAIL` ⇒ `skip_census exit=1 expect=0 RED`

`#847` (job 101313822248) กับ `#852` (job 101321779770) ตารางสรุปเกตเหมือนกันเป๊ะ
— ทุกช่อง GREEN เหลือ `skip_census` ช่องเดียว RED **สาเหตุเดียวกันทั้งสองใบ**

## ทำไมรอบก่อนมองไม่เห็น (ของจริงที่ต้องบันทึก ไม่ใช่ความสะเพร่า)

รอบ `wjprxa` ได้ `PREFLIGHT PASS` บนคอมมิตที่ตาย และสรุปว่า "ไฟล์เทสใหม่ไม่เพิ่ม
skip (0 skip ในไฟล์ใหม่ทั้งสอง)" — วัดสดรอบนี้ว่าประโยคนั้นจริงบนเครื่องเรา:

```
ls -d ../pf_bridge/gamedata/tables            -> PRESENT
pytest tests/test_world_m2_sailing_result_key.py -q -rs
  -> 17 passed, 18 subtests passed            (0 skipped)
```

`@BRIDGE_GAMEDATA.skip_unless_present()` skip เฉพาะเมื่อ **ไม่มี** `pf_bridge`
ข้าง ๆ · โคลนคลาวด์มีเสมอ ⇒ skip ไม่เกิด ⇒ census ไม่มีบรรทัดให้อ่าน ⇒ เขียว
เกต Windows เช็คเอาต์รีโปเดียว ⇒ skip เกิด 1 ⇒ ไม่มีหมุด ⇒ แดง
แถว `[census]` ของ `pf_gate_preflight.py` รันในสภาพเครื่องปัจจุบัน
(artifact present ⇒ expected 0, observed 0) จึงตอบ PASS ได้เสมอสำหรับ skip
ชนิดนี้ — รูของเครื่องมือ ไม่ใช่รูของกฎ (`AGENTS.md` §7 สั่งซ้อมไว้ถูกแล้ว)
⇒ เขียนเป็นจดหมาย `2248` ถึง COO พร้อมทางแก้สามทาง (เขต `tools_bridge/` = chief)

## ทำอะไรไปบ้าง

1. `git fetch origin claude/magical-goldberg-wjprxa` แล้ว **cherry-pick คอมมิต
   เดียวของ `#852` มาทั้งดุ้น ไม่แก้เนื้องานแม้บรรทัดเดียว** (`06461e6` →
   `0851b46`) · ตรวจก่อน cherry-pick ตามกฎ §7:
   `git merge-base --is-ancestor 06461e6 origin/main` = **exit 1** (ไม่อยู่บน main)
   ไม่ได้ใช้ฟิลด์ `merged=false` เป็นเหตุผล
2. เติมหมุดที่ขาดใน `docs/PYTEST_SKIP_PINS.json`:
   `key=bridge_gamedata` · `module=tests/test_world_m2_sailing_result_key.py` ·
   `count=1` · test เดียวคือ
   `CurateReDerivationTests::test_the_committed_copy_matches_a_fresh_curate_from_the_bridge`
   note เขียนไว้ยาวว่าหมุดนี้เกิดเพราะอะไร skip นี้ราคาเท่าไร (บนเครื่องที่ปิดใบ
   TSV ไม่เคยถูก re-derive) และอะไรคือส่วนที่เกตยังรันได้ (`CommittedCopyTests`
   สองตัวที่ปฏิเสธสำเนาที่ถูกแก้มือโดยไม่แก้ pin)
   — แก้ทางที่ §7 อนุญาต **ไม่ได้อ่อนตัว census ลงแม้แต่นิดเดียว**
   อ่านโค้ด census ยืนยันความหมายของ `count` ก่อนเติม:
   `expected = 0 if module excluded · 0 if artifact present · else count`
   ⇒ หมุด count 1 ถูกต้องทั้งบนสะพาน (present ⇒ 0/0) และบนเกต (absent ⇒ 1/1)
3. **ซ้อมเกตในสภาพ "ไม่มี `pf_bridge` ข้าง ๆ" จริง** ตามสูตร §7 ตรงตัว
   (`git worktree add --detach "$(mktemp -d)" HEAD` · ไม่มี `rm -r` ทุกการสะกด
   ทั้งรอบ · ไม่ `worktree remove` ตามที่ §7 สั่ง) อ่าน exit code **ทั้งสองบรรทัด**:
   - `pytest_subset` **exit=0** — 10381 passed, 111 skipped, 18988 subtests
   - `skip_census` **exit=0** — `every skip is declared, named and pinned` ·
     `RESULT: PASS` · บรรทัดที่เคยฆ่าสองใบตอนนี้อ่านว่า
     `bridge_gamedata  tests/test_world_m2_sailing_result_key.py  x1`
4. `git merge origin/main` (`322f7da`) — **conflict** ที่ `PYTEST_SKIP_PINS.json`
   กับหมุด `lupa_package` ของ LANE-Q (`#855` เพิ่ง merge) แก้แบบ **เก็บทั้งสอง
   รายการ** ไม่ทับของสายอื่น (ยืนยัน JSON ยัง parse ได้ · ทั้งสองโมดูลอยู่ครบ)
5. ชุดเต็มบนต้นไม้สุดท้ายหลัง merge = commit สุดท้ายจริง

## หลักฐาน

- ชุดเต็ม (`pytest tests/` ครั้งเดียวต่อรอบ บนต้นไม้ที่ merge `origin/main`
  `322f7da` แล้ว): **11353 passed, 349 skipped, 21081 subtests passed,
  0 failed** (607.50s)
- ซ้อมเกตไร้ sibling: `pytest_subset exit=0` · `skip_census exit=0` (ข้างบน)
- `tools_bridge/pf_gate_preflight.py --repo` = **PREFLIGHT PASS**
  (cp874 · no new skips · main อยู่ในกิ่ง · census agrees · mergeable ·
  ไฟล์ bridge ใต้เพดาน)
- `BYTECODE_PURGED: PYTHONDONTWRITEBYTECODE=1 + python3 -B` ทั้งรอบ
- diff เทียบ `origin/main` = 7 ไฟล์ +479/-7 (6 ไฟล์เดิมของ `#852` + หมุด 1 ไฟล์)

## หลักฐานสองชั้น แยกกัน

- **ชั้นเกต/เครื่องมือ** (ชั้นที่รอบนี้ซ่อม): census ในสภาพเกตจริงตอบ PASS
  วัดจาก log ที่มี `-rs` ของตัวเอง ไม่ได้อ้างจากชุดเต็ม
- **ชั้นเนื้องาน** (ชั้นที่ `#852` พิสูจน์ไว้แล้ว ไม่ได้แก้รอบนี้):
  เทส 17 ตัวของโมดูล + การ re-derive TSV จากต้นทางบนสะพาน
  **ไม่ใช้ชั้นหนึ่งอ้างอีกชั้น** — census เขียวไม่ได้แปลว่า key ถูก และเทสเขียว
  ไม่ได้แปลว่าเกตจะเขียว (นั่นคือบทเรียนของรอบนี้ทั้งรอบ)

## nonclaims

1. **ไม่อ้างว่า `#852` ใบใหม่จะ merge** — เขียนได้แค่ "เปิดแล้ว รอเกต"
   "อยู่บน main" ต้องรอรอบหน้าวัดด้วย `git merge-base --is-ancestor`
2. ไม่อ้างว่าแถวไหนใน 18 แถวคือ key ที่ "ถูก" ของเกาะ 2/เกาะ 3 — ตารางไม่บอก
   เป็น provisional ตาม COO เหมือนเดิม ไม่มีอะไรเปลี่ยนจาก `#852`
3. ไม่อ้างว่า `Common_Confirm` จะเด้งบนจอ — นั่นคือ `GT-233` v3 (attended)
4. ไม่อ้างว่ารูของ `pf_gate_preflight.py` ปิดแล้ว — **ยังเปิดอยู่** รอบนี้แค่
   วัดมันและส่งจดหมาย เขต `tools_bridge/` ไม่ใช่ของสายนี้
5. ไม่แตะ `runtime.py` · `app.py` · v141 · เขตสายอื่น · ไม่มี CORE-REQUEST ใหม่

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว — รอบนี้ไม่แตะสถานะโลกต่อฉากที่แก้ไขได้
มีแต่ตารางนิ่ง (สำเนา TSV ที่ pin ด้วย SHA256) ฟังก์ชันอ่านอย่างเดียว และหมุด
JSON ของเกต · สอง session ในฉากเดียวกันอ่านค่าเดียวกันจากตารางเดียวกัน

## adversary — ผลคืนแล้ว 23:05 หลังปลดล็อก (บันทึกอย่างเดียว ไม่แตะโค้ด)

🔴 ผลคืน **หลัง** เติม marker ปลดล็อก ⇒ ตามกติกา `COMMON_LANE_ROUND`
("ผล pf-adversary เพิ่งคืน/เจอของต้องแก้หลังปลด ⇒ เขียนลงไฟล์รอบ รอบถัดไปหยิบ
เป็นงานแรก") รอบนี้ **บันทึกอย่างเดียว ไม่แตะโค้ด ไม่แก้ `#857` ไม่เปิดใบใหม่**

**หมุดกับการซ้อม = ผ่าน วัดซ้ำเป็นอิสระ** (นี่คือของที่รอบนี้สร้างจริง):
adversary รันเองสองสภาพ — มี sibling: 17 passed / **0 skipped** · census PASS ·
ไม่มี sibling: 16 passed / **1 skipped** · ก่อนเติมหมุด = ข้อความ `UNPINNED`
ตรงกับของ reaper แบบ byte-identical · หลังเติมหมุด = `RESULT: PASS` exit 0 ·
ชุดเต็มรูปเกต 10389 passed/133 skipped rc 0 · count 1 ถูกต้อง (`guarded_tests()`
นับ decorator ตัวเดียว ไฟล์นี้มี `@BRIDGE_GAMEDATA.skip_unless_present()` ตัวเดียว
บรรทัด 130 ไม่มี class-level guard ไม่มี `require()` ไม่มี `skipTest`) ·
ลองทำให้หมุดแดงบนสะพานสามทาง ทุกทางมีการ์ดในไฟล์เทสจับได้เอง ⇒ ไม่มีกับดัก

**ยืนยันรูของเครื่องมือ ลึกกว่าที่รอบนี้เขียนไว้ข้างบน**: ไม่ได้อยู่ที่ท่อของ
`pf_gate_preflight.py` แต่อยู่ที่ **กติกาของ census เอง** — `census()` ออก
`UNPINNED` ก็ต่อเมื่อคู่ `(key, module)` โผล่ใน `observed_pre` คือ **ต่อเมื่อมี
บรรทัด SKIPPED จริง** ⇒ หมุดที่ขาดสำหรับ precondition **ตรวจไม่ได้เลยบนสะพาน
โดยโครงสร้าง** · `check_precondition_census` ปิดรูนี้ไม่ได้เพราะมันรัน
self-test ของ census ซึ่งเดินทาง **pin → source** เท่านั้น · **ไม่มีการ์ดไหน
ในรีโปเดินทาง source → pin** (เดิน `tests/*.py` หาตัว decorate แล้วบังคับให้มีหมุด)
· `check_new_skips` ก็เห็นไม่ได้: `SKIP_MARKERS` มีแค่ `@unittest.skip`,
`@pytest.mark.skip`, `self.skipTest`, `pytest.skip(` — decorator ของบ้านเราไม่ตรงสักตัว
⇒ **เพิ่มน้ำหนักให้ข้อเสนอ (ก) ในจดหมาย `2248`** และเพิ่มทางเลือกที่ถูกที่สุด:
เขียนการ์ดใหม่ทิศ source → pin หนึ่งใบ (เร็วเป็นวินาที ไม่ต้องรัน pytest ซ้ำ)

### ของที่ต้องแก้ รอบหน้าหยิบเป็นงานแรกก่อน re-land cast 304

- 🔴 **D1 (HIGH · วัดแล้ว) — ไฟล์ข้อมูลเพี้ยน = เซิร์ฟเวอร์ไม่บูตเลย และทาง
  ปฏิเสธที่ `runtime.py` เขียนไว้ไม่มีวันได้ทำงาน**
  `world_m2_sailing_result_key.py:186` เรียก `_load_ids()` **ที่ module scope** ⇒
  `world_m2_provisioning_trial` import ต่อ ⇒ `runtime.py:32` import ต่อ ⇒
  **ทุกบูต ไม่ว่ามีแฟล็กหรือไม่ ต้อง hash ไฟล์นั้น** · adversary วัดจริง: เติม
  newline ท้าย TSV หรือย้ายไฟล์ออก ⇒ `IMPORT FAILED: SailingResultCopyError`
  `runtime.py:11831-11875` ห่อ `encode_trial_records` ด้วย try/except พร้อม
  คอมเมนต์ *"a trial that cannot compose must cost this player nothing"* —
  **โมฆะ** เพราะพังตั้งแต่ import ก่อน try จะเกิด
  แบบที่ถูกมีอยู่แล้วข้างๆ: `world_marker_copy.py` เรียก `load_copy()` **แบบ lazy
  ในแต่ละฟังก์ชัน** (357/383/416/432/463) ไม่เคยเรียกที่ module scope
  ⇒ **อันตรายที่สุดเพราะมันจะระเบิดบนเครื่อง Panya ในรอบ attended ที่มีนัดเดียว**
- 🔴 **D3 (HIGH) — ชั้นหลักฐานปนกัน: "REAL key" ยังไม่ได้พิสูจน์ว่าเป็น key จริง**
  RE-265 วัดว่า `+0x14` เป็น key เข้า store ที่สร้างจากตารางชื่อ `SAILING_RESULT`
  **แต่ไม่เคยบอกว่าคอลัมน์ไหนของตารางคือ key ของ store** · โมดูลเอาชั้น
  client-code static มาต่อกับชั้น data-table แล้วรายงานผลรวมเป็น "พิสูจน์แล้ว"
  — สองชั้นตรงกัน = consistency ไม่ใช่ proof
  **ฉากพังที่แพงที่สุด**: `GT-233` v3 ยิง `+0x14 = 1` และ `= 2` ถ้า store ไม่ได้
  keyed ด้วยคอลัมน์ `n_ID` (อาจเป็น `n_AREA`, composite, หรือ packed index ที่
  TSV export ไม่เก็บ) ⇒ null lookup ทั้งคู่ ⇒ เงียบเหมือน R318 เป๊ะ ⇒ ตาม
  `COO-DECISION 1348` (no-backup) รอบจบตรงนั้น และรายงานจะเขียนว่า "ทฤษฎี
  SAILING_RESULT key ผิด" ทั้งที่ **ยังไม่เคยถูกทดสอบ** — คือการล่มสลายเชิงวินิจฉัย
  แบบเดียวกับที่ `provisional_area_126_keys` ถูกเขียนมาเพื่อกันไว้ แต่ย้อนกลับมา
  ที่ระดับ "เลือกคอลัมน์" แทน "เลือกแถว" · ไม่มีที่ไหนติดป้ายข้อนี้ว่า `[PROPOSED]`
  corroboration ที่แข็งที่สุดที่หาได้ในรีโป: `n_ID` unique ทั่วโลก 1..138 ข้าม 6 ค่า
  `n_AREA` (สอดคล้องกับการเป็น primary key แต่ไม่ใช่การวัด)
- 🔴 **D2 (HIGH · วัดแล้ว) — เทสตัวเดียวในรีโปที่เขียนทับไฟล์ tracked ใต้ `src/`**
  `tests/test_world_m2_sailing_result_key.py:34-41` เขียนสำเนาปลอมทับ artifact จริง
  แล้ว restore ใน `finally` · adversary ฆ่า process กลางช่วงนั้น ⇒ เหลือไฟล์ tracked
  ที่ถูกแก้ค้างไว้ + `import runtime` พังทั้งทรีจนกว่าจะ `git checkout --`
  แบบที่ถูกอยู่ข้างๆ: `tests/test_world_marker_copy.py:73-79` **เปลี่ยน
  `COPY_PATH` ไปชี้ temp file** แล้วคืนค่า ไม่แตะ artifact เลย
- **D4 (MEDIUM · วัดแล้ว)** docstring บรรทัด 29-30 อ่านคอลัมน์ผิด: `n_ITEM_ID`
  ของ 18 แถวคือ **0** ไม่ใช่ 3 · เลข 3 เป็นของ `n_VARI_3` (คอลัมน์ก่อน `s_OUTFIT`)
  ย่อหน้านั้นหัวข้อ "READ RATHER THAN ASSUMED" และเป็นที่เดียวที่อธิบายว่าทำไม
  ตารางนี้เป็น per-AREA encounter table ⇒ ฐานของ fallback "ใช้ทุกแถว" ทั้งอัน
- **D5 (MEDIUM)** สำเนาที่ commit ไม่มี provenance เลย (ไม่มีชื่อต้นทาง/sha ต้นทาง/
  วันที่) `COPY_SHA256` พิสูจน์ได้แค่ "ไฟล์นี้คือไฟล์ที่ฉัน hash ครั้งล่าสุด"
  `world_marker_copy.py:291,297` เขียน sha ของ **ต้นทาง** ลงในสำเนาอยู่แล้ว —
  precedent แก้ปัญหานี้ไว้แล้ว เราไม่ได้ใช้ · (ยืนยันว่าสำเนาปัจจุบัน **ถูกต้องจริง**:
  curate จากสะพานได้ไบต์ตรงกัน · sha ต้นทางตรงกับที่ RE-265 pin ไว้เป๊ะ)
- **D6 (MEDIUM)** note ในหมุดมีสามประโยค: หนึ่งจริง (คำพูดของรอบ `wjprxa` ตรวจแล้ว
  ตรง) · หนึ่ง **ยืนยันจากในรีโปไม่ได้** (`#847` แดงด้วยขั้นเดียวกัน — SYNC-NOTICE
  บอกแค่ "Gate RED" ผมอ่าน job log ของ GitHub เอง ซึ่งไม่ได้อยู่ในรีโป ⇒ ในหมุด
  ควรติดป้ายว่ามาจาก job 101313822248 ไม่ใช่เขียนลอย) · หนึ่ง **ชี้ผิดรีโป**
  (สูตรซ้อมอยู่ใน `pf_bridge/AGENTS.md:176-181` ไม่ใช่ `AGENTS.md` ของรีโปเซิร์ฟเวอร์
  ที่คนอ่านหมุดจะ grep) ⇒ รอบหน้าแก้ถ้อยคำในหมุด (แก้กระดาษ ไม่ใช่โค้ด)
- **D7 (LOW · วัดแล้ว)** `provisional_area_126_keys` กันด้วย `len()` ไม่ใช่
  `len(set())` ทั้งที่ docstring สัญญาว่า "never picks a row twice" — ยังไม่
  เกิดจริงวันนี้ (18/18 distinct) แต่สัญญาถูกบังคับด้วยเทสข้างเคียง ไม่ใช่ตัวเอง
- **D8 (LOW)** ตัวเลขสับสนได้: trigger 153 → `+0x12`=2, `+0x14`=1 · trigger 154 →
  `+0x12`=3, `+0x14`=**2** ⇒ key ของเกาะ 3 เท่ากับ `+0x12` ของเกาะ 2 พอดี
  ถ้าเด้งใบเดียว การตีความจะไม่ falsifiable จากรอบ attended เดียว
  แก้ถูก ๆ: หยิบสอง key จากคนละปลายของช่วง id แทนสองตัวล่างสุด
- **D9 (LOW)** `curate()` กรองด้วย `n_AREA` อย่างเดียว ส่วน `n_EVENT` ของคำสั่ง COO
  ไปอยู่เป็น raise ใน `_load_ids()` ⇒ กลไกตรวจจับคือการระเบิดตอน import (= D1)
- **D10 (LOW)** `navigationex_survey_record.py:292` คอมเมนต์ยังเขียน
  `unmeasured_0x14: int = 0  # +0x14 u16, UNMEASURED` และ default ยังเป็น 0

### ที่ adversary ตรวจแล้วสะอาด (รอบหน้าไม่ต้องเสียเวลาซ้ำ)

sha pin ตรง (`5c96db08…fe55e`) · curate จากสะพานได้ไบต์เดิม · sha ต้นทางตรงกับ
RE-265 · TSV อยู่ใน git จริง · 18 ids distinct · `provisional_area_126_keys(2)`
= `(1, 2)` จริง สองระเบียนได้ key ต่างกันจริง ไม่มีศูนย์ · ไม่มีผู้บริโภคอื่นของ
default 0 เดิมนอกจาก `navigationex_survey_record` + เทส · ห้าไฟล์ที่แตะเป็น ASCII
ล้วน cp874 ได้ · ledger/coverage/compileall rc 0 · ชุดเต็มเขียวทั้งสองสภาพเครื่อง

### คำถามเดียวที่ดีไซน์ยังไม่ตอบ (ยกไปให้ COO ในจดหมาย `2310`)

**คอลัมน์ไหนของ `CONSTDATA_TH__SAILING_RESULT.tsv` คือ key ของ store ที่ client
สร้างที่ `0x0072FE50` และมีหลักฐาน static ชิ้นไหนระบุ?** ทุกอย่างปลายน้ำ —
สำเนาที่ commit, `COPY_SHA256`, ข้อโต้แย้งสองผู้สมัคร, การพลิกหัว `GT-233` —
ตั้งอยู่บนสมมติว่าเป็น `n_ID` และไม่มี artifact ในสองรีโปบอกไว้เลย

## adversary (คำสั่งเดิมที่บันทึกไว้ตอน push)

`ADVERSARY_PENDING pirate-force-server (กิ่ง claude/nifty-euler-tk4hr7)` —
สั่งไปต้นรอบพร้อมเริ่มงาน (ก่อนแตะหมุด) ให้ไล่สามเรื่อง: (1) รูปทรงหมุดที่ถูกต้อง
สำหรับ census สองทิศ (2) ทำไม preflight ถึงเขียวบนคอมมิตที่ตาย (3) เนื้องานที่
cherry-pick มา (SHA256 pin, key ต่างกันจริงสองระเบียน, ผู้บริโภคเดิมของ default 0)
ผลยังไม่คืนตอน push ⇒ push ตามกฎ **ไม่เขียนว่า "ผ่าน adversary"**
(ผลคืนแล้วตอน 23:05 — อ่านหัวข้อข้างบน ไม่ต้องสั่งซ้ำบนกิ่งนี้)

## จดหมายรอบนี้

- บริโภค: `20260905_2102_SYNC-NOTICE-*pr847*` · `20260905_2151_COO-DECISION-a847-*`
  · `20260905_2204_SYNC-NOTICE-*pr852*` (วาง `.CONSUMED.txt` ครบสามใบ · สำเนาไป `consumed/` แล้วบนดิสก์ แต่
  `consumed/` อยู่ใน `.gitignore` ของ pf_bridge ⇒ commit ได้เฉพาะ stub
  ต้นฉบับใน `notes_to_chief/` ไม่ถูกลบตามกฎ)
- ส่ง: `20260905_2248_LANE-A-TO-COO-preflight-census-is-blind-to-unpinned-skips-
  when-pf_bridge-is-present.md` (ADDRESSEE: COO)
- **ยังไม่บริโภค ยกไปรอบหน้า** (ไม่ใช่เรื่องของรอบนี้ เขียนไว้ให้ COO นับได้):
  `0805_LANE-B-TO-LANE-A-scene14-responder` · `1152_COO-DECISION-world-registry` ·
  `1506_SYNC-NOTICE-pf_bridge-pr1319` · `2052_COO-DECISION-third-admission-arm`
  (ใช้ตอน re-land cast 304) · `2056_COO-DECISION-lane-q-needs-world-registry-interface`

## รอบหน้าทำอะไร (เรียงแล้ว)

0. **D1 + D2 ก่อนอย่างอื่น** (adversary คืนหลังปลดล็อก รอบนี้แตะไม่ได้):
   ย้าย `_load_ids()` ออกจาก module scope ให้เป็น lazy ตามแบบ `world_marker_copy.py`
   (D1 = เซิร์ฟเวอร์ไม่บูตถ้าไฟล์เพี้ยน · อันตรายบนเครื่อง Panya) แล้วเปลี่ยนเทส
   D2 ให้ชี้ `COPY_PATH` ไป temp file แทนการเขียนทับ artifact จริง
   จากนั้น D4 (คอลัมน์ `n_ITEM_ID`) · D6 (ถ้อยคำในหมุด) · D7 · D10
1. วัดว่า `#857` ขึ้น main หรือยังด้วย `git merge-base --is-ancestor`
2. **re-land cast ฉาก 304 จากกิ่ง `claude/great-ride-yob0a2`** (`#847`, 19 ไฟล์
   +2978) — สาเหตุแดงรู้แล้ว: `skip_census` ตัวเดียวกัน ⇒ ตรวจว่าไฟล์เทสใหม่ของ
   ใบนั้นไฟล์ไหนบ้างที่ skip ตอนไม่มี sibling (`test_world_bg3007_identity_
   rederived.py` แน่ ๆ ตาม body ของ `#847`) เติมหมุดให้ครบ **แล้วซ้อมสองช่อง
   ก่อน push** · ตอน re-land ลบป้าย `[ASSUMPTION OF LANE A - AWAITING COO
   CONFIRMATION]` ออกจากแขนที่สาม แทนด้วย `COO-DECISION 20260905_2052`
   (COO สั่งไว้ใน `2151` ข้อ 4)
3. บล็อก `ATTENDED:` ของใบ `1953` (cast 304) — ค้างจาก `2052` ข้อ 4
4. cast ฉาก 305 (Bg3008) เป็นงานสำรอง

## Status

PR เซิร์ฟเวอร์: **`pirate-force-server#857`** เปิดแล้ว **ไม่ draft** ·
`PF-AUTOMERGE: v4` อยู่ใน body ตั้งแต่เปิด · GET ยืนยัน marker อยู่จริงแล้ว ·
**รอเกต ยังไม่อยู่บน main** (วัดรอบหน้าด้วย `--is-ancestor`)
claim `pf_bridge#1384` เติม marker เป็นขั้นสุดท้ายของรอบ (ไฟล์รอบ + จดหมาย +
stub ลงกิ่งเดียวกัน · ลบ `_claim.md` แล้ว)

## กำหนดเวลา

เริ่ม 22:22 · เพดาน 75 นาที = 23:37 · ปิดรอบก่อนเพดาน
เวลาหลักหมดไปกับสองอย่างที่จำเป็น: ซ้อมเกตไร้ sibling (9:15) และชุดเต็ม (10:07)
ซึ่งเป็นสองอย่างที่รอบก่อนข้ามไปหนึ่งอย่างแล้วเสียทั้งรอบ

SCOREBOARD: COMING | โค้ดที่ทำให้หน้า "รายงานกัปตัน" มีโอกาสเด้งเองตอนเรือชนเกาะ 2/3 (ตัวบล็อกโค้ดตัวเดียวที่เหลือของ M2) กลับขึ้น PR อีกครั้งพร้อมแก้สาเหตุที่ทำให้ใบก่อนถูกปิดทิ้ง ผู้เล่นยังไม่เห็นหน้าต่างนี้จนกว่าจะ merge + GT-233 v3 ยืนยันบนจอ | PR: pirate-force-server#857 (แทน #852), claim pf_bridge#1384, ชุดเต็ม 11353 passed/0 failed, skip_census exit=0 ในสภาพเกตจริง
