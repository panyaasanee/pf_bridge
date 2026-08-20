# FINDINGS R106 — FINDINGS R12 ถูกวัดบนเครื่องที่สองเป็นครั้งแรกในประวัติโปรเจกต์

**เขียนโดย:** chief รอบ 106 (2026-08-20 ~15:5x → 17:xx, scheduled)
**ที่ HEAD:** `7f893b8` (ก่อนแก้) — คำสั่งต้นทาง: `notes_to_chief/20260820_1545_ORDER-pytest-subset-fresh-clone-preconditions.md`
**สถานะ:** ปิดคำถามที่ R12 เปิดค้างไว้ตั้งแต่ 2026-08-17 — **ด้วยตัวเลขวัดจริง ไม่ใช่การอนุมานอีกต่อไป**

---

## 1. R12 พูดว่าอะไร และทำไมตอนนั้นยังไม่ใช่หลักฐาน

`FINDINGS_R12_GATE_NOT_REPRODUCIBLE_FROM_GIT.md` (17 ส.ค.) เขียนไว้ว่า

> gate ผ่านเพราะ **"เครื่องนี้"** ไม่ใช่เพราะ **"repo"**

ตอนนั้นวิธีวัดคือ `git archive` ลงแซนด์บ็อกซ์ Linux แล้วดูว่าอะไรหาย — **เป็นการจำลอง**
ไม่มีใครเคยรันสวีตนี้บนเครื่องอื่นจริง ๆ เลยตลอด 3 วันถัดมา คำว่า "เขียว" จึงแปลว่า
"เขียวบนแท่นของ Panya" มาตลอด และไม่มีใครรู้ว่าส่วนต่างมีขนาดเท่าไหร่

## 2. วันนี้มีตัวเลขจากเครื่องที่สองจริง

GitHub Actions **run #3** (2026-08-20, `windows-latest`, fresh clone) รัน `THE GATE` เต็มเป็นครั้งแรก
**21/22 step เขียว** เหลือแดง step เดียวคือ `pytest_subset`

| | Windows ของ Panya (บริดจ์) | runner (fresh clone) |
|---|---|---|
| ผลสวีต | **1,860 passed · 1 skipped** | **912 passed · 1,486 subtests · 4 failed** |
| artifact ที่มี | ครบทุกอย่าง | ไม่มีสักอย่าง |
| โมดูลที่ถูก `--ignore` | 0 | **42** |

**ส่วนต่างนี้คือหนี้ reproducibility ที่เหลืออยู่จริง — วัดได้แล้ว**

## 3. ทั้งสี่ตัวเป็นอาการเดียวกัน: เทสเอื้อมไปหาของที่ clone ไม่มี

| # | เทส | ของที่ขาด | อาการ |
|---|---|---|---|
| ① | `test_damage_hp_link_dispatch.py::HeadlessReplayToolTests::test_the_replay_tool_runs_clean_against_the_real_dispatcher` | canonical DB | rc 2 |
| ② | `…::test_the_replay_tools_output_is_pure_ascii` | canonical DB | `AssertionError: 2 != 0` |
| ③ | `test_multiplayer_readiness_audit.py::ExactCountTests::test_interlock_facts_match` | capture `analysis/…/LOGIN_*.txt` | `'reproduced' != 'skipped (untracked capture absent)'` |
| ④ | `test_population.py::PopulationTransitionTests::test_natural_v94_provenance_is_exact_and_read_only` | `backups/` | `FileNotFoundError` |

🔴 **กับดักการอ่าน log ที่ Panya จับได้เอง และต้องจดไว้:**
`AssertionError: 2 != 0` ของข้อ ② **ไม่ใช่จำนวนอักขระ non-ASCII** อย่างที่ชื่อเทสชวนให้คิด
มันคือ `self.assertEqual(completed.returncode, 0)` — เลข 2 มาจาก
`tools/pf_damage_hp_link_headless_replay.py:479-481` ที่คืน 2 เมื่อไม่มีไฟล์ DB
**ชื่อเทสที่บอกว่า "pure_ascii" ทำให้ log ของตัวเองอ่านผิดทาง** — บทเรียนสำหรับคนออกแบบเทส:
assert ตัวแรกในเทสควรเป็นเรื่องเดียวกับชื่อเทส ไม่งั้นข้อความล้มจะโกหกโดยไม่ตั้งใจ

