# จาก chief (cloud R123) ถึงผู้เทส LOCAL + ผู้ช่วย + คุณ Panya — 2026-08-23 16:15 (+07:00)

รอบใหญ่ #13 ของพวกคุณ (22–23 ส.ค.) ถูกบริโภคครบทั้ง 14 ใบแล้ว (ใบคำตัดสิน 21 ส.ค. 11:04 บริโภคไปแล้วตั้งแต่ R122) งานคืนนั้นคุณภาพสูงมาก — ขอบคุณครับ
คิว/ledger ถูก flip ตามผลแล้วทั้งหมด (รายละเอียดใน `rounds/R123_3fyvv8_biground13_consume_and_ledger_amendments.md`)

## สรุปที่ flip แล้ว

- ✅ PASS: **GT-038** (selection ไม่ใช่เงื่อนไขของเลข — ตรงคำทำนาย static R102) · **GT-041** (no-rejection · relog = last-wire) · **GT-043** (survival · subsecond-unobserved) · **GT-042** (re-derive + erratum handler len 47) · **GT-044** (BG0001 = scene id 1) · **GT-001** (smoke `cf81730` · รับทราบ CANON_SHA ใหม่ `23FD885A…`)
- 🟡 GT-034 = **NO-RESULT กรณี 3** (ไม่เห็นตัว) — GT-035/036 คง BLOCKED · 🟡 GT-033C = ผลลบมีค่า · 🟠 GT-030 = **CLIENT NO-RENDER** ห้ามรอบสาม
- ledger ฝั่ง code repo: amendment evidence_gap 4 เลน (HYP-PF-024/027/030/031) — PR ผ่าน gate ตามปกติ

## ใบใหม่ในคิว (ท้ายไฟล์ GAME_TEST_QUEUE.md)

1. **GT-045 GROUNDDROP-RENDER-001** [attended] — 🔴 BLOCKED: ต้องรอ chief เขียนเลนเซิร์ฟเวอร์ (bit `0x08` element) + gate เขียว + merge ก่อน **ห้ามบูต**
2. **GT-046 PICKUP-DIRECTION-001** [STATIC-ON-BRIDGE] — ทำได้ทันที · หาทิศทาง `PickupTerrainThing` (WRITE `0x89A600` vs READ `0x89A640`)
3. **GT-047 RUNTIMEPROTO-CAPTURE-VALIDATE-001** [STATIC-ON-BRIDGE] — ทำได้ทันที **ต้องรันบน Windows** · parse 50,820 เฟรม `GSCN_RunTimeProtocol*` ปิด F2 + การ์ด mutation `field_offset` (ข้อบังคับจากใบตรวจปฏิปักษ์ 07:30)

## คำตอบที่ปิดในรอบนี้

- **คำถาม GT-038 ข้อ 3** (`damage_model_hypothesis_npc_sweep_sent` ไม่โผล่ใน capture log): **ไม่ใช่บั๊ก** — `self.events` เป็น list ในหน่วยความจำโดยดีไซน์ (`runtime.py:1819` พินโดยเทส/replay) ไม่เคยถูก print ⇒ เกณฑ์ attended อ้าง wire label 4 ใบจาก server console เป็นหลักฐานที่ถูกต้องแล้ว ไม่ต้องแก้โค้ด

## ฝากเจ้าของ tooling ฝั่งสะพาน (chief แตะไม่ได้ — template ไม่อยู่ใน VCS)

1. `TEMPLATE_teardown_generic.ps1`: local `$jobTag=''` ชน parameter `$JobTag` แบบ case-insensitive ⇒ receipt ถูกตั้งชื่อ `TEMPLATE_teardown_generic.*` แทน tag จริง (เจอใน GT-034 job 984) — เปลี่ยนชื่อตัวแปร local
2. capture collector ใน template: เมื่อไม่ส่ง `CaptureFilter` มันเลือก `capture_v142` แทน `captureroot` จาก info file ล่าสุด (เจอใน GT-033C job 987) — ให้ default ใช้ `captureroot` จาก newest info file หรือ fail เมื่อ path กับ filter ไม่ตรง

## ฝากผู้ช่วย (เอกสารบนเครื่อง Panya — ไม่อยู่ใน VCS)

- erratum ที่คุณเสนอเอง: ต่อท้าย `decoded external videos\tp6C_6uZwUM\reports\01_ground_loot.md` ว่าบรรทัด "สนับสนุนว่าสัตว์เลี้ยงเก็บค้อนให้อัตโนมัติ" ต้องลดน้ำหนัก (เพ็ตมาถึงช้ากว่าของหาย 0.42s — การเก็บไม่ใช่การสัมผัส) **ต่อท้ายเท่านั้น ห้ามลบของเดิม** — เห็นด้วยและอนุมัติตามที่ร่างไว้

## ถึงคุณ Panya — คำถามค้างหนึ่งข้อ (ไม่บล็อกงานอื่น)

**GT-034 ไม่เห็นตัวนกเลย** ที่พิกัดคาด (placement ทำงานเป๊ะ แต่ scene-load เปล่า ๆ ไม่มีตัวอะไรโผล่) ⇒ ตอนนี้แยกไม่ได้ระหว่าง (ก) client ไม่ spawn มอนจากข้อมูล ship เองเลย — ต้องมีเฟรมจาก server (= Door A ต้อง splice เสมอ) กับ (ข) ตัวอยู่จริงแต่เงื่อนไข render/ระยะ/มุมอื่น
ทางเลือกที่เสนอ (เรียงถูก→แพง): ① ใบ static หา "เงื่อนไข spawn NPC ฝั่ง client data" ในอิมเมจ (STATIC-ON-BRIDGE — chief ร่างได้เลยถ้าคุณเคาะ) ② เลนวางจุดสังเกตหลายจุดรอบพิกัดเป้า (ต้องเขียนเลนใหม่+gate) ③ พักเรื่อง native-red แล้วยอมรับ Door A แบบ splice ไปก่อน
**ขอคำเคาะทางใดทางหนึ่ง** — ระหว่างรอ chief จะไม่เดินเลนนี้ต่อเอง (คำสั่งเดิม: ห้าม redirect Door A โดยพลการ)

## ลำดับที่แนะนำสำหรับรอบเทสถัดไป

1. GT-047 (Windows · ปิด F2 — คุ้มสุดตามใบตรวจปฏิปักษ์) → 2. GT-046 (static ทิศทาง pickup) → 3. รอคำเคาะ GT-034 จากคุณ Panya

— chief (R123 · เซสชัน 3fyvv8)
