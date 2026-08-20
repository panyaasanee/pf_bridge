# ATTENDED SESSION RUNBOOK — วิธีทำให้คิวเทสเดินได้ ใช้เวลาคุณ ~25 นาที

สร้างโดย chief รอบ 15 (2026-08-17 09:4x) หลังพบว่าคิวเทสรอมา 24 รอบเพราะ
**ไม่มีใครมารับงาน** ไม่ใช่เพราะงานยังไม่พร้อม — รายละเอียดเต็ม:
`FINDINGS_R15_TESTER_TASK_DISABLED.md`

---

## ทำไมต้องเป็น "attended" (คุณนั่งอยู่หน้าเครื่อง)

กำแพงชั้นเดียวที่เหลือคือ **computer use ต้องมีคนกด Allow** — ตรวจสดในรอบ 15 แล้ว
scheduled task ได้ `{"allowedApps":[], "grantFlags":{...false, false, false}}`
คือ **ไม่มีสิทธิ์แตะหน้าจออะไรเลย** ต่อให้เปิด task `pirate-force-game-tester` กลับมา
มันก็จะขับ GameClient ไม่ได้อยู่ดี

ส่วน server / DB / git / gate — ทำได้หมดโดยไม่ต้องมีคุณ (chief ทำมา 15 รอบแล้ว)
**สิ่งเดียวที่ติดคือการคลิกในเกม**

---

## ขั้นตอน (ทำครั้งเดียว)

### 1. เช็คว่า chief ไม่ได้ถือ LOCK อยู่

เปิด `pf_bridge\LOCK.txt` — ถ้าบรรทัดแรกขึ้นต้นด้วย `RELEASED` → เริ่มได้เลย
ถ้าเป็น `HELD` และ timestamp อายุ < 20 นาที → รอ 2–3 นาทีแล้วดูใหม่ (รอบ chief ใช้ 11–17 นาที)

> ถ้าอยากตัดปัญหาให้เด็ดขาด: ปิด task `pirate-force-chief-continue` ชั่วคราวก่อนเริ่ม
> แล้วเปิดกลับตอนจบ — จะได้ไม่มีอะไรมาแย่ง LOCK ระหว่างเทส

### 2. เปิดแชทใหม่ในโฟลเดอร์ `Pirate Force` แล้ววาง prompt นี้ทั้งก้อน

```
คุณคือ Game Runtime Tester ของ Pirate Force Command 2 — เซสชันนี้ผมนั่งอยู่หน้าเครื่อง
พร้อมกด Allow ให้ทุก dialog ที่ขึ้นมา

1. อ่าน pf_bridge\CHIEF_CONTINUATION.md (ข้ามส่วน idle round ที่เก่ากว่ารอบ 11 ได้)
   และ pf_bridge\GAME_TEST_QUEUE.md ให้จบ โดยเฉพาะหัวข้อ PLAYBOOK
2. เขียน LOCK.txt ระบุตัวเองเป็น holder
3. รัน GT-005 (movement position persistence) ให้ครบทุก step ตามที่คิวเขียนไว้
   แล้วต่อด้วย GT-006 (chat input observation) ในรอบ client เดียวกันถ้าทำได้
4. กฎที่ห้ามลืม:
   - ขั้นแรกของ job ต้อง copy state\pirateforce.sqlite3 + เทียบ sha256 ก่อนเสมอ
     (ต้องได้ 673f4bfb1c35ec390d6ed3b0c1fe3f581b20c6895ace9183c86a5971bccc9708)
   - ห้ามนับ count(*) FROM sessions เปล่า ๆ ให้ใช้ WHERE selected_character_id IS NOT NULL
     และบันทึก max(lease_generation) ก่อน/หลัง
   - เปิด client ด้วย ProcessStartInfo + UseShellExecute=$false เท่านั้น
   - ปุ่มในหน้าเลือกตัวละคร (แก้ 2026-08-18 จาก GT-010 ยืนยันด้วย zoom — โน้ตเก่าที่ว่า
     "ปุ่มที่ 2 = ลบ" ผิด): **ปุ่มแรกซ้ายสุด = ลบตัวละคร** · ปุ่มที่ 2 = สร้างตัวละคร ·
     กดลบเฉพาะเทสที่คิวสั่งเท่านั้น — flow ลบจริง: dialog ใช่/ไม่ (ไม่มีช่องพิมพ์ชื่อ) →
     password pad คีย์บอร์ดสุ่ม (พิมพ์คีย์บอร์ดจริงได้) · X ที่หน้า char select ปิดทันที
     ไม่มี dialog ยืนยัน (ต่างจากใน world)
   - ห้าม git commit เอง — กรอกผลลงคิวแล้วให้ chief commit
   - screenshot ทุกจุดสำคัญ เก็บที่ pf_bridge\evidence_screens\
5. จบแล้ว: กรอก result ใน GAME_TEST_QUEUE.md (PASS/FAIL + หลักฐาน + nonclaims)
   → อัปเดต CHIEF_CONTINUATION.md → ปลด LOCK เป็น RELEASED

ถ้าติดอะไรถามผมได้ทันที ผมอยู่ตรงนี้
```

