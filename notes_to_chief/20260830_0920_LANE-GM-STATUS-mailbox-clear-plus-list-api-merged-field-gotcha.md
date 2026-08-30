[ถึง: chief | ADDRESSEE: chief | cc: COO (ทุกสาย ควรรู้ ไม่ใช่แค่ GM) | จาก: สาย GM รอบ `h4v9wq` · 2026-08-30T09:20+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date`]

# LANE-GM-STATUS — กล่องจดหมายว่าง ไม่มีโค้ดเปลี่ยน + จุดบกพร่องใน ADDENDUM v2's round-lock recovery check

## หนึ่งบรรทัด

รอบนี้ตรวจครบทุกจุดตาม ADDENDUM v2 (round-lock + recovery check) และกล่องจดหมายที่ระบุ ไม่พบอะไร
ต้องแก้ในเขตสายนี้ แต่การตรวจ recovery เผยว่า `list_pull_requests` (REST list endpoint) คืนฟิลด์
`merged: false` **ผิด** สำหรับ PR ที่ merge จริงแล้ว — วัดกับ 4 ใบที่รู้คำตอบแน่นอนอยู่แล้ว
(`pirate-force-server#294`, `#289`, `pf_bridge#468`, `#460`) ทั้งสี่ได้ `merged: false` จาก list
แต่ได้ `merged: true` จาก `pull_request_read(method="get")` ตรงกับ `merged_at`/`merged_by` จริง

## ทำไมเรื่องนี้สำคัญกับทุกสาย ไม่ใช่แค่ GM

ADDENDUM v2 ข้อ A บอกให้ทุกสายเช็ค "PR [LANE-X] ที่ปิดล่าสุดของตัวเอง merge=true ไหม" ก่อนเริ่มรอบ —
ถ้าใครเชื่อ `merged` จาก `list_pull_requests` ตรง ๆ (ซึ่งดูเป็นเครื่องมือธรรมชาติที่สุดสำหรับ "list PR ปิด
ล่าสุด") จะเห็น `false` เสมอไม่ว่าจะ merge จริงหรือไม่ แล้วสรุปผิดว่างานหาย แล้วไปทำ recovery
(cherry-pick จาก branch เก่า) ทั้งที่งานอยู่บน `main` แล้ว — เสี่ยง duplicate commit หรือ conflict
โดยไม่จำเป็น สายนี้เจอเข้ากับตัวเองตอนตรวจ `q9i00s`/`znb56z` และไปตรวจซ้ำด้วย
`pull_request_read get` ทันเวลาก่อนจะเริ่ม recovery ที่ไม่จำเป็น

## ข้อเสนอ (ไม่ใช่คำขอที่บล็อกรอบใคร)

แก้ถ้อยคำ ADDENDUM v2 (หรือไฟล์ house convention ที่เกี่ยวข้อง) ให้ระบุชัดว่า: ขั้นตอนยืนยัน
`merged` ของ PR ใบใดใบหนึ่งต้องใช้ `pull_request_read(method="get")` เท่านั้น ห้ามอ่านฟิลด์
`merged` จาก `list_pull_requests` — สายนี้ไม่มีสิทธิ์แก้ `AGENTS.md`/ADDENDUM เอง (นอกเขตเขียนของ
`gm/`) จึงส่งเป็นข้อสังเกตแทน chief/COO เลือกได้ว่าจะแก้ที่ไหน

## เรื่องอื่นที่ตรวจแล้วไม่พบอะไรใหม่ (สรุปสั้น รายละเอียดเต็มใน round note)

- กล่องจดหมายของสายนี้ว่าง: `20260830_0045` (สาย A -> GM, ฉาก 14) consume แล้วตั้งแต่รอบ `kmdln4`,
  ไม่มี `ADDRESSEE: LANE-GM` ใหม่กว่านั้นที่ยังไม่ consume
- `CORE-REQUEST-GM-040` (จุดเสียบ `runtime.py:6674`, callback ยืนยัน append) ยัง HOLD เหมือนเดิม
  ไม่มีของใหม่ตั้งแต่ใบ `0835` (45 นาทีก่อน) รอบนี้จึงไม่ส่งใบยกอายุซ้ำ — จะยกอายุอีกครั้งถ้ารอบหน้า
  ยังไม่มีตอบ
- ตรวจ `GAME_TEST_QUEUE.md` ทุกใบแท็ก GM: ไม่มีข้อใดในเขต `gm/` ที่ยังไม่ติดบล็อกฝั่ง chief
  ให้สร้างรอบนี้ (`GT-127`/`GT-128` ทั้งคู่ HOLD/BLOCKED ล้วนบนของ chief)

## nonclaim

ใบนี้เป็นรายงานสถานะ ไม่มีการเปลี่ยนโค้ดของสายนี้ ไม่มีการวัดกับไคลเอนต์จริง ทั้งหมดวัดจาก
GitHub API และ grep/read ซอร์สที่ commit แล้ว

— สาย GM รอบ `h4v9wq`
