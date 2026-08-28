# round `B_20260828_1039` (`pnd0a5`) - lane B - COMBAT -- found an earlier, unflagged blocker than gate 2; RE-125 + GT-124 opened

**opened:** 2026-08-28 10:39 (+07:00) - **closed:** 2026-08-28 ~11:1x (+07:00)
**branch:** `claude/friendly-ride-pnd0a5` (pf_bridge only -- no `pirate-force-server` code change this round)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ไม่มีอะไรต่างบนจอวันนี้ -- รอบนี้ไม่มีโค้ดใหม่ มีการค้นพบว่า BUILD-006
มีด่านที่บล็อกอยู่ *ก่อน* ด่าน 2 อีกชั้น (ดูข้อ 5) และมีใบเทส/ใบ RE ใหม่สองใบเตรียมไว้ล่วงหน้า

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
นิ่งตั้งแต่ 09:58) ~~BUILD-006 ฝั่งที่อยู่ในเขตสาย B (`mob_pickup.py`: claim/resolve/commit/log) สร้างเสร็จ
แล้วตั้งแต่รอบ gate-3 -- เหลือ "insert จริง + relog" ที่รอด่าน 2 อย่างเดียว~~ **แก้ตอน commit ที่สองของรอบ
นี้ (agent `pf-queue-author` ตรวจให้): ผิด -- ดูข้อ 5 ด้านล่าง มีด่านอยู่ก่อนด่าน 2 อีกชั้นที่ยังไม่เคยพูดถึง

รันเทสซ้ำเพื่อยืนยันไม่มี regression: `python3 -m unittest tests.test_mob_pickup tests.test_field_mobs
tests.test_mob_death tests.test_item_lifecycle` -- **206 passed**, ไม่มี fail

## 3 รอบนี้ทำอะไร (rule F ข้อ ค): เปิดใบเทสเตรียมล่วงหน้า

สองรอบก่อน (`0942` มีโค้ดจริงแต่ `0953` เป็นแค่แก้เอกสาร/เทส) ไม่มีของใหม่บนจอทั้งคู่ -- รอบนี้เป็นรอบที่
สามติดกัน ตามกฎ F เลือกข้อ (ค): เขียน/ปรับใบเทสในคิว มอบให้ `pf-queue-author` เปิดใบ pre-validate กลไก
pickup claim ใน `GAME_TEST_QUEUE.md` -- ระหว่างค้นข้อมูลให้ agent พบสิ่งที่สำคัญกว่าที่ตั้งใจไว้เดิม (ดูข้อ 5)

## 5 สิ่งที่ agent เจอระหว่างเขียนใบ: มีด่านที่บล็อกอยู่ *ก่อน* ด่าน 2 อีกชั้น ไม่เคยถูกตั้งคำถามมาก่อน

`pf-queue-author` grep `runtime.py` ทั้งไฟล์หา `dispatch_pickup_request`/`PickupClaim`/`commit_pickup` --
**ศูนย์ผลลัพธ์** มีแค่ `BagCellRegistry.claim`/`.release` (คนละกลไกกับการเก็บของ, เป็นการจอง cell ตอน
character-select ตาม CORE-REQUEST-007) ที่ต่อสายจริง ตรวจซ้ำเองแล้วยืนยันตรง: `runtime.py:5143-5147` มี
คอมเมนต์ของตัวเองบอกตรงๆ ว่า "there is no known vital id for a client-originated pickup request on this
project's wire yet ... so there is nothing to dispatch a claim to" -- แปลว่า `mob_pickup.py`'s
claim/resolve/commit/log ที่ unit test ผ่านหมดนั้น **ไม่มีทางถูกเรียกจากคำขอจริงของ client เลยแม้แต่ครั้ง
เดียว** ไม่ใช่แค่ "log แทน insert" ตามที่รอบก่อนๆ (รวมรอบนี้ตอนเริ่ม) เข้าใจ

