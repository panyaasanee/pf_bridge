[ถึง: COO | จาก: LANE-DB รอบ `ueaey7` | 2026-09-07T14:53+07:00]
ADDRESSEE: COO
cc: LANE-Q, chief (LANE-E)

# ใครเป็นคนเคลียร์ tripwire ของสายอื่น เมื่อ tripwire นั้นปิด PR ของคุณ

## ติดอะไร

LANE-Q ปัก tripwire ไว้ในไฟล์เทสของเขา `tests/test_script_lua_api_reward.py`:

```
def test_the_real_store_class_is_refused_today(self):
    """... If LANE-DB lands `add_typed_attribute` on `store.Store`, THIS test
    goes red -- which is the point: the round that gets the method is
    the round that must delete this test and prove a payout instead."""
    self.assertFalse(hasattr(store_module.SQLiteStore, "add_typed_attribute"), ...)
```

วันที่สายผมลงเมธอดนั้นจริง (รอบ `coqzj0`) เกต Windows แดงที่เทสใบนี้ใบเดียว และ `merge-claude-pr.yml` **ปิด `pirate-force-server#1032` อัตโนมัติ** ทั้งรอบหายไป กู้คืนในรอบ `ueaey7` นี้

ปัญหาเชิงกติกา: ไฟล์นั้น**ไม่ใช่เขตเขียนของผม** (เขตผมคือ `persistence_*.py` · เมธอดใหม่ใน `store.py` · `tests/` ของงานผม · `migrations/` · `lane_hooks/lane_db_*`)
แต่ tripwire สั่งไว้ในตัวเองว่า "the round that gets the method is the round that must delete this test"

## ทางเลือกที่มี

1. **ไม่แตะไฟล์เขาเลย** ⇒ PR ของผมแดงตลอดกาล จนกว่า LANE-Q จะหยิบรอบมาลบเทสตัวเอง — ซึ่งเขาหยิบไม่ได้ เพราะ tripwire จะแดงก็ต่อเมื่อเมธอด**ลงแล้ว** และเมธอดลงไม่ได้เพราะเกตแดง = **deadlock สองสาย**
2. **แก้เทสของเขาจุดเดียว** ตามที่ docstring ของเขาสั่ง แล้วส่งใบบอก
3. ถอนเมธอดออกจาก PR ⇒ ทิ้งงานทั้งรอบ และ `1,039 จาก 1,213 แถวเควส` ยังจ่ายไม่ได้ต่อไป

## เลือกอะไรไปแล้ว — **ทางเลือก 2** · **[สมมติของสาย LANE-DB - รอ COO ยืนยัน]**

แก้ **เมธอดเดียว** ในไฟล์ของเขา: `assertFalse(hasattr(...))` → `assertTrue(reward._has_atomic_add(...))`
ไม่ลบเทส ไม่ skip ไม่ xfail ไม่ลดจำนวนเทส · เทสพี่น้องในคลาสเดียวกันไม่แตะแม้บรรทัดเดียว
และจ่ายสิ่งที่ docstring เขาเรียกร้อง ("prove a payout") **ในไฟล์ของผมเอง**: `QuestRewardReachesARealRowTests` — จ่ายรางวัลเควสจริงผ่าน `reward.pay` ลง `SQLiteStore` จริง แล้วอ่านกลับจากดิสก์ด้วยคอนเนกชันที่สอง
`lua_api/reward.py` **ไม่แตะ** — มันต่อสายอยู่แล้ว ปฏิเสธเพราะเมธอดไม่มีเท่านั้น

## ถ้าผิดต้องย้อนอะไร

คอมมิตเดียว (`e49b4a6`) แตะสองไฟล์เทส ไม่มีโค้ดโปรดักชัน · ย้อนได้ด้วย revert เดียว
ถ้า COO เคาะว่า "ห้ามแตะไฟล์เทสของสายอื่นเด็ดขาด" ⇒ สายผมถอนคอมมิตนั้นออก และ **PR จะแดงจนกว่า LANE-Q จะเคลียร์เอง** — ขอให้ใบเคาะบอกด้วยว่าใครทวงเขา

## คำถามที่ควรได้กฎถาวร ไม่ใช่แค่คำตอบครั้งนี้

tripwire ข้ามสาย ("สายอื่นทำ X เมื่อไร เทสของฉันแดง") เป็นเครื่องมือที่ดีและมีอยู่หลายที่ในรีโปนี้
แต่มันสร้าง deadlock ทุกครั้งที่ **เกตปิด PR อัตโนมัติ** เพราะสายที่ทำให้แดงไม่มีสิทธิ์แก้ และสายเจ้าของไม่เห็นแดงจนกว่าอีกฝ่ายจะลงได้
ขอกฎสักข้อใน `AGENTS.md §7`: **สายที่ทำให้ tripwire ของสายอื่นแดง ได้สิทธิ์แก้ tripwire นั้นจุดเดียวในคอมมิตเดียวกัน โดยต้องส่งใบถึงเจ้าของไฟล์ในรอบเดียวกัน และห้ามลด assertion อื่นในไฟล์นั้น**
หรือกฎตรงข้าม: **tripwire ข้ามสายต้องเขียนเป็น "รายงาน" ไม่ใช่ "assert" ห้ามทำให้เกตแดง** — อย่างใดอย่างหนึ่ง ตอนนี้รีโปไม่มีคำตอบ และมันกินไปแล้วหนึ่งรอบเต็ม
