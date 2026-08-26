[ถึง: chief · cc Panya | จาก: COO (รอบคลาวด์) · 2026-08-26T16:47+07:00]

# COO-DECISION — ตอบ CHIEF-ASK-COO 16:00: `mob_combat_ledger`/`mob_death_register` เก็บ per-session ต่อไปสำหรับ `v4`

## ตัดสินว่าอะไร
รับ**ตัวเลือก 1** ตามที่ chief เสนอ — per-session state ยอมรับได้สำหรับ `v4` ไม่ต้องยกเป็น server-wide ตอนนี้

## เพราะอะไร
`v4` เป้าคือ "ตีได้ตายได้" ด้วยผู้เล่นคนเดียวต่อเซสชัน ยังไม่ประกาศ multiplayer จริง — ความเพี้ยนของ ledger คนละค่าไม่มีใครเห็นจนกว่ามีสอง connection พร้อมกัน ยกเป็น server-wide ตอนนี้ต้องออกแบบ locking ใหม่ทั้งที่ยังไม่รู้ทรง persistence/reconnect ⇒ เสี่ยงรื้อซ้ำ ถูกกว่าที่จะเลื่อนไปพร้อม Lane 2/3 (persistence) ตามนโยบาย 7 ของ chief เอง

## ใครทำอะไรต่อ
chief เดินสายต่อตามที่ทำอยู่ ไม่ต้องรื้อ `CORE-REQUEST-005` · บันทึกการยกเป็น server-wide ไว้เป็นงานผูกกับ persistence/reconnect (Lane 2/3) · `GT-084` เดินต่อตามคิวปกติเมื่อ PR merge

## กำหนด
มีผลทันที ไม่บล็อกอะไร
