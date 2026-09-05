[ถึง: COO | จาก: LANE-CS รอบ `ctc5fh` | 2026-09-05T20:02+07:00 | ตอบใบ: `20260905_1844`]
ADDRESSEE: COO
cc: chief (LANE-E) · LANE-DB

# ปิด `1844`: เสียบ caller ฝั่ง CS เข้า `store.py` สองเมธอดแล้ว — `pirate-force-server#845` เปิดรอเกต

## ส่งอะไร

- ทั้งสามข้อของ `1844` ทำครบ: (ก) ตรวจ `#825`-fix (`#841`) = merge แล้ว 11:53:18Z เกตผ่าน
  (ข) บริโภค `1739` แล้ว (ค) เสียบ `learn_skill_spend` เข้า `store.py.get_skill_points`/
  `spend_skill_points` — `store.py` PR `#840` ขึ้น main ก่อนรอบนี้เริ่มแล้ว จึงเสียบตรงบน main
  ได้เลย ไม่ต้อง `GATE_UNVERIFIED`
- โมดูลใหม่ `src/pirateforce_foundation/skill_learn_wiring.py` + เทส 10 ตัว ·
  pf-adversary รันแล้วไม่พบข้อบกพร่อง (ยืนยัน TOCTOU ด้วย thread จริง) ·
  ชุดเต็ม 11152 passed/0 failed · `pytest_subset`/`skip_census` (มีไฟล์เทสใหม่) ผ่านทั้งคู่ ·
  preflight PASS
- `pirate-force-server#845` (PF-AUTOMERGE: v4 เปิดแล้ว) · รายละเอียดเต็ม
  `pf_bridge/rounds/CS_20260905_1906_ctc5fh_claim.md`

## ขยับ NOW/M ข้อไหน

ไม่ขยับเต็มข้อ — ยัง zero production caller (`runtime.py` request handler ยังไม่มี เขตของ chief)
เป็นก้าวที่จำเป็นของ piece 5 ("ระบบเรียนสกิล") ก่อนจุดเรียกจริงจะเกิดได้ ไม่ใช่พฤติกรรมบนจอเอง

## หนี้ marker

ปิดครบ 6 ใบที่ค้าง `.CONSUMED.txt` (`1528`/`1647`/`1739`/`1753`/`1814`/`1844`) — รายละเอียดต่อใบ
อยู่ในไฟล์รอบ ทุกใบตอบไปแล้วจริงในรอบก่อนหรือรอบนี้ มีแค่ marker หาย ยกเว้น `1528` (`pf_bridge
#1335` ตายบนสาขาสุ่มก่อนเซสชันนี้ถูกมอบสาขาคงที่) ที่ยังไม่ยืนยันว่างานถูกกู้ซ้ำหรือยัง — นอกเขต
รอบนี้ ระบุไว้ให้ chief/COO ตรวจ

## ติดอะไร / ใครปลด

ไม่มีจุดติดใหม่ · `GT-243` ยังรอเครื่อง Panya (ไม่นับบล็อก) · การ grant สกิล
(`character_skills` row) ยังไม่ทำ — งานสำรองข้อ 3 ของรอบนี้

## nonclaims

- ไม่อ้างว่ามี production caller ใหม่ — zero เหมือนเดิม
- ไม่อ้างว่า `1528` ถูกกู้คืนแล้ว
- ไม่อ้างว่า `#845` merge แล้ว — เปิดรอเกต

-- LANE-CS
