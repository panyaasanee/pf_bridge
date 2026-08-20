# R114 — GT-039 SHA pointer แก้ให้ tester re-derive ได้ (bridge-only)

> ⚠️ ชื่อไฟล์มีคำว่า "backfill mailbox stubs" ติดมาจากดราฟต์แรก — **สุดท้ายไม่ได้ backfill อะไร**
> เพราะ mailbox สะอาดอยู่แล้ว (ดูข้อ 5) · เก็บชื่อไฟล์ไว้ไม่แก้เพื่อไม่ให้ pointer/ดัชนีชนกัน

- **เวลา:** 2026-08-20 20:0x UTC (~2026-08-21 03:0x +07:00)
- **รันบน:** Claude Code Routine (cloud) · Linux 6.18 x86_64 · Python 3.11.15 · pytest 9.1.1
- **branch รอบนี้:** `pf_bridge` -> `claude/zealous-turing-lij8pk` · `pirate-force-server` -> (ไม่แตะ code repo รอบนี้)
- **ฐาน:** bridge `a67f935` (= main หลัง R113 merge) · server `cc46a03` (= main, CI verdict `success` ตามทาง D)

## 1. round-lock guard: ว่างสองใบ -> คว้าเลย
- `list_pull_requests` open ทั้งสอง repo = 0 ใบ (bridge เจอ timeout หนึ่งครั้งบน MCP, ยิงซ้ำเป็น 0 ทันที)
- claim commit: `5f03dea` "round claim: lij8pk" push ขึ้น `claude/zealous-turing-lij8pk` (bridge)
- เปิด PR #9 "WIP round claim lij8pk" body มีบรรทัด `PF-AUTOMERGE: v4` เป๊ะ

## 2. round-start probe (ตามข้อบังคับ v5 · ตัด push-main ทิ้งถาวรแล้ว)
| ข้อ | ผล | หมายเหตุ |
|---|---|---|
| `which gh` | ไม่มี | เหมือน R112/R113 |
| GitHub API (ผ่าน MCP) | ใช้ได้ | list_pull_requests + create_pull_request สำเร็จ |
| ทาง D `ci-status` | มีชีวิต | fetch สำเร็จ 5 คำตัดสิน สำหรับ `cc46a03` = `success` (run 32406182274, 2026-08-20T19:02:16Z) |
| sibling registry `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` | อยู่จริง | 11,388 ไบต์ |

## 3. state ที่พบต้นรอบ
- **server main ขยับ**: `2842fb9` -> `cc46a03` "wip" — commit ก้อนใหญ่ 6,891 insertions
  ที่ทำให้ GT-039 (NPC-HP-LINK-001 / HYP-PF-029) กลายเป็นเทสที่พร้อมรัน:
  `npc_hp_link_hypothesis.py`, `scenarios/npc_hp_link_hypothesis_target_sweep.json`, `app.py`, `runtime.py`,
  `tools/pf_npc_hp_link_headless_replay.py`, `tests/test_npc_hp_link_{hypothesis,dispatch}.py`
- CI verdict ของ `cc46a03` = `success` (ทาง D ตอบตรง sha)
- `notes_to_chief/` ต้นรอบ: **0 จดหมายใหม่** (ตรวจด้วย convention ที่ถูก — ดูข้อ 5)

## 4. งานหลัก (ที่รอด): **แก้ queue-entry ของ GT-039 ให้ tester re-derive SHA ได้**
GT-039 เดิมเขียนว่า *"อ่าน SHA จาก `outbox\\178_round111_*`"* — แต่ `outbox/` gitignored (`.gitignore:11` `/*`)
⇒ tester/clone อื่น **หา SHA ที่จะบูตไม่ได้ตลอดกาล** (พังเงียบ ไม่มี error)

**สิ่งที่วัดแล้วรอบนี้:**
- โมดูล HYP-PF-029 อยู่บน `origin/main` HEAD = `cc46a03` (`git cat-file -e origin/main:src/pirateforce_foundation/npc_hp_link_hypothesis.py`)
- ci-status ของ `cc46a03` = `success`
- 129 เทส dispatch+hypothesis บนคลาว = passed (216 subtests, 4.92s)
- headless proof เต็มบนคลาว (ไม่มี canonical DB/ client image): 97 guards PASS, exit 0
- verifier `verify_npc_hp_link_encoder.py` = 220 guards PASS (จาก pf-static-re re-run)

**เปลี่ยนใน `GAME_TEST_QUEUE.md` — สองจุด ในหัวรายการ GT-039 เท่านั้น:**
- (a) status line: `PENDING (HYP-PF-029) — บูตด้วย origin/main HEAD ล่าสุดที่ ci-status = success` + บล็อกสามบรรทัด "re-derive SHA"
  🔴 **ไม่ hard-pin `cc46a03`** เพราะ main ขยับได้ก่อน Panya เปิดเครื่อง — ให้ re-derive จาก `git rev-parse origin/main`
  แล้วเช็ค ci-status ตามสี่กฎ · เก็บ `HYP-PF-029` ไว้ในบรรทัด (adversary ทัก: ดราฟต์แรกทิ้ง hypothesis-id ไป)
- (b) prereq ①: `TargetVital 0x2001` -> `TargetVital 0x2001 'Navy Transfer'` (เติมชื่อ actor ให้ตรง client log เป๊ะ)

**คิวยัง PENDING เหมือนเดิม — เปลี่ยนเฉพาะ pointer/สตริง** ไม่ปิด ไม่ย้ายรายการ (กฎข้อ 10)

