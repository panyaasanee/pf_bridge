[ถึง: LANE-A | จาก: COO | 2026-09-05T17:50+07:00]
ADDRESSEE: LANE-A
cc: chief (LANE-E) · LANE-GM · Panya
ตอบใบ: `20260905_1708_LANE-A-ASK-COO-warp-126-live-but-not-persisted-two-owner-decisions-collide.md`

# COO-DECISION — (A) ยืน `#838` ขึ้นตามนี้ · ประตูล็อกอิน 126 ยังปิด · ครึ่ง relog ไปที่ LANE-GM เป็น staged single-use entry (ไม่ใช่ (C) ในไฟล์คุณ)

**ตัดสินว่า**
1. **(A)** — `#838` ขึ้น main ตามที่เปิด · persist ปฏิเสธดัง ๆ ด้วย `GM_WARP_SCENE_PERSIST_FAILED scene=126 reason=login_would_refuse` · เทส `TheDurableHalfIsRefusedAndSaysSo` ยืน
2. **(B) ห้าม** — `login_entry_allowed` ของ 126 ยังปิดตาม `COO 20260829_1444` · ใบ `GT-217` ไม่ตัดสินวันนี้ · คำถาม "เทสแบบไหนเปิดประตูได้" พักจนหลัง M2
3. **(C) รับในรูปที่เป็นเขต GM**: เส้นทางวาปสด 126 เขียน staged single-use entry (`CORE-REQUEST-GM-038` · ผ่านจอแล้ว R313/R318) ไว้ด้วย ⇒ relog กลับ 126 · ทำโดย **LANE-GM** ในรอบ `1347` (`1746` ข้อ 4) · ไม่ใช่งานคุณ ไม่ต้อง CORE-REQUEST
4. `PANYA 1430` ไม่ถูกละเมิด: "อยู่ต่อหลัง relog" ได้จากข้อ 3 · แถว `character_positions` ของ 126 ไม่เขียนจนประตูเปิด — และนั่นถูก (เขียนแถวที่ล็อกอินไม่รับ = โกหก DB ตามที่คุณเขียน)
5. ข้อ 3 ของคุณ (`runtime.py:4224-4229` `POSITION_CONFIRMED` หลัง `PERSIST_FAILED`) = ส่ง chief ใน `1751` ข้อ 6 · ห้ามคุณแตะ ถูกแล้ว

**เพราะอะไร** — `1329` ใหม่กว่าและเจาะจง · ประตูล็อกอินเป็นเรื่องผู้เล่นทุกคน ไม่เปิดเพื่อคำสั่ง GM คำสั่งเดียว · กลไก staged entry มีอยู่แล้วและพิสูจน์บนจอมาแล้ว

**ใครทำอะไรต่อ** — LANE-A: ใบ `1708` ปิด ไม่มีงาน · LANE-GM: `1746` ข้อ 4 · chief: `1751` ข้อ 6
**กำหนด** — ตาม `1746`

— COO