## 4. ตัวที่ 4 ที่ log ไม่ได้แสดง — ยืนยันแล้วว่าเดาถูก

Panya เขียนในคำสั่งว่า *"ตัวที่ 4 ที่ไม่ได้แสดงใน log น่าจะเป็น
`test_the_replay_tool_runs_clean_against_the_real_dispatcher` — ยืนยันเองก่อนแก้"*
**ยืนยันแล้วด้วยการรันซ้ำบน clone จริง: ถูกต้อง** (ดูข้อ 5 — reproduce ได้ตรงทั้งชุด)

## 5. ⭐ การจำลอง runner ที่ตรงกันเกือบสมบูรณ์ — และนี่คือของที่มีค่าที่สุดของรอบนี้

`git clone` รีโปเต็ม ๆ ลง `/tmp` (ไม่ใช่ `git archive` — **มี `.git` จริง** ซึ่งสำคัญ เพราะเทสหลายตัว
`skipTest("not a git work tree")` และจะหลอกตัวเองถ้าใช้ archive) แล้วรันด้วย exclusion list
สูตรเดียวกับ workflow:

```
git clone <repo> /tmp/fc2
EX=$(grep -lE "GameClient|capture_v141" tests/*.py | grep -v test_foundation_legacy_seam.py)
python3 -m pytest tests -q -p no:cacheprovider $(for f in $EX; do echo --ignore $f; done)
```

ผลที่ได้: **`5 failed, 911 passed, 1486 subtests passed`**
เทียบกับ runner: **`4 failed, 912 passed, 1486 subtests`**

- **subtest ตรงเป๊ะ 1,486**
- ส่วนต่าง 1 ตัวเดียวคือ `test_server_shutdown.py::test_primary_exception_is_preserved_with_cleanup_failure`
  ซึ่งใช้ `Exception.__notes__` (ของใหม่ตั้งแต่ Python **3.11**) — แซนด์บ็อกซ์เป็น **3.10**, runner เป็น **3.14**
  ⇒ **ไม่ใช่ข้อบกพร่องของรีโป เป็นความต่างของอินเทอร์พรีเตอร์ในแซนด์บ็อกซ์**
- FAILED ทั้ง 4 ตัวตรงกันชื่อต่อชื่อ

🔴 **สรุปเชิงเครื่องมือ: ตั้งแต่วันนี้ chief มีวิธีวัด "runner จะเห็นอะไร" ได้เองในแซนด์บ็อกซ์
โดยไม่ต้อง push และไม่ต้องรอ Actions** — ค่าใช้จ่ายประมาณ 50 วินาที
**นี่คือสิ่งที่ R12 ขาดไป: ไม่ใช่ข้อสรุป แต่เป็นวิธีวัด**
เงื่อนไขที่ต้องจำ: (ก) ต้อง `git clone` ไม่ใช่ `git archive` (ข) ต้องรันใน `/tmp` **ห้ามรันบน mount ของ Windows**
เพราะสวีตจะเอื้อมถึง canonical DB ผ่าน mount (บทเรียน R41) (ค) ผลต่างที่เกิดจาก Python 3.10 vs 3.14 ต้องหักออกทุกครั้ง

## 6. ของที่ยังไม่ได้วัด และเป็นหลุมที่ใหญ่กว่าเดิม

heuristic ใน workflow ตัดทิ้ง **42 โมดูล** ด้วยการ grep คำว่า `GameClient|capture_v141`
เมื่อลองรันสวีตเต็มโดย**ไม่ใช้** `--ignore` บน fresh clone: **180 failed · 70 error**

แต่ผลสำรวจ (ลูกมือรอบนี้ วัดทีละโมดูล — `FACTPACK_R106_PYTEST_EXCLUSION_INVENTORY.md`) พบของสำคัญ:

- **9 ใน 42 โมดูลเป็น false positive ของ heuristic** — ผ่าน **100%** บน clone ที่ไม่มี artifact เลย
  7 ตัวโดนจับเพราะ docstring **เขียนว่า "no GameClient"** (คือโดนลงโทษเพราะประกาศว่าตัวเองไม่ต้องใช้)
  ⇒ **เอาออกจาก ignore list ได้ฟรี ได้เทสคืน 398 ตัวบน runner โดยไม่ต้องแก้เทสสักบรรทัด**
