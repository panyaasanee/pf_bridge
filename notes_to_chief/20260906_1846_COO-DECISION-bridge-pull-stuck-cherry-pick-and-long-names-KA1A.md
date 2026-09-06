[ถึง: ka1-A (มือที่เครื่อง Panya) · จาก: COO | 2026-09-06T18:46+07:00]
ADDRESSEE: ka1-A
cc: Panya · chief (LANE-E)
ตอบใบ: `SYNC_STUCK_20260906_1816` `1834` `1836` `1842` `1844` (สะพานเขียนเอง 5 ฉบับ)

# COO-DECISION: สะพานฝั่งเครื่องคุณ pull ไม่ได้ตั้งแต่ 18:16 — แก้ได้ที่เครื่องเท่านั้น สองคำสั่ง

## ตัดสินอะไร
เครื่อง Panya **เปิดแล้ว** (heartbeat 18:16 → 18:44 · push จากเครื่องขึ้น main ได้ปกติ) แต่ **pull เข้าเครื่องติด** ทุกรอบ (behind 165 → 7 · ahead 0) ⇒ จดหมาย/ใบใหม่จาก cloud (เช่น `GT-281` READY) **ไม่ถึงเครื่อง** จนกว่าจะแก้ · สะพานครึ่งตาย = สำคัญกว่าไมล์สโตน (COO.md)

## เพราะอะไร (อ่านจาก `git said:` ในใบ STUCK ทั้ง 5 — ไม่ใช่เดา)
1. **18:16**: `Filename too long` ×6 ไฟล์ — ทั้ง 6 เป็นชื่อ 190–222 อักขระ และ **5 ใน 6 เป็นไฟล์ COO เอง** (`COO-DECISION`/`COO-ROUND`) · COO ผิดกฎ `AGENTS.md §7` "ชื่อไฟล์ ≤ 100 ตัวอักษร" ที่มีอยู่แล้ว · **แก้ที่ COO ตั้งแต่ใบนี้: ชื่อไฟล์ COO ทุกใบ ≤ 100** · ขอ chief ตั้งเกต (ใบแยก `1846 … LANE-E`)
2. **18:34 เป็นต้นมา**: `You have not concluded your cherry-pick (CHERRY_PICK_HEAD exists)` — `pf_git_sync.ps1` ไม่มีคำว่า cherry-pick แม้แต่บรรทัดเดียว ⇒ **มีคนสั่ง cherry-pick ด้วยมือบน clone `pf_bridge` ของเครื่อง** แล้วค้างไว้ · จนกว่าจะปิด ทุก `merge --ff-only` ถูกปฏิเสธ

## ใครทำอะไร เมื่อไร
**ka1-A (หรือ Panya) ที่เครื่อง · ทันทีที่เห็น** ใน clone `pf_bridge`:
```
git status
git cherry-pick --abort
git config core.longpaths true
```
- `git status` ก่อน: ถ้า cherry-pick นั้นตั้งใจทำและมีของต้องเก็บ → เก็บเป็น**ไฟล์ใหม่**ใน `notes_to_chief/` (ทางที่สะพาน push ได้) แล้วค่อย abort · ห้าม commit ทับ main ของเครื่อง (push allowlist ไม่พาไป · ตรงกับกฎ "ห้ามแก้ไฟล์เดิม" `AGENTS.md §7`)
- `core.longpaths true` ทำให้ 6 ไฟล์ยาวที่ค้างอยู่ checkout ได้ — ไม่ต้อง rename ไฟล์เก่า (rename = deletion บนสะพาน ห้าม)
- แล้วรอ sync รอบถัดไป (สคริปต์ตื่นเอง) — ถ้า ff ผ่าน ไฟล์ `SYNC_ATTENTION.txt` หายเอง และไม่มี `SYNC_STUCK_*` ใบใหม่ = จบ
- ยังติดหลังทำสองคำสั่ง → เขียน `notes_to_chief/<เวลา>_KA1A-TO-COO-bridge-still-stuck.md` แปะ `git status` + `git said:` — COO ตัดสินต่อรอบ 19:41

## COO ทำอะไรแล้ว
- แจ้ง Panya ผ่าน notification 18:46 (ช่องทางเดียวที่ถึงเครื่องตอนนี้ — ใบนี้จะถึงเครื่องได้ก็ต่อเมื่อ pull กลับมา)
- `NOW.md` แก้บรรทัดบนสุดจาก "สะพานเงียบ เครื่องปิด" เป็น "เครื่องเปิด · pull ติด" + ใส่ในหัวข้อ "รอ Panya ติ๊ก"
- ผลถ้าไม่แก้: ใบ attended ทุกใบบูตจากคิวเก่า (ไม่เห็น `GT-281` `GT-279` ฉบับล่าสุด) · จดหมาย COO/chief ทุกฉบับหลัง 18:16 ไม่ถึงเครื่อง

-- COO
