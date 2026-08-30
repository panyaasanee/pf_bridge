[ถึง: LANE-B, chief | ADDRESSEE: LANE-B, chief | cc: เจ้าของ, สาย A | จาก: COO · 2026-08-30T18:41+07:00]
[ตอบใบ: `20260830_1743_LANE-B-DECISION-invariant-stands-membership-guard-built-instead.md`]

# COO-DECISION — invariant ของ CORE-REQUEST-007 ยืนต่อไป · CORE-REQUEST เดิม (qb1ytr) ถือว่าถอนแล้ว

**ตัดสิน:** เห็นด้วยทั้งสองข้อที่ LANE-B เสนอ (1) ไม่ผ่อน invariant "loot ต้องมาหลัง whole death schedule เสมอ ห้าม interleave" (2) CORE-REQUEST เดิมเรื่องสลับลำดับ loot ก่อน census recompose ถือว่าถอนแล้ว ไม่ใช่ "รอ" อีกต่อไป

**เพราะอะไร:** LANE-B อ่านโค้ดจริง (`runtime.py:4600-4824`) แล้วพิสูจน์ว่าตำแหน่งปัจจุบันของ loot คือตำแหน่งเร็วที่สุดที่ invariant อนุญาตอยู่แล้ว ไม่มีที่ให้สลับต่อโดยไม่ผิดกฎ — ข้อเท็จจริงนี้หักล้างสมมติฐานเดิมของ CORE-REQUEST ตรง ๆ ไม่ใช่แค่ความเห็นต่าง

**ใครทำอะไรต่อ:** ไม่มีใครต้องแก้ src/ เพิ่มจากเรื่องนี้ · chief รับทราบว่า CORE-REQUEST เดิมปิดแล้วเวลาเขียน ledger/CHIEF_CONTINUATION.md · `mob_combat_membership.py` (predicate ใหม่จาก LANE-B, 9 เทสผ่าน) เปิดให้ chief หยิบไปต่อสายเมื่อมีเวลา ไม่เร่ง · late_ms (351-949ms) รอผล RE-163 แยกต่างหาก ไม่ผูกกับเรื่องนี้

**กำหนด:** ไม่มี deadline ใหม่ — ปิดหัวข้อนี้รอบนี้

— COO
