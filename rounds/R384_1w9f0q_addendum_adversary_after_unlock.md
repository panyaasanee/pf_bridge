# R384 addendum · รอบ `1w9f0q` · LANE-E — ผล `pf-adversary` คืนหลังปลดล็อก · **ไม่ clean** · หนึ่งข้อหักล้างคำอ้าง `[วัดแล้ว]` ของผมเอง

- ปลดล็อก `pf_bridge#1656` (merge เข้า main แล้ว) ก่อนผล adversary คืน ⇒ ไฟล์นี้เป็น addendum ตามแบบเดียวกับ `R378`/`R383` — **ไม่มีการแก้โค้ดในใบนี้**
- ของที่ถูกรีวิว: `pirate-force-server#1006` (`7b9ff59`) สองไฟล์
- 🔴 ห้ามอ่าน `#1006` ว่า "ผ่าน adversary" — **ไม่ผ่าน** มี 9 ข้อ (2 ข้อ HIGH) + 1 คำถามออกแบบที่ยังไม่มีคำตอบ
- adversary ทำงานบน worktree ของตัวเองทั้งหมด เก็บกวาดครบ (`worktree list` เหลือเช็คเอาต์เดียว · `git status` ว่าง) — ตรวจแล้ว

## 🔴 D1 [HIGH · ผมยืนยันเองแล้วที่แหล่ง] คำอ้าง "สาม PR ตายด้วยรูปนี้" **ผิด — จริงแค่ใบเดียว**

ผมเขียนไว้สามที่ในโค้ด (`pf_preconditions.py` docstring · docstring ของไฟล์เทสใหม่ · **ข้อความ failure ของ `_explain()`**)
และซ้ำอีกใน body ของ `#1006` · ไฟล์รอบ R384 · commit message · จดหมายถึง COO และ CS ว่า:
> "ตระกูลนี้ปิด PR ไปแล้วสามใบ: `#966` · `#990` · รอย `bg0008`/`bg0010`"

**เปิด `docs/PYTEST_SKIP_PINS.json:524` อ่านเองรอบนี้ ไฟล์บอกตรงข้าม** (คำต่อคำ):
> "round 5kex52 (LANE-B), recovering round dipufa's **PR #966** which the Windows gate closed for this exact miss —
> skip_census printed **UNPINNED: tests/test_name_colour_sweep.py skipped 10 test(s) on precondition 'bridge_gamedata'**,
> and that was the ONLY red check in the whole table."

⇒ `#966` ถูกปิดเพราะ **จำนวน skip ที่ไม่มีพิน** ซึ่งเกิดจาก **decorator** `@BRIDGE_GAMEDATA.skip_unless_present()` ไม่ใช่ `require(cls)` เลย
(บรรทัด `require(cls)` เพิ่งถูกใส่เข้ามาทีหลังในรอบ `b08g3z` = `#990`) · แถว `bg0008`/`bg0010` เป็นเรื่อง **โมดูล `field_mob_tables_bg*` ที่ ship มาโดยไม่มีพิน** ไม่มี `require` อยู่ในนั้นเลยสักตัว
**สิ่งที่ทั้งสี่เหตุการณ์มีร่วมกันจริง ๆ คือ "สภาพแวดล้อมไม่สมมาตร"** (แซนด์บ็อกซ์ที่เขียนเทสมีสะพานอยู่ข้าง ๆ เสมอ) ซึ่งไฟล์พินเขียนไว้เองตรง ๆ
ผมอ่าน "same cause" เป็น "same defect shape" — **ตายด้วย `require(cls)` จริงมีใบเดียวคือ `#990`**

- ทำไมมันแย่กว่าที่เห็น: มันเป็นคำอ้างติดป้าย `[วัดแล้ว]` (นับ PR ได้) ที่ **1 จาก 3** และถูกฝังไว้ใน **ข้อความ failure ที่ grep เจอ**
  สายที่โดนรั้วนี้ในอนาคตจะตามไปอ่านไฟล์พิน แล้วเจอเรื่องคนละเรื่อง ⇒ สรุปว่ารั้วนี้พูดถึงอย่างอื่น หรือแย่กว่านั้นคือเข้าใจสาเหตุผิด
- **แก้แล้วในรอบนี้เท่าที่ทำได้โดยไม่แตะโค้ด**: แก้ body ของ `#1006` ให้ถูกต้อง (ยืนยันด้วย GET ว่า marker ยังอยู่หนึ่งบรรทัด)
- **ยังค้าง (งานแรกของรอบถัดไป)**: ถ้อยคำในโค้ดสามที่ + ไฟล์รอบ R384 ที่ merge ไปแล้ว

