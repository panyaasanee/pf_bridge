# ✅ วัดจริงแล้ว: สภาพแวดล้อมของ **Routine** ที่ chief จะไปรัน — และมันใช้ได้

## 🔴 แก้ความเข้าใจผิดของทั้งโปรเจกต์ก่อน
เราวางแผนกันมาทั้งวันบนสมมติฐานว่า cloud chief = **scheduled task ของ Cowork** — **ผิด**
probe ยิงจริง 2026-08-20 15:4x พิสูจน์ว่า scheduled task แบบนั้น **ไม่มี credential ของ GitHub เลย**
(`could not read Username` · ไม่มี gh · ไม่มี credential helper) และ **ไม่มี device bridge** ⇒ clone ไม่ได้เลย

**กลไกที่ถูกชื่อ Routines** (`claude.ai/code/routines`) — prompt + **รายชื่อ repo** + connectors
เอกสารระบุ: *"Each repository is cloned at the start of a run"* และ *"keep working when your laptop is closed"*
⇒ **มัน clone repo private ให้เองทุกรอบ** ซึ่งเป็นสิ่งเดียวที่ scheduled task ทำไม่ได้

---

## สิ่งที่ probe รอบสองวัดได้ (ทุกบรรทัดคือผลจริง ไม่ใช่คำสัญญาจากเอกสาร)

### ✅ โครงพี่น้อง — **ปิดเงื่อนไข ③ ของ chief verdict ได้แล้วโดยไม่ต้องแตะโค้ด**
```
/home/user/pf_bridge
/home/user/pirate-force-server
```
`/home/user/pf_bridge/../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` → **EXISTS (11,388 bytes)**
⇒ `tools/pf_vital_name_thunk_static.py:127` (`ROOT.parent / "pf_bridge"`) **ทำงานได้ที่นั่นเหมือนบนเครื่อง Panya**

🔴 **แต่มันจริงเพราะ Panya เปลี่ยนชื่อ repo บน GitHub เป็น `pf_bridge`** — probe รอบแรกได้
`pirate-force-bridge` และ path นั้น **NOT FOUND** ⇒ **โฟลเดอร์ถูกตั้งชื่อตามชื่อ repo บน GitHub**
**เขียนกฎนี้ลงเอกสารพร้อมเทสที่ล้มถ้าหาไม่เจอ** (เงื่อนไข ③ เดิม) — ตอนนี้มันจริงโดย "ชื่อ repo บังเอิญตรง"
ซึ่งคือสมมติฐานเงียบชนิดเดียวกับที่ chief เตือนไว้เอง

### ✅ ไฟล์ครบ
| repo | ไฟล์ที่ clone มา |
|---|---|
| `pf_bridge` | **228** (= tracked เป๊ะ) |
| `pirate-force-server` | **519** (= tracked เป๊ะ) |
`CHIEF_CONTINUATION.md` 88,484 B · `GAME_TEST_QUEUE.md` 80,264 B · `agent_kit/` ครบ

### ✅ git ใช้ได้ · remote ตั้งแล้วทั้งสอง repo
`origin https://github.com/panyaasanee/pf_bridge` · `.../pirate-force-server`

### ⚠️ ล่ามต่างรุ่นจากสะพาน
| | สะพานของ Panya | Routine |
|---|---|---|
| OS | Windows | **Linux 6.18 x86_64** |
| Python | **3.14** | **3.11.15** |
| console | **cp874** | ไม่ใช่ |
🔴 **⇒ Windows gate ต้องอยู่บน GitHub Actions ต่อไป ห้ามให้ chief-บน-Routine อ้างว่าตัวเองรัน gate แทนได้**
กับดัก cp874 และ `py -3` 3.14 **ไม่มีอยู่ที่นั่น** — เขียวที่นั่นไม่ได้แปลว่าเขียวบนสะพาน

### ✅ package พร้อม (ผ่าน setup script ของ environment ซึ่งถูก cache)
`pytest 9.1.1` · `capstone 5.0.7` · `pefile 2024.8.26` · เน็ต: `curl -sI https://pypi.org` → **HTTP/2 200**

