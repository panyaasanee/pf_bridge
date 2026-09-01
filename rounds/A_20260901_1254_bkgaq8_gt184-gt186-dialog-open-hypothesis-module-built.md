# LANE-A round `bkgaq8`

2026-09-01T12:23+07:00 - 2026-09-01T12:54+07:00 (+07:00 via `TZ=Asia/Bangkok date`).

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ไม่มี — โมดูลใหม่ยังไม่ต่อสายเข้า `runtime.py` เลย
(`production_allowed = False`, ตั้งใจ) รอบนี้เป็นรอบสร้างของ + CORE-REQUEST ให้ chief ต่อสาย
ผู้เล่นจะเห็นความต่างจริงก็ต่อเมื่อ wiring landed + attended run ยืนยัน (`GT-184`/`GT-186`)

## 0. บริบทก่อนเริ่ม (ตรวจ mailbox + PR รอบก่อนก่อนเชื่อ prompt เก่า)

อ่าน `pf_bridge/NOW.md` ก่อนเริ่มตามกฎ 🔴 — สถานะ "มีงานด่วน 3 ข้อ" (P-1/P-2/P-3, PANYA-ORDER
`20260901_0215`) ไม่มีข้อไหนอยู่ในเขตเขียนของสาย A โดยตรง (P-1/P-2/P-3 เป็นของ LANE-B/GM/DB ตาม
ที่ NOW.md เองระบุสถานะไว้) แต่คิวถัดไปใน NOW.md เดียวกันมี **UI-A/UI-B** ซึ่งตรงกับ `GT-184`/
`GT-185`/`GT-186` ที่ chief broadcast มอบให้ **LANE-A** เป็น build-owner lane ไว้แล้วอย่างชัดเจน
(`GAME_TEST_QUEUE.md`) เลือกหัวข้อนี้แทนที่จะรายงานรอบว่าง

ตรวจ GitHub API ตามข้อ A ของ ADDENDUM v2: PR ล่าสุดของสาย A ทั้งสองรีโป —
`pirate-force-server#465` (`merged: false`) และ `pf_bridge#700` (`merged: true`) `#465` ไม่ได้
หายจาก main จริง — chief's `FROM_CHIEF_R286_TO_LANE-A` (บริโภคแล้วรอบนี้) ยืนยันว่าเนื้องานของ
`#465` (bg0004 composer+wiring) มีอยู่บน `main` แล้วทั้งหมดตั้งแต่รอบ `bq4mst` ก่อน `#465` จะเปิด
เสีย — ไม่ต้อง cherry-pick อะไร (list_pull_requests's `merged` field ไม่น่าเชื่อถือ ตรวจด้วย
`pull_request_read get` ตรง ๆ แทนทุกครั้ง)

Mailbox: grep `ADDRESSEE: LANE-A` ไม่มี `.CONSUMED.txt` คู่ = 3 ใบ (สอง COO-DECISION ปิดแล้วไม่มี
งานต่อ, จดหมาย chief R286 แจ้งไว้เฉย ๆ) บริโภคครบ วาง stub + สำเนาไป `consumed/` แล้ว
(`pf_bridge` commit `e50a9be`) ไม่มี `*CLAIM-LANE-A*` ค้าง ไม่มี `[LANE-A]` PR เปิดค้างต้นรอบ ->
เปิด draft PR ยึดล็อกทั้งสองรีโป (`pf_bridge#704`, `pirate-force-server#471`)

Fast-forward: `pirate-force-server` local อยู่ที่ `653b4d3` ตรงกับ `git ls-remote origin main`
เป๊ะ (การ fetch ครั้งแรกได้ ref ค้างจาก proxy/cache ต้อง force-update ก่อน) `pf_bridge` ตรงอยู่แล้ว

## 1. ทำไมเลือกหัวข้อนี้

`RE-189` (ปิดแล้ว รอบ `yv3k9x`) ทิ้ง `BUILD_IMPACT` ไว้ตรง ๆ ว่ากิ่ง 2/3/6 ของ response-policy
ใหม่สำหรับ `GT-033`/`GT-184`/`GT-186` **buildable โดย LANE-A ในรอบถัดไปที่มีที่ว่าง** (เลื่อนรอบ
`yv3k9x` เองเพราะ PANYA-ORDER `09:55` เร่งด่วนกว่า) — census latch (PANYA-ORDER `09:55`) ปิดไป
แล้วส่วนใหญ่ตั้งแต่รอบ chief `8zf80f`/`R285` นี่คือรอบว่างที่มีที่ว่างจริงตามที่ `RE-189` รอไว้ และ
`GT-184`/`GT-186` เป็นสองใบที่ NOW.md เองบอกว่า "บล็อกเจ้าของสองรอบเทสติดกันแล้ว เสียรอบ attended
ทั้งรอบทุกครั้ง" — priority สูงกว่า backlog อื่นที่ไม่ได้บล็อกรอบเทสจริง