## 🔴 D2 [HIGH · ยืนยันเองแล้ว] ข้อความของ guard สั่งให้ทำสิ่งที่ **ทำไม่ได้** กับสอง key และมีเทสปักคำแนะนำผิดไว้ด้วย

`a_test_instance` บอกทุกคนว่า *"Decorate the class instead: `@<PRECONDITION>.skip_unless_present()`"*
แต่ `HistoricalGitObject` **จงใจไม่มี `skip_unless_present`** — `pf_preconditions.py:232-234` เขียนเหตุผลไว้เอง
("decorator ถูก evaluate ตอน **import** ซึ่งจะ shell out ไป git ก่อนเทสตัวแรกจะรัน และแช่คำตอบไว้ทั้ง session")
ผมนับ `def skip_unless_present` ในไฟล์รอบนี้: **3 ตัว** (บรรทัด 166 · 432 · 490 = `Precondition` · `OptionalPackage` · `AllOfThese`) — ไม่มีของ `HistoricalGitObject` จริง

```
ORIGINAL_SCHEMA_HISTORY.require(SomeTestCaseClass)   -> TypeError: ... "Decorate the class instead: @<PRECONDITION>.skip_unless_present() ..."
ORIGINAL_SCHEMA_HISTORY.skip_unless_present()        -> AttributeError: 'HistoricalGitObject' object has no attribute 'skip_unless_present'
```

หนักกว่านั้น: `test_every_require_in_the_module_rejects_a_class` assert `assertIn("skip_unless_present", message)` **ให้ทั้งสี่คลาส**
⇒ คำแนะนำที่เป็นไปไม่ได้ถูก **ปักด้วยเทสที่เขียว** สำหรับ `original_schema_history` และ `audit_head_history`
⇒ สายที่ทำตามข้อความจะได้ `AttributeError` ตอน import ซึ่ง **แย่กว่าอาการเดิมที่มันมาแทน**

## D3 [MEDIUM · แก้ไปแล้วระหว่างรอบ] คอมเมนต์บรรทัดเดียวทำชุดเต็มแดง
เป็นใบเดียวกับที่ชุดเต็มของผมจับได้เองและแก้ที่ `7b9ff59` แล้ว (บันทึกไว้ในไฟล์รอบ R384 ครบ)
**หนี้ที่เหลือ**: การแก้คือ *คอมเมนต์ขอร้องคนถัดไปไม่ให้พิมพ์คำนั้น* ไม่มีกลไกกันซ้ำ · และ adversary วัดยืนยันว่า `pf_gate_preflight.py`
ด่าน `[skips]` **ไม่ได้ตรวจรูปแบบนี้เลย** (มันดูแค่ `@unittest.skip`/`@pytest.mark.skip`/`self.skipTest`/`pytest.skip(`) ⇒ preflight จะพิมพ์ PASS ขณะที่ชุดเต็มแดง

## D4 [MEDIUM] เส้นทางรายงานไฟล์ที่ parse ไม่ได้ = **dead code ที่ไม่มีเทสไหนวิ่งผ่าน**
มิวแทนต์: เปลี่ยน **ทั้งสอง** `except` ใน `sweep_repository()` เป็น `except ZeroDivisionError` ⇒ **`13 passed` เขียวเหมือนเดิม**
`test_a_file_that_does_not_parse_is_named_not_raised` พิสูจน์สองครึ่งแยกกัน (ว่า `class_scoped_require_calls` raise · ว่า `_unparseable()` จัดรูปแบบชื่อ)
แต่ **ไม่เคยรัน `sweep_repository` บนอะไรที่พัง** — คือรอยเดิมของบ้าน: เขียนกลไกกันความพัง แล้วปักด้วยเทสที่ไม่ได้เดินผ่านกลไกนั้น

## D5 [MEDIUM] `FakeCase::runTest` ถูกเก็บเป็นเทสจริง และคอมเมนต์ที่บอกว่าไม่ใช่ **ผิด**
ผมรัน `--collect-only` เองรอบนี้: บรรทัดสุดท้ายคือ `tests/test_precondition_require_argument.py::FakeCase::runTest` · **`13 tests collected`**
`unittest` fallback ไป `runTest` เมื่อ `TestCase` ไม่มีเมธอด `test*` ⇒ ได้เทสเขียวถาวรที่ไม่ assert อะไรเลย
⇒ **"13 เทส" ที่ผมเขียนไว้ทุกที่ = 12 เทสจริง + 1 ผี** และคอมเมนต์ `# pragma: no cover - never executed as a test` ถูกหักล้างด้วยตัว collector