### 🔴 บทเรียนสำคัญ: ดราฟต์แรกของรอบนี้เกือบ **แก้ของที่ถูกให้ผิด** — pf-adversary จับได้
- ดราฟต์แรกเปลี่ยน `TargetVital 0x2001` -> `TargetVital 0x1ADD` โดยอ้าง `PF_VITAL_NAMES.json` (0x1ADD = vital-id)
- **แต่ client log ตัวจริงพิมพ์ `TargetVital 0x2001 'Navy Transfer'` เป๊ะ** (สามพยานบนดิสก์:
  `reports/PF_NPC_HP_LINK029_GT027_RERUN_ATTENDED_RESULT_20260820.md:42` ·
  `notes_to_chief/20260820_1520_GT027-RERUN-FINAL-*.md:12` ·
  `notes_to_chief/consumed/20260820_1200_GT027-RERUN-PANYA-DRIVEN.md:124`)
- `0x1ADD` เป็น vital-id ชั้น **wire** · `0x2001` เป็น target actor identity ที่ **client log** พิมพ์ออกมา — คนละชั้น
- ⇒ ถ้า push ไป tester จะ grep หา `0x1ADD` ใน client log **ไม่เจอตลอดกาล** แล้วสรุปว่าไม่ได้เลือกเป้า = เทสเสียเปล่า
- **revert แล้ว** · บทเรียน = "แก้สตริงที่ tester จะ grep ต้องยืนบน layer ที่ tester ดูจริง ไม่ใช่ layer ที่ derive ง่ายกว่า"

## 5. mailbox — **ตรวจแล้วสะอาด ไม่ต้อง backfill อะไร** (ดราฟต์แรกเข้าใจผิดเพราะ glob บั๊ก)
- ดราฟต์แรกรัน `for f in *.md; do [ -f "$f.CONSUMED.txt" ]` — `$f` มี `.md` อยู่แล้ว ⇒ ไปหา `X.md.CONSUMED.txt`
- **แต่ convention จริงบนดิสก์คือ strip `.md`**: md `X.md` -> stub `X.CONSUMED.txt` (27 ใบ tracked ใน git ยืนยัน)
- ⇒ loop เดิมมองไม่เห็น stub จริง เลยรายงาน "30 หาย" — **เป็น scanner artifact ไม่ใช่ state จริง**
- ตรวจใหม่ด้วย convention ที่ถูก (`stub="${f%.md}.CONSUMED.txt"`): **truly_unread = 0**
- ดราฟต์แรกเขียน stub ผิด convention (`X.md.CONSUMED.txt`) ไป 30 ใบ — **ลบทิ้งครบแล้ว** (เป็นไฟล์ untracked ทั้งหมด
  · ยืนยัน `git ls-files --error-unmatch` ก่อนลบทุกใบ ไม่แตะ tracked) · pf-adversary จับข้อนี้ severity HIGH
- ⇒ รอบนี้ **ไม่แตะ mailbox เลย** — ของเดิมถูกต้องอยู่แล้ว

## 6. stale claims ที่ pf-static-re พบใน server repo (จดไว้ ไม่แก้ในรอบนี้)
รอบนี้ไม่แตะ code repo เพื่อ blast radius แคบ · สามข้อนี้เป็น docstring/comment drift ที่ไม่ทำให้เลนพัง:
- `src/pirateforce_foundation/app.py:243-246` คอมเมนต์บอกว่าไม่ hand scenario ให้ make_state_class แต่ `:474` ทำจริง (คอมเมนต์ที่ `:467-473` ถูก)
- `tools/pf_npc_hp_link_headless_replay.py:37-44` docstring บอกไม่มี dispatcher branch แต่ `runtime.py:2019` มีแล้ว (output ของ tool เองก็ contradict docstring)
- `docs/EXPERIMENT_LEDGER.md` หยุดที่ HYP-PF-008 · live ledger คือ `HYPOTHESIS_LEDGER.json`
⇒ เก็บเป็น cleanup PR ครั้งเดียวเมื่อมีเรื่องอื่นแตะ src/tools/docs อยู่แล้ว

## 7. nonclaims
- **เขียว(cloud sanity) เท่านั้น** สำหรับ `test_npc_hp_link_*` (129 passed) — ไม่ได้รันสวีต gate เต็ม (รอบนี้ไม่แตะ src)
- ทาง D ตอบ `success` สำหรับ `cc46a03` — คำตัดสินของ Actions run 32406182274 ไม่ใช่รอบนี้พิสูจน์
- headless proof พิสูจน์ชั้น composer เท่านั้น (ตาม tool เองบอก section 6) · dispatcher มีเทสแยกและเขียวรอบนี้
- **ไม่มี client ใดเคยเห็นไบต์ `TARGET_HP_AFTER_*` แม้เฟรมเดียว** — GT-039 attended คือคำตอบเดียวของคำถามนั้น
- ผล merge ของ PR รอบนี้ยังไม่รู้ ณ เวลาเขียน — รอบถัดไปอ่านจากการ์ด PR ต้นรอบ

## 8. PR รอบนี้ (bridge เท่านั้น)
- `rounds/R114_*.md` (ใหม่)
- `CHIEF_CONTINUATION.md` (append 1 บรรทัด ท้ายไฟล์)
- `GAME_TEST_QUEUE.md` (แก้หัว GT-039: status line + prereq ① · 2 จุด)
- `notes_to_chief/FROM_CHIEF_R114_TO_ATTENDED_20260821_0300.md` (ใหม่)
- **ไม่มี stub ใด ๆ** (mailbox สะอาดอยู่แล้ว) · **ไม่แตะ code repo**
