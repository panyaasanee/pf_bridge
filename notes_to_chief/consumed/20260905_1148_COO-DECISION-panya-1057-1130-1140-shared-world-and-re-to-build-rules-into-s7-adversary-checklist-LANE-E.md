[ถึง: chief (LANE-E) | จาก: COO | 2026-09-05T11:48+07:00]
ADDRESSEE: LANE-E
cc: LANE-A, LANE-B, LANE-DB, LANE-GM, LANE-CS, LANE-UI, ka1-A
ตอบใบ: `20260905_1057_PANYA-DECISION-all-game-logic-...shared-persistent-multiplayer-world...md` · `20260905_1130_PANYA-DECISION-an-answered-re-with-a-feature-waiting-must-open-a-build-ticket...md` · `20260905_1140_PANYA-CLARIFICATION-shared-world-state-lives-in-server-memory-not-db...md`

# ตัดสิน: รับคำสั่ง Panya สามใบเป็นกติกาบ้านทันที · chief ลง `AGENTS.md` §7 สองข้อ + checklist adversary หนึ่งข้อ รอบ 12:21 ตก 13:51

## ตัดสินว่าอะไร
1. **กติกา "shared world" (Panya 1057 + 1140 แทนถ้อยคำ 1057 ข้อ 1)**: สถานะโลกต่อฉาก (roster/ตำแหน่งมอน · เลือดมอน · ศพ/เกิดใหม่ · ของพื้น+อายุ) อยู่ใน **หน่วยความจำ process เซิร์ฟเวอร์ แชร์ทุก session ในฉากเดียวกัน · reboot = โลกใหม่** · ลง DB เฉพาะของตัวละคร/บัญชี (ตำแหน่ง/ฉาก · กระเป๋า · สกิล · เควส · class) · เจ้าของ: **LANE-A = world registry · LANE-B = combat state เขียนลง registry ของ A · LANE-DB ไม่รับงานโลก** · "ทะเบียนต่อ session" และ "relogin แล้วรีเซ็ต" = ข้อบกพร่อง
2. **กติกา delta (1057 ข้อ 2)**: เฟรมที่เกิดจากการกระทำของผู้เล่นคนเดียว ห้ามทำให้ client ลบ/วาดโลกใหม่ทั้งฉาก ส่งเฉพาะส่วนต่าง
3. **checklist adversary + เกต (1057 ข้อ 3)**: ทุก PR/ใบงานใหม่ต้องตอบบรรทัด `TWO_SESSIONS_SAME_SCENE: <ถูก/ไม่เกี่ยว เพราะ …>` ในไฟล์รอบ · chief ตัดสินรูปแบบ (ลง `pf-adversary` + `PROCESS_GATES.md`)
4. **§7 ขยาย (1130 ข้อ 1)**: RE ที่ "ตอบแล้ว" และปลดล็อกฟีเจอร์ผู้เล่น ⇒ ผู้บริโภคผลเปิด **ใบสร้าง (CORE-REQUEST หรือ PR ของสายตัวเอง) + ใบ GT ยืนยันบนจอ ในรอบเดียวกัน** · ไม่มีฟีเจอร์รอ = เขียนบรรทัด `NO_FEATURE_WAITING: <เหตุผล>` · chief ตรวจใน `QUEUE_TRIAGE:` ทุก 6 ชม. ว่าทุก RE ที่ปิดในช่วงนั้นมีใบสร้างคู่หรือบรรทัดนี้
5. เกณฑ์ผ่านเดียวของ shared world (1140 ข้อ 3): **session ที่สอง หรือ relogin โดยเซิร์ฟไม่ reboot เห็นเลือดมอน/ตำแหน่งมอน/ศพ/ของพื้นเหมือน session แรก** · ใบ GT ใช้ relogin ได้ (เครื่อง Panya มี client เดียว)

## เพราะอะไร
Panya สั่งตรง ("บังคับเลย") · ไม่ขัดบันได M · เป็นข้อบังคับคุณภาพครอบทุกขั้น · ka1-A ขอให้ COO/chief แปลงเป็นข้อบังคับ ข้อ 1-5 ข้างบนคือถ้อยคำบังคับ ถ้อยคำใน §7 = chief

## ใครทำอะไรต่อ · เมื่อไร
- chief รอบ 12:21: ลง §7 ข้อ 1/2/4 + checklist ข้อ 3 (ใบเดี่ยว ไม่รวมกับ D13) · ตก 13:51 = escalation
- การมอบหมายรายสาย = ใบแยก `1152` (A) · `1153` (B) · `1154` (DB) · `1151` (UI GO!) วันนี้
- ประเมินกำลังทีม (1130 ข้อ 3 บนการมอบหมาย 1140 ข้อ 2) = COO รอบผู้บริหาร 21:41 วันนี้ ตอบ Panya ผ่าน ka1-A พร้อมตัวเลข
