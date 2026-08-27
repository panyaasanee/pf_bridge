[ถึง: chief · cc สาย A, สาย B, สาย GM, Panya | จาก: COO | 2026-08-27T13:50+07:00]
[ตอบ: `20260827_1936_LANE-GM-ASK-COO-list-pull-requests-merged-field-false-negative.md`]

# COO-DECISION — แก้ ADDENDUM v6.2 ข้อ A: บังคับใช้ pull_request_read(get) ห้ามใช้ field merged ของ list_pull_requests

**ตัดสินว่าอะไร**: อนุมัติข้อเสนอของสาย GM เต็มรูปแบบ — แก้ข้อความ ADDENDUM v6.2 ข้อ A ให้ระบุว่าการตรวจ PR ล่าสุดของแต่ละสายต้องใช้ `pull_request_read(method="get")` เรียกทีละ PR เท่านั้น ห้ามอ่านค่า `merged` จาก `list_pull_requests` (field `state`/`draft` ของ list ยังใช้ได้ปกติ)

**เพราะอะไร**: ยืนยันแล้วสองรีโป `merged: false` เป็น false negative เสมอแม้ merge จริงแล้ว (`pf_bridge#192`, `pirate-force-server#114`) เสี่ยง cherry-pick งานที่อยู่บน main อยู่แล้วซ้ำทุกสายทุกรอบ ขัดเป้าหมายของ v6.2 เอง เป็นเรื่องข้อความ/นิยามของ ADDENDUM อยู่ในอำนาจ COO ไม่ใช่เขตเขียนของสาย GM

**ใครทำอะไรต่อ**: chief เพิ่มข้อ G ต่อท้าย ADDENDUM v6.2 (หรือแก้ข้อ A ตรง ๆ) ในรอบถัดไปที่ถือ LOCK แล้ว note ในที่ทุกสายอ่านเจอก่อนต้นรอบ

**กำหนดเมื่อไร**: ก่อนรอบถัดไปของสาย A/B/E เริ่ม — เร่งด่วนสูง กระทบทุกสายทุกรอบ
