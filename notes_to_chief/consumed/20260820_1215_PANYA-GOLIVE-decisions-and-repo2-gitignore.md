# 🚀 คำสั่ง Panya 2026-08-20 ~12:15 — "ฉันพร้อมขึ้น cloud ตอนนี้แล้ว"

## คำตัดสินของ Panya (ปิดคำถามค้างของ chief)
| คำถามค้าง | คำตัดสิน |
|---|---|
| (ก) `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` ขึ้นไหม | ✅ **ขึ้น** (ตามที่ chief เสนอ) |
| (ข) `evidence_screens/` ขึ้นไหม | ✅ **ขึ้น** (ตามที่ chief เสนอ) |
| `verify_foundation.ps1` re-pin หรือปลดระวาง (79 vs 105) | ⏸️ **พักไว้ ตัดสินหลังขึ้น cloud** — อย่าใช้เป็นตัวบล็อก |
| ลำดับสับสวิตช์ | 🔴 **push ก่อน → เห็น Actions แดงจริงหนึ่งครั้งแล้วเขียวกลับ → ค่อยสับ chief ขึ้น cloud** |
| `report_images/` | ❌ **ยังไม่ตัดสิน ⇒ กันออกไปก่อน** (ถามใหม่ได้ทีหลัง) |

---

## 🔴 ของด่วนที่สุด — งานแรกของรอบถัดไป
**`.github/workflows/gate-windows.yml` มีอยู่จริงบนดิสก์ แต่ git มองไม่เห็น**

ตรวจสดเมื่อ 12:1x: `git check-ignore -v .github/workflows/gate-windows.yml`
→ `.gitignore:1:/*` · `git ls-files .github` = **ว่างเปล่า**

⇒ **push ตอนนี้ CI จะไม่ติดไปด้วย และ Actions จะไม่มีวันรันเลย**

**สั่ง:** งานแรกของรอบถัดไปคือ commit `.gitignore` เติม allowlist ให้ `.github/`
(`!/.github/` + `!/.github/**` — จำกฎ deny-all ว่า git ไม่เดินเข้าโฟลเดอร์ที่ถูก exclude แล้ว
ต้องเปิดตัวโฟลเดอร์ก่อน) · จ็อบเดียว เล็ก ๆ ไม่ต้องรอ gate เต็ม ถ้าแยกได้

---

## รีโปที่สอง — `.gitignore` สร้างและ **ทดสอบแล้ว** พร้อมใช้
ไฟล์: **`pf_bridge\DRAFT_gitignore_REPO2_20260820.txt`** (2,776 ไบต์)
ทำตามเงื่อนไขบังคับทั้ง 3 ข้อของ chief verdict:
- **① deny-all + allowlist** — บรรทัดแรกคือ `/*` เหมือนรีโปหลัก **ไม่ใช่ท่า ignore-list**
  (บล็อก (ข) เดิมใน `DRAFT_gitignore_runtime_state.txt` เป็นท่า ignore-list ⇒ **ไม่ผ่านเงื่อนไข ① ของ chief เอง** — ฉบับใหม่นี้แทน)
- **② `factpack_L1/strings_*.tsv` + `pe_*.tsv` ถูกกันสองชั้น** (ทั้ง `/factpack_L1/*` และบรรทัด deny ท้ายไฟล์)
  เข้าเฉพาะ `MANIFEST.md` · `TIMING.md` · `blocks_256.tsv` · `make_factpack_l1.py`
- **③ กฎ sibling** — 🔲 **chief ต้องเขียนเอกสาร + เทสที่ล้มถ้าโครงไม่ตรง** (ยังไม่ได้ทำ ดูข้างล่าง)

### ผลทดสอบจริง (ผมรันเอง ไม่ได้ประมาณ)
สร้างรีโปชั่วคราวใน `/tmp` ที่มีพาธเหมือนจริงครบ **1,310 พาธ** แล้ว `git add -A`:

**เข้ารีโป 224 ไฟล์ / 13.6 MiB · ถูกกัน 1,086 ไฟล์**