- ไม่มีโมดูลใดพังตอน collection เลย (890 node, 0 error) ⇒ **ไม่ต้องใช้ module-level skip กับตัวไหนทั้งสิ้น**
- 8 โมดูลที่ "ป้องกันตัวเองอยู่แล้ว" **ไม่ฟรี**: reason string ไม่มี token `[precondition:]`
  และ **4 ใน 8 ฝัง path เต็มของเครื่องไว้ในข้อความ skip** ⇒ pin ข้ามเครื่องไม่ได้แน่นอน
- 3 โมดูลใช้ `pytest.skip(allow_module_level=True)` ซ่อน `def test_` ไว้ **56 ตัว** จาก collector
  แล้วรายงานแค่ `1 skipped` — **นี่คือรูปแบบที่ census ถูกสร้างมาเพื่อจับโดยตรง**

## 7. สิ่งที่รอบ 106 ลงจริง (ดู release note ในธง / CHIEF_CONTINUATION สำหรับรายละเอียด)

- `tests/pf_preconditions.py` — ทะเบียนกลาง 7 คีย์ ทุก reason ขึ้นต้นด้วย `[precondition:<key>]`
- แก้ 4 เทสตามคำสั่ง **ด้วย `skipUnless` ที่ตัวเทส ไม่ใช่ `--ignore` ฝั่ง CI**
  และ **เพิ่มเทสที่รันบนทุกเครื่อง 3 ตัว** เพื่อไม่ให้ skip พาของที่ยังตรวจได้หายไปด้วย
- `tools/pf_pytest_precondition_census.py` + `docs/PYTEST_SKIP_PINS.json` — นับ/พิมพ์ชื่อ+เหตุผล/พินจำนวน
  **แดงทั้งขาขึ้นและขาลง** · กติกาคำนวณสด: excluded → 0 · artifact อยู่ → 0 · นอกนั้น → ค่า pin
  ⇒ **ไฟล์ pin ใบเดียวถูกต้องทั้งบนบริดจ์ (1 skip) และบน runner (4 skip) โดยไม่มีเลขที่พิมพ์มือเพื่อเครื่องใดเครื่องหนึ่ง**

## 8. 🔴 NONCLAIMS

- **"run #4 จะเขียว" เป็นคำทำนาย ไม่ใช่ผลวัด** — chief ไม่ push และไม่เห็น Actions ด้วยตาตัวเอง
  สิ่งที่วัดได้จริงคือ: fresh clone + exclusion list เดิม + Python 3.10 บน Linux = แดงเหลือตัวเดียวที่เป็นเรื่องของ 3.10
- **ไม่ได้วัดฝั่งที่ artifact มีครบบน Windows** ในแซนด์บ็อกซ์ — ฝั่งนั้นพิสูจน์ด้วย gate job บนบริดจ์เท่านั้น
- ตัวเลข 398 / 180 / 70 / 890 มาจากลูกมือที่วัดบน **Linux + Python 3.10** ⇒ ใช้เป็นแผนที่ ไม่ใช่ใบเสร็จ
- **การเลิกใช้ `--ignore` ทั้ง 42 โมดูลยังไม่ได้ทำในรอบนี้** — ดูเหตุผลที่จดไว้ใน CHIEF_CONTINUATION รอบ 106
- ไม่มี runtime observation ใหม่ ไม่มีการบูตเซิร์ฟเวอร์ ไม่มีการเปิด client ไม่แตะ canonical DB

---
---

# ✅ ภาคผนวก (เขียนโดย chief รอบ 107 · 2026-08-20 ~17:5x) — **run #4 เขียว · คำทำนายในข้อ 8 กลายเป็นผลจริง**

> **ธรรมเนียมบ้าน: ข้อความเดิมด้านบนไม่ถูกแก้แม้แต่ตัวเดียว** — ข้อ 8 ยังเขียนว่า "run #4 จะเขียวเป็นคำทำนาย"
> และมันควรอยู่อย่างนั้น เพราะตอนเขียนมันเป็นคำทำนายจริง ๆ ภาคผนวกนี้บันทึกว่ามันออกหัวหรือก้อย

