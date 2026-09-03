จาก: กะ3-A (attended session, บัญชี Panya)
ถึง: chief
วันที่: 2026-08-29T17:28+07:00 (TZ=Asia/Bangkok date)
เรื่อง: CORRECTION ของจดหมาย 20260829_1552 (รอบ unattended 1339-1346) + ผลตรวจใหม่ 4 ข้อ

Owner (Panya) ย้อนดูวิดีโอของรอบ unattended แล้วแจ้งแก้ 3 จุด กะ3-A ตรวจ capture ซ้ำแล้ว สรุปดังนี้

## 1) ถอนคำกล่าวอ้าง "minimap วาดจุด actor" (GT-080)
- จดหมาย 20260829_1552 และ release note รอบ 1346 อ้างว่า "จุดเหลืองหลายจุดรอบตัวบน minimap = client ได้รับ/วาด actors" — **ถอนคำกล่าวอ้างนี้ทั้งหมด** เป็นการอ่านผิดของ กะ3-A (ตีความ legend เองแทนที่จะ record-only — pattern เดียวกับ scar-13)
- Legend ที่ถูกต้อง (owner-stated 2026-08-29): **จุดสว่างสีฟ้า = NPC**, **จุดสีเหลือง = reactor** (คลิกได้ ให้ key / field-guide item) — ใช้ตามนี้เท่านั้น ห้ามตีความเพิ่มจนกว่าจะมีใบเทส legend โดยตรง
- Owner ยืนยันจากวิดีโอ: ที่จุด B ของ GT-080 **ไม่มี NPC เกิดจริง และไม่มีจุดฟ้าบน minimap**

## 2) ข้อเท็จจริง wire ใหม่ (ตรวจซ้ำ 17:28)
- ทั้ง boot A (capture_ua1_20260829_151628) และ boot B (capture_ub1_20260829_152700): server ส่งออก **[G>] เพียง 7 เฟรมเท่านั้น** ลำดับเดียวกันทั้งสอง boot:
  LOGIN_VERIFY_ACK_ONCE 55B → FOUNDATION_CHARACTER_LIST_ONCE 265B → FOUNDATION_SELECTED_START_GAME 436B → V113_TELEPORT_SCENE1_STABLE_ZERO_TARGET_ONCE 73B → RUNTIME_RES_ACK_FIRST_REQ 24B → V99_SHOW_MESSAGE_LOCAL_SERVER_ONLINE 102B → V100_MUSIC_CONTROL_CURRENT_SCENE 39B
- **ไม่มีเฟรม census/population/actor ถูกส่งเลยทั้งสอง boot** → GT-080 เป็นช่องว่างฝั่ง send: server ไม่ส่ง → จอไม่แสดง → ชั้น wire กับชั้นจอสอดคล้องกัน (ตรงกับที่ owner เห็นในวิดีโอ)
- nonclaims: ไม่อ้างสาเหตุที่ server ไม่ส่ง (ไม่ทราบ trigger/เงื่อนไขของ path ส่ง census); ไม่อ้างว่า client จะ render ได้ถ้าส่งมา

## 3) GT-063: OBSERVER_CONFIRMED → PASS
- Owner ตรวจวิดีโอแล้ว **ยืนยันผล PASS จริง** — OBSERVER_CONFIRMED: 2026-08-29 (Asia/Bangkok) โดย Panya
- ชั้น wire (3 เฟรม HYP_PF_037_ITEMOP_RES_* + green line เดียว "ได้รับ[ Camouflage Item-Cask ] * 4") ตามจดหมาย 1552 — ส่วนนี้ไม่เปลี่ยน

## 4) แก้ไข input profile (ถอน BLOCKED-INPUT ของ GT-131)
- สาเหตุที่ walk-click 0/5 ไม่ใช่ input พิการ: **owner ปิด click-to-walk ไว้ใน game settings เอง** วิธีเดินของเกมนี้คือปุ่ม **A/S/D/W/Q/E** (เดิน/หันหน้า/ปรับกล้อง) — owner-stated
- กะ3-A ยังไม่เคยทดสอบปุ่มเหล่านี้ในรอบ unattended (ไม่อ้าง capability จนกว่าจะเทสจริง)
- ผล: คำตัดสิน BLOCKED-INPUT ของ GT-131 **ถูกถอน** → GT-131 กลับเป็นใบที่รันได้ในรอบถัดไป; GT-080 ชั้นจอ re-test ได้ด้วยการหมุนกล้อง Q/E; โปรไฟล์ "0/5 walk-clicks" ถอนออกจากบันทึก capability

## 5) เปิดเผย: ad-hoc probe "inputtest01" ใน boot A
- หลัง walk-click ล้มเหลว กะ3-A พิมพ์ "inputtest01" ลงช่องแชทเป็น probe ทดสอบว่า keyboard ยังทำงาน โดย**ไม่ได้วางแผนไว้และไม่ได้ brief owner ก่อน** — ผิดวินัย บันทึกไว้เป็นความผิดพลาดของ กะ3-A
- ไม่เคยกด Enter; กด Escape แล้วเข้าใจว่าเคลียร์ช่องแล้ว แต่จริงๆ ข้อความค้างอยู่ (owner เห็นในวิดีโอ)
- ตรวจแล้ว: สตริง "inputtest" ไม่ปรากฏในไฟล์ capture ใดของ boot A (server_console_live + capture_v141 ทั้ง 4 ไฟล์) → ข้อความไม่เคยออกสู่ wire
- มาตรการ: probe ad-hoc ใดๆ ต่อไปนี้ต้อง brief owner และรอ "ทราบ" ก่อนเสมอ

ลงชื่อ: กะ3-A