### 3. สิ่งที่คุณต้องทำระหว่างทาง

- **กด Allow** ตอนขอสิทธิ์ `GameClient.local.bin` (ครั้งเดียว ตอนต้น)
- ถ้า client ค้างจนปิดไม่ได้ → **End task ให้** (มีบันทึกว่าเคยเกิดตอน server ปฏิเสธเงียบ)
- นอกนั้นดูเฉย ๆ ได้เลย

---

## ทำไมเลือก GT-005 เป็นตัวแรก (คิวเลือกไว้แล้ว ⭐)

- **ไม่ต้องรอคุณเคาะข้อไหนเลย** — ต่างจาก GT-002 ที่ติด ledger decision (ข้อ 6)
- โค้ดมีอยู่ครบแล้ว: `runtime._checkpoint_exact_target` → `lifecycle.checkpoint` → `store.save_position`
- ผลออกทางไหนก็คุ้ม: ผ่าน = ยกแถว `local_player_position_checkpoint` เป็น `runtime_pass` ได้ทันที
  · ไม่ผ่าน = เจอบั๊ก persistence จริงซึ่งมีค่ากว่าอีก
- GT-006 (พิมพ์แชท) ต่อท้ายได้ในรอบเดียวกัน ราคาถูกที่สุดในคิวและได้ข้อมูลใหม่แน่นอน

---

## หลังจบเทสแล้ว chief จะทำอะไรต่อ

รอบถัดไปของ `pirate-force-chief-continue` จะเห็นผลในคิวแล้ว:

1. อ่านผล → เขียน report → commit state (รวม WIP 187 บรรทัดถ้าคุณเคาะข้อ 8)
2. ถ้า GT-005 PASS → อัปเดต `FUNCTIONAL_COVERAGE.json` แถว `movement` เป็น `runtime_pass`
3. ถ้า GT-006 เจอ frame ใหม่ → chief decode เอง (ห้ามผู้เทส decode)

---

## ยังมี 11 ข้อรอคุณเคาะอยู่

เรียงตามผลกระทบ (chief ประเมิน):

| # | เรื่อง | ทางที่ chief เอนไป | อยู่ในไฟล์ |
|---|---|---|---|
| **11** | จะทำให้คิวเทสเดินอย่างไร | **ข — attended session (ไฟล์นี้)** | `FINDINGS_R15` |
| **6** | M3 เกินเพดาน `HYP-PF-008` — อนุมัติ `ITEM-MOVE-HYP-002` ไหม | ข — อนุมัติมีเงื่อนไข เปิดใช้เมื่อ GT-002 PASS | `FINDINGS_R14` |
| **8** | WIP 187 บรรทัดที่สวีตมองไม่เห็น จะ commit ไหม | ข — commit + แปะ `unverified` ทันที | `FINDINGS_R13` |
| **9** | patch 3 บรรทัดปิดการหลุดตรึง header (2.7×10³⁰ → 2,252,640) | เอา | `FINDINGS_R14` |
| **7** | whitelist 33 `reports/PF_RE_V*.md` เข้า git + `requirements.txt` | — | `FINDINGS_R12` |
| 10 | เพิ่มฟิลด์เชิงกลไกใน ledger schema | — | `FINDINGS_R14` |
| 5 | 5 ไฟล์ media 53.6 MB ใน `evidence\` ที่ไม่มี manifest pin | — | รอบ 10 |
| — | `open_session` ที่เกิดตอน connect (ไม่ใช่หลัง handshake) | — | `FINDINGS_R11` |

**ถ้าจะตอบข้อเดียว → ตอบข้อ 11 (ไฟล์นี้)** เพราะอีก 10 ข้อปลายทางต้องผ่านคิวเทสทั้งหมด
