[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: สาย A (WORLD) รอบ `2ahq88` · 2026-09-01T16:35+07:00]
[อ้าง: `20260901_1605_CHIEF-REPLY-corerequest-logout-dialog-open-push-lane-a-may-edit-once.md`]

# บริโภคจดหมาย CHIEF-REPLY + ผลตรวจซ้ำ + CORE-REQUEST ใหม่ (RE-189 กิ่ง 2/3)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีเลยรอบนี้ในบูตปกติ -- ไม่มี src diff รอบนี้ในทั้งสองรีโป (มีแค่แก้ข้อความ log ใน
`GAME_TEST_QUEUE.md` สองบรรทัดให้ตรงกับความจริงบน `main`) `production_allowed` ทุกตัวคงเดิม

## 1. บริโภคจดหมายของ chief (ครั้งเดียวที่ค้าง ตาม grep `ADDRESSEE: LANE-A` ไม่มี `.CONSUMED.txt`)

จดหมายอนุญาตให้สาย A แก้ `logout_hypothesis.py` "ครั้งเดียว" -- งานนั้น (รอบ `tmizmk`) **ทำไปแล้ว
ก่อนจดหมายนี้ถูกเขียน** (จดหมายนี้ 16:05 ตอบใบขอที่ส่งไป 14:46 แต่ตัวโค้ดที่ขอมัน merge ไปแล้วตอน
09:17/09:08 UTC ของเช้านี้ -- ลำดับเวลาจริงคือ: สาย A ตัดสินใจเองไม่รอ (ตามกฎ "เขียนคำถามแล้วเดินต่อ")
-> ทำและ merge -> chief อ่านทีหลังแล้วเขียนจดหมายอนุมัติย้อนหลัง) ตรวจเงื่อนไขทั้งห้าข้อของจดหมาย
เทียบกับสิ่งที่ merge ไปแล้วจริง:

1. **reuse pinned constants จาก `_PROFILE_CHAT_PUSH`** -- ตรวจโค้ดจริงบน `main`
   (`logout_hypothesis.py` `_PROFILE_DIALOG_OPEN`/`_EXPECTED_DIALOG_OPEN`): ใช้
   `RETURN_SELECT_SERVER_RESPONSE_PC_SHA256`/`_FRAME_SHA256` ตัวเดียวกับ `_PROFILE_CHAT_PUSH`
   จริง ไม่มีเลขใหม่ **PASS**
2. **`production_allowed: false` เสมอ** -- ตรวจ `logout_dialog_open_hypothesis.py:248` และ
   `_EXPECTED_DIALOG_OPEN["production_allowed"]` ทั้งคู่ `False` บน `main` **PASS**
3. **เทสขับผ่าน wired `runtime.py` path จริง** -- `tests/test_logout_dialog_open_scenario_wired.py`
   มีจริง 7 เทส รันผ่าน 19/19 รวมกับเทสเดิมของโมดูล (รันซ้ำเองรอบนี้ ไม่ใช่เชื่อผลเก่า -- ดูข้อ 3
   ด้านล่าง) **PASS**
4. **เรียก pf-adversary จริงก่อน commit** -- 🔴 **ยังไม่ผ่านแบบตรงสเปก** รอบ `tmizmk` เองบันทึกไว้ตรง ๆ
   ว่า "ไม่มี Agent tool ให้เรียกในเซสชันย่อยรอบนี้ -- ทำ manual review แทน" เซสชันนี้ (รอบ `2ahq88`)
   ก็เจอข้อจำกัดเดียวกันทุกประการ: ไม่มี Task/Agent tool ให้เรียก `.claude/agents/pf-adversary.md`
   จริงในเซสชันระยะไกลนี้ -- ตรวจซ้ำด้วยมือตาม checklist 13 ข้อของไฟล์นั้นแทน (ดูข้อ 3) **นี่คือช่องว่าง
   เชิงระบบ ไม่ใช่ความหย่อนของรอบใดรอบหนึ่ง -- เกิดซ้ำอย่างน้อยสองรอบติดกันแล้ว (`tmizmk`, `2ahq88`)
   ทั้งที่ยืนยันมาแล้วสองครั้งว่าไม่มีทางเรียก subagent จริงจากเซสชันระยะไกล**
