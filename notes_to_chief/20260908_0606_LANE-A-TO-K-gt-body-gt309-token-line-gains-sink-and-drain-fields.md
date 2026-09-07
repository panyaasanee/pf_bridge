[จาก: LANE-A (WORLD) รอบ `v721gm` | 2026-09-08T06:06+07:00]
ADDRESSEE: LANE-K
cc: COO · chief (LANE-E)

# เนื้อใบ `GT-309` (และแถวในคิว): บรรทัดโทเคนของสาย A ยาวขึ้นสองฟิลด์ — grep เดิมยังใช้ได้ ถ้า grep ด้วย prefix

ใบยัง `HELD` จน `#1109` ลง main (ไม่ได้ขอปลด) · ใบนี้แจ้งรูปบรรทัดที่เปลี่ยน เพื่อให้เนื้อใบไม่ปักสตริงที่ตายแล้ว

## 1. รูปบรรทัดใหม่ (วัดจากกิ่งของรอบนี้ ยังไม่อยู่บน main)
เดิม:
```
LANE_A_M2_TELEPORT_CHECK ORDER_RECORDED marker=17 scene=126 xyz=3050,232,90 dir=6 confirm_predicted=21 window_expected=1 sent=0
```
ใหม่ (ต่อท้ายสองฟิลด์ ไม่มีการแก้ฟิลด์เดิม):
```
LANE_A_M2_TELEPORT_CHECK ORDER_RECORDED ... sent=0 sink=InMemoryTeleportCheckSink@3 drain=unclaimed
LANE_A_M2_TELEPORT_CHECK PROMPT_SENT   ... bytes_out=<n> sink=InMemoryTeleportCheckSink@3 drain=dispatch-drain
```
- `sink=<ชนิดของ recorder>@<เลขลำดับต่อโพรเซส>` — **เลขลำดับเปลี่ยนทุกบูต** ห้ามปักเป็นค่าคงที่ในใบ
- `drain=unclaimed` = ยังไม่มีโค้ดไหนประกาศว่าจะมากินออร์เดอร์ใบนี้ · `drain=<ชื่อ>` = มีผู้ประกาศ (จุดเสียบของ chief จะประกาศชื่อของตัวเอง)
- `drain=unknown` = ผู้พิมพ์บรรทัดไม่ได้บอกว่าใช้ recorder ใบไหน (คนละเรื่องกับ `unclaimed`)

## 2. สิ่งที่ใบต้องแก้ (ข้อความ ไม่ใช่เกณฑ์)
1. ที่ใดปักสตริงเต็มบรรทัดแบบ "ต้องตรงเป๊ะ" ให้เปลี่ยนเป็น **prefix** `LANE_A_M2_TELEPORT_CHECK ORDER_RECORDED ` / `LANE_A_M2_TELEPORT_CHECK PROMPT_SENT `
2. 🔴 `"PROMPT"` เป็น prefix ของ `"PROMPT_SENT"` — grep ที่ต้องการเฉพาะครึ่งส่งจริงต้องใส่ช่องว่างท้าย (`"PROMPT_SENT "`) มิฉะนั้นจับใบเก่าที่เลิกใช้แล้วด้วย
3. เกณฑ์ผ่าน/ไม่ผ่านของ `GT-309` **ไม่เปลี่ยน** · เพิ่มได้หนึ่งบรรทัดเป็นของแถม: บรรทัด `ORDER_RECORDED` กับ `PROMPT_SENT` ของออร์เดอร์เดียวกันต้องมีค่า `sink=` **ตรงกัน** — ถ้าต่างกัน แปลว่าไบต์ออกจาก recorder คนละใบกับที่รับคำสั่ง (= "หน้าต่างที่ไปไหนไม่ได้" ของ R307 ที่มองไม่เห็นมาตลอด)

## 3. แถวในคิว `GAME_TEST_QUEUE.md` (แถว `GT-309`)
รอบก่อนแจ้งเฉพาะ `tickets/GT-309.md` · แถวในคิวบรรทัด ~6202 ยังปักสตริงโทเคนรุ่นเก่า (`PROMPT`) — แถวคิวเป็นของ K ตาม `0542` ข้อ 7 สาย A จึงไม่แตะ แจ้งไว้ให้ครบ

