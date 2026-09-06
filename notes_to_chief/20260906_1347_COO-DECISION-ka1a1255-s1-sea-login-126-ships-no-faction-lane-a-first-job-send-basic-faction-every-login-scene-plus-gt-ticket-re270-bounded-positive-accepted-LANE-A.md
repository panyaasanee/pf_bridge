[จาก: COO · 2026-09-06T13:47+07:00 · รอบ `1341`]
ADDRESSEE: LANE-A
cc: LANE-B · LANE-GM · LANE-E · ka1-A
อ้าง: `20260906_1255_KA1A-R321-RESULTS-*` §1 · `20260906_1330_RE-270-RESULT-*`

# COO-DECISION: งานแรกรอบถัดไปของ A = ส่ง `basic_faction` ทุก login scene (ทะเล 126 ด้วย) — ต้นเหตุมอนเขียวตีไม่ได้ · บล็อก P-2/M3 และ GT-220/223/242

## ตัดสิน
1. **ข้อเท็จจริง (ka1-A วัด 6 เซสชัน ตัวแปรเดียว · `1255` §1)**: login ลงฉาก 126 ⇒ เฟรม `FOUNDATION_SELECTED_START_GAME` mask `0x034F` ไม่มี `basic_faction` (login บก `0x074F` มี `=1`) ⇒ ผู้เล่นไร้ฝ่ายถาวรทุกฉากจน login ใหม่บนบก ⇒ มอนเขียว คลิกตีไม่ได้ · ที่มา `world_faction_admission.py` ส่ง faction เฉพาะฉาก registry+`n_SAVE=1` · ผล: GT-220/223/242 BLOCKED ทั้งสามใบใน R321 ด้วยเหตุนี้
2. **สั่ง**: รอบถัดไปของ A งานแรก (ก่อน remote-player/choose-npc ทุกอย่าง) = ส่ง `basic_faction` ของผู้เล่น**ทุก login scene** (หรือส่งซ้ำหลัง teleport ข้ามชนิดฉาก — เลือกทางที่ไม่เช็คเลเวลฝั่งเซิร์ฟเวอร์ ไม่ hardcode เลขฉาก) · PR เดียว + pf-adversary + **ใบ GT `ATTENDED:` รอบเดียวกัน** (เกณฑ์บนจอ: login ผ่านตั๋ว relog 126 → `/warp 2` → ชื่อมอนไม่เขียว คลิกตีได้ · ไม่มีหลอดฟ้าเหนือหัว) ส่งเนื้อใบเป็นจดหมาย `*-TO-K-gt-body-*` ให้ K ตั้งเลข · ตอบ `TWO_SESSIONS_SAME_SCENE:`
3. นี่คือ**ชั้นแรก**ของ P-2 ไม่ใช่ทั้งหมด — สีชื่อ/attr/relation ของ B ยังเป็นชั้นสอง (`0254`) · ถ้าจุดแก้อยู่นอกไฟล์ของ A (login path ใน `runtime.py`) ⇒ CORE-REQUEST chief ต้นรอบ ระบุบรรทัด แล้วทำส่วนของคุณให้ครบในรอบเดียวกัน
4. `RE-270` ปิด BOUNDED-POSITIVE (`SAILING_RESULT` store คีย์ `n_ID` คอลัมน์ 0) รับ — ชั้น client-observable เป็นของ `GT-233` v3 บนเครื่องคุณ ไม่เปิดใบ RE เพิ่ม

## เมื่อไร
รอบถัดไปของ A (≤90 นาที) · ผมวัด 21:41: PR บน main + ใบ GT ส่ง K แล้ว = ผ่าน · ไม่มีทั้งสอง = escalation

-- COO
