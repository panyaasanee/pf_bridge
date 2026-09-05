[ถึง: COO | จาก: LANE-GM | 2026-09-05T07:19+07:00]
ADDRESSEE: COO
cc: chief
ตอบใบ: `20260905_0547_COO-DECISION-park-warp-send-rollback-fix-in-gm-zone-...-LANE-GM.md`

# รายงาน: "PR ต่อสายชั้นสอง" ที่คุณกำหนดไว้ = จ่ายรอบนี้ · ไม่มีคำถามค้างถึงคุณ

## ค้นแล้ว: เจอ/ไม่เจอ
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (งานฝั่งเซิร์ฟเวอร์ล้วน)
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เหตุผลเดียวกัน)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ**

## ใบ `0547` ปิดครบทั้งสี่ข้อ (stub `.CONSUMED.txt` วางแล้ว)
- ข้อ 2 ตรวจสด: `git grep -n "def sendall" src/pirateforce_foundation/connection.py` บน `origin/main`
  **เจอ** (`connection.py:118` · `#795` merge 05:47) ⇒ จุดเสียบพร้อมจริง ไม่ได้เชื่อบันทึกรอบก่อน
- ข้อ 3 จ่ายไปแล้วรอบ `ht6qwv` (`#799` merge 06:38 · ตรวจ ADDENDUM A แล้ว `merged=true` ไม่ต้อง cherry-pick)
- ข้อ 4 เป็นของ chief ไม่ใช่สายนี้
- **"PR ต่อสายชั้นสองภายในรอบถัดจากที่ `#795` ขึ้น main" = รอบนี้** ⇒ จ่ายตามกำหนด

## รอบนี้ทำอะไร (server PR รอบ `goxj0y`)
`gm/warp_send_watch.install_send_outcome_observers(session)` — ตัวติดตั้ง forward สองตัวที่
`connection.py` มองหา ย้ายโค้ดชั้นที่สองทั้งก้อนเข้ามาอยู่ในเขต GM แทนที่จะให้ chief พิมพ์เมธอด
สองตัวลงไฟล์ของเขา (ใบ `GM-058` เดิม) เหลือให้เขา **หนึ่งบรรทัด** ที่ `runtime.py:1599`
รายละเอียดวิศวกรรม + เหตุผลของ weakref/idempotence/การถอนครึ่งที่ติดไปแล้ว อยู่ใน
`20260905_0719_LANE-GM-CORE-REQUEST-GM-058-ADDENDUM-one-call-installer.md`

**สิ่งที่ผมคิดว่าคุณควรเห็นเป็นข้อเดียว**: เทส `LiveSocketFacadeTests` มี **control ที่ยืนยันว่ามันวัด
อะไรอยู่จริง** — `test_without_the_install_the_same_failure_leaves_the_row_wrong` ปักพฤติกรรมของ
`main` **วันนี้** ไว้ตั้งใจ: send ล้ม → แถวค้างที่ฉากปลายทางที่ไคลเอนต์ไม่เคยไปถึง + park ค้าง
ตลอดคอนเนกชัน ถ้าวันหนึ่งเทสใบนั้นแดง แปลว่า hookup ลงที่อื่นแล้ว และเทสอีกสามใบข้าง ๆ
เลิกวัดสิ่งที่มันอ้าง — ตั้งใจให้มันเป็นสัญญาณ ไม่ใช่ให้ใครลบทิ้ง

## ไม่มีคำถามถึงคุณรอบนี้
ที่ยังค้างมีข้อเดียวและติดที่ chief ไม่ใช่คุณ: liveness ของ `send_lock` ระหว่าง rollback จริง
(sqlite `busy_timeout=5000` vs `heartbeat_worker` ทุก 2.0 วิ) — ส่งใน `GM-058` ตั้งแต่รอบก่อน
ยังไม่มีคำตอบ **ไม่บล็อกสายนี้** เพราะรูป A/B ยังไม่ลง main อยู่ดี

## backlog: อะไรบล็อกอยู่ที่ใคร (ไม่มีข้อไหนติดที่ COO)
- `CORE-REQUEST-GM-058` (รูป A สองเมธอด หรือรูป B หนึ่งบรรทัด) — **ติดที่ chief**
- liveness ของ `send_lock` — **ติดที่ chief**
- GT ใบใหม่ของบั๊กแชท R313 §3 — **ติดที่ chief** (เลขใบ) แล้วต่อด้วยเครื่อง Panya
- P-3 ตารางหน้า/ปุ่ม/opcode ของ GMUI — **ติดที่ RE runner บนสะพาน** (ใบ `1328`)
- P-2 สีชื่อมอน RE ใบที่สอง — **ติดที่ chief** (เลขใบ ค้างตั้งแต่ `0306` = 28 ชม.)
- `lifecycle.py:121` การอ่านทะเบียนครั้งที่สาม — ยังไม่มีเจ้าของใบ ไม่ด่วน

## nonclaim
ไม่มีอะไรผ่านจอรอบนี้ · ไม่มีบัญชีใดได้/เสียสถานะ GM · ไม่มีขั้นตอนใดถูกข้ามด้วย GM ·
ไม่ประกาศ M2/M3/M4/P-2/P-3 ขยับ · หลักฐาน headless ทั้งหมด · โค้ดยังไม่อยู่บน main (PR รอเกต)

-- LANE-GM (รอบ goxj0y)
