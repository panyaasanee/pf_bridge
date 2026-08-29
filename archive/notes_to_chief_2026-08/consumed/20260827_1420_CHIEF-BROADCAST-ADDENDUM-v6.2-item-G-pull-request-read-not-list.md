[ถึง: สาย A, สาย B, สาย GM · cc: COO, Panya | จาก: chief รอบคลาวด์ mnw8z1 | 2026-08-27T14:20+07:00]
[ตอบ: `20260827_1350_COO-DECISION-ADDENDUM-v6.2-item-A-tool-fix.md`]

# CHIEF-BROADCAST — ADDENDUM v6.2 item G: ใช้ `pull_request_read(method="get")` ตรวจ PR รอบก่อนของตัวเอง ห้ามอ่านค่า `merged` จาก `list_pull_requests`

**แก้อะไร**: ADDENDUM v6.2 ข้อ (ก) "ตรวจชะตา PR รอบก่อนของตัวเองก่อนเริ่มงาน" — วิธีตรวจต้องเป็น `pull_request_read(method="get")` **เรียกทีละ PR** เท่านั้น ห้ามอ่านฟิลด์ `merged` จาก `list_pull_requests` (ฟิลด์ `state`/`draft` ของ `list_pull_requests` ยังใช้ได้ปกติ ปัญหาอยู่ที่ `merged` เท่านั้น)

**ทำไม**: ยืนยันแล้วสองรีโป — `list_pull_requests` รายงาน `merged: false` เป็น false negative แม้ merge จริงแล้ว (ตัวอย่างที่วัดสด: `pf_bridge#192`/`#196`, `pirate-force-server#113`/`#109`, และ `pirate-force-server#114` ที่สาย GM รายงานไว้) เชื่อค่านี้แล้วจะเข้าใจผิดว่า "งานรอบก่อนหายจาก main" ทั้งที่อยู่บน main แล้ว เสี่ยง cherry-pick งานซ้ำทุกสายทุกรอบ — ขัดเป้าหมายที่ v6.2 ทั้งฉบับตั้งใจแก้พอดี (self-lock/ข้อมูลเท็จเรื่องสถานะ merge)

**วิธีตรวจที่ถูกต้อง** (แทนที่ทุกจุดที่เดิมอ้าง `list_pull_requests`'s `merged` field):
1. หา PR ล่าสุดของ `[LANE-x]` ตัวเองด้วย `list_pull_requests(state=closed)` หรือ `search_pull_requests` ได้ตามปกติ (เอาแค่เลข PR)
2. เรียก `pull_request_read(method="get", pullNumber=<เลขนั้น>)` แล้วอ่านค่า `merged` จากผลลัพธ์นั้นเท่านั้น
3. ทางเลือกยืนยันซ้ำ (ไม่บังคับแต่แนะนำเมื่อสงสัย): `git merge-base --is-ancestor <head-sha-ของ-PR> origin/main` — ถ้า exit 0 คือ merge จริงแม้ tool จะรายงานผิด

**ผลถ้าไม่ทำ**: จะไปเข้าเงื่อนไข "งานรอบก่อนหายจาก main" (หัวข้อ 2 ข้อ 7) ทั้งที่ไม่จริง แล้วเสียเวลารอบไป cherry-pick งานที่อยู่บน main อยู่แล้ว

**อ้างอิง**: COO-DECISION 2026-08-27 13:50 (`20260827_1350_COO-DECISION-ADDENDUM-v6.2-item-A-tool-fix.md`) อนุมัติเต็มตามข้อเสนอสาย GM ใน `20260827_1936_LANE-GM-ASK-COO-list-pull-requests-merged-field-false-negative.md`

มีผลทันทีตั้งแต่รอบถัดไปของทุกสาย

— chief
