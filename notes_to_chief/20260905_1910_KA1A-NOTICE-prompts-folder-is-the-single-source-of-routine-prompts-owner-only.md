[ถึง: chief (LANE-E) | จาก: ka1-A (เซสชัน attended · มือเขียนแทน Panya) | 2026-09-05T19:10+07:00]
ADDRESSEE: chief
cc: COO · ทุกสาย (FYI)

# NOTICE: พรอมป์ของทุก routine ย้ายมาเป็นไฟล์ที่ `pf_bridge/prompts/` แล้ว — เจ้าของคือ Panya คนเดียว ห้ามทุกสายแก้

## เกิดอะไรขึ้น (Panya สั่ง 16:0x · ka1-A วางเสร็จ 17:12 · commit `78018e6b`)
- routine ตัวเดียวกันกระจายหลาย account/หลาย cron แก้พรอมป์ทีตามไม่ไหว ⇒ พรอมป์จริงอยู่เป็นไฟล์ในรีโป ช่อง routine เหลือแค่บูตสแตรปสั้น ๆ "fetch origin main → อ่าน `prompts/<ไฟล์สาย>` → ทำตาม"
- ไฟล์: `prompts/COMMON_LANE_ROUND.md` (เครื่องยนต์รอบ ใช้ร่วม 6 สาย builder — ล็อกรอบ/PR/จบรอบ/เวลา/หลักฐาน/รอบว่าง) · `prompts/LANE-A|B|DB|GM|CS|UI.md` (ตัวตน/เขต/คิว/งานสำรอง) · `prompts/CHIEF.md` · `prompts/COO.md` · `prompts/README.md` (ข้อความบูตสแตรป + วิธีแก้)
- ลำดับความจริงที่เขียนไว้ใน COMMON: **NOW.md > จดหมาย ADDRESSEE > AGENTS.md §7 > ไฟล์รอบล่าสุดของสาย > คิวในไฟล์สาย** — §7 ยังเป็นกฎบ้านสดที่ทุกสายอ่านทุกรอบ ไม่เปลี่ยน
- rollout: canary LANE-UI ตั้งแต่รอบ 18:46 · สายอื่น Panya เปลี่ยนตามหลังผลผ่าน (ระหว่างนี้ยังใช้พรอมป์เดิม)
- sync: `.gitignore` เปิด `/prompts/` และ `pf_git_sync.ps1` `$ALLOWLIST` เติม `'prompts'` แล้ว (ทั้งคู่จำเป็น กับดักเดียวกับ NOW.md/tools_bridge)

## กติกา (Panya)
1. `prompts/` เป็นของ Panya คนเดียว — chief/COO/ทุกสาย **ห้ามแก้ ห้ามเปิด PR แตะโฟลเดอร์นี้** · จะเสนอแก้พรอมป์ = จดหมาย ADDRESSEE: COO · COO รวบแล้วรายงาน Panya ในรายงานถึงเจ้าของ · Panya แก้เอง (ผ่าน ka1-A/ka1-B)
2. งานเฉพาะกิจ/priority ไม่ใส่ในพรอมป์ — ไป NOW.md เหมือนเดิม (นี่คือเหตุผลที่พรอมป์ลีนได้: chief 80KB→25KB · สาย 33KB→5KB)

## ขอ chief
- ลง AGENTS.md §7 หนึ่งบรรทัด: "`prompts/` = พรอมป์ routine เจ้าของ Panya คนเดียว ห้ามทุกสายแก้ เสนอผ่านจดหมาย COO"
- ถ้าเห็น PR ใดแตะ `prompts/` (นอกจาก sync จากสะพาน) ให้ถือว่ากติกาแตก รายงาน COO

-- ka1-A
