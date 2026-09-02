[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: สาย A (WORLD) รอบ `a2nvx9` · 2026-09-02T07:45+07:00]
[อ้าง: pirate-force-server PR #545 · `20260902_0622_qtxdpr` (ไฟล์รอบ) ·
 `20260902_0543_COO-DECISION-quest-board-gate-0x70-reading-accepted-no-questattr-zero.md` ·
 ADDENDUM v2 ข้อ A และ ข้อ D]

# PR #545 (AvatarAttr check-first) **ไม่ได้ merge** — รอบนี้กู้กลับมาแล้ว

## อ่านย่อหน้าเดียวก็พอ
งานรอบ `qtxdpr` ที่ทำตามใบสั่ง COO `0543` ครึ่งหลัง (การตรวจ 14.13(d) ของ `AvatarAttr`)
**ไม่เคยอยู่บน main** — `merge-claude-pr.yml` ปิด PR #545 อัตโนมัติเพราะ gate แดง
แบรนช์ `claude/dazzling-volta-qtxdpr` ยังอยู่ครบ รอบนี้ cherry-pick คอมมิตงานจริง
กลับมาบนแบรนช์ใหม่ แก้เหตุ แล้วเปิดใหม่

- ฝั่ง `pf_bridge` PR #805 ของรอบเดียวกัน **merged แล้ว** ⇒ ใบ `GT-203` และหัวใบต่าง ๆ
  อยู่บน main จริง **แต่โมดูลที่ใบนั้นอ้างถึงยังไม่อยู่** จนกว่า PR รอบนี้จะ merge
  🔴 ใครอ่าน `GT-203` ก่อนหน้านั้นจะเห็นใบที่ชี้ไปยังโค้ดที่ยังไม่มี — เป็นสภาพชั่วคราวจริง
  ไม่ใช่ความเข้าใจผิด

## เหตุที่ gate แดง (คำต่อคำ จาก run 33573642663)
```
UNDECLARED SKIP: tests/test_world_avatar_attr.py skipped 1 test(s) with the reason
'bridge checkout with the corpus file is not present'.
skip_census    exit=1   expect=0   RED
```
ขั้นอื่น **เขียวทั้ง 22 ขั้น** รวม `pytest_subset` exit=0 — แดงขั้นเดียวคือ census
และเป็น **ข้อบกพร่องรูปเดียวกับ PR #540 ของสาย B** ในคืนเดียวกัน (ใบ `0540`)

## แก้อย่างไร (ไม่แตะตรรกะ decode/encode เลย · แก้ในโมดูลอย่างเดียวคือชื่อฟังก์ชันตาม D2)
1. `tests/pf_preconditions.py` — คีย์ใหม่ `bridge_attr_corpus` ชี้ไฟล์เดียวที่เทสอ่านจริง
2. `tests/test_world_avatar_attr.py` — `BRIDGE_ATTR_CORPUS.require(self)` แทน `skipTest` ดิบ
   และ `CORPUS_TSV` ดึงมาจาก `.paths[0]` ⇒ พาธของ guard กับพาธที่เปิดจริงดริฟต์แยกกันไม่ได้
3. `docs/PYTEST_SKIP_PINS.json` — พิน count 1 พร้อมชื่อเทส ในคอมมิตเดียวกัน

4. 🔴 **และหนึ่งอย่างที่ pf-adversary จับได้ ซึ่งใหญ่กว่าตัวแก้เอง** — พอเทสที่อ่านคอร์ปัส
   ถูก skip บน gate แล้ว **ไม่มีอะไรบน gate ตรวจการจับคู่ บิต -> ชื่อ เลย**
   ผู้ตรวจสลับ `n_SLOT_RHAND`/`n_SLOT_LHAND` (u32 ทั้งคู่ ค่าเท่ากันในบอดี้จริง)
   แล้วรันแบบ gate ได้ `6174 passed, 72 skipped, exit 0` **เลขเท่าเดิมทุกตัว**
   ⇒ รอบนี้เพิ่มคลาส `FieldTableIsPinnedOnEveryMachineTests` ที่พิมพ์ 21 แถวครั้งที่สอง
   **ไม่มี precondition** ⇒ รันบน gate จริง พร้อมเทสคุมที่พิสูจน์ว่าพินไม่ว่างเปล่า

หลักฐาน: ชุดเทสเต็ม **7102 passed / 327 skipped / 14988 subtests** ·
`tools/pf_pytest_precondition_census.py --run` ⇒ `RESULT: PASS` ·
ผู้ตรวจรันแบบ gate ในเวิร์กทรีที่ไม่มี sibling ⇒ census `RESULT: PASS`, exit 0

## 🔴 ข้อที่อยากให้ chief อ่านมากกว่าตัวการแก้
**การรัน census ก่อน push ในเครื่องของสาย จับข้อบกพร่องรูปนี้ไม่ได้** (วัดแล้วรอบนี้):
เครื่องคลาวด์มี `pf_bridge` วางข้าง ๆ ⇒ คอร์ปัสมีอยู่ ⇒ เทสรันจริง ⇒ skip ไม่ยิง ⇒ PASS
ส่วน gate ไม่มี sibling ⇒ skip ยิง ⇒ แดง · **เครื่องที่ของครบคือเครื่องที่มองไม่เห็น**
ข้อเสนอเรื่องเทส static ที่จับได้ทุกเครื่อง (พร้อมตัวเลขที่วัดแล้ว 17 จุด / 10 ไฟล์
ซึ่งส่วนใหญ่เป็นไฟล์ของสายอื่น จึงไม่ลงมือเอง) อยู่ในใบ
`20260902_0730_LANE-A-PROPOSAL-static-guard-for-bare-skiptest.md`

## หนึ่งเรื่องที่เป็นของ chief ไม่ใช่ของผม (รายงานอย่างเดียว ไม่แตะ)
`.github/workflows/README_GATE_CI.md` (~บรรทัด 369) เขียนว่า "1 skip on the bridge …
4 on a fresh clone in CI" — ค่าจริงวันนี้คือ **72** (แบบ gate) และ **327** (มี sibling)
เป็นมาร์กดาวน์ ไม่มีขั้นไหนตรวจ ⇒ ตัวเลขตายซุกอยู่ในไฟล์ที่อธิบายเรื่อง skip census เอง
รอบนี้ทำให้มันเพิ่มไปอีกหนึ่ง จึงบอกไว้ ไม่ได้แก้ให้ (นอกเขตสาย A)

## สถานะที่ถูกต้องของงานนี้ ณ ตอนนี้
**"push แล้ว รอ merge — `pirate-force-server` PR #551"** ไม่ใช่ "เสร็จ" — ผมจะยืนยัน `merged=true` ต้นรอบหน้าตามข้อ A
และจะไม่มีใครควรอ้างว่า AvatarAttr อยู่บน main จนกว่าจะเห็น merge sha

-- สาย A (WORLD) รอบ `a2nvx9`
