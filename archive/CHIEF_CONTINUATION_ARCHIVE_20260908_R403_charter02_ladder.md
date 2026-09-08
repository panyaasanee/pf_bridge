# CHIEF_CONTINUATION.md - CHARTER-02 ladder + P-1/P-2/P-3 block, moved verbatim (R403, 2026-09-08)

Moved by chief round `8bdjhn` on COO-DECISION `20260908_1341` item 2 (trim >=3,000 bytes,
ride the `0206` PR) and because `prompts/CHIEF.md` section 13 says the pass criteria and the
owner of every milestone step live in `pf_bridge/NOW.md` "bandai milestone" ALONE -- so this
copy was a second source of truth for the same ladder, which is the thing that rule forbids.
NOTHING is deleted or reworded: the block below is byte-for-byte what stood in
`CHIEF_CONTINUATION.md` lines 10-43 before this commit.

---

### CHARTER-02 — บันไดไมล์สโตน (คอลัมน์ "กำหนด" ถูกลบตาม `0243` ข้อ 2 · กฎสี่ข้อของเวอร์ชัน + วินัยหลักฐานคงเดิม)

- ✅ **M1/v1** เมืองมีชีวิต — ประกาศแล้ว (R249)
- ⏳ **M2/v2** ออกจากเมืองได้ — เหลือเกณฑ์เดียว: แล่นเรือชนเกาะ → หน้า "รายงานกัปตัน เรือเทียบท่า [ชื่อเกาะ]"
  เด้งเอง (ไม่ต้องคลิก · `PANYA-INFO 20260904_0409`) → ผู้เล่นกดยืนยัน → วาปเข้าเกาะ 2 (Prison Exile) และเกาะ 3
  (Spice Paradise) ได้จริงบนจอ **ทั้งสองเกาะ** → **LANE-A**
  🔴 **แก้ถ้อยคำโดย chief รอบ `3kwnnr`/R332 ตาม `COO-DECISION 20260904_0344` ข้อ 2** — ~~"ใกล้เกาะ client ยิง
  `TriggerVital` (`0x1FB2`) → server ตอบ"~~ **ถอน หักล้างแล้ว**: `0x1FB2` id 40/51/3/57/36 = trigger prop
  กลางทะเล (Seafood Cargo/Offer Altar/…) ไม่ใช่ทางเข้าเกาะ (`LANE-A 20260904_0300` จาก
  `TEXTDATA_TH__Trigger_TIP.tsv`) · **อะไรเปิดหน้ารายงานกัปตันยังไม่รู้ = ใบ RE ของ LANE-A** (ร่างรอบ 04:21 ·
  chief ตั้งเลขในรอบที่ใบถึง ตาม `0344` ข้อ 3) · ห้ามใบเทสใบไหนถือ `0x1FB2` เป็นฐานของ "เทียบท่า" อีก
- **M3** สนามมีมอนสเตอร์ (= P-2 ยกระดับ): สีชื่อมอนถูกตามสถานะ **และ** attr + relation/faction ของมอนถูกจริง
  ไม่ใช่แค่ทาสี → LANE-GM (สี) ร่วม LANE-B (attr/relation ของ roster)
- **M4** ตีได้ตายได้ — สี่ข้อครบบนจอ: (1) มอนตีกลับ HP ผู้เล่นลดจริง (2) ตายถูกต้อง ท่าตาย/ชื่อเทา/ไม่มี
  ข้อความ-ตัวนับของผู้เล่น (3) ศพไม่แข็งค้าง (4) เกิดใหม่ได้ (`GT-224`) → LANE-B
- **M5** เก็บของได้ (คงเดิม) — เก็บได้ + รอด relog · หนี้: ของผี 120 วิ · หาง P-1 · ไอคอน/ใช้ของ → LANE-B
- **M final** (ไม่มีเลข แทน M6) — เกมเล่นได้ครบวงจร เกิด-เดินทาง-สู้-เก็บ-โต-กลับมา

- **P-1** ของดรอปต้องอยู่บนพื้นนานพอให้เดินไปเก็บทัน → **LANE-B** (ตัวหลักติ๊กแล้ว · หางค้าง: กะพริบหลัง
  `#689` + หนี้ `DropLedgerCell` = `GT-225`)
- **P-2** สีชื่อมอนต้องถูกสถานะ: ปกติ=ส้ม / สู้=แดง / ตาย=เทา (ห้ามชมพู) → **LANE-GM** ร่วม LANE-B (attr/relation)
  — เกณฑ์ผ่าน M3 ตั้งแต่ `0233`
- **P-3** ทุกปุ่ม/ทุกฟังก์ชันใน GMUI ทั้ง 3 หน้าต้องทำงานจริงครบทุกตัว → **LANE-GM**
- 🆕 UI-A/UI-B (ปุ่มกลับหน้าเลือกตัวละคร/logout) **ย้ายเจ้าของจาก LANE-A ไป LANE-UI** ตาม
  `notes_to_chief/20260904_0330_COO-DECISION-*.md` — ดูหัวข้อ "ทีมและเขตเขียน — สายที่ 6/7" ด้านล่าง
- 🆕 GM-B `/speed` เจ้าของ **LANE-DB** (`COO-DECISION/ORDER 20260901_1059/1100/1101`)
- `GT-146`/ใบตีมอนทั้งหมด **ห้ามเข้าคิว attended** จนกว่า P-2 จะปิด (P-1 ผ่านจอแล้ว)
- **"ตัวละคร" (class/สแตท/HP จากตาราง class)** ไม่เปิดเลนใหม่ (`0243` ข้อ 3) — แถว typed HP/เลเวล = LANE-DB ·
  `class_id` NULL = chief (`GT-215`) · ค่าเริ่มต้น HP/สแตทจากตาราง class = chief ออก CORE-REQUEST ให้ LANE-DB
  เมื่อ `GT-215` ปิด — M4 ข้อ (1) ต้องมีแถวนี้ก่อน

`SERVER_VERSIONS.md` (ที่รากรีโปเซิร์ฟเวอร์) ตารางแผน v2-v-final: ลบคอลัมน์วันที่ตามเดียวกัน — งานถัดไปของ chief
(ยังไม่ลงรอบนี้ เพื่อคุมขนาด PR ให้อยู่หนึ่งเรื่องต่อใบ)

