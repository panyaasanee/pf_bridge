# จาก chief (cloud R157) ถึงผู้เทส/Panya — 2026-08-25 ~00:40 (+07:00)

## สรุปรอบเดียวอ่านจบ
เลนหลักทุกเลนติดรอฝั่งคุณ (GT-063/GT-060 พร้อมบูตรวมสามเลน · GT-045/GT-034 นัดตา 26 ส.ค. ·
compose count>0 รอคำเคาะ) ⇒ รอบนี้ดึง milestone สำรองตามกติกา: **เปิดเลน mob-AI สไลซ์แรก
MOB-AGGRO-001** — threat table + tick ตัดสินใจ แบบ pure logic ตามร่างดีไซน์ R98 §5 ที่ค้างไว้

## ของใหม่
1. **PR โค้ด #27** (รอ gate · merge เอง): `mob_aggro.py` + เทส 55/32 + notes ใน coverage
   - deterministic ล้วน · fail-closed 15 refusal ชื่อ · ไม่แตะ runtime/scenario ใด — บูตทุกแบบ
     byte-identical เท่าเดิม · แถว coverage **คง not_started** ตามกติกา R98
   - intent โจมตีชื่อ `INTENT_ATTACK_UNDELIVERABLE` โดยเจตนา — Door B ยังไม่มีทางส่ง
   - ผ่าน pf-adversary 11 findings แก้ครบก่อน commit (รายละเอียดใน `rounds/R157_*.md`)
2. **RE-065** (ใหม่ · `CLIENT_RE_QUEUE.md` ท้ายไฟล์ · **NEEDS-BRIDGE-IMAGE**):
   เดิน ctor `CActorTask_UseBehavior`/`CActorTask_PlayActionEvent` — คำถามชี้ขาด Door B:
   เฟรม behavior-id จากเซิร์ฟเวอร์สร้าง attack task ให้ `CNetNPC` ได้ไหม (ผลลบก็มีค่า —
   สอดคล้อง SCENE-013) · ทำได้เฉพาะหน้าเครื่องที่มีอิมเมจ ไม่ต้องเปิดเกม ไม่จับ LOCK_GAME

## คิวเทสเกม (ตามกฎทุกรอบต้องตอบ)
- **GT ใหม่: ไม่มี** — สไลซ์นี้ไม่มีพฤติกรรมบนจอให้เทส (ไม่มีเฟรมออก wire แม้แต่ใบเดียว)
- ใบเดิมทั้งหมดคงเดิม ไม่ลบ ไม่ย้าย · RE-065 คือรายการใหม่ฝั่ง static

## คำถามค้างถึง Panya (สองข้อ)
1. (ค้างจาก R156) HYP-PF-037 compose count>0 — เปิด NEW VERSION เลย หรือรอผลตา GT-063?
2. (ใหม่) เลน mob-aggro ขั้นต่อไป: อนุญาตให้ wire intent ที่ส่งได้จริง (approach/leash-return →
   เฟรม movement ที่พิสูจน์แล้ว) เป็นเลนโค้ด opt-in รอบถัดไปไหม? ผมถือว่าเกิน pre-approved
   (ต่อ decision loop เข้า runtime) จึงยังไม่เริ่มเอง

## ตอนนี้ต้องทำอะไรต่อ (ขั้นเดียว)
เมื่อเปิดคอม: บูตเทสรวมสามเลน **GT-063** ก่อนใบอื่น (พร้อมแล้วทุกเงื่อนไข) — ผลของมันปลดทั้ง
คำถามข้อ 1 และมิติ count>0 ของ ItemOperate
