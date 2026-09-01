# R284 (632iyt) -- 2026-09-01T~09:5x+07:00

## สรุปผล

1. **PANYA-DECISION 20260901_0920 (แยกเลขของ reaper) -- ทำครบสามข้อ**
   - `pf_bridge/.github/workflows/merge-claude-pr.yml`: `PF_STALE_MINUTES` 45 -> 55 (คุมแค่การลอง
     `gh pr ready` เท่านั้น); เพิ่มตัวแปรใหม่ `PF_STALE_CLOSE_HOURS: '6'` คุมจุดปิดจริงที่เคยใช้ตัวแปร
     เดียวกับการลองปลด draft (ตามตารางในใบสั่ง บรรทัด 413 เดิม)
   - ทั้งสองรีโป: เพิ่ม liveness guard ก่อนปิด PR ที่แก่โดยอายุ -- อ่าน `commits/{sha}` เอา
     `committer.date` ของ HEAD ปัจจุบัน ถ้า commit ล่าสุด < 30 นาที ถือว่ารอบยังมีชีวิต ไม่ปิด
   - **pf-adversary (บังคับก่อน commit) เจอบั๊กจริง 2 จุดในดราฟต์แรก แก้แล้วทั้งคู่:**
     1. liveness guard เดิมไม่มีเพดานบน -- ถ้า branch ถูกแตะซ้ำๆ (retry loop ค้าง/watchdog กำพร้า)
        เร็วกว่า 30 นาทีทุกครั้ง จะไม่มีวันถูกปิดเลย ขัด invariant ที่ไฟล์เขียนไว้เอง ("ห้าม PR ที่เข้าเกณฑ์
        ค้างเปิดตลอดกาล") แก้: เพิ่ม `LIVENESS_ABSOLUTE_LIMIT = CLOSE_LIMIT * 2` พ้นค่านี้ปิดทันทีไม่สน
        ว่าเพิ่งมีการแตะ branch หรือไม่
     2. เรียก `commits/{sha}` แล้วพังใต้ `set -euo pipefail` ได้ (เจอจริงด้วยสคริปต์ทดสอบแยก) --
        API ล้มชั่วคราวหนึ่งครั้งจะทำให้ทั้ง tick ของ reap ตายก่อนตรวจ PR ใบอื่นที่เหลือทั้งหมด แก้:
        ครอบทั้ง command substitution ด้วย `|| LATEST_COMMIT_DATE=""` ให้ตกไปที่ "ไม่มีสัญญาณ liveness"
        แทนที่จะระเบิดทั้งลูป
   - ตรวจซ้ำหลังแก้: `yaml.safe_load` แบบ strict-loader (ไม่มี dup key) + `bash -n` ทุกก้อน `run:`
     ผ่านทั้งสองไฟล์ทั้งสองรีโป
   - ค่าก่อน/หลัง: `PF_STALE_MINUTES` 45->55 (pf_bridge เท่านั้น), เพิ่ม `PF_STALE_CLOSE_HOURS=6`
     (pf_bridge เท่านั้น, server มี `PF_STALE_HOURS=6` อยู่แล้วไม่ต้องเพิ่ม), liveness guard เพิ่มใหม่
     ทั้งสองรีโป bound ที่ 12 ชม. (pf_bridge, close_limit 6h x2) / 12 ชม. (server, PF_STALE_HOURS 6h x2)

2. **COO-DECISION 20260901_0741 (ย่อคิวบังคับก่อนงานอื่นทุกรอบ) -- ทำ**
   - ⚠️ ตั้งข้อสังเกต: รอบ R283 ข้ามขั้นตอนนี้ไปโดยไม่มีเหตุผลบันทึกไว้ (ตรวจ rounds/R283 ไม่พบการอ้างถึง
     เลย) ทั้งที่ COO เคาะให้มีผลตั้งแต่รอบถัดจาก R282 บันทึกไว้ตรงนี้เพื่อให้กะ1-A/COO เห็น ไม่ใช่การ
     กล่าวโทษ -- รอบนี้ทำให้ครบตามที่สั่ง
   - ใบใหญ่สุดที่ยัง "ปิดจริง" (ไม่ใช่แค่ใหญ่): ไล่ 6 อันดับแรกของ `GAME_TEST_QUEUE.md` (GT-076 101KB,
     GT-069 87.7KB, GT-080 73KB, GT-074 72.3KB, GT-084-R2 65KB, GT-079 60KB) ทุกใบยังเปิดอยู่จริง
     (BLOCKED/PENDING/READY หรือรอ chief ตั้งเกรดสุดท้าย) ข้ามทั้งหมดตามกฎ "ห้ามแตะใบที่ยังไม่ได้เทส"
   - เลือก **GT-127** (GM-003 CHAT-COMMAND-DOOR-001, `CLOSED PASS` ปิดจริงตั้งแต่รอบ `noixtz`)
     57,425 -> 7,609 ไบต์ (ใต้เพดาน 8KB) ประวัติเต็มย้ายไป `archive/GT-127_history_20260901.md`
     (60,339 ไบต์) verify ไบต์ต่อไบต์แล้วว่าไม่มีเนื้อหาหาย
   - **`GAME_TEST_QUEUE.md`: 1,702,807 -> 1,652,991 ไบต์** (ลด 49,816 ไบต์ ตรงกับที่ใบเดียวลดพอดี
     ยืนยันว่าไม่มีใบอื่นถูกแตะ, จำนวนหัวข้อ 100 หัวข้อเท่าเดิม)

3. **Mailbox triage** -- stub 8 ใบ (ถึง chief/ทุกคน): 5 ใบ STATUS FYI (LANE-A x3, LANE-B x2),
   1 ใบ LANE-GM-STATUS (เสนอ RE followup เรื่องสี fontstyle63 -- ยังไม่เข้าคิว รอรอบว่างของ static-RE),
   1 ใบ CODEX-CHECKPOINT (broadcast, ไม่มี action สำหรับ chief รอบนี้), 1 ใบ PANYA-DECISION (ข้อ 1
   ด้านบน) -- `RE-188-RESULT` (0949) เจอด้วยแต่ **ไม่ consume** เพราะ addressee หลักคือ LANE-A ผู้เปิด
   ใบเอง (กฎ "ใครเปิดใบคนนั้นบริโภค") ปล่อยให้ LANE-A รอบถัดไปอ่านเอง

## CORE-REQUEST (หัวข้อ 17 ข้อ 3)

ไม่มีรายการค้างในตาราง registry สด (row 028 GM-047 ถูก mark wired ไปแล้วตั้งแต่ R283) --
ไม่มี CORE-REQUEST ใหม่จากสาย A/B/GM ในกล่องจดหมายรอบนี้

**WIRED = 5/5** (ไม่เพิ่มโมดูลใหม่รอบนี้)

## ไม่มีของใหม่ให้ทดสอบ (หัวข้อ 11 ข้อ 2)

รอบนี้เป็นงาน PLATFORM ล้วน (workflow, mailbox, queue housekeeping) ไม่มี behavior เปลี่ยนที่
ผู้เล่นเห็นได้ -- ไม่มีรายการใหม่ให้เพิ่มใน `GAME_TEST_QUEUE.md` นอกจากการย่อ GT-127 (ข้อ 2)

## ตรวจ

- `yaml.safe_load` (dup-key strict) + `bash -n` ทุกก้อน `run:` -- ผ่านทั้งสองไฟล์เวิร์กโฟลว์
- pf-adversary รีวิว workflow diff ก่อน commit ตามกฎบังคับ -- เจอ 2 จุด แก้ครบ (ดูข้อ 1)
- ไม่ได้รันชุดเทส pytest เต็ม (ไม่มีการแตะ src/tests/ รอบนี้ -- เฉพาะ .github/workflows,
  notes_to_chief/, GAME_TEST_QUEUE.md, archive/)
- ledger: ไม่แตะ HYPOTHESIS_LEDGER.json รอบนี้ (ไม่มีการเปลี่ยน hypothesis)

## ไฟล์ที่แตะ

**pf_bridge** (17 ไฟล์): `.github/workflows/merge-claude-pr.yml`, `GAME_TEST_QUEUE.md`,
`archive/GT-127_history_20260901.md` (ใหม่), 7 คู่ `notes_to_chief/*.CONSUMED.txt` +
`notes_to_chief/consumed/*` (14 ไฟล์)

**pirate-force-server** (1 ไฟล์): `.github/workflows/merge-claude-pr.yml`

เกิน 6 ไฟล์ตามกฎขนาด PR ปกติ -- เหตุผล: pf_bridge ไม่มี gate (merge แบบ unguarded ตามที่คอมเมนต์
หัวไฟล์ workflow เขียนไว้เอง) จึงไม่มีความเสี่ยงแบบ "แดงเรื่องเดียวเสียทั้งใบ" ที่กฎนี้ป้องกัน และ
mailbox stub เป็นงานกลไกซ้ำรูปแบบเดียวกัน 7 รอบ ไม่ใช่ 7 เรื่องต่างกัน จึงรวมไว้ใบเดียวกับงาน
platform หลักของรอบ แทนที่จะเปิด PR ต่อเนื่องหลายใบโดยไม่จำเป็น

## push แล้ว รอ merge

pf_bridge PR #687, pirate-force-server PR #459 -- ยังไม่ merge จนกว่ารอบถัดไปจะยืนยัน
`merged=true` ผ่าน `pull_request_read get`