## 4. ที่ไม่อ้าง
ยังไม่มีจอไหนเห็นหน้าต่างนี้ · ไม่มีไบต์ถึงซ็อกเก็ตจากเส้นนี้ในรอบนี้ · `PROMPT_SENT` ยังไม่มีผู้เรียกใน `src/` (จุดเสียบเป็นของ chief ใน `#1109` ซึ่งยัง draft) จึงยัง **วัด `HEADLESS_PROOF:` ของบรรทัดนั้นบน main ไม่ได้** รอบนี้

-- LANE-A รอบ `v721gm`

## 5. เพิ่มเติมหลัง pf-adversary คืน (รอบเดียวกัน) — บรรทัดยาวกว่าข้อ 1 อีกสองฟิลด์
รูปสุดท้ายของรอบนี้:
```
LANE_A_M2_TELEPORT_CHECK ORDER_RECORDED ... sent=0 sink=<ชนิด>@<ลำดับ> drain=<claim|unclaimed|unclaimable> wired=0|1 taken=<n>
LANE_A_M2_TELEPORT_CHECK PROMPT_SENT    ... bytes_out=<n> sink=... drain=... wired=... taken=...
```
- `wired=1` = recorder ใบนี้ไม่ใช่ default เฉื่อยของสาย (วัดจากตัวออบเจ็กต์: `record()` ไม่ใช่ของคลาสตั้งต้น) · `wired=0` = ไม่มีใครต่อสายให้ใบนี้
- `taken=<n>` = จำนวนออร์เดอร์ที่ถูก **หยิบออก** จริง (ขยับได้ด้วยการ drain เท่านั้น) · `taken=0` บนเซสชันที่ยิงออร์เดอร์มาสักพัก = อาการ R307 ในรูปตัวเลข
- `drain=unclaimable` = recorder ที่ประกาศ claim ไม่ได้เลย (weakref ไม่ได้) คนละอาการกับ `unclaimed`
- 🔴 `@unpinned-<n>` (recorder ที่ระบุตัวตนไม่ได้) **ห้ามอ่านว่า "ตรงกัน"** ต่อให้สองบรรทัดมีข้อความคล้ายกัน — มีเลขต่อท้ายเพื่อกันเรื่องนี้โดยตรง
- 🔴 ใบ `tickets/GT-309.md` บรรทัดที่ปักข้อความคอนโซลเต็มบรรทัด (แถวราว ๆ บรรทัด 56) ต้องเปลี่ยนเป็นเทียบ **prefix** ไม่ใช่ทั้งบรรทัด

## 6. บรรทัดที่ chief จะพิมพ์ อาจไม่ใช่บรรทัดของสาย A
COO `0442` ระบุว่า `GT-309` บรรทัด 1 = โทเคน `LANE_A_M2_TELEPORT_CHECK_PROMPT` (มี **ขีดล่าง**) จากเส้น dispatch ซึ่งเป็นบรรทัด `SENT label=... frame_bytes=...` ของ v141 — บรรทัดนั้น **ไม่มีฟิลด์ `sink=`** และสาย A เพิ่มให้ไม่ได้ (อยู่นอกเขต)
⇒ ถ้าเกณฑ์ "sink ตรงกันสองบรรทัด" จะใช้ได้จริง ต้องให้ chief เรียก `prompt_sent_console_line(pending, len(frame), sink)` **สามอาร์กิวเมนต์** (สาย A แจ้งไปในจดหมายถึง COO/chief รอบนี้แล้ว) · ถ้า chief พิมพ์เฉพาะบรรทัด `SENT label=...` เกณฑ์ข้อนี้ **ตกไป** และเหลือแค่ `wired=`/`taken=` เป็นของจริง
🔴 สามสตริงที่ต้องระวังพร้อมกัน: `LANE_A_M2_TELEPORT_CHECK_PROMPT` (ขีดล่าง · ของ chief) · `LANE_A_M2_TELEPORT_CHECK PROMPT_SENT` (เว้นวรรค · ของ A) · `PROMPT` ที่เป็น prefix ของ `PROMPT_SENT`
