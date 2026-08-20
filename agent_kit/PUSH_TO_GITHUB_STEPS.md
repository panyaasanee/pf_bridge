# 🚀 ขั้นตอน push repo ขึ้น GitHub ครั้งแรก

**ตรวจความปลอดภัยแล้วด้วยจ็อบ `917` เมื่อ 2026-08-19 23:4x — ผลเขียวทุกข้อ**

| ตรวจอะไร | ผล |
|---|---|
| remote ปัจจุบัน | **ไม่มีเลย** — ไม่เคย push ไปไหนทั้งนั้น |
| ไฟล์ที่ถูก track | **449 ไฟล์ · รวม 5.99 MB** |
| ไฟล์ที่ track เกิน 1 MB | **ไม่มีสักไฟล์** |
| `GameClient*.bin` · `gameclient.bi_` · `*.dmp` | ✅ **ไม่ถูก track** |
| `*.sqlite3` (canonical DB + run copies) | ✅ **ไม่ถูก track** |
| zip ก้อนใหญ่ (75.5 MB / 25.7 MB) | ✅ **ไม่ถูก track** |
| `references/` `evidence/` `capture_v141/` `v77_video_frames/` `backups/` `logs/` `state/` | ✅ **ไม่ถูก track** |
| ไฟล์ที่ยังไม่ track และ **ไม่ได้** ถูก ignore (เสี่ยงโดน `git add -A` กวาด) | ✅ **0 ไฟล์** |
| branch / HEAD | `main` / `47c7211` (chief รอบ 91) |

⇒ **`.gitignore` ฉบับ 20 KB ทำงานถูกต้องครบถ้วน — push ได้อย่างปลอดภัย**

---

## ขั้นตอน (ท่านรันเอง — ผมไม่แตะขั้นตอน auth)

### 1. สร้าง repo เปล่าบน GitHub
**ตั้งเป็น Private** · **อย่าติ๊ก** "Add a README" / "Add .gitignore" / "Choose a license"
(ถ้าติ๊ก จะมี commit แรกที่ไม่ตรงกับของเรา แล้วต้อง merge โดยไม่จำเป็น)

### 2. เปิด PowerShell แล้วรัน

```powershell
cd "C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject"

# ตรวจซ้ำอีกครั้งด้วยตาตัวเองก่อน (ควรได้ 449 และไม่มีอะไรน่าตกใจ)
git ls-files | Measure-Object -Line
git ls-files | Select-String -Pattern '\.bin$|\.dmp$|\.zip$|\.sqlite3$'   # <- ต้องไม่คืนอะไรเลย

# ผูก remote (แทน <URL> ด้วยของจริง)
git remote add origin <URL>
git remote -v

# push ครั้งแรก
git push -u origin main
```

### 3. ยืนยันด้วยตาบนเว็บ
เปิด repo บน GitHub แล้ว **ดูว่าไม่มีโฟลเดอร์ `GameClient` และไม่มีไฟล์ `.bin` / `.dmp` / `.zip`**
🔴 **อย่าเชื่อผลตรวจของผมอย่างเดียว — ดูด้วยตาอีกชั้นหนึ่ง** เพราะถ้าพลาดชั้นนี้ แก้ทีหลังต้องล้าง history

---

## ⚠️ ข้อควรระวัง

- **ตอนนี้ chief กำลัง commit อยู่เรื่อย ๆ** (รอบ 91 = `47c7211`) ⇒ ถ้า push แล้วรอสักพัก
  ค่อย `git push` ซ้ำเพื่อเก็บ commit ใหม่ · หรือรอให้ chief จบรอบก่อนค่อย push
- **ห้ามใช้ `git add -A` แบบไม่ดู** — วันนี้ผลออกมาว่าไม่มีไฟล์ค้าง แต่ถ้าวันหลังมีไฟล์ใหม่
  ที่ `.gitignore` ยังไม่ครอบคลุม มันจะโดนกวาดไปด้วย
- **`pf_bridge\` อยู่นอกรีโป** — คิวเทส กล่องจดหมาย และ `agent_kit\` **จะไม่ขึ้นไปด้วย**
  ⇒ ต้องตัดสินใจแยกต่างหาก (ดูหัวข้อถัดไปในโน้ตถึง chief)
