# FINDINGS R12 — gate ผ่านเพราะ "เครื่องนี้" ไม่ใช่เพราะ "repo"

รอบ idle ครั้งที่ 12 · 2026-08-17 08:50–09:0x ICT · chief-continue
ขอบเขต: read-only ต่อ repo 100% (ใช้ `git archive` ลง `/tmp/r12` — ไม่ clone ไม่สร้าง worktree)
ไม่แตะ GameClient ทั้งรอบ · ไม่รัน server

---

## คำถามของรอบนี้

รอบ 10 ตอบว่า *"หลักฐาน 316 ไฟล์อยู่นอก git ทั้งหมด git กู้ให้ไม่ได้"* — แล้วก็หยุดตรงนั้น
รอบนี้ถามคำถามถัดไปที่ไม่มีใครเคยถาม และมันแรงกว่า:

> **"ถ้ามีคน `git clone` ที่ `eef51fa` แล้วรัน gate — `verify_foundation.ps1` จะผ่านไหม"**

คำตอบคือ **ไม่** และไม่ใช่เพราะขาดหลักฐานประกอบ แต่เพราะ **verifier สองตัวที่เป็นหัวใจของ gate
บังคับให้ไฟล์ที่ `.gitignore` กันไว้ต้องมีอยู่จริงบนดิสก์ ไม่งั้น throw ทันที**

---

## 1. FACT — เกรด A (วัดได้ ทำซ้ำได้ มีคำสั่งกำกับ)

### 1.1 โค้ดฝั่งที่ควรอยู่ใน git — อยู่ครบจริง (ข่าวดี)

| dir | บนดิสก์ | tracked | หมายเหตุ |
|---|---|---|---|
| `src/` | 26 | **26** | ครบ 100% |
| `tests/` | 49 | **49** | ครบ 100% (42 โมดูล `test*.py` + 7 golden json) |
| `scenarios/` | 10 | **10** | ครบ |
| `migrations/` | 3 | **3** | ครบ |
| `docs/` | 19 | **19** | ครบ |
| `current/` | 116 | **2** | ตั้งใจ — `pf_login_game_server_v141.py` (ตัวที่ Foundation สืบทอดจริง) **อยู่ใน git** + 1 `.bat` |
| `tools/` | 50 | 39 | 11 ตัวที่ไม่ track ไม่มีตัวไหนถูก gate เรียก |

→ **ข้อกังวลใหญ่ที่สุดก่อนเริ่มรอบ (M13 บอกว่า Foundation ครอบ V141 8,014 บรรทัด —
ถ้าไฟล์นั้นไม่อยู่ใน git ก็จบ) พิสูจน์แล้วว่า *ไม่เป็นความจริง* — V141 tracked**

`git archive HEAD` → **209 ไฟล์** (= จำนวน tracked พอดี) และ
`python3 -m compileall -q src tests tools/build_foundation_release.py` → **exit 0**

### 1.2 แต่พอรันเทสจากต้นไม้ที่มีแต่ไฟล์ tracked — พัง 33 ตัว

```
/tmp/r12/head_only$ python3 -m unittest discover -s tests
Ran 337 tests — FAILED (failures=8, errors=25)
```

### 1.3 ต้นตอ: `evidence_refs` ในไฟล์ที่ tracked ชี้ไปไฟล์ที่ **ไม่** tracked

| ไฟล์ (tracked) | จำนวน ref | tracked | **untracked** |
|---|---|---|---|
| `docs/FUNCTIONAL_COVERAGE.json` | 103 | 70 | **33** |
| `docs/HYPOTHESIS_LEDGER.json` | 30 | 29 | **1** (เป็น subset ของ 33) |

untracked ทั้ง 33 = `reports/PF_RE_V*.md` — **มีอยู่บนดิสก์ครบทุกไฟล์ เป็น UTF-8 text ล้วน
รวม 181,157 ไบต์ (176.9 KiB) ไม่มีไบนารีเลยสักไฟล์**

`verify_functional_coverage.py:81` และ `verify_hypothesis_ledger.py:97` ทำแบบเดียวกัน:
`raise …Error(f"{label} does not exist: {text}")` → **fail-closed ที่ตัว loader**
แปลว่า **เทสทุกตัวที่เรียก `load_coverage()` ตายพร้อมกันหมด** ไม่ใช่แค่ตัวที่เช็ค path

