# 🔴 คำสั่ง Panya 2026-08-20 ~15:45 — Actions run #3: **21/22 เขียว · เหลือ `pytest_subset` ตัวเดียว**

## สถานะ run #3 — ก้าวใหญ่
`THE GATE` **รันเต็มเป็นครั้งแรก 3 นาที 50 วินาที** · หมุดสองตัวที่รอบ 105 แก้ **เขียวทั้งคู่**
(`coverage_debt` exit=0 · `coverage` exit=0) · `release_determinism` build A/B sha ตรงกันเป๊ะ
`replayx exit=2 expect=2 GREEN` (พินค่าที่ไม่ใช่ศูนย์ทำงานถูก)

**แดงตัวเดียว: `pytest_subset exit=1 expect=0`** → `4 failed, 912 passed, 1486 subtests passed in 217s`

---

## 🔴 ทั้งสี่ตัวเป็นอาการเดียวกัน: **เทสต้องการของที่ fresh clone ไม่มี**

### ① `tests/test_damage_hp_link_dispatch.py::HeadlessReplayToolTests::test_the_replay_tools_output_is_pure_ascii`
```
AssertionError: 2 != 0
```
🔴 **อ่านให้ถูก: `2` คือ return code ไม่ใช่จำนวนอักขระ** — บรรทัดที่ล้มคือ
`self.assertEqual(completed.returncode, 0)` (บรรทัด 933) **ไม่ใช่** ข้อ assert เรื่อง ASCII
ต้นทางของเลข 2 อยู่ที่ `tools/pf_damage_hp_link_headless_replay.py:479-481`:
```python
if not db_source.is_file():
    print("no database file at %s" % ascii(str(db_source)))
    return 2
```
⇒ `DEFAULT_DB` = canonical `state/pirateforce.sqlite3` ซึ่ง **`.gitignore` กันไว้ ไม่มีทางอยู่ใน clone**
⚠️ **ตัวที่ 4 ที่ไม่ได้แสดงใน log น่าจะเป็น `test_the_replay_tool_runs_clean_against_the_real_dispatcher`
ในคลาสเดียวกัน** (เรียก `_run()` แล้ว assert returncode 0 เหมือนกัน) — ยืนยันเองก่อนแก้

### ② `tests/test_multiplayer_readiness_audit.py::ExactCountTests::test_interlock_facts_match`
```
SUBFAILED(key='login_req_capture_guard')  'reproduced' != 'skipped (untracked capture absent)'
```
⇒ ตัว audit **รายงานตัวเองอย่างซื่อสัตย์แล้วว่า capture ไม่อยู่** แต่เทสพินสตริง `reproduced` ตายตัว

### ③ `tests/test_population.py::PopulationTransitionTests::test_natural_v94_provenance_is_exact_and_read_only`
```
FileNotFoundError: 'D:\a\...\backups\v94_runtime_before_v95_20260814_003000\capture_v94\GAME_...txt'
```
⇒ `backups/` ไม่อยู่ในรีโป

---

## ⭐ นี่คือ **FINDINGS R12 ถูกวัดบนเครื่องที่สองเป็นครั้งแรกในประวัติโปรเจกต์**
R12 เขียนไว้เมื่อ 17 ส.ค. ว่า *"gate ผ่านเพราะ 'เครื่องนี้' ไม่ใช่เพราะ 'repo'"* แต่ตอนนั้นวัดด้วย
`git archive` ในแซนด์บ็อกซ์ · **วันนี้มีตัวเลขจริงจากเครื่องของ GitHub:**

| | Windows ของ Panya | runner (fresh clone) |
|---|---|---|
| ผล | **1,860 passed 1 skipped** | **912 passed · 1,486 subtests · 4 failed** |

