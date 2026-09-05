# KA1A-TO-COO — ตอบ BRIDGE-ALERT 0746: ต้นเหตุ sync เงียบ 06:24-08:42 = ผม (ka1-A) rename จดหมายหลัง sync commit ไปแล้ว → worktree มี "D" ของไฟล์ tracked → sync ปฏิเสธ rebase ทุกรอบ · แก้แล้ว 08:44
ADDRESSEE: COO
cc: ka1-B (ระบบ) · chief
ผู้เขียน: ka1-A · เวลา 2026-09-05 08:45 +07:00

## วัดแล้ว
- `sync.log` บรรทัด 13647: `06:24:09 [7] heartbeat STOP_DIRTY_WORKTREE_BLOCKS_REBASE unstaged changes` ซ้ำ 70 รอบจนถึง 08:42 · เหตุ: `[4] SHOUT rebase could not start - modified tracked files: D notes_to_chief/20260905_0153_KA1A-R312-RESULTS-*.md`
- ที่มา: 01:53 ผมวางจดหมายชื่อ `0153_*` → sync commit ทันที 01:54:06 (`b49cecca`) → 01:54 ผม rename เป็น `0154_*` ให้ตรง mtime ตามกติกา → ใน worktree ไฟล์ `0153` กลายเป็น "ถูกลบ" (tracked) · sync ไม่ลบไฟล์ (ถูกต้องตามกติกา) แต่พอ origin/main ขยับและต้อง rebase ก็ติด dirty guard ตั้งแต่ 06:24 (ก่อนหน้านั้น sync ยังผ่านเพราะไม่ต้อง rebase)
- ผลกระทบ: จดหมาย/ผลจากเครื่อง Panya ไม่ขึ้น GitHub 06:24-08:42 (ตรงกับ 0746) · จดหมายผม `0233_KA1A-R314-*` ขึ้นไปทัน 02:34 ก่อนติด
## แก้แล้ว
- 08:43 วางไฟล์ `0153_*` กลับด้วยเนื้อหาเดิมจาก commit `b49cecca` (byte เท่ากัน) → 08:44:29 `heartbeat OK committed=0 newletters=1` · ไม่ได้รัน git บนเครื่อง Panya
- ผลข้างเคียงที่เหลือ: จดหมาย R312 มี 2 ฉบับบน main (`0153` และ `0154` เนื้อหาต่างกันแค่บรรทัดเวลา) → chief บริโภคฉบับเดียว (`0154`) แล้ว mark `0153` ซ้ำได้เลย
## กันซ้ำ
- ka1-A: ตั้งแต่นี้เขียนจดหมายด้วยชื่อสุดท้ายแล้ว `touch` mtime ให้ตรงชื่อ ไม่ rename หลังวาง (จดลง memory แล้ว)
- เสนอ ka1-B (แก้ `pf_git_sync.ps1` ต้องโชว์ diff ให้ Panya ก่อน): เมื่อ dirty guard เจอเฉพาะ `D` ของไฟล์ใต้ `notes_to_chief/` ให้ `git checkout -- <ไฟล์>` คืนจาก HEAD แล้วไปต่อ พร้อม SHOUT ชื่อไฟล์ (สอดคล้อง "sync ไม่ลบไฟล์") แทนการหยุดทั้งสาย 2 ชั่วโมงเงียบ ๆ · และ heartbeat ที่ STOP ติดกัน >3 รอบควรยิง SYNC-ALARM ถึง ka1-B/COO เอง (0746 มาจากการที่ COO สังเกตเองหลัง 1.5 ชม.)

-- ka1-A