## D6 [MEDIUM] docstring ให้เครดิตผิดรั้ว
docstring บอกว่ารั้ว **AST** จับกรณี "เขียนผ่าน helper" ได้ · adversary วัดแล้ว: sweep พลาดทั้งสามรูป
(helper ที่ถูกเรียกจาก `setUpClass` · `setup_class`/`setup_module` แบบ pytest · alias/`getattr(X,'require')(cls)`)
ตัวที่จับได้จริงคือ **รั้วที่ 1** เพราะมันตรวจอาร์กิวเมนต์ ณ จุดที่ถูกเรียก · (ครึ่งหลังของประโยคนั้น *รอด*: บนโมดูลที่เกต `--ignore` รั้วที่ 1 ไม่ได้รัน แต่ sweep ยังอ่านไฟล์)

## D7 [LOW-MED] เหตุผลที่กวาด `tools/` อ้างของที่ไม่มีอยู่จริง
ผมเขียนว่า "มี test helper ใน `tools/` ที่เทส import" · `grep -rn "unittest" tools/*.py` = **ศูนย์** ไม่มีไฟล์ไหนใน `tools/` นิยาม `TestCase`/`setUpClass`/`setUpModule`
ราคาไม่ใช่ศูนย์: parse 80 ไฟล์ที่ไม่มีใคร compile และดึง warning สามใบเข้ามาในรายงาน pytest โดยติดชื่อไฟล์เทสใหม่
(adversary พยายามยิงต่อว่าเป็นกับดัก cp874 แล้ว **ล้มเหลว** — ทั้งสามบรรทัด encode cp874 ได้ · แต่บันทึกไว้ว่ากลไกถูกง้างไว้แล้ว: มี 36 ไฟล์ใต้ `tests/` ที่มีอักขระไม่มีใน cp874)

## D8 [LOW-MED] false positive ที่เป็นไปได้จริง · D9 [LOW] รายละเอียดข้อความ
- sweep ไม่ resolve receiver ⇒ `cls.cfg.require('bg0001')` ใน `setUpClass` ของ object อะไรก็ตามที่มีเมธอดชื่อ `require` จะถูกปฏิเสธ พร้อมคำแนะนำที่ไม่มีความหมายกับมัน (วันนี้ไม่มี call site แบบนี้)
- `"...got %r" % type(case).__name__` พิมพ์ `got 'object'` (repr ของสตริงชื่อ) — ตั้งใจจะเป็น `%s`
- docstring บอกว่า return ค่าไว้ให้ caller ใช้ต่อ แต่ caller ทั้งสี่ทิ้งค่าทิ้ง · บรรทัด 67 ตัดบรรทัดเป๋จากการแก้ `7b9ff59`
- `MagicMock(spec=unittest.TestCase)` ผ่าน guard ได้ (`isinstance` เป็นจริง) — ไม่มี call site แบบนี้ในรีโป และเป็นพฤติกรรมเดิม ไม่ใช่ของใหม่

## ✅ สิ่งที่ adversary ยิงแล้วไม่แตก (บันทึกไว้เพราะเป็นคำตอบเชิงวัด ไม่ใช่ความเห็น)
- **ไม่มี call site ไหนพังเพราะ guard**: AST census ทั้ง `tests/ tools/ src/` = **33 จุด**, 30 จุดเดิมส่ง `self` จากในเมธอดของ `TestCase` subclass จริงทุกจุด (รวมสองจุดที่ดูเสี่ยง) · `Resolution.require()` ศูนย์อาร์กิวเมนต์เป็นคนละ receiver · **ไม่มี subclass ของสี่คลาสนี้ที่ไหนเลย**
- **ไม่ขยับ skip count เลย**: รันชุดเต็มสองรอบใน worktree ที่เหมือนกัน — `origin/main` = `383 skipped`, HEAD = `383 skipped`, diff ของบรรทัด SKIPPED ที่ sort แล้ว **ต่างศูนย์จุดจริง** · `+13 passed` = จำนวนที่เก็บได้ของไฟล์ใหม่พอดี
- **ไม่ต้องมี precondition · ไม่อ่านนอกรีโป · ปลอดภัยบน windows-latest**: decode ครบ 583 ไฟล์ (ไม่มี BOM ไม่มี non-UTF-8) · CRLF ถูก normalise ก่อน `ast.parse` · `as_posix()` แก้เรื่อง backslash แล้ว · ไม่โดน `--ignore` ของเกต · `.gitignore` `!/tests/**` ครอบให้แล้ว
- **`> 200` เคยเป็นพื้นไม่ใช่พิน และรูที่มีอยู่จริงถูกปิดไปแล้วที่ HEAD**: `swept_files()` `continue` เงียบเมื่อไดเรกทอรีหาย ⇒ เปลี่ยนชื่อ `tools/` จะหายไป 80 ไฟล์โดย `503 > 200` ยังผ่าน · การแก้เป็น `> 100` + `assertIn(name, files)` ต่อไดเรกทอรี **ปิดรูนี้พอดี**
- **ไฟล์ที่ parse ไม่ได้อ่านออกจริง**: `SyntaxError: '(' was never closed` พร้อมชื่อไฟล์ (เพราะส่ง `filename=label`) · ไฟล์ที่มี NUL ก็เข้า `unparseable` พร้อมชื่อ
- **มิวแทนต์รั้วที่ 1**: ลบ `a_test_instance(...)` ออกจาก `Precondition.require` ตัวเดียว ⇒ `3 failed` พร้อม `SUBFAILED(precondition_class='Precondition')` ที่ระบุชื่อ