| assertion | ผล |
|---|---|
| `strings_ascii.tsv` · `strings_utf16.tsv` · `pe_imports/exports/sections.tsv` ถูกกัน | ✅ 5/5 |
| `LOCK*.txt` · `PANYA_PRESENT.txt` · `watchdog.log` · `bridge_loop_state.txt` ถูกกัน | ✅ 5/5 |
| `blocks_256.tsv` · `MANIFEST.md` · `make_factpack_l1.py` เข้า | ✅ 3/3 |
| `VITAL_REGISTRY...tsv` · `GAME_TEST_QUEUE.md` · `CHIEF_CONTINUATION.md` เข้า | ✅ 3/3 |
| `agent_kit/chief_task_prompt.md` · `staged/TEMPLATE_teardown_generic.ps1` · `pf_bridge.ps1` เข้า | ✅ 3/3 |
| `FACTPACK_R102_HOSTILE13_ROSTER.md` เข้า | ✅ |
| ไฟล์นามสกุล bin/dmp/zip/exe/dll/sqlite3/log/pyc หลุดเข้าไหม | ✅ **0 ไฟล์** |
| ภาพที่เข้ามาอยู่ใน `evidence_screens/` เท่านั้นไหม | ✅ 14/14 |

**สัดส่วนที่เข้า:** notes_to_chief 61 · root 53 · archive 46 · staged 17 · evidence_screens 14 · drafts 12 · agent_kit 9 · codex_orders 5 · factpack_L1 4 · image_queries 2 · templates 1
**ก้อนใหญ่สุดที่เข้า:** `blocks_256.tsv` 4.6 MB · ภาพ GT-027 5 ใบ ~4 MB

🔴 **chief ตรวจซ้ำเองก่อนใช้** — ผมทดสอบด้วยไฟล์เปล่าที่มีพาธเหมือนจริง ไม่ใช่ไฟล์จริง
(พฤติกรรม `.gitignore` ขึ้นกับพาธ ไม่ขึ้นกับเนื้อไฟล์ แต่ผมอยากให้มีสองตาก่อนของขึ้น remote)

---

## งานที่เหลือของ chief เรียงตามลำดับ
1. 🔴 **`.gitignore` เติม `!/.github/` + `!/.github/**`** — ไม่งั้น CI ตายตั้งแต่เกิด (ข้างบน)
2. **กฎ sibling + เทสที่ล้มจริง** — สองรีโปต้อง clone ลงมาเป็นพี่น้องกัน ชื่อ `Pirate Force ServerProject`
   และ `pf_bridge` **เป๊ะทั้งคู่** เพราะ `tools\pf_vital_name_thunk_static.py:127` ใช้ `ROOT.parent / "pf_bridge"`
   ⇒ เขียนเป็นกฎในเอกสาร **และ** เทสที่ fail ถ้าโครงไม่ตรง (ห้ามเป็นความรู้ในหัวคนเดียว)
3. **Actions: ต้องเห็นแดงจริงหนึ่งครั้งก่อนถึงจะนับว่าใช้ได้** — จงใจทำให้แดง (เช่นใส่ตัวอักษรนอก cp874
   ในเครื่องมือสักตัวชั่วคราว) ดูว่ามันจับได้ แล้วแก้กลับให้เขียว · **เขียวที่ไม่เคยแดง ไม่ใช่ gate**
4. **`chief_task_prompt_CLOUD_DRAFT.md` เก่าแล้ว** (19 ส.ค. 17:40) — วันนี้มีกฎใหม่เพิ่มสองข้อ:
   กฎแม่บ้าน "ห้ามลบคิวที่ยังไม่เทส" และกฎเลขจ็อบ `0`-prefix ⇒ **rebase ร่างใหม่แล้วให้ Panya เห็น diff**
5. 🔴 **ห้าม `git push` อัตโนมัติจากจ็อบ gate_commit จนกว่า Panya จะสั่ง** — credential เป็นของท่าน
   ท่านสั่ง push เองทุกครั้งจนกว่าจะเปลี่ยนกฎ

## nonclaims
- ผมไม่ได้แตะ `.gitignore` ของรีโปหลัก ไม่ได้ `git init` ที่ `pf_bridge` ไม่ได้ commit อะไรทั้งสิ้น
- ผมไม่ได้ทดสอบว่า Actions รันผ่านจริง — แค่ยืนยันว่าไฟล์ workflow ยัง **ไม่ถูก track**
- ⚠️ **ผมทำ `git status` ในรีโปหลักแล้วมันทิ้ง `.git/index.lock` ไว้** (mount ลบไฟล์ไม่ได้)
  **ผมเปลี่ยนชื่อเป็น `.git/STALE_index.lock_20260820_1210_delete_me` แล้ว** ⇒ git ใช้งานได้ปกติ
  **ฝาก Panya ลบไฟล์นั้นทิ้งเมื่อสะดวก** — ผมลบเองไม่ได้
