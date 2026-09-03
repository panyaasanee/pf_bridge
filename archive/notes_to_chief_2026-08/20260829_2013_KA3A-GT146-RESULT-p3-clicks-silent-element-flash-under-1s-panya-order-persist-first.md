จาก: กะ3-A (attended session) · ถึง: chief (cc สาย B)
วันที่: 2026-08-29T20:13+07:00 (TZ=Asia/Bangkok date)
เรื่อง: ผล GT-146 PICKUP-CLICK-OPCODE-CAPTURE-001 — P3 (คลิกทั้งหมดเงียบ) · ใบยังเปิด · พร้อม PANYA-ORDER ใหม่: ทำให้ element ค้างก่อน ค่อยเปิดรอบ capture ใหม่

## ข้อมูลรอบ
- attended · **Panya ขับ UI เองทั้งหมด** · jobs 1347/1348/1349/1350 · 19:53–20:12 (+07:00) ใต้เพดาน 60 นาที
- BOOT_COMMIT `fb9bca6208c9632d23e3e4713b309590be6ab9de` (เขียว ci-status ตรง · code-delta vs origin/main = 0) · แฟล็กคู่ ground-loot + pickup-listener ยืนยันบน cmdline จริง · LISTENER_LANE=PRESENT
- canonical `4FF37060…8454` **เท่าเดิมก่อน-หลัง** · teardown 1349 PASS (listeners/clients/ffmpeg = 0 · integrity ok · FK 0)
- วิดีโอ `evidence_video\1348_gt146_FULLROUND_20260829_195346.mkv` + FRAME proofs 3 รูป · capture `GameClient\capture_gt146_20260829_195343\` · 🔴 ห้ามลบ

## ชั้น wire
- precondition (ก) **PASS**: `GROUND_LOOT_BIT08_RENDER_NEAR_ONCE` + `FAR_ONCE` ออกครบ (54 B/เฟรม · hexdump เต็มอยู่ใน console log — การ decode พิกัด/element key เป็นงานผู้บริโภคผลตาม nonclaim 5)
- สำมะโนขาเข้า**ทั้งบูต** (GAME_LIVE.txt · RECV 394 เฟรม): login family + `TargetPosVital` ×7 (W-tap trigger + เดิน) + แชท `0xAC52` ×1 + `UserSetting_UpdateServerSettingVital` ×2 + keepalive `GSCN_RunTimeProtocolReq` ~390
- 🔴 **ไม่มีเฟรม pickup / เฟรมไม่รู้จัก แม้แต่เฟรมเดียว** — ไม่มี `0x4543` ไม่มี id ใหม่ ในทุกหน้าต่างเวลารอบคลิกทุกครั้ง

## ชั้น client-observable (ตาเจ้าของ สดตลอดรอบ)
- หลัง W-tap: **ฝุ่น + ป้ายชื่อไอเท็มโผล่จริงแล้วหายในเสี้ยววินาที** — เจ้าของอ่านตัวหนังสือไม่ทัน (ข้อความบนป้าย = AWAITING video review ที่เฟรมช่วง ~19:57–58)
- คลิกชุด A: จุดที่ตาเห็นภาพแว็บ (หลายคลิก + ควานหา) · คลิกชุด B: แนวพิกัดคำนวณ trigger+30X (X≈-8,52x · Y≈-2,579 · 3 คลิกเว้น ~5 วิ + hover กวาด) — **cursor ไม่เคยเปลี่ยนรูป · จอไม่มีปฏิกิริยาใดๆ ทั้งสองชุด**
- `OBSERVER_CONFIRMED: 2026-08-29T20:1x+07:00 โดย Panya` (เห็นสดเองทั้งรอบ · คำยืนยันอยู่ในแชทเซสชัน)

## คำตัดสิน: **P3 — คลิกครบแล้วเงียบ = ผลลบที่วัดแล้ว · ใบยังเปิดตามกติกาผลลบ**
ข้อจำกัดการอ่าน P3 รอบนี้ (สำคัญ): อายุการแสดงผลของ element สั้นกว่า 1 วินาที ⇒ **แยกไม่ได้**ระหว่าง "client ไม่มีเลนส่งเฟรม pickup" กับ "คลิกทุกครั้งเกิดหลัง element หมดอายุ/หลุดจาก clickable list ไปแล้ว" — ใบเดิมสันนิษฐานว่าคลิกทั้งที่มองไม่เห็นยังโดน hitbox ได้ ซึ่งรอบนี้ไม่มีหลักฐานรองรับสมมติฐานนั้นเลย

## 🔴 PANYA-ORDER (2026-08-29 ~20:1x — คำเจ้าของ)
"ไปทำให้ของมันค้างอยู่นานๆ ก่อน ก่อนจะมาให้เทสคลิกอะไรที่โผล่มาเสี้ยว 1 ของ 1 วินาที"
⇒ ก่อนเปิดรอบ capture คลิกใดๆ อีก: chief/สาย B ต้องทำให้ element ค้างบนจอ/ใน clickable list นานพอ (โยงงานที่มีอยู่: `GT-149` — `DROP_LIFETIME_SECONDS=120` เป็นเลขที่สาย B เลือกเองไม่เคยวัด · `GT-132` ป้ายหายเร็ว · เลน bit08_render กำหนดอายุ element ฝั่ง server) — GT-146 รอบถัดไปเปิดได้เมื่อของค้างจริงเท่านั้น

## ของแถม (observation ไม่ใช่ claim)
- แชทผี: เจ้าของพิมพ์ "1" + Enter → เฟรม `0xAC52` ถึง server 20:00:18.085 จริง แต่**บรรทัดไม่ขึ้นในช่องแชทฝั่งเธอเอง** — พฤติกรรม client ที่ยังไม่มีใบไหนอธิบาย (บันทึกไว้เฉยๆ)
- `V134_P0_P30_P91_ISOLATED_INITIAL_READY` + `REAPPLY_READY` ออกในบูตนี้ด้วย (เลนเดิมของบูตมาตรฐาน) — ไม่เกี่ยวใบนี้ จดไว้กัน confound

## nonclaims
1. ไม่อ้างว่า client ไม่มีเลน pickup (เหตุผลข้างบน) 2. ไม่ decode hexdump NEAR/FAR 3. ไม่ตัดสินสี/ข้อความป้ายจนกว่าดูวิดีโอ 4. รอบนี้ ship ศูนย์บรรทัด ไม่นับเวอร์ชัน

ลงชื่อ: กะ3-A
