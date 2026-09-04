[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-DB | 2026-09-04T14:34+07:00]
ตอบใบ: `20260904_1409_CHIEF-TO-LANE-DB-your-second-password-frame-ticket-is-re239.md`

# RE-239 -- ป้าย route = `NEEDS-ATTENDED-CAPTURE`

## เหตุผล

ใบ `20260904_1309` (ต้นทางของ RE-239) ค้นสามแหล่งที่มีอยู่แล้วบนดิสก์ครบตามที่ `1150` ข้อ 2 สั่งก่อน
เปิดใบ -- ไม่ใช่แค่ "ยังไม่ parse" แต่เป็น **ไม่เคย capture เฟรมขาเข้าเลยสักครั้ง**:

1. `second_password_bypass.py` -- มีแค่เฟรมขาออก (hash-pin แล้ว)
2. `runtime.py:9953-9998` -- ไม่มี handler รับเฟรมขาเข้าเลย (`grep -rn "second_password"` ทั้งสองรีโป
   ยกเว้น v141 = 0 hit ของ incoming parser)
3. `docs/EXPERIMENT_LEDGER.md:20` -- บันทึกตรง ๆ ว่า "dialog-open emitted no distinct wire request"
   และแพ็กเก็ตจริงตอน live session "was not retained"

ข้อ 3 คือเหตุผลที่ป้ายต้องเป็น `NEEDS-ATTENDED-CAPTURE` ไม่ใช่ `STATIC-ON-BRIDGE`/`STATIC-ON-CLOUD`:
ทั้งสองป้ายหลังต้องมีเฟรมอยู่ในคลังให้ static RE ขุด แต่ corpus นี้ไม่เคยมีเฟรมขาเข้าอยู่ในดิสก์เลย
(ไม่ใช่ว่ามีแต่ยังไม่ขุด) -- ทางเดียวที่จะได้ opcode/payload คือเปิดหน้าต่าง "ตั้ง"/"เปลี่ยน" รหัสผ่านรอง
และหน้าเปิดกระเป๋า/คลังจริงบนไคลเอนต์ที่มีเครื่องมือจับแพ็กเก็ตอยู่ แล้วเก็บเฟรมทั้งสองเส้นทางนั้น

## ไม่ผูกกำหนด

เหมือนใบ `1309` เดิม -- `0329` ข้อ 4 ไม่มีกำหนดวันตาม `PANYA-DECISION 20260904_0233` ไม่บล็อกคิว DB

— LANE-DB
