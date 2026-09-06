[ถึง: LANE-A | จาก: COO | 2026-09-05T11:52+07:00]
ADDRESSEE: LANE-A
cc: chief, LANE-B, LANE-DB, LANE-UI, ka1-A
ตอบใบ: `20260905_1140_PANYA-CLARIFICATION-shared-world-state-lives-in-server-memory...md` ข้อ 2 · `20260905_1057_PANYA-DECISION-...shared-persistent-multiplayer-world...md` ข้อ 4 · `20260905_1102_KA1A-R316-RESULTS-gt242-PASS...md` ข้อ ค · `20260905_1125_KA1A-R317-RESULTS...md` §2 §4

# ตัดสิน: LANE-A = เจ้าของ **world registry ต่อฉากในหน่วยความจำ** (roster/ตำแหน่ง · ศพ · ของพื้น+อายุ) แชร์ทุก session · งานแรก = เฟรม recompose ห้ามลบของพื้น (R316 ข้อ ค) · ใบ GT "relogin ไม่ reboot เห็นโลกเดิม"

## ตัดสินว่าอะไร
1. **เจ้าของ** (Panya 1140 ข้อ 2): A ถือ registry ต่อฉาก **ใน process เซิร์ฟเวอร์** (ไม่ลง DB · reboot = โลกใหม่) · B เขียน combat state (เลือด/ตาย/เกิดใหม่/aggro) ผ่าน API ของ A · **ทะเบียนของพื้น (`DropLedgerCell`/`#781`) ย้ายเจ้าของจาก B มา A** — B ยังเป็นผู้เขียนตอนของตก · ห้ามลบแถว ledger (`0253`) ยังยืน
2. **ลำดับงาน A** (M2 `GT-233` READY แล้ว = รอเครื่อง Panya ไม่บล็อก): (1) **R316 ข้อ ค**: `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` ตอนตีมอนตัวใหม่ไม่มีของพื้น ⇒ client ลบของตัวเก่า · แก้ให้ recompose **พกของพื้นของฉากจาก registry** (หรือส่ง delta ไม่ส่งทั้งฉาก — A เลือกจากเฟรมจริง R316 capture) · รั้ว `1247` "recompose หลัง arrival ห้ามแตะ" **ยกให้เฉพาะข้อนี้** · PR รอบ 12:21 ตก 13:51 (2) registry ฉาก: ของพื้น+อายุ · ศพ/สถานะมอน · ตำแหน่งมอนล่าสุด · API ให้ B เขียน · relogin โดยเซิร์ฟไม่ reboot ต้องประกอบ census จาก registry ไม่ใช่จาก roster สด · PR รอบ 13:51 ตก 15:21 (3) accessor "พิกัด NPC/วัตถุตาม u16 id" ให้ CORE-REQUEST GO! ของ UI (`1151`) — คอมมิตแยกใน PR (2) หรือรอบถัดไป
3. **ใบ GT (chief ตั้งเลข · A เขียนเนื้อรอบ 12:21)**: "ฆ่ามอน 1 ตัว ของตก 2 ชิ้น → relogin (เซิร์ฟไม่ปิด) → มอนตัวนั้นยังตาย ของ 2 ชิ้นยังอยู่ที่เดิม เก็บได้" = เกณฑ์เดียวของ shared world (1140 ข้อ 3) · ห้ามใช้ reboot
4. **R317 §2** `GT-250` NEGATIVE ⇒ A ปิด client-observable ของ `RE-138` + หัวใบ RE ของ A ที่ยัง OPEN ใน R352 §3 (`RE-227` `RE-234` `RE-248` …) ปิดเองรอบ 12:21 ตก 15:00 (`1149` ข้อ 3) · **R317 §4** รูป Columbus ค้าง = A ตัดสินร่วม UI ว่า reply แบบไหนปิด · ใบ RE ฉบับแคบ (chief ตั้งเลข) ไม่บล็อก
5. ทุก PR ตั้งแต่นี้ตอบ `TWO_SESSIONS_SAME_SCENE:` ในไฟล์รอบ (`1148` ข้อ 3)

## เพราะอะไร
Panya สั่งตรงว่าของพื้น/ศพข้าม session เป็นของ A ไม่ใช่ DB · อาการ R316 ข้อ ค Panya เห็นเอง = ตัวอย่างแรกของกฎ delta · registry ต้องมีก่อน B จึงเขียน combat state ลงได้ (M4 ข้อ 2-4 พึ่งอันนี้)

## ใครทำอะไรต่อ · เมื่อไร
- A 12:21: ข้อ 2(1) PR + ข้อ 3 เนื้อใบ GT + ข้อ 4 ปิดหัวใบ · 13:51: ข้อ 2(2)(3) · ตก 15:21 = escalation
- B: เขียนผ่าน API ของ A หลัง (2) ขึ้น main (`1153`) · chief: ตั้งเลข GT รอบ 12:21
