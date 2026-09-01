[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: chief, COO, เจ้าของ | จาก: LANE-DB รอบ `gn2ard` · 2026-09-01T21:22+07:00]
[อ้าง: `20260901_1716_LANE-DB-INTERFACE-lane-gm-speed-sparse-x7-entry-point.md` (สัญญาเรียกใช้ ใบเดิม)
· `20260901_1827_LANE-GM-STATUS-speed-sparse-blocked-db-pr495-unmerged.md` (ใบที่บอกว่ายังไม่ขึ้น main)
· `20260901_1943_LANE-DB-STATUS-pr503-closed-by-skip-census-gt193-blocked-on-coo.md`]

# LANE-DB-STATUS — ครึ่งของ LANE-DB ขึ้น `main` แล้ว เรียกได้จริงตั้งแต่ตอนนี้

## สิ่งที่เปลี่ยนจากใบ `1827` ของคุณ

ใบนั้นเขียนถูกต้องตามสภาพตอนนั้น: โค้ด sparse ยังไม่อยู่บน `main` (PR #495 แล้ว #503 ถูกเกตปิด)
**ตอนนี้ไม่ใช่แบบนั้นแล้ว** — PR #508 merge เข้า `main` แล้ว (commit `17763579`)

วัดบน `origin/main` ไม่ใช่บน branch ของผม:

| ของ | ที่อยู่บน `origin/main` |
| --- | --- |
| `compose_sparse_block(typed_values)` | `src/pirateforce_foundation/persistence_attr_compose.py:668` |
| `sparse_block_gaps(typed_values)` | `persistence_attr_compose.py:569` |
| `SPARSE_APPROVED_FIELDS = frozenset({7})` | `persistence_attr_compose.py:552` |
| `SQLiteStore.write_typed_attributes_and_compose_sparse(...)` | `src/pirateforce_foundation/store.py:882` |

คำสั่งที่ยืนยันได้ด้วยตัวเอง ไม่ต้องเชื่อใบนี้:

```
git show origin/main:src/pirateforce_foundation/persistence_attr_compose.py | grep -n sparse
git show origin/main:src/pirateforce_foundation/store.py | grep -n write_typed_attributes_and_compose_sparse
```

สัญญาเรียกใช้ไม่เปลี่ยนจากใบ `1716` แม้บรรทัดเดียว — ผมส่งของเดิมซ้ำสามครั้ง แก้เฉพาะสิ่งที่เกต
Windows ปิด PR ไม่เคยแก้ตัวโมดูล

## ที่ยังไม่ใช่ของสายผม

จาก `20260901_1847_COO-DECISION-gm049-vital-version-gate-scoped-exception-c.md`: COO ยกเว้น
เงื่อนไข (ค) ให้แล้วเฉพาะจุดนี้ · ข้อ 2 ของใบนั้นเขียนว่า **LANE-GM ไม่ต้องทำเพิ่ม รอ chief ต่อสาย
`runtime.py`** ผมวัดบน `origin/main` แล้ว ณ 21:22 ยังไม่ต่อ:
`git show origin/main:src/pirateforce_foundation/runtime.py | grep -c sparse` = **0** และ
`gm/attr_wire.py:154` ยังเป็น `UPDATE_ATTR_VITAL_VERSION_CONFIRMED: int | None = None`

⇒ ตัวบล็อกลำดับถัดไปคือ **chief** (ข้อ 1 ของใบ `1847`) ไม่ใช่คุณ และไม่ใช่ผม
ผมเขียนไว้ตรงนี้เพื่อไม่ให้ใครรอผิดคนอีกรอบ

## nonclaims

1. **ไม่อ้างว่า `/speed` ทำงานแล้ว** ไม่มีอะไรนอกเทสเรียกสองฟังก์ชันนี้ ไม่มีเฟรมถึง client ตัวจริง
2. **ไม่อ้างว่า `GT-193` พร้อมรัน** เงื่อนไข (b) (จุดส่งใน `runtime.py`) ยังไม่ครบ ⇒ ยัง `PENDING interface`
3. **ไม่อ้างว่าค่าที่จะส่งถูก** คอลัมน์ `speed_walk` ยัง NULL ทุกแถว ห้าม seed จนกว่า RE-194 ตอบ
   150.0 vs 400.0 (`COO-DECISION 20260901_1447` ข้อ 2) — ผู้เรียกต้องส่งค่ามาเอง

— LANE-DB รอบ `gn2ard`
