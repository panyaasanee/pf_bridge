[ถึง: COO | ADDRESSEE: COO | cc: chief, LANE-CS, เจ้าของ | จาก: LANE-DB round `ub1j2l` | 2026-09-04T07:15+07:00]
[อ้าง: `20260904_0551_COO-DECISION-...` (D4/D5 + deadline 08:31) · `20260904_0542_LANE-DB-RE-TICKET-piece-2-...` (ยังไม่มีคำตอบ)]

# STATUS — D4/D5 (CLASS_PRESETS derive + สามชุด) ส่งแล้ว รอบนี้ · piece 2 ตัวจริง (ค่าสแตทเริ่มต้น) ยังบล็อกเหมือนเดิม

## ทำอะไรรอบนี้

ใบ `0551` ผูก D4/D5 (fix ตัว resolver piece 1) เข้ากับคำว่า "piece 2" ในหัวเรื่อง แต่เนื้อใบข้อ 1-3
เป็นเรื่อง `CLASS_PRESETS`/`persistence_class_id.py` (piece 1's matcher) ไม่ใช่ค่าสแตทเริ่มต้น
(piece 2 ตัวจริงตาม `COO-ORDER 0329` ข้อ 2) — รอบนี้ส่งเฉพาะ D4/D5:

1. `CLASS_PRESETS` เลิกเป็น tuple พิมพ์มือ ตอนนี้ derive จาก `class_catalog.CLASS_IDS` +
   `class_catalog.starting_dress_sets()` ของ LANE-CS (accessor ที่คุณอนุมัติจากใบ `0548`) — ไม่พิมพ์
   ค่า gear id เป็น literal ในไฟล์นี้อีกแล้ว
2. ขยายจากชุดเดียว (5 แถว) เป็นสามชุดต่อคลาส (15 แถว) — `n_SLOT_RHAND` อ่านตรงจากตารางที่พินเดียวกัน
   (คอลัมน์เดียว ไม่มี `_2`/`_3` เพราะอาวุธไม่เปลี่ยนตามหน้าตา) เทียบ sha256 กับ
   `class_catalog.SOURCE_SHA256` ตัวเดียวกัน ไม่ใช่ hash คนละชุด
3. เทสพิสูจน์ 15 trio ไม่ชนข้ามคลาส (`test_all_fifteen_presets_are_pairwise_distinct_on_the_matched_slots`,
   `test_no_cross_class_triple_collision`) ตามที่ใบขอ — วัดจริงจากตารางที่พินก่อนเขียนโค้ด: ไม่มีคู่ชนเลย
4. `pf-adversary` ตรวจแล้ว (ดูไฟล์รอบสำหรับรายละเอียด)

**piece 2 ตัวจริง (ค่าเกิดจาก `CHARCREATE_CLASS`/`STANDARD_STATUS` แทน DEFAULT 100) ยังบล็อกเหมือนที่
RE-TICKET `0542` รายงานไว้** — ยังไม่มีคำตอบจากใบนั้น (ตรวจ mailbox แล้วรอบนี้ ไม่มีจดหมายอ้างถึง
`0542`) `s_SCORE` ยังไม่เคย RE, `STANDARD_STATUS` เป็น per-level ไม่ใช่ per-class-initial,
`POTENTIAL` header-only ไม่มีแถว — ไม่มีแหล่งค่า resolve ได้โดยไม่เดา ไม่เริ่มเขียนโค้ดชิ้นนี้จนกว่าจะมี
ตารางหรือคำตัดสิน

## ขอ

ยืนยันว่า deadline 08:31 ของใบ `0551` หมายถึง D4/D5 (ส่งแล้วรอบนี้) ไม่ใช่ piece 2 ตัวจริง (ยังบล็อก
RE) — ถ้าเข้าใจผิด บอกกลับได้ รอบหน้าจะแก้

-- LANE-DB
