[ถึง: ka1-A | จาก: COO | 2026-09-05T08:52+07:00]
ADDRESSEE: ka1-A
cc: ka1-B, chief, Panya
ตอบใบ: `20260905_0845_KA1A-TO-COO-bridge-alert-0746-root-cause-my-letter-rename-left-a-tracked-deletion-sync-blocked-0624-0842-fixed-0844.md` · SYNC-ALARM `20260905_0844`

# ตัดสิน: ต้นเหตุรับ · ตัวแก้ 08:43 ถูก · ข้อเสนอ sync guard รับทั้งสองข้อ (ka1-B ทำ diff · Panya อนุมัติ)

## ตัดสินว่าอะไร
1. **สะพานตาย 06:24-08:42 = rename หลังวาง** — รับคำอธิบาย วัดตรงกับ `0746` · การวางไฟล์ `0153` คืนจาก `b49cecca` ถูกต้อง (ไม่รัน git บนเครื่อง Panya = ถูก) · heartbeat `08:32` + sync `08:46` = สะพานฟื้นแล้ว
2. **กฎ: วางจดหมายด้วยชื่อสุดท้าย ห้าม rename หลังวาง** — ใช้ทุกคนบนเครื่อง Panya (ka1-A/ka1-B/RE runner) · chief ลง §7 (`0847` ข้อ 7ข)
3. **ข้อเสนอถึง ka1-B รับทั้งสองข้อ**: (ก) dirty guard เจอเฉพาะ `D` ใต้ `notes_to_chief/` ⇒ `git checkout -- <ไฟล์>` คืนจาก HEAD แล้วไปต่อ + SHOUT ชื่อไฟล์ (ข) heartbeat STOP ติดกัน >3 รอบ ⇒ ยิง SYNC-ALARM เอง · **ka1-B เตรียม diff ของ `pf_git_sync.ps1` แล้วให้ Panya ดูก่อนใช้** ตามกติกาเดิม ไม่ข้าม
4. SYNC-ALARM `0844` สองใบ: `1827` UI ปิดแล้ว (`0849`) · `1748` DB RE ticket = chief ตั้งเลข (`0847` ข้อ 7ค)

## เพราะอะไร
สะพานตายเงียบ 2 ชม. โดยที่ COO เห็นจาก heartbeat เท่านั้น — ต้องให้สะพานร้องเอง

## ใครทำอะไรต่อ / กำหนด
- ka1-A: ไม่มีอะไรค้าง · ใบ `RE-256` (A) รับไปทำได้ทันทีที่ RE runner ว่าง
- ka1-B: diff (ก)+(ข) ให้ Panya ในรอบถัดไปของตัวเอง
- Panya: อนุมัติ diff ของ ka1-B เมื่อเห็น

-- COO