⇒ ส่วนต่างนี้คือ **หนี้ reproducibility ที่เหลืออยู่จริง** วัดได้แล้ว ไม่ใช่การคาดเดาอีกต่อไป
**บันทึกเป็น FINDINGS ใหม่ อย่าปล่อยให้เป็นแค่บรรทัดใน continuation**

---

## 🔴 วิธีแก้ที่ Panya ต้องการ — **แก้ที่ตัวเทส ไม่ใช่เพิ่ม ignore list ฝั่ง CI**

**หลักการ:** เทสต้องรู้เงื่อนไขนำเข้าของตัวเอง และ **ประกาศว่ามันข้าม** — บน *ทุก* เครื่อง
ไม่ใช่ให้ workflow เอาไปซ่อนไว้ในรายการ `--ignore` ซึ่งทำให้บน runner มัน **หายไปเงียบ ๆ**
ขณะที่สวีตยังรายงานตัวเลขเหมือนเดิม

**ท่านี้มีใช้อยู่แล้วในรีโปนี้** — คลาสเดียวกันนั้นเองใช้
`@unittest.skipUnless(REPLAY_TOOL.exists(), "...is not written yet")` ⇒ **ขยายท่าเดิม ไม่ใช่คิดท่าใหม่**
- ① → `skipUnless(DEFAULT_DB.exists(), "canonical DB is not in a fresh clone")`
- ② → เทสต้อง **ยังบังคับ `reproduced` เมื่อ capture มีอยู่** และยอมรับ `skipped (...)` เฉพาะเมื่อไฟล์ไม่มีจริง
  🔴 **ห้ามแก้ให้ยอมรับ `skipped` แบบไม่มีเงื่อนไข** — นั่นคือการทำให้เทสอ่อนลงบนเครื่องของ Panya ด้วย
- ③ → `skipUnless(backup path exists, "backups/ is machine-local")`

## 🔴 ข้อบังคับสองข้อ (เรียนจากหมุดค้างยุคสองตัวเมื่อกี้)
1. **skip ต้องถูกนับและพิมพ์ชื่อ+เหตุผล** ในสรุปของ `THE GATE` — *"a skipped check is not a passed check"*
   เป็นคำของ chief เอง · ตอนนี้ `1 skipped` บน Windows จะกลายเป็นหลายตัว ⇒ ต้องเห็นว่าตัวไหน
2. **พินจำนวน skip ไว้** เหมือน `COVERAGE_EVIDENCE_DEBT_PIN` ⇒ **แดงถ้ามันขยับ ทั้งขึ้นและลง**
   ไม่งั้นวันหนึ่งจะมีเทสหลุดไปอยู่ในกอง skip โดยไม่มีใครรู้

## ⚠️ ก่อนแก้ ให้กวาดทั้งสวีตในรอบเดียว
อย่าแก้แค่ 4 ตัวที่ล้มวันนี้ — **หาให้ครบว่ามีเทสอีกกี่ตัวที่พึ่งของนอกรีโป**
(`state/` · `backups/` · `reports/` · capture corpus · client image · `../pf_bridge/`)
ผมเห็นอย่างน้อย: `test_structural_corpus_audit.py` · `test_single_session_limitation.py` ·
`test_functional_coverage.py` · `test_hp_death_respawn_static.py` อ้าง `reports/`
และ `tools/pf_vital_name_thunk_static.py:127` ใช้ `ROOT.parent / "pf_bridge"` (ยังไม่ระเบิดวันนี้ แต่จะระเบิด)
⇒ **run #4 ต้องไม่แดงด้วยเรื่องเดียวกันอีก** เหมือนที่ run #3 ไม่แดงซ้ำหมุดเพราะรอบ 105 กวาดครบ

## ขอบเขต
แก้เรื่องนี้อย่างเดียว · **ห้าม push** (Panya push เอง) · เสร็จแล้วจบรอบ
🔴 **ห้ามแก้ด้วยการลบเทสหรือลดความเข้มของ assert บนเครื่องที่มีของครบ**
