# GAME_TEST_QUEUE archive — closed-item stubs + GT-001 biground #3 result details
# ย้ายมาโดย chief รอบ 97 (2026-08-20 07:3x) เพราะคิวชนเพดาน ~60KB
# เนื้อหาคัดลอกมาตรงตัว ไม่ตัดทอน — pointer อยู่ในคิวหลัก

## ก้อน 1: stub รายการที่ปิดแล้ว (GT-011 / 015+017 / 018-020 / 021 / 022 / 023-025)

## GT-011 HYP-PF-015 v2 delete ack — ⤴ ย้ายไป archive แล้ว (รอบ 81)  [🟡 ปิดในทางโครงสร้าง]

> ผลเต็ม + เหตุผลปิดอยู่ที่ `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260819_GT011.md`
> และ `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260819_R85_HOUSEKEEPING.md` (chief รอบ 85)
> · สรุปสั้น: ปิดโดยโครงสร้าง ไม่ใช่เพราะส่งผิด · **ผู้สืบทอด = GT-018** (PASS แล้ว)

---

## GT-015 + GT-017 — ✅ **PASS ทั้งคู่ (รอบใหญ่ #6) ย้ายไป archive แล้ว (รอบ 90)**

⤴ `archive\GAME_TEST_QUEUE_ARCHIVE_20260819_R90_GT015_GT017.md` (เนื้อหาเต็ม ไม่ตัดทอน)
· **GT-015** HYP-PF-017 ลากไอเทมทับ slot ที่มีของ → สลับตำแหน่งจริงบนจอ + client ยิง `op=4` tuple เดิม
· **GT-017** STATS-PROG-001 หลอด XP / `LV.1 → LV.7` ขยับจริงทั้ง 9 เฟรม (1 ข้อ "ไม่ยืนยัน" = persistence ซึ่งยังไม่มี write path)
· ผลถูกบริโภคโดย chief รอบ 89 แล้ว — ไม่มีงานค้างจากสองรายการนี้

## GT-018 / GT-019 / GT-020 — ✅ **PASS ทั้งสาม ย้ายไป archive แล้ว (รอบใหญ่ #4-#5)**

⤴ `archive\GAME_TEST_QUEUE_ARCHIVE_20260819_GT018_GT019_GT020.md`
· GT-018 delete-refresh · GT-019 HP=0 ตายบนจอ (ผู้สืบทอด **GT-021**) · GT-020 login บัญชีอื่น


## GT-022 — ✅ PASS แบบมีเงื่อนไข (รอบใหญ่ #7, consumed รอบ 91) — ⤴ ย้ายไป archive แล้ว (รอบ 96)
> เนื้อหาเต็ม: `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R96_GT022_GT023_024_025.md`
## GT-021 HP-DEATH-003 `dying_hold` — 🟡 **PARTIAL (รอบใหญ่ #6) ย้ายไป archive แล้ว (รอบ 90)**

⤴ `archive\GAME_TEST_QUEUE_ARCHIVE_20260819_R90_GT021.md` (เนื้อหาเต็ม ไม่ตัดทอน)
· **ผลลบที่มีค่าที่สุดของสัปดาห์:** ตัวละครลงไปร่อแร่จริง แต่ **client ไม่ลดตัวนับเอง** ค้างเกิน 4 นาที
· chief รอบ 89 บริโภคผลนี้ไปเป็น **DEATH-ESCALATE-001** (เฟรมที่สี่ `timer = 0.0`) ⇒ ผู้สืบทอดคือ **GT-023** ด้านล่าง
· ไม่มีงานค้างจากรายการนี้ — ถ้าจะเทสซ้ำ ให้รัน GT-023 แทน

## GT-023 / GT-024 / GT-025 — ✅ รันจบทั้งสาม (รอบใหญ่ #8, consumed รอบ 93) — ⤴ ย้ายไป archive แล้ว (รอบ 96)
> เนื้อหาเต็ม: `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R96_GT022_GT023_024_025.md` · สรุปปิด GT-024/027/028 ยังอยู่ในคิวด้านล่าง

## ก้อน 2: GT-001 — รายละเอียดผล PASS รอบใหญ่ #3 (17:4x jobs 072/073)

> ✅ **RESULT รอบใหญ่ #3 (17:4x, jobs 072/073) — PASS ทุกเกณฑ์ที่ `f286945` · ผลเต็ม: `pf_bridge\notes_to_chief\consumed\20260818_1745_biground3-results.md`**
> - client-observable: full loop ครบ (HP 100/100 · minimap · Port Royal · chat online) · **เกิดที่ `X:-8,094 Y:-3,207` = ค่า persist จากรอบก่อนเป๊ะ** · เดินได้ · ออกสะอาด X+ยืนยัน
> - wire/DB: stopped ×1 · stderr 0B · listeners 0 · **sessions 6→7** · lease 6→7 · open 0 · backpack `[1@0,2@1,4@3]` ไม่เปลี่ยน · integrity ok
> - **position ถูกเขียนใหม่ตามที่เดิน** → `(-8553.947, -2579.689, 186.0, h=4.532)` @ 10:38:40Z = **persistence ทำงานอีกครั้ง** (ของแถมจาก GT-014)
> - 🔴 **canonical sha ใหม่ = `159F40EF758D567503828F0381F088247743E9663C13C692854C950F1F32DBC6`** (เดิม `B5557E9F..C9ED`)

## ก้อน 3: pointer เก่า GT-002/003/005/006 + โน้ตรอบ 82

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** GT-002 M4 free-slot runtime [PASS — processed `b1087bb`] → `pf_bridge/archive/GAME_TEST_QUEUE_ARCHIVE_20260817.md`

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** GT-003 concurrent_multi_client [CLOSED — known_limitation] → `pf_bridge/archive/GAME_TEST_QUEUE_ARCHIVE_20260817.md`

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** GT-005 position persistence [PASS — processed] → `pf_bridge/archive/GAME_TEST_QUEUE_ARCHIVE_20260817.md`

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** GT-006 chat input observation [DONE — observation ครบ → นำไปสู่สาย chat 0xAC52] → `pf_bridge/archive/GAME_TEST_QUEUE_ARCHIVE_20260817.md`

---

> 🛈 **รอบ 82 (chief, commit `11fea4f`) — ไม่มีรายการเทสใหม่ และนั่นถูกต้อง**
> รอบนี้เป็นงาน infrastructure ล้วน (CORPUS-PIN-001: เลิกใช้ glob ตัดสินว่าไฟล์ไหนคือหลักฐาน)
> ไม่แตะ `src/` ไม่เปิด hypothesis ไม่มีอะไรที่ผู้เล่นเห็นในเกม ⇒ **ไม่มีอะไรให้เทสด้วย UI**
> **ของพร้อมรันรอบใหญ่ยังเป็น 5 รายการเดิม: GT-015 · GT-017 · GT-018 · GT-019 · GT-020**
> ⚠️ หมายเหตุถึงผู้เทส: รอบนี้ไม่แตะ `src/` เลย ⇒ **hash ที่ระบุไว้ในแต่ละ GT ยังใช้ได้ ไม่ต้องตั้ง PENDING ใหม่**

---

