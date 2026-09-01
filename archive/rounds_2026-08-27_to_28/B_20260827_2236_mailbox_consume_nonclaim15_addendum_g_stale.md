[LANE-B (COMBAT) · round `wcpm2h` · 2026-08-27T22:36+07:00]

# 0 ล็อกรอบ

ต้นรอบ: PR ล่าสุดของ [LANE-B] ทั้งสอง repo (`pf_bridge#240`, `pirate-force-server#151`, รอบ
`k25cur`) `merged=true` จริง (ยืนยันด้วย `pull_request_read get` เต็ม ไม่ใช่แค่ field `merged` จาก
`list_pull_requests` ที่ addendum v2 เตือนไว้ว่าไม่น่าเชื่อถือ -- ของจริงคือ `merged_at`/`merged_by`
มีค่า) -- งานรอบก่อนอยู่บน `main` แล้วทั้งคู่ ไม่ต้อง cherry-pick อะไร ไม่มี [LANE-B] PR เปิดค้างตอนต้น
รอบ (`list_pull_requests state=open` ว่างทั้งสอง repo) -- เปิด draft PR ยึดล็อกก่อนแตะไฟล์
(`pf_bridge#243`, `pirate-force-server#152`) ตามกฎ

# 1 กล่องจดหมาย (ขั้นที่สองของทุกรอบ)

Backlog รอบแรกที่อ่าน v2 ของสาย B ตามที่ addendum ระบุ: `RE-098` -- ตรวจแล้วพบว่า **บริโภคไปแล้วจริง**
ตั้งแต่รอบ `20260827_1549` (BUILD-004 field-mobs verification) มี stub `.CONSUMED.txt` ทั้งที่ root และ
`consumed/` ครบ ไม่ต้องทำซ้ำ

กวาดกล่องจดหมายทั้งกล่องหาใบที่ยังไม่มี stub (`ls notes_to_chief/*.md` ที่ไม่มี `.CONSUMED.txt` คู่กัน)
เจอหนึ่งใบที่เป็นของสาย B จริง (คำตอบต่อคำถามที่สาย B เปิดเอง ไม่ใช่ status letter ของสาย B เอง):

`20260827_1550_CHIEF-REPLY-LANE-B-CORE-REQUEST-015-nonclaim15-answer.md` -- ตอบ NONCLAIM 15
(ใครยืนยัน `claimant_identity == self.foundation.selected.actor_identity`, `runtime.py` หรือ
`mob_pickup.py`) chief ตอบ: `runtime.py` เป็นคนเช็ค ไม่ใช่ `mob_pickup.py` เพิ่ม defense-in-depth เอง

ตรวจแล้วพบว่าคำตอบนี้ **ถูกพับเข้า `CHIEF_CONTINUATION.md` แถว `015` ไปแล้วโดย chief เองตอนตอบ**
(อ้างอิงคำตอบเดียวกันคำต่อคำ) จึงไม่มีอะไรให้ "เอาไปใช้" เพิ่มในโค้ด -- `mob_pickup.py` ยังมี 0 จุดเรียก
จริง (`grep -rn "dispatch_pickup_request(" src/ app.py 2>/dev/null` = ว่าง นอก `mob_pickup.py`/เทสตัวเอง)
เพราะยังรอ RE opcode decoder (`GT-060`) เหมือนเดิม ไม่มี call site ให้ apply เช็คนี้ได้จริงในวันนี้ --
เขียน stub ปิดใบ (`notes_to_chief/20260827_1550_..._nonclaim15-answer.md.CONSUMED.txt` + สำเนาไป
`consumed/`) บันทึกว่าเก็บคำตอบไว้ใช้ตอนมี call site จริง

ใบอื่นที่ไม่มี stub ในกล่องล้วนเป็น (ก) จดหมายที่สาย B เขียนเอง (STATUS/ASK-COO/REPLY -- ไม่ต้องมี stub
ปิดตัวเอง) (ข) `FROM_CHIEF_R19x` broadcast ถึงทุกสาย ไม่ใช่ RE-*/GT-*/COO-DECISION/CORE-REQUEST-reply
เฉพาะเจาะจงถึงสาย B (ค) จดหมายเก่าก่อนกฎ stub มีผล (26 ส.ค.) -- ไม่อยู่ใน backlog ที่ addendum ระบุชื่อ
ไว้ ไม่ขยายขอบเขตไปจัดการเอง

# 2 ตรวจ Addendum v2 ข้อ G (world-wipe fix, สาย B เท่านั้น) -- **เก่าไปแล้ว ไม่ใช่ของค้าง**

ข้อ G สั่งให้สาย B แก้ `runtime.py:3828-3835` (`bar_frames`/`death_frames` ต้อง compose census เหมือน
arrival) เป็นครั้งเดียวก่อน `lane_hooks` ลง main แล้วพิสูจน์ headless + เขียนบรรทัด "พร้อมสำหรับ
GT-084-R2" ใน `GAME_TEST_QUEUE.md`

ตรวจโค้ดจริงที่บรรทัด 3828-3835 ของ `pirate-force-server/src/pirateforce_foundation/runtime.py` วันนี้:
เป็นโค้ด `mob_combat_ledger_stale_retry_limit_exceeded_no_reply` (คนละเรื่องกับ census compose เลย --
เลขบรรทัดขยับไปแล้วเพราะไฟล์โตขึ้นหลายรอบตั้งแต่ addendum ถูกเขียน)

การแก้ census compose ของ `bar_frames`/`death_frames` **ทำไปแล้วจริงตั้งแต่ R188** (`CORE-REQUEST-008`,
`pirate-force-server@741ab5d`) -- token คอนโซล `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` /
`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE` มีอยู่จริง มี fail-closed guard ที่ pf-adversary จับได้ในรอบนั้น
(ดู `rounds/R188_*.md`, แถว `CHIEF_CONTINUATION.md` บรรทัด 3619 ของ `GAME_TEST_QUEUE.md`)

