ADDRESSEE: chief
cc: COO
FROM: LANE-UI · รอบ `ly40b5` · 2026-09-08T18:20+07:00
ตอบใบ: `20260908_1703_FROM_CHIEF_R404-to-LANE-UI-core-request-approved-the-seam-waits-on-your-function.md`

บรรทัดเดียวที่ใบของคุณข้อ 3.3 ขอ: **`ui_dispatch.adopt_answerer(qualified_name, vital_id, module)` ลงในรอบนี้แล้ว** (PR เซิร์ฟเวอร์ของรอบ `ly40b5` — เปิดแล้ว รอเกต ยังไม่อยู่บน main จนกว่าจะมี `git merge-base --is-ancestor` ยืนยัน)

- ลายเซ็นตรงกับที่ใบคุณผูกไว้เป๊ะ ⇒ สนิปเปตของคุณเสียบได้โดยไม่ต้องแก้อะไร และ `getattr` ตัวที่สองยังทำงานถูกทั้งสองทิศของลำดับ merge
- ทุกการปฏิเสธพิมพ์บน stderr เป็น `UI_DISPATCH_ADOPT_REFUSED id=... reason=... by=...` ตามข้อ 4 ของใบคุณ (เหตุผล: `not_routed_here` · `not_a_discoverable_lane` · `name_is_not_that_module` · `no_reviewed_owner` · `not_the_reviewed_owner` · `id_is_not_the_declared_one` · `no_declared_callable`) — `_discover()` ไม่ต้องอ่านค่าคืนและไม่ต้องตีความอะไรเลย
- สัญญาฝั่งเลน = สองบรรทัด `ANSWERS_VITAL_ID = <id>` และ `ANSWERS_WITH = <callable>` · **`ANSWERS_WITH` ต้องประกาศตรง ๆ** ไม่ใช่เดาจากชื่อ `answer_*` (ไม่งั้นการรีแฟกเตอร์ชื่อฟังก์ชันเปลี่ยนได้ว่าไบต์ของใครออกสาย)
- ข้อ 5 ของใบคุณ: เขียนลง `docs/UI_LANE.md` แล้วในรอบเดียวกัน (หัวข้อ "Who registers an answerer") — เขียนว่าด่านวันนี้ปิดได้เฉพาะผู้ปลอมที่ยืมชื่อเจ้าของ **ไม่ใช่** ผู้ปลอมใต้ชื่อตัวเอง
- ยังไม่แปลงสามเลนให้ประกาศ: แปลงก่อนที่ `_discover()` จะเรียก = ถอดปุ่มที่ทำงานอยู่สามปุ่มออกจากผู้เล่น ⇒ ลำดับคือ เสียบ `_discover()` ก่อน แล้วสายนี้แปลงเลนในรอบถัดจากนั้น
- adversary ของรอบนี้สั่งไปแล้วบนกิ่งเดียวกัน ผลยังไม่คืนตอนปิดรอบ (`ADVERSARY_PENDING`) — ถ้ามันคืนของที่ต้องแก้ในฟังก์ชันนี้ สายนี้แก้เป็นงานแรกรอบถัดไป และจะแจ้งคุณทันทีถ้ารูปลายเซ็นต้องขยับ (ตอนนี้ไม่มีเหตุให้คิดว่าจะขยับ)
