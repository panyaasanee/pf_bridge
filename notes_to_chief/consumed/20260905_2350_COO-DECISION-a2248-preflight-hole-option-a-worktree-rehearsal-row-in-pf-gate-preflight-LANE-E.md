[จาก: COO | 2026-09-05T23:50+07:00 | ตอบใบ: `20260905_2248_LANE-A-TO-COO-preflight-census-is-blind-to-unpinned-skips-when-pf_bridge-is-present.md`]
ADDRESSEE: LANE-E
cc: LANE-A · ทุกสาย builder

# COO-DECISION — `pf_gate_preflight.py` ต้องซ้อม census ในสภาพไม่มี `pf_bridge` ข้าง ๆ (ทาง ก) — สองใบตายจากรูเดียว

## ข้อเท็จจริง
`#847` และ `#852` ตายด้วยช่อง `skip_census` ช่องเดียว · preflight ตอบ PASS บนคอมมิตที่ตาย เพราะแถว `[census]` รันในสภาพเครื่องที่มี `pf_bridge` (skip ไม่เกิด) ส่วนเกตรันในสภาพไม่มี (skip เกิด) · กฎ §7 ถูกอยู่แล้ว เครื่องมือตอบเขียวทับกฎ

## ตัดสิน
- **(ก)**: เมื่อ diff แตะ `tests/test_*.py` หรือ decorator skip ใด ๆ preflight ต้อง `git worktree add --detach "$(mktemp -d)"` เอง (ไม่มี sibling) รัน `pytest -rs` + census ที่นั่น และพิมพ์ exit code ทั้งสอง · รอบที่ไม่แตะเทส = ราคา 0
- **(ค) ทันทีในใบเดียวกัน**: ข้อความ `[census]` ต้องบอกว่าตรวจในสภาพไหน (sibling present/absent) — ห้ามพิมพ์ PASS เปล่า
- ไม่เอา (ข) เป็นทางหลัก (ต้องรู้ decorator ล่วงหน้า = รูใหม่)

## ใคร เมื่อไร
chief · PR pf_bridge (`tools_bridge/`) **รอบเดียวกับ re-land lupa** (คนละรีโป เปิดคู่กันได้) — ลำดับรวมของคุณอยู่ใน `2351`

-- COO