### 🔴 สิ่งที่ **ไม่มี** ที่นั่น (และทำไมงานรอบ 106 ของคุณคือสิ่งที่ทำให้ทั้งแผนเป็นไปได้)
**ไม่มี canonical DB · ไม่มี `backups/` · ไม่มี capture corpus · ไม่มี client image**
⇒ นี่คือ fresh clone ตัวจริง ⇒ **`skipUnless` + SKIP-CENSUS-001 ที่คุณเพิ่งลงในรอบ 106 คือชิ้นส่วนที่ทำให้
cloud chief รันสวีตได้โดยไม่แดงมั่ว** · ไม่ได้ทำเพื่อ Actions อย่างเดียว มันคือ **เงื่อนไขของการขึ้น cloud**
⭐ **ผลพลอยได้:** FINDINGS R41 (pytest แตะ canonical ผ่าน mount) **หายไปเองที่นั่น** เพราะไม่มี canonical ให้แตะ

---

## กติกาของ Routine ที่ต้องเขียนลง prompt ฉบับ cloud
- **push:** branch ขึ้นต้น `claude/` **รับเสมอ** · branch อื่นรับก็ต่อเมื่อ **ไม่ถูก protect · ไม่มี PR เปิดค้างจาก branch นั้น · ไม่มี commit ของคนอื่น**
- **commit/PR จะขึ้นชื่อ GitHub ของ Panya** (routine ผูกกับบัญชีเธอ)
- 🔴 **ช่อง Environment variables ห้ามใส่ credential เด็ดขาด** — เอกสารระบุว่าไม่มี secrets store และใครใช้ environment นั้นก็อ่านได้
- **มีเพดานจำนวนรันต่อวัน** แยกจาก usage ปกติ ⇒ **cadence รายชั่วโมง = 24 รอบ/วัน อาจชนเพดาน**
  Panya ต้องดูตัวเลขจริงที่ `claude.ai/code/routines` ก่อนตั้ง cron · **ถ้าไม่พอ ให้ลดเป็นทุก 2-3 ชั่วโมง**
- รันแบบ autonomous **ไม่มี approval prompt คั่น** ⇒ prompt ต้องเขียนให้จบในตัวเอง

## 🔴 สิ่งที่ยัง **ไม่มีคำตอบ** และต้องออกแบบก่อนสับสวิตช์
**ผู้เทส local จะรับใบสั่งยังไง** — ตอนนี้ผู้เทสอ่าน `pf_bridge\` บนดิสก์ตรง ๆ
แต่ cloud chief จะเขียนใบสั่งลง **repo บน GitHub** ⇒ เครื่อง Panya ต้อง `git pull` ถึงจะเห็น
และผลเทสต้อง `git push` กลับขึ้นไปถึง chief จะเห็น
⇒ **ต้องมีตัว sync ฝั่ง Windows** (Task Scheduler ทำ `git pull`/`push` เป็นระยะ) **ไม่ใช่ให้ Panya พิมพ์เอง**
🔴 ถ้าไม่มีตัวนี้ **Panya จะกลายเป็นสายพานส่งของด้วยมือตลอดไป ซึ่งเธอปฏิเสธชัดเจนแล้ว**
**ออกแบบมาเสนอในรอบถัดไป** พร้อมคำตอบว่า LOCK ทำงานยังไงเมื่อไฟล์ธงอยู่คนละเครื่องและถูก `.gitignore` กันไว้

## สถานะเช็คลิสต์หลัง probe นี้
| # | ข้อ | สถานะ |
|---|---|---|
| 1-4 · 8 · 9 | repo สะอาด · factpack · VCS · remote · ผู้เทส · แผนตอนปิดคอม | ✅ |
| 6 | หนี้ coverage | ✅ (หมุด 33 → 0 รอบ 105) |
| 5 | Actions เขียว → ปลูกแดง → เขียวกลับ | 🔲 รอ run #4 |
| 7 | prompt ฉบับ cloud | 🔲 **งานถัดไปของคุณ — rebase ให้ตรงกับข้อเท็จจริงข้างบน** |
| 🆕 10 | ตัว sync ฝั่ง Windows สำหรับผู้เทส | 🔲 **ยังไม่มีใครออกแบบ** |
