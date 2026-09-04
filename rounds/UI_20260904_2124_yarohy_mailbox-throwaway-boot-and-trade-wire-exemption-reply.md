# LANE-UI round `yarohy` — สองใบในกล่องจดหมาย: บูตกิ่งทิ้ง HYP-PF-040 + ตอบ chief เรื่อง exemption

เวลา: 2026-09-04 21:24 +07:00 (`TZ=Asia/Bangkok date`)

## รอบนี้ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
**ไม่ขยับ M-ladder** (M2 คงเดิม — ตัวบล็อกเดียวที่เหลือคือ chief แก้หัวใบ `GT-233` เป็น READY ซึ่งไม่ใช่ของสายนี้)
รอบนี้เคลียร์กล่องจดหมายสองใบที่ค้าง (ทั้งสองมาก่อนคิวของตัวเองตาม §7 ข้อ 3) — ไม่มีข้อไหนใน "รอเครื่องคุณ"/M-ladder
ที่ผมมีสิทธิ์ปิดเองได้ในรอบนี้ (ทั้งคู่เป็นแค่ mail handling ไม่ใช่โค้ดปิดใบ)

## ลำดับตาม §7
1. `git fetch origin main` ทั้งสองรีโป (bridge → `242ffe8` (force-updated) · server → `433fde4`) ·
   `checkout -B` จาก `origin/main` ทั้งคู่ · list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — **ไม่มี** ⇒ ไม่ต้องถอย ·
   claim `claude/lane-ui-round-yarohy` (pf_bridge เท่านั้น — ใช้กิ่งเซสชัน `claude/wizardly-knuth-yarohy` เป็นกิ่งพาหะจริง)
2. รอบก่อน (`n4vqwx`) ไม่มี `ADVERSARY_PENDING` ค้าง (ไฟล์รอบเขียนไว้ชัดว่า adversary คืนผลก่อน push จริง)
3. กล่องจดหมาย `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` ข้าม `.CONSUMED.txt` — พบสองใบไม่ consumed:
   - **`2016`** (chief · การ์ด quest/shop recursive นอกเกต hit เขตผม 1 โมดูล 4 symbol ใน
     `lane_ui_trade_wire_log.py`) — ต้องตอบว่าขอ exemption หรือเปลี่ยนชื่อ ก่อนเส้นตาย 2026-09-05 03:21
   - **`2047`** (COO-DECISION HYP-PF-040 · อนุญาต LANE-UI push กิ่งทิ้งหนึ่งคอมมิตบน `pirate-force-server`
     พลิก `logout_dialog_open_hypothesis.production_allowed = True` ห้ามเปิด PR แล้วเขียนจดหมายถึง ka1-A
     ระบุ hash) — ตอบใบ `1953` ของรอบ `n4vqwx` เอง กำหนดส่งรอบ 21:16
4. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน — **ไม่สั่งรอบนี้** เพราะไม่มี PR เปิดกับกิ่งทิ้ง (`2047` ข้อ 1: "ไม่มี PR
   = workflow ไม่แตะ") และจดหมายตอบ chief (`2016`) ไม่ใช่โค้ด — เขตงานรอบนี้ทั้งหมดอยู่นอกเกณฑ์ที่ต้องผ่าน
   adversary (โค้ดจริงที่แก้ = บรรทัดเดียวในกิ่งทิ้งที่ไม่มี PR)

## ทำอะไร

### ใบ `2047` — บูตกิ่งทิ้ง HYP-PF-040 (COO อนุมัติหนึ่งครั้ง)
อ่านไฟล์จริงก่อนแก้: `pirate-force-server/src/pirateforce_foundation/logout_dialog_open_hypothesis.py:248`
มี `production_allowed = False` ตรงตามที่รอบ `n4vqwx` วิเคราะห์ไว้ — สร้างกิ่งทิ้งใหม่จาก `origin/main`
(`claude/hyp-pf-040-throwaway-yarohy`) พลิกบรรทัดเดียวเป็น `True` คอมมิตเดียว push ขึ้น GitHub
**ไม่เปิด PR** (ยืนยันด้วยตาว่า workflow list PR เปิดของ `pirate-force-server` ไม่มีรายการนี้หลัง push)
แล้วสลับกลับกิ่งเซสชัน `claude/keen-gates-yarohy` ทันที (ไม่ทำงานต่อบนกิ่งทิ้ง)

- กิ่งทิ้ง: `claude/hyp-pf-040-throwaway-yarohy`
- commit: `e678a376a274f5ba3d1f3e30e86bf1c43df1047c`
- เขียนจดหมายถึง ka1-A ตามข้อ 3 ของ `2047`: hash + แฟล็กเดิมทุกตัว (ไม่แตะอย่างอื่น) + **STOP-on-close บังคับ**
  → `notes_to_chief/20260904_2120_LANE-UI-TO-KA1A-hyp-pf-040-throwaway-branch-boot-hash-and-stop-rule.md`
- ยังไม่รันเอง ไม่มีหลักฐานจอ — ผลรอ ka1-A รอบ attended ถัดไป

### ใบ `2016` — ตอบ chief เรื่อง exemption ของ `lane_ui_trade_wire_log.py`
อ่านทั้งไฟล์ `lane_hooks/lane_ui_trade_wire_log.py` และ `ui_trade_wire.py` ก่อนตอบ (ไม่เดา) — ยืนยันว่า 4
symbol ที่ถูก hit (`_on_trade_invite`, `decode_trade_invite_payload`, `encode_trade_invite_payload`,
`ui_trade_wire`) ทั้งหมดตั้งชื่อตาม `TradeInviteVital` (opcode `0x3700`) ที่ RE ยืนยันแล้ว ไม่ใช่คำที่เลือกเอง
เพื่อสื่อความหมายร้านค้า/เทรด และโมดูลเป็น log-only (`bytes_out=0` ทุกบรรทัด) ตาม CORE-REQUEST `1120` —
ไม่ใช่การสร้างระบบร้านค้า/เทรดจริงที่การ์ด quest/shop ควรจับ ⇒ **ขอ exemption ทั้ง 4 symbol** ไม่ขอเปลี่ยนชื่อ
(เปลี่ยนชื่อจะตัดการตามรอยกลับไปยังชื่อเฟรมของไคลเอนต์ ซึ่งเป็น convention เดียวกับ
`lane_ui_party_wire_log.py`/`lane_ui_friend_wire_log.py`/`lane_ui_mail_wire_log.py` ทุกตัว)
→ `notes_to_chief/20260904_2121_LANE-UI-TO-CHIEF-trade-wire-log-four-symbols-request-exemption-not-rename.md`
· ไม่ได้แก้ไฟล์ในเขตตัวเองรอบนี้ — รอคำตัดสินของ chief ในขั้น 2 (เส้นตาย 2026-09-05 03:21)

## ADVERSARY
ไม่สั่งรอบนี้ (ดูเหตุผลข้อ 4 ข้างบน) — ไม่มีโค้ดที่ผ่าน PR ให้รีวิว

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR หัว `[LANE-UI] round yarohy: claim` กิ่ง `claude/wizardly-knuth-yarohy` — ไฟล์รอบนี้ + จดหมายใหม่
  2 ใบ (`2120` ถึง ka1-A, `2121` ถึง chief) + `.CONSUMED.txt` ของใบ `2016`/`2047`
- `pirate-force-server`: **ไม่มี PR** — มีแค่กิ่งทิ้ง `claude/hyp-pf-040-throwaway-yarohy` (commit
  `e678a376a274f5ba3d1f3e30e86bf1c43df1047c`) ตามที่ `2047` สั่งห้ามเปิด PR ตรงๆ · กิ่งเซสชัน
  `claude/keen-gates-yarohy` ไม่มีคอมมิตใหม่รอบนี้ (ไม่มีอะไรอยู่ในเขตเขียนที่พร้อมทำโดยไม่เดา opcode)
- ไม่มี GT/RE ใหม่ · ไม่มีเลข CORE-REQUEST ใหม่

## nonclaims
① ไม่ได้รันไคลเอนต์เอง ไม่มีหลักฐานจอสำหรับกิ่งทิ้ง HYP-PF-040 — ผลรอ ka1-A
② ไม่ยืนยันว่า chief จะเห็นด้วยกับข้อเสนอ exemption — เป็นข้อเสนอ ไม่ใช่คำตัดสิน
③ ไม่แตะ UI-A/UI-B (`world_logout_button_notice.py`) รอบนี้ — เขตงานจริงที่เหลือ (ทำให้ปุ่มเปลี่ยนหน้าจอจริง)
   ยังบล็อกด้วยข้อสรุปเดิมของ `RE-189`: field ที่ client ใช้ตัดสินทรานซิชันเป็น local-UI-only ไม่มีเฟรมเขียนถึง
   — ยังไม่มีหลักฐาน RE ใหม่ที่พลิกข้อสรุปนั้น จึงไม่มีเฟรมให้ต่อสายโดยไม่เดา (กติกา §0 ห้ามเดา opcode)
④ ตรวจงานสำรองของรอบก่อน (`n4vqwx`) ทั้ง 3 ข้อแล้ว — ข้อ 3 (รอผล `1953`) ปิดแล้วรอบนี้ (คือใบ `2047`) ·
   ข้อ 1 (`RE-236`) ยังค้าง `[NEEDS-ATTENDED-CAPTURE]` ("รอเครื่องคุณ" ข้อ 7 · ไม่บล็อก LANE-UI) · ข้อ 2
   (CORE-REQUEST `0621` เงิน/กระเป๋าร้านค้า) ยังไม่มีความคืบหน้าใหม่จาก LANE-DB (grep `notes_to_chief/*LANE-DB*`
   ล่าสุด = งาน piece3/piece4/scene-select ของ PLAYER/CHARACTER ยังไม่ถึงคิวร้านค้า)

## งานสำรอง (พร้อมเริ่มได้ทันทีรอบถัดไปถ้างานหลักติด — ตาม `PANYA 1450` ข้อ 6)
1. เช็คว่า `RE-236` พ้นสถานะ `PENDING (RESERVED)` แล้วหรือยัง (`CLIENT_RE_QUEUE.md:4908`) — ถ้า Panya จับ
   differential ที่เครื่องแล้วและผลยืนยัน client-local ล้วน (ตรง `RE-115`) ⇒ เขียนโมดูล `ui_*.py` บันทึกผลปิด
   คิวข้อ 4 ของสารบัญ
2. เช็คว่า CORE-REQUEST `0621` (LANE-DB เงิน/กระเป๋าร้านค้า NPC) มีอินเทอร์เฟซใหม่จาก LANE-DB หรือยัง — ถ้ามี
   กลับมาต่อสาย `TradeCmdVital` ทันที
3. เช็คว่า chief ตอบใบ `2121` (exemption 4 symbol ของ `lane_ui_trade_wire_log.py`) แล้วหรือยัง — ถ้าสั่งเปลี่ยนชื่อ
   แทน exemption ให้ทำในรอบถัดไปก่อนเส้นตายขั้น 2 (2026-09-05 03:21) · เช็คด้วยว่าผล GT-184/GT-186 จากกิ่งทิ้ง
   (`e678a37`) กลับมาจาก ka1-A หรือยัง — มีผล ⇒ รายงาน COO ตามข้อ 4 ของ `2047`

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
1. เช็คงานสำรองข้อ 1-3 ข้างบนตามลำดับ
2. ถ้าไม่มีอะไรขยับ กลับไปอ่านสารบัญ 15 แถวเดิม (`0400`) หารายการที่ RE ใบใหม่ปิดระหว่างที่ผ่านมาแต่ยังไม่ถูก
   ต่อสาย

— LANE-UI รอบ `yarohy`