### 1.4 พิสูจน์แบบ differential ว่า 33 ไฟล์นั้นคือตัวแปรเดียว

เอา **เฉพาะ 33 ไฟล์นั้น** ใส่กลับเข้าไปในต้นไม้ HEAD-only (ไม่แตะอะไรอย่างอื่นเลย):

```
py verify_hypothesis_ledger.py   -> exit 0   HYPOTHESIS_LEDGER PASS entries=16
py verify_functional_coverage.py -> exit 0   OPEN DOMAINS: 7
python3 -m unittest discover -s tests -> Ran 337 — FAILED (errors=17)
```

**33 → 17 และ failures 8 → 0** คือ 16 เทสกลับมาเขียวจากการวางไฟล์ 33 ไฟล์เท่านั้น

### 1.5 อีก 17 ตัวที่เหลือ — แยกได้ 5 กลุ่ม ไม่มีตัวไหนเป็นบั๊กของโค้ด

| # | กลุ่ม | ต้องการอะไร | track ได้ไหม |
|---|---|---|---|
| 9 | `import capstone` / `pefile` ระดับโมดูล | แพ็กเกจ third-party | — (ดู 1.6) |
| 3 | probe tests | `GameClient/GameClient.bin` (14,759,424 B) | **ห้ามเด็ดขาด** — อยู่นอก repo + ห้ามอัปโหลด |
| 2 | `test_structural_corpus_audit` | `evidence/v74-v76/*` 6 ไฟล์ | ห้าม — gate เองแบน `^evidence/` |
| 1 | `test_natural_v94_provenance…` | `backups/v94_runtime_before_v95_.../capture_v94/` 2 ไฟล์ (268,244 B) | ห้าม — gate เองแบน `^backups/` |
| 1 | `test_upgrade_from_original_foundation_schema` | `git show 5c200e2:migrations/001_initial.sql` | ต้องมี `.git` — ผ่านใน clone จริง ตกใน archive |
| 1 | `test_primary_exception_is_preserved…` | `Exception.__notes__` = **Python ≥ 3.11** | ไม่เกี่ยวกับ git (sandbox เป็น 3.10) |

**ยืนยันบน Windows (job 035):** `py -3` = **3.14.7**, `HAS_NOTES=True`
→ 1 ตัวสุดท้ายเป็นผลของ Linux sandbox ล้วน ๆ ไม่ใช่ของโปรเจกต์

### 1.6 NEGATIVE เกรด A — ของที่ค้นแล้ว **ไม่มีจริง**

- `git ls-files` หา `requirement*` / `pyproject*` / `setup.py|cfg` / `Pipfile` / `constraints*`
  → **0 ไฟล์** ทั้งที่ **9 โมดูลเทสที่ tracked** `import capstone` / `pefile` ระดับ top-level
  (พังตอน discovery = `_FailedTest` ไม่ใช่ skip — ดังแต่ไม่มีใครบอกว่าต้องลงอะไร)
  ชื่อ 2 แพ็กเกจนี้โผล่ในเอกสารที่ tracked แค่ที่เดียวคือ
  `docs/COVERAGE_TEST_STRENGTH_AUDIT_ROUND4_20260817.md` และเป็นการเอ่ยผ่าน
- grep `python *3\.[0-9]+` ในทุก `.md` ที่ tracked → **0 hit** ทั้งที่มีเทสที่ต้องการ ≥ 3.11
- `git ls-files reports/PF_RE_V*.md` = **0** · `backups/` = **0** · `evidence/` = **0**
  (ยืนยันบน Windows ด้วย git จริง — job 035 §5)
  `check-ignore` ตอบ `.gitignore:8:/reports/*`

### 1.7 ข่าวดีอีกข้อ — guard ของ release archive แน่นจริง

`tools/build_foundation_release.py` ใช้ **glob** (`src/**.py`, `migrations/*.sql`, `scenarios/*.json`)
ขณะที่ `verify_foundation.ps1` เทียบกับ **expected set ที่ hardcode 78 สมาชิก**
→ เพิ่มหรือลบโมดูลเมื่อไร set ไม่ตรงทันที **gate แดงเสียงดัง** (ตรวจแล้ว: ปัจจุบันตรงกันเป๊ะ)
🟡 แต่ release zip **ไม่มี `tests/` เลย** → archive ที่ปล่อยออกไป **ตรวจตัวเองไม่ได้**

---

## 2. INFERENCE — เกรด B