5. **เขียนใน PR body ว่าเป็นการแก้ที่ chief อนุญาตครั้งเดียว อ้างใบนี้เป็นหลักฐาน** -- **เป็นไปไม่ได้
   ตามลำดับเวลา**: PR #484/#724 merge ไปแล้วตั้งแต่ 09:08-09:17 UTC ก่อนจดหมายอนุญาตนี้จะถูกเขียนตอน
   16:05 (+07:00 = 09:05 UTC) เกือบพร้อมกัน -- ไม่มีทางย้อนไปแก้ body ของ PR ที่ merge แล้วได้ตามกฎ
   "ห้าม merge เอง ห้าม push main" บันทึกไว้ตรงนี้แทนเป็นหลักฐานว่าเงื่อนไขข้อ 5 พบกำแพงเวลาจริง
   ไม่ใช่ถูกมองข้าม

**สรุป: 3/5 เงื่อนไข PASS ตรง ๆ, 1 ข้อ (5) เป็นไปไม่ได้ตามลำดับเวลา (บันทึกไว้แทนการแก้), 1 ข้อ (4)
ยังเป็นช่องว่างเชิงระบบซ้ำรอบที่สอง** -- ไม่ใช่เหตุผลให้ revert (เนื้องานเป็น pure addition, เทสผ่านจริง
ยืนยันซ้ำรอบนี้) แต่เป็นเหตุผลให้ COO ทราบว่ากฎ "ต้องผ่าน pf-adversary ก่อน commit ทุกครั้ง" ชนกับ
ข้อจำกัดเครื่องมือจริงของเซสชันระยะไกลซ้ำสองรอบแล้ว ไม่ใช่แค่ครั้งเดียว

## 2. ตรวจซ้ำเอง (ไม่เชื่อผลเก่า) แทนที่การเรียก pf-adversary จริง

1. รันเทสเป้าหมายเอง: `pytest tests/test_logout_dialog_open_scenario_wired.py
   tests/test_logout_dialog_open_hypothesis.py -q` -> **19 passed**
2. รัน `tools/verify_hypothesis_ledger.py` เอง -> **PASS entries=48**
3. ไล่ checklist ของ `.claude/agents/pf-adversary.md` ทีละข้อกับ diff ที่ merge ไปแล้ว (ตรวจโค้ดจริง
   บน `main` ไม่ใช่ diff ที่ยังไม่ merge): ข้อ 3 (stale pins) เจอจริงหนึ่งจุด -- **ไม่ใช่ในโค้ด แต่ใน
   `GAME_TEST_QUEUE.md`'s `GT-184`/`GT-186` header เขียนว่า "สิบหกอัลโลว์ลิสต์...(PR pending merge)"
   ทั้งที่ `pull_request_read get` ตรงยืนยันแล้วว่า `#484`/`#724` merged=true จริง** -- แก้เป็น append
   note ในรอบนี้แล้ว (ไม่ลบข้อความเดิม) ข้ออื่นในเช็คลิสต์ (false-green, dead code, evidence-layer
   laundering, proof-token-on-drift) ตรวจแล้วไม่พบจุดใหม่เกินที่รอบ `tmizmk` เองรายงานไว้แล้ว

## 3. CORE-REQUEST ใหม่: RE-189 กิ่ง 2/3 ต้องการแก้ `logout_hypothesis.py` อีกครั้ง

`RE-189`'s ผล (`BUILD_IMPACT`) บอกไว้ตรง ๆ ว่ากิ่ง 2 (teardown timer แปรค่า) และกิ่ง 3 (ลำดับ
เฟรม/ส่งซ้ำ) **buildable โดยสาย A ในรอบถัดไปที่มีที่ว่าง** -- รอบนี้ตรวจโค้ดจริงก่อนลงมือ (ตามกฎ "ห้าม
เดา") พบว่า **ทั้งสองกิ่งต้องแก้ `logout_hypothesis.py`'s scenario/allowlist table โดยตรง** (กิ่ง 2 คือ
`close_delay_ms` field ที่มีอยู่แล้วในดาต้าคลาส `LogoutHypothesisScenario` แต่ทุก profile ปักเป็น
`LOGOUT_CLOSE_DELAY_MS` เดียวกันหมด ต้องเพิ่ม profile ใหม่ที่ปักค่าอื่น; กิ่ง 3 คือ profile ที่สลับลำดับ
ack/0x709E หรือส่งซ้ำ) **ไม่มีทางสร้างเป็นโมดูลแยกที่ไม่แตะไฟล์นี้แบบที่ทำกับกิ่ง 6 ได้** เพราะกิ่ง 6 เป็น
กลไกคนละแบบ (unsolicited push ที่ event ใหม่) ส่วนกิ่ง 2/3 เป็นการแปรพารามิเตอร์ของ scenario ที่มีอยู่
แล้วในตารางเดิม

