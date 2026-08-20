# จดหมายส่งกะ — chief รอบ 114 (cloud) -> ผู้เทส/Panya · 2026-08-21 ~03:0x เวลาไทย

## TL;DR (3 บรรทัด)
1. **GT-039 (NPC-HP-LINK-001) พร้อมรันแล้วจริง ๆ** — code เข้า main แล้ว (ตั้งแต่ `cc46a03`, CI success)
   **แก้ pointer ในคิว** จากที่เดิมชี้ `outbox\178_round111_*` (gitignored หา SHA ไม่ได้) เป็น
   "บูตด้วย `origin/main` HEAD ล่าสุดที่ ci-status = success" พร้อมสามบรรทัดวิธี re-derive SHA
2. รอบนี้ **ไม่แตะ code repo** และ **ไม่แตะ mailbox** — งานเดียวคือ pointer ในคิว
3. 🔴 ดราฟต์แรกของรอบนี้เกือบแก้ของถูกให้ผิดสองจุด — pf-adversary จับได้ ทั้งคู่ revert แล้ว (ดูล่าง)

## ถึงคุณ Panya — ตอนนี้ต้องทำอะไรต่อ
**ขั้นเดียว:** เมื่อเปิดคอมเทสได้ ปลุกเซสชันหลัก (skill `pf-attended-test`) มารัน **GT-039** ได้เลย
บูตด้วย server `origin/main` HEAD ล่าสุดที่ ci-status ตอบ `success` (มีวิธี re-derive SHA สามบรรทัดในหัว GT-039)
steps/pass-criteria/nonclaims ในหัว GT-039 เหมือนเดิมทุกประการ

## รายละเอียด

### 1. ทำไม pointer เดิมพัง
- คิวเดิมชี้ `outbox\178_round111_*` · `outbox/` ถูก `.gitignore:11` (`/*`) กันไว้ ⇒ เครื่องอื่น/clone ใหม่หาไฟล์ไม่เจอตลอดกาล
- แก้เป็น re-derive: `git fetch origin main ci-status` → `SHA=$(git rev-parse origin/main)` → `git show origin/ci-status:ci/$SHA.json`
  ต้องเห็น `"sha"` ตรง `$SHA` และ `"conclusion":"success"` แล้วบูต `$SHA` นั้น
- 🔴 **ไม่ hard-pin `cc46a03`** ตั้งใจ — main อาจขยับก่อนคุณเปิดเครื่อง การ pin ตัวเลขตายจะพาไปบูต commit เก่า

### 2. หลักฐานว่า commit นั้นผ่าน gate จริง
`git show origin/ci-status:ci/cc46a0371c737c2121a9bc86119b81c5b8e595c2.json`
= `{"sha":"cc46a03...","conclusion":"success","run_id":"32406182274","utc":"2026-08-20T19:02:16Z"}`
⇒ เขียว(Actions run 32406182274) ตามสี่กฎ ci-status

### 3. cloud sanity รอบนี้ (ไม่ใช่ gate เต็ม)
- `pytest test_npc_hp_link_dispatch.py test_npc_hp_link_hypothesis.py -q` = 129 passed, 216 subtests, exit 0
- `python3 tools/pf_npc_hp_link_headless_replay.py` = 97 guards PASS, exit 0 (ไม่มี canonical DB/client image)

### 4. 🔴 สองจุดที่ดราฟต์แรกเกือบทำพัง (pf-adversary จับได้ — เล่าไว้เพื่อความโปร่งใส)
- **(a) TargetVital:** ดราฟต์แรกจะเปลี่ยน `TargetVital 0x2001` -> `0x1ADD` แต่ **client log จริงพิมพ์ `TargetVital 0x2001 'Navy Transfer'`**
  (สามพยานบนดิสก์ รวม `PF_NPC_HP_LINK029_..._20260820.md:42`) · `0x1ADD` เป็น vital-id ชั้น wire คนละชั้นกับ log ⇒ **revert**
  (คงไว้แค่เติมชื่อ `'Navy Transfer'` ให้ตรง log เป๊ะขึ้น)
- **(b) mailbox stubs:** ดราฟต์แรกคิดว่ามี stub หาย 30 ใบ แต่นั่นเกิดจาก glob บั๊ก (หา `X.md.CONSUMED.txt` แทน `X.CONSUMED.txt`)
  convention จริง strip `.md` และ stub ครบอยู่แล้ว ⇒ **mailbox สะอาด truly_unread=0** · ไฟล์ผิด 30 ใบที่เผลอเขียน ลบทิ้งครบแล้ว

### 5. queue สถานะ (คิวเทสในเกม)
- มีอะไรให้เทสไหม? **มี** — GT-039 พร้อมรัน (หลังแก้ pointer)
- ไม่มีรายการใหม่/ปิด/ย้าย (กฎ 10) · ค้างเหมือนเดิม: GT-030 · GT-031 · GT-032 · GT-033 · GT-038 · GT-039 · GT-001
- GT-034 ยังรอคุณเคาะเรื่องระยะทาง (GT-035/036 blocked ต่อ)

### 6. งาน follow-up ที่จดไว้ (ไม่ทำรอบนี้ เพราะไม่แตะ code repo)
docstring/comment drift ฝั่ง server 3 จุด (`app.py:243-246` · replay-tool docstring · `EXPERIMENT_LEDGER.md` ไม่มี HYP-PF-029)
— ไม่ทำให้เลนพัง เก็บเป็น cleanup PR ครั้งเดียวเมื่อมีเรื่องอื่นแตะ src/tools/docs

## nonclaims
- ยังไม่พิสูจน์ว่า client render `TARGET_HP_AFTER_WEAK`=37 บนแถบเป้า — คือคำถามเดียวของ GT-039 attended
- ไม่ได้รัน gate เต็มบนคลาว (7 check ต้อง client image + 1 ต้อง canonical DB · gate จริงอยู่บน Actions ของ PR)
- ผล merge ของ PR รอบนี้ยังไม่รู้ ณ เวลาเขียน — ถ้าไม่ merge ในเวลาสมควร ดู Actions log ของ `merge-claude-pr` ก่อน

## commit ของรอบนี้ (bridge เท่านั้น)
- `rounds/R114_*.md` (ใหม่) · `CHIEF_CONTINUATION.md` (+1 บรรทัดท้าย) · `GAME_TEST_QUEUE.md` (หัว GT-039 · 2 จุด) · ใบนี้
- **ไม่มี stub · ไม่แตะ code repo**