> **gate เขียวเพราะเครื่องนี้ ไม่ใช่เพราะ repo**
>
> `git clone` ที่ `eef51fa` ลงเครื่องที่มี Python 3.14 + capstone + pefile ครบ
> **ยังรัน `verify_foundation.ps1` ให้ผ่านไม่ได้** เพราะ `verify_hypothesis_ledger.py`
> และ `verify_functional_coverage.py` ตายที่ loader ก่อนถึงขั้นตรวจอะไรเลย
>
> จำนวนไฟล์นอก git ที่ต้องหามาวางคู่ clone ก่อน gate จะเริ่มทำงานได้ = **อย่างน้อย 42 ไฟล์**
> (33 reports + 2 backups + 6 evidence + `GameClient.bin`)

**ความขัดแย้งเชิงนโยบายที่เป็นรากของเรื่องนี้:** `verify_foundation.ps1` มีกฎ
`FORBIDDEN TRACKED PATH` ที่ **ห้าม** track `references|evidence|backups|packages|derived|analysis|history|v77_video_frames|capture*`
— ขณะที่ verifier อีกสองตัวใน gate เดียวกัน **บังคับ** ว่าไฟล์ในโฟลเดอร์เหล่านั้นต้องมีอยู่
สองกฎนี้อยู่ในสคริปต์เดียวกันและขัดกันโดยตรง

⚠️ **ต่อยอดจากรอบ 10 ทันที:** รอบ 10 สรุปว่าถ้าหลักฐานหาย "เกรดพิสูจน์ไม่ได้"
รอบนี้ได้ผลที่แรงกว่า — ถ้าหลักฐานหาย **gate รันไม่ได้เลย** ทุกเกรดกลายเป็น unverifiable
พร้อมกันทั้งกระดาน ไม่ใช่แค่แถวที่อ้างไฟล์นั้น

---

## 3. สิ่งที่ทำในรอบนี้ (ไม่แตะ repo)

1. **`pf_bridge\backup\gate_required_untracked_20260817_0857.tar.gz`** (94,791 B)
   sha256 `277841bdbaea2dc18982d2d90c6d104dc52115243683d8c7d6af08c21cec6ec2`
   บรรจุ **36 entry = 35 ไฟล์ + manifest** (33 reports + 2 ไฟล์ `backups/v94…`)
   → เดิม **ไม่มีอะไรถือไฟล์ 35 ตัวนี้ไว้เลย** และ **ไม่อยู่ใน bundle ของรอบ 10** ด้วย
   (6 ไฟล์ `evidence/` ที่ structural audit ต้องใช้ — ตรวจแล้ว **อยู่ใน bundle รอบ 10 ครบ 6/6**)
2. **`pf_bridge\backup\GATE_REQUIRED_UNTRACKED_20260817.manifest`** — ฟอร์แมต A
   (`PATH|BYTES|SHA256`, path จาก root `Pirate Force`) 35 บรรทัด รวม 449,401 B
3. **`pf_bridge\backup\verify_manifest_a.py`** — ตัวตรวจ format-A แบบทั่วไป (stdlib ล้วน)
   ใช้ได้กับ manifest ฟอร์แมต A ทุกไฟล์ ไม่ผูกกับ corpus ใด
