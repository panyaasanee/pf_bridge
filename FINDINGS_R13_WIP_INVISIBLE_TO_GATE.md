# FINDINGS R13 — WIP 187 บรรทัด "มองไม่เห็น" จากมุมของ gate

รอบ idle ครั้งที่ 13 · 2026-08-17 09:07–09:1x ICT · Claude (Cowork, `pirate-force-chief-continue`)
**read-only ต่อ repo 100%** — เขียนเฉพาะใน `pf_bridge\` · ไม่เปิด GameClient · ไม่รัน server

---

## คำถามของรอบนี้

รอบ 12 ถามว่า *"ถ้า `git clone` แล้วรัน gate ผ่านไหม"* คำตอบคือไม่ผ่านเพราะไฟล์นอก git

รอบนี้ถามคำถามคนละแกนที่ไม่มีใครเคยถาม และแรงกว่าในเชิงผลลัพธ์:

> **gate ที่รายงานเขียว `384 tests exit 0` (M14) รันบน worktree ซึ่ง = HEAD + WIP 187 บรรทัด
> ที่ยังไม่ commit — แล้ว HEAD เพียว ๆ (สิ่งที่ repo ถือจริง) ให้ผลต่างไหม**

ถ้าต่าง → เกรดเขียวขึ้นอยู่กับของที่ยังไม่ commit (เปราะมาก)
ถ้าไม่ต่าง → ต้องถามต่อว่า *แล้วอะไรในสวีตที่มองเห็น WIP บ้าง*

---

## วิธี (differential + mutation ตามระเบียบที่ M14 วางไว้)

สร้าง 2 ต้นไม้ใน `/tmp/r13` — **ไม่ clone ไม่สร้าง worktree ไม่แตะ repo**

| ต้นไม้ | ที่มา |
|---|---|
| `head` | `git archive HEAD` (209 ไฟล์) + คืนไฟล์นอก git ที่ gate ต้องการจาก bundle รอบ 10 + รอบ 12 (33 reports + 2 backups + 6 evidence) → 250 ไฟล์ |
| `wip` | สำเนาของ `head` + `patch -p1 < backup\main_dirty_20260817_0752_lf_verified.patch` |

**ตรวจความถูกต้องของต้นไม้ `wip` ก่อนใช้:** เทียบ `cmp` กับ worktree จริงทีละไฟล์
→ **byte-identical ครบ 6/6** (`docs/AI_WORKSPACE_LEASE.json`, `inventory.py`, `lifecycle.py`,
`repository.py`, `session.py`, `store.py`) — เป็นการยืนยันเส้นทางกู้ WIP **ครั้งที่ 4**
ด้วยเครื่องมือคนละตัว (`patch(1)` ไม่ใช่ `git apply`) และ sha ของ patch ยังเป็น `a80b3374…`

---

## FACT เกรด A — สิ่งที่วัดได้ตรง ๆ

### A1 — HEAD เพียว กับ HEAD+WIP ให้ผล **เหมือนกันทุกประการ**

```
head : Ran 337 tests — FAILED (errors=14, failures=0)
wip  : Ran 337 tests — FAILED (errors=14, failures=0)
diff ของเซ็ตชื่อเทสที่ ERROR/FAIL  →  ว่างเปล่า (IDENTICAL)
```

14 ตัวที่ error เป็นข้อจำกัดของ sandbox ล้วน (ตรงกับที่รอบ 12 แยกไว้):
9 = `capstone`/`pefile` ไม่มี · 3 = ต้องมี `GameClient.bin` · 1 = `Exception.__notes__` (Python ≥ 3.11) ·
1 = `git show 5c200e2:…` (ต้องมี `.git`) — **ไม่มีตัวไหนเป็นบั๊กของโค้ด และไม่มีตัวไหนเกี่ยวกับ WIP**

> 🟢 **ข่าวดี:** commit WIP ตอนนี้ **ทำ gate พังไม่ได้** — มันไม่เปลี่ยนผลเทสสักตัว
> 🔴 **ข่าวร้ายที่เป็นอีกด้านของเหรียญเดียวกัน:** gate **แยก HEAD กับ HEAD+WIP ไม่ออก**
> → เขียว 384 ที่รายงานไว้ **ไม่ใช่หลักฐานอะไรเลยเกี่ยวกับงาน M3 ที่ค้างอยู่**

### A2 — บรรทัดใหม่ 168 บรรทัด ถูกรันจริงแค่ **11 บรรทัด (6.5%)**

วัดด้วย `sys.settrace` + `threading.settrace` เก็บเฉพาะไฟล์ใต้ `src/pirateforce_foundation/`
(นับเฉพาะบรรทัดที่เป็นโค้ดจริง ตัดบรรทัดว่าง/คอมเมนต์ออกแล้ว)

| ไฟล์ | บรรทัดโค้ดที่เพิ่ม | ถูกรัน | % |
|---|---:|---:|---:|
| `inventory.py` | 93 | 10 | 10.8% |
| `session.py` | 23 | 1 | 4.3% |
| `store.py` | 42 | **0** | **0.0%** |
| `lifecycle.py` | 6 | **0** | **0.0%** |
| `repository.py` | 4 | **0** | **0.0%** |
| **รวม** | **168** | **11** | **6.5%** |

11 บรรทัดที่ถูกรัน = `_item_content_signature`, allowlist raise, `is_unmoved_baseline`
และ guard บรรทัดเดียวใน `session.py:39` — **คือส่วน "ยาม" ทั้งหมด ไม่ใช่ส่วน "ฟีเจอร์"**

### A3 — mutation: 11 บรรทัดที่ถูกรันนั้น **มีคนเฝ้าจริง 3/3**

| mutation | ผล | เทสที่จับได้ |
|---|---|---|
| `inventory.py:129` allowlist → `if False:` | 🟢 จับได้ | `test_item_lifecycle.ItemLifecycleTests.test_unknown_persisted_shape_and_read_only_mutation_reject` |
| `is_unmoved_baseline` → `return True` | 🟢 จับได้ | `test_item_move_hypothesis…test_reconnect_projection_is_opt_in_and_baseline_fails_closed` |
| `session.py:39` guard → `if False:` | 🟢 จับได้ | (ตัวเดียวกับข้างบน) |

**แต่** — เทสทั้งสองตัวนี้เป็นเทส **ที่มีอยู่ก่อนแล้ว** และเฝ้า *implementation เก่าของ HEAD* อยู่ด้วย
(HEAD เขียน guard เป็น `backpack == HYPOTHESIZED_V111_SLOT2_BACKPACK`,
WIP เขียนใหม่เป็น `not is_unmoved_baseline(backpack)`) → เทสพอใจกับทั้งสองแบบ
**จึงพิสูจน์ได้แค่ว่า refactor ไม่ทำสัญญาเดิมพัง ไม่ได้พิสูจน์พฤติกรรมใหม่เลย**

### A4 — canary: **ไม่มีเทสสักตัวใน 337 ที่เรียกฟีเจอร์ M3 เข้าไป**

ใส่ `raise AssertionError("R13-CANARY")` เป็นบรรทัดแรกของ
`store.move_backpack_item_to_free_slot` **และ** `lifecycle.move_backpack_item_to_free_slot`
(ครอบ chain `session → lifecycle → store` ทั้งเส้น) แล้วรันสวีตเต็ม:

```
canary : Ran 337 — FAILED (errors=14)      เซ็ตที่พังเทียบกับ baseline = IDENTICAL
control: Ran 337 — FAILED (errors=36)      (canary วางบนบรรทัดที่พิสูจน์แล้วว่าถูกรัน)
```

**control พังเพิ่ม 22 ตัว → harness ตรวจจับโค้ดที่ถูกเรียกได้แน่นอน**
ดังนั้นการที่ canary **ไม่ขยับอะไรเลย** เป็นผลลบที่เชื่อถือได้:
**entry point ของ M3 ทั้ง 52 บรรทัด (`store` 42 + `lifecycle` 6 + `repository` 4)
ไม่ถูกเรียกโดยเทสตัวใดเลย**

### A5 — ยืนยันซ้ำแบบ static บน Windows (job 036)

`git grep move_backpack_item_to_free_slot -- src tests scenarios docs tools` → **7 hit ทั้งหมดอยู่ใน `src/` เท่านั้น**
(`lifecycle.py:74,77` · `repository.py:26` · `session.py:74,83,162` · `store.py:354`)
→ **`tests/` `scenarios/` `docs/` `tools/` ไม่มีสักที่เดียวที่เอ่ยชื่อฟีเจอร์นี้**

### A6 — ปิด nonclaim ของรอบ 12 ที่ค้าง: **ทำไม 337 ≠ 384**

รอบ 12 ทิ้งไว้เป็น nonclaim รอบนี้กระทบยอดได้ **ลงตัวพอดีไม่มีเศษ**:

```
9 โมดูลที่ import ไม่ได้ (capstone/pefile) กลายเป็น _FailedTest อย่างละ 1  =  9 รายการ
จำนวนเมธอด test จริงในโมดูลทั้ง 9 (นับด้วย AST ไม่ต้อง import)         =  56 ตัว
337 - 9 + 56 = 384   ✅
```

นับซ้ำบน Windows ด้วย `py -3` ใน worktree จริง → **TOTAL_HIDDEN=56, RECONCILE = 384** ตรงกัน
และบนเครื่องนี้ `capstone=OK v5.0.6 | pefile=OK v2024.8.26`

> 🔴 **ผลพลอยได้ที่ต่อยอดจากรอบ 12 โดยตรง: 56 จาก 384 เทส (14.6%) มีอยู่ได้เพราะ
> *เครื่องนี้บังเอิญลง capstone/pefile ไว้* และ repo **ไม่มี `requirements.txt`
> ไม่มี `pyproject.toml` ไม่มีที่ไหนเขียนว่าต้องใช้ Python เวอร์ชันอะไร** (NEGATIVE เกรด A รอบ 12)
> → เครื่องอื่นจะได้ `Ran 337` แล้ว **ไม่มีอะไรบอกว่าหายไป 56 ตัว** เพราะมันโผล่มาเป็น
> "error 9 ตัว" ที่หน้าตาเหมือนปัญหาสภาพแวดล้อมทั่วไป**

---

## INFERENCE เกรด B

**B1** — WIP คือการ *generalise* ยามเดิม (จากเทียบเท่ากับ backpack ที่ hypothesise ไว้ตัวเดียว
→ เป็น allowlist ตาม content signature) **บวก** ฟีเจอร์ใหม่ `move_backpack_item_to_free_slot`
ที่ยังไม่มีใครเรียก — สอดคล้องกับที่ `GT-002` ถูกตั้งเป็น `BLOCKED — รอ M3 implementation เสร็จ`

**B2** — ถ้า commit WIP ตอนนี้โดยไม่เพิ่มอะไร repo จะได้โค้ด 52 บรรทัดที่
**ไม่มีเทสแตะ ไม่มี scenario แตะ ไม่มีเอกสารอ้าง** เข้าไปอยู่ในสถานะ "gate เขียว"
→ เป็นเขียวที่ให้ความมั่นใจผิด ๆ ตรงตามรูปแบบที่ M14 เจอมาแล้วรอบหนึ่ง
(`store.expire_open_sessions()` ลบทิ้งแล้วเทส 322 ตัวยังเขียวหมด)

**B3** — `session.py:162` เป็น stub ของ method เดียวกันในคลาสปลอม → คนเขียน WIP
ตั้งใจให้ Protocol ใน `repository.py` กับตัวปลอมไม่หลุดจากกัน (เป็นสัญญาณว่างานทำอย่างระวัง
ไม่ใช่โค้ดที่หลงมา) — แต่ก็ยังไม่มีเทสเรียกอยู่ดี

---

## NONCLAIMS — สิ่งที่รอบนี้ **ไม่ได้** พิสูจน์

1. **ไม่ได้บอกว่าโค้ด WIP ผิด** — รอบนี้วัด *การมองเห็นของเทส* ไม่ได้วัดความถูกต้อง
   ไม่มีอะไรในรอบนี้ชี้ว่า `move_backpack_item_to_free_slot` มีบั๊ก
2. **ไม่ได้รัน `verify_foundation.ps1` เต็มตัว** — เทียบเฉพาะ `unittest discover -s tests`
   ซึ่งเป็นขั้นที่ 60 ของ gate ยังมีขั้น verifier อื่นที่ไม่ได้รันในรอบนี้
3. **รันบน Python 3.10 ของ sandbox** ไม่ใช่ 3.14.7 ของ Windows — แต่ข้อสรุปเป็น
   **differential ในสภาพแวดล้อมเดียวกันทั้งสองฝั่ง** จึงไม่ขึ้นกับเวอร์ชัน
   (และ A5/A6 ยืนยันซ้ำบน Windows แล้ว)
4. **coverage 6.5% เป็น lower bound** — tracer ทำให้ `testsRun` ลดเหลือ 301
   จึงอาจ under-count ได้ · **แต่ข้อสรุปหลัก (A4) ไม่ได้อาศัยตัวเลขนี้เลย**
   มันอาศัย canary ที่รันผ่าน CLI ปกติครบ 337 พร้อม control ที่พิสูจน์ว่า harness จับได้
5. **ไม่ได้แตะ `.gitignore` ไม่ `git add` ไม่ commit ไม่แก้โค้ด** — mutation/canary ทั้งหมด
   ทำบนสำเนาใน `/tmp/r13` เท่านั้น
6. **ไม่ใช่ข้อสรุปว่าควรรีบเขียนเทสให้ M3** — เทสที่ถูกต้องต้องรู้ก่อนว่า
   **ceiling ของ HYP-PF-008 ครอบ M3 หรือไม่ (คำถามข้อ 6 ที่ยังค้าง)** เขียนก่อนตอบ = เสี่ยงเขียนผิดทิศ

---

## ต้องให้ Panya เคาะ — ข้อ 8 (ใหม่)

WIP 187 บรรทัดค้างมา ~6 ชั่วโมง และตอนนี้รู้แล้วว่า **สวีตมองไม่เห็นมันเลย** จะเดินทางไหน:

| | ทางเลือก | ผลที่ตามมา |
|---|---|---|
| **ก** | commit ตามสภาพตอนนี้ | WIP พ้นจากสถานะ "มีสำเนาเดียว" (ปิดความเสี่ยงรอบ 7–8 ถาวร) แต่ได้โค้ด 52 บรรทัดที่ไม่มีอะไรเฝ้าเข้า repo พร้อมป้ายเขียว |
| **ข** | commit แล้วแปะ `# PF-UNVERIFIED` / เพิ่มแถวใน `FUNCTIONAL_COVERAGE.json` เป็น `unverified` ทันที | ได้ทั้งความปลอดภัยของ git และไม่โกหกตัวเอง — ต้องยอมให้ `OPEN DOMAINS` เพิ่มจาก 7 เป็น 8 |
| **ค** | เขียนเทสให้ครบก่อนแล้วค่อย commit | ตรงตามมาตรฐาน M14 ที่สุด **แต่ติดคำถามข้อ 6** (ceiling ของ HYP-PF-008) ซึ่งยังไม่มีคำตอบ → ทำตอนนี้ไม่ได้ |
| **ง** | ปล่อยค้างต่อ | ความเสี่ยงเดิมทั้งหมดยังอยู่ และรอบ 8 พิสูจน์แล้วว่ามีแค่ tag เดียวกัน stash จาก GC |