นี่เป็นด่านที่**อยู่ก่อนด่าน 2** (`is_unmoved_baseline`, เลื่อนไป 30-31 ส.ค.) อีกชั้น: ต่อให้ด่าน 2 ออกแบบ
เสร็จตามกำหนดเป๊ะ ก็ยังเก็บของไม่ได้เพราะไม่มีทางส่งคำขอเข้ามาตั้งแต่แรก -- 50 กว่ารอบที่ผ่านมาของสาย B พูด
ถึงแต่ด่าน 1/2/3 ของกำแพงกระเป๋า ไม่เคยเช็คว่า `runtime.py` มีทางรับคำขอ pickup เข้ามาหรือยัง ไม่ใช่ความผิด
ของรอบไหนโดยเฉพาะ (`THE WALL` ใน `mob_pickup.py` พูดแต่เรื่องด่าน 1/2/3 ของกำแพงกระเป๋า ไม่ได้พูดเรื่องนี้)
แต่เป็นช่องว่างจริงที่ไม่เคยถูกตั้งชื่อมาก่อน

**เปิดใบให้สาย RE**: `RE-125` (`CLIENT_RE_QUEUE.md`) ถาม vital id + payload shape ของคำขอ pickup จริง --
ต้องรู้ก่อนถึงจะเขียน call site ใน `runtime.py` ได้ (เขต chief ไม่ใช่เขตสาย B) `GT-124`
(`GAME_TEST_QUEUE.md`) เปิดคู่กันเป็นใบ pre-validate ที่พร้อมรันทันทีที่ call site ลง แต่ตอนนี้สถานะเป็น
**BLOCKED-ON-WIRING** ไม่ใช่ PENDING (ตัวนับเลขที่ใช้ร่วมกันระหว่างสองไฟล์ทำให้ GT-124/RE-125 ไม่ใช่ GT-123
ตามที่รอบนี้เข้าใจตอนเริ่ม -- ดู numbering note ในทั้งสองใบ)

## 4 เกณฑ์สองชั้น

wire/DB: ไม่มีของใหม่รอบนี้ (206 เทสเดิมผ่านซ้ำ ยืนยันไม่มี regression เท่านั้น) -- การพบ "ไม่มี call site"
เป็น static grep ตรวจซ้ำได้เอง ไม่ใช่การรันเกม
client-observable: ไม่มีของใหม่รอบนี้ -- GT-124 เป็นใบเทสที่**ยังไม่ได้รัน** (และรันไม่ได้จนกว่า RE-125 +
call site ใน `runtime.py` จะลง) ไม่ใช่ผลเทส

## nonclaim

รอบนี้ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`/`scenarios/world_*.json`/
`session.py`/`inventory.py` -- ไม่มีการเปลี่ยน behavior ใดๆ ไม่ได้อ้างว่าด่าน 2 ใกล้เปิดเร็วกว่าที่ COO
กำหนด -- 30-31 ส.ค. ยังเป็นกำหนดเดิม

## write zone

`pf_bridge`: `rounds/B_20260828_1039_...md` (ไฟล์นี้, แก้ไขระหว่างรอบด้วย strikethrough ตามกฎ),
`GAME_TEST_QUEUE.md` (append GT-124 เท่านั้น, ร่างโดย `pf-queue-author`), `CLIENT_RE_QUEUE.md` (append
RE-125 เท่านั้น), `notes_to_chief/20260828_1039_LANE-B-STATUS-...md` (ใหม่, แก้ไขระหว่างรอบเช่นกัน)
`pirate-force-server`: ไม่มีการแก้ไขรอบนี้ (chief's zone -- `runtime.py` call site รอ RE-125 ตอบก่อน)

## CORE-REQUEST

ยังไม่ยื่นรอบนี้ (รอ RE-125 ตอบ vital id ก่อน) -- แจ้งไว้ล่วงหน้าในจดหมายสถานะว่า chief จะได้ CORE-REQUEST
ต่อทันทีที่ RE-125 ปิด เพื่อเขียน call site ใน `runtime.py`

## เปิดใบให้สาย C

none
