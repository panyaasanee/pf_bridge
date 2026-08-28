# round `B_20260828_1039` (`pnd0a5`) - lane B - COMBAT -- gate 2 not due, pre-validation ticket opened

**opened:** 2026-08-28 10:39 (+07:00) - **closed:** 2026-08-28 ~10:5x (+07:00)
**branch:** `claude/friendly-ride-pnd0a5` (pf_bridge only -- no `pirate-force-server` code change this round)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ไม่มีอะไรต่างบนจอวันนี้ -- รอบนี้ไม่มีโค้ดใหม่ มีแค่ใบเทสใหม่หนึ่งใบ
เตรียมไว้ล่วงหน้าสำหรับตอนที่ด่าน 2 เปิด

## 0 ต้นรอบ: ตรวจล็อกรอบก่อนตามข้อ A ของ addendum v2

`pf_bridge#295` (`merged=true`, ยืนยันด้วย `git merge-base --is-ancestor` บน `origin/main` สด) และ
`pirate-force-server#192` (`merged=true`, ยืนยันเช่นกัน) ทั้งคู่อยู่บน `main` แล้ว -- ไม่ต้อง cherry-pick กู้
อะไร ไปต่อได้ตามปกติ

## 1 กล่องจดหมาย (ข้อ B): ไม่มีใบที่ต้องบริโภครอบนี้

ไล่ทุกใบใหม่ตั้งแต่ `0953` ถึง `0955` แล้ว -- ใบเดียวที่มาใหม่คือ `0955_KA1B-EVIDENCE-...` ซึ่ง
`[ถึง: chief, COO · cc สาย A, B, GM, ...]` ไม่ใช่ `ADDRESSEE: LANE-B` โดยตรงและไม่ตอบใบไหนที่สาย B เปิด
(เป็นเรื่อง nameboard/character-name ของสาย A/chief) -- ไม่ consume รอบนี้ ไม่มี RE-098 residual จาก
addendum v2 (ปิดไปแล้วตั้งแต่ PR #211, 2026-08-27)

## 2 เช็ค BUILD-004/005/006: ยังไม่มีอะไรใหม่ให้สร้างในเขตตัวเอง

อ่าน `notes_to_chief/20260827_1350_COO-DECISION-bagwall-second-wall-redesign-deferred-post-M4.md` ซ้ำ
เพื่อยืนยันวันที่: COO กำหนดให้ออกแบบด่าน 2 ใหม่ (แยก "ดริฟต์เกมเพลย์จริง" จาก "hypothesis state ที่ยัง
ไม่ opt-in") **ต้นสัปดาห์ M5 (30-31 ส.ค.)** -- วันนี้ 28 ส.ค. ยังไม่ถึงกำหนด ไม่ใช่ค้างเพราะไม่มีคนทำ แต่
เป็นตารางที่ COO วางไว้เอง 3 วันก่อน สาย B ไม่มีเหตุผลใหม่จะขอทำเร็วขึ้น (ไม่มีข้อมูลใหม่ตั้งแต่รอบ `3iq8jk`
ที่จะเปลี่ยนคำตัดสินนั้น) -- **ไม่ยื่นขอสิทธิ์แก้ `session.py`/`inventory.py` รอบนี้**

BUILD-004 (มอนสเตอร์จริงจากตาราง MOBS) และ BUILD-005 (ตี/ตาย) reverified ล่าสุดในรอบ `3iq8jk`
(pf_bridge#292/295, pirate-force-server#189/192) -- ไม่มีอะไรเปลี่ยนตั้งแต่นั้น (`git log` ของทั้งสอง repo
นิ่งตั้งแต่ 09:58) BUILD-006 ฝั่งที่อยู่ในเขตสาย B (`mob_pickup.py`: claim/resolve/commit/log) สร้างเสร็จแล้ว
ตั้งแต่รอบ gate-3 -- เหลือ "insert จริง + relog" ที่รอด่าน 2 อย่างเดียว ตรงกับที่ `THE WALL` ใน
`mob_pickup.py`'s module docstring บันทึกไว้

รันเทสซ้ำเพื่อยืนยันไม่มี regression: `python3 -m unittest tests.test_mob_pickup tests.test_field_mobs
tests.test_mob_death tests.test_item_lifecycle` -- **206 passed**, ไม่มี fail

## 3 รอบนี้ทำอะไร (rule F ข้อ ค): เปิดใบเทสเตรียมล่วงหน้า

สองรอบก่อน (`0942` มีโค้ดจริงแต่ `0953` เป็นแค่แก้เอกสาร/เทส) ไม่มีของใหม่บนจอทั้งคู่ -- รอบนี้เป็นรอบที่
สามติดกัน ตามกฎ F เลือกข้อ (ค): เขียน/ปรับใบเทสในคิว มอบให้ `pf-queue-author` เปิด **GT-123** ใน
`GAME_TEST_QUEUE.md` เพื่อ pre-validate กลไก pickup claim (resolve/commit/log-only) ที่สร้างเสร็จแล้ว
วันนี้ ก่อนด่าน 2 จะเปิดจริงวันที่ 30-31 -- เป้าหมาย: พอด่าน 2 เปิด ไม่ต้องเสียเวลาคิดวิธีเทสใหม่ มีใบพร้อม
รันทันที **ใบนี้กำลังเขียนโดย agent แยก ยังไม่จบตอน commit นี้ -- จะตามมาเป็น commit ที่สองในรอบเดียวกัน
ก่อนเอา draft ออกจาก PR** (รายละเอียด: ดู commit ถัดไปหรือ `GAME_TEST_QUEUE.md` GT-123 โดยตรง)

## 4 เกณฑ์สองชั้น

wire/DB: ไม่มีของใหม่รอบนี้ (206 เทสเดิมผ่านซ้ำ ยืนยันไม่มี regression เท่านั้น)
client-observable: ไม่มีของใหม่รอบนี้ -- GT-123 เป็นใบเทสที่**ยังไม่ได้รัน** ไม่ใช่ผลเทส

## nonclaim

รอบนี้ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`/`scenarios/world_*.json`/
`session.py`/`inventory.py` -- ไม่มีการเปลี่ยน behavior ใดๆ ไม่ได้อ้างว่าด่าน 2 ใกล้เปิดเร็วกว่าที่ COO
กำหนด -- 30-31 ส.ค. ยังเป็นกำหนดเดิม

## write zone

`pf_bridge`: `rounds/B_20260828_1039_...md` (ไฟล์นี้), `GAME_TEST_QUEUE.md` (append GT-123 เท่านั้น,
โดย `pf-queue-author`), `notes_to_chief/20260828_1039_LANE-B-STATUS-...md` (ใหม่)
`pirate-force-server`: ไม่มีการแก้ไขรอบนี้

## CORE-REQUEST

none

## เปิดใบให้สาย C

none