**ผมเอนไปทาง ข** — มันปิดความเสี่ยง "ของหาย" ได้ทันทีโดยไม่ต้องรอคำตอบข้อ 6
และไม่สร้างเขียวปลอม แต่มันเปลี่ยน "สิ่งที่ repo ถือ" + เปลี่ยนตัวเลข `OPEN DOMAINS`
= การตัดสินใจเชิงขอบเขต **จึงไม่ทำโดยไม่มีคำสั่งจากคุณ**

---

## หลักฐานประกอบ

- `pf_bridge\outbox\036_r13_wip_observability.out.txt` — ผลรันบน Windows (dep, census, git grep, repo state)
- `/tmp/r13/{head,wip,mut1,mut2,mut3,canary,ctrl2}` — ต้นไม้และผลรัน (ชั่วคราวใน sandbox)
- patch ที่ใช้: `pf_bridge\backup\main_dirty_20260817_0752_lf_verified.patch` sha256 `a80b3374…` (ยืนยันซ้ำบน Windows)

## ยืนยันว่า repo ไม่ถูกแตะ (job 036, 09:14:31–09:14:32)

HEAD `eef51fa` เท่าเดิม · dirty **6 ไฟล์ 187+/21− ครบรายไฟล์** · staged 0 · untracked 0 ·
`diff --check` exit 0 · ไม่มี `index.lock` · tag → `d381be5` · console worktree `0e922b6` (**16 รอบติด**) ·
canonical DB **69,632 B mtime `04:23:18.5714411` sha `673f4bfb…` ไม่ขยับ** · ไม่มี `-wal`/`-shm`