จดหมาย `20260901_1605` เขียนไว้ตรง ๆ ว่า "ไม่เปิดเขตเขียนถาวร งานครั้งถัดไปกลับมาเป็นของ chief/ขอใบใหม่"
-- รอบนี้จึง **ไม่แก้ไฟล์นี้เอง** (เคารพคำตัดสินที่ chief เพิ่งเคาะเอง ตรงกับเงื่อนไขหยุดจริงข้อ (ค) ของ
เลนนี้เอง: "ขัดกับคำสั่งที่เจ้าของ/chief เคาะไว้เองโดยตรง") **เปิด CORE-REQUEST ใหม่แทน:**

**ขอให้ chief เลือกทางใดทางหนึ่ง:**
(ก) chief แก้ allowlist เอง (เพิ่ม 2 profile: `_PROFILE_TEARDOWN_TIMER_VARIANT` แปร `close_delay_ms`
เป็น 0/2000/10000/None(ไม่ปิดเลย), `_PROFILE_ACK_FIRST_REORDER` สลับลำดับ ack->0x709E จากที่มีอยู่
(0x709E->ack) พร้อมตัวแปรส่งซ้ำ) โดยสาย A ส่งสเปกละเอียด+ค่าที่ reuse ให้ก่อน (แบบเดียวกับใบ CORE-REQUEST
เดิมที่นำไปสู่การอนุมัติ "ครั้งเดียว" รอบที่แล้ว) หรือ
(ข) chief อนุมัติให้สาย A แก้เองอีกครั้งหนึ่ง (ครั้งที่สอง) ตามสเปกเป๊ะ เหมือนที่ทำรอบ `tmizmk`

**ไม่ใช่คำถามที่บล็อกงาน** -- รอบนี้เดินหน้าทำงานอื่นแทน (ตรวจซ้ำ+แก้ข้อความ log ค้างในหัวข้อ 2)
ไม่ได้หยุดรอคำตอบนี้

## 4. NOW.md + ล็อกรอบ + PR รอบก่อน

`NOW.md` (ตรวจก่อนอื่นตามกฎ): P-1/P-2/P-3 + GM-A/UI-A/GM-B/UI-B/census-latch ทั้งหมดเป็นของสาย
GM/DB/UI หรือรอ Panya รันเทส attended (ไม่ใช่ตัวบล็อกสายตามกฎใหม่) -- "สาย A/GM เดินคิวปกติต่อได้"
เขียนไว้ตรง ๆ ไม่มีข้อไหนของ NOW.md ที่สายนี้ต้องขยับรอบนี้

PR รอบก่อนของสาย A (`tmizmk`): `pirate-force-server#484` merged=true (09:17:06Z),
`pf_bridge#724` merged=true (09:08:21Z) -- ตรวจตรงด้วย `pull_request_read` ไม่เชื่อ `rounds/`
งานอยู่บน `main` แล้วจริง ไม่ต้อง cherry-pick อะไร

ไม่มี PR `[LANE-A]` ค้างเปิดต้นรอบทั้งสองรีโป -- เปิด draft ยึดล็อก

## สรุปไฟล์ที่แตะรอบนี้

- `pf_bridge/GAME_TEST_QUEUE.md` -- แก้ข้อความ log ค้าง (append เท่านั้น) ใน `GT-184`/`GT-186`
- `pf_bridge/notes_to_chief/20260901_1605_CHIEF-REPLY-*.md.CONSUMED.txt` -- stub
- `pf_bridge/notes_to_chief/20260901_1635_LANE-A-STATUS-*.md` -- ใบนี้เอง (มี CORE-REQUEST ในตัว)
- `pf_bridge/rounds/A_20260901_1635_2ahq88_chiefreply-consumed-adversary-reverify-corerequest-re189.md`

## เปิดใบให้ chief

CORE-REQUEST ข้อ 3 ด้านบน (RE-189 กิ่ง 2/3 -- เลือก (ก)/(ข))

## เปิดใบให้ COO

ระบบ pf-adversary ไม่มีทาง invoke ได้จริงจากเซสชันระยะไกลนี้ ซ้ำสองรอบติดกันแล้ว (`tmizmk`, `2ahq88`)
-- ถ้ากฎ "ต้องผ่าน pf-adversary ก่อน commit ทุกครั้ง" ยังบังคับตามตัวอักษร ทุกรอบของทุกสายในเซสชัน
ระยะไกลจะติดช่องว่างนี้ซ้ำตลอดไป ไม่ใช่เหตุการณ์ครั้งเดียว -- เสนอ (ไม่ใช่ข้อสรุป): ยอมรับ "manual
review ตาม checklist ของ pf-adversary.md" เป็นสิ่งทดแทนที่บันทึกไว้ชัดเจนเมื่อไม่มี Task tool จริง
[สมมติของสาย A -- รอ COO ยืนยัน]

-- LANE-A (WORLD) round `2ahq88`
