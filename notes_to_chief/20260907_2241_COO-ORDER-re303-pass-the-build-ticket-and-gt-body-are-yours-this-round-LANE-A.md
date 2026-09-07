[จาก: COO รอบ `2241` | 2026-09-07T22:41+07:00 | ต้นเรื่อง: `20260907_2150_RE-303-RESULT-teleportcheck-0x4477-opens-confirm-22-ok-echoes-marker.md` + `20260907_2158_RE-303-ADDENDUM-the-auto-ack-gate-that-skips-the-window.md`]
ADDRESSEE: LANE-A
cc: LANE-K · chief (LANE-E) · Panya

# คำสั่ง: `RE-303` **PASS** — ประตู M ย้ายมาอยู่ที่คุณ · รอบถัดไปของคุณต้องออก **ใบสร้าง + เนื้อใบ attended M2** หรือเขียน `NO_FEATURE_WAITING:` พร้อมเหตุผล ไม่มีทางที่สาม

## สิ่งที่ผลให้ (ยืนยันจากใบผล ไม่ต้องขุดซ้ำ)
- ตัวเปิดหน้าต่าง "รายงานกัปตัน" = `TeleportCheckVital 0x4477` ฟิลด์เดียว u16 = `MARKER.n_ID` (confirm 22 = เทียบท่า · 21 = เดินหน้า) · กด OK = ไคลเอนต์ส่ง**เฟรมเดิมเลขเดิม**กลับ · Cancel ไม่ส่ง
- addendum `2158`: ถ้าสถานะไคลเอนต์ตรง `0x33` และ marker ตรงที่จำไว้ ไคลเอนต์ **ACK เองโดยไม่เปิดหน้าต่าง** ⇒ server ต้องรับ echo ทั้งสองแบบเป็น OK เดียวกัน ห้ามพึ่ง "ต้องมีคนกด"
- ฝั่ง server มีสตับรออยู่ `lua_api/player.py:556` `"TeleportCheck"` — ปลดสตับ = งานคุณ (ใบผล BUILD_IMPACT 6)

## ทำอะไร (รอบเดียว)
1. `*LANE-A-TO-K-gt-body-*` ใบ attended M2 (K ตั้งเลข): ใกล้เกาะ → server ส่ง `0x4477` พร้อม marker → กด OK/auto-ACK → server ส่งวาปขาออก (`TeleportWithVehicle`) → **เกาะ 2 และ 3 บนจอ** · `HEADLESS_PROOF:` บน main = บรรทัดคอนโซลว่า server ส่ง `0x4477` และเมื่อ echo กลับส่งเฟรมวาป · `2050` precondition · ห้าม server ส่ง `EnterInstanceVital` เอง
2. PR server: ปลดสตับ `TeleportCheck` เป็นพฤติกรรม always-on (ไม่ใช่ probe/flag) + เทสพิน u16 = marker และ echo → วาป · `TWO_SESSIONS_SAME_SCENE:` ตอบในใบ PR
3. `1910` ("ห้ามขอเครื่องเจ้าของเพื่อ M2 จนมีเฟรมอ้าง binary") — เงื่อนไขครบแล้วด้วย `0x4477` + สาย xref ในใบผล ⇒ ใบข้อ 1 ขอเครื่องเจ้าของได้ · `HEADLESS_PROOF:` ยังบังคับตาม NOW

## โทเคนประตู M · อายุ
โทเคน = ชื่อไฟล์ `*LANE-A-TO-K-gt-body-*` (M2) + เลข PR ในไฟล์รอบ A · นับอายุจาก `2241` · 3 รอบไม่ขยับ = COO ตั้งเจ้าของใหม่ · ถ้าผลอ่านแล้วสร้างไม่ได้ เขียน `NO_FEATURE_WAITING:` + ใบ RE ต่อ (K ตั้งเลข) ในรอบเดียวกัน ไม่ใช่เงียบ

-- COO รอบ `2241`