## 2. งานที่ทำ — โมดูล branch 6 (ส่ง 0x709E ตอน dialog เปิด)

รายละเอียดเชิงเทคนิคเต็มอยู่ในดอกสตริงของ
`src/pirateforce_foundation/logout_dialog_open_hypothesis.py` เอง (เขียนให้อ่านจบแล้วเข้าใจได้
โดยไม่ต้องกลับมาอ่านรอบนี้อีก) สรุปสั้น: standalone dispatch function ที่ reuse composer/
classifier เดิมทั้งคู่ไม่เขียน byte ใหม่ guard shape เดียวกับ `_dispatch_logout_chat_push_
hypothesis` (HYP-PF-031) ทุกจุด ยังไม่ต่อสายเข้า `runtime.py` — เป็น dead code บน `main` จนกว่า
CORE-REQUEST จะถูกทำ

`tests/test_logout_dialog_open_hypothesis.py`: 12 เทสใหม่ ผ่านทั้งหมด สวีตเต็ม
`6228 passed / 327 skipped`, 0 failure (ก่อน/หลังงานนี้)

## 3. pf-adversary (บังคับก่อน commit)

พบข้อบกพร่องจริงหนึ่งจุด: ทางเลือกการต่อสาย (b) ที่ดอกสตริงร่างแรกเสนอไว้ (thread flag เข้า
`_dispatch_worldinfo_observation` เดิม) จะทำให้ `self.rx_frames` นับซ้ำสองครั้งต่อเฟรม เพราะทั้ง
ฟังก์ชันเดิมและฟังก์ชันใหม่ต่าง `+= 1` เอง ไม่มี carve-out แบบที่ `_dispatch_mob_combat`
(`runtime.py:4113-4127`) ทำไว้แล้วสำหรับกรณีถูกเรียกซ้อน — แก้ดอกสตริงให้ระบุทางเลือก (a) เป็น
ทางที่แนะนำ และเตือนทางเลือก (b) ชัดเจนก่อน commit (ดู CORE-REQUEST) ตรวจ line pointer ทุกจุดใน
ดอกสตริงกับไฟล์จริง ตรงหมด ตรวจเทสไม่ mock จนกลวง (compose-refusal เทส patch ชื่อที่ผูกจริงใน
namespace ของโมดูลใหม่ ไม่ใช่ no-op) — ผ่านหลังแก้

## 4. CORE-REQUEST ถึง chief

wire โมดูลเข้า `runtime.py` ตามที่ระบุในดอกสตริงไฟล์ + จดหมาย
`notes_to_chief/20260901_1254_LANE-A-CORE-REQUEST-wire-logout-dialog-open-hypothesis-gt184-gt186.md`
ใช้ทางเลือก (a) เท่านั้น (ห้าม (b) ตามที่ pf-adversary จับได้)

อัปเดตหัวใบ `GT-184`/`GT-186` ใน `GAME_TEST_QUEUE.md` ให้ชี้มาที่ PR นี้ + สถานะ "ยังไม่ต่อสาย"

## ยังไม่ได้พิสูจน์

- ยังไม่มีใครวัดว่าการ push `0x709E` ตอน dialog เปิดจะทำให้ client transition จริง — รอ wiring +
  attended run (`GT-184`/`GT-186`)
- `HYP_PF_040` เป็นเลขชั่วคราว grep ว่างตอนเขียน ยังไม่ได้จองใน `docs/HYPOTHESIS_LEDGER.json`
  (นอกเขตสายนี้รอบนี้) — คนต่อสายต้องตรวจซ้ำว่ายังว่าง
- ไม่ได้สร้างฟังก์ชันคู่ "ปฏิเสธ LogoutVital เงียบ" — เปิดเป็นคำถามให้ CORE-REQUEST ตัดสินใจแทน
  ไม่ใช่การตัดสินใจของรอบนี้

-- LANE-A (round `bkgaq8`)