## 9.1 สิ่งที่เกิดขึ้น
**Panya ยืนยันด้วยตาตัวเองจากหน้า Actions (~17:10):** **run #4 = GREEN ทั้งชุด**
`pytest_subset` เขียว · skip census เขียว · **ทุก check ผ่าน**
ที่มา: `notes_to_chief\20260820_1710_ORDER-cloud-prompt-and-sync-design.md`

## 9.2 ⭐ FINDINGS R12 ปิดได้แล้ว — เป็นครั้งแรกในประวัติโปรเจกต์

R12 (17 ส.ค.) เขียนว่า *"gate ผ่านเพราะ **เครื่องนี้** ไม่ใช่เพราะ **repo**"*
วันนี้สวีตชุดเดียวกันรันเขียวบน **เครื่องที่ไม่ใช่แท่นของ Panya** จาก **clone เปล่าที่ไม่มี artifact สักชิ้น**

| | บริดจ์ของ Panya | runner run #3 | runner run #4 |
|---|---|---|---|
| ผล | **1,860 passed · 1 skipped** | 912 passed · 1,486 subtests · **4 failed** | **เขียวหมด** |
| artifact | ครบ | ไม่มี | ไม่มี |
| skip | 1 (design) | — | **4 (precondition) นับและพินถูกต้อง** |

🔴 **ส่วนต่าง 1,860 vs 912 ยังอยู่ และยังเป็นหนี้ reproducibility** — สิ่งที่ปิดคือคำถามว่า
*"repo นี้รันได้ไหมถ้าไม่มีเครื่องของ Panya"* (**ได้**) **ไม่ใช่** *"repo นี้รันได้ครบเท่าเครื่องของ Panya ไหม"* (**ยังไม่**)
งานลดส่วนต่าง = `FACTPACK_R106_PYTEST_EXCLUSION_INVENTORY.md` (9 โมดูลแรกได้คืนฟรี 398 เทส)

## 9.3 🔴 สิ่งที่ run #4 **ไม่ได้** พิสูจน์ (nonclaims ของภาคผนวกนี้)
- **ไม่ได้พิสูจน์ว่า gate จับของจริงได้** — แดงสามครั้งที่ผ่านมาเป็นแดงที่ *บังเอิญเกิด* (plumbing · หมุดค้าง · เทสล้ม)
  กฎที่โปรเจกต์เขียนเองบอกว่าต้อง **ปลูก** ถึงจะนับ ⇒ **เช็คลิสต์ข้อ 5 ยังค้าง**
  ข้อเสนอปลูกพร้อมแล้วที่ `PROPOSAL_R107_PLANTED_RED.md`
- **chief ไม่ได้เห็นหน้า Actions ด้วยตาตัวเอง** — บรรทัด "GREEN" นี้เป็น **คำบอกเล่าของ Panya** ซึ่งเชื่อถือได้
  ตามนโยบายข้อ 12 แต่ **ไม่ใช่ log ที่ chief อ่านเอง** · log ตัวจริงยังไม่ถูกเก็บลง repo
- **ตัวเลข "22 check" ที่ใบสั่งอ้าง ยังไม่ถูกยืนยัน** — ลูกมือรอบ 107 นับตาราง `GATE SUMMARY` ที่ pin=0 ได้ **23 แถว**
  ⇒ **ก่อนอ้างเลข 22 ที่ไหนอีก ให้เทียบกับ log ของ run #4 ก่อน**
- **cp874 ยังถูกจับชั้นเดียวบน CI ไม่ใช่สองชั้น** — `tests/test_names_fold003_thunk_census.py::Cp874ConsoleGateTests`
  (ตะแกรงที่สแกนทั้ง `tools/`) ยังติดตัวกรอง `GameClient|capture_v141` จึงถูก `--ignore` ออก
  ⇒ บนบริดจ์จับสองชั้น **บน runner จับชั้นเดียว** (static tripwire ของ workflow เท่านั้น)
- **`README_GATE_CI.md` มีสองจุดที่ต้องแก้** (พบระหว่างร่างข้อเสนอปลูกแดง): recipe เขียน `git checkout master`
  ทั้งที่ repo มีแต่ `main` · และ recipe 2 ทำนายว่าจะเห็น "แดงสองช่อง" ทั้งที่ Actions หยุด job
  ที่ step แรกที่ล้มและ workflow ไม่มี `if: always()` ⇒ **เห็นได้ช่องเดียวเสมอ**
