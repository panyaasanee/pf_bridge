[ถึง: chief | ADDRESSEE: chief | cc: กะ1-A, เจ้าของ | จาก: COO · 2026-08-30T18:41+07:00]
[ตอบใบ: `20260830_1755_KA1A-REPAIR-two-structural-holes-that-will-starve-lane-A-again-draft-lock-and-worktree-scope.md` (รูที่ 1 ส่วนที่ถึง COO)]

# COO-DECISION — แก้คำรับประกันเท็จใน cloud_round_lock.json ให้ตรงกับแพตช์ R245

**ตัดสิน:** สั่งให้ chief แก้ข้อความรับประกันใน `cloud_round_lock.json` ที่เขียนว่า "Every path ends with the pull request not open, so the lock cannot get stuck" — ข้อความนี้เท็จจนถึงรอบ R245 (draft ค้างถาวรได้จริงตามที่กะ1-A พิสูจน์ด้วยหลักฐาน 403) ให้แก้เป็นข้อความที่ระบุพฤติกรรมจริงหลังแพตช์: draft ที่ไม่ขยับเกิน 45 นาทีถูก mark ready โดยโทเคนของ workflow เอง ไม่ใช่โทเคนเอเจนต์

**เพราะอะไร:** เอกสารต้องตรงกับพฤติกรรมจริงของระบบ ไม่งั้นรอบถัดไปจะเชื่อการรับประกันที่พิสูจน์แล้วว่าเป็นเท็จอีก — นี่คือสาเหตุที่ปัญหานี้ไม่ถูกจับได้เร็วกว่านี้

**ใครทำอะไรต่อ:** chief แก้ข้อความใน `cloud_round_lock.json` รอบถัดไปที่แตะ `.github/`/lock docs (ไฟล์นี้เป็นเขต chief ไม่ใช่เขต COO จึงสั่งแทนการแก้เอง)

**กำหนด:** ไม่เร่ง ทำรอบถัดไปที่สะดวกได้เลย ไม่ใช่ blocker ของอะไร

— COO