4. **drill ตามกติการอบ 7** (ห้ามเชื่อว่ามี backup จนกว่าจะพิสูจน์):
   แตก bundle ลง dir เปล่า → อ่าน manifest *จากใน bundle* → **ok=35 missing=0 mismatch=0
   differs_from_original=0** และ sha256 หลัง copy ลง `backup\` **ตรงกับตอนสร้าง**
   ตรวจซ้ำบน Windows `py -3` → **exit 0 ok=35** (job 035 §2–3)

---

## 4. NONCLAIMS — สิ่งที่รอบนี้ **ไม่** ได้พิสูจน์

- **ไม่ได้รัน `verify_foundation.ps1` เต็มตัว** บนต้นไม้ HEAD-only (ต้องเป็น Windows และมันสร้าง
  release zip 2 ก้อน) — ข้อสรุปเรื่อง gate มาจาก **verifier 2 ตัวที่ gate เรียก** ซึ่งตายก่อน
  ไม่ใช่จากการรัน gate จริง
- **ไม่ได้ clone จริง** (กติกาห้าม) — ใช้ `git archive HEAD` ซึ่งต่างกันตรง **ไม่มี `.git`**
  → เทส `test_upgrade_from_original_foundation_schema` ที่ต้องใช้ `git show` **น่าจะผ่านใน clone จริง**
  แต่รอบนี้ยืนยันไม่ได้
- **337 ≠ 384**: ตัวเลข 337 คือจำนวนที่ Linux 3.10 นับได้เมื่อ 9 โมดูล import ไม่ผ่าน
  **ไม่ได้พิสูจน์** ว่า 384 บน Windows ประกอบด้วยอะไร
- **ไม่ใช่ข้อสรุปว่า `.gitignore` เขียนผิด** — เป็นการชี้ว่านโยบาย "ห้าม track evidence"
  กับ verifier ที่ "บังคับให้ evidence อยู่ครบ" ขัดกัน ซึ่ง**ต้องให้ Panya ตัดสิน** ไม่ใช่ผมตัดสิน
- ไม่ได้แตะ `.gitignore`, ไม่ได้ `git add` อะไร, ไม่ได้ commit

---

## 5. ต้องการคำตัดสินจาก Panya — ข้อ 7 (ใหม่)

| ตัวเลือก | ทำอะไร | ได้อะไร | เสียอะไร |
|---|---|---|---|
| **ก** | whitelist **33 `reports/PF_RE_V*.md`** ใน `.gitignore` แล้ว commit | ledger + coverage verifier **รันได้จาก git ล้วน** · 16 เทสกลับมาเขียวโดยไม่พึ่งไฟล์นอก git · gate ไม่ผูกกับเครื่องอีกต่อไปในส่วนนี้ | repo โต **176.9 KiB** (text ล้วน ไม่มีไบนารี) · ต้องรัน gate เต็มบน Windows ยืนยัน |
| **ข** | เพิ่ม `requirements.txt` (capstone, pefile) + ระบุ **Python ≥ 3.11** ใน `README`/`AGENTS.md` | คนที่มาใหม่รู้ว่าต้องลงอะไร แทนที่จะเจอ `ModuleNotFoundError` 9 บรรทัด | ต้อง pin เวอร์ชันให้ถูก |
| **ค** | เพิ่ม **external-inputs manifest** เข้า git แล้วให้ gate เช็คก่อนเป็นขั้นแรก แล้วรายงานว่า *"ขาดไฟล์นอก git N ไฟล์"* | gate เลิกตายแบบงง ๆ · ครอบ `GameClient.bin` + `evidence/` + `backups/` ที่ **track ไม่ได้ตลอดกาล** | ต้องเขียน verifier ใหม่ 1 ตัว |
| **ง** | ไม่ทำอะไร | สถานะเดิม แต่ตอนนี้ **มี bundle รองแล้ว** ถ้าไฟล์หายก็กู้ได้ | gate ยังผูกกับเครื่องนี้เครื่องเดียว |

ผมเอนไปทาง **ก + ข** (ทั้งคู่เล็ก ย้อนกลับได้ ไม่แตะพฤติกรรม runtime สักบรรทัด)
แต่ทั้งสองเปลี่ยน "สิ่งที่ repo ถือ" ซึ่งเป็นการตัดสินใจเชิงขอบเขต
**กติกาปัจจุบันห้ามผมทำเองโดยไม่มีคำตัดสินจากคุณ** — จึงหยุดไว้ตรงนี้

---

## 6. คำสั่งกู้ (ถ้า 35 ไฟล์นั้นหาย)

```powershell
cd "C:\Users\Panya\Desktop\Pirate Force"
tar -xzf pf_bridge\backup\gate_required_untracked_20260817_0857.tar.gz
py -3 pf_bridge\backup\verify_manifest_a.py pf_bridge\backup\GATE_REQUIRED_UNTRACKED_20260817.manifest
# ต้องได้ ok=35 missing=0 mismatch=0 และ exit 0
```

หลักฐาน `evidence/` 6 ไฟล์ที่ structural audit ใช้ → กู้จาก bundle รอบ 10
`evidence_pinned_20260817_0819.tar.gz` (ดู `backup\EVIDENCE_CORPUS_BASELINE.md`)
`GameClient.bin` → **กู้จาก backup ไม่ได้และไม่ควรมี** แต่ sha256 ถูก pin ไว้ใน probe config
ที่ tracked 12 ไฟล์ (`C528BF43…`) → พิสูจน์ได้ว่าไบนารีที่มีอยู่เป็นตัวเดิมหรือไม่