หนักกว่านั้น: **GT-084-R2 ที่ข้อ G บอกให้ "เตรียมพร้อมสำหรับ" นั้นวิ่งไปแล้วจริงตั้งแต่วันนี้บ่าย** --
ผลอยู่ที่ `notes_to_chief/20260827_1620_GT084R2-RESULT-*.md` และปักหัวใบ `GT-084` ใน
`GAME_TEST_QUEUE.md` แล้ว (wire/DB ครบ hit x5 → HP 0 → MOB-DEATH-001 kill → dying/dead frames →
loot drop x2 ผ่านหมด, client-observable FAIL 2 จุดที่ปิดเป็น bounded negative แล้วผ่าน RE-107/RE-108 --
คนละเรื่องกับ census compose ที่ข้อ G ถาม) หลักฐาน headless ที่ข้อ G ขอเป็นแค่ proxy ของสิ่งที่ attended
session จริงให้คำตอบที่ดีกว่าไปแล้ว -- เขียนบรรทัด "พร้อมสำหรับ GT-084-R2" ตอนนี้จะเป็นการเขียนสิ่งที่
เกิดไปแล้วให้ดูเหมือนยังไม่เกิด จึงไม่เขียน

**สรุป: ข้อ G ของ addendum v2 อ้างอิงสถานะที่ COO/เจ้าของยังไม่รู้ว่าปิดไปแล้ว -- ไม่ใช่งานค้างของสาย B
จริง** แจ้งใน STATUS letter คู่กันเพื่อไม่ให้รอบถัดไปเสียเวลาไล่บรรทัด 3828-3835 ซ้ำ

# 3 พื้นผิวที่สร้างได้จริงรอบนี้

ไม่มี code diff ใหม่ใน `src/pirateforce_foundation/` รอบนี้ -- ตรวจตามลำดับเหตุผลของรอบก่อน
(`rounds/B_20260827_2153_*.md` ข้อ 9 "รอบถัดไปควรทำอะไร") ครบทั้งสามข้อ:

1. จดหมาย ASK-COO ของรอบ `k25cur` (`actor_identity` ต้องการมิติ scene) -- **ยังไม่มี COO-DECISION
   ตอบ** (กวาด `notes_to_chief/*COO-DECISION*` และ `*CHIEF-REPLY*` ทั้งหมดหลัง `2153` แล้ว ไม่เจอ) ยัง
   รอเหมือนเดิม
2. `CORE-REQUEST-021` (bg0002 login) ต่อสายแล้วจริง (`CHIEF-REPLY 2200`) แต่ยังเป็น "dead code จนกว่า
   จะ seed" และ M2 (ข้าม scene ในเซสชันเดียว) ยังพักตาม `PANYA-DECISION 2010` -- ยังไม่มีบั๊กที่เห็นจริง
   ตามที่รอบก่อนวิเคราะห์ไว้ ไม่ต้องยกจดหมายข้อ 7 ขึ้นมา
3. `BUILD-006` ยังรอ RE opcode decoder (`GT-060`) เหมือนเดิม ไม่มี pure-function เพิ่มให้สร้างได้จริง

ตรวจ `mob_aggro.py`/`mob_combat.py`/`mob_death.py`/`field_mobs.py`/`mob_pickup.py` ทั้งห้าไฟล์อีกรอบ
(`production_allowed = True` ทุกไฟล์ ไม่มีแฟล็ก) ไม่มีจุดใดที่มี TODO/nonclaim เปิดค้างที่แก้ได้เองโดยไม่
ต้องพึ่งอีกสายหรืออีกใบ

# 4 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | ไม่มีโค้ดเปลี่ยน -- ไม่มีอะไรให้เทส สวีตเต็มไม่จำเป็นต้องรันซ้ำ (ไม่แตะไฟล์ `.py` เลย) |
| **client-observable** | ไม่มี -- ไม่ใช่รอบ attended |

# 5 pf-adversary

ไม่มี code diff ให้ตรวจ (เอกสาร/mailbox stub ล้วน) -- ข้ามตามกฎเดิม (เกทนี้มีไว้ตรวจโค้ดก่อน commit ไม่ใช่
บังคับทุกรอบที่ไม่มีโค้ด)

# 6 จดหมาย

`notes_to_chief/20260827_2236_LANE-B-STATUS-nonclaim15-consumed-addendum-g-stale-no-new-surface.md`

# 7 ถ้าผิดต้องย้อนอะไรบ้าง

ย้อนได้ด้วยการลบสอง stub file + คืนไฟล์จดหมาย `1550` กลับที่เดิม (ไม่มีอะไรอื่นเปลี่ยน)

# 8 รอบถัดไปควรทำอะไร

เหมือนเดิมทั้งสามข้อจากรอบก่อน (ยังไม่ปลดล็อกสักข้อ) -- เช็คซ้ำทุกรอบ: (1) COO-DECISION ตอบจดหมาย
`2153` แล้วหรือยัง (2) M2 ปลดพักหรือยัง ถ้าปลดให้ยกจดหมาย `2153` ข้อ 7 ขึ้นมาอ่านก่อนเดินสาย (3)
`GT-060` (RE opcode decoder) ปิดหรือยัง ถ้าปิดแล้วเปิดทางให้ chief ต่อสาย `mob_pickup.dispatch_pickup_request`
เข้า `runtime.py` ตาม nonclaim 15 ที่ตอบไว้แล้ว

-- **สาย B · COMBAT**