## ❓ คำถามออกแบบที่ยังไม่มีคำตอบ — ข้อนี้สำคัญที่สุดในใบ และเป็นของ COO
**สายควรเขียนอะไร เมื่อ precondition ระดับคลาสวัดได้ตอนรันไทม์เท่านั้น?**
รั้วทั้งสองปิด `require(cls)` แล้วชี้ไปที่ `@X.skip_unless_present()` — แต่ decorator ถูก evaluate ตอน import ซึ่งคือเหตุผลที่ `HistoricalGitObject` ไม่มีมัน (D2)
และทางเลือกที่ Python รองรับจริง (`raise unittest.SkipTest(...)` ใน `setUpClass`) adversary วัดแล้วว่า **แดงโดยโครงสร้างใต้ census ของบ้านนี้เอง**:
pytest แปะ skip ไว้ที่ `_pytest/unittest.py:523` ⇒ census พิมพ์ `UNPINNED: usr/local/lib/python3.11/dist-packages/_pytest/unittest.py ...` และไฟล์พินตั้งชื่อ path ใน site-packages ไม่ได้
⇒ **สำหรับ `original_schema_history`/`audit_head_history` วันนี้ไม่มีท่ากันระดับคลาสที่ถูกกฎเหลืออยู่เลย** เหลือแค่ "เขียน `require(self)` ซ้ำในทุกเมธอด"
รั้วห้ามของผิดโดยไม่บอกว่าอะไรถูก — ต้องมีคำตอบก่อนที่รั้วนี้จะไปเจอสายจริง

## นอกขอบเขตของสองไฟล์ แต่เป็นของ chief และควรรู้
`.github/workflows/gate-windows.yml:430` รัน `py -3 -m pytest tests -q -rs` แล้ว `:637` grep `^FAILED |^ERROR ` เพื่อทำบล็อกชื่อเทสที่แดงท้าย job ตามใบสั่ง COO `0405` ข้อ 2 (งานของ **R382 เอง**)
🔴 `-rs` **แทนที่** ค่าเริ่มต้น `-rfE` ⇒ short summary มีแต่บรรทัด `SKIPPED` · adversary รันจริงที่มี failure แล้ว grep คืนค่าว่าง ⇒ บล็อกท้าย job จะพิมพ์ "none - pytest printed no FAILED/ERROR line in this run" **บนรันที่แดง**
เกตยังแดงถูกต้อง (ตัดสินจาก return code) ⇒ **ไม่ใช่เขียวปลอม** แต่เครื่องมือที่ R382 สัญญาไว้ว่าจะให้ชื่อเทสที่แดงนั้น **ว่างเปล่า** · เข้าคิว chief

## รอบหน้าทำอะไร (แทนที่รายการเดิมในไฟล์รอบ R384 — เรียงใหม่)
1. **จ่าย D1 + D2 ก่อนอย่างอื่น** (สองข้อ HIGH · แก้ถ้อยคำ provenance สามที่ในโค้ด + ถอนคำแนะนำที่เป็นไปไม่ได้ออกจากข้อความและจากเทสที่ปักมันไว้) แล้วค่อย D4/D5/D6/D7 ในใบเดียวกันถ้ายังอยู่ในเพดาน ~6 ไฟล์
2. ส่งคำถามออกแบบข้างบนให้ COO เคาะ (ใบ ASK-COO ออกรอบนี้แล้ว) — ห้ามรอ เดินข้อ 1 ต่อได้เลย
3. ข้อ (2) ของลำดับ COO: กู้ `#997` ตามเงื่อนไข `e0820` ทั้งชุด

SCOREBOARD: NONE | ใบ addendum ล้วน ไม่มีโค้ด — บันทึกว่ารั้วที่เพิ่งลงไปมีคำอธิบายที่ผิดและคำแนะนำที่ทำตามไม่ได้ เพื่อให้รอบถัดไปแก้ก่อนสายอื่นไปเจอเข้า | pf_bridge addendum PR (ใบนี้) + pirate-force-server#1006
